#!/usr/bin/env python3
"""Continuously animated S04 QC from the actual rig and 3D prop motions.

No slide show or frame interpolation. One still per alternate native keyframed
Blender animation frame, played at 15fps for 12 seconds, for rapid narrative QC.
Production 4K60 is a separate locked step and does not start before visual QC.
"""
from pathlib import Path
import bpy
import runpy
S=runpy.run_path("odyssey_185/scene04_cyclops_v11.py")
scene=S["scene"]
out=Path("odyssey_185/out/cyclops_v11")
frames=out/"continuous_motion_frames"
frames.mkdir(parents=True,exist_ok=True)
scene.render.image_settings.file_format="PNG"
scene.render.resolution_percentage=75
scene.render.film_transparent=False
# Genuine consecutive animation poses sampled from an 11-12s Blender action,
# no synthesized fake zooms or static PBR snapshots.
count=0
for index,f in enumerate(range(1,361,2),start=1):
 scene.frame_set(f)
 scene.render.filepath=str(frames/("frame-%04d.png"%index))
 bpy.ops.render.render(write_still=True)
 count+=1
 if count%30==0:print("ODYSSEY_V11_REAL_MOTION_PREVIEW",count,"/",180,flush=True)
assert count==180
print("ODYSSEY_V11_REAL_3D_CONTINUOUS_MOTION_FRAMES",count,flush=True)
