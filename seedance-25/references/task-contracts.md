# Task Contracts

This file is the canonical owner for executable generation, editing, extension, anchor, keyframe, storyboard, blockout, one-click, and transition contracts. Capability and parameter facts are owned by [source-boundaries.md](source-boundaries.md); general timing, blocking, camera, and audio grammar by [prompt-architecture.md](prompt-architecture.md); ambiguity and delivery by [optimizer-runtime.md](optimizer-runtime.md).

## Contents

- [Primary-task router](#primary-task-router)
- [Reference generation](#reference-generation)
- [Video editing](#video-editing)
- [Audio editing](#audio-editing)
- [Forward and backward extension](#forward-and-backward-extension)
- [First and last frames](#first-and-last-frames)
- [Ordered keyframes](#ordered-keyframes)
- [Storyboard grids](#storyboard-grids)
- [Coarse and fine blockouts](#coarse-and-fine-blockouts)
- [One-click video](#one-click-video)
- [Seamless transition](#seamless-transition)

## Primary-task router

Use one primary task per submitted prompt:

- **Generation** creates a new video. It includes text-only, multimodal reference, keyframe, storyboard, blockout, one-click, and bridge-transition generation.
- **Editing** changes named visual or audio content inside a source video while inheriting its timeline.
- **Extension** creates a new segment before or after a source boundary without editing the original.

The presence of a video reference does not automatically mean editing. A motion, style, camera, storyboard, or blockout video used to create a new work remains a generation reference.

If a request needs both edit and extension, use two prompts only when the operations are sequential. Step 2 must name the edited output of Step 1 as its new source master.

For a finished program longer than one documented 30-second video, keep generation as the primary task but return multiple clip contracts using [the long-program segmentation workflow](prompt-architecture.md#programs-longer-than-30-seconds).

## Reference generation

Use this scalable shape:

```text
[Generation Goal]
Generate <video type or core event>. The central subject is <subject>; the primary event is <summary>.

[Reference Material Roles]
@Image 1 defines <one entity and attributes>. Do not use <irrelevant content>.
@Video 1 defines <motion/camera/pace/effect>. Do not use <identity/scene/audio>.
@Audio 1 defines <speaker or sound category>.

[Unused Materials]
<Every known inactive number and the roles it must not control>.

[Subjects and Relationships]
<One-to-one identity, count, ownership, group, and spatial mappings>.

[Event Script]
Opening state: <state>.
Primary event: <event>.
Ending state: <visible state>.

[Maintain Consistency]
<Identity, count, clothing, structure, ownership, blocking, axis, camera, and audio>.
```

Do not invent style, camera, or audio simply to fill the form.

## Video editing

### Parameter behavior

For BytePlus ModelArk, use `ratio=adaptive`, `duration=-1`, and preferably `output_format=mov`. The output follows the input aspect ratio and approximately its duration; it may differ by up to about 0.3 seconds. Keep these settings outside the creative prompt.

### Source-video inventory

Before writing a visual edit, inspect the whole source video and inventory every visible category: named and unnamed characters, other live-action people, models or mannequins, animals, products and props, foreground objects, background subjects, visible text/subtitles/watermarks, scene/background, lighting, effects, and camera behavior. For each category, choose one explicit disposition: `replace`, `remove`, `modify`, or `keep unchanged`. Do not omit an unnamed person, model, prop, foreground object, or background subject merely because the user did not name it.

Objects the user did not ask to change remain unchanged by default. Include a whole category in replacement/removal only when the user requests that group-level scope or asks to retain only named targets. The inventory controls edit scope; it must not activate an unmentioned reference or override the user's target-material mapping.

If the full source cannot be inspected and only sparse previews are available, do not claim an exhaustive inventory. Name every user-specified modification and known preserved object, then use the closed fallback sentence:

```text
Except for the objects explicitly modified above, all other visible people, props, foreground objects, background subjects, text, and scene elements in @Video 1 remain unchanged and must not be replaced or removed.
```

If the user explicitly wants only named retained targets, replace that fallback with: `Except for the objects explicitly retained above, remove all other visible subjects from @Video 1. Do not add unspecified objects.`

### Documented edit-operation inventory

The BytePlus capability table documents these visual categories:

- **Add:** subjects, costumes, camera movements, special effects, and comparable visible elements.
- **Modify:** a whole subject, a subject part, style, background, color, lighting, material, motion, camera position, or comparable attributes.
- **Remove:** subjects, subtitles, watermarks, and comparable visible elements.
- **Local redraw/restore:** redraw or restore a named portion of the frame while preserving everything outside that region.

It documents adding, modifying, or removing vocals, music, and sound effects for audio editing. In every case, identify the exact target, interval/region, count when applicable, A-to-B change, inherited timeline, and categories that remain unchanged. Treat this inventory as documented scope vocabulary, not a guarantee that a dense combination of edits will succeed in one pass.

### Required contract

Every visual edit must include:

```text
[Edit Goal]
Edit @Video 1. Within <whole video or exact scope>, change only <original object/region> from <A> to <B>.

[Source Video Role]
@Video 1 is the sole editing master. It defines <people, scene, actions, composition, camera, occlusion, audio, and event order>.

[Target Material Role]
@Image 1 defines <target>'s <appearance, structure, material, or scene attributes>. Do not use <irrelevant content>.

[Edit Objects and Scope]
Modify only <object, quantity, region, interval, or attribute>.
Except for the objects explicitly modified above, all other visible people, props, and background elements in @Video 1 remain unchanged and must not be replaced or removed.

[Timeline Inheritance]
The target inherits every appearance, motion, occlusion, and exit of the original, including timing, path, duration, and speed changes.
Keep the remaining actions, camera, cuts, audio, and event order from @Video 1.
```

If the user explicitly wants only named retained objects, replace the local-preservation sentence with a closed removal instruction: retain the named targets, remove all other visible subjects, and add nothing unspecified.

### Editing variants

- **Local attribute change**: name the object/region, time interval, A-to-B property, environmental response, and all preserved content.
- **Subject replacement**: remove the original; bind the target reference; state count; inherit the same motion slot, path, speed, occlusions, entrance, and exit; state that the original no longer appears.
- **Cross-category replacement**: use the same motion-slot rule when replacing, for example, a person/bicycle with a vehicle.
- **Background replacement**: modify only the background outside the subject silhouette; inherit layout/depth/light from the environment reference; preserve subject identity, size, pose, action, and camera.
- **Add/remove**: state object count, position, first appearance, affected interval, and preserved surroundings.
- **Reference-image edit**: keep the source's action and rhythm; give each replacement subject and the new environment a separate reference role.

Do not reconstruct frame-level time ranges from a partial preview. Global master inheritance plus a few observable event conditions is safer. Wording increases the probability of alignment; it does not guarantee frame overlap.

The provider's own fight-edit example also shows that an explicit numeric mapping can lose to strong visual similarity: dark source clothing was matched to the dark reference outfit despite the requested cross-mapping. When two candidates differ mainly by light/dark appearance, use labeled or tightly cropped references and repeat the source-relative assignment (`source-left/source-dark -> @Image N`) in both the role and edit-scope sections. Locked duration and ratio do not imply unchanged resolution, codec, loudness, or bitwise source frames.

## Audio editing

Keep the source video as the sole editing master:

```text
[Edit Goal]
Edit @Video 1. Within <scope>, change only <speaker or sound category>.

[Source Video Role]
@Video 1 defines all visuals, action, lip-sync timing, camera, edit rhythm, other audio, and event order.

[Target Audio Role]
@Audio 1 defines <speaker/sound>'s <voice, line, ambience, effect, or music>. Do not use <irrelevant audio>.

[Audio Edit Scope]
Modify only <speaker, category, or interval>.

[Content to Preserve]
Keep <other dialogue, speaking times, lip sync, ambience, effects, visuals, camera, and rhythm> unchanged.
```

Examples of supported intent include adding/removing/replacing vocals, music, or sound effects; changing one speaker's language or voice characteristics; adding ambience; and translating dialogue. Preserve dialogue content and speaking times unless rewriting is explicit. Do not redesign the visuals because audio changes.

Dialogue localization can require new mouth shapes while the remaining face and shot stay aligned. Use `change only the dialogue and mouth articulation`, name the target language and any explicit user-requested voice/accent requirement, and compare paired face frames plus audio during QA rather than checking duration alone. Whenever dialogue remains or is added and the user has not requested visible subtitles, state `No subtitles.` If subtitles are requested, bind only their exact supplied text.

If the user requires a character to speak using `@Audio N` but supplies no dialogue text, or the audio cannot be transcribed reliably, preserve the character's speaking time and direct the spoken content to come from `@Audio N`; do not invent words. Written dialogue controls the words whenever it is supplied unless the user explicitly asks to reuse the reference audio's dialogue.

## Forward and backward extension

For BytePlus ModelArk, use `ratio=adaptive` and a user-set extension duration. For best audio-visual continuity, use `mov` for both the input/source video and output when the surface accepts it; selecting only an output container does not retroactively make a non-MOV source a MOV input. Direction is core information; ask when it is genuinely unknown.

For a subject visible at the source boundary, use only a name or role confirmed by the user. If the user supplied only `person` or `subject`, retain that neutral term; do not infer a profession, demographic, performance type, or story identity from action, posture, clothing, or filename.

### Forward

The generated segment begins at the source's observed last frame:

```text
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the last frame of @Video 1. Maintain <subject pose/orientation, prop position, layout, camera/composition, light, audio state, and motion direction>.

Then, <new action or event>.

Throughout the extension, keep <identity, clothing, props, layout, axis, camera, and audio> continuous.
Each subject remains the same continuous object without duplication or splitting. Keep anatomy, topology, and component count stable.
```

Additional references may define appearance, clothing, a new prop, or sound, but the source last frame owns the extension's opening image.

When the source was written with an extension-ready last beat (stable pose, leftover particles or dust, a subject or threat that can still act), continue from that observed leftover state. Restate the boundary; do not re-narrate the whole source clip or reset the fight.

### Backward

Describe the new preceding event first, then make the source's observed first frame the explicit end state:

```text
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source begins, <preceding event>.

The last frame of the extended segment naturally connects to the first frame of @Video 1. Match <pose/orientation, prop state, layout, camera/composition, light, audio state, and motion direction>.

Keep every subject one continuous instance. Do not allow later-only characters, props, or effects to appear early.
```

Review both sides of the boundary and the entire new segment, preferably as a stitched preview as well as a standalone extension. Natural continuity does not mean pixel-identical frames, identical audio level, or exact additive container duration. If the new event must reach a distinct destination, make that destination visually unmistakable or supply it as a reference; a polished close-up may otherwise complete the local action without traveling to the requested second location/object.

## First and last frames

Choose one route and name it correctly:

- **Strict ModelArk anchor:** assign `content.role=first_frame` and optional `last_frame` outside the creative prompt. This locks the output ratio to the first image; duration remains externally selectable. First and last images should have the same ratio to avoid stretching the last frame.
- **Semantic reference anchor:** keep each asset as `content.role=reference_image` and describe its intended opening/ending role in the prompt. This does not activate the strict ratio lock, and the generated frames may only resemble the reference images.

For the strict route, use exact standalone prompt declarations:

Use exact standalone declarations:

```text
@Image 1 is the first frame.
This frame defines <opening composition, subject position, pose, prop state, scene, and camera direction>.
@Image 2 is the last frame.
This frame defines <ending composition, subject position, pose, prop state, scene, and camera direction>.
```

Give every additional image one supplementary role and state that it does not replace either anchor composition. Describe one continuous action that begins naturally at the first frame and arrives at the last. Preserve identity, prop structure/ownership, scene layout, and camera direction.

The exact prompt sentence names the intended frame role, but prose alone does not create the strict lock; the external `content.role` does. For a semantic route, the prompt may still say `@Image 1 is the desired first-frame reference` and `@Image 2 is the desired last-frame reference`, but do not represent those images as strict timeline anchors, claim a ratio lock, or promise an exact match.

## Ordered keyframes

Prefer separate images over a multi-panel grid when visible state order matters:

```text
Use @Image 1 through @Image N in order as keyframes.

@Image 1 is the first frame.
@Image 2 defines the visible state at the end of Stage 1.
@Image 3 defines the visible state at the end of Stage 2.
@Image N is the last frame.

Pass through all states in order with continuous action. Maintain identity, object structure/ownership, layout, lighting, and axis.
```

Keyframes are semantic state anchors. They do not reproduce every intermediate frame or require static holds unless requested.

Independent keyframes normally remain `reference_image` assets. If the first and/or last image must become a strict boundary, promote only those assets to the corresponding strict `content.role`; otherwise the first/last wording in the sequence expresses semantic order and does not create a locked ratio by itself.

For exact logos, dates, interface copy, or long text, supply the finished text inside a keyframe and ask for clarity/stability. A shared canvas, palette, scale, and recurring subject across all keyframes makes the sequence easier to interpolate than independently styled frames.

## Storyboard grids

Use storyboards for high-level plot, shot order, approximate composition, and rhythm. Prefer 15 or fewer simple line-art panels with minimal text. Avoid noisy, oversharpened AI images, contradictions, and unreasonable camera designs.

`Shot N` is ordinary sequence syntax, not a strict keyframe mechanism and not limited to storyboard inputs. It may also organize a text-only or multi-reference plot when exact elapsed time is unnecessary. Preserve the number as a shot identifier rather than reading it as a camera angle.

```text
@Image 1 provides an <N-panel storyboard> for shot order and approximate composition. Read it <order>. Do not use its line-art style, labels, or placeholder people.
@Image 2 defines <character appearance>.
@Image 3 defines <prop or scene>.

Shot 1: <shot size, action, and state>.
...
Shot N: <closing event and final state>.

Use <final visual style>. Audio includes <dialogue, ambience, effects, or requested music>.
```

If strict states matter, switch to independent keyframes.

### Simplified concept-storyboard mode

When the input is explicitly a concept storyboard or keyframe design and the user wants the model to construct the connective plot, a simplified contract is allowed:

```text
@Image 1 is a concept storyboard. Follow its panel sequence and construct one complete, reasonable, coherent story using the shots in order. Use only its plot progression and approximate compositions; do not reproduce its line-art style, labels, arrows, or placeholder people.
@Image 2 defines <recurring subject or prop>, if supplied.
Keep <identity, count, ownership, scene logic, final visual style, and audio> consistent.
```

Use this simplified mode only when connective invention is authorized. If exact actions, dialogue, panel-to-shot mapping, or visible states are supplied, preserve them in explicit `Shot N` blocks. If strict state alignment matters, use independent ordered keyframes instead.

## Coarse and fine blockouts

A blockout is a generation reference, not automatically an editing master. Even when it already defines motion and space, the prompt must still state the intended final subjects, scene, primary action/event, visual style, and audio. The written event must remain consistent with the blockout's observable action, shot order, paths, and camera logic; if the requested event contradicts those controls, ask which one should govern rather than pretending both can be inherited.

For every final subject that has no additional image/video appearance reference, describe its user-supplied or otherwise neutral observable appearance and key distinguishing features in enough detail to render it consistently. Do not invent a name, age, demographic, profession, relationship, or personality from the blockout geometry. A shape-to-subject mapping still needs final appearance, count, and structural detail.

### Coarse blockout

Use simple geometry as a motion skeleton. It may control path, direction, blocking, entrances/exits, camera, cuts, lighting, sound rhythm, and spatial relationships.

Map each geometric object to one final subject or prop. State which temporal/spatial dimensions to inherit and exclude geometry, gray materials, empty scene, markers, axes, path lines, controllers, and camera frustums. Avoid incomplete appendage rigs; use arms, wings, or similar appendage geometry only when the complete action sequence is represented, because incomplete appendage motion can cause stiffness or structural misinterpretation.

```text
@Video 1 is a coarse blockout. Use only <paths, blocking, camera, cuts, lighting, sound rhythm, or space>. Do not use its appearance, materials, or scene.
<Shape A> corresponds to <Subject A>.
<Shape B> corresponds to <Prop B>.
@Image 1 defines <Subject A>.

<Event in final scene>.
Keep <named inherited dimensions> from @Video 1.
Use <final characters, scene, materials, style, and audio>.
```

### Fine blockout

Use complete clean modeling for re-rendering. Preserve structure, action, layout, camera, and cuts; replace character appearance, material, color, scene, or style.

```text
@Video 1 is a fine blockout. Preserve <structure, action, layout, camera, and cuts>. Do not use its gray materials, empty background, or production markers.
@Image 1 defines <subject material/appearance>.
@Image 2 defines <scene, material, lighting, or style>.

Re-render <blockout subject and scene> as <final design> while keeping <structure, motion, camera, and spatial relationships>.
```

## One-click video

Both the Lark and BytePlus documents describe this operation. The BytePlus capability table allows multiple images, multiple videos, or both; source assets may also be combined with an additional reference video. Organize them into a complete short sequence:

```text
Material roles -> Source order -> Motion amount -> Editing style -> Optional text/stickers/transitions -> Visual treatment -> Audio
```

State whether image/video order is exact or model-selected. Bind every recurring character/product. For images, define the allowed live-photo motion, parallax, push/pull, lateral motion, or local action. For source videos, define which original segment, motion, timing, or live audio is retained and whether trimming/reordering is allowed. Preserve source text, product structure, identity, and spatial relationships. A style/reference video should not leak its identities, locations, dialogue, or unrequested audio.

If every asset must appear exactly once, say so and give either an exact order or permission for model-selected order plus a preferred hold range. For strict still fidelity, constrain motion by channel: `camera push and parallax only; do not synthesize new body, limb, or product poses`. “Move slightly” can otherwise become substantial subject animation. Name any authorized text, sticker, or transition vocabulary and the audio mood; unrequested generated text should remain excluded.

## Seamless transition

Both supplied documents describe generating bridge content between two videos:

```text
Before video -> After video -> Trigger -> Camera path -> Visual transformation -> Arrival state -> Audio transition
```

Identify the ending subject/composition/motion/audio of `@Video 1` and the opening state of `@Video 2`. Use an explicit method: dive/reverse movement, character rotation, foreground occlusion, object morph, push/pull, or focus shift. Describe corresponding shapes/materials, speed, and the arrival composition. Preserve the original portions semantically, but do not promise a pixel-identical splice.

The bridge can add duration and change output frame rate even when both source segments remain visually close. If an orientation change is essential, name visible before/after landmarks and the exact direction of the turn; a generic “turn back” may be replaced by a smoother forward morph. Define one-to-one transformation correspondences when multiple source objects must each become distinct destination objects.
