"""bg_bouncing_mud_puddles_afternoon: a meadow of warm brown mud puddles that bounce like trampolines (some domed up
with flying drops, one just landed with ripples), reeds and cattails at the sides, bright dragonflies, a green sky
in soft afternoon light (240x135, Endesga 64)."""
import math
import random

from common import OUT, Canvas, Studio
from bg_singing_dragons_chorus import check_palette

# mud ramp: cool purple-brown in the shadow, warm peach where the light hits
MUD_DD, MUD_D, MUD, MUD_L, MUD_LL, MUD_HI = '#391f21', '#5d2c28', '#8a4836', '#bf6f4a', '#e69c69', '#f6ca9f'
GRASS_L, GRASS, GRASS_D, GRASS_DD = '#99e65f', '#5ac54f', '#33984b', '#1e6f50'
SHINE = '#f9e6cf'


def cloud(c, x, y, s):
    lit, shade = '#ffffff', SHINE
    w = int(38 * s)
    c.ellipse(x, y + int(5 * s), w, int(10 * s), '#c7cfdd')
    c.ellipse(x, y + int(4 * s), w, int(9 * s), shade)
    c.ellipse(x + 1, y + int(2 * s), w - 2, int(9 * s), lit)
    c.ellipse(x + int(4 * s), y - int(3 * s), int(14 * s), int(12 * s), lit)
    c.ellipse(x + int(13 * s), y - int(8 * s), int(15 * s), int(16 * s), lit)
    c.ellipse(x + int(24 * s), y - int(3 * s), int(11 * s), int(10 * s), lit)


