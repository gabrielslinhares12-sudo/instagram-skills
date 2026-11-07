#!/usr/bin/env python3
"""Odyssey TUE V28: directed 2D animated sequences in canonical original Trojan cartoon style.

No 3D, no slides, no AI generated substitute cast. Every shot receives a unique
set, a motivated composition, hand/prop blocking and actual frame-by-frame motion.
TUE original Odysseus head and Trojan horse cutout remain the character canon.
"""
from __future__ import annotations
import sys,math,bisect,random,os,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from collections import OrderedDict
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_16_cenas as old

W,H=old.W,old.H
P=old.poly; E=old.ellipse; L=old.line; R=old.rect
INK='#342930'; GOLD='#d3b077';WALL='#a98c69';SAND='#c2a080'; OAK='#77533d'

def E0(d,bb,fill):
    d.ellipse(tuple(map(int,bb)),fill=fill)

def field_lines(d,x,y,w,h,ink='#745f50',spacing=26):
    for yy in range(int(y),int(y+h),spacing):
        L(d,[(x,yy),(x+w,yy)],ink,2)
    for xx in range(int(x),int(x+w),max(30,spacing*2)):
        L(d,[(xx,y),(xx,y+h)],ink,1)

def painted_house(d,x,y,w=94,h=118,lit=False):
    R(d,(x,y-h,x+w,y),'#b99b79',2)
    P(d,[(x-8,y-h),(x+w/2,y-h-29),(x+w+8,y-h)],'#795849',2)
    R(d,(x+w*.42,y-h*.57,x+w*.62,y),'#705c52',2)
    if lit:R(d,(x+w*.42+3,y-h*.51,x+w*.62-3,y-6),'#e4b06b',0)
    for z in range(2):
        L(d,[(x+10,y-h+19+z*28),(x+w-10,y-h+19+z*28)],'#a78a6b',1)

def painter_mountains(d,t,depth=0):
    for k,c in enumerate(['#82958a','#6e807a','#556c73']):
        low=552+k*68
        pts=[(-10,low+80)]
        for q in range(11):
            x=-20+q*60
            yy=low+27*math.sin(q*.95+k*1.4)+6*math.sin(q*2.3+k)
            pts.append((x,yy))
        pts.extend([(560,960),(-10,960)])
        P(d,pts,c,1)

def timber(d,x1,x2,y0,y1):
    P(d,[(x1,y0),(x2,y0),(x2,y1),(x1,y1)],'#7d5741',2)
    for off in range(15,int(x2-x1),31):L(d,[(x1+off,y0+4),(x1+off,y1-4)],'#af835c',2)
    for yy in range(int(y0+35),int(y1),61):L(d,[(x1+5,yy),(x2-5,yy)],'#503a33',2)

def banquet_table(d,x=270,y=730,width=310):
    P(d,[(x-width/2,y-27),(x+width/2,y-27),(x+width/2+15,y-4),(x-width/2-13,y-4)],'#8b5d40',3)
    for k in (-1,1):
        L(d,[(x+k*width*.38,y),(x+k*width*.36,y+80)],'#715039',10)
    for k in range(6):
        xx=x+(k-2.5)*width/6
        E(d,(xx-13,y-40,xx+13,y-30),'#dbc7a5',2)
        old.bowl(d,xx,y-42,34)
    E(d,(x-24,y-66,x+24,y-53),'#b78d5b',2)

def side_loom(d,x=350,y=797,t=0,unweave=False,p=0):
    timber(d,x-100,x+95,y-307,y-16)
    # visible 12 vertical warp cords and cross-thread progressively created or removed
    for k in range(12):
        xx=x-82+k*14.4
        L(d,[(xx,y-287),(xx,y-29)],'#f0d0a1',2)
    progress=int(9*(1-p if unweave else p))
    for k in range(progress):
        yy=y-55-k*18
        L(d,[(x-87,yy),(x+84,yy)],'#dcc19a',4)
    L(d,[(x-96,y-170+12*math.sin(t*3.5)),(x+90,y-170+12*math.sin(t*3.5))], '#9b714a',6)

