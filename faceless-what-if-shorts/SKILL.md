---
name: faceless-what-if-shorts
description: >-
  Produce a finished, original 9:16 faceless "What would happen if you…?" hypothetical-life
  YouTube Short (50–60 s): one stylized avatar standing in for "you", five time-stamped chapters
  ("Day one" → "Year N" or "Day N"), 2–3 s cuts, escalating stakes, and a reframing payoff.
  Uses Higgsfield MCP end to end: GPT Image 2.5 for keyframes, Seedance 2.5 for video, Seed
  Audio for narration, and the Higgsfield sandbox for assembly and captions. Trigger on "what if
  you" or "what would happen if you" Shorts, hypothetical life-simulation Shorts, "day one / year
  ten" story Shorts, or requests to make a video in this faceless what-if format, with or
  without a topic.
---

# faceless-what-if-shorts

This Skill turns a premise (or no premise) into a complete, captioned 9:16 Short. The user never
writes scene prompts; you do.

Every rule below comes from scene-by-scene Higgsfield analysis of five reference Shorts. The
numbers are measured targets, not taste. Evidence and confidence levels are in
`references/*.md`. Read the reference file named at each phase before you do that phase.

## Non-negotiables

1. **Original content only.**
   - Write a new script and design one new avatar, a new signature prop and new worlds.
   - Never reproduce reference scripts, distinctive lines, reference premises, the
     glass/translucent/skeleton avatar look, the swirl-lollipop prop, or any channel branding.
     `validate_plan.py` fails on that design language.
   - No real people: no names, no look-alikes, no allusions such as "the guide looks exactly like him".
2. **Higgsfield MCP is the execution layer.** Every image, video, voice and assembly step goes
   through Higgsfield tools (`generate_image[_batch]`, `generate_video[_batch]`,
   `generate_audio[_batch]`, `jobs_wait`, `sandbox_exec`, `media_upload`/`media_confirm`,
   `video_analysis_create`).
3. **Locked models.** Do not replace either model unless it is technically impossible.
   - **Images:** `gpt_image_2_5`, `variant: "flare"` by default, `aspect_ratio: "9:16"`.
     - Use `variant: "sunburst"` only for precise edits that must preserve details, e.g. ageing
       the approved avatar.
     - Accepted frames use `quality: "high"`, or `"xhigh"` for the hook and payoff, at
       `resolution: "2k"`.
   - **Video:** `seedance_2_5`, `aspect_ratio: "9:16"`. Every accepted shot is `resolution: "1080p"`.
     - Drafts (`draft: true`, 480p) are only for inspection. Finalize them with `draft_job_id`
       at 1080p.
   - **Final output:** 9:16, 1080×1920.
   - If Seedance 2.5 cannot technically do an operation, explain the limitation to the user
     **before** proposing another model. Never switch silently.
4. **Faceless:** no on-camera presenter and no talking head. The narrator is a voice only.
5. **No paid job before an approved cost preflight** (Phase 3). The first paid job is the
   avatar reference, so the gate comes before it.

## Execution rules

These apply on top of the measured channel rules and do not change them.

### E1. Seedance minimum clip duration: generate long, edit short

- The learned rhythm needs final holds of 1–3 s (≤ 4 s, final shot ≤ 5 s). Seedance 2.5
  generates 4–30 s.
- Never ask Seedance for a 1–3 s clip.
  - Generate every shot at `gen_duration` ≥ 4 s: 4 s by default, 5 s for the final shot, and
    5–6 s when the action needs a run-up.
  - Design the useful action to happen inside a planned `useful_window: [a, b]` of that
    source clip, with `a` ≥ 0.2 s (the first frames often settle) and `b − a` ≥ the edited hold.
  - Assembly trims each clip to `[a, a + dur]`.
- `dur` is the **final edited hold**. All pacing rules and every `validate_plan.py` pacing
  check use `dur`, never `gen_duration`.
- The Seedance prompt must place the action in the window, e.g. "Between 0.3 s and 2.5 s the
  character…; afterwards the motion settles."
- If the action lands outside the window, move `useful_window` (re-trim, which is free) before
  you regenerate.

### E2. Audio policy: narration owns the soundtrack

