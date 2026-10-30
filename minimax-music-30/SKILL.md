---
name: minimax-music-30
description: Create, optimize, audit, and serialize production-ready MiniMax Music 3.0 songs, three-part Structured Captions, section-tagged lyrics, and runtime payloads. Invoke whenever the user requests a MiniMax Music 3.0 prompt, song package, structured music caption (Global Metadata / Vocal Details / Arrangement), section-tagged lyrics, instrumental cue, hosted MiniMax /v1/music_generation API payload, open-weight SGLang-Omni or Diffusers Music 3.0 call, native ComfyUI Music 3.0 workflow, template-library routing, or Music 3.0 render repair.
---

# MiniMax Music 3.0

Build complete, production-ready MiniMax Music 3.0 packages that strictly preserve the provider's dual-input architecture (`Caption` $\neq$ `Lyrics`) and target-surface serialization rules.

## 1. Non-Negotiable Invariants

1. **Strict Dual-Input Separation (`SongGen` `arXiv:2502.13128`)**: Treat `Caption` and `Lyrics` as separate inputs. Never bury lyrics inside the caption or place production essays inside the lyrics field.
2. **Newline-Isolated Section Tags (SGLang/Diffusers normalization, [prompt-architecture.md](references/prompt-architecture.md))**: Place every lyric section tag (`[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Solo]`, `[Instrumental]`, `[Outro]`) strictly alone on its own line, with blank lines between sections. Local runtimes silently drop sung text placed on the tag line.
3. **Surface Isolation**: Keep hosted API, SGLang-Omni, Diffusers, and ComfyUI controls separate. Do not import Suno controls, Music 2.6 assumptions, TTS voice fields, or generic diffusion parameters.
4. **Generative Honesty & Rights**: Treat BPM, key, instrumentation, and structure as generative conditioning rather than symbolic MIDI guarantees. Describe abstract musical traits rather than cloning living artists.
5. **Licensing Boundary**: Never claim the open weights are Apache or MIT licensed; they use the MiniMax-Music3 Community License. Read [model-contract.md](references/model-contract.md) before giving licensing or deployment guidance.

## 2. Request Routing Decision Tree

Select one primary execution route:

| Route | Deliverable | Required Reference Loading |
| --- | --- | --- |
| **1. Creative Package** | Concept + 3-part Structured Caption + tagged Lyrics + iteration plan | Read [prompt-architecture.md](references/prompt-architecture.md) for every prompt-writing or repair task, plus [genre-router.md](references/genre-router.md). |
| **2. Caption Only** | Provider-authored 3-part Structured Caption (`Global Metadata`, `Vocal Details`, `Arrangement`) | Read [genre-router.md](references/genre-router.md) and [prompt-architecture.md](references/prompt-architecture.md). |
| **3. Lyrics Only** | Original, singable, prosody-checked, section-tagged lyrics | Read [songcraft-and-originality.md](references/songcraft-and-originality.md) when writing lyrics, adapting references, scoring picture, or diagnosing musical weakness. |
| **4. Hosted MiniMax API** | Valid `/v1/music_generation` or `/v1/lyrics_generation` JSON payload | Read [runtime-surfaces.md](references/runtime-surfaces.md) for routes 4–9 and [examples.md](references/examples.md) when a payload or formatting pattern is useful. |
| **5. Open-Weight SGLang-Omni** | `instructions` (Caption) + `input` (non-empty tagged Lyrics) + 25 fps frame cap | Read [runtime-surfaces.md](references/runtime-surfaces.md) and [music-generation-research.md](references/music-generation-research.md). |
| **6. Open-Weight Diffusers** | `prompt`, `lyrics`, `audio_duration`, and seeded `torch.Generator` call | Read [runtime-surfaces.md](references/runtime-surfaces.md). |
| **7. Native ComfyUI** | Separate Caption and Lyrics node inputs + workflow settings (`max_duration`, seed, tiled decode) | Read [runtime-surfaces.md](references/runtime-surfaces.md). |
| **8. Render Repair** | Single-layer causal diagnosis and minimal targeted revision | Read [prompt-architecture.md](references/prompt-architecture.md) and [music-generation-research.md](references/music-generation-research.md). |
| **9. Hosted Cover Companion** | Explicit `music-cover` hosted workflow (only when requested; not an open-weight Music 3.0 feature) | Read [runtime-surfaces.md](references/runtime-surfaces.md). |

