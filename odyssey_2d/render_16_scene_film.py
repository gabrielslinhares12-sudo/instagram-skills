#!/usr/bin/env python3
"""ODISSEIA TUE: actual frame-by-frame 2D articulated animation.
No Blender, no static-image zoompan, no overlays of characters onto photos.
Scenes are painted every frame with multi-joint actors and physically staged props.
Private voice passed by --voice, never generated or downloaded by this program.
"""
import argparse, bisect, math, random, subprocess, sys, json, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TIMES=[0,9.65,22.68,34.59,54.42,67.625,80.36,91.9,103.095,115.845,127.415,138.82,152.045,167.09,182.38,200.655,220.56]
NAMES=['O ARCO DO REI','A QUEDA DE TROIA','CÍCONES E LÓTUS','POLIFEMO','ÉOLO E LESTRIGÕES','CIRCE','MUNDO DOS MORTOS','SEREIAS','CILA E CARÍBDIS','O ÚLTIMO NAVIO','CALIPSO','REGRESSO A ÍTACA','PALÁCIO TOMADO','PAI, FILHO E ARGOS','O ARCO E A VINGANÇA','O REGRESSO À FAMÍLIA']
LINES=[
'Um velho mendigo ergueu um arco diante de dezenas de guerreiros. Ninguém imaginava quem ele realmente era.',
'Era Odisseu, o estrategista que ajudara a destruir Troia com um gigantesco cavalo de madeira. Após dez anos de guerra, ele finalmente partiu para casa.',
'Mas a viagem começou com tragédias. Na terra dos cícones, perdeu homens em combate. Entre os lotófagos, precisou resgatar companheiros que haviam esquecido o próprio lar.',
'Em uma caverna, foram aprisionados por Polifemo, um gigante de um olho só. Odisseu o embriagou, disse chamar-se Ninguém e cegou o monstro. Seus homens escaparam escondidos sob ovelhas. Mas, ao revelar seu verdadeiro nome, Odisseu provocou a vingança de Poseidon.',
'Éolo lhe entregou um saco contendo os ventos perigosos. Seus homens o abriram por engano, afastando a frota de Ítaca. Depois, gigantes lestrigões destruíram quase todos os navios.',
'Na ilha de Circe, seus companheiros foram transformados em porcos. Protegido por Hermes, Odisseu resistiu à magia e conseguiu libertá-los. Mas, antes de continuar, recebeu uma ordem terrível.',
'Ele precisou descer aos limites do mundo dos mortos. Ali, Tirésias revelou os perigos restantes. Odisseu também encontrou a própria mãe, mas não conseguiu abraçá-la.',
'Depois vieram as sereias. Seu canto atraía navegantes para a morte. Odisseu pediu para ser amarrado ao mastro, enquanto seus homens remavam com os ouvidos protegidos.',
'Em um estreito mortal, precisou escolher entre Caríbdis, um redemoinho gigantesco, e Cila, um monstro de seis cabeças. O navio escapou, mas seis marinheiros morreram.',
'Famintos, seus homens desobedeceram à ordem de não tocar nos rebanhos sagrados do Sol. Zeus destruiu o último navio com um raio. Todos morreram, menos Odisseu.',
'Ele chegou à ilha de Calipso, que o manteve ali por sete anos e lhe ofereceu a imortalidade. Mas Odisseu só desejava voltar para Penélope e Telêmaco.',
'Depois de outra tempestade, foi acolhido pelos feácios. Ao conhecerem sua história, eles o levaram de navio até Ítaca. Vinte anos depois, ele estava em casa.',
'Mas seu palácio estava ocupado por pretendentes que queriam se casar com Penélope e tomar o reino. Ela resistia. Seu filho Telêmaco, agora adulto, também procurava notícias do pai.',
'Disfarçado de mendigo, Odisseu reencontrou Telêmaco e preparou a vingança. Seu velho cão Argos o reconheceu. Mais tarde, a ama Euricleia descobriu sua identidade pela cicatriz.',
'Penélope anunciou uma prova: quem armasse o arco de Odisseu e atravessasse doze machados com uma flecha poderia desposá-la. Todos falharam. O mendigo conseguiu. Era o rei. Com Telêmaco, derrotou os pretendentes.',
'Penélope ainda duvidou, até ele revelar o segredo da cama construída sobre uma oliveira viva. Ela o reconheceu. Odisseu reencontrou o pai, Laertes, e Atena encerrou a vingança. Depois de vinte anos, finalmente estava em casa. Tem uma explicação.'
]
PAL=[
('#1c2539','#4f352f','#c58b50'),('#202a45','#d57f46','#eab968'),('#2f4753','#90a17e','#c9ad7c'),('#121a1c','#48433b','#d0a36d'),('#242e46','#5681a6','#bfc4c5'),('#172e35','#44836e','#d7bd7b'),('#111e2e','#243a4a','#a7bbc0'),('#15364a','#2e7f94','#92bed0'),('#0d2036','#396d72','#a8d1d4'),('#111b2e','#303b58','#9dbad0'),('#17475b','#78b2aa','#d7cb8c'),('#192f4d','#c49c6f','#f1dbac'),('#332f39','#a16e4b','#e1b774'),('#343039','#8b684a','#e0c6a5'),('#33252d','#936044','#e9be79'),('#1d3654','#bc9165','#f1d6a4')]
INK='#152130';PALE='#efe0c6';GOLD='#e6b86c';WOOD='#6a4331';BRONZE='#ad7341';BLUE='#4a718e'

