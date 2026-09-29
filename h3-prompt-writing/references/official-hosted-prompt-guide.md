# Official Hosted H3 Prompt Guide

Use this reference for MiniMax Design, Hailuo, or another hosted H3 surface that follows MiniMax's August 11, 2026 user guide. It governs hosted freeform prompt planning and upload handles. It does not replace the structured grammar in `base-en.txt` / `ref-en.txt`, native-ComfyUI tags, or API transport roles.

## Sources And Boundary

- MiniMax H3 showcase revision dated August 11, 2026: `https://app.notion.com/p/MiniMax-H3-The-Next-Gen-Open-Weight-Multimodal-Generation-Model-5cdd99c3d331822397f18130e7b480a8`
- Provider-linked developer prompt-expansion guide: `https://vrfi1sk8a0.feishu.cn/wiki/Vztzwstuqi3MQKkxs8QcGmxinxe`
- Read `runtime-surfaces.md` before applying these rules to an API or local workflow. An API `role` field and an on-screen `@Image N` handle are different mechanisms.

Hosted/API freeform prose may follow the user's requested language when the target surface supports it. Structured `base-en.txt` / `ref-en.txt` sections remain English, with the original language preserved only for dialogue, lyrics, and visible scene text as those guides require.

## Default Formula

Build a hosted prompt from three semantic parts:

```text
Reference Asset Instructions
Core Concept
Shot-by-Shot Description
```

Headings are useful but not mandatory when the surface accepts ordinary prose. The three jobs are mandatory in substance whenever references or multiple beats exist.

## Reference Asset Instructions

Identify hosted uploads by their visible upload order when the surface exposes these handles:

- `@Image N`
- `@Video N`
- `@Audio N`

Give every asset one explicit job. Useful roles include:

- character, object, product, wardrobe, or environment identity;
- opening frame, ending frame, other keyframe, composition, or storyboard;
- visual style without copying source content;
- motion, performance, or camera-motion reference;
- voice tone/timbre, complete audio reuse, or a bounded audio segment;
- direct video editing, continuation, replacement, or preservation source.

State the exact features that must survive. For copied or reperformed vocals, include the exact dialogue or lyrics when preservation matters. Omit this whole section for text-only work.

Do not transfer these `@...` handles into structured or native-ComfyUI prompts. Use the label system documented for that profile.

## Core Concept

Use one compact sentence to establish:

- subject;
- location;
- visible action;
- genre, medium, and style;
- special camera treatment;
- editing topology when it is load-bearing.

H3 uses cuts by default on the hosted surface. Say `one continuous take` only when the action truly remains continuous, then avoid separate `Shot N` or cut blocks.

Describe camera mechanics directly. For an orbit-like result, specify the paired translation and pan direction, such as truck left while panning right, rather than relying only on the abstract word `orbit`.

## Shot-By-Shot Description

Use shots or time ranges as audiovisual timeline segments. For each segment, define only what it needs:

- shot size, framing, and established subject;
- environment and visible action;
- camera movement;
- on-screen or off-screen speaker and exact dialogue;
- synchronized physical sound, ambience, and music behavior;
- referenced asset and the exact quality borrowed from it;
- required visible text, logo, title, tagline, or button copy;
- targeted exclusions or preservation rules.

Keep dialogue proportional to the segment. When one line spans a cut, state that it continues from the previous shot. Identify the speaker again after a cut, especially when an off-screen voice becomes visible. Re-establish framing and which known character appears so continuity does not depend on pronouns alone.

Prefer observable instructions over metaphors. Name the source state, intermediate change, target state, and what remains unchanged.

If no audience-only music is wanted, end with an explicit no-music instruction such as `Non-diegetic music: N/A`. Do not simultaneously request a score or BGM.

## Mode-Specific Use

### Multimodal Fusion

Map character, motion, camera, environment, voice, and music assets separately. Do not ask one reference to control unrelated qualities unless the user intends that coupling.

### Image-To-Video

- One endpoint image: state whether it is the opening or ending frame.
- Two endpoint images: describe the continuous motion, lighting, and sound path between them. H3 does not automatically insert a cut between first and last frames.
- When other reference roles are present, follow the actual surface or API contract instead of assuming endpoint and reference roles can be mixed.

### Text-To-Video

Describe subject appearance, environment, action, and style more fully because no media supplies them. A reliable default progression is establishing space, readable action coverage, then a detail or payoff shot; change that structure when the user's concept requires a oner or another topology.

## Exact Text Workaround

The August 11 page gives an official hosted-surface workaround for garbled text: provide the intended lettering as an image reference and state, `This content must be interpreted as an image, not processed as text.`

Use this only when the user can supply or approves a text plate. Assign the plate one bounded job, preserve its spelling, typography, layout, and aspect, and animate or composite the plate as a whole instead of asking H3 to regenerate individual letters. This improves fidelity but does not guarantee pixel-identical lettering from a generative render; when exact pixels are non-negotiable, generate a clean plate region and composite the original plate afterward.

## August 11 Pattern Routing

The revised showcase expands the hosted planning evidence. Use these as content patterns, not as new modes or syntax:

- **Selective hand-drawn overlays:** identify one live-action object per beat, transform only that object into 2D marks, and preserve the photographic world around it.
- **Causal brand systems:** carry one line, dot, glyph, logo fragment, or shape through every composition so each state visibly produces the next.
- **Kinetic typography:** treat literal type as the main subject, quote it exactly, define its physical transformation, and protect readable states.
- **Direct AR compositing:** edit the supplied real footage in place; preserve source camera, environment, timing, occlusion, and untargeted subjects rather than generating a replacement scene.
- **Locked game/UI flows:** keep the camera and layout stable; describe input, state change, feedback, and settle for each cursor, arrow, selection, dodge, or companion action.
- **Industrial and robotic edits:** favor one mechanically plausible action and strict change-versus-preserve boundaries for robot, workspace, lighting, contact shadows, and occlusion.
- **Poster and anime motion:** use flat high-contrast graphic grammar, designed crops, silhouettes, and bounded layer movement rather than drifting into generic pseudo-3D coverage.
- **Food/product launch:** make material and appetite details causal and visible, then land exact localized copy in a stable closing state.

## Common Pitfalls

- One unstructured paragraph with no hierarchy: separate asset roles, concept, and chronology.
- Uploaded assets with no job: label every used asset and say what to preserve.
- Music plus `no BGM`: resolve the contradiction or scope the rules to different segments.
- A declared continuous take plus many cuts: choose one topology.
- Face consistency without an identity reference: request or use a character image when identity fidelity is essential.
- Under-described text-to-video: supply appearance, setting, action, and medium/style.
- Exact text described only semantically: quote the literal copy and use the image-plate workaround when needed.

## Review Checklist

- Every hosted handle exists and retains one stable role.
- The core concept defines the whole clip without replacing the timeline.
- Shots cover the requested duration in order.
- Camera direction is mechanical and physically coherent.
- Speaker visibility and dialogue continuation are explicit.
- Literal copy is exact.
- Music rules do not conflict.
- Endpoint motion converges rather than jumping.
- Settings and transport metadata remain outside the paste-ready prompt unless the surface explicitly requires them there.
