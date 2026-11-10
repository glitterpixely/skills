# Desk Continuity, Vignettes, Prosody, & Coverage

Clip-desk craft heuristics for observational and curiosity vignettes, literal multi-shot continuity, conversational dialogue prosody, diegetic phone-camera comedy, and reference-plate / single-clip `[Cut to]` coverage. Companion modules cover [kinetic action, combat VFX, and four-mode timing](desk-prompt-patterns.md) and [ByteDance Seed training architecture and evidence boundaries](research-mechanics.md).

These heuristics do **not** expand first-party capabilities, limits, or API fields in [source-boundaries.md](source-boundaries.md), [prompt-architecture.md](prompt-architecture.md), or [task-contracts.md](task-contracts.md).

## Contents

- [Untimed, rule-led worldbuilding vignettes](#untimed-rule-led-worldbuilding-vignettes)
- [Curiosity-driven character vignettes](#curiosity-driven-character-vignettes)
- [Literal multi-shot control](#literal-multi-shot-control)
- [Split references by job](#split-references-by-job)
- [Multi-shot continuity craft & conversational prosody](#multi-shot-continuity-craft)
- [Diegetic phone-camera comedy](#diegetic-phone-camera-comedy)
- [Result-backed notes: two-character door-to-door comedy](#result-backed-notes-two-character-door-to-door-comedy)
- [Reference-plate preparation and single-clip coverage](#reference-plate-preparation-and-single-clip-coverage)

## Untimed, rule-led worldbuilding vignettes

Use when the user wants everyday worldbuilding, an observational montage, or generative moment-selection rules rather than a scripted plot. Distilled from a user-supplied written example (video not inspected; its 19-cut count is example-specific, not a default or limit).

1. **Choose the organizing principle:** routine, a place's working life, social presence, or ordinary encounters. Lock any user-requested cut count without inventing timestamps, a numbered shot list, or a dramatic crisis.
2. **Bind continuity, then scope invention:** map the uploaded reference to identity, design, and medium. Preserve established fictional role and temperament; do not infer real-person demographics from appearance or assert unknown canon as fact. For non-human designs (yokai, creatures, aliens), name the inhabitant type explicitly so generic words like "people" do not pull the world toward ordinary human street life.
3. **Direct selection rather than plot:** ask for varied small moments showing maintenance, exchange, travel, etiquette, labor, or shared space so each cut adds a fresh social or environmental detail.
4. **Preserve tone without moral sanitization:** threatening characters alter bystanders' spacing and eye contact; gentle characters show warmth through small habits.
5. **Specify one coherent observer:** e.g., detached third-person 28–40mm shoulder-mounted documentary framing with subtle breathing drift and reactive pans, excluding POV/vlog/drone shots.
6. **Close sound and text:** diegetic location foley only; exclude intelligible background speech, narration, BGM, subtitles, and title cards unless requested.
7. **Deliver compact connected prose:** `premise & cut structure -> identity/style locks -> permitted world invention -> moment-selection rules -> tonal boundaries -> camera -> sound/exclusions`.

## Curiosity-driven character vignettes

Use when the user wants a short character study built around one unanswered visual question, cause-and-effect discovery, and a payoff rather than routine worldbuilding (video not inspected; 10–15 cuts in source study was example-specific).

1. **Open on a visual question** that a viewer can follow without dialogue.
2. **Reveal character through physical behavior** (instincts, habits, abilities, limitations) rather than exposition.
3. **Make early details pay off** in a closing reveal, reversal, or emotional beat.
4. **Vary scale and framing** across cuts while keeping third-person continuity and diegetic sound.
5. **Keep distinct from routine worldbuilding** unless a hybrid is explicitly requested.

## Literal multi-shot control

Use when continuity, prop state, and readable transitions matter more than adjective density (distilled from public Seedance 2.5 prompt studies; videos not inspected):

1. **Describe the physical transition, not just the new view:** name the turn, crossing, landing, or handoff before cutting to a rear or reverse angle.
2. **Let action quantity control pace:** avoid stuffing multi-minute plots into short beats or copying decimal timestamps.
3. **Override likely still-image misreads upfront:** state whether a pictured item is alive, already worn, holstered, or rigid.
4. **Keep a prop and target ledger:** track counts, owners, irreversible damage, and where released objects rest.
5. **Repeat a route only to change it** (an escape lane closes or redirects visibly).
6. **Show speed through overlap:** let earlier debris keep falling while a fast subject re-enters frame, without unrequested clones or teleports.
7. **Order strike before body response** (contact -> fold/slide/recoil) while keeping attached gear attached.
8. **End in a legible carried state** rather than defaulting to a static victory pose.

## Split references by job

Give each active asset one primary job — typically one identity/appearance lock (a multi-view turnaround sheet when available) and one world/environment lock — stating both inherited and excluded attributes on every `@Image` / `@Video` / `@Audio` line.

## Multi-shot continuity craft

Distilled from studied multi-shot prompts (2026-10-30) and inspected renders (`Untitled_(2).mp4`, `Untitled_(3).mp4` on 2026-11-01; 57.4s 2-part German period-drama dinner render on 2026-11-02). Apply across `Shot N` prompts with recurring characters, props, or speech:

- **Restate prop and hand state in every shot:** declare single-instance ownership once ("her only gun, always in her right hand; hip holster stays empty") and restate it even when unchanged ("still hangs on its hook", "arrives empty-handed, arms free").
- **Tag each character on every mention** with `<Name>, <2-word visual trait>` ("Kira, lilac buns"; `Kai，黑色机械臂`), especially when re-entering after a cut or multi-character occlusion.
- **Isolate speakers and script active listening:** write `<Name> alone speaks` and give listeners specific closed-mouth beats (`eyes stay on the table through lines 1–3, lifting from under knitted brows only after line 4`).
- **Keep air between bodies and anchor the 180-degree stage map:** maintain depth separation (`a clear gap between them`) and pair screen sides with fixed landmarks (`the bag shelf at screen left`).
- **Cut on active motion:** end shots with `Cut as <observable action>` (`切于<动作>`) and end the clip without unrequested fade-outs.
- **Lock asymmetry and anti-slide footwork:** state exact left/right placement for prosthetics, tattoos, earrings, and holsters; for grounded movement, state `feet plant, push, leap, or roll cleanly without floor-skating`.
- **Use shot-indexed damage ledgers (`Continuity:` footer)** for mid-clip breaks (`necklace remains a broken strand after Shot 11`), **bound partial orbits by degrees** (`60-degree partial orbit from three-quarter to profile without turning her chair`), **start cross-cut solo rooms with `<Name> alone`**, and **explicitly close any split-screen divider** on the next cut.
- **Separate 3D/live-action optical grammar, lineless airbrushed digital painting, and 2D cel layer grammar:**
  - *3D CG / live-action:* optical lens/FOV terms (`47° deep-focus`, `29° shallow DOF`) are valid.
  - *2D hand-drawn / cel / gouache:* never use `bokeh`, `shallow depth of field`, or `85mm f/1.4` (`STYLE_2D_LENS_CONFLICT`); use `multiplane background scroll`, `cel-shaded over painted gouache`, `animated on twos with bursts on ones`.
  - *Lineless airbrushed semi-realistic digital painting:* never label `2D anime` or `cel-shaded` (`AIRBRUSH_CEL_CONFLICT`, which snapped Shot 3+ into hard black comic outlines in a 2026-11-01 30s render); re-state `lineless airbrushed semi-realistic digital painting matching @Image 1` across cuts and keep magic/snow translucent rather than a full-screen whiteout wipe.
- **Keep dialogue and facial acting in the Conversational Goldilocks Zone:**
  1. *Avoid unintended prosody flatteners (`PROSODY_FLATTENER_RISK`):* `flat tone`, `monotone delivery`, and `keep expressions subtle, cool, and deadpan` froze faces into mannequin stares and robotic TTS in `Untitled_(2).mp4` (valid only for intentional kuudere/gothic deadpan personas).
  2. *Avoid cartoon over-acting & face-occlusion triggers (`CARTOON_OVERACTING_RISK`):* `inhales excitedly`, `offended gasp`, `sing-song lilt`, `eyes snapping wide into circles`, and `puffs her cheeks` synthesized loud `"HAAAH!"` gasps and bug-eyed/balloon-cheek distortion in `Untitled_(3).mp4`, while a hat pom-pom dangling in front of the face glued to the nose (`anchor dangling ornaments off to the side leaving the face clear`).
  3. *Pair conversational vocal tone + anatomical upper-face cues + subtext anchor gestures:* use grounded phrasing (`smooth teasing conversational voice`, `dryly amused tone`), natural micro-expressions (`slow arch of one eyebrow`, `blinking twice`), `normal human eyes; no glowing eyes` on realistic humans, and subtext gestures (`turns one hand palm up, as if to say "obviously, who else?"`).
  4. *Isolate emotion to brow and eyes + chew/swallow gates:* write `All facial expression lives in the brow and the eyes; the mouth is left natural, at most slightly parted` so emotional adjectives do not fight `p/b/m` lip closure; enforce `finishes chewing and swallows before speaking`.
  5. *Break turns into `2–6 word` period-separated clauses with mundane physiological micro-actions between them:* inserting a quick nasal sniffle, throat clear into a fist, swallow, or spoon placement between short period-terminated sentences (verified in the 57.4s 1080p German dinner render) resets the TTS read-through waveform and gives each clause natural downward pitch cadence.
  6. *Keep each sentence inside one on-camera shot (`SPLIT_DIALOGUE_ACROSS_CUT`)* and chain `6–10` subtle reaction micro-actions using explicit order gates (`in this exact order, each step its own beat: first..., then..., only after...`).
  7. *Calibrate clip dialogue budgets & warn rather than auto-splitting 30s takes:* keep general/action/comedy clips `<= 24 words` (`< 2.0 words/sec`). Dedicated 25–30s timed conversations hold `8–10` short clauses (`<= 38–43 words`, `< 1.8 words/sec`; BytePlus's own 9-shot 30s storyboard carries 43 words). Above `~40 words` in 30s (or `>= 2.0 words/sec`), warn of TTS prosody crowding (`CLIP_DIALOGUE_OVERLOAD` / `DIALOGUE_DENSITY`) and let the user choose between tightening clauses, keeping one 30s take when per-shot pace stays `< 1.8 words/sec`, using Dreamina 30–180s Long Video, or splitting across two generations around a silent reaction beat.
- **Keep `[Strictly exclude]` / `Avoid:` compact (`<= 80 words`, 3–5 hard rules; `BLOATED_EXCLUSION_LIST`):** Seedance's decoder-only LLM text encoder feeds spatial MMDiT multi-modality self-attention in one token stream, so 200-word lists of banned garments/props inject those exact nouns into spatial attention. Move wardrobe/prop persistence into affirmative state locks.

## Diegetic phone-camera comedy

Distilled from an 8-shot 30s handheld apartment comedy prompt (2026-10-30; video not inspected). Use whenever a character holds the camera:

- **Name holder and hand in every shot** ("the camera, still in Yuki's right hand") so body shake and screen side stay anchored.
- **Make the phone object cause every transition** (a snatch triggers a whip pan; a drop cuts on floor impact; the next shot opens face-up looking at the ceiling).
- **Declare one global energy rule** in the style header ("handheld, restless, bobbing with whoever holds it") to permit motivated multi-move shots.
- **Mark `Continuous` vs. `Later`** in scene headers, repeat temperament tags (`flat deadpan face` vs. `loud and easily flustered`), track temporary gag states (`hair over her face` -> `hair neat again`), and **end on physical lens contact** (fingertip or prop covering the lens to black).

## Result-backed notes: two-character door-to-door comedy

Inspected on a 30.08s render (`480x854`, 24 fps, sampled at 2 fps; audio not assessed):
- **Held:** per-side binding from one group image (`the figure on the left/right of @Image 1`) across all 8 untimed `Shot N` cuts (`3.3s`–`27.0s`), cut-on-action broom/door transitions, hands-only doorway adults, hat pop-off state, and chocolate-bar lens-contact blackout.
- **Repairs for observed misses (hypotheses until re-rendered):** replace negative `"wrappers carry no writing"` with an affirmative plain-wrapper design lock; keep the owner's sleeve/hand visible at the frame edge during close prop inserts so bucket identity does not drift; give sub-second micro-gags their own dedicated beat/shot; and keep one distinctive limb/hat tip visible when characters dive into leaf piles or cover.

## Reference-plate preparation and single-clip coverage

Distilled from an inspected 3-clip multi-shot workflow and 17 prepared reference plates (keep upstream image-editor names out of the Seedance prompt body):

- **Solid-white oval (`#FFFFFF`) face masking on wide staging & full-body turnaround panels:** mask small, expression-locked, or face-filter-sensitive faces on wide/full-body panels while leaving the high-res macro face panel unmasked. Pair with `Ignore the blank white face circles on the staging/full-body views; use the face close-up panel for facial features` in reference roles and `no white, blue, or green placeholder shapes or markers rendered` in exclusions.
- **3-in-1 16:9 composite character sheets:** pack full-body rear, full-body front, and macro face portrait onto one `@Image` plate to save asset slots while locking rear hair, cape, and armor geometry across OTS cuts.
- **Upstream 5–10% `#FFFFFF` silhouette paint-outs & untextured 3D graybox angle locks:** prep clean entry plates and multi-angle architectural layouts before keyframe generation.
- **Single-clip `[Cut to]` coverage clusters (`2–5 cuts` inside one `6–15s` generation)** keep weather, mud, firelight, and vocal strain unified across master-to-insert or wide-to-OTS reverse coverage:

```text
[Visual Style & Continuity]
<Shared film medium, palette, lighting, and atmosphere lock across all cuts; keep weapon geometry and armor plates rigid and continuous throughout.>

[Scene Setup & Reference Binding]
@Image 1 defines the opening staging, foreground elements, and lighting layout.
@Image 2 defines <Character A>'s facial features (from the unmasked close-up panel; ignore blank white face circles on full-body views) and outfit; do not use @Image 2's studio backdrop.
@Image 3 defines <Character B>'s appearance and fixed prop; normal human eyes; no glowing eyes.

Shot 1:
<Framing + camera path>. <Character A, 2-word trait>, <preparation -> physical contact/action -> spoken line in {}>. <Environmental response>. Cut as <active motion>.

[Cut to]

Shot 2:
<OTS reverse or macro insert>. <Connected continuation or active listening reaction from Shot 1>.

[Cut to]

Shot N:
<Payoff framing and observable end state>.

[Audio & Exclusions]
The audio contains only spoken lines, physical contact foley, and room/weather ambience; no background music. No subtitles. No white, blue, or green placeholder shapes or markers rendered.
```
