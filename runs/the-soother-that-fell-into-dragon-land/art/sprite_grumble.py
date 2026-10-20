"""Grumble: a big sleepy dragon as tall as a house. Dusty purple scales, heavy eyelids, small cream horns, little
wings behind the shoulders, a thick tail curled in front, a friendly snaggle tooth. He holds a shiny gold coin.
Only his head, neck and upper body fit on the canvas; the canvas bottom cuts him off."""
from common import Canvas, OUTLINE, WHITE, BLUSH, MOUTH, TONGUE, SPRITE_H, run_sprite

W = 120
S_DD, S_D, S, S_L = '#3b1443', '#622461', '#93388f', '#ca52c9'
BELLY, BELLY_D = '#fdd2ed', '#c7cfdd'
WING, WING_D = '#c85086', '#622461'
HORN, HORN_D = '#f9e6cf', '#e69c69'
IRIS_D, IRIS, IRIS_L = '#ed7614', '#ffc825', '#ffeb57'
GOLD_DD, GOLD_D, GOLD, GOLD_L = '#e07438', '#edab50', '#ffc825', '#ffeb57'
BROW = S_DD


def mx(pts):
    """Mirror polygon points across the canvas centre."""
    return [(W - x, y) for (x, y) in pts]


def layer(c: Canvas, draw):
    """Draw a part on its own canvas, outline it, and lay it over the picture (so overlapping parts stay separate)."""
    t = Canvas(c.w, c.h)
    draw(t)
    t.outline(OUTLINE)
    c.paste(t)


def scales(c: Canvas, pts, color=S_D):
    """Little scale arcs: a 3-px 'u'."""
    for (x, y) in pts:
        c.set(x, y, color)
        c.set(x + 1, y + 1, color)
        c.set(x + 2, y, color)


def chain(t: Canvas, path, col, dx=0, dy=0):
    """Circles along a path of (x, y, r) points, interpolated so the tube is smooth."""
    for (a, b) in zip(path, path[1:]):
        n = max(1, int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))))
        for i in range(n + 1):
            f = i / n
            t.circle(a[0] + (b[0] - a[0]) * f + dx, a[1] + (b[1] - a[1]) * f + dy, a[2] + (b[2] - a[2]) * f, col)


def belly_plates(t: Canvas, y0, y1, step=6):
    for y in range(y0, y1, step):
        for x in range(t.w):
            if t.get(x, y) == BELLY:
                t.set(x, y, BELLY_D)


# --- parts ---------------------------------------------------------------------------------------
def wings(c: Canvas):
    pts = [(18, 76), (3, 50), (10, 52), (10, 37), (18, 48), (25, 33), (36, 62)]
    bones = [((26, 68), (4, 51)), ((26, 68), (11, 39)), ((26, 68), (25, 35))]
    for flip in (False, True):
        def w(t, flip=flip):
            p = mx(pts) if flip else pts
            t.polygon(p, WING)
            for a, b in bones:
                if flip:
                    a, b = (W - 1 - a[0], a[1]), (W - 1 - b[0], b[1])
                t.line(a[0], a[1], b[0], b[1], WING_D)
        layer(c, w)


def body(c: Canvas):
    def b(t):
        # shade first, body over it leaves a crescent on the right
        for col, dx in ((S_D, 2), (S, 0)):
            t.ellipse(10 + dx, 62, 38, 36, col)
            t.ellipse(72 + dx, 62, 38, 36, col)
            t.ellipse(26 + dx, 58, 68, 40, col)
            t.rect(10 + dx, 80, 100, 40, col)
            t.polygon([(42 + dx, 40), (78 + dx, 40), (86 + dx, 72), (34 + dx, 72)], col)
        t.rect(10, 80, 2, 40, S)
        # belly plates from the neck down
        t.polygon([(49, 44), (71, 44), (77, 72), (84, 120), (36, 120), (43, 72)], BELLY)
        t.polygon([(68, 44), (71, 44), (77, 72), (84, 120), (79, 120), (73, 72)], BELLY_D)
        belly_plates(t, 50, 120)
        scales(t, [(92, 72), (100, 78), (16, 68)])
    layer(c, b)


