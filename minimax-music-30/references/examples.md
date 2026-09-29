# Surface-safe examples

Use these examples as serialization patterns, not as fixed creative defaults. Replace all creative content with the user's brief. Never reuse example lyrics as if they were user-owned material.

## Structured Caption plus Lyrics

Caption:

```text
### Global Metadata

Alternative R&B / restrained electronic soul at a slow, late-pocket tempo. The song begins guarded and nocturnal, then opens into a quietly decisive final chorus. Keep the mix intimate and low-lit: rounded sub-bass, dry percussion, warm negative space, and no festival-scale synths.

### Vocal Details

One close female alto lead with a smoke-soft lower register and precise consonants. Verses use conversational, slightly behind-the-beat phrasing; choruses lengthen the vowels without turning into a belt. Add a low unison double only on the hook and a small three-part harmony in the final chorus. Use subtle tuning and a short dark plate; no glossy vocal stacks.

### Arrangement

The Intro isolates a detuned electric-piano figure and distant room texture. The Verse adds muted sub-bass and rim clicks while staying narrow and dry. The Pre-Chorus removes the rim clicks, raises a filtered pulse, and lets the vocal move closer. The Chorus restores a deep kick, opens the electric piano, and introduces the low hook double without adding new harmonic layers. Verse 2 adds a soft counter-synth that answers only at line endings. The Bridge drops drums and bass, leaving voice, electric piano, and one unstable pad. The final Chorus returns the full groove, adds the small high harmony, and widens the counter-synth. The Outro ends on the exposed piano figure rather than a long fade.
```

Lyrics:

```text
[Verse]
I left the hallway light on low
Like you might still remember where to go

[Pre-Chorus]
One more hour, one less excuse

[Chorus]
If the door stays open
It is not for you
```

## Hosted API: vocal song

The `prompt` below must remain at or below 2,000 characters and `lyrics` at or below 3,500 characters.

```json
{
  "model": "music-3.0",
  "prompt": "Alternative R&B / electronic soul at a slow late-pocket tempo. Guarded verses open into a quietly decisive final chorus. Close female alto, conversational and behind the beat, with a low unison hook double and small final-chorus harmony. Detuned electric piano, rounded sub-bass, dry rim clicks, and restrained counter-synth. The bridge drops drums and bass; the final chorus restores the groove and widens without festival synths. Intimate, low-lit mix with short dark plate reverb.",
  "lyrics": "[Verse]\nI left the hallway light on low\nLike you might still remember where to go\n\n[Pre Chorus]\nOne more hour, one less excuse\n\n[Chorus]\nIf the door stays open\nIt is not for you",
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "mp3"
  },
  "output_format": "url",
  "stream": false
}
```

## Hosted API: instrumental

```json
{
  "model": "music-3.0",
  "prompt": "Instrumental minimalist suspense cue at 78 BPM. Prepared-piano taps establish a five-note motif; bowed metal and low cello enter gradually while percussion remains absent. The middle section narrows to one dry pulse, then the final third adds muted frame drum and a rising viola counterline. No vocals, choir, heroic brass, trailer impacts, or stock risers. Close, tense mix with a short stone-room tail.",
  "is_instrumental": true,
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "wav"
  },
  "output_format": "url"
}
```

## Hosted Lyrics API

```json
{
  "mode": "write_full_song",
  "title": "Porch Light",
  "prompt": "Write an original plainspoken alternative R&B song in English. A person leaves the porch light on out of habit, then decides before dawn to switch it off. Intimate first person, concrete household details, no fire/shadows/echoes imagery, concise repeatable chorus, natural conversational stress."
}
```

Use `mode: edit` and supply `lyrics` when the user asks for continuation or targeted rewriting.

## SGLang-Omni: 30-second audition

At 25 frames per second, `750` caps the render at 30 seconds.

```json
{
  "model": "MiniMaxAI/MiniMax-Music3",
  "input": "[Verse]\nI left the hallway light on low\nLike you might still remember where to go\n[Chorus]\nIf the door stays open\nIt is not for you",
  "instructions": "Alternative R&B / electronic soul at a slow late-pocket tempo. Close female alto, conversational verses, restrained open-vowel chorus. Detuned electric piano, rounded sub-bass, dry rim clicks, no glossy stacks. Narrow intimate verse opens modestly in the chorus.",
  "response_format": "wav",
  "seed": 7,
  "max_new_tokens": 750,
  "stream": false
}
```

Command wrapper:

```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H 'Content-Type: application/json' \
  --data @request.json \
  --output audition.wav
```

## SGLang-Omni: instrumental placeholder

```json
{
  "model": "MiniMaxAI/MiniMax-Music3",
  "input": "[Intro]\n(instrumental)",
  "instructions": "Instrumental ambient cue, no lead or backing vocals. Warm analog pads, a distant felt-piano motif, and slowly changing low strings at 70 BPM. No drums; sparse, dark, and spacious.",
  "response_format": "wav",
  "seed": 3,
  "max_new_tokens": 250,
  "stream": false
}
```

## Diffusers

```python
import soundfile as sf
import torch
from diffusers import ModularPipeline

pipe = ModularPipeline.from_pretrained("MiniMaxAI/MiniMax-Music3")
pipe.load_components(dtype=torch.bfloat16)
pipe.to("cuda")

caption = """Global Metadata: Alternative R&B / electronic soul at a slow late-pocket tempo, intimate and nocturnal, opening into a restrained final release.
Vocal Details: Close female alto, conversational verses, low hook double, small final-chorus harmony, subtle tuning and short dark plate.
Arrangement: Detuned electric piano opens alone; muted sub-bass and rim clicks enter in the verse. The pre-chorus removes percussion. The chorus restores a deep kick and opens the stereo field. The bridge drops drums and bass; the final chorus returns the groove with one high counterline."""

lyrics = """[Verse]
I left the hallway light on low
Like you might still remember where to go
[Chorus]
If the door stays open
It is not for you"""

audio = pipe(
    prompt=caption,
    lyrics=lyrics,
    audio_duration=30.0,
    generator=torch.Generator("cuda").manual_seed(7),
    output="audios",
)[0]

sf.write(
    "audition.wav",
    audio.T.float().cpu().numpy(),
    pipe.sampling_rate,
)
```

## Native ComfyUI handoff

Provide four separate copy-ready values:

Caption:

```text
### Global Metadata
...

### Vocal Details
...

### Arrangement
...
```

Lyrics:

```text
[Verse]
...

[Chorus]
...
```

Settings:

```text
max_duration: 60
seed: 7
tiled_decode: false
```

Keep model download and workflow setup notes outside the field blocks.

## Failure repair examples

### Tag-line loss

Bad:

```text
[Chorus] Take me home before the morning
```

Fixed:

```text
[Chorus]
Take me home before the morning
```

### Static arrangement

Bad:

```text
Piano, strings, drums, bass, guitar, emotional vocals throughout.
```

Fixed:

```text
The Verse keeps dry piano and bass only. The Pre-Chorus removes bass and raises
a string tremolo. The Chorus restores bass, adds drums, and lets guitar answer
the vocal; guitar exits after the chorus. The Bridge returns to piano alone.
```

### Hosted field leakage

Bad hosted payload fields:

```json
{
  "instructions": "...",
  "input": "...",
  "seed": 7,
  "max_new_tokens": 750
}
```

Fixed hosted payload fields:

```json
{
  "model": "music-3.0",
  "prompt": "...",
  "lyrics": "..."
}
```
