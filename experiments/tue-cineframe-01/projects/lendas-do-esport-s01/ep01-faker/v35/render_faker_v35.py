#!/usr/bin/env python3
"""Faker EP01 v3.5: 112s contextual motion documentary with CC-licensed historical media.
No stock, no generic AI faces, no paid APIs, no publishing. Original graphics are animated,
photographs remain visibly labeled stills, one authentic 2020 interview plays as real video.
"""
from __future__ import annotations
import io, os, json, math, random, subprocess, hashlib, wave, html, sys, textwrap, urllib.parse
from pathlib import Path
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"; OUT.mkdir(parents=True,exist_ok=True)
MEDIA=OUT/"media";MEDIA.mkdir(exist_ok=True)
W,H,FPS,SECONDS=720,1280,30,112
RED=(241,48,70);BLUE=(44,156,240);WHITE=(242,245,250);GOLD=(244,194,87);DARK=(10,17,31)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTS={(s,b):ImageFont.truetype(BOLD if b else FONT,s) for s in [17,18,20,22,24,25,28,31,35,39,42,50,56,62,68,78,100,130] for b in (True,False)}
F=lambda s,b=True:FONTS[(s,b)]
ASSETS={
"faker2015":("Faker at 2015 Worlds.jpeg","Bruce Liu","CC license, Wikimedia Commons"),
"arena2017":("League of Legends World Championship 2017 Finals.jpg","Richard Ye","CC BY-SA 2.0"),
"t12022":("T1 at 2022 Worlds Media Day (1).jpg","fomos esports","CC BY 3.0"),
"trophy2023":("T1 hold 2023 Summoners Cup.jpg","Creative Silver","CC BY 4.0"),
"winners2024":("T1 win 2024 Worlds.jpg","fomos esports","CC BY 3.0"),
"faker2025":("Faker 2025 Worlds Final Post-Game.jpg","Fomos Esports","CC BY 3.0"),
"t12025":("T1 Worlds 2025 Media Day.jpg","Fomos Esports","CC license, verify"),
"kt2025":("KT Worlds 2025 Media Day.jpg","Fomos Esports","CC license, verify"),
"interview2020":("'페이커' 이상혁, 이제 아침을 먹겠습니다 .webm","fomos esports","CC BY 3.0")
}
SRC_LIST=[]
def fetch_asset(key):
    name,credit,license_name=ASSETS[key]; dest=MEDIA/(key+(".webm" if key=="interview2020" else ".jpg"))
    if dest.exists() and dest.stat().st_size>2000:return dest
    headers={"User-Agent":"TUE-Cineframe/1.0 (history documentary, github project)","Accept":"*/*"}
    params={"action":"query","format":"json","prop":"imageinfo","iiprop":"url|extmetadata","titles":"File:"+name}
    if key=="arena2017":params["iiurlwidth"]="1920"
    if key=="interview2020":params["iiurlwidth"]="1280"
    try:
        r=requests.get("https://commons.wikimedia.org/w/api.php",params=params,headers=headers,timeout=25);r.raise_for_status()
        pages=r.json()["query"]["pages"];item=next(iter(pages.values()))["imageinfo"][0]
        url=item.get("thumburl") or item["url"]
        lic=html.unescape(item.get("extmetadata",{}).get("LicenseShortName",{}).get("value",""))
        if not ("CC" in lic or "Attribution" in lic or "Creative Commons" in lic):
            print("UNVERIFIED_MEDIA_LICENSE",key,lic);return None
        d=requests.get(url,headers=headers,timeout=70);d.raise_for_status()
        if len(d.content)<3000:raise ValueError("Downloaded file too small")
        if len(d.content)>60_000_000:raise ValueError("Archive over size guard")
        dest.write_bytes(d.content)
        SRC_LIST.append({"key":key,"file":name,"url":"https://commons.wikimedia.org/wiki/File:"+urllib.parse.quote(name.replace(" ","_")),"download_url":url,"credit":credit,"license":lic,"sha256":hashlib.sha256(d.content).hexdigest(),"bytes":len(d.content)})
        print("MEDIA_FETCHED",key,len(d.content),lic,flush=True)
        return dest
    except Exception as ex:
        print("MEDIA_UNAVAILABLE",key,type(ex).__name__,str(ex)[:240],flush=True)
        return None

