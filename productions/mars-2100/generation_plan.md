# Generation plan: What If You Were Born on Mars in 2100?

Rendered from `plan.json` by `render_generation_plan.py`. **Nothing here has been submitted.**

Locked stack: `gpt_image_2_5` (flare by default, sunburst only for avatar stage edits), `seedance_2_5` (1080p accepted shots), 9:16, `seed_audio` narration.

## 1. Avatar concept: "Pip"

**Design:** small knitted-wool doll figure in cream wool with visible stitch texture, oversized glossy green enamel button eyes, sunflower-yellow pom-pom beanie.

- **silhouette:** compact rounded figure: big round head under a sunflower-yellow pom-pom beanie, soft pear-shaped body, short stubby limbs; reads instantly at thumbnail size
- **proportions:** head 1/3 of height as newborn, 1/4 as child, 1/5 as teen and adult; button eyes about 1/3 of face width
- **materials:** cream knitted wool with visible stitch rows, slightly fuzzy edges, glossy green enamel buttons for eyes, small stitched curved mouth in brown thread
- **clothing:** permanent accent: sunflower-yellow knitted pom-pom beanie (never in any background); per-chapter garments in stage_changes
- **identifying features:** glossy green enamel button eyes, sunflower-yellow pom-pom beanie, brown stitched curved mouth, one darker cream darning patch on the left cheek

**Originality:**
- Knitted wool and button eyes: no glass, translucent or skeleton look; the validator's forbidden-design check passes.
- It also differs from the Skill's example avatar (a birch marionette).
- The yellow beanie is the one accent colour. It never appears in any Mars background (rust, butterscotch, blue dusk, greenhouse green).

| Chapter | Age | Clothing | State |
|---|---|---|---|
| 1 | newborn | silver thermal swaddle + beanie | pristine, fluffy wool |
| 2 | child (6) | cut-down orange colony jumpsuit; outdoors a small orange pressure suit with a polycarbonate bubble helmet | wool slightly fuzzed at elbows |
| 3 | teen (14) | patched grey utility coveralls, dust goggles pushed up on the beanie | red dust worked into the wool edges |
| 4 | adult (22) | navy travel jacket with a plain round mission patch, shoulder bag | neat, freshly washed wool, hopeful |
| 5 | adult (30) | green greenhouse apron over coveralls, soil-stained hands | beanie faded, a few repair stitches in yellow thread, settled and calm |

## 2. GPT Image 2.5 jobs (17)

All jobs use `model: gpt_image_2_5`, `aspect_ratio: 9:16`, `resolution: 2k`, submitted with `generate_image_batch` (≤ 12 per call). The exception is I-1, a single `generate_image` so you can approve it on its own.

| Job | Batch | Variant / quality | image_references | Purpose |
|---|---|---|---|---|
| I-1 avatar reference | I1 (alone, approval gate) | flare / high | — | AVATAR_REF |
| I-stage-newborn | I2 | **sunburst** / high | AVATAR_REF | avatar:stage:newborn |
| I-stage-child | I2 | **sunburst** / high | AVATAR_REF | avatar:stage:child |
| I-stage-teen | I2 | **sunburst** / high | AVATAR_REF | avatar:stage:teen |
| I-stage-adult22 | I2 | **sunburst** / high | AVATAR_REF | avatar:stage:adult22 |
| I-stage-adult30 | I2 | **sunburst** / high | AVATAR_REF | avatar:stage:adult30 |
| I-prop seedcup | I3 | flare / high | — | prop:seedcup |
| I-env-ch1 (= shot 2 keyframe) | I3 | flare / high | avatar:stage:newborn | env:ch1 |
| I-env-ch2 (= shot 7 keyframe) | I3 | flare / high | avatar:stage:child | env:ch2 |
| I-env-ch3 (= shot 13 keyframe) | I3 | flare / high | avatar:stage:teen | env:ch3 |
| I-env-ch4 (= shot 17 keyframe) | I3 | flare / high | avatar:stage:adult22 | env:ch4 |
| I-env-ch5 (= shot 22 keyframe) | I3 | flare / high | avatar:stage:adult30 | env:ch5 |
| I-kf-shot1 | I4 (after --gate-keyframes) | flare / **xhigh** | avatar:stage:newborn, env:ch1 | hook frame: premise + avatar identity (xhigh) |
| I-kf-shot3 | I4 (after --gate-keyframes) | flare / high | avatar:stage:newborn, env:ch1 | diegetic UI: signal-delay counter '12:00' on comms screen |
| I-kf-shot12 | I4 (after --gate-keyframes) | flare / high | avatar:stage:child, env:ch2 | composition: tiny suited child silhouetted against a blue Martian sunset |
| I-kf-shot19 | I4 (after --gate-keyframes) | flare / high | avatar:stage:adult22, env:ch4 | diegetic UI: medical scanner panel flashing red 'NOT CLEARED' |
| I-kf-shot26 | I4 (after --gate-keyframes) | flare / **xhigh** | avatar:stage:adult30, env:ch5 | payoff frame: prop callback in final tableau (xhigh) |

