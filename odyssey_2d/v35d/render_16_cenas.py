#!/usr/bin/env python3
"""A ODISSEIA — THE RETURN TO ITHACA. TUE original-visual 2D follow-on.
True keyframe-animated, independently posed illustrated objects; 16 scenes,
64 editorial shots, original OWNED 60-second Trojan Horse art cutouts. New cast
is developed in the exact chocolate-line/Bronze Age/flat-cell aesthetic.
Owner-supplied Rasalgethi 220.56s voice. This is a QC film, not auto-publish.
"""
import os,sys,math,bisect,random,subprocess,json,argparse,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parent))
import canon_rig as canon
import base_tue as base

W,H=540,960
DARK='#372e2c'; INK='#312931'; WOOD='#9d7151'; WOOD_D='#66432e'
SAND='#ceaf83'; BRONZE='#b58b57'; GOLD='#e3be78'; PALE='#f6e6c0'; SKIN='#c99367'
DEEPBLUE='#213e50'; WATER='#3f6a78'; SAND_L='#e0bf91'; SHADOW='#253f48'
MONO=Image.open(str(Path(__file__).resolve().parent/'assets'/'CAVALO_TROIA_ORIGINAL_RGBA.png')).convert('RGBA')
T=base.TIMES; NAMES=base.NAMES; LINES=base.LINES
CANVAS=None;SCALE=1.0
FONT_DIR='/usr/share/fonts/truetype/dejavu'
# 4 visually distinct directed shots per voice-anchored script scene.
SETS=[
 ['hall','hall','hall','hall'],
 ['troy','troy','troy_night','sea'],
 ['coast','sea','lotus','coast'],
 ['cave','cave','cave','cave_exit'],
 ['wind','sea','storm','harbor'],
 ['island','circe','island','circe'],
 ['underworld','underworld','underworld','underworld'],
 ['sea','sea','sirens','sea'],
 ['strait','strait','strait','sea'],
 ['island','island','storm','sea'],
 ['island','island','island','sea'],
 ['shore','hall','sea','ithaca'],
 ['hall','weave','weave','courtyard'],
 ['hut','courtyard','hall','hut'],
 ['hall','hall','hall','hall'],
 ['bed','bed','orchard','ithaca'],
]

def mix(a,b,t):return tuple(round((1-t)*a[k]+t*b[k]) for k in range(3))
def clamp(x,a=0,b=1):return max(a,min(b,x))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def lp(a,b,p):return a+(b-a)*p
def cv(c):return tuple(int(c[k:k+2],16) for k in (1,3,5))
def poly(d,pts,color,width=3):
    d.polygon([(round(x),round(y)) for x,y in pts],fill=color)
    d.line([(round(x),round(y)) for x,y in pts]+[tuple(round(v) for v in pts[0])],fill=DARK,width=width,joint='curve')
def ellipse(d,bb,color,width=2,outline=DARK):
    d.ellipse(tuple(round(v) for v in bb),fill=color,outline=outline,width=max(1,int(width)))
def line(d,pts,color,width=3):
    d.line([(round(x),round(y)) for x,y in pts],fill=color,width=max(1,int(width)),joint='curve')
def rect(d,bb,color,width=2):
    d.rectangle(tuple(round(v) for v in bb),fill=color,outline=DARK,width=width)
def actor(d,x,y,h,role='odysseus',t=0,action='idle',scale=1):
    return canon.actor(d,x,y,h,role,t,action,scale=scale)

def composite_sprite(sprite, x, y, width):
    global CANVAS,SCALE
    sw=round(width*SCALE);sh=round(sprite.height*sprite.width**-1*sw)
    if sw<1 or sh<1:return
    scaled=sprite.resize((sw,sh),Image.Resampling.BILINEAR)
    dx=round((x-width/2)*SCALE);dy=round((y-sh/SCALE)*SCALE)
    CANVAS.paste(scaled,(dx,dy),scaled)

def illustrated_sky(d,setting,t):
    # Original Trojan reel palette, same giant round sand-coloured moon/sun.
    night=setting in ('troy_night','underworld','storm','cave','cave_exit')
    top=cv('#1b3b51' if not night else '#132d40')
    middle=cv('#506c73' if not night else '#364858')
    bottom=cv('#c8ad83' if not night else '#777f80')
    # geometric gradient same cinematographic picture-book world as Trojan Horse.
    for yy in range(H):
        z=yy/H
        col=mix(top,middle,ease(z/.58)) if z<.58 else mix(middle,bottom,ease((z-.58)/.42))
        d.line((0,yy,W,yy),fill=col)
    if setting not in ('hall','bed','weave','hut','circe','cave','underworld'):
        sunx=int(W*.79);suny=int(H*.20)
        rr=58 if not night else 43
        ellipse(d,(sunx-rr,suny-rr,sunx+rr,suny+rr),'#f0d59c',0,None)
    if night:
        for q in range(34):
            x=(q*67+19)%W;y=(q*97+30)%460
            ellipse(d,(x,y,x+1,y+1),'#e5d7c3',1,None)
    # 3 levels of fixed illustrated hill silhouettes and moving subtleties.
    if setting not in ('hall','bed','weave','hut','circe','cave','underworld'):
        for k,(y0,col) in enumerate([(530,'#9ca395'),(574,'#7a8f88'),(626,'#4f6870')]):
            shift=2*math.sin(t*.17+k)
            pts=[(-30,H)]+[(int(x),int(y0+shift+35*math.sin(x/81+k*1.7))) for x in range(-30,W+35,35)]+[(W+20,H)]
            d.polygon(pts,fill=col)

