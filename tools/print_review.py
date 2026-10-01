#!/usr/bin/env python3
"""Look at a print before printing it: a top-down contact sheet and four numbers per piece.

    python3 tools/print_review.py sheet <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py art <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py edge <out.png> <x>,<y>,<side> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py --self-test

The sheet is white material on black, one tile per STL, the way the piece reads from above,
with the STL's file name under each tile so a sheet of variants can be picked from by name.
Beside it the tool prints, per piece, over the area inside its outline:

  open     the share of that area cut through. A coaster whose holes are the point and
           which is near-solid reads as a slab with pinholes.
  biggest  the share taken by the single largest hole. A bare wedge between art and frame,
           or art that stops short of the outline, shows up as one hole far bigger than the
           rest.
  bare     the share of grid cells (8x8 over the outline) that are almost all hole. Art
           that fills the shape leaves none; a half-filled square leaves many.
  sym      how well the art matches itself turned: the share of its top faces that land on
           art after the best turn of 360/n about the art's centre of mass, n from 2 to 16,
           checked both ways. `order` is that n. A rosette scores 1; art that sits to one
           side, stops partway, or has uneven petals scores low. Only turns are tried, not
           mirrors. The art is the faces at the piece's top height, so a relief coaster is
           judged by its raised lines, not by its slab, and a join tab does not count.

`art` draws the same sheet from the top faces only: what `sym` measured, with the centre it
turned about marked, so a low score can be read by eye.

`edge` draws each piece's footprint (the faces at its lowest height, where every wall stands)
inside one square of the STL's own frame, centred at x,y and `side` mm across, filling the
tile. It is for comparing edges: a 4 mm square puts 100 px on a millimetre, so a 0.4 mm step
is 40 px. The top faces would not do: on a rounded top their outline is the round, not the
wall.

The numbers flag, the eyes decide: read the sheet every time (review-print skill).
Only Pillow is needed.
"""
import math
import struct
import sys
from collections import deque

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

S = 400          # tile size, px
CAPTION = 32     # caption band under each tile, px
GRID = 8         # bare-cell grid
BARE_CELL = 0.8  # a cell at least this open counts as bare
TOP_EPS = 0.05   # mm: a face this close to the top height is part of the art
SYM_ORDERS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16)
SYM_SLACK = 5    # px (MaxFilter size): how far turned art may land from art and still count


def load_triangles(path):
    data = open(path, "rb").read()
    if data[:5] == b"solid" and b"facet" in data[:400]:
        raise SystemExit(f"{path}: ASCII STL, render with --format stl (binary)")
    n = struct.unpack_from("<I", data, 80)[0]
    return [struct.unpack_from("<12f", data, 84 + 50 * i)[3:] for i in range(n)]


def silhouette(tris, top=False):
    """The piece from above. With top=True, only the faces at its top height (the art), in
    the same frame, so the two images line up pixel for pixel."""
    xs = [t[j] for t in tris for j in (0, 3, 6)]
    ys = [t[j] for t in tris for j in (1, 4, 7)]
    x0, y0 = min(xs), min(ys)
    span = max(max(xs) - x0, max(ys) - y0)
    zmax = max(t[j] for t in tris for j in (2, 5, 8))
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    f = lambda x, y: ((x - x0) / span * (S - 3) + 1, (S - 2) - (y - y0) / span * (S - 3))
    kept = [t for t in tris if not top or min(t[2], t[5], t[8]) >= zmax - TOP_EPS]
    for t in kept:
        d.polygon([f(t[0], t[1]), f(t[3], t[4]), f(t[6], t[7])], fill=255)
    return img, centre(img)


