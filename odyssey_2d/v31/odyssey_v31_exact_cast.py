#!/usr/bin/env python3
"""V30 original 2D Trojan Odysseus puppet integrated across all 16 scenes.
This remains technical QC until all scenes pass the owner's editorial standard.
"""
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0,'/mnt/data')
import odyssey_v29_polyphemus as film
import troia_puppet_rig_v30 as puppet
from troia_cyclops_art_v31 import cyclops
old=film.old
previous_actor=old.actor

def canon_actor(draw,x,feet,height,role='odysseus',t=0,action='idle',scale=1,**kw):
    if role=='cyclops':
        return cyclops(draw,x,feet,height*scale,t,action)
    if role!='odysseus':
        return previous_actor(draw,x,feet,height,role,t,action,scale=scale,**kw)
    if old.CANVAS is None:return previous_actor(draw,x,feet,height,role,t,action,scale=scale,**kw)
    lay=Image.new('RGBA',old.CANVAS.size,(0,0,0,0))
    h=height*scale
    p=0.75 if action in ('draw','aim','push') else .5
    info=puppet.draw_puppet(lay,x,feet,h,t,action,p)
    old.CANVAS.paste(lay,(0,0),lay)
    return info

old.actor=canon_actor
# One callback supplies all storyboard actions. Altering the cast does not
# alter the original voice or produce extra duplicate clip loops.
old.frame=film.shot_frame
if __name__=='__main__':old.main()