def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def lerp(a,b,x):return a+(b-a)*x
def sin(x):return math.sin(x)
def poly(draw,pts,fill,outline=INK,width=3):draw.polygon([(int(x),int(y)) for x,y in pts],fill=fill);draw.line([(int(x),int(y)) for x,y in pts+[pts[0]]],fill=outline,width=width,joint='curve')
def line(d,pts,fill,width=5):d.line([(int(x),int(y)) for x,y in pts],fill=fill,width=max(1,int(width)),joint='curve')
def ell(d,bb,fill,outline=INK,width=2):d.ellipse(tuple(map(int,bb)),fill=fill,outline=outline,width=max(1,width))
def rect(d,bb,fill,outline=None,width=2):d.rectangle(tuple(map(int,bb)),fill=fill,outline=outline,width=width)
def shift_col(c,k):
 c=c.lstrip('#');return tuple(max(0,min(255,int(int(c[i:i+2],16)*k))) for i in (0,2,4))
def mix_rgb(a,b,t):return tuple(int(lerp(a[i],b[i],t)) for i in range(3))

def background(W,H,scene,t,d):
 a,b,c=PAL[scene];a=shift_col(a,1);b=shift_col(b,1);c=shift_col(c,1)
 # Painted atmospheric gradient is recomputed on every animation frame.
 for y in range(H):
  p=y/H
  col=mix_rgb(a,b,ease(min(1,p*1.8))) if p<.58 else mix_rgb(b,c,ease((p-.58)/.42))
  d.line((0,y,W,y),fill=col)
 # soft subtle hand painted stratification; never photographs or slides
 horizon=int(H*.66)
 for k in range(6):
  p=k/6;Y=int(H*(.40+p*.25));off=math.sin(t*.12+k*.6)*2
  pts=[(-20,Y+40)]+[(int(i*W/8),int(Y+14*math.sin(i*.8+k*1.4)+off)) for i in range(9)]+[(W+20,Y+40)]
  d.polygon(pts,fill=(*mix_rgb(b,a,.22+p*.3),))
 if scene in (0,12,13,14,15):
  # Tall Mycenaean stone hall perspective, painted ancient timber roof.
  poly(d,[(0,0),(W,0),(W,int(H*.28)),(0,int(H*.16))],('#382f35'),width=3)
  for i in range(7):
   x=int(i*W/6)
   poly(d,[(x-7,0),(x+7,0),(int(W*.50+(x-W*.5)*.65)+6,int(H*.30)),(int(W*.5+(x-W*.5)*.65)-6,int(H*.30))],('#63452f'),width=1)
  poly(d,[(0,int(H*.65)),(W,int(H*.65)),(W,H),(0,H)],'#755848',width=3)
  for x in (45,W-45):
   poly(d,[(x-18,160),(x+18,160),(x+16,int(H*.78)),(x-16,int(H*.78))],'#7e6047',width=2)
   poly(d,[(x-25,160),(x+25,160),(x+40,180),(x-40,180)],'#a78660',width=2)
  for x in range(0,W,95):line(d,[(x,int(H*.66)),(int(W*.5+(x-W*.5)*1.6),H)],'#4d4544',2)
  for ty in (.74,.83,.94):line(d,[(0,H*ty),(W,H*ty)],'#4d4544',2)
  # amber torches with real flicker
  for x in (65,W-65):
   line(d,[(x,250),(x+7,345)],'#262a2b',8)
   q=math.sin(17*t+x)*6
   ell(d,(x-13,221-q,x+13,276+q),'#efac54',width=1)
   ell(d,(x-7,238-q,x+7,273),'#fff0a5',width=1)
 elif scene in (2,4,7,8,9,11):
  # Water undulates independently of any camera movement.
  poly(d,[(0,horizon),(W,horizon),(W,H),(0,H)],'#204962',width=1)
  for yy in range(horizon,H,26):
   for j in range(8):
    x=(j*93+int(t*(10+yy/H*8))+yy*3)%W
    line(d,[(x,yy+3*math.sin(t*1.4+j)),(x+40,yy-2*math.sin(t*.7+j))],('#82b1b3' if j%2 else '#4d8191'),2)
  poly(d,[(-10,horizon),(72,horizon-92),(146,horizon-42),(198,horizon-105),(254,horizon),(0,horizon+10)],'#59645a',width=2)
  poly(d,[(W-172,horizon),(W-90,horizon-125),(W,horizon-67),(W,horizon)],'#59645a',width=2)
 elif scene==1:
  # Walled city forecourt: road must be dry land, not the ocean.
  poly(d,[(0,H*.65),(W,H*.65),(W,H),(0,H)],'#8c7758',width=2)
  for col in range(12):
   x=col*W/11
   line(d,[(W*.5+(x-W*.5)*.35,H*.65),(x,H)],'#72614d',2)
  for y in (.71,.82,.93):line(d,[(0,H*y),(W,H*y)],'#776751',2)
  for j in range(7):
   x=W*(j/6);yy=H*.31+12*math.sin(j*1.5)
   poly(d,[(x-30,yy+105),(x-25,yy),(x+5,yy-20),(x+30,yy+105)],'#6c635b',width=2)
 elif scene==3:
  poly(d,[(0,H*.62),(W,H*.62),(W,H),(0,H)],'#34332f',width=2)
  poly(d,[(0,130),(W,145),(W,600),(W-105,560),(W-180,470),(W-300,500),(W-420,520),(0,470)],'#353e3c',width=3)
  poly(d,[(40,160),(W-45,160),(W-120,440),(W-50,570),(75,570),(118,422)],'#1b252b',width=5)
  for k in range(9):
   y=195+k*48;line(d,[(50,y),(130,y+14)],'#66716b',2)
 elif scene in (5,10):
  poly(d,[(0,H*.71),(W,H*.71),(W,H),(0,H)],'#547d68',width=2)
  for j in range(8):
   x=30+j*76;h=110+40*((j*13)%3)
   line(d,[(x,540),(x+15,540-h)],'#364d3e',14)
   ell(d,(x-26,530-h,x+52,550-h),'#426b56',width=2)
 elif scene==6:
  poly(d,[(0,580),(W,580),(W,H),(0,H)],'#172538',width=2)
  for j in range(18):
   x=(j*83+int(math.sin(t*.3+j)*10))%W; y=340+(j*73)%300
   ell(d,(x-13,y-3,x+14,y+3),'#536774',outline=None)
 return horizon

