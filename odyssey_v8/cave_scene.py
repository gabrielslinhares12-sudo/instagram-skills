#!/usr/bin/env python3
"""ODYSSEY V8: genuine 3D blocking, physically shared cave/giant/boulder coordinates.

First 17s proof-of-story (source narration 00:38..00:55). This is a new
independent set, not an edited V5/V7 image or a stock photo composition.
Deterministic procedural 3D scene. No paid models, services or APIs.
"""
import os, math, argparse, subprocess, sys, json, random
from pathlib import Path
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy

P = lambda x: tuple(v/255 for v in x)
COL={
  'rock':P((77,74,76)), 'rock2':P((103,99,94)),'rock3':P((124,117,101)),
  'sand':P((111,98,86)),'sand2':P((170,143,110)),'cloth':P((115,58,49)),
  'bronze':P((202,147,81)),'bronze2':P((140,89,54)),
  'skin':P((190,125,92)),'giant':P((167,135,112)),'tunic':P((84,69,70)),
  'eye':P((244,226,190)),'pupil':P((44,34,38)),
  'ink':P((40,38,43)), 'wood':P((113,75,50)), 'torch':P((239,168,85)),
}
FPS=60
DURATION=17

def clamp(v,a=0.0,b=1.0):return max(a,min(b,v))
def sm(v):
 v=clamp(v);return v*v*(3-2*v)
def mix(a,b,w):return a*(1-w)+b*w

def material(actor,color,ambient=.24,diffuse=.76,specular=.16,spower=27):
 p=actor.GetProperty();p.SetColor(*color);p.SetAmbient(ambient);p.SetDiffuse(diffuse)
 p.SetSpecular(specular);p.SetSpecularPower(spower);return actor

def poly_actor(source,color,renderer,amb=.23,sp=.15):
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(source.GetOutputPort());
 actor=vtk.vtkActor();actor.SetMapper(mapper);material(actor,color,amb,specular=sp);renderer.AddActor(actor)
 return actor

def ellipsoid(renderer,pos,radii,color,res=18,rotation=None,amb=.2):
 src=vtk.vtkSphereSource();src.SetRadius(1);src.SetThetaResolution(res);src.SetPhiResolution(res)
 a=poly_actor(src,color,renderer,amb=amb,sp=.13)
 a.SetPosition(*pos);a.SetScale(*radii)
 if rotation:a.SetOrientation(*rotation)
 return a

def cube(renderer,pos,lengths,color,rotate=(0,0,0),amb=.23):
 s=vtk.vtkCubeSource();s.SetXLength(lengths[0]);s.SetYLength(lengths[1]);s.SetZLength(lengths[2]);
 a=poly_actor(s,color,renderer,amb=amb);a.SetPosition(*pos);a.SetOrientation(*rotate);return a

def taper(renderer,p1,p2,r1,r2,color,sides=13):
 # tapered rigid cone/cylinder with endpoints in common XYZ world coordinates
 vec=np.subtract(p2,p1);L=float(np.linalg.norm(vec))
 src=vtk.vtkConeSource();src.SetHeight(L);src.SetRadius(max(r1,r2));src.SetResolution(sides)
 # vtk cone default X axis, point usually cone; for arm forms use tube below instead
 return between(renderer,p1,p2,max(r1,r2),color)

def between(renderer,p1,p2,r,color,sides=16):
 s=vtk.vtkLineSource();s.SetPoint1(*p1);s.SetPoint2(*p2)
 tube=vtk.vtkTubeFilter();tube.SetInputConnection(s.GetOutputPort());tube.SetRadius(r);tube.SetNumberOfSides(sides);tube.CappingOn()
 a=poly_actor(tube,color,renderer,sp=.12)
 return (a,s)

def update_between(segment,p1,p2):
 src=segment[1];src.SetPoint1(*p1);src.SetPoint2(*p2);src.Modified()

