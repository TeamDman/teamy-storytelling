from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
import numpy as np
root=Path(__file__).parent
out=root/'comparisons';out.mkdir(exist_ok=True)
contact=Image.new('RGB',(1280,8*200),'#182330');d=ImageDraw.Draw(contact)
metrics=[]
for i in range(1,9):
 ref=Image.open(root/f'reference-evidence/reference/figure_0{i}_orbit-0{i-1}.png').convert('RGB').crop((0,87,1280,807))
 got=Image.open(root/f'stills/figure-0{i}.png').convert('RGB')
 ref.save(out/f'reference-0{i}-viewport.png')
 pair=Image.new('RGB',(2560,770),'#182330');pair.paste(ref,(0,50));pair.paste(got,(1280,50));pd=ImageDraw.Draw(pair)
 pd.text((24,15),f'FIGURE {i}  /  ORIGINAL GAME CAPTURE (87 px caption cropped)',fill='white',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20))
 pd.text((1304,15),'THREE.JS RECONSTRUCTION  /  recorded optical pose, provisional FOV 70',fill='white',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20))
 pair.save(out/f'comparison-0{i}.png')
 contact.paste(ref.resize((320,180)),(0,(i-1)*200+20));contact.paste(got.resize((320,180)),(320,(i-1)*200+20));d.text((8,(i-1)*200+3),f'{i} ORIGINAL',fill='white');d.text((328,(i-1)*200+3),'RECONSTRUCTION',fill='white')
 delta=np.abs(np.asarray(ref).astype(float)-np.asarray(got).astype(float));metrics.append({'figure':i,'fullViewportMAE8bit':round(float(delta.mean()),4),'note':'Includes terrain/horizon, uncalibrated lightmap/AO and unknown animation phase; not a geometry-only score.'})
# Compact contact sheet without blank half.
contact.crop((0,0,640,1600)).save(out/'all-eight-contact.png')
(out/'metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics))
