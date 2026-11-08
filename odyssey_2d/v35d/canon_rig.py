#!/usr/bin/env python3
"""Odyssey: extend the FIRST Trojan Horse film's 2D style, not generic V19.
Articulated 2D production rig, original Odysseus head sampled from the owner's
pre-existing 60s Troy film, all secondary cast uniquely designed in matching
flat hand-drawn style. Private Rasalgethi user narration remains unchanged.
"""
from pathlib import Path
import math,sys,os,subprocess,bisect,random,argparse,json
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parent))
import base_tue as base

SRC_HEAD=Path(__file__).resolve().parent/'assets'/'ODISSEU_CAVALO_TROIA_CABECA_EXATA_RGBA.png'
ORIGINAL_HEAD=Image.open(SRC_HEAD).convert('RGBA')
ORIGINAL_BEGGAR_FACE=Image.open(str(Path(__file__).resolve().parent/'assets'/'ODISSEU_ROSTO_ORIGINAL_SEM_CAPACETE_RGBA.png')).convert('RGBA')
DARK='#34272a'; DEEP='#292a2c'; GOLD='#f2ba67'; BGOLD='#c18a4f'; SKIN='#c58a60'; CREAM='#f3d5a2'; RED='#8d4449'; REDL='#a85a56'; WOOD='#967054'; BROWN='#68513f'; OCRE='#d7b083'; SKY='#31566b'
IMG=None; SCALE=1.0

def P(draw,points,fill,outline=DARK,width=3):
    draw.polygon([(round(x),round(y)) for x,y in points],fill=fill)
    if outline:draw.line([(round(x),round(y)) for x,y in list(points)+[points[0]]],fill=outline,width=max(1,int(width)),joint='curve')
def E(d,xy,color,outline=DARK,width=3):
    d.ellipse(tuple(int(v) for v in xy),fill=color,outline=outline,width=max(1,int(width)))
def L(d,xy,col,width=4):
    d.line([(round(x),round(y)) for x,y in xy],fill=col,width=max(1,int(width)),joint='curve')
def safeclip(v,a,b):return max(a,min(b,v))

# Characters are **not** copies of Odysseus. They share his canonical drawing
# grammar, proportions, thick brown contour, shading, aged-Bronze-age textiles.
CAST={
 'odysseus': dict(skin='#c58a60',hair='#302829',fabric='#b68b57',cloak=RED,armor=True,helmet=True,beard=True,kind='hero',eye='#26242b'),
 'beggar': dict(skin='#c58a60',hair='#302829',fabric='#88806e',cloak='#706456',armor=False,helmet=False,beard=True,kind='hero',eye='#26242b'),
 'penelope': dict(skin='#cfa484',hair='#46332d',fabric='#e0c8a1',cloak='#aa7866',armor=False,helmet=False,beard=False,kind='robe',eye='#35252a',braid=True),
 'telemachus': dict(skin='#bc8e65',hair='#302b30',fabric='#b2a287',cloak='#627d91',armor=False,helmet=False,beard=False,kind='young',eye='#28282c'),
 'suitor': dict(skin='#bc8d68',hair='#4a3129',fabric='#995442',cloak='#6e383d',armor=False,helmet=False,beard=True,kind='tunic',eye='#28282c'),
 'suitor2': dict(skin='#c89c79',hair='#29272b',fabric='#78677f',cloak='#66526f',armor=False,helmet=False,beard=False,kind='tunic',eye='#27252a'),
 'cyclops': dict(skin='#b69a7c',hair='#413534',fabric='#86725c',cloak='#665747',armor=False,helmet=False,beard=True,kind='giant',eye='#332328'),
 'circe': dict(skin='#cc9d7a',hair='#33292e',fabric='#52725c',cloak='#a6794c',armor=False,helmet=False,beard=False,kind='robe',eye='#2d2527',braid=True),
 'calypso': dict(skin='#d5b49a',hair='#6d5143',fabric='#e4d7b4',cloak='#b6bcac',armor=False,helmet=False,beard=False,kind='robe',eye='#3c3131',braid=True),
 'athena': dict(skin='#cca17a',hair='#4b3b34',fabric='#bcab8a',cloak='#7d8f9a',armor=True,helmet=True,beard=False,kind='armor',eye='#888e94'),
 'mother': dict(skin='#bcc7ca',hair='#9a9295',fabric='#afbbc5',cloak='#8ea1ab',armor=False,helmet=False,beard=False,kind='robe',eye='#4c6672',braid=True),
 'laertes': dict(skin='#c19c7a',hair='#d8c9b1',fabric='#8d7e67',cloak='#726c63',armor=False,helmet=False,beard=True,kind='elder',eye='#433b3a'),
 'eurycleia': dict(skin='#beaa8b',hair='#dad1c3',fabric='#c6b89d',cloak='#938677',armor=False,helmet=False,beard=False,kind='elderrobe',eye='#463d3b',braid=True),
 'eumaeus': dict(skin='#b9946e',hair='#5b4b3e',fabric='#938165',cloak='#806c57',armor=False,helmet=False,beard=True,kind='tunic',eye='#44322f'),
 'sailor': dict(skin='#c69c78',hair='#45332e',fabric='#79949b',cloak='#766756',armor=False,helmet=False,beard=False,kind='tunic',eye='#29252b'),
 'trojan': dict(skin='#b99070',hair='#52362f',fabric='#947354',cloak='#ac845c',armor=False,helmet=False,beard=True,kind='tunic',eye='#29252b'),
 'nausicaa': dict(skin='#dfb79b',hair='#80644c',fabric='#d5c1a1',cloak='#94b4b8',armor=False,helmet=False,beard=False,kind='robe',eye='#302e30',braid=True),
 'hermes': dict(skin='#bf9874',hair='#594238',fabric='#bfa26d',cloak='#a98d5f',armor=False,helmet=True,beard=False,kind='tunic',eye='#362c2a'),
 'aiolos': dict(skin='#c4a280',hair='#dfd3bf',fabric='#a8a69b',cloak='#8d9aa1',armor=False,helmet=False,beard=True,kind='elder',eye='#3b3e3f'),
 'tiresias': dict(skin='#b1bbc0',hair='#d6d6d0',fabric='#9daab1',cloak='#798b96',armor=False,helmet=False,beard=True,kind='elder',eye='#546066'),
 'siren': dict(skin='#ceaf94',hair='#292830',fabric='#657979',cloak='#9aafb2',armor=False,helmet=False,beard=False,kind='robe',eye='#362832',braid=True),
}

