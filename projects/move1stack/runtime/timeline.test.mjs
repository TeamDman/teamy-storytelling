import assert from 'node:assert/strict';
import test from 'node:test';
import {orbitAt,linearAt,textureFrameAt,validateCamera} from './timeline.mjs';

test('camera orbit closes and supports arbitrary out-of-order timestamps',()=>{
 const spec={center:[2,3,4],target:[1,2,3],radius:5,height:2,startRadians:.4,radiansPerSecond:Math.PI/2,up:[0,1,0],fovYDegrees:70};
 const before=orbitAt(1,spec);
 orbitAt(3.5,spec);orbitAt(0,spec);
 assert.deepEqual(orbitAt(1,spec),before);
 const first=orbitAt(0,spec),last=orbitAt(4,spec);
 first.position.forEach((v,i)=>assert.ok(Math.abs(v-last.position[i])<1e-12));
 assert.deepEqual(first.target,spec.target);
});
test('atlas follows nonuniform durations, repeated frame indices and wrap',()=>{
 const animation={ticksPerSecond:20,frametime:2,frames:[2,{index:0,time:3},2,1]};
 const samples=[0,.05,.1,.2,.25,.3,.35,.4,.45];
 assert.deepEqual(samples.map(t=>textureFrameAt(t,animation,3)),[2,2,0,0,2,2,1,1,2]);
 assert.equal(textureFrameAt(-.05,animation,3),1);
 assert.equal(textureFrameAt(.25,animation,3),textureFrameAt(.25,animation,3));
});
test('missing atlas frames play the full strip',()=>{
 const animation={ticksPerSecond:20};
 assert.deepEqual([0,.05,.1,.15].map(t=>textureFrameAt(t,animation,3)),[0,1,2,0]);
});
test('unsupported interpolation and corrupt frame metadata fail explicitly',()=>{
 assert.throws(()=>textureFrameAt(0,{ticksPerSecond:20,interpolate:true},3),/verified shader/);
 assert.throws(()=>textureFrameAt(0,{ticksPerSecond:20,frames:[3]},3),/out of range/);
 assert.throws(()=>textureFrameAt(0,{ticksPerSecond:20,frametime:0},3),/duration/);
});
test('reference camera requires valid projection and orientation',()=>{
 const camera={position:[0,1,3],target:[0,1,0],up:[0,1,0],fovYDegrees:70,near:.05,far:1000};
 assert.deepEqual(validateCamera(camera),camera);
 assert.throws(()=>validateCamera({...camera,target:camera.position}),/orientation/);
 assert.throws(()=>validateCamera({...camera,far:.01}),/projection/);
 assert.throws(()=>validateCamera({...camera,fovYDegrees:180}),/projection/);
});
test('beam/texture linear tracks use supplied rates without accumulated drift',()=>{
 const spec={initial:1,unitsPerSecond:-.4};
 assert.equal(linearAt(20,spec),-7);
 linearAt(0,spec);assert.equal(linearAt(20,spec),-7);
 assert.throws(()=>linearAt(Infinity,spec),/finite/);
});
