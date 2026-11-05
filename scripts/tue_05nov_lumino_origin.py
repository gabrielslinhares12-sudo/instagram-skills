#!/usr/bin/env python3
"""6 original TUE-MESTRE-01 slides using the IMMUTABLE canonical Lúmino PNG.
Editorial *fictional* origin, not a claim about the real creation of the mascot.
No publishing, account operations, or stories.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, hashlib, json, random
ROOT=Path(__file__).resolve().parents[1]
LUM=ROOT/"content/brand/lumino-original.png"
OUT=ROOT/"content/media/instagram/2026-11-05/lumino-origem"
OUT.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(LUM.read_bytes()).hexdigest()=="f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b", "LÚMINO ORIGINAL ALTERADO"
ORIGINAL=Image.open(LUM).convert("RGBA")
S=2; W=1080*S; H=1350*S
PAPER=(244,237,225);INK=(17,17,17);RED=(213,14,21);YELLOW=(255,214,0)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def pt(v): return int(round(v*S))
def F(sz,bold=True): return ImageFont.truetype(FONT if bold else BODY,pt(sz))
def rect(d,bb,fill,rad=0,outline=None,width=3):
 b=tuple(pt(q) for q in bb);d.rounded_rectangle(b,radius=pt(rad),fill=fill,outline=outline,width=pt(width))
def line(d,points,fill,width=3):
 d.line([(pt(x),pt(y)) for x,y in points],fill=fill,width=pt(width),joint="curve")
def title(d, lines, x,y,size=74):
 for k,s in enumerate(lines):
  d.text((pt(x),pt(y+k*size*1.04)),s,font=F(size),fill=INK,stroke_width=0)
def sub(d,lines,x,y,size=34,color=INK):
 for k,s in enumerate(lines):d.text((pt(x),pt(y+k*size*1.55)),s,font=F(size,False),fill=color)
def brush(im,y,x=54,w=730,thick=45):
 d=ImageDraw.Draw(im);rng=random.Random(y*3);p=[]
 for k in range(27):
  xx=x+w*k/26;p.append((pt(xx),pt(y+rng.randint(-6,7))))
 for k in range(26,-1,-1):
  xx=x+w*k/26;p.append((pt(xx),pt(y+thick+rng.randint(-7,7))))
 d.polygon(p,fill=YELLOW)
 for i in range(7):
  xx=x+rng.randint(0,w);line(d,[(xx,y-5),(xx+rng.randint(13,49),y-12)],(221,166,0),1)
def bg(seed):
 rng=random.Random(seed)
 im=Image.new("RGB",(W,H),PAPER)
 d=ImageDraw.Draw(im)
 for _ in range(5600):
  x=rng.randrange(W);y=rng.randrange(H)
  c=rng.choice([(251,245,231),(237,229,216),(229,226,212),(249,242,224)])
  d.point((x,y),fill=c)
 return im
def mascot(im,x,y,w=390,angle=0):
 h=round(w*ORIGINAL.height/ORIGINAL.width)
 obj=ORIGINAL.resize((pt(w),pt(h)),Image.Resampling.LANCZOS)
 if angle:obj=obj.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 shadow=Image.new("RGBA",obj.size,(0,0,0,0))
 alpha=obj.getchannel("A").filter(ImageFilter.GaussianBlur(pt(22)))
 shadow.paste((50,44,36,95),(0,0,obj.width,obj.height))
 shadow.putalpha(alpha.point(lambda a:int(a*.37)))
 im.paste(shadow,(pt(x)+pt(17),pt(y)+pt(22)),shadow)
 im.paste(obj,(pt(x),pt(y)),obj)
 return [x,y,w,h]
def frame(d,section):
 d.text((pt(56),pt(36)),"TEM UMA EXPLICAÇÃO",font=F(24),fill=INK)
 line(d,[(56,87),(1024,87)],(76,67,59),2)
 d.text((pt(56),pt(101)),"HISTÓRIA DO PERSONAGEM  ·  FICÇÃO",font=F(19,False),fill=RED)
def foot(im,i,n=6):
 d=ImageDraw.Draw(im)
 rect(d,[0,1239,1080,1350],PAPER)
 line(d,[(56,1239),(1023,1239)],(211,198,175),2)
 for j in range(n):
  x=487+(j-(n-1)/2)*22; y=1269
  d.ellipse([pt(x-5),pt(y-5),pt(x+5),pt(y+5)],fill=(244,185,0) if i==j else (179,178,173))
 if i<n-1:
  d.text((pt(405),pt(1285)),"A R R A S T E   P A R A   O   L A D O",font=F(12,False),fill=INK)
  line(d,[(796,1295),(847,1295),(838,1287)],INK,2)
 d.text((pt(56),pt(1327)),"LÚMINO · UM PERSONAGEM DO TEM UMA EXPLICAÇÃO",font=F(12,False),fill=(122,111,97))
def scene1(im):
 d=ImageDraw.Draw(im);brush(im,275,56,635,56)
 title(d,["QUEM É","O LÚMINO?"],54,158,84)
 sub(d,["A pequena luz que decidiu","investigar perguntas gigantes."],56,444,30)
 for r in range(9):
  x=755+(r%3)*81;y=570+(r//3)*77
  d.ellipse([pt(x),pt(y),pt(x+32),pt(y+32)],outline=(210,166,84),width=pt(3))
 # original is a true part of scene, not a replacement
 mascot(im,550,555,475)
 rect(d,[40,1085,1040,1153],(226,209,178),11)
 d.text((pt(77),pt(1098)),"UMA HISTÓRIA SOBRE A CURIOSIDADE.",font=F(32),fill=INK)
def scene2(im):
 d=ImageDraw.Draw(im)
 brush(im,228,50,855,54);title(d,["TUDO COMEÇOU","COM UMA PERGUNTA"],55,135,65)
 sub(d,["Por que o mundo é cheio","de coisas extraordinárias?"],59,422,31)
 # Workshop with distinctly drawn desk, instruments and stars
 rect(d,[50,738,1036,1161],(105,68,39),20)
 for i in range(11):
  x=78+i*84;rect(d,[x,810,x+39,1050],(165+i*3,100,58),3)
 d.ellipse([pt(105),pt(788),pt(465),pt(1120)],outline=(232,192,117),width=pt(12))
 d.ellipse([pt(155),pt(840),pt(420),pt(1068)],outline=(232,192,117),width=pt(3))
 for i in range(16):
  x=40+i*57; yy=570+((i*43)%112)
  d.ellipse([pt(x),pt(yy),pt(x+4),pt(yy+4)],fill=(203,165,82))
 mascot(im,534,646,444)
def scene3(im):
 d=ImageDraw.Draw(im);brush(im,212,56,812,58)
 title(d,["UMA LUZ","SE ACENDEU"],55,135,84)
 sub(d,["Não era mágica.","Era vontade de entender."],59,427,32)
 for i in range(14):
  angle=i*math.tau/14
  x=765+260*math.cos(angle);y=852+250*math.sin(angle)
  line(d,[(765,852),(x,y)],(255,200,36),5)
 d.ellipse([pt(496),pt(596),pt(1032),pt(1132)],outline=(232,194,74),width=pt(10))
 mascot(im,544,585,475)
 rect(d,[52,1110,470,1178],(235,223,198),9)
 d.text((pt(74),pt(1127)),"CURIOSIDADE > MEDO",font=F(28),fill=RED)
def scene4(im):
 d=ImageDraw.Draw(im);brush(im,243,51,850,62)
 title(d,["DO FUNDO","DO OCEANO..."],54,141,70)
 sub(d,["...ATÉ AS ESTRELAS."],60,408,39,RED)
 # deliberate photographic-like scene in illustration: ocean vs cosmos
 d.polygon([(0,pt(710)),(W,pt(594)),(W,pt(1235)),(0,pt(1235))],fill=(30,83,110))
 for i in range(7):
  y=797+i*52
  d.arc([pt(-80),pt(y),pt(1180),pt(y+84)],10,165,fill=(117,192,203),width=pt(4))
 for i in range(56):
  x=(i*167)%1080;y=530+(i*137)%248
  d.ellipse([pt(x),pt(y),pt(x+4+i%4),pt(y+4+i%4)],fill=(246,228,164))
 d.ellipse([pt(778),pt(538),pt(866),pt(625)],fill=(246,210,102))
 mascot(im,549,642,457)
def scene5(im):
 d=ImageDraw.Draw(im);brush(im,218,48,888,58)
 title(d,["RESPOSTA BOA","NÃO É CHUTE."],54,141,71)
 sub(d,["Ele observa, procura pistas","e confere cada explicação."],60,418,30)
 # Distinct archival-paper trail with crossed lines and evidence marks
 for j in range(4):
  xx=75+j*127;yy=666+j*30
  rect(d,[xx,yy,xx+270,yy+334],(255,250,238),8,(174,154,118),2)
  for k in range(6):
   y=yy+59+k*34;line(d,[(xx+22,y),(xx+222-12*k,y)],(150,145,132),3)
  d.ellipse([pt(xx+208),pt(yy+24),pt(xx+242),pt(yy+58)],outline=RED,width=pt(4))
 mascot(im,569,632,450)
def scene6(im):
 d=ImageDraw.Draw(im);brush(im,219,54,790,60)
 title(d,["E AGORA","É COM VOCÊ."],54,132,80)
 sub(d,["Qual mistério o Lúmino","deve investigar depois?"],59,433,32)
 for k in range(5):
  xx=70+k*185;yy=824+(k%2)*84
  d.ellipse([pt(xx),pt(yy),pt(xx+86),pt(yy+86)],fill=YELLOW,outline=(122,79,42),width=pt(4))
  d.text((pt(xx+28),pt(yy+1)),"?",font=F(68),fill=INK)
 mascot(im,534,603,450)
 rect(d,[54,1120,1024,1192],RED,8)
 d.text((pt(104),pt(1132)),"CONTE NOS COMENTÁRIOS.",font=F(41),fill=(255,250,240))
SCENES=[scene1,scene2,scene3,scene4,scene5,scene6]
info=[]
for i,do in enumerate(SCENES):
 im=bg(100+i)
 frame(ImageDraw.Draw(im),"")
 do(im);foot(im,i)
 master=OUT/f"master-{i+1:02}.png";im.save(master,optimize=True)
 reduced=im.resize((1080,1350),Image.Resampling.LANCZOS)
 final=OUT/f"{i+1:02}-a-origem-do-lumino.jpg";reduced.save(final,quality=94,subsampling=0,optimize=True)
 info.append({"file":final.name,"size":list(reduced.size),"sha256":hashlib.sha256(final.read_bytes()).hexdigest(),"bytes":final.stat().st_size})
preview=Image.new("RGB",(324*3,405*2),PAPER)
for i in range(6):
 small=Image.open(OUT/info[i]["file"]).resize((324,405),Image.Resampling.LANCZOS)
 preview.paste(small,((i%3)*324,(i//3)*405))
preview.save(OUT/"PREVIA-06-ARTES.png")
(OUT/"manifest.json").write_text(json.dumps({"date":"2026-11-05","theme":"A origem fictícia de Lúmino","preset":"TUE-MESTRE-01","canon_sha256":hashlib.sha256(LUM.read_bytes()).hexdigest(),"approved":False,"published":False,"pages":info},ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"ok":True,"slides":len(info),"out":str(OUT)},ensure_ascii=False))
