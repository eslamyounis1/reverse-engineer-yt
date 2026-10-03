#!/usr/bin/env python3
"""Writes video_requests.json: one seedance_2_5 omni_reference item per shot (Phase 7)."""
import json

p = json.load(open("plan.json"))
STAGE = {"newborn": "c3b30ceb-9bb3-43f9-b94e-7d7d6c261d12", "child": "fb481017-5f8f-4136-8452-0cfee6f96396",
         "teen": "048e6430-4f67-4afc-8de3-d4edbfc36957", "adult22": "765a97cd-00ac-4261-b8a1-63f5e3f62adb",
         "adult30": "096c4764-ec4d-4e81-92bc-4e3c3c63e9e4"}
ENV = {1: "5f888c54-18c4-40fc-898e-6e051a7fbc8d", 2: "98a1bae6-bef3-43a5-94aa-2e017a296caf",
       3: "a8a55784-f1a1-4b4c-a721-25119431e52c", 4: "bdc76e5a-8ee8-45f4-9615-75c62536479d",
       5: "b431034e-ce97-48f5-8d4a-a1514695857b"}
KEYFRAME = {1: "87314528-3d5c-4bae-aede-40ccc49fc222", 12: "c7ca0987-ebbb-4fa2-8f73-d1fbebed16b6",
            23: "76862754-47ae-48a7-8701-a9b315a0f513"}
PROP = "97771449-9f61-407b-b2f7-e20d39268a73"
CAM = {"locked": "Locked-off camera.", "push-in": "Slow push-in.", "low tracking": "Low tracking camera.",
       "behind follow": "Camera follows from behind.", "handheld": "Gentle handheld camera."}
TAIL = ("Stylized 3D animated feature-film look, cinematic motivated lighting, rich saturated colour. "
        "The knitted wool character keeps its exact design: cream wool, glossy green button eyes, sunflower-yellow pom-pom beanie. "
        "Single continuous shot, no cuts, no text, no subtitles.")

reqs = []
for s in p["shots"]:
    a, b = s["useful_window"]
    ch = max(1, s["chapter"])
    src = s["visual_source"]
    if src == "KEYFRAME_REQUIRED":
        kf = KEYFRAME.get(s["id"]) or ENV[ch]
        medias = [{"role": "start_image", "value": kf}]
        lead = f"{s['scale']} shot continuing from the start image."
    elif src == "DIRECT_VIDEO":
        medias = [{"role": "image_references", "value": STAGE[s["avatar_stage"]]},
                  {"role": "image_references", "value": ENV[ch]}]
        if "prop:kite" in s["refs"]:
            medias.append({"role": "image_references", "value": PROP})
        lead = (f"{s['scale']} shot of the knitted wool character from the first reference, "
                f"in the world of the second reference. Setting: {s['environment']}.")
    else:  # REUSE_REFERENCE (prop)
        medias = [{"role": "image_references", "value": STAGE[s["avatar_stage"]]},
                  {"role": "image_references", "value": PROP},
                  {"role": "image_references", "value": ENV[ch]}]
        lead = (f"{s['scale']} shot of the knitted wool character from the first reference with the red kite "
                f"from the second reference, in the world of the third reference. Setting: {s['environment']}.")
    prompt = (f"{lead} {CAM.get(s['camera'], '')} From {a}s to {b}s: {s['action']}. "
              f"After that the motion settles and holds. {TAIL}")
    reqs.append({"index": s["id"], "params": {
        "model": "seedance_2_5", "mode": "omni_reference", "aspect_ratio": "9:16", "resolution": "1080p",
        "duration": s["gen_duration"], "generate_audio": False, "medias": medias, "prompt": prompt}})
json.dump(reqs, open("video_requests.json", "w"), indent=1)
print(len(reqs), "requests")
