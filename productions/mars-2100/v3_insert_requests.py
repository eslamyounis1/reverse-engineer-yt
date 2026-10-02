#!/usr/bin/env python3
"""Seedance 2.5 requests for the 12 cut-v3 insert shots (see v3_inserts.md). DIRECT_VIDEO, 4 s, 1080p, no audio."""
import json
m = json.load(open("manifest.json"))
stage = {k: v["job_id"] for k, v in m["stage_refs"].items()}
env = m["images"]
STYLE = "Stylized 3D animated feature-film look, single continuous shot, no cuts, no text, no letters, no captions."
WHO = "The cream knitted-wool character from the first reference (green button eyes, stitched brown smile, darker cream cheek patch, sunflower-yellow pom-pom beanie)"
INS = [  # key, stage, chapter, scale, camera, action (with avatar unless avatar=False)
 ("1b", "newborn", 1, "Extreme wide aerial", "Slow drone glide forward.", "a cluster of colony domes half-buried in red soil on a rocky Martian plain, a small rover trundling past leaving tracks, warm lights glowing in the dome windows", False),
 ("2b", "newborn", 1, "Wide cross-section", "Slow vertical crane down.", "a cut-away view through thick layers of red dirt revealing a cosy, warmly lit nursery deep underground where the newborn version of the character sleeps swaddled in a crib", True),
 ("7b", "child", 2, "Medium", "Locked-off camera.", "the six-year-old character casually lifts a big metal crate over its head with one hand, grinning, while a classmate beside it stares with jaw dropped", True),
 ("8b", "child", 2, "Medium", "Gentle tilt up then down.", "the child bounces too high, softly bonks its beanie against the padded tunnel ceiling, then drifts slowly down giggling while a teacher in the background shakes her head", True),
 ("13b", "teen", 3, "Extreme wide high-angle", "Locked-off camera.", "a towering rust-red dust wall rolls across the plain and swallows the colony domes one by one, light fading to dim orange", False),
 ("14b", "teen", 3, "Medium", "Locked-off camera.", "in a dim red-lit room the teen character pedals hard on an exercise bike wired to a single small light bulb that flickers brighter, so a younger kid beside it can read a book", True),
 ("15b", "teen", 3, "Medium", "Gentle handheld camera.", "the exhausted dusty teen in a pressure suit flops face-first into a soft drift of red dust, lies still for a beat, then pops back up and keeps shovelling", True),
 ("16b", "teen", 3, "Close-Up", "Slow push-in.", "inside the greenhouse the teen character carefully squeezes a single water drop from an eyedropper onto a tiny green apple sapling in a tin cup, tongue poking out in concentration", True),
 ("17b", "adult22", 4, "Medium", "Locked-off camera.", "the young adult character does a goofy happy victory dance in its small quarters, waving a glowing boarding token above its head", True),
 ("18b", "adult22", 4, "Medium", "Slow push-in.", "the character stands before a wall completely covered in crossed-off paper calendars and draws one final big X with a marker, then steps back proudly", True),
 ("20b", "adult22", 4, "Medium Close-Up", "Locked-off camera.", "the character watches a holographic display in a medical bay: a small glowing hologram of itself standing on a blue planet slowly squashes flat like a pancake, and the real character winces", True),
 ("20c", "adult22", 4, "Medium", "Locked-off camera.", "in a gravity-training room the character grabs a small dumbbell with both hands and strains with all its might, but the dumbbell will not budge from the floor", True),
]
out = []
for i, (k, st, ch, scale, cam, action, av) in enumerate(INS):
    who = (WHO + ". " if av else "")
    prompt = (f"{scale} shot. {cam} {who}Setting: matches the {'second' if av else 'first'} reference. {action}. "
              + ("The character keeps its exact design. " if av else "No characters visible. ") + STYLE)
    out.append({"index": i, "key": k, "params": {"model": "seedance_2_5", "mode": "omni_reference", "aspect_ratio": "9:16",
        "duration": 4, "resolution": "1080p", "generate_audio": False,
        "medias": ([{"role": "image_references", "value": stage[st]}] if av else []) + [{"role": "image_references", "value": env[f"env:ch{ch}"]}],
        "prompt": prompt, "declined_preset_id": "24bae836-2c4a-48e0-89b6-49fcc0b21612"}})
json.dump(out, open("v3_insert_requests.json", "w"), indent=1)
print(json.dumps([o["params"] for o in out]))
