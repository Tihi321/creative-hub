"""bg_singing_dragons_chorus_day: a grassy hilltop with a ring of standing stones (the dragons, as sprites, sit on
them), humming flowers with music notes, green sky with fluffy clouds, rolling hills behind (240x135, Endesga 64)."""
import math
import random

from common import OUT, Canvas, Studio
from pxcanvas import BAYER4

E64 = {
    '#ff0040', '#131313', '#1b1b1b', '#272727', '#3d3d3d', '#5d5d5d', '#858585', '#b4b4b4',
    '#ffffff', '#c7cfdd', '#92a1b9', '#657392', '#424c6e', '#2a2f4e', '#1a1932', '#0e071b',
    '#1c121c', '#391f21', '#5d2c28', '#8a4836', '#bf6f4a', '#e69c69', '#f6ca9f', '#f9e6cf',
    '#edab50', '#e07438', '#c64524', '#8e251d', '#ff5000', '#ed7614', '#ffa214', '#ffc825',
    '#ffeb57', '#d3fc7e', '#99e65f', '#5ac54f', '#33984b', '#1e6f50', '#134c4c', '#0c2e44',
    '#00396d', '#0069aa', '#0098dc', '#00cdf9', '#0cf1ff', '#94fdff', '#fdd2ed', '#f389f5',
    '#db3ffd', '#7a09fa', '#3003d9', '#0c0293', '#03193f', '#3b1443', '#622461', '#93388f',
    '#ca52c9', '#c85086', '#f68187', '#f5555d', '#ea323c', '#c42430', '#891e2b', '#571c27',
}

# stone ramp, cool and purple in the shadow, warm white on top
ST_DD, ST_D, ST, ST_L, ST_HI = '#424c6e', '#657392', '#92a1b9', '#c7cfdd', '#ffffff'
MOSS, MOSS_D, MOSS_L = '#5ac54f', '#33984b', '#99e65f'

FLOWERS = {  # petal, petal shade, petal light, centre, centre shade, note colour
    'pink': ('#f389f5', '#c85086', '#fdd2ed', '#ffeb57', '#ffa214', '#93388f'),
    'blue': ('#00cdf9', '#0098dc', '#94fdff', '#ffeb57', '#ffa214', '#0069aa'),
    'yellow': ('#ffeb57', '#ffa214', '#ffffff', '#e07438', '#c64524', '#c64524'),
}

def front_top(x):
    return 80 + 0.0011 * (x - 118) ** 2 + 1.2 * math.sin(x / 11.0)


def cloud(c, x, y, s):
    lit, shade = '#ffffff', '#c7cfdd'
    w = int(38 * s)
    c.ellipse(x, y + int(5 * s), w, int(10 * s), shade)
    c.ellipse(x + 1, y + int(3 * s), w - 2, int(9 * s), lit)
    c.ellipse(x + int(4 * s), y - int(2 * s), int(14 * s), int(12 * s), lit)
    c.ellipse(x + int(13 * s), y - int(7 * s), int(15 * s), int(16 * s), lit)
    c.ellipse(x + int(24 * s), y - int(2 * s), int(11 * s), int(10 * s), lit)


