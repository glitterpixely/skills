# Desk Prompt Patterns

Clip-desk production heuristics distilled from public and user-supplied action and observational worldbuilding prompts. Written-prompt study provides craft hypotheses, not evidence of generated fidelity. These heuristics do **not** expand model capabilities, limits, prices, UI quotas, or API fields. If a heuristic conflicts with [source-boundaries.md](source-boundaries.md), [prompt-architecture.md](prompt-architecture.md), or [task-contracts.md](task-contracts.md), follow those files.

Honor the user's standing clip-desk defaults unless they override them: beauty-first (ethereal, regal, romantic celestial / anime — not grotesque); no music or BGM unless they ask; paste-ready prompt body only.

## Action mechanics and framing

Use these user-supplied directing lessons for a leap, evasion, connected movement, or finishing strike when relevant. They also apply to simple action shots without requiring the dense kinetic-action mode below. Preserve the requested choreography, pace, camera restrictions, and outcome; railings, walls, and swords are examples, not required scene elements.

- **Load before release.** For an explosive grounded leap, show the body lowering deeply, hips and knees flexing over planted feet, then the legs driving against the ground before takeoff. Make the support contact and launch direction visible. Keep anticipation compact at a fast pace; a deep compression does not require a long pause or slow motion.
- **Make the defense feed the next move.** When the action should continue, connect evasion to an available environmental contact: a hand catches an established railing and pulls the body around it, or a foot plants against a wall and pushes off into the next trajectory. Specify contact -> force/redirection -> release -> next movement. Carry momentum and position forward without an unexplained reset. Check that the surface is reachable and the gripping hand is free without changing weapon ownership.
- **Frame the near miss.** Let the camera rapidly follow the evading face, arriving at an angle that shows the face, passing sword, and narrow visible gap together at closest approach. Preserve readable separation through focus, silhouettes, and restrained blur; camera speed alone does not communicate how close the miss was. Continue with the movement without inserting unrequested slow motion or a freeze.
- **Reveal the final strike's reach.** Trigger a strong pullback or motivated cut to a much wider view as the finishing attack travels. Keep its origin, path, and farthest affected point legible against established environmental landmarks. Widen the framing, not the aspect ratio, and reveal the attack's existing reach without inventing extra power or destruction. Preserve a locked camera or continuous-shot requirement when supplied.

## Reference-led kinetic action

Use this mode only when the user wants a supplied prompt's dense, cinematic control pattern for a fight, chase, transformation, destruction, or effects-led sequence. Reuse the mechanics of the prompt, not its characters, world, unsupported render settings, or story outcome.

Build in this order:

`reference jobs -> global locks -> force/effect system -> causal stages -> camera path -> escalation -> failure guards`

The prompt should read like a small production contract. Give each image one job, state what it does not control, then lock identity, count, prop ownership, axis, palette, lighting direction, and two or three rigid environmental landmarks. If an existing action is translated into a new material or environment, preserve its dramatic function and state the replacement explicitly.

### Causal force and VFX grammar

For every important attack or effect, use:

`preparation -> acceleration -> contact/trigger -> force transfer -> visible material response -> residue -> recovery`

Examples of valid origins include contact, friction, velocity, impact, wind, or a clearly named energy trigger. A monster does not burn before the blade, wave, beam, or marked effect reaches it. A spark, dust burst, fabric movement, heat distortion, fragment, or glow should have a visible source. Replace vague phrases such as “powerful” with body mechanics, object motion, impact feedback, and environmental response.

### Dense stage pattern

For a user-requested maximal action pass, use consecutive stages such as:

```text
T=0-2s — <beat name>
Initial state: <blocking, prop state, and camera state>.
Action: <preparation -> contact or trigger -> consequence -> recovery>.
Camera: <target/start> -> <path and speed change> -> <end framing and visible result>.
End state: <observable state that carries forward>.
```

Up to three short sub-beats can appear inside one stage when they form one connected causal chain. If they are separate techniques, effects, or targets, split the stage or use an extension. Preserve the user's intense pacing as an approximate creative budget; do not claim frame-accurate timing.

### Escalation and scale

Prefer a readable escalation: distant crowd or silhouette mass, mid-ground attack, foreground elite contact, large-scale consequence, then a new threat or aftermath hook. Use crowd density and simplified silhouettes in the distance; reserve detailed anatomy, hit response, and causal VFX for the near subject. Keep environmental anchors visible through the camera path so the sequence remains geographically legible.

When the scene is a fight, change choreography before adding more adjectives if a result is weak. Keep identity, location, axis, prop ownership, and camera contract; reduce the number of contacts until each one reads.

### Reciprocal combat and action-driven travel

For an evenly matched duel, build exchanges around `attack -> defense -> counterattack -> recovery or regained initiative`. Let defenses change the next attack through a deflection, redirected momentum, escape, or position change. Balance initiative across the sequence; do not require identical exchanges in every shot. Preserve a requested victor or deliberate power imbalance instead of imposing a stalemate on every fight.

