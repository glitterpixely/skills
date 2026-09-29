# Runtime surfaces

Route first. These surfaces share the caption-and-lyrics concept but do not share one request schema. Facts are sourced as of 2026-08-13; recheck linked primary documentation when emitting executable installation or hosted API guidance.

## Surface matrix

| Surface | Caption field | Lyrics field | Duration control | Seed | Streaming | Output |
|---|---|---|---|---|---|---|
| Hosted MiniMax Music API | `prompt` | `lyrics` | Not exposed in the reviewed request schema | Not exposed | Supported; streamed output must be hex | URL or hex; MP3/WAV/PCM with selectable sample rate and bitrate |
| SGLang-Omni | `instructions` | `input` | `max_new_tokens` at 25 frames/second | `seed` | Must be `false` | 32 kHz stereo WAV response body |
| Diffusers modular pipeline | `prompt` | `lyrics` | `audio_duration` seconds | `torch.Generator` | No documented external streaming path | Native 44.1 kHz stereo tensor |
| Native ComfyUI workflow | `Caption` text widget | `Lyrics` text widget | `max_duration` seconds | workflow `seed` | Workflow execution, not token streaming | Saved audio through workflow, documented as MP3 |

The hosted `music-cover` model is a related platform feature, not an open-weight Music 3.0 mode.

## Hosted MiniMax API

Endpoint:

```text
POST https://api.minimax.io/v1/music_generation
Authorization: Bearer $MINIMAX_API_KEY
Content-Type: application/json
```

Current model identifiers:

- `music-3.0`: paid or Token Plan, documented at 120 RPM
- `music-3.0-free`: free tier, documented at 3 RPM
- `music-cover` and `music-cover-free`: hosted cover-generation companion models

Because availability and rate limits can change, verify the live endpoint documentation before presenting these as current.

### Hosted vocal request

Use:

- `model`: required
- `prompt`: optional for a vocal request, 0–2,000 characters; use it anyway for reliable musical direction
- `lyrics`: required unless `lyrics_optimizer` is true, 1–3,500 characters
- `lyrics_optimizer`: set true only when the user wants the platform to create lyrics from `prompt`
- `audio_setting`: optional sample rate, bitrate, and format
- `output_format`: `url` or `hex`; URL expires after 24 hours
- `stream`: optional boolean; when true, output must be `hex`

Do not add local fields such as `seed`, `max_new_tokens`, `instructions`, `input`, or `audio_duration`.

The official rewriter's 250–450-word default can exceed the hosted API's 2,000-character `prompt` ceiling. Count characters after composing and compress the caption without losing its three-layer logic.

### Hosted instrumental request

Set `is_instrumental: true`, provide a `prompt` of 1–2,000 characters, and omit `lyrics`. Do not use a fake lyric placeholder on this surface.

### Hosted audio settings

Allowed documented values:

- `sample_rate`: `16000`, `24000`, `32000`, `44100`
- `bitrate`: `32000`, `64000`, `128000`, `256000`
- `format`: `mp3`, `wav`, `pcm`
- `output_format`: `url`, `hex`

Use `url` for convenient non-streaming workflows and download promptly because it expires after 24 hours. Use `hex` when streaming or when a self-contained response is required.

### Hosted lyric generation

Endpoint: `POST /v1/lyrics_generation`.

Modes:

- `write_full_song`: create a complete song from an optional prompt
- `edit`: edit or continue supplied lyrics

Relevant fields:

- `prompt`: up to 2,000 characters; an empty prompt generates a random song
- `lyrics`: up to 3,500 characters and effective only in `edit` mode
- `title`: optional; the API preserves a supplied title

The response includes `song_title`, comma-separated `style_tags`, and structured `lyrics` that can feed the hosted music endpoint.

### Hosted cover companion

Use only when explicitly requested.

- Quick mode: send `model: music-cover`, exactly one of `audio_url` or `audio_base64`, and a target-style `prompt` of 10–300 characters. If lyrics are absent, hosted ASR extracts them.
- Advanced mode: call `/v1/music_cover_preprocess`, review the returned `formatted_lyrics`, then send its `cover_feature_id` plus edited `lyrics` to `/v1/music_generation`.
- Reference audio: 6 seconds to 6 minutes, at most 50 MB, common audio formats.
- `cover_feature_id` is valid for 24 hours and is mutually exclusive with raw audio input.

Do not describe cover generation as a capability of the released open weights.

Primary hosted docs:

- <https://platform.minimax.io/docs/guides/music-generation>
- <https://platform.minimax.io/docs/api-reference/music-generation>
- <https://platform.minimax.io/docs/api-reference/lyrics-generation>
- <https://platform.minimax.io/docs/api-reference/music-cover-preprocess>

## SGLang-Omni open-weight server

