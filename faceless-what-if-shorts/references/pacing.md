# Pacing DNA

All values were measured from 5 reference Shorts via Higgsfield scene analysis (±0.5 s timing
resolution). "Target" is what this Skill enforces. "Observed" is the min–max range (mean) across
the references.

## Targets

| Metric | Observed min–max (mean) | Target | Validator |
|---|---|---|---|
| Duration | 45–64 s (55.4) | 50–60 s; default 55 | FAIL outside 45–64 |
| Shots | 15–27 (21.4) | 20–26 @55 s (scale with duration: ≈ 0.4 shots/s) | FAIL < 15 or > 30 |
| Mean hold | 2.15–3.33 s (2.68) | 2.2–2.8 s | FAIL > 3.3; WARN outside target |
| Median hold | 2–3 s | 2–3 s | — |
| Shots ≤ 3 s | 67–96% (87) | ≥ 85% | FAIL < 67; WARN < 85 |
| Longest hold | 4–5 s | ≤ 4 s (final shot ≤ 5 s) | FAIL above |
| Shortest hold | 1–2 s | ≥ 1 s; holds < 1.5 s only on `interrupt`/`montage`/flash shots | WARN |
| Cuts / 10 s | 2.8–4.5 (3.7) | 3.5–4.5 | WARN outside |
| Hook line | 1–3 s, 10–14 words | ≤ 2.5 s, 10–14 words | FAIL > 3 s or outside 9–15 words |
| First time stamp | 1.7–3.0 s | 1.5–3.0 s | FAIL outside |
| Spoken words | 197–233 (212) | 3.6–4.2 w/s × duration | WARN outside |
| Words / shot | 8.6–14 mean; max 13–25 | 8–14; ≤ 16 | WARN > 16 |
| Chapter onsets (% runtime) | 3–5 / 14–20 / 31–42 / 50–63 / 71–80 | 4 / 17 / 37 / 57 / 75, each ±6 | FAIL > ±10; WARN > ±6 |
| Final chapter length | 12–17 s | 12–17 s | WARN outside |
| Shots per chapter | 3.0–5.4 | 3–6 | WARN outside |

## Edited holds vs Seedance source clips

- Every duration in this file is a **final edited hold** (`dur`), measured on the finished cut.
- Seedance 2.5 generates ≥ 4 s per clip, so each shot is generated longer (`gen_duration`,
  4 s by default and 5 s for the final shot) and trimmed in assembly to `useful_window[0]` +
  `dur`.
- The validator checks pacing on `dur` only. It separately checks that `gen_duration` is 4–30 s
  and that `useful_window` fits inside the source clip and covers `dur`.
- After narration retiming, confirm each new `dur` still fits its `useful_window`. Widen the
  window, or raise `gen_duration`, **before** generating video.

## Narration speed

- Observed 3.36–4.53 words/s (mean 3.87), about 200–270 wpm. That is faster than default TTS.
- With `seed_audio`, start at `speech_rate: 25`. Measure words/s on the concatenated
  narration with Whisper. Adjust ±10 per iteration until it sits in 3.6–4.2.
- **Never time-stretch** the audio (no `atempo`). Regenerate instead.
- Pauses:
  - 0.2–0.3 s after the hook question;
  - 0.12 s between chapter takes;
  - optional 0.5–1 s silence before the final line, or a 1–3 s held tableau after it (R5).

## Audio-locked retiming (do this after narration exists)

1. Run Whisper word timestamps on `narration.wav`.
2. For each shot, find the first word of its `line`. Set `start = word.start − 0.05`
   (clamp ≥ 0).
3. Set `dur = next_shot.start − start`. The final shot gets `dur = narration_end − start + tail`,
   with `tail` 0.8–2.5 s.
4. Carry-over shots (`line` empty or a continuation) split their parent clause's time at a
   natural comma or the midpoint.
5. If any `dur > 4.0` (or > 5.0 for the final shot), insert a carry-over shot. Do not stretch.
   If a `dur` grows past its `useful_window`, widen the window or raise `gen_duration`.
6. If any `dur < 1.0`, merge it with a neighbour, unless it is tagged `interrupt` (an impact).
7. Rerun `validate_plan.py`.

## Montage rule

When narration describes repetition or variety ("again and again", "sometimes… sometimes…",
"one fight, then another"), cut 2–3 shots of 1–1.5 s inside that one clause (R3). Tag them
`montage`.

## QC on the finished Short

1. Run `video_analysis_create` on the uploaded final. Convert its scenes to the
   `analysis/raw/*.json` format: `ref`, `video_id`, `timestamp_convention`, and
   `scenes[{n,start,end,shot,audio,visual}]`. Use `"exclusive"` when each `end` equals the next
   `start`; use `"inclusive"` when the next start is `end + 1`.
2. Run `python3 scripts/validate_plan.py --from-analysis final_analysis.json`.
3. The Short passes when there are no FAILs and ≤ 4 WARNs. Four of the five references meet
   this bar in analysis mode; R1, the slowest and widest, has 9 WARNs.
   - The analyser may merge quick cuts, so a slightly low cut count alone is not a FAIL if the
     plan validated.
   - If the analyser reports the avatar absent or changed in a shot, treat that shot as a
     regeneration candidate.