asset_paths={k:fetch_asset(k) for k in ASSETS}
# Text-only layouts are a fail-safe, not a claim that a photo/video was imported.
def draw_gradient_scene(seed):
    rng=np.random.default_rng(seed);a=np.zeros((H,W,3),dtype=np.uint8)
    yy=np.linspace(0,1,H,dtype=np.float32)
    base=np.array([9+10*yy,14+12*yy,27+17*yy]).T
    for c in range(3):a[:,:,c]=base[:,c,None]
    for j in range(55):
        x=int(rng.integers(0,W));y=int(rng.integers(0,H));r=int(rng.integers(1,5))
        col=(90,40,70) if j%2 else (38,80,105)
        a[max(0,y-r):min(H,y+r+1),max(0,x-r):min(W,x+r+1)]=col
    return Image.fromarray(a)
def photo_bg(key):
    if asset_paths.get(key):
        try:
            im=Image.open(asset_paths[key]).convert("RGB")
            # Never create fake photo motion: image fixed, graphic overlays move over it.
            im=ImageOps.fit(im,(W,875),method=Image.Resampling.LANCZOS,centering=(.5,.46))
            bg=draw_gradient_scene(abs(hash(key))%99999)
            bg.paste(im,(0,180))
            mask=Image.new("L",(W,H),0);dr=ImageDraw.Draw(mask)
            for y in range(H):
                if y<180:alpha=0
                elif y<275:alpha=int((y-180)/95*205)
                elif y<900:alpha=205
                elif y<1090:alpha=int(205*(1090-y)/190)
                else:alpha=0
                dr.line((0,y,W,y),fill=alpha)
            layer=Image.new("RGB",(W,H),(0,0,0))
            bg=Image.composite(Image.blend(bg,layer,.24),draw_gradient_scene(0),mask)
            return bg
        except Exception as e:print("PHOTO_FAILED",key,e)
    return draw_gradient_scene(abs(hash(key))%99999)
