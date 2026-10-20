"""Mama: Petra and Pip's mother, about thirty-five. Warm round freckled face, kind green eyes, shoulder-length wavy
brown hair tied back with a red scarf, blue cardigan over a white shirt, flowered apron, brown trousers.
Drawn from mid-thigh up so she fills the 120-row canvas, hands folded in front of her apron."""
import math

from common import Canvas, OUTLINE, SKIN, SKIN_D, SKIN_L, BLUSH, MOUTH, TONGUE, WHITE, SPRITE_H, eye5, brow5, run_sprite

W = 64
HAIR, HAIR_D, HAIR_L = '#8a4836', '#5d2c28', '#bf6f4a'
SCARF, SCARF_D, SCARF_L = '#ea323c', '#c42430', '#f5555d'
CARD, CARD_D, CARD_L, CARD_DD = '#0069aa', '#00396d', '#0098dc', '#03193f'
SHIRT, SHIRT_D = WHITE, '#c7cfdd'
APRON, APRON_D, APRON_L = '#fdd2ed', '#f68187', WHITE
PETAL, PETAL_D, PETAL_C, LEAF = '#ea323c', '#c42430', '#ffc825', '#5ac54f'
TROU, TROU_D, TROU_L = '#bf6f4a', '#8a4836', '#e69c69'
IRIS, IRIS_D = '#5ac54f', '#1e6f50'
FRECKLE = '#bf6f4a'
BROW = HAIR_D


def hair_back(c: Canvas):
    # the crown, and the waves falling behind the neck to the shoulders
    c.ellipse(12, 1, 40, 38, HAIR_D)
    pts = [(12, 18), (52, 18), (54, 34), (53, 46)]
    for i, x in enumerate(range(53, 10, -3)):
        pts.append((x, 47 + (2 if i % 2 else 0)))
    pts += [(11, 46), (10, 34)]
    c.polygon(pts, HAIR_D)


def body(c: Canvas):
    # trousers (mid thigh to the canvas bottom)
    c.rect(14, 92, 17, 28, TROU)
    c.rect(33, 92, 17, 28, TROU_D)
    c.rect(31, 100, 2, 20, TROU_D)
    c.line(16, 104, 16, 119, TROU_L)
    # cardigan
    c.polygon([(19, 42), (45, 42), (53, 47), (55, 60), (52, 98), (12, 98), (9, 60), (11, 47)], CARD)
    c.polygon([(36, 42), (45, 42), (53, 47), (55, 60), (52, 98), (40, 98)], CARD_D)
    c.rect(12, 95, 41, 3, CARD_D)  # ribbed hem
    for x in range(13, 52, 2):
        c.set(x, 96, CARD_DD)
    # white shirt in the open front, with its collar
    c.polygon([(25, 42), (39, 42), (40, 98), (24, 98)], SHIRT)
    c.polygon([(34, 42), (39, 42), (40, 98), (36, 98)], SHIRT_D)
    c.polygon([(26, 42), (31, 47), (26, 49), (23, 43)], SHIRT)
    c.polygon([(38, 42), (33, 47), (38, 49), (41, 43)], SHIRT_D)
    # open cardigan edges
    c.line(24, 44, 23, 97, CARD_L)
    c.line(40, 44, 41, 97, CARD_DD)
    for by in (50, 57, 64):  # buttons on the open front
        c.rect(42, by, 2, 2, SHIRT_D)
        c.set(42, by, WHITE)
    # neck
    c.polygon([(27, 34), (37, 34), (36, 44), (32, 47), (28, 44)], SKIN_D)
    c.line(29, 44, 32, 46, SKIN)


def apron(c: Canvas):
    # straps over the shoulders
    c.line(26, 46, 26, 55, APRON_D)
    c.line(38, 46, 38, 55, APRON_D)
    # bib and skirt
    c.polygon([(25, 54), (39, 54), (40, 74), (24, 74)], APRON)
    skirt = [(18, 74), (46, 74), (51, 112)]
    for i, x in enumerate(range(51, 12, -3)):
        skirt.append((x, 112 + (2 if i % 2 else 0)))
    skirt += [(13, 112)]
    c.polygon(skirt, APRON)
    # soft shade on the right, pockets, the hem frill
    c.line(46, 78, 50, 111, APRON_D)
    c.line(45, 82, 48, 104, APRON_D)
    c.rect(24, 54, 16, 1, APRON_D)
    for x in range(13, 52):
        for y in range(104, 116):
            if c.get(x, y) == APRON and c.get(x, y + 1) in (None, TROU, TROU_D, TROU_L):
                c.set(x, y, APRON_D)
                break
    # waist band
    c.rect(18, 74, 28, 2, APRON_D)
    # flowers: red petals, a yellow centre, a green leaf
    for (x, y) in [(28, 59), (35, 67), (20, 82), (31, 98), (43, 86), (18, 101), (40, 104), (25, 108)]:
        c.blit(['.p.', 'pcp', '.P.'], {'p': PETAL, 'P': PETAL_D, 'c': PETAL_C}, x, y)
        c.set(x + 3, y + 2, LEAF)
    for (x, y) in [(32, 56), (24, 66), (38, 61), (27, 89), (47, 97), (21, 92)]:
        c.set(x, y, APRON_L)


