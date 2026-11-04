"""Stage the supplied player and an untextured placeholder in the 3D fixture.

The second figure has no supplied identity or skin. Positions, gestures and
camera are staged; this is not Minecraft footage or a verified game animation.
"""
import runpy
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/conference-slice-17'
OUT.mkdir(parents=True,exist_ok=True)
mode='verify' if '--verify' in sys.argv else 'render' if '--render' in sys.argv else 'still'
frame=int(sys.argv[sys.argv.index('--frame')+1]) if '--frame' in sys.argv else 75
still=OUT/f'still-{frame:03d}.png'
if mode=='render' and (OUT/'frames').exists():
    raise RuntimeError('Frames already exist; preserve them')
if mode=='still' and still.exists():
    raise RuntimeError('Still already exists; preserve it')
argv=sys.argv[:]
sys.argv=[argv[0],'--verify']
runpy.run_path(str(ROOT/'conference-preview/world_barrel.py'),run_name='__main__')
sys.argv=argv
scene=bpy.context.scene
scene.frame_set(1)
# Neutral, deliberately untextured stand-in; per-face values make its block
# geometry readable without suggesting a supplied skin or identity.
def placeholder_material(part,face):
    strength={'head':1.1,'torso':.8,'arm':.95,'leg':.7}[part]
    shade=(.9,.75,.66,.82,1.15,.55)[face]*strength
    material=bpy.data.materials.new(f'placeholder {part} face {face}')
    material.use_nodes=True
    nodes=material.node_tree.nodes
    nodes.clear()
    emission=nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value=(.22*shade,.29*shade,.35*shade,1)
    out=nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(emission.outputs[0],out.inputs['Surface'])
    return material
placeholder=bpy.data.objects.new('participant placeholder',None)
bpy.context.collection.objects.link(placeholder)
placeholder.location=(3.35,1.35,0)
placeholder.scale=(.05625,)*3
placeholder.rotation_euler.z=-1.03  # Faces toward the staged player.
for name in ('head','torso','right arm','left arm','right leg','left leg'):
    original=bpy.data.objects[name]
    part=original.copy()
    part.data=original.data.copy()
    part.name='placeholder '+name
    part.animation_data_clear()
    part.parent=placeholder
    part.rotation_euler=(0,0,0)
    part.data.materials.clear()
    kind='arm' if 'arm' in name else 'leg' if 'leg' in name else name
    for face in range(6):
        part.data.materials.append(placeholder_material(kind,face))
    for face,polygon in enumerate(part.data.polygons):
        polygon.material_index=face
    bpy.context.collection.objects.link(part)
actor=bpy.data.objects['player']
if (Vector(actor.location)-Vector(placeholder.location)).length < 1:
    raise RuntimeError('Characters overlap')
if not (3 <= placeholder.location.x <= 4 and 1 <= placeholder.location.y <= 2 and placeholder.location.z == 0):
    raise RuntimeError('Placeholder not placed on the restored ground')
scene.frame_start=1
scene.frame_end=90
if mode=='verify':
    print('Two distinct staged figures; placeholder is untextured and on the ground')
    print('Two characters are separated by',round((Vector(actor.location)-Vector(placeholder.location)).length,3),'world units')
elif mode=='still':
    scene.frame_set(frame)
    scene.render.filepath=str(still)
    bpy.ops.render.render(write_still=True)
else:
    (OUT/'frames').mkdir()
    scene.frame_set(1)
    scene.render.filepath=str(OUT/'frames'/'frame-')
    bpy.ops.render.render(animation=True)
