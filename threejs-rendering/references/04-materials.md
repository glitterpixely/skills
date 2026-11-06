> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 4. PBR and micro-surface materials

### 4.1 Rules for physically plausible inputs

- **Albedo (linear):** dielectrics 0.02–0.9. Charcoal is about 0.04, fresh snow about 0.85. Never use 0 or 1. In sRGB 8-bit terms that is roughly 30–240.
- **Metals:** `metalness = 1`, with `color` = linear F0 (*settled values*, Hoffman / RTR4): gold `(1.000, 0.766, 0.336)`, silver `(0.972, 0.960, 0.915)`, aluminium `(0.913, 0.922, 0.924)`, copper `(0.955, 0.638, 0.538)`, iron `(0.562, 0.565, 0.578)`. Set them with `color.setRGB( r, g, b )`, which writes linear values. Metalness between 0 and 1 belongs only at transitions such as rust edges or dust over metal.
- **Roughness floor:** r187 clamps `material.roughness = max( roughnessFactor, 0.045 )`, then adds `geometryRoughness`, a normal-derivative term that suppresses specular aliasing on curved low-poly surfaces (`lights_physical_fragment`). Real surfaces rarely go below 0.05–0.1. Pure 0.0 reads as CG.
- **Specular F0 of dielectrics:** F0 = ((n − 1) / (n + 1))². `ior` drives it, as does `specularIntensity` (scales F0) with `specularColor` (tints it).

### 4.2 Dielectrics and glass

```js
const glass = new THREE.MeshPhysicalMaterial( {
	color: 0xffffff, metalness: 0, roughness: 0.02,
	transmission: 1,                 // physically based see-through (not opacity)
	ior: 1.52,                       // valid range 1.0–2.333 in three
	thickness: 0.006,                // metres in the mesh's local space; 0 = thin-walled
	attenuationColor: new THREE.Color( 0.82, 0.95, 0.9 ),  // Beer–Lambert tint
	attenuationDistance: 0.4,        // distance at which light is tinted to attenuationColor
	dispersion: 0.31,                // 20 / Abbe number (KHR_materials_dispersion)
	specularIntensity: 1,
} );
renderer.transmissionResolutionScale = 0.5; // WebGL: halves the transmission pre-pass cost
```

- **Beer–Lambert:** transmittance T(d) = attenuationColor^(d / attenuationDistance). Thick glass goes greener or darker realistically, which flat `opacity` cannot do.
- **Cost model (WebGL):** transmissive objects trigger an extra opaque-scene render into a mipmapped target, used for rough refraction blur. Transmissive objects **do not see each other** in it. Keep transmissive draw calls few and use `transmissionResolutionScale`.

| Material | IOR | F0 | Abbe → `dispersion` |
|---|---|---|---|
| Air | 1.0003 | 0 | — |
| Ice | 1.31 | 0.018 | — |
| Water | 1.333 | 0.020 | ~56 → 0.36 |
| Skin / organic tissue (approx.) | 1.40 | 0.028 | — |
| Acrylic (PMMA) | 1.49 | 0.039 | ~58 → 0.34 |
| Generic glass / glTF default | 1.50 | 0.040 | — |
| Soda-lime / BK7 crown glass | 1.52 | 0.043 | 64 → 0.31 |
| Amber | 1.55 | 0.046 | — |
| PET plastic | 1.57 | 0.049 | — |
| Polycarbonate | 1.585 | 0.051 | ~30 → 0.67 |
| Sapphire | 1.77 | 0.077 | 72 → 0.28 |
| Dense flint glass | 1.6–1.9 | 0.053–0.096 | ~30 → 0.67 |
| Diamond | 2.417 → **clamp to 2.333** | 0.172 (0.160 at 2.333) | 55 → 0.36 |

IOR, F0 and the dispersion conversion were computed from these IORs and Abbe numbers; the IOR and Abbe values themselves are *settled reference data*. Diamond cannot reach its true IOR in three. Compensate with `dispersion` and a high-frequency HDRI.

### 4.3 Layered surfaces: clearcoat

Clearcoat IOR is fixed at 1.5 (F0 = 0.04). Clearcoat light is occluded by `aoMap` (see `aomap_fragment`).

| Surface | Base layer | Clearcoat |
|---|---|---|
| Metallic car paint | `metalness` 0.6–1, `roughness` 0.3–0.45, flake normal map (fine noise, high tiling) | `clearcoat: 1`, `clearcoatRoughness: 0.02–0.06`, `clearcoatNormalMap` = low-frequency orange peel, `clearcoatNormalScale ≈ (0.05, 0.05)` |
| Wet asphalt / stone | Albedo darkened ×0.5–0.7 (porous surfaces absorb more water), roughness lowered | `clearcoat` driven by a puddle mask, `clearcoatRoughness: 0.03–0.08` |
| Varnished wood | `roughness` 0.5–0.7, wood normal | `clearcoat: 0.7–1`, `clearcoatRoughness: 0.1–0.3` |
| Carbon fibre | Anisotropic weave (§4.4) | `clearcoat: 1`, `clearcoatRoughness: 0.03` |

