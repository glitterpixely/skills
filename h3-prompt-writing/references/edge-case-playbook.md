# H3 Edge-Case Playbook

Use these resolutions after reading the official guides. They clarify workflow decisions without changing provider grammar.

## Contents

- [Ambiguous Mode Selection](#ambiguous-mode-selection)
- [Missing Duration](#missing-duration)
- [Local Render Window Versus Delivery Window](#local-render-window-versus-delivery-window)
- [Conflicting References](#conflicting-references)
- [Precise Editing](#precise-editing)
- [Green Screen And Environment Replacement](#green-screen-and-environment-replacement)
- [Motion, Camera, And Performance Transfer](#motion-camera-and-performance-transfer)
- [Tool-Causal Procedural Creation](#tool-causal-procedural-creation)
- [Counted, Beat-Mapped Performance Oners](#counted-beat-mapped-performance-oners)
- [Voice And Dialogue](#voice-and-dialogue)
- [Visible Text, Titles, Signs, And UI](#visible-text-titles-signs-and-ui)
- [First/Last-Frame Convergence](#firstlast-frame-convergence)
- [Partial Showcase Examples](#partial-showcase-examples)
- [Unavailable Or Unreadable Media](#unavailable-or-unreadable-media)

## Ambiguous Mode Selection

### One image

- Literal first frame: I2VA.
- Literal last frame: L2VA.
- Identity, wardrobe, product, environment, composition, or style reference: Ref2VA.
- Edited keyframe plus further reference roles: Ref2VA with `keyframe completion`.

### Two images

- Literal first and last frames only: FL2VA.
- Two character/product/style references: Ref2VA.
- Storyboard panels or shot anchors: Ref2VA with standalone `<Picture N>` entries mapped to shots.
- First and last frames plus voice/motion/edit references: Ref2VA.

### Video present

- Directly alter pixels/content/timing of the source: `video editing`.
- Generate new content after its ending: `video continuation`.
- Borrow only motion, camera, rhythm, cuts, acting, or style: `reference generation`.
- Do not infer `audio reuse` from an enabled track alone.

## Missing Duration

Choose the shortest whole-second value from 4–15 that fits the observable beats. Budget roughly:

- 0.4–1.0 seconds for a readable micro-action or hard-cut insert;
- 1.0–2.0 seconds for a simple action plus reaction;
- 2.0–4.0 seconds for a spoken line, depending on word count and delivery;
- roughly 0.3–0.7 seconds for a simple final state, title, product, or UI confirmation when no stronger evidence governs the pacing.

These are starting heuristics for a new, untested concept, not provider limits. Never use average dwell time, cut count, prompt length, a short final hold, or frame-scale motion cues as a veto against a supplied or user-validated dense schedule. Judge the actual workload: one dominant information job per range, chronological coverage, clear transition topology, stable global rules, and a recognizable end state. Simplify only to address an observed omission, merge, readability failure, identity drift, or explicit user request. See `proven-dense-motion-design.md`.

## Local Render Window Versus Delivery Window

Some ComfyUI graphs snap to a frame grid, add leading context, or trim after decoding. Keep two clocks:

- render clock: the timeline the model actually receives;
- delivery clock: the retained interval after trim.

Write all prompt timestamps on the render clock. Shift requested beats by the graph's trim-start or leading-pad value and keep crop metadata outside the prompt. Verify the actual processed audio and video window, not only the requested UI duration.

For `ComfyUI-H3-Motion-Context`, read its pinned section in `community-runtime-extensions.md`. Its transported frames/latent/audio are graph state, so use canonical T2VA and do not label them as Ref2VA media. With the audited plugin version, do not combine motion context with stock first/last keyframes or existing Ref2VA references.

## Conflicting References

Create a control map:

| Attribute | Controlling source | Priority |
| --- | --- | --- |
| Identity | ... | strict |
| Wardrobe/product | ... | strict |
| Motion/performance | ... | transfer |
| Camera/edit rhythm | ... | structural |
| Environment/style | ... | reference |
| Voice/audio | ... | copy/reference |

Ask only when two sources claim the same strict attribute and the user's intent does not resolve the conflict. Otherwise state the hierarchy explicitly in subject definitions and retention analysis.

## Precise Editing

Name four things:

1. source target and interval;
2. requested replacement or transformation;
3. interaction and relighting consequences;
4. everything that must remain stable.

For multiple changes, write them separately before describing shared preservation. Examples of stable dimensions include other people, facial identity, hands, action timing, camera movement, framing, background geometry, shadows, reflections, audio, and duration.

For a deliberately simple edit, the showcase proves that a concise instruction can work. Use the already selected target-surface profile: structured Ref2VA when that profile applies, and freeform for a documented native-ComfyUI or hosted raw surface. If the surface is unknown, default to structured. Return a one-line command only when brevity still preserves the requested change and all necessary locks.

## Green Screen And Environment Replacement

- Define the foreground performance separately from the target environment.
- Remove green spill and preserve the original silhouette and action timing.
- Match perspective, camera movement, light direction, exposure, contact shadows, reflections, atmospheric depth, and occlusion.
- Make background elements respond causally to foreground actions when requested.
- Preserve embedded dialogue/audio unless the user targets it.

## Motion, Camera, And Performance Transfer

- Identify the destination subject and source motion separately.
- Transfer action phases, pace, expression timing, body mechanics, and camera relationship without transferring source identity unless requested.
- Describe nonhuman anatomical adaptation explicitly when mapping human action to animals or stylized characters.
- A camera/rhythm-only reference normally uses `reference generation`, not `video editing`.

## Tool-Causal Procedural Creation

Use this pattern for drawing timelapses, editing demonstrations, assembly sequences, UI-authored graphics, and other clips where the visible process must genuinely produce the result. It is prompt-audit guidance, not generation-validated capability evidence; inspect the output before claiming causal compliance.

- When an image is designated as a result, identity, or style target rather than a literal endpoint or intended in-scene asset, classify it as Ref2VA. State that the source asset itself remains off-screen and is not the opening frame, pasted content, a trace layer, overlay, reveal, or transition source; the referenced subject or style may still appear as requested.
- Show the required initial state long enough to register before work begins. If a blank canvas, empty timeline, unassembled object, or untouched surface is essential evidence, do not hide it behind the first action.
- Write each phase as `actuator -> visible input -> immediate tool-consistent effect -> retained state`. The actuator may be a cursor, hand, stylus, brush, machine head, button, or control.
- Continuous marks grow from the active tool path. Discrete operations such as fill, undo, stamp, toggle, delete, or an explicitly triggered command may change a larger or remote state only after their visible trigger and only as that operation permits. Do not require “only pixels under the cursor change” when the chosen tool legitimately acts elsewhere.
- Bound the allowed tool vocabulary and verify that every requested operation is achievable with it; do not prohibit the mechanism needed for a required change. Keep the working view readable when visible authorship is the point, so camera movement does not hide inputs or intermediate states.
- Keep completed work stable unless a later visible operation targets it. Exclude autonomous line growth, preloaded-content reveals, uncaused state changes, morphing, interpolation, and a last-second snap to the reference.
- Make corrections observable and local: identify the target, the selected tool, the imperfect removal or change, and the causal redraw. Avoid a generic “make corrections” beat that can become invisible cleanup.
- Prefer one coherent software or tool vocabulary. If exact branded fidelity matters, inspect and assign a separate UI/environment reference role; otherwise describe an unbranded tool class and do not simultaneously require exact brand recognition.
- Reserve a final hold after every required change is complete. Scope that hold, and any opening registration, as explicit exceptions to a global “continuously active” rule.
- Define intentional imperfection with positive defects—wobble, missed closures, overshoot, uneven pressure, asymmetry, crude fill, or awkward overlap—then use anti-polish exclusions only to protect those defects.
- When tone depends on a contrast, encode both sides as observable behavior—such as formal, disciplined presentation paired with intentionally crude output—rather than relying on abstract labels such as “funny” or “ironic.”
- Specify process audio separately from audience-only music: clicks, drags, motor motion, taps, erasing, or room tone may remain audible when music is absent. State whether audience-only music is present or absent rather than leaving it unspecified.

## Counted, Beat-Mapped Performance Oners

Use this pattern when one continuous performance contains an exact number of held pose/state locks or beat-triggered events such as reveals and impacts. It is prompt-audit guidance, not generation-validated capability evidence; inspect the output before claiming exact event, pose, beat, or camera-path compliance.

- Treat the declared count as a cardinality contract. Define whether the counted unit is an instantaneous event or a held state, number every occurrence once, distinguish connective motion from an additional counted occurrence, and do not add another instance of that counted unit after the final numbered occurrence. For held states, any following motion must remain within the final hold or be clearly non-locking unless another state is declared.
- Build an event ledger before prose: `number -> entry/cause -> counted event or readable lock -> exit/result`. Count opening and final compositions when they function as held states, even if they were not originally numbered.
- When tempo is load-bearing, calculate `beat_seconds = 60 / BPM` and `total_beats = duration_seconds * BPM / 60`; a fractional total-beat span is valid. Declare where beat 1 begins, then place locks, cuts, flashes, impacts, and clicks on named beats or subdivisions. Any second timestamp paired with a beat label must agree with the calculated grid to the precision displayed in the prompt.
- If BPM is only atmospheric, say so and do not promise exact synchronization. Otherwise identify whether it governs audible music, an audible click track, synchronized physical sounds, or a silent choreography grid; keep physical sounds and audience-only music distinct.
- Treat transition velocity and lock readability as separate controls. State where the performer and camera accelerate, brake, settle, and resume; a beat label alone does not define the motion profile.
- Define one global, collision-free camera route before local moves: starting position, height, subject side, travel direction, low/high point, focal-length behavior, and ending composition. Every push, arc, rise, whip, orbit, or braking move must remain on that route.
- Keep camera translation and lens change separate. Describe the intended focal-length holds, ramps, or deliberate snap zooms; do not use a focal-length range as a substitute for a spatial path.
- Do not hide a cut, camera teleport, duplicate subject, or pose substitution inside a strobe, white flash, motion blur, occlusion, foreground wipe, or close body pass. A final flash should clear in time to reveal the unobscured payoff.
- Give major body changes a causal bridge: planted support, weight transfer, limb order, floor or prop contact, relevant garment response, and arrival at the next lock. This matters especially for large level changes, extreme foreshortening, orientation reversals, and floor contact.
- Lock each relevant retained reference attribute positively: identity, anatomy, hairstyle, garment construction and coverage, accessory count/shape/placement, palette, linework, and rendering method. “Add no new accessories” does not prevent existing ones from disappearing.
- Audit reference coverage before promising unseen views. If strict rear, profile, foot, full-body, or garment-back accuracy is required but the supplied image does not show it, request another view or disclose conservative inference outside the prompt.
- For youth-ambiguous stylized work, state adulthood and intended wardrobe coverage explicitly when needed; keep the direction non-explicit unless the user requests otherwise within policy.
- Land the final numbered state—or the visible consequence of the final counted event—before the endpoint, let any flash or impact decay, and preserve a readable payoff hold whose job is clear rather than applying a universal minimum duration.

## Voice And Dialogue

- Quote user-supplied dialogue exactly and assign a stable speaker ID.
- Estimate spoken duration and reserve time for mouth closure or reaction.
- Voice timbre reference without signal copy: `<Audio N>` with `reference`.
- Source signal retained exactly: `fully_copy` or `partially_copy` as appropriate.
- Dialogue replacement in a video: preserve the source performance and timing only if compatible with the new line; otherwise specify the intended facial and body performance change.
- Never add source words when only timbre, pace, or emotion is referenced.

## Visible Text, Titles, Signs, And UI

- Put exact visible copy in English double quotation marks, even when it is not English.
- Preserve case, punctuation, spacing, and requested line breaks.
- Name where the text appears, when it resolves, how long it stays readable, and how it exits. A tagline or title is a last-frame readable state unless the user asked it to exit earlier.
- For layered editorial cards, establish the exact text as the sharp information plane first, then introduce character overlap, occlusion, parallax, or motion.
- Reserve an accent color for a semantic state such as active selection, progress, confirmation, or CTA when the interface uses color as logic rather than decoration.
- For UI/mechanical causality, enumerate every intermediate state in chronological order: selection, activation, transformation, confirmation, transition, final state.
- Keep the display region geometrically stable when only internal content should move.

## First/Last-Frame Convergence

- I2VA: begin from the actual image, then initiate motion.
- FL2VA: write observable intermediate changes that progressively reduce the difference between Picture 1 and Picture 2. Prefer one continuous shot unless cuts are explicitly required.
- L2VA: invent a compatible earlier state and land on the supplied frame in the actual last shot.
- Do not say only “transition to” or “morph into.” Name pose, object, camera, light, and spatial changes.

## Partial Showcase Examples

Thirty-five source-page demonstrations label themselves “Partial prompt — expand as needed.” Use them for one demonstrated technique only. Before adapting one, supply the missing duration logic, reference definitions, shot chronology, audio plan, preservation clauses, and official output fields.

## Unavailable Or Unreadable Media

If a referenced file cannot be opened, do not write a supposedly grounded prompt. Report which file failed and request a re-upload. If only one nonessential reference fails, proceed only when the user can still get the intended outcome and disclose the omission outside the prompt.
