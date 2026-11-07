#!/usr/bin/env python3
"""ODISSEIA REBUILD 01 — real 3-D departure, actors move through one persistent set.

Every visible prop is a mesh in a single world, depth-tested by Blender.
No original SVG cast, no 2-D photographs, no per-shot actor overlay.
Free rigs: KayKit Adventurers 1.0 (CC0, creator Kay Lousberg).
Prototype is a geometry/acting QC only — NOT ready for social publishing.
"""
import bpy, math, os, sys, random
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi
random.seed(14)
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/"assets"
OUT=ROOT/"out"
OUT.mkdir(exist_ok=True)
FRAME_START=1
FPS=60
SECONDS=10
def mat(name,color,roughness=.82,metallic=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    node=m.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value=(*color,1)
    node.inputs["Roughness"].default_value=roughness
    node.inputs["Metallic"].default_value=metallic
    return m
SAND=mat("wet ochre Trojan shore",(.48,.38,.28))
SANDHI=mat("sunlit ochre sand",(.63,.49,.32))
SEA=mat("aged Mediterranean sea",(.09,.26,.32),.33)
WOOD=mat("aged hardwood galley",(.34,.18,.105))
WOODLIGHT=mat("galley rib and planking",(.53,.32,.16))
BRONZE=mat("ship bronze fittings",(.51,.36,.15),.33,.62)
LINEN=mat("old wind-filled linen sail",(.69,.62,.44))
STONE=mat("weathered Troy sandstone",(.34,.32,.27))
STONEHI=mat("stone edge",(.46,.43,.36))
FIRE=mat("burning Troy amber",(.96,.25,.038))
ASH=mat("ash dark",(.17,.19,.21))
SKY=mat("smoky air",(.18,.19,.21))
def cube(name,loc,scale,material,bev=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=name
    o.dimensions=scale;bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:o.data.materials.append(material)
    if bev:
        mod=o.modifiers.new("soft stone/wood edge","BEVEL");mod.width=bev;mod.segments=2
        o.modifiers.new("weighted vertex normals","WEIGHTED_NORMAL")
    return o
def sphere(name,loc,scale,material,segments=14,rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc)
    o=bpy.context.object;o.name=name
    o.scale=scale;o.data.materials.append(material);return o
def cylinder(name,loc,radius,depth,material,verts=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
def beam(name,start,end,thickness,material):
    midpoint=(Vector(start)+Vector(end))/2
    vec=Vector(end)-Vector(start)
    o=cylinder(name,midpoint,thickness,vec.length,material,10)
    o.rotation_euler=vec.to_track_quat('Z','Y').to_euler()
    return o
def add_ship():
    root=bpy.data.objects.new("single physical vessel | entire crew boards this hull",None)
    bpy.context.collection.objects.link(root)
    root.location=(1.2,1.3,.03)
    # Longitudinal hull sections: 3D mesh, not a front-facing drawing.
    xz=[(-3.30,.95),(-3.07,.30),(-2.52,.10),(2.4,.10),(3.05,.55),(3.3,1.0)]
    verts=[];faces=[]
    for half in (-1,1):
        for x,z in xz:
            width=(.72+.4*(1-abs(x)/3.5))*half
            verts.append((x,width,z))
    n=len(xz)
    for k in range(n-1):
        faces.append((k,k+1,k+1+n,k+n))
    faces.extend([tuple(range(n-1,-1,-1)),tuple(range(n,n*2))])
    mesh=bpy.data.meshes.new("true 3D hull");mesh.from_pydata(verts,[],faces);mesh.update()
    hull=bpy.data.objects.new("galley timber hull — bow stern depth and keel",mesh)
    bpy.context.collection.objects.link(hull);hull.data.materials.append(WOOD)
    hull.parent=root
    def parent(ob):
        if ob!=root:ob.parent=root;return ob
    deck=parent(cube("deck at human feet", (0,0,.98),(5.8,1.42,.16),WOODLIGHT,.05))
    # Ribs, railings and rowing thwarts in true perspective.
    for i,x in enumerate([-2.45,-1.75,-1.05,-.35,.35,1.05,1.75,2.45]):
        parent(cube("thwart %02d"%i,(x,0,1.08),(.10,1.86,.10),WOODLIGHT,.02))
        for y in [-.84,.84]:
            parent(cylinder("rail baluster", (x,y,1.38),.05,.7,WOOD))
    for y in [-.85,.85]:
        parent(beam("gunwale",(-2.7,y,1.70),(2.7,y,1.70),.07,WOODLIGHT))
    for x in [-2.5,-1.5,-.5,.5,1.5,2.5]:
        for y in [-1,1]:
            parent(beam("real projecting oar",(x,y*.78,1.15),(x+.3,y*2.28,.65),.035,WOODLIGHT))
    mast=parent(cylinder("mast with depth",(0,0,3.32),.13,4.8,WOOD))
    parent(beam("wood yard",(-2.18,0,4.55),(2.15,0,4.55),.085,WOODLIGHT))
    # Wind-shaped sails, TWO surfaces connected to the mast.
    verts=[];faces=[]
    for i in range(6):
        x=-1.7+(3.4/5)*i
        for j in range(5):
            z=2.05+j*.56
            y=.13+sin(pi*i/5)*.42+sin(pi*j/4)*.18
            verts.append((x,y,z))
    for i in range(5):
        for j in range(4):
            a=i*5+j;faces.append((a,a+1,a+6,a+5))
    mesh=bpy.data.meshes.new("curved sail cloth");mesh.from_pydata(verts,[],faces);mesh.update()
    sail=bpy.data.objects.new("rigged bowing linen sail",mesh)
    bpy.context.collection.objects.link(sail);sail.data.materials.append(LINEN);sail.parent=root
    for x in (-1.5,1.5):
        parent(beam("tensioned rigging",(0,0,5.4),(x,0,1.1),.015,BRONZE))
    for i in range(8):
        parent(cube("wooden hull strake", (0,(-1 if i%2 else 1)*(1.02+i*.008),.34+i*.12),(5.35,.055,.04),WOODLIGHT))
    # Drawbridge/ramp stays in world and does NOT sail away with ship.
    plank=cube("gangplank attached to shoreline",(-1.68,-1.57,.61),(.92,3.20,.14),WOODLIGHT,.07)
    plank.rotation_euler[0]=.24
    for i in range(6):
        grip=cube("gangplank cross grip",(-1.68,-2.82+i*.47,.64+i*.06),(.80,.10,.04),WOOD)
        # Keep decking fastened to plank during physical retraction, not scattered across beach.
        bpy.context.view_layer.update()
        old_world=grip.matrix_world.copy()
        grip.parent=plank
        grip.matrix_world=old_world
    # Movement after crew is physically on board.
    root.location=(1.2,1.3,.03);root.keyframe_insert(data_path="location",frame=1)
    root.location=(1.2,1.3,.03);root.keyframe_insert(data_path="location",frame=480)
    root.location=(2.8,5.9,.06);root.keyframe_insert(data_path="location",frame=600)
    root.rotation_euler=(0,0,0);root.keyframe_insert(data_path="rotation_euler",frame=480)
    root.rotation_euler=(.018,-.02,.065);root.keyframe_insert(data_path="rotation_euler",frame=600)
    # Retract intact gangplank into the boat after last sailor's feet touch deck.
    # The six grips are parented, hence cannot remain floating on the beach.
    plank.location=(-1.68,-1.57,.61)
    plank.keyframe_insert(data_path="location",frame=470)
    plank.rotation_euler[0]=.24
    plank.keyframe_insert(data_path="rotation_euler",frame=470)
    plank.location=(-1.68,.85,1.04)
    plank.keyframe_insert(data_path="location",frame=530)
    plank.rotation_euler[0]=0.0
    plank.keyframe_insert(data_path="rotation_euler",frame=530)
    return root
def make_environment():
    # Actual coastline: dry sand ends at y=-0.6, water begins beyond that line.
    # The ship floats on water rather than sitting above the beach geometry.
    cube("one walkable sandy beach",(0,-7.2,-.19),(26,13.2,.32),SANDHI)
    cube("one water surface behind landing",(0,12,-.15),(50,25.2,.08),SEA)
    for i in range(26):
        x=random.uniform(-12,11);y=random.uniform(-10,-2)
        size=random.uniform(.15,.65)
        sphere("rock on beach %02d"%i,(x,y,-.08),(size,size*.8,size*.27),STONE,9,6)
    # City far behind actor-plane; its walls never compete with ship depth.
    cube("Troy fortress rock platform",(-5.2,13,.72),(10,3.5,1.55),STONE,.28)
    for x in [-10.1,-8.2,-6.4,-4.6,-2.8,-1.0]:
        cylinder("Troy defensive tower",(x,12.9,2.8),.74,4.25,STONEHI,10)
        for j in range(8):
            ang=2*pi*j/8
            cube("crenellation",(x+cos(ang)*.61,12.9+sin(ang)*.61,5.08),(.24,.23,.52),STONE)
    wall=cube("ancient Troy city wall",(-5.5,13,2.30),(11.5,.58,3.65),STONE)
    for i in range(34):
        x=-11.0+i*.33
        cube("masonry joint",(x,12.64,1.3+(i%3)*.67),(.035,.06,.24),STONEHI)
    for i in range(13):
        x=-10.3+i*.76
        cube("ruined burning house",(x,14.5+(i%2)*.28,3.0),( .5,.6,random.uniform(1.0,2.4)),ASH)
        for k in range(2):
            sphere("smoldering fire",(x+random.uniform(-.16,.15),14.3,4.0+k*.31),(.2,.2,.45),FIRE,8,5)
    # City is separate from the gangplank sightline rather than touching the sail.
    # Each piece keeps its own 3D world-space depth.
    for city_ob in list(bpy.data.objects):
        if any(tag in city_ob.name.lower() for tag in ("troy ","crenellation","masonry joint","ruined burning house","smoldering fire","smoke above")):
            city_ob.location.x -= 5.2
    # Torches and boatside smoky atmosphere at physically separate z depths.
    # Don't make floating gray balls stand in for volumetric smoke.
    # For this storyboard retain ruined walls and ember-colored fire only.
    for i in range(21):
        x=-10+i*.9
        beam("shore scattered charred wood",(x,-5+sin(i)*2,-.02),(x+.23,-4.9+sin(i)*2,-.01),.05,WOOD)
def find_action(actions,sub):
    subset=[a for a in actions if sub.lower() in a.name.lower()]
    if subset:return subset[0]
    subset=[a for a in actions if 'walk' in a.name.lower()]
    return subset[0] if subset else (actions[0] if actions else None)
def actor(name,file,ship,origin,arrival,enter,finish,scale=.9):
    before=set(bpy.data.objects)
    action_before=set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=str(file))
    new=[o for o in bpy.data.objects if o not in before]
    acts=[a for a in bpy.data.actions if a not in action_before]
    arm=[o for o in new if o.type=="ARMATURE"]
    print("ODYSSEY_IMPORT",name,"OBJECTS",len(new),"ARMATURES",len(arm),"ANIMATIONS",len(acts),flush=True)
    print("ODYSSEY_ACTIONS",name,[a.name for a in acts[:24]],flush=True)
    root=bpy.data.objects.new(name+" — actor-root with ground contact",None)
    bpy.context.collection.objects.link(root)
    for ob in new:
        if ob.parent not in new:
            ob.parent=root
    root.parent=ship
    root.scale=(scale,scale,scale)
    for rig in arm:
        walk=find_action(acts,"Walking_A")
        idle=find_action(acts,"Idle")
        if walk:
            rig.animation_data_clear();anim=rig.animation_data_create()
            track=anim.nla_tracks.new();track.name="actual bone locomotion then stationary on deck"
            strip=track.strips.new("walk only while actor translates",max(1,enter),walk)
            dur=max(1,strip.action_frame_end-strip.action_frame_start)
            strip.repeat=max(1,(finish-enter)/dur)
            strip.frame_end=finish
            strip.blend_type="REPLACE"
            if idle:
                idle_strip=track.strips.new("idle after boarding, no frozen walk",finish+1,idle)
                idle_duration=max(1,idle_strip.action_frame_end-idle_strip.action_frame_start)
                idle_strip.repeat=max(1,(600-finish-1)/idle_duration)
                idle_strip.frame_end=600
                idle_strip.blend_type="REPLACE"
            print("ODYSSEY_RIG_BONES",name, [b.name for b in rig.data.bones[:12]],flush=True)
            print("ODYSSEY_ACTING",name,"WALK",walk.name,"IDLE",idle.name if idle else None,"ENTER",enter,"FINISH",finish,flush=True)
    # All actors use *one* physical gangplank. Approach it in separate start
    # intervals, go up along its centerline and arrive at three distinct deck spots.
    # Convert WORLD path into ship-parent local coordinates (ship stays still until 480).
    ox,oy=origin
    ax,ay=arrival
    def local(world):return (world[0]-1.2, world[1]-1.3,world[2]-.03)
    duration=finish-enter
    keys=[
        (1,             (ox,oy,.07)),
        (enter,         (ox,oy,.07)),
        (int(enter+.20*duration), (-3.7,-4.0,.07)),
        (int(enter+.42*duration), (-1.68,-2.88,.28)),
        (int(enter+.64*duration), (-1.68,-1.00,.70)),
        (int(enter+.81*duration), (-1.68,.28,1.02)),
        (finish,        (ax,ay,1.04)),
        (600,           (ax,ay,1.04))
    ]
    for frame,world in keys:
        root.location=local(world)
        root.keyframe_insert(data_path="location",frame=frame)
    # Face the actual direction of the plank as soon as actor reaches it.
    for fr,heading in [(enter,-.10),(int(enter+.25*duration),0.85),
                       (int(enter+.45*duration),math.pi/2),
                       (int(enter+.80*duration),math.pi/2),
                       (finish,1.25)]:
        root.rotation_euler=(0,0,heading-math.pi/2)
        root.keyframe_insert(data_path="rotation_euler",frame=fr)
    print("ODYSSEY_ACTOR_PATH",name,"START",origin,"PLANK",(-1.68,-2.88),
          "DECK",arrival,flush=True)
    return root
def setup():
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.frame_start=FRAME_START
    scene.frame_end=SECONDS*FPS
    scene.render.fps=FPS
    scene.render.engine="BLENDER_EEVEE"
    if getattr(scene,"eevee",None) and hasattr(scene.eevee,"taa_render_samples"):
        scene.eevee.taa_render_samples=16
    scene.display.shading.light="STUDIO"
    scene.display.shading.color_type="MATERIAL"
    scene.display.shading.show_shadows=False
    scene.display.shading.show_cavity=True
    scene.display.shading.cavity_type="BOTH"
    scene.display.shading.curvature_ridge_factor=1.1
    scene.display.shading.curvature_valley_factor=1.0
    scene.display.shading.background_type="WORLD"
    scene.display.shading.studiolight_rotate_z=.25
    scene.display.shading.background_type="WORLD"
    available={x.name for x in bpy.context.preferences.studio_lights}
    if "paint.sl" in available: scene.display.shading.studio_light="paint.sl"
    scene.render.film_transparent=False
    # Vertical native 60fps animation QC. Full master rendering will be 2160x3840.
    scene.render.resolution_x=1080
    scene.render.resolution_y=1920
    scene.render.resolution_percentage=int(os.environ.get("QC_PERCENT","50"))
    scene.render.image_settings.file_format="PNG"
    scene.render.filepath=str(OUT/"frames"/"troia_departure_")
    scene.render.image_settings.color_mode="RGB"
    scene.render.image_settings.color_depth="8"
    bpy.context.view_layer.update()
    make_environment()
    ship=add_ship()
    prefix=ASSETS/"addons"/"kaykit_character_pack_adventures"/"Characters"/"gltf"
    # KayKit 3D humanoids are CC0. Each is a real armature/animated mesh.
    actor("ODYSSEUS bronze leader",prefix/"Knight.glb",ship,(-7.5,-5.4),(-.95,1.10),1,385,.78)
    actor("ROWER 01 distinct rogue",prefix/"Rogue.glb",ship,(-9.4,-4.75),(.15,1.18),70,432,.76)
    actor("ROWER 02 distinct barbarian",prefix/"Barbarian.glb",ship,(-8.9,-7.0),(1.25,1.12),135,473,.78)
    cam_data=bpy.data.cameras.new("35mm live-action composition")
    cam=bpy.data.objects.new("single real perspective camera",cam_data)
    bpy.context.collection.objects.link(cam)
    def configure_cam(cam_obj,position,look_at,lens):
        cam_obj.location=position
        cam_obj.rotation_euler=(Vector(look_at)-cam_obj.location).to_track_quat("-Z","Y").to_euler()
        cam_obj.data.type="PERSP"
        cam_obj.data.lens=lens
    # Three actual perspective camera setups, edited together as an intelligible
    # action. No 2-D pan and no overlay of a different character onto the set.
    configure_cam(cam,(4.5,-10.5,5.20),(-.45,1.30,2.25),38)
    camera_b_data=bpy.data.cameras.new("shoreline physical boarding POV")
    camera_b=bpy.data.objects.new("CAM-B boarding in one 3D world",camera_b_data)
    bpy.context.collection.objects.link(camera_b)
    configure_cam(camera_b,(2.6,-8.2,4.55),(-1.40,-1.0,1.50),26)
    camera_c_data=bpy.data.cameras.new("departing galley 3D perspective")
    camera_c=bpy.data.objects.new("CAM-C ship sails away",camera_c_data)
    bpy.context.collection.objects.link(camera_c)
    configure_cam(camera_c,(4.85,-11.0,5.45),(1.40,2.30,2.25),38)
    scene.camera=cam
    for fr,obj,mark in [(1,cam,"A - Trojan coast"),(150,camera_b,"B - actual boarding"),(480,camera_c,"C - depart")]:
        scene.timeline_markers.new(mark,frame=fr).camera=obj
    scene.world.color=(.46,.49,.55)
    scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value=(.31,.37,.43,1)
    bg.inputs["Strength"].default_value=.35
    # True PBR lighting instead of the black, unsupported Workbench studio shader.
    def add_light(name,kind,location,color,energy,angle=0):
        light=bpy.data.lights.new(name,kind)
        light.energy=energy
        light.color=color
        if kind=="AREA":light.shape="DISK";light.size=angle
        if kind=="SUN":light.angle=.12
        obj=bpy.data.objects.new(name,light)
        bpy.context.collection.objects.link(obj)
        obj.location=location
        obj.rotation_euler=(Vector((0,0,0))-obj.location).to_track_quat("-Z","Y").to_euler()
    add_light("golden evening sunlight", "SUN", (-5,-7,14), (1.0,.81,.62),1.6)
    add_light("sand bounce diffuse key", "AREA", (-1,-6,10), (1,.86,.69),600,12)
    add_light("ship fill to reveal faces", "AREA", (7,-2,8), (.66,.81,1.0),420,10)
    add_light("city flame amber rim", "AREA", (-10,9,7), (1,.45,.20),260,8)
    scene.view_settings.view_transform="Standard"
    scene.view_settings.look="Medium High Contrast"
    scene.view_settings.exposure=-.65
    scene.render.filepath=str(OUT/"frames"/"troia_departure_")
    print("ODYSSEY_SCENE_READY","meshes",len([x for x in bpy.data.objects if x.type=="MESH"]),"rindex",scene.render.resolution_percentage,flush=True)
    blend=OUT/"odyssey_3d_departure.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    if "--still" in sys.argv:
        for frame in [1,80,180,300,420,540,599]:
            scene.frame_set(frame)
            scene.render.filepath=str(OUT/("frame-%03d.png"%frame))
            bpy.ops.render.render(write_still=True)
    elif "--render" in sys.argv:
        scene.render.filepath=str(OUT/"frames"/"troia_departure_")
        os.makedirs(OUT/"frames",exist_ok=True)
        bpy.ops.render.render(animation=True)
if __name__=="__main__":
    setup()
