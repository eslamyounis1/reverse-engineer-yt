# Cross-Reference Evidence & Production DNA — Helix² faceless "What if" Shorts

Written **after** the five independent analyses in `references/R1…R5`.
All numbers come from `python3 analysis/metrics.py`, computed from the Higgsfield scene data in `raw/`.

| Ref | Video | Premise type | Duration | Scenes |
|---|---|---|---|---|
| R1 | TrU_nSJeu0Q | Lifespan — raised in extreme wealth | 50 s | 15 |
| R2 | FEPc8jsf_Wc | Bounded survival — 5 days in wilderness | 60 s | 22 |
| R3 | I9vWSCiumKo | Lifespan — born into slavery, historical | 45 s | 16 |
| R4 | L8pd3-SkbW8 | Lifespan — born in the far future | 58 s | 27 |
| R5 | 786iLphSIMI | Lifespan — raised by a dangerous tribe | 64 s | 27 |

## Method and limits (read before trusting the numbers)

- **Source:** Higgsfield `video_analysis_create`, one job per video. Three jobs stalled in the queue and were resubmitted with the `/shorts/` URL. All five completed.
- **Timing resolution:** timestamps are whole seconds, so each scene duration is ±0.5 s and each chapter onset ±1 s.
- **Shot splitting:** the analyser sometimes merges fast montage cuts into one "scene". R3 has ≥ 3 such merged cuts, so its scene counts and cut rates are **lower bounds**.
- **Words/second:** computed from the analyser's transcript and timing. Treat it as ±10%.
- **Not measured:** subtitle styling, music and SFX design, and camera moves are only partly reported. Rules about these are marked **Low** or **Medium** confidence.
- **Ignored:** the analyser's `label` field (e.g. "Product Selling Points") is an ad-template taxonomy and is not meaningful here.

---

## 1. Evidence table: what recurs