Total: **17 GPT Image 2.5 jobs**.

Batch order:
1. **I1:** avatar reference. **Stop for your approval.**
2. **I2:** 5 stage edits.
3. **I3:** prop + 5 chapter establishing frames (they need the stage refs).
4. **I4:** 5 scene keyframes, only after `validate_plan.py --gate-keyframes` passes.

### Prompts

**I-1 avatar reference** (flare, high):
```
Character reference sheet on a neutral warm-grey studio backdrop: small knitted-wool doll figure in cream wool with visible stitch texture, oversized glossy green enamel button eyes, sunflower-yellow pom-pom beanie.
Silhouette: compact rounded figure: big round head under a sunflower-yellow pom-pom beanie, soft pear-shaped body, short stubby limbs; reads instantly at thumbnail size. Proportions: head 1/3 of height as newborn, 1/4 as child, 1/5 as teen and adult; button eyes about 1/3 of face width. Materials: cream knitted wool with visible stitch rows, slightly fuzzy edges, glossy green enamel buttons for eyes, small stitched curved mouth in brown thread.
Clothing: permanent accent: sunflower-yellow knitted pom-pom beanie (never in any background); per-chapter garments in stage_changes; wearing navy travel jacket with a plain round mission patch, shoulder bag for the sheet.
Identifying features: glossy green enamel button eyes, sunflower-yellow pom-pom beanie, brown stitched curved mouth, one darker cream darning patch on the left cheek.
Three views in one vertical image: full body front (top), three-quarter view (middle), face close-up (bottom).
Consistent proportions, no text, no logos. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition
```
**I-stage-* (sunburst edits of AVATAR_REF):**
```
Same character: identical silhouette, materials, eyes and identifying features (glossy green enamel button eyes, sunflower-yellow pom-pom beanie, brown stitched curved mouth, one darker cream darning patch on the left cheek). Change only: age = {age}, clothing = {clothing}, state = {state}. Full body, neutral backdrop.
```
**I-prop seedcup:**
```
Prop reference on neutral warm-grey backdrop: a small dented tin cup, hand-scuffed, holding dark potting soil with one apple seed resting on top. Close-up, no text, no logos. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition
```
**Chapter establishing frames and scene keyframes** (refs: avatar stage + chapter frame):
- **shot 1** (Medium): "Medium shot. The character from the first reference (newborn stage), newborn avatar in a padded incubator pod opens its button eyes as red dust streaks past the porthole. buried habitat nursery, curved regolith-brick walls, small porthole showing red dust blowing outside, warm amber lamps. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 2** (Medium): "Medium shot. The character from the first reference (newborn stage), a parent in a grey colony jumpsuit lifts the swaddled newborn as soil trickles on the dome roof. cutaway of habitat dome buried under red regolith mounds, warm interior light, rocky crater outside. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 3** (Medium Close-Up): "Medium Close-Up shot. The character from the first reference (newborn stage), the newborn wails in the foreground while a signal bar crawls across the screen behind. comms alcove, glowing screen with a transmission bar and delay counter reading 12:00. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 7** (Medium): "Medium shot. The character from the first reference (child stage), six-year-old avatar steps onto a floor scale whose needle barely moves; classmates giggle behind. underground school tunnel, padded walls, painted planet murals, cool white strip lights. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 12** (Wide): "Wide shot. The character from the first reference (child stage), the suited child stands on the crater rim as the sun sinks and the blue halo spreads. crater rim at dusk, cold blue glow around a small pale sun, butterscotch sky above, long shadows. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 13** (Wide): "Wide shot. The character from the first reference (teen stage), the teen avatar presses a hand to the window as the dust wall swallows the horizon. habitat observation window, a towering brown dust wall rolling across the plain, light dimming to rust. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 17** (Medium): "Medium shot. The character from the first reference (adult22 stage), the adult avatar raises a glowing boarding token and grins at the rocket outside. launch hall with a tall window, a silver passenger rocket on the pad outside, pale morning light. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 19** (Medium Close-Up): "Medium Close-Up shot. The character from the first reference (adult22 stage), the avatar stands in the scanner arch as the panel flashes red and its smile fades. medical scan booth, scanner arch, red alert panel. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 22** (Wide): "Wide shot. The character from the first reference (adult30 stage), the adult avatar walks a row of crops with a watering can, mist drifting in shafts of light. huge greenhouse dome, terraced green rows, misting sprinklers, red cliffs beyond the dome. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"
- **shot 26** (Wide): "Wide shot. The character from the first reference (adult30 stage), the avatar looks up at a tiny blue dot (Earth) in the dusk sky, then lifts the tin cup with the new seed toward it, the apple tree glowing behind. greenhouse dome at blue sunset, apple tree behind, red plains and the blue-haloed sun beyond. Keep the bottom 17% of the frame visually quiet for captions. stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition"

