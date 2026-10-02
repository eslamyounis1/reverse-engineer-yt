# Visual DNA

## 1. The avatar ("you")

**Observed (5/5, High):**

- One stylized, non-photoreal, big-eyed humanoid with a transparent, glassy or skeletal body
  stands in for the viewer. It appears in 96–100% of shots.
- It ages and changes wardrobe every chapter.
- Supporting cast are ordinary generic humans or creatures.

**Inferred function (Medium):** a universal, identity-free "you" that every viewer can project
onto. It stays visually consistent and reads instantly at phone size. It also contrasts with
realistic surroundings, so the eye finds it in every cut.

**Rule:** design an **original** avatar for each video (or one per series) with this recipe. Do
**not** make a glass, translucent or skeleton humanoid, because that is the reference channel's
signature.

| Attribute | Requirement | Original directions (pick or invent) |
|---|---|---|
| Identity | No real face, no human skin likeness, no celebrity resemblance | — |
| Material | One distinctive, readable material that survives every lighting key | carved pale wood marionette · matte ceramic/porcelain doll with seam lines · felt-and-thread plush · living paper-craft origami · smooth river-stone golem · knitted wool figure |
| Eyes | Oversized, expressive, the main emotion carrier (5/5 have large eyes) | glossy bead eyes · glowing ember eyes · painted enamel eyes |
| Silhouette | Distinct at thumbnail size; head ≈ 1/5 of height | — |
| Colour | One accent colour unique to the avatar that never appears in backgrounds | — |
| Evolution | Age, body mass, wardrobe and wear change per chapter; material, eyes and accent stay fixed | infant → child → teen → adult → elder; or clean → worn → scarred → restored |
| Power/wear signal | One visual marker that intensifies at the turn (observed: glowing eyes, chest glow, tattered clothes) | cracks that glow · thread unravelling · ink spreading |

Write the recipe as one line in `plan.avatar.design`, e.g.:
`hand-carved pale birch marionette, oversized glossy black bead eyes, visible wooden joints, single teal scarf as accent`.

## 2. Signature prop (plant → payoff)

- **Observed:** the swirl lollipop appears in 3/5 references, in the first and/or last frame.
  It is a **channel Easter egg, so do not use it.**
- **Rule:** choose one small, colourful, original prop tied to the avatar, e.g. a brass compass,
  a paper crane, a red marble, a tin whistle.
  - It appears in a ch-1 shot (tag `plant`) and in the final shot (tag `payoff`).
  - An optional third appearance in the middle can be an environmental detail (R4 put a prop
    icon in the sky).
- Alternative (R3): the plant is a **constraint** (chains), and the payoff shows it removed.

## 3. Shot grammar

| Scale | Share (observed → target) | Use for |
|---|---|---|
| Wide | 5–47% → **10–30%** | Chapter establishing shots, crowds, landscapes, spectacle (vehicles, arenas, space), wealth or scale premises |
| Medium | 53–70% → **default** | Narrative action; the avatar centred with context behind |
| Medium Close-Up | 0–18% | Emotional reaction with environment, struggle, holding objects |
| Close-Up | 0–18% → **5–15% CU/ECU** | Hands (knife, weaving, fire), eyes in terror, the direct-to-camera turning-point look |
| Extreme Close-Up | 1 shot in R4 | Making an invisible concept visible (a chip in the brain) |

- Change scale on **≥ 2/3 of cuts** (observed 0.54–0.80).
- **Composition:**
  - The avatar is centred or on the central third, in the upper 70% of the frame. Keep the
    bottom 17% clear for captions.
  - A threat or other key subject may take the foreground, with the avatar behind (R2 bear).
  - Behind-the-back framing is for entering the unknown (R3 emperor, R5 raids).
- **Camera** (Medium confidence; the analyser under-reports it):

  | Camera | Use for |
  |---|---|
  | `locked` (default) | Most shots |
  | `low tracking` | Chases and running |
  | `handheld` | Unstable worlds (ships, storms) |
  | `behind follow` | Stealth and arrival |
  | `push-in` | The payoff close-up and turning points |
  | `front-mounted vehicle` | Vehicles |

  Never use a slow drift with no subject motion. Movement comes from the subject first.
