---
name: kling-4-prompting
description: Write, optimize, and repair Kling 4.0 and Kling 4.0 Flash video prompts using model-specific limits and explicit reference roles. Use for text-to-video, image animation, first/last frames, multi-keyframes, Omni references, creative recreation, dialogue, visible text, and targeted video edits. Also use to plan extensions while checking feature availability. Applies to Kling 4 requests, not other video models or Kling 3 by default.
---

# Kling 4 Prompting

Turn the brief and supplied materials into a concise, ready-to-paste video prompt with separately stated generation settings. Optimize for observable action, reference ownership, coherent timing, and a deliberate final state.

This skill derives capabilities from Kling's **Meet All-New Kling 4.0!** release notes, read on **2026-09-28**. Prompt construction and examples are authored craft guidance, not official syntax or benchmark-proven recipes. Read [capabilities.md](references/capabilities.md) for the source, exact limits, conflicting statements, and availability boundaries.

## Choose the model and operation

- **Full Kling 4.0:** announced for October 2026; documented generation range 3–30 seconds. Do not treat the announcement as proof of account access.
- **Kling 4.0 Flash:** limited early access began September 28; documented generation range 3–20 seconds, 720p, 8-bit SDR. Do not silently transfer full-model controls or specifications to Flash.
- **HDR and repeated extension:** marked coming soon. Confirm current availability before giving executable instructions that depend on either.

For prompt-only work, proceed with the user's named model and label an unavailable feature as a future-use draft. Do not interrupt ordinary creative drafting to ask about account access. For live execution, verify the actual model, mode, settings, and upload controls. Read the capability reference when limits or model choice affect the task; refresh official evidence for current availability questions or requests outside this dated snapshot.

Choose the operation from the requested outcome:

| Need | Operation and controlling input |
| --- | --- |
| Invent a scene | Text-to-video |
| Animate an existing composition | Image-to-video; source image anchors the initial visual state |
| Arrive at a specific final composition | First & Last Frames; specify the causal bridge |
| Hit several visual story states in order | Multi-keyframes; ordered inputs, up to 10 on full 4.0 |
| Combine identity, performance, style, camera, voice | Omni Reference; bind each input to its role |
| Reuse an ad's pacing or camera with new content | Creative recreation; identify what is inherited and replaced |
| Change a region, subject, behavior, or style in existing footage | Video editing; identify exactly one primary video |
| Add new footage after an existing ending | Extension only if available; otherwise plan separately generated adjacent clips |

Do not equate an ordered keyframe sequence with an unordered identity reference set. Do not rewrite a supplied video when the user only wants a continuation. Backward extension and exact extension increments are not established by these notes.

## Build the prompt

### 1. Preserve the brief

Extract identities, subject count, action direction, environment, style, duration, framing, camera behavior, dialogue, audio intent, and final outcome. Preserve the newest literal corrections and previously accepted parts. Translate abstract emotion into visible performance without inventing a new plot.

If a detail is optional, make a reasonable creative choice. Ask a focused question only when ambiguity changes a core identity, reference assignment, edit target, or narrative endpoint. Do not require a form before writing a simple prompt.

### 2. Bind the materials

Inspect accessible assets; distinguish what was actually seen or heard from the user's descriptions. Do not diagnose an unseen result or infer video motion from one still frame.

For multiple references, make a compact working ledger:

| Input as labeled in the user's surface | Role | Inherit | Exclude when relevant |
| --- | --- | --- | --- |
| Character image | Identity | Face, costume, proportions | Reference background |
| Performance video | Action | Gesture order and timing | Performer identity and costume |
| Camera reference | Camera | Travel path and framing | Scene objects |
| Voice reference | Voice | Named speaker's vocal identity | Unrequested words or music |

Use actual attachment handles if supplied by the UI or user. Otherwise use plain prose such as “the character reference image” and “the camera reference video,” with an external mapping note when needed. Do not invent Kling token grammar or copy Seedance `@Image 1`, H3 subject tokens, or Midjourney flags as required Kling syntax.

