#!/usr/bin/env python3
"""Cross-check TUE-MESTRE-01 weekly frame registry, 14 briefs and independent topics.
Pure stdlib. No publishing, no network, no image generation.
"""
from __future__ import annotations
import json
from pathlib import Path
from instagram_preset_mestre import ROOT, check_brief, check_week, verify, PresetError

WEEK=ROOT/"content/editorial/semana-independente-2026-11-02-a-08/grade.json"
CATALOG=ROOT/"content/brand/QUADROS-TUE-MESTRE-01.json"

def validate(root=ROOT):
    profile=verify(root)
    plan=json.loads((root/WEEK.relative_to(ROOT)).read_text(encoding="utf-8"))
    c=json.loads((root/CATALOG.relative_to(ROOT)).read_text(encoding="utf-8"))
    if c.get("preset_id")!=profile["id"] or c.get("version")!=1:
        raise PresetError("Catálogo de quadros não usa o padrão mestre.")
    names={s["id"] for s in c["series"]}
    checked=check_week(plan)
    if len(plan["posts"])!=14 or checked["days_checked"]!=7:
        raise PresetError("A grade precisa de 14 postagens em 7 dias.")
    if len({p["series_id"] for p in plan["posts"]})<6:
        raise PresetError("Faltam quadros diferentes para diversificar a semana.")
    previous_day=None
    day_counts={}
    kinds={"carousel":0,"meme":0}
    for post in plan["posts"]:
        if post.get("series_id") not in names:
            raise PresetError("Quadro editorial não cadastrado.")
        day_counts.setdefault(post["day"],set()).add(post["slot"])
        bp=root/post["brief_path"]
        if not bp.resolve().is_relative_to((root/WEEK.relative_to(ROOT)).parent.resolve()):
            raise PresetError("Brief aponta para fora da semana.")
        brief=json.loads(bp.read_text(encoding="utf-8"))
        check_brief(brief,profile)
        if any(brief.get(k)!=post.get(k) for k in ("id","day","slot","series_id","topic_id","subject_id","kind")):
            raise PresetError("Brief diverge da grade semanal.")
        if brief.get("publication_attempted") is not False or brief.get("owner_authorized") is not False:
            raise PresetError("Brief simulou publicação ou autorização.")
        if post["kind"] not in kinds:
            raise PresetError("Tipo fora da proposta semanal.")
        kinds[post["kind"]]+=1
        if post["kind"]=="carousel" and len(brief["slides"])<4:
            raise PresetError("Carrossel sem desenvolvimento suficiente.")
        if post["kind"]=="meme" and "CENA 1:" not in brief["slides"][0]["new_information"]:
            raise PresetError("Meme não tem tirinha autoral desenvolvida.")
    if any(slots!={"12:00","18:00"} for slots in day_counts.values()):
        raise PresetError("Existem horários duplicados ou lacunas.")
    if kinds!={"carousel":7,"meme":7}:
        raise PresetError("Formato/quantidade da grade divergente.")
    return {"ok":True,**checked,"formats":kinds,"series":len({p["series_id"] for p in plan["posts"]}),
            "approval":False,"publications":0,"manual_visual_review":"pending"}

if __name__=="__main__":
    print(json.dumps(validate(),ensure_ascii=False))
