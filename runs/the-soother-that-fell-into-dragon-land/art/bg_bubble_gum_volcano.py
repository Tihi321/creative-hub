"""bg_bubble_gum_volcano_any: Dragon Land by the bubble-gum volcano, where Petra lands (240x135, Endesga 64)."""
import math

from common import Canvas, Studio, OUT
from dl_parts import (shade_cone, sky, cloud, ball, ring_bubble, gum_tree, gumdrop, tuft, pillow, check,
                      PINK, MINT, LEMON, ORANGE, GRAPE, CHERRY, GUM_PINK, GUM_BLUE,
                      GROUND_L, GROUND, GROUND_D, MOSS_L, MOSS, MOSS_D)

NAME = 'bg_bubble_gum_volcano_any'

# volcano: caramel rock, lit from the left
V_HI, V_LIT, V_MID, V_SH, V_DEEP = '#f6ca9f', '#e69c69', '#bf6f4a', '#8a4836', '#5d2c28'
VCX, VTOP, VBASE, V_RIM, V_FOOT = 184, 32, 106, 17, 72


def half(y):
    t = max(0.0, (y - VTOP) / (VBASE - VTOP))
    return V_RIM + 6 * math.sqrt(t) + (V_FOOT - V_RIM - 6) * t ** 1.5


def ground_top(x):
    return 99 + 1.4 * math.sin(x / 11.0 + 0.6) + 0.9 * math.sin(x / 4.7)


def volcano(c: Canvas):
    shade_cone(c, VCX, VTOP, VBASE, half, (V_MID, V_LIT, V_MID, V_SH, V_DEEP))
    # soft gullies running down from the crater give the cone its round form
    darker = {V_LIT: V_MID, V_MID: V_SH, V_SH: V_DEEP, V_DEEP: V_DEEP}
    lighter = {V_LIT: V_HI, V_MID: V_LIT, V_SH: V_MID, V_DEEP: V_SH}
    for (k, y0, y1) in [(-0.55, VTOP + 14, VBASE - 4), (-0.12, VTOP + 30, VBASE - 2), (0.42, VTOP + 22, VBASE - 6)]:
        for y in range(y0, y1):
            x = round(VCX + k * half(y))
            col = c.get(x, y)
            if col in darker:
                c.set(x, y, darker[col])
                if c.get(x - 1, y) in lighter and (y - y0) % 2 == 0:
                    c.set(x - 1, y, lighter[c.get(x - 1, y)])
    # the crater lip and the dark mouth
    c.ellipse(VCX - V_RIM - 1, VTOP - 5, 2 * V_RIM + 2, 10, V_HI)
    c.ellipse(VCX - V_RIM + 2, VTOP - 4, 2 * V_RIM - 4, 7, V_DEEP)


def gum_ramp(x):
    return GUM_PINK if x < VCX else GUM_BLUE


def gum_back(c: Canvas):
    """The back half of the gum ring on the lip and the pool in the mouth."""
    for x in range(VCX - V_RIM - 1, VCX + V_RIM + 1):
        dark, base, light, hi = gum_ramp(x)
        for y in range(VTOP - 5, VTOP):
            if c.get(x, y) == V_HI:
                c.set(x, y, light if c.get(x, y - 1) != V_HI else base)
    c.ellipse(VCX - V_RIM + 4, VTOP - 2, 2 * V_RIM - 8, 3, GUM_PINK[0])


DRIPS = [(-15, 9, 2.6), (-9, 19, 3.0), (-3, 8, 2.4), (3, 6, 2.2), (8, 15, 3.0), (14, 22, 2.8), (19, 8, 2.2)]


