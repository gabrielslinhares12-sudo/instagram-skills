#!/usr/bin/env python3
"""Real rigged-actor QC: Polyphemus physically seals the one cave exit.
Technical evidence only, not the approved final film.
Requires CC0 Ara3D Gen exported GLBs; never replace cast with primitives.
"""
import bpy, math, os, sys, json, glob, random
random.seed(20261107)
from mathutils import Vector
from pathlib import Path

OUT=Path("odyssey_185/out/scanrock_v12")
OUT.mkdir(parents=True,exist_ok=True)
FPS=30
def material(name, rgb, metal=0, rough=.7, emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF")
 bs.inputs["Base Color"].default_value=(*rgb,1)
 bs.inputs["Metallic"].default_value=metal;bs.inputs["Roughness"].default_value=rough
 if emission:
  bs.inputs["Emission Color"].default_value=(*rgb,1)
  bs.inputs["Emission Strength"].default_value=emission
 return m
rockmat=material("deep blue-gray layered volcanic basalt",(.105,.113,.117))
stone_dark=material("deep shadow interior cave",(.035,.042,.045))
sandmat=material("Aegean wet sand",(.24,.19,.12))
wood=material("Aged olive wood",(.24,.13,.06))
cloth=material("Ancient pale linen",(.53,.41,.25))
eye=material("Cyclops only eye pearly white",(.92,.87,.72),rough=.3)
iris=material("Cyclops iris burnt amber",(.16,.09,.035),rough=.3)
def cube(name,pos,dim,mat,bevel=.05):
 bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
 o=bpy.context.object;o.name=name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mat)
 if bevel>0:
  md=o.modifiers.new("Stone softly worn edges","BEVEL");md.width=bevel;md.segments=2
  o.modifiers.new("Normals","WEIGHTED_NORMAL")
 return o
def ico(name,pos,scale,mat,subdiv=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdiv,radius=1,location=pos)
 o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mat)
 # Rigged human anatomy stays skinned; only rock geometry gets physical breakup.
 if mat==rockmat or mat==sandmat:
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for v in o.data.vertices:
   v.co *= random.uniform(.86,1.14)
 for p in o.data.polygons:p.use_smooth=True
 return o
def look_at(o,target):
 o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
def import_rig(path,name,target_height,position):
 before=set(bpy.context.scene.objects)
 earlier_actions=set(bpy.data.actions.keys())
 bpy.ops.import_scene.gltf(filepath=str(path))
 created=[o for o in bpy.context.scene.objects if o not in before]
 armatures=[o for o in created if o.type=="ARMATURE"]
 meshes=[o for o in created if o.type=="MESH" and len(o.data.vertices)>0]
 if not armatures or sum(len(x.data.vertices) for x in meshes)<4500:
  raise RuntimeError("REAL_SKINNED_CHARACTER_ASSET_MISSING: fail closed")
 # Parent all imported top-level roots under a single world-transform.
 root=bpy.data.objects.new(name+"Root",None)
 bpy.context.scene.collection.objects.link(root)
 for obj in created:
  if obj.parent not in created:
   mw=obj.matrix_world.copy();obj.parent=root;obj.matrix_world=mw
 bpy.context.view_layer.update()
 coords=[obj.matrix_world @ Vector(corner) for obj in meshes for corner in obj.bound_box]
 zmin=min(v.z for v in coords);zmax=max(v.z for v in coords)
 height=zmax-zmin
 if not .5 < height < 4.5:raise RuntimeError("CHARACTER_UNEXPECTED_NATIVE_HEIGHT")
 factor=target_height/height
 root.scale=(factor,)*3
 root.location=(position[0],position[1],position[2]-zmin*factor)
 root.rotation_euler=(0,0,position[3])
 bpy.context.view_layer.update()
 count=sum(len(obj.data.vertices) for obj in meshes)
 new_actions=[action for action in bpy.data.actions if action.name not in earlier_actions]
 action_label = "Push" if name=="POLYPHEMUS" else "Hit reaction"
 acting = next((act for act in new_actions if act.name.startswith(action_label+"_Armature")),None)
 if acting is None:
  print("AVAILABLE_NEW_ACTING_ACTIONS",[a.name for a in new_actions if "Push" in a.name or "Hit" in a.name],flush=True)
  raise RuntimeError("SOURCE_GLB_LACKS_ANIMATION_"+action_label)
 rig=armatures[0]
 rig.animation_data_clear()
 track=rig.animation_data_create().nla_tracks.new()
 track.name=name+"_BODY_ACTING_NOT_STATIC"
 start=48 if name=="POLYPHEMUS" else 208
 strip=track.strips.new(name+"_ACTION_"+action_label,start,acting)
 strip.scale=3.45 if name=="POLYPHEMUS" else 2.0
 strip.extrapolation="HOLD_FORWARD"
 print("NATIVE_CHARACTER_ACTING",name,acting.name,"worldstart",start,"end",strip.frame_end,flush=True)
 clips=sorted(set(action.name for action in bpy.data.actions))
 print("SKINNED_ACTOR_IMPORTED",name,"height",round(target_height,2),"vertices",count,"actions",len(clips),flush=True)
 return root,armatures[0],count,clips

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE"
scene.render.resolution_x=720
scene.render.resolution_y=1280
scene.render.resolution_percentage=100
scene.render.fps=FPS
scene.frame_start=1;scene.frame_end=360
scene.render.image_settings.file_format="PNG"
scene.render.film_transparent=False
scene.world.color=(.035,.048,.065)
try: scene.eevee.taa_render_samples=28
except Exception: pass

