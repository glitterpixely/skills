---
name: threejs-rendering
description: >-
  Make three.js and React Three Fiber scenes look right at 60 FPS: photoreal first (colour, tone mapping,
  light units, HDRI, GI, shadows, physical materials, TSL, post, KTX2 assets), stylized looks (toon, anime,
  outlines, pixel, stylized-real), animation, camera controls, raycasting, instancing/BatchedMesh, WebGPU
  compute, GLSL-to-TSL shaders, R3F 9.8 + drei 10.7, and a gated quality loop. WebGL2 and WebGPU, r165–r187+.
  Not for whole games (gemini-4-argon-3d-worlds). Trigger terms: three.js, WebGPU, TSL, photoreal, PBR, HDRI,
  shadows, post-processing, toon shader, outlines, looks fake, quality loop, r187 migration, React Three Fiber,
  R3F, drei, gltfjsx, AnimationMixer, SkeletonUtils, OrbitControls, TransformControls, raycasting, InstancedMesh,
  BatchedMesh, compute shader, ShaderMaterial, onBeforeCompile, GLSL to TSL.
---

# three.js rendering: photoreal-first, every look

This skill is a rulebook plus verified code for three.js render quality. Photorealism is the default
target. Stylized looks are deliberate departures, made one layer at a time (shading, edges, colour, post)
on the same physically based pipeline.

The references were checked against **three r187** (2026-10-31): source grep, the official examples,
and GPU renders in headless Chrome on both the WebGPU and WebGL2 backends. three.js changes APIs every
month, so **step 1 is always to check the project's installed version**.

## Reference map (`§n` in the references = file `0n-…`)

| Need | Read |
|---|---|
| Which APIs exist in this version; renamed/removed classes | [00-version-gates.md](references/00-version-gates.md) |
| Renderer setup, colour spaces, AgX/ACES/Neutral, exposure, light units | [01-color-tonemapping-units.md](references/01-color-tonemapping-units.md) |
| HDRI + PMREM, sun extraction, direct lights, GI (probes, lightmaps, SSGI) | [02-ibl-lighting-gi.md](references/02-ibl-lighting-gi.md) |
| Shadow filters, frustum fitting, bias math, CSM, contact shadows | [03-shadows.md](references/03-shadows.md) |
| Physical materials, IOR table, metals, SSS, ORM, TSL/onBeforeCompile extension | [04-materials.md](references/04-materials.md) |
| Post pipeline order and code (WebGPU RenderPipeline, pmndrs), DOF math, bloom | [05-post-processing.md](references/05-post-processing.md) |
| Bevels and weighted normals, gltf-transform, KTX2 UASTC/ETC1S, disposal | [06-geometry-assets.md](references/06-geometry-assets.md) |
| "Why does it look fake?" symptom → fix table | [07-diagnostics-photoreal.md](references/07-diagnostics-photoreal.md) |
| Toon, anime, outlines, painterly, low-poly, pixel art, retro, stylized-real | [08-stylized-looks.md](references/08-stylized-looks.md) |
| The enforceable rules in one list | [09-rulebook.md](references/09-rulebook.md) |
| Evidence log for r187: scripts run, renders, open gaps | [10-evidence-r187.md](references/10-evidence-r187.md) |
| Iterating a project to a fixed ceiling: probe, ceiling, gates G0–G4, stop rules | [11-quality-loop.md](references/11-quality-loop.md) |
| Animation (`Timer`, `AnimationMixer`, crossfades, `SkeletonUtils.clone`, TSL vertex motion), controls & raycasting | [12-animation-interaction.md](references/12-animation-interaction.md) |
| Performance profiling (`renderer.info`), `InstancedMesh`, `BatchedMesh`, `compileAsync` & WebGPU compute | [13-performance-batching-compute.md](references/13-performance-batching-compute.md) |
| Custom shaders, GLSL ↔ TSL translation table, `*NodeMaterial` slots & `onBeforeCompile` | [14-shaders-tsl.md](references/14-shaders-tsl.md) |
| React Three Fiber 9.8, `@react-three/drei` 10.7 WebGPU matrix, hooks & `gltfjsx` | [15-react-three-fiber.md](references/15-react-three-fiber.md) |

Load only the files the task needs. A material question needs `04`, not the whole set.

## Workflow

### 1. Pin the version and renderer

Run the API checker against the project:

```bash
node <skill>/scripts/check-three-api.mjs --root <project>
node <skill>/scripts/check-three-api.mjs --root <project> three/addons/tsl/display/SSGINode.js:ssgi three/addons/lights/SunLight.js:SunLight
```

It prints the revision, the version gates that apply (`PCFSoftShadowMap` removed in r186,
`PostProcessing` → `RenderPipeline` in r183, `RGBELoader` → `HDRLoader` in r180, and so on) and any
missing symbols. If pmndrs `postprocessing` is installed, it prints its declared three peer range: 6.39.5
stops at `<0.187.0`. Write code for the version the project has, not the newest one. If the project is on
a release newer than r187, re-check any gate the task depends on in that release's source.

