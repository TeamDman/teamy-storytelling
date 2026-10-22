import {defineConfig} from 'vite';
import {realpathSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import motionCanvas from '@motion-canvas/vite-plugin';
import ffmpeg from '@motion-canvas/ffmpeg';
export default defineConfig({
  plugins:[motionCanvas.default({project:'./src/project-*.ts',output:'./renders'}),ffmpeg.default()],
  server:{host:'127.0.0.1',port:9010,strictPort:true,fs:{allow:[fileURLToPath(new URL('.',import.meta.url)),realpathSync(new URL('./node_modules',import.meta.url))]}},
});
