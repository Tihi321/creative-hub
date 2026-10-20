"""Nib: a tidy knee-high dragon with neat green scales, round glasses, a red bow tie and a label-maker on his belt, a pencil
behind his ear. He runs the Lost Things Office. Drawn standing on two labelled ledgers on a tall wooden stool, so his face
sits above the text box."""
from common import Canvas, OUTLINE, WHITE, BLUSH, MOUTH, TONGUE, SPRITE_H, eye5, brow5, run_sprite

W = 64
SCALE_G, SCALE_D, SCALE_DD, SCALE_L, SCALE_LL = '#5ac54f', '#33984b', '#1e6f50', '#99e65f', '#d3fc7e'
BELLY, BELLY_D = '#f9e6cf', '#f6ca9f'
HORN, HORN_D = '#f9e6cf', '#edab50'
IRIS, IRIS_D = '#0098dc', '#0069aa'
BROW = '#134c4c'
FRAME = '#3d3d3d'
TIE, TIE_D, TIE_K = '#ea323c', '#c42430', '#891e2b'
BELT, BELT_D = '#5d2c28', '#391f21'
GOLD, GOLD_L = '#ffc825', '#ffeb57'
WOOD, WOOD_D, WOOD_DD, WOOD_L = '#bf6f4a', '#8a4836', '#5d2c28', '#e69c69'
BOOK1, BOOK1_D, BOOK1_L = '#0069aa', '#00396d', '#0098dc'
BOOK2, BOOK2_D, BOOK2_L = '#93388f', '#622461', '#ca52c9'
PAGE, PAGE_D = '#f9e6cf', '#f6ca9f'
PENCIL, PENCIL_D = '#ffc825', '#edab50'
GREY, GREY_D = '#c7cfdd', '#92a1b9'

FEET = 66  # bottom row of Nib's feet (he stands on the top ledger)


def stool(c: Canvas):
    # the back leg first, then the two front legs splayed, a crossbar and the round seat
    c.line(31, 82, 32, 115, WOOD_DD, 3)
    for (x0, x1) in [(14, 10), (48, 52)]:
        c.line(x0, 82, x1, 117, WOOD, 3)
        c.line(x0 + 2, 82, x1 + 2, 117, WOOD_D)
    c.rect(12, 103, 41, 2, WOOD_D)
    c.rect(12, 103, 41, 1, WOOD)
    c.ellipse(9, 76, 46, 8, WOOD_D)
    c.ellipse(9, 75, 46, 7, WOOD)
    c.line(14, 77, 26, 76, WOOD_L)


def ledgers(c: Canvas):
    # bottom: a blue ledger, spine to us, with a white label; top: a plum one, a bit smaller
    c.rect(14, 72, 36, 6, BOOK1)
    c.rect(14, 77, 36, 1, BOOK1_D)
    c.rect(14, 72, 36, 1, BOOK1_L)
    c.rect(16, 73, 2, 4, BOOK1_D)
    c.rect(46, 73, 2, 4, BOOK1_D)
    c.rect(26, 73, 12, 4, PAGE)
    c.line(28, 75, 35, 75, GREY_D)
    c.rect(17, 66, 30, 6, BOOK2)
    c.rect(17, 71, 30, 1, BOOK2_D)
    c.rect(17, 66, 30, 1, BOOK2_L)
    c.rect(19, 67, 2, 4, BOOK2_D)
    c.rect(43, 67, 2, 4, BOOK2_D)
    c.rect(27, 67, 10, 4, PAGE)
    c.line(29, 69, 34, 69, GREY_D)


def tail(c: Canvas):
    # a neat tail curled along the top ledger to the right, tip turned up
    c.line(40, 61, 47, 64, SCALE_G, 3)
    c.line(47, 64, 52, 63, SCALE_G, 3)
    c.line(53, 63, 55, 59, SCALE_G, 2)
    c.set(56, 58, SCALE_G)
    c.line(42, 64, 52, 65, SCALE_D)


def body(c: Canvas):
    y = FEET
    # legs and feet
    for fx in (23, 34):
        c.ellipse(fx, y - 8, 7, 8, SCALE_G)
        c.rect(fx - 1, y - 2, 9, 3, SCALE_G)
        c.rect(fx - 1, y, 9, 1, SCALE_D)
        for k in (0, 4, 7):
            c.set(fx - 1 + k, y, HORN)
    # pear-shaped body, shade on the right
    c.ellipse(22, 43, 21, 19, SCALE_D)
    c.ellipse(21, 42, 21, 19, SCALE_G)
    c.ellipse(26, 46, 12, 14, BELLY)
    for by in (50, 53, 58):
        c.line(28, by, 35, by, BELLY_D)
    # where the body meets the legs
    c.line(23, 61, 29, 61, SCALE_D)
    c.line(34, 61, 40, 61, SCALE_DD)
    c.line(36, 62, 40, 62, SCALE_D)
    # arms at his sides, a little apart from the body, neat claws
    c.polygon([(22, 45), (17, 50), (15, 58), (18, 59), (20, 52)], SCALE_G)
    c.polygon([(41, 45), (46, 50), (48, 58), (45, 59), (43, 52)], SCALE_D)
    c.line(21, 46, 18, 50, SCALE_L)
    for (x, yy) in [(15, 59), (17, 60), (47, 59), (45, 60)]:
        c.set(x, yy, HORN)
    # belt with a gold buckle
    c.rect(22, 55, 21, 2, BELT)
    c.rect(30, 54, 4, 4, GOLD)
    c.rect(31, 55, 2, 2, BELT)
    c.set(30, 54, GOLD_L)
    # the label-maker on his belt (on his left, our right): a blue box with keys and a label coming out of the top
    c.rect(38, 55, 7, 8, BOOK1)
    c.rect(38, 62, 7, 1, BOOK1_D)
    c.rect(44, 56, 1, 6, BOOK1_D)
    c.rect(39, 56, 5, 2, GREY)  # little screen
    for kx in (39, 41, 43):
        c.set(kx, 59, WHITE)
        c.set(kx, 61, WHITE)
    c.rect(40, 52, 3, 3, WHITE)  # label strip
    c.set(41, 53, GREY_D)


