import os, sys, pathlib, subprocess, time, hashlib, urllib.request, urllib.parse, math, json
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path.cwd()
W = ROOT / "build-real-reel-07nov"
W.mkdir(exist_ok=True)
OUT = ROOT / "content/staging/instagram/2026-11-07/REELS-18H-PREDIOS-VIDEOS-REAIS-QC.mp4"
OUT.parent.mkdir(parents=True,exist_ok=True)
def cmd(args):
    print("+", " ".join(str(x) for x in args), flush=True)
    subprocess.run([str(x) for x in args],check=True)
def download(name):
    file = W / name
    if file.exists() and file.stat().st_size > 100000: return file
    id_by_name = {
      "taipei_1.mp4":"mixkit-aerial-shot-of-a-busy-avenue-in-the-city-2034_clip_1.mp4",
      "building_1.mp4":"mixkit-aerial-shot-of-buildings-in-a-city-1670_clip_1.mp4",
      "building_2.mp4":"mixkit-aerial-view-of-a-city-during-the-morning-1617_clip_1.mp4",
      "taipei_2.mp4":"mixkit-aerial-panorama-of-a-big-city-at-night-42352_clip_1.mp4"
    }
    identifier=id_by_name[name]
    urls=[
      "https://huggingface.co/datasets/FastVideo/Mixkit-Src/resolve/main/Traffic/"+identifier+"?download=true",
      "https://huggingface.co/datasets/FastVideo/Mixkit-Src/resolve/main/Traffic/"+identifier+"?download=true".replace("-large.mp4","-medium.mp4")
    ]
    for remote in urls:
        try:
            req=urllib.request.Request(remote,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                                                       "Accept":"video/mp4,application/octet-stream,*/*","Referer":"https://huggingface.co/"})
            with urllib.request.urlopen(req,timeout=90) as src,open(file,"wb") as dst:
                while True:
                    block=src.read(1048576)
                    if not block:break
                    dst.write(block)
            if file.stat().st_size < 100000:raise RuntimeError("video too small")
            p=subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type","-of","default=nw=1:nk=1",str(file)],text=True)
            if "video" not in p:raise RuntimeError("download was not video")
            print("SAVED_VIDEO",name,file.stat().st_size,flush=True)
            return file
        except Exception as ex:
            print("SOURCE_ATTEMPT_FAILED",name,str(ex),flush=True)
            if file.exists():file.unlink()
            time.sleep(1)
    raise RuntimeError("Cannot obtain freely licensed real video "+name)
sources={
 "taipei":"taipei_1.mp4",
 "toronto":"building_1.mp4",
 "toronto_short":"building_2.mp4",
 "sf":"taipei_2.mp4",
}

for k,v in sources.items():download(v)
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
reg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F=ImageFont.truetype(bold,53)
S=ImageFont.truetype(reg,25)
small=ImageFont.truetype(reg,21)
def title_png(i,title,location):
    # Overlay only subtitling on actual videos. No banner, no logo, no interface graphics.
    im=Image.new("RGBA",(720,1280),(0,0,0,0)); d=ImageDraw.Draw(im)
    subtitles={
      0:"Um prédio alto pode balançar com o vento.",
      1:"O vento exerce pressão sobre a estrutura.",
      2:"A flexibilidade é prevista no projeto.",
      3:"No topo, o balanço pode causar desconforto.",
      4:"O Taipei 101 usa um amortecedor de massa.",
      5:"Uma massa de 660 toneladas ajuda a controlar as oscilações.",
      6:"Parte da energia do movimento é dissipada.",
      7:"O segredo está no projeto. Tem uma explicação."
    }
    phrase=subtitles[i]; font=ImageFont.truetype(reg,30)
    lines=[];line=""
    for word in phrase.split():
        test=(line+" "+word).strip()
        if d.textbbox((0,0),test,font=font)[2] > 630:
            if line: lines.append(line)
            line=word
        else: line=test
    if line: lines.append(line)
    y=1095-(len(lines)-1)*22
    for j,line in enumerate(lines):
        bbox=d.textbbox((0,0),line,font=font)
        x=(720-(bbox[2]-bbox[0]))//2
        d.text((x,y+j*43),line,font=font,fill=(255,255,251,255),stroke_width=4,stroke_fill=(15,15,15,238))
    out=W/("subtitle-%02d.png"%i);im.save(out);return out
