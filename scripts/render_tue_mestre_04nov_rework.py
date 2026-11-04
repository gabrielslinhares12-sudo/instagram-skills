#!/usr/bin/env python3
"""Rebuild 04NOV rejected slides using the approved TUE-MESTRE-01 grammar.

Creates distinct editorial compositions from verified source photography, genuine
paper texture, irregular paint strokes, canon Lúmino PNG, black condensed text,
red accents and discreet pale-footed swipe cues. This does NOT approve or publish.
"""
from __future__ import annotations
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib, io, json, random, math, os
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"content/media/instagram/2026-11-04/REWORK-TUE-MESTRE-01"
OUT.mkdir(parents=True,exist_ok=True)
LUMINO=ROOT/"content/brand/lumino-original.png"
EXPECTED="f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b"
assert hashlib.sha256(LUMINO.read_bytes()).hexdigest()==EXPECTED,"Canonical mascot has changed"
S=3
W,H=1080*S,1350*S
PAPER=(244,237,225); INK=(17,17,17); YELLOW=(255,214,0); RED=(213,14,21); GRAY=(172,171,168)
MASCOT=Image.open(LUMINO).convert("RGBA")

def get_font(name,size):
    names={
        "display":["/tmp/anton.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"],
        "body":["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
        "bold":["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    }
    for p in names[name]:
        if Path(p).is_file(): return ImageFont.truetype(p,size*S)
    raise RuntimeError("No usable font")

def load_photo(url):
    request=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; TUEStudio/1.0; editorial research)"})
    with urlopen(request,timeout=80) as fh: data=fh.read(25000000)
    if len(data)<5000: raise RuntimeError("Empty media: "+url)
    pic=Image.open(io.BytesIO(data)); pic.load()
    return pic.convert("RGB")

def base(seed):
    # Grain in true RGB pixels (vectorized), not a plain-colored card.
    rng=np.random.default_rng(seed)
    grain=rng.integers(-8,9,size=(H,W),dtype=np.int16)
    edge=np.zeros((H,W),dtype=np.int16)
    edge[:35*S,:]=-3; edge[:,:45*S]-=3;edge[:,W-40*S:]-=3
    rgb=np.stack([np.clip(c+grain+edge,0,255).astype(np.uint8) for c in PAPER],axis=2)
    return Image.fromarray(rgb,"RGB")

def rect(d,xy,color,width=0):
    d.rectangle(tuple(int(t*S) for t in xy),fill=color if width==0 else None,outline=color if width else None,width=width*S)

def draw_text(d,pos,txt,size=40,ink=INK,font="display",maxw=None,anchor="la",spacing=0):
    ft=get_font(font,size)
    if maxw:
        while d.textbbox((0,0),txt,font=ft)[2]>maxw*S and size>16:
            size-=1;ft=get_font(font,size)
    d.text((int(pos[0]*S),int(pos[1]*S)),txt,font=ft,fill=ink,anchor=anchor,spacing=spacing)
    return ft

def brush(im,box,seed,color=YELLOW):
    rng=random.Random(seed)
    x0,y0,x1,y1=box
    poly=[]
    for j in range(25):
        x=x0+(x1-x0)*j/24
        poly.append((int(x*S),int((y0+rng.uniform(-6,7))*S)))
    for j in range(24,-1,-1):
        x=x0+(x1-x0)*j/24
        poly.append((int(x*S),int((y1+rng.uniform(-8,8))*S)))
    layer=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    d.polygon(poly,fill=(*color,240))
    for k in range(55):
        x=rng.randint(int(x0*S),int(x1*S))
        y=int(rng.choice([y0,y1])*S+rng.randint(-15*S,15*S))
        d.line([(x,y),(x+rng.randrange(-38*S,38*S),y+rng.randrange(-2*S,2*S))],fill=(*color,rng.randrange(90,200)),width=rng.randrange(1*S,5*S))
    im.paste(layer,(0,0),layer)

def fitted_photo(pic,w,h,mode="cover"):
    cw,ch=int(w*S),int(h*S)
    iw,ih=pic.size
    fac=max(cw/iw,ch/ih) if mode=="cover" else min(cw/iw,ch/ih)
    pic=pic.resize((round(iw*fac),round(ih*fac)),Image.Resampling.LANCZOS)
    left=(pic.width-cw)//2; top=(pic.height-ch)//2
    return pic.crop((left,top,left+cw,top+ch))

def photo(im,pic,xy,seed=1,sepia=False,angle=0):
    x,y,w,h=xy
    # Each source image becomes a materially different archival matte, NOT a
    # reused darkened full-canvas texture or decorative card.
    pic=fitted_photo(pic,w,h)
    if sepia:
        g=ImageEnhance.Contrast(pic.convert("L")).enhance(1.1)
        pic=Image.merge("RGB",tuple(g.point(lambda p,scale=s: int(p*scale)) for s in (1,.94,.81)))
    frame=Image.new("RGBA",(int((w+20)*S),int((h+20)*S)),(254,250,244,255))
    frame.paste(pic,(10*S,10*S))
    if angle:
        frame=frame.rotate(angle,expand=True,resample=Image.Resampling.BICUBIC,fillcolor=(0,0,0,0))
    shadow=Image.new("RGBA",frame.size,(0,0,0,0))
    shadow.paste((0,0,0,85),(0,0,*frame.size))
    shadow=shadow.filter(ImageFilter.GaussianBlur(12*S))
    px=int(x*S);py=int(y*S)
    im.paste(shadow,(px+10*S,py+12*S),shadow)
    im.paste(frame,(px,py),frame)

def mascot(im,x=708,y=825,w=330):
    # Canonical PNG, never generated or cropped into a different character.
    h=round(w*MASCOT.height/MASCOT.width)
    copy=MASCOT.resize((w*S,h*S),Image.Resampling.LANCZOS)
    im.paste(copy,(x*S,y*S),copy)

def stroke(d,x0,y0,x1,y1,width=5):
    d.line([(x0*S,y0*S),(x1*S,y1*S)],fill=RED,width=width*S)

def header(im,series,tag):
    d=ImageDraw.Draw(im)
    draw_text(d,(54,38),"TEM UMA EXPLICAÇÃO",25,INK,"bold")
    d.line([(54*S,83*S),(1027*S,83*S)],fill=INK,width=2*S)
    draw_text(d,(55,96),series.upper(),24,RED,"bold",maxw=690)
    draw_text(d,(1025,96),tag.upper(),22,INK,"bold",maxw=380,anchor="ra")

def footer(im,i,n,credit):
    d=ImageDraw.Draw(im)
    d.rectangle((0,1244*S,W,H),fill=PAPER)
    d.line((54*S,1241*S,1025*S,1241*S),fill=(206,201,191),width=2*S)
    # Tiny dynamic dots; no page numbers, yellow badges or boxes.
    # Exact five-dot progress marker: slide i highlights dot (i+1).
    # Last slide retains its fifth active dot but never shows a swipe arrow.
    for j in range(n):
        x=488+24*(j-(n-1)/2)
        d.ellipse(((x-4)*S,1260*S,(x+4)*S,1268*S),
                  fill=YELLOW if j==i else (191,193,195))
    if i<n-1:
        draw_text(d,(540,1277),"A R R A S T E   P A R A   O   L A D O",13,INK,"body",anchor="ma")
        d.line((797*S,1280*S,829*S,1280*S),fill=INK,width=2*S)
        d.line((829*S,1280*S,823*S,1275*S),fill=INK,width=2*S)
        d.line((829*S,1280*S,823*S,1285*S),fill=INK,width=2*S)
    draw_text(d,(540,1321),credit.upper(),12,(107,102,96),"body",maxw=960,anchor="ms")

def save(im,name):
    # High-resolution working canvas renders all the typography and textures
    # before the official Instagram final JPEG is downsampled.
    final=im.resize((1080,1350),Image.Resampling.LANCZOS)
    path=OUT/name
    final.save(path,"JPEG",quality=95,subsampling=0,optimize=True)
    return {"file":name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size,"dimensions":[1080,1350]}

BOSTON=[
  {"title":["UMA CIDADE","SOTERRADA"],"emph":"POR MELAÇO.","fact":"BOSTON, 15 DE JANEIRO DE 1919","tag":"ARQUIVO REAL", "src":"https://commons.wikimedia.org/wiki/Special:Redirect/file/BostonMolassesDisaster.jpg","kind":"cover"},
  {"title":["UM TANQUE","SE ROMPEU"],"emph":"15 METROS.","fact":"A ESTRUTURA NÃO RESISTIU.","tag":"A ORIGEM", "src":"https://commons.wikimedia.org/wiki/Special:Redirect/file/North%20End%20molasses%20tank.jpg","kind":"evidence"},
  {"title":["8,7 MILHÕES","DE LITROS"],"emph":"INVADIRAM AS RUAS.","fact":"CASAS E TRILHOS FORAM ATINGIDOS.","tag":"O VOLUME", "src":"https://commons.wikimedia.org/wiki/Special:Redirect/file/Boston%20post-January%2016%2C%201919%2C.jpg","kind":"number"},
  {"title":["21 PESSOAS","MORRERAM"],"emph":"150 FERIDOS.","fact":"UMA TRAGÉDIA, NÃO UMA LENDA.","tag":"AS VÍTIMAS", "src":"https://commons.wikimedia.org/wiki/Special:Redirect/file/TheBostonDailyGlobe-frontpage-1919-1-16.jpg","kind":"news"},
  {"title":["O DESASTRE","DEIXOU MARCAS"],"emph":"SEGURANÇA IMPORTA.","fact":"A INVESTIGAÇÃO MUDOU O DEBATE INDUSTRIAL.","tag":"O LEGADO", "src":"https://commons.wikimedia.org/wiki/Special:Redirect/file/Molasses%20Flood%20Historical%20Marker.jpg","kind":"end"}
]
M87=[
  {"title":["FOTOGRAFARAM","O INVISÍVEL?"],"emph":"SIM. EM 2019.","fact":"A PRIMEIRA SOMBRA DE UM BURACO NEGRO.","tag":"REGISTRO REAL", "src":"https://nsf-gov-resources.nsf.gov/2024-12/Event%20Horizon%20Black%20Hole%20Image.jpg","kind":"cover"},
  {"title":["TELESCÓPIOS","DO PLANETA"],"emph":"TRABALHARAM JUNTOS.","fact":"ANTENAS DE RÁDIO FORMARAM UMA REDE.","tag":"O MÉTODO", "src":"https://cdn.eso.org/images/large/alma-drone-1.jpg","kind":"evidence"},
  {"title":["55 MILHÕES","DE ANOS-LUZ"],"emph":"É A DISTÂNCIA.","fact":"M87* TEM CERCA DE 6,5 BILHÕES DE MASSAS SOLARES.","tag":"A GALÁXIA", "src":"https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2024/09/hubble_s_view_of_m87_galaxy/26324816-3-eng-GB/Hubble_s_view_of_M87_galaxy.jpg","kind":"number"},
  {"title":["O ANEL BRILHA"],"emph":"O CENTRO É SOMBRA.","fact":"A IMAGEM VEIO DE DADOS DE RÁDIO.","tag":"A EXPLICAÇÃO", "src":"https://nsf-gov-resources.nsf.gov/2024-12/Event%20Horizon%20Black%20Hole%20Image.jpg","kind":"end"}
]

def paint_page(subject,data,idx,total,source):
    im=base(507+idx+10*(subject=="M87"))
    header(im,"ARQUIVO IMPROVÁVEL" if subject=="BOSTON" else "RAIO-X DA REALIDADE",data["tag"])
    kind=data["kind"]
    rng_seed=120+idx+(20 if subject=="M87" else 0)
    d=ImageDraw.Draw(im)
    if kind=="cover":
        brush(im,(55,190,940,355),rng_seed)
        draw_text(d,(78,184),data["title"][0],78,maxw=880)
        draw_text(d,(80,269),data["title"][1],78,maxw=860)
        stroke(d,80,374,590,368,6)
        photo(im,source,(72,469,805,620),seed=rng_seed,sepia=subject=="BOSTON",angle=2)
        mascot(im,625,735,430)
        brush(im,(64,1112,785,1186),rng_seed+10)
        draw_text(ImageDraw.Draw(im),(91,1114),data["emph"],55,INK,maxw=640)
        draw_text(ImageDraw.Draw(im),(72,414),data["fact"],21,INK,"bold",maxw=880)
    elif kind=="evidence":
        photo(im,source,(72,170,545,760),seed=rng_seed,sepia=subject=="BOSTON",angle=-2)
        brush(im,(440,236,1020,333),rng_seed)
        d=ImageDraw.Draw(im)
        draw_text(d,(469,236),data["title"][0],56,INK,maxw=526)
        draw_text(d,(465,345),data["title"][1],62,INK,maxw=525)
        stroke(d,466,449,1000,449,5)
        draw_text(d,(464,477),data["emph"],42,RED,maxw=545)
        draw_text(d,(76,1046),data["fact"],32,INK,"bold",maxw=940)
        mascot(im,640,700,400)
    elif kind=="number":
        brush(im,(52,184,1040,399),rng_seed)
        draw_text(d,(79,185),data["title"][0],100,INK,maxw=930)
        draw_text(d,(80,285),data["title"][1],85,INK,maxw=870)
        photo(im,source,(58,503,955,624),seed=rng_seed,sepia=subject=="BOSTON",angle=-1)
        mascot(im,660,780,375)
        draw_text(ImageDraw.Draw(im),(70,443),data["emph"],47,RED,maxw=960)
        draw_text(ImageDraw.Draw(im),(68,1164),data["fact"],26,INK,"bold",maxw=930)
    elif kind=="news":
        photo(im,source,(50,155,526,985),seed=rng_seed,sepia=True,angle=2)
        brush(im,(440,211,1023,327),rng_seed)
        draw_text(d,(472,207),data["title"][0],54,INK,maxw=526)
        draw_text(d,(471,319),data["title"][1],57,INK,maxw=520)
        draw_text(d,(467,470),data["emph"],51,RED,maxw=520)
        d.line((465*S,537*S,1000*S,537*S),fill=RED,width=5*S)
        draw_text(d,(480,585),data["fact"],25,INK,"bold",maxw=540)
        mascot(im,650,794,405)
    else:
        photo(im,source,(82,173,895,645),seed=rng_seed,sepia=subject=="BOSTON",angle=1)
        brush(im,(57,871,1000,1023),rng_seed)
        draw_text(d,(77,870),data["title"][0],67,INK,maxw=902)
        draw_text(d,(80,945),data["title"][1] if len(data["title"])>1 else data["title"][0],59,INK,maxw=900)
        stroke(d,70,1055,520,1055,6)
        draw_text(d,(76,1081),data["emph"],44,RED,maxw=820)
        mascot(im,655,728,402)
        draw_text(d,(74,1181),data["fact"],22,INK,"bold",maxw=900)
    footer(im,idx,total,"FONTES: BOSTON CITY ARCHIVES / WIKIMEDIA" if subject=="BOSTON" else "FONTES: EHT / NSF / ESO / ESA")
    return im

def main():
    # The originals remain rejected; output goes ONLY to the distinct REWORK
    # directory and has no queue schedule side effects.
    for family,pages in [("BOSTON",BOSTON)]:
        qc={"preset_id":"TUE-MESTRE-01","visual_reference_sha256":"571f7f31012e8265c784c66f68c1f5847906f02a1e533559c2ea5624551833e9","lumino_sha256":EXPECTED,"subject":family,"manual_visual_reviewed":False,"approved":False,"publication_blocked":True,"pages":[]}
        for i,data in enumerate(pages):
            try:
                pic=load_photo(data["src"])
            except Exception:
                if i!=len(pages)-1: raise
                # No invented fake archive photo if historical marker unavailable.
                data=dict(data,src=BOSTON[0]["src"])
                pic=load_photo(data["src"])
            im=paint_page(family,data,i,len(pages),pic)
            name=f"{family}-MESTRE01-{i+1:02d}.jpg"
            receipt=save(im,name)
            receipt.update({"source":data["src"],"layout":data["kind"],"swipe_cue":i<len(pages)-1})
            qc["pages"].append(receipt)
            print(f"REWORK_PAGE={family}:{name}:{receipt['sha256']}",flush=True)
        (OUT/f"{family}-REWORK-QC.json").write_text(json.dumps(qc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("REWORK_COMPLETE=5_BOSTON_JPEGS__ORIGINAL_LUMINO__FIVE_DOTS__NOT_PUBLISHED",flush=True)

if __name__=="__main__":
    main()
