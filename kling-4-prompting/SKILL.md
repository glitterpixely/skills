---
name: kling-4-prompting
description: Write, optimize, audit, and repair Kling 4.0 and Kling 4.0 Flash video prompts using model-specific limits, explicit reference ownership, and Kuaishou DiT/Omni conditioning rules. Invoke whenever the user requests a Kling 4 or Kling 4.0 Flash prompt for text-to-video, image animation, First & Last Frames, multi-keyframes (up to 10), Omni Reference (up to 15 combined assets), white-model/depth/camera transfer, creative ad recreation, synchronized stereo dialogue, visible scene lettering/UI, targeted video editing, or multi-clip continuation plans.
---

# Kling 4 Prompting

Turn a user brief and supplied reference assets into a concise, paste-ready Kling 4.0 or Kling 4.0 Flash prompt with separately stated generation settings. Enforce single-owner reference binding, physical causality, 6-DoF camera separation, and hard model budget checks before delivery.

Read [`references/capabilities.md`](references/capabilities.md) for audited Kling 4.0 vs. Flash specifications (snapshot: `Meet All-New Kling 4.0!`, 2026-09-28) and [`references/kling-architecture-research.md`](references/kling-architecture-research.md) for Kuaishou DiT / Kling-Omni (`arXiv:2512.16776`, `arXiv:2503.19907`, `arXiv:2501.04698`, `arXiv:2503.11647`) failure mitigations.

## 1. Model & Operation Decision Tree

### Step 1A: Verify Model Tier & Hard Budgets (`references/capabilities.md`)

| Dimension | Full Kling 4.0 (Documented) | Kling 4.0 Flash (Documented) | Enforcement Rule |
| --- | --- | --- | --- |
| **Modes** | T2V, I2V, First & Last Frames, Multi-keyframes, Omni Reference, Video Editing | T2V, I2V, Omni Reference | Do not silently transfer Full 4.0 modes (e.g., 10 keyframes, editing) to Flash without flagging unconfirmed parity. |
| **Duration** | **3–30 seconds** per generation | **3–20 seconds** per generation | Fit all beats and speech inside the single-call cap; plan multi-clip sequences beyond 30s (or 20s on Flash). |
| **Resolution & Range** | 720p, 1080p, 4K (10-bit HDR marked *coming soon*) | 720p, 8-bit SDR | State resolution/HDR in external `Settings`, not as proof inside prompt prose. |
| **Aspect Ratio** | `21:9`, `16:9`, `1:1`, `9:16`, `Auto` | Surface-dependent | Compose for the target frame; keep ratio in `Settings`. |
| **Prompt Cap** | Up to **8,000 tokens** | Unspecified in Flash table | Treat 8,000 tokens as ceiling capacity, not a verbosity target. |
| **Reference Caps (Full 4.0)** | $\le$**15 combined** ($\le$10 images, $\le$5 videos totaling $\le$30s, voice audio, $\le$7 elements including $\le$3 video elements) | Check live Flash surface | Enforce **both** per-type caps and the 15-item / 30s combined ceiling. Never silently drop required user assets. |
| **Video Editing** | $\le$**5 input clips** (1 primary + up to 4 supporting), each 3–30s, **combined $\le$30s total** | Not in Flash table | Include the primary video's duration inside the 30-second total editing budget. |

### Step 1B: Route to Exactly One Operation

