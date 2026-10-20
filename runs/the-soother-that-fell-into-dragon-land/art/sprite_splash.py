"""Splash: a round, chubby mud dragon the size of a big dog, smooth chocolate-brown scales speckled with lighter mud
spots, drippy little wings, round yellow eyes, a big grin with a tongue that pokes out like a happy dog. Drawn
mid-bounce ("Boing!") above a little mud puddle that splashes up drops."""
from common import Canvas, OUTLINE, WHITE, MOUTH, TONGUE, SPRITE_H, eye5, brow5, run_sprite
from dragonkit import disc, tube, part

W = 72
M, M_L, M_D = '#8a4836', '#bf6f4a', '#5d2c28'
SPOT, SPOT_L = '#bf6f4a', '#e69c69'
BELLY, BELLY_D = '#e69c69', '#bf6f4a'
IRIS, IRIS_D = '#ffc825', '#ed7614'
HORN, HORN_D = '#f6ca9f', '#e69c69'
CLAW = '#f9e6cf'
BLUSH = '#f68187'
TONGUE_L = '#f68187'
LINE = M_D


def puddle(c: Canvas):
    c.ellipse(5, 109, 62, 10, M_D)
    c.ellipse(9, 110, 54, 7, M)
    c.line(16, 111, 28, 111, M_L)
    c.line(44, 115, 54, 115, M_L)
    # a little crown on the rim, then drops flying up and out
    for x in (10, 15, 55, 60):
        c.blit(['.d.', 'dDd', 'ddd'], {'d': M, 'D': M_L}, x, 106)
    drop = ['.d..', 'dDd.', 'dddd', '.dd.']
    for (x, y, f) in [(4, 99, False), (11, 94, False), (19, 100, False), (61, 94, True), (66, 99, True), (49, 100, True),
                      (24, 86, False), (45, 88, True)]:
        c.blit(drop, {'d': M, 'D': M_L}, x, y, flip=f)


def wing(t: Canvas):
    t.polygon([(15, 28), (6, 14), (1, 22), (1, 33), (5, 37), (15, 38)], M_D)
    for (sx, sy) in [(3, 35), (8, 37), (13, 38)]:
        disc(t, sx, sy, 2.2, M_D)
    t.polygon([(14, 29), (6, 17), (3, 23), (3, 32), (6, 35), (14, 36)], M)
    t.line(6, 17, 13, 31, M_D)
    t.line(3, 27, 12, 33, M_D)
    for (x, h) in [(2, 3), (8, 5), (13, 3)]:  # mud drips off the wing
        t.rect(x, 39, 2, h, M_D)


def wing_r(t: Canvas):
    w = Canvas(W, SPRITE_H)
    wing(w)
    for yy in range(w.h):
        for xx in range(w.w):
            if w.px[yy][xx]:
                t.set(71 - xx, yy, w.px[yy][xx])


def tail(t: Canvas):
    """A short tail trailing down behind the bounce, with a little spade tip."""
    tube(t, [(50, 58), (58, 63), (62, 70)], 4.0, 2.0, M_D)
    tube(t, [(49.6, 57.4), (57.6, 62.4), (61.4, 69.4)], 3.0, 1.2, M)
    t.polygon([(62, 68), (66, 72), (62, 77), (58, 72)], M_D)
    t.polygon([(62, 70), (64, 72), (62, 75), (60, 72)], M)


def leg(x, shade):
    def f(t: Canvas):
        col = M_D if shade else M
        tube(t, [(x + 6, 58), (x + 6, 72)], 4.8, 4.0, col)
        t.ellipse(x, 72, 13, 8, col)
        if shade:
            tube(t, [(x + 5.5, 58), (x + 5.5, 72)], 4.0, 3.2, M)
            t.ellipse(x, 72, 12, 7, M)
        for k in range(3):
            t.set(x + 2 + 4 * k, 78, CLAW)
        # mud splashed on the feet, and a drip falling off
        for (dx, dy) in [(3, 73), (4, 73), (8, 75), (9, 74), (6, 66), (5, 63)]:
            t.set(x + dx, dy, M_D)
        t.set(x + 4, 74, SPOT_L)
        t.set(x + 5, 74, SPOT_L)
        t.rect(x + 9, 79, 1, 2, M_D)
        t.rect(x + 3, 79, 1, 1, M_D)
    return f


