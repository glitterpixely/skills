---
name: seedance-25
description: Create, optimize, audit, and repair production-ready Dreamina Seedance 2.5 prompts and workflows from text, scripts, images, videos, and audio. Use for text-to-video, up-to-30-second clips, multi-reference jobs with as many as 50 assets, first/last frames, ordered keyframes, storyboard grids, coarse or fine 3D blockouts, video or audio editing, forward/backward extension, one-click videos, seamless transitions, camera/action/dialogue direction, reference mapping, ModelArk task parameters, or evidence-grounded repair when the user supplies a generated result together with its intended prompt or material contract.
---

# Seedance 2.5

Turn the user's intent and available materials into one executable Seedance 2.5 production contract. Preserve the story, bind every active reference, use the correct task semantics, and distinguish creative prompt text from locked generation parameters.

## Source authority

Use only claims supported by the two supplied first-party documents and their linked official `sd25-pe` optimizer unless the user supplies a newer primary source:

- Dreamina Seedance 2.5 Prompt Guide: the authenticated Lark document supplied by the user, fully captured on 2026-08-02.
- Dreamina Seedance 2.5 prompt guide: BytePlus ModelArk document `2607689`, updated 2026-08-07 and checked on 2026-08-08.
- Official `sd25-pe` optimizer version `0.3.3`, installed from the BytePlus document's provider registry into an isolated review directory.

Read [references/source-boundaries.md](references/source-boundaries.md) before answering capability, limit, availability, API, or parameter questions. Keep Dreamina UI behavior and BytePlus ModelArk parameter behavior surface-specific. Do not invent model IDs, prices, endpoints, quotas, UI limits, or unsupported guarantees.

Canonical ownership is deliberate: [references/source-boundaries.md](references/source-boundaries.md) owns capabilities, limits, and locked parameters; [references/optimizer-runtime.md](references/optimizer-runtime.md) owns mapping, ambiguity, notes, and result-repair behavior; [references/prompt-architecture.md](references/prompt-architecture.md) owns generation structure, timing, blocking, camera, and audio; [references/task-contracts.md](references/task-contracts.md) owns operation-specific templates. Examples and the coverage ledger are illustrative indexes. If a summary conflicts with its canonical owner, follow the canonical owner.

## Route the request

Select exactly one primary operation for each prompt:

1. **Generation**: create a new video from text and optional image, video, or audio references. Keyframes, storyboards, blockouts, multi-reference work, one-click creation, and seamless transitions are generation modules.
2. **Editing**: modify visual or audio content inside one existing source video. Make that source the sole editing master.
3. **Extension**: create new material before or after one source video without rewriting the original segment.

When editing must happen before extension, return two sequential prompts: edit first, then extend the edited output as the new master. If a new subject appears only after the source ends, use extension alone. Ask one short question only when the operation, extension direction, core identity, or boundary role genuinely has multiple equally plausible answers.

A supplied-result audit is not a fourth generation operation. Require the result plus the intended prompt or reference-role contract, compare observed mismatches with the documented contract, and then repair the appropriate generation, editing, or extension prompt. Do not diagnose an unseen output or present a speculative model failure cause as confirmed.

## Load only the needed references

- For factual limits, task locking, ModelArk fields, triggers, or 2.0 differences, read [references/source-boundaries.md](references/source-boundaries.md).
- For prompt shape, reference binding, stages, timestamps, dialogue, camera, emotion, and audio, read [references/prompt-architecture.md](references/prompt-architecture.md).
- For editing, extension, first/last frames, keyframes, storyboards, blockouts, one-click creation, or transitions, read [references/task-contracts.md](references/task-contracts.md).
- For ambiguous, missing, unreadable, or numerous materials; novels; mapping confidence; or exact delivery rules, read [references/optimizer-runtime.md](references/optimizer-runtime.md).
- For source-derived patterns and examples, read [references/examples.md](references/examples.md).
- For visual-output evidence, artifacts, and lessons from all 51 images and 22 videos in the BytePlus page, read [references/media-evidence.md](references/media-evidence.md).
- For reference-led kinetic action, dense VFX, reciprocal combat, action-driven travel, pseudo-one-take transitions, or a supplied standout prompt whose control patterns should be reused, read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md). These Clip-desk craft heuristics are not first-party limits.
- When revising or auditing this skill, read [references/source-coverage.md](references/source-coverage.md) and run `scripts/validate_coverage.py`.

## Core workflow

### 1. Establish the factual and creative contract

Extract and lock:

