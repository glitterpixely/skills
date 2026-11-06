> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 1. Colour management, tone mapping and renderer architecture

### 1.1 The linear workflow contract

- `ColorManagement.enabled = true` and `workingColorSpace = LinearSRGBColorSpace` are the defaults (`src/math/ColorManagement.js`). Do not disable it.
- **Hex and CSS colours** (`color.set('#c8a27a')`, `new Color(0x…)`) are read as sRGB and converted to linear. `color.setRGB(r, g, b)` with no colour-space argument writes **working-space (linear)** values. Use `setRGB` for physically measured values, such as metal F0.
- **GLTFLoader** tags `baseColorTexture`, `emissiveTexture`, `sheenColorTexture` and `specularColorTexture` as `SRGBColorSpace`, and reads colour factors as linear. Do not re-tag glTF textures.

| Texture slot | `texture.colorSpace` |
|---|---|
| `map`, `emissiveMap`, `sheenColorMap`, `specularColorMap`, background JPG/PNG/AVIF | `SRGBColorSpace` |
| `normalMap`, `roughnessMap`, `metalnessMap`, `aoMap`, ORM, `clearcoat*Map`, `transmissionMap`, `thicknessMap`, `iridescence*Map`, `anisotropyMap`, `displacementMap`, `diffuseRoughnessMap`, `specularIntensityMap` | `NoColorSpace` (default) |
| `.hdr` / `.exr` environments, float lightmaps | `LinearSRGBColorSpace` (`HDRLoader`/`EXRLoader` set it) |
| 8-bit PNG lightmap saved from Blender with the "Standard" view transform | `SRGBColorSpace` |

### 1.2 `WebGLRenderer` setup

```js
import * as THREE from 'three';

const renderer = new THREE.WebGLRenderer( {
	antialias: false,              // true only when rendering straight to screen with no post chain
	powerPreference: 'high-performance',
	stencil: false,
} );
renderer.setPixelRatio( Math.min( window.devicePixelRatio, 2 ) ); // cap: DPR 3 costs 2.25x the fragments of DPR 2
renderer.setSize( innerWidth, innerHeight );
renderer.outputColorSpace = THREE.SRGBColorSpace;   // default; sRGB OETF applied at output
renderer.toneMapping = THREE.AgXToneMapping;        // see 1.4
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;       // PCFSoftShadowMap removed in r186
```

`WebGLRenderer` applies tone mapping and the sRGB conversion **only when it renders to the screen** (render target `null`). With three's own `EffectComposer`, end the chain with `OutputPass`. With pmndrs, see §5.2.

### 1.3 `WebGPURenderer` setup

```js
import * as THREE from 'three/webgpu';

const renderer = new THREE.WebGPURenderer( {
	antialias: false,                       // MSAA conflicts with TRAA; use TRAA/SMAA in the pipeline
	outputBufferType: THREE.HalfFloatType,  // default; keeps HDR headroom through the post chain
	// forceWebGL: true                     // WebGL2 backend fallback, same node pipeline
} );
await renderer.init();                      // required before PMREM, KTX2 detectSupport, compile
renderer.setPixelRatio( Math.min( devicePixelRatio, 1.5 ) );
renderer.toneMapping = THREE.AgXToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
```

With a `RenderPipeline`, tone mapping and the colour-space conversion run at the end of the pipeline when `renderPipeline.outputColorTransform === true` (the default). Set it to `false` and call `renderOutput()` yourself when display-space effects (grain, chromatic aberration, vignette, SMAA) must run **after** tone mapping. See §5.3.

### 1.4 AgX vs ACES Filmic vs Khronos PBR Neutral

What the r187 shader code does (`tonemapping_pars_fragment.glsl.js`):

