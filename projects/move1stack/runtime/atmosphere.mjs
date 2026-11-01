import * as T from 'three';
// Optional FAST cloud layer from supplied Overworld constants. Matched captures
// default OFF; FANCY two-pass extruded clouds are intentionally not claimed.
export async function addCloudLayer(scene,{enabled=false}={}){
 if(!enabled)return {update(){},dispose(){}};
 const map=await new T.TextureLoader().loadAsync(new URL('../ground-truth/assets/minecraft/textures/environment/clouds.png',import.meta.url).href);
 map.wrapS=map.wrapT=T.RepeatWrapping;map.minFilter=map.magFilter=T.NearestFilter;map.generateMipmaps=false;
 const geometry=new T.PlaneGeometry(6144,6144);geometry.rotateX(-Math.PI/2);
 const uv=geometry.getAttribute('uv');for(let i=0;i<uv.count;i++)uv.setXY(i,uv.getX(i)*2,uv.getY(i)*2);
 const material=new T.MeshBasicMaterial({map,transparent:true,opacity:.8,side:T.DoubleSide,depthTest:true,depthWrite:true,toneMapped:false});
 const cloud=new T.Mesh(geometry,material);cloud.position.y=192-(-60);scene.add(cloud);
 return {update(seconds){map.offset.x=seconds*.6/3072},dispose(){scene.remove(cloud);geometry.dispose();material.dispose();map.dispose()}};
}
// Noon's moon is below the ground. Phase defaults to 0 for optional alternate
// sky exploration; capture-time moon phase is unknown and never inferred.
export async function addNoonMoon(scene,{phase=0}={}){
 if(!Number.isInteger(phase)||phase<0||phase>7)throw Error('Moon phase must be 0..7');
 const map=await new T.TextureLoader().loadAsync(new URL('../ground-truth/assets/minecraft/textures/environment/moon_phases.png',import.meta.url).href);
 map.magFilter=map.minFilter=T.NearestFilter;map.repeat.set(.25,.5);map.offset.set((phase%4)/4,1-(Math.floor(phase/4)+1)/2);
 const moon=new T.Mesh(new T.PlaneGeometry(40,40),new T.MeshBasicMaterial({map,transparent:true,blending:T.AdditiveBlending,depthWrite:false,side:T.DoubleSide,toneMapped:false}));moon.rotation.x=Math.PI/2;moon.position.y=-100;scene.add(moon);return moon;
}
