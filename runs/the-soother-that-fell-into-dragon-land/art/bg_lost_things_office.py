"""bg_lost_things_office_any: Nib's Lost Things Office (240x135, Endesga 64).

Pale yellow striped walls with wood panelling, tall shelves on both sides full of tagged lost things, a big desk at the
back with an open ledger, an ink pot and a glowing green lamp, a round window onto Dragon Land's green sky, a red rug.
"""
import math

from common import Canvas, Studio, OUT
from fx_light import glow, vignette, darken, lighten, check

K = '#391f21'
WOOD_L, WOOD, WOOD_D, WOOD_DD = '#e69c69', '#bf6f4a', '#8a4836', '#5d2c28'

RED = ('#f5555d', '#ea323c', '#c42430')
BLUE = ('#00cdf9', '#0098dc', '#0069aa')
GREEN = ('#99e65f', '#5ac54f', '#33984b')
YELLOW = ('#ffeb57', '#ffc825', '#edab50')
PURPLE = ('#ca52c9', '#93388f', '#622461')
PINK = ('#fdd2ed', '#f68187', '#c85086')
HONEY = ('#f6ca9f', '#e69c69', '#bf6f4a')
ORANGE = ('#ffa214', '#ed7614', '#c64524')
SNOW = ('#ffffff', '#c7cfdd', '#92a1b9')
CARD = ('#f6ca9f', '#e69c69', '#bf6f4a')

# hand-drawn lost things; l/m/d = the item's ramp, a/A = accent ramp mid/dark, k dark, w white, g pale grey,
# p pale skin, s glass blue, o orange, h wooden handle
ITEMS = {
    'teddy': [".mm....mm.", "mpmmmmmmpd", ".mlmmmmmd.", ".mkmmmmkd.", ".mmmppmmd.", "..mpkkpd..",
              "...mmmd...", ".lmmmmmmd.", "lmmppppmdd", "mmmppppmdd", ".mmmppmmd.", ".mdd..mdd."],
    'duck': [".ll....", "lykl...", "yyyoo..", ".yy...l", "lyyyyyy", "yyyyyyY", ".YYYYY."],
    'sock': ["wwww..", "mmmd..", "aaaA..", "mmmd..", "aaaA..", "mmmd..", "mmmmm.", "mmmmmd", ".dddd."],
    'tophat': ["..lmmmd..", "..lmmmd..", "..lmmmd..", "..lmmmd..", "..aaaaA..", "..lmmmd..", "lmmmmmmmd",
               ".ddddddd."],
    'strawhat': ["....lmmm....", "...lmmmmd...", "...aaaaaA...", "lmmmmmmmmmmd", ".dddddddddd."],
    'cap': ["..lmmd....", ".lmmmmd...", "lmmwmmmd..", "mmmmmmmmml", "dddddddddd"],
    'bobble': ["...wg...", "..wwwg..", "...mm...", "..lmmd..", ".lmmmmd.", ".lmmmmd.", "lmmmmmmd", "wawawawa",
               "awawawaw"],
    'key': [".lll.....", "l..lmmmmm", "l..lmmmmd", ".mmm..d.d"],
    'keyv': [".l.", "l.l", ".l.", ".m.", ".mm", ".m.", ".mm", ".d."],
    'car': ["...lmmd...", "..lssmmd..", "lmmmmmmmmd", "wmmmmmmmmd", "dkkdddkkdd", ".kk...kk.."],
    'boat': [".....h.....", "....wh.....", "...wwh.....", "..wwwh.....", ".wwwgh.....", ".....h.....",
             "lmmmmmmmmmd", ".dmmmmmmmd.", "..ddddddd.."],
    'umbrella': [".hh...............", "h..h.lmmmmmmmmmm..", "....hmmmmmmmmmmmmk", ".....dddddddddd..."],
    'glasses': [".mmm.mmm.", "msssmsssm", ".mmm.mmm."],
    'clock': ["mm...mm", "m.lll.m", ".lwwwd.", "lwwkwwd", "lwwkkwd", "lwwwwwd", ".ldddd.", ".d...d."],
    'box': ["llllllllll", "mmmmmmmmmd", "mmwwwwmmmd", "mmwwwwmmmd", "mmmmmmmmmd", "mmmmmmmmmd", "dddddddddd"],
    'scarf': ["lmmmmmmmmmmd", "aaaaaaaaaaaA", "lmmmmmmmmmmd", "aaaaaaaaaaaA", "w.w.w.w.w.w."],
    'mug': ["gggggg..", "lmmmmd..", "lmwmmddd", "lmmmmd.d", "lmmmmd.d", "lmmmmddd", "lmmmmd..", ".dddd..."],
    'boot': ["lmmmd..", "lmmmd..", "lmmmd..", "lmmmd..", "lmmmd..", "lmmmmmd", "lmmmmmmd", "dddddddd"],
}
# where each item's tag string is tied (relative to the item's top-left)
TAG_AT = {
    'teddy': (8, 7), 'duck': (5, 3), 'sock': (3, 1), 'tophat': (6, 4), 'strawhat': (10, 3), 'cap': (8, 3),
    'bobble': (6, 6), 'key': (7, 2), 'keyv': (2, 4), 'car': (8, 2), 'boat': (9, 6), 'umbrella': (15, 1),
    'glasses': (7, 1), 'clock': (5, 3), 'box': (8, 1), 'scarf': (10, 1), 'boot': (4, 2), 'mug': (4, 1),
}