def palace(d,setting,t):
    # 100% painted 2D period-appropriate hall with wood beams and side pillars.
    base='#766255' if setting!='bed' else '#9f7d68'
    d.rectangle((0,235,W,H),fill='#90765a' if setting!='bed' else '#b5946d')
    for y in range(270,670,57):line(d,[(0,y),(W,y)],'#ae8a68',1)
    for x in range(0,W,78):line(d,[(x,265),(x,656)],'#876e59',1)
    poly(d,[(0,0),(W,0),(W,225),(0,275)],'#433c38',2)
    for i in range(7):
        x=i*88-10
        poly(d,[(x-11,0),(x+6,0),(x+61,265),(x+40,265)],'#6d4c34',1)
    d.rectangle((0,660,W,H),fill=base)
    for x in range(0,W,75):line(d,[(W/2+(x-W/2)*.4,660),(x,H)],'#68584c',2)
    for y in range(675,H,74):line(d,[(0,y),(W,y)],'#76604e',2)
    for x in (60,W-60):
        rect(d,(x-22,218,x+22,720),'#9d795a',2)
        poly(d,[(x-35,218),(x+35,218),(x+24,201),(x-24,201)],'#b4966e',2)
        for flick in (0,):
            line(d,[(x,304),(x,374)],DARK,7)
            ellipse(d,(x-15,282+math.sin(t*7+x)*3,x+15,326),'#ebac55',0,None)
            ellipse(d,(x-7,293,x+7,320),'#f5d996',0,None)
    if setting=='bed':
        # bedroom leaves space for the living olive-root bed later
        d.rectangle((80,350,460,640),fill='#ad8c65')
        poly(d,[(70,350),(470,350),(455,386),(90,386)],'#674a3d')

def hamlet(d,t):
    # Same Mycenaean walls/city perspective as the OWNED 60s animation.
    for x in range(-45,W+90,91):
        ht=70+(x*17)%37
        rect(d,(x,584-ht,x+80,700),'#ae9070',1)
        poly(d,[(x-12,590-ht),(x+38,562-ht),(x+92,590-ht)],'#825846',2)
        rect(d,(x+29,622-ht,x+40,645-ht),'#53626d',1)
    d.polygon([(0,700),(W,690),(W,H),(0,H)],fill='#c5a37a')
    for y in range(712,H,52):line(d,[(0,y),(W,y)],'#b59572',1)

def troy_gate(d,t,night=False,openness=1):
    # Real gate width > horse full body; right leaf hinges outward.
    hamlet(d,t)
    for x1,x2 in [(0,90),(428,W)]:rect(d,(x1,335,x2,758),'#a98a6b',3)
    for x in (89,428):rect(d,(x-18,280,x+18,754),'#a88969',3)
    for x in range(0,W,53):rect(d,(x,313,x+39,340),'#a88969',2)
    # two doors pivot from appropriate side, not slide like a photo.
    if openness<.95:
        wid=165*(1-openness)
        poly(d,[(89,379),(89+wid,392),(89+wid,730),(89,735)],'#654532',3)
        poly(d,[(428-wid,392),(428,379),(428,735),(428-wid,730)],'#654532',3)
        for yy in range(414,735,30):line(d,[(89,yy),(89+wid,yy)],'#a07853',1)
    d.polygon([(0,750),(W,735),(W,H),(0,H)],fill='#c0a17a')
    if night:d.rectangle((0,760,W,H),fill='#62636a')

def cliff_cave(d,t):
    # A single coherent massive cliff with a tunnel and unified floor.
    poly(d,[(0,178),(540,178),(540,770),(0,770)],'#6b655c',4)
    poly(d,[(0,210),(105,190),(165,256),(215,310),(245,410),(330,440),(420,360),(480,253),(540,212),(540,780),(0,780)],'#494946',3)
    poly(d,[(90,770),(145,382),(228,291),(314,269),(402,342),(458,770)],'#1d2e35',4)
    for j in range(10):
        yy=260+j*45
        line(d,[(17,yy),(int(90+18*math.sin(j*2)),yy+24)],'#8b8273',2)
        line(d,[(490,yy+12),(537,yy-21)],'#837a69',2)
    d.polygon([(0,740),(W,740),(W,H),(0,H)],fill='#71665a')
    for y in range(746,960,37):line(d,[(0,y),(W,y)],'#716453',1)

def ocean(d,t,storm=False):
    y=604
    d.polygon([(0,y),(W,y),(W,H),(0,H)],fill='#2d5267' if not storm else '#233e55')
    for k in range(14):
        yy=y+k*26
        xx=(k*137+int(t*31))%W
        line(d,[(xx-50,yy+4*math.sin(t+k)),(xx+76,yy-4*math.sin(t*.7+k))], '#82b4ba' if k%3 else '#5a8d9f',2)
        x2=(xx+270)%W
        line(d,[(x2-30,yy+15),(x2+48,yy+13)],'#8aadb2',1)
    if storm:
        for j in range(4):
            poly(d,[(0,300+j*40),(200,274+j*23),(540,300+j*40),(540,335+j*40),(0,340+j*40)],'#263c4b',2)

