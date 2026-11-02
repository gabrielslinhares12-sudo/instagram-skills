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
        for i, page in enumerate(pages, 1):
            if page.get("source_sha256") != page.get("sha256"):
                raise VisualError("Arte foi alterada durante a montagem.")
            # The cue is part of the individual master JPG. These metadata
            # checks complement, never replace, a manual visual inspection.
            cue = "Arraste →" if i < len(pages) else None
            if "swipe_cue" not in page or page["swipe_cue"] != cue:
                raise VisualError(
                    f"Página {i}: falta 'Arraste →' para indicar continuação, "
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
            # A capa nao comprova audio e MP4. Reels novos requerem liberacao editorial separada.
            raise VisualError("Reel aprovado sem validador dedicado de audio e video; bloquear.")
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
