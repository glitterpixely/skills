# MiniMax H3 Physical-World Reasoning & Audio-Video Alignment Research

Use this reference when an H3 prompt depends on the model inferring something the prompt does not state: a spatial relation spread across several images, what a sound means, what should happen next in a prefix video, or which part of a video a spoken instruction refers to.

Citations were checked against the arXiv API and the paper HTML on 2026-10-30. Each table separates what a paper reports from the prompt rule this skill derives from it. A derived rule is a prompting heuristic, not a result the paper measured.

## 1. System facts used by these rules

These facts come from [`model-contract.md`](model-contract.md) and [`runtime-surfaces.md`](runtime-surfaces.md). Those files hold the dated provider sources.

| Fact | Source file | Prompt consequence |
| --- | --- | --- |
| H3 generates video and native 32 kHz stereo audio together at 24 FPS. | `model-contract.md` | Write a sound and the visible action that causes it in the same timed clause. |
| Hosted pipeline: H3-Context-IR structures the inputs, H3-Base generates 768p, H3-Regenerate-2K regenerates to 1440p/2K from the draft plus the original inputs. | `runtime-surfaces.md` | Check blocking and timing at 768p. Keep the original reference bindings unchanged when you regenerate to 2K. |

Parameter counts, encoder layers and VAE internals are not part of this skill's audited source set. Do not state them in a prompt or a reply.

## 2. Benchmark: implicit multimodal reasoning (`arXiv:2609.18323`)

**Paper:** Haoyu Zhao et al. (National University of Singapore), *"Can MiniMax-H3 Reason About the Physical World? An Evaluation of Omni-Modal Generative Model"*, [`arXiv:2609.18323`](https://arxiv.org/abs/2609.18323), 16 Sep 2026.

**Design:** 517 expert-verified instances in 4 scenarios and 29 subcategories. Every prompt is *implicit*: it names the task but withholds the target inference, so the model must derive it from the images, audio or video.

| Scenario (paper's name) | n | Success rate | What the input gives and what is withheld |
| --- | ---: | ---: | --- |
| **VDR** — Video-based Decision Reasoning | 100 | **56.00%** | A prefix video. The prompt does not say how to respond (e.g., a ball rolls into the road, so the vehicle should stop before a child appears). |
| **AVIR** — Audiovisual Integrated Reasoning | 71 | **47.89%** | A video plus audio or spoken constraints, not necessarily time-aligned. The model must continue the video, or find the content that conflicts with the speech and revise it. |
| **MSR** — Multi-view Spatial Reasoning | 200 | **43.50%** | K images of one scene from different viewpoints. The spatial relation is only recoverable across views (correspondence, occlusion, viewpoint change). |
| **ADR** — Audio-based Disambiguation Reasoning | 146 | **27.40%** | One ambiguous image plus audio that decides between interpretations (e.g., which of three cups of different materials fell, from the impact sound). |
| **Overall** | 517 | **41.97%** | — |

**Failure types the paper reports (Section 4.4):**

1. **Incorrect evidence grounding:** a plausible event, attached to the wrong entity or action.
2. **Incomplete event realization:** the right objects appear, but the implied interaction (typing, opening a can) does not happen.
3. **Physical and configurational violations:** broken contact dynamics, object geometry or state transitions (skateboard, rolling object, puzzle, Rubik's Cube cases).
4. **Temporal state inconsistency:** object states, motion trends or scene content established earlier are not kept through the continuation.

**What this means for prompting:** the benchmark scores H3 on inferences that the prompt withholds. Production prompts do not have to withhold anything. Every rule in Section 4 converts a withheld inference into a stated one.

## 3. Supporting literature

| Paper | arXiv ID | What the paper reports | Derived prompt rule (heuristic) |
| --- | --- | --- | --- |
| **Physics-IQ** (*Do generative video models understand physical principles?*) | [`2501.09038`](https://arxiv.org/abs/2501.09038) | Across Sora, Runway, Pika, Lumiere, SVD and VideoPoet, physical understanding is severely limited and unrelated to visual realism. | A photoreal style request does not buy correct physics. Write the mechanism: support, force, contact, result. |
| **VideoPhy** | [`2406.03520`](https://arxiv.org/abs/2406.03520) | Benchmarks physical commonsense in material interactions (solid–solid, solid–fluid, fluid–fluid); text-to-video models often violate it. | Name the materials on both sides of a contact and the expected outcome (`ceramic cup hits tile and shatters into three large pieces`). |
| **PhyGenBench** | [`2410.05363`](https://arxiv.org/abs/2410.05363) | 160 prompts over 27 physical laws in four domains, for physical-commonsense correctness in T2V. | When a shot depends on one physical law (buoyancy, refraction, melting), make the visible consequence the subject of the sentence. |
| **VBench-2.0** | [`2503.21755`](https://arxiv.org/abs/2503.21755) | Scores "intrinsic faithfulness" on Human Fidelity, Controllability, Creativity, Physics and Commonsense. | Use these five headings as the review checklist when you inspect a render. |
| **JavisDiT** | [`2503.23377`](https://arxiv.org/abs/2503.23377) | Joint audio-video DiT. A Hierarchical Spatial-Temporal Synchronized Prior (HiST-Sypo) estimator extracts global and fine-grained priors that guide audio-video synchronization. | State the scene layout first. Then bind each transient sound (`click`, `thud`, `splash`) to the visible contact that makes it. |
| **AudioGen-Omni** | [`2508.00733`](https://arxiv.org/abs/2508.00733) | Unified MMDiT for video-synchronized audio, speech and song. A lyrics-transcription encoder gives frame-level grapheme/phoneme features; PAAPI applies RoPE only to temporally structured modalities; joint training improves lip-sync. | Give each spoken line a speaker and a time window. The 2.5–3.0 words/s ceiling in this skill is a craft heuristic for natural delivery, not a value from this paper. |
| **NegBench** (*Vision-Language Models Do Not Understand Negation*) | [`2501.09425`](https://arxiv.org/abs/2501.09425) | 79k examples across image, video and medical data: modern VLMs often handle negated captions at chance level. | Describe the wanted state positively (`the table stays empty`) instead of only listing absences. Keep any `no ...` list short and specific. |

## 4. Prompt rules derived from Sections 2–3

1. **Write what the audio means (ADR, 27.40%).** When a sound must decide what happened, name the event in text: `the glass cup on the left falls and shatters; matching bright glass-break sound`. Do not leave H3 to infer the event from `<Audio N>`. Give every diegetic sound a visible cause at the same timestamp.
2. **Write the cross-view spatial relation (MSR, 43.50%).** When several images show one scene from different angles, state the relation the views establish: `the red door seen in Picture 2 is directly behind the sofa from Picture 1`. When bridging keyframes, also write the physical bridge: grip or support → transport path → alignment → contact or release → settled state.
3. **Write the intended response (VDR, 56.00%).** For a continuation, state the reaction you want and its cause: `the car brakes to a full stop before the crossing because the ball rolled into the road`. Also state the boundary-frame pose, velocity direction and active prop state.
4. **Bind the spoken constraint to its target (AVIR, 47.89%).** For a speech-driven edit or continuation, quote the constraint and name the visual element it changes: `the narrator says the lamp is off, so turn off the desk lamp on screen right; keep everything else unchanged`.
5. **Pre-empt the four failure types.** Name the entity for each action (grounding). State the interaction verb and its visible result (realization). Name the materials and the contact outcome (physics). Restate prop and pose states after each cut or phase change (temporal consistency).
