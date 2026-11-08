#!/usr/bin/env python3
"""Objective V35F editorial preflight; does not certify animation artistry."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse,bisect,json,subprocess,hashlib,math
import numpy as np

W,H=180,320
FPS=3

def analyze(movie,manifest,out_dir):
    out_dir.mkdir(parents=True,exist_ok=True)
    obj=json.loads(manifest.read_text(encoding='utf8'))
    shots=obj['shots'];starts=[s['start_seconds_estimate'] for s in shots]
    assert len(shots)==68 and len({s['shot_id'] for s in shots})==68
    proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-vf',f'fps={FPS},scale={W}:{H}', '-pix_fmt','rgb24','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    framebytes=W*H*3
    prior={};scores={i:[] for i in range(len(shots))}; mid_frames={};dists={}
    k=0
    while True:
        data=proc.stdout.read(framebytes)
        if not data:break
        if len(data)!=framebytes:raise RuntimeError('truncated raw frame')
        t=k/FPS
        idx=max(0,min(len(shots)-1,bisect.bisect_right(starts,t)-1))
        image=np.frombuffer(data,dtype=np.uint8).reshape(H,W,3).copy()
        if idx in prior:
            mean=np.abs(image.astype(np.int16)-prior[idx].astype(np.int16)).mean()
            scores[idx].append(float(mean))
        prior[idx]=image
        midpoint=(shots[idx]['start_seconds_estimate']+shots[idx]['end_seconds_estimate'])/2
        if idx not in dists or abs(t-midpoint)<dists[idx]:
            mid_frames[idx]=image.copy();dists[idx]=abs(t-midpoint)
        k+=1
    code=proc.wait(timeout=30)
    if code:raise RuntimeError('ffmpeg decoding failed '+str(code))
    results=[]
    for i,s in enumerate(shots):
        vals=scores[i]
        mean=float(np.mean(vals)) if vals else 0
        results.append({'shot_id':s['shot_id'],'scene':s['scene'],'narrative_action':s.get('narrative_action'),
                        'within_shot_motion_mean_rgb_delta':round(mean,3),
                        'frames_with_comparable_neighbors':len(vals),
                        'potential_static_or_weak_action':mean<1.7})
    duplicates=[]
    for i in range(len(shots)):
        if i not in mid_frames:continue
        a=mid_frames[i].astype(np.int16)
        for j in range(i+1,len(shots)):
            if j not in mid_frames:continue
            # Reusing the same composition for unrelated events is more serious
            # than maintaining scenic geography across adjacent shots.
            if abs(i-j)<2:continue
            b=mid_frames[j].astype(np.int16)
            mad=float(np.abs(a-b).mean())
            if mad<3.5: duplicates.append({'first':shots[i]['shot_id'],'second':shots[j]['shot_id'],'mean_rgb_delta':round(mad,2)})
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',11)
    for g in range(2):
        canvas=Image.new('RGB',(6*W,6*(H+24)),'#e5d4b1');d=ImageDraw.Draw(canvas)
        for local in range(34):
            i=34*g+local
            if i not in mid_frames:continue
            x=(local%6)*W;y=(local//6)*(H+24)
            canvas.paste(Image.fromarray(mid_frames[i]),(x,y))
            d.text((x+5,y+H+4),shots[i]['shot_id'],font=font,fill='#242424')
        canvas.save(out_dir/f'CONTACT_V35F_{g+1}.jpg',quality=86)
    warnings=[]
    weak=[r for r in results if r['potential_static_or_weak_action']]
    if weak:warnings.append(f'{len(weak)} shots with insufficient pixel motion at 3fps')
    if duplicates:warnings.append(f'{len(duplicates)} nonadjacent near-identical visual pairs')
    report={'movie':str(movie),'frames_measured':k,'sample_fps':FPS,'narrated_shots':68,
            'potential_static_count':len(weak),'near_identical_distant_pairs':duplicates,
            'shots':results,'warnings':warnings,'human_visual_approved':False,
            'qc_status':'REVIEW_REQUIRED' if warnings else 'TECHNICAL_PASS_VISUAL_REVIEW_REQUIRED',
            'frame_differencing_not_proof_of_story_sync':True}
    (out_dir/'MOVEMENT_QC_V35F.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('MOTION_QC',json.dumps({k:report[k] for k in ('frames_measured','potential_static_count','qc_status','warnings')}),flush=True)
    for s in weak[:15]:print('WEAK_SHOT',s['shot_id'],s['within_shot_motion_mean_rgb_delta'],s['narrative_action'])
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--movie',required=True);p.add_argument('--manifest',required=True);p.add_argument('--out',required=True)
    args=p.parse_args()
    analyze(Path(args.movie),Path(args.manifest),Path(args.out))