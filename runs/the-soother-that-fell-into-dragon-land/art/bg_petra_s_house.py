"""bg_petra_s_house_morning and bg_petra_s_house_evening: the cottage garden (240x135, Endesga 64)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from pxcanvas import Canvas, Studio  # noqa: E402

OUT = Path(__file__).resolve().parent / 'out'


def build(evening: bool) -> Canvas:
    c = Canvas(240, 135)
    # sky
    if evening:
        c.vgradient(0, 92, ['#622461', '#c85086', '#f68187', '#ffa214', '#ffc825'])
        c.circle(128, 58, 13, '#ffa214')
        c.circle(128, 58, 10, '#ffeb57')
    else:
        c.vgradient(0, 92, ['#0098dc', '#00cdf9', '#94fdff'])
        c.circle(205, 18, 11, '#ffeb57')
        c.circle(205, 18, 8, '#ffffff')
    # clouds
    cl, cs = ('#fdd2ed', '#f68187') if evening else ('#ffffff', '#c7cfdd')
    for (x, y, s) in [(118, 14, 1.0), (30, 22, 0.8), (160, 40, 0.6)]:
        w = int(34 * s)
        c.ellipse(x, y + int(4 * s), w, int(10 * s), cs)
        c.ellipse(x, y + int(2 * s), w, int(9 * s), cl)
        c.ellipse(x + int(6 * s), y - int(3 * s), int(14 * s), int(10 * s), cl)
        c.ellipse(x + int(16 * s), y - int(5 * s), int(12 * s), int(11 * s), cl)
    # tall white mountains far away
    lit, shade, snow = ('#f6ca9f', '#c85086', '#fdd2ed') if evening else ('#c7cfdd', '#92a1b9', '#ffffff')
    ridge = [(-10, 74), (22, 52), (58, 70), (96, 40), (128, 64), (160, 34), (196, 60), (220, 48), (252, 70)]
    c.polygon(ridge + [(252, 92), (-10, 92)], lit)
    for i in range(1, len(ridge) - 1, 2):  # the odd points are the peaks, the even ones the valleys
        (xp, yp), (xb, yb) = ridge[i], ridge[i + 1]
        c.polygon([(xp, yp), (xb, yb), (xb, 92), (xp + (xb - xp) * 0.35, 92)], shade)
        c.polygon([(xp - 7, yp + 8), (xp, yp), (xp + 7, yp + 8), (xp + 4, yp + 6), (xp + 1, yp + 9), (xp - 3, yp + 6)], snow)
    # green hill behind the garden
    hill, hill_d = ('#33984b', '#1e6f50') if evening else ('#5ac54f', '#33984b')
    c.hills(0, 240, 0, lambda x: 84 + 5 * math.sin(x / 23) + 3 * math.sin(x / 7.0), hill)
    c.vgradient(88, 100, [hill, hill_d], mask=lambda x, y: c.get(x, y) == hill)
    # lawn
    lawn = ['#5ac54f', '#33984b'] if evening else ['#99e65f', '#5ac54f']
    c.vgradient(98, 135, lawn)
    for y in range(96, 99):
        for x in range(240):
            if (x * 7 + y * 3) % 5 < 3:
                c.set(x, y, lawn[0])
    c.speckle(0, 100, 240, 35, '#33984b' if not evening else '#1e6f50', 0.05, seed=3)
    # stone path from the door
    c.polygon([(50, 109), (60, 109), (76, 135), (36, 135)], '#c7cfdd' if not evening else '#92a1b9')
    for (x, y, w) in [(52, 112, 6), (48, 117, 8), (55, 121, 8), (45, 126, 9), (58, 129, 10)]:
        c.ellipse(x, y, w, 3, '#92a1b9' if not evening else '#657392')

    # cottage
    wall, wall_d = ('#f6ca9f', '#e69c69') if evening else ('#f9e6cf', '#f6ca9f')
    c.rect(18, 62, 72, 47, wall)
    c.rect(18, 62, 6, 47, wall_d)
    c.rect(18, 105, 72, 4, '#bf6f4a')
    # chimney
    c.rect(70, 30, 10, 26, '#8a4836')
    c.rect(68, 28, 14, 4, '#5d2c28')
    for y in range(33, 54, 4):
        c.line(71, y, 79, y, '#5d2c28')
    # roof
    c.polygon([(8, 66), (54, 28), (100, 66)], '#c64524')
    c.polygon([(8, 66), (54, 28), (30, 66)], '#e07438')
    for y in range(36, 66, 5):
        c.line(int(54 - (y - 28) * 1.2), y, int(54 + (y - 28) * 1.2), y, '#8e251d')
    c.rect(8, 65, 92, 3, '#8e251d')
    # door
    c.rect(46, 82, 16, 27, '#891e2b')
    c.rect(48, 84, 12, 25, '#ea323c')
    c.rect(48, 84, 12, 3, '#f5555d')
    c.ellipse(48, 79, 12, 8, '#891e2b')
    c.ellipse(50, 81, 8, 6, '#ea323c')
    c.set(57, 97, '#ffc825')
    c.set(57, 98, '#ffc825')
    c.rect(44, 108, 20, 2, '#c7cfdd')
    # windows with flower boxes
    glass, glow = ('#ffc825', '#ffeb57') if evening else ('#94fdff', '#ffffff')
    for wx in (26, 70):
        c.rect(wx - 1, 71, 16, 16, '#ffffff')
        c.rect(wx, 72, 14, 14, glass)
        c.line(wx + 1, 73, wx + 4, 73, glow)
        c.line(wx + 1, 74, wx + 2, 74, glow)
        c.line(wx + 7, 72, wx + 7, 85, '#ffffff')
        c.line(wx, 78, wx + 13, 78, '#ffffff')
        c.rect(wx - 1, 72, 3, 14, '#f68187')
        c.rect(wx + 12, 72, 3, 14, '#f68187')
        c.rect(wx - 2, 87, 18, 4, '#8a4836')
        c.rect(wx - 2, 90, 18, 1, '#5d2c28')
        for i, col in enumerate(['#f5555d', '#ffeb57', '#f389f5', '#ffffff', '#f5555d', '#ffeb57']):
            c.set(wx - 1 + i * 3, 86, col)
            c.set(wx + i * 3, 85, '#33984b')
    # bushes by the walls
    for (x, w) in [(4, 20), (84, 18)]:
        c.ellipse(x, 96, w, 14, '#33984b')
        c.ellipse(x + 2, 95, w - 6, 10, '#5ac54f')
        c.speckle(x, 95, w, 14, '#f389f5', 0.06, seed=x, on='#5ac54f')

    # white picket fence
    fence, fence_d = ('#fdd2ed', '#c85086') if evening else ('#ffffff', '#c7cfdd')
    c.rect(100, 99, 140, 2, fence)
    c.rect(100, 105, 140, 2, fence)
    for x in range(102, 240, 6):
        c.rect(x, 95, 3, 15, fence)
        c.set(x + 1, 94, fence)
        c.line(x + 2, 96, x + 2, 109, fence_d)

    # clothesline with baby clothes
    pole = '#8a4836'
    c.rect(132, 62, 2, 52, pole)
    c.rect(222, 62, 2, 52, pole)
    c.rect(129, 62, 8, 2, pole)
    c.rect(219, 62, 8, 2, pole)
    sag = lambda x: 64 + 6 * math.sin(math.pi * (x - 134) / 88)
    for x in range(134, 222):
        c.set(x, round(sag(x)), '#5d5d5d')
    onesie = ['..bbbb..', 'bbbbbbbb', 'bbbbbbbb', '.bbbbbb.', '..bbbb..', '..bbbb..', '..bbbb..', '..b..b..', '..b..b..']
    sock = ['bb', 'bb', 'bb', 'bbb', 'bbb']
    for i, (x, col, kind) in enumerate([(142, '#5ac54f', 'o'), (156, '#0098dc', 's'), (166, '#ffeb57', 'o'), (182, '#f389f5', 's'), (192, '#00cdf9', 'o'), (208, '#f5555d', 's')]):
        y = round(sag(x + 4)) + 1
        rows = onesie if kind == 'o' else sock
        c.blit(rows, {'b': col}, x, y)
        c.set(x + 1, y - 1, '#ffffff')
        c.set(x + (6 if kind == 'o' else 1), y - 1, '#ffffff')

    # sandbox with a little castle and a bucket
    c.rect(150, 114, 52, 13, '#5d2c28')
    c.rect(151, 115, 50, 10, '#edab50')
    c.speckle(151, 115, 50, 10, '#ffc825', 0.12, seed=9)
    c.rect(150, 114, 52, 2, '#8a4836')
    c.rect(150, 125, 52, 2, '#8a4836')
    c.blit(['h.h.h', 'hhhhh', 'hhhhh', 'hhhhh'], {'h': '#e69c69'}, 166, 109)
    c.blit(['.k.', 'rrr', 'rrr', '.r.'], {'k': '#3d3d3d', 'r': '#ea323c'}, 186, 111)

    # flowers in the lawn
    for i, col in enumerate(['#ffeb57', '#f5555d', '#ffffff', '#f389f5']):
        c.speckle(0, 112, 240, 23, col, 0.012, seed=20 + i)
    return c


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    with Studio() as s:
        for name, evening in [('bg_petra_s_house_morning', False), ('bg_petra_s_house_evening', True)]:
            c = build(evening)
            s.push(c, name)
            print(s.export(str(OUT / f'{name}.png'), 1920, 1080))
