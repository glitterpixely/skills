# Source coverage and authority

Use this ledger before asserting time-sensitive facts. Last audited: 2026-08-13.

## Authority order

Prefer, in order:

1. The live documentation for the exact selected surface.
2. The released checkpoint files, model card, and license.
3. MiniMax's provider-authored caption skill and examples.
4. The launch article for model intent and architecture.
5. Clearly labeled practical inference.

When two first-party sources conflict, preserve the discrepancy in internal reasoning and use the artifact closest to the actual runtime. Do not silently merge schemas.

## Source inventory

| ID | Source | Owns these claims | Drift risk |
|---|---|---|---|
| `BLOG` | <https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model> | launch date, five-minute positioning, architecture, Structured Caption intent, audio-quality claims, examples | Low for historical text; medium for product claims |
| `GH` | <https://github.com/MiniMax-AI/MiniMax-Music3> | official release repository, official prompt skill, model overview | High; launch-day README already trails newer runtime guidance |
| `HF` | <https://huggingface.co/MiniMaxAI/MiniMax-Music3> | released checkpoint identifier, local surfaces, current examples, limitations, Diffusers guidance | High |
| `LICENSE` | <https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE> | open-weight license and AUP terms | High and legally consequential; quote current text rather than this summary |
| `HOSTED-GUIDE` | <https://platform.minimax.io/docs/guides/music-generation> | hosted workflows, instrumental and automatic lyrics, cover overview | High |
| `HOSTED-MUSIC` | <https://platform.minimax.io/docs/api-reference/music-generation> | hosted field schema, limits, formats, model IDs, rates | High |
| `HOSTED-LYRICS` | <https://platform.minimax.io/docs/api-reference/lyrics-generation> | lyric modes, limits, output tags | High |
| `HOSTED-COVER` | <https://platform.minimax.io/docs/api-reference/music-cover-preprocess> | cover preprocessing and feature-ID workflow | High |
| `PRICING` | <https://platform.minimax.io/docs/guides/pricing-paygo#music> | current hosted prices | Very high; always refresh |
| `RELEASES` | <https://platform.minimax.io/docs/release-notes/models> | hosted model release history | Medium |
| `SGLANG` | <https://sgl-project.github.io/sglang-omni/cookbook/minimax_music3.html> | SGLang setup, fields, frame math, seed, rejected controls, 32 kHz output | Very high; new integration |
| `DIFFUSERS` | <https://github.com/huggingface/diffusers/blob/minimax-music3-integration/docs/source/en/api/pipelines/minimax_music3.md> | modular pipeline call, memory guidance, native 44.1 kHz, experimental tuning | Very high while PR is open |
| `COMFY` | <https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3> | native workflow, files, controls, tiled decode, saved output | Very high; nightly/stable lag |
| `DEMO` | <https://minimax-ai.github.io/music3-demo/> | provider examples and caption patterns | Medium |

## Claim ledger

