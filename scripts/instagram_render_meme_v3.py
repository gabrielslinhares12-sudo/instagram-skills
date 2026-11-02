#!/usr/bin/env python3
"""Single 4-panel electoral meme with original Lúmino. Review only."""
from __future__ import annotations
import hashlib,json,random
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageEnhance,ImageFilter
from instagram_visual_standard import verify_brand
ROOT=Path(__file__).resolve().parent.parent
SPEC=ROOT/"content/editorial/meme-voto-nulo-v3.json"
OUT=ROOT/"content/staging/meme-voto-nulo-2026-11-02-v3"
W,H=1080,1350
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
YELLOW=(255,214,0);RED=(213,14,21);INK=(18,22,28);PAPER=(250,240,220)

def font(n,bold=True):return ImageFont.truetype(FONT if bold else REG,n)
def hash_file(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def multiline(draw,lines,x,y,fs,color,gap=0):
    f=font(fs)
    for j,line in enumerate(lines):
        draw.text((x,y+j*(fs+gap)),line,font=f,fill=color,stroke_width=0)

def fit_text(draw,text,max_width,initial,smallest=23):
    n=initial
    while n>=smallest and draw.textbbox((0,0),text,font=font(n))[2]>max_width:
        n-=1
    if n<smallest:raise RuntimeError("Headline too wide: "+text)
    return n

def panel_photo(photo,w=526,h=659,variant=0):
    pan=ImageOps.fit(photo,(w,h),Image.Resampling.LANCZOS,
        centering=[(.45,.50),(.53,.55),(.56,.47),(.38,.59)][variant])
    pan=ImageEnhance.Contrast(pan).enhance(1.18)
    pan=ImageEnhance.Color(pan).enhance(.74)
    return pan

def main():
    cfg=verify_brand(ROOT)
    sp=json.loads(SPEC.read_text(encoding="utf-8"))
    if sp["status"]!="draft_review_no_publication":raise ValueError("Review only")
    photo=Image.open(ROOT/sp["media_path"]).convert("RGB")
    lumino=Image.open(ROOT/cfg["lumino"]["path"]).convert("RGBA")
    im=Image.new("RGB",(W,H),INK)
    draw=ImageDraw.Draw(im)
    panels=[(7,7),(548,7),(7,685),(548,685)]
    for i,(x,y) in enumerate(panels):
        p=panel_photo(photo,525,657,i)
        # Monochrome/documentary photo + color tint, each panel uses different composition.
        dark=Image.new("RGBA",p.size,(8,16,31,150 if i in (0,3) else 175))
        p=Image.alpha_composite(p.convert("RGBA"),dark).convert("RGB")
        im.paste(p,(x,y))
    draw=ImageDraw.Draw(im)
    # Panel 1: opening question, a white speech bubble.
    draw.rounded_rectangle((27,30,518,425),radius=52,fill=(255,250,235),outline=INK,width=9)
    draw.polygon([(344,405),(416,405),(451,483)],fill=(255,250,235))
    multiline(draw,["SE EU VOTAR","NULO, A","ELEIÇÃO É","ANULADA?"],58,65,59,INK,10)
    draw.line((78,357,380,357),fill=RED,width=11)
    # Panel 2: the punchline.
    draw.polygon([(565,55),(1060,22),(1038,205),(576,235)],fill=YELLOW)
    draw.text((594,65),"MITO!",font=font(125),fill=RED)
    draw.text((568,525),"NÃO EXISTE BOTÃO",font=font(31),fill=PAPER)
    draw.text((568,565),"'ANULAR ELEIÇÃO'.",font=font(31),fill=YELLOW)
    # Panel 3: easy-to-scan proof. Contrasting cards.
    draw.polygon([(30,713),(527,695),(512,834),(17,846)],fill=YELLOW)
    multiline(draw,["BRANCO","E NULO"],53,719,65,INK,4)
    draw.rounded_rectangle((32,855,507,1067),radius=25,fill=(250,242,228))
    draw.text((56,889),"NÃO SÃO VÁLIDOS.",font=font(42),fill=RED)
    draw.text((55,955),"NÃO VÃO PARA",font=font(39),fill=INK)
    draw.text((55,1005),"NINGUÉM.",font=font(45),fill=INK)
    draw.text((37,1131),"Mesmo se forem muitos.",font=font(31),fill=PAPER)
    # Panel 4: legal distinction, small original mascot.
    draw.rounded_rectangle((567,708,1051,900),radius=25,fill=(250,242,228))
    draw.text((591,732),"VOTO NULO ≠",font=font(56),fill=RED)
    draw.text((589,806),"NULIDADE",font=font(66),fill=INK)
    draw.text((571,1122),"Nulidade da votação",font=font(29),fill=PAPER)
    draw.text((571,1162),"depende de hipótese legal.",font=font(27),fill=YELLOW)
    draw.text((572,1205),"Não de voto em branco/nulo.",font=font(24),fill=PAPER)
    # Exact unmodified canonical mascot only; no redraws or AI substitutes.
    boxes=[[331,389,194,203],[636,238,312,324],[299,1089,190,197],[784,895,220,228]]
    for x,y,w,h in boxes:
        pic=lumino.resize((w,h),Image.Resampling.LANCZOS)
        im.paste(pic,(x,y),pic)
    draw=ImageDraw.Draw(im)
    draw.rectangle((0,1340,W,1350),fill=YELLOW)
    draw.text((30,1301),"@temumaexplicacao  •  FONTE: TSE",font=font(21),fill=PAPER)
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/"meme-voto-nulo.jpg"
    im.save(path,"JPEG",quality=97,subsampling=0,optimize=True)
    with Image.open(path) as chk:
        if chk.size!=(W,H) or chk.format!="JPEG":
            raise RuntimeError("Invalid Instagram JPEG size/format")
        # Verify that the canonical mascot survives JPG encoding at all 4 positions.
        pix=chk.convert("RGB").load()
    source=lumino.resize((220,228),Image.Resampling.LANCZOS)
    match=im.crop((784,895,1004,1123)).convert("RGB")
    diffs=[]
    for yy in range(0,228,5):
        for xx in range(0,220,5):
            if source.getpixel((xx,yy))[3]>245:
                observed=match.getpixel((xx,yy))
                expected=source.getpixel((xx,yy))
                diffs.extend(abs(observed[k]-expected[k]) for k in range(3))
    error=sum(diffs)/max(len(diffs),1)
    if error>5:raise RuntimeError("Canonical Lúmino overlay altered")
    report={"id":sp["id"],"approved":False,"visual_reviewed":False,
            "owner_authorized":False,"published":False,"media_file":path.name,
            "size":[W,H],"sha256":hash_file(path),
            "canonical_lumino_sha256":cfg["lumino"]["sha256"],
            "photo_source":sp["photo_source"],"source":sp["source"],
            "mascot_boxes":boxes,"source_pixel_match_error":round(error,3)}
    (OUT/"qa.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("MEME_QA="+json.dumps({"ok":True,"approved":False,
            "original_lumino":True,"size":[W,H]},ensure_ascii=False))
if __name__=="__main__":main()