| User Goal | Selected Operation | Controlling Input & Structural Rule |
| --- | --- | --- |
| Invent a scene from scratch | **Text-to-Video** | One causal action chain with opening state, physical change, and terminal hold. |
| Animate an existing still | **Image-to-Video** | Source image locks initial appearance/layout; spend prompt words on **what moves** vs. what stays fixed. |
| Bridge two exact compositions | **First & Last Frames** | Inspect both frames; write the physical locomotion, grip, lighting, and camera bridge connecting them. |
| Hit 3–10 ordered story states | **Multi-Keyframes** (up to 10 on Full 4.0) | Order keyframes chronologically; specify the physical transition or explicit cut between each node. |
| Combine identity, motion, camera, layout, or voice | **Omni Reference** | Assign one non-overlapping role per asset; state each asset's positive job first, then one short exclusion (`arXiv:2512.16776`, `arXiv:2503.19907`, `arXiv:2501.09425`). |
| Reuse an ad/clip's pacing & camera with new product/cast | **Creative Recreation** | Separate inherited shot timing/camera from replacement identity/product geometry and hand grip. |
| Modify a region, expression, style, or background in footage | **Video Editing** | Designate **one primary video**; state edited interval/target and explicitly preserve all untargeted content. |
| Add footage after an existing clip's ending | **Continuation / Adjacent Clip Plan** | Native repeated extension (up to 2 min) is marked *coming soon*; unless verified live, write a standalone adjacent clip carrying forward the source's terminal pose, velocity, camera vector, and audio. |

## 2. Reference Ownership & Anti-Bleeding Protocol

1. **Inspect Accessible Media First**: Never diagnose an unseen render or infer motion from a single still.
2. **Build an Ownership Ledger (`Kling-Omni` `arXiv:2512.16776` & `FullDiT` `arXiv:2503.19907`)**:
   Give each uploaded asset one authoritative dimension and explicitly block cross-modal contamination:
   - **Identity / Multi-view sheet** $\rightarrow$ Inherits face, body proportions, outfit; excludes reference background and static pose. State clearly when multiple views depict **one single character** (`ConceptMaster`, `arXiv:2501.04698`).
   - **Performance / Action video** $\rightarrow$ Inherits gesture sequence and rhythm; excludes reference performer's face, body, costume, and room.
   - **White-model / Depth / Wireframe / Camera video** $\rightarrow$ Inherits camera trajectory, obstacle spacing, and timing; explicitly replace all gray proxy/wireframe surfaces with finished scene materials (`FullDiT`, `arXiv:2503.19907`).
   - **Voice reference audio** $\rightarrow$ Documented for **voice identity only**; bind to a named speaker and never promise music, SFX, or full-mix transfer from an audio upload.
3. **Write Positive Ownership Before Exclusions (`NegBench`, `arXiv:2501.09425`)**: Vision-language encoders often miss negation. Write `use the performance video only for timing and gesture order`, then one short `do not inherit ...` clause. Never rely on a long `no ...` list alone.
4. **Use Real Surface Handles or Plain Prose**: Use actual attachment names when supplied; otherwise write clear prose (`the character reference image`, `the performance reference video`) plus an external upload map. Never invent fake Kling token syntax or import Seedance `@Image 1`, H3 `<Subject N>`, or Midjourney `--` flags into Kling prompt prose.

## 3. Prompt Compilation Formula

Compile prompts in this deterministic 7-part sequence (`references/prompt-patterns.md`):

`[1. Reference Role & Exclusion Header] -> [2. Opening Spatial State & Subject Cardinality] -> [3. Causal Action & Contact Chain] -> [4. 6-DoF Camera Trajectory] -> [5. Medium & Visual Treatment] -> [6. Stereo Audio, Dialogue & Lettering] -> [7. Terminal State & Hard Constraints]`

### Imperative Drafting Rules
- **Physical Causality Before Spectacle (`Physics-IQ` `arXiv:2501.09038`, `VideoPhy` `arXiv:2406.03520`)**: Visual realism does not imply correct physics. Establish footing, approach vector, both contact materials, and the contact point before debris, sparks, or reaction recovery. Replace vague "subtle movement" fillers with concrete amplitudes and trajectories.
- **Decouple Camera from Subject Motion (`arXiv:2503.11647`, `arXiv:2404.02101`)**: State starting framing, camera travel direction, tracked target, and ending framing without crossing the 180° action axis or combining contradictory moves (`fixed camera` + `orbit`).
- **Topology Honesty**: Explain continuous-take transitions via camera travel or foreground pass; if shots cut, name the cut and new angle explicitly.
- **Preserve Stylized Media**: Do not overwrite requested anime, clay, felt, 2D illustration, or 3D cyber styles with generic photorealistic lens buzzwords.
- **Dialogue & Two-Channel Stereo Audio**:
  - Name the speaker, language/accent, exact quoted words, and turn order ($\approx$2–3 words/s conversational pacing). Keep non-speaking listeners' mouths closed.
  - Place sound sources in screen-relative stereo space (`rolls from screen right to screen left`). Do not invent numerical pan values or stem exports.
  - Default to scene-appropriate ambience and foley with `No music` unless score is requested.