def tail(c: Canvas):
    path = [(126, 103, 9), (112, 109, 9), (96, 113, 8.5), (78, 115, 8), (60, 115, 7), (46, 112, 6.5), (34, 109, 5.5)]

    def tl(t):
        chain(t, path, S_D, dy=1)
        chain(t, path, S)
        # spade tip pointing left
        t.polygon([(32, 105), (21, 100), (6, 108), (21, 117), (32, 113)], S)
        t.polygon([(6, 108), (21, 117), (32, 113), (30, 110), (20, 112)], S_D)
        t.line(9, 107, 20, 102, S_L)
        # light ridge along the top
        for x in range(30, 116):
            for y in range(90, 120):
                if t.get(x, y) == S:
                    t.set(x, y + 1, S_L)
                    break
        scales(t, [(98, 114), (82, 116), (64, 116), (48, 113)])
    layer(c, tl)


ARM = [(22, 76, 11), (26, 85, 10), (32, 92, 9), (40, 96, 8)]


def arms(c: Canvas):
    for flip in (False, True):
        def a(t, flip=flip):
            path = [(W - x, y, r) for (x, y, r) in ARM] if flip else ARM
            chain(t, path, S_D, dx=1, dy=1)
            chain(t, path, S)
            if flip:
                scales(t, [(94, 82), (88, 89)])
            else:
                t.line(13, 75, 17, 69, S_L)
                t.line(18, 68, 21, 66, S_L)
                scales(t, [(22, 82), (28, 89)])
        layer(c, a)


def coin(c: Canvas):
    def co(t):
        t.circle(60, 95, 9, GOLD_DD)
        t.circle(59.5, 94.5, 8, GOLD_D)
        t.circle(59, 94, 7, GOLD)
        t.ellipse(53, 88, 7, 7, GOLD_L)
        # an embossed star in the middle
        t.blit(['..d..', '.ddd.', 'ddddd', '.ddd.', '.d.d.'], {'d': GOLD_D}, 57, 92)
    layer(c, co)
    for (x, y) in [(66, 87), (66, 86), (66, 88), (65, 87), (67, 87), (55, 90)]:
        c.set(x, y, WHITE)


def hands(c: Canvas):
    for flip in (False, True):
        def h(t, flip=flip):
            x0 = 36 if not flip else W - 36 - 18
            t.ellipse(x0, 90, 18, 15, S)
            t.ellipse(x0 + 2, 90, 14, 3, S_L)
            for fx in (6, 11):
                xx = x0 + fx if not flip else x0 + 17 - fx
                t.line(xx, 99, xx, 103, S_D)
            for fx in (2, 7, 12):
                xx = x0 + fx if not flip else x0 + 17 - fx - 3
                t.polygon([(xx, 103), (xx + 4, 103), (xx + 2, 108)], HORN)
                t.set(xx + 3 if not flip else xx, 104, HORN_D)
        layer(c, h)


