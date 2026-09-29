# Prompt Architecture

This file is the canonical owner for generation-prompt structure, reference binding, scene activation, blocking, stages and shot sequencing, long-program segmentation, timestamps, camera, performance, dialogue, subtitles, and audio direction. Use [source-boundaries.md](source-boundaries.md) for factual limits and locked parameters, [task-contracts.md](task-contracts.md) for operation-specific templates, and [optimizer-runtime.md](optimizer-runtime.md) for ambiguity and output notes.

## Contents

- [Core formula](#core-formula)
- [Reference binding](#reference-binding)
- [Multi-reference organization](#multi-reference-organization)
- [Reference-led kinetic action](#reference-led-kinetic-action)
- [Space and blocking diagrams](#space-and-blocking-diagrams)
- [Long scenes and timestamps](#long-scenes-and-timestamps)
- [Programs longer than 30 seconds](#programs-longer-than-30-seconds)
- [Audio, dialogue, subtitles, and negative control](#audio-dialogue-subtitles-and-negative-control)
- [Camera and transitions](#camera-and-transitions)
- [Action and performance](#action-and-performance)
- [Products and real processes](#products-and-real-processes)
- [Pre-submission checklist](#pre-submission-checklist)

## Core formula

Build prompts from only the elements the task needs:

```text
Subject + Action or Event + Scene and Environment + Visual Style + Camera Movement or Cut + Audio
```

- **Subject + action/event**: name who or what does what.
- **Scene/environment**: location, time, weather, background state, layout, and spatial relationships.
- **Visual style**: lighting, color, material, texture, medium, and mood.
- **Camera/cut**: shot size, viewpoint, focus target, path, speed, destination, and transition.
- **Audio**: speaker, language, delivery, dialogue, voice reference, ambience, sound effects, and optional music.

Keep generation settings out of the creative prompt. Set ratio, duration, resolution, frame rate, and other configurable parameters on the surface or through its API. Existing user-authored event time ranges remain creative content and must not be discarded merely because duration is external.

For a short event, write a compact shot direction. For a complex event, use labeled material roles, subject relationships, event stages, and consistency locks. Do not add sections merely to fill a template.

When the user wants a supplied prompt's dense cinematic control style, treat it as a reference-led action problem: make the material contract and invariants precede the choreography, then express force, effects, camera, escalation, and failure prevention as observable instructions.

## Reference binding

Number assets by upload order within their media type unless the runtime already provides labels. Preserve the user's labels and spacing.

Use this form:

```text
@Image 1 defines <Subject A>'s <appearance, clothing, structure, or material>. Do not use <irrelevant people, background, or composition>.
@Video 1 defines <Subject A>'s <motion, camera path, pacing, or effect>. Do not use <identity, clothing, scene, or audio not requested>.
@Audio 1 defines <speaker or sound category>'s <voice, dialogue, ambience, sound effect, or music>. Do not use <irrelevant audio>.
```

Rules:

- Write every mapping in the prompt. Do not rely on names printed inside an image.
- Bind each named person, group, product, prop, and scene on its own line.
- State which part of an asset is used when only one attribute matters.
- Give one active material one primary job. A material may supply closely related attributes for the same entity, but do not let it become an uncontrolled source for identity, scene, motion, style, and audio at once.
- Prefer a job split when several images exist: one identity or multi-view appearance lock, one world / silhouette / environment lock. State exclusions on every line.
- If several images show the same entity, label front, left, right, rear, or attribute views and state the output count.
- If a video already defines motion, camera, and sequence correctly, name those dimensions and do not re-narrate every micro-action.
- If the user supplies exact dialogue and a voice reference, written text controls the words; audio controls voice traits unless reuse of the original audio dialogue is explicit.
- When the full material list is known, list every unused number under `[Unused Materials]` inside the prompt. State that unused items define no people, scene, prop, action, camera, or audio.

## Multi-reference organization

Use this order:

```text
Define each material's role -> Map subjects -> Group by type -> Create subject profiles -> Select references by scene
```

### Group by type

```text
[Characters]
<Character A> corresponds to @Image 1. Use only <observable appearance attributes>.
<Character B> corresponds to @Image 2. Use only <observable appearance attributes>.
Do not interchange their identities, clothing, actions, positions, dialogue, or audio.

[Props]
<Prop A> corresponds to @Image 3, remains one object, and belongs only to <Character A>.

[Scenes]
<Scene A> references @Image 4. Use only <layout, architecture, material, and lighting>. Do not use the people.

[Motion and Audio]
@Video 1 defines <named motion/camera dimension>. Do not use its person or scene.
@Audio 1 defines <named speaker or sound category>.
```

### Subject profile

Create one profile when a character or product spans several scenes and materials:

```text
[Subject Profile: <Name>]
Appearance and clothing: <references>.
Fixed prop: <reference and ownership>.
Allowed locations: <scenes>.
Motion and audio: <references>.
Do not use: <other subjects' appearance, props, or voices>.
```

### Scene activation

For each scene, list only the references needed there. State one primary event and a visible end state. The goal is correct selection and combination, not simultaneous appearance of every uploaded asset.

## Reference-led kinetic action

Use this optional structure for a high-energy, reference-driven fight, chase, transformation, destruction, or VFX sequence:

```text
[Reference Contract]
@Image 1 controls <identity, clothing, and prop design only>.
@Image 2 controls <world, creatures, lighting, and scale only>.
Do not import <unwanted people, setting, text, or visual layout> from either image.

[Global Locks]
Keep <subject count, identity, prop count, clothing, axis, palette, landmarks, and light direction> consistent.

[Force and Effect System]
<Effect> begins only when <visible physical trigger> occurs, then produces <ordered material response> and ends in <residue or recovery state>.

[Stage N]
Initial state: <blocking, prop state, camera state>.
Primary causal event: <preparation -> contact or trigger -> consequence -> recovery>.
Camera: <target and start> -> <path and speed change> -> <end framing and visible result>.
End state: <observable state carried into the next stage>.

[Failure Guards]
Do not generate <specific likely drift>. Generate <the intended replacement or preserved state>.
```

This mode has six reusable rules:

1. **Separate design extraction from action invention.** An appearance reference may control face, clothing, or prop construction without controlling its background. A world reference may control terrain, creature silhouette, lighting, or crowd density without importing its people or layout. If an existing action is remapped into another medium, state the replacement explicitly while preserving the action's dramatic function.
2. **Lock invariants before adding spectacle.** Repeat only the identity, count, ownership, landmark, axis, palette, and lighting facts that must survive every stage. For a single hero prop, say that only one instance exists and that its size, shape, ownership, and hand placement do not drift.
3. **Give force and VFX an origin.** Write `preparation -> acceleration -> contact -> force transfer -> material response -> residue -> recovery`. Heat, sparks, dust, fragments, cloth motion, glow, and smoke should come from contact, friction, velocity, impact, wind, or a named energy trigger. Prohibit source-free effects and effects that appear before the cause.
4. **Make impact readable before making it spectacular.** Use one primary causal chain per stage. Up to three short sub-beats are acceptable when the user explicitly wants tightly choreographed action, but they must be connected consequences rather than unrelated moves. If a stage needs more, merge it, split it, or use a later extension.
5. **Escalate by scale and consequence.** A reliable progression is distant mass or silhouettes -> readable mid-ground threats -> one elite contact -> battlefield-scale effect -> a new threat or aftermath hook. Keep distant crowds simple and reserve detailed anatomy, impact, and reaction for foreground subjects. Repeat two or three rigid environmental anchors so violent camera movement does not erase geography.
6. **Use a targeted failure-guard block.** Organize exclusions by identity/costume, prop count and anatomy, environment, effect causality, blood or gore policy, camera/edit behavior, and unwanted source-image artifacts. Pair important negatives with the intended replacement. Do not bury the prompt in generic quality words or a giant unrelated negative list.

Named techniques or effect names can be useful as shorthand, but define their visible behavior on first use. User-supplied percentages may express a creative priority or mixture; do not present them as guaranteed physical simulation. Exact engine, resolution, frame-rate, shutter, or other generation settings remain outside the creative prompt.

For reciprocal exchanges, combat-driven travel, aerial propulsion, pseudo-one-take bridges, and contact visibility during dense effects, apply the conditional craft guidance in [desk-prompt-patterns.md](desk-prompt-patterns.md#reciprocal-combat-and-action-driven-travel). Preserve the requested balance of power, location scope, ending, and prohibitions on slow motion or pauses.

## Space and blocking diagrams

Use stable objects to describe blocking: inside/outside a counter, in front of/behind a table, facing a door, on the road side of a barrier. Record facing direction, distance, and any separating structure. Screen-left/right alone is fragile because the camera can reverse.

When the user provides a clean blocking diagram, use it only for composition, subject positions, facing directions, distances, and spatial relationships. Do not reproduce arrows, labels, annotation boxes, grid coordinates, or explanatory text as visible video content. Bind the diagram explicitly:

```text
@Image 1 is a blocking diagram. Use only the composition, positions, facing directions, distances, and spatial relationships. Do not use its arrows, labels, boxes, grid, line-art style, or explanatory text.
<Subject A> stands <relationship to stable object>, facing <Subject B or landmark>.
<Subject B> remains <relationship to stable object>, separated from <Subject A> by <counter/table/door/road>.
```

If the diagram's identities or directions conflict with the user's text, the user's story assignment controls. If a core direction remains ambiguous, apply the stop rule in [optimizer-runtime.md](optimizer-runtime.md#mapping-confidence).

## Long scenes and timestamps

Prefer stateful stages for several events:

```text
[Generation Goal]
Generate <video type>. The central subject is <subject>; the primary event is <summary>.

[Stage 1]
Initial state: <characters, props, scene, camera, and audio state>.
Primary event: <one state-changing event>.
End state: <directly visible ownership, position, pose, or environment state>.

[Stage 2]
Continue from the previous stage: <facts that remain true>.
Primary event: <one state-changing event>.
End state: <observable state>.

[Maintain Consistency]
Keep <identity, count, clothing, prop ownership, layout, axis, camera direction, and audio roles> consistent.
```

Use as many stages as the causal sequence requires; three is not mandatory. Preserve subject roles, events, and end states before style adjectives.

For ordinary shot sequencing without required elapsed times, use `Shot N` blocks. `Shot N` is not limited to storyboard tasks:

```text
Shot 1: <specific visuals, shot size, action, camera, dialogue, and sound>.
Shot 2: <next causal shot and its visible end state>.
Shot N: <closing event and final visible state>.
```

Preserve shot numbers as identifiers. `Shot 45` means the forty-fifth shot, not a 45-degree angle, unless the user explicitly writes `45 degrees` or an equivalent camera-angle instruction.

Use timestamps as integer-second pacing allocations:

- **Range**: `0-3 seconds`, `3-7 seconds`, `7-12 seconds`.
- **Point**: at a named second, one key event or transition occurs.
- **Relative delay**: an event occurs a stated number of seconds after a trigger.

Rules:

- Make ranges continuous, consecutive, and non-overlapping.
- Give each range a realistic amount of content.
- Too little content permits improvisation; too much causes cuts or omissions.
- Do not ask for high-frequency repetitions such as several head shakes per second.
- Do not claim decimal or frame-level accuracy.
- If an external target duration is longer than the user's story, redistribute only the natural progression of existing action, reaction, breath, pause, pickup/handoff, or transition. Do not mechanically fill time with repeated motion, empty establishing shots, a new character, a new main event, or a new outcome. Do not invent numeric ranges merely to fill an external duration.
- If user-authored ranges conflict with an external duration and the user did not mark them hard, preserve order, relative pace, and outcome in nonnumeric stages. If the user explicitly says those ranges are hard constraints, ask one consolidated question to resolve the conflict and stop; do not silently change the ranges or output a provisional prompt.

For handoffs, state the object's ownership before and after. Once released, the prior holder no longer possesses it.

## Programs longer than 30 seconds

A single generated video is documented up to 30 seconds. Treat a longer requested finished program as a multi-call production plan:

1. Build one global beat map and protect the causal order, dialogue, ownership changes, and final outcome.
2. Group beats into clips no longer than 30 seconds. Each clip must form a coherent mini-scene with one observable opening state and one observable closing state; do not split in the middle of an uncompleted handoff or identity-critical reveal.
3. Prefer a cut boundary with a stable pose, held prop state, completed action, foreground occlusion, or clean camera resting point. Record identity, clothing, pose/orientation, prop ownership, layout/blocking, camera/composition, lighting, motion direction, and audio state in a boundary ledger.
4. Write one submit-ready prompt per clip using clip-local stages or `Shot N`. Keep global timestamps in the production plan; do not carry global seconds into a later prompt as if they were local model time.
5. When visible/audio continuity is required, render the earlier clip first and use it as the source for a forward-extension prompt for the following segment. When a hard cut is intended, a new generation prompt may start from the recorded next state.
6. Assemble the rendered clips outside the creative prompts. Do not claim that one Seedance 2.5 request produces a program longer than the documented per-video maximum.

For every later clip, repeat only the continuity facts needed at that boundary rather than padding the story with filler.

## Audio, dialogue, subtitles, and negative control

Natural language is valid. Use categorical syntax only when it improves separation:

| Content | Syntax | Example form |
|---|---|---|
| Music | `()` | `(low, restrained instrumental texture)` |
| Sound effects | `<>` | `<a distant bell rings>` |
| Dialogue | `{}` | `{Exact spoken line.}` |
| Subtitles | `【】` | `【Exact visible title】` |

If `<>` marks sound effects, write character names without angle brackets.

For each dialogue line specify:

```text
Language + user-requested regional variety/accent + delivery + speaker + {exact dialogue}
```

- Label every speaker separately.
- Do not infer an accent or dialect from the written language.
- If non-Chinese dialogue may be spoken in Chinese, reinforce the intended language.
- Add a regional accent only when the user requests it.
- If the user has not specified a spoken language, do not infer Mandarin, a dialect, nationality, or regional variety from the script, speaker appearance, or reference filename.
- In multi-speaker scenes, state who speaks and that listeners keep their mouths naturally closed.
- Preserve a dialogue ledger internally: speaker, vocal state, exact words, audio reference, language, delivery, and on/off-screen state.
- Do not expand a quoted fragment into new lines or turn a speaking intention into invented dialogue.
- If a character must speak using a bound audio reference but no reliable dialogue text is available, state that the character vocalizes using the spoken content from that audio reference. Do not invent words, and do not convert the stage to silence.

Whenever the prompt contains speech or dialogue and the user has not requested visible subtitles, add `No subtitles.` If subtitles are requested, use `【】` only for the exact supplied visible text and keep speaker/dialogue roles separate. Documented negative controls also include `No BGM; only ambience and action sounds` and `No audio`; use them only when relevant. For no-dialogue clips, control mouth movement, narration, sound sources, and visible text together.

The user's standing preference is no music unless requested. Default to dialogue, ambience, sound effects, or silence. If the user asks for music, bind its role and desired relationship to events.

## Camera and transitions

Basic supported language includes:

- extreme wide, wide, medium, medium close-up, close-up, extreme close-up;
- push in, pull out/dolly out, pan, lateral move/track, follow, orbit, dive, tilt up, handheld shake;
- low angle, overhead, and first-person view;
- one-take/long take, dolly zoom, aerial view, FPV, bullet time, handheld, and bounce speed ramp.

For every camera instruction name:

```text
Technique + target subject + start position/state + path/direction/speed + end position/state + visible result
```

For niche terms, retain the term but translate it into an observable foreground/background change. Examples:

- rack focus: name the foreground object that softens and the background subject that becomes sharp;
- shallow depth of field: name the subject that remains sharp and the bokeh background;
- tracking: match the subject's speed and state the opposite direction of background blur;
- dolly zoom: preserve subject size and state whether the background appears to approach or recede;
- vignette: corners darken gradually while the center and skin tone stay natural;
- speed ramp: use only when compatible with the requested pace; name the acceleration, deceleration, rebound, and final motion state. A useful impact cycle is real-time → burst or dash → short impact slow-motion → snap back to real-time. When slow motion or hit-stop is prohibited, use contact visibility, camera impulse, recoil, and environmental response while motion continues. Do not claim decimal-second or frame-accurate holds.

For a transition, specify trigger time/event, occluding or morphing object, camera direction and speed, transformation method, and the arrival composition or motion trend. A seamless bridge is not a pixel-identical splice.

## Action and performance

For action, prioritize a clear general pattern and a few memorable specifics. Avoid long catalogs of repeated moves. If a fight is not working, replace the choreography rather than adding style adjectives; keep identity, location, axis, and camera contract. One generated clip should carry one primary causal chain — split, edit, or extend instead of crowding named techniques.

Any spark, bloom, particle, fabric tear, or glow must name a physical origin (contact, friction, velocity, impact, wind, or a held prop). Do not write magic projection, beams, or aura unless the user asked for it.

For expressions, use direct observable cues rather than idioms.

For one emotional transition, use two to four cues:

```text
Starting emotion -> trigger -> immediate observable response -> gradual eye/brow/mouth/breath/gaze/hand/posture change -> final outward behavior
```

Use multiple trigger-based stages only when emotion changes several times. Show the cause before the reaction. Preserve both in one composition or connect them with one explicit gaze/camera shift.

## Products and real processes

Replace abstract claims such as efficient, smart, or reliable with:

```text
Initial state -> Concrete operation -> Observable result
```

One stage should demonstrate one operation. Keep product appearance, part count, component position, operator identity, and scene relationships stable. Use exact visible end states: button released, cover closed, item transferred, indicator changed, or output completed.

Exact specifications, formulas, signs, labels, and interface copy may require prepared reference graphics and post-production.

## Pre-submission checklist

- Is the subject and primary event explicit?
- Is every active reference assigned one role, with relevant exclusions?
- Is every distinct character, product, prop, group, and scene mapped separately?
- Are unused materials explicitly inactive when the full list is known?
- Are references activated by scene instead of forced into one moment?
- Does every stage contain one primary change and a visible end state?
- Are character count, clothing, prop ownership, blocking, axis, and audio relationships stable?
- Does an editing prompt identify one sole master, target count, scope, inheritance, and closed preservation set?
- Does an extension prompt use the observed boundary state, correct direction, motion/audio continuity, and single-instance rules?
- Does every anchor image have one exact frame or key-state role, with matching first/last ratios?
- Does a storyboard state reading order and excluded placeholder content?
- Is a blockout classified as coarse or fine with inherited and excluded dimensions?
- Are abstract emotion and camera terms translated into visible or audible changes?
- Are dialogue speaker, language, delivery, exact line, mouth state, and audio role correct?
- Are timestamps consecutive integer-second event budgets rather than promises?
- Are external parameters absent from the creative prompt?
