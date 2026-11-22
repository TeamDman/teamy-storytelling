// Timestamp-addressable Chromium canvas renderer with actual browser captures.
const {chromium}=require('playwright'),{spawn}=require('child_process'),fs=require('fs'),http=require('http');
const {once}=require('events'),path=require('path');
(async()=>{
 const out=path.resolve(process.env.OUTPUT_DIR||path.join(__dirname,'../output')),mode=process.argv[2]||'film';
 const timeline=JSON.parse(fs.readFileSync(path.join(out,'timeline.json'))),start=mode==='clip'?Number(process.env.CLIP_START||0):0;
 const end=mode==='clip'?Number(process.env.CLIP_END||start+10):timeline.at(-1).end,duration=mode==='clip'?end-start:mode==='film'?end:8,fps=15;
 if(!Number.isFinite(duration)||duration<=0||start<0||end>timeline.at(-1).end+.001)throw Error('Invalid clip range');
 const server=http.createServer((req,res)=>{const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);let file;
  if(name==='/film.html')file=path.join(__dirname,'film.html');else if(name==='/example/snail.svg')file=path.resolve(__dirname,'../example/snail.svg');else if(/^\/out\/[a-z0-9-]+\.(png|json)$/.test(name))file=path.join(out,path.basename(name));else {res.writeHead(404).end();return;}
  res.setHeader('Content-Type',file.endsWith('.svg')?'image/svg+xml':file.endsWith('.json')?'application/json':file.endsWith('.png')?'image/png':'text/html');fs.createReadStream(file).on('error',()=>res.writeHead(404).end()).pipe(res);
 });await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox']});const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});page.on('pageerror',e=>console.error(e));await page.goto(`http://127.0.0.1:${server.address().port}/film.html`);await page.waitForFunction(()=>window.ready,null,{timeout:10000});
 if(mode==='preview'){for(const t of (process.env.PREVIEW_TIMES||'0').split(',').map(Number)){await page.evaluate(t=>window.renderAt(t),t);await page.screenshot({path:path.join(out,`preview-final-${t}.png`)});}await browser.close();await new Promise(resolve=>server.close(resolve));return;}
 const hasAudio=mode==='film'||mode==='clip',scale=mode==='clip'?'1280:720':'1920:1080';
 const args=['-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-framerate',String(fps),'-i','pipe:0'];
 if(hasAudio){if(mode==='clip')args.push('-ss',String(start),'-t',String(duration));args.push('-i',path.join(out,'narration.wav'));}
 args.push('-vf',`scale=${scale}:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p`,'-color_range','tv','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p');
 if(hasAudio)args.push('-c:a','aac','-b:a','128k','-shortest');
 const label=mode==='clip'?(process.env.CLIP_LABEL||'review'):'film';if(!/^[a-z0-9_-]+$/.test(label))throw Error('Invalid clip label');args.push('-movflags','+faststart',path.join(out,label+'.mp4'));
 const ff=spawn('ffmpeg',args,{stdio:['pipe','inherit','inherit']});ff.stdin.on('error',e=>console.error(e));const total=Math.ceil(duration*fps);
 try{for(let i=0;i<total;i++){await page.evaluate(t=>window.renderAt(t),start+i/fps);const buf=await page.screenshot({type:'jpeg',quality:91});if(!ff.stdin.write(buf))await once(ff.stdin,'drain');if(i%450===0)console.log(label,i,'/',total)}ff.stdin.end();const [code]=await once(ff,'exit');if(code!==0)throw Error('ffmpeg exit '+code);console.log('rendered',label,duration);}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})();
