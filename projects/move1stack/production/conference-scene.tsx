import {Img,makeScene2D} from '@motion-canvas/2d';
import {createSignal,linear} from '@motion-canvas/core';
import {Three} from './Three';
import {createWorld} from '../runtime/world.mjs';
import {createPlayer} from './story-player.mjs';
import {transferAt} from '../runtime/conference-timeline.mjs';
const world=await createWorld({profile:'source-cutout'});
const player=await createPlayer(world.scene);
const asset=(name:string)=>new URL(`../.inputs/conference-assets/${name}`,import.meta.url).href;
export default makeScene2D(function*(view){
 const time=createSignal(0);
 view.add(new Three({size:[1280,720],scene:world.scene,camera:world.camera,background:'#b5d0ff',onRender(renderer,scene,camera){
  const t=time();world.update(t);player.update(t);const a=-.8+t*.025;
  camera.position.set(1.5+6*Math.sin(a),3.5,-6*Math.cos(a));camera.lookAt(1.35,1.7,-.05);camera.fov=58;camera.updateProjectionMatrix();
  renderer.setClearColor('#b5d0ff');renderer.render(scene,camera);
 }}));
 view.add(new Img({src:asset('manager.png'),size:[1280,720],opacity:()=>time()>=3&&time()<6?1:0}));
 view.add(new Img({src:asset('editor.png'),size:[1280,720],opacity:()=>time()>=6&&time()<10?1:0}));
 view.add(new Img({src:asset('barrels.png'),size:[1280,720],opacity:()=>transferAt(time()).visible?1:0}));
 view.add(new Img({src:asset('stack.png'),size:[48,48],position:()=>{const p=transferAt(time());return [p.x-640,p.y-360];},opacity:()=>transferAt(time()).visible?1:0}));
 yield* time(15,15,linear);
});
