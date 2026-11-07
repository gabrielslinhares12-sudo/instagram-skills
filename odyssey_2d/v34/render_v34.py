#!/usr/bin/env python3
"""Odyssey — 68 original action beats, 16 scenes, canon 2D Troy cartoon.

Native 2D source is a QC film. Each event has its own storyboard and actor/object
animation, an anchored scenery layout and original Rasalgethi voice.  No paid API.
"""
from __future__ import annotations
import math,bisect,json,sys,subprocess,os,random,argparse
from collections import OrderedDict,Counter
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import render_16_cenas as v
import scenery_v28 as sc
import puppet_original_v30 as pup
from functools import lru_cache
_cached_rotated=lru_cache(maxsize=1000)(pup.rotated)
W,H=v.W,v.H
CONTRACT=json.loads((ROOT/'shot_contract.json').read_text(encoding='utf-8'))
SHOTS=CONTRACT['shots']; START=[s['start_seconds_estimate'] for s in SHOTS]
assert len(SHOTS)==68 and len(set(s['narrative_action'] for s in SHOTS))==68
assert abs(SHOTS[-1]['end_seconds_estimate']-220.56)<.01
HERO=Image.open(ROOT/'assets'/'ODISSEU_ORIGINAL_TROIA_SPRITE_CANONICO.png').convert('RGBA')
INK='#332a2b';STONE='#81796d';STRAW='#e2c497';WOOD='#8c684a';GLINT='#e9d2a6';RED='#964b48';SKIN='#c9966b';WATER='#7fa7b1';GOLD='#bca06a'
BG=OrderedDict(); FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',17)

def E(t):return v.ease(t)
def M(a,b,p):return v.lp(a,b,E(p))
def P(d,pts,c,w=3):v.poly(d,pts,c,w)
def L(d,pts,c,w=4):v.line(d,pts,c,w)
def O(d,b,c,w=3):v.ellipse(d,b,c,w)
def R(d,b,c,w=3):v.rect(d,b,c,w)
def act(d,x,y,h,role='odysseus',t=0,pose='idle'):
    if role in ('antinoos','eurymachos','eurymachus','alcinous','cicones'):role='suitor'
    elif role in ('greek','trojan','trojans'):role='trojan'
    elif role in ('anticleia',):role='mother'
    elif role in ('aiolos',):role='aiolos'
    elif role in ('crew',):role='sailor'
    elif role in ('sailors',):role='sailor'
    elif role in ('giants',):role='cyclops'
    elif role in ('scylla',):role='cyclops'
    return v.actor(d,x,y,h,role,t,pose)
def figure_shadows(d, positions):
    for x,y,r in positions:
        O(d,(x-r,y-10,x+r,y+6),'#786656',1)
def rays(d,x,y,t,c='#f8c480'):
    for i in range(7):
        th=i*math.tau/7+t*.55
        L(d,[(x+26*math.cos(th),y+26*math.sin(th)),(x+43*math.cos(th),y+43*math.sin(th))],c,2)
def waves(d,t,y=768,off=0):
    for k in range(7):
        xx=((k*113+int(t*35)+off)%710)-90
        yy=y+(k%3)*24+math.sin(t*3+k)*5
        d.arc((xx,yy,xx+95,yy+18),5,170,fill='#aacbd1',width=3)
def smoke(d,x,y,t,size=1):
    for k in range(4):
        xx=x+23*math.sin(.9*t+k*1.7)*size
        yy=y-k*25*size-(t*15%(26*size))
        O(d,(xx-16*size,yy-15*size,xx+16*size,yy+8*size),'#747575',1)
def flame(d,x,y,t,scale=1):
    hh=(28+10*math.sin(t*7+x))*scale
    P(d,[(x-9*scale,y),(x-14*scale,y-13*scale),(x-3*scale,y-hh),(x+9*scale,y-8*scale),(x+12*scale,y)],'#dc814d',2)
    P(d,[(x-4*scale,y),(x-3*scale,y-hh*.65),(x+3*scale,y-2*scale)],'#f3d99c',1)
