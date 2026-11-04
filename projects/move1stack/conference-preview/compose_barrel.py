#!/usr/bin/env python3
"""Compose an illustrative empty barrel screen over the staged open animation.

The real Minecraft GUI texture/font were not included in the restored inputs;
this is not an actual game capture or a pixel-exact inventory screen.
"""
import hashlib
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/conference-slice-13'
FRAMES = OUT / 'frames'
expected = {f'frame-{n:04d}.png' for n in range(1,181)}
actual = {p.name for p in FRAMES.glob('frame-*.png')}
if actual != expected:
    raise SystemExit(f'Expected exactly 180 frames; missing={len(expected-actual)}, extra={len(actual-expected)}')
video, preview, overlay = OUT / 'output.mkv', OUT / 'preview.mp4', OUT / 'inventory-overlay.png'
if any(p.exists() for p in (video,preview,overlay)):
    raise SystemExit('Output exists; preserve it and choose a new directory')
# Reuse the source SFM manager's original 176x166 frame and player-inventory
# slots, repeating the actual slot pixels for the barrel's three rows. This is
# still a reconstruction: the vanilla barrel GUI texture and font are absent.
manager = ROOT / '.inputs/sfm-gui/manager.png'
with manager.open('rb') as f:
    if hashlib.file_digest(f,'sha256').hexdigest() != 'b6945789f1b663261a0c3bc6f922052a41f827cbd966e5014cadbc188eb7dea0':
        raise SystemExit('Manager GUI texture hash mismatch')
source = Image.open(manager).convert('RGBA')
panel = source.crop((0,0,176,166))
panel.paste(source.crop((7,83,169,137)),(7,17))
draw = ImageDraw.Draw(panel)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',8)
draw.text((8,5),'Barrel',font=font,fill='#404040')
draw.text((8,71),'Inventory',font=font,fill='#404040')
# The actual walkthrough opens source a only after the transfer, when empty.
panel = panel.resize((352,332), Image.Resampling.NEAREST)
layer = Image.new('RGBA',(768,432),(0,0,0,112))
layer.alpha_composite(panel,(208,50))
layer.save(overlay)
graph = ("[0:v]settb=expr=1/30,setpts=N[world];"
         "[1:v]trim=duration=6,settb=expr=1/30,setpts=N[gui];"
         "[world][gui]overlay=0:0:enable='gte(n,94)':shortest=1,format=yuv420p[v]")
subprocess.run(['ffmpeg','-v','error','-framerate','30','-start_number','1','-i',str(FRAMES/'frame-%04d.png'),
                '-loop','1','-framerate','30','-i',str(overlay),'-filter_complex',graph,'-map','[v]',
                '-frames:v','180','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
                '-metadata','title=SFM staged barrel open and reconstructed inventory','-n',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                '-movflags','+faststart','-n',str(preview)],check=True)
print(f'Created {video} and {preview}')