def actor(d,x,feet,h,role='odysseus',t=0,action='idle',alpha=1,face=1,scale=1):
    """Bone-driven painted rig: real foot support phase and knee/elbow pivots.
    No generic stick rectangles. Model components match original Troy cartoon.
    """
    global IMG,SCALE
    c=CAST.get(role,CAST['sailor']);h*=scale
    x=float(x);feet=float(feet)
    o=max(2,int(h*.016));lw=max(3,int(h*.065))
    moving=action in ('walk','run','escape','approach')
    cyc=math.sin(t*(6.5 if action in ('run','escape') else 4.9)+x*.003)
    stride=(.085 if action in ('run','escape') else .057)*h if moving else 0
    bob=abs(math.sin(t*4.9))*.011*h if moving else math.sin(t*1.15)*.004*h
    crouch=.14*h if action in ('kneel','fall','sleep') else 0
    y=feet-crouch
    forward=(.06*h if action in ('push','fight','pull','draw','aim') else .01*h if moving else 0)
    bodyx=x+forward
    hip=(bodyx, y-.405*h+bob)
    shoulder=(bodyx, y-.685*h+bob)
    stance=base.ease((cyc+1)/2) if moving else 0
    # anchored feet + knees: support leg stays fixed while opposite swings.
    E(d,(x-.19*h,y-.008*h,x+.2*h,y+.02*h),'#3e3b36',outline=None,width=1)
    for side in (-1,1):
        phase=cyc*side
        fw=side*.094*h+(stride*phase if moving else 0)
        lift=stride*.42*max(0,phase) if moving else 0
        foot=(x+fw,y-lift)
        kneex=hip[0]+side*.10*h+fw*.22+(stride*.13 if moving else 0)
        kneey=y-.227*h+lift*.36
        # shin and thigh outlined shapes resembling original bronze greaves.
        legcolor='#c28e59' if c['armor'] else ('#896749' if c['kind']=='giant' else '#a58a6c')
        L(d,[hip,(kneex,kneey),foot],DARK,lw+o*2)
        L(d,[hip,(kneex,kneey),foot],legcolor,lw)
        L(d,[(kneex-o,kneey+.018*h),(foot[0],foot[1]-.035*h)],'#e3b378' if c['armor'] else '#d3aa86',max(1,int(lw*.32)))
        P(d,[(foot[0]-.07*h,foot[1]-.026*h),(foot[0]+.050*h,foot[1]-.042*h),(foot[0]+.11*h,foot[1]+.002*h),(foot[0]-.063*h,foot[1]+.002*h)],DEEP,width=o)
    # flowing behind-body cape, same rust-red tonal folds as Trojan hero.
    w=.022*h*math.sin(t*2.3)
    if c['kind'] not in ('robe','elderrobe','giant'):
        P(d,[(shoulder[0]-.17*h,shoulder[1]+.015*h),(shoulder[0]-.055*h,shoulder[1]+.04*h),(x+.02*h-w,y-.14*h),(x-.37*h+w,y-.17*h),(x-.29*h+w,y-.40*h)],c['cloak'],width=o+1)
        P(d,[(x-.23*h,y-.29*h),(x-.32*h+w,y-.17*h),(x-.11*h,y-.23*h)],REDL if c['kind']=='hero' else c['cloak'],outline=None)
    # rear arm, skinned wrist and elbow in genuine joint chain.
    def arm(side,front=False):
        ox=shoulder[0]+side*.17*h;oy=shoulder[1]+.04*h
        gesture=action in ('hold','offer','draw','aim','push','fight','drink','weave','embrace','pull')
        if action=='push':
            # Both arms physically reach the rock on the LEFT; no mirrored waving.
            elbow=(bodyx-.16*h+side*.035*h,oy-.012*h)
            hand=(bodyx-.32*h+side*.017*h,oy-.018*h)
        elif action=='pull':
            elbow=(ox+side*.095*h,oy+.045*h)
            hand=(ox+side*.17*h,oy+.015*h)
        elif action in ('draw','aim'):
            # Draw hand stays near the string; bow grip reaches without clipping.
            elbow=(ox+side*.09*h,oy-.045*h)
            hand=(elbow[0]+side*.085*h,oy-.073*h)
        elif action=='fight':
            elbow=(ox+side*.13*h,oy-.07*h)
            hand=(ox+side*.22*h,oy-.19*h+.04*h*math.sin(t*7))
        elif action in ('hold','offer','drink'):
            elbow=(ox+side*.14*h,oy+.08*h)
            hand=(ox+side*.24*h,oy-.14*h)
        elif action=='embrace':
            elbow=(ox+side*.15*h,oy+.04*h)
            hand=(ox+side*.27*h,oy+.065*h)
        elif action=='weave':
            elbow=(ox+side*.13*h,oy+.065*h)
            hand=(ox+side*.22*h,oy+.045*h+.045*h*math.sin(t*5))
        elif moving:
            elbow=(ox+side*.04*h+cyc*side*.030*h,oy+.13*h)
            hand=(elbow[0]-side*cyc*.08*h,elbow[1]+.12*h)
        else:
            elbow=(ox+side*.04*h,oy+.13*h)
            hand=(elbow[0]+side*.035*h,elbow[1]+.12*h)
        # Pauldron, arm segment and wrist all remain physically joined.
        L(d,[(ox,oy),elbow,hand],DARK,max(3,int(h*.107)))
        L(d,[(ox,oy),elbow,hand],c['skin'],max(3,int(h*.077)))
        E(d,(ox-.061*h,oy-.059*h,ox+.060*h,oy+.058*h),BGOLD if c['armor'] else c['fabric'],width=o+1)
        if c['armor']:E(d,(ox-.035*h,oy-.035*h,ox+.037*h,oy+.036*h),'#ce985b',outline=None,width=1)
        E(d,(hand[0]-.043*h,hand[1]-.050*h,hand[0]+.047*h,hand[1]+.041*h),c['skin'],width=max(1,int(o*.8)))
        return hand
    arm(-1)
    # torso and tunic armor silhouette, curved leather skirt with 5-6 animated tassels.
    if c['kind'] in ('robe','elderrobe'):
        P(d,[(shoulder[0]-.17*h,shoulder[1]),(shoulder[0]+.17*h,shoulder[1]),(hip[0]+.36*h,y-.04*h),(hip[0]-.32*h,y-.04*h)],c['fabric'],width=o+1)
        P(d,[(x+.01*h,y-.61*h),(x+.07*h,y-.59*h),(x+.03*h,y-.09*h),(x-.04*h,y-.10*h)],c['cloak'],outline=None)
        L(d,[(x-.23*h,y-.38*h),(x+.23*h,y-.38*h)],'#ad8556',max(2,int(h*.017)))
        for q in (0,1):L(d,[(x+(-.12+q*.19)*h,y-.32*h),(x+(-.17+q*.25)*h,y-.08*h)],'#f5d8a9',max(1,int(h*.012)))
    elif c['armor']:
        P(d,[(shoulder[0]-.19*h,shoulder[1]),(shoulder[0]+.19*h,shoulder[1]),(hip[0]+.21*h,hip[1]+.035*h),(hip[0]-.20*h,hip[1]+.035*h)],'#cfac72',width=o+2)
        P(d,[(shoulder[0]-.17*h,shoulder[1]+.015*h),(shoulder[0]-.10*h,shoulder[1]+.015*h),(hip[0]+.08*h,hip[1]-.11*h),(hip[0]+.020*h,hip[1]-.09*h)],DARK,outline=None)
        P(d,[(shoulder[0]+.13*h,shoulder[1]+.020*h),(shoulder[0]+.19*h,shoulder[1]+.020*h),(hip[0]-.05*h,hip[1]-.11*h),(hip[0]-.10*h,hip[1]-.11*h)],DARK,outline=None)
        E(d,(x-.045*h,shoulder[1]+.115*h,x+.047*h,shoulder[1]+.204*h),GOLD,width=o)
        P(d,[(x-.16*h,hip[1]-.025*h),(x+.17*h,hip[1]-.025*h),(x+.20*h,hip[1]+.09*h),(x-.20*h,hip[1]+.09*h)],DARK,width=o)
        for k in range(6):
            xk=x+(-.18+k*.067)*h;shake=math.sin(t*2+k*.6)*.007*h
            P(d,[(xk,hip[1]+.07*h),(xk+.052*h,hip[1]+.07*h),(xk+.038*h+shake,hip[1]+.23*h),(xk-.01*h+shake,hip[1]+.22*h)],'#b98953',width=max(1,int(o*.6)))
            L(d,[(xk+.012*h,hip[1]+.09*h),(xk+.005*h,hip[1]+.19*h)],'#ddaf70',1)
    else:
        P(d,[(shoulder[0]-.16*h,shoulder[1]),(shoulder[0]+.16*h,shoulder[1]),(hip[0]+.19*h,hip[1]+.18*h),(hip[0]-.19*h,hip[1]+.18*h)],c['fabric'],width=o+1)
        L(d,[(x-.18*h,hip[1]-.006*h),(x+.17*h,hip[1]-.006*h)],'#e0b373',max(2,int(.023*h)))
        if role in ('suitor','suitor2','telemachus'):
            L(d,[(x-.10*h,shoulder[1]+.075*h),(x+.075*h,hip[1]-.05*h)],'#d8b47d',max(1,int(.027*h)))
    arm(1,True)
    # Human scale heads use the same stylized Bronze Age anatomy as 60s film.
    cx=shoulder[0];cy=shoulder[1]-.10*h
    fy=y-.83*h+bob
    headrad=.155*h
    if role in ('odysseus','beggar') and IMG is not None:
        # Pixel-true transparent canonical Odisseus helmet + face from OWNED first film.
        tw=max(1,int(.43*h*SCALE));th=max(1,int(.49*h*SCALE))
        head=(ORIGINAL_HEAD if role=='odysseus' else ORIGINAL_BEGGAR_FACE).resize((tw,th),Image.Resampling.LANCZOS)
        tilt=math.sin(t*.73)*1.3
        head=head.rotate(tilt,resample=Image.Resampling.BICUBIC,expand=True)
        px=int((cx-.22*h)*SCALE);py=int((y-h*1.003)*SCALE)
        IMG.paste(head,(px,py),head)
    else:
        # Custom cast follows same graphite outline, angular cheek/nose, shadowed hair.
        P(d,[(cx-.13*h,fy-.13*h),(cx+.075*h,fy-.17*h),(cx+.15*h,fy-.015*h),(cx+.108*h,fy+.16*h),(cx-.046*h,fy+.17*h),(cx-.155*h,fy+.06*h)],c['skin'],width=o+1)
        if c.get('braid'):
            L(d,[(cx-.09*h,fy-.10*h),(cx-.175*h,fy+.06*h),(cx-.20*h,fy+.30*h)],c['hair'],max(3,int(.063*h)))
            for k in range(4): E(d,(cx-.23*h,fy+.11*h+k*.05*h,cx-.17*h,fy+.16*h+k*.05*h),c['hair'],outline=None,width=1)
        if c['kind'] not in ('giant','elder','elderrobe'):
            P(d,[(cx-.155*h,fy-.024*h),(cx-.15*h,fy-.155*h),(cx-.005*h,fy-.205*h),(cx+.14*h,fy-.11*h),(cx+.11*h,fy+.004*h),(cx+.04*h,fy-.10*h)],c['hair'],width=max(1,int(o*.9)))
        else:
            P(d,[(cx-.145*h,fy-.060*h),(cx-.13*h,fy-.145*h),(cx+.05*h,fy-.19*h),(cx+.14*h,fy-.065*h)],c['hair'],width=o)
        if c.get('beard'):
            P(d,[(cx-.11*h,fy+.080*h),(cx-.035*h,fy+.155*h),(cx+.045*h,fy+.198*h),(cx+.124*h,fy+.054*h),(cx+.085*h,fy+.125*h),(cx+.005*h,fy+.145*h)],c['hair'],width=max(1,int(o*.75)))
        # Eyes must be consistent between cuts; Polyphemus has precisely ONE.
        if role=='cyclops':
            E(d,(cx-.053*h,fy-.066*h,cx+.054*h,fy+.035*h),'#f9e4b3',width=max(1,int(o*.8)))
            E(d,(cx-.025*h,fy-.041*h,cx+.025*h,fy+.016*h),'#7d493a',outline=None,width=1)
            E(d,(cx-.009*h,fy-.027*h,cx+.01*h,fy+.010*h),DARK,outline=None,width=1)
        else:
            for side in (-1,1):
                xe=cx+side*.055*h
                P(d,[(xe-.033*h,fy-.021*h),(xe+.015*h,fy-.014*h),(xe+.007*h,fy+.007*h)],c['eye'],outline=None)
        # Greek Bronze-age straight angular nose and small line mouth.
        L(d,[(cx+.008*h,fy-.018*h),(cx+.035*h,fy+.058*h),(cx+.005*h,fy+.064*h)],'#996c51',max(1,int(.017*h)))
        if role not in ('cyclops',):L(d,[(cx-.010*h,fy+.105*h),(cx+.05*h,fy+.117*h)],'#754b40',max(1,int(.010*h)))
        if c['helmet']:
            P(d,[(cx-.156*h,fy-.091*h),(cx-.13*h,fy-.210*h),(cx+.003*h,fy-.260*h),(cx+.16*h,fy-.185*h),(cx+.17*h,fy-.07*h)],'#b6844c',width=o+1)
            P(d,[(cx-.13*h,fy-.231*h),(cx-.064*h,fy-.316*h),(cx+.068*h,fy-.330*h),(cx+.18*h,fy-.225*h),(cx+.31*h,fy-.185*h),(cx+.145*h,fy-.204*h),(cx+.030*h,fy-.287*h)],RED if role!='athena' else '#506f83',width=o+1)
            L(d,[(cx-.15*h,fy-.105*h),(cx+.14*h,fy-.108*h)],'#e6b571',max(2,int(.025*h)))
    if role=='cyclops':
        for side in (-1,1):E(d,(cx+side*.20*h-.025*h,shoulder[1]-.015*h,cx+side*.20*h+.025*h,shoulder[1]+.04*h),'#b9a37a',width=1)
        # Wild matted locks, muscular ochre shoulders, stitched animal-hide skirt.
        for k in range(6):
            xx=cx+(-.13+k*.055)*h
            P(d,[(xx,fy-.12*h),(xx+.03*h,fy-.18*h),(xx+.045*h,fy-.105*h)],'#4e3b34',outline=None)
        P(d,[(x-.20*h,hip[1]-.055*h),(x+.18*h,hip[1]-.055*h),(x+.20*h,hip[1]+.17*h),(x-.17*h,hip[1]+.17*h)],'#736754',width=o)
        for k in range(6):
            L(d,[(x+(-.16+k*.06)*h,hip[1]+.02*h),(x+(-.15+k*.06)*h,hip[1]+.15*h)],'#aa9875',max(1,int(h*.006)))
    if role=='penelope':
        # Bronze Age queen: braided crown, pale peplos, teal woven sash.
        L(d,[(x-.17*h,y-.44*h),(x+.18*h,y-.44*h)],'#497c80',max(3,int(.026*h)))
        E(d,(cx-.15*h,fy-.19*h,cx+.12*h,fy-.155*h),'#d6b06b',outline=None,width=1)
        E(d,(x-.027*h,y-.685*h,x+.028*h,y-.633*h),'#bf9255',width=1)
        for k in range(5):
            xx=x-.17*h+k*.08*h
            L(d,[(xx,y-.23*h),(xx+.01*h,y-.15*h)],'#eecf9e',1)
    elif role=='circe':
        # Witch: copper embroidered hem, dark locks, unique emerald collar.
        P(d,[(x-.20*h,y-.69*h),(x+.19*h,y-.69*h),(x+.13*h,y-.60*h),(x-.14*h,y-.60*h)],'#b4825f',width=o)
        L(d,[(x-.16*h,y-.18*h),(x+.16*h,y-.18*h)],'#cda365',max(2,int(.023*h)))
        E(d,(cx-.025*h,fy+.15*h,cx+.032*h,fy+.205*h),'#d8b17b',width=1)
    elif role=='calypso':
        # Nymph: marine-white gown, azure clasp and curling long hair.
        P(d,[(x+.12*h,y-.68*h),(x+.23*h,y-.66*h),(x+.27*h,y-.27*h),(x+.19*h,y-.26*h)],'#b6c9c4',outline=None)
        E(d,(cx+.07*h,fy-.21*h,cx+.13*h,fy-.16*h),'#a6c5c0',width=1)
        L(d,[(x-.12*h,y-.39*h),(x+.11*h,y-.39*h)],'#8fa8af',max(2,int(.020*h)))
    elif role=='nausicaa':
        # Younger princess, lighter hair, pearl collar and bright-blue mantle.
        L(d,[(cx-.14*h,fy-.15*h),(cx+.12*h,fy-.15*h)],'#d7c493',max(2,int(.018*h)))
        E(d,(cx+.11*h,fy-.19*h,cx+.15*h,fy-.15*h),'#f4ead2',outline=None,width=1)
        P(d,[(x+.05*h,y-.67*h),(x+.19*h,y-.65*h),(x+.27*h,y-.11*h),(x+.19*h,y-.11*h)],'#7da7b7',outline=None)
    elif role=='eurycleia':
        # Elderly nurse with silver hair bun + thick shawl and low posture.
        E(d,(cx-.12*h,fy-.20*h,cx-.01*h,fy-.10*h),'#d0c9bd',width=1)
        P(d,[(x-.24*h,y-.66*h),(x+.22*h,y-.65*h),(x+.16*h,y-.48*h),(x-.19*h,y-.49*h)],'#9f8f78',width=o)
        for q in range(3):L(d,[(cx-.09*h,fy+.045*h+q*6),(cx-.03*h,fy+.055*h+q*6)],'#947c6b',1)
    elif role=='athena':
        # Olive-gold aegis and round shield, spear, steel-blue helmet plume.
        E(d,(x+.18*h,y-.59*h,x+.43*h,y-.35*h),'#aa884c',width=o+1)
        E(d,(x+.23*h,y-.53*h,x+.37*h,y-.41*h),'#667e81',width=1)
        L(d,[(x-.32*h,y-.16*h),(x-.21*h,y-.93*h)],'#806247',max(2,int(.018*h)))
        P(d,[(x-.25*h,y-.90*h),(x-.21*h,y-1.02*h),(x-.16*h,y-.90*h)],'#c1a16a',width=1)
    elif role=='hermes':
        # Herald's tiny winged travelling cap and staff, distinct from Odisseus.
        P(d,[(cx-.13*h,fy-.18*h),(cx-.25*h,fy-.29*h),(cx-.16*h,fy-.22*h)],'#f1dfb2',width=2)
        P(d,[(cx+.14*h,fy-.18*h),(cx+.26*h,fy-.30*h),(cx+.17*h,fy-.21*h)],'#f1dfb2',width=2)
        L(d,[(x+.29*h,y-.20*h),(x+.28*h,y-.85*h)],'#c7a05f',3)
    elif role=='telemachus':
        # Son inherits father's proportions but has short hair and BLUE mantle.
        L(d,[(x-.14*h,y-.60*h),(x+.12*h,y-.48*h)],'#d5ba8b',max(2,int(.029*h)))
        P(d,[(cx-.13*h,fy-.11*h),(cx-.07*h,fy-.22*h),(cx+.02*h,fy-.18*h),(cx+.13*h,fy-.21*h),(cx+.15*h,fy-.12*h)],'#29292b',width=2)
    elif role=='laertes':
        # Old father's silver beard, olive cloak and bowed walking staff.
        P(d,[(cx-.09*h,fy+.085*h),(cx-.02*h,fy+.26*h),(cx+.09*h,fy+.10*h)],'#c6bfb1',width=2)
        L(d,[(x+.27*h,y-.05*h),(x+.25*h,y-.69*h)],'#7b5b3e',max(3,int(.016*h)))
    elif role=='eumaeus':
        # Swineherd's shaggy animal pelt instead of royal armor.
        P(d,[(x-.22*h,y-.69*h),(x+.04*h,y-.70*h),(x+.19*h,y-.47*h),(x-.18*h,y-.49*h)],'#74624e',width=o)
        for k in range(4):
            E(d,(x-.16*h+k*.10*h,y-.65*h,x-.11*h+k*.10*h,y-.60*h),'#968066',outline=None)
    elif role=='suitor':
        E(d,(x-.029*h,y-.68*h,x+.027*h,y-.62*h),'#edc176',width=1)
        L(d,[(x-.13*h,y-.27*h),(x+.12*h,y-.27*h)],'#b77b61',2)
    elif role=='suitor2':
        # Dark-violet Eurymachus — silver chained necklace, no beard.
        L(d,[(x-.08*h,y-.68*h),(x,y-.63*h),(x+.08*h,y-.68*h)],'#e1c8ae',2)
        E(d,(x-.022*h,y-.64*h,x+.024*h,y-.60*h),'#bdab94',width=1)
    elif role=='aiolos':
        P(d,[(cx-.14*h,fy-.18*h),(cx+.14*h,fy-.18*h),(cx+.09*h,fy-.13*h),(cx-.11*h,fy-.13*h)],'#b9a887',width=2)
    elif role=='tiresias':
        L(d,[(x-.27*h,y-.10*h),(x-.25*h,y-.94*h)],'#7a6959',3)
        E(d,(cx-.18*h,fy-.14*h,cx+.17*h,fy-.115*h),'#b8b8b0',width=2)
    elif role=='mother':
        P(d,[(x-.20*h,y-.66*h),(x+.18*h,y-.66*h),(x+.22*h,y-.10*h),(x-.17*h,y-.08*h)],'#9aafb8',outline=None)
    elif role=='sailor':
        L(d,[(cx-.13*h,fy-.14*h),(cx+.13*h,fy-.14*h)],'#9c8067',max(2,int(.015*h)))
    if role=='cyclops':
        # ONE eye and one eye only: no separate human pupils under forehead.
        pass
    return {'x':x,'head':(cx,fy),'hip':hip,'shoulder':shoulder,'feet':feet,'height':h}

