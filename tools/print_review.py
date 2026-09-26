#!/usr/bin/env python3
"""Look at a print before printing it: a top-down contact sheet and three numbers per piece.

    python3 tools/print_review.py sheet <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py --self-test

The sheet is white material on black, one tile per STL, the way the piece reads from above.
Beside it the tool prints, per piece, over the area inside its outline:

  open     the share of that area cut through. A coaster whose holes are the point and
           which is near-solid reads as a slab with pinholes.
  biggest  the share taken by the single largest hole. A bare wedge between art and frame,
           or art that stops short of the outline, shows up as one hole far bigger than the
           rest.
  bare     the share of grid cells (8x8 over the outline) that are almost all hole. Art
           that fills the shape leaves none; a half-filled square leaves many.

The numbers flag, the eyes decide: read the sheet every time (review-print skill).
Only Pillow is needed.
"""
import struct
import sys
from collections import deque

from PIL import Image, ImageDraw

S = 400          # tile size, px
GRID = 8         # bare-cell grid
BARE_CELL = 0.8  # a cell at least this open counts as bare


def load_triangles(path):
    data = open(path, "rb").read()
    if data[:5] == b"solid" and b"facet" in data[:400]:
        raise SystemExit(f"{path}: ASCII STL, render with --format stl (binary)")
    n = struct.unpack_from("<I", data, 80)[0]
    return [struct.unpack_from("<12f", data, 84 + 50 * i)[3:] for i in range(n)]


def silhouette(tris):
    xs = [t[j] for t in tris for j in (0, 3, 6)]
    ys = [t[j] for t in tris for j in (1, 4, 7)]
    x0, y0 = min(xs), min(ys)
    span = max(max(xs) - x0, max(ys) - y0)
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    f = lambda x, y: ((x - x0) / span * (S - 3) + 1, (S - 2) - (y - y0) / span * (S - 3))
    for t in tris:
        d.polygon([f(t[0], t[1]), f(t[3], t[4]), f(t[6], t[7])], fill=255)
    return img


def components(mask, w, h):
    """Sizes of 4-connected components of the True cells in a flat mask."""
    seen = bytearray(w * h)
    out = []
    for start in range(w * h):
        if not mask[start] or seen[start]:
            continue
        seen[start] = 1
        q, n = deque([start]), 0
        while q:
            p = q.popleft()
            n += 1
            x, y = p % w, p // w
            for nb in ((p - 1) if x else -1, (p + 1) if x < w - 1 else -1,
                       (p - w) if y else -1, (p + w) if y < h - 1 else -1):
                if nb >= 0 and mask[nb] and not seen[nb]:
                    seen[nb] = 1
                    q.append(nb)
        out.append(n)
    return out


def measure(img):
    w, h = img.size
    px = img.load()
    solid = [px[i % w, i // w] > 127 for i in range(w * h)]
    # outside = empty cells reachable from the border
    outside = bytearray(w * h)
    q = deque(i for i in range(w * h)
              if (i % w in (0, w - 1) or i // w in (0, h - 1)) and not solid[i])
    for i in q:
        outside[i] = 1
    while q:
        p = q.popleft()
        x, y = p % w, p // w
        for nb in ((p - 1) if x else -1, (p + 1) if x < w - 1 else -1,
                   (p - w) if y else -1, (p + w) if y < h - 1 else -1):
            if nb >= 0 and not solid[nb] and not outside[nb]:
                outside[nb] = 1
                q.append(nb)
    inside = [not outside[i] for i in range(w * h)]
    hole = [inside[i] and not solid[i] for i in range(w * h)]
    area = sum(inside)
    sizes = components(hole, w, h)
    cells, bare = 0, 0
    c = w // GRID
    for gy in range(GRID):
        for gx in range(GRID):
            idx = [(gy * c + y) * w + gx * c + x for y in range(c) for x in range(c)]
            ins = sum(inside[i] for i in idx)
            if ins < 0.9 * len(idx):
                continue  # cell on or past the outline edge
            cells += 1
            if sum(hole[i] for i in idx) >= BARE_CELL * ins:
                bare += 1
    return {
        "open": sum(hole) / area,
        "biggest": (max(sizes) if sizes else 0) / area,
        "bare": bare / cells if cells else 0.0,
        "holes": len(sizes),
    }


def sheet(out, paths):
    pad = 10
    tiles = [silhouette(load_triangles(p)) for p in paths]
    im = Image.new("L", ((S + pad) * len(tiles) - pad, S), 0)
    print(f"{'piece':40} {'open':>6} {'biggest':>8} {'bare':>6} {'holes':>6}")
    for k, (p, t) in enumerate(zip(paths, tiles)):
        im.paste(t, (k * (S + pad), 0))
        m = measure(t)
        name = p.rsplit("/", 1)[-1]
        print(f"{name:40} {m['open']:6.2f} {m['biggest']:8.2f} {m['bare']:6.2f} {m['holes']:6d}")
    im.save(out)
    print("wrote", out)


def self_test():
    def square(draw_holes):
        img = Image.new("L", (S, S), 0)
        d = ImageDraw.Draw(img)
        d.rectangle([20, 20, S - 21, S - 21], fill=255)
        draw_holes(d)
        return img

    def lattice(d):  # even small holes everywhere: open, no big hole, no bare cells
        for y in range(40, S - 40, 30):
            for x in range(40, S - 40, 30):
                d.rectangle([x, y, x + 18, y + 18], fill=0)

    def pinholes(d):  # a slab with pinholes: barely open
        for y in range(40, S - 40, 30):
            for x in range(40, S - 40, 30):
                d.rectangle([x, y, x + 3, y + 3], fill=0)

    def half(d):  # the art stops halfway: one huge bare hole
        lattice(d)
        d.rectangle([200, 30, S - 31, S - 31], fill=0)

    good, slab, part = (measure(square(f)) for f in (lattice, pinholes, half))
    checks = [
        ("lattice reads open", good["open"] > 0.25 and good["biggest"] < 0.01 and good["bare"] == 0),
        ("pinhole slab reads near-solid", slab["open"] < 0.05),
        ("half-filled square has a huge hole", part["biggest"] > 0.3 and part["bare"] > 0.3),
        ("the lattice beats the half-fill on bare", good["bare"] < part["bare"]),
    ]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return all(ok for _, ok in checks)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        sys.exit(0 if self_test() else 1)
    if len(a) >= 3 and a[0] == "sheet":
        sheet(a[1], a[2:])
        sys.exit(0)
    sys.exit(__doc__)
