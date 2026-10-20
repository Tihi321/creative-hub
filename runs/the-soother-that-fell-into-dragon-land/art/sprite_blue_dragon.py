"""Blue dragon: a tall, slim singing dragon, sky-blue scales, white belly, sleepy half-closed teal eyes, a long
swaying neck, a curly tail tip and a tiny striped scarf. Calm and dreamy. Sits on a grey standing stone."""
import math

from common import Canvas, OUTLINE, WHITE, MOUTH, TONGUE, SPRITE_H, eye5, brow5, run_sprite
from dragonkit import disc, bez, tube, stone, part

W = 84
B, B_L, B_D, B_DD = '#00cdf9', '#94fdff', '#0098dc', '#0069aa'
BELLY, BELLY_D = WHITE, '#c7cfdd'
IRIS, IRIS_D = '#1e6f50', '#134c4c'
SC, SC_D, SC2 = '#ea323c', '#c42430', '#ffeb57'
HORN, HORN_D = '#f9e6cf', '#f6ca9f'
BLUSH = '#f68187'
LINE = B_DD

NECK = bez((47, 59), (50, 42), (33, 33), 30)


def tail(t: Canvas):
    pts = bez((56, 88), (78, 100), (74, 80), 24)
    cx, cy = 70.5, 76.5
    for i in range(1, 26):
        a = -0.2 + i / 25 * 1.7 * math.pi
        r = 4.5 - i / 25 * 2.6
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    tube(t, pts, 5, 1.6, B_D)
    tube(t, pts, 4.2, 1.2, B, dx=-0.6, dy=-0.6)


def wing(t: Canvas):
    t.polygon([(37, 60), (27, 53), (25, 57), (27, 65), (32, 68), (37, 67)], B_D)
    t.polygon([(37, 61), (28, 56), (28, 63), (32, 66), (37, 65)], B_L)
    t.line(28, 56, 35, 63, B_D)


def wing_r(t: Canvas):
    w = Canvas(W, SPRITE_H)
    wing(w)
    _mirror(w, t, 91)


def torso(t: Canvas):
    t.ellipse(33, 56, 28, 41, B_D)
    t.ellipse(32, 55, 27, 40, B)
    t.ellipse(39, 62, 15, 32, BELLY_D)
    t.ellipse(39, 61, 14, 32, BELLY)
    for by in (70, 76, 82, 88):
        for xx in range(38, 54):
            if t.get(xx, by) == BELLY:
                t.set(xx, by, BELLY_D)


def haunch(x, shade):
    def f(t: Canvas):
        t.ellipse(x, 78, 13, 17, B_D if shade else B)
        if shade:
            t.ellipse(x, 78, 11, 16, B)
        else:
            t.ellipse(x + 3, 81, 2, 4, B_L)
    return f


def foot(x):
    def f(t: Canvas):
        t.ellipse(x, 92, 11, 8, B_D)
        t.ellipse(x, 91, 10, 8, B)
        for k in range(3):
            t.set(x + 2 + 3 * k, 98, BELLY)
    return f


def arms(t: Canvas):
    """Thin arms down the sides, paws resting on the knees."""
    tube(t, [(35, 64), (33, 72), (34, 78)], 2.4, 2.2, B)
    tube(t, [(57, 64), (59, 72), (57, 78)], 2.4, 2.2, B_D)
    tube(t, [(56.6, 63.6), (58.6, 71.6), (56.6, 77.6)], 1.7, 1.5, B)
    t.ellipse(31, 77, 7, 5, B)
    t.ellipse(54, 77, 7, 5, B_D)
    t.ellipse(54, 77, 6, 4, B)
    for k in range(3):
        t.set(32 + 2 * k, 82, BELLY)
        t.set(55 + 2 * k, 82, BELLY)


def neck(t: Canvas):
    tube(t, NECK, 6.5, 5.5, B_D)
    tube(t, NECK, 5.8, 4.8, B, dx=-0.8)
    tube(t, NECK, 2.6, 2.2, BELLY, dx=-0.6)
    for i in range(6, 28, 4):  # throat bands
        x, y = NECK[i]
        for dx in (-2, -1, 0, 1):
            if t.get(round(x + dx - 0.6), round(y)) == BELLY:
                t.set(round(x + dx - 0.6), round(y), BELLY_D)


