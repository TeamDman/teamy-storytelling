import {makeScene2D,Node,Rect,Txt,Line,Circle,Code,lines} from '@motion-canvas/2d';
import {all,createSignal,waitFor,linear,Vector2} from '@motion-canvas/core';
import {C,sans,mono,text,chrome,panel,arrow,agenda,codePanel} from './components';
import {tomlHighlighter} from './highlight';
import {director} from './director';
import {payloadGrid} from './payload';
import {inputExcerpt,baselineExcerpt,fixedExcerpt,extractionExcerpt,insertionExcerpt,sourceLabel} from './evidence';

const items=['Introduction','The route','Two droppers','Other changes','Source to release'];
const fmt=(v:number)=>Math.round(v).toLocaleString('en-US');

function dock(view:any,active:()=>number){
  const n=new Node({y:410});view.add(n);
  items.forEach((label,i)=>n.add(<Node x={-690+i*345}>
    <Circle size={15} fill={()=>active()===i?C.cyan:C.line}/>
    {text({text:`${i}  ${label}`,x:21,y:0,offsetX:-1,fontSize:20,fill:()=>active()===i?C.ink:C.muted})}
  </Node>));return n;
}
function tile(parent:Node,x:number,y:number,w:number,h:number,label:string,value:string,color=C.cyan){
  const n=panel(parent,x,y,w,h,label,color);const v=new Txt({text:value,fontFamily:sans,fontSize:34,fontWeight:700,fill:C.ink,y:20});n.add(v);return {n,v};
}
function* reveal(n:Node){yield* all(n.opacity(1,.6),n.y(n.y()-12,.6));}
function route(parent:Node){
  const g=new Node({});parent.add(g);
  const a=createSignal(99975),b=createSignal(0);
  // Physical storage stays at left. Ticket is selection/control flow only.
  const source=panel(g,-680,90,280,270,'ENERGY SOURCE',C.amber);
  source.add(<>
    <Rect y={13} width={120} height={123} radius={10} stroke={C.amber} lineWidth={4}/>
    <Rect y={27} width={98} height={88} fill={C.amber} radius={5}/>
    {text({text:'Mekanism',y:99,fontSize:23,fill:C.amber})}
  </>);
  const ticket=panel(g,-220,-130,360,155,'SOURCE RECORD',C.cyan);
  ticket.add(text({text:'selection + constraints',y:21,fontSize:25}));
  const d1=panel(g,540,-70,380,210,'FIRST DROPPER');
  const d2=panel(g,540,200,380,210,'SECOND DROPPER');
  [d1,d2].forEach((d,i)=>d.add(<>
    {text({text:()=>fmt(i===0?a():b()),y:10,fontFamily:mono,fontSize:51,fontWeight:700})}
    {text({text:'/ 100,000 FE',y:68,fontFamily:mono,fontSize:22,fill:C.muted})}
  </>));
  const line1=new Line({points:[[-40,-130],[190,-130],[190,-70],[345,-70]],stroke:C.cyan,lineWidth:4,lineDash:[12,10],endArrow:true,arrowSize:13});
  const line2=new Line({points:[[190,-130],[190,200],[345,200]],stroke:C.cyan,lineWidth:4,lineDash:[12,10],endArrow:true,arrowSize:13});
  g.add([line1,line2]);line1.moveToBottom();line2.moveToBottom();
  const actual=new Line({points:[[-536,160],[-440,160],[-440,312],[785,312],[785,200],[735,200]],stroke:C.amber,lineWidth:5,endArrow:true,arrowSize:14,end:0});g.add(actual);actual.moveToBottom();
  const stamp=new Rect({x:-220,y:-130,width:335,height:115,fill:'#592e36',stroke:C.red,lineWidth:3,radius:13,opacity:0,rotation:-8});
  stamp.add(text({text:'SOURCE RECORD\nDONE',textAlign:'center',fontSize:30,fontWeight:700,fill:C.red}));g.add(stamp);
  const gate=new Line({points:[[295,-108],[295,-33]],stroke:C.red,lineWidth:9,opacity:0});g.add(gate);
  const callout=new Txt({text:'Dashed cyan: control flow',x:-300,y:340,fontSize:24,fill:C.cyan,fontFamily:sans});g.add(callout);
  return {g,a,b,source,ticket,d1,d2,line1,line2,actual,stamp,gate,callout};
}
function* pause(view:any,id:string,title:string,expected:string){
  const n=new Rect({x:-280,y:75,width:1180,height:565,radius:26,fill:'#0c1828',stroke:C.cyan,lineWidth:3,opacity:0});view.add(n);
  const remaining=createSignal(5);const bar=new Rect({x:-570,y:200,width:1140,height:9,offsetX:-1,fill:C.cyan,radius:4});
  n.add(<>
    {text({text:id,x:-560,y:-217,offsetX:-1,fontFamily:mono,fontSize:26,fill:C.cyan})}
    {text({text:'Pause here',x:-560,y:-136,offsetX:-1,fontSize:66,fontWeight:700})}
    {text({text:title,x:-560,y:-48,offsetX:-1,fontSize:36})}
    {text({text:expected,x:-560,y:23,offsetX:-1,fontSize:27,fill:C.amber})}
    {text({text:'Expected from automated characterization',x:-560,y:81,offsetX:-1,fontSize:22,fill:C.muted})}
    {text({text:'Local preparation required • commands in extras.7z',x:-560,y:132,offsetX:-1,fontSize:26})}
    {text({text:()=>`${Math.max(0,Math.ceil(remaining()))}s • playback continues automatically`,x:-560,y:239,offsetX:-1,fontSize:21,fill:C.muted})}
  </>);n.add(bar);
  yield* n.opacity(1,.4);yield* waitFor(4);yield* all(bar.width(0,5,linear),remaining(0,5,linear));yield* waitFor(1.2);yield* n.opacity(0,.4);n.remove();
}

