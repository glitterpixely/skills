# Optimizer Runtime

This file is the canonical owner for material inspection and mapping, ambiguity handling, long-text selection notes, permitted post-prompt notes, delivery, and evidence-grounded result repair. Capability and parameter facts remain owned by [source-boundaries.md](source-boundaries.md); prompt construction by [prompt-architecture.md](prompt-architecture.md); operation templates by [task-contracts.md](task-contracts.md).

## Contents

- [Non-negotiable behavior](#non-negotiable-behavior)
- [Input states](#input-states)
- [Story compilation](#story-compilation)
- [Material inspection and mapping](#material-inspection-and-mapping)
- [Mapping confidence](#mapping-confidence)
- [Output contract](#output-contract)
- [Result diagnosis and repair](#result-diagnosis-and-repair)
- [Capability disclosures](#capability-disclosures)
- [Final audit](#final-audit)
- [Runtime compatibility](#runtime-compatibility)

This file preserves procedural behavior from the provider's linked `sd25-pe` optimizer that is not expressed fully in the prose guides.

## Non-negotiable behavior

1. Preserve intent: identities, counts, props, scenes, causality, edit target, direction, and outcome.
2. Select and apply the template for the actual task instead of merely paraphrasing the input.
3. Give every active material an explicit role and every known inactive material an explicit unused declaration.
4. Respect user mappings before text inference, material appearance, metadata, or upload order.
5. Ask only one consolidated question when ambiguity can change the core result.
6. Keep analysis, evaluation labels, run metadata, API keys, endpoints, and reasons for rewriting outside the submit-ready prompt.
7. Keep configurable parameters outside the creative prompt while preserving user-authored event ranges.
8. Do not add generic quality, stability, logo, watermark, duplicate-subject, or negative boilerplate. `No subtitles` is task-relevant—not generic—whenever speech/dialogue is present and the user did not request visible subtitles.
9. Return one best version unless comparison is requested.
10. Keep story facts separate from material observations.
11. Match subject cardinality. One single-person image does not define two simultaneous characters.
12. Retain user-supplied names and neutral labels. Do not infer demographics, identity, relationship, profession, status, or personality from appearance or metadata.

The optimizer compiles text; it does not invoke a generation API by itself. If generation is requested, produce the prompt first, then use a separate authorized generation workflow.

## Input states

### Text only

Extract the subject, action/event, scene, visual treatment, camera, and audio. Do not invent reference numbers or pressure the user to add materials.

### A required reference is missing

Continue with all confirmed text and valid assets. Remove the nonexistent handle from the prompt rather than pretending it was inspected. Preserve the role it was meant to support, but omit appearance, voice, motion, or scene facts available only from that missing item.

After the prompt, add at most one line:

```text
Supplementary Suggestion: <missing handle> was not provided; supply it to bind <role> more precisely.
```

Request access before proceeding only when the item is the sole identity anchor, sole editing master, or sole extension source.

### Materials readable

Inventory and inspect them. Use two passes for a large set:

1. classify every item lightly by subject, prop, scene, motion, camera, pace, audio, or style;
2. inspect deeply only items that fit the story, conflict, act as anchors, or become active in the current scene.

### Materials inaccessible

Do not claim understanding. Use text and explicit labels, list unreadable non-core material as inactive, and request access only when core execution depends on it.

### Paths or Asset IDs

- If JSON or long text contains Asset IDs, assign `@Image N`, `@Video N`, and `@Audio N` by each media type's first appearance; replace raw IDs in the final prompt.
- If only local paths are available, assign stable aliases by media type and provided order. Do not expose local filesystem paths inside the creative prompt or infer content from a filename. Append one `Material Mapping Note:` recording the path-to-alias/upload order that the uploader must preserve.

## Story compilation

For novels and long-form text:

- use a thematic montage for an explicitly requested trailer, overview, or ensemble piece;
- preserve a continuous causal event for one-scene requests;
- when no range is chosen, select one causally complete event that fits and disclose the selection briefly outside the prompt;
- ask once when several mutually exclusive main threads are equally important.

Compress repetition and non-filmable explanation after protecting relationships, dialogue, triggers, and the ending state.

When the agent selects a range or event from longer material, use the legal one-line form `Selection Note: selected <event/range> because it is one causally complete unit that fits the requested clip.` Do not hide a story-changing selection inside the prompt. If several mutually exclusive core threads remain equally important, ask one consolidated question and stop instead of selecting silently.

Build these internal ledgers:

- **Required entities**: every character/group, key prop, product, and scene.
- **Dialogue**: speaker, mouth state, exact words, audio role, language, delivery, and on/off-screen state per stage.
- **Ownership**: who holds, transfers, releases, or receives each singular prop.
- **Continuity**: identity, clothing, structure, layout, axis, camera direction, lighting, and audio state.

Preserve identifiers. `Shot 45` is a shot number, not a 45-degree angle. Do not reinterpret material, chapter, step, or shot numbers as photographic parameters.

Do not invent lines around a quoted fragment. Do not invent dialogue from an intention such as “assert authority.” Express the intention with performance unless exact words are supplied.

If the user explicitly requires a character to speak with a bound audio reference but supplies no dialogue text, or the audio cannot be transcribed reliably, keep that character vocalizing in the correct stage and say that the spoken content comes from the bound reference audio. Do not fabricate a transcript or turn the stage into silence. If written dialogue exists, the written words still control unless the user explicitly asks to reuse the audio's dialogue.

For a reaction, show the cause first. If the cause and reaction are separated, connect them with one gaze or camera shift. If an event is staged, simulated, or a near miss, make the uninjured or undamaged state observable so it is not rewritten as real harm.

## Material inspection and mapping

Materials may supply only directly visible or audible attributes. When the user calls someone only a `person` or `subject`, retain that neutral term. Do not infer age, gender identity, race, ethnicity, nationality, profession, family relationship, rank, disability, vulnerability, dominance, or other demographic/story attributes from face, body, clothing, action, filename, metadata, or upload order. User-supplied identity terms remain valid; otherwise describe only observable hair, facial, clothing, accessory, structure, and posture details needed for visual continuity.

Use this priority:

```text
User assignment > Prompt description > Direct material content > Filename/metadata > Upload order
```

Upload order creates numbering, not identity evidence. Use it only as a stable final tie-breaker when the user requests a direct assumption, candidates are equally plausible, and the number of required slots equals the number of candidates.

Mapping procedure:

1. Take the next unassigned entity from the required-entity ledger.
2. Compare all candidates by subject count, clothing layers, silhouette, structure, props, and scene role.
3. Assign the best candidate, then continue to the next entity.
4. Audit omissions: every required entity appears, and every active material performs its declared role only.
5. Subtract active items from the full list and enumerate the remainder under `[Unused Materials]`.

Do not merge named characters, reuse one single-person image for several simultaneous people, or add an unmentioned reinforcement reference to a role already covered by the user's mappings. A group image may define that same group when no better independent mapping exists. When several materials jointly define one entity, say so explicitly.

For a video whose role is unspecified, inherit only task-relevant motion, camera, pacing, scene, or audio. Do not inherit person, clothing, and whole environment by default.

When references for one subject conflict, follow the user's assignment. Without one, choose the clearest story-fit reference per attribute. Ask only when the core identity remains unresolved.

## Mapping confidence

- **High**: map and continue.
- **Medium**: make the conservative mapping and disclose the one consequential assumption in a `Material Mapping Note:` outside the prompt.
- **Low, no core impact**: leave the material unused.
- **Low, core impact**: ask one consolidated question about identity/count, ownership, front/back, left/right, facing direction, edit target, source video, extension direction, or anchor role, then stop. Do not emit a provisional prompt in the same response.

If user mappings visibly conflict with the asset, follow the user and confirm once only when failure is almost certain. Do not interrupt for style, lighting, ordinary camera choices, or image quality that can be resolved conservatively. A `Material Mapping Note:` is not a substitute for the required stop on low-confidence core ambiguity; use an assumption only when the user explicitly requests a direct assumed version.

If materials arrive without any generation, edit, or extension goal, ask for the minimum creative goal instead of inventing a story.

## Output contract

Match the user's language and reference notation. Do not renumber explicit handles.

Default delivery:

- output the prompt body only;
- use no outer title, explanation, or code fence;
- retain task-internal labels when they help execution;
- write inferred mappings directly into the role section rather than exposing a reasoning table;
- include all known inactive handles under `[Unused Materials]`;
- return one version unless alternatives are requested.

Permitted post-prompt notes, each at most one line and only when needed:

- `Supplementary Suggestion:` for a missing material;
- `Selection Note:` for one disclosed long-text range or causally complete event selected by the agent;
- `Material Mapping Note:` for one genuinely consequential medium-confidence mapping or a required local-path alias/upload-order assumption;
- `Material Note:` for a hard input-limit violation;
- `Parameter Note:` for a locked-parameter conflict or first/last ratio mismatch;
- `Additional Note:` when exact text, formulas, signs, product specs, or frame timing also require prepared material or post-production.

For a mixed sequential request, use `Step 1:` and `Step 2:`. Explicitly state that the second operation uses the first output as its new master.

If low-confidence ambiguity affects a core fact, the output contract is suspended: ask the consolidated question and stop. Do not attach any submit-ready prompt, selection note, or mapping note until the user resolves the ambiguity or explicitly authorizes an assumed version.

## Result diagnosis and repair

Use this workflow only when the user supplies the generated result and the intended prompt or material-role contract. If the result itself is missing, or the intended target cannot be reconstructed from supplied evidence, request the missing core item and stop.

1. **Reconstruct the intended contract:** operation, subjects/count, active references and roles, event order, end states, edit/extension scope, anchors, camera, dialogue, audio, and external locked parameters.
2. **Inspect the full result:** for video, examine its opening, ending, every event and cut, identity/count/ownership changes, camera, visible text, and relevant audio; for a still, inspect the complete frame. Record only observable or audible facts.
3. **Build a mismatch ledger:** pair each intended fact with the observed result and mark it `met`, `partially met`, `not met`, or `not observable`. Do not infer an internal model cause from the output alone.
4. **Trace repairs to evidence:** connect each repair to a documented rule in this skill or to a directly inspected reference fact. Common evidence-grounded repairs include clearer one-to-one mapping, a closed edit inventory, one dominant state change per stage, explicit ownership/end states, strict-anchor routing, boundary continuity, and separated audio roles.
5. **Return the next executable artifact:** rewrite the appropriate generation, editing, or extension prompt. Put external parameter corrections in a `Parameter Note:`. If an explanation is useful, label any unverified causal explanation as `Hypothesis:` and keep it outside the submit-ready prompt.

Never diagnose a result from a thumbnail, filename, duration alone, or vague dissatisfaction when the missing visual/audio evidence matters. Never claim that a prompt change guarantees correction; it changes the control contract and likelihood of adherence.

## Capability disclosures

Never claim:

- timestamps are frame-accurate;
- editing reproduces every source frame;
- keyframes reproduce every intermediate frame;
- first/last or extension boundary frames are pixel-identical;
- a generated transition preserves both originals pixel for pixel;
- subtitles, signs, formulas, specifications, or UI copy are exact;
- all references appear simultaneously;
- prompt wording bypasses input limits;
- examples guarantee a result.

When exactness is essential, produce the best prompt and recommend prepared source graphics, generation, and post-production together.

## Final audit

Confirm all of the following before delivery:

- one primary task per prompt, or two explicitly sequential operations;
- original identity, count, scene, ownership, blocking, causality, and outcome preserved;
- every required entity covered once and no story fact inferred from appearance;
- one explicit role per active material;
- no missing handle or raw Asset ID in the prompt;
- all known unused handles enumerated;
- no inaccessible item presented as inspected;
- no demographic or story identity inferred from appearance, filename, metadata, or upload order;
- distinct entities mapped separately;
- one-person references do not define several simultaneous characters;
- long stages each have one primary state change and one visible end state;
- user-authored time ranges preserved unless the user authorizes change;
- editing defines master, scope, count, inheritance, and closed preservation;
- audio editing defines changed and preserved sounds, lip-sync timing, and visual inheritance;
- locked ratio/duration behavior respected outside the prompt;
- extension direction, observed boundary, audio/motion continuity, and single-instance topology explicit;
- exact standalone first/last role sentences used when strict anchors are intended;
- keyframes ordered without frame-reproduction promises;
- storyboards include reading order and excluded placeholder content;
- blockout classified as coarse or fine;
- camera and emotion expressed observably;
- speaking stages preserve speaker, mouth state, line, language, audio role, and screen position;
- a required speaking role with no reliable transcript uses its bound reference audio without invented words;
- identifiers remain identifiers;
- no external parameters, keys, endpoints, internal analysis, or run metadata in the prompt;
- no unrequested boilerplate;
- no unresolved placeholders;
- any result-repair claim is tied to inspected output evidence, and uncertain causes are labeled as hypotheses.

## Runtime compatibility

- A text-only agent may use explicit labels but must not claim attachment inspection.
- A multimodal agent should inspect all active materials and use the two-pass review for a large set.
- Without filesystem access, preserve user labels and apply the inaccessible-material fallback.
- Without network access, do not resolve a URL or infer its content from its name.
- This skill prepares text. It does not require a generation API, file write, network call, or binary output unless the user's separate workflow requests one.
