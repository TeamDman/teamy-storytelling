import {makeScene2D} from '@motion-canvas/2d';
import {createSignal,linear} from '@motion-canvas/core';
import {Three} from './Three';
import {createWorld} from '../runtime/world.mjs';
const profile=new URLSearchParams(location.search).get('profile')??'first';
const world=await createWorld({profile});
export default makeScene2D(function*(view){
 const time=createSignal(0);
 view.add(new Three({size:[1280,720],scene:world.scene,camera:world.camera,background:'#b5d0ff',onRender(renderer,scene,camera){
  renderer.setClearColor('#b5d0ff');world.update(time());renderer.render(scene,camera);
 }}));
 yield* time(24,24,linear);
});
