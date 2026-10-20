"""bg_golden_cave_afternoon (and the same picture as bg_golden_cave_any): Grumble's Golden Cave (240x135, Endesga 64).

A big warm cave: faceted rock walls with gold veins and sparkles, a great heap of gold coins at the back in the middle
(Grumble's bed; he is a sprite and not drawn here), wobbly towers of coins, buttons and plates at the sides, cups,
crowns, gems and spoons, and a cave mouth onto Dragon Land's green afternoon sky on the right.
"""
import math
import random

from common import Canvas, Studio, OUT
from fx_light import glow, vignette, darken, lighten, sparkle, check, DARKER, LIGHTER

GOLD = ['#ffffff', '#ffeb57', '#ffc825', '#ffa214', '#ed7614', '#c64524']   # light to dark, hue-shifted
BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
RUBY = ('#f5555d', '#ea323c', '#891e2b')
SAPPHIRE = ('#94fdff', '#0cf1ff', '#0069aa')
EMERALD = ('#d3fc7e', '#5ac54f', '#1e6f50')
AMETHYST = ('#fdd2ed', '#db3ffd', '#622461')
SILVER = ('#ffffff', '#c7cfdd', '#657392')
FLOOR_Y = 100


def thr(x, y):
    return (BAYER4[y % 4][x % 4] + 0.5) / 16


def gold_at(level, x, y):
    """Gold ramp colour for a shade level (0 = brightest), dithered between steps."""
    level = max(0.0, min(len(GOLD) - 1.001, level))
    i = int(level)
    f = min(1.0, max(0.0, (level - i - 0.3) / 0.4))
    return GOLD[i + 1] if f > thr(x, y) else GOLD[i]


# ----------------------------------------------------------------------------------------------- the cave shell
ROCK = ['#3b1443', '#391f21', '#5d2c28', '#8a4836', '#bf6f4a', '#e69c69', '#edab50', '#ffc825']


def rock_wall(c: Canvas, light=(120, 70)):
    """Faceted rock: flat Voronoi facets, brighter near the gold, each with a lit upper-left edge, a shaded
    lower-right edge and dark seams; some seams are veins of gold."""
    r = random.Random(7)
    seeds = []
    for _ in range(105):
        sx, sy = r.uniform(-10, 250), r.uniform(-8, FLOOR_Y + 4)
        d = math.hypot((sx - light[0]) / 130, (sy - light[1]) / 85)
        lvl = int(round(6.9 - 6.2 * d + r.uniform(-0.8, 0.8)))
        seeds.append((sx, sy, max(0, min(len(ROCK) - 1, lvl))))
    for y in range(FLOOR_Y):
        for x in range(240):
            ds = sorted(((x - sx) ** 2 + ((y - sy) * 1.5) ** 2, i) for i, (sx, sy, _) in enumerate(seeds))
            (d1, a), (d2, b) = ds[0], ds[1]
            e = math.sqrt(d2) - math.sqrt(d1)
            ax, ay, lvl = seeds[a]
            bx, by, lvl_b = seeds[b]
            if e < 1.2:
                if (min(a, b) * 7 + max(a, b) * 3) % 3 == 0 and 2 <= min(lvl, lvl_b) and max(lvl, lvl_b) <= 6:
                    col = '#ffc825' if (x + y) % 3 else '#ffeb57'
                    c.set(x, y, col)
                    c.set(x, y + 1, '#edab50')
                    continue
                col = ROCK[max(0, min(lvl, lvl_b) - 2)]
            elif e < 3.0:
                shadow = (bx - ax) + (by - ay) * 1.2 > 0
                col = ROCK[max(0, lvl - 1)] if shadow else ROCK[min(len(ROCK) - 1, lvl + 1)]
            else:
                col = ROCK[lvl]
            if c.get(x, y) not in ('#ffc825', '#ffeb57', '#edab50'):
                c.set(x, y, col)


