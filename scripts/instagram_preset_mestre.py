#!/usr/bin/env python3
"""TUE-MESTRE-01 editorial guard, pure stdlib. Does NOT create or publish media.

Usage:
  python3 scripts/instagram_preset_mestre.py verify
  python3 scripts/instagram_preset_mestre.py check-brief --brief path.json

Visual aesthetics are NOT provable by hashes or a CI test; the approval gate
requires an explicit accountable visual comparison against the canonical asset.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "content/brand/TUE-MESTRE-01.json"
IDENTITY = "TUE-MESTRE-01"
LUMINO_SHA = "f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b"
VISUAL_MASTER = "content/brand/modelo-oficial-aprovado-2026-11-02.png"
VISUAL_MASTER_SHA = "571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9"


class PresetError(ValueError):
    pass


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PresetError("Configuração não é um objeto JSON.")
    return value


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def verify(root: Path = ROOT) -> dict:
    preset = load_json(root / "content/brand/TUE-MESTRE-01.json")
    brand = load_json(root / "content/brand/padrao-visual.json")
    mirror = load_json(root / "content/visual-standard/standard.json")
    if preset.get("id") != IDENTITY or preset.get("activation_phrase") != "ATIVAR TUE-MESTRE-01":
        raise PresetError("Gatilho TUE-MESTRE-01 inválido ou alterado.")
    # Active standard is the editorial contract approved on 01/11, not an old
    # eight-panel visual reference. Only the canonical mascot is a pinned image.
    assets = preset.get("canonical_assets", {})
    if (assets.get("editorial_contract_id") != IDENTITY
            or assets.get("editorial_contract_path") != "content/brand/TUE-MESTRE-01.md"
            or brand.get("editorial_standard", {}).get("id") != IDENTITY
            or brand["editorial_standard"].get("path") != assets["editorial_contract_path"]
            or mirror.get("editorial_contract", {}).get("id") != IDENTITY
            or mirror["editorial_contract"].get("path") != assets["editorial_contract_path"]):
        raise PresetError("Contrato editorial ativo divergente do TUE-MESTRE-01.")
    if not (root / assets["editorial_contract_path"]).is_file():
        raise PresetError("Contrato editorial TUE-MESTRE-01 ausente.")
    if any(key in assets for key in ("model_path", "model_sha256")):
        raise PresetError("Referência antiga de oito painéis não pode estar ativa.")
    if "reference" in brand or "approved_layout_reference" in mirror:
        raise PresetError("Referência antiga de oito painéis não pode estar ativa.")
    # The owner's 02/11/2026 image is the only current art-direction
    # reference. Pin the exact uploaded bytes, not an approximate recreation.
    master = brand.get("visual_master", {})
    mirror_master = mirror.get("approved_visual_master", {})
    if (assets.get("visual_master_path") != VISUAL_MASTER
            or assets.get("visual_master_sha256") != VISUAL_MASTER_SHA
            or assets.get("visual_master_size") != [1229, 1536]
            or preset.get("visual", {}).get("visual_master_sha256") != VISUAL_MASTER_SHA
            or master.get("path") != VISUAL_MASTER
            or master.get("sha256") != VISUAL_MASTER_SHA
            or mirror_master.get("path") != VISUAL_MASTER
            or mirror_master.get("sha256") != VISUAL_MASTER_SHA
            or sha256(root / VISUAL_MASTER) != VISUAL_MASTER_SHA):
        raise PresetError("Imagem visual-mestre oficial de 02/11 ausente ou modificada.")
    rel = assets.get("lumino_path", "")
    if (rel != "content/brand/lumino-original.png"
            or assets.get("lumino_sha256") != LUMINO_SHA
            or not (root / rel).is_file()
            or sha256(root / rel) != LUMINO_SHA
            or brand["lumino"]["sha256"] != LUMINO_SHA
            or mirror["original_mascot"]["sha256"] != LUMINO_SHA):
        raise PresetError("PNG canônico do Lúmino alterado ou ausente.")
    if brand["output"]["width"] != 1080 or brand["output"]["height"] != 1350:
        raise PresetError("Formato do carrossel foi alterado.")
    if brand["output"]["min_pages"] != 2 or brand["output"]["max_pages"] != 20:
        raise PresetError("Número de lâminas deixou de ser variável.")
    if brand["design"].get("numbering") is not False or preset["visual"]["no_visible_page_numbers"] is not True:
        raise PresetError("Numeração visual proibida pelo TUE-MESTRE-01.")
    cue = preset["visual"].get("swipe_cue")
    brand_cue = brand.get("design", {})
    mirror_cue = mirror.get("swipe_cue", {})
    if (not preset["visual"].get("discreet_swipe_cue")
            or not isinstance(cue, dict)
            or cue.get("text") != "Arraste →"
            or cue.get("required_on_nonfinal_carousel_slides") is not True
            or cue.get("forbidden_on_last_slide") is not True
            or brand_cue.get("swipe_cue_text") != cue["text"]
            or brand_cue.get("swipe_cue_required") is not True
            or brand_cue.get("no_forward_cue_on_last_slide") is not True
            or mirror_cue.get("label") != cue["text"]
            or mirror_cue.get("on") != "all_except_last"
            or cue.get("display_text") != "ARRASTE PARA O LADO →"
            or brand_cue.get("swipe_cue_display_text") != cue["display_text"]
            or mirror_cue.get("display_text") != cue["display_text"]
            or cue.get("progress_dots") is not True
            or brand_cue.get("footer_dots") is not True
            or mirror_cue.get("progress_dots") is not True
            or cue.get("dot_count_matches_carousel_length") is not True
            or mirror_cue.get("dot_count_dynamic") is not True
            or cue.get("position") != "rodapé CENTRAL abaixo da arte, respeitando margem segura; sem cobrir texto, Lúmino ou cena"
            or mirror_cue.get("position") != "bottom_center"
            or mirror_cue.get("no_colored_badge") is not True):
        raise PresetError("Indicação Arraste → não segue o padrão TUE-MESTRE-01.")
    if (not preset.get("visual", {}).get("visual_master_mandatory_for_all_art")
            or not preset.get("reference_style", "").startswith(
                "EXCLUSIVAMENTE a imagem visual-mestre enviada pelo proprietário em 02/11/2026")):
        raise PresetError("Foi alterada a referência visual oficial de 02/11.")
    return preset


def check_brief(brief: dict, preset: dict) -> dict:
    """Fail closed for *new* content, without grandfathering rejected versions."""
    if brief.get("preset_id") != IDENTITY:
        raise PresetError("Brief sem TUE-MESTRE-01: criar conteúdo está bloqueado.")
    if brief.get("reference_standard_id") != IDENTITY or "reference_sha256" in brief:
        raise PresetError("Brief deve usar TUE-MESTRE-01, sem referência antiga de oito painéis.")
    if brief.get("lumino_sha256") != LUMINO_SHA:
        raise PresetError("Brief não usa o Lúmino canônico.")
    if brief.get("status") != "draft_review_no_publication":
        raise PresetError("Produção só pode nascer como rascunho não publicável.")
    if brief.get("approved") is not False:
        raise PresetError("Arte não pode ser aprovada automaticamente.")
    kind = brief.get("kind")
    if kind not in ("carousel", "meme", "single_post", "reel"):
        raise PresetError("Tipo de conteúdo inválido.")
    if not isinstance(brief.get("sources"), list) or not brief["sources"]:
        raise PresetError("Brief sem fontes factuais ou créditos de referências.")
    pages = brief.get("slides")
    if not isinstance(pages, list):
        raise PresetError("Brief sem roteiro por lâmina.")
    if kind == "carousel" and not 2 <= len(pages) <= 20:
        raise PresetError("Carrossel deve ter páginas variáveis entre 2 e 20.")
    if kind in ("meme", "single_post") and len(pages) != 1:
        raise PresetError("Post único deve ter somente uma imagem final.")
    if kind == "reel" and not pages:
        raise PresetError("Reel exige plano visual.")
    seen = set()
    for i, page in enumerate(pages, 1):
        if not isinstance(page, dict):
            raise PresetError("Lâmina inválida.")
        for name in ("headline", "new_information", "distinct_scene", "visual_direction", "source_credit"):
            if not isinstance(page.get(name), str) or len(page[name].strip()) < 8:
                raise PresetError(f"Lâmina {i}: falta {name} detalhado.")
        scene = page["distinct_scene"].casefold().strip()
        if scene in seen:
            raise PresetError("Cenas repetidas: o miolo não acompanha a capa.")
        seen.add(scene)
        if page.get("uses_original_lumino") is not True:
            raise PresetError(f"Lâmina {i}: Lúmino original obrigatório.")
        if kind == "carousel":
            expected_cue = "Arraste →" if i < len(pages) else None
            if page.get("swipe_cue") != expected_cue:
                raise PresetError(
                    f"Lâmina {i}: usar Arraste → nas páginas com continuação e omitir na última."
                )

    return {"preset_id": IDENTITY, "pages": len(pages), "draft_only": True,
            "human_visual_comparison_still_required": True}


def check_week(plan: dict) -> dict:
    """Enforce separate, independent editorial subjects; semantics require human QC."""
    posts = plan.get("posts")
    if not isinstance(posts, list) or not posts:
        raise PresetError("Grade semanal sem publicações.")
    if plan.get("preset_id") != IDENTITY or plan.get("status") != "draft_review_no_publication":
        raise PresetError("Grade fora do TUE-MESTRE-01 ou com liberação indevida.")
    preset = verify()
    production = preset.get("production", {})
    if not all(production.get(key) is True for key in (
            "independent_daily_posts", "no_same_topic_twice_in_one_day",
            "no_companion_memes", "every_post_distinct_subject_in_week")):
        raise PresetError("O bloqueio de temas independentes foi desativado.")
    by_day = {}
    topic_ids, subject_ids, post_ids = set(), set(), set()
    for p in posts:
        if not isinstance(p, dict):
            raise PresetError("Publicação semanal inválida.")
        day, slot = p.get("day"), p.get("slot")
        topic, subject, post_id = p.get("topic_id"), p.get("subject_id"), p.get("id")
        for value in (day, slot, topic, subject, post_id):
            if not isinstance(value, str) or not value.strip():
                raise PresetError("Publicação sem dia, slot ou tema identificável.")
        if len(topic.strip()) < 5 or len(subject.strip()) < 5:
            raise PresetError("Tema vago ou não identificado.")
        if p.get("approved") is not False:
            raise PresetError("Grade não pode aprovar conteúdo automaticamente.")
        if p.get("part_of_series") is True or p.get("companion_to") or p.get("derived_from_post_id"):
            raise PresetError("Publicação derivada/continuação de outro post proibida.")
        if p.get("depends_on_other_post") is True or p.get("same_topic_as"):
            raise PresetError("Posts devem ser autônomos, sem tema compartilhado.")
        dkey, tkey, skey = day.strip(), topic.strip().casefold(), subject.strip().casefold()
        if post_id in post_ids or tkey in topic_ids or skey in subject_ids:
            raise PresetError("Temas duplicados na semana; cada post é individual.")
        if slot in by_day.setdefault(dkey, set()):
            raise PresetError("Dois posts no mesmo horário da mesma data.")
        by_day[dkey].add(slot)
        post_ids.add(post_id)
        topic_ids.add(tkey)
        subject_ids.add(skey)
    return {"preset_id": IDENTITY, "posts_checked": len(posts),
            "days_checked": len(by_day), "distinct_topics": len(topic_ids),
            "independent_subjects": True, "status": "draft_review_no_publication"}

def check_release(manifest: dict) -> None:
    """Required additionally to existing manifest/hash checks before publication."""
    if manifest.get("preset_id") != IDENTITY:
        raise PresetError("PADRÃO TUE-MESTRE-01 não foi ativado neste carrossel.")
    qc = manifest.get("human_visual_qc")
    if not isinstance(qc, dict) or qc.get("reference_standard_id") != IDENTITY:
        raise PresetError("Comparação visual assinada com o TUE-MESTRE-01 está ausente.")
    flags = ("cover_matches_model_1", "inner_pages_match_cover_quality",
             "original_lumino_visually_confirmed", "all_text_readable",
             "all_facts_checked", "sources_and_rights_checked",
             "no_unnecessary_repeated_scenes", "swipe_cue_verified",
             "no_forward_cue_on_last_slide", "no_visible_page_numbers")
    if not all(qc.get(item) is True for item in flags):
        raise PresetError("Revisão manual página por página não foi concluída.")
    if not isinstance(qc.get("reviewer_note"), str) or len(qc["reviewer_note"].strip()) < 30:
        raise PresetError("Falta justificativa específica de comparação com a referência.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["verify", "check-brief", "check-week"])
    parser.add_argument("--brief", type=Path)
    parser.add_argument("--plan", type=Path)
    args = parser.parse_args(argv)
    try:
        preset = verify()
        if args.action == "check-brief":
            if not args.brief:
                raise PresetError("--brief é obrigatório para check-brief.")
            result = check_brief(load_json(args.brief), preset)
        elif args.action == "check-week":
            if not args.plan:
                raise PresetError("--plan é obrigatório para check-week.")
            result = check_week(load_json(args.plan))
        else:
            result = {"verified": True, "preset_id": preset["id"],
                      "activation": preset["activation_phrase"],
                      "manual_artistic_review_required": True}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (PresetError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"verified": False, "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
