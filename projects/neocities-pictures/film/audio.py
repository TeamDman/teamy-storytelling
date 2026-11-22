#!/usr/bin/env python3
"""Generate offline eSpeak narration and shared, word-event-aligned captions."""
import array, hashlib, json, os, pathlib, re, shutil, subprocess, sys, textwrap, wave
here=pathlib.Path(__file__).resolve().parent
out=pathlib.Path(os.environ.get('OUTPUT_DIR',str(here.parent/'output')));out.mkdir(parents=True,exist_ok=True)
voice=os.environ.get('ESPEAK_BIN') or shutil.which('espeak-ng')
if not voice:raise SystemExit('Set ESPEAK_BIN or install eSpeak NG locally')
script=json.loads((here/'script.json').read_text());timeline=[];srt=[];cursor=0.0;interpolated=0

def fmt(seconds):
 ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{sec:02},{ms:03}'
def event_time(position):
 global interpolated
 exact=[e[2] for e in events if e[0]==position]
 if exact:return min(exact)/1000
 before=[e for e in events if e[0]<position];after=[e for e in events if e[0]>position]
 interpolated+=1
 if before and after:
  lo=max(before,key=lambda e:e[0]);hi=min(after,key=lambda e:e[0]);return (lo[2]+(hi[2]-lo[2])*(position-lo[0])/(hi[0]-lo[0]))/1000
 return (min(after,key=lambda e:e[0])[2] if after else max(before,key=lambda e:e[0])[2])/1000
for i,item in enumerate(script):
 text=item['text']
 if not text.isascii(): raise SystemExit('Word-event mapping requires ASCII narration; use plain punctuation')
 p=out/f'voice-{i:02}.wav'
 subprocess.run([str(voice),'-v','en-us','-s','151','-p','43','-a','95','-w',str(p),text],check=True)
 with wave.open(str(p),'rb') as w:
  params=w.getparams();raw=w.readframes(w.getnframes())
 result=json.loads(subprocess.run([sys.executable,str(here/'word_events.py')],input=text,text=True,capture_output=True,check=True).stdout);rate=result['rate'];events=result['events'];generated_bytes=result['bytes']
 if params.nchannels!=1 or params.sampwidth!=2 or params.framerate!=rate:raise SystemExit('Unexpected eSpeak output format')
 if not generated_bytes or hashlib.sha256(raw[:generated_bytes]).hexdigest()!=result['sha256']:raise SystemExit(f'Word-event PCM did not match voice file for segment {i}')
 samples=array.array('h');samples.frombytes(raw)
 last=next((n for n in range(len(samples)-1,-1,-1) if abs(samples[n])>64),0)
 keep=min(len(samples),last+1+round(rate*.18));trimmed=raw[:keep*2]
 with wave.open(str(p),'wb') as w:w.setparams(params);w.writeframes(trimmed)
 dur=keep/rate;start=cursor;end=start+dur;duration=dur+.35
 words=list(re.finditer(r'\S+',text));groups=[];group=[];chars=0
 for word in words:
  token=word.group();extra=len(token)+(1 if group else 0)
  if group and (len(group)>=7 or chars+extra>70):groups.append(group);group=[];chars=0;extra=len(token)
  group.append(word);chars+=extra
  if len(group)>=3 and re.search(r'[.!?]$',token):groups.append(group);group=[];chars=0
 if group:groups.append(group)
 starts=[start]
 for group in groups[1:]:starts.append(start+max(0,event_time(group[0].start()+1)-.08))
 if any(starts[j]<=starts[j-1] for j in range(1,len(starts))) or starts[-1]>=end:raise SystemExit(f'Invalid word-event cue ordering in segment {i}')
 cues=[]
 for j,group in enumerate(groups):
  cue={'start':round(starts[j],3),'end':round(starts[j+1] if j+1<len(starts) else end,3),'text':' '.join(w.group() for w in group)};cues.append(cue)
  srt.append(f"{len(srt)+1}\n{fmt(cue['start'])} --> {fmt(cue['end'])}\n{textwrap.fill(cue['text'],width=39)}\n")
 timeline.append(dict(**item,start=round(start,3),end=round(start+duration,3),voice_end=round(end,3),cues=cues));cursor+=duration
for i in range(len(timeline)):
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(out/f'voice-{i:02}.wav'),'-af','apad=pad_dur=0.35','-ar','48000','-ac','1',str(out/f'clip-{i:02}.wav')],check=True)
(out/'concat.txt').write_text(''.join(f"file 'clip-{i:02}.wav'\n" for i in range(len(timeline))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-c:a','pcm_s16le',str(out/'narration.wav')],check=True)
(out/'captions.srt').write_text('\n'.join(srt));(out/'timeline.json').write_text(json.dumps(timeline,indent=2));print('Duration',round(cursor,2),'seconds;',len(srt),'word-aligned cues;',interpolated,'interpolated onsets; matching PCM verified')