When combat travels, make each new location the consequence of a visible action. Track `departure landmark -> force or locomotion -> visible route -> arrival state`. For example: an uppercut breaks through a roof; pursuit crosses its wet ridge toward a visible cliff; a clash launches both fighters beyond the edge. Carry their relative positions and momentum into the next beat. A location list alone does not establish continuity. Preserve a requested single arena.

In aerial action, name the propulsion that changes direction or altitude: a surface rebound, air-step, flight thrust, or directed energy recoil. A downward blow does not explain both fighters accelerating upward without an additional force.

### Camera continuity and contact visibility

Tie each camera move to an action trigger and a framing purpose: follow a launch upward, track a fall downward, or travel beside a pursuit. Specify whose viewpoint a first-person or body-mounted camera uses. A pseudo-one-take needs explicit bridges between viewpoints: debris, a passing roof edge, cloud cover, a waterfall curtain, or a motivated whip pan, followed by a defined arrival composition and preserved motion direction. Merely listing camera abbreviations does not create a continuous path.

Make contact readable before the largest effect bloom. Preserve fighter silhouettes, assigned energy colors, and the attack target through the burst. Use environmental displacement to communicate force, escalating from local fragments to larger structural or landscape responses when the story calls for it. Reserve the greatest consequence for the intended climax instead of making every hit equally large.

For nonstop action without slow motion or hit-stop, emphasize impact with a brief light surge, camera impulse, immediate recoil, expanding shockwave, debris, and continuing motion. Do not introduce a speed ramp against that instruction. Express speed through pursuit, parallax, cloth drag, trails, and rapid recovery rather than quotas of actions per second.

### Timing and continuation checks

Give each shot one dominant exchange or state change. Keep connected sub-beats only while preparation, contact, and reaction remain distinguishable. If the climax includes impact, environmental destruction, separation, recovery, and a final close-up, allocate time across those beats or simplify them; do not pack them into the last second.

For an unresolved ending, retain a readable final position and an active threat or renewed approach when requested. A stable, trackable boundary does not require a motionless pose. Specify contact sounds and environmental audio when useful; preserve the no-music default. Keep failure guards specific to identity, geography, contact, effects, and the requested outcome rather than copying an exhaustive negative list.

## Bilingual combat VFX & spatiotemporal prompting

Seedance 2.5 is natively bilingual, but combat physics, anime impact frames, and martial-arts kinematics are heavily weighted toward Chinese captions in its training distribution.

### Key execution rules

- **Bypass middleware rewriters**: Global API wrappers and UI "Prompt Enhance" layers often rewrite or translate snappy tokens like `闪切` (flash-cut) into generic English (`transform`, `morph`), which triggers mesh melting. Disable "Prompt Enhance" when using this mode.
- **Hybrid token injection**: Even when structuring schemas or prompts in English, inject native Chinese action and physics tokens directly into the prompt payload to lock onto high-density motion weights.

### Principle 1: Impact frames (`冲击帧`) & transformation logic

Raw AI transformations take ~2 seconds and look mushy. Use hard style-cut tokens in the prompt, then compress in post-production.

- **Prompt formula**:
  `闪白 → 发光线稿 → 闪切 2D 漫画 → 同一姿势落定`
  *(White flash → glowing line art → flash-cut 2D manga → settle into 3D model in the exact same pose)*
- **Strict lexical constraint**:
  - **USE**: `闪切` (flash-cut)
  - **BANNED**: `变形` (morph / transform / shape-shift) — causes melting, sticky transitions.
- **Pacing contrast (Bullet Time)**:
  Precede high-speed combat with a slow macro dolly shot:
  `子弹时间：微距贴着刀刃慢慢移` *(Bullet time: macro camera glides slowly along the blade edge)*.

### Principle 2: Specific anatomical targets (`攻击位置`) & color locking

Generic prompts like `机甲攻击巨龙` ("Mecha attacks giant dragon") produce repetitive, identical swings.

- **Multi-vector target rule**: Every strike in a combo must pair an **exact anatomical target** with a **directional slash vector** (alternating up, down, left, right):
  1. `额头 · 横切` — Forehead: Horizontal slash
  2. `头顶 / 两角之间 · 斜劈` — Crown / Between horns: Diagonal downward chop
  3. `龙头 / 下颚 · 由下往上挑` — Dragon head / Jaw: Upward rising slash (with ground sparks)
  4. `前腿 / 龙腹 · 低位撞` — Front leg / Belly: Low-angle collision strike
