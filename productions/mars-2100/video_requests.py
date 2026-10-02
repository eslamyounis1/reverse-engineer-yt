#!/usr/bin/env python3
"""Build Seedance 2.5 request params for every shot from plan.json + manifest.json.

Usage: python3 video_requests.py [--draft] [ids...]   -> JSON list of {index, params}
Rules (SKILL.md E1/E2/E5): duration = gen_duration (>=4), 1080p final (480p draft),
generate_audio only for diegetic shots, media by visual_source / reuse_mode.
"""
import json
import sys

STYLE = "Stylized 3D animated feature-film look, single continuous shot, no cuts, no text, no captions."
CAM = {"locked": "Locked-off camera.", "push-in": "Slow push-in.", "low tracking": "Low tracking camera follows the action.",
       "handheld": "Gentle handheld camera.", "behind follow": "Camera follows from behind.",
       "front-mounted": "Front-mounted camera."}


def main(argv):
    draft = "--draft" in argv
    ids = {int(a) for a in argv if a.isdigit()}
    p = json.load(open("plan.json"))
    m = json.load(open("manifest.json"))
    stage = {k: v["job_id"] for k, v in m["stage_refs"].items()}
    img = m["images"]  # keys: prop, env:chN, kf:<shot id>
    out = []
    for s in p["shots"]:
        if ids and s["id"] not in ids:
            continue
        a, b = s["useful_window"]
        st = stage[s["avatar_stage"]]
        src = s["visual_source"]
        if src == "KEYFRAME_REQUIRED":
            kf = img[f"env:ch{s['chapter']}"] if s.get("keyframe_is_establishing") else img[f"kf:{s['id']}"]
            medias = [{"role": "start_image", "value": kf}]
        elif src == "REUSE_REFERENCE":
            ro = s["reuse_of"]
            ref = img["prop"] if ro.startswith("prop:") else img.get(f"kf:{ro.split('shot')[1]}") or \
                img[f"env:ch{next(x['chapter'] for x in p['shots'] if x['id'] == int(ro.split('shot')[1]))}"]
            if s.get("reuse_mode") == "start_image":
                medias = [{"role": "start_image", "value": ref}]
            else:
                medias = [{"role": "image_references", "value": st}, {"role": "image_references", "value": ref}]
        else:
            medias = [{"role": "image_references", "value": st},
                      {"role": "image_references", "value": img[f"env:ch{max(1, s['chapter'])}"]}]
        who = ("The character from the start image" if medias[0]["role"] == "start_image"
               else "The cream knitted-wool character from the first reference (green button eyes, sunflower-yellow pom-pom beanie)")
        setting = ("as in the start image" if medias[0]["role"] == "start_image" else s["environment"])
        prompt = (f"{s['scale']} shot. {CAM.get(s['camera'], '')} {who}. Setting: {setting}. "
                  f"From {a}s to {b}s: {s['action']}. After that the motion settles and holds. "
                  f"The character keeps its exact design. {STYLE}")
        diegetic = s["audio"] == "diegetic"
        if diegetic:
            prompt += f" Sound: {s['audio_note']}. No speech, no voices, no music."
        params = {"model": "seedance_2_5", "mode": "omni_reference", "aspect_ratio": "9:16",
                  "duration": s["gen_duration"], "resolution": "480p" if draft else "1080p",
                  "generate_audio": diegetic, "medias": medias, "prompt": prompt,
                  # Higgsfield may intercept a submission with a preset recommendation; this Skill
                  # generates its own shots, so the observed recommendation is declined up front.
                  "declined_preset_id": "24bae836-2c4a-48e0-89b6-49fcc0b21612"}
        if draft:
            params["draft"] = True
        out.append({"index": s["id"], "params": params})
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv[1:])