Read [source-coverage.md](references/source-coverage.md) before asserting current availability, rate limits, installation, or licensing details.

## 3. Execution Protocol

### Step 1: Establish the Contract & Song Architecture
1. Extract target surface, vocal vs. instrumental mode, target duration (advertised complete-song target is **up to 5 minutes**; local 9,000-frame / 6-minute cap is an implementation ceiling, not a coherence promise), language, genre/groove, emotional arc, vocal timbre, instrumentation, and exclusions.
2. **Align Caption & Lyric Chronology (8B Global LLM carries song structure, `references/music-generation-research.md`)**:
   - Design the section order (`[Intro]` $\rightarrow$ `[Verse]` $\rightarrow$ `[Pre-Chorus]` $\rightarrow$ `[Chorus]` $\rightarrow$ `[Bridge]` $\rightarrow$ `[Outro]`) before drafting prose.
   - Give every section a distinct dynamic and instrumental delta (`YuE`, `arXiv:2503.08638`) so the model does not loop a static backing loop.
   - Budget lyric length to duration ($\text{frames} = \text{seconds} \times 25$ on local runtimes). Keep hooks shorter and more open-voweled than verses (craft heuristic).

### Step 2: Author or Preserve Section-Tagged Lyrics
- Preserve user-supplied lyrics verbatim unless revision is requested.
- Place each portable tag (`[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Solo]`, `[Instrumental]`, `[Outro]`) alone on its line with blank lines between sections.
- Keep parentheticals strictly to brief performable ad-libs or the local-runtime instrumental placeholder (`[Intro]\n(instrumental)\n\n[Outro]\n(instrumental)`).

### Step 3: Synthesize the Three-Part Structured Caption (250–450 Words)
Use progressive disclosure across the 1,000-template library without scanning all templates:
1. Read the official progressive-disclosure entry point, [genre-router.md](references/genre-router.md).
2. Open at most 1 primary family index (plus 1 secondary index only for genuine genre fusions).
3. Select at most 3 template cards (`Foundation`, `Modifier`, `Arrangement`) under `templates/` and synthesize fresh prose tailored to the user's brief (never copy template sentences verbatim).

Output these exact three headings in order:
- `### Global Metadata`: Genre/subgenres, tempo feel (include exact BPM/key only when requested or musically load-bearing), emotional progression, use-case scenario, and overall mix aesthetic.
- `### Vocal Details`: Lead configuration, timbre, register, articulation, harmonies/backing layers, and restrained vocal processing. For instrumentals, state explicitly that the track is instrumental and name the lead melodic instrument.
- `### Arrangement`: Chronological section-by-section timeline matching the lyric tags, tracking instrument entrances/exits, bass/percussion groove shifts, how the accompaniment leaves room for the vocal (`YuE` `arXiv:2503.08638`, `LeVo` `arXiv:2506.07520`), transitions, and spatial dynamics.