def coast(d,t):
    hamlet(d,t)
    d.polygon([(0,800),(100,760),(250,795),(370,763),(540,805),(540,H),(0,H)],fill='#cdb187')

def forest(d,t,magic=False):
    hamlet(d,t)
    for j in range(7):
        x=25+j*88;h=120+(j*17)%62
        line(d,[(x,735),(x+4,735-h)],'#65513e',10)
        for q in range(4):
            xx=x+31*math.sin(q*1.9+j);yy=735-h+30*math.cos(q*2+j)
            ellipse(d,(xx-51,yy-36,xx+44,yy+31),'#54765c' if not magic else '#477566',1)
    d.polygon([(0,752),(540,734),(540,H),(0,H)],fill='#7c906c')

def side_ship(d,x,y,scale,t,show_sail=True):
    # Hand-illustrated wooden ship, layered hull, curved stern/prow, oars.
    s=scale; bob=2.4*math.sin(t*2.0)
    y+=bob
    poly(d,[(x-1.45*s,y),(x+1.42*s,y),(x+1.18*s,y+.52*s),(x-.99*s,y+.53*s)],'#654b3b',4)
    for j in range(3):line(d,[(x-1.18*s,y+.10*s+j*.12*s),(x+1.14*s,y+.10*s+j*.12*s)],'#ab7951',max(1,int(.027*s)))
    line(d,[(x-1.39*s,y+.08*s),(x-1.53*s,y-.45*s)],'#957455',max(2,int(.075*s)))
    line(d,[(x+1.38*s,y+.04*s),(x+1.60*s,y-.40*s)],'#957455',max(2,int(.075*s)))
    if show_sail:
        line(d,[(x,y),(x,y-2.43*s)],DARK,max(2,int(.05*s)))
        wave=math.sin(t*1.1)*.13*s
        poly(d,[(x,y-2.33*s),(x+.92*s+wave,y-1.45*s),(x+.79*s,y-.20*s),(x,y-.20*s)],'#e0d2b6',3)
        line(d,[(x,y-2.23*s),(x+.66*s,y-1.40*s)],'#baa785',2)
    for j in range(5):
        ox=x+(-.84+j*.42)*s
        dx=22*math.sin(t*4+j*.4)
        line(d,[(ox,y+.23*s),(ox+dx,y+.80*s)],'#b68a5d',max(2,int(.032*s)))
    return y

def horse_original(x,y,width,t):
    # Entire original user-accepted horse sprite (not a reimagined model).
    composite_sprite(MONO,x,y,width)
    # wheel centers continue using genuine material base with moving bronze spokes.
    srcw, srch=MONO.size;f=width/srcw
    left=x-width/2
    top=y-srch*f
    for wx,wy in [(111-25,696-386),(244-25,698-386)]:
        cx=left+wx*f;cy=top+wy*f
        for k in range(4):
            th=t*2.9+k*math.pi/2
            line(D,[(cx,cy),(cx+9*f*math.cos(th),cy+9*f*math.sin(th))],'#f0bd69',max(1,int(2*f)))

def pig(d,x,y,s,t):
    ellipse(d,(x-s*.72,y-s*.65,x+s*.65,y),'#c28f78',3)
    ellipse(d,(x+s*.37,y-s*.69,x+s*.88,y-s*.25),'#c28f78',3)
    poly(d,[(x+s*.42,y-s*.68),(x+s*.48,y-s*1.03),(x+s*.71,y-s*.74)],'#c99783',2)
    ellipse(d,(x+s*.78,y-s*.49,x+s*1.02,y-s*.34),'#dcb5a1',2)
    ellipse(d,(x+s*.65,y-s*.58,x+s*.69,y-s*.54),DARK,0,None)
    for a in (-.35,.26):line(d,[(x+a*s,y),(x+a*s,y+s*.19)],'#8a6755',max(3,int(s*.09)))

def sheep(d,x,y,s,t):
    bob=abs(math.sin(t*4))*.04*s;y-=bob
    for j in range(5):
        xx=x+(-.42+j*.19)*s
        ellipse(d,(xx-s*.24,y-.98*s,xx+s*.26,y-.29*s),'#ded5bd',2)
    ellipse(d,(x+.51*s,y-.92*s,x+.94*s,y-.42*s),'#8c765f',3)
    for xx in (-.45,.20):line(d,[(x+xx*s,y-.30*s),(x+xx*s,y+.04*s)],'#7b6757',max(2,int(s*.07)))
    ellipse(d,(x+.77*s,y-.76*s,x+.83*s,y-.71*s),DARK,0,None)

def dog(d,x,y,s,t,raise_head=False):
    ellipse(d,(x-.65*s,y-.48*s,x+.48*s,y),'#a58c70',3)
    for xx in (-.3,.29):line(d,[(x+xx*s,y-.12*s),(x+xx*s,y+.17*s)],'#6a5141',5)
    hy=y-.58*s-(math.sin(t*.7)*.10*s if raise_head else 0)
    ellipse(d,(x+.29*s,hy-s*.18,x+.88*s,hy+s*.27),'#8e6f54',3)
    poly(d,[(x+.55*s,hy-s*.09),(x+.83*s,hy-s*.32),(x+.85*s,hy+.03*s)],'#614537',2)
    ellipse(d,(x+.72*s,hy+.01*s,x+.77*s,hy+.05*s),DARK,0,None)
    line(d,[(x-.6*s,y-.39*s),(x-.90*s,y-.57*s),(x-.94*s,y-.37*s)],'#806650',4)

