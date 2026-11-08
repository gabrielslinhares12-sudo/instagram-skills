"""Shot-specific puppet staging: no generic repeat loops for the hardest actions.
Each rig is drawn from inked 2D parts with stable physical anchor positions.
"""
from PIL import ImageDraw
import math
import render_v33 as old
import environments_v35 as art
INK='#392f30'

def P(d,p,c,w=3):art.polygon(d,p,c,w)
def L(d,p,c,w=3):art.line(d,p,c,w)
def E(d,bb,c,w=2):art.el(d,bb,c,w=w)
def ease(x):return x*x*(3-2*x)
def clamp(x):return min(1,max(0,x))

def polyphemus_puppet(d,x,y,h,t,action='stand',progress=0):
 """One-eyed Greek shepherd giant. His hands, limbs and trunk share anchors."""
 progress=ease(clamp(progress))
 skin='#bba084'; deep='#927d6a'; black='#3a3332'; hair='#483a35'
 bob=3*math.sin(t*1.8)
 if action=='sway':bob=9*math.sin(3.2*t)
 if action=='fall':bob=10*progress
 y=y+bob
 # Contact shadow + stance, all dimensions relative to h.
 E(d,(x-.20*h,y-15,x+.20*h,y+8),'#514a43',w=0)
 hip=(x,y-.38*h)
 shoulders=(x-13*progress if action=='push' else x,y-.64*h)
 for side in (-1,1):
  hipx=x+side*.092*h
  knee=(hipx+side*(.028*h+.015*h*math.sin(t*1.6)),y-.17*h)
  foot=(hipx+side*.06*h,y-3)
  L(d,[(hipx,hip[1]),knee,foot],black,max(3,int(.095*h)))
  L(d,[(hipx,hip[1]),knee,foot],skin,max(3,int(.075*h)))
  E(d,(foot[0]-34,foot[1]-16,foot[0]+34,foot[1]+9),'#79634f',w=3)
 # Giant torso, large mass compared with Odysseus ~3:1.
 P(d,[(shoulders[0]-.18*h,shoulders[1]),(shoulders[0]+.19*h,shoulders[1]),(x+.19*h,y-.41*h),(x-.21*h,y-.4*h)],skin,5)
 E(d,(x-.115*h,y-.575*h,x+.115*h,y-.44*h),deep,w=0)
 P(d,[(x-.2*h,y-.44*h),(x+.2*h,y-.43*h),(x+.2*h,y-.26*h),(x-.2*h,y-.25*h)],'#6d6350',5)
 for k in range(8):L(d,[(x+(-.17+k*.05)*h,y-.4*h),(x+(-.16+k*.05)*h,y-.285*h)],'#a29375',3)
 # Neck and enormous head with nose and single eye.
 L(d,[(shoulders[0],shoulders[1]),(shoulders[0],y-.795*h)],black,int(h*.15))
 L(d,[(shoulders[0],shoulders[1]),(shoulders[0],y-.795*h)],skin,int(h*.11))
 hx=shoulders[0];hy=y-.84*h
 E(d,(hx-.16*h,hy-.16*h,hx+.16*h,hy+.15*h),skin,w=5)
 # Hair fringe, irregular handmade silhouette.
 P(d,[(hx-.16*h,hy-.05*h),(hx-.17*h,hy-.155*h),(hx-.075*h,hy-.21*h),
      (hx+.02*h,hy-.175*h),(hx+.095*h,hy-.212*h),(hx+.165*h,hy-.112*h),
      (hx+.13*h,hy-.02*h),(hx+.05*h,hy-.075*h)],hair,4)
 # A SINGLE centered eye (not duplicated).
 E(d,(hx-.063*h,hy-.067*h,hx+.063*h,hy+.035*h),'#efe2c2',w=3)
 E(d,(hx-.027*h,hy-.042*h,hx+.031*h,hy+.021*h),'#8b6350',w=2)
 E(d,(hx-.009*h,hy-.024*h,hx+.011*h,hy+.014*h),'#322d2b',w=1)
 L(d,[(hx-.08*h,hy-.075*h),(hx+.08*h,hy-.074*h)],hair,7)
 # Nose and beard follow head; don't float when moved.
 P(d,[(hx-.014*h,hy+.025*h),(hx+.057*h,hy+.078*h),(hx-.022*h,hy+.075*h)],deep,2)
 P(d,[(hx-.10*h,hy+.082*h),(hx+.10*h,hy+.080*h),(hx+.07*h,hy+.162*h),(hx,hy+.183*h),(hx-.08*h,hy+.15*h)],hair,3)
 for k in range(6):
  xx=hx+(-.08+k*.03)*h
  L(d,[(xx,hy+.10*h),(xx+math.sin(k*3)*5,hy+.15*h)],'#765f50',2)
 # Arm targets; pushing hand moves with stone's right edge, fixed contact.
 hands=[]
 for side in (-1,1):
  shoulder=(shoulders[0]+side*.168*h,shoulders[1]+.005*h)
  if action=='push':
   hand=(x-.12*h+20*progress,y-.44*h+(side*.09*h))
  elif action=='drink':
   hand=(x+side*.17*h,y-.84*h if side==1 else y-.49*h)
  elif action=='wail':
   hand=(x+side*.27*h,y-.79*h)
  elif action=='sleep':
   hand=(x+side*.25*h,y-.46*h)
  elif action=='fall':
   hand=(x+side*.29*h,y-.31*h)
  else:
   hand=(x+side*.28*h,y-.42*h)
  elbow=((shoulder[0]+hand[0])/2+side*.03*h,(shoulder[1]+hand[1])/2+.015*h)
  L(d,[shoulder,elbow,hand],black,max(3,int(.10*h)))
  L(d,[shoulder,elbow,hand],skin,max(3,int(.073*h)))
  E(d,(hand[0]-13,hand[1]-12,hand[0]+14,hand[1]+13),skin,w=3)
  hands.append(hand)
 return hands

