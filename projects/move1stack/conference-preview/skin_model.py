"""Render the supplied legacy 64x32 skin as a static classic player model.

Run in Blender background mode; no Minecraft or browser execution is needed.
Cuboid dimensions and legacy mirrored limbs are a reconstruction, not a game
capture. The source image is not redistributed in the repository.
"""
import hashlib
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / '.inputs/skin.png'
OUT = ROOT / 'previews/conference-slice-10'
EXPECTED = 'dc6d27c115e71009ced5a2bc41a24e918b45edf5a584e639ec56b832126d2635'
with SKIN.open('rb') as f:
    if hashlib.file_digest(f, 'sha256').hexdigest() != EXPECTED:
        raise RuntimeError('Skin hash does not match the supplied legacy skin')
if OUT.exists() and any(OUT.iterdir()):
    raise RuntimeError('Output exists; preserve it and choose a new directory')
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 8
scene.cycles.use_denoising = False
scene.render.film_transparent = True
scene.render.resolution_x = 500
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.world.color = (0, 0, 0)

mat = bpy.data.materials.new('Legacy skin')
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()
tex = nodes.new('ShaderNodeTexImage')
tex.image = bpy.data.images.load(str(SKIN), check_existing=True)
if tuple(tex.image.size) != (64, 32):
    raise RuntimeError('Expected a 64x32 legacy skin')
tex.interpolation = 'Closest'
output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
mat.node_tree.links.new(tex.outputs['Color'], emission.inputs['Color'])
mat.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])


def cuboid(name, center, size, origin, mirror=False):
    x, y, z = center
    w, h, d = size
    a, b = origin
    left, right = x-w/2, x+w/2
    front, back = y-d/2, y+d/2
    bottom, top = z-h/2, z+h/2
    faces = [
        [(left,front,top),(right,front,top),(right,front,bottom),(left,front,bottom)],
        [(right,back,top),(left,back,top),(left,back,bottom),(right,back,bottom)],
        [(left,back,top),(left,front,top),(left,front,bottom),(left,back,bottom)],
        [(right,front,top),(right,back,top),(right,back,bottom),(right,front,bottom)],
        [(left,back,top),(right,back,top),(right,front,top),(left,front,top)],
        [(left,front,bottom),(right,front,bottom),(right,back,bottom),(left,back,bottom)],
    ]
    rects = [
        (a+d,b+d,a+d+w,b+d+h),
        (a+2*d+w,b+d,a+2*d+2*w,b+d+h),
        (a,b+d,a+d,b+d+h),
        (a+d+w,b+d,a+2*d+w,b+d+h),
        (a+d,b,a+d+w,b+d),
        (a+d+w,b,a+d+2*w,b+d),
    ]
    if mirror:
        rects[2], rects[3] = rects[3], rects[2]
    vertices = [v for face in faces for v in face]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], [tuple(range(i*4, i*4+4)) for i in range(6)])
    mesh.update()
    layer = mesh.uv_layers.new(name='SkinUV')
    for poly, (u0,v0,u1,v1) in zip(mesh.polygons, rects):
        if mirror:
            u0, u1 = u1, u0
        coords = [(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
        for idx, (u, v) in zip(poly.loop_indices, coords):
            layer.data[idx].uv = (u/64, 1-v/32)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)


# coordinates: front faces negative Y; +Z is up; pixels are model units.
cuboid('head',(0,0,28),(8,8,8),(0,0))
cuboid('torso',(0,0,18),(8,12,4),(16,16))
cuboid('right arm',(-6,0,18),(4,12,4),(40,16))
cuboid('left arm',(6,0,18),(4,12,4),(40,16),mirror=True)
cuboid('right leg',(-2,0,6),(4,12,4),(0,16))
cuboid('left leg',(2,0,6),(4,12,4),(0,16),mirror=True)
# The supplied legacy head-overlay region is fully transparent.
if any(tex.image.pixels[(y*64+x)*4+3] > 0 for y in range(16,32) for x in range(32,64)):
    raise RuntimeError('Unexpected head overlay; model requires overlay support')

camera_data = bpy.data.cameras.new('Camera')
camera = bpy.data.objects.new('Camera', camera_data)
bpy.context.collection.objects.link(camera)
scene.camera = camera
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 35
camera.location = (0,-100,16)
camera.rotation_euler = (Vector((0,0,16)) - camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath = str(OUT / 'front.png')
bpy.ops.render.render(write_still=True)
camera.location = (-24,-100,25)
camera.rotation_euler = (Vector((0,0,16)) - camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath = str(OUT / 'player.png')
bpy.ops.render.render(write_still=True)
print('Wrote', scene.render.filepath)
