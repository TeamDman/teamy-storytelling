#!/usr/bin/env python3
"""Present a static reconstructed legacy player beside the SFM editor and orbit."""
import hashlib
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/conference-slice-11'
MODEL = ROOT / 'previews/conference-slice-10/player.png'
ORBIT = ROOT / 'deliverable/output.mkv'
EDITOR = ROOT / 'previews/conference-slice-05/editor.png'
SKIN = ROOT / '.inputs/skin.png'
EXPECTED = {
    ORBIT: 'ffe2d3f7f68c67de44e0439c6ffdf4e512f79c0ed93a651b6d83f6345908c3b5',
    EDITOR: '1b6250d2e2c796977412003bf9332dd1389a7370c1e442ba3a0c2dce97ac5a41',
    SKIN: 'dc6d27c115e71009ced5a2bc41a24e918b45edf5a584e639ec56b832126d2635',
}


def main():
    for path, expected in EXPECTED.items():
        with path.open('rb') as f:
            if hashlib.file_digest(f, 'sha256').hexdigest() != expected:
                raise SystemExit(f'Input hash mismatch: {path}')
    subprocess.run([sys.executable, str(ROOT / 'conference-preview/verify_skin_model.py')], check=True)
    if any((OUT / name).exists() for name in ('background.png','output.mkv','preview.mp4')):
        raise SystemExit('Output exists; preserve it and choose a new directory')
    OUT.mkdir(parents=True, exist_ok=True)
    model = MODEL
    if not model.exists():
        raise SystemExit('Render the player model before composing this slice')
    bg = Image.open(EDITOR).convert('RGB')
    draw = ImageDraw.Draw(bg)
    draw.rectangle((925,35,1235,254), fill='black')
    draw.rectangle((1236,35,1238,254), fill='white')
    draw.rectangle((1239,35,1260,254), fill='#272727')
    draw.rectangle((956,47,1214,193), fill='#142434', outline='#90adbd', width=2)
    background = OUT / 'background.png'
    bg.save(background)
    graph = (
        '[0:v]trim=duration=9,settb=expr=1/30,setpts=N[bg];'
        '[1:v]trim=start=10:duration=9,settb=expr=1/30,setpts=N,scale=250:140[world];'
        '[bg][world]overlay=960:50:shortest=1[base];'
        '[2:v]trim=duration=9,settb=expr=1/30,setpts=N,scale=430:550,format=rgba,fade=t=in:st=1:d=1:alpha=1[skin];'
        '[base][skin]overlay=350:75:shortest=1,format=yuv420p[v]'
    )
    video, preview = OUT / 'output.mkv', OUT / 'preview.mp4'
    subprocess.run(['ffmpeg','-v','error','-loop','1','-framerate','30','-i',str(background),
                    '-i',str(ORBIT),'-loop','1','-framerate','30','-i',str(model),
                    '-filter_complex',graph,'-map','[v]','-t','9','-r','30',
                    '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
                    '-metadata','title=SFM conference slice 11','-n',str(video)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-c','copy',
                    '-movflags','+faststart','-n',str(preview)],check=True)
    print(f'Created {video} and {preview}')


if __name__ == '__main__':
    main()
