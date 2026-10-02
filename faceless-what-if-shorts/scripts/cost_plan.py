#!/usr/bin/env python3
"""Cost preflight helper for faceless-what-if-shorts.

Batch tools (generate_*_batch) do NOT accept get_cost, so the preflight prices each DISTINCT
configuration once with the single tools (generate_image / generate_video / generate_audio +
get_cost:true) and multiplies by job counts.

Step 1  python3 cost_plan.py plan.json > preflight.json
        -> list of priced configurations; for each, call the named tool once with `params`
           (which already contain get_cost:true) and write the returned credit cost into
           prices.json as {"<config key>": <unit cost>}.
Step 2  python3 cost_plan.py plan.json --prices prices.json [--write]
        -> image / video / narration / total table (+ retry contingency, shown separately).
           --write stores the result in plan.cost_preflight (approved_by_user stays false
           until the user approves).
"""
import json
import sys
from collections import OrderedDict

IMG = "gpt_image_2_5"
VID = "seedance_2_5"
TTS = "seed_audio"
CONTINGENCY = 0.20  # retries / regeneration of the weakest scene, shown as a separate line


def image_jobs(plan):
    """(key, params, count, what) for every planned GPT Image 2.5 job."""
    n_stages = len(plan.get("avatar", {}).get("spec", {}).get("stage_changes", [])) or 5
    shots = plan["shots"]
    # Chapter-opener shots whose keyframe IS the Phase-4 establishing frame are not billed twice.
    kf = [s for s in shots if s.get("visual_source") == "KEYFRAME_REQUIRED"
          and not s.get("keyframe_is_establishing")]
    hero = [s for s in kf if set(s.get("tags", [])) & {"hook", "payoff"}]
    jobs = [
        ("img:flare:high:2k", {"variant": "flare", "quality": "high", "resolution": "2k"}, 1, "avatar base reference"),
        ("img:sunburst:high:2k", {"variant": "sunburst", "quality": "high", "resolution": "2k"}, n_stages,
         "avatar stage frames (edits of the approved reference)"),
        ("img:flare:high:2k", {"variant": "flare", "quality": "high", "resolution": "2k"}, 1, "signature prop"),
        ("img:flare:high:2k", {"variant": "flare", "quality": "high", "resolution": "2k"}, 5,
         "chapter establishing keyframes"),
        ("img:flare:high:2k", {"variant": "flare", "quality": "high", "resolution": "2k"}, len(kf) - len(hero),
         "KEYFRAME_REQUIRED scene keyframes"),
        ("img:flare:xhigh:2k", {"variant": "flare", "quality": "xhigh", "resolution": "2k"}, len(hero),
         "hook + payoff keyframes"),
    ]
    out = []
    for key, p, n, what in jobs:
        params = {"model": IMG, "aspect_ratio": "9:16", "prompt": "cost preflight", "get_cost": True, **p}
        out.append((key, "generate_image", params, n, what))
    return out


def video_jobs(plan):
    agg = OrderedDict()
    for s in plan["shots"]:
        gen = s.get("gen_duration", 4)
        audio = s.get("audio") == "diegetic"
        variants = []
        if s.get("difficult"):
            variants.append(("draft", {"resolution": "480p", "draft": True}))
        variants.append(("final", {"resolution": "1080p"}))
        for tag, extra in variants:
            key = f"vid:{gen}s:{extra['resolution']}:{'draft' if extra.get('draft') else 'final'}:audio={str(audio).lower()}"
            if key not in agg:
                params = {"model": VID, "mode": "t2v", "aspect_ratio": "9:16", "duration": gen,
                          "generate_audio": audio, "prompt": "cost preflight", "get_cost": True, **extra}
                agg[key] = [key, "generate_video", params, 0, f"{gen}s source clips, {tag}, audio={audio}"]
            agg[key][3] += 1
    return [tuple(v) for v in agg.values()]


def narration_jobs(plan):
    """One Seed Audio take per chapter. Price each take's actual text (cost may scale with length)."""
    chapters = OrderedDict()
    for s in plan["shots"]:
        ch = max(1, s.get("chapter", 1))  # hook rides in the chapter-1 take
        chapters.setdefault(ch, []).append(s["line"])
    out = []
    for ch, lines in chapters.items():
        text = " ".join(l for l in lines if l)
        v = plan.get("voice", {})
        params = {"model": TTS, "prompt": text, "speech_rate": v.get("speech_rate", 25), "get_cost": True}
        if v.get("voice_id"):
            params.update({"voice_type": v.get("voice_type", "preset"), "voice_id": v["voice_id"]})
        out.append((f"tts:ch{ch}", "generate_audio", params, 1, f"narration take, chapter {ch} ({len(text.split())} words)"))
    return out


def main(argv):
    plan_path = argv[0]
    plan = json.load(open(plan_path))
    groups = {"image": image_jobs(plan), "video": video_jobs(plan), "narration": narration_jobs(plan)}
    if "--prices" not in argv:
        seen, req = set(), []
        for g, jobs in groups.items():
            for key, tool, params, n, what in jobs:
                if key in seen or n == 0:
                    continue
                seen.add(key)
                req.append({"key": key, "group": g, "tool": tool, "params": params})
        print(json.dumps({"note": "Call each tool once with params (single tool, not *_batch). "
                                  "Video uses mode t2v as the price probe; re-check one omni_reference item "
                                  "before the video batch (SKILL.md Phase 7).", "preflight": req}, indent=1))
        return
    prices = json.load(open(argv[argv.index("--prices") + 1]))
    totals, lines, missing = {}, [], []
    for g, jobs in groups.items():
        sub = 0.0
        for key, tool, params, n, what in jobs:
            if n == 0:
                continue
            if key not in prices or prices[key] is None:
                missing.append(key)
                continue
            cost = prices[key] * n
            sub += cost
            lines.append({"group": g, "what": what, "count": n, "unit": prices[key], "cost": round(cost, 2)})
        totals[g] = round(sub, 2)
    if missing:
        raise SystemExit(f"missing prices for: {sorted(set(missing))}: never guess, preflight them")
    totals["total"] = round(totals["image"] + totals["video"] + totals["narration"], 2)
    totals["contingency_20pct"] = round(totals["total"] * CONTINGENCY, 2)
    print(f"{'group':10} {'what':58} {'n':>3} {'unit':>8} {'cost':>9}")
    for l in lines:
        print(f"{l['group']:10} {l['what'][:58]:58} {l['count']:>3} {l['unit']:>8} {l['cost']:>9}")
    print()
    for k in ("image", "video", "narration", "total", "contingency_20pct"):
        label = {"image": "estimated image cost", "video": "estimated video cost",
                 "narration": "estimated narration cost", "total": "ESTIMATED TOTAL",
                 "contingency_20pct": "retry contingency (+20%, not included)"}[k]
        print(f"{label:40} {totals[k]:>10}")
    if "--write" in argv:
        plan["cost_preflight"] = {**totals, "currency": "credits", "lines": lines,
                                  "approved_by_user": False}
        json.dump(plan, open(plan_path, "w"), indent=1)
        print(f"\nwrote cost_preflight to {plan_path} (approved_by_user=false)")


if __name__ == "__main__":
    main(sys.argv[1:])
