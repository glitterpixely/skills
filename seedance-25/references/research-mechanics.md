# Research-Grounded Model Mechanics & Training Lineage

This reference synthesizes primary **ByteDance Seed / Intelligent Creation** technical reports and companion papers to explain *why* Seedance 2.5 responds to specific prompt structures, asset orderings, and API parameter locks. It never overrides first-party capability limits or surface contracts in [source-boundaries.md](source-boundaries.md).

## Contents

- [Architectural lineage (2025–2026)](#architectural-lineage-20252026)
- [Six core training pillars](#six-core-training-pillars)
- [Research-grounded model mechanics (directing rules)](#research-grounded-model-mechanics)
- [Explicit Seedance 2.5 evidence boundary](#explicit-seedance-25-evidence-boundary)

## Architectural lineage (2025–2026)

ByteDance's video generation stack evolved across five foundational model generations plus specialized conditioning, captioning, and post-training papers:

- **Backbone progression:** *Seaweed-7B* (`arXiv:2504.08685`) -> *Seedance 1.0* (`arXiv:2506.09113`) -> *Seedance 1.5 Pro* (`arXiv:2512.13507`) -> *Seedance 2.0* (`arXiv:2604.14148`) -> *FlowAct-R2* on *Seedance 2.0 Mini* (`arXiv:2609.35728`) and production *Dreamina Seedance 2.5* (`dreamina-seedance-2-5-260628`).
- **Companion ByteDance subsystems:** *Tarsier2* (`arXiv:2501.07888`, frame-grounded video captioning), *Phantom* (`arXiv:2502.11079`) & *Phantom-Data* (`arXiv:2506.18851`, cross-paired subject-to-video decoupling), *OmniHuman-1* (`arXiv:2502.01061`) & *HuMo* (`arXiv:2509.08519`, audio-driven human animation & time-adaptive multimodal CFG), *DanceGRPO* (`arXiv:2505.07818`) & *RewardDance* (`arXiv:2509.08826`, generative VLM Chain-of-Thought reward modeling with ReFL), and *APT* (`arXiv:2501.08316`) / *AAPT* (`arXiv:2506.09350`, 1-to-few-step adversarial distillation).

*(Attribution guard: do not attribute Kuaishou / Kling papers such as VideoReward / Flow-DPO `arXiv:2501.13918` or Koala-36M `arXiv:2410.08260` to ByteDance's Seedance team.)*

## Six core training pillars

### 1. Heterogeneous data curation, `Tarsier2` captioning, & `PE` rewriting
- **5-stage BMF/Ray curation (*Seedance 1.0*, Sec. 3.1 & 3.3):** Raw corpora run across CPU/GPU/NPU pools through (1) shot-boundary cut segmentation, (2) hybrid detector **visual overlay rectification** that crops out watermarks, logos, and burned-in subtitles, (3) aesthetic, jitter, optical-flow motion, and safety classifiers, (4) video-embedding cluster semantic deduplication, and (5) head-class downsampling + tail-concept rebalancing.
- **`Tarsier2` frame-grounded bilingual captions (`arXiv:2501.07888`; *Seedance 1.0*, Sec. 3.2):** Pretrained on `40M` video-text pairs (`200B` tokens), `Tarsier2` is fine-tuned on `150K` two-stage human annotations (exact frame-timestamped atomic actions, micro-expressions, object state changes, and camera moves synthesized into **static inventories + chronological dynamic trajectories**) plus `20K` `AutoDQ` temporal-perturbation DPO pairs that penalize temporal hallucinations.
- **Prompt Engineer (`PE`, *Seedance 1.0*, Sec. 2.4):** To bridge sparse user prompts and dense `Tarsier2` captions, ByteDance applies full-parameter SFT + LoRA-DPO to a `Qwen2.5-14B` rewriter, evolving into `Seedance 2.5`'s task-aware `sd25-pe` (`0.3.3`) specification.

### 2. Temporally causal `64x` 3D VAE & the `8n + 1` edit frame quantum
- **Causal latent packing (*Seaweed-7B*, Sec. 2.1; *Seedance 1.0*, Sec. 2.1):** Pixel tensors $(T'+1, H', W', 3)$ map to continuous latents $(T+1, H, W, C)$ with $(r_t, r_h, r_w) = (4, 16, 16)$, $C = 48$ ($64\times$ compression), and DiT `patch size = (1, 1, 1)`. Frame $0$ occupies its own causal slot ($T=T'=0$) so images and video share one latent space, paired in *Seedance 1.5 Pro* with a continuous universal audio VAE.
- **Why `8n + 1` eliminates edit duration drift:** While `Seedance 1.0` exposed `25 + 4n` frame increments ($r_t=4$ plus causal frame $0$), `Seedance 2.5` Edit mode operates on an `8`-frame (`0.333s` @ 24 fps) temporal alignment stride ($2 \times r_t$ window grouping / dual-branch audio-video stride) after causal frame $0$. Pre-trimming edit source clips to **`8n + 1` frames** (`161 = 8 \times 20 + 1` frames = `6s 17f` @ 24 fps) aligns exactly with that latent boundary and prevents the documented `~0.33s` trailing truncation.

### 3. Decoupled spatial concatenated `MMDiT`, `Multishot MM-RoPE`, & dual-branch audio-video
- **Spatial multi-modality self-attention (*Seedance 1.0*, Sec. 2.2):** Encoded by a fine-tuned decoder-only LLM, text tokens are **concatenated** with visual tokens inside **spatial layers** via **multi-modality self-attention** (with modality-specific AdaLN, QKV projections, and MLPs plus QK-Norm — *not* cross-attention). **Temporal layers** process visual tokens only, combining spatial windowing with global temporal receptive fields.
- **`Multishot MM-RoPE` (*Seedance 1.0*, Sec. 2.2):** 3D `(t, h, w)` visual RoPE interleaves with 1D shot-indexed text RoPE (`[global_style, shot_1_caption, shot_1_latents, shot_2_caption, shot_2_latents, ...]`), natively supporting multi-shot cuts and OTS reverses inside one generation.
- **Dual-branch joint audio-visual `MMDiT` (*Seedance 1.5 Pro*, Sec. 2.1.2; *Seedance 2.0*, `arXiv:2604.14148`) & streaming conditioning (*FlowAct-R2*, `arXiv:2609.35728`):** Parallel video and audio `MMDiT` branches exchange bidirectional cross-modal attention over visual tokens, acoustic foley, and bilingual phoneme latents, while `FlowAct-R2` demonstrates Diffusion Forcing chunk training, video-driven 3D RoPE, and historical-frame noise injection for long-horizon stability.

### 4. Cross-modal reference decoupling (`Phantom`, `HuMo`) & 50-asset scaling
- **Non-frame cross-paired triplets (*Phantom* `arXiv:2502.11079`; *Phantom-Data* `arXiv:2506.18851`):** Training on `~1M` cross-paired identity triplets (where reference portraits come from different scenes/poses than target clips) teaches sequence-concatenated DiT blocks to strip background and static pose when prompted (`do not use @Image 1's background or static standing pose`).
- **Facial BCE mask & reverse-diffusion CFG (*HuMo* `arXiv:2509.08519`):** `HuMo` appends zero-initialized reference projections at the spatial tail, trains a size-aware `focus-by-predicting` binary cross-entropy facial attention mask so speech audio binds to the speaker's face rather than background clutter, and varies multimodal CFG across **reverse-diffusion noise timesteps** ($t \in [1.0, 0.98]$ emphasizes text/layout across all frames simultaneously; $t \in [0.98, 0]$ ramps up identity and lip-sync). *(Note: diffusion timestep $t$ denoises all frames in parallel and is distinct from playback seconds `0–1s`.)*
- **2.0 -> 2.5 scaling:** Expands multimodal capacity from `9+3+3` (`15s`) to **`30` images + `10` videos (`<=30s`) + `10` audio (`<=30s`) = `50` assets**, `30s` Standard (`180s` Dreamina Long Video), integer-second timestamps, `[0.4, 2.5]` ratios, multi-view sheets, audio-only + text, and `.mov` continuity.

### 5. Progressive flow matching, merged specialist SFT, & multi-reward RLHF
- **Progressive pre-training & Continue Training (*Seedance 1.0*, Sec. 4.1–4.2):** Rectified flow matching with shifted logit-normal timestep sampling scales from `256px` T2I -> `256px` `12fps` -> `640px` `12fps` -> `640px` `24fps` (`20%` -> `40%` I2V in Continue Training, pairing full captions with **motion-only short captions** so I2V prompts need not re-describe the start frame).
- **Specialist SFT merging (*Seedance 1.0*, Sec. 4.3):** Hundreds of curated style and motion categories are fine-tuned as separate specialist SFT checkpoints with early stopping and **weight-merged** into one model. Mixing conflicting style cues (`airbrushed painterly` + `2D cel-shaded` or `2D anime` + `85mm bokeh`) pulls between merged specialist basins across cuts.
- **Direct-$x_0$ composite 3-RM RLHF & `RewardDance` ReFL (*Seedance 1.0*, Sec. 4.4; *Seedance 1.5 Pro*, Sec. 2.2.3; *RewardDance*, `arXiv:2509.08826`):** Multi-round RLHF predicts clean $x_0$ directly to maximize a composite of three reward models (outperforming DPO/PPO/GRPO in *Seedance 1.0*): (1) omni-modal VLM alignment judge (`RewardDance` scales generative VLM RMs up to `26B`, scoring $P_\theta(\text{"yes"})$ with `SEED-VL 1.5` Chain-of-Thought rubrics via **ReFL**), (2) latent/video **Motion RM** penalizing frozen slow-mo and anatomical artifacts, and (3) keyframe **Aesthetic RM**.

### 6. Multi-stage distillation & the RLHF `480p -> 1080p` Diffusion Refiner
- **`>10x` acceleration (*Seedance 1.0*, Sec. 5; *Seedance 1.5 Pro*, Sec. 2.3):** Combines `TSCD`, Multi-Segment `MeanFlow`, `RayFlow`, adversarial `APT`, `AdaSpa` block-sparse attention, a thin $2\times$ VAE decoder, and FP8 parallelism.
- **Cascaded `480p -> 1080p` Refiner & `draft_task` locking (*Seedance 1.0*, Sec. 2.3 & 4.4.4):** The base model generates `480p` latents; an RLHF-aligned **Diffusion Refiner** upsamples and channel-concatenates those `480p` latents with noise to synthesize `1080p` 10-bit HEVC detail. On BytePlus ModelArk, Step-1 `draft=true` runs and caches the `480p` base trajectory for 14 days, and Step-2 `draft_task` runs **only** the `1080p` Refiner on that cached trajectory — explaining why re-sending `prompt`, `seed`, `duration`, `ratio`, `generate_audio`, `omni_reference_task_type`, or media URLs in Step 2 throws a hard API error.

## Research-grounded model mechanics

Translate the six pillars above into seven high-leverage prompt rules:

1. **Unbind portrait background & static pose (`Phantom`):** Always write `@Image 1 defines only <Name>'s facial features, hairstyle, and outfit; do not use its background or static standing pose` when animating a portrait or turnaround sheet, and upload multi-subject `@Image` plates in **chronological order of first on-screen appearance**.
2. **Front-load spatial layout & camera; scope `0–1s` settle to dialogue only (`HuMo` + causal VAE):** Put the 180-degree stage map and camera trajectory in clause 1 so early diffusion steps ($t \in [1.0, 0.98]$) lock layout across all frames. Reserve a `0–1s` playback settle strictly for dialogue/lip-sync clips (empirical causal-VAE stabilization) — **never** write `"settling briefly before the action"` in fast fights or chases (`OPENING_SETTLE_IN_ACTION`). Add torso **rhythm carriers** (`breathing, subtle weight shift, small hand gesture`) so heavy `@Image` + `@Audio` guidance does not freeze speakers.
3. **Write 3-part verifiable state transitions (`RewardDance` CoT RM + Motion RM):** Phrase key beats as `observable entry state -> physical contact/operation -> observable exit state` rather than mood adjectives.
4. **Keep strict forward chronology & gated micro-action chains (`Tarsier2`):** Write actions strictly in forward frame order (`A -> B -> C`), chaining `6–10` subtle reaction beats with `in this exact order, each step its own beat: first..., then..., only after...`.
5. **Use the 3-tier caption hierarchy & post-cut re-tagging (`Multishot MM-RoPE`):** Structure complex multi-shot prompts as `[Brief]` -> `[Style, Reference Roles, & Continuity Locks]` -> `[Shot list]`, re-tagging `<Name>, <2-word trait>` after hard cuts or heavy occlusions, and keep exclusions `<= 80` words so banned nouns do not flood spatial `MMDiT` multi-modality self-attention (`BLOATED_EXCLUSION_LIST`).
6. **Lock one pure visual medium (`Merged Specialist SFT`):** Never mix `2D cel-shaded` with `airbrushed painterly` (`AIRBRUSH_CEL_CONFLICT`) or live-action `bokeh` (`STYLE_2D_LENS_CONFLICT`).
7. **Isolate emotion to brow and eyes during lip-sync (`Dual-Branch Audio-Visual MMDiT`):** Route emotion to the upper face (`All facial expression lives in the brow and the eyes; the mouth is left natural`) with `<Name> alone speaks` and `No subtitles.` so emotional tokens do not distort `p/b/m` viseme closure.

## Explicit Seedance 2.5 Evidence Boundary

As of `2026-11-10`, ByteDance has published standalone technical reports through *Seedance 2.0* (`arXiv:2604.14148`) and *FlowAct-R2* (`arXiv:2609.35728`), with **no standalone `Seedance 2.5` arXiv architecture paper**. Keep these provenance tiers distinct when answering technical questions:

| Claim Category | Provenance Status on `Seedance 2.5` | Primary Source |
| :--- | :--- | :--- |
| Causal `64x` 3D VAE (`4x16x16`, `C=48`), spatial concatenated `MMDiT` self-attention, windowed temporal attention, `Multishot MM-RoPE`, `Qwen2.5-14B` `PE`, merged specialist SFT, direct-$x_0$ 3-RM RLHF, `480p -> 1080p` Refiner | **Published for `1.0–1.5 Pro`; high-confidence architectural heritage for `2.5`** (exact `2.5` parameter count, layer depth, and `sd25-pe` base model size are undisclosed) | `arXiv:2506.09113`, `arXiv:2512.13507` |
| Dual-branch joint audio-visual `MMDiT` + unified multimodal reference (`@Image` + `@Video` + `@Audio` + text + edit + extend) | **Published for `1.5 Pro` & `2.0`; confirmed active capability surface on `2.5`** | `arXiv:2512.13507`, `arXiv:2604.14148`, BytePlus `seedance-2-5` |
| `Tarsier2` frame-grounded captioning, `Phantom` cross-paired decoupling, `HuMo` facial BCE mask & timestep CFG, `RewardDance` `26B` CoT ReFL | **Published ByteDance companion papers** (verified lab methods; exact `2.5` mixture weights are bounded inferences) | `arXiv:2501.07888`, `arXiv:2502.11079`, `arXiv:2509.08519`, `arXiv:2509.08826` |
| `dreamina-seedance-2-5-260628`, `50` assets (`30+10+10`), `4–30s` Standard (`180s` Dreamina Long Video), `4–30s` edit video (`8n+1` exact frames), `1080p` 10-bit HEVC cap (`4K` unsupported), mono audio, integer timestamps, `[0.4, 2.5]` ratio, `mov`, 14-day `draft_task`, 30-day portrait trust | **Directly documented `Seedance 2.5` production facts** | BytePlus ModelArk official docs (`2026-11-07`) & Dreamina web surface |
