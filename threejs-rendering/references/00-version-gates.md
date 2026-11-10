> Part of the `threejs-rendering` skill. Verified against three r187 (`0.187.0`); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# 0. Version gates and runtime pitfalls

These items change code that a skill or outdated tutorial would otherwise write wrong.

| # | Common assumption | Actual state (r187 source & GPU tests) | Rule for the skill |
|---|---|---|---|
| 1 | `PCFSoftShadowMap` vs `VSMShadowMap` | `PCFSoftShadowMap` was **deprecated in r182 and removed at runtime in r186** (`constants.js` JSDoc says `@deprecated since r186`, while `WebGLShadowMap` and `Renderer.js:1031` log `"PCFSoftShadowMap has been removed. Using PCFShadowMap instead."` and rewrite `shadowMap.type = PCFShadowMap`). `PCFShadowMap` is soft by default: 5 Vogel-disk taps × hardware 2×2 comparison, rotated by IGN, scaled by `shadow.radius`. | Use `PCFShadowMap` + `shadow.radius`. Use `VSMShadowMap` only for very soft, wide penumbrae. |
| 2 | `LinearSRGBColorSpace` for normal/roughness/metalness | Non-colour data maps (`normalMap`, `roughnessMap`, `metalnessMap`, `aoMap`, `bumpMap`, `alphaMap`, `sheenRoughnessMap`, `clearcoat*`, etc.) must stay `NoColorSpace` (default). Use `LinearSRGBColorSpace` for linear **colour** data: HDR environments, EXR/HDR lightmaps. | Data maps → `NoColorSpace` (leave the default). |
| 3 | `RectAreaLightUniformsLib` | WebGL only. `WebGPURenderer` needs `THREE.RectAreaLightNode.setLTC( RectAreaLightTexturesLib.init() )`. | Branch on the renderer. |
| 4 | Native WebGPU post = `PostProcessing` | Renamed **`RenderPipeline` in r183**. `PostProcessing` is now a deprecated subclass that warns. | `new THREE.RenderPipeline( renderer )`. |
| 5 | `RGBELoader` | Renamed **`HDRLoader` in r180**. `RGBELoader` still exists as a deprecated shim. | `import { HDRLoader } from 'three/addons/loaders/HDRLoader.js'`. |
| 6 | pmndrs `postprocessing` peer range on r187 | **`postprocessing@6.39.6`** declares `peerDependencies.three: ">= 0.168.0 < 0.188.0"`, installing cleanly and rendering on `three@0.187.0` (`6.39.5` stopped at `< 0.187.0`). However, see the three GPU-verified `pmndrs` + `n8ao` traps below. | Use `postprocessing@^6.39.6` on r187; run `check-three-api.mjs` to check peer upper bounds dynamically on newer three releases. |

**GPU-verified r187 runtime pitfalls (caught in headless Chrome on Metal WebGPU & WebGL2):**

