# H3 Runtime Surfaces

Read this reference when the user names an API, hosted product, local H3-Base workflow, or ComfyUI. It determines prompt serialization and runtime handoff; it does not change the five canonical H3 modes or the official media limits.

## Contents

- [Audited Sources](#audited-sources)
- [Choose One Prompt Profile](#choose-one-prompt-profile)
- [Structured Profile](#structured-profile)
- [Official Open-Weight Serving](#official-open-weight-serving)
- [Direct V2 API](#direct-v2-api)
- [Native ComfyUI Profile](#native-comfyui-profile)
- [Native-ComfyUI Freeform Assembly](#native-comfyui-freeform-assembly)
- [Hosted Freeform Profile](#hosted-freeform-profile)

## Audited Sources

- MiniMax official repository, commit `d21241f0a4b3acbb34c97dae47fa417b7065e438` (August 15, 2026): `https://github.com/MiniMax-AI/MiniMax-H3`
- MiniMax official structured prompt grammar at that commit: `base-en.txt` and `ref-en.txt` in this skill, preserved byte-for-byte.
- MiniMax Open Platform V2 create contract, audited August 27, 2026: `https://platform.minimax.io/docs/api-reference/video-generation-v2-create`
- Official ComfyUI H3 guide, audited August 8, 2026: `https://docs.comfy.org/tutorials/video/minimax/minimax-h3`
- Official ComfyUI implementation audited at commit `40e46c711025947f126cccaa1a692a14937a3096`.
- Official ComfyUI workflow templates: moving snapshots of `video_minimax_h3_t2v.json`, `video_minimax_h3_i2v.json`, and `video_minimax_h3_r2v.json` from `https://github.com/Comfy-Org/workflow_templates`, retrieved August 8, 2026. Re-inspect current graphs before relying on defaults.
- Product showcase revision dated August 11, 2026: the Notion page cited in `model-contract.md`.

Authority order is MiniMax model contract and grammar, official target-surface documentation/templates, showcase evidence, then community extensions. A runtime default never becomes a provider-wide capability rule.

## Choose One Prompt Profile

| Profile | Use when | Serialization |
| --- | --- | --- |
| Structured | The workflow expects provider skill output, Context-IR-style preprocessing, direct open-weight H3-Base input, or the surface is unknown | Exact three-field base grammar or six-field Ref2VA grammar |
| Native ComfyUI | Prompt goes directly into `MiniMaxH3ImageToVideo` or `MiniMaxH3ReferenceToVideo` | One freeform audiovisual prompt; endpoint `<Picture N>` tags in I2VA/L2VA/FL2VA and exact connected-media tags in Ref2VA |
| Hosted/API freeform | MiniMax Design, Hailuo, or the V2 generation API accepts natural-language intent and performs hosted preprocessing | Official three-part semantic formula; visible hosted upload handles only when that surface exposes them |

Default to Structured when the target is unknown. State the assumption outside the prompt.

## Structured Profile

MiniMax describes the complete system as:

1. H3-Context-IR structures text and multimodal context;
2. H3-Base generates 768p audiovisual output;
3. H3-Regenerate-2K performs the higher-resolution regeneration stage.

The official repository says Context-IR is important to the hosted pipeline but is not open sourced. For a local Base workflow without it, follow the official prompting guides manually. Use `base-en.txt` for T2VA/I2VA/FL2VA/L2VA and both grammar files for Ref2VA. Do not alter their headings, order, alignment lines, label forms, or dialogue rules.

The structured profile is the skill's highest-fidelity portable handoff. It is not proof that every raw text box requires the serialized headings.

## Official Open-Weight Serving

The current official repository releases two separate BF16, CFG-distilled H3-Base checkpoint families:

- Base FL2VA: T2VA plus first-frame, last-frame, and first-plus-last-frame generation;
- Base Ref2VA: reference generation from text plus image, video, and/or audio conditions.

MiniMax now documents official serving paths for SGLang, vLLM, Diffusers, and ComfyUI. Route by the checkpoint family and the serving adapter's actual prompt input; for direct H3-Base text without hosted Context-IR, use the Structured profile unless the adapter's official template demonstrably expects raw freeform text.

Local H3-Base generates 768p audiovisual output. H3-Context-IR and H3-Regenerate-2K remain hosted and were not open sourced at the audited commit. Do not promise a local-only 2K workflow merely because the hosted API accepts `2K`; official 2K uses context-aware regeneration with the original multimodal context.

The model architecture was trained with native sparse attention, but the initial open release performs inference with full attention. Treat current framework performance and memory guidance as runtime-specific, not as prompt rules.

## Direct V2 API

The V2 generation endpoint requires one non-empty `text` content item plus any media items. Put `resolution`, `duration`, `ratio`, callback handling, URLs, and content `role` values in the request, outside the prompt text.

Use these transport-role rules:

- T2VA: text only.
- I2VA/L2VA/FL2VA: text plus one or two images labeled `first_frame` and/or `last_frame`.
- Ref2VA: text plus `reference_image`, `reference_video`, and/or `reference_audio` items.
- Endpoint roles and reference roles are mutually exclusive in one V2 request.

The API's `role` values are not prompt handles. Do not turn `reference_image` into `@Image 1` unless a separate hosted UI or prompt preprocessor documents that handle. For the direct V2 text item, use the official hosted three-part formula in `official-hosted-prompt-guide.md` when sending natural-language intent, or send exact Structured output when a preceding Context-IR/manual expansion stage produced it.

API settings differ by mode: T2VA requires a concrete supported ratio; I2VA always derives its ratio from the endpoint image and ignores a concrete ratio in favor of `adaptive`; Ref2VA defaults to `adaptive` but accepts a concrete supported ratio. The API accepts `768P` and `2K` output tiers. Re-check `model-contract.md` for current media limits and formats.

## Native ComfyUI Profile

The official ComfyUI guide documents native T2V, I2V, and R2V support in ComfyUI 0.30.0 or newer. Its official workflow templates send freeform prompts directly to the model and keep node settings outside the prompt.

### Base Modes

- Use `MiniMaxH3ImageToVideo` with the FL2VA checkpoint family.
- No image, first frame only, last frame only, or both endpoints select T2VA, I2VA, L2VA, or FL2VA through node inputs.
- Write one freeform audiovisual block. Do not add Context-IR headings merely to imitate the structured profile.
- Native keyframes are exposed to the prompt in connection order: I2VA first frame is `<Picture 1>`, L2VA last frame is `<Picture 1>`, and FL2VA first/last frames are `<Picture 1>` and `<Picture 2>`. Use no Video, Audio, or Subject tags in these base modes.
- Pass an explicit linter `--mode` for every native picture-endpoint prompt. A picture-only tag map is ambiguous among I2VA, L2VA, FL2VA, and picture-based Ref2VA.
- The official template uses a native 768-pixel short edge, dimensions rounded to multiples of 32, and a template canvas cap of 1344 by 768 in either orientation. Treat these as that local workflow's settings, not hosted H3 limits.

### Ref2VA

- Use `MiniMaxH3ReferenceToVideo` with the separate Ref2VA checkpoint family.
- The official node accepts up to 9 images, 3 reference videos, and 3 standalone audios, subject to the official duration and mixed-file limits in `model-contract.md`.
- Picture and Video ordinals follow node-slot order. Audio ordinals follow the official node's fixed serialization: enabled reference-video soundtracks in video-slot order first, followed by standalone audios. Use those exact `<Picture N>`, `<Video N>`, and `<Audio N>` tags rather than assuming one global wiring order.
- Give every connected asset one job: identity, style, composition, motion, camera, voice, source edit, or audio.
- Do not use `<Subject N>` as a raw connected-media handle. That label belongs to the structured Ref2VA analysis grammar.
- `ref_image_size=match` scales references to generation resolution and is faster. `ref_image_size=max` preserves up to a 2048-pixel short edge for stronger identity detail but increases reference-token cost and runtime.

### Frame And Audio Runtime

Official templates convert requested seconds to a valid 24 FPS frame count with:

```text
max(5, round(seconds * 24)) + (5 - (max(5, round(seconds * 24)) % 17)) % 17
```

This yields a `17k+5` frame grid and may make the rendered clip slightly longer than the requested seconds. Keep the requested duration and aligned render duration separate. A community graph may add another pad/trim window; if so, prompt on its untrimmed render clock and report the delivery crop outside the prompt.

H3 produces a packed audiovisual latent. The official workflow decodes video and audio with their separate H3 VAEs and muxes them at 24 FPS. Do not describe native audio as an unrelated post-production layer.

### Official Template Defaults

- The audited templates use 20 sampling steps and `res_multistep`.
- The Ref2VA template notes that `beta` or `normal` scheduler often performs better than `simple` for reference-heavy prompts, although the downloadable graph must be inspected because defaults can change.
- T2VA/FL2VA and Ref2VA use different diffusion checkpoints.
- Dtype fallback warnings can be expected on some hardware. Re-check the official guide and the actual installed ComfyUI build before troubleshooting a current graph.

These are reproducible official-template settings, not universal quality guarantees.

## Native-ComfyUI Freeform Assembly

Write the raw block in this order:

1. visual medium, scene, and composition anchor;
2. one explicit job for every connected media tag;
3. chronological visible actions and intermediate states;
4. camera and performance behavior;
5. literal dialogue, visible text, synchronized effects, ambience, and music;
6. exact preservation and exclusion clauses;
7. final readable or stable hold.

Do not include upload maps, model filenames, LoRA strengths, samplers, schedulers, resolution, seed, trim metadata, or warnings inside the prompt.

Validate with actual graph counts:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile comfyui --mode ref2va --duration SECONDS --pictures N --videos N --audios N --standalone-audios N
```

Here `--audios` is the number of connected audio ordinals, including enabled reference-video soundtracks; repeated mentions of one `<Audio N>` still count once. `--standalone-audios` counts separate audio files. The linter checks exact tag spelling, connected ordinals, official counts, the visual-media requirement for audio, time ranges, and the native frame-grid snap. It cannot prove that a connected asset's semantic job matches its pixels or sound.

For a graph that crops after decode, pass its requested pre-snap seconds with `--duration`, its actual untrimmed count with `--raw-frames N` when available, `--trim-frames N` for the leading crop, and `--tail-trim-frames N` for the trailing crop. The linter reports the delivery duration, raw-to-delivery timestamp offset, and timed ranges that fall into the discarded tail. To target an exact delivery frame count, choose the smallest `17k+5` raw count that can contain the requested frames plus required context, then assign any residual to the trailing crop.

## Hosted Freeform Profile

The August 11 hosted guide defines a semantic planning formula—**Reference Asset Instructions + Core Concept + Shot-by-Shot Description**—rather than the six-field Context-IR serialization. Read `official-hosted-prompt-guide.md` before writing for MiniMax Design, Hailuo, or another surface known to follow that guide.

- Use upload-order `@Image N`, `@Video N`, and `@Audio N` handles only when the hosted surface exposes them. Give each asset one bounded job. Direct V2 API requests instead bind media through explicit `role` metadata; do not paste hosted handles into API role fields.
- Treat cuts as the hosted default. For one continuous take, remove separate shot/cut structures and describe one unbroken causal path. State J-cuts or L-cuts explicitly when a line crosses an edit.
- Quote visible copy and dialogue exactly. If native rendering garbles approved text, supply the approved text plate as an image reference and state: “This content must be interpreted as an image, not processed as text.”
- Keep the same causal planning, physical camera language, preservation clauses, and literal-copy discipline as the structured grammar.
- Freeform organizational devices that a compatible surface or user-confirmed output has demonstrated—including a `PARAMETERS` dictionary, zero-padded `CUT` headers, bare timed macro-stage headers, and global motion/audio/exclusion blocks—remain optional extensions, not official structured fields.
- Keep each declared parameter single-valued and each complete timeline contiguous. Do not claim that a showcase example is a complete recipe when it is marked partial.
- Hosted prose may follow the user's requested language. The immutable English structured templates keep their own localization rule.
- Check the live surface before promising codecs, prices, resolutions, availability, or UI labels.

Validate a hosted prompt's length, chronology, declared cut count, parameter bindings, handle spelling, mode/handle boundary, and obvious music/topology conflicts without applying native-ComfyUI media-tag requirements:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile hosted --mode MODE --duration SECONDS
```

The linter cannot verify what an uploaded asset contains, whether a role assignment is semantically true, or every multilingual phrasing conflict. Review those manually. If the user needs a portable prompt independent of one hosted UI, return the Structured profile instead.
