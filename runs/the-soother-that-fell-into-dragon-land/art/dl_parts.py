"""Shared parts for the Dragon Land backgrounds: green sky, clouds, gum trees, bubbles, squishy ground, palette check."""
import math

from common import Canvas
from pxcanvas import BAYER4

E64 = {
    '#ff0040', '#131313', '#1b1b1b', '#272727', '#3d3d3d', '#5d5d5d', '#858585', '#b4b4b4', '#ffffff', '#c7cfdd',
    '#92a1b9', '#657392', '#424c6e', '#2a2f4e', '#1a1932', '#0e071b', '#1c121c', '#391f21', '#5d2c28', '#8a4836',
    '#bf6f4a', '#e69c69', '#f6ca9f', '#f9e6cf', '#edab50', '#e07438', '#c64524', '#8e251d', '#ff5000', '#ed7614',
    '#ffa214', '#ffc825', '#ffeb57', '#d3fc7e', '#99e65f', '#5ac54f', '#33984b', '#1e6f50', '#134c4c', '#0c2e44',
    '#00396d', '#0069aa', '#0098dc', '#00cdf9', '#0cf1ff', '#94fdff', '#fdd2ed', '#f389f5', '#db3ffd', '#7a09fa',
    '#3003d9', '#0c0293', '#03193f', '#3b1443', '#622461', '#93388f', '#ca52c9', '#c85086', '#f68187', '#f5555d',
    '#ea323c', '#c42430', '#891e2b', '#571c27',
}

SKY = ['#5ac54f', '#99e65f', '#d3fc7e']
CLOUD, CLOUD_S = '#ffffff', '#c7cfdd'

# candy ramps: dark, base, light, shine
PINK = ('#c85086', '#f68187', '#fdd2ed', '#ffffff')
MINT = ('#00cdf9', '#94fdff', '#ffffff', '#ffffff')
LEMON = ('#ed7614', '#ffc825', '#ffeb57', '#ffffff')
ORANGE = ('#c64524', '#ed7614', '#ffa214', '#ffeb57')
GRAPE = ('#93388f', '#ca52c9', '#f389f5', '#fdd2ed')
CHERRY = ('#891e2b', '#ea323c', '#f5555d', '#fdd2ed')
GUM_PINK = ('#ca52c9', '#f389f5', '#fdd2ed', '#ffffff')
DEEP = {PINK: '#93388f', MINT: '#0098dc', LEMON: '#c64524', ORANGE: '#8e251d', GRAPE: '#622461', CHERRY: '#571c27'}
GUM_BLUE = ('#0069aa', '#00cdf9', '#94fdff', '#ffffff')

# the squishy marshmallow ground
GROUND_L, GROUND, GROUND_D, GROUND_DD = '#fdd2ed', '#f68187', '#c85086', '#93388f'
MOSS_L, MOSS, MOSS_D = '#d3fc7e', '#99e65f', '#5ac54f'


def check(c: Canvas):
    bad = [x for x in c.colors() if x not in E64]
    if bad:
        raise ValueError(f'colours outside Endesga 64: {bad}')


def sky(c: Canvas, y1: int):
    c.vgradient(0, y1, SKY)


def cloud(c: Canvas, x: int, y: int, s: float = 1.0, flip: bool = False, lit=CLOUD, shade=CLOUD_S):
    """A fluffy cloud about 36*s wide with (x, y) near its top-left; flat shaded belly."""
    puffs = [(0, 5, 36, 10), (4, 0, 14, 12), (13, -5, 15, 15), (24, -1, 12, 11), (29, 3, 9, 8)]
    if flip:
        puffs = [(36 - dx - w, dy, w, h) for (dx, dy, w, h) in puffs]
    S = lambda v: int(round(v * s))
    for (dx, dy, w, h) in puffs:
        c.ellipse(x + S(dx), y + S(dy) + 2, S(w), S(h), shade)
    for (dx, dy, w, h) in puffs:
        c.ellipse(x + S(dx), y + S(dy), S(w), max(2, S(h) - 1), lit)
    # belly: the shade shows under the bottom puff
    c.ellipse(x + S(2), y + S(8) + 1, S(32), S(7), shade)
    c.ellipse(x + S(3), y + S(6), S(30), S(6), lit)


