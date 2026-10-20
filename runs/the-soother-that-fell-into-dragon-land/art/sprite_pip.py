"""Pip: Petra's baby brother, about one, chubby, gummy smile, wispy blonde hair, blue eyes, soft green onesie.
He sits in a little wicker pram on wheels with a pink blanket over his lap, so his face is high on the canvas."""
import math

from common import Canvas, OUTLINE, SKIN, SKIN_D, SKIN_L, BLUSH, MOUTH, TONGUE, WHITE, SPRITE_H, eye5, brow5, run_sprite

W = 64
HAIR, HAIR_D, HAIR_L = '#ffc825', '#edab50', '#ffeb57'
SUIT, SUIT_D, SUIT_L, SUIT_DD = '#99e65f', '#5ac54f', '#d3fc7e', '#33984b'
IRIS, IRIS_D = '#0098dc', '#0069aa'
WICK, WICK_D, WICK_DD, WICK_L = '#edab50', '#e07438', '#bf6f4a', '#ffc825'
INSIDE = '#8a4836'
BLANK, BLANK_D, BLANK_L = '#fdd2ed', '#f68187', WHITE
METAL, METAL_D, METAL_L = '#657392', '#424c6e', '#c7cfdd'
TYRE = '#2a2f4e'
GUM = '#f68187'
CHEEK_RED = '#f5555d'
TEAR, TEAR_D = '#94fdff', '#00cdf9'
SOOTH, SOOTH_D, SOOTH_L, SOOTH_DD = '#0098dc', '#0069aa', '#00cdf9', '#00396d'

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
CX = 32  # centre line
RIM_Y = 66  # centre row of the basket's top rim (an ellipse seen from slightly above)
RIM_RX, RIM_RY = 27, 5


def rim_front(x):
    t = (x + 0.5 - CX) / RIM_RX
    return RIM_Y + RIM_RY * math.sqrt(max(0.0, 1 - t * t))


def tub_bottom(x):
    t = (x + 0.5 - CX) / 26.5
    return 84 + 17 * math.sqrt(max(0.0, 1 - t * t))


def tub_half(y):
    # the tub narrows a little towards the bottom
    return RIM_RX - max(0, (y - RIM_Y)) * 0.08


def wheel(c: Canvas, cx: int, cy: int):
    c.circle(cx, cy, 8, TYRE)
    c.circle(cx, cy, 6, METAL_L)
    for a in range(0, 360, 45):
        r = math.radians(a)
        c.line(cx, cy, round(cx + 5 * math.cos(r)), round(cy + 5 * math.sin(r)), METAL)
    c.circle(cx, cy, 1.5, METAL_D)
    c.set(cx - 1, cy - 1, WHITE)
    c.set(cx - 4, cy - 5, WHITE)


def pram_back(c: Canvas):
    # push handle behind on the right
    c.line(55, 72, 60, 48, METAL_D, t=2)
    c.line(55, 72, 59, 52, METAL, t=1)
    c.rect(57, 44, 6, 4, METAL_L)
    c.rect(57, 47, 6, 1, METAL)
    # wheels and the frame
    wheel(c, 15, 110)
    wheel(c, 49, 110)
    c.line(15, 110, 26, 100, METAL_D, t=2)
    c.line(49, 110, 38, 100, METAL_D, t=2)
    # the inside of the basket (seen over the far rim)
    c.ellipse(CX - RIM_RX, RIM_Y - RIM_RY, 2 * RIM_RX, 2 * RIM_RY + 1, WICK_DD)
    c.ellipse(CX - RIM_RX + 2, RIM_Y - RIM_RY + 2, 2 * RIM_RX - 4, 2 * RIM_RY - 2, INSIDE)


def pram_front(c: Canvas):
    # the wicker tub
    for y in range(RIM_Y, 103):
        hw = tub_half(y)
        for x in range(0, W):
            if abs(x + 0.5 - CX) > hw:
                continue
            if y < rim_front(x) - 0.5 or y > tub_bottom(x):
                continue
            band = (y - RIM_Y) // 4
            r = (y - RIM_Y) % 4
            u = (x + 0.5 - CX) / hw  # -1 left .. 1 right
            if r == 3:
                col = WICK_DD
            elif (x + y if band % 2 else x - y) % 4 == 0:
                col = WICK_DD if u > 0.55 else WICK_D
            elif u < -0.55 and r == 0:
                col = WICK_L
            elif u > 0.55:
                col = WICK_D
            else:
                col = WICK_L if (r == 0 and u < 0.1) else WICK
            c.set(x, y, col)
    # a darker belly under the tub
    for x in range(8, 57):
        b = round(tub_bottom(x))
        c.set(x, b, WICK_DD)
    # the rolled, braided front rim
    for x in range(CX - RIM_RX, CX + RIM_RX):
        y = round(rim_front(x))
        for dy in (-1, 0, 1):
            c.set(x, y + dy, WICK_D)
        c.set(x, y - 1 + (x % 3 == 0), WICK_L if x < 46 else WICK)
        c.set(x, y + 1, WICK_DD)
    # far rim, the top edge seen behind the baby
    for x in range(CX - RIM_RX, CX + RIM_RX):
        t = (x + 0.5 - CX) / RIM_RX
        y = round(RIM_Y - RIM_RY * math.sqrt(max(0.0, 1 - t * t)))
        c.set(x, y, WICK)
        c.set(x, y + 1, WICK_D)


