"""cover: the main menu picture (240x135 -> 1920x1080). Petra, Mango and a peeking Grumble in Dragon Land, the soother flying
over the sky. The left ~45 columns stay calm for the menu buttons."""
import math

from common import Canvas, Studio, OUT, OUTLINE
import sprite_grumble
import sprite_mango
import sprite_petra


def soother(c: Canvas, x: int, y: int):
    """Pip's round blue soother, seen from the front, about 11 px wide."""
    c.blit([
        '...kkkkk...',
        '..kbbbbbk..',
        '.kbBBBBBbk.',
        'kbBBwBBBBbk',
        'kbBBBttBBbk',
        'kbBBtTTtBbk',
        'kbBBBttBBbk',
        '.kbBBBBBbk.',
        '..kbbbbbk..',
        '...kkkkk...',
    ], {'k': OUTLINE, 'b': '#0069aa', 'B': '#0098dc', 'w': '#ffffff', 't': '#f6ca9f', 'T': '#e69c69'}, x, y)


def build() -> Canvas:
    c = Canvas(240, 135)
    # green Dragon Land sky
    c.vgradient(0, 100, ['#5ac54f', '#99e65f', '#d3fc7e', '#f9e6cf'])
    for (x, y, s) in [(52, 18, 0.9), (150, 30, 0.7), (200, 10, 1.0)]:
        w = int(34 * s)
        c.ellipse(x, y + int(4 * s), w, int(10 * s), '#c7cfdd')
        c.ellipse(x, y + int(2 * s), w, int(9 * s), '#ffffff')
        c.ellipse(x + int(6 * s), y - int(3 * s), int(14 * s), int(10 * s), '#ffffff')
        c.ellipse(x + int(16 * s), y - int(5 * s), int(12 * s), int(11 * s), '#ffffff')
    # the bubble-gum volcano far away, with pink and blue gum
    vx = -46  # the volcano sits far left, behind the menu side
    c.polygon([(58 + vx, 92), (78 + vx, 58), (90 + vx, 58), (112 + vx, 92)], '#bf6f4a')
    c.polygon([(84 + vx, 58), (90 + vx, 58), (112 + vx, 92), (96 + vx, 92)], '#8a4836')
    c.polygon([(76 + vx, 62), (80 + vx, 56), (88 + vx, 56), (92 + vx, 62), (88 + vx, 66), (84 + vx, 62), (80 + vx, 68)], '#f389f5')
    for (bx, by, r, col) in [(38, 50, 4, '#f389f5'), (32, 44, 3, '#00cdf9'), (44, 40, 3, '#fdd2ed'), (36, 34, 2, '#94fdff')]:
        c.circle(bx, by, r, col)
        c.set(bx - r // 2, by - r // 2, '#ffffff')
    # rolling hills
    c.hills(0, 240, 0, lambda x: 88 + 6 * math.sin(x / 19 + 1) + 3 * math.sin(x / 7), '#33984b')
    c.hills(0, 240, 0, lambda x: 100 + 5 * math.sin(x / 27 + 2), '#5ac54f')
    c.vgradient(108, 135, ['#99e65f', '#5ac54f'])
    for y in range(106, 109):
        for x in range(240):
            if (x * 5 + y * 3) % 4 < 2 and c.get(x, y) == '#5ac54f':
                c.set(x, y, '#99e65f')
    for i, col in enumerate(['#ffeb57', '#f5555d', '#ffffff', '#f389f5', '#00cdf9']):
        c.speckle(0, 112, 240, 23, col, 0.012, seed=40 + i)
    # the soother sailing over the sky, with a swoosh behind it
    for i in range(0, 40, 2):
        x = 239 - i * 1.4
        y = 26 - 16 * math.sin(i / 52 * math.pi)
        c.set(round(x), round(y), '#ffffff')
        if i % 4 == 0:
            c.set(round(x), round(y) + 1, '#ffffff')
    soother(c, 168, 2)
    for (sx, sy) in [(165, 3), (181, 6), (167, 14)]:
        c.set(sx, sy, '#ffffff')
        c.set(sx - 1, sy, '#ffeb57')
        c.set(sx + 1, sy, '#ffeb57')
        c.set(sx, sy - 1, '#ffeb57')
        c.set(sx, sy + 1, '#ffeb57')
    # the characters, at the same pixel density as in the game
    c.paste(sprite_grumble.build('happy'), 170, 14)
    c.paste(sprite_petra.build('happy'), 110, 15)
    c.paste(sprite_mango.build('happy'), 46, -4)
    return c


if __name__ == '__main__':
    with Studio() as s:
        print(s.image(build(), 'cover', OUT / 'cover.png', 1920, 1080))