export default makeScene2D(function*(view){
  const d=director('route');d.mark('intro','0 · Introduction',true);
  const title=chrome(view,'Keep the route open','Keep the route open');
  const chapter=createSignal(0);const rail=dock(view,chapter);
  const world=new Node({});view.add(world);world.moveToBottom();
  const r=route(world);r.g.opacity(0);
  yield* agenda(view,items,0,4);
  const intro=new Node({});view.add(intro);
  intro.add(text({text:'One small scope change.\nOne more destination reached.',fontSize:66,fontWeight:700,x:-800,y:-30,offsetX:-1,lineHeight:88}));
  yield* waitFor(3);yield* intro.opacity(0,.8);intro.remove();
  yield* d.at(10);d.mark('route','1 · The route',true);chapter(1);
  title().text('One source. More than one destination.');
  yield* agenda(view,items,1,2);yield* r.g.opacity(1,.7);
  r.callout.text('This trigger • one record, independent destination checks');
  yield* d.at(20);d.mark('input');title().text('INPUT registers. OUTPUT transfers.');
  yield* all(r.g.scale(.78,.6),r.g.position([150,90],.6));
  const input=panel(world,-610,-130,420,200,'INPUT',C.cyan);input.opacity(0);
  input.add(text({text:'Source + constraints\nNo energy extracted yet',fontSize:26,lineHeight:44,textAlign:'center',y:20}));
  input.remove();r.g.scale(.58);r.g.position([420,180]);r.ticket.opacity(0);
  const inputCode=codePanel(world,inputExcerpt,'InputStatement.java 57–67 • … = omitted source',{x:-380,y:-86,width:990,height:345,fontSize:28});
  yield* inputCode.code.selection(lines(2),.5);yield* r.ticket.opacity(1,.7);r.callout.text('INPUT creates a record; it does not hold energy.');
  yield* d.at(30);d.mark('output-order');title().text('OUTPUT does the work.');
  inputCode.frame.remove();r.callout.text('OUTPUT checks, simulates, then performs the transfer.');yield* all(r.g.scale(.78,.4),r.g.position([150,90],.4));
  const steps=new Node({y:-233});world.add(steps);
  const labels=['Read source','Simulate acceptance','Apply limits','Extract','Insert returned'];
  const boxes:Rect[]=[];
  labels.forEach((t,i)=>{const p=new Rect({x:-676+i*338,width:310,height:90,radius:14,stroke:i<3?C.cyan:C.amber,lineWidth:2,fill:C.bg});p.add(text({text:t,fontSize:23,fill:i<3?C.cyan:C.amber}));steps.add(p);boxes.push(p);});
  for(let i=0;i<5;i++){yield* boxes[i].fill(i<3?'#254357':'#57462e',.3);if(i===3){const parcel=new Rect({x:-400,y:100,size:26,radius:5,fill:C.amber});world.add(parcel);yield* parcel.position([565,45],1.4);parcel.remove();}else yield* waitFor(1.4);}
  r.callout.text('Only extraction withdraws energy. Insert the amount returned.');
  const actualCode=codePanel(world,extractionExcerpt,'OutputStatement.java 309–310 • earlier checks omitted',{x:0,y:90,width:1640,height:235,fontSize:30});r.g.opacity(.15);yield* actualCode.code.selection(lines(1),.3);yield* waitFor(1.3);actualCode.frame.remove();r.g.opacity(1);
  yield* d.at(44);d.mark('conversion-25');title().text('25 FE requested. 24 FE delivered.');
  steps.remove();yield* all(r.g.opacity(0,.5),r.g.scale(.68,.5));
  const math=new Node({});world.add(math);
  const cells=[['REQUEST','25 FE'],['SIMULATE','62 J'],['RETURN','24 FE'],['WITHDRAW','60 J'],['DELIVER','24 FE']];
  const mathNodes:any[]=[];
  cells.forEach(([label,value],i)=>{const o=tile(math,-680+i*340,-45,305,190,label,value,i<3?C.cyan:C.amber);o.n.opacity(0);mathNodes.push(o);if(i<4)arrow(math,[-520+i*340,-45],[-505+i*340,-45],C.muted).end(1);});
  for(const cell of mathNodes){yield* cell.n.opacity(1,.45);yield* waitFor(.7);}
  math.add(text({text:'Mekanism default: 2.5 J / FE • integer conversion',y:130,fontSize:29,fill:C.muted}));
  math.add(text({text:'60 J withdrawn = 24 FE delivered',y:210,fontSize:42,fontWeight:700,fill:C.amber}));
  math.add(text({text:'62 J is simulated. No energy is destroyed.',y:282,fontSize:30}));
  yield* d.at(58);d.mark('conversion-1');title().text('1 FE requested. Nothing withdrawn.');
  const vals=['1 FE','2 J','0 FE','0 J','0 FE'];
  for(let i=0;i<5;i++)mathNodes[i].v.text(vals[i]);
  math.children().slice(-2).forEach(n=>n.remove());
  math.add(text({text:'Zero transfer. Source still usable.',y:210,fontSize:44,fontWeight:700,fill:C.cyan}));
  math.add(text({text:'A local zero does not prove the source is empty.',y:282,fontSize:30}));
  yield* d.at(70);d.mark('fixture','2 · Two droppers',true);chapter(2);math.remove();
  title().text('Two droppers. Two pulses.');
  yield* agenda(view,items,2,2);yield* all(r.g.opacity(1,.6),r.g.scale(1,.6),r.g.position([0,0],.6));
  r.callout.text('Setup  •  first 99,975 / 100,000  •  second 0');
  yield* waitFor(1.4);r.callout.text('Pulse 1');yield* all(r.a(99999,1.2),r.b(100000,1.2));yield* waitFor(2);
  r.callout.text('Separate working drain • first idle • only the second drains');yield* r.b(0,1.2);yield* waitFor(1.5);
  yield* d.at(84);d.mark('D01baseline');title().text('Live demo • SFM 4.34');
  r.callout.opacity(0);yield* pause(view,'D01baseline','SFM 4.34 • run the next pulse','Expected: first 99,999  •  second 0');
  r.callout.opacity(1);yield* d.at(96);d.mark('baseline-scope');title().text('4.34 ends the source route too early.');
  r.callout.text('First wants 1 FE → extraction returns 0');yield* waitFor(3);
  yield* r.stamp.opacity(1,.5);yield* r.line2.end(0,.8);r.callout.text('source.setDone() • second skipped for this trigger');
  yield* waitFor(4);r.callout.text('The source record is done. The physical source still holds energy.');
  yield* d.at(110);d.mark('scope-comparison');title().text('Keep the source record.');
  yield* all(r.g.scale(.52,.6),r.g.position([350,140],.6));
  const comp=new Node({});world.add(comp);
  const scopeCode=codePanel(comp,baselineExcerpt,'4.34 • OutputStatement.java 315–320 • … = omitted source',{x:-305,y:-80,width:1100,height:455,fontSize:29});
  r.g.scale(.4);r.g.position([570,170]);
  comp.add(text({text:'Source records reset every trigger.',x:-800,y:240,offsetX:-1,fontSize:31}));
  comp.add(text({text:'Rendered Java from tested projections • 8e349578',x:-800,y:305,offsetX:-1,fontSize:23,fill:C.muted}));
  yield* scopeCode.code.selection(lines(2),.4);yield* waitFor(4.2);
  yield* scopeCode.code.code(fixedExcerpt,.8);scopeCode.frame.children()[0].text('4.35 • same branch • only this destination is skipped');
  yield* scopeCode.code.selection(lines(2),.4);yield* all(r.stamp.opacity(0,.6),r.line2.end(1,.6),r.gate.opacity(1,.6));r.callout.text('4.35 • source record retained');
  yield* d.at(124);d.mark('fixed-route');title().text('4.35 skips this stop, then continues.');
  comp.remove();yield* all(r.g.scale(1,.6),r.g.position([0,0],.6));
  r.callout.text('First: zero extraction • close only this destination exit');yield* waitFor(2);
  yield* r.actual.end(1,1.2);yield* r.b(100000,1.5);r.callout.text('Source record retained • second receives 100,000 FE');
  yield* waitFor(2);r.callout.text('First remains 99,999. The last 1 FE gap is unchanged.');
  yield* d.at(136);d.mark('D02fixed');title().text('Live demo • SFM 4.35');
  r.callout.opacity(0);yield* pause(view,'D02fixed','Same setup. Same sequence.','Expected: first 99,999  •  second 100,000');
  r.callout.opacity(1);yield* d.at(148);d.mark('test-evidence');title().text('Two tests. Two expected results.');
  yield* r.g.opacity(0,.5);
  const receipts=new Node({});world.add(receipts);
  tile(receipts,-440,-15,770,280,'4.34 · AUTOMATED CHARACTERIZATION','PASS  /  Bug reproduced',C.green);
  tile(receipts,440,-15,770,280,'4.35 · AUTOMATED CHARACTERIZATION','PASS  /  Intended behavior',C.green);
  receipts.add(text({text:'Full manual two-button walkthrough: not yet verified.',y:245,fontSize:30,fill:C.muted}));
  yield* d.at(160);d.mark('label-gun','3 · Other changes',true);chapter(3);receipts.remove();
  title().text('Quieter Label Gun confirmations.');yield* agenda(view,items,3,2);
  const label=new Node({});world.add(label);
  const cfg=codePanel(label,'showLabelGunPushPullMessages = false','config/sfm-client.toml • TOML',{y:-100,width:1640,height:210,fontSize:38,highlighter:tomlHighlighter});
  const bubble=panel(label,360,140,730,95,'');bubble.add(text({text:'Routine push/pull success',fontSize:29}));
  label.add(text({text:'On by default.',x:-800,y:125,offsetX:-1,fontSize:34,fill:C.cyan}));
  yield* waitFor(2);yield* bubble.opacity(0,.8);
  label.add(text({text:'Hides routine push/pull success messages.',x:-800,y:282,offsetX:-1,fontSize:36}));
  yield* d.at(172);d.mark('listener');title().text('Watch the far position.');label.remove();
  const listener=new Node({});world.add(listener);
  const relay=tile(listener,-585,20,400,230,'RETAINED','Relay block entity');
  const pos=tile(listener,400,20,600,230,'FAR POSITION','Position-level listener');
  const ring=new Circle({x:400,y:20,width:650,height:285,stroke:C.cyan,lineWidth:4,lineDash:[14,12]});listener.add(ring);
  const cap=new Rect({x:400,y:200,width:340,height:70,radius:12,fill:C.line});cap.add(text({text:'Capability object A',fontSize:23}));listener.add(cap);
  arrow(listener,[85,20],[-380,20],C.cyan).end(1);
  listener.add(text({text:'NeoForge 1.20.3+ • listener stays anchored to coordinates',y:-205,fontSize:32,fill:C.cyan}));
  yield* waitFor(3);yield* cap.opacity(0,.5);cap.children()[0].remove();cap.add(text({text:'Capability object B',fontSize:23}));yield* cap.opacity(1,.5);
  listener.add(text({text:'Invalidation reaches the retained relay.',y:310,fontSize:35}));
  yield* d.at(184);d.mark('resources');title().text('Resources, references, polish.');listener.remove();
  const resources=new Node({});world.add(resources);
  const folder=tile(resources,-485,-55,650,290,'RECIPE PATH','data/minecraft',C.amber);
  const content=tile(resources,400,-55,650,290,'CONTENT','Same recipe JSON',C.green);
  resources.add(text({text:'Recipe IDs + advancement references change',y:180,fontSize:33,fill:C.cyan}));
  yield* waitFor(2);yield* folder.v.text('data/sfm',.8);
  const polish=['French','Brazilian Portuguese','Buffer itemless loot'];
  polish.forEach((s,i)=>tile(resources,-560+i*560,302,510,86,'',s,C.muted).v.fontSize(25));
  yield* d.at(196);d.mark('projections','4 · Source to release',true);chapter(4);resources.remove();
  title().text('One authored source. Explicit projections.');yield* agenda(view,items,4,2);
  const projection=new Node({});world.add(projection);
  tile(projection,-620,-20,420,250,'AUTHOR','Liquid core',C.cyan);
  tile(projection,-80,-20,430,250,'SELECT','Projection config',C.amber);
  arrow(projection,[-398,-20],[-308,-20]).end(1);
  const outputs=['Java','Resources','Build files'];
  outputs.forEach((s,i)=>{tile(projection,570,-165+i*174,450,134,'GENERATE',s,C.green);arrow(projection,[150,-20],[332,-165+i*174]).end(1)});
  projection.add(text({text:'Replaces source maintenance on one branch per Minecraft version.',y:305,fontSize:27}));
  projection.add(text({text:'Git branches still exist.',y:354,fontSize:24,fill:C.muted}));
  yield* d.at(210);d.mark('release-inspection');title().text('Inspect the captured runtime payload.');projection.remove();
  const inspect=new Node({});world.add(inspect);
  payloadGrid(inspect,true);
  yield* waitFor(4);yield* inspect.opacity(0,.6);inspect.remove();
  title().text('SFM 4.35 • Keep the route open');yield* all(r.g.opacity(1,.6),r.gate.opacity(1,.6));r.callout.text('Skip the local zero. Keep the next destination eligible.');
  yield* d.at(224);d.end();
});
