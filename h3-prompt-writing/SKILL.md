---
name: h3-prompt-writing
description: Plan, inspect, write, repair, and validate surface-aware MiniMax H3 (Hailuo 3.0) audiovisual prompts across T2VA, I2VA, FL2VA, L2VA, and Ref2VA. Invoke whenever the user asks for a MiniMax H3 or Hailuo 3 prompt, Context-IR structured prompt, hosted @Image/@Video/@Audio prompt, open-weight SGLang/vLLM/Diffusers H3 workflow, native ComfyUI MiniMaxH3 prompt, first/last-frame bridge, multi-reference video/audio conditioning, dense motion design, kinetic typography, game/pet UI states, or targeted H3 video editing and continuation.
---

# H3 Prompt Writing

Turn a brief and any supplied media into one verified, paste-ready MiniMax H3 prompt matched to the user's exact execution surface. Inspect supplied media first, route by asset role and target profile, enforce physical and audiovisual causality, and run `scripts/lint_h3_prompt.py` as a black-box validator before delivery.

## 1. Authority & Precedence Order

Resolve conflicts strictly in this order:

1. **User Literal Constraints**: Preserve exact dialogue, lyrics, visible strings, counts, and locked elements verbatim.
2. **Direct Media Inspection**: Ground every claim about supplied media in direct observation (`references/media-inspection.md`); never invent unseen features.
3. **Official Structured Grammar**: Follow `references/base-en.txt` and `references/ref-en.txt` verbatim when targeting the structured Context-IR profile.
4. **Target Surface Serialization**: Follow `references/runtime-surfaces.md` and `references/official-hosted-prompt-guide.md` when targeting native ComfyUI or the hosted surface. Hosted surfaces use upload-order `@Image N`, `@Video N`, and `@Audio N` handles; never leak those handles into structured or native-ComfyUI prompts.
5. **Confirmed User Baselines**: Preserve the working hierarchy, timeline density, and reference strategy of any user-confirmed prompt unless fixing a specific observed defect.
6. **Empirical Planning & Research Safeguards**: Apply `references/omni-reasoning-research.md`, `references/showcase-patterns.md`, `references/proven-dense-motion-design.md`, and `references/motion-design-fundamentals.md` within the selected profile's grammar.
7. **Pinned Community Overlays**: Treat `references/community-runtime-extensions.md` as optional graph-level guidance that never overrides official modes or limits.

## 2. Applicability Gate & Decision Tree

Before drafting, define the 5-item execution contract:
- **Surface**: `structured` (Context-IR / open-weight H3-Base), `comfyui` (`MiniMaxH3ImageToVideo` / `MiniMaxH3ReferenceToVideo`), or `hosted` (Hailuo / MiniMax Design freeform). Default to `structured` if unspecified and note the assumption outside the prompt.
- **Mode**: `T2VA`, `I2VA`, `FL2VA`, `L2VA`, or `Ref2VA`.
- **Topology**: **Single generation** (4–15s whole seconds, default shortest duration that fits all beats; $\ge$5s for Turbo LoRA) or **staged multi-clip assembly** (see Pattern D in `references/candidate-motion-design-patterns.md`).
- **Asset Roles & Hard Limits**: Media counts, durations, `17k+5` frame crop rules, and literal copy.
- **Verification Oracle**: What the rendered video and 32 kHz stereo track must visibly and audibly prove.

### Mode Selection Decision Tree

| Condition | Selected Mode | Required Grammar / Tag Rules |
| --- | --- | --- |
| Text alone defines the entire timeline (or `ComfyUI-H3-Motion-Context` transport chain) | **T2VA** | Read `references/base-en.txt`. No media tags. |
| Exactly 1 image is the literal frame at `0.00s`; no other reference roles | **I2VA** | Read `references/base-en.txt` (exact first-line alignment header + blank line). Native ComfyUI uses `<Picture 1>`. |
| Exactly 2 images are the literal first and final frames; no other reference roles | **FL2VA** | Read `references/base-en.txt` (exact FL2VA header + blank line). Native ComfyUI uses `<Picture 1>` then `<Picture 2>`. |
| Exactly 1 image is the literal final frame; no other reference roles | **L2VA** | Read `references/base-en.txt` (exact L2VA header + blank line). Native ComfyUI uses `<Picture 1>`. |
| Any asset provides identity, style, environment, prop, storyboard, motion, camera, voice/audio, edit master, or continuation source; or keyframes combine with references | **Ref2VA** | Read **both** `references/base-en.txt` and `references/ref-en.txt`. Concrete endpoints remain `<Picture N>` with `keyframe completion` in `summary`. |

