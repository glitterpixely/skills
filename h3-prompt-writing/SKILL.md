---
name: h3-prompt-writing
description: Plan, inspect, write, and validate surface-aware MiniMax H3 audiovisual prompts for T2VA, I2VA, FL2VA, L2VA, and Ref2VA. Use for hosted/API, open-weight SGLang/vLLM/Diffusers, or native ComfyUI prompting; text-to-video; first/last-frame animation; multi-image storyboards; character or style references; dense motion design; game UI; motion/camera/voice transfer; continuation; compositing; relighting; object/dialogue replacement; precise video editing; native audio; visible text; timed UI states; and compatible community runtime extensions.
---

# H3 Prompt Writing

Turn an idea plus any supplied media into one paste-ready MiniMax H3 prompt for the user's actual surface. Inspect first, select the canonical mode from each asset's real role, choose the correct official prompt profile, budget an observable audiovisual timeline, and lint before delivery.

## Authority And Precedence

Use this order when instructions appear to conflict:

1. Preserve the user's literal dialogue, lyrics, visible copy, required actions, and explicit preservation constraints.
2. Ground all claims about supplied media in direct inspection; never invent unseen features.
3. Follow the official model contract and exact structured grammar in `references/base-en.txt` and `references/ref-en.txt` when that profile applies.
4. Follow official target-surface behavior in `references/runtime-surfaces.md` when it differs only in serialization or runtime settings.
5. Treat a user-confirmed successful prompt or output as surface-specific capability evidence. Preserve its working architecture unless it conflicts with a higher authority or the user asks to change it.
6. Use `references/showcase-patterns.md` and `references/proven-dense-motion-design.md` for content-planning lessons, not as replacement schemas. Translate duration, ratio, and media-handle syntax to the selected H3 surface. The official hosted guide uses `@Image N`, `@Video N`, and `@Audio N`; those handles belong to that hosted profile, not to structured or native-ComfyUI prompts.
7. Treat `references/community-runtime-extensions.md` as optional, pinned, third-party runtime guidance. It never overrides official modes, grammar, or limits.

The August 11, 2026 H3 showcase, its official hosted user guide, and MiniMax's native-ComfyUI templates use freeform natural-language examples. The provider's official H3 skill supplies the structured Context-IR-style grammar. These are separate official surfaces, not competing model contracts. Preserve the structured grammar exactly when selected; use the hosted or raw-freeform profile only for a surface documented to accept it.

## Applicability Gate

Before following any reference profile, write a small execution contract:

- **surface**: structured provider, native ComfyUI, or hosted freeform;
- **mode**: T2VA, I2VA, FL2VA, L2VA, or Ref2VA;
- **asset roles**: endpoint, reusable subject, edit/continuation source, or audio reference;
- **hard constraints**: media counts, durations, crop/frame rules, and literal copy;
- **oracle**: what the rendered result must visibly or audibly prove.

If a prior prompt or result is available, preserve its confirmed architecture and record the observed mismatch before changing it. A successful pattern is evidence for its tested surface and context, not a license to remove its assumptions. If a missing surface or core asset role would materially change the mode or serialization and cannot be safely inferred, ask only that decision before drafting. Otherwise use the explicit default below and state the assumption outside the prompt.

During execution, re-check assumptions at each asset binding, timeline handoff, and final verification. If a result fails, classify the failure before rewriting: wrong surface/profile, reference not operationalized, guidance misapplied, incompatible context, execution/environment failure, or missing verification. Change one causal layer and re-lint.

## Workflow

### 1. Establish The Deliverable

Extract the requested output, target H3 surface, duration, aspect ratio, resolution, language, dialogue, music, reference assets, edit targets, and locked elements. Classify the surface before drafting:

- structured provider skill / Context-IR-assisted API or direct open-weight H3-Base workflow such as SGLang, vLLM, or Diffusers;
- native ComfyUI raw prompt (`MiniMaxH3ImageToVideo` or `MiniMaxH3ReferenceToVideo`);
- hosted Hailuo/Hub-style freeform surface;
- optional community ComfyUI extension layered over an official mode.

After choosing the surface:

