#!/usr/bin/env python3
"""Cross-check TUE-MESTRE-01 weekly frame registry, 14 briefs and independent topics.
Pure stdlib. No publishing, no network, no image generation.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from instagram_preset_mestre import ROOT, check_brief, check_week, verify, PresetError
from instagram_story_gate import verify_linked_stories, StoryGateError

WEEK=ROOT/"content/editorial/semana-independente-2026-11-02-a-08/grade.json"
CATALOG=ROOT/"content/brand/QUADROS-TUE-MESTRE-01.json"
REELS=ROOT/"content/editorial/REELS-E-STORIES-2026-11-02-a-08.json"
STORIES=ROOT/"content/editorial/STORIES-VINCULADOS-2026-11-02-a-08.json"


def verify_reels_and_stories(reels_plan, feed_plan, publication_ledger=None):
    """Fail-closed check of the separate 18h reel / post-publication story plan.

    This does not publish anything or misrepresent a Story upload as a native
    in-app share of the Reel. Provenance and the original video must be verified.
    """
    if (not isinstance(reels_plan, dict) or reels_plan.get("preset_id") != "TUE-MESTRE-01"
            or reels_plan.get("status") != "draft_review_no_publication"):
        raise PresetError("Fila de Reels e Stories fora do padrão mestre ou liberada.")
    spec=reels_plan.get("story_spec", {})
    if (spec.get("text_cta_required") is not True
            or spec.get("native_post_direct_share_only") is not True
            or spec.get("no_external_link_or_link_sticker") is not True
            or spec.get("text_overlay_only") is not True
            or spec.get("spoken_cta_required") is True):
        raise PresetError("Stories exigem compartilhamento direto e CTA somente em texto, sem link externo ou áudio.")
    items=reels_plan.get("reels")
    if not isinstance(items, list) or len(items)!=7:
        raise PresetError("É preciso planejar sete Reels, um por data.")
    feed={entry["day"]: {p["topic_id"] for p in feed_plan["posts"] if p["day"]==entry["day"]}
          for entry in feed_plan["posts"]}
    days=set()
    sources=set()
    for reel in items:
        day=reel.get("day")
        if day not in feed or day in days or reel.get("slot")!="18:00":
            raise PresetError("Reel sem data única ou fora das 18h.")
        days.add(day)
        source=reel.get("source_video_id")
        if source:
            if not isinstance(source,str) or source in sources:
                raise PresetError("Vídeo do YouTube ausente ou reutilizado em outro Reel.")
            sources.add(source)
        if reel.get("topic_id") is not None and reel["topic_id"] in feed[day]:
            raise PresetError("Reel repete tema de um post do feed do mesmo dia.")
        origin=reel.get("ai_origin")
        if origin not in ("unverified","verified_non_synthetic","synthetic"):
            raise PresetError("A origem de IA do vídeo é inválida.")
        if reel.get("approved") is True:
            # A previously published Reel can retain uncertain origin metadata
            # as an historical fact, but ONLY when matched to the immutable
            # real publication ledger. This never approves future media.
            ledger_items = (publication_ledger or {}).get("items", {})
            matches = [record for record in ledger_items.values()
                       if isinstance(record, dict) and record.get("status") == "published"
                       and record.get("instagram_user_id") == "17841433004716815"
                       and record.get("source_video_id") == source
                       and record.get("media_id") == reel.get("reel_media_id")
                       and record.get("permalink") == reel.get("reel_permalink")
                       and str(record.get("media_id", "")).isdigit()]
            historical_receipt = (reel.get("reel_published") is True
                                  and reel.get("source_verified") is True
                                  and bool(reel.get("topic_id"))
                                  and len(matches) == 1)
            # Um Reel original produzido dentro do TUE pode não possuir ID do
            # YouTube. Aceitar essa origem SOMENTE com MP4 imutável hospedado
            # no GitHub, identificação do processo original e QC registrado.
            original_tue_source = (
                reel.get("source_kind") == "tue_original_production"
                and isinstance(reel.get("source_mp4"), str)
                and re.fullmatch(
                    r"https://raw\.githubusercontent\.com/gabrielslinhares12-sudo/"
                    r"instagram-skills/[a-f0-9]{40}/content/media/instagram/"
                    r"2026-11-04/release/Reel-Defesa-Civil-Rasalgethi-LEGENDADO\.mp4",
                    reel["source_mp4"]
                ) is not None
                and reel.get("source_video_id") is None
                and reel.get("ai_origin") == "synthetic"
            )
            if not historical_receipt and (not reel.get("source_verified")
                    or not (source or original_tue_source)
                    or not reel.get("source_mp4") or not reel.get("topic_id")
                    or origin == "unverified"):
                raise PresetError("Reel sem fonte e origem verificadas não pode ser aprovado.")
        if reel.get("reel_published"):
            if not reel.get("approved") or not reel.get("reel_media_id"):
                raise PresetError("Reel publicado sem aprovação ou recibo.")
        if reel.get("story_created") and not reel.get("reel_published"):
            raise PresetError("Story não pode preceder o Reel confirmado.")
        if reel.get("story_published"):
            if (not reel.get("reel_published") or not reel.get("story_media_id")
                    or not reel.get("story_created")
                    or not reel.get("story_native_reshare_confirmed")
                    or not reel.get("story_text_cta_verified")
                    or not reel.get("story_parent_permalink")):
                raise PresetError("Story não pode preceder o Reel ou omitir compartilhamento nativo, texto ou recibo.")
    return {"reels_planned":len(items),"stories_confirmed":sum(bool(x.get("story_published")) for x in items),
            "reels_confirmed":sum(bool(x.get("reel_published")) for x in items)}

def validate(root=ROOT):
    profile=verify(root)
    plan=json.loads((root/WEEK.relative_to(ROOT)).read_text(encoding="utf-8"))
    c=json.loads((root/CATALOG.relative_to(ROOT)).read_text(encoding="utf-8"))
    if c.get("preset_id")!=profile["id"] or c.get("version")!=1:
        raise PresetError("Catálogo de quadros não usa o padrão mestre.")
    names={s["id"] for s in c["series"]}
    frame_kinds={s["id"]:s["format"] for s in c["series"]}
    checked=check_week(plan)
    if len(plan["posts"])!=14 or checked["days_checked"]!=7:
        raise PresetError("A grade precisa de 14 postagens em 7 dias.")
    if len({p["series_id"] for p in plan["posts"]})<6:
        raise PresetError("Faltam quadros diferentes para diversificar a semana.")
    # The feed must rotate formats between both hours. The educational carousel is a series,
    # not a fixed daily format or a compulsory noon post.
    by_slot = {slot: {p["kind"] for p in plan["posts"] if p.get("slot") == slot}
               for slot in ("11:00", "15:00")}
    if any(kinds != {"carousel", "meme"} for kinds in by_slot.values()):
        raise PresetError("Os quadros devem alternar entre 11h e 15h, sem formato fixo.")
    if not any(p.get("series_id") == "carrossel-educativo" for p in plan["posts"]):
        raise PresetError("O quadro Carrossel Educativo deve entrar em rodízio semanal.")
    reels_plan=json.loads((root/REELS.relative_to(ROOT)).read_text(encoding="utf-8"))
    stories_plan=json.loads((root/STORIES.relative_to(ROOT)).read_text(encoding="utf-8"))
    ledger=json.loads((root/"content/publication-state.json").read_text(encoding="utf-8"))
    verify_reels_and_stories(reels_plan, plan, ledger)
    try:
        native_stories=verify_linked_stories(plan, reels_plan, stories_plan)
    except StoryGateError as exc:
        raise PresetError(str(exc)) from exc
    previous_day=None
    day_counts={}
    kinds={"carousel":0,"meme":0}
    for post in plan["posts"]:
        if post.get("series_id") not in names:
            raise PresetError("Quadro editorial não cadastrado.")
        if frame_kinds[post["series_id"]] != post.get("kind"):
            raise PresetError("Quadro incompatível com o formato desta postagem.")
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
    if any(slots!={"11:00","15:00"} for slots in day_counts.values()):
        raise PresetError("Existem horários duplicados ou lacunas.")
    if kinds!={"carousel":7,"meme":7}:
        raise PresetError("Formato/quantidade da grade divergente.")
    return {"ok":True,**checked,"formats":kinds,"series":len({p["series_id"] for p in plan["posts"]}),
            "approval":False,"publications":0,"manual_visual_review":"pending",
            "native_stories":native_stories}

if __name__=="__main__":
    print(json.dumps(validate(),ensure_ascii=False))
