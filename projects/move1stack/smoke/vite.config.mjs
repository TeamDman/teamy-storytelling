import {defineConfig} from 'vite';
import motionCanvas from '@motion-canvas/vite-plugin';
import ffmpeg from '@motion-canvas/ffmpeg';
export default defineConfig({plugins:[motionCanvas.default({project:'./project.ts',output:'../smoke-media'}),ffmpeg.default()],server:{host:'127.0.0.1',port:9001,strictPort:true}});
