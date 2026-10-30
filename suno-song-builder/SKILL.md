---
name: suno-song-builder
description: Create original song concepts, prosody-checked lyrics, instrumental film/game scores, paste-ready Suno v6 prompt packages (Title, Style, Lyrics, Exclude, v6/v6-wild/v6-mini Settings, Max Mode, Variety), natural-language edit commands, and A/B iteration plans from a user brief or reference audio/video. Invoke whenever the user asks to make a song, write or improve a Suno prompt, develop lyrics or hooks, score a film or short video, translate a reference track's appeal into an original song without copying it, diagnose generic or synthetic-sounding Suno output, produce multiple distinct song directions, or operate Suno directly when authorized.
---

# Suno Song Builder

Turn a user brief or reference into an original, production-aware Suno v6 song package. Treat Suno as a probabilistic composition and production engine—never as a uniqueness, copyright, or symbolic-MIDI guarantee.

## 1. Request Routing Decision Tree

Identify the primary deliverable and load only the required references:

| Deliverable Route | Scope & Output | Required Reference Loading |
| --- | --- | --- |
| **1. Complete Suno v6 Package** | Creative direction + paste-ready `Title`, `Style`, `Lyrics`/`Instrumental structure`, `Exclude`, `Settings` (`v6`/`v6-wild`/`v6-mini`, `Max Mode`, `Variety`, sliders), and `Iteration` plan | Read [`references/songcraft.md`](references/songcraft.md), [`references/suno-controls.md`](references/suno-controls.md), and [`references/controllable-song-research.md`](references/controllable-song-research.md). |
| **2. Concept, Lyrics, or Hook Only** | Premise, stressed-meter lyrics, open-vowel hook, and section tags | Read [`references/songcraft.md`](references/songcraft.md) and [`references/controllable-song-research.md`](references/controllable-song-research.md). |
| **3. Instrumental / Picture Score** | Through-composed or episodic dramatic cue with edit points, dropouts, and hero passage | Read [`references/songcraft.md`](references/songcraft.md) and [`references/suno-controls.md`](references/suno-controls.md). |
| **4. Reference Originality Translation** | Appeal map + $\ge$5-dimension ($\ge$7 for famous sources) originality delta + fresh Suno v6 package | Read [`references/songcraft.md`](references/songcraft.md). |
| **5. Render Diagnosis & Natural-Language Repair** | Single-variable A/B repair plan, v6 natural-language edit prompt, or Song Editor section replacement | Read [`references/songcraft.md`](references/songcraft.md), [`references/suno-controls.md`](references/suno-controls.md), and [`references/controllable-song-research.md`](references/controllable-song-research.md). |
| **6. Authorized Live Suno UI Operation** | Direct browser creation (1 batch default, private/link-only, zero purchases) | Read [`references/suno-controls.md`](references/suno-controls.md) and the active browser-control skill. |

Infer harmless defaults (`2:40–3:20` full song; `2:30–3:15` film cue with a `40–60s` hero passage; continuous v6 generation supports up to `8:00`) and ask at most one concise question only when a missing choice materially alters the work (e.g., vocal vs. instrumental when unresolved).

## 2. Deterministic Song Engineering Protocol

### Step 1: Write the Creative Thesis & Originality Delta
1. **One-Sentence Thesis**:
   `A [function] about [concrete physical situation/decision], moving from [emotional state A] to [state B], identified by [one audible relational signature rule].`
2. **Originality Enforcement (`references/songcraft.md`)**:
   - When working from a reference track, extract only abstract functional appeal (energy curve, pocket, ensemble relationship, mix space).
   - **Never** include an artist name, song title, copied lyric, or recognizable progression in any field.
   - Change **at least 5** identity-bearing dimensions (**at least 7** for famous/iconic sources): premise/title, hook phonetic shape, melodic contour, harmonic engine, groove/meter, section order, lead/counter-voice roles, signature sound event, recording space, and emotional resolution.
   - For multi-song batches, vary **all 6 anchors** (Premise, Hook shape, Groove, Harmony, Lead identity, Form) across every option.

