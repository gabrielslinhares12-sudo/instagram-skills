#!/usr/bin/env python3
"""A Odisseia V29: block Polyphemus as EIGHT unique chronological illustrated shots,
not four loops: cave entrance, rock, wine, sleep, heated stake, sheep, shout, Poseidon.
Preserves first Trojan Horse actor line-art. Independent QC clip, not publishable.
"""
import os,sys,math,bisect
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'/mnt/data')
import odyssey_v28_director as v
old=v.old

# S04 natural-voice sequence has 19.83s; eight causal shots, no filler loops.
BORDERS=[0,.11,.25,.36,.46,.57,.70,.83,1]
BEATS=['CAVE_ESTABLISH_THREE_HUMANS','GIANT_ROLLS_TRUE_SCALE_ROCK',
       'ODYSSEUS_GIVES_WINE_TO_HAND','GIANT_DRINKS_AND_SLEEP_IN_CAVE',
       'HOT_STAKE_AND_ONE_EYE_RECOIL','CREW_HIDDEN_UNDER_SHEEP_ESCAPE',
       'ODYSSEUS_SHOUTS_IDENTITY_FROM_SHIP','CYCLOPS_INVOKES_POSEIDON_FROM_SHORE']

def cave_stage(d,j,t,p):
    # Background entirely painted in first-film vector language. One cave volume,
    # one correct entrance and connected floor, not repeated random rock silhouettes.
    v.old.illustrated_sky(d,'cave' if j<=5 else 'sea',t)
    if j<=5:
        # Distant olive-colored cliffs and a single large vaulted entrance.
        v.P(d,[(0,206),(105,160),(240,190),(330,156),(540,200),(540,960),(0,960)],'#767265',4)
        v.P(d,[(34,746),(65,378),(125,298),(190,245),(280,224),(388,250),(447,319),(510,746)],'#1d2e35',4)
        # Inner shaded wall follows arch rather than floating triangular ceiling shards.
        v.P(d,[(35,752),(106,411),(175,346),(263,320),(361,370),(461,752)],'#263338',4)
        for k in range(11):
            x=45+k*44
            v.L(d,[(x,742),(x+12,752+((k*37)%12))],'#504e48',2)
        v.P(d,[(0,748),(540,748),(540,960),(0,960)],'#776b59',3)
        for yy in (789,846,908):v.L(d,[(0,yy),(540,yy)],'#63594e',2)
        # One sheep pen, not several unrelated props.
        v.P(d,[(31,672),(132,678),(132,759),(31,759)],'#645545',2)
        for k in range(5):v.L(d,[(40+k*22,677),(40+k*22,758)],'#9b815e',3)
        if j in (2,3,4):
            # Actual fire source anchored to ground.
            v.E(d,(305,744,354,762),'#4b3c37',2)
            for k in range(3):
                xx=319+k*10
                v.P(d,[(xx,754),(xx-9,711+10*math.sin(t*3+k)),(xx+15,734)],'#e6b66e',1)
        if j==5:
            # Show sunlight shining through physically same cave mouth, toward exit.
            v.P(d,[(0,356),(83,294),(147,412),(147,753),(0,753)],'#bdad8b',2)
    else:
        old.ocean(d,t)
        v.painter_mountains(d,t)
        old.ocean(d,t)
        if j==7:
            v.P(d,[(390,710),(420,524),(469,499),(540,571),(540,960),(390,960)],'#867d6a',3)
        else:
            for x in (36,497):v.P(d,[(x-42,770),(x+32,680),(x+56,785)],'#928672',3)

def physically_connected(d,a,b,width=14):
    # Thick outline and flesh inner segment to match first-film actors.
    v.L(d,[a,b],old.DARK,width+5)
    v.L(d,[a,b],'#c49978',width)
    v.E(d,(b[0]-width/1.2,b[1]-width/1.2,b[0]+width/1.2,b[1]+width/1.2),'#c49978',2)

