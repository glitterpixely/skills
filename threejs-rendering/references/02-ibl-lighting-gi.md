> Part of the `threejs-rendering` skill. Verified against three r187 (`0.187.0`); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 2. Image-based lighting, procedural sky, many-light scaling and GI

### 2.1 Loading HDRIs, `PMREMGenerator`, `SkyMesh` and `GroundedSkybox`

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
	const envRT = pmrem.fromEquirectangular( equirect ); // GGX-prefiltered cube render target mip chain (r187 #34585)
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
- Studio lighting without a download: `pmrem.fromScene( new RoomEnvironment(), 0.04 ).texture` (`'three/addons/environments/RoomEnvironment.js'`).
- Choose HDRIs captured unclipped, ideally 16+ stops, and **2K is enough for lighting**. Use a higher-resolution Ultra HDR JPEG or LDR backplate only if the background is visible and sharp.
- **Grounded HDRI backplate (`GroundedSkybox`):** For automotive or outdoor product turntables where infinite skybox parallax makes the car look like it floats in space, project the lower hemisphere onto a finite ground dome with `new GroundedSkybox( equirect, height, radius )` (`'three/addons/objects/GroundedSkybox.js'`).
- **Procedural Preetham sky + clouds (`SkyMesh`, `WebGPURenderer`):**
  ```js
  import { SkyMesh } from 'three/addons/objects/SkyMesh.js';

  const sky = new SkyMesh();
  sky.scale.setScalar( 10000 );
  sky.sunPosition.value.copy( sunDirection );
  sky.showSunDisc.value = 0; // hide solar disc during PMREM bake to avoid specular fireflies!
  const skyBakeScene = new THREE.Scene();
  skyBakeScene.add( sky );
  const pmrem = new THREE.PMREMGenerator( renderer );
  scene.environment = pmrem.fromScene( skyBakeScene ).texture;
  pmrem.dispose();

  sky.showSunDisc.value = 1;
  sky.renderOrder = - 1e6;          // REQUIRED when reversedDepthBuffer: true (SkyMesh.js:222 sets z = w,
  sky.material.depthTest = false;   // which is camera.near under reversed depth and overwrites closer meshes!)
  scene.add( sky );
  ```

### 2.2 Splitting the sun out of the HDRI

A clipped or compressed sun in the HDRI gives weak, shadowless key light. Paint the sun out (or clamp it), then add a shadow-casting `DirectionalLight` along the sun direction. Three's equirect lookup (`equirectUV` in `three.tsl.js`) is `u = atan(dir.z, dir.x)/2π + 0.5`, `v = asin(dir.y)/π + 0.5`. Furthermore, `materialEnvRotation` and `backgroundRotation` in r187 transform the world-space sampling vector by `_m1.makeRotationFromEuler(rotation).transpose()`, so a texel at unrotated azimuth `phi0` appears in world space at `phi = phi0 - envRotationY` (or `dir.applyEuler(new THREE.Euler(0, -envRotationY, 0))`). Also weight each texel by solid angle `sin(theta)` so wide polar rows near the zenith do not bias the peak, and honour `texture.flipY` (`HDRLoader` sets `flipY = true`, so row 0 is `v = 1`; `EXRLoader` sets `flipY = false`, so row 0 is `v = 0`):

```js
// image: equirect.image ({ width, height, data }); convert Uint16 half-floats with THREE.DataUtils.fromHalfFloat
function sunDirectionFromEquirect( image, envRotationY = 0, flipY = true ) {

	const { width, height, data } = image;
	let best = - 1, bestIdx = 0;
	for ( let y = 0; y < height; y ++ ) {

		const v = flipY ? 1 - ( y + 0.5 ) / height : ( y + 0.5 ) / height;
		const sinT = Math.sin( ( 1 - v ) * Math.PI );
		for ( let x = 0; x < width; x ++ ) {

			const i = ( y * width + x ) * 4;
			const lum = ( 0.2126 * data[ i ] + 0.7152 * data[ i + 1 ] + 0.0722 * data[ i + 2 ] ) * sinT;
			if ( lum > best ) { best = lum; bestIdx = y * width + x; }

		}

	}

	const ix = bestIdx % width, iy = ( bestIdx - ix ) / width;
	const u = ( ix + 0.5 ) / width;
	const v = flipY ? 1 - ( iy + 0.5 ) / height : ( iy + 0.5 ) / height;
	const theta = ( 1 - v ) * Math.PI;
	const phi = ( u - 0.5 ) * 2 * Math.PI - envRotationY; // minus envRotationY matches R_y(envRotationY)^T sampling
	return new THREE.Vector3(
		Math.sin( theta ) * Math.cos( phi ),
		Math.cos( theta ),
		Math.sin( theta ) * Math.sin( phi )
	).normalize();
	// sun.position.copy( dir ).multiplyScalar( D ); sun.target at scene centre

}
```

