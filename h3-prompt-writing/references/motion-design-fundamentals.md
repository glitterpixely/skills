# Motion-Design Fundamentals for H3 Prompting

## Scope and evidence boundary

Use this reference whenever H3 is asked to create kinetic typography, a title sequence, a brand film, an abstract graphic system, a product transformation, an interface journey, or a character-and-type trailer. It supplies motion-design procedure; the governing H3 surface, mode, media grammar, duration, and literal-copy rules still come from `SKILL.md`, `base-en.txt`, `ref-en.txt`, and `runtime-surfaces.md`.

The principles below are distilled from first-party motion systems, professional animation documentation, and peer-reviewed kinetic-typography research. They are not proof that a generative model can execute exact curves, frames, masks, optics, or spelling. Translate them into observable states and priorities, then verify the render.

## Core mental model: motion communicates change

Motion should identify relationships, reveal change, direct attention, and provide a readable result—not merely keep the frame busy.[1][4][5]
Apple explicitly advises adding motion purposefully without letting it overshadow the experience.[1]
For H3, every motion event therefore needs a **communication job**:

- reveal or remove an element;
- connect a source state to a target state;
- direct the eye to the next focal point;
- express weight, force, emotion, or material;
- confirm an impact, lock, completion, or hierarchy change;
- bridge two scenes while preserving continuity.

If an action has no job, remove it or demote it to a short accent.

## The motion-design compiler

### 1. Lock the frame constitution

Before writing motion, define the rules of the still frame:

- render domain: flat vector, paper collage, ink wash, cel animation, painted 2.5D, tactile stop motion, glossy 3D, or another single primary medium;
- palette and contrast roles;
- shape grammar: rounded, angular, geometric, organic, brush-based, architectural;
- outline, fill, highlight, shadow, grain, and texture policy;
- spatial system: flat plane, layered 2.5D, deep 3D, grid, stage, or environmental world;
- camera constitution: fixed, restrained, or dynamic, with permitted moves;
- exact visible copy and forbidden marks.

Resolve competing style phrases into a hierarchy. A primary render domain controls form; secondary references may control only surface texture, palette, or transition language. Do not ask for mutually dominant flat, photoreal, painterly, glossy, and line-art treatments at the same time.

### 2. Build a state ledger

For every beat, write four observable states:

1. **before** — what exists, where it is, and whether it is moving;
2. **action** — what force or input begins the change;
3. **during** — visible intermediate geometry, path, overlap, or material behavior;
4. **after/settle** — the exact readable result and what no longer exists.

This prevents teleporting objects, duplicate source and target states, replacement cuts disguised as morphs, and unfinished transformations. When one object becomes another, track conservation explicitly:

```text
source object -> transition operator -> target object
carry forward: [color / silhouette fragment / texture / motion direction]
consumed: [source parts that must disappear]
end state: [only the target remains]
```

For performance or mechanically precise action, use pose-to-pose planning inside the ledger: establish the neutral state, anticipation extreme, action/contact extreme, recovery or overshoot, and final hold before asking for generated in-betweens.[20]

### 3. Assign motion hierarchy

When several elements move, they must form one coherent experience rather than compete for attention.[3][7] Assign each beat:

- **primary motion** — the single action that communicates the state change;
- **secondary motion** — a delayed or physically caused response, such as hair lag, syrup follow-through, dust from impact, or letters trailing a hand gesture;
- **accent motion** — one brief flourish at impact or settle;
- **persistent anchor** — an object, container, title, silhouette, or horizon that preserves orientation through the transition.

Use consistent motion for elements with the same meaning or function.[3][4] Reserve the largest, most expressive motion for important moments; Carbon recommends expressive motion as an occasional rhythmic break rather than the default for every event.[2]

### 4. Give every action a timing envelope

Do not write only “moves smoothly” or “moves dynamically.” Describe the velocity story:

- **anticipation** — a small opposite move, compression, draw-back, or pause that prepares the action.[16]
- **launch** — acceleration away from the starting pose;
- **travel** — the main path and peak speed;
- **impact or arrival** — collision, lock, reveal, or material switch;
- **settle** — deceleration, overshoot and return, follow-through, or complete stop; loose or secondary parts may continue after the leader stops.[18]
- **hold** — enough stability to recognize the resulting state.

