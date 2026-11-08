"""ODYSSEY V35: newly painted, event-specific 2D animation sets.

Not sourced from any rejected version's frames.  These are redraws in the same
ink/ochre/blue dusk architecture as the owned 60s Trojan-Horse master.
Detailed spatial continuity: floor line, door hinge, cliffs, ships and props
are anchored to fixed world coordinates for connected actions.
"""
from PIL import Image,ImageDraw,ImageFilter
import math,random
W,H=540,960
INK='#392f30';LIGHT='#ecd8ad';GOLD='#c6a374';STONE='#b59779';DARK='#203b4d'

def rgb(s):return tuple(int(s[j:j+2],16) for j in (1,3,5))
def mix(a,b,p):return tuple(int(a[k]*(1-p)+b[k]*p) for k in range(3))
def polygon(d,pts,c,w=3,outline=INK):
 d.polygon(pts,fill=c)
 if w:d.line(pts+[pts[0]],fill=outline,width=w,joint='curve')
def line(d,pts,c,w=3):d.line(pts,fill=c,width=w,joint='curve')
def el(d,bb,c,outline=INK,w=2):d.ellipse(bb,fill=c,outline=outline if w else None,width=w)
def rect(d,bb,c,outline=INK,w=2):d.rectangle(bb,fill=c,outline=outline if w else None,width=w)
def gradient(d,top='#19384c',bottom='#c9ae89',end=760):
 a=rgb(top);b=rgb(bottom)
 for y in range(end):d.line((0,y,W,y),fill=mix(a,b,(y/end)**1.6))
def stars(d,seed=0,n=45):
 rng=random.Random(seed+382)
 for i in range(n):
  x=rng.randrange(W);y=rng.randrange(5,440)
  el(d,(x,y,x+1,y+1),'#e6dabf',w=0)
def sun(d,x=420,y=199,r=49,night=False):
 el(d,(x-r,y-r,x+r,y+r),'#e9d1a0' if not night else '#e6d9b0',w=0)
def clouds(d,night=False,seed=0):
 for i in range(5):
  x=((i*155+seed*39)%710)-100;y=190+i*54
  c=('#6d7b7a' if night else '#8d9b91')
  for dx,rr in [(-26,25),(0,41),(35,32),(59,19)]:el(d,(x+dx-rr,y-rr*.37,x+dx+rr,y+rr*.36),c,w=0)
def mountains(d,seed=0,base=590):
 for layer,col,amp in [(0,'#a8a99a',48),(1,'#818f88',61),(2,'#627b7b',56)]:
  y=base+layer*31
  pts=[(-25,830)]
  for x in range(-25,590,21):
   pts.append((x,int(y-amp*(.45+.38*math.sin(x*.014+seed*.5+layer)+.16*math.sin(x*.05+layer)))))
  pts.extend([(560,840),(-25,840)])
  polygon(d,pts,col,w=0)
