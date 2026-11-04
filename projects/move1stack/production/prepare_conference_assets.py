#!/usr/bin/env python3
"""Build local conference layers from verified 1.19.2 and SFM sources."""
import hashlib, io, json, math, re, textwrap, zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.inputs/conference-assets'
expected={
 ROOT/'.inputs/minecraft-1.19.2-client.jar':('sha1','055b30d860ead928cba3849ba920c88b6950b654'),
 ROOT/'.inputs/skin.png':('sha256','dc6d27c115e71009ced5a2bc41a24e918b45edf5a584e639ec56b832126d2635'),
 ROOT/'.inputs/sfm-gui/manager.png':('sha256','b6945789f1b663261a0c3bc6f922052a41f827cbd966e5014cadbc188eb7dea0'),
 ROOT/'.inputs/sfm-gui/disk.png':('sha256','049bca9a9be439beca5979e8af504bb3c822eb06dbf390927de9f490ce0514e1'),
 ROOT/'ground-truth/evidence/sfm/src/gametest/java/ca/teamdman/sfm/gametest/tests/general/Move1StackDirectGameTest.java':('sha256','750a09bcc1f910c2ed80954141d1ba77f39f1f52679c8cce98c818562c0aae01'),
}
for path,(algorithm,want) in expected.items():
 if hashlib.new(algorithm,path.read_bytes()).hexdigest()!=want: raise SystemExit(f'Input hash mismatch: {path}')
if (ROOT/'.inputs/minecraft-1.19.2-client.jar').stat().st_size!=21644740: raise SystemExit('Incorrect client size')
if OUT.exists() and any(OUT.iterdir()): raise SystemExit(f'Preserving existing assets: {OUT}')
OUT.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ROOT/'.inputs/minecraft-1.19.2-client.jar') as z:
 def image(name): return Image.open(io.BytesIO(z.read('assets/minecraft/textures/'+name))).convert('RGBA')
 def model(name): return json.loads(z.read('assets/minecraft/models/'+name+'.json'))
 atlas=image('font/ascii.png'); gui=image('gui/container/generic_54.png'); dirt=image('block/dirt.png')
 provider=next(p for p in json.loads(z.read('assets/minecraft/font/default.json'))['providers'] if p.get('file')=='minecraft:font/ascii.png')
 assert model('item/dirt')['parent']=='minecraft:block/dirt'
 assert model('block/dirt')['textures']['all']=='minecraft:block/dirt'
 assert model('block/dirt')['parent']=='minecraft:block/cube_all'
 assert model('block/cube')['elements'][0]['from']==[0,0,0] and model('block/cube')['elements'][0]['to']==[16,16,16]
 transform=model('block/block')['display']['gui']; assert transform['rotation']==[30,225,0] and transform['scale']==[.625]*3
chars=provider['chars']
def width(value):
 n=0
 for c in value:
  if c==' ': n+=4; continue
  row,col=next((r,s.index(c)) for r,s in enumerate(chars) if c in s)
  box=atlas.crop((col*8,row*8,col*8+8,row*8+8)).getchannel('A').getbbox()
  if not box: raise ValueError(c)
  n+=box[2]+1
 return n

