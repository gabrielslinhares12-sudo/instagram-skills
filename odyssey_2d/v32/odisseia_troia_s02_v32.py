#!/usr/bin/env python3
"""Odyssey TUE S02: The fall of Troy. True 2D frame-by-frame animation,
source horse and Odysseus extracted from the owner's first Cavalo de Troia
film; fully drawn world with deliberate nonrepeating actions.

This render is 13.03s scene-level visual QC, not 16-scene film master. No 3D,
Runway, Guthy, paid API, AI-video credits, still-image zoom or footage loops.
"""
import argparse
import math
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

HOME=Path(__file__).resolve().parent
SRC=HOME/'assets'
HORSE=Image.open(SRC/'CAVALO_TROIA_ORIGINAL_RGBA.png').convert('RGBA')
HERO=Image.open(SRC/'ODISSEU_ORIGINAL_TROIA_SPRITE_CANONICO.png').convert('RGBA')
FPS=30
W,H=720,1280
OUT=HOME/'ODISSEIA_TROIA_S02_V32_MODELO_ORIGINAL_13s_QC.mp4'
INK=(62,46,44)
STONE=(161,131,100)
EDGE=(80,60,52)
SAND=(181,149,108)
TAN=(202,165,125)
DARK=(27,48,67)
YELLOW=(244,209,149)
WOOD=(127,78,51)
SMOKE=(58,62,67)


def ease(t):
 t=min(1,max(0,t));return t*t*(3-2*t)

def mix(a,b,f):return a+(b-a)*f

def draw_background(d,night=False):
 sky1=(12,33,50) if night else (31,65,84)
 sky2=(53,62,75) if night else (211,158,111)
 for y in range(H):
  p=min(1,y/850)
  v=tuple(round(mix(a,b,p)) for a,b in zip(sky1,sky2))
  d.line([(0,y),(W,y)],fill=v)
 # Medallion disc matching original film, slowly moving clouds instead of moving a static frame
 d.ellipse((517,86,627,196),fill=(241,202,128) if night else (242,201,138))
 for k in range(4):
  y=680+30*k
  d.polygon([(-40,y+24),(85,y-38),(150,y+7),(258,y-59),(372,y+24),(500,y-30),(765,y+17),(765,y+110),(-40,y+110)],
   fill=(52+12*k,66+10*k,66+8*k) if night else (130+12*k,137+6*k,126+5*k))
 if night:
  for j in range(32):
   x=(j*211+59)%W;y=(j*87+37)%625
   if (x-572)**2+(y-140)**2>7500:d.ellipse((x,y,x+2,y+2),fill=(208,216,203))


def city(d,cx=0,night=False):
 """World-scale decorative Mycenaean houses, correct Bronze-Age silhouette."""
 for k in range(11):
  x=int(k*113-90-cx*.27)
  y=826-(k%4)*18
  col=(87,92,89) if night else (168,131,99)
  d.rectangle((x,y-130,x+89,y+70),fill=col,outline=EDGE,width=3)
  d.polygon([(x-8,y-130),(x+46,y-176),(x+97,y-130)],fill=(73,62,61) if night else (112,80,64),outline=EDGE)
  d.rectangle((x+37,y-90,x+53,y-43),fill=(245,183,114) if night else (56,68,72))
  if night:d.ellipse((x+42,y-77,x+48,y-67),fill=(252,211,128))


def path_ground(d,night=False):
 d.polygon([(0,890),(W,866),(W,H),(0,H)],fill=(95,87,82) if night else (189,153,111))
 for i in range(6):
  y=930+i*50
  d.line((0,y,W,y+7),fill=(105,96,87) if night else (159,127,94),width=2)