### Step 2: Engineer the `Style` Field (`Mustango` `arXiv:2311.08355` & `MusicRL` `arXiv:2402.04229`)
Construct `Style` as a positive-only, music-theory-grounded studio brief ($\le$**1,000 characters** in Suno v6; obey any tighter user-supplied cap) following this exact 8-part sequence:
`[1. Function & target duration] -> [2. Primary genre lane + 1 contrast] -> [3. BPM/tempo feel, meter, & pocket] -> [4. Harmonic engine/mode] -> [5. Focal ensemble roles (2–3 core instruments + counter-voice)] -> [6. Vocal register, distance, & delivery (or instrumental lead)] -> [7. Section energy arc across >=3 states including subtraction] -> [8. Recording space, mix finish, & 1 signature rule]`

- **Focal Ensemble Rule (`arXiv:2402.04229`)**: Anchor around 2–3 primary instruments with relational verbs (`muted telecaster answers the vocal cadence; upright bass holds a pedal drone`) rather than a 10-instrument noun list that averages into mud.
- **Zero Inline Negations**: Keep `Style` 100% positive; move all unwanted sounds into `Exclude`.

### Step 3: Engineer `Lyrics` or `Instrumental Structure` (`SongComposer` `arXiv:2402.17645` & `LeVo` `arXiv:2506.07520`)
- **Prosodic Stress & Vowel Placement (`arXiv:2402.17645`)**: Keep `Lyrics` within the **5,000-character** v6 cap. Match stressed-beat counts across parallel verse lines, place open sustainable vowels (`ah`, `oh`, `ay`) on long hook notes, and cut syllable-crowded lines so vocals never rush.
- **Concrete Evidence Over AI Clichés**: Use tangible objects, places, actions, and interpersonal stakes; ban default AI filler (`neon shadows`, `echoes in the dark`, `ashes rising`, `scars`, `chains`, `destiny`) unless literally required by the brief.
- **Clean Section Tags (`arXiv:2506.07520`)**: Place concise structural tags (`[Cold Open | dry single voice]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus | drums drop out]`, `[Bridge]`, `[Outro]`) on their own lines with blank lines between sections. Keep production essays out of sung text.
- **Instrumental Cues**: Enable `Instrumental` and structure by dramatic state (`Establish Motif` $\rightarrow$ `Build Motion` $\rightarrow$ `Subtraction/Drop` $\rightarrow$ `Hero Passage` $\rightarrow$ `Edit Tail/Resolve`).

### Step 4: Populate `Exclude` & Calibrate Suno v6 Controls (`JASCO` `arXiv:2406.10970`)
- **`Exclude` Field**: Comma-separated list of unwanted audible traits only (e.g., `stock risers, trap hi-hat rolls, supersaws, four-chord pop loop, heavy autotune, stadium reverb, over-compressed master`).
- **Suno v6 Model & Mode Selection (`references/suno-controls.md`)**:
  - **`v6` (Flagship — Pro/Premier)**: Default for polished, reliable, genre-accurate production.
  - **`v6-wild` (Experimental — Pro/Premier)**: Recommend when the user wants bold, unpredictable textures or avant-garde motif discovery before converging in core `v6`.
  - **`v6-mini` (Fast/All Tiers)**: Recommend for free-tier users or rapid lyric/meter sketching.
  - **`Variety` (`Off / 0` vs. `On`)**: Set `Variety: Off (0)` in More Options when locking literal `Style` wording across controlled A/B takes; leave `On` for wider take-to-take variation.
  - **`Max Mode` (`2x` credits)**: Recommend enabling for arrangements longer than 2 minutes (up to 8 minutes), faithful covers, or strict style transfers requiring high vocal/structural continuity.
- **Slider Heuristics (`references/controllable-song-research.md`)**: Clearly label numeric slider suggestions as practical heuristics (e.g., Exploration: `Weirdness 45–65% / Style Influence 50–70%`; Convergence: `Weirdness 20–40% / Style Influence 75–90%`; Owned Audio Seed / Mashup: `Audio Influence 75–90%`, avoiding hard `100%` artifact transfer).

## 3. Mandatory 7-Block Delivery Schema

Deliver every complete package in this order, putting each paste-ready field in its own standalone fenced block (when the user requests easy copy/paste or one-at-a-time prompts, keep wrapper prose minimal):

1. **Creative direction**: 1 concise paragraph stating the thesis, signature rule, and originality delta.
2. **Title**:
   ```text
   [Original title]
   ```
