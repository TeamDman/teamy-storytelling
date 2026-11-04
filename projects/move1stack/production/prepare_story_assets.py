#!/usr/bin/env python3
"""Build local, untracked GUI layers from the pinned vanilla client.

The atlas covers the ASCII labels used here; item icon and staging are illustrative.
"""
import hashlib, io, json, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
JAR=ROOT/'.inputs/minecraft-1.19.2-client.jar'
OUT=ROOT/'.inputs/story-assets'
CLIENT_SHA1='055b30d860ead928cba3849ba920c88b6950b654'
skin=ROOT/'.inputs/skin.png'
if hashlib.sha256(skin.read_bytes()).hexdigest()!='dc6d27c115e71009ced5a2bc41a24e918b45edf5a584e639ec56b832126d2635':
    raise SystemExit('Player skin does not match the supplied legacy skin')
data=JAR.read_bytes()
if len(data)!=21644740 or hashlib.sha1(data).hexdigest()!=CLIENT_SHA1:
    raise SystemExit('Minecraft client does not match the pinned 1.19.2 metadata')
with zipfile.ZipFile(io.BytesIO(data)) as z:
    font=Image.open(io.BytesIO(z.read('assets/minecraft/textures/font/ascii.png'))).convert('RGBA')
    spec=json.loads(z.read('assets/minecraft/font/default.json'))
    gui=Image.open(io.BytesIO(z.read('assets/minecraft/textures/gui/container/generic_54.png'))).convert('RGBA')
provider=next(p for p in spec['providers'] if p.get('file')=='minecraft:font/ascii.png')
chars=provider['chars']
assert font.size==(128,128) and gui.size==(256,256) and provider['ascent']==7

def text(img, xy, value, color):
    x,y=xy
    for c in value:
        if c==' ': x+=4; continue
        row,col=next((r,s.index(c)) for r,s in enumerate(chars) if c in s)
        glyph=font.crop((col*8,row*8,col*8+8,row*8+8))
        alpha=glyph.getchannel('A')
        box=alpha.getbbox()
        if not box: raise ValueError(f'empty glyph {c!r}')
        tinted=Image.new('RGBA',(8,8),color); tinted.putalpha(alpha)
        img.alpha_composite(tinted,(x,y))
        x+=box[2]+1
    return x

def panel(full):
    # ContainerScreen draws the top 3 rows and bottom inventory from generic_54.
    p=Image.new('RGBA',(176,166)); p.paste(gui.crop((0,0,176,71)),(0,0)); p.paste(gui.crop((0,126,176,222)),(0,71))
    text(p,(8,6),'Barrel',(64,64,64,255)); text(p,(8,72),'Inventory',(64,64,64,255))
    if full:
        # Existing project reconstruction of a dirt block item, not an extracted item sprite.
        from importlib.machinery import SourceFileLoader
        module=SourceFileLoader('slice08',str(ROOT/'conference-preview/slice08.py')).load_module()
        p.alpha_composite(module.dirt_icon(),(8,18))
        text(p,(14,27),'64',(63,63,63,255)); text(p,(13,26),'64',(255,255,255,255))
    return p

OUT.mkdir(parents=True,exist_ok=True)
for full,name in [(False,'empty.png'),(True,'full.png')]:
    path=OUT/name
    if path.exists(): raise SystemExit(f'Refusing to replace {path}')
    p=panel(full).resize((528,498),Image.Resampling.NEAREST)
    layer=Image.new('RGBA',(1280,720),(0,0,0,112)); layer.alpha_composite(p,(376,111)); layer.save(path)
# Like-for-like output-resolution type proof against the prior DejaVu approximation.
proof=Image.new('RGBA',(1280,720),(32,38,45,255)); d=ImageDraw.Draw(proof)
d.text((44,35),'Earlier approximation',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24),fill='white')
d.text((674,35),'Minecraft 1.19.2 bitmap',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24),fill='white')
old=panel(False); d=ImageDraw.Draw(old); d.rectangle((8,6,100,14),fill='#c6c6c6'); d.rectangle((8,72,100,80),fill='#c6c6c6'); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',8); d.text((8,5),'Barrel',font=f,fill='#404040'); d.text((8,71),'Inventory',font=f,fill='#404040')
proof.alpha_composite(old.resize((528,498),Image.Resampling.NEAREST),(44,111)); proof.alpha_composite(panel(False).resize((528,498),Image.Resampling.NEAREST),(674,111)); proof.convert('RGB').save(OUT/'font-comparison.png')
print('Generated verified vanilla GUI layers and output-resolution font comparison in',OUT)
