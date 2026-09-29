# Prompt patterns

These are original craft examples, not official Kling prompts, reserved syntax, or generated-output evidence. Model capabilities and availability come from [capabilities.md](capabilities.md). Replace prose reference labels with actual attachment handles only when those handles are known. Put settings outside the prompt block.

## Text-to-video: complete action in one shot

Build one dominant event with an opening, visible change, and final state. Choose motivated movement rather than stacking lens and camera buzzwords.

Example settings: full Kling 4.0, text-to-video, 10 seconds, 16:9; subject to access.

```text
A continuous medium-wide shot inside a small pottery studio at sunrise. A potter lifts a newly finished bowl from the wheel, turns it toward the window, notices a thin crack, then gently places it on the workbench. Their pleased smile fades into a brief, quiet disappointment. The camera slowly pushes from the spinning wheel toward their face, keeping the bowl visible until it touches the bench. Warm window light reveals wet clay and fingerprints. Hear the slowing wheel, a soft ceramic tap, and the room's quiet ambience. No dialogue or music. End on their still hand beside the bowl.
```

## Image-to-video: visible motion without scene drift

Let the image supply appearance. Rank movement and distinguish the moving environment from fixed architecture. A locked camera does not mean frozen subjects. To request a loop, describe the return to the initial configuration, but do not promise a dedicated seamless-loop control.

Example settings: Flash, image-to-video, 8 seconds, 720p. Confirm any requested aspect-ratio/audio controls in the current surface.

```text
Animate the supplied garden image while preserving its painted texture, composition, pond outline, and stone structures. Keep the camera fixed. The two visible koi swim along separate curved paths beneath the surface, using clearly visible tail strokes and small fin corrections; maintain two distinct fish throughout. A steady breeze bends the leaf clusters and ripples the hanging branches, then lets them rebound. Broad reflections drift across the pond behind the fish, while the stone lantern and bridge remain still. End with both koi clearly visible near the center of the pond.
```

## First & Last Frames: bridge the states

Inspect both endpoints. Explain how position, pose, prop ownership, lighting, and camera evolve between them. If the endpoints require a cut or transformation, make that choice explicit rather than asking for physically impossible interpolation. Do not assume frame-slot syntax or exact timing controls.

Example: first image shows a closed greenhouse door, last image shows the door open with a gardener holding a tray.

```text
Begin in the supplied first-frame composition and arrive at the supplied last-frame composition. From behind the closed greenhouse door, the gardener pushes it open with one shoulder while supporting the seedling tray in both hands. The door swings outward toward the camera; the gardener steps through and stops at the position shown in the final image. The camera remains at the original viewpoint, and the greenhouse geometry and daylight stay consistent. Preserve the tray and seedling count during the movement. Hear the hinge creak and two footsteps. No dialogue or music. Finish with the open door and gardener matching the final reference.
```

## Multi-keyframes: states plus transitions

Use only the keyframes needed for essential visual anchors, up to the full model's documented limit. Put them in chronological order. Describe each state and the causal bridge to the next. Do not merely list still-image descriptions. If a storyboard/grid is one reference image, describe panel reading order and whether panels mean separate shots; it does not automatically become separately uploaded keyframes.

Example settings: full Kling 4.0, 12 seconds, three keyframe inputs. Beat timings below are intent, not guaranteed slot timestamps.

```text
Use the three keyframe images in their supplied order as the beginning, middle, and ending visual states. Preserve the courier's identity, red satchel, and the rainy station throughout.
Opening: the courier stands beside the closed ticket booth, holding the brass key shown in the first image.
Middle: they notice the locker opposite the booth, cross the platform, and insert that same key with their right hand. Track sideways with them at waist height, then move closer as the locker opens, reaching the second keyframe state.
Ending: they lift the folded blue scarf from inside, smile with recognition, and hold it against their chest, arriving at the third keyframe. Ease the camera to a still medium close-up for the last moment.
One continuous take. Rain, footsteps, the key turning, and the locker latch are audible. No dialogue or music.
```

## Omni: separate ownership of identity, action, camera, and style

Map roles before writing beats. If a motion reference includes unwanted costume, identity, setting, or audio, exclude those dimensions specifically. Do not repeat a long transcription of an already adequate motion reference.

```text
Use the character reference image for the dancer's face, braided hair, green jacket, and body proportions. Use the performance reference video only for the choreography and its rhythm, retaining the same turn, low step, and final raised-arm pose. Use the studio image for the room layout and warm sidelight. Show one dancer. Do not inherit the reference performer's appearance or background. Begin in a full-body view, track laterally to keep both feet visible through the low step, and settle into a centered full-body composition as the dancer holds the final pose. Preserve the jacket and braid through the turn. Hear the shoes contacting the wooden floor and a final exhale. No added music.
```

### White-model, depth, wireframe, and layout references

Assign geometry, relative depth, blocking, motion, camera, and timing to the structural reference. Assign surface appearance, lighting, costume, and identity to separate visual references. Explicitly replace proxy materials; retain only the intended structural features. A diagram is not automatically a frame-accurate control track.

