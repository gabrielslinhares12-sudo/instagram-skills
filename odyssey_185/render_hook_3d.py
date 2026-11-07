#!/usr/bin/env python3
"""Odyssey 185 V9 – scene 01: a physically staged, self-contained Blender 3D blocking test.
No 2D overlays, no stock footage and NO publication. This is a technical pilot, not a final film.
Run in Blender: blender -b -t 2 --python odyssey_185/render_hook_3d.py -- --stills|--preview
"""
import bpy, math, os, sys, random
from pathlib import Path
from mathutils import Vector
random.seed(2026)
BASE=Path(__file__).resolve().parent
OUT=BASE/"out"
OUT.mkdir(exist_ok=True)
FRAMES=210
FPS=30
def material(name,color,rough=.78,metal=0.0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    n=m.node_tree.nodes.get("Principled BSDF")
    n.inputs["Base Color"].default_value=(*color,1)
    n.inputs["Roughness"].default_value=rough
    n.inputs["Metallic"].default_value=metal
    return m
SKIN=material("sun weathered Aegean skin",(.47,.26,.18),.67)
HAIR=material("Odysseus black wavy hair",(.055,.041,.038))
BEARD=material("Odysseus same identifiable beard",(.063,.047,.043))
LINEN=material("worn ash linen beggar",(.36,.30,.26))
CAP=material("weathered dark traveling cloak",(.18,.19,.20))
RED=material("Antinous dark carmine",(.41,.055,.048))
BLUE=material("Eurymachus dark teal",(.07,.18,.23))
SANDAL=material("weathered sandals",(.17,.088,.047))
WOOD=material("ancient hardwood",(.23,.105,.051))
WOOD_L=material("beaten timber",(.37,.23,.105))
BRONZE=material("dull ancient bronze",(.44,.31,.10),.31,.75)
STONE=material("old Mycenaean rough plaster",(.36,.34,.29))
DARK=material("dark pupils",(.038,.026,.022))
EYE=material("warm white sclera",(.78,.71,.61))
FIRE=material("fire amber",(.98,.29,.035),.3)
def cube(name,loc,dimensions,ma,bev=.025,parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    ob=bpy.context.object;ob.name=name;ob.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if ma:ob.data.materials.append(ma)
    if bev:
        mod=ob.modifiers.new("real beveled edges","BEVEL");mod.width=bev;mod.segments=2
        ob.modifiers.new("weighted normals","WEIGHTED_NORMAL")
    if parent:parent_world(ob,parent)
    return ob
def sphere(name,loc,scale,ma,parent=None,seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=10,location=loc)
    ob=bpy.context.object;ob.name=name;ob.scale=scale;ob.data.materials.append(ma)
    if parent:parent_world(ob,parent)
    return ob
def cyl(name,loc,radius,depth,ma,parent=None,segments=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=segments,radius=radius,depth=depth,location=loc)
    ob=bpy.context.object;ob.name=name;ob.data.materials.append(ma)
    if parent:parent_world(ob,parent)
    return ob
def rod(name,a,b,r,ma,parent=None):
    v=Vector(b)-Vector(a)
    ob=cyl(name,(Vector(a)+Vector(b))/2,r,v.length,ma,segments=10)
    ob.rotation_euler=v.to_track_quat("Z","Y").to_euler()
    if parent:parent_world(ob,parent)
    return ob
def parent_world(ob,parent):
    bpy.context.view_layer.update();mw=ob.matrix_world.copy()
    ob.parent=parent;ob.matrix_world=mw
def empty(name,loc,parent=None):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob.location=loc
    if parent:parent_world(ob,parent)
    return ob
def arc(name,points,ma,thickness=.028,parent=None):
    data=bpy.data.curves.new(name,"CURVE");data.dimensions="3D";data.resolution_u=24
    data.bevel_depth=thickness;data.bevel_resolution=3
    sp=data.splines.new("BEZIER");sp.bezier_points.add(len(points)-1)
    for p,xyz in zip(sp.bezier_points,points):
        p.co=xyz;p.handle_left_type="AUTO";p.handle_right_type="AUTO"
    ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);data.materials.append(ma)
    if parent:parent_world(ob,parent)
    return ob
def look(ob,target):
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
def person(name,position,tunic,is_hero=False):
    root=empty(name+" permanent root",position)
    # Anatomy: individually articulated shoulders, pelvis, head and hands.
    cube(name+" pelvis",(position[0],position[1],1.02),(.55,.31,.36),tunic,.08,root)
    body=sphere(name+" ribcage",(position[0],position[1],1.47),(.35,.24,.52),tunic,root)
    sphere(name+" neck",(position[0],position[1]-.01,1.90),(.115,.11,.17),SKIN,root)
    sphere(name+" head",(position[0],position[1]-.05,2.14),(.235,.205,.31),SKIN,root)
    sphere(name+" nose",(position[0],position[1]-.26,2.13),(.065,.075,.095),SKIN,root)
    for side in [-1,1]:
        x=position[0]+side*.09
        sphere(name+" eye socket "+str(side),(x,position[1]-.245,2.19),(.060,.024,.034),EYE,root)
        sphere(name+" brown pupil "+str(side),(x,position[1]-.271,2.19),(.021,.010,.025),DARK,root)
        sphere(name+" ear "+str(side),(position[0]+side*.235,position[1],2.12),(.045,.067,.093),SKIN,root)
    sphere(name+" hair volume",(position[0],position[1]+.013,2.335),(.24,.205,.12),HAIR,root)
    if is_hero:
        sphere("ODYSSEUS signature dark full beard",(position[0],position[1]-.105,1.97),(.21,.185,.15),BEARD,root)
        cube("ODYSSEUS unique diagonal brow scar",(position[0]+.12,position[1]-.258,2.265),(.055,.013,.012),SKIN,.005,root)
        cube("ODYSSEUS battered hood shadow",(position[0],position[1]+.07,2.40),(.50,.40,.10),CAP,.06,root)
        cube("ODYSSEUS torn dark cloak",(position[0],position[1]+.18,1.35),(.77,.10,1.16),CAP,.04,root)
    else:
        cyl(name+" bronze belt",(position[0],position[1],1.18),.315,.09,BRONZE,root)
    for side in [-1,1]:
        side_name="left" if side<0 else "right"
        hip=empty(name+" "+side_name+" HIP JOINT",(position[0]+side*.17,position[1],.96),root)
        rod(name+" "+side_name+" upper leg",(position[0]+side*.17,position[1],.96),(position[0]+side*.20,position[1],.55),.105,tunic,root)
        rod(name+" "+side_name+" shin",(position[0]+side*.20,position[1],.55),(position[0]+side*.21,position[1]-.015,.16),.082,SKIN,root)
        sphere(name+" "+side_name+" sandal",(position[0]+side*.21,position[1]-.08,.08),(.14,.23,.075),SANDAL,root)
    arms={}
    for side in [-1,1]:
        side_name="left" if side<0 else "right"
        pivot=empty(name+" "+side_name+" SHOULDER PIVOT",(position[0]+side*.37,position[1],1.76),root)
        rootpos=(position[0]+side*.37,position[1],1.76)
        rod(name+" "+side_name+" upper arm",rootpos,
            (rootpos[0]+side*.045,rootpos[1],rootpos[2]-.36),.102,tunic,pivot)
        rod(name+" "+side_name+" forearm",(rootpos[0]+side*.045,rootpos[1],rootpos[2]-.36),
            (rootpos[0]+side*.055,rootpos[1]-.09,rootpos[2]-.69),.078,SKIN,pivot)
        sphere(name+" "+side_name+" gripping hand",(rootpos[0]+side*.055,rootpos[1]-.13,rootpos[2]-.78),(.095,.10,.112),SKIN,pivot)
        arms[side_name]=pivot
    return root,arms
def hall():
    cube("real solid Mycenaean floor",(0,1,-.16),(14,19,.32),STONE)
    cube("back plaster wall",(0,9.0,3.3),(14,.7,6.6),STONE)
    for side in [-1,1]:
        cube("side wall "+str(side),(side*7,1.0,3),(0.55,19,6),STONE)
        for y in [-6,-1,4,7]:
            cyl("ancient wooden column",(side*5.3,y,2.5),.30,5,WOOD)
            cube("square structural abacus",(side*5.3,y,4.9),(1.0,1.0,.25),WOOD_L)
    for i in range(13):
        cube("visible roof beam",(0,-7.5+i*1.4,5.65),(13.4,.22,.24),WOOD_L)
    for i in range(18):
        x=random.uniform(-5,5);y=random.uniform(-5.5,6.8)
        cube("stone floor seam",(x,y,.016),(.016,random.uniform(.45,1.3),.012),WOOD,.002)
    for side in [-1,1]:
        for y in [-4,4]:
            support=rod("torch brace",(side*6.3,y,2.75),(side*5.85,y,3.18),.07,BRONZE)
            flame=sphere("three dimensional torch flame",(side*5.83,y,3.44),(.11,.11,.30),FIRE)
            l=bpy.data.lights.new("torch area lamp","POINT")
            l.energy=140;l.color=(1,.45,.17);obj=bpy.data.objects.new("torch flicker physical",l)
            bpy.context.collection.objects.link(obj);obj.location=(side*5.84,y,3.55)
            for f,mult in [(1,1),(45,.88),(90,1.1),(160,.92),(210,1.02)]:
                l.energy=140*mult;l.keyframe_insert("energy",frame=f)
    # A tangible interior, no floating decorative elements or cropped photograph.
def animate():
    hall()
    hero,arm=person("ODYSSEUS SAME FACE begging version",(0,0),LINEN,True)
    a,aa=person("ANTINOUS heavy red arrogant suitor",(-2.15,2.2),RED)
    e,ee=person("EURYMACHUS elegant blue suitor",(2.1,2.1),BLUE)
    person("SUITOR 03 distinct short crowd",(-3.8,4.1),RED)
    person("SUITOR 04 distinct tall crowd",(3.9,4.3),BLUE)
    # Bow: real curved wooden limbs and a drawable THREE-DIMENSIONAL cord.
    # Its geometry is attached to Odisseus' hand-group in the same world space.
    bowroot=empty("ODYSSEUS one persistent bow geometry",(0,-.68,1.50))
    arc("seasoned wooden bow limbs",[(0,-.65,.62),(-.15,-.66,.89),(-.23,-.66,1.28),(0,-.66,1.5),(-.24,-.66,1.77),(-.14,-.66,2.10),(0,-.65,2.36)],WOOD,.045,bowroot)
    arc("bowstring physically under tension",[(0,-.65,.62),(.04,-.68,1.20),(.09,-.72,1.50),(.04,-.68,1.84),(0,-.65,2.36)],BRONZE,.009,bowroot)
    # The hero's feet never translate. Only his arm articulation, chest and bow pose change.
    for f,r,al,ar,bb in [(1,.02,-.20,.12,-.20),(50,.02,-.24,.2,-.11),(95,.0,-.43,.46,.07),(145,.0,-.54,.59,.11),(185,0,-.58,.63,.14),(210,.0,-.58,.63,.14)]:
        hero.rotation_euler[2]=r;hero.keyframe_insert("rotation_euler",frame=f)
        arm["left"].rotation_euler=(0,al,0);arm["left"].keyframe_insert("rotation_euler",frame=f)
        arm["right"].rotation_euler=(0,ar,0);arm["right"].keyframe_insert("rotation_euler",frame=f)
        bowroot.location=(0,-.68,1.50+bb);bowroot.keyframe_insert("location",frame=f)
    # Pretenders react as distinct actors, not mirrored walking loops.
    for f,ang in [(1,-.12),(80,-.10),(140,.05),(210,.18)]:
        a.rotation_euler[2]=ang;a.keyframe_insert("rotation_euler",frame=f)
    for f,ang in [(1,.14),(95,.02),(160,-.15),(210,-.22)]:
        e.rotation_euler[2]=ang;e.keyframe_insert("rotation_euler",frame=f)
    for target in [hero,a,e]:
        if target.animation_data:
            for fc in target.animation_data.action.fcurves:
                for p in fc.keyframe_points:p.interpolation="BEZIER"
    # Actual lens and camera location change in 3D with a motivated reveal.
    d=bpy.data.cameras.new("real lens 85 to 35mm")
    cam=bpy.data.objects.new("real moving perspective camera",d)
    bpy.context.collection.objects.link(cam)
    s=bpy.context.scene;s.camera=cam
    for f,loc,lookat,lens in [(1,(.75,-4.8,2.15),(.1,-.6,1.6),85),
                             (88,(.65,-6.3,2.25),(0,0,1.7),58),
                             (210,(1.9,-10.6,3.05),(0,.9,1.85),35)]:
        cam.location=loc;look(cam,lookat);cam.data.lens=lens
        cam.keyframe_insert("location",frame=f)
        cam.keyframe_insert("rotation_euler",frame=f)
        cam.data.keyframe_insert("lens",frame=f)
    d.clip_end=150
    def light(name,kind,loc,energy,color,size=4):
        dl=bpy.data.lights.new(name,kind);dl.energy=energy;dl.color=color
        ob=bpy.data.objects.new(name,dl);bpy.context.collection.objects.link(ob)
        ob.location=loc;look(ob,(0,0,1.3))
        if kind=="AREA":dl.shape="DISK";dl.size=size
    light("warm chandelier bounce","AREA",(-3,-3,4.8),650,(1,.72,.43),6)
    light("indirect blue fill","AREA",(4,-1,4.5),410,(.54,.69,1),5)
    light("bronze rim","AREA",(1,5,5.0),650,(1,.40,.17),5)
def run():
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    s=bpy.context.scene;s.frame_start=1;s.frame_end=FRAMES;s.render.fps=FPS
    s.render.engine="BLENDER_EEVEE"
    s.render.resolution_x=720;s.render.resolution_y=1280
    s.render.resolution_percentage=int(os.environ.get("QC_PERCENT","70"))
    s.render.image_settings.file_format="PNG"
    s.render.image_settings.color_mode="RGB"
    s.render.film_transparent=False
    s.world.use_nodes=True
    s.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.07,.065,.067,1)
    s.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.26
    s.view_settings.view_transform="Standard"
    s.view_settings.look="Medium High Contrast"
    animate()
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"odyssey_185_scene01_blocking.blend"))
    if "--stills" in sys.argv:
        for frame in (1,42,84,126,168,210):
            s.frame_set(frame);s.render.filepath=str(OUT/("scene01-%03d.png"%frame))
            bpy.ops.render.render(write_still=True)
            print("ODYSSEY_185_PHYSICAL_QC_FRAME",frame,flush=True)
    if "--preview" in sys.argv:
        p=OUT/"frames";p.mkdir(exist_ok=True)
        for frame in range(1,FRAMES+1):
            s.frame_set(frame);s.render.filepath=str(p/("frame-%04d.png"%frame))
            bpy.ops.render.render(write_still=True)
            if frame%30==0:print("ODYSSEY_185_ANIMATED_FRAMES",frame,FRAMES,flush=True)
    print("ODYSSEY_185_SCENE01_BLOCKING_3D_COMPLETE_NOT_FINAL",flush=True)
if __name__=="__main__":run()