# Keep all shots in facts checked from Leaguepedia/Riot. No fabricated quote or face.
SHOTS=[
  dict(year="2017",head="O SILÊNCIO DE UMA FINAL",sub="A Samsung Galaxy vence a SKT por 3 a 0",kind="photo",img="arena2017",team="SKT",opponent="SAMSUNG GALAXY",score="0 : 3",roster=("Huni","Peanut","Faker","Bang","Wolf"),narr="O fim de uma dinastia parecia definitivo.",tag="FOTO DE ARQUIVO • ARENA 2017"),
  dict(year="2013",head="O NOVATO DE 17 ANOS",sub="Lee Sang-hyeok estreia no profissional",kind="arena",team="SK TELECOM T1",opponent="ROYAL CLUB",score="3 : 0",roster=("Impact","Bengi","Faker","Piglet","PoohManDu"),narr="Reflexos, leitura de mapa e decisões extraordinárias.",tag="RECONSTITUIÇÃO GRÁFICA"),
  dict(year="2013",head="O JOGO POR TRÁS DA LENDA",sub="Dois times. Cinco jogadores. Um Nexus.",kind="map",team="AZUL",opponent="VERMELHO",score="5 vs 5",roster=("Top","Jungle","Mid","Bot","Support"),narr="O meio controla a ligação entre as rotas.",tag="SIMULAÇÃO TÁTICA 2D"),
  dict(year="2013",head="O PRIMEIRO MUNDIAL",sub="SK Telecom T1 supera Royal Club por 3–0",kind="champ",team="SK TELECOM T1",opponent="ROYAL CLUB",score="3 : 0",roster=("Impact","Bengi","Faker","Piglet","PoohManDu"),narr="Aos 17 anos, Faker já era campeão mundial.",tag="RECONSTITUIÇÃO GRÁFICA"),
  dict(year="2015",head="A VOLTA AO TRONO",sub="SKT derrota KOO Tigers por 3–1",kind="photo",img="faker2015",team="SK TELECOM T1",opponent="KOO TIGERS",score="3 : 1",roster=("MaRin","Bengi","Faker","Bang","Wolf"),narr="A equipe muda. A excelência permanece.",tag="FOTO DE ARQUIVO • 2015"),
  dict(year="2016",head="O QUINTO JOGO",sub="SKT e Samsung Galaxy chegam à decisão",kind="map",team="SK TELECOM T1",opponent="SAMSUNG GALAXY",score="3 : 2",roster=("Duke","Bengi","Faker","Bang","Wolf"),narr="A final é decidida somente na quinta partida.",tag="SIMULAÇÃO TÁTICA 2D"),
  dict(year="2017",head="A DERROTA QUE MARCOU",sub="Samsung Galaxy derrota a SKT por 3–0",kind="photo",img="arena2017",team="SK TELECOM T1",opponent="SAMSUNG GALAXY",score="0 : 3",roster=("Huni","Peanut","Faker","Bang","Wolf"),narr="O peso de perder diante de um estádio lotado.",tag="FOTO DE ARQUIVO • FINAL 2017"),
  dict(year="2020",head="O TRABALHO NÃO PAROU",sub="Faker permanece ativo entre mudanças de elenco",kind="interview",img="interview2020",team="T1",opponent="NOVA GERAÇÃO",score="—",roster=("Faker","Treino","Equipe","Estratégia","Adaptação"),narr="A carreira é construída muito além das finais.",tag="ENTREVISTA REAL DE 2020 • FOMOS ESPORTS"),
  dict(year="2022",head="A ÚLTIMA PARTIDA ESCAPA",sub="A DRX supera a T1 por 3–2",kind="photo",img="t12022",team="T1",opponent="DRX",score="2 : 3",roster=("Zeus","Oner","Faker","Gumayusi","Keria"),narr="Deft e a DRX vencem uma série histórica.",tag="FOTO DE ARQUIVO • T1 2022"),
  dict(year="2023",head="RECONSTRUÍDOS EM EQUIPE",sub="T1 derrota Weibo Gaming por 3–0",kind="photo",img="trophy2023",team="T1",opponent="WEIBO GAMING",score="3 : 0",roster=("Zeus","Oner","Faker","Gumayusi","Keria"),narr="O quarto mundial chega após sete anos.",tag="FOTO REAL • FINAL DE 2023"),
  dict(year="2024",head="UMA FINAL NO LIMITE",sub="T1 vence Bilibili Gaming no quinto jogo",kind="photo",img="winners2024",team="T1",opponent="BILIBILI GAMING",score="3 : 2",roster=("Zeus","Oner","Faker","Gumayusi","Keria"),narr="Cinco títulos. O primeiro Hall of Legends.",tag="FOTO REAL • FINAL DE 2024"),
  dict(year="2025",head="UMA EQUIPE DIFERENTE",sub="Doran substitui Zeus no topo da T1",kind="photo",img="t12025",team="T1",opponent="KT ROLSTER",score="2 : 2",roster=("Doran","Oner","Faker","Gumayusi","Keria"),narr="Um rival histórico. Outra série de cinco jogos.",tag="FOTO REAL • ELENCO 2025"),
  dict(year="2025",head="O JOGO QUE DECIDE TUDO",sub="T1 e KT Rolster disputam o quinto jogo",kind="map",team="T1",opponent="KT ROLSTER",score="3 : 2",roster=("Doran","Oner","Faker","Gumayusi","Keria"),narr="T1, KT, KT, T1... e o quinto jogo.",tag="SIMULAÇÃO TÁTICA 2D • NÃO É GAMEPLAY"),
  dict(year="2025",head="SEIS MUNDIAIS",sub="Três títulos consecutivos: 2023, 2024, 2025",kind="photo",img="faker2025",team="T1",opponent="KT ROLSTER",score="3 : 2",roster=("Doran","Oner","Faker","Gumayusi","Keria"),narr="Uma década de adaptações. A lenda continua.",tag="FOTO DE ARQUIVO • FINAL 2025")
]
assert len(SHOTS)==14
# Precompose photo backgrounds once. No artificial pans/zooms.
BGS=[photo_bg(s["img"]) if s["kind"]=="photo" else draw_gradient_scene(i*73+5) for i,s in enumerate(SHOTS)]
# Render the interview to a silent raw RGB frame stream, fall back if unavailable.
interview=None
if asset_paths.get("interview2020"):
    try:
        args=["ffmpeg","-v","error","-ss","30","-i",str(asset_paths["interview2020"]),"-t","8","-an","-vf","fps=30,scale=720:650:force_original_aspect_ratio=increase,crop=720:650","-pix_fmt","rgb24","-f","rawvideo","pipe:1"]
        interview=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,bufsize=128*1024)
        print("REAL_VIDEO_ARCHIVE_2020_USED",flush=True)
    except Exception as ex:print("INTERVIEW_DECODE_FAILED",ex,flush=True)
