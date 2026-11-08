"""V35E theatrical override.

Preserves *the exact* original Odysseus sprite in ALL appearances, including
the beggar/disguise passages; no generic actor stand-in. Dispatches 15 action
beats measured almost static in V35D to 15 distinct physical performances.
All previous V35D animation continues for the other 53 beats. QC only.
"""
import argparse
import render_v35d as prior
import active_performance_15 as revised
import focused_motion_v36 as manual

old=prior.old
actual_figure=old.man
def original_identity(d,x,y,h,t,pose='walk',role='sailor'):
    if role=='beggar':
        role='odysseus'
    return actual_figure(d,x,y,h,t,pose,role)
old.man=original_identity

class Performance:
    @staticmethod
    def affected(scene,beat):
        return revised.affected(scene,beat) or manual.affected(scene,beat)
    @staticmethod
    def act(d,canvas,shot,t,p):
        if revised.affected(shot['scene'],shot['beat']):
            return revised.act(d,canvas,shot,t,p)
        return manual.act(d,canvas,shot,t,p)

prior.movement=Performance

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--voice',default=str(prior.ROOT/'audio.wav'))
    p.add_argument('--output',default=str(prior.ROOT/'ODISSEIA_V35E_QC_NAO_PUBLICAR.mp4'))
    p.add_argument('--width',type=int,default=720)
    p.add_argument('--height',type=int,default=1280)
    p.add_argument('--fps',type=int,default=30)
    p.add_argument('--crf',type=int,default=19)
    p.add_argument('--preview',type=float,default=0)
    p.add_argument('--contact',action='store_true')
    args=p.parse_args()
    if args.contact:
        from pathlib import Path
        prior.contact(Path(args.output).with_suffix('.jpg'))
    else:
        prior.render(args)
