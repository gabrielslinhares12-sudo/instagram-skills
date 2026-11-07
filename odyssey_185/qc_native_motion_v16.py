#!/usr/bin/env python3
"""Independent pixel-level proof of continuous native animation in V16 QC clip.

Pass is technical ONLY: it cannot approve story, acting, 3D cinematography
or any social publication. Runs with stdlib and existing FFmpeg binaries.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument("mp4",type=Path)
parser.add_argument("--report",type=Path,default=None)
a=parser.parse_args()
if not a.mp4.is_file() or a.mp4.stat().st_size<50000:
    raise SystemExit("MISSING_OR_EMPTY_NATIVE_VIDEO")
meta=json.loads(subprocess.check_output([
    "ffprobe","-v","error","-select_streams","v:0",
    "-show_entries","stream=width,height,r_frame_rate,nb_frames,codec_name",
    "-of","json",str(a.mp4)],text=True))["streams"][0]
assert meta["codec_name"]=="h264", meta
assert meta["r_frame_rate"]=="30/1", meta
assert int(meta["nb_frames"])==150, meta
assert tuple(int(meta[k]) for k in ("width","height"))==(378,672),meta
width,height=96,170
raw=subprocess.check_output([
    "ffmpeg","-v","error","-i",str(a.mp4),
    "-vf",f"scale={width}:{height},format=gray",
    "-f","rawvideo","-pix_fmt","gray","-"])
n=width*height
assert len(raw)==n*150,(len(raw),n*150)
frames=[memoryview(raw)[i*n:(i+1)*n] for i in range(150)]
hashes=[hashlib.sha256(frame).digest() for frame in frames]
same=sum(x==y for x,y in zip(hashes,hashes[1:]))
# Conservative hard-stop against encoding a single still as moving frames.
assert same<=30,("REPEATED_STATIC_FRAMES",same)
assert hashes[0]!=hashes[-1],"NO_ACTOR_OR_MONOLITH_MOTION_VISIBLE"
# Sampled difference curves; editorially assess action contact separately.
diff=[]
for i in range(1,len(frames)):
    x,y=frames[i-1],frames[i]
    delta=sum(abs(int(a)-int(b)) for a,b in zip(x[::16],y[::16]))/(n//16)
    diff.append(delta)
assert max(diff)>0.12,("NO_VISUAL_MOTION",max(diff))
report={
  "project":"ODISSEIA_TUE","clip":"S04_POLYPHEMUS_3D_QC_V16",
  "technical_status":"REAL_FRAME_SEQUENCE_VERIFIED_ARTISTIC_QC_PENDING",
  "frame_count":150,"fps":30,"resolution":"378x672","codec":"h264",
  "identical_consecutive_frames":same,
  "unique_frames":len(set(hashes)),
  "mean_sampled_pixel_delta":round(sum(diff)/len(diff),4),
  "max_sampled_pixel_delta":round(max(diff),4),
  "narration_integrated":False,"full_film_completed":False,
  "owner_artistic_approval":False,"publication_allowed":False
}
dest=a.report or a.mp4.with_suffix(".motion_qc.json")
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