# Overlays and video body
def text(draw,xy,message,size,color=WHITE,stroke=0,anchor=None):
    draw.text(xy,message,font=F(size),fill=color,stroke_width=stroke,stroke_fill=(0,0,0),anchor=anchor)
def lerp(a,b,t):return a+(b-a)*max(0,min(1,t))
def ease(t):return 1-(1-max(0,min(1,t)))**3
def compose_map(im,shot,t,idx):
    d=ImageDraw.Draw(im,"RGBA")
    rect=(44,340,676,985)
    d.rounded_rectangle(rect,radius=20,fill=(13,27,44,245),outline=(65,99,128,180),width=3)
    # A clear fictionalized tactical map: no League of Legends gameplay passed off as broadcast footage.
    M=(115,395,612,917)
    d.polygon([(130,894),(130,409),(598,409),(598,894)],fill=(18,41,56,255),outline=(77,117,135,240),width=3)
    # lanes
    for off in [-10,0,10]:
        d.line((160+off,852,562+off,455),fill=(85,120,126,190),width=5 if off==0 else 1)
    d.line((162,866,564,866),fill=(96,132,120,180),width=6);d.line((564,866,564,454),fill=(96,132,120,180),width=6)
    d.line((162,866,162,453),fill=(96,132,120,180),width=6);d.line((162,453,560,453),fill=(96,132,120,180),width=6)
    # towers jungle camp corners
    for k in range(7):
        x=158+(k%3)*198;y=455+(k//3)*205
        d.ellipse((x-8,y-8,x+8,y+8),fill=(50,90,80,255),outline=(76,143,150,255),width=2)
    # blue and red moving team markers animate across diagonal / lanes
    prog=(t/8)
    for j in range(5):
        lane=(j-2)*20
        x=int(170+350*max(0,min(1,prog*1.35-j*.08))+lane*.35)
        y=int(860-356*max(0,min(1,prog*1.35-j*.08))-lane*.27)
        rx=int(560-305*max(0,min(1,prog*1.05-j*.085))+lane*.35)
        ry=int(476+313*max(0,min(1,prog*1.05-j*.085))-lane*.25)
        d.ellipse((x-12,y-12,x+12,y+12),fill=(*BLUE,255),outline=WHITE,width=2)
        d.ellipse((rx-12,ry-12,rx+12,ry+12),fill=(*RED,255),outline=WHITE,width=2)
    if prog>.36:
        cx=int(390+18*math.sin(t*4))
        cy=int(630+12*math.cos(t*3))
        radius=20+int(26*(math.sin(t*2.5)**2))
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=(*GOLD,180),width=4)
        d.arc((cx-55,cy-55,cx+55,cy+55),0,int(360*prog),fill=(*GOLD,250),width=5)
    text(d,(75,952),"SIMULAÇÃO DE ROTAS E OBJETIVOS",18,GOLD)
def score_widget(im,s,t):
    d=ImageDraw.Draw(im,"RGBA");d.rounded_rectangle((34,1030,686,1167),radius=17,fill=(10,16,28,240),outline=(75,93,120,220),width=2)
    a=s["team"];b=s["opponent"];score=s["score"]
    text(d,(60,1046),a[:24],20,RED)
    text(d,(660,1046),b[:24],20,BLUE,anchor="ra")
    text(d,(360,1084),score,50,GOLD,anchor="ma")
    if ":" in score:
        try:
            wa,wb=[int(x.strip()) for x in score.split(":")]
        except:wa,wb=0,0
        n=wa+wb;completed=int(min(n, math.floor(lerp(0,n,(t-.4)/6))))
        x0=305
        for k in range(max(1,n)):
            x=x0+(k-2)*28
            owner= k in [i for i in range(n) if i%2==0] # decorative; never pretend game-by-game historical
            col=RED if k<wa else BLUE
            d.ellipse((x-6,1147,x+6,1159),fill=(*col,255) if k<completed else (70,76,90,255))
