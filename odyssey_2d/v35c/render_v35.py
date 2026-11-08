#!/usr/bin/env python3
"""A ODISSÉIA V35 — completely repainted 16 sets, 68 acted beats.
Uses the ORIGINAL user-supplied Rasalgethi WAV exactly; original cutout hero
and horse; no reused or rescaled previous-film frames.  Native illustrated
Pillow character animation and event-specific hand blocked props.  QC ONLY.
"""
import os,sys,math,json,argparse,subprocess,hashlib,bisect,random,functools
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import render_v33 as old
import environments_v35 as sets
import special_acting_v35 as perf
from story_sync_v35 import remap,write as save_timeline,validate_transcript
from collections import Counter
# Match actions to their spoken clauses instead of uniform four-beat slots.
assert validate_transcript(old.v.LINES)
old.SHOTS[:]=remap(old.SHOTS,old.v.T)
old.START[:]=[s['start_seconds_estimate'] for s in old.SHOTS]
save_timeline(old.SHOTS,ROOT/'retimed_68_shots.json')
W,H=540,960
INK='#392f30'
FRAMES=68

def new_bg(i):
 shot=old.SHOTS[i]
 return sets.build(shot['scene'], shot['beat'])
old.BGSHOT=new_bg

def animate_atoms(d,shot,t,p):
 """Individually performed environmental responses, not looped footage."""
 scene=shot['scene']; beat=shot['beat']
 if scene in (2,3,5,8,9,10,12):
  if ((scene in (5,9,10) and beat>=3) or (scene==8 and beat==4)):
   for k in range(24):
    x=(k*131+int(t*82))%640-45
    y=360+(k*47+int(t*124))%500
    sets.line(d,[(x,y),(x-12,y+23)],'#9eb9c1',1)
  if scene in (2,3) and beat in (2,4):
   for k in range(10):
    xx=(k*91+int(t*41))%590-25
    yy=707+(k%4)*42
    d.arc((xx-13,yy-5,xx+41,yy+11),5,170,fill='#b0d0c7',width=2)
 if scene==4:
  # physical environment reaction is synchronized to the performed beat
  if beat==2:
   # Monolith displaces anchored dust while giant moves it; dust dissipates.
   amp=math.sin(math.pi*max(0,min(1,p)))
   for k in range(12):
    x=219+k*20+math.sin(k*3)*12
    y=765-30*amp-15*(k%4)
    rr=3+(k%3)*2
    sets.el(d,(x-rr,y-rr,x+rr,y+rr),'#af9b80',w=0)
  elif beat==5:
   for k in range(16):
    x=old.M(250,380,p)+int(35*math.sin(k*1.9))
    y=472+int(28*math.cos(k*2.1))
    sets.line(d,[(x,y),(x+15,y-14)],'#dcaa70',2)
 if scene==6 and beat in (2,4):
  # Visible magical transformation localized to actor, fading in/out.
  amp=1 if beat==2 else (1-p)
  if amp>.01:
   for k in range(13):
    ang=k*6.283/13+t*.55
    xx=275+math.cos(ang)*70*amp; yy=621+math.sin(ang)*62*amp
    sets.el(d,(xx-2,yy-2,xx+3,yy+3),'#d4c38c',w=0)
 if scene==7:
  for k in range(18):
   x=(k*71+10+int(t*4))%540
   y=625+(k*39%129)+5*math.sin(t*.6+k)
   sets.el(d,(x-28,y-2,x+43,y+5),'#6c858a',w=0)
 if scene==10 and beat==3:
  # Flash illumination follows narrated lightning but never fills full frame.
  if .37<p<.43:
   d.rectangle((0,0,W,560),fill='#b1bbbc',width=0)
 if scene==11 and beat in (1,2,3):
  for k in range(12):
   x=127+(k%4)*8;y=495+((k*31+int(t*61))%280)
   sets.line(d,[(x,y),(x+2,y+14)],'#d8e9cf',2)