Traditional animation techniques adapted to kinetic type include slow-in/slow-out, movement in arcs, anticipation, follow-through, secondary action, and volume-conserving squash and stretch.[11]
Strictly linear movement often feels mechanical; easing creates acceleration and deceleration that viewers read as weight and natural force.[4][6][9]
Use curved paths for expressive organic movement when a rigid straight translation is not intended.[19]
At impact or launch, squash and stretch should preserve apparent volume rather than inflate, deflate, or melt the object.[17]

Use these mappings as qualitative prompt language, not guaranteed Bézier curves:

- **rest to rest:** accelerates quickly, then decelerates into a clean settle;
- **entrance:** arrives quickly, slows near its final position, then holds;
- **exit:** accelerates away and leaves decisively;
- **continuous rotation/conveyor motion:** constant rate may be appropriate;
- **heavy object:** slower launch, longer deceleration, low rebound;
- **light object:** fast launch, short settle, slightly larger follow-through;
- **stepped animation:** discrete pose changes with intentionally held frames and no fluid in-betweens.

Duration should reflect the element’s size and travel distance: larger or farther changes generally need more time than smaller changes.[2][4][6] In H3, state this relationship and the intended impression; do not paste interface-specific millisecond tokens unless frame-accurate execution is being measured.

### 5. Choose one transition operator

Name the actual operation instead of saying “transition beautifully.”

- **continuous contour morph** — the source silhouette visibly deforms through intermediate shapes into the target; no duplicate target, cover mask, or replacement cut.[23]
- **shared transformation** — one persistent object or container changes size, position, orientation, or material while preserving identity.[21]
- **match cut** — source and target share a contour, axis, direction, color block, motion vector, or audio feature across a hard cut.[22]
- **hard material cut** — the geometry stays fixed while its appearance changes in one frame; no crossfade or intermediate material;
- **wipe** — a moving boundary conceals one state and reveals another, normally signaling a change of state, place, time, or subject.[24]
- **occlusion handoff** — a foreground object hides the exact moment of replacement;
- **fade/crossfade/fade-through** — opacity is the intended mechanism;
- **assemble/disassemble** — parts visibly separate, travel, and lock into a new whole;
- **split/merge** — one form becomes several or several become one, with every part accounted for.

Material notes that shared transformations and focal elements support continuity, while many unrelated transformations compete for attention.[7] Classify elements as **outgoing**, **incoming**, or **persistent**; use the persistent element as the bridge. If a replacement must be hidden, place it near peak velocity, inside occlusion, or at a deliberate hard cut—do not accidentally blend incompatible states.[7]

### 6. Choreograph attention and staging

Movement captures attention, and a large sweep tends to pull the eye toward its endpoint.[11] Sudden onset is therefore a scarce resource: use it for the intended focal change, not for background decoration.
Treat staging as the requirement that one idea be completely and unmistakably clear in each beat; hold or suppress competing motion until that idea reads.[15]

For each beat, specify:

- where the viewer should look first;
- the path that carries the eye;
- the endpoint that becomes readable;
- what stops or softens while that endpoint is read.

Sequence or stagger multiple entrances instead of introducing everything simultaneously.[3][4] Stagger in semantic order, not randomly. A useful hierarchy is anchor first, supporting elements next, primary information last; reverse it only when surprise is the explicit goal. Keep a shared axis, grid, container, motion vector, or silhouette through complex changes so the viewer remains oriented.

### 7. Design kinetic typography as type, not generic geometry

Kinetic typography adds film-like emotion, character, and attention direction to the communicative properties of text.[11]
Adobe likewise describes animated text as a way to grab attention, guide the viewer’s eye, and move a story forward.[10]
Typeface, size, weight, position, pacing, direction, rotation, contrast, and persistence can collectively convey tone.[11][12]

Use a three-level temporal hierarchy:

- **phrase level** — the whole line enters, travels, transforms, and settles;
- **word level** — one semantic word receives emphasis or changes relationship;
- **letter level** — brief stagger, tracking change, vibration, split, or reassembly.

Do not animate all three levels aggressively at once. One level leads; the others support.

Choose the legibility objective explicitly:

- **functional kinetic type:** the copy may distort during travel, but it must land in at least one protected, correctly spelled, readable state;
- **experimental temporal type:** letterforms may deliberately pass through a medial or asemic in-between state where they are perceived as forms rather than immediately read, but the prompt must define the recognizable source and target poles if semantic recovery matters;
- **navigable type:** the form stays stable while a camera or viewpoint change reveals different spatial readings;
- **transitory type:** the readable form exists only briefly before becoming an image, material, or abstract shape.