def actor(d,x,feet,h,role='odysseus',t=0,action='idle',alpha=1,face=1,scale=1):
 """Full 2D articulated character: legs bend at knees, arms at elbows, head pitch.
 Each joint and visible costume is re-drawn every frame. No imported photos.
 """
 h*=scale; x=float(x);feet=float(feet)
 roles={
 'odysseus':('#b88b64','#4b403e','#383039','#695149',True),
 'beggar':('#b88b64','#80765b','#383039','#5b5250',True),
 'penelope':('#c69b79','#e1c8a6','#5b4035','#c6b99f',False),
 'telemachus':('#ba9072','#66859c','#352b2b','#677382',True),
 'suitor':('#c7956e','#9d5544','#27232b','#603641',True),
 'suitor2':('#c69c7c','#77657b','#342d35','#5c4a62',True),
 'cyclops':('#998269','#77634f','#272c2d','#423b35',True),
 'circe':('#c9a582','#376756','#30373a','#917458',False),
 'calypso':('#d7b89a','#d3bfab','#654a3b','#dfd2b1',False),
 'athena':('#cba47b','#9c7239','#4a3b2d','#6c7890',False),
 'mother':('#bac3ce','#9fabb9','#a1aabb','#9ca9b8',False),
 'laertes':('#aa907d','#97866e','#d8d7cf','#6c6457',True),
 'eurycleia':('#b8a589','#b4aa95','#d4d1c4','#817b6e',False),
 'eumaeus':('#b99b7a','#80715b','#4e4037','#665746',True)
 }
 skin,tunic,hair,cloak,beard=roles.get(role,roles['odysseus'])
 # 2D physical perspective with foot contact. One weight-bearing knee each stride.
 bend=0; lean=.0
 if action in ('walk','run','escape','approach'):
  speed=5.7 if action=='run' else 3.2
  bend=math.sin(t*speed)*.15*h
  lean=.055*h if action=='run' else .01*h
 if action in ('push','pull','fight'):lean=.07*h
 if action=='kneel':feet+=.06*h;h*=.77
 if action in ('sleep','fall'):lean=.24*h
 sway=math.sin(t*1.8+ord(role[0]))*.009*h
 hip=(x+lean*.4,feet-h*.44+sway)
 shoulder=(x+lean,feet-h*.76+sway)
 head=(x+lean+math.sin(t*.7+face)*h*.009,feet-h*.93+sway)
 # cast shadow sticks to feet with body movement
 ell(d,(x-h*.21,feet-h*.012,x+h*.25,feet+h*.014),'#26333a',outline=None)
 # pair of legs: bent knee and planted support foot
 for side in (-1,1):
  hf=side*.11*h
  step=bend*(1 if side<0 else -1)
  knee=(hip[0]+hf*.90+step*.7,feet-h*.24+abs(step)*.11)
  shoe=(x+hf+step*1.3,feet-abs(step)*.22)
  if action in ('walk','run','escape'):shoe=(shoe[0],shoe[1]-max(0,step)*.35)
  line(d,[hip,knee,shoe],INK,max(3,int(h*.10)))
  line(d,[hip,knee,shoe],('#66594b' if role not in ('penelope','circe','calypso','mother') else tunic),max(2,int(h*.068)))
  ell(d,(shoe[0]-h*.059,shoe[1]-h*.022,shoe[0]+h*.058,shoe[1]+h*.026),'#5f4335',width=1)
 # cloak cloth shape dynamically ripples with body breathing / airflow
 cape_wave=math.sin(t*4.3)*h*.038
 if role not in ('circe','penelope','calypso','mother'):
  poly(d,[(shoulder[0]-.16*h,shoulder[1]+h*.06),(shoulder[0]+.19*h,shoulder[1]+h*.03),
          (x+.26*h+cape_wave,feet-.12*h),(x-.18*h-cape_wave,feet-.11*h)],cloak,width=2)
 # back arm, with elbow-based joint. hand reaches object in poses
 armspan=h*.26
 for side in (-1,1):
  top=(shoulder[0]+side*h*.20,shoulder[1]+h*.025)
  elbow=(top[0]+side*.055*h,top[1]+h*.25)
  hand=(elbow[0]+side*.03*h,elbow[1]+h*.20)
  if action in ('draw','aim','fight','push'):
   elbow=(top[0]+side*h*.15,top[1]+h*.09)
   hand=(elbow[0]+side*h*.23,elbow[1]-h*.055)
  elif action in ('hold','offer','drink','embrace','weave'):
   elbow=(top[0]+side*h*.11,top[1]+h*.12)
   hand=(x+side*h*.20,top[1]+h*.015)
  elif action=='pull':
   elbow=(top[0]+side*h*.13,top[1]+h*.13)
   hand=(x+side*h*.16,top[1]-h*.02)
  elif action in ('run','escape'):
   elbow=(top[0]-side*bend*.5,top[1]+h*.24)
   hand=(elbow[0]-side*bend*.3,elbow[1]+h*.13)
  line(d,[top,elbow,hand],INK,max(3,int(h*.094)))
  line(d,[top,elbow,hand],tunic,max(2,int(h*.061)))
  ell(d,(hand[0]-h*.045,hand[1]-h*.05,hand[0]+h*.045,hand[1]+h*.035),skin,width=1)
 # trapezoid tunic, belt, ornament. Distinct silhouette.
 poly(d,[(shoulder[0]-.20*h,shoulder[1]),(shoulder[0]+.20*h,shoulder[1]),
        (hip[0]+.17*h,hip[1]+.065*h),(hip[0]-.17*h,hip[1]+.065*h)],tunic,width=max(2,int(h*.013)))
 line(d,[(hip[0]-.18*h,hip[1]-.025*h),(hip[0]+.18*h,hip[1]-.025*h)],GOLD,max(2,int(h*.025)))
 # head with hair, beard, clear nose and eyes. Keyframed expression from pose.
 hx,hy=head
 ell(d,(hx-h*.125,hy-h*.15,hx+h*.126,hy+h*.114),skin,width=max(2,int(h*.011)))
 # hair clump and side hair, not helmet
 poly(d,[(hx-h*.12,hy-h*.022),(hx-h*.13,hy-h*.13),(hx-h*.055,hy-h*.164),
 (hx+h*.07,hy-h*.17),(hx+h*.14,hy-h*.1),(hx+h*.13,hy-h*.014),
 (hx+h*.05,hy-h*.105),(hx-h*.055,hy-h*.10)],hair,width=1)
 if beard and role not in ('telemachus',):
  poly(d,[(hx-h*.082,hy+h*.03),(hx-h*.065,hy+h*.11),(hx,hy+h*.164),
   (hx+h*.073,hy+h*.11),(hx+h*.075,hy+h*.035),(hx,hy+h*.090)],hair,width=1)
 # eye and eyebrow; facial direction signed
 for sid in (-1,1):
  ex=hx+sid*h*.047
  ell(d,(ex-h*.015,hy-h*.018,ex+h*.017,hy+h*.009),'#e8d4b4',width=1)
  ell(d,(ex+face*h*.006-h*.008,hy-h*.012,ex+face*h*.006+h*.008,hy+h*.008),INK,width=0)
  line(d,[(ex-h*.027,hy-h*.049),(ex+h*.024,hy-h*.045)],hair,max(1,int(h*.009)))
 line(d,[(hx+h*.008,hy-h*.01),(hx+h*.019*face,hy+h*.044),(hx-h*.004,hy+h*.044)],'#7a5241',max(1,int(h*.011)))
 if role=='cyclops':
  # Center eye mask covers human-sized eyes; single recognisable central eye.
  ell(d,(hx-h*.051,hy-h*.08,hx+h*.051,hy+h*.02),'#e8dbb9',width=2)
  ell(d,(hx-h*.022,hy-h*.064,hx+h*.022,hy-h*.008),'#684625',width=1)
  ell(d,(hx-h*.011,hy-h*.051,hx+h*.011,hy-h*.014),INK,width=0)
 if role=='odysseus':
  line(d,[(hx-h*.112,hy+h*.038),(hx-h*.086,hy+h*.012)],'#99664d',2)
 return {'head':head,'hip':hip,'shoulder':shoulder,'x':x,'feet':feet,'height':h}

