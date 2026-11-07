#!/usr/bin/env python3
"""Preflight for Odyssey full film V12. Does not generate visual media or publish.

Validates all 16 scene/64 distinct shot commitments against unmodified 220.56s
user Rasalgethi WAV. Artistic approval requires actual rendered visual inspection;
manifest success must never be mistaken for video completion.
"""
import json
from pathlib import Path
from collections import Counter

HERE=Path(__file__).resolve().parent
DOC=HERE/"film_v12_64shots_220s_manifest.json"
EXPECTED_HASH="9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667"
EXPECTED_FRAMES=13234
m=json.loads(DOC.read_text(encoding="utf8"))
assert m["fps"]==60 and m["width"]==2160 and m["height"]==3840
assert abs(m["voice"]["duration_seconds"]-220.56)<1e-6
assert m["voice"]["sha256"]==EXPECTED_HASH
assert m["voice"]["no_speed_change"] is True
assert m["voice"]["no_regeneration"] is True
assert m["scene_count"]==16 and len(m["scenes"])==16
assert m["shot_count"]==64
assert m["total_frames"]==EXPECTED_FRAMES
assert m["publication_allowed"] is False
assert m["project_status"]!="FINISHED_APPROVED"
ids=set();allsets=set();pos=0;total=0
for i,scene in enumerate(m["scenes"],1):
    assert scene["id"]==f"S{i:02d}"
    assert scene["render_state"]!="APPROVED"
    assert scene["publication_allowed"] is False
    assert len(scene["mandatory_3d_assets"])>=3
    assert len(scene["mandatory_rigged_actions"])>=2
    assert scene["environment"] and scene["environment"] not in allsets,scene["environment"]
    allsets.add(scene["environment"])
    assert len(scene["shots"])>=2
    for shot in scene["shots"]:
        assert shot["id"] not in ids
        ids.add(shot["id"])
        assert shot["source_scene"]==scene["id"]
        assert shot["start_frame_60fps"]==pos,(shot["id"],pos,shot["start_frame_60fps"])
        assert shot["frames_60fps"]>=20,shot["id"]
        pos=shot["end_frame_exclusive_60fps"]
        assert shot["required_event"] and shot["render_state"]=="NOT_BUILT_NOT_APPROVED"
        assert shot["review"]["narrative_silently_clear"]=="pending"
        assert 18<=shot["camera_lens_mm"]<=100
        total+=1
    assert pos==scene["audio"]["end_frame_exclusive"]
assert pos==EXPECTED_FRAMES and total==64 and len(ids)==64 and len(allsets)==16
report={"status":"SHOT_CONTRACT_VALIDATED_NOT_A_RENDER","scenes":len(allsets),
        "unique_shots":total,"frames_60fps":pos,"duration_sec_audio":220.56,
        "original_wav_sha256":EXPECTED_HASH,"visuals_completed":False,
        "publication_authorized":False}
out=HERE/"out"/"v12_film_contract_qc.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2),encoding="utf-8")
print("ODISSEIA_V12_SHOTPLAN_PREFLIGHT_PASSED",json.dumps(report),flush=True)