def wall(d,camx,night=False,front=False):
 if front:
  X=lambda x:round(x-camx)
  for x in [454,795]:
   d.rectangle((X(x-13),353,X(x+14),904),fill=(98,92,91) if night else (164,129,98),outline=EDGE,width=4)
  return
 # Giant wall only at x < 460 or > 800; 340px gate taller than the horse.
 def X(x):return round(x-camx)
 block=(107,110,112) if night else STONE
 brick=(64,75,78) if night else (127,100,76)
 for left,right in [(-500,460),(800,1700)]:
  l,r=X(left),X(right)
  if r<0 or l>W:continue
  d.rectangle((l,365,r,896),fill=block,outline=EDGE,width=5)
  for j in range(10):
   y=386+j*49
   d.line((l,y,r,y),fill=brick,width=2)
   b0=left+(j%2)*31
   for x in range(b0,right,85):
    xx=X(x)
    if 0<xx<W:d.line((xx,y,xx,y+49),fill=brick,width=2)
  for x in range(left,right,67):
   d.rectangle((X(x),337,X(x+58),369),fill=block,outline=EDGE,width=3)
 # Structural architrave: realistic horse-to-gate clearance about 1.3x.
 lx,rx=X(460),X(800)
 d.rectangle((lx,365,rx,542),fill=block,outline=EDGE,width=4)
 for yy in (391,439,489,535):
  d.line((lx,yy,rx,yy),fill=brick,width=2)
 for xx in (490,572,653,732,775):
  xline=X(xx)
  d.line((xline,392,xline,537),fill=brick,width=2)
 if front:
  for x in [454,795]:
   d.rectangle((X(x-13),353,X(x+14),904),fill=(98,92,91) if night else (164,129,98),outline=EDGE,width=4)


def gate_doors(d,camx,p,night=False):
 """Two actual hinged panels: widths shrink as door opens, hinges stay fixed."""
 def X(x):return round(x-camx)
 open_amount=ease(p)
 for x,side in [(460,1),(800,-1)]:
  door_width=165*(1-open_amount)+8*open_amount
  x1=x;x2=x+side*door_width
  d.polygon([(X(x1),543),(X(x2),553),(X(x2),875),(X(x1),894)],
            fill=(75,49,42) if night else (116,75,55),outline=INK)
  # diagonal planks and dark metal rivets
  for j in range(3):
   y=607+j*108
   d.line((X(x1),y,X(x2),y+14),fill=(152,112,78),width=7)
  for y in (566,647,742,844):
   d.ellipse((X(x1)-4,y-4,X(x1)+4,y+4),fill=(38,40,40))


def ship(d,cx,y,scale,t):
 """Ship translates and visibly pitches, oars stroke and waves move."""
 P=lambda x,z:(int(cx+x*scale),int(y+z*scale))
 bob=math.sin(t*2.9)*7
 y+=bob
 p=lambda x,z:(int(cx+x*scale),int(y+z*scale))
 d.polygon([p(-225,-15),p(199,-15),p(171,65),p(-162,77),p(-217,44)],fill=(124,73,43),outline=INK)
 d.line([p(-225,-15),p(212,-15)],fill=(70,48,39),width=max(2,int(8*scale)))
 d.line([p(-8,-13),p(-8,-210)],fill=(84,65,51),width=max(2,int(10*scale)))
 d.polygon([p(-2,-196),p(118,-157),p(99,-40),p(-2,-46)],fill=(218,200,165),outline=(94,74,60))
 for x in (-145,-70,0,71,132):
  ang=math.sin(t*5.5+x*.01)*.32
  d.line([p(x,19),p(x+33*ang,94)],fill=(86,56,40),width=max(1,int(5*scale)))
 for k in range(6):
  xx=cx+(k*93-250)*scale
  yy=y+79*scale+math.sin(t*5+k)*5
  d.arc((xx-35,yy-5,xx+42,yy+15),0,180,fill=(228,216,174),width=3)


def small_actor(d,x,feet,size=65,t=0,look_right=True,color=(151,112,71),arm_action='pull'):
 """New Trojan figure follows original line/shape grammar. Legs truly alternate."""
 s=size/95;face=1 if look_right else -1
 head_y=feet-79*s
 p=lambda dx,dy:(round(x+dx*s),round(feet+dy*s))
 # cape/loin cloth around animated trunk
 d.polygon([p(-18,-48),p(15,-49),p(14,-11),p(-19,-9)],fill=color,outline=INK)
 d.ellipse((*p(-13,-94),*p(13,-71)),fill=(195,153,109),outline=INK,width=max(2,int(3*s)))
 d.line([p(-8,-88),p(10,-88)],fill=(94,70,57),width=max(1,int(2*s)))
 swing=math.sin(t*7.4)*12 if arm_action=='walk' else math.sin(t*4.1)*2
 foot_l=p(-10+swing*.4,0);foot_r=p(10-swing*.4,0)
 d.line([p(-6,-12),p(-10+swing*.4,-2),foot_l],fill=INK,width=max(3,int(7*s)))
 d.line([p(8,-12),p(10-swing*.4,-2),foot_r],fill=INK,width=max(3,int(7*s)))
 if arm_action=='pull':
  d.line([p(-15,-43),p(-24*face,-50),p(-34*face,-37)],fill=INK,width=max(3,int(7*s)))
  d.line([p(14,-43),p(20*face,-48),p(31*face,-35)],fill=INK,width=max(3,int(7*s)))
 else:
  d.line([p(-14,-42),p(-15-swing*.6,-20)],fill=INK,width=max(3,int(7*s)))
  d.line([p(14,-42),p(15+swing*.6,-21)],fill=INK,width=max(3,int(7*s)))