def cloud_bank(c: Canvas, puffs, lit=CLOUD, shade=CLOUD_S, deep='#92a1b9'):
    """A big fluffy cloud from circles [(cx, cy, r)]: one merged shape, white on top, a grey belly, and soft grey
    creases where a lower puff sits in front of a higher one."""
    for (cx, cy, r) in puffs:
        c.circle(cx + 0.6, cy + 2.6, r, deep)
    for (cx, cy, r) in puffs:
        c.circle(cx + 0.3, cy + 1.4, r, shade)
    for (cx, cy, r) in puffs:
        c.circle(cx, cy, r - 0.4, lit)
    # creases: the top-left rim of puffs that sit low and in front
    order = sorted(puffs, key=lambda p: p[1])
    for i, (cx, cy, r) in enumerate(order):
        if i < len(order) // 2:
            continue
        for k in range(18):
            a = math.pi * (1.05 + 0.5 * k / 17)       # from left round to the top
            px, py = round(cx + (r - 0.6) * math.cos(a)), round(cy + (r - 0.6) * math.sin(a))
            # only where the rim crosses another puff's white (a crease inside the cloud)
            if any(math.hypot(px + 0.5 - ox, py + 0.5 - oy) < orr - 1.5 for (ox, oy, orr) in puffs if (ox, oy, orr) != (cx, cy, r)):
                if c.get(px, py) == lit:
                    c.set(px, py, shade)


def blob(c: Canvas, circles, ramp, shine=True):
    """A shaded cluster of circles [(cx, cy, r)]: dark rim bottom-right, base, light top-left, a shine pixel."""
    dark, base, light, hi = ramp
    for (cx, cy, r) in circles:
        c.circle(cx, cy, r, dark)
    for (cx, cy, r) in circles:
        c.circle(cx - 0.8, cy - 1.0, r - 1.2, base)
    for (cx, cy, r) in circles:
        if r >= 3:
            c.circle(cx - r * 0.35, cy - r * 0.42, r * 0.42, light)
    if shine:
        cx, cy, r = min(circles, key=lambda t: t[1] - t[2])
        if r >= 3:
            c.set(round(cx - r * 0.45), round(cy - r * 0.55), hi)
            if r >= 6:
                c.set(round(cx - r * 0.45) + 1, round(cy - r * 0.55), hi)
                c.set(round(cx - r * 0.45), round(cy - r * 0.55) + 1, hi)


def ball(c: Canvas, cx, cy, r, ramp):
    blob(c, [(cx, cy, r)], ramp)


BUBBLE_ROWS = {
    2: ['.rr.', 'rw.r', 'r..r', '.rr.'],
    3: ['.rrr.', 'rw..r', 'r...r', 'r...r', '.rrr.'],
    4: ['..rrr..', '.r...r.', 'rw....r', 'r.....r', 'r.....r', '.r...r.', '..rrr..'],
    5: ['...rrr...', '.rr...rr.', '.rw.....r', 'r w.....r', 'r.......r', 'r.......r', '.r.....r.', '.rr...rr.', '...rrr...'],
}


def ring_bubble(c: Canvas, cx, cy, size, ring, shine='#ffffff'):
    """A see-through bubble (size 2-5): a coloured ring with a white glint top-left."""
    rows = BUBBLE_ROWS[size]
    rows = [r.replace(' ', '.') for r in rows]
    c.blit(rows, {'r': ring, 'w': shine}, round(cx - len(rows[0]) / 2), round(cy - len(rows) / 2))


def candy_trunk(c: Canvas, x, top, bottom, w=4, stripe='#ea323c', stripe_d='#c42430'):
    """A lollipop-stick trunk with diagonal candy stripes; light on the left, shade on the right."""
    for yy in range(top, bottom):
        for i in range(w):
            xx = x - w // 2 + i
            if (yy + i) % 6 < 2:
                col = stripe_d if i == w - 1 else stripe
            elif i == 0:
                col = '#ffffff'
            elif i == w - 1:
                col = '#c7cfdd'
            else:
                col = '#f9e6cf'
            c.set(xx, yy, col)


def crown_shape(x, top, r):
    """Lumps of a round crown, back ones first."""
    k = r * 0.6
    return [(x - r * 0.3, top - r * 0.72, r * 0.6), (x + r * 0.4, top - r * 0.62, r * 0.58),
            (x - k, top + r * 0.12, r * 0.66), (x + k, top + r * 0.18, r * 0.64),
            (x, top - r * 0.12, r * 0.78), (x - r * 0.28, top + r * 0.42, r * 0.56), (x + r * 0.36, top + r * 0.46, r * 0.52)]


