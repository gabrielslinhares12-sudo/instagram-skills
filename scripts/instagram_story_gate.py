#!/usr/bin/env python3
"""TUE-MESTRE-01: validação OFFLINE de Stories nativos ligados a posts reais.

Este arquivo somente valida um planejamento; NÃO publica, cria ou simula Stories.
"""
from __future__ import annotations

import json
from pathlib import Path

CTA = "Gostou dessa? Então vai lá, curte o post e segue o Tem Uma Explicação para não perder as próximas!"
METHOD = "share_existing_instagram_post_to_story"
ROOT = Path(__file__).resolve().parent.parent


class StoryGateError(ValueError):
    pass


def verify_linked_stories(feed_plan: dict, reel_plan: dict, story_plan: dict) -> dict:
    if (story_plan.get("preset_id") != "TUE-MESTRE-01" or
            story_plan.get("status") != "planning_only_no_story_assets_created" or
            story_plan.get("do_not_use_as_publish_queue") is not True):
        raise StoryGateError("Plano de Stories deve ficar em planejamento, sem publicação direta.")
    if (story_plan.get("native_share_required") is not True or
            story_plan.get("parent_receipt_required") is not True or
            story_plan.get("text_cta_required") is not True or
            story_plan.get("text_cta") != CTA or
            story_plan.get("no_external_link_or_link_sticker") is not True or
            story_plan.get("narration_required") is not False):
        raise StoryGateError("A republicação nativa sem link extra e o CTA em texto foram alterados.")

    expected = {
        p["id"]: (p["day"], p["slot"], p["kind"])
        for p in feed_plan["posts"]
    }
    for reel in reel_plan["reels"]:
        key = "tue-" + reel["day"] + "-18-youtube-reel"
        if key in expected:
            raise StoryGateError("ID de Reel conflita com item do feed.")
        expected[key] = (reel["day"], "18:00", "reel")

    entries = story_plan.get("entries")
    if not isinstance(entries, list) or len(entries) != len(expected) or len(expected) != 21:
        raise StoryGateError("Exigir um Story planejado para cada um dos 21 posts/Reels.")
    seen = set()
    for item in entries:
        pid = item.get("parent_id")
        if pid not in expected or pid in seen:
            raise StoryGateError("Story sem post existente ou repetido.")
        seen.add(pid)
        if (item.get("day"), item.get("slot"), item.get("parent_kind")) != expected[pid]:
            raise StoryGateError("Story está vinculado ao dia, horário ou tipo errado.")
        if (item.get("native_share_method") != METHOD or item.get("text_cta") != CTA or
                item.get("no_external_link_sticker") is not True):
            raise StoryGateError("Story deve ser republicação nativa com CTA escrito e sem link extra.")
        # Proibir a mídia separada como substituta, inclusive após o post de origem.
        if (item.get("story_media_url") or item.get("independent_story_asset")
                or item.get("external_link_sticker") or item.get("link_url")
                or item.get("story_link_sticker")):
            raise StoryGateError("Story independente é proibido: republicar o post nativo.")
        verified = (item.get("parent_published") is True and
                    item.get("source_verified_by_official_receipt") is True and
                    bool(item.get("parent_media_id")) and bool(item.get("parent_permalink")))
        editing_started = any(item.get(k) is True for k in
                              ("story_created", "text_cta_visible_verified", "story_published",
                               "native_original_post_tappable_verified"))
        if editing_started and not verified:
            raise StoryGateError("Story só pode ser criado depois do post publicado e verificado.")
        if item.get("story_published") is True:
            if (item.get("story_created") is not True or
                    item.get("text_cta_visible_verified") is not True or
                    item.get("native_original_post_tappable_verified") is not True or
                    not item.get("story_media_id")):
                raise StoryGateError("Story não concluído: falta republicação nativa, chamada em texto ou recibo.")
        if item.get("story_media_id") and item.get("story_published") is not True:
            raise StoryGateError("Story tem recibo sem publicação confirmada.")
        if (item.get("voiceover_asset") or item.get("voiceover_created")
                or item.get("spoken_cta_verified")):
            raise StoryGateError("Não usar narração no Story; a chamada é somente escrita.")
        if (item.get("parent_published") is True and
                (not item.get("parent_media_id") or not item.get("parent_permalink") or
                 item.get("source_verified_by_official_receipt") is not True)):
            raise StoryGateError("Post publicado sem recibo de origem verificável.")
    return {"ok": True, "linked_stories_planned":len(entries),
            "stories_published":sum(e["story_published"] is True for e in entries),
            "source_verified_required":True, "native_reshare_required":True,
            "text_cta_required":True, "audio_required":False, "external_link_sticker_forbidden":True}


def main() -> None:
    base = ROOT / "content/editorial"
    feed = json.loads((base / "semana-independente-2026-11-02-a-08/grade.json").read_text(encoding="utf-8"))
    reels = json.loads((base / "REELS-E-STORIES-2026-11-02-a-08.json").read_text(encoding="utf-8"))
    stories = json.loads((base / "STORIES-VINCULADOS-2026-11-02-a-08.json").read_text(encoding="utf-8"))
    print(json.dumps(verify_linked_stories(feed, reels, stories), ensure_ascii=False))


if __name__ == "__main__":
    main()
