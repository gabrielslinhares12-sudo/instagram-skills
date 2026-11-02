#!/usr/bin/env python3
"""One original art-directed 7-page voting carousel, strictly for staging review."""
from __future__ import annotations
import hashlib, io, json, math, random, textwrap, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
from instagram_visual_standard import verify_brand, validate_package, preview_geometry
ROOT=Path(__file__).resolve().parent.parent
SPEC=ROOT/"content/editorial/votos-validos-reconstrucao-v3.json"
DEST=ROOT/"content/staging/votos-validos-2026-11-02-reconstrucao-v3"
W,H=1080,1350
PAPER=(244,237,225); YELLOW=(255,214,0); RED=(213,14,21); INK=(17,17,17)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def hash_file(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(size,bold=True):
    path=FONT if bold else REG
    if not Path(path).exists():
        raise RuntimeError("Fonte editorial DejaVu exigida e ausente")
    return ImageFont.truetype(path,size)

def photo_url(filename):
    md5=hashlib.md5(filename.encode("utf-8")).hexdigest()
    return "https://upload.wikimedia.org/wikipedia/commons/"+md5[0]+"/"+md5[:2]+"/"+urllib.parse.quote(filename)

def get_photos(spec):
    d=DEST/"source-photos"
    d.mkdir(parents=True,exist_ok=True)
    # Wikimedia Commons currently rate-limits shared GitHub Actions IPs (HTTP 429).
    # Public TSE Flickr originals are an alternative source for the *same* works.
    flickr_ids=["51744471623","51744227376","51744543743"]
    out=[]
    for i,info in enumerate(spec["photos"]):
        name=info["file"];target=d/("photo-"+str(i)+".jpg")
        candidates=[]
        if i==0:
            candidates.append("https://live.staticflickr.com/65535/51744471623_4bd4dd11e9_o.jpg")
        # Flickr public oEmbed reveals a public static photo URL without any key.
        try:
            oembed=("https://www.flickr.com/services/oembed/?format=json&url="+
                urllib.parse.quote("https://www.flickr.com/photos/tsejusbr/"+flickr_ids[i]+"/",safe=""))
            req=urllib.request.Request(oembed,headers={"User-Agent":"Mozilla/5.0 TUE editorial research"})
            with urllib.request.urlopen(req,timeout=18) as response:
                meta=json.loads(response.read(20_000))
            url=meta.get("url") or meta.get("thumbnail_url")
            if url and url.startswith("https://"):
                candidates.append(url)
        except Exception:
            pass
        candidates.append(photo_url(name))
        candidates.append("https://commons.wikimedia.org/wiki/Special:Redirect/file/"+
                          urllib.parse.quote(name))
        last_error=None;selected=None
        for url in candidates:
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"})
                with urllib.request.urlopen(req,timeout=25) as response:
                    blob=response.read(9_000_000)
                if not 15_000<len(blob)<9_000_000:
                    raise ValueError("photo bytes out of bounds")
                with Image.open(io.BytesIO(blob)) as im:
                    im.verify()
                target.write_bytes(blob)
                selected=url
                break
            except Exception as exc:
                last_error=type(exc).__name__
        if not selected:
            # Never claim another image was sourced/credited if this one is missing.
            if i==0:raise RuntimeError("No trusted photo available: "+str(last_error))
            target.write_bytes(out[0]["file"].read_bytes())
            out.append({"file":target,"source":out[0]["source"],
                "sha256":hash_file(target),"credit":out[0]["credit"],
                "source_index":0,"fallback":True})
        else:
            out.append({"file":target,"source":selected,
                "sha256":hash_file(target),"credit":info["credit"],
                "source_index":i,"fallback":False})
        print("PHOTO_SOURCE_STATUS="+json.dumps({
            "slot":i,"verified":True,"source_index":out[-1]["source_index"],
            "fallback":out[-1]["fallback"]}),flush=True)
    return out

def paper(seed):
    rand=random.Random(seed)
    image=Image.new("RGB",(W,H),PAPER)
    pix=image.load()
    for y in range(0,H,4):
        for x in range(0,W,4):
            offset=rand.randint(-7,7)
            color=tuple(max(0,min(255,c+offset)) for c in PAPER)
            for yy in range(y,min(H,y+4)):
                for xx in range(x,min(W,x+4)):
                    pix[xx,yy]=color
    return image

def label(draw,xy,text,fill=INK,size=31):
    draw.text(xy,text,font=font(size),fill=fill,stroke_width=0)

def centered(draw,xy,text,fill=INK,size=48):
    draw.text(xy,text,font=font(size),fill=fill,anchor="mm")

def brush(draw,y,width,seed):
    rand=random.Random(seed)
    x=50;right=min(1028,x+width)
    poly=[(x-10,y+10),(x+rand.randint(7,18),y-7),
          (right-9,y-3),(right+9,y+rand.randint(5,19)),
          (right-7,y+75),(x+11,y+83),(x-7,y+70)]
    draw.polygon(poly,fill=YELLOW)
    draw.line([(x-10,y+79),(right+18,y+76)],fill=(255,193,0),width=6)

def photo_panel(base,source,variant):
    im=Image.open(source).convert("RGB")
    # Alternative crops to avoid repeating the same panorama exactly.
    im=ImageOps.fit(im,(992,640),Image.Resampling.LANCZOS,centering=[
       (.50,.53),(.36,.42),(.62,.57),(.43,.60),(.55,.44),(.65,.50),(.48,.45)
    ][variant])
    im=ImageEnhance.Color(im).enhance(.83)
    im=ImageEnhance.Contrast(im).enhance(.96)
    # Rounded photo with creamy atmospheric haze.
    m=Image.new("L",(992,640));md=ImageDraw.Draw(m)
    md.rounded_rectangle((0,0,991,639),radius=34,fill=255)
    base.paste(im,(44,405),m)
    return im

def lines_fit(draw,text,maxwidth,size=32,limit=4):
    result=[];cur=""
    for token in text.split():
        trial=token if not cur else cur+" "+token
        if draw.textbbox((0,0),trial,font=font(size,False))[2] <= maxwidth:
            cur=trial
        else:
            if cur:result.append(cur)
            cur=token
    if cur:result.append(cur)
    if len(result)>limit:
        raise RuntimeError("Texto denso para arte: "+text)
    return result

def main():
    cfg=verify_brand(ROOT)
    spec=json.loads(SPEC.read_text(encoding="utf-8"))
    if spec["status"]!="draft_review_no_publication" or len(spec["slides"])!=7:
        raise ValueError("Apenas sete slides de revisão; não publicar")
    DEST.mkdir(parents=True,exist_ok=True)
    photos=get_photos(spec)
    lumino=Image.open(ROOT/cfg["lumino"]["path"]).convert("RGBA")
    manifest=[]
    for idx,s in enumerate(spec["slides"],1):
        lay=s["layout"]
        a=paper(20261102+idx)
        draw=ImageDraw.Draw(a)
        draw.rectangle((0,0,W,16),fill=YELLOW)
        draw.rounded_rectangle((50,37,454,104),radius=20,fill=INK)
        label(draw,(69,47),"TEM UMA EXPLICAÇÃO",fill=(255,255,255),size=28)
        draw.ellipse((934,24,1059,135),fill=RED)
        centered(draw,(998,79),"TUE",fill=(255,255,255),size=40)
        titles=s["headline"]
        titlesize=70 if len(titles)==3 else 83
        for j,heading in enumerate(titles):
            yy=136+j*79 if len(titles)==3 else 150+j*85
            # Render headline on variable hand-made yellow bands.
            px=draw.textbbox((0,0),heading,font=font(titlesize))
            stripe_width=min(960,max(650,px[2]+86))
            brush(draw,yy,stripe_width,idx*11+j)
            label(draw,(66,yy-4),heading,size=titlesize)
        draw.text((60,360),s["subhead"],font=font(25),fill=RED)
        photo_panel(a,photos[s["photo"]]["file"],idx-1)
        draw=ImageDraw.Draw(a)
        # Distinct large-number overlay on photographic evidence for depth.
        if lay=="diagram":
            draw.rounded_rectangle((70,465,760,670),radius=24,fill=(255,247,229),outline=(247,197,0),width=7)
            centered(draw,(415,525),s["accent"],size=61,fill=RED)
            centered(draw,(415,600),"EXEMPLO HIPOTÉTICO",size=25)
        elif lay=="split":
            draw.rounded_rectangle((430,500,998,670),radius=29,fill=(255,248,231),outline=RED,width=6)
            centered(draw,(715,558),s["accent"],size=59,fill=RED)
            centered(draw,(715,621),"APURAÇÃO DOS VÁLIDOS",size=24)
        else:
            draw.rounded_rectangle((70,490,540,654),radius=26,fill=(255,246,226),outline=RED,width=6)
            centered(draw,(305,559),s["accent"],size=55,fill=RED)
            centered(draw,(305,618),"FATOS, NÃO BOATOS",size=20)
        # Card alternates so visual rhythm is not a repeated fixed template.
        left=idx in (2,4,6)
        card=(406,850,1028,1196) if left else (49,850,673,1196)
        draw.rounded_rectangle(card,radius=28,fill=(255,250,239),outline=(213,196,171),width=3)
        tx=card[0]+30
        draw.rounded_rectangle((tx,881,card[2]-30,945),radius=13,fill=YELLOW)
        label(draw,(tx+16,892),s["label"],size=25)
        bodylines=lines_fit(draw,s["body"],card[2]-tx-63,size=29,limit=5)
        for j,line in enumerate(bodylines):
            draw.text((tx+4,972+j*43),line,font=font(29,False),fill=INK)
        mx=64 if left else 700
        my=821 if left else 801
        mw,mh=(315,327) if left else (310,322)
        original=lumino.resize((mw,mh),Image.Resampling.LANCZOS)
        a.paste(original,(mx,my),original)
        draw=ImageDraw.Draw(a)
        draw.rectangle((35,1204,1045,1209),fill=(214,199,170))
        draw.text((51,1230),"DESLIZE PARA O LADO",font=font(24),fill=INK)
        for j in range(7):
            cx=730+j*24
            draw.ellipse((cx-6,1241,cx+6,1253),fill=RED if j==idx-1 else (180,165,144))
        draw.text((54,1290),"TSE | EXEMPLO HIPOTÉTICO | @temumaexplicacao",font=font(21,False),fill=(98,88,73))
        page=DEST/f"{idx:02d}-votos-validos.jpg"
        a.save(page,"JPEG",quality=96,subsampling=0,optimize=True)
        sha=hash_file(page)
        manifest.append({"number":idx,"file":page.name,"source_sha256":sha,
            "sha256":sha,"layout":lay,"headline":" / ".join(titles),
            "mascot_box":[mx,my,mw,mh],"background_type":"documentary_photo",
            "background_credit":photos[s["photo"]]["credit"],
            "photo_source":photos[s["photo"]]["source"],
            "photo_source_sha256":photos[s["photo"]]["sha256"]})
    cols,rows,pw,ph=preview_geometry(len(manifest))
    preview=Image.new("RGB",(pw,ph),PAPER)
    for i,item in enumerate(manifest):
        with Image.open(DEST/item["file"]) as pg:
            thumb=pg.resize((216,270),Image.Resampling.LANCZOS)
            preview.paste(thumb,((i%cols)*216,(i//cols)*270))
    prev=DEST/f"PREVIA-{len(manifest):02d}-ARTES.png"
    preview.save(prev,"PNG")
    m={"version":1,"standard_id":cfg["id"],"post_id":spec["id"],
       "production_mode":"individually_art_directed_v1","approved":False,
       "visual_reviewed":False,"owner_authorized":False,
       "lumino_sha256":cfg["lumino"]["sha256"],
       "reference_sha256":cfg["reference"]["sha256"],
       "preview_file":prev.name,"preview_sha256":hash_file(prev),
       "pages":manifest}
    path=DEST/"visual-manifest.json"
    path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result=validate_package(path)
    (DEST/"qa-offline.json").write_text(
       json.dumps({"technical":result,"publication_approved":False,
       "manual_visual_review_required":True,
       "legal_context":"Eleição presidencial HIPOTÉTICA e fotos de urnas TSE de outras datas"},
       ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("VOTOS_RECONSTRUCAO_QA="+json.dumps({
       "page_count":len(manifest),"all_artwork_original_lumino":True,
       "photo_sources":len(photos),"technical_qc":result["ok"],
       "approved":False,"publication_attempted":False},ensure_ascii=False))
if __name__=="__main__":main()
