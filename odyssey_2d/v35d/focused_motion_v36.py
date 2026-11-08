"""Focused V36 hand-keyed 2D performance corrections.

These override previously generic poses for the narrated story beats. The
character silhouettes, proportions, palette and original-Odysseus source
are supplied by render_v34 (imported as render_v33). No loops or zoompan.

Editorial warning: these are source animations; visual approval remains pending.
"""
import math
import render_v33 as old
import environments_v35 as art

INK="#392f30"
SKIN="#bb926d"
WOOD="#72523e"
GOLD="#cfaa6e"

def ease(x):
    p=max(0.0,min(1.0,x))
    return p*p*(3-2*p)

def L(d,pts,color=INK,w=4):art.line(d,pts,color,w)
def P(d,pts,color,w=3):art.polygon(d,pts,color,w)
def E(d,bb,color,w=2):art.el(d,bb,color,w=w)

def rope(d,x1,y1,x2,y2,width=4):
    L(d,[(x1,y1),(x2,y2)],"#d1ad80",width)
    for i in range(8):
        p=i/7
        xx=x1+(x2-x1)*p;yy=y1+(y2-y1)*p
        L(d,[(xx,yy),(xx+5,yy+3)],"#8b684d",1)

def axe(d,x,y):
    L(d,[(x,y),(x,y-121)],"#947557",5)
    E(d,(x-9,y-137,x+9,y-117),"#b5a06d",2)
    E(d,(x-5,y-134,x+5,y-123),"#4e4b43",1)

def cattle_disobedience(d,canvas,t,p):
    # Three distinct moments: crew approaches, touches sacrificial cattle,
    # and cuts the tether; all grounded on the SAME pasture as the real herd.
    u=ease(p)
    for k in range(3):
        x=118+k*138-52*u if k<2 else 452-60*u
        old.man(d,x,779,188,t,"walk" if u<.55 else "hold","sailor")
    if u>.30:
        xx=327; yy=675
        P(d,[(xx-12,yy),(xx+12,yy-8),(xx+27,yy+28),(xx-22,yy+30)],"#d4b889",2)
        rope(d,xx-20,yy-3,310+42*ease((u-.3)/.7),yy+15,3)
    if u>.72:
        for k in range(8):
            x=296+k*5;y=676+int(math.sin(t*5+k)*7)
            L(d,[(x,y),(x-4,y+13)],"#a89072",2)

def water_splash(d,x,y,p):
    for j in range(17):
        a=j*2.399
        radius=10+38*ease(p)
        xx=x+radius*math.cos(a);yy=y+radius*.5*math.sin(a)
        E(d,(xx-2,yy-2,xx+3,yy+3),"#cbdedb",0)

def eurycleia_scar(d,canvas,t,p):
    # A clear 3-beat action: kneel -> lift beggar's leg -> identify scar.
    u=ease(p); foot_x=245+36*u;foot_y=768-38*u
    old.man(d,208,787,239,t,"kneel","beggar")
    old.man(d,365-35*u,785,214,t,"kneel","eurycleia")
    E(d,(270,770,327,784),"#ad9779",0)
    # Small ceramic basin anchored in floor perspective.
    P(d,[(267,766),(327,768),(318,804),(275,803)],"#d7bca0",3)
    E(d,(269,757,325,775),"#aab5ac",3)
    # The lower leg is supported by her hand and lifts toward her face.
    L(d,[(232,736),(foot_x,foot_y)],"#aa8061",13)
    E(d,(foot_x-11,foot_y-7,foot_x+11,foot_y+5),"#ba9270",2)
    if u>.52:
        L(d,[(foot_x-6,foot_y-3),(foot_x+4,foot_y-12),(foot_x+12,foot_y-6)],"#75453d",3)
        E(d,(foot_x-3,foot_y-11,foot_x+4,foot_y-5),"#dc9c90",0)
        # One hand points to the visible mark (don't depict arbitrary sparkles).
        L(d,[(327,704),(foot_x+10,foot_y-10)],SKIN,9)

