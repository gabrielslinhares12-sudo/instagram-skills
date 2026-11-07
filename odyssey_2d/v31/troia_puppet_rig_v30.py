#!/usr/bin/env python3
"""Animate user's exact original 2D Odysseus cartoon cut-out, no redraw.
Separates transparent body regions into layered rotatable parts and preserves
first Trojan film ink, palette and face identity. Private draft, no publishing.
"""
import math,subprocess,argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path('/mnt/data/troia_model_lock')
SOURCE=HERE/'ODISSEU_ORIGINAL_TROIA_SPRITE_CANONICO.png'
ORIGINAL=Image.open(SOURCE).convert('RGBA')
W,H=ORIGINAL.size
STYLE_BG='#193950'

def mask(poly):
    m=Image.new('L',(W,H),0)
    ImageDraw.Draw(m).polygon(poly,fill=255)
    a=ORIGINAL.copy();a.putalpha(Image.composite(a.getchannel('A'),Image.new('L',(W,H),0),m))
    return a

# The masks do not redraw the face, cape, armour or bronze; they only delimit
# joints that were part of the original owned artwork.
PARTS={
    'cape': mask([(8,335),(38,254),(51,180),(68,161),(90,144),(140,154),(144,270),(107,307),(24,349)]),
    'leg_left': mask([(72,273),(113,262),(146,279),(145,305),(111,368),(74,375),(74,349)]),
    'leg_right': mask([(132,276),(167,257),(193,279),(207,365),(175,377),(141,356)]),
    'left_arm': mask([(44,164),(72,149),(91,169),(101,203),(94,252),(52,263),(40,229)]),
    'right_arm': mask([(176,154),(207,160),(231,207),(236,249),(204,263),(182,230)]),
    'torso': mask([(76,123),(113,120),(176,119),(209,164),(199,240),(190,286),(95,289),(75,247)]),
    'head': mask([(88,0),(205,0),(205,92),(194,147),(149,166),(97,144),(86,70)]),
}
PARTS['cape']=PARTS['cape'].resize((W,H))

PIVOTS={'cape':(76,157),'leg_left':(117,280),'leg_right':(163,279),
        'left_arm':(71,177),'right_arm':(199,182),'torso':(142,162),'head':(143,144)}

def rotated(name,angle):
    if abs(angle)<.001:return PARTS[name]
    return PARTS[name].rotate(angle,resample=Image.Resampling.BICUBIC,center=PIVOTS[name])

def smooth(x):return x*x*(3-2*x)
def clamp(x):return max(0,min(1,x))

def draw_puppet(target,x,feet,height,t,action,progress=0):
    """Puppet-specific actions: real walk cycle, bow grip, grounded push/brace."""
    phi=2*math.pi*1.15*t
    walk=action in ('walk','run','escape','approach')
    swing=math.sin(phi) if walk else 0
    bob=abs(math.sin(phi))*(3.6 if walk else 0)
    # Cloth reacts to movement, but head maintains identity and orientation.
    cape_ang=-(4*math.sin(t*2.2)+6*swing)
    body_ang=3*math.sin(phi) if walk else (-4*progress if action=='push' else 0)
    leg_l=18*swing if walk else (-15 if action=='push' else 0)
    leg_r=-18*swing if walk else (12 if action=='push' else 0)
    arm_l=-14*swing if walk else (22 if action in ('offer','fight','aim','embrace') else -46*progress if action=='push' else -13)
    arm_r=14*swing if walk else (-67*progress if action in ('draw','aim') else 35*progress if action=='push' else -43 if action in ('offer','embrace') else 23*math.sin(t*5) if action=='fight' else 11)
    if action in ('kneel','sleep'):leg_l=-38;leg_r=17
    if action=='pull':arm_l=-30;arm_r=-20

    head_ang=-2*math.sin(t*1.1)+(2*progress if action=='push' else 0)
    sprite=Image.new('RGBA',(W,H),(0,0,0,0))
    for name,ang in [('cape',cape_ang),('leg_left',leg_l),('leg_right',leg_r),
                     ('torso',body_ang),('left_arm',arm_l),('right_arm',arm_r),('head',head_ang)]:
        sprite.alpha_composite(rotated(name,ang))
    # The original sprite defines the exact body proportions. Never alter them.
    target_w=round(height*W/H)
    im=sprite.resize((target_w,round(height)),Image.Resampling.LANCZOS)
    # Foot coordinates relative to target remain consistent to scene floor.
    target.alpha_composite(im,(round(x-target_w*.5),round(feet-height+bob)))
    # contact locations derived from exact original local joint geometry.
    s=height/H
    return {'left_hand':(x+(82-142)*s,feet-height+(235+bob)*s),
            'right_hand':(x+(218-142)*s,feet-height+(247+bob)*s),
            'head':(x+(140-142)*s,feet-height+(101+bob)*s),
            'feet':feet, 'height':height}

def frame(t,fps=30):
    w,h=540,960
    im=Image.new('RGBA',(w,h),(33,64,80,255));d=ImageDraw.Draw(im)
    # Period-appropriate Mycenaean hall with original film sky/bronze palette.
    for y in range(960):
        k=y/960
        col=(int(27+134*k),int(57+99*k),int(72+60*k),255)
        d.line((0,y,540,y),fill=col)
    # Illustrated city skyline and durable stone entrance at exact positions.
    for k in range(7):
        x=10+k*85; yy=671-(k%3)*22
        d.rectangle((x,yy-94,x+77,758),fill='#ac8c6e',outline='#463734',width=3)
        d.polygon([(x-10,yy-94),(x+38,yy-125),(x+84,yy-94)],fill='#795a4a')
        d.rectangle((x+28,yy-66,x+44,yy-29),fill='#526371')
    d.polygon([(0,756),(540,744),(540,960),(0,960)],fill='#bda17c')
    for k in range(5):d.line((0,794+k*30,540,794+k*30),fill='#9f8a6b',width=2)
    p=clamp(t/5.8)
    x=95+318*smooth(p)
    info=draw_puppet(im,x,766,300,t,'walk' if t<3.9 else 'draw',p)
    d=ImageDraw.Draw(im)
    if t>3.4:
        # A prop actually enters and is gripped: one connected olive-wood bow.
        bx=x+85;cy=608
        d.line([(bx,cy-96),(bx-30,cy-49),(bx-42,cy),(bx-30,cy+50),(bx,cy+99)],fill='#382d2a',width=16,joint='curve')
        d.line([(bx,cy-96),(bx-30,cy-49),(bx-42,cy),(bx-30,cy+50),(bx,cy+99)],fill='#9d6e4b',width=10,joint='curve')
        pull=65*smooth(clamp((t-3.6)/2.2))
        d.line([(bx,cy-96),(bx+pull,cy),(bx,cy+99)],fill='#e4d7b5',width=3,joint='curve')
    return im.convert('RGB')

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--fps',type=int,default=30);p.add_argument('--seconds',type=float,default=6)
    args=p.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-video_size','540x960','-r',str(args.fps),'-i','-', '-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',args.output]
    pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(round(args.seconds*args.fps)):
        pr.stdin.write(frame(n/args.fps).tobytes())
    pr.stdin.close();assert pr.wait()==0
if __name__=='__main__':main()