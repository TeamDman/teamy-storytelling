import {useThread,waitFor} from '@motion-canvas/core';

export type Cue={id:string,start:number,end?:number,title?:string,chapter?:boolean};
export function director(name:string){
  const timeline:Cue[]=[];
  (globalThis as any).actualTimelines??={};
  (globalThis as any).actualTimelines[name]=timeline;
  return {
    *at(seconds:number){
      const remaining=seconds-useThread().time();
      if(remaining<-.05)throw Error(`Timeline overrun: ${name} wanted ${seconds}, got ${useThread().time()}`);
      yield* waitFor(Math.max(0,remaining));
    },
    mark(id:string,title?:string,chapter=false){
      const start=useThread().time();
      if(timeline.length)timeline[timeline.length-1].end=start;
      timeline.push({id,start,title,chapter});
    },
    end(){if(timeline.length)timeline[timeline.length-1].end=useThread().time();},
  };
}
