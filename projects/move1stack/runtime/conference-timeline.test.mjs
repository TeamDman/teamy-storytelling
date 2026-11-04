import {test} from 'node:test';
import assert from 'node:assert/strict';
import {transferAt} from './conference-timeline.mjs';
test('one continuous stack moves from source to destination without a jump',()=>{
 assert.equal(transferAt(9.99).visible,false);
 assert.deepEqual(transferAt(10),{visible:true,x:128,y:238,phase:'source'});
 assert.deepEqual(transferAt(13),{visible:true,x:720,y:238,phase:'destination'});
 assert.equal(transferAt(15).visible,true);
 assert.equal(transferAt(15.01).visible,false);
 let last=128;
 for(let t=11.5;t<=13;t+=1/30){const p=transferAt(t);assert.ok(p.x>=last&&p.x<=720);assert.ok(p.y>=178&&p.y<=238);last=p.x;}
 assert.equal(transferAt(12.25).phase,'moving');
});