**Ref2VA Hard Input Gate (`references/model-contract.md`)**:
- Maximum **9 images**, **3 videos** (2–15s each, $\le$15s combined), **3 standalone audio clips** (2–15s each, $\le$15s combined), and **12 total mixed files**.
- **Audio cannot be the sole media input** (requires $\ge$1 image or video).
- V2 API endpoint roles (`first_frame`, `last_frame`) and reference roles (`reference_image`, `reference_video`, `reference_audio`) are mutually exclusive at the transport layer; express mixed keyframe+reference plans inside Ref2VA (`keyframe completion`).

## 3. Selective Reference Loading

Load only the reference files required by the task:
- **Structured T2VA/I2VA/FL2VA/L2VA**: `references/base-en.txt`.
- **Structured Ref2VA**: `references/base-en.txt` + `references/ref-en.txt`.
- **Native ComfyUI**: `references/runtime-surfaces.md`.
- **Hosted Hailuo / MiniMax Design**: `references/official-hosted-prompt-guide.md`.
- **Physical-World & Audio-Visual Causality Mitigations**: `references/omni-reasoning-research.md`.
- **Page-Derived Task Recipes**: `references/showcase-patterns.md` (covers all 58 current page demonstrations).
- **High-Density Montage, Causal UI, Material Transforms**: `references/proven-dense-motion-design.md` + `references/motion-design-fundamentals.md`.
- **Procedural Construction & Counted Beat-Mapped Oners**: `references/edge-case-playbook.md` for cursor-, hand-, tool-, or machine-driven construction, or an exact count, BPM-synchronized choreography, or a complex one-take camera route.
- **Experimental / Staged Assembly / Optional JSON Brief**: `references/candidate-motion-design-patterns.md` or `references/hosted-creative-director-json.md`.
- **Community ComfyUI Extensions**: `references/community-runtime-extensions.md`.

## 4. Reference Binding & Causal Timeline Rules

### Reference Role Mapping
1. **Audit Supplied Media First**: Build an inventory table (`Asset | Observed content | Intended role | Preserve | Change | Literal text/audio | Confidence`) per `references/media-inspection.md`. If a required asset is inaccessible, stop and request it.
2. **Structured Ref2VA Labels**: Number `<Subject N>`, `<Picture N>`, `<Video N>`, and `<Audio N>` independently. Create `retention_analysis` rows only for standalone tracked labels, not inline provenance-only citations. Do not create `<Audio N>` merely because a video contains an audio track or for post-generation mux tracks.
3. **Native-ComfyUI Ordinals**: Wire the graph first. `<Picture N>` and `<Video N>` follow slot order; `<Audio N>` orders enabled reference-video soundtracks first (in video-slot order), then standalone audio files. Never emit `<Subject N>` in raw ComfyUI prompts.
4. **Dialogue Punctuation Scope**: Preserve user-supplied dialogue punctuation verbatim in base modes; apply the `ref-en.txt` punctuation normalization rule only to Ref2VA speech/lyrics transcribed or reperformed from source audio.