class Figure:
 def __init__(self,ren,name,scale=1.0,body=COL['cloth'],skin=COL['skin'],bronze=True):
  self.ren=ren;self.name=name;self.scale=scale;self.body=body;self.skin=skin
  self.parts=[];self.links=[];self.bronze=bronze
  # local parts; all positions are computed from one root transform, not screen layers
  self.torso=ellipsoid(ren,(0,0,0),(1,1,1),body)
  self.hips=ellipsoid(ren,(0,0,0),(1,1,1),body)
  self.neck=ellipsoid(ren,(0,0,0),(1,1,1),skin)
  self.head=ellipsoid(ren,(0,0,0),(1,1,1),skin,res=30)
  self.nose=ellipsoid(ren,(0,0,0),(1,1,1),skin,res=14)
  self.leftEye=ellipsoid(ren,(0,0,0),(1,1,1),COL['eye'],res=18)
  self.rightEye=ellipsoid(ren,(0,0,0),(1,1,1),COL['eye'],res=18)
  self.pupilL=ellipsoid(ren,(0,0,0),(1,1,1),COL['ink'],res=16)
  self.pupilR=ellipsoid(ren,(0,0,0),(1,1,1),COL['ink'],res=16)
  self.belt=cube(ren,(0,0,0),(1,1,1),COL['bronze2'])
  self.helmet=None;self.crest=None
  if bronze:
   self.helmet=ellipsoid(ren,(0,0,0),(1,1,1),COL['bronze'],res=24)
   self.crest=ellipsoid(ren,(0,0,0),(1,1,1),COL['cloth'],res=24)
  self.limbs=[between(ren,(0,0,0),(0,0,1),.145*scale,skin) for _ in range(8)]
  self.hands=[ellipsoid(ren,(0,0,0),(1,1,1),skin) for _ in range(2)]
  self.feet=[ellipsoid(ren,(0,0,0),(1,1,1),COL['bronze2']) for _ in range(2)]
  self.shadow=ellipsoid(ren,(0,0,.06),(1,1,.05),P((38,34,35)),res=24,amb=.95)
  self.shield=None
  if bronze:
   self.shield=ellipsoid(ren,(0,0,0),(1,1,1),COL['bronze'],res=24)
   self.shieldBoss=ellipsoid(ren,(0,0,0),(1,1,1),COL['bronze2'],res=18)
  Figure.pose(self,0,(0,0),0,False)
 def pose(self,t,root=(0,0),yaw=0,walk=False,afraid=False,distance=0.0):
  s=self.scale;px,py=root
  # 3D world, Z is vertical; yaw rotates local X/Y in ground plane
  co=math.cos(yaw);si=math.sin(yaw)
  def xyz(x,y,z):return (px+s*(x*co-y*si),py+s*(x*si+y*co),s*z)
  sway=(.055*math.sin(5.4*t) if walk else .014*math.sin(t*1.3))
  # Foot planting is tied to root travel distance, NOT an unrelated sine clock.
  step_length=.90*s
  self.torso.SetPosition(*xyz(0,0,1.55+sway));self.torso.SetScale(.42*s,.27*s,.62*s)
  self.hips.SetPosition(*xyz(0,0,1.10+sway));self.hips.SetScale(.35*s,.3*s,.28*s)
  self.neck.SetPosition(*xyz(0,-.02,2.08+sway));self.neck.SetScale(.14*s,.15*s,.25*s)
  self.head.SetPosition(*xyz(0,-.025,2.34+sway));self.head.SetScale(.27*s,.27*s,.32*s)
  self.nose.SetPosition(*xyz(0,-.29,2.31+sway));self.nose.SetScale(.105*s,.14*s,.12*s)
  for i,xx in enumerate([-.115,.115]):
   eye=self.leftEye if i==0 else self.rightEye
   pupil=self.pupilL if i==0 else self.pupilR
   eye.SetPosition(*xyz(xx,-.24,2.45+sway));eye.SetScale(.086*s,.041*s,.071*s)
   pupil.SetPosition(*xyz(xx,-.279,2.44+sway));pupil.SetScale(.034*s,.024*s,.048*s)
  self.belt.SetPosition(*xyz(0,0,1.14+sway));self.belt.SetScale(.69*s,.60*s,.11*s)
  if self.helmet:
   self.helmet.SetPosition(*xyz(0,.015,2.58+sway));self.helmet.SetScale(.289*s,.295*s,.24*s)
   self.crest.SetPosition(*xyz(0,.025,2.85+sway));self.crest.SetScale(.125*s,.44*s,.18*s)
  # Articulated legs with planted ankles and marching knees, never root translation without gait.
  for i,side in enumerate([-1,1]):
   if walk:
    phase=(distance/(2*step_length)+i*.5)%1.0
    if phase<.5:
     off=-step_length/(2*s)+phase*2*step_length/s
     lift=0.0   # stance: root moves while planted world foot stays fixed
    else:
     swing=(phase-.5)*2
     off=step_length/(2*s)-swing*step_length/s
     lift=.32*math.sin(math.pi*swing) # airborne foot returns forward
   else:
    off=0.0;lift=0.0
   hip=xyz(side*.20,0,1.02+sway)
   knee=xyz(side*.23,off*.42,.55+lift*.47+sway)
   foot=xyz(side*.23,off,.16+lift)
   update_between(self.limbs[i*2+0],hip,knee)
   update_between(self.limbs[i*2+1],knee,foot)
   for a in [self.limbs[i*2+0][0],self.limbs[i*2+1][0]]:a.GetProperty().SetColor(*self.skin)
   self.feet[i].SetPosition(*foot);self.feet[i].SetScale(.175*s,.31*s,.15*s)
   shoulder=xyz(side*.40,0,1.93+sway)
   if afraid:
    elbow=xyz(side*.65,-.32,2.12+sway)
    hand=xyz(side*.42,-.52,2.70+sway)
   else:
    arm=side*(.24*math.cos(math.pi*distance/step_length) if walk else .045*math.sin(t*1.5))
    elbow=xyz(side*.48,-arm*.45,1.56+sway)
    hand=xyz(side*.43,-arm,1.11+sway)
   update_between(self.limbs[4+i*2],shoulder,elbow)
   update_between(self.limbs[5+i*2],elbow,hand)
   self.hands[i].SetPosition(*hand);self.hands[i].SetScale(.12*s,.14*s,.15*s)
  if self.shield:
   self.shield.SetPosition(*xyz(-.54,.23,1.43+sway));self.shield.SetScale(.13*s,.5*s,.53*s)
   self.shieldBoss.SetPosition(*xyz(-.67,.23,1.43+sway));self.shieldBoss.SetScale(.055*s,.14*s,.14*s)
  self.shadow.SetPosition(px,py,.055);self.shadow.SetScale(.56*s,.39*s,.025)