def orchard_tree(d,x,y,s,t):
    line(d,[(x,y),(x,y-2.3*s),(x-.32*s,y-3*s)],'#6c5541',max(5,int(.23*s)))
    for j in range(7):
        xx=x+math.sin(j*2.31)*s*1.30+math.sin(t*.4+j)*s*.025
        yy=y-(2.6+math.cos(j*2.31)*.40)*s
        ellipse(d,(xx-.56*s,yy-.45*s,xx+.56*s,yy+.45*s),'#62836c',2)

def throne(d,x,y,s):
    rect(d,(x-.33*s,y-.9*s,x+.33*s,y),'#966b49',3)
    poly(d,[(x-.40*s,y-.93*s),(x+.40*s,y-.93*s),(x+.34*s,y-.99*s),(x-.34*s,y-.99*s)],'#c6a36c',3)

def bowl(d,x,y,s):
    poly(d,[(x-.40*s,y-.12*s),(x+.41*s,y-.12*s),(x+.29*s,y+.19*s),(x-.27*s,y+.19*s)],'#a97e55',2)
    ellipse(d,(x-.40*s,y-.18*s,x+.40*s,y-.04*s),'#b99c6f',2)

def bow(d,x,y,s,t,drawback=0):
    # Bow reacts to hands; animated draw point moves through 2D trajectory.
    for sh in (-1,1):
        a=sh*.58*s
        line(d,[(x,y+a),(x-.13*s,y+sh*.45*s),(x-.24*s,y)],DARK,max(3,int(s*.056)))
        line(d,[(x,y+a),(x-.13*s,y+sh*.45*s),(x-.24*s,y)],'#a97952',max(2,int(s*.031)))
    drawx=x+.18*s*drawback
    line(d,[(x,y-.58*s),(drawx,y),(x,y+.58*s)],'#ead4ab',max(2,int(s*.019)))
    return (drawx,y)

def axe_line(d,x,y,total=12):
    for k in range(total):
        xx=x+k*15
        line(d,[(xx,y),(xx,y-94)],'#a1774f',5)
        ellipse(d,(xx-3,y-102,xx+6,y-85),'#b49561',2)

def bridge_of_ship(d,x,y,s,t):
    # Decorative deck/short rail used to place rowers relative to a real boat.
    side_ship(d,x,y,s,t)