def centre(img):
    """The centre of mass of what was drawn: the art's own, so a join tab that widens the
    outline does not move it. A turn that maps the art onto itself leaves this point where it
    is, so it is the middle of every rosette. The bbox centre is not, for an odd order: a
    seven-point star with a point up reaches farther up than down, and turning about its bbox
    centre scored the seven-fold CS-6 0.72 with seven equal petals."""
    w = img.size[0]
    n = sx = sy = 0
    for i, v in enumerate(img.tobytes()):
        if v > 127:
            n += 1
            sx += i % w
            sy += i // w
    return (sx / n, sy / n) if n else (w / 2, img.size[1] / 2)


def count(img):
    return img.histogram()[255]


def symmetry(art, centre):
    """(sym, order): the best turn of the art about the centre, see the module doc."""
    art = art.point(lambda v: 255 if v > 127 else 0)
    fat = art.filter(ImageFilter.MaxFilter(SYM_SLACK))
    n = count(art)
    if not n:
        return 0.0, 0
    scores = []
    for k in SYM_ORDERS:
        turned = art.rotate(360 / k, resample=Image.NEAREST, center=centre)
        fat_turned = turned.filter(ImageFilter.MaxFilter(SYM_SLACK))
        there = count(ImageChops.multiply(turned, fat)) / max(count(turned), 1)
        back = count(ImageChops.multiply(art, fat_turned)) / n
        scores.append((min(there, back), k))
    best = max(s for s, _ in scores)
    # a 12-fold rosette also matches its 2-, 3-, 4- and 6-fold turns: report the highest
    return best, max(k for s, k in scores if s >= best - 0.02)


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


def compose(tiles, names):
    """Tiles side by side, each with its name centred in a caption band beneath it."""
    pad = 10
    im = Image.new("L", ((S + pad) * len(tiles) - pad, S + CAPTION), 0)
    d = ImageDraw.Draw(im)
    font = ImageFont.load_default(size=20)
    for k, (t, name) in enumerate(zip(tiles, names)):
        x = k * (S + pad)
        im.paste(t, (x, 0))
        d.text((x + S / 2, S + CAPTION / 2), name, fill=200, font=font, anchor="mm")
    return im


def sheet(out, paths):
    tiles, syms = [], []
    for p in paths:
        tris = load_triangles(p)
        tiles.append(silhouette(tris)[0])
        syms.append(symmetry(*silhouette(tris, top=True)))
    names = [p.rsplit("/", 1)[-1] for p in paths]
    print(f"{'piece':40} {'open':>6} {'biggest':>8} {'bare':>6} {'holes':>6} {'sym':>5} {'order':>5}")
    for name, t, (sym, order) in zip(names, tiles, syms):
        m = measure(t)
        print(f"{name:40} {m['open']:6.2f} {m['biggest']:8.2f} {m['bare']:6.2f} {m['holes']:6d}"
              f" {sym:5.2f} {order:5d}")
    compose(tiles, [n.removesuffix(".stl") for n in names]).save(out)
    print("wrote", out)


def art_sheet(out, paths):
    tiles = []
    for p in paths:
        img, (cx, cy) = silhouette(load_triangles(p), top=True)
        ImageDraw.Draw(img).ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=128, width=2)
        tiles.append(img)
    compose(tiles, [p.rsplit("/", 1)[-1].removesuffix(".stl") for p in paths]).save(out)
    print("wrote", out)


def footprint(tris, region):
    """The faces at the piece's lowest height, inside `region` = (x, y, side) mm in the STL's
    own frame, the square filling an S-px tile."""
    cx, cy, side = region
    x0, y0 = cx - side / 2, cy - side / 2
    zmin = min(t[j] for t in tris for j in (2, 5, 8))
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    f = lambda x, y: ((x - x0) / side * S, S - (y - y0) / side * S)
    for t in tris:
        if max(t[2], t[5], t[8]) <= zmin + TOP_EPS:
            d.polygon([f(t[0], t[1]), f(t[3], t[4]), f(t[6], t[7])], fill=255)
    return img


