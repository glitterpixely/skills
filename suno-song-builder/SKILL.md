---
name: suno-song-builder
description: Create original song concepts, prosody- and phonetics-checked lyrics, parody/lyric adaptations, instrumental film/game scores, 6-stage studio signal-chain Style strings (with 83 sonic archetypes across 68–174 BPM), paste-ready Suno v6 prompt packages (Title, Style, Lyrics, Exclude, v6/v6-wild/v6-mini Settings, Max Mode, Variety), natural-language edit commands, and A/B iteration plans from a user brief or reference audio/video. Invoke whenever the user asks to make a song, write or improve a Suno prompt, pick a sonic archetype, develop lyrics or hooks, write a parody or song adaptation, score a film or short video, translate a reference track's appeal into an original song without copying it, diagnose generic or synthetic-sounding Suno output, or operate Suno directly when authorized. Trigger terms: suno, suno v6, suno prompt, suno style prompt, make a song, write a song, writing a song, song lyrics, music prompt, parody song, adapting a song, AI music generation, film score, instrumental cue.
---

# Suno Song Builder

Turn a user brief, genre archetype, or reference into an original, production-aware Suno v6 prompt or full song package. Treat Suno as a probabilistic composition and production engine—never as a uniqueness, copyright, or symbolic-MIDI guarantee.

## 1. Request Routing Decision Tree

Identify the primary deliverable and load only the required references:

| Deliverable Route | Scope & Output | Required Reference Loading |
| --- | --- | --- |
| **1. Fast `Style` / Sonic Archetype Prompt** | Copy-ready 6-Stage Studio Signal Chain `Style` block (+ optional `Exclude`) from an archetype or vibe request | Read [`references/studio-signal-chain-and-archetypes.md`](references/studio-signal-chain-and-archetypes.md). |
| **2. Complete Suno v6 Song Package** | 1-line thesis + paste-ready `Title`, `Style`, `Lyrics`/`Instrumental structure`, `Exclude`, compact `Settings` (`v6`/`v6-wild`/`v6-mini`, `Max Mode`, `Variety`, sliders), and concise `Iteration` notes | Read [`references/studio-signal-chain-and-archetypes.md`](references/studio-signal-chain-and-archetypes.md), [`references/songcraft.md`](references/songcraft.md), [`references/suno-controls.md`](references/suno-controls.md), and [`references/controllable-song-research.md`](references/controllable-song-research.md). |
| **3. Concept, Lyrics, Hook, or Parody/Adaptation** | Premise, stressed-meter & phonetic-checked lyrics (or opt-in parody skeleton mapping), open-vowel hook, and standalone section tags | Read [`references/songcraft.md`](references/songcraft.md) and [`references/controllable-song-research.md`](references/controllable-song-research.md). |
| **4. Instrumental / Picture Score** | Through-composed or episodic dramatic cue with edit points, dropouts, and hero passage | Read [`references/studio-signal-chain-and-archetypes.md`](references/studio-signal-chain-and-archetypes.md), [`references/songcraft.md`](references/songcraft.md), and [`references/suno-controls.md`](references/suno-controls.md). |
| **5. Reference Originality Translation** | Appeal map + $\ge$5-dimension ($\ge$7 for famous sources) originality delta + fresh Suno v6 package | Read [`references/songcraft.md`](references/songcraft.md) and [`references/studio-signal-chain-and-archetypes.md`](references/studio-signal-chain-and-archetypes.md). |
| **6. Render Diagnosis & Natural-Language Repair** | Single-variable A/B repair plan, v6 natural-language edit prompt, or Song Editor section replacement | Read [`references/songcraft.md`](references/songcraft.md), [`references/suno-controls.md`](references/suno-controls.md), and [`references/controllable-song-research.md`](references/controllable-song-research.md). |
| **7. Authorized Live Suno UI Operation** | Direct browser creation (1 batch default, private/link-only, zero purchases) | Read [`references/suno-controls.md`](references/suno-controls.md) and the active browser-control skill. |

Infer harmless defaults (`2:40–3:20` full song; `2:30–3:15` film cue with a `40–60s` hero passage; check the live Duration slider for the current maximum) and ask at most one concise question only when a missing choice materially alters the work (e.g., vocal vs. instrumental when unresolved).

## 2. Deterministic Song Engineering Protocol

### Step 1: Write the Creative Thesis & Originality Delta (or Opt-In Parody Map)
1. **One-Sentence Thesis**:
   `A [function] about [concrete physical situation/decision], moving from [emotional state A] to [state B], identified by [one audible relational signature rule].`
