"""Mango: a small orange dragon the size of a cat, smooth scales, big round amber eyes, tiny wings, curly tail, cream belly,
little horns, a round snout and a brown satchel for lost things. Drawn hovering in the upper part of the canvas."""
import math

from common import Canvas, OUTLINE, WHITE, BLUSH, MOUTH, TONGUE, SPRITE_H, brow5, run_sprite

W = 72
Y = 6  # vertical offset of the whole figure (he hovers, the canvas below him stays empty)
BODY, BODY_D, BODY_DD, BODY_L = '#ed7614', '#c64524', '#8e251d', '#ffa214'
BELLY, BELLY_D = '#f9e6cf', '#f6ca9f'
HORN, HORN_D = '#f9e6cf', '#edab50'
WING, WING_D, WING_RIB = '#ffc825', '#edab50', '#e07438'
BAG, BAG_D, BAG_L = '#8a4836', '#5d2c28', '#bf6f4a'
GOLD, GOLD_L = '#ffc825', '#ffeb57'
IRIS, IRIS_D, IRIS_L = '#ffa214', '#e07438', '#ffeb57'
BROW = '#5d2c28'
SWEAT, SWEAT_D = '#94fdff', '#00cdf9'

# Mango's own big round eyes, 7x8, in the same build as eye5 (k line, w white, g iris, G iris dark, y glow, p pupil)
EYES7 = {
    'open': ['.kkkkk.', 'kwwGGGk', 'kwwppGk', 'kgpppGk', 'kgpppGk', 'kggggwk', 'kgyyygk', '.kkkkk.'],
    'wide': ['.kkkkk.', 'kwwwwwk', 'kwwGwwk', 'kwGpGwk', 'kwGpGwk', 'kwwgwwk', 'kwwwwwk', '.kkkkk.'],
    'up': ['.kkkkk.', 'kGppwwk', 'kGpppwk', 'kGpppgk', 'kGgggyk', 'kwwwwwk', 'kwwwwwk', '.kkkkk.'],
    'happy': ['.......', '.......', '.kkkkk.', 'kk...kk', 'k.....k', '.......', '.......', '.......'],
}


def eye7(c: Canvas, x: int, y: int, kind: str, flip: bool = False):
    c.blit(EYES7[kind], {'k': OUTLINE, 'w': WHITE, 'g': IRIS, 'G': IRIS_D, 'y': IRIS_L, 'p': OUTLINE}, x, y, flip=flip)


