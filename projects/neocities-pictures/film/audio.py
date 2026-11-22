#!/usr/bin/env python3
"""Render local narration, subtitle timings and a scene timeline; no cloud voice."""
import json, os, pathlib, subprocess, wave, textwrap, shutil
here=pathlib.Path(__file__).resolve().parent
out=pathlib.Path(os.environ.get('OUTPUT_DIR',str(here.parent/'output'))); out.mkdir(parents=True,exist_ok=True)
voice=os.environ.get('ESPEAK_BIN') or shutil.which('espeak-ng')
if not voice: raise SystemExit('Set ESPEAK_BIN or install eSpeak NG locally')
env=os.environ.copy()
script=json.loads((here/'script.json').read_text()); timeline=[]; srt=[]; clips=[]; cursor=0.0
def fmt(s):
 ms=round(s*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); sec,ms=divmod(ms,1000); return f'{h:02}:{m:02}:{sec:02},{ms:03}'
for i,item in enumerate(script):
 p=out/f'voice-{i:02}.wav'; subprocess.run([str(voice),'-v','en-us','-s','151','-p','43','-a','95','-w',str(p),item['text']],env=env,check=True)
 with wave.open(str(p),'rb') as w: dur=w.getnframes()/w.getframerate()
 start=cursor; end=start+dur; duration=dur+.65; timeline.append(dict(**item,start=round(start,3),end=round(start+duration,3),voice_end=round(end,3)))
 words=item['text'].split(); count=max(1,(len(words)+9)//10)
 for j in range(count):
  a=len(words)*j//count; b=len(words)*(j+1)//count; part=' '.join(words[a:b]); left=start+dur*j/count; right=start+dur*(j+1)/count
  srt.append(f'{len(srt)+1}\n{fmt(left)} --> {fmt(right)}\n{textwrap.fill(part, width=48)}\n')
 clips.append(f"file '{p}'\nduration {duration:.6f}\n"); cursor+=duration
# Render each clip with its own silence; concatenate without overlapping.
for i,item in enumerate(timeline):
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(out/f'voice-{i:02}.wav'),'-af','apad=pad_dur=0.65','-ar','48000','-ac','1',str(out/f'clip-{i:02}.wav')],check=True)
(out/'concat.txt').write_text(''.join(f"file 'clip-{i:02}.wav'\n" for i in range(len(timeline))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-c:a','pcm_s16le',str(out/'narration.wav')],check=True)
(out/'captions.srt').write_text('\n'.join(srt)); (out/'timeline.json').write_text(json.dumps(timeline,indent=2)); print('Duration',round(cursor,2),'seconds')