def head(c: Canvas):
    def hd(t):
        horn = [(35, 13), (45, 9), (32, 0)]
        for pts in (horn, mx(horn)):
            t.polygon(pts, HORN)
        t.line(36, 9, 34, 3, HORN_D)
        t.line(84, 9, 86, 3, HORN_D)
        t.line(38, 11, 42, 9, HORN_D)
        t.line(81, 11, 77, 9, HORN_D)
        # crest spikes
        side = [(47, 8), (50, 3), (54, 7)]
        for pts in ([(55, 7), (60, 0), (65, 7)], side, mx(side)):
            t.polygon(pts, S_L)
        # fin ears
        ear = [(28, 20), (13, 14), (19, 22), (13, 28), (28, 30)]
        for pts in (ear, mx(ear)):
            t.polygon(pts, S)
        t.line(16, 16, 24, 21, S_D)
        t.line(16, 27, 24, 27, S_D)
        t.line(103, 16, 95, 21, S_D)
        t.line(103, 27, 95, 27, S_D)
        # skull and jowly cheeks: shade, then base
        t.ellipse(29, 5, 64, 42, S_D)
        t.ellipse(23, 19, 76, 32, S_D)
        t.ellipse(28, 4, 63, 41, S)
        t.ellipse(22, 18, 75, 30, S)
        # muzzle
        t.ellipse(41, 32, 39, 21, BELLY_D)
        t.ellipse(40, 31, 39, 20, BELLY)
        # highlights and scales
        t.line(34, 14, 42, 8, S_L)
        t.line(44, 7, 50, 6, S_L)
        t.set(32, 17, S_L)
        t.set(33, 16, S_L)
        scales(t, [(52, 9), (60, 7), (68, 9), (56, 13), (64, 13), (27, 36), (90, 36), (31, 41), (86, 41)])
        # round nostrils
        for nx in (51, 65):
            t.blit(['.dd.', 'dDDd', '.dd.'], {'d': S_D, 'D': S_DD}, nx, 35)
    layer(c, hd)


# --- face ----------------------------------------------------------------------------------------
EYE = ['....kkkk....',
       '..kkiiiikk..',
       '.kiiiiiiiik.',
       'kiiiiiiiiiik',
       'kiiiiiiiiiik',
       'kiiiiiiiiiik',
       'kiiiiiiiiiik',
       'kiiiiiiiiiik',
       '.kiiiiiiiik.',
       '..kkiiiikk..',
       '....kkkk....']
EW, EH = 12, 11
LX, RX, EY = 35, W - 35 - 12, 16


def eye(c: Canvas, x, y, lid=None, low=None, look=(0, 0), lash=0):
    """A 12x11 dragon eye: white, big gold iris, round pupil. lid / low: per column the row of the upper / lower
    lid edge (rows above lid are eyelid, rows below low are cheek)."""
    cx, cy = 6 + look[0], 5.5 + look[1]
    for r in range(EH):
        for i in range(EW):
            ch = EYE[r][i]
            if ch == '.':
                continue
            if ch == 'k':
                col = OUTLINE
            else:
                px, py = i + 0.5 - cx, r + 0.5 - cy
                d = (px * px + py * py) ** 0.5
                col = WHITE
                if d <= 3.9:
                    col = IRIS_D if py < -2 else (IRIS_L if py > 2.2 else IRIS)
                if abs(px) <= 1 and abs(py) <= 1.6:
                    col = OUTLINE
                hx, hy = int(cx) - 3, int(cy) - 2
                if (i, r) in ((hx, hy), (hx + 1, hy), (hx, hy + 1), (hx + 1, hy + 1)):
                    col = WHITE
                if (i, r) == (int(cx) + 2, int(cy) + 2):
                    col = WHITE
            if lid is not None and r < lid[i]:
                col = S_D if ch == 'k' else S
            elif lid is not None and r == lid[i]:
                col = OUTLINE
            if low is not None and r > low[i]:
                col = S
            elif low is not None and r == low[i]:
                col = OUTLINE
            c.set(x + i, y + r, col)
    if lash and lid is not None:
        if lash < 0:
            c.set(x - 1, y + lid[0], OUTLINE)
            c.set(x - 2, y + lid[0] - 1, OUTLINE)
        else:
            c.set(x + EW, y + lid[-1], OUTLINE)
            c.set(x + EW + 1, y + lid[-1] - 1, OUTLINE)


def brow(c: Canvas, x, y, dys, thick=2):
    for i, d in enumerate(dys):
        for k in range(thick):
            c.set(x + i, y + d + k, BROW)


def outlined_px(c: Canvas, pts, color, line=OUTLINE):
    s = set(pts)
    for (x, y) in pts:
        c.set(x, y, color)
    for (x, y) in pts:
        for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + ddx, y + ddy)
            if p not in s and c.get(*p) != OUTLINE:
                c.set(p[0], p[1], line)