- Narration is generated separately with Seed Audio (`seed_audio`).
- Every Seedance shot uses `generate_audio: false` by default.
- Set `generate_audio: true` **only** on shots marked `"audio": "diegetic"` with an
  `audio_note`, e.g. "hull groan sells the pressure interrupt". Use it only when the sound adds
  meaning (impact beats, a silent SFX beat, environmental tension), never for general ambience.
- Assembly drops all clip audio except diegetic shots. Those are attenuated (`diegetic_db`,
  default −20 dB), sidechain-ducked under the narration, and the receipts must show the bed
  peaking ≥ 6 dB below the narration.
- Never let generated speech, singing or music from a clip reach the mix. If a diegetic clip
  contains voices or music, set it back to `"audio": "none"`.

### E3. Cost preflight: single tools only, then user approval

- Verified from the tool schemas: `generate_image`, `generate_video` and `generate_audio`
  accept `get_cost: true`. The `*_batch` tools **reject** it.
- So the preflight prices each **distinct configuration once** with the single tool and
  multiplies by job counts (Phase 3).
- If a preflight call returns no price, or the tool rejects `get_cost` for a configuration,
  report that line as **unknown**. Never guess a price, and do not proceed until the user
  accepts the unknown.

### E4. One original avatar, reference-locked

- Design **one** original recurring faceless avatar per Short (`references/visual-language.md` §1).
- Store its full visual spec in `plan.avatar.spec`: silhouette, proportions, materials,
  clothing, non-branded identifying features, and per-chapter `stage_changes` (age, clothing,
  state for chapters 1–5).
- Generate the avatar reference with GPT Image 2.5 (flare) and get the user's approval. Store
  `plan.avatar.reference.job_id`.
- Derive the stage frames from that reference with **sunburst** edits. Change only
  age, clothing and state; keep the silhouette, materials, eyes and identifying features.
- From then on, every shot with the avatar in frame passes the approved reference or its stage
  frame as `image_references` (`refs` in the plan starts with `avatar:`). Do not rely on
  re-describing the character in text.

### E5. Keyframe policy: control only where it pays

Every shot carries `visual_source`:

| Value | Use when | What is generated |
|---|---|---|
| `KEYFRAME_REQUIRED` | Composition, avatar identity, environment design or continuity needs control: hook, payoff, chapter openers, foreground/background compositions, crowds with an isolated avatar, diegetic text/UI, exact wardrobe or stage moments. Give a `keyframe_reason`. | GPT Image 2.5 keyframe, then Seedance with `start_image` |
| `DIRECT_VIDEO` | Seedance can produce a clean shot from the references alone (simple action, single subject, a known environment) | Seedance `omni_reference` with avatar stage + environment refs, no new image |
| `REUSE_REFERENCE` | An existing avatar, environment, prop or keyframe already gives the continuity needed (same place, a return to an earlier frame, a prop close-up). Name it in `reuse_of`, e.g. `keyframe:shot1`, `prop:compass`. | No new image; Seedance with the named existing reference |

Do not keyframe every shot. The validator warns above 60% `KEYFRAME_REQUIRED`, and warns if
the hook or payoff is not keyframed.

## Pipeline

### Phase 0: Intake (one message, sensible defaults)

Ask only what is missing. Defaults:

| Setting | Default |
|---|---|
| Duration | 55 s |
| Narration language | English |
| Voice | Calm-intense adult narrator from `list_voices` |
| Caption look | `bold --font-key tiktok` |
| On-screen chapter labels | On |
| Music bed | None (Higgsfield has no general music model; use a bed only if the user supplies one) |

If no topic is given, propose 3 premises built with `references/hooks.md` §Premise generator and
let the user pick. In a headless run, take the strongest one.

### Phase 1: Premise, research and script → `references/hooks.md`, `references/narrative.md`

1. Classify the premise:
   - **Lifespan** ("born as / raised by"): Day one → Year a…d.
   - **Bounded duration** ("stranded for N days / 24 hours on…"): Day/Hour 1…N.
2. **Research** when the premise touches history, science, geography, medicine, survival or
   law. Use WebSearch/WebFetch and collect 6–10 concrete, checkable details. Hypothetical events
   may be invented; facts about real places, eras and physics must be correct. Keep a
   `sources` list in the manifest.
