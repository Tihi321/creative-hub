"""Petra: six, round freckled face, bright green eyes, short messy brown hair, yellow raincoat, blue jeans, red rain boots."""
from common import Canvas, OUTLINE, SKIN, SKIN_D, BLUSH, MOUTH, TONGUE, SPRITE_H, eye5, brow5, run_sprite

W = 56
HAIR, HAIR_D, HAIR_L = '#8a4836', '#5d2c28', '#bf6f4a'
COAT, COAT_D, COAT_L, COAT_DD = '#ffc825', '#edab50', '#ffeb57', '#e07438'
JEANS, JEANS_D, JEANS_L = '#0069aa', '#00396d', '#0098dc'
BOOT, BOOT_D, BOOT_L = '#ea323c', '#c42430', '#f5555d'
IRIS, IRIS_D = '#5ac54f', '#1e6f50'
FRECKLE = '#bf6f4a'
BROW = HAIR_D


def body(c: Canvas):
    y0 = SPRITE_H - 120  # top of the figure
    # boots
    for (sx, toe) in [(15, -3), (31, 3)]:
        c.rect(sx, y0 + 104, 10, 10, BOOT)
        c.ellipse(sx + min(0, toe) - 1, y0 + 110, 12 + abs(toe), 9, BOOT)
        c.rect(sx + min(0, toe), y0 + 117, 11 + abs(toe), 2, BOOT_D)
        c.rect(sx, y0 + 104, 10, 2, BOOT_D)
        c.line(sx + 2, y0 + 107, sx + 2, y0 + 113, BOOT_L)
    # jeans
    for sx in (16, 31):
        c.rect(sx, y0 + 82, 9, 23, JEANS)
        c.rect(sx, y0 + 101, 9, 3, JEANS_L)
    c.line(24, y0 + 84, 24, y0 + 100, JEANS_D)
    c.line(31, y0 + 84, 31, y0 + 100, JEANS_D)
    # raincoat (A-line), shade on the right
    c.polygon([(17, y0 + 43), (39, y0 + 43), (47, y0 + 88), (9, y0 + 88)], COAT)
    c.polygon([(31, y0 + 43), (39, y0 + 43), (47, y0 + 88), (36, y0 + 88)], COAT_D)
    c.polygon([(17, y0 + 43), (21, y0 + 43), (14, y0 + 88), (9, y0 + 88)], COAT_L)
    c.rect(9, y0 + 86, 39, 2, COAT_DD)
    c.line(28, y0 + 47, 28, y0 + 86, COAT_D)
    for by in (51, 59, 67, 75):
        c.rect(25, y0 + by, 2, 2, HAIR_D)
    c.rect(13, y0 + 70, 7, 6, COAT_D)  # pocket
    c.rect(13, y0 + 70, 7, 1, COAT_DD)
    # sleeves and hands
    c.polygon([(17, y0 + 44), (22, y0 + 47), (15, y0 + 74), (9, y0 + 72)], COAT)
    c.polygon([(39, y0 + 44), (34, y0 + 47), (41, y0 + 74), (47, y0 + 72)], COAT_D)
    c.ellipse(8, y0 + 71, 8, 7, SKIN)
    c.ellipse(40, y0 + 71, 8, 7, SKIN)
    c.rect(8, y0 + 70, 8, 2, COAT_DD)
    c.rect(40, y0 + 70, 8, 2, COAT_DD)
    # neck and hood folded behind it
    c.ellipse(15, y0 + 37, 26, 10, COAT_D)
    c.rect(25, y0 + 37, 7, 6, SKIN_D)
    c.polygon([(20, y0 + 41), (28, y0 + 46), (22, y0 + 49)], COAT_L)
    c.polygon([(36, y0 + 41), (28, y0 + 46), (34, y0 + 49)], COAT)


