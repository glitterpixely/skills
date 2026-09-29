# H3 Community Runtime Extensions

Read only the section for a community repository the user explicitly names or whose graph they provide. These are dated, third-party ComfyUI overlays. They may change conditioning, sampling, or post-processing, but they do not create new MiniMax modes, relax official media limits, or supersede `base-en.txt`, `ref-en.txt`, `model-contract.md`, or `runtime-surfaces.md`.

Do not copy GPL implementation code into this skill. The rules below are independently written behavioral summaries with source attribution.

## Contents

- [ComfyUI-H3-Motion-Context](#comfyui-h3-motion-context)
- [comfyui-minimax-h3-audio-T8](#comfyui-minimax-h3-audio-t8)
- [MiniMax-H3-Turbo-LoRA](#minimax-h3-turbo-lora)

## ComfyUI-H3-Motion-Context

Source: `https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context`  
Audited commit: `15fc6a7bf7b78efb27f33d7eef3818e7ed0e118a`  
Audit date: August 8, 2026  
License: GPL-3.0

### Narrow Routing Exception

When the user explicitly targets this plugin:

- classify every chained segment as canonical T2VA;
- treat `context_frames`, `context_latent`, and transported tail audio as graph state, not Ref2VA assets;
- do not emit `<Video N>` or `<Audio N>` for that transport state;
- do not label the operation as the official Ref2VA `video continuation` task;
- serialize with the target surface's base profile: native-ComfyUI freeform for a raw node, or the exact base grammar only when a preprocessing workflow expects it.

The current plugin writes new `minimax_keyframes` and, when audio is wired, a new `minimax_refs` list without appending. It therefore discards stock first/last keyframes and existing Ref2VA references. Do not combine this audited version with I2VA, FL2VA, L2VA, or Ref2VA conditioning unless the plugin implementation changes and is re-audited.

### Render Clock And Handoff

In recommended `head` mode, pinned context occupies the start of the raw generated clip and is removed only after decode. Prompt timestamps must therefore use the untrimmed render clock.

```text
overlap_seconds = trim_frames / 24
delivered_timestamp = raw_prompt_timestamp - overlap_seconds
delivered_frames = raw_frames - trim_frames
delivered_duration = delivered_frames / 24
```

With the recommended 22-frame overlap, raw `0.000–0.917s` is carry-over context. Place the first new delivered beat at or after raw `00:00.917`; it becomes delivery time 0 after trim.

At the start of each later segment, restate:

- exact pose and action phase at the seam;
- subject direction and speed;
- object momentum and contact state;
- camera vector, amplitude, and speed;
- lighting and environmental motion;
- continuing ambience, dialogue phase, tempo, and instrumentation;
- the first new action after the overlap.

Keep canvas, aspect ratio, and 24 FPS constant through the chain. Use the node's returned `trim_frames`; off-grid requests can snap to a supported context run.

### Community-Tested Starting Configuration

- `context_length: 22`
- `encode_mode: video`
- `anchor_mode: head`
- `audio_mode: timeline`
- `audio_context_length: 22`
- trim picture and audio together
- `match_tail: true`
- Spectrum disabled
- indexed Load/Save slots for retry-safe chains
- `context_latent` preferred over decoded `context_audio` to avoid an extra audio-VAE round trip

These settings are community-tested, not official MiniMax defaults.

### Risks

- The plugin monkey-patches moving ComfyUI internals. Its layout patch has semantic checks, but the payload patch is not fully fail-closed.
- Do not promise an identical waveform. The author reports high join correlation, a roughly 10 ms fixed offset, cumulative high-frequency dulling, and limited testing on one machine/configuration.
- The repository contains no real-output fixtures that independently reproduce its perceptual claims.
- Do not copy its example workflow as authority: the audited example conflicts with the README on Spectrum, prompt duration versus raw frames, and audio-context length.

## comfyui-minimax-h3-audio-T8

Source: `https://github.com/T8mars/comfyui-minimax-h3-audio-T8`  
Audited commit: `5ff46c253192e9d8cae185280fd34f4b4add063b`  
Audited package version: 1.3.3  
Audit date: August 8, 2026  
License: GPL-3.0-or-later; Python 3.10+; relies on ComfyUI, PyTorch, torchaudio, and private H3 internals

### Official Input Gate Still Applies

The T8 preflight does not enforce every official rule. Before drafting or running, independently verify:

- 4–15-second H3 output;
- no more than 9 images, 3 videos, 3 standalone audio files, and 12 mixed files;
- every reference video and standalone audio file is 2–15 seconds;
- combined reference-video duration and combined standalone-audio duration are each no more than 15 seconds;
- audio is not the sole media input.

Do not accept the repository's audio-only example as evidence that official Ref2VA allows audio-only input.

### Resolve Media Ordinals After Wiring

Use the native-ComfyUI freeform profile for the audited T8 conditioning node. Do not insert structured Context-IR headings unless a separate upstream preprocessor explicitly consumes them.

The audited node orders audio labels from enabled reference-video soundtracks, then `drive_audio` when it is added as a reference, then standalone reference audios. For a T8 graph:

1. connect every asset;
2. inspect the emitted `media_map_json`;
3. assign `<Picture N>`, `<Video N>`, and `<Audio N>` from that actual map;
4. set `prompt_primary_audio_ordinal` to 0 when the prompt already contains a deliberate multi-audio map, because its remapper substitutes all occurrences of the selected ordinal.

Video and audio categories are independently numbered, consistent with the official Ref2VA grammar.

### Separate Audio Roles

Record each audio path as one of:

- model-fed reference or copy;
- latent initialization;
- model-generated output;
- post-generation mux only.

Only model-fed audio receives `<Audio N>`. A clean `final_audio` or other track used only after generation remains outside the prompt and media-label map.

Choose structured retention meaning from the actual final signal:

| Runtime path | Structured interpretation |
| --- | --- |
| Complete source survives unchanged | `audio reuse` + `fully_copy` |
| Source is cropped, mixed, ducked, layered, or only partly retained | `audio reuse` + `partially_copy` |
| Source guides voice, rhythm, or semantics without proven signal reuse | `audio reference` + `reference` |
| Only broad category or atmosphere remains | `audio reference` + `weak_reference` |
| Native generated audio with no model-fed source | no `<Audio N>` |

Do not infer the final audible path from `lock_source`, `remix_source`, `reference_only`, or `native` alone. The audited implementation can return `final_audio` or `drive_audio` for mux regardless of the generation dropdown, and its mixer can resample, change channels/gain, pad, duck, and peak-limit the signal.

### Padded Render Timing

T8 can embed a short requested scene in a longer aligned render context and trim afterward. Use render-window coordinates in every prompt timestamp:

```text
raw_prompt_timestamp = requested_delivery_timestamp + final_trim_start_seconds
```

Keep crop start, leading/trailing padding, and final delivery duration outside the paste-ready prompt. Inspect both source and runtime-processed audio duration and confirm that copied vocal/music events still land at the written raw timestamps after resampling, truncation, or zero-padding.

### Do Not Promote To Official Behavior

- `Hybrid` is not a sixth canonical H3 mode. Express combined endpoints and references as official Ref2VA with `keyframe completion` when the official workflow supports that combination.
- `lock_source`, `remix_source`, `reference_only`, and `native` are graph controls, not official prompt task types.
- Experimental still-image editing is not an official H3 image-editing contract.
- The repository's approximate 124–362-frame training range, `17n+5` grid, 1920×1088 canvas, 32-pixel multiples, batch-size-one advice, dual-clock sampling, and four-step settings are local runtime claims, not hosted-provider limits.
- T8's tag normalizer does not replace this skill's structural validator.
- Alternative sampler quality is not established by the repository's numerical checks.

The hybrid path depends on private ComfyUI structure and a sentinel behavior in `PackedLayout`; treat it as version-sensitive and re-audit after upstream changes.

## MiniMax-H3-Turbo-LoRA

Source: `https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora`  
Audited revision: `43a74557ac3f6539db8e0f2a959d03feb7a81480`  
Last modified and audited: August 8, 2026  
Card-declared license: Apache-2.0, subject to the upstream-license caveat below

### Prompt Contract Does Not Change

Turbo is a sampling/runtime adapter. Keep the same official H3 mode, asset-role mapping, prompt profile, dialogue, timing, and preservation logic that the non-Turbo workflow would use. Do not shorten, densify, or rewrite the prompt merely because sampling uses fewer steps. Put checkpoint, strength, steps, scheduler, VRAM mode, and sampler outside the paste-ready prompt.

### Audited Author Recommendations

| Situation | Third-party runtime recommendation |
| --- | --- |
| General work | `minimax_h3_turbo_v4_step600_ema.safetensors` |
| Quality-oriented | 6–8 steps, v4-600 EMA |
| Minimum-speed run without heavy motion | 4 steps, v4-600 EMA |
| Heavy/fast motion constrained to 4 steps | older v1 EMA checkpoint around training step 850 may be friendlier |
| LoRA strength | 1.0 by default |
| Blur/ghosting on one clip | cautiously try about 1.05–1.2 |
| Over-sharp grain on one clip | cautiously try about 0.8–0.95 |
| Scheduler | `simple` |
| Custom-node `low_vram` | off by default; on only for memory pressure, with possible softness on quantized bases |

The author describes 4–8 as the useful range and warns that higher counts can introduce over-sharp artifacts. The current v4 preview still lists audio and fast/intense motion as active problem areas. Treat all perceptual comparisons as author claims until reproduced on the user's checkpoint, graph, seed, and media.

The Turbo card says its validated frame range begins around 124 frames, roughly five seconds, and extends to about 15 seconds. This does not change official H3's 4–15-second contract; it means a four-second Turbo result lies outside the adapter's stated validation range. Its 32-pixel canvas and `17k+5` frame guidance are local runtime settings from the supplied ComfyUI/generator paths.

### Proven Compatibility Scope

- The shipped graph uses `MiniMaxH3ImageToVideo` with an FL2VA-family int8 checkpoint, so it directly demonstrates the base T2VA/I2VA/FL2VA node family.
- The standalone script directly targets a BF16 FL2VA base and a text-only prompt. The shipped graph directly names an `int8_convrot` FL2VA model.
- I2VA is supported by the documented ComfyUI path. Last-frame and first-plus-last ports are structurally present but have no demonstrated result in this repository.
- The standalone script does not implement Ref2VA conditioning, and the repository supplies no Ref2VA graph, reference-input test, or explicit validation.
- The model card says the companion custom node supports full, quantized, pruned, and curve variants by adapting time conditioning. That is a third-party node claim, not proof from the standalone script.
- This Turbo repository has no audited example for the separate Ref2VA checkpoint family and no Turbo-specific compatibility proof for the official Diffusers, SGLang, or vLLM integrations. Upstream H3 officially supports those runtimes; that does not prove this third-party adapter works on them. Test the exact adapter, checkpoint, and runtime before promising a Turbo path.

The downloadable workflow is not a safe source of defaults: the audited file selects an older v1 ckpt500 adapter, while its prompt describes five seconds but its node length is 73 frames, about 3.04 seconds before any further handling. Rebuild from the current official workflow and apply the current README recommendations instead of copying that graph verbatim.

The author's “about 5×” claim compares four denoising steps with roughly twenty; it is not an end-to-end benchmark and does not make prompt encoding, model loading, VAE decode, or mux five times faster. The repository provides no quantitative parity evaluation against official H3-Base. Treat Turbo as an experimental latency/quality option, not a generally superior default.

The recommended safetensors audited at this revision is 779,849,816 bytes with LFS SHA-256 `5f3a626cd72c93a8b9318d6760c510bc5092d2ab13aaba1f932c5bab07a416d3`. Prefer final `.safetensors`; do not recommend the large experimental `.bin` files. Pin and review the companion executable node code and ComfyUI revision. The standalone script names ComfyUI commit `14b05228cef127ce529bc0c08660770d4af3e9a8`, while its requirements use lower bounds and are not a locked environment. Also verify filenames: the card mentions a v4 step150 EMA file absent from the audited repository tree.

### Upstream License Caveat

The adapter card declares Apache-2.0, but the official MiniMax H3 materials use the MiniMax H3 Community License Agreement. That agreement purports to cover model materials and documentation, defines Model Derivatives and Outputs broadly, restricts its license to an applicable territory that excludes the United States, European Union, United Kingdom, and Republic of Korea, and imposes license/NOTICE and other conditions on use or distribution.

Do not present the adapter's Apache tag as clearing upstream MiniMax obligations. Before using or distributing the adapter, review the current official H3 license and obtain legal guidance where needed. This skill records the conflict; it does not resolve it.

Where local authorization is unavailable, do not recommend an unauthorized deployment. A hosted MiniMax service/API may have separate terms and availability; verify those terms rather than treating hosted access as automatic clearance. Do not vendor or automatically download Turbo weights as part of a prompt-writing task.