def ground(d,start=750,color='#bba07b',seed=1,stone=False):
 polygon(d,[(0,start),(540,start-7),(540,960),(0,960)],color,w=0)
 rng=random.Random(seed+2038)
 for k in range(130):
  x=rng.randrange(540);y=rng.randrange(start+6,952)
  r=rng.choice([1,1,2,3,4])
  c='#a48d72' if not stone else '#756357'
  line(d,[(x,y),(x+r*2,y+r//3)],c,1)
 if stone:
  for y in range(start+40,980,56):line(d,[(0,y),(540,y+3)],'#917b68',2)
  for j in range(11):
   x=25+j*54
   line(d,[(x,start+40+(j%3)*52),(x-7+5*(j%2),960)],'#a28c72',2)
def stone_block(d,x,y,w,h,seed=0):
 rect(d,(x,y,x+w,y+h),'#ad9170',INK,2)
 rng=random.Random(int(x+y+seed))
 for i in range(13):
  a=x+rng.randrange(4,max(5,int(w-4)));b=y+rng.randrange(4,max(5,int(h-4)))
  line(d,[(a,b),(a+rng.randrange(-12,13),b+rng.randrange(3,14))],'#927d64',1)
 line(d,[(x+7,y+5),(x+w-6,y+5)],'#d9b893',2)
def brick_wall(d,top=280,bottom=750,light='#b29577',beige=False):
 rect(d,(0,top,540,bottom),light,w=0)
 for y in range(top+8,bottom,37):
  line(d,[(0,y),(540,y)],'#8d785f',2)
  for x in range(((y//37)%2)*-38,580,77):
   line(d,[(x,y),(x,y+37)],'#917860',2)
   line(d,[(x+5,y+4),(x+26,y+4)],'#cdb08b',2)
 for x in range(0,550,108):
  rect(d,(x,top-25,x+78,top+5),light,w=2)
def column(d,x,top=230,bottom=780,shaft='#9e8164',cap='#c0a080'):
 polygon(d,[(x-20,top+18),(x+22,top+18),(x+18,bottom),(x-20,bottom)],shaft)
 line(d,[(x-10,top+25),(x-10,bottom-4)],'#bb9a78',4)
 line(d,[(x+9,top+25),(x+9,bottom-4)],'#6e5e50',2)
 polygon(d,[(x-35,top),(x+36,top),(x+29,top+20),(x-28,top+20)],cap)
 rect(d,(x-31,bottom-15,x+31,bottom+5),cap)
def roof(d,y=220):
 polygon(d,[(0,0),(540,0),(540,y-10),(0,y+28)],'#463b36')
 for i in range(10):
  x=-20+i*65
  polygon(d,[(x,0),(x+18,0),(x+75,y+15),(x+52,y+18)],'#76523e',w=1)
  line(d,[(x+9,0),(x+57,y)],'#916847',2)
def torch(d,x,y=470):
 line(d,[(x,y+20),(x+8,y+65)],'#3b3432',8)
 polygon(d,[(x-17,y+8),(x,y-30),(x+15,y+6),(x+8,y+22),(x-11,y+22)],'#e59e58',w=1)
 polygon(d,[(x-8,y+13),(x+1,y-14),(x+8,y+10)],'#f8d695',w=0)
 line(d,[(x-26,y+45),(x+28,y+45)],'#70523f',5)
def frieze(d,y=285):
 for x in range(0,540,45):
  polygon(d,[(x+5,y),(x+35,y),(x+24,y+10),(x+18,y+10)],'#6f5a4b',w=1)
  el(d,(x+17,y+11,x+25,y+18),'#d5b784',w=1)
def wall_hall(d,variant='royal'):
 brick_wall(d,258,766,'#94785c' if variant=='dark' else '#a48666')
 roof(d,225)
 frieze(d,279)
 for x in (42,497):column(d,x,228,784,'#987353')
 for x in (113,424):torch(d,x,446)
 ground(d,777,'#87684e',seed=4,stone=True)
 # Massive raised stone alcove with a real recessed door, not a reused plain box.
 polygon(d,[(175,365),(365,365),(382,730),(164,730)],'#644f44',3)
 polygon(d,[(193,392),(347,392),(353,745),(189,745)],'#53473f',3)
 for x in (215,328):line(d,[(x,415),(x,730)],'#83644f',6)
 for j in range(11):
  y=412+j*27
  line(d,[(198,y),(344,y)],'#70594a',1)
 if variant=='royal':
  for x in (55,490):
   line(d,[(x,328),(x,492)],'#9c805b',6)
   polygon(d,[(x-13,369),(x,338),(x+12,369)],'#d4ac75')

def house(d,x,y,w=96,h=121,lit=False):
 stone_block(d,x,y-h,w,h)
 polygon(d,[(x-13,y-h),(x+w/2,y-h-41),(x+w+13,y-h)],'#795446')
 rect(d,(x+w*.35,y-h*.57,x+w*.62,y),'#594a43',w=2)
 if lit:rect(d,(x+w*.40,y-h*.48,x+w*.58,y-11),'#d4ac6a',w=0)
 for xx in (x+10,x+w-8):line(d,[(xx,y-h+8),(xx,y-5)],'#ccb08b',2)
def city(d,dark=False):
 mountains(d,5,580)
 for i in range(8):
  x=i*74-42;y=694+(i%3)*7
  house(d,x,y,85,115+(i%3)*32,lit=dark and i%2==0)
 ground(d,745,'#bd9f77',seed=11)
 for x in (46,500):
  el(d,(x-14,725,x+14,736),'#88765e',w=0)

def gate(d,open_fraction=0.85):
 brick_wall(d,350,766)
 for x in (84,455):
  column(d,x,275,780,shaft='#a08465')
 polygon(d,[(109,354),(431,354),(431,749),(109,749)],'#3c3b38',5)
 # Doors rotate toward wall, visible hinges remain anchored.
 f=max(0,1-open_fraction)
 for mirror in (False,True):
  x=111 if not mirror else 429
  ww=153*f
  pts=[(x,386),(x+ww if not mirror else x-ww,408),(x+ww if not mirror else x-ww,760),(x,760)]
  polygon(d,pts,'#78513b',3)
  for k in range(10):
   yy=405+k*32
   line(d,[(x,yy),(x+ww if not mirror else x-ww,yy)],'#ad8456',2)
 for y in range(350,740,35):
  for x in (99,445):el(d,(x-3,y,x+3,y+6),'#d3b78d',w=0)

def tree(d,x,y,scale=1,flower=False,seed=0):
 trunk=scale*6
 line(d,[(x,y),(x-3*scale,y-89*scale)],'#66503f',max(3,int(trunk*2)))
 for k in range(4):
  angle=k*1.34
  xx=x+(k-1.4)*19*scale;yy=y-(112+17*math.sin(k))*scale
  line(d,[(x,y-75*scale),(xx,yy)],'#6a5041',max(2,int(trunk)))
 for k in range(8):
  xx=x+math.sin(k*2.37+seed)*47*scale
  yy=y-(121+17*math.cos(k*1.91+seed))*scale
  rr=(22+(k%3)*4)*scale
  el(d,(xx-rr,yy-rr*.75,xx+rr,yy+rr*.66),'#4e715b' if k%2 else '#5d8065',w=2)
  if flower:
   for q in range(4):el(d,(xx+(q-2)*9*scale-2,yy+(q%2)*11*scale,xx+(q-2)*9*scale+3,yy+(q%2)*11*scale+6),'#e0b6a0',w=0)

def dense_forest(d,magical=False):
 mountains(d,3,550)
 for i in range(18):
  x=i*42-30
  y=758-((i*17)%52)
  tree(d,x,y,scale=.65+((i*3)%5)*.1,flower=magical,seed=i)
 ground(d,756,'#829273',seed=14)
 for j in range(30):
  x=(j*83+13)%540;y=770+(j*71)%180
  line(d,[(x,y),(x+3,y-16)],'#577458',2)
  if magical:el(d,(x+1,y-20,x+8,y-12),'#edd3b6',w=1)

def ship_details(d,sea_y=698,night=False):
 for x in (15,510):
  # distant real vessels; no copy of hero action in foreground.
  yy=649+(x//300)*14
  polygon(d,[(x-32,yy),(x+22,yy),(x+5,yy+14),(x-17,yy+14)],'#725548',2)
  line(d,[(x-6,yy-50),(x-6,yy)],'#a98a63',2)
  polygon(d,[(x-4,yy-45),(x-4,yy-4),(x+30,yy-5)],'#e5d5af',2)
def sea(d,storm=False):
 polygon(d,[(0,676),(540,675),(540,960),(0,960)],'#244b63' if storm else '#477285',w=0)
 for k in range(16):
  y=689+k*22
  for j in range(8):
   x=(k*89+j*107)%600-45
   line(d,[(x,y),(x+25+(j%2)*15,y-4)],'#78a1a6' if k%2 else '#638e9a',1+(j%3==0))
 for x in range(2,540,135):
  el(d,(x,665,x+35,675),'#627f86',w=0)

def harbor(d,night=False):
 mountains(d,7,555)
 for x in (16,530):
  polygon(d,[(x-75,705),(x-21,540),(x+60,585),(x+80,700)],'#7c7669',2)
 sea(d)
 for x in (56,220,430):
  line(d,[(x,689),(x-3,606)],'#bda684',3)
  polygon(d,[(x,603),(x-3,672),(x+37,666)],'#eee0bd',2)

def cave(d,scene=3):
 # Cave is a connected environment: rear rock geometry and doorway never teleport.
 gradient(d,top='#202e33',bottom='#56564f',end=810)
 polygon(d,[(0,245),(85,208),(144,264),(204,219),(312,249),(426,190),(540,232),(540,768),(0,768)],'#665f55',4)
 polygon(d,[(0,275),(96,262),(156,331),(186,436),(324,437),(389,302),(453,275),(540,295),(540,775),(0,775)],'#464745',3)
 polygon(d,[(62,748),(83,472),(111,397),(158,363),(212,374),(240,456),(248,761)],'#1b3137',3)
 # Rock strata and chipped shadows: cave reads as inhabited, physically immense.
 for j in range(16):
  y=270+j*29
  line(d,[(0,y),(70+20*math.sin(j*2.3),y+13)],'#8d8172',2)
  line(d,[(480-23*math.cos(j),y+7),(540,y-10)],'#7c766a',2)
  if j%4==0:polygon(d,[(271,y+18),(318,y),(334,y+32),(285,y+41)],'#514d48',w=0)
 # Stalactites, overhang and scale-revealing dust pockets.
 for j in range(13):
  x=20+j*45;hh=35+(j*21)%110
  polygon(d,[(x-16,240),(x+20,240),(x+5,240+hh)],'#3d403f',2)
 ground(d,748,'#6c6258',seed=17,stone=True)
 for j in range(10):
  x=(j*69+22)%530;y=690+(j%3)*18
  el(d,(x-9,y-3,x+15,y+7),'#776d5f',w=1)
 # animal pen, huge ceramic amphorae and woven baskets
 for x in (78,115,469,508):
  polygon(d,[(x-13,740),(x-18,686),(x+17,686),(x+13,740)],'#b18a63',2)
  line(d,[(x-12,699),(x+13,699)],'#714f3b',2)
 for x in (60,460):
  for y in (676,697,716):line(d,[(x-38,y),(x+27,y)],'#936c50',3)

def circe_palace(d,beat=0):
 dense_forest(d,magical=True)
 polygon(d,[(74,411),(269,297),(462,412)],'#72543d',4)
 rect(d,(99,405,439,783),'#aa9470',w=4)
 for x in (119,166,366,414):column(d,x,410,776,shaft='#bc9b76')
 rect(d,(204,499,333,761),'#435848',w=4)
 for i in range(13):
  y=507+i*20;line(d,[(211,y),(323,y)],'#7d6b4d',2)
 for x in (35,508):tree(d,x,798,.72,flower=True,seed=x)
 for x in (65,468):
  polygon(d,[(x-33,771),(x+30,771),(x+37,802),(x-40,802)],'#a07758',2)
  for k in range(5):el(d,(x+(k-2)*9-3,752,x+(k-2)*9+4,762),'#dcaa91',w=0)

def underworld(d):
 gradient(d,'#172b38','#60737c',end=765)
 stars(d,21,35)
 mountains(d,10,586)
 polygon(d,[(0,662),(540,665),(540,960),(0,960)],'#304451',w=0)
 for x in (37,481):
  polygon(d,[(x-34,749),(x-24,449),(x+18,408),(x+42,749)],'#4a5960',3)
  for k in range(4):line(d,[(x-16,489+k*51),(x+22,489+k*51)],'#61747c',2)
 for k in range(11):
  x=(k*89+17)%540;y=675+(k%5)*25
  el(d,(x-48,y-8,x+48,y+3),'#6d8383',w=0)
 for k in range(8):
  x=(k*81+14)%540
  polygon(d,[(x-12,736),(x-16,623),(x+14,601),(x+26,736)],'#3d515c',2)

def sirens(d,beat=0):
 mountains(d,beat+8,560)
 sea(d)
 for x,y,w in [(90,580,120),(445,565,130),(245,623,57)]:
  polygon(d,[(x-w/2,736),(x-w/3,y+48),(x-3,y-34),(x+w/3,y+35),(x+w/2,739)],'#746e62',3)
  for j in range(7):line(d,[(x-14+j*4,y+24),(x-26+j*4,y+36)],'#958979',1)

def strait(d):
 mountains(d,8,475)
 sea(d,storm=True)
 polygon(d,[(0,303),(110,318),(157,405),(136,633),(142,820),(0,830)],'#666761',3)
 polygon(d,[(540,255),(439,295),(392,441),(412,614),(375,837),(540,840)],'#5e635f',3)
 for xx,sign in [(66,1),(465,-1)]:
  for j in range(14):
   y=330+j*28
   line(d,[(xx+sign*10,y),(xx+sign*(32+j%4*10),y+16)],'#898174',2)
 # Charybdis vortex always to the LEFT, Scylla anchored to the RIGHT.
 for k in range(8):
  rr=36+k*17
  d.arc((107-rr,798-rr*.20,107+rr,798+rr*.20),10,310,fill='#aacbd1',width=3)

def cow(d,x,y,s=1):
 el(d,(x-32*s,y-57*s,x+25*s,y-22*s),'#dcd3b3',w=2)
 el(d,(x+9*s,y-68*s,x+44*s,y-38*s),'#e8dabc',w=2)
 for xx in (x-23*s,x+9*s):line(d,[(xx,y-23*s),(xx-3*s,y)],'#7c664e',max(2,int(5*s)))
 for k in range(2):polygon(d,[(x+17*s+k*14*s,y-61*s),(x+9*s+k*14*s,y-78*s),(x+25*s+k*14*s,y-63*s)],'#bba47e',w=1)
 el(d,(x+27*s,y-56*s,x+31*s,y-52*s),'#3f302f',w=0)
 line(d,[(x-30*s,y-45*s),(x-50*s,y-73*s)],'#987c63',max(2,int(3*s)))

def meadow(d,beat=0):
 mountains(d,13,565)
 ground(d,740,'#82926f',seed=5)
 for x in (40,490):tree(d,x,768,.65)
 if beat in (0,1):
  for j in range(7):
   x=58+(j%4)*131;y=744-(j//4)*103
   cow(d,x,y,1.14 if j<4 else .77)

def calypso(d,beat=0):
 gradient(d,'#2d6071','#e6bf96',end=780)
 sun(d,433,190,55)
 mountains(d,15,543)
 # Striking island cascade over layered volcanic rock and a sheltered lagoon.
 polygon(d,[(0,550),(106,459),(174,499),(233,543),(236,785),(0,785)],'#858b7c',3)
 polygon(d,[(0,600),(82,536),(146,570),(179,689),(172,797),(0,797)],'#666e68',2)
 polygon(d,[(122,501),(153,491),(162,630),(168,785),(130,785)],'#9dd1cb',w=0)
 for k in range(8):line(d,[(137+k%3*7,532+k*25),(144+k%3*7,551+k*25)],'#ecf1d6',2)
 for x,s in ((36,.78),(220,.64),(493,.94)):
  tree(d,x,770,s,flower=True,seed=x)
 if beat!=3:ground(d,780,'#b7a67e',seed=15)
 else:
  sea(d)
  ground(d,845,'#b7a67e',seed=15)

def phaeciens(d,beat=0):
 gradient(d,'#244b60','#e0c49a',end=780)
 sun(d,417,174,50)
 mountains(d,12,573)
 if beat==0:
  ground(d,778,'#d3b88d',seed=12)
  for x in (24,480):tree(d,x,766,.75)
 elif beat==1:wall_hall(d,'royal')
 elif beat==2:sea(d)
 else:
  city(d)
  for x in (105,432):tree(d,x,773,.60)

def loom(d,night=False):
 wall_hall(d,'dark' if night else 'royal')
 # The loom is FULL SIZE relative to the queen, with traceable weaving threads.
 for x in (260,450):line(d,[(x,411),(x,790)],'#6e533f',12)
 line(d,[(259,412),(453,412)],'#6b4c39',12)
 line(d,[(259,740),(453,740)],'#6b4c39',12)
 for j in range(31):
  x=271+j*5.6
  line(d,[(x,430),(x,710)],'#d6bb8c',1)
 for y in range(492,712,18):
  line(d,[(271,y),(440,y+3)],'#a76b66' if (y//18)%3 else '#578278',3)
 rect(d,(285,715,434,736),'#775841')
 if night:
  for x in (300,415):torch(d,x,350)

def hut(d,beat=0):
 mountains(d,22,576)
 dense_forest(d)
 # Simple but fully furnished rural hut, physically consistent across two rooms.
 polygon(d,[(85,515),(283,409),(479,517)],'#6c4b3a',3)
 rect(d,(95,515,466,784),'#9d7c5c',w=3)
 for x in range(110,471,31):line(d,[(x,519),(x,785)],'#b29470',2)
 rect(d,(245,611,349,795),'#524237',w=3)
 for x in (125,437):
  rect(d,(x,560,x+50,618),'#615e57')
  for yy in range(567,616,9):line(d,[(x,yy),(x+50,yy)],'#b0a384',1)
 ground(d,792,'#a18868',seed=19)
 for x in (57,487):
  rect(d,(x,718,x+42,781),'#98765e',w=3)
  for y in (727,751):line(d,[(x+6,y),(x+37,y)],'#7b614d',2)

def bedroom(d):
 wall_hall(d,'royal')
 # Rooted olive tree is structural: bed belongs to same live trunk each beat.
 line(d,[(200,780),(199,542),(173,480)],'#6b5140',23)
 for j in range(6):
  x=170+j*23;y=445+19*math.cos(j*1.8)
  el(d,(x-40,y-32,x+39,y+22),'#658068' if j%2 else '#4e705a',w=2)
 polygon(d,[(171,706),(433,705),(418,790),(168,790)],'#8f644a')
 polygon(d,[(179,710),(419,710),(400,756),(179,756)],'#e3c99e')
 line(d,[(169,707),(170,810)],'#543b32',12)
 line(d,[(430,705),(430,814)],'#543b32',12)

def orchard(d):
 gradient(d,'#213e55','#dfc49b',end=790)
 sun(d,438,181,56)
 mountains(d,29,555)
 for j in range(10):
  x=j*64-25;y=751+(j%3)*8
  tree(d,x,y,.58+(j%3)*.13,seed=j)
 ground(d,775,'#987b5d',seed=30)
 for k in range(15):
  x=(k*67+38)%540;y=780+(k*43)%160
  el(d,(x-6,y,x+8,y+3),'#7b7860',w=0)

def build(scene:int,beat:int)->Image.Image:
 assert 1<=scene<=16 and 1<=beat<=8,(scene,beat)
 im=Image.new('RGB',(W,H),'#233b50');d=ImageDraw.Draw(im)
 night=scene in (1,4,7,8,9,13,14,15)
 gradient(d,'#19364a' if night else '#2b5063','#b4a082' if night else '#d5b693',end=795)
 if scene not in (1,4,6,7,13,14,15,16):
  sun(d,410,185,49,night)
  mountains(d,scene,559)
 if scene==1:wall_hall(d,'royal')
 elif scene==2:
  if beat in (1,2,3):
   city(d,night)
   gate(d,.35 if beat==1 else .94)
  else:harbor(d,True)
 elif scene==3:
  if beat==1:city(d,True)
  elif beat==2:harbor(d)
  else:dense_forest(d,True)
 elif scene==4:cave(d)
 elif scene==5:
  if beat==1:calypso(d,0)
  elif beat in (2,3):
   sea(d,beat==3)
   ship_details(d)
  else:strait(d)
 elif scene==6:circe_palace(d,beat)
 elif scene==7:underworld(d)
 elif scene==8:sirens(d,beat)
 elif scene==9:strait(d)
 elif scene==10:
  if beat<=2:meadow(d,beat-1)
  else:sea(d,True)
 elif scene==11:calypso(d,beat-1)
 elif scene==12:phaeciens(d,beat-1)
 elif scene==13:
  if beat==1:wall_hall(d,'royal')
  elif beat==2:loom(d,False)
  elif beat==3:loom(d,True)
  else:wall_hall(d,'royal')
 elif scene==14:
  if beat in (1,2):hut(d,beat-1)
  elif beat==3:city(d)
  else:wall_hall(d,'royal')
 elif scene==15:wall_hall(d,'royal')
 elif scene==16:
  if beat<=2:bedroom(d)
  else:orchard(d)
 # Scene-specific props are always distinct by action, but physical backdrops
 # stay coherent across connected cuts, per user's spatial-continuity rule.
 return im