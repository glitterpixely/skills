---
name: minimax-music-30
description: Create, optimize, audit, and operationalize production-ready MiniMax Music 3.0 songs and prompts from ideas, lyrics, references, or generation results. Use for structured Music 3.0 captions, original lyrics and section tags, vocal or instrumental tracks, full-song arrangement planning, hosted MiniMax API payloads, open-weight SGLang-Omni or Diffusers requests, native ComfyUI workflows, deterministic seed and duration planning, prompt repair, and explicitly requested hosted music-cover companion workflows.
---

# MiniMax Music 3.0

Build a complete Music 3.0 package while preserving the provider-native separation between the music description and the lyrics. Route by the actual generation surface before choosing fields or limits.

## Non-negotiable rules

- Treat `Caption` and `Lyrics` as separate inputs. Never bury lyrics inside the caption.
- Put every lyric section tag on its own line. Never place sung text after a leading tag on the same line.
- Keep hosted API, SGLang-Omni, Diffusers, and ComfyUI controls separate. Never transfer a field merely because another surface supports it.
- Use Music 3.0 facts only. Do not import Suno controls, Music 2.6 assumptions, TTS voice fields, or generic diffusion knobs.
- Treat tempo, key, instrumentation, words, and structure as generative direction rather than symbolic guarantees.
- Describe musical traits instead of requesting a clone of a living artist or a copyrighted recording. Preserve user-owned lyrics and references, but do not imply that generation clears rights.
- Do not claim that the open weights are Apache or MIT licensed. They use the MiniMax-Music3 Community License; read [model-contract.md](references/model-contract.md) before giving licensing or deployment guidance.

## Route the request

Choose one primary route:

1. **Creative package**: concept, structured caption, lyrics, and iteration plan.
2. **Caption only**: transform a brief into the provider-authored three-part Structured Caption.
3. **Lyrics only**: write or repair original, singable, section-tagged lyrics.
4. **Hosted MiniMax API**: emit a valid `/v1/music_generation` or `/v1/lyrics_generation` request.
5. **Open-weight SGLang-Omni**: emit `input` plus `instructions` and local runtime parameters.
6. **Open-weight Diffusers**: emit `prompt`, `lyrics`, `audio_duration`, and a seeded pipeline call.
7. **Native ComfyUI**: provide the Caption and Lyrics field contents plus workflow settings.
8. **Repair**: compare the intended package with the generated audio or reported failure, then change the smallest causal layer.
9. **Hosted cover companion**: only when explicitly requested; identify it as the separate `music-cover` model, not an open-weight Music 3.0 feature.

Read [runtime-surfaces.md](references/runtime-surfaces.md) for routes 4–9. Read [prompt-architecture.md](references/prompt-architecture.md) for every prompt-writing or repair task. Read [songcraft-and-originality.md](references/songcraft-and-originality.md) when writing lyrics, adapting references, scoring picture, or diagnosing musical weakness. Read [examples.md](references/examples.md) only when a concrete payload or formatting pattern is useful.

## Applicability Gate

Before building a package, record a compact contract:

- selected surface and route;
- vocal/instrumental state and active inputs;
- hard constraints, exclusions, and provider fields;
- the audible result that would count as success;
- any observed defect from a prior render.

Keep a successful package's architecture tied to the tested surface and context. Do not transfer controls from Suno, Music 2.6, TTS, or another runtime merely because the concepts sound similar. On repair, classify the failure first—representation, field routing, lyrics/tag parsing, guidance misapplied, runtime/material failure, or missing listening/validation evidence—then change one causal layer and rerun the linter or audition check.

## Build the brief

Extract what is known without interrogating the user unnecessarily:

- target surface and requested deliverable
- vocal song or instrumental
- target duration and use case
- language, lyrical premise, point of view, and content boundaries
- primary genre, secondary influence, groove, meter, and tempo feel
- emotional starting state, turn, peak, and resolution
- lead vocal configuration, timbre, register, delivery, harmonies, and effects
- primary instruments, supporting instruments, bass and percussion behavior
- section order, hook location, instrumental or solo moments, and ending behavior
- production era, density, dynamics, stereo space, and finish
- reference tracks or artists translated into abstract musical traits
- hard requirements and exclusions

Mark unsupported details as unspecified. Infer conservatively when the choice is reversible; ask only when a missing answer would materially change the song or execution surface.

## Design the song before wording the caption

1. Choose an energy arc with a clear contrast between sections.
2. Allocate lyric density to the available duration. Do not write a five-minute lyric sheet for a short audition.
3. Give each major section a musical job: establish, tighten, release, contrast, peak, or resolve.
4. Track instrument lifecycles. State what enters, leaves, widens, strips back, or changes pattern.
5. Reserve the strongest melodic, lyrical, and production event for the intended payoff.
6. For picture, map story turns and edit points to musical sections before writing lyrics.

Treat five minutes as the provider-advertised complete-song target. Some local runtimes expose a 9,000-frame ceiling equal to six minutes; do not turn that implementation ceiling into a promise of six-minute song coherence.

