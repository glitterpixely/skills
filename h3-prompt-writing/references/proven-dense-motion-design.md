# Proven Dense Motion-Design Patterns

Use this reference for high-energy H3 character trailers, title sequences, editorial motion graphics, game-interface showcases, and clips whose plot is a material or surface transforming. Architectures A and B distill two user-confirmed successful 15-second freeform prompts. Architecture C distills public H3 prompts that repeatedly land when the event is one material changing state. Treat the patterns as surface-specific empirical evidence, not as official MiniMax grammar or a universal guarantee.

## Core Lesson

Do not equate density with overload. Both successful prompts use many instructions, but they externalize hierarchy:

1. a global design, reference, and identity contract;
2. a complete chronological edit or state plan;
3. global motion, audio, preservation, and exclusion rules.

This lets each local beat inherit a stable visual constitution instead of repeating it. Judge atomic workload and state clarity, not average seconds per cut.

## Architecture A: Parameterized Editorial Montage

Use this architecture for a reusable character-reveal template driven by rapid contrast between cinematic action and graphic cards.

- Begin with a `PARAMETERS` dictionary for literal names, status copy, subtitles, or project text. Keep each symbol single-valued and use it consistently. Bracketed values may remain placeholders while authoring a template; fill them for a concrete production job.
- Give one reference sole authority over identity, proportions, wardrobe, materials, colors, and style while allowing environment, action, and effects to adapt to that identity.
- Declare one global editorial system: palette, type behavior, graphic motifs, parallax, sharpness hierarchy, and how the character interacts with typography.
- State the exact cut count and cover the complete timeline with numbered, contiguous ranges. Give every cut a distinct compositional job such as face, activation, card, world, detail, impact, velocity, hero moment, or identity.
- Alternate action and text-led cards so the graphic states reset the rhythm rather than competing with uninterrupted combat.
- Stage typography temporally: show the exact copy clearly first, then let the character, silhouette, or cropped close-up overlap it for depth.
- Use controlled option sets in a reusable template when all options fill the same functional slot and should adapt to the supplied character.
- Put global editing rhythm and score design after the cut plan. Synchronize typography hits, impacts, transitions, the hero peak, and the final reveal stinger.
- Finish with a longer identity or project payoff that consolidates the name, subtitle, character, and governing motif.

This architecture demonstrates that 13 distinct cuts in 15 seconds can work. It is not evidence for a required cut count or for simplifying every dense timeline.

## Architecture B: Geometry-Causal Interface Journey

Use this architecture for a game UI or product-interface sequence that must feel like one operating system rather than a slideshow.

- Assign every reference one bounded job: layout, identity, equipment, product design, icon set, final composition, or motion language. State exclusions such as “motion-language source only; never reproduce the board literally.”
- Front-load an exact identity and product lock, including face, proportions, wardrobe, materials, colors, and signature equipment.
- Divide the timeline into named functional stages such as selection, equipment, inspection, modules, lock-in, and deploy.
- Carry existing geometry forward: bracket to tile, tile to product, leader line to module path, modules to summary cards, focus rail to palette wipe.
- Describe each interaction as input → state change → feedback → settle. Useful elements include cursor travel, selection jump, button compression, bar fill, docking, pressure pulse, rebound, and locked state.
- Use color semantically. Reserve the accent for active selection, progress, confirmation, or CTA rather than distributing it decoratively.
- Keep the interface-readable viewpoint stable. Use planar parallax and restrained product rotation instead of camera motion that destroys UI comprehension.
- End on an exact final composition and deliberate hold, even when the hold is brief.

## Architecture C: Material-Causal Transformation

Use this architecture when the plot is one surface changing state: line art becoming a scene, embroidery stitches becoming motion, paint leaking from a mirror or torch, type becoming smoke / neon / metal / paper.

- Name the source material and the destination material before any camera flourish.
- Keep one rail. Enumerate every intermediate state in order (for example: tea bag → pour → steam line-work → armchair scene → boxed product → tagline hold).
- Quote any on-screen copy exactly, including case and punctuation. Land the tagline, title, or HUD string as a readable last-frame state with a hold, not as a floating sticker.
- Declare topology in the prompt: one continuous transformation, or hard-cut beats. Do not write a oner that secretly wants 13 cards.
- Bind identity or product on a separate reference from the transforming material. A storyboard sheet supplies shot order only.
- Diegetic material sound (pour, stitch, paper fold, mirror creak) belongs in the soundscape; do not add music unless the user asked.
- Preserve the untransformed world until the leak or transform actually reaches it.

This architecture is for craft, product, and beauty-first H3 work. It is not a license to paraphrase brand copy or to mix surface syntaxes: use hosted `@Image N` handles only on a hosted H3 surface that exposes them, native-ComfyUI `<Picture N>` tags only for connected nodes, and structured Context-IR labels only in the structured profile.

## Shared Success Conditions

- State whether energy comes from hard-cut contrast or continuous transformation.
- Give each time range one dominant information purpose even when it contains several ordered micro-actions.
- Keep the identity, product, text, and interface as sharp information planes; localize blur and streaks to transitions or foreground layers.
- Centralize literal copy separately from its animation behavior.
- Make transitions carry state instead of decorating a cut.
- Use sparse bounded motion cues—two-frame stagger or rebound, restrained degrees of rotation, small scale changes—as motion-character accents rather than universal values.
- Protect the governing system with targeted negatives: no redesign, reference-board leakage, fake text, forbidden colors, duplicate assets, destructive camera motion, or style drift.
- Land on a recognizable payoff whose duration matches its job; do not impose one universal minimum hold.

## Evidence-Calibrated Review

When a user confirms that a prompt worked, treat that result as stronger evidence than a generic capacity heuristic. Do not automatically reduce cuts, text states, references, prompt length, controlled alternatives, short cards, short holds, or frame-scale cues.

If the output is available, compare it with the prompt and name observed misses: omitted or merged states, incorrect text, broken transition causality, identity drift, reference leakage, palette drift, or a weak final payoff. Revise those defects while preserving the successful architecture. A visually impressive result does not prove that every instruction was followed, so ask for or inspect the output when exact compliance is the question.

## Surface Boundary

`PARAMETERS`, `CUT 01 | 0.00-1.10s`, named macro-stage ranges, `EDITING`, `BGM DESIGN`, and `GLOBAL MOTION RULES` are proven freeform organizational devices, not official structured fields. Preserve them only on a hosted/native freeform surface that supports them. Otherwise translate their content into the selected official grammar and use the target surface's real media handles.

Validate hosted chronology and declared parameters with:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile hosted --mode MODE --duration SECONDS
```
