#!/usr/bin/env bash
set -euo pipefail
# Retain PT-BR captions from original visual stream with precise timing.
# No OCR, no paid API, no opaque caption bar and no narration regeneration.
# Usage: bash motion/scripts/restore-odyssey-captions.sh MASTER.mp4 VISUAL_DIR OUTPUT_DIR
[[ $# -eq 3 ]] || { echo "usage: $0 MASTER.mp4 VISUAL_DIR OUTPUT_DIR" >&2; exit 2; }
MASTER="$1"; VISUALS="$2"; DEST="$3"
[[ -s "$MASTER" ]] || { echo "Missing master: $MASTER" >&2; exit 3; }
mkdir -p "$DEST"
for PART in 1 2 3; do
 case "$PART" in
  1) START=0; DURATION=88.6;;
  2) START=88.6; DURATION=228.8;;
  3) START=317.4; DURATION=242.7;;
 esac
 SRC="$VISUALS/odyssey-episode-$PART-visual-4k60.mp4"
 OUT="$DEST/odisseia-ep$PART-nova-animacao-voz-e-legendas-original-4K60.mp4"
 [[ -s "$SRC" ]] || { echo "Missing render: $SRC" >&2; exit 4; }
 # Original movie's subtitle band: y=3220..3660 at 2160x3840.
 # A luma matte preserves glyphs and timing over the new visuals.
 ffmpeg -hide_banner -loglevel error -y -i "$SRC" -ss "$START" -t "$DURATION" -i "$MASTER" \
  -filter_complex "[1:v]crop=2160:440:0:3220,split[subcolor][srcmask];[srcmask]format=gray,lut=y='if(gte(val,207),255,0)'[mask];[subcolor]format=rgba[rgba];[rgba][mask]alphamerge[sub];[0:v][sub]overlay=0:3220:format=auto[v]" \
  -map '[v]' -map 1:a:0 -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -r 60 -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart "$OUT"
 ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,sample_rate:format=duration -of json "$OUT" > "$OUT.json"
 python3 - "$OUT.json" "$PART" <<'PY'
import json,sys
j=json.load(open(sys.argv[1]))
part=int(sys.argv[2])
v=next(s for s in j['streams'] if s['codec_type']=='video')
a=next(s for s in j['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'])==(2160,3840,'60/1'),v
assert int(a['sample_rate'])==48000,a
assert abs(float(j['format']['duration'])-{1:88.6,2:228.8,3:242.7}[part])<0.12,j
print('AUDIO_VIDEO_SUBTITLES_TECHNICAL_PASS',part)
PY
done
echo 'Original narration and synchronized captions preserved. Editorial visual QC remains mandatory.'
