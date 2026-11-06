> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 2. Image-based lighting and hybrid direct lighting

### 2.1 Loading and pre-filtering

```js
import * as THREE from 'three';                       // or 'three/webgpu'
import { HDRLoader } from 'three/addons/loaders/HDRLoader.js';
import { EXRLoader } from 'three/addons/loaders/EXRLoader.js';
import { UltraHDRLoader } from 'three/addons/loaders/UltraHDRLoader.js'; // JPEG + gain map: far smaller download than .hdr/.exr

export async function loadEnvironment( renderer, scene, url, { rotationY = 0, intensity = 1, showBackground = true } = {} ) {

	const loader = url.endsWith( '.exr' ) ? new EXRLoader() : url.endsWith( '.jpg' ) ? new UltraHDRLoader() : new HDRLoader();
	loader.setDataType( THREE.HalfFloatType );           // half the VRAM of FloatType; enough for IBL
	const equirect = await loader.loadAsync( url );
	equirect.mapping = THREE.EquirectangularReflectionMapping;

	const pmrem = new THREE.PMREMGenerator( renderer );  // WebGPU: call after await renderer.init()
	const envRT = pmrem.fromEquirectangular( equirect ); // GGX-prefiltered cube-UV mip chain
	pmrem.dispose();

	scene.environment = envRT.texture;
	scene.environmentIntensity = intensity;              // global IBL scale (r163+)
	scene.environmentRotation.set( 0, rotationY, 0 );    // Euler, radians (r162+)

	if ( showBackground ) {

		scene.background = equirect;                     // full-res sharp backplate
		scene.backgroundRotation.copy( scene.environmentRotation ); // keep reflections aligned with what is seen
		scene.backgroundIntensity = intensity;
		scene.backgroundBlurriness = 0;                  // >0 samples PMREM mips instead

	} else {

		equirect.dispose();

	}

	return envRT; // envRT.dispose() when switching environments

}
```

- Assigning an equirect texture straight to `scene.environment` also works: both renderers PMREM-convert it automatically. Explicit PMREM lets you dispose the source, reuse the result, and control timing to avoid a first-frame hitch.
- Studio lighting without a download: `pmrem.fromScene( new RoomEnvironment(), 0.04 ).texture` (the r187 SSR and AO examples use it).
- Choose HDRIs captured unclipped, ideally 16+ stops, and **2K is enough for lighting**. PMREM's top level is small. Use a separate higher-resolution LDR or Ultra HDR backplate only if the background is visible and sharp.

### 2.2 Splitting the sun out of the HDRI

A clipped or compressed sun in the HDRI gives weak, shadowless key light. Paint the sun out (or clamp it), then add a shadow-casting `DirectionalLight` along the sun direction. Three's equirect lookup (`common.glsl.js`) is `u = atan(dir.z, dir.x)/2π + 0.5`, `v = asin(dir.y)/π + 0.5`. Inverting it for the brightest texel (`HDRLoader` sets `flipY = true`, so data row 0 is the top of the image, v = 1):

```js
// data: Float32Array/Uint16 RGBA from equirect.image.data (convert half-floats with THREE.DataUtils.fromHalfFloat)
function sunDirectionFromEquirect( lumAt, width, height, envRotationY = 0 ) {

	let best = - 1, bx = 0, by = 0;
	for ( let y = 0; y < height; y ++ ) for ( let x = 0; x < width; x ++ ) {

		const l = lumAt( x, y ); if ( l > best ) { best = l; bx = x; by = y; }

	}

	const u = ( bx + 0.5 ) / width, v = 1 - ( by + 0.5 ) / height;
	const phi = ( u - 0.5 ) * 2 * Math.PI, theta = ( v - 0.5 ) * Math.PI;
	const dir = new THREE.Vector3( Math.cos( theta ) * Math.cos( phi ), Math.sin( theta ), Math.cos( theta ) * Math.sin( phi ) );
	return dir.applyAxisAngle( new THREE.Vector3( 0, 1, 0 ), envRotationY ); // apply scene.environmentRotation.y
	// sun.position.copy( dir ).multiplyScalar( D ); sun.target at scene centre

}
```

*(The inversion follows algebraically from the shader formula. I have not checked it on a GPU against a rendered reflection, and the sign of the `environmentRotation` application should be confirmed visually once.)*

### 2.3 Pairing IBL with direct lights

