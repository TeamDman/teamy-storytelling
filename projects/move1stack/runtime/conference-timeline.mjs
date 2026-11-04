// Presentation timing: the test establishes endpoints, not this motion.
export function transferAt(t) {
 const u=Math.min(1,Math.max(0,(t-11.5)/1.5));
 const eased=u*u*(3-2*u);
 return {visible:t>=10&&t<=15, x:128+592*eased, y:238-60*Math.sin(Math.PI*u), phase:u===0?'source':u===1?'destination':'moving'};
}