### 4.4 Fabrics, organics and special lobes

- **Sheen (Charlie distribution):**
  - Velvet: `sheen: 1`, `sheenRoughness: 0.3–0.5`, `sheenColor` = a brighter, lower-saturation version of the fabric hue, base `roughness: 0.8–1`.
  - Cotton or wool: `sheenRoughness: 0.7–1`, weaker `sheenColor`.
  - Sheen is also occluded by AO.
- **`diffuseRoughness`** (r187, with `diffuseRoughnessMap` in red): rough diffuse response that flattens terminators. Use for clay, plaster, moon dust and cloth, at 0.5–1.
- **Anisotropy:**
  - Brushed metal: `anisotropy: 0.6–0.9`, `anisotropyRotation` in radians.
  - `anisotropyMap`: RG = direction, B = strength (glTF KHR_materials_anisotropy).
  - Export **tangents** from the DCC tool (or call `BufferGeometryUtils.computeMikkTSpaceTangents`). Without them three falls back to derivative tangents, which are less stable on curved UV seams.
  - The IBL path has a dedicated `getIBLAnisotropyRadiance`.
- **Iridescence** (thin-film): soap bubbles, oil slicks, anodised titanium, beetle shells. `iridescence: 1`, `iridescenceIOR: 1.3`, `iridescenceThicknessMinimum: 100`, `iridescenceThicknessMaximum: 400` nm (the defaults; r187 deprecated the old `iridescenceThicknessRange` array, #35039), with variation from `iridescenceThicknessMap`.
- **Retroreflectivity** (r186): road signs, bike reflectors, safety tape. `retroreflectivity: 1` mirrors the specular lobe back toward the light.
- **Subsurface scattering** has no physical model in `MeshPhysicalMaterial`. Approximations by cost:
  1. **Skin:** `roughness 0.45–0.6`, F0 ≈ 0.028 (`ior: 1.4`), detail normal + `specularIntensityMap` for pores, low warm `sheen` (0.1–0.25) for peach fuzz. Never use `metalness`.
  2. **Fast translucency:** `MeshSSSNodeMaterial` (WebGPU), Barré-Brisebois' approximation: `thicknessColorNode`, `thicknessDistortionNode` (0.1), `thicknessAmbientNode` (0.4), `thicknessAttenuationNode` (0.8), `thicknessPowerNode` (2), `thicknessScaleNode` (16), plus a baked thickness map. WebGL: `SubsurfaceScatteringShader` (`webgl_materials_subsurface_scattering`).
  3. **Wax, jade, marble:** `transmission: 0.3–0.8` + `thickness` + warm `attenuationColor` with short `attenuationDistance`. Expensive, but it carries depth correctly.
  4. **Foliage:** `side: DoubleSide`, alpha-tested (`alphaTest: 0.5`, **not** blending), and a TSL back-light term added to `emissiveNode`: `max(dot(−N, L), 0) × leafTransmissionColor × thickness`.

### 4.5 Texture packing and normal space

- **ORM (glTF):** R = occlusion, G = roughness, B = metalness. Assign the same texture to `aoMap`, `roughnessMap` and `metalnessMap`: three samples `.r`, `.g` and `.b` respectively (`roughnessmap_fragment`: `roughnessFactor *= texelRoughness.g`; `metalnessmap_fragment`: `.b`). That is one fetch path, one upload and one KTX2 UASTC file. The roughness and metalness factors multiply the map, so set `roughness: 1, metalness: 1` when the map is authoritative.
- **AO** (`aomap_fragment`) multiplies **indirect diffuse**, and applies `computeSpecularOcclusion` to indirect specular. It never darkens direct light. A baked AO map that looks too strong usually means the IBL is too strong.
- **`TangentSpaceNormalMap`** (default) is for anything deforming or reused across meshes. glTF uses the OpenGL (+Y) convention. GLTFLoader handles the flip when it falls back to derivative tangents, so do not flip glTF normals manually. For DirectX (−Y) maps from other sources, set `normalScale.y = -1`.
- **`ObjectSpaceNormalMap`** suits rigid, non-instanced-with-rotation-variety static meshes (baked hero props). It needs no tangents and avoids seam issues, but cannot be skinned or reused.
- **Specular aliasing from normal maps:** keep mipmaps on, use `texture.anisotropy = renderer.capabilities.getMaxAnisotropy()` (WebGL) or `renderer.getMaxAnisotropy()` (WebGPU), and pre-filter roughness against normal variance offline (Toksvig / LEAN) for high-frequency maps. TRAA covers the rest.

### 4.6 Extending materials without breaking PBR

The rule: modify **inputs** to the lighting model (albedo, roughness, metalness, normal, AO, emissive). Never modify its **outputs** (`outgoingLight`, `gl_FragColor`). Then IBL, shadows, AO contexts, tone mapping and every post effect stay consistent.

**TSL / `MeshPhysicalNodeMaterial` (WebGPU, and the WebGL2 backend via `forceWebGL`):** dust on up-facing surfaces, fingerprint/smudge roughness, and dust turning metal into a dielectric.

```js
import * as THREE from 'three/webgpu';
import { texture, uv, normalWorld, positionWorld, mx_fractal_noise_float, smoothstep, mix, vec3, float, uniform, clamp, materialRoughness, materialColor } from 'three/tsl';

const dustAmount = uniform( 0.6 );
const smudge = texture( smudgeTex, uv().mul( 4 ) ).r;                      // 0..1 data (NoColorSpace)
const dustNoise = mx_fractal_noise_float( positionWorld.mul( 3.0 ) ).mul( 0.5 ).add( 0.5 );
const dustMask = smoothstep( 0.55, 0.95, normalWorld.y ).mul( dustNoise ).mul( dustAmount ).toVar();

const mat = new THREE.MeshPhysicalNodeMaterial( { color: 0x8a8f94, metalness: 1, roughness: 0.32 } );
mat.colorNode = mix( materialColor, vec3( 0.42, 0.40, 0.37 ), dustMask );   // dust albedo, linear
mat.roughnessNode = clamp( mix( materialRoughness.add( smudge.mul( 0.25 ) ), float( 0.9 ), dustMask ), 0.045, 1.0 );
mat.metalnessNode = mix( float( 1 ), float( 0 ), dustMask );               // dust is a dielectric layer
```

All physical slots are node-assignable in r187: `clearcoatNode`, `clearcoatRoughnessNode`, `clearcoatNormalNode`, `sheenNode`, `sheenRoughnessNode`, `iridescenceNode`, `iridescenceIORNode`, `iridescenceThicknessNode`, `specularIntensityNode`, `specularColorNode`, `iorNode`, `transmissionNode`, `thicknessNode`, `attenuationDistanceNode`, `attenuationColorNode`, `dispersionNode`, `retroreflectivityNode`, `anisotropyNode`, `diffuseRoughnessNode`. Base slots: `colorNode`, `normalNode`, `roughnessNode`, `metalnessNode`, `aoNode`, `emissiveNode`. For tiling without UV seams, `triplanarTexture` is exported from `three/tsl`.

**`onBeforeCompile` (WebGLRenderer, built-in materials):** the same idea, injected **after** the chunks that define the inputs:

```js
const mat = new THREE.MeshPhysicalMaterial( { color: 0x8a8f94, metalness: 1, roughness: 0.32 } );
mat.onBeforeCompile = ( shader ) => {

	shader.uniforms.uDust = { value: 0.6 };
	shader.vertexShader = shader.vertexShader
		.replace( '#include <common>', '#include <common>\nvarying vec3 vWorldNormalDust;' )
		.replace( '#include <beginnormal_vertex>', '#include <beginnormal_vertex>\nvWorldNormalDust = normalize( mat3( modelMatrix ) * objectNormal );' );
	shader.fragmentShader = shader.fragmentShader
		.replace( '#include <common>', '#include <common>\nuniform float uDust;\nvarying vec3 vWorldNormalDust;' )
		.replace( '#include <color_fragment>', '#include <color_fragment>\nfloat dust = smoothstep( 0.55, 0.95, normalize( vWorldNormalDust ).y ) * uDust;\ndiffuseColor.rgb = mix( diffuseColor.rgb, vec3( 0.42, 0.40, 0.37 ), dust );' )
		.replace( '#include <roughnessmap_fragment>', '#include <roughnessmap_fragment>\nroughnessFactor = mix( roughnessFactor, 0.9, dust );' )
		.replace( '#include <metalnessmap_fragment>', '#include <metalnessmap_fragment>\nmetalnessFactor = mix( metalnessFactor, 0.0, dust );' );
	mat.userData.shader = shader; // to animate: mat.userData.shader.uniforms.uDust.value = x

};
mat.customProgramCacheKey = () => 'dust-v1'; // distinct program from un-patched physical materials
```

*Checked:* in r187's `ShaderLib.physical`, all six anchors exist, and `color_fragment` precedes `roughnessmap_fragment`, which precedes `metalnessmap_fragment`. The TSL material constructs without errors in Node (`check-materials.mjs`). Neither snippet has been compiled on a GPU in this session.