def giant_boulder_push(d,canvas,t,p):
 # World coordinates fixed to the same cave entrance as adjacent shots.
 u=ease(p)
 # Giant is several human heights, within the same floor plane.
 hands=polyphemus_puppet(d,421,786,440,t,'push',p)
 cx=470-158*u
 old.boulder(d,cx,645,145)
 # Hand contact remains on surface through the entire push.
 for yhand in (594,677):
  contact=(cx+122,yhand-8)
  elbow=(443,yhand-9)
  L(d,[(453,563 if yhand==594 else 650),elbow,contact],INK,17)
  L(d,[(453,563 if yhand==594 else 650),elbow,contact],'#bba084',12)
  E(d,(contact[0]-11,contact[1]-10,contact[0]+11,contact[1]+10),'#bba084',w=3)
 # Specks of dust rise ONLY while the monolith moves; no constant particle cloud.
 for k in range(21):
  x=cx-100+(k*17)%200
  y=765-(k%5)*16-20*math.sin(math.pi*p)
  E(d,(x,y,x+2+(k%3),y+3),'#ac9780',w=0)
 old.man(d,98,786,151,t,'escape','odysseus')
 old.man(d,54,786,123,t,'escape','sailor')

def cyclops_drink(d,canvas,t,p):
 # Wine is handed off visibly between human and giant.
 u=ease(p)
 polyphemus_puppet(d,407,786,430,t,'drink',u)
 old.man(d,145+30*u,786,205,t,'offer','odysseus')
 old.cup(d,260+95*u,632-76*u,45)
 # Cup path travels from O's hand to giant's hand; no jump cut.
 L(d,[(205+28*u,616),(260+95*u,622-70*u)],'#b78664',8)

def cyclops_sleep(d,canvas,t,p):
 u=ease(p)
 polyphemus_puppet(d,405,790,420,t,'sway' if u<.6 else 'sleep',u)
 old.cup(d,370+25*u,469+120*u,46)
 old.man(d,105,790,161,t,'hold','odysseus')
 for x in (93,138):
  old.flame(d,x,732,t,.47)

