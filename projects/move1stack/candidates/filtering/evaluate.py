from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[2]
poses=json.loads((root/'ground-truth/scene-manifest.json').read_text())['cameras']['reference_optical_poses']
rows=[];sheet=Image.new('RGB',(1200,8*220),'#182330');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for i,p in enumerate(poses):
 n=i+1
 ref=Image.open(root/f'reference-evidence/reference/figure_0{n}_orbit-0{i}.png').convert('RGB').crop((0,87,1280,807))
 first=Image.open(root/f'candidates/filtering/first/figure-0{n}.png').convert('RGB')
 after=Image.open(root/f'candidates/filtering/source-cutout/figure-0{n}.png').convert('RGB')
 f=np.array(p['forward']);r=np.cross(f,[0,1,0]);r/=np.linalg.norm(r);u=np.cross(r,f);eye=np.array([p['local_eye'][a] for a in ['x','y','z']]);scale=720/(2*math.tan(math.radians(35)))
 corners=[]
 for x in [-1,0]:
  for y in [-1,1]:
   for z in [-1,0]:
    v=np.array([x,y,z])-eye;depth=np.dot(f,v);corners.append([640+scale*np.dot(r,v)/depth,360-scale*np.dot(u,v)/depth])
 xs,ys=zip(*corners);box=(max(0,math.floor(min(xs))-12),max(0,math.floor(min(ys))-12),min(1280,math.ceil(max(xs))+12),min(720,math.ceil(max(ys))+12))
 preserved=root/f'stills/figure-0{n}.png'
 if not preserved.exists():preserved=root.parent/f'first/figure-0{n}.png'
 a=np.asarray(ref).astype(float);b=np.asarray(first).astype(float);c=np.asarray(after).astype(float);changed=np.any(b!=c,axis=2);x,y,X,Y=box
 bb=np.abs(a-b);cc=np.abs(a-c)
 row={'figure':n,'baselineMatchesPreservedPixels':(np.array_equal(np.array(first),np.array(Image.open(preserved).convert('RGB'))) if preserved.exists() else None),'changedPixels':int(changed.sum()),'wholeImageBeforeMAE':float(bb.mean()),'wholeImageAfterMAE':float(cc.mean()),'beaconROIBeforeMAE':float(bb[y:Y,x:X].mean()),'beaconROIAfterMAE':float(cc[y:Y,x:X].mean()),'beaconROI':box,'changedPixelsBeforeMAE':float(bb[changed].mean()) if changed.any() else 0,'changedPixelsAfterMAE':float(cc[changed].mean()) if changed.any() else 0}
 rows.append(row)
 for j,(label,image) in enumerate([('REFERENCE',ref),('FIRST',first),('SOURCE CUTOUT',after)]):
  crop=image.crop(box);crop.thumbnail((380,185));sheet.paste(crop,(400*j,220*i+25));draw.text((400*j+5,220*i+5),f'{n} {label}',font=font,fill='white')
sheet.save(root/'candidates/filtering/beacon-crops.png')
(root/'candidates/filtering/comparison-metrics.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