2. **Originality Enforcement vs. Opt-In Parody (`references/songcraft.md`)**:
   - **Default (Original Songs & Reference Translation)**: Extract only abstract functional appeal (energy curve, pocket, ensemble relationship, mix space). **Never** include an artist name, producer name, song title, copied lyric, or recognizable progression in any field. Change **at least 5** identity-bearing dimensions (**at least 7** for famous/iconic sources): premise/title, hook phonetic shape, melodic contour, harmonic engine, groove/meter, section order, lead/counter-voice roles, signature sound event, recording space, and emotional resolution.
   - **Opt-In Parody / Lyric Adaptation (only when explicitly requested)**: Map the source skeleton first (syllables per line, stressed-beat positions, rhyme scheme, and open vowel families on held notes), lock new stressed syllables to the original beats, use monosyllabic swaps at hook anchors, and keep `Style` 100% free of artist or song-title names.
   - **Multi-Song Batches**: Vary **all 6 anchors** (Premise, Hook shape, Groove, Harmony, Lead identity, Form) across every option.

### Step 2: Engineer the `Style` Field (`Mustango` `arXiv:2311.08355` & `MusicRL` `arXiv:2402.04229`)
Captions are ambiguous by default: MusicRL reports that one caption maps to very different music for different users. Keep `Style` 100% positive (move all negations to `Exclude`) and within the live character counter (third-party sources report 1,000 characters, unconfirmed by Suno; obey any tighter user cap). Select the mode that fits the request:

- **Mode A — 6-Stage Studio Signal Chain** (best for fast style prompts, genre locks, and the 83 sonic archetypes in [`references/studio-signal-chain-and-archetypes.md`](references/studio-signal-chain-and-archetypes.md)):
  `[01. Era & Subgenre], [02. Exact BPM (68–174BPM)], [03. Core Timbres (specific amps, synths, samplers, acoustic models)], [04. Vocal Delivery (register, mic distance, texture)], [05. Scene & Mood (emotional arc & cinematic setting)], [06. Mix & Master (reverb space, console/tape saturation, stereo imaging)]`
  *Example*: `Dreamy 80s synth-pop, 110BPM, vintage Juno-106 poly-synths, shimmering 16th-note arpeggios, ethereal female vocal, hazy nostalgic midnight mood, spacious Lexicon hall reverb, warm analog chorus modulation`

- **Mode B — 8-Part Relational Studio Architecture** (best for picture scoring, reference originality translation, or custom multi-state arrangements):
  `[1. Function & target duration] -> [2. Primary genre lane + 1 contrast] -> [3. BPM/tempo feel, meter, & pocket] -> [4. Harmonic engine/mode] -> [5. Focal ensemble roles (2–3 core hardware/acoustic instruments + counter-voice)] -> [6. Vocal register, mic distance, & delivery (or instrumental lead)] -> [7. Section energy arc across >=3 states including subtraction] -> [8. Recording space, console/reverb finish, & 1 signature rule]`
  - **Focal Ensemble Rule (`LeVo` `arXiv:2506.07520`)**: Anchor around 2–3 primary instruments with specific hardware/acoustic timbres and relational verbs (`muted Telecaster answers the vocal cadence; upright bass holds a pedal drone`) rather than a 10-instrument noun list.

### Step 3: Engineer `Lyrics` or `Instrumental Structure` (`SongComposer` `arXiv:2402.17645` & `YuE` `arXiv:2503.08638`)
- **Prosodic Stress, Rhyme Blend, & Vowel Placement**: Keep `Lyrics` within the live character counter (third-party sources report 5,000 characters). Match stressed-beat counts across parallel verse lines without forcing awkward word inversions, blend perfect rhyme (for closure/hooks) with family/slant/internal rhyme (for momentum and tension), and place open sustainable vowels (`ah`, `oh`, `ay`, `oo`) on long hook notes.
- **AI Vocalist Phonetic & Pronunciation Hygiene (`references/songcraft.md`)**:
  - Spell numbers and symbols out as sung words (`twenty four seven`, `nineteen ninety-nine`).
  - Space or hyphenate acronyms (`A-I`, `N-Y-C`) unless sung as a word; respell or hyphenate tricky homographs/proper nouns (`thru`, `bi-o-en-gi-neer-ing`).
  - Use restrained delivery punctuation only where needed: hyphenated vowel extension (`lo-o-o-ove`) on melismas, ellipses (`I... need... you`) for breath pauses, and `ALL CAPS` sparingly for belted peaks.