# Directed 4x16 story shots: each set plays different causal ACTION with
# character/key prop positions progressing rather than reverse walking loops.
def action_shot(d,i,j,p,t):
    B=775
    hh=230
    if i==0:  # 00:00 — bow flashforward
        if j==0:
            actor(d,265,B,238,'beggar',t,'hold')
            actor(d,94,B-32,190,'suitor',t,'drink')
            actor(d,440,B-24,190,'suitor2',t,'offer')
            bow(d,352,590,176,t,.08)
        elif j==1:
            actor(d,235,B,280,'beggar',t,'draw')
            bow(d,331,556,218,t,ease(p)*.70)
            actor(d,469,B-25,160,'suitor',t,'hold')
        elif j==2:
            actor(d,228,B,310,'beggar',t,'draw')
            bow(d,310,550,220,t,.50+.30*ease(p))
            # hand tracks string
            line(d,[(294,537),(340+18*p,547)],SKIN,7)
        else:
            actor(d,255,B,286,'beggar',t,'aim')
            actor(d,440,B-20,180,'suitor2',t,'idle')
            bow(d,360,555,207,t,.80)
    elif i==1:  # 00:09 — same original horse from approved first film
        if j==0:
            troy_gate(d,t,openness=lp(.55,1,ease(p)))
            horse_original(lp(174,294,ease(p)),742,295,t)
            actor(d,430,756,115,'trojan',t,'pull')
            line(d,[(410,700),(320,716)],'#71563d',3)
        elif j==1:
            troy_gate(d,t,openness=1)
            horse_original(lp(232,349,ease(p)),744,310,t)
            actor(d,452,774,102,'trojan',t,'walk')
            line(d,[(433,706),(386,724)],'#73523c',3)
        elif j==2:
            troy_gate(d,t,night=True,openness=1)
            horse_original(220,752,310,t)
            # Exit explicitly from horse side hatch, then cross threshold
            actor(d,lp(173,340,ease(p)),764,128,'odysseus',t,'walk')
            actor(d,lp(195,382,ease(p)),770,118,'sailor',t,'walk')
            if p>.37:
                rect(d,(205,559,253,620),'#383136',2)
        else:
            ocean(d,t)
            side_ship(d,lp(130,322,ease(p)),720,108,t)
            # city glows behind departing ship
            for k in range(5):
                xx=k*110+12
                ellipse(d,(xx-8,577,xx+10,613),'#e0a15b',1)
                line(d,[(xx,616),(xx+math.sin(t*5+k)*12,562)],'#c87d52',3)
    elif i==2:  # Cícones, lotus
        if j==0:
            actor(d,lp(415,239,ease(p)),775,218,'odysseus',t,'run')
            actor(d,lp(290,80,ease(p)),780,188,'sailor',t,'run')
            actor(d,460,778,190,'trojan',t,'fight')
        elif j==1:
            side_ship(d,325,729,97,t)
            actor(d,lp(90,275,ease(p)),777,190,'odysseus',t,'run')
            actor(d,lp(32,187,ease(p)),789,175,'sailor',t,'escape')
        elif j==2:
            orchard_tree(d,100,778,45,t)
            orchard_tree(d,473,798,42,t)
            actor(d,280,785,238,'sailor',t,'offer')
            ellipse(d,(320,550,340,567),'#ebbd81',2)
            actor(d,97,785,195,'odysseus',t,'approach')
        else:
            actor(d,lp(360,233,ease(p)),780,220,'sailor',t,'walk')
            actor(d,lp(120,218,ease(p)),780,225,'odysseus',t,'pull')
            line(d,[(260,603),(310-80*ease(p),614)],'#ad8765',6)
            side_ship(d,458,789,55,t,False)
    elif i==3:  # Polyphemus — four clear causal beats
        if j==0:
            actor(d,405,785,415,'cyclops',t,'push')
            actor(d,120,774,146,'odysseus',t,'escape')
            actor(d,53,788,121,'sailor',t,'escape')
            sx=lp(567,269,ease(p))
            ellipse(d,(sx-116,458,sx+125,795),'#8a857c',6)
            for yy in (533,607,695):line(d,[(sx-73,yy),(sx+28,yy+14)],'#b3a18d',4)
            # contact points connected to both arms, not magically floating rock
            line(d,[(409,509),(sx+70,547)],'#c9a98a',12)
            line(d,[(448,549),(sx+65,587)],'#c9a98a',11)
        elif j==1:
            actor(d,390,778,395,'cyclops',t,'drink')
            actor(d,162,779,177,'odysseus',t,'offer')
            bowl(d,280,574,66)
            if p>.3:line(d,[(289,555),(368,488)],'#c8ad80',5)
        elif j==2:
            actor(d,395,798,390,'cyclops',t,'fall')
            actor(d,172,788,181,'odysseus',t,'pull')
            actor(d,270,790,171,'sailor',t,'pull')
            line(d,[(166,610),(lp(298,390,ease(p)),489)],'#825238',19)
            line(d,[(166,610),(lp(298,390,ease(p)),489)],'#db994f',6)
            # no gore
        else:
            if p<.70:
                for k in range(3):
                    sheep(d,lp(80+k*145,164+k*145,ease(p/.70)),780,95,t+k)
                actor(d,130,786,120,'odysseus',t,'escape')
            else:
                ocean(d,t)
                side_ship(d,290,720,95,t)
                actor(d,lp(390,480,ease((p-.70)/.30)),785,268,'cyclops',t,'fight')
    elif i==4:
        if j==0:
            actor(d,375,775,244,'aiolos',t,'offer')
            actor(d,176,782,215,'odysseus',t,'hold')
            poly(d,[(243,567),(280,547),(312,577),(285,640),(253,626)],'#8c654b',3)
            line(d,[(250,565),(294,561)],'#e7cc9f',3)
        elif j==1:
            side_ship(d,280,735,111,t)
            actor(d,220,744,139,'sailor',t,'offer')
            for q in range(5):
                th=t*3+q*1.2
                line(d,[(220,545),(220+110*math.sin(th),530-60*q)],'#c8e1d4',3)
        elif j==2:
            side_ship(d,lp(380,200,ease(p)),705,105,t)
            for q in range(10):
                xx=(q*130+int(t*69))%540
                line(d,[(xx,470),(xx+72,402)],'#d2e2dd',3)
        else:
            side_ship(d,lp(120,320,ease(p)),735,85,t)
            for x in (60,465):
                actor(d,x,779,300,'cyclops',t,'fight')
            for q in range(3):
                x=lp(75,325,ease(p))
                ellipse(d,(x+q*20,430+q*35,x+q*20+50,485+q*35),'#726a65',3)
    elif i==5:
        if j==0:
            actor(d,370,770,239,'circe',t,'offer')
            actor(d,145,774,195,'sailor',t,'drink')
            bowl(d,265,585,70)
        elif j==1:
            actor(d,376,785,234,'circe',t,'hold')
            if p<.50:actor(d,175,790,220*(1-ease(p/.5)*.43),'sailor',t,'fall')
            pig(d,lp(100,200,ease(p)),784,80*ease(p),t)
            for k in range(6):
                xx=(k*87+120);ellipse(d,(xx-10,390+30*math.sin(t*2+k),xx+8,410+30*math.sin(t*2+k)),'#dfc789',0,None)
        elif j==2:
            actor(d,350,790,231,'hermes',t,'offer')
            actor(d,153,789,231,'odysseus',t,'hold')
            line(d,[(250,600),(285,569)],'#76936b',9)
            ellipse(d,(277,554,299,577),'#8cb47c',2)
        else:
            actor(d,136,790,220,'odysseus',t,'hold')
            actor(d,375,786,229,'circe',t,'hold')
            actor(d,lp(253,302,ease(p)),782,210,'sailor',t,'approach')
    elif i==6:
        if j==0:
            side_ship(d,lp(420,270,ease(p)),730,97,t)
            actor(d,235,770,171,'odysseus',t,'kneel')
        elif j==1:
            actor(d,176,782,242,'odysseus',t,'kneel')
            actor(d,380,782,246,'tiresias',t,'offer')
        elif j==2:
            actor(d,185,780,245,'odysseus',t,'embrace')
            actor(d,400,781,244,'mother',t,'embrace')
        else:
            actor(d,lp(178,259,ease(p)),779,245,'odysseus',t,'embrace')
            actor(d,lp(399,320,ease(p)),780,250,'mother',t,'embrace')
            # spectral hands cannot meet; transparency visual rim
            line(d,[(296,582),(319,580)],'#bfd6d9',2)
    elif i==7:
        if j==0:
            side_ship(d,280,747,109,t)
            actor(d,152,752,144,'sailor',t,'hold')
            actor(d,308,742,165,'odysseus',t,'hold')
        elif j==1:
            side_ship(d,290,755,112,t)
            actor(d,300,737,176,'odysseus',t,'pull')
            line(d,[(288,558),(312,680)],'#e6ddc1',6)
            line(d,[(310,556),(285,705)],'#e6ddc1',6)
        elif j==2:
            for k in range(3):
                actor(d,100+k*175,779,214,'siren',t,'offer')
                for q in range(3):
                    yy=400+k*60;xx=120+k*175+q*12
                    line(d,[(xx,yy),(xx+11,yy-14)],'#c8dcdb',2)
        else:
            side_ship(d,lp(185,345,ease(p)),755,105,t)
            actor(d,250,739,166,'odysseus',t,'pull')
    elif i==8:
        if j==0:
            side_ship(d,285,730,99,t)
            for k in range(6):
                xx=375+k*17
                line(d,[(xx,687),(xx+math.sin(t*3+k)*14,492)],'#49665c',10)
            for r in range(5):
                x=118;y=711
                d.arc((x-r*15,y-r*15,x+r*15+2,y+r*15+2),0,320,fill='#a7c9c8',width=3)
        elif j==1:
            side_ship(d,lp(370,195,ease(p)),730,102,t)
            for k in range(6):
                x=380+k*16
                line(d,[(x,680),(x-60+math.sin(t*4+k)*12,475)],'#5f7568',12)
        elif j==2:
            side_ship(d,280,729,115,t)
            for k in range(6):
                x=420+k*13
                neckx=x-90+math.sin(t*4.1+k)*18
                line(d,[(x,687),(neckx,521)],'#506b65',11)
                ellipse(d,(neckx-17,504,neckx+19,538),'#7d8d78',3)
                ellipse(d,(neckx-4,511,neckx+4,519),'#e8bd74',1)
            for k in range(2):actor(d,199+k*105,737,103,'sailor',t,'fall')
        else:
            side_ship(d,270,724,118,t)
            actor(d,280,728,181,'odysseus',t,'kneel')
            for k in range(3):line(d,[(230+k*52,738),(230+k*52,776)],'#745e4f',2)
    elif i==9:
        if j==0:
            for k in range(3):
                ellipse(d,(120+k*110,701,202+k*110,763),'#d9c9a4',2)
                ellipse(d,(177+k*110,691,229+k*110,731),'#bcac8c',2)
            actor(d,94,777,208,'sailor',t,'hold')
        elif j==1:
            actor(d,165,775,225,'odysseus',t,'fight')
            actor(d,370,780,213,'sailor',t,'kneel')
            for k in range(2):
                ellipse(d,(270+k*95,719,350+k*95,776),'#c0ae88',2)
        elif j==2:
            side_ship(d,263,739,114,t)
            y=375;x=278+20*math.sin(t*6)
            poly(d,[(x,275),(x-20,462),(x+40,460),(x-45,750),(x+77,486),(x+2,495)],'#f6dba3',3)
            for q in range(12):
                xx=(q*89+int(t*69))%540
                line(d,[(xx,180),(xx+77,240)],'#b2c4ca',2)
        else:
            line(d,[(60,701),(440,760)],'#785138',26)
            actor(d,lp(168,290,ease(p)),747,165,'odysseus',t,'pull')
            for j2 in range(3):ellipse(d,(50+j2*167,721,114+j2*167,754),'#5d8690',1)
    elif i==10:
        if j==0:
            actor(d,245,789,228,'odysseus',t,'sleep')
            actor(d,390,780,226,'calypso',t,'kneel')
            orchard_tree(d,115,784,53,t)
        elif j==1:
            actor(d,200,781,238,'odysseus',t,'kneel')
            actor(d,375,781,226,'calypso',t,'offer')
            orchard_tree(d,80,784,49,t)
        elif j==2:
            actor(d,370,774,247,'hermes',t,'hold')
            actor(d,170,781,229,'odysseus',t,'hold')
            actor(d,450,782,206,'calypso',t,'hold')
        else:
            side_ship(d,lp(228,376,ease(p)),738,100,t)
            actor(d,142,778,195,'calypso',t,'hold')
    elif i==11:
        if j==0:
            actor(d,lp(194,245,ease(p)),780,210,'odysseus',t,'kneel')
            actor(d,400,777,229,'nausicaa',t,'offer')
        elif j==1:
            actor(d,180,773,239,'odysseus',t,'hold')
            actor(d,370,773,245,'suitor2',t,'offer')
            bowl(d,273,630,85)
        elif j==2:
            side_ship(d,lp(195,320,ease(p)),734,118,t)
            actor(d,298,742,175,'odysseus',t,'sleep')
        else:
            actor(d,270,780,246,'odysseus',t,'kneel')
            orchard_tree(d,105,784,42,t)
            orchard_tree(d,460,787,44,t)
            ellipse(d,(230,780,310,799),'#dfc79f',2)
    elif i==12:
        if j==0:
            for k in range(4):actor(d,120+k*102,776,197,'suitor' if k%2 else 'suitor2',t,'drink')
            actor(d,268,739,210,'penelope',t,'hold')
            for k in range(3):bowl(d,98+k*157,720,66)
        elif j==1:
            actor(d,210,780,239,'penelope',t,'weave')
            for k in range(12):line(d,[(300+k*12,512),(300+k*12,760)],'#d4bc95',2)
            line(d,[(298,625+math.sin(t*3)*12),(438,625+math.sin(t*3)*12)],'#c19c6a',6)
        elif j==2:
            actor(d,220,775,232,'penelope',t,'weave')
            for k in range(12):line(d,[(300+k*12,512),(300+k*12,720-40*ease(p))],'#ead9b6',2)
            line(d,[(299,620),(438,620)],'#927353',4)
        else:
            actor(d,182,780,231,'telemachus',t,'walk')
            actor(d,400,781,237,'athena',t,'offer')
    elif i==13:
        if j==0:
            actor(d,lp(165,251,ease(p)),779,223,'odysseus',t,'embrace')
            actor(d,lp(382,299,ease(p)),781,215,'telemachus',t,'embrace')
        elif j==1:
            actor(d,170,781,235,'beggar',t,'kneel')
            dog(d,385,784,110,t,raise_head=p>.15)
        elif j==2:
            actor(d,210,783,227,'beggar',t,'kneel')
            actor(d,380,782,223,'eurycleia',t,'kneel')
            bowl(d,298,760,76)
            line(d,[(268,758),(238,790)],'#ccac83',5)
        else:
            actor(d,180,781,220,'beggar',t,'hold')
            actor(d,360,781,221,'telemachus',t,'hold')
            line(d,[(258,640),(282,625)],'#dec593',3)
    elif i==14:
        if j==0:
            actor(d,175,781,221,'suitor',t,'draw')
            actor(d,375,781,215,'suitor2',t,'fight')
            bow(d,287,601,161,t,.12)
        elif j==1:
            actor(d,180,786,257,'beggar',t,'aim')
            bx,by=bow(d,293,582,188,t,.85)
            axe_line(d,330,732,12)
            if p>.33:line(d,[(310,570),(lp(315,515,ease((p-.33)/.67)),568)],'#e6d3a0',6)
        elif j==2:
            actor(d,250,781,264,'odysseus',t,'fight')
            actor(d,460,780,209,'suitor',t,'fall')
            bow(d,361,602,148,t,.1)
        else:
            actor(d,192,781,246,'odysseus',t,'fight')
            actor(d,360,781,224,'telemachus',t,'fight')
            actor(d,455,775,180,'suitor2',t,'fall')
            line(d,[(199,560),(349,526+25*math.sin(t*6))],BRONZE,5)
    elif i==15:
        if j==0:
            orchard_tree(d,300,753,64,t)
            poly(d,[(171,689),(407,689),(409,774),(166,774)],'#ad8460',3)
            actor(d,144,788,217,'odysseus',t,'hold')
            actor(d,452,787,219,'penelope',t,'hold')
        elif j==1:
            actor(d,lp(177,258,ease(p)),784,244,'odysseus',t,'embrace')
            actor(d,lp(387,299,ease(p)),785,235,'penelope',t,'embrace')
        elif j==2:
            actor(d,lp(190,258,ease(p)),784,229,'odysseus',t,'embrace')
            actor(d,lp(400,302,ease(p)),788,203,'laertes',t,'embrace')
            actor(d,460,783,223,'athena',t,'offer')
        else:
            orchard_tree(d,80,795,53,t)
            orchard_tree(d,469,790,55,t)
            for k,(role,h) in enumerate([('odysseus',232),('penelope',226),('telemachus',222)]):
                actor(d,150+k*122,786,h,role,t,'idle')

