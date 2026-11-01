import * as T from 'three';
import {loadScene} from './scene.mjs';
import {applyRenderProfile} from './profiles.mjs';
export async function createWorld({profile='first'}={}){
 const base=new URL('../production/',import.meta.url);if(!base.pathname.endsWith('/'))base.pathname+='/';
 const baked=await fetch(new URL('../baked-scene.json',import.meta.url)).then(r=>r.json());
 const source=await fetch(new URL('../ground-truth/scene-manifest.json',import.meta.url)).then(r=>r.json());
 const world=await loadScene(applyRenderProfile(baked,profile),base);const {scene,camera}=world;
 const beam=new T.Group();beam.position.set(-.5,-1,-.5);scene.add(beam);
 const texture=await new T.TextureLoader().loadAsync(new URL('../ground-truth/assets/minecraft/textures/entity/beacon_beam.png',import.meta.url).href);
 texture.wrapS=texture.wrapT=T.RepeatWrapping;texture.minFilter=texture.magFilter=T.NearestFilter;texture.generateMipmaps=false;
 const segments=[];
 function segment(y,h,color){
  const core=new T.Group(),halo=new T.Group();beam.add(core,halo);
  function quads(points,group,opacity,speed){
   const tex=texture.clone();tex.needsUpdate=true;
   const mat=new T.MeshBasicMaterial({map:tex,color,transparent:opacity<1,opacity,blending:opacity===1?T.NoBlending:T.NormalBlending,depthWrite:opacity===1,side:T.DoubleSide,toneMapped:false});
   const p=[],uv=[];
   for(let i=0;i<4;i++){
    const a=points[i],b=points[(i+1)%4];
    const pp=[[a[0],y+h,a[1]],[a[0],y,a[1]],[b[0],y,b[1]],[b[0],y+h,b[1]]];const u=[[1,h*speed],[1,0],[0,0],[0,h*speed]];
    for(const j of [0,1,2,0,2,3]){p.push(...pp[j]);uv.push(...u[j]);}
   }
   const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));
   const m=new T.Mesh(g,mat);m.renderOrder=opacity===1?1:5;group.add(m);return tex;
  }
  const ct=quads([[0,.2],[.2,0],[0,-.2],[-.2,0]],core,1,2.5);
  const ht=quads([[-.25,-.25],[.25,-.25],[.25,.25],[-.25,.25]],halo,.125,1);
  segments.push({core,ct,ht});
 }
 segment(0,1,0xffffff);segment(1,1024,0x80c71f);
 const outline=new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(3.006,2.006,1.006)),new T.LineBasicMaterial({color:0xffffff,toneMapped:false}));outline.position.set(1.5,2,.5);scene.add(outline);
 // Source outline has colored axis edges at the lower origin corner.
 for(const [end,color] of [[[3,1,0],0xff7070],[[0,3,0],0x70ff70],[[0,1,1],0x7070ff]]){
  const g=new T.BufferGeometry().setFromPoints([new T.Vector3(0,1,0),new T.Vector3(...end)]);scene.add(new T.Line(g,new T.LineBasicMaterial({color,toneMapped:false})));
 }
 // Noon celestial geometry stays beyond the downward-looking matched views.
 const sunTexture=await new T.TextureLoader().loadAsync(new URL('../ground-truth/assets/minecraft/textures/environment/sun.png',import.meta.url).href);
 const sun=new T.Mesh(new T.PlaneGeometry(60,60),new T.MeshBasicMaterial({map:sunTexture,transparent:true,blending:T.AdditiveBlending,depthWrite:false,side:T.DoubleSide}));sun.rotation.x=Math.PI/2;sun.position.y=100;scene.add(sun);
 // No visible clouds or moon were observed; clouds default OFF. No invented
 // solar/cloud objects are placed in the camera path to decorate the capture.
 function pose(index){const p=source.cameras.reference_optical_poses[index];camera.position.set(p.local_eye.x,p.local_eye.y,p.local_eye.z);camera.lookAt(camera.position.clone().add(new T.Vector3(...p.forward)));beam.visible=p.beam_visible;}
 function update(t,{figure=null,angle=null,beamVisible=true}={}){
  world.update(t);beam.visible=beamVisible;
  if(figure!==null)pose(figure);
  else {const a=angle??t/24*Math.PI*2;camera.position.set(1+7*Math.cos(a),5.527402276237758,7*Math.sin(a));camera.lookAt(camera.position.clone().add(new T.Vector3(-Math.cos(a)*.8137334690964149,-.5812381966735445,-Math.sin(a)*.8137334690964149)));}
  const f=((t*20)%40+40)%40;const sign=-f;const v=-1+((sign*.2-Math.floor(sign*.1))%1+1)%1;
  for(const s of segments){s.core.rotation.y=(f*2.25-45)*Math.PI/180;s.ct.offset.y=v;s.ht.offset.y=v;}
 }
 update(0);return {...world,update,pose,beam,source};
}
