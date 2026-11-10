#!/usr/bin/env python3
"""Carrosséis TUE 10NOV: renderer editorial, fotos com crédito e Lúmino original.
NÃO publica, agenda ou aprova. Tudo gerado em staging para inspeção.
"""
import os,io,re,json,math,hashlib,random,urllib.parse,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'content/staging/2026-11-10/v3'
CANON=ROOT/'content/brand/lumino-original.png'; ASSET=OUT/'_cache'
BRAND_HASH='f905d801f013c2e253b8a17ae3bc1279b57022d1b805baa632f291a3b73e0c1b'
W,H=1080,1350; PAPER=(244,237,225);INK=(17,17,17);YELLOW=(255,214,0);RED=(213,14,21);CYAN=(0,207,246)
F_HEAVY='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'; F_TEXT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';F_BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PAGES={
'abs':[
('FÍSICA APLICADA','O FREIO ABS|SOLTA A RODA?','Na freada forte, ele evita travamentos e ajuda você a manter o controle.','Disc brakes.jpg','cover','FREAR SEM PERDER A DIREÇÃO'),
('O PROBLEMA','RODA TRAVADA.|DIREÇÃO PERDIDA.','Quando um pneu desliza, fica muito mais difícil orientar a trajetória do carro.','Ontheroad.jpg','wide','DESLIZAR NÃO É CONTROLAR'),
('SENSORES','O SISTEMA|PERCEBE O RISCO.','Sensores medem a rotação de cada roda e detectam o início de um travamento.','ABS-Sensor.jpg','detail','SENSOR DE ROTAÇÃO'),
('O CICLO','ALIVIA. MANTÉM.|FREIA DE NOVO.','O módulo hidráulico ajusta a pressão repetidamente para limitar o deslizamento.','ABS HCU April 2018.jpg','graph','PRESSÃO MODULADA'),
('ADERÊNCIA','FREAR TAMBÉM|É PODER VIRAR.','Rodas girando conservam mais capacidade de produzir a força lateral que orienta o carro.','Car brake test.jpg','wide','ATRITO ENTRE PNEU E PISTA'),
('A VERDADE','ABS NÃO CRIA|ADERÊNCIA EXTRA.','Gelo, água, pneus e velocidade ainda importam. No cascalho, a parada pode demorar mais.','Disc brake car.jpg','last','REDUZA A VELOCIDADE')],
'cinto':[
('FÍSICA APLICADA','O CARRO PARA.|SEU CORPO NÃO.','Por que o cinto e o airbag precisam trabalhar juntos numa colisão?','Crash-test-with-airbag-and-safty-belt.jpg','cover','A FÍSICA DA PROTEÇÃO'),
('A INÉRCIA','SEU CORPO TENDE|A CONTINUAR.','O veículo desacelera; o ocupante tende a manter o movimento até que uma força atue.','Crash test dummy with three-point seat belt (cropped).jpg','wide','PRIMEIRA LEI DE NEWTON'),
('O CINTO','SEGURA ONDE|É MAIS SEGURO.','O cinto distribui a força principalmente pelo tórax e pela pelve.','Hand reaches for seatbelt in a vehicle.jpg','detail','TÓRAX E PELVE'),
('O IMPULSO','MAIS TEMPO.|MENOS FORÇA MÉDIA.','Para a mesma mudança na quantidade de movimento, mais tempo reduz a força média.','Seat belt testing.jpg','equation','F MÉDIA = Δp / Δt'),
('O AIRBAG','ELE COMPLEMENTA.|NÃO SUBSTITUI.','O airbag amortece o contato enquanto o cinto mantém o ocupante na posição correta.','Abandoned car interior showing a deployed airbag and a worn steering wheel in a forgotten location.jpg','wide','CINTO + AIRBAG'),
('O RESULTADO','PROTEÇÃO É|TRABALHO EM EQUIPE.','Cinto, airbag e estrutura deformável atuam juntos. O cinto é indispensável.','Car seat belt.jpg','last','USE O CINTO SEMPRE')]}
def http(url):
 req=urllib.request.Request(url,headers={'User-Agent':'TUEEditorial/1.0 (automated science educational media; contact via github.com/gabrielslinhares12-sudo/instagram-skills)','Accept':'application/json,image/*,*/*'})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read()
def photo(name):
 ASSET.mkdir(parents=True,exist_ok=True)
 k=re.sub('[^a-z0-9]+','_',name.lower())
 p=ASSET/(k+'.jpg');mp=ASSET/(k+'.json')
 if p.exists() and mp.exists(): return Image.open(p).convert('RGB'),json.loads(mp.read_text())
 query=urllib.parse.urlencode({'action':'query','format':'json','prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':'1600','titles':'File:'+name})
 blob=json.loads(http('https://commons.wikimedia.org/w/api.php?'+query))
 info=next(iter(blob['query']['pages'].values()))['imageinfo'][0]
 raw=http(info.get('thumburl',info['url']))
 im=Image.open(io.BytesIO(raw)).convert('RGB')
 if min(im.size)<400:raise RuntimeError('Foto sem resolução suficiente: '+name)
 im.save(p,quality=92)
 meta={'name':name,'source':info['descriptionurl'],'license':re.sub('<[^>]+>','',info.get('extmetadata',{}).get('LicenseShortName',{}).get('value','')).strip(),'author':re.sub('<[^>]+>','',info.get('extmetadata',{}).get('Artist',{}).get('value',''))[:180], 'dimensions':list(im.size)}
 mp.write_text(json.dumps(meta,ensure_ascii=False))
 return im,meta
