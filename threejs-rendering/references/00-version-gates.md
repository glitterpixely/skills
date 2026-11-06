> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 0. Version gates and corrections to the brief

These six items change code that a skill would otherwise write wrong.

| # | Brief assumption | Actual state (r187 source) | Rule for the skill |
|---|---|---|---|
| 1 | `PCFSoftShadowMap` vs `VSMShadowMap` | `PCFSoftShadowMap` was **deprecated in r182 and removed in r186**. `WebGLShadowMap` and `WebGPURenderer` now warn `"PCFSoftShadowMap has been removed. Using PCFShadowMap instead."` `PCFShadowMap` is now soft by default: 5 Vogel-disk taps × hardware 2×2 comparison, rotated by interleaved gradient noise. You set the softness with `shadow.radius`. | Use `PCFShadowMap` + `shadow.radius`. Use `VSMShadowMap` only for very soft, wide penumbrae. |
| 2 | `LinearSRGBColorSpace` for normal/roughness/metalness | The material docs say non-colour maps "must have `texture.colorSpace = NoColorSpace` (default)". Use `LinearSRGBColorSpace` for linear **colour** data: HDR environments, EXR/HDR lightmaps. | Data maps → `NoColorSpace` (leave the default). |
| 3 | `RectAreaLightUniformsLib` | WebGL only. `WebGPURenderer` needs `THREE.RectAreaLightNode.setLTC( RectAreaLightTexturesLib.init() )`. | Branch on the renderer. |
| 4 | Native WebGPU post = `PostProcessing` | Renamed **`RenderPipeline` in r183**. `PostProcessing` is now a deprecated subclass that only warns. | `new THREE.RenderPipeline( renderer )`. |
| 5 | `RGBELoader` | Renamed **`HDRLoader` in r180**. `RGBELoader` still exists as a deprecated shim. | `import { HDRLoader } from 'three/addons/loaders/HDRLoader.js'`. |
| 6 | pmndrs `postprocessing` covers r165–r186+ | `postprocessing@6.39.5` declares the peer range `three >=0.168.0 <0.187.0`. On r187, npm refuses to install without `--legacy-peer-deps`. The modules do load on r187 (my import test), but nothing has rendered on r187. | Pin `three@0.186.x` with pmndrs, or render-test before you ship on r187. |

**Other gates confirmed by probing per-version files:**

| Feature | First present |
|---|---|
| `useLegacyLights` removed (physical lights are the only mode) | r165 |
| `RenderPipeline` | r183 (as the new public name) |
| `SSGINode` (`ssgi()`) | r181 |
| `SSSNode` (screen-space shadows) | ≤ r181 |
| `LightProbeGrid` (irradiance volume) | r184 |
| `SunLight` (built-in 2-cascade CSM), `VXGIVolume`, `retroreflectivity` | r186 |
| `LightMapper` (in-browser lightmap baking), `diffuseRoughness` | r187 |
| `renderAsync()` / `KTX2Loader.detectSupportAsync()` deprecated | r181 (use `await renderer.init()` then the sync calls) |
| GTAO `distanceExponent` / `distanceFallOff` deprecated | r186 |
| `THREE.Clock` deprecated in favour of `THREE.Timer` (`timer.connect(document)`) | r183 |
| `DRACOLoader.setDecoderConfig()` deprecated (WASM used automatically) | r185 |
| `USDZLoader` deprecated in favour of `USDLoader` (reads `.usd`, `.usda`, `.usdc`, `.usdz`) | r179 |
| `CapsuleGeometry` 2nd arg renamed `length` → `height` (and 5th arg `heightSegments` added) | r176 |
| `TransformControls` no longer an `Object3D` — add `scene.add( controls.getHelper() )` | r169 |
| `PointerLockControls.getObject()` → `.object`; `DragControls.getObjects()` → `.objects`, `activate()` → `connect(el)` | r168 |
| `BatchedMesh` requires `addInstance( addGeometry( geo ) )` to draw | r166 |
| `TextGeometry` extrusion option renamed `height` → `depth` | r163 |
| TSL renames: `uniforms()` → `uniformArray()`, `viewportTopLeft` → `viewportUV` (r168); `screen()` → `blendScreen` (r171); `texture().uv()` → `.sample()` (r172); `.label()` → `.setName()` (r179); `PI2` → `TWO_PI` (r181); `directionToColor()` → `packNormalToRGB()` (r185) | r168–r185 |

**Official r186 → r187 migration items** (three.js Migration Guide and r187 release notes, read 2026-10-31):

| Change | PR | What to do |
|---|---|---|
| r177 deprecations removed: `ColorManagement.fromWorkingColorSpace()` / `.toWorkingColorSpace()`, TSL `transformedNormalView`, `transformedNormalWorld`, `transformedClearcoatNormalView` | #34517 | Use `workingToColorSpace()` / `colorSpaceToWorking()`, and `normalView` / `normalWorld` / `clearcoatNormalView` |
| PMREM is now a cube render target; `CubeUVReflectionMapping` removed; PMREM quality changed, so materials look slightly different | #34585 | Remove cubeUV assumptions from custom shaders and readbacks; re-baseline reference images |
| TSL math operands are implicitly coerced to broader common types | #33695 | Re-check int/float mixing in `Fn()` bodies |
| Struct storage buffers are always arrays | #34807 | `storage( buf, Struct ).element( 0 ).get( 'member' )` |
| `WebGLRenderer.setViewport()` / `setScissor()` no longer scale by pixel ratio while a render target is bound | #34460 | Remove manual pixel-ratio compensation in custom passes |
| `pixelationPass()` `pixelSize` is a plain `Number` | #34543 | No node objects |
| Custom lights register with `CustomLight.registerNode( CustomLightNode )` | #34622 | Replace `renderer.library.addLight()` |
| `iridescenceThicknessRange` deprecated | #35039 | `iridescenceThicknessMinimum` / `iridescenceThicknessMaximum` |
| Renderers use `WeakRef` / `FinalizationRegistry` internally | #34368 | Still call `dispose()` explicitly; lifecycle soaks measured after explicit disposal returned to baseline (r187 test) |
| Reversed-depth fixes (#35264, #34606, #34892, #34801) | — | Delete manual reversed-depth workarounds |
| EON rough diffuse BRDF (`diffuseRoughness`) | #34379 | `MeshPhysicalMaterial` only |
| `@types/three` 0.187.0 is published (npm, 2026-10-31) | — | Pin it with three |

`scripts/quality/probe.mjs` greps a project for all of these.
