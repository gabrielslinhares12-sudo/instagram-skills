#!/usr/bin/env python3
"""Bloqueio editorial obrigatório para carrosséis TUE; não faz chamadas à Meta."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "content/brand/padrao-visual.json"
DATE_LIMIT = "2026-11-01"
SAFE_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,79}\Z")
HASH = re.compile(r"[a-f0-9]{64}\Z")

class VisualError(ValueError):
    pass

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def safe_file(base: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel or len(rel) > 260:
        raise VisualError("Caminho de midia invalido.")
    base = base.resolve()
    p = (base / rel).resolve()
    if not p.is_relative_to(base) or p.is_symlink():
        raise VisualError("Midia fora do diretorio permitido.")
    return p

def verify_brand(root: Path = ROOT) -> dict:
    """Bind the current editorial contract and the immutable original mascot.

    No eight-panel image reference is permitted as an active template.
    """
    spec = read_json(root / "content/brand/padrao-visual.json")
    expected = {"width": 1080, "height": 1350, "format": "JPEG",
                "min_pages": 2, "max_pages": 20, "automatic_api_max_pages": 10}
    if (spec.get("version") != 2 or spec.get("id") != "TUE-MESTRE-01"
            or spec.get("output") != expected):
        raise VisualError("Configuração atual TUE-MESTRE-01 ou limites alterados.")
    contract = spec.get("editorial_standard", {})
    if (contract.get("id") != "TUE-MESTRE-01"
            or contract.get("path") != "content/brand/TUE-MESTRE-01.md"
            or not (root / contract["path"]).is_file()):
        raise VisualError("Contrato editorial TUE-MESTRE-01 ausente ou divergente.")
    if "reference" in spec:
        raise VisualError("Modelo antigo de oito painéis não pode ser referência ativa.")
    # Compare the exact image uploaded by the owner, never an invented model.
    master = spec.get("visual_master", {})
    path = "content/brand/REFERENCIA-VISUAL-OFICIAL-TUE-MESTRE-01-02NOV2026.jpg"
    digest = "571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9"
    master_path = safe_file(root, path)
    if (master.get("path") != path or master.get("sha256") != digest
            or not master_path.is_file() or sha256(master_path) != digest):
        raise VisualError("Arquivo visual-mestre aprovado pelo proprietário foi alterado ou está ausente.")
    with Image.open(master_path) as approved:
        # The user-provided bytes have a JPEG header (FF D8) despite the
        # original conversation filename ending in .png. Preserve the original
        # byte stream and validate the TRUE encoded format, not its old suffix.
        if approved.format != "JPEG" or approved.size != (1229, 1536):
            raise VisualError("Dimensões ou formato da imagem visual-mestre divergentes.")
    ref = spec.get("reference_visual", {})
    if (ref.get("path") != path or ref.get("sha256") != digest
            or ref.get("width") != 1229 or ref.get("height") != 1536):
        raise VisualError("A referência oficial precisa ser a imagem original aprovada em 02/11, sem recompressão.")
    design = spec.get("design", {})
    if (design.get("footer_dots") is not True or
            design.get("swipe_cue_progress_dots") is not True or
            design.get("swipe_cue_dot_count_dynamic") is not True or
            design.get("swipe_cue_display_text") != "ARRASTE PARA O LADO →" or
            design.get("no_forward_cue_on_last_slide") is not True):
        raise VisualError("Rodapé do carrossel não usa os pontos discretos do modelo oficial.")
    lumino = spec["lumino"]
    asset = safe_file(root, lumino["path"])
    if not asset.is_file() or sha256(asset) != lumino["sha256"]:
        raise VisualError("PNG canônico Lúmino alterado ou ausente.")
    with Image.open(asset) as im:
        if (im.width, im.height) != (lumino["width"], lumino["height"]):
            raise VisualError("Dimensões do PNG Lúmino incorretas.")
    mirror = root / "content/visual-standard/standard.json"
    if mirror.is_file():
        other = read_json(mirror)
        peer_master = other.get("approved_visual_master", {})
        visual_ref = other.get("approved_visual_reference", {})
        if visual_ref.get("path") != path or visual_ref.get("sha256") != digest:
            raise VisualError("Espelho não aponta para o mesmo JPEG visual aprovado.")
        if (peer_master.get("path") != path or peer_master.get("sha256") != digest
                or peer_master.get("required") is not True
                or other.get("swipe_cue", {}).get("position") != "bottom_center"
                or other.get("swipe_cue", {}).get("progress_dots") is not True):
            raise VisualError("Espelho não preserva a imagem-mestre e o rodapé oficial.")
        if "approved_layout_reference" in other or "reference_example_pages" in other.get("output", {}):
            raise VisualError("Espelho visual ainda exige antigo modelo de oito painéis.")
        peer = other["original_mascot"]
        mirror_file = safe_file(root, peer["path"])
        if (peer["sha256"] != lumino["sha256"] or not mirror_file.is_file()
                or sha256(mirror_file) != lumino["sha256"]
                or other.get("editorial_contract", {}).get("id") != "TUE-MESTRE-01"):
            raise VisualError("Espelho Lúmino / contrato editorial divergentes.")
    return spec

def _color_ratio(image: Image.Image, box: tuple[int,int,int,int], predicate, stride: int = 8) -> float:
    crop = image.crop(box).convert("RGB")
    pixels = crop.load()
    total = count = 0
    for y in range(0, crop.height, stride):
        for x in range(0, crop.width, stride):
            total += 1
            if predicate(*pixels[x,y]): count += 1
    return count / max(total,1)

def _lumino_match(image: Image.Image, box: list[int], asset: Path) -> float:
    if not (isinstance(box,list) and len(box)==4 and all(type(n) is int for n in box)):
        raise VisualError("A posicao da PNG original do Lumino deve ser documentada.")
    x,y,w,h = box
    if not (0<=x<1080 and 0<=y<1350 and 160<=w<=550 and 160<=h<=650
            and x+w<=1080 and y+h<=1350):
        raise VisualError("Posicao/tamanho do Lumino fora do template.")
    source = Image.open(asset).convert("RGBA").resize((w,h),Image.Resampling.LANCZOS)
    target = image.crop((x,y,x+w,y+h)).convert("RGB")
    a,b = source.load(),target.load()
    total=count=0
    for yy in range(4,h-4,4):
        for xx in range(4,w-4,4):
            if a[xx,yy][3] >= 250:
                total += sum(abs(a[xx,yy][c]-b[xx,yy][c]) for c in range(3))/3
                count += 1
    if count < 100:
        raise VisualError("Mascote nao tem area suficiente para verificacao.")
    return total/count

INDIVIDUAL_MODE = "individually_art_directed_v1"
LEGACY_MODE = "generic_template_draft_only"


def preview_geometry(count: int) -> tuple[int, int, int, int]:
    """Derived from final page count. Never distort or redraw final artwork."""
    if type(count) is not int or not 2 <= count <= 20:
        raise VisualError("Prévia exige entre 2 e 20 páginas.")
    cols = min(4, count)
    rows = (count + cols - 1) // cols
    return cols, rows, cols * 216, rows * 270


def verify_preview(folder: Path, data: dict) -> None:
    """Contact sheet must match the final JPEGs byte-to-pixel, no creative generation."""
    count = len(data["pages"])
    name = f"PREVIA-{count:02d}-ARTES.png"
    if data.get("preview_file") != name:
        raise VisualError("Prévia não indica a quantidade final de páginas.")
    path = safe_file(folder, name)
    if not path.is_file() or sha256(path) != data.get("preview_sha256"):
        raise VisualError("Prévia ausente ou com hash divergente.")
    columns, rows, width, height = preview_geometry(count)
    with Image.open(path) as actual:
        if actual.format != "PNG" or actual.size != (width, height):
            raise VisualError("Dimensões inválidas da prévia.")
        actual_pixels = actual.convert("RGB").tobytes()
    expected = Image.new("RGB", (width, height))
    for idx, page in enumerate(data["pages"]):
        file = safe_file(folder, page["file"])
        with Image.open(file) as slide:
            thumb = slide.convert("RGB").resize((216, 270), Image.Resampling.LANCZOS)
        expected.paste(thumb, ((idx % columns) * 216, (idx // columns) * 270))
    if expected.tobytes() != actual_pixels:
        raise VisualError("Prévia não corresponde aos JPGs finais.")


def verify_visible_progress_dots(image: Image.Image, index: int, count: int) -> None:
    """Validate painted progress dots, not merely metadata.

    The approved editorial footer uses small yellow/grey dots centered at
    x=534, y=1275, with constant 31px spacing, dynamically distributed for
    any 2..20 slides. Exactly the active index must be yellow; all others
    must be neutral grey. This blocks previous generated-art incidents
    where the first three slides showed the wrong count / active position.
    """
    if (not isinstance(image, Image.Image) or not 2 <= count <= 20
            or not 1 <= index <= count):
        raise VisualError("Parametros de progresso visual invalidos.")
    positions=[round(534 + (j-(count-1)/2)*31) for j in range(count)]
    for j,x in enumerate(positions,1):
        r,g,b=image.convert("RGB").getpixel((x,1275))
        yellow=(r>200 and g>160 and b<120 and r>g and g>b+55)
        grey=(125<=r<=226 and 125<=g<=226 and 125<=b<=226
              and max(r,g,b)-min(r,g,b)<=22)
        if j==index:
            if not yellow:
                raise VisualError(f"Pagina {index}: ponto {j} nao esta amarelo no JPG final.")
        elif not grey:
            raise VisualError(f"Pagina {index}: ponto {j} ausente ou com cor incorreta.")


def validate_package(manifest: Path, root: Path = ROOT) -> dict:
    spec = verify_brand(root)
    data = read_json(manifest)
    if (data.get("version") != 1 or
        data.get("standard_id") != spec["id"] or
        data.get("lumino_sha256") != spec["lumino"]["sha256"] or
        data.get("reference_standard_id") != spec["editorial_standard"]["id"] or
        "reference_sha256" in data):
        raise VisualError("Manifesto não vincula o TUE-MESTRE-01 e Lúmino canônico, ou mantém modelo antigo.")
    pages = data.get("pages")
    limit = spec["output"]
    if not isinstance(pages, list) or not limit["min_pages"] <= len(pages) <= limit["max_pages"]:
        raise VisualError("Carrossel deve ter entre 2 e 20 páginas; uma imagem é post simples.")
    mode = data.get("production_mode", LEGACY_MODE)
    if mode not in {LEGACY_MODE, INDIVIDUAL_MODE}:
        raise VisualError("Processo de produção não autorizado.")
    if mode == INDIVIDUAL_MODE:
        if data.get("reference_visual_sha256") != spec["reference_visual"]["sha256"]:
            raise VisualError("Novo carrossel sem hash do modelo visual original aprovado.")
        for i, page in enumerate(pages, 1):
            if page.get("source_sha256") != page.get("sha256"):
                raise VisualError("Arte foi alterada durante a montagem.")
            # The cue is part of the individual master JPG. These metadata
            # checks complement, never replace, a manual visual inspection.
            cue = "Arraste para o lado →" if i < len(pages) else None
            if "swipe_cue" not in page or page["swipe_cue"] != cue:
                raise VisualError(
                    f"Página {i}: falta 'Arraste para o lado →' com progresso discreto, "
                    "ou existe uma seta incorreta na última."
                )
        verify_preview(manifest.parent, data)
    lumino = root / spec["lumino"]["path"]
    checked=[]
    for index,page in enumerate(pages,1):
        if page.get("number") != index or page.get("layout") not in {"hero","split","diagram"}:
            raise VisualError(f"Pagina {index}: ordem ou layout incorreto.")
        p = safe_file(manifest.parent,page.get("file"))
        if not p.is_file() or not HASH.fullmatch(page.get("sha256","")) or sha256(p)!=page["sha256"]:
            raise VisualError(f"Pagina {index}: JPG ausente ou hash incorreto.")
        with Image.open(p) as original:
            if original.format!="JPEG" or original.size!=(1080,1350):
                raise VisualError(f"Pagina {index}: imagem deve ser JPG 1080x1350.")
            im=original.convert("RGB")
        if mode == INDIVIDUAL_MODE:
            if page.get("dot_count")!=len(pages) or page.get("active_dot")!=index:
                raise VisualError(f"Pagina {index}: progresso do carrossel nao corresponde a quantidade real.")
            verify_visible_progress_dots(im,index,len(pages))
        yellow = _color_ratio(im,(20,118,1060,356),lambda r,g,b:r>190 and g>145 and b<115)
        red = _color_ratio(im,(855,15,1075,130),lambda r,g,b:r>125 and g<110 and b<110)
        light = _color_ratio(im,(16,920,1064,1250),lambda r,g,b:r>168 and g>147 and b>122)
        if yellow<.08 or red<.018 or light<.16:
            raise VisualError(f"Pagina {index}: falta faixa amarela, selo vermelho ou base clara.")
        difference=_lumino_match(im,page.get("mascot_box"),lumino)
        if difference>28:
            raise VisualError(f"Pagina {index}: o Lumino foi redesenhado ou adulterado (erro {difference:.1f}).")
        if not isinstance(page.get("headline"),str) or len(page["headline"].strip())<5:
            raise VisualError(f"Pagina {index}: manchete ausente.")
        checked.append({"number":index,"name":p.name,"sha256":page["sha256"],
                        "match_error":round(difference,2)})
    return {"ok":True,"standard":spec["id"],"pages":checked,"manual_review_required":True}

def spec_max_pages(root: Path = ROOT) -> int:
    return read_json(root / "content/brand/padrao-visual.json")["output"]["automatic_api_max_pages"]


def verify_publication_route(approval: dict) -> None:
    """Fail closed: music in a photo carousel is selected in Instagram mobile UI.

    API publishing has no native carousel-music selection in this project.
    Never publish a silent carousel and call it an audio/Reels experience.
    """
    mode = approval.get("distribution_mode", "native_music_carousel")
    if mode == "native_music_carousel":
        raise VisualError(
            "Carrossel com música nativa: publicar pelo aplicativo Instagram, "
            "não pela API. Música e elegibilidade Reels não são verificáveis aqui."
        )
    if mode == "api_carousel_without_native_music":
        if approval.get("owner_authorized_without_music") is not True:
            raise VisualError(
                "Publicação sem música nativa exige autorização expressa específica."
            )
        return
    if mode == "api_carousel_then_native_music":
        if approval.get("owner_authorized_two_step_music") is not True:
            raise VisualError("Música posterior exige autorização expressa do proprietário.")
        return
    raise VisualError("Modo de distribuição de carrossel não reconhecido.")


def verify_reel_release(root: Path, post: dict) -> str:
    """Fail closed: a Reel needs an immutable MP4, factual QC and owner go-ahead.

    Metadata is a QC receipt, not a substitute for the immutable file SHA.
    All distribution inputs must match the approved fingerprint; a new encode
    demands a new approval. No social network request is performed here.
    """
    slug = post.get("id")
    if not isinstance(slug, str) or not SAFE_ID.fullmatch(slug):
        raise VisualError("Reel com identificador invalido.")
    path = root / "content/approved" / slug / "approval.json"
    if not path.is_file():
        raise VisualError(f"Reel sem recibo de liberacao editorial: {slug}")
    receipt = read_json(path)
    media = post.get("media_urls")
    hashes = post.get("media_sha256")
    cover = post.get("cover_url")
    if (not isinstance(media, list) or len(media) != 1
            or not isinstance(hashes, list) or len(hashes) != 1
            or not isinstance(hashes[0], str) or not HASH.fullmatch(hashes[0])):
        raise VisualError(f"Reel sem MP4 e SHA-256 verificaveis: {slug}")
    # Um unico upload aprovado pelo usuario em 05NOV; demonstrar a origem
    # sem fingir que o transcode Descript preservou os 60 FPS ou a resolucao 4K.
    if slug == "tue-2026-11-05-10-cavalo-de-troia":
        expected_sha = "922844fefb4f668eea141a50eff193eb020a2ae7f6ca4aef4d495792ffa78254"
        media_on_disk = (root / "content/media/instagram/2026-11-05/odisseu-troia"
                         / "Cavalo_Troia_4K60_Meta_10h.mp4")
        expected_url = (
            "https://raw.githubusercontent.com/gabrielslinhares12-sudo/"
            "instagram-skills/705b24db115c4351d4e2b75f051d37d9018158f1/"
            "content/media/instagram/2026-11-05/odisseu-troia/"
            "Cavalo_Troia_4K60_Meta_10h.mp4")
        if (media != [expected_url] or hashes != [expected_sha]
                or not media_on_disk.is_file() or sha256(media_on_disk) != expected_sha
                or receipt.get("owner_authorized") is not True
                or receipt.get("approved") is not True
                or receipt.get("owner_authorizes_only") != slug
                or receipt.get("source_origin") != "user_attachment"
                or receipt.get("source_original_sha256") !=
                   "42da81f753f4251fc5262c33eca115b377f640792cddf6e3f84b4ce30b62f266"
                or receipt.get("source_original_width") != 2160
                or receipt.get("source_original_height") != 3840
                or receipt.get("source_original_fps") != 60
                or receipt.get("release_url") != expected_url
                or receipt.get("media_sha256") != [expected_sha]
                or receipt.get("encoded_width") != 720
                or receipt.get("encoded_height") != 1280
                or receipt.get("encoded_fps") != 30
                or receipt.get("encoded_duration_seconds") != 60
                or receipt.get("encoded_has_audio") is not True
                or receipt.get("not_native_4k") is not True
                or receipt.get("post_due_at") != post.get("due_at")
                or receipt.get("disclosure_review") != post.get("ai_disclosure_review")
                or post.get("ai_origin") != "synthetic"
                or post.get("is_ai_generated") is not True
                or post.get("ai_disclosure_review") !=
                   "mandatory_realistic_synthetic_audio"):
            raise VisualError("Troia 05NOV: arquivo ou aprovacao do usuario divergente.")
        return slug
    # A 40-char commit makes GitHub's raw URL immutable. A mutable branch,
    # signed link or unapproved host must never be used for a release.
    if slug == "tue-2026-11-04-extra-trial-sprites":
        rx = (r"https://raw\.githubusercontent\.com/gabrielslinhares12-sudo/"
              r"instagram-skills/([a-f0-9]{40})/content/media/instagram/"
              r"2026-11-04/trial-sprites-v4-no-top-title/REEL-TRIAL-SPRITES-CLEAN-60FPS\.mp4")
        media_on_disk = (root / "content/media/instagram/2026-11-04/trial-sprites-v4-no-top-title"
                         / "REEL-TRIAL-SPRITES-CLEAN-60FPS.mp4")
        if (not media_on_disk.is_file() or sha256(media_on_disk) != hashes[0]
                or receipt.get("caption_background") is not False or receipt.get("fps") != 60
                or receipt.get("opening_title_duration_seconds") != 0
                or receipt.get("opening_title_duration_seconds") != 0
                or receipt.get("trial_reel") is not True
                or receipt.get("graduation_strategy") != "MANUAL"
                or post.get("trial_reel") is not True):
            raise VisualError(f"Trial Sprites sem integridade ou modo de teste: {slug}")
    elif slug == "tue-2026-11-04-18-titanic-sem-tarjas-v3":
        rx = (r"https://raw\.githubusercontent\.com/gabrielslinhares12-sudo/"
              r"instagram-skills/([a-f0-9]{40})/content/media/instagram/"
              r"2026-11-04/titanic-sem-tarjas-v3/REEL-TITANIC-META-1080X1920-60FPS\.mp4")
        media_on_disk = (root / "content/media/instagram/2026-11-04/titanic-sem-tarjas-v3"
                         / "REEL-TITANIC-META-1080X1920-60FPS.mp4")
        if (not media_on_disk.is_file() or sha256(media_on_disk) != hashes[0]
                or receipt.get("caption_background") is not False or receipt.get("fps") != 60):
            raise VisualError(f"Reel Titanic sem integridade ou legenda limpa: {slug}")
    else:
        rx = (r"https://raw\.githubusercontent\.com/gabrielslinhares12-sudo/"
              r"instagram-skills/([a-f0-9]{40})/content/media/instagram/"
              r"2026-11-04/release/Reel-Defesa-Civil-Rasalgethi-(?:LEGENDADO|META)\.mp4")
    match = re.fullmatch(rx, media[0])
    if not match or not isinstance(cover, str):
        raise VisualError(f"Reel sem origem imutavel ou capa: {slug}")
    if (not cover.startswith("https://raw.githubusercontent.com/"
                             "gabrielslinhares12-sudo/instagram-skills/"
                             + match.group(1) + "/content/media/instagram/2026-11-04/")
            or not cover.endswith(".jpg")):
        raise VisualError(f"Capa do Reel nao corresponde ao commit imutavel: {slug}")
    if (receipt.get("id") != slug or receipt.get("kind") != "reel"
            or receipt.get("preset_id") != "TUE-MESTRE-01"
            or receipt.get("approved") is not True
            or receipt.get("owner_authorized") is not True
            or receipt.get("technical_video_qc_passed") is not True
            or receipt.get("audio_qc_technical_passed") is not True
            or receipt.get("caption_transcript_verified") is not True
            or receipt.get("visual_geometry_qc_passed") is not True
            or receipt.get("subtitles_embedded") is not True
            or receipt.get("caption_segments", 0) < 20
            or receipt.get("video_width") != 1080
            or receipt.get("video_height") != 1920
            or not 40 <= receipt.get("video_duration_seconds", 0) <= (50 if slug == "tue-2026-11-04-extra-trial-sprites" else 45)
            or receipt.get("media_sha256") != hashes
            or receipt.get("release_url") != media[0]
            or receipt.get("cover_url") != cover
            or receipt.get("owner_authorizes_only") != slug
            or receipt.get("disclosure_review") != post.get("ai_disclosure_review")):
        raise VisualError(f"QC de audio/video ou autorizacao incorreta: {slug}")
    if (post.get("ai_origin") != "synthetic"
            or post.get("ai_disclosure_review") != "mandatory_realistic_synthetic_audio"
            or post.get("is_ai_generated") is not True
            or receipt.get("synthetic_voice_disclosure_mandatory") is not True):
        raise VisualError(f"Reel com narracao sintetica sem divulgacao obrigatoria: {slug}")
    return slug


def audit_queue(root: Path=ROOT) -> dict:
    verify_brand(root)
    schedule=read_json(root/"content/schedule.json")
    reviewed=[]
    pending_native_music=[]
    for post in schedule.get("posts",[]):
        if not post.get("approved") or str(post.get("due_at",""))[:10]<DATE_LIMIT:
            continue
        if post.get("kind")=="carousel":
            slug=post.get("id")
            if not isinstance(slug,str) or not SAFE_ID.fullmatch(slug):
                raise VisualError("Id de publicacao nao e seguro.")
            # Exception scoped to the eight ORIGINAL Halloween files approved on
            # 31/10, now re-authorized for the two-step music workflow on 01/11.
            # Never allow other legacy posts to bypass the individual-art QC.
            if slug=="halloween-2026-10-31-historia-8-laminas":
                pinned="f32ed0dae986e38ff058d3ba84f02b6a5c4b94fb"
                prefix=("https://raw.githubusercontent.com/gabrielslinhares12-sudo/"
                        "instagram-skills/"+pinned+"/content/media/halloween-2026-10-31/")
                urls=[prefix+f"{i:02d}-historia-halloween.jpg" for i in range(1,9)]
                hashes=post.get("media_sha256")
                if (post.get("distribution_mode")!="api_carousel_then_native_music"
                        or post.get("owner_authorized_two_step_music") is not True
                        or post.get("is_ai_generated") is not True
                        or post.get("media_urls")!=urls
                        or not isinstance(hashes,list) or len(hashes)!=8):
                    raise VisualError("Recuperação Halloween diferente do material autorizado.")
                for i,expected in enumerate(hashes,1):
                    file=root/"content/media/halloween-2026-10-31"/f"{i:02d}-historia-halloween.jpg"
                    if (not file.is_file() or not HASH.fullmatch(str(expected))
                            or sha256(file)!=expected):
                        raise VisualError("JPG Halloween aprovado modificado ou ausente.")
                    with Image.open(file) as im:
                        if im.format!="JPEG" or im.size!=(1080,1350):
                            raise VisualError("JPG Halloween aprovado em formato incorreto.")
                reviewed.append(slug)
                continue
            # One-time owner's explicit approval of the exact five final
            # renders shown in conversation on 02/11/2026. This does not
            # weaken QC for future posts or any different asset. An original
            # mascot PNG pixel-match is NOT asserted by this special route.
            if slug == "tue-2026-11-02-12-mar-cruzado":
                record=root/"content/approved"/slug/"approval.json"
                if not record.is_file():
                    raise VisualError("Mar Cruzado sem autorização expressa das cinco artes.")
                approval=read_json(record)
                expected=[
                    "6831ca151f9774699026b89d6647f282092af7d3ac5dc1a9df362591261d679c",
                    "372bf00e76ede34f1e6ebd9b996caf25df7b188c94bd275ce495e0060f51c457",
                    "ce862156a6f3e6a0fc2e08781aaf0911cf1176560d33d785f022e45f0cc3fc35",
                    "3a9e3bbe0f0412825cb581e2dd98cf8c75cec3d66dba02669e66bcd82c292702",
                    "977a00814cb18b0c46c4d4dc64dc4e246c1668c06f31d7d604a256ef03fe507c",
                ]
                pinned="f7195510c58c2a8ab7fe45118f184341c0bea791"
                prefix=("https://raw.githubusercontent.com/gabrielslinhares12-sudo/"
                        "instagram-skills/"+pinned+
                        "/content/media/instagram/2026-11-02/mar-cruzado-final/")
                urls=[prefix+f"MAR-CRUZADO-FINAL-{i:02d}.jpg" for i in range(1,6)]
                if (approval.get("id")!=slug
                        or approval.get("preset_id")!="TUE-MESTRE-01"
                        or approval.get("owner_authorized") is not True
                        or approval.get("visual_reviewed") is not True
                        or approval.get("approved") is not True
                        or approval.get("approved_visual_reference_sha256") !=
                           "571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9"
                        or approval.get("approved_media_sha256") != expected
                        or post.get("media_sha256") != expected
                        or post.get("media_urls") != urls
                        or post.get("distribution_mode") != approval.get("distribution_mode")
                        or post.get("owner_authorized_two_step_music") is not True):
                    raise VisualError("Mar Cruzado divergiu dos cinco JPGs aprovados.")
                for i, digest in enumerate(expected, 1):
                    asset=root/"content/media/instagram/2026-11-02/mar-cruzado-final"/f"MAR-CRUZADO-FINAL-{i:02d}.jpg"
                    if not asset.is_file() or sha256(asset)!=digest:
                        raise VisualError("Arquivo exato do Mar Cruzado não foi preservado.")
                    with Image.open(asset) as im:
                        if im.format!="JPEG" or im.size!=(1080,1350):
                            raise VisualError("Imagem do Mar Cruzado tem dimensões divergentes.")
                verify_publication_route(approval)
                reviewed.append(slug)
                continue
            # Scope a one-off exception to five exact JPEGs that the owner
            # visually approved for 03/11, with explicit later authorization
            # to OMIT native music. No claim of mascot pixel equivalence.
            # Other carousel packages must continue through full QC.
            if slug=="tue-2026-11-03-15-atacama-florido":
                folder=root/"content/media/instagram/2026-11-03/final"
                record=root/"content/approved"/slug/"approval.json"
                if not record.is_file():
                    raise VisualError("Atacama sem aprovação específica para postagem sem música.")
                approval=read_json(record)
                names=[f"{i:02d}_03NOV_15H_ATACAMA_0{i-1}.jpg" for i in range(2,7)]
                expected=[
                    "08ca2c522f0768b8f3acd5307127e913eccfad0c23df5066ec5f07be6c1f2e5f",
                    "b35b9e0af99f008b95a89f3f04652470a3d53717cf937c6dec589da3ecb60203",
                    "e717e1338a5d4a68ef87a4b05fa0458a15d51a5f4d61f61659c0d0cc1c86fbff",
                    "4df804be6371acbe6658e5f9b5592996aca73c90d8c0ca8d4cf98d1dd21a8988",
                    "a3d750b169b5dea568f0271e10b449a2de1ae444e4ff6266b0df9c9977e9acc8",
                ]
                pinned="007a7fefb47b303316170c972e0ffdff7d8475dc"
                prefix=("https://raw.githubusercontent.com/gabrielslinhares12-sudo/"
                        "instagram-skills/"+pinned+"/content/media/instagram/2026-11-03/final/")
                urls=[prefix+name for name in names]
                if (approval.get("id")!=slug or approval.get("preset_id")!="TUE-MESTRE-01"
                        or approval.get("approved") is not True
                        or approval.get("owner_authorized") is not True
                        or approval.get("visual_reviewed") is not True
                        or approval.get("distribution_mode")!="api_carousel_without_native_music"
                        or approval.get("owner_authorized_without_music") is not True
                        or approval.get("precise_release_scope") != "EXACT_FIVE_JPEG_HASHES_ONLY__03NOV_15H"
                        or approval.get("approved_visual_reference_sha256") !=
                           "571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9"
                        or approval.get("original_mascot_pixel_match_verified") is not False
                        or approval.get("media_sha256")!=expected
                        or post.get("media_sha256")!=expected
                        or post.get("media_urls")!=urls
                        or post.get("distribution_mode")!=approval.get("distribution_mode")
                        or post.get("owner_authorized_without_music") is not True):
                    raise VisualError("O Atacama divergiu das artes, da rota ou da autorização do dono.")
                for name,digest in zip(names,expected):
                    image_file=folder/name
                    if not image_file.is_file() or sha256(image_file)!=digest:
                        raise VisualError("Atacama original ausente ou modificado.")
                    with Image.open(image_file) as im:
                        if im.format!="JPEG" or im.size!=(1080,1350):
                            raise VisualError("O arquivo Atacama não é JPEG 1080x1350.")
                verify_publication_route(approval)
                reviewed.append(slug)
                continue
            # Carrossel Boston 04NOV: autorização expressa do usuário para as
            # CINCO artes exatas visivelmente aprovadas. Não declarar
            # correspondência pixel-a-pixel do Lúmino (imagem ilustrada).
            # Exceção de lançamento estritamente vinculada a SHA256, commit,
            # ordem, legenda e rota Meta sem música. Não altera QC geral.
            if slug == "tue-2026-11-04-boston-1919-carrossel-imediato":
                folder=root/"content/media/instagram/2026-11-04/boston-aprovado-publicacao"
                record=root/"content/approved"/slug/"approval.json"
                if not record.is_file():
                    raise VisualError("Boston 04NOV sem recibo editorial específico.")
                approval=read_json(record)
                expected=[
                    "08d7586dbd5128e6724961b70bd424f8304165fa98bf76f3b8c6b2911f5db342",
                    "73a1bc03a2e3ba6c4bd90b29a3a011554c1ee5aee65702f2c4dfe5c8c0b38be5",
                    "891858906de4b4c4110b242e7a3b47f12744b0d0896b54dc7989b5994fd94ff6",
                    "6257fa8efdb1d99678ae6d1e95be3dd1169e707363be4af7ae9915b18a46e136",
                    "9a859f7017e94f4c696e817e83fe96bc38fd51a0ae48ec27a7569f7501147336",
                ]
                pinned="5771a6ee4c61f44561f77d4a0e0712f83d420f61"
                prefix=("https://raw.githubusercontent.com/gabrielslinhares12-sudo/"
                        "instagram-skills/"+pinned+
                        "/content/media/instagram/2026-11-04/boston-aprovado-publicacao/")
                urls=[prefix+f"BOSTON-CARROSSEL-FINAL-{i:02d}.jpg" for i in range(1,6)]
                if (approval.get("id") != slug
                        or approval.get("kind") != "carousel"
                        or approval.get("preset_id") != "TUE-MESTRE-01"
                        or approval.get("approved") is not True
                        or approval.get("visual_reviewed") is not True
                        or approval.get("owner_authorized") is not True
                        or approval.get("precise_release_scope") !=
                           "ONLY_EXACT_FIVE_BOSTON_04NOV_NOV2026_JPEG_HASHES"
                        or approval.get("original_mascot_pixel_match_verified") is not False
                        or approval.get("approved_visual_reference_sha256") !=
                           "571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9"
                        or approval.get("media_sha256") != expected
                        or approval.get("media_urls") != urls
                        or approval.get("release_commit") != pinned
                        or post.get("media_sha256") != expected
                        or post.get("media_urls") != urls
                        or post.get("caption") != approval.get("caption")
                        or approval.get("distribution_mode") != "api_carousel_without_native_music"
                        or approval.get("owner_authorized_without_music") is not True
                        or post.get("distribution_mode") != "api_carousel_without_native_music"
                        or post.get("owner_authorized_without_music") is not True
                        or post.get("ai_origin") != "synthetic"
                        or post.get("content_style") != "clearly_illustrated"
                        or post.get("ai_disclosure_review") !=
                           "no_mandatory_self_disclosure_for_stylized_still"):
                    raise VisualError("Boston 04NOV não corresponde às cinco artes autorizadas.")
                for i,digest in enumerate(expected,1):
                    image_file=folder/f"BOSTON-CARROSSEL-FINAL-{i:02d}.jpg"
                    if not image_file.is_file() or sha256(image_file)!=digest:
                        raise VisualError("Arquivo aprovado do Boston ausente ou modificado.")
                    with Image.open(image_file) as im:
                        if im.format!="JPEG" or im.size!=(1080,1350):
                            raise VisualError("Boston deve ter cinco JPGs 1080x1350.")
                verify_publication_route(approval)
                reviewed.append(slug)
                continue
            manifest=root/"content/approved"/slug/"visual-manifest.json"
            if not manifest.is_file():
                raise VisualError(f"Carrossel aprovado sem verificacao de estilo: {slug}")
            validated=validate_package(manifest,root)
            approval=read_json(manifest)
            # TUE-MESTRE-01: no new approved carousel may bypass manual
            # comparison to the exact original model 1 and all inner slides.
            from instagram_preset_mestre import PresetError, check_release
            try:
                check_release(approval)
            except PresetError as error:
                raise VisualError(str(error)) from error
            # A color/mascot-valid generic template is NEVER publishable.
            # Only independent artwork, preserved byte-for-byte, can advance.
            if approval.get("production_mode") != INDIVIDUAL_MODE:
                raise VisualError(f"Gerador genérico proibido na publicação: {slug}")
            if len(validated["pages"]) > spec_max_pages(root):
                raise VisualError(
                    f"Carrossel {slug}: API automática aceita no máximo 10 páginas. "
                    "Escolha Reel MP4 ou publicação manual, sem descartar imagens."
                )
            # A generated QA manifest defaults to approved=false. Technical
            # integrity alone NEVER authorizes publication.
            if (approval.get("approved") is not True
                    or approval.get("visual_reviewed") is not True
                    or approval.get("owner_authorized") is not True
                    or not isinstance(approval.get("approval_note"),str)
                    or not approval["approval_note"].strip()):
                raise VisualError(f"Carrossel sem revisao e autorizacao expressa: {slug}")
            hashes=[p["sha256"] for p in validated["pages"]]
            if hashes!=post.get("media_sha256"):
                raise VisualError(f"Os hashes do carrossel aprovado nao sao os mesmos do QA: {slug}")
            urls=post.get("media_urls",[])
            if len(urls)!=len(hashes) or any(not isinstance(u,str) or "raw.githubusercontent.com/" not in u
                                  for u in urls):
                raise VisualError(f"URLs do carrossel nao estao prontas: {slug}")
            if approval.get("distribution_mode", "native_music_carousel") == "native_music_carousel":
                # A good approved photo carousel may be staged, but cannot be sent
                # without its requested native audio via the official Graph API.
                pending_native_music.append(slug)
                continue
            verify_publication_route(approval)
            reviewed.append(slug)
        elif post.get("kind")=="reel":
            reviewed.append(verify_reel_release(root, post))
        elif post.get("kind")=="post":
            # Memes may use their own visual language, but still require a
            # separate review of their exact image and an owner authorization.
            slug=post.get("id")
            if not isinstance(slug,str) or not SAFE_ID.fullmatch(slug):
                raise VisualError("Id de post invalido.")
            record=root/"content/approved"/slug/"approval.json"
            if not record.is_file():
                raise VisualError(f"Post individual sem documento de aprovacao: {slug}")
            item=read_json(record)
            if not (item.get("owner_authorized") is True
                    and item.get("visual_reviewed") is True
                    and item.get("media_sha256") == post.get("media_sha256")
                    and len(post.get("media_urls",[])) == 1):
                raise VisualError(f"Post individual sem autorizacao especifica: {slug}")
        else:
            raise VisualError("Tipo de midia nao coberto pelo controle editorial.")
    return {"ok":True,"approved_new_carousels_checked":reviewed,
            "native_music_carousels_waiting_for_compatible_publication":pending_native_music,
            "approved_posts_unchanged":True}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=["verify-assets","verify-package","audit-queue"])
    parser.add_argument("--manifest",type=Path)
    args=parser.parse_args(argv)
    try:
        if args.mode=="verify-assets": result={"ok":True,"assets":list(verify_brand())[:3]}
        elif args.mode=="audit-queue":result=audit_queue()
        else:
            if args.manifest is None: raise VisualError("--manifest e obrigatorio.")
            result=validate_package(args.manifest.resolve())
        print(json.dumps(result,ensure_ascii=False))
        return 0
    except (VisualError, OSError, ValueError, KeyError) as e:
        print(json.dumps({"ok":False,"error":str(e)},ensure_ascii=False),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