def tag(c: Canvas, x, y):
    """A tiny white tag tied at (x, y): a pale string pixel, then a 3x2 card hanging down-right."""
    c.set(x, y, '#c7cfdd')
    c.rect(x + 1, y + 1, 3, 2, '#ffffff')
    c.set(x + 3, y + 2, '#c7cfdd')


def item(c: Canvas, name, x, bottom, ramp, accent=RED, with_tag=True):
    rows = ITEMS[name]
    top = bottom - len(rows) + 1
    l, m, d = ramp
    legend = {'l': l, 'm': m, 'd': d, 'a': accent[1], 'A': accent[2], 'k': K, 'w': '#ffffff', 'g': '#c7cfdd',
              'p': '#f9e6cf', 's': '#94fdff', 'o': '#ed7614', 'h': '#e69c69',
              'y': '#ffc825', 'Y': '#edab50'}
    c.blit(rows, legend, x, top)
    if with_tag:
        tx, ty = TAG_AT[name]
        tag(c, x + tx, top + ty)


def ball(c: Canvas, cx, bottom, r, ramp, stripe=None, with_tag=True):
    l, m, d = ramp
    cy = bottom - r + 0.5
    c.circle(cx, cy, r, d)
    c.circle(cx - 0.5, cy - 0.5, r - 0.6, m)
    if stripe:
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                if c.get(x, y) == m and abs((x - cx) + (y - cy) * 0.4) < r * 0.28:
                    c.set(x, y, stripe)
    c.set(int(cx - r * 0.45), int(cy - r * 0.45), '#ffffff')
    if r >= 3:
        c.set(int(cx - r * 0.45) + 1, int(cy - r * 0.45), l)
        c.set(int(cx - r * 0.45), int(cy - r * 0.45) + 1, l)
    if with_tag:
        tag(c, int(cx + r * 0.5), int(cy - r * 0.7))


def jar(c: Canvas, x, bottom, seed=1):
    """A glass jar of lost buttons."""
    top = bottom - 9
    c.rect(x + 1, top, 6, 2, WOOD)
    c.rect(x + 1, top, 6, 1, WOOD_L)
    c.rect(x, top + 2, 8, 8, '#c7cfdd')
    c.rect(x + 1, top + 3, 6, 6, '#92a1b9')
    cols = ['#ea323c', '#ffc825', '#0098dc', '#5ac54f', '#f389f5', '#ffffff']
    i = seed
    for yy in range(top + 4, top + 9):
        for xx in range(x + 1, x + 7):
            if (xx * 3 + yy * 5 + seed) % 3:
                c.set(xx, yy, cols[i % len(cols)])
                i += 7
    c.line(x + 1, top + 3, x + 1, top + 6, '#ffffff')
    tag(c, x + 6, top + 1)


def yoyo(c: Canvas, cx, bottom, ramp):
    l, m, d = ramp
    cy = bottom - 3
    c.circle(cx, cy + 0.5, 3.5, d)
    c.circle(cx - 0.5, cy, 3, m)
    c.line(cx - 3, cy, cx + 2, cy, d)
    c.set(cx - 2, cy - 2, l)
    c.set(cx - 1, cy - 2, '#ffffff')
    for y in range(cy - 12, cy):
        c.set(cx, y, '#f9e6cf')
    tag(c, cx, cy - 10)


