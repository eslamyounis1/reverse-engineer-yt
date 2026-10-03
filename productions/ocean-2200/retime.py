#!/usr/bin/env python3
"""Retime plan.json to narration v3 (Whisper word starts; cut 0.05 s before each clause's first word)."""
import json

FIRST_WORD = [0.0, 2.56, 4.76, 6.96, 9.70, 11.84, 13.92, 15.56, 18.14, 20.98, 23.56, 25.56, 26.76,
              29.28, 32.26, 34.48, 36.38, 38.08, 39.64, 42.40, 43.68, 45.44, 46.76]
END = 51.41  # narration ends 49.31; final shot holds 4.7 s (5 s source, window 0.3-5.0)

p = json.load(open("plan.json"))
cuts = [0.0] + [round(t - 0.05, 2) for t in FIRST_WORD[1:]] + [END]
for i, s in enumerate(p["shots"]):
    s["start"], s["dur"] = cuts[i], round(cuts[i + 1] - cuts[i], 2)
    gen = s["gen_duration"]
    s["useful_window"] = [0.3, round(min(gen, 0.3 + s["dur"] + 0.6), 2)]
p["narration"] = {"version": 3, "voice": "Sterling", "speech_rate": 50, "media_id": "a340441e-95d6-4140-87c2-6809225fd96f",
                  "url": "https://d2ol7oe51mr4n9.cloudfront.net/user_3JKkOpZH7SUehrR7g2n1NyV75TN/a340441e-95d6-4140-87c2-6809225fd96f.mp3",
                  "duration_s": 49.31, "words_per_sec_measured": 3.79,
                  "post": "pauses capped at 0.3 s, 0.45 s chapter gaps, ch4 take trimmed after 'Hard.' (possible repeated word/breath)",
                  "takes": {"ch1": "34fa21d8-f689-49ca-8754-0495d591db6a", "ch2": "ec133e61-c162-4ef5-8d8f-d4e1f2f2a01f",
                            "ch3": "4b9414cb-8222-490b-a45d-b40120b4fdf4", "ch4": "c699259a-9f4b-493c-ad1f-d5ebfdb7c3e3",
                            "ch5": "d0528a3f-21f4-47f9-a643-db9438b2e5dc"},
                  "rejected_takes_rate30": ["afd1d3f3-713d-400e-a709-31e674965d9f", "f5bfa265-3262-482d-8823-2b3af42c6d5e",
                                            "24496438-7b2d-452f-94e4-94ee047ac87d", "0d8f6e73-98c1-4615-8e80-33f92362a26c",
                                            "1e9b0491-002e-4b5e-9d2f-b483f8ad3d29"]}
p["voice"]["speech_rate"] = 50
p["notes"].append("Narration: rate 30 measured 2.94 w/s (too slow), re-taken at rate 50 -> 3.79 w/s after pause capping.")
json.dump(p, open("plan.json", "w"), indent=1)
print("retimed", len(p["shots"]), "shots; end", END)