*(Verified on GPU in headless Chrome on both WebGPU and WebGL2 against both `scene.background` with `backgroundRotation.y` and a `PMREMGenerator` mirror sphere under `scene.environment` with `environmentRotation.y`; also unit-tested in `scripts/physical.mjs`.)*

### 2.3 Pairing IBL with direct lights and many-light scaling

| Light / Lighting system | Import & role | Constraints |
|---|---|---|
| `DirectionalLight` | `'three'` — Sun / key; the only cheap large-area shadow caster | Fit the shadow frustum (§3.2). Exterior intensity is about 5–10× the sky's contribution. |
| `SpotLight` / `IESSpotLight` / `ProjectorLight` | `'three'`, `'three/addons/lights/IESSpotLight.js'` (+ `IESLoader`), `'three/addons/lights/ProjectorLight.js'` | Perspective shadow: keep `shadow.camera.near` as large as possible. `IESSpotLight` and `ProjectorLight` require `WebGPURenderer`. |
| `RectAreaLight` | `'three'` — Windows, softboxes, LED panels, TV glow | **No shadows.** Affects only Standard/Physical materials. Needs LTC tables: WebGL `RectAreaLightUniformsLib.init()`; WebGPU `THREE.RectAreaLightNode.setLTC( RectAreaLightTexturesLib.init() )`. |
| `ClusteredLighting` (r187) | `'three/addons/lighting/ClusteredLighting.js'` — `renderer.lighting = new ClusteredLighting( maxLights, sliceX, sliceY, sliceZ )` | **WebGPU compute clustered shading** (`renderer.backend.isWebGPUBackend`) for dozens to hundreds of `PointLight` / `SpotLight` fixtures with finite `distance > 0`. |
| `DynamicLighting` (r187) | `'three/addons/lighting/DynamicLighting.js'` — `renderer.lighting = new DynamicLighting()` | Evaluates lights via a uniform array loop so adding/removing punctual lights at runtime does **not** recompile material shaders. |
| `HemisphereLight` / `AmbientLight` | Avoid in photoreal scenes | Constant, unoccluded fill; flattens form. Use IBL or probes instead. |

**Avoid double-counting.** When the HDRI already contains a window or the sun, the matching direct light replaces it: paint it out of the HDRI or lower `environmentIntensity`. Interiors lit mainly by practicals typically need `environmentIntensity` 0.1–0.4. Without occlusion the IBL lights the inside of cupboards as brightly as the open room.

### 2.4 Approximating global illumination

Ranked by cost and quality:

| Technique | Exact r187 import & API | What it captures | Cost | When |
|---|---|---|---|---|
| Single SH probe | `'three/addons/lights/LightProbeGenerator.js'` — `LightProbeGenerator.fromCubeRenderTarget( renderer, cubeRT )` | One L2 (9-coefficient) irradiance for the whole scene | ~free | Outdoor, open scenes |
| **Probe grid (irradiance volume)** | `'three/addons/lighting/LightProbeGrid.js'` (`LightProbeGridWebGL.js` on WebGL) — `new LightProbeGrid( width, height, depth, resX, resY, resZ )`, `probes.bake( renderer, scene, { cubemapSize: 32, near: 0.05, far: 20 } )`, `scene.add( probes )` | Spatially varying diffuse bounce, colour bleeding; dynamic objects pick it up | Bake once (or on change); per-pixel trilinear SH lookup | **Interiors with moving objects.** r184+ |
| **Baked lightmaps** | `material.lightMap`, `lightMap.channel = 1` | Full multi-bounce diffuse GI + soft shadows at any quality | Zero runtime; VRAM + second UV set | **Static architecture: best quality per millisecond** |
| In-browser lightmap bake | `'three/addons/lighting/LightMapper.js'` + `unwrapUVs` from `'three/addons/utils/UVsUtils.js'`, fed by `lightProbeGridIrradiance` or `vxgiIrradiance` | Lightmaps generated on the client | Progressive, seconds | r187, experimental (`WebGPURenderer`) |
| SSGI | `'three/addons/tsl/display/SSGINode.js'` — `ssgi( color, depth, normal, camera )` | One-bounce screen-space diffuse + AO | High: run at `resolutionScale = 0.5`, `sliceCount` 1–2, `stepCount` 8–12, with TRAA | Hero shots on desktop GPUs (`WebGPURenderer`) |
| VXGI | `'three/addons/lighting/VXGIVolume.js'` — `VXGIVolume` + `vxgiIrradiance( volume, { coneCount: 3 } )` | Voxel cone-traced diffuse | High | r186+, experimental (`WebGPURenderer`) |

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
