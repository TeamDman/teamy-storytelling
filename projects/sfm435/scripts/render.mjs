import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
const name=process.argv[2]||'smoke';
const stillArg=process.argv.find(x=>x.startsWith('--stills='));
const port=Number(process.argv.find(x=>x.startsWith('--port='))?.slice(7)||9010);
if(!Number.isInteger(port)||port<1024||port>65535)throw Error('Invalid local render port');
const browser=await chromium.launch({executablePath:process.env.CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:1920,height:1080}});
let errors=[];
page.on('pageerror',e=>{errors.push(String(e));console.error(e)});
page.on('console',m=>{if(m.type()==='error')console.error(m.text())});
const started=Date.now();
try {
  await page.goto(`http://127.0.0.1:${port}/render.html?project=${encodeURIComponent(name)}`);
  await page.waitForFunction(()=>window.ready,null,{timeout:60000});
  if(stillArg){
    await mkdir(`review/${name}`,{recursive:true});
    // Renderer 3.17.2 calculates the first seek frame before assigning fps.
    // Prime at zero so all requested timestamps use the selected 24 fps.
    await page.evaluate(()=>window.still(0));
    for(const t of stillArg.slice(9).split(',').map(Number)){
      const data=await page.evaluate(t=>window.still(t),t);
      await writeFile(`review/${name}/${String(t).padStart(4,'0')}.png`,Buffer.from(data.split(',')[1],'base64'));
      console.log(`STILL ${name} ${t}s`);
    }
  }else{
    const range=process.argv.find(x=>x.startsWith('--range='));
    const options=range?{range:range.slice(8).split(',').map(Number)}:{};
    await page.evaluate(options=>{window.run(options)},options);
    while(!await page.evaluate(()=>window.done)){
      await page.waitForTimeout(1000);
      if(errors.length)throw Error(errors.join('\n'));
      if((Date.now()-started)%20000<1100)console.log(`RENDER ${name}: frame ${await page.evaluate(()=>window.frame)}`);
    }
    const report=await page.evaluate(()=>({result:window.result,logs:window.logs,frame:window.frame,timelines:globalThis.actualTimelines}));
    console.log(JSON.stringify(report));
    await mkdir('renders',{recursive:true});
    await writeFile(`renders/${name}-render.json`,JSON.stringify({...report,seconds:(Date.now()-started)/1000},null,2));
    if(report.result!==0||errors.length)throw Error('Motion Canvas render did not succeed');
  }
}finally{await browser.close()}
