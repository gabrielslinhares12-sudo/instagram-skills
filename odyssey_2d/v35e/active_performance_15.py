"""V35E: 15 low-motion shots rewritten as purposeful 2D performances.

No source movie footage or generic zoompan is used. Native original-Odysseus
puppet is supplied by render_v34 and restored in render_v35e. Not editorially
approved until original-film visual QC and voice sync are reviewed.
"""
import math
import render_v33 as old
import environments_v35 as art

INK='#392f30'; GOLD='#d1ad7a'; SKIN='#b69372'
def e(p):
 p=max(0.,min(1.,p))
 return p*p*(3-2*p)
def L(d,pts,c=INK,w=5):art.line(d,pts,c,w)
def P(d,pts,c,w=3):art.polygon(d,pts,c,w)
def E(d,bb,c,w=2):art.el(d,bb,c,w=w)
def body(d,x,y,h,t,pose,who):
 return old.man(d,x,y,h,t,pose,who)
def shift(a,b,p):return a+(b-a)*e(p)

def opening_lift(d,canvas,t,p):
 # The bow is lifted from a low resting pose and truly changes hands.
 u=e(p);x=250;y=787
 body(d,x-14*u,y,254,t,'offer' if u<.60 else 'aim','beggar')
 old.bow(d,shift(335,310,u),shift(710,585,u),185,t,.02+.20*u)
 L(d,[(x+10,660),(shift(333,309,u),shift(692,576,u))],SKIN,9)
 for k in range(3):
  px=38+k*42
  body(d,px,796,166,t,'hold','suitor')

def string_tension(d,canvas,t,p):
 u=e(p);x=211+24*u
 body(d,x,789,290,t,'draw','beggar')
 old.bow(d,298,580,225,t,.1+.79*u)
 # String and guiding wrist stretch together; no idle arrow loop.
 wrist=(277-30*u,580+5*u)
 L(d,[(298,475),wrist,(298,684)],GOLD,3)
 L(d,[(wrist[0],wrist[1]),(x+18,575)],SKIN,11)
 L(d,[(280-30*u,580),(365,580)],'#cda96b',4)

def look_reveal(d,canvas,t,p):
 u=e(p)
 # Face becomes visible as the hero turns toward a line of alarmed suitors.
 body(d,178+60*u,785,333,t,'offer' if u<.55 else 'aim','beggar')
 for i in range(3):
  dx=390+i*56+14*u
  body(d,dx,783,185,t,'hold','suitor' if i%2 else 'suitor2')
  E(d,(dx-6,565-12*u,dx+8,579-12*u),'#d6c6a5',2)
 for k in range(3):
  x=86+k*51
  L(d,[(x,707),(x+8+18*u,696-22*u)],'#9c7d5e',3)

def cave_arrival(d,canvas,t,p):
 u=e(p)
 # Small sailor figures approach a monolithic cave, cyclops physically dwarfs them.
 old.cyclops(d,401,784,505,t,'idle')
 for k in range(3):
  x=35+k*52+138*u
  body(d,x,786,131,t,'walk','sailor')
  L(d,[(x+8,731),(x+20,713)],'#be9b72',2)
 E(d,(249+20*u,788,293+25*u,799),'#615952',0)

def circe_pours(d,canvas,t,p):
 u=e(p)
 body(d,355-35*u,786,273,t,'offer','circe')
 body(d,142+44*u,790,228,t,'hold','sailor')
 cx=300-32*u;cy=595+95*u
 old.cup(d,cx,cy,37)
 # Drink runs visibly from vessel into cup and is actively offered.
 if .22<u<.79:
  for k in range(7):
   yy=628+((k*12+int(t*52))%88)
   E(d,(cx-5,yy,cx,yy+8),'#9e4c52',0)
 L(d,[(327,649),(cx+3,cy-9)],SKIN,8)

