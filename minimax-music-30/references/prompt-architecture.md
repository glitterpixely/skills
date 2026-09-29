# Prompt architecture

Use this reference for creative construction, surface-safe tag syntax, and prompt repair. The official MiniMax caption library is the primary stylistic authority; this file explains how to use it without confusing Caption, Lyrics, and runtime settings.

## The two-channel contract

Music 3.0 receives two complementary conditions:

```text
Caption -> how the music should sound and change
Lyrics  -> what is sung and where major song sections occur
```

Do not duplicate full lyrics in the Caption. Do not turn the Lyrics field into a production brief. If a section needs a specific musical change, keep the tag and words in Lyrics, then describe the change under the matching section in the Caption's Arrangement.

## Portable section tags

These tags appear across MiniMax's open model materials and are the safest portable core:

```text
[Intro]
[Verse]
[Pre-Chorus]
[Chorus]
[Bridge]
[Solo]
[Instrumental]
[Outro]
```

Put each tag alone on its line:

```text
[Verse]
First lyric line
Second lyric line
```

Never do this for a local open-weight request:

```text
[Verse] First lyric line
```

SGLang/Diffusers normalization drops text on the tag line without warning.

## Surface-specific tag inventory

The sources disagree slightly. Use exact spellings only when targeting that surface.

### Hosted music generation endpoint

Documented tags:

```text
[Intro] [Verse] [Pre Chorus] [Chorus] [Interlude] [Bridge]
[Outro] [Post Chorus] [Transition] [Break] [Hook] [Build Up]
[Inst] [Solo]
```

### Hosted lyrics-generation response

Documented tags:

```text
[Intro] [Verse] [Pre-Chorus] [Chorus] [Hook] [Drop] [Bridge]
[Solo] [Build-up] [Instrumental] [Breakdown] [Break]
[Interlude] [Outro]
```

### Open checkpoint and provider caption skill

Commonly shown tags:

```text
[Intro] [Verse] [Pre-Chorus] [Chorus] [Post-Chorus]
[Bridge] [Instrumental] [Solo] [Outro]
```

Do not claim the union is guaranteed everywhere. When portability matters, stay with the portable core.

## Lyrics design

### Match density to duration

Estimate the space available before drafting. A frame or duration cap is not a promise that every supplied word will be sung.

- short audition: one short verse and hook, or one hook plus instrumental context
- 30–60 seconds: one to three compact sections
- 1–2 minutes: abbreviated song form with one clear turn
- full song: use repetition strategically; do not fill every second with new words

Prefer breathing room over cramming. Dense lyrics increase skipped words, awkward stresses, unclear diction, and rushed form.

### Write for a voice

- Favor concrete images and active verbs.
- Keep a consistent point of view and tense.
- Use conversational word order unless a deliberate formal style is requested.
- Place open vowels and important words at likely sustained notes in the hook.
- Vary line length deliberately, but keep the hook's stress pattern repeatable.
- Use internal rhyme and consonance as texture; avoid forcing every line into perfect end rhyme.
- Give rap or sing-rap an explicit cadence and density in Vocal Details rather than over-punctuating lyrics.
- Keep ad-libs brief and performable, such as `(oh)` or `(stay)`. Do not use parentheses for long production directions.

### Structural economy

Every section needs a different job:

- `Intro`: establish palette or motif; avoid spending the main payoff
- `Verse`: advance images, situation, or argument
- `Pre-Chorus`: tighten rhythm, harmony, or lyrical tension
- `Chorus`: deliver the shortest, clearest promise and title-level phrase
- `Bridge`: change perspective, harmony, rhythm, or instrumentation
- `Solo` / `Instrumental`: release lyrical density and feature a named musical voice
- `Outro`: resolve, strip down, reprise, or deliberately leave tension

Repeating the same Chorus text can improve hook continuity. If the final chorus must differ musically, say so in Arrangement rather than rewriting words merely to signal more energy.

## Structured Caption anatomy

The three headings are an authoring contract, not JSON keys. Write precise prose beneath them.

### Global Metadata

Prioritize:

1. primary genre and at most one or two compatible modifiers
2. tempo or groove
3. emotional trajectory, not just a static mood
4. use case only when it influences composition or mix
5. production era, density, dynamics, and spatial finish

Useful pattern:

```text
<primary genre> / <modifier>, <tempo>. <emotional start> grows toward
<payoff>, with <core palette> and a <production character> mix.
```