| Trap | Exact symptom / error | Fix |
|---|---|---|
| `oitPass` fed directly into `taau`, `traa`, `bloom`, `dof`, or `fxaa` | OIT transparent meshes completely disappear with zero console errors (`RTTNode.js:368` `convertToTexture` checks `if ( node.isPassNode ) return node.getTextureNode()`, bypassing `OITPassNode.setup()`). | Wrap `oitPass` in `vec4( scenePass )` before passing to any post node so `OITPassNode.setup()` composites `accum` + `revealage` (`§5.5`). |
| `FSR1Node` JSDoc import path | `ERR_MODULE_NOT_FOUND` / 404 on `'three/addons/tsl/display/fsr1/FSR1Node.js'` (typo in Three r187's own JSDoc). | Import from **`'three/addons/tsl/display/FSR1Node.js'`**. |
| `chromaticAberration()` default `center` | `TypeError` when omitting the 3rd argument despite JSDoc saying `center = null` defaults to `(0.5, 0.5)`. | Always pass `uniform( new THREE.Vector2( 0.5, 0.5 ) )` as the 3rd argument. |
| `NodeMaterialInstance` + `materialReference` in `colorNode` + `castShadow = true` | `TypeError: Cannot read properties of undefined (reading 'r')` in `NodeUniformsGroup.updateColor` during shadow passes (`Renderer._getShadowNodes` copies `colorNode` onto `ShadowMaterial` where custom material props are `undefined`). | Read per-object `colorNode` / `opacityNode` / `positionNode` values via `reference( 'userData.tint', 'color' )` on `mesh.userData`; reserve `materialReference(...)` for shading-only slots (`roughnessNode`, `metalnessNode`, `clearcoatNode`) (`§4.7`). |
| `SkyMesh` + `reversedDepthBuffer: true` | Any opaque mesh closer to the camera than `sky.position` is overwritten with flat sky colour on both WebGPU and WebGL2 (`SkyMesh.js:222` sets `position.z = position.w`, which is `camera.near = 1.0` instead of `0.0` under reversed depth). | Set `sky.renderOrder = -1e6; sky.material.depthTest = false;` whenever `reversedDepthBuffer: true` is enabled (`§2.1`). |
| `pmndrs` `EffectPass` merging `ChromaticAberrationEffect` + `SMAAEffect` | Throws `Error: Convolution effects cannot be merged (ChromaticAberrationEffect)` (`postprocessing` forbids two `EffectAttribute.CONVOLUTION` effects in one `EffectPass`). | Place `SMAAEffect` in its own final `EffectPass` after the `ChromaticAberrationEffect` + `VignetteEffect` + `NoiseEffect` pass (`§5.4`). |
| `n8ao@2.0.1` `configuration.halfRes = true` on `three@0.187.0` | Throws `TypeError: Cannot read properties of undefined (reading 'length')` in `WebGLTextures.setupRenderTarget` (`N8AO.js:1503` overrides `get texture()` to return `this.textures` array); also `n8ao` imports `"three/examples/jsm/postprocessing/Pass.js"`. | Keep `n8ao.configuration.halfRes = false` on r187, and include `"three/examples/jsm/"` alongside `"three/addons/"` in browser importmaps (`§5.4`). |
| `WebGLRenderer({ reversedDepthBuffer: true })` + `pmndrs` `EffectComposer` | Renders a **100% pitch-black canvas (`#000000`) with zero console errors**. | Keep `reversedDepthBuffer: false` with `pmndrs` `EffectComposer`; use `WebGPURenderer({ reversedDepthBuffer: true })` + TSL `RenderPipeline` instead (`§1.6`). |
| `SceneOptimizer.toInstancingMesh()` | Throws `Error: SceneOptimizer.toInstancingMesh() is not implemented yet` in r187. | Call `new SceneOptimizer( group ).toBatchedMesh()` (`§13.2`). |

**Feature availability gates across Three.js r163–r187:**

| Feature | First present |
|---|---|
| `TextGeometry` extrusion option renamed `height` → `depth` | r163 |
| `useLegacyLights` removed (physical lights are the only mode) | r165 |
| `BatchedMesh` requires `addInstance( addGeometry( geo ) )` to draw | r166 |
| `PointerLockControls.getObject()` → `.object`; `DragControls.getObjects()` → `.objects`, `activate()` → `connect(el)` | r168 |
| `TransformControls` no longer an `Object3D` — add `scene.add( controls.getHelper() )` | r169 |
| `CapsuleGeometry` 2nd arg renamed `length` → `height` (and 5th arg `heightSegments` added) | r176 |
| `USDZLoader` deprecated in favour of `USDLoader` (reads `.usd`, `.usda`, `.usdc`, `.usdz`) | r179 |
| `HDRLoader` replaces `RGBELoader` | r180 |
| `SSGINode` (`ssgi()`), `SSSNode`, sync `render()` after `await renderer.init()` (`renderAsync()` deprecated) | r181 |
| `RenderPipeline` replaces `PostProcessing`; `THREE.Timer` replaces deprecated `THREE.Clock` | r183 |
| `LightProbeGrid` (irradiance volume) | r184 |
| `DRACOLoader.setDecoderConfig()` deprecated (WASM used automatically) | r185 |
| `PCFSoftShadowMap` removed; `SunLight` (2-cascade CSM), `VXGIVolume`, `retroreflectivity`; GTAO `distanceExponent` deprecated | r186 |
| `LightMapper`, `diffuseRoughness` (EON), `BundleGroup` (`three/webgpu`), `NodeMaterialInstance` (`three/webgpu`), `TAAUNode`, `FSR1Node`, `OITPassNode`, `GaussianSplat` + `SPZLoader` + `GLTFGaussianSplatLoaderExtension`, `ClusteredLighting`, `DynamicLighting`, `SceneOptimizer.toBatchedMesh()`, `VideoFrameTexture`, `HTMLTexture` | r187 |
| TSL renames: `uniforms()` → `uniformArray()`, `viewportTopLeft` → `viewportUV` (r168); `screen()` → `blendScreen` (r171); `texture().uv()` → `.sample()` (r172); `.label()` → `.setName()` (r179); `PI2` → `TWO_PI` (r181); `directionToColor()` → `packNormalToRGB()` (r185) | r168–r185 |

**Official r186 → r187 migration items** (three.js Migration Guide and r187 release notes):

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
| Renderers use `WeakRef` / `FinalizationRegistry` internally | #34368 | Still call `dispose()` explicitly; lifecycle soaks return to baseline only with explicit disposal |
| Reversed-depth fixes (#35264, #34606, #34892, #34801) | — | Delete manual reversed-depth shader hacks; pass `reversedDepthBuffer: true` to the renderer (`§1.6`) |
| EON rough diffuse BRDF (`diffuseRoughness`) | #34379 | `MeshPhysicalMaterial` / `MeshPhysicalNodeMaterial` only |
| `@types/three` `0.187.0` published | — | Pin exact `0.187.0` alongside `three` |

`scripts/quality/probe.mjs` greps a project for all of these.
