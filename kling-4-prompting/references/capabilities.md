# Capability and source ledger

Primary source: [Meet All-New Kling 4.0!](https://kling.ai/release-note/release-notes/Kling_4?type=dialog).

Read directly in the browser on **2026-09-28**. The page's complete textual specification tables, highlights, and creation-page section were inspected. Embedded demo clips were not played or independently evaluated. These are vendor claims, not verified performance benchmarks. The ordinary web reader failed to retrieve this dynamic page; browser accessibility text exposed the full article.

## Availability and model boundary

The introduction announces full Kling 4.0 for October and limited Kling 4.0 Flash early access beginning September 28. In context, these are 2026 dates. Account eligibility, regional access, pricing, and actual UI controls are not established by the article. Recheck the official source and target surface when current availability matters.

The full-model table is broader than the Flash table. A capability omitted from the Flash table is **not confirmed for Flash by this source**; omission alone is not proof it is unsupported.

## Full Kling 4.0 specification table

| Item | Documented claim | Prompting consequence |
| --- | --- | --- |
| Generation modes | Text-to-video, image-to-video, First & Last Frames, multi-keyframes, Omni Reference | Choose the input role that expresses the intended control |
| Keyframes | Up to 10 keyframe images | Order visual states; describe the action connecting them |
| Generated duration | 3–30 seconds | Keep each generation within this range; timing prose is not the setting |
| Resolution | 720p, 1080p, 4K | Select in the actual surface; do not imply a frame rate or encoding |
| Dynamic range | Table lists 10-bit HDR for 1080p and 4K | Prose explicitly says coming soon; verify availability |
| Aspect ratio | 21:9, 16:9, 1:1, 9:16, Auto | Preserve the user's requested composition and configured ratio |
| Output audio | Two-channel stereo | Directional sound can be requested; no documented pan controls or stems |
| Text input | Up to 8,000 tokens | Not characters; tokenizer unspecified; concise prompts remain useful |
| Reference images | Up to 10 | Assign identity, layout, style, text, or narrative roles |
| Reference videos | Up to 5, combined duration up to 30 seconds | Includes video subjects according to the highlights prose |
| Reference audio | Voice reference only | Do not generalize to music, SFX, or full-mix transfer |
| Reference subjects/elements | Up to 7 total, including up to 3 video-based elements | Count elements as assets, not merely people visible in a frame |
| Combined reference inputs | Up to 15 across images, videos, voice references, and elements | Per-type caps cannot all be added together |
| Video editing | Up to 5 input clips including 1 primary video; each 3–30 seconds; all clips together at most 30 seconds | Identify the primary edit target; budget its duration with the supporting clips |

### Counting without inventing accounting rules

The combined 15-item cap and the individual caps apply together. Ten images plus five videos already occupy 15 listed references; adding a voice reference would exceed that total. Four editing clips of eight seconds each exceed the 30-second total even though each clip and the clip count fit.

The notes do not fully define whether constituent images inside a saved multi-image element count again, how keyframes share budgets with other image uploads, or how one underlying video linked through an element is accounted for in every UI. Inventory logical references plus their underlying media; use the actual surface's accounting before declaring a near-limit mixed request valid. Do not invent extra allowances or count the same uploaded item twice without evidence. Include video-subject footage when checking the documented total video duration.

No per-voice count, audio length, upload file size, frame rate, file format, seed, negative-prompt field, or reference-weight syntax is specified here.

## Flash specification table

| Item | Explicitly documented for Kling 4.0 Flash |
| --- | --- |
| Generation modes | Text-to-video, image-to-video, Omni Reference |
| Duration | 3–20 seconds |
| Resolution | 720p |
| Dynamic range | 8-bit SDR |

The source describes Flash as faster and suitable for frequent creation, without quantified latency or prices. Its own table does not establish first/last-frame control, multi-keyframes, stereo audio, aspect ratios, exact reference budgets, input-token cap, editing, or extension parity. Check those controls if a Flash job depends on them. Do not claim “Flash cannot do X” solely because X is absent from this table.

## Speech and visible text

The full-model language table names Chinese, English, Japanese, Korean, Spanish, Portuguese, German, French, and Indonesian, followed by “and more.” The multilingual highlights instead include Hindi and omit Indonesian from their examples. The visible-text table includes Indonesian and emojis; its descriptive highlight includes Hindi, emojis, and logos. Preserve this difference when answering exact support questions: the article mentions both languages in different places, but is not a definitive exhaustive per-feature language matrix.

Chinese varieties named include Beijing and Taiwanese Mandarin accents, Northeastern accent, Sichuan dialect, and Cantonese. English accents named include American, British, and Indian. A named accent is not a request to change the script's language. Availability, pronunciation, lip-sync, and lettering still need output-level assessment.

## Highlights translated into useful controls

These summaries are source claims; the prompting choices are craft inferences.

| Release-note section | Claimed capability | Useful authored direction |
| --- | --- | --- |
| Audio-visual performance | Stable fast action, complex camera motion, synchronized speech, nuanced expression | Give a physical action chain, an achievable camera path, and a visible emotional change |
| Professional output | 21:9; forthcoming HDR at 1080p/4K | Compose for the chosen frame; keep HDR status separate from lighting prose |
| Omni image references | Subject and three-view images, grids, infographics, keyframes, wireframes | Explain which input controls identity, layout, style, text, or shot composition |
| Omni video references | Performance, action, camera, pacing; white-model and depth-map videos | Transfer specified geometry/timing while replacing proxy appearance explicitly |
| Consistency | Improved coordination across characters, action, shots, and audio | Assign one source of truth to each dimension and audit the result |
| Creative recreation | Reuse pacing, composition, and visual expression with asset replacement | Separate inherited shot structure from replacement identities and products |
| Precise editing | Expressions, body motion, camera position/motion, style, background | Name the target, interval, change, and preserved content |
| Narrative | Up to 30 seconds, up to 10 keyframes, expanded prompt input | Write a complete progression with an ending; bridge keyframe states |
| Camera | Push/pull, pan, tracking, orbit, shot sizes and transitions | Specify start/end framing and motivated movement |
| Creative styles | Vlog/documentary, clay, glitch, felt, 3D cyber aesthetics, and broader creative work | Describe medium and motion language rather than adding realism indiscriminately |
| Extension | Repeated extensions up to 2 minutes, coming soon | Treat as a future total-length workflow, not a supported 120-second single call |

## Creation-page changes

The article describes a unified input box for multimodal references, grid/list result views, a timeline for previewing/editing/adding assets, and a node canvas with an Agent experience. These are workflow announcements, not instructions for token syntax, automatic multi-shot execution, or API schemas. Inspect the live interface before describing exact buttons or automation steps. A prompt-authoring request does not itself request credit-consuming generation.

## Maintenance

When updating this skill, compare the live release note or newer official Kling guide with this ledger. Update dated status and exact model-specific evidence together; preserve unresolved distinctions until a primary source settles them. Never use older Kling 3, other providers, or generic search snippets to silently fill Kling 4 specification gaps.