def font(f,size):return ImageFont.truetype(f,size)
def fit(d,s,width,start=97,end=39,file=F_HEAVY):
 for n in range(start,end-1,-1):
  f=font(file,n)
  if d.textbbox((0,0),s,font=f)[2]<=width:return f
 return font(file,end)
def lines(d,s,width=960,size=34):
 words=s.split();cur='';out=[];f=font(F_TEXT,size)
 for word in words:
  cand=(cur+' '+word).strip()
  if cur and d.textbbox((0,0),cand,font=f)[2]>width:out.append(cur);cur=word
  else:cur=cand
 if cur:out.append(cur)
 return out
def stroke(d,x,y,w,h,seed=2):
 r=random.Random(seed);xy=[(x-12,y+9)]
 for i in range(20):xy.append((x+w*i/19,y+r.randint(-8,9)))
 xy.append((x+w+12,y+h-5))
 for i in range(19,-1,-1):xy.append((x+w*i/19,y+h+r.randint(-6,14)))
 d.polygon(xy,fill=YELLOW)
 for k in range(4):
  yy=y+h+r.randint(0,11);d.line((x+r.randint(0,20),yy,x+w-r.randint(5,34),yy),fill=(255,186,0),width=r.randint(2,6))
def image_layer(im,source,mode):
 if mode=='detail':
  x,y,w,h=325,545,755,675
 else:x,y,w,h=0,575,1080,645
 p=ImageOps.fit(source,(w,h),method=Image.Resampling.LANCZOS,centering=(.5,.5))
 mask=Image.new('L',(w,h),0);m=ImageDraw.Draw(mask)
 if mode=='detail':m.polygon([(110,0),(w,0),(w,h),(0,h),(0,140)],fill=255)
 else:
  for z in range(h):
   m.line((0,z,w,z),fill=min(255,int(255*z/150)))
 im.paste(p,(x,y),mask)
def lumino(im,x,y,w):
 assert hashlib.sha256(CANON.read_bytes()).hexdigest()==BRAND_HASH,'ERRO: mascote não é o PNG original'
 src=Image.open(CANON).convert('RGBA')
 h=round(w*src.height/src.width); src=src.resize((w,h),Image.Resampling.LANCZOS)
 sh=Image.new('RGBA',im.size)
 sh.paste(src,(x+17,y+18),src.getchannel('A'))
 sh.putalpha(sh.getchannel('A').filter(ImageFilter.GaussianBlur(22)).point(lambda a:round(a*.42)))
 im.alpha_composite(sh);im.alpha_composite(src,(x,y))
def marker(d,msg,x,y):
 f=fit(d,msg,490,34,22,F_BOLD);bb=d.textbbox((x,y),msg,font=f)
 d.rounded_rectangle((x-20,y-12,bb[2]+17,bb[3]+18),radius=12,fill=PAPER)
 d.text((x,y),msg,font=f,fill=INK)
def extras(im,mode,index,key,label):
 d=ImageDraw.Draw(im)
 if mode=='cover':
  lumino(im,570,735,480)
  d=ImageDraw.Draw(im)
  d.rounded_rectangle((53,1110,630,1180),radius=12,fill=INK)
  d.text((76,1122),label,font=fit(d,label,540,32,21,F_BOLD),fill=YELLOW)
 elif mode=='wide':
  d.line((88,1080,530,1080),fill=RED,width=16)
  d.polygon([(530,1080),(494,1061),(494,1099)],fill=RED)
  marker(d,label,100,1141)
 elif mode=='detail':
  d.line([(92,764),(237,764),(404,861)],fill=RED,width=10)
  d.ellipse((392,850,415,873),fill=YELLOW,outline=INK,width=4)
  d.arc((55,728,320,992),start=215,end=330,fill=CYAN,width=10)
  d.text((78,1056),'01',font=font(F_HEAVY,98),fill=RED)
  d.text((92,1160),label,font=fit(d,label,800,34,23,F_BOLD),fill=INK)
 elif mode=='graph':
  layer=Image.new('RGBA',(900,205));a=ImageDraw.Draw(layer)
  a.rounded_rectangle((0,0,899,204),radius=18,fill=(244,237,225,240))
  a.line((48,154,846,154),fill=INK,width=4)
  a.line((48,27,48,154),fill=INK,width=4)
  pts=[(72,122),(162,36),(252,135),(342,51),(430,143),(530,32),(620,112),(722,60),(820,78)]
  a.line(pts,fill=RED,width=12,joint='curve')
  a.text((70,165),'ALIVIA  •  REAPLICA  •  ALIVIA',font=font(F_BOLD,22),fill=INK)
  im.alpha_composite(layer,(90,1005))
 elif mode=='equation':
  d.rounded_rectangle((84,990,1000,1190),radius=20,fill=INK)
  d.text((112,1010),'IMPULSO DA COLISÃO',font=font(F_BOLD,29),fill=YELLOW)
  d.text((112,1054),'F média = Δp / Δt',font=fit(d,'F média = Δp / Δt',840,72,50,F_HEAVY),fill=PAPER)
 elif mode=='last':
  lumino(im,674,783,365)
  d=ImageDraw.Draw(im)
  d.polygon([(0,1088),(670,1050),(670,1183),(0,1183)],fill=YELLOW)
  d.text((61,1100),label,font=fit(d,label,568,49,29,F_HEAVY),fill=INK)
