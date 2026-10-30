# Kling 4 & Kuaishou Video DiT Research Lineage

Use this reference to ground multi-reference disentanglement, multi-concept identity locking, 6-DoF camera trajectory separation, and video editing prompts in published Kuaishou / Kling research mechanics. Model availability and hard surface caps remain governed by [`capabilities.md`](capabilities.md).

## 1. Foundational Research Papers (Kuaishou / Kling Lab)

| Paper | arXiv ID | Core Architectural Mechanism | Deterministic Prompting Rule |
| --- | --- | --- | --- |
| **Kling-Omni Technical Report** | [`2512.16776`](https://arxiv.org/abs/2512.16776) | Unified Multi-Modal Visual Language (MVL) framework interleaving text instructions, reference images, and reference videos in a single end-to-end transformer for generation, Omni Reference, and instruction-based editing. | Assign each reference asset exactly one semantic ownership dimension (`identity`, `action/choreography`, `camera path`, `environment/layout`, or `voice`) and explicitly exclude unrequested dimensions (`do not inherit the reference performer's identity or background`). |
| **FullDiT** | [`2503.19907`](https://arxiv.org/abs/2503.19907) | Replaces separate adapter/ControlNet branches with unified 3D full self-attention across text, camera extrinsics, depth/white-model geometry, and identity conditions. | Order prompt clauses from coarse spatio-temporal structure to fine detail: `reference ownership -> spatial layout & camera trajectory -> primary physical action -> surface/lighting treatment -> audio -> terminal hold`. When using white-model/depth/wireframe videos, explicitly instruct the model to replace all gray/proxy shading with finished materials. |
| **ConceptMaster** | [`2501.04698`](https://arxiv.org/abs/2501.04698) | Tuning-free multi-concept video customization on DiTs; resolves **identity attribute bleeding** (where multiple subjects swap faces, outfits, or props) by decoupling concept tokens and binding each to distinct entity anchors. | State the exact count of distinct entities (`two distinct characters, one of each`), clarify when multiple turnaround views depict a **single** character, and pair each character with a persistent visual attribute anchor plus screen-side coordinate (`on screen left` / `on screen right`). |
| **ReCamMaster** & **SynCamMaster** | [`2503.11647`](https://arxiv.org/abs/2503.11647), [`2412.07760`](https://arxiv.org/abs/2412.07760) | 6-DoF camera-controlled generative rendering and multi-viewpoint dynamic synchronization over monocular/T2V diffusion backbones. | Decouple **camera extrinsics** (`start framing -> translation/rotation axis -> tracked target -> terminal framing`) from **subject kinematics**. Never combine mutually exclusive camera commands (e.g., `locked static camera` + `dolly in`) in the same continuous shot. |

## 2. Deterministic Mitigation Rules for Common Kling 4 Failure Modes

1. **Multi-Concept Attribute Bleeding (`arXiv:2501.04698`)**:
   - **Failure**: Two characters merge outfits, swap weapons, or duplicate into three figures.
   - **Rule**: Declare total subject cardinality up front, bind each reference image to a named role with 2–3 distinctive visual anchors (`armored courier in silver bracer` vs. `masked pursuer with wooden staff`), and maintain explicit left/right screen-axis separation.
2. **Cross-Modal Reference Contamination (`arXiv:2512.16776`, `arXiv:2503.19907`)**:
   - **Failure**: Motion or camera reference video leaks its source actor's clothing, room background, or proxy gray-box shading into the render.
   - **Rule**: Pair every structural/motion video binding with an explicit negative transfer clause: *"Use the performance video only for movement timing and gesture order; do not inherit the performer's appearance, costume, or background."*
3. **6-DoF Camera vs. Subject Velocity Confusion (`arXiv:2503.11647`)**:
   - **Failure**: Background slides unnaturally or camera crosses the 180° action line mid-impact.
   - **Rule**: Specify camera motion relative to the scene geometry and subject trajectory (`lateral tracking shot parallel to the rooftop from the near side without crossing the action axis`).
4. **Multi-Keyframe Teleportation (Up to 10 Keyframes)**:
   - **Failure**: Ordered keyframe images render as disconnected jump-cuts or morphing dissolves instead of physical progression.
   - **Rule**: Write an explicit causal transition bridge (`Entry Keyframe N -> physical locomotion/grip/contact -> Arrival Keyframe N+1`) and declare whether the bridge is `one continuous take` or an intentional editorial cut.