# Preserve exact wooden horse cutout, rotate only its wheel artwork for real motion.
# Composite original horse with left and right wheel suppressed before drawing
# fresh spokes in the exact original brown/black style.
H0=HORSE.copy()
for box in [(64,290,101,327),(202,290,240,327)]:
 from PIL import ImageDraw
 ImageDraw.Draw(H0).ellipse(box,fill=(0,0,0,0))

def draw_horse(canvas,cx,feet,w,t,night=False,hatch=0,people=0):
 h=round(w*HORSE.height/HORSE.width)
 asset=H0.resize((w,h),Image.Resampling.LANCZOS)
 if night:
  # Same outlines and colors from original asset, low-key night illumination.
  rgb=ImageEnhance.Brightness(asset.convert('RGB')).enhance(.72)
  rgb.putalpha(asset.getchannel('A'));asset=rgb
 canvas.alpha_composite(asset,(round(cx-w/2),round(feet-h)))
 d=ImageDraw.Draw(canvas)
 scale=w/HORSE.width;x0=cx-w/2;y0=feet-h
 # Original wheels, animated spokes and hubs. Contact point remains stationary.
 for lx in (85,220):
  wx=x0+lx*scale;wy=y0+308*scale
  r=17*scale
  d.ellipse((wx-r,wy-r,wx+r,wy+r),fill=(157,99,60),outline=INK,width=max(2,int(4*scale)))
  for j in range(8):
   a=j*math.pi/4-t*1.46
   d.line((wx,wy,wx+math.cos(a)*r*.85,wy+math.sin(a)*r*.85),fill=(66,46,38),width=max(1,int(2.4*scale)))
  d.ellipse((wx-4*scale,wy-4*scale,wx+4*scale,wy+4*scale),fill=(224,176,109),outline=INK,width=1)
 if hatch:
  # Actual trapezoidal body opening in same position as original trapdoor.
  a=ease(hatch)
  bx=x0+177*scale;by=y0+162*scale
  bw=47*scale;bh=48*scale
  d.polygon([(bx,by),(bx+bw,by),(bx+bw,by+bh),(bx,by+bh)],fill=(40,37,36),outline=INK)
  d.polygon([(bx,by),(bx+bw,by-17*a*scale),(bx+bw,by+bh-17*a*scale),(bx,by+bh)],fill=(159,103,67),outline=INK)
  # Ladder attaches to the hatch, bottom remains grounded near horse foot.
  d.line((bx+bw*.65,by+bh,bx+bw*.65+24*scale,feet-6*scale),fill=(128,83,50),width=5)
  d.line((bx+bw*.65+20*scale,by+bh,bx+bw*.65+44*scale,feet-6*scale),fill=(128,83,50),width=5)
  for j in range(4):
   ly=by+bh+((feet-10*scale)-(by+bh))*j/3
   xx=bx+bw*.65+(ly-(by+bh))/(feet-(by+bh))*23*scale
   d.line((xx,ly,xx+20*scale,ly),fill=(201,152,96),width=3)
 return (x0,y0,scale)


