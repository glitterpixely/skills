# Source Boundaries and Capability Matrix

This file is the canonical owner for provider claims, limits, surface boundaries, locked parameters, role values, and documented task support. [prompt-architecture.md](prompt-architecture.md) owns generation composition, [task-contracts.md](task-contracts.md) owns executable operation templates, and [optimizer-runtime.md](optimizer-runtime.md) owns ambiguity and delivery behavior. If a summary elsewhere differs, use this file for factual capability and parameter questions.

## Contents

- [Authority and provenance](#authority-and-provenance)
- [Surface boundary](#surface-boundary)
- [Documented capability envelope](#documented-capability-envelope)
- [Input limits and stability recommendations](#input-limits-and-stability-recommendations)
- [Locked and unlocked tasks](#locked-and-unlocked-tasks)
- [ModelArk role and trigger rules](#modelark-role-and-trigger-rules)
- [Differences from Seedance 2.0](#differences-from-seedance-20)
- [Claims that remain unsupported](#claims-that-remain-unsupported)

## Authority and provenance

Use this authority order:

1. The user's current generation surface and observed accepted inputs.
2. The current BytePlus ModelArk page at `https://docs.byteplus.com/en/docs/ModelArk/2607689`.
3. The authenticated Lark prompt guide at `https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh`.
4. The provider's linked `sd25-pe` optimizer.
5. This distilled skill.

Recorded source state:

- Lark title: `Dreamina Seedance 2.5 Prompt Guide`.
- The saved authenticated Lark plain-text extraction from 2026-08-02 contains 692 text lines and 8,456 whitespace-delimited words. Its SHA-256 is `9590e5a8bfd161f4e56cf7e980fbfe1bce72e33f39a4d0c49caccd7fedf837b5`. These are properties of that local extraction, not stable page metadata. It contains prompt text, tables, and code-style templates but no embedded image or video asset markers.
- BytePlus title: `Dreamina Seedance 2.5 prompt guide`.
- BytePlus document code: `2607689`; created 2026-08-06; first published 2026-08-07; updated 2026-08-07; checked 2026-08-08 local time.
- The saved BytePlus `MDContent` extraction checked on 2026-08-08 contains 1,110 text lines. Its SHA-256 is `cdce3fc9aa423ffa15c01145e9480749fa86bd1d2d6387a988335bfa3e68c491`. The live document payload referenced 51 images and 22 videos. The line count describes the saved extraction, not a provider-published document metric.
- Provider optimizer: `sd25-pe`, version `0.3.3`, discovered through the registry URL published in the BytePlus page and installed only into an isolated review directory. The reviewed `SKILL.md` SHA-256 is `9c73a93bf49ced5dd2dcbc54cd04ec5e2845fdda1cc7adc79983cc91d88dd84a`.

The BytePlus page recommends the official optimizer with:

```bash
npx --yes skills@latest add \
  "https://arkdocs-en.tos-ap-southeast-1.volces.com/skills/" \
  --skill sd25-pe \
  --yes
```

Its documented invocation is `/sd25-pe + the user's prompt`. This local skill preserves its behavior while using Codex-compatible frontmatter and progressive disclosure.

## Surface boundary

Treat `Seedance 2.5` as the model family, but do not flatten all surfaces into one contract.

- The Lark document describes Dreamina prompt authoring and mentions that configurable parameters are set on the generation page or through an API.
- The BytePlus document adds ModelArk-specific field values such as `content.role`, `ratio=adaptive`, `duration=-1`, and `output_format=mov`.
- A claim about one surface does not establish identical access, defaults, input UI, model ID, price, quota, or endpoint on another surface.
- One embedded re-render tutorial visual shows a legacy `Seedance 2.1` selector. Treat the visible selection workflow as a transferable editing pattern only; it is not evidence that the same selector label, UI, or control exists for Seedance 2.5.
- Check the live surface when a user asks for current access, a selectable model identifier, billing, request schema, or an exact UI limit.
- The documents describe prompt behavior and task planning; they do not guarantee a generated result.

## Documented capability envelope

Seedance 2.5 is documented as supporting:

- one generated video up to 30 seconds;
- up to 50 combined image, video, and audio reference assets;
- text-only generation and multimodal reference-to-video generation;
- native generation in more than 10 languages;
- subject appearance and voice reference;
- motion, expression, camera, creative-effect, and pacing reference from video;
- visual style reference from images or video;
- music, melody, dialogue, voice, tone, timbre, ambience, and sound-effect reference or editing;
- storyboard grids and independent keyframes;
- first-frame and first-and-last-frame generation;
- coarse and fine 3D blockout reference/rendering;
- visual instruction editing and reference-image-guided editing;
- audio adding, removing, replacement, translation, and voice modification;
- forward and backward extension with visual and audio continuity;
- one-click assembly from images and/or video;
- generation of a bridge between two videos for a seamless transition;
- combinations of the preceding capabilities when task semantics remain coherent.

The documented visual-edit inventory includes adding subjects, costumes, camera movements, and special effects; modifying a whole subject or a subject part, style, background, color, lighting, material, motion, or camera position; and removing subjects, subtitles, or watermarks. The editing overview also includes redrawing or restoring part of a frame. The documented audio-edit inventory includes adding, modifying, or removing vocals, music, and sound effects. These examples are an operational inventory, not a guarantee that every complex combination will succeed in one pass; use [task-contracts.md](task-contracts.md#video-editing) to scope one edit precisely.

The creative emphasis is production utility: longer storytelling, richer multimodal control, editing, extension, multilingual work, more realistic lighting/performance/camera behavior, reuse, deliverability, and scalable workflows. The provider describes 2.5 as a systematic production enhancement over 2.0, not a leap of the same magnitude as 2.0 over 1.5.

## Input limits and stability recommendations

Hard request limits:

| Type | Hard limit |
|---|---|
| Images | Up to 30; each no larger than 4K |
| Videos | Up to 10; combined duration at most 30 seconds |
| Audio | Up to 10; combined duration at most 30 seconds |
| Total | Up to 50 image, video, and audio assets combined |

The 30-second capability is per generated video. A request for a longer finished program requires multiple generation calls; segment it using the continuity workflow in [prompt-architecture.md](prompt-architecture.md#programs-longer-than-30-seconds). Do not present multi-call assembly as a single documented model request.

Recommendations for stability, not capability limits:

| Use case | Preferred range | Higher range that may require retries |
|---|---|---|
| Distinct subjects in subject images | 1-8 | 9-12 |
| Distinct subjects in subject audio/video | 1-5 | 6-10 |
| Duration of one subject audio/video reference | 5-10 seconds | Longer clips may reduce stability |
| Reference images for video editing | 1-5 | 6-8 |
| Source video for editing | Under 20 seconds | Longer clips may reduce stability |
| Storyboard panels | 15 or fewer | More may cause stillness or wrong order |

For one to five subjects, single-view and multi-view subject images are supported. For more than five subjects, single-view inputs are usually more stable. If multiple views are required, use separate images per view instead of one collage containing several views.

Use simple line-art or stick-figure storyboards with minimal embedded text. Use simple geometric primitives for coarse blockouts. Use complete, clean geometry for fine blockouts and remove path lines, axes, controllers, camera cones/frustums, and production labels.

## Locked and unlocked tasks

The provider divides tasks by whether an input asset is placed as a strict segment or anchor on the output timeline.

### Locked tasks

| Task | Aspect ratio | Duration | Recommended format | Key condition |
|---|---|---|---|---|
| Video editing | Match input video; set `ratio=adaptive` | Approximately match input; set `duration=-1` | `mov` | Source video is the sole editing master |
| First-frame / first-and-last-frame | Match first image; set `ratio=adaptive` | User-set | Surface-dependent | Use `content.role=first_frame` and optional `last_frame` |
| Extension | Match source video; set `ratio=adaptive` | User-set extension length | `mov` | Continue before or after the source boundary |

Editing may differ from the input by up to about 0.3 seconds because some transition frames are compressed. The event order and content are expected to remain approximately aligned. The BytePlus page states that editing a Seedance 2.5-generated video does not produce that duration difference.

First and last images should have the same aspect ratio. A mismatched last image may be stretched.

The provider warns that extension may produce a slight difference described in English as “volume.” The term is ambiguous in the source, so do not silently reinterpret it as file size, loudness, or some other quantity. Treat it as a general continuity caveat unless the active surface clarifies the intended metric. For best audio-visual continuity, the BytePlus guide specifically recommends `mov` for both the input/source video and the extension output; continuity is also usually better when the source was generated by Seedance 2.5.

### Unlocked tasks

Ordinary reference generation, storyboard reference, and keyframe reference do not inherit a fixed duration or aspect ratio merely because references are present.

- A storyboard grid is a high-level plot, shot-order, and approximate-composition guide. It is not a strict frame contract.
- Independent keyframe images align more strongly with visible states and order, but still do not reproduce every in-between frame exactly.
- Configurable output ratio and duration remain external generation parameters unless a locked first-frame role is used.

## ModelArk role and trigger rules

### Editing

Use `content.role` values appropriate to the asset type, including `reference_image`, `reference_video`, or `reference_audio`. Include an edit verb in the prompt, such as edit, add, insert, remove, delete, modify, replace, or change. State the sole master, target, A-to-B change, time or region, count, and preserved content.

### First and last frames

Preferred strict route:

- assign the first image `content.role=first_frame`;
- assign the optional final image `content.role=last_frame`;
- use `ratio=adaptive`;
- set duration externally.

Semantic alternative:

- keep the images as `reference_image`;
- name one as the first frame and another as the last frame in the prompt;
- understand that the output is similar to, but may not exactly match, those semantic references and does not lock ratio in the same way.

These routes must not be collapsed. `content.role=first_frame` and optional `last_frame` are strict timeline roles and activate the first-image ratio lock. Ordinary `reference_image` assets are semantic guidance even when the prompt calls them first or last frames; they do not activate that strict lock, and the output may only resemble them.

The official optimizer requires strict anchor sentences in prompt-authoring mode:

```text
@Image N is the first frame.
@Image N is the last frame.
```

Do not weaken or merge those declarations when strict anchors are intended.

### Extension

Use reference roles for supporting assets and include an extension verb such as extend forward, extend backward, continue, continue from, or extend the story. State direction explicitly. The source video owns the boundary image; additional references may supplement appearance, prop, voice, or scene attributes but must not override the boundary.

## Differences from Seedance 2.0

The BytePlus document identifies four specific differences:

1. Seedance 2.5 responds to integer-second timestamps; 2.0 responds to shot numbering rather than timestamps.
2. Seedance 2.5 supports multi-view subject images; 2.0 does not recommend them.
3. Seedance 2.5 can use input assets to support any aspect ratio in the inclusive range 0.4 to 2.5; 2.0 is limited to six fixed output ratios.
4. Seedance 2.5 supports `mov` output to improve color, brightness, and audio-visual consistency in editing and extension.

Do not generalize the 0.4-2.5 ratio statement to a task whose aspect ratio is automatically locked to a first frame or source video.

## Claims that remain unsupported

Do not state any of the following as a documented fact unless a newer primary source or live surface confirms it:

- a public model ID or endpoint for Seedance 2.5;
- price, credits, quota, concurrency, latency, or region availability;
- native 4K output generation;
- a universal UI prompt-character limit;
- frame-accurate timestamp adherence;
- pixel-identical edits, transitions, or boundary frames;
- guaranteed lip sync, text rendering, formula accuracy, or reference fidelity;
- guaranteed preservation of every source frame during editing;
- a promise that all 50 references should be used at once;
- parity between Dreamina, BytePlus ModelArk, CapCut, Volcengine, or third-party hosts.

The provider explicitly frames its examples as prompt-writing demonstrations whose results vary with materials, complexity, and generation parameters.