Exact diegetic text strings:
- shot 3: `12:00` signal-delay counter.
- shot 15: `NOT CLEARED`.
- Anything else: no text.

## 3. Seedance 2.5 jobs (26 accepted shots + 5 drafts = 31 submissions)

Common settings:
- `model: seedance_2_5`, `mode: omni_reference`, `aspect_ratio: 9:16`, `resolution: 1080p`.
- `duration = gen_duration`: 4 s, or 5 s for the payoff. The 1–3 s holds are cut out of `useful_window` in assembly.
- `generate_audio: false` except shot 17 (diegetic).
- Difficult shots run a 480p `draft: true` first, then are finalized with `draft_job_id` at 1080p.

| Shot | Edited hold | Source | Window | visual_source | Media | Audio | Draft | Action (inside window) |
|---|---|---|---|---|---|---|---|---|
| 1 | 2.53s | 4s | 0.3–3.43s | KEYFRAME_REQUIRED | start_image: kf-shot1 | none | — | newborn avatar in a padded incubator pod opens its button eyes as red dust streaks past the porthole |
| 2 | 2.93s | 4s | 0.3–3.83s | KEYFRAME_REQUIRED | start_image: env:ch1 | none | — | a parent in a grey colony jumpsuit lifts the swaddled newborn as soil trickles on the dome roof |
| 3 | 1.85s | 4s | 0.3–2.75s | KEYFRAME_REQUIRED | start_image: kf-shot3 | none | — | the newborn wails in the foreground while a signal bar crawls across the screen behind |
| 4 | 1.42s | 4s | 0.3–2.32s | REUSE_REFERENCE | image_references: keyframe:shot3 + avatar:stage:newborn | none | — | close on the glowing comms screen: the delay counter ticks from 12:00 as the signal bar crawls; the newborn's tiny wool hand rests at the frame edge |
| 5 | 1.86s | 4s | 0.3–2.76s | REUSE_REFERENCE | image_references: prop:seedcup + avatar:stage:newborn | none | — | a parent's hands lower a dented tin cup of dark soil beside the swaddled newborn, who turns its button eyes toward it |
| 6 | 1.54s | 4s | 0.3–2.44s | REUSE_REFERENCE | image_references: prop:seedcup + avatar:stage:newborn | none | — | tiny wool hand reaches and touches the single apple seed resting on the soil in the tin cup |
| 7 | 2.92s | 4s | 0.3–3.82s | KEYFRAME_REQUIRED | start_image: env:ch2 | none | — | six-year-old avatar steps onto a floor scale whose needle barely moves; classmates giggle behind |
| 8 | 2.94s | 4s | 0.3–3.84s | DIRECT_VIDEO | image_references: avatar:stage:child + env:ch2 | none | yes | the child leaps and floats in a long slow arc over a line of laughing classmates |
| 9 | 1.54s | 4s | 0.3–2.44s | DIRECT_VIDEO | image_references: avatar:stage:child + env:ch2 | none | — | the child in a small orange pressure suit seals a bubble helmet as the airlock light turns from red to green |
| 10 | 2.0s | 4s | 0.3–2.9s | DIRECT_VIDEO | image_references: avatar:stage:child + env:ch2 | none | — | the suited child steps out of the airlock onto the red plain, helmet visor catching the hazy light |
| 11 | 1.78s | 4s | 0.3–2.68s | DIRECT_VIDEO | image_references: avatar:stage:child + env:ch2 | none | — | the suited child tilts its helmet back to look up at the butterscotch noon sky |
| 12 | 1.36s | 4s | 0.3–2.26s | KEYFRAME_REQUIRED | start_image: kf-shot12 | none | — | the suited child stands on the crater rim as the sun sinks and the blue halo spreads |
| 13 | 2.93s | 4s | 0.3–3.83s | KEYFRAME_REQUIRED | start_image: env:ch3 | none | yes | the teen avatar presses a hand to the window as the dust wall swallows the horizon |
| 14 | 2.97s | 4s | 0.3–3.87s | DIRECT_VIDEO | image_references: avatar:stage:teen + env:ch3 | none | — | the teen switches off lamps one by one as the corridor drops into red emergency light |
| 15 | 2.42s | 4s | 0.3–3.32s | DIRECT_VIDEO | image_references: avatar:stage:teen + env:ch3 | none | yes | the teen in a dusty pressure suit shovels drifts away from the greenhouse door |
| 16 | 2.62s | 4s | 0.3–3.52s | REUSE_REFERENCE | image_references: prop:seedcup + avatar:stage:teen | none | — | hard colour flip: after the rust-red storm, a vivid green apple sapling glows under the grow-light in the tin cup as the teen's gloved hand cups it |
| 17 | 2.72s | 4s | 0.3–3.62s | KEYFRAME_REQUIRED | start_image: env:ch4 | none | — | the adult avatar raises a glowing boarding token and grins at the rocket outside |
| 18 | 3.0s | 4s | 0.3–3.9s | DIRECT_VIDEO | image_references: avatar:stage:adult22 + env:ch4 | none | yes | colonists stream toward a boarding gate while the avatar waits in line clutching a bag |
| 19 | 1.62s | 4s | 0.3–2.52s | KEYFRAME_REQUIRED | start_image: kf-shot19 | none | — | the avatar stands in the scanner arch as the panel flashes red and its smile fades |
| 20 | 2.97s | 4s | 0.3–3.87s | DIRECT_VIDEO | image_references: avatar:stage:adult22 + env:ch4 | none | — | in a gravity simulator, the avatar's knees buckle and it grips the handrails, straining |
| 21 | 1.77s | 4s | 0.3–2.67s | REUSE_REFERENCE | start_image: keyframe:shot17 | diegetic | yes | the avatar presses a palm to the window as the rocket rises and the hall trembles |
| 22 | 2.34s | 4s | 0.3–3.24s | KEYFRAME_REQUIRED | start_image: env:ch5 | none | — | the adult avatar walks a row of crops with a watering can, mist drifting in shafts of light |
| 23 | 2.06s | 4s | 0.3–2.96s | REUSE_REFERENCE | image_references: keyframe:shot22 + avatar:stage:adult30 | none | — | the avatar reaches up and picks a red apple from the tree |
| 24 | 1.74s | 4s | 0.3–2.64s | REUSE_REFERENCE | image_references: keyframe:shot1 + avatar:stage:adult30 | none | — | the avatar leans over the incubator as a newborn's hand grips its wool finger |
| 25 | 1.6s | 4s | 0.3–2.5s | REUSE_REFERENCE | image_references: prop:seedcup + avatar:stage:adult30 | none | — | the avatar's hands press an apple seed into soil in a fresh tin cup |
| 26 | 4.42s | 5s | 0.3–5s | KEYFRAME_REQUIRED | start_image: kf-shot26 | none | — | the avatar looks up at a tiny blue dot (Earth) in the dusk sky, then lifts the tin cup with the new seed toward it, the apple tree glowing behind |

