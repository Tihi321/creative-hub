"""Shared bits for the art scripts of this production: paths, the Endesga 64 colours we use, small helpers."""
import sys
from pathlib import Path

ART = Path(__file__).resolve().parent
OUT = ART / 'out'
sys.path.insert(0, str(ART.parents[2] / 'scripts'))
from pxcanvas import Canvas, Studio  # noqa: E402,F401

SCALE = 8  # every art pixel is 8x8 screen pixels: backgrounds 240x135 -> 1920x1080, sprites 120 rows -> 960 px
SPRITE_H = 120

# Endesga 64 picks
OUTLINE = '#391f21'
SKIN, SKIN_D, SKIN_L = '#f6ca9f', '#e69c69', '#f9e6cf'
BLUSH = '#f68187'
WHITE = '#ffffff'
MOUTH = '#8e251d'
TONGUE = '#f5555d'


def face_eye(c: Canvas, x: int, y: int, kind: str, iris: str, iris_d: str, line: str = OUTLINE):
    """A 4x5 cartoon eye with its top-left at (x, y). kinds: open, happy, lid, wide, up, down, closed, sad."""
    k, w, g, G = line, WHITE, iris, iris_d
    shapes = {
        'open': ['kkkk', 'kwGk', 'kgGk', 'kggk', '.kk.'],
        'wide': ['kkkk', 'kwwk', 'kwGk', 'kwwk', '.kk.'],
        'lid': ['....', 'kkkk', 'kgGk', 'kggk', '.kk.'],
        'up': ['kkkk', 'kGgk', 'kggk', 'kwwk', '.kk.'],
        'side': ['kkkk', 'kwGk', 'kwgk', 'kwwk', '.kk.'],
        'down': ['....', 'kkkk', 'kwwk', 'kGgk', '.kk.'],
        'happy': ['....', '.kk.', 'k..k', '....', '....'],
        'closed': ['....', '....', 'kkkk', '....', '....'],
        'sad': ['....', 'kkkk', 'kwGk', 'kggk', '.kk.'],
    }
    c.blit(shapes[kind], {'k': k, 'w': w, 'g': g, 'G': G}, x, y)


EYES5 = {
    'open': ['.kkk.', 'kwGGk', 'kgGGk', 'kggGk', 'kgggk', '.kkk.'],
    'wide': ['.kkk.', 'kwwwk', 'kwGwk', 'kwGwk', 'kwwwk', '.kkk.'],
    'lid': ['.....', 'kkkkk', 'kgGGk', 'kggGk', 'kgggk', '.kkk.'],
    'half': ['.....', '.....', 'kkkkk', 'kgGGk', 'kgggk', '.kkk.'],
    'up': ['.kkk.', 'kGGgk', 'kGggk', 'kgggk', 'kwwwk', '.kkk.'],
    'down': ['.....', '.....', 'kkkkk', 'kwwwk', 'kgGGk', '.kkk.'],
    'happy': ['.....', '.kkk.', 'k...k', '.....', '.....', '.....'],
    'closed': ['.....', '.....', '.....', 'kkkkk', '.....', '.....'],
    'teary': ['.kkk.', 'kwGGk', 'kgGGk', 'kggGk', 'kgggk', '.kkk.'],
}


def eye5(c: Canvas, x: int, y: int, kind: str, iris: str, iris_d: str, lash: int = 0, line: str = OUTLINE):
    """A 5x6 cartoon eye with its top-left at (x, y); lash -1 / +1 adds a lash on the left / right top corner."""
    c.blit(EYES5[kind], {'k': line, 'w': WHITE, 'g': iris, 'G': iris_d}, x, y)
    if lash and kind not in ('happy', 'closed'):
        top = y if EYES5[kind][0].strip('.') else y + (1 if EYES5[kind][1].strip('.') else 2)
        c.set(x - 1 if lash < 0 else x + 5, top, line)
    if kind == 'teary':
        c.set(x + 1, y + 6, '#94fdff')
        c.set(x + 1, y + 7, '#00cdf9')


def brow5(c: Canvas, x: int, y: int, tilt: str, color: str, thick: int = 1):
    """A 5-pixel brow starting at x. tilt: flat, up, raised, in (angry, inner end low) and sad (inner end high);
    the right brow uses in-r / sad-r, the mirrored forms."""
    dys = {
        'flat': [0, 0, 0, 0, 0], 'up': [0, -1, -1, -1, 0],
        'in': [-1, -1, 0, 0, 1], 'in-r': [1, 0, 0, -1, -1],
        'sad': [1, 0, 0, -1, -1], 'sad-r': [-1, -1, 0, 0, 1],
        'raised': [-1, -2, -2, -2, -1],
    }[tilt]
    for i, dy in enumerate(dys):
        for t in range(thick):
            c.set(x + i, y + dy + t, color)


def run_sprite(name: str, build, expressions):
    """Draw every expression in one Pixel Studio document and export sprite_<name>_<expr>.png."""
    frames = {e: build(e) for e in expressions}
    with Studio() as s:
        paths = s.sprite(f'sprite_{name}', frames, OUT, scale=SCALE)
    for p in paths:
        print(p)
    return paths
