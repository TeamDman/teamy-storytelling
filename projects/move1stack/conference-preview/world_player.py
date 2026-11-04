"""Rebuild the saved baked world in Blender and stage a skin-player gesture.

No Minecraft or browser is run. The pose, timing, camera, Blender material
handling and beacon are reconstructions; this is not captured gameplay.
"""
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/conference-slice-12'
BAKED = ROOT / 'baked-scene.json'
SKIN = ROOT / '.inputs/skin.png'
EXPECTED = {
    BAKED: 'da2058cd350a89b11dd4fdd0ae0808caa4616fec4c2f1f7b7a2561b0d85f6d15',
    SKIN: 'dc6d27c115e71009ced5a2bc41a24e918b45edf5a584e639ec56b832126d2635',
    ROOT / 'grass-field.png': 'c0f9667ed408ced9440ba040bbf5f03175a4e5c908a7e56419c203a2f80fc555',
}
for path, expected in EXPECTED.items():
    with path.open('rb') as f:
        if hashlib.file_digest(f, 'sha256').hexdigest() != expected:
            raise RuntimeError(f'Input hash mismatch: {path}')
OUT.mkdir(parents=True, exist_ok=True)
mode = 'verify' if '--verify' in sys.argv else 'render' if '--render' in sys.argv else 'still'
still_frame = int(sys.argv[sys.argv.index('--frame')+1]) if '--frame' in sys.argv else 73
still_path = OUT / f'world-still-{still_frame:03d}.png'
if mode == 'render' and (OUT / 'frames').exists():
    raise RuntimeError('Frames already exist; preserve them')
if mode == 'still' and still_path.exists():
    raise RuntimeError('Still already exists; preserve it')

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 4
scene.cycles.use_denoising = False
scene.render.resolution_x = 768
scene.render.resolution_y = 432
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.world.use_nodes = True
scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value = (.46,.63,1,1)
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value = 1

baked = json.loads(BAKED.read_text())
if baked['schemaVersion'] != 1 or len(baked['meshes']) != 195:
    raise RuntimeError('Unexpected baked scene')
textures = {t['id']: t for t in baked['textures']}
materials = {}
for spec in baked['materials']:
    t = textures[spec['texture']]
    path = ROOT / ('grass-field.png' if t['url'].endswith('grass-field.png') else 'ground-truth/' + t['id'])
    mat = bpy.data.materials.new(spec['id'])
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(str(path), check_existing=True)
    tex.interpolation = 'Closest'
    vc = nodes.new('ShaderNodeVertexColor')
    vc.layer_name = 'light'
    mix = nodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 1
    emit = nodes.new('ShaderNodeEmission')
    output = nodes.new('ShaderNodeOutputMaterial')
    links = mat.node_tree.links
    links.new(tex.outputs['Color'], mix.inputs[1])
    links.new(vc.outputs['Color'], mix.inputs[2])
    links.new(mix.outputs['Color'], emit.inputs['Color'])
    if spec['transparent'] or spec['alphaTest']:
        trans = nodes.new('ShaderNodeBsdfTransparent')
        combine = nodes.new('ShaderNodeMixShader')
        links.new(tex.outputs['Alpha'], combine.inputs[0])
        links.new(trans.outputs[0], combine.inputs[1])
        links.new(emit.outputs[0], combine.inputs[2])
        links.new(combine.outputs[0], output.inputs['Surface'])
    else:
        links.new(emit.outputs[0], output.inputs['Surface'])
    materials[spec['id']] = (mat, tex.image.size[:], bool(t.get('animation')))

# The baked renderer uses Minecraft's +Y up; Blender uses +Z up.
for n, spec in enumerate(baked['meshes']):
    p, uv, col = spec['positions'], spec['uvs'], spec['colors']
    count = len(p)//3
    vertices = [(p[i], -p[i+2], p[i+1]) for i in range(0,len(p),3)]
    mesh = bpy.data.meshes.new(f'world-{n}')
    mesh.from_pydata(vertices, [], [tuple(range(i,i+3)) for i in range(0,count,3)])
    mesh.update()
    texcoords = mesh.uv_layers.new(name='UV')
    colors = mesh.color_attributes.new(name='light', type='FLOAT_COLOR', domain='POINT')
    material, size, animated = materials[spec['material']]
    for i in range(count):
        u, v = uv[2*i:2*i+2]
        if animated:
            # Saved animated textures are vertical atlases: use their first
            # frame as a disclosed static approximation.
            v = 1 - (1-v) * size[0]/size[1]
        texcoords.data[i].uv = (u,v)
        colors.data[i].color = (*col[i*3:i*3+3],1)
    obj = bpy.data.objects.new(spec['id'], mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)