Temporal-typography research treats legibility as something that can fluctuate during transformation and distinguishes global movement of a word or phrase from local change inside individual letterforms.[14] In H3, decide whether the phrase, word, or letter is the active level and state when readability returns.

#### Semantic motion mapping

Use motion to reinforce the meaning and emotional energy already present in the copy; kinetic treatment can strengthen or temper meaning but should not be expected to reverse strong semantic content.[11]

- urgency or force: faster onset, larger scale/weight, stronger impact, restrained vibration;
- calm or elegance: slower pacing, smaller acceleration, stable baseline, generous hold;
- ascent or rising pitch: upward path;
- falling energy: downward drift, deceleration, reduced weight or scale;
- loudness/accent: temporary increase in size, weight, contrast, or persistence;
- intimacy: smaller spatial range, low amplitude, close grouping;
- authority: stable baseline, limited deformation, decisive settle.

#### Legibility contract

For every literal phrase:

1. quote the exact copy;
2. define its type family, case, weight, and color;
3. define entry and direction;
4. define the readable settled state;
5. protect it from occlusion during the hold;
6. define exit or transformation;
7. state whether it persists into the next beat.

Animate optical typography rather than merely stretching a bitmap. The kinetic-typography research notes that geometric scaling can create poor letter spacing compared with typographic scaling.[11] In prompt language: preserve recognizable letterforms, baseline, counters, and optical spacing; allow tracking to change briefly, then restore correct spacing before the hold.

Distinct speakers, characters, brands, or information roles should retain persistent typeface, position, weight, movement pattern, or tone cues so they can be recognized again.[11][12] Do not invent seals, microcopy, random glyphs, or background script. Inventory every visible string before drafting, especially for multilingual work.

#### Reading order, contrast, and multilingual shaping

Group copy at natural syntactic clause or phrase boundaries rather than cutting language into arbitrary visual fragments; coherent linguistic segmentation can improve readability.[25]
If sequence changes meaning, state the exact reading order and give every phrase an unambiguous temporal or spatial handoff.[26]
Do not derive a universal hold length from word count. Size the readable hold for linguistic complexity, language familiarity, delivery size, shot synchronization, background motion, and whether the audience is also listening; then inspect the actual render.[25]

During the readable hold:

- stop tracking changes, glyph assembly, deformation, blur, vibration, and exposure shifts unless continued instability is the message;
- preserve strong light-dark separation between copy and its background, and prevent moving edges or flashes from crossing counters.[27]
- declare z-order explicitly and keep essential glyphs unobscured; confine intentional occlusion to entry, exit, or a named wipe;
- preserve one meaningful reading path when several text blocks remain on screen.

For every non-Latin or multilingual string, name its language, script, base direction, and horizontal or vertical writing mode. Animate a valid shaped word or grapheme cluster rather than treating every Unicode code point as an independent Latin letter. Arabic-script text is right-to-left and its cursive joining makes separated-letter styling unsafe; preserve joining forms, ligatures, diacritics, and surrounding punctuation.[28] In Japanese vertical composition, characters run top-to-bottom and lines run right-to-left; preserve the requested vertical order and script-appropriate punctuation rather than rotating a horizontal line as one generic object.[29] Other scripts have different shaping and segmentation rules: consult the relevant layout standard and verify with a native reader.

### 8. Coordinate camera motion with graphic motion

Decide which coordinate system owns the beat:

- **fixed-camera graphic beat:** the frame behaves like a poster or stage; shapes and type create the motion;
- **camera-led beat:** the subject or typography is comparatively stable while camera movement creates parallax and scale change;
- **coupled beat:** one primary subject action causes one camera response and one secondary typography response;
- **bullet-time beat:** subject and graphics freeze while only the camera moves;
- **hard-cut montage:** each cut establishes a new composition rather than pretending one continuous camera path.

Do not let camera, subject, typography, particles, and background all peak simultaneously unless deliberate sensory overload is the communication job. Name motion type, direction, amplitude, speed, endpoint, and what remains fixed. Treat focal length, aperture, shutter angle, Kelvin values, and lens terminology as appearance cues unless the runtime exposes measurable controls.

### 9. Use shape and material to imply force

Squash and stretch should preserve apparent volume and occur around acceleration or impact, not as arbitrary gelatinous deformation.[11] Secondary action should result from the primary action: fabric trails a turn, droplets lag behind a moving word, dust expands from a landing, or a shadow snaps into place after the object settles.