def gold_veins(c: Canvas):
    # little gold nuggets set in the rock
    r = random.Random(13)
    for _ in range(48):
        x, y = r.randint(4, 234), r.randint(6, FLOOR_Y - 6)
        if c.get(x, y) not in ('#5d2c28', '#8a4836', '#bf6f4a', '#e69c69'):
            continue
        c.blit(['.lm', 'lmd', 'md.'] if r.random() < 0.5 else ['lm', 'md'],
               {'l': '#ffeb57', 'm': '#ffc825', 'd': '#edab50'}, x, y)
    # gold flecks embedded in the rock
    c.speckle(0, 0, 240, FLOOR_Y - 2, '#ffc825', 0.008, seed=5, on='#8a4836')
    c.speckle(0, 0, 240, FLOOR_Y - 2, '#ffeb57', 0.010, seed=6, on='#bf6f4a')
    c.speckle(0, 0, 240, FLOOR_Y - 2, '#edab50', 0.010, seed=8, on='#5d2c28')


def cave_mouth(c: Canvas):
    """An opening in the upper right onto the green sky. Returns a test for 'inside the opening'."""
    pts = [(197, 34), (199, 24), (205, 20), (207, 14), (214, 13), (219, 9), (226, 12), (231, 11), (234, 18),
           (238, 24), (237, 36), (239, 46), (236, 56), (237, 64), (231, 70), (224, 74), (216, 72), (208, 75),
           (201, 70), (198, 62), (194, 54), (196, 44)]
    mouth = Canvas(240, 135)
    mouth.polygon(pts, '#000000')
    inside = lambda x, y: mouth.get(x, y) is not None
    # rim: lit rock around the hole
    rim = Canvas(240, 135)
    rim.polygon([(x + (x - 216) * 0.12, y + (y - 43) * 0.12) for (x, y) in pts], '#000000')
    for y in range(135):
        for x in range(240):
            if rim.get(x, y) and not inside(x, y):
                c.set(x, y, '#e69c69' if x < 216 else '#bf6f4a')
    c.vgradient(10, 76, ['#5ac54f', '#99e65f', '#d3fc7e'], mask=inside)
    # cloud, far hills, a gum-drop tree
    for (cx, cy, w, h, col) in [(205, 25, 18, 6, '#ffffff'), (210, 21, 9, 7, '#ffffff'), (204, 29, 20, 3, '#c7cfdd')]:
        for y in range(cy, cy + h):
            for x in range(cx, cx + w):
                if inside(x, y) and ((x + 0.5 - cx - w / 2) / (w / 2)) ** 2 + ((y + 0.5 - cy - h / 2) / (h / 2)) ** 2 <= 1:
                    c.set(x, y, col)
    for x in range(190, 240):
        h1 = 56 + 4 * math.sin(x / 6.0)
        h2 = 63 + 3 * math.sin(x / 4.0 + 2)
        for y in range(round(h1), 80):
            if inside(x, y):
                c.set(x, y, '#33984b' if y < h2 else '#1e6f50')
        if inside(x, round(h1)):
            c.set(x, round(h1), '#5ac54f')
    for (tx, ty, col) in [(222, 50, '#f68187'), (206, 54, '#ffeb57')]:
        for y in range(ty, ty + 8):
            if inside(tx, y):
                c.set(tx, y, '#8a4836')
        for (dx, dy, rr) in [(0, 0, 3.5)]:
            for y in range(ty - 4, ty + 4):
                for x in range(tx - 4, tx + 5):
                    if inside(x, y) and (x - tx) ** 2 + (y - ty) ** 2 <= rr * rr:
                        c.set(x, y, col)
        if inside(tx - 1, ty - 2):
            c.set(tx - 1, ty - 2, '#ffffff')
    return inside


