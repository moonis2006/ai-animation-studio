import bpy
import math
import os
from mathutils import Vector

# AI Animation Studio — first cloud render.
# 4 seconds, 12 fps, 480x854 (portrait), CPU-friendly Eevee.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

scn=bpy.context.scene
scn.render.engine='BLENDER_EEVEE'
scn.render.resolution_x=480
scn.render.resolution_y=854
scn.render.resolution_percentage=100
scn.render.fps=12
scn.frame_start=1
scn.frame_end=48
scn.render.image_settings.file_format='PNG'
scn.render.filepath=os.path.abspath('//output/frames/frame_')
scn.render.film_transparent=False
scn.world.color=(0.04,0.05,0.10)
scn.view_settings.view_transform='AgX'

def material(name, color, metallic=0, roughness=0.4, emission=None):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=(*color,1)
    bsdf.inputs['Metallic'].default_value=metallic
    bsdf.inputs['Roughness'].default_value=roughness
    if emission:
        bsdf.inputs['Emission Color'].default_value=(*color,1)
        bsdf.inputs['Emission Strength'].default_value=emission
    return m

blue=material('Pip turquoise enamel',(0.025,0.47,0.76),0.30,0.25)
cream=material('Face visor',(0.8,0.95,1),0.0,0.25)
eye=material('Warm cyan glowing eyes',(0.02,0.9,1),0.0,0.22,2.0)
mouth=material('Mouth',(0.015,0.04,0.07),0.0,0.5)
gold=material('Gold details',(0.95,0.5,0.12),0.65,0.24)
floor_mat=material('Dark blue floor',(0.065,0.095,0.16),0.05,0.75)
jar_mat=material('Jar terracotta',(0.48,0.19,0.09),0.05,0.65)
light_mat=material('Jar glow',(0.7,0.94,0.25),0.0,0.35,2.3)

def uv(name, location, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=location)
    o=bpy.context.object
    o.name=name
    o.scale=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if parent: o.parent=parent
    return o

def cube(name,loc,scale,mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object;o.name=name;o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    bevel=o.modifiers.new('softened corners','BEVEL')
    bevel.width=0.12;bevel.segments=2
    o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    return o

root=bpy.data.objects.new('PIP | animation root',None)
bpy.context.collection.objects.link(root)
root.location=(0,0,0)

uv('Pip head',(0,0,2.20),(0.58,0.48,0.55),blue,root)
uv('Face panel',(0,-0.46,2.22),(0.43,0.10,0.31),cream,root)
for x in (-0.19,0.19):
    uv('Eye',(x,-0.55,2.27),(0.105,0.035,0.12),eye,root)
uv('tiny smile',(0,-0.553,2.04),(0.11,0.02,0.023),mouth,root)
uv('Body',(0,0,1.27),(0.42,0.38,0.57),blue,root)
uv('Chest light',(0,-0.38,1.39),(0.14,0.045,0.14),gold,root)
for x in (-0.30,0.30):
    uv('Foot',(x,-0.1,0.32),(0.25,0.35,0.16),blue,root)
uv('Left arm',(-0.55,0,1.43),(0.18,0.21,0.43),blue,root)

# The waving arm pivots around the shoulder.
shoulder=bpy.data.objects.new('RIGHT ARM | shoulder joint',None)
bpy.context.collection.objects.link(shoulder)
shoulder.parent=root
shoulder.location=(0.47,0,1.66)
uv('Right arm mesh',(0.13,0,-0.32),(0.18,0.22,0.37),blue,shoulder)
uv('Right hand',(0.15,-0.02,-0.61),(0.19,0.20,0.20),blue,shoulder)

# Jar prop
uv('Old jar belly',(1.2,-0.20,0.52),(0.39,0.33,0.53),jar_mat)
uv('Old jar neck',(1.2,-0.20,0.95),(0.24,0.24,0.15),jar_mat)
uv('Jar magical glow',(1.2,-0.46,0.74),(0.19,0.035,0.19),light_mat)

cube('Stone platform',(0,0,-0.18),(7,7,0.35),floor_mat)

# Studio lighting
def area(name,loc,power,color,size):
    data=bpy.data.lights.new(name,'AREA')
    data.energy=power;data.color=color;data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(obj)
    obj.location=loc
    direction=Vector((0,0,1.4))-obj.location
    obj.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
area('Soft key',(-3,-4,7),700,(0.72,0.88,1),5)
area('Amber rim',(3,1,5),900,(1,0.58,0.25),4)

camera_data=bpy.data.cameras.new('Movie camera')
camera=bpy.data.objects.new('Movie camera',camera_data)
bpy.context.collection.objects.link(camera)
scn.camera=camera
camera_data.type='ORTHO'
camera_data.ortho_scale=4.3

# Keyframes: character floats and waves; camera gently pushes in.
for frame in (1,12,24,36,48):
    t=(frame-1)/12
    scn.frame_set(frame)
    root.location.z=0.045*math.sin(t*3)
    root.rotation_euler.z=0.07*math.sin(t*1.3)
    root.keyframe_insert(data_path='location',frame=frame)
    root.keyframe_insert(data_path='rotation_euler',frame=frame)
    shoulder.rotation_euler.y= -0.90-0.40*math.sin(t*5)
    shoulder.rotation_euler.z=0.18*math.sin(t*5)
    shoulder.keyframe_insert(data_path='rotation_euler',frame=frame)
    camera.location=(3.9-0.6*t/4,-7.8+0.7*t/4,3.2)
    point=Vector((0.30,0,1.43))
    camera.rotation_euler=(point-Vector(camera.location)).to_track_quat('-Z','Y').to_euler()
    camera.keyframe_insert(data_path='location',frame=frame)
    camera.keyframe_insert(data_path='rotation_euler',frame=frame)

scn.frame_set(1)
os.makedirs(os.path.dirname(scn.render.filepath),exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('//output/pip_first_film.blend'))
bpy.ops.render.render(animation=True)
