// Run after pinned dependencies are available and Vite serves smoke/ on :9001.
// Launch-scoped blocklist override explicitly approved for this local task.
const {chromium}=require('playwright');
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist']});
 try {
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto('http://127.0.0.1:9001/render.html');await page.waitForFunction(()=>window.ready,{},{timeout:30000});
  await page.evaluate(()=>window.run());await page.waitForFunction(()=>window.done,{},{timeout:120000});
  const result=await page.evaluate(()=>({result:window.result,logs:window.logs}));
  fs.writeFileSync('evidence/motion-canvas-smoke-result.json',JSON.stringify({...result,errors},null,2));
  if(result.result!==0||errors.length)throw new Error('Motion Canvas did not complete cleanly');
  console.log(JSON.stringify(result));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
