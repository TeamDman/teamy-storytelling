#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
choices={
'route':[2,16,25,36,40,53,65,79,87,91,101,115,121,132,139,144,153,169,180,193,205,212,220],
'forensic':[2,17,26,31,43,58,70,83,95,107,116,123,134,141,147,156,170,182,194,207,214,222],
'atlas':[7,18,33,45,58,72,86,100,114,121,126,136,144,151,159,164,174,188,200,214,223,229]
}
for name in sys.argv[1:]:
 dest=root/'review'/name/'final';dest.mkdir(exist_ok=True,parents=True)
 for t in choices[name]:
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(root/'renders'/f'{name}.mp4'),'-frames:v','1',str(dest/f'{t:04}.png')],check=True)
 count=len(choices[name]);out=Image.new('RGB',(1920,250*((count+4)//5)),(25,29,35));draw=ImageDraw.Draw(out)
 for i,t in enumerate(choices[name]):
  im=Image.open(dest/f'{t:04}.png');im.thumbnail((384,216));x=i%5*384;y=i//5*250;out.paste(im,(x,y));draw.text((x+12,y+225),f'{t//60:02}:{t%60:02}',fill='white')
 out.save(root/'review'/name/'contact-final.png')
 print(name,'final video frames',count)