def baby_body(c: Canvas):
    # torso in the onesie, sitting in the basket
    c.ellipse(17, 44, 30, 30, SUIT_D)
    c.ellipse(16, 44, 29, 30, SUIT)
    c.ellipse(19, 47, 8, 10, SUIT_L)
    c.ellipse(19, 49, 6, 7, SUIT)
    # round collar and snaps
    c.ellipse(24, 45, 16, 6, WHITE)
    c.rect(24, 45, 16, 2, None)
    c.set(32, 54, SUIT_DD)
    c.set(32, 58, SUIT_DD)
    # left arm resting on the blanket
    c.polygon([(18, 50), (23, 53), (19, 64), (12, 62)], SUIT)
    c.line(19, 54, 15, 61, SUIT_L)
    # right arm raised by his cheek
    c.polygon([(41, 50), (46, 49), (51, 56), (46, 59)], SUIT_D)
    c.line(44, 50, 48, 55, SUIT)


def blanket(c: Canvas):
    top = 60
    pts = [(15, top + 1), (24, top - 1), (32, top), (40, top - 1), (49, top + 1), (51, 72), (50, 80)]
    # scalloped hem hanging over the rim
    hem = []
    for i, x in enumerate(range(50, 13, -4)):
        hem.append((x, 81 + (2 if i % 2 else 0)))
    pts += hem + [(14, 80), (13, 72)]
    c.polygon(pts, BLANK)
    # fold shadows and the hem stripe
    c.line(49, 62, 50, 79, BLANK_D)
    c.line(48, 66, 48, 72, BLANK_D)
    c.line(26, 63, 22, 78, BLANK_D)
    c.line(38, 63, 41, 78, BLANK_D)
    for x in range(14, 51):
        for y in range(76, 86):
            if c.get(x, y) and (c.get(x, y + 1) is None or y == 85):
                c.set(x, y, BLANK_D)
                c.set(x, y - 1, BLANK_D)
                break
    # white polka dots
    for (x, y) in [(18, 64), (30, 66), (44, 64), (24, 72), (36, 73), (17, 76), (46, 74)]:
        c.rect(x, y, 2, 2, BLANK_L)
    # left hand on the blanket
    c.ellipse(10, 60, 8, 7, SKIN)
    c.set(15, 62, SKIN_D)
    c.set(15, 64, SKIN_D)
    c.set(11, 61, SKIN_L)


def right_hand(c: Canvas):
    c.ellipse(44, 52, 8, 8, SKIN)
    c.set(45, 53, SKIN_L)
    c.line(50, 54, 50, 58, SKIN_D)
    c.set(46, 58, SKIN_D)
    c.set(48, 58, SKIN_D)


def soother(c: Canvas):
    """His round blue soother in the classic side view: a teat on top, the wide shield, the ring in his fist.
    Drawn on its own layer with its own outline so it stands clear of his cheek."""
    t = Canvas(W, SPRITE_H)
    t.blit([
        '.....ww.....',
        '....wWWc....',
        '....wWWc....',
        '.....cc.....',
        '..LLssssss..',
        '.LWLsssssdd.',
        'sLssssssssdd',
        '.dddddddddd.',
        '...rrrrrr...',
        '..rr....rr..',
        '..rr....rr..',
        '..rr....rr..',
        '...rr..rr...',
    ], {'w': WHITE, 'W': WHITE, 'c': '#c7cfdd', 's': SOOTH, 'L': SOOTH_L, 'd': SOOTH_D, 'r': SOOTH_D},
        42, 39)
    t.rect(46, 48, 4, 3, SOOTH_DD)
    t.outline(OUTLINE)
    # the fist closes over the bottom of the ring
    for y in range(52, 60):
        for x in range(40, 56):
            t.set(x, y, None)
    c.paste(t)