def prophet_speaks(d,canvas,t,p):
 u=e(p)
 body(d,410-88*u,791,284,t,'offer','tiresias')
 body(d,105+66*u,787,254,t,'hold','odysseus')
 # Tiresias points his staff from the underworld river toward the passage home.
 L(d,[(395-72*u,730),(316-110*u,538-48*u)],'#b9a986',8)
 P(d,[(315-110*u,538-48*u),(328-110*u,554-48*u),(303-110*u,558-48*u)],'#d8be89',3)
 for k in range(6):
  x=201+k*13+35*u
  E(d,(x,650+3*math.sin(t*4+k),x+6,656+3*math.sin(t*4+k)),'#889ea0',0)

def hungry_cattle(d,canvas,t,p):
 u=e(p)
 # Cattle are contextual large animals; sailors enter frame reaching for herd.
 for j in range(3):
  art.cow(d,150+j*133-42*u,770,1.3)
 for j in range(3):
  x=2+j*85+132*u
  body(d,x,794,180,t,'walk' if u<.72 else 'offer','sailor')
  if u>.67:
   L(d,[(x+18,661),(x+28+35*(u-.67),617)],SKIN,8)

def calypso_rescues(d,canvas,t,p):
 u=e(p)
 # Receding surf, exhausted sailor becomes upright through direct assistance.
 art.sea(d)
 for k in range(15):
  x=30+k*36;h=5+14*math.sin(k*1.3+t*2)
  L(d,[(x,811+h),(x+30,806+h)],'#b6d4d2',2)
 body(d,305-65*u,788,280,t,'kneel' if u<.6 else 'offer','calypso')
 if u<.55:
  body(d,153,810-30*u,190+25*u,t,'sleep','odysseus')
 else:
  body(d,153+45*e((u-.55)/.45),786,235,t,'offer','odysseus')
 L(d,[(260-55*u,670),(189+44*u,700-55*u)],SKIN,8)

def hermes_orders(d,canvas,t,p):
 u=e(p)
 body(d,153+107*u,785,259,t,'offer','hermes')
 body(d,425-35*u,785,266,t,'hold','calypso')
 # Winged emissary points a fixed message to Calypso.
 L(d,[(210+105*u,633),(275+90*u,589-44*u)],'#bfaa88',10)
 P(d,[(270+90*u,589-44*u),(280+90*u,571-44*u),(290+90*u,595-44*u)],'#d9c8a4',2)
 for k in range(3):
  P(d,[(120+107*u,607+k*10),(91+107*u,582+k*9),(110+107*u,614+k*9)],'#e2ddd0',2)

def nausicaa_finds(d,canvas,t,p):
 u=e(p)
 body(d,100+154*u,787,255,t,'walk' if u<.62 else 'kneel','nausicaa')
 body(d,332,808-30*u,192+22*u,t,'sleep' if u<.7 else 'hold','odysseus')
 # The hand carrying a water bowl approaches the exhausted traveler.
 cx=223+74*u;cy=649-15*u
 old.cup(d,cx,cy,32)
 L(d,[(170+145*u,673),(cx,cy)],SKIN,9)
 for k in range(6):
  x=345+27*k-17*u
  L(d,[(x,778),(x+17,777)],'#aed2cc',2)

def phaeacian_banquet(d,canvas,t,p):
 u=e(p)
 body(d,182+16*u,785,259,t,'offer','odysseus')
 body(d,389-33*u,789,236,t,'hold','suitor')
 # Consistent table foreground with food and active gesture.
 P(d,[(103,693),(451,692),(442,730),(107,732)],'#87604a',4)
 for k in range(7):
  E(d,(133+41*k,665+math.sin(k+t)*7,151+41*k,678+math.sin(k+t)*7),'#cea06f',2)
 L(d,[(229+15*u,615),(310+74*u,644)],SKIN,9)
 for k in range(4):
  xx=367+k*22
  E(d,(xx,622-20*u,xx+6,629-20*u),'#bd9d6f',0)