- **Skill color-locking (`一个技能锁一个颜色`)**: Bind one distinct color per VFX element to prevent visual muddiness:
  - Blade Energy: Violet (`刀光 紫` / `#A855F7`)
  - Whirlwind: Cyan (`旋风 青` / `#06B6D4`)
  - Tsunami / Water: Deep Blue (`海啸 深蓝` / `#1E3A8A`)
  - Dragon Flame: Orange-Red (`龙焰 橙红` / `#EA580C`)

### Principle 3: Velocity & force modifiers (`速度` / `加速度词`)

Standard movement verbs like `飞向` ("flies toward") generate slow, floaty trajectories (`软绵绵`).

- **Mandatory pre-action modifiers**: Prepend kinetic force tokens before movement verbs:
  - `瞬间` (instantly)
  - `极速` (at extreme speed)
  - `蹬地` (kicks violently off the ground)
  - `残影` (afterimage / motion trail)
  - `连闪` (consecutive rapid flashes)
- **Canonical syntax**:
  `机甲蹬地化作紫色残影冲上半空，绕龙连闪七次`
  *(Mecha kicks off the ground, turning into a violet afterimage shooting into mid-air, flashing seven times consecutively around the dragon).*

### Post-processing & frame schedule

Treat sub-second frame counts as NLE finishing targets applied after generation, not guaranteed model-native frame timing.

#### A. 0.3-second impact transformation (18 frames @ 60fps)

Slice the 2-second raw transformation into 5 rapid flashes (2–5 frames per style pass):

| Pass | Visual Filter / Shader | Chinese Term | Duration (60fps) | Time (sec) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Pure White Flash (`#FFFFFF`) | `白闪` | 3 frames | 0.05s |
| **2** | Inverted High-Contrast Line Art | `反色线稿` | 3 frames | 0.05s |
| **3** | 2D Manga Halftone + RGB Chromatic Aberration | `漫画 + 色散` | 5 frames | 0.08s |
| **4** | Deep Purple/Black Posterization (Threshold) | `色调分离` | 4 frames | 0.07s |
| **5** | Pure White Flash (`#FFFFFF`) | `白闪` | 2 frames | 0.03s |
| **6** | 3D Mecha Settles (Identical Pose Lock) | `3D 机甲落定` | Hold / Continue | — |

#### B. Climax explosion / tsunami impact

- **Rule**: Insert **3 pure white frames (`爆发前插 3 帧纯白`)** immediately before the climax impact or wave split.

### Reference implementation (Female Valkyrie Mecha vs. Dragon)

Preserve the user's surface handle format (`@Image 1` on Dreamina/ModelArk, or `@Image1` when the user's workflow specifies compact handles).

#### A. Keyframe binding prompts

- **`@Image1` (Human Start Frame)**: Medium close-up of a fierce female warrior with windswept black hair, arms crossed in a defensive katana stance, sleek black tactical armor, stormy ocean background, golden rim lighting, 3D CG render, 8k.
- **`@Image2` (Mecha Target Frame)**: Medium close-up in the exact same crossed-arm pose as `@Image1`. Female obsidian valkyrie mecha armor, angular wing thrusters, glowing violet chest core and visor, stormy ocean background, 3D CG render, 8k.
- **`@Image3` (Boss Anchor)**: Wide low-angle shot of a colossal white-maned Eastern dragon with golden horns and glowing orange eyes rising from dark ocean waves, 3D CG render, 8k.

#### B. Spatiotemporal planning JSON (`seed-110-temporal-v2.5`)

Use this schema when the user requests a structured spatiotemporal planning contract (strip JSON wrappers when delivering a paste-ready Dreamina prompt body):

