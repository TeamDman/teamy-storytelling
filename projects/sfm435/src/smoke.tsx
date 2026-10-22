import {makeScene2D,Node} from '@motion-canvas/2d';
import {waitFor} from '@motion-canvas/core';
import {chrome,agenda,codePanel,select,demo} from './components';
export default makeScene2D(function*(view){
  chrome(view,'Production components','A local zero is not a global stop');
  const n=new Node({});view.add(n);
  const {code}=codePanel(n,'// Component qualification — not a source excerpt\nif (extracted == 0) {\n    continue;\n}','Java • installed TextMate grammar');
  yield* agenda(view,['Introduction','Routing','Before / after','Release map'],0,3.5);
  yield* select(code,1,1.5);yield* select(code,2,1.5);
  yield* waitFor(1);
  yield* demo(view,'D01baseline','SFM 4.34 • observe the stalled second destination');
});
