const{chromium}=require('playwright');const fs=require('fs');
const profile=process.env.MOVE1_PROFILE??'first';if(!['first','source-cutout'].includes(profile))throw Error('Unknown render profile');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist']});
 try{const p=await b.newPage();const errors=[];p.on('pageerror',e=>{errors.push(String(e));console.error(e)});
 await p.goto('http://127.0.0.1:9002/render.html?profile='+profile);await p.waitForFunction(()=>window.ready,null,{timeout:60000});
 await p.evaluate(()=>{window.runPromise=window.run()});
 let last=-1;
 while(!await p.evaluate(()=>window.done)){
  await p.waitForTimeout(1000);const frame=await p.evaluate(()=>window.frame??0);
  if(Math.floor(frame/60)!==last){last=Math.floor(frame/60);console.log(`Frame ${frame}/720`);}
 }
 const result=await p.evaluate(()=>({result:window.result,logs:window.logs,frame:window.frame}));fs.writeFileSync(profile==='first'?'evidence/orbit-render-result.json':'candidates/filtering/orbit-render-result.json',JSON.stringify({...result,errors},null,2));
 if(result.result!==0||errors.length)throw Error('Motion Canvas export failed');console.log(JSON.stringify(result));
 }finally{await b.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
