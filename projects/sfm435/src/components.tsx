import {Code,Node,Rect,Txt,Line,lines} from '@motion-canvas/2d';
import {all,createRef,createSignal,easeInOutCubic,linear,waitFor} from '@motion-canvas/core';
import {javaHighlighter} from './highlight';

export const C={bg:'#0b1220',panel:'#142238',line:'#30435e',ink:'#eff3fa',muted:'#a2b2c9',cyan:'#6ad5e9',amber:'#f4c274',green:'#a6dfac',red:'#ff9aa7'};
export const sans='DejaVu Sans';
export const mono='DejaVu Sans Mono';
export const text=(props:any)=><Txt fill={C.ink} fontFamily={sans} fontSize={32} {...props}/>;

export function chrome(view:any,series:string,title:string){
  view.fill(C.bg);
  const titleRef=createRef<Txt>();
  view.add(<Node>
    {text({text:'SFM 4.35',x:-836,y:-480,fontSize:24,fontWeight:700,fill:C.cyan})}
    {text({text:series.toUpperCase(),x:805,y:-480,fontSize:21,fill:C.muted,offsetX:1})}
    <Line points={[[-866,-438],[866,-438]]} stroke={C.line} lineWidth={2}/>
    <Txt ref={titleRef} text={title} x={-866} y={-359} offsetX={-1} fill={C.ink} fontFamily={sans} fontSize={58} fontWeight={700}/>
    <Line points={[[-866,450],[866,450]]} stroke={C.line} lineWidth={2}/>
    {text({text:'Release review  /  Teamy',x:-866,y:486,offsetX:-1,fontSize:22,fill:C.muted})}
    {text({text:'SCHEMATIC • source-derived unless marked tested',x:866,y:486,offsetX:1,fontSize:20,fill:C.muted})}
  </Node>);
  return titleRef;
}

export function panel(parent:Node,x:number,y:number,w:number,h:number,label?:string,color=C.cyan){
  const n=new Rect({x,y,width:w,height:h,radius:22,fill:C.panel,stroke:C.line,lineWidth:2});parent.add(n);
  if(label)n.add(text({text:label,x:-w/2+28,y:-h/2+33,offsetX:-1,fontSize:23,fill:color}));
  return n;
}

export function codePanel(parent:Node,code:string,label:string,opts:any={}){
  const {x=0,y=30,width=1640,height=570,fontSize=32,highlighter=javaHighlighter}=opts;
  const frame=panel(parent,x,y,width,height,label);
  const ref=new Code({code,highlighter,fontFamily:mono,fontSize,lineHeight:fontSize*1.55,fill:C.ink,
    offset:[-1,-1],x:-width/2+38,y:-height/2+84,drawHooks:{token(ctx,token,position,color,selection){ctx.fillStyle=color;ctx.globalAlpha*=.72+.28*selection;ctx.fillText(token,position.x,position.y);}}});
  frame.add(ref);
  return {frame,code:ref};
}

export function* agenda(view:any,items:string[],active:number,seconds=3.5){
  const n=new Rect({width:1920,height:1080,fill:C.bg,opacity:0});view.add(n);
  n.add(text({text:'REVIEW MAP',x:-810,y:-395,offsetX:-1,fontSize:25,fill:C.cyan}));
  n.add(text({text:'SFM 4.35',x:-810,y:-300,offsetX:-1,fontSize:74,fontWeight:700}));
  items.forEach((item,i)=>{
    const y=-165+i*102;
    n.add(<Rect x={0} y={y} width={1660} height={84} radius={12} fill={i===active?C.panel:C.bg} stroke={i===active?C.cyan:C.bg} lineWidth={2}>
      {text({text:String(i).padStart(2,'0'),x:-775,fill:i===active?C.cyan:C.muted,fontSize:28})}
      {text({text:item,x:-698,offsetX:-1,fontSize:34,fill:i===active?C.ink:C.muted})}
      {i===active?text({text:'NOW',x:748,fontSize:20,fill:C.cyan}):null}
    </Rect>);
  });
  yield* n.opacity(1,.3);yield* waitFor(seconds-.6);yield* n.opacity(0,.3);n.remove();
}

export function* demo(view:any,id:'D01baseline'|'D02fixed',subtitle:string,hold=4){
  const bar=createRef<Rect>();const remaining=createSignal(5);
  const n=new Rect({width:1920,height:1080,fill:C.bg,opacity:0});view.add(n);
  n.add(<>
    {text({text:id,x:-800,y:-390,offsetX:-1,fontFamily:mono,fontSize:31,fill:C.cyan})}
    {text({text:'Pause here',x:-800,y:-240,offsetX:-1,fontSize:108,fontWeight:700})}
    {text({text:subtitle,x:-800,y:-95,offsetX:-1,fontSize:43})}
    {text({text:'Run the real Minecraft demo. Resume when ready.',x:-800,y:25,offsetX:-1,fontSize:32,fill:C.muted})}
    {text({text:'Copyable commands and reset steps are in extras.7z.',x:-800,y:105,offsetX:-1,fontSize:28,fill:C.muted})}
    <Rect x={-800} y={285} offsetX={-1} width={1600} height={10} fill={C.line} radius={5}/>
    <Rect ref={bar} x={-800} y={285} offsetX={-1} width={1600} height={10} fill={C.cyan} radius={5}/>
    {text({text:()=>`${Math.max(0,Math.ceil(remaining()))} seconds to pause`,x:-800,y:355,offsetX:-1,fontSize:26,fill:C.cyan})}
    {text({text:'The video continues automatically.',x:800,y:355,offsetX:1,fontSize:26,fill:C.muted})}
  </>);
  yield* n.opacity(1,.3);
  yield* waitFor(hold);
  yield* all(bar().width(0,5,linear),remaining(0,5,linear));
  yield* n.opacity(0,.3);n.remove();
}

export function* select(code:Code,line:number,hold=1.5){yield* code.selection(lines(line),.35);yield* waitFor(hold);}

export function arrow(parent:Node,from:[number,number],to:[number,number],color=C.cyan){
  const a=new Line({points:[from,to],stroke:color,lineWidth:5,endArrow:true,arrowSize:14,end:0});parent.add(a);return a;
}

export function metric(parent:Node,x:number,y:number,label:string,value:string,color=C.cyan){
  const n=panel(parent,x,y,480,190,label,color);
  const v=new Txt({text:value,y:28,fill:C.ink,fontFamily:mono,fontSize:44,fontWeight:700});n.add(v);return {node:n,value:v};
}
