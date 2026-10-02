#!/usr/bin/env python3
"""Compute per-reference production metrics from Higgsfield scene analyses.

Usage: python3 analysis/metrics.py            # per-video table + JSON
       python3 analysis/metrics.py --json     # machine-readable only
"""
import glob
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER_RE = re.compile(
    r"\b(day|night|week|month|year|hour|minute|second|age)\s+"
    r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
    r"thirty|forty|fifty|hundred|thousand|\d+)",
    re.I,
)
NON_SPEECH_RE = re.compile(r"^\s*\[.*\]\s*$")
SCALE_ORDER = ["Extreme Wide", "Wide", "Medium", "Medium Close-Up", "Close-Up", "Extreme Close-Up"]


def words(text):
    if NON_SPEECH_RE.match(text):
        return 0
    return len(re.findall(r"[A-Za-z0-9']+", text))


def scene_durations(doc):
    inclusive = doc["timestamp_convention"] == "inclusive"
    return [s["end"] - s["start"] + (1 if inclusive else 0) for s in doc["scenes"]]


def analyze(doc):
    scenes = doc["scenes"]
    durs = scene_durations(doc)
    total = sum(durs)
    wc = [words(s["audio"]) for s in scenes]
    spoken = sum(wc)
    silent = [s["n"] for s, w in zip(scenes, wc) if w == 0]
    shots = {}
    for s in scenes:
        shots[s["shot"]] = shots.get(s["shot"], 0) + 1
    # Chapter markers: scene number + elapsed time when a time-stamp phrase starts
    chapters = []
    for s, d in zip(scenes, durs):
        q = s["audio"].find("?") if s["n"] == 1 else -1
        for m in CHAPTER_RE.finditer(s["audio"]):
            if m.start() < q:  # time phrase inside the hook question is premise, not a chapter
                continue
            # estimate onset by word position inside the scene
            frac = words(s["audio"][: m.start()]) / max(1, words(s["audio"]))
            chapters.append({"scene": s["n"], "t": round(s["start"] + frac * d, 1), "marker": m.group(0)})
    hook = scenes[0]
    hook_dur = durs[0]
    # hook words = words spoken before the first chapter marker (or all of scene 1)
    q = hook["audio"].find("?")
    hook_words = words(hook["audio"][: q + 1] if q >= 0 else hook["audio"])
    eff_cuts = len(scenes) - 1 + doc.get("internal_extra_cuts", 0)
    # Scale changes between consecutive scenes
    scale_changes = sum(1 for a, b in zip(scenes, scenes[1:]) if a["shot"] != b["shot"])
    return {
        "ref": doc["ref"],
        "video_id": doc["video_id"],
        "duration_s": total,
        "scene_count": len(scenes),
        "scene_dur_mean": round(statistics.mean(durs), 2),
        "scene_dur_median": statistics.median(durs),
        "scene_dur_min": min(durs),
        "scene_dur_max": max(durs),
        "pct_scenes_le_3s": round(100 * sum(d <= 3 for d in durs) / len(durs)),
        "cuts_per_10s": round(10 * (len(scenes) - 1) / total, 2),
        "effective_cuts_per_10s": round(10 * eff_cuts / total, 2),
        "mean_visual_hold_s": round(total / (eff_cuts + 1), 2),
        "hook_dur_s": hook_dur,
        "hook_words": hook_words,
        "hook_text": hook["audio"],
        "spoken_words": spoken,
        "words_per_sec": round(spoken / total, 2),
        "words_per_scene_mean": round(spoken / (len(scenes) - len(silent)), 1),
        "words_per_scene_max": max(wc),
        "silent_scenes": silent,
        "shot_scale_counts": shots,
        "pct_medium_family": round(
            100 * sum(v for k, v in shots.items() if k in ("Medium", "Medium Close-Up")) / len(scenes)
        ),
        "pct_close": round(100 * sum(v for k, v in shots.items() if "Close-Up" in k and "Medium" not in k) / len(scenes)),
        "pct_wide": round(100 * sum(v for k, v in shots.items() if "Wide" in k) / len(scenes)),
        "scale_change_rate": round(scale_changes / (len(scenes) - 1), 2),
        "chapters": chapters,
        "chapter_count": len(chapters),
        "chapter_onset_pct": [round(100 * c["t"] / total) for c in chapters],
        "final_chapter_len_s": round(total - chapters[-1]["t"], 1) if chapters else None,
        "first_chapter_t": chapters[0]["t"] if chapters else None,
        "scenes_per_chapter": round(len(scenes) / max(1, len(chapters)), 1),
    }


def main():
    docs = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(HERE, "raw", "R*.json")))]
    results = [analyze(d) for d in docs]
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
        return
    keys = ["duration_s", "scene_count", "scene_dur_mean", "scene_dur_median", "scene_dur_min",
            "scene_dur_max", "pct_scenes_le_3s", "cuts_per_10s", "effective_cuts_per_10s", "mean_visual_hold_s", "hook_dur_s", "hook_words",
            "spoken_words", "words_per_sec", "words_per_scene_mean", "words_per_scene_max",
            "pct_medium_family", "pct_close", "pct_wide", "scale_change_rate", "chapter_count",
            "first_chapter_t", "scenes_per_chapter"]
    print("metric".ljust(22) + "".join(r["ref"].rjust(9) for r in results))
    for k in keys:
        print(k.ljust(22) + "".join(str(r[k]).rjust(9) for r in results))
    print()
    for r in results:
        print(r["ref"], "shots:", r["shot_scale_counts"])
        print(r["ref"], "no-new-line scenes (silence or carry-over):", r["silent_scenes"])
        print(r["ref"], "chapters:", [(c["t"], c["marker"]) for c in r["chapters"]])
    print()
    print("CROSS-REFERENCE AGGREGATE (n=%d)" % len(results))
    for k in keys + ["final_chapter_len_s"]:
        vals = [r[k] for r in results if isinstance(r[k], (int, float))]
        if vals:
            print("  %-22s min %-6s max %-6s mean %s" % (k, min(vals), max(vals), round(statistics.mean(vals), 2)))
    for i in range(5):
        col = [r["chapter_onset_pct"][i] for r in results if len(r["chapter_onset_pct"]) > i]
        print("  chapter %d onset %%     min %-6s max %-6s mean %s" % (i + 1, min(col), max(col), round(statistics.mean(col))))
    with open(os.path.join(HERE, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
