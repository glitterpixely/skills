# MiniMax Music 3.0 model contract

Use this reference for capability, architecture, limitation, and license claims. Facts are sourced as of 2026-08-13. Recheck the live sources before making current availability, pricing, rate-limit, installation, or legal claims.

## Capability boundary

MiniMax describes Music 3.0 as a complete-song generator conditioned on a creative music description and optional lyrics at the product level. It composes, arranges, performs, and produces a song in one generation. The open-weight checkpoint and its common local runtimes expose the same two concepts as separate fields and generally require both fields to be non-empty.

Verified model-level capabilities:

- complete-song generation with an advertised target of up to five minutes
- vocal or instrumental output
- lyrics with section tags for macrostructure
- a detailed music description for genre, tempo, meter, key, emotion, use case, vocal performance, instrumentation, arrangement, groove, effects, and production character
- section-aware changes in emotion, instruments, rhythm, low end, vocal delivery, harmony, and effects
- long-range modeling intended to maintain themes, rhythm, vocal identity, and arrangement progression
- generated tempo, key, instrumentation, lyrics, and structure remain probabilistic controls, not symbolic guarantees

Do not invent an official language list. The launch materials demonstrate English and Chinese songs, but the reviewed primary sources do not publish a closed set of supported lyric languages.

## Provider-recommended prompt representation

Use two inputs:

1. `Lyrics`: words to sing plus bracketed section tags.
2. `Music description` or `Caption`: the musical direction.

For precision, MiniMax recommends a Structured Caption with:

- `Global Metadata`: genre, subgenre, BPM, key, scale, emotional progression, listening scenario, and production profile
- `Vocal Details`: lead configuration, gender, timbre, register, delivery, harmony, backing vocals, and vocal effects
- `Arrangement`: primary and secondary instruments, section-level evolution, groove, bass, percussion, textures, and spatial effects

The bundled genre router, 18 family indexes, and 1,000 complete caption templates were vendored from MiniMax's official `music-caption-rewriter` skill at GitHub commit `91410fb657c007ae57c60df8240f5ece5be089c7`.

## Architecture

The open checkpoint is a hierarchical autoregressive-plus-flow system:

- an eight-layer Residual Vector Quantization representation separates musical semantics from residual acoustic detail
- the first semantic codebook contains 16,384 entries
- the remaining seven acoustic codebooks contain 1,024 entries each
- an 8B Global LLM predicts the semantic layer frame by frame and carries full-song structure
- a 0.6B Local LLM predicts within-frame acoustic layers
- continuous hidden states from both language models condition a 2.4B flow-matching module
- a 123M decoder reconstructs final audio from the generated latent representation

The intended synthesis path is:

```text
Global and Local LLM hidden states
                -> hidden-state fusion
                -> flow matching
                -> VAE latent
                -> audio decoder
                -> stereo waveform
```

Do not use the architecture description as a prompt recipe. Users control lyrics, the caption, length, and any surface-exposed seed; they do not directly author RVQ tokens or hidden states.

## Output differs by runtime

Do not state one sample rate for every surface:

| Surface | Verified output behavior |
|---|---|
| Hosted MiniMax API | User-selectable 16, 24, 32, or 44.1 kHz; MP3, WAV, or PCM; supported bitrates depend on the API field |
| SGLang-Omni reference server | 32 kHz, 16-bit stereo WAV |
| Diffusers modular pipeline | Native 44.1 kHz stereo; the SGLang reference path separately resamples to 32 kHz |
| Native ComfyUI example | Documentation describes 32 kHz stereo saved through the workflow as MP3 |

## Duration boundary

The product blog, model card, and ComfyUI guide advertise songs up to five minutes or about 300 seconds.

The local SGLang contract exposes `max_new_tokens` as a cap of at most 9,000 audio frames at 25 frames per second, mathematically six minutes. Treat this as a runtime ceiling, not a revised promise of six-minute musical coherence. The model may emit an end token and stop before either limit.