# 2-line genuine spoken text chunks by scene, distributed only within measured
# natural-audio silence boundaries; this is approximate alignment, not ASR.
def captions_for_scene(s):
    words=LINES[s].split();chunks=[];i=0
    while i<len(words):
        chunk=[]
        while i<len(words) and len(' '.join(chunk+[words[i]]))<57:
            chunk.append(words[i]);i+=1
        if not chunk and i<len(words):chunk=[words[i]];i+=1
        chunks.append(' '.join(chunk))
    return chunks
CAPTIONS=[captions_for_scene(s) for s in range(16)]

def caption(d,scene,u,scale):
    arr=CAPTIONS[scene]
    j=min(len(arr)-1,round(clamp(u)*len(arr)-.001))
    txt=arr[j]
    font=ImageFont.truetype(FONT_DIR+'/DejaVuSans-Bold.ttf',22)
    words=txt.split();rows=['']
    for word in words:
        if len(rows[-1]+' '+word)<=36:rows[-1]=(rows[-1]+' '+word).strip()
        else:rows.append(word)
    rows=rows[:2]
    y=825-(len(rows)-1)*5
    for k,s in enumerate(rows):
        bb=d.textbbox((0,0),s,font=font,stroke_width=1)
        x=(W-(bb[2]-bb[0]))//2
        d.text((x,y+27*k),s,font=font,fill='#f5ecd8',stroke_width=2,stroke_fill='#26333a')

