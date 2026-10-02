#!/usr/bin/env python3
"""Assemble a faceless-what-if Short inside the Higgsfield sandbox (ffmpeg/ffprobe required).

timeline.json:
{
  "fps": 30, "width": 1080, "height": 1920,
  "narration_url": "https://... (wav/mp3)",
  "shots": [{"url": "https://...mp4", "in": 0.3, "dur": 2.4, "label": "DAY 1",
             "gen_duration": 4, "diegetic": false, "diegetic_db": -20}, ...]
}
"still": true marks a shot rendered from an approved keyframe image with a slow push-in
(fallback when a video shot cannot be generated). `dur` is the FINAL EDITED hold (1–5 s). The Seedance source clip is longer (>= 4 s);
`in` = plan.useful_window[0], and the shot is trimmed to [in, in+dur]. A window that runs past
the source clip is a hard failure (no silent freeze-frame padding).
Seedance audio is DROPPED unless the shot is marked "diegetic": true; diegetic audio is
attenuated (diegetic_db, default -20 dB), ducked under the narration (sidechain) and the
receipts assert it peaks >= 6 dB below the narration.
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


def has_audio(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
               "-of", "csv=p=0", path]).strip()
    return bool(out)


def max_volume(path):
    p = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"max_volume: (-?[\d.]+) dB", p.stderr)
    return float(m.group(1)) if m else -91.0


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

    seg_list, aud_list, planned, diegetic_n = [], [], 0.0, 0
    for i, s in enumerate(tl["shots"], 1):
        src = f"clips/shot{i:02d}" + (".png" if s.get("still") else ".mp4")
        fetch(s["url"], src)
        frames = max(1, round(s["dur"] * fps))
        planned += frames / fps
        if s.get("still"):
            # Fallback for a shot Seedance could not render: slow push-in on its approved keyframe.
            seg = f"segs/seg{i:02d}.mp4"
            zp = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
                  f"zoompan=z='min(1+0.0009*on,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={fps},setsar=1")
            run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", src, "-vf", zp, "-frames:v", str(frames),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), seg])
            seg_list.append(seg)
            wav = f"segs/aud{i:02d}.wav"
            run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{frames/fps:.3f}", wav])
            aud_list.append(wav)
            print(f"shot {i:02d}: STILL push-in {frames/fps:.2f}s", file=sys.stderr)
            continue
        cdur = probe(src, "v:0")
        start = float(s.get("in", 0.3))
        if start + s["dur"] > cdur + 0.05:
            raise SystemExit(f"shot {i}: trim window {start:.2f}+{s['dur']:.2f}s exceeds source clip "
                             f"{cdur:.2f}s: fix useful_window or regenerate a longer clip")
        if cdur < 3.9:
            print(f"WARN shot {i}: source clip {cdur:.2f}s is shorter than the 4 s Seedance minimum",
                  file=sys.stderr)
        pad = 0.1  # frame-rounding safety only
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
        # per-shot audio bed: diegetic clip audio (attenuated) or digital silence
        wav = f"segs/aud{i:02d}.wav"
        if s.get("diegetic") and has_audio(src):
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", src, "-vn", "-ac", "1", "-ar", "48000",
                 "-af", f"volume={float(s.get('diegetic_db', -20))}dB,apad", "-t", f"{frames/fps:.3f}", wav])
            diegetic_n += 1
        else:
            if s.get("diegetic"):
                print(f"WARN shot {i}: marked diegetic but source has no audio stream", file=sys.stderr)
            run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
                 "-t", f"{frames/fps:.3f}", wav])
        aud_list.append(wav)
        print(f"shot {i:02d}: source {cdur:.2f}s -> edited in {start:.2f}s dur {frames/fps:.2f}s"
              f"{'  diegetic' if s.get('diegetic') else ''}{'  label ' + label if label else ''}",
              file=sys.stderr)

    with open("segs/list.txt", "w") as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in seg_list)
    # concat FILTER (frame-exact); the concat demuxer with -c copy drifts ~0.03 s per segment
    ins = [x for sg in seg_list for x in ("-i", sg)]
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex",
         "".join(f"[{k}:v]" for k in range(len(seg_list))) + f"concat=n={len(seg_list)}:v=1:a=0[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", str(fps), "video_only.mp4"])
    vdur = probe("video_only.mp4", "v:0")
    if narr > vdur + 0.05:
        raise SystemExit(f"narration {narr:.2f}s longer than picture {vdur:.2f}s: extend final shot dur")

    narr_chain = f"[1:a]loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000,apad=whole_dur={vdur:.3f}"
    sfx_peak = narr_peak = None
    if diegetic_n:
        with open("segs/alist.txt", "w") as f:
            f.writelines(f"file '{os.path.basename(p)}'\n" for p in aud_list)
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "segs/alist.txt",
             "-c:a", "pcm_s16le", "diegetic_bed.wav"])
        # narration keys a sidechain compressor on the diegetic bed, then both are summed
        fc = (f"{narr_chain},asplit=2[nk][nm];[2:a]aresample=48000[bed];"
              f"[bed][nk]sidechaincompress=threshold=0.02:ratio=10:attack=5:release=300[duck];"
              f"[nm][duck]amix=inputs=2:normalize=0:duration=first[a]")
        run(["ffmpeg", "-y", "-v", "error", "-i", "video_only.mp4", "-i", "narration.wav", "-i", "diegetic_bed.wav",
             "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-ar", "48000", "-t", f"{vdur:.3f}", "-movflags", "+faststart", out])
        sfx_peak, narr_peak = max_volume("diegetic_bed.wav"), max_volume("narration.wav")
        assert sfx_peak <= narr_peak - 6, f"diegetic bed peak {sfx_peak} dB not >= 6 dB under narration {narr_peak} dB"
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", "video_only.mp4", "-i", "narration.wav",
             "-filter_complex", f"{narr_chain}[a]",
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
    if diegetic_n:
        print(f"  diegetic  {diegetic_n} shot(s), bed peak {sfx_peak:.1f} dB vs narration peak {narr_peak:.1f} dB "
              f"(pre-duck; ducked under speech)")
    else:
        print("  diegetic  none (all Seedance audio dropped)")
    print("  DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