The current official model card names SGLang-Omni as a supported server. The current SGLang cookbook documents both single-GPU colocation and two-GPU placement.

Install SGLang-Omni from its current source instructions, then serve:

```bash
CUDA_VISIBLE_DEVICES=0 sgl-omni serve --model-path MiniMaxAI/MiniMax-Music3 --port 8000
```

Or place stages across two devices:

```bash
CUDA_VISIBLE_DEVICES=0,1 sgl-omni serve --model-path MiniMaxAI/MiniMax-Music3 --port 8000
```

Do not promise that an unspecified single GPU has enough memory. Use current hardware documentation and available devices.

### SGLang request contract

Endpoint: `POST http://127.0.0.1:8000/v1/audio/speech`.

Required:

- `model`: normally `MiniMaxAI/MiniMax-Music3`
- `input`: non-empty tagged lyrics
- `instructions`: non-empty music caption

Supported operational controls:

- `seed`: non-negative 64-bit integer; omitted defaults to deterministic seed `0`
- `max_new_tokens`: frame cap, 25 frames per second, maximum 9,000
- `response_format`: `wav`
- `stream`: must be false

For a target upper bound in seconds, calculate:

```text
max_new_tokens = min(9000, ceil(seconds * 25))
```

This is a cap, not a target. The model may stop early. A render that reaches the cap may be truncated even though it returns valid audio.

For instrumental music, local preprocessing still requires non-empty `input`. Use a minimal placeholder:

```text
[Intro]
(instrumental)
```

and explicitly request `instrumental, no vocals` in the caption.

Reject or omit `temperature`, `top_p`, `top_k`, `repetition_penalty`, `voice`, `ref_audio`, `ref_text`, `language`, `task_type`, and `stream: true`. Tempo belongs in the caption; `speed` is not a musical tempo control.

Important preprocessing behavior:

- Put a section tag alone on its line. Text following a leading tag on that same line is silently dropped.
- Markdown residue is removed and special `<|tag value|>` forms are normalized.
- The combined tokenized prompt is capped at 5,000 tokens.
- Byte-identical reproducibility depends on identical lyrics, caption, whitespace, seed, length cap, checkpoint, and runtime.

Primary runtime source: <https://sgl-project.github.io/sglang-omni/cookbook/minimax_music3.html>

## Diffusers open-weight pipeline

MiniMax's current model card says the integration lives on a pending Diffusers branch until the named pull request is merged. Recheck before installing; prefer a stable released Diffusers version once official support lands.

Current documented installation while pending:

```bash
pip install git+https://github.com/huggingface/diffusers@dafe3733fcfdbf3c48915fe77be3aef65b5d6a2d transformers accelerate soundfile
```

Core call:

```python
audio = pipe(
    prompt=caption,
    lyrics=lyrics,
    audio_duration=60.0,
    generator=torch.Generator("cuda").manual_seed(7),
    output="audios",
)[0]
```

The documented pipeline loads components in bfloat16 on CUDA. `audio_duration` is an upper bound. Tags must be alone on their lines. The native pipeline returns 44.1 kHz stereo; use `pipe.sampling_rate` when saving.

Current memory guidance from the model card and Diffusers docs:

- full pipeline: roughly 23 GB VRAM in bfloat16
- automatic CPU offload: roughly 22 GB of free VRAM during generation
- additional layer-by-layer group offload can fit an 8 GB GPU, with a speed tradeoff

Treat these as measured guidance, not universal guarantees. Hardware, drivers, Diffusers revisions, duration, and offload behavior matter.

Diffusers exposes a flow-stage classifier-free guidance component whose reference value is 1.7. Do not expose it in an ordinary creative package. Change it only for an explicitly technical local experiment and label it as surface-specific, quality-affecting tuning.

Primary source: <https://github.com/huggingface/diffusers/blob/minimax-music3-integration/docs/source/en/api/pipelines/minimax_music3.md>

## Native ComfyUI open-weight workflow

Use the official Template Library workflow named `MiniMax Music 3` under Audio. Update ComfyUI if the workflow or nodes are missing.

The official guide points to repacked weights under `Comfy-Org/MiniMax-Music-3`:

- FP16 or INT8 diffusion model -> `ComfyUI/models/diffusion_models/`
- pruned INT8 text encoder -> `ComfyUI/models/text_encoders/`
- DAV VAE -> `ComfyUI/models/vae/`

Use the workflow's separate fields:

- `Caption`: the three-part structured caption
- `Lyrics`: tagged lyrics
- `max_duration`: upper bound in seconds, default 60 in the documented template
- `seed`: reproduce or vary a take
- `tiled_decode`: lowers VAE decode VRAM at the cost of speed and a small seam risk; turn it off on sufficient VRAM for the cleaner path

Do not place workflow settings inside Caption prose.

Primary source: <https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3>
