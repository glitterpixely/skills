# BytePlus Media Evidence

## Contents

- [Scope and method](#scope-and-method)
- [Traceability map](#traceability-map)
- [Still-image catalog](#still-image-catalog)
- [Video technical inventory](#video-technical-inventory)
- [Sequence findings](#sequence-findings)
- [Cross-example lessons](#cross-example-lessons)

## Scope and method

This is the visual-evidence layer for BytePlus ModelArk document `2607689`. The authenticated Lark text capture contained no embedded image/video markers, captions, or media URLs, so no visual claim is attributed to that capture.

Audit performed on the BytePlus page's 51 images and 22 videos:

- all 51 stills were opened and inspected at full resolution;
- all 9,622 video frames were decoded end-to-end;
- frame counts, duration, frame rate, resolution, aspect ratio, codec, and audio streams were inventoried;
- dense two-frame-per-second sheets, scene-change frames, and targeted four-frame-per-second, seam, face, action, and side-by-side sheets were inspected;
- the first eleven videos also received per-frame checksum manifests;
- source/output pairs were compared for timing, composition, action, facial changes, seams, and audio envelope/correlation where useful;
- audio codecs, rates, levels, silence, timing, and correlations were inspected, but semantic speech transcription and music-genre recognition were not treated as independently verified.

Every video decoded without corruption. The second audit set contained no black frames or exact consecutive duplicate decoded frames. Treat all output observations as evidence from one provider example, not as a model guarantee.

## Traceability map

Local still names map one-to-one: `image_001` is provider `img_001`, through `image_051` as provider `img_051`.

Local video numbering begins after the stills:

| Local ID | Provider ID / source filename | Document role |
|---|---|---|
| `video_052` | `vid_000_panda-cub-basic.mp4` | Basic prompt output |
| `video_053` | `vid_001_video-1.mp4` | Coarse blockout input |
| `video_054` | `vid_002_10.mp4` | Coarse-blockout rendered output |
| `video_055` | `vid_003_8月3日(1).mp4` | Synchronized blockout/output comparison |
| `video_056` | `vid_004_偷感很重.mp4` | Fine blockout input |
| `video_057` | `vid_005_seedance25-cyberpunk-rooftop-raccoon-render-6s-720p-20260804-baseline-run01_cgt-20260804112511-lpq4w.mp4` | Fine-blockout rendered output |
| `video_058` | `vid_006_飞船-594音乐.mov` | Spacecraft re-render tutorial/comparison |
| `video_059` | `vid_007_守护机器人_火箭发射_30s.mp4` | Storyboard output |
| `video_060` | `vid_008_pixel_cgt-20260805221932-s8jkr.mp4` | Ordered-keyframe output |
| `video_061` | `vid_009_对镜含泪凝视.mp4` | Aging-edit source |
| `video_062` | `vid_010_20260803T215035_2614ad0b51c3_表情变化.mp4` | Aging-edit output |
| `video_063` | `vid_011_reference1.mp4` | Fight-edit source |
| `video_064` | `vid_012_output.mp4` | Fight-edit output |
| `video_065` | `vid_013_30秒动漫独白.mp4` | Dialogue-localization source |
| `video_066` | `vid_014_动漫中文输出.mp4` | Dialogue-localization output |
| `video_067` | `vid_015_0615_发芽.mp4` | Flower-growth extension source |
| `video_068` | `vid_016_seedance25-extend-bee-pollination-5s-720p-mov-20260803-baseline-run01_cgt-20260803215229-28wbd.mov` | Standalone extension |
| `video_069` | `vid_017_8月3日.mp4` | Stitched source-plus-extension preview |
| `video_070` | `vid_018_8282ec97-0d00-4a2f-9896-9c1d88c600bc.mp4` | One-click dog montage |
| `video_071` | `vid_019_1.mp4` | Transition source 1 |
| `video_072` | `vid_020_2.mp4` | Transition source 2 |
| `video_073` | `vid_021_积木转场视频.mov` | Generated transition output |

## Still-image catalog

### Storyboard-versus-keyframe demonstration, images 001-021

- `image_001` — 1536x1024. Six-panel monochrome manga storyboard: a man and braided girl in a snowy bedroom, a book handoff, tearful close-ups, the girl exiting, and the man remaining at the window. Captions specify shot size, angle, composition, and fixed camera. Pixel-identical to `image_012`.
- `image_002` — 1536x1024. Pastel new-Chinese/Ukiyo-e keyframe: enormous blue-pink spirit fish dominates the left sky; an ornate umbrella-covered mountain town and pagoda occupy the right; a river valley lies below. Strong directional first composition.
- `image_003` — 1536x1024. Wider town approach without the fish; city on the right two-thirds and negative cloud/sky space on the left. Defines destination and approach space.
- `image_004` — 1280x853. Closer town view with a centered pagoda and a blue Western-style spire. Tightens scale while preserving palette and linework.
- `image_005` — 1536x1024. Symmetrical ornate Chinese hall, circular pool in the foreground, and the mountain town through the window. Clean interior geography.
- `image_006` — 1536x1024. Same hall and composition; fish descends through the open window toward the pool. Adds trajectory without changing environment.
- `image_007` — 1536x1024. Tight pool composition; fish swims rightward amid concentric ripples. Strong action/state anchor.
- `image_008` — 1536x1024. Dark temple; rear-view monk faces a large framed painting of the hall and fish. Candles and vertical plaques support the nested-picture ending reveal.
- `image_009` — 1535x1024. Explicitly discouraged 3x3 tiger-versus-warrior storyboard: oversharpened photoreal panels, dense Chinese titles/timecodes/captions, busy grass and costume detail. Nine panels can still be too noisy.
- `image_010` — 1254x1254. Explicitly discouraged 16-panel photoreal sunset-street confrontation with captions in every frame. Exceeds the 15-panel recommendation and over-specifies micro-actions.
- `image_011` — 1536x1024. Explicitly discouraged four-shot factory-fight storyboard embedded in a dense Chinese table of lens, shot, duration, and description fields. Low panel count alone does not cure layout/text clutter.
- `image_012` — 1536x1024. Recommended simple line-art bedroom storyboard, pixel-identical to `image_001`. Six readable compositions with restrained detail; the prompt, not the drawing, supplies atmosphere and continuity.
- `image_013` — 6300x1080. Documentation montage of four supporting references: empty snowy bedroom; male front/side/back turnaround; braided female front/side/back turnaround; rose book cover with `快快乐乐`. It is a display strip, not proof that the four assets should be uploaded as one collage.
- `image_014` — 1024x1024. 3x3 fantasy-panda concept board: mountain temple, cub, woman feeding it, magical leaf vortex, incense, bridge, spectral tiger, and tea pour. A rich high-level story concept suited to a simplified “construct a complete story” instruction rather than a strict shot contract.
- `image_015` — Exact duplicate of `image_002`, repeated in the advanced keyframe section.
- `image_016` — Exact duplicate of `image_003`.
- `image_017` — Exact duplicate of `image_004`.
- `image_018` — Exact duplicate of `image_005`.
- `image_019` — Exact duplicate of `image_006`.
- `image_020` — Exact duplicate of `image_007`.
- `image_021` — Exact duplicate of `image_008`. Images 015-021 turn the earlier sequence into independent ordered keyframes, which are intended to preserve visible state/composition more strongly than one grid.

### Coarse blockout rendering references, images 022-030

- `image_022` — 2048x1152; example label Image 2. Warm 3D-animation overhead bedroom: girl holds a toy airplane amid suspended planets, stars, and clouds. Opening composition.
- `image_023` — 2048x1152; example label Image 3. Girl flies a yellow toy plane through sunset clouds and white birds; side-following composition.
- `image_024` — 2048x1152; example label Image 4. Plane surrounded by a flying whale, winged horse, dragon, and birds. Dense fantasy escalation.
- `image_025` — 1280x720 JPEG; example label Image 5. Rear/over-shoulder plane dive toward water and a pink crystalline sea creature; visibly softer and more motion-blurred than adjacent references.
- `image_026` — 2048x1152; example label Image 6. Girl in a bubble helmet rides a translucent manta through luminous coral; strong central travel axis.
- `image_027` — 2048x1152; example label Image 7. Underwater space-time rift with torn black center, blue-white edge, jellyfish, and cosmic forms. No girl; chiefly an environment/effect reference.
- `image_028` — 1920x1080 JPEG; example label Image 8. Girl in a white spacesuit stands on a tiny planet and reaches for a glowing star against a purple galaxy.
- `image_029` — 3010x1688; example label Image 9. Overhead bedroom return: sleeping girl on a patchwork rug, blanket and open space book, father's hand entering foreground.
- `image_030` — 2546x1435; example label Image 10. Close-up of the closed picture book with stable readable title `小小冒险家 / Little Adventurer`; intended final frame.

### Robot/rocket storyboard set, images 031-034

- `image_031` — 1536x1024. Simple nine-panel line-art board: launch-site wide, robot/woman medium, woman close-ups, launch, explosion, grief, protective embrace, and smoking wreckage. Strong high-level sequencing.
- `image_032` — 1536x1024. Photoreal environment reference: centered rocket and launch tower in golden grassland at sunset beneath a cool-blue upper sky.
- `image_033` — 1536x1024. Actual asset is the grandmother turnaround: front, side, and back, long loose silver hair, gold dress with blue embroidery.
- `image_034` — 1536x1024. Actual asset is the robot sheet: distressed teal body, glowing red camera eyes, front/side/back/head close-up, exposed chest mechanisms; its printed specification gives a 1420 mm height.

The accompanying source prose reverses Images 3 and 4, describes the woman with a low bun, and calls the robot twice human height. The visible assets show the opposite numbering, loose hair, and a 1420 mm robot. The output follows the assets: loose hair and a roughly human-scale robot. Do not silently copy a prose mapping that conflicts with inspected media; preserve user priority, but warn or clarify when failure is nearly certain.

### Pixel-wuxia ordered keyframes, images 035-040

All six are 500x890 vertical RGBA images on the same pale-blue canvas, with a repeated character, palette, and pixel scale.

- `image_035` — Ink-wash ring, calligraphy logo `江湖风云`, and small red `原创` seal; large negative space. Opening hold.
- `image_036` — Male wuxia lead close-up: topknot, long black hair, blue ribbon, blue-white robe, direct serious gaze. Slide/blink/exit state.
- `image_037` — Centered dark-blue thread-bound manual labeled `武功秘籍` with red seal. Logo-replacement state.
- `image_038` — Full-body hero beneath blue diamond question mark; headline `今日闯江湖!`; sheathed sword. Jump, hit, greet, and run-preparation state.
- `image_039` — Same hero in right-facing airborne run, sword horizontal, hair/ribbon/robe trailing left. Run/follow bridge.
- `image_040` — Final interface: `三月廿七日`, bird silhouette, yin-yang divider, body copy, button `进入江湖（开始）`, and presenting hero at right. Finished text/UI anchor.

This set demonstrates the value of a shared canvas and embedding literal text in supplied keyframes rather than asking generation to invent it.

### Reference-image fight edit, images 041-043

- `image_041` — 2048x2048 RGB. Empty medieval stone terrace with broad paving, battlement, tower/banner, foggy mountain valley, and overcast sky. Clear central duel space.
- `image_042` — 2048x2048 RGBA. Headless/hands-free brown leather fantasy outfit: layered shoulder armor, tan cowl, straps, belts, skirt panels, trousers, and boots. Costume/material reference, not identity.
- `image_043` — 2048x2048 RGB. Headless/hands-free black/charcoal fitted leather outfit: gray scarf/cowl, quilted torso, dark pants, and tall boots. Costume/material reference, not identity.

### One-click dog montage, images 044-051

All eight show the same black sighthound/greyhound-like dog in varied outfits and cafe/outdoor settings.

- `image_044` — 452x689 JPEG. Front-facing dog runs toward a yellow ball in a blue coat; action/finale image.
- `image_045` — 664x927 JPEG. Seated three-quarter-right beside a brick/stucco wall in a beige sherpa jacket.
- `image_046` — 544x769 JPEG. Black-and-white striped shirt at a cafe table with cake, strawberry, and white mug; head turned right.
- `image_047` — 559x772 JPEG. Patio-step portrait in a white floral/frilled dress.
- `image_048` — 588x993 JPEG. Frontal cafe portrait in dark-green sweater with a heart latte dominating the foreground.
- `image_049` — 291x446 JPEG. Lower-resolution outdoor standing portrait in tan coat/harness with plaid collar; head left.
- `image_050` — 293x444 JPEG. Lower-resolution cozy interior; dog reclines in wicker chair wearing a cream turtleneck among teddy bears and flowers.
- `image_051` — 292x447 JPEG. Lower-resolution warm cafe/bench portrait in plush ivory jacket with pendant collar; head right.

## Video technical inventory

Container duration is shown; decoded video duration differs slightly where noted. All listed audio streams are stereo.

| Asset | Duration | FPS / decoded frames | Resolution | Audio |
|---|---:|---:|---|---|
| `video_052` | 8.042 s | 24 / 193 | 1280x720 | AAC 32 kHz |
| `video_053` | 30.000 s | 30 / 900 | 1920x1080 | AAC 44.1 kHz, effectively silent |
| `video_054` | 30.042 s | 24 / 721 | 1280x720 | AAC 32 kHz |
| `video_055` | 30.042 s | 24 / 721 | 3840x1080 | AAC 44.1 kHz |
| `video_056` | 6.042 s | 24 / 145 | 960x960 | no audio |
| `video_057` | 6.050 s | 24 / 145 | 1280x720 | AAC 32 kHz |
| `video_058` | 26.624 s; video 26.542 s | 24 / 637 | 1920x1080 | AAC 48 kHz plus data track |
| `video_059` | 30.050 s; video 30.042 s | 24 / 721 | 1280x720 | AAC 32 kHz |
| `video_060` | 15.050 s; video 15.042 s | 24 / 361 | 720x1280 | AAC 32 kHz |
| `video_061` | 15.042 s | 24 / 361 | 3840x2160 | AAC 44.1 kHz |
| `video_062` | 15.104 s; video 15.042 s | 24 / 361 | 1280x720 | AAC 32 kHz |
| `video_063` | 8.080 s; video 8.042 s | 24 / 193 | 1664x1248 | AAC 44.1 kHz |
| `video_064` | 8.096 s; video 8.042 s | 24 / 193 | 1112x834 | AAC 32 kHz |
| `video_065` | 30.042 s | 24 / 721 | 1280x720 | AAC 32 kHz |
| `video_066` | 30.042 s | 24 / 721 | 1280x720 | AAC 32 kHz |
| `video_067` | 15.046 s; video 15.042 s | 24 / 361 | 1280x720 | AAC 44.1 kHz |
| `video_068` | 5.000 s | 24 / 120 | 1280x720, yuv444p | PCM s16le 32 kHz |
| `video_069` | 20.083 s | 24 / 482 | 1280x720 | AAC 44.1 kHz |
| `video_070` | 15.050 s; video 15.042 s | 24 / 361 | 720x1280 | AAC 32 kHz |
| `video_071` | 5.056 s; video 5.042 s | 24 / 121 | 1280x720 | AAC 32 kHz |
| `video_072` | 5.056 s; video 5.042 s | 24 / 121 | 1280x720 | AAC 32 kHz |
| `video_073` | 12.074 s; video 12.067 s | 30 / 362 | 1280x720 | AAC 44.1 kHz |

## Sequence findings

### Basic prompt output: video 052

One continuous low-angle nature-documentary shot. The panda rolls clumsily down a gentle slope from roughly 0-3.5 seconds, flops onto its back/side, settles belly-down, raises its head toward camera, and rests. The camera follows subtly without losing it; grass, moss, clover, stones, flowers, and backlit forest remain stable. Natural depth of field and dappled light succeed; no cut, subtitle, gross mutation, or anatomy failure is visible. Audio is active but extremely quiet, consistent with restrained ambience.

### Coarse blockout transfer: videos 053-055 with images 022-030

`video_053` is an abstract primitive animation that encodes a full 30-second camera/action skeleton. Major structural transitions occur near 3.27, 10.5, 19.13, and 22.87 seconds: overhead bedroom/throw, flight, underwater portal, space, and bedroom return. It supplies orbit, follow, dive, portal passage, transformation, overhead push, blanket gesture, and book close while intentionally supplying no target appearance.

`video_054` renders that skeleton:

- 0-3 s: overhead bedroom push; girl rises and throws the plane.
- 3-10 s: toy becomes a flying plane; bird wipe, side-following cloud flight, creatures, and dive.
- 10-19 s: water impact, bubble helmet, manta ride, coral world, rift reveal/entry.
- 19-23 s: spacesuit transformation and glowing-star reach.
- 23-24 s: cosmic scene folds/dissolves into the bedroom.
- 24-28 s: sleeping girl; father enters partly and covers her.
- 28-30 s: push to book; hand closes it; readable cover hold.

`video_055` is a 32:9 editorial split, not another generated output. It confirms close macro alignment of timing, camera direction, spatial blocking, portal crossing, return, and book close. Misses remain: the winged horse is not clearly readable; planet-to-planet jumping compresses into one star reach; the father is mainly a partial hand/head; some connections are cuts/dissolves rather than one continuous take.

Lesson: list the blockout dimensions that remain invariant, then bind appearance/environment separately. Abstract geometry can transfer macro choreography strongly, but every decorative story request may not survive a dense 30-second plan.

### Fine blockout rendering: videos 056-057

`video_056` is a clean, static side-view, untextured child mannequin walking/running left-to-right along a white wall. It supplies gait, shadow, path, timing, and exit without trajectory lines, controls, or camera cones.

`video_057` replaces it with a black-suited raccoon-like silhouette crossing a neon blue-purple cyberpunk rooftop. Duration, lateral path, gait rhythm, and fixed side camera transfer; the unlocked output changes from square to 16:9. The dark silhouette sometimes reads as wolf/large rat rather than unmistakably raccoon. Identity readability can suffer when the requested styling hides the diagnostic features of the subject.

### Spacecraft re-render tutorial: video 058

The composite shows a white-model derelict-spacecraft fly-through (0-2.5 s), a generation interface and typed Chinese prompt (about 2.5-6.4 s), the textured cinematic render (about 6.4-18.4 s), and a synchronized split comparison (about 18.4-26.6 s).

The prompt visible only inside the video operationally says to preserve the source video's camera movement, duration, composition, shot size, spatial relationships, object positions, model structure, and motion paths; use the image for material, lighting, color, and atmosphere; replace white-model material with realistic material; and add natural light/shadow, contact shadows, ambient light, reflections, highlights, and spatial depth for cinematic rendering.

Critical provenance caveat: the visible model selector reads `Seedance 2.1`. Preserve this as a transferable re-rendering workflow pattern, not evidence of a 2.5-specific user interface or exclusive 2.5 capability.

### Storyboard output: video 059 with images 031-034

Shot changes occur close to the requested whole-second boundaries: approximately 3.125, 5.917, 10.167, 13.833/14.417, 17.667, 21.792, 24.667, and 27.583 seconds versus 3/6/10/14/18/22/25/28 in the text. The sequence is: golden launch-site wide; robot supports woman; reluctant face close-up; launch; explosion; tearful shock; breakdown; low-angle protective embrace under falling debris; distant twilight embrace.

The environment, palette, grain, shallow depth, dialogue performance, and storyboard order are strong. There are no subtitles. The output resolves source contradictions in favor of the actual assets: the woman has loose hair and the robot is approximately human height. Visual source evidence may overpower contradictory prose even when the prose is explicit.

### Ordered-keyframe output: video 060 with images 035-040

The output holds `江湖风云`, slides the male close-up upward, blinks/exits, reveals `武功秘籍`, introduces the jumping/question-mark state and `今日闯江湖!`, follows the rightward run, and slides in the final interface. The closing heading `三月廿七日`, generated body copy, and `进入江湖（开始）` button remain readable. Light-blue continuity and graphic transitions are strong. It resembles polished 16-bit sprite work more than strict 8-bit, and the final pose uses one obvious presenting arm rather than both fully open.

Lesson: exact text/UI is most reliable when already drawn into ordered keyframes and given a deliberate hold. Shared canvas/style/scale helps the connective motion.

### Aging instruction edit: videos 061-062

The 4K source is one mirror shot with slow push, restrained gaze change, tear formation/travel, and no cut. The output keeps composition, shot path, blouse, lighting, tearful gaze, and performance rhythm. The woman remains young through roughly 5 seconds, gains gray hair/wrinkles through roughly 9-10 seconds, then softens into a full tearful smile by 11-15 seconds. Identity stays continuous with no visible flicker.

The example demonstrates the documented lock boundary: ratio and decoded 361-frame duration remain aligned, but resolution falls from 3840x2160 to 1280x720 and container duration differs by about 0.062 seconds. Do not promise resolution preservation merely because an edit is duration/ratio locked.

### Reference-image fight edit: videos 063-064 with images 041-043

The source is a static medium-wide 4:3 rooftop/platform shot: dark fighter left, pale fighter right, guard/feints through about 4.2 seconds, lunge/intercept around 4.29, rapid parry/counter near 5.2, clinch near 6.25, and reset near 7.2-7.75.

The output keeps one-shot framing, 193 frames, choreography, identities, relative positions, and beat timing while replacing the environment with the overcast stone terrace and the clothing with fantasy armor. Fast hand motion blurs naturally; no gross extra limbs appear. Resolution changes from 1664x1248 to 1112x834.

Important failure: the apparent outfit mapping is inverted relative to the written indices. The dark/left source fighter receives the black reference outfit, while the light/right fighter receives the brown one. Visual light/dark similarity overrode the cross-mapping. The requested cold-weapon setup never reaches a weapon draw. Source/output audio is strongly correlated, but the output is roughly 5.4 dB louder.

Lesson: when visual similarity can defeat numeric mapping, use labeled/cropped references and repeat source-relative assignments. Give required weapon/action payoffs their own timed beat. Preserved audio timing does not imply identical level.

### Dialogue localization: videos 065-066

Both are the same 30.042-second animated one-shot of a dark-haired young man in a cool-blue corridor/room, with a slow medium-to-close push. The restrained speech, right-hand rise, closing fist, hand drop, gaze, clothing, lighting, and camera remain nearly identical; full-frame comparison measured SSIM 0.9873. No subtitles or visible text appear.

Matched mouth shapes differ while the rest of the face/body stays aligned, showing genuine lip retiming rather than a simple audio replacement. Audio changes materially while duration stays equal; output level is about 2.7 dB higher. The audit did not independently transcribe the speech, so language identity comes from the documented task plus visual/audio change, not speech recognition.

Lesson: state `change only dialogue and mouth articulation`, name the target language and any explicit voice/accent need, state no subtitles when required, and QA paired face frames plus audio.

### Forward extension: videos 067-069

The 15-second source moves from seed splitting in soil, to sprout and leaves, to bud, to an open yellow flower. The five-second MOV extension begins on a matching open bloom: a bee enters, lands, crawls among the anthers, receives an extreme-macro treatment, then rises while visible pollen falls. Bee anatomy and pollen remain readable.

The prompt's distinct “another flower of the same species” destination is not clearly reached; the macro continues to read as the same bloom. The local action succeeds while the travel/destination request remains ambiguous.

The 20.083-second stitched preview retains the source section almost exactly after re-encoding and has an imperceptible visual seam near 15 seconds. Input audio correlation through the original segment is 1.0; extension-envelope correlation is about 0.982 and levels stay close. The stitched duration is about 0.037 seconds longer than the nominal source-plus-extension sum because of handoff/container timing.

Lesson: define and inspect the exact boundary, request MOV for both input/output where supported, QA a stitched preview, and make any new destination unmistakable or reference-bound.

### One-click montage: video 070 with images 044-051

The vertical 15-second output uses all eight stills exactly once. Detected clean cuts occur at 2.000, 3.875, 5.708, 7.542, 9.292, 10.958, and 12.833 seconds. Model-selected order is 046, 048, 045, 047, 049, 051, 050, 044. Treatments include dashed cutout outlines, hearts, sparkles, steam, leaves, flowers, halftone/grid doodles, and motion lines. Stable generated text `Coffee Time` appears in the latte shot.

Dog identity, outfits, and photographic compositions remain recognizable. Most movement is gentle head/parallax work, but the final running still becomes a substantial gallop and image 049 changes pose. Therefore “move slightly” and “do not alter the originals” were not literal constraints. Stereo background music is present because this source example explicitly requested it.

Lesson: say whether every asset appears exactly once, fix or free the order, set a hold range, name allowed overlays, and constrain motion by channel. For strict still fidelity, allow camera push/parallax only and prohibit new subject/body/limb poses.

### Seamless transition: videos 071-073

Source 1 is a continuous low/fisheye office FPV flying among scattered mahjong-like tiles toward and up a tall white tile tower. Source 2 is a sunset aerial approaching a tapered golden Art-Deco skyscraper and diving down its facade.

The 12.074-second output preserves the source sequences visually but re-encodes/retimes them from 24 to 30 fps and inserts about 1.9-2.0 seconds. Around 5.0-6.9 seconds, the white tower splits and bends outward; warm light blooms through the center; a gold skyscraper appears/grows; the office dissolves into the city; then the source-2 dive continues. The circular office light becomes a useful graphic halo. There is no hard seam, black frame, or freeze.

Partial misses: no unmistakable rapid 180-degree turn occurs; motion reads as continuous rise/reveal/descent. Tiles peel and warp around one building instead of each tile becoming a distinct high-rise. The deformation is visibly AI-morphed but coherent. Audio envelope alignment to both sources is strong and levels stay close.

Lesson: define the source-1 boundary action, visible orientation landmarks, camera turn/path, one-to-one transformation mapping, target opening state, and audio handoff. A bridge may change total duration and frame rate even when source portions remain close.

## Cross-example lessons

1. Inspect assets before trusting prose. The provider page itself contains reversed image labels, hairstyle/height contradictions, and a legacy 2.1 selector inside a 2.5 guide.
2. Separate invariant structure from replacement appearance. Name camera, duration, framing, space, positions, model structure, paths, and timing separately from material, light, color, identity, and atmosphere.
3. Storyboard grids are high-level plot/shot guides. Keep them simple, preferably line art, usually no more than 15 panels, and low in embedded text/noise. Use independent keyframes for stricter visible states.
4. Whole-second stage boundaries can align closely when each interval contains one feasible dramatic beat. They remain pacing controls, not frame-accurate guarantees.
5. Locked edit/extension behavior preserves ratio and approximate timing, not resolution, codec, frame rate, loudness, or bitwise frames.
6. Preserve/change contracts should name every source category. Numeric mapping alone may lose to visual similarity; repeat consequential source-relative mappings and use unmistakable references.
7. Exact text/UI is safer as prepared keyframe artwork with explicit stability and hold instructions.
8. QA semantic completion, not polish alone. Provider examples visibly miss or soften a winged horse, planet hopping, clear father entrance, weapon draw, second flower, literal turn, one-to-one tile transformation, and strict 8-bit style.
9. For editing/localization, compare matched frames, mouth/face regions, timing, and audio. Equal duration does not prove faithful preservation.
10. For extension and transition, inspect the seam in a stitched result and track container/fps/audio changes.
11. Example-specific music does not establish a default. Include music only when requested; otherwise preserve existing source audio or specify ambience/effects/dialogue as appropriate.
