const clamp=(x)=>Math.max(0,Math.min(1,x));
const smooth=(x)=>{const u=clamp(x);return u*u*(3-2*u);};
// The orbit uses the existing world clock. UI and item motion are staged.
export function compositeAt(t){
 const transition=smooth((t-2)/1.2), transfer=smooth((t-10)/2);
 return {scale:1-.6*transition,x:316*transition,y:194*transition,ui:smooth((t-2.5)/.7),editor:t>=6.5,stackX:892-65*Math.sin(Math.PI*transfer),stackY:72+170*transfer};
}
