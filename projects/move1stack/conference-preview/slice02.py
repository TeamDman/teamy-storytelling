#!/usr/bin/env python3
"""Short manager-screen study using pinned SFM textures and layout geometry.

This is a reconstruction, not a Minecraft screenshot: widget skins, font,
inventory contents and screen state are approximations. The screen structure,
texture, disk icon, button text and positions are derived from pinned sources.
"""
import hashlib
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews' / 'conference-slice-02'
MANAGER = ROOT / '.inputs/sfm-gui/manager.png'
DISK = ROOT / '.inputs/sfm-gui/disk.png'
ORBIT = ROOT / 'deliverable/output.mkv'
EXPECTED = {
    MANAGER: 'b6945789f1b663261a0c3bc6f922052a41f827cbd966e5014cadbc188eb7dea0',
    DISK: '049bca9a9be439beca5979e8af504bb3c822eb06dbf390927de9f490ce0514e1',
    ORBIT: 'ffe2d3f7f68c67de44e0439c6ffdf4e512f79c0ed93a651b6d83f6345908c3b5',
}
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def digest(path):
    with path.open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def main():
    for path, expected in EXPECTED.items():
        if digest(path) != expected:
            raise SystemExit(f'Input hash mismatch: {path}')
    if any((OUT / name).exists() for name in ('output.mkv', 'preview.mp4', 'layout.png')):
        raise SystemExit('Preview exists; preserve it and choose a new output directory.')
    OUT.mkdir(parents=True, exist_ok=True)

    # ManagerScreen positions relative to the 176x166 background, including
    # the 120x16 left buttons. The original Minecraft widget sprites/font are
    # not part of the source bundle, so draw an explicitly approximate skin.
    gui = Image.new('RGBA', (296, 192), (0, 0, 0, 0))
    background = Image.open(MANAGER).convert('RGBA').crop((0, 0, 176, 166))
    gui.alpha_composite(background, (120, 0))
    gui.alpha_composite(Image.open(DISK).convert('RGBA'), (135, 47))
    gd = ImageDraw.Draw(gui)
    f = ImageFont.truetype(FONT, 7)
    gd.text((128, 6), 'Manager', font=f, fill='#404040')
    gd.text((128, 20), 'State: running', font=f, fill='#404040')
    gd.text((128, 72), 'Inventory', font=f, fill='#404040')
    buttons = [
        (0, 16, 120, 16, 'Paste from clipboard'),
        (0, 66, 120, 16, 'Edit'),
        (0, 82, 120, 16, 'View examples'),
        (0, 112, 120, 16, 'Discord'),
        (0, 128, 120, 16, 'Copy to clipboard'),
        (0, 144, 120, 16, 'View logs'),
        (0, 160, 120, 16, 'Rebuild cable network'),
        (0, 176, 120, 16, 'View server config'),
        (240, 10, 50, 12, 'Reset'),
    ]
    for x, y, w, h, label in buttons:
        gd.rectangle((x, y, x+w-1, y+h-1), fill='#494949', outline='#171717')
        gd.line((x+1, y+1, x+w-2, y+1), fill='#dddddd')
        gd.line((x+1, y+1, x+1, y+h-2), fill='#dddddd')
        gd.line((x+1, y+h-2, x+w-2, y+h-2), fill='#262626')
        gd.rectangle((x+2, y+2, x+w-3, y+h-3), fill='#838383')
        box = gd.textbbox((0, 0), label, font=f)
        tx = x+(w-(box[2]-box[0]))/2
        ty = y+(h-(box[3]-box[1]))/2-box[1]
        gd.text((tx+1, ty+1), label, font=f, fill='#303030')
        gd.text((tx, ty), label, font=f, fill='#f6f6f6')
    gui = gui.resize((592, 384), Image.Resampling.NEAREST)

    image = Image.new('RGB', (1280, 720))
    px = image.load()
    for y in range(720):
        for x in range(1280):
            px[x, y] = (12 + x // 220, 19 + y // 150, 31 + x // 160)
    draw = ImageDraw.Draw(image)
    font = lambda path, size: ImageFont.truetype(path, size)
    draw.rounded_rectangle((55, 47, 276, 83), radius=18, fill='#17364a')
    draw.text((72, 54), 'SFM  /  MANAGER', font=font(BOLD, 16), fill='#80d9e0')
    draw.text((55, 103), 'Inside the manager', font=font(BOLD, 42), fill='#f1f6fc')
    draw.text((58, 162), 'The disk holds the direct-test transfer program', font=font(FONT, 21), fill='#aabdd0')
    draw.rounded_rectangle((54, 211, 688, 626), radius=18, fill='#111e2e', outline='#31485b', width=2)
    image.paste(gui, (75, 226), gui)
    draw = ImageDraw.Draw(image)
    draw.text((59, 650), 'Source textures and layout; font, widgets and state approximated.', font=font(FONT, 15), fill='#93a9b8')
    draw.text((746, 292), 'WORLD VIEW', font=font(BOLD, 15), fill='#80d9e0')
    draw.text((746, 321), 'Reconstructed orbit', font=font(FONT, 22), fill='#dfeaf2')
    draw.rounded_rectangle((738, 360, 1228, 640), radius=11, fill='#07101b', outline='#607c8f', width=2)
    draw.text((746, 655), 'Minecraft 1.19.2  ·  SFM', font=font(FONT, 15), fill='#93a9b8')
    layout = OUT / 'layout.png'
    image.save(layout)

    ease = 'min(max((t-2)/2,0),1)'
    graph = (f"[1:v]scale=w='2*trunc((1280-800*{ease})/2)':"
             f"h='2*trunc((720-450*{ease})/2)':eval=frame[world];"
             f"[0:v][world]overlay=x='743*{ease}':y='365*{ease}':"
             "eval=frame:shortest=1,format=yuv420p[v]")
    video, preview = OUT / 'output.mkv', OUT / 'preview.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-loop', '1', '-framerate', '30', '-i', str(layout),
                    '-i', str(ORBIT), '-filter_complex', graph, '-map', '[v]', '-t', '9',
                    '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    '-pix_fmt', 'yuv420p', '-metadata', 'title=SFM conference slice 02',
                    '-n', str(video)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0', '-c', 'copy',
                    '-movflags', '+faststart', '-n', str(preview)], check=True)
    print(f'Created {video} and {preview}')


if __name__ == '__main__':
    main()