def bow(d,x,y,r,t,draw_amt=1.0):
 # A bowed wooden stave and independently displaced drawn string. Hands grip it.
 k=math.sin(t*1.7)*.018*r
 pts=[(x,y-r*.47),(x-r*.16,y-r*.36),(x-r*.22,y),(x-r*.16,y+r*.36),(x,y+r*.48)]
 line(d,pts,INK,int(r*.055)+3);line(d,pts,WOOD,int(r*.035)+2)
 xx=x-r*.03+draw_amt*r*.20
 line(d,[(x,y-r*.47),(xx+k,y),(x,y+r*.48)],PALE,int(r*.014)+1)
 return xx,y

def horse(d,x,y,sc,t):
 # Full 2D equine model: head, neck, tail, four separately animated knees.
 S=sc;wave=math.sin(t*4.2)
 # wheels and carriage moving with same horse root
 poly(d,[(x-1.11*S,y-.18*S),(x+.95*S,y-.18*S),(x+.95*S,y),(x-1.11*S,y)],'#4f3028',width=3)
 for wx in (-.76,.72):
  cx=x+wx*S;cy=y+.16*S;r=.20*S
  ell(d,(cx-r,cy-r,cx+r,cy+r),'#7e5440',width=4)
  for j in range(6):
   th=t*3+j*math.pi/3
   line(d,[(cx,cy),(cx+r*.85*math.cos(th),cy+r*.85*math.sin(th))],GOLD,2)
 # four legs visible: each leg knee and hoof re-keyframed
 for sid in (-1,1):
  for k,xx in enumerate((-.65,.60)):
   joint=x+(xx+sid*.07)*S
   step=math.sin(t*3+sid+2*k)*.08*S
   line(d,[(joint,y-1.55*S),(joint+step,y-.85*S),(joint+step*.7,y-.10*S)],INK,int(.16*S)+3)
   line(d,[(joint,y-1.55*S),(joint+step,y-.85*S),(joint+step*.7,y-.10*S)],'#8b5840',int(.10*S)+1)
   rect(d,(joint-.14*S+step*.7,y-.14*S,joint+.16*S+step*.7,y+.04*S),'#442e2b',width=2)
 # tail
 line(d,[(x-1.09*S,y-1.90*S),(x-1.34*S,y-1.98*S),(x-1.38*S+wave*.06*S,y-1.36*S)],'#66412f',int(.13*S)+2)
 poly(d,[(x-1.1*S,y-2.17*S),(x+.77*S,y-2.13*S),(x+1.12*S,y-1.66*S),(x+.72*S,y-1.31*S),(x-.92*S,y-1.39*S)],'#9a6544',width=4)
 for j in range(5):line(d,[(x-.94*S,y-(1.44+j*.13)*S),(x+.67*S,y-(1.44+j*.13)*S)],'#bf8960',max(2,int(.03*S)))
 poly(d,[(x+.50*S,y-1.84*S),(x+.67*S,y-2.85*S),(x+.95*S,y-3.12*S),(x+1.16*S,y-2.79*S),(x+.96*S,y-1.83*S)],'#956343',width=4)
 ell(d,(x+.76*S,y-3.30*S,x+1.32*S,y-2.76*S),'#9e6b4c',width=4)
 poly(d,[(x+1.18*S,y-2.97*S),(x+1.58*S,y-2.82*S),(x+1.45*S,y-2.59*S),(x+1.16*S,y-2.63*S)],'#ac7954',width=3)
 for k in (0,1):
  ex=x+(.88+k*.20)*S
  poly(d,[(ex,y-3.22*S),(ex+.06*S,y-3.52*S),(ex+.22*S,y-3.27*S)],'#916045',width=3)
 ell(d,(x+1.06*S,y-3.05*S,x+1.13*S,y-2.99*S),INK,width=0)
 # Eight bronze rivets along the carved body
 for j in range(8):ell(d,(x+(-.85+.20*j)*S,y-1.89*S,x+(-.82+.20*j)*S,y-1.86*S),GOLD,width=0)

