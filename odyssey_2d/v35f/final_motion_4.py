"""V35F -- final measured-motion corrections for four weak 2D story beats.

Four scenes have unique blocking and original-Troia puppet. Not suitable
for publication without art-director review against approved owner master.
"""
import math
import render_v33 as old
import environments_v35 as art

SKIN='#b99472';INK='#392f30';GOLD='#d5b07b'
def E(p):
 p=max(0.,min(1.,p));return p*p*(3-2*p)
def L(d,a,c=INK,w=4):art.line(d,a,c,w)
def P(d,a,c,w=3):art.polygon(d,a,c,w)
def C(d,a,c,w=2):art.el(d,a,c,w=w)
def m(d,x,y,h,t,pose,role):old.man(d,x,y,h,t,pose,role)
def between(a,b,p):return a+(b-a)*E(p)

def opening(d,canvas,t,p):
 # Hero walks into center foreground, takes/raises bow from resting position.
 u=E(p)
 m(d,170+114*u,786,255,t,'walk' if u<.53 else 'offer','beggar')
 m(d,78+19*u,787,215,t,'hold','suitor')
 m(d,442-27*u,787,216,t,'hold','suitor2')
 x=333-23*u;y=728-160*u
 old.bow(d,x,y,165+40*u,t,.08+.55*u)
 L(d,[(223+100*u,666-8*u),(x,y-16)],SKIN,11)
 # Physically fixed bow grip travels with the actor, no teleport.
 C(d,(x-9,y-18,x+8,y-2),'#d1aa79',3)

def tell(d,canvas,t,p):
 # Phaeacian court: walking narrating hero turns to table then uses both hands.
 u=E(p)
 x=161+99*u
 m(d,x,788,258,t,'walk' if u<.35 else 'offer','odysseus')
 m(d,395-28*u,787,239,t,'offer' if u>.5 else 'hold','suitor')
 m(d,490-32*u,788,215,t,'hold','sailor')
 P(d,[(88,694),(458,692),(438,736),(102,740)],'#856147',4)
 for k in range(6):
  xx=125+k*56
  C(d,(xx-10,665+7*math.sin(t*.7+k),xx+16,685+7*math.sin(t*.7+k)),'#ccad7c',2)
 # The story's narration is enacted by an unfolding scroll/historical route:
 q=E(max(0,(u-.25)/.75));width=15+183*q
 P(d,[(x+14,615),(x+14+width,615),(x+14+width,670),(x+14,670)],'#dbcba7',3)
 for j in range(int(1+6*q)):
  xx=x+21+j*27
  L(d,[(xx,636),(xx+19,635)],'#ad8969',2)
 L(d,[(x+3,650),(x+14+width*.85,640)],SKIN,10)

def suitors_fail(d,canvas,t,p):
 # A failed suitor genuinely pulls, loses balance and falls, dropping the bow.
 u=E(p)
 x=192-55*E(max(0,(u-.5)*2))
 y=789+11*math.sin(t*2)
 pose='pull' if u<.45 else 'fall'
 m(d,x,y,269,t,pose,'suitor')
 m(d,388+40*u,788,242,t,'offer','suitor2')
 mx=260+125*E(max(0,(u-.38)/.62))
 my=572+172*E(max(0,(u-.38)/.62))
 old.bow(d,mx,my,192-15*u,t,.1+.11*u)
 L(d,[(x+20,652),(mx-12,my-3)],SKIN,8)
 for k in range(10):
  xx=280+k*12
  C(d,(xx-7,748+10*u,xx+5,757+10*u),'#ba9472',0)

def shoot(d,canvas,t,p):
 # Prepare (0-.25), draw (.25-.52), release (.52-.62), shoot (.62-1).
 # This actually crosses 12 axe holes with the same arrow in continuous space.
 u=E(p)
 x=136+106*E(min(1,u/.63))
 m(d,x,787,283,t,'walk' if u<.27 else 'draw' if u<.63 else 'aim','beggar')
 for k in range(12):
  xx=285+20*k
  L(d,[(xx,784),(xx,658)],'#926d4a',3)
  C(d,(xx-10,629,xx+10,653),'#cfa46a',3)
 bowx=248+36*u;bowy=577+41*E(min(1,u/.52))
 old.bow(d,bowx,bowy,195,t,.1+.85*E(min(1,u/.57)))
 if u<.62:
  wristx=257-71*E(u/.62)
  L(d,[(wristx,620),(bowx+65,620)],GOLD,5)
  L(d,[(x+17,656),(wristx,620)],SKIN,9)
  L(d,[(wristx,517),(wristx,722)],'#e4ce9d',3)
 else:
  q=E((u-.62)/.38)
  ax=248+329*q
  L(d,[(ax-72,647),(ax+12,647)],GOLD,5)
  P(d,[(ax+14,647),(ax+3,637),(ax+3,657)],'#aa9c86',2)
  # Holes respond successively with a small nudge as the arrow passes.
  for k in range(12):
   wx=285+20*k
   hit=E(max(0,min(1,(q-k/12)*12)))
   if hit>0:
    L(d,[(wx,634),(wx+10*hit,618-10*hit)],'#ddc8a2',2)

ACT={(1,1):opening,(12,2):tell,(15,1):suitors_fail,(15,2):shoot}
def affected(scene,beat):return (scene,beat) in ACT
def act(d,canvas,shot,t,p):return ACT[shot['scene'],shot['beat']](d,canvas,t,p)
