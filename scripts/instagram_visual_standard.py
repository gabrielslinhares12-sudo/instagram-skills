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
    spec = read_json(root / "content/brand/padrao-visual.json")
    if spec.get("version") != 1 or spec.get("output") != {
        "width": 1080, "height": 1350, "format": "JPEG", "pages": 8
    }:
        raise VisualError("A configuracao do formato foi alterada.")
    for item in ("reference", "lumino"):
        ref = spec[item]
        asset = safe_file(root, ref["path"])
        if not asset.is_file() or sha256(asset) != ref["sha256"]:
            raise VisualError(f"Ativo canonico alterado ou ausente: {item}")
        with Image.open(asset) as im:
            if (im.width, im.height) != (ref["width"], ref["height"]):
                raise VisualError(f"Dimensoes do ativo canonico incorretas: {item}")
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

def validate_package(manifest: Path, root: Path = ROOT) -> dict:
    spec = verify_brand(root)
    data = read_json(manifest)
    if (data.get("version") != 1 or
        data.get("standard_id") != spec["id"] or
        data.get("lumino_sha256") != spec["lumino"]["sha256"] or
        data.get("reference_sha256") != spec["reference"]["sha256"]):
        raise VisualError("Manifesto nao vincula as duas referencias oficiais.")
    pages = data.get("pages")
    if not isinstance(pages,list) or len(pages)!=8:
        raise VisualError("Cada carrossel deve ter exatamente 8 paginas.")
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

def audit_queue(root: Path=ROOT) -> dict:
    verify_brand(root)
    schedule=read_json(root/"content/schedule.json")
    reviewed=[]
    for post in schedule.get("posts",[]):
        if not post.get("approved") or str(post.get("due_at",""))[:10]<DATE_LIMIT:
            continue
        if post.get("kind")=="carousel":
            slug=post.get("id")
            if not isinstance(slug,str) or not SAFE_ID.fullmatch(slug):
                raise VisualError("Id de publicacao nao e seguro.")
            manifest=root/"content/approved"/slug/"visual-manifest.json"
            if not manifest.is_file():
                raise VisualError(f"Carrossel aprovado sem verificacao de estilo: {slug}")
            validated=validate_package(manifest,root)
            hashes=[p["sha256"] for p in validated["pages"]]
            if hashes!=post.get("media_sha256"):
                raise VisualError(f"Os hashes do carrossel aprovado nao sao os mesmos do QA: {slug}")
            urls=post.get("media_urls",[])
            if len(urls)!=8 or any(not isinstance(u,str) or "raw.githubusercontent.com/" not in u
                                  for u in urls):
                raise VisualError(f"URLs do carrossel nao estao prontas: {slug}")
            reviewed.append(slug)
        elif post.get("kind")=="reel":
            # A capa nao comprova audio e MP4. Reels novos requerem liberacao editorial separada.
            raise VisualError("Reel aprovado sem validador dedicado de audio e video; bloquear.")
    return {"ok":True,"approved_new_carousels_checked":reviewed,
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