def ship(d,x,y,sc,t,flags=0):
 # rigid wooden hull with finite hull sides and a real sail that flaps
 s=sc;bob=math.sin(t*2)*4; y+=bob
 poly(d,[(x-1.45*s,y),(x+1.48*s,y),(x+1.20*s,y+.42*s),(x-.98*s,y+.42*s)],'#533f37',width=3)
 line(d,[(x-1.32*s,y+.20*s),(x+1.23*s,y+.20*s)],'#ab805a',int(max(2,.05*s)))
 line(d,[(x,y-.20*s),(x,y-2.48*s)],'#342f37',max(3,int(s*.06)))
 # Sail tangibly morphs with wind, not a still rotated background.
 f=math.sin(t*1.9)*.11*s
 poly(d,[(x+f,y-2.35*s),(x+1.01*s+f*.5,y-1.47*s),(x+.78*s,y-.39*s),(x,y-.42*s)],'#d6c5a0',width=3)
 line(d,[(x-1.33*s,y+.05*s),(x-1.06*s,y-.45*s)],'#ddd0b7',2)
 for j in range(4):
  oar_x=x+(-.8+j*.45)*s
  oy=y+.21*s;ang=math.sin(t*3+j*1.4)*.28*s
  line(d,[(oar_x,oy),(oar_x+ang,oy+.68*s)],'#ae8260',max(2,int(.038*s)))
 return y

def sheep(d,x,y,size,t):
 s=size;bounce=abs(math.sin(t*5))*s*.05;y-=bounce
 for k in range(6):
  ox=(-.7+k*.29)*s;line(d,[(x+ox,y-.45*s),(x+ox+s*.02,y)],'#786b58',int(.09*s)+1)
 for k in range(5):
  cx=x+(-.56+k*.25)*s
  ell(d,(cx-s*.28,y-1.24*s,cx+s*.28,y-.56*s),'#dfd7bc',width=2)
 ell(d,(x+.55*s,y-1.18*s,x+1.05*s,y-.66*s),'#84715e',width=2)
 ell(d,(x+.85*s,y-.95*s,x+.91*s,y-.89*s),INK,width=0)

def tree(d,x,y,s,t):
 line(d,[(x,y),(x,y-2.5*s),(x-s*.45,y-3.25*s)],'#594631',max(4,int(.23*s)))
 for z in range(10):
  a=z*2.399;xx=x+math.sin(a)*1.45*s+math.sin(t*.7+z)*s*.04;yy=y-(2.7+math.cos(a)*.45)*s
  ell(d,(xx-.61*s,yy-.4*s,xx+.61*s,yy+.42*s),'#477157',width=1)

def light_spark(d,x,y,r,t,col=GOLD):
 z=.5+.5*math.sin(t*3+r)
 line(d,[(x-r*z,y),(x+r*z,y)],col,2)
 line(d,[(x,y-r*z),(x,y+r*z)],col,2)