3. Write the script with the beat sheet in `references/narrative.md`:
   - hook question (10–14 words) followed by "Day one";
   - 5 chapters with their word budgets;
   - the turn in chapter 4 or 5;
   - a reframing payoff line;
   - no CTA.
4. **Word budget** = target seconds × 3.9 (range 3.6–4.2 words/s). For 55 s that is ≈ 215 words
   (190–235).

### Phase 2: Shot plan and avatar spec → `references/pacing.md`, `references/visual-language.md`, `references/retention.md`

1. Split the script into **one clause per shot** and write `plan.json` (schema below). Every
   shot needs:
   - the edited hold `dur`;
   - the source clip spec `gen_duration` + `useful_window` (E1);
   - `visual_source` (E5);
   - `refs`;
   - `audio` (E2).
2. Write `plan.avatar.spec` (E4) and choose the signature prop.
3. Run:
   ```
   python3 faceless-what-if-shorts/scripts/validate_plan.py plan.json
   ```
   Fix every `FAIL`. `WARN`s need a one-line justification in `plan.notes`.

Measured targets enforced on **final edited** durations:

- **Shots:** 20–26.
- **Holds:** mean 2.2–2.8 s; ≥ 85% of shots ≤ 3 s; max 4 s (final shot ≤ 5 s); 1 s only for impact or flash shots.
- **Cut rate:** 3.5–4.5 cuts per 10 s.
- **Chapters:** exactly 5, with onsets at ≈ 4 / 17 / 37 / 57 / 75% (±6 pts). The final chapter is the longest (12–17 s).
- **Shot mix:** Medium-family 60–80%, Wide 10–30%, CU/ECU 5–15%. Shot scale changes on ≥ 2/3 of cuts.
- **Avatar:** in ≥ 95% of shots.
- **Pattern interrupts:** at least one every 15 s.
- **Plant and payoff:** a plant in the first 15% and its payoff in the final shot.

### Phase 3: Cost preflight and approval gate (before ANY paid job)

1. Run `python3 faceless-what-if-shorts/scripts/cost_plan.py plan.json > preflight.json`.
   It lists every distinct priced configuration:
   - **image:** avatar reference, stage edits, prop, chapter establishing frames,
     `KEYFRAME_REQUIRED` keyframes, and hook/payoff at xhigh;
   - **video:** per source duration × 1080p final / 480p draft × audio on/off;
   - **narration:** one Seed Audio take per chapter, priced with its real text.
2. For each entry, call the **single** tool it names with its `params` (which include
   `get_cost: true`): `generate_image` for images, `generate_video` for video,
   `generate_audio` for narration.
   - Write the returned unit costs to `prices.json` as `{key: cost}`.
   - The video price probe uses `mode: "t2v"` because no reference media exist yet. Phase 8
     re-checks one real `omni_reference` item.
3. Run `python3 faceless-what-if-shorts/scripts/cost_plan.py plan.json --prices prices.json --write`.
4. Show the user:
   ```
   estimated image cost      …
   estimated video cost      …
   estimated narration cost  …
   ESTIMATED TOTAL           …   (+20% retry contingency shown separately)
   ```
   Also show `balance` if they want it. Then **ask for approval**.
5. Only after an explicit yes, set `plan.cost_preflight.approved_by_user = true`. Then
   `validate_plan.py plan.json --gate` must pass before any paid submission.
   - Later, if the plan grows (more shots, regeneration rounds) by more than the
     contingency, re-preflight and re-ask.

### Phase 4: Avatar lock and world references (GPT Image 2.5) → `references/visual-language.md`

1. **Avatar reference.** Use `generate_image` with flare, high, 2k, 9:16 and the avatar sheet
   recipe built from `plan.avatar.spec`. Show it to the user.
   - On approval, store `avatar.reference.job_id` and set `approved_by_user: true`.
   - If it is rejected, revise the spec and regenerate. This stays inside the contingency;
     re-ask if exceeded.
2. **Stage frames.** Use `generate_image_batch`, one sunburst edit per `stage_changes` entry,
   with `medias:[{role:"image_references", value:<avatar reference job id>}]`.
   - Store the results in `avatar.reference.stage_refs`.
   - Regenerate any frame that drifts in silhouette, material, eyes or identifying features.
