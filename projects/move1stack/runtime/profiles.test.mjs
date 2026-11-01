import test from 'node:test';import assert from 'node:assert/strict';import {applyRenderProfile} from './profiles.mjs';
const names=['glass','obsidian','beacon','polished_andesite'];
const original={textures:names.map(n=>({id:`assets/minecraft/textures/block/${n}.png`,mipmaps:true})),materials:names.map((n,i)=>({texture:`assets/minecraft/textures/block/${n}.png`,alphaTest:i<3?.1:0})),meshes:[{id:'unchanged-geometry',positions:[0,0,0]}]};
test('first render profile remains the exact original object',()=>assert.equal(applyRenderProfile(original),original));
test('source cutout profile changes only mipmaps on the three beacon cutout textures',()=>{
 const before=structuredClone(original),after=applyRenderProfile(original,'source-cutout');
 assert.deepEqual(before,original);const changed=[];
 for(let i=0;i<after.textures.length;i++){
  const a=after.textures[i],b=before.textures[i];
  if(a.mipmaps!==b.mipmaps){changed.push(a.id);assert.equal(a.mipmaps,false);a.mipmaps=b.mipmaps;}
 }
 assert.equal(changed.length,3);assert.ok(changed.every(x=>['glass.png','obsidian.png','beacon.png'].some(s=>x.endsWith('/'+s))));assert.deepEqual(before,after);
});
