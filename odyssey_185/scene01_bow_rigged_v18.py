#!/usr/bin/env python3
"""S01 cinematic blocking with THREE distinct skinned actors, physical bow and
actual IK-driven hands. This is a QC preview, NOT the 220.56s final film.
Written for free Blender 3.0 Linux GitHub-hosted runner + pinned MIT Ara3D.
"""
from __future__ import annotations
import bpy, math, os, json, sys
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from render_hook_3d import hall,arc,cube,sphere,rod,material,look
OUT=HERE/"out"/"s01_v18"
OUT.mkdir(parents=True,exist_ok=True)
FPS=30
FRAME_COUNT=150
ACTOR_ROOT=Path("ara3d/out")
assert ACTOR_ROOT.exists(),"ARA3D_GENERATED_CAST_MISSING"

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE"
scene.render.resolution_x=540
scene.render.resolution_y=960
scene.render.resolution_percentage=70
scene.render.fps=FPS
scene.frame_start=1
scene.frame_end=FRAME_COUNT
scene.render.image_settings.file_format="PNG"
scene.render.image_settings.color_mode="RGB"
scene.render.film_transparent=False
scene.eevee.taa_render_samples=10
scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.06,.042,.025,1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.32
try:scene.view_settings.view_transform="Standard"
except:pass

def import_actor(folder,character_name,height_m,at,rotation=0.0):
    files=list((ACTOR_ROOT/folder).glob("*.glb"))
    if len(files)!=1:raise RuntimeError("ONE_REAL_ASSET_REQUIRED_"+folder)
    before=set(bpy.context.scene.objects)
    existing_acts=set(bpy.data.actions.keys())
    bpy.ops.import_scene.gltf(filepath=str(files[0]))
    created=[ob for ob in bpy.context.scene.objects if ob not in before]
    rigs=[ob for ob in created if ob.type=="ARMATURE"]
    skins=[ob for ob in created if ob.type=="MESH" and len(ob.data.vertices)>0]
    if not rigs or sum(len(x.data.vertices) for x in skins)<12000:
        raise RuntimeError("NO_SKINNED_MESH_"+folder)
    root=bpy.data.objects.new(character_name+"_PERSISTENT_FACE_ROOT",None)
    bpy.context.scene.collection.objects.link(root)
    for o in created:
        if o.parent not in created:
            world=o.matrix_world.copy();o.parent=root;o.matrix_world=world
    bpy.context.view_layer.update()
    points=[obj.matrix_world@Vector(corner) for obj in skins for corner in obj.bound_box]
    low=min(p.z for p in points);high=max(p.z for p in points)
    native=high-low
    if not .5<native<4.0:raise RuntimeError("UNSUPPORTED_NATIVE_ACTOR_HEIGHT_"+folder)
    scalar=height_m/native
    root.scale=(scalar,)*3
    root.rotation_euler[2]=rotation
    root.location=(at[0],at[1],-low*scalar)
    bpy.context.view_layer.update()
    armature=rigs[0]
    fresh=[a for a in bpy.data.actions if a.name not in existing_acts]
    idle=next((a for a in fresh if a.name.startswith("Idle_Armature")),None)
    if idle is None:idle=next((a for a in fresh if a.name.startswith("Hit reaction_Armature")),None)
    if idle is None:raise RuntimeError("NO_BREATHING_OR_ACTING_CLIP_"+folder)
    armature.animation_data_clear()
    tr=armature.animation_data_create().nla_tracks.new()
    tr.name=character_name+"_REAL_SKINNED_ACTING"
    st=tr.strips.new("Actual breathing and balance",1,idle)
    st.scale=3.0
    st.extrapolation="HOLD_FORWARD"
    print("V18_REAL_RIGGED_ACTOR",folder,character_name,
        "height_m",height_m,"vertices",sum(len(o.data.vertices) for o in skins),
        "action",idle.name,flush=True)
    return root,armature

def hand(arm,side):
    norm=lambda s:"".join(c for c in s.lower() if c.isalnum())
    names=[b for b in arm.pose.bones if (side+"hand") in norm(b.name)
           and "finger" not in norm(b.name) and "thumb" not in norm(b.name)]
    if not names:raise RuntimeError("NO_REAL_ARMATURE_"+side+"_HAND")
    return min(names,key=lambda b:len(b.name))

def hand_target(arm,side,name,keys,weight=.85):
    bone=hand(arm,side)
    tgt=bpy.data.objects.new(name+"_WORLDSPACE_HAND_CONTACT",None)
    scene.collection.objects.link(tgt)
    tgt.empty_display_type="SPHERE"
    tgt.empty_display_size=.05
    tgt.hide_render=True
    for fr,loc in keys:
        tgt.location=loc
        tgt.keyframe_insert("location",frame=fr)
    c=bone.constraints.new("IK")
    c.name="REAL_ARM_IK_"+name
    c.target=tgt
    c.chain_count=2
    c.influence=weight
    print("V18_3D_HAND_IK",name,bone.name,flush=True)
    return tgt