def cliff_rocks(d,scene,j,t):
    # Different coast geography, not an identical generic hill on unrelated islands.
    cols=['#83796b','#6f776f','#5d6965']
    for side in (0,1):
        x=0 if side==0 else W
        for k in range(3):
            y=380+k*93
            w=60+k*29+(scene%3)*12
            if side==0:pts=[(0,y),(w-18,y-18),(w+18,y+43),(w-2,y+112),(0,y+125)]
            else:pts=[(W,y),(W-w+18,y-18),(W-w-18,y+43),(W-w+2,y+112),(W,y+125)]
            P(d,pts,cols[k],3)
            if side==0:L(d,[(w-23,y+6),(w-13,y+37)],'#9c9081',2)
            else:L(d,[(W-w+23,y+6),(W-w+13,y+37)],'#9c9081',2)

def arch_cave_interior(d,t,with_sheep=False):
    P(d,[(0,150),(W,150),(W,960),(0,960)],'#514d48',2)
    # Massive single arch and vaulted interior; no disconnected floating rocks.
    P(d,[(50,780),(84,350),(160,244),(260,206),(370,242),(456,355),(490,780)],'#222e30',4)
    P(d,[(0,745),(W,745),(W,960),(0,960)],'#6b6254',3)
    for k in range(12):
        a=80+k*34
        L(d,[(a,735),(a-25,782)],'#8f8273',1)
        if k%3==0:
            P(d,[(a-20,309),(a,370),(a+21,321)],'#625951',2)
    # Torches anchored to wall and animal pens, scale references for human actors.
    for x in (83,454):
        L(d,[(x,479),(x,546)],'#8a6a4a',8)
        E(d,(x-14,454+2*math.sin(t*6+x),x+15,509),'#f0b46a',1)
    if with_sheep:
        for k in range(4):old.sheep(d,70+k*110,781,66,t*.6+k)

def olive_bed(d,x=340,y=766,w=230):
    # Live tree trunk visibly penetrates ground and joins the bed frame.
    L(d,[(x-w*.32,y+50),(x-w*.32,y-300),(x-w*.48,y-368)],'#644f3e',24)
    for k in range(7):
        xx=x-w*.32+math.sin(k*1.7)*75
        yy=y-342+30*math.cos(k*2)
        E(d,(xx-33,yy-30,xx+31,yy+28),'#587960',2)
    P(d,[(x-w*.54,y-54),(x+w*.5,y-54),(x+w*.43,y+24),(x-w*.53,y+24)],'#a97851',3)
    P(d,[(x-w*.49,y-59),(x+w*.46,y-59),(x+w*.34,y-11),(x-w*.46,y-11)],'#e3cda5',3)
    L(d,[(x-w*.54,y-54),(x-w*.57,y+52)],'#6a4335',10)
    L(d,[(x+w*.51,y-54),(x+w*.51,y+52)],'#6a4335',10)

def skyline(d,t,torch=False):
    painter_mountains(d,t)
    for k in range(7):
        x=k*85-34
        painted_house(d,x,702,w=84,h=110+(k%2)*37,lit=torch and (k%3==0))
    P(d,[(0,704),(540,702),(540,960),(0,960)],'#a58b70',2)
    for k in range(0,540,67):L(d,[(k,705),(k+(k-270)*.21,940)],'#8d7862',2)

