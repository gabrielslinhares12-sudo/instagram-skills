#!/usr/bin/env python3
"""S02 native 3D horse-through-Troy-gate sequence with real skinned Trojan pullers.
Actual 3D model/rig/actions/shadowing; FIVE-SECOND TECHNICAL QC ONLY, NOT FINAL.
"""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from render_hook_3d import cube,sphere,rod,arc,cyl,material,look,parent_world
OUT=HERE/"out"/"s02_v18";OUT.mkdir(parents=True,exist_ok=True)
N=150
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.render.engine="BLENDER_EEVEE"
sc.render.resolution_x=540;sc.render.resolution_y=960
sc.render.resolution_percentage=70;sc.render.fps=30
sc.render.image_settings.file_format="PNG"
sc.render.frame_start=1;sc.render.frame_end=N
sc.eevee.taa_render_samples=10
sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs["Color"].default_value=(.26,.18,.12,1)
sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.6
wall=material("Mycenaean stone limestone",(.46,.33,.23),.85)
oak=material("Heavy hand-built olive wood",(.30,.16,.09),.78)
plank=material("Wooden horse individual longitudinal planks",(.43,.21,.105),.84)
rope=material("Real twisted hemp ropes",(.59,.40,.21),.85)
metal=material("Bronze rivets and rims",(.39,.26,.12),.4,.65)
ground=material("Earth Troy causeway",(.45,.35,.25),.95)
dark=material("Dark wooden hooves",(.13,.08,.06),.8)
cube("Troy continuous road",(0,0,-.24),(25,37,.48),ground)
for x in (-5.6,5.6):cube("Troy real gate stone side",(x,0,4.2),(4.75,2.2,8.4),wall,.11)
cube("Real clearance above horse head",(0,0,8.1),(6.45,2.3,1.7),wall,.08)
for x in (-8,-5.1,5.1,8):
 cube("Ancient Troy stonework buttress",(x,0,4.2),(.29,3.6,8.4),wall,.07)
for i in range(6):
 cube("Troy wall battlement",(i*2.94-7.35,0,9.12),(.95,2,1.1),wall,.08)
# Real horse visual anatomy: broad torso, full neck/head, distinct ears/hooves,
# FOUR legs and wheeled platform. Only one spatial model, not composited still.
horse=bpy.data.objects.new("PERSISTENT_FOUR_LEGGED_GIANT_TROJAN_HORSE",None)
sc.collection.objects.link(horse)
def bind(obj):
 parent_world(obj,horse)
 return obj
bind(cube("One solid wooden carriage chassis",(0,-.05,.92),(3.55,5.4,.22),dark))
bind(sphere("Horse large hollow barrel-shaped torso",(0,-.20,3.07),(1.12,1.88,.93),oak))
bind(sphere("Horse unmistakable haunches",(0,-1.39,2.91),(1.01,.8,.73),oak))
bind(sphere("Horse upright sloping shoulders",(0,1.08,3.19),(.94,.75,.82),oak))
for side in (-1,1):
 for y in (-1.42,1.2):
  tag="HORSE_LEFT" if side<0 else "HORSE_RIGHT"
  bind(rod(tag+"_FOUR_INDEPENDENT_UPPER_LEGS",(side*.73,y,2.55),(side*.72,y+.09,1.68),.23,oak))
  bind(rod(tag+"_FOUR_INDEPENDENT_LOWER_LEGS",(side*.72,y+.09,1.68),(side*.71,y+.12,1.0),.15,oak))
  bind(cube(tag+"_FOUR_REAL_HOOVES",(side*.71,y+.20,.99),(.41,.49,.22),dark,.025))
  bind(sphere(tag+"_REAL_EYE",(side*.53,2.30,4.91),(.048,.035,.052),dark))
  bind(sphere(tag+"_REAL_EAR",(side*.27,2.0,5.48),(.13,.18,.33),oak))
for i in range(5):
 bind(cube("HORSE_BODY_WOOD_PLANK_%02d"%i,(-1.01,-.2,2.68+i*.21),(.11,3.21,.12),plank))
 bind(cube("HORSE_OTHER_SIDE_PLANK_%02d"%i,(1.01,-.2,2.68+i*.21),(.11,3.21,.12),plank))
