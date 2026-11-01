// First-render settings remain the default. Candidate correction is grounded in
// faa.java CUTOUT -> BLOCK_SHEET and ezz.java ai=(atlas,false,false), in contrast
// to BLOCK_SHEET_MIPPED ah=(atlas,false,true).
export function applyRenderProfile(baked,profile='first'){
 if(profile==='first')return baked;
 if(profile!=='source-cutout')throw Error(`Unknown profile ${profile}`);
 const copy=structuredClone(baked);
 const cutoutTextures=new Set(copy.materials.filter(m=>m.alphaTest>0).map(m=>m.texture));
 for(const texture of copy.textures)if(cutoutTextures.has(texture.id))texture.mipmaps=false;
 return copy;
}
