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
