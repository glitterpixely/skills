---
name: suno-song-builder
description: Create original song concepts, lyrics, instrumental scores, paste-ready Suno prompt packages, settings, and iteration plans from a user's brief or reference audio/video. Use when the user asks to make or generate a song, write or improve a Suno prompt, develop lyrics or hooks, score a film or short video, translate a reference track's appeal without copying it, diagnose generic or artificial-sounding Suno output, or produce multiple genuinely distinct song directions.
---

# Suno Song Builder

Turn a request into an original, production-aware song package. Treat Suno as a composition and production tool, not a uniqueness guarantee.

## Route the request

1. Identify the deliverable:
   - complete Suno prompt package;
   - song concept, lyrics, or hook development;
   - instrumental or picture-scoring cue;
   - reference-inspired originality translation;
   - diagnosis and revision of an existing result;
   - direct creation in the Suno UI when explicitly requested and browser control is available.
2. Extract supplied constraints: use case, duration, language, vocal configuration, genre lane, emotional arc, reference material, explicit exclusions, and output format.
3. Infer harmless defaults and proceed. Ask one concise question only when a missing choice would materially change the song, such as instrumental versus vocal when neither the brief nor reference resolves it.
4. Read [references/songcraft.md](references/songcraft.md) for reference mapping, lyrics, scoring, prompt construction, variation, and diagnosis.
5. Read [references/suno-controls.md](references/suno-controls.md) when specifying Suno fields or settings, discussing current features, diagnosing a Suno render, or operating the live product.

## Applicability Gate

Before building, record the active surface, deliverable, vocal/instrumental state, hard constraints, supplied references, and the listening or field-level check that defines success. Keep a confirmed arrangement tied to the tested Suno mode and context; do not generalize one render into a provider guarantee.

When repairing a result, classify the failure before rewriting: composition/representation, field routing, lyrics or prosody, guidance misapplied, performance/mix, runtime/material failure, or missing audition evidence. Change one causal layer at a time and preserve the strongest confirmed element. A prompt that was selected or followed but produced a weak song is not automatically a retrieval failure.

## Build the song

1. Write a one-sentence creative thesis containing:
   - the song's function;
   - a fresh central premise or dramatic situation;
   - the emotional turn;
   - one audible signature rule.
2. Define the musical engine:
   - duration and edit target;
   - BPM or tempo behavior and meter feel;
   - harmonic color or tonal center;
   - groove and microtiming;
   - instrument roles and performance behavior;
   - section-by-section energy movement;
   - recording space and mix character.
3. For vocal songs, develop the title, hook, point of view, section map, and singable lyrics before polishing production language.
4. For instrumentals, replace verse/chorus assumptions with a clear dramatic form and intentional edit points.
5. Translate the design into the provider fields described in `references/suno-controls.md`.

## Enforce originality

- Abstract a reference into high-level appeal such as energy curve, groove, ensemble relationship, vocal mechanics, or mix space.
- Replace the reference's central concept, title, lyrical hook, melodic contour, signature rhythm, harmonic path, section order, and defining sound event.
- Change at least five identity-bearing dimensions listed in `references/songcraft.md`; change more when the source is highly recognizable.
- Never put an artist name, source title, copied lyric, transcribed melody, or request for close imitation in a paste-ready prompt.
- Do not upload third-party music, film audio, or another person's voice to Suno unless the user establishes the necessary rights. Prefer a newly hummed motif, played chord loop, tapped rhythm, scratch vocal, or owned demo.
- Do not promise that output is unique or “undetectable.” Describe the workflow as originality-oriented and verify similarity by listening and revision.
- Make every song in a batch differ in premise, hook shape, groove, harmonic engine, lead timbre, and form. Do not reskin one template with new nouns.

## Deliver paste-ready fields

Use this default order:

1. `Creative direction` — one short paragraph explaining the governing idea and what makes it distinct.
2. `Title` — one standalone fenced block.
3. `Style` — one standalone fenced block containing audible production decisions.
4. `Lyrics` or `Instrumental structure` — one standalone fenced block.
5. `Exclude` — one standalone fenced block containing only unwanted sounds, styles, or production traits.
6. `Settings` — model, mode, instrumental state, duration, and clearly labeled slider heuristics.
7. `Iteration` — the smallest useful generate, select, edit, and finish loop.

When the user requests easy copying, individual formatting, or one-at-a-time prompts, keep every field or song in its own fenced block with minimal wrapper text. Count the complete paste-ready field when the user supplies a character cap.

Keep production directions out of sung lines. Use familiar section labels such as `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, and `[Outro]`; treat more elaborate tags and exact musical values as probabilistic guidance rather than code.

## Diagnose an existing result

1. Separate the failure into composition, arrangement, lyrics/prosody, performance, timbre, mix, or generation artifacts.
2. Preserve the strongest identity-bearing element.
3. Change one controlled variable per A/B batch.
4. Replace a weak section instead of regenerating a good song wholesale.
5. Rebuild or overdub at least one defining stem when the user wants release-ready individuality.
6. Remaster only after structure, lyrics, and performances are settled.

## Operate Suno only on explicit request

- Verify the live interface and current official guidance before relying on version-specific controls.
- Read and follow the available browser-control skill before operating a signed-in Suno session.
- Treat an explicit request to generate as authorization for one initial batch unless the user specifies a different amount. Do not buy credits, change subscriptions, publish publicly, or alter account settings.
- Use only inputs the user owns or has permission to use.
- Return the created song links and visible settings. Never claim to have judged audio that was not actually available for listening; ask the user to audition numbered candidates and report what they hear.