def cyclops_stake(d,canvas,t,p):
 polyphemus_puppet(d,401,786,420,t,'wail',p)
 for k,x in enumerate((95,158,225)):
  old.man(d,x+16*p,788,156,t,'pull','odysseus' if k==0 else 'sailor')
 # One continuous wooden stake, held at back by all crew, aimed at one eye.
 tip=(388-18*p,443)
 L(d,[(122,620),(186,580),(255,525),tip],INK,21)
 L(d,[(122,620),(186,580),(255,525),tip],'#a17146',15)
 L(d,[(tip[0]-22,tip[1]+16),tip,(tip[0]-28,tip[1]+4)],'#e5ae70',6)

def circe_weave(d,canvas,t,p,night=False):
 # A stationary loom fully integrated into background while a hand moves
 # across its warp and Penelope unpicks the fabric in the following shot.
 x=198
 old.man(d,x,790,265,t,'weave','penelope')
 hx=280+12*math.sin(t*3)
 hy=597+math.sin(t*3)*14
 L(d,[(x+45,638),(242,622),(hx,hy)],INK,12)
 L(d,[(x+45,638),(242,622),(hx,hy)],'#c7a17a',8)
 E(d,(hx-7,hy-8,hx+8,hy+8),'#c7a17a',w=2)
 if night:
  # Threads gradually unravel but physical loom stays in place.
  for k in range(int(20*p)):
   y=686-k*5
   L(d,[(300,y),(413,y+3)],'#ac9980',2)
 else:
  for k in range(int(16*p)):
   y=690-k*7
   L(d,[(300,y),(413,y+3)],'#5c847e' if k%2 else '#bd7974',2)

def argos(d,canvas,t,p):
 """Old dog with a visible muzzle, ears, four paws and last head raise."""
 old.man(d,170,789,257,t,'kneel','beggar')
 x=380;y=789
 lift=26*math.sin(math.pi*min(1,p*1.27))
 E(d,(x-58,y-66,x+34,y-23),'#a78c6c',w=4)
 E(d,(x+17,y-64-lift,x+62,y-32-lift),'#bba383',w=3)
 P(d,[(x+20,y-57-lift),(x+4,y-90-lift),(x+32,y-75-lift)],'#7f6851',3)
 P(d,[(x+51,y-55-lift),(x+42,y-86-lift),(x+64,y-69-lift)],'#80634b',3)
 E(d,(x+55,y-47-lift,x+77,y-35-lift),'#d1bd9b',w=2)
 E(d,(x+64,y-43-lift,x+70,y-39-lift),INK,w=0)
 E(d,(x+38,y-53-lift,x+45,y-46-lift),INK,w=0)
 for ax in (x-42,x+5):
  L(d,[(ax,y-37),(ax+7,y-7)],'#745f4b',7)
  E(d,(ax-2,y-10,ax+15,y+2),'#9d8265',w=2)
 # Bent old tail moves only once in recognition, no indefinite wag.
 L(d,[(x-57,y-52),(x-85,y-60-lift*.3),(x-82,y-70-lift*.3)],'#8b7258',7)
 for k in range(4):
  xx=x+45+8*k
  L(d,[(xx,y-35-lift),(xx+4,y-20-lift)],'#c4b49b',1)

def scylla_six_heads(d,canvas,t,p):
 # Same strait geography; six separate animated serpent jaws and six losses.
 u=ease(p)
 old.ship(d,266,751,150,t,storm=True)
 for k in range(6):
  frac=k/6
  origin=(505+k*3,535+k*25)
  target=(85+k*71,596-37*u-(k%2)*14)
  head=(origin[0]+(target[0]-origin[0])*u,origin[1]+(target[1]-origin[1])*u)
  elbow=(450-25*u-(k%3)*9,490+k*29-(u*18))
  c='#50725e' if k%2 else '#45685a'
  L(d,[origin,elbow,head],INK,18)
  L(d,[origin,elbow,head],c,13)
  E(d,(head[0]-17,head[1]-12,head[0]+23,head[1]+14),c,w=3)
  E(d,(head[0]-8,head[1]-6,head[0]-1,head[1]+2),'#e7ce96',w=1)
  P(d,[(head[0]+6,head[1]+4),(head[0]+18,head[1]+21),(head[0]-1,head[1]+12)],'#d4d0a7',2)
  if u>.38:
   lift=(u-.38)*135
   xx=92+k*62
   yy=734-lift-(k%2)*11
   old.man(d,xx,yy,74,t,'fall','sailor')

