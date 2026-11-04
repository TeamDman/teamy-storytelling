#!/usr/bin/env python3
"""720p integer-scaled typography proof; still uses provisional fonts.

This is a scaling experiment, not a Minecraft font recreation. It preserves
logical inventory pixels at 3x and keeps the original 720p editor image at native pixels.
"""
import hashlib
import subprocess
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/conference-slice-16'
THIRD=ROOT/'previews/conference-slice-13/frames'
FIRST=ROOT/'previews/conference-slice-14/frames'
GUI_A=ROOT/'previews/conference-slice-13/inventory-overlay.png'
GUI_B=ROOT/'previews/conference-slice-14/destination-overlay.png'
EDITOR=ROOT/'previews/conference-slice-05/editor.png'
ORBIT=ROOT/'deliverable/output.mkv'
EXPECTED={
 GUI_A:'d56c5816abc58a928ccd72df8eec722e4b52e088d3075a494d6f22361e070132',
 GUI_B:'2e7120393beef39c8a345914568b461cb57d81a6eac0bd06f40e74e7d455542e',
 EDITOR:'1b6250d2e2c796977412003bf9332dd1389a7370c1e442ba3a0c2dce97ac5a41',
 ORBIT:'ffe2d3f7f68c67de44e0439c6ffdf4e512f79c0ed93a651b6d83f6345908c3b5',
}
for path,expected in EXPECTED.items():
    with path.open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=expected:
            raise SystemExit(f'Input hash mismatch: {path}')
for folder,count in [(THIRD,180),(FIRST,120)]:
    expected={f'frame-{n:04d}.png' for n in range(1,count+1)}
    if {p.name for p in folder.glob('frame-*.png')} != expected:
        raise SystemExit(f'Incomplete input frame sequence: {folder}')
if OUT.exists() and any(OUT.iterdir()):
    raise SystemExit('Output exists; preserve it and choose a new directory')
OUT.mkdir(parents=True,exist_ok=True)

def make_overlay(source,destination):
    panel2=Image.open(source).convert('RGBA').crop((208,50,560,382))
    native=panel2.resize((176,166),Image.Resampling.NEAREST)
    if native.resize((352,332),Image.Resampling.NEAREST).tobytes()!=panel2.tobytes():
        raise SystemExit(f'Inventory source is not exact 2x pixels: {source}')
    overlay=Image.new('RGBA',(1280,720),(0,0,0,112))
    overlay.alpha_composite(native.resize((528,498),Image.Resampling.NEAREST),(376,111))
    overlay.save(destination)

ag,bg=OUT/'source-overlay.png',OUT/'destination-overlay.png'
make_overlay(GUI_A,ag)
make_overlay(GUI_B,bg)
graph=(
 '[0:v]trim=end_frame=90,scale=1280:720:flags=lanczos,settb=expr=1/30,setpts=N,setsar=1[third];'
 '[1:v]split=2[sa][sb];'
 '[sa]trim=end_frame=60,scale=1280:720:flags=lanczos,settb=expr=1/30,setpts=N[av];'
 '[sb]trim=start_frame=60:end_frame=120,scale=1280:720:flags=lanczos,settb=expr=1/30,setpts=N[bv];'
 '[2:v]trim=duration=2,settb=expr=1/30,setpts=N[ag];'
 '[3:v]trim=duration=2,settb=expr=1/30,setpts=N[bg];'
 "[av][ag]overlay=0:0:enable='gte(n,18)':shortest=1:format=rgb,setsar=1[a];"
 "[bv][bg]overlay=0:0:enable='gte(n,18)':shortest=1:format=rgb,setsar=1[b];"
 '[4:v]trim=duration=2,settb=expr=1/30,setpts=N[editorbg];'
 '[5:v]trim=start=8:duration=2,scale=320:180:flags=neighbor,settb=expr=1/30,setpts=N[editorworld];'
 '[editorbg][editorworld]overlay=933:68:shortest=1:format=rgb,setsar=1[editor];'
 '[third][a][b][editor]concat=n=4:v=1:a=0,format=yuv444p[v]'
)
video,preview=OUT/'output.mkv',OUT/'preview.mp4'
subprocess.run(['ffmpeg','-v','error','-framerate','30','-start_number','1','-i',str(THIRD/'frame-%04d.png'),
                '-framerate','30','-start_number','1','-i',str(FIRST/'frame-%04d.png'),
                '-loop','1','-framerate','30','-i',str(ag),'-loop','1','-framerate','30','-i',str(bg),
                '-loop','1','-framerate','30','-i',str(EDITOR),'-i',str(ORBIT),'-filter_complex',graph,'-map','[v]','-frames:v','270','-r','30',
                '-c:v','libx264','-profile:v','high444','-preset','medium','-crf','12','-pix_fmt','yuv444p',
                '-metadata','title=SFM provisional integer-scale typography proof','-n',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                '-movflags','+faststart','-n',str(preview)],check=True)
print(f'Created {video} and {preview}')
