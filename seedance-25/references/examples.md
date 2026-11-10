# Source-Derived Example Patterns

## Contents

- [How to use these patterns](#how-to-use-these-patterns)
- [Basic and multimodal generation](#basic-and-multimodal-generation)
- [Multi-reference and long-scene patterns](#multi-reference-and-long-scene-patterns)
- [Editing patterns](#editing-patterns)
- [Extension patterns](#extension-patterns)
- [Anchor, storyboard, and blockout patterns](#anchor-storyboard-and-blockout-patterns)
- [One-click and transition patterns](#one-click-and-transition-patterns)
- [Performance, camera, and process patterns](#performance-camera-and-process-patterns)
- [Canonical submit-ready prompt examples](#canonical-submit-ready-prompt-examples)
- [BytePlus media-example index](#byteplus-media-example-index)

## How to use these patterns

These are structural distillations of every example family in the supplied documents and the linked official optimizer. They preserve the instructional mechanics without requiring the source's characters, wording, or aesthetic. Adapt the pattern to the user's actual story and materials; never copy an example's facts into an unrelated prompt.

## Basic and multimodal generation

### Ceramic process, text only

Use one subject and a two-step making action. Establish dawn studio light and material sheen. Begin at the hands/process, move closer to surface detail, then reveal the finished object in its final location. Preserve process sounds and room ambience.

Lesson: subject/action, environment, visible material treatment, camera path, and audio can form a complete compact prompt.

### Ceramic process with separate references

- Image A controls artist identity/clothing, not its background.
- Image B controls studio layout/light, not its people.
- Video A controls process pace and hand motion, not identity or scene.

Lesson: each asset owns one dimension; re-narrating an already accurate motion video can introduce conflict.

### Multiple views, one object

Assign front, left, right, and rear images to one folding product. State explicitly that all four define one entity and that only one entity appears.

Lesson: view count is not output-subject count.

### Panda timed nature clip

The BytePlus basic example uses a low handheld documentary view of a panda rolling down a detailed forest slope, then settling and reacting. Two consecutive ranges separate the rolling state change from the resting state. Camera, depth of field, light direction, environmental sound, and final pose remain explicit.

Lesson: timestamp blocks work best when each contains one dominant physical change and a visible landing state.

### Carpenter repairing one chair

Image references separate carpenter identity from chair structure; a video provides glue-and-press hand motion. The event begins with a loose joint and ends only after both hands release and the backrest remains secure.

Lesson: real processes need initial condition, operation, count control, and an observable proof of completion.

### Barista handoff

Separate barista identity, cafe scene, and pour motion. Use inside/outside counter blocking. End with the single coffee cup only in the customer's hands and both of the barista's hands released.

Lesson: handoff prompts must state exclusive final ownership.

## Multi-reference and long-scene patterns

### Museum roles

Map conservator, registrar, installer, and guide separately. Give the conservator a sample case, the registrar a record board, and bind lab/gallery scenes independently. Build one central profile for a recurring subject, then activate only required identities, props, motion, and scene material per scene.

Lesson: many references should behave like a cast/prop/location registry, not a collage request.

### Observatory data handoff

Bind an inspector, archivist, one recorder, two environments, an equipment-bay action reference, and one voice reference. Track a memory card from equipment bay to recorder, then transfer the recorder across a table. List one speaker while the listener's mouth remains closed.

Lesson: maintain entity count, ownership, spatial sides, and speaker responsibility across scene changes.

### Flower-shop packing

Stage 1 arranges/trims stems and ends with scissors returned. Stage 2 wraps and ties the bouquet, ending centered with the bow visible. Stage 3 transfers it to a pickup shelf, ending with both workers inspecting it.

Lesson: one state change and one end state per stage reduce ambiguity.

### Object-swap timeline

Three consecutive time ranges place a plate, remove it for a glass, then replace the glass with a vase. Each interval ends with only the current object centered.

Lesson: state subtraction matters as much as state addition.

### Exact time and relative delay

Use one named second for a single whip-pan or effect trigger. Use “N seconds after” for a delayed response such as lights shutting off after a button press.

Lesson: use time precision only for a critical beat; do not treat it as a frame edit.

## Editing patterns

### Local lighting edit

Make one video the sole master. During a small interval, change only one wall's cool light to warm light, let skin tone respond naturally, and preserve identity, clothing, pose, motion, room, camera, dialogue, and ambience.

### Folding-lamp replacement

Replace only one colored lamp with one referenced lamp. Exclude the reference background. Preserve desk, books, hands, and camera. The new lamp inherits every rotation, hand occlusion, appearance, and exit of the original.

### Moving-subject motion-slot replacement

Remove a bicycle and rider, insert one patrol vehicle, and make it inherit the same entrance time, route, speed, and occlusion. State that the original no longer appears.

### Greenhouse background replacement

Use the source for people/actions/camera. Use an image only for greenhouse layout, depth, ambient color, and light. Replace the background outside the subject silhouette; preserve facial features, clothing, expression, scale, position, and arm motion.

### Female aging performance edit

Preserve composition, camera, light, and performance rhythm. Modify only appearance and expression: continuous aging plus an observable emotional shift, without jump cuts, flicker, or identity drift.

Lesson: specify both the edit and the invariants that make it an edit rather than regeneration.

### Fight and environment replacement

Use one action video as the master, one castle image for environment, and separate images for two fighters. Replace identities and scene while retaining original action rhythm; bind restrained fog, dust, cloth response, metal reflections, and audio-beat synchronization.

### Remove music only

Remove only the original BGM. Preserve dialogue, lip sync, ambience, action sounds, visuals, camera, and edit rhythm.

### Change spoken language only

Translate one speaker or the whole dialogue, preserve meaning and speaking times, adjust lip movement, state `No subtitles` unless visible subtitles were requested, and preserve every other visual/audio category.

## Extension patterns

### Forward paper airplane

Continue from the observed last frame: same locked camera, airplane position/orientation, window background, light, and rightward motion. Let it glide out while the curtain reacts.

### Forward gardener and basket

Additional images define face, apron, and basket, but the source last frame controls the boundary. The gardener lifts the single basket to one shelf and releases it. End with exclusive shelf placement and no duplication.

### Backward empty greenhouse

Generate an establishing segment before people enter. Raise a shade and move mist/leaves, then end exactly in the source first-frame layout and camera state with no early character.

### Backward curator preparation

Use separate face, clothing, case, assistant-clothing, and room references. Show the curator approaching and opening one case; end at the source first-frame composition with assistants in their correct later positions. Do not allow source-only events to appear before the boundary.

### Bee pollination extension

Continue the flower footage by five seconds: bee arrival, macro pollen accumulation, takeoff, tracked flight, and pollination in a matching flower. Use `mov` and inspect the stitched boundary around the join.

Lesson: extension prompts can contain a short causal arc, but continuity at the actual boundary remains primary.

## Anchor, storyboard, and blockout patterns

### Perfumer first and last frames

Give opening and ending compositions separate exact anchor sentences. Additional images define the perfumer and bottle without replacing the anchors. One continuous mixing, stoppering, and placement action must arrive at the specified end.

### Pastry-chef first and last frames

Start with an undecorated cake and known tool positions; end with one finished two-tier cake centered and both hands released. Supplementary references define the chef and cake structure only.

### Four-keyframe paper airplane

Anchor desk, hand pickup, window pass, and shelf landing as four ordered states. Preserve one orange airplane, its folds, travel direction, classroom layout, light, and camera axis.

### Spirit-fish keyframes

The BytePlus example orders seven independent images through cloud mountains, a mountain town, a hall and pool, then a temple painting. It uses the first sentence to declare order and a unified illustration style.

Lesson: independent images provide stronger state ordering than one grid.

### Pottery storyboard grid

State four-panel reading order and exclude line art/labels. Use independent references for the artist and blue cup. Translate panels into wide setup, side process, detail close-up, and finished placement; add final documentary style and process audio.

### Robot/launch storyboard

Bind one nine-panel storyboard for approximate shot structure, a live-action grassland reference, a tall robot, and an elderly woman. Define each subject, environment, color-film treatment, explicit exclusions, nine shots, dialogue ownership, and a protective ending.

Lesson: a storyboard can direct plot and rhythm while identity and look come from separate assets.

Source-audit caution: this provider example reverses the robot/grandmother image labels in parts of its prose and contains conflicting hair/height descriptions. The rendered result demonstrates that strong visual assets can overpower contradictory text. Do not copy those contradictions as a template. Verify each image-to-subject assignment, keep one authoritative description per subject, and follow the user's explicit mapping; if an unresolved conflict affects a core identity, ask and stop under the mapping-confidence rule.

### Coarse blockout: guide and cart

Map a cylinder to the guide and a box to the cart. Inherit walking path, cart direction, one push-in, and cut points; replace geometry with referenced people, prop, and gallery. Preserve footsteps, wheels, and room ambience.

### Coarse blockout: fantasy journey

The BytePlus 30-second example uses a clay video only for camera, shot rhythm, blocking, and character motion, while ten images define successive fantasy states. It progresses from bedroom toy plane to sky, ocean, space, and back to sleeping child/book, with explicit timestamps and a return-to-origin ending.

Lesson: name every temporal/spatial dimension inherited from a complex blockout and every visual dimension not inherited.

### Fine blockout: kinetic sculpture

Preserve complete ring structure, rotation, pedestal, orbit, and cuts. Replace gray materials with brass and blue glass and replace the empty room with a gallery.

### Fine blockout: rooftop raccoon

Re-render a complete blockout as a small stealth-suited raccoon crossing a neon cyberpunk rooftop. Preserve structural motion and camera; replace scene/material/style; use environmental/action sounds without BGM.

### High-difficulty spaceship previsualization

The BytePlus page supplies an additional complex blockout example without a paired written prompt. Treat it as evidence that blockouts may contain dense camera, lighting, and action information; do not infer a new documented template from it.

## One-click and transition patterns

### Night-market one-click sequence

Give six images exact roles from entrance through group photo, optionally use one video only for rhythm/stickers/transitions, keep three identities consistent, constrain motion per image, and bind market, dish, and river audio.

### Puppy coffee-shop one-click sequence

Allow the model to arrange eight puppy images freely, preserve each original image, add only slight live-photo motion, and apply a hand-drawn doodle/cutout package with playful requested audio.

### Umbrella-to-skylight transition

Use one clip's ending umbrella/rain/push-in and another clip's opening skylight/upward move. Fill the frame with the umbrella, morph its circular edge into the skylight ring, transform red fabric to daylight, and fade rain into interior footsteps.

### Mahjong-to-city transition

At the end of the first clip, fly up, turn, and dive. Transform mahjong tiles into high-rise buildings while arriving at the second video's motion and composition. Preserve the source portions semantically.

## Performance, camera, and process patterns

### Actor after applause

Use applause as the trigger. Stop the fingers, shift gaze, keep shoulders tense, then exhale, relax, form a restrained smile, and let tears appear without leaving.

### Returned letter

Use a placed letter as the visible cause. Stop a cup gesture, look at the return mark, tighten brows, let the smile disappear, breathe, turn the envelope down, then deliver one exact line in a controlled voice.

### Camera translations

- Rack focus: foreground leaves soften as the background face sharpens.
- Shallow portrait: keep eyes/face sharp; turn jars/lights into circular bokeh.
- Tracking: match the skateboarder's speed; background wall blurs oppositely.
- Golden hour: specify warm low-angle light direction and long shadow path.
- Natural vignette: darken corners gradually without a hard border or altered central skin tone.
- Whip-pan: state the second, direction, full-frame occluder, cut point, and continued speed in the next scene.

### Humidifier demonstration

Show an empty/off initial state, filling below a maximum line, reassembly and one button press, then stable mist with intact components and no leaked water.

Lesson: convert “smart” or “reliable” into operations with observable outcomes.

## Canonical submit-ready prompt examples

Each fenced block below is a complete, lint-verified prompt body (`0` errors, `0` warnings under `scripts/prompt_lint.py`). Keep external parameters (`duration`, `ratio`, `resolution`, `omni_reference_task_type`, `output_format`) outside the prompt text.

### 1. Multi-reference narrative scene (chronological asset order + 3-tier hierarchy)

```text
[Brief]
Period fantasy drama in 6 shots across approximately 24 seconds: an astronomer discovers that a brass astrolabe responds to a bottled starlight moth.

[Style & Reference Roles]
Anamorphic 35mm live-action film, warm tungsten lantern light against deep midnight window light, natural film grain, grounded physical weight.
@Image 1 defines only Elara's facial features, silver-streaked braided hair, and indigo wool coat; normal human eyes; no glowing eyes; do not use @Image 1's background or static portrait pose.
@Image 2 defines only the engraved brass astrolabe's ring geometry and patina; do not use @Image 2's tabletop.
@Image 3 defines only the glass apothecary jar holding one pale-gold glowing moth; do not use @Image 3's background.
@Image 4 defines the stone observatory study's arched window, oak desk, and brass oil lamp.
Stage map: Elara stands behind the oak desk facing camera; the arched window sits screen left; the brass astrolabe rests center-desk beside the oil lamp.

[Shot list]
Shot 1 (0-4s): Medium shot inside the @Image 4 observatory, slow dolly-in. Elara, silver-braided indigo coat, lets her shoulders settle with a quiet breath, leans over the oak desk, and turns the outer ring of the @Image 2 brass astrolabe with her right thumb until its pointer clicks into a notch. <Crisp brass ratchet click, quiet night wind outside stone glass.>
Shot 2 (4-8s): Close-up low-angle insert on Elara's left hand setting the @Image 3 glass jar onto the oak desk six inches screen left of the @Image 2 astrolabe; the pale-gold moth flutters once against the glass wall, casting warm gold reflections across her knuckles. <Glass base thud on wood, delicate wing flutter.>
Shot 3 (8-12s): Extreme close-up on the @Image 2 brass astrolabe. As golden light from screen left hits the engraved rings, fine brass gear teeth unlock on their own and spin smoothly counter-clockwise, lifting the central arm upward. <Low resonant metallic hum, interlocking clockwork ticks.>
Shot 4 (12-17s): Medium close-up on Elara, silver-braided indigo coat, slow push-in. All facial expression lives in the brow and the eyes; the mouth is left natural. Her brows lift slightly as warm gold light reflects in her pupils; she pulls her hand back half an inch, pauses, then speaks softly in English in a quiet, awed conversational voice: {It remembers the sky.} Finish speaking by 16s; hold her silent gaze on the spinning rings until 17s.
Shot 5 (17-21s): Over-the-shoulder shot past Elara's right shoulder toward the desk and @Image 4 arched window. She uncaps the @Image 3 jar lid an inch; a thin thread of golden dust rises from the jar and arcs into the spinning @Image 2 astrolabe rings without obscuring her profile. <Cork unsealing pop, soft crystalline shimmer.>
Shot 6 (21-24s): Wide three-quarter shot across the @Image 4 observatory, slow pull-back. The @Image 2 astrolabe locks into an upright alignment pointing straight through the screen-left arched window toward the night sky while Elara rests both palms flat on the desk edge watching it hold steady. <Heavy brass lock clunk, quiet room tone.>

[Audio & Exclusions]
The audio contains only the spoken English line, brass clockwork foley, glass contact sounds, and quiet night room tone; no background music or score. No subtitles. Avoid extra people, floating props, or text overlays.
```

### 2. Readable choreography fight (`~3.3s` per shot, 9 untimed cuts over ~30s)

```text
[Brief]
High-speed 2D hand-painted ink-and-watercolor duel across 9 untimed shots (approximately 30 seconds): a horned crimson-scarf martial artist breaks through a six-eyed mage's gravity rings in a rain-slick shrine courtyard and wins decisively.

[Style & Reference Roles]
Pure 2D hand-drawn sakuga animation with textured sumi-ink brush lines, layered watercolor washes, and flat two-tone shadow planes throughout.
@Image 1 defines only Kael's curved dark horns, crimson scarf, sleeveless obsidian gi, and wide-open amber eyes (screen left); do not use @Image 1's background or standing pose.
@Image 2 defines only Vael's six vertical golden eyes, tall collar, and ochre ring-cloak (screen right); do not use @Image 2's background or static pose.
@Image 3 defines the rain-slick stone shrine courtyard, central stone lantern, and dark cedar treeline.

[Shot list]
Shot 1: Wide low-angle side-tracking shot opening directly in motion with zero pause. Kael, crimson scarf streaming, crouches deep onto wet flagstones and drives off his back foot in three explosive bounds, swinging a rising ember-orange heel kick at Vael's collarbone; Vael snaps one arm forward, deploying a deep-violet gravity ring that catches the heel in a spray of rainwater and skids Vael backward two paces. Cut as rainwater sheets off the vibrating ring.
Shot 2: Medium tracking shot orbiting 45 degrees clockwise. Using the ring's rebound, Kael twists mid-air, plants his left palm onto a wet stone balustrade, vaults over Vael's sweeping violet whip-slash by inches so the whip shears the stone rail cap behind him, and lands low on Vael's flank. Cut as carved stone chips fly past the foreground.
Shot 3: Medium-wide two-shot, brisk lateral dolly right. Vael spins his ochre cloak wide, detaching three spinning violet gravity rings; Kael drops beneath the first ring, shatters the second upward with an ember-sheathed forearm smash, and vault-kicks off the third ring straight toward Vael's chest. Cut as Kael launches off the third ring.
Shot 4: Tight three-quarter close-up tracking backward ahead of Kael's charge. Kael chambers his right fist at his hip as ember-orange fire spirals tightly down his forearm; Vael's six golden eyes widen behind a double-layered violet barrier. Cut at the instant Kael's knuckles strike the outer barrier.
Shot 5: Wide profile shot across the central stone lantern. Kael's punch cracks the outer barrier, Vael counters with a downward gravity pulse that slams Kael's boots two inches into cracked flagstones, and Kael braces both knees before ripping upward with a twin-palm uppercut that splits the inner barrier cleanly in two. Cut as the barrier halves burst outward.
Shot 6: Dynamic over-the-shoulder tracking shot behind Vael. Reeling off-balance, Vael hurls a compressed violet sphere point-blank; Kael ducks his shoulder inside its arc so it grazes his scarf and blasts a background cedar trunk, leaving Vael's chest open at arm's reach. Cut as bark splinters erupt.
Shot 7: Medium low-angle impact shot with a snap push-in. Kael plants his lead boot in ankle-deep water and drives a spinning back-fist squarely into Vael's solar plexus with a two-frame black-and-white ink impact flash, lifting Vael off his feet as rain blows outward in a clear ring. Cut as Vael launches backward.
Shot 8: Wide whip-pan right across the @Image 3 courtyard. Vael crashes backward through the central stone lantern in a spray of dust and rain and slides to a halt against the shrine steps as every remaining violet ring flickers out. Cut as the lantern topples beside him.
Shot 9: Low-angle medium-wide payoff shot. In the left foreground, Kael straightens from his follow-through stance and exhales steam as ember light fades from his knuckles; in the right background, Vael remains slumped motionless against the wet shrine steps. <Heavy stone impacts, whipping cloth, crackling flame bursts, pouring rain.>

[Audio & Exclusions]
The audio consists solely of martial impacts, stone debris, flame bursts, and pouring rain; no background music. No subtitles. No 3D glossy CG shading or stalemate freeze.
```

### 3. `8n + 1` frame-preserving localized video edit

```text
[Edit Goal]
Edit @Video 1. Across the entire video, replace only the courier's matte-black motorcycle helmet with the weathered copper visor helmet in @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the courier's body, leather jacket, gloves, motorcycle, wet neon street, camera tracking path, lighting reflections, audio, and exact event order.

[Target Material Role]
@Image 1 defines only the replacement helmet's brushed-copper shell, riveted brow ridge, and dark amber glass visor. Do not use @Image 1's studio background or pedestal.

[Edit Objects and Scope]
Modify only the single helmet worn on the courier's head throughout @Video 1. Remove the original matte-black helmet completely so no black shell remains.
Except for the helmet explicitly replaced above, all other visible people, clothing, motorcycle parts, background vehicles, neon signs, rain reflections, and scene elements in @Video 1 remain unchanged and must not be replaced or removed.

[Timeline Inheritance]
The @Image 1 copper helmet inherits every head turn, lean angle, raindrop splash, neon highlight, motion blur, and frame boundary of the original helmet in @Video 1. Keep all remaining actions, camera movement, cuts, and street audio from @Video 1 unchanged.
```

### 4. Forward `.mov` extension

```text
@Video 1 is the source video to extend forward.
@Image 1 defines only the sunlit alpine valley vista waiting beyond the tunnel mouth; do not use @Image 1 to replace the opening boundary frame.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the last frame of @Video 1, maintaining the red steam locomotive's forward velocity along wet iron rails, cab-side tracking framing, drifting coal smoke, and rhythmic wheel-and-rail audio state.

0-4s: The locomotive bursts out of the dark stone tunnel mouth into crisp morning sunlight as exposure adapts smoothly, revealing the @Image 1 snow-dusted alpine valley and timber trestle bridge ahead while coal smoke whips past the cab window.
4-8s: The camera glides wider beside the driving wheels as the locomotive crosses onto the timber trestle over rushing glacial water at steady forward speed.

Throughout the extension, keep the single continuous red locomotive, brass boiler fittings, track gauge, camera direction, and steam-and-rail mechanical audio without duplication, splitting, background music, or subtitles. No music, no subtitles.
```

### 5. Timed two-person dialogue drama (upper-face isolation + clause micro-actions)

```text
[Brief]
Intimate 35mm live-action interior drama in 5 timed shots across 26 seconds: two brothers divide their late father's pocket watch over soup at a winter kitchen table.

[Style, Reference Roles, & Performance Locks]
Naturalistic 35mm European cinema, soft overcast north-window daylight from screen right, muted slate and warm oak palette, subtle handheld breathing motion.
@Image 1 defines only Lukas's lean face, short dark curls, and grey wool Henley (seated screen left facing right); do not use @Image 1's background or static pose.
@Image 2 defines only Tomas's bearded face, wire-rimmed glasses, and brown corduroy jacket (seated screen right facing left); do not use @Image 2's background or static pose.
@Image 3 defines only the tarnished silver pocket watch with a cracked enamel dial resting center-table; do not use @Image 3's background.
Performance locks: All facial expression lives in the brow and the eyes; mouths remain natural and relaxed. Neither man speaks with food in his mouth; each finishes swallowing before speaking. Normal human eyes; no glowing eyes.

[Shot list]
Shot 1 (0-5s): Medium two-shot across the scarred oak kitchen table; Lukas sits screen left with a soup bowl, Tomas sits screen right with the @Image 3 silver pocket watch untouched between them. In 0-1s both men settle naturally in the quiet room. Lukas sets his spoon gently in his bowl, wipes his thumb against his napkin, and lifts his eyes to Tomas. Lukas alone speaks in English in a quiet, matter-of-fact voice: {You stayed the winter.} <Spoon clink on ceramic, distant radiator hiss.>
Shot 2 (5-11s): Over-the-shoulder medium close-up past Lukas's shoulder onto Tomas, wire-rimmed glasses. Tomas looks down at the @Image 3 pocket watch, pushes it two inches across the oak grain toward Lukas, pulls his hand back, swallows once, and knits his brows slightly. Tomas alone speaks in English in a low, dryly affectionate tone: {He asked for you.} He exhales briefly through his nose and glances up: {Take the watch.}
Shot 3 (11-14s): Macro tabletop insert on the @Image 3 silver pocket watch near Lukas's grey wool cuff; Lukas's fingertips enter from screen left and rest lightly atop the cracked glass without lifting it yet. <Faint mechanical watch tick, wool sleeve brush on wood.>
Shot 4 (14-21s): Reverse over-the-shoulder close-up past Tomas's shoulder onto Lukas, grey wool Henley. Lukas keeps his eyes on the watch for a beat, blinks twice as his brow softens, closes his fingers around the silver case, and lifts only his eyes to meet Tomas's gaze. Lukas alone speaks in English in a warm, understated voice: {Then we split the orchard.} Finish speaking by 19s; hold Lukas's quiet half-nod in silence until 21s.
Shot 5 (21-26s): Medium two-shot matching Shot 1, gentle slow pull-back. Lukas slips the @Image 3 pocket watch into his palm while Tomas gives one crooked corner-of-mouth nod and reaches for his bread crust. <Chair creak, quiet winter room tone.>

[Audio & Exclusions]
The audio consists solely of the four spoken English clauses, ceramic and wood tabletop foley, faint watch ticking, and room tone; no background music. No subtitles. Avoid extra people or costume drift.
```

## BytePlus media-example index

The page's complete media set and observed output evidence are documented in [media-evidence.md](media-evidence.md):

- `image_001`-`image_008`: storyboard-versus-keyframe concept comparison.
- `image_009`-`image_014`: unsuitable and suitable storyboard examples.
- `image_015`-`image_021`: ordered spirit-fish keyframes.
- `image_022`-`image_030`: fantasy blockout/keyframe stages.
- `image_031`-`image_034`: rocket storyboard, environment, robot, and grandmother.
- `image_035`-`image_040`: pixel-wuxia keyframes/UI states.
- `image_041`-`image_043`: castle and two fighter identities.
- `image_044`-`image_051`: puppy coffee-shop one-click inputs.
- `video_052`: panda basic generation.
- `video_053`-`video_055`: coarse blockout, output, and synchronized comparison.
- `video_056`-`video_057`: fine blockout and cyberpunk raccoon output.
- `video_058`: difficult spaceship previsualization.
- `video_059`: storyboard-driven robot/launch output.
- `video_060`: ordered pixel-wuxia keyframe output.
- `video_061`-`video_062`: original and aging edit.
- `video_063`-`video_064`: original fight and reference-guided edit.
- `video_065`-`video_066`: original and Chinese audio/localization edit.
- `video_067`-`video_069`: source, generated bee extension, and stitched result.
- `video_070`: one-click puppy output.
- `video_071`-`video_073`: two sources and generated mahjong-to-city bridge.