| Light | Role | Constraints |
|---|---|---|
| `DirectionalLight` | Sun / key; the only cheap large-area shadow caster | Fit the shadow frustum (§3.2). Exterior intensity is about 5–10× the sky's contribution. |
| `SpotLight` | Practicals, stage lights; `.map` projects a gobo; `penumbra` 0.3–1 for real fixtures | Perspective shadow: keep `shadow.camera.near` as large as possible. `IESSpotLight` (WebGPU only, `src/lights/webgpu/`) takes real photometric profiles. |
| `RectAreaLight` | Windows, softboxes, LED panels, TV glow | **No shadows.** Affects only `MeshStandardMaterial`/`MeshPhysicalMaterial`. Needs LTC tables: WebGL `RectAreaLightUniformsLib.init()`; WebGPU `THREE.RectAreaLightNode.setLTC( RectAreaLightTexturesLib.init() )`. |
| `HemisphereLight`/`AmbientLight` | Avoid in photoreal scenes | Constant, unoccluded fill; flattens form. Use IBL or probes instead. |

**Avoid double-counting.** When the HDRI already contains a window or the sun, the matching direct light replaces it: paint it out of the HDRI or lower `environmentIntensity`. Interiors lit mainly by practicals typically need `environmentIntensity` 0.1–0.4. Without occlusion the IBL lights the inside of cupboards as brightly as the open room.

### 2.4 Approximating global illumination

Ranked by cost and quality:

| Technique | API (r187) | What it captures | Cost | When |
|---|---|---|---|---|
| Single SH probe | `LightProbe` + `LightProbeGenerator.fromCubeTexture()` / `.fromCubeRenderTarget()` | One L2 (9-coefficient) irradiance for the whole scene | ~free | Outdoor, open scenes |
| **Probe grid (irradiance volume)** | `LightProbeGrid` (WebGPU) / `LightProbeGridWebGL` — `new LightProbeGrid( sizeX, sizeY, sizeZ, resX, resY, resZ )`, `probes.bake( renderer, scene, { cubemapSize: 32, near: 0.05, far: 20, bounces } )`, `scene.add( probes )` | Spatially varying diffuse bounce, colour bleeding; dynamic objects pick it up | Bake once (or on change); per-pixel trilinear SH lookup | **Interiors with moving objects.** r184+ |
| **Baked lightmaps** | `material.lightMap`, `lightMap.channel = 1` | Full multi-bounce diffuse GI + soft shadows at any quality | Zero runtime; VRAM + second UV set | **Static architecture: best quality per millisecond** |
| In-browser lightmap bake | `LightMapper( renderer, resolution, irradianceFn )` + `unwrapUVs( scene, { resolution, padding } )`, fed by `lightProbeGridIrradiance` or `vxgiIrradiance` | Lightmaps generated on the client | Progressive, seconds | r187, experimental |
| SSGI | `ssgi( color, depth, normal, camera )` (WebGPU) | One-bounce screen-space diffuse + AO | High: run at `resolutionScale = 0.5`, `sliceCount` 1–2, `stepCount` 8–12, with TRAA | Hero shots on desktop GPUs |
| VXGI | `VXGIVolume` + `vxgiIrradiance( volume, { coneCount: 3 } )` | Voxel cone-traced diffuse | High | r186+, experimental |

**Lightmap workflow from Blender (dual UV):**

1. Add a second UV map ("UVMap.001"). Unwrap it with *Lightmap Pack* or *Smart UV Project*: no overlaps, island margin ≥ 2–4 texels at the target resolution.
2. Bake with Cycles, *Diffuse* pass, **Direct + Indirect enabled, Color disabled**. Three multiplies the lightmap by the material albedo: `lights_fragment_maps` adds `lightMapTexel.rgb * lightMapIntensity` to irradiance, which then goes through the diffuse BRDF. Baking albedo in would apply it twice. Save as 16-bit half EXR or Radiance HDR.
3. Export glTF with both UV sets. They arrive as `uv` and `uv1`.
4. In three:

```js
const lm = await new EXRLoader().setDataType( THREE.HalfFloatType ).loadAsync( 'room_lightmap.exr' );
lm.channel = 1;          // second UV set (Texture.channel, default 0)
lm.flipY = false;        // glTF UV convention
// colorSpace already LinearSRGBColorSpace from EXRLoader
mesh.material.lightMap = lm;
mesh.material.lightMapIntensity = 1;
mesh.material.envMapIntensity = 0.25; // IBL diffuse is ALSO added (iblIrradiance) -> avoid double bounce
```

> [!IMPORTANT]
> In `lights_fragment_maps` the lightmap and the PMREM diffuse irradiance are both added. A lightmap that already contains sky light plus a full-strength `scene.environment` double-counts the bounce. Either lower `envMapIntensity` on lightmapped materials, or bake direct light only and let the IBL supply the sky.
