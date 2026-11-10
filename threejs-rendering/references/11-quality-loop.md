> Part of the `threejs-rendering` skill. Written for three r187 (2026-10-31). The tooling lives in `scripts/quality/`.

# 11. Three.js r187 quality loop

You are running a quality loop on a three.js project. **The iteration count is an output, not an input.** Never pick a number up front. There is always more you could add, so the ceiling must be fixed before pass one. Without it, the loop cannot tell good from busy.

## r187 fact check of this loop (read first)

The loop's version-specific premises were checked against the r187 source (`src/core/Timer.js`, `src/math/ColorManagement.js`, `src/renderers/common/PMREMGenerator.js`), the official Migration Guide (`186 → 187`) and the r187 release notes on 2026-10-31. The loop below includes these corrections.

| Premise | Finding | Effect on the loop |
|---|---|---|
| "r187 removed all r177 deprecations" | **Confirmed** (#34517): `ColorManagement.fromWorkingColorSpace()` / `.toWorkingColorSpace()`, TSL `transformedNormalView`, `transformedNormalWorld`, `transformedClearcoatNormalView` | Probe greps for them |
| "Subclassed Pass touching removed public quad (now internal `_fsQuad`)" | **Not an r187 change.** `OutputPass`/`GTAOPass` already used `_fsQuad` in r176–r186. In r187, `SAOPass` and `SSRPass` still expose a public `fsQuad`. | Kept as a hygiene grep, not a migration item |
| PMREM #34585 | **Confirmed**: cube render targets, `CubeUVReflectionMapping` removed, materials "look slightly different" | Re-baseline reference images after migrating; expect G4/perceptual deltas that are not regressions |
| TSL implicit coercion, storage buffer bindings | **Confirmed** (#33695, #34807: struct storage buffers are always arrays) | Probe greps |
| Reversed-depth workarounds fixed upstream | **Confirmed**: several fixes (#35264, #34606, #34892, #34801) | Probe greps for manual workarounds |
| Missing from the original list | `setViewport/setScissor` stop scaling by pixel ratio with a render target bound (#34460); `pixelationPass` `pixelSize` is a Number (#34543); `CustomLight.registerNode()` (#34622); `iridescenceThicknessRange` deprecated (#35039); renderers use `WeakRef`/`FinalizationRegistry` (#34368) | Added to the probe |
| "Allow `@types/three >= 0.186.0` if 0.187.x types lag" | `@types/three` **0.187.0 is published** (npm, 2026-10-31) | Pin `@types/three` 0.187.0 |
| "Step `THREE.Timer` manually" | **Not deterministic as-is.** `Timer.update( t )` subtracts `_startTime = performance.now()` captured in the constructor, so the first synthetic step has a run-dependent delta. Tested: two identical runs rendered the ball at different positions until `_startTime` was zeroed. | `createFixedStepper()` zeroes `_startTime`. Projects that step their own Timer must do the same, or drive animation from a fixed-step counter. |
| "EON rough diffuse" | **Confirmed** (#34379): it is `MeshPhysicalMaterial.diffuseRoughness` | G3 material policy stands |
| "TSL PostProcessing" | Renamed `RenderPipeline` in r183 | Probe flags `new PostProcessing()` |
| GPU timers | Both work in headless Chrome on this Mac: WebGPU `trackTimestamp: true` + `resolveTimestampsAsync()`, and WebGL `EXT_disjoint_timer_query_webgl2` | G2 reads them; a missing timer fails G2 with a note |
| "Exact SHA-256 on a software rasterizer" | Achieved on both backends with SwiftShader (`--software`). Hardware runs of the template scene also matched exactly. | Run G1 in software mode; run G2 timing on hardware only |
| "Shadow map depth buffers non-empty" | The audit checks that every shadow-casting light has an **allocated** shadow map after rendering. It does not read back the depth contents. | Inspect shadows visually in G4 |
| Perceptual diff "FLIP or RMSE" | The runner reports RMSE (8-bit units) and the max channel delta. FLIP is not bundled. | Set `perceptualRmse` in the ceiling; use FLIP externally if installed |

## PROBE (once)

```bash
node <skill>/scripts/quality/probe.mjs --root <project> --json quality/probe.json
```

Record:
- three version: pin the exact `0.187.0` (r187) and `@types/three` `0.187.0`.
- Active pipeline: `WebGLRenderer` + `EffectComposer`, or `three/webgpu` + `RenderPipeline`/TSL.
- WebGL2 fallback: if `three/webgpu` is active, record whether `forceWebGL: true` parity is in scope. That becomes `"webglParity"` in the ceiling.
- Loop style (manual `THREE.Timer` step vs rAF), bundler, R3F or vanilla. The probe detects these.
- Migration surface: the probe greps every item in the table above plus hygiene (`PCFSoftShadowMap`, `RGBELoader`, `*Async` render calls). It also flags caret or tilde ranges on three.

## CEILING (once, before pass one)

Copy `scripts/quality/ceiling.example.json` to `quality/ceiling.json` and write down what "highest quality" means for this brief, as numbers:
- GPU frame time budget (`gpuMs`, timer query) and CPU submission budget (`cpuMs`) on the target device.
- `drawCalls`, `triangles`, `textures` and `geometries` budgets (`renderer.info`).
- Perceptual threshold `perceptualRmse` (8-bit RMSE) below which a change is imperceptible.
- The brief's required elements as a binary `checklist`.
- `criticTarget` score for G4.

If it is not on this list, it is not part of the ceiling.

## GATES (ordered, fail-fast)

Run them with the gate harness: copy `scripts/quality/gate-harness.html` and `gates.js` into `quality/`, put the project scene in `mount()`, and serve the project root.

```bash
node <skill>/scripts/quality/run-gates.mjs --url http://localhost:8765/quality/gate-harness.html \
  --ceiling quality/ceiling.json --out quality/pass-01 [--prev quality/pass-00] [--software] [--critic quality/pass-01/g4.json]
```

- **G0 Build:** imports resolve; zero runtime deprecation warnings; zero shader/WGSL/TSL compile warnings (the runner scans the console of both runs); typecheck passes (`npx tsc --noEmit` when the probe found TypeScript).
- **G1 Determinism:**
  - Seeded PRNG replaces `Math.random`, and fixed 16 ms steps drive a `THREE.Timer` with `_startTime` zeroed.
  - Await `LoadingManager`s, KTX2/Draco workers (as `extra` promises), `document.fonts.ready` and `renderer.compileAsync( scene, camera )` before frame 0.
  - Two independent page loads render to frame N. Zero NaN/Inf: the raw scene goes to a HalfFloat target and is scanned for non-finite halves.
  - Pass rule: exact SHA-256 match on a software rasterizer (`--software`), or `maxChannelDelta <= 1` across 99.9% of pixels on a hardware GPU.
- **G2 Resource & Lifecycle:**
  - GPU frame time (median of 10 timer queries), CPU frame time (median of 30), `renderer.info.render` (draw calls, triangles) and `renderer.info.memory` (geometries, textures, programs), all inside the ceiling.
  - Lifecycle soak: mount → render 120 frames → dispose → remount → render → dispose. Assert zero net delta on geometries, textures and programs.
  - Timing from a software rasterizer is reported as pending; measure it on the target hardware. For interactive pass-by-pass GPU timing, live TSL node graph values, and VRAM breakdowns on `WebGPURenderer`, attach Three's first-party `Inspector`:
    ```js
    import { Inspector } from 'three/addons/inspector/Inspector.js';
    renderer.inspector = new Inspector(); // mount before await renderer.init()
    ```
- **G3 Rendering:**
  - Automated: `renderer.outputColorSpace === SRGBColorSpace`; albedo/emissive/sheen/specular-colour maps `SRGBColorSpace`; every data map `NoColorSpace`; tone mapping not `NoToneMapping` unless the brief mandates unmapped (`"allowNoToneMapping": true`); every shadow-casting light has an allocated shadow map.
  - Material policy: enable EON rough diffuse (`diffuseRoughness`) only on hero dielectric assets already budgeted for `MeshPhysicalMaterial` with roughness above 0.5. Never upgrade background `MeshStandardMaterial` props if that threatens G2.
- **G4 Intent & Temporal Stability:**
  - An independent blind critic receives **only** `packet/`: a 3-angle static contact sheet (`contact.png`), a 3-frame motion burst at t, t+16 ms, t+32 ms (`burst.png`), a temporal luminance-delta heatmap (`heatmap.png`), the G2/G3 metric table (`metrics.md`) and the brief checklist (`checklist.md`).
  - It never sees your reasoning or your code diff. Run it as a fresh subagent whose prompt holds only the packet paths and the scoring instructions.
  - It fails immediately on temporal shimmer, z-fighting or shadow-cascade swimming.
  - It returns JSON, saved as `g4.json` and passed back with `--critic`:
    `{ "score": 0-10, "shimmer": bool, "zFighting": bool, "cascadeSwimming": bool, "checklistFailed": ["…"], "notes": "…" }`

## EACH PASS

1. Target the lowest failing gate G_k (`lowestFailing` in the runner output). Only that one.
2. Isolate one root cause. Fix one mechanism. You may touch any file that mechanism requires.
3. Re-measure G0 through G_k, and G_{k+1}…G4 once G_k passes. The runner appends the full metric vector to `quality/quality-log.jsonl`.
4. Keep the change **only if** no passing lower gate (G0 … G_{k−1}) regressed **and** the targeted sub-metric in G_k improved monotonically (even if a multi-bottleneck gate has not yet crossed its threshold). Otherwise `git revert` immediately. Commit each kept pass separately so a revert is one command.

Renames, comments, dead-code cleanup and formatting do not count as a pass.

## PHASE BUDGETS (decoupled)

- **Plumbing (G0–G1):** at most 3 passes. If build or determinism still fails after 3, halt and escalate the harness/environment blockers.
- **Convergence (G2–G4):** at most 6 passes. Plumbing fixes do not consume convergence passes.

## CONVERGENCE vs EXPANSION

Convergence closes the gap to the ceiling. It is finite. This loop does convergence only.

Expansion adds detail that is not in the brief. It is unbounded, and it is not a pass. If you see a detail worth adding, do not add it; log it as a proposed requirement. After the loop stops, a human decides whether to accept it. Accepted additions become a new brief: update the ceiling, re-run the probe, run the loop again, stop again.

## STOP WHEN

- **Converged:** G0–G4 all pass, and for 2 consecutive convergence passes the perceptual diff against the previous pass (`perceptualVsPrev.rmse`, from `--prev`) is below `perceptualRmse`, or the metric delta is inside measurement noise.
- **Stalled:** the targeted sub-metric is unchanged for 2 consecutive passes. Escalate to structural root-cause analysis. No third retry.
- **Capped:** 3 passes spent in G0–G1, or 6 passes spent in G2–G4. Past that you are polishing noise or fighting the architecture.

## REPORT

- Which stop rule fired, and in which phase (Plumbing vs Convergence).
- Full metric and gate vector history per pass (from `quality-log.jsonl`).
- Convergence trajectory: last-pass delta vs remaining gap to the ceiling, plus the pass-over-pass decay ratio. Classify it as **Asymptotic** (parameter tuning exhausted) or **Structural** (requires an architecture change outside the loop).
- Proposed expansions, one line each, not implemented.