- subjects and subject count;
- actions, events, causality, and outcome;
- scene, time, weather, spatial relationships, and axis of action;
- prop count, ownership, handoffs, and final states;
- visual style, camera, cuts, audio, dialogue, subtitles, and exclusions;
- primary operation and any anchor-frame, storyboard, blockout, or transition role.

Do not change a user's identities, relationships, character count, edit target, extension direction, story outcome, reference assignment, or exact dialogue. Translate internal thoughts and abstract qualities into observable action, expression, sound, or image changes without adding plot.

### 2. Inspect materials honestly

Inventory every supplied image, video, and audio item. Do not infer content from filenames. For each video, inspect the subjects, action, camera changes, opening state, ending state, and relevant audio. Separate:

- **Story assignment** from the user: name, age, relationship, function, ownership, and outcome.
- **Material observation** from the asset: visible or audible appearance, clothing, structure, color, layout, motion, camera, pace, voice, or ambience.

Never promote a visual guess into a story fact. If an asset is unreadable, say so and continue with confirmed information. Request access only when it is the sole core identity reference, editing master, or extension source.

Keep user-supplied names and neutral labels such as `person` or `subject`. Do not infer age, gender identity, race, ethnicity, nationality, profession, relationship, personality, rank, or other demographic/story facts from appearance, clothing, action, filename, or upload order. Describe only directly observable features needed for visual control.

### 3. Apply the material preflight

Treat these as hard request limits:

- no more than 30 images, each at most 4K;
- no more than 10 videos totaling at most 30 seconds;
- no more than 10 audio clips totaling at most 30 seconds;
- no more than 50 image, video, and audio assets combined.

Treat stability ranges as recommendations, never capability limits: usually 1-8 subjects in images; 1-5 subjects in audio/video with 5-10 seconds per subject clip; an editing master under 20 seconds with 1-5 reference images; no more than 15 simple storyboard panels. Continue when only a recommendation is exceeded. If a hard limit is exceeded, keep user-selected and task-critical materials, then append one concise `Material Note:` identifying what must be reduced.

One generated clip is documented up to 30 seconds. For a requested program longer than 30 seconds, create a multi-call plan of clips no longer than 30 seconds each. Cut at an observable stable state, carry a boundary ledger for identity, pose, ownership, blocking, camera, light, motion, and audio, and use forward extension for the next clip when continuous adjacency is required. Keep global timing in the plan and convert each prompt to clip-local stages; never imply that one request can generate the entire longer program.

### 4. Bind references explicitly

Use the user's existing runtime labels. For Dreamina/ModelArk-style handles, preserve spaces: `@Image 1`, `@Video 1`, `@Audio 1`.

For every active material, state:

1. the subject, prop, scene, action, camera, style, voice, or audio category it controls;
2. the exact attributes to inherit;
3. any identities, background, composition, sound, or style not to inherit.

Map distinct entities one by one. If several views define one subject, label the view supplied by each image and state that only one instance appears. When the complete material list is known, include `[Unused Materials]` inside the prompt and list every inactive number by type so it cannot be reactivated implicitly.

Use a `Material Mapping Note:` only for a consequential medium-confidence mapping or an explicit path/upload-order assumption. If low-confidence ambiguity affects a core identity, count, ownership, direction, sole master, edit target, or anchor role, ask one consolidated question and stop; do not also output a provisional submit-ready prompt.

Do not repeat a reference video's action description when the reference already defines it accurately; name only the dimensions to inherit. The user's written dialogue controls the words unless the user explicitly asks to reuse dialogue from an audio reference.

### 4a. Activate the reference-led kinetic-action mode when needed

Use the optional action mode when the user supplies multiple visual references or a strong example prompt and wants a dense fight, chase, transformation, destruction, or effects-led sequence. Read `references/desk-prompt-patterns.md` and extract its reusable control pattern, not its characters, setting, unsupported parameters, or surface-specific claims.

Build the prompt in this order: reference ownership and exclusions -> global identity/prop/world locks -> physical force and effect causality -> staged escalation -> camera path and impact response -> continuity and failure guards. If the user's source action is being moved into a new world, explicitly preserve the dramatic beat while naming the material or environmental replacement. Keep the primary operation and the source-bound parameter rules unchanged.

### 5. Structure the event

For a simple clip, use the minimum sufficient form:

```text
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <observable style or emotional treatment>.
Use <shot size, target subject, camera path, and cuts>.
Audio includes <dialogue, ambience, and sound effects>.
```

For several events, use consecutive stages. Give each stage one primary state change and an observable end state. Carry forward identities, clothing, prop ownership, blocking, axis, camera direction, and audio state.