def ball(t: Canvas):
    t.ellipse(11, 13, 52, 52, M_D)
    t.ellipse(10, 12, 50, 50, M)
    t.ellipse(15, 15, 14, 9, M_L)
    t.ellipse(17, 16, 5, 3, SPOT_L)
    t.ellipse(21, 45, 30, 19, BELLY_D)
    t.ellipse(21, 44, 29, 18, BELLY)
    for by in (50, 56):
        for xx in range(21, 51):
            if t.get(xx, by) == BELLY:
                t.set(xx, by, BELLY_D)
    t.ellipse(25, 30, 23, 14, M_D)
    t.ellipse(25, 29, 22, 14, SPOT)
    t.ellipse(28, 30, 6, 2, SPOT_L)
    # lighter mud spots
    for (x, y) in [(32, 16), (44, 15), (52, 22), (13, 31), (56, 33), (16, 40), (54, 44), (39, 20), (47, 51), (14, 50)]:
        t.blit(['ss', 'sS'], {'s': SPOT, 'S': SPOT_L}, x, y)
    for (x, y) in [(27, 19), (50, 28), (12, 36), (57, 40), (37, 14), (19, 55)]:
        t.set(x, y, SPOT)


def horns(t: Canvas):
    t.polygon([(25, 15), (31, 13), (25, 5)], HORN_D)
    t.polygon([(26, 14), (29, 13), (25, 7)], HORN)
    t.polygon([(47, 15), (41, 13), (47, 5)], HORN_D)
    t.polygon([(46, 14), (43, 13), (47, 7)], HORN)


def paw_l(t: Canvas):
    tube(t, [(15, 46), (19, 52)], 3.2, 3.0, M)
    t.ellipse(17, 50, 7, 6, M)
    for k in range(3):
        t.set(18 + 2 * k, 55, CLAW)


def paw_r_down(t: Canvas):
    tube(t, [(57, 46), (53, 52)], 3.2, 3.0, M_D)
    t.ellipse(48, 50, 7, 6, M_D)
    t.ellipse(48, 50, 6, 5, M)
    for k in range(3):
        t.set(48 + 2 * k, 55, CLAW)


def paw_r_chin(t: Canvas):
    """Thinking: the right paw comes up under the chin and taps it with one claw."""
    tube(t, [(57, 48), (51, 48), (44, 46)], 3.2, 2.8, M_D)
    tube(t, [(56.5, 47.4), (50.5, 47.4), (43.5, 45.4)], 2.4, 2.0, M)
    t.ellipse(37, 42, 9, 7, M_D)
    t.ellipse(37, 42, 8, 6, M)
    t.set(39, 43, M_L)
    t.rect(38, 39, 2, 3, M)  # the tapping finger
    t.set(38, 39, CLAW)
    t.set(39, 39, CLAW)
    t.set(41, 48, CLAW)
    t.set(43, 47, CLAW)


def face(c: Canvas, expr: str):
    eyes = {'neutral': 'open', 'happy': 'open', 'thinking': 'up', 'sad': 'teary'}[expr]
    c.set(32, 33, M_D)
    c.set(39, 33, M_D)
    eye5(c, 25, 24, eyes, IRIS, IRIS_D)
    eye5(c, 42, 24, eyes, IRIS, IRIS_D)
    if eyes in ('open', 'teary'):
        for ex in (25, 42):
            c.set(ex + 3, 27, WHITE)
    tl, tr = {'neutral': ('flat', 'flat'), 'happy': ('up', 'up'), 'thinking': ('flat', 'raised'),
              'sad': ('sad', 'sad-r')}[expr]
    brow5(c, 25, 21, tl, OUTLINE)
    brow5(c, 42, 21, tr, OUTLINE)
    for (bx, by) in [(20, 33), (21, 33), (22, 33), (21, 34), (49, 33), (50, 33), (51, 33), (50, 34)]:
        c.set(bx, by, BLUSH)
    k = OUTLINE
    mouths = {
        'neutral': (['k........k', '.kkkkkkkk.'], 31, 37),
        'happy': (['k............k', '.kkkkkkkkkkkk.', '.kmmmmmmmmmmk.', '..kmmmmttttmk.', '...kkkttTTtk..', '.....kttTttk..',
                   '.....kttttk...', '......kkkk....'], 29, 36),
        'thinking': (['.kkkk.', 'k.....'], 30, 37),
        'sad': (['k........k', '.kkk..kkk.', '....kk....'], 31, 37),
    }
    rows, mx, my = mouths[expr]
    c.blit(rows, {'k': k, 'm': MOUTH, 't': TONGUE, 'T': TONGUE_L}, mx, my)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    puddle(c)
    part(c, wing, LINE)
    part(c, wing_r, LINE)
    part(c, tail, LINE)
    part(c, leg(17, False), LINE)
    part(c, leg(42, True), LINE)
    part(c, ball, LINE)
    part(c, horns, LINE)
    part(c, paw_l, LINE)
    part(c, paw_r_chin if expr == 'thinking' else paw_r_down, LINE)
    face(c, expr)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'happy', 'thinking', 'sad']

if __name__ == '__main__':
    run_sprite('splash', build, EXPRESSIONS)
