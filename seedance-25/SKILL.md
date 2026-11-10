---
name: seedance-25
description: "Write, optimize, audit, and repair Dreamina Seedance 2.5 video prompts and BytePlus ModelArk workflows (up to 30s or 180s Long Video, 50 multimodal @Image/@Video/@Audio refs, keyframes, storyboards, 3D blockouts, edit, extend, and result repair). Trigger terms: Seedance 2.5, sd25, sd25-pe, dreamina-seedance-2-5, 即梦 2.5, Jimeng."
---
# Seedance 2.5

Turn the user's intent and available materials into one executable Seedance 2.5 production contract. Preserve the story, bind every active reference, use the correct task semantics, and distinguish creative prompt text from locked generation parameters.

## Source authority

Use claims supported by the supplied first-party documents, BytePlus ModelArk's official specifications, and the linked `sd25-pe` optimizer unless the user supplies a newer primary source:

- Dreamina Seedance 2.5 Prompt Guide: authenticated Lark document (`2026-08-02`).
- Dreamina Seedance 2.5 prompt guide: BytePlus ModelArk document `2607689` (`seedance-2-5-prompt-guide`, including the `2026-11-07` troubleshooting FAQ update).
- BytePlus ModelArk API, pricing, portrait-asset, and badcase specifications (`seedance-2-5`, `create-video-generation-task-api`, `model-pricing`, `seedance-portrait-asset-guide`, `badcase-report-api`, checked `2026-11-10`).
- Official `sd25-pe` optimizer version `0.3.3`.

Read [references/source-boundaries.md](references/source-boundaries.md) before answering capability, limit, availability, API, pricing, or parameter questions. Keep Dreamina UI behavior and BytePlus ModelArk (`dreamina-seedance-2-5-260628`) parameter behavior surface-specific. Do not invent undocumented quotas, UI limits, or unsupported guarantees.

Canonical ownership is deliberate: [references/source-boundaries.md](references/source-boundaries.md) owns capabilities, limits, API specs, and locked parameters; [references/optimizer-runtime.md](references/optimizer-runtime.md) owns mapping, ambiguity, notes, Draft promotion, and result-repair behavior; [references/prompt-architecture.md](references/prompt-architecture.md) owns generation structure, timing, blocking, camera, and audio; [references/task-contracts.md](references/task-contracts.md) owns operation-specific templates. Craft and research modules provide heuristics and mechanistic explanations without altering canonical limits. If a summary conflicts with its canonical owner, follow the canonical owner.

## Route the request

Select exactly one primary operation for each prompt:

1. **Generation**: create a new video from text and optional image, video, or audio references (`omni_reference_task_type="reference"` when assets are attached on ModelArk). Keyframes, storyboards, blockouts, multi-reference work, one-click creation, aspect-ratio outpainting, and seamless transitions are generation modules.
2. **Editing**: modify visual or audio content inside one existing source video (`4–30s`, `omni_reference_task_type="edit"`). Make that source the sole editing master.
3. **Extension**: create new material before or after one source video without rewriting the original segment (`omni_reference_task_type="extend"`).

When editing must happen before extension, return two sequential prompts: edit first, then extend the edited output as the new master. If a new subject appears only after the source ends, use extension alone. Ask one short question only when the operation, extension direction, core identity, or boundary role genuinely has multiple equally plausible answers.

A supplied-result audit is not a fourth generation operation. Require the result plus the intended prompt or reference-role contract, compare observed mismatches with the documented contract, and then repair the appropriate generation, editing, or extension prompt. Do not diagnose an unseen output or present a speculative model failure cause as confirmed.

## Load only the needed references

