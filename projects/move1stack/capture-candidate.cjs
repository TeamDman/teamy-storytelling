const {chromium}=require('playwright');const fs=require('fs');const assert=require('assert/strict');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist']});
 const errors=[];const result={};
 try{
  for(const profile of ['first','source-cutout']){
   const p=await b.newPage({viewport:{width:1280,height:720}});p.on('pageerror',e=>errors.push(String(e)));
   await p.goto(`http://127.0.0.1:9002/still.html?profile=${profile}`);await p.waitForFunction(()=>window.ready,null,{timeout:60000});
   const out=`candidates/filtering/${profile}`;fs.mkdirSync(out,{recursive:true});result[profile]=[];
   for(let i=0;i<8;i++){result[profile].push(await p.evaluate(i=>window.draw(i),i));await p.locator('canvas').screenshot({path:`${out}/figure-0${i+1}.png`});}
   await p.close();
  }
  assert.equal(errors.length,0);fs.writeFileSync('candidates/filtering/browser-result.json',JSON.stringify({result,errors},null,2));console.log('Both profiles captured at all eight exact cameras, zero page errors.');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