Prompt template per shot:
```
{camera}. From {a}s to {b}s: {action}. After that the motion settles and holds. The character keeps its exact design from the reference. Stylized 3D animated film look, single continuous shot, no cuts, no text.
```
Shot 17 appends: "Sound: muffled rocket rumble, window trembling. No speech, no voices, no music."

Batch order:
1. **V0:** a single `generate_video` `get_cost` re-check on one real omni_reference item.
2. **V1:** 5 drafts (shots 8, 13, 15, 18, 21).
3. **V2 + V3:** 12 + 5 non-difficult finals.
4. **V4:** finalize the 5 accepted drafts.

## 4. Narration plan (Seed Audio)

- Model `seed_audio`, voice `bd072316-f77c-588b-b6e5-e46b9b03d008` (preset, Archie (user-selected)), `speech_rate: 75`.
- **5 takes**, one per chapter, via `generate_audio_batch`. The hook rides in the chapter-1 take, followed by a 0.25 s pause before "Day one".
- **Assembly:** in one sandbox call, ffprobe the takes, concatenate them with 0.12 s gaps, and run faster-whisper word timestamps.
- **Speed target:** 3.6–4.2 words/s. The plan estimates 3.97 w/s at 57.4 s.
  - If a take falls outside the target, adjust `speech_rate` ±10 and regenerate it. Never time-stretch.