def head(c: Canvas, expr: str):
    # ears
    c.ellipse(11, 30, 6, 8, SKIN_D)
    c.ellipse(47, 30, 6, 8, SKIN_D)
    c.set(13, 33, SKIN)
    c.set(50, 33, SKIN)
    # big round head, shade crescent on the right, chubby cheeks low on the face
    c.ellipse(15, 14, 36, 34, SKIN_D)
    c.ellipse(14, 13, 35, 34, SKIN)
    c.ellipse(14, 28, 14, 18, SKIN)
    c.ellipse(37, 29, 14, 18, SKIN_D)
    c.ellipse(36, 28, 14, 18, SKIN)
    c.line(22, 19, 25, 17, SKIN_L)  # shine on the brow
    c.set(21, 20, SKIN_L)

    eyes = {'neutral': 'open', 'happy': 'happy', 'sad': None}[expr]
    if eyes:
        eye5(c, 22, 31, eyes, IRIS, IRIS_D)
        eye5(c, 37, 31, eyes, IRIS, IRIS_D)
        if eyes == 'open':  # a second shine: baby eyes sparkle
            c.set(25, 35, WHITE)
            c.set(40, 35, WHITE)
    else:
        k = OUTLINE
        c.blit(['k....', '.kk..', '...kk', '.kk..', 'k....'], {'k': k}, 22, 32)
        c.blit(['....k', '..kk.', 'kk...', '..kk.', '....k'], {'k': k}, 37, 32)
    tl, tr = {'neutral': ('up', 'up'), 'happy': ('up', 'up'), 'sad': ('sad', 'sad-r')}[expr]
    brow5(c, 22, 28 if expr != 'sad' else 29, tl, HAIR_D)
    brow5(c, 37, 28 if expr != 'sad' else 29, tr, HAIR_D)

    # cheeks
    if expr == 'sad':
        for (x, y) in [(18, 39), (19, 39), (20, 39), (21, 39), (18, 40), (19, 40), (20, 40), (19, 41),
                       (42, 39), (43, 39), (44, 39), (45, 39), (43, 40), (44, 40), (45, 40), (44, 41)]:
            c.set(x, y, CHEEK_RED)
        c.set(19, 39, BLUSH)
        c.set(43, 39, BLUSH)
    else:
        for (x, y) in [(18, 39), (19, 39), (20, 39), (19, 40), (43, 39), (44, 39), (45, 39), (44, 40)]:
            c.set(x, y, BLUSH)

    k = OUTLINE
    mouths = {
        'neutral': (['.kk.', 'kmmk', 'kttk', '.kk.'], 30, 41),
        'happy': (['kkkkkkkkkk', 'kggwggwggk', 'kmmmmmmmmk', '.kmmttmmk.', '..kkkkkk..'], 27, 40),
        'sad': (['...kkkk...', '.kkmmmmkk.', 'kmmmmmmmmk', 'kmmmmmmmmk', 'kmmmttmmmk', '.kmttttmk.', '..kkkkkk..'], 27, 40),
    }[expr]
    rows, mx, my = mouths
    c.blit(rows, {'k': k, 'm': MOUTH, 't': TONGUE, 'g': GUM, 'w': WHITE}, mx, my)
    if expr == 'sad':
        # tears streaming down both cheeks and a drop flying off each side
        for (x0, x1) in [(21, 20), (42, 43)]:
            for y in range(37, 46):
                x = x0 if y < 41 else x1
                c.set(x, y, TEAR)
            c.set(x1, 46, TEAR_D)
            c.set(x1, 45, TEAR_D)
        drop = ['.t.', 'tTt', 'tTt', '.t.']
        c.blit(drop, {'t': TEAR_D, 'T': TEAR}, 7, 25)
        c.blit(drop, {'t': TEAR_D, 'T': TEAR}, 54, 25)
        c.set(11, 22, TEAR)
        c.set(52, 22, TEAR)

    # wispy blonde hair: a soft fringe line and a curl on top
    c.polygon([(18, 20), (23, 15), (31, 13), (40, 14), (45, 19), (46, 23), (42, 20), (39, 22), (36, 18), (32, 21),
               (28, 17), (25, 21), (22, 19), (19, 23)], HAIR)
    c.line(24, 16, 30, 14, HAIR_L)
    c.line(35, 15, 38, 16, HAIR_L)
    c.set(41, 18, HAIR_D)
    c.set(33, 18, HAIR_D)
    # a wispy curl standing up on top
    c.blit(['..hh..', '.h..h.', 'h...h.', '.h.hh.', '..hh..'], {'h': HAIR}, 29, 8)
    c.set(31, 13, HAIR_D)
    c.set(30, 12, HAIR_D)
    c.set(29, 9, HAIR_L)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    pram_back(c)
    baby_body(c)
    pram_front(c)
    blanket(c)
    head(c, expr)
    right_hand(c)
    if expr == 'happy':
        soother(c)
        right_hand(c)
        # thumb over the ring, the fist holds it
        c.set(47, 52, SKIN_D)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'sad', 'happy']

if __name__ == '__main__':
    run_sprite('pip', build, EXPRESSIONS)