3. **Signature prop** and **5 chapter establishing frames** (flare). Each establishing frame
   passes its chapter's stage ref as `image_references`.
4. Gate: `validate_plan.py plan.json --gate-keyframes` must pass before Phase 6.
5. Batch the calls, wait with `jobs_wait`, and show the results once with `show_generation_by_ids`.

### Phase 5: Narration (audio-locked edit)

1. **Generate the narration.** Use `generate_audio_batch` with `model: "seed_audio"`, one request
   per chapter (5 requests), with the chosen `voice_type` + `voice_id`. Start at `speech_rate: 25`.
   The hook goes in the chapter-1 take, followed by a 0.25 s pause before "Day one".
2. **Measure.** In one `sandbox_exec` call:
   - Download the takes and measure them with `ffprobe`.
   - Concatenate them with 0.12 s gaps into `narration.wav`.
   - Run faster-whisper (`small`) word timestamps.
   - Print the words per second.
3. **Tune the speed.** If the rate is outside 3.6–4.2 w/s, adjust `speech_rate` by ±10 and
   regenerate the takes that are off. Never time-stretch the audio.
4. **Retime the plan.** Set each shot's edited `start`/`dur` from the clause word timestamps:
   the cut lands 0–0.1 s before the clause's first word.
   - If a hold now exceeds 4 s, split the shot (add a carry-over image) rather than slowing it.
   - Re-check that `useful_window` still covers the new `dur`. Widen it, or raise
     `gen_duration`, before any video is generated.
   - Rerun `validate_plan.py`.

### Phase 6: Scene keyframes (GPT Image 2.5, `KEYFRAME_REQUIRED` only) → `references/visual-language.md` §5

- Use `generate_image_batch` (≤ 12 per call) for `KEYFRAME_REQUIRED` shots that are not already
  covered by a Phase-4 establishing frame:
  - flare, 9:16, high, 2k;
  - xhigh for the hook and payoff;
  - `medias:[{role:"image_references", value:<avatar stage ref>}, {role:"image_references", value:<chapter establishing frame>}]`.
- `DIRECT_VIDEO` and `REUSE_REFERENCE` shots get **no** new image.
- A chapter-opener shot whose keyframe *is* its Phase-4 establishing frame sets
  `"keyframe_is_establishing": true`. It is not generated again, and `cost_plan.py` does not
  bill it twice.

### Phase 7: Shots (Seedance 2.5)

One `generate_video_batch` item per shot (≤ 12 per call):

- **Settings:** `model: "seedance_2_5"`, `aspect_ratio: "9:16"`, `resolution: "1080p"`,
  `duration: <gen_duration>` (≥ 4).
- **Audio:** `generate_audio: false`, or `true` only for `"audio": "diegetic"` shots.
- **Media by `visual_source`:**
  - `KEYFRAME_REQUIRED`: `mode: "omni_reference"`, `medias:[{role:"start_image", value:<keyframe>}]`.
  - `DIRECT_VIDEO`: `mode: "omni_reference"`, `medias:[{role:"image_references", value:<avatar stage ref>}, {role:"image_references", value:<chapter establishing frame>}]`.
  - `REUSE_REFERENCE`: `mode: "omni_reference"`, plus the avatar stage ref. Set the shot's
    `reuse_mode`:
    - `"start_image"`: only when the reused frame already shows the **same avatar stage and
      composition**;
    - `"image_references"` otherwise, e.g. returning to an earlier location at a later age.
      This keeps a newborn-era frame from opening an adult-era shot.
- **Prompt:** put the action inside `useful_window` (E1) and use the camera vocabulary from
  `references/visual-language.md`. Diegetic shots also describe the sound and add "no speech,
  no music".
- **Price re-check:** before the first batch, call `generate_video` once with `get_cost: true`
  on one real `omni_reference` item. If its unit price differs from the t2v probe by more than
  10%, update `prices.json`, re-run `cost_plan.py`, and re-ask the user.
- **Difficult shots** (crowds, fights, vehicles, transformations, liquids, text):
  1. Submit `draft: true` (480p).
  2. In the sandbox, grab frames inside `useful_window` and inspect identity, framing, action
     timing and artifacts.
  3. Finalize the accepted draft with `draft_job_id` at 1080p.