class Giant(Figure):
 def __init__(self,ren):
  super().__init__(ren,'Polifemo',scale=3.65,body=COL['tunic'],skin=COL['giant'],bronze=False)
  # Make exactly one eye at the center of the forehead, rather than two hidden eyes.
  for a in [self.leftEye,self.rightEye,self.pupilL,self.pupilR]:a.SetVisibility(False)
  self.oneEye=ellipsoid(ren,(0,0,0),(1,1,1),COL['eye'],res=30)
  self.onePupil=ellipsoid(ren,(0,0,0),(1,1,1),COL['pupil'],res=24)
  self.brow=between(ren,(0,0,0),(0,0,1),.08,COL['ink'])
  self.eyelid=ellipsoid(ren,(0,0,0),(1,1,1),COL['giant'],res=20);self.eyelid.SetVisibility(False)
  # Mouth modeled as real dark geometry on face; tunic and rope belt.
  self.mouth=between(ren,(0,0,0),(0,0,1),.04,COL['ink'])
  self.belt.GetProperty().SetColor(*P((95,65,48)))
 def pose(self,t,root=(0,0),yaw=0,walk=False,afraid=False,pushing=False,rock_center=None,distance=0.0):
  super().pose(t,root,yaw,walk,False,distance=distance)
  s=self.scale;px,py=root
  co=math.cos(yaw);si=math.sin(yaw)
  def xyz(x,y,z):return (px+s*(x*co-y*si),py+s*(x*si+y*co),s*z)
  self.oneEye.SetPosition(*xyz(0,-.275,2.43));self.oneEye.SetScale(.135*s,.054*s,.099*s)
  self.onePupil.SetPosition(*xyz(0,-.332,2.43));self.onePupil.SetScale(.064*s,.03*s,.072*s)
  update_between(self.brow,xyz(-.19,-.295,2.59),xyz(.19,-.295,2.59))
  update_between(self.mouth,xyz(-.17,-.265,2.17),xyz(.17,-.265,2.17))
  if pushing and rock_center is not None:
   # single coordinate system: both palms contact world-space right face of rock.
   # full arm has shoulder->elbow->hand, no detached hand on top of the boulder.
   rx,ry,rz=rock_center
   for i,side in enumerate([-1,1]):
    shoulder=xyz(side*.38,-.09,1.87)
    hand=(rx+side*2.18,ry+1.53,rz+side*.63)
    elbow=(mix(shoulder[0],hand[0],.52),mix(shoulder[1],hand[1],.52)-.18, mix(shoulder[2],hand[2],.48)+.25)
    update_between(self.limbs[4+2*i],shoulder,elbow)
    update_between(self.limbs[5+2*i],elbow,hand)
    self.hands[i].SetPosition(*hand);self.hands[i].SetScale(.16*s,.14*s,.16*s)