For every material, define:

- rigidity or softness;
- mass and rebound;
- surface finish;
- deformation limit;
- edge behavior;
- highlight and shadow construction.

Choose one material model per object state. If a material changes, declare whether it morphs continuously, switches at a hard cut, is wiped on, or emerges after impact.

### 10. Choreograph sound as a hierarchy

Sound should clarify the same event hierarchy as the visuals. Material recommends that sound prominence match importance, that related events share sonic attributes, and that mixing or ducking direct attention toward the important sound.[8]

Build an event map:

```text
visual trigger -> physical or graphic event -> sound onset -> sound character -> music response -> silence/decay
```

Use:

- transient clicks, snaps, clacks, pops, impacts, and whooshes for discrete changes;
- sustained or rising sounds for continuous morphs, draws, charges, and expansions;
- related timbre or envelope for related state changes;
- small variations for repeated drips, taps, or type-on events rather than an identical sample every time;
- brief music ducking or removal around the hero impact;
- silence as an intentional contrast or final hold.

Apple Motion can map audio amplitude or transients to visual parameters, illustrating two different synchronization logics: continuous pulsing versus event-triggered response.[13] In H3 prompting, name the visible event and its sound directly; “sync everything to the beat” is too vague. Do not sonify every minor movement, and do not let decorative music conceal the primary causal effects.

Pair salient visual accents with salient auditory accents when congruency is the goal: name the exact hit and visible state change in the same beat, such as a panel locking on the snare or a logo settling on the final chord.[31] Also align broader temporal contours, not just isolated hits: a short-short-pause-long visual pattern should use the same short-short-pause-long sound pattern when the two are meant to feel causally related.[32] Match overall music tempo and visual speed deliberately; a mismatch can be a purposeful source of complexity rather than an automatic error.[31]

Treat silence as timed auditory negative space. State which layers drop out, what residual ambience remains, and which event restores sound; silence can create focus just as visual negative space does.[30]

### 11. Construct a readable 15-second arc

Do not impose a universal cut count. Dense motion design is valid when every phase has one dominant job and each required state becomes recognizable. A robust arc is:

1. **anchor** — establish medium, composition, identity, or graphic system;
2. **activation** — one force begins the motion language;
3. **development** — causal transformations or escalating variations;
4. **contrast** — a stop, hard cut, palette/material switch, or scale reversal;
5. **hero transformation** — the largest state change or identity payoff;
6. **resolution** — title, product, character, or lockup settles;
7. **hold** — clean stillness or one bounded living detail.

A hold is not wasted time. It is the state that proves the transformation completed and lets the viewer read the result. Use either:

- **clean hold:** every element and camera remain still;
- **living hold:** layout remains fixed while one low-priority periodic detail continues;
- **camera-only hold:** subject and graphics freeze while camera movement reveals depth.

### 12. Replace vague adjectives with observable instructions

| Weak wording | Motion-design wording for H3 |
| --- | --- |
| “dynamic typography” | The exact phrase enters from the left as one group, accelerates across frame, overshoots slightly, restores correct spacing, and holds fully readable. |
| “smooth transition” | The circular product silhouette continuously deforms through visible intermediate contours into the first letter; the source object is gone when the word settles. |
| “punchy” | A short anticipation compression precedes a fast launch, one-frame impact accent, low rebound, and complete stop. |
| “cinematic camera” | The camera arcs clockwise with large amplitude at fast speed, then decelerates into a frontal hero frame while the subject remains centered. |
| “sync to the beat” | The launch begins on the kick, the material switch occurs on the snare, letters settle on the next downbeat, and the music ducks under the impact. |
| “premium motion graphics” | Restrained palette, one primary action per beat, controlled easing, persistent alignment, precise optical spacing, and a clean final hold. |
| “letters explode” | Letters separate radially from the word’s center, preserve recognizable glyphs, decelerate at bounded positions, then reverse along the same paths and reassemble correctly. |

## H3 motion-design review

Before linting the provider grammar, check:

