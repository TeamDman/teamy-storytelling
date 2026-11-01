const{chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist']});
 try{const p=await browser.newPage({viewport:{width:1280,height:720}});const errors=[];p.on('pageerror',e=>{errors.push(String(e));console.error(String(e))});
 await p.goto('http://127.0.0.1:9002/still.html');await p.waitForFunction(()=>window.ready,null,{timeout:60000});
 fs.mkdirSync('stills',{recursive:true});const poses=[];
 for(let i=0;i<8;i++){poses.push(await p.evaluate(i=>window.draw(i),i));await p.locator('canvas').screenshot({path:`stills/figure-0${i+1}.png`});}
 const first=await p.evaluate(()=>{window.draw(0,0);return document.querySelector('canvas').toDataURL()});await p.evaluate(()=>window.draw(6,2.4));const repeated=await p.evaluate(()=>{window.draw(0,0);return document.querySelector('canvas').toDataURL()});
 fs.writeFileSync('evidence/still-result.json',JSON.stringify({poses,errors,repeatIdentical:first===repeated},null,2));
 if(errors.length||first!==repeated||poses.some(x=>x.glError))throw Error('Still validation failed');
 console.log('Eight stills rendered; random-access repeat identical; zero WebGL errors.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