- Wait with `jobs_wait` and display once with `show_generation_by_ids`.

Retry ladder for a failed or rejected shot:

1. Re-trim by moving `useful_window` (free).
2. Simplify the motion.
3. Remove violent or explicit wording, keeping the intent implied rather than graphic.
4. Regenerate the keyframe.
5. Split the shot into two simpler shots.

### Phase 8: Assembly (Higgsfield sandbox)

Build `timeline.json` from the retimed plan. Per shot:

- `url` (accepted 1080p result);
- `in = useful_window[0]`;
- `dur` (the edited hold);
- `gen_duration`;
- `diegetic` (true only for `"audio": "diegetic"`);
- optional `diegetic_db`;
- optional chapter `label`.

Plus `narration_url`.

Run everything inside **one self-contained** `sandbox_exec`. The sandbox is ephemeral, so the
downloads, assembly, captions and upload all go in the same call.

1. Call `media_upload({filename:"final.mp4", content_type:"video/mp4"})` first and keep the `upload_url`.
2. Run this command:
   ```
   set -e; mkdir -p wi && cd wi
   printf '%s' '<gzip+base64 of scripts/assemble_short.py>' | base64 -d | gunzip > assemble_short.py
   printf '%s' '<gzip+base64 of timeline.json>' | base64 -d | gunzip > timeline.json
   printf '%s' '<gzip+base64 of script_manifest.json>' | base64 -d | gunzip > script_manifest.json
   python3 assemble_short.py timeline.json --out final_clean.mp4
   bash ${HF_WORKFLOWS}/subtitles/scripts/fetch_fonts.sh
   python3 ${HF_WORKFLOWS}/subtitles/scripts/audio_to_captions.py narration.wav --srt caps.srt --script script_manifest.json --language en
   python3 ${HF_WORKFLOWS}/subtitles/scripts/subtitle_paper_burn.py --in final_clean.mp4 --srt caps.srt --out final.mp4 --style bold --font-key tiktok
   ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4
   [ -s final.mp4 ] && curl -f -X PUT --upload-file final.mp4 '<upload_url>' -w '%{http_code}\n'
   ```
   - Use `background:true` if the command will run over 120 s, and poll the log in the very next call.
   - `sandbox_exec` commands are capped at 16 000 characters. Encode the files locally with
     `gzip -9c f | base64 -w0`. If the total still exceeds the cap, publish `timeline.json` via
     `media_upload` (type `file`) and `curl` it at the top of the same command.
3. Call `media_confirm` only after HTTP 200.

What goes into the command:

- `script_manifest.json` = `{"blocks":[{"vo_line": "<chapter text>"}, …]}`.
- `assemble_short.py`:
  - trims each ≥ 4 s source clip to `[in, in+dur]`, and **fails** if the window overruns the
    clip (no freeze-frame padding);
  - scales to 1080×1920 at 30 fps with hard cuts;
  - burns the chapter labels for 1.2 s;
  - drops non-diegetic clip audio, and ducks diegetic audio under the narration;
  - loudnorms to −14 LUFS;
  - asserts that the video and audio durations match the plan within 0.2 s;
  - prints `RECEIPTS` (per-shot source → edited durations, diegetic levels).
- Subtitle burning follows the Higgsfield `subtitles` workflow, route 2 (continuous narration).
  Gate on `similarity ≥ 0.90` before burning. If Whisper is unavailable, deliver the clean cut
  and say so.

### Phase 9: QC against the learned rules → `references/pacing.md` §QC

1. Run `video_analysis_create({video_input_id: <confirmed media id>})` on the finished Short and
   poll `video_analysis_status`.
2. Save the scenes in the `analysis/raw` JSON format and run
   `python3 faceless-what-if-shorts/scripts/validate_plan.py --from-analysis <file>`.
   - This measures the **edited** cut, which is what the rules govern.
3. Also extract 6 frames (hook, every chapter start, payoff) in the sandbox and look at them for:
   - avatar consistency against the approved reference;
   - caption safe-zone collisions;
   - AI artifacts (hands, text, faces in crowds).