### Step 4: Serialize for the Target Surface
Follow [runtime-surfaces.md](references/runtime-surfaces.md) to Serialize fields without cross-surface leakage:
- **Hosted API (`/v1/music_generation`)**: `prompt` = Caption ($\le$2,000 chars); `lyrics` = Lyrics ($\le$3,500 chars). For instrumentals, set `is_instrumental: true` and omit `lyrics`. Never send `seed` or `max_new_tokens`. Streamed responses require `output_format: "hex"`.
- **SGLang-Omni**: `instructions` = Caption; `input` = non-empty tagged Lyrics (use `[Intro]\n(instrumental)...` placeholder for instrumentals). `max_new_tokens` caps frames at **25 fps** (max 9,000), `stream` must be `false`.
- **Diffusers**: Pass `prompt`, `lyrics`, `audio_duration` (upper bound), and a seeded `torch.Generator` (outputs 44.1 kHz stereo vs. SGLang's 32 kHz).
- **Native ComfyUI**: Supply Caption and Lyrics in their dedicated node inputs; keep `max_duration`, `seed`, and tiled decoding in workflow settings.

## 4. Diagnostic Repair Matrix

When repairing a prior render, keep the seed fixed (where supported) and modify only the single causal layer responsible. When comparing takes by ear, score the five SongEval dimensions (`arXiv:2505.10793`: coherence, memorability, vocal breathing/phrasing, structure clarity, musicality) and repair the weakest first. Root causes below are likely diagnoses, not confirmed mechanisms:

| Observed Defect | Likely Cause (`references/music-generation-research.md`) | Deterministic Repair Action |
| --- | --- | --- |
| **Skipped, repeated, or mangled lyric line** | Section tag shared a line with sung text, line exceeded the syllable budget, or generator lyric omission/repetition (`DiffRhythm+` `arXiv:2507.12890`). | Isolate `[Tag]` on its own line; trim overcrowded lines; then reroll. |
| **Track ends early below duration cap** | The model likely finished the lyric sheet before the cap. | Add structural sections (`[Instrumental]`, `[Bridge]`, repeat `[Chorus]`) or expand lyric bars. |
| **Track cuts off abruptly mid-phrase** | Hit `max_new_tokens` (25 fps) or `audio_duration` ceiling. | Increase frame/duration cap or condense lyric section count before touching the seed. |
| **Opening works, middle/end drifts or flattens** | `Arrangement` lacks section-specific instrument lifecycles. | Specify explicit entrances, dropouts, register shifts, and final-chorus lift per section. |
| **Muddy mix or buried vocals** | Too many simultaneous midrange parts competing with the lead. | Reduce simultaneous competing instruments; specify where the accompaniment leaves room in `Arrangement` and projection in `Vocal Details`. |
| **Vocal appears on an instrumental request** | Missing `is_instrumental: true` (Hosted) or stray sung words in `input` (Local). | Set `is_instrumental: true` and omit `lyrics` (Hosted), or use only `[Intro]\n(instrumental)` tags (Local) and declare instrumental lead in `Vocal Details`. |

## 5. Verification Gate (Black-Box Linter Execution)

Do not read the full source of `scripts/lint_music_prompt.py` into context unless debugging the script. Save artifacts to temporary files and run the linter as a black-box CLI check:

```bash
python3 scripts/lint_music_prompt.py --surface <hosted|sglang|diffusers|comfyui> --caption-file <caption.txt> --lyrics-file <lyrics.txt>
# Optional JSON payload check:
python3 scripts/lint_music_prompt.py --surface <hosted|sglang> --request-json <request.json>
```

When modifying skill files, also run `python3 scripts/validate_coverage.py`. Verify that no commentary, template IDs, or track titles leaked inside provider fields.

## 6. Resource Index

- [`references/model-contract.md`](references/model-contract.md): Audited architecture, 32 kHz vs. 44.1 kHz and Qwen3-8B vs. Qwen3.5-8B source discrepancies, and MiniMax-Music3 Community License terms.
- [`references/music-generation-research.md`](references/music-generation-research.md): Architecture facts used for frame budgeting and full-song research with findings separated from derived rules (`YuE` `arXiv:2503.08638`, `DiffRhythm` `arXiv:2503.01183`, `DiffRhythm+` `arXiv:2507.12890`, `SongGen` `arXiv:2502.13128`, `LeVo` `arXiv:2506.07520`, `SongEval` `arXiv:2505.10793`).
- [`references/runtime-surfaces.md`](references/runtime-surfaces.md): Exact field schemas, limits, and serialization for Hosted API, SGLang-Omni, Diffusers, ComfyUI, and `music-cover`.
- [`references/prompt-architecture.md`](references/prompt-architecture.md): Dual-input contract, three-part Structured Caption grammar, and section-tag discipline.
- [`references/songcraft-and-originality.md`](references/songcraft-and-originality.md): Prosody, hook construction, reference translation, and picture scoring.
- [`references/genre-router.md`](references/genre-router.md): Entry router to the 18 genre family indexes and 1,000 official caption templates in `templates/`.
- [`references/examples.md`](references/examples.md): Complete end-to-end payloads and formatting patterns across surfaces.
- [`references/source-coverage.md`](references/source-coverage.md): Audited repository commit hashes, rate-limit snapshots, and provenance.
- [`scripts/lint_music_prompt.py`](scripts/lint_music_prompt.py): Deterministic caption, lyrics, and JSON payload validator.
- [`scripts/validate_coverage.py`](scripts/validate_coverage.py): Repository structure, routing-link, and 1,000-template coverage validator.