Several views of one character define **one character**, not several cast members. Bind voice to a named speaker. Where references disagree, assign ownership by dimension: identity from the portrait, action from the motion video, camera from the camera video, words from the user's script. Exclude irrelevant references instead of giving them competing authority.

Check combined and per-type input budgets in the capability reference before recommending a large reference stack. Do not solve an over-limit request by silently dropping critical material.

### 3. Describe a filmable event

Use the shortest structure that expresses the job:

**Reference roles if needed → opening state → action and change → camera → visual treatment → audio → ending and essential constraints.**

For a simple shot, write one connected paragraph. For a complex narrative, use a few ordered beats or explicitly separated shots. An 8,000-token allowance is capacity, not a target.

- Write concrete verbs, trajectories, contact, reactions, and consequences. For physical action, establish footing and distance; show impact before debris or magical effects.
- Distinguish subject motion from camera motion. State the starting framing, movement direction, tracked target, and ending framing. Avoid simultaneous incompatible camera instructions.
- For a continuous take, explain transitions through camera travel or occlusion. For an edited sequence, name the cut and new viewpoint. Do not call hard cuts a continuous take.
- Use time ranges only when they clarify pacing. They are creative timing requests, not frame-exact control. Fit action and speech into the configured duration; reserve space for the requested ending.
- For image animation, spend words on what changes. Preserve source identity/composition/style as appropriate; do not re-describe the entire image or lock every moving component.
- For stylized work, retain the specified medium. Realism improvements do not require replacing anime, felt, clay, or illustration with photorealism.
- Specify a perceptible main movement, with secondary reactions at lower intensity. “Subtle” everywhere often weakens the intended animation; use visible amplitudes and clear paths.
- Keep failure constraints few and specific to the job, such as fixed subject count, stable product label, or no unrequested cut. The notes do not establish a separate negative-prompt field.

Read [prompt-patterns.md](references/prompt-patterns.md) for the relevant mode, including keyframe bridges, blockouts, stereo sound, dialogue, lettering, and edits. Examples are adaptable, not a mandatory output template.

### 4. Direct the audio and text deliberately

For speech, name the speaker, language/accent when needed, exact quoted words, performance, and speaking order. Distinguish vocal identity from dialogue content. Give visible facial performance time to match the line. Keep subtitles separate from spoken words.

Separate dialogue, environmental sound, synchronized effects, and music. Preserve the user's audio choices. When unspecified, use scene-appropriate ambience/effects without adding an unsolicited score; this is a skill default, not a Kling requirement. Ask for “No music” explicitly when appropriate. Reference audio is documented for **voice only**: do not promise music, sound-effect, or full-mix transfer from audio uploads.

For lettering, provide exact text, language, surface, position, and when it is visible. Short, readable copy and a deliberate hold are useful craft choices. Legibility claims still require inspecting the rendered spelling and stability.

### 5. Keep settings outside the prompt

State model, operation, duration, aspect ratio, resolution, and available audio/HDR controls separately when relevant. Text requesting “4K,” “30 seconds,” or “HDR” is not proof those output settings were selected. Keep requested settings distinct from confirmed current controls.

Do not invent model IDs, endpoints, JSON fields, seeds, guidance scales, frame rates, prices, or Flash feature parity. For API work, obtain the current official API contract first; the release notes are not an API specification.

## Deliver and refine

Lead with the complete copy-ready prompt. Add only necessary settings, reference assignments, or one concise availability/limit note. If the user asks for prompt only, omit explanatory material unless an essential feasibility issue must be disclosed. Do not include internal ledgers, source commentary, or alternative drafts inside the paste block.

For a requested video longer than one supported generation, write a sequence of valid clips with local timing and carry forward each boundary state. Label manual stitching as a production plan, not native extension. Never turn the forthcoming two-minute extension total into a single 120-second generation claim.

Before delivery, check model limits, reference roles, chronological beats, camera compatibility, speech budget, style, exact text, and the final state. For supplied results, read [review-and-repair.md](references/review-and-repair.md), preserve successful parts, and repair the observed mismatch. Prompt review, submission, rendering, frame inspection, playback, listening, and metadata verification are separate evidence states.
