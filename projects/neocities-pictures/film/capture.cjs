// Capture actual Chromium layout from a temporary copy of the shipped example.
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http'), os = require('os'), assert = require('assert');
(async()=>{
 const out=process.env.OUTPUT_DIR || path.resolve(__dirname,'../output'); fs.mkdirSync(out,{recursive:true});
 const fixture=fs.mkdtempSync(path.join(os.tmpdir(),'moon-snail-')); fs.cpSync(path.resolve(__dirname,'../example'),fixture,{recursive:true});
 const server=http.createServer((req,res)=>{const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\//,'') || 'index.html';
  if(!['index.html','style.css','snail.svg','garden.svg','stamp.svg'].includes(name)){res.writeHead(404).end();return;}
  res.setHeader('Content-Type',name.endsWith('.css')?'text/css':name.endsWith('.svg')?'image/svg+xml':'text/html');res.setHeader('Cache-Control','no-store');fs.createReadStream(path.join(fixture,name)).pipe(res);
 }); await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve)); const base=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM || '/usr/bin/chromium',args:['--no-sandbox']});
 const measurements={};
 try {
 for (const [name,width,height,gap,right] of [['wide',1024,760,null],['phone',390,844,null],['anchor-wide',1024,760,null,'100px'],['anchor-phone',390,844,null,'100px'],['anchor-exercise',1024,760,null,'40px'],['gap',1024,760,'60px'],['exercise',1024,760,'12px'],['middle',700,760,null],['w900',900,760,null],['w800',800,760,null],['w650',650,760,null],['w600',600,760,null],['w500',500,760,null]]) {
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
  await page.goto(base+'/index.html'); await page.locator('img').first().waitFor();
  if(gap) { const css=path.join(fixture,'style.css');const original=fs.readFileSync(css,'utf8');try {fs.writeFileSync(css,original.replace('gap: 24px',`gap: ${gap}`)); await page.reload(); await page.waitForFunction(value=>getComputedStyle(document.querySelector('.postcard')).gap===value,gap,{timeout:5000});} finally {fs.writeFileSync(css,original);} }
  if(right) { const css=path.join(fixture,'style.css');const original=fs.readFileSync(css,'utf8');try {fs.writeFileSync(css,original.replace('right: 12px',`right: ${right}`));await page.reload();await page.waitForFunction(value=>getComputedStyle(document.querySelector('.stamp')).right===value,right,{timeout:5000});} finally {fs.writeFileSync(css,original);} }
  await page.screenshot({path:path.join(out,`${name}.png`)});
  const m=await page.evaluate(()=>{const e=document.querySelector('.postcard'),c=[...document.querySelectorAll('.postcard-art,.postcard-note,.stamp')]; return {grid:getComputedStyle(e).gridTemplateColumns,gap:getComputedStyle(e).gap,right:getComputedStyle(document.querySelector('.stamp')).right,rects:c.map(x=>{const r=x.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}})}});
  measurements[name]=m;
  if(name.startsWith('anchor-')){const base=measurements[name==='anchor-phone'?'phone':'wide'];assert.equal(m.right,right);assert(Math.abs((base.rects[2].x-m.rects[2].x)-(parseInt(right)-12))<0.1,'stamp movement should match the offset edit');for(let i=0;i<2;i++){assert(Math.abs(base.rects[i].x-m.rects[i].x)<0.1 && Math.abs(base.rects[i].y-m.rects[i].y)<0.1,'other children must stay put');}}
  if(name==='wide'){assert(Math.abs(m.rects[0].y-m.rects[1].y)<1 && m.rects[1].x>m.rects[0].x, 'wide picture and note should share a row');}
  if(name==='phone'){assert(Math.abs(m.rects[0].x-m.rects[1].x)<1 && m.rects[1].y>=m.rects[0].y+m.rects[0].height, 'phone picture and note should stack');}
  if(name==='gap')assert.equal(m.gap,'60px','the refreshed edit must be visible');
  if(name==='exercise')assert.equal(m.gap,'12px','the exercise edit must be visible');
  if(name==='wide'||name==='phone'){const positioning=await page.evaluate(()=>({parent:getComputedStyle(document.querySelector('.postcard')).position,stamp:getComputedStyle(document.querySelector('.stamp')).position,alt:document.querySelector('.postcard-art').alt}));assert.deepEqual([positioning.parent,positioning.stamp],['relative','absolute']);assert(positioning.alt.length>0,'illustration needs alternative text');}
  console.log(name,JSON.stringify(m)); await page.close();
 }
 } finally {await browser.close();await new Promise(resolve=>server.close(resolve));fs.rmSync(fixture,{recursive:true,force:true});}
})();
