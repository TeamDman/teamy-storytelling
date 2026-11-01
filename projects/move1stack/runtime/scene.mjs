import * as THREE from 'three';
import {linearAt,orbitAt,textureFrameAt,validateCamera} from './timeline.mjs';

// Input is baked geometry and explicit state from the extraction. This module
// neither resolves Minecraft model inheritance nor infers missing scene objects.
export async function loadScene(manifest, baseUrl) {
  if (manifest.schemaVersion!==1) throw new Error('Unsupported extraction schema');
  const scene=new THREE.Scene();
  const materials=new Map(),textures=new Map(),objects=new Map(),animatedAtlases=[];
  for (const spec of manifest.textures) {
    if (textures.has(spec.id)) throw new Error(`Duplicate texture ${spec.id}`);
    const image=await new THREE.ImageLoader().loadAsync(new URL(spec.url,baseUrl).href);
    let texture;
    if (spec.animation) {
      const {frameWidth,frameHeight}=spec;
      if (!Number.isInteger(frameWidth)||!Number.isInteger(frameHeight)||frameWidth<1||frameHeight<1||image.width%frameWidth||image.height%frameHeight) throw new Error(`Invalid atlas grid ${spec.id}`);
      const canvas=document.createElement('canvas');canvas.width=frameWidth;canvas.height=frameHeight;
      texture=new THREE.CanvasTexture(canvas);
      animatedAtlases.push({spec,image,canvas,context:canvas.getContext('2d'),texture,lastFrame:-1,count:(image.width/frameWidth)*(image.height/frameHeight)});
    } else texture=new THREE.Texture(image);
    texture.magFilter=THREE.NearestFilter;texture.minFilter=THREE.NearestFilter;texture.generateMipmaps=!!spec.mipmaps;if(spec.mipmaps)texture.minFilter=THREE.NearestMipmapLinearFilter;
    if (typeof spec.flipY!=='boolean' || typeof spec.srgb!=='boolean') throw new Error(`Texture orientation/color encoding missing: ${spec.id}`);
    texture.flipY=spec.flipY;texture.encoding=spec.srgb?THREE.sRGBEncoding:THREE.LinearEncoding;
    texture.wrapS=wrap(spec.wrapS);texture.wrapT=wrap(spec.wrapT);texture.needsUpdate=true;
    textures.set(spec.id,texture);
  }
  for (const spec of manifest.materials) {
    if (materials.has(spec.id)) throw new Error(`Duplicate material ${spec.id}`);
    for (const flag of ['transparent','depthTest','depthWrite']) if(typeof spec[flag]!=='boolean') throw new Error(`Missing ${flag}: ${spec.id}`);
    const parameters={map:textures.get(spec.texture),transparent:spec.transparent,depthTest:spec.depthTest,depthWrite:spec.depthWrite,
      opacity:spec.opacity,alphaTest:spec.alphaTest,side:side(spec.side),blending:blend(spec.blending),color:spec.color,
      vertexColors:spec.vertexColors,toneMapped:false};
    if (!parameters.map) throw new Error(`Unknown material texture ${spec.texture}`);
    if (![spec.opacity,spec.alphaTest,spec.color].every(Number.isFinite)||typeof spec.vertexColors!=='boolean') throw new Error(`Incomplete material ${spec.id}`);
    materials.set(spec.id,new THREE.MeshBasicMaterial(parameters));
  }
  for (const spec of manifest.meshes) {
    if (objects.has(spec.id)) throw new Error(`Duplicate mesh ${spec.id}`);
    const geometry=new THREE.BufferGeometry();
    if (!Array.isArray(spec.positions)||spec.positions.length%9 || !spec.positions.length) throw new Error(`Invalid triangle positions ${spec.id}`);
    const vertices=spec.positions.length/3;
    if (spec.uvs.length!==vertices*2 || ![...spec.positions,...spec.uvs].every(Number.isFinite)) throw new Error(`Invalid mesh attributes ${spec.id}`);
    geometry.setAttribute('position',new THREE.Float32BufferAttribute(spec.positions,3));
    geometry.setAttribute('uv',new THREE.Float32BufferAttribute(spec.uvs,2));
    if (spec.colors) {
      if (spec.colors.length!==vertices*3||!spec.colors.every(Number.isFinite)) throw new Error(`Invalid colors ${spec.id}`);
      geometry.setAttribute('color',new THREE.Float32BufferAttribute(spec.colors,3));
    }
    const material=materials.get(spec.material);
    if(!material) throw new Error(`Unknown material ${spec.material}`);
    if(material.vertexColors&&!spec.colors)throw new Error(`Missing extracted vertex lighting ${spec.id}`);
    const mesh=new THREE.Mesh(geometry,material);
    if(!Number.isFinite(spec.renderOrder))throw new Error(`Missing render order ${spec.id}`);
    mesh.renderOrder=spec.renderOrder;objects.set(spec.id,mesh);scene.add(mesh);
  }
  const reference=validateCamera(manifest.camera);
  const camera=new THREE.PerspectiveCamera(reference.fovYDegrees,manifest.viewport.width/manifest.viewport.height,reference.near,reference.far);
  function setCamera(pose) {
    camera.position.fromArray(pose.position);camera.up.fromArray(pose.up);camera.lookAt(...pose.target);
    camera.fov=pose.fovYDegrees;camera.updateProjectionMatrix();
  }
  function update(seconds,{orbit=false}={}) {
    setCamera(orbit?orbitAt(seconds,manifest.orbit):reference);
    for(const atlas of animatedAtlases) {
      const anim=atlas.spec.animation;
      const frame=textureFrameAt(seconds,{...anim,interpolate:false},atlas.count);
      if(frame===atlas.lastFrame&&!anim.interpolate)continue;
      const columns=atlas.image.width/atlas.spec.frameWidth;
      atlas.context.clearRect(0,0,atlas.canvas.width,atlas.canvas.height);
      atlas.context.drawImage(atlas.image,(frame%columns)*atlas.canvas.width,Math.floor(frame/columns)*atlas.canvas.height,atlas.canvas.width,atlas.canvas.height,0,0,atlas.canvas.width,atlas.canvas.height);
      if(anim.interpolate){
        // Vanilla interpolates RGB between atlas frames on game ticks. Alpha
        // remains from the current frame; clock phase is not capture evidence.
        const weight=(Math.floor(seconds*20)%anim.frametime)/anim.frametime;
        const next=(frame+1)%atlas.count;
        const current=atlas.context.getImageData(0,0,atlas.canvas.width,atlas.canvas.height);
        atlas.context.clearRect(0,0,atlas.canvas.width,atlas.canvas.height);
        atlas.context.drawImage(atlas.image,0,next*atlas.canvas.height,atlas.canvas.width,atlas.canvas.height,0,0,atlas.canvas.width,atlas.canvas.height);
        const following=atlas.context.getImageData(0,0,atlas.canvas.width,atlas.canvas.height);
        for(let i=0;i<current.data.length;i+=4)for(let c=0;c<3;c++)current.data[i+c]=Math.floor(current.data[i+c]*(1-weight)+following.data[i+c]*weight);
        atlas.context.putImageData(current,0,0);
      }
      atlas.texture.needsUpdate=true;atlas.lastFrame=frame;
    }
    for(const track of manifest.tracks??[]) {
      const registry=track.targetType==='texture'?textures:track.targetType==='mesh'?objects:null;
      if(!registry)throw new Error('Unknown animation target type');
      const target=registry.get(track.target);
      if(!target)throw new Error(`Unknown animation target ${track.target}`);
      const allowed=track.targetType==='texture'?['offset.x','offset.y','rotation']:['rotation.x','rotation.y','rotation.z','position.x','position.y','position.z'];
      if(!allowed.includes(track.property))throw new Error('Unsupported animation property');
      const parts=track.property.split('.');
      if(parts.length===1)target[parts[0]]=linearAt(seconds,track);
      else target[parts[0]][parts[1]]=linearAt(seconds,track);
    }
  }
  update(0);
  return {scene,camera,update,dispose(){for(const mesh of objects.values())mesh.geometry.dispose();for(const material of materials.values())material.dispose();for(const texture of textures.values())texture.dispose();}};
}
function wrap(value){const result={repeat:THREE.RepeatWrapping,clamp:THREE.ClampToEdgeWrapping,mirror:THREE.MirroredRepeatWrapping}[value];if(result===undefined)throw new Error('Missing/unsupported wrap mode');return result;}
function side(value){const result={front:THREE.FrontSide,back:THREE.BackSide,double:THREE.DoubleSide}[value];if(result===undefined)throw new Error('Missing/unsupported face side');return result;}
function blend(value){const result={none:THREE.NoBlending,normal:THREE.NormalBlending,additive:THREE.AdditiveBlending}[value];if(result===undefined)throw new Error('Missing/unsupported blend mode; extract exact custom shader state');return result;}
