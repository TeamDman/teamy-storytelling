#!/usr/bin/env python3
"""Encode the preserved Blender frames without retiming or replacing them."""
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/conference-slice-12'
FRAMES = OUT / 'frames'
expected = {f'frame-{n:04d}.png' for n in range(1,181)}
actual = {p.name for p in FRAMES.glob('frame-*.png')}
if actual != expected:
    raise SystemExit(f'Expected exactly 180 numbered frames; missing={len(expected-actual)}, extra={len(actual-expected)}')
video, preview = OUT / 'output.mkv', OUT / 'preview.mp4'
if video.exists() or preview.exists():
    raise SystemExit('Output exists; preserve it and choose a new directory')
subprocess.run(['ffmpeg','-v','error','-framerate','30','-start_number','1','-i',str(FRAMES/'frame-%04d.png'),
                '-frames:v','180','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
                '-metadata','title=SFM world and skin gesture reconstruction','-n',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                '-movflags','+faststart','-n',str(preview)],check=True)
print(f'Created {video} and {preview}')