def text(img,xy,value,color,shadow=False,bold=False):
 x,y=xy
 for c in value:
  if c==' ': x+=4; continue
  row,col=next((r,s.index(c)) for r,s in enumerate(chars) if c in s)
  alpha=atlas.crop((col*8,row*8,col*8+8,row*8+8)).getchannel('A')
  def glyph(xx,yy,rgba):
   layer=Image.new('RGBA',(8,8),rgba);layer.putalpha(alpha);img.alpha_composite(layer,(xx,yy))
  if shadow: glyph(x+1,y+1,tuple(v//4 for v in color[:3])+(255,))
  glyph(x,y,color)
  if bold: glyph(x+1,y,color)
  x+=alpha.getbbox()[2]+1+(1 if bold else 0)
 return x

def button(img,x,y,w,h,label):
 d=ImageDraw.Draw(img); d.rectangle((x,y,x+w-1,y+h-1),fill='#777777',outline='#151515');d.line((x+1,y+1,x+w-2,y+1),fill='#dddddd');d.line((x+1,y+h-2,x+w-2,y+h-2),fill='#252525')
 text(img,(x+(w-width(label))//2,y+(h-8)//2),label,(255,255,255,255),shadow=True)

manager=Image.new('RGBA',(296,192),(0,0,0,0)); manager.alpha_composite(Image.open(ROOT/'.inputs/sfm-gui/manager.png').convert('RGBA').crop((0,0,176,166)),(120,0));manager.alpha_composite(Image.open(ROOT/'.inputs/sfm-gui/disk.png').convert('RGBA'),(135,47))
for y,s in [(6,'Manager'),(20,'State: running'),(72,'Inventory')]:text(manager,(128,y),s,(64,64,64,255))
for x,y,w,h,label in [(0,16,120,16,'Paste from clipboard'),(0,66,120,16,'Edit'),(0,82,120,16,'View examples'),(0,112,120,16,'Discord'),(0,128,120,16,'Copy to clipboard'),(0,144,120,16,'View logs'),(0,160,120,16,'Rebuild cable network'),(0,176,120,16,'View server config'),(240,10,50,12,'Reset')]: button(manager,x,y,w,h,label)
layer=Image.new('RGBA',(1280,720),(0,0,0,150));layer.alpha_composite(manager.resize((888,576),Image.Resampling.NEAREST),(196,72));layer.save(OUT/'manager.png')

source=(ROOT/'ground-truth/evidence/sfm/src/gametest/java/ca/teamdman/sfm/gametest/tests/general/Move1StackDirectGameTest.java').read_text()
match=re.search(r'manager\.setProgram\("""\s*\n(.*?)"""\.stripTrailing\(\)\.stripIndent\(\)\)',source,re.S)
if not match or textwrap.dedent(match.group(1)).strip().splitlines()!=['EVERY 20 TICKS DO','    INPUT FROM a','    OUTPUT TO b','END']:raise SystemExit('Unexpected test program')
editor=Image.new('RGBA',(427,240),'#272727');d=ImageDraw.Draw(editor);d.rectangle((13,10,412,209),fill='white');d.rectangle((14,11,411,208),fill='black')
lines=[[('EVERY','#5555ff',1),(' ','#ffffff',0),('20','#55ffff',0),(' ','#ffffff',0),('TICKS','#ffaa00',0),(' ','#ffffff',0),('DO','#5555ff',1)], [('    ','#ffffff',0),('INPUT','#ff55ff',0),(' ','#ffffff',0),('FROM','#ff55ff',0),(' ','#ffffff',0),('a','#55ff55',0)], [('    ','#ffffff',0),('OUTPUT','#ff55ff',0),(' ','#ffffff',0),('TO','#ff55ff',0),(' ','#ffffff',0),('b','#55ff55',0)], [('END','#5555ff',1)]]
for i,line in enumerate(lines):
 x=17
 for word,color,bold in line: x=text(editor,(x,14+9*i),word,tuple(bytes.fromhex(color[1:]))+(255,),shadow=True,bold=bold)
for x,w,label in [(13,16,'#'),(61,200,'Done'),(311,100,'Cancel')]:button(editor,x,215,w,20,label)
editor.resize((1281,720),Image.Resampling.NEAREST).crop((0,0,1280,720)).save(OUT/'editor.png')

# Exact vanilla texture and inherited GUI model transform. Faces are rasterized
# at 3x GUI scale; flat directional shading approximates the game's lighting.
icon=Image.new('RGBA',(48,48)); draw=ImageDraw.Draw(icon)
a,b=map(math.radians,(30,225))
def rotate(p):
 x,y,z=p; x,z=math.cos(b)*x+math.sin(b)*z,-math.sin(b)*x+math.cos(b)*z
 return (x,math.cos(a)*y-math.sin(a)*z,math.sin(a)*y+math.cos(a)*z)
def xy(p):return (24+p[0]*30,24-p[1]*30)
faces=[((-1,0,0),(0,1,0),(0,0,1)),((1,0,0),(0,1,0),(0,0,-1)),((0,-1,0),(1,0,0),(0,0,1)),((0,1,0),(1,0,0),(0,0,-1)),((0,0,-1),(-1,0,0),(0,1,0)),((0,0,1),(1,0,0),(0,1,0))]
visible=[]
for normal,u,v in faces:
 n=rotate(normal)
 if n[2]>0:visible.append((n[2],normal,u,v))
for _,normal,u,v in sorted(visible):
 def pos(s,t):return rotate(tuple((normal[i]*.5+u[i]*(s-.5)+v[i]*(t-.5))*.625 for i in range(3)))
 shade=.98 if normal[1]>0 else .8 if normal[0] else .65
 for iy in range(16):
  for ix in range(16):
   c=dirt.getpixel((ix,iy)); color=tuple(round(ch*shade) for ch in c[:3])+(255,)
   points=[xy(pos(s,t)) for s,t in [(ix/16,1-iy/16),((ix+1)/16,1-iy/16),((ix+1)/16,1-(iy+1)/16),(ix/16,1-(iy+1)/16)]]
   draw.polygon(points,fill=color)
# Count is the same Minecraft bitmap atlas, drawn at 1x then nearest enlarged.
count=Image.new('RGBA',(16,16));text(count,(2,7),'64',(255,255,255,255),shadow=True)
icon.alpha_composite(count.resize((48,48),Image.Resampling.NEAREST));icon.save(OUT/'stack.png')
# Panels: a and b are presentation labels, not part of a simultaneous in-game view.
panel=Image.new('RGBA',(176,166));panel.paste(gui.crop((0,0,176,71)),(0,0));panel.paste(gui.crop((0,126,176,222)),(0,71));text(panel,(8,6),'Barrel',(64,64,64,255));text(panel,(8,72),'Inventory',(64,64,64,255))
pair=Image.new('RGBA',(1280,720),(0,0,0,170));
for x,label in [(80,'a'),(672,'b')]:
 pair.alpha_composite(panel.resize((528,498),Image.Resampling.NEAREST),(x,160));labelimg=Image.new('RGBA',(16,12));text(labelimg,(0,0),label,(85,255,85,255),shadow=True);pair.alpha_composite(labelimg.resize((48,36),Image.Resampling.NEAREST),(x,120))
pair.save(OUT/'barrels.png')
print('Built verified conference layers in',OUT)