def frame_rocks(c: Canvas):
    """Dark foreground rock around the edges and a lumpy ceiling with a few round stalactites."""
    DK, MD, RIM = '#1c121c', '#3b1443', '#622461'
    left = lambda y: 10 + 6 * math.sin(y / 9.0) + 4 * math.sin(y / 3.7 + 1) + (14 if y < 20 else 0) * (1 - y / 20)
    right = lambda y: 232 - 4 * math.sin(y / 8.0 + 2) - 3 * math.sin(y / 3.1)
    top = lambda x: 6 + 3 * math.sin(x / 7.0) + 2 * math.sin(x / 2.9 + 1)
    for y in range(135):
        lx = round(left(y)) if y < 100 else round(left(100) - (y - 100) * 0.9)
        for x in range(0, max(0, lx)):
            c.set(x, y, MD if x > lx - 3 else DK)
        if lx >= 0:
            c.set(lx, y, RIM)
        rx = round(right(y))
        if y > 80:
            for x in range(rx, 240):
                c.set(x, y, MD if x < rx + 3 else DK)
            c.set(rx - 1, y, RIM)
    for x in range(240):
        t = round(top(x))
        for y in range(0, t):
            c.set(x, y, DK if y < t - 2 else MD)
        c.set(x, t, RIM)
    # stalactites: round-tipped, rim-lit on the left
    for (sx, length, w) in [(34, 14, 7), (62, 9, 5), (92, 16, 8), (150, 12, 6), (176, 18, 8), (188, 8, 5)]:
        y0 = round(top(sx))
        c.polygon([(sx - w / 2, y0 - 1), (sx + w / 2, y0 - 1), (sx + 1, y0 + length), (sx - 1, y0 + length)], MD)
        c.line(sx - round(w / 2) + 1, y0, sx - 1, y0 + length - 1, RIM)
        c.set(sx, y0 + length, MD)
        c.set(sx, y0 + length + 2, '#ffc825')  # a gold drip
    # a couple of rocks bulging into the floor at the sides


FLOOR = ['#f6ca9f', '#e69c69', '#bf6f4a', '#8a4836', '#5d2c28', '#391f21']


def floor(c: Canvas):
    """Warm cave floor: brightest just in front of the heap, darker towards the front and the sides."""
    for y in range(FLOOR_Y - 2, 135):
        for x in range(240):
            t = (y - FLOOR_Y + 2) / (135 - FLOOR_Y + 2)
            level = 1.0 + 2.3 * t + 1.6 * (abs(x - 120) / 120) ** 1.5 + 0.25 * math.sin(x / 9.0 + y / 4.0)
            level = max(0.0, min(len(FLOOR) - 1.001, level))
            i = int(level)
            f = min(1.0, max(0.0, (level - i - 0.3) / 0.4))
            c.set(x, y, FLOOR[i + 1] if f > thr(x, y) else FLOOR[i])
    r = random.Random(3)
    for _ in range(30):
        x, y = r.randint(0, 236), r.randint(FLOOR_Y + 6, 132)
        w = r.randint(4, 8)
        base = c.get(x, y) or '#8a4836'
        c.ellipse(x, y, w, 3, DARKER.get(base, base))
        c.rect(x + 1, y, w - 2, 1, LIGHTER.get(base, base))
    # the floor's back edge catches the light
    c.rect(0, FLOOR_Y - 2, 240, 1, '#e69c69')


