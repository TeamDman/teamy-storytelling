const {chromium}=require('playwright');const fs=require('fs');
if(fs.existsSync('media/move1stack-manager-flight-v3.mp4')) throw Error('Preview exists; preserve it before rerendering');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist']});
 try {const p=await b.newPage();const errors=[];p.on('pageerror',e=>{errors.push(String(e));console.error(e)});
 await p.goto('http://127.0.0.1:9002/manager-flight-render.html');await p.waitForFunction(()=>window.ready,null,{timeout:60000});await p.evaluate(()=>window.run());
 await p.waitForFunction(()=>window.done,null,{timeout:600000});const result=await p.evaluate(()=>({result:window.result,logs:window.logs,frame:window.frame}));
 fs.writeFileSync('evidence/manager-flight-render-result.json',JSON.stringify({...result,errors},null,2));if(result.result!==0||errors.length)throw Error('Motion Canvas export failed');console.log(JSON.stringify(result));
 }finally{await b.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
