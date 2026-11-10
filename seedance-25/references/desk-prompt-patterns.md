# Desk Prompt Patterns: Action, Combat VFX, & Timing

Clip-desk production heuristics for kinetic action, bilingual combat VFX, continuous movement, four-mode pacing, and 2.5D letterbox compositing. Companion modules cover [vignettes, multi-shot continuity, conversational prosody, and reference-plate coverage](desk-continuity-and-coverage.md) and [ByteDance Seed training architecture and evidence boundaries](research-mechanics.md).

Written-prompt study provides craft hypotheses, not evidence of generated fidelity. These heuristics do **not** expand model capabilities, limits, prices, UI quotas, or API fields. If a heuristic conflicts with [source-boundaries.md](source-boundaries.md), [prompt-architecture.md](prompt-architecture.md), or [task-contracts.md](task-contracts.md), follow those files.

Standing clip-desk defaults unless the user overrides them:
- **Aesthetic scope:** apply a beauty-first look (ethereal, regal, romantic, non-grotesque) only to celestial, fairy, romantic fantasy, and stylized anime requests whose tone is otherwise unspecified; preserve gritty realism, historical drama, documentary texture, creature design, or gothic horror whenever the brief calls for them.
- **Audio & wrapper:** no music or BGM unless requested; deliver the paste-ready prompt body only.

## Contents

