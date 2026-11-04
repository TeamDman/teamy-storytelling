import {test} from 'node:test';import assert from 'node:assert/strict';import {compositeAt} from './composite-timeline.mjs';
test('world transition and stack hold their exact endpoints',()=>{
 const start=compositeAt(0), inset=compositeAt(3.2), before=compositeAt(10), after=compositeAt(12);
 assert.equal(start.scale,1);assert.equal(start.ui,0);assert.equal(inset.scale,.4);assert.equal(inset.x,316);assert.equal(inset.y,194);assert.equal(inset.ui,1);
 assert.equal(before.stackX,892);assert.equal(before.stackY,72);assert.ok(Math.abs(after.stackX-892)<1e-9);assert.equal(after.stackY,242);
 assert.equal(compositeAt(6.49).editor,false);assert.equal(compositeAt(6.5).editor,true);
 let previous=72;for(let t=10;t<12;t+=1/30){const p=compositeAt(t);assert.ok(p.stackY>=previous&&p.stackY<=242);previous=p.stackY;}
});
