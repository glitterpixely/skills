---
name: threejs-rendering
description: "Build, debug, and polish 60 FPS Three.js and React Three Fiber scenes on WebGPU and WebGL2 (r165–r187+): photoreal PBR, colour/AgX/Neutral, HDRI/GI, fitted shadows, TSL shaders & compute, RenderPipeline/pmndrs post, OIT/TAAU/FSR1, stylized/toon/anime, glTF/KTX2/3DGS splats, instancing/BatchedMesh/BundleGroup/BVH, WebXR, and G0–G4 quality gates. Trigger terms: three.js, threejs, WebGPU, TSL, R3F, drei, PBR, shadows, postprocessing, 3DGS."
---

# three.js rendering: photoreal-first, every look

This skill is a rulebook plus verified code for three.js render quality and 60 FPS architecture. Photorealism is
the default target. Stylized looks are deliberate departures, made one layer at a time (shading, edges, colour,
post) on the same physically based pipeline. For hybrid headless-Blender world generation + Three.js games, see
`gemini-4-argon-3d-worlds`.

The references were checked against **three r187** (`0.187.0`): source reads, official examples, Node self-tests,
and live GPU renders in headless Chrome on both the Metal WebGPU and WebGL2 (`forceWebGL` + `WebGLRenderer`)
backends. three.js changes APIs every month, so **step 1 is always to check the project's installed version**.

## Reference map (`§n` in the references = file `0n-…`)

| Need | Read |
|---|---|
| Which APIs exist in this version; renamed/removed classes & r187 runtime traps | [00-version-gates.md](references/00-version-gates.md) |
| Renderer setup, colour spaces, AgX/ACES/Neutral, exposure, light units, `reversedDepthBuffer`, device loss | [01-color-tonemapping-units.md](references/01-color-tonemapping-units.md) |
| HDRI + PMREM, `SkyMesh`, sun extraction, `ClusteredLighting`, GI (probes, lightmaps, SSGI, VXGI) | [02-ibl-lighting-gi.md](references/02-ibl-lighting-gi.md) |
| Shadow filters, zero-import frustum fitting, bias math, CSM/`SunLight`/`TileShadowNode`, contact shadows | [03-shadows.md](references/03-shadows.md) |
| Physical materials, IOR, 5-way transparency matrix, EON diffuse, normal-variance AA, `NodeMaterialInstance` | [04-materials.md](references/04-materials.md) |
| Post pipelines (`RenderPipeline` & `pmndrs` + `n8ao`), `oitPass`, `taau`/`fsr1`, SSR, DOF math, bloom | [05-post-processing.md](references/05-post-processing.md) |
| Bevels, `gltf-transform` CLI & programmatic JS, KTX2 UASTC/ETC1S, 3D Gaussian Splatting (`GaussianSplat`), disposal | [06-geometry-assets.md](references/06-geometry-assets.md) |
| "Why does it look fake / broken?" symptom → fix table | [07-diagnostics-photoreal.md](references/07-diagnostics-photoreal.md) |
| Toon, anime, outlines, painterly Kuwahara/halftone, low-poly, pixel art, retro, stylized-real | [08-stylized-looks.md](references/08-stylized-looks.md) |
| All enforceable rules in one numbered list | [09-rulebook.md](references/09-rulebook.md) |
| Evidence log for r187: scripts run, GPU renders, refutations, open boundaries | [10-evidence-r187.md](references/10-evidence-r187.md) |
| Iterating a project to a fixed ceiling: probe, ceiling, gates G0–G4, `Inspector`, stop rules | [11-quality-loop.md](references/11-quality-loop.md) |
| Animation (`Timer`, `AnimationMixer`, `SkeletonUtils.clone`, TSL vertex motion), `three-mesh-bvh`, controls & WebXR | [12-animation-interaction.md](references/12-animation-interaction.md) |
| Profiling (`renderer.info`, `Inspector`), `InstancedMesh`, `BatchedMesh`, `SceneOptimizer`, `BundleGroup` & WebGPU compute | [13-performance-batching-compute.md](references/13-performance-batching-compute.md) |
| Custom shaders, GLSL ↔ TSL table, `Fn` layouts/control flow, `Transpiler`, `*NodeMaterial` & `onBeforeCompile` | [14-shaders-tsl.md](references/14-shaders-tsl.md) |
| React Three Fiber 9.8, `drei` 10.7 WebGPU matrix, TSL `RenderPipeline` in R3F, `<Bvh>`, Rapier v2, XR v6 & `gltfjsx` | [15-react-three-fiber.md](references/15-react-three-fiber.md) |