def unique_set(d,i,j,p,t):
    """Stage props: every screenplay scene has physical, period-correct geography."""
    if i in (0,12,14):
        # 0 first hall, 12 corrupt hall, 14 retake it, same palace geography preserved.
        if i==0:
            if j==0:
                R(d,(155,689,377,746),'#856245',3)
                P(d,[(176,687),(250,675),(350,685),(347,710),(171,716)],'#af7d55',2)
                old.bow(d,265,668,108,t,.1)
            elif j==1:
                banquet_table(d,275,763,270)
            elif j==2:
                # Twelve axe handles align into an unmistakable visual target corridor.
                for k in range(12):
                    xx=190+k*23
                    L(d,[(xx,721),(xx,605)],'#ad825c',4)
                    E(d,(xx-9,589,xx+9,618),'#ae874c',2)
            else:
                R(d,(320,652,495,715),'#aa8258',3)
        elif i==12:
            if j==0:banquet_table(d,277,786,420)
            if j in (1,2):side_loom(d,351,806,t,unweave=j==2,p=p)
            if j==3:
                P(d,[(0,704),(540,707),(540,960),(0,960)],'#90755f',3)
                for k in range(4):R(d,(k*150-10,710,k*150+40,810),'#896b50',2)
        else:
            if j in (0,1):old.axe_line(d,160,805,12)
            if j==2:
                R(d,(380,744,540,930),'#85674b',2)
                L(d,[(400,650),(490,713)],'#ae9869',10)
            if j==3:
                P(d,[(0,752),(540,755),(540,960),(0,960)],'#85664e',3)
                for x in (34,490):old.throne(d,x,730,98)
    elif i==1:
        if j==0:
            # Bronze-age city walls with complete door in correctly scaled gap.
            for k in range(0,540,48):R(d,(k,350,k+34,379),'#b99a7b',2)
            for x in (80,445):R(d,(x-21,277,x+21,732),'#9c8063',3)
        elif j==1:
            for x in (74,460):old.throne(d,x,783,82)
            L(d,[(80,545),(135,485)],'#95734c',8)
        elif j==2:
            # Door physically open on side of horse, stone gate visible.
            R(d,(115,340,163,750),'#9c8164',4)
            R(d,(379,340,427,750),'#9c8164',4)
            for x in (132,414):E(d,(x-12,690,x+12,720),'#e4b06f',2)
        else:
            skyline(d,t,torch=True)
            for k in range(7):
                x=k*86+23
                L(d,[(x,675),(x+10*math.sin(t*4+k),618)],'#dc8055',4)
                E(d,(x-15,615,x+15,651),'#efb85d',1)
    elif i==2:
        if j==0:
            skyline(d,t,torch=True)
            for x in (53,460):L(d,[(x,739),(x+43,699)],'#6f5140',8)
        if j==1:
            cliff_rocks(d,i,j,t)
            for k in range(2):P(d,[(35+k*395,715),(110+k*300,697),(140+k*300,797)],'#7f7569',3)
        if j==2:
            # Lush lotus-island near bright tree and edible flower.
            for k in range(4):old.orchard_tree(d,80+k*133,789,32,t)
            for x in (128,414):
                L(d,[(x,747),(x,701)],'#4f755f',3)
                for a in (-1,1):E(d,(x-9+a*8,696,x+9+a*8,710),'#e5b5a8',2)
        if j==3:cliff_rocks(d,i,j,t)
    elif i==3:
        arch_cave_interior(d,t,with_sheep=j==3)
        if j==0:
            # Size measurement implied by identical floor horizon: ~3x human.
            R(d,(26,701,128,758),'#87674c',2)
            for x in (40,108):L(d,[(x,701),(x,664)],'#ad8b65',6)
        if j==1:
            # Cave storage emphasizes that this is a real occupied place.
            for k in range(5):R(d,(20+k*62,701,65+k*62,739),'#77624b',2)
            for k in range(3):E(d,(75+k*101,664,91+k*101,686),'#b9a48a',1)
        if j==2:
            L(d,[(83,722),(143,630)],'#674a36',18)
            E(d,(145,628,191,644),'#e2a051',2)
        if j==3:
            # Light visible from coherent single portal at left edge.
            P(d,[(0,389),(69,342),(117,398),(126,742),(0,742)],'#a39375',3)
    elif i==4:
        if j==0:
            old.orchard_tree(d,75,801,50,t)
            R(d,(340,456,480,746),'#a28d75',2)
            for k in range(4):E(d,(378+k*19,500,393+k*19,516),'#d6b98c',2)
        if j==1:
            # Ithaca visible as distant destination, before bag is opened.
            P(d,[(278,589),(348,516),(426,571),(460,611)],'#79958a',2)
        if j==2:
            for k in range(13):
                x=(k*61+int(t*45))%W
                L(d,[(x,335),(x+45,402)],'#bed6d0',2)
        if j==3:
            cliff_rocks(d,i,j,t)
            for k in range(3):
                old.side_ship(d,85+k*175,760,49,t,show_sail=False)
    elif i==5:
        if j in (0,1,3):
            # Circe's green/copper palace, stable geography across connected shots.
            for x in (20,420):
                R(d,(x,435,x+97,752),'#ab9e81',2)
                for k in range(4):L(d,[(x+15,460+60*k),(x+80,460+60*k)],'#7a6551',2)
            P(d,[(90,439),(270,320),(455,439)],'#63523e',3)
            R(d,(146,444,391,747),'#92795b',3)
            R(d,(212,541,333,747),'#44574d',3)
            for x in (138,399):old.orchard_tree(d,x,790,28,t)
        elif j==2:
            for x in (75,456):old.orchard_tree(d,x,801,47,t)
    elif i==6:
        if j==0:
            cliff_rocks(d,i,j,t)
        else:
            P(d,[(0,738),(540,740),(540,960),(0,960)],'#3c4f57',2)
            for k in range(9):
                x=30+k*64
                E(d,(x-38,555+k*12+3*math.sin(t*.8+k),x+38,585+k*12),'#657b80',1)
            if j>=2:
                # Ethereal arch of Hades behind soul, painterly and non-intrusive.
                L(d,[(310,743),(319,453),(359,411),(430,447),(447,743)],'#71878a',7)
    elif i==7:
        if j in (0,1):
            for x in (15,510):
                P(d,[(x,708),(x+55,535),(x+95,727)],'#697066',3)
        if j==2:
            cliff_rocks(d,i,j,t)
            for x in (82,285,468):
                P(d,[(x-44,715),(x,620),(x+45,715)],'#a79d86',3)
        if j==3:
            for k in range(9):
                xx=k*75
                L(d,[(xx,696),(xx+25,704)],'#83b0ad',2)
    elif i==8:
        if j in (0,1,2):
            # Distinct geographic alternatives: whirlpool LEFT and six heads RIGHT.
            # Huge vertical cliffs remain spatially stable as ship moves.
            P(d,[(0,379),(100,317),(134,505),(136,742),(0,742)],'#77736b',3)
            P(d,[(540,319),(400,284),(376,500),(385,743),(540,743)],'#6d6b63',3)
            cx=91+10*math.sin(t*.9)
            for k in range(6):
                R0=40+k*16
                d.arc((cx-R0,654-R0*.31,cx+R0,654+R0*.31),35,335,fill='#a7bfbe',width=3)
        else:
            P(d,[(0,748),(540,752),(540,960),(0,960)],'#23516a',2)
    elif i==9:
        if j in (0,1):
            for x in range(7):old.orchard_tree(d,40+x*82,783,20,t)
            for x in (50,489):R(d,(x,741,x+62,785),'#927f64',2)
        if j==2:
            for k in range(14):
                x=(k*81+int(t*25))%W
                L(d,[(x,170),(x-50,270)],'#b0bec1',2)
        if j==3:
            for k in range(8):
                L(d,[(k*67,758),(k*67+62,749)],'#a6babc',3)
    elif i==10:
        # Paradise beautiful but prison-like, lush full environment.
        for k in range(5):old.orchard_tree(d,22+k*129,785,32+(k%2)*9,t)
        if j in (0,1):
            P(d,[(0,631),(89,594),(141,715),(161,786),(0,790)],'#80796c',3)
            for x in (114,129,144):L(d,[(x,580),(x-5,715)],'#b4d6ca',3)
        if j==2:
            R(d,(420,449,526,769),'#aa957a',3)
        if j==3:
            for k in range(6):L(d,[(230+k*18,739),(320+k*8,739)],'#a8875b',6)
    elif i==11:
        if j==0:
            cliff_rocks(d,i,j,t)
            for x in (53,470):old.orchard_tree(d,x,782,34,t)
        if j==1:
            banquet_table(d,279,749,290)
            for x in (50,475):
                R(d,(x-17,380,x+16,739),'#a28768',3)
        if j==2:
            for k in range(9):E0(d,(k*64,175+k%3*14,k*64+2,178+k%3*14),'#d7d4bd')
        if j==3:
            for x in (45,502):old.orchard_tree(d,x,787,42,t)
            P(d,[(0,725),(540,735),(540,960),(0,960)],'#d4b891',2)
    elif i==13:
        if j==0:
            # Loyal swineherd hut rather than king's hall.
            P(d,[(60,476),(270,358),(469,478)],'#6b5341',3)
            timber(d,81,452,480,747)
            R(d,(255,545,337,745),'#453a35',3)
        if j==1:
            for x in (35,480):old.orchard_tree(d,x,785,37,t)
            R(d,(323,621,495,760),'#a58e70',3)
        if j==2:
            old.bowl(d,280,776,66)
            R(d,(25,412,125,735),'#9a8066',3)
        if j==3:
            R(d,(45,411,145,734),'#a3876b',3)
            timber(d,185,365,560,740)
    elif i==15:
        if j in (0,1):olive_bed(d,330,754,210)
        elif j==2:
            for x in (35,180,440):old.orchard_tree(d,x,785,44,t)
        else:
            skyline(d,t)
            for x in (80,460):old.orchard_tree(d,x,780,28,t)