def books(c: Canvas, x, bottom, cols):
    for i, (col, h) in enumerate(cols):
        c.rect(x + i * 3, bottom - h + 1, 3, h, col[1])
        c.line(x + i * 3, bottom - h + 1, x + i * 3, bottom, col[0])
        c.set(x + i * 3 + 1, bottom - h + 3, '#ffeb57')


def shelf_unit(c: Canvas, x0, side):
    """Front face of a tall shelf at x0 (72 wide), with its inner side face receding towards the middle.
    side = +1 when the unit is on the left (side face to its right), -1 on the right. Returns compartments."""
    w = 72
    top, bot = 6, 106
    # side face (towards the vanishing point at 120, 60)
    if side > 0:
        fx, bx = x0 + w, x0 + w + 8
    else:
        fx, bx = x0, x0 - 8
    c.polygon([(fx, 4), (bx, 14), (bx, 98), (fx, 107)], WOOD)
    # board edges on the side face, receding
    for by in (28, 50, 72, 94):
        for i in range(9):
            xx = fx + (i if side > 0 else -i - 1)
            t = i / 8
            yy = round(by + (60 - by) * t * 8 / 46)
            c.set(xx, yy, WOOD_L)
            c.set(xx, yy + 1, WOOD_D)
    c.line(bx - (1 if side > 0 else 0), 14, bx - (1 if side > 0 else 0), 98, WOOD_D)
    # front frame
    c.rect(x0, top, w, bot - top, WOOD_D)
    c.rect(x0 - 1, top - 2, w + 2, 3, WOOD_DD)   # cornice
    c.rect(x0 - 1, top - 2, w + 2, 1, WOOD)
    c.rect(x0, top + 1, w, 1, WOOD_L)
    c.line(x0, top + 1, x0, bot - 1, WOOD)
    c.line(x0 + 1, top + 1, x0 + 1, bot - 1, WOOD)
    c.line(x0 + w - 1, top + 1, x0 + w - 1, bot - 1, WOOD_DD)
    comps = []
    cols = [(x0 + 3, 31), (x0 + 37, 32)]
    rows = [(9, 19), (31, 19), (53, 19), (75, 19)]
    for (cx, cw) in cols:
        for (cy, ch) in rows:
            c.rect(cx, cy, cw, ch, WOOD_DD)
            c.rect(cx, cy, cw, 2, K)                 # shadow under the board above
            c.dither_fill(cx, cy + 2, cw, 2, WOOD_DD, K, 0.5)
            c.line(cx, cy, cx, cy + ch - 1, K)       # shadow of the frame
            comps.append((cx, cy, cw, ch))
    # shelf boards: lit top edge, mid, dark lip
    for by in (28, 50, 72):
        c.rect(x0 + 2, by, w - 3, 3, WOOD)
        c.rect(x0 + 2, by, w - 3, 1, WOOD_L)
        c.rect(x0 + 2, by + 2, w - 3, 1, WOOD_D)
    # middle divider
    c.rect(x0 + 34, top + 2, 3, 88, WOOD)
    c.line(x0 + 34, top + 2, x0 + 34, 93, WOOD_L)
    c.line(x0 + 36, top + 2, x0 + 36, 93, WOOD_D)
    # plinth with drawers and labels
    c.rect(x0 + 2, 94, w - 3, 1, WOOD_L)
    for (dx, dw) in [(x0 + 3, 31), (x0 + 37, 32)]:
        c.rect(dx, 96, dw, 8, WOOD)
        c.rect(dx, 96, dw, 1, WOOD_L)
        c.rect(dx, 103, dw, 1, WOOD_D)
        c.line(dx + dw - 1, 96, dx + dw - 1, 103, WOOD_D)
        mx = dx + dw // 2
        c.rect(mx - 3, 97, 6, 3, '#ffffff')
        c.rect(mx - 3, 99, 6, 1, '#c7cfdd')
        c.rect(mx - 1, 101, 2, 2, '#ffc825')
        c.set(mx, 102, '#edab50')
    c.rect(x0, bot - 1, w, 2, WOOD_DD)
    return comps