def tooth(c: Canvas, x, y):
    """The snaggle tooth hanging from the upper lip; (x, y) is its top-left pixel."""
    outlined_px(c, [(x, y), (x + 1, y), (x + 1, y + 1)], WHITE)


def blush(c: Canvas):
    for (x, y) in [(27, 30), (28, 30), (29, 30), (30, 30), (31, 30), (28, 31), (29, 31), (30, 31)]:
        c.set(x, y, BLUSH)
        c.set(W - 1 - x, y, BLUSH)


BY = 12  # brow row


def face(c: Canvas, expr: str):
    k = OUTLINE
    if expr == 'neutral':
        sleepy = [5] * EW
        eye(c, LX, EY, lid=sleepy, look=(0, 1), lash=-1)
        eye(c, RX, EY, lid=sleepy, look=(0, 1), lash=1)
        b = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        brow(c, LX - 1, BY, b)
        brow(c, RX - 1, BY, b)
        c.blit(['k....................k',
                '.kk................kk.',
                '...kkkkkkkkkkkkkkkk...'], {'k': k}, 49, 43)
        tooth(c, 64, 46)
    elif expr == 'thinking':
        # one eye open and looking up to the side, the other squinting
        eye(c, LX, EY, lid=[3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3], look=(1, -1), lash=-1)
        eye(c, RX, EY, lid=[6] * EW, look=(1, 0), lash=1)
        brow(c, LX - 1, BY, [1, 0, -1, -2, -2, -3, -3, -3, -3, -2, -2, -1, 0, 1])
        brow(c, RX - 1, BY, [3] * 14)
        # mouth pushed to the side
        c.blit(['...............kk',
                '...........kkkk..',
                'kkkkkkkkkkk......'], {'k': k}, 53, 43)
        tooth(c, 66, 45)
    elif expr == 'sad':
        droop = [8, 8, 7, 7, 6, 6, 5, 5, 4, 4, 4, 4]
        eye(c, LX, EY, lid=droop, look=(0, 1), lash=-1)
        eye(c, RX, EY, lid=droop[::-1], look=(0, 1), lash=1)
        b = [4, 4, 3, 3, 2, 2, 1, 1, 0, 0, -1, -1, -2, -2]
        brow(c, LX - 1, BY, b)
        brow(c, RX - 1, BY, b[::-1])
        c.blit(['....kkkkkkkk....',
                '..kk........kk..',
                '.k............k.'], {'k': k}, 52, 44)
        tooth(c, 63, 45)
    elif expr == 'happy':
        curve = [9, 8, 8, 7, 7, 7, 7, 7, 7, 8, 8, 9]
        eye(c, LX, EY, low=curve, look=(0, -1))
        eye(c, RX, EY, low=curve, look=(0, -1))
        b = [2, 1, 0, -1, -1, -2, -2, -2, -2, -1, -1, 0, 1, 2]
        brow(c, LX - 1, BY, b)
        brow(c, RX - 1, BY, b)
        c.blit(['kk......................kk',
                '.kkkkkkkkkkkkkkkkkkkkkkkk.',
                '..kmmmmmmmmmmmmmmmmmmmmk..',
                '...kmmmmmmmmmmmmmmmmmmk...',
                '....kmmmmmtttttttmmmmk....',
                '.....kkmmtttttttttmkk.....',
                '.......kkkkkkkkkkkk.......'], {'k': k, 'm': MOUTH, 't': TONGUE}, 47, 42)
        for (x, y) in [(64, 44), (65, 44), (65, 45)]:
            c.set(x, y, WHITE)
        blush(c)


def build(expr: str) -> Canvas:
    c = Canvas(W, SPRITE_H)
    wings(c)
    body(c)
    tail(c)
    arms(c)
    hands(c)
    coin(c)
    head(c)
    face(c, expr)
    c.outline(OUTLINE)
    return c


EXPRESSIONS = ['neutral', 'thinking', 'sad', 'happy']

if __name__ == '__main__':
    run_sprite('grumble', build, EXPRESSIONS)
