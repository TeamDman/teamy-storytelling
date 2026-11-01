const{chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/lib/chromium/chromium',headless:false,chromiumSandbox:true,ignoreDefaultArgs:['--enable-unsafe-swiftshader','--unsafely-disable-devtools-self-xss-warnings'],args:['--ignore-gpu-blocklist','--enable-logging=stderr']});
 const p=await b.newPage({viewport:{width:680,height:260}});await p.setContent('<!doctype html><title>Approved local WebGL test</title><body style="margin:0;background:#111;color:white;font:14px sans-serif"></body>');
 const results=await p.evaluate(()=>{
  const results=[];
  for(const type of ['webgl','webgl2']){
   const canvas=document.createElement('canvas');canvas.width=320;canvas.height=180;document.body.append(canvas);
   let error=null;canvas.addEventListener('webglcontextcreationerror',e=>error=e.statusMessage);
   const gl=canvas.getContext(type,{preserveDrawingBuffer:true});if(!gl){results.push({type,available:false,error});continue;}
   const prefix=type==='webgl2'?'#version 300 es\n':'';
   const vertex=prefix+(type==='webgl2'?'in':'attribute')+' vec2 position;void main(){gl_Position=vec4(position,0.,1.);}';
   const fragment=prefix+'precision mediump float;'+(type==='webgl2'?'out vec4 color;':'')+'void main(){'+(type==='webgl2'?'color':'gl_FragColor')+'=vec4(1.,.25,.125,1.);}';
   function shader(kind,source){const s=gl.createShader(kind);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;}
   const program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(program));gl.useProgram(program);
   const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-.75,-.7,.75,-.7,0,.75]),gl.STATIC_DRAW);
   const loc=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);gl.clearColor(.125,.25,.5,1);gl.clear(gl.COLOR_BUFFER_BIT);gl.drawArrays(gl.TRIANGLES,0,3);
   const center=new Uint8Array(4),corner=new Uint8Array(4);gl.readPixels(160,90,1,1,gl.RGBA,gl.UNSIGNED_BYTE,center);gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,corner);
   results.push({type,available:true,version:gl.getParameter(gl.VERSION),center:[...center],corner:[...corner],error:gl.getError(),png:canvas.toDataURL('image/png')});
  }
  return results;
 });
 for(const r of results){if(r.png){fs.writeFileSync('evidence/approved-'+r.type+'.png',Buffer.from(r.png.split(',')[1],'base64'));delete r.png;}}
 await p.screenshot({path:'evidence/approved-webgl-preview.png'});
 await p.goto('chrome://sandbox');const sandbox=await p.locator('body').innerText();fs.writeFileSync('evidence/approved-sandbox.txt',sandbox);
 const cdp=await b.newBrowserCDPSession();fs.writeFileSync('evidence/approved-gpu-system-info.json',JSON.stringify(await cdp.send('SystemInfo.getInfo'),null,2));
 fs.writeFileSync('evidence/approved-webgl-result.json',JSON.stringify({results,sandbox},null,2));console.log(JSON.stringify({results,sandbox}));await b.close();
 if(results.some(r=>!r.available||r.error!==0||r.center[0]!==255||r.corner[0]===255)||!sandbox.includes('Seccomp-BPF sandbox\tYes'))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
