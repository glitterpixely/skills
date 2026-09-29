# MiniMax H3 Model Contract

Use this reference when duration, upload limits, input modes, aspect ratio, resolution, prompt length, supported formats, pricing, or licensing affects the response. Treat all operational limits and prices as a dated snapshot and re-check the live H3 surface when current accuracy matters.

## Contents

- [Source Authority](#source-authority)
- [System Overview](#system-overview)
- [Generation Contract](#generation-contract)
- [Input Modes And Limits](#input-modes-and-limits)
- [Official License Snapshot](#official-license-snapshot)
- [Audited Pricing Snapshot](#audited-pricing-snapshot)
- [Page Coverage Evidence](#page-coverage-evidence)
- [Surface-Sensitive Rules](#surface-sensitive-rules)

## Source Authority

- Official repository: `https://github.com/MiniMax-AI/MiniMax-H3`
- Official model materials and MiniMax H3 Community License: `https://huggingface.co/MiniMaxAI/MiniMax-H3`
- Official repository commit audited for this skill: `d21241f0a4b3acbb34c97dae47fa417b7065e438` (August 15, 2026).
- Product showcase: `https://app.notion.com/p/MiniMax-H3-The-Next-Gen-Open-Weight-Multimodal-Generation-Model-5cdd99c3d331822397f18130e7b480a8`
- Open Platform H3 V2 create contract: `https://platform.minimax.io/docs/api-reference/video-generation-v2-create`
- Current pay-as-you-go pricing: `https://platform.minimax.io/docs/guides/pricing-paygo`
- Visible page revision: August 11, 2026.
- Retrieval and audit date: August 27, 2026.
- The two provider-authored grammar files in this skill are copied byte-for-byte from that repository commit.

The August 11 showcase now defines a hosted three-part prompt formula, but it does not use the structured field names supplied by the official provider skill. Therefore:

- for the Structured profile, use `base-en.txt` and `ref-en.txt` as the authoritative output grammar;
- use the official repository for overlapping core model limits and the showcase only for supplementary surface-specific formats, sizes, pricing, aspect controls, task patterns, and observed behavior;
- do not merge the two into an invented hybrid schema.

## System Overview

H3 is an omni-modal audiovisual generation system accepting combinations of text, images, video, and audio. It generates video with native stereo audio. The official repository describes Context-IR as an intermediate representation, H3-Base as the generator, and Regenerate-2K as the higher-resolution stage.

## Generation Contract

| Dimension | Audited value | Evidence source |
| --- | --- | --- |
| Duration | 4–15 whole seconds on the V2 API | Official repository + V2 API |
| Frame rate | 24 FPS | Official repository |
| Audio | Native 32 kHz stereo | Official repository |
| Prompt length | 7,000 characters maximum | V2 API + showcase |
| Output tiers | 768p and 1440p/2K | Official system overview + showcase |

The official repository lists stable dialogue support for 11 languages: Arabic, Chinese, English, French, German, Italian, Japanese, Korean, Portuguese, Russian, and Spanish, with additional languages supported to varying degrees. The August 11 hosted showcase separately says multilingual prompt input and content generation are supported; it describes reliable TTS coverage across 11 languages, names Chinese, English, Japanese, Korean, French, German, and Spanish as examples, and calls more than 40 additional languages—including Arabic, Thai, Indonesian, and Hindi—exploratory.

These sources use different scopes and place Arabic in different tiers: repository dialogue support versus hosted-surface TTS/localization. Do not collapse them into one guarantee. Preserve the requested dialogue language, do not translate unless asked, and verify the target surface before promising voice quality in an exploratory language.

### Aspect Ratio

- Text-to-Video: 21:9, 16:9, 4:3, 1:1, 3:4, 9:16.
- Omni Reference: the same ratios plus Auto.
- First/Last Frame output follows the uploaded image ratio; the page explicitly gives its image inputs a 5:2 through 2:5 range.
- The current V2 API applies a width/height range of 0.4–2.5 to every image input, including reference images, and to reference videos.
- In the V2 API, Text-to-Video requires a concrete ratio. Image-to-Video always derives its output ratio from the endpoint image and treats any supplied concrete ratio as `adaptive`. Reference-to-Video may use `adaptive` or a concrete supported ratio.

### Resolution

- 768p uses a 768-pixel short edge from 16:9 through 9:16. Wider formats target about 1 megapixel; the page gives 1536×672 for 21:9.
- 768p output can be regenerated to 1440p/2K through H3-Regenerate-2K; this is context-aware regeneration, not a conventional pixel upscaler.
- 1440p/2K uses a 1440-pixel short edge from 16:9 through 9:16. Wider formats target about 3.7 megapixels; the page gives 2976×1248 for 21:9.
- The official open-weight repository releases H3-Base for 768p generation. H3-Regenerate-2K is the provider's context-aware regeneration stage and was not open sourced at the audited commit; the official API exposes 2K generation/regeneration.

Treat aspect ratio and resolution as settings rather than prompt prose unless the user's surface requires otherwise or composition depends on them.

## Input Modes And Limits

### First/Last Frame

- 0, 1, or 2 images.
- Zero images invokes Text-to-Video.
- Image dimensions: 256–5760 pixels.
- Image aspect ratio: 5:2 through 2:5.

### Omni Reference

- Up to 9 images.
- Up to 3 video clips.
- Each video: 2–15 seconds.
- Combined input-video duration: no more than 15 seconds.
- Video dimensions: 256–5760 pixels.
- Video aspect ratio: 5:2 through 2:5.
- Up to 3 audio clips.
- Each audio clip: 2–15 seconds.
- Combined input-audio duration: no more than 15 seconds.
- Audio requires at least one image or video.
- Maximum 12 mixed media files.
- No assets invokes Text-to-Video.

### V2 API Role Boundary

The V2 create endpoint makes Image-to-Video endpoint roles and Reference-to-Video roles mutually exclusive. A request cannot combine `first_frame` or `last_frame` with `reference_image`, `reference_video`, or `reference_audio`.

This transport restriction does not erase the structured Ref2VA task type `keyframe completion`. For a mixed keyframe-plus-reference plan, use a supported Ref2VA/Context-IR workflow and express the keyframe relationship inside that profile; do not send conflicting V2 endpoint roles.

### Formats And File Sizes

| Type | Formats | Per-file limit |
| --- | --- | --- |
| Image | JPG, JPEG, PNG, WEBP, HEIC, HEIF | 30 MB |
| Video | MP4 or MOV container; H.264/AVC or H.265/HEVC video; AAC or MP3 embedded audio | 50 MB |
| Audio | WAV, MP3 | 15 MB |

The V2 API accepts reference-video frame rates from 23.976 through 60 FPS. The audited page and API list a 64 MB request-body limit and recommend public URL media for large API inputs.

## Official License Snapshot

The official repository does not use Apache-2.0. Its MiniMax H3 Community License Agreement, dated August 2, 2026, purports to cover model materials and documentation, defines MiniMax H3 Works, Model Derivatives, and Outputs broadly, and limits granted rights to an applicable territory that excludes the United States, European Union, United Kingdom, and Republic of Korea. It also specifies license/NOTICE, use, distribution, and commercial conditions.

Re-check the current official agreement and obtain legal guidance before using or distributing covered materials, derivatives, or outputs. A third-party LoRA or node license does not by itself clear upstream obligations, and a hosted service may have separate terms rather than providing automatic clearance. This is an audit warning, not legal advice.

## Audited Pricing Snapshot

Do not surface these figures as current without live verification.

| Item | 768p | 2K |
| --- | ---: | ---: |
| Input video | $0.08/second | $0.13/second |
| Output video | $0.08/second | $0.13/second |

- First five input images: free.
- Each additional input image: $0.04.
- Input audio: free.
- Regenerate an existing 768p result to 2K: $0.05/second, with original inputs billed again under the regeneration schedule.
- H3-Context-IR: $0.90 per million input tokens and $3.60 per million output tokens.

The August 11 showcase still listed 768p input video at $0.09/second, while the August 27 Open Platform pricing page lists $0.08/second. Treat the current pricing page as the operational source and preserve this discrepancy as evidence that prices drift.

## Page Coverage Evidence

The August 11 revision contains 58 Prompt/Input/Output showcase demonstrations, 35 marked partial. It adds 14 demonstrations but removes the earlier Rotating Product Page Reveal, for a net increase of 13 over the August 7 snapshot. It also adds a practical hosted prompt guide and two extended style examples. The new lanes are Hand-Drawn 2.0, Motion Graphics & After Effects, AR Creative Videos, Food & Beverage Commercials, Hand-Drawn 2D Game, Interactive Virtual Pet UI, Hardware/Industrial/Embodied AI, and Anime-Inspired Style, plus localization guidance.

The fully rendered current page exposes 81 attachment images, 88 video elements, and 2 audio elements. The earlier exhaustive frame/media audit covered the original 45 demonstrations and its old 64/67/2 inventory only. The 14 August 11 additions were text- and structure-audited for this update but were not included in that earlier frame-by-frame review. Do not represent the old attachment totals as coverage of the current page.

The complete current lesson index is preserved in `showcase-patterns.md`; the hosted formula and pitfalls are in `official-hosted-prompt-guide.md`.

## Surface-Sensitive Rules

- The August 11 hosted user guide explicitly uses upload-order `@Image N`, `@Video N`, and `@Audio N` handles. Use them only on a hosted surface that exposes or documents them; older showcase examples also use plain `Image N` names.
- Keep the user's actual upload filenames or UI handles in a separate upload map.
- Use structured `<Subject N>`, `<Picture N>`, `<Video N>`, and `<Audio N>` labels where the official Ref2VA grammar requires them. Native ComfyUI additionally exposes endpoint `<Picture N>` tags in I2VA, L2VA, and FL2VA as documented in `runtime-surfaces.md`.
- Direct V2 API `role` fields (`first_frame`, `last_frame`, `reference_image`, `reference_video`, `reference_audio`) are transport metadata, not interchangeable prompt handles.
- In native ComfyUI, an explicitly enabled soundtrack from a connected reference video can create an `<Audio N>` label without counting as another uploaded mixed-media file; standalone audio files remain limited separately.
- Re-check the live interface before promising availability, price, complimentary generations, UI control names, or a newly added codec/language/resolution.
