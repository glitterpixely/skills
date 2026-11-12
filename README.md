<div align="center">

<img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/hero-banner.png" alt="Creative AI Skills Studio — Minimalist pastel desk with film clapperboard, bunny notebook, and cassette tape" width="100%" />

# ✦ Creative AI Skills Studio ✦

**From a creative brief to a structured, paste-ready video or music prompt.**

*Video direction · Multimodal reference workflows · Original songwriting · Deterministic prompt validation*

<p>
  <a href="#choose-a-skill"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-video.svg" alt="3 Video Studios" height="26" /></a>
  <a href="#choose-a-skill"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-music.svg" alt="2 Music Studios" height="26" /></a>
  <a href="#validation"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-validators.svg" alt="Python 3 Validators" height="26" /></a>
  <a href="LICENSE"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-mit.svg" alt="MIT License" height="26" /></a>
</p>

<p>
  <a href="https://www.instagram.com/glitterpixely"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-instagram.svg" alt="Instagram @glitterpixely" height="26" /></a>
  <a href="https://x.com/glitterpixely"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-x.svg" alt="X @glitterpixely" height="26" /></a>
  <a href="https://www.tiktok.com/@glitterpixely"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-tiktok.svg" alt="TikTok @glitterpixely" height="26" /></a>
</p>