def disk(c: Canvas, cx: float, cy: float, r: float, col):
    for yy in range(math.floor(cy - r), math.ceil(cy + r) + 1):
        for xx in range(math.floor(cx - r), math.ceil(cx + r) + 1):
            if (xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= r * r:
                c.set(xx, yy, col)


def wings(c: Canvas):
    # tiny bat-like wings raised beside the head (mid-flap): a bone along the top, three finger tips, scalloped membrane
    wr = (12, 17)  # the wrist; finger tips fan out from it, the membrane dips in between them
    tips = [(4, 10), (3, 23), (8, 31), (16, 37)]
    sh = (25, 36)  # shoulder, behind the body
    pts = tips + [sh]
    for flip in (False, True):
        def X(x):
            return W - x if flip else x

        def P(x):  # the same column for single pixels
            return W - 1 - x if flip else x
        mem, mem_d = (WING_D, WING_RIB) if flip else (WING, WING_D)
        for a, b in zip(pts, pts[1:]):
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            m = (m[0] + (wr[0] - m[0]) * 0.25, m[1] + (wr[1] - m[1]) * 0.25)
            c.polygon([(X(wr[0]), Y + wr[1]), (X(a[0]), Y + a[1]), (X(m[0]), Y + m[1]), (X(b[0]), Y + b[1])], mem)
        # ribs from the wrist to the finger tips, the arm bone from the shoulder to the wrist and the top tip
        for t in tips[1:]:
            c.line(P(wr[0]), Y + wr[1], P(t[0]), Y + t[1], mem_d)
        c.line(P(sh[0] - 1), Y + sh[1] - 1, P(wr[0]), Y + wr[1], BODY_D if flip else BODY, 2)
        c.line(P(wr[0]), Y + wr[1], P(tips[0][0]), Y + tips[0][1], BODY_D if flip else BODY)
        c.set(P(tips[0][0]), Y + tips[0][1] - 1, HORN_D if flip else HORN)  # a little claw on top
    c.line(9, Y + 21, 6, Y + 21, GOLD_L)  # warm light on the left membrane
    c.line(10, Y + 24, 8, Y + 26, GOLD_L)


def tail(c: Canvas):
    # from the bottom left of the body out and round into a curl (a spiral of shrinking disks)
    for t in range(0, 101):
        f = t / 100
        disk(c, 29 - 11 * f, Y + 59 + 3 * math.sin(f * math.pi), 2.2, BODY)
    cx, cy = 13, Y + 53
    n = 140
    for i in range(n + 1):
        f = i / n
        a = math.radians(90 + 400 * f)  # start at the bottom, go round by the left, the top and the right, inward
        r = 7.0 - 4.5 * f
        disk(c, cx + r * math.cos(a), cy + r * math.sin(a), 2.2 - 1.0 * f, BODY)
    # shade under the tail
    c.line(19, Y + 62, 27, Y + 62, BODY_D)


def body(c: Canvas):
    # round little body under the head, shade on the right
    c.ellipse(26, Y + 38, 23, 24, BODY_D)
    c.ellipse(25, Y + 37, 22, 23, BODY)
    # cream belly with scale bands
    c.ellipse(30, Y + 42, 14, 17, BELLY)
    for by in (46, 50, 54):
        c.line(32, Y + by, 41, Y + by, BELLY_D)
    # feet dangling (he is hovering)
    for fx in (29, 40):
        c.ellipse(fx, Y + 57, 6, 7, BODY)
        c.rect(fx + 1, Y + 62, 4, 1, BODY_D)
        c.set(fx + 1, Y + 63, HORN)
        c.set(fx + 4, Y + 63, HORN)
    # tiny arms held up in front of the chest
    c.ellipse(24, Y + 43, 6, 6, BODY)
    c.ellipse(45, Y + 43, 6, 6, BODY_D)
    for x in (25, 27, 46, 48):
        c.set(x, Y + 48, HORN)


def satchel(c: Canvas):
    # strap from the left shoulder to the right hip
    c.line(29, Y + 39, 46, Y + 53, BAG, 2)
    c.line(30, Y + 39, 46, Y + 52, BAG_L)
    # bag at the right hip
    c.rect(43, Y + 50, 11, 9, BAG)
    c.rect(43, Y + 57, 11, 2, BAG_D)
    c.rect(43, Y + 50, 11, 4, BAG_D)  # flap
    c.rect(43, Y + 50, 11, 1, BAG_L)
    c.rect(47, Y + 53, 3, 2, GOLD)  # buckle
    c.set(47, Y + 53, GOLD_L)
    # something shiny peeking out of the flap
    c.blit(['.y.', 'yYy', '.y.'], {'y': GOLD, 'Y': GOLD_L}, 50, Y + 47)


def head(c: Canvas, expr: str):
    # horns
    for flip in (False, True):
        def X(x):
            return W - 1 - x if flip else x
        c.polygon([(X(25), Y + 18), (X(23), Y + 7), (X(26), Y + 9), (X(30), Y + 16)], HORN_D if flip else HORN)
        c.line(X(24), Y + 9, X(25), Y + 14, HORN_D if not flip else '#e07438')
    # ear frills
    c.polygon([(21, Y + 21), (14, Y + 19), (17, Y + 25), (15, Y + 29), (22, Y + 29)], BODY_L)
    c.polygon([(50, Y + 21), (57, Y + 19), (54, Y + 25), (56, Y + 29), (49, Y + 29)], BODY_D)
    # head: shade crescent on the right, then the scales
    c.ellipse(21, Y + 12, 32, 29, BODY_D)
    c.ellipse(20, Y + 11, 31, 28, BODY)
    c.line(27, Y + 14, 33, Y + 13, BODY_L)  # shine on the crown
    c.line(25, Y + 16, 26, Y + 15, BODY_L)
    for x in (33, 36):  # crest bumps between the horns
        c.rect(x, Y + 9, 2, 2, BODY_L)
    # round snout
    c.ellipse(28, Y + 28, 16, 11, BODY_D)
    c.ellipse(28, Y + 27, 15, 11, BODY_L)
    c.set(32, Y + 30, BODY_DD)
    c.set(39, Y + 30, BODY_DD)
    # big eyes and brows
    eyes = {'neutral': 'open', 'happy': 'happy', 'worried': 'up', 'surprised': 'wide'}[expr]
    eye7(c, 25, Y + 18, eyes)
    eye7(c, 39, Y + 18, eyes, flip=eyes == 'up')
    tl, tr = {'neutral': ('flat', 'flat'), 'happy': ('up', 'up'), 'worried': ('sad', 'sad-r'),
              'surprised': ('raised', 'raised')}[expr]
    by = Y + 15 if expr != 'surprised' else Y + 14
    thick = 2 if expr == 'worried' else 1
    brow5(c, 26, by, tl, BROW, thick)
    brow5(c, 40, by, tr, BROW, thick)
    # blush
    for (x, y) in [(22, 27), (23, 27), (24, 27), (23, 28), (47, 27), (48, 27), (49, 27), (48, 28)]:
        c.set(x, Y + y, BLUSH)
    k = OUTLINE
    mouths = {
        'neutral': ['.k......k.', '..kkkkkk..', '...w......'],
        'happy': ['kkkkkkkkkk', 'kwmmmmmmwk', '.kmmmmmmk.', '.kmttttmk.', '..kkkkkk..'],
        'worried': ['..........', '...kk.kk..', '..k..k..k.', '...w......'],
        'surprised': ['....kk....', '...kmmk...', '...kmmk...', '....kk....'],
    }[expr]
    c.blit(mouths, {'k': k, 'm': MOUTH, 't': TONGUE, 'w': WHITE}, 31, Y + 32)
    if expr == 'worried':  # a sweat drop on the side of the head
        c.blit(['.s.', 'sSs', 'sSs', '.s.'], {'s': SWEAT_D, 'S': SWEAT}, 49, Y + 17)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    wings(c)
    tail(c)
    body(c)
    satchel(c)
    head(c, expr)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'happy', 'worried', 'surprised']

if __name__ == '__main__':
    run_sprite('mango', build, EXPRESSIONS)
