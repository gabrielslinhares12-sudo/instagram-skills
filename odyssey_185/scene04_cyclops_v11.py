#!/usr/bin/env python3
"""Real rigged-actor QC: Polyphemus physically seals the one cave exit.
Technical evidence only, not the approved final film.
Requires CC0 Ara3D Gen exported GLBs; never replace cast with primitives.
"""
import bpy, math, os, sys, json, glob
from mathutils import Vector
from pathlib import Path

OUT=Path("odyssey_185/out/cyclops_v11")
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
rockmat=material("Stone basalt rough PBR",(.15,.17,.20))
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
 return o
def look_at(o,target):
 o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
def import_rig(path,name,target_height,position):
 before=set(bpy.context.scene.objects)
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

# Exact cave dimensions: a 5.6m opening, 6.4m high; boulder covers it.
cube("solid coastline rock platform",(0,1,-.50),(40,23,1),sandmat)
cube("cave left continuous rock wall",(-6.5,5,4),(7.5,7,8),rockmat,.28)
cube("cave right continuous rock wall",(6.5,5,4),(7.5,7,8),rockmat,.28)
cube("cave top solid lintel",(0,5,7.3),(5.9,7,2.0),rockmat,.35)
cube("dark far cave wall",(0,9.0,3.7),(5.4,1.5,7.4),rockmat,.14)
for i in range(25):
 x=((i*19)%23)-11.4;y=(((i*7)%20)-4.0)
 if abs(x)<3.5 and y<3: continue
 sc=.75+(i%5)*.35
 ico("irregular geologic scree %02d"%i,(x,y,sc*.31),(sc,sc*.9,sc*.7),rockmat,2)
# The stone is demonstrably bigger than mouth: width 6.5m, height 7.0m.
rock=ico("Monolithic boulder larger than cave opening",(6.35,1.4,3.55),(3.18,2.25,3.65),rockmat,3)
tex=bpy.data.textures.new("Pitted stone relief","CLOUDS")
tex.noise_scale=.55
modifier=rock.modifiers.new("Basalt natural fractures","DISPLACE")
modifier.texture=tex;modifier.strength=.22
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
# Blind two eyes with worn leather mask and leave one huge centered eye.
mask=ico("cyclops eye-cover mask",(0,0,0),(.28,.1,.18),cloth,2)
mask.parent=cyclops_arm;mask.parent_type="BONE";mask.parent_bone=bone.name
mask.location=(0,-.12,.045)
large=ico("the one central Cyclops eye",(0,0,0),(.11,.055,.105),eye,3)
large.parent=cyclops_arm;large.parent_type="BONE";large.parent_bone=bone.name
large.location=(0,-.25,.05)
pupil=ico("one iris",(0,0,0),(.05,.028,.065),iris,3)
pupil.parent=cyclops_arm;pupil.parent_type="BONE";pupil.parent_bone=bone.name
pupil.location=(0,-.302,.05)
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
cam=bpy.data.cameras.new("35mm dramatic scale camera")
ob=bpy.data.objects.new("Stage continuity camera",cam);scene.collection.objects.link(ob)
scene.camera=ob
ob.location=(16.7,-29.0,11.4);look_at(ob,(2.4,2.8,3.5));cam.lens=19;cam.clip_end=140
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
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"S04_POLYPHEMUS_RIGGED_TEST.blend"))
# Three stages, compare first/middle/end for legible causal blocking.
for f in [1,90,180,270,360]:
 scene.frame_set(f)
 scene.render.filepath=str(OUT/f"S04_polyphemus_{f:03d}.png")
 bpy.ops.render.render(write_still=True)
 print("ODYSSEY_RIGGED_S04_STILL",f,flush=True)
print("ODYSSEY_REAL_RIGGED_CAST_QC_READY_NOT_FINAL",flush=True)
