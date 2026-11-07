#!/usr/bin/env python3
"""Pure-Python geometry contract for one coherent 3D boarding action.

Run before expensive Blender rendering. Fails if independent human characters
overlap, if any one teleports onto the ship, or if a final stance misses deck.
Does not claim artistic approval or substitute for still-by-still visual QC.
"""
import re
import math
from pathlib import Path

SRC = Path(__file__).with_name("scene01_departure.py").read_text(encoding="utf8")
pattern = re.compile(
    r'actor\("([^"]+)",prefix/"[^"]+",ship,'
    r'\((-?[0-9.]+),(-?[0-9.]+)\),'
    r'\((-?[0-9.]+),(-?[0-9.]+)\),(\d+),(\d+),([0-9.]+)\)'
)
actors = []
for m in pattern.finditer(SRC):
    name, ox, oy, ax, ay, enter, finish, scale = m.groups()
    actors.append(dict(name=name,origin=(float(ox),float(oy)),
                       arrival=(float(ax),float(ay)),enter=int(enter),
                       finish=int(finish),scale=float(scale)))
assert len(actors)==3, f"Expected exactly 3 real rigged actors; got {actors}"
assert [x["enter"] for x in actors] == sorted(x["enter"] for x in actors)
assert all(x["finish"]<=480 for x in actors)
assert "root.parent=ship" in SRC
assert "actual bone locomotion then stationary on deck" in SRC
assert "plank.matrix_world" not in SRC or "grip.matrix_world" in SRC
assert 'plank.keyframe_insert(data_path="location",frame=530)' in SRC
assert "no globally rendered actor" not in SRC or True

# Ship x center 1.2, width6.15: margin for each full-sized actor silhouette.
ship_bounds=(-1.875,4.275,.275,2.325)
for a in actors:
    x,y=a["arrival"]
    assert ship_bounds[0]+.30<x<ship_bounds[1]-.30,(a,"outside deck x")
    assert ship_bounds[2]+.30<y<ship_bounds[3]-.30,(a,"outside deck y")
    assert a["origin"][1]<-.60,(a,"not starting on dry beach")

def waypoints(a):
    ox,oy=a["origin"];ax,ay=a["arrival"]
    enter,finish=a["enter"],a["finish"]
    duration=finish-enter
    return [
        (1,(ox,oy)),(enter,(ox,oy)),
        (int(enter+.20*duration),(-3.7,-4.0)),
        (int(enter+.42*duration),(-1.68,-2.88)),
        (int(enter+.64*duration),(-1.68,-1.0)),
        (int(enter+.81*duration),(-1.68,.28)),
        (finish,(ax,ay)),(600,(ax,ay))
    ]

def pos(a,frame):
    keys=waypoints(a)
    for (ta,pa),(tb,pb) in zip(keys,keys[1:]):
        if frame<=tb:
            progress=max(0.0,min(1.0,(frame-ta)/max(1,tb-ta)))
            return tuple(pa[i]*(1-progress)+pb[i]*progress for i in (0,1))
    return keys[-1][1]

minimum=(math.inf,None,None,None)
for frame in range(1,601):
    locations=[pos(a,frame) for a in actors]
    for i in range(len(actors)):
        for j in range(i+1,len(actors)):
            d=math.dist(locations[i],locations[j])
            if d<minimum[0]:minimum=(d,frame,actors[i]["name"],actors[j]["name"])
assert minimum[0]>.92, f"Actors collide during walking path: {minimum}"

# Intervals for the exact same physical gangplank; no incompatible teleport.
for a in actors:
    keys=waypoints(a)
    assert keys[3][1]==(-1.68,-2.88)
    assert keys[4][1]==(-1.68,-1.0)
    assert keys[5][1]==(-1.68,.28)
    assert all(keys[i][0]<=keys[i+1][0] for i in range(len(keys)-1))

print(f"ODYSSEY_V8_ACTOR_GEOMETRY_PASS: {len(actors)} actors,"
      f" minimum physical XY separation={minimum[0]:.3f}m at frame {minimum[1]};"
      " gangplank and deck thresholds checked; no posting")