Identify the renderer: `WebGLRenderer` (classic materials, `onBeforeCompile`, pmndrs post) or
`WebGPURenderer` from `three/webgpu` (node materials, TSL, `RenderPipeline`; also runs on WebGL2 with
`forceWebGL`). For new photoreal work on r183+, prefer `WebGPURenderer`.

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

1. **Units and colour:** 1 unit = 1 m. Albedo-class textures `SRGBColorSpace`; data maps left at
   `NoColorSpace`; HDR `LinearSRGBColorSpace`; exactly one output transform. Pick the tone mapper:
   AgX for photoreal HDR, Neutral for brand/product colour, `NoToneMapping` (values ≤ 1) for flat
   stylized palettes.
2. **Lighting:** `scene.environment` from a PMREM'd HDRI; one shadow-casting key light with intensity set
   in physical units (`.power` in lumens, `decay = 2`); no ambient/hemisphere fill; GI from lightmaps,
   `LightProbeGrid` or SSGI.
3. **Shadows:** `PCFShadowMap` + `shadow.radius`. Fit the frustum with
   [fit-shadow.mjs](scripts/fit-shadow.mjs) **before** touching bias. Take the starting `normalBias` and
   `bias` from `suggestShadowBias()`.
4. **Materials:** change lighting *inputs* (albedo, roughness, metalness, normal, AO), never outputs.
   Metals use the linear F0 table; glass uses `transmission` + `ior` + `thickness`. Get IOR and F0, Abbe →
   dispersion, exposure and DOF numbers from [physical.mjs](scripts/physical.mjs) instead of guessing.
5. **Post:** AO into indirect light only (`builtinAOContext`) → SSR → TRAA → DOF → bloom (linear HDR) →
   `renderOutput()` → CA, vignette, grain, LUT (display space). Stylized post (pixelation, posterize,
   dither, ink lines) follows `08`.
6. **Assets:** UASTC for normals and ORM, ETC1S for colour, Meshopt geometry. Override `optimize`'s
   simplify, join and palette defaults on hero assets. Dispose GPU resources.

### 4. Verify on a GPU (required before calling a look done)

Neither a clean build nor a silent console shows that a look works. Render it:

1. Copy [render-check/harness.html](scripts/render-check/harness.html) into the project and put the scene
   and pipeline in `buildScene()`. Serve the project root (`python3 -m http.server 8765`) and install
   `playwright-core` as a dev dependency.
2. Shoot both backends:
   `node <skill>/scripts/render-check/shoot.mjs "http://localhost:8765/<path>/harness.html" webgpu.png`,
   then again with `?webgl`. Read the printed console. Any `THREE.TSL:` error or `[pageerror]` is a
   failure.
3. **Look at the screenshots.** Check them against the diagnostics tables (`07`, `08` §8.7).
4. **Ablate** each post stage with query flags and diff the images. Every effect should change only the
   pixels it is meant to change (GTAO: contact creases; SSR: reflective surfaces). With every stage off,
   the output must match a plain `renderer.render()`.
5. Report what was rendered, on which backend, and what was not. Headless frame times are capped by the
   display (about 16.7 ms), so measure GPU cost on target hardware with the Inspector or timer queries.

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
5. AO darkens indirect light only. Temporal resolve comes before DOF and bloom. Bloom runs on linear HDR.
   Grain, CA, vignette and LUT run after tone mapping.
6. In custom post nodes, convert depth with the **scene** camera's near/far
   (`reference( 'near', 'float', camera )` or `scenePass.getViewZNode()`). Global `cameraNear` and
   `cameraFar` there resolve to the post quad and break every depth-based effect.
7. r187 `chromaticAberration()`: pass `center` explicitly (`uniform( new Vector2( 0.5, 0.5 ) )`). The
   documented `null` default crashes.
8. Stylized: toon ramps use `NearestFilter`, no mipmaps. `toonOutlinePass` outlines only toon materials.
   Line widths scale with DPR. Pixel art uses an orthographic camera, frustum snapping and no AA.
9. Never report a look as done without the GPU render check in step 4.
10. Deterministic stepping: r187 `THREE.Timer.update( t )` subtracts a wall-clock `_startTime` from the
    constructor. Zero it (`timer._startTime = 0`) or drive animation from a fixed-step counter, or two
    identical runs will differ.
11. In a quality loop, the ceiling is fixed before pass one and expansions are proposals, never passes.
12. Displace vertices on `positionLocal` (never `positionGeometry`) and sync shadow casters with
    `castShadowPositionNode`. Clone rigged models with `SkeletonUtils.clone()`, add `TransformControls`
    via `scene.add( tc.getHelper() )`, and use `shadows="percentage"` + `AgXToneMapping`/`NeutralToneMapping`
    in React Three Fiber (`12`–`15`).
