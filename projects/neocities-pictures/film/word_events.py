#!/usr/bin/env python3
"""One fresh eSpeak process: report word onsets and synthesized PCM digest."""
import ctypes as c, ctypes.util, hashlib, json, os, sys
name=os.environ.get('ESPEAK_LIB') or ctypes.util.find_library('espeak-ng')
if not name and os.environ.get('ESPEAK_DATA_PATH'):
 candidate=os.path.join(os.environ['ESPEAK_DATA_PATH'],'libespeak-ng.so.1')
 if os.path.isfile(candidate):name=candidate
if not name:raise SystemExit('Set ESPEAK_LIB or install eSpeak NG')
lib=c.CDLL(name)
class EventID(c.Union):_fields_=[('number',c.c_int),('name',c.c_char_p),('string',c.c_char*8)]
class Event(c.Structure):_fields_=[('type',c.c_int),('uid',c.c_uint),('pos',c.c_int),('length',c.c_int),('audio_ms',c.c_int),('sample',c.c_int),('user',c.c_void_p),('id',EventID)]
Callback=c.CFUNCTYPE(c.c_int,c.POINTER(c.c_short),c.c_int,c.POINTER(Event));events=[];chunks=[]
@Callback
def receive(wav,n,ev):
 if wav and n:chunks.append(c.string_at(wav,n*2))
 i=0
 while ev[i].type:
  if ev[i].type==1:events.append((ev[i].pos,ev[i].length,ev[i].audio_ms))
  i+=1
 return 0
lib.espeak_Initialize.argtypes=[c.c_int,c.c_int,c.c_char_p,c.c_int];lib.espeak_Initialize.restype=c.c_int
rate=lib.espeak_Initialize(2,0,None,0)
if rate<=0:raise SystemExit('eSpeak initialization failed')
lib.espeak_SetSynthCallback.argtypes=[Callback];lib.espeak_SetSynthCallback(receive)
lib.espeak_SetVoiceByName.argtypes=[c.c_char_p]
if lib.espeak_SetVoiceByName(b'en-us')!=0:raise SystemExit('eSpeak voice unavailable')
for parameter,value in ((1,151),(2,95),(3,43)):lib.espeak_SetParameter(parameter,value,0)
lib.espeak_Synth.argtypes=[c.c_void_p,c.c_size_t,c.c_uint,c.c_int,c.c_uint,c.c_uint,c.POINTER(c.c_uint),c.c_void_p]
text=sys.stdin.read();buf=c.create_string_buffer(text.encode()+b'\0');lib.espeak_Synth(buf,len(buf),0,1,0,1,None,None);lib.espeak_Terminate()
pcm=b''.join(chunks);print(json.dumps({'rate':rate,'bytes':len(pcm),'sha256':hashlib.sha256(pcm).hexdigest(),'events':events}))
