import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
const available=['../baked-scene.json','../ground-truth/scene-manifest.json','../reference-evidence/reference/preview-manifest.json'].every(p=>fs.existsSync(new URL(p,import.meta.url)));
const scene=available?JSON.parse(fs.readFileSync(new URL('../baked-scene.json',import.meta.url))):null;
const manifest=available?JSON.parse(fs.readFileSync(new URL('../ground-truth/scene-manifest.json',import.meta.url))):null;
const captures=available?JSON.parse(fs.readFileSync(new URL('../reference-evidence/reference/preview-manifest.json',import.meta.url))):null;
test('both solid barrel top textures face north after blockstate rotation',{skip:!available},()=>{
 const faces=scene.meshes.filter(m=>m.material.includes('/barrel_top.png'));assert.equal(faces.length,2);
 for(const m of faces){assert.ok(m.id.endsWith('/up'));for(let i=2;i<m.positions.length;i+=3)assert.ok(Math.abs(m.positions[i])<1e-12);}
});
test('all 20 manifest blocks are represented, including submerged support base',{skip:!available},()=>{
 for(let i=0;i<20;i++){const faces=scene.meshes.filter(m=>m.id.startsWith(i+'-'));assert.ok(faces.length>=6,`missing block ${i}`)}
 const beacon=scene.meshes.filter(m=>m.id.startsWith('3-beacon'));assert.equal(beacon.length,18);
 assert.equal(new Set(beacon.map(m=>m.material)).size,3);
 for(const m of scene.meshes.filter(m=>m.id.startsWith('14-polished_andesite'))){for(let i=1;i<m.positions.length;i+=3)assert.ok(m.positions[i]>=1&&m.positions[i]<=2);}
});
test('exact optical positions preserve original manifest without adding eye height',{skip:!available},()=>{
 for(let i=0;i<8;i++){
  const p=manifest.cameras.reference_optical_poses[i];const c=captures.captures[i].camera;
  assert.equal(p.local_eye.x,c.x);assert.equal(p.local_eye.y,c.y+60);assert.equal(p.local_eye.z,c.z);
  assert.ok(Math.abs(Math.hypot(...p.forward)-1)<1e-12);
 }
 assert.deepEqual(manifest.cameras.reference_optical_poses.map(x=>x.beam_visible),[true,true,false,true,true,true,true,true]);
});
test('cutout and translucent beacon layers retain distinct depth states',{skip:!available},()=>{
 const glass=scene.materials.find(x=>x.id.includes('/glass.png'));const lime=scene.materials.find(x=>x.id.includes('/lime_stained_glass.png'));
 assert.equal(glass.alphaTest,.1);assert.equal(glass.transparent,false);assert.equal(glass.depthWrite,true);
 assert.equal(lime.transparent,true);assert.equal(lime.depthWrite,true);assert.equal(lime.blending,'normal');
});