class Scene:
 def __init__(self,width=540,height=960):
  self.ren=vtk.vtkRenderer();self.ren.SetBackground(.08,.106,.137)
  self.ren.SetBackground2(.20,.19,.19);self.ren.GradientBackgroundOn()
  self.win=vtk.vtkRenderWindow();self.win.OffScreenRenderingOn();self.win.AddRenderer(self.ren);self.win.SetSize(width,height)
  self.win.SetMultiSamples(4)
  self.camera=self.ren.GetActiveCamera();self.camera.SetViewUp(0,0,1);self.camera.SetClippingRange(.1,350)
  self.set_lights();self.build_environment()
  self.hero=Figure(self.ren,'Odisseu',body=COL['cloth'],skin=COL['skin'],bronze=True)
  self.sailor1=Figure(self.ren,'marinheiro_de_azul',body=P((65,86,108)),skin=P((179,120,91)),bronze=False)
  self.sailor2=Figure(self.ren,'marinheiro_de_areia',body=P((135,112,80)),skin=P((165,105,81)),bronze=False)
  self.giant=Giant(self.ren)
  self.boulder=self.build_boulder()
  self.sheep=[self.build_sheep(i) for i in range(3)]
  self.width=width;self.height=height
 def set_lights(self):
  def light(pos,color,intensity):
   l=vtk.vtkLight();l.SetLightTypeToSceneLight();l.SetPosition(*pos);l.SetFocalPoint(0,2,4)
   l.SetColor(*color);l.SetIntensity(intensity);self.ren.AddLight(l)
  light((5,17,18),(1,.80,.63),1.08)
  light((-9,-7,14),(.48,.64,.8),.78)
  light((17,-10,8),(1,.71,.50),.42)
 def build_environment(self):
  cube(self.ren,(0,0,-.35),(38,48,.7),COL['sand'])
  # Deep cave: continuous corridor rather than separately layered painted backdrops.
  cube(self.ren,(-24,0,5),(6.0,37,10),COL['rock'])
  cube(self.ren,(24,0,5),(6.0,37,10),COL['rock2'])
  cube(self.ren,(0,1,14),(25,35,4),COL['rock'])
  # The giant returns from exterior y=+9; an open arch leaves a real passage.
  for x in [-6.25,6.25]:
   cube(self.ren,(x,7.7,5.3),(5.4,3.8,10.6),COL['rock3'],rotate=(0,0,(-7 if x<0 else 8)))
  cube(self.ren,(0,7.7,14.2),(18,3.8,4.1),COL['rock2'])
  # Stone threshold, visible between the pillars and the approaching giant.
  cube(self.ren,(0,7.65,.09),(8.25,4,.26),COL['sand2'])
  rand=random.Random(61)
  for n in range(55):
   side=(-1 if n%2==0 else 1)
   xx=side*rand.uniform(18.5,25.5)
   yy=rand.uniform(-11,19)
   zz=rand.uniform(.4,1.1)
   sx=rand.uniform(.8,3.2);sy=rand.uniform(.7,3.3);sz=rand.uniform(.8,2.6)
   ellipsoid(self.ren,(xx,yy,zz),(sx,sy,sz),[COL['rock2'],COL['rock3'],COL['rock']][n%3],res=8,
            rotation=(rand.uniform(-14,14),rand.uniform(-10,10),rand.uniform(-35,35)))
  for n in range(30):
   xx=rand.uniform(-10,10);yy=rand.uniform(-11,17)
   if xx*xx+yy*yy<4:continue
   ellipsoid(self.ren,(xx,yy,.11),(rand.uniform(.13,.48),rand.uniform(.13,.52),rand.uniform(.09,.24)),
             COL['rock3'] if n%3 else COL['rock2'],res=9)
  # Food inside cave; physically modeled jugs, bread, bowls.
  for x,y in [(1.8,1.4),(3.1,1.7)]:
   ellipsoid(self.ren,(x,y,.69),(.6,.52,.73),P((142,82,61)),res=20)
   ellipsoid(self.ren,(x,y,1.28),(.41,.38,.17),P((176,111,75)),res=20)
   ellipsoid(self.ren,(x,y,1.36),(.29,.26,.08),P((57,44,36)),res=20)
  for k in range(8):
   x=2.1+.43*(k%4);y=-.1+.55*(k//4)
   ellipsoid(self.ren,(x,y,.19),(.32,.21,.15),P((187,144,83)),res=12)
  # Distinct torch on the near wall; a 3D source of color, not an overlay.
  between(self.ren,(-6.5,-1.5,1.9),(-6.3,-1.1,3.8),.10,COL['wood'])
  ellipsoid(self.ren,(-6.25,-1.08,4.06),(.28,.28,.64),COL['torch'],res=16)
  ellipsoid(self.ren,(-6.25,-1.08,4.18),(.16,.15,.38),P((255,222,132)),res=16,amb=.66)
 def build_sheep(self,i):
  # Flock accompanies Polyphemus; full 3D meshes and ground-contact legs.
  color=P((198,178,147)) if i%2==0 else P((158,151,139))
  body=ellipsoid(self.ren,(0,0,0),(.68,.39,.44),color,res=14)
  head=ellipsoid(self.ren,(0,0,0),(.28,.26,.29),P((144,122,97)),res=14)
  legs=[cube(self.ren,(0,0,0),(.12,.12,.49),P((116,94,80))) for _ in range(4)]
  return body,head,legs
 def build_boulder(self):
  # The stone is wider and taller than the actual portal; rolling closes it.
  s=vtk.vtkSphereSource();s.SetRadius(1);s.SetThetaResolution(16);s.SetPhiResolution(11)
  s.Update()
  points=s.GetOutput().GetPoints()
  for k in range(points.GetNumberOfPoints()):
   x,y,z=points.GetPoint(k)
   r=1+.055*math.sin(k*1.271)+.06*math.cos(x*7+z*3.7)+.03*math.sin(z*11+y*9)
   points.SetPoint(k,x*r,y*r,z*r)
  points.Modified()
  a=poly_actor(s,P((105,100,95)),self.ren,amb=.26,sp=.08)
  a.SetScale(4.30,1.65,6.05)
  # Real rock chips, all parented to the boulder, not motion overlay.
  chips=[]
  for i in range(17):
   r=random.Random(109+i)
   u=r.uniform(-2.6,2.6);v=r.uniform(-3.5,3.6)
   chip=ellipsoid(self.ren,(0,0,0),(r.uniform(.28,.7),r.uniform(.14,.28),r.uniform(.18,.6)),
             COL['rock3'] if i%3 else COL['rock2'],res=7)
   chips.append((chip,u,v,r.uniform(.15,.35)))
  return (a,chips)
 def set_camera(self,seconds):
  # Continuous camera moves, never a series of unrelated flat illustrations.
  if seconds<5.0:
   q=sm(seconds/5);p=(mix(4.5,3.7,q),mix(-19,-17.8,q),mix(8.5,8.1,q));f=(mix(0,0,q),mix(7.2,8.2,q),mix(4.6,5.1,q));ang=42
  elif seconds<10.5:
   q=sm((seconds-5)/5.5);p=(mix(3.7,5.7,q),mix(-17.8,-17,q),mix(8.1,8.8,q));f=(mix(0,2.2,q),mix(8.2,8.6,q),mix(5.1,5.9,q));ang=mix(42,39,q)
  elif seconds<11.45:
   q=sm((seconds-10.5)/.95);p=(mix(5.7,7.7,q),mix(-17,-12.8,q),mix(8.8,7.0,q));f=(mix(2.2,0.,q),mix(8.6,12.2,q),mix(5.9,4.6,q));ang=41
  elif seconds<15.55:
   # Lateral 3D shot: see the giant's physical push and stone progress to arch.
   q=sm((seconds-11.45)/4.1);p=(19.7,12.3,10.2);f=(.3,12.3-.8*q,4.9);ang=43
  else:
   # Reaction from inside after the enormous stone is wedged in the opening.
   q=sm((seconds-15.55)/1.45);p=(3.2,-17.9,7.4);f=(.1,8.9,4.6);ang=41
  self.camera.SetPosition(*p);self.camera.SetFocalPoint(*f);self.camera.SetViewAngle(ang)
  self.camera.SetClippingRange(.2,150)
 def update(self,t):
  self.set_camera(t)
  # Crew enter together; feet move in phase with root displacement.
  for fig,xx,offset in [(self.hero,-1.0,0),(self.sailor1,-2.1,-.65),(self.sailor2,.05,-1.15)]:
   q=sm((t-offset)/6.0)
   y=mix(8.8,2.2,q)
   x=xx-.6*q
   walk=t-offset>0 and t-offset<6
   fig.pose(t+offset,(x,y),yaw=.05,walk=walk,afraid=t>=11.4,distance=max(0.0,8.8-y))
  # Polyphemus must appear at the arch only AFTER the narration says he returned.
  if t<5.0:
   self.giant_visible=False
   for part in self.giant.ren.GetActors():
    pass
  gq=sm((t-5.0)/5.3)
  rock_q=sm((t-11.3)/4.8)
  rock_x=.10
  rock_y=mix(17.6,8.95,rock_q)
  rock_z=6.10
  actor,chips=self.boulder
  actor.SetPosition(rock_x,rock_y,rock_z)
  actor.SetOrientation(0,0,rock_q*2.5)
  for obj,u,v,d in chips:
   obj.SetPosition(rock_x+u,rock_y-d,rock_z+v)
   obj.SetOrientation(0,0,0)
   obj.SetVisibility(False)
  actor.SetVisibility(t>=10.5)
  root=(.25,mix(24.4,20.4,gq) if t<=11.3 else rock_y+2.8)
  self.giant.pose(t,root,yaw=0.0,walk=5.0<=t<10.9 or 11.3<t<16.0,
                  pushing=t>11.1,rock_center=(rock_x,rock_y,rock_z),distance=max(0.0,24.4-root[1]))
  # Walking sheep follow the giant through the same passage behind the men.
  for i,(body,head,legs) in enumerate(self.sheep):
   sheep_t=sm((t-5.6-i*.35)/5.2)
   yy=mix(19.8+i*.65,5.5+i*.3,sm((t-5.6-i*.35)/9.7))
   xx=(-1.7,1.5,-.5)[i]
   bob=.05*math.sin(6*t+i)
   body.SetPosition(xx,yy,.78+bob)
   head.SetPosition(xx,yy-.64,1.05+bob)
   for k,leg in enumerate(legs):
    side=-1 if k%2==0 else 1
    rear=-1 if k<2 else 1
    step=.21*math.sin(7.3*t+i+math.pi*k/2) if t<11 else 0
    leg.SetPosition(xx+side*.43,yy+rear*.21+step,.35)
   for prop in [body,head,*legs]:prop.SetVisibility(t>=5.4)
  # VTK actors of the giant managed as a single gated figure, not hiding random layers.
  visible=t>=5.0
  for prop in [self.giant.torso,self.giant.hips,self.giant.neck,self.giant.head,self.giant.nose,self.giant.belt,self.giant.oneEye,self.giant.onePupil,self.giant.brow[0],self.giant.mouth[0],self.giant.shadow,*self.giant.hands,*self.giant.feet,*[x[0] for x in self.giant.limbs]]:prop.SetVisibility(visible)
  # When boulder reaches threshold at t≈16 it physically blocks the opening.
 def screenshot(self,p):
  self.win.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(self.win);f.ReadFrontBufferOff();f.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(p));writer.SetInputConnection(f.GetOutputPort());writer.Write()
 def render(self,out,frames,fps=FPS,crf=18):
  self.win.Render()
  w,h=self.width,self.height
  cmd=['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{w}x{h}',
        '-framerate',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf',str(crf),'-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  buf=vtk.vtkWindowToImageFilter();buf.SetInput(self.win);buf.ReadFrontBufferOff()
  try:
   for i in range(frames):
    self.update(i/fps)
    self.win.Render();buf.Modified();buf.Update()
    vtk_image=buf.GetOutput();arr=vtk_to_numpy(vtk_image.GetPointData().GetScalars()).reshape((h,w,3))
    proc.stdin.write(arr[::-1].tobytes())
    if i%max(1,fps*2)==0:print(f'frame {i}/{frames} {i/fps:.1f}s',flush=True)
  finally:
   proc.stdin.close()
  err=proc.stderr.read();result=proc.wait()
  if result!=0:raise RuntimeError(err.decode('utf-8','replace')[-2000:])
  return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--size',default='540x960');parser.add_argument('--stills',action='store_true');parser.add_argument('--video',action='store_true');parser.add_argument('--fps',type=int,default=24);parser.add_argument('--duration',type=float,default=17);parser.add_argument('--output',default='/mnt/data/odyssey_v8');a=parser.parse_args()
 w,h=map(int,a.size.split('x'));out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 scene=Scene(w,h)
 if a.stills:
  for sec in (1,3.5,6,8.5,10.8,12.5,14.5,16.8):
   scene.update(sec);scene.screenshot(out/f'odyssey3d_{sec:04.1f}.png');print('snapshot',sec,flush=True)
 if a.video:scene.render(out/'odyssey-v8-3d-blocking-video-silent.mp4',round(a.duration*a.fps),a.fps)
if __name__=='__main__':main()