def frame(t,scale=1):
    global CANVAS,SCALE,D
    SCALE=scale
    i=min(15,max(0,bisect.bisect_right(T,t)-1))
    u=clamp((t-T[i])/(T[i+1]-T[i]))
    j=min(3,int(u*4));p=u*4-j
    setting=SETS[i][j]
    CANVAS=Image.new('RGB',(round(W*scale),round(H*scale)),(30,59,74))
    D=canon.base.ScaledDraw(ImageDraw.Draw(CANVAS),scale) if scale!=1 else ImageDraw.Draw(CANVAS)
    canon.IMG=CANVAS;canon.SCALE=scale
    illustrated_sky(D,setting,t)
    if setting in ('hall','bed','weave','circe','hut'):
        palace(D,setting,t)
    elif setting in ('troy','troy_night'):
        troy_gate(D,t,night=setting=='troy_night',openness=1)
    elif setting in ('cave','cave_exit'):
        cliff_cave(D,t)
    elif setting in ('sea','storm','strait','wind','sirens','harbor'):
        ocean(D,t,storm=setting=='storm')
    elif setting in ('island','lotus','orchard'):
        forest(D,t,magic=setting=='lotus')
    elif setting in ('coast','shore','ithaca','courtyard'):
        coast(D,t)
    elif setting=='underworld':
        d=D;d.polygon([(0,567),(W,567),(W,H),(0,H)],fill='#283c48')
        for k in range(11):
            x=(k*53+int(t*3))%W;y=583+k*24
            ellipse(d,(x-46,y-6,x+47,y+5),'#617985',0,None)
    # Grounded 4-part acting choreography, each shot bound to exact narration period.
    action_shot(D,i,j,p,t)
    caption(D,i,u,scale)
    if t<3:
        font=ImageFont.truetype(FONT_DIR+'/DejaVuSerif-Bold.ttf',14)
        D.text((37,48),'MITOLOGIA GREGA  ·  ODISSEU',font=font,fill=PALE)
    if t>=T[15]+.94*(T[16]-T[15]):
        # Narrative final fades only after concluding shot, not hiding unfinished actor motion.
        k=clamp((t-(T[15]+.94*(T[16]-T[15])))/(T[16]-(T[15]+.94*(T[16]-T[15]))))
        if k>.12:
            dark=Image.new('RGB',CANVAS.size,'#0e1c27')
            CANVAS=Image.blend(CANVAS,dark,k*.82)
    canon.IMG=None
    return CANVAS

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--output',required=True)
    pa.add_argument('--width',type=int,default=540)
    pa.add_argument('--fps',type=int,default=24)
    pa.add_argument('--start',type=float,default=0)
    pa.add_argument('--duration',type=float,default=220.56)
    pa.add_argument('--voice')
    pa.add_argument('--crf',type=int,default=22)
    args=pa.parse_args()
    if args.width%2!=0:raise SystemExit('Width must be even')
    scale=args.width/W
    h=round(H*scale)//2*2
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    intermediate=target.with_suffix('.tempvideo.mp4') if args.voice else target
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24',
         '-video_size',f'{args.width}x{h}','-framerate',str(args.fps),'-i','-',
         '-c:v','libx264','-threads','3','-preset','veryfast','-crf',str(args.crf),'-pix_fmt','yuv420p',
         '-movflags','+faststart',str(intermediate)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=round(args.duration*args.fps)
    try:
        for n in range(frames):
            img=frame(args.start+n/args.fps,scale)
            proc.stdin.write(img.tobytes())
            if n and n%(args.fps*10)==0:print('TUE_CANON_2D_FRAME',n,'/',frames,flush=True)
    finally:
        proc.stdin.close()
    err=proc.stderr.read().decode(errors='replace');ret=proc.wait()
    if ret:raise RuntimeError('Video encoding failed: '+err[-1000:])
    if args.voice:
        audio=Path(args.voice)
        assert audio.exists(),'Original Rasalgethi WAV missing'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(intermediate),'-i',str(audio),
            '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',
            '-shortest','-movflags','+faststart',str(target)],check=True)
        intermediate.unlink()
    receipt={'title':'A Odisseia — O Regresso a Ítaca','style':'same canonical first Trojan Horse film',
        'owned_original_assets':['Odysseus head from owner-supplied 60s video','original Trojan wooden horse 2D cutout'],
        'new_characters':list(canon.CAST.keys()),'script_scenes':16,'directed_shots':64,
        'voice_original':bool(args.voice),'duration_sec':args.duration,'fps':args.fps,'width':args.width,'height':h,
        'published':False,'qc_visual_user_approved':False,'4k_native':args.width>=2160,
        'caveats':['Subtitle chunk timing approximated by scene audio boundaries','2D cutout animation, not hand-animated individual fullbody poses','Scene-to-scene artistic QC required before release']}
    target.with_suffix('.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    print('TUE_ODISSEIA_2D_CANONICAL_16_SCENES_64_SHOTS_RENDERED_QC_ONLY',flush=True)
if __name__=='__main__':main()