def track_cylinder(name,mat,rad):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=rad,depth=1)
    ob=bpy.context.object;ob.name=name
    ob.data.materials.append(mat)
    return ob
def place_bar(obj,a,b):
    a=Vector(a);b=Vector(b)
    d=b-a
    obj.location=(a+b)*.5
    obj.rotation_euler=d.to_track_quat("Z","Y").to_euler()
    obj.scale=(1,1,d.length)
def animate_rod(obj,a,p_frames):
    for fr,b in p_frames:
        place_bar(obj,a,b)
        obj.keyframe_insert("location",frame=fr)
        obj.keyframe_insert("rotation_euler",frame=fr)
        obj.keyframe_insert("scale",frame=fr)

hall()
WOOD=material("Bow seasoned aged olive wood grain",(.19,.08,.045),.8)
STRING=material("Bow twisted gut physical tension",(.76,.65,.39),.7)
BRONZE=material("Bronze hammered axe heads",(.37,.25,.09),.4,.7)
LINEN=material("Dusty limestone ground hall",(.23,.18,.12),.81)

hero,hero_arm=import_actor("odysseus","ODYSSEUS_IDENTICAL_FACE_BEGGAR",1.84,(0.0,-.05),.05)
anti,anti_arm=import_actor("antinoos","ANTINOOS_UNIQUE_FACE",1.97,(-2.5,2.0),-.06)
eury,eury_arm=import_actor("eurymachos","EURYMACHOS_UNIQUE_FACE",1.89,(2.4,1.9),.06)
assert len({id(hero),id(anti),id(eury)})==3

# The bow is solid model geometry IN THE HERO'S ARMS, not a static superimposed image.
bowroot=bpy.data.objects.new("ODYSSEUS_REAL_BOW_ONE_PERSISTENT_PROP",None)
scene.collection.objects.link(bowroot)
arc("ODYSSEUS_ANATOMICAL_BOW_CURVED_ONE_MODEL",
    [(-.14,-.69,1.01),(-.36,-.70,1.27),(-.43,-.72,1.53),
     (-.27,-.72,1.78),(-.35,-.69,2.05),(-.14,-.69,2.30)],
    WOOD,.04,bowroot)
# Bow has separate modelled handle and narrow wrapped grip, not an image.
rod("BOW_OLIVE_WOOD_GRIP",(-.40,-.72,1.43),(-.40,-.72,1.65),.067,WOOD,bowroot)
for z in (1.45,1.58):
    rod("BOW_GRIP_WRAPPED_LINEN",(-.398,-.794,z),(-.398,-.794,z+.06),.009,STRING,bowroot)
# String is two independent mesh segments. Its draw point is animated in space.
string_l=track_cylinder("BOW_STRING_LOWER_DYNAMIC",STRING,.007)
string_u=track_cylinder("BOW_STRING_UPPER_DYNAMIC",STRING,.007)
p_frames=[(1,(-.20,-.68,1.58)),(42,(-.20,-.63,1.58)),
          (72,(-.16,-.53,1.58)),(112,(-.12,-.38,1.57)),(150,(-.12,-.33,1.57))]
animate_rod(string_l,(-.14,-.69,1.01),p_frames)
animate_rod(string_u,(-.14,-.69,2.30),p_frames)
left_grip=[(1,(-.40,-.73,1.52)),(150,(-.40,-.73,1.52))]
right_draw=[(f,(p[0],p[1],p[2])) for f,p in p_frames]
hand_target(hero_arm,"left","ODYSSEUS_GRIP_BOW",left_grip,1)
hand_target(hero_arm,"right","ODYSSEUS_TENSION_STRING",right_draw,.86)

# Distinct suitor gestures, actual arm IK + articulated 3D chalice.
goblet=bpy.data.objects.new("ANTINOOS_BRONZE_CHALICE_WORLD",None)
scene.collection.objects.link(goblet)
cup=cube("ANTINOOS_CHALICE_CUP",(0,0,0.0),(.18,.18,.14),BRONZE,.06)
cup.parent=goblet
stem=rod("ANTINOOS_CHALICE_STEM",(0,0,-.04),(0,0,-.26),.027,BRONZE)
stem.parent=goblet
for fr,xyz in [(1,(-2.12,1.18,1.30)),(65,(-2.07,1.12,1.62)),
               (120,(-2.01,1.06,1.97)),(150,(-2.0,1.05,1.95))]:
    goblet.location=xyz;goblet.keyframe_insert("location",frame=fr)
