#!/usr/bin/env python3
"""Arte editorial de fisica aplicada, TUE-MESTRE-01, 10/11/2026.
Gera JPEGs REAIS de 1080x1350 usando exclusivamente o Lúmino original.
Nunca publica: salvos em staging para revisao visual/autorizações.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import hashlib, json, math, random

ROOT=Path(__file__).resolve().parent.parent
STAGE=ROOT/"content/staging/2026-11-10"
BRIEF=STAGE/"fisica-aplicada-brief.json"
MASCOT=ROOT/"content/brand/lumino-original.png"
W,H=1080,1350
PAPER=(244,237,225); INK=(17,17,17); YELLOW=(255,214,0)
RED=(213,14,21); CYAN=(0,207,246); MUTED=(89,80,71)
def ft(size,bold=True,condensed=True):
    names=(["/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSansNarrow-Bold.ttf"] if condensed
           else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"])
    for p in names:
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default()
def fit(draw,s,maxwidth,starting=88,minimum=36):
    for size in range(starting,minimum-1,-1):
        font=ft(size)
        if draw.textbbox((0,0),s,font=font,stroke_width=0)[2]<=maxwidth:return font
    return ft(minimum)
def text(draw,x,y,s,size=35,color=INK,bold=False,anchor=None,maxwidth=None):
    font=fit(draw,s,maxwidth,size) if maxwidth else ft(size,bold,not bold)
    draw.text((x,y),s,font=font,fill=color,anchor=anchor,stroke_width=0)
def texture(im,seed,flavor):
    rnd=random.Random(seed)
    d=ImageDraw.Draw(im,"RGBA")
    for j in range(950):
        x=rnd.randrange(W);y=rnd.randrange(H);r=rnd.choice([1,1,1,2])
        d.ellipse((x-r,y-r,x+r,y+r),fill=(50,39,30,rnd.randrange(4,15)))
    for i in range(14):
        y=600+i*47+flavor*8
        d.arc((-90,y,1160,y+230),start=195,end=345,fill=(40,45,40,10),width=2)
    for q in range(5):
        xx=rnd.randrange(50,1040); yy=rnd.randrange(650,1140)
        d.line((xx,yy,xx+90,yy-14),fill=(213,14,21,18),width=4)
def rough_band(draw,top,height,width=930,seed=1):
    r=random.Random(seed)
    left=42; pts=[(left,top+10)]
    for i in range(19):
        pts.append((left+i*width/18,top+r.randint(-8,6)))
    pts.append((left+width,top+height-5))
    for i in range(18,-1,-1):
        pts.append((left+i*width/18,top+height+r.randint(-4,14)))
    draw.polygon(pts,fill=YELLOW)
    for k in range(5):
        y=top+height+r.randint(-8,10)
        draw.line((60+r.randint(-10,20),y,830+r.randint(-30,120),y-12),fill=(255,184,0),width=r.randint(2,5))
def arrow(d,a,b,color=RED,width=12):
    d.line((*a,*b),fill=color,width=width,joint="curve")
    ang=math.atan2(b[1]-a[1],b[0]-a[0])
    r=29
    p=[b,(int(b[0]-r*math.cos(ang-.52)),int(b[1]-r*math.sin(ang-.52))),
         (int(b[0]-r*math.cos(ang+.52)),int(b[1]-r*math.sin(ang+.52)))]
    d.polygon(p,fill=color)
def wheel(im,cx,cy,rad=205,rotate=0):
    layer=Image.new("RGBA",im.size,(0,0,0,0));d=ImageDraw.Draw(layer)
    d.ellipse((cx-rad+10,cy-rad+20,cx+rad+14,cy+rad+22),fill=(0,0,0,75))
    d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=(15,18,21),outline=(50,46,40),width=6)
    for delta,col in [(17,(45,45,44)),(36,(6,7,8)),(55,(110,108,102)),(71,(222,214,194))]:
        r=rad-delta
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=col)
    r=rad-93;d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(51,52,54),outline=YELLOW,width=8)
    for k in range(7):
        a=2*math.pi*k/7+rotate
        x=cx+r*.79*math.cos(a);y=cy+r*.79*math.sin(a)
        d.line((cx,cy,x,y),fill=(192,187,179),width=22)
    d.ellipse((cx-40,cy-40,cx+40,cy+40),fill=(254,216,60),outline=(14,14,14),width=7)
    im.alpha_composite(layer)
def mascot(im,x=580,y=720,w=475):
    with Image.open(MASCOT) as src: src=src.convert("RGBA")
    h=round(w*src.height/src.width)
    src=src.resize((w,h),Image.Resampling.LANCZOS)
    sh=Image.new("RGBA",im.size,(0,0,0,0)); sh.paste(src,(x+9,y+21),src.getchannel("A"))
    sh.putalpha(sh.getchannel("A").filter(ImageFilter.GaussianBlur(21)))
    black=Image.new("RGBA",im.size,(4,3,0,80));black.putalpha(sh.getchannel("A").point(lambda a: round(a*.43)))
    im.alpha_composite(black)
    im.alpha_composite(src,(x,y))
def car_body(d, x=120,y=900, scale=1):
    # Vista lateral esquematica, sem fingir que e fotografia.
    s=scale
    pts=[(x,y+130*s),(x+115*s,y+90*s),(x+210*s,y+12*s),(x+530*s,y+12*s),
         (x+625*s,y+94*s),(x+720*s,y+132*s),(x+720*s,y+240*s),(x+12*s,y+240*s)]
    d.polygon(pts,fill=(62,68,71),outline=INK)
    d.polygon([(x+240*s,y+28*s),(x+500*s,y+28*s),(x+568*s,y+94*s),(x+160*s,y+94*s)],fill=(198,213,213))
    d.line((x+75*s,y+150*s,x+655*s,y+150*s),fill=YELLOW,width=max(4,int(12*s)))
    for xx in [x+172*s,x+565*s]:
        r=65*s
        d.ellipse((xx-r,y+210*s-r,xx+r,y+210*s+r),fill=INK)
        d.ellipse((xx-r*.6,y+210*s-r*.6,xx+r*.6,y+210*s+r*.6),fill=(193,186,175))
def road(d,y=1115):
    d.polygon([(0,y),(W,y-40),(W,H),(0,H)],fill=(120,115,106))
    d.line((0,y+95,W,y+50),fill=(237,226,194),width=15)
def sign(d,x,y,label,col=RED):
    d.rounded_rectangle((x,y,x+290,y+52),radius=8,fill=col)
    text(d,x+15,y+10,label,26,(255,255,255),True)
def draw_pressure(d):
    x0=110; y0=1070
    d.line((x0,y0,x0+800,y0),fill=INK,width=5)
    d.line((x0,y0,x0,y0-310),fill=INK,width=5)
    pts=[(x0+10,1020),(250,925),(330,1010),(415,880),(490,990),(565,855),(635,950),(710,842),(810,870),(895,833)]
    d.line(pts,fill=RED,width=14,joint="curve")
    for xx,yy in pts[1::2]:d.ellipse((xx-9,yy-9,xx+9,yy+9),fill=YELLOW,outline=INK,width=3)
    text(d,124,725,"PRESSÃO DO FREIO",30,INK,True)
    text(d,680,1090,"TEMPO →",28,INK,True)
    for xx,l in [(250,"ALIVIA"),(455,"REAPLICA"),(700,"ALIVIA")]:
        text(d,xx,1132,l,25,RED,True)
def passenger(d,x,y,scale=1,airbag=False):
    # silhueta tecnica para representar ocupante sentado, com cinto realcado
    s=scale
    pt=lambda a,b:(round(x+a*s),round(y+b*s))
    d.rounded_rectangle((*pt(40,270),*pt(405,320)),radius=18,fill=(70,68,64))
    d.rounded_rectangle((*pt(36,60),*pt(87,300)),radius=16,fill=(106,103,94))
    d.ellipse((*pt(165,35),*pt(280,150)),fill=(196,174,150),outline=INK,width=4)
    d.polygon([pt(178,157),pt(280,158),pt(345,294),pt(132,294)],fill=(140,157,159),outline=INK)
    d.line((*pt(278,166),*pt(150,292)),fill=YELLOW,width=max(12,int(22*s)))
    d.line((*pt(147,289),*pt(341,290)),fill=YELLOW,width=max(10,int(18*s)))
    d.rounded_rectangle((*pt(132,279),*pt(178,312)),radius=5,fill=RED,outline=INK,width=3)
    if airbag:
        d.ellipse((*pt(345,75),*pt(590,240)),fill=(236,232,216),outline=CYAN,width=8)
        d.ellipse((*pt(360,90),*pt(565,220)),outline=(140,147,141),width=4)
def draw_scene(im,key):
    d=ImageDraw.Draw(im)
    if key=="hero-abs":
        road(d,1120);wheel(im,310,960,220,.25)
        arrow(d,(120,732),(397,796),RED,13)
        mascot(im,610,680,445)
        sign(d,85,1173,"CONTROLE NA FRENAGEM")
    elif key=="wheel-compare":
        wheel(im,290,922,175);wheel(im,780,922,175,0.2)
        d.line((95,1130,480,1130),fill=RED,width=10)
        d.line((595,1130,975,1130),fill=YELLOW,width=10)
        text(d,122,1180,"DESLIZANDO",37,RED,True)
        text(d,630,1180,"ROLANDO",37,INK,True)
        arrow(d,(150,743),(405,805),RED,10)
        arrow(d,(635,760),(865,719),YELLOW,10)
    elif key=="sensor":
        wheel(im,310,944,225)
        d.ellipse((470,850,520,900),fill=CYAN,outline=INK,width=8)
        d.line((510,872,680,745),fill=RED,width=9)
        d.rounded_rectangle((675,686,980,880),radius=28,fill=INK)
        text(d,704,715,"CENTRAL",56,YELLOW,True)
        text(d,715,785,"DO ABS",60,(250,247,231),True)
        for i in range(7):
            d.arc((490+i*27,756+i*9,785+i*27,955+i*9),35,85,fill=CYAN,width=4)
        text(d,686,974,"ROTAÇÃO",41,INK,True)
        text(d,686,1022,"MONITORADA",41,RED,True)
    elif key=="pressure":
        draw_pressure(d)
        text(d,142,654,"CICLO DE AJUSTE",37,INK,True)
    elif key=="friction":
        road(d,1104); wheel(im,357,880,223)
        for x in [182,272,372,465]:
            arrow(d,(x,1142),(x+45,1108),YELLOW,10)
        d.line((520,916,940,781),fill=RED,width=12)
        d.polygon([(940,781),(888,774),(913,817)],fill=RED)
        text(d,540,831,"FORÇA",41,RED,True)
        text(d,540,873,"LATERAL",41,RED,True)
        sign(d,584,1037,"PNEU + PISTA")
    elif key=="takeaway":
        road(d,1116);car_body(d,70,856,1.02)
        mascot(im,755,835,255)
        arrow(d,(220,771),(715,754),RED,10)
        sign(d,95,1163,"NÃO ANULA A FÍSICA")
    elif key=="hero-belt":
        passenger(d,125,730,1.15)
        mascot(im,610,820,425)
        arrow(d,(480,840),(648,860),RED,10)
        sign(d,91,1170,"O SEGREDO É O TEMPO")
    elif key=="inertia":
        car_body(d,55,780,1.28)
        for i in range(4):
            arrow(d,(150,1170+i*20),(420,1170+i*20),RED,7)
        arrow(d,(508,745),(902,745),RED,17)
        text(d,605,790,"O CORPO",45,INK,True)
        text(d,605,839,"CONTINUA",45,RED,True)
    elif key=="belt":
        passenger(d,100,690,1.33)
        d.ellipse((695,800,790,895),fill=YELLOW,outline=INK,width=5)
        d.line((685,845,525,925),fill=RED,width=8)
        text(d,675,909,"TÓRAX",44,INK,True)
        d.ellipse((700,1022,795,1117),fill=YELLOW,outline=INK,width=5)
        d.line((695,1069,537,1081),fill=RED,width=8)
        text(d,676,1135,"PELVE",44,INK,True)
    elif key=="impulse":
        d.rounded_rectangle((104,762,967,1030),radius=28,fill=(26,27,26))
        text(d,146,798,"IMPULSO",46,YELLOW,True)
        text(d,142,864,"Δp = Fmédia × Δt",57,(248,243,232),True)
        d.line((140,959,922,959),fill=(255,255,255),width=3)
        text(d,157,980,"MESMA VARIAÇÃO DE MOVIMENTO",27,(235,231,219),True)
        arrow(d,(135,1113),(850,1113),RED,15)
        text(d,180,1153,"TEMPO DE DESACELERAÇÃO",32,INK,True)
    elif key=="airbag":
        passenger(d,125,695,1.21,True)
        for q in range(3):
            d.arc((560+q*23,720+q*20,1000+q*10,1120+q*18),205,280,fill=RED,width=5)
        text(d,676,1090,"CINTO + AIRBAG",41,INK,True)
    elif key=="takeaway-belt":
        passenger(d,85,703,1.10,True)
        mascot(im,685,800,325)
        d.line((100,1190,970,1190),fill=YELLOW,width=22)
        text(d,158,1160,"REDUÇÃO DE RISCO",41,RED,True)
    else: raise ValueError(key)
def page(post,index,slide):
    im=Image.new("RGBA",(W,H),(*PAPER,255));seed=sum(map(ord,post["id"]))+index
    texture(im,seed,index)
    d=ImageDraw.Draw(im)
    d.line((54,58,1012,58),fill=INK,width=4)
    text(d,64,79,"TEM UMA EXPLICAÇÃO",29,INK,True)
    text(d,732,80,slide["eyebrow"],24,RED,True,maxwidth=282)
    # titulo e marca-texto, sem caixa de cartão genérica
    lines=slide["headline"].split("\n")
    title_y=188
    rough_band(d,title_y-13,91,975,seed)
    for line in lines:
        font=fit(d,line,968,100,56)
        d.text((62,title_y),line,font=font,fill=INK)
        title_y+=111
    d.line((62,title_y+7,570,title_y+7),fill=RED,width=12)
    # subtitulo ajustado a duas ou tres linhas para leitura em celular
    description=slide["description"]
    words=description.split()
    rows=[]; cur=""
    for w in words:
        attempt=(cur+" "+w).strip()
        if d.textbbox((0,0),attempt,font=ft(40,False,False))[2]>925 and cur:
            rows.append(cur);cur=w
        else:cur=attempt
    if cur:rows.append(cur)
    yy=title_y+37
    for s in rows[:3]:
        d.text((64,yy),s,font=ft(39,False,False),fill=INK)
        yy+=51
    draw_scene(im,slide["visual"])
    d=ImageDraw.Draw(im)
    # Progressos dinamicos, sem numeracao e sem CTA falso na ultima
    n=len(post["slides"])
    if index<n-1:
        center=495
        for j in range(n):
            x=center+(j-(n-1)/2)*30
            d.ellipse((int(x-7),1263,int(x+7),1277),fill=YELLOW if j==index else (169,166,158))
        arrow(d,(633,1270),(684,1270),INK,3)
        text(d,402,1290,"A R R A S T E  P A R A  O  L A D O  →",22,INK,True)
    else:
        text(d,306,1290,"T E M   U M A   E X P L I C A Ç Ã O",25,INK,True)
    d.line((54,1333,1025,1333),fill=(186,178,164),width=2)
    out=STAGE/("abs" if "abs-" in post["id"] else "cinto")/f"{index+1:02d}.jpg"
    out.parent.mkdir(parents=True,exist_ok=True)
    im.convert("RGB").save(out,"JPEG",quality=93,subsampling=0,optimize=True)
    return out
def main():
    assert MASCOT.exists(),"Mascote canonico ausente, nao improvise."
    assert hashlib.sha256(MASCOT.read_bytes()).hexdigest()=="f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b","Lúmino nao e o original aprovado!"
    brief=json.loads(BRIEF.read_text(encoding="utf-8"))
    assert len(brief["posts"])==2
    assets=[]
    for post in brief["posts"]:
        assert len(post["slides"])==6
        for i,slide in enumerate(post["slides"]):
            p=page(post,i,slide)
            assets.append({"path":p.relative_to(ROOT).as_posix(),
                           "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
                           "post_id":post["id"],"order":i+1})
            print(p.relative_to(ROOT),p.stat().st_size)
    manifest={"date":"2026-11-10","preset":"TUE-MESTRE-01",
              "staging_only":True,"technical_qc":True,"visual_reviewed":False,
              "approved":False,"published":False,"images":assets}
    (STAGE/"render-manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
if __name__=="__main__":main()