3. **Style**:
   ```text
   [Positive-only 8-part production brief; <=1,000 characters in v6 and obeying any stricter user cap]
   ```
4. **Lyrics** (or **Instrumental structure**):
   ```text
   [Section-tagged lyrics (<=5,000 characters) or dramatic instrumental cue map]
   ```
5. **Exclude**:
   ```text
   [Comma-separated unwanted instruments, styles, vocal traits, and mix habits]
   ```
6. **Settings**: Model (`v6`, `v6-wild`, or `v6-mini`), Mode (`Custom`), `Instrumental` toggle state, `Duration` slider target (up to `8:00`), `Max Mode` recommendation (`On [2x credits]` vs. `Off`), `Variety` setting (`Off / 0` for literal style lock vs. `On`), and clearly labeled heuristic starting ranges for `Weirdness`, `Style Influence`, and (when using an owned audio/multimodal seed) `Audio Influence`.
7. **Iteration**: Controlled single-variable A/B loop, **v6 natural-language edit command** (for targeted lyric, vocal, or section swaps) + **Song Editor** section-replacement step, **Suno Studio** / 12-stem WAV export (with Auto-Stretch and semitone+cent fine pitch where useful), and post-lock **Remaster** guidance.

## 4. Verification Gate & Diagnostic Repair

Before delivery, verify:
- [ ] **Zero Artist/Title Leakage**: No living artist names, reference titles, or copied hooks appear in `Title`, `Style`, `Lyrics`, or `Exclude`.
- [ ] **v6 Cap & Dynamic Subtraction**: `Style` is $\le$1,000 chars, `Lyrics` is $\le$5,000 chars, and at least 3 distinct energy states are planned (including at least one moment of subtraction/dropout).
- [ ] **Prosody & Tag Hygiene**: Section tags sit on their own lines; verses use concrete physical imagery and natural spoken stress.
- [ ] **Evidence Honesty**: Settings distinguish official Suno v6 controls (`v6`/`v6-wild`/`v6-mini`, `Max Mode`, `Variety`, sliders) from practical numeric heuristics; un-auditioned audio is never described as heard or verified.

When repairing an existing Suno v6 render (`references/songcraft.md`), isolate the failure layer (`composition`, `arrangement`, `prosody`, `timbre`, `mix`, or `local section glitch`), preserve the winning seed/section, change **one variable per A/B batch** (with `Variety: Off`), and use **v6 natural-language editing** (e.g., *"Change the chorus arrangement to stripped upright bass and dry close harmony"* or *"Change the lyric in Verse 2 from X to Y"*) or **Song Editor** section replacement before regenerating the entire track.

### Do Not
- Do not upload or sample third-party music, film audio, or another person's voice in Suno (including in v6 mashups or multimodal prompts), or promise copyrightability, uniqueness, or detector evasion.
- Do not bury negative exclusions inside `Style` or `Lyrics` instead of using `Exclude`.
- Do not reskin the same chord loop and form across a multi-song batch.
- Do not purchase credits, change plans, enable `Max Mode` (`2x` credits) without user consent, or publish songs publicly when operating the live Suno UI.

## 5. Resource Index

- [`references/songcraft.md`](references/songcraft.md): Intake defaults, 9-dimension reference appeal map, 10-point originality delta, thesis & musical engine design, prosody checks, 6-anchor batch diversity, and diagnostic repair table.
- [`references/suno-controls.md`](references/suno-controls.md): Audited Suno v6 controls snapshot (2026-10-30), `v6` / `v6-wild` / `v6-mini` model selection, `Max Mode`, `Variety`, Duration/Weirdness/Style/Audio sliders, natural-language editing, multimodal & mashup rules, Custom Models, Voices, Suno Studio (Clip Settings, cent-level pitch, Auto-Stretch), 12-stem separation, live UI rules, and official links.
- [`references/controllable-song-research.md`](references/controllable-song-research.md): Controllable music generation research (`Mustango` `arXiv:2311.08355`, `JASCO` `arXiv:2406.10970`, `SongComposer` `arXiv:2402.17645`, `MusicRL` `arXiv:2402.04229`, `YuE` `arXiv:2503.08638`, `LeVo` `arXiv:2506.07520`) and CFG/v6 mode/slider mechanics.
