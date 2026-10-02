#!/usr/bin/env python3
"""Cut v3: 26 approved clips + 12 insert shots, cut to the Sterling narration (pauses capped).

Each cut lands 0.05 s before its first word (minus the shot's J-cut). Inserts come from
v3_jobs.json (key -> result url). No slow-motion: every hold must fit the clip at real speed.
Usage: python3 build_v3.py   -> timeline_v3.json
"""
import json
NARR = "https://d2ol7oe51mr4n9.cloudfront.net/user_3JKkOpZH7SUehrR7g2n1NyV75TN/2590dfbd-6746-401f-97be-2e67179681ee.mp3"
END = 83.43 + 1.45  # narration end + tail (shot 26 is a 5.04 s clip)
# (shot key, time of the first word it covers, J-cut). Keys are plan ids, inserts are "<id><b|c>".
CUTS = [("1", 0.0, 0), ("1b", 1.80, 0),            # "Mars in the year 2100"
        ("2", 4.26, 0), ("2b", 5.70, 0),           # "three metres of dirt"
        ("3", 8.14, 0.25), ("4", 10.46, 0), ("5", 12.40, 0.3), ("6", 14.42, 0),
        ("7", 16.72, 0), ("7b", 18.36, 0),         # "just over a third"
        ("8", 20.60, 0.1), ("8b", 22.20, 0),       # "becomes a slow, floating flight"
        ("9", 24.88, 0), ("10", 26.30, 0), ("11", 28.96, 0), ("12", 31.72, 0),
        ("13", 33.86, 0), ("13b", 35.96, 0),       # "swallows the whole planet"
        ("14", 38.36, 0.15), ("14b", 40.06, 0),    # "the colony rations every watt"
        ("15", 42.14, 0.3), ("15b", 43.40, 0),     # "by hand, sol after sol"
        ("16", 45.98, 0), ("16b", 47.96, 0),       # "the only green for kilometres"
        ("17", 50.30, 0), ("17b", 51.82, 0),       # "finally win a seat"
        ("18", 54.22, 0), ("18b", 56.12, 0),       # "months. You've waited years."
        ("19", 57.94, 0),
        ("20b", 61.24, 0), ("20", 63.22, 0), ("20c", 64.62, 0),  # Mars gravity / On Earth / nearly three times heavier
        ("21", 66.50, 0.45), ("22", 68.78, 0), ("23", 72.22, 0), ("24", 74.82, 0), ("25", 77.76, 0), ("26", 79.94, 0)]
LABELS = {"2": "DAY 1", "7": "YEAR 6", "13": "YEAR 14", "17": "YEAR 22", "22": "YEAR 30"}
CLIP = 4.04


def main():
    v2 = json.load(open("timeline.json"))["shots"]
    res = json.load(open("results.json"))
    ins = json.load(open("v3_jobs.json"))
    starts = [max(0.0, round(t - 0.05 - j, 2)) for _, t, j in CUTS]
    starts[0] = 0.0
    ends = starts[1:] + [round(END, 2)]
    shots = []
    for (k, _, _), a, b in zip(CUTS, starts, ends):
        dur = round(b - a, 2)
        if k.isdigit():
            base = dict(v2[int(k) - 1])
            base["url"] = res[k]
            clip = 5.04 if k == "26" else CLIP
        else:
            base = {"url": ins[k], "gen_duration": 4, "diegetic": False, "diegetic_db": -20, "still": False}
            clip = CLIP
        base.update(dur=dur, label=LABELS.get(k), still=False, key=k)
        base["in"] = round(min(0.3, clip - dur - 0.02), 2)
        assert base["in"] >= 0.0, (k, dur)
        shots.append(base)
    tl = {"fps": 30, "width": 1080, "height": 1920, "narration_url": NARR, "shots": shots}
    json.dump(tl, open("timeline_v3.json", "w"), indent=1)
    d = [s["dur"] for s in shots]
    print(len(shots), "shots, total", round(sum(d), 2), "mean hold", round(sum(d) / len(d), 2), "max", max(d), "min", min(d))
    for s in shots:
        print(f'{s["key"]:>4} in {s["in"]:.2f} dur {s["dur"]:.2f}', s["label"] or "", "DIEGETIC" if s["diegetic"] else "")


if __name__ == "__main__":
    main()