## Write or preserve lyrics

- Keep user-supplied lyric wording unchanged unless editing was requested.
- Use concise, singable lines with deliberate stress, vowel shape, rhyme pressure, and breath space.
- Make the hook shorter and more repeatable than the verse language.
- Use a portable core tag set unless the chosen surface requires otherwise: `[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Solo]`, `[Instrumental]`, `[Outro]`.
- Put tags alone on their lines. Use blank lines between sections.
- Do not place production essays, camera directions, or parenthetical paragraphs in the lyrics field.
- Use short parentheticals only for performable ad-libs or a minimal local-runtime instrumental placeholder.

See the surface-specific tag spellings and contradictions in [prompt-architecture.md](references/prompt-architecture.md).

## Build the Structured Caption

Use MiniMax's official progressive-disclosure library for substantial caption work:

1. Read the official progressive-disclosure entry point, [genre-router.md](references/genre-router.md).
2. Read one primary family index and, only for a real fusion, one secondary family index.
3. Select at most three cards with distinct roles: `Foundation`, `Modifier`, and `Arrangement`.
4. Read only the selected complete files under [templates/](templates/). Never scan all templates.
5. Synthesize a new caption around the user's brief. Do not copy template sentences or inherit unsupported specifics.

Return these headings in this order:

### Global Metadata

Specify genre and subgenres, tempo, emotional progression, scenario when useful, and the overall sonic and production profile. Include exact BPM, key, or scale only when explicit or musically justified.

### Vocal Details

For vocal music, specify lead configuration, timbre, register, delivery, harmonies or backing vocals, and restrained vocal effects. For instrumental music, explicitly say it is instrumental and identify the lead melodic role.

### Arrangement

Describe a section-by-section timeline with instrument lifecycles, groove and low-end development, transitions, texture, dynamics, and spatial changes. Prefer observable musical changes to adjective stacks.

Default to roughly 250–450 English words for a full structured caption, but obey the target surface's hard length limit. Keep lyrics, title, routing notes, template IDs, and hidden reasoning out of the caption.

## Serialize for the chosen surface

Follow [runtime-surfaces.md](references/runtime-surfaces.md) exactly.

- **Hosted API**: `prompt` receives the caption and `lyrics` receives lyrics. Do not add `seed` or `max_new_tokens`. Use `is_instrumental: true` with no lyrics for an instrumental.
- **SGLang-Omni**: `instructions` receives the caption and `input` receives non-empty tagged lyrics. Use a minimal instrumental placeholder when needed. `max_new_tokens` is a frame cap at 25 frames per second, not a guaranteed duration.
- **Diffusers**: use `prompt`, `lyrics`, `audio_duration`, and a seeded `torch.Generator`. Treat duration as an upper bound.
- **ComfyUI**: supply the three-part Caption and tagged Lyrics separately; set `max_duration`, seed, and tiled decoding in the workflow rather than inserting them into prose.

If the user wants copy/paste output, use one standalone fenced block per field or payload with minimal wrapper text.

## Repair a result

Classify the failure before rewriting:

- **Wrong genre or generic arrangement**: strengthen Global Metadata and the primary groove/instrument identity.
- **Correct opening, later drift**: make section-level instrument, energy, and vocal changes explicit in Arrangement.
- **Wrong or disappearing vocal**: clarify Vocal Details and ensure the lyrics are present and proportionate to duration.
- **Skipped lyric line**: check that no tag shares a line with text.
- **Truncated local render**: raise the duration/frame cap or shorten the lyric plan; do not change the seed first.
- **Track ends early below the cap**: the model may have emitted its end token; change structure or lyrics rather than assuming an infrastructure failure.
- **Muddy mix**: reduce simultaneous roles and define foreground, support, low end, and space.
- **Static song**: write entrances, exits, drops, lifts, breakdowns, and final-chorus deltas.
- **Prompt followed but song is weak**: repair hook, prosody, contrast, and payoff using [songcraft-and-originality.md](references/songcraft-and-originality.md).

Change one causal layer at a time and keep the seed fixed where the surface exposes one. Change the seed only to explore another take after the contract is sound.

## Validate before returning

Check that:

- the selected surface is explicit or safely inferable
- caption and lyrics are separate
- every tag is alone on its line
- every explicit constraint and exclusion is preserved
- an instrumental request remains instrumental
- no exact BPM, key, singer identity, or technique was fabricated without reason
- the emotional and arrangement arcs evolve across sections
- prompt fields and limits belong to the selected surface
- no template wording, track title, or artist imitation leaked into the result
- the package is paste-ready and contains no commentary inside provider fields

For saved artifacts, run:

```bash
python3 scripts/lint_music_prompt.py --surface <surface> --caption-file <caption.txt> --lyrics-file <lyrics.txt>
```

Use `--request-json <request.json>` for payload validation. Read [source-coverage.md](references/source-coverage.md) before asserting current availability, rate limits, installation commands, licensing, or runtime requirements; those facts can drift.