- Choose the production topology: **single generation** for one coherent timeline, or **staged multi-clip assembly** when distinct stages need separate approval stills, generations, retained edit ranges, and final stitching. For staged work, read Pattern D in `references/candidate-motion-design-patterns.md`; do not describe the assembly as one H3 generation.
- Within a single-generation topology, default to one final H3 prompt, not several alternatives.
- When the user supplies a prompt or result known to work, record the successful surface, hierarchy, timeline architecture, reference strategy, and literal-copy behavior before proposing changes. Do not replace observed capability with generic caution.
- Keep upload mapping, settings, assumptions, and warnings outside the paste-ready prompt.
- Do not embed aspect ratio, resolution, or other UI settings in the prompt unless the user requests them there or they materially affect composition.
- If duration is missing, choose the shortest whole-second duration from 4–15 seconds that can show every required beat. For the audited Turbo LoRA, default to at least 5 seconds because its stated validation begins around 124 frames; warn when an explicit four-second Turbo request falls outside that adapter-tested range. State the assumption outside the prompt.
- Do not claim a feature or limit is current without checking `references/model-contract.md` and, when stakes warrant it, the live provider surface.
- For local-weight use, derivatives, distribution, commercial terms, or licensing questions, read the official-license snapshot in `references/model-contract.md` and re-check the current agreement; do not treat a community component's license as upstream clearance.
- If the surface is unknown, default to the official structured profile and state that assumption outside the prompt.

### 2. Audit Every Supplied Asset

Read `references/media-inspection.md` whenever the task includes any image, video, or audio. Build an inventory before writing:

| Asset | Observed content | Intended role | Preserve | Change | Literal text/audio | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

Inspect original-resolution stills, video endpoints and shot changes, action phases, visible text, audio events, voices, and synchronization. If a required asset is missing, inaccessible, corrupted, or too ambiguous to inspect, say so and request it; never silently substitute guessed details.

### 3. Select One Mode

Select by asset role, not merely by asset count:

| Mode | Select when |
| --- | --- |
| T2VA | Text alone defines the complete audiovisual timeline. |
| I2VA | One image is the literal first frame at 0.00 seconds and there are no other reference roles. |
| FL2VA | Two images are the literal first and last frames and there are no other reference roles. |
| L2VA | One image is the literal final frame and there are no other reference roles. |
| Ref2VA | Any asset supplies identity, environment, product, wardrobe, style, storyboard, motion, camera, voice, audio, edit source, continuation source, or another reusable role; or multiple role types are combined. |

Prefer Ref2VA when a picture is a character/style reference rather than a concrete endpoint, when a video is edited or continued, when an input audio asset supplies a copy/reference role, or when keyframe completion is combined with other references. Ordinary text-defined dialogue, sound effects, ambience, or music do not by themselves require Ref2VA. In Ref2VA, a concrete endpoint remains a `<Picture N>` and the summary includes `keyframe completion`.

Apply the official Ref2VA input gate before drafting: no more than 9 images, 3 videos, 3 standalone audio clips, or 12 mixed files; each video/audio is 2–15 seconds; combined video and standalone-audio durations are each no more than 15 seconds; audio cannot be the sole media input. An enabled reference-video soundtrack can additionally create an `<Audio N>` label without becoming a separate mixed file. Community graphs do not relax these provider limits.

Narrow exception: when the user explicitly targets the audited `ComfyUI-H3-Motion-Context` plugin, its carried frames/latent/audio are transport state rather than reference assets. Classify each chained segment as T2VA and follow its compatibility and trim rules in `references/community-runtime-extensions.md`.

### 4. Load The Governing Grammar And Surface Profile