def bow_tie(c: Canvas):
    c.blit(['rr...rr', 'rRr.rRr', 'rRRkRRr', 'rRr.rRr', 'rr...rr'],
           {'r': TIE_D, 'R': TIE, 'k': TIE_K}, 29, 44)
    c.set(30, 45, '#f5555d')
    c.set(34, 45, '#f5555d')


def head(c: Canvas, expr: str):
    # horns, neat and short
    for (x, col, sh) in [(24, HORN, HORN_D), (37, HORN_D, '#e07438')]:
        c.polygon([(x, 22), (x + 1, 14), (x + 3, 13), (x + 4, 22)], col)
        c.line(x + 1, 16, x + 1, 21, sh)
    # left ear fin (the right one goes over the pencil, after the head)
    c.polygon([(19, 30), (12, 27), (14, 33), (12, 37), (19, 37)], SCALE_L)
    # a pencil tucked behind his right ear (our right): it goes in behind the head, the eraser end sticks out
    c.line(38, 28, 53, 22, PENCIL, 2)
    c.line(39, 29, 53, 23, PENCIL_D)
    c.rect(54, 21, 2, 2, BLUSH)  # eraser
    c.set(53, 21, GREY)
    c.set(53, 23, GREY)
    # head: shade crescent on the right, then the scales, a tidy crest of three scales on top
    c.ellipse(19, 20, 28, 26, SCALE_D)
    c.ellipse(18, 19, 27, 25, SCALE_G)
    for x in (29, 32):
        c.rect(x, 17, 2, 3, SCALE_L)
    c.line(24, 22, 29, 21, SCALE_LL)
    c.line(22, 24, 23, 23, SCALE_LL)
    # right ear fin over the pencil
    c.polygon([(45, 30), (52, 27), (50, 33), (52, 37), (45, 37)], SCALE_D)
    # muzzle
    c.ellipse(25, 35, 15, 10, SCALE_D)
    c.ellipse(25, 34, 14, 10, SCALE_L)
    c.set(29, 37, SCALE_DD)
    c.set(35, 37, SCALE_DD)
    # round glasses: frames, then the eyes inside, a glint on each lens
    for gx in (21, 34):
        c.ellipse(gx, 26, 10, 10, FRAME)
        c.ellipse(gx + 1, 27, 8, 8, SCALE_LL)
    c.rect(31, 29, 3, 1, FRAME)  # bridge
    c.line(21, 29, 18, 28, FRAME)  # arms to the ears
    c.line(43, 29, 46, 28, FRAME)
    eyes = {'neutral': 'open', 'happy': 'happy', 'angry': 'lid'}[expr]
    eye5(c, 23, 28, eyes, IRIS, IRIS_D)
    eye5(c, 36, 28, eyes, IRIS, IRIS_D)
    for gx in (21, 34):
        c.set(gx + 7, 28, WHITE)
        c.set(gx + 6, 29, WHITE) if eyes != 'open' else None
        c.set(gx + 7, 29, WHITE)
    # brows above the frames
    tl, tr = {'neutral': ('flat', 'flat'), 'happy': ('up', 'up'), 'angry': ('in', 'in-r')}[expr]
    by = 24 if expr != 'angry' else 25
    brow5(c, 23, by, tl, BROW, 2 if expr == 'angry' else 1)
    brow5(c, 36, by, tr, BROW, 2 if expr == 'angry' else 1)
    # blush (not when cross)
    if expr != 'angry':
        for (x, y) in [(20, 37), (21, 37), (22, 37), (42, 37), (43, 37), (44, 37)]:
            c.set(x, y, BLUSH)
    k = OUTLINE
    mouths = {
        'neutral': ['.......', 'k.....k', '.kkkkk.'],
        'happy': ['kkkkkkk', 'kwmmmwk', '.kmttk.', '..kkk..'],
        'angry': ['.......', '.kkkkk.', 'k.....k'],
    }[expr]
    c.blit(mouths, {'k': k, 'm': MOUTH, 't': TONGUE, 'w': WHITE}, 29, 39)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    stool(c)
    ledgers(c)
    tail(c)
    body(c)
    head(c, expr)
    bow_tie(c)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'happy', 'angry']

if __name__ == '__main__':
    run_sprite('nib', build, EXPRESSIONS)