def boulder(d,x,y,r,phase=0):
    pts=[]
    for i in range(10):
        a=i*math.tau/10
        rr=r*(.83+.12*math.sin(i*3+1.2))
        pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
    # Large grounded irregular stone with shaded planes, sharp weight cues,
    # internal cracks and a bottom contact shadow (never a flat floating disc).
    O(d,(x-r*.92,y+r*.76,x+r*.94,y+r*1.02),'#6d625a',1)
    P(d,pts,'#8e8476',5)
    P(d,[(x-r*.61,y-r*.35),(x-r*.1,y-r*.74),(x+r*.50,y-r*.48),(x+r*.19,y-r*.18)],'#b2a796',2)
    P(d,[(x-r*.61,y-r*.35),(x-r*.73,y+r*.32),(x-r*.14,y+r*.72),(x-r*.30,y+r*.15)],'#756f65',1)
    P(d,[(x+r*.26,y-r*.17),(x+r*.68,y+r*.06),(x+r*.40,y+r*.64),(x+.05*r,y+.46*r)],'#7b756b',1)
    for pts2 in (
        [(x-r*.26,y-r*.12),(x-r*.08,y+r*.12),(x+r*.20,y+r*.19)],
        [(x+r*.23,y-r*.40),(x+r*.12,y-r*.15),(x+r*.38,y+r*.04)],
        [(x-r*.51,y+r*.37),(x-r*.19,y+r*.48),(x-r*.07,y+r*.66)],
    ):L(d,pts2,'#665f5a',3)
    for dx,dy in [(-.47,-.48),(.30,-.29),(-.16,.41)]:
        O(d,(x+r*dx-4,y+r*dy-2,x+r*dx+2,y+r*dy+3),'#c5b4a0',1)
def cyclops(d,x,y,h,t,pose='idle'):
    # Continuous body/limb rig, three times a 1.84 m sailor (visual 5.5 m).
    # One SINGLE centrally mounted eye; every frame has consistent proportions.
    lift=math.sin(t*2.1)*2.5
    x=float(x);y=float(y)+lift
    skin='#bca084'; shadow='#957a66'; dark='#3e3434'; hair='#483938'
    sway=12*math.sin(t*2.0) if pose in ('push','fight','drink') else 2*math.sin(t*1.3)
    # ground contact and giant's stride
    for side in (-1,1):
        hx=x+side*42;ky=y-h*.19
        L(d,[(hx,y-h*.28),(hx+sway*.4,ky),(hx+side*11,y-11)],dark,30)
        L(d,[(hx,y-h*.28),(hx+sway*.4,ky),(hx+side*11,y-11)],skin,23)
        O(d,(hx+side*11-26,y-18,hx+side*11+24,y+5),'#765b49',4)
    # Rough wool kilt, bronze age hand drawn folds
    P(d,[(x-74,y-h*.42),(x+75,y-h*.42),(x+87,y-h*.21),(x-81,y-h*.21)],'#74664f',4)
    for k in range(7):L(d,[(x-60+k*20,y-h*.35),(x-55+k*19,y-h*.23)],'#ad9874',3)
    # shoulders + torso
    P(d,[(x-60+sway,y-h*.66),(x+57+sway,y-h*.66),(x+64,y-h*.38),(x-69,y-h*.38)],skin,5)
    O(d,(x-45,y-h*.55,x+47,y-h*.39),shadow,0)
    # Neck, head oval, sculpted hair, single giant eye, nose and mouth
    L(d,[(x-5+sway,y-h*.69),(x-5+sway,y-h*.79)],skin,37)
    O(d,(x-70+sway,y-h*.96,x+70+sway,y-h*.61),skin,5)
    P(d,[(x-70+sway,y-h*.83),(x-71+sway,y-h*.94),(x-22+sway,y-h*1.015),(x+59+sway,y-h*.97),(x+70+sway,y-h*.84),(x+41+sway,y-h*.87),(x-5+sway,y-h*.91)],hair,3)
    ey=x+sway;yeye=y-h*.81
    O(d,(ey-23,yeye-18,ey+23,yeye+19),'#e6dccb',4)
    O(d,(ey-9,yeye-12,ey+9,yeye+10),'#705044',2)
    O(d,(ey-4,yeye-6,ey+3,yeye+7),'#28262a',1)
    L(d,[(ey-27,yeye-24),(ey+27,yeye-24)],dark,7)
    L(d,[(ey-20,yeye+49),(ey+19,yeye+54)],'#5e4141',4)
    # Long arms track intended actions; elbow and wrist are not disconnected.
    for side in (-1,1):
        sx=x+side*57+sway;sy=y-h*.63
        if pose=='push':tx=x-158 if side<0 else x-116;ty=y-h*(.61 if side<0 else .43)
        elif pose=='drink':tx=x+side*35;ty=y-h*.88 if side>0 else y-h*.45
        elif pose=='fall':tx=x+side*105;ty=y-h*.35
        elif pose=='fight':tx=x+side*112;ty=y-h*.70
        else:tx=x+side*95;ty=y-h*.39
        ex=(sx+tx)/2+side*20;ey2=(sy+ty)/2-5
        L(d,[(sx,sy),(ex,ey2),(tx,ty)],dark,27)
        L(d,[(sx,sy),(ex,ey2),(tx,ty)],skin,20)
        O(d,(tx-15,ty-13,tx+15,ty+13),skin,4)

