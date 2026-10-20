"""bg_dragon_path_morning: a winding stone road between candy-leaf trees, with the LOST THINGS OFFICE signpost
and the bubble-gum volcano far away (240x135, Endesga 64)."""
import math

from common import Canvas, Studio, OUT
from dl_parts import (shade_cone, sky, cloud, ball, gum_tree, gumdrop, tuft, pillow, check,
                      PINK, MINT, LEMON, CHERRY, GUM_PINK, GUM_BLUE,
                      GROUND_L, GROUND, GROUND_D, MOSS_L, MOSS, MOSS_D)

NAME = 'bg_dragon_path_morning'
HORIZON = 91

# stones: cool grey-blue, warm white highlight
ST_HI, ST, ST_SH, ST_JOINT = '#ffffff', '#c7cfdd', '#92a1b9', '#657392'
# wood
WOOD_HI, WOOD, WOOD_D, WOOD_DD, INK = '#f9e6cf', '#f6ca9f', '#e69c69', '#8a4836', '#5d2c28'
POST, POST_L, POST_D = '#8a4836', '#bf6f4a', '#5d2c28'

FONT = {
    'L': ['x..', 'x..', 'x..', 'x..', 'xxx'],
    'O': ['xxx', 'x.x', 'x.x', 'x.x', 'xxx'],
    'S': ['xxx', 'x..', 'xxx', '..x', 'xxx'],
    'T': ['xxx', '.x.', '.x.', '.x.', '.x.'],
    'H': ['x.x', 'x.x', 'xxx', 'x.x', 'x.x'],
    'I': ['xxx', '.x.', '.x.', '.x.', 'xxx'],
    'N': ['xx.', 'x.x', 'x.x', 'x.x', 'x.x'],
    'G': ['xxx', 'x..', 'x.x', 'x.x', 'xxx'],
    'F': ['xxx', 'x..', 'xx.', 'x..', 'x..'],
    'C': ['xxx', 'x..', 'x..', 'x..', 'xxx'],
    'E': ['xxx', 'x..', 'xx.', 'x..', 'xxx'],
}


def text_width(s):
    w = 0
    for i, ch in enumerate(s):
        w += 2 if ch == ' ' else 3
        if i < len(s) - 1:
            w += 1
    return w


def text(c: Canvas, s, x, y, col):
    for ch in s:
        if ch == ' ':
            x += 3
            continue
        c.blit(FONT[ch], {'x': col}, x, y)
        x += 4


# --- the road in perspective -------------------------------------------------------------------
def road_at(y):
    """Centre x and half width of the road on row y (perspective: s is the screen scale, d the distance)."""
    s = (y - HORIZON) / (135 - HORIZON)
    d = 1 / max(s, 1e-3)
    dd = min(d, 1 + (1.5 * math.pi + 0.25) / 1.3)   # past the last bend the road runs straight away
    cx = 140 + s * (30 * math.sin(1.3 * (dd - 1) - 0.25) - 22)
    return cx, 1.0 + 33 * s, s, d


def road(c: Canvas):
    # rows of stones: equal steps in distance
    bands = []
    d = 1.0
    while True:
        y = HORIZON + (135 - HORIZON) / d
        if y < HORIZON + 1.5:
            break
        bands.append(y)
        d += 0.32 * d ** 0.55
    bands = [136.0] + bands
    for y in range(HORIZON + 1, 135):
        cx, hw, s, d = road_at(y + 0.5)
        xl, xr = cx - hw, cx + hw
        # which band
        k = next((i for i in range(len(bands) - 1) if bands[i + 1] <= y < bands[i]), None)
        for x in range(math.floor(xl), math.ceil(xr) + 1):
            if not (xl <= x + 0.5 <= xr):
                continue
            if x + 0.5 - xl < 1.0 + s or xr - (x + 0.5) < 1.0 + s:
                c.set(x, y, ST_JOINT)
                continue
            if k is None or bands[k] - bands[k + 1] < 2.2:
                # far away: just a dithered stone texture
                c.set(x, y, ST_SH if (x + y) % 3 == 0 else ST)
                continue
            top, bot = bands[k + 1], bands[k]
            # stones per band: about 5 across, offset every other band
            n = 5
            u = (x + 0.5 - xl) / (xr - xl) * n + (0.5 if k % 2 else 0.0)
            fu = u - math.floor(u)
            sw = (xr - xl) / n   # stone width in px
            gap = 1.0 / sw
            if y >= bot - 1 or fu < gap:
                col = ST_JOINT
            elif y < top + 1 and bot - top >= 3:
                col = ST_HI if fu < 0.6 else ST
            elif y >= bot - 2 and bot - top >= 4:
                col = ST_SH
            elif fu > 1 - gap * 1.6 and sw >= 5:
                col = ST_SH
            else:
                col = ST
            c.set(x, y, col)
    # mint grass along the road edges, here and there
    for i, y in enumerate([97, 101, 106, 110, 115, 121, 126, 131, 99, 104, 112, 118, 124, 129, 134]):
        cx, hw, s, d = road_at(y)
        size = 3 if s > 0.45 else 2
        if i < 8:
            tuft(c, round(cx - hw - 4 - 2 * s), y, size=size)
        else:
            tuft(c, round(cx + hw + 1), y, size=size)