Load only the files the task needs. A material question needs `04`, not the whole set.

## Workflow

### 1. Pin the version and renderer

Run the API checker against the project:

```bash
node <skill>/scripts/check-three-api.mjs --root <project>
node <skill>/scripts/check-three-api.mjs --root <project> three/addons/tsl/display/SSGINode.js:ssgi three/addons/lights/SunLight.js:SunLight
```

It prints the revision, active version gates (`PCFSoftShadowMap` removed in r186, `PostProcessing` →
`RenderPipeline` in r183, `RGBELoader` → `HDRLoader` in r180, and so on) and any missing symbols. If pmndrs
`postprocessing` is installed, it evaluates its `peerDependencies.three` range dynamically (`6.39.6` declares
`>= 0.168.0 < 0.188.0`, compatible with r187; `6.39.5` stopped at `< 0.187.0`). Write code for the version the
project has. For releases newer than r187, re-check gates in that release's source.

Identify the renderer: `WebGLRenderer` (classic materials, `onBeforeCompile`, pmndrs post) or
`WebGPURenderer` from `three/webgpu` (node materials, TSL, `RenderPipeline`, `BundleGroup`, compute, 3DGS;
also runs on WebGL2 via automatic fallback or `forceWebGL`). For new photoreal work on r183+, prefer
`WebGPURenderer`.

### 2. Classify the look

- **Photoreal** (default): follow `01`→`06` in order.
- **Stylized-real** (animated-feature, clay, product hero): keep the physical light transport; stylize
  shape, colour and lighting design (`08` §8.6).
- **Stylized** (toon, anime, ink, painterly, pixel, retro): choose the departure per layer (`08` §8.1).
  Everything else stays physical.

When the user's request does not settle the look and the choice changes the code (tone mapper, lighting
model), ask once. Otherwise default to photoreal.

### 3. Build in this order

Each step depends on the one before it. Fixing a later step first wastes effort.

1. **Units, depth and colour (`01`):** 1 unit = 1 m. Albedo-class textures `SRGBColorSpace`; data maps left at
   `NoColorSpace`; HDR `LinearSRGBColorSpace`; exactly one output transform. Pick AgX for photoreal HDR,
   Neutral for brand/product colour, `NoToneMapping` (values ≤ 1) for flat stylized palettes. Use
   `reversedDepthBuffer: true` for large worlds on `WebGPURenderer` + `RenderPipeline` (never with pmndrs
   `EffectComposer`).
2. **Lighting (`02`):** `scene.environment` from a PMREM'd HDRI or `SkyMesh` (`showSunDisc.value = 0` during
   PMREM bake); one shadow-casting key light in physical units (`.power` in lumens, `decay = 2`); no
   ambient/hemisphere fill; GI from lightmaps, `LightProbeGrid` or SSGI; `ClusteredLighting` for many lights.
3. **Shadows (`03`):** `PCFShadowMap` + `shadow.radius`. Fit the frustum with
   [fit-shadow.mjs](scripts/fit-shadow.mjs) **before** touching bias. Take the starting `normalBias` and
   `bias` from `suggestShadowBias()`.
4. **Materials (`04`):** change lighting *inputs* (albedo, roughness, metalness, normal, AO), never outputs.
   Pick transparency deliberately (`alphaTest`, `alphaHash`, `backdropNode`, `oitPass`, or `transmission` +
   `ior` + `thickness` + `dispersion`). Derive numbers from [physical.mjs](scripts/physical.mjs).
5. **Post (`05`):** AO into indirect light only (`builtinAOContext`) → SSR → TRAA / `taau()` → DOF → bloom
   (linear HDR) → `renderOutput()` → CA, vignette, grain, LUT (display space). Wrap `oitPass` in
   `vec4( scenePass )` before feeding post nodes. On pmndrs, keep `SMAAEffect` in a separate final `EffectPass`
   from `ChromaticAberrationEffect` and set `n8ao.configuration.halfRes = false` on r187.
6. **Assets & scale (`06`, `12`, `13`):** UASTC for normals/ORM, ETC1S for colour, Meshopt geometry, `GaussianSplat`
   for first-party 3DGS, `InstancedMesh` / `BatchedMesh` / `SceneOptimizer.toBatchedMesh()` / `BundleGroup`
   for draw calls, `three-mesh-bvh` for raycasting, and explicit GPU disposal.

### 4. Verify on a GPU (required before calling a look done)

Neither a clean build nor a silent console shows that a look works. Render it:

1. Copy [render-check/harness.html](scripts/render-check/harness.html) into the project and put the scene
   and pipeline in `buildScene()`. Serve the project root (`python3 -m http.server 8765`) and install
   `playwright-core` as a dev dependency.
