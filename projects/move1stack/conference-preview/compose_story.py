#!/usr/bin/env python3
"""Assemble the existing staged shots into a single short story preview.

All shots are reconstructions. The second player is a labeled placeholder;
the UI, fonts, gesture and viewpoints are not verified game captures.
"""
import hashlib
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews/conference-slice-18'
S05=ROOT/'previews/conference-slice-05/preview.mp4'
S08=ROOT/'previews/conference-slice-08/preview.mp4'
S16=ROOT/'previews/conference-slice-16/preview.mp4'
S17=ROOT/'previews/conference-slice-17/preview.mp4'
EXPECTED={
 S05:'e0f57bd136092f20ae818025324c73d07c94664b6ebfd030805b150ee7e9ac64',
 S08:'5fa0268e8748f8e8324f0719fbc5bcdae4ed8b3913defc736d1087b595ff2d5c',
 S16:'e13f02da070685ff7086409f9da7d5fe4ad3ae43dc04f4fb96033ae11490e570',
 S17:'99402156c210abf72a3a2cc3c118ed7434512ef33b8bdbf07b552be3b9941742',
}
for path,expected in EXPECTED.items():
    with path.open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=expected:
            raise SystemExit(f'Input hash mismatch: {path}')
if OUT.exists() and any(OUT.iterdir()):
    raise SystemExit('Output exists; preserve it and choose a new directory')
OUT.mkdir(parents=True,exist_ok=True)
# Cuts are intentional: manager-to-editor at the existing Edit action, then
# the transfer, the labeled two-character shot, and both close viewpoints.
graph=(
 '[0:v]trim=end_frame=240,settb=expr=1/30,setpts=N,setsar=1,format=yuv444p[manager];'
 '[1:v]trim=start_frame=60:end_frame=240,settb=expr=1/30,setpts=N,setsar=1,format=yuv444p[transfer];'
 '[2:v]split=2[e0][p0];'
 '[e0]trim=start_frame=210:end_frame=270,settb=expr=1/30,setpts=N,setsar=1,format=yuv444p[editor];'
 '[p0]trim=start_frame=90:end_frame=210,settb=expr=1/30,setpts=N,setsar=1,format=yuv444p[views];'
 '[3:v]trim=end_frame=90,settb=expr=1/30,setpts=N,setsar=1,format=yuv444p[characters];'
 '[manager][editor][transfer][characters][views]concat=n=5:v=1:a=0,format=yuv444p[v]'
)
video,preview=OUT/'output.mkv',OUT/'preview.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(S05),'-i',str(S08),'-i',str(S16),'-i',str(S17),
                '-filter_complex',graph,'-map','[v]','-frames:v','690','-r','30','-c:v','libx264',
                '-profile:v','high444','-preset','medium','-crf','12','-pix_fmt','yuv444p',
                '-metadata','title=Move one stack - staged story preview','-n',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                '-movflags','+faststart','-n',str(preview)],check=True)
print(f'Created {video} and {preview}')