4. **Regenerate the clearest weak scene:** pick the single worst shot by impact and fix it.
   - Impact order: hook frame > payoff > a chapter opener > any other shot.
   - Problems to look for: avatar drift, a muddy composition, an action peak outside the trim
     window, or an artifact.
   - Try a re-trim first. Otherwise regenerate it through Phase 6/7 within the approved
     contingency, re-assemble, and re-check.
   - Do at most 2 regeneration rounds unless the user asks for more.

### Phase 10: Deliver

Give the user:

- the confirmed hosted URL;
- the 1-line premise;
- the QC table with measured vs target values: duration, shots, mean edited hold, cut rate,
  chapter onsets, words/s, and avatar presence;
- the scene that was regenerated, and why;
- actual vs estimated credits.

Do not publish anywhere unless asked.

## plan.json schema

```json
{
  "title": "working title",
  "premise_type": "lifespan | bounded",
  "target_seconds": 55,
  "avatar": {
    "name": "internal id",
    "design": "one-line recipe",
    "spec": {
      "silhouette": "...", "proportions": "...", "materials": "...", "clothing": "...",
      "identifying_features": ["non-branded feature", "..."],
      "stage_changes": [{"chapter": 1, "age": "...", "clothing": "...", "state": "..."}]
    },
    "reference": {"job_id": null, "approved_by_user": false, "stage_refs": {"newborn": null}}
  },
  "signature_prop": "original prop",
  "cost_preflight": {"image": null, "video": null, "narration": null, "total": null,
                     "currency": "credits", "approved_by_user": false, "lines": []},
  "notes": [],
  "chapters": [{"n": 1, "label": "Day one", "world": "environment + lighting key", "event": "rite of passage"}],
  "shots": [
    {"id": 1, "chapter": 0, "start": 0.0, "dur": 2.2,
     "gen_duration": 4, "useful_window": [0.3, 3.0],
     "line": "What would happen if you…?",
     "scale": "Wide|Medium|Medium Close-Up|Close-Up|Extreme Close-Up",
     "avatar": true, "avatar_stage": "newborn",
     "visual_source": "KEYFRAME_REQUIRED|DIRECT_VIDEO|REUSE_REFERENCE",
     "keyframe_reason": "required for KEYFRAME_REQUIRED",
     "reuse_of": "required for REUSE_REFERENCE, e.g. keyframe:shot1 | prop:compass | env:ch2",
     "refs": ["avatar:stage:newborn", "env:ch1"],
     "audio": "none|diegetic", "audio_note": "required when diegetic",
     "environment": "...", "camera": "locked|push-in|low tracking|behind follow|orbit|handheld",
     "action": "what visibly happens inside useful_window",
     "difficult": false,
     "tags": ["hook", "interrupt", "plant", "payoff", "turn", "carry-over", "montage"]}
  ]
}
```

- `chapter: 0` is the hook. Chapters 1–5 follow, and the first shot of each chapter carries its
  time-stamp line.
- `start`/`dur` are positions in the **edited** timeline. `gen_duration`/`useful_window`
  describe the Seedance source clip.

## Files

- `references/hooks.md`: hook formula, premise generator, title/hook bank patterns.
- `references/narrative.md`: 5-chapter beat sheet, word budgets, turn and payoff types, writing rules.
- `references/pacing.md`: timing targets, retiming from narration, source-clip trimming, QC thresholds.
- `references/visual-language.md`: avatar spec and reference lock, shot grammar, environments, prompt recipes for GPT Image 2.5 and Seedance 2.5.
- `references/retention.md`: interrupt menu, plant/payoff, chapter cliffhangers, endings.
- `scripts/validate_plan.py`: pacing (edited durations), source-clip, keyframe, audio, avatar and
  originality checks; `--gate` / `--gate-keyframes` production gates; `--from-analysis` QC.
- `scripts/cost_plan.py`: enumerates priced configurations for single-tool `get_cost` preflight
  and totals image / video / narration / total.
- `scripts/assemble_short.py`: sandbox assembler (window trim, scale, labels, narration,
  diegetic ducking, loudnorm, receipts).
- `examples/example_plan.json`: a complete 21-shot plan for an original premise ("born at the
  bottom of the ocean") that passes the validator with 0 FAIL / 0 WARN. Use it as a format
  reference only; never reuse its content.