def events(d,j,p,t):
    """Every new shot changes the state of at least one object or character."""
    p=old.clamp(p)
    if j==0:
        old.actor(d,115+30*old.ease(p),782,157,'odysseus',t,'approach')
        old.actor(d,60+20*old.ease(p),781,145,'sailor',t,'approach')
        old.actor(d,191+17*old.ease(p),778,139,'sailor',t,'approach')
        old.sheep(d,425,777,74,t)
        # A shadow crossing entrance foreshadows giant walking into same cave.
        gx=600-95*old.ease(p)
        v.E(d,(gx-87,292,gx+79,783),'#443d36',3)
    elif j==1:
        q=old.ease(p)
        rockx=498-187*q;giantx=rockx+150
        old.actor(d,68,782,154,'odysseus',t,'kneel')
        old.actor(d,142,781,145,'sailor',t,'kneel')
        # The monolith's bottom is the ground. Width 328px vs doorway 320px.
        # A single irregular boulder with real planar floor contact,
        # NEVER a mathematical circle/disc and never hovering above its base.
        stone_shape=[(rockx-171,787),(rockx-189,720),(rockx-179,594),
           (rockx-150,505),(rockx-84,439),(rockx+18,407),
           (rockx+122,452),(rockx+174,555),(rockx+187,687),
           (rockx+160,785),(rockx+67,792),(rockx-61,792)]
        v.P(d,stone_shape,'#8e8577',5)
        for k in range(9):
            xx=rockx-111+k*29
            v.L(d,[(xx,490+25*(k%2)),(xx-22,554+19*(k%3))],'#b8aa91',3)
        old.actor(d,giantx,793,438,'cyclops',t,'push')
        # Fingers on boulder boundary; the actor and stone travel in SAME direction.
        for dy,offset in ((560,-25),(632,5)):
            b=(rockx+162,dy)
            a=(giantx-94,dy+offset)
            physically_connected(d,a,b,14)
        for x in (rockx-55,rockx+67):
            v.L(d,[(x,787),(x+16,796)],'#5e514a',5)
    elif j==2:
        # Wide hands physically transfer cup. Cup belongs to one focal action.
        old.actor(d,133,783,184,'odysseus',t,'offer')
        old.actor(d,408,789,414,'cyclops',t,'drink')
        cupx=old.lp(206,324,old.ease(p))
        cupy=603-56*old.ease(p)
        v.L(d,[(219,607),(cupx,cupy)],'#c69a74',11)
        v.L(d,[(349,520),(cupx,cupy)],'#c69a74',14)
        old.bowl(d,cupx,cupy,77)
        for k in range(4):
            v.E(d,(cupx-22+k*8,cupy-16,cupx-14+k*8,cupy-9),'#815347',1)
    elif j==3:
        # Giant really transitions from awake to reclining, not a static statue.
        # The actor leans and lowers; a large single eye visibly closes.
        slump=old.ease(p)
        gx=388+21*slump;ground=794
        old.actor(d,gx,ground,414,'cyclops',t,'fall' if slump>.45 else 'drink')
        old.actor(d,104,783,177,'odysseus',t,'kneel')
        old.actor(d,209,782,165,'sailor',t,'hold')
        old.bowl(d,310,748,63)
        v.E(d,(332,730,359,749),'#d8b487',2)
    elif j==4:
        # Non-graphic one-eye attack: real wood staff point advances, giant recoils.
        old.actor(d,394+50*old.ease(p),789,402,'cyclops',t,'fall' if p>.55 else 'hold')
        old.actor(d,111+35*old.ease(p),781,176,'odysseus',t,'pull')
        old.actor(d,210+26*old.ease(p),783,165,'sailor',t,'pull')
        tip=(old.lp(286,398,old.ease(p)),old.lp(611,469,old.ease(p)))
        v.L(d,[(140,686),tip],old.DARK,25)
        v.L(d,[(140,686),tip],'#b47642',17)
        v.L(d,[(tip[0]-16,tip[1]+8),tip],'#eba24d',6)
        for k in range(5):
            q=k*math.pi/2.5+t*4
            x=tip[0]+14*math.cos(q);y=tip[1]+14*math.sin(q)
            v.E(d,(x-3,y-3,x+3,y+3),'#f6be6a',1)
    elif j==5:
        # Three distinct refugees physically shelter UNDER THREE moving sheep.
        # The giant feels the wool, not a magically escaping crowd.
        old.actor(d,437,787,420,'cyclops',t,'hold')
        for k in range(3):
            xx=100+k*104+125*old.ease(p)
            old.actor(d,xx-5,789,84,'sailor' if k else 'odysseus',t,'escape')
            old.sheep(d,xx,766,93,t+k)
        v.L(d,[(370,575),(295+100*old.ease(p),706)],'#c4a07f',16)
    elif j==6:
        old.side_ship(d,260+90*old.ease(p),730,113,t)
        old.actor(d,277+90*old.ease(p),739,155,'odysseus',t,'fight')
        # Pointing backward identifies the claimant and causes the curse.
        v.L(d,[(321,643),(385,582-20*math.sin(t*2))],'#c59c77',9)
        for k in range(3):old.actor(d,177+90*old.ease(p)+k*41,725,95,'sailor',t,'hold')
    elif j==7:
        old.actor(d,428,789,385,'cyclops',t,'fight')
        old.side_ship(d,96+90*old.ease(p),752,61,t)
        # Physical thunderbolt silhouette only AFTER invocation, not before.
        if p>.5:
            xx=230-30*old.ease(p)
            v.P(d,[(xx,168),(xx-34,326),(xx+11,316),(xx-50,479),(xx+61,278),(xx+17,290),(xx+68,168)],'#e2cd92',2)

