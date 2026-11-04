#!/usr/bin/env python3
"""Create a short presentation-layout study from the preserved orbit.

This preview uses the source test's program as presentation text. It is not a
reconstruction of the SFM editor, and does not simulate an inventory transfer.
"""
import hashlib
import re
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews' / 'conference-slice-01'
TEST = ROOT / 'ground-truth/evidence/sfm/src/gametest/java/ca/teamdman/sfm/gametest/tests/general/Move1StackDirectGameTest.java'
ORBIT = ROOT / 'deliverable/output.mkv'
TEST_SHA256 = '750a09bcc1f910c2ed80954141d1ba77f39f1f52679c8cce98c818562c0aae01'
ORBIT_SHA256 = 'ffe2d3f7f68c67de44e0439c6ffdf4e512f79c0ed93a651b6d83f6345908c3b5'


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    if digest(TEST) != TEST_SHA256 or digest(ORBIT) != ORBIT_SHA256:
        raise SystemExit('Source test or preserved orbit does not match the recorded input.')
    java = TEST.read_text()
    match = re.search(r'manager\.setProgram\("""\s*\n(.*?)"""\.stripTrailing\(\)\.stripIndent\(\)\)', java, re.S)
    if not match:
        raise SystemExit('Could not extract the direct test program.')
    code = textwrap.dedent(match.group(1)).strip().splitlines()
    expected = ['EVERY 20 TICKS DO', '    INPUT FROM a', '    OUTPUT TO b', 'END']
    if code != expected:
        raise SystemExit('The test program differs from the expected source-grounded text.')
    if any((OUT / name).exists() for name in ('output.mkv', 'preview.mp4', 'layout.png')):
        raise SystemExit('Preview exists; preserve it and choose a new output directory.')
    OUT.mkdir(parents=True, exist_ok=True)

    image = Image.new('RGB', (1280, 720))
    pixels = image.load()
    for y in range(720):
        for x in range(1280):
            pixels[x, y] = (12 + x // 220, 19 + y // 150, 31 + x // 160)
    draw = ImageDraw.Draw(image)
    sans = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    mono = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    font = lambda path, size: ImageFont.truetype(path, size)
    draw.rounded_rectangle((55, 47, 295, 83), radius=18, fill='#17364a')
    draw.text((72, 54), 'SFM  /  DIRECT TEST', font=font(bold, 16), fill='#80d9e0')
    draw.text((55, 103), 'One stack, two barrels', font=font(bold, 42), fill='#f1f6fc')
    draw.text((58, 162), 'A source-grounded explanation of move_1_stack_direct', font=font(sans, 21), fill='#aabdd0')
    draw.rounded_rectangle((55, 235, 716, 568), radius=18, fill='#111e2e', outline='#31485b', width=2)
    draw.text((81, 257), 'TEST PROGRAM', font=font(bold, 15), fill='#76c6d0')
    draw.text((81, 289), 'From Move1StackDirectGameTest.java', font=font(sans, 16), fill='#91a8bb')
    fcode = font(mono, 30)
    y = 337
    for line in code:
        x = 84
        for piece in re.split(r'(EVERY|TICKS|DO|INPUT|FROM|OUTPUT|TO|END|20|\ba\b|\bb\b)', line):
            if not piece:
                continue
            color = '#dce8f2'
            if piece in {'EVERY', 'TICKS', 'DO', 'INPUT', 'FROM', 'OUTPUT', 'TO', 'END'}:
                color = '#83d5dc'
            elif piece == '20':
                color = '#f1c77b'
            elif piece in {'a', 'b'}:
                color = '#c8a6f4'
            draw.text((x, y), piece, font=fcode, fill=color)
            x += draw.textlength(piece, font=fcode)
        y += 45
    draw.text((59, 604), '64 dirt  ·  left barrel a  →  right barrel b', font=font(bold, 20), fill='#dbe8f0')
    draw.text((59, 643), 'Program text from the test; editor and inventory views are next.', font=font(sans, 17), fill='#8fa6b7')
    draw.text((746, 292), 'WORLD VIEW', font=font(bold, 15), fill='#80d9e0')
    draw.text((746, 321), 'Reconstructed orbit', font=font(sans, 22), fill='#dfeaf2')
    draw.rounded_rectangle((738, 360, 1228, 640), radius=11, fill='#07101b', outline='#607c8f', width=2)
    draw.text((746, 655), 'Minecraft 1.19.2  ·  SFM', font=font(sans, 15), fill='#93a9b8')
    layout = OUT / 'layout.png'
    image.save(layout)

    # The first two seconds are full-frame; over two seconds the same orbit
    # scales and moves into the presentation inset. No new world rendering.
    ease = 'min(max((t-2)/2,0),1)'
    graph = (f"[1:v]scale=w='2*trunc((1280-800*{ease})/2)':"
             f"h='2*trunc((720-450*{ease})/2)':eval=frame[world];"
             f"[0:v][world]overlay=x='743*{ease}':y='365*{ease}':"
             "eval=frame:shortest=1,format=yuv420p[v]")
    video = OUT / 'output.mkv'
    preview = OUT / 'preview.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-loop', '1', '-framerate', '30', '-i', str(layout),
                    '-i', str(ORBIT), '-filter_complex', graph, '-map', '[v]', '-t', '9',
                    '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    '-pix_fmt', 'yuv420p', '-metadata', 'title=SFM conference slice 01',
                    '-n', str(video)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0', '-c', 'copy',
                    '-movflags', '+faststart', '-n', str(preview)], check=True)
    print(f'Created {video} and {preview}')


if __name__ == '__main__':
    main()
