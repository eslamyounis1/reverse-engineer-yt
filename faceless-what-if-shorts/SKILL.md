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
   - Write a new script and design a new avatar, new signature prop and new worlds.
   - Never reproduce reference scripts, distinctive lines, reference premises, the
     glass/skeleton avatar, the swirl-lollipop prop, or any channel branding.
   - No real people: no names, no look-alikes, no allusions such as "the guide looks exactly like him".
2. **Higgsfield MCP is the execution layer.** Every image, video, voice and assembly step goes
   through Higgsfield tools (`generate_image[_batch]`, `generate_video[_batch]`,
   `generate_audio[_batch]`, `jobs_wait`, `sandbox_exec`, `media_upload`/`media_confirm`,
   `video_analysis_create`).
3. **Locked models.** Do not silently substitute a faster or cheaper model.
   - **Images:** `gpt_image_2_5`, `variant: "flare"` by default. Use `variant: "sunburst"` only for
     precise edits that must preserve details, e.g. ageing the avatar while keeping its design.
     `aspect_ratio: "9:16"`. Draft frames at `quality: "medium"`; accepted keyframes at
     `quality: "high"` (or `"xhigh"`/`"max"` for the hook and payoff frames) with `resolution: "2k"`.
   - **Video:** `seedance_2_5`, `aspect_ratio: "9:16"`. Accepted shots at `resolution: "1080p"`.
     For difficult shots, render a `draft: true` 480p version first, inspect it, then finalize
     with `draft_job_id`.
   - If Seedance 2.5 cannot do an operation, explain the limitation to the user **before**
     proposing another model.
4. **Faceless:** no on-camera presenter and no talking head. The narrator is a voice only.
5. Confirm with the user before the first paid generation batch. Show the script and the
   shot-plan summary with `get_cost: true` totals.

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

### Phase 2: Shot plan → `references/pacing.md`, `references/visual-language.md`, `references/retention.md`

Split the script into **one clause per shot** and write `plan.json` (schema below). Then run:

```
python3 faceless-what-if-shorts/scripts/validate_plan.py plan.json
```

Fix every `FAIL` before generating anything. `WARN`s need a one-line justification in
`plan.notes`.

Targets enforced by the validator (from the measurements):

- **Shots:** 20–26.
- **Holds:** mean 2.2–2.8 s; ≥ 85% of shots ≤ 3 s; max 4 s (final shot ≤ 5 s); 1 s only for impact or flash shots.
- **Cut rate:** 3.5–4.5 cuts per 10 s.
- **Chapters:** exactly 5, with onsets at ≈ 4 / 17 / 37 / 57 / 75% (±6 pts). The final chapter is the longest (12–17 s).
- **Shot mix:** Medium-family 60–80%, Wide 10–30%, CU/ECU 5–15%. Shot scale changes on ≥ 2/3 of cuts.
- **Avatar:** in ≥ 95% of shots.
- **Pattern interrupts:** at least one every 15 s.
- **Plant and payoff:** a plant in the first 15% and its payoff in the final shot.

### Phase 3: World lock: avatar, prop, chapter worlds → `references/visual-language.md`

All of these use `gpt_image_2_5` with flare, 9:16, high quality. Batch the calls in Phase 3
with `generate_image_batch`, wait with `jobs_wait`, then show the results once with
`show_generation_by_ids`.

1. **Avatar base sheet.** Design one original stylized avatar using the avatar recipe. Produce
   one image with a full body, a 3/4 view, and a face close-up on a neutral backdrop. Keep its
   job id as `AVATAR_REF`.
2. **Avatar stage frames.** Make one frame per chapter age or condition, edited from
   `AVATAR_REF` with `variant: "sunburst"` and `medias:[{role:"image_references",value:AVATAR_REF}]`.
   Change only age, body, wardrobe and wear. Keep the material, eyes and silhouette identical.
3. **Signature prop.** Make one original prop that appears in the plant shot and the payoff shot.
4. **Chapter establishing keyframes.** Make one per chapter: the avatar stage frame plus the new
   environment and lighting key.

Gate: show the user the avatar sheet before Phase 5. If the avatar drifts between stage frames,
regenerate the drifting frame with sunburst before you go on.

### Phase 4: Narration (audio-locked edit)

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
4. **Retime the plan.** Set each shot's `start`/`dur` from the clause word timestamps: the cut
   lands 0–0.1 s before the clause's first word. Rerun `validate_plan.py`. If a hold now
   exceeds 4 s, split that shot (add a carry-over image) rather than slowing the cut.

### Phase 5: Keyframes, GPT Image 2.5 → `references/visual-language.md` §Prompt recipes

Generate a keyframe only where it adds composition or consistency control:

- the hook frame and the payoff frame (`quality: "xhigh"`);
- chapter establishing shots (already made in Phase 3);
- shots with a foreground/background relationship (a threat in the foreground with the avatar
  behind, or the avatar facing a crowd);
- shots containing diegetic text, UI or signage;
- any shot where the avatar's stage or wardrobe must be exact.

Make each keyframe with `generate_image_batch` (≤ 12 per call). Pass
`medias:[{role:"image_references", value: <stage frame>}, {role:"image_references", value: <chapter establishing keyframe>}]`.

Skip the keyframe for simple motion or carry-over shots. Those go straight to Seedance
`omni_reference` with the same stage frame and chapter keyframe as `image_references`.

### Phase 6: Shots, Seedance 2.5

Make one `generate_video_batch` item per shot (≤ 12 per call) with these settings:

- `model: "seedance_2_5"`, `aspect_ratio: "9:16"`, `duration: 4` (the minimum; use 5 for the
  final shot), `resolution: "1080p"`, `generate_audio: false`.
