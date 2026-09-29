# Source Coverage Ledger

## Contents

- [Purpose](#purpose)
- [Lark A88 prompt guide](#lark-a88-prompt-guide)
- [BytePlus ModelArk 2607689](#byteplus-modelark-2607689)
- [Provider optimizer 0.3.3](#provider-optimizer-033)
- [BytePlus visual assets](#byteplus-visual-assets)
- [Raw-to-local media mapping](#raw-to-local-media-mapping)
- [Validation](#validation)

## Purpose

Use this ledger when revising the skill. It records where each supplied-document section and media asset is represented. A check mark means the information is encoded operationally; it does not mean source wording was copied verbatim.

`references/desk-prompt-patterns.md` is Clip-desk craft, not a first-party source. Do not treat it as coverage of Lark, BytePlus, or the provider optimizer, and do not let it invent capabilities, limits, or API fields.

## Lark A88 prompt guide

Source: `https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh`

| Source section | Covered in |
|---|---|
| Scope: text-only, image/video/audio reference, editing | `SKILL.md`, `source-boundaries.md` |
| 1.1 core formula and parameter separation | `prompt-architecture.md` |
| 1.2 hard limits, recommended ranges, higher retry ranges, multi-view handling | `source-boundaries.md`, `SKILL.md` |
| 1.2 material roles, exclusions, one-to-one mapping, same-subject views | `prompt-architecture.md`, `optimizer-runtime.md` |
| 1.3 music/SFX/dialogue/subtitle syntax and language reinforcement | `prompt-architecture.md` |
| 2.1 multi-reference order, grouping, profiles, scene activation | `prompt-architecture.md` |
| 2.2 long stages, end states, ranges, exact points, relative timing | `prompt-architecture.md` |
| Requests longer than one 30-second clip | `source-boundaries.md`, `prompt-architecture.md` |
| 2.3 locked editing, anchor, and extension parameters | `source-boundaries.md`, `task-contracts.md` |
| 2.4 master-video editing, subject/background/audio variants | `task-contracts.md` |
| 2.5 forward/backward extension and boundary inspection | `task-contracts.md` |
| 3.1 first/last anchors, multi-keyframes, storyboards, blockouts | `task-contracts.md` |
| 3.2 one-click creation | `task-contracts.md` |
| 3.3 seamless transitions | `task-contracts.md` |
| 3.4 emotional direction | `prompt-architecture.md` |
| 3.5 camera vocabulary and observable expansion | `prompt-architecture.md` |
| 4 checklist | `prompt-architecture.md`, `optimizer-runtime.md` |
| 5 limitations | `source-boundaries.md`, `optimizer-runtime.md` |
| 6 examples disclaimer | `source-boundaries.md` |
| Every concrete Lark example pattern | `examples.md` |

The authenticated plain-text capture contained no image/video markers or media URLs. Its word-level guidance is covered; no unsupported visual claim is attributed to that source.

## BytePlus ModelArk 2607689

Source: `https://docs.byteplus.com/en/docs/ModelArk/2607689`

| Source section | Covered in |
|---|---|
| Get the skill and `/sd25-pe` usage | `source-boundaries.md` |
| Overall introduction and production positioning | `source-boundaries.md` |
| Typical capability table | `source-boundaries.md` |
| Locked versus unlocked task distinction | `source-boundaries.md` |
| Editing/anchor/extension role and trigger rules | `source-boundaries.md`, `task-contracts.md` |
| Storyboard versus keyframe alignment | `source-boundaries.md`, `task-contracts.md` |
| Reference input recommendations | `source-boundaries.md` |
| Basic prompt, mapping, edits, anchors, timestamps, negatives | `prompt-architecture.md` |
| Camera, action/expression, blockout, storyboard, keyframe guidance | `prompt-architecture.md`, `task-contracts.md` |
| Differences from Seedance 2.0 | `source-boundaries.md` |
| Coarse and fine blockout examples | `examples.md`, `media-evidence.md` |
| Storyboard and keyframe examples | `examples.md`, `media-evidence.md` |
| Instruction, reference-image, and audio editing examples | `examples.md`, `media-evidence.md` |
| Extension, one-click, and transition examples | `examples.md`, `media-evidence.md` |
| Summary and disclaimer boundary | `source-boundaries.md` |

## Provider optimizer 0.3.3

| Optimizer section | Covered in |
|---|---|
| Purpose, when to use, output-only boundary | `SKILL.md`, `optimizer-runtime.md` |
| Eleven non-negotiable principles | `optimizer-runtime.md` |
| Text, missing, readable, inaccessible, and over-limit input states | `optimizer-runtime.md` |
| Story contract, dialogue ledger, required entities, causal reveal | `optimizer-runtime.md` |
| Novel and long-form compilation | `optimizer-runtime.md` |
| Two-pass material review and observation/story split | `optimizer-runtime.md` |
| Mapping priority, roles, cardinality, unused materials | `optimizer-runtime.md` |
| Mapping confidence and minimal clarification | `optimizer-runtime.md` |
| Legal selection/mapping notes and mandatory stop on low-confidence core ambiguity | `optimizer-runtime.md` |
| Primary-task router and sequential operations | `SKILL.md`, `task-contracts.md` |
| Parameter rules and notes | `SKILL.md`, `source-boundaries.md` |
| Generation and multi-reference templates | `prompt-architecture.md`, `task-contracts.md` |
| Space/blocking and long-video override | `prompt-architecture.md`, `optimizer-runtime.md` |
| Editing inventory, closed scope, motion-slot replacement | `task-contracts.md` |
| Audio editing | `task-contracts.md` |
| Extension topology and boundary rules | `task-contracts.md` |
| Exact anchors, keyframes, storyboards, blockouts | `task-contracts.md` |
| Emotion, camera, dialogue, products | `prompt-architecture.md` |
| Neutral subject terms, no demographic inference, and speaking from audio without invented words | `SKILL.md`, `optimizer-runtime.md`, `prompt-architecture.md` |
| Evidence-grounded generated-result repair | `SKILL.md`, `optimizer-runtime.md` |
| Output contract, note types, final checklist, runtime notes | `optimizer-runtime.md` |
| Every distinct official optimizer example pattern | `examples.md` |

## BytePlus visual assets

Each identifier below must have a dedicated entry in `media-evidence.md` and a role in `examples.md` or the media index.

Images:

`image_001 image_002 image_003 image_004 image_005 image_006 image_007 image_008 image_009 image_010 image_011 image_012 image_013 image_014 image_015 image_016 image_017 image_018 image_019 image_020 image_021 image_022 image_023 image_024 image_025 image_026 image_027 image_028 image_029 image_030 image_031 image_032 image_033 image_034 image_035 image_036 image_037 image_038 image_039 image_040 image_041 image_042 image_043 image_044 image_045 image_046 image_047 image_048 image_049 image_050 image_051`

Videos:

`video_052 video_053 video_054 video_055 video_056 video_057 video_058 video_059 video_060 video_061 video_062 video_063 video_064 video_065 video_066 video_067 video_068 video_069 video_070 video_071 video_072 video_073`

## Raw-to-local media mapping

The BytePlus HTML/Markdown source uses raw provider basenames `img_001` through `img_051` and `vid_000` through `vid_021`. This skill's evidence ledger uses one continuous local identifier namespace:

- raw `img_NNN` maps directly to local `image_NNN` (`img_001` -> `image_001`; `img_051` -> `image_051`);
- raw `vid_NNN` maps to local `video_MMM`, where `MMM = NNN + 52` (`vid_000` -> `video_052`; `vid_021` -> `video_073`).

The local identifier is an audit alias, not a provider upload handle. Runtime prompts must use the user's actual `@Image N`, `@Video N`, and `@Audio N` labels. Exact downloaded filenames and source URLs remain in the extraction manifest used for the audit; do not infer semantic roles from either filename or numeric order.

## Validation

Run from the skill directory:

```bash
python3 scripts/validate_coverage.py
python3 scripts/prompt_lint.py --self-test
```

`validate_coverage.py` verifies required files, source concepts, every image ID, every video ID, and the absence of TODO placeholders. It is a coverage guard, not a substitute for human source review.