def ring(c, cx, cy, rw, rh, col, dash=0, only_on=None):
    """An ellipse outline (rw x rh), optionally dashed, drawn only over the colours in only_on."""
    m = Canvas(c.w, c.h)
    m.ellipse(round(cx - rw / 2), round(cy - rh / 2), round(rw), round(rh), '#000000')
    for yy in range(m.h):
        for xx in range(m.w):
            if m.px[yy][xx] and any(m.get(xx + dx, yy + dy) is None for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]):
                if dash and (xx // dash) % 2:
                    continue
                if only_on is None or c.get(xx, yy) in only_on:
                    c.set(xx, yy, col)


def puddle(c, cx, cy, w, h, ripples=0, dip=False, seed=0):
    """A puddle sunk in the meadow: wet-earth bank, glossy mud, shade under the far bank, light on the near rim,
    a shine on the sun side (left)."""
    r = random.Random(seed)
    x, y = round(cx - w / 2), round(cy - h / 2)
    # wet earth bank around it, lit along the near (lower) edge
    c.ellipse(x - 3, y - 1, w + 6, h + 3, MUD_L)
    c.ellipse(x - 3, y - 2, w + 6, h + 2, MUD)
    # the pool
    c.ellipse(x, y, w, h, MUD)
    # shade under the far bank: a crescent along the top inside
    m = Canvas(c.w, c.h)
    m.ellipse(x, y, w, h, '#000000')
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if m.get(xx, yy) and (m.get(xx, yy - 1) is None or m.get(xx, yy - 2) is None and h >= 8):
                c.set(xx, yy, MUD_D)
            if m.get(xx, yy) and m.get(xx, yy - 1) is None and h >= 6:
                c.set(xx, yy, MUD_DD)
    if dip:  # sinking: a dark hollow in the middle with soft steps
        c.ellipse(round(cx - w * 0.36), round(cy - h * 0.28), round(w * 0.72), round(h * 0.7), MUD_D)
        c.ellipse(round(cx - w * 0.24), round(cy - h * 0.2), round(w * 0.48), round(h * 0.48), MUD_DD)
        ring(c, cx, cy + 1, w * 0.72, h * 0.7, MUD_L, only_on=(MUD,))
    # the near rim inside catches the light
    for xx in range(x + 2, x + w - 2):
        t = (xx + 0.5 - cx) / (w / 2)
        yy = round(cy + (h / 2) * math.sqrt(max(0.0, 1 - t * t))) - 1
        if c.get(xx, yy) == MUD:
            c.set(xx, yy, MUD_L)
    # shine streaks on the sun side
    sx, sy = round(cx - w * 0.3), round(cy - h * 0.05)
    ln = max(2, w // 8)
    for i in range(ln):
        c.set(sx + i, sy, MUD_LL)
    c.set(sx, sy, MUD_HI)
    c.set(sx + ln + 1, sy, MUD_LL)
    if h >= 8:
        for i in range(max(1, ln // 2)):
            c.set(sx + 2 + i, sy + 2, MUD_L)
    # ripples: rings left by a bounce, the outer one dashed
    for k in range(ripples):
        f = 0.42 + 0.26 * k
        ring(c, cx, cy + 0.5, w * f, h * f, MUD_L if k == 0 else MUD_LL, dash=3 if k else 0, only_on=(MUD, MUD_D))
    # tufts on the far bank
    for _ in range(max(2, w // 12)):
        a = r.uniform(math.pi * 1.1, math.pi * 1.9)
        tx, ty = round(cx + math.cos(a) * (w / 2 + 3)), round(cy + math.sin(a) * (h / 2 + 2))
        c.blit(['..#', '#.#', '.#.'], {'#': GRASS_D}, tx - 1, ty - 2)


def dome(c, cx, cy, w_pool, h_pool, H, sigma=0.6, seed=0):
    """A mud puddle bouncing up like a trampoline: the pool's surface bulges into a glossy rounded bubble with a
    stretched skirt at its foot. Cartoon ball shading: shadow on the right, light and a wet shine upper left (sun)."""
    puddle(c, cx, cy, w_pool, h_pool, seed=seed)
    rx = w_pool / 2 * sigma
    ry_low = max(2.0, h_pool / 2 * sigma)
    base = cy

    def bubble(ox, oy, sx, sy):
        """Mask of the bubble shifted by (ox, oy) and scaled by (sx, sy)."""
        m = Canvas(c.w, c.h)
        for yy in range(round(base - H) - 2, round(base + ry_low) + 2):
            for xx in range(round(cx - rx) - 2, round(cx + rx) + 2):
                dx = (xx + 0.5 - cx - ox) / (rx * sx)
                up = yy + 0.5 <= base + oy
                dy = (yy + 0.5 - base - oy) / ((H if up else ry_low) * sy)
                if dx * dx + dy * dy <= 1:
                    m.set(xx, yy, '#000000')
        return m

    shape = bubble(0, 0, 1, 1)
    # the stretched skirt where the bubble pulls up out of the pool
    skirt = Canvas(c.w, c.h)
    skirt.ellipse(round(cx - rx * 1.32), round(base - ry_low * 1.1), round(rx * 2.64), round(ry_low * 2.3), '#000000')
    for yy in range(c.h):
        for xx in range(c.w):
            if skirt.px[yy][xx] and not shape.px[yy][xx]:
                u = (xx - cx) / (rx * 1.32)
                c.set(xx, yy, MUD_L if u < -0.55 else MUD if u < 0.35 else MUD_D)
    c.ellipse(round(cx - rx) - 1, round(base - ry_low * 0.2), round(rx * 2) + 2, round(ry_low * 1.4) + 1, MUD_DD)
    layers = [
        (MUD_D, shape),
        (MUD, bubble(-rx * 0.16, -H * 0.1, 0.9, 0.9)),
        (MUD_L, bubble(-rx * 0.34, -H * 0.3, 0.55, 0.55)),
        (MUD_LL, bubble(-rx * 0.4, -H * 0.42, 0.28, 0.25)),
    ]
    for col, m in layers:
        for yy in range(c.h):
            for xx in range(c.w):
                if m.px[yy][xx] and shape.px[yy][xx]:
                    c.set(xx, yy, col)
    # deepest shade along the lower right rim, with a thin warm reflected light just inside it
    for yy in range(c.h):
        for xx in range(c.w):
            if shape.px[yy][xx] and (shape.get(xx + 1, yy) is None or shape.get(xx + 1, yy + 1) is None):
                if xx > cx:
                    c.set(xx, yy, MUD_DD)
                    if shape.get(xx - 1, yy) and yy > base - H * 0.6 and c.get(xx - 1, yy) == MUD_D:
                        c.set(xx - 1, yy, MUD)
    # wet shine: a curved streak and a glint, upper left
    for i in range(max(3, round(rx * 0.55))):
        a = math.pi * (1.08 + 0.3 * i / max(3, round(rx * 0.55)))
        c.set(round(cx + math.cos(a) * rx * 0.68), round(base + math.sin(a) * H * 0.7), MUD_HI)
    gx, gy = round(cx - rx * 0.12), round(base - H * 0.8)
    c.set(gx, gy, '#ffffff')
    c.set(gx + 1, gy, MUD_HI)

def drop(c, x, y, size, trail=0):
    """A flying mud drop with a shine, and a dotted trail of pale specks under it."""
    if size >= 3:
        c.blit(['.mm.', 'mhmm', 'mmmd', '.dd.'], {'m': MUD, 'd': MUD_D, 'h': MUD_HI}, x, y)
        c.set(x + 2, y, MUD_L)
    elif size == 2:
        c.blit(['hm', 'md'], {'m': MUD, 'd': MUD_D, 'h': MUD_LL}, x, y)
    else:
        c.set(x, y, MUD)
    for k in range(trail):
        c.set(x + size // 2 + (k % 2), y + size + 2 + k * 2, SHINE)


def arcs(c, cx, top, half, n=2):
    """Bounce marks: curved ( ) lines hugging both sides of a dome's top, and a fan of dashes above it."""
    for k in range(n):
        off = half + 3 + k * 3
        hgt = 7 - 2 * k
        for sgn in (-1, 1):
            for i in range(hgt):
                bow = round(1.8 * math.sin(math.pi * (i + 0.5) / hgt))
                c.set(round(cx + sgn * (off + bow)), top + 1 + k + i, '#ffffff' if k == 0 else SHINE)
    for (dx, dy, ex) in [(-7, -2, -1), (0, -5, 0), (7, -2, 1)]:  # fan of dashes above
        for j in range(3):
            c.set(cx + dx + ex * j, top + dy - j, '#ffffff')

def blade(c, bx, by, tx, ty, bend, col, col_l=None, thick=2):
    """A reed leaf from (bx, by) to (tx, ty), bowed sideways by `bend`, thick at the base, pointed at the tip."""
    n = max(4, int(abs(by - ty) * 1.2))
    for i in range(n + 1):
        t = i / n
        x = bx + (tx - bx) * t + bend * math.sin(math.pi * t) * (1 - 0.3 * t)
        y = by + (ty - by) * t
        c.set(round(x), round(y), col)
        if thick >= 2 and t < 0.65:
            c.set(round(x) + 1, round(y), col if col_l is None else col_l)
        if thick >= 3 and t < 0.3:
            c.set(round(x) - 1, round(y), col)


def cattail(c, x, by, top, lean=0):
    """A cattail: a thin stem with a brown velvet head and a spike, lit from the left (the sun)."""
    n = by - top
    for i in range(n + 1):
        t = i / n
        c.set(round(x + lean * t * t), by - i, GRASS_DD if i < n * 0.5 else GRASS_D)
    hx = round(x + lean) - 1
    hy = top + 2
    c.blit(['.LM.', 'LMMD', 'LMMD', 'HMMD', 'LMMD', 'LMMD', 'LMDD', 'LMDD', 'LMDD', '.MD.'],
           {'M': MUD, 'L': MUD_L, 'D': MUD_D, 'H': MUD_LL}, hx, hy)
    c.set(hx + 1, hy - 1, GRASS_D)
    c.set(hx + 1, hy - 2, GRASS_D)
    c.set(hx + 1, hy - 3, GRASS)


DRAGONFLY = [
    '...ww...ww.......',
    '..wWWw.wWWw......',
    '..wWWWwWWWw......',
    'eehTTbBbBbBbBbBbt',
    'eehTTbBbBbBbBbBbt',
    '..wWWWwWWWw......',
    '..wWWw.wWWw......',
    '...ww...ww.......',
]


def dragonfly(c, x, y, body, body_d, flip=False, trail=None):
    """A bright dragonfly seen from above: big round eyes, four see-through wings, a striped tail."""
    rows = [r[::-1] for r in DRAGONFLY] if flip else DRAGONFLY
    if trail:  # a dotted, looping flight path behind it
        for (px, py) in trail:
            c.set(px, py, '#ffffff')
    t = Canvas(c.w, c.h)
    t.blit(rows, {'w': '#ffffff', 'W': '#94fdff', 'e': body_d, 'h': body, 'T': body_d, 'b': body, 'B': body_d,
                  't': body_d}, x, y)
    # thinner tail: the lower body row only runs half way
    for i in range(10, 17):
        xx = x + (16 - i if flip else i)
        t.set(xx, y + 4, None)
    # eye shine
    t.set(x + (15 if flip else 1), y + 3, '#ffffff')
    c.paste(t)


def build() -> Canvas:
    c = Canvas(240, 135)
    # green sky, warming to a soft gold glow near the horizon (afternoon)
    c.vgradient(0, 90, ['#5ac54f', '#99e65f', '#d3fc7e', '#d3fc7e', '#ffeb57'])
    # afternoon sun, lower on the left
    c.circle(40, 36, 16, '#d3fc7e')
    c.circle(40, 36, 13, '#ffc825')
    c.circle(40, 36, 11, '#ffeb57')
    c.circle(39, 35, 8, '#ffffff')
    for (x, y, s) in [(74, 14, 1.15), (150, 22, 0.9), (206, 10, 0.7), (186, 54, 0.45)]:
        cloud(c, x, y, s)

    # far hills, then a soft line of round trees along the horizon
    far = lambda x: 72 + 4 * math.sin(x / 21.0 + 0.5) + 2 * math.sin(x / 8.0)
    c.hills(0, 240, 0, far, '#5ac54f', bottom=92)
    c.vgradient(64, 92, ['#99e65f', '#5ac54f', '#33984b'], mask=lambda x, y: y > round(far(x)))
    for x in range(240):
        c.set(x, round(far(x)), '#99e65f')
    r = random.Random(4)
    x = -4
    while x < 244:
        tw = r.randint(8, 14)
        ty = 79 + r.randint(-3, 2)
        c.ellipse(x, ty, tw, tw, GRASS_DD)
        c.ellipse(x + 1, ty, tw - 3, tw - 3, GRASS_D)
        c.set(x + 2, ty + 2, GRASS)   # sun on the left of each crown
        c.set(x + 3, ty + 1, GRASS)
        c.set(x + 2, ty + 3, GRASS)
        x += tw - r.randint(2, 4)
    c.rect(0, 88, 240, 4, GRASS_DD)

    # the meadow, with warm light on it
    c.vgradient(89, 135, ['#99e65f', '#99e65f', '#5ac54f', '#5ac54f', '#33984b'])
    for x in range(240):
        if (x * 7) % 5 < 3:
            c.set(x, 89, '#d3fc7e')
        if (x * 3) % 7 == 0:
            c.set(x, 88, GRASS_D)
    c.speckle(0, 90, 240, 45, GRASS, 0.05, seed=5, on='#99e65f')
    c.speckle(0, 104, 240, 31, GRASS_D, 0.04, seed=6, on='#5ac54f')
    c.speckle(0, 90, 240, 20, '#d3fc7e', 0.02, seed=7, on='#99e65f')
    for _ in range(60):
        x, y = r.randrange(240), r.randrange(96, 135)
        dark = GRASS if c.get(x, y) == '#99e65f' else GRASS_D
        if y > 115:
            c.blit(['...#', '#..#', '.#.#', '.##.'], {'#': dark}, x - 1, y - 3)
        else:
            c.blit(['..#', '#.#', '.#.'], {'#': dark}, x - 1, y - 2)
    for i, col in enumerate(['#ffeb57', '#ffffff', '#f389f5']):
        c.speckle(0, 94, 240, 41, col, 0.003, seed=60 + i)

    # puddles far away (small, flat), then the bouncing ones nearer: up high, rising, just landed, sinking
    for (px, py, pw, ph, sd) in [(76, 96, 24, 5, 1), (150, 95, 28, 6, 2), (112, 101, 20, 5, 4)]:
        puddle(c, px, py, pw, ph, seed=sd)
    dome(c, 203, 99, 22, 6, 5, sigma=0.7, seed=3)                     # a little one far right, rising
    puddle(c, 120, 116, 48, 14, ripples=2, seed=5)             # just landed: rings
    dome(c, 52, 112, 46, 13, 20, sigma=0.68, seed=7)                   # bouncing up, high
    dome(c, 188, 120, 48, 12, 9, sigma=0.75, seed=8)                  # rising, still low
    puddle(c, 30, 130, 52, 13, dip=True, seed=6)               # sinking down
    puddle(c, 216, 133, 44, 11, ripples=1, seed=9)

    # flying drops and bounce marks
    arcs(c, 52, 88, 12)
    for (dx, dy, s, tr) in [(28, 84, 3, 2), (74, 82, 3, 2), (38, 72, 3, 1), (64, 70, 3, 1), (51, 76, 2, 0), (20, 94, 2, 0), (83, 92, 2, 0)]:
        drop(c, dx, dy, s, tr)
    arcs(c, 188, 110, 11, n=1)
    for (dx, dy, s, tr) in [(172, 100, 2, 1), (202, 98, 3, 1), (186, 93, 2, 0)]:
        drop(c, dx, dy, s, tr)
    for (dx, dy, s, tr) in [(199, 90, 1, 0), (208, 91, 1, 0), (203, 87, 1, 0)]:
        drop(c, dx, dy, s, tr)
    # splash beads around the ring puddle
    for (dx, dy, s) in [(94, 109, 2), (145, 110, 2), (101, 104, 1), (139, 105, 1), (120, 103, 2)]:
        drop(c, dx, dy, s, 0)
    # reeds and cattails at the sides
    for (bx, tx, ty, bend, col) in [(2, -2, 60, -3, GRASS_D), (6, 10, 66, 3, GRASS), (10, 4, 74, -2, GRASS_DD),
                                    (14, 22, 80, 4, GRASS_D), (18, 16, 92, 2, GRASS), (0, 8, 86, 2, GRASS_L),
                                    (22, 30, 100, 3, GRASS_D)]:
        blade(c, bx, 135, tx, ty, bend, col, GRASS_DD if col != GRASS_DD else GRASS_D)
    cattail(c, 8, 135, 56, lean=-2)
    cattail(c, 16, 135, 64, lean=3)
    cattail(c, 3, 135, 72, lean=1)
    for (bx, tx, ty, bend, col) in [(238, 242, 58, 3, GRASS_D), (234, 228, 64, -3, GRASS), (230, 236, 72, 2, GRASS_DD),
                                    (226, 218, 80, -4, GRASS_D), (222, 224, 92, -2, GRASS), (240, 232, 84, -2, GRASS_L),
                                    (218, 210, 100, -3, GRASS_D)]:
        blade(c, bx, 135, tx, ty, bend, col, GRASS_DD if col != GRASS_DD else GRASS_D)
    cattail(c, 232, 135, 54, lean=2)
    cattail(c, 225, 135, 66, lean=-3)
    cattail(c, 238, 135, 70, lean=-1)
    # small reed clumps by the far puddles
    for (bx, by, n) in [(60, 96, 3), (164, 95, 4), (90, 100, 2), (212, 99, 3)]:
        for k in range(n):
            blade(c, bx + k * 2, by, bx + k * 2 + (k - n / 2), by - 5 - (k % 2) * 3, 0.5, GRASS_DD, thick=1)

    # dragonflies: bright, with dotted flight paths
    loop = lambda x0, y0, sx, sy, n: [(round(x0 + sx * i + 3 * math.sin(i / 2.2)), round(y0 + sy * i + 2.5 * math.cos(i / 2.2))) for i in range(0, n, 2)]
    dragonfly(c, 74, 50, '#0cf1ff', '#0069aa', trail=loop(94, 54, 1.6, 0.4, 20))
    dragonfly(c, 150, 62, '#f389f5', '#93388f', flip=True, trail=loop(146, 66, -1.5, 0.3, 16))
    dragonfly(c, 192, 80, '#ffa214', '#c64524', flip=True, trail=loop(188, 84, -1.4, -0.2, 12))
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    c = build()
    check_palette(c)
    name = 'bg_bouncing_mud_puddles_afternoon'
    with Studio() as s:
        print(s.image(c, name, OUT / f'{name}.png', 1920, 1080))
