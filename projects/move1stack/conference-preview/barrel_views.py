"""Reconstructed source/destination point-of-view shots in the saved 3D fixture.

The camera placement and motion are staged. The walkthrough establishes the
barrel order and post-transfer contents, not this camera path or footage.
"""
import runpy
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/conference-slice-14'
OUT.mkdir(parents=True,exist_ok=True)
mode='verify' if '--verify' in sys.argv else 'render' if '--render' in sys.argv else 'still'
frame=int(sys.argv[sys.argv.index('--frame')+1]) if '--frame' in sys.argv else 30
still=OUT/f'view-{frame:03d}.png'
if mode=='render' and (OUT/'frames').exists():
    raise RuntimeError('Frames exist; preserve the previous render')
if mode=='still' and still.exists():
    raise RuntimeError('Still exists; preserve the previous render')
# Reuse the checked world/model construction without rendering its prior shot.
argv=sys.argv[:]
sys.argv=[argv[0],'--verify']
runpy.run_path(str(ROOT/'conference-preview/world_barrel.py'),run_name='__main__')
sys.argv=argv
scene=bpy.context.scene
camera=scene.camera
target=bpy.data.objects['camera target']
camera.animation_data_clear()
target.animation_data_clear()
# First-person framing omits the third-person model. No first-person hand
# animation is asserted or fabricated.
for name in ('head','torso','right arm','left arm','right leg','left leg'):
    bpy.data.objects[name].hide_render=True

def visibility(obj,values):
    obj.animation_data_clear()
    for f,visible in values:
        obj.hide_render=not visible
        obj.keyframe_insert(data_path='hide_render',frame=f)

source_closed=bpy.data.objects['19-test_barrel/0/up']
source_open=bpy.data.objects['barrel a open front']
dest_closed=bpy.data.objects['17-test_barrel/0/up']
dest_open=dest_closed.copy()
dest_open.data=dest_closed.data.copy()
dest_open.name='barrel b open front'
bpy.context.collection.objects.link(dest_open)
dest_open.data.materials.clear()
dest_open.data.materials.append(source_open.data.materials[0])
visibility(source_open,[(1,True),(60,True),(61,False),(120,False)])
visibility(source_closed,[(1,False),(60,False),(61,True),(120,True)])
visibility(dest_open,[(1,False),(60,False),(61,True),(120,True)])
visibility(dest_closed,[(1,True),(60,True),(61,False),(120,False)])
# Two separate staged eye-level views, with a discrete cut at frame 61. The
# slow movement within each view is a presentation camera, not game movement.
poses=[(1,(2.15,2.0,2.62),(2.5,0,2.5)),(60,(2.15,1.95,2.62),(2.5,0,2.5)),
       (61,(.15,2.0,2.62),(.5,0,2.5)),(120,(.15,1.95,2.62),(.5,0,2.5))]
for f,pos,look in poses:
    camera.location=pos
    camera.keyframe_insert(data_path='location',frame=f)
    target.location=look
    target.keyframe_insert(data_path='location',frame=f)
for obj in (camera,target):
    for curve in obj.animation_data.action.fcurves:
        for key in curve.keyframe_points:
            key.interpolation='CONSTANT' if round(key.co.x)==60 else 'LINEAR'
scene.frame_start=1
scene.frame_end=120
if mode=='verify':
    positions=[]
    for f in range(1,121):
        scene.frame_set(f)
        bpy.context.view_layer.update()
        positions.append(camera.matrix_world.translation.copy())
        expected_source=f<=60
        if source_open.hide_render == expected_source or dest_open.hide_render != expected_source:
            raise RuntimeError(f'Wrong open barrel at frame {f}')
    deltas=[(positions[i+1]-positions[i]).length for i in range(119) if i!=59]
    if min(deltas)<=0:
        raise RuntimeError('Camera repeats within a moving viewpoint')
    print('Verified source and destination open states and all 118 within-view camera steps;',
          'range',round(min(deltas),7),round(max(deltas),7),'with one deliberate cut')
scene.frame_set(frame if mode=='still' else 1)
if mode=='verify':
    print('Viewpoint checks passed; no image rendered')
elif mode=='still':
    scene.render.filepath=str(still)
    bpy.ops.render.render(write_still=True)
else:
    (OUT/'frames').mkdir()
    scene.render.filepath=str(OUT/'frames'/'frame-')
    bpy.ops.render.render(animation=True)