def gum_front(c: Canvas):
    """The front of the gum ring spilling over the lip like icing: drips with round ends, lit left, shaded right."""
    def length(x):
        px = x + 0.5 - VCX
        best = 4.0 + 0.8 * math.sin(x * 0.7)
        for (dx, ln, w) in DRIPS:
            d = abs(px - dx)
            if d < w:
                best = max(best, ln - w + math.sqrt(w * w - d * d))
            elif d < w + 1.6:   # a soft fillet where the drip meets the cap
                best = max(best, 4.0 + (w + 1.6 - d) * 1.2)
        return best

    L = {x: length(x) for x in range(VCX - 30, VCX + 31)}
    for x in range(VCX - 30, VCX + 30):
        dark, base, light, hi = gum_ramp(x)
        dx = (x + 0.5 - VCX) / (V_RIM + 1)
        top = VTOP - 1 + 2.6 * math.sqrt(max(0.0, 1 - dx * dx)) if abs(dx) < 1 else VTOP + 1
        bot = VTOP + L[x]
        for y in range(round(top) - 1, round(bot) + 1):
            hx = half(y) + 0.4
            if abs(x + 0.5 - VCX) > hx:
                continue
            col = base
            if y <= top + 0.5:
                col = light
            elif y >= round(bot) or VTOP + L[x + 1] < y or x + 0.5 - VCX > hx - 1.5:
                col = dark
            elif VTOP + L[x - 1] < y or x + 0.5 - VCX < -hx + 1.5:
                col = light
            c.set(x, y, col)
    # a shine near the end of each long drip
    for (dx, ln, w) in DRIPS:
        if ln > 10:
            x = round(VCX + dx - w * 0.35)
            c.set(x, VTOP + ln - 3, gum_ramp(x)[3])
            c.set(x, VTOP + ln - 4, gum_ramp(x)[2])

    # a few gum splats further down the slope
    for (x, y, ramp) in [(160, 74, GUM_PINK), (204, 60, GUM_BLUE), (150, 96, GUM_BLUE), (214, 94, GUM_PINK)]:
        dark, base, light, hi = ramp
        c.ellipse(x, y, 6, 3, dark)
        c.ellipse(x, y - 1, 6, 3, base)
        c.set(x + 1, y - 1, light)
        c.set(x + 2, y - 1, light)


