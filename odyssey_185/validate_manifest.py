#!/usr/bin/env python3
"""Preflight for the new 185-second Odyssey. No rendering, no Instagram writes."""
import json
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
m=json.loads((P/"manifest_v9.json").read_text(encoding="utf-8"))
narr=(P/"narracao_rasalgethi.txt").read_text(encoding="utf-8").strip().split("\n\n")
scenes=m["scenes"]
assert m["target_seconds"]==185
assert len(scenes)==m["scene_count"]==len(narr)==16
assert (m["format"]["width"],m["format"]["height"],m["format"]["fps"])==(2160,3840,60)
assert m["voice"]["name"]=="Rasalgethi" and m["voice"]["api_paid"] is False
assert m["publication"]["enabled"] is False
assert scenes[0]["start_seconds"]==0 and scenes[-1]["end_seconds"]==185
for i,s in enumerate(scenes):
    assert s["id"]=="S"+str(i+1).zfill(2)
    assert s["end_seconds"]>s["start_seconds"],s
    assert s["duration_seconds"]==s["end_seconds"]-s["start_seconds"],s
    assert i==0 or scenes[i-1]["end_seconds"]==s["start_seconds"],s
    assert s["narration"]==narr[i],s["id"]
    assert len(s["cast"])>0 and len(s["action_contract"])>40,s["id"]
    assert s["animation_required"] and s["material_3d_required"]
    assert s["approved_for_render"] is False
tot=sum(len(s["narration"].split()) for s in scenes)
assert 400<=tot<=500,tot
assert m["asset_contracts"]["Polifemo"]["eye_count"]==1
assert m["asset_contracts"]["axes"]["count"]==12
assert m["asset_contracts"]["trojan_horse"]["legs"]==4
assert "Runway" in m["engine"] and "no Runway" in m["engine"]
assert "no 2D overlays" in m["art_direction"]["no"]
assert (P/"render_hook_3d.py").is_file()
rows=[{"id":s["id"],"duration":s["duration_seconds"],
       "words":len(s["narration"].split()),
       "words_per_minute":round(60*len(s["narration"].split())/s["duration_seconds"])}
      for s in scenes]
report={"project":"ODYSSEY_185_3D_V9","timeline_covered_seconds":185,
        "narration_word_count":tot,"overall_words_per_minute":round(tot*60/185),
        "cast_identifiers":dict(Counter(x for s in scenes for x in s["cast"])),
        "time_beats":rows,"render_ready":False,
        "reasons":["No 185s Rasalgethi WAV obtained from AI Studio web",
                   "15 scenes lack 3D film animation implementation",
                   "Scene01 pilot has not passed artistic QC"],
        "publication_allowed":False}
(P/"out").mkdir(exist_ok=True)
(P/"out"/"preflight.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
print("PASS 185-sec scene coverage and script integrity")
print("PASS cast/prop scale contracts",m["asset_contracts"]["Polifemo"])
print("PASS per-scene narration mapping, total words",tot)
print("FAIL-CLOSED publication=False full-render=False")