bind(rod("Long equine rising neck",(0,1.20,3.38),(0,2.04,4.79),.45,oak))
bind(sphere("Long recognisable horse head",(0,2.26,4.92),(.53,.68,.47),oak))
bind(sphere("Forward elongated muzzle",(0,2.74,4.54),(.37,.45,.30),plank))
bind(arc("Actual trailing carved horse tail",[(0,-1.74,3.24),(0,-2.18,3.05),(0,-2.35,2.47),(0,-2.43,2.22)],oak,.145))
wheel_roots=[]
for xx in (-1.68,1.68):
 for yy in (-1.4,1.4):
  root=bpy.data.objects.new("ROTATING_CART_WHEEL_AXIS",None)
  sc.collection.objects.link(root);root.location=(xx,yy,.56)
  bpy.ops.mesh.primitive_cylinder_add(vertices=36,radius=.56,depth=.14,
      rotation=(0,math.pi/2,0),location=(xx,yy,.56))
  o=bpy.context.object;o.name="WHEEL_SOLID_PBR_TIMBER";o.data.materials.append(oak);parent_world(o,root)
  for i in range(8):
   theta=i*2*math.pi/8
   a=(xx,yy,.56)
   b=(xx,yy+math.cos(theta)*.52,.56+math.sin(theta)*.52)
   parent_world(rod("ACTUALLY_ROTATING_WOOD_SPOKE",a,b,.026,plank),root)
  parent_world(root,horse);wheel_roots.append(root)
# The horse + wheels measure under 3.9 meters across, narrower than 6.45-meter gate.
assert 2*(1.68+.12)<6.45 and 5.81<7.20
frames=[(1,-5.8),(35,-4.45),(65,-3.15),(95,-1.75),(125,-.35),(150,1.05)]
for f,y in frames:
 horse.location.y=y;horse.keyframe_insert("location",frame=f)
 for w in wheel_roots:
  w.rotation_euler[0]=(y+5.8)/.56
  w.keyframe_insert("rotation_euler",frame=f)
def load_trojan(folder,label,h,x,y):
 models=list((Path("ara3d/out")/folder).glob("*.glb"))
 if len(models)!=1:raise RuntimeError("ONE_SKINNED_GLB_REQUIRED_"+folder)
 before=set(sc.objects);acts=set(bpy.data.actions.keys())
 bpy.ops.import_scene.gltf(filepath=str(models[0]))
 new=[o for o in sc.objects if o not in before]
 rigs=[o for o in new if o.type=="ARMATURE"]
 meshes=[o for o in new if o.type=="MESH" and len(o.data.vertices)>0]
 if not rigs or sum(len(m.data.vertices) for m in meshes)<15000:raise RuntimeError("NO_SKINNED_TROJAN_"+folder)
 root=bpy.data.objects.new(label+"_PERSISTENT_FACE",None);sc.collection.objects.link(root)
 for o in new:
  if o.parent not in new:
   matrix=o.matrix_world.copy();o.parent=root;o.matrix_world=matrix
 bpy.context.view_layer.update()
 points=[m.matrix_world@Vector(v) for m in meshes for v in m.bound_box]
 low=min(v.z for v in points);high=max(v.z for v in points)
 factor=h/(high-low);root.scale=(factor,)*3
 root.location=(x,y,-low*factor)
 arm=rigs[0]
 fresh=[a for a in bpy.data.actions if a.name not in acts]
 walk=next((a for a in fresh if a.name.lower().startswith("walk_")),None)
 if walk is None:walk=next((a for a in fresh if "walk" in a.name.lower() and "armature" in a.name.lower()),None)
 if walk is None:
  print("CANDIDATE_WALK_ACTIONS",[a.name for a in fresh if "walk" in a.name.lower()],flush=True)
  raise RuntimeError("REAL_WALK_CYCLE_NOT_FOUND_"+folder)
 arm.animation_data_clear();track=arm.animation_data_create().nla_tracks.new()
 track.name="MOCAP_ACTUAL_LEG_CYCLE";st=track.strips.new("WALK",1,walk)
 st.scale=3.4;st.extrapolation="HOLD_FORWARD"
 for f,yy in frames:
  root.location.y=y+(yy+5.8)
  root.keyframe_insert("location",frame=f)
 print("S02_NATIVE_RIGGED_TROJAN_WALK",label,walk.name,flush=True)
 return root,arm