```json
{
  "schema_version": "seed-110-temporal-v2.5",
  "project_metadata": {
    "title": "Valkyrie_Mecha_Dragon_Duel",
    "duration_sec": 12.0,
    "fps": 60,
    "aspect_ratio": "16:9",
    "color_locks": {
      "blade_energy": "violet (#A855F7)",
      "whirlwind": "cyan (#06B6D4)",
      "tsunami": "deep_blue (#1E3A8A)",
      "dragon_flame": "orange_red (#EA580C)"
    }
  },
  "reference_bindings": {
    "@Image1": "Female warrior in black armor, crossed-arm blade stance, ocean backdrop",
    "@Image2": "Obsidian valkyrie mecha in identical crossed-arm pose, violet core glow",
    "@Image3": "Colossal horned Eastern sea dragon emerging from ocean waves"
  },
  "temporal_schedule": [
    {
      "shot_id": "SHOT_01_FLASH_TRANSFORM",
      "time_range": "00:00.0 - 00:02.0",
      "references": ["@Image1", "@Image2"],
      "camera_kinematics": "Static locked medium close-up, micro-shake on impact",
      "action_prompt": "@Image1 女战士双臂交叉，紫色能量爆发。闪白 → 发光线稿 → 闪切 2D 漫画 → 同一姿势落定为 @Image2 3D女性暗黑机甲，胸口紫光闪烁。",
      "negative_constraints": "变形, slow morphing, melting mesh",
      "audio_anchor": "Electric surge, sub-bass drop, metallic armor lock"
    },
    {
      "shot_id": "SHOT_02_BULLET_TIME_BLADE",
      "time_range": "00:02.0 - 00:04.0",
      "references": ["@Image2", "@Image3"],
      "camera_kinematics": "Extreme macro dolly pan tracking slowly from hilt to tip along the katana edge",
      "action_prompt": "子弹时间，微距镜头贴着刀刃慢慢移动，刀光紫能量流淌，背景 @Image3 巨龙虚化。",
      "audio_anchor": "Time-dilation whoosh, crystalline blade ring"
    },
    {
      "shot_id": "SHOT_03_FOUR_POINT_COMBO",
      "time_range": "00:04.0 - 00:08.0",
      "references": ["@Image2", "@Image3"],
      "camera_kinematics": "Dynamic whip-pans and snap-zooms tracking 4 strike vectors",
      "action_prompt": "@Image2 极速攻击 @Image3 四个位置：1. 额头横切（刀光紫）；2. 头顶两角之间斜劈；3. 龙头下颚由下往上挑，擦出火花；4. 巨龙前腿低位撞击。",
      "audio_anchor": "Four rapid metallic slashes, heavy impacts, dragon roar"
    },
    {
      "shot_id": "SHOT_04_AFTERIMAGE_TSUNAMI_FINALE",
      "time_range": "00:08.0 - 00:12.0",
      "references": ["@Image2", "@Image3"],
      "camera_kinematics": "High-angle orbital tracking shot pulling back into ultra-wide reveal",
      "action_prompt": "@Image2 瞬间蹬地化作紫色残影冲上半空，在青色旋风与橙红龙焰中绕龙连闪七次，随后一刀紫光垂直劈开深蓝海啸巨浪。",
      "audio_anchor": "Sonic boom, seven teleport zaps, roaring tsunami split"
    }
  ]
}
```

#### C. Compiled bracketed prompts

Native Chinese Physics Prompt (Recommended):

```text
[00:00-00:02] @Image1 女战士双臂交叉，紫色能量爆发。闪白 → 发光线稿 → 闪切 2D 漫画 → 同一姿势落定为 @Image2 3D女性暗黑机甲，胸口紫光闪烁。
[00:02-00:04] 子弹时间，微距镜头贴着刀刃慢慢移动，刀光紫能量流淌，背景 @Image3 巨龙虚化。
[00:04-00:08] @Image2 极速攻击 @Image3 四个位置：1. 额头横切（刀光紫）；2. 头顶两角之间斜劈；3. 龙头下颚由下往上挑，擦出火花；4. 巨龙前腿低位撞击。
[00:08-00:12] @Image2 瞬间蹬地化作紫色残影冲上半空，在青色旋风与橙红龙焰中绕龙连闪七次，随后一刀紫光垂直劈开深蓝海啸巨浪。
```

English Prompt:

```text
[00:00-00:02 | Shot 1: Medium Close-Up, Locked Camera] @Image1 female warrior stands against ocean waves, violet energy erupting around her crossed arms. White flash -> glowing line art -> flash-cut 2D manga -> settle into @Image2 3D obsidian female mecha in the exact same pose, violet core glowing. (SFX: Electric surge, heavy bass impact, metallic lock).
[00:02-00:04 | Shot 2: Extreme Macro, Slow Dolly Pan] Bullet-time macro camera glides slowly along the katana blade from hilt to tip as violet energy and sparks ripple across the steel, with @Image3 giant dragon blurred in the background. (SFX: Slow-motion hum, blade ring).
[00:04-00:08 | Shot 3: Dynamic Action Tracking, Whip-Pans] @Image2 attacks @Image3 at extreme speed across four distinct anatomical targets: 1. Horizontal violet slash across the dragon's forehead; 2. Diagonal chop onto the top of the skull between the horns; 3. Upward slash from beneath the dragon's jaw kicking up orange sparks; 4. Low-angle collision strike against the dragon's front leg. (SFX: Four rapid energy slashes, heavy impacts).
[00:08-00:12 | Shot 4: Aerial Orbit to Wide Reveal] @Image2 kicks off the ground, instantly turning into a violet afterimage shooting into mid-air, flashing seven times consecutively around @Image3 amidst a cyan whirlwind and orange-red dragon flames, then plunging a vertical violet blade beam to cleave a massive deep-blue tsunami in half. (SFX: Sonic boom, rapid teleport flashes, massive wave split).
```

## Continuous-action prompting

Use when the user wants uninterrupted kinetic flow, reactive choreography, or adaptation of a successful action prompt. It also applies to a single-reference chase or playful physical sequence; combat, multiple references, and dense VFX are not prerequisites. Do not impose it on a quiet performance, product demonstration, or an explicitly paced scene with pauses.

