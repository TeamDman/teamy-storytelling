import {Img,Rect,makeScene2D} from '@motion-canvas/2d';
import {createSignal,linear} from '@motion-canvas/core';
import {Three} from './Three';
import {createWorld} from '../runtime/world.mjs';
import {createPlayer} from './story-player.mjs';
import {compositeAt} from '../runtime/composite-timeline.mjs';
const world=await createWorld({profile:'source-cutout'});
const player=await createPlayer(world.scene);
const asset=(name:string)=>new URL(`../.inputs/composite-assets/${name}`,import.meta.url).href;
export default makeScene2D(function*(view){
 const time=createSignal(0);
 view.add(new Rect({size:[1280,720],fill:'#111b29'}));
 view.add(new Three({size:[1280,720],scene:world.scene,camera:world.camera,background:'#b5d0ff',scale:()=>compositeAt(time()).scale,position:()=>{const p=compositeAt(time());return [p.x,p.y];},onRender(renderer,scene,camera){
  const t=time();world.update(t);player.update(t);renderer.setClearColor('#b5d0ff');renderer.render(scene,camera);
 }}));
 view.add(new Img({src:asset('manager.png'),size:[592,384],position:[-314,-18],opacity:()=>compositeAt(time()).editor?0:compositeAt(time()).ui}));
 view.add(new Img({src:asset('editor.png'),size:[592,480],position:[-314,-20],opacity:()=>compositeAt(time()).editor?compositeAt(time()).ui:0}));
 for(const [name,y] of [['a',20],['b',190]] as const){
  view.add(new Img({src:asset(`barrel-${name}.png`),size:[352,142],position:[396,y+71-360],opacity:()=>compositeAt(time()).ui}));
  view.add(new Img({src:asset(`label-${name}.png`),size:[24,24],position:[196,y+42-360],opacity:()=>compositeAt(time()).ui}));
 }
 view.add(new Img({src:new URL('../.inputs/composite-corrected/stack.png',import.meta.url).href,size:[34,34],position:()=>{const p=compositeAt(time());return [p.stackX-639,p.stackY-359];},opacity:()=>compositeAt(time()).ui}));
 yield* time(16,16,linear);
});