# --- the signpost ------------------------------------------------------------------------------
def arrow_board(c: Canvas, x, y, w, h, label):
    """A wooden board with an arrow tip on the right, lettered in dark brown."""
    mid = h // 2
    span = {j: x + w + (mid - abs(j - mid)) for j in range(h)}
    for j in range(h):
        for xx in range(x, span[j] + 1):
            edge = j in (0, h - 1) or xx in (x, span[j]) or (xx > span[j] - 1)
            col = WOOD_DD if edge else WOOD
            if not edge and j == 1:
                col = WOOD_HI
            elif not edge and j == h - 2:
                col = WOOD_D
            c.set(xx, y + j, col)
        # the diagonal edges of the tip are two pixels wide where they step
        if 0 < j < h - 1 and span[j] - span[j - 1 if j <= mid else j + 1] != 0:
            pass
    # wood grain
    for (gx, gy, gl) in [(x + 2, y + 3, 4), (x + w - 9, y + h - 4, 5), (x + w // 2, y + 2, 3)]:
        c.line(gx, gy, gx + gl - 1, gy, WOOD_D)
    # nails
    c.set(x + 1, y + 2, INK)
    c.set(x + 1, y + h - 3, INK)
    tx = x + 3 + (w - 3 - text_width(label)) // 2
    # clear grain behind the letters
    c.rect(tx - 1, y + 2, text_width(label) + 2, 5, WOOD)
    text(c, label, tx, y + 2, INK)


def signpost(c: Canvas, x, ground):
    # shadow and post
    c.ellipse(x - 6, ground - 2, 16, 4, GROUND_D)
    c.rect(x, ground - 52, 4, 52, POST)
    c.line(x, ground - 52, x, ground - 1, POST_L)
    c.line(x + 3, ground - 52, x + 3, ground - 1, POST_D)
    c.rect(x - 1, ground - 54, 6, 2, POST_D)
    c.set(x, ground - 54, POST)
    w1 = text_width('LOST THINGS') + 7
    w2 = text_width('OFFICE') + 7
    arrow_board(c, x - 4, ground - 49, w1, 9, 'LOST THINGS')
    arrow_board(c, x - 2, ground - 37, w2, 9, 'OFFICE')
    # a little tuft and a flower at its foot
    tuft(c, x - 4, ground, size=3)
    tuft(c, x + 4, ground + 1, size=3)
    c.set(x + 7, ground - 3, '#ffeb57')
    c.set(x + 7, ground - 2, MOSS_D)


# --- the far volcano ---------------------------------------------------------------------------
def far_volcano(c: Canvas, cx, top, base):
    rim, foot = 5.5, 30

    def half(y):
        t = max(0.0, (y - top) / (base - top))
        return rim + 2 * math.sqrt(t) + (foot - rim - 2) * t ** 1.5
    shade_cone(c, cx, top, base, half, ('#e69c69', '#f6ca9f', '#e69c69', '#bf6f4a', '#8a4836'))
    # gum icing and a few bubbles
    for x in range(cx - 8, cx + 9):
        h = half(top + 2) + 0.4
        if abs(x + 0.5 - cx) > h + 1:
            continue
        ramp = GUM_PINK if x < cx else GUM_BLUE
        ln = 3 + {-6: 2, -5: 4, -4: 4, -1: 6, 0: 6, 3: 3, 4: 5, 5: 5, 7: 2}.get(x - cx, 0)
        for y in range(top - 1, top + ln):
            if abs(x + 0.5 - cx) <= half(y) + 0.4:
                c.set(x, y, ramp[2] if y == top - 1 else ramp[0] if y == top + ln - 1 else ramp[1])
    c.line(cx - 3, top - 1, cx + 2, top - 1, '#5d2c28')
    ball(c, cx - 1, top - 5, 3.2, GUM_PINK)
    ball(c, cx + 4, top - 8, 2.2, GUM_BLUE)
    c.set(cx - 3, top - 11, GUM_PINK[1])
    c.rect(cx - 3, top - 12, 2, 2, GUM_PINK[1])
    c.rect(cx + 1, top - 15, 2, 2, GUM_BLUE[1])


def build() -> Canvas:
    c = Canvas(240, 135)
    sky(c, HORIZON + 4)
    # a soft morning sun
    c.circle(212, 18, 10, '#ffeb57')
    c.circle(212, 18, 7.5, '#ffffff')
    cloud(c, 18, 12, 1.0)
    cloud(c, 120, 6, 0.8, flip=True)
    cloud(c, 182, 32, 0.6)
    cloud(c, 70, 40, 0.45, flip=True)
    # far volcano behind the hills
    far_volcano(c, 160, 56, 90)
    # far hills
    hill = lambda x: 84 + 3 * math.sin(x / 15.0 + 1) + 2 * math.sin(x / 5.7)
    c.hills(0, 240, 0, lambda x: max(hill(x), 84 + 6 * math.exp(-((x - 160) / 30) ** 2)) if 132 < x < 188 else hill(x), '#5ac54f')
    c.vgradient(82, HORIZON + 3, ['#5ac54f', '#33984b'], mask=lambda x, y: c.get(x, y) == '#5ac54f' and y > 85)
    # tiny far lollipop trees on the hills
    for (x, y, ramp) in [(18, 84, PINK), (40, 86, MINT), (96, 85, PINK), (206, 85, MINT), (226, 84, PINK), (116, 87, MINT)]:
        c.rect(x, y, 1, 4, '#ffffff')
        ball(c, x + 0.5, y - 1, 2.6, ramp)
    # ground
    top = {x: HORIZON + round(0.8 * math.sin(x / 9.0)) for x in range(240)}
    for x in range(240):
        for y in range(top[x], 135):
            c.set(x, y, GROUND)
        c.set(x, top[x], GROUND_L)
    c.vgradient(HORIZON + 1, HORIZON + 10, [GROUND_L, GROUND])
    c.vgradient(124, 135, [GROUND, GROUND_D], mask=lambda x, y: x < 70 or x > 190)
    # pillows and moss at the sides
    for (x, y, w, h) in [(2, 98, 10, 3), (54, 97, 8, 3), (196, 99, 10, 3), (0, 112, 16, 5), (206, 110, 15, 5),
                         (4, 126, 22, 8), (210, 125, 24, 9), (180, 118, 14, 5), (40, 120, 14, 5)]:
        pillow(c, x, y, w, h)
    for (x, y, w, h) in [(20, 104, 18, 4), (182, 104, 16, 4), (160, 124, 18, 5), (62, 128, 18, 6), (224, 102, 14, 3)]:
        c.ellipse(x, y + 1, w, h, MOSS_D)
        c.ellipse(x, y, w, h, MOSS)
        c.ellipse(x + 2, y, w - 4, max(1, h // 2), MOSS_L)
        for i in range(x + 1, x + w - 4, 5):
            tuft(c, i, y + 1, size=3 if h > 4 else 2)
    road(c)
    # trees along the road, far to near (pink and mint)
    trees = [  # (x, ground, h, r, ramp)
        (150, 94, 7, 3, MINT), (113, 95, 8, 3.5, PINK), (160, 97, 11, 5, PINK), (98, 99, 13, 6, MINT),
        (186, 103, 19, 8, MINT), (70, 104, 21, 9, PINK),
        (224, 116, 42, 15, PINK), (6, 122, 48, 17, MINT),
    ]
    for (x, g, h, r, ramp) in trees:
        stripe = ('#ea323c', '#c42430') if ramp is MINT else ('#0098dc', '#0069aa')
        gum_tree(c, x, g, h, r, ramp, stripe=stripe, shadow=GROUND_D if r > 5 else None)
    signpost(c, 38, 112)
    # gumdrops and flowers by the road
    for (x, y, w, ramp) in [(196, 128, 5, CHERRY), (30, 131, 5, LEMON), (176, 110, 3, LEMON), (60, 112, 4, CHERRY)]:
        gumdrop(c, x, y, w, ramp)
    for i, col in enumerate(['#ffeb57', '#ffffff', '#f389f5']):
        c.speckle(0, 100, 240, 35, col, 0.006, seed=40 + i, on=GROUND)
    check(c)
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    with Studio() as s:
        print(s.image(build(), NAME, OUT / f'{NAME}.png', 1920, 1080))
