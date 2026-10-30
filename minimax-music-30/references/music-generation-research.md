# MiniMax Music 3.0 Architecture & Full-Song Generation Research

Use this reference to ground section-tag formatting, syllable-to-frame budgeting, vocal-accompaniment separation, and long-form arrangement progression in MiniMax Music 3.0's Hybrid-LM + Flow-Matching stack and peer-reviewed full-song generation literature.

## 1. MiniMax Music 3.0 Hybrid-LM + Flow-Matching Stack

| Architectural Stage | Mechanism | Deterministic Prompting Consequence |
| --- | --- | --- |
| **Global Autoregressive LLM (`Qwen3-8B` / `Qwen3.5-8B`)** | Models macro musical form, phrase boundaries, harmonic progression, and vocal phrasing at **25 frames per second (fps)** (`max_new_tokens` $\le$ 9,000 frames = 6 min implementation ceiling; 5 min creative target) by predicting Layer-1 semantic RVQ tokens from `Caption` + `Lyrics`. | The `Arrangement` section of the Caption must follow the exact chronological section order used in `Lyrics` (`[Intro]` $\rightarrow$ `[Verse]` $\rightarrow$ `[Chorus]`, etc.) so global attention aligns text instructions with lyric section delimiters. |
| **Local Depth LLM (0.6B) + 8-Layer RVQ** | Refines Layers 2–8 residual acoustic tokens along the depth axis at each 25 fps timestep to capture vocal timbre, articulation transients, and instrument micro-dynamics. | Specific, non-contradictory timbre and articulation descriptors in `Vocal Details` (register, breathiness, vibrato restraint) directly condition the depth transformer without needing inline stage essays inside the lyrics. |
| **Flow-Matching DiT + Flow-VAE Decoder** | Maps discrete/hidden token states into continuous audio latents via Flow Matching before waveform reconstruction (32 kHz stereo in SGLang-Omni; 44.1 kHz stereo in Diffusers). | Continuous flow-matching preserves stereo width and timbral sheen across 5-minute spans only when simultaneous instrument density is managed; overcrowded captions produce midrange masking. |

## 2. Full-Song Generation Literature & Failure Mitigations

| Paper | arXiv ID | Core Finding | Deterministic Rule for Music 3.0 |
| --- | --- | --- | --- |
| **YuE** (*Scaling Open Foundation Models for Long-Form Music Generation*) | [`2503.08638`](https://arxiv.org/abs/2503.08638) | Long-form (up to 5 min) lyrics-to-song generation requires **Structural Progressive Conditioning** and **Track-Decoupled Prediction** to prevent vocal-accompaniment masking in dense genres (metal, heavy rock, EDM) and section drift over multi-minute spans. | 1. Give every section in `Arrangement` a distinct instrumental delta (what enters, drops out, or shifts octave).<br>2. In dense genres, explicitly carve midrange space for the lead vocal in `Arrangement` and specify clear chest/belting projection in `Vocal Details`. |
| **DiffRhythm** & **DiffRhythm 2** | [`2503.01183`](https://arxiv.org/abs/2503.01183), [`2507.12890`](https://arxiv.org/abs/2507.12890) | Full-length song alignment between sparse/dense lyrics and acoustic frames breaks when syllable density mismatches tempo or when instrumental spans lack explicit structural anchors. | Budget lyric syllable count to tempo and frame cap ($\text{frames} = \text{seconds} \times 25$): keep verses around 6–11 stressed syllables per line and hooks shorter/more open-voweled so the 25 fps token stream neither rushes phrases nor emits `<EOS>` prematurely. |
| **SongGen** | [`2502.13128`](https://arxiv.org/abs/2502.13128) | Single-stage autoregressive text-to-song transformers require strict separation between global style/timbre descriptors and phonetic lyric tokens to prevent prompt words from being sung. | Never place production notes, instrument instructions, or long parenthetical descriptions inside the `Lyrics` input; keep all sonic direction in the three-part `Caption`. |
| **LeVo** (*High-Quality Song Generation with Multi-Preference Alignment*) | [`2506.07520`](https://arxiv.org/abs/2506.07520) | Explicit newline-isolated structural tags (`[Verse]`, `[Chorus]`, `[Bridge]`) act as hard attention reset anchors between mixed global structure tokens and fine vocal fidelity tokens. | Place every `[Section]` tag strictly alone on its own line with blank lines between sections; sharing a line between `[Chorus]` and sung words corrupts section-boundary detection. |

## 3. Quantitative Duration & Prosody Heuristics

- **25 FPS Frame Budget (Local Runtimes)**:
  $$\text{Target Frames} = \text{Target Seconds} \times 25 \quad (\text{e.g., } 180\text{s} = 4,500\text{ frames}; \text{hard cap } 9,000\text{ frames} = 360\text{s})$$
- **Early `<EOS>` vs. Frame-Cap Truncation Diagnostic**:
  - If a generated track ends cleanly *before* `audio_duration` / `max_new_tokens`, the Global LLM exhausted the lyric tokens and emitted `<EOS>`: add an `[Instrumental]`, `[Bridge]`, or additional `[Chorus]`/`[Outro]` section.
  - If a track cuts off mid-phrase *at* the exact time cap, raise `max_new_tokens` / `audio_duration` or trim lyric line count before changing the seed.