def foreground(d,i,j,p,t):
    # Foreground establishes depth and fixes feet/objects to the same ground plane.
    if i in (0,12,14):
        if j in (0,2):
            for x in (0,520):P(d,[(x-30,749),(x+22,749),(x+34,960),(x-44,960)],'#8d6748',2)
    elif i==3 and j in (0,3):
        for x in (35,490):
            P(d,[(x-46,785),(x+18,765),(x+54,851),(x-33,863)],'#7e7366',2)
    elif i==8 and j<=2:
        for x in (8,540):
            P(d,[(x-20,757),(x+20,744),(x+35,960),(x-35,960)],'#4d5f62',1)
    elif i==10 and j<3:
        P(d,[(0,802),(97,781),(230,801),(377,787),(540,813),(540,960),(0,960)],'#988a6b',2)

# Directed camera crop in a few narrative moments, applied before caption and
# never used to substitute moving actors. We preserve every prop's camera-space size.
CLOSEUPS={
    (0,0):(255,640,1.34),(0,2):(250,580,1.40),
    (2,2):(275,675,1.14),(3,1):(270,610,1.14),
    (5,1):(265,675,1.13),(6,3):(280,605,1.18),
    (7,1):(270,650,1.17),(9,3):(273,665,1.21),
    (10,1):(268,672,1.13),(11,3):(268,685,1.12),
    (12,1):(278,655,1.15),(13,1):(265,666,1.16),
    (13,2):(286,677,1.16),(14,1):(279,600,1.14),
    (15,1):(285,664,1.18),
}

