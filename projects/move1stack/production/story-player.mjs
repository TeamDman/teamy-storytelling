import * as T from 'three';

// Classic 64x32 legacy skin. The body and pose are a staged approximation;
// mirrored side/back UVs have not been checked against an in-game capture.
export async function createPlayer(scene) {
  const texture=await new T.TextureLoader().loadAsync(new URL('../.inputs/skin.png',import.meta.url).href);
  if(texture.image.width!==64 || texture.image.height!==32) throw Error('Expected legacy 64x32 skin');
  texture.magFilter=texture.minFilter=T.NearestFilter; texture.generateMipmaps=false;
  texture.encoding=T.sRGBEncoding;
  const material=new T.MeshBasicMaterial({map:texture,toneMapped:false});
  const root=new T.Group(); root.position.set(1.8,1,-.42); root.scale.setScalar(.05625); root.rotation.y=-50*Math.PI/180; scene.add(root);
  function box(w,h,d,a,b,mirror=false) {
    const geometry=new T.BoxGeometry(w,h,d);
    const rects=[[a+d+w,b+d,a+2*d+w,b+d+h],[a,b+d,a+d,b+d+h],[a+d,b,a+d+w,b+d],[a+d+w,b,a+d+2*w,b+d],[a+2*d+w,b+d,a+2*d+2*w,b+d+h],[a+d,b+d,a+d+w,b+d+h]];
    if(mirror) [rects[0],rects[1]]=[rects[1],rects[0]];
    const uv=geometry.attributes.uv;
    rects.forEach(([u0,v0,u1,v1],i)=>{
      if(mirror) [u0,u1]=[u1,u0];
      [[u0,v0],[u1,v0],[u0,v1],[u1,v1]].forEach(([u,v],j)=>uv.setXY(i*4+j,u/64,1-v/32));
    }); uv.needsUpdate=true;
    return new T.Mesh(geometry,material);
  }
  function part(w,h,d,a,b,x,y,mirror=false) {const mesh=box(w,h,d,a,b,mirror);mesh.position.set(x,y,0);root.add(mesh);return mesh;}
  const head=part(8,8,8,0,0,0,28); part(8,12,4,16,16,0,18); part(4,12,4,0,16,-2,6); part(4,12,4,0,16,2,6,true);
  const arm=new T.Group();arm.position.set(-6,24,0);root.add(arm);const right=box(4,12,4,40,16);right.position.y=-6;arm.add(right);
  part(4,12,4,40,16,6,18,true);
  return {root,head,arm,update(t){const phase=Math.max(0,1-Math.abs(t-2.05)/.48);arm.rotation.x=-1.05*phase;}};
}