# 5.6m natural entrance in an irregular basalt cliff, no cube-room walls.
ico("irregular beach landform",(0,1,-4.1),(27,24,4.3),sandmat,4)
for side in (-1,1):
 for i in range(16):
  x=side*(4.85+((i*7)%5)*.64)
  y=5.4+(i//5)*2.5
  z=1.8+((i*11)%7)*.83
  sx=1.55+(i%4)*.28;sy=2.35+(i%3)*.43;sz=1.9+(i%5)*.35
  ico("natural fractured wall "+str(side)+" "+str(i),(x,y,z),(sx,sy,sz),rockmat,3)
for i in range(11):
 x=-3.8+i*.76
 z=8.0+.58*math.sqrt(max(0,1-(x/5.5)**2))
 ico("basalt cave mouth arch "+str(i),(x,5.7,z),(1.3,2.2,1.55),rockmat,3)
ico("dark cavern recess shadow beyond passage",(0,19.0,3.5),(3.6,3.6,4.4),stone_dark,3)
for i in range(47):
 x=((i*47)%260)/10-13.0
 y=((i*29)%180)/10-3.5
 if abs(x)<2.9 and y<5:continue
 sc=.3+((i*7)%11)*.1
 ico("coast fractured basalt scree %02d"%i,(x,y,sc*.31),(sc,sc*.92,sc*.61),rockmat,2)
# The stone is demonstrably bigger than mouth: width 6.5m, height 7.0m.
rock=ico("Monolithic boulder larger than cave opening",(6.35,1.4,3.55),(3.18,2.25,3.65),rockmat,3)
tex=bpy.data.textures.new("Pitted stone relief","CLOUDS")
tex.noise_scale=.55
modifier=rock.modifiers.new("Basalt natural fractures","DISPLACE")
modifier.texture=tex;modifier.strength=.72
# The boulder translates from open to sealed entrance. Does not teleport.
for frame,x in [(1,6.35),(60,6.35),(145,4.45),(230,2.3),(315,0),(360,0)]:
 rock.location.x=x;rock.keyframe_insert("location",frame=frame)
 rock.rotation_euler=(0,(5.25-x)*.027,(5.25-x)*.013)
 rock.keyframe_insert("rotation_euler",frame=frame)

p_model=next(iter(Path("ara3d/out/polyphemus").glob("*.glb")),None)
o_model=next(iter(Path("ara3d/out/odysseus").glob("*.glb")),None)
if p_model is None or o_model is None:
 raise RuntimeError("PERIOD_GLB_ASSET_MISSING_BOTH_CHARACTERS")
print("PERIOD_ACCURATE_ASSETS",p_model,o_model,flush=True)
polyphemus,cyclops_arm,cyclops_verts,clips=import_rig(p_model,"POLYPHEMUS",(5.5),(11.1,1.0,0,-1.5707963))
crew1,crew_arm1,crew_verts,crew_clips=import_rig(o_model,"ODYSSEUS",(1.84),(-1.55,8.0,0,0))
crew2,crew_arm2,_,_=import_rig(o_model,"SAILOR",(1.77),(1.4,8.6,0,.3))
# Cyclops follows boulder while firmly grounded, planted feet in every still.
for frame,x in [(1,11.1),(60,11.1),(145,9.2),(230,7.0),(315,4.8),(360,4.8)]:
 polyphemus.location.x=x;polyphemus.keyframe_insert("location",frame=frame)
# Sailors recoil deeper into cave, explicitly trapped as light shuts off.
for frame,y in [(1,8.0),(90,8.0),(150,8.6),(260,10.1),(360,10.35)]:
 crew1.location.y=y;crew1.keyframe_insert("location",frame=frame)
 crew2.location.y=y+.7;crew2.keyframe_insert("location",frame=frame)
# Lightweight patches aren't allowed as primary anatomy: the CC0 skinned
# mesh must be the visible character; this is an identifiable cyclops eye.
# Attach central oversized eye geometry to head bone so it moves with acting.
bone=next((b for b in cyclops_arm.pose.bones if "head" in b.name.lower()),None)
if bone is None:raise RuntimeError("HUMANOID_RIG_HEAD_BONE_NOT_FOUND")
# Attach one large, recognizable cyclopean eye to an actual skinned head
# bone, using WORLD-SPACE placement to avoid arbitrary bone-local placement.
scene.frame_set(1)
bpy.context.view_layer.update()
headworld=cyclops_arm.matrix_world @ bone.head
forward=(polyphemus.matrix_world.to_quaternion() @ Vector((0,-1,0))).normalized()
def facepart(name,at,scale,ma):
 ob=ico(name,at,scale,ma,3)
 bpy.context.view_layer.update()
 world=ob.matrix_world.copy()
 ob.parent=cyclops_arm;ob.parent_type="BONE";ob.parent_bone=bone.name
 ob.matrix_world=world
 return ob
mask_position=headworld+Vector((0,0,.24))+forward*.20
facepart("Cyclops brow covers both natural human eye sockets",mask_position,
 (.18,.55,.23),cloth)
facepart("ONE_ONLY_CYCLOPEAN_WHITE_EYE",mask_position+forward*.13,
 (.12,.38,.28),eye)
facepart("ONE_ONLY_AMBER_IRIS",mask_position+forward*.23,
 (.076,.17,.18),iris)
facepart("ONE_ONLY_BLACK_PUPIL",mask_position+forward*.31,
 (.055,.080,.095),material("dark central one pupil",(.017,.011,.008)))
# Set: light escapes through opening until sealed; boulder blocks the beam.
def lamp(name,kind,xyz,energy,color,size=3):
 L=bpy.data.lights.new(name,kind);L.energy=energy;L.color=color
 o=bpy.data.objects.new(name,L);scene.collection.objects.link(o)
 o.location=xyz;look_at(o,(0,2,3))
 if kind=="AREA":L.shape="DISK";L.size=size
 return o
lamp("Dusk key daylight","AREA",(1,-7,9),2200,(.83,.78,.60),7)
lamp("Cold cave bounce","AREA",(0,8,7),650,(.18,.35,.60),4)
lamp("Rim cyclops","AREA",(10,2,8),1100,(.80,.38,.21),5)
lamp("warm evening bounce","AREA",(-6,-5,12),1500,(1,.69,.37),9)
lamp("soft overcast bounce","AREA",(6,-12,9),1300,(.55,.62,.83),12)
# Physically shaded texture detail, not uniformly grey plastic surfaces.
for rocky in [rockmat,sandmat]:
 ns=rocky.node_tree.nodes
 bs=ns.get("Principled BSDF")
 texnode=ns.new("ShaderNodeTexNoise")
 texnode.inputs["Scale"].default_value=8 if rocky==rockmat else 18
 texnode.inputs["Detail"].default_value=4
 bump=ns.new("ShaderNodeBump")
 bump.inputs["Strength"].default_value=.3
 bump.inputs["Distance"].default_value=.09
 rocky.node_tree.links.new(texnode.outputs["Fac"],bump.inputs["Height"])
 rocky.node_tree.links.new(bump.outputs["Normal"],bs.inputs["Normal"])
cam=bpy.data.cameras.new("18mm wide geographic situation")
ob=bpy.data.objects.new("Wide shows giant, cave mouth, and stone simultaneously",cam)
scene.collection.objects.link(ob);scene.camera=ob
ob.location=(12.8,-20.8,8.2);look_at(ob,(3.0,3.8,3.7));cam.lens=18;cam.clip_end=180
close_cam=bpy.data.cameras.new("25mm actual body effort and face")
close_ob=bpy.data.objects.new("Close real character action",close_cam)
scene.collection.objects.link(close_ob)
close_ob.location=(10,-12.5,7.1);look_at(close_ob,(6.3,1.7,3.9));close_cam.lens=26;close_cam.clip_end=180
inside_cam=bpy.data.cameras.new("27mm trapped crew consequence")
inside_ob=bpy.data.objects.new("Inside cavern no exit",inside_cam)
scene.collection.objects.link(inside_ob)
inside_ob.location=(1.2,13.1,4.9);look_at(inside_ob,(0,5.0,2.8))
inside_cam.lens=26;inside_cam.clip_end=180
for fr,which,marker in [(1,ob,"OPEN_CAVE_GIANT_VISIBLE"),
 (125,close_ob,"GIGANTIC_HANDS_PUSH_MONOLITH"),
 (286,inside_ob,"TRAPPED_CREW_AFTER_CLOSURE")]:
 p=scene.timeline_markers.new(marker,frame=fr);p.camera=which
# V12 geological replacement: actual CC0 scan rock meshes and PBR maps.
# No recycled procedural spheres for the cave/boulder.
from mathutils import Matrix
ASSET_ROOT=Path("odyssey_185/out/cc0_rocks")
def import_scan(asset_id,label,at,dimensions,rz=0.0):
    source=ASSET_ROOT/asset_id
    paths=list(source.glob("*.gltf"))
    if len(paths)!=1:
        raise RuntimeError("POLYHAVEN_SCAN_MISSING_OR_DUPLICATE_"+asset_id)
    existing=set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(paths[0]))
    new=[obj for obj in bpy.context.scene.objects if obj not in existing]
    meshes=[obj for obj in new if obj.type=="MESH" and len(obj.data.vertices)>100]
    if not meshes or sum(len(obj.data.vertices) for obj in meshes)<1000:
        raise RuntimeError("INVALID_POLYHAVEN_3D_SCAN_"+asset_id)
    bpy.context.view_layer.update()
    verts=[ob.matrix_world @ Vector(pt) for ob in meshes for pt in ob.bound_box]
    low=Vector((min(p[i] for p in verts) for i in range(3)))
    high=Vector((max(p[i] for p in verts) for i in range(3)))
    span=high-low
    if any(v<.01 for v in span):raise RuntimeError("CC0_SCAN_INVALID_BBOX")
    center=(low+high)*.5
    master=bpy.data.objects.new(label+"_WORLD_ROOT",None)
    bpy.context.scene.collection.objects.link(master)
    # Preserve scanned hierarchy and material links while recentering geometry.
    for ob in new:
        if ob.parent not in new:
            world=ob.matrix_world.copy()
            ob.parent=master
            ob.matrix_world=Matrix.Translation(-center) @ world
    master.scale=tuple(dimensions[i]/span[i] for i in range(3))
    master.location=at
    master.rotation_euler[2]=rz
    bpy.context.view_layer.update()
    print("V12_POLYHAVEN_SCAN_IMPORTED",asset_id,label,
          "vertices",sum(len(x.data.vertices) for x in meshes),
          "materials",sum(len(x.data.materials) for x in meshes),
          "bbox",tuple(round(x,2) for x in span),flush=True)
    return master

