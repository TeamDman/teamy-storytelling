// Pure timestamp evaluation: no performance.now(), timers or accumulated deltas.
const finite = (value, label) => {
  if (!Number.isFinite(value)) throw new Error(`${label} must be finite`);
  return value;
};
export function vector3(value, label) {
  if (!Array.isArray(value) || value.length !== 3) throw new Error(`${label} must have 3 components`);
  return value.map((x, i) => finite(x, `${label}[${i}]`));
}
export function orbitAt(seconds, orbit) {
  finite(seconds, 'seconds');
  const center=vector3(orbit.center,'orbit.center');
  const target=vector3(orbit.target,'orbit.target');
  const radius=finite(orbit.radius,'orbit.radius');
  if (radius <= 0) throw new Error('orbit.radius must be positive');
  const angle=finite(orbit.startRadians,'orbit.startRadians') +
    finite(orbit.radiansPerSecond,'orbit.radiansPerSecond') * seconds;
  return {
    position:[center[0]+radius*Math.sin(angle),center[1]+finite(orbit.height,'orbit.height'),center[2]+radius*Math.cos(angle)],
    target, up:vector3(orbit.up,'orbit.up'), fovYDegrees:finite(orbit.fovYDegrees,'orbit.fovYDegrees'),
  };
}
export function linearAt(seconds, track) {
  finite(seconds,'seconds');
  return finite(track.initial,'track.initial') +
    finite(track.unitsPerSecond,'track.unitsPerSecond') * seconds;
}
export function textureFrameAt(seconds, animation, atlasFrameCount) {
  finite(seconds,'seconds');
  const ticksPerSecond=finite(animation.ticksPerSecond,'animation.ticksPerSecond');
  if (ticksPerSecond<=0) throw new Error('ticksPerSecond must be positive');
  if (!Number.isInteger(atlasFrameCount) || atlasFrameCount<1) throw new Error('invalid atlas frame count');
  if (animation.interpolate) throw new Error('Interpolated Minecraft atlas needs a verified shader; unsupported');
  const defaultTime=animation.frametime ?? 1;
  const entries=animation.frames?.length ? animation.frames : Array.from({length:atlasFrameCount},(_,index)=>index);
  const frames=entries.map(entry=>typeof entry==='number'?{index:entry,time:defaultTime}:{index:entry.index,time:entry.time??defaultTime});
  for (const frame of frames) {
    if (!Number.isInteger(frame.index) || frame.index<0 || frame.index>=atlasFrameCount) throw new Error('frame index out of range');
    if (!Number.isInteger(frame.time) || frame.time<1) throw new Error('frame duration must be positive integer ticks');
  }
  const total=frames.reduce((sum,frame)=>sum+frame.time,0);
  let tick=((seconds*ticksPerSecond)%total+total)%total;
  for (const frame of frames) {
    if (tick<frame.time) return frame.index;
    tick-=frame.time;
  }
  return frames[0].index;
}
export function validateCamera(camera) {
  const position=vector3(camera.position,'camera.position');
  const target=vector3(camera.target,'camera.target');
  const up=vector3(camera.up,'camera.up');
  const fov=finite(camera.fovYDegrees,'camera.fovYDegrees');
  const near=finite(camera.near,'camera.near'),far=finite(camera.far,'camera.far');
  if (!(fov>0 && fov<180 && near>0 && far>near)) throw new Error('invalid projection');
  const direction=target.map((v,i)=>v-position[i]);
  const cross=[direction[1]*up[2]-direction[2]*up[1],direction[2]*up[0]-direction[0]*up[2],direction[0]*up[1]-direction[1]*up[0]];
  if (Math.hypot(...cross)<1e-10) throw new Error('camera target and up must define an orientation');
  return {position,target,up,fovYDegrees:fov,near,far};
}
