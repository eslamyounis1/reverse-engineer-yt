#!/usr/bin/env python3
"""Build timeline.json + script_manifest.json for assemble_short.py from plan.json and video result URLs.

Usage: python3 build_timeline.py results.json   (results.json = {"<shot id>": "<result_url>", ...})
"""
import json
import sys

LABELS = {1: "DAY 1", 2: "YEAR 6", 3: "YEAR 14", 4: "YEAR 22", 5: "YEAR 30"}


def main(path):
    p = json.load(open("plan.json"))
    urls = json.load(open(path))
    shots, seen = [], set()
    for s in p["shots"]:
        label = None
        if s["chapter"] >= 1 and s["chapter"] not in seen:
            seen.add(s["chapter"])
            label = LABELS[s["chapter"]]
        shots.append({"url": urls[str(s["id"])], "in": s["useful_window"][0], "dur": s["dur"],
                      "gen_duration": s["gen_duration"], "diegetic": s["audio"] == "diegetic",
                      "diegetic_db": -20, "label": label, "still": urls[str(s["id"])].endswith(".png")})
    tl = {"fps": 30, "width": 1080, "height": 1920, "narration_url": p["narration"]["url"], "shots": shots}
    json.dump(tl, open("timeline.json", "w"), indent=1)
    blocks, cur = [], {}
    for s in p["shots"]:
        cur.setdefault(max(1, s["chapter"]), []).append(s["line"])
    json.dump({"blocks": [{"vo_line": " ".join(v)} for v in cur.values()]}, open("script_manifest.json", "w"), indent=1)
    print("shots", len(shots), "total", round(sum(x["dur"] for x in shots), 2))


if __name__ == "__main__":
    main(sys.argv[1])
