"""bg_sky_over_dragon_land_afternoon: high up on a dragon's back; clouds and far dragons in the green sky, and far
below the bubble-gum volcano, the custard lake and the Golden Cave (240x135, Endesga 64)."""
import math
import random

from common import Canvas, Studio, OUT
from pxcanvas import BAYER4
from dl_parts import (shade_cone, sky, cloud, cloud_bank, ball, check, PINK, MINT, LEMON, GRAPE, CHERRY, ORANGE, GUM_PINK, GUM_BLUE,
                      GROUND, GROUND_D)

NAME = 'bg_sky_over_dragon_land_afternoon'
HORIZON = 92
HAZE = '#d3fc7e'
FIELDS = ['#99e65f', '#5ac54f', '#33984b', '#99e65f', '#5ac54f', '#d3fc7e', GROUND, '#99e65f', '#33984b', '#5ac54f']
HEDGE = '#1e6f50'
DRAGON = '#1e6f50'
WIND = '#ffffff'


# --- the land below ----------------------------------------------------------------------------
def land(c: Canvas):
    rnd = random.Random(11)
    vx = 124  # vanishing point of the field lines
    rows = []
    d = 1.0
    while True:
        y = HORIZON + (135 - HORIZON) / d
        if y < HORIZON + 1:
            break
        rows.append(y)
        d *= 1.2
    rows = [136.0] + rows
    colors = {}
    for y in range(HORIZON + 1, 135):
        s = (y + 0.5 - HORIZON) / (135 - HORIZON)
        k = next((i for i in range(len(rows) - 1) if rows[i + 1] <= y < rows[i]), len(rows) - 1)
        for x in range(240):
            wx = (x + 0.5 - vx) / max(s, 0.02) + 1000
            off = (0.37 * k) % 1.0
            u = wx / 46 + off
            key = (k, math.floor(u))
            if key not in colors:
                colors[key] = rnd.choice(FIELDS)
            col = colors[key]
            if col == GROUND and s < 0.4:
                col = '#99e65f'
            if (u % 1.0) * 46 * s < 0.8 and s > 0.55:
                col = HEDGE                      # hedges between fields
            if k < len(rows) - 1 and rows[k] - rows[k + 1] > 2.5 and y == math.floor(rows[k + 1]):
                col = HEDGE
            # haze: fields fade into the pale horizon
            haze = max(0.0, 1 - s * 3.2)
            if haze > (BAYER4[y % 4][x % 4] + 0.5) / 16:
                col = HAZE
            c.set(x, y, col)
    for x in range(240):
        c.set(x, HORIZON, HAZE)
    # tiny trees dotted about
    for i in range(70):
        x = rnd.randrange(4, 236)
        y = rnd.randrange(HORIZON + 8, 133)
        s = (y - HORIZON) / (135 - HORIZON)
        ramp = rnd.choice([PINK, MINT, LEMON, GRAPE, CHERRY, ORANGE])
        if s > 0.6:
            c.set(x, y + 1, '#ffffff')
            c.rect(x - 1, y - 1, 3, 2, ramp[1])
            c.set(x - 1, y - 1, ramp[2])
            c.set(x + 1, y, ramp[0])
        else:
            c.set(x, y, ramp[1])
            c.set(x, y + 1, '#1e6f50')