def bow_test(d,canvas,t,p):
    # Bow starts vertical, then bends under the hero's pull; an actual arrow
    # travels THROUGH all twelve aligned axe heads toward the far wall.
    u=ease(p)
    old.man(d,159,789,263,t,"aim","beggar")
    # Twelve axe heads with holes in correct depth. Do not multiply symbols.
    for k in range(12):
        xx=282+k*20
        axe(d,xx,760)
    # Bow stays in the original hero's hand throughout the draw.
    bx=242;by=607; bend=40*u
    L(d,[(bx+20,by-104),(bx-18-bend,by),(bx+20,by+104)],WOOD,8)
    L(d,[(bx+20,by-104),(bx-2-bend*.5,by),(bx+20,by+104)],"#d5b07d",3)
    rope(d,bx+20,by-104,bx+20-55*u,by,2)
    rope(d,bx+20-55*u,by,bx+20,by+104,2)
    # Releasing arrow follows the spoken "atravessou", not before.
    if u>.64:
        q=ease((u-.64)/.36)
        xx=225+(540-225)*q
        L(d,[(xx-84,639),(xx+5,639)],"#c2a16d",4)
        P(d,[(xx+8,639),(xx-2,630),(xx-2,648)],"#9e9587",2)
        for k in range(6):
            xp=285+int(q*30)-k*7
            L(d,[(xp,630),(xp+4,633)],"#dcc69e",1)
    else:
        L(d,[(225,639),(270,639)],"#c2a16d",4)

def olive_tree_bed(d,canvas,t,p):
    # The test of the rooted bed is the CAUSE of the recognition,
    # not two actors posing by a generic bed.
    u=ease(p)
    old.man(d,148,787,247,t,"offer","odysseus")
    old.man(d,444,787,234,t,"hold","penelope")
    # Stable trunk rooted beneath the mattress on the ORIGINAL bedroom set.
    L(d,[(195,805),(197,620),(170,528)],"#6d503c",20)
    # First Penelope points to the bed, then Odysseus gestures to its trunk.
    if u<.48:
        hx=407-25*ease(u/.48);hy=660
        L(d,[(434,677),(hx,hy)],SKIN,10)
    else:
        hx=176+39*ease((u-.48)/.52);hy=660
        L(d,[(158,684),(hx,hy)],SKIN,10)
        E(d,(190,574,202,590),"#d3b78b",1)
    for j in range(7):
        x=182+19*j
        L(d,[(x,745),(x+3,741)],"#a28b72",2)

def reunion(d,canvas,t,p):
    # Actions: Penelope hesitates, approaches, and embraces, with planted feet.
    u=ease(p)
    ax=168+107*u;bx=420-111*u
    pose="walk" if u<.67 else "embrace"
    old.man(d,ax,791,255,t,pose,"odysseus")
    old.man(d,bx,790,245,t,pose,"penelope")
    if u>.65:
        v=ease((u-.65)/.35)
        L(d,[(ax+35,632),(bx-30,641)],SKIN,max(3,int(5+7*v)))
    # Environmental response: curtain drifts slightly, bed stays fixed.
    line_y=410+4*math.sin(t*.6)
    L(d,[(58,318),(66,line_y),(83,497)],"#a98065",3)

def laertes_reunion(d,canvas,t,p):
    u=ease(p)
    old.man(d,153+110*u,787,257,t,"walk" if u<.58 else "embrace","odysseus")
    old.man(d,400-90*u,789,211,t,"walk" if u<.58 else "embrace","laertes")
    old.man(d,475,780,250,t,"offer","athena")
    if u>.75:
        E(d,(278,638,288,648),"#d3bb91",1)

ACTORS={(10,2):cattle_disobedience,(14,4):eurycleia_scar,
        (15,2):bow_test,(16,1):olive_tree_bed,(16,2):reunion,
        (16,3):laertes_reunion}

def affected(scene,beat):
    return (scene,beat) in ACTORS

def act(d,canvas,shot,t,p):
    ACTORS[shot["scene"],shot["beat"]](d,canvas,t,p)
