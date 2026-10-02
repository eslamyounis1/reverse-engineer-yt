#!/usr/bin/env python3
"""Render generation_plan.md (GPT Image 2.5 / Seedance 2.5 / narration job specs) from plan.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = ("stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour, "
         "shallow depth of field, clean readable silhouettes, 9:16 vertical composition")


def main():
    p = json.load(open(os.path.join(HERE, "plan.json")))
    av, spec, shots = p["avatar"], p["avatar"]["spec"], p["shots"]
    stage_of = {1: "newborn", 2: "child", 3: "teen", 4: "adult22", 5: "adult30"}
    L = []
    w = L.append
    w("# Generation plan: What If You Were Born on Mars in 2100?\n")
    w("Rendered from `plan.json` by `render_generation_plan.py`. **Nothing here has been submitted.**\n")
    w("Locked stack: `gpt_image_2_5` (flare by default, sunburst only for avatar stage edits), "
      "`seedance_2_5` (1080p accepted shots), 9:16, `seed_audio` narration.\n")

    w("## 1. Avatar concept: \"Pip\"\n")
    w(f"**Design:** {av['design']}.\n")
    for k in ("silhouette", "proportions", "materials", "clothing"):
        w(f"- **{k}:** {spec[k]}")
    w(f"- **identifying features:** {', '.join(spec['identifying_features'])}")
    w("\n**Originality:**")
    w("- Knitted wool and button eyes: no glass, translucent or skeleton look; the validator's"
      " forbidden-design check passes.")
    w("- It also differs from the Skill's example avatar (a birch marionette).")
    w("- The yellow beanie is the one accent colour. It never appears in any Mars background"
      " (rust, butterscotch, blue dusk, greenhouse green).\n")
    w("| Chapter | Age | Clothing | State |\n|---|---|---|---|")
    for c in spec["stage_changes"]:
        w(f"| {c['chapter']} | {c['age']} | {c['clothing']} | {c['state']} |")
    w("")

    # ---------- images ----------
    w("## 2. GPT Image 2.5 jobs (17)\n")
    w("All jobs use `model: gpt_image_2_5`, `aspect_ratio: 9:16`, `resolution: 2k`, submitted with"
      " `generate_image_batch` (≤ 12 per call). The exception is I-1, a single `generate_image`"
      " so you can approve it on its own.\n")
    w("| Job | Batch | Variant / quality | image_references | Purpose |\n|---|---|---|---|---|")
    jobs = [("I-1 avatar reference", "I1 (alone, approval gate)", "flare / high", "—", "AVATAR_REF")]
    for c in spec["stage_changes"]:
        jobs.append((f"I-stage-{stage_of[c['chapter']]}", "I2", "**sunburst** / high", "AVATAR_REF",
                     f"avatar:stage:{stage_of[c['chapter']]}"))
    jobs.append(("I-prop seedcup", "I3", "flare / high", "—", "prop:seedcup"))
    for s in shots:
        if s.get("keyframe_is_establishing"):
            jobs.append((f"I-env-ch{s['chapter']} (= shot {s['id']} keyframe)", "I3", "flare / high",
                         f"avatar:stage:{s['avatar_stage']}", f"env:ch{s['chapter']}"))
    for s in shots:
        if s["visual_source"] == "KEYFRAME_REQUIRED" and not s.get("keyframe_is_establishing"):
            hero = set(s["tags"]) & {"hook", "payoff"}
            refs = [r for r in s["refs"]]
            jobs.append((f"I-kf-shot{s['id']}", "I4 (after --gate-keyframes)",
                         "flare / **xhigh**" if hero else "flare / high", ", ".join(refs), s["keyframe_reason"]))
    for j in jobs:
        w("| " + " | ".join(j) + " |")
    w(f"\nTotal: **{len(jobs)} GPT Image 2.5 jobs**.\n")
    w("Batch order:")
    w("1. **I1:** avatar reference. **Stop for your approval.**")
    w("2. **I2:** 5 stage edits.")
    w("3. **I3:** prop + 5 chapter establishing frames (they need the stage refs).")
    w("4. **I4:** 5 scene keyframes, only after `validate_plan.py --gate-keyframes` passes.\n")

    w("### Prompts\n")
    w("**I-1 avatar reference** (flare, high):")
    w("```")
    w(f"Character reference sheet on a neutral warm-grey studio backdrop: {av['design']}.")
    w(f"Silhouette: {spec['silhouette']}. Proportions: {spec['proportions']}. Materials: {spec['materials']}.")
    w(f"Clothing: {spec['clothing']}; wearing {spec['stage_changes'][3]['clothing']} for the sheet.")
    w(f"Identifying features: {', '.join(spec['identifying_features'])}.")
    w("Three views in one vertical image: full body front (top), three-quarter view (middle), face close-up (bottom).")
    w(f"Consistent proportions, no text, no logos. {STYLE}")
    w("```")
    w("**I-stage-* (sunburst edits of AVATAR_REF):**")
    w("```")
    w("Same character: identical silhouette, materials, eyes and identifying features "
      f"({', '.join(spec['identifying_features'])}). Change only: age = {{age}}, clothing = {{clothing}}, "
      "state = {state}. Full body, neutral backdrop.")
    w("```")
    w("**I-prop seedcup:**")
    w("```")
    w("Prop reference on neutral warm-grey backdrop: a small dented tin cup, hand-scuffed, holding dark "
      f"potting soil with one apple seed resting on top. Close-up, no text, no logos. {STYLE}")
    w("```")
    w("**Chapter establishing frames and scene keyframes** (refs: avatar stage + chapter frame):")
    for s in shots:
        if s["visual_source"] != "KEYFRAME_REQUIRED":
            continue
        w(f"- **shot {s['id']}** ({s['scale']}): \"{s['scale']} shot. The character from the first reference "
          f"({s['avatar_stage']} stage), {s['action']}. {s['environment']}. Keep the bottom 17% of the frame "
          f"visually quiet for captions. {STYLE}\"")
    w("")
    w("Exact diegetic text strings:")
    w("- shot 3: `12:00` signal-delay counter.")
    w("- shot 15: `NOT CLEARED`.")
    w("- Anything else: no text.\n")

    # ---------- video ----------
    n_draft = sum(s["difficult"] for s in shots)
    w(f"## 3. Seedance 2.5 jobs ({len(shots)} accepted shots + {n_draft} drafts = {len(shots) + n_draft} submissions)\n")
    w("Common settings:")
    w("- `model: seedance_2_5`, `mode: omni_reference`, `aspect_ratio: 9:16`, `resolution: 1080p`.")
    w("- `duration = gen_duration`: 4 s, or 5 s for the payoff. The 1–3 s holds are cut out of"
      " `useful_window` in assembly.")
    w("- `generate_audio: false` except shot 17 (diegetic).")
    w("- Difficult shots run a 480p `draft: true` first, then are finalized with `draft_job_id` at 1080p.\n")
    w("| Shot | Edited hold | Source | Window | visual_source | Media | Audio | Draft | Action (inside window) |")
    w("|---|---|---|---|---|---|---|---|---|")
    for s in shots:
        src = s["visual_source"]
        if src == "KEYFRAME_REQUIRED":
            media = f"start_image: env:ch{s['chapter']}" if s.get("keyframe_is_establishing") else f"start_image: kf-shot{s['id']}"
        elif src == "REUSE_REFERENCE":
            ro = s["reuse_of"]
            media = (f"start_image: {ro}" if s.get("reuse_mode") == "start_image" else
                     f"image_references: {ro} + avatar:stage:{s['avatar_stage']}")
        else:
            media = f"image_references: avatar:stage:{s['avatar_stage']} + env:ch{max(1, s['chapter'])}"
        a, b = s["useful_window"]
        w(f"| {s['id']} | {s['dur']}s | {s['gen_duration']}s | {a}–{b}s | {src} | {media} | "
          f"{s['audio']} | {'yes' if s['difficult'] else '—'} | {s['action']} |")
    w("\nPrompt template per shot:")
    w("```")
    w("{camera}. From {a}s to {b}s: {action}. After that the motion settles and holds. The character keeps its "
      "exact design from the reference. Stylized 3D animated film look, single continuous shot, no cuts, no text.")
    w("```")
    w("Shot 17 appends: \"Sound: muffled rocket rumble, window trembling. No speech, no voices, no music.\"\n")
    w("Batch order:")
    w("1. **V0:** a single `generate_video` `get_cost` re-check on one real omni_reference item.")
    w(f"2. **V1:** {n_draft} drafts (shots {', '.join(str(s['id']) for s in shots if s['difficult'])}).")
    w("3. **V2 + V3:** 12 + 5 non-difficult finals.")
    w(f"4. **V4:** finalize the {n_draft} accepted drafts.\n")

    # ---------- narration ----------
    v = p["voice"]
    w("## 4. Narration plan (Seed Audio)\n")
    w(f"- Model `seed_audio`, voice `{v['voice_id']}` ({v['voice_type']}, {v['name']}), `speech_rate: {v['speech_rate']}`.")
    w("- **5 takes**, one per chapter, via `generate_audio_batch`. The hook rides in the chapter-1 take,"
      " followed by a 0.25 s pause before \"Day one\".")
    w("- **Assembly:** in one sandbox call, ffprobe the takes, concatenate them with 0.12 s gaps, and run"
      " faster-whisper word timestamps.")
    w("- **Speed target:** 3.6–4.2 words/s. The plan estimates 3.97 w/s at 57.4 s.")
    w("  - If a take falls outside the target, adjust `speech_rate` ±10 and regenerate it. Never time-stretch.")
    w("- **Retiming:** move each edited cut 0.05 s before its clause's first word.")
    w("  - Check that every new `dur` still fits its `useful_window` **before** any video is generated.")
    w("  - Re-run `validate_plan.py`.")
    w("- Narration is generated **before** the Seedance batches, so video windows are locked to real timing.\n")
    w("| Take | Words | Text |\n|---|---|---|")
    chap = {}
    for s in shots:
        chap.setdefault(max(1, s["chapter"]), []).append(s["line"])
    for c, lines in chap.items():
        t = " ".join(lines)
        w(f"| ch{c} | {len(t.split())} | {t} |")
    open(os.path.join(HERE, "generation_plan.md"), "w").write("\n".join(L) + "\n")
    print(f"images {len(jobs)}, video submissions {len(shots) + n_draft}, accepted shots {len(shots)}")


if __name__ == "__main__":
    main()