- For a structured T2VA, I2VA, FL2VA, or L2VA prompt, read all of `references/base-en.txt`.
- For a structured Ref2VA prompt, read all of both `references/base-en.txt` and `references/ref-en.txt`. The full-reference guide deliberately delegates its camera, speaker, dialogue, cut, and visible-text rules to the base guide.
- For native ComfyUI, read `references/runtime-surfaces.md`. Use the official freeform prompt profile; Ref2VA still requires exact connected-media tags, while Context-IR section headings and `<Subject N>` serialization are not required by the raw node.
- For MiniMax Design, Hailuo, or another hosted surface that follows the August 11 guide, read `references/official-hosted-prompt-guide.md`. Use its three-part planning formula and its upload-order `@Image N`, `@Video N`, and `@Audio N` handles only when that surface exposes them.
- For a dense character trailer, title sequence, motion-design reel, game-interface flow, or a clip whose plot is a material transformation (line art becoming a scene, stitches becoming motion, paint leaking from a prop, type becoming matter), also read `references/proven-dense-motion-design.md`. Use its empirical planning patterns only on a compatible freeform surface or translate them into the selected official structured grammar.
- For cursor-, hand-, tool-, or machine-driven construction, an exact count of pose/state locks, BPM-synchronized choreography, or a complex one-take camera route, read the matching sections of `references/edge-case-playbook.md`. These are planning safeguards for untested concepts, not provider grammar or proof of model capability.
- For motion graphics, kinetic typography, brand films, or product transformations, read `references/motion-design-fundamentals.md` before drafting. Apply its state, motion, timing, typography, camera, and audio checks within the governing surface profile.
- For experimental flat-graphic systems, product-to-type transformations, multi-reference ensembles, or staged clip assembly, also read `references/candidate-motion-design-patterns.md`. Keep prompt-only examples and screenshot observations distinct from inspected render evidence.
- For an explicitly requested or surface-confirmed JSON-shaped creative brief, read `references/hosted-creative-director-json.md`. This optional organization format never replaces the official hosted guide, structured grammar, or actual media-handle syntax.
- For a named community extension, also read only its section in `references/community-runtime-extensions.md`. Keep its graph controls and caveats outside the prompt.
- Do not normalize the three keyframe alignment templates. Their angle brackets and square brackets intentionally differ.
- Scope dialogue punctuation rules correctly: preserve user-supplied dialogue punctuation verbatim in base modes; only Ref2VA dialogue or lyrics transcribed or reperformed from source audio use the normalization rule in `ref-en.txt`.

### 5. Map Reference Roles

For structured Ref2VA, assign labels only after inspection:

- `<Subject N>`: reusable visible content such as a person, object, product, environment, wardrobe, interface, action, style, or effect.
- `<Picture N>`: a concrete first, key, edited, last, composition, or storyboard frame.
- `<Video N>`: a directly edited/continued source or a whole-video temporal structure.
- `<Audio N>`: a copied or referenced audio signal.

Number each category independently and keep each meaning stable. One asset may yield several subjects; several assets may define one subject. A source-only picture or video cited inside a subject definition does not require a standalone definition or retention row unless it is separately used later. An ordinary video with sound does not automatically create `<Audio N>`.

For native-ComfyUI Ref2VA, wire the graph first. Picture and Video ordinals follow their node-slot order. Audio uses a fixed provider order rather than one global wiring order: enabled reference-video soundtracks in video-slot order first, then standalone audios. Give every connected asset one explicit job and do not emit `<Subject N>` as a raw media handle. For the T8 audio extension, use its emitted `media_map_json` after wiring because it inserts `drive_audio` when enabled and can therefore change the final audio ordinals.

For native-ComfyUI endpoint modes, connected keyframes are also presented as picture tags: I2VA uses `<Picture 1>` for the first frame, L2VA uses `<Picture 1>` for the last frame, and FL2VA uses `<Picture 1>` then `<Picture 2>` in first/last connection order. Video, Audio, and Subject tags remain invalid in those base modes.

Only model-fed audio receives `<Audio N>`. Keep latent initialization, generated output audio, and a clean track used only for post-generation muxing distinct in the asset inventory. Choose `fully_copy`, `partially_copy`, `reference`, or `weak_reference` from the final audible signal path, not from a community node's dropdown label.

- Do not assume UI handle syntax. Mirror the user's asset names in the upload map, then use the selected surface's native labels: structured Context-IR labels, native-ComfyUI angle-bracket media tags, hosted `@Image N` / `@Video N` / `@Audio N` handles, or explicit API `role` metadata. Never carry one profile's labels into another.
- A storyboard or shot-order sheet is Ref2VA shot guidance, not automatically a first frame. Bind identity on a separate character or style reference.

### 6. Build A Feasible Timeline

Convert the request into visible and audible state changes that fit the duration. For motion-design work, first apply the compiler in `references/motion-design-fundamentals.md`: lock the visual rules, inventory before/during/after states, assign primary/secondary/accent motion, describe anticipation/travel/impact/settle/hold, name the transition operator, protect readable typography, separate camera from graphic motion, and map visual events to sound.

For a continuous mechanism-driven piece, define the governing interaction as **condition -> local mapping -> boundary behavior -> synchronization rule**. Bind motion-only references without importing their identity, clothing, scene, or rendering style. Treat exact masking, per-pixel inversion, frame timing, and zero-lag coupling as priorities requiring measurement or deterministic post-production, not guaranteed model behavior.