oldnames=(
  "natural fractured wall ", "basalt cave mouth arch ",
  "dark cavern recess shadow beyond passage",
  "coast fractured basalt scree ",
  "Monolithic boulder larger than cave opening"
)
removed=[obj for obj in list(bpy.context.scene.objects)
         if any(obj.name.startswith(prefix) for prefix in oldnames)]
for obj in removed:bpy.data.objects.remove(obj,do_unlink=True)
# True scanned stratified cliffs; real nonuniform rock silhouettes, 3 unique
# geographic placements. The cave mouth at x=-2.8..2.8 remains legible.
left=import_scan("coastal_cliff_01","LEFT_CLIFF_CC0",
       (-7.5,5.2,3.9),(8.6,6.0,8.1),.23)
right=import_scan("coastal_cliff_01","RIGHT_CLIFF_CC0",
       (7.6,5.3,3.8),(8.2,6.2,8.2),-1.20)
lintel=import_scan("coastal_cliff_01","TOP_CAVE_CC0",
       (0.0,5.6,9.0),(7.5,5.9,2.3),1.68)
# Replace mathematically spheroidal boulder with 3D photogrammetry model.
stone=import_scan("namaqualand_boulder_02","MONOLITH_CC0_LARGER_THAN_OPENING",
       (6.35,1.4,3.62),(6.5,4.5,7.35),-.05)