| Claim | Authority | Skill location |
|---|---|---|
| Up to five-minute complete songs | `BLOG`, `HF`, `COMFY` | `model-contract.md`, `SKILL.md` |
| Caption plus separate tagged lyrics | `BLOG`, `HF`, official skill | `SKILL.md`, `prompt-architecture.md` |
| Three-part Structured Caption | `HF`, official skill | `SKILL.md`, `prompt-architecture.md` |
| 8B global, 0.6B local, 2.4B flow, 123M decoder | `BLOG`, `HF` | `model-contract.md` |
| 16,384 plus seven 1,024 RVQ codebooks | `BLOG`, `HF` | `model-contract.md` |
| Qwen base discrepancy | `BLOG` versus `HF`, `LICENSE`, released files | `model-contract.md` |
| Hosted 2,000-character prompt and 3,500-character lyrics | `HOSTED-MUSIC` | `runtime-surfaces.md`, linter |
| Hosted instrumental and lyric optimizer flags | `HOSTED-MUSIC` | `runtime-surfaces.md`, linter |
| Hosted streaming and URL expiry | `HOSTED-MUSIC` | `runtime-surfaces.md` |
| Hosted covers use separate model | `HOSTED-GUIDE`, `HOSTED-MUSIC`, `HOSTED-COVER` | `runtime-surfaces.md` |
| SGLang 25 frames/second and 9,000 cap | `SGLANG`, `HF` | `runtime-surfaces.md`, linter |
| SGLang fixed seed 0 and deterministic exact request | `SGLANG` | `runtime-surfaces.md` |
| Local tags must be alone on lines | `SGLANG`, `DIFFUSERS`, `HF` | all prompting guidance, linter |
| Diffusers BF16/offload memory guidance | `HF`, `DIFFUSERS` | `runtime-surfaces.md` |
| ComfyUI duration, seed, tiled decode | `COMFY` | `runtime-surfaces.md` |
| License display, revenue authorization, safeguards, AUP | `LICENSE` | `model-contract.md` |

## Known conflicts and chosen handling

| Conflict | Handling |
|---|---|
| Blog says Qwen3.5-8B; released artifacts say Qwen3-8B | Describe the open checkpoint as Qwen3-family/Qwen3-8B and flag the blog discrepancy in technical reports |
| Product says five minutes; local frame ceiling equals six | Recommend no more than five minutes; label 9,000 frames as an implementation ceiling only |
| GitHub launch README says two GPUs; current SGLang supports one or two | Follow current SGLang docs and avoid a universal GPU-fit promise |
| General model material says 32 kHz; Diffusers returns 44.1 kHz | State output by runtime surface |
| Hosted API streams; open checkpoint does not | Never transfer hosted streaming to local requests |
| Hosted instrumental omits lyrics; local requires non-empty lyrics | Use the surface-specific approach |
| Hosted and local tag lists differ | Use portable core tags by default; use exact surface spellings when necessary |
| Official caption skill defaults to 250–450 words; hosted prompt caps at 2,000 characters | Compose full local captions; compress and character-count hosted captions |
| Hosted output URL appears in guide but formal response schema emphasizes hex audio | Follow the documented request option and handle either response form without claiming the schema is perfectly aligned |

## Facts requiring live refresh

Browse or fetch the current primary source before answering about:

- API pricing, free-tier availability, RPM, or quotas
- current Diffusers installation commit or whether its PR merged
- SGLang installation pins, supported releases, or hardware requirements
- ComfyUI model filenames, stable/nightly availability, or workflow controls
- model-card limits or new modalities
- license or AUP terms
- hosted terms of service or ownership wording
- current CLI model support

## Unsupported claims

Do not assert these without new primary evidence:

- exhaustive supported-language list or count
- a quality, preference, MOS, FAD, CLAP, or adherence benchmark
- render speed on ordinary consumer hardware
- minimum VRAM for SGLang or ComfyUI
- stem output, inpainting, extension, continuation, or local reference-audio conditioning
- copyrightability, royalty-free status, non-infringement, or commercial clearance of outputs
- training-data provenance or memorization guarantees
- exact BPM, key, lyrics, pronunciation, or arrangement adherence
- waveform identity across SGLang, Diffusers, ComfyUI, or hosted surfaces for the same numeric seed

## Vendored official prompt library

Source: <https://github.com/MiniMax-AI/MiniMax-Music3/tree/main/skills/music-caption-rewriter>

Vendored snapshot:

- Git commit: `91410fb657c007ae57c60df8240f5ece5be089c7`
- 18 family indexes plus `genre-router.md`
- 1,000 complete caption templates

The release repository has no root license file as of this audit, although its README links the checkpoint's Hugging Face Community License. Do not independently label the prompt-template library MIT or Apache. Preserve provenance, avoid bulk reproduction in user output, and refresh from the official repository when updating the skill.