def foreground(d,shot):
 scene=shot['scene'];beat=shot['beat']
 # Contextual foreground silhouettes anchor depth and scale. No title cards.
 if scene==4:
  for x,r in ((10,42),(542,47)):
   sets.polygon(d,[(x-r,881),(x-16,825),(x+16,800),(x+r,886),(x+r,980),(x-r,980)],'#554d47',w=2)
 elif scene==9 and beat<=3:
  for x in (-14,547):
   sets.polygon(d,[(x-30,840),(x+20,800),(x+34,930),(x-40,962)],'#63665f',w=2)
 elif scene==7:
  for x in (27,520):
   sets.polygon(d,[(x-20,926),(x+4,846),(x+29,930)],'#435760',w=0)
 elif scene==6:
  for x in (31,514):
   sets.el(d,(x-47,840,x+50,877),'#4b6754',w=0)
 elif scene in (12,16) and beat==4:
  for x in (16,520):
   sets.tree(d,x,916,.43,seed=x)


def editorial_camera(img,shot):
 """Distinct shot sizes/editing, never zoom on a still: actors move underneath."""
 scene=shot['scene'];beat=shot['beat']
 zooms={
  1:[1.24,1.12,1.27,1.28],2:[1.04,1.06,1.11,1.04],
  3:[1.08,1.03,1.17,1.16],4:[1.00,1.06,1.18,1.18,1.04,1.02,1.05,1.04],
  5:[1.12,1.07,1.02,1.02],6:[1.12,1.15,1.12,1.10],
  7:[1.06,1.18,1.16,1.20],8:[1.00,1.06,1.09,1.03],
  9:[1.00,1.00,1.00,1.11],10:[1.08,1.15,1.00,1.08],
  11:[1.13,1.17,1.13,1.05],12:[1.14,1.10,1.06,1.16],
  13:[1.08,1.14,1.14,1.08],14:[1.06,1.15,1.17,1.15],
  15:[1.10,1.21,1.13,1.11],16:[1.09,1.16,1.08,1.13]}
 z=zooms[scene][beat-1]
 if z<1.01:return img
 cx=270;cy=570
 if (scene,beat)==(4,3):cx=315;cy=560
 elif (scene,beat)==(4,4):cx=380;cy=565
 elif (scene,beat)==(14,3):cx=313;cy=640
 elif (scene,beat) in {(13,2),(13,3)}:cx=315;cy=620
 w=W/z;h=H/z
 left=max(0,min(W-w,cx-w/2));top=max(0,min(H-h,cy-h/2))
 return img.crop((int(left),int(top),int(left+w),int(top+h))).resize((W,H),Image.Resampling.LANCZOS)

@functools.lru_cache(maxsize=1)
def subtitle_font():
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)

@functools.lru_cache(maxsize=128)
def caption_fragments(txt):
 """Keep exact spoken words, split only for mobile readability."""
 words=txt.split();out=[];cur=[]
 for word in words:
  test=' '.join(cur+[word])
  if len(test)>52 and cur:
   out.append(' '.join(cur));cur=[word]
  else:cur.append(word)
 if cur:out.append(' '.join(cur))
 return out

def exact_subtitle(d,shot,p):
 txt=shot['caption_exact_original']
 chunks=caption_fragments(txt)
 chunk=chunks[min(len(chunks)-1,max(0,int(p*len(chunks))))]
 font=subtitle_font()
 words=chunk.split();rows=[];cur=[]
 for word in words:
  test=' '.join(cur+[word])
  if d.textlength(test,font=font)>505 and cur:
   rows.append(' '.join(cur));cur=[word]
  else:cur.append(word)
 if cur:rows.append(' '.join(cur))
 rows=rows[:2]
 y=854-(len(rows)-1)*12
 for k,s in enumerate(rows):
  x=int((540-d.textlength(s,font=font))/2)
  d.text((x,y+28*k),s,font=font,fill='#f9f4e9',stroke_width=3,stroke_fill='#243038')

def film_frame(t):
 i=max(0,min(67,bisect.bisect_right(old.START,t)-1))
 shot=old.SHOTS[i]
 p=max(0,min(1,(t-shot['start_seconds_estimate'])/(shot['end_seconds_estimate']-shot['start_seconds_estimate'])))
 img=old.BG[i].copy()
 old.v.CANVAS=img;old.v.SCALE=1;old.v.canon.IMG=img;old.v.canon.SCALE=1
 d=ImageDraw.Draw(img)
 old.v.D=d
 animate_atoms(d,shot,t,p)
 if perf.affected(shot["scene"],shot["beat"]):perf.act(d,img,shot,t,p)
 else:old.action(d,img,i,p,t)
 foreground(d,shot)
 # The moving camera belongs to the physical scene only. Captions stay fixed
 # to the screen and never crop/scale with the camera (previous QC failure).
 img=editorial_camera(img,shot)
 d=ImageDraw.Draw(img)
 # Exact transcript text per event, mapped to recorded voice pause windows.
 # Character-level timing within each speech clause remains approximate.
 exact_subtitle(d,shot,p)
 old.v.canon.IMG=None
 return img