def neck_fins(t: Canvas):
    for i in (8, 14, 20, 26):
        (x0, y0), (x1, y1) = NECK[i - 1], NECK[i + 1]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = dy / L, -dx / L  # the outer (back) side of the curve
        if nx < 0:
            nx, ny = -nx, -ny
        bx, by = NECK[i]
        t.polygon([(bx + nx * 4 - dx, by + ny * 4 - dy), (bx + nx * 9, by + ny * 9 - 1), (bx + nx * 4 + dx * 1.5, by + ny * 4 + dy * 1.5)], B_DD)


def scarf(t: Canvas):
    t.ellipse(38, 56, 20, 7, SC)
    for xx in range(38, 58):
        if (xx // 2) % 2 == 0:
            for yy in range(56, 63):
                if t.get(xx, yy) == SC:
                    t.set(xx, yy, SC2)
    for yy in range(56, 63):
        for xx in range(52, 58):
            g = t.get(xx, yy)
            if g == SC:
                t.set(xx, yy, SC_D)
    # the hanging end
    for j in range(10):
        col = SC if (j // 2) % 2 == 0 else SC2
        t.rect(52 + j // 4, 61 + j, 4, 1, col)
    for k in range(3):
        t.set(53 + 2 + k, 72, SC)
    t.set(54, 72, SC_D)


def ears(t: Canvas):
    t.polygon([(17, 18), (7, 13), (9, 21), (8, 27), (17, 27)], B_D)
    t.polygon([(16, 19), (10, 16), (11, 21), (10, 25), (16, 25)], B_L)
    t.polygon([(49, 18), (59, 13), (57, 21), (58, 27), (49, 27)], B_D)
    t.polygon([(50, 19), (56, 16), (55, 21), (56, 25), (50, 25)], B)


def horns(t: Canvas):
    t.polygon([(22, 14), (28, 11), (19, 1)], HORN_D)
    t.polygon([(23, 13), (26, 11), (20, 3)], HORN)
    t.polygon([(44, 14), (38, 11), (47, 1)], HORN_D)
    t.polygon([(43, 13), (40, 11), (46, 3)], HORN)


def skull(t: Canvas):
    t.ellipse(15, 10, 38, 30, B_D)
    t.ellipse(14, 9, 37, 29, B)
    t.ellipse(19, 12, 9, 4, B_L)
    t.ellipse(22, 25, 23, 13, BELLY_D)
    t.ellipse(22, 24, 22, 13, BELLY)


def face(c: Canvas, expr: str):
    c.set(29, 28, B_DD)
    c.set(30, 28, B_DD)
    c.set(36, 28, B_DD)
    c.set(37, 28, B_DD)
    eyes = {'neutral': 'half', 'happy': 'happy'}[expr]
    eye5(c, 21, 17, eyes, IRIS, IRIS_D)
    eye5(c, 40, 17, eyes, IRIS, IRIS_D)
    if expr == 'neutral':  # heavy sleepy lids in scale colour above the lid line
        for ex in (21, 40):
            c.rect(ex, 18, 5, 1, B_D)
    tilt = {'neutral': 'flat', 'happy': 'up'}[expr]
    brow5(c, 21, 15, tilt, B_DD)
    brow5(c, 40, 15, tilt, B_DD)
    for (bx, by) in [(18, 25), (19, 25), (20, 25), (46, 25), (47, 25), (48, 25)]:
        c.set(bx, by, BLUSH)
    mouths = {
        'neutral': ['k.....k', '.kkkkk.'],
        'happy': ['kkkkkkk', 'kmmmmmk', '.kmttk.', '..kkk..'],
    }[expr]
    c.blit(mouths, {'k': OUTLINE, 'm': MOUTH, 't': TONGUE}, 30, 31)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    stone(c, 22, 92, 46, seed=11)
    part(c, tail, LINE)
    part(c, wing, LINE)
    part(c, wing_r, LINE)
    part(c, torso, LINE)
    part(c, haunch(29, False), LINE)
    part(c, haunch(52, True), LINE)
    part(c, foot(30), LINE)
    part(c, foot(52), LINE)
    part(c, arms, LINE)
    part(c, neck_fins, LINE)
    part(c, neck, LINE)
    part(c, scarf, SC_D)
    part(c, ears, LINE)
    part(c, horns, LINE)
    part(c, skull, LINE)
    face(c, expr)
    c.outline(OUTLINE)
    return c


def _mirror(src: Canvas, dst: Canvas, axis2: int):
    """Paste src mirrored around x = axis2 / 2."""
    for yy in range(src.h):
        for xx in range(src.w):
            p = src.px[yy][xx]
            if p is not None:
                dst.set(axis2 - xx, yy, p)


EXPRESSIONS = ['neutral', 'happy']

if __name__ == '__main__':
    run_sprite('blue_dragon', build, EXPRESSIONS)