def arms(c: Canvas):
    # upper arms down the sides, a dark crease where they meet the body
    c.polygon([(11, 45), (18, 48), (19, 75), (9, 75), (8, 56)], CARD)
    c.line(10, 50, 9, 72, CARD_L)
    c.line(11, 48, 10, 60, CARD_L)
    c.line(19, 52, 19, 74, CARD_DD)
    c.polygon([(53, 45), (46, 48), (45, 75), (55, 75), (56, 56)], CARD_D)
    c.line(54, 52, 55, 72, CARD)
    c.line(45, 52, 45, 74, CARD_DD)
    # forearms folding in to the hands in front of the apron
    c.polygon([(9, 72), (19, 72), (29, 83), (26, 91), (11, 81)], CARD)
    c.line(12, 75, 22, 85, CARD_L)
    c.line(19, 73, 28, 83, CARD_DD)
    c.polygon([(55, 72), (45, 72), (35, 83), (38, 91), (53, 81)], CARD_D)
    c.line(45, 73, 36, 83, CARD_DD)
    # cuffs and folded hands
    c.polygon([(23, 82), (28, 84), (25, 91), (20, 88)], CARD_D)
    c.polygon([(41, 82), (36, 84), (39, 91), (44, 88)], CARD_DD)
    c.ellipse(26, 83, 12, 9, SKIN)
    c.ellipse(32, 84, 6, 8, SKIN_D)
    c.line(31, 85, 31, 90, SKIN_D)
    c.line(28, 87, 30, 87, SKIN_D)
    c.set(28, 84, SKIN_L)
    c.set(29, 84, SKIN_L)


def head(c: Canvas, expr: str):
    # ears
    c.ellipse(14, 20, 5, 8, SKIN_D)
    c.ellipse(45, 20, 5, 8, SKIN_D)
    # face: shade crescent on the right
    c.ellipse(17, 6, 31, 35, SKIN_D)
    c.ellipse(16, 5, 31, 35, SKIN)
    eyes = {'neutral': 'open', 'happy': 'happy'}[expr]
    eye5(c, 22, 21, eyes, IRIS, IRIS_D, lash=-1)
    eye5(c, 37, 21, eyes, IRIS, IRIS_D, lash=1)
    brow5(c, 22, 18, 'flat' if expr == 'neutral' else 'up', BROW)
    brow5(c, 37, 18, 'flat' if expr == 'neutral' else 'up', BROW)
    # nose, blush, freckles
    c.set(32, 28, SKIN_D)
    c.set(31, 29, SKIN_D)
    for (x, y) in [(19, 29), (20, 29), (21, 29), (20, 30), (42, 29), (43, 29), (44, 29), (43, 30)]:
        c.set(x, y, BLUSH)
    for (x, y) in [(23, 28), (25, 29), (24, 30), (38, 28), (40, 29), (39, 30)]:
        c.set(x, y, FRECKLE)
    k = OUTLINE
    rows, mx, my = {
        'neutral': (['k......k', '.kkkkkk.'], 28, 32),
        'happy': (['kkkkkkkk', 'kmmmmmmk', '.kmttmk.', '..kkkk..'], 28, 32),
    }[expr]
    c.blit(rows, {'k': k, 'm': MOUTH, 't': TONGUE}, mx, my)


def hair_front(c: Canvas):
    # side-swept wavy fringe from a parting on the left
    c.polygon([(16, 22), (16, 12), (21, 5), (30, 2), (40, 3), (47, 9), (48, 18), (48, 24), (45, 17), (41, 14),
               (36, 15), (31, 12), (27, 13), (23, 11), (21, 15), (19, 15)], HAIR)
    # wavy locks framing the face down to the shoulders
    c.polygon([(17, 12), (20, 16), (18, 22), (19, 29), (16, 35), (18, 41), (14, 46), (11, 42), (13, 36), (11, 29),
               (13, 22), (14, 15)], HAIR)
    c.polygon([(47, 12), (44, 17), (46, 22), (45, 29), (48, 35), (46, 41), (50, 46), (53, 42), (51, 36), (53, 29),
               (51, 22), (50, 15)], HAIR)
    # wave highlights
    c.line(22, 7, 28, 4, HAIR_L)
    c.line(32, 4, 38, 5, HAIR_L)
    c.line(25, 10, 30, 9, HAIR_L)
    c.line(14, 24, 15, 29, HAIR_L)
    c.line(14, 37, 15, 41, HAIR_L)
    c.line(13, 17, 14, 21, HAIR_L)
    c.line(50, 25, 51, 30, HAIR_D)
    c.line(49, 37, 50, 41, HAIR_D)
    # the red scarf tied round the head, a bow on the upper right
    for x in range(14, 51):
        t = (x + 0.5 - 32) / 18.5
        y = round(21 - 18.5 * math.sqrt(max(0.0, 1 - t * t)) + 2)
        if y > 17:
            continue
        c.set(x, y, SCARF_L)
        c.set(x, y + 1, SCARF)
        c.set(x, y + 2, SCARF_D)
    c.blit([
        '.ooo.....ooo.',
        'oLLoo...ooodd',
        'oLoood.dooodd',
        'ooooodKdoooDd',
        '.ooood.dooDd.',
        '..oooodddDd..',
        '....oodd.....',
        '...oo..dd....',
        '...oo...dd...',
        '..oo.....dd..',
        '..o.......d..',
    ], {'o': SCARF, 'L': SCARF_L, 'd': SCARF_D, 'D': '#891e2b', 'K': SCARF_L}, 44, 2)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    hair_back(c)
    body(c)
    apron(c)
    arms(c)
    head(c, expr)
    hair_front(c)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'happy']

if __name__ == '__main__':
    run_sprite('mama', build, EXPRESSIONS)
