"""Compose pixel art in code and draw it in Pixel Studio over its MCP.

A Canvas is a grid of hex colours (None = transparent) with shape helpers: rect, ellipse, polygon, line,
dithered gradients, speckles, hand-written rows (blit) and outlines. Studio.push() opens a document in
Pixel Studio and paints the canvas there as draw_grid tiles (64x64, the tool's limit); Studio.export()
writes the PNG through Pixel Studio. Standard library only.

    from pxcanvas import Canvas, Studio
    c = Canvas(240, 135)
    c.vgradient(0, 80, ['#0098dc', '#00cdf9', '#94fdff'])
    with Studio() as s:
        s.push(c, 'bg_house', palette='endesga-64')
        s.export('C:/out/bg_house.png', 1920, 1080)
"""
from __future__ import annotations

import json
import math
import os
import random
import tempfile
import time
import urllib.request
from pathlib import Path

PIXEL_STUDIO = 'http://127.0.0.1:7457/mcp'

BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-=?@^~<>/|'


def norm(c):
    if c is None:
        return None
    c = c.lower()
    if len(c) == 4:
        c = '#' + ''.join(ch * 2 for ch in c[1:])
    return c


class Canvas:
    def __init__(self, w: int, h: int, fill: str | None = None):
        self.w, self.h = w, h
        self.px = [[norm(fill)] * w for _ in range(h)]

    # --- pixels -------------------------------------------------------------------------------
    def set(self, x: int, y: int, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = norm(c)

    def get(self, x: int, y: int):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[y][x]
        return None

    def copy(self) -> 'Canvas':
        c = Canvas(self.w, self.h)
        c.px = [row[:] for row in self.px]
        return c

    # --- shapes -------------------------------------------------------------------------------
    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def ellipse(self, x, y, w, h, c):
        """Filled ellipse in the box (x, y, w, h)."""
        cx, cy = x + w / 2, y + h / 2
        rx, ry = w / 2, h / 2
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                dx, dy = (xx + 0.5 - cx) / rx, (yy + 0.5 - cy) / ry
                if dx * dx + dy * dy <= 1.0:
                    self.set(xx, yy, c)

    def circle(self, cx, cy, r, c):
        self.ellipse(round(cx - r), round(cy - r), round(2 * r), round(2 * r), c)

    def polygon(self, pts, c):
        """Filled polygon (even-odd), sampled at pixel centres."""
        ys = [p[1] for p in pts]
        for yy in range(max(0, math.floor(min(ys))), min(self.h, math.ceil(max(ys)) + 1)):
            py = yy + 0.5
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= py < y1) or (y1 <= py < y0):
                    xs.append(x0 + (py - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for xx in range(math.ceil(xs[i] - 0.5), math.floor(xs[i + 1] - 0.5) + 1):
                    self.set(xx, yy, c)

    def line(self, x0, y0, x1, y1, c, t: int = 1):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            for oy in range(t):
                for ox in range(t):
                    self.set(x0 + ox, y0 + oy, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def hills(self, x0, x1, base, fn, c, bottom=None):
        """Fill under a curve: for each x the column from fn(x) down to bottom (default canvas bottom)."""
        b = self.h if bottom is None else bottom
        for xx in range(x0, x1):
            top = round(fn(xx))
            for yy in range(max(0, top), b):
                self.set(xx, yy, c)

    # --- gradients and texture ----------------------------------------------------------------
    def vgradient(self, y0, y1, colors, x0=0, x1=None, mask=None):
        """Vertical gradient over rows y0..y1 through the colours, with 4x4 ordered dither between neighbours."""
        x1 = self.w if x1 is None else x1
        n = len(colors) - 1
        for yy in range(y0, y1):
            t = (yy - y0) / max(1, (y1 - y0 - 1)) * n
            i = min(n - 1, int(t)) if n > 0 else 0
            f = t - i
            for xx in range(x0, x1):
                if mask and not mask(xx, yy):
                    continue
                if n == 0:
                    self.set(xx, yy, colors[0])
                    continue
                thr = (BAYER4[yy % 4][xx % 4] + 0.5) / 16
                self.set(xx, yy, colors[i + 1] if f > thr else colors[i])

    def dither_fill(self, x, y, w, h, a, b, level: float):
        """Ordered dither of b over a at a level 0..1."""
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, b if level > (BAYER4[yy % 4][xx % 4] + 0.5) / 16 else a)

    def speckle(self, x, y, w, h, c, density: float, seed: int = 1, on=None):
        """Random single pixels of c over the area (only on colour `on` when given)."""
        r = random.Random(seed)
        on = norm(on) if on else None
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if r.random() < density and (on is None or self.get(xx, yy) == on):
                    self.set(xx, yy, c)

    def replace(self, a, b, region=None):
        a, b = norm(a), norm(b)
        x0, y0, w, h = region or (0, 0, self.w, self.h)
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                if self.get(xx, yy) == a:
                    self.set(xx, yy, b)

    # --- hand-drawn parts ---------------------------------------------------------------------
    def blit(self, rows, legend, x=0, y=0, flip=False):
        """Paint rows of characters; '.' and ' ' are transparent unless the legend names them."""
        for j, row in enumerate(rows):
            r = row[::-1] if flip else row
            for i, ch in enumerate(r):
                if ch in legend:
                    col = legend[ch]
                    if col is not None:
                        self.set(x + i, y + j, col)
                elif ch in '. ':
                    continue
                else:
                    raise ValueError(f'blit: {ch!r} not in legend (row {j})')

    def paste(self, other: 'Canvas', x=0, y=0):
        for j in range(other.h):
            for i in range(other.w):
                c = other.px[j][i]
                if c is not None:
                    self.set(x + i, y + j, c)

    def outline(self, c, diagonal=False):
        """1 px outline outside the opaque pixels."""
        c = norm(c)
        add = []
        for yy in range(self.h):
            for xx in range(self.w):
                if self.px[yy][xx] is not None:
                    continue
                nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if diagonal:
                    nb += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                if any(self.get(xx + dx, yy + dy) not in (None, c) for dx, dy in nb):
                    add.append((xx, yy))
        for xx, yy in add:
            self.px[yy][xx] = c

    def flip(self) -> 'Canvas':
        c = Canvas(self.w, self.h)
        c.px = [row[::-1] for row in self.px]
        return c

    def colors(self):
        return sorted({p for row in self.px for p in row if p})

    # --- tiles for draw_grid ------------------------------------------------------------------
    def tiles(self, size=64, base=None):
        """draw_grid argument dicts covering the canvas; with `base`, only the pixels that differ from it."""
        out = []
        for ty in range(0, self.h, size):
            for tx in range(0, self.w, size):
                w, h = min(size, self.w - tx), min(size, self.h - ty)
                cols = {}
                rows = []
                any_px = False
                for yy in range(ty, ty + h):
                    row = []
                    for xx in range(tx, tx + w):
                        p = self.px[yy][xx]
                        if base is not None and base.px[yy][xx] == p:
                            row.append('.')
                            continue
                        if p is None:
                            row.append('_') if base is not None else row.append('.')
                            if base is not None:
                                cols.setdefault('transparent', '_')
                                any_px = True
                            continue
                        if p not in cols:
                            if len(cols) >= len(CHARS):
                                raise ValueError('too many colours in one tile')
                            cols[p] = CHARS[len(cols)]
                        row.append(cols[p])
                        any_px = True
                    rows.append(''.join(row))
                if not any_px:
                    continue
                legend = {'.': None}
                for col, ch in cols.items():
                    legend[ch] = None if col == 'transparent' else col
                args = {'rows': rows, 'legend': legend, 'x': tx, 'y': ty}
                if base is not None and 'transparent' in cols:
                    # '_' cells must erase: clear the cells with '_' via a separate erase pass
                    args['_erase'] = True
                out.append(args)
        return out


class _FileLock:
    def __init__(self, path: Path, timeout_s: float):
        self.path, self.timeout_s = path, timeout_s

    def __enter__(self):
        end = time.time() + self.timeout_s
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                # a lock older than 10 minutes was left by a crashed script
                try:
                    if time.time() - self.path.stat().st_mtime > 600:
                        self.path.unlink(missing_ok=True)
                        continue
                except FileNotFoundError:
                    continue
                if time.time() > end:
                    raise TimeoutError(f'Pixel Studio is busy ({self.path})')
                time.sleep(0.5)

    def __exit__(self, *a):
        self.path.unlink(missing_ok=True)
        return False


class Studio:
    """A small MCP client for Pixel Studio (Streamable HTTP)."""

    def __init__(self, url: str = PIXEL_STUDIO):
        self.url = url
        self.session = None
        self._id = 0

    def __enter__(self):
        self._rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'pxcanvas', 'version': '1'}})
        self._post({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return self

    def __exit__(self, *a):
        return False

    def _post(self, body, timeout=120):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
        if self.session:
            headers['mcp-session-id'] = self.session
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=timeout) as r:
            sid = r.headers.get('mcp-session-id')
            if sid:
                self.session = sid
            text = r.read().decode('utf-8')
        if not text.strip():
            return None
        if text.lstrip().startswith('{'):
            return json.loads(text)
        data = [l[5:].strip() for l in text.splitlines() if l.startswith('data:')]
        return json.loads(data[-1]) if data else None

    def _rpc(self, method, params):
        self._id += 1
        r = self._post({'jsonrpc': '2.0', 'id': self._id, 'method': method, 'params': params})
        if r and r.get('error'):
            raise RuntimeError(f"{method}: {r['error'].get('message')}")
        return r.get('result') if r else None

    def call(self, tool: str, args: dict | None = None) -> str:
        res = self._rpc('tools/call', {'name': tool, 'arguments': args or {}})
        text = '\n'.join(c.get('text', '') for c in (res or {}).get('content', []) if c.get('type') == 'text')
        if res and res.get('isError'):
            raise RuntimeError(f'{tool}: {text}')
        return text

    def new(self, w, h, name, palette='endesga-64'):
        return self.call('new_document', {'width': w, 'height': h, 'name': name, 'palette': palette})

    def push(self, canvas: Canvas, name: str | None = None, palette='endesga-64', frame=None, base: Canvas | None = None):
        """Paint the canvas in Pixel Studio. With name: a new document first. With base: only the difference (for frames)."""
        if name:
            self.new(canvas.w, canvas.h, name, palette)
        n = 0
        for t in canvas.tiles(base=base):
            erase = t.pop('_erase', False)
            if erase:
                # clear the transparent cells first, then paint the rest
                for j, row in enumerate(t['rows']):
                    for i, ch in enumerate(row):
                        if ch == '_':
                            a = {'region': {'x': t['x'] + i, 'y': t['y'] + j, 'w': 1, 'h': 1}}
                            if frame is not None:
                                a['frame'] = frame
                            self.call('clear_cel', a)
                t['rows'] = [row.replace('_', '.') for row in t['rows']]
                t['legend'].pop('_', None)
                if all(set(r) <= {'.'} for r in t['rows']):
                    continue
            if frame is not None:
                t['frame'] = frame
            self.call('draw_grid', t)
            n += 1
        return n

    def lock(self, timeout_s: float = 900):
        """A cross-process lock: Pixel Studio has one current document for every client, so only one script may draw at a time."""
        return _FileLock(Path(tempfile.gettempdir()) / 'pxcanvas-pixel-studio.lock', timeout_s)

    def image(self, canvas: Canvas, name: str, path, width=None, height=None, scale=None, palette='endesga-64'):
        """New document, paint, export: one picture, under the lock."""
        with self.lock():
            self.push(canvas, name, palette)
            return self.export(str(path), width, height, scale=scale)

    def sprite(self, name: str, frames: dict, out_dir, scale: int = 8, palette='endesga-64'):
        """One document with a frame per expression: the first is painted whole, the others as differences on a
        duplicated frame. Exports <out_dir>/<name>_<expression>.png at `scale`. Returns the paths."""
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        keys = list(frames)
        base = frames[keys[0]]
        paths = []
        with self.lock():
            self.push(base, name, palette)
            self.export(str(out_dir / f'{name}_{keys[0]}.png'), scale=scale, frame=0)
            paths.append(out_dir / f'{name}_{keys[0]}.png')
            for i, k in enumerate(keys[1:], start=1):
                self.call('duplicate_frame', {'frame': 0, 'index': i})
                self.push(frames[k], frame=i, base=base)
                p = out_dir / f'{name}_{k}.png'
                self.export(str(p), scale=scale, frame=i)
                paths.append(p)
        return paths

    def export(self, path, width=None, height=None, frame=None, scale=None):
        a = {'path': path}
        if width:
            a['width'] = width
        if height:
            a['height'] = height
        if scale:
            a['scale'] = scale
        if frame is not None:
            a['frame'] = frame
        return self.call('export_png', a)
