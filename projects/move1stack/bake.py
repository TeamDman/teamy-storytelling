"""Bake the supplied Minecraft JSON model hierarchy into the restored renderer schema."""
import json, math, hashlib
from pathlib import Path
ROOT=Path(__file__).parent
INPUT=ROOT/'ground-truth'
manifest=json.loads((INPUT/'scene-manifest.json').read_text())
textures={}; materials={}; meshes=[]
def model(name):
 ns,_,path=name.partition(':')
 if not path: ns,path='minecraft',ns
 d=json.loads((INPUT/f'assets/{ns}/models/{path}.json').read_text())
 p=model(d['parent']) if d.get('parent') else {}
 return {**p,**d,'textures':{**p.get('textures',{}),**d.get('textures',{})}}
def texid(name):
 ns,_,path=name.partition(':')
 if not path: ns,path='minecraft',ns
 return f'assets/{ns}/textures/{path}.png'
def getmat(path,trans=False,cut=False):
 key=path+(':trans' if trans else ':cut' if cut else '')
 if key not in materials:
  t={'id':path,'url':'../ground-truth/'+path,'flipY':True,'srgb':False,'wrapS':'repeat','wrapT':'repeat','mipmaps':True}
  meta=INPUT/(path+'.mcmeta')
  if meta.exists():
   a=json.loads(meta.read_text())['animation']
   from PIL import Image
   w,h=Image.open(INPUT/path).size
   t.update(frameWidth=w,frameHeight=w,animation={'frametime':a.get('frametime',1),'frames':a.get('frames',list(range(h//w))),'ticksPerSecond':20,'interpolate':a.get('interpolate',False)})
  textures[path]=t
  materials[key]={'id':key,'texture':path,'transparent':trans,'depthTest':True,'depthWrite':True,'opacity':1,'alphaTest':.1 if cut else 0,'side':'front','blending':'normal' if trans else 'none','color':0xffffff,'vertexColors':True}
 return key
def rotate(v,rx,ry):
 x,y,z=v;c=math.cos(rx);s=math.sin(rx);y,z=c*y-s*z,s*y+c*z;c=math.cos(ry);s=math.sin(ry);return [c*x+s*z,y,-s*x+c*z]
def bake(name,position,modelname,rx=0,ry=0):
 d=model(modelname); tx=d['textures']
 def resolve(t):
  while t.startswith('#'):t=tx[t[1:]]
  return texid(t)
 for j,e in enumerate(d['elements']):
  a,b=e['from'],e['to'];x,y,z=a;X,Y,Z=b
  vertices={'down':[[x,y,Z],[x,y,z],[X,y,z],[X,y,Z]],'up':[[x,Y,z],[x,Y,Z],[X,Y,Z],[X,Y,z]],'north':[[X,Y,z],[X,y,z],[x,y,z],[x,Y,z]],'south':[[x,Y,Z],[x,y,Z],[X,y,Z],[X,Y,Z]],'west':[[x,Y,z],[x,y,z],[x,y,Z],[x,Y,Z]],'east':[[X,Y,Z],[X,y,Z],[X,y,z],[X,Y,z]]}
  normals={'down':[0,-1,0],'up':[0,1,0],'north':[0,0,-1],'south':[0,0,1],'west':[-1,0,0],'east':[1,0,0]}
  default={'down':[x,16-Z,X,16-z],'up':[x,z,X,Z],'north':[16-X,16-Y,16-x,16-y],'south':[x,16-Y,X,16-y],'west':[z,16-Y,Z,16-y],'east':[16-Z,16-Y,16-z,16-y]}
  for face,f in e['faces'].items():
   n=rotate(normals[face],rx,ry);brightness=.5 if n[1]<-.5 else 1 if n[1]>.5 else .6 if abs(n[0])>.5 else .8
   path=resolve(f['texture']);uv=f.get('uv',default[face]);u,v,U,V=uv
   coords=[[u/16,1-v/16],[u/16,1-V/16],[U/16,1-V/16],[U/16,1-v/16]]
   # Vanilla face vertex order: top right, bottom right, bottom left, top left.
   if face in ['up','down']: coords=[[u/16,1-v/16],[u/16,1-V/16],[U/16,1-V/16],[U/16,1-v/16]]
   rot=f.get('rotation',0)//90;coords=coords[rot:]+coords[:rot]
   pts=[]
   for vtx in vertices[face]:
    p=rotate([vtx[k]/16-.5 for k in range(3)],rx,ry);pts.append([p[k]+position[k]+.5 for k in range(3)])
   idx=[0,1,2,0,2,3]
   meshes.append({'id':f'{name}/{j}/{face}','material':getmat(path,'lime_stained_glass' in name,'beacon' in name),'positions':[v for i in idx for v in pts[i]],'uvs':[v for i in idx for v in coords[i]],'colors':[brightness]*18,'renderOrder':10 if 'lime_stained_glass' in name else 0})
for i,b in enumerate(manifest['blocks']):
 id=b['id'];name=id.split(':')[1];rx=-math.pi/2 if name in ['test_barrel','stone_button'] else 0
 mn='minecraft:block/'+({'test_barrel':'barrel','structure_block':'structure_block_load'}.get(name,name))
 if name=='manager':
  # The SFM datagen uses this exact vanilla cube parent and these supplied textures.
  dest=INPUT/'assets/sfm/models/block/manager.json';dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text(json.dumps({'parent':'minecraft:block/cube_bottom_top','textures':{'top':'sfm:block/manager_top','bottom':'sfm:block/manager_bot','side':'sfm:block/manager_side'}}))
  mn='sfm:block/manager'
 bake(f'{i}-{name}',b['position'],mn,rx)
def plane(name,x,z,X,Z,path,color):
 mat=getmat(path); p=[[x,0,z],[x,0,Z],[X,0,Z],[X,0,z]];uv=[[x,-z],[x,-Z],[X,-Z],[X,-z]];idx=[0,1,2,0,2,3]
 meshes.append({'id':name,'material':mat,'positions':[v for i in idx for v in p[i]],'uvs':[v for i in idx for v in uv[i]],'colors':color*6,'renderOrder':0})
from PIL import Image
# Vanilla-style position-seeded rotation breaks identical tile stripes. Exact
# historical chunk/model random stream is not available; this seeded field is
# disclosed as a terrain sampling approximation.
base=Image.open(INPUT/'assets/minecraft/textures/block/grass_block_top.png').convert('RGBA')
field=Image.new('RGBA',(4096,4096))
variants=[base.rotate(-90*k) for k in range(4)]
for z in range(-128,128):
 for x in range(-128,128):
  seed=((x*3129871)^(z*116129781)^-61)&((1<<64)-1)
  seed=(seed*seed*42317861+seed*11)&((1<<64)-1)
  field.paste(variants[(seed>>16)%4],((x+128)*16,(z+128)*16))
field.save(ROOT/'grass-field.png')
grass='assets/minecraft/textures/block/grass_block_top.png';tint=[120/255,195/255,74/255] # Observed clear-ground color calibration, not recovered biome settings.
for n,(x,z,X,Z) in enumerate([(-128,-128,-2,128),(6,-128,128,128),(-2,-128,6,-3),(-2,4,6,128)]):plane('grass'+str(n),x,z,X,Z,grass,tint)
for x in range(-2,6):
 for z in range(-3,4):
  if (x,z)==(-1,-1):continue
  plane(f'dirt{x},{z}',x,z,x+1,z+1,'assets/minecraft/textures/block/dirt.png',[1,1,1])
# Terrain layers around the exposed beacon hole; other buried layers are occluded.
for x,z,face in [(-2,-1,'east'),(0,-1,'west'),(-1,-2,'south'),(-1,0,'north')]:
 start=len(meshes);bake(f'hole{x},{z}',[x,-1,z],'minecraft:block/dirt')
 meshes[start:]=[m for m in meshes[start:] if m['id'].endswith('/'+face)]
eye=manifest['cameras']['reference_optical_poses'][0];p=list(eye['local_eye'].values());f=eye['forward']
for m in meshes:
 if m['id'].startswith('grass'):
  m['uvs']=[(v/256+.5) if k%2==0 else (v/256+.5) for k,v in enumerate(m['uvs'])]
textures[grass]['url']='../grass-field.png'
out={'schemaVersion':1,'viewport':{'width':1280,'height':720},'textures':list(textures.values()),'materials':list(materials.values()),'meshes':meshes,'camera':{'position':p,'target':[a+b for a,b in zip(p,f)],'up':[0,1,0],'fovYDegrees':70,'near':.05,'far':2048}}
(ROOT/'baked-scene.json').write_text(json.dumps(out,separators=(',',':')))
print(f'Baked {len(meshes)} faces from 20 fixture blocks and terrain, {len(textures)} textures')