def intro_overlay(im,s,t,idx):
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle((0,0,W,164),fill=(7,11,23,240))
    d.rectangle((0,0,10,H),fill=(*RED,255))
    d.line((0,164,W,164),fill=(*RED,255),width=3)
    text(d,(33,27),"LENDAS DO ESPORT  /  EP. 01",18,GOLD)
    text(d,(36,58),s["year"],56,WHITE)
    text(d,(205,92),s["head"],24,WHITE)
    text(d,(38,1198),s["narr"],20,WHITE)
    text(d,(38,1241),s["tag"],17,GOLD)
    # animate red accent by filling dynamically: a real graphic, not image zoom
    d.rounded_rectangle((36,1190,36+int(648*ease(t/7.8)),1195),radius=3,fill=(*RED,255))
def roster_card(im,s,t):
    d=ImageDraw.Draw(im,"RGBA")
    if s["kind"]=="map":return
    # roster title and staggered revealed names; no invented faces
    x1=35;y0=214
    d.rounded_rectangle((x1,y0,685,y0+105),radius=12,fill=(6,14,28,204),outline=(60,90,125,100),width=2)
    text(d,(48,y0+8),"ELENCO DA ÉPOCA / TIME DE FAKER",18,GOLD)
    ss=s["roster"]
    for j,name in enumerate(ss):
        if t>j*.25:
            x=48+j*125
            d.rounded_rectangle((x,y0+40,x+116,y0+80),radius=5,fill=(*RED,70+int(70*ease((t-j*.25)))),outline=(130,80,80,145),width=1)
            d.text((x+57,y0+61),name,font=F(17),fill=WHITE,anchor="mm")
def light_particles(im,t,shot_idx,kind):
    # Foreground independently animated show/event light and energy (no photographic zoom)
    d=ImageDraw.Draw(im,"RGBA")
    rnd=random.Random(shot_idx*1732)
    for j in range(28):
        x0=rnd.uniform(0,W);speed=rnd.uniform(28,88)
        y0=rnd.uniform(-200,1200);y=(y0+t*speed)%1400-110
        x=x0+math.sin(t*.75+j)*12
        sz=2+rnd.uniform(0,3)
        color=(244,185,80,115) if kind in ("champ","photo") else (74,175,249,80)
        d.ellipse((x-sz,y-sz,x+sz,y+sz),fill=color)
def draw_frame(index,t):
    s=SHOTS[index];im=BGS[index].copy()
    if s["kind"]=="interview" and interview is not None:
        raw=interview.stdout.read(720*650*3)
        if len(raw)==720*650*3:
            frame=Image.frombytes("RGB",(720,650),raw)
            im.paste(frame,(0,360))
    elif s["kind"] in ("arena","champ"):
        # Original vector story illustration instead of inventing photography.
        d=ImageDraw.Draw(im,"RGBA")
        for j in range(15):
            x=30+j*54
            d.polygon([(x,440),(x+23,320),(x+46,440)],fill=(38,58,85,140))
        for j in range(6):
            x=50+j*116
            d.ellipse((x-15,650,x+55,740),fill=(24,29,53,255),outline=(146,40,52,200),width=3)
            d.line((x+20,738,x+15,830),fill=(31,45,66,255),width=17)
        for i in range(7):
            cy=430+i*67
            d.line((40,cy,680,cy),fill=(70,87,118,50),width=1)
        d.rounded_rectangle((70,846,650,940),radius=12,fill=(15,26,43,230))
        text(d,(360,881),"2013 • INÍCIO DE UMA LENDA" if index==1 else "UM NOVO CAPÍTULO",31,GOLD,anchor="ma")
    if s["kind"]=="map":compose_map(im,s,t,index)
    light_particles(im,t,index,s["kind"])
    roster_card(im,s,t)
    intro_overlay(im,s,t,index)
    score_widget(im,s,t)
    return im

