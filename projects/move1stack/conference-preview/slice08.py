#!/usr/bin/env python3
"""Illustrative test-barrel inventory cutaway; no game or browser execution.

The source test establishes the endpoints, not the on-screen timing or motion.
The dual inventory layout, icon, font and moving stack are reconstructions.
"""
import hashlib
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/conference-slice-08'
ORBIT = ROOT / 'deliverable/output.mkv'
EDITOR = ROOT / 'previews/conference-slice-05/editor.png'
DIRT = ROOT / 'ground-truth/assets/minecraft/textures/block/dirt.png'
TEST = ROOT / 'ground-truth/evidence/sfm/src/gametest/java/ca/teamdman/sfm/gametest/tests/general/Move1StackDirectGameTest.java'
EXPECTED = {
    ORBIT: 'ffe2d3f7f68c67de44e0439c6ffdf4e512f79c0ed93a651b6d83f6345908c3b5',
    EDITOR: '1b6250d2e2c796977412003bf9332dd1389a7370c1e442ba3a0c2dce97ac5a41',
    DIRT: 'fb0450253248276e0b8d653d5a4d21c59763cbf775c0e048469ff500afaaef68',
    TEST: '750a09bcc1f910c2ed80954141d1ba77f39f1f52679c8cce98c818562c0aae01',
}
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def dirt_icon():
    """Approximate Minecraft's block item icon from the saved 16x16 texture."""
    texture = Image.open(DIRT).convert('RGB')
    if texture.size != (16, 16):
        raise SystemExit('Unexpected dirt texture dimensions')
    icon = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            px, py = x + .5, y + .5
            u = ((px - 8) / 7 + (py - 1) / 4) / 2
            v = ((py - 1) / 4 - (px - 8) / 7) / 2
            shade = 1.0
            if not (0 <= u < 1 and 0 <= v < 1):
                u, v = (px - 1) / 7, (py - 5 - 4 * (px - 1) / 7) / 7
                shade = .72
                if not (0 <= u < 1 and 0 <= v < 1):
                    u, v = (px - 8) / 7, (py - 9 + 4 * (px - 8) / 7) / 7
                    shade = .86
            if 0 <= u < 1 and 0 <= v < 1:
                color = texture.getpixel((int(u * 16), int(v * 16)))
                icon.putpixel((x, y), (*[int(c * shade) for c in color], 255))
    return icon


def panel(full):
    # Reconstructed vanilla-style 9x3 barrel and 9x4 player inventory.
    # Texture, typography and item icon are approximations, not a game capture.
    img = Image.new('RGBA', (176, 166), '#c6c6c6')
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 175, 165), outline='#191919')
    d.line((1, 1, 174, 1), fill='white')
    d.line((1, 1, 1, 164), fill='white')
    d.line((2, 164, 174, 164), fill='#555555')
    d.line((174, 2, 174, 164), fill='#555555')
    font = ImageFont.truetype(MONO, 8)
    countfont = ImageFont.truetype(BOLD, 8)
    d.text((8, 5), 'Barrel', font=font, fill='#404040')
    d.text((8, 71), 'Inventory', font=font, fill='#404040')
    for top in (18, 36, 54, 84, 102, 120, 142):
        for col in range(9):
            x = 7 + 18 * col
            d.rectangle((x, top - 1, x + 17, top + 16), fill='#8b8b8b')
            d.line((x, top - 1, x + 17, top - 1), fill='#373737')
            d.line((x, top - 1, x, top + 16), fill='#373737')
            d.line((x + 1, top + 16, x + 17, top + 16), fill='white')
            d.line((x + 17, top, x + 17, top + 16), fill='white')
    if full:
        img.alpha_composite(dirt_icon(), (8, 18))
        d = ImageDraw.Draw(img)
        d.text((15, 27), '64', font=countfont, fill='#333333', stroke_width=1, stroke_fill='#333333')
        d.text((14, 26), '64', font=countfont, fill='white')
    return img.resize((528, 498), Image.Resampling.NEAREST)


def make_pair(left, right, path):
    layer = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    layer.alpha_composite(panel(left), (80, 205))
    layer.alpha_composite(panel(right), (672, 205))
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(BOLD, 21)
    d.text((84, 171), 'a', font=f, fill='#55ff55')
    d.text((676, 171), 'b', font=f, fill='#55ff55')
    layer.save(path)


def main():
    for path, expected in EXPECTED.items():
        if digest(path) != expected:
            raise SystemExit(f'Input hash mismatch: {path}')
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit('Output exists; preserve it and choose a new directory')
    OUT.mkdir(parents=True, exist_ok=True)
    bg = Image.open(EDITOR).convert('RGB')
    draw = ImageDraw.Draw(bg)
    draw.rectangle((925, 35, 1235, 254), fill='black')
    draw.rectangle((1236, 35, 1238, 254), fill='white')
    draw.rectangle((1239, 35, 1260, 254), fill='#272727')
    draw.rectangle((956, 47, 1214, 193), fill='#142434', outline='#90adbd', width=2)
    background = OUT / 'background.png'
    bg.save(background)
    before, between, after = (OUT / name for name in ('before.png', 'between.png', 'after.png'))
    make_pair(True, False, before)
    make_pair(False, False, between)
    make_pair(False, True, after)
    flying = dirt_icon().resize((48, 48), Image.Resampling.NEAREST)
    count = ImageDraw.Draw(flying)
    f = ImageFont.truetype(BOLD, 22)
    count.text((19, 24), '64', font=f, fill='white', stroke_width=2, stroke_fill='#333333')
    icon = OUT / 'stack.png'
    flying.save(icon)

    # Exact frame clocks avoid the repeated world frames in the first preview.
    # The stack's movement is a cinematic illustration, not a captured action.
    graph = (
        '[0:v]trim=duration=10,settb=expr=1/30,setpts=N[bg];'
        '[1:v]trim=start=10:duration=10,settb=expr=1/30,setpts=N,scale=250:140[world];'
        '[bg][world]overlay=960:50:shortest=1[base];'
        "[base][2:v]overlay=0:0:enable='between(t,2,5.2)':shortest=1[a];"
        "[a][3:v]overlay=0:0:enable='gt(t,5.2)*lt(t,5.8)':shortest=1[b];"
        "[b][4:v]overlay=0:0:enable='gte(t,5.8)':shortest=1[c];"
        "[c][5:v]overlay=x='104+592*min(max((t-5.2)/0.6,0),1)':y=259:"
        "enable='gt(t,5.2)*lt(t,5.8)':shortest=1,format=yuv420p[v]"
    )
    video, preview = OUT / 'output.mkv', OUT / 'preview.mp4'
    args = ['ffmpeg', '-v', 'error', '-loop', '1', '-framerate', '30', '-i', str(background),
            '-i', str(ORBIT)]
    for path in (before, between, after, icon):
        args += ['-loop', '1', '-framerate', '30', '-i', str(path)]
    args += ['-filter_complex', graph, '-map', '[v]', '-t', '10', '-r', '30',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
             '-metadata', 'title=SFM conference slice 08', '-n', str(video)]
    subprocess.run(args, check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0', '-c', 'copy',
                    '-movflags', '+faststart', '-n', str(preview)], check=True)
    print(f'Created {video} and {preview}')


if __name__ == '__main__':
    main()