def build() -> Canvas:
    c = Canvas(240, 135)

    # --- back wall: pale yellow, dithered darker towards the ceiling, with soft stripes ---------------------
    c.vgradient(6, 40, ['#ffc825', '#ffeb57'])
    c.rect(0, 40, 240, 38, '#ffeb57')
    for y in range(6, 78):
        for x in range(240):
            if x % 12 in (0, 1):
                col = c.get(x, y)
                c.set(x, y, {'#ffeb57': '#f9e6cf', '#ffc825': '#ffeb57'}.get(col, col))
    # ceiling beam
    c.rect(0, 0, 240, 6, WOOD_D)
    c.rect(0, 0, 240, 2, WOOD_DD)
    c.rect(0, 5, 240, 1, WOOD)
    c.rect(0, 6, 240, 1, '#edab50')
    # wainscot panels
    c.rect(0, 78, 240, 20, WOOD_D)
    c.rect(0, 76, 240, 2, WOOD_L)
    c.rect(0, 77, 240, 1, WOOD)
    c.rect(0, 78, 240, 1, WOOD_DD)
    for px in range(2, 240, 16):
        c.rect(px, 81, 12, 11, WOOD_DD)
        c.rect(px + 1, 82, 11, 10, WOOD)
        c.rect(px + 1, 82, 11, 1, WOOD_DD)
        c.line(px + 1, 82, px + 1, 91, WOOD_DD)
        c.rect(px + 2, 91, 10, 1, WOOD_L)
    c.rect(0, 94, 240, 4, WOOD_DD)
    c.rect(0, 94, 240, 1, WOOD)

    # --- floor: warm planks converging on the middle ---------------------------------------------------------
    c.rect(0, 98, 240, 37, WOOD)
    vx, vy = 120, 30
    xs = list(range(-260, 520, 15))
    for i, xb in enumerate(xs):
        for y in range(98, 135):
            x = round(vx + (xb - vx) * (y - vy) / (135 - vy))
            c.set(x, y, WOOD_D)
    # plank seams, staggered
    for i in range(len(xs) - 1):
        for sy in ([103, 117] if i % 2 else [109, 127]):
            xa = vx + (xs[i] - vx) * (sy - vy) / (135 - vy)
            xb2 = vx + (xs[i + 1] - vx) * (sy - vy) / (135 - vy)
            for x in range(round(xa) + 1, round(xb2)):
                c.set(x, sy, WOOD_D)
    c.rect(0, 98, 240, 1, WOOD_DD)

    # --- rug in the middle -----------------------------------------------------------------------------------
    c.ellipse(56, 108, 128, 25, '#891e2b')
    c.ellipse(57, 107, 126, 24, '#c42430')
    c.ellipse(60, 109, 120, 20, '#ffc825')
    c.ellipse(61, 110, 118, 18, '#ea323c')
    c.ellipse(76, 113, 88, 12, '#c42430')
    c.ellipse(78, 114, 84, 10, '#f5555d')
    c.ellipse(90, 116, 60, 6, '#ea323c')
    for (dx, col) in [(0, '#ffc825'), (-32, '#ffeb57'), (32, '#ffeb57')]:
        cx = 120 + dx
        c.polygon([(cx - 3, 119), (cx, 116), (cx + 3, 119), (cx, 122)], col)
    for x in range(64, 178, 6):
        y = round(119 - 9.5 * math.sqrt(max(0, 1 - ((x + 0.5 - 120) / 59) ** 2)))
        c.set(x, y, '#fdd2ed')
    for y in range(114, 126, 2):  # tassels
        c.set(55, y, '#f9e6cf')
        c.set(184, y, '#f9e6cf')
    darken(c, 56, 129, 128, 4, 0.8, mask=lambda x, y, col: col in ('#c42430', '#891e2b', '#ffc825', '#ea323c'))

    # --- round window onto Dragon Land ------------------------------------------------------------------------
    wx, wy = 120, 33
    c.circle(wx + 1, wy + 1, 17, WOOD_DD)
    c.circle(wx, wy, 17, WOOD_D)
    c.circle(wx, wy, 15, WOOD)
    c.circle(wx - 0.5, wy - 0.5, 14.5, WOOD_L)
    c.circle(wx, wy, 13, WOOD_DD)
    inside = lambda x, y: (x + 0.5 - wx) ** 2 + (y + 0.5 - wy) ** 2 <= 12.4 ** 2
    c.vgradient(wy - 13, wy + 13, ['#5ac54f', '#99e65f', '#d3fc7e'], mask=inside)
    for x in range(wx - 13, wx + 14):
        h1 = wy + 6 + 2.5 * math.sin(x / 5.0)
        h2 = wy + 9 + 2 * math.sin(x / 3.3 + 1)
        for y in range(round(h1), wy + 14):
            if inside(x, y):
                c.set(x, y, '#33984b')
        for y in range(round(h2), wy + 14):
            if inside(x, y):
                c.set(x, y, '#1e6f50')
    for (cx, cy, w, h) in [(104, 24, 10, 4), (107, 22, 5, 4), (128, 29, 8, 3), (130, 27, 4, 3)]:
        for y in range(cy, cy + h):
            for x in range(cx, cx + w):
                if inside(x, y) and ((x + 0.5 - cx - w / 2) / (w / 2)) ** 2 + ((y + 0.5 - cy - h / 2) / (h / 2)) ** 2 <= 1:
                    c.set(x, y, '#ffffff')
    for x in range(102, 116):
        if inside(x, 26) and c.get(x, 26) == '#ffffff' and c.get(x, 27) != '#ffffff':
            c.set(x, 26, '#c7cfdd')
    # mullions and shine
    c.rect(wx - 1, wy - 13, 2, 26, WOOD)
    c.rect(wx - 13, wy - 1, 26, 2, WOOD)
    c.line(wx, wy - 13, wx, wy + 12, WOOD_D)
    c.line(wx - 13, wy, wx + 12, wy, WOOD_D)
    for i in range(3):
        c.set(wx - 8 + i, wy - 6 - i, '#ffffff')
    c.set(wx - 9, wy - 4, '#ffffff')
    # sill with a little potted plant
    c.rect(102, 50, 36, 3, WOOD)
    c.rect(102, 50, 36, 1, WOOD_L)
    c.rect(103, 53, 34, 1, '#edab50')
    c.rect(129, 45, 6, 5, '#c64524')
    c.rect(128, 45, 8, 1, '#e07438')
    c.line(129, 46, 129, 49, '#e07438')
    c.blit(['.g.g..', 'gGgGg.', '.gGgGg', 'gGgg..', '.g.g..'], {'g': '#5ac54f', 'G': '#99e65f'}, 129, 40)

    # --- kite on the left bit of wall ----------------------------------------------------------------------
    kx, ky = 93, 26
    top, rgt, bot, lft = (kx, ky - 13), (kx + 9, ky - 1), (kx, ky + 15), (kx - 9, ky - 1)
    sh = lambda p: (p[0] + 2, p[1] + 2)
    c.polygon([sh(top), sh(rgt), sh(bot), sh(lft)], '#edab50')
    c.polygon([top, rgt, (kx, ky - 1)], '#ffeb57')
    c.polygon([top, (kx, ky - 1), lft], '#ea323c')
    c.polygon([lft, (kx, ky - 1), bot], '#0098dc')
    c.polygon([(kx, ky - 1), rgt, bot], '#5ac54f')
    c.line(kx, ky - 12, kx, ky + 14, WOOD_D)
    c.line(kx - 8, ky - 1, kx + 8, ky - 1, WOOD_D)
    # tail with bows
    pts = [(kx + round(3 * math.sin(i / 3.0)), ky + 15 + i) for i in range(0, 34)]
    for (x, y) in pts:
        c.set(x, y, '#c7cfdd')
    for j, col in enumerate(['#f5555d', '#ffc825', '#00cdf9', '#99e65f']):
        x, y = pts[5 + j * 8]
        c.blit(['b.b', '.b.', 'b.b'], {'b': col}, x - 1, y - 1)
    tag(c, kx + 4, ky + 5)

    # --- key board on the right bit of wall: hooks with tagged keys ----------------------------------------
    c.rect(140, 18, 18, 30, WOOD_D)
    c.rect(141, 19, 16, 28, WOOD)
    c.rect(141, 19, 16, 1, WOOD_L)
    c.rect(141, 46, 16, 1, WOOD_D)
    c.rect(142, 48, 16, 1, '#edab50')
    for (hx, hy, ramp) in [(144, 21, YELLOW), (151, 21, SNOW), (144, 33, SNOW), (151, 33, YELLOW)]:
        c.set(hx + 1, hy, '#c7cfdd')
        c.set(hx + 1, hy + 1, '#92a1b9')
        item(c, 'keyv', hx, hy + 9, ramp, with_tag=False)
        tag(c, hx + 2, hy + 5)

    # --- the big desk -------------------------------------------------------------------------------------------
    dx0, dx1 = 82, 158
    c.polygon([(dx0 + 3, 73), (dx1 - 3, 73), (dx1, 77), (dx0, 77)], WOOD)
    c.line(dx0 + 3, 73, dx1 - 4, 73, WOOD_D)
    c.rect(dx0, 77, dx1 - dx0, 2, WOOD_L)
    c.rect(dx0 + 1, 79, dx1 - dx0 - 2, 22, WOOD_D)
    c.rect(dx0 + 1, 79, dx1 - dx0 - 2, 1, WOOD_DD)
    for (px, pw) in [(dx0 + 3, 22), (dx1 - 25, 22)]:   # pedestals with three drawers
        for i in range(3):
            y = 81 + i * 6
            c.rect(px, y, pw, 5, WOOD)
            c.rect(px, y, pw, 1, WOOD_L)
            c.line(px + pw - 1, y, px + pw - 1, y + 4, WOOD_DD)
            c.rect(px, y + 4, pw, 1, WOOD_DD)
            mx = px + pw // 2
            c.rect(mx - 3, y + 1, 4, 2, '#ffffff')
            c.set(mx, y + 2, '#c7cfdd')
            c.set(mx + 3, y + 2, '#ffc825')
    c.rect(dx0 + 27, 81, 22, 5, WOOD)                    # middle drawer
    c.rect(dx0 + 27, 81, 22, 1, WOOD_L)
    c.rect(dx0 + 27, 85, 22, 1, WOOD_DD)
    c.rect(dx0 + 36, 83, 4, 1, '#ffc825')
    c.rect(dx0 + 27, 87, 22, 13, K)                      # knee hole
    c.rect(dx0 + 27, 87, 22, 2, '#1c121c')
    c.rect(dx0 + 1, 99, dx1 - dx0 - 2, 2, WOOD_DD)
    darken(c, dx0 - 2, 101, dx1 - dx0 + 4, 3, 1.0)       # shadow on the floor
    darken(c, dx0, 104, dx1 - dx0, 1, 0.5)

    # the lamp's warm glow on the wall, desk and floor (drawn before the desk things and the shelves)
    glow(c, 93, 60, 58, 42, 1.0, power=0.6)
    glow(c, 93, 66, 30, 20, 1.0, power=1.0, mask=lambda x, y, col: col not in ('#f9e6cf', '#ffffff'))

    # lamp (green banker's lamp) on the left of the desk
    lamp = ["....lllllll....", "...lmmmmmmmd...", "..lmmmmmmmmmd..", ".lmmmmmmmmmmmd.", "kkkkkkkkkkkkkkk",
            ".ggggggggggggg."]
    c.blit(lamp, {'l': '#99e65f', 'm': '#5ac54f', 'd': '#33984b', 'k': '#1e6f50', 'g': '#ffffff'}, 86, 56)
    c.set(88, 58, '#d3fc7e')
    c.set(89, 57, '#d3fc7e')
    c.rect(93, 62, 1, 11, '#edab50')
    c.set(92, 62, '#ffc825')
    c.rect(94, 62, 1, 11, '#bf6f4a')
    c.rect(93, 62, 1, 1, '#ffeb57')
    c.blit(["...bbbbb...", ".lbbbbbbbB.", "BBBBBBBBBBB"], {'b': '#ffc825', 'l': '#ffeb57', 'B': '#edab50'}, 88, 72)
    # light pool under the shade
    lighten(c, 87, 62, 14, 12, 1.0, mask=lambda x, y, col: abs(x - 93.5) < 7 + (y - 62) * 0.35)
    # ledger: a thick open book
    lx = 106
    c.rect(lx - 2, 74, 34, 3, '#891e2b')                 # red cover
    c.rect(lx - 2, 74, 34, 1, '#c42430')
    c.rect(lx - 2, 76, 34, 1, '#571c27')
    c.rect(lx, 70, 30, 4, '#f6ca9f')                      # thick block of pages
    for y in (71, 73):
        for x in range(lx, lx + 30):
            if (x + y) % 3:
                c.set(x, y, '#e69c69')
    c.polygon([(lx - 1, 62), (lx + 6, 60.5), (lx + 15, 62), (lx + 24, 60.5), (lx + 31, 62), (lx + 31, 70),
               (lx - 1, 70)], '#bf6f4a')
    c.polygon([(lx, 63), (lx + 6, 61.5), (lx + 15, 63), (lx + 15, 70), (lx, 70)], '#f9e6cf')
    c.polygon([(lx + 15, 63), (lx + 24, 61.5), (lx + 30, 63), (lx + 30, 70), (lx + 15, 70)], '#ffffff')
    c.line(lx - 1, 63, lx - 1, 73, '#bf6f4a')
    c.line(lx + 31, 63, lx + 31, 73, '#bf6f4a')
    c.line(lx + 15, 62, lx + 15, 70, '#c7cfdd')
    c.line(lx + 14, 63, lx + 14, 69, '#f6ca9f')
    for row in (64, 66, 68):
        for x in range(lx + 2, lx + 13):
            if (x * 5 + row) % 7 not in (0, 3):
                c.set(x, row, '#92a1b9')
        for x in range(lx + 17, lx + 28):
            if (x * 3 + row) % 6 not in (0,):
                c.set(x, row, '#c7cfdd')
    c.rect(lx + 22, 70, 1, 8, '#ea323c')                 # ribbon bookmark
    c.set(lx + 22, 78, '#c42430')
    # ink pot and quill
    c.blit(["..ss..", ".dmmd.", "dmlmmd", "dmmmmd", ".dddd."], {'s': WOOD_D, 'd': '#2a2f4e', 'm': '#424c6e',
                                                                  'l': '#92a1b9'}, 139, 71)
    for i in range(10):
        c.set(141 + i // 2, 71 - i, '#c7cfdd' if i < 2 else '#ffffff')
        if 3 <= i <= 9:
            c.set(142 + i // 2, 71 - i, '#c7cfdd')
    c.set(146, 61, '#ffffff')
    # reception bell
    c.blit(["..y..", ".lyy.", "lyyyY", "BBBBB"], {'y': '#ffc825', 'l': '#ffeb57', 'Y': '#edab50', 'B': '#8a4836'},
           149, 72)
    # neat stack of blank tags
    c.rect(98, 74, 4, 2, '#ffffff')
    c.rect(98, 75, 4, 1, '#c7cfdd')
    c.rect(99, 73, 4, 1, '#ffffff')

    # --- shelves full of lost things ----------------------------------------------------------------------------
    L = shelf_unit(c, 2, +1)
    R = shelf_unit(c, 166, -1)
    # left unit: compartments are listed column A top..bottom, then column B
    (ax, _, _, _) = L[0]
    (bx, _, _, _) = L[4]
    item(c, 'bobble', ax + 2, 27, RED, accent=SNOW)
    item(c, 'strawhat', ax + 13, 27, YELLOW, accent=PINK)
    item(c, 'tophat', bx + 2, 27, PURPLE, accent=YELLOW)
    item(c, 'cap', bx + 16, 27, BLUE)
    item(c, 'teddy', ax + 2, 49, HONEY)
    item(c, 'duck', ax + 17, 49, YELLOW)
    item(c, 'sock', bx + 2, 49, SNOW, accent=RED)
    item(c, 'sock', bx + 12, 49, BLUE, accent=YELLOW)
    item(c, 'sock', bx + 22, 49, GREEN, accent=PINK)
    item(c, 'key', ax + 2, 71, YELLOW)
    item(c, 'key', ax + 2, 66, SNOW)
    item(c, 'box', ax + 16, 71, CARD)
    item(c, 'teddy', bx + 2, 71, PINK)
    item(c, 'car', bx + 17, 71, RED)
    ball(c, ax + 6, 93, 4.5, RED, stripe='#ffffff')
    ball(c, ax + 17, 93, 3.5, BLUE)
    ball(c, ax + 26, 93, 2.5, GREEN)
    item(c, 'boot', bx + 2, 93, YELLOW)
    yoyo(c, bx + 16, 93, BLUE)
    jar(c, bx + 23, 93)
    # right unit
    (ax, _, _, _) = R[0]
    (bx, _, _, _) = R[4]
    item(c, 'umbrella', ax + 2, 27, PURPLE)
    item(c, 'glasses', ax + 21, 27, RED)
    item(c, 'bobble', bx + 3, 27, GREEN, accent=YELLOW)
    item(c, 'strawhat', bx + 15, 27, ORANGE, accent=BLUE)
    item(c, 'boat', ax + 2, 49, RED)
    item(c, 'mug', ax + 18, 49, PINK)
    item(c, 'teddy', bx + 2, 49, SNOW)
    ball(c, bx + 20, 49, 4.5, YELLOW, stripe='#ea323c')
    item(c, 'scarf', ax + 2, 71, BLUE, accent=SNOW)
    item(c, 'scarf', ax + 2, 66, PINK, accent=PURPLE, with_tag=False)
    item(c, 'duck', ax + 19, 71, YELLOW)
    books(c, bx + 2, 71, [(GREEN, 12), (RED, 14), (BLUE, 11)])
    tag(c, bx + 7, 59)
    jar(c, bx + 14, 71, seed=4)
    item(c, 'key', bx + 23, 71, YELLOW)
    item(c, 'sock', ax + 2, 93, PURPLE, accent=PINK)
    item(c, 'sock', ax + 11, 93, ORANGE, accent=YELLOW)
    item(c, 'box', ax + 20, 93, CARD)
    item(c, 'boot', bx + 2, 93, RED)
    item(c, 'tophat', bx + 12, 93, SNOW, accent=BLUE)
    item(c, 'glasses', bx + 22, 93, BLUE)

    # --- floor things: a basket of lost balls (left), an umbrella stand (right) -------------------------------
    # basket
    bx0, by0 = 8, 114
    ball(c, bx0 + 5, by0 + 1, 3.5, PINK, with_tag=False)
    ball(c, bx0 + 12, by0, 4, GREEN, stripe='#ffffff', with_tag=False)
    ball(c, bx0 + 18, by0 + 1, 3, BLUE, with_tag=False)
    c.polygon([(bx0, by0), (bx0 + 22, by0), (bx0 + 20, by0 + 11), (bx0 + 2, by0 + 11)], '#edab50')
    for y in range(by0 + 1, by0 + 11, 2):
        for x in range(bx0, bx0 + 23):
            if c.get(x, y) == '#edab50' and (x + y // 2) % 3 == 0:
                c.set(x, y, '#bf6f4a')
    c.rect(bx0 - 1, by0, 24, 2, '#ffc825')
    c.rect(bx0 - 1, by0 + 1, 24, 1, '#bf6f4a')
    darken(c, bx0 + 14, by0 + 2, 8, 9, 1.0, mask=lambda x, y, col: col in ('#edab50', '#bf6f4a'))
    c.rect(bx0 + 2, by0 + 11, 19, 1, WOOD_DD)
    tag(c, bx0 + 19, by0 + 2)
    # umbrella stand
    sx0, sy0 = 214, 116
    for (ux, h, ramp) in [(216, 12, BLUE), (222, 15, RED), (228, 11, GREEN)]:
        top = sy0 - h
        l, m, d = ramp
        # a curly wooden handle, a short silver shaft, then the folded canopy (widest at the top)
        c.blit(['.hhh.', 'h...H', 'h...H', '.h..H'], {'h': '#391f21', 'H': '#391f21'}, ux - 4, top - 4)
        c.set(ux - 2, top - 4, '#8a4836')
        c.line(ux, top, ux, top + 1, '#c7cfdd')
        c.polygon([(ux - 1, top + 2), (ux + 2, top + 2), (ux + 3.5, top + 6), (ux + 2.5, sy0 + 2),
                   (ux - 2.5, sy0 + 2), (ux - 3.5, top + 6)], m)
        c.line(ux - 2, top + 5, ux - 2, sy0 + 1, l)
        c.line(ux + 2, top + 5, ux + 2, sy0 + 1, d)
        c.line(ux, top + 4, ux, sy0 + 1, d)
        c.set(ux, top + 2, l)
        c.line(ux - 2, top + 8, ux + 2, top + 8, '#ffffff')
    tag(c, 223, sy0 - 13)
    c.rect(sx0, sy0, 16, 14, '#424c6e')
    c.rect(sx0, sy0, 16, 2, '#92a1b9')
    c.rect(sx0 + 1, sy0 + 1, 14, 1, '#c7cfdd')
    c.line(sx0 + 2, sy0 + 3, sx0 + 2, sy0 + 12, '#657392')
    c.rect(sx0 + 12, sy0 + 2, 4, 12, '#2a2f4e')
    c.rect(sx0, sy0 + 7, 16, 1, '#ffc825')
    c.rect(sx0 - 1, sy0 + 14, 18, 1, WOOD_DD)

    # --- light: the lamp's warm glow, the window's soft light, darker corners -----------------------------------
    vignette(c, 1.0, inner=0.62, cy=58, mask=lambda x, y, col: y >= 107 or (82 < x < 158) or y < 4)
    check(c)
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    c = build()
    with Studio() as s:
        print(s.image(c, 'bg_lost_things_office_any', OUT / 'bg_lost_things_office_any.png', 1920, 1080))
