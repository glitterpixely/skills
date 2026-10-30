# MiniMax Music 3.0 & Full-Song Generation Research

Use this reference to ground section structure, lyric-length budgeting, vocal/accompaniment clarity and listening review. Provider facts stay in [`model-contract.md`](model-contract.md) and [`runtime-surfaces.md`](runtime-surfaces.md).

Citations were checked against the arXiv API on 2026-10-30. Each table separates what a paper reports from the prompt rule this skill derives from it. A derived rule is a heuristic, not a result the paper measured on MiniMax Music 3.0.

## 1. Architecture facts used here

From [`model-contract.md`](model-contract.md): an 8-layer RVQ representation (one 16,384-entry semantic codebook, seven 1,024-entry acoustic codebooks); an 8B Global LLM that predicts the semantic layer frame by frame and carries full-song structure; a 0.6B Local LLM for within-frame acoustic layers; a 2.4B flow-matching module conditioned on both LLMs' hidden states; a 123M audio decoder. SGLang caps generation at 9,000 frames at 25 frames per second (6 minutes). The advertised creative target is up to 5 minutes. The backbone is named Qwen3.5-8B in the launch blog and Qwen3-8B in the license; see the contract for the discrepancy.

`model-contract.md` warns: *do not use the architecture description as a prompt recipe.* Users control the caption, lyrics, length and seed, not tokens. The architecture explains two things only:

- **Frame budget.** Length is counted in 25 fps frames on local runtimes: `frames = seconds × 25` (180 s = 4,500 frames).
- **Structure is carried by the Global LLM.** Section order in `Arrangement` should match the section tags in `Lyrics`, so text and lyrics describe the same timeline.

## 2. Full-song generation literature

| Paper | arXiv ID | What the paper reports | Derived rule for Music 3.0 (heuristic) |
| --- | --- | --- | --- |
| **YuE** | [`2503.08638`](https://arxiv.org/abs/2503.08638) | Lyrics-to-song up to 5 minutes using (1) track-decoupled next-token prediction to handle dense vocal+accompaniment mixtures and (2) structural progressive conditioning for long-context lyric alignment. | Give each section its own instrumental change (what enters, drops out, shifts register). In dense arrangements, leave room for the lead vocal in `Arrangement` and state its projection in `Vocal Details`. |
| **DiffRhythm** | [`2503.01183`](https://arxiv.org/abs/2503.01183) | Latent-diffusion full-song model (vocals + accompaniment, up to 4m45s) that needs only lyrics and a style prompt at inference. | Lyrics and style are separate inputs in this model family too. Size the lyric sheet to the target length before changing other variables. |
| **DiffRhythm+** | [`2507.12890`](https://arxiv.org/abs/2507.12890) | A larger, balanced training set reduces **repetition and omission of lyrics**; adds text + reference-audio style conditioning and preference optimization. | Lyric omission and repetition are known failure modes of full-song generators. When a line is skipped or doubled, first check the line length and the tag line, then reroll with the same seed policy. |
| **SongGen** | [`2502.13128`](https://arxiv.org/abs/2502.13128) | Single-stage autoregressive text-to-song model taking lyrics and a text description (instrumentation, genre, mood, timbre) as separate controls; mixed and dual-track output modes. | Keep sonic direction in the `Caption` and sung words in `Lyrics`. |
| **LeVo** | [`2506.07520`](https://arxiv.org/abs/2506.07520) | Models mixed tokens (vocal-instrument harmony) and dual-track tokens (separate vocal and accompaniment quality) in parallel; DPO-based multi-preference alignment improves musicality and instruction following. | Describe how voice and accompaniment relate (`piano leaves space under the verse vocal; strings answer the chorus line`), not only lists of instruments. |
| **SongEval** | [`2505.10793`](https://arxiv.org/abs/2505.10793) | 2,399 full songs rated by 16 professional annotators on five dimensions: overall coherence, memorability, naturalness of vocal breathing and phrasing, clarity of song structure, overall musicality. | Use these five dimensions as the listening checklist when comparing takes. Fix the weakest dimension first. |

**Tag-line rule source:** the rule "put each section tag alone on its own line" comes from SGLang/Diffusers lyric normalization, which drops text on the tag line without warning ([`prompt-architecture.md`](prompt-architecture.md)). It is a provider runtime fact, not a research finding.

## 3. Duration diagnostics (inferred from the frame cap)

- **Track ends cleanly before `audio_duration` / `max_new_tokens`:** the model likely finished the lyric sheet. Add an `[Instrumental]`, `[Bridge]`, repeated `[Chorus]` or `[Outro]` section.
- **Track cuts off mid-phrase exactly at the cap:** the cap was reached. Raise `max_new_tokens` / `audio_duration` or remove lyric lines before you change the seed.
- **Lyric density:** about 6–11 syllables per verse line, with shorter, open-vowel hook lines, is a songwriting heuristic for singable phrasing. No paper in this table measured it.
