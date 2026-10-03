"""Emit the single self-contained sandbox command (assemble -> captions -> upload)."""
import base64, gzip, sys
def b(path): return base64.b64encode(gzip.compress(open(path, "rb").read(), 9)).decode()
up = open(sys.argv[1]).read().strip()
tl = sys.argv[2] if len(sys.argv) > 2 else 'timeline.json'
cmd = f"""set -e; mkdir -p /home/user/wi && cd /home/user/wi
printf '%s' '{b('../../faceless-what-if-shorts/scripts/assemble_short.py')}' | base64 -d | gunzip > assemble_short.py
printf '%s' '{b(tl)}' | base64 -d | gunzip > timeline.json
printf '%s' '{b('script_manifest.json')}' | base64 -d | gunzip > script_manifest.json
python3 assemble_short.py timeline.json --out final_clean.mp4
bash ${{HF_WORKFLOWS}}/subtitles/scripts/fetch_fonts.sh >/dev/null 2>&1 || true
python3 ${{HF_WORKFLOWS}}/subtitles/scripts/audio_to_captions.py narration.wav --srt caps.srt --script script_manifest.json --language en 2>&1 | grep -v HF_TOKEN | tail -n 8
python3 ${{HF_WORKFLOWS}}/subtitles/scripts/subtitle_paper_burn.py --in final_clean.mp4 --srt caps.srt --out final.mp4 --style bold --font-key tiktok 2>&1 | tail -n 3
echo "FINAL $(ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4)"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 final.mp4
[ -s final.mp4 ] && echo "UPLOAD_HTTP $(curl -s -o /dev/null -w '%{{http_code}}' -X PUT -H 'Content-Type: video/mp4' -H 'If-None-Match: *' --upload-file final.mp4 '{up}')"
echo DONE"""
open("assembly_cmd.sh", "w").write(cmd)
print(len(cmd))