Use exact BPM when supplied, musically important, or needed for sync. Otherwise choose a narrow range or qualitative tempo. Use exact key or scale only when the user has a harmonic reason; it is generative control, not guaranteed notation.

### Vocal Details

Specify only audible properties:

- number and role of lead vocalists
- gender presentation only when requested or musically necessary
- register and timbre
- articulation, phrasing, rhythmic placement, breath, vibrato, falsetto, belt, rasp, or rap delivery
- when harmonies, doubles, call-and-response, or backing vocals appear
- restrained use of tuning, delay, saturation, distortion, filtering, or reverb

Avoid celebrity names, vague `beautiful voice`, contradictory registers, and every technique at once.

For instrumental music, say:

```text
Instrumental; no lead or backing vocals. <instrument> carries the lead melody,
with <secondary texture> answering only in the larger sections.
```

### Arrangement

Write chronological cause and effect. Name the section, foreground, support, groove, transition, and energy change.

Weak:

```text
Guitars, drums, synths, strings, huge cinematic energy.
```

Strong:

```text
The Intro isolates a filtered guitar pulse. The Verse adds dry kick and bass
while keeping the stereo field narrow. The Pre-Chorus removes the kick and
raises a string ostinato. The Chorus restores full drums, opens doubled guitars,
and moves the lead vocal forward; the final chorus adds a high counterline but
does not introduce another rhythm section.
```

Track these lifecycles:

- primary harmonic or riff instrument
- lead melodic voice
- bass role and register
- kick, snare, hats, percussion, and groove changes
- supporting pads, strings, brass, guitars, keys, or ornaments
- backing vocals and harmonies
- width, depth, filtering, reverb, delay, saturation, and compression changes

Keep transitions plausible. A section can change through addition, removal, register, rhythm, articulation, dynamics, harmony, space, or timbre; it does not need a new instrument every time.

## Use the official caption library

The vendored library contains 1,000 provider-authored complete caption references. Use it through progressive disclosure:

1. Read `genre-router.md`.
2. Read one family index; read a second only for a genuine fusion.
3. Pick up to three cards:
   - `Foundation`: genre, groove, and songwriting language
   - `Modifier`: a specific secondary palette, cultural color, vocal treatment, or production trait
   - `Arrangement`: energy curve and instrument lifecycle
4. Open only those complete template files.
5. Extract principles, then write original prose.

Do not scan all filenames or treat frequency as a recommendation. Do not copy a sentence, exact key, BPM, vocalist, instrument stack, story, or section order merely because a template contains it.

## Prompt precedence

Resolve conflicts in this order:

1. explicit user requirements and exclusions
2. section-local user directions
3. hard surface limits
4. strong musical implications of the brief
5. compatible provider template traits
6. conservative defaults

If two explicit constraints cannot coexist, state the conflict outside the provider fields and make the smallest reversible compromise only when the user's intent is still clear.

## Hosted caption compression

The hosted API accepts at most 2,000 characters in `prompt`, while the official caption skill defaults to 250–450 English words. Validate characters, not words.

Compress in this order:

1. remove redundant adjectives and restated genre labels
2. merge production and spatial phrases
3. keep only section changes that materially affect the arc
4. retain vocal identity and the core instrument lifecycle
5. retain explicit exclusions
6. remove key before BPM if neither was user-supplied

Preserve the three logical layers even if rendered as three compact paragraphs.

## Repair hierarchy

Inspect the result against the intended contract:

1. **Lyrics ingestion**: missing line, broken tag, excessive word density
2. **Global identity**: wrong genre, groove, era, or mood
3. **Vocal identity**: wrong register, timbre, delivery, harmony, or effects
4. **Section development**: static dynamics or wrong entrances/exits
5. **Production**: masking, harshness, narrowness, excessive effects, or weak low end
6. **Runtime cap**: truncation, early model ending, or wrong output setting
7. **Sampling variation**: only after the contract is correct, compare seeds

Change one layer per controlled iteration. Preserve the original seed on seeded local surfaces until the prompt change is evaluated.

## Anti-patterns

- keyword soup without an emotional or arrangement arc
- contradictory production, such as `raw live room` plus `hyper-quantized sterile perfection`, without intentional contrast
- listing every instrument as a constant full-song layer
- using negative prompts as the main description
- embedding duration, seed, or file format in caption prose when the surface has dedicated controls
- asking for `the exact voice of` a real singer
- passing an artist name as a substitute for musical analysis
- using a caption template verbatim
- assuming a precise key or BPM will be obeyed exactly
- conflating `Instrumental` lyric tags with the hosted `is_instrumental` request flag