def original_odysseus(x,feet,height,t,action='idle'):
    # ART LOCK: every pixel belongs to the approved Trojan Horse original hero.
    # ONLY joint rotation, transparent cutouts and timed posing. No redraw.
    phi=math.tau*1.15*t
    walking=action in ('walk','run','escape','approach')
    swing=math.sin(phi) if walking else 0
    bob=abs(math.sin(phi))*(3.6 if walking else 0)
    angles={
       'cape':-(4*math.sin(t*2.2)+6*swing),
       'leg_left':18*swing if walking else (-14 if action=='push' else 0),
       'leg_right':-18*swing if walking else (12 if action=='push' else 0),
       'torso':3*math.sin(phi) if walking else (-7 if action=='push' else 0),
       'left_arm':-14*swing if walking else (32 if action in ('offer','fight','aim','embrace') else -25 if action=='push' else -13),
       'right_arm':14*swing if walking else (-60 if action in ('draw','aim') else 25 if action=='push' else -43 if action in ('offer','embrace') else 23*math.sin(t*5) if action=='fight' else 11),
       'head':-2*math.sin(t*1.1)
    }
    if action in ('kneel','sleep'):
        angles['leg_left']=-38;angles['leg_right']=17
    if action=='pull':angles['left_arm']=-30;angles['right_arm']=-20
    sprite=Image.new('RGBA',pup.ORIGINAL.size)
    for part in ('cape','leg_left','leg_right','torso','left_arm','right_arm','head'):
        sprite.alpha_composite(_cached_rotated(part,int(round(angles[part]/2)*2)))
    ww=max(1,round(height*pup.W/pup.H));hh=max(1,round(height))
    sprite=sprite.resize((ww,hh),Image.Resampling.BILINEAR)
    v.CANVAS.paste(sprite,(round(x-ww/2),round(feet-height+bob)),sprite)

def man(d,x,y,h,t,pose='walk',role='sailor'):
    if role in ('cyclops','giants'):
        return cyclops(d,x,y,h,t,pose)
    if role=='odysseus':
        return original_odysseus(x,y,h,t,pose)
    return act(d,x,y,h,role,t,pose)
def sea(d,t,storm=False,level=685):
    color='#294d67' if storm else '#41718a';R(d,(0,level,W,H),color,1)
    waves(d,t,level+26)
    for k in range(8):
        yy=level+45+k*31
        xx=(k*79+int(t*43))%680-90
        L(d,[(xx,yy),(xx+45,yy-4)],'#7babb4',2)
def ship(d,x,feet,size,t,storm=False,sail=True):
    # Rowing galley with waterline, mast, sail, oars and proportional passengers
    v.side_ship(d,x,feet,size,t,show_sail=sail)
    sc.ship(d,x,feet-20,size/190,t) if size>170 else None
    for k in range(4):
        ang=math.sin(t*5.1+k)*21
        L(d,[(x-55+k*37,feet-25),(x-64+k*40+ang,feet+18)],'#b59167',5)
    waves(d,t,feet+16,int(x))
def staff(d,x1,y1,x2,y2,c='#c8a67c',w=7):L(d,[(x1,y1),(x2,y2)],c,w)
def cup(d,x,y,size=27,angle=0):
    P(d,[(x-size*.7,y-size*.3),(x+size*.7,y-size*.3),(x+size*.45,y+size*.6),(x-size*.43,y+size*.6)],'#cf9f57',2)
    O(d,(x-size*.6,y-size*.5,x+size*.6,y-size*.14),'#7a4042',2)
def bag(d,x,y,size=45,open=False):
    P(d,[(x-size*.4,y-size*.6),(x+size*.4,y-size*.6),(x+size*.62,y+size*.35),(x,y+size*.7),(x-size*.54,y+size*.29)],'#a07551',3)
    L(d,[(x-size*.36,y-size*.53),(x+size*.36,y-size*.53)],'#523a32',5)
    if open:
        for i in range(6):
            a=i*math.pi/3
            L(d,[(x,y-size*.6),(x+65*math.cos(a),y-size*.6-57*math.sin(a))],'#d6eee1',3)
def bow(d,x,y,s,t,p=.1):v.bow(d,x,y,s,t,p)
def axeline(d,x=180,y=780,total=12):
    # Draw all twelve visually instead of 3-4 symbols.
    for k in range(total):
        xx=x+k*24
        L(d,[(xx,y),(xx,y-122)],'#9d7d5c',3)
        O(d,(xx-12,y-140,xx+12,y-117),'#c6a06c',2)
    L(d,[(x-28,y),(x+(total-1)*24+15,y)],'#5e4a3a',4)
