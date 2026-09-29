# Suno controls and provider guidance

This is a verified snapshot from August 8, 2026. Suno features and interfaces drift. Recheck official Suno sources whenever the user asks for current or latest behavior, version-specific controls, plan availability, exact limits, pricing, rights, or direct UI operation.

## Contents

- [Current snapshot](#current-snapshot)
- [Map the fields](#map-the-fields)
- [Recommended creation loop](#recommended-creation-loop)
- [Direct UI operation](#direct-ui-operation)
- [Rights and honesty](#rights-and-honesty)
- [Official sources](#official-sources)

## Current snapshot

- v5.5 is the current personalization-focused model in the verified snapshot.
- Advanced/Custom creation separates lyrics, Style, title, instrumental state, and Advanced Options.
- v5.5 on web includes a Duration slider.
- Creative controls include Weirdness and Style Influence; Audio Upload adds Audio Influence.
- Exclude accepts unwanted instruments, styles, or vocal qualities.
- Audio Upload supports up to 60 seconds on Basic and up to eight minutes on Pro/Premier in the verified snapshot.
- Pro/Premier users can create up to three private Custom Models from as few as six tracks they own.
- Voices can use a verified recording of the creator's own voice.
- Song Editor can replace, add, move, split, crop, fade, and extend sections.
- Remaster refines sound after structure and performance are settled; it is not a songwriting repair.
- Stem separation can produce up to twelve automatically detected categories, target one instrument plus its complement, or offer more granular Premier controls.

Do not silently assume these remain current. Prefer the provider's current documentation over community syntax or older model habits.

## Map the fields

### Title

Use a fresh title connected to the song's governing premise. Avoid a reference title, artist, branded world, or generic mood label.

### Style

Write a compact production brief in natural language. Include only audible decisions:

1. function and duration;
2. musical lane and contrast;
3. BPM or tempo feel, meter, and groove;
4. harmonic behavior;
5. instrument and vocal roles;
6. section evolution;
7. recording and mix space;
8. one signature rule.

Suno officially supports detailed conversational style instructions and recommends precise musical vocabulary. Exact compliance remains probabilistic.

### Lyrics

Use original lyrics and familiar section labels. Keep directions short. Put genre and production language primarily in Style, not inside lines intended to be sung.

For an instrumental, enable Instrumental and place the dramatic structure in Style or the available structure controls rather than inventing sung text.

### Exclude

Put unwanted instruments, styles, vocal traits, and production qualities here. Keep the main prompt positive. Do not rely on negative phrases buried in Style or Lyrics.

### Creative sliders

Treat values as iteration heuristics, never universal optimums:

- exploration: moderately higher Weirdness and looser Style Influence;
- text-only convergence: moderate Weirdness and stronger Style Influence;
- owned audio-seed convergence: lower Weirdness with stronger Style and Audio Influence.

Change one slider at a time in controlled A/B batches. State clearly that official documentation defines what the controls do, while any numeric starting value is a practical heuristic.

## Recommended creation loop

1. Start with a human-authored title, premise, hook, motif, rhythm, lyric, or recording.
2. Generate several candidates with the same prompt and settings.
3. Select for composition, hook, form, and performance before mix polish.
4. Freeze the winning identity and change only one variable per batch.
5. Replace weak sections in Song Editor.
6. Export WAV, stems, or MIDI when available.
7. Re-record, reprogram, or overdub at least one defining part for release-oriented work.
8. Add personal foley, room tone, automation, timing, and dynamics.
9. Use a subtle remaster only when the song itself is settled.

If the user owns at least six coherent tracks, consider a Custom Model. If the user has no catalog, prioritize an owned audio seed over a longer adjective list.

## Direct UI operation

When explicitly asked to create songs in Suno:

1. Read the available browser-control skill.
2. Open the signed-in Suno session and inspect the live Create form.
3. Verify model, mode, duration, privacy, and credit impact visible in the UI.
4. Keep songs private or link-only unless the user explicitly requests publication.
5. Use one initial batch by default.
6. Save the exact prompt and settings with each candidate.
7. Return links and numbered candidates for the user's listening decision.
8. Do not claim to hear or evaluate audio unless the active tools genuinely expose it.

Never buy credits, upgrade a plan, train another person's voice, upload unlicensed material, or publish a song without explicit authorization.

## Rights and honesty

- Suno's terms require the user to hold the necessary rights, permissions, and authority for uploaded submissions.
- Voice modeling is limited to the creator's own voice under the verified terms and guidance.
- Suno states that machine-learning output may not be unique and similar inputs can yield similar output for other users.
- Do not promise copyrightability, non-infringement, uniqueness, or detector evasion.
- When commercial release matters, advise the user to confirm the current plan rights and obtain professional legal advice for high-stakes questions.

## Official sources

- Current song-making guide: <https://suno.com/hub/how-to-make-a-song>
- v5.5 announcement: <https://suno.com/release-notes/introducing-v5-5-voices-custom-models-and-my-taste>
- Duration slider: <https://suno.com/release-notes/duration-slider-on-web>
- Detailed Style instructions: <https://help.suno.com/en/articles/5782849>
- Music glossary: <https://help.suno.com/en/articles/9010177>
- Creative sliders: <https://help.suno.com/en/articles/6141377>
- Exclude: <https://help.suno.com/en/articles/3161921>
- Audio Uploads: <https://help.suno.com/en/articles/6141569>
- Custom Models: <https://help.suno.com/en/articles/11362497>
- Voices: <https://help.suno.com/en/articles/11362369>
- Lyrics improvements: <https://suno.com/release-notes/lyrics-improvements-on-web>
- Song Editor: <https://help.suno.com/en/articles/6141505>
- Remaster: <https://help.suno.com/en/articles/8105281>
- Advanced Stem Separation: <https://help.suno.com/en/articles/12702337>
- Studio exports: <https://help.suno.com/en/articles/8128193>
- Moderation: <https://help.suno.com/en/articles/3198209>
- Terms of Service: <https://suno.com/terms/>