def scene_art(d,W,H,i,u,t):
 base=H*.80;hero_h=H*.29;mid=W*.50;action_phase=int(u*4)
 if i==0: # Geriatric beggar braces a drawn bow, suitors heckle
  p=actor(d,mid,base,hero_h,'beggar',t,'draw')
  actor(d,W*.18,base-H*.06,hero_h*.87,'suitor',t,'offer',scale=.86)
  actor(d,W*.85,base-H*.07,hero_h*.86,'suitor2',t,'hold',scale=.86)
  bx=mid+W*.15;bow(d,bx,base-hero_h*.52,hero_h*.65,t,lerp(0,.9,ease(u)))
  light_spark(d,bx,base-hero_h*.67,9,t)
 elif i==1:
  if u<.56:
   # Horse actually traverses gate, not a cut from exterior directly to interior.
   g=W*.5;gate_y=H*.54
   poly(d,[(0,H*.12),(W,H*.12),(W,H*.70),(0,H*.70)],'#a88a60',width=3)
   poly(d,[(W*.22,H*.29),(W*.78,H*.29),(W*.78,H*.80),(W*.22,H*.80)],'#192b39',width=3)
   line(d,[(W*.22,H*.29),(W*.22,H*.8)],'#a37e4f',17)
   line(d,[(W*.78,H*.29),(W*.78,H*.8)],'#a37e4f',17)
   S=W*.16; horse(d,W*(.40+.17*ease(u/.56)),H*.80,S,t)
   for ox in (-1,1):actor(d,W*(.2 if ox<0 else .77),H*.83,hero_h*.70,'suitor',t,'pull')
  elif u<.77:
   # warriors climb down inside their hollow wooden horse, reach for hinges
   horse(d,W*.49,H*.78,W*.145,t)
   actor(d,W*.33,H*.78,hero_h*.75,'odysseus',t,'escape')
   actor(d,W*.73,H*.78,hero_h*.75,'telemachus',t,'escape')
  else:
   ship(d,W*.44,H*.74,W*.17,t)
   for xx in (W*.14,W*.72):tree(d,xx,H*.70,W*.05,t)
 elif i==2:
  if u<.47:
   actor(d,W*(.66-.38*ease(u/.47)),base,hero_h,'odysseus',t,'run')
   actor(d,W*(.30-.29*ease(u/.47)),base,hero_h*.92,'suitor',t,'fight')
   for j in range(3):line(d,[(W*.70+j*13,H*.51),(W*.74+j*14,H*.46)],'#ebcf9f',3)
  else:
   for j in range(5):tree(d,60+j*100,H*.77,24,t)
   actor(d,W*.31,base,hero_h,'odysseus',t,'pull')
   actor(d,W*.68-.16*W*ease((u-.47)/.53),base,hero_h*.92,'telemachus',t,'walk')
   ell(d,(W*.66,H*.54,W*.70,H*.58),'#debb6f',width=1)
 elif i==3:
  if u<.27:
   # giant pushes boulder to block real cave opening
   S=hero_h*2.05
   actor(d,W*.71,base,S,'cyclops',t,'push')
   bx=W*(.98-.65*ease(u/.27))
   ell(d,(bx-W*.20,base-H*.35,bx+W*.20,base+H*.04),'#817b72',width=5)
   actor(d,W*.25,base,hero_h*.65,'odysseus',t,'escape')
  elif u<.53:
   actor(d,W*.72,base,hero_h*1.9,'cyclops',t,'drink')
   actor(d,W*.25,base,hero_h*.74,'odysseus',t,'offer')
   ell(d,(W*.50,H*.54,W*.57,H*.58),GOLD,width=2)
  elif u<.76:
   actor(d,W*.73,base+.06*H,hero_h*1.82,'cyclops',t,'fall')
   actor(d,W*.24,base,hero_h*.65,'odysseus',t,'pull')
   line(d,[(W*.19,H*.61),(W*.72,H*.41)],'#aa6a45',12)
  else:
   for j in range(3):sheep(d,(j+1)*W*.22+W*.06*ease((u-.76)/.24),base,W*.11,t+j)
   actor(d,W*.33,base,hero_h*.53,'odysseus',t,'escape')
 elif i==4:
  if u<.52:
   ship(d,W*.53,H*.72,W*.18,t)
   actor(d,W*.30,H*.71,hero_h*.65,'odysseus',t,'pull')
   for k in range(8):
    xx=W*.2+(k*47+int(t*80))%int(W*.70)
    line(d,[(xx,H*.44),(xx+25+math.sin(t*3+k)*15,H*.30)],'#cfe1dc',3)
  else:
   for x,y,s in [(W*.33,H*.70,W*.17),(W*.82,H*.72,W*.19)]:ship(d,x,y,s,t)
   for j in range(2):ell(d,(W*(.2+j*.55),H*.34,W*(.38+j*.55),H*.48),'#6b605a',width=2)
 elif i==5:
  for j in range(5):tree(d,60+j*125,H*.77,W*.07,t)
  actor(d,W*.73,base,hero_h,'circe',t,'offer')
  if u<.5:actor(d,W*.28,base,hero_h*.94,'telemachus',t,'drink')
  else:
   # Physical transformation: limbs grow shorter, body tilts and becomes pig.
   s=lerp(1,.36,ease((u-.5)/.5));actor(d,W*.28,base,hero_h,'telemachus',t,'fall',scale=s)
   ell(d,(W*.20,base-W*.10,W*.42,base-W*.02),'#cc977e',width=2)
  for j in range(5):light_spark(d,W*(.33+.06*j),H*(.30+.13*math.sin(j*2)),13,t+j,'#b8d8a2')
 elif i==6:
  actor(d,W*.31,base,hero_h,'odysseus',t,'embrace')
  hx=W*.66-.05*W*ease(u)
  # transparent ethereal mother drawn as cool washed vector character
  actor(d,hx,base,hero_h*.97,'mother',t,'embrace')
  for k in range(12):
   xx=(k*53+int(t*14))%W;yy=H*.30+k*25
   line(d,[(xx,yy),(xx+19,yy-4)],'#829bb6',2)
 elif i==7:
  ship(d,W*.50,H*.73,W*.20,t)
  actor(d,W*.50,H*.69,hero_h*.62,'odysseus',t,'pull')
  for j in (-1,1):
   line(d,[(W*.50,H*.48),(W*(.50+j*.13),H*.69)],'#e6e2cf',4)
   actor(d,W*(.20 if j==-1 else .84),base,hero_h*.75,'circe',t,'offer')
  for j in range(4):
   x=W*(.1+j*.26);y=H*.32+math.sin(t*2+j)*12
   light_spark(d,x,y,8,t+j,'#c6d8ea')
 elif i==8:
  ship(d,W*.50,H*.76,W*.16,t)
  # Scylla: six independently dancing necks from rock opening
  for j in range(6):
   x=W*.73+j*W*.038;theta=t*3+j*.7
   pts=[(x,H*.76),(x+math.sin(theta)*W*.09,H*.61),
        (x+math.sin(theta+1)*W*.13,H*.42)]
   line(d,pts,'#354f49',max(6,int(W*.035)))
   ell(d,(pts[-1][0]-11,pts[-1][1]-14,pts[-1][0]+12,pts[-1][1]+12),'#6f7b5d',width=2)
  for j in range(5):
   cx=W*.15+math.sin(t*1.6)*j*3;cy=H*.73+(j-2)*17;r=23+j*14
   d.arc((cx-r,cy-r,cx+r,cy+r),5,340,fill='#8bceda',width=4)
 elif i==9:
  if u<.45:
   for j in range(3):ell(d,(W*(.1+j*.27),H*.66,W*(.25+j*.27),H*.78),'#b6a58a',width=2)
   actor(d,W*.44,base,hero_h,'odysseus',t,'fight')
  else:
   ship(d,W*.43,H*.75,W*.21,t)
   z=math.sin(t*8)*W*.10
   # animated lightning zigzag for real action beat
   poly(d,[(W*.52,H*.08),(W*.47+z,H*.36),(W*.58,H*.37),(W*.49+z,H*.71),
           (W*.65,H*.42),(W*.56,H*.40)],'#f6dcaa',width=2)
 elif i==10:
  for j in range(5):tree(d,W*(.10+j*.23),H*.77,W*.052,t)
  actor(d,W*.35,base,hero_h,'odysseus',t,'kneel')
  actor(d,W*.70,base,hero_h,'calypso',t,'offer')
  if u>.74:ship(d,W*.66,H*.77,W*.12,t)
 elif i==11:
  if u<.38:
   actor(d,W*.27,base,hero_h,'odysseus',t,'kneel')
   actor(d,W*.70,base,hero_h*.90,'penelope',t,'offer')
  elif u<.70:
   ship(d,W*.50,H*.73,W*.21,t)
   ell(d,(W*.28,H*.30,W*.55,H*.39),'#c8cfe2',width=1)
  else:
   for j in range(4):tree(d,W*(.13+j*.24),H*.77,W*.045,t)
   actor(d,W*.50,base,hero_h,'odysseus',t,'kneel')
 elif i==12:
  if u<.36:
   for j in range(4):actor(d,W*(.15+j*.21),base,hero_h*.88,'suitor' if j%2 else 'suitor2',t,'drink')
   actor(d,W*.52,H*.70,hero_h*.73,'penelope',t,'idle')
  elif u<.75:
   actor(d,W*.40,base,hero_h,'penelope',t,'weave')
   for x in range(0,14):
    X=W*.54+x*11
    line(d,[(X,H*.57),(X,H*.84)],'#d8cba4',2)
   line(d,[(W*.51,H*.73),(W*.85,H*.73+math.sin(t*3)*4)],'#a7895c',4)
  else:
   actor(d,W*.38,base,hero_h,'telemachus',t,'walk')
   actor(d,W*.77,base,hero_h,'athena',t,'hold')
 elif i==13:
  if u<.37:
   x=W*.30+.15*W*ease(u/.37)
   actor(d,x,base,hero_h,'odysseus',t,'embrace')
   actor(d,W*.70-.10*W*ease(u/.37),base,hero_h*.89,'telemachus',t,'embrace')
  elif u<.65:
   actor(d,W*.45,base,hero_h,'beggar',t,'kneel')
   # Argos lifts head and lowers again; separate front/rear legs and tail
   cy=H*.80
   ell(d,(W*.67,cy-46,W*.89,cy),'#b29c82',width=3)
   yy=12*math.sin(ease((u-.37)/.28)*math.pi)
   ell(d,(W*.82,cy-67-yy,W*.94,cy-31-yy),'#6f5b50',width=2)
   line(d,[(W*.80,cy-25),(W*.79,cy+12)],'#5b4e41',5)
  else:
   actor(d,W*.44,base,hero_h,'beggar',t,'kneel')
   actor(d,W*.73,base,hero_h*.87,'eurycleia',t,'kneel')
   light_spark(d,W*.48,base-hero_h*.22,12,t,'#b6ad9c')
 elif i==14:
  if u<.42:
   actor(d,W*.33,base,hero_h,'beggar',t,'draw')
   bow(d,W*.47,H*.54,hero_h*.74,t,draw_amt=ease(u/.42))
   for j in range(12):
    X=W*.55+j*W*.034
    line(d,[(X,H*.64),(X,H*.71)],'#d4a475',3)
  elif u<.70:
   actor(d,W*.28,base,hero_h,'odysseus',t,'fight')
   actor(d,W*.68,base,hero_h*.89,'suitor',t,'fight')
   line(d,[(W*.27,H*.58),(W*.68+.07*W*ease((u-.42)/.28),H*.43)],GOLD,3)
  else:
   actor(d,W*.37,base,hero_h,'odysseus',t,'fight')
   actor(d,W*.71,base,hero_h*.94,'telemachus',t,'fight')
 elif i==15:
  if u<.43:
   actor(d,W*.25+.13*W*ease(u/.43),base,hero_h,'odysseus',t,'embrace')
   actor(d,W*.77-.17*W*ease(u/.43),base,hero_h,'penelope',t,'embrace')
   tree(d,W*.51,H*.80,W*.05,t)
   poly(d,[(W*.48,H*.75),(W*.66,H*.75),(W*.66,H*.83),(W*.48,H*.83)],'#b69a71',width=3)
  elif u<.67:
   actor(d,W*.41,base,hero_h,'odysseus',t,'embrace')
   actor(d,W*.70,base,hero_h*.83,'laertes',t,'embrace')
  else:
   for j,role in enumerate(('odysseus','penelope','telemachus')):
    actor(d,W*(.23+j*.27),base,hero_h*.94,role,t,'idle')
   for j in range(3):tree(d,W*(.07+j*.45),H*.77,W*.035,t)
   if u>.985:rect(d,(0,0,W,H),'#0c131c')

