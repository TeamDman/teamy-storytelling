#!/usr/bin/env python3
"""Render a slot-sized dirt stack using 1.19.2 GUI geometry and bitmap font.

Texture orientation, flat directional lighting and software rasterization remain
approximations; size, model transform, glyph metrics and count origin come from
the verified client assets and 1.19.2 ItemRenderer / ChestMenu implementations.
"""
import hashlib,io,json,math,zipfile
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
jar=ROOT/'.inputs/minecraft-1.19.2-client.jar'
raw=jar.read_bytes()
if len(raw)!=21644740 or hashlib.sha1(raw).hexdigest()!='055b30d860ead928cba3849ba920c88b6950b654':raise SystemExit('Client verification failed')
out=ROOT/'.inputs/composite-corrected'
if out.exists() and any(out.iterdir()):raise SystemExit(f'Preserving existing output: {out}')
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 def model(name):return json.loads(z.read('assets/minecraft/models/'+name+'.json'))
 def texture(name):return Image.open(io.BytesIO(z.read('assets/minecraft/textures/'+name+'.png'))).convert('RGBA')
 assert model('item/dirt')['parent']=='minecraft:block/dirt'
 assert model('block/dirt')['parent']=='minecraft:block/cube_all' and model('block/dirt')['textures']['all']=='minecraft:block/dirt'
 cube=model('block/cube')['elements'][0];assert cube['from']==[0,0,0] and cube['to']==[16,16,16]
 transform=model('block/block')['display']['gui'];assert transform['rotation']==[30,225,0] and transform['scale']==[.625]*3
 dirt=texture('block/dirt');atlas=texture('font/ascii')
 provider=next(p for p in json.loads(z.read('assets/minecraft/font/default.json'))['providers'] if p.get('file')=='minecraft:font/ascii.png')
assert dirt.size==(16,16) and atlas.size==(128,128) and provider['ascent']==7
chars=provider['chars'];glyphs=[]
for c in '64':
 row,col=next((r,s.index(c)) for r,s in enumerate(chars) if c in s)
 alpha=atlas.crop((col*8,row*8,col*8+8,row*8+8)).getchannel('A');glyphs.append((alpha,alpha.getbbox()[2]+1))
text_width=sum(advance for _,advance in glyphs);assert text_width==12
# ChestMenu: first slot (8,18), others 18 apart. ItemRenderer: item center
# x+8,y+8; 16-unit GUI scale; count x+17-font.width, y+9 with shadow.
# At 2x the item is 32x32, plus the possible one-logical-pixel text shadow.
SCALE=2; SIZE=16*SCALE
body=Image.new('RGBA',(SIZE,SIZE));draw=ImageDraw.Draw(body)
a,b=map(math.radians,transform['rotation'][:2])
def rotate(p):
 x,y,z=p;x,z=math.cos(b)*x+math.sin(b)*z,-math.sin(b)*x+math.cos(b)*z
 return x,math.cos(a)*y-math.sin(a)*z,math.sin(a)*y+math.cos(a)*z
def xy(p):return (SIZE/2+p[0]*SIZE,SIZE/2-p[1]*SIZE)
faces=[((-1,0,0),(0,1,0),(0,0,1)),((1,0,0),(0,1,0),(0,0,-1)),((0,-1,0),(1,0,0),(0,0,1)),((0,1,0),(1,0,0),(0,0,-1)),((0,0,-1),(-1,0,0),(0,1,0)),((0,0,1),(1,0,0),(0,1,0))]
visible=[]
for n,u,v in faces:
 depth=rotate(n)[2]
 if depth>0:visible.append((depth,n,u,v))
for _,normal,u,v in sorted(visible):
 def pos(s,t):return rotate(tuple((normal[i]*.5+u[i]*(s-.5)+v[i]*(t-.5))*.625 for i in range(3)))
 shade=.98 if normal[1]>0 else .8 if normal[0] else .65
 for iy in range(16):
  for ix in range(16):
   c=dirt.getpixel((ix,iy));color=tuple(round(v*shade) for v in c[:3])+(255,)
   pts=[xy(pos(s,t)) for s,t in [(ix/16,1-iy/16),((ix+1)/16,1-iy/16),((ix+1)/16,1-(iy+1)/16),(ix/16,1-(iy+1)/16)]]
   draw.polygon(pts,fill=color)
# Count is rendered in logical pixels so the text uses the same 2x scale.
count=Image.new('RGBA',(17,17));x=17-text_width;y=9
for alpha,advance in glyphs:
 for dx,dy,colour in [(1,1,(63,63,63,255)),(0,0,(255,255,255,255))]:
  ink=Image.new('RGBA',(8,8),colour);ink.putalpha(alpha);count.alpha_composite(ink,(x+dx,y+dy))
 x+=advance
icon=Image.new('RGBA',(34,34));icon.alpha_composite(body);icon.alpha_composite(count.resize((34,34),Image.Resampling.NEAREST))
out.mkdir(parents=True);icon.save(out/'stack.png')
metrics={'slot_origin':[8,18],'slot_spacing':18,'item_area':[16,16],'item_center':[8,8],'gui_scale':16,'model_scale':.625,'rotation':[30,225,0],'output_scale':2,'count':'64','count_width':text_width,'count_origin':[17-text_width,9],'shadow_offset':[1,1],'body_bbox_output':body.getchannel('A').getbbox()}
(out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics))