- **Visible Text & UI**: Quote exact strings, script/language, surface placement, causal trigger (e.g., button press $\rightarrow$ state change), and readable hold duration.

## 4. Verification & Repair Gate

Before outputting, verify every item in this checklist (and consult [`references/review-and-repair.md`](references/review-and-repair.md) when diagnosing a user's rendered clip; sort render findings by the VBench-2.0 headings: Human Fidelity, Controllability, Creativity, Physics, Commonsense):
- [ ] **Model & Budget Compliance**: Duration (3–30s Full / 3–20s Flash), reference counts ($\le$15 total, $\le$10 images, $\le$5 videos $\le$30s), and editing duration ($\le$30s including primary clip) are within documented bounds.
- [ ] **Single-Owner Dimensions**: No two references compete for identity, motion, or camera; proxy/performer exclusions and exact subject counts (`one of each`) are explicit.
- [ ] **Keyframe / Continuation Continuity**: Every keyframe pair has a physical or editorial bridge; continuations start from the source's exact terminal pose and velocity rather than restarting the action.
- [ ] **Clean Prompt Boundary**: Settings (model, mode, duration, aspect ratio, resolution, HDR) and upload mappings sit outside the fenced prompt block.

## 5. Delivery Format & Hard Prohibitions

Lead directly with the copy-ready prompt block, followed by compact settings and reference bindings (omit wrapper text if the user asked for prompt-only output):

````text
Prompt:
```text
[paste-ready Kling 4 prompt only]
```

Settings & Reference Map:
- Model & Operation: [Full Kling 4.0 | Kling 4.0 Flash] — [Operation]
- Duration / Aspect Ratio / Resolution: ...
- Reference Bindings: [asset -> role, inherited traits, exclusions]
- Availability / Limit Note: [only if HDR, native extension, or Flash parity applies]
````

### Do Not
- Do not equate an ordered multi-keyframe sequence with an unordered identity reference set.
- Do not promise music, SFX, or full-mix audio transfer from voice-only reference audio uploads.
- Do not invent Kling API endpoints, JSON payloads, model IDs, seeds, CFG scales, or negative-prompt fields not established in official docs.
- Do not present the forthcoming 2-minute repeated extension ceiling as a single 120-second generation call.
- Do not conflate prompt drafting, queue submission, rendering, frame inspection, and audio listening into a single "verified" state.

## 6. Resource Index

- [`references/capabilities.md`](references/capabilities.md): Audited Kling 4.0 vs. Flash specifications, reference accounting rules, language coverage, and availability boundaries.
- [`references/kling-architecture-research.md`](references/kling-architecture-research.md): Kuaishou research (Kling-Omni `arXiv:2512.16776`, FullDiT `arXiv:2503.19907`, ConceptMaster `arXiv:2501.04698`, ReCamMaster/SynCamMaster `arXiv:2503.11647`, `arXiv:2412.07760`) plus physics, camera, negation, and evaluation evidence (Physics-IQ, VideoPhy, CameraCtrl, NegBench, VBench-2.0), with paper findings separated from derived prompt rules.
- [`references/prompt-patterns.md`](references/prompt-patterns.md): Production-ready prompt patterns across T2V, I2V, First & Last Frames, Multi-keyframes, Omni Reference, white-model/depth transfer, creative recreation, stereo dialogue, UI, editing, and continuation.
- [`references/review-and-repair.md`](references/review-and-repair.md): Pre-generation checklist, render inspection protocol, and failure-to-repair diagnostic table.
