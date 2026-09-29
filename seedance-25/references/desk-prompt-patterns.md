# Desk Prompt Patterns

Clip-desk production heuristics distilled from public and user-supplied action prompts. Written-prompt study provides craft hypotheses, not evidence of generated fidelity. These heuristics do **not** expand model capabilities, limits, prices, UI quotas, or API fields. If a heuristic conflicts with [source-boundaries.md](source-boundaries.md), [prompt-architecture.md](prompt-architecture.md), or [task-contracts.md](task-contracts.md), follow those files.

Honor the user's standing clip-desk defaults unless they override them: beauty-first (ethereal, regal, romantic celestial / anime — not grotesque); no music or BGM unless they ask; paste-ready prompt body only.

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

## Do not import from public dumps

Leave these out of the creative prompt unless the user explicitly requires them:

- JSON / schema wrappers around the story;
- duration, aspect ratio, resolution, fps, or “4K masterpiece” boosters;
- quality-word piles (`cinematic, photorealistic, highly detailed`);
- music or BGM;
- Dreamina `@Image N` syntax mixed into a MiniMax H3 prompt;
- decimal frame promises.

Stills pipelines (Recraft / Seedream / Midjourney → Seedance) belong in upload notes, not in the Seedance prompt body.