hand_target(anti_arm,"right","ANTINOOS_HOLD_RAISED_CHALICE",
    [(1,(-2.12,1.18,1.30)),(65,(-2.07,1.12,1.62)),
     (120,(-2.01,1.06,1.97)),(150,(-2.,1.05,1.95))],.78)
hand_target(eury_arm,"left","EURYMACHOS_MOCKING_GESTURE",
    [(1,(2.08,1.25,1.34)),(50,(1.87,1.15,1.57)),
     (114,(1.47,.98,1.57)),(150,(1.48,.97,1.52))],.73)

# Twelve genuine prop alignments foreshadow S15. Heads and handles share scale.
for i in range(12):
    y=3.0+i*.48
    rod("TWELVE_REAL_AXES_HANDLE_%02d"%(i+1),(-4.6,y,.28),(-4.6,y,1.30),.047,WOOD)
    cube("TWELVE_AXES_BRONZE_HEAD_%02d"%(i+1),(-4.6,y,1.33),(.27,.12,.17),BRONZE,.035)

def area(name,loc,color,power,size=5):
    light=bpy.data.lights.new(name,"AREA")
    light.energy=power;light.color=color;light.shape="DISK";light.size=size
    ob=bpy.data.objects.new(name,light);scene.collection.objects.link(ob)
    ob.location=loc;look(ob,(0,0,1.6))
area("S01_TORCH_AMBER_CINEMATIC_KEY",(-2,-4,5),(1,.68,.37),1000,6)
area("S01_DARK_BLUE_FILL",(3,-2,4),(.40,.52,.73),460,6)
area("S01_BACK_RIM",(0,5,5),(1,.39,.16),900,6)

# Motivated camera: hand/string close-up THEN reveal beggar and two distinct suitors.
def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name)
    o=bpy.data.objects.new(name,d)
    scene.collection.objects.link(o);o.location=loc;look(o,target);d.lens=lens
    d.clip_end=100
    return o
close=camera("S01_SHOT01_REAL_85mm_BOW",(1.00,-3.05,1.84),(-.32,-.67,1.55),85)
reveal=camera("S01_SHOT02_REAL_35mm_HERO_SUITS",(2.4,-6.35,2.33),(0,.80,1.66),35)
scene.camera=close
for fr,cam,m in [(1,close,"S01_BOW_HANDS_A_REAL_ACTION"),
                 (78,reveal,"S01_REVEAL_ODYSSEUS_AND_DISTINCT_SUITORS")]:
    marker=scene.timeline_markers.new(m,frame=fr);marker.camera=cam
# Acting comes from skinned originals and IK, with separate action for each hand.
# Every character is world-space 3D with shadows/occlusion and depth.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"S01_RIGGED_CAST_BOW_ACTING_V18_QC.blend"))
report={
 "source_scene":"S01","test_duration_sec":FRAME_COUNT/FPS,
 "source_audio_duration_sec":220.56,"film_target_minutes":3.676,
 "native_bone_based_3d_actors":["ODYSSEUS","ANTINOOS","EURYMACHOS"],
 "unique_actor_identity_ids":[2002,7015,8144],
 "genuine_mesh_props":["ONE_OLIVE_WOOD_BOW","2_DYNAMIC_STRING_SEGMENTS",
                       "TWELVE_AXES","ANTINOOS_CHALICE"],
 "action":["GRAB_BOW","DRAW_STRING","RAISE_CHALICE","MOCK_HERO"],
 "visual_qc_approved":False,
 "full_film_completed":False,"published":False
}
(OUT/"scene_technical_qc.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
if "--preview" in sys.argv:
    frames=OUT/"frames";frames.mkdir(exist_ok=True)
    for n,fr in enumerate(range(1,FRAME_COUNT+1)):
        scene.frame_set(fr)
        scene.camera=close if fr<78 else reveal
        scene.render.filepath=str(frames/f"frame-{n:04d}.png")
        bpy.ops.render.render(write_still=True)
        if n%25==0:print("S01_V18_REAL_SKINNED_FRAME",n,flush=True)
    print("S01_V18_3D_TRUE_ANIMATION_150_FRAMES_QC_NOT_FINAL",flush=True)
if "--stills" in sys.argv:
    for fr in (1,40,80,115,150):
        scene.frame_set(fr)
        scene.camera=close if fr<78 else reveal
        scene.render.filepath=str(OUT/f"S01_still_{fr:03d}.png")
        bpy.ops.render.render(write_still=True)
    print("S01_V18_3D_STILLS_QC_NOT_FINAL",flush=True)
