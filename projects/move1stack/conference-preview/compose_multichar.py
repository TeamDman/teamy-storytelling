#!/usr/bin/env python3
"""Assemble staged two-player and barrel-view shots without inventory text."""
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/conference-slice-17'
THIRD=OUT/'frames'
VIEWS=ROOT/'previews/conference-slice-14/frames'
for folder,count in ((THIRD,90),(VIEWS,120)):
    expected={f'frame-{n:04d}.png' for n in range(1,count+1)}
    if {p.name for p in folder.glob('frame-*.png')}!=expected:
        raise SystemExit(f'Incomplete frame sequence: {folder}')
label,video,preview=OUT/'placeholder-label.png',OUT/'output.mkv',OUT/'preview.mp4'
if any(p.exists() for p in (label,video,preview)):
    raise SystemExit('Output exists; preserve it and choose a new directory')
layer=Image.new('RGBA',(1280,720),(0,0,0,0))
draw=ImageDraw.Draw(layer)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
draw.rounded_rectangle((145,273,263,299),radius=4,fill=(0,0,0,170))
draw.text((153,278),'PLACEHOLDER',font=font,fill=(255,255,255,255))
layer.save(label)
graph=(
 '[0:v]scale=1280:720:flags=lanczos,settb=expr=1/30,setpts=N,setsar=1[third];'
 '[2:v]trim=duration=3,settb=expr=1/30,setpts=N[label];'
 '[third][label]overlay=0:0:shortest=1,setsar=1[scene];'
 '[1:v]scale=1280:720:flags=lanczos,settb=expr=1/30,setpts=N,setsar=1[views];'
 '[scene][views]concat=n=2:v=1:a=0,format=yuv420p[v]'
)
subprocess.run(['ffmpeg','-v','error','-framerate','30','-start_number','1','-i',str(THIRD/'frame-%04d.png'),
                '-framerate','30','-start_number','1','-i',str(VIEWS/'frame-%04d.png'),
                '-loop','1','-framerate','30','-i',str(label),'-filter_complex',graph,'-map','[v]',
                '-frames:v','210','-r','30','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
                '-metadata','title=SFM staged multi-character camera proof','-n',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                '-movflags','+faststart','-n',str(preview)],check=True)
print(f'Created {video} and {preview}')
