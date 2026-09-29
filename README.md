<div align="center">

# Creative AI Skills

**From a creative brief to a prompt you can use.**

Video direction · Reference workflows · Songwriting · Prompt validation

A personal collection by [glitterpixely](https://github.com/glitterpixely), built for working with creative AI tools through an assistant.

[Explore the skills](#choose-a-skill) · [Install](#installation) · [Try a brief](#example-briefs) · [Contribute](CONTRIBUTING.md)

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

## Installation

### Use with Codex

Clone this repository:

```bash
git clone https://github.com/glitterpixely/skills.git
cd skills
```

Copy the skill you want into your Codex skills directory. For example:

```bash
skill="seedance-25"
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills_dir"

# Preserve an existing installation instead of overwriting it.
if [ -e "$skills_dir/$skill" ]; then
  printf 'Already installed: %s\nBack up the existing folder before replacing it.\n' "$skills_dir/$skill"
else
  cp -R "./$skill" "$skills_dir/$skill"
fi
```

Replace `seedance-25` with any skill folder listed above. Copy the **entire folder** so that references, templates, and scripts remain available. Start a new Codex chat after installation and invoke the skill by name, for example `$seedance-25`.

To update your downloaded copy, run `git pull --ff-only` in the cloned repository. Review the changes and back up any customized installed skill before copying the updated folder. Pulling this repository does not automatically update your installed skills.

### Use with Hermes (Git-backed)

For a single working copy that Hermes can load and Git can track, clone the complete repository inside the active profile's skills directory:

```bash
hermes_home="${HERMES_HOME:-$HOME/.hermes}"
mkdir -p "$hermes_home/skills/creative"
git clone https://github.com/glitterpixely/skills.git \
  "$hermes_home/skills/creative/glitterpixely-skills"
hermes skills list --source local --enabled-only
```

If any of these five skills are already installed elsewhere in that profile, compare and back up those folders **outside the skills directory** before retiring the duplicate installations. Preserve local customizations for review; do not overwrite them blindly. Start a fresh Hermes chat after installation.

The checkout is the installed library: edits to its skill files are immediately local Git changes, and pulling reviewed upstream changes updates the installed files without another copy step. Use authenticated Git access to push owner-authorized updates. Review changes, run the relevant validators, commit only the intended files, push, and verify the remote commit. See [AGENTS.md](AGENTS.md) for the maintenance workflow. This does not create a background auto-push service or update separate Codex installations or other Hermes profiles.

### Use as a reference library

You can also read the Markdown files directly or provide a skill and its relevant reference files to another assistant. The workflows are written in plain text; assistant-specific discovery and tool integration may differ.

## Example briefs

These are requests to give your assistant after loading the appropriate skill. The assistant uses the skill to develop the final generation prompt.

**A small visual story**

```text
Use $seedance-25 to write a 15-second video prompt.
A tiny witch tries to lift a fallen star into her wheelbarrow.
One character, one garden setting, one clear visual payoff.
Use a gentle camera move, preserve a storybook look, and include no music.
```

**A reference-led character moment**

```text
Use $kling-4-prompting to animate my attached character image.
Preserve the face, outfit, and illustration style. The character notices
a glowing moth, reaches toward it, and smiles as it lands on one finger.
Keep the action readable and list any generation settings separately.
```

**An original song direction**

```text
Use $suno-song-builder to develop an original indie-pop song about
finding your confidence again. Warm vocals, tactile percussion,
and a chorus that feels hopeful without becoming grandiose.
Give me a style prompt and complete lyrics in separate paste-ready blocks.
```

For MiniMax Music, the [genre guide](minimax-music-30/references/genre-router.md) helps you navigate the [template library](minimax-music-30/templates). Adapt a template to the song’s premise, vocal character, and arrangement.

## Repository layout

```text
skills/
├── seedance-25/
├── h3-prompt-writing/
├── kling-4-prompting/
├── minimax-music-30/
└── suno-song-builder/
```

Inside each skill:

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Main instructions and workflow |
| `references/` | Supporting craft guidance, examples, and capability notes |
| `agents/openai.yaml` | Codex display metadata and default prompt |
| `scripts/` | Validation helpers, where included |
| `templates/` | Music prompt templates, in the MiniMax Music skill |

## Validation

The Seedance, H3, and MiniMax Music skills include Python prompt validators. Run these commands from the repository root to see their options:

```bash
python3 seedance-25/scripts/prompt_lint.py --help
python3 h3-prompt-writing/scripts/lint_h3_prompt.py --help
python3 minimax-music-30/scripts/lint_music_prompt.py --help
```

Follow the chosen skill’s instructions for the correct mode, duration, input files, or runtime surface. A passing prompt check establishes structural compliance; the generated video or song still needs visual or listening review.

## Scope and maintenance

These skills provide prompting guidance and local validation helpers. Generation runs in the relevant creative platform or runtime, using your own access. Capability notes record their sources and boundaries; check those references when a model version, interface, or feature changes.

Found a broken reference, an outdated capability, or a useful improvement? [Open an issue](https://github.com/glitterpixely/skills/issues) or see the [contribution guide](CONTRIBUTING.md).
