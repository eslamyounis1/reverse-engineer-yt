#!/usr/bin/env python3
"""timeline.json (assembler input) from plan.json + results.json (shot id -> accepted 1080p url)."""
import json

LABELS = {2: "DAY 1", 5: "YEAR 6", 9: "YEAR 15", 14: "YEAR 22", 19: "YEAR 30"}
p = json.load(open("plan.json"))
res = json.load(open("results.json"))
shots = []
for s in p["shots"]:
    shots.append({"url": res[str(s["id"])], "in": s["useful_window"][0], "dur": s["dur"],
                  "gen_duration": s["gen_duration"], "diegetic": s["audio"] == "diegetic", "diegetic_db": -20,
                  "label": LABELS.get(s["id"])})
tl = {"fps": 30, "width": 1080, "height": 1920, "narration_url": p["narration"]["url"], "shots": shots}
json.dump(tl, open("timeline.json", "w"), indent=1)
print(len(shots), "shots, total", round(sum(x["dur"] for x in shots), 2))
