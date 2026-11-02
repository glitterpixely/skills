# Songcraft and originality guide

Use this reference to turn a request or source track into a complete song design before writing provider fields.

## Contents

- [Intake and useful defaults](#intake-and-useful-defaults)
- [Build an appeal map](#build-an-appeal-map)
- [Opt-in parody and lyric adaptation](#opt-in-parody-and-lyric-adaptation)
- [Write the creative thesis](#write-the-creative-thesis)
- [Design the musical engine](#design-the-musical-engine)
- [Write vocal songs](#write-vocal-songs)
- [Phonetic and pronunciation hygiene for AI singers](#phonetic-and-pronunciation-hygiene-for-ai-singers)
- [Write instrumental and film cues](#write-instrumental-and-film-cues)
- [Construct the Style field](#construct-the-style-field)
- [Construct the Exclude field](#construct-the-exclude-field)
- [Generate distinct directions](#generate-distinct-directions)
- [Iterate and diagnose](#iterate-and-diagnose)
- [Quality gate](#quality-gate)

## Intake and useful defaults

Capture what the user already supplied:

- purpose: release, film, trailer, social clip, character theme, parody/adaptation, demo, or experiment;
- vocal state: instrumental, solo, duet, group, choir, spoken, or mixed;
- language and point of view;
- duration and any edit length;
- emotional beginning, turn, and ending;
- genre lane and compatible contrast;
- reference material and what the user likes about it;
- required sounds, prohibited sounds, literal text, or structural constraints.

If unspecified, prefer these defaults:

- full song: 2:40–3:20;
- short-film music: a complete 2:30–3:15 cue containing a dedicated 40–60 second hero passage;
- one primary genre lane plus one compatible contrast;
- one signature motif or sound rule;
- three or more clearly different energy states;
- a new central concept rather than a paraphrase of the reference (unless the user explicitly requested a parody or lyric adaptation).

## Build an appeal map

When translating a reference track into an **original song** (the default), analyze the reference without copying its identity. Record observations under these headings:

| Dimension | Extract | Do not carry over directly |
|---|---|---|
| Function | dance, confession, duel, montage, suspense | the same story or branded world |
| Energy | density curve, silence, release timing | identical section timestamps |
| Rhythm | pocket, swing, subdivision, acceleration | signature beat pattern |
| Harmony | brightness, tension, pedal behavior | recognizable progression or voicing sequence |
| Melody | range, density, call-and-response | contour, intervals, cadence, or hook |
| Ensemble | acoustic/electronic balance, role exchange | the same signature instrument combination and roles |
| Vocal | register, intimacy, attack, group mechanics | voice imitation, phrasing, or ad-libs |
| Form | through-composed, refrain-led, episodic | identical section order and payoff placement |
| Production | dry/wide, live/programmed, rough/polished | distinctive source effects or mix fingerprint |

Then write an originality delta. Change at least five of:

1. central premise and title;
2. hook wording and phonetic shape;
3. melodic contour and cadence;
4. harmonic engine;
5. groove or meter feel;
6. section order and lengths;
7. lead instrument and counter-voice;
8. signature sound event;
9. recording space and stereo movement;
10. emotional resolution.

For a famous or strongly recognizable reference, change at least seven. Preserve only broad functional appeal.

## Opt-in parody and lyric adaptation

Use this mode **only** when the user explicitly asks for a parody, comedic rewrite, or lyric adaptation of an existing song structure. Never use it for original-song requests.

1. **Map the structural skeleton first**:
   - Count syllables per line and mark the rhyme scheme (`ABAB`, `AABB`, `ABCB`).
   - Mark the **stressed beats** in every line (stressed syllables govern singability more than raw syllable count; unstressed pickups can flex by 1–2 syllables).
   - Note where long held/sustained notes land.
2. **Fit new words to the prosodic skeleton**:
   - Lock stressed syllables to the exact same musical beats as the source skeleton.
   - Match the **open vowel family** on long held notes (e.g., if the sustained note sits on an `oo` or `oh` vowel, choose a target word with the same open vowel shape rather than a clipped consonant-closed vowel).
   - Use **monosyllabic word swaps** at hook anchors to preserve rhythmic punch while flipping the meaning.
   - Use the bridge slot to pivot or escalate the comedic/thematic premise while preserving the section's emotional function.
3. **Keep `Style` moderation-safe**:
   - Even in a parody, **never** put the original artist name or copyrighted song title into Suno's `Style` field. Translate the backing arrangement into the 6-Stage Studio Signal Chain (`Era & Subgenre`, `Exact BPM`, `Core Hardware/Acoustic Timbres`, `Vocal Delivery`, `Scene & Mood`, `Mix & Master`).

## Write the creative thesis

Use this pattern:

`A [function] about [specific premise], moving from [state A] to [state B], identified by [audible signature rule].`

Good signature rules are relational or structural:

- the bass carries the hook while the voice avoids it;
- cymbals appear only in the final section;
- every return of a five-note motif omits a different note;
- the chorus becomes smaller instead of larger;
- a dry household sound becomes the percussion identity;
- lead and counterline never play simultaneously until the ending.

Avoid generic claims such as “unique,” “powerful,” “cinematic,” or “emotional” without an audible mechanism.

## Design the musical engine

Specify audible decisions in this order:

1. musical lane and emotional color;
2. tempo, meter feel, and pocket;
3. harmonic behavior;
4. primary motif or hook mechanics;
5. instrument roles and playing techniques;
6. vocal register, distance, and delivery when applicable;
7. section-by-section additions and removals;
8. recording space, dynamics, and mix behavior;
9. one signature constraint.

Prefer relationships over inventories. Write “muted guitar answers the last word of each line” rather than “guitar.” Write “drums vanish before the refrain” rather than “dynamic drums.”

Treat exact BPM, key, chord symbols, bar counts, and unusual meters as requests. If precision matters, have the user play, program, hum, or tap the behavior and use the owned recording as an audio seed.

## Write vocal songs

### Establish the premise

- Give the narrator a concrete situation, desire, obstacle, and decision.
- Use specific physical evidence, actions, places, objects, contradictions, and consequences (“your hoodie's still on the hook by the door” rather than “I was sad”).
- Replace default abstraction clusters such as fire, shadows, echoes, scars, chains, destiny, rising, and breaking free unless the brief makes one of them materially specific.
- Make the title do conceptual work; do not merely repeat the genre or mood.

### Build the hook

- Make it understandable after one listen.
- Use a distinct rhythmic or syntactic shape.
- Favor open, sustainable vowels (`ah`, `oh`, `ay`, `oo`) on long notes.
- Repeat deliberately, then change one word or implication.
- Avoid reproducing a reference hook's syllable count, rhyme position, melodic contour, or call-and-response pattern (unless in explicit Parody/Adaptation mode).

### Check prosody, rhyme, and meter

- Speak every line aloud; if the tongue stumbles, cut unstressed filler words.
- Align natural word stress with musical accents. Keep parallel verse lines matched in **stressed-beat count** without forcing unnatural word inversions (“Yoda-speak”) just to hit an end rhyme.
- Blend rhyme types intentionally:
  - **Perfect rhyme** (`lean / mean`) for settled closure, punchlines, or anthemic hooks;
  - **Family rhyme** (`crate / braid`), **assonance** (`had / glass`), **consonance** (`scene / when`), or **slant rhyme** for unresolved tension, longing, or conversational realism;
  - **Internal rhyme** within lines to build forward momentum without nursery-rhyme stiffness.
- Put breath points at meaningful line breaks.

### Use section labels simply

Use familiar labels and short action-oriented cues on their own standalone lines:

```text
[Cold Open | dry single voice]

[Verse 1 | bass enters on line three]

[Refrain | drums drop out]

[Instrumental Interlude | lead instrument carries the hook]

[Final Refrain | half length]

[End]
```

Do not overload every section with several contradictory metatags (e.g., never combine `[Calm]` and `[Aggressive]` in the same section, and avoid stacking more than 1–2 concise cues on a section header).

## Phonetic and pronunciation hygiene for AI singers

AI vocal models pronounce phonetically rather than reading semantic intent. Apply these checks to `Lyrics` before delivery:

1. **Numbers and symbols**: Always spell numbers and symbols out as sung words to lock syllable count and rhythm (`twenty four seven` instead of `24/7`, `nineteen ninety-nine` instead of `1999`, `percent` instead of `%`).
2. **Acronyms and initialisms**: Space or hyphenate letters that should be spelled out (`A-I` or `A I` instead of `AI`, `N-Y-C` instead of `NYC`) unless pronounced as a single word (`NASA`).
3. **Homographs and unusual proper nouns**: Spell tricky proper nouns or ambiguous words phonetically (`thru` when a clean monosyllable is needed; hyphenate multi-syllable technical words like `re-search` or `bi-o-en-gi-neer-ing` to guide syllable stress). When a song relies on an unusual proper noun, test pronunciation in a quick `v6-mini` sketch before spending `Max Mode` credits.
4. **Restrained delivery punctuation**:
   - **Sustained melisma**: Extend the stressed vowel with hyphens (`lo-o-o-ove`, `sta-a-ay`) sparingly on climax notes.
   - **Dramatic pause**: Use ellipses (`I... need... you`) for audible breath/hesitation inside a phrase.
   - **Belted emphasis**: Use `ALL CAPS` sparingly on a peak phrase (`LET IT BURN`) to cue higher vocal intensity.

## Write instrumental and film cues

Replace lyrical form with dramatic states:

1. establish a motif or texture;
2. introduce motion or threat;
3. create contrast through subtraction;
4. reserve the densest passage for the visual or emotional pivot;
5. include clean edit points, dropouts, or tails;
6. resolve, fracture, or deliberately withhold resolution.

For a short visual, avoid asking the model to compress an entire conventional song into the clip length. Generate a full cue with a dedicated hero passage, then edit the strongest sequence to picture.

Useful non-default forms include through-composed episodes, AABA, refrain-at-end-of-verse, instrumental hook instead of a second chorus, bridge by subtraction, shortened final refrain, and false ending followed by one dry line or motif.

## Construct the Style field

Choose the `Style` construction mode that matches the task:

### Mode A: 6-Stage Studio Signal Chain (fast prompts, genre archetypes, & tight production lock)
See [`studio-signal-chain-and-archetypes.md`](studio-signal-chain-and-archetypes.md) for the full 83-archetype catalog and hardware lexicon:

```text
[01. Era & Subgenre], [02. Exact BPM], [03. Core Timbres (specific amps, synths, acoustic models)], [04. Vocal Delivery (register, mic distance, texture)], [05. Scene & Mood (emotional arc & setting)], [06. Mix & Master (reverb space, console/tape warmth, stereo imaging)]
```

### Mode B: 8-Part Relational Studio Architecture (picture scoring, reference translation, & custom dynamic arcs)

```text
[1. Function & duration]. [2. Primary musical lane + 1 contrast]. [3. BPM, meter feel, & groove pocket]. [4. Harmonic engine]. [5. Lead, counter-voice, rhythm, & bass roles]. [6. Vocal register, distance, & delivery]. [7. Section energy arc across >=3 states including subtraction]. [8. Recording space, mix finish, & 1 signature rule].
```

Keep every phrase audible, positive-only, and mutually compatible. Remove decorative adjectives and redundant genre labels.

## Construct the Exclude field

List only unwanted audible elements, styles, vocal qualities, or production traits. Examples:

```text
choir, heroic brass fanfare, stock risers, trap hi-hat rolls, supersaws, four-chord pop loop, constant percussion, excessive reverb, hard tuning, over-bright compressed master
```

Do not put the main creative brief or abstract instructions such as “do not be generic” in Exclude.

## Generate distinct directions

For multiple songs, vary all six anchors:

| Anchor | Examples |
|---|---|
| Premise | confession, bargain, ritual, misdirection, physical task |
| Hook | chant, long-vowel line, clipped question, instrumental motif, response chain |
| Groove | late pocket, straight motorik, swung sixteenths, half-time march, free pulse |
| Harmony | pedal tension, modal vamp, descending bass, shifting dyads, chromatic planing |
| Lead identity | breath, bowed metal, prepared piano, plucked strings, found percussion |
| Form | refrain-led, through-composed, AABA, false ending, chorus by subtraction |

Reject batches that vary only title, costume-like imagery, color, or one instrument.

## Iterate and diagnose

Separate exploration from convergence:

- exploration: seek a distinctive motif, form, or performance; allow more variation;
- convergence: preserve an owned seed and strengthen adherence;
- change one variable per A/B batch;
- choose composition before polish;
- preserve the strongest section and replace only failures (using v6 natural-language section/lyric editing or Song Editor);
- rebuild a defining part with an owned recording, instrument, sample, or MIDI performance;
- remaster only after composition and performance are locked.

Classify problems before revising:

| Symptom | Likely cause | Revision |
|---|---|---|
| Generic but clean | default form or harmonic loop | change form, hook carrier, or harmonic engine |
| Big all the time | additive arrangement | specify subtraction, silence, and narrow-to-wide movement |
| Lyrics feel AI-written | abstraction and forced rhyme | add physical evidence, decision, and natural stress |
| Mispronounced word or number | raw digits, acronyms, or homographs | spell out numbers, space acronyms (`A-I`), or respell phonetically in `Lyrics` |
| Vocal feels synthetic | delivery and source identity | use close-mic/ribbon-mic studio descriptors, an owned voice seed, or re-record the lead |
| Instruments feel fake | exposed generated timbre | anchor `Style` with specific hardware/amp/mic models (`Fender Rhodes Mark I`, `Juno-106`, `ribbon-mic`) or replace the stem |
| Prompt ignored | overload or contradiction | switch to the concise 6-Stage Studio Signal Chain and remove conflicting cues |
| Good song, weak passage | local generation failure | use v6 natural-language editing or Song Editor to replace that section, not the whole song |
| Polished but forgettable | no signature mechanism | impose one motif, sound, or structural rule |

## Quality gate

Before delivery, verify that:

- the title, concept, hook, and imagery are not paraphrases of a reference (unless in explicit Parody/Adaptation mode);
- the prompt contains no artist, producer, or source-title name;
- required runtime, BPM, vocal setup, language, and structure are explicit when requested;
- numbers and acronyms in `Lyrics` are formatted for natural vocal pronunciation;
- every instrument has a clear role or specific acoustic/hardware identity;
- at least three energy states (or a clear dynamic arc) are audible in the plan;
- each song in a batch has a different governing musical engine;
- settings are labeled as official controls versus practical heuristics;
- copy-ready fields contain no explanatory prose;
- no uniqueness, rights, or audio-quality claim exceeds the available evidence.