# Static simplified green beacon, placed using the saved renderer's position.
beam_mat = bpy.data.materials.new('beacon approximation')
beam_mat.diffuse_color = (.3,.8,.05,.35)
beam_mat.use_nodes = True
nodes = beam_mat.node_tree.nodes
nodes.clear()
out = nodes.new('ShaderNodeOutputMaterial')
trans = nodes.new('ShaderNodeBsdfTransparent')
emit = nodes.new('ShaderNodeEmission')
emit.inputs['Color'].default_value = (.22,.8,.025,1)
combine = nodes.new('ShaderNodeMixShader')
combine.inputs[0].default_value = .45
links = beam_mat.node_tree.links
links.new(trans.outputs[0], combine.inputs[1])
links.new(emit.outputs[0], combine.inputs[2])
links.new(combine.outputs[0], out.inputs['Surface'])
bpy.ops.mesh.primitive_cylinder_add(vertices=4,radius=.19,depth=32,location=(-.5,.5,16))
bpy.context.object.name = 'reconstructed beacon'
bpy.context.object.data.materials.append(beam_mat)

skin = bpy.data.images.load(str(SKIN), check_existing=True)
if tuple(skin.size) != (64,32):
    raise RuntimeError('Expected legacy 64x32 skin')
skinmat = bpy.data.materials.new('player skin')
skinmat.use_nodes = True
nodes = skinmat.node_tree.nodes
nodes.clear()
image = nodes.new('ShaderNodeTexImage')
image.image = skin
image.interpolation = 'Closest'
emit = nodes.new('ShaderNodeEmission')
out = nodes.new('ShaderNodeOutputMaterial')
skinmat.node_tree.links.new(image.outputs['Color'],emit.inputs['Color'])
skinmat.node_tree.links.new(emit.outputs[0],out.inputs['Surface'])
actor = bpy.data.objects.new('player', None)
bpy.context.collection.objects.link(actor)
# Staged position: feet on the existing command block; faces toward barrel a.
actor.location = (1.8,.42,1)
actor.scale = (.05625,)*3
actor.rotation_euler.z = math.radians(50)

# Explicit per-face legacy texture rectangles, independently checked against
# the UVs attached to each mesh. This is not comparison with a game capture.
UV = {
 'head': [(8,8,16,16),(24,8,32,16),(0,8,8,16),(16,8,24,16),(8,0,16,8),(16,0,24,8)],
 'torso': [(20,20,28,32),(32,20,40,32),(16,20,20,32),(28,20,32,32),(20,16,28,20),(28,16,36,20)],
 'arm': [(44,20,48,32),(52,20,56,32),(40,20,44,32),(48,20,52,32),(44,16,48,20),(48,16,52,20)],
 'leg': [(4,20,8,32),(12,20,16,32),(0,20,4,32),(8,20,12,32),(4,16,8,20),(8,16,12,20)],
}
uv_checks = 0
pixel_checks = 0

def cuboid(name, center, size, origin, reference, mirror=False, pivot=None):
    global uv_checks, pixel_checks
    x,y,z=center; w,h,d=size; a,b=origin
    l,r=x-w/2,x+w/2; f,k=y-d/2,y+d/2; lo,hi=z-h/2,z+h/2
    faces=[[(l,f,hi),(r,f,hi),(r,f,lo),(l,f,lo)],
           [(r,k,hi),(l,k,hi),(l,k,lo),(r,k,lo)],
           [(l,k,hi),(l,f,hi),(l,f,lo),(l,k,lo)],
           [(r,f,hi),(r,k,hi),(r,k,lo),(r,f,lo)],
           [(l,k,hi),(r,k,hi),(r,f,hi),(l,f,hi)],
           [(l,f,lo),(r,f,lo),(r,k,lo),(l,k,lo)]]
    rects=[(a+d,b+d,a+d+w,b+d+h),(a+2*d+w,b+d,a+2*d+2*w,b+d+h),
           (a,b+d,a+d,b+d+h),(a+d+w,b+d,a+2*d+w,b+d+h),
           (a+d,b,a+d+w,b+d),(a+d+w,b,a+d+2*w,b+d)]
    expected = list(UV[reference])
    if mirror:
        rects[2],rects[3]=rects[3],rects[2]
        expected[2],expected[3]=expected[3],expected[2]
    if rects != expected:
        raise RuntimeError(f'Unexpected {name} face rectangles')
    shift = Vector(pivot) if pivot else Vector((0,0,0))
    vertices=[tuple(Vector(v)-shift) for face in faces for v in face]
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],[tuple(range(i*4,i*4+4)) for i in range(6)])
    mesh.update()
    layer=mesh.uv_layers.new(name='SkinUV')
    for poly,(u0,v0,u1,v1),reference_rect in zip(mesh.polygons,rects,expected):
        if mirror:
            u0,u1=u1,u0
        coords=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
        for idx,(u,v) in zip(poly.loop_indices,coords):
            layer.data[idx].uv=(u/64,1-v/32)
            actual=layer.data[idx].uv
            if abs(actual.x-u/64)>1e-6 or abs(actual.y-(1-v/32))>1e-6:
                raise RuntimeError(f'Bad {name} UV')
            uv_checks += 1
        # Independently compare every pixel center interpolated from the
        # installed mesh UVs to the explicit legacy face rectangle.
        ru0,rv0,ru1,rv1=reference_rect
        width,height=ru1-ru0,rv1-rv0
        top_left=layer.data[poly.loop_indices[0]].uv
        top_right=layer.data[poly.loop_indices[1]].uv
        bottom_left=layer.data[poly.loop_indices[3]].uv
        for py in range(height):
            for px in range(width):
                fu,fv=(px+.5)/width,(py+.5)/height
                u=top_left.x+(top_right.x-top_left.x)*fu
                v=top_left.y+(bottom_left.y-top_left.y)*fv
                got=(math.floor(u*64),math.floor((1-v)*32))
                want=(ru1-1-px if mirror else ru0+px,rv0+py)
                if got != want:
                    raise RuntimeError(f'Bad {name} pixel mapping: {got} != {want}')
                pixel_checks += 1
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(skinmat)
    obj.parent=actor
    if pivot:
        obj.location=pivot
    return obj