def failed_suitors(d,canvas,t,p):
 u=e(p)
 body(d,122+18*u,791,249,t,'pull' if u<.55 else 'fall','suitor')
 body(d,330-12*u,791,258,t,'hold','suitor2')
 bx=231;by=591
 old.bow(d,bx+30*u,by+10*u,194,t,.18+.2*u)
 L(d,[(198+14*u,615),(bx+30*u,568+10*u)],SKIN,7)
 if u>.55:
  old.bow(d,240+108*e((u-.55)/.45),677,160,t,.13)
  for k in range(7):
   xx=230+(k*9)%50
   E(d,(xx,758+5*k,xx+5,765+5*k),'#b79d74',0)

def actual_bow_arrow(d,canvas,t,p):
 u=e(p)
 # ACTION in five beats, with a deliberately large physical arc.
 body(d,180+40*u,790,274,t,'draw' if u<.68 else 'aim','beggar')
 for k in range(12):
  x=287+k*20
  L(d,[(x,757),(x,655)],'#966f4d',3)
  E(d,(x-8,635,x+8,655),'#d4b17b',3)
 old.bow(d,251+20*u,587,205,t,.20+.78*min(1,u/.64))
 if u<.67:
  x=257-39*e(u/.67)
  L(d,[(x,589),(369,589)],'#c4a277',5)
 else:
  fly=e((u-.67)/.33)
  xx=233+335*fly
  L(d,[(xx-59,639),(xx+7,639)],'#c9a776',5)
  P(d,[(xx+12,639),(xx+2,629),(xx+2,649)],'#bbb5a1',2)
  for k in range(12):
   hit=e(min(1,max(0,fly*13-k)))
   xx2=286+k*20
   if hit>.1:
    L(d,[(xx2,642),(xx2+12*hit,640-9*hit)],'#e0c9a4',2)

def bed_proof(d,canvas,t,p):
 u=e(p)
 # Heavy rooted trunk is an unmovable bedpost, not a generic loose furniture prop.
 body(d,123+80*u,786,263,t,'offer','odysseus')
 body(d,464-90*u,788,240,t,'hold','penelope')
 L(d,[(179,805),(197,558),(175,489)],'#624934',23)
 L(d,[(140+80*u,671),(192,587)],SKIN,10)
 for k in range(5):
  x=194+k*25
  L(d,[(x,721),(x+12*u,701-11*u)],'#a87e60',4)
 for j in range(7):
  E(d,(158+j*23,439+17*math.sin(t*.9+j),200+j*23,470+14*math.sin(t*.9+j)),'#507558',2)

def family_dawn(d,canvas,t,p):
 u=e(p)
 # Traveling through the olive grove is a consequence of the narrated reunion.
 for k,(role,x,y,h) in enumerate([
    ('odysseus',98,788,249),('penelope',282,791,225),
    ('telemachus',404,795,205),('laertes',503,785,204)]):
  body(d,x-15+45*u+7*math.sin(t*.7+k),y,h,t,'walk' if u<.68 else 'offer',role)
 # Sun rises; foreground olives do not disappear.
 art.sun(d,402,217-41*u,45)
 for k in range(9):
  x=18+k*65
  L(d,[(x,821),(x+5+12*u,813)],'#a59274',2)

ACT={
 (1,1):opening_lift, (1,3):string_tension,(1,4):look_reveal,
 (4,1):cave_arrival,(6,1):circe_pours,(7,2):prophet_speaks,
 (10,1):hungry_cattle,(11,1):calypso_rescues,(11,3):hermes_orders,
 (12,1):nausicaa_finds,(12,2):phaeacian_banquet,
 (15,1):failed_suitors,(15,2):actual_bow_arrow,
 (16,1):bed_proof,(16,4):family_dawn
}
def affected(scene,beat): return (scene,beat) in ACT
def act(d,canvas,shot,t,p): ACT[shot['scene'],shot['beat']](d,canvas,t,p)
