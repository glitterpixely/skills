# Studio Signal Chain & 83 Sonic Archetypes Reference

Use this reference to engineer high-fidelity, copy-ready Suno `Style` strings using concrete studio signal-chain descriptors (specific synth topologies, amplifier models, microphone placements, console saturation, and reverb spaces) without relying on living artist or producer names.

## Contents

- [The 6-Stage Studio Signal Chain](#the-6-stage-studio-signal-chain)
- [Studio Hardware & Acoustic Lexicon](#studio-hardware--acoustic-lexicon)
- [Suite 01: Pop, R&B, Synth-Pop & Contemporary Vocal Production (#01–#15 • 72–134 BPM)](#suite-01-pop-rb-synth-pop--contemporary-vocal-production-0115--72134-bpm)
- [Suite 02: Hip-Hop, Boom-Bap, Melodic Trap & Tropical Grooves (#16–#27 • 85–150 BPM)](#suite-02-hip-hop-boom-bap-melodic-trap--tropical-grooves-1627--85150-bpm)
- [Suite 03A: Rock, Alternative, Grunge, Punk & Indie Guitar Styles Part I (#28–#37 • 94–148 BPM)](#suite-03a-rock-alternative-grunge-punk--indie-guitar-styles-part-i-2837--94148-bpm)
- [Suite 03B: Blues, Post-Punk, Math-Rock, Stoner & Space Rock Part II (#38–#46 • 84–144 BPM)](#suite-03b-blues-post-punk-math-rock-stoner--space-rock-part-ii-3846--84144-bpm)
- [Suite 04: Electronic, Synthwave, Techno, Club, IDM & Ambient Synthesis (#47–#66 • 68–174 BPM)](#suite-04-electronic-synthwave-techno-club-idm--ambient-synthesis-4766--68174-bpm)
- [Suite 05: Jazz, Bossa Nova, Folk, Bluegrass, Reggae & Western Cinema (#67–#76 • 72–136 BPM)](#suite-05-jazz-bossa-nova-folk-bluegrass-reggae--western-cinema-6776--72136-bpm)
- [Suite 06: Gothic Chamber Folk, Festive & East-Asian Traditional Hybrids (#77–#83 • 76–130 BPM)](#suite-06-gothic-chamber-folk-festive--east-asian-traditional-hybrids-7783--76130-bpm)

---

## The 6-Stage Studio Signal Chain

When the user wants a fast, genre-accurate `Style` prompt or an acoustically grounded sonic archetype, assemble a comma-separated studio chain following these 6 stages in order:

| Stage | Slot | Acoustic Function | Example Descriptors |
| --- | --- | --- | --- |
| **01** | **Era & Subgenre** | Anchors harmonic rules and rhythm feel | `Dreamy 80s synth-pop`, `90s grunge rock`, `Vintage 60s bossa nova`, `Contemporary R&B pop fusion` |
| **02** | **Exact Tempo** | Locks groove pocket and transient speed | `75BPM` (Slow `<90`), `104BPM` (Mid `90–115`), `126BPM` (Upbeat `116–135`), `174BPM` (Fast `136+`) |
| **03** | **Core Timbres** | Names specific amps, synths, and acoustic models | `vintage Juno-106 poly-synths`, `Fender Rhodes Mark I chords`, `dusty E-mu SP-1200 punchy drum breaks`, `Marshall JCM800 guitar riffs` |
| **04** | **Vocal Delivery** | Sets register, mic distance, and vocal texture | `intimate breathy female vocal`, `tender whisper-close vocal`, `deadpan detached baritone vocal`, `smoky sultry female jazz contralto` |
| **05** | **Scene & Mood** | Shapes the emotional arc and cinematic setting | `dramatic slow-burn crescendo`, `quiet-verse to explosive-chorus dynamics`, `rain-streaked midnight detective cinema atmosphere` |
| **06** | **Mix & Master** | Defines reverb space, tape warmth, and stereo imaging | `spacious Lexicon hall reverb`, `warm SSL analog console bus compression`, `uncompressed ambient room-mic studio production`, `tight sub-bass mono control` |

### Tempo Bands
- **Slow (`<90 BPM`)**: Torch ballads, noir jazz, beatless ambient drones, slowcore, sad rap, gothic chamber folk (`68–89 BPM`).
- **Mid (`90–115 BPM`)**: Boom-bap, neo-soul, R&B, bedroom lo-fi, G-funk, blues shuffle, bossa nova, shoegaze, chillwave (`90–115 BPM`).
- **Upbeat (`116–135 BPM`)**: Commercial pop, club dance-pop, deep/melodic house, techno, synthwave, grunge, arena hard rock, math-rock (`116–135 BPM`).
- **Fast (`136+ BPM`)**: Folk-punk, skate punk, two-tone ska, horrorcore trap, breakbeat jungle, liquid drum & bass (`136–174 BPM`).

---

## Studio Hardware & Acoustic Lexicon

Use these moderation-safe acoustic and hardware descriptors to replace generic instrument nouns or prohibited artist/producer references:

- **Keyboards & Synths**: `close-mic felt piano`, `Steinway concert grand piano`, `upright tack piano`, `Fender Rhodes Mark I electric piano`, `Wurlitzer 200A reed piano`, `Korg M1 house piano chords`, `Hammond B3 organ with Leslie rotary speaker`, `Juno-106 chorus poly-synths`, `Oberheim brassy analog synth leads`, `Minimoog squelchy synth bass`, `Moog ladder-filter arpeggio`, `TB-303 resonant acid squelch`, `Buchla & granular modular synth drones`, `layered supersaw synths`.
- **Guitars & Amps**: `finger-picked parlor acoustic guitar`, `strummed dreadnought acoustic`, `syncopated nylon-string classical guitar`, `clean reverberant Telecaster arpeggios`, `crunchy Les Paul boogie riffs`, `clean jazz-inflected semi-hollow guitar leads`, `overdriven Fender Bassman tube-amp licks`, `crunchy Marshall JCM800 guitar riffs`, `heavy drop-D Big Muff distorted guitars`, `mammoth C-standard Orange-amp fuzz guitars`, `glide-guitar reverse reverb & fuzz`, `twangy spring-reverb tremolo baritone guitar`.
- **Drums, Samplers & Bass**: `dusty E-mu SP-1200 punchy drum breaks`, `MPC60 swung boom-bap drums`, `gated-reverb LinnDrum snare`, `TR-808 booming distorted bass glides`, `TR-909 crisp open hi-hats & driving four-on-the-floor kick`, `fast rolling Amen breakbeats`, `warm Reese sub-bass`, `punchy sidechained sub-bassline`, `thick envelope-filter slap bassline`, `melodic driving high-register chorused pick-bass`, `walking upright double bass`, `brushed snare & floor-tom pulse`, `plodding heavy triplet-groove cavern drums`.
- **World, Folk & Orchestral Timbres**: `three-finger banjo rolls`, `flatpicked Martin acoustic guitar`, `mournful Gaelic fiddle`, `airy penny tin whistle`, `Celtic bodhran frame drum`, `Nordic bowed lyre`, `delicate plucked guzheng zither`, `meditative seven-string guqin`, `expressive bamboo dizi flute`, `virtuosic weeping erhu fiddle`, `rapid pipa lute tremolos`, `high-velocity tsugaru shamisen`, `thunderous taiko war drums`, `Harmon-muted cool-jazz trumpet`, `wooden marimba & kalimba`, `island steelpan percussion`.
- **Mics, Consoles & Spatial Mix**: `unadorned ribbon-mic studio fidelity`, `warm tube-mic vocal booth`, `dry single-mic ensemble blend`, `uncompressed ambient room-mic studio production`, `warm SSL analog console bus compression`, `vintage Trident console warmth`, `1960s warm valve-console analog mix`, `soft cassette tape saturation`, `analog tape flutter`, `spacious Lexicon hall reverb`, `lush plate reverb`, `analog spring reverb & tape delay`, `austere gated drum reverb`, `endless cathedral shimmer decay`, `hyper-detailed binaural panning`, `mono-centered low end`.

---

## Suite 01: Pop, R&B, Synth-Pop & Contemporary Vocal Production (#01–#15 • 72–134 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **01** | **Modern Sentimental Pop** (*Heartbreak Radio Ballad*) | `98 BPM` | `Modern sentimental pop, 98BPM, warm close-mic felt piano, subtle evolving analog synth pads, intimate breathy female vocal, heartfelt soaring chorus hook, emotional breakup atmosphere, lush plate reverb, crisp radio-ready studio master` |
| **02** | **Upbeat Sunny Pop** (*Daylight Commercial*) | `122 BPM` | `Upbeat sunny commercial pop, 122BPM, bright double-tracked acoustic guitar, snappy tight pocket drums, charismatic light male vocal, infectious earworm chorus, carefree youthful spirit, glossy wide top-40 stereo mix` |
| **03** | **Dreamy 80s Synth-Pop** (*Nostalgic Midnight Wave*) | `110 BPM` | `Dreamy 80s synth-pop, 110BPM, vintage Juno-106 poly-synths, shimmering 16th-note arpeggios, ethereal female vocal, hazy nostalgic midnight mood, spacious Lexicon hall reverb, warm analog chorus modulation` |
| **04** | **Dark Cinematic Ballad** (*Widescreen Power Vocal*) | `75 BPM` | `Dark emotional pop ballad, 75BPM, resonant concert grand piano, sweeping chamber string layers, powerhouse belting female vocal, dramatic slow-burn crescendo, deep sorrow, widescreen film-score dynamic range` |
| **05** | **Intimate Bedroom Lo-Fi** (*Tape-Saturated Indie Pop*) | `92 BPM` | `Lo-fi bedroom pop, 92BPM, muted low-pass drum machine beat, warm vinyl surface crackle, gentle husky male vocal, lazy unhurried pocket, cozy late-night intimacy, soft cassette tape saturation, dry close-room acoustics` |
| **06** | **Club Dance-Pop** (*Peak-Hour Floorfiller*) | `128 BPM` | `Energetic dance-pop, 128BPM, punchy sidechained sub-bassline, bright house piano & synth stabs, confident diva female vocal, driving four-on-the-floor kick, euphoric club-ready production, tight transient master` |
| **07** | **Indie Acoustic Soft Pop** (*Whispered Confessional*) | `104 BPM` | `Indie folk-pop, 104BPM, delicate finger-picked parlor acoustic guitar, light organic shaker percussion, tender whisper-close vocal, gentle autumn melancholy, raw unadorned ribbon-mic studio fidelity` |
| **08** | **Retro 90s Throwback** (*Classic New-Jack & Pop*) | `116 BPM` | `Retro 90s pop, 116BPM, classic Korg M1 house piano chords, swung 90s R&B drum machine, smooth expressive male vocal, nostalgic uplifting chorus, warm SSL analog console bus compression` |
| **09** | **Sad Dark Alt-Pop** (*3AM Insomnia Minimalism*) | `86 BPM` | `Sad dark alt-pop, 86BPM, subtle micro-glitch synth plucks, deep minimal sub-bass pulse, fragile breathy close-mic vocal, lonely late-night mood, dark binaural spatial atmosphere, haunting negative space` |
| **10** | **Stadium Anthem Pop** (*Massive Arena Chorus*) | `130 BPM` | `Stadium anthem pop, 130BPM, massive layered supersaw synths, thunderous reverberant tom drums, soaring powerhouse lead vocal, uplifting hopeful energy, giant crowd-chant chorus, wide festival stereo master` |
| **11** | **Bubblegum Kawaii Pop** (*Hyper-Bright Pastel*) | `134 BPM` | `Bubblegum cute pop, 134BPM, playful chiptune-tinged synth bells, bouncy syncopated drums, sweet high-pitched female vocal, bright innocent kawaii aesthetic, sparkling harmonic exciter polish, crisp punchy mix` |
| **12** | **Contemporary R&B Pop** (*Velvet Neo-Soul Groove*) | `100 BPM` | `Contemporary R&B pop fusion, 100BPM, lush Fender Rhodes Mark I chords, deep warm sub-bass, soulful melismatic female vocal, silky layered vocal harmonies, velvety late-night warmth, pristine modern R&B mix` |
| **13** | **Atmospheric Dream Pop** (*Cathedral Shimmer Haze*) | `96 BPM` | `Atmospheric dream pop, 96BPM, chorus-drenched shimmer-reverb guitars, floating airy pad swells, distant angelic vocals, foggy meditative slow-burning build, lush stereo modulation, immersive sonic halo` |
| **14** | **Slow-Burn Torch R&B** (*After-Hours Velvet Ballad*) | `72 BPM` | `Slow-burn neo-soul torch ballad, 72BPM, warm tremolo Wurlitzer 200A electric piano, deep fretless bass swells, intimate smoky alto vocal with close-mic breath detail, aching midnight confession mood, warm tube-preamp saturation, spacious chamber decay` |
| **15** | **Modern Nu-Disco Pop** (*Mirrorball Funk Boogie*) | `124 BPM` | `Modern nu-disco funk pop, 124BPM, crisp muted sixteenth-note Stratocaster rhythm guitar, octave-jumping analog slap bass, silky falsetto lead vocal with stacked disco harmonies, glittering rooftop party euphoria, tight sidechained SSL bus glue` |

---

## Suite 02: Hip-Hop, Boom-Bap, Melodic Trap & Tropical Grooves (#16–#27 • 85–150 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **16** | **Summer Tropical Pop** (*Sunlit Island Marimba*) | `120 BPM` | `Summer tropical pop, 120BPM, bright wooden marimba & kalimba melody, light island steelpan percussion, cheerful sun-kissed vocal, breezy beach vacation mood, warm golden-hour stereo imaging, crisp acoustic top-end` |
| **17** | **90s East Coast Boom-Bap** (*Golden-Era SP-1200 Grit*) | `96 BPM` | `Hard-hitting 90s boom-bap hip-hop, 96BPM, dusty E-mu SP-1200 punchy drum breaks, gritty vinyl soul sample chops, sharp authoritative male rap delivery, raw NYC underground basement grit, mono-centered low end` |
| **18** | **Melodic Emo Trap** (*Autotune 808 Heartache*) | `132 BPM` | `Melodic emo trap, 132BPM, melancholic bell-synth arpeggio, booming distorted 808 bass glides, crisp triplet hi-hat rolls, polished melodic pitch-corrected rap-singing, bittersweet nocturnal mix, wide vocal doubler` |
| **19** | **Dreamy Cloud Rap** (*Vaporous Ambient Trap*) | `110 BPM` | `Chill cloud rap, 110BPM, ethereal detuned floating pad chords, muted slow 808 sub-bass, distant reverb-drenched rap vocals, surreal dreamy fog aesthetic, spacious ambient trap soundstage, soft high-shelf roll-off` |
| **20** | **Conscious Storytelling** (*Lyrical Upright Piano*) | `94 BPM` | `Emotional conscious hip-hop, 94BPM, looping melancholic upright piano motif, light organic boom-bap drums, passionate articulate storytelling rap, reflective lyricism, intimate dry vocal booth mix, warm analog low-mids` |
| **21** | **Late-Night Jazz Hop** (*Smoky Rhodes & Brushes*) | `86 BPM` | `Jazzy lo-fi hip-hop, 86BPM, warm vintage Rhodes jazz piano sample, brushed snare drums, acoustic upright bass walk, smooth conversational rap flow, smoky midnight cafe ambiance, subtle vinyl warmth` |
| **22** | **Retro 90s West Coast** (*G-Funk Moog Cruiser*) | `105 BPM` | `Retro 90s G-funk hip-hop, 105BPM, fat Minimoog squelchy synth bass, high-pitched portamento sine-wave synth lead, laid-back West Coast rap cadence, sunny palm-tree boulevard groove, punchy analog mix` |
| **23** | **Dark Horrorcore Trap** (*Sinister Industrial 808*) | `150 BPM` | `Dark horrorcore hip-hop, 150BPM, eerie detuned music-box synths, heavily clipped blown-out 808 sub-bass, menacing low-register rap delivery, tense sinister psychological thriller atmosphere, aggressive limiting` |
| **24** | **Upbeat Club Party Rap** (*Triumphant Brass Bounce*) | `126 BPM` | `Upbeat party hip-hop, 126BPM, bouncy Southern club drum groove, triumphant stadium brass stabs, playful charismatic confident rap vocal, high-energy VIP club celebration vibe, punchy low-end master` |
| **25** | **Psychedelic Warp Rap** (*Kaleidoscopic Tape Pitch*) | `101 BPM` | `Psychedelic abstract hip-hop, 101BPM, swirling phaser-soaked synths, pitch-warped soul tape samples, slow meandering hypnotic rap flow, kaleidoscopic hallucinatory stereo panning, analog tape flutter` |
| **26** | **Minimal Sad Rap** (*Solitary Rain-Soaked*) | `85 BPM` | `Introspective sad hip-hop, 85BPM, sparse minimal minor-key felt piano notes, quiet rimshot drums, vulnerable spoken-word rap about solitude, somber rain-against-window foley texture, intimate dry vocal` |
| **27** | **Funky Live-Band Rap** (*Organic Wah-Guitar Pocket*) | `112 BPM` | `Funky live-instrument hip-hop, 112BPM, thick envelope-filter slap bassline, crisp wah-wah rhythm guitar chops, upbeat bouncy rap cadence, infectious feel-good block party energy, live studio room warmth` |

---

## Suite 03A: Rock, Alternative, Grunge, Punk & Indie Guitar Styles Part I (#28–#37 • 94–148 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **28** | **Indie Folk-Rock** (*Earnest Heartland Roots*) | `106 BPM` | `Indie folk-rock, 106BPM, blend of strummed dreadnought acoustic and gritty tube-driven electric guitars, steady driving drums, raspy emotional male vocal, raw earnest roots-rock energy, organic live-off-the-floor mix` |
| **29** | **90s Seattle Grunge** (*Sludgy Quiet-Loud Dynamic*) | `118 BPM` | `90s grunge rock, 118BPM, heavy drop-D Big Muff distorted guitars, crashing cavern drums, quiet-verse to explosive-chorus dynamics, strained angsty male vocal, raw uncompressed ambient room-mic studio production` |
| **30** | **Dreamy Shoegaze** (*Towering Wall of Fuzz*) | `94 BPM` | `Dreamy shoegaze rock, 94BPM, towering wall of glide-guitar reverse reverb & fuzz, buried ethereal vocals blended as instrument, slow drifting hypnotic pulse, immersive warm analog noise-pop blanket` |
| **31** | **Classic Arena Hard Rock** (*Marshall-Stack Riff Power*) | `124 BPM` | `Classic hard rock, 124BPM, crunchy Marshall JCM800 guitar riffs, punchy gated-room stadium drums, powerful gravelly male rock vocal, screaming guitar solo, anthemic highway rock punch, wide stereo double-tracked guitars` |
| **32** | **2000s Garage Rock Revival** (*Overdriven Twin-Amp Stomp*) | `132 BPM` | `Raw 2000s garage rock revival, 132BPM, biting overdriven Fender Twin combo guitars, driving eighth-note P-bass pulse, urgent distorted room-mic male vocal, sweaty basement club intensity, zero-polish analog tape slapback` |
| **33** | **Anthemic Pop-Punk** (*Dual-Rectifier Power Chords*) | `142 BPM` | `High-energy melodic pop-punk, 142BPM, tight palm-muted Mesa Dual-Rectifier power chords, rapid punk snare rolls, nasal youthfully urgent tenor vocal with gang-shout hooks, rebellious suburban summer drive, punchy radio rock compression` |
| **34** | **90s Britpop Guitar Anthem** (*Jangly Rickenbacker Chiming*) | `114 BPM` | `90s Britpop guitar anthem, 114BPM, layered chiming Rickenbacker 12-string & overdriven Vox AC30 guitars, tambourine-led swaggering drum groove, confident melodic male vocal, soaring stadium singalong chorus, warm British studio console mix` |
| **35** | **Post-Hardcore Emo Dynamic** (*Octave-Lead Catharsis*) | `136 BPM` | `Emotional post-hardcore rock, 136BPM, dissonant octave-chord guitar leads over heavy drop-tuned rhythm walls, shifting halftime-to-doubletime drums, raw alternating clean tenor and strained cathartic vocal, stormy nocturnal urgency, tight modern rock master` |
| **36** | **Fast Skate Punk** (*Blistering Double-Time Thrash*) | `148 BPM` | `Blistering 90s skate punk, 148BPM, relentless double-time D-beat snare & cymbal drive, razor-sharp downpicked distortion guitars, metallic galloping bass, defiant raspy shouted punk vocal, raw DIY rehearsal-room energy, dry punchy mix` |
| **37** | **Velvet Art-Punk Indie** (*Motorik Garage Minimal*) | `110 BPM` | `Angular art-punk indie rock, 110BPM, repetitive motorik snare-and-tom pulse, wiry trebly transistor-amp rhythm guitar, droning viola counterline, cool conversational baritone vocal, smoky urban underground tension, narrow vintage mono-room staging` |

---

## Suite 03B: Blues, Post-Punk, Math-Rock, Stoner & Space Rock Part II (#38–#46 • 84–144 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **38** | **Smoky Blues Rock** (*Overdriven Tube Shuffle*) | `104 BPM` | `Smoky blues rock, 104BPM, overdriven Fender Bassman tube-amp guitar licks, Texas shuffle snare groove, husky soulful male vocal, expressive string bends, vintage roadhouse bar room acoustics, warm spring reverb` |
| **39** | **Dark Cold Post-Punk** (*80s Factory Underground*) | `122 BPM` | `Dark cold post-punk, 122BPM, angular chorus-soaked jangly guitar, melodic driving high-register chorused pick-bass lead, deadpan detached baritone vocal, austere gated drum reverb, icy industrial gloom` |
| **40** | **Indie Rock Ballad** (*Wistful Slowcore Telecaster*) | `84 BPM` | `Melodic indie rock ballad, 84BPM, clean reverberant Telecaster arpeggios, soft brushed snare & floor-tom pulse, tender vulnerable male vocal, wistful nostalgic late-autumn mood, intimate analog room warmth` |
| **41** | **Heavy Desert Stoner** (*Mammoth C-Standard Fuzz*) | `92 BPM` | `Stoner psychedelic rock, 92BPM, mammoth C-standard Orange-amp fuzz guitars, plodding heavy triplet-groove cavern drums, distant echoed lethargic vocals, thick sludgy low-end wall, hypnotic desert mirage vibe` |
| **42** | **70s Theatrical Glam** (*Stomp-Clap Boogie Swagger*) | `130 BPM` | `70s retro glam rock, 130BPM, bright crunchy Les Paul boogie riffs, bold honky-tonk piano & punchy brass section, swaggering theatrical lead vocal, flashy glitter-era stomp-clap groove, vintage Trident console warmth` |
| **43** | **Intricate Math-Rock** (*Odd-Meter Clean Tapping*) | `126 BPM` | `Intricate technical math-rock, 126BPM, complex two-hand tapped clean compressor guitar lines, syncopated odd-time signature drums, minimal airy vocals, ultra-crisp transient separation, articulate dry studio mix` |
| **44** | **Fiery Acoustic Folk-Punk** (*Rebellious Busker Singalong*) | `144 BPM` | `Fiery folk-punk, 144BPM, frantically strummed steel-string acoustic guitar, rough punk snare & tambourine, passionate hoarse shouting vocals, rebellious DIY pub-singalong spirit, raw zero-compression dynamics` |
| **45** | **Cosmic Space Rock** (*Zero-Gravity Delay Swells*) | `100 BPM` | `Cosmic space rock, 100BPM, wide ping-pong tape-delay guitars, evolving analog modular synth swells, distant floating vocals, vast weightless interstellar soundscape, ultra-wide panoramic stereo field` |
| **46** | **70s Yacht Soft Rock** (*West Coast Analog Gold*) | `95 BPM` | `Mellow 70s soft rock, 95BPM, warm Fender Rhodes electric piano & clean jazz-inflected semi-hollow guitar leads, tight studio rhythm section, silky male vocal, nostalgic sunset coastal cruise vibe, audiophile 70s LA mix` |

---

## Suite 04: Electronic, Synthwave, Techno, Club, IDM & Ambient Synthesis (#47–#66 • 68–174 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **47** | **Sun-Faded Chillwave** (*VHS Summer Nostalgia*) | `108 BPM` | `Retro synth chillwave, 108BPM, lush sun-bleached vintage analog polysynths, soft cascading arpeggios, washed-out reverb vocals, nostalgic VHS summer memory aesthetic, warm sidechain tape compression` |
| **48** | **Late-Night Deep House** (*Subterranean Lounge Groove*) | `122 BPM` | `Smooth deep house, 122BPM, warm rolling sine-sub bassline, lush minor-9th Rhodes chord pads, sparse soulful diva vocal snippets, hypnotic 4AM underground club groove, silky analog warmth` |
| **49** | **Meditative Drone** (*Beatless Harmonic Bath*) | `68 BPM` | `Ambient drone electronic, 68BPM, slowly evolving Buchla & granular synth drones, zero percussion, floating angelic vocal textures, deep meditative spatial serenity, endless cathedral shimmer decay` |
| **50** | **Liquid Drum & Bass** (*High-Speed Melodic Rollers*) | `174 BPM` | `Liquid drum and bass, 174BPM, crisp fast rolling Amen breakbeats, warm Reese sub-bass, emotive electric piano chords, silky melodic female vocal, uplifting atmospheric flow, tight sub-bass mono control` |
| **51** | **80s Outrun Synthwave** (*Neon Testarossa Highway*) | `118 BPM` | `80s retrowave synthwave, 118BPM, neon brassy Oberheim synth leads, driving 16th-note octave bass arpeggio, gated-reverb LinnDrum snare, nostalgic arcade night-drive energy, wide analog stereo chorus` |
| **52** | **Experimental Glitch IDM** (*Granular Micro-Fractals*) | `112 BPM` | `Experimental glitch IDM, 112BPM, stuttering granular micro-percussion, chopped pitch-shifted vocal fragments, cerebral futuristic sound design, hyper-detailed binaural panning, surgical digital clarity` |
| **53** | **Afterhours Melodic Techno** (*Cavernous Warehouse Pulse*) | `126 BPM` | `Driving melodic techno, 126BPM, hypnotic repeating Moog arpeggio motif, relentless four-on-the-floor kick, faint ghostly vocal texture, cavernous warehouse tension build, expansive stereo reverb tail & tight club low-end` |
| **54** | **UK Garage 2-Step** (*Swung Sub-Bass Shuffle*) | `132 BPM` | `Classic UK garage 2-step, 132BPM, skipped syncopated snare & swung hi-hat shuffle, warm organ-tone M1 bassline, chopped pitch-shifted R&B female vocal hooks, slick late-night London pirate-radio vibe, crisp punchy club master` |
| **55** | **Acid Warehouse Techno** (*Resonant 303 Squelch*) | `138 BPM` | `Raw acid warehouse techno, 138BPM, squelching resonant TB-303 filter-sweep bassline, pounding distorted TR-909 kick and crisp open hi-hats, robotic vocoder vocal stabs, relentless industrial strobe-lit intensity, overdriven analog mixer saturation` |
| **56** | **Progressive Melodic House** (*Sunrise Horizon Build*) | `124 BPM` | `Atmospheric progressive house, 124BPM, evolving plucked analog synth arpeggios, deep warm rolling bassline, airy breathy female vocal refrain, emotional sunrise festival crescendo, wide stereo shimmer & clean sidechain pocket` |
| **57** | **Cyberpunk Midtempo Bass** (*Dystopian Industrial Grit*) | `100 BPM` | `Dark cyberpunk midtempo electronic, 100BPM, heavily distorted wavetable bass growls, mechanical half-time industrial percussion, cold processed vocoder voice, neon rain dystopian sci-fi tension, aggressive multiband compression` |
| **58** | **Berlin Dub Techno** (*Tape-Delay Chord Echoes*) | `120 BPM` | `Hypnotic dub techno, 120BPM, filtered minor synth stabs drenched in multi-tap Roland Space Echo tape delay, deep subterranean sine kick, vinyl crackle & static floor, foggy monochrome nocturnal minimalism, immersive cavernous depth` |
| **59** | **90s Atmospheric Jungle** (*Chopped Breakbeat Odyssey*) | `168 BPM` | `90s atmospheric jungle, 168BPM, intricately chopped time-stretched Think & Amen breakbeats, deep booming 808 sub-bass drops, ethereal pitched-up soul vocal pads, aquatic sci-fi euphoria, warm vintage Akai sampler crunch` |
| **60** | **Minimal Microhouse** (*Organic Click-and-Cut Pocket*) | `125 BPM` | `Minimal microhouse, 125BPM, tactile foley micro-percussion & rimshot clicks, rubbery syncopated sub-bass groove, whispered ASMR vocal syllables, playful intimate afterhours lounge mood, surgical transient placement` |
| **61** | **Balearic Sunset Downtempo** (*Mediterranean Analog Chill*) | `98 BPM` | `Balearic downtempo electronica, 98BPM, warm nylon-string guitar phrases over lazy TR-808 percussion, lush Prophet-5 pad washes, soft wordless female vocal sighs, golden coastal sunset serenity, airy analog tape warmth` |
| **62** | **Nostalgic Mallsoft Vaporwave** (*Slowed-Tape Muzak Haze*) | `82 BPM` | `Slowed nostalgic vaporwave, 82BPM, pitch-dropped 80s FM DX7 electric piano & smooth soprano sax loops, gated snare through cavernous mall reverb, distant slowed vocal chop, surreal consumer-dream melancholy, VHS warble & hiss` |
| **63** | **Darkwave Witch House** (*Occult Hoover & Half-Time Trap*) | `74 BPM` | `Gothic darkwave witch house, 74BPM, detuned stereo hoover synth leads, dragged half-time pitch-shifted snare & booming sub-bass, ghostly formant-lowered vocal chant, eerie nocturnal ritual atmosphere, drenched cathedral reverb` |
| **64** | **Euphoric Uplifting Trance** (*Supersaw Breakdown & Drop*) | `138 BPM` | `Euphoric uplifting trance, 138BPM, soaring detuned supersaw lead melody, rolling sixteenth-note off-beat bassline, angelic operatic female vocal in a beatless piano breakdown, hands-in-the-air mainstage climax, wide festival stereo master` |
| **65** | **French Filter House** (*Phaser Loop & Sidechain Pump*) | `123 BPM` | `French touch filter house, 123BPM, heavily sidechained low-pass filtered disco string & guitar loops, funky slap-bass groove, repetitive vocoder hook, jubilant retro club energy, crunchy vintage compressor pumping` |
| **66** | **Halftime Neuro Glitch-Hop** (*Surgical Bass Design*) | `90 BPM` | `Halftime neuro glitch-hop, 90BPM, morphing modulated Reese basslines, crisp syncopated foley snare & glitch fills, chopped rhythmic vocal percussion, futuristic kinetic sound design, ultra-tight sub-bass and crystalline highs` |

---

## Suite 05: Jazz, Bossa Nova, Folk, Bluegrass, Reggae & Western Cinema (#67–#76 • 72–136 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **67** | **Pastoral Orchestral Folk** (*Chamber Strings & Acoustic*) | `80 BPM` | `Orchestral folk ballad, 80BPM, fingerpicked acoustic folk instruments, warm chamber string ensemble, intimate storytelling female vocal, pastoral nostalgic countryside vista, natural wooden hall acoustics` |
| **68** | **Late-Night Lounge Jazz** (*Velvet Cocktail Quartet*) | `88 BPM` | `Smooth lounge jazz, 88BPM, warm Steinway grand piano voicings, walking upright double bass, whispered brushed snare drums, smoky sultry female jazz contralto, intimate candlelit club ambiance, tube-mic warmth` |
| **69** | **1960s Rio Bossa Nova** (*Sunlit Nylon Guitar*) | `100 BPM` | `Vintage 60s bossa nova, 100BPM, syncopated nylon-string classical guitar, gentle rimshot & cabasa percussion, breezy effortless female vocal, warm sunlit Ipanema beach elegance, classic 1960s warm valve-console analog mix` |
| **70** | **Midnight Dark Noir Jazz** (*Harmon-Muted Trumpet*) | `74 BPM` | `Dark noir jazz, 74BPM, lonely Harmon-muted cool-jazz trumpet, slow walking upright bass, breathy world-weary vocal, rain-streaked midnight detective cinema atmosphere, smoky plate reverb` |
| **71** | **Appalachian Bluegrass** (*Virtuosic Porch Breakdown*) | `112 BPM` | `Traditional bluegrass folk, 112BPM, rapid three-finger finger-roll banjo, lively acoustic fiddle, flatpicked Martin guitar, bright folksy male tenor vocal, rustic mountain spirit, dry single-mic ensemble blend` |
| **72** | **Ethereal New-Age Healing** (*Celestial Harp Sanctuary*) | `72 BPM` | `New-age meditative music, 72BPM, cascading concert harp arpeggios, warm crystalline synth pads, wordless angelic choir vocalizations, peaceful sanctuary healing resonance, ultra-clean spatial depth` |
| **73** | **Spaghetti Western Score** (*Desert Frontier Duel*) | `94 BPM` | `Cinematic spaghetti western, 94BPM, twangy spring-reverb tremolo baritone guitar, mournful harmonica, whistling melody, sparse epic choir shouts, sun-scorched desert tension, vintage 60s Italian widescreen tape film mix` |
| **74** | **Misty Dark Celtic Folk** (*Ancient Gaelic Lore*) | `86 BPM` | `Dark Celtic folk ballad, 86BPM, mournful Gaelic fiddle, airy penny tin whistle, Celtic bodhran frame drum, haunting melancholic female vocal, misty ancient stone-circle atmosphere, natural cavernous decay` |
| **75** | **Island Roots Reggae** (*Warm Kingston One-Drop*) | `98 BPM` | `Laid-back roots reggae, 98BPM, crisp off-beat guitar & bubble organ skanks, deep melodic one-drop bassline, warm relaxed male vocal, sunny Jamaican island dub warmth, analog spring reverb & tape delay` |
| **76** | **Upbeat Two-Tone Ska** (*Punchy Horn Dancehall*) | `136 BPM` | `Upbeat retro ska, 136BPM, punchy trombone & trumpet brass section, fast walking bass, energetic off-beat guitar upstrokes, cheerful lively male vocal, vintage two-tone dancehall party vibe, tight live-room punch` |

---

## Suite 06: Gothic Chamber Folk, Festive & East-Asian Traditional Hybrids (#77–#83 • 76–130 BPM)

| # | Sonic Archetype | Tempo | Engineered Copy-Ready `Style` Prompt String |
| --- | --- | --- | --- |
| **77** | **Gothic Dark Chamber Folk** (*Somber Cello & Acoustic*) | `82 BPM` | `Gothic dark folk, 82BPM, minor-key fingerpicked nylon guitar, resonant low solo cello, somber haunting female vocal, Victorian candlelit mystery atmosphere, intimate woody chamber acoustics` |
| **78** | **Warm Winter Festive Folk** (*Fireside Holiday Glow*) | `92 BPM` | `Cozy Christmas winter folk, 92BPM, warm fingerstyle acoustic guitar, sparkling glockenspiel & sleigh bells, soft choir harmonies, gentle comforting male vocal, nostalgic fireside holiday magic, lush ribbon-mic warmth` |
| **79** | **Cinematic Post-Folk** (*Nordic Glacier Grandeur*) | `88 BPM` | `Cinematic post-folk, 88BPM, ancient Nordic bowed lyre & folk strings blended with sweeping orchestral swells, soaring wordless vocals, vast glacier-and-fjord atmospheric grandeur, widescreen depth` |
| **80** | **Cinematic Eastern Ballad** (*Poetic Zither & Bamboo Flute*) | `76 BPM` | `Cinematic Eastern orchestral ballad, 76BPM, delicate plucked guzheng zither, expressive bamboo dizi flute, lush string orchestra, emotive male tenor vocal, ancient poetic melancholy, concert-hall spatial imaging` |
| **81** | **Martial-Arts Epic Score** (*Heroic Silk-and-Bamboo*) | `102 BPM` | `Epic martial-arts fantasy soundtrack, 102BPM, virtuosic weeping erhu fiddle, rapid pipa lute tremolos, thunderous taiko-style war drums, soaring dramatic vocal, heroic cinematic energy, explosive dynamic range` |
| **82** | **Oriental Chill Lo-Fi Beat** (*Tea-House Zither Boom-Bap*) | `90 BPM` | `Oriental lo-fi hip-hop fusion, 90BPM, meditative seven-string guqin zither sample, dusty boom-bap drum groove, subtle bamboo flute layers, tranquil rainy tea-house ambiance, warm analog cassette lo-fi master` |
| **83** | **Cyber-Folk Shamisen Festival** (*High-Velocity Silk & Sub*) | `130 BPM` | `High-energy East-Asian cyber-folk fusion, 130BPM, percussive rapid tsugaru shamisen riffs, driving taiko drum ensemble & modern sidechained sub-bass, fierce traditional vocal kakegoe chants, neon lantern festival adrenaline, wide punchy hybrid master` |