The Diffusers and ComfyUI surfaces expose time in seconds. Treat requested duration as an upper bound rather than an exact ending time.

## Known source discrepancies

Keep these discrepancies visible instead of silently choosing whichever value is convenient:

1. **Backbone name**: the launch blog says the 8B Global LLM is initialized from Qwen3.5-8B. The open checkpoint's model card, repository paths, and Community License identify Qwen3-8B. For the released open checkpoint, use Qwen3-8B unless MiniMax updates the checkpoint artifacts.
2. **Maximum duration**: model-facing sources advertise five minutes; the SGLang frame limit can represent six minutes. Use five minutes as the creative product claim and 9,000 frames only as the local implementation ceiling.
3. **Sample rate**: the top-level open model materials emphasize 32 kHz output, while Diffusers documents a native 44.1 kHz vocoder output and says the reference server resamples it to 32 kHz. State the selected surface.
4. **Section tag spelling**: the hosted music endpoint, hosted lyrics endpoint, open model card, and local runtimes show overlapping but non-identical spellings. Use the portable core or the exact selected-surface contract in [prompt-architecture.md](prompt-architecture.md).
5. **GPU topology**: the initial GitHub README describes two CUDA GPUs, while the current SGLang cookbook documents both single-GPU colocation and dual-GPU placement. Say CUDA is required and select a current supported topology from the runtime documentation; do not promise that an unspecified GPU will fit.

## Limitations

Verified open-weight limitations:

- CUDA is required by the documented local paths.
- Generation is externally non-streaming in the open model contract.
- The combined tokenized text prompt is capped at 5,000 tokens.
- SGLang audio generation is capped at 9,000 acoustic frames.
- Exact tempo, key, instrumentation, wording, pronunciation, and section structure can drift.
- A fixed seed can reproduce a request only when all text, whitespace, parameters, model files, and runtime behavior remain identical.

Do not claim an exact render speed, exact SGLang VRAM minimum, supported operating system matrix, training-data provenance, copyright clearance, or guaranteed vocal-language support unless a current primary source establishes it.

## License boundary

The checkpoint is distributed under the `MiniMax-Music3 COMMUNITY LICENSE`, not an OSI-standard permissive license.

Operationally important terms in the published license include:

- retain the copyright and permission notice in copies or substantial portions
- comply with law, trade rules, the Acceptable Use Policy, and third-party intellectual-property rights
- prominently display `MiniMax-Music3` in a commercial product or service that uses the Software
- obtain separate prior written authorization from MiniMax if aggregate yearly revenue from relevant products or services by the user or affiliates exceeds USD 20 million
- maintain reasonable safeguards for third-party generation products or hosted services
- comply with the listed prohibited-use categories

The license says the checkpoint was fine-tuned from Qwen3-8B under Apache-2.0, with parts modified from MIT-licensed Stable Audio and DAC code. Those upstream licenses do not replace the MiniMax-Music3 Community License for the distributed checkpoint.

Summarize these terms factually and link the current license. Do not provide a legal conclusion or claim that a use is cleared.

## Primary sources

- Launch blog: <https://www.minimax.io/blog/minimax-music-3-0-next-generation-open-weights-production-ready-versatile-music-model>
- Official GitHub repository: <https://github.com/MiniMax-AI/MiniMax-Music3>
- Official Hugging Face model card: <https://huggingface.co/MiniMaxAI/MiniMax-Music3>
- Community License: <https://huggingface.co/MiniMaxAI/MiniMax-Music3/blob/main/LICENSE>
- SGLang-Omni cookbook: <https://sgl-project.github.io/sglang-omni/cookbook/minimax_music3.html>
- Diffusers integration document: <https://github.com/huggingface/diffusers/blob/minimax-music3-integration/docs/source/en/api/pipelines/minimax_music3.md>
- ComfyUI native guide: <https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3>