scenes=[
  ("toronto",0,6,"PRÉDIOS ALTOS|BALANÇAM?","VÍDEO REAL • CIDADE MODERNA"),
  ("taipei",0,7,"O VENTO|EMPURRA","VÍDEO REAL • CENÁRIO URBANO"),
  ("toronto_short",0,7,"FLEXIBILIDADE|CONTROLADA","VÍDEO REAL • CIDADE MODERNA"),
  ("toronto",0,6,"NO ALTO, O|MOVIMENTO CONTA","VÍDEO REAL • PANORAMA URBANO"),
  ("taipei",0,7,"TAIPEI 101|TAIWAN","VÍDEO REAL • CENÁRIO URBANO"),
  ("taipei",0,9,"660 TONELADAS|EM MOVIMENTO","VÍDEO REAL + SIMULAÇÃO TÉCNICA"),
  ("toronto",0,7,"AMORTECEDOR|REDUZ A OSCILAÇÃO","VÍDEO REAL • EXEMPLO URBANO"),
  ("sf",0,5,"PROJETADO|PARA FLEXIONAR","VÍDEO REAL • CENÁRIO URBANO"),
]
assert sum(s[2] for s in scenes)==54
# TUE-MESTRE-01 editorial diagram: IVORY paper, BLACK ink, YELLOW paint, RED signal.
# Real kinematics, no neon-blue science fiction sphere or decorative UI.
PAPER=(250,248,241,255); INK=(26,24,22,255)
YELLOW=(251,194,40,255); RED=(214,40,41,255)
MUTED=(110,106,98,255)
BIG=ImageFont.truetype(bold,47)
MID=ImageFont.truetype(reg,26)
SMALL=ImageFont.truetype(reg,20)
STRONG=ImageFont.truetype(bold,27)
def paper():
    im=Image.new("RGBA",(720,1280),PAPER)
    d=ImageDraw.Draw(im)
    for k in range(0,1280,50):d.line((0,k,720,k),fill=(232,229,221,150),width=1)
    for k in range(0,720,50):d.line((k,0,k,1280),fill=(232,229,221,150),width=1)
    return im
def header(d,title,subtitle):
    d.polygon([(38,108),(649,102),(654,173),(40,180)],fill=YELLOW)
    d.text((54,113),title,font=BIG,fill=INK)
    d.text((53,211),subtitle,font=MID,fill=INK)
def arrow(d,x,y,x2,y2,color):
    d.line((int(x),int(y),int(x2),int(y2)),fill=color,width=5)
    ang=math.atan2(y2-y,x2-x)
    for k in (-1,1):
        ang2=ang+math.pi+k*.45
        d.line((int(x2),int(y2),int(x2+17*math.cos(ang2)),int(y2+17*math.sin(ang2))),fill=color,width=5)
def sim_png(t,num):
    im=paper();d=ImageDraw.Draw(im)
    header(d,"AMORTECEDOR DE MASSA","ESQUEMA TÉCNICO ILUSTRATIVO")
    phi=2*math.pi*t/4.8
    xb=16*math.sin(phi)
    xm=8*math.sin(phi)-62*math.sin(phi-.45)
    sx=360+xb;mx=360+xm;y=692;rad=106
    d.line((sx-215,398,sx+215,398),fill=INK,width=14)
    d.line((sx-215,333,sx-215,472),fill=INK,width=10)
    d.line((sx+215,333,sx+215,472),fill=INK,width=10)
    for offset in [-55,55]:
        d.line((sx+offset,398,mx+offset,y-rad+12),fill=INK,width=5)
    d.ellipse((mx-rad,y-rad,mx+rad,y+rad),fill=YELLOW,outline=INK,width=7)
    d.text((mx-71,y-25),"660 t",font=BIG,fill=INK)
    # Damper cylinders connected between suspended mass and moving structural base
    for sign in [-1,1]:
        ax=mx+sign*63;bx=sx+sign*162
        d.line((ax,y+90,bx,958),fill=INK,width=14)
        d.ellipse((ax-8,y+82,ax+8,y+98),fill=RED)
        cx=.54*ax+.46*bx;cy=.54*(y+90)+.46*958
        d.ellipse((cx-15,cy-15,cx+15,cy+15),fill=MUTED,outline=INK,width=2)
    d.line((sx-225,963,sx+225,963),fill=INK,width=13)
    d.line((360,330,360,987),fill=(155,151,143,120),width=2)
    if abs(xb)>3:arrow(d,360,302,360+xb,302,RED)
    if abs(xm-xb)>3:arrow(d,sx,840,mx,840,INK)
    d.line((58,1023,90,1023),fill=RED,width=5)
    d.text((103,1008),"ESTRUTURA EM MOVIMENTO",font=STRONG,fill=INK)
    d.line((58,1074,90,1074),fill=INK,width=5)
    d.text((103,1059),"MASSA E AMORTECEDORES",font=STRONG,fill=INK)
    d.text((50,1194),"SIMULAÇÃO DIDÁTICA · DESLOCAMENTO EXAGERADO",font=SMALL,fill=MUTED)
    out=W/("sim-%04d.png"%num);im.save(out);return out
