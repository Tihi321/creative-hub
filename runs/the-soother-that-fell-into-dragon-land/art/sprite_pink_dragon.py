"""Pink dragon: a round, cheerful singing dragon, bubble-gum pink scales, pale cream belly, big sparkly violet eyes,
small frilly wings, a flower behind one ear, mouth open in a happy O. Sits upright on a grey standing stone."""
from common import Canvas, OUTLINE, WHITE, MOUTH, TONGUE, SPRITE_H, eye5, brow5, run_sprite
from dragonkit import disc, bez, tube, stone, part

W = 88
P, P_L, P_D, P_DD = '#f68187', '#fdd2ed', '#c85086', '#93388f'
CREAM, CREAM_D = '#f9e6cf', '#f6ca9f'
IRIS, IRIS_D = '#db3ffd', '#7a09fa'
BLUSH = '#f5555d'
NOTE, NOTE_L = '#7a09fa', '#db3ffd'
YELLOW, YELLOW_L = '#ffc825', '#ffeb57'
PETAL_D = '#c7cfdd'
LINE = P_DD  # inner contour lines


def tail(t: Canvas):
    pts = bez((56, 84), (84, 96), (78, 68), 30)
    tube(t, pts, 6, 2.5, P_D)
    tube(t, pts, 5, 2, P, dx=-0.7, dy=-0.7)
    t.polygon([(78, 71), (72, 64), (78, 57), (84, 64)], P_D)
    t.polygon([(78, 70), (73, 64), (78, 58), (82, 64)], P)
    t.line(76, 61, 75, 63, P_L)


def wing(t: Canvas):
    t.polygon([(33, 52), (19, 40), (13, 42), (11, 50), (13, 58), (19, 62), (30, 62)], P_D)
    for (sx, sy) in [(13, 56), (17, 60), (22, 62)]:
        disc(t, sx, sy, 2.6, P_D)
    t.polygon([(32, 53), (19, 42), (14, 44), (13, 50), (15, 56), (20, 59), (30, 60)], P_L)
    for (sx, sy) in [(14.5, 55.5), (18, 58.5), (22.5, 60)]:
        disc(t, sx, sy, 1.8, P_L)
    t.line(19, 42, 31, 54, P_D)
    t.line(14, 48, 30, 55, P_D)
    t.line(16, 56, 29, 57, P_D)


def torso(t: Canvas):
    t.ellipse(27, 40, 36, 55, P_D)
    t.ellipse(26, 39, 35, 54, P)
    t.ellipse(34, 48, 20, 44, CREAM_D)
    t.ellipse(34, 47, 19, 44, CREAM)
    for by in (60, 67, 74, 81, 88):
        for xx in range(33, 56):
            if t.get(xx, by) == CREAM:
                t.set(xx, by, CREAM_D)


def haunch(x, shade):
    def f(t: Canvas):
        if shade:
            t.ellipse(x, 74, 15, 19, P_D)
            t.ellipse(x, 74, 13, 18, P)
        else:
            t.ellipse(x, 74, 15, 19, P)
            t.ellipse(x + 3, 78, 2, 4, P_L)
    return f


def foot(x):
    def f(t: Canvas):
        t.ellipse(x, 91, 12, 9, P_D)
        t.ellipse(x, 90, 11, 9, P)
        for k in range(3):
            t.set(x + 2 + 3 * k, 99, CREAM)
            t.set(x + 2 + 3 * k, 98, CREAM)
    return f


def arm_l(t: Canvas):
    tube(t, [(30, 51), (32, 58), (37, 64)], 3.6, 3.0, P)
    t.ellipse(36, 61, 8, 7, P)
    t.set(32, 52, P_L)
    t.set(32, 53, P_L)
    for k in range(3):
        t.set(37 + 2 * k, 67, CREAM)


def arm_r(t: Canvas):
    tube(t, [(58, 51), (56, 58), (51, 64)], 3.6, 3.0, P_D)
    tube(t, [(57.5, 50.5), (55.5, 57.5), (50.5, 63.5)], 2.8, 2.2, P)
    t.ellipse(44, 61, 8, 7, P_D)
    t.ellipse(44, 61, 7, 6, P)
    for k in range(3):
        t.set(45 + 2 * k, 67, CREAM)


