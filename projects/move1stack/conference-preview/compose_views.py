#!/usr/bin/env python3
"""Combine the staged player, two barrel viewpoints and the SFM editor.

Barrel inventories, icon, fonts, gestures and camera cuts are illustrative;
the test establishes the two post-transfer inventory states, not this footage.
"""
import hashlib
import importlib.util
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/conference-slice-14'
THIRD=ROOT/'previews/conference-slice-13/frames'
FIRST=OUT/'frames'
GUI=ROOT/'previews/conference-slice-13/inventory-overlay.png'
EDITOR=ROOT/'previews/conference-slice-05/preview.mp4'
DIRT=ROOT/'ground-truth/assets/minecraft/textures/block/dirt.png'
EXPECTED={
 GUI:'d56c5816abc58a928ccd72df8eec722e4b52e088d3075a494d6f22361e070132',
 EDITOR:'e0f57bd136092f20ae818025324c73d07c94664b6ebfd030805b150ee7e9ac64',
 DIRT:'fb0450253248276e0b8d653d5a4d21c59763cbf775c0e048469ff500afaaef68',
}
for path,expected in EXPECTED.items():
    with path.open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=expected:
            raise SystemExit(f'Input hash mismatch: {path}')
for folder,count in [(THIRD,180),(FIRST,120)]:
    expected={f'frame-{n:04d}.png' for n in range(1,count+1)}
    if {p.name for p in folder.glob('frame-*.png')} != expected:
        raise SystemExit(f'Incomplete input frame sequence: {folder}')
video,preview,dest_gui=OUT/'output.mkv',OUT/'preview.mp4',OUT/'destination-overlay.png'
if any(p.exists() for p in (video,preview,dest_gui)):
    raise SystemExit('Output exists; preserve it and choose a new directory')
# The saved test asserts 64 dirt in destination slot zero after completion.
spec=importlib.util.spec_from_file_location('cutaway_panel',ROOT/'conference-preview/slice08.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
icon=mod.dirt_icon()
draw=ImageDraw.Draw(icon)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',8)
draw.text((7,9),'64',font=font,fill='#333333',stroke_width=1,stroke_fill='#333333')
draw.text((6,8),'64',font=font,fill='white')
layer=Image.open(GUI).convert('RGBA')
layer.alpha_composite(icon.resize((32,32),Image.Resampling.NEAREST),(224,86))
layer.save(dest_gui)
graph=(
 '[0:v]trim=end_frame=90,settb=expr=1/30,setpts=N,setsar=1[third];'
 '[1:v]split=2[sa][sb];'
 '[sa]trim=end_frame=60,settb=expr=1/30,setpts=N[av];'
 '[sb]trim=start_frame=60:end_frame=120,settb=expr=1/30,setpts=N[bv];'
 '[2:v]trim=duration=2,settb=expr=1/30,setpts=N[ag];'
 '[3:v]trim=duration=2,settb=expr=1/30,setpts=N[bg];'
 "[av][ag]overlay=0:0:enable='gte(n,18)':shortest=1,setsar=1[a];"
 "[bv][bg]overlay=0:0:enable='gte(n,18)':shortest=1,setsar=1[b];"
 '[4:v]trim=start=8:duration=2,scale=768:432,settb=expr=1/30,setpts=N,setsar=1[editor];'
 '[third][a][b][editor]concat=n=4:v=1:a=0,format=yuv420p[v]'
)
subprocess.run(['ffmpeg','-v','error','-framerate','30','-start_number','1','-i',str(THIRD/'frame-%04d.png'),
                '-framerate','30','-start_number','1','-i',str(FIRST/'frame-%04d.png'),
                '-loop','1','-framerate','30','-i',str(GUI),'-loop','1','-framerate','30','-i',str(dest_gui),
                '-i',str(EDITOR),'-filter_complex',graph,'-map','[v]','-frames:v','270','-r','30',
                '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
                '-metadata','title=SFM staged multi-view walkthrough','-n',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                '-movflags','+faststart','-n',str(preview)],check=True)
print(f'Created {video} and {preview}')
