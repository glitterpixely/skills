# Candidate Motion-Design Prompt Patterns

Read `motion-design-fundamentals.md` first. That file supplies the sourced motion-design compiler; this file shows three prompt-derived applications plus one inspected staged-production workflow.

## Evidence Status

Patterns A–C are distilled from prompt-only examples supplied for study. Pattern D is grounded in an inspected MiniMax Design canvas screenshot, but its source clips and final rendered video were not available for direct playback inspection. These patterns are useful planning hypotheses, not verified H3 capability claims. Do not move a pattern into `proven-dense-motion-design.md`, promise exact compliance, or preserve its full density by default until a rendered output and its target surface are available. When output is supplied, compare visible states, text accuracy, reference retention, transition type, timing, and audio synchronization against the prompt.

## Pattern A: Continuous Mechanism-Driven Field

Use for a fixed-camera piece governed by one persistent visual rule rather than a montage.

1. Lock the render domain first: palette, dimensionality, camera, compositing model, and forbidden effects.
2. Establish scale and spatial hierarchy in frame-relative terms.
3. Give each subject one motion path across the complete duration.
4. Define the governing interaction as `condition -> local mapping -> boundary behavior -> synchronization rule`.
5. Describe evolving environment geometry with a bounded verb set so variation stays inside one system.
6. If reference footage supplies only motion, bind that role and explicitly reject its identity, wardrobe, lighting, location, and render style.

Exact per-pixel inversion, mathematical coupling, fixed ratios, zero lag, and anti-aliasing behavior are renderer or compositing claims. Treat them as priorities unless measured; use deterministic post-compositing when they are delivery requirements.

## Pattern B: Product-to-Typography State-Conservation Chain

Use for flat 2D brand films in which an illustrated product physically becomes a title or logo.

1. Define one global visual constitution: fixed camera, palette, outline policy, highlight construction, texture ceiling, and prohibited rendering modes.
2. Build a causal object chain with observable intermediate states, for example: ingredients converge -> merge -> fall -> squash into product -> accumulate -> garnish -> clean hero hold -> contour-morph into exact title -> hard material switch -> secondary copy -> lockup -> living hold.
3. Name the transition operator and ban substitutes:
   - **continuous contour morph**: the source silhouette itself deforms through visible intermediate shapes; no replacement cut, covering mask, or incoming duplicate;
   - **hard material cut**: one-frame replacement with no interpolation, crossfade, intermediate color, or gradual morph;
   - **wipe/mask**: use only when conceal-and-reveal is actually intended.
4. Track state conservation. At every transformation, state which objects are consumed, which attributes carry forward, and what must no longer exist at completion.
5. Separate hold purposes:
   - **clean hero hold**: composition and every element remain still so the product reads;
   - **living lockup hold**: layout remains fixed while one small periodic motion prevents a dead final frame.
6. Map each physical beat to a discrete sound and keep non-diegetic music in its own layer. Silence may begin while visual micro-motion continues.
7. Quote every visible title, tagline, and lockup string exactly. Avoid unspecified seal copy, pseudo-text, or tiny brand copy the model cannot be checked against.

For the official structured profile, a fixed-camera transformation chain is usually one continuous shot with timed phases. Increment `[Shot N]` only at a real cut. Do not use `Shot` as a synonym for every state change. Hosted freeform may use named phases instead.

## Pattern C: Multi-Reference Ensemble Trailer

Use for a short trailer that introduces several distinct referenced characters and assigns each a visual domain.

1. Build a per-character identity matrix: reference source, name, position, face and hair anchors, clothing silhouette and materials, signature prop, accessories, palette, pose language, and prohibited swaps.
2. Assign each uploaded image a bounded job. Replace vague directions such as “fuse every detail from all references” with explicit provenance so faces, outfits, props, and styles do not bleed between subjects.
3. Give the ensemble a shared constitution—render medium, contrast, texture family, transition motif, lighting logic—and then one bounded background and action motif per character.
4. Use a recurring transition bridge, such as one ink wipe or brush sweep, to make separate character domains feel like one film.
5. Treat focal length, aperture, shutter angle, Kelvin values, lens flare, film grain, and resolution as visual or runtime cues rather than guarantees unless the surface exposes measurable controls.
6. Resolve mixed style phrases into a hierarchy. For example, choose `2.5D painted anime` as the render domain and use oil paint, ink wash, and gold leaf only as surface textures; do not simultaneously demand flat anime, photoreal pores, IMAX realism, and incompatible material models without a priority order.
7. Inventory all literal copy before drafting. Assign each phrase one readable beat and one hierarchy level. Character labels, vertical titles, slogans, seals, microcopy, and background script all consume the same typography budget. Do not impose a universal numeric ceiling, but do not assume an unrendered 15-second prompt can spell every layer correctly.
8. Keep each scene's action budget explicit: entrance, one signature action, one camera move, one text reveal, and a settled identity state. Add complexity only when output evidence supports it.
9. In canonical H3 terms, multiple identity/style reference images mean Ref2VA. `Omni Reference`, `Premium Grade`, `2000p`, and similar labels are surface or marketing controls, not new official modes or structured fields.

