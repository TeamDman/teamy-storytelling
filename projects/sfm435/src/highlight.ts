import {DependencyContext} from '@motion-canvas/core';
import type {CodeHighlighter,HighlightResult} from '@motion-canvas/2d';
import {createStarryNight} from '@wooorm/starry-night';
import java from '@wooorm/starry-night/lang/source.java.js';
import toml from '@wooorm/starry-night/lang/source.toml.js';
import json from '@wooorm/starry-night/lang/source.json.js';
import onig from 'vscode-oniguruma/release/onig.wasm?url';

// Real installed TextMate grammars feed Motion Canvas Code, including edits.
// Palette maps grammar classes; no hand-authored token spans are used.
const palette:Record<string,string>={
  'pl-k':'#ff8fba','pl-s':'#a5dfa2','pl-c':'#9ba8bc','pl-c1':'#82d6ef',
  'pl-en':'#d6b3ff','pl-e':'#d6b3ff','pl-ent':'#f6ca7e','pl-smi':'#e8edf7',
  'pl-v':'#f6ca7e','pl-pds':'#a5dfa2','pl-s1':'#e8edf7',
};
let engine:any;
const loading=createStarryNight([java,toml,json],{getOnigurumaUrlFetch:()=>new URL(onig,location.href)}).then(x=>{engine=x});
type Token={start:number,end:number,text:string,color:string|null};
export class GrammarHighlighter implements CodeHighlighter<Token[]> {
  constructor(private scope:string){}
  initialize(){if(engine)return true;DependencyContext.collectPromise(loading);return false;}
  prepare(code:string){
    if(!engine)return [];
    const tokens:Token[]=[];let offset=0;
    const visit=(node:any,color:string|null=null)=>{
      for(const cls of node.properties?.className||[])color=palette[cls]||color;
      if(node.type==='text'){
        tokens.push({start:offset,end:offset+node.value.length,text:node.value,color});offset+=node.value.length;
      }else for(const child of node.children||[])visit(child,color);
    };
    visit(engine.highlight(code,this.scope));
    return tokens;
  }
  highlight(index:number,tokens:Token[]):HighlightResult {
    const t=tokens.find(t=>t.start<=index&&index<t.end);
    return {color:t?.color||null,skipAhead:t?Math.max(1,t.end-index):1};
  }
  tokenize(code:string){return this.prepare(code).map(t=>t.text);}
}
export const javaHighlighter=new GrammarHighlighter('source.java');
export const tomlHighlighter=new GrammarHighlighter('source.toml');
export const jsonHighlighter=new GrammarHighlighter('source.json');