2. Shoot both backends:
   `node <skill>/scripts/render-check/shoot.mjs "http://localhost:8765/<path>/harness.html" webgpu.png --strict`,
   then again with `?webgl`. Any `THREE.TSL:` error, `[error]`, `[pageerror]`, or `[timeout]` is a failure.
3. **Look at the screenshots.** Check them against the diagnostics tables (`07`, `08` §8.7).
4. **Ablate** each post stage with query flags and diff the images. Every effect should change only the
   pixels it is meant to change (GTAO: contact creases; SSR: reflective surfaces). With every stage off,
   the output must match a plain `renderer.render()`.
5. Report what was rendered, on which backend, and what was not. Headless frame times are capped by the
   display (about 16.7 ms), so measure GPU cost on target hardware with `Inspector` or GPU timer queries.

### 5. Polishing an existing project: run the quality loop

When the user asks to polish, iterate or "make it as good as possible", run the loop in
[11-quality-loop.md](references/11-quality-loop.md). Do not keep adding detail.

1. Run the PROBE once: [probe.mjs](scripts/quality/probe.mjs).
2. Fix the CEILING as numbers before pass one: [ceiling.example.json](scripts/quality/ceiling.example.json).
3. Measure gates G0–G3 with [gate-harness.html](scripts/quality/gate-harness.html) +
   [gates.js](scripts/quality/gates.js) + [run-gates.mjs](scripts/quality/run-gates.mjs). G4 goes to a blind
   critic subagent that sees only `packet/`.
4. One mechanism per pass on the lowest failing gate. Keep or `git revert`.
5. Stop on converged, stalled or capped. Report the trajectory, and list expansions as proposals without
   implementing them.

## Hard rules

1. Check the installed three version before writing API calls. Gate on `THREE.REVISION`.
2. One output transform: `OutputPass` (three composer), one `renderOutput()` (TSL), or
   `ToneMappingEffect` with `renderer.toneMapping = NoToneMapping` (pmndrs).
3. Lights in physical units with `decay = 2`. Pre-expose rather than push absolute sun luminance into
   half-float buffers (overflow at 65,504).
4. Fit the shadow frustum first. Then `normalBias ≈ 1 texel`, then a small `bias`. `bias × (far − near)`
   is the world-space offset.
5. AO darkens indirect light only. Temporal resolve (`traa` / `taau`) comes before DOF and bloom. Bloom runs on
   linear HDR. Grain, CA, vignette and LUT run after tone mapping.
6. In custom post nodes, convert depth with the **scene** camera's near/far
   (`reference( 'near', 'float', camera )` or `scenePass.getViewZNode()`). Global `cameraNear` and
   `cameraFar` resolve to the post quad. When chaining `oitPass` into post nodes, wrap `vec4( scenePass )`
   so `convertToTexture` does not bypass `OITPassNode.setup()`.
7. r187 post pitfalls: pass `center` explicitly to `chromaticAberration( node, strength, uniform( new Vector2( 0.5, 0.5 ) ) )`;
   import `fsr1` from `'three/addons/tsl/display/FSR1Node.js'`; on pmndrs, never merge `ChromaticAberrationEffect`
   with `SMAAEffect` in one `EffectPass`, keep `n8ao.configuration.halfRes = false`, and never enable
   `reversedDepthBuffer: true` on `WebGLRenderer` + `EffectComposer`.
8. Stylized: toon ramps use `NearestFilter`, no mipmaps. `toonOutlinePass` outlines only toon materials.
   Line widths scale with DPR. Pixel art uses an orthographic camera, frustum snapping and no AA.
9. Never report a look as done without the GPU render check in step 4.
10. Deterministic stepping: r187 `THREE.Timer.update( t )` subtracts a wall-clock `_startTime` from the
    constructor. Zero it (`timer._startTime = 0`) or drive animation from a fixed-step counter.
11. In a quality loop, the ceiling is fixed before pass one and expansions are proposals, never passes.
12. Displace vertices on `positionLocal` (never `positionGeometry`) and sync shadows with
    `castShadowPositionNode`. On shadow-casting `NodeMaterialInstance` meshes, read `colorNode` props via
    `reference( 'userData.x', type )` on `mesh.userData` (never `materialReference`, which crashes on the
    `ShadowMaterial` override pass). Clone rigged models with `SkeletonUtils.clone()`, add `TransformControls`
    via `scene.add( tc.getHelper() )`, and pass `shadows="percentage"` in React Three Fiber (`12`–`15`).
