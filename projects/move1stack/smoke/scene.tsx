// Synthetic acceptance scene only. No move1stack geometry is inferred here.
import {makeScene2D, Txt} from '@motion-canvas/2d';
import {createSignal, linear, waitFor} from '@motion-canvas/core';
import {BoxGeometry, Mesh, MeshBasicMaterial, PerspectiveCamera, Scene} from 'three';
import {Three} from './Three';

export default makeScene2D(function* (view) {
  const scene = new Scene();
  const camera = new PerspectiveCamera(50, 16 / 9, .05, 100);
  const angle = createSignal(0);
  scene.add(new Mesh(new BoxGeometry(1, 1, 1), [
    0xe96852, 0x815ca0, 0xe5c65d, 0x3777a1, 0x61a58b, 0x4e91cb,
  ].map(color => new MeshBasicMaterial({color}))));
  view.add(new Three({
    size: [640, 360], scene, camera, background: '#182330',
    onRender(renderer, world, lens) {
      // This signal is evaluated by the Motion Canvas render timeline.
      camera.position.set(3 * Math.sin(angle()), 1.8, 3 * Math.cos(angle()));
      camera.lookAt(0, 0, 0);
      renderer.render(world, lens);
    },
  }));
  view.add(<Txt text="SYNTHETIC 3D ACCEPTANCE TEST" y={-150} fill="white" fontSize={16}/>);
  yield* waitFor(.25);
  yield* angle(2 * Math.PI, 3.5, linear);
  yield* waitFor(.25);
});
