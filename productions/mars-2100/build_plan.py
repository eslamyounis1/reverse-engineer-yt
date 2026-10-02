#!/usr/bin/env python3
"""Builds plan.json for "What If You Were Born on Mars in 2100?" (pre-generation package).
Edited timings are pre-narration estimates; Phase 5 retimes them to Whisper word timestamps."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K, D, R = "KEYFRAME_REQUIRED", "DIRECT_VIDEO", "REUSE_REFERENCE"
STAGE = {0: "newborn", 1: "newborn", 2: "child", 3: "teen", 4: "adult22", 5: "adult30"}

# id, ch, dur, line, scale, source, extra(dict), camera, environment, action, tags
SHOTS = [
 (1, 0, 2.4, "What would happen if you were born on Mars in the year 2100?", "Medium", K,
  {"keyframe_reason": "hook frame: premise + avatar identity (xhigh)"}, "push-in",
  "buried habitat nursery, curved regolith-brick walls, small porthole showing red dust blowing outside, warm amber lamps",
  "newborn avatar in a padded incubator pod opens its button eyes as red dust streaks past the porthole", ["hook"]),
 (2, 1, 2.4, "Day one. You're born under three metres of dirt that blocks radiation.", "Medium", K,
  {"keyframe_reason": "chapter 1 opener: habitat design", "keyframe_is_establishing": True}, "locked",
  "cutaway of habitat dome buried under red regolith mounds, warm interior light, rocky crater outside",
  "a parent in a grey colony jumpsuit lifts the swaddled newborn as soil trickles on the dome roof", []),
 (3, 1, 2.4, "Your first cry, sent by radio,", "Medium Close-Up", K,
  {"keyframe_reason": "diegetic UI: signal-delay counter '12:00' on comms screen", "jcut": 0.25}, "locked",
  "comms alcove, glowing screen with a transmission bar and delay counter reading 12:00",
  "the newborn wails in the foreground while a signal bar crawls across the screen behind", []),
 ("3b", 1, 2.4, "takes twelve minutes to reach Earth.", "Medium Close-Up", R,
  {"reuse_of": "keyframe:shot3", "reuse_mode": "image_references"}, "push-in", "the same comms screen, close",
  "close on the glowing comms screen: the delay counter ticks from 12:00 as the signal bar crawls; the newborn's tiny wool hand rests at the frame edge", ["interrupt"]),
 (4, 1, 2.0, "Your parents carried one gift from Earth:", "Medium Close-Up", R,
  {"reuse_of": "prop:seedcup", "reuse_mode": "image_references", "jcut": 0.3}, "locked", "habitat nursery, warm lamp",
  "a parent's hands lower a dented tin cup of dark soil beside the swaddled newborn, who turns its button eyes toward it", ["plant"]),
 ("4b", 1, 1.6, "an apple seed in a tin cup.", "Close-Up", R,
  {"reuse_of": "prop:seedcup", "reuse_mode": "image_references"}, "push-in", "habitat nursery shelf, warm lamp",
  "tiny wool hand reaches and touches the single apple seed resting on the soil in the tin cup", []),
 (5, 2, 2.6, "Year six. You weigh just over a third of an Earth kid.", "Medium", K,
  {"keyframe_reason": "chapter 2 opener: underground school tunnel", "keyframe_is_establishing": True}, "locked",
  "underground school tunnel, padded walls, painted planet murals, cool white strip lights",
  "six-year-old avatar steps onto a floor scale whose needle barely moves; classmates giggle behind", []),
 (6, 2, 2.4, "Every jump in the school tunnel becomes a slow, floating flight.", "Medium", D,
  {"jcut": 0.1}, "low tracking", "same school tunnel",
  "the child leaps and floats in a long slow arc over a line of laughing classmates", ["interrupt"]),
 (7, 2, 2.6, "Outside, without a suit,", "Medium Close-Up", D,
  {}, "push-in", "airlock chamber, red warning light, pressure gauge",
  "the child in a small orange pressure suit seals a bubble helmet as the airlock light turns from red to green", []),
 ("7b", 2, 2.4, "you'd pass out in seconds as your saliva boils.", "Wide", D,
  {}, "behind follow", "airlock door opening onto the red plain, distant dust devils, butterscotch haze",
  "the suited child steps out of the airlock onto the red plain, helmet visor catching the hazy light", []),
 ("8a", 2, 2.4, "The noon sky is butterscotch.", "Medium", D,
  {}, "locked", "red plain at noon, hazy butterscotch sky, small pale sun overhead",
  "the suited child tilts its helmet back to look up at the butterscotch noon sky", []),
 (8, 2, 2.8, "The sunsets glow blue.", "Wide", K,
  {"keyframe_reason": "composition: tiny suited child silhouetted against a blue Martian sunset"}, "locked",
  "crater rim at dusk, cold blue glow around a small pale sun, butterscotch sky above, long shadows",
  "the suited child stands on the crater rim as the sun sinks and the blue halo spreads", ["interrupt"]),
 (9, 3, 2.6, "Year fourteen. A dust storm swallows the whole planet for months.", "Wide", K,
  {"keyframe_reason": "chapter 3 opener: planet-wide dust storm wall", "keyframe_is_establishing": True}, "locked",
  "habitat observation window, a towering brown dust wall rolling across the plain, light dimming to rust",
  "the teen avatar presses a hand to the window as the dust wall swallows the horizon", ["interrupt"]),
 (10, 3, 2.4, "The solar panels go dark. The colony rations every watt.", "Medium", D,
  {"jcut": 0.15}, "locked", "habitat corridor under red emergency lighting, dust-caked solar panels visible through a porthole",
  "the teen switches off lamps one by one as the corridor drops into red emergency light", []),
 (11, 3, 2.6, "You dig the greenhouse out by hand, sol after sol.", "Medium", D,
  {"jcut": 0.3}, "handheld", "outside the greenhouse dome in swirling brown dust, half-buried dome",
  "the teen in a dusty pressure suit shovels drifts away from the greenhouse door", ["montage"]),
 (12, 3, 2.4, "Your seed is now a sapling, the only green for kilometres.", "Close-Up", R,
  {"reuse_of": "prop:seedcup", "reuse_mode": "image_references"}, "push-in", "greenhouse bench under dim red grow-light",
  "hard colour flip: after the rust-red storm, a vivid green apple sapling glows under the grow-light in the tin cup as the teen's gloved hand cups it", ["interrupt"]),
 (13, 4, 2.6, "Year twenty-two. You finally win a seat on the ship to Earth.", "Medium", K,
  {"keyframe_reason": "chapter 4 opener: launch hall with ship on the pad", "keyframe_is_establishing": True}, "locked",
  "launch hall with a tall window, a silver passenger rocket on the pad outside, pale morning light",
  "the adult avatar raises a glowing boarding token and grins at the rocket outside", []),
 (14, 4, 2.4, "Launch windows open every twenty-six months. You've waited years.", "Wide", D,
  {}, "locked", "launch hall crowd with luggage, departure board glowing, rocket through the window",
  "colonists stream toward a boarding gate while the avatar waits in line clutching a bag", []),
 (15, 4, 2.4, "Then the medical scan flashes red.", "Medium Close-Up", K,
  {"keyframe_reason": "diegetic UI: medical scanner panel flashing red 'NOT CLEARED'"}, "push-in",
  "medical scan booth, scanner arch, red alert panel",
  "the avatar stands in the scanner arch as the panel flashes red and its smile fades", ["turn", "interrupt"]),
 (16, 4, 2.6, "You grew up in Mars gravity. On Earth, you'd feel nearly three times heavier.", "Medium", D,
  {}, "locked", "clinic room with a gravity-simulator harness",
  "in a gravity simulator, the avatar's knees buckle and it grips the handrails, straining", ["turn"]),
 (17, 4, 2.4, "The ship leaves without you.", "Medium", R,
  {"reuse_of": "keyframe:shot13", "reuse_mode": "start_image", "jcut": 0.45}, "locked", "the same launch hall window, rocket lifting off on a pillar of flame",
  "the avatar presses a palm to the window as the rocket rises and the hall trembles", []),
 (18, 5, 2.6, "Year thirty. You run the largest garden on Mars.", "Wide", K,
  {"keyframe_reason": "chapter 5 opener: lush greenhouse dome", "keyframe_is_establishing": True}, "locked",
  "huge greenhouse dome, terraced green rows, misting sprinklers, red cliffs beyond the dome",
  "the adult avatar walks a row of crops with a watering can, mist drifting in shafts of light", []),
 (19, 5, 2.4, "The seed from Earth is now a tree taller than you.", "Medium", R,
  {"reuse_of": "keyframe:shot18", "reuse_mode": "image_references"}, "push-in", "the same greenhouse, a young apple tree at its centre",
  "the avatar reaches up and picks a red apple from the tree", []),
 (20, 5, 2.6, "Then a baby is born in the nursery where you were born.", "Medium", R,
  {"reuse_of": "keyframe:shot1", "reuse_mode": "image_references"}, "locked", "the same nursery and incubator pod from the hook, warm amber lamps",
  "the avatar leans over the incubator as a newborn's hand grips its wool finger", ["interrupt"]),
 (21, 5, 2.6, "You plant a new seed in a tin cup.", "Close-Up", R,
  {"reuse_of": "prop:seedcup", "reuse_mode": "image_references"}, "locked", "nursery shelf beside the incubator",
  "the avatar's hands press an apple seed into soil in a fresh tin cup", []),
 (22, 5, 4.6, "You were never an Earthling on Mars. You're the first Martian.", "Wide", K,
  {"keyframe_reason": "payoff frame: prop callback in final tableau (xhigh)"}, "push-in",
  "greenhouse dome at blue sunset, apple tree behind, red plains and the blue-haloed sun beyond",
  "the avatar looks up at a tiny blue dot (Earth) in the dusk sky, then lifts the tin cup with the new seed toward it, the apple tree glowing behind", ["payoff"]),
]

DIEGETIC = {17: "muffled rocket rumble and window tremble sells the departure; no speech, no music"}
DIFFICULT = {6, 9, 11, 14, 17}


def build():
    shots, t = [], 0.0
    key2id = {str(row[0]): i for i, row in enumerate(SHOTS, 1)}
    for sid0, (key, ch, dur, line, scale, src, extra, cam, env, act, tags) in enumerate(SHOTS, 1):
        sid = sid0
        extra = dict(extra)
        if "reuse_of" in extra and extra["reuse_of"].startswith("keyframe:shot"):
            extra["reuse_of"] = "keyframe:shot%d" % key2id[extra["reuse_of"].split("shot")[1]]
        gen = 5 if sid == len(SHOTS) else 4
        stage = STAGE[ch]
        refs = [f"avatar:stage:{stage}", f"env:ch{max(1, ch)}"]
        if "tin cup" in line or "seed" in line:
            refs.append("prop:seedcup")
        s = {"id": sid, "chapter": ch, "start": round(t, 2), "dur": dur,
             "gen_duration": gen, "useful_window": [0.3, round(min(gen, 0.3 + dur + 0.6), 2)],
             "line": line, "scale": scale, "avatar": True, "avatar_stage": stage,
             "visual_source": src, **extra, "refs": refs,
             "audio": "diegetic" if key in DIEGETIC else "none", "key": str(key),
             "environment": env, "camera": cam, "action": act,
             "difficult": key in DIFFICULT, "tags": tags}
        if key in DIEGETIC:
            s["audio_note"] = DIEGETIC[key]
        shots.append(s)
        t += dur
    plan = {
        "title": "What If You Were Born on Mars in 2100?",
        "premise_type": "lifespan",
        "target_seconds": 55,
        "voice": {"model": "seed_audio", "voice_type": "preset", "voice_id": "bd072316-f77c-588b-b6e5-e46b9b03d008",
                  "name": "Archie (user-selected)", "speech_rate": 25},
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
                    {"chapter": 1, "age": "newborn", "clothing": "silver thermal swaddle + beanie",
                     "state": "pristine, fluffy wool"},
                    {"chapter": 2, "age": "child (6)", "clothing": "cut-down orange colony jumpsuit; outdoors a small "
                     "orange pressure suit with a polycarbonate bubble helmet", "state": "wool slightly fuzzed at elbows"},
                    {"chapter": 3, "age": "teen (14)", "clothing": "patched grey utility coveralls, dust goggles pushed up on the beanie",
                     "state": "red dust worked into the wool edges"},
                    {"chapter": 4, "age": "adult (22)", "clothing": "navy travel jacket with a plain round mission patch, shoulder bag",
                     "state": "neat, freshly washed wool, hopeful"},
                    {"chapter": 5, "age": "adult (30)", "clothing": "green greenhouse apron over coveralls, soil-stained hands",
                     "state": "beanie faded, a few repair stitches in yellow thread, settled and calm"},
                ],
            },
            "reference": {"job_id": None, "approved_by_user": False, "stage_refs": {}},
            "stages": ["newborn", "child", "teen", "adult22", "adult30"],
        },
        "signature_prop": "dented tin cup holding an apple seed sent from Earth (seed -> sapling -> tree -> new seed)",
        "cost_preflight": {"image": None, "video": None, "narration": None, "total": None,
                           "currency": "credits", "approved_by_user": False, "lines": []},
        "notes": [
            "Timings are pre-narration estimates; Phase 5 retimes them to Whisper word timestamps.",
            "dur = final edited hold; gen_duration = Seedance source clip (>=4s), trimmed to useful_window.",
            "Hook contains 'year 2100' inside the question; the validator treats it as premise, not a chapter stamp.",
        ],
        "chapters": [
            {"n": 1, "label": "Day one", "world": "buried habitat nursery, warm amber", "event": "birth under regolith; 12-minute delay; seed gift (plant)"},
            {"n": 2, "label": "Year six", "world": "underground school + crater rim, cool white then blue sunset", "event": "low gravity; first walk outside; blue sunset"},
            {"n": 3, "label": "Year fourteen", "world": "global dust storm, rust light + red emergency", "event": "storm, power rationing, digging out greenhouse; sapling"},
            {"n": 4, "label": "Year twenty-two", "world": "launch hall, pale morning -> red alert", "event": "seat on Earth ship; failed medical scan; ship leaves (turn)"},
            {"n": 5, "label": "Year thirty", "world": "greenhouse dome, lush green + blue sunset", "event": "apple tree; new baby; new seed; reframing payoff"},
        ],
        "sources": [
            "https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html",
            "https://en.wikipedia.org/wiki/Timekeeping_on_Mars",
            "https://www.swri.org/newsroom/press-releases/swri-scientists-publish-first-radiation-measurements-the-surface-of-mars",
            "https://www.jpl.nasa.gov/news/mars-sunset-clip-from-opportunity-tells-dusty-tale/",
            "https://en.wikipedia.org/wiki/2018_Mars_global_dust_storm",
            "https://ntrs.nasa.gov/api/citations/20220013418/downloads/ASCEND-Communication%20Delays,%20Disruptions,%20and%20Blackouts%20for%20Crewed%20Mars%20Missions.pdf",
            "https://en.wikipedia.org/wiki/Launch_window",
            "https://www.sciencedirect.com/science/article/pii/S3117347026000751",
        ],
        "shots": shots,
    }
    # Carry over production state recorded after the plan was first built (approvals, refs, costs).
    path = os.path.join(HERE, "plan.json")
    if os.path.exists(path):
        old = json.load(open(path))
        for k in ("cost_preflight", "narration"):
            if k in old:
                plan[k] = old[k]
        if "voice" in old:
            plan["voice"] = old["voice"]
        for k in ("reference", "core_identity_locked", "notes"):
            if k in old.get("avatar", {}):
                plan["avatar"][k] = old["avatar"][k]
        plan["notes"] = list(dict.fromkeys(plan["notes"] + old.get("notes", [])))
    json.dump(plan, open(path, "w"), indent=1)
    print("total", round(t, 2), "shots", len(shots))


if __name__ == "__main__":
    build()