def contact(out,with_labels=True):
 old.build_backgrounds()
 sample=[(s['start_seconds_estimate']+s['end_seconds_estimate'])/2 for s in old.SHOTS]
 w0,h0=180,320
 N=34
 for group in range(2):
  sel=sample[group*N:(group+1)*N]
  width=6*w0; height=6*(h0+28)
  canvas=Image.new('RGB',(width,height),'#d8c9aa')
  d=ImageDraw.Draw(canvas)
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)
  for k,t in enumerate(sel):
   i=group*N+k
   im=film_frame(t).resize((w0,h0),Image.Resampling.LANCZOS)
   col,row=k%6,k//6
   x=col*w0;y=row*(h0+28)
   canvas.paste(im,(x,y))
   d.text((x+6,y+h0+3),old.SHOTS[i]['shot_id'],font=font,fill='#493d36')
  path=out.parent/(out.stem+f'_{group+1}.jpg')
  canvas.save(path,quality=88)
  print('CONTACT',path,flush=True)

def render(args):
 from hashlib import sha256
 path=Path(args.voice)
 h=sha256(path.read_bytes()).hexdigest()
 expected='9be8b79920b318c76f23874d38d12f4f77b46f8a9871833612ac1efa82b5d667'
 if h!=expected:raise RuntimeError('original voice mismatch '+h)
 old.build_backgrounds()
 output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
 count=math.ceil(min(220.56,args.preview if args.preview else 220.56)*args.fps)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(args.fps),'-i','pipe:0','-i',str(path),'-vf',f'scale={args.width}:{args.height}:flags=lanczos,setsar=1','-c:v','libx264','-preset','veryfast','-crf',str(args.crf),'-pix_fmt','yuv420p','-threads','4','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-shortest','-movflags','+faststart',str(output)]
 print('V35_16_AUTHORED_SCENES_68_UNIQUE_ACTIONS',count,'frames',flush=True)
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(count):
  im=film_frame(i/args.fps)
  p.stdin.write(im.tobytes())
  if i and i%(args.fps*10)==0:print('RENDER',i,'/',count,flush=True)
 p.stdin.close();rc=p.wait()
 if rc:raise RuntimeError('ffmpeg '+str(rc))
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',str(output)]))
 actual=float(probe['format']['duration'])
 assert abs(actual-min(220.56,args.preview if args.preview else 220.56))<.3,actual
 qc={'source':'Original owner-owned Trojan-Horse 60sec art','scenes':16,'unique_storyboard_beats':68,'created_new_scene_backdrops':True,'video':str(output),'duration':actual,'native_paint_size':[540,960], 'render_dimensions':[args.width,args.height], 'render_fps':args.fps, 'original_voice_hash_verified':h, 'subtitles_phrase_estimated':True,'owner_approved':False,'editorial_visual_quality_pass':False,'published':False}
 output.with_suffix('.qc.json').write_text(json.dumps(qc,indent=2,ensure_ascii=False),encoding='utf8')
 print('RENDER_DONE',output,output.stat().st_size,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--voice',default=str(ROOT/'audio.wav'))
 p.add_argument('--output',default=str(ROOT/'ODISSEIA_V35_2D_NOVOS_CENARIOS_NAO_PUBLICAR.mp4'))
 p.add_argument('--width',type=int,default=720)
 p.add_argument('--height',type=int,default=1280)
 p.add_argument('--fps',type=int,default=30)
 p.add_argument('--crf',type=int,default=21)
 p.add_argument('--preview',type=float,default=0)
 p.add_argument('--contact',action='store_true')
 args=p.parse_args()
 if args.contact:contact(Path(args.output).with_suffix('.jpg'))
 else:render(args)