Evidence boundary: this pattern is distilled from a user-supplied painterly action prompt reported to work well. The resulting video was not inspected. The mechanisms below are craft hypotheses, not proven causes of model performance, provider claims, or evidence that every named maneuver was generated. The example below is newly written, not a reproduction of the supplied prompt.

### Build connected motion

1. **Open on a concrete disruption.** Name the incoming obstacle, force, or movement that demands an immediate response. For a playful scene, this may be a companion rushing past rather than an attack. Respect any required opening frame; begin the disruption from that state instead of replacing it.
2. **Make the response feed the next action.** Write `incoming force or obstacle -> response/contact -> redirected momentum -> next action -> new spatial problem`. A pivot becomes a sprint, a landing becomes a bank, or a deflection becomes a counter. Avoid neutral-pose resets unless the user requests a pause.
3. **Overlap aftermath and anticipation.** Keep one dominant action readable while the previous action's residue persists and the next obstacle becomes visible. Leaves may still be falling as the subject approaches a turn. Do not treat overlap as permission for several unrelated actions per second.
4. **Give each subject a physical vocabulary.** Choose a few compatible behaviors, such as elastic bounds and low banking turns versus quick footwork and running vaults. Tie behavior to the requested character and observed design; do not import the source prompt's weapons, aggression, abilities, or outcome into another world.
5. **Make the camera follow a cause.** Follow the bank, landing, or approach with a move that reveals its path or contact. A brief wide reframe can restore geography while the subjects keep moving. An aggressive camera is not an instruction to scramble the action axis or add arbitrary cuts.
6. **Translate the artwork into motion.** Specify how the reference's medium depicts speed and impact: broken painted strokes following fur, flattened graphic leaves displaced by a landing, or ink-like wakes behind movement. Keep effects attached to physical triggers. Do not introduce magical energy merely because another prompt used it.
7. **Escalate toward a readable payoff.** Increase consequence or spatial difficulty, not merely the number of moves. Protect silhouettes, spacing, screen direction, contact visibility, and an observable final state. The final state may remain in motion if the requested ending allows it.

### Form and transfer example