- Use an opening anchor, action onset, intermediate causal states, payoff, and final hold when relevant.
- For the official hosted profile, establish one core-concept sentence, then write chronological shot or time-range blocks. Each block names what is visible, camera/framing, performance, dialogue, physical sound, and any referenced asset. Read `references/official-hosted-prompt-guide.md` for the full formula.
- Make every edit causal: name the source state, transition, target state, and what remains unchanged.
- Distinguish shots from phases: increment `[Shot N]` only at an actual cut in the structured profile. Keep continuous transformations inside one shot; hosted freeform may use phases or beats.
- Name the transformation operator and forbidden substitutes: continuous contour morph, hard material cut, wipe, mask, split, stack, or replacement. Track consumed source objects, inherited attributes, and what must be absent in the final state.
- Distinguish a clean hero hold, where everything freezes for legibility, from a living lockup hold, where the layout stays fixed while one bounded detail continues.
- Inventory exact visible strings, language, script direction, hierarchy, entry, readable hold, and exit. Preserve grapheme integrity and map each referenced subject feature to an inspected source.
- Treat a declared exact count as a contract. Define whether the counted unit is an instantaneous event or a held state, label each occurrence once, distinguish transitions from counted events, and do not introduce extra unnumbered occurrences anywhere in the chronology or ending.
- For procedural creation, write each change as actuator, visible input, tool-consistent effect, and retained result. Direct marks follow the active tool path; fills, undo, toggles, and other discrete operations occur only after their visible trigger. Do not impose a direct-pixel rule that contradicts the selected tool.
- When BPM is load-bearing, declare the beat origin, calculate `60 / BPM` seconds per beat, and make beat labels agree with any second timestamps. State whether the tempo belongs to audible music, a click track, synchronized physical sounds, or a silent choreography grid.
- For a one-take performance, define one traversable camera route before its local pushes, arcs, rises, whips, and lens changes. Preserve spatial direction and subject continuity; do not let a flash, blur, occlusion, or foreground pass conceal a cut or substitution.
- Give major pose or body-state changes a physical bridge through support, weight transfer, limb order, contact, relevant garment or prop response, and arrival at the next readable lock.
- For UI, mechanical transformations, signs, and titles, enumerate every intermediate state chronologically and quote literal copy exactly. Treat a tagline, title card, or HUD string as a timed readable last-frame state, not a sticker overlay.
- When exact hosted-surface text remains garbled and an approved text plate is available, supply that plate as an image reference and explicitly tell H3 to interpret it as an image rather than re-typeset it. Keep this workaround surface-specific and preserve the plate's lettering and layout.
- For FL2VA and L2VA, describe the physical path that narrows differences and lands on the final frame; do not jump to it.
- Do not impose a generic cuts-per-second, text-card, or minimum-hold ceiling. High-density timelines are valid when they remain within hard surface limits, cover the requested window, give every cut or phase one dominant information job, factor global rules out of local beats, and land each beat in a recognizable state.
- Choose the edit topology explicitly. A dense editorial montage may alternate action with graphic cards and demand a new composition per cut; a causal UI journey or material transformation may preserve one rail, bracket, tile, card, leader line, or surface and transform it into the next state. Do not blur the two into an accidental slideshow. Write `hard cuts only` or `one continuous shot` when that choice is load-bearing.
- Treat sparse frame-scale directions such as a two-frame stagger, overshoot, or rebound as useful motion-character cues inside second-based macro ranges. Do not promise frame-exact obedience unless the output is being measured.
- In a reusable freeform template, controlled alternatives may share one functional slot when every option serves the same beat. Resolve them in a one-off prompt only when the user has supplied the needed creative choice.
- Fit spoken words to the available seconds. Keep speaker IDs stable and assign them by actual vocal-event order.
- H3 uses cuts by default on the hosted surface. If the request is one continuous take, remove shot/cut structures and describe one continuous action path. For dialogue that crosses a cut, identify the on-screen or off-screen speaker and state that the line continues across the cut.
- Separate diegetic sounds, ambience, physical sound effects, and audience-only music according to the official guide.
- Preserve all untargeted identities, actions, props, framing, timing, lighting, and audio explicitly in editing prompts.
- When a local graph pads or pins context and trims afterward, write prompt timestamps on the untrimmed render clock. Keep the requested delivery-window crop outside the prompt and provide the render-to-delivery offset.
- Finish every required beat and payoff by the retained raw-clock endpoint `(raw_frames - trailing_trim_frames) / 24`. Only disposable continuation or an already-established final hold may extend into the trailing crop.

