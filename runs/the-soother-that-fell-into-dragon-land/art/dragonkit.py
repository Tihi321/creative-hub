"""Small drawing helpers shared by the dragon sprites: discs, tubes along curves, the grey standing stone."""
import math

from common import Canvas, SPRITE_H

ST, ST_L, ST_D, ST_DD = '#92a1b9', '#c7cfdd', '#657392', '#424c6e'
MOSS, MOSS_L, MOSS_D = '#5ac54f', '#99e65f', '#33984b'


def disc(c: Canvas, cx: float, cy: float, r: float, col: str):
    for yy in range(math.floor(cy - r) - 1, math.ceil(cy + r) + 2):
        for xx in range(math.floor(cx - r) - 1, math.ceil(cx + r) + 2):
            if (xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= r * r:
                c.set(xx, yy, col)


def bez(p0, p1, p2, n=24):
    """Points of a quadratic Bezier curve."""
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, d = (1 - t) ** 2, 2 * (1 - t) * t, t * t
        out.append((a * p0[0] + b * p1[0] + d * p2[0], a * p0[1] + b * p1[1] + d * p2[1]))
    return out


def tube(c: Canvas, pts, r0: float, r1: float, col: str, dx: float = 0, dy: float = 0):
    """Discs along a polyline, radius going from r0 to r1; dx/dy shift every disc (for shade passes)."""
    segs = list(zip(pts, pts[1:]))
    total = sum(math.dist(a, b) for a, b in segs) or 1
    done = 0.0
    for a, b in segs:
        L = math.dist(a, b)
        n = max(1, int(L * 2))
        for i in range(n + 1):
            t = i / n
            r = r0 + (r1 - r0) * ((done + L * t) / total)
            disc(c, a[0] + (b[0] - a[0]) * t + dx, a[1] + (b[1] - a[1]) * t + dy, r, col)
        done += L


def stone(c: Canvas, x: int, y: int, w: int, seed: int = 3):
    """A squat grey standing stone from row y down to the canvas bottom, x..x+w, lit from the upper left."""
    b = SPRITE_H
    c.polygon([(x + 2, y + 3), (x + 7, y), (x + w - 7, y), (x + w - 2, y + 3), (x + w, y + 10), (x + w + 1, b),
               (x - 1, b), (x, y + 10)], ST)
    # shade on the right face, light on the left and top
    c.polygon([(x + w - 9, y + 2), (x + w - 2, y + 3), (x + w, y + 10), (x + w + 1, b), (x + w - 8, b), (x + w - 7, y + 12)], ST_D)
    c.polygon([(x + 2, y + 3), (x + 7, y), (x + 12, y), (x + 6, y + 6), (x + 5, b), (x - 1, b), (x, y + 10)], ST_L)
    c.rect(x + 7, y, w - 14, 2, ST_L)
    # cracks and pebbly texture
    c.speckle(x + 1, y + 4, w - 1, b - y - 4, ST_DD, 0.025, seed=seed, on=ST_D)
    c.speckle(x + 1, y + 4, w - 1, b - y - 4, ST_D, 0.03, seed=seed + 1, on=ST)
    c.speckle(x + 1, y + 4, w - 1, b - y - 4, ST, 0.03, seed=seed + 2, on=ST_L)
    c.line(x + 14, y + 12, x + 17, y + 17, ST_DD)
    c.line(x + 17, y + 17, x + 16, y + 22, ST_DD)
    c.line(x + w - 16, b - 12, x + w - 13, b - 7, ST_DD)
    # a strip of darker ground contact and a tuft of moss at each foot
    c.rect(x - 1, b - 2, w + 2, 2, ST_D)
    for mx in (x - 1, x + w - 6):
        c.blit(['.m..m.', 'mMmmMm', 'MMMMMM'], {'m': MOSS_L, 'M': MOSS}, mx, b - 3)


def part(c: Canvas, fn, line: str):
    """Draw fn(t) on a scratch canvas and paste it with a contour line in `line`, the contour only where it falls on
    pixels already painted (inner lines); the silhouette edge is left to the final OUTLINE pass."""
    t = Canvas(c.w, c.h)
    fn(t)
    edge = Canvas(c.w, c.h)
    edge.px = [row[:] for row in t.px]
    edge.outline(line)
    for yy in range(c.h):
        for xx in range(c.w):
            if t.px[yy][xx] is None and edge.px[yy][xx] is not None and c.px[yy][xx] is not None:
                c.px[yy][xx] = edge.px[yy][xx]
    c.paste(t)