- **Transitions:** hard cuts only.

## 4. Environments and lighting

- **Every chapter opens with a new environment AND a new lighting key** (5/5). Within a chapter,
  change the sub-location every 1–2 shots.
- Rotate lighting keys so neighbouring chapters contrast. Observed keys:
  - soft morning;
  - golden hour / sunset;
  - torch or firelight;
  - cold blue storm;
  - neon night;
  - overcast grey;
  - stark sterile blue;
  - red alarm.
- The turn chapter gets the most contrasting key. Examples: bright luxury → night balcony;
  sunny village → burning orange.
- **Global style lock** for all GPT Image 2.5 and Seedance prompts:
  `stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, shallow depth of field, clean readable silhouettes, 9:16 vertical composition`.
  Never mix in photoreal or 2D shots.

## 5. Prompt recipes

### GPT Image 2.5: avatar base sheet (Phase 3)

```
model gpt_image_2_5 · variant flare · quality high · resolution 2k · aspect_ratio 9:16
Character reference sheet on a neutral warm-grey studio backdrop: {avatar.design}.
Three views in one vertical image: full body front (top), three-quarter view (middle),
face close-up showing the oversized {eye spec} (bottom). Consistent proportions, no text,
no logos. {GLOBAL STYLE LOCK}
```

### GPT Image 2.5: stage frame (sunburst edit from AVATAR_REF)

```
model gpt_image_2_5 · variant sunburst · quality high · medias [image_references: AVATAR_REF]
Same character, identical material, eye design, accent colour and proportions style.
Change only: age stage = {stage}, body = {build}, wardrobe = {wardrobe}, wear = {marks}.
Full body, neutral backdrop, 9:16.
```

### GPT Image 2.5: scene keyframe

```
model gpt_image_2_5 · variant flare · quality high (xhigh for hook/payoff) · 9:16
medias [image_references: {stage frame}, image_references: {chapter establishing keyframe}]
{SCALE} shot. {avatar.design} at {stage}, {pose/action at its peak}, positioned {placement}.
{Environment}, {lighting key}. {Foreground/background subject if any}. {Prop if plant/payoff}.
Keep the bottom 17% of the frame visually quiet for captions. No text unless specified:
{diegetic text exact string}. {GLOBAL STYLE LOCK}
```

### Seedance 2.5: shot from keyframe

```
model seedance_2_5 · mode omni_reference · medias [start_image: {keyframe}]
duration 4 · resolution 1080p · aspect_ratio 9:16 · generate_audio false
{Camera move}. Within the first 2 seconds: {single clear action}. {Secondary motion: dust,
sparks, rain, crowd}. The character keeps its exact design from the start image.
Stylized 3D animated film look, no cuts, no text.
```

### Seedance 2.5: shot without keyframe

```
model seedance_2_5 · mode omni_reference
medias [image_references: {stage frame}, image_references: {chapter establishing keyframe}]
duration 4 · resolution 1080p · aspect_ratio 9:16 · generate_audio false
{SCALE} shot of the character from the first reference, in the world of the second reference.
{Camera}. Within the first 2 seconds: {action}. Single continuous shot, no cuts, no text.
```

### Difficult-shot draft loop

1. Submit with `draft: true` (480p).
2. Grab frames at 0.5 / 1.5 / 2.5 s in the sandbox (`ffmpeg -ss … -frames:v 1`) and check:
   identity match, framing, that the action peaks before 2.5 s, and hands, faces and text.
3. If it passes, finalize with `draft_job_id` at 1080p. If it fails, revise the prompt and
   redraft, at most twice before you split the shot.

## 6. Content safety

- Violence is implied or stylized, never graphic. Cut on the strike, not the injury (R5 cut to
  a water splash).
- Historical oppression is shown with dignity, and supporting cast are not caricatured.
- No real people, brands or logos.