def head(c: Canvas, expr: str):
    y0 = SPRITE_H - 120
    # hair behind the head
    c.ellipse(9, y0 + 4, 38, 30, HAIR_D)
    # ears
    c.ellipse(9, y0 + 22, 6, 8, SKIN_D)
    c.ellipse(41, y0 + 22, 6, 8, SKIN_D)
    # face: shade crescent on the right, then skin
    c.ellipse(12, y0 + 8, 32, 32, SKIN_D)
    c.ellipse(11, y0 + 7, 31, 32, SKIN)
    # eyes, brows, mouth
    eyes = {'neutral': 'open', 'happy': 'happy', 'angry': 'lid', 'worried': 'open', 'surprised': 'wide', 'thinking': 'up'}[expr]
    eye5(c, 18, y0 + 22, eyes, IRIS, IRIS_D, lash=-1)
    eye5(c, 33, y0 + 22, eyes, IRIS, IRIS_D, lash=1)
    tl, tr = {'neutral': ('flat', 'flat'), 'happy': ('up', 'up'), 'angry': ('in', 'in-r'), 'worried': ('sad', 'sad-r'),
              'surprised': ('raised', 'raised'), 'thinking': ('flat', 'raised')}[expr]
    brow5(c, 18, y0 + 20, tl, BROW, 2 if expr == 'angry' else 1)
    brow5(c, 33, y0 + 20, tr, BROW, 2 if expr == 'angry' else 1)
    # blush and freckles
    for (x, y) in [(15, 30), (16, 30), (17, 30), (16, 31), (38, 30), (39, 30), (40, 30), (39, 31)]:
        c.set(x, y0 + y, BLUSH)
    for (x, y) in [(23, 29), (25, 30), (24, 31), (31, 29), (33, 30), (32, 31)]:
        c.set(x, y0 + y, FRECKLE)
    k = OUTLINE
    mouths = {
        'neutral': ['k....k', '.kkkk.'],
        'happy': ['kkkkkk', 'kmmmmk', '.kttk.', '..kk..'],
        'angry': ['......', '.kkkk.', 'k....k'],
        'worried': ['......', '.kkkk.', 'k....k'],
        'surprised': ['..kk..', '.kmmk.', '.kmmk.', '..kk..'],
        'thinking': ['......', '..kkkk', '......'],
    }[expr]
    c.blit(mouths, {'k': k, 'm': MOUTH, 't': TONGUE}, 25, y0 + 31)
    # messy fringe and tufts
    c.polygon([(10, y0 + 22), (11, y0 + 11), (19, y0 + 4), (30, y0 + 3), (41, y0 + 6), (46, y0 + 14), (46, y0 + 22),
               (43, y0 + 16), (40, y0 + 19), (37, y0 + 15), (33, y0 + 18), (29, y0 + 14), (25, y0 + 18), (21, y0 + 14),
               (17, y0 + 18), (14, y0 + 15)], HAIR)
    for tuft in ([(20, y0 + 6), (17, y0 + 0), (25, y0 + 4)], [(31, y0 + 4), (36, y0 + -1), (38, y0 + 6)], [(42, y0 + 9), (49, y0 + 7), (45, y0 + 14)]):
        c.polygon(tuft, HAIR)
    c.line(16, y0 + 9, 22, y0 + 6, HAIR_L)
    c.line(26, y0 + 5, 32, y0 + 5, HAIR_L)
    c.line(12, y0 + 14, 14, y0 + 11, HAIR_L)
    # side strands over the ears
    c.polygon([(10, y0 + 16), (14, y0 + 18), (13, y0 + 28), (10, y0 + 25)], HAIR)
    c.polygon([(46, y0 + 16), (42, y0 + 18), (43, y0 + 28), (46, y0 + 25)], HAIR)
    # a red hair clip on the left
    c.blit(['.rr.', 'rRRr', 'rRRr', '.rr.'], {'r': BOOT_D, 'R': BOOT}, 12, y0 + 12)
    c.set(13, y0 + 13, BOOT_L)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    body(c)
    head(c, expr)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'angry', 'worried', 'surprised', 'happy', 'thinking']

if __name__ == '__main__':
    run_sprite('petra', build, EXPRESSIONS)