For an exact trimmed delivery length, calculate in frames:

```text
requested_delivery_frames = round(requested_delivery_seconds * 24)
raw_frames = smallest 17k+5 value at least requested_delivery_frames + leading_trim_frames
trailing_trim_frames = raw_frames - leading_trim_frames - requested_delivery_frames
```

Use the graph planner's returned raw/trim values when it provides them. If exact duration matters, apply both leading and trailing crop; otherwise disclose the actual delivered duration.

Use the page-derived planning patterns in `references/showcase-patterns.md`, especially explicit asset roles, timed beats, transition bridges, literal text, identity locks, and preservation/exclusion clauses.
For proven dense motion-design work, use `references/proven-dense-motion-design.md` and preserve demonstrated complexity unless an actual result shows omitted, merged, unreadable, or drifting requirements.

### 7. Draft In The Exact Schema

The structured base profile uses, in order:

```text
integrated_multimodal_description:
overall_soundscape:
non_diegetic_music:
```

I2VA, FL2VA, and L2VA additionally require their exact first-line alignment instruction from `references/base-en.txt`, followed by one blank line.

The structured Ref2VA profile uses, in order:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

For structured Ref2VA, create retention rows for standalone tracked labels, not for inline provenance-only picture/video citations. Use only the fixed task types and relationship markers in `references/ref-en.txt`.

The native-ComfyUI profile uses one freeform block: visual style and scene anchor, one explicit job per connected reference, causal timed beats, camera/performance, dialogue and synchronized sound, preservation/exclusion rules, and a final hold. In I2VA/L2VA/FL2VA, use only the connected `<Picture N>` endpoint tags described above. In Ref2VA, use exact `<Picture N>`, `<Video N>`, and `<Audio N>` tags. Do not wrap the raw prompt in the six structured field headings or invent `<Subject N>` media handles.

The official hosted-freeform profile defaults to three semantic parts: `Reference Asset Instructions`, `Core Concept`, and `Shot-by-Shot Description`. It uses upload-order `@Image N`, `@Video N`, and `@Audio N` handles when the live surface exposes them. A compact `PARAMETERS` dictionary, contiguous numbered-cut grid, named macro-stage timeline, and global editing/audio/exclusion blocks remain optional freeform conveniences supported by a compatible surface or a user-confirmed result; they do not become structured-provider fields. Keep unresolved placeholders only in templates and use supplied final values for production prompts.

For a compatible hosted surface, the optional creative-director JSON profile organizes the same content into concept, reference contract, camera, typography, visual style, motion, sound, storyboard, and continuity fields. Use it only when requested or supported by surface evidence; it is not an API payload or a new provider schema. Read `references/hosted-creative-director-json.md` for compilation and separate JSON/timeline checks.

### 8. Validate

Save the draft to a temporary text file and run:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --mode MODE --duration SECONDS
```

For native ComfyUI, validate the raw profile and provide actual connected counts for Ref2VA:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile comfyui --mode ref2va --duration SECONDS --pictures N --videos N --audios N --standalone-audios N
```

