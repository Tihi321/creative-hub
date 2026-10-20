"""Light and shade for the indoor backgrounds: hue-shifted Endesga 64 ramps, dithered glows and vignettes, sparkles."""
import math

from common import Canvas

BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

E64 = {
    '#ff0040', '#131313', '#1b1b1b', '#272727', '#3d3d3d', '#5d5d5d', '#858585', '#b4b4b4', '#ffffff', '#c7cfdd',
    '#92a1b9', '#657392', '#424c6e', '#2a2f4e', '#1a1932', '#0e071b', '#1c121c', '#391f21', '#5d2c28', '#8a4836',
    '#bf6f4a', '#e69c69', '#f6ca9f', '#f9e6cf', '#edab50', '#e07438', '#c64524', '#8e251d', '#ff5000', '#ed7614',
    '#ffa214', '#ffc825', '#ffeb57', '#d3fc7e', '#99e65f', '#5ac54f', '#33984b', '#1e6f50', '#134c4c', '#0c2e44',
    '#00396d', '#0069aa', '#0098dc', '#00cdf9', '#0cf1ff', '#94fdff', '#fdd2ed', '#f389f5', '#db3ffd', '#7a09fa',
    '#3003d9', '#0c0293', '#03193f', '#3b1443', '#622461', '#93388f', '#ca52c9', '#c85086', '#f68187', '#f5555d',
    '#ea323c', '#c42430', '#891e2b', '#571c27',
}

# one step darker, shifted cooler / purpler
DARKER = {
    '#ffffff': '#c7cfdd', '#c7cfdd': '#92a1b9', '#92a1b9': '#657392', '#657392': '#424c6e', '#424c6e': '#2a2f4e',
    '#2a2f4e': '#1a1932', '#1a1932': '#0e071b',
    '#f9e6cf': '#f6ca9f', '#f6ca9f': '#e69c69', '#e69c69': '#bf6f4a', '#bf6f4a': '#8a4836', '#8a4836': '#5d2c28',
    '#5d2c28': '#391f21', '#391f21': '#1c121c', '#1c121c': '#0e071b',
    '#ffeb57': '#ffc825', '#ffc825': '#edab50', '#edab50': '#bf6f4a', '#ffa214': '#ed7614', '#ed7614': '#c64524',
    '#e07438': '#c64524', '#c64524': '#8e251d', '#8e251d': '#571c27', '#ff5000': '#c64524',
    '#d3fc7e': '#99e65f', '#99e65f': '#5ac54f', '#5ac54f': '#33984b', '#33984b': '#1e6f50', '#1e6f50': '#134c4c',
    '#134c4c': '#0c2e44', '#0c2e44': '#03193f',
    '#94fdff': '#00cdf9', '#0cf1ff': '#00cdf9', '#00cdf9': '#0098dc', '#0098dc': '#0069aa', '#0069aa': '#00396d',
    '#00396d': '#03193f',
    '#fdd2ed': '#f389f5', '#f389f5': '#ca52c9', '#db3ffd': '#93388f', '#ca52c9': '#93388f', '#93388f': '#622461',
    '#622461': '#3b1443', '#3b1443': '#0e071b',
    '#f68187': '#c85086', '#c85086': '#93388f', '#f5555d': '#ea323c', '#ea323c': '#c42430', '#c42430': '#891e2b',
    '#891e2b': '#571c27', '#571c27': '#3b1443', '#ff0040': '#c42430',
}

# one step lighter, shifted warmer
LIGHTER = {
    '#0e071b': '#1c121c', '#1c121c': '#391f21', '#391f21': '#5d2c28', '#5d2c28': '#8a4836', '#8a4836': '#bf6f4a',
    '#bf6f4a': '#e69c69', '#e69c69': '#f6ca9f', '#f6ca9f': '#f9e6cf', '#f9e6cf': '#ffffff',
    '#edab50': '#ffc825', '#ffc825': '#ffeb57', '#ffeb57': '#f9e6cf', '#ffa214': '#ffc825', '#ed7614': '#ffa214',
    '#e07438': '#ffa214', '#c64524': '#e07438', '#8e251d': '#c64524',
    '#0c2e44': '#134c4c', '#134c4c': '#1e6f50', '#1e6f50': '#33984b', '#33984b': '#5ac54f', '#5ac54f': '#99e65f',
    '#99e65f': '#d3fc7e', '#d3fc7e': '#ffffff',
    '#03193f': '#00396d', '#00396d': '#0069aa', '#0069aa': '#0098dc', '#0098dc': '#00cdf9', '#00cdf9': '#94fdff',
    '#0cf1ff': '#94fdff', '#94fdff': '#ffffff',
    '#1a1932': '#2a2f4e', '#2a2f4e': '#424c6e', '#424c6e': '#657392', '#657392': '#92a1b9', '#92a1b9': '#c7cfdd',
    '#c7cfdd': '#ffffff',
    '#571c27': '#891e2b', '#891e2b': '#c42430', '#c42430': '#ea323c', '#ea323c': '#f5555d', '#f5555d': '#f68187',
    '#f68187': '#fdd2ed', '#c85086': '#f68187',
    '#3b1443': '#622461', '#622461': '#93388f', '#93388f': '#ca52c9', '#ca52c9': '#f389f5', '#db3ffd': '#f389f5',
    '#f389f5': '#fdd2ed', '#fdd2ed': '#ffffff',
}


