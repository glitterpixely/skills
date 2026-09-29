# Hosted H3 Creative-Director JSON Profile

Use this profile only when the target hosted H3 surface accepts freeform JSON-shaped prompts, or when the user explicitly asks to match a working community prompt written this way. It is a content-organization profile, not the official Context-IR schema and not a substitute for native-ComfyUI media tags.

## Canonical hierarchy

```json
{
  "archetype": "Artistic / Fashion / Conceptual",
  "duration": "15s",
  "prompt": {
    "concept": {
      "title": "...",
      "description": "...",
      "duration": "15s",
      "rhythm_structure": {
        "0-2s": "..."
      }
    },
    "reference_contract": {
      "@Image 1": "Exact role, inherited features, and excluded baggage"
    },
    "camera_direction": {
      "shot_type": "...",
      "forbidden": ["..."],
      "camera_journey": "..."
    },
    "typography": {
      "allowed_words": [],
      "treatment": {
        "not_flat_overlay": true,
        "required_properties": []
      }
    },
    "visual_style": {
      "overall": "...",
      "inspired_by": [],
      "color_palette": [],
      "materials_and_texture": "..."
    },
    "motion_language": {
      "follows_music": false,
      "core_behavior": "..."
    },
    "sound_design": {
      "music": "none",
      "overall": "...",
      "synchronization_rules": []
    },
    "storyboard": {
      "total_beats": 0,
      "beat_duration": "...",
      "beats": [
        {
          "id": "01",
          "time": "0.0–2.0",
          "description": "Opening state, dominant action, transition operator, camera, synchronized sound, and visible end state."
        }
      ]
    },
    "continuity_and_exclusions": {
      "preserve": [],
      "forbidden": []
    }
  }
}
```

Omit empty optional sections instead of padding them with placeholders. A production prompt contains final values only.

## Compilation rules

1. **Archetype** names the production lane, not a vague mood.
2. **Concept description** locks the render constitution: subject count, reference treatment, environment, palette, texture, transformation mechanism, pacing, and final payoff.
3. **Rhythm structure** is a compact index of the entire timeline. Its ranges must exactly match the detailed storyboard.
4. **Reference contract** gives every image/video/audio one bounded job, lists inherited features, and excludes unwanted identity, environment, crop, lighting, or style baggage. Mirror the host's actual handle syntax. The sample uses the official hosted guide's `@Image 1`; do not transfer it to a surface with different labels.
5. **Camera direction** separates camera behavior from subject and graphic motion. The forbidden list must block plausible but wrong solutions such as cuts in a one-take, static framing in a montage, teleportation, hidden transitions, full-body reframes, or freeze frames.
6. **Typography** contains every exact allowed string, entry behavior, material, z-order, and readable state. If exact text is not requested, omit the section or use an empty inventory and forbid generated text.
7. **Visual style** converts each reference into operational features, then locks palette and materials. Do not merely list aesthetic adjectives.
8. **Motion language** defines persistent micro-motion, transition operators, directionality, and whether behavior follows music. State what must remain alive between large beats.
9. **Sound design** maps visible events to exact tactile sounds. Separate music policy, ambience, physical SFX, and silence. Honor the user's sound policy; do not add music unless requested.
10. **Storyboard** makes every beat auditable: source state, dominant change, camera behavior, synchronized sound, explicit transition into the next beat, and visible landing state.
11. **Continuity and exclusions** protect identities, counts, props, reference style, typography, and final-frame obligations without generic boilerplate.

## Density and pacing

- H3's normal single-generation window is 4–15 seconds. Do not represent a 30-second H3 film as one ordinary generation; use two coordinated 15-second prompts and a handoff state when needed.
- A deliberately restrained one-take may use five 3-second beats when one continuous mechanism carries the piece.
- For an explicitly fast VFX, transformation, or character-showcase brief, 8–10 beats in 15 seconds or 13–16 beats across a two-part 30-second package can be a planning starting point, not a provider rule or universal default. Preserve a user-confirmed architecture and adjust to observed results. Use one dominant payoff per beat and only the cuts or named graphic transitions allowed by the brief.
- Repeat critical rules at different abstraction levels only when the repetition has a job: constitution in `concept`, timing in `rhythm_structure`, persistent behavior in `motion_language`, and execution in `storyboard`.

## Transition chain

End every beat by initiating the next transition. Strong patterns include:

- RGB outlines tear into scanlines; reversed scanlines reform the next silhouette;
- a brush stroke fills the frame; wet ink opens into the next environment;
- a gold disc expands into an eclipse; the eclipse iris becomes an eye;
- a raven wing crosses the lens; feathers reveal the next composition;
- a material shatters; fragments lock into the next object's contour.

Do not use unexplained morphing, teleportation, generic dissolves, or hidden transitions when a visible causal operator can connect the states.

## Verification

Before delivery, verify:

- valid JSON when strict parsing matters;
- duration matches the surface limit;
- rhythm ranges and storyboard ranges agree exactly;
- beats cover the full duration without gaps or overlaps;
- total beat count equals the beats array;
- every reference has one explicit role;
- exact visible strings appear only in the typography inventory and intended beats;
- every beat has one dominant information job and a visible landing state;
- every transition is causal;
- sound events map to visual events;
- all preservation and exclusion rules are compatible;
- the prompt uses the actual host's media syntax.

The prompt linter is not a JSON-schema validator and does not prove that the nested `rhythm_structure` and `storyboard` agree. Check JSON syntax separately and compare their ranges and counts explicitly. Serialize the final chronological beats as a hosted text prompt for the existing timing checks; a successful check of that projection does not certify the original JSON structure. When the production prompt is already hosted text, lint it directly:

```bash
python3 scripts/lint_h3_prompt.py PROMPT.txt --profile hosted --mode MODE --duration SECONDS
```
