import {Node,Rect,Txt} from '@motion-canvas/2d';
import {sans,mono} from './components';
export const inventory={scope:'Captured runtime payloads including GameTests',union:1317,baseline:1282,fixed:1294,categories:[
 {label:'Same bytes',count:1240,color:'#aeb9c6'},
 {label:'Printed instructions/signatures changed',count:10,color:'#4768af'},
 {label:'Printed debug changed with main view equal',count:4,color:'#8c6bac'},
 {label:'Raw change missed by narrow views',count:1,color:'#d1a537'},
 {label:'Changed resource payload',count:4,color:'#4f9585'},
 {label:'Added paths',count:35,color:'#3a9665'},
 {label:'Removed paths',count:23,color:'#b16a78'},
]};
const ranges:Record<string,number[][]>={
 resource_payload_changed:[[1,1],[25,25],[27,27],[72,72]],
 printed_instruction_signature_changed:[[227,227],[399,403],[440,440],[655,655],[835,835],[1006,1006]],
 printed_debug_changed_main_view_equal:[[226,226],[653,654],[656,656]],
 unknown_raw_change_equal_printed_views:[[836,836]],
 added:[[26,26],[421,422],[809,816],[967,968],[1093,1095],[1098,1101],[1103,1105],[1127,1127],[1131,1131],[1138,1140],[1143,1146],[1148,1150]],
 removed:[[1061,1082],[1108,1108]],
};
const categoryColors:Record<string,string>={same_bytes:'#aeb9c6',resource_payload_changed:'#4f9585',printed_instruction_signature_changed:'#4768af',printed_debug_changed_main_view_equal:'#8c6bac',unknown_raw_change_equal_printed_views:'#d1a537',added:'#3a9665',removed:'#b16a78'};
/** Exact producer mapping: lexically sorted relative paths, 44 columns. */
export function payloadGrid(parent:Node,dark=false){
 const ink=dark?'#eef3f9':'#212a35',muted=dark?'#adbdce':'#626e7a';
 const root=new Node({});parent.add(root);
 const tx=(p:any)=><Txt fontFamily={sans} fill={ink} fontSize={28} {...p}/>;
 root.add(tx({text:inventory.scope,x:-780,y:-220,offsetX:-1,fontSize:31,fontWeight:700}));
 root.add(tx({text:'MC 1.21.1 • lexically sorted paths • 44 columns',x:-780,y:-171,offsetX:-1,fontSize:23,fill:muted}));
 const grid=new Node({x:-780,y:-110,cache:true});root.add(grid);
 for(let i=0;i<1317;i++){
  let category='same_bytes';
  for(const [key,rs] of Object.entries(ranges))if(rs.some(([a,b])=>a<=i&&i<=b))category=key;
  grid.add(new Rect({x:(i%44)*13.5,y:Math.floor(i/44)*13.5,width:10,height:10,fill:categoryColors[category]}));
 }
 grid.add(new Rect({x:(1006%44)*13.5,y:Math.floor(1006/44)*13.5,width:23,height:23,stroke:dark?'#f4c274':'#335eb0',lineWidth:3}));
 root.add(tx({text:'1,317',x:450,y:-85,fontFamily:mono,fontSize:70,fontWeight:700}));
 root.add(tx({text:'union paths',x:450,y:-23,fontSize:26,fill:muted}));
 root.add(tx({text:'1,240 same bytes • 77 other paths',x:0,y:45,offsetX:-1,fontSize:25}));
 root.add(tx({text:'Baseline 1,282  /  Fixed 1,294',x:0,y:98,offsetX:-1,fontSize:25,fill:muted}));
 root.add(tx({text:'TILE 1006',x:0,y:166,offsetX:-1,fontSize:22,fill:dark?'#f4c274':'#335eb0'}));
 root.add(tx({text:'ca/teamdman/sfml/ast/\nOutputStatement.class',x:0,y:218,offsetX:-1,fontFamily:mono,fontSize:26,lineHeight:37}));
 root.add(tx({text:'Printed instruction/signature change',x:0,y:282,offsetX:-1,fontSize:23,fill:muted}));
 root.add(tx({text:'Not a shipped release inventory. Printed-view equality is not behavioral equivalence.',x:-780,y:336,offsetX:-1,fontSize:22,fill:muted}));
 return root;
}
