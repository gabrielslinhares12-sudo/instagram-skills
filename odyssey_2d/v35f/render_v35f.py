"""V35F: four final under-animated story beats enhanced.

Builds on original-film 2D sprites and V35E performances. QC-only 16 scenes.
"""
import argparse
import render_v35e as base
import final_motion_4 as correction
import active_performance_15 as prior_act

class CorrectedFifteen:
    @staticmethod
    def affected(scene,beat):
        return correction.affected(scene,beat) or prior_act.affected(scene,beat)
    @staticmethod
    def act(d,canvas,shot,t,p):
        if correction.affected(shot['scene'],shot['beat']):
            return correction.act(d,canvas,shot,t,p)
        return prior_act.act(d,canvas,shot,t,p)
base.revised=CorrectedFifteen

if __name__=='__main__':
    root=base.prior.ROOT
    p=argparse.ArgumentParser()
    p.add_argument('--voice',default=str(root/'audio.wav'))
    p.add_argument('--output',default=str(root/'ODISSEIA_V35F_QC_NAO_PUBLICAR.mp4'))
    p.add_argument('--width',type=int,default=720)
    p.add_argument('--height',type=int,default=1280)
    p.add_argument('--fps',type=int,default=30)
    p.add_argument('--crf',type=int,default=19)
    p.add_argument('--preview',type=float,default=0)
    p.add_argument('--contact',action='store_true')
    args=p.parse_args()
    if args.contact:
        from pathlib import Path
        base.prior.contact(Path(args.output).with_suffix('.jpg'))
    else:
        base.prior.render(args)