- **Concrete Evidence Over AI Clichés**: Use tangible objects, places, actions, and interpersonal stakes; ban default AI filler (`neon shadows`, `echoes in the dark`, `ashes rising`, `scars`, `chains`, `destiny`) unless literally required by the brief.
- **Clean Section Tags (`YuE` `arXiv:2503.08638`)**: Place concise structural tags (`[Cold Open | dry single voice]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus | drums drop out]`, `[Bridge]`, `[Outro]`) alone on their own lines with blank lines between sections. Never stack contradictory metatags or put sung text on the same line as a `[Tag]`.
- **Instrumental Cues**: Enable `Instrumental` and structure by dramatic state (`Establish Motif` $\rightarrow$ `Build Motion` $\rightarrow$ `Subtraction/Drop` $\rightarrow$ `Hero Passage` $\rightarrow$ `Edit Tail/Resolve`).

### Step 4: Populate `Exclude` & Calibrate Suno v6 Controls (`JASCO` `arXiv:2406.10970`)
- **`Exclude` Field**: Comma-separated list of unwanted audible traits only (e.g., `stock risers, trap hi-hat rolls, supersaws, four-chord pop loop, heavy autotune, stadium reverb, over-compressed master`).
- **Suno v6 Model & Mode Selection (`references/suno-controls.md`)**:
  - **`v6` (Flagship — Pro/Premier)**: Default for polished, reliable, genre-accurate production.
  - **`v6-wild` (Experimental — Pro/Premier)**: Recommend when the user wants bold, unpredictable textures or avant-garde motif discovery before converging in core `v6`.
  - **`v6-mini` (Fast/All Tiers)**: Recommend for free-tier users or rapid lyric/meter/pronunciation sketching.
  - **`Variety` slider (`0` vs. above `0`)**: Set `Variety` to `0` to keep full control of style tags during controlled A/B takes; raise it for wider variation.
  - **`Max Mode` (extra credits; Suno gives no multiplier)**: Recommend for songs longer than 2 minutes, covers that stay close to the original, style transfer, and consistent vocals/style through the track.
- **Slider Heuristics (`references/controllable-song-research.md`)**: Clearly label numeric slider suggestions as practical heuristics (e.g., Exploration: `Weirdness 45–65% / Style Influence 50–70%`; Convergence: `Weirdness 20–40% / Style Influence 75–90%`; Owned Audio Seed / Mashup: `Audio Influence 75–90%`, avoiding hard `100%` artifact transfer).

## 3. Tiered Copy-Ready Delivery Schema

Lead immediately with the requested deliverable, keep wrapper prose short, and place every paste-ready field in its own standalone fenced `text` block:

### Tier 1: Fast `Style` / Sonic Archetype Requests
When the user asks for a quick `Style` string, sonic archetype, or backing vibe without lyrics:
1. **`Style`**:
   ```text
   [6-Stage Studio Signal Chain prompt string]
   ```
2. **`Exclude`** (include when helpful to protect the sonic pocket):
   ```text
   [Comma-separated unwanted traits]
   ```

### Tier 2: Complete Suno v6 Song Packages
When the user asks to build a song, score, or full prompt package, deliver in this order:
1. **Creative direction**: 1 concise sentence/paragraph stating the thesis, signature rule, and (when adapting a reference) the originality delta.
2. **Title**:
   ```text
   [Original title]
   ```
3. **Style**:
   ```text
   [Positive-only Mode A (6-Stage Studio Signal Chain) or Mode B (8-Part Relational Brief)]
   ```
4. **Lyrics** (or **Instrumental structure**):
   ```text
   [Section-tagged, prosody- and phonetics-checked lyrics, or dramatic instrumental cue map]
   ```
5. **Exclude**:
   ```text
   [Comma-separated unwanted instruments, styles, vocal traits, and mix habits]
   ```
6. **Settings**: Compact summary of Model (`v6`, `v6-wild`, or `v6-mini`), Mode (`Custom`), `Instrumental` toggle, `Duration` target, `Max Mode` (`On [extra credits]` vs. `Off`), `Variety` (`0` vs. above `0`), and heuristic slider ranges (`Weirdness`, `Style Influence`, `Audio Influence`).
7. **Iteration** (keep to 1–2 concise bullets by default; expand into full `SongEval` `arXiv:2505.10793` diagnostics, **v6 natural-language edit commands**, **Song Editor** section replacement, **Suno Studio** Auto-Stretch / cent-level pitch, 12-stem export, and **Remaster** steps when troubleshooting or requested).