def lump(c: Canvas, cx, cy, r, ramp, deep):
    """One round lump of a crown: deep rim bottom-right, base body, a light crescent and a shine top-left."""
    dark, base, light, hi = ramp
    c.circle(cx, cy, r, deep)
    c.circle(cx - 0.6, cy - 0.7, r - 0.9, dark)
    c.circle(cx - 1.0, cy - 1.2, r - 1.6, base)
    if r >= 3.5:
        # light crescent: the light disc minus a base disc nudged down-right
        lr = r * 0.62
        lx, ly = cx - r * 0.3, cy - r * 0.36
        for yy in range(int(ly - lr) - 1, int(ly + lr) + 2):
            for xx in range(int(lx - lr) - 1, int(lx + lr) + 2):
                px, py = xx + 0.5, yy + 0.5
                if math.hypot(px - lx, py - ly) <= lr and math.hypot(px - lx - r * 0.3, py - ly - r * 0.3) > lr * 0.95                         and math.hypot(px - cx + 1.0, py - cy + 1.2) <= r - 1.6:
                    c.set(xx, yy, light)
        sx, sy = round(cx - r * 0.5), round(cy - r * 0.55)
        if c.get(sx, sy) in (light, base):
            c.set(sx, sy, hi)


def leaf_crown(c: Canvas, circles, ramp, deep=None):
    dark = ramp[0]
    deep = deep or DEEP.get(ramp, dark)
    for (cx, cy, r) in circles:
        lump(c, cx, cy, r, ramp, deep)


def gum_tree(c: Canvas, x, ground, h, r, ramp, deep=None, stripe=('#ea323c', '#c42430'), shadow=None):
    """A gum tree: a candy-stick trunk and a round crown of candy leaves, with a soft shadow on the ground."""
    top = ground - h
    if shadow:
        c.ellipse(x - r, ground - 2, 2 * r, 5, shadow)
    tw = max(3, r // 3)
    candy_trunk(c, x, top, ground, tw, *stripe)
    circles = crown_shape(x, top, r)
    leaf_crown(c, circles, ramp, deep)
    return circles


def gumdrop(c: Canvas, x, y, w, ramp):
    """A little gumdrop dome sitting on y (its bottom row)."""
    dark, base, light, hi = ramp
    h = max(2, w * 2 // 3)
    c.ellipse(x, y - h, w, 2 * h, dark)
    c.ellipse(x, y - h, w - 1, 2 * h - 1, base)
    c.set(x + 1, y - h + 1, light)
    if w >= 4:
        c.set(x + 2, y - h + 1, hi)


def tuft(c: Canvas, x, y, col=MOSS, dark=MOSS_D, size=3):
    """A small grass tuft whose roots sit on row y."""
    if size >= 3:
        c.set(x, y - 2, col)
        c.set(x + 2, y - 3, col)
        c.set(x + 4, y - 2, col)
        c.line(x + 1, y - 1, x + 3, y - 1, col)
        c.line(x, y, x + 4, y, dark)
        c.set(x + 2, y - 2, col)
    else:
        c.set(x, y - 1, col)
        c.set(x + 2, y - 1, col)
        c.line(x, y, x + 2, y, dark)
        c.set(x + 1, y - 1, col)


def pillow(c: Canvas, x, y, w, h, light=GROUND_L, base=GROUND, dark=GROUND_D):
    """A soft marshmallow mound: a dark belly, the body, a dithered light top and a shine."""
    c.ellipse(x, y + 1, w, h, dark)
    c.ellipse(x, y, w, h - 1, base)
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            dx, dy = (xx + 0.5 - (x + w * 0.42)) / (w * 0.42), (yy + 0.5 - (y + h * 0.3)) / (h * 0.45)
            d = dx * dx + dy * dy
            if c.get(xx, yy) == base and (d < 0.55 or (d < 1.0 and (xx + yy) % 2 == 0)):
                c.set(xx, yy, light)
    c.set(x + max(1, w // 4), y + 1 if h > 4 else y, '#ffffff')


def shade_cone(c: Canvas, cx, top, bottom, half_fn, ramp):
    """Fill a cone row by row, banded lit-left / shade-right with dithered seams. ramp: edge, lit, mid, shade, deep."""
    edge, lit, mid, sh, deep = ramp
    for y in range(top, bottom):
        h = half_fn(y)
        xl, xr = cx - h, cx + h
        for x in range(math.floor(xl), math.ceil(xr) + 1):
            if x + 0.5 < xl or x + 0.5 > xr:
                continue
            u = (x + 0.5 - xl) / (xr - xl) + ((BAYER4[y % 4][x % 4] + 0.5) / 16 - 0.5) * 0.08
            col = edge if u < 0.06 else lit if u < 0.36 else mid if u < 0.6 else sh if u < 0.88 else deep
            c.set(x, y, col)
