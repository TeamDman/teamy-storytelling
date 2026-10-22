#!/usr/bin/env python3
"""Package canonical files and inspect the actual encoded timeline.

Run after the Motion Canvas render. All chapter starts come from the scene's
recorded generator timeline. MP4 preview remains outside the two-file contract.
"""
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('treatment')
args=parser.parse_args(); name=args.treatment
render=root/'renders'/f'{name}.mp4'
report=json.loads((root/'renders'/f'{name}-render.json').read_text())
assert report['result']==0, report
timeline=report['timelines'][name]
scene_duration=timeline[-1]['end']
fps=24
# Motion Canvas exports the closing boundary frame inclusively. Preserve it
# without another lossy encode, and extend the final cue to its encoded end.
expected_frames=round(scene_duration*fps)+1
duration=expected_frames/fps
timeline[-1]['end']=duration
chapters=[c for c in timeline if c.get('chapter')]
assert chapters and chapters[0]['start']==0
titles={'route':'Keep the route open','forensic':'The one-FE gap','atlas':'Inside the release'}
meta=[';FFMETADATA1','title=SFM 4.35 — '+titles[name]]
for i,c in enumerate(chapters):
    end=chapters[i+1]['start'] if i+1<len(chapters) else duration
    meta+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(c["start"]*1000)}',f'END={round(end*1000)}','title='+c['title'].replace('=','\\=')]
work=root/'review'/name;work.mkdir(exist_ok=True,parents=True)
metadata=work/'chapters.ffmeta';metadata.write_text('\n'.join(meta)+'\n')
dest=root/'deliverables'/name;dest.mkdir(exist_ok=True,parents=True)
previews=root/'deliverables'/'previews';previews.mkdir(exist_ok=True,parents=True)
def run(*cmd,capture=False):
    return subprocess.run([str(v) for v in cmd],check=True,capture_output=capture,text=capture)
run('ffmpeg','-v','error','-y','-i',render,'-i',metadata,'-map','0:v:0','-map_metadata','1','-map_chapters','1','-c','copy','-disposition:v:0','default','-t',str(duration),dest/'output.mkv')
run('ffmpeg','-v','error','-y','-i',dest/'output.mkv','-map','0:v:0','-c','copy','-movflags','+faststart',previews/f'{name}.mp4')
probe=json.loads(run('ffprobe','-v','error','-count_frames','-show_streams','-show_chapters','-show_format','-of','json',dest/'output.mkv',capture=True).stdout)
video=probe['streams'][0]
assert video['width']==1920 and video['height']==1080
assert len(probe['streams'])==1 and video['codec_name']=='h264'
assert video['pix_fmt']=='yuv420p' and video['r_frame_rate']=='24/1'
assert video['disposition']['default']==1
assert abs(float(probe['format']['duration'])-duration)<1/fps+.01
assert len(probe['chapters'])==len(chapters)
assert int(video['nb_read_frames'])==expected_frames
for p,c in zip(probe['chapters'],chapters):
    assert abs(float(p['start_time'])-c['start'])<.002
    assert p['tags']['title']==c['title']
for file in [dest/'output.mkv',previews/f'{name}.mp4']:
    result=run('ffmpeg','-v','error','-xerror','-i',file,'-f','null','-',capture=True)
    assert not result.stderr, result.stderr
validation={'duration':float(probe['format']['duration']),'scene_duration':scene_duration,'closing_boundary_frame':'Preserved from native Motion Canvas export; final cue and chapter include it.','frames':int(video['nb_read_frames']),'dimensions':[video['width'],video['height']],'codec':video['codec_name'],'pixel_format':video['pix_fmt'],'fps':video['r_frame_rate'],'audio_streams':0,'default_video':True,
    'full_decode':'PASS','preview_decode':'PASS','chapters':probe['chapters'],'timeline':timeline,
    'source_render_seconds':report.get('seconds'),'visual_review':'See REVIEW.md; contact sheet and actual frames must be inspected.'}
(work/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
(work/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
staging=work/'extras'
if staging.exists():shutil.rmtree(staging)
staging.mkdir()
source=staging/'source';source.mkdir()
for item in ['src','scripts','render.html','vite.config.mjs','package.json','tsconfig.json','ATTRIBUTION.md','README.md','ENVIRONMENT.md']:
    p=root/item
    if p.is_dir():shutil.copytree(p,source/item,ignore=shutil.ignore_patterns('*.meta','__pycache__'))
    elif p.exists():shutil.copy2(p,source/item)
license_path=root/'LICENSE'
if not license_path.exists():license_path=root.parents[1]/'LICENSE'
shutil.copy2(license_path,source/'LICENSE')
for item in [f'{name}-storyboard.md',f'{name}-presenter-notes.md','commands.md','provenance.json','source-excerpts.md','inventory.json','inventory.md','REVIEW.md']:
    p=root/'handoff'/item
    if not p.exists():raise FileNotFoundError(f'Required extra missing: {p.name}')
    shutil.copy2(p,staging/item)
for item in ['validation.json','timeline.json','chapters.ffmeta']:shutil.copy2(work/item,staging/item)
contact=work/'contact-final.png'
if contact.exists():shutil.copy2(contact,staging/'contact-sheet.png')
for p in staging.rglob('*'):
    assert not p.is_symlink() and '..' not in p.relative_to(staging).parts
archive=dest/'extras.7z';archive.unlink(missing_ok=True)
subprocess.run(['7z','a','-t7z',str(archive),'.'],cwd=staging,check=True,stdout=subprocess.DEVNULL)
run('7z','t',archive,capture=True)
listing=run('7z','l','-slt',archive,capture=True).stdout
(work/'archive-list.txt').write_text(listing)
assert sorted(p.name for p in dest.iterdir())==['extras.7z','output.mkv']
for p in [dest/'output.mkv',archive,previews/f'{name}.mp4']:
    print(json.dumps({'file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()}))