- For factual limits, task locking, ModelArk fields, pricing, `draft_task`, portrait trust, troubleshooting fixes, triggers, or 2.0 differences, read [references/source-boundaries.md](references/source-boundaries.md).
- For prompt shape, reference binding, stages, timestamps, dialogue, camera, emotion, and audio, read [references/prompt-architecture.md](references/prompt-architecture.md).
- For editing, extension, first/last frames, keyframes, storyboards, blockouts, one-click creation, or transitions, read [references/task-contracts.md](references/task-contracts.md).
- For ambiguous, missing, unreadable, or numerous materials; novels; mapping confidence; Draft-to-1080p workflow; or exact delivery rules, read [references/optimizer-runtime.md](references/optimizer-runtime.md).
- For source-derived patterns, examples, and canonical submit-ready prompt templates, read [references/examples.md](references/examples.md).
- For visual-output evidence, artifacts, and lessons from all 51 images and 22 videos in the BytePlus page, read [references/media-evidence.md](references/media-evidence.md).
- For Clip-desk craft on action mechanics, bilingual combat VFX (`闪切` vs. `变形`), continuous-action prompting, physics origin, fight repair, extension-ready beats, the [four-mode timing architecture](references/desk-prompt-patterns.md#four-mode-timing-architecture-and-pacing-control), or 2.5D letterbox pop-out compositing, read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md).
- For [untimed worldbuilding vignettes](references/desk-continuity-and-coverage.md#untimed-rule-led-worldbuilding-vignettes), [curiosity vignettes](references/desk-continuity-and-coverage.md#curiosity-driven-character-vignettes), [literal multi-shot control](references/desk-continuity-and-coverage.md#literal-multi-shot-control), [multi-shot continuity & conversational prosody](references/desk-continuity-and-coverage.md#multi-shot-continuity-craft), [diegetic phone-camera comedy](references/desk-continuity-and-coverage.md#diegetic-phone-camera-comedy), door-to-door result notes, or [reference-plate preparation and `[Cut to]` coverage](references/desk-continuity-and-coverage.md#reference-plate-preparation-and-single-clip-coverage), read [references/desk-continuity-and-coverage.md](references/desk-continuity-and-coverage.md).
- For research-grounded directing mechanics from ByteDance Seed papers (`MMDiT` spatial self-attention, `Multishot MM-RoPE`, `Tarsier2`, `Phantom`, `HuMo`, `RewardDance`, causal `8n+1` VAE stride, `480p -> 1080p` Refiner, and the `Seedance 2.5` evidence boundary), read [references/research-mechanics.md](references/research-mechanics.md).
- When revising or auditing this skill, read [references/source-coverage.md](references/source-coverage.md) and run `scripts/validate_coverage.py`.

## Applicability Gate

Before drafting, create a compact execution contract:
- primary operation: generation, editing, or extension;
- active reference materials and the exact role of each;
- hard provider limits and locked parameters;
- surface: Dreamina UI, BytePlus ModelArk, or another documented runtime;
- observable success check and any known result defect.

Do not widen the operation because a reference looks superficially similar. If a core identity, master video, extension direction, or anchor role is unresolved, stop and ask the one decision that changes the contract. After generation or repair, classify the outcome before editing the prompt (reference not operationalized, guidance ignored, guidance misapplied, incompatible context, execution/material failure, or missing verification), change one causal layer at a time, and re-run `prompt_lint.py`.

## Core workflow

### 1. Establish the factual and creative contract

Extract and lock: subjects and count; actions, causality, and outcome; scene, time, weather, spatial layout, and 180-degree axis; prop count, ownership, handoffs, and final states; visual medium, camera, cuts, audio, dialogue, subtitles, and exclusions; and primary operation plus any anchor, storyboard, blockout, or transition role. Do not change the user's identities, relationships, count, edit target, extension direction, outcome, reference assignment, or exact dialogue.

### 2. Inspect materials honestly

Inventory every supplied image, video, and audio item without inferring content from filenames. Separate **story assignment** from the user (name, relationship, function, ownership, outcome) from **material observation** (visible/audible appearance, clothing, structure, motion, camera, voice, ambience). Retain user-supplied names and neutral labels (`person`, `subject`); never infer age, gender identity, race, ethnicity, nationality, profession, or personality from appearance, clothing, filename, or upload order. Request access only when an unreadable asset is the sole core identity reference, editing master, or extension source.

### 3. Apply the material preflight

Hard request limits:
- no more than 30 images, each no larger than 4K (`< 6000px`, `<= 30 MB` on ModelArk; downscale AI stills to `<=` output resolution to prevent grass/fur swirl moiré);
- no more than 10 videos totaling at most 30 seconds (`2–30s` each for reference, `4–30s` required for video editing);
- no more than 10 audio clips totaling at most 30 seconds (`2–30s` each);
- no more than 50 image, video, and audio assets combined.

Treat stability ranges as recommendations, never hard limits: 1–8 subjects in images; 1–5 subjects in audio/video with 5–10s per clip; an editing master under 20s with 1–5 reference images; 15 or fewer simple storyboard panels. If a hard limit is exceeded, keep task-critical materials and append one concise `Material Note:`.

One generated clip is documented up to 30 seconds by default (Standard mode, `4–30s`). Dreamina web also exposes Long Video mode (`30–180s`) when explicitly requested. Otherwise, for programs above 30s, build a multi-call plan of `<= 30s` clips cut at observable stable states with a boundary ledger, using `.mov` forward extension when continuous adjacency is required.

### 4. Bind references explicitly

Preserve the user's runtime handles (`@Image 1`, `@Video 1`, `@Audio 1`, or Dreamina CN `@图片1`, `@视频1`, `@音频1`). When preparing multi-subject uploads, order `@Image` files in **chronological order of first on-screen appearance** (`@Image 1` enters first, `@Image 2` enters second) to minimize identity swaps.

For every active material, state: (1) the subject, prop, scene, motion, camera, style, or audio category it controls; (2) the exact attributes to inherit; and (3) any identities, background, static pose, sound, or style not to inherit (`do not use its background or static standing pose`). List every known inactive handle under `[Unused Materials]`. Use a `Material Mapping Note:` only for a consequential medium-confidence mapping or path/upload-order assumption; on low-confidence core ambiguity, ask one consolidated question and stop.

### 4a. Activate reference-led kinetic action when needed

For fights, chases, transformations, or dense VFX, read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md) and build: `reference roles -> global locks -> force/VFX origin -> staged escalation -> camera path -> compact failure guards`.

- **Default to `8–12` sustained shots over 30s (`~2.5–3.75s` per shot in the user's language) for readable fights and chases:** Give each shot one complete `wind-up -> strike or catch lunge -> contact or narrow miss -> recoil/redirection` phrase ending on `Cut as <active motion>`, avoiding sub-2s generator-transition flash clutter. Use **opt-in `Mode 1b` (`16–24` untimed shots in compact Chinese)** only when the user explicitly requests a rapid-fire anime sakuga blitz (`>= 12` cuts) or Chinese combat prompting; `prompt_lint.py` supports native Chinese role bindings (`@Image 1 仅定义…；不要使用…`).
- **Open fast clips *in medias res* (`OPENING_SETTLE_IN_ACTION`):** Never write `"settling briefly before the chase/fight"` in Shot 1; reserve `0–1s` settling strictly for dialogue scenes.
- **End fights with a 4–5 shot one-way finisher (`STALEMATE_CLASH_ENDING`):** Unless a tie is requested, never end on a frozen mutual clash/glare; script `break projectile -> shatter guard & land clean hit -> wide knockdown into landmark -> weapon/magic fades -> winner in foreground, opponent downed in background`.
- **Use active catch mechanics & affirmative plane/eye locks (`PASSIVE_PURSUIT_RISK`):** Pair pursuit with upper-body lunges/grabs and narrow misses; state ground-vs-tree plane separation affirmatively; override closed reference eyes (`wide-open amber eyes actively tracking`) and keep held props off the face centerline.

### 5. Structure the event and timing mode

For simple clips, state `Subject + primary action in environment + visual style + camera path + audio`. For multi-beat clips, use consecutive stages or `Shot N` + `[Cut to]` coverage with one primary state change per beat, re-stating the visual medium across cuts. Select the timing mode from [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md#four-mode-timing-architecture-and-pacing-control):

1. **Untimed Action-Quantity (`Shot N`):** Default for continuous fights and chases (`8–12` readable shots in the user's language, `4` long fluid shots with one `Quick detail cut`, or opt-in `16–24` compact-Chinese sakuga cuts) driven by `Cut as <action>`.
2. **Accordion Timed (`Shot N (start-ends)`):** Alternate `1s` snap impacts, `2–3s` movement phrases, and `4–5s` dialogue beats rather than flat `4–6s` action blocks (`SLUGGISH_UNIFORM_TIMING`), capping final victory/capture holds to the last `2–3s` (`27-30s`).
3. **Nested One-Take (`Shot 1 (0-30s):` + internal windows):** Carve dedicated `1s` hinge windows for steps (`8-9s`) or sudden silence (`24-25s`), and bridge in-shot face changes with timed optical defocus (`25-28s` blur -> `28-30s` snap-back).
4. **Proportional Speed-Contrast & Inertia Scaling:** Scale shot count and duration across slow-mo (`9s / 3 shots`), rewind (`2s / 1 locked wide`), and real-time (`4s / 1 pan`), anchored by gravity/pendulum lag.

Keep timestamps consecutive, integer-second, and non-overlapping; never demand multiple repeated actions per second.

### 6. Apply operation-specific rules

Read [references/task-contracts.md](references/task-contracts.md) and enforce the exact contract for Editing (sole master, target, region/interval, count, A-to-B change, inherited timeline, closed preservation; pre-trim edit masters to `8n + 1` frames at 24 fps when exact duration match is needed), Extension (explicit forward/backward direction, observed boundary, single-instance continuity), First/Last Frames (strict `first_frame`/`last_frame` standalone declarations vs. semantic `reference_image`), Ordered Keyframes, Storyboard Grids (`<= 15` simple panels), Coarse/Fine Blockouts, One-Click Video, or Seamless Transitions.

### 7. Separate parameters from the prompt

Keep total duration, aspect ratio, resolution (`480p`/`720p`/`1080p`; `4K` is unsupported on `Seedance 2.5`), frame rate, `omni_reference_task_type`, `draft_task`, API keys, and endpoints outside the creative prompt. On ModelArk: editing locks `ratio=adaptive` and `duration=-1` (`mov` preferred); strict first/last frame and extension lock `ratio=adaptive` with user-set duration; and Step-2 `draft_task` promotion (`480p -> 1080p`) forbids re-sending prompt, media, `seed`, `duration`, or `ratio`. Append one concise `Parameter Note:` when a requested setting conflicts with a task lock.

### 8. Direct camera, performance, text, and audio observably

Name camera `technique + target + start + path/speed + end + visible result`. Chain `6–10` subtle reaction micro-actions with explicit beat gates (`in this exact order, each step its own beat: first..., then..., only after...`). See [references/desk-continuity-and-coverage.md](references/desk-continuity-and-coverage.md#multi-shot-continuity-craft) for full dialogue craft:

- **Conversational Goldilocks prosody:** Write natural `2–6` word period-terminated clauses with mundane physiological micro-actions *between* clauses (swallow, sniffle, spoon placement, weight shift) and subtext anchor gestures (`turns one hand palm up, as if to say "..."`). Never use unintended prosody flatteners (`flat tone`, `monotone`) on expressive speakers or cartoon gasp/bug-eye triggers (`inhales excitedly`, `sing-song lilt`, `eyes wide into circles`, `puffs cheeks`).
- **Upper-face isolation & eye realism:** Route emotion to the brow and eyes (`All facial expression lives in the brow and the eyes; the mouth is left natural`), enforce chew/swallow gates, add `normal human eyes; no glowing eyes` on realistic humans, isolate speakers (`<Name> alone speaks`), and keep every spoken sentence self-contained inside one on-camera shot (`SPLIT_DIALOGUE_ACROSS_CUT`) with an internal speech ceiling (`Finish speaking by 28s; hold in silence until 30s`) on long shots.
- **Dialogue word budget & 30s single-take choice:** Keep general/action/comedy clips `<= 24` words (`< 2.0` words/sec) and 25–30s slow dialogue dramas `<= 38–43` words across `8–10` short clauses. Above `~40` words in 30s (or `>= 2.0` words/sec), warn of TTS prosody crowding (`CLIP_DIALOGUE_OVERLOAD` / `DIALOGUE_DENSITY`) rather than splitting unilaterally: offer tightening clauses, keeping one 30s take when per-shot pace stays `< 1.8` words/sec, Dreamina 30–180s Long Video, or two generations if preferred. Keep exclusions compact (`<= 80` words, `BLOATED_EXCLUSION_LIST`).

When categorical separation helps, use `()` music, `<>` SFX, `{}` dialogue, and `【】` subtitles (never wrapping character names in `<>`). Whenever speech is present without requested visible captions, include `No subtitles.` (`无字幕`). Honor the standing no-music default unless music is requested.

### 9. Validate and deliver

Run:

```bash
python3 scripts/prompt_lint.py <prompt-file> --mode generation
python3 scripts/prompt_lint.py <prompt-file> --mode edit
python3 scripts/prompt_lint.py <prompt-file> --mode extension
```

Pass `--images`, `--videos`, `--audio`, `--video-seconds`, `--audio-seconds`, `--target-duration`, `--long-video`, or `--allow-music` when applicable. Return one submit-ready prompt body with no outer Markdown heading or code fence, plus at most the one-line notes authorized in [references/optimizer-runtime.md](references/optimizer-runtime.md#output-contract). Never guarantee pixel-identical edits/transitions, frame-accurate timestamps, or exact text rendering.
