#!/usr/bin/env python3
"""Cadence-corrected manager-to-V1-editor preview, reconstructed from pinned SFM source.

The screenshot, click timing, cursor, Minecraft font and widget skin are not
captured from the game. The V1 layout and default syntax colours are source
derived; the exact direct-test program comes from the verified test source.
"""
import hashlib
import re
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews' / 'conference-slice-04'
MANAGER = ROOT / 'previews/conference-slice-02/layout.png'
ORBIT = ROOT / 'deliverable/output.mkv'
TEST = ROOT / 'ground-truth/evidence/sfm/src/gametest/java/ca/teamdman/sfm/gametest/tests/general/Move1StackDirectGameTest.java'
EXPECTED = {
    MANAGER: 'f81d175af71975c8b8d9c3880c104035ed9fb9f5b63b5334b6c2050e02984bea',
    ORBIT: 'ffe2d3f7f68c67de44e0439c6ffdf4e512f79c0ed93a651b6d83f6345908c3b5',
    TEST: '750a09bcc1f910c2ed80954141d1ba77f39f1f52679c8cce98c818562c0aae01',
}
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'


def digest(path):
    with path.open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def main():
    for path, expected in EXPECTED.items():
        if digest(path) != expected:
            raise SystemExit(f'Input hash mismatch: {path}')
    source = TEST.read_text()
    match = re.search(r'manager\.setProgram\("""\s*\n(.*?)"""\.stripTrailing\(\)\.stripIndent\(\)\)', source, re.S)
    if not match:
        raise SystemExit('Could not extract the direct-test program.')
    code = textwrap.dedent(match.group(1)).strip().splitlines()
    if code != ['EVERY 20 TICKS DO', '    INPUT FROM a', '    OUTPUT TO b', 'END']:
        raise SystemExit('Direct-test program differs from the expected source.')
    if any((OUT / name).exists() for name in ('output.mkv', 'preview.mp4', 'editor.png', 'cursor.png')):
        raise SystemExit('Preview exists; preserve it and choose a new output directory.')
    OUT.mkdir(parents=True, exist_ok=True)

    # At 427x240, V1 computes textarea (13,10), size 400x200; footer y=215.
    # No line numbers or suggestions are shown (source defaults). The source
    # default syntax theme is used; font, its metrics and widget skin are not
    # the game's assets and remain visibly approximate.
    ui = Image.new('RGB', (427, 240), '#272727')
    draw = ImageDraw.Draw(ui)
    draw.rectangle((13, 10, 412, 209), fill='#ffffff')
    draw.rectangle((14, 11, 411, 208), fill='#000000')
    font = ImageFont.truetype(MONO, 8)
    bold = ImageFont.truetype(BOLD, 8)
    roles = {
        'EVERY': ('#5555ff', bold), 'DO': ('#5555ff', bold), 'END': ('#5555ff', bold),
        'INPUT': ('#ff55ff', font), 'FROM': ('#ff55ff', font),
        'OUTPUT': ('#ff55ff', font), 'TO': ('#ff55ff', font),
        'TICKS': ('#ffaa00', font), '20': ('#55ffff', font),
        'a': ('#55ff55', font), 'b': ('#55ff55', font),
    }
    y = 14
    for line in code:
        x = 17.0
        for piece in re.split(r'(EVERY|TICKS|DO|INPUT|FROM|OUTPUT|TO|END|20|\ba\b|\bb\b)', line):
            if not piece:
                continue
            color, face = roles.get(piece, ('#ffffff', font))
            draw.text((x+1, y+1), piece, font=face, fill='#202020')
            draw.text((x, y), piece, font=face, fill=color)
            x += draw.textlength(piece, font=face)
        y += 9
    button_font = ImageFont.truetype(MONO, 7)
    for x, width, label in [(13, 16, '#'), (61, 200, 'Done'), (311, 100, 'Cancel')]:
        draw.rectangle((x, 215, x+width-1, 234), fill='#777777', outline='#151515')
        draw.line((x+1, 216, x+width-2, 216), fill='#dddddd')
        draw.line((x+1, 233, x+width-2, 233), fill='#252525')
        box = draw.textbbox((0, 0), label, font=button_font)
        tx = x+(width-(box[2]-box[0]))/2
        ty = 215+(20-(box[3]-box[1]))/2-box[1]
        draw.text((tx+1, ty+1), label, font=button_font, fill='#303030')
        draw.text((tx, ty), label, font=button_font, fill='#ffffff')
    ui = ui.resize((1281, 720), Image.Resampling.NEAREST).crop((0, 0, 1280, 720))
    draw = ImageDraw.Draw(ui)
    caption = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    draw.text((936, 39), 'WORLD VIEW  /  RECONSTRUCTED', font=caption, fill='#c7d7e4')
    draw.rectangle((929, 64, 1257, 252), fill='#142434', outline='#90adbd', width=2)
    editor = OUT / 'editor.png'
    ui.save(editor)
    cursor = Image.new('RGBA', (30, 38), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cursor)
    cd.polygon([(1, 1), (1, 30), (8, 23), (14, 35), (19, 32), (13, 20), (24, 20)], fill='white', outline='black', width=2)
    cursor_path = OUT / 'cursor.png'
    cursor.save(cursor_path)

    # Put both still images and decoded orbit on the same exact 1/30 frame
    # clock before framesync. The MKV's millisecond time base otherwise makes
    # the overlay repeat and skip source frames at some output timestamps.
    u = 'min(max((t-2)/2,0),1)'
    ease = f'({u}*{u}*(3-2*{u}))'
    motion = 'min(max((t-5.3)/1.0,0),1)'
    graph = (
        "[0:v]trim=duration=8,settb=expr=1/30,setpts=N[layout];"
        "[1:v]trim=duration=8,settb=expr=1/30,setpts=N,"
        f"scale=w='2*trunc((1280-800*{ease})/2)':"
        f"h='2*trunc((720-450*{ease})/2)':eval=frame[world];"
        f"[layout][world]overlay=x='743*{ease}':y='365*{ease}':eval=frame:shortest=1[manager];"
        f"[manager][3:v]overlay=x='320-125*{motion}':y='520-152*{motion}':"
        "enable='between(t,5.3,7.9)':shortest=1[withcursor];"
        "[withcursor]drawbox=x=75:y=358:w=240:h=32:color=white@0.6:t=2:"
        "enable='between(t,6.8,7.0)'[managerfinal];"
        "[4:v]trim=start=8:duration=6,settb=expr=1/30,setpts=N,scale=320:180[editorworld];"
        "[2:v]trim=duration=6,settb=expr=1/30,setpts=N[editor];"
        "[editor][editorworld]overlay=933:68:shortest=1[editorfinal];"
        "[managerfinal][editorfinal]concat=n=2:v=1:a=0,format=yuv420p[v]"
    )
    video, preview = OUT / 'output.mkv', OUT / 'preview.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-loop', '1', '-framerate', '30', '-i', str(MANAGER), '-i', str(ORBIT),
                    '-loop', '1', '-framerate', '30', '-i', str(editor),
                    '-loop', '1', '-framerate', '30', '-i', str(cursor_path), '-i', str(ORBIT),
                    '-filter_complex', graph, '-map', '[v]', '-t', '14', '-r', '30',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-metadata', 'title=SFM conference slice 04', '-n', str(video)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0', '-c', 'copy',
                    '-movflags', '+faststart', '-n', str(preview)], check=True)
    print(f'Created {video} and {preview}')


if __name__ == '__main__':
    main()