def sirens_on_rocks(d,canvas,t,p):
 # The narration introduces sirens before it mentions the earwax and mast.
 for k,x in enumerate((105,273,449)):
  y=736+(k%2)*11
  old.man(d,x,y,222,t,'offer','siren')
  for j in range(4):
   ang=j*1.3+t*.65+k
   xx=x+42*math.cos(ang);yy=y-190+23*math.sin(ang)
   L(d,[(xx,yy),(xx+15*math.cos(ang),yy-17)],'#e6d3a9',2)
 # Distant incoming ship, never the main character in this introductory shot.
 old.ship(d,445-72*ease(p),781,65,t)

def sailors_block_ears(d,canvas,t,p):
 # Wax and visible ear contact as their ship approaches the sirens.
 old.ship(d,278,749,137,t)
 for k,x in enumerate((155,410)):
  old.man(d,x,744,145,t,'hold','sailor')
  E(d,(x-20,586,x-6,601),'#e8c78b',w=2)
  E(d,(x+6,583,x+19,599),'#e8c78b',w=2)
  L(d,[(x-16,599),(x-7,624)],'#c39b71',4)
  L(d,[(x+15,599),(x+6,621)],'#c39b71',4)

def odysseus_tied_to_mast(d,canvas,t,p):
 old.ship(d,268,752,150,t)
 old.man(d,270,747,170,t,'pull','odysseus')
 old.man(d,148,741,133,t,'pull','sailor')
 # Rope wraps around mast/torso in connected loops, tightened by the sailor.
 for k in range(4):
  y=636+20*k
  xx=272+12*math.sin(t*.4+k)
  L(d,[(xx-24,y),(xx+29,y),(xx+34,y+7)],'#dfba7f',4)
 L(d,[(161,610),(238,649),(272,659)],'#dfba7f',5)

def telemachus_prepares(d,canvas,t,p):
 # Following the actual narrated line about Telêmaco, not Penelope's loom.
 old.man(d,172+70*ease(p),789,255,t,'walk','telemachus')
 old.man(d,432,786,220,t,'hold','penelope')
 # A leather satchel he physically picks up for his search for his father.
 x=326-58*ease(p)
 P(d,[(x-26,692),(x+30,692),(x+35,754),(x-30,754)],'#976c50',3)
 L(d,[(x-26,700),(x+1,675),(x+30,700)],'#c7a078',5)
 L(d,[(x-22,731),(x+23,731)],'#c5a17b',3)

def affected(scene,beat):
 return (scene,beat) in {(4,2),(4,3),(4,4),(4,5),(8,1),(8,2),(8,3),(9,3),(13,2),(13,3),(14,3)}

def act(d,canvas,shot,t,p):
 scene=shot['scene'];beat=shot['beat']
 if (scene,beat)==(4,2):giant_boulder_push(d,canvas,t,p)
 elif (scene,beat)==(4,3):cyclops_drink(d,canvas,t,p)
 elif (scene,beat)==(4,4):cyclops_sleep(d,canvas,t,p)
 elif (scene,beat)==(4,5):cyclops_stake(d,canvas,t,p)
 elif (scene,beat)==(8,1):sirens_on_rocks(d,canvas,t,p)
 elif (scene,beat)==(8,2):sailors_block_ears(d,canvas,t,p)
 elif (scene,beat)==(8,3):odysseus_tied_to_mast(d,canvas,t,p)
 elif (scene,beat)==(9,3):scylla_six_heads(d,canvas,t,p)
 elif (scene,beat)==(13,2):circe_weave(d,canvas,t,p)
 elif (scene,beat)==(13,3):telemachus_prepares(d,canvas,t,p)
 elif (scene,beat)==(14,3):argos(d,canvas,t,p)
 else:raise ValueError((scene,beat))