def sheep(d,x,y,s,t):v.sheep(d,x,y,s,t)
def pig(d,x,y,s,t):v.pig(d,x,y,s,t)
def tree(d,x,y,s,t):v.orchard_tree(d,x,y,s,t)
def dog(d,x,y,s,t,up=False):v.dog(d,x,y,s,t,raise_head=up)
def horse(canvas,x,y,w,t,hatch=0):
    v.CANVAS=canvas;v.SCALE=1
    v.horse_original(x,y,w,t)
    if hatch:
        d=ImageDraw.Draw(canvas)
        R(d,(x-10,y-w*.49,x+25,y-w*.32),'#413335',2)
        L(d,[(x+4,y-w*.33),(x+26,y-14)],'#a3754c',4)
        L(d,[(x+21,y-w*.34),(x+46,y-14)],'#a3754c',4)
        for k in range(4):L(d,[(x+5+k*5,y-w*.34+k*w*.08),(x+31+k*5,y-w*.34+k*w*.08)],'#dab17a',3)
def glyph_rune(d,x,y):
    L(d,[(x,y),(x+11,y+24),(x-12,y+43)],'#9c8568',4)

def BGSHOT(i):
    shot=SHOTS[i];scene=shot['scene']-1;beat=shot['beat']-1
    # Use connected scene setting for story continuity but physically distinct
    # set dressing and camera framing for each unique beat.
    n=sum(s['scene']==shot['scene'] for s in SHOTS)
    stage=min(3,int((beat+.18)*4/n))
    setting=v.SETS[scene][stage]
    img=sc.paint_background(scene,stage,setting,1)
    d=ImageDraw.Draw(img)
    if scene==3:
        # consistent shared cave geography, with the same arch and rock wall
        for x in (35,501):
            P(d,[(x-35,750),(x,726),(x+15,778),(x+3,838)],'#8b8478',2)
    if scene==6:
        for k in range(6):
            O(d,(k*110,690,65+k*110,728),'#3f5b68',1)
    if scene==15 and beat<=1:
        # Stable rooted olive-bed position for the recognition proof.
        sc.olive_bed(d,340,763,214)
    if scene==4 and beat==3:
        for k in range(3):boulder(d,135+k*142,676,27)
    if scene==8 and beat<3:
        # fixed left Charybdis, fixed right Scylla, never teleport cliffs
        P(d,[(0,330),(107,290),(145,490),(145,750),(0,800)],'#766e67',3)
        P(d,[(W,305),(412,250),(375,480),(379,750),(W,800)],'#6e6c63',3)
    if scene==12 and beat in (1,2):sc.side_loom(d,348,792,0,beat==2,.4)
    if scene==1 and beat in (0,1,2):
        # Troy masonry landmarks remain same in all 3 crossing shots
        for x in (62,459):
            R(d,(x-20,345,x+20,773),'#a58a6a',3)
    return img

def build_backgrounds():
    for i in range(len(SHOTS)):
        BG[i]=BGSHOT(i)
    return len(BG)

