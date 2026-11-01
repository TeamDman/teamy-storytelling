import json,subprocess,sys
from pathlib import Path
root=Path(__file__).parent
results={}
delivery=Path(sys.argv[1]) if len(sys.argv)>1 else root/'deliverable'
for name in ['output.mkv','preview.mp4']:
 p=delivery/name
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]))
 video=data['streams'][0]
 assert len(data['streams'])==1 and video['codec_name']=='h264' and video['pix_fmt']=='yuv420p'
 assert (video['width'],video['height'],video['nb_read_frames'])==(1280,720,'720')
 assert video['r_frame_rate']=='30/1' and abs(float(data['format']['duration'])-24)<.001
 packets=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','packet=pts_time','-of','json',str(p)]))['packets']
 times=sorted(float(x['pts_time']) for x in packets)
 assert len(times)==720
 err=max(abs(t-i/30) for i,t in enumerate(times));assert err<.001
 results[name]={'codec':'h264','pixelFormat':'yuv420p','width':1280,'height':720,'fps':30,'frames':720,'duration':24,'maxTimestampErrorSeconds':err,'fullDecode':'passed','defaultVideo':video['disposition']['default']}
((delivery.parent/'video-validation.json') if len(sys.argv)>1 else (root/'evidence/video-validation.json')).write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