def subtitle(d,W,H,i,u,font):
 # Phrase-level estimate, anchored on measured silence windows.
 text=LINES[i].split()
 # Display a rolling *two-line* window and avoid unsupported word-level forced alignment claims.
 count=max(1,math.ceil(len(text)/10));j=min(count-1,int(u*count))
 start=j*10;part=' '.join(text[start:start+10])
 if not part:return
 words=part.split();line1='';line2=''
 for word in words:
  if len(line1)+len(word)+1<30:line1=(line1+' '+word).strip()
  else:line2=(line2+' '+word).strip()
 parts=[x for x in (line1,line2) if x]
 for k,string in enumerate(parts):
  yy=int(H*.87+k*29)
  box=d.textbbox((0,0),string,font=font,stroke_width=1)
  xx=(W-(box[2]-box[0]))//2
  d.text((xx,yy),string,font=font,fill='#fff3dc',stroke_width=2,stroke_fill='#14202e')

def render_frame(W,H,tt,font):
 i=min(15,max(0,bisect.bisect_right(TIMES,tt)-1))
 u=(tt-TIMES[i])/(TIMES[i+1]-TIMES[i]);t=tt
 img=Image.new('RGB',(W,H));d=ImageDraw.Draw(img)
 background(W,H,i,t,d)
 scene_art(d,W,H,i,u,t)
 subtitle(d,W,H,i,u,font)
 # No labels, scene numbers, stamps, prompts, or tool watermarks.
 return img

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default='/mnt/data/ODISSEIA_TUE_2D_QC_SEM_VOZ.mp4')
 ap.add_argument('--width',type=int,default=480);ap.add_argument('--height',type=int,default=854)
 ap.add_argument('--fps',type=int,default=18);ap.add_argument('--seconds',type=float,default=220.56)
 ap.add_argument('--start',type=float,default=0);ap.add_argument('--voice');ap.add_argument('--crf',type=int,default=23)
 args=ap.parse_args()
 assert args.width>200 and args.height>350 and args.fps>=10
 fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
 try:font=ImageFont.truetype(fontpath,max(12,int(args.width*.032)))
 except:font=ImageFont.load_default()
 out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
 video=out.with_suffix('.video-only.mp4') if args.voice else out
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24',
 '-video_size',f'{args.width}x{args.height}','-framerate',str(args.fps),'-i','-',
 '-c:v','libx264','-preset','veryfast','-crf',str(args.crf),'-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 n=int(round(args.seconds*args.fps))
 try:
  for k in range(n):
   frame=render_frame(args.width,args.height,args.start+k/args.fps,font)
   proc.stdin.write(frame.tobytes())
   if k and k%max(args.fps*10,1)==0:print(f'RENDER_2D_ARTICULATED {k}/{n}',flush=True)
 finally:
  proc.stdin.close()
 status=proc.wait();err=proc.stderr.read().decode(errors='replace')
 if status:raise RuntimeError('FFMPEG_RENDER_FAILED '+err[-500:])
 if args.voice:
  assert os.path.isfile(args.voice),'PRIVATE_RASALGETHI_ORIGINAL_WAV_MISSING'
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-i',args.voice,
   '-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',
   '-map','0:v:0','-map','1:a:0','-shortest','-movflags','+faststart',str(out)]
  subprocess.run(cmd,check=True);video.unlink()
 receipt={'name':'ODISSEIA_TUE_2D_FRAME_BY_FRAME','render_actual_unique_frames':n,'fps':args.fps,'width':args.width,'height':args.height,
  'seconds':args.seconds,'script_scenes':16,'narration_integrated':bool(args.voice),'original_audio_only':bool(args.voice),
  'native_4k60':False,'visual_owner_approved':False,'published':False,
  'warnings':['QC lower resolution; not 4K60 master','Phrase-level subtitle estimates; human word-level QC pending']}
 out.with_suffix('.qc.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
 print('ODISSEIA_2D_RENDER_COMPLETE_QC_ONLY',out,receipt,flush=True)
if __name__=='__main__':main()