# Inject matching illustrated cast into the previously grounded complete narrative.
base.actor=actor
_old_render=base.render_frame

def render_frame(W,H,tt,font,scale=1.0):
    global IMG,SCALE
    SCALE=scale
    # Keep actor drawing in EXACT same RGB canvas through hook.
    i=min(15,max(0,bisect.bisect_right(base.TIMES,tt)-1))
    u=(tt-base.TIMES[i])/(base.TIMES[i+1]-base.TIMES[i]);t=tt
    IMG=Image.new('RGB',(int(W*scale),int(H*scale)))
    d=base.ScaledDraw(ImageDraw.Draw(IMG),scale) if scale!=1 else ImageDraw.Draw(IMG)
    base.background(W,H,i,t,d)
    base.scene_art(d,W,H,i,u,t)
    base.subtitle(d,W,H,i,u,font)
    # Original film discreet type at top: don't add random title overlay on every shot.
    if t<4 or i==1 or (i==15 and u>.85):
        small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',max(9,int(W*.018*scale)))
        d.text((int(W*.070),int(H*.045)),'MITOLOGIA GREGA · ODISSEU',font=small,fill='#f3dfc0')
    out=IMG
    IMG=None
    return out
base.render_frame=render_frame

def main():
    base.main()
if __name__=='__main__':main()