// Creative-flight staging is illustrative: the source test does not capture a player.
export const playerPosition=[2.3,2.2,-2.5]; // feet: above the y=1 command-block top
export const managerCenter=[1.5,2.5,.5];
export const modelScale=.05625;
export function managerPose(){
 const dx=managerCenter[0]-playerPosition[0], dz=managerCenter[2]-playerPosition[2];
 const headY=playerPosition[1]+28*modelScale;
 return {yaw:Math.atan2(-dx,-dz),headPitch:Math.atan2(managerCenter[1]-headY,Math.hypot(dx,dz))};
}
// Sweep stays on the negative-Z command-block side over the complete slice.
export function cameraAngle(t){return -.7-.6*Math.max(0,Math.min(1,t/16));}
export function armSwing(t){return 1.05*Math.max(0,1-Math.abs(t-2.05)/.48);}
