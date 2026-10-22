import {makeScene2D,Node,Rect,Txt,Line,Circle,Code,lines} from '@motion-canvas/2d';
import {all,createSignal,waitFor,linear} from '@motion-canvas/core';
import {sans,mono,codePanel} from './components';
import {tomlHighlighter} from './highlight';
import {director} from './director';
import {payloadGrid} from './payload';
import {baselineExcerpt,fixedExcerpt,inputExcerpt,extractionExcerpt,insertionExcerpt} from './evidence';
const A={bg:'#e3e1dc',ink:'#212a35',muted:'#626e7a',cobalt:'#335eb0',white:'#fdfdfa',runtime:'#111d2a',mint:'#8cdfba',line:'#9cabb9'};
const tx=(p:any)=><Txt fontFamily={sans} fill={A.ink} fontSize={31} {...p}/>;
const fmt=(v:number)=>Math.round(v).toLocaleString('en-US');
function region(parent:Node,x:number,y:number,label:string,fill:string){const n=new Rect({x,y,width:1620,height:640,radius:22,fill,stroke:A.line,lineWidth:2});parent.add(n);n.add(tx({text:label,x:-748,y:-273,offsetX:-1,fontSize:26,fill:fill===A.runtime||fill===A.cobalt?'#e8f0fc':A.muted}));return n;}
function block(parent:Node,x:number,y:number,w:number,h:number,label:string,fill=A.white,ink=A.ink){const n=new Rect({x,y,width:w,height:h,radius:12,fill,stroke:A.line,lineWidth:2});n.add(tx({text:label,textAlign:'center',fontSize:30,fill:ink,lineHeight:43}));parent.add(n);return n;}
function link(parent:Node,points:number[][],color=A.line,dashed=false){const line=new Line({points:points as any,stroke:color,lineWidth:5,endArrow:true,arrowSize:14,lineDash:dashed?[12,10]:[],end:0});parent.add(line);line.moveToBottom();return line;}
function* handoff(view:any,id:string,fixed:boolean){const n=new Rect({width:1640,height:650,y:45,radius:22,fill:A.runtime,stroke:A.mint,lineWidth:3});view.add(n);const remaining=createSignal(5);n.add(tx({text:id,x:-750,y:-260,offsetX:-1,fontFamily:mono,fontSize:27,fill:A.mint}));n.add(tx({text:'Pause here',x:-750,y:-164,offsetX:-1,fontSize:84,fontWeight:700,fill:A.white}));n.add(tx({text:fixed?'SFM 4.35 • same setup, same sequence':'SFM 4.34 • run the next pulse',x:-750,y:-63,offsetX:-1,fontSize:38,fill:A.white}));n.add(tx({text:`First 99,999  /  Second ${fixed?'100,000':'0'}`,x:-750,y:22,offsetX:-1,fontFamily:mono,fontSize:39,fill:A.mint}));n.add(tx({text:'Expected from automated characterization',x:-750,y:100,offsetX:-1,fontSize:27,fill:'#a4b7c7'}));n.add(tx({text:'Local preparation required • commands in extras.7z',x:-750,y:161,offsetX:-1,fontSize:27,fill:A.white}));const bar=new Rect({x:-750,y:229,offsetX:-1,width:1500,height:10,fill:A.mint});n.add(bar);n.add(tx({text:()=>`${Math.max(0,Math.ceil(remaining()))}s • playback continues automatically`,x:-750,y:278,offsetX:-1,fontSize:23,fill:'#a4b7c7'}));yield* waitFor(4);yield* all(bar.width(0,5,linear),remaining(0,5,linear));yield* waitFor(1);yield* n.opacity(0,.4);n.remove();}
export default makeScene2D(function*(view){
 const d=director('atlas');d.mark('intro','0 · Introduction',true);view.fill(A.bg);
 const title=new Txt({text:'Inside the release',x:-850,y:-365,offsetX:-1,fontSize:64,fontFamily:sans,fontWeight:700,fill:A.ink});view.add(title);
 view.add(tx({text:'SFM 4.35  /  TECHNICAL ATLAS',x:-850,y:-480,offsetX:-1,fontSize:24,fill:A.cobalt}));view.add(tx({text:'Schematic • source-derived unless marked tested',x:850,y:-480,offsetX:1,fontSize:20,fill:A.muted}));
 const crumb=new Txt({text:'0 Introduction  →  1 Source to build  →  2 Build to behavior  →  3 Baseline to fix  →  4 Other changes',x:-850,y:485,offsetX:-1,fontSize:23,fontFamily:sans,fill:A.muted});view.add(crumb);
 const viewport=new Rect({width:1780,height:720,y:45,clip:true});view.add(viewport);
 const map=new Node({scale:.4});viewport.add(map);
 const source=region(map,-920,-530,'01  /  AUTHORED SOURCE + PROJECTIONS',A.cobalt);
 const jar=region(map,920,-530,'02  /  CAPTURED RUNTIME PAYLOADS INCLUDING GAMETESTS',A.white);
 const runtime=region(map,920,530,'03  /  EXECUTED CODE + WORLD',A.runtime);
 const resources=region(map,-920,530,'04  /  RESOURCES + CLIENT CONFIG',A.white);
 link(map,[[-100,-530],[100,-530]],A.cobalt).end(1);link(map,[[920,-200],[920,200]],A.cobalt).end(1);link(map,[[100,530],[-100,530]],A.cobalt).end(1);
 const liquid=block(source,-500,-45,470,280,'Liquid core',A.white);const projection=block(source,90,-45,470,280,'Projection config',A.white);
 const generated=block(source,590,-45,380,280,'Java\nResources\nBuild files',A.white);
 link(source,[[-265,-45],[-145,-45]],A.white).end(1);link(source,[[325,-45],[392,-45]],A.white).end(1);
 source.add(tx({text:'Replaces branch-per-Minecraft source maintenance.',y:200,fontSize:28,fill:A.white}));source.add(tx({text:'Git branches remain.',y:260,fontSize:25,fill:'#cbd9f4'}));
 const jarFiles=new Node({});jar.add(jarFiles);
 const grid=payloadGrid(jarFiles);grid.scale(.85);grid.y(-20);
 const nested=new Node({});runtime.add(nested);
 const trigger=new Rect({width:1490,height:450,y:25,radius:16,stroke:'#748ba0',lineWidth:3,fill:'#172739'});nested.add(trigger);
 trigger.add(tx({text:'THIS TRIGGER',x:-690,y:-183,offsetX:-1,fontSize:23,fill:'#9db2c4'}));
 const record=new Rect({x:50,y:35,width:1250,height:315,radius:14,stroke:A.mint,lineWidth:3,fill:'#193944'});trigger.add(record);
 record.add(tx({text:'SOURCE RECORD → DESTINATION ATTEMPTS',x:-570,y:-117,offsetX:-1,fontSize:25,fill:A.mint}));
 const first=createSignal(99975),second=createSignal(0);
 const d1=block(record,-300,35,500,175,'',A.runtime,A.white),d2=block(record,300,35,500,175,'',A.runtime,A.white);
 [d1,d2].forEach((n,i)=>n.add(<>
  {tx({text:i?'SECOND DROPPER':'FIRST DROPPER',y:-48,fontSize:21,fill:'#aec0d0'})}
  {tx({text:()=>fmt(i?second():first()),y:9,fontFamily:mono,fontSize:44,fill:A.white,fontWeight:700})}
  {tx({text:'/ 100,000 FE',y:61,fontSize:21,fontFamily:mono,fill:'#aec0d0'})}
 </>));
 const zeroMark=new Rect({x:-250,y:70,width:500,height:175,radius:12,stroke:'#eebc72',lineWidth:6,opacity:0});trigger.add(zeroMark);
 const runtimeCaption=new Txt({text:'No energy extracted yet',y:280,fontSize:28,fontFamily:sans,fill:A.mint});runtime.add(runtimeCaption);
 const config=block(resources,-400,-55,650,275,'Client configuration');const recipe=block(resources,390,-55,650,275,'Recipes + references');resources.add(tx({text:'French  •  Brazilian Portuguese  •  Buffer itemless loot',y:245,fontSize:28,fill:A.muted}));
 function* go(x:number,y:number,scale=1,seconds=1.6){yield* all(map.scale(scale,seconds),map.position([-x*scale,-y*scale],seconds));}
 function* tab(label:string){const n=new Rect({width:1100,height:150,y:-60,fill:A.white,radius:20,stroke:A.cobalt,lineWidth:3});n.add(tx({text:label,fontSize:45,fill:A.cobalt,fontWeight:700}));view.add(n);yield* waitFor(1.5);yield* all(n.position([-570,475],.5),n.scale(.35,.5),n.opacity(0,.5));n.remove();}
 function focus(t:string,c:string){title.text(t);crumb.text(c);}
 yield* waitFor(5);yield* map.scale(.39,1.5);
 yield* d.at(10);d.mark('source','1 · Source to build',true);focus('Author once. Project explicitly.','1 Source to build  /  Liquid core → projection config → generated outputs');
 yield* tab('1  Source to build');yield* go(-920,-530);yield* liquid.stroke(A.mint,.5);yield* projection.stroke(A.mint,.5);yield* generated.stroke(A.mint,.5);
 yield* d.at(24);d.mark('jar');focus('Inspect the runtime payload.','1 Source to build  /  source → projection → runtime payload');yield* go(920,-530);
 yield* waitFor(4);
 yield* d.at(38);d.mark('executed-path','2 · Build to behavior',true);focus('Follow the executed path.','2 Build to behavior  /  runtime payload → executed Java → SFML');
 yield* tab('2  Build to behavior');yield* go(920,-110,.72);jarFiles.opacity(.35);
 const execution=region(map,920,-110,'RENDERED JAVA • TESTED PROJECTIONS',A.runtime);execution.height(480);execution.children()[0].y(-200);
 const ex=codePanel(execution,extractionExcerpt,'OutputStatement.java 309–310 • earlier checks omitted',{y:10,width:1480,height:250,fontSize:40});
 execution.add(tx({text:'Rendered Java • 8e349578 • SFML directs destination attempts',y:185,fontSize:27,fill:A.mint}));
 yield* ex.code.selection(lines(1),.5);
 yield* d.at(52);d.mark('input');focus('INPUT registers a source and constraints.','2 Build to behavior  /  this trigger → source input record');execution.remove();yield* go(920,530);
 runtimeCaption.text('Source + constraints • no energy extracted at INPUT');yield* record.stroke(A.mint,.7);
 const inputCode=codePanel(runtime,inputExcerpt,'InputStatement.java 57–67 • … = omitted source',{y:-70,width:1470,height:390,fontSize:32});
 nested.scale(.38);nested.y(205);runtimeCaption.opacity(0);yield* inputCode.code.selection(lines(2),.4);yield* waitFor(3);
 yield* d.at(64);d.mark('output');focus('OUTPUT turns the record into a transfer.','2 Build to behavior  /  source record → destination attempt → actual transfer');inputCode.frame.remove();nested.scale(1);nested.y(0);runtimeCaption.opacity(1);nested.opacity(.18);runtimeCaption.text('Simulation is outlined. Extraction and insertion are actual.');
 const stack=new Node({});runtime.add(stack);const steps=['Read source','Simulate acceptance','Apply limits','Extract','Insert returned amount'];
 const rowNodes:Rect[]=[];steps.forEach((s,i)=>{const n=block(stack,0,-175+i*89,1070,74,s,i<3?A.runtime:'#2d564f',A.white);if(i<3)n.lineDash([10,8]);rowNodes.push(n)});
 for(let i=0;i<5;i++){yield* rowNodes[i].stroke(A.mint,.3);yield* rowNodes[i].lineWidth(6,.3);yield* waitFor(1.2);}
 runtimeCaption.text('Simulation is outlined. Extraction and insertion are actual.');
 yield* d.at(78);d.mark('conversion25');focus('25 FE requested → 24 FE delivered','2 Build to behavior  /  Mekanism default · 2.5 J / FE · integer conversion');stack.remove();nested.opacity(0);
 const conversion=new Node({});runtime.add(conversion);
 const sim=block(conversion,0,-105,1450,180,'25 FE  →  62 J  →  24 FE',A.runtime,A.white);sim.lineDash([12,8]);sim.children()[0].fontSize(52);sim.add(tx({text:'SIMULATED',x:-660,y:-60,offsetX:-1,fontSize:22,fill:'#a8c0d5'}));
 const actual=block(conversion,0,125,1450,180,'Actually withdrawn 60 J  /  Delivered 24 FE','#2b514c',A.white);actual.children()[0].fontSize(37);actual.add(tx({text:'ACTUAL',x:-660,y:-60,offsetX:-1,fontSize:22,fill:A.mint}));
 runtimeCaption.text('No energy destroyed. 60 J withdrawn equals 24 FE delivered.');yield* actual.stroke(A.mint,.8);
 yield* d.at(92);d.mark('conversion1');focus('The last 1 FE returns zero.','2 Build to behavior  /  source record → one destination-sized problem');
 sim.children()[0].text('1 FE  →  2 J  →  0 FE');actual.children()[0].text('Actually withdrawn 0 J');runtimeCaption.text('A destination-sized problem. The source can still serve others.');
 yield* waitFor(4);yield* all(conversion.scale(.6,.8),conversion.position([-260,10],.8));nested.opacity(.4);yield* zeroMark.opacity(1,.6);
 yield* d.at(104);d.mark('fixture','3 · Baseline to fix',true);focus('Two droppers, one repeatable sequence.','3 Baseline to fix  /  setup → first pulse → separate work drain');conversion.remove();yield* tab('3  Baseline to fix');nested.opacity(1);zeroMark.opacity(0);runtimeCaption.text('Start: 99,975 / 0');
 yield* waitFor(2);yield* all(first(99999,1),second(100000,1));runtimeCaption.text('First pulse: 99,999 / 100,000');yield* waitFor(2);
 const drain=link(runtime,[[350,170],[350,260],[650,260]],A.mint);yield* drain.end(1,.8);yield* second(0,1);runtimeCaption.text('Separate drain: second works; first stays idle.');
 yield* d.at(118);d.mark('D01baseline');yield* handoff(view,'D01baseline',false);
 yield* d.at(130);d.mark('wrong-scope');focus('4.34 closes the wrong scope.','3 Baseline to fix  /  trigger stays open · source record marked done');drain.remove();
 yield* zeroMark.opacity(1,.6);runtimeCaption.text('First: 0 FE → source.setDone() → second skipped');
 const shut=new Rect({x:50,y:60,width:1250,height:315,fill:'#563443',stroke:'#ee9cb0',lineWidth:4,radius:14,opacity:0});shut.add(tx({text:'SOURCE RECORD DONE',fontSize:49,fontWeight:700,fill:'#ffd7e1'}));nested.add(shut);yield* shut.opacity(.94,.8);
 yield* d.at(142);d.mark('right-scope');focus('4.35 closes only this attempt.','3 Baseline to fix  /  same source record → next destination');yield* shut.opacity(0,.8);shut.remove();nested.scale(.5);nested.y(160);runtimeCaption.opacity(0);
 const change=codePanel(runtime,baselineExcerpt,'4.34 → 4.35 • OutputStatement.java 315–320 • … = omitted source',{y:-100,width:1470,height:310,fontSize:28});
 yield* change.code.selection(lines(2),.3);yield* waitFor(2);yield* change.code.code(fixedExcerpt,.7);yield* change.code.selection(lines(2),.3);runtimeCaption.text('Source records reset every trigger. No new INPUT is needed here.');
 yield* d1.stroke('#eebc72',.6);yield* d2.stroke(A.mint,.6);yield* second(100000,1.4);yield* waitFor(2);
 yield* d.at(156);d.mark('D02fixed');change.frame.remove();nested.scale(1);nested.y(0);runtimeCaption.opacity(1);yield* handoff(view,'D02fixed',true);
 yield* d.at(168);d.mark('tests');focus('Automated characterization: both PASS.','3 Baseline to fix  /  baseline reproduces bug · fixed confirms intended behavior');
 const proof=new Node({});runtime.add(proof);nested.opacity(.25);block(proof,-390,-50,690,250,'4.34  PASS\nBug reproduced','#25483f',A.mint);block(proof,390,-50,690,250,'4.35  PASS\nIntended behavior','#25483f',A.mint);runtimeCaption.text('Full manual two-button walkthrough: not yet verified.');
 yield* d.at(180);d.mark('tunnel','4 · The rest of 4.35',true);focus('Tunnel listeners follow positions.','4 Other changes  /  NeoForge 1.20.3+ · position-level listener');proof.remove();yield* tab('4  The rest of 4.35');nested.opacity(0);
 const listener=new Node({});runtime.add(listener);block(listener,-440,-15,620,250,'Retain relay\nblock entity',A.runtime,A.white);const capability=block(listener,400,-15,620,250,'Capability A',A.runtime,A.white);
 const ring=new Circle({x:400,y:-15,width:680,height:300,stroke:A.mint,lineWidth:4});listener.add(ring);link(listener,[[76,-15],[-120,-15]],A.mint).end(1);runtimeCaption.text('Watch far position. Invalidation reaches the same relay.');yield* waitFor(3);yield* capability.children()[0].text('Capability B',.8);
 yield* d.at(192);d.mark('config');focus('Optional Label Gun confirmations.','4 Other changes  /  client config → routine push/pull success messages');listener.remove();nested.opacity(1);runtimeCaption.text('First 99,999  /  Second 100,000');yield* go(-920,530);
 recipe.opacity(.2);config.opacity(0);const cfg=codePanel(resources,'showLabelGunPushPullMessages = false','config/sfm-client.toml',{y:-40,width:1470,height:275,fontSize:34,highlighter:tomlHighlighter});resources.add(tx({text:'On by default. Set false to hide routine success confirmations.',y:155,fontSize:28,fill:A.cobalt}));
 yield* d.at(204);d.mark('resources');focus('Resource changes, in place.','4 Other changes  /  recipe paths + matching references + translations + loot');cfg.frame.remove();resources.children().slice(-1)[0].remove();recipe.opacity(1);config.opacity(1);
 config.children()[0].text('data/minecraft');recipe.children()[0].text('Same recipe JSON');yield* waitFor(2);yield* config.children()[0].text('data/sfm',.8);
 resources.add(tx({text:'Recipe IDs + advancement references updated',y:150,fontSize:30,fill:A.cobalt}));
 yield* d.at(218);d.mark('return-to-atlas');focus('One release, traceable from source to behavior.','Source → projection → runtime payload → executed code → world');
 yield* go(920,530,.95,1.7);yield* waitFor(2);jarFiles.opacity(1);yield* go(920,-530,.8,1.5);yield* go(-920,-530,.7,1.3);yield* go(0,0,.4,1.8);title.text('SFM 4.35 · Inside the release');
 yield* d.at(230);d.end();
});
