#!/usr/bin/env python3
"""Assemble a faceless-what-if Short inside the Higgsfield sandbox (ffmpeg/ffprobe required).

timeline.json:
{
  "fps": 30, "width": 1080, "height": 1920,
  "narration_url": "https://... (wav/mp3)",
  "shots": [{"url": "https://...mp4", "in": 0.2, "dur": 2.4, "label": "DAY 1"}, ...]
}
Usage: python3 assemble_short.py timeline.json --out final_clean.mp4 [--lufs -14] [--no-labels]
Writes ./narration.wav (for the subtitles step), the MP4, and prints RECEIPTS. Idempotent.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-2000:])
        raise SystemExit(f"command failed: {' '.join(cmd[:6])} ...")
    return p.stdout


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return
    if os.path.exists(url):  # local file (testing)
        shutil.copy(url, path)
        return
    for attempt in range(3):
        try:
            urllib.request.urlretrieve(url, path)
            if os.path.getsize(path) > 0:
                return
        except Exception as e:  # noqa: BLE001
            err = e
    raise SystemExit(f"download failed: {path}: {err}")


def probe(path, stream):
    out = run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries",
               "stream=duration", "-of", "csv=p=0", path]).strip().splitlines()
    vals = [float(x) for x in out if x and x != "N/A"]
    if not vals:
        out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
        vals = [float(out.strip())]
    return vals[0]


def font_file():
    for q in ("Montserrat:bold", "TikTok Sans:bold", "DejaVu Sans:bold", "sans:bold"):
        try:
            f = subprocess.run(["fc-match", "-f", "%{file}", q], capture_output=True, text=True).stdout
            if f and os.path.exists(f):
                return f
        except FileNotFoundError:
            break
    return None


def main(argv):
    tl_path = argv[0]
    out = argv[argv.index("--out") + 1] if "--out" in argv else "final_clean.mp4"
    lufs = argv[argv.index("--lufs") + 1] if "--lufs" in argv else "-14"
    labels = "--no-labels" not in argv
    tl = json.load(open(tl_path))
    fps, W, H = tl.get("fps", 30), tl.get("width", 1080), tl.get("height", 1920)
    os.makedirs("clips", exist_ok=True)
    os.makedirs("segs", exist_ok=True)
    font = font_file()

    # narration
    fetch(tl["narration_url"], "narration_src")
    run(["ffmpeg", "-y", "-v", "error", "-i", "narration_src", "-ac", "1", "-ar", "48000", "narration.wav"])
    narr = probe("narration.wav", "a:0")

    seg_list, planned = [], 0.0
    for i, s in enumerate(tl["shots"], 1):
        src = f"clips/shot{i:02d}.mp4"
        fetch(s["url"], src)
        frames = max(1, round(s["dur"] * fps))
        planned += frames / fps
        cdur = probe(src, "v:0")
        start = min(float(s.get("in", 0.2)), max(0.0, cdur - s["dur"]))
        pad = max(0.0, start + s["dur"] - cdur) + 0.5
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},setsar=1,"
              f"tpad=stop_mode=clone:stop_duration={pad:.2f}")
        label = re.sub(r"[^A-Za-z0-9 ]", "", s.get("label") or "").upper().strip()
        if labels and label and font:
            vf += (f",drawtext=fontfile='{font}':text='{label}':fontsize={int(H*0.045)}:fontcolor=white:"
                   f"borderw={int(H*0.004)}:bordercolor=black:x=(w-text_w)/2:y=h*0.14:enable='lt(t,1.2)'")
        seg = f"segs/seg{i:02d}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", src, "-vf", vf, "-frames:v", str(frames),
             "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
             "-r", str(fps), seg])
        seg_list.append(seg)
        print(f"shot {i:02d}: in {start:.2f}s dur {frames/fps:.2f}s{'  label ' + label if label else ''}",
              file=sys.stderr)

    with open("segs/list.txt", "w") as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in seg_list)
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "segs/list.txt", "-c", "copy",
         "video_only.mp4"])
    vdur = probe("video_only.mp4", "v:0")
    if narr > vdur + 0.05:
        raise SystemExit(f"narration {narr:.2f}s longer than picture {vdur:.2f}s: extend final shot dur")

    run(["ffmpeg", "-y", "-v", "error", "-i", "video_only.mp4", "-i", "narration.wav",
         "-filter_complex", f"[1:a]loudnorm=I={lufs}:TP=-1.5:LRA=11,apad=whole_dur={vdur:.3f}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-t", f"{vdur:.3f}", "-movflags", "+faststart", out])
    ov, oa = probe(out, "v:0"), probe(out, "a:0")
    assert abs(ov - oa) <= 0.2, f"A/V mismatch {ov} vs {oa}"
    assert abs(ov - planned) <= 0.2, f"duration {ov} != planned {planned}"
    print("RECEIPTS")
    print(f"  file      {out}  (video {ov:.2f}s / audio {oa:.2f}s, planned {planned:.2f}s)")
    print(f"  shots     {len(seg_list)}  mean hold {planned/len(seg_list):.2f}s")
    print(f"  narration narration.wav  {narr:.2f}s  (tail {vdur-narr:.2f}s)")
    print(f"  labels    {'on' if labels and font else 'off'}")
    print("  DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