- **Retiming:** move each edited cut 0.05 s before its clause's first word.
  - Check that every new `dur` still fits its `useful_window` **before** any video is generated.
  - Re-run `validate_plan.py`.
- Narration is generated **before** the Seedance batches, so video windows are locked to real timing.

| Take | Words | Text |
|---|---|---|
| ch1 | 51 | What would happen if you were born on Mars in the year 2100? Day one. You're born under three metres of dirt that blocks radiation. Your first cry, sent by radio, takes twelve minutes to reach Earth. Your parents carried one gift from Earth: an apple seed in a tin cup. |
| ch2 | 45 | Year six. You weigh just over a third of an Earth kid. Every jump in the school tunnel becomes a slow, floating flight. Outside, without a suit, you'd pass out in seconds as your saliva boils. The noon sky is butterscotch. The sunsets glow blue. |
| ch3 | 42 | Year fourteen. A dust storm swallows the whole planet for months. The solar panels go dark. The colony rations every watt. You dig the greenhouse out by hand, sol after sol. Your seed is now a sapling, the only green for kilometres. |
| ch4 | 46 | Year twenty-two. You finally win a seat on the ship to Earth. Launch windows open every twenty-six months. You've waited years. Then the medical scan flashes red. You grew up in Mars gravity. On Earth, you'd feel nearly three times heavier. The ship leaves without you. |
| ch5 | 52 | Year thirty. You run the largest garden on Mars. The seed from Earth is now a tree taller than you. Then a baby is born in the nursery where you were born. You plant a new seed in a tin cup. You were never an Earthling on Mars. You're the first Martian. |