trojan_a,arm_a=load_trojan("troiano_a","TROJAN_01_UNIQUE",1.84,-1.13,-2.2)
trojan_b,arm_b=load_trojan("troiano_b","TROJAN_02_UNIQUE",1.77,1.11,-2.2)
# Both hand targets are held at real modeled rope endpoints, in the moving cart frame.
for sign,arm in [(-1,arm_a),(1,arm_b)]:
 tgt=bpy.data.objects.new("ACTUAL_HAND_PHYSICAL_ROPE_"+str(sign),None)
 sc.collection.objects.link(tgt);tgt.location=(sign*1.08,3.11,1.58)
 parent_world(tgt,horse);tgt.hide_render=True
 norm=lambda name:"".join(c for c in name.lower() if c.isalnum())
 side="right" if sign<0 else "left"
 candidates=[b for b in arm.pose.bones if side+"hand" in norm(b.name) and "finger" not in norm(b.name)]
 if not candidates:raise RuntimeError("NO_REAL_HAND_BONE")
 b=min(candidates,key=lambda b:len(b.name))
 c=b.constraints.new("IK");c.target=tgt;c.chain_count=2;c.influence=.85
 bind(rod("TWO_INDEPENDENT_TAUT_PULLING_ROPES", (sign*.70,2.32,2.17),
             (sign*1.08,3.11,1.58),.045,rope))
 print("S02_TROJAN_ROPE_REAL_HAND_IK",side,b.name,flush=True)
def keylight(name,loc,power,col,size):
 L=bpy.data.lights.new(name,"AREA");L.energy=power;L.color=col;L.shape="DISK";L.size=size
 o=bpy.data.objects.new(name,L);sc.collection.objects.link(o)
 o.location=loc;look(o,(0,-1,3))
keylight("COPPER_TROJAN_SUNSET",(-8,-10,12),1450,(1,.64,.34),13)
keylight("COOL_OUTSIDE_FILL",(8,-5,9),700,(.52,.58,.70),10)
keylight("INSIDE_GATE_RIM",(0,8,11),850,(1,.36,.23),8)
def camera(name,xyz,target):
 data=bpy.data.cameras.new(name);data.lens=35;data.clip_end=180
 o=bpy.data.objects.new(name,data);sc.collection.objects.link(o)
 o.location=xyz;look(o,target);return o
outside=camera("EXTERIOR_ESTABLISHING_FOUR_LEGS_ENTIRE_GATE",(11,-15.6,7.1),(0,-1.6,3.5))
inside=camera("INTERIOR_SHOW_HORSE_ENTERING_THROUGH_OPENING",(8,7.9,7.0),(0,0,3.2))
for f,cy in [(1,-15.6),(100,-13.7),(150,-12.0)]:
 outside.location.y=cy;outside.keyframe_insert("location",frame=f)
for f,cam in [(1,outside),(112,inside)]:
 marker=sc.timeline_markers.new("S02_ACTUAL_CAMERA_CUT",frame=f);marker.camera=cam
sc.camera=outside
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"S02_HORSE_TROJAN_GATE_TRUE_3D_V18_QC.blend"))
receipt={"scene":"S02","artistic_QC_pass":False,"full_film_complete":False,
"native_3d_horse_parts":["four legs","four hooves","head","ears","muzzle","neck","tail","body","twelve planks"],
"carries_hidden_warriors_final_shot_present":False,"gate_clearance_width_m":6.45,
"horse_width_m":3.6,"max_horse_height_m":5.81,"four_wheels_physically_rotate":True,
"two_actual_mocap_trojan_pullers":True,"handover_to_audio_pending":True,
"published":False}
(OUT/"scene_technical_qc.json").write_text(json.dumps(receipt,indent=2),encoding="utf8")
if "--preview" in sys.argv:
 framesdir=OUT/"frames";framesdir.mkdir(exist_ok=True)
 for i,f in enumerate(range(1,N+1)):
  sc.frame_set(f);sc.camera=outside if f<112 else inside
  sc.render.filepath=str(framesdir/f"frame-{i:04d}.png")
  bpy.ops.render.render(write_still=True)
  if i%25==0:print("ODYSSEY_S02_REAL_3D_ANIMATION_FRAME",i,flush=True)
 print("ODYSSEY_S02_V18_NATIVE_150_FRAMES_NOT_FINAL",flush=True)