Continuous prose is useful when connective language carries the choreography. Timed stages are equally valid when timing matters: carry momentum, positions, and aftermath across their boundaries. A stage boundary is not a compulsory stop. Follow the canonical timing rules in [prompt-architecture.md](prompt-architecture.md#long-scenes-and-timestamps); this pattern is not a blanket preference for longer prompts or for removing timestamps.

Illustrative motion passage, not a complete reference-bound submission:

> A gust drives a curtain of reeds across the runner's path, forcing a low sidestep that flows directly into a turn around the next tree. The camera tracks the turn from the outside, keeping the approaching root visible. Before the reeds spring upright, the runner clears the root and lands into the next stride; loose leaves rise from the footfall while the route ahead opens into view.

### Verification and pitfalls

Before submission, check that each transition has a physical bridge, each effect has an origin, the reference's visual language survives the action, and no neutral reset was accidentally inserted. Preserve subject counts, ownership, geography, requested outcome, and audio preferences. Run the normal generation prompt linter; passing establishes prompt checks, not rendered success.

When a render is supplied, inspect the opening motion, action-to-action continuity, readable contacts, subject/style stability, camera geography, and ending. Record missed instructions separately from inferred causes. If comparing prompt variants, keep references, story, settings, and budget matched; vary the connective choreography rather than adding length and extra techniques at the same time. Long move catalogs, prestige adjectives, and repetition are not demonstrated explanations for success.

## Untimed, rule-led worldbuilding vignettes

Use when the user wants everyday worldbuilding, an observational montage, or a prompt that defines generative rules rather than scripting every shot. This is a separate mode from continuous-action prompting: multiple cuts can accumulate meaning without forming one causal adventure. Do not apply it to a fight or the preceding task merely because a style example arrives in that conversation. When the user supplies an example to learn from, capture its reusable method; adapt the current project only when asked.

Evidence boundary: distilled from a user-supplied written example, not an inspected generated video. Its particular choice of 19 short cuts is an example-specific creative constraint, not a provider limit, a universal default, or proof of exact cut-count adherence. These are craft heuristics, not first-party capabilities. The guidance below summarizes the method rather than reproducing the source prompt.

### Contract and procedure

1. **Choose the organizing principle.** State what the piece explores: routine, a place's working life, a character's social presence, or ordinary encounters. Lock any requested cut count, but do not invent timestamps, a numbered shot list, or one continuous take. Untimed does not mean unstructured. Done when the model has a clear selection rule for every moment.
2. **Bind continuity, then define creative freedom.** Map the actual uploaded reference to character identity, visual design and style. Preserve established fictional role, temperament, moral alignment and relationships. If the user explicitly invites worldbuilding from a fictional design, allow compatible invention of routine, surroundings and social customs as creative proposals, not facts observed in the image. Do not infer real-person demographics, occupation, status or morality from appearance. Do not assert unknown fictional canon as established; retain ambiguity or author within the user's stated permission. Done when preserved facts and invented world detail are distinguishable.
3. **Direct selection rather than prescribe a plot.** Ask for varied, small, observable moments that reveal how the world works: maintenance, exchange, travel, etiquette, labor, leisure or use of shared spaces, selected only where compatible with the character and setting. Each cut should add a different environmental or social fact instead of repeating scenic portraits. The reference character can connect the moments without dominating every composition; surrounding inhabitants continue their own activity. Do not add a crisis, quest, exposition, climax or victory unless requested. Done when cumulative world understanding, not dramatic escalation, is the organizing outcome.
4. **Preserve tone without moral correction.** Ordinary life need not mean wholesome life. Established threatening characters can alter others' spacing, eye contact or behavior; established gentle characters can reveal their nature through small choices. Do not automatically redeem a villain, soften an unsettling world, or add spectacle. These are conditional examples, not instructions to invent an alignment from costume. Done when ordinary behavior retains the supplied characterization.
5. **Specify one coherent observer.** For this example's observational variant, use detached objective third-person framing, natural 28–40mm lens language, and restrained shoulder-mounted handheld motion. Describe subtle micro-jitter, shoulder drift, soft focus breathing, delayed reframing and brief reactive pans while keeping action legible. Exclude POV, camera acknowledgment, vlog or surveillance framing, gimbal glides, cranes and drones. Lens language is an aesthetic direction, not a guarantee of simulated optics. Do not append incompatible spectacle-camera directions. Done when the camera observes rather than performs.
6. **Close the sound and text contract.** For the supplied style, use only diegetic location sound: footsteps, tools, fabric, weather and other visible or spatially credible sources. Exclude intelligible background speech as well as dialogue, narration, music, subtitles and title cards. Do not add a musical emotional cue by habit. Done when sound supports the lived environment without explaining it.
7. **Deliver compact connected prose.** Order the prompt as premise and cut structure -> identity/style locks -> permitted world invention -> moment-selection rules -> tonal boundaries -> camera -> sound/exclusions. Use actual runtime reference handles, not the source example's placeholder. Avoid template headings, timers and exhaustive shot catalogs unless requested. This is an additional option, not a replacement for timed choreography, required anchors or exact event scripts. Done when every paragraph governs a useful choice and no hidden timed sequence has been imposed.

### Verification and failure guards

- Before delivery, check that the requested cut structure survives, no timestamps or major plot were inserted, distinct moments reveal world function, characterization is not automatically sanitized, and camera/audio rules remain mutually consistent.
- Keep duration outside the creative prompt. A dense cut count does not establish a suitable duration or make every moment readable; check against the requested runtime without silently changing an explicit count. This multi-cut video pattern is not a supplied storyboard grid, so do not apply the storyboard-panel recommendation as a cut-count limit.
- Run the normal generation prompt linter. A clean result verifies prompt checks only. If a render is supplied, inspect the actual cut count, reference/style continuity, diversity of routine moments, active background life, observational camera, lack of dramatic-plot drift, and diegetic-only sound. Record omissions rather than claiming successful execution from the written prompt.
- Transfer check: a supplied gentle character and a supplied feared antagonist should yield different social responses under the same observational architecture; neither should automatically become a hero montage or a fight. A quiet single-take request should not acquire 19 cuts merely because this pattern exists.
- Do not let human-default wording override a non-human design. Words such as "people" can pull a yokai, creature, or alien design toward ordinary human social life. Name the intended kind of inhabitant when the reference is not human, and keep that distinction in the selection rules.
- The source author later noted that cut count should change with the model and requested duration. Keep an explicit count when the user requires it, but do not treat 19 as portable to every runtime.

## Curiosity-driven character vignettes

Use when the user wants a short character study built from connected discoveries rather than either a scripted plot or an everyday-routine montage. This mode conflicts with everyday worldbuilding: it needs one underlying situation, visual cause and effect, and a payoff, and it should avoid generic daily routines. Do not combine the two unless the user explicitly asks for a hybrid.

Evidence boundary: distilled from a user-supplied written prompt example, not an inspected generated video. Its 10–15 cut range is an example constraint, not a provider limit or a default. Summarize the method; do not reproduce the source prompt.

1. **Open on a question.** The first image should create one simple unanswered situation. Later cuts answer it through discovery, reaction, progression, and small consequences. Done when a viewer can follow one situation without dialogue.
2. **Reveal character through behavior.** Use movement, instincts, habits, abilities, limitations, and interaction with the world. Do not explain the character, and do not force familiar human behavior onto a design that does not support it. Done when identity is shown rather than narrated.
3. **Make early details pay off.** Each cut adds a distinct visual idea while advancing the same situation. A detail introduced early should gain meaning later. End on a reveal, reversal, transformation, emotional beat, or satisfying visual payoff. Done when the ending depends on something already seen.
4. **Vary the view without breaking continuity.** Change scale, framing, environment, movement, tension, or information often enough that the cuts do not repeat. Keep objective third-person observation, readable handheld imperfection, and motivated camera movement. Use diegetic sound only unless the user requests otherwise. Done when variety serves the same story.
5. **Keep it separate from routine worldbuilding.** If the request is ordinary lived experience without a question or payoff, use the worldbuilding pattern instead. If the user supplies exact events, script those events rather than inviting invention. Done when the selected mode matches the requested outcome.

## Literal multi-shot control

Use when studying or writing a reference-led, multi-shot Seedance sequence where continuity, prop state, and readable action matter more than adjective density. These mechanisms are distilled from reviewed public Seedance 2.5 prompts and prompting notes. The corresponding videos were not inspected, so none of this is evidence of rendered fidelity or a provider guarantee. Do not reproduce those prompts, and do not name their authors in this skill. If a public example conflicts with [source-boundaries.md](source-boundaries.md) or [prompt-architecture.md](prompt-architecture.md), follow the canonical file.

Observed examples repeatedly separate reference jobs in prose: identity and style from one image, environment from another, and explicit exclusions for background, text, layout, and reference poses. They then give one premise and rhythm, followed by shots or beats that carry prop ownership, geography, and momentum across cuts. Useful mechanisms:

1. **Describe the transition, not only the destination.** A later view from behind does not by itself make a character turn. Name the turn, crossing, landing, or handoff that connects the states. The author reports that 2.5 can morph into an undescribed rear view; treat that as a reported failure mode, not a universal rule.
2. **Let action quantity control pace.** Too many actions in one short beat can read as sped up; too much time for a quick action can read as slow motion. This applies to untimed shot lists as well as timestamps. Do not compress a multi-minute story into one clip by adding more beats. Use integer-second ranges only when timing is required; do not copy decimal timestamps from public examples.
3. **Override a likely still misread before the action.** If a pictured object is alive, already worn, concealed, or must not transform, say so in the opening state. Equipment used later should already exist when the story requires it.
4. **Keep a prop and target ledger.** State exact counts, owners, one-time damage, and where each object remains. Give similar opponents one durable visual difference, and do not retarget or restore one after its stated outcome.
5. **Repeat a route only to change it.** A recurring escape, attack lane, or destination landmark should stay readable, then close, redirect, or pay off through a visible path change.
6. **Show speed through overlap.** Let the camera lose and reacquire a fast subject while earlier debris is still moving. Do not explain speed with clones, teleportation, or extra instances unless requested.
7. **Order cause before body response.** For an impact, show the strike, then the fold, slide, or recoil. Keep attached equipment attached through the fall unless the story removes it.
8. **End in a legible carried state.** Spectacle can resolve into an ordinary action, or the action can still be moving. Name which, and do not default to a victory pose.

Do not import these example habits: duration or aspect ratio written inside the prompt, placeholder handles such as `@[ref image]`, `Image1`, or `Image #1` instead of the active runtime's labels, angle-bracket character names in a prompt that also uses `<>` for sound effects, or a claimed universal prompt-character limit. The author reported rewriting one dense English dialogue scene in Chinese to fit more detail; the supplied provider documents do not establish a universal character cap, so do not state one.

## Split references by job

Give each active asset one primary job. Typical winning split:

- one identity / appearance lock (a multi-view character sheet when available);
- one world / silhouette / environment lock.

Do not let a single image own face, outfit, set, and camera at once. State what to inherit and what not to inherit on each `@Image` / `@Video` / `@Audio` line.

## Physics needs an origin

Any spark, bloom, particle, fabric tear, dust slipstream, or glow must name a physical cause: contact, friction, velocity, impact, wind, or a held prop. If the VFX reads as magic projection, beams, or aura, rewrite the **cause**, not the adjectives.

## Fight repair

If a fight is not working, replace the choreography. Keep identity, location, axis, and camera contract. Cut named techniques until every contact is readable. Do not patch with more style words.

## Speed-ramp cycle

When impact emphasis is needed and slow motion is compatible with the request, name the cycle in observable terms:

`real-time → burst / dash → short impact slow-motion → snap back to real-time`

Do not claim decimal-second or frame-accurate holds. Integer-second stage budgets remain the only timing grammar.

## Stage density

One generated clip gets one primary causal chain. Prefer fewer readable contacts over a catalog of named martial-arts styles. If the event cannot fit without crowding, split into generation then forward extension, or into sequential clips — do not stuff.

Chinese `阶段` / `开始时` / `主要事件` / `结束时` is the same as Stage N initial state / primary event / end state. Use that labeling only when the user writes in that form.

## Extension-ready last beat

When a sequel or forward extension is likely, land the last beat on:

- a readable boundary pose and motion direction, or a camera rest when compatible with the requested pace;
- leftover particles, dust, ash, or fabric that can still exist;
- a subject or threat that can still act.

The extension prompt restates the **observed** source-boundary state, then adds new action. It does not re-narrate the whole source clip.

## Multi-shot continuity craft

Source: three user-supplied written prompts studied on 2026-10-30 (a boutique comedy, a slow-motion/rewind gunslinger duel, and a cyborg hangar brawl). These are prompt-reading hypotheses. No generated result was reviewed. Use them for any `Shot N` prompt with recurring characters, props, or dialogue, in any genre.

- **Restate prop state in every shot.** Declare the starting state and the single instance once: "hangs alone on a hook from the start"; "her only gun, always in her right hand; her hip holster stays empty". Then restate location and holder in each shot where the prop is visible, also when nothing changed: "still hangs on its hook", "strap not yet on her shoulder", "still on her right shoulder", "holster empty". Give hands a declared entry state: "arrives empty-handed, arms free". This extends item 4 of [Literal multi-shot control](#literal-multi-shot-control) from a ledger to a per-shot restatement.
- **Tag each character on every mention.** Use the name plus one visible trait, and keep the same tag: "Kira, lilac buns"; "Dana, black bob"; "Kai, black mechanical arm". In a bilingual prompt, write the tag in the shot's language: `Kai，黑色机械臂`.
- **Isolate the speaker.** In a shot with several visible faces and one line, write "<Name> alone speaks" and give each listener a closed-mouth action: "Dana stays silent, lips pressed shut, one eyebrow twitching". This adds an observable performance to the listener rule in [prompt-architecture.md](prompt-architecture.md).
- **Keep air between bodies.** When two characters are close, ask for visible separation: "a clear gap between them"; "one body nearer the camera, the other clearly behind it with air between".
- **Keep the screen map and eyelines.** Anchor each character and set element to a fixed object and its screen side together: "the bag shelf at screen left". Screen side alone is fragile when the camera reverses; see [prompt-architecture.md](prompt-architecture.md#space-and-blocking-diagrams). Keep each character on the same side across shots. Point every offscreen look toward the place where the target was last shown. If the target has moved during a cut (a comic ellipsis), say so in the same sentence. For a reverse angle, say what stays hidden and refer back: "same side as Shot 5, his face hidden".
- **Cut on an action.** End each shot with "Cut as <observable action>" and open the next shot on its continuation. End the clip on a cut, not a fade: "the clip cuts mid-turn"; "the picture stays bright, no fade-out". This prevents a default fade or a settling pose.
- **Use one camera move per shot.** Name its direction and speed. Lock the camera for dialogue shots. Break this only under a stated global energy rule.
- **Scope rules to scenes.** Define a look (slow motion, grade, afterimages, sound treatment) once at scene level. Turn it off explicitly in the scene that drops it: "no afterimages". For a callback, cite the earlier framing: "framed as Shot 1".
- **Define an effect by contrast.** State what it is and what it is not: "five or six distinct see-through copies of her whole body, not speed lines".
- **Stylize damage to match the medium.** When the user excludes gore, replace it with a style-native material and keep the exclusion: "the back of his head bursts into pale lavender paint and black ink" with "no realistic gore, no blood". This follows the user's content choice. It does not change platform moderation.
- **Budget dialogue.** Keep spoken words to about 2.5 words per second of shot time. Use fewer when the same shot carries several physical actions. At 3 or more words per second, lengthen the shot or cut words. `prompt_lint.py` warns with `DIALOGUE_DENSITY`.
- **Check the Avoid list against the body.** "No freeze frames" conflicts with "hit-stop" or `定格` (literally a freeze frame). "No slow motion" conflicts with a speed ramp or `子弹时间`. Remove one side or rewrite the effect as an impact flash plus a camera jolt. `prompt_lint.py` warns with `NEGATION_CONFLICT`.
- **Mark must-hit beats.** In dense action, mark three or four exchanges per shot as required. Apply [Stage density](#stage-density) and item 2 of [Literal multi-shot control](#literal-multi-shot-control) before adding more.

## Do not import from public dumps

Leave these out of the creative prompt unless the user explicitly requires them:

- JSON / schema wrappers around the story;
- duration, aspect ratio, resolution, fps, or “4K masterpiece” boosters;
- quality-word piles (`cinematic, photorealistic, highly detailed`);
- music or BGM;
- Dreamina `@Image N` syntax mixed into a MiniMax H3 prompt;
- decimal frame promises.

Stills pipelines (Recraft / Seedream / Midjourney → Seedance) belong in upload notes, not in the Seedance prompt body.