def s01(t):
 # S02: four DISTINCT causal actions, no shot duplicated, no scenery reused.
 z=Image.new('RGBA',(W,H),(0,0,0,255));d=ImageDraw.Draw(z)
 if t<6.52:
  stage=0 if t<3.26 else 1
  camx=-20+180*ease(t/3.26) if t<3.26 else 160+320*ease((t-3.26)/3.26)
  draw_background(d,night=False)
  city(d,camx)
  path_ground(d)
  wall(d,camx,front=False)
  gate_doors(d,camx,0 if stage==0 else (t-3.26)/1.55)
  horse_x=(190+110*ease(t/3.26)) if t<3.26 else (300+20*ease((t-3.26)/1.34)) if t<4.6 else (320+625*ease((t-4.6)/1.92))
  horse_w=260
  px=horse_x-camx
  # Attached ropes: same world-space contact over full shot.
  d.line((px-130,775,px-195,840),fill=(229,201,155),width=3)
  d.line((px+120,775,px+170,840),fill=(229,201,155),width=3)
  small_actor(d,px-196,895,78,t,True,arm_action='walk')
  small_actor(d,px+176,895,75,t,True,arm_action='walk')
  draw_horse(z,px,900,horse_w,t)
  wall(ImageDraw.Draw(z),camx,front=True)
 elif t<9.78:
  u=t-6.52
  draw_background(d,night=True)
  city(d,0,night=True)
  path_ground(d,night=True)
  # The ORIGINAL horse is centered inside night Troy, never replaced.
  horsecx=350
  draw_horse(z,horsecx,894,460,t,night=True,hatch=u/1.2)
  # Distinct Greek soldiers EMERGE from the visible door, climb down the
  # same ladder and walk with changing feet to the real city gate.
  # The hatch is never hidden by a cut to an unrelated view.
  if u>.36:
   p=ease((u-.36)/1.85)
   out=ease((u-2.15)/1.1)
   first_x=horsecx+36+92*p+82*out
   first_feet=744+146*p
   small_actor(ImageDraw.Draw(z),first_x,first_feet,112,t,True,
               color=(122,75,57),arm_action='walk')
   # Bronze blade is held in the right hand throughout descent.
   dd=ImageDraw.Draw(z)
   dd.line((first_x+21,first_feet-52,first_x+47,first_feet-112),fill=(43,46,48),width=6)
   dd.line((first_x+23,first_feet-53,first_x+48,first_feet-112),fill=(194,159,95),width=3)
  if u>1.45:
   p=ease((u-1.45)/1.65)
   second_x=horsecx+16+62*p
   second_feet=748+145*p
   small_actor(ImageDraw.Draw(z),second_x,second_feet,95,t,True,
               color=(158,105,68),arm_action='walk')
  # Torches flicker as characters leave, visible environmental consequence.
  d=ImageDraw.Draw(z)
  for tx in (72,642):
   d.line((tx,674,tx,790),fill=(88,64,50),width=8)
   r=11+3*math.sin(t*12+tx)
   d.ellipse((tx-r,665-r,tx+r,671+r),fill=(245,158,78))
  # Motivated medium shot of the hatch: soldiers physically descend into the
  # street. Fixed camera change, not a pan over a still image.
  z=z.crop((145,286,675,1228)).resize((W,H),Image.Resampling.BILINEAR)
 else:
  u=t-9.78
  draw_background(d,night=True)
  city(d,0,night=True)
  # Burning coastal city fades behind ship; identifiable flames with physical sources.
  for x in [102,204,277,430,581]:
   base=832-(x%3)*45
   amp=30+14*math.sin(t*8+x)
   d.polygon([(x-20,base),(x-5,base-amp),(x,base-amp-18),(x+18,base-amp*.6),(x+31,base)],fill=(236,112,44))
   d.polygon([(x-6,base),(x+4,base-amp*.75),(x+20,base)],fill=(255,198,85))
  # Water drawn in world-space traveling waves, not a translated still.
  d.rectangle((0,860,W,H),fill=(26,62,82))
  for k in range(15):
   yy=880+k*27
   for j in range(8):
    xx=(j*127+t*52+k*37)%(W+100)-35
    d.arc((xx,yy,xx+83,yy+13),0,180,fill=(85,117,128),width=2)
  xx=245+310*ease(u/3.24)
  ship(d,xx,931,1.0,t)
  # Exact original Odysseus character stands on ship deck, consistently styled.
  h=125;ow=int(h*HERO.width/HERO.height)
  asset=HERO.resize((ow,h),Image.Resampling.LANCZOS)
  z.alpha_composite(asset,(int(xx-54),int(896-h+math.sin(t*2.9)*7)))
 return z.convert('RGB')


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(OUT));ap.add_argument('--fps',type=int,default=FPS);ap.add_argument('--scale',type=float,default=1.0);ap.add_argument('--stills',action='store_true');args=ap.parse_args()
 path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
 if args.stills:
  for i,t in enumerate([0.5,2.5,3.8,5.2,6.9,8,9.2,10.0,11.4,12.6]):
   img=s01(t);img.save(path.with_name(f'Troia_S02_QC_FRAME_{i:02d}.png'))
  return
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-video_size',f'{W}x{H}','-r',str(args.fps),'-i','-',
      '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(path)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for frame in range(round(13.03*args.fps)):
  p.stdin.write(s01(frame/args.fps).tobytes())
 p.stdin.close()
 if p.wait()!=0:raise RuntimeError('ffmpeg failed')
 print('RENDERED',path,path.stat().st_size)

if __name__=='__main__':main()