For a documented hosted-freeform surface, validate its timeline and declared parameters without imposing native media tags:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile hosted --mode MODE --duration SECONDS
```

`--audios` is the number of connected audio ordinals, including enabled reference-video soundtracks; repeated mentions of one ordinal still count once. `--standalone-audios` counts separate audio files only. `--duration` is the graph's requested pre-snap duration and remains within the official 4–15-second range. Append `--raw-frames N` when the graph exposes its actual untrimmed `17k+5` frame count, plus `--trim-frames N` and/or `--tail-trim-frames N` when it crops after decode. The linter uses explicit raw frames for timestamp and delivery-window checks; otherwise it derives them from `--duration`.

Correct all errors. Review warnings rather than deleting required content merely to silence them. Also perform the semantic checks the linter cannot prove:

- every requested beat appears once and in order;
- every media claim matches inspection;
- every quoted line and visible label is exact;
- every action and line fits the duration;
- camera direction is physically coherent;
- every declared exact count matches every occurrence of the counted unit, including unnumbered held states when states or poses are being counted;
- beat and second clocks share one origin and agree whenever exact synchronization is claimed;
- every procedural change has a visible, tool-consistent cause and its retained state does not jump, morph, or reveal itself autonomously;
- a one-take route is spatially traversable and no flash, blur, occlusion, or foreground pass hides a cut;
- major pose transitions make support, contact, and weight transfer causal while preserving anatomy and any relevant garment or prop continuity;
- when a source image is designated only as a generation control rather than a literal endpoint or intended in-scene asset, the source asset itself remains off-screen and is not silently treated as an opening frame, pasted asset, trace, overlay, or reveal;
- opening registration and final holds are explicitly scoped when the rest of the clip must remain continuously active;
- keyframe convergence is explicit;
- edits name both change and preservation;
- audio layers are assigned to the correct section;
- cut topology is internally consistent: a declared oner does not contain separate shots, and requested music does not conflict with `N/A` or a no-music rule;
- no analysis, settings, caveats, or Markdown labels have leaked into the prompt block.
- when revising a user-confirmed successful prompt, every simplification answers an observed defect or an explicit request rather than a generic capacity concern.

### 9. Deliver

Use this compact structure unless the user requests prompt-only output:

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

When the user asks for easy copy/paste, return one standalone fenced block per prompt with minimal wrapper text.

## Failure Conditions

Stop and request the missing asset or decision only when it materially changes the result. Do not:

- claim to have inspected inaccessible media;
- treat every image as a concrete keyframe;
- create an audio label merely because a video has an audio track;
- use audio as the sole Ref2VA media input;
- omit the base guide when writing Ref2VA;
- paraphrase supplied dialogue, lyrics, signs, titles, or UI copy;
- use hosted `@Image N` / `@Video N` / `@Audio N` handles in a structured or native-ComfyUI prompt, or use structured/native angle-bracket labels in a hosted prompt without surface evidence;
- treat a storyboard sheet as a literal first frame when it is only shot order;
- convert visible change into abstract mood language;
- use undefined labels, nonsequential shots, or out-of-range timestamps;
- place a mode setting inside the paste-ready prompt by default;
- promote `Hybrid`, Turbo, audio-lock, or motion-context controls into new official H3 modes;
- convert local frame grids, training-range estimates, sampler settings, or VRAM advice into provider-wide model limits;
- assign `<Audio N>` to a track used only after generation;
- represent a showcase example marked “Partial prompt — expand as needed” as a complete canonical recipe.
- call a prompt overloaded, reduce its cuts, inline its parameter dictionary, lengthen its short holds, or remove sparse frame-scale cues solely because they look ambitious when the user has demonstrated that architecture successfully.

## Resources

- `references/base-en.txt`: immutable official grammar for T2VA/I2VA/FL2VA/L2VA and shared audiovisual rules.
- `references/ref-en.txt`: immutable official Ref2VA grammar.
- `references/model-contract.md`: audited capabilities, limits, surface distinctions, provenance, and official-license warning.
- `references/runtime-surfaces.md`: official structured, hosted, and native-ComfyUI prompt/runtime profiles.
- `references/official-hosted-prompt-guide.md`: August 11 hosted prompt formula, media handles, shot continuity, text workaround, and common pitfalls.
- `references/community-runtime-extensions.md`: pinned third-party ComfyUI overlays, compatible practices, and risks.
- `references/media-inspection.md`: exhaustive media/frame/audio inspection workflow.
- `references/showcase-patterns.md`: all 58 current page demonstrations, the two prompt-guide examples, and their durable prompting lessons.
- `references/proven-dense-motion-design.md`: user-validated high-density editorial-montage, causal-UI, and material-transformation planning patterns.
- `references/motion-design-fundamentals.md`: sourced motion-design procedure, typography, timing, sound, and render-review checks.
- `references/candidate-motion-design-patterns.md`: explicitly evidence-bounded experimental patterns and staged production workflow.
- `references/hosted-creative-director-json.md`: optional hosted creative-brief organization, not an official provider schema.
- `references/edge-case-playbook.md`: practical resolution rules for ambiguous modes, tool-causal creation, counted beat-mapped performance, and other fragile requests.
- `scripts/lint_h3_prompt.py`: deterministic structural and timing validator.
- `scripts/validate_coverage.py`: maintenance validator for required files, official-source invariants, grammar hashes, and August 11 showcase coverage.