- **purpose:** every motion has a communication job;
- **state:** each beat has before, during, after, and settle states;
- **hierarchy:** one primary motion leads; secondary and accent motions are causally subordinate;
- **timing:** anticipation, travel, impact, settle, and hold are observable where appropriate;
- **continuity:** a persistent anchor, shared path, container, axis, or motif bridges complex changes;
- **transition:** morph, cut, wipe, occlusion, assemble, split, or fade is named and substitutes are excluded when necessary;
- **typography:** every exact string has one readable state, protected counters, baseline, and spacing;
- **reading system:** phrase segmentation, semantic order, contrast, z-order, script direction, grapheme integrity, and vertical-text rules are explicit;
- **camera:** camera and graphic motion have distinct roles and do not compete unintentionally;
- **material:** deformation and follow-through match weight and surface rules;
- **audio:** primary events have synchronized effects, related sounds form a family, and silence/ducking is intentional;
- **audio contour:** salient hits and broader interval patterns have an explicit visual relationship rather than generic beat-sync wording;
- **endpoint:** every required payoff is complete before the retained endpoint;
- **capability boundary:** frame-exact, per-pixel, optical, and spelling claims are labeled for measurement or deterministic post-production when essential.

## Sources

[1] https://developer.apple.com/design/human-interface-guidelines/motion — Apple Human Interface Guidelines: Motion
[2] https://v10.carbondesignsystem.com/guidelines/motion/overview — IBM Carbon: Motion Overview
[3] https://v10.carbondesignsystem.com/guidelines/motion/choreography — IBM Carbon: Motion Choreography
[4] https://fluent2.microsoft.design/motion — Microsoft Fluent 2: Motion
[5] https://m2.material.io/design/motion/understanding-motion.html — Material Design: Understanding Motion
[6] https://m2.material.io/design/motion/speed.html — Material Design: Motion Speed
[7] https://m2.material.io/design/motion/choreography.html — Material Design: Motion Choreography
[8] https://m2.material.io/design/sound/sound-choreography.html — Material Design: Sound Choreography
[9] https://www.adobe.com/uk/creativecloud/animation/discover/easing.html — Adobe: Animation Easing
[10] https://www.adobe.com/learn/after-effects/web/creating-animating-text — Adobe: Animate Text in After Effects
[11] http://johnnylee.net/academic/KT_Engine_UIST2002.pdf — The Kinetic Typography Engine (UIST 2002)
[12] https://www.cs.cmu.edu/~joonhwan/documents/p41-lee.pdf — Using Kinetic Typography to Convey Emotion (DIS 2006)
[13] https://support.apple.com/guide/motion/audio-parameter-behavior-motn1872e265/mac — Apple Motion: Audio Parameter Behavior
[14] https://brooke-francesi-qcqu.squarespace.com/s/TemporalType_BrookeFrancesi_MFA-Thesis2015.pdf — Temporal Typography (CCA MFA Thesis, 2015)
[15] https://www.evl.uic.edu/ralph/508S99/staging.html — The Principles of Animation: Staging
[16] https://www.evl.uic.edu/ralph/508S99/anticipa.html — The Principles of Animation: Anticipation
[17] https://www.evl.uic.edu/ralph/508S99/squash.html — The Principles of Animation: Squash and Stretch
[18] https://www.evl.uic.edu/ralph/508S99/follow.html — The Principles of Animation: Follow Through and Overlapping Action
[19] https://www.evl.uic.edu/ralph/508S99/arcs.html — The Principles of Animation: Arcs
[20] https://www.evl.uic.edu/ralph/508S99/straight.html — The Principles of Animation: Straight Ahead and Pose-to-Pose Action
[21] https://m3.material.io/blog/motion-research-container-transform — Choosing the Right Transitions
[22] https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/match-cut.html — Match cut: What is a match cut in film and how to create one
[23] https://www.adobe.com/creativecloud/animation/discover/morphing-in-animation.html — What is Morphing in Animation? Morphing vs Tweening
[24] https://www.adobe.com/creativecloud/video/post-production/transitions/wipe.html — Wipe transition: What is a wipe transition and how to use it
[25] https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles — BBC Subtitle Guidelines
[26] https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html — W3C Meaningful Sequence
[27] https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum — W3C Contrast Minimum
[28] https://www.w3.org/International/alreq — W3C Arabic and Persian Layout Requirements
[29] https://www.w3.org/TR/jlreq — W3C Japanese Text Layout Requirements
[30] https://m2.material.io/design/sound/applying-sound-to-ui.html — Material Design: Applying Sound
[31] https://doi.org/10.1109/ICSMC.2000.886019 — Effects of Audio-Visual Accent Synchronization
[32] https://doi.org/10.3389/fpsyg.2012.00619 — Temporal Structure and Audio-Visual Correspondence