- [Action mechanics and framing](#action-mechanics-and-framing)
- [Reference-led kinetic action](#reference-led-kinetic-action)
- [Bilingual combat VFX & spatiotemporal prompting](#bilingual-combat-vfx--spatiotemporal-prompting)
- [Continuous-action prompting](#continuous-action-prompting)
- [Physics, fight repair, speed ramps, & extension beats](#physics-needs-an-origin)
- [Four-mode timing architecture and pacing control](#four-mode-timing-architecture-and-pacing-control)
- [2.5D letterbox frame-break ("pop-out") compositing](#25d-letterbox-frame-break-pop-out-compositing)
- [Do not import from public dumps](#do-not-import-from-public-dumps)

## Action mechanics and framing

Use these directing lessons for a leap, evasion, connected movement, or finishing strike when relevant. They also apply to simple action shots without requiring the dense kinetic-action mode below. Preserve the requested choreography, pace, camera restrictions, and outcome; railings, walls, and swords are examples, not required scene elements.

- **Load before release.** For an explosive grounded leap, show the body lowering deeply, hips and knees flexing over planted feet, then the legs driving against the ground before takeoff. Make the support contact and launch direction visible. Keep anticipation compact at a fast pace; a deep compression does not require a long pause or slow motion.
- **Make the defense feed the next move.** Connect evasion to an established environmental contact: a hand catches a railing and pulls the body around it, or a foot plants against a wall and pushes off into the next trajectory (`contact -> force/redirection -> release -> next movement`). Carry momentum and position forward without an unexplained reset. Verify that the surface is reachable and the gripping hand is free without changing weapon ownership.
- **Frame the near miss.** Let the camera track the evading face and arrive at an angle showing the face, passing blade, and narrow visible gap together at closest approach. Preserve separation through silhouettes and restrained motion blur rather than inserting unrequested slow motion or a freeze.
- **Reveal the final strike's reach.** Trigger a motivated pullback or cut to a wider view as the finishing attack travels so its origin, path, and farthest affected landmark remain legible. Widen the framing (not the aspect ratio) without inventing extra destruction, while respecting any continuous-shot lock.

## Reference-led kinetic action

Use this mode when the user wants dense cinematic control for a fight, chase, transformation, destruction, or effects-led sequence. Reuse the control mechanics, not a source prompt's characters, world, unsupported render flags, or story outcome.

Build in this order:

`reference jobs -> global locks -> force/effect system -> causal stages -> camera path -> escalation -> failure guards`

Give each image one primary job, state what it does not control, and lock identity, count, prop ownership, axis, palette, lighting direction, and two or three rigid environmental landmarks.

### Causal force and VFX grammar

For every important attack or effect, write:

`preparation -> acceleration -> contact/trigger -> force transfer -> visible material response -> residue -> recovery`

Valid origins include contact, friction, velocity, impact, wind, or a named energy trigger. Targets do not burn or shatter before the strike reaches them. Replace vague intensifiers ("powerful") with body mechanics, impact recoil, and environmental displacement.

### Dense stage pattern

For an explicitly timed maximal action pass, use consecutive integer-second windows:

```text
0-3s — <beat name>
Initial state: <blocking, prop state, and camera state>.
Action: <preparation -> contact or trigger -> consequence -> recovery>.
Camera: <target/start> -> <path and speed change> -> <end framing and visible result>.
End state: <observable state carried forward>.
```

Keep up to three connected sub-beats inside one window; split separate techniques into distinct shots or a follow-on extension.

### Escalation and scale

Escalate from distant silhouettes -> mid-ground threat -> foreground elite contact -> arena-scale consequence -> aftermath hook. Keep distant crowds simple and reserve detailed anatomy and hit response for foreground subjects. When a fight render looks muddled, simplify the choreography until each contact reads rather than stacking style adjectives.

### Reciprocal combat and action-driven travel

For an evenly matched duel, build exchanges around `attack -> defense -> counterattack -> recovery or regained initiative` so defenses redirect momentum into the next move. Preserve a requested victor; unless the user asks for a cliffhanger tie, never end a fight on a frozen mutual clash (`STALEMATE_CLASH_ENDING`).

When combat travels across arenas, make each location change the consequence of a visible physical force (`departure landmark -> force/locomotion -> visible route -> arrival state`), or use an action-triggered white-flash hard cut (`白闪硬切`: end Shot $N$ on `Cut at the instant the stomp lands` and open Shot $N+1$ already mid-exchange in the new arena without animating mushy background melting). In aerial action, name the propulsion source that alters altitude (surface rebound, wing/thruster impulse, or energy recoil).

### Camera continuity and contact visibility

Tie each camera move to an action trigger and framing purpose. A pseudo-one-take across viewpoints needs an explicit physical bridge (debris wipe, roof edge, cloud bank, waterfall curtain, or whip pan) plus a defined arrival composition. Make weapon or fist contact readable before the largest effect bloom, keeping silhouettes and assigned energy colors distinct. When slow motion or hit-stop is excluded, convey impact via a two-frame flash, camera jolt, recoil, shockwave, and uninterrupted follow-through.

## Bilingual combat VFX & spatiotemporal prompting

Seedance 2.5 is natively bilingual, and high-velocity anime impact frames and martial-arts kinematics carry strong Chinese supervision in its training corpus.

### Key execution rules

- **Disable external prompt-enhance rewriters on flash-cut jobs:** Middleware rewriters often translate `闪切` (flash-cut) into generic English `transform` / `morph`, triggering slow mesh melting.
- **Targeted bilingual token injection:** In stylized anime/CG combat, pair clean reference bindings with sharp Chinese impact tokens (`闪切`, `两帧黑白冲击帧`, `化作残影`) when helpful, or keep pure English for readable `8–12` shot choreography.

### Principle 1: Impact frames (`冲击帧`) & transformation logic

Raw unguided transformations take ~2 seconds and melt geometry. Use hard style-cut tokens in the prompt:

- **Formula:** `闪白 → 发光线稿 → 闪切 2D 漫画 → 同一姿势落定` *(White flash -> glowing line art -> flash-cut 2D manga -> settle into target armor/mecha in the exact same pose)*.
- **Lexical rule:** Use `闪切` (`flash-cut`); avoid `变形` (`morph` / `shape-shift`, flagged by `MORPH_TOKEN_RISK`).
- **Bullet-time contrast:** Precede a burst combo with a slow macro blade glide (`子弹时间：微距贴着刀刃慢慢移`).

### Principle 2: Specific anatomical targets (`攻击位置`) & color locking

Generic phrasing (`机甲攻击巨龙` / "Mecha attacks giant dragon") yields repetitive swings. Pair an **exact anatomical target** with an **alternating directional slash vector**:
1. `额头 · 横切` — Forehead: horizontal slash
2. `头顶 / 两角之间 · 斜劈` — Crown / between horns: diagonal downward chop
3. `龙头 / 下颚 · 由下往上挑` — Jaw: upward rising slash kicking up sparks
4. `前腿 / 龙腹 · 低位撞` — Front leg / belly: low-angle collision strike

Bind **one distinct color per VFX skill** (`一个技能锁一个颜色`), e.g. violet blade energy (`#A855F7`), cyan whirlwind (`#06B6D4`), deep-blue tsunami (`#1E3A8A`), orange-red dragon flame (`#EA580C`).

### Principle 3: Velocity & force modifiers (`速度` / `加速度词`)

Replace floaty verbs (`飞向` / "flies toward") with grounded launch mechanics (`瞬间`, `极速`, `蹬地`, `化作残影`) while keeping combo counts physically readable (`绕龙高速连闪三次` / three rapid aerial arc passes — never 7+ high-frequency flashes inside one 4s window).

### Post-processing NLE frame schedule

Sub-second frame counts are **post-generation NLE finishing targets** (e.g., slicing a generated flash transition into 3f white `#FFFFFF` -> 3f inverted line art -> 5f manga halftone -> 4f purple/black posterize -> 2f white flash at 60 fps, or inserting 3 pure-white frames immediately before a tsunami split), never guaranteed model-native frame accuracy.

### Reference implementation (Valkyrie Mecha vs. Sea Dragon)

If an upstream pipeline uses a planning JSON (`seed-110-temporal-v2.5`), strip the JSON wrapper, `fps`, `aspect_ratio`, `duration_sec`, and decimal seconds before submitting to Dreamina or ModelArk. Both compiled prompts below use spaced `@Image N` handles, explicit role bindings, integer-second windows, `<SFX>` angle brackets, and `No subtitles.` so they pass `prompt_lint.py` cleanly:

#### Compiled Chinese Prompt

```text
[参考绑定]
@Image 1 仅定义黑甲女战士的面部与交叉持刀起始姿态；不要使用 @Image 1 的静态构图锁定后续运镜。
@Image 2 仅定义暗黑女武神机甲的棱角翼推进器与紫光胸核；不要使用其他人物。
@Image 3 仅定义白鬃金角东方海龙的体型与橙红龙瞳；不要将其缩为普通小怪。

[分镜列表]
镜头 1 (0-2s): 中近景固定机位微震。@Image 1 女战士立于怒海前双臂交叉，紫色刀能瞬间炸开；闪白 → 发光线稿 → 闪切 2D 漫画 → 同一姿势落定为 @Image 2 3D暗黑女武神机甲，胸核紫光亮起。<电流暴涌、低频重击与机甲金属锁扣声>
镜头 2 (2-4s): 极微距慢推镜头。子弹时间贴着武士刀刃从刀镡滑向刀尖，紫色能量流淌，后景 @Image 3 巨龙盘旋于海雾中。<时间放缓低鸣与清脆刀鸣>
镜头 3 (4-8s): 高速跟拍与急摇切换。@Image 2 极速突进连续劈击 @Image 3 三个部位：1. 额头紫光横切；2. 两角之间斜劈压顶；3. 下颚由下往上挑起橙色火花直撞前腿。<三次密集金属斩击、重压爆响与龙吼>
镜头 4 (8-12s): 高空环绕拉远至超广角。@Image 2 猛然蹬踏海面化作紫色残影冲天而起，在青色旋风与橙红龙焰间绕 @Image 3 高速折跃三次，随即垂直劈下一道紫光刀柱将深蓝海啸巨浪一分为二。<音爆、三次折跃破空声与巨浪轰然裂开声>

[音频与排除]
全片仅含机甲斩击、风浪与海龙环境音效，无背景音乐，无字幕。避免网格融化变形与静止对波僵持。
```

#### Compiled English Prompt

```text
[Reference Roles]
@Image 1 defines only the black-armored warrior's facial features and crossed-katana opening stance; do not lock later shots to @Image 1's static framing.
@Image 2 defines only the obsidian valkyrie mecha's wing thrusters and glowing violet chest core; do not add extra pilots.
@Image 3 defines only the white-maned golden-horned sea dragon rising from dark ocean swells.

[Shot list]
Shot 1 (0-2s): Locked medium close-up with impact micro-shake. The @Image 1 warrior braces her crossed arms above stormy waves as violet energy erupts; white flash -> glowing line art -> flash-cut 2D manga -> settle in the identical crossed-arm pose as the @Image 2 3D obsidian valkyrie mecha with violet chest core blazing. <Electric surge, sub-bass drop, crisp metallic armor lock.>
Shot 2 (2-4s): Extreme macro slow dolly along the katana edge from hilt to tip in bullet time as violet sparks ripple down the steel and the @Image 3 sea dragon looms in the misty background. <Low time-dilation hum, crystalline blade ring.>
Shot 3 (4-8s): High-speed tracking camera with motivated whip-pans. @Image 2 lunges into @Image 3 across three distinct strike vectors: horizontal violet slash across the dragon's forehead, diagonal chop between the golden horns, and rising uppercut beneath the jaw kicking up orange sparks into its front leg. <Three heavy metallic slashes, concussive impacts, deep dragon roar.>
Shot 4 (8-12s): Aerial orbit pulling back into an ultra-wide reveal. @Image 2 kicks violently off the wave crest as a violet afterimage, arcs three times around @Image 3 through a cyan whirlwind and orange-red dragon flame, then drives a vertical violet blade beam straight down to split a towering deep-blue tsunami wave in two. <Sonic boom, three rapid air-step cracks, roaring ocean cleave.>

[Audio & Exclusions]
The audio contains only metallic combat impacts, storm waves, and dragon foley; no background music or score. No subtitles. Avoid slow mesh morphing or stalemate freezes.
```

## Continuous-action prompting

Use when the user wants uninterrupted kinetic flow or reactive choreography, including single-reference noncombat chases and playful physical sequences. Distilled from a user-supplied painterly action prompt (video not inspected; craft hypothesis only).

1. **Open on a concrete disruption** demanding an immediate physical response.
2. **Make the response feed the next action:** `incoming obstacle -> contact/evasion -> redirected momentum -> next action -> new spatial problem`, avoiding neutral-pose resets.
3. **Overlap aftermath and anticipation:** leaves or sparks from Beat A are still settling as the runner banks into Beat B.
4. **Assign distinct physical vocabularies** (elastic bounds and low banking turns vs. heavy vaults) grounded in each subject's anatomy and costume.
5. **Follow causes with the camera** and use brief wide reframes to keep landmarks legible without scrambling the 180-degree axis.
6. **Translate the reference's artistic medium into motion** (broken painterly brush wakes, ink splatters, or cel smears attached to physical contact).
7. **Escalate spatial difficulty toward a legible payoff.**

Illustrative passage (not a standalone reference-bound prompt):
> A gust drives a curtain of reeds across the runner's path, forcing a low sidestep that flows directly into a banking turn around the next trunk. The camera tracks from the outside, keeping the exposed root ahead in frame. Before the reeds spring upright, the runner vaults the root into the next stride as loose leaves lift behind the footfall.

## Physics needs an origin

Any spark, bloom, particle, fabric tear, dust slipstream, or glow must name a physical cause: contact, friction, velocity, impact, wind, or a held prop. If VFX drifts into generic magic aura, rewrite the **physical trigger**, not the adjectives.

## Fight repair

When a fight render muddles choreography, keep identity, location, axis, and camera contract intact and **reduce named techniques until every contact reads**. Do not patch weak mechanics with extra style adjectives.

## Speed-ramp cycle

When slow motion is compatible with the brief, write the observable cycle (`real-time -> burst/dash -> brief impact slow-motion -> snap back to real-time`) using integer-second windows only, and scope any single exception explicitly (`no slow motion except one brief speed ramp at the final impact`) so `NEGATION_CONFLICT` does not trigger.

## Stage density

Give one generated clip one primary causal chain. Chinese `阶段` / `开始时` / `主要事件` / `结束时` maps directly to `Stage N` `Initial state` / `Primary event` / `End state`; use Chinese headers when authoring in Chinese.

## Extension-ready last beat

When forward extension is planned, land the closing beat on a readable boundary pose and travel vector, residual particles/dust/fabric motion, and an active subject or horizon landmark. The follow-on extension prompt restates that **observed** boundary state and adds new action without re-narrating the source clip.

## Four-mode timing architecture and pacing control

Source: nine public Seedance 2.5 prompts studied on 2026-11-02 plus inspected 30-second renders (2026-11-02 & 2026-11-03). Choose one timing mode matched to the scene's physical rhythm:

### Mode 1: Untimed action-quantity pacing (`Shot N` without timestamps)
- **Why omit `(0-3s)` brackets in continuous action:** Fixed second brackets can cause the model to pad single strikes into floaty slow motion or clip multi-hit exchanges mid-swing. State shot count and approximate duration once in `[Brief]`, leave `Shot N:` untimed, and end each shot with `Cut as <mid-motion trigger>` (`切于<动作>`).
- **Mode 1a — Readable Choreography (`8–12 shots / ~30s`, `~2.5–3.75s` per shot in the user's language — DEFAULT for fights & chases):** Give each shot one complete martial or pursuit phrase (`load/wind-up -> strike or active catch lunge -> contact or narrow miss -> recoil/redirection`) so choreography reads cleanly without generator-transition flash clutter. For long fluid master brawls (`4 shots / ~30s`), punctuate the middle of a 7s exchange with one brief `Quick detail cut` (`快速细节切`: squinting eyes, boot sole filling lens) before returning to the wide clash.
- **Mode 1b — Hyper-Cut Sakuga Blitz (`16–24 shots / ~30s`, `~1.2–1.8s` per shot in compact Chinese — OPT-IN):** Use only when the user explicitly asks for rapid-fire `>= 12`-shot anime montage cuts or Chinese combat prompting. Pure Chinese role bindings (`@Image 1 仅定义…；不要使用…`) lint natively in `prompt_lint.py`. Give each `Shot N:` one strike + one material reaction + immediate cut trigger, and dedicate the final 4–5 shots to a one-way finishing chain (`破招 -> 破防重击 -> 击飞砸落 -> 法阵崩碎 -> 胜者前景落定、败者后景倒地`).

### Mode 2: Accordion timed pacing (`Shot N (start-ends)`)
- **When to use:** Rhythmic kata, anime OPs, and structured multi-angle comedy/narrative beats.
- **Budget seconds like an accordion (never flat `4–6s` blocks across action, `SLUGGISH_UNIFORM_TIMING`):**
  - **`1s` micro-windows (`6-7s`, `15-16s`, `24-25s`):** Single snap strikes, grabs, foot stamps, kiai snap-zooms, or impact bursts.
  - **`2–3s` phrase windows (`0-3s`, `10-13s`, `20-22s`):** Complete movement phrases, near-miss lunges, 180° turns, or macro prop inserts.
  - **`4–5s` dialogue windows:** Reserved for spoken lines. Cap any non-dialogue final capture or victory reaction to **at most the final `2–3 seconds` (`27-30s`)** so the story never finishes early and stalls on a 10s hold.
- **Refinements:** (1) Group 3–4 sub-second micro-angles inside one `3–4s` window (`0-3s: Rapid sequence of three connected angles: 1... 2... 3...`); (2) bridge unbroken tracking moves across timestamp boundaries (`Continue that same tracking shot across the time boundary without a cut; no new run-up or position reset`); (3) set internal speech ceilings on long dialogue shots (`Finish speaking by 28s; hold in silence until 30s`).

### Result-backed notes: 20-shot magic duel vs. 30-second forest-spirit chase (2026-11-02 & 2026-11-03)

Inspected via `ffprobe`, `ffmpeg` `scdet=threshold=12`, `volumedetect`, and 2–4 fps contact sheets on two 30.05s renders (`854x480`, 24 fps, `.mov`):

1. **20-shot compact Chinese magic duel (opt-in Mode 1b benchmark):**
   - **What held (`00:00–29.0s`):** 19 clean cuts (`~1.5s`/cut), 2D ink-and-watercolor medium, exact character details (`@Image 1` horns/red scarf/gold necklace; `@Image 2` six golden vertical eyes/ring cloak), detaching gravity orbs (`04.5–07.5s`), canopy spear rain (`13.5–15.0s`), 3-hit mid-air combo (`18.5–20.0s`), and two-frame B&W impact flash (`26.6–26.7s`).
   - **What failed (`29.0–30.05s`):** Writing Shot 20 as a mutual fist-vs-spear clash and glare lock (`硬生生对撞…死死对视`) froze the final `0.8s` in a split-screen stalemate (`STALEMATE_CLASH_ENDING`). Fix: dedicate the last 4–5 shots to a decisive one-way knockdown chain.
2. **30-second painterly forest-spirit chase (`SLUGGISH_UNIFORM_TIMING`, `PASSIVE_PURSUIT_RISK`, `OPENING_SETTLE_IN_ACTION`):**
   - **Initial failure:** Zero cuts after `09.0s` left a `10.5s` static bubble hold (`19.5–30.05s`); passive chase verbs produced stiff upright jogging (`02.5–05.0s`); lacking an affirmative ground lock ran the floor-gown nymph vertically up a tree trunk (`08.0–11.0s`); and `@Image 2`'s closed-eye portrait plus chest-centered bubble froze her face.
   - **6-shot timed repair (`dreamina-2026-11-03-3417...mp4`):** Fixed all 5 cut boundaries, ground-plane lock, active puddle/log lunges, and unobstructed right-side bubble smile (`26.7–30.08s`), yet `"settling briefly... before the chase erupts"` still wasted `0.0–3.0s` standing still (`OPENING_SETTLE_IN_ACTION`) and uniform `5–6s` blocks kept cameras gentle.
   - **Takeaway:** Open fast chases *in medias res* with zero settle beat, pair every pursuit beat with upper-body near-miss catch mechanics, state vertical ground-vs-canopy separation affirmatively, override closed reference eyes (`wide-open amber eyes actively tracking`), and keep `~2.5–3.5s` shots (`8–12` cuts) or accordion `1–3s` windows with the final capture capped to `27–30s`.

### Mode 3: Nested one-take sub-beats & `1s` hinge windows (`Shot 1 (0-30s):` + internal ranges)
- Declare `Shot 1 (0-30s): [Front camera of her phone, one continuous take]`, subdivide into consecutive integer-second sub-windows (`0-4s:`, `4-8s:`, ...), carve dedicated **`1s` hinge windows** for physical locomotion (`8-9s: One step brings her to the shelf`) or sudden room-sound cutoffs (`24-25s: One second of total silence`), and veil in-shot facial transformations with a timed **autofocus hunt** (`25-28s` blur while jaw transforms -> `28-30s` sharp snap-back).

### Mode 4: Proportional speed-contrast & inertia scaling
- Scale duration and shot count proportionally rather than relying on speed words alone (`9s across 3 shots` slow-mo with dust/afterimages -> `2s in 1 locked wide shot framed as Shot 1` fast rewind -> `4s in 1 panning wide shot` real-time replay with `no afterimages`), and anchor extreme speed or heavy mass via **gravity/pendulum lag** (a knocked-over plant is still falling when the fast subject returns; a braking carriage stops while its suspended payload keeps swinging).

## 2.5D letterbox frame-break ("pop-out") compositing

Use when the user asks for an out-of-frame or letterbox pop-out effect:
1. **3-layer back-to-front compositing order:** (1) background/scene confined strictly inside the central window, (2) two static full-width solid-black horizontal letterbox bars (e.g. top and bottom 15%), and (3) selected foreground subject parts (blade, hands, hair, boots, flaring skirt) rendered **in front of** the black bars.
2. **Static bars, moving subject:** Keep both black bars screen-locked with straight horizontal inner borders that never shake, bend, or stretch when the inner camera pans or recoils, leaving black bar visible on both sides of overlapping limbs.
3. **First-second overlap + alternating breaches:** Establish the pop-out in `0–1s` (near-lens palm wipe or foreshortened blade lunge spilling across the lower bar) and alternate upper-bar flourishes with lower-bar sweeps.

## Do not import from public dumps

Strip JSON/schema wrappers, embedded `16:9` / `1080p` / `60fps` / duration parameters, generic quality-word piles (`masterpiece, 8k, photorealistic`), unrequested BGM, un-normalized wrapper handles (`<<<Image1>>>`, `@[ref]`, `<视频1>`), decimal timestamps, and upstream still-generator tool names (`Seedream`, `Midjourney`, `Recraft`) from the creative prompt body.