def check(c: Canvas):
    bad = [x for x in c.colors() if x not in E64]
    if bad:
        raise ValueError(f'colours outside Endesga 64: {bad}')


def _shift(col, steps, table):
    for _ in range(steps):
        col = table.get(col, col)
    return col


def glow(c: Canvas, cx, cy, rx, ry, strength=1.5, lighten=True, region=None, mask=None, power=1.0):
    """Dithered radial light (or shade): each pixel steps `level` times along LIGHTER (or DARKER); the
    fractional step is ordered-dithered, so the falloff reads as soft bands."""
    table = LIGHTER if lighten else DARKER
    x0, y0, w, h = region or (0, 0, c.w, c.h)
    for y in range(max(0, y0), min(c.h, y0 + h)):
        for x in range(max(0, x0), min(c.w, x0 + w)):
            col = c.px[y][x]
            if col is None or (mask and not mask(x, y, col)):
                continue
            d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
            if d >= 1:
                continue
            level = strength * (1 - d) ** power
            n = int(level)
            if level - n > (BAYER4[y % 4][x % 4] + 0.5) / 16:
                n += 1
            if n:
                c.px[y][x] = _shift(col, n, table)


def vignette(c: Canvas, strength=1.2, inner=0.55, cx=None, cy=None, mask=None):
    """Darken towards the edges (outside an inner ellipse), dithered."""
    cx = c.w / 2 if cx is None else cx
    cy = c.h / 2 if cy is None else cy
    for y in range(c.h):
        for x in range(c.w):
            col = c.px[y][x]
            if col is None or (mask and not mask(x, y, col)):
                continue
            d = math.hypot((x + 0.5 - cx) / (c.w / 2), (y + 0.5 - cy) / (c.h / 2))
            if d <= inner:
                continue
            level = strength * min(1.0, (d - inner) / (1.25 - inner))
            n = int(level)
            if level - n > (BAYER4[y % 4][x % 4] + 0.5) / 16:
                n += 1
            if n:
                c.px[y][x] = _shift(col, n, DARKER)


def darken(c: Canvas, x, y, w, h, level=1.0, mask=None):
    """Flat dithered shade over a rectangle (level 0..n steps)."""
    for yy in range(max(0, y), min(c.h, y + h)):
        for xx in range(max(0, x), min(c.w, x + w)):
            col = c.px[yy][xx]
            if col is None or (mask and not mask(xx, yy, col)):
                continue
            n = int(level)
            if level - n > (BAYER4[yy % 4][xx % 4] + 0.5) / 16:
                n += 1
            if n:
                c.px[yy][xx] = _shift(col, n, DARKER)


def lighten(c: Canvas, x, y, w, h, level=1.0, mask=None):
    for yy in range(max(0, y), min(c.h, y + h)):
        for xx in range(max(0, x), min(c.w, x + w)):
            col = c.px[yy][xx]
            if col is None or (mask and not mask(xx, yy, col)):
                continue
            n = int(level)
            if level - n > (BAYER4[yy % 4][xx % 4] + 0.5) / 16:
                n += 1
            if n:
                c.px[yy][xx] = _shift(col, n, LIGHTER)


def sparkle(c: Canvas, x, y, size=1, core='#ffffff', arm='#ffeb57'):
    """A four-point twinkle: size 0 is one pixel, 1 a plus, 2 a long-armed star."""
    c.set(x, y, core)
    if size >= 1:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            c.set(x + dx, y + dy, arm if size >= 2 else core)
    if size >= 2:
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            c.set(x + dx, y + dy, arm)
    if size >= 3:
        for dx, dy in [(3, 0), (-3, 0), (0, 3), (0, -3)]:
            c.set(x + dx, y + dy, arm)
