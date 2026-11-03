---
name: seedance-25
description: "Create, optimize, audit, and repair production-ready Dreamina Seedance 2.5 prompts and workflows from text, scripts, images, videos, and audio. Use for text-to-video, up-to-30-second clips, multi-reference jobs with as many as 50 assets, first/last frames, ordered keyframes, storyboard grids, coarse or fine 3D blockouts, video or audio editing, forward/backward extension, one-click videos, seamless transitions, camera/action/dialogue direction, reference mapping, ModelArk task parameters, or evidence-grounded repair when the user supplies a generated result together with its intended prompt or material contract."
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
- For action mechanics and framing, reference-led kinetic action, continuous-action prompting (including single-reference noncombat chases), dense VFX, bilingual combat tokens (`闪切` vs. `变形`), impact-frame transformations, anatomical strike vectors, single-color VFX locks, velocity modifiers, reciprocal combat, action-driven travel, pseudo-one-take transitions, post-cut frame schedules, the four-mode timing architecture (untimed action-quantity pacing, accordion timestamps, nested one-take sub-beats with 1s hinges, proportional speed-contrast scaling), 2.5D letterbox frame-break pop-out compositing, action-triggered arena swaps (`白闪硬切`), shot-indexed progressive damage ledgers, or a supplied standout prompt whose control patterns should be reused, read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md). These Clip-desk craft heuristics are not first-party limits; continuous action is optional and does not require longer prompts or removal of timestamps.
- For untimed, rule-led prompts, everyday worldbuilding, observational multi-cut vignettes, or a user-supplied style example meant for learning rather than adaptation, read [the rule-led worldbuilding pattern](references/desk-prompt-patterns.md#untimed-rule-led-worldbuilding-vignettes). Keep it distinct from continuous-action choreography and from curiosity-driven vignettes; do not force it onto the preceding task.
- For a curiosity-driven character vignette—an unanswered question, visual cause and effect, and a payoff rather than ordinary routine—read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md#curiosity-driven-character-vignettes).
- For literal state transitions, prop and target ledgers, action-density pacing, or patterns distilled from public Seedance prompt posts, read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md#literal-multi-shot-control). Do not copy third-party prompt text, unsupported limits, or syntax that conflicts with the canonical files.
- For any multi-shot `Shot N` prompt with recurring characters, props, or dialogue, apply [the multi-shot continuity craft](references/desk-prompt-patterns.md#multi-shot-continuity-craft): per-shot prop state, character ID tags, speaker isolation, body separation, screen map and eyelines, cut-on-action endings, scene-scoped rules, the dialogue word budget, and Avoid-list conflicts. These are Clip-desk heuristics, not first-party limits.
- For selfie, vlog, found-footage, or any prompt where a character holds the camera, apply [the diegetic phone-camera comedy pattern](references/desk-prompt-patterns.md#diegetic-phone-camera-comedy): holder and hand per shot, transitions caused by the camera object, one global energy rule, `Continuous`/`Later` scene headers, temperament in the reference header, temporary-look state, and a lens-contact ending.
- For two characters bound from one group image, hands-only extras, wrapper or label text, prop ownership in close inserts, or small gags inside busy shots, read [the result-backed door-to-door notes](references/desk-prompt-patterns.md#result-backed-notes-two-character-door-to-door-comedy). They come from one inspected render (2 fps frames, audio not assessed).
- For reference-plate preparation (solid-white oval face masking on staging/full-body views, 3-in-1 composite character sheets, 5–10% `#FFFFFF` paint-out masks for clean entry plates, 3D graybox interior angle locks) and single-clip `[Cut to]` coverage clusters (master-to-inserts and wide-to-OTS reverses inside one generation), read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md#reference-plate-preparation-and-single-clip-coverage).
- For architecture-backed directing rules distilled from ByteDance Seed research papers (pose-leakage exclusions, denoising-aligned clause order, 0–1s geometry settle, speaking rhythm carriers, VLM state-transition checklists, chronological event order, and sliding-window re-anchoring), read [references/desk-prompt-patterns.md](references/desk-prompt-patterns.md#research-grounded-model-mechanics).
- When revising or auditing this skill, read [references/source-coverage.md](references/source-coverage.md) and run `scripts/validate_coverage.py`.

## Applicability Gate

Before drafting, create a compact execution contract:

- primary operation: generation, editing, or extension;
- active reference materials and the exact role of each;
- hard provider limits and locked parameters;
- surface: Dreamina UI, ModelArk, or another documented runtime;
- observable success check and any known result defect.

Do not widen the operation because a reference looks superficially similar. Reuse a confirmed prompt architecture only for the surface and context where it was observed, and keep its assumptions visible. If a core identity, master video, extension direction, or anchor role is unresolved, stop and ask the one decision that changes the contract.

After generation or repair, classify the outcome before editing the prompt: reference not operationalized, guidance ignored, guidance misapplied, incompatible context, execution/material failure, or missing verification. Change one causal layer at a time, run the linter again, and preserve the evidence that motivated the change.

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

One generated clip is documented up to 30 seconds by default (Standard mode, 4–30 seconds). Dreamina web also exposes a Long Video mode (30–180 seconds) when the user explicitly requests a single long-mode generation above 30 seconds. Otherwise, for a requested program longer than 30 seconds, create a multi-call plan of clips no longer than 30 seconds each. Cut at an observable stable state, carry a boundary ledger for identity, pose, ownership, blocking, camera, light, motion, and audio, and use forward extension for the next clip when continuous adjacency is required. Keep global timing in the plan and convert each prompt to clip-local stages; never imply that a standard 30-second surface can generate the entire longer program in one call.

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

Build the prompt in this order: reference ownership and exclusions -> global identity/prop/world locks -> physical force and effect causality -> staged escalation -> camera path and impact response -> continuity and failure guards. For stylized combat or armor/mecha transformations, apply the bilingual token, flash-cut (`闪切`, never `变形`), anatomical target + directional vector, single-color VFX lock, and kinetic acceleration heuristics from `references/desk-prompt-patterns.md`. If the user's source action is being moved into a new world, explicitly preserve the dramatic beat while naming the material or environmental replacement. Keep the primary operation and the source-bound parameter rules unchanged.

Enforce **high-tempo kinetic defaults** across all action, combat, chase, and physical-comedy prompts unless the user explicitly asks for slow, contemplative pacing:

- **Default to compact Chinese (`Mode 1`, `16–24 untimed shots`) for ALL fast-paced fights, chases, and action sequences:** Even when the user prompts in English, write fast-paced fights, magical chases, hunts, and high-cut action blitzes (`>= 12 shots`) in compact Chinese (with English `@Image N defines only ...; do not use ...` role verbs so reference binding lints cleanly). English prose with 6–8 timed shots (`5s` per shot) renders gentle storybook motion with static cameras, whereas compact Chinese fits 16–24 cuts cleanly and locks directly onto Seedance 2.5's high-velocity sakuga weights (`极速跟拍`, `急摇`, `急推`, `瞬间`, `化作残影`, `两帧黑白冲击帧`, `切于<动作>的一瞬`).
- **Open fast-paced clips *in medias res* (never put a `"settling briefly"` beat in Shot 1 of action/chases):** Reserve the `0–1s` geometry-settle beat strictly for dialogue/lip-sync clips. In action, fights, and chases, writing `"settling briefly before the chase erupts"` causes the model to stand still for the first 3 seconds (`0.0–3.0s`); open Shot 1 directly on the explosive trigger (`开场无停顿直接进入高速追逐/交锋`) and scale up environmental magic (`水龙卷`, `藤蔓鞭`, `花火连爆`) rather than low-energy micro-actions (`taps one leaf`, `tugs a vine`).
- **End fights with a 4-to-5 shot decisive finisher (`破招 -> 破防重击 -> 击飞砸落 -> 胜负落定`), never a stalemate clash freeze:** Unless the user requests a cliffhanger tie, never end Shot $N$ on a mutual face-to-face clash (`拳矛对撞…死死对视` / `lock glares in a stalemate`, `STALEMATE_CLASH_ENDING`), which causes the model to freeze the final second in a generic split-screen tie. Dedicate the final 4–5 shots (~5–6 seconds) to a one-way finishing chain: (1) break through the opponent's ultimate projectile, (2) shatter their last shield and land a clean point-blank strike (`两帧黑白冲击帧`), (3) wide whip-pan tracking the opponent blasted into a landmark, (4) opponent's magic/weapons shattering and extinguishing on the ground, and (5) winner landing in the foreground while the defeated opponent remains visibly downed in the background.
- **Replace passive pursuit (`runs after`, `chases`) with active near-miss catch attempts (`PASSIVE_PURSUIT_RISK`):** In any chase or hunt, never write passive running; every beat must pair upper-body catch mechanics (`lunges low with cupped hands`, `snaps fingers shut an inch behind`, `sweeps both arms`, `yanks a hanging vine`) with a narrow miss whose momentum drives the next obstacle.
- **Lock vertical planes and open-eye facial acting affirmatively:** When a small/agile target climbs vertical trunks or high branches while the pursuer wears a floor-length gown/robe or lacks climbing anatomy, state affirmatively that only the small target climbs while the pursuer stays rooted on the ground floor (`pulls hanging vines or splashes water upward from ground level`), avoiding negative `"never climbs trees"` phrasing that leaks climbing tokens. When an `@Image` reference has closed eyes or a tilted-back serene pose, state the open eye color and active tracking gaze (`wide-open amber eyes actively tracking the target; do not use @Image N's background or static pose`) and keep held props/bubbles to the side of the chest so the face is never occluded.

### 5. Structure the event

For a simple clip, use the minimum sufficient form:

```text
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <observable style or emotional treatment>.
Use <shot size, target subject, camera path, and cuts>.
Audio includes <dialogue, ambience, and sound effects>.
```

For several prescribed events, use consecutive stages or `Shot N` + `[Cut to]` coverage. Give each shot/stage one primary state change and an observable end state. Carry forward identities, clothing, prop ownership, blocking, axis, camera direction, and audio state, and re-state the reference's visual rendering medium across camera-angle cuts. For a requested untimed, rule-led vignette, define moment-selection and continuity rules instead of inventing a staged plot; follow the optional worldbuilding pattern in `references/desk-prompt-patterns.md`.

Choose the **timing mode** that keeps editorial tempo brisk (`1.5–3s` per shot in action/chase/comedy, or untimed `Shot N` with immediate `Cut as <action>` triggers) rather than forcing sluggish `4–6s` blocks onto every clip (`SLUGGISH_UNIFORM_TIMING`; see [the four-mode timing architecture](references/desk-prompt-patterns.md#four-mode-timing-architecture-and-pacing-control)):

1. **Untimed Action-Quantity Pacing (`Shot N` without timestamps — default for fast continuous combat, chases, & sakuga):** Omit per-shot `(0-3s)` brackets, which cause the model to pad single strikes or lunges into floaty slow motion or truncate multi-hit exchanges at arbitrary seconds. State total shot count and approximate duration once (`10–14 shots, about 30 seconds` for a brisk chase, `4 shots, about 30 seconds` for long fluid master exchanges with one mid-shot `快速细节切` / `Quick detail cut`, or `共20–24个镜头，约30秒` in compact Chinese for 1-strike-per-shot blitzes) and let **action quantity + `Cut as <mid-motion trigger>` (`切于<动作>`)** drive the clock before any pose settles.
2. **Accordion Timed Pacing (`Shot N (start-ends)` — best for rhythmic kata, anime OPs, and structured multi-angle comedy/story):** Vary integer-second shot lengths instead of flat `4–6s` blocks (`SLUGGISH_UNIFORM_TIMING`): use **`1s` micro-windows** (`6-7s`, `15-16s`, `24-25s`) for single snap strikes, hand grabs, foot stamps, kiai snap-zooms, or impact bursts; **`2–3s` windows** for full movement phrases, near-miss lunges, 180° turns, or macro prop inserts; and reserve **`4–5s` windows** strictly for spoken dialogue delivery. Cap any final capture, bubble hold, or victory reaction to **at most the final `2–3 seconds` (`27-30s` or `28-30s`)** so the clip never finishes the story early and stalls on a static 10-second hold. To pack 3–4 rapid sub-cuts without fragile sub-second timestamps, group them inside one `3–4s` window (`0-3s: Rapid sequence of three connected angles: 1... 2... 3...`). When one continuous tracking shot spans multiple timed phases (`approach -> brake/charge -> slow-mo release`), start the next timestamp block with `Continue that same tracking shot across the time boundary without a cut; no new run-up or position reset`.
3. **Nested One-Take Sub-Beats (`Shot 1 (0-30s):` + internal windows with `1s` hinges — best for continuous single-camera / selfie takes):** Declare the outer one-take container (`Shot 1 (0-30s): [Front camera of her phone, one continuous take]`), subdivide into consecutive integer-second windows (`0-4s:`, `4-8s:`, ...), and carve out dedicated **`1s` hinge windows** for physical locomotion (`8-9s: One step brings her to the shelf`) or sudden acoustic drops (`24-25s: Every room sound cuts out; one second of total silence`) so transitions are never rushed. For in-shot facial transformations without a cut, use a timed **optical defocus bridge** (`25-28s`: start eye change in sharp focus, then command `autofocus hunts and softens into blur` while the jaw/mouth transforms -> `28-30s`: `focus snaps back` onto the completed face).
4. **Proportional Speed-Contrast & Inertia Scaling (`Slow-Mo vs. Rewind vs. Real-Time` & `Gravity/Pendulum Lag`):** When showing the same action at different speeds, scale shot count and duration proportionally rather than relying on speed adjectives alone (e.g., `9s across 3 shots` in extreme slow motion -> `2s in 1 locked wide shot framed as Shot 1` for rewind -> `4s in 1 panning wide shot` for the full-speed replay). Anchor extreme speed or heavy mass through **gravity/inertia asynchrony** (an object knocked airborne in Beat A is still falling when a speedster/cat re-enters in Beat B; a braking carriage stops while its heavy suspended head keeps swinging into the next window).

`Shot N` is also valid for ordinary shot sequencing when elapsed time is not important. Treat `Shot 45` as an identifier, never as a 45-degree camera angle unless the user explicitly says degrees.

Use integer-second timestamps only when the user supplies them or when Mode 2, Mode 3, or Mode 4 pacing benefits from explicit time windows. Make ranges consecutive and non-overlapping (or cleanly nested inside a `Shot 1 (0-30s)` one-take container). Treat them as pacing budgets, not frame-accurate edit points. Do not use high-frequency instructions such as several actions per second.

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

For **natural dialogue and audio prosody**, enforce these rules on every speaking prompt:

- **Write conversational human lines (when authoring or polishing dialogue):** Use natural speech rhythm, contractions (`it's`, `I'm`, `what's`), `...` for a mid-thought pause, and `—` for an in-shot self-interruption. Avoid cheesy nursery-rhyme couplets or stiff theatrical prose unless explicitly requested.
- **Hit the Prosody Goldilocks Zone:** Pair what the speaker feels with **grounded conversational vocal direction** (`smooth, teasing, conversational voice`, `natural, puzzled tone`, `startled, disbelieving little laugh`, `dry, incredulous, playfully offended voice`, `relaxed, dryly amused tone`) and **anatomically natural micro-expressions** (`slow arch of one eyebrow`, `blinking twice in confusion`, `brows knitting together`, `amused eye roll`, `crooked half-smile`).
  - *Never use unintended prosody flatteners* (`flat tone`, `monotone delivery`, `keep expressions subtle, cool, and deadpan`) on warm or expressive characters—they flatten TTS into a monotone robot and freeze the face. *Exception:* `deadpan` is valid when the character profile or genre intentionally establishes a stone-faced/kuudere or gothic deadpan persona (`flat deadpan face`, `deadpan tour`, `Deadpan: "Family resemblance."`).
  - *Never use cartoon gasp/over-acting triggers* (`inhales excitedly`, `offended gasp`, `sharp yelp`, `sing-song lilt`, `high-pitched voice that cracks`, `eyes snapping wide into circles`, `brows shooting into bangs`, `puffs her cheeks`)—pre-line breath/gasp cues synthesize loud `"HAAAH!"` cartoon gasps and children's-show dubbing, while extreme eye/cheek cues distort semi-realistic faces into bug-eyes and balloon cheeks.
- **Keep each spoken sentence inside one on-camera shot:** Never split a single spoken sentence across a `[Cut to]` boundary (`{"Part one—"}` -> cut to insert -> `{"—part two!"}`), which resets TTS prosody at the seam and creates disembodied voiceover. Keep macro prop inserts short (`2–3s`) and purely visual with a clear `<SFX>` anchor so there are no dead-air gaps.
- **Keep dialogue sparse so TTS does not drift or narrate the visuals (`CLIP_DIALOGUE_OVERLOAD` & `DIALOGUE_DENSITY`):** Keep total clip speech `<= 24 words` and per-shot speech below `2.0 words/sec` (`~1.0–1.5 words/sec` ideal). Default to **2–3 short lines (`3–5 words` each)** in untimed multi-shot clips, or up to **4–5 ultra-short lines (`1–5 words` each, `<= 24 words total`)** in timed sequences where each line has its own `3–4s` window and prop action. Leave remaining beats as silent physical reactions (`keeps lips closed, does a silent double-take`) and crisp `<SFX>`.
- **Pace syllables, set internal speech ceilings, and prevent "statue body":** Keep per-shot speech below `2.0 words/sec` (`3–5 words` in a 4s shot), let reference geometry settle in the opening `0–1s`, unbind static reference poses (`do not use its background or static standing pose`), and add subtle body rhythm carriers (`slight weight shift, natural head tilt, small hand gesture`) while speaking. When a long shot (`5-15s` or `23-30s`) includes both dialogue and a silent reaction tail, state an **internal speech-completion ceiling** (`Finish this exchange by 13s; hold the quiet reaction until 15s`, or `Finish speaking by 28s; hold in silence until 30s`) so speech does not stretch across the silent beat. Use abrupt audio cutoffs (`Drop all sound at 23-24s`) and J/L-cut audio bridges (`Her cheer carries over into Red's shot as audio only, ending on Red's desk thump`) as timing anchors.
- **Isolate speakers and bind `@Audio 1` cleanly:** In multi-speaker shots, state `<Name> alone speaks` and keep listeners' mouths naturally closed. For `@Audio 1` voice-timbre cloning, exclude its background sound and original words while supplying `{Exact written line.}`; for full waveform lip-sync to a pre-acted `.wav` clip, bind `@Audio 1` for vocal timing/inflection and still include `{Exact verbatim transcript}` so plosives (`p/b/m`) lock cleanly.

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