### Research-Grounded Causality & Timeline Construction (`references/omni-reasoning-research.md`)
0. **State Every Inference (`arXiv:2609.18323`)**: On 517 implicit-prompt instances, H3 succeeded 41.97% of the time overall. Never make H3 infer what a sound means, how views relate, how to react, or what a spoken instruction targets. Write the inference in the prompt.
1. **Write What the Audio Means (ADR — Audio-based Disambiguation, 27.40%)**: Never expect `<Audio N>` or an acoustic cue alone to decide or trigger a physical event. Name the event in text and pair every diegetic sound with its visible actuator, contact point, and result at the same timestamp.
2. **Write Cross-View Relations and Bridges (MSR — Multi-view Spatial Reasoning, 43.50%)**: When several images show one scene, state the spatial relation they establish. In `FL2VA`, `L2VA`, and multi-image `Ref2VA`, write the physical bridge (`support/grip -> transport path -> contact/alignment -> settled state`) instead of leaving manipulation steps implicit.
3. **Lock Continuation & Edit Boundaries (VDR 56.00% / AVIR — Audiovisual Integrated Reasoning, 47.89%)**: When continuing or editing `<Video N>`, state the intended reaction and its cause, the terminal pose, motion vector, and unchanged elements at the handoff. For speech-driven edits, quote the spoken constraint and name the on-screen element it changes.
4. **Co-Locate Audio-Visual Transients (`arXiv:2503.23377`, `arXiv:2508.00733`)**: Place diegetic sound effects and speech onsets inside the same timed clause as the visible contact or mouth articulation ($\le$2.5–3.0 words/s craft heuristic; stable speaker IDs in vocal-event order). Keep audience-only score strictly inside `non_diegetic_music` (and never pair `Non-diegetic music: N/A` with a BGM request).
5. **Distinguish Shots from Continuous Phases**: In structured prompts, increment `[Shot N]` only at a real camera cut. For continuous takes (`one continuous shot`), remove cut structures and define a single spatially traversable camera route without using flashes or foreground wipes to hide cuts.
6. **Procedural, Counted, & BPM-Locked Precision**:
   - **Procedural creation**: Write `actuator -> visible input -> tool-consistent effect -> retained result`. Keep control-only reference images off-screen.
   - **Exact counts**: Declare whether the counted unit is an instantaneous event or held state, number each occurrence once, and add no unnumbered extras.
   - **BPM sync**: Declare beat origin, compute `60 / BPM` seconds per beat, and align beat numbers with second timestamps.
   - **Typography & UI**: Quote literal strings verbatim, specify entry/hold/exit, and distinguish a frozen hero hold from a living lockup hold. On hosted surfaces where typesetting garbles, supply an approved text plate as an image reference and instruct H3 to render it as an image.
7. **Untrimmed `17k+5` Frame Clock Math (Local Graphs)**:
   ```text
   requested_delivery_frames = round(requested_delivery_seconds * 24)
   raw_frames = smallest (17k + 5) >= requested_delivery_frames + leading_trim_frames
   trailing_trim_frames = raw_frames - leading_trim_frames - requested_delivery_frames
   ```
   Write prompt timestamps on the untrimmed clock and finish all required payoffs by `(raw_frames - trailing_trim_frames) / 24`.

## 5. Required Output Schemas by Profile

- **Structured Base (`T2VA`, `I2VA`, `FL2VA`, `L2VA`)**: Exact endpoint alignment header ( plus blank line for `I2VA`/`FL2VA`/`L2VA`), then:
  `integrated_multimodal_description:` $\rightarrow$ `overall_soundscape:` $\rightarrow$ `non_diegetic_music:`.
- **Structured `Ref2VA`**:
  `subject_definitions:` $\rightarrow$ `summary:` $\rightarrow$ `retention_analysis:` $\rightarrow$ `detailed_description:` $\rightarrow$ `overall_soundscape:` $\rightarrow$ `non_diegetic_music:`.
- **Native ComfyUI (`--profile comfyui`)**: One freeform block using `<Picture N>`, `<Video N>`, and `<Audio N>` tags (no Context-IR section headers, no `<Subject N>`).
- **Hosted Freeform (`--profile hosted`)**: `Reference Asset Instructions` $\rightarrow$ `Core Concept` $\rightarrow$ `Shot-by-Shot Description` using `@Image N`, `@Video N`, `@Audio N` upload-order handles.

## 6. Verification Gate (Black-Box Linter Execution)

Do not read the full source of `scripts/lint_h3_prompt.py` into context unless debugging a script change. Save the draft prompt to a temporary file and run the linter as a black-box CLI gate:

```bash
# Structured profile
python3 scripts/lint_h3_prompt.py PROMPT.txt --mode MODE --duration SECONDS

# Native ComfyUI profile
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile comfyui --mode ref2va --duration SECONDS --pictures N --videos N --audios N --standalone-audios N

# Hosted freeform profile
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile hosted --mode MODE --duration SECONDS
```

