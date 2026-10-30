# Kling 4 & Kuaishou Video DiT Research Lineage

Use this reference to ground reference ownership, multi-subject identity separation, camera/subject separation and physical-causality rules. Model availability and hard caps stay in [`capabilities.md`](capabilities.md).

Citations were checked against the arXiv API on 2026-10-30. The four Kuaishou papers below list Kuaishou authors in their arXiv HTML. Kling 4.0's own architecture is not published; these papers show the lab's published methods, not Kling 4.0 internals. Each table separates what a paper reports from the prompt rule this skill derives from it.

## 1. Kuaishou / Kling research

| Paper | arXiv ID | What the paper reports | Derived prompt rule (heuristic) |
| --- | --- | --- | --- |
| **Kling-Omni Technical Report** | [`2512.16776`](https://arxiv.org/abs/2512.16776) | One end-to-end framework that takes text instructions, reference images and video contexts as a unified multimodal representation, for generation, editing and reasoning-based editing. | Inputs are read jointly, so an asset can leak traits you did not intend. Give each asset one job (`identity`, `action`, `camera path`, `environment`, `voice`) and say what it must not contribute. |
| **FullDiT** | [`2503.19907`](https://arxiv.org/abs/2503.19907) | Fuses multiple conditions (e.g., camera, identity, depth) into one sequence with full self-attention instead of separate adapters, to avoid branch conflicts between conditions. | Conditions compete inside one attention space. Do not give two assets the same job. When you use a gray-box, depth or wireframe video, tell the model to replace all proxy shading with finished materials. |
| **ConceptMaster** | [`2501.04698`](https://arxiv.org/abs/2501.04698) | Names the *identity decoupling* problem: multi-concept customization mixes identity attributes between subjects. Learns decoupled per-concept embeddings. | State the subject count (`two distinct characters, one of each`). Say when several turnaround views show **one** character. Give each subject 2–3 unique visual anchors and a screen side. |
| **ReCamMaster** | [`2503.11647`](https://arxiv.org/abs/2503.11647) | Re-renders the dynamic scene of an input video along a new camera trajectory, conditioned on the source video. | Describe camera motion separately from subject motion: start framing → move axis → tracked target → end framing. |
| **SynCamMaster** | [`2412.07760`](https://arxiv.org/abs/2412.07760) | Multi-camera generation from arbitrary 6-DoF viewpoints with a multi-view synchronization module for appearance and geometry consistency. | When a sequence cuts between angles of one moment, restate the subject's appearance and position for each angle. |

## 2. General video-generation evidence

| Paper | arXiv ID | What the paper reports | Derived prompt rule (heuristic) |
| --- | --- | --- | --- |
| **Physics-IQ** | [`2501.09038`](https://arxiv.org/abs/2501.09038) | Physical understanding in current video models is severely limited and unrelated to visual realism. | Write footing, approach, contact and result before spectacle. "Cinematic" or "realistic" does not add physics. |
| **VideoPhy** | [`2406.03520`](https://arxiv.org/abs/2406.03520) | Text-to-video outputs often break physical commonsense in solid–solid, solid–fluid and fluid–fluid interactions. | Name both materials at a contact and the outcome (`boot sinks ankle-deep into wet sand`). |
| **CameraCtrl** | [`2404.02101`](https://arxiv.org/abs/2404.02101) | Camera pose is a distinct control signal from content; camera-diverse training data improves camera controllability. | Treat the camera as its own clause. Never combine contradictory camera commands (`locked-off` + `dolly in`) in one continuous shot. |
| **NegBench** | [`2501.09425`](https://arxiv.org/abs/2501.09425) | Modern vision-language models often handle negated captions at chance level. | Pair every exclusion with a positive ownership statement: `use the performance video only for timing and gesture order` before `do not inherit the performer's face, costume or room`. |
| **VBench-2.0** | [`2503.21755`](https://arxiv.org/abs/2503.21755) | Scores intrinsic faithfulness on Human Fidelity, Controllability, Creativity, Physics and Commonsense. | Use these five headings when you review a render ([`review-and-repair.md`](review-and-repair.md)). |

## 3. Failure modes and mitigations

1. **Identity bleeding between subjects (ConceptMaster):** two characters swap outfits or props, or a third appears. Declare the subject count. Bind each reference to a named role with 2–3 unique anchors (`courier in silver bracer` / `pursuer with wooden staff`). Keep left/right screen sides fixed.
2. **Reference contamination (Kling-Omni, FullDiT, NegBench):** a motion or camera video leaks its actor, room or gray-box shading. State the positive job of the asset first, then one short exclusion clause.
3. **Camera vs. subject confusion (ReCamMaster, CameraCtrl):** the background slides or the camera crosses the action line during an impact. Describe camera motion relative to scene geometry and the subject's path (`lateral tracking shot parallel to the rooftop, near side, without crossing the action axis`).
4. **Keyframe teleportation (up to 10 keyframes; craft rule, no paper):** ordered keyframes render as jump cuts or morphs. Write the bridge (`Keyframe N → locomotion/grip/contact → Keyframe N+1`) and say whether it is `one continuous take` or an intentional cut.
5. **Physically wrong contact (Physics-IQ, VideoPhy):** objects pass through each other, liquids behave like solids, impacts have no reaction. Name materials, the contact point and the visible result.
