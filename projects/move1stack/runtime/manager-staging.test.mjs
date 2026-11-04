import {test} from 'node:test';import assert from 'node:assert/strict';
import {playerPosition,managerCenter,modelScale,managerPose,cameraAngle,armSwing} from './manager-staging.mjs';
test('hovering player looks from command side at the manager',()=>{
 const {yaw,headPitch}=managerPose(), [x,y,z]=playerPosition,[tx,ty,tz]=managerCenter;
 const horizontal=Math.hypot(tx-x,tz-z), forward=[-Math.sin(yaw),-Math.cos(yaw)];
 assert.ok(y>=2 && horizontal>2 && horizontal<4.5);
 assert.ok(Math.abs(forward[0]-(tx-x)/horizontal)<1e-12 && Math.abs(forward[1]-(tz-z)/horizontal)<1e-12);
 assert.ok(Math.abs(Math.tan(headPitch)-(ty-(y+28*modelScale))/horizontal)<1e-12);
 for(let t=0;t<=16;t+=.5)assert.ok(Math.sin(cameraAngle(t))<0);
 assert.equal(armSwing(0),0);assert.equal(armSwing(2.05),1.05);assert.equal(armSwing(2.6),0);
});