Append `--raw-frames N`, `--trim-frames N`, and `--tail-trim-frames N` when local graph cropping applies. Fix all linter errors and verify semantic invariants (exact literal strings, causal bridges, off-screen control exclusions, and zero leaked wrapper commentary inside the prompt block). When modifying skill documentation, run `python3 scripts/validate_coverage.py`.

## 7. Delivery Format & Hard Prohibitions

Deliver in this compact layout unless the user requests a standalone prompt block only:

````text
Upload map:
- [user filename] -> [role / provider label]

Settings:
- Surface/profile: ...
- Requested delivery: ... seconds / ... frames
- Raw render: ... seconds / ... frames
- Crop: ... leading / ... trailing frames
- Aspect ratio: ...
- Resolution: ...

Prompt:
```text
[paste-ready provider-native prompt only]
```

Assumptions or warnings:
- ...
````

### Do Not
- Do not claim to have inspected inaccessible media or treat a storyboard sheet as a literal opening frame when it is only shot order.
- Do not mix handle syntaxes across profiles (`@Image N` in structured/ComfyUI or `<Subject N>` in raw ComfyUI/hosted).
- Do not use audio as the sole Ref2VA input, assign `<Audio N>` to post-mux tracks, or rely on audio alone to imply a visual state change (ADR trap).
- Do not omit `references/base-en.txt` rules when writing `Ref2VA`, normalize the three endpoint alignment headers, or paraphrase supplied copy.
- Do not promote `Hybrid`, Turbo, audio-lock, or motion-context graph settings into official H3 modes, or simplify a user-confirmed high-density prompt without an observed defect.

## 8. Resource Index

- [`references/base-en.txt`](references/base-en.txt): Immutable official grammar for T2VA/I2VA/FL2VA/L2VA and shared audiovisual rules.
- [`references/ref-en.txt`](references/ref-en.txt): Immutable official Ref2VA grammar.
- [`references/model-contract.md`](references/model-contract.md): Audited capabilities, limits, pricing/licensing snapshots, and surface boundaries.
- [`references/omni-reasoning-research.md`](references/omni-reasoning-research.md): Implicit-prompt physical-reasoning benchmark (`arXiv:2609.18323`, 517 instances, 4 failure types), physics benchmarks (Physics-IQ, VideoPhy, PhyGenBench, VBench-2.0), joint audio-video DiT alignment (`arXiv:2503.23377`, `arXiv:2508.00733`), negation (NegBench), and ADR/MSR/AVIR/VDR failure mitigations.
- [`references/runtime-surfaces.md`](references/runtime-surfaces.md): Structured, hosted, and native-ComfyUI profiles.
- [`references/official-hosted-prompt-guide.md`](references/official-hosted-prompt-guide.md): August 11 hosted three-part formula, `@Image N`/`@Video N`/`@Audio N` handles, and pitfalls.
- [`references/community-runtime-extensions.md`](references/community-runtime-extensions.md): Pinned third-party ComfyUI overlays and frame-grid rules.
- [`references/media-inspection.md`](references/media-inspection.md): Media, frame, and audio inspection protocol.
- [`references/showcase-patterns.md`](references/showcase-patterns.md): All 58 current page demonstrations and durable prompting lessons.
- [`references/proven-dense-motion-design.md`](references/proven-dense-motion-design.md): Validated high-density montage, causal-UI, and material-transformation patterns.
- [`references/motion-design-fundamentals.md`](references/motion-design-fundamentals.md): Motion-design compiler, typography, timing, and sound checks.
- [`references/candidate-motion-design-patterns.md`](references/candidate-motion-design-patterns.md): Evidence-bounded experimental patterns and staged multi-clip assembly.
- [`references/hosted-creative-director-json.md`](references/hosted-creative-director-json.md): Optional hosted JSON creative brief organization.
- [`references/edge-case-playbook.md`](references/edge-case-playbook.md): Safeguards for procedural creation, exact counts, and beat-mapped oners.
- [`scripts/lint_h3_prompt.py`](scripts/lint_h3_prompt.py): Deterministic structural and timing validator (run as black-box CLI).
- [`scripts/validate_coverage.py`](scripts/validate_coverage.py): Repository coverage and grammar-hash validator.