## 4. Verification Gate & Diagnostic Repair

Before delivery, verify (and run [`scripts/prompt_lint.py`](scripts/prompt_lint.py) when validating files):
- [ ] **Zero Artist/Producer/Title Leakage**: No living artist names, producer names, reference titles, or copied hooks appear in `Title`, `Style`, `Lyrics`, or `Exclude`.
- [ ] **Length & Positive `Style` Hygiene**: `Style` and `Lyrics` fit the live counters (third-party-reported 1,000 / 5,000 characters when the UI is not visible), `Style` contains zero inline negations, and at least 3 distinct energy states (or a clear dynamic arc) are planned.
- [ ] **Prosody, Phonetics & Tag Hygiene**: Section tags sit alone on their own lines; numbers and acronyms are formatted for natural vocal pronunciation; verses use concrete physical imagery and natural spoken stress.
- [ ] **Evidence Honesty**: Settings distinguish official Suno v6 controls (`v6`/`v6-wild`/`v6-mini`, `Max Mode`, `Variety`, sliders) from practical numeric heuristics; un-auditioned audio is never described as heard or verified.

When repairing an existing Suno v6 render (`references/songcraft.md`), isolate the failure layer (`composition`, `arrangement`, `prosody/pronunciation`, `timbre`, `mix`, or `local section glitch`), preserve the winning seed/section, change **one variable per A/B batch** (with `Variety: 0`), and use **v6 natural-language editing** (e.g., *"Change the chorus arrangement to stripped upright bass and dry close harmony"* or *"Change the lyric in Verse 2 from X to Y"*) or **Song Editor** section replacement before regenerating the entire track.

### Do Not
- Do not upload or sample third-party music, film audio, or another person's voice in Suno (including in v6 mashups or multimodal prompts), or promise copyrightability, uniqueness, or detector evasion.
- Do not bury negative exclusions inside `Style` or `Lyrics` instead of using `Exclude`.
- Do not reskin the same chord loop and form across a multi-song batch.
- Do not purchase credits, change plans, enable `Max Mode` (extra credits) without user consent, or publish songs publicly when operating the live Suno UI.

## 5. Resource Index

- [`references/studio-signal-chain-and-archetypes.md`](references/studio-signal-chain-and-archetypes.md): The 6-Stage Studio Signal Chain, Tempo Pill bands (`68–174 BPM`), moderation-safe hardware/amp/synth/mic/console/reverb lexicon, and 83 engineered copy-ready sonic archetypes across 6 suites.
- [`references/songcraft.md`](references/songcraft.md): Intake defaults, 9-dimension reference appeal map, 10-point originality delta, opt-in parody & lyric adaptation skeleton mapping, thesis & musical engine design, prosody/rhyme/phonetic hygiene, 6-anchor batch diversity, and diagnostic repair table.
- [`references/suno-controls.md`](references/suno-controls.md): Audited Suno v6 controls snapshot (2026-10-30), `v6` / `v6-wild` / `v6-mini` model selection, `Max Mode`, `Variety`, Duration/Weirdness/Style/Audio sliders, natural-language editing, multimodal & mashup rules, Custom Models, Voices, Suno Studio (Clip Settings, cent-level pitch, Auto-Stretch), 12-stem separation, live UI rules, and official links.
- [`references/controllable-song-research.md`](references/controllable-song-research.md): Controllable music generation research (`Mustango` `arXiv:2311.08355`, `JASCO` `arXiv:2406.10970`, `SongComposer` `arXiv:2402.17645`, `MusicRL` `arXiv:2402.04229`, `YuE` `arXiv:2503.08638`, `LeVo` `arXiv:2506.07520`, `SongEval` `arXiv:2505.10793`, `NegBench` `arXiv:2501.09425`) with paper findings separated from craft heuristics, plus v6 mode/slider starting ranges.
- [`scripts/prompt_lint.py`](scripts/prompt_lint.py): Standalone CLI linter and self-test suite checking `Style` length, inline negations, artist/producer name leaks, standalone `[Section]` tag formatting, and unexpanded digit strings in `Lyrics`.
- [`scripts/validate_coverage.py`](scripts/validate_coverage.py): Repository validator checking required files, frontmatter keys, routed links, all 83 numbered archetypes (`01`–`83`) across `68–174 BPM`, and zero artist-name leakage.
