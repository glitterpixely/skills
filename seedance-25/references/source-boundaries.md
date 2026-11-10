# Source Boundaries and Capability Matrix

This file is the canonical owner for provider claims, limits, surface boundaries, ModelArk API parameters, pricing, Draft promotion, portrait trust, official troubleshooting fixes, and documented task support. [prompt-architecture.md](prompt-architecture.md) owns generation composition, [task-contracts.md](task-contracts.md) owns executable operation templates, and [optimizer-runtime.md](optimizer-runtime.md) owns ambiguity and delivery behavior. If a summary elsewhere differs, use this file for factual capability and parameter questions.

## Contents

- [Authority and provenance](#authority-and-provenance)
- [Surface boundary](#surface-boundary)
- [Documented capability envelope](#documented-capability-envelope)
- [Input limits and stability recommendations](#input-limits-and-stability-recommendations)
- [BytePlus ModelArk API, pricing, Draft, & portrait rules (Nov 2026)](#byteplus-modelark-api-pricing-draft--portrait-rules-nov-2026)
- [Locked and unlocked tasks](#locked-and-unlocked-tasks)
- [ModelArk role and trigger rules](#modelark-role-and-trigger-rules)
- [Official Nov 7, 2026 BytePlus troubleshooting fixes & badcase API](#official-nov-7-2026-byteplus-troubleshooting-fixes--badcase-api)
- [Differences from Seedance 2.0](#differences-from-seedance-20)
- [Claims that remain unsupported](#claims-that-remain-unsupported)

## Authority and provenance

Use this authority order:

1. The user's current generation surface and observed accepted inputs.
2. BytePlus ModelArk's official Seedance 2.5 documentation (`https://docs.byteplus.com/en/docs/ModelArk/2607689` / `seedance-2-5-prompt-guide`, `seedance-2-5`, `create-video-generation-task-api`, `model-pricing`, `seedance-portrait-asset-guide`, and `badcase-report-api`, checked `2026-11-10`).
3. The authenticated Lark prompt guide at `https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh` (`2026-08-02`).
4. The provider's linked `sd25-pe` optimizer (`0.3.3`).
5. This distilled skill.

Recorded source state:

- **Lark guide:** `Dreamina Seedance 2.5 Prompt Guide` (`2026-08-02` plain-text capture, SHA-256 `9590e5a8bfd161f4e56cf7e980fbfe1bce72e33f39a4d0c49caccd7fedf837b5`).
- **BytePlus prompt guide (`2607689`):** `Dreamina Seedance 2.5 prompt guide` (initial `2026-08-08` capture with 51 images and 22 videos, SHA-256 `cdce3fc9aa423ffa15c01145e9480749fa86bd1d2d6387a988335bfa3e68c491`; expanded on `2026-11-07` with 10 official FAQ troubleshooting items, checked `2026-11-10`).
- **BytePlus ModelArk API & pricing bundle (`checked 2026-11-10`):** `seedance-2-5`, `create-video-generation-task-api`, `model-pricing`, `seedance-portrait-asset-guide`, and `badcase-report-api`.
- **Provider optimizer:** `sd25-pe`, version `0.3.3` (`npx --yes skills@latest add "https://arkdocs-en.tos-ap-southeast-1.volces.com/skills/" --skill sd25-pe --yes`, invoked as `/sd25-pe + the user's prompt`; reviewed `SKILL.md` SHA-256 `9c73a93bf49ced5dd2dcbc54cd04ec5e2845fdda1cc7adc79983cc91d88dd84a`).

## Surface boundary

Treat `Seedance 2.5` as the model family, without flattening distinct surfaces into one contract:

- **Dreamina web / app (`即梦`)** exposes interactive prompt authoring, Standard `4–30s` generation, and Dreamina web's `30–180s` Long Video mode, with consumer credit billing and `@Image 1` / `@图片1` handles.
- **BytePlus ModelArk** exposes model ID `dreamina-seedance-2-5-260628` at `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks`, with `content.role`, `omni_reference_task_type`, `ratio=adaptive`, `duration=-1`, `output_format=mov`, two-step `draft_task` promotion, and per-million-token billing.
- One embedded re-render tutorial visual shows a legacy `Seedance 2.1` selector; treat it as a transferable workflow illustration only.
- Check the active surface whenever a user asks about Dreamina consumer credit packs, Volcengine CN regional IDs, or third-party wrapper limits.

## Documented capability envelope

Seedance 2.5 is documented as supporting:

- one generated video up to 30 seconds by default (Standard `4–30` seconds; Dreamina web also exposes a Long Video mode for `30–180` seconds when explicitly selected);
- up to 50 combined image, video, and audio reference assets;
- text-only generation, audio-only + text generation, and multimodal reference-to-video generation;
- native generation in more than 10 languages;
- subject appearance, multi-view turnaround, and voice reference;
- motion, expression, camera, creative-effect, and pacing reference from video;
- visual style reference from images or video;
- music, melody, dialogue, voice, tone, timbre, ambience, and sound-effect reference or editing;
- storyboard grids and independent keyframes;
- first-frame and first-and-last-frame generation;
- coarse and fine 3D blockout reference/rendering;
- visual instruction editing and reference-image-guided editing (adding, modifying, removing, or locally restoring subjects, costumes, backgrounds, lighting, camera moves, subtitles, or watermarks);
- audio adding, removing, replacement, translation, and voice modification;
- forward and backward extension with visual and audio continuity;
- one-click assembly from images and/or video;
- generation of a bridge between two videos for a seamless transition.

The provider positions 2.5 as a systematic production upgrade over 2.0 (longer single-clip storytelling, 50-asset capacity, integer timestamps, flexible ratios, and `.mov` delivery).

## Input limits and stability recommendations

Hard request limits:

| Type | Hard limit | ModelArk file & format rules (`2026-11-10`) |
|---|---|---|
| Images | Up to 30; each no larger than 4K | `jpeg`, `png`, `webp`, `bmp`, `tiff`, `gif`; `<= 30 MB` each; width & height `< 6000 px`; aspect ratio `[0.4, 2.5]` |
| Videos | Up to 10; combined duration at most 30 seconds | `mp4`, `mov`; **`2–30s` each for reference, `4–30s` required for video editing**; `<= 200 MB` each; pixels `[407696, 8295044]`; `24–60 fps` |
| Audio | Up to 10; combined duration at most 30 seconds | `wav`, `mp3`; `2–30s` each; `<= 15 MB` each (can be submitted with text alone on `2.5`, unlike `2.0`) |
| Total | Up to 50 image, video, and audio assets combined | Total HTTP JSON request body `<= 64 MB` (use BytePlus TOS URLs rather than Base64 for large batches) |

Stability recommendations (not hard capability caps):

| Use case | Preferred range | Higher range that may require retries |
|---|---|---|
| Distinct subjects in subject images | 1-8 | 9-12 |
| Distinct subjects in subject audio/video | 1-5 | 6-10 |
| Duration of one subject audio/video reference | 5-10 seconds | Longer clips may reduce stability |
| Reference images for video editing | 1-5 | 6-8 |
| Source video for editing | Under 20 seconds (`4-20s`) | `20-30s` may reduce stability |
| Storyboard panels | 15 or fewer | More may cause stillness or wrong order |

For 1–5 subjects, single-view and multi-view sheets are supported; for 6+ subjects, single-view plates are more stable. Keep blockouts free of path lines, axes, rig controllers, and camera frustums.

## BytePlus ModelArk API, pricing, Draft, & portrait rules (Nov 2026)

- **Model ID & Endpoint:** `"model": "dreamina-seedance-2-5-260628"` at `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks` (`seedance-1-5-pro-251215` retires `2026-11-11`).
- **Output Resolution, Codec, & Mono Audio:** Supports `480p`, `720p` (default), and `1080p` (**10-bit H.265/HEVC** at `1080p`; play in QuickTime, mpv, or VLC). **`4K` output is unsupported on `Seedance 2.5`** (`4K` exists on `Seedance 2.0` only; passing `4K` to `2.5` returns an error). All ModelArk generated videos with audio output **mono** audio regardless of input channel count. Returned API `duration` floors `frames / 24` (`133` frames at `24 fps` = `5.54s` -> returns `5`).
- **Explicit Task Router (`omni_reference_task_type`):** Accepts `"auto"` (default), `"reference"`, `"edit"`, or `"extend"`. Setting `"reference"`, `"edit"`, or `"extend"` explicitly validates parameter constraints synchronously at submission instead of failing mid-queue with `InvalidParameter.TaskTypeConstraint` or `InvalidParameter.TaskTypeMismatch`.
- **Online Token Pricing (`model-pricing`):** Token usage = `(input_video_duration + output_video_duration) * width * height * 24 / 1024`.
  - *Without video input:* **\$10.70 / M tokens** (`480p` / `720p`) and **\$11.70 / M tokens** (`1080p`).
  - *With video input:* **\$6.40 / M tokens** (`480p` / `720p`) and **\$7.00 / M tokens** (`1080p`).
- **Two-Step `draft_task` Promotion (`480p -> 1080p`):**
  1. *Step 1 (`480p` Draft):* Submit `"draft": true, "resolution": "480p"`. On `Seedance 2.5`, Draft uses the standard `480p` token rate (no extra Draft conversion multiplier, ~`5.5x` fewer tokens than `1080p` due to pixel count). Draft IDs created on/after `2026-10-28` remain valid for **14 days**.
  2. *Step 2 (`1080p` Final):* Submit `"model": "dreamina-seedance-2-5-260628"`, `"resolution": "1080p"`, `"draft": false`, and `"content": [{"type": "draft_task", "draft_task": {"id": "<DRAFT_TASK_ID>"}}]` (plus optional `output_format`, `watermark`, `callback_url`). **Do not re-send** `content.text`, `content.*_url`, `duration`, `ratio`, `seed`, `generate_audio`, or `omni_reference_task_type` in Step 2 — passing any of them throws an API error even when values match Step 1. Step 1 and Step 2 bill independently without double-counting the Draft video as input duration.
- **Real-Human Face Ban, 30-Day Virtual Portrait Trust, & 24-Hour URL Expiry (`seedance-portrait-asset-guide`):**
  - `Seedance 2.5` and `2.0` block direct uploads of reference images or videos containing real human faces.
  - Unedited, uncompressed virtual-portrait assets generated under the **same BytePlus account** (`Seedance 2.5`, `Seedance 2.0`, `Seedream 5.0`) are automatically trusted for **30 days**. Any cropping, watermarking, format conversion, or `ffmpeg` re-compression invalidates the trust signature.
  - Generated media URLs expire after **24 hours**; archive approved files directly to BytePlus TOS without re-encoding.

## Locked and unlocked tasks

### Locked tasks

| Task | Aspect ratio | Duration | Recommended format | Key condition |
|---|---|---|---|---|
| Video editing (`omni_reference_task_type="edit"`) | Match input video; set `ratio=adaptive` | Match input; set `duration=-1` | `mov` | Source video (`4–30s`) is the sole editing master |
| First-frame / first-and-last-frame | Match first image; set `ratio=adaptive` | User-set (`4–30s`) | Surface-dependent | Use `content.role=first_frame` and optional `last_frame` |
| Extension (`omni_reference_task_type="extend"`) | Match source video; set `ratio=adaptive` | User-set extension length (`4–30s`) | `mov` | Continue before or after the source boundary |

Editing a non-aligned clip may differ from the input by up to about 0.3 seconds (`~0.33s` / 8 frames at 24 fps) unless the source was generated by Seedance 2.5 or pre-trimmed to **`8n + 1` frames** (see troubleshooting item 1 below). First and last images must share the same aspect ratio to avoid stretching. Extension carries a provider continuity caveat (translated as "volume" in early English docs); use `mov` for both source and output when audio-visual continuity matters.

### Unlocked tasks

Ordinary reference generation (`omni_reference_task_type="reference"`), storyboard grids, and ordered `reference_image` keyframes leave `ratio` and `duration` user-configurable unless combined with a strict `first_frame` role.

## ModelArk role and trigger rules

- **Editing:** Use `reference_video` / `reference_image` / `reference_audio`, set `omni_reference_task_type="edit"`, `ratio=adaptive`, `duration=-1`, and include an edit verb (`Edit @Video 1`, `编辑 @Video 1`, `sole editing master`).
- **First and last frames:**
  - *Strict route:* `content.role=first_frame` and optional `last_frame` + `ratio=adaptive` + standalone prompt lines:
    ```text
    @Image 1 is the first frame.
    @Image N is the last frame.
    ```
  - *Semantic route:* keep `content.role=reference_image` and describe opening/ending states semantically without claiming a strict ratio lock or frame match.
- **Extension:** Use `reference_video` (+ optional supporting refs), set `omni_reference_task_type="extend"`, `ratio=adaptive`, `output_format="mov"`, and include an explicit directional extension verb (`Extend @Video 1 forward`, `Extend @Video 1 backward`).

## Official Nov 7, 2026 BytePlus troubleshooting fixes & badcase API

| # | Symptom / Error | Official BytePlus Fix (`2607689` Nov 7, 2026 FAQ) |
|---|---|---|
| **1** | Edited output is `~0.33s` shorter than input | Adjust input video frame count to **`8n + 1` frames** (`n >= 1`, e.g. `161` frames = `6s 17f` @ 24 fps) so output duration matches input, or route via `reference` mode with explicit `duration`. |
| **2** | HTTP 400 `invalid image: heic: decode failed` on `.jpg` | Caused by non-standard asymmetric JPEG chroma subsampling (`Y 2x2, Cb 1x1, Cr 2x1`). Re-encode to standard 4:2:0 via `ffmpeg -i input.jpg -pix_fmt yuvj420p fixed.jpg` or convert to `.png`. |
| **3** | Multi-subject identity swap / confusion | Upload `@Image` references in **strict chronological order of first on-screen appearance** (`@Image 1` enters first, `@Image 2` enters second). |
| **4** | Unrequested burned-in subtitles appear | Use subtitle-free reference videos, format lines as `Speaker's line (tone): "..."` or `{...}`, and state `No subtitles.` |
| **5** | Garbled English signage, logos, or titles | Spell short words letter-by-letter (`"D", "I", "H", "E", "T", "A", "O"`) AND supply a clean `@Image` text/logo reference plate. |
| **6** | Swirling fingerprint moiré in grass, leaves, or fur | Downscale AI-generated reference stills so pixel dimensions are **`<=` the target video output resolution** (`1920x1080` for `1080p`). |
| **7** | Unnatural glowing / over-bright human eyes | Include the literal phrase **`normal human eyes; no glowing eyes`** in the character description. |
| **8** | `Seedance 2.5` shifts visual style away from `Seedance 2.0` | Generate a short anchor clip in `Seedance 2.0`, export as `.mov`, and **extend forward in `Seedance 2.5` with `output_format="mov"`**. |
| **9** | Aspect-ratio outpainting (`9:16 -> 16:9`) or timed dubbing fails in `edit` | Route through **`reference` mode (`omni_reference_task_type="reference"`)** with a `[Visual timeline]` matching `@Video 1` rather than locked `edit` mode. |
| **10** | Unwanted BGM or strange ripple / whistling artifacts | Enumerate music negatives at **both start and end** (`no music, no BGM, no score, no soundtrack; room tone and foley only`), and remove metaphorical `water`, `waves`, or `echoes` from non-water prompts. |

**Diagnostic Badcase Reporting (`CasePlatformV1BadcaseReport`):** Submit persistent generation defects (`<= 50` task IDs per call, `<= 1024` chars description) within **72 hours** of task creation via `POST https://open.byteplusapi.com/?Action=CasePlatformV1BadcaseReport&Version=2024-01-01` (requires ModelArk Data Diagnostic opt-in). *Doc caveat:* `badcase-report-api` line 85 retains a legacy note mentioning `Seedance 2.0` only, whereas line 177's `BadcaseType` model table explicitly lists `dreamina-seedance-2-5-260628` (`video_artifact_flicker`, `character_id_drift`, `visual_text_distortion`, `physics_anatomy_error`, `audio_quality_sync_issue`, `visual_instruction_miss`, `video_edit_extend_error`).

## Differences from Seedance 2.0

1. Seedance 2.5 responds to integer-second timestamps (`2.0` responds to shot numbering rather than timestamps) and doubles Standard single-clip duration from `15s` to `30s`.
2. Seedance 2.5 supports multi-view subject turnaround sheets and expands asset caps from `9+3+3` (`15s`) to `30+10+10 = 50` (`30s`).
3. Seedance 2.5 supports any input-driven aspect ratio in the inclusive range `0.4` to `2.5` (`2.0` uses six fixed output ratios) and allows audio-only + text requests.
4. Seedance 2.5 adds `mov` output for editing/extension continuity, while `4K` resolution remains exclusive to `Seedance 2.0` (`2.5` caps at `1080p` 10-bit HEVC).

Do not generalize the `0.4` to `2.5` ratio range to tasks locked to a first frame or source video.

## Claims that remain unsupported

Do not state any of the following as a documented fact unless a newer primary source or live surface confirms it:

- native `4K` output generation on `Seedance 2.5` (`1080p` is the documented ModelArk ceiling);
- standalone published `Seedance 2.5` parameter counts or internal architecture weights;
- universal Dreamina consumer credit prices, UI character caps, or account concurrency quotas across regions;
- frame-accurate timestamp adherence;
- pixel-identical edits, transitions, or boundary frames;
- guaranteed lip sync, text rendering, formula accuracy, or reference fidelity;
- guaranteed preservation of every source frame during editing;
- parity between Dreamina, BytePlus ModelArk, CapCut, Volcengine, or third-party hosts.
