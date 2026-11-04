import {Img, makeScene2D} from '@motion-canvas/2d';
import {createSignal, linear} from '@motion-canvas/core';
import {Three} from './Three';
import {createWorld} from '../runtime/world.mjs';
import {createPlayer} from './story-player.mjs';
const world=await createWorld({profile:'source-cutout'});
const player=await createPlayer(world.scene);
const empty=new URL('../.inputs/story-assets/empty.png',import.meta.url).href;
const full=new URL('../.inputs/story-assets/full.png',import.meta.url).href;
export default makeScene2D(function*(view){
 const time=createSignal(0);
 view.add(new Three({size:[1280,720],scene:world.scene,camera:world.camera,background:'#b5d0ff',onRender(renderer,scene,camera){
  const t=time();world.update(t);player.update(t);
  // Match the earlier staged viewpoint, converted from Blender's Z-up axes.
  const angle=-.8+t*.025; camera.position.set(1.5+6*Math.sin(angle),3.5,-6*Math.cos(angle));
  camera.lookAt(1.35,1.7,-.05);camera.fov=58;camera.updateProjectionMatrix();
  renderer.setClearColor('#b5d0ff');renderer.render(scene,camera);
 }}));
 view.add(new Img({src:empty,size:[1280,720],opacity:()=>time()>=2.5&&time()<4.8?1:0}));
 view.add(new Img({src:full,size:[1280,720],opacity:()=>time()>=5.2?1:0}));
 yield* time(8,8,linear);
});