def stone(c, cx, bottom, w, h, seed):
    """A chunky, friendly standing stone: bulging sides, a flat seat on top (seen a little from above),
    lit from the upper right, cool purple-grey shadows, moss at the foot."""
    r = random.Random(seed)
    top = bottom - h
    face = max(2, round(w / 6))           # height of the visible top face
    skew = r.uniform(-0.6, 0.6)           # the stone leans a touch
    bulge = r.uniform(0.06, 0.14)
    spans = {}
    for yy in range(top, bottom + 1):
        t = (yy - top) / h
        hw = w / 2 * (0.76 + bulge * math.sin(math.pi * min(1, t * 1.1)) + 0.18 * t)
        d = yy - top
        if d < face:                       # round the top face into an ellipse
            k = (d + 0.5) / face
            hw *= math.sqrt(max(0.0, 1 - (1 - k) ** 2)) * 0.8 + 0.12
        elif d < face + 3:                 # soft shoulders under the seat
            hw *= (0.93, 0.97, 0.99)[d - face]
        mid = cx + skew * (1 - t) * 2
        spans[yy] = (round(mid - hw), round(mid + hw) - 1)
    # cast shadow on the grass, to the lower left
    c.ellipse(round(cx - w / 2) - 4, bottom - 2, w + 4, 5, MOSS_D if bottom > 100 else MOSS)
    for yy, (x0, x1) in spans.items():
        span = max(1, x1 - x0)
        for xx in range(x0, x1 + 1):
            u = (xx - x0) / span
            d = yy - top
            if d < face:                    # the flat seat on top
                col = ST_HI if (u > 0.5 and d < face - 1) else ST_L
            elif d == face:                 # the rim under the seat
                col = ST if u > 0.25 else ST_D
            elif xx == x0 or u < 0.09:
                col = ST_DD
            elif u < 0.36:
                col = ST_D
            elif u > 0.84 or xx == x1:
                col = ST_L
            else:
                col = ST
            c.set(xx, yy, col)
    # chips and pits: short light ledges with a shadow under them
    for _ in range(max(1, h // 14)):
        y = r.randrange(top + face + 4, bottom - 6)
        x0, x1 = spans[y]
        ln = r.randint(2, 3)
        x = r.randint(x0 + (x1 - x0) // 2, max(x0 + (x1 - x0) // 2, x1 - ln - 1))
        for i in range(ln):
            c.set(x + i, y, ST_L)
            c.set(x + i, y + 1, ST_D)
        c.set(x + ln, y + 1, ST_D)
    # moss: soft clumps at the foot (more on the shadow side) and a cap spilling off the seat
    m = Canvas(c.w, c.h)
    x0, x1 = spans[bottom]
    bw = x1 - x0
    for _ in range(3 if h > 20 else 2):
        ew = r.randint(max(3, bw // 4), max(4, bw // 2))
        ex = x0 - 1 + r.randint(0, max(0, int(bw * 0.55) - ew // 2))
        eh = r.randint(3, max(4, h // 6))
        m.ellipse(ex, bottom - eh + 2, ew, eh + 1, MOSS)
    cx0, cx1 = spans[top + face]
    cw = max(3, (cx1 - cx0) // 2)
    m.ellipse(cx0 - 1, top + face - 1, cw, 3 if h < 20 else 4, MOSS)
    m.set(cx0, top + face + 2, MOSS)
    m.set(cx0 + 2, top + face + 3, MOSS)
    for yy in range(m.h):
        for xx in range(m.w):
            if m.px[yy][xx]:
                if m.get(xx, yy - 1) is None:
                    c.set(xx, yy, MOSS_L)
                elif m.get(xx, yy + 1) is None or m.get(xx - 1, yy) is None:
                    c.set(xx, yy, MOSS_D)
                else:
                    c.set(xx, yy, MOSS)
    # grass blades in front of the foot
    x0, x1 = spans[bottom]
    for xx in range(x0 - 2, x1 + 3):
        if r.random() < 0.5:
            hgt = r.choice([1, 2, 2, 3, 4]) if h > 20 else r.choice([1, 2])
            for k in range(hgt):
                c.set(xx, bottom - k, MOSS_L if k == hgt - 1 and k else MOSS)


def flower(c, cx, cy, rad, kind, stem_to=None, seed=0):
    petal, dark, light, eye, eye_d, _ = FLOWERS[kind]
    r = random.Random(seed)
    if stem_to is not None:
        th = 2 if rad >= 5 else 1
        c.line(cx, cy, cx, stem_to, '#1e6f50', th)
        if th == 2:
            c.line(cx + 1, cy, cx + 1, stem_to, MOSS_D)
        # two leaves, dark with a light upper edge so they read on the grass
        side = r.choice([-1, 1])
        lw = max(4, rad + 2)
        for (frac, sd) in [(0.4, side), (0.72, -side)]:
            ly = cy + rad * 0.6 + (stem_to - cy - rad * 0.6) * frac
            sx = cx + (th if sd > 0 else 0)
            tipx, tipy = sx + sd * lw, ly - lw * 0.7
            wdt = 1.6 if rad >= 6 else 1.2
            # a pointed leaf rising from the stem: base, bulge below, tip, bulge above
            mx, my = (sx + tipx) / 2, (ly + tipy) / 2
            leaf = Canvas(c.w, c.h)
            leaf.polygon([(sx, ly + 1.5), (mx + sd * wdt, my + wdt + 0.8), (tipx, tipy), (mx - sd * wdt, my - wdt + 0.4), (sx, ly - 1)], MOSS)
            for yy in range(leaf.h):
                for xx in range(leaf.w):
                    if leaf.px[yy][xx]:
                        if leaf.get(xx, yy - 1) is None:
                            leaf.set(xx, yy, MOSS_L)
                        elif leaf.get(xx, yy + 1) is None:
                            leaf.set(xx, yy, '#1e6f50')
            c.paste(leaf)
    # petals: round lobes on a darker disc, so the gaps between them read as soft creases
    n = 6 if rad >= 5 else 5
    pr = rad * 0.48
    pts = []
    for k in range(n):
        a = k * 2 * math.pi / n - math.pi / 2 + (0.3 if n == 5 else 0)
        pts.append((cx + math.cos(a) * rad * 0.6, cy + math.sin(a) * rad * 0.6))
    t = Canvas(c.w, c.h)
    for (px, py) in pts:
        t.circle(px, py, pr + 0.6, dark)
    for (px, py) in pts:
        t.circle(px + 0.3, py - 0.3, pr - 0.3, petal)
    for (px, py) in pts:  # warm highlight on the upper right of each lobe
        hx, hy = round(px + pr * 0.25), round(py - pr * 0.45)
        if t.get(hx, hy) == petal:
            t.set(hx, hy, light)
            if rad >= 6 and t.get(hx - 1, hy) == petal:
                t.set(hx - 1, hy, light)
    t.outline(dark)
    c.paste(t)
    cr = max(1.6, rad * 0.38)
    c.circle(cx, cy, cr + 0.5, eye_d)
    c.circle(cx + 0.4, cy - 0.4, cr - 0.2, eye)
    c.set(round(cx + cr * 0.35), round(cy - cr * 0.5), '#ffffff')


NOTE1 = ['...#...', '...##..', '...#.#.', '...#..#', '...#...', '.###...', '####...', '.##....']
NOTE2 = ['...######', '...######', '...#....#', '...#....#', '...#....#', '.###..###', '####.####', '.##...##.']


def note(c, x, y, shape, col):
    """One music note with a white halo, so it reads on sky and grass alike."""
    t = Canvas(c.w, c.h)
    t.blit(NOTE2 if shape == 2 else NOTE1, {'#': col}, x, y)
    t.outline('#ffffff')
    c.paste(t)


def notes(c, x, y, kind, rising):
    """A short trail of music notes floating up from a flower head."""
    col = FLOWERS[kind][5]
    for (dx, dy, shape) in rising:
        note(c, x + dx, y + dy, shape, col)


def build() -> Canvas:
    c = Canvas(240, 135)
    # green sky with dithered bands
    c.vgradient(0, 86, ['#5ac54f', '#99e65f', '#d3fc7e'])
    # sun, upper right
    c.circle(206, 19, 12, '#ffc825')
    c.circle(206, 19, 10, '#ffeb57')
    c.circle(207, 18, 7, '#ffffff')
    for k in range(8):  # short soft rays
        a = k * math.pi / 4 + math.pi / 8
        for d in (15, 16, 17):
            c.set(round(206 + math.cos(a) * d), round(19 + math.sin(a) * d), '#ffeb57' if d < 17 else '#d3fc7e')
    for (x, y, s) in [(14, 20, 0.9), (98, 12, 1.15), (160, 40, 0.62), (58, 44, 0.5), (226, 46, 0.45)]:
        cloud(c, x, y, s)

    # far rolling hills (light), mid hills (darker) with round trees
    far = lambda x: 63 + 5 * math.sin(x / 17.0 + 1.0) + 2.5 * math.sin(x / 7.0)
    c.hills(0, 240, 0, far, '#5ac54f', bottom=90)
    c.vgradient(56, 90, ['#99e65f', '#5ac54f', '#5ac54f', '#33984b'],
                mask=lambda x, y: y >= round(far(x)) + 1)
    for x in range(240):
        c.set(x, round(far(x)), '#99e65f')
    mid = lambda x: 73 + 4 * math.sin(x / 13.0 + 2.0) + 2 * math.sin(x / 5.3)
    for (tx, ty, tw) in [(4, 68, 9), (12, 66, 11), (22, 69, 8), (196, 67, 10), (206, 65, 12), (218, 68, 9), (229, 66, 11)]:
        c.rect(tx + tw // 2, ty + tw - 3, 1, 6, '#1e6f50')
        c.ellipse(tx, ty, tw, tw, '#1e6f50')
        c.ellipse(tx + 2, ty, tw - 3, tw - 3, '#33984b')
        c.set(tx + tw - 3, ty + 2, '#5ac54f')
        c.set(tx + tw - 4, ty + 1, '#5ac54f')
    c.hills(0, 240, 0, mid, '#33984b', bottom=100)
    c.vgradient(66, 100, ['#33984b', '#33984b', '#1e6f50'], mask=lambda x, y: y >= round(mid(x)) + 1 and y < 100)
    for x in range(240):
        c.set(x, round(mid(x)), '#5ac54f')
        if x % 5 == 0:
            c.set(x, round(mid(x)) - 1, '#5ac54f')

    # back stones: beyond the crest, their feet hidden by it
    back = [(80, 86, 11, 15, 1), (105, 83, 10, 14, 2), (133, 83, 10, 14, 3), (158, 86, 11, 15, 4)]
    for (sx, sb, sw, sh, sd) in back:
        stone(c, sx, sb, sw, sh, sd)

    # the hilltop
    c.hills(0, 240, 0, front_top, '#99e65f')
    c.vgradient(78, 135, ['#99e65f', '#99e65f', '#5ac54f', '#5ac54f', '#33984b'],
                mask=lambda x, y: y >= round(front_top(x)))
    for x in range(240):
        y = round(front_top(x))
        c.set(x, y, '#d3fc7e')
        if (x * 7) % 9 == 0:
            c.set(x, y - 1, '#99e65f')
        if (x * 5) % 11 == 0:
            c.set(x, y + 1, '#d3fc7e')
    # grass texture and tufts, denser in front
    r = random.Random(7)
    c.speckle(0, 82, 240, 53, '#5ac54f', 0.05, seed=11, on='#99e65f')
    c.speckle(0, 100, 240, 35, '#33984b', 0.04, seed=12, on='#5ac54f')
    for _ in range(70):  # little grass tufts, bigger in front
        x = r.randrange(240)
        y = r.randrange(96, 135)
        g = c.get(x, y)
        dark = '#5ac54f' if g == '#99e65f' else '#33984b'
        if y > 114:
            c.blit(['...#', '#..#', '.#.#', '.##.'], {'#': dark}, x - 1, y - 3)
        else:
            c.blit(['..#', '#.#', '.#.'], {'#': dark}, x - 1, y - 2)
    # a few small flowers in the grass, fewer in the middle where the dragons stand
    for i, col in enumerate(['#ffeb57', '#f389f5', '#ffffff', '#00cdf9']):
        c.speckle(0, 92, 85, 43, col, 0.006, seed=30 + i)
        c.speckle(155, 92, 85, 43, col, 0.006, seed=40 + i)
        c.speckle(85, 92, 70, 43, col, 0.002, seed=50 + i)

    # mid-back and mid ring stones on the hilltop
    for (sx, sb, sw, sh, sd) in [(55, 91, 14, 20, 5), (183, 91, 14, 20, 6), (32, 104, 18, 28, 7), (208, 104, 18, 28, 8)]:
        stone(c, sx, sb, sw, sh, sd)

    # tiny flowers between the stones
    for (fx, fy, kind) in [(68, 92, 'pink'), (92, 88, 'yellow'), (146, 88, 'blue'), (170, 92, 'pink'),
                           (48, 100, 'blue'), (194, 99, 'yellow'), (118, 86, 'pink'), (82, 97, 'blue'), (160, 97, 'yellow')]:
        petal, dark, light, eye, *_ = FLOWERS[kind]
        c.set(fx, fy + 2, MOSS_D)
        c.set(fx, fy + 3, MOSS_D)
        c.blit(['.p.', 'pep', '.d.'], {'p': petal, 'e': eye, 'd': dark}, fx - 1, fy - 1)

    # big front stones at the sides
    stone(c, 12, 129, 28, 46, 9)
    stone(c, 228, 129, 28, 46, 10)

    # big humming flowers in front, left and right of the middle
    big = [
        (54, 109, 9, 'pink', 135, 21), (35, 122, 6, 'blue', 135, 23), (71, 121, 7, 'yellow', 135, 22),
        (186, 110, 9, 'blue', 135, 25), (205, 122, 6, 'yellow', 135, 27), (169, 121, 7, 'pink', 135, 26),
        (86, 130, 4, 'blue', 135, 24), (153, 130, 4, 'yellow', 135, 28),
    ]
    for (fx, fy, rad, kind, st, sd) in big:
        flower(c, fx, fy, rad, kind, stem_to=st, seed=sd)
    # music notes floating up from the humming flowers
    notes(c, 0, 0, 'pink', [(60, 88, 1), (66, 76, 2), (62, 63, 1)])
    notes(c, 0, 0, 'blue', [(172, 89, 2), (166, 76, 1), (171, 63, 1)])
    notes(c, 0, 0, 'yellow', [(78, 101, 1)])
    notes(c, 0, 0, 'pink', [(156, 101, 1)])
    # tiny hum sparkles around the notes
    for (x, y) in [(58, 84), (76, 74), (70, 61), (164, 87), (180, 72), (162, 62), (88, 99), (152, 98)]:
        c.set(x, y, '#ffffff')
    return c


def check_palette(c):
    bad = [col for col in c.colors() if col not in E64]
    if bad:
        raise SystemExit(f'colours outside Endesga 64: {bad}')


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    c = build()
    check_palette(c)
    name = 'bg_singing_dragons_chorus_day'
    with Studio() as s:
        print(s.image(c, name, OUT / f'{name}.png', 1920, 1080))
