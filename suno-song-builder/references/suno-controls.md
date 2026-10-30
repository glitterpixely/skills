# Suno controls and provider guidance

This snapshot was re-checked on October 30, 2026 against the official v6 help article (`help.suno.com/en/articles/13924481`), the `introducing-v6` release note, and the October 2026 Studio release notes. Items marked *unconfirmed* are not stated on those official pages. Suno features drift: recheck official sources, or read the live UI, whenever the user asks for current behavior, exact limits, pricing, rights, or direct UI operation.

## Contents

- [Current snapshot (Suno v6)](#current-snapshot-suno-v6)
- [v6 model family selection](#v6-model-family-selection)
- [Map the fields](#map-the-fields)
- [Recommended creation loop](#recommended-creation-loop)
- [Direct UI operation](#direct-ui-operation)
- [Rights and honesty](#rights-and-honesty)
- [Official sources](#official-sources)

## Current snapshot (Suno v6)

- **v6 Model Family** (official): v6 replaces the older models for new generations.
  - **`v6` (Flagship — Pro/Premier)**: "reliable, precise and consistently delivers polished music across every genre and style."
  - **`v6-wild` (Exploration — Pro/Premier)**: "less predictable and more varied, producing unexpected, textured and ambitious results"; bring ideas back into `v6` for refinement.
  - **`v6-mini` (All users, including Free)**: the fastest and free version of the v6 models.
- **Credit cost** (official): each generation makes two songs for a total of 10 credits, the same as v5.5. Many image and video inputs increase the cost.
- **Max Mode** (official): an option for any generation "when you want v6 to spend more on getting it right." It costs more credits (the help article gives no multiplier). Best for songs longer than two minutes, covers that should stay close to the original, style transfer from one song to another, and consistent vocals and style through the whole track. Standard mode is enough for quick ideas and short songs.
- **`Variety` slider** (official): introduces variety by adjusting and updating your style prompts. To keep full control of your style tags, set Variety to `0`.
- **Duration and field limits**:
  - The web Create form has a **Duration slider** (official release note, v5.5 era).
  - *Unconfirmed*: the maximum single-generation length for v6, and the `Style` (1,000 characters) and `Lyrics` (5,000 characters) caps. These caps come from third-party documentation only. Read the live character counter before promising a limit.
- **Creative Sliders & Negative Space**:
  - Creative controls include `Weirdness` and `Style Influence`; conditioning on an audio seed adds `Audio Influence`.
  - `Exclude` accepts comma-separated unwanted instruments, styles, vocal traits, or mix habits.
- **Natural-Language Song Editing & Song Editor** (official):
  - Edit part of an existing song in plain language while keeping the rest (*"Change the chorus so it's sung by a gospel choir"*), or change one lyric word or line (*"Change the lyric from 'love' to 'light'"*).
  - **Song Editor** can replace, add, move, split, crop, fade, and extend sections.
- **Multiple references, Sampling, & Mashups** (official):
  - In **Simple mode**, one prompt can reference Suno songs, playlists, audio uploads, images, and video, and v6 picks the workflow (Cover, Remix, Extend) itself.
  - Build a mashup from several of your sources in one request.
  - Audio Upload length in the earlier verified snapshot: up to 60 seconds on Basic and up to 8 minutes on Pro/Premier.
- **Personalization, Stems, & Remaster**:
  - Pro/Premier users can create up to **3 private Custom Models** from as few as **6 tracks they own**; existing custom models were upgraded to v6 automatically (official).
  - **Voices** can model a verified recording of the creator's own voice.
  - **Remaster** refines mix polish after structure and performance are settled; it is not a songwriting repair.
  - **Stem Separation** produces up to **12 automatically detected categories**, single-instrument + complement splits, or granular Premier exports.
- **Suno Studio Updates** (official, October 2026 Studio release note):
  - Larger **Clip Settings** sidebar and Clip Info panel.
  - **Fine Pitch Adjustment** in semitones plus cents (`2.38` = 2 semitones, 38 cents).
  - **Auto-stretch** setting for audio added from the library or uploads.
  - Timeline ruler **Grid Density & Contrast** controls; hide tracks with `Shift-H`, show them with `Shift-Alt-H`.

Do not silently assume these remain current. Prefer the provider's current documentation over community syntax or older model habits.

## v6 model family selection

| Model Variant | Availability | Primary Use Case | Pairing with `Max Mode` & `Variety` |
|---|---|---|---|
| **`v6`** | Pro / Premier | Default flagship for polished songs and scores | Set **`Variety` to `0`** for strict single-variable A/B tests; enable **`Max Mode`** (extra credits) for tracks `>2 min`, covers, or style transfer. |
| **`v6-wild`** | Pro / Premier | Motif discovery, unconventional textures, and genre-bending experiments | Leave **`Variety`** above `0` during exploration; take winning hooks back into **`v6`** to lock the arrangement. |
| **`v6-mini`** | All users (incl. Free) | Fast lyric/prosody checks, structural timing tests, and sketching | Test lyric meter and section lengths before spending paid-model or **`Max Mode`** credits. |

## Map the fields

### Title

Use a fresh title connected to the song's governing premise. Avoid a reference title, artist, branded world, or generic mood label.

### Style

Write a compact production brief in natural language. Keep it within the live character counter (third-party sources report 1,000 characters; unconfirmed officially). Include only audible decisions following a clear progression (Foundation $\rightarrow$ Expression $\rightarrow$ Development $\rightarrow$ Mix/Signature):

1. function and target duration;
2. primary musical lane and one compatible contrast;
3. BPM or tempo feel, meter, and groove pocket;
4. harmonic behavior or mode;
5. focal instrument and vocal roles (2–3 primary instruments + counter-voice);
6. section-by-section energy evolution (at least 3 states including subtraction);
7. recording space and mix finish;
8. one audible signature rule.

Suno v6 officially supports conversational studio briefs and descriptive musical vocabulary. Exact compliance remains probabilistic.

### Lyrics

Use original lyrics (within the live character counter; third-party sources report 5,000 characters) and concise section labels (`[Verse 1]`, `[Pre-Chorus]`, `[Chorus - full drums, wider guitars, backing harmony]`, `[Bridge - stripped to bass and dry vocal]`, `[Outro]`). Put global genre and mix language in `Style`, not inside lines intended to be sung.

For an instrumental, enable `Instrumental` and place the dramatic structure in `Style` or the available structure controls rather than inventing sung text.

### Exclude

Put unwanted instruments, styles, vocal traits, and production qualities here. Keep the main prompt positive. Do not rely on negative phrases buried in `Style` or `Lyrics`.

### Creative sliders, Variety, and Max Mode

Treat numeric slider values as iteration heuristics, never universal optimums:

- **Exploration (`v6-wild` or `v6`)**: moderately higher `Weirdness` (`40–65%`), looser `Style Influence` (`50–70%`), `Variety` above `0`;
- **Text-only convergence (`v6`)**: lower-to-moderate `Weirdness` (`20–40%`), stronger `Style Influence` (`75–90%`), `Variety` set to `0` when isolating single prompt edits;
- **Owned audio-seed / cover / long-form lock (`v6`)**: lower `Weirdness` (`15–35%`), strong `Style Influence` (`70–85%`), strong `Audio Influence` (`75–90%`), and **`Max Mode` enabled** (extra credits) when generating tracks over 2 minutes or requiring strict vocal/structural continuity.

Change one control at a time in controlled A/B batches. State clearly that official documentation defines what the controls do, while any numeric starting value is a practical heuristic.

## Recommended creation loop

1. Start with a human-authored title, premise, hook, motif, rhythm, lyric, or owned recording.
2. Sketch prosody quickly in `v6-mini` or explore bold textures in `v6-wild`, then lock production in flagship `v6`.
3. Generate candidates with identical settings (`Variety` at `0` when testing controlled prompt deltas).
4. Select for composition, hook, form, and performance before mix polish.
5. Use **v6 natural-language editing** (plain-text section, ensemble, or single-word lyric fixes) or **Song Editor** section replacement before regenerating an entire track.
6. Export WAV, up to 12 stems, or arrange directly in **Suno Studio** (using Auto-Stretch and fine semitone+cent pitch adjustment where needed).
7. Re-record, reprogram, or overdub at least one defining part for release-oriented work.
8. Add personal foley, room tone, automation, timing, and dynamics.
9. Use a subtle **Remaster** only when the song itself is settled.

If the user owns at least six coherent tracks, consider a **Custom Model**. If the user has no catalog, prioritize an owned audio seed over a longer adjective list.

## Direct UI operation

When explicitly asked to create songs in Suno:

1. Read the available browser-control skill.
2. Open the signed-in Suno session and inspect the live Create form.
3. Verify model (`v6`, `v6-wild`, or `v6-mini`), mode, `Max Mode` state and the credit cost shown in the UI, `Duration` slider, `Variety` state, and privacy visible in the UI.
4. Keep songs private or link-only unless the user explicitly requests publication.
5. Use one initial batch by default; do not enable `Max Mode` (extra credits) in live UI operation unless the user authorized the higher credit spend or requested `Max Mode`.
6. Save the exact prompt and settings with each candidate.
7. Return links and numbered candidates for the user's listening decision.
8. Do not claim to hear or evaluate audio unless the active tools genuinely expose it.

Never buy credits, upgrade a plan, train another person's voice, upload unlicensed material, or publish a song without explicit authorization.

## Rights and honesty

- Suno's terms require the user to hold the necessary rights, permissions, and authority for uploaded submissions (audio, stems, images, video, or mashup sources).
- Voice modeling is limited to the creator's own voice under the verified terms and guidance.
- Suno states that machine-learning output may not be unique and similar inputs can yield similar output for other users.
- Do not promise copyrightability, non-infringement, uniqueness, or detector evasion.
- When commercial release matters, advise the user to confirm the current plan rights and obtain professional legal advice for high-stakes questions.

## Official sources

- Introducing Suno v6: <https://suno.com/release-notes/introducing-v6>
- Suno v6 models & features help guide: <https://help.suno.com/en/articles/13924481>
- All release notes (v6 & Suno Studio updates): <https://suno.com/release-notes>
- Current song-making guide: <https://suno.com/hub/how-to-make-a-song>
- v5.5 personalization announcement (Voices & Custom Models): <https://suno.com/release-notes/introducing-v5-5-voices-custom-models-and-my-taste>
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