- With a keyframe: `mode: "omni_reference"`, `medias:[{role:"start_image", value:<keyframe>}]`.
- Without one: `mode: "omni_reference"`, `medias:[{role:"image_references", value:<stage frame>}, {role:"image_references", value:<chapter keyframe>}]`.
- In the prompt, write the action to **peak in the first 2.5 s**, because clips are trimmed to the
  planned hold. Use the camera vocabulary from `references/visual-language.md`.
- **Difficult shots** (crowds, fights, vehicles, transformations, liquids, text):
  1. Submit `draft: true` (480p).
  2. Inspect the frame grabs: subject identity, framing, motion peak, artifacts.
  3. Finalize with `draft_job_id`.
- Wait with `jobs_wait` and display once with `show_generation_by_ids`.

Retry ladder for a failed or rejected shot:

1. Simplify the motion.
2. Remove violent or explicit wording, keeping the intent implied rather than graphic.
3. Regenerate the keyframe.
4. Split the shot into two simpler shots.

### Phase 7: Assembly, Higgsfield sandbox

Build `timeline.json` from the retimed plan: per shot `url`, `in` (the trim in-point, default 0.2),
`dur`, and the optional chapter `label`; plus `narration_url`.

Run the bundled assembler inside **one self-contained** `sandbox_exec`. The sandbox is
ephemeral, so the downloads, assembly, captions and upload all go in the same call.

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
   Use `background:true` if the command will run over 120 s, and poll the log in the very next call.
   `sandbox_exec` commands are capped at 16 000 characters. Encode the files locally with
   `gzip -9c f | base64 -w0`. If the total still exceeds the cap, publish `timeline.json` via
   `media_upload` (type `file`) and `curl` it at the top of the same command.
3. Call `media_confirm` only after HTTP 200.

What goes into the command:

- `script_manifest.json` = `{"blocks":[{"vo_line": "<chapter text>"}, …]}`.
- `assemble_short.py`:
  - trims every clip to its `dur`;
  - scales to 1080×1920 at 30 fps with hard cuts;
  - burns the chapter labels for 1.2 s;
  - lays `narration.wav` over the cut;
  - loudnorms to −14 LUFS;
  - asserts that the video and audio durations match within 0.2 s and prints `RECEIPTS`.
- Subtitle burning follows the Higgsfield `subtitles` workflow, route 2 (continuous narration).
  Gate on `similarity ≥ 0.90` before burning. If Whisper is unavailable, deliver the clean cut
  and say so.

### Phase 8: QC against the learned rules → `references/pacing.md` §QC

1. Run `video_analysis_create({video_input_id: <confirmed media id>})` on the finished Short and
   poll `video_analysis_status`.
2. Save the scenes in the `analysis/raw` JSON format and run
   `python3 faceless-what-if-shorts/scripts/validate_plan.py --from-analysis <file>`.
3. Also extract 6 frames (hook, every chapter start, payoff) in the sandbox and look at them for:
   avatar consistency, caption safe-zone collisions, and AI artifacts (hands, text, faces in crowds).
4. **Regenerate the clearest weak scene:** pick the single worst shot by impact and fix it.
   - Impact order: hook frame > payoff > a chapter opener > any other shot.
   - Problems to look for: avatar drift, a muddy composition, a motion peak that misses the trim
     window, or an artifact.
   - Regenerate it through Phase 5/6, re-assemble, and re-check. Do at most 2 regeneration rounds
     unless the user asks for more.

### Phase 9: Deliver

Give the user:

- the confirmed hosted URL;
- the 1-line premise;
- the QC table with measured vs target values: duration, shots, mean hold, cut rate, chapter
  onsets, words/s, and avatar presence;
- the scene that was regenerated, and why.

Do not publish anywhere unless asked.

## plan.json schema

```json
{
  "title": "working title",
  "premise_type": "lifespan | bounded",
  "target_seconds": 55,
  "avatar": {"name": "internal id", "design": "one-line recipe", "stages": ["infant", "child", "teen", "adult", "elder"]},
  "signature_prop": "original prop",
  "notes": [],
  "chapters": [{"n": 1, "label": "Day one", "world": "environment + lighting key", "event": "rite of passage"}],
  "shots": [
    {"id": 1, "chapter": 0, "start": 0.0, "dur": 2.2,
     "line": "What would happen if you…?",
     "scale": "Wide|Medium|Medium Close-Up|Close-Up|Extreme Close-Up",
     "avatar": true, "avatar_stage": "infant",
     "environment": "...", "camera": "locked|push-in|low tracking|behind follow|orbit|handheld",
     "action": "what visibly happens in the first 2.5 s",
     "keyframe": true, "difficult": false,
     "tags": ["hook", "interrupt", "plant", "payoff", "turn", "carry-over", "montage"]}
  ]
}
```

`chapter: 0` is the hook. Chapters 1–5 follow, and the first shot of each chapter carries its
time-stamp line.

## Files

- `references/hooks.md`: hook formula, premise generator, title/hook bank patterns.
- `references/narrative.md`: 5-chapter beat sheet, word budgets, turn and payoff types, writing rules.
- `references/pacing.md`: timing targets, retiming from narration, QC thresholds.
- `references/visual-language.md`: avatar recipe, shot grammar, environments, prompt recipes for GPT Image 2.5 and Seedance 2.5.
- `references/retention.md`: interrupt menu, plant/payoff, chapter cliffhangers, endings.
- `scripts/validate_plan.py`: hard and soft checks of a plan or a Higgsfield analysis.
- `scripts/assemble_short.py`: sandbox assembler (trim, scale, labels, narration, loudnorm, receipts).
- `examples/example_plan.json`: a complete 21-shot plan for an original premise ("born at the
  bottom of the ocean") that passes the validator with 0 FAIL / 0 WARN. Use it as a format
  reference only; never reuse its content.
