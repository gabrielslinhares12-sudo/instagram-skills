#!/usr/bin/env python3
"""Compositor oficial de carrossel TUE: usa PNG canônica, nunca gera personagem."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

from instagram_visual_standard import ROOT, VisualError, safe_file, sha256, verify_brand, validate_package

SIZE=(1080,1350)
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_BODY="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
PAPER=(246,237,222)
YELLOW=(255,214,0)
RED=(213,14,21)
INK=(17,17,17)

def font(size:int, bold:bool=True):
    path=FONT_BOLD if bold else FONT_BODY
    return ImageFont.truetype(path,size)

def wrap(draw, text:str, width:int, max_lines:int, start_size:int, min_size:int):
    if not isinstance(text,str) or not text.strip():
        raise VisualError("Texto vazio na imagem.")
    for size in range(start_size,min_size-1,-2):
        f=font(size)
        words=text.strip().split()
        lines=[];line=""
        for word in words:
            candidate=(line+" "+word).strip()
            if draw.textbbox((0,0),candidate,font=f)[2] <= width:
                line=candidate
            else:
                if line:lines.append(line)
                line=word
        if line:lines.append(line)
        if len(lines)<=max_lines and all(draw.textbbox((0,0),x,font=f)[2]<=width for x in lines):
            return f,lines
    raise VisualError("Texto comprido para o template; encurte a manchete ou explicacao.")

def brush(draw, idx):
    random.seed(600+idx)
    top=139
    points=[(24,top+17),(80,top+4),(220,top+9),(370,top-8),(540,top+6),
            (720,top-1),(900,top+7),(1055,top+14),(1042,348),
            (900,343),(728,351),(530,347),(380,359),(172,353),(34,355)]
    draw.polygon(points,fill=YELLOW)
    for z in range(7):
        x=random.randint(30,950)
        y=random.randint(133,153)
        draw.line((x,y,x+random.randint(35,120),y-5),fill=YELLOW,width=random.randint(3,9))
    draw.line((26,358,960,358),fill=(243,186,1),width=5)

def scene(base, photo, secondary, layout):
    draw=ImageDraw.Draw(base)
    # Drop-shadowed photograph panels; photographs never contain the mascot.
    if layout=="split":
        if secondary is None:raise VisualError("Layout split exige imagem secundaria diferente.")
        for image, rect in ((photo,(30,396,540,942)),(secondary,(548,396,1050,942))):
            frame=(rect[0]-5,rect[1]-5,rect[2]+5,rect[3]+5)
            draw.rounded_rectangle(frame,25,fill=(231,215,192))
            fitted=ImageOps.fit(image.convert("RGB"),(rect[2]-rect[0],rect[3]-rect[1]),
                                method=Image.Resampling.LANCZOS,centering=(.5,.4))
            mask=Image.new("L",fitted.size)
            ImageDraw.Draw(mask).rounded_rectangle((0,0,*fitted.size),radius=23,fill=255)
            base.paste(fitted,(rect[0],rect[1]),mask)
    else:
        rect=(30,396,1050,943)
        draw.rounded_rectangle((24,390,1056,949),radius=30,fill=(235,216,192))
        fitted=ImageOps.fit(photo.convert("RGB"),(1020,547),
                            method=Image.Resampling.LANCZOS,centering=(.5,.45))
        mask=Image.new("L",(1020,547));ImageDraw.Draw(mask).rounded_rectangle((0,0,1020,547),radius=28,fill=255)
        base.paste(fitted,(30,396),mask)
        if layout=="diagram":
            draw.rounded_rectangle((710,735,1022,915),radius=24,fill=(247,241,229),outline=(255,214,0),width=9)
            draw.line((756,864,968,779),fill=RED,width=13)
            draw.ellipse((747,852,775,880),fill=RED)
            draw.ellipse((956,766,986,796),fill=INK)

def render_one(item, number, lumino, output:Path, specdir:Path):
    for field in ("headline","body","photo","credit"):
        if not isinstance(item.get(field),str) or not item[field].strip():
            raise VisualError("Cada pagina exige headline, body, photo e credit.")
    if len(item["body"])>280:
        raise VisualError("Texto do corpo muito longo para mobile.")
    layout=item.get("layout",["hero","split","diagram"][number%3])
    if layout not in {"hero","split","diagram"}:raise VisualError("Layout desconhecido.")
    p=safe_file(specdir,item["photo"])
    if not p.is_file():raise VisualError("Fotografia/ilustracao de fundo nao encontrada.")
    secondary=None
    if layout=="split":
        q=safe_file(specdir,item.get("photo_secondary",""))
        if not q.is_file() or sha256(q)==sha256(p):
            raise VisualError("Layout comparativo exige segunda imagem diferente.")
        secondary=Image.open(q).convert("RGB")
    photo=Image.open(p).convert("RGB")
    image=Image.new("RGB",SIZE,PAPER)
    draw=ImageDraw.Draw(image)
    # Textura clara; reforco editorial, nao fundo escuro.
    random.seed(number*71)
    for _ in range(8500):
        xx=random.randrange(1080);yy=random.randrange(1350)
        tint=random.randrange(233,246)
        draw.point((xx,yy),fill=(tint,tint-7,tint-20))
    draw.rectangle((0,0,1080,98),fill=(248,242,232))
    draw.line((30,95,520,95),fill=RED,width=8)
    draw.text((35,26),"TEM UMA EXPLICAÇÃO  •  LÚMINO INVESTIGA",
              fill=INK,font=font(34))
    draw.rounded_rectangle((859,21,1058,105),radius=18,fill=RED)
    draw.text((880,42),f"PÁG. {number}/8",fill="white",font=font(38))
    brush(draw,number)
    headline=item["headline"].upper()
    f,lines=wrap(draw,headline,962,3,85,46)
    step=f.size+5
    y=172+(3-len(lines))*12
    for line in lines:
        draw.text((52,y),line,font=f,fill=INK,stroke_width=0);y+=step
    scene(image,photo,secondary,layout)
    draw=ImageDraw.Draw(image)
    # Cartao claro para leitura, sobre a area inferior da imagem.
    draw.rounded_rectangle((288,956,1055,1180),radius=33,fill=(252,248,240),
                           outline=(219,205,181),width=4)
    f,lines=wrap(draw,item["body"],704,5,44,29)
    totalh=len(lines)*(f.size+11)
    y=978+max(0,(180-totalh)//2)
    for line in lines:
        draw.text((321,y),line,fill=INK,font=f);y+=f.size+11
    draw.rounded_rectangle((330,1193,1002,1271),radius=21,fill=RED)
    callout=item.get("callout","DESLIZE PARA CONTINUAR").upper()
    f,lines=wrap(draw,callout,612,1,37,26)
    draw.text((366,1212),lines[0],fill="white",font=f)
    # O PNG canônico é posicionado como layer final, sem reinterpretação.
    box=[18,973,274,284]
    original=lumino.resize((box[2],box[3]),Image.Resampling.LANCZOS)
    image.paste(original,(box[0],box[1]),original)
    draw=ImageDraw.Draw(image)
    for i in range(8):
        draw.ellipse((435+i*34,1291,454+i*34,1310),
                     fill=YELLOW if i==number-1 else (172,163,150))
    draw.ellipse((989,1286,1041,1338),fill=INK)
    draw.text((999,1293),"→",font=font(31),fill="white")
    output.parent.mkdir(parents=True,exist_ok=True)
    image.save(output,format="JPEG",quality=97,subsampling=0,optimize=True)
    return {"number":number,"file":output.name,"headline":item["headline"],
            "layout":layout,"mascot_box":box,"sha256":sha256(output),
            "background_sha256":sha256(p),
            "background_credit":item["credit"],"background_type":item.get("background_type","illustration")}

def render(spec_path:Path,out:Path):
    config=verify_brand()
    content=json.loads(spec_path.read_text(encoding="utf-8"))
    slides=content.get("slides")
    if not isinstance(slides,list) or len(slides)!=8:
        raise VisualError("Carrossel precisa de 8 descricoes de paginas.")
    out=out.resolve();specdir=spec_path.resolve().parent
    if out==specdir:raise VisualError("Imagens finais precisam de pasta propria.")
    mascot=Image.open(ROOT/config["lumino"]["path"]).convert("RGBA")
    pages=[]
    for n,item in enumerate(slides,1):
        pages.append(render_one(item,n,mascot,out/f"{n:02d}.jpg",specdir))
    manifest={"version":1,"standard_id":config["id"],"lumino_sha256":config["lumino"]["sha256"],
              "reference_sha256":config["reference"]["sha256"],
              "post_id":content.get("post_id"),"approved":False,"pages":pages}
    manifest_path=out/"visual-manifest.json"
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return validate_package(manifest_path)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--spec",required=True,type=Path);p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    try: print(json.dumps(render(a.spec,a.out),ensure_ascii=False))
    except (VisualError,OSError,ValueError,KeyError) as e:p.error(str(e))

if __name__=="__main__":main()
