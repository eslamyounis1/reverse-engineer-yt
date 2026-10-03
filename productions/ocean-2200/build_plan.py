#!/usr/bin/env python3
"""Builds plan.json for "What If You Were Born Under the Ocean in 2200?".
Edited timings are pre-narration estimates; Phase 5 retimes them to Whisper word timestamps."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
K, D, R = "KEYFRAME_REQUIRED", "DIRECT_VIDEO", "REUSE_REFERENCE"
STAGE = {0: "newborn", 1: "newborn", 2: "child", 3: "teen", 4: "adult22", 5: "adult30"}
WPS = 3.8

# Pip identity: approved base reference + Mars-era stage refs that fit this story unchanged.
PIP_REF = "42fbcc4f-9cf2-4971-a73f-e3230c9b2aa8"
REUSED_STAGES = {"newborn": "c3b30ceb-9bb3-43f9-b94e-7d7d6c261d12",
                 "adult22": "765a97cd-00ac-4261-b8a1-63f5e3f62adb"}

# id, ch, line, scale, source, extra, camera, environment, action, tags
SHOTS = [
 (1, 0, "What would happen if you were born under the ocean in 2200?", "Medium", K,
  {"keyframe_reason": "hook frame: premise + avatar identity (xhigh)"}, "push-in",
  "round nursery porthole in a seafloor dome, deep blue water outside, soft teal night-lights",
  "newborn avatar in a padded crib pod opens its button eyes as a huge manta ray glides past the porthole; a small red diamond kite hangs folded on the crib rail", ["hook", "plant"]),
 (2, 1, "Day one. You're born a hundred metres underwater.", "Wide", K,
  {"keyframe_reason": "chapter 1 opener: seafloor city design", "keyframe_is_establishing": True}, "locked",
  "cluster of glowing domes on the dark-blue seafloor 100 m down, tube walkways, fish schools, faint light from far above",
  "inside the nearest lit dome window a parent lifts the swaddled newborn while a school of fish swirls past outside", []),
 (3, 1, "The air is helium. Your first cry is a squeak.", "Medium Close-Up", D,
  {}, "locked", "nursery inside the dome, warm teal lamps, pressure gauge reading 11 atm on the wall",
  "the newborn in a parent's arms opens its mouth to cry and two nurses behind cover their mouths, giggling", ["interrupt"]),
 (4, 1, "From the surface, your grandparents send a red kite.", "Medium", R,
  {"reuse_of": "prop:kite", "reuse_mode": "image_references"}, "push-in", "nursery, a small pressure-lock delivery hatch in the wall",
  "a parent unwraps a bright red diamond kite from a delivery canister and holds it above the crib; the newborn reaches for its tail", ["plant"]),
 (5, 2, "Year six. Red is the first colour the ocean swallows.", "Medium", K,
  {"keyframe_reason": "chapter 2 opener: undersea classroom", "keyframe_is_establishing": True}, "locked",
  "dome classroom with a giant round window onto blue water, little desks, cool white light",
  "the six-year-old avatar presses the red kite against the big window, the blue water beyond it", []),
 (6, 2, "Outside the window, your kite turns grey.", "Medium", D,
  {}, "behind follow", "open water just outside the dome, everything tinted deep blue",
  "the child in a small dive suit swims out holding the kite, which looks dull grey-blue in the water; the child frowns at it", ["interrupt"]),
 (7, 2, "At school, sun lamps keep your bones strong.", "Wide", D,
  {}, "locked", "classroom under rows of glowing violet-white sun lamps, kids in tinted goggles",
  "a row of kids in goggles bask under glowing lamps; the avatar in the middle stretches its arms like a sunbather", []),
 (8, 2, "Even the strictest teacher sounds like a cartoon.", "Medium Close-Up", D,
  {}, "locked", "classroom, a stern tall teacher at the front",
  "the stern teacher speaks and the avatar and classmates burst into laughter, the avatar covering its mouth", ["interrupt"]),
 (9, 3, "Year fifteen. You visit the surface for the first time.", "Medium", K,
  {"keyframe_reason": "chapter 3 opener: lift capsule bay", "keyframe_is_establishing": True}, "locked",
  "lift capsule bay, a round steel capsule with a porthole, cables rising into the dark water above, warm work lights",
  "the teen avatar climbs into the capsule clutching the folded red kite, glancing up the cable into the dark", []),
 (10, 3, "First, four days sealed in a decompression chamber.", "Medium", D,
  {}, "locked", "cramped round decompression chamber, bunk, gauge on the wall",
  "the bored teen lies on a bunk and scratches a fourth tally mark on the wall as a gauge needle creeps down", ["montage"]),
 (11, 3, "The hatch opens. Your voice drops low.", "Close-Up", D,
  {}, "push-in", "chamber hatch swinging open onto blinding daylight",
  "the hatch swings open and bright daylight floods the teen's face; it squints and its button eyes go wide", []),
 (12, 3, "The sky has no ceiling.", "Wide", K,
  {"keyframe_reason": "composition: tiny teen on a floating deck under a vast open sky (lighting flip)"}, "locked",
  "floating platform deck on a sparkling sea, enormous bright blue sky with towering white clouds, golden afternoon sun",
  "the tiny teen avatar stands at the deck rail and slowly tilts its head back to take in the endless sky", ["interrupt"]),
 (13, 3, "For one windy afternoon, your kite flies red.", "Medium", R,
  {"reuse_of": "prop:kite", "reuse_mode": "image_references"}, "low tracking", "floating platform deck, bright sky, wind",
  "the teen runs along the deck and the vivid red kite leaps into the wind, tail snapping, against the blue sky", []),
 (14, 4, "Year twenty-two. A hurricane up top rips the power cables loose.", "Medium", K,
  {"keyframe_reason": "chapter 4 opener: control room + storm monitor", "keyframe_is_establishing": True}, "locked",
  "dome control room under red emergency light, a large monitor showing a hurricane and snapping power cables",
  "the adult avatar grips the console as the monitor shows giant waves snapping the floating power cables", ["turn"]),
 (15, 4, "The domes go dark. The pumps slow down.", "Wide", D,
  {}, "locked", "the seafloor city from outside, dome lights going out one by one",
  "dome lights blink out one by one across the city until only the avatar's flashlight glows in one window", ["interrupt"]),
 (16, 4, "Then you remember how hard your kite pulled.", "Close-Up", R,
  {"reuse_of": "prop:kite", "reuse_mode": "image_references"}, "push-in", "dark quarters lit by a flashlight",
  "the avatar's hands lift the faded old red kite off a shelf in the flashlight beam", []),
 (17, 4, "You tie it in the deep current outside.", "Medium", D,
  {}, "handheld", "outside the dome in dark blue water, a dome strut, drifting particles in a strong current",
  "the avatar in a dive suit and headlamp ties the kite line to a dome strut; the kite unfurls in the current", []),
 (18, 4, "It pulls. Hard.", "Medium Close-Up", D,
  {}, "push-in", "a small spinning generator hub on the dome strut, one dome lamp beside it",
  "the kite line snaps taut, a small generator hub spins up and the lamp beside the avatar flickers on, lighting its wide button eyes", ["turn", "interrupt"]),
 (19, 5, "Year thirty. Fifty giant kites now fly beneath the city.", "Wide", K,
  {"keyframe_reason": "chapter 5 opener: undersea kite farm", "keyframe_is_establishing": True}, "locked",
  "below the city, rows of giant red underwater kites on tethers sweeping figure-eights, lit by floodlights",
  "the adult avatar stands on a lit lookout platform as giant red kites sweep slow figure-eights below", []),
 (20, 5, "They never land, never stop.", "Medium", D,
  {}, "low tracking", "open water beside a giant red underwater kite",
  "the avatar pilots a small bubble-canopy sub alongside a giant red kite as it sweeps past", []),
 (21, 5, "Every light in every dome runs on them.", "Wide", D,
  {}, "locked", "the whole seafloor city glowing warmly, walkways lit",
  "the avatar walks a lit tube walkway as dome after dome glows warm around it", []),
 (22, 5, "Kids still squeak your name.", "Medium", D,
  {}, "locked", "busy dome corridor with children",
  "a group of kids run past waving and laughing at the avatar, who waves back with a grin", ["interrupt"]),
 (23, 5, "You didn't need the sky. The ocean had wind all along.", "Medium", K,
  {"keyframe_reason": "payoff frame: old kite + giant kite callback (xhigh)"}, "push-in",
  "big round dome window, warm interior light, deep blue water outside",
  "the avatar holds the small faded red kite at the window as a giant glowing red kite sweeps past outside", ["payoff"]),
]

DIFFICULT = set()  # budget: no drafts; Phase 9 regenerates the weakest scene instead.


def wc(t):
    return len(re.findall(r"[A-Za-z0-9']+", t))


def build():
    shots, t = [], 0.0
    for sid, (key, ch, line, scale, src, extra, cam, env, act, tags) in enumerate(SHOTS, 1):
        last = sid == len(SHOTS)
        dur = round(max(1.6, wc(line) / WPS), 2)
        if last:
            dur = round(max(dur, 4.2), 2)
        gen = 5 if last else 4
        stage = STAGE[ch]
        refs = [f"avatar:stage:{stage}", f"env:ch{max(1, ch)}"]
        if "kite" in act:
            refs.append("prop:kite")
        s = {"id": sid, "chapter": ch, "start": round(t, 2), "dur": dur,
             "gen_duration": gen, "useful_window": [0.3, round(min(gen, 0.3 + dur + 0.6), 2)],
             "line": line, "scale": scale, "avatar": True, "avatar_stage": stage,
             "visual_source": src, **extra, "refs": refs, "audio": "none",
             "environment": env, "camera": cam, "action": act,
             "difficult": key in DIFFICULT, "tags": tags}
        shots.append(s)
        t += dur
    plan = {
        "title": "What If You Were Born Under the Ocean in 2200?",
        "premise_type": "lifespan",
        "target_seconds": 57,
        "voice": {"model": "seed_audio", "voice_type": "preset", "voice_id": "dc382508-c8bd-443c-8cb2-46e57b8d2e6f",
                  "name": "Sterling (user-selected in Mars 2100 v3)", "speech_rate": 30},
        "avatar": {
            "name": "pip",
            "design": "small knitted-wool doll figure in cream wool with visible stitch texture, oversized glossy green "
                      "enamel button eyes, sunflower-yellow pom-pom beanie",
            "spec": {
                "silhouette": "compact rounded figure: big round head under a sunflower-yellow pom-pom beanie, "
                              "soft pear-shaped body, short stubby limbs; reads instantly at thumbnail size",
                "proportions": "head 1/3 of height as newborn, 1/4 as child, 1/5 as teen and adult; button eyes about "
                               "1/3 of face width",
                "materials": "cream knitted wool with visible stitch rows, slightly fuzzy edges, glossy green enamel "
                             "buttons for eyes, small stitched curved mouth in brown thread",
                "clothing": "permanent accent: sunflower-yellow knitted pom-pom beanie (never in any background); "
                            "per-chapter garments in stage_changes",
                "identifying_features": ["glossy green enamel button eyes", "sunflower-yellow pom-pom beanie",
                                         "brown stitched curved mouth", "one darker cream darning patch on the left cheek"],
                "stage_changes": [
                    {"chapter": 1, "age": "newborn", "clothing": "silver thermal swaddle + beanie (reused approved stage ref)",
                     "state": "pristine, fluffy wool"},
                    {"chapter": 2, "age": "child (6)", "clothing": "sea-teal school jumpsuit; outdoors a small teal dive suit with a round clear-visor helmet",
                     "state": "wool slightly fuzzed at elbows"},
                    {"chapter": 3, "age": "teen (15)", "clothing": "charcoal-grey wetsuit jacket over a striped knit shirt",
                     "state": "wool a little salt-crusted at the edges, curious"},
                    {"chapter": 4, "age": "adult (22)", "clothing": "navy jacket with a plain round patch (reused approved stage ref)",
                     "state": "neat, determined"},
                    {"chapter": 5, "age": "adult (30)", "clothing": "deep-teal engineer coveralls with a coiled tether rope on the shoulder",
                     "state": "beanie faded, a few repair stitches in yellow thread, settled and proud"},
                ],
            },
            "reference": {"job_id": PIP_REF, "approved_by_user": True,
                          "stage_refs": {k: {"job_id": v, "reused_from": "mars-2100"} for k, v in REUSED_STAGES.items()}},
            "stages": ["newborn", "child", "teen", "adult22", "adult30"],
        },
        "signature_prop": "small bright-red diamond kite with a knotted tail, sent from the surface (plant -> grey underwater -> flies red in the wind -> powers the city -> giant kite farm)",
        "cost_preflight": {"image": None, "video": None, "narration": None, "total": None,
                           "currency": "credits", "approved_by_user": False, "lines": []},
        "notes": [
            "Timings are pre-narration estimates; Phase 5 retimes them to Whisper word timestamps.",
            "dur = final edited hold; gen_duration = Seedance source clip (>=4s), trimmed to useful_window.",
            "Hook contains '2200' inside the question; the validator treats it as premise, not a chapter stamp.",
            "Pip base reference 42fbcc4f was approved in Mars 2100; newborn and adult22 stage refs reused unchanged. Only child, teen and adult30 are new sunburst edits.",
            "No draft passes (budget cap 1,300); weakest scene is regenerated in Phase 9 from the contingency.",
            "Voice: Sterling, the voice the user chose for Mars 2100 v3; speech_rate tuned to the Skill's 3.6-4.2 w/s band.",
        ],
        "chapters": [
            {"n": 1, "label": "Day one", "world": "seafloor dome city, deep blue + warm teal", "event": "birth at 100 m; helium squeak; red kite gift (plant)"},
            {"n": 2, "label": "Year six", "world": "dome classroom, cool white + violet sun lamps", "event": "red vanishes underwater; sun lamps; squeaky teacher"},
            {"n": 3, "label": "Year fifteen", "world": "capsule bay -> chamber -> floating deck, bright golden sky", "event": "4-day decompression; first sky; kite flies red"},
            {"n": 4, "label": "Year twenty-two", "world": "control room red alert -> dark city", "event": "hurricane cuts power; kite in the current lights a lamp (turn)"},
            {"n": 5, "label": "Year thirty", "world": "floodlit kite farm, warm glowing city", "event": "fifty giant current kites power the city; reframing payoff"},
        ],
        "sources": [
            "https://oceanservice.noaa.gov/facts/light_travel.html",
            "https://oceanexplorer.noaa.gov/ocean-fact/light-distributed/",
            "https://www.oceanexplorer.woc.noaa.gov/technology/diving/aquarius/aquarius.html",
            "https://en.wikipedia.org/wiki/Aquarius_Reef_Base",
            "https://gcaptain.com/1000-feet-below-the-surface-the-extraordinary-world-of-saturation-diving/",
            "https://apps.dtic.mil/sti/tr/pdf/ADA498140.pdf",
            "https://en.wikipedia.org/wiki/Minesto",
        ],
        "shots": shots,
    }
    path = os.path.join(HERE, "plan.json")
    if os.path.exists(path):
        old = json.load(open(path))
        for k in ("cost_preflight", "narration", "voice"):
            if k in old:
                plan[k] = old[k]
        if "reference" in old.get("avatar", {}):
            plan["avatar"]["reference"] = old["avatar"]["reference"]
        plan["notes"] = list(dict.fromkeys(plan["notes"] + old.get("notes", [])))
    json.dump(plan, open(path, "w"), indent=1)
    print("total", round(t, 2), "shots", len(shots), "words", sum(wc(s["line"]) for s in shots))


if __name__ == "__main__":
    build()