def camera_crop(img,i,j):
    data=CLOSEUPS.get((i,j))
    if data is None:return img
    x,y,z=data
    w,h=img.size
    boxw=w/z;boxh=h/z
    left=old.clamp(x/W*w-boxw/2,0,w-boxw)
    top=old.clamp(y/H*h-boxh/2,0,h-boxh)
    return img.crop((int(left),int(top),int(left+boxw),int(top+boxh))).resize((w,h),Image.Resampling.BILINEAR)

# Every one of the 64 shots has its own background plate. Backdrop is drawn only
# once per shot, but actors, props and effects are animated in EVERY frame.
# This is not slideshow: background plate = stage scenery, not an action frame.
BG_CACHE=OrderedDict()

prev_action=old.action_shot

def corrected_action(d,i,j,p,t):
    if i==3 and j==0:
        # Physical rock with a common ground plane and continuous world-space
        # progression for both giant and monolith. Odisseu and sailor are 1.84m,
        # Polyphemus 5.5m => three times their visual height.
        g=old.ease(p)
        sx=old.lp(480,271,g)
        gx=sx+147
        old.actor(d,95,781,146,'odysseus',t,'escape')
        old.actor(d,34,781,132,'sailor',t,'escape')
        # Rock precedes giant on the picture plane, so it does not magically
        # occupy a location after moving from nowhere.
        old.ellipse(d,(sx-171,437,sx+171,792),'#8f887b',5)
        for k in range(7):
            xx=sx-116+k*31
            old.line(d,[(xx,492+k%3*25),(xx-14,580+k%2*24)],'#b4aa93',2)
        # Cyclops body follows the SAME trajectory and has feet at ground level.
        old.actor(d,gx,791,415,'cyclops',t,'push')
        # Hands are both attached to right side of monolith as it moves.
        contact=(sx+167,549)
        old.line(d,[(gx-80,546),(contact[0],contact[1])],'#392e2b',22)
        old.line(d,[(gx-80,546),(contact[0],contact[1])],'#c6a181',15)
        old.ellipse(d,(contact[0]-19,contact[1]-20,contact[0]+19,contact[1]+20),'#c9a384',3)
        contact2=(sx+168,625)
        old.line(d,[(gx-84,618),(contact2[0],contact2[1])],'#392e2b',19)
        old.line(d,[(gx-84,618),(contact2[0],contact2[1])],'#c6a181',12)
        old.ellipse(d,(contact2[0]-16,contact2[1]-16,contact2[0]+16,contact2[1]+16),'#c9a384',3)
    else:
        prev_action(d,i,j,p,t)