for frame,x,tilt in [(1,6.35,0),(60,6.35,0),(145,4.45,-.035),
                    (230,2.3,-.075),(315,0,-.10),(360,0,-.10)]:
    stone.location.x=x
    stone.keyframe_insert("location",frame=frame)
    stone.rotation_euler[1]=tilt
    stone.keyframe_insert("rotation_euler",frame=frame)
# No cube substitute and no fallback: fail before rendering if external scans
# are inaccessible, keeping the result editorially honest.
stage_scan={
    "asset_source":"Poly Haven official API, CC0 rock photogrammetry",
    "citation":"Powered by Poly Haven",
    "rock_assets":["coastal_cliff_01","namaqualand_boulder_02"],
    "procedural_cave_sphere_reused":False,
    "actors":"Ara3D skinned characters, 1 cyclops and 2 sailors",
    "user_rasalgethi_wav_unchanged":True,
    "visual_editorial_pass":False,"publish":False
}
(OUT/"scanrock_sources.json").write_text(json.dumps(stage_scan,indent=2),encoding="utf-8")
print("V12_CC0_PHOTOGRAMMETRY_ASSETS_STAGED",flush=True)

try:
 scene.view_settings.view_transform="AgX"
except Exception:
 scene.view_settings.view_transform="Standard"