| Operator | Implementation | Highlight behaviour | Use for |
|---|---|---|---|
| `ACESFilmicToneMapping` | Stephen Hill's RRT+ODT fit, with input pre-scaled by **1/0.6** for "a brighter viewing environment" | High contrast. Saturated primaries skew in hue and clip to pure channels before they go white: bright blue drifts to purple, red and orange to yellow (*settled knowledge* about ACES 1.x fits). | Legacy look matching; games that want punch |
| `AgXToneMapping` | Filament/Blender AgX: Rec.2020 inset matrix → log2 encoding over −12.47 to +4.03 EV around 0.18 grey (≈16.5 stops) → sigmoid → outset | Bright saturated sources desaturate smoothly to white ("path to white"). Mid-tones are less contrasty and slightly desaturated. | **Default for photoreal scenes with bright emissives, sun, HDR skies** |
| `NeutralToneMapping` | Khronos PBR Neutral | Keeps base-colour hue and saturation through the mid-range and compresses only near-white highlights | **E-commerce, product configurators, brand-colour accuracy** |

**Calibrating exposure.** Two methods; use one per project:

1. **Grey-card method (relative units, recommended).** Put a Lambertian card with albedo 0.18 (`color.setRGB(0.18,0.18,0.18)`) facing the key light. Read the pixel back (`renderer.readRenderTargetPixels` on the final LDR target). Adjust `toneMappingExposure` until the card sits where your reference photo or grade wants mid-grey. AgX needs about +0.2 to +0.5 EV more than ACES for similar mid-tone brightness, because ACES carries a built-in 1/0.6 ≈ ×1.67 (+0.74 EV) pre-scale (*belief*: the +0.2 to +0.5 EV figure is a working range, not a measurement).
2. **EV100 method (absolute photometric units).** Exposure = 1 / (1.2 · 2^EV100) (Lagarde & de Rousiers, *Moving Frostbite to PBR*, 2014; saturation-based sensitivity):

$$\text{exposure} = \frac{1}{1.2 \cdot 2^{EV_{100}}}$$

| Scene | EV100 | `toneMappingExposure` |
|---|---|---|
| Dim interior | 5 | 2.60e-2 |
| Bright interior | 7 | 6.51e-3 |
| Overcast exterior | 12 | 2.04e-4 |
| Direct sun ("sunny 16") | 15 | 2.54e-5 |

> [!WARNING]
> Absolute units overflow half-float buffers. `HalfFloatType` saturates at 65,504. A visible sun disc is around 1.6×10⁹ cd/m², and a sunlit white wall is around 30,000 cd/m². Both clip or lose precision before the exposure multiply in the tone mapper. Use **pre-exposed units**: multiply all light intensities and `environmentIntensity` by the exposure on the CPU, and keep `toneMappingExposure ≈ 1`. Filament does the same.

### 1.5 Physical units

- **1 unit = 1 metre.** glTF 2.0 mandates metres. N8AO, GTAO, SSR, contact-shadow, DOF and shadow-bias parameters are all in world units, so a model imported at centimetre scale breaks every one of them. Fix the scale at import (`gltf.scene.scale.setScalar(0.01)`, or better, in the DCC tool).
- **Light units in three r187** (from source comments):

| Light | `intensity` unit | `power` (lumens) getter |
|---|---|---|
| `PointLight` | candela (cd) | P = 4π·I |
| `SpotLight` | candela (cd) | P = π·I (three's convention, independent of cone angle) |
| `RectAreaLight` | nits (cd/m²) | P = I·w·h·π |
| `DirectionalLight`, `HemisphereLight`, `AmbientLight` | illuminance (lux); the three source does not label it, KHR_lights_punctual defines directional in lux | — |

  Example: a 60 W-equivalent bulb is 800 lm → `light.power = 800` → 63.7 cd.
- **Decay.** `decay = 2` (inverse square) is the default for `PointLight` and `SpotLight`. `distance = 0` means no cut-off. `distance > 0` multiplies by a smooth windowing function that reaches zero at `distance`. That is fine for culling as long as `distance` is well past the visible falloff.
- **Why legacy setups look fake.** Before r155 the default mode multiplied punctual intensities by π. `useLegacyLights` was removed in r165. Old scenes ported verbatim (`decay: 1`, or a short `distance` used as the falloff) light up as linear gradients instead of inverse-square pools. You get flat walls with no hot spot near the lamp, and IBL-to-direct ratios that cannot be tuned consistently. Rule: never set `decay ≠ 2` on a photoreal light.
- **Keep ratios, not absolutes** (*settled photometry*): direct sun to sky illuminance runs about 5:1 to 10:1. An interior lamp should overpower IBL only within its own falloff radius.