cuboid('head',(0,0,28),(8,8,8),(0,0),'head')
cuboid('torso',(0,0,18),(8,12,4),(16,16),'torso')
arm=cuboid('right arm',(-6,0,18),(4,12,4),(40,16),'arm',pivot=(-6,0,24))
cuboid('left arm',(6,0,18),(4,12,4),(40,16),'arm',mirror=True)
cuboid('right leg',(-2,0,6),(4,12,4),(0,16),'leg')
cuboid('left leg',(2,0,6),(4,12,4),(0,16),'leg',mirror=True)
if uv_checks != 144:
    raise RuntimeError(f'Expected 144 UV corners, got {uv_checks}')
if pixel_checks != 1632:
    raise RuntimeError(f'Expected 1632 face pixel centers, got {pixel_checks}')
print('Verified 36 face rectangles, 144 UV corners and 1632 pixel centers against legacy mapping table')
for frame,deg in [(1,0),(52,0),(68,-65),(77,-65),(96,0),(180,0)]:
    arm.rotation_euler.x=math.radians(deg)
    arm.keyframe_insert(data_path='rotation_euler',index=0,frame=frame)
scene.frame_set(73)
bpy.context.view_layer.update()
hand=arm.matrix_world @ Vector((0,0,-12))
if not (2 <= hand.x <= 3 and -1 <= hand.y <= 0 and 2 <= hand.z <= 3):
    raise RuntimeError(f'Gesture misses the reconstructed a barrel: {tuple(hand)}')
print('At gesture peak, hand enters a barrel bounds:', tuple(round(v,3) for v in hand))

camera_data=bpy.data.cameras.new('camera')
camera=bpy.data.objects.new('camera',camera_data)
bpy.context.collection.objects.link(camera)
scene.camera=camera
camera_data.lens_unit='FOV'
camera_data.angle=math.radians(58)
target=bpy.data.objects.new('camera target',None)
bpy.context.collection.objects.link(target)
target.location=(1.35,.05,1.7)
constraint=camera.constraints.new(type='TRACK_TO')
constraint.target=target
constraint.track_axis='TRACK_NEGATIVE_Z'
constraint.up_axis='UP_Y'
for frame,angle in [(1,-.8),(46,-.76),(91,-.72),(136,-.68),(180,-.64)]:
    camera.location=(1.5+6*math.sin(angle), 6*math.cos(angle), 3.5)
    camera.keyframe_insert(data_path='location',frame=frame)
if camera.animation_data:
    for curve in camera.animation_data.action.fcurves:
        for point in curve.keyframe_points:
            point.interpolation='LINEAR'
if mode == 'verify':
    positions=[]
    for frame in range(1,181):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        positions.append(camera.matrix_world.translation.copy())
    deltas=[(b-a).length for a,b in zip(positions,positions[1:])]
    if min(deltas) <= 0:
        raise RuntimeError('Camera position repeats on adjacent frames')
    print('Camera moves on all 179 frame intervals; step range:',
          round(min(deltas),7), round(max(deltas),7))
scene.frame_start=1
scene.frame_end=180
scene.frame_set(still_frame if mode=='still' else 1)
if mode=='verify':
    print('World and skin checks passed; no image rendered')
elif mode=='still':
    scene.render.filepath=str(still_path)
    bpy.ops.render.render(write_still=True)
else:
    (OUT/'frames').mkdir()
    scene.render.filepath=str(OUT/'frames'/'frame-')
    bpy.ops.render.render(animation=True)