# ----------------------------------------------------------------------------------------------- treasure
def heap(c: Canvas, cx=120, half=72, peak=50, base=104, seed=1, lumps=True):
    """A great heap of gold coins, lit from the upper left, with coins drawn into it and gems on top."""
    r = random.Random(seed)
    top = {}
    for x in range(cx - half, cx + half + 1):
        u = (x - cx) / half
        if abs(u) > 1:
            continue
        h = (base - peak) * (1 - u * u) ** 0.9
        if lumps:
            h += 2.0 * math.sin(x / 4.3 + seed) + 1.5 * math.sin(x / 2.1 + seed * 2) * (1 - abs(u))
        top[x] = round(base - max(0.0, h))
    for x, t in top.items():
        for y in range(t, base + 1):
            u = (x - cx) / half
            depth = (y - t) / max(1, base - t)
            level = 1.1 + 1.3 * max(0.0, u + 0.25) + 1.2 * depth ** 1.5 - 0.6 * max(0.0, -u - 0.2)
            c.set(x, y, gold_at(level, x, y))
    # coins: little 3x2 discs, light on top, dark edge below
    for _ in range(int(half * (base - peak) * 0.05)):
        x = r.randint(cx - half + 3, cx + half - 4)
        if x not in top:
            continue
        y = r.randint(top[x] + 1, base - 1)
        under = c.get(x, y)
        if under is None or under not in GOLD:
            continue
        i = GOLD.index(under)
        face, edge = GOLD[max(1, i - 1)], GOLD[min(len(GOLD) - 1, i + 1)]
        c.rect(x, y, 3, 1, face)
        c.set(x - 1, y + 1, edge)
        c.rect(x, y + 1, 3, 1, under)
        c.set(x + 3, y + 1, edge)
    # the bumpy silhouette gets a bright rim on top
    for x, t in top.items():
        c.set(x, t, '#ffeb57' if x < cx + half * 0.4 else '#ffc825')
    return top


def gem(c: Canvas, x, y, ramp, size=3):
    l, m, d = ramp
    if size <= 2:
        c.rect(x, y, 2, 2, m)
        c.set(x, y, l)
        c.set(x + 1, y + 1, d)
        return
    c.blit(['.lm.', 'lmmd', 'mmdd', '.dd.'] if size == 3 else ['..l..', '.lmm.', 'lmmmd', '.mdd.', '..d..'],
           {'l': l, 'm': m, 'd': d}, x, y)
    c.set(x + 1, y + 1, '#ffffff')


def coin_tower(c: Canvas, x, bottom, n, w=8, phase=0.0, ramp=None):
    """A wobbly stack of n coins (each 2 px tall) standing at x..x+w on `bottom`; returns (top_x, top_y)."""
    off = 0.0
    xs = []
    for i in range(n):
        off = 1.6 * math.sin(i * 0.33 + phase) + 0.6 * math.sin(i * 0.9 + phase * 2)
        xi = x + round(off)
        y = bottom - 2 * i - 1
        xs.append((xi, y))
    lit, mid, shade, dark = ramp or ('#ffeb57', '#ffc825', '#ffa214', '#ed7614')
    for (xi, y) in xs:
        c.rect(xi, y - 1, w, 1, mid)
        c.set(xi, y - 1, lit)
        c.set(xi + 1, y - 1, lit)
        c.set(xi + w - 1, y - 1, shade)
        c.rect(xi, y, w, 1, shade)
        c.set(xi + w - 1, y, dark)
        c.set(xi, y, mid)
    tx, ty = xs[-1]
    c.rect(tx, ty - 2, w, 1, lit)                      # the top face of the last coin
    c.set(tx + 2, ty - 2, '#ffffff')
    return tx, ty - 2


