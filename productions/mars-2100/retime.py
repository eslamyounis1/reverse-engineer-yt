"""Phase 5 retiming: cut each shot 0.05 s before its clause's first word (Whisper on narration v2)."""
import json, re
NARR_END, TAIL = 58.25, 1.6
W = [(float(t), re.sub(r"[^a-z0-9']", "", w.lower())) for t, w in (x.split("|", 1) for x in open("words_v2.txt").read().split())]
p = json.load(open("plan.json"))
ptr, starts = 0, []
for s in p["shots"]:
    toks = [re.sub(r"[^a-z0-9']", "", t.lower()) for t in s["line"].split()[:2]]
    def ok(i):
        if W[i][1] != toks[0]:
            return False
        a, b = toks[1], W[i + 1][1] if i + 1 < len(W) else ""
        return a == b or (a and b and (a.startswith(b) or b.startswith(a))) or any(c.isdigit() for c in a + b) or a in ("one", "six", "fourteen", "twentytwo", "thirty", "three", "twelve")
    while not ok(ptr):
        ptr += 1
    starts.append(max(0.0, round(W[ptr][0] - 0.05 - s.get("jcut", 0.0), 2)))
    ptr += 1
starts[0] = 0.0
ends = starts[1:] + [round(NARR_END + TAIL, 2)]
for s, a, b in zip(p["shots"], starts, ends):
    s["start"], s["dur"] = a, round(b - a, 2)
    gen = s["gen_duration"]
    if s["dur"] + 0.3 > gen:  # useful window must cover the new hold
        s["gen_duration"] = gen = int(-(-(s["dur"] + 0.6) // 1))
    s["useful_window"] = [0.3, round(min(gen, 0.3 + s["dur"] + 0.6), 2)]
p["narration"] = {"version": 2, "speech_rate": 75, "media_id": "47cd141c-0564-4721-9bf2-ab9c27fd20da",
                  "url": "https://d2ol7oe51mr4n9.cloudfront.net/user_3JKkOpZH7SUehrR7g2n1NyV75TN/47cd141c-0564-4721-9bf2-ab9c27fd20da.mp3",
                  "duration_s": NARR_END, "words": 237, "words_per_sec_measured": 4.07}
p["voice"]["speech_rate"] = 75
p["notes"].append("Retimed to Whisper word timestamps of narration v2 (speech_rate 75; v1 at 25 measured 2.8 w/s, rejected).")
json.dump(p, open("plan.json", "w"), indent=1)
for s in p["shots"]:
    print(s["id"], s["start"], s["dur"], s["gen_duration"], s["useful_window"])