def tiny_road(c: Canvas):
    pts = [(132, 135), (126, 128), (128, 121), (140, 116), (156, 113), (170, 109), (182, 105), (191, 103)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        c.line(x0, y0, x1, y1, '#c7cfdd', t=2 if y0 > 120 else 1)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 > 120:
            c.line(x0 + 1, y0 + 1, x1 + 1, y1 + 1, '#92a1b9')


def tiny_volcano(c: Canvas, cx, top, base):
    rim, foot = 3.5, 19

    def half(y):
        t = max(0.0, (y - top) / (base - top))
        return rim + (foot - rim) * t ** 1.4
    shade_cone(c, cx, top, base, half, ('#bf6f4a', '#e69c69', '#bf6f4a', '#8a4836', '#5d2c28'))
    # gum icing with two drips
    for x in range(cx - 6, cx + 7):
        ramp = GUM_PINK if x < cx else GUM_BLUE
        ln = 3 + {cx - 4: 1, cx - 3: 2, cx - 2: 2, cx - 1: 1, cx + 2: 2, cx + 3: 3, cx + 4: 2}.get(x, 0)
        for y in range(top - 1, top + ln):
            if abs(x + 0.5 - cx) <= half(y) + 0.5:
                last = y == top + ln - 1
                c.set(x, y, ramp[2] if y == top - 1 else ramp[0] if last else ramp[1])
    ball(c, cx - 1, top - 5, 3.6, GUM_PINK)
    ball(c, cx + 4, top - 10, 2.6, GUM_BLUE)
    c.rect(cx - 5, top - 12, 2, 2, GUM_PINK[1])
    c.set(cx + 1, top - 15, GUM_PINK[1])
    # its foot in the squishy pink ground
    for yy in range(base - 1, base + 4):
        for xx in range(cx - foot - 6, cx + foot + 7):
            dx, dy = (xx + 0.5 - cx) / (foot + 6), (yy + 0.5 - base - 0.5) / 3.5
            if dx * dx + dy * dy < 1 and (dx * dx + dy * dy < 0.6 or (xx + yy) % 2 == 0):
                c.set(xx, yy, GROUND)
    c.line(cx - foot + 1, base - 1, cx + foot - 1, base - 1, GROUND_D)


def custard_lake(c: Canvas, x, y, w, h):
    c.ellipse(x - 2, y - 1, w + 4, h + 3, '#f9e6cf')       # a pale sandy shore
    c.ellipse(x, y, w, h, '#edab50')
    c.ellipse(x + 1, y, w - 2, h - 1, '#ffc825')
    c.ellipse(x + 4, y + 1, w - 14, h - 5, '#ffeb57')
    # glints and a caramel swirl
    for (gx, gy, gl) in [(x + 8, y + 3, 5), (x + w - 16, y + h - 4, 4), (x + w // 2, y + 2, 3)]:
        c.line(gx, gy, gx + gl - 1, gy, '#ffffff')
    c.line(x + w // 2 - 6, y + h // 2 + 1, x + w // 2 + 3, y + h // 2 + 1, '#edab50')
    c.set(x + w // 2 + 4, y + h // 2, '#edab50')


def golden_cave(c: Canvas, cx, base):
    # the hill: a round green dome, lit top-left
    w, h = 36, 17
    snap = c.copy()
    c.ellipse(cx - w // 2, base - h, w, 2 * h, '#1e6f50')
    c.ellipse(cx - w // 2, base - h, w - 3, 2 * h - 2, '#33984b')
    c.ellipse(cx - w // 2 + 3, base - h + 1, w // 2, h - 4, '#5ac54f')
    c.ellipse(cx - w // 2 + 6, base - h + 1, w // 4, 3, '#99e65f')
    for y in range(base + 1, c.h):     # cut the dome flat at its foot
        c.px[y] = snap.px[y][:]
    # glow around the mouth
    mx, my = cx + 3, base - 5
    for yy in range(my - 12, base + 1):
        for xx in range(mx - 14, mx + 15):
            d = math.hypot((xx + 0.5 - mx) / 1.25, yy + 0.5 - my)
            thr = (BAYER4[yy % 4][xx % 4] + 0.5) / 16
            if d < 10 and c.get(xx, yy) in ('#1e6f50', '#33984b', '#5ac54f', '#99e65f') and (10 - d) / 5.5 > thr:
                c.set(xx, yy, '#ffeb57' if d < 6.5 else '#d3fc7e')
    # the mouth: a round arch, glowing gold
    c.ellipse(mx - 5, my - 5, 11, 12, '#ffa214')
    c.ellipse(mx - 4, my - 4, 9, 11, '#ffc825')
    c.ellipse(mx - 2, my - 2, 5, 8, '#ffeb57')
    c.rect(mx - 1, my, 3, 5, '#ffffff')
    c.line(mx - 6, base, mx + 6, base, '#ffa214')
    c.line(mx - 8, base + 1, mx + 8, base + 1, '#ffeb57')
    # sparkles
    for (sx, sy) in [(mx - 10, my - 8), (mx + 8, my - 11), (mx + 12, my - 1)]:
        c.set(sx, sy, '#ffffff')
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            c.set(sx + dx, sy + dy, '#ffeb57')


# --- the sky -----------------------------------------------------------------------------------
DRAGON_UP = [
    '.....x..........x........',
    '.....xx........xx..x.....',
    '.....xxx.......xx...x....',
    '.....xxxx.....xxx..xxx...',
    '.x...xxxxx...xxxx.xxxxxx.',
    'xx...x.xxxx..xxx.xxx.....',
    'xx.....xxxxxxxxxxxx......',
    '..x....xxxxxxxxxxx.......',
    '...x..xxxxxxxxxxx........',
    '....xxx..xxxxxxx.........',
    '..........x...x..........',
]
DRAGON_SMALL = [
    '...x....x....',
    '...xx..xx..x.',
    '...xxx.xx.xxx',
    'x...xxxxxxxx.',
    '.xxxxxxxxx...',
    '.....x..x....',
]


def dragon(c: Canvas, x, y, rows, flip=False, col=DRAGON):
    c.blit(rows, {'x': col}, x, y, flip=flip)


def swirl(c: Canvas, x, y, length, r, col=WIND, curl=1, flip=False):
    """A wind line: a gentle wave that rolls up into a round curl at its end (curl=1 up, -1 down)."""
    pts = []
    for i in range(length):
        pts.append((i, 1.0 * math.sin(i / 6.0)))
    ex, ey = pts[-1]
    cyy = ey - curl * r
    n = 40
    for k in range(1, n + 1):
        a = k / n * 1.6 * math.pi
        rr = r * (1 - 0.45 * k / n)
        pts.append((ex + rr * math.sin(a), cyy + curl * rr * math.cos(a)))
    seen = set()
    for (px, py) in pts:
        p = (round(px), round(py))
        if p in seen:
            continue
        seen.add(p)
        c.set(x + (-p[0] if flip else p[0]), y + p[1], col)
    # a shorter companion line under it
    for i in range(length // 3, length - 3):
        c.set(x + (-i if flip else i), y + 3 * curl + round(1.0 * math.sin(i / 6.0)), col)


def build() -> Canvas:
    c = Canvas(240, 135)
    sky(c, HORIZON + 1)
    land(c)
    tiny_road(c)
    tiny_volcano(c, 50, 84, 105)
    custard_lake(c, 92, 107, 46, 12)
    golden_cave(c, 196, 104)
    # clouds below us, over the land at the corners
    cloud_bank(c, [(-2, 124, 10), (14, 118, 9), (30, 124, 9), (46, 130, 8), (8, 132, 10), (60, 134, 6), (-6, 112, 7)])
    cloud_bank(c, [(240, 116, 10), (224, 122, 9), (206, 126, 8), (190, 131, 7), (232, 131, 9), (214, 134, 7)])
    # big clouds around the sides of the sky
    cloud_bank(c, [(-4, 52, 11), (14, 46, 10), (28, 54, 9), (40, 60, 7), (6, 62, 10), (22, 64, 8), (-6, 70, 7)])
    cloud_bank(c, [(244, 22, 10), (226, 18, 11), (208, 26, 9), (196, 34, 7), (230, 32, 9), (212, 38, 7), (244, 40, 7)])
    cloud(c, 82, 6, 0.7)
    cloud(c, 130, 70, 0.5, flip=True)
    # far dragons
    dragon(c, 102, 24, DRAGON_UP)
    dragon(c, 150, 44, DRAGON_SMALL, col='#33984b')
    dragon(c, 58, 36, DRAGON_UP, flip=True, col='#33984b')
    # friendly wind
    swirl(c, 88, 54, 26, 4)
    swirl(c, 176, 78, 20, 3.5, flip=True)
    swirl(c, 40, 22, 22, 4)
    swirl(c, 150, 30, 16, 3)
    check(c)
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    with Studio() as s:
        print(s.image(build(), NAME, OUT / f'{NAME}.png', 1920, 1080))