## Pattern D: Approval-Still to Multi-Clip Assembly

Use when a polished final sequence contains distinct stages that are easier to control as separate H3 generations than as one monolithic prompt. This pattern is supported here by an inspected MiniMax Design canvas screenshot, not by inspection of the rendered source clips or final video.

1. Write a compact production brief covering final duration, aspect ratio, stage order, visual constitution, forbidden elements, sound policy, and final payoff.
2. Write one shared still-frame style signature, then produce one **approval still** per stage. Each still must already prove composition, palette, materials, subject inventory, and camera framing before video generation begins.
3. Give every stage one dominant action and generate it as a separate short source clip from its approved still. Select the H3 mode by the still's actual role: I2VA when it is the literal first frame, FL2VA when two approved endpoints must be connected, or Ref2VA when the still supplies reusable appearance/style rather than a fixed endpoint.
4. Keep the global constitution identical across clips: medium, palette, paper/edge/shadow rules, camera logic, motion vocabulary, scale, and audio family. Vary only the stage-specific object state and action.
5. Render source clips with enough handles for editing, then record the raw duration and the exact retained range from each clip. Source duration is not final timeline duration; several longer source clips may be trimmed into a shorter assembled film.
6. Design editorial handoffs deliberately. Match adjacent clips by object position, silhouette, palette field, motion direction, impact, occlusion, or sound so assembly feels causal rather than like unrelated slideshow cuts.
7. Assemble outside the individual H3 generations: trim, order, hard-cut or bridge, normalize visual/audio levels, and export one final file. Do not describe post-generation stitching as if H3 produced the complete composite in one pass.
8. Run final-film QC separately from per-clip QC: exact duration, aspect ratio, stage order, style consistency, allowed motion vocabulary, text/logo/UI/watermark policy, BGM/voice/subtitle policy, sound effects, and completed payoff frame.
9. Keep an asset graph or manifest that links `brief -> style signature -> approval still -> source clip -> retained range -> final assembly`, with stable filenames for every artifact.
10. Treat text strategy as an independent risk decision. The inspected example explicitly excludes text, logos, UI, watermarks, BGM, voiceover, and subtitles, allowing the generations to focus on tactile image motion and paper sound. If exact typography is required in another project, bind and verify it per clip or add it deterministically in the final assembly; do not assume a multi-clip workflow alone fixes spelling or glyph drift.

The inspected screenshot visibly shows a planning document, a still-frame specification, a group titled “Pizza Collage Approval Stills,” four connected source clips with six-second badges, a final `pizza-collage-process.mp4` with a fifteen-second badge, and a Korean completion report. It does **not** reveal the exact prompts, exact H3 modes, retained edit ranges, or enough frames to judge visual success; do not invent those details.

## Cross-Pattern Drafting Contract

Before writing, record:

- **render constitution**: medium, palette, texture, dimensionality, outline/highlight rules;
- **camera constitution**: locked or mobile, permitted moves, framing changes;
- **asset authority**: exact role and exclusions for every image/video/audio;
- **state ledger**: object inventory before, during, and after each transform;
- **transition vocabulary**: morph, hard cut, wipe, split, stack, type-on, settle;
- **typography inventory**: exact strings, language, hierarchy, location, entry, hold, exit;
- **audio event map**: diegetic/physical effects versus audience-only music;
- **oracle**: observable frames or events that prove the requested mechanism worked.

## Review And Failure Classification

When a render is available, diagnose one causal layer at a time:

- **profile failure**: surface expected structured grammar but received hosted labels, or vice versa;
- **reference failure**: missing role binding, identity bleed, wardrobe/prop swap, style leakage;
- **state failure**: object replacement instead of morph, skipped intermediate state, duplicate source and target, wrong hard-cut behavior;
- **typography failure**: misspelling, omitted copy, unreadable hierarchy, pseudo-text, too many simultaneous layers;
- **render-constitution failure**: gradients, dark outlines, unwanted 3D/gloss, palette or texture drift;
- **timing failure**: omitted phase, mistimed hold, unresolved state at the endpoint;
- **audio failure**: wrong layer, missing event sync, sound continuing into required silence;
- **capability boundary**: mathematically exact mask, frame-exact timing, or optics claim not verifiable in generation.

Revise only the failed layer, re-lint, and compare the next output against the same observable oracle.