def action(d,canvas,i,p,t):
    shot=SHOTS[i];s=shot['scene'];b=shot['beat'];u=E(p)
    feet=775
    # Main performance: 68 separate motivated actions, none reused as a scene.
    if s==1:
        if b==1:
            man(d,270,788,246,t,'hold','beggar');bow(d,360,582,175,t,.02+u*.10)
            L(d,[(290,616),(360,573)],SKIN,8)
        elif b==2:
            man(d,138,786,224,t,'drink','suitor');man(d,401,786,230,t,'drink','suitor2')
            cup(d,178,575-75*u,42);cup(d,363,574-62*u,36)
        elif b==3:
            man(d,208,783,284,t,'draw','beggar');axeline(d,307,769,12)
            bow(d,294,575,196,t,.22+.64*u);L(d,[(276,567),(313+25*u,573)],SKIN,7)
        else:
            man(d,260,787,310,t,'aim','beggar');bow(d,358,555,207,t,.85)
            for x in (100,425):flame(d,x,395,t,1.0)
    elif s==2:
        if b==1:
            horse(canvas,M(118,297,u),779,338,t)
            man(d,M(384,436,u),795,122,t,'walk','trojan')
            L(d,[(310+150*u,739),(390+55*u,726)],STRAW,4)
        elif b==2:
            horse(canvas,M(165,350,u),773,338,t)
            man(d,400,788,110,t,'pull','trojan')
            for k,x in enumerate((166,370)):
                R(d,(x-7,485,x+9*(1-u),740),'#6d4a39',2)
        elif b==3:
            horse(canvas,230,778,370,t,hatch=1)
            man(d,M(235,354,u),M(710,790,u),156,t,'walk','odysseus')
            man(d,M(189,326,u),M(664,785,u),146,t,'walk','sailor')
        else:
            sea(d,t,False,692);ship(d,M(150,370,u),720,112,t)
            for k,x in enumerate((80,158,472)):
                flame(d,x,668,t,1.3);smoke(d,x,599,t,.8)
    elif s==3:
        if b==1:
            man(d,M(434,270,u),778,236,t,'run','odysseus');man(d,M(85,190,u),778,222,t,'fight','trojan')
            man(d,M(470,368,u),779,196,t,'fall','sailor');staff(d,240,668,355,589)
        elif b==2:
            sea(d,t,False,718);ship(d,M(370,266,u),745,122,t)
            man(d,M(70,237,u),786,194,t,'run','odysseus');man(d,M(44,184,u),786,180,t,'walk','sailor')
        elif b==3:
            tree(d,100,783,50,t);tree(d,448,793,46,t)
            man(d,285,783,229,t,'offer','sailor');man(d,92,785,211,t,'approach','odysseus')
            O(d,(302+21*u,540,332+21*u,567),'#e8c29c',2);L(d,[(309,554),(320,585)],'#678367',2)
        else:
            man(d,M(379,263,u),785,226,t,'pull','sailor');man(d,M(136,248,u),782,238,t,'pull','odysseus')
            L(d,[(263+12*u,613),(310+24*u,623)],SKIN,8);ship(d,476,785,56,t,False)
    elif s==4:
        if b==1:
            # reveal cave and giant at the same floor baseline, ~3:1 height
            man(d,M(110,181,u),790,151,t,'approach','odysseus')
            man(d,M(64,106,u),790,145,t,'walk','sailor')
            man(d,420,790,425,t,'idle','cyclops')
        elif b==2:
            # Giant shifts bodyweight and uses TWO hands touching the boulder
            xx=M(485,274,u)
            man(d,430-42*u,797,407,t,'push','cyclops')
            boulder(d,xx,650,149)
            for yy in (548,608):L(d,[(403-42*u,yy),(xx+136,yy+12)],SKIN,13)
            man(d,94,791,142,t,'escape','odysseus')
        elif b==3:
            man(d,130+25*u,788,185,t,'offer','odysseus');man(d,401,785,423,t,'hold','cyclops')
            cup(d,M(252,362,u),M(632,537,u),58)
            L(d,[(225+25*u,633),(M(252,362,u),M(632,537,u))],SKIN,7)
        elif b==4:
            man(d,406,795,395-38*u,t,'drink' if u<.8 else 'fall','cyclops')
            cup(d,355+23*u,474+90*u,67)
            flame(d,90,683,t,1.15);man(d,124,791,172,t,'hold','odysseus')
        elif b==5:
            man(d,404,787,406,t,'fall','cyclops')
            for k,x in enumerate((104,181,256)):
                man(d,x+22*u,789,163,t,'pull','odysseus' if k==0 else 'sailor')
            L(d,[(133,607),(M(257,408,u),469)],'#8e563b',20)
            L(d,[(133,607),(M(257,408,u),469)],'#efad6b',7)
            flame(d,118,619,t,.65)
        elif b==6:
            for k in range(3):sheep(d,M(83+150*k,176+150*k,u),780,100,t+k*.5)
            man(d,114+62*u,775,112,t,'escape','odysseus')
            man(d,465,785,360,t,'hold','cyclops')
        elif b==7:
            sea(d,t,False,691);ship(d,M(198,357,u),744,132,t)
            man(d,258+58*u,716,151,t,'offer','odysseus');man(d,57,741,135,t,'hold','sailor')
        else:
            sea(d,t,True,699);man(d,386,790,429,t,'fight','cyclops')
            for q in range(7):
                a=q*math.tau/7+t*1.5
                L(d,[(390,500),(390+75*math.cos(a),500-78*math.sin(a))],'#b5c6be',2)
    elif s==5:
        if b==1:
            man(d,386,785,259,t,'offer','aiolos');man(d,152,785,230,t,'hold','odysseus')
            bag(d,M(382,258,u),602,62)
        elif b==2:
            ship(d,274,755,116,t);man(d,230,754,152,t,'sleep','odysseus')
            for x in (345,416):man(d,x,751,142,t,'offer','sailor')
            bag(d,375,655,50,open=u>.42)
        elif b==3:
            sea(d,t,True);ship(d,M(381,150,u),738,132,t,storm=True)
            for k in range(6):L(d,[(k*110+int(t*100)%100,484),(k*105+87,426)],'#d9ebe4',3)
        else:
            sea(d,t,True);ship(d,M(95,311,u),761,113,t,storm=True)
            for k in range(3):
                boulder(d,M(92+160*k,256+140*k,u),M(392+k*28,677+k*15,u),38)
                man(d,32+230*k,780,325,t,'fight','cyclops')
    elif s==6:
        if b==1:
            man(d,360,785,252,t,'offer','circe');man(d,153,784,207,t,'drink','sailor')
            cup(d,M(360,241,u),595,51)
        elif b==2:
            man(d,390,788,252,t,'hold','circe');man(d,155,789,216-140*u,t,'fall','sailor')
            pig(d,280+70*u,793,10+85*u,t);rays(d,280,602,t)
        elif b==3:
            man(d,373,781,260,t,'offer','hermes');man(d,146,787,238,t,'hold','odysseus')
            L(d,[(286,583),(210+55*u,619)],'#72916e',9)
            for k in range(3):O(d,(275+k*9,568,287+k*9,580),'#9bbb7a',1)
        else:
            man(d,420,785,246,t,'offer','circe');man(d,110,782,234,t,'hold','odysseus')
            man(d,M(320,250,u),785,100+118*u,t,'approach','sailor');rays(d,287,590,t)
    elif s==7:
        if b==1:
            sea(d,t,False);ship(d,M(399,250,u),741,126,t);smoke(d,112,559,t,1.7)
        elif b==2:
            man(d,197,786,237,t,'kneel','odysseus');man(d,397,788,263,t,'offer','tiresias')
            L(d,[(336,600),(268,600)],'#aab7b5',4)
        elif b==3:
            man(d,M(127,228,u),782,246,t,'approach','odysseus');man(d,397,783,260,t,'hold','mother')
        else:
            man(d,M(158,290,u),785,250,t,'embrace','odysseus');man(d,M(413,328,u),785,246,t,'embrace','mother')
            # translucent spectral embrace: hands appear to pass, no contact
            O(d,(304,577,327,606),'#718c9a',1)
    elif s==8:
        if b==1:
            ship(d,260,749,132,t)
            for x in (120,404):man(d,x,743,142,t,'hold','sailor')
            O(d,(130,585,143,604),'#e8d3a1',1);O(d,(409,585,422,604),'#e8d3a1',1)
        elif b==2:
            ship(d,275,745,140,t)
            man(d,281,733,185,t,'pull','odysseus')
            for x in (254,316):L(d,[(x,551),(x+8,729)],STRAW,7)
            man(d,134,739,140,t,'hold','sailor')
        elif b==3:
            for x,y in ((105,789),(272,772),(445,780)):
                man(d,x,y,230,t,'offer','siren')
                for k in range(3):rays(d,x+45,540+k*18,t,'#cedad0')
        else:
            sea(d,t,False);ship(d,M(155,385,u),755,142,t)
            man(d,270,737,160,t,'pull','odysseus')
    elif s==9:
        if b==1:
            sea(d,t,True,663);ship(d,292,751,128,t,storm=True)
            for k in range(6):
                xx=422+k*9;L(d,[(xx,681),(xx-14+math.sin(t*5+k)*14,474)],'#587268',10)
                O(d,(xx-30,458,xx,481),'#66856c',2)
            for r in range(5):
                rr=35+16*r;d.arc((100-rr,709-rr*.2,100+rr,709+rr*.2),20,330,fill='#8fbdc3',width=4)
        elif b==2:
            sea(d,t,True,697);ship(d,M(285,341,u),739,150,t,storm=True)
            L(d,[(W-150,400),(W-185,760)],'#7c8076',28)
        elif b==3:
            ship(d,287,750,137,t)
            for k in range(6):
                xx=470-19*k;hx=xx-190*u+16*math.sin(t*3+k)
                L(d,[(xx,705),(hx,505)],'#4b6d5e',12)
                O(d,(hx-14,491,hx+18,527),'#63866d',2)
                if u>.52:man(d,95+55*k,751-85*(u-.52),92,t,'fall','sailor')
        else:
            ship(d,268,759,155,t)
            man(d,278,730,177,t,'kneel','odysseus')
            for k in range(4):L(d,[(122+k*65,764),(122+k*65,815)],'#9f795d',4)
    elif s==10:
        if b==1:
            for k in range(7):
                x=46+(k%4)*125;y=742-(k//4)*82
                O(d,(x-37,y-52,x+23,y-8),'#e4d9b1',2);O(d,(x+17,y-60,x+45,y-34),'#cab991',2)
            man(d,85,781,220,t,'hold','sailor')
        elif b==2:
            man(d,397,787,227,t,'kneel','sailor');man(d,M(50,218,u),781,242,t,'run','odysseus')
            for x in (282,376):flame(d,x,728,t,1.15)
        elif b==3:
            sea(d,t,True,661);ship(d,281,753,160,t,True)
            P(d,[(277,210),(254,442),(303,442),(231,757),(357,468),(294,478)],'#f9dfaa',2)
            smoke(d,300,600,t,1.6)
        else:
            sea(d,t,True,668);L(d,[(65,700),(450,759)],'#866144',23)
            man(d,M(130,283,u),748,161,t,'pull','odysseus')
            for k in range(5):waves(d,t,730,21*k)
    elif s==11:
        if b==1:
            man(d,230,778,230,t,'sleep','odysseus');man(d,398,786,236,t,'kneel','calypso')
            tree(d,88,776,55,t)
        elif b==2:
            man(d,196,784,244,t,'kneel','odysseus');man(d,387,785,251,t,'offer','calypso')
            sea(d,t,False,817)
        elif b==3:
            man(d,373,781,255,t,'hold','hermes');man(d,145,787,216,t,'hold','calypso')
            staff(d,355,630,396,567)
            man(d,275,786,214,t,'hold','odysseus')
        else:
            man(d,145,785,235,t,'pull','odysseus')
            for k in range(5):L(d,[(188+k*27,748),(191+k*28,815)],WOOD,13)
            ship(d,M(245,409,u),795,118,t,False)
    elif s==12:
        if b==1:
            man(d,M(155,240,u),785,216,t,'kneel','odysseus');man(d,395,788,250,t,'offer','nausicaa')
            tree(d,458,775,45,t)
        elif b==2:
            man(d,191,779,258,t,'hold','odysseus');man(d,386,786,250,t,'offer','suitor2')
            cup(d,280,640,68);sc.banquet_table(d,279,756,340)
        elif b==3:
            sea(d,t,False,703);ship(d,M(166,351,u),744,133,t)
            man(d,271,734,138,t,'sleep','odysseus')
        else:
            man(d,M(190,285,u),785,260,t,'kneel','odysseus')
            O(d,(240,766,302,795),'#dac296',1)
    elif s==13:
        if b==1:
            sc.banquet_table(d,278,780,365)
            for k,x in enumerate((92,199,369,470)):
                man(d,x,765,180,t,'drink','suitor' if k%2 else 'suitor2');cup(d,x+18,588-34*u,31)
            man(d,285,785,216,t,'hold','penelope')
        elif b==2:
            man(d,140,785,241,t,'weave','penelope');sc.side_loom(d,345,793,t,False,u)
        elif b==3:
            man(d,168,784,240,t,'weave','penelope');sc.side_loom(d,350,797,t,True,u)
        else:
            man(d,M(150,253,u),782,240,t,'walk','telemachus')
            man(d,415,784,255,t,'offer','athena')
    elif s==14:
        if b==1:
            man(d,M(119,233,u),782,247,t,'approach','beggar');man(d,393,785,240,t,'hold','telemachus')
            man(d,471,785,205,t,'hold','eumaeus');rays(d,280,572,t,'#ded7c0')
        elif b==2:
            man(d,M(167,268,u),787,261,t,'embrace','odysseus');man(d,M(397,322,u),787,252,t,'embrace','telemachus')
            L(d,[(288,606),(301,609)],SKIN,11)
        elif b==3:
            man(d,M(190,260,u),786,249,t,'kneel','beggar');dog(d,387,784,113,t,up=u<.75)
            if u>.8:L(d,[(379,773),(421,784)],'#5e554d',4)
        else:
            man(d,194,781,259,t,'kneel','beggar');man(d,389,779,224,t,'kneel','eurycleia')
            cup(d,296,764,80);L(d,[(273,776),(241,790)],SKIN,8)
    elif s==15:
        if b==1:
            man(d,150,785,247,t,'draw','suitor');man(d,412,785,231,t,'fight','suitor2')
            bow(d,289,592,184,t,.09)
        elif b==2:
            man(d,166,782,270,t,'aim','beggar');bow(d,287,591,188,t,.80)
            axeline(d,294,771,12)
            if u>.20:L(d,[(270,591),(M(276,508,(u-.2)/.8),591)],GLINT,6)
        elif b==3:
            man(d,261,783,276,t,'fight','odysseus');man(d,M(448,489,u),784,226,t,'fall','suitor')
            bow(d,369,593,153,t,.50);R(d,(50,422,73,749),'#745842',3)
        else:
            man(d,M(186,238,u),784,270,t,'fight','odysseus')
            man(d,M(353,329,u),784,234,t,'fight','telemachus')
            man(d,M(482,452,u),783,195,t,'fall','suitor2')
            staff(d,200,620,371,522,'#a4875a')
    else:
        if b==1:
            sc.olive_bed(d,345,754,224)
            man(d,160,783,250,t,'offer','odysseus');man(d,444,783,240,t,'hold','penelope')
        elif b==2:
            sc.olive_bed(d,345,754,224)
            man(d,M(167,268,u),783,259,t,'embrace','odysseus')
            man(d,M(397,324,u),785,250,t,'embrace','penelope')
            L(d,[(298,606),(309,614)],SKIN,9)
        elif b==3:
            man(d,M(158,247,u),783,251,t,'embrace','odysseus')
            man(d,M(389,317,u),781,213,t,'embrace','laertes')
            man(d,474,782,239,t,'offer','athena');tree(d,80,770,45,t)
        else:
            tree(d,105,777,48,t);tree(d,465,782,46,t)
            for k,(role,h) in enumerate((('odysseus',245),('penelope',236),('telemachus',235))):
                man(d,141+k*124,788,h,t,'idle',role)
            rays(d,425,215,t,'#e7d5aa')
    # Move actual scenic secondary elements per shot: not simulated camera zoom.
    if s in (2,4,5,8,9,10,12):
        for k in range(4):
            y=813+k*27;x=(k*136+int(t*27))%610-50
            L(d,[(x,y),(x+43,y-3)],'#93b9bc',2)

def frame(t):
    i=min(67,bisect.bisect_right(START,t)-1)
    shot=SHOTS[i];t0=shot['start_seconds_estimate'];t1=shot['end_seconds_estimate'];p=max(0,min(1,(t-t0)/(t1-t0)))
    canvas=BG[i].copy()
    v.CANVAS=canvas;v.SCALE=1;v.canon.IMG=canvas;v.canon.SCALE=1
    d=ImageDraw.Draw(canvas)
    action(d,canvas,i,p,t)
    # An unobtrusive film subtitle tied to the original 16 measured voice scenes
    scene=shot['scene']-1
    local=(t-v.T[scene])/(v.T[scene+1]-v.T[scene])
    v.caption(d,scene,max(0,min(.999,local)),1)
    v.canon.IMG=None
    return canvas

def render(opts):
    from hashlib import sha256
    voice=Path(opts.voice)
    if voice.is_file():
        digest=sha256(voice.read_bytes()).hexdigest()
        if digest!='9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667':
            raise RuntimeError('ORIGINAL_RASALGETHI_SHA256_MISMATCH '+digest)
    build_backgrounds()
    out=Path(opts.output);out.parent.mkdir(parents=True,exist_ok=True)
    ff=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(opts.fps),'-i','pipe:0']
    if voice.is_file():ff+=['-i',str(voice)]
    ff+=['-vf',f'scale={opts.width}:{opts.height}:flags=lanczos,setsar=1','-c:v','libx264','-preset','veryfast','-crf',str(opts.crf),'-pix_fmt','yuv420p','-threads','4']
    if voice.is_file():ff+=['-c:a','aac','-ar','48000','-ac','2','-b:a','160k','-shortest']
    else:ff+=['-an']
    ff+=['-movflags','+faststart',str(out)]
    total=math.ceil(220.56*opts.fps)
    if opts.preview_seconds:total=math.ceil(min(220.56,opts.preview_seconds)*opts.fps)
    print('RENDER_BEGIN',len(SHOTS),'shots',total,'frames',opts.width,opts.height,opts.fps,flush=True)
    with subprocess.Popen(ff,stdin=subprocess.PIPE) as enc:
        for f in range(total):
            img=frame(f/opts.fps)
            enc.stdin.write(img.tobytes())
            if f and f%(opts.fps*10)==0:print('RENDER_FRAMES',f,'/',total,flush=True)
        enc.stdin.close();code=enc.wait()
        if code:raise RuntimeError('ffmpeg encoder code '+str(code))
    qc={'filename':out.name,'fps':opts.fps,'width':opts.width,'height':opts.height,
        'scripted_shots':68,'scenes':16,'audio_sha256_verified':voice.is_file(),
        'narration_original':voice.is_file(), 'synced_word_for_word':False,
        'owner_approved':False,'ready_for_publication':False,
        'native_4k':False,'warnings':['68 distinct shot contracts with hand-coded actions','Original audio scene-boundary sync, subtitles phrase-estimated','Still requires owner visual QC']}
    out.with_suffix('.qc.json').write_text(json.dumps(qc,ensure_ascii=False,indent=2))
    print('RENDER_COMPLETE',out,out.stat().st_size,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--voice',default=str(ROOT/'audio.wav'))
    parser.add_argument('--output',default=str(ROOT/'ODISSEIA_V33_2D_68_ACTIONS_QC.mp4'))
    parser.add_argument('--width',type=int,default=720)
    parser.add_argument('--height',type=int,default=1280)
    parser.add_argument('--fps',type=int,default=30)
    parser.add_argument('--crf',type=int,default=23)
    parser.add_argument('--preview-seconds',type=float,default=0)
    render(parser.parse_args())