def shot_frame(t,scale=1):
    old.SCALE=scale
    i=min(15,max(0,bisect.bisect_right(old.T,t)-1))
    if i!=3:return v.still_frame(t,scale)
    u=old.clamp((t-old.T[i])/(old.T[i+1]-old.T[i]))
    j=min(len(BEATS)-1,bisect.bisect_right(BORDERS,u)-1)
    p=old.clamp((u-BORDERS[j])/(BORDERS[j+1]-BORDERS[j]))
    old.CANVAS=Image.new('RGB',(round(v.W*scale),round(v.H*scale)),'#183447')
    old.D=old.canon.base.ScaledDraw(ImageDraw.Draw(old.CANVAS),scale) if scale!=1 else ImageDraw.Draw(old.CANVAS)
    old.canon.IMG=old.CANVAS;old.canon.SCALE=scale
    d=old.D
    cave_stage(d,j,t,p)
    events(d,j,p,t)
    if j in (0,1,5):
        for x in (20,520):
            v.P(d,[(x-18,770),(x+19,749),(x+48,960),(x-40,960)],'#665c50',2)
    # Editorial phrase segmentation follows this shot's voiced event, not the
    # legacy V27 equal-quarter subtitle loop. Aural word-level review still needed.
    captions=[
      'Em uma caverna, foram aprisionados',
      'por Polifemo, um gigante de um olho só.',
      'Odisseu o embriagou,',
      'disse chamar-se Ninguém',
      'e cegou o monstro.',
      'Seus homens escaparam escondidos sob ovelhas.',
      'Mas, ao revelar seu verdadeiro nome,',
      'Odisseu provocou a vingança de Poseidon.'
    ]
    text=captions[j]
    font=ImageFont.truetype(old.FONT_DIR+'/DejaVuSans-Bold.ttf',21)
    words=text.split();rows=['']
    for word in words:
        if len((rows[-1]+' '+word).strip())<=35:rows[-1]=(rows[-1]+' '+word).strip()
        elif len(rows)<2:rows.append(word)
        else:rows[-1]+=' '+word
    for k,row in enumerate(rows):
        box=d.textbbox((0,0),row,font=font,stroke_width=2)
        xx=int((old.W-(box[2]-box[0]))/2)
        d.text((xx,825+k*29),row,font=font,fill='#f5ecd8',stroke_width=2,stroke_fill='#26333a')
    old.canon.IMG=None
    return old.CANVAS

v.old.frame=shot_frame
if __name__=='__main__':v.old.main()