def ears(t: Canvas):
    t.polygon([(26, 19), (15, 14), (17, 23), (15, 30), (26, 30)], P_D)
    t.polygon([(25, 20), (18, 17), (19, 23), (18, 28), (25, 28)], P_L)
    t.polygon([(62, 19), (73, 14), (71, 23), (73, 30), (62, 30)], P_D)
    t.polygon([(63, 20), (70, 17), (69, 23), (70, 28), (63, 28)], P)


def horns(t: Canvas):
    t.polygon([(31, 15), (37, 12), (29, 2)], CREAM_D)
    t.polygon([(32, 14), (35, 12), (30, 4)], CREAM)
    t.polygon([(57, 15), (51, 12), (59, 2)], CREAM_D)
    t.polygon([(56, 14), (53, 12), (58, 4)], CREAM)


def skull(t: Canvas):
    t.ellipse(24, 10, 42, 35, P_D)
    t.ellipse(23, 9, 41, 34, P)
    t.ellipse(29, 12, 10, 5, P_L)
    t.ellipse(33, 29, 23, 14, CREAM_D)
    t.ellipse(33, 28, 22, 14, CREAM)


def curl(t: Canvas):
    t.blit(['..pp.', '.p..p', '.p...', '..pp.'], {'p': P}, 41, 6)
    t.set(42, 7, P_L)


def flower(t: Canvas):
    for (fx, fy) in [(71, 12), (75, 14.5), (73.5, 19), (68.5, 19), (67, 14.5)]:
        disc(t, fx, fy, 2.3, WHITE)
    for (fx, fy) in [(73, 20), (69, 20), (75, 16)]:
        t.set(fx, fy, PETAL_D)
    disc(t, 71.5, 16, 1.6, YELLOW)
    t.set(71, 15, YELLOW_L)


def face(c: Canvas, expr: str):
    c.set(40, 32, P_D)
    c.set(41, 32, P_D)
    c.set(47, 32, P_D)
    c.set(48, 32, P_D)
    eyes = {'neutral': 'open'}[expr]
    for (ex, lash) in ((31, -1), (52, 1)):
        eye5(c, ex, 20, eyes, IRIS, IRIS_D, lash=lash)
        if eyes == 'open':
            c.set(ex + 3, 24, WHITE)  # second sparkle
    brow5(c, 31, 17, 'up', P_DD)
    brow5(c, 52, 17, 'up', P_DD)
    for (bx, by) in [(27, 28), (28, 28), (29, 28), (28, 29), (58, 28), (59, 28), (60, 28), (59, 29)]:
        c.set(bx, by, BLUSH)
    c.blit(['.kkkk.', 'kmmmmk', 'kmmmmk', 'kmmmmk', 'kmttmk', '.kkkk.'], {'k': OUTLINE, 'm': MOUTH, 't': TONGUE}, 41, 35)


def note(t: Canvas):
    t.blit(['...nn.', '...nNn', '...n.N', '...n..', '.nnn..', 'nNnn..', '.nn...'], {'n': NOTE, 'N': NOTE_L}, 75, 27)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    stone(c, 18, 90, 52, seed=5)
    part(c, tail, LINE)
    part(c, wing, LINE)
    part(c, lambda t: (wing(w := Canvas(W, SPRITE_H)), t.paste(w.flip())), LINE)
    part(c, torso, LINE)
    part(c, haunch(22, False), LINE)
    part(c, haunch(51, True), LINE)
    part(c, foot(25), LINE)
    part(c, foot(51), LINE)
    part(c, arm_l, LINE)
    part(c, arm_r, LINE)
    part(c, ears, LINE)
    part(c, horns, LINE)
    part(c, skull, LINE)
    part(c, curl, LINE)
    part(c, flower, PETAL_D)
    face(c, expr)
    note(c)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral']

if __name__ == '__main__':
    run_sprite('pink_dragon', build, EXPRESSIONS)
