# Controllable Song Generation Research & Conditioning Heuristics

Use this reference to ground Suno v6 `Style` construction, `Exclude` use, lyric prosody, audio-seed anchoring, listening review and slider heuristics. Suno controls and terms stay in [`suno-controls.md`](suno-controls.md).

Citations were checked against the arXiv API on 2026-10-30. Suno's model is unpublished; none of these papers describe Suno internals. Each table separates what a paper reports from the prompt rule this skill derives from it. A derived rule is a heuristic, not a measured result.

## 1. Research behind the prompting rules

| Paper | arXiv ID | What the paper reports | Derived rule for Suno packages (heuristic) |
| --- | --- | --- | --- |
| **Mustango** | [`2311.08355`](https://arxiv.org/abs/2311.08355) | A music-domain-knowledge-informed guidance module (MuNet) lets text captions control chords, beats, tempo and key; the MusicBench dataset adds music-theory descriptions to captions. | Prefer concrete musical descriptors (`112 BPM swung 16ths, Dorian vamp, palm-muted guitar answers the vocal`) over mood adjectives (`epic`, `emotional`). |
| **MusicRL** | [`2402.04229`](https://arxiv.org/abs/2402.04229) | First text-to-music model fine-tuned from human feedback (300,000 pairwise preferences). Captions are user-dependent: "upbeat work-out music" can mean a retro guitar solo or a techno-pop beat. Rewards target text adherence and audio quality. | An ambiguous caption leaves the model to choose. Name the genre lane, groove and lead instrument so your intent is not one of several valid readings. |
| **JASCO** | [`2406.10970`](https://arxiv.org/abs/2406.10970) | Flow-matching text-to-music with global text plus local symbolic or audio controls (chords, melody, separated drums, full mix), using information bottlenecks and temporal blurring to extract only control-relevant information. | An audio seed is a structural control, not a style. Use `Audio Influence` to lock motif or rhythm, and let `Style` describe the target finish. Not paper-backed: avoiding 100% Audio Influence to keep scratch-take noise out is a practical heuristic. |
| **SongComposer** | [`2402.17645`](https://arxiv.org/abs/2402.17645) | Symbolic lyric+melody LLM using a word-level tuple format for lyric–note alignment, and a motif-to-phrase training pipeline for structure. | Lyrics and melody are aligned word by word, so each line's stress pattern shapes the melody. The specific prosody rules in this skill (matched stressed-beat counts, open vowels on long notes) are songwriting craft, not results from this paper. |
| **YuE** | [`2503.08638`](https://arxiv.org/abs/2503.08638) | Lyrics-to-song up to 5 minutes using track-decoupled prediction for dense mixes and structural progressive conditioning over section-segmented lyrics. | Use concise section tags on their own lines and give each section a different energy state, including at least one subtraction. |
| **LeVo** | [`2506.07520`](https://arxiv.org/abs/2506.07520) | Models mixed tokens (vocal-instrument harmony) and dual-track tokens in parallel; DPO multi-preference alignment improves musicality and instruction following. | Describe how voice and accompaniment relate (`bass holds a pedal under the verse; strings answer the chorus`) rather than listing instruments. |
| **SongEval** | [`2505.10793`](https://arxiv.org/abs/2505.10793) | 2,399 full songs rated by 16 professional annotators on five dimensions: overall coherence, memorability, naturalness of vocal breathing and phrasing, clarity of song structure, overall musicality. | Use these five dimensions when choosing between takes; repair the weakest one first. |
| **NegBench** | [`2501.09425`](https://arxiv.org/abs/2501.09425) | Vision-language models often handle negated captions at chance level. | Text-audio encoders are likely to share this weakness (analogy, not measured for audio). Keep `Style` positive and put unwanted sounds in `Exclude`. |

**Focal-ensemble rule (craft heuristic, no paper):** anchor `Style` on one genre lane plus one contrast and 2–3 focal instruments with roles (`lead`, `counter-voice`, `low end`). Long instrument lists tend to blur in practice; no paper above measured this.

## 2. `Style` vs. `Exclude`

- **Positive `Style` field:** only the audible traits you want: function, genre lane and contrast, tempo and groove, harmony, focal instrument roles, vocal delivery, section energy arc, mix space, one signature rule.
- **`Exclude` field:** unwanted sounds (`stock EDM risers, trap hi-hat rolls, supersaws, heavy autotune, four-chord pop loop, stadium reverb`). Do not write `no drums` inside `Style` (NegBench analogy above).

## 3. Suno v6 model, mode and slider heuristics

Official Suno sources define what `v6`, `v6-wild`, `v6-mini`, `Max Mode` and `Variety` do (see [`suno-controls.md`](suno-controls.md)). Every number below is a starting heuristic, not a provider value.

| Iteration Phase | v6 Model & Mode | Weirdness | Style Influence | Audio Influence | Rationale |
| --- | --- | --- | --- | --- | --- |
| **1. Prosody / form sketch** | **`v6-mini`** (all users) | `35%–50%` | `60%–75%` | N/A | Check lyric stress, syllable density and section timing cheaply before paid-model renders. |
| **2. Motif exploration** | **`v6-wild`** (Pro/Premier), `Variety` above 0 | `45%–65%` | `50%–70%` | N/A (or `40%–60%`) | Suno describes `v6-wild` as less predictable and more varied; use it to find hooks and textures. |
| **3. Controlled text convergence** | **`v6`**, `Variety: 0` | `20%–40%` | `75%–90%` | N/A | Suno: `Variety: 0` keeps full control of your style tags. Change one variable per A/B batch. |
| **4. Long-form (>2 min), cover, or owned-seed lock** | **`v6`** + **`Max Mode`** (extra credits), `Variety: 0` | `15%–35%` | `70%–85%` | `75%–90%`, avoid `100%` | Suno recommends Max Mode for songs over two minutes, close covers, style transfer, and consistent vocals; the Audio Influence range is a heuristic. |
