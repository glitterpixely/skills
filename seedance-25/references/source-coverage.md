# Source Coverage Ledger

## Contents

- [Purpose](#purpose)
- [Lark A88 prompt guide](#lark-a88-prompt-guide)
- [BytePlus ModelArk 2607689 & Nov 2026 spec bundle](#byteplus-modelark-2607689--nov-2026-spec-bundle)
- [Provider optimizer 0.3.3](#provider-optimizer-033)
- [Craft & research companion modules](#craft--research-companion-modules)
- [BytePlus visual assets](#byteplus-visual-assets)
- [Raw-to-local media mapping](#raw-to-local-media-mapping)
- [Validation](#validation)

## Purpose

Use this ledger when revising the skill. It records where each supplied-document section, API specification, media asset, and companion module is represented operationally.

`references/desk-prompt-patterns.md`, `references/desk-continuity-and-coverage.md`, and `references/research-mechanics.md` provide Clip-desk craft heuristics and published ByteDance research context; they never invent undocumented capabilities, limits, or API fields over `references/source-boundaries.md`.

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

## BytePlus ModelArk 2607689 & Nov 2026 spec bundle

Primary prompt guide: `https://docs.byteplus.com/en/docs/ModelArk/2607689` (`seedance-2-5-prompt-guide`, including the `2026-11-07` 10-item FAQ update), plus `seedance-2-5`, `create-video-generation-task-api`, `model-pricing`, `seedance-portrait-asset-guide`, and `badcase-report-api` (`checked 2026-11-10`).

| Source section | Covered in |
|---|---|
| Get the skill and `/sd25-pe` usage | `source-boundaries.md` |
| Overall introduction, capability table, and locked vs. unlocked tasks | `source-boundaries.md` |
| Public model ID `dreamina-seedance-2-5-260628`, endpoint, `1080p` 10-bit HEVC cap (`4K` unsupported), mono audio | `source-boundaries.md`, `SKILL.md` |
| Online token pricing (`$6.40–$11.70` / M tokens) & two-step `480p -> 1080p` `draft_task` parameter lock | `source-boundaries.md`, `optimizer-runtime.md` |
| `omni_reference_task_type` (`auto` / `reference` / `edit` / `extend`) & `4–30s` edit source video floor | `source-boundaries.md`, `task-contracts.md`, `prompt_lint.py` |
| Real-human face restriction, 30-day same-account ModelArk portrait trust, & 24h URL expiry | `source-boundaries.md` |
| Nov 7, 2026 10-item troubleshooting FAQ (`8n+1` edit frames, `yuvj420p`, chronological upload order, `normal human eyes`, `2.0->2.5` `.mov` bridge, outpaint routing) | `source-boundaries.md`, `task-contracts.md`, `prompt-architecture.md` |
| 72h `CasePlatformV1BadcaseReport` diagnostic endpoint (including `:85` vs `:177` doc note) | `source-boundaries.md` |
| Editing/anchor/extension role and trigger rules | `source-boundaries.md`, `task-contracts.md` |
| Storyboard, keyframe, blockout, one-click, and transition examples | `examples.md`, `media-evidence.md` |
| Differences from Seedance 2.0 & unsupported-claim boundaries | `source-boundaries.md` |

## Provider optimizer 0.3.3

| Optimizer section | Covered in |
|---|---|
| Purpose, when to use, output-only boundary, and 12 non-negotiable principles | `SKILL.md`, `optimizer-runtime.md` |
| Text, missing, readable, inaccessible, and over-limit input states | `optimizer-runtime.md` |
| Story contract, dialogue ledger, required entities, novel compilation | `optimizer-runtime.md` |
| Two-pass material review, observation/story split, mapping priority & confidence | `optimizer-runtime.md` |
| Primary-task router, sequential operations, parameter notes, result-repair ladder | `SKILL.md`, `task-contracts.md`, `optimizer-runtime.md` |
| Neutral subject terms, no demographic inference, audio vocalization without invented words | `SKILL.md`, `optimizer-runtime.md`, `prompt-architecture.md` |
| Distinct official optimizer example patterns & lint-verified canonical templates | `examples.md` |

## Craft & research companion modules

All markdown files in `seedance-25/` stay strictly `<= 40,000` bytes (`validate_coverage.py`) so single-call `read_file` invocations never truncate:

| Module | Scope |
|---|---|
| `references/desk-prompt-patterns.md` | Action mechanics, bilingual combat VFX (`闪切`), continuous action, four-mode timing (`8–12` shot readable default + opt-in `16–24` compact Chinese blitz), 2.5D letterbox pop-out, public-dump exclusions |
| `references/desk-continuity-and-coverage.md` | Observational & curiosity vignettes, literal multi-shot control, multi-shot continuity & Conversational Goldilocks prosody, diegetic phone-camera comedy, door-to-door result notes, oval-masked reference plates & `[Cut to]` coverage |
| `references/research-mechanics.md` | Primary ByteDance Seed papers (`Seaweed-7B`, `Seedance 1.0`/`1.5 Pro`/`2.0`, `FlowAct-R2`, `Tarsier2`, `Phantom`, `HuMo`, `RewardDance`), 6 training pillars, architecture-backed directing rules, and the `Seedance 2.5` Evidence Boundary table |

## BytePlus visual assets

Images:

`image_001 image_002 image_003 image_004 image_005 image_006 image_007 image_008 image_009 image_010 image_011 image_012 image_013 image_014 image_015 image_016 image_017 image_018 image_019 image_020 image_021 image_022 image_023 image_024 image_025 image_026 image_027 image_028 image_029 image_030 image_031 image_032 image_033 image_034 image_035 image_036 image_037 image_038 image_039 image_040 image_041 image_042 image_043 image_044 image_045 image_046 image_047 image_048 image_049 image_050 image_051`

Videos:

`video_052 video_053 video_054 video_055 video_056 video_057 video_058 video_059 video_060 video_061 video_062 video_063 video_064 video_065 video_066 video_067 video_068 video_069 video_070 video_071 video_072 video_073`

## Raw-to-local media mapping

- raw `img_NNN` maps directly to local `image_NNN` (`img_001` -> `image_001`; `img_051` -> `image_051`);
- raw `vid_NNN` maps to local `video_MMM`, where `MMM = NNN + 52` (`vid_000` -> `video_052`; `vid_021` -> `video_073`).

Local identifiers are audit aliases; runtime prompts always use the uploader's `@Image N`, `@Video N`, and `@Audio N` labels.

## Validation

Run from the skill directory:

```bash
python3 scripts/validate_coverage.py
python3 scripts/prompt_lint.py --self-test
```

`validate_coverage.py` verifies required files, frontmatter description length (`<= 380` chars) and YAML validity, per-file byte caps (`<= 40,000` bytes), routing cues, local file and `#anchor` slug integrity, sourced concepts, all 51 image and 22 video IDs, lint cleanliness of canonical examples, and absence of TODO markers.