| Pattern | R1 | R2 | R3 | R4 | R5 | Support | Status |
|---|---|---|---|---|---|---|---|
| Hook is a 2nd-person "What (would happen) if you…?" question | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Exact opener "What would happen if you…" | ✔ | ✔ | ✔ | ✔ | "What if you…" | 4/5 | Channel rule (variant allowed) |
| Hook ≤ 3 s, 10–14 words | 2 s / 10 w | 3 / 14 | 2 / 13 | 1 / 11 | 3 / 11 | **5/5** | Channel rule |
| Frame 1 already shows the avatar *inside* the premise | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| "Day one" is the first narration beat after the hook (1.7–3.0 s) | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Exactly 5 time-stamped chapters | 5 | 5 | 5 | 5 | 5 | **5/5** | Channel rule |
| Chapter units: "Day one" → "Year N" (lifespan) | ✔ | Days only | ✔ | ✔ | ✔ | 4/5 | Rule, chosen by premise type |
| Chapter units: "Day 1…Day N" (bounded duration) | | ✔ | | | | 1/5 | Topic-specific variant |
| Time gaps between chapters widen | 10→20→30→40 | equal | 5→15→25→30 | 5→18→35→80 | 3→10→15→20 | 4/5 | Tendency |
| 2nd-person, present-tense narration throughout | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| One stylized, translucent/skeletal big-eyed avatar = "you" | glass | skeleton | glass | glowing | pale skeletal | **5/5** | Channel rule (the design itself is branding, so **don't copy it**) |
| Avatar in frame in ≥ 96% of scenes | 15/15 | 21/22 | 16/16 | 26/27 | 27/27 | **5/5** | Channel rule |
| Avatar's age, body or costume changes each chapter | ✔ | clothes tatter | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Supporting cast is generic and unnamed (staff, guards, tribe, family) | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| New environment or lighting at every chapter start | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Medium shot is the most common scale | 53% | 59% | 56% | 63% | 70% | **5/5** | Channel rule |
| Hard cuts only (no stylised transitions reported) | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Rule (Medium conf.: analyser may under-report) |
| Recurring signature prop (swirl lollipop) appears early and/or late | ✔ (first + last frame) | — | — | ✔ (incubator + sky icon) | ✔ (scene 4 + last frame) | 3/5 | Channel signature, so **replace with an original prop** |
| Early constraint/object returns as the payoff image | lollipop | — | chains | — | lollipop | 3/5 | Rule |
| Stakes escalate every chapter | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Tonal or scale "turn" lands in chapter 4–5 (≥ 50% runtime) | Yr 30 loneliness (60%) | Day 4 terror (63%) | Yr 25 arena (53%) | Yr 80 simulation (71%) | Yr 20 soldiers (78%) | **5/5** | Channel rule |
| Final line reframes the premise (moral, reversal, or twist) | "Purpose." | meta joke | freedom | "someone's experiment" | "never the one who needed saving" | 4/5 reframe + 1/5 comic | Channel rule |
| No spoken CTA (subscribe/follow) | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Pattern interrupt roughly every 8–15 s | ✔ | ✔ | ✔ | ✔ | ✔ | **5/5** | Channel rule |
| Comedic deflation lines inside spectacle | — | meta ending | — | ✔ (3×) | — | 2/5 | Optional tendency |
| 1 s flash-forward inside the hook | — | — | — | ✔ | — | 1/5 | Uncertain / optional |
| Silent beat (SFX or music only) before/at the end | — | — | — | — | ✔ | 1/5 | Optional |
| Diegetic on-screen text (HUD, sky sign, countdown) | — | — | — | ✔ | — | 1/5 | Topic-specific |
| On-screen chapter labels ("Day 3", "Year 30") | ✔ | ✔ | not reported | not reported | not reported | 2/5 reported | Probable rule (Medium, under-reported) |

## 2. Quantified pacing (n = 5)

| Metric | Min | Max | Mean | Rule derived |
|---|---|---|---|---|
| Duration | 45 s | 64 s | 55.4 s | **Target 50–60 s**, hard bounds 45–64 s |
| Scenes | 15 | 27 | 21.4 | **20–26 scenes** for 55 s (fewer only if wide spectacle dominates) |
| Mean scene hold | 2.15 s | 3.33 s | 2.68 s | **Mean hold 2.2–2.8 s** |
| Median hold | 2 s | 3 s | 2.6 s | Default hold **2–3 s** |
| Shortest / longest scene | 1 s | 5 s | 1.6 / 4.4 s | **1 s** only for impacts/flashes; **≤ 4 s** except the final shot (≤ 5 s) |
| Scenes ≤ 3 s | 67% | 96% | 87% | **≥ 85% of scenes ≤ 3 s** |
| Cuts per 10 s | 2.8 | 4.5 | 3.6–3.8 | **3.5–4.5 cuts / 10 s** |
| Hook duration | 1 s | 3 s | 2.2 s | Hook line **≤ 2.5 s** |
| Hook words | 10 | 14 | 11.8 | **10–14 words** |
| Spoken words | 197 | 233 | 212 | **190–235 words per ~55 s** |
| Words / second | 3.4 | 4.5 | 3.9 | **3.6–4.2 w/s** (~215–250 wpm): fast TTS |
| Words per scene | 8.6 | 14.0 | 11.0 | **≈ 1 clause (8–14 words) per shot**; split longer sentences across 2 shots |
| Medium + MCU share | 53% | 81% | 70% | **Medium-family 60–80%** |
| Close / ECU share | 0% | 18% | 8% | **CU/ECU 5–15%** |
| Wide share | 5% | 47% | 21% | **Wide 10–30%** (up to 45% for spectacle/wealth premises) |
| Shot-scale change rate | 0.54 | 0.80 | 0.71 | **Change scale on ≥ 2 of every 3 cuts** |
| Chapters | 5 | 5 | 5 | **Exactly 5** |
| Chapter onsets (% of runtime) | — | — | 4 / 17 / 37 / 57 / 75 | **≈ 4%, 17%, 37%, 57%, 75%** (each ±6 pts) |
| Final chapter length | 12 s | 17 s | 13.6 s | **Final chapter 12–17 s** (longest chapter) |
| Scenes per chapter | 3.0 | 5.4 | 4.3 | **3–6 scenes per chapter** |

## 3. Observation vs inference

| Claim | Type | Confidence | Basis |
|---|---|---|---|
| Five chapters, "Day one" first, at 1.7–3 s | Observed | High | 5/5, transcript + timing |
| Mean hold 2.15–3.33 s, mostly ≤ 3 s | Observed | High | 5/5, timing (±0.5 s) |
| Medium shot dominant | Observed | High | 5/5 analyser shot labels |
| Avatar is one stylized translucent/skeletal non-human "you" | Observed | High | 5/5 visual descriptions |
| *Why* a stylized skeleton avatar: universal, identity-free, readable "you" that keeps continuity with no real face | Inferred | Medium | Purpose is not observable |
| Lollipop is a deliberate channel Easter egg | Inferred | Medium | Present in 3/5, including first and last frames |
| Chapter-4/5 turn at 50–78% runtime | Observed | High | 5/5, timing |
| Chapter labels burned on screen | Partly observed | Medium | Reported in 2/5; analyser may omit text |
| Word-level subtitles | Not observed | Low | Analyser does not report captions; adopted as a platform default |
| Camera is mostly static or subject-driven, with low tracking for chases | Partly observed | Medium | Camera moves reported in ~8 scenes total |
| Rendered as stylized 3D CG with motivated cinematic lighting | Inferred from descriptions | Medium | "glass", "translucent", "glowing", lighting language in every scene |
| Music/SFX design | Mostly unobserved | Low | Only R5 reports SFX/music beats |

---

## 4. Production DNA

### A. Hook DNA
1. Line 1 is a single question: `What would happen if you [were born / were raised / woke up / were stranded…] [extreme condition]?` The alternate form `What if you…?` is allowed. **10–14 words, ≤ 2.5 s.**
2. The condition is an **extreme displacement** of an ordinary life. Pick at least one axis: status (billionaire, slave), era (ancient Rome, year 3000), environment (wilderness), or society (dangerous tribe).
3. Frame 1 shows the avatar **already inside the premise and in motion or under threat**. Never use an abstract title card.
4. "Day one" follows **immediately** (1.7–3 s). Optionally, the Day-one line subverts the normal version of the event, e.g. "you're not born in a hospital…".

### B. Narrative DNA
1. **5 chapters**, each opened by a spoken time stamp. Pick the unit from the premise:
   - **Lifespan premise:** `Day one → Year a → Year b → Year c → Year d`, with gaps that widen or stay even.
   - **Bounded-duration premise:** `Day one … Day five`, or hours/weeks, sized to the stated duration.
2. Each chapter = **one rite of passage or status change**. It has one concrete event, one sensory/body detail, and one consequence.
3. **Escalate every chapter** along at least 2 axes: physical stakes, scale of the world, social status, or psychological pressure.
4. **The turn** lands in chapter 4 or 5 (~57–75%). Choose one: invert the premise's promise (luxury → emptiness), raise it to an extreme (arena → emperor), or break reality (twist).
5. **The payoff** resolves the hook's implied question and reframes it. Close with one short thesis or twist line, ideally ≤ 8 words or ending on a single word.
6. Narration is 2nd person, present tense, plain declarative sentences, with concrete nouns and numbers ("six hours", "30 languages"). No named characters. No real people.

### C. Pacing DNA
- 50–60 s total. 190–235 words at 3.6–4.2 w/s.
- 20–26 shots, mean hold 2.2–2.8 s, ≥ 85% ≤ 3 s, max 4 s (final shot ≤ 5 s).
- One clause per shot. A sentence > 14 words spans 2 shots, and the second shot is a "carry-over" image.
- Chapter onsets at ≈ 4 / 17 / 37 / 57 / 75% of runtime, each ±6 pts. Make the final chapter the longest (12–17 s).
- When narration describes repetition ("again and again", "sometimes… sometimes…"), cut a 2–3 shot montage inside the line.

### D. Visual DNA
- **One original avatar:** stylized, non-photoreal, identity-free and big-eyed, with a distinctive material (e.g. a glass or skeletal look). The Skill must design its **own** avatar, not a skeleton/glass clone.
- The avatar appears in ≥ 95% of shots, usually centred, with context and supporting cast behind it.
- The avatar's age, body and wardrobe evolve per chapter. Use a visible "power-up" or "wear-down" signal (glow, scars, tattered clothes).
- Shot mix: Medium-family 60–80%, Wide 10–30%, CU/ECU 5–15%. Change scale on ≥ 2/3 of cuts. Use Wide to establish each chapter's new world, and CU for hands, eyes and concept details.
- Every chapter opens with a new environment and lighting key (time of day or colour temperature). Within a chapter, change sub-location every 1–2 shots.
- Camera: mostly locked or gently moving. Low tracking for chases, behind-the-back for entering the unknown, a push-in for the final emotional beat. Hard cuts only.
- Optional diegetic text (HUDs, signs, countdowns) when the premise is technological.

### E. Retention DNA
- A pattern interrupt every 8–15 s: a new threat, an anomaly (glow, hallucination, glitch), a direct-to-camera look, a genre intrusion, or a comic deflation.
- Each spoken time stamp is a micro-cliffhanger. The audience knows how many chapters remain only implicitly (e.g. "five days").
- **Plant and pay off:** an early object or constraint returns in the final image. Use an original signature prop or a premise-specific constraint (chains, a lost item).
- End with no CTA: a reframing line, then a held tableau (1–3 s, optionally music-only), or an open twist that invites a loop.