`Shot N` is also valid for ordinary shot sequencing when elapsed time is not important. Treat `Shot 45` as an identifier, never as a 45-degree camera angle unless the user explicitly says degrees.

Use integer-second timestamps only when the user supplies them or needs a critical handoff, entrance, exit, transition, or beat. Make ranges consecutive and non-overlapping. Treat them as pacing budgets, not frame-accurate edit points. Do not use high-frequency instructions such as several actions per second.

### 6. Apply operation-specific rules

Read [references/task-contracts.md](references/task-contracts.md), then enforce the applicable contract:

- Editing: one sole master; explicit target, region/category, time scope, count, A-to-B change, inherited timeline, and closed preservation scope.
- Extension: explicit forward/backward direction; actual boundary state; visual, motion, camera, lighting, and audio continuity; one continuous instance per subject.
- First/last frame: for strict ModelArk anchors, assign `content.role=first_frame` and optional `last_frame`, use one exact standalone role sentence per anchor, and match their aspect ratios. For semantic `reference_image` anchors, state the intended opening/ending roles but do not claim the strict ratio lock or exact match.
- Keyframes: ordered independent images, one visible state per image, continuous transitions, no claim of frame-by-frame reproduction.
- Storyboard: reading order, approximate shot structure, excluded line art/text/placeholders, final style and audio; use no more than 15 simple panels when possible.
- Blockout: identify coarse motion skeleton versus fine complete structure; map geometry; keep the described event consistent with the blockout; define unreferenced subjects' observable appearance and key features; state inherited dimensions and excluded production markers.
- One-click: accept multiple images, multiple videos, or both; define material roles, source order, motion amount, editing rhythm, visual treatment, optional text/stickers/transitions, and audio.
- Transition: before clip, after clip, trigger, camera path, visual transformation, arrival state, and audio bridge.

### 7. Separate parameters from the prompt

Do not write total duration, aspect ratio, resolution, frame rate, API keys, endpoints, or run metadata into the creative prompt. Preserve time ranges that are themselves part of the user's event direction.

For BytePlus ModelArk locked tasks:

- editing uses the input video's aspect ratio and approximate duration; use `ratio=adaptive` and `duration=-1` outside the prompt;
- first-frame or first-and-last-frame generation uses the first image's aspect ratio; duration remains user-set;
- extension uses the source video's aspect ratio; extension duration remains user-set;
- prefer `mov` output for editing; for extension, use `mov` for both the input source and output when the surface accepts it and audio-visual continuity matters.

If the user requests a conflicting locked parameter, return the best prompt first and append one concise `Parameter Note:`.

### 8. Direct camera, performance, text, and audio observably

Name the camera's target, start, path, speed change, and end. Expand uncommon terms into visible foreground/background changes. Use two to four observable acting cues for one emotional shift. Bind every supplied spoken line to its speaker, language, optional user-requested accent, delivery, and on/off-screen state. If the user requires a character to speak using a bound audio reference but gives no reliable transcript, preserve that speaking role and direct use of the reference audio without inventing words.

Use natural language by default. When categorical separation helps, use the documented syntax: `()` music, `<>` sound effects, `{}` dialogue, `【】` subtitles. Do not use angle brackets around subject names in the same prompt. Whenever dialogue or speech is present and visible subtitles were not requested, include `No subtitles.` If subtitles are requested, bind their exact supplied text and role. Honor the user's standing preference for no music unless they explicitly request music.

### 9. Validate and deliver

Run:

```bash
python3 scripts/prompt_lint.py <prompt-file> --mode generation
python3 scripts/prompt_lint.py <prompt-file> --mode edit
python3 scripts/prompt_lint.py <prompt-file> --mode extension
```

Add material counts and durations when known. Use `--allow-music` only when the user requested music.

By default, return one best submit-ready prompt body with no analysis wrapper, Markdown heading, or code fence. Retain internal prompt labels when they help execution. Add only the necessary one-line note allowed by [the canonical output contract](references/optimizer-runtime.md#output-contract), including a `Selection Note:` or `Material Mapping Note:` when its stated conditions apply. A low-confidence core ambiguity requires a question and stop, not a provisional prompt plus note.

Never guarantee pixel-identical edits, pixel-identical transitions, frame-accurate timestamps, exact subtitle/formula/sign rendering, exact boundary frames, or perfect adherence. Recommend prepared source material and post-production when literal accuracy is critical.

For a result-repair request, follow the evidence procedure in [references/optimizer-runtime.md](references/optimizer-runtime.md): record only visible/audible mismatches, trace each repair to a documented contract or source-bound media fact, and label uncertain explanations as hypotheses. Return the repaired prompt, not an unsupported claim about the model's internal cause.
