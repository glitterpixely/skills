# MiniMax H3 Architecture & Physical-World Reasoning Research

Use this reference to ground failure-mode mitigations across multi-frame, audio-conditioned, and video-continuation tasks in empirical benchmark findings and joint audio-video Diffusion Transformer (MMDiT) mechanics.

## 1. System Architecture Summary

| Component | Technical Mechanism | Prompting Implication |
| --- | --- | --- |
| **33B Omni-DiT + Vision-Language Backbone** | Joint audio-video Diffusion Transformer conditioned on multimodal hidden states (Qwen3-VL-class encoder) generating 24 FPS video on a `17k+5` causal 3D VAE frame grid alongside native 32 kHz stereo audio. | Visual trajectories and acoustic transients denoise simultaneously inside shared cross-modal attention windows; co-locate visual contact and sound onset in the same chronological clause. |
| **Context-IR Intermediate Representation** | Translates heterogeneous inputs (`<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>`, `retention_analysis`, and task-type markers) into normalized structural conditioning before `H3-Base` synthesis. | In structured Ref2VA, explicit `retention_analysis` and `[Keep]`/`[Modify]`/`[Delete]` tags prevent identity and layout drift across cuts. |
| **H3-Regenerate-2K** | Second-stage context-aware 1440p/2K regeneration conditioned on the 768p draft plus original multimodal references (not a pixel upscaler). | Validate multi-reference blocking and timing at 768p before running 2K regeneration; keep original reference bindings intact during regeneration. |

## 2. Empirical Benchmark: Physical-World Omni-Modal Reasoning (`arXiv:2609.18323`)

**Study:** *"Can MiniMax-H3 Reason About the Physical World? An Evaluation of Omni-Modal Generative Models"* ([`arXiv:2609.18323`](https://arxiv.org/abs/2609.18323), Zhao et al., 2026) evaluated MiniMax-H3 across **517 multimodal test instances** spanning four reasoning regimes where essential task constraints are distributed across text, multi-frame images, audio, and prefix videos:

| Reasoning Regime | Benchmark Success Rate | Task Definition | Primary Observed Failure Mode |
| --- | ---: | --- | --- |
| **VDR** (Video-based Decision Reasoning) | **56.00%** | Short-horizon physical continuation and reaction from a prefix video (e.g., object approach, tool-surface contact). | Momentum discontinuities or ignored boundary collisions when the handoff frame state is left implicit. |
| **AVIR** (Audio-Video Integration Reasoning) | **47.89%** | Grounding auditory constraints alongside prefix or reference video dynamics. | Desynchronization between acoustic events and visual state transitions when sound and motion are described in separate clauses without shared timestamps. |
| **MSR** (Multi-frame State Reasoning) | **43.50%** | Inferring multi-step physical manipulation across multiple reference/keyframe images (e.g., assembly, container transfer). | Object teleportation, skipped mechanical steps, or implausible persistence when intermediate manipulation between frames is unstated. |
| **ADR** (Audio-based Disambiguation Reasoning) | **27.40%** | Inferring a physical event or state transition primarily from an audio cue or `<Audio N>` input (e.g., cabinet opening or paper rustling triggered by sound). | **72.60% failure rate**—the model frequently hallucinates static scenes or unrelated motion when expected to deduce physical causality from audio alone. |
| **Overall Aggregate (517 instances)** | **41.97%** | Combined omni-modal physical reasoning benchmark. | Native multimodal ingestion does not automatically resolve unstated physical causality (>58% aggregate error rate on implicit prompts). |

## 3. Joint Audio-Video DiT Alignment Literature

| Paper | arXiv ID | Core Mechanism | Deterministic Prompt Rule |
| --- | --- | --- | --- |
| **JavisDiT** | [`2503.23377`](https://arxiv.org/abs/2503.23377) | Hierarchical Spatio-Temporal Prior (HiST-Sypo) synchronization between global scene layout and fine-grained acoustic beats/onsets. | State global spatial layout first, then bind each percussive or foley transient (`click`, `thud`, `splash`) to the exact visual contact beat. |
| **AudioGen-Omni** | [`2508.00733`](https://arxiv.org/abs/2508.00733) | Unified MMDiT with Phase-Aligned Anisotropic Positional Infusion (PAAPI) and selective RoPE across video, speech, and song tokens. | Keep spoken word density within natural articulation limits ($\le$2.5–3.0 words/s) and assign stable speaker IDs in chronological vocal-onset order. |

## 4. Deterministic Failure-Mitigation Rules

1. **Eliminate Pure ADR Dependency (27.40% baseline):** Never rely on `<Audio N>` or a sound description alone to trigger or disambiguate a physical action. Every acoustic cue in `overall_soundscape` or inline `<Audio N>` binding must have an explicit visual counterpart (`actuator -> contact -> visible state change`) at the same timestamp in the visual description.
2. **Spell Out MSR Intermediate Mechanics (43.50% baseline):** When bridging two keyframes (`FL2VA`) or multiple reference stills (`Ref2VA`), never leave the manipulation step implicit. Explicitly write the physical bridge: grip/support $\rightarrow$ transport path $\rightarrow$ alignment $\rightarrow$ contact/release $\rightarrow$ settled target state.
3. **Lock VDR/AVIR Handoff Boundary (56.00% / 47.89% baseline):** For video continuation or editing (`<Video N>`), state the exact terminal pose, velocity direction, and active prop state at the boundary frame before describing the new action.
4. **Co-Locate Transient Audio-Visual Clauses (`2503.23377`, `2508.00733`):** Place diegetic foley and speech onsets inside the same timed shot/phase block as the physical contact or mouth articulation that produces them, while keeping audience-only score isolated in `non_diegetic_music`.