assert cyclops_verts>4500 and crew_verts>4500
stage={
"scene":"S04","physical":"cave boulder push with imported skinned Ara3D actors",
"stone_width_m":6.36,"cave_opening_m":5.6,
"stone_height_m":7.3,"opening_height_m":6.4,
"actors":[{"name":"Polyphemus","height_m":5.5,"skinned_vertices":cyclops_verts},
          {"name":"Odysseus","height_m":1.84,"skinned_vertices":crew_verts}],
"clip_names":[n for n in clips if n.startswith("Push")][:8],"release_status":"STILLS_ONLY_QC_NOT_FINAL",
"narration_not_attached":True,"published":False}
(OUT/"scene_technical_qc.json").write_text(json.dumps(stage,indent=2),encoding="utf-8")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"S04_POLYPHEMUS_SCANROCK_V12_TEST.blend"))
# Three stages, compare first/middle/end for legible causal blocking.
for f in [1,90,180,270,360]:
 scene.frame_set(f)
 scene.render.filepath=str(OUT/f"S04_v12_scanrock_{f:03d}.png")
 bpy.ops.render.render(write_still=True)
 print("ODYSSEY_RIGGED_S04_STILL",f,flush=True)
print("ODYSSEY_V12_SCANROCK_RIGGED_CYCLOPS_QC_NOT_FINAL",flush=True)