A curated studio collection by **[glitterpixely](https://github.com/glitterpixely)** ([Instagram](https://www.instagram.com/glitterpixely) · [X](https://x.com/glitterpixely) · [TikTok](https://www.tiktok.com/@glitterpixely)), built for directing video and music models through any AI assistant.

[**Studio Desks**](#studio-desks) · [**Choose a Skill**](#choose-a-skill) · [**Model Guides**](#model-guides--research-lineage) · [**Install**](#installation) · [**Sample Briefs**](#example-briefs) · [**Validators**](#validation) · [**Contribute**](CONTRIBUTING.md)

<img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/divider-pastel.svg" alt="" width="100%" />

</div>

## Studio Desks

Five focused skills for turning ideas, scripts, character sheets, and audio references into structured video and music prompts. Each skill pairs a step-by-step directing workflow with model-specific references and standalone validators.

<div align="center">
  <a href="#video-direction-skills"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/card-video-studio.svg" alt="Desk 01: Video Direction Studio" width="48%" /></a>
  &nbsp;
  <a href="#music--songcraft-skills"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/card-music-studio.svg" alt="Desk 02: Music and Songcraft Studio" width="48%" /></a>
</div>

- **Direct the scene:** define physical action, camera trajectory, timing, reference bindings (`@Image`, `@Video`, `@Audio`), and continuity locks.
- **Shape the song:** develop an original premise, prosody-checked lyrics, vocal posture, focal instrumentation, and dynamic arrangement arcs.
- **Refine the result:** diagnose a rendered clip or track by failure layer and apply targeted single-variable or section-level repairs.
- **Check the prompt:** run the zero-dependency Python 3 linters before generation to catch structural or reference-binding errors early.

<div align="center">
  <img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/divider-pastel.svg" alt="" width="100%" />
</div>

## Choose a Skill

Start with the model you plan to generate in. Open its `SKILL.md` for the core routing protocol, then load only the references needed for your task.

### Video Direction Skills

| Skill | Target Model & Best Use | Key References | Automated Checks |
| --- | --- | --- | --- |
| **[`seedance-25`](seedance-25/SKILL.md)** | **Seedance 2.5 (`dreamina-seedance-2-5-260628`)** — Multi-shot video generation (4–30s & 30–180s Long Video), up to 50 `@` references, storyboards, `8n+1` localized edits, and `.mov` extensions | [`source-boundaries.md`](seedance-25/references/source-boundaries.md), [`prompt-architecture.md`](seedance-25/references/prompt-architecture.md), [`desk-prompt-patterns.md`](seedance-25/references/desk-prompt-patterns.md), [`desk-continuity-and-coverage.md`](seedance-25/references/desk-continuity-and-coverage.md), [`research-mechanics.md`](seedance-25/references/research-mechanics.md) | [`prompt_lint.py`](seedance-25/scripts/prompt_lint.py), [`validate_coverage.py`](seedance-25/scripts/validate_coverage.py) |
| **[`h3-prompt-writing`](h3-prompt-writing/SKILL.md)** | **MiniMax H3** — Audiovisual scene direction, first/last frame interpolation, multimodal `@` asset binding, and delta-only video edits | [`model-contract.md`](h3-prompt-writing/references/model-contract.md), [`official-hosted-prompt-guide.md`](h3-prompt-writing/references/official-hosted-prompt-guide.md), [`omni-reasoning-research.md`](h3-prompt-writing/references/omni-reasoning-research.md) | [`lint_h3_prompt.py`](h3-prompt-writing/scripts/lint_h3_prompt.py), [`validate_coverage.py`](h3-prompt-writing/scripts/validate_coverage.py) |
| **[`kling-4-prompting`](kling-4-prompting/SKILL.md)** | **Kling 4.0 & Flash** — Text-to-video, image animation (`I2V`), start/end keyframes, Omni reference binding, and render diagnosis | [`capabilities.md`](kling-4-prompting/references/capabilities.md), [`prompt-patterns.md`](kling-4-prompting/references/prompt-patterns.md), [`kling-architecture-research.md`](kling-4-prompting/references/kling-architecture-research.md) | Built-in verification gate in [`SKILL.md`](kling-4-prompting/SKILL.md) |

### Music & Songcraft Skills

| Skill | Target Model & Best Use | Key References | Automated Checks |
| --- | --- | --- | --- |
| **[`suno-song-builder`](suno-song-builder/SKILL.md)** | **Suno v6 (`v6`, `v6-wild`, `v6-mini`)** — Original songs, hooks, stressed-meter lyrics, film/game scores, `Max Mode` / `Variety` calibration, natural-language edits, and Suno Studio workflows | [`songcraft.md`](suno-song-builder/references/songcraft.md), [`suno-controls.md`](suno-song-builder/references/suno-controls.md), [`controllable-song-research.md`](suno-song-builder/references/controllable-song-research.md) | 7-block schema & originality gate in [`SKILL.md`](suno-song-builder/SKILL.md) |
| **[`minimax-music-30`](minimax-music-30/SKILL.md)** | **MiniMax Music 3.0** — 8-layer `Caption` design, section-tagged `Lyrics`, instrumental cues, and **1,000 bilingual genre templates** (`100 genres × 10 variants`) | [`genre-router.md`](minimax-music-30/references/genre-router.md), [`prompt-architecture.md`](minimax-music-30/references/prompt-architecture.md), [`music-generation-research.md`](minimax-music-30/references/music-generation-research.md) | [`lint_music_prompt.py`](minimax-music-30/scripts/lint_music_prompt.py), [`validate_coverage.py`](minimax-music-30/scripts/validate_coverage.py) |

### 3D & Real-Time Rendering Skills

| Skill | Target Engine & Best Use | Key References | Automated Checks |
| --- | --- | --- | --- |
| **[`threejs-rendering`](threejs-rendering/SKILL.md)** | **Three.js (`r165–r187+`) & React Three Fiber 9.8** — Photoreal & stylized WebGPU/WebGL2 rendering, AgX/Neutral colour, HDRI/GI, fitted shadows, TSL shaders & compute, `RenderPipeline`/`pmndrs` post, OIT/TAAU/FSR1, 3DGS Gaussian splats, `BatchedMesh`/`BundleGroup`/BVH, WebXR, and gated quality loop (`G0`–`G4`) | [`00-version-gates.md`](threejs-rendering/references/00-version-gates.md), [`11-quality-loop.md`](threejs-rendering/references/11-quality-loop.md), [`14-shaders-tsl.md`](threejs-rendering/references/14-shaders-tsl.md), [`15-react-three-fiber.md`](threejs-rendering/references/15-react-three-fiber.md) | [`validate_coverage.py`](threejs-rendering/scripts/validate_coverage.py), [`physical.mjs`](threejs-rendering/scripts/physical.mjs), [`probe.mjs`](threejs-rendering/scripts/quality/probe.mjs), [`run-gates.mjs`](threejs-rendering/scripts/quality/run-gates.mjs) |
| **[`blender-craft`](blender-craft/SKILL.md)** | **Blender 5.x (`5.0–5.1+`, `Python 3.13`, `bpy`/`bmesh`)** — Hero props, Geometry Nodes 5.x (Bundles, Closures, SDF Volume Grids, `Scene Time` FX, ecosystem scattering), EEVEE painterly/cel anime (`Shader to RGB` + depth haze + Kuwahara), `Ucupaint`/PBR baking, multi-angle AI-video graybox/turnaround plates, `+Z`→`+Y` `.glb` GPU instancing export, and `G1`–`G5` audit gates | [`00-blender5-api-and-gotchas.md`](blender-craft/references/00-blender5-api-and-gotchas.md), [`03-geometry-nodes-scatter-and-environments.md`](blender-craft/references/03-geometry-nodes-scatter-and-environments.md), [`04-materials-pbr-stylized-and-anime.md`](blender-craft/references/04-materials-pbr-stylized-and-anime.md), [`05-uvs-baking-and-glb-export.md`](blender-craft/references/05-uvs-baking-and-glb-export.md) | [`validate_coverage.py`](blender-craft/scripts/validate_coverage.py), [`blender_scene_audit.py`](blender-craft/scripts/blender_scene_audit.py) |

<div align="center">
  <img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/divider-pastel.svg" alt="" width="100%" />
</div>

## Model Guides & Research Lineage

<details open>
<summary><strong>🎬 Seedance 2.5 Guide & ByteDance Seed Research Summary</strong></summary>
<br />

The [`seedance-25`](seedance-25/SKILL.md) skill combines first-party capability and ModelArk rules ([`source-boundaries.md`](seedance-25/references/source-boundaries.md), [`prompt-architecture.md`](seedance-25/references/prompt-architecture.md), [`task-contracts.md`](seedance-25/references/task-contracts.md), [`optimizer-runtime.md`](seedance-25/references/optimizer-runtime.md)) with field-tested directing craft ([`desk-prompt-patterns.md`](seedance-25/references/desk-prompt-patterns.md), [`desk-continuity-and-coverage.md`](seedance-25/references/desk-continuity-and-coverage.md)) and primary-paper mechanics ([`research-mechanics.md`](seedance-25/references/research-mechanics.md)).

### Core Envelope & Duration Rules

- **Duration:** **30 seconds** by default (`Standard` mode, 4–30s single-pass generation). Dreamina web also exposes a **Long Video** mode (**30–180 seconds**) when explicitly requested (`--long-video` in `prompt_lint.py`). Multi-clip segmentation plans remain available for multi-call workflows above 30s.
- **Multimodal references:** Up to **50 total assets** per request (up to 30 images, 10 videos totaling ≤30s, and 10 audio clips totaling ≤30s) bound with explicit roles (`@Image 1`, `@Video 1`, `@Audio 1`, or Dreamina CN `@图片1`, `@视频1`, `@音频1`) and `[Unused Materials]` exclusions. Order multi-subject `@Image` uploads chronologically by first on-screen appearance.
- **Primary operations:** One operation per prompt—**Generation** (`omni_reference_task_type="reference"`), **Editing** (`4–30s` source, `omni_reference_task_type="edit"`, `@Video 1 is the sole editing master`; pre-trim to `8n + 1` frames at 24 fps for exact duration match), or **Extension** (`omni_reference_task_type="extend"`, `Extend @Video 1 forward/backward` with `.mov`). Never phrase an editing master or extension source as `"Reference @Video 1"` (`参考 <视频1>`).
- **Cost-aware workflow:** Validate multi-shot blocking in **Draft Mode** (`draft=true, resolution="480p"`) before promoting the cached Draft ID to `1080p` 10-bit HEVC via `draft_task` (`draft=false`, valid 14 days without re-sending prompt/seed/duration; `4K` is `Seedance 2.0` only), and use **localized time-window editing (`局部重拍`)** to repair a 2–4s flaw rather than re-rolling a full 30s clip.

### ByteDance Seed Research Lineage & Prompting Implications

| Paper | arXiv ID | Core Mechanism | What It Means for Prompts |
| --- | --- | --- | --- |
| **Seedance 1.0** | [`2506.09113`](https://arxiv.org/abs/2506.09113) | Spatial concatenated `MMDiT` self-attention + windowed temporal attention + **Multishot MM-RoPE** + merged specialist SFT + direct-$x_0$ 3-RM RLHF | Explicit `Shot N` labels trigger native multi-shot cuts; keep style pure within one specialist basin and keep exclusion lists `<= 80` words. |
| **Seedance 1.5 Pro** | [`2512.13507`](https://arxiv.org/abs/2512.13507) | **Dual-Branch MMDiT** joint audio-video co-denoising + >10× distillation (`TSCD`, `MeanFlow`, `APT`) | Isolate emotion to the brow and eyes during close-up speech so emotional tokens do not fight `p/b/m` lip closure. |
| **Seedance 2.0** & **FlowAct-R2** | [`2604.14148`](https://arxiv.org/abs/2604.14148), [`2609.35728`](https://arxiv.org/abs/2609.35728) | Unified multimodal reference (`@Image`, `@Video`, `@Audio`, edit, extend) + Diffusion Forcing streaming | Give each reference asset one non-overlapping job (`identity` vs. `environment` vs. `motion` vs. `voice`). |
| **Phantom** & **Phantom-Data** | [`2502.11079`](https://arxiv.org/abs/2502.11079), [`2506.18851`](https://arxiv.org/abs/2506.18851) | Cross-modal alignment on `~1M` non-frame cross-paired identity triplets | Exclude both background and static pose on portrait references (`do not use its background or static standing pose`) to prevent copy-paste leakage. |
| **HuMo** & **OmniHuman-1** | [`2509.08519`](https://arxiv.org/abs/2509.08519), [`2502.01061`](https://arxiv.org/abs/2502.01061) | Facial BCE attention mask + reverse-diffusion timestep CFG ($t \in [1.0, 0.98]$ layout -> $t \in [0.98, 0]$ identity/lip-sync across all frames) | Front-load the 180° stage map and camera move in clause 1; add torso **rhythm carriers** (breathing, weight shift) so speaking bodies do not freeze. |
| **RewardDance** & **DanceGRPO** | [`2509.08826`](https://arxiv.org/abs/2509.08826), [`2505.07818`](https://arxiv.org/abs/2505.07818) | Generative `26B` VLM reward judge scoring `SEED-VL 1.5` Chain-of-Thought criteria via ReFL | Write beats as verifiable state transitions (`entry state -> physical contact -> observable exit state`) rather than mood adjectives. |
| **Tarsier2** | [`2501.07888`](https://arxiv.org/abs/2501.07888) | Frame-grounded 2-stage human SFT + `AutoDQ` temporal DPO video captioner | Keep actions in strict forward chronological order (`[camera] + [actor + action] + [environment response]`); avoid literary metaphors (`意识流`). |
| **Seaweed-7B**, **APT**, & **AAPT** | [`2504.08685`](https://arxiv.org/abs/2504.08685), [`2501.08316`](https://arxiv.org/abs/2501.08316), [`2506.09350`](https://arxiv.org/abs/2506.09350) | Causal `64x` 3D VAE (`8n+1` edit alignment), 1-step Adversarial Post-Training, and sliding-window attention | Re-tag characters (`Name, 2-word trait`) after cuts or heavy occlusion so they re-bind inside the active attention window. |

### 6-Part Multi-Shot Continuity Formula

For complex multi-shot clips, [`desk-continuity-and-coverage.md`](seedance-25/references/desk-continuity-and-coverage.md#multi-shot-continuity-craft) codifies a reusable 6-part structure:

1. **Reference & character header:** Visual traits + limb/accessory left-right asymmetry locks (`white mechanical right arm; hip holster stays empty`) + starting hand/inventory state (`arrives empty-handed`).
2. **Visual style + energy/physics locks:** Medium and palette (keeping 2D layer grammar free of live-action bokeh/DOF terms), anti-slide footwork (`feet always plant, push, leap, or roll, never slide`), and sub-object material physics.
3. **Avoid block:** Concise hard exclusions (`<= 80` words: `no subtitles, no BGM, no extra foreground characters, no fade-out`) checked for self-contradiction against the body.
4. **Global premise & 180° stage map:** 1-sentence story summary + `screen left / screen right` landmark coordinates + `air between bodies` depth separation.
5. **Scene header:** Continuity mode, speed/time state, and scene-scoped visual/audio shifts.
6. **Shot breakdown (`Shot N`):** Camera framing & move in clause 1 → per-shot prop state restatement → causal `A -> B -> C` action chain with 2-word character anchors (`Kira, lilac buns`) → isolated speaker + closed-mouth listeners (`< 2.0` words/s) → kinetic `Cut as <active motion>` trigger.

### Automated Checks in `seedance-25/scripts/prompt_lint.py`

In addition to bilingual material limits (`@Image 1` / `@图片1`), reference role bindings, `Stage N`/`Shot N`/`镜头 N` timeline gaps/overlaps, and mode contracts, `prompt_lint.py` checks for:

- `DIALOGUE_DENSITY` & `CLIP_DIALOGUE_OVERLOAD` — warns when a timed shot reaches `>= 2.0` spoken word-equivalents/s (Latin words + CJK characters) or exceeds clip speech budgets.
- `MISSING_NO_SUBTITLES` — warns when spoken dialogue is present without `No subtitles.` (`无字幕`) or explicit `【...】` subtitle binding.
- `NEGATION_CONFLICT` — catches contradictions between `Avoid` bans (`no freeze frames`, `no slow motion`) and body instructions (`hit-stop`, `定格`, `speed ramp`, `子弹时间`).
- `EDIT_REFERENCE_TRAP` — warns if an edit or extension prompt phrases the master/source video as `Reference @Video N` (`参考 <视频N>`).
- `MORPH_TOKEN_RISK` — flags non-negated `变形` / `morph into` / `shape-shift into` in generation prompts in favor of `闪切` (`flash-cut`).
- `STYLE_2D_LENS_CONFLICT` & `AIRBRUSH_CEL_CONFLICT` — flags 2D cel/hand-drawn prompts mixed with live-action bokeh/DOF or lineless airbrushed painterly terms (respecting symmetrical negations).
- `UNSUPPORTED_HANDLE_SYNTAX` — catches un-normalized wrapper/dump tokens (`<<<Image1>>>`, `@[ref]`, `<视频1>`).

</details>

<details>
<summary><strong>🎥 MiniMax H3 &amp; Kling 4.0 Video Direction Highlights</strong></summary>
<br />

- **MiniMax H3 ([`h3-prompt-writing`](h3-prompt-writing/SKILL.md)):**
  - Enforces a 5-stage causal spine (**Reference Mapping → Anchor Scene → Causal Motion Chain → Camera Trajectory → Synchronized Soundscape**) and a "state every inference" rule drawn from an independent 517-instance physical-reasoning benchmark of H3 (41.97% overall success on implicit prompts; [`omni-reasoning-research.md`](h3-prompt-writing/references/omni-reasoning-research.md)).
  - Separates first/last-frame interpolation bridges from delta-only video edits (`Keep ... unchanged; change only ...`).
- **Kling 4.0 & Flash ([`kling-4-prompting`](kling-4-prompting/SKILL.md)):**
  - Selects deterministically between Text-to-Video, Image-to-Video (`I2V`), Start/End Keyframes, and Omni Multi-Reference workflows ([`kling-architecture-research.md`](kling-4-prompting/references/kling-architecture-research.md)).
  - Reduces "talking statue" failure modes in `I2V` by omitting redundant static portrait descriptions and specifying concrete physical weight transfers and micro-motions.

</details>

<details>
<summary><strong>🎧 Suno v6 &amp; MiniMax Music 3.0 Songcraft Highlights</strong></summary>
<br />

- **Suno v6 ([`suno-song-builder`](suno-song-builder/SKILL.md)):**
  - Supports the **Suno v6 model family** (`v6` flagship, `v6-wild` exploration, `v6-mini` for all users), **`Max Mode`** (extra credits; Suno recommends it for songs over two minutes, close covers, and style transfer), and **`Variety` at `0`** to keep full control of style tags ([`suno-controls.md`](suno-song-builder/references/suno-controls.md)).
  - Integrates **v6 natural-language song editing** (plain-text section, ensemble, or single-word lyric swaps) and **Suno Studio** finishing (Clip Settings, semitone+cent fine pitch, Auto-Stretch, and 12-stem export).
- **MiniMax Music 3.0 ([`minimax-music-30`](minimax-music-30/SKILL.md)):**
  - Provides **1,000 bilingual production templates** across 100 genres ([`templates/`](minimax-music-30/templates)) plus an 8-layer `Caption` formula and stressed-meter `Lyrics` validator ([`lint_music_prompt.py`](minimax-music-30/scripts/lint_music_prompt.py)).

</details>

<div align="center">
  <img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/divider-pastel.svg" alt="" width="100%" />
</div>

## Installation

Every skill uses the portable `SKILL.md` + `references/` + `scripts/` layout and plain-text Markdown, so it works with **any AI coding agent, desktop assistant, IDE, or chat interface**.

### 1. Any Agent with a Local `skills/` Directory

Clone this repository:

```bash
git clone https://github.com/glitterpixely/skills.git
cd skills
```

Copy the skill folder you want (or symlink/clone the repository) into your agent's skills directory:

| Agent / Environment | Typical Skills Path |
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

### 2. Any Chat UI, Project, Gem, or Custom GPT

No CLI or agent runtime is required:

1. Upload or attach the skill's `SKILL.md` file (and the relevant files from `references/`) to your **Claude Project**, **Gemini Gem**, **ChatGPT Custom GPT**, or directly into a chat thread.
2. Give your brief in plain language—the assistant will follow the workflow and rules in `SKILL.md`.

<div align="center">
  <img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/divider-pastel.svg" alt="" width="100%" />
</div>

## Example Briefs

These prompts work in any assistant once the relevant skill is loaded or attached:

**🌸 A small visual story (`seedance-25`)**

```text
Using the seedance-25 skill, write a 15-second video prompt.
A tiny witch tries to lift a fallen star into her wheelbarrow.
One character, one garden setting, one clear visual payoff.
Use a gentle camera move, preserve a storybook look, and include no music.
```

**🦋 A reference-led character moment (`kling-4-prompting`)**

```text
Using the kling-4-prompting skill, animate my attached character image.
Preserve the face, outfit, and illustration style. The character notices
a glowing moth, reaches toward it, and smiles as it lands on one finger.
Keep the action readable and list any generation settings separately.
```

**🍵 An original song direction (`suno-song-builder`)**

```text
Using the suno-song-builder skill, develop an original indie-pop song for Suno v6
about finding your confidence again. Warm vocals, tactile percussion,
and a chorus that feels hopeful without becoming grandiose.
Give me a style prompt and complete lyrics in separate paste-ready blocks.
```

For MiniMax Music, the [genre guide](minimax-music-30/references/genre-router.md) helps you navigate the [1,000-template library](minimax-music-30/templates). Adapt a template to the song’s premise, vocal character, and arrangement.

<div align="center">
  <img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/divider-pastel.svg" alt="" width="100%" />
</div>

## Repository Layout

```text
skills/
├── AGENTS.md                  # Repository automation & sync conventions
├── CONTRIBUTING.md            # Contribution & validator checklist
├── LICENSE                    # MIT License
├── README.md                  # Studio overview & quick-start guide
├── seedance-25/               # Seedance 2.5 video directing & linter
├── h3-prompt-writing/         # MiniMax H3 audiovisual directing & linter
├── kling-4-prompting/         # Kling 4.0 & Flash video directing
├── minimax-music-30/          # MiniMax Music 3.0 + 1,000 templates & linter
├── suno-song-builder/         # Suno v6 songwriting, controls, & Studio workflow
├── threejs-rendering/         # Three.js r187 & R3F 9.8 rendering, TSL, & GPU quality gates
└── blender-craft/             # Blender 5.x modeling, Geometry Nodes, anime/PBR shading, & GLB/scene audit
```

Inside each skill:

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Main instructions and deterministic routing workflow (portable across all agents) |
| `references/` | Supporting craft guidance, academic foundations, examples, and capability notes |
| `scripts/` | Python 3 validation helpers (standard library only, zero third-party dependencies) |
| `templates/` | 1,000 bilingual music prompt templates (`100 genres × 10`), in `minimax-music-30` |
| `agents/openai.yaml` | Optional display metadata for runtimes that read it |

## Validation

The Seedance, H3, and MiniMax Music skills include standalone Python 3 prompt linters and repository coverage validators (using only the Python standard library):

```bash
# Prompt linters
python3 seedance-25/scripts/prompt_lint.py --help
python3 h3-prompt-writing/scripts/lint_h3_prompt.py --help
python3 minimax-music-30/scripts/lint_music_prompt.py --help

# Skill coverage & self-test suites
python3 seedance-25/scripts/validate_coverage.py
python3 h3-prompt-writing/scripts/validate_coverage.py
python3 minimax-music-30/scripts/validate_coverage.py
python3 threejs-rendering/scripts/validate_coverage.py
python3 blender-craft/scripts/validate_coverage.py
```

Follow the chosen skill’s instructions for the correct mode, duration, input files, or runtime surface. A passing prompt check establishes structural compliance; the generated video or song still needs visual or listening review.

## Scope & Maintenance

These skills provide prompting guidance and local validation helpers. Generation runs in the relevant creative platform or runtime, using your own access. Capability notes record their sources and boundaries; check those references when a model version, interface, or feature changes.

Found a broken reference, an outdated capability, or a useful improvement? [Open an issue](https://github.com/glitterpixely/skills/issues) or see the [contribution guide](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE).

<div align="center">
  <br />
  <p>
    <a href="https://www.instagram.com/glitterpixely"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-instagram.svg" alt="Instagram @glitterpixely" height="26" /></a>
    <a href="https://x.com/glitterpixely"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-x.svg" alt="X @glitterpixely" height="26" /></a>
    <a href="https://www.tiktok.com/@glitterpixely"><img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/badge-tiktok.svg" alt="TikTok @glitterpixely" height="26" /></a>
  </p>
  <img src="https://raw.githubusercontent.com/glitterpixely/skills/assets/footer-stamp.svg" alt="crafted with care · glitterpixely studio" width="320" />
</div>
