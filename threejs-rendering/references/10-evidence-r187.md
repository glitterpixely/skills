> Part of the `threejs-rendering` skill. Verified against three r187 (2026-10-31); re-check version gates in `00-version-gates.md` for newer releases. `§n` refers to reference file `0n-…`.

# Evidence and coverage

- **Run in this session:**
  - npm registry queries for current versions.
  - Installed `three@0.187.0`, `postprocessing@6.39.5`, `n8ao@2.0.1` and `@gltf-transform/cli@4.5.1` in `scratch/three`.
  - Grep reads of the r187 source.
  - Downloaded 21 r187 examples from the `r187` git tag.
  - Per-version unpkg probes for r164–r187 feature gates.
  - `check-imports.mjs` + `check-extra.mjs`: 138 imported symbols checked against r187. One name was wrong in my draft (`ProgressiveLightMapGPU.js` exports `ProgressiveLightMap`) and is corrected; the rest resolve. Also checked: the pmndrs constructor options used in §5.4 construct, and `PerspectiveCamera.getFocalLength()` / `getFilmHeight()` return 50 mm / 19.69 mm for 16:9.
  - `fitShadow.test.mjs`: pass, with a mutation run that failed as expected.
  - `check-materials.mjs`: TSL construction and the `onBeforeCompile` anchors.
  - Arithmetic for F0, CoC, hyperfocal, lumen→candela and EV exposure values.
- **Rendered (headless Chrome, this Mac, three r187):**
  - The §5.3 WebGPU pipeline on both backends, with stage ablation (§5.3).
  - The §8 toon ramp, anime material, screen-space ink edges, `toonOutlinePass` and `pixelationPass` + `bayerDither`. The first edge draft inked the whole frame because it used global `cameraNear`/`cameraFar`. The fixed version shown in §8.3 outlines silhouettes and creases, including the non-toon sphere. `toonOutlinePass` skipped that sphere, as §8.3 states.
  - Scripts: `scratch/render/` (pages) and `scratch/three/shoot.mjs` (Playwright screenshotter).
- **Not rendered:** §5.4 (pmndrs on WebGLRenderer), the `onBeforeCompile` patch, the transmission/IOR table values, the §8.4 painterly algorithms (described, not coded), and the sun-direction inversion. The harness logged 16.67 ms per frame, the 60 Hz display cap, which hides GPU cost. KTX2 encoding was not run because KTX-Software is not installed.
- **What would change the conclusions:** a three r188+ release, which could move the APIs gated in §0; a `postprocessing` release that widens its peer range to r187; a GPU profile on the target hardware, which replaces every timing estimate here.

## Reusable checks shipped with the skill

- `scripts/check-three-api.mjs`: revision, version gates and symbol presence against a project's installed three. Tested on r187 with a deliberately missing symbol, which it reported.
- `scripts/fit-shadow.mjs` + `fit-shadow.test.mjs`: 2,000-box containment test. Run it from a folder where `three` resolves.
- `scripts/physical.mjs`: run it directly for its self-test (exposure, lumens, F0, dispersion, CoC, hyperfocal, blur ramp).
- `scripts/render-check/`: `harness.html` + `shoot.mjs`. Tested here on both backends, which reported 4 draw calls and 7,939 triangles for the template scene.

## Quality-loop tooling tests (2026-10-31, fixture project, three r187, headless Chrome on this Mac)

- `probe.mjs` on a fixture with 10 planted patterns reported 8 migration categories, the `THREE.Clock` loop style and the unpinned `^0.187.0` range, and exited 1. It missed one plant: TSL `int` was imported but never called, and the coercion check matches calls only.
- `run-gates.mjs` on the clean template: G0–G3 pass on WebGPU and WebGL2. Two page loads matched exactly (maxChannelDelta 0) on hardware and on SwiftShader (`--software`). NaN/Inf count 0. Soak net delta 0. GPU timers returned ~0.5–1.0 ms on hardware and ~38 ms on SwiftShader (reported as pending).
- Failure detection, each seen failing: G0 (`PCFSoftShadowMap` removal warning), G1 (wall-clock term in the animation; and, before the fix, unzeroed `THREE.Timer._startTime`), G2 soak (an undisposed `RoomEnvironment`, then an undisposed `DataTexture`), G3 (normal map tagged sRGB).
- G0 initially missed the `PCFSoftShadowMap` warning because it only matched "deprecat". It now fails on any console warning or error.

## Folded modules (`§12`–`§15`, 2026-11-05)

- Adapted and upgraded to three r187 from [`CloudAI-X/threejs-skills`](https://github.com/CloudAI-X/threejs-skills) (MIT License; originally targeting `three@0.186.1`, `@react-three/fiber@9.8.2`, `@react-three/drei@10.7.9`, `@gltf-transform/cli@4.5.1`, and `gltfjsx@6.5.3`):
  - `12-animation-interaction.md`: `THREE.Timer`, `AnimationMixer`, crossfades, additive clips, `SkeletonUtils.clone`, TSL vertex displacement (`positionLocal` + `castShadowPositionNode`), raycasting (`layers.enable(1)`), and `Controls` (`TransformControls.getHelper()`).
  - `13-performance-batching-compute.md`: WebGL2 vs WebGPU `renderer.info` counters, `InstancedMesh`, `BatchedMesh` (`addGeometry` + `addInstance`), `compileAsync`, WebGPU `renderer.compute()` (`instancedArray` and r187 array-indexed struct `storage().element(i).get(...)`), and `Sprite` + `PointsNodeMaterial`.
  - `14-shaders-tsl.md`: GLSL ↔ TSL r187 translation table (`normalView`/`normalWorld`, `uniformArray`, `viewportUV`, `.sample()`, `.setName()`, `TWO_PI`), node material extensions, and `onBeforeCompile` / `ShaderMaterial` rules.
  - `15-react-three-fiber.md`: R3F 9.8 + React 19 + `drei` 10.7 setup (`shadows="percentage"`, `AgXToneMapping`/`NeutralToneMapping`, async `WebGPURenderer` `<Canvas gl={...}>` factory, `extend(THREE)`, WebGPU `drei` compatibility table, and `gltfjsx`).
- `probe.mjs` tested against a synthetic bad fixture (7 new migration/hygiene patterns caught, exit 1) and a clean r187/R3F fixture (0 hits, exit 0).