def make_audio(out):
    # Original, non-TTS ambient score. No claim of Rasalgethi.
    sr=22050;n=int(SECONDS*sr);a=np.zeros(n,dtype=np.float32)
    for start in range(0,SECONDS,8):
        dur=8;begin=start*sr;end=(start+dur)*sr
        tt=np.arange(dur*sr,dtype=np.float32)/sr
        chord=[55,82.4,110] if start<56 else [65.4,98,130.8]
        pad=np.zeros(len(tt),dtype=np.float32)
        for f in chord:
            pad+=np.sin(2*np.pi*f*tt+0.15*np.sin(tt*.3))*.05
        fade=np.clip(tt/1.7,0,1)*np.clip((dur-tt)/1.5,0,1)
        a[begin:end]+=pad*fade
        for beat in range(0,8,2):
            k=begin+beat*sr;nn=min(sr//4,len(a)-k)
            if nn>0:
                t0=np.arange(nn,dtype=np.float32)/sr
                a[k:k+nn]+=.028*np.sin(2*np.pi*(190-100*t0)*t0)*np.exp(-13*t0)
    a=np.clip(a,-.7,.7)
    with wave.open(str(out),"wb") as wf:
        wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes((a*32767).astype("<i2").tobytes())
def make_movie():
    print("BUILD_START",len(SHOTS),len([k for k in asset_paths if asset_paths[k]]),flush=True)
    silent=OUT/"faker_v35_video_only.mp4";final=OUT/"EP01_FAKER_V35_112s_CONTEXTUAL_ARQUIVO_CC_REVISAO.mp4"
    codec=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-an","-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p","-movflags","+faststart",str(silent)]
    p=subprocess.Popen(codec,stdin=subprocess.PIPE)
    try:
        for f in range(FPS*SECONDS):
            shot=f//(8*FPS);t=(f%(8*FPS))/FPS
            im=draw_frame(shot,t)
            p.stdin.write(im.tobytes())
            if f%240==0:print("FRAME_PROGRESS",f,flush=True)
    finally:
        p.stdin.close()
    if p.wait()!=0:raise RuntimeError("Video encoder failed")
    wav=OUT/"original_ambient_pad.wav";make_audio(wav)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(silent),"-i",str(wav),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",str(final)]
    subprocess.run(cmd,check=True,timeout=240)
    raw=subprocess.check_output(["ffprobe","-v","error","-count_frames","-show_entries","stream=codec_type,width,height,r_frame_rate,nb_read_frames:format=duration,size","-of","json",str(final)])
    probe=json.loads(raw)
    vs=next(x for x in probe["streams"] if x["codec_type"]=="video")
    assert int(vs["nb_read_frames"])==FPS*SECONDS,vs
    assert (vs["width"],vs["height"],vs["r_frame_rate"])==(W,H,"30/1")
    assert abs(float(probe["format"]["duration"])-112)<0.03
    qc={"asset_successes":{k:bool(p) for k,p in asset_paths.items()},"historical_real_video_used":interview is not None,
        "source_licenses":SRC_LIST,"clips":14,"frames":FPS*SECONDS,"resolution":[W,H],"fps":FPS,"duration":112,
        "contains_rasalgethi":False,"source_has_original_broadcast_video":False,
        "scene_type":"Genuine 2020 interview excerpt and archival CC photos, independent 2D tactical motion graphics; not match-footage recordings",
        "sha256":hashlib.sha256(final.read_bytes()).hexdigest(),"bytes":final.stat().st_size,"probe":probe,
        "published":False,"scheduled":False,"approved":False}
    (OUT/"QC_AND_SOURCES.json").write_text(json.dumps(qc,ensure_ascii=False,indent=2),encoding="utf8")
    # supplementary attribution in full text
    (OUT/"CREDITOS_E_LIMITACOES.md").write_text("# FONTES E CRÉDITOS – FAKER V3.5\n\n"+ "\n".join(
        f"- {v['file']} — {v['credit']}, {v['license']}: {v['url']}" for v in SRC_LIST)+
        "\n\nFotografias mantidas estáticas e identificadas. Não são tratadas como clipes de jogo. Retratos gerados não foram usados. Movimentos são de gráficos táticos e de entrevista real. Sem Rasalgethi. Revisão apenas, sem publicação.\n",encoding="utf8")
    print("COMPLETE",str(final),"SHA256",qc["sha256"],"BYTES",qc["bytes"],flush=True)
if __name__=="__main__":
    make_movie()
