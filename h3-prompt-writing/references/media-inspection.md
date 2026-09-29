# H3 Media Inspection Workflow

Use this workflow before assigning reference roles or describing any supplied media. The goal is a grounded asset map, not an impressionistic summary.

## Contents

- [Inspection Standard](#inspection-standard)
- [Images](#images)
- [Video](#video)
- [Audio](#audio)
- [Cross-Asset Reconciliation](#cross-asset-reconciliation)
- [Coverage Gate](#coverage-gate)

## Inspection Standard

For every asset, record:

- filename or user-visible handle;
- media type and technical properties;
- source duration and runtime-processed duration when a graph resamples, pads, aligns, or trims it;
- directly observed content;
- timeline or spatial structure;
- readable text and exact punctuation/case;
- audible speech, lyrics, music, ambience, and sound effects;
- proposed H3 role;
- runtime route: model-fed reference/copy, latent initialization, generated output, or post-generation mux only;
- what must remain unchanged;
- what may change;
- uncertainties and confidence.

Never infer an identity, brand, exact wording, off-screen event, or audio source that cannot be observed. Distinguish observation from user-provided intent.

## Images

1. Open the original-resolution image, not only a thumbnail.
2. Inspect the whole frame and zoom into each information-bearing region.
3. Record:
   - subject count, identity cues, pose, gaze, expression, wardrobe, and held objects;
   - environment, foreground/midground/background, geometry, and spatial relationships;
   - framing, lens cues, camera angle, depth of field, and aspect ratio;
   - light direction, contrast, time of day, palette, texture, and medium;
   - product geometry, material, logo placement, and small design details;
   - literal visible text with capitalization, punctuation, line breaks, and location;
   - elements that appear cropped, occluded, reflected, or ambiguous.
4. Run OCR when text exists, then verify OCR manually against the pixels.
5. Decide its semantic role before choosing syntax. In structured Ref2VA, a concrete first/key/last/edited frame is `<Picture N>` and reusable visible content is `<Subject N>`; one image can supply both roles. In native ComfyUI, use only the picture endpoint or connected-media tags allowed by the selected raw mode and never invent a `<Subject N>` media handle.

## Video

### Technical Pass

Probe duration, frame rate, resolution, aspect ratio, codec, orientation, and audio-stream presence. Do not assume a video is silent from its caption or that embedded audio should be reused.

### Visual Pass

Inspect the video in playback order using all of these layers:

1. first frame and last frame;
2. evenly spaced coverage frames across the full duration;
3. every detected hard cut, dissolve, wipe, flash, blackout, or large visual discontinuity;
4. additional frames before, during, and after each action, expression, camera, lighting, object, UI, or text change;
5. original-resolution crops for small text, products, faces, hands, and interaction points;
6. playback at normal speed for rhythm, motion continuity, and cause/effect;
7. slower or frame-by-frame playback where timing, lip movement, sleight of hand, transformation, or exact edit preservation matters.

For high-risk precise edits, inspect every frame in the affected interval or use an equivalent dense frame sequence. A sparse contact sheet is not sufficient to prove unchanged details across the edit.

Record a shot ledger:

| Time | Shot/state | Subjects and action | Camera/edit | Text/UI | Lighting/VFX | Audible event |
| --- | --- | --- | --- | --- | --- | --- |

For structured Ref2VA, determine whether the video supplies:

- a direct edit source (`<Video N>` and `video editing`);
- a continuation source (`<Video N>` and `video continuation`);
- whole-video rhythm, cut, or camera structure (`<Video N>` or a subject role, normally `reference generation`);
- a reusable character/action/effect (`<Subject N>`);
- an audio signal only when explicitly copied or referenced (`<Audio N>`).

For native-ComfyUI Ref2VA, map only the actual connected `<Video N>` and enabled `<Audio N>` ordinals and describe reusable people/objects naturally rather than creating `<Subject N>` handles.

### Text And UI Pass

Transcribe every visible word that affects the requested output. For animated UI, record the complete state sequence, not just the first and last screens. Preserve exact copy in double quotation marks in the prompt. If OCR and visual inspection disagree, use the pixels and mark unresolved characters as uncertain rather than guessing.

## Audio

Listen through the complete asset at least once, then inspect event boundaries and difficult spans. Record:

- duration, channels, sample rate, clipping/noise, and leading/trailing silence;
- each vocal source, language, exact words, delivery, emotion, pace, pitch, and timbre;
- music instrumentation, tempo/rhythm, dynamics, transitions, and whether it is diegetic;
- ambience, Foley, impacts, breaths, laughs, crowd sounds, and other nonverbal events;
- event timestamps and synchronization cues;
- unintelligible spans as `[unclear]` rather than invented words.

Choose the audio relationship deliberately:

- `fully_copy`: complete signal becomes the complete target track;
- `partially_copy`: only a segment or layers are copied, or other layers change;
- `reference`: signal is not copied; timbre, delivery, beat, words, or texture guides generation;
- `weak_reference`: only broad category or atmosphere remains.

When only voice timbre is referenced, do not carry source dialogue into the target. When source words are copied or explicitly reperformed in Ref2VA, follow the scoped transcription and punctuation rule in `ref-en.txt`.

For a local graph, also record crop start, leading/trailing padding, resampled rate, latent window, gain/mix/ducking changes, and the final mux source. Only model-fed signals receive `<Audio N>`. Re-evaluate `fully_copy`, `partially_copy`, `reference`, or `weak_reference` after preprocessing and mixing, then confirm that every copied vocal or musical event still lands at the prompt's render-clock timestamp.

## Cross-Asset Reconciliation

Compare assets before drafting:

- identify the same subject across files and specify which asset controls identity, wardrobe, pose, motion, voice, environment, or style;
- call out conflicts rather than blending them silently;
- use one role per asset when that is sufficient, but allow multiple explicit roles when the user needs them;
- rank strict identity/product/frame anchors above loose mood references;
- use the smallest upload stack that supplies all required information;
- resolve raw ComfyUI media ordinals from actual graph wiring or an emitted media map, not from filename order;
- map every requested target detail to at least one text instruction or inspected source.

## Coverage Gate

Do not begin the prompt until all answers are yes:

- [ ] Every supplied asset opened successfully.
- [ ] Every image was viewed at original resolution.
- [ ] Every video was reviewed across its full duration and at every shot/state change.
- [ ] Every affected precise-edit interval received dense or frame-by-frame review.
- [ ] Every audio asset and relevant embedded track was heard or measured.
- [ ] Every relevant visible word and spoken line was transcribed and verified.
- [ ] Every asset has an explicit role or is intentionally excluded with a reason.
- [ ] Preservation and change targets are unambiguous.
- [ ] Uncertainties are disclosed outside the prompt.

If any required item remains unchecked, pause and obtain the missing access or user decision.
