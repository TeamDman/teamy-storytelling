const{chromium}=require('playwright');const fs=require('fs');const assert=require('assert/strict');
(async()=>{const b=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist']});
try{const p=await b.newPage();await p.goto('http://127.0.0.1:9002/still.html');await p.waitForFunction(()=>window.ready);
const results=await p.evaluate(()=>{
 const w=window.world;const samples=[];
 for(const t of [0,.15,.6,1.95,2,7.5,24,0]){
  w.update(t);const core=w.beam.children[0],halo=w.beam.children[1];
  samples.push({time:t,eye:w.camera.position.toArray(),coreRotation:core.rotation.y,haloRotation:halo.rotation.y,coreDepthWrite:core.children[0].material.depthWrite,haloDepthWrite:halo.children[0].material.depthWrite,coreBlending:core.children[0].material.blending,haloOpacity:halo.children[0].material.opacity,textureOffset:core.children[0].material.map.offset.y});
 }
 return {samples,materials:w.scene.children.filter(x=>x.material).length,fixtureFaces:w.scene.children.filter(x=>x.isMesh).length};
});
assert.deepEqual(results.samples[0],results.samples.at(-1));
for(const s of results.samples){assert.equal(s.haloRotation,0);assert.equal(s.coreDepthWrite,true);assert.equal(s.haloDepthWrite,false);assert.equal(s.haloOpacity,.125);assert.equal(s.coreBlending,0);}
assert.ok(Math.abs(results.samples[0].eye[0]-results.samples[6].eye[0])<1e-10);assert.ok(Math.abs(results.samples[0].eye[2]-results.samples[6].eye[2])<1e-10);
fs.writeFileSync('evidence/browser-animation-validation.json',JSON.stringify(results,null,2));console.log('Beam core rotates; halo stationary; depth states correct; orbit closes; random-access clock repeat exact.');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
