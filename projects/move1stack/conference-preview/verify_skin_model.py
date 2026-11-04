"""Check rendered front-face skin samples against the original legacy texture."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
image = Image.open(ROOT / 'previews/conference-slice-10/front.png').convert('RGBA')
texture = Image.open(ROOT / '.inputs/skin.png').convert('RGBA')
if image.size != (500, 640) or texture.size != (64, 32):
    raise SystemExit('Unexpected render or skin dimensions')
parts = [
    ('head', 0, 28, 8, 8, (8, 8), False),
    ('torso', 0, 18, 8, 12, (20, 20), False),
    ('right arm', -6, 18, 4, 12, (44, 20), False),
    ('left arm', 6, 18, 4, 12, (44, 20), True),
    ('right leg', -2, 6, 4, 12, (4, 20), False),
    ('left leg', 2, 6, 4, 12, (4, 20), True),
]
scale = 640 / 35
for name, x, z, w, h, (u, v), mirror in parts:
    errors = []
    for j in range(h):
        for i in range(w):
            sx = round(250 + (x - w/2 + i + .5) * scale)
            sy = round(320 - (z + h/2 - j - .5 - 16) * scale)
            actual = image.getpixel((sx, sy))
            expected = texture.getpixel((u + (w-1-i if mirror else i), v+j))
            errors.append(max(abs(actual[k] - expected[k]) for k in range(4)))
    if max(errors) > 2:
        raise SystemExit(f'{name}: maximum color error {max(errors)} exceeds 2')
    print(f'{name}: {len(errors)} samples, maximum channel error {max(errors)}')
