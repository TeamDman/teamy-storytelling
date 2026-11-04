#!/usr/bin/env python3
"""Derive pixel-aligned presentation layers from the verified prior slice."""
import hashlib, io, json, zipfile
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'.inputs/conference-assets'; OUT=ROOT/'.inputs/composite-assets'
expected={'barrels.png':'f520d110eb899807a3c8a054bac55cf948c1b2c225cc984c0eb97337e13d243d','editor.png':'aa4fe6680bc1d8e9c169a3792d64d767ea1c10d2d2d5ef415e7cdfc5596b5fb4','manager.png':'e22440748a0faefdd0935d51e216ce047271662eea6b2607ed35d85016be561f','stack.png':'67a45659528e6a03b23b4ae1fdc5d9a9ebdf6b00a51c1e55c39e30d4a360d014'}
for name,want in expected.items():
 if hashlib.sha256((SRC/name).read_bytes()).hexdigest()!=want: raise SystemExit(f'Prior asset hash mismatch: {name}')
jar=ROOT/'.inputs/minecraft-1.19.2-client.jar'
if hashlib.sha1(jar.read_bytes()).hexdigest()!='055b30d860ead928cba3849ba920c88b6950b654':raise SystemExit('Wrong client')
if OUT.exists() and any(OUT.iterdir()):raise SystemExit(f'Preserving existing assets: {OUT}')
OUT.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(jar) as z:
 atlas=Image.open(io.BytesIO(z.read('assets/minecraft/textures/font/ascii.png'))).convert('RGBA')
 chars=next(p['chars'] for p in json.loads(z.read('assets/minecraft/font/default.json'))['providers'] if p.get('file')=='minecraft:font/ascii.png')
def measure(s):
 n=0
 for c in s:
  if c==' ':n+=4;continue
  row,col=next((r,v.index(c)) for r,v in enumerate(chars) if c in v)
  n+=atlas.crop((8*col,8*row,8*col+8,8*row+8)).getchannel('A').getbbox()[2]+1
 return n
def text(img,xy,s,color=(255,255,255,255),shadow=True):
 x,y=xy
 for c in s:
  if c==' ':x+=4;continue
  row,col=next((r,v.index(c)) for r,v in enumerate(chars) if c in v)
  alpha=atlas.crop((8*col,8*row,8*col+8,8*row+8)).getchannel('A')
  def put(pos,rgba):
   ink=Image.new('RGBA',(8,8),rgba);ink.putalpha(alpha);img.alpha_composite(ink,pos)
  if shadow:put((x+1,y+1),tuple(v//4 for v in color[:3])+(255,))
  put((x,y),color);x+=alpha.getbbox()[2]+1

def button(img,x,y,w,label):
 d=ImageDraw.Draw(img);d.rectangle((x,y,x+w-1,y+19),fill='#777777',outline='#151515');d.line((x+1,y+1,x+w-2,y+1),fill='#dddddd');d.line((x+1,y+18,x+w-2,y+18),fill='#252525');text(img,(x+(w-measure(label))//2,y+6),label)
# The manager's logical pixels are extracted from the verified 3x preview,
# stripped of its dark matte, and enlarged exactly 2x.
mgr=Image.open(SRC/'manager.png').convert('RGBA').crop((196,72,1084,648)).resize((296,192),Image.Resampling.NEAREST)
mgr.putdata([(0,0,0,0) if p[3]==150 else p for p in mgr.getdata()])
mgr.resize((592,384),Image.Resampling.NEAREST).save(OUT/'manager.png')
# EditorLayout at 296x240: textarea (4,10,288,200), footer y=215,
# buttons x=4/22/158 and widths 16/134/134. Reuse exact prior glyph pixels.
old=Image.open(SRC/'editor.png').convert('RGBA').resize((427,240),Image.Resampling.NEAREST)
editor=Image.new('RGBA',(296,240),'#272727');d=ImageDraw.Draw(editor);d.rectangle((4,10,291,209),fill='white');d.rectangle((5,11,290,208),fill='black');editor.alpha_composite(old.crop((17,14,180,50)),(8,14))
for x,w,label in [(4,16,'#'),(22,134,'Done'),(158,134,'Cancel')]:button(editor,x,215,w,label)
editor.resize((592,480),Image.Resampling.NEAREST).save(OUT/'editor.png')
# Crop only the 3-row container area; player inventory is intentionally omitted.
panels=Image.open(SRC/'barrels.png').convert('RGBA')
for name,x in [('a',80),('b',672)]:
 panels.crop((x,160,x+528,373)).resize((352,142),Image.Resampling.NEAREST).save(OUT/f'barrel-{name}.png')
 label=Image.new('RGBA',(12,12));text(label,(0,1),name,(85,255,85,255));label.resize((24,24),Image.Resampling.NEAREST).save(OUT/f'label-{name}.png')
Image.open(SRC/'stack.png').convert('RGBA').resize((32,32),Image.Resampling.NEAREST).save(OUT/'stack.png')
print('Derived pixel-aligned composite layers in',OUT)