def parse_region(text):
    """`x,y,side` in mm, side > 0."""
    try:
        x, y, side = (float(v) for v in text.split(","))
    except ValueError:
        raise SystemExit(f"edge: region must be <x>,<y>,<side> in mm, got {text!r}")
    if side <= 0:
        raise SystemExit(f"edge: side must be > 0, got {side}")
    return x, y, side


def edge_sheet(out, region, paths):
    tiles = [footprint(load_triangles(p), region) for p in paths]
    compose(tiles, [p.rsplit("/", 1)[-1].removesuffix(".stl") for p in paths]).save(out)
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

    def star(extra, points=6):  # a star band, a point straight up; `extra` adds a blob
        # filled, not a wide line: PIL widens a line unevenly with its angle, which moves a
        # seven-point star's centre of mass 4.5 px
        img = Image.new("L", (S, S), 0)
        d = ImageDraw.Draw(img)
        c = S / 2
        ring = lambda k: [(c + k * (150 if i % 2 == 0 else 70) * math.cos(math.pi * i / points - math.pi / 2),
                           c + k * (150 if i % 2 == 0 else 70) * math.sin(math.pi * i / points - math.pi / 2))
                          for i in range(2 * points)]
        d.polygon(ring(1), fill=255)
        d.polygon(ring(0.9), fill=0)
        if extra:
            d.ellipse([c + 60, c + 60, c + 140, c + 140], outline=255, width=6)
        return symmetry(img, centre(img))

    # A 2 mm square slab at z 0..1 with a stray face at z 1 off to one side: the footprint is the
    # bottom square only, a quarter of a 4 mm region, and the top face is not drawn.
    sq = lambda x0, y0, x1, y1, z: [(x0, y0, z, x1, y0, z, x1, y1, z), (x0, y0, z, x1, y1, z, x0, y1, z)]
    foot = footprint(sq(0, 0, 2, 2, 0) + sq(2.2, 2.2, 2.8, 2.8, 1), (1, 1, 4))
    foot_share = sum(foot.histogram()[128:]) / (S * S)
    stray_px = foot.getpixel((int(3.5 / 4 * S), int(S - 3.5 / 4 * S)))

    even, lopsided, seven = star(False), star(True), star(False, points=7)
    good, slab, part = (measure(square(f)) for f in (lattice, pinholes, half))
    tiles = [square(lattice), square(half)]
    im = compose(tiles, ["a-lattice", "b-half"])
    band = lambda k: im.crop((k * (S + 10), S, k * (S + 10) + S, S + CAPTION)).getextrema()[1]
    checks = [
        ("lattice reads open", good["open"] > 0.25 and good["biggest"] < 0.01 and good["bare"] == 0),
        ("pinhole slab reads near-solid", slab["open"] < 0.05),
        ("half-filled square has a huge hole", part["biggest"] > 0.3 and part["bare"] > 0.3),
        ("the lattice beats the half-fill on bare", good["bare"] < part["bare"]),
        ("every tile has its name under it", band(0) > 0 and band(1) > 0),
        ("the caption leaves the tile as drawn", measure(im.crop((0, 0, S, S))) == good),
        ("a centred six-fold star matches itself six ways", even[0] > 0.95 and even[1] == 6),
        ("the same star with a blob to one side does not", lopsided[0] < 0.9),
        ("a seven-point star, a point up, matches itself seven ways", seven[0] > 0.95 and seven[1] == 7),
        ("edge draws the footprint at the region's scale", abs(foot_share - 0.25) < 0.01),
        ("edge leaves out a face above the bottom", stray_px == 0),
    ]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return all(ok for _, ok in checks)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        sys.exit(0 if self_test() else 1)
    if len(a) >= 3 and a[0] in ("sheet", "art"):
        (sheet if a[0] == "sheet" else art_sheet)(a[1], a[2:])
        sys.exit(0)
    if len(a) >= 4 and a[0] == "edge":
        edge_sheet(a[1], parse_region(a[2]), a[3:])
        sys.exit(0)
    sys.exit(__doc__)