def plot_png(t,num):
    im=paper();d=ImageDraw.Draw(im)
    header(d,"MENOS OSCILAÇÃO","COMPARAÇÃO ILUSTRATIVA DA RESPOSTA")
    x0,x1=80,650
    for y0,amp,label,col in [(532,78,"SEM AMORTECEDOR",RED),(846,29,"COM AMORTECEDOR",INK)]:
        d.text((82,y0-150),label,font=STRONG,fill=INK)
        d.line((x0,y0,x1,y0),fill=MUTED,width=2)
        end=int(x0+(x1-x0)*min(1,t/6.3))
        pts=[]
        for x in range(x0,end+1,3):
            phase=6*math.pi*(x-x0)/(x1-x0)
            pts.append((x,int(y0-amp*math.exp(-.04*phase)*math.sin(phase))))
        if len(pts)>1:d.line(pts,fill=col,width=6)
        if pts:
            px,py=pts[-1]
            d.ellipse((px-8,py-8,px+8,py+8),fill=YELLOW,outline=INK,width=2)
        d.text((80,y0+104),"TEMPO  →",font=SMALL,fill=MUTED)
    d.line((80,1090,635,1090),fill=YELLOW,width=9)
    d.text((80,1116),"Menos movimento; energia dissipada.",font=MID,fill=INK)
    d.text((50,1194),"GRÁFICO DIDÁTICO · SEM ESCALA",font=SMALL,fill=MUTED)
    out=W/("plot-%04d.png"%num);im.save(out);return out

for i,(src,start,duration,title,place) in enumerate(scenes):
    over=title_png(i,title,place)
    target=W/("scene-%02d.mp4"%i)
    filename=W/sources[src]
    filt="[0:v]fps=30,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,eq=contrast=1.035:saturation=1.12,setsar=1[base];[base][1:v]overlay=0:0:shortest=1"
    inputs=["-stream_loop","-1","-ss",str(start),"-i",str(filename),"-loop","1","-framerate","30","-i",str(over)]
    if i in (5,6):
        for n in range(duration*30):
            if i==5: sim_png(n/30,n)
            else: plot_png(n/30,n)
        pathpattern="sim-%04d.png" if i==5 else "plot-%04d.png"
        inputs.extend(["-framerate","30","-i",str(W/pathpattern)])
        filt+="[titled];[titled][2:v]overlay=0:0:shortest=1[v]"
    else:
        filt+="[v]"
    args=["ffmpeg","-hide_banner","-loglevel","error","-y",*inputs,
          "-filter_complex",filt,"-map","[v]","-an",
          "-t",str(duration),"-frames:v",str(duration*30),
          "-c:v","libx264","-crf","22","-preset","fast","-pix_fmt","yuv420p","-r","30",str(target)]
    cmd(args)
    probe=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(target)],text=True).strip()
    if abs(float(probe)-duration)>0.09:raise RuntimeError("Unexpected scene duration: "+probe)
concat=W/"concat.txt"
concat.write_text("".join("file '"+str(W/("scene-%02d.mp4"%i))+"'\n" for i in range(len(scenes))),encoding="utf-8")
silent=W/"silent_video.mp4"
cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)])
# Speech from the old video is NOT available to this cloud job; this is NOT a publishing master.
cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(silent),"-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
     "-map","0:v:0","-map","1:a:0","-t","54","-c:v","copy","-c:a","aac","-b:a","64k","-movflags","+faststart",str(OUT)])
metadata=subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height,r_frame_rate:format=duration,size","-of","json",str(OUT)],text=True)
data=json.loads(metadata)
assert abs(float(data["format"]["duration"])-54)<.25
assert data["streams"][0]["width"]==720 and data["streams"][0]["height"]==1280
import hashlib as H
digest=H.sha256(OUT.read_bytes()).hexdigest()
(W/"creditos.txt").write_text(
 "EDITORIAL: visual-motion documentary preview only; original Rasalgethi voice missing, do not publish.\n"
 "CLIP 1 (Mixkit Stock Video Free License): https://mixkit.co/free-stock-video/aerial-shot-of-a-busy-avenue-in-the-city-2034/\n"
 "CLIP 2 (Mixkit Stock Video Free License): https://mixkit.co/free-stock-video/aerial-shot-of-buildings-in-a-city-1670/\n"
 "CLIP 3 (Mixkit Stock Video Free License): https://mixkit.co/free-stock-video/daytime-city-traffic-aerial-view-56/\n"
 "CLIP 4 (Mixkit Stock Video Free License): https://mixkit.co/free-stock-video/drone-flying-over-a-city-at-sunset-44804/\n"
 "Simulação física vetorial desenhada por procedimento para explicar funcionamento, não é uma gravação real do amortecedor.\n"
 "Não exibir cidades diferentes como Taipei; créditos e etiquetas distinguem cada cidade.\n"
 "Audio: silence (requires verified Rasalgethi narration from original video before distribution).\n"
 f"Output: {OUT.name}, SHA-256={digest}; 720x1280/30fps REVIEW ONLY, NOT native 4K60.\n",encoding="utf-8")
manifest={
 "standard":"TUE-MESTRE-01","reel":"predios-altos-balancam","output":str(OUT.relative_to(ROOT)),
 "sha256":digest,"duration_seconds":54,"format":"720x1280@30 for QC",
 "contains_real_video":True,"real_footage_count":4,"animated_diagram_seconds":16,
 "voice_status":"MISSING_RASALGETHI_MUST_REUSE_ORIGINAL","owner_approved":False,
 "safe_to_schedule":False,"safe_to_publish":False,"visual_style":"TUE_MESTRE_01_ivory_yellow_black_red","photographs_as_moving_video":False,
 "sources":[x for x in sources.values()]
}
(W/"metadata.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("PREVIEW_RENDERED",str(OUT),json.dumps(data),digest,flush=True)
