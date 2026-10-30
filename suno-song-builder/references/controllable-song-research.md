# Controllable Song Generation Research & Conditioning Mechanics

Use this reference to ground Suno `Style` construction, negative `Exclude` filtering, prosodic lyric-to-melody alignment, audio-seed anchoring, and slider iteration heuristics in peer-reviewed controllable music generation research. Provider-specific controls and terms remain governed by [`suno-controls.md`](suno-controls.md).

## 1. Peer-Reviewed Foundations for Controllable Song Prompting

| Paper | arXiv ID | Core Mechanism | Deterministic Rule for Suno Packages |
| --- | --- | --- | --- |
| **Mustango** (*Toward Controllable Text-to-Music Generation*) | [`2311.08355`](https://arxiv.org/abs/2311.08355) | Music-Domain-Knowledge-Informed UNet guidance (`MuNet`) trained on `MusicBench` shows that explicit music-theory descriptors (tempo/BPM, meter feel, harmonic mode/tension, beat subdivision, and lead/accompaniment role assignment) steer generation far more reliably than subjective mood adjectives. | Replace abstract mood adjectives (`emotional`, `epic`, `magical`) in `Style` with concrete music-theory and role relationships (`112 BPM swung 16th pocket, Dorian pedal bass, muted palm-picked telecaster answering the vocal phrase`). |
| **JASCO** (*Joint Audio and Symbolic Conditioning for Temporally Controlled Text-to-Music Generation*) | [`2406.10970`](https://arxiv.org/abs/2406.10970) | Flow-matching with information bottleneck layers and temporal blurring combines global text conditioning with local time-varying audio/harmonic seeds (drums, chords, or stems); over-tight audio bottleneck weights copy source compression and room artifacts alongside structure. | When conditioning on an owned Audio Upload or Voice seed, keep `Audio Influence` strong enough to lock motif/timbre without over-indexing on room noise or scratch-take artifacts, and let `Style` specify the target studio finish. |
| **SongComposer** (*LLM for Lyric and Melody Composition*) | [`2402.17645`](https://arxiv.org/abs/2402.17645) | Word-to-note tuple modeling across motif-to-phrase hierarchies demonstrates that lyric prosody (syllable count symmetry, natural lexical stress on downbeats, and open vowels on sustained cadences) directly governs melodic contour stability. | Write parallel verse lines with matched stressed-beat counts (even when total syllable counts vary slightly), place open vowels (`ah`, `oh`, `ay`) on held hook syllables, and insert explicit breath breaks via line breaks. |
| **MusicRL** (*Aligning Music Generation to Human Preferences*) | [`2402.04229`](https://arxiv.org/abs/2402.04229) | RLHF post-training on text-to-music models reveals a systematic failure mode where dense multi-genre/multi-instrument wish-lists collapse toward a muddy, over-compressed "average" mix unless primary timbral anchors are constrained. | **Focal Ensemble Rule**: Anchor `Style` around **1 primary genre lane + 1 contrast** and **2–3 focal instruments** with explicit relational roles (`lead`, `counter-voice`, `rhythm/low-end`), rather than listing 8+ competing instruments. |
| **YuE** & **LeVo** (*Long-Form & Multi-Preference Song Alignment*) | [`2503.08638`](https://arxiv.org/abs/2503.08638), [`2506.07520`](https://arxiv.org/abs/2506.07520) | Structural progressive conditioning and isolated section delimiters (`[Verse]`, `[Chorus]`, `[Bridge]`) prevent multi-minute arrangement flattening and keep production meta-text out of the sung phoneme stream. | Keep section brackets concise (`[Verse 1 | dry vocal & bass]`, `[Chorus | full drums enter]`), never put long prose sentences inside `Lyrics`, and enforce at least **3 distinct energy states** across the arrangement (including subtraction/dropouts). |

## 2. Classifier-Free Guidance (CFG) & Negative Space (`Style` vs. `Exclude`)

In joint text-audio embedding spaces (CLAP/MuLan-class encoders), inline negations inside the positive prompt (`"no drums, not synthwave"` inside `Style`) often activate the very token embeddings you want to suppress.
- **Positive `Style` Field**: Include **only** desired audible traits (function, genre lane + contrast, tempo/groove, harmonic behavior, focal instrument roles, vocal mechanics, section dynamic arc, mix space, and 1 signature rule).
- **Negative `Exclude` Field**: Offload all suppressed tokens (`stock EDM risers, trap hi-hat rolls, supersaws, heavy autotune, four-chord pop loop, stadium reverb`) into the dedicated `Exclude` box so negative guidance steers away from those regions cleanly.

## 3. Practical Slider Regime Heuristics (Non-Universal Starting Points)

Official Suno documentation defines the function of `Weirdness`, `Style Influence`, and `Audio Influence`; any numeric percentage is an **iteration heuristic**, not a provider guarantee:

| Iteration Phase | Weirdness Heuristic | Style Influence Heuristic | Audio Influence Heuristic | Rationale |
| --- | --- | --- | --- | --- |
| **1. Motif / Form Exploration** | Moderate–High (`40%–65%`) | Moderate (`50%–70%`) | N/A (or Low–Mod `40%–60%`) | Widens sampling entropy to discover non-default melodic contours and section transitions. |
| **2. Text-Only Convergence** | Low–Moderate (`20%–40%`) | High (`75%–90%`) | N/A | Tightens adherence to the curated `Style` ensemble and `Exclude` boundaries while avoiding glitch chaos (`>80%` Weirdness). |
| **3. Owned Audio-Seed Lock** | Low (`15%–35%`) | High (`70%–85%`) | High (`75%–90%`, avoid hard `100%`) | Locks the uploaded chord loop, tapped rhythm, or hummed motif (`arXiv:2406.10970`) without cloning scratch-recording artifacts. |