```text
Use the white-model video for camera travel, the runner's path, obstacle spacing, and the timing of the vault. Replace its proxy runner with the character from the portrait reference and render the set as the rain-soaked neon alley from the environment image. Preserve the white-model video's camera height and left-to-right travel. The runner plants a hand on the barrier, clears it, lands, and keeps running before the camera settles at the alley exit. Keep the character's coat and bag consistent. Replace all gray proxy surfaces with the finished scene; no wireframes or depth-map shading appear in the output.
```

## Creative recreation: preserve selected structure, replace assets

Name inherited pacing, transitions, composition, and performance separately from replacement objects. Replacing a product may require new hand contact and material behavior; keep the function of the action without forcing incompatible geometry.

```text
Use the reference ad video for its three-shot pacing, camera directions, and transition timing. Replace its featured product with the amber glass bottle in the product image, preserving that bottle's silhouette, cap, and label. Adapt the hand grip to fit the new bottle. Follow the source's progression: opening tabletop reveal, close view of the hand lifting the product, then a centered final display. Use the cream backdrop from the background image. Keep the supplied label facing the camera in the final shot. Do not inherit the source brand, lettering, or soundtrack. Hear the bottle lift and settle onto the table with quiet studio ambience. No music.
```

## Physical action: cause before spectacle

Define the participants, axis, approach, contact, reaction, recovery, and endpoint. Use effects to reveal force. Keep rapid action readable through a stable camera relationship; a reaction beat may be brief without removing causality.

```text
Use the two character images for the armored courier and the masked pursuer, one of each. In a single lateral tracking shot, the courier runs left to right across the wet rooftop while the pursuer closes from behind. The courier plants the left foot, turns, and strikes the pursuer's raised staff with the metal bracer. Sparks appear only at the bracer-staff contact. The staff deflects outward; the pursuer staggers one step back while the courier recovers balance and resumes running to the right. The camera continues parallel to the rooftop without crossing to the opposite side. Hear fast footsteps, a sharp metal impact, and a sliding recovery step. No music. End with the courier reaching the stairwell and the pursuer still on the roof.
```

## Dialogue and stereo scene sound

Attach each voice to an identity; use exact dialogue and distinct turns. At ordinary conversational speed, roughly two to three words per second can help estimate English speech space, but pace, language, pauses, and emotion change the budget. Treat this as an editorial estimate, not a model limit.

For stereo intent, describe sound sources in screen or camera-relative space. Do not fabricate pan values or assume discrete stem export. Movement that changes a source's screen position should have consistent sound direction.

```text
The mechanic stands on the left and the pilot on the right beside the grounded aircraft. Bind the supplied voice reference only to the mechanic. Begin in a medium two-shot. The mechanic looks up, wipes their hands on a cloth, and says in calm British English, "Give me one more minute." The pilot waits for the line to finish, glances toward the runway, then answers in a brisk American accent, "That's all we've got." Keep each speaker's mouth movement aligned with their own words; the listening character remains silent. A service cart rolls from screen right to screen left behind them, its engine sound moving with it across the stereo field. Keep the voices clear above the distant wind. No subtitles or music. End on their exchanged look.
```

## Visible text, logos, and UI

Specify literal copy, location, appearance, visibility interval, and behavior under camera movement. For UI, define a few states and the action causing each change; avoid contradictory simultaneous screens. Distinguish scene text from captions. Inspect spelling in the actual render; use a finishing tool if exact commercial copy remains unreliable.

```text
Use the interface reference image for the screen layout, typography, and colors. Begin with the central button reading "START". A fingertip presses it once; the button depresses, a circular progress indicator fills clockwise, and the heading changes to "READY". Keep the surrounding icons and panel layout fixed. Hold the final screen long enough to read "READY" clearly. The camera makes a slow, slight push toward the display without rotating. A soft click accompanies the press and a short chime accompanies completion. No spoken dialogue, additional captions, or music.
```

## Targeted editing: change plus preservation

Identify the primary video, target, interval/event, and requested change. Supporting clips are references, not additional editing masters. Preserve accepted edits and unaffected action, identity, geometry, camera, lighting, timing, and audio to the extent relevant. A text request for preservation is not a guarantee of pixel-identical output.

```text
Edit the primary video. During the final close-up, change only the performer's expression from a broad smile to a small, relieved smile: soften the eyes and keep the mouth mostly closed. Preserve the existing opening, all earlier acting, the face and hairstyle, body movement, costume, camera movement, shot boundaries, background, lighting, and current soundtrack. Finish at the same framing and moment as the source.
```

## Continuation: future-use or verified available mode

Read the availability note before offering native extension. For an available continuation tool, inspect the source ending and carry pose, velocity, screen direction, prop ownership, camera movement, lighting, and sound into the added segment. Do not invent backward extension support.

```text
Continue directly from the source video's last frame. The cyclist is still moving rightward, hands on the handlebars, with the red bag secured over the rear wheel. Carry the existing camera tracking speed and evening light into the new footage. The cyclist rounds the visible bend, slows beside the lit cafe, places one foot on the ground, and turns toward the door. Keep the bicycle and bag unchanged. Continue the tire noise into the braking sound and evening street ambience. Do not replay the approach or restart from an earlier pose. End on the stopped bicycle beside the cafe.
```

If native extension is unavailable, present this as creative direction for a separately generated adjacent clip, with its own valid duration and an explicit edit/stitch step. Do not imply that a source-video upload can automatically be used as an extension on any mode.
