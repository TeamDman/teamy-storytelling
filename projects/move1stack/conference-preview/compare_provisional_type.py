#!/usr/bin/env python3
"""Compare provisional editor scaling; does not verify the Minecraft font."""
import argparse
import io
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'previews/conference-slice-14/preview.mp4'
NEW=ROOT/'previews/conference-slice-16/preview.mp4'
REF=ROOT/'previews/conference-slice-05/editor.png'
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=ROOT/'previews/conference-slice-16/provisional-font-comparison.png')
args=parser.parse_args()
if args.output.exists():
    raise SystemExit(f'Output exists; preserve it: {args.output}')

def frame(path):
    data=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vf',"select='eq(n,240)'",'-frames:v','1',
                         '-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True).stdout
    return Image.open(io.BytesIO(data)).convert('RGB')

before=frame(OLD).resize((1280,720),Image.Resampling.BILINEAR)
after=frame(NEW)
reference=Image.open(REF).convert('RGB')
box=(39,32,320,144)
for name,img in [('previous',before),('integer scale',after)]:
    actual=np.asarray(img.crop(box),dtype=np.int16)
    expected=np.asarray(reference.crop(box),dtype=np.int16)
    delta=np.abs(actual-expected)
    print(name, 'mean channel error:',round(float(delta.mean()),3),
          'pixels with max error > 20:',int((delta.max(axis=2)>20).sum()))
scale=3
left=before.crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale),Image.Resampling.NEAREST)
right=after.crop(box).resize(left.size,Image.Resampling.NEAREST)
w,h=left.size
out=Image.new('RGB',(w*2+36,h+68),'#1b2433')
draw=ImageDraw.Draw(out)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
draw.text((12,15),'Earlier: reduced to 432p',font=font,fill='white')
draw.text((w+24,15),'720p integer scaling — provisional font',font=font,fill='white')
out.paste(left,(12,52))
out.paste(right,(w+24,52))
out.save(args.output)
print(f'Created {args.output}')