def button_tower(c: Canvas, x, bottom, colours, w=9, phase=0.0):
    """A wobbly stack of big buttons (3 px each) in many colours."""
    y = bottom
    xi = x
    for i, ramp in enumerate(colours):
        xi = x + round(1.5 * math.sin(i * 0.8 + phase))
        l, m, d = ramp
        c.rect(xi, y - 2, w, 1, l)
        c.rect(xi, y - 1, w, 1, m)
        c.rect(xi, y, w, 1, d)
        c.set(xi + w // 2 - 1, y - 2, d)
        c.set(xi + w // 2 + 1, y - 2, d)
        y -= 3
    return xi, y + 1


def goblet(c: Canvas, x, bottom, ramp=None, gem_ramp=RUBY):
    l, m, d = ramp or ('#ffeb57', '#ffc825', '#ed7614')
    rows = ["lmmmmmd", "lmmmmmd", ".lmmmd.", ".lmgmd.", "..lmd..", "...m...", "...d...", "..lmd..", ".lmmmdd"]
    c.blit(rows, {'l': l, 'm': m, 'd': d, 'g': gem_ramp[1]}, x, bottom - len(rows) + 1)
    c.set(x + 1, bottom - len(rows) + 2, '#ffffff')


def crown(c: Canvas, x, bottom):
    rows = ["l...l...l", "ll.lml.ld", "lmmmmmmmd", "lrmmbmmgd", "lmmmmmmmd", "ddddddddd"]
    c.blit(rows, {'l': '#ffeb57', 'm': '#ffc825', 'd': '#ed7614', 'r': '#ea323c', 'b': '#0cf1ff', 'g': '#5ac54f'},
           x, bottom - len(rows) + 1)
    c.set(x, bottom - 6, '#ffffff')


def spoon(c: Canvas, x, y, flip=False):
    rows = [".ll.......", "lwmm......", "lmmdmmmmmd", ".dd......."]
    c.blit([r[::-1] for r in rows] if flip else rows, {'l': '#ffffff', 'w': '#ffffff', 'm': '#c7cfdd', 'd': '#657392'},
           x, y)


def plates(c: Canvas, x, bottom, n, w=11, phase=1.0):
    """A wobbly stack of silver plates."""
    y = bottom
    for i in range(n):
        xi = x + round(1.2 * math.sin(i * 0.7 + phase))
        c.rect(xi, y - 1, w, 1, '#ffffff' if i % 2 else '#c7cfdd')
        c.rect(xi + 1, y, w - 2, 1, '#92a1b9')
        c.set(xi + w - 1, y - 1, '#92a1b9')
        y -= 2
    return xi, y


def chest(c: Canvas, x, bottom):
    """A small open chest spilling gems."""
    W = 18
    c.rect(x, bottom - 8, W, 9, '#8a4836')
    c.rect(x, bottom - 8, W, 1, '#bf6f4a')
    c.rect(x, bottom, W, 1, '#5d2c28')
    for bx in (x + 2, x + W - 4):
        c.rect(bx, bottom - 8, 2, 9, '#ffc825')
        c.line(bx + 1, bottom - 8, bx + 1, bottom, '#ed7614')
    c.rect(x + W // 2 - 1, bottom - 6, 2, 3, '#ffeb57')
    c.set(x + W // 2 - 1, bottom - 4, '#391f21')
    # lid tilted back
    c.polygon([(x, bottom - 9), (x + W, bottom - 9), (x + W - 2, bottom - 16), (x + 2, bottom - 16)], '#5d2c28')
    c.polygon([(x + 1, bottom - 10), (x + W - 1, bottom - 10), (x + W - 3, bottom - 15), (x + 3, bottom - 15)], '#8a4836')
    c.line(x + 3, bottom - 15, x + W - 4, bottom - 15, '#bf6f4a')
    # gold and gems inside
    for i in range(W - 2):
        c.set(x + 1 + i, bottom - 9, '#ffc825' if i % 3 else '#ffeb57')
    gem(c, x + 3, bottom - 12, RUBY)
    gem(c, x + 9, bottom - 11, SAPPHIRE, size=2)
    gem(c, x + 12, bottom - 13, EMERALD)
    c.set(x + 7, bottom - 10, '#ffffff')


def build() -> Canvas:
    c = Canvas(240, 135)
    rock_wall(c)
    gold_veins(c)
    floor(c)
    inside = cave_mouth(c)
    frame_rocks(c)

    not_sky = lambda x, y, col: not inside(x, y)
    # wall sparkles
    r = random.Random(21)
    for _ in range(46):
        x, y = r.randint(14, 226), r.randint(10, 92)
        if inside(x, y):
            continue
        sparkle(c, x, y, size=r.choice([0, 1, 1, 2]))

    # --- the great heap at the back (Grumble's bed) -----------------------------------------------------------
    top = heap(c, cx=120, half=68, peak=52, base=104, seed=2)
    for (gx, gy, ramp, size) in [(96, 72, RUBY, 3), (131, 61, SAPPHIRE, 3), (148, 80, EMERALD, 3), (82, 88, AMETHYST, 3),
                                 (112, 58, EMERALD, 2), (160, 92, RUBY, 2), (70, 96, SAPPHIRE, 2), (124, 84, AMETHYST, 2),
                                 (104, 92, RUBY, 2), (172, 98, EMERALD, 2)]:
        gem(c, gx, gy, ramp, size)
    goblet(c, 140, top[143] + 3, gem_ramp=SAPPHIRE)
    crown(c, 98, top[102] + 3)
    for (sx, sy) in [(110, 52), (87, 66), (152, 70), (128, 76), (66, 90), (176, 90)]:
        sparkle(c, sx, sy, 2)

    # --- wobbly towers on the left --------------------------------------------------------------------------
    small_heap = lambda cx, half, peak, base, seed: heap(c, cx, half, peak, base, seed)
    tx, ty = coin_tower(c, 20, 108, 26, w=9, phase=0.3)
    crown(c, tx, ty)
    tx, ty = button_tower(c, 33, 110, [RUBY, SAPPHIRE, EMERALD, AMETHYST, ('#ffeb57', '#ffc825', '#ed7614'),
                                       RUBY, ('#f9e6cf', '#f6ca9f', '#bf6f4a'), SAPPHIRE, EMERALD], w=10, phase=1.0)
    tx, ty = coin_tower(c, 46, 112, 13, w=8, phase=2.0)
    gem(c, tx + 2, ty - 4, AMETHYST)
    small_heap(30, 26, 100, 120, 5)
    chest(c, 18, 121)
    goblet(c, 42, 117, gem_ramp=EMERALD)
    spoon(c, 50, 117)

    # --- wobbly towers on the right (against the sky in the mouth) --------------------------------------------
    tx, ty = plates(c, 186, 110, 14, w=11)
    tx, ty = coin_tower(c, 200, 108, 30, w=9, phase=1.7)
    goblet(c, tx + 1, ty, gem_ramp=RUBY)
    tx, ty = coin_tower(c, 214, 112, 19, w=8, phase=0.8)
    gem(c, tx + 2, ty - 4, SAPPHIRE)
    small_heap(212, 30, 102, 121, 9)
    crown(c, 222, 116)
    goblet(c, 196, 119, gem_ramp=AMETHYST)
    spoon(c, 204, 120, flip=True)
    gem(c, 188, 118, EMERALD)
    for (sx, sy) in [(24, 64), (49, 88), (205, 52), (218, 70), (190, 82), (30, 104), (214, 108)]:
        sparkle(c, sx, sy, 2)

    # --- a few spilled coins and gems on the floor (the middle stays clear for the sprites) --------------------
    r = random.Random(4)
    for _ in range(26):
        x = r.choice([r.randint(56, 84), r.randint(156, 184), r.randint(60, 180)])
        y = r.randint(106, 132)
        if 92 < x < 148 and y > 108:
            continue
        c.rect(x, y, 2, 1, '#ffeb57')
        c.rect(x, y + 1, 2, 1, '#ffa214')
    gem(c, 70, 124, RUBY, 2)
    gem(c, 168, 128, SAPPHIRE, 2)
    darken(c, 52, 104, 140, 2, 0.6, mask=lambda x, y, col: col in ('#bf6f4a', '#e69c69', '#f6ca9f', '#8a4836'))

    vignette(c, 1.0, inner=0.7, cy=62, mask=lambda x, y, col: y >= FLOOR_Y + 8)
    check(c)
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    c = build()
    with Studio() as s:
        with s.lock():
            s.push(c, 'bg_golden_cave_afternoon')
            print(s.export(str(OUT / 'bg_golden_cave_afternoon.png'), 1920, 1080))
            print(s.export(str(OUT / 'bg_golden_cave_any.png'), 1920, 1080))