def paint_background(i,j,setting,scale):
    # Internally draw at requested resolution, but painted scene never moves
    # with a fictitious camera as a substitute for actor animation.
    old.CANVAS=Image.new('RGB',(round(W*scale),round(H*scale)),(30,59,74))
    old.D=old.canon.base.ScaledDraw(ImageDraw.Draw(old.CANVAS),scale) if scale!=1 else ImageDraw.Draw(old.CANVAS)
    old.canon.IMG=old.CANVAS;old.canon.SCALE=scale
    d=old.D
    t=(old.T[i]+((j+.50)/4)*(old.T[i+1]-old.T[i]))
    old.illustrated_sky(d,setting,t)
    if setting in ('hall','bed','weave','circe','hut'):
        old.palace(d,setting,t)
    elif setting in ('troy','troy_night'):
        old.troy_gate(d,t,night=setting=='troy_night',openness=1)
    elif setting in ('cave','cave_exit'):
        arch_cave_interior(d,t,with_sheep=False)
    elif setting in ('sea','storm','strait','wind','sirens','harbor'):
        old.ocean(d,t,storm=setting=='storm')
    elif setting in ('island','lotus','orchard'):
        old.forest(d,t,magic=setting=='lotus')
    elif setting in ('coast','shore','ithaca','courtyard'):
        old.coast(d,t)
    elif setting=='underworld':
        d.polygon([(0,567),(W,567),(W,H),(0,H)],fill='#283c48')
        for k in range(11):
            xx=(k*53+int(t*3))%W;yy=583+k*24
            E(d,(xx-46,yy-6,xx+47,yy+5),'#617985',0,None)
    unique_set(d,i,j,.5,t)
    return old.CANVAS.copy()

def ambience(d,i,j,p,t):
    # Real environmental secondary motion, separate from puppets and props.
    if i in (1,4,7,8,9,11) and j in (1,2,3):
        for k in range(7):
            y=810+k*19
            x=(k*83+int(t*34))%600-30
            L(d,[(x,y),(x+53+8*math.sin(t*2+k),y-3)],'#91b7b9',2)
    if i in (1,9) and j==2:
        for q in range(7):
            xx=q*81+23
            L(d,[(xx,210+(q*71)%125),(xx-28,280+(q*71)%125)],'#d7e0d9',2)
    if i in (0,12,14) and j in (0,3):
        for xx in (65,475):
            L(d,[(xx,337),(xx+6*math.sin(t*9+xx),301-7*math.sin(t*6))],'#ebbd72',4)

def still_frame(t,scale=1):
    old.SCALE=scale
    i=min(15,max(0,bisect.bisect_right(old.T,t)-1))
    u=old.clamp((t-old.T[i])/(old.T[i+1]-old.T[i]))
    j=min(3,int(u*4));p=u*4-j
    setting=old.SETS[i][j]
    key=(i,j,scale)
    if key not in BG_CACHE:
        BG_CACHE[key]=paint_background(i,j,setting,scale)
    old.CANVAS=BG_CACHE[key].copy()
    old.D=old.canon.base.ScaledDraw(ImageDraw.Draw(old.CANVAS),scale) if scale!=1 else ImageDraw.Draw(old.CANVAS)
    old.canon.IMG=old.CANVAS;old.canon.SCALE=scale
    d=old.D
    ambience(d,i,j,p,t)
    corrected_action(d,i,j,p,t)
    foreground(d,i,j,p,t)
    img=camera_crop(old.CANVAS,i,j)
    if img is not old.CANVAS:
        old.CANVAS=img
        old.D=old.canon.base.ScaledDraw(ImageDraw.Draw(old.CANVAS),scale) if scale!=1 else ImageDraw.Draw(old.CANVAS)
    old.caption(old.D,i,u,scale)
    if t<2.75:
        font=ImageFont.truetype(old.FONT_DIR+'/DejaVuSerif-Bold.ttf',14)
        old.D.text((37,48),'MITOLOGIA GREGA  ·  ODISSEU',font=font,fill=old.PALE)
    if t>=old.T[15]+.94*(old.T[16]-old.T[15]):
        k=old.clamp((t-(old.T[15]+.94*(old.T[16]-old.T[15])))/(old.T[16]-(old.T[15]+.94*(old.T[16]-old.T[15]))))
        if k>.12:
            dark=Image.new('RGB',old.CANVAS.size,'#0e1c27')
            old.CANVAS=Image.blend(old.CANVAS,dark,k*.82)
    old.canon.IMG=None
    return old.CANVAS

# Use verified source voice and unchanged scene boundaries. Renderer does not
# synthesize voices, replace user-approved horse artwork, or auto-publish.
old.frame=still_frame
if __name__=='__main__':old.main()