def gum_bubbles(c: Canvas):
    # bubbles rising out of the crater, the biggest still sitting in the mouth
    ball(c, VCX - 4, VTOP - 10, 10, GUM_PINK)
    ball(c, VCX + 10, VTOP - 15, 7, GUM_BLUE)
    ball(c, VCX + 1, VTOP - 29, 4.5, GUM_PINK)
    ball(c, VCX - 17, VTOP - 24, 3.5, GUM_BLUE)
    ball(c, VCX + 21, VTOP - 30, 2.8, GUM_PINK)
    # a blue bubble that just popped: a starburst with flying bits
    px, py = VCX + 22, VTOP - 13
    for (dx, dy) in [(0, -4), (3, -3), (4, 0), (3, 3), (0, 4), (-3, 3), (-4, 0), (-3, -3)]:
        c.line(px + dx // 2, py + dy // 2, px + dx, py + dy, '#ffffff')
    c.rect(px - 1, py - 1, 3, 3, GUM_BLUE[1])
    c.set(px - 1, py - 1, GUM_BLUE[2])
    for (dx, dy, col) in [(-7, -2, GUM_BLUE[1]), (6, -6, GUM_BLUE[1]), (7, 4, GUM_BLUE[2]), (-1, 7, GUM_BLUE[1])]:
        c.rect(px + dx, py + dy, 2, 2, col)
    # a pink pop on the other side
    px, py = VCX - 22, VTOP - 9
    for (dx, dy) in [(0, -3), (3, 0), (0, 3), (-3, 0), (2, -2), (2, 2), (-2, 2), (-2, -2)]:
        c.set(px + dx, py + dy, '#ffffff')
    c.set(px, py, GUM_PINK[1])
    for (dx, dy) in [(-5, -3), (4, -5), (-4, 4)]:
        c.rect(px + dx, py + dy, 2, 2, GUM_PINK[1])


def ground(c: Canvas):
    top = {x: round(ground_top(x)) for x in range(240)}
    for x in range(240):
        for y in range(top[x], 135):
            c.set(x, y, GROUND)
    c.vgradient(96, 107, [GROUND_L, GROUND], mask=lambda x, y: y > top[x])
    for x in range(240):  # a soft light lip along the top edge
        c.set(x, top[x], GROUND_L)
    c.vgradient(122, 135, [GROUND, GROUND_D], mask=lambda x, y: x < 64 or x > 176)
    # marshmallow pillows, bigger in front, mostly at the sides
    for (x, y, w, h) in [(2, 102, 10, 4), (40, 101, 9, 3), (196, 102, 10, 4), (224, 101, 10, 4),
                         (4, 114, 16, 6), (44, 111, 13, 5), (184, 112, 15, 5), (212, 116, 16, 6),
                         (0, 125, 24, 9), (28, 128, 20, 8), (192, 127, 22, 9), (218, 124, 22, 10)]:
        pillow(c, x, y, w, h)
    # moss patches: the green in the pink
    for (x, y, w, h) in [(22, 108, 18, 5), (58, 126, 22, 6), (170, 110, 16, 4), (124, 118, 20, 5), (206, 108, 14, 4),
                         (98, 103, 12, 2)]:
        c.ellipse(x, y + 1, w, h, MOSS_D)
        c.ellipse(x, y, w, h, MOSS)
        c.ellipse(x + 2, y, w - 4, max(1, h // 2), MOSS_L)
        for i in range(x + 1, x + w - 4, 5):
            tuft(c, i, y + 1, size=3 if h > 4 else 2)
    # mint tufts
    for (x, y) in [(5, 106), (34, 114), (54, 108), (88, 113), (140, 113), (160, 108), (184, 108), (232, 112),
                   (46, 132), (112, 124), (150, 133), (230, 134), (16, 124), (78, 133)]:
        tuft(c, x, y, size=3 if y > 112 else 2)
    # gumdrops lying about
    for (x, y, w, ramp) in [(36, 120, 5, CHERRY), (96, 110, 3, LEMON), (148, 116, 4, MINT), (204, 122, 5, GRAPE),
                            (60, 131, 6, LEMON), (178, 131, 6, CHERRY), (126, 104, 3, ORANGE), (226, 113, 4, ORANGE)]:
        gumdrop(c, x, y, w, ramp)


def build() -> Canvas:
    c = Canvas(240, 135)
    sky(c, 100)
    # fluffy clouds
    cloud(c, 8, 18, 1.15)
    cloud(c, 84, 38, 0.7, flip=True)
    cloud(c, 108, 9, 0.55)
    # far hills, rolling green
    hill = lambda x: 88 + 4 * math.sin(x / 17.0) + 2 * math.sin(x / 6.3 + 1)
    c.hills(0, 240, 0, hill, '#5ac54f')
    c.vgradient(86, 101, ['#5ac54f', '#33984b'], mask=lambda x, y: y >= hill(x) + 1)
    # tiny far gum trees on the hills
    for (x, y, ramp) in [(72, 89, PINK), (92, 91, LEMON), (116, 89, MINT), (134, 92, GRAPE)]:
        c.rect(x, y, 1, 6, '#ffffff')
        ball(c, x + 0.5, y - 1, 3, ramp)
    volcano(c)
    gum_back(c)
    gum_bubbles(c)
    gum_front(c)
    ground(c)
    # gum trees at the sides
    gum_tree(c, 60, 104, 25, 9, LEMON, stripe=('#0098dc', '#0069aa'), shadow=GROUND_D)
    gum_tree(c, 22, 113, 40, 15, PINK, shadow=GROUND_D)
    gum_tree(c, 229, 121, 44, 13, GRAPE, stripe=('#5ac54f', '#33984b'), shadow=GROUND_D)
    # bubbles drifting by
    for (x, y, size, col) in [(104, 58, 5, GUM_PINK[1]), (92, 27, 3, GUM_BLUE[1]), (150, 47, 4, GUM_BLUE[1]),
                              (128, 70, 3, GUM_PINK[1]), (60, 56, 3, GUM_BLUE[1]), (160, 19, 2, GUM_PINK[1]),
                              (122, 40, 2, GUM_BLUE[1])]:
        ring_bubble(c, x, y, size, col)
    check(c)
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    with Studio() as s:
        print(s.image(build(), NAME, OUT / f'{NAME}.png', 1920, 1080))