def footer(im,index):
 d=ImageDraw.Draw(im)
 d.rectangle((0,1218,W,H),fill=PAPER);d.line((55,1335,1024,1335),fill=(182,176,164),width=2)
 if index==5:d.text((540,1290),'TEM UMA EXPLICAÇÃO.',anchor='mm',font=font(F_BOLD,28),fill=INK)
 else:
  for j in range(6):
   x=434+j*33;d.ellipse((x-8,1246,x+8,1262),fill=YELLOW if j==index else (175,173,170))
  d.line((664,1254,715,1254),fill=INK,width=4);d.polygon([(719,1254),(697,1241),(697,1267)],fill=INK)
  d.text((540,1292),'A R R A S T E   P A R A   O   L A D O   →',anchor='mm',font=font(F_TEXT,21),fill=INK)
def render(key,index,page,src):
 kick,head,body,pname,mode,marker_text=page
 im=Image.new('RGBA',(W,H),(*PAPER,255)); image_layer(im,src,mode)
 d=ImageDraw.Draw(im)
 d.line((57,55,1023,55),fill=INK,width=4)
 d.text((67,72),'TEM UMA EXPLICAÇÃO',font=font(F_BOLD,26),fill=INK)
 kf=fit(d,kick,330,33,20,F_HEAVY); width=d.textbbox((0,0),kick,font=kf)[2]
 d.text((1015-width,72),kick,font=kf,fill=RED)
 parts=head.split('|');yy=178
 for n,t in enumerate(parts):
  f=fit(d,t,962,99,50,F_HEAVY)
  if n==0:stroke(d,58,168,min(958,d.textbbox((0,0),t,font=f)[2]+35),90,seed=index+12)
  d.text((61,yy),t,font=f,fill=INK);yy+=112
 d.line((66,yy+6,612,yy+6),fill=RED,width=10)
 yy+=45
 for row in lines(d,body,960,35)[:3]:
  d.text((66,yy),row,font=font(F_TEXT,35),fill=INK);yy+=49
 extras(im,mode,index,key,marker_text)
 footer(im,index)
 return im.convert('RGB')
def main():
 assert CANON.exists(),'Arquivo original do Lúmino ausente'
 assert hashlib.sha256(CANON.read_bytes()).hexdigest()==BRAND_HASH,'SHA do Lúmino canônico inválido'
 OUT.mkdir(parents=True,exist_ok=True)
 meta={'preset_id':'TUE-MESTRE-01','date':'2026-11-10','target':'@temumaexplicacao','approved':False,'visual_reviewed':False,'published':False,'mascot_source':str(CANON.relative_to(ROOT)),'mascot_sha256':BRAND_HASH,'images':[],'sources':[]}
 for key,pages in PAGES.items():
  directory=OUT/key;directory.mkdir(parents=True,exist_ok=True)
  for i,p in enumerate(pages):
   src,credit=photo(p[3])
   im=render(key,i,p,src)
   path=directory/(f'{i+1:02d}.jpg')
   im.save(path,'JPEG',quality=94,subsampling=0,optimize=True)
   assert im.size==(1080,1350)
   meta['images'].append({'path':path.relative_to(ROOT).as_posix(),'post':key,'order':i+1,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':credit['source']})
   if credit not in meta['sources']:meta['sources'].append(credit)
   print('RENDERED',path.relative_to(ROOT),path.stat().st_size,flush=True)
  sheet=Image.new('RGB',(1080,900),PAPER)
  for i in range(6):
   im=Image.open(directory/(f'{i+1:02d}.jpg'))
   sheet.paste(im.resize((360,450),Image.Resampling.LANCZOS),((i%3)*360,(i//3)*450))
  sheet.save(OUT/('PREVIA-'+key.upper()+'.jpg'),quality=93)
 (OUT/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('TECHNICAL_OK 12 JPEG 1080x1350; review and owner approval pending. NEVER PUBLISHED')
if __name__=='__main__':main()
