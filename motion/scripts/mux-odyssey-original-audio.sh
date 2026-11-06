#!/usr/bin/env bash
set -euo pipefail
# Assemble the recovered original 48kHz Portuguese narration into revised silent
# 4K60 Remotion episode renders, without changing speaker or paying for TTS/API.
# Invocation: bash motion/scripts/mux-odyssey-original-audio.sh AUDIO.m4a VIDEO_DIR OUTPUT_DIR
if [ "$#" -ne 3 ]; then
  echo "usage: $0 Odisseia_O_regresso_a_Itaca.m4a path/to/silent/renders path/to/final" >&2
  exit 2
fi
VOICE="$1"; VIDEO_DIR="$2"; OUT_DIR="$3"
test -s "$VOICE" || { echo "Original voice file missing" >&2; exit 3; }
mkdir -p "$OUT_DIR"
for PART in 1 2 3; do
  case "$PART" in
    1) START=0; DURATION=88.6;;
    2) START=88.6; DURATION=228.8;;
    3) START=317.4; DURATION=242.7;;
  esac
  VIDEO="$VIDEO_DIR/odyssey-episode-$PART-visual-4k60.mp4"
  OUT="$OUT_DIR/odisseia-episodio-$PART-com-audio-4k60.mp4"
  test -s "$VIDEO" || { echo "Render missing: $VIDEO" >&2; exit 4; }
  ffmpeg -hide_banner -loglevel error -y \
    -i "$VIDEO" -ss "$START" -t "$DURATION" -i "$VOICE" \
    -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k \
    -ar 48000 -ac 2 -movflags +faststart -shortest "$OUT"
  python3 - "$PART" "$OUT" <<'PY'
import sys,json,subprocess
p=int(sys.argv[1]); f=sys.argv[2]
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
'stream=codec_type,width,height,r_frame_rate,sample_rate:format=duration','-of','json',f]))
v=next(s for s in j['streams'] if s['codec_type']=='video')
a=next(s for s in j['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'])==(2160,3840,'60/1'),v
assert a['sample_rate']=='48000',a
assert abs(float(j['format']['duration'])-{1:88.6,2:228.8,3:242.7}[p])<0.12,j
print('MUX_ORIGINAL_NARRATION_OK',p,f)
PY
done
echo 'OK: three episodes retain original narrator. Visual editorial QC still required.'
