<div align="center">

# Creative AI Skills

**From a creative brief to a prompt you can use.**

Video direction · Reference workflows · Songwriting · Prompt validation

A personal collection by [glitterpixely](https://github.com/glitterpixely), built for working with creative AI tools through an assistant.

[Explore the skills](#choose-a-skill) · [Seedance 2.5 guide](#seedance-25-summary) · [Install](#installation) · [Try a brief](#example-briefs) · [Contribute](CONTRIBUTING.md) · [License](LICENSE)

</div>

---

## What’s inside

Five focused skills for turning ideas, scripts, images, and audio references into structured video and music prompts. Each skill combines a practical workflow with supporting craft guidance and model-specific references.

- **Direct the scene:** define action, camera movement, timing, reference roles, and continuity.
- **Shape the song:** develop a concept, lyrics, vocal direction, instrumentation, and arrangement.
- **Refine the result:** compare a generated output with the brief and make targeted changes.
- **Check the prompt:** use the included validators where available to catch structural problems before generation.

## Choose a skill

| Skill | Use it for | Included resources |
| --- | --- | --- |
| **[Seedance 2.5](seedance-25/SKILL.md)** | Video generation, reference mapping, storyboards, editing, and extensions | Prompt architecture, task contracts, examples, prompt linter, coverage validator |
| **[MiniMax H3](h3-prompt-writing/SKILL.md)** | Audiovisual direction, first/last frames, reference-led scenes, and targeted edits | Mode and runtime guidance, motion patterns, prompt linter, coverage validator |
| **[Kling 4](kling-4-prompting/SKILL.md)** | Kling 4.0 and Flash prompts, image animation, keyframes, and Omni references | Capability notes, prompt patterns, review and repair guidance |
| **[MiniMax Music 3.0](minimax-music-30/SKILL.md)** | Song captions, lyrics, vocal direction, and full arrangements | Genre guide, **1,000 templates**, prompt linter, coverage validator |
| **[Suno Song Builder](suno-song-builder/SKILL.md)** | Original songs, hooks, lyrics, instrumental scores, and iteration | Songcraft guidance and Suno controls reference |

Start with the tool you plan to generate in. Open its `SKILL.md` for the workflow, then follow the references relevant to your task.

## Seedance 2.5 summary

The [`seedance-25`](seedance-25/SKILL.md) skill combines first-party capability rules ([`source-boundaries.md`](seedance-25/references/source-boundaries.md), [`prompt-architecture.md`](seedance-25/references/prompt-architecture.md), [`task-contracts.md`](seedance-25/references/task-contracts.md), [`optimizer-runtime.md`](seedance-25/references/optimizer-runtime.md)) with field-tested directing craft and architecture notes ([`desk-prompt-patterns.md`](seedance-25/references/desk-prompt-patterns.md)).

### Core envelope and duration rules

- **Duration:** **30 seconds** by default (`Standard` mode, 4–30s single-pass generation). Dreamina web also exposes a **Long Video** mode (**30–180 seconds**) when explicitly requested (`--long-video` in `prompt_lint.py`). Multi-clip segmentation plans remain available for multi-call workflows above 30s.
- **Multimodal references:** Up to **50 total assets** per request (up to 30 images, 10 videos totaling $\le$30s, and 10 audio clips totaling $\le$30s) bound with explicit roles (`@Image 1`, `@Video 1`, `@Audio 1`) and `[Unused Materials]` exclusions.
- **Primary operations:** One operation per prompt—**Generation** (including keyframes, storyboards, 3D blockouts, one-click, and seamless transitions), **Editing** (`@Video 1 is the sole editing master`), or **Extension** (`Extend @Video 1 forward/backward`). Never phrase an editing master or extension source as `"Reference @Video 1"` (`参考 <视频1>`), which misroutes the job to ordinary reference generation.
- **Cost-aware workflow:** Validate multi-shot blocking in **Draft Mode** (`draft=true` / 480p preview) before promoting the seed to 1080p/4K (`draft=false`), and use **localized time-window editing (`局部重拍`)** to repair a 2–4s flaw rather than re-rolling a full 30s clip.

### ByteDance Seed research lineage & prompting implications

| Paper | arXiv ID | Core mechanism | What it means for prompts |
| --- | --- | --- | --- |
| **Seedance 1.0** | [`2506.09113`](https://arxiv.org/abs/2506.09113) | Decoupled spatial/temporal DiT + **Multi-Shot MM-RoPE** + native cut-boundary pre-training | Explicit `Shot N` labels and cut counts (`受控多段序列`) trigger learned hard-cut transitions inside a single pass. |
| **Seedance 1.5 Pro** | [`2512.13507`](https://arxiv.org/abs/2512.13507) | **Dual-Branch MMDiT** joint audio-video co-denoising + >10$\times$ distillation | Sound effects (`<...>`), ambience, and lip phonemes denoise simultaneously with video frames; concrete sound cues tighten visual timing. |
| **Seedance 2.0** | [`2604.14148`](https://arxiv.org/abs/2604.14148) | Unified multi-modal backbone across text, `@image`, `@video`, and `@audio` | Give each reference asset one non-overlapping job (`identity` vs. `environment` vs. `motion` vs. `voice`). |
| **Phantom** | [`2502.11079`](https://arxiv.org/abs/2502.11079) | Cross-modal alignment on non-frame text-image-video triplets (`Phantom-Data`) | Exclude both background and static pose on portrait references (`do not copy its background or static standing pose`) to prevent pose leakage. |
| **HuMo** & **OmniHuman-1** | [`2509.08519`](https://arxiv.org/abs/2509.08519), [`2502.01061`](https://arxiv.org/abs/2502.01061) | **Time-Adaptive CFG** (layout/camera early; `@Image` identity & `@Audio` lip-sync late) | Front-load the 180° stage map and camera move in clause 1; allow `0–1s` for geometry to settle; add **rhythm carriers** (breathing, weight shift) so speaking bodies do not freeze. |
| **RewardDance** & **VideoReward** | [`2509.08826`](https://arxiv.org/abs/2509.08826), [`2501.13918`](https://arxiv.org/abs/2501.13918) | 26B VLM reward judge with Chain-of-Thought verification & Flow-DPO | Write beats as verifiable state checklists (`entry state -> physical action -> observable exit state`) rather than mood adjectives. |
| **Tarsier2** | [`2501.07888`](https://arxiv.org/abs/2501.07888) | 40M fine-grained chronological video captioner | Keep actions in strict forward chronological order (`[camera] + [actor + action] + [environment response]`); avoid literary metaphors (`意识流`). |
| **Seaweed-7B**, **APT**, & **AAPT** | [`2504.08685`](https://arxiv.org/abs/2504.08685), [`2501.08316`](https://arxiv.org/abs/2501.08316), [`2506.09350`](https://arxiv.org/abs/2506.09350) | Causal 3D VAE, 1-step Adversarial Post-Training, and KV-cached sliding-window attention | Powers low-cost `Draft` previews and 30s horizon stability; re-tag characters (`Name, 2-word trait`) after cuts or heavy occlusion so they re-bind inside the active attention window. |

### 6-part multi-shot continuity formula

For complex multi-shot clips, [`desk-prompt-patterns.md`](seedance-25/references/desk-prompt-patterns.md#multi-shot-continuity-craft) codifies a reusable 6-part structure:

1. **Reference & character header:** Visual traits + limb/accessory left-right asymmetry locks (`white mechanical right arm; hip holster stays empty`) + starting hand/inventory state (`arrives empty-handed`).
2. **Visual style + energy/physics locks:** Medium and palette (keeping 2D layer grammar free of live-action bokeh/DOF terms), anti-slide footwork (`feet always plant, push, leap, or roll, never slide`), and sub-object material physics.
3. **Avoid block:** Concise hard exclusions (`no subtitles, no BGM, no extra foreground characters, no fade-out`) checked for self-contradiction against the body.
4. **Global premise & 180° stage map:** 1-sentence story summary + `screen left / screen right` landmark coordinates + `air between bodies` depth separation.
5. **Scene header:** Continuity mode, speed/time state, and scene-scoped visual/audio shifts.
6. **Shot breakdown (`Shot N`):** Camera framing & move in clause 1 $\rightarrow$ per-shot prop state restatement $\rightarrow$ causal `A -> B -> C` action chain with 2-word character anchors (`Kira, lilac buns`) $\rightarrow$ isolated speaker + closed-mouth listeners ($\le$2.5 words/s) $\rightarrow$ kinetic `Cut as <active motion>` trigger.

### Automated checks in `seedance-25/scripts/prompt_lint.py`

In addition to material limits, reference role bindings, timeline gaps/overlaps, and mode contracts, `prompt_lint.py` checks for:

- `DIALOGUE_DENSITY` — warns when a timed shot exceeds $\ge$3.0 spoken Latin-script words per second.
- `NEGATION_CONFLICT` — catches contradictions between `Avoid` bans (`no freeze frames`, `no slow motion`) and body instructions (`hit-stop`, `定格`, `speed ramp`, `子弹时间`).
- `EDIT_REFERENCE_TRAP` — warns if an edit or extension prompt phrases the master/source video as `Reference @Video N` (`参考 <视频N>`).
- `MORPH_TOKEN_RISK` — flags non-negated `变形` / `morph into` / `shape-shift into` in generation prompts in favor of `闪切` (`flash-cut`).
- `STYLE_2D_LENS_CONFLICT` — flags 2D cel/hand-drawn/gouache prompts mixed with live-action bokeh or shallow-DOF lens terms.
- `UNSUPPORTED_HANDLE_SYNTAX` — catches un-normalized wrapper/dump tokens (`<<<Image1>>>`, `@[ref]`, `<视频1>`).

## Installation

Every skill uses the portable `SKILL.md` + `references/` + `scripts/` layout and plain-text Markdown, so it works with **any AI coding agent, desktop assistant, IDE, or chat interface**.

### 1. Any agent with a local `skills/` directory

Clone this repository:

```bash
git clone https://github.com/glitterpixely/skills.git
cd skills
```

Copy the skill folder you want (or symlink/clone the repository) into your agent's skills directory:

| Agent / Environment | Typical skills path |
| --- | --- |
| **Antigravity** | `~/.gemini/config/skills/<skill>` |
| **Claude Code** | `~/.claude/skills/<skill>` |
| **Codex** | `${CODEX_HOME:-$HOME/.codex}/skills/<skill>` |
| **Hermes** | `${HERMES_HOME:-$HOME/.hermes}/skills/<skill>` |
| **OpenCode / Cursor / Other** | Your configured local `skills/` directory |

Example copy command (set `skills_dir` to your agent's path):

```bash
skill="seedance-25"
skills_dir="$HOME/.gemini/config/skills"
mkdir -p "$skills_dir"

# Preserve an existing installation instead of overwriting it.
if [ -e "$skills_dir/$skill" ]; then
  printf 'Already installed: %s\nBack up the existing folder before replacing it.\n' "$skills_dir/$skill"
else
  cp -R "./$skill" "$skills_dir/$skill"
fi
```

Copy the **entire skill folder** so that `references/`, `templates/`, and `scripts/` remain available alongside `SKILL.md`. To update later, run `git pull --ff-only` in the cloned repository and refresh your installed copy.

### 2. Any chat UI, Project, Gem, or Custom GPT

No CLI or agent runtime is required:

1. Upload or attach the skill's `SKILL.md` file (and the relevant files from `references/`) to your **Claude Project**, **Gemini Gem**, **ChatGPT Custom GPT**, or directly into a chat thread.
2. Give your brief in plain language—the assistant will follow the workflow and rules in `SKILL.md`.

## Example briefs

These prompts work in any assistant once the relevant skill is loaded or attached:

**A small visual story (`seedance-25`)**

```text
Using the seedance-25 skill, write a 15-second video prompt.
A tiny witch tries to lift a fallen star into her wheelbarrow.
One character, one garden setting, one clear visual payoff.
Use a gentle camera move, preserve a storybook look, and include no music.
```

**A reference-led character moment (`kling-4-prompting`)**

```text
Using the kling-4-prompting skill, animate my attached character image.
Preserve the face, outfit, and illustration style. The character notices
a glowing moth, reaches toward it, and smiles as it lands on one finger.
Keep the action readable and list any generation settings separately.
```

**An original song direction (`suno-song-builder`)**

```text
Using the suno-song-builder skill, develop an original indie-pop song about
finding your confidence again. Warm vocals, tactile percussion,
and a chorus that feels hopeful without becoming grandiose.
Give me a style prompt and complete lyrics in separate paste-ready blocks.
```

For MiniMax Music, the [genre guide](minimax-music-30/references/genre-router.md) helps you navigate the [template library](minimax-music-30/templates). Adapt a template to the song’s premise, vocal character, and arrangement.

## Repository layout

```text
skills/
├── LICENSE
├── README.md
├── seedance-25/
├── h3-prompt-writing/
├── kling-4-prompting/
├── minimax-music-30/
└── suno-song-builder/
```

Inside each skill:

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Main instructions and workflow (portable across all agents) |
| `references/` | Supporting craft guidance, examples, and capability notes |
| `scripts/` | Python 3 validation helpers (stdlib only, no third-party packages required) |
| `templates/` | Music prompt templates, in the MiniMax Music skill |
| `agents/openai.yaml` | Optional display metadata for runtimes that read it |

## Validation

The Seedance, H3, and MiniMax Music skills include standalone Python 3 validators (using only the Python standard library):

```bash
python3 seedance-25/scripts/prompt_lint.py --help
python3 h3-prompt-writing/scripts/lint_h3_prompt.py --help
python3 minimax-music-30/scripts/lint_music_prompt.py --help
```

Follow the chosen skill’s instructions for the correct mode, duration, input files, or runtime surface. A passing prompt check establishes structural compliance; the generated video or song still needs visual or listening review.

## Scope and maintenance

These skills provide prompting guidance and local validation helpers. Generation runs in the relevant creative platform or runtime, using your own access. Capability notes record their sources and boundaries; check those references when a model version, interface, or feature changes.

Found a broken reference, an outdated capability, or a useful improvement? [Open an issue](https://github.com/glitterpixely/skills/issues) or see the [contribution guide](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE).
