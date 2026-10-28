#!/usr/bin/env python3
"""Look at a print before printing it: a top-down contact sheet and four numbers per piece.

    python3 tools/print_review.py sheet <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py art <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py edge <out.png> <x>,<y>,<side> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py bottom <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py bed <out.png> <plate.3mf> [--zoom] [--key]
    python3 tools/print_review.py footprints <plate>-media/bed.json <plate.3mf>
    python3 tools/print_review.py side <out.png> <frame.stl> <label> <x0>,<y0>,<x1>,<y1> <piece.stl> [...]
    python3 tools/print_review.py paths <out.png> <plate.3mf> <z> <x>,<y>,<side> [--below] [--px N] [--check]
    python3 tools/print_review.py join <out.png> <a.png> <b.png> [<c.png> ...]
    python3 tools/print_review.py compare <out.png> <LABEL>=<picture>@<x>,<y>,<w>,<h> | <LABEL>=<picture>@<cx>,<cy>,<r>,<a0>,<a1> [...]
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

`bottom` draws each piece's bed face as seen from below, left and right swapped the way a person
turning the piece over sees it, the piece filling its tile. It is for reading the carved id
(D-109) cut into that face before the plate prints: the id shows as dark letters on the face.

`bed` draws a composed plate from above as it will print: every object where `--arrange` put
it, turned as it was turned, on the bed square with the front edge at the bottom, and each one
named by the label in the bed map `bambu slice compose` wrote beside the plate
(`<plate>.bedmap.json`; without it, by the object's file name). It is for plates whose sets look
alike, so the person at the printer bags each one under the right name. Each piece's top faces
are shaded by height, darker the lower, so a piece cut in two shows its pins bright and its holes
and slots dark, where a flat fill would draw a half as a whole piece. A label sits on its own
piece when it fits there whole, and otherwise beside it, clear of every piece, with a line to it.
`--zoom` draws only the part of the bed the pieces take, larger, so a plate of many small pieces
(SPL-1: 30 squares 15 mm across) gets each label on its own piece instead of a web of lines.
`--key` drops the labels for numbers: each label gets one number and one color, shared by all
its copies, numbered in the bed map's order (the recipe's), the number sits on the deepest point
of each half of each piece, and a list beside the bed reads number, color, label and how many
copies. It is for a bed of many small look-alike pieces whose
labels cannot sit on them (split-10: 29 pieces in 18 kinds, where labels and lines tangled).

`side` cuts the frame and a piece straight down along a line, x0,y0 to x1,y1 mm in their shared
frame, and draws the cut from the side: the frame grey, the piece gold, one row per label, every
row at the same scale and with the tallest point of each written under it. It is for seeing how
tall a piece stands against the walls it sits in. Both meshes must be in the same frame: a
piece at the place of its hole, as bikar's coupons put them. The label, line and piece repeat,
one row each.

`paths` draws what the slicer lays down on one layer of a sliced plate: every extruding move on
the layer nearest z mm, inside a square `side` mm across centred at x,y on the bed, each as a
bead of its own line width colored by what it is (outer and inner wall, bottom surface, gap
fill). Black inside the print is bed no line covers. It counts the slits: bare pockets that lines
close in on every side and that are under half a millimetre across on average. `--below` swaps
left and right, so the first layer reads like a photo of the bed face. `--px N` sets the picture's
side (1200 by default): a slit is counted in pixels, so a whole coaster wants about 25 px a
millimetre (`--px 2800` for 112 mm) to count the same slits a close-up does. It is for holes in a face:
whether the slicer left them, or the printer did (the beads are drawn at the width the slicer
asked for, not as they came out). `--check` is the bed-face design's check: it draws at 30 px a
millimeter unless `--px` says otherwise, prints PASS or FAIL, and exits 1 when the bare share is
0.6% or more or the largest bare pocket is 0.2 sq mm or more.

`join` puts pictures side by side on black, each scaled to the same height, for a page that
compares two drawings: a piece's first layer on stock beside the same piece on other settings.

`compare` cuts the same part out of each experiment's picture and lays the cuts side by side on
white, each scaled to one height, with its label under it. It is for comparing one spot across
prints, not whole coasters: a strap corner on three bottoms, or the drawing beside the photo.
Each cut is given in that picture's own pixels: four numbers are a box (x, y, width, height),
five a wedge (centre x, y, radius, and the two angles it runs between, in degrees clockwise from
straight up like a clock face; 0,360 is the whole circle). A wedge is turned so its middle points
up, so wedges cut from photos taken at different turns line up; a box suits a photo taken at a
slant, where a wedge's centre is not the coaster's. Each cut fills the same height whatever its
size, so cut the same span of coaster from each, or the slits will not read at one scale.

The numbers flag, the eyes decide: read the sheet every time (review-print skill).
Only Pillow is needed.
"""
import json
import math
import re
import struct
import sys
import zipfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

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


JOIN_PX = 1000  # the height `join` scales each picture to
JOIN_GAP = 20   # px of black between two joined pictures


def join_pictures(pictures, height=JOIN_PX):
    """Pictures side by side on black, each scaled to `height` keeping its shape."""
    scaled = [p.convert("RGB").resize((round(p.width * height / p.height), height), Image.LANCZOS)
              for p in pictures]
    im = Image.new("RGB", (sum(s.width for s in scaled) + JOIN_GAP * (len(scaled) - 1), height))
    x = 0
    for s in scaled:
        im.paste(s, (x, 0))
        x += s.width + JOIN_GAP
    return im


def join_sheet(out, paths):
    join_pictures([Image.open(p) for p in paths]).save(out)
    print("wrote", out)


COMPARE_PX = 700     # the height `compare` scales each cut to
COMPARE_CAPTION = 44  # the label band under each cut, px
WHITE = (255, 255, 255)


def parse_cut(text):
    """LABEL=path@x,y,w,h (a box) or LABEL=path@cx,cy,r,a0,a1 (a wedge), in the picture's pixels.
    The label ends at the first `=` and the cut starts after the last `@`, so a path may hold either."""
    label, _, rest = text.partition("=")
    path, _, spec = rest.rpartition("@")
    try:
        nums = [float(v) for v in spec.split(",")]
    except ValueError:
        nums = []
    if not label or not path or len(nums) not in (4, 5):
        sys.exit(f"compare: {text!r} is not LABEL=path@x,y,w,h or LABEL=path@cx,cy,r,a0,a1")
    return label, path, nums


def cut_picture(img, nums):
    """The part of `img` the numbers name, on white. Four numbers are a box: x, y, width, height.
    Five are a wedge: centre, radius, and the angles it runs between, in degrees clockwise from
    straight up, like a clock face; 0,360 is the whole circle. A wedge is turned so its middle
    points up, so wedges cut from pictures taken at different turns line up side by side; a
    circle is left as it was taken."""
    img = img.convert("RGB")
    if len(nums) == 4:
        x, y, w, h = nums
        out = Image.new("RGB", (round(w), round(h)), WHITE)
        out.paste(img, (-round(x), -round(y)))
        return out
    cx, cy, r, a0, a1 = nums
    side = round(2 * r)
    square = Image.new("RGB", (side, side), WHITE)
    square.paste(img, (round(r - cx), round(r - cy)))
    whole = a1 - a0 >= 360
    mid = 0 if whole else (a0 + a1) / 2
    if mid:
        square = square.rotate(mid, resample=Image.BICUBIC, fillcolor=WHITE)  # counterclockwise
    mask = Image.new("L", (side, side), 0)
    d = ImageDraw.Draw(mask)
    if whole:
        d.ellipse([0, 0, side - 1, side - 1], fill=255)
    else:  # PIL counts angles from three o'clock, clockwise
        half = (a1 - a0) / 2
        d.pieslice([0, 0, side - 1, side - 1], start=-half - 90, end=half - 90, fill=255)
    out = Image.new("RGB", (side, side), WHITE)
    out.paste(square, mask=mask)
    return out.crop(mask.getbbox())


def compare_pictures(cuts, height=COMPARE_PX):
    """(label, picture) pairs side by side on white, each scaled to `height` keeping its shape,
    with its label in a band beneath it."""
    scaled = [(name, p.resize((max(1, round(p.width * height / p.height)), height), Image.LANCZOS))
              for name, p in cuts]
    im = Image.new("RGB", (sum(p.width for _, p in scaled) + JOIN_GAP * (len(scaled) - 1),
                           height + COMPARE_CAPTION), WHITE)
    d = ImageDraw.Draw(im)
    font = ImageFont.load_default(size=26)
    x = 0
    for name, p in scaled:
        im.paste(p, (x, 0))
        d.text((x + p.width / 2, height + COMPARE_CAPTION / 2), name, fill=(30, 30, 30), font=font, anchor="mm")
        x += p.width + JOIN_GAP
    return im


def compare_sheet(out, specs):
    cuts = []
    for label, path, nums in map(parse_cut, specs):
        cut = cut_picture(ImageOps.exif_transpose(Image.open(path)), nums)
        print(f"{label}: {'box' if len(nums) == 4 else 'wedge'} {cut.width}x{cut.height} px from {path}")
        cuts.append((label, cut))
    compare_pictures(cuts).save(out)
    print("wrote", out)


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


def pins_sheet(out, paths):
    """A split half from above in grey, its pin tops (the faces at its top height) drawn
    large and white over it, so where the pins sit reads against the art. Prints each count."""
    tiles = []
    for p in paths:
        tris = load_triangles(p)
        base, _ = silhouette(tris)
        top, _ = silhouette(tris, top=True)
        mask = [v > 127 for v in top.tobytes()]
        n = len(components(mask, S, S))
        print(f"{p.rsplit('/', 1)[-1]:40} pins {n}")
        tiles.append(ImageChops.lighter(base.point(lambda v: 90 if v > 127 else 0),
                                        top.filter(ImageFilter.MaxFilter(9))))
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


def bottom(tris):
    """The face that sits on the bed, seen from below as a person turning the piece over sees it:
    left and right swapped, the faces at the lowest height, the piece's outline filling the tile.
    A carved id (D-109) is cut into that face, so it reads as dark letters on it."""
    xs = [t[j] for t in tris for j in (0, 3, 6)]
    ys = [t[j] for t in tris for j in (1, 4, 7)]
    x1, y0 = max(xs), min(ys)
    span = max(x1 - min(xs), max(ys) - y0)
    zmin = min(t[j] for t in tris for j in (2, 5, 8))
    img = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(img)
    f = lambda x, y: ((x1 - x) / span * (S - 3) + 1, (S - 2) - (y - y0) / span * (S - 3))
    for t in tris:
        if max(t[2], t[5], t[8]) <= zmin + TOP_EPS:
            d.polygon([f(t[0], t[1]), f(t[3], t[4]), f(t[6], t[7])], fill=255)
    return img


def bottom_sheet(out, paths):
    tiles = [bottom(load_triangles(p)) for p in paths]
    compose(tiles, [p.rsplit("/", 1)[-1].removesuffix(".stl") for p in paths]).save(out)
    print("wrote", out)


BED_MM = 256     # the X2D bed, mm (D-053)
BED_PX = 4       # px per mm on the bed picture
ZOOM_PX = 1400   # the long side of a --zoom bed picture, px (the size the plate pages shrink to)
ZOOM_MARGIN = 8  # mm of bed kept round the pieces on a --zoom picture
NUM = r"(-?[0-9.]+(?:[eE][-+]?[0-9]+)?)"


def transform(text, with_z=False):
    """A 3MF transform (12 numbers, row-vector form) as a function of (x, y) -> (x, y), or of
    (x, y, z) -> (x, y, z) with_z."""
    m = [float(v) for v in text.split()] if text else [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    if with_z:
        return lambda x, y, z: (x * m[0] + y * m[3] + z * m[6] + m[9], x * m[1] + y * m[4] + z * m[7] + m[10],
                                x * m[2] + y * m[5] + z * m[8] + m[11])
    return lambda x, y: (x * m[0] + y * m[3] + m[9], x * m[1] + y * m[4] + m[10])


def plate_objects(zf, with_z=False):
    """[(object id, [triangle as three (x, y) bed points])] for every build item of a 3MF; the
    points are (x, y, z) with_z."""
    model = zf.read("3D/3dmodel.model").decode()
    comps = {}
    for oid, body in re.findall(r'<object id="([^"]+)"[^>]*>(.*?)</object>', model, re.S):
        comps[oid] = re.findall(r'<component[^>]*?path="([^"]+)"[^>]*?objectid="([^"]+)"[^>]*?(?:transform="([^"]*)")?[^>]*/>', body)
    meshes = {}

    def mesh(path, oid):
        if (path, oid) not in meshes:
            text = zf.read(path.lstrip("/")).decode()
            body = re.search(rf'<object id="{oid}"[^>]*>(.*?)</object>', text, re.S).group(1)
            vs = [tuple(map(float, v)) for v in re.findall(rf'<vertex x="{NUM}" y="{NUM}" z="{NUM}"', body)]
            ts = [(int(a), int(b), int(c)) for a, b, c in re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', body)]
            meshes[(path, oid)] = (vs, ts)
        return meshes[(path, oid)]

    build = re.search(r"<build\b.*?</build>", model, re.S).group(0)
    out = []
    for tag in re.findall(r"<item\b[^>]*>", build):
        oid = re.search(r'objectid="([^"]+)"', tag).group(1)
        place = transform((re.search(r'transform="([^"]*)"', tag) or [None, ""])[1], True)
        tris = []
        for path, sub, t in comps.get(oid, []):
            local = transform(t, True)
            vs, ts = mesh(path, sub)
            pts = [place(*local(*v)) if with_z else place(*local(*v))[:2] for v in vs]
            tris += [(pts[a], pts[b], pts[c]) for a, b, c in ts]
        out.append((oid, tris))
    return out


def crosses(line, box):
    """Does a leader line pass through a label box? Sampled every 2 px: the boxes are 30 px tall."""
    (x0, y0), (x1, y1) = line
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 2))
    return any(box[0] <= x0 + (x1 - x0) * i / n <= box[2] and box[1] <= y0 + (y1 - y0) * i / n <= box[3]
               for i in range(n + 1))


def label_spot(d, font, name, at, taken, mask, size, lines=(), own=None, inside=None):
    """Where a label's box goes: at the object's centre if the box lies wholly on that object
    (`own`, its footprint alone) or covers no object, and no other label; else the nearest place
    on rings round it that covers no object, whose leader line crosses no other label and whose
    box sits on no other leader. A box on top of small look-alike pieces hides the very thing the
    picture is for, and a leader running through a neighbour's box points at the wrong row
    (sheets-04g-fit: kite rungs under their labels, then KITE 0.10's line through KITE 0.05). A box
    on its own piece points at nothing else. `size` is the picture's (width, height). `inside`, a
    (left, top, right, bottom) box in px, keeps the label within its piece's group box, so a label
    never sits over the next set (split-04: HEX-15's label over set 7's edge)."""
    w, h = size
    for r in range(0, max(w, h), 12):
        for k in range(1 if r == 0 else 16):
            a = 2 * math.pi * k / 16
            x, y = at[0] + r * math.cos(a), at[1] - r * math.sin(a)
            b = d.textbbox((x, y), name, font=font, anchor="mm")
            box = (b[0] - 6, b[1] - 4, b[2] + 6, b[3] + 4)
            if box[0] < 0 or box[1] < 0 or box[2] >= w or box[3] >= h:
                continue
            if inside and (box[0] < inside[0] or box[1] < inside[1] or box[2] > inside[2] or box[3] > inside[3]):
                continue
            if any(box[0] < t[2] and t[0] < box[2] and box[1] < t[3] and t[1] < box[3] for t in taken):
                continue
            if r == 0 and own is not None and own.crop(box).getextrema() == (255, 255):
                return (x, y), box
            if r and (any(crosses((at, (x, y)), t) for t in taken) or any(crosses(ln, box) for ln in lines)):
                continue
            if mask.crop(box).getbbox() is None:
                return (x, y), box
    b = d.textbbox(at, name, font=font, anchor="mm")
    return at, (b[0] - 6, b[1] - 4, b[2] + 6, b[3] + 4)


RELIEF_LOW = 0.45        # how dark an object's lowest top face is drawn, against its highest


def relief(d, f, tris, shade):
    """Paint an object's upward faces over its outline, lowest first, darker the lower they sit
    against the object's own top. From above, a piece cut in two at its middle has the whole
    piece's outline, so a flat fill drew split-07's 82 halves as whole pieces (Omar, 2026-10-26:
    "i don't see the split infill pieces"); its pins stand out bright and its holes and slots
    sink dark, and a pin half's face sits darker than a hole half's, so the pairs read. A piece
    of one height draws as before."""
    up = []
    for t in tris:
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
        if (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) > 1e-9:  # faces up: counter-clockwise from above
            up.append(((az + bz + cz) / 3, t))
    if not up:
        return
    lo, hi = min(z for z, _ in up), max(z for z, _ in up)
    for z, t in sorted(up, key=lambda u: u[0]):
        k = 1 if hi - lo < 1e-6 else RELIEF_LOW + (1 - RELIEF_LOW) * (z - lo) / (hi - lo)
        d.polygon([f(p[:2]) for p in t], fill=tuple(round(c * k) for c in shade))


KEY_W = 420              # px of the list beside a --key bed picture
KEY_ROW = 36             # px per row of that list
BADGE_R = 15             # px radius of the number on each piece of a --key bed picture


def key_shades(n):
    """n colors far apart round the wheel, alternately lighter and darker, so neighbours in the
    list do not look alike."""
    import colorsys
    return [tuple(round(c * 255) for c in colorsys.hsv_to_rgb((i * 0.618034) % 1, 0.55, 0.95 if i % 2 else 0.75))
            for i in range(n)]


def parts(own):
    """An object's footprint split into the pieces that lie apart on the bed, as masks: a piece cut
    in two comes off the bed as two halves, and each half is bagged, so each gets its own badge.
    A part smaller than a badge is a speck, not a half, and is left out."""
    rest, out = own.copy(), []
    while (box := rest.getbbox()) is not None:
        x = box[0]
        y = next(y for y in range(box[1], box[3]) if rest.getpixel((x, y)))
        ImageDraw.floodfill(rest, (x, y), 128)
        part = rest.point(lambda v: 255 if v == 128 else 0)
        rest = rest.point(lambda v: 0 if v == 128 else v)
        if part.histogram()[255] >= math.pi * BADGE_R ** 2:
            out.append(part)
    return out


def deepest(own):
    """The pixel of a footprint farthest from its edge, found by wearing the footprint down a
    pixel at a time: the badge goes there, on the piece, not at its box centre, which on a kite
    or a star can be bare bed."""
    box = own.getbbox()
    if box is None:
        return None
    left, top = box[0] - 2, box[1] - 2
    m = own.crop((left, top, box[2] + 2, box[3] + 2))
    while True:
        worn = m.filter(ImageFilter.MinFilter(3))
        if worn.getbbox() is None:
            break
        m = worn
    b = m.getbbox()
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    x, y = min(((x, y) for y in range(b[1], b[3]) for x in range(b[0], b[2]) if m.getpixel((x, y))),
               key=lambda q: (q[0] - cx) ** 2 + (q[1] - cy) ** 2)
    return x + left, y + top


def kind_order(labels, oids):
    """The labels on the bed, each once, in the bed map's order (the recipe's): kind n of a --key
    bed picture is entry n - 1 here, and `footprints` writes the same n, so the two never drift."""
    present = [labels.get(oid, oid) for oid in oids]
    return list(dict.fromkeys([v for v in labels.values() if v in present] + present))


GROUP_PAD = 3            # mm between a group's pieces and the box drawn round them
GROUP_INK = (250, 215, 60)


def bed_picture(plate, labels, names=True, zoom=False, groups=None, key=False):
    """The bed from above, front edge at the bottom: each object in its own shade, its label on a
    white box on its own object when it fits there whole, else clear of every object and every
    other label with a line from the box to its object. `labels` maps object id -> label;
    names=False leaves the boxes off. zoom=True draws only the pieces' part of the bed, ZOOM_MARGIN
    mm round them, at the scale that puts its long side at ZOOM_PX. `groups` maps object id -> the
    plate's `group:`; each group gets a yellow box round its pieces, GROUP_PAD mm out, and its name
    on a yellow tag above the box, so a set reads as one block (split-03 mixed its sets; Omar,
    2026-10-22: "group related pieces into a rectangle"). key=True numbers the pieces instead of
    naming them, one number and color per label, with the list beside the bed (KEY_W px wide);
    the third value returned is then the badges' boxes and the fourth the list's rows."""
    groups = groups or {}
    with zipfile.ZipFile(plate) as zf:
        solids = plate_objects(zf, with_z=True)
    objects = [(oid, [tuple(p[:2] for p in t) for t in tris]) for oid, tris in solids]
    x0, y0, x1, y1, px = 0, 0, BED_MM, BED_MM, BED_PX
    pts = [p for _, tris in objects for t in tris for p in t]
    if zoom and pts:
        x0 = max(0, min(p[0] for p in pts) - ZOOM_MARGIN)
        y0 = max(0, min(p[1] for p in pts) - ZOOM_MARGIN)
        x1 = min(BED_MM, max(p[0] for p in pts) + ZOOM_MARGIN)
        y1 = min(BED_MM, max(p[1] for p in pts) + ZOOM_MARGIN)
        px = ZOOM_PX / max(x1 - x0, y1 - y0)
    w, h = round((x1 - x0) * px), round((y1 - y0) * px)
    img = Image.new("RGB", (w + (KEY_W if key else 0), h + CAPTION), (24, 24, 24))
    mask = Image.new("L", (w, h), 0)
    d, m = ImageDraw.Draw(img), ImageDraw.Draw(mask)
    d.rectangle([0, 0, w - 1, h - 1], outline=(90, 90, 90), width=2)
    for k in range(32, BED_MM, 32):  # a 32 mm grid, to read distances by eye
        if x0 < k < x1:
            d.line([((k - x0) * px, 0), ((k - x0) * px, h)], fill=(40, 40, 40))
        if y0 < k < y1:
            d.line([(0, h - (k - y0) * px), (w, h - (k - y0) * px)], fill=(40, 40, 40))
    f = lambda p: ((p[0] - x0) * px, h - (p[1] - y0) * px)
    shades = [(230, 180, 90), (120, 200, 230), (160, 220, 130), (230, 130, 160), (190, 160, 240),
              (240, 230, 120), (250, 140, 90), (110, 230, 200), (200, 200, 200), (170, 120, 90)]
    font = ImageFont.load_default(size=26)
    kinds = kind_order(labels, [oid for oid, _ in objects])
    if key:
        palette = dict(zip(kinds, key_shades(len(kinds))))
        shades = [palette[labels.get(oid, oid)] for oid, _ in objects]
    named, owns = [], []
    for k, (oid, tris) in enumerate(objects):
        own = Image.new("L", (w, h), 0)
        o = ImageDraw.Draw(own)
        for t in tris:
            d.polygon([f(p) for p in t], fill=shades[k % len(shades)])
            m.polygon([f(p) for p in t], fill=255)
            o.polygon([f(p) for p in t], fill=255)
        relief(d, f, solids[k][1], shades[k % len(shades)])
        owns.append(own)
        xs = [p[0] for t in tris for p in t] or [0]
        ys = [p[1] for t in tris for p in t] or [0]
        named.append((labels.get(oid, oid), ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)))
    taken, lines, tags = [], [], []
    blocks = {}
    for oid, tris in objects:
        if oid in groups:
            b = blocks.setdefault(groups[oid], [math.inf, math.inf, -math.inf, -math.inf])
            for t in tris:
                for x, y in t:
                    b[:] = [min(b[0], x), min(b[1], y), max(b[2], x), max(b[3], y)]
    rects = {}
    for g, (bx0, by0, bx1, by1) in blocks.items():
        (lx, ty), (rx, by) = f((bx0 - GROUP_PAD, by1 + GROUP_PAD)), f((bx1 + GROUP_PAD, by0 - GROUP_PAD))
        rects[g] = (lx + 3, ty + 3, rx - 3, by - 3)
        d.rectangle([lx, ty, rx, by], outline=GROUP_INK, width=3)
        tb = d.textbbox(((lx + rx) / 2, ty - 22), g, font=font, anchor="mm")
        tag = (tb[0] - 6, tb[1] - 4, tb[2] + 6, tb[3] + 4)
        taken.append(tag)
        tags.append((g, tag))
    if key:
        return keyed(img, d, font, (w, h), objects, labels, kinds, shades, owns, tags, zoom, (x0, y0, x1, y1))
    for (oid, _), (name, centre), own in zip(objects, named, owns) if names else []:
        at = f(centre)
        (x, y), box = label_spot(d, font, name, at, taken, mask, (w, h), lines, own, rects.get(groups.get(oid)))
        taken.append(box)
        if (x, y) != at:
            lines.append((at, (x, y)))
            d.line([at, (x, y)], fill=(255, 255, 255), width=2)
            d.ellipse([at[0] - 4, at[1] - 4, at[0] + 4, at[1] + 4], fill=(255, 255, 255))
    for g, box in tags:
        d.rectangle(box, fill=GROUP_INK)
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), g, fill=(0, 0, 0), font=font, anchor="mm")
    for (name, centre), box in zip(named if names else [], taken[len(tags):]):
        d.rectangle(box, fill=(255, 255, 255))
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), name, fill=(0, 0, 0), font=font, anchor="mm")
    bed_caption(d, font, w, h, zoom, (x0, y0, x1, y1))
    return img, named, taken, lines


def bed_caption(d, font, w, h, zoom, span):
    x0, y0, x1, y1 = span
    caption = "front of the bed" if not zoom else \
        f"front of the bed (this is {x0:.0f} to {x1:.0f} mm across, {y0:.0f} to {y1:.0f} mm back)"
    d.text((w / 2, h + CAPTION / 2), caption, fill=(200, 200, 200), font=font, anchor="mm")


def keyed(img, d, font, size, objects, labels, kinds, shades, owns, tags, zoom, span):
    """The rest of a --key bed picture: a numbered badge on the deepest point of each part of each
    piece, the group tags, and the list beside the bed, numbered in the bed map's order."""
    w, h = size
    small = ImageFont.load_default(size=20)
    badges, named = [], []
    for (oid, _), own in zip(objects, owns):
        name = labels.get(oid, oid)
        n = kinds.index(name) + 1
        named.append((name, deepest(own)))
        for part in parts(own) or [own]:
            if (at := deepest(part)) is None:
                continue
            x, y = at
            box = (x - BADGE_R, y - BADGE_R, x + BADGE_R, y + BADGE_R)
            d.ellipse(box, fill=(0, 0, 0), outline=(255, 255, 255), width=2)
            d.text((x, y), str(n), fill=(255, 255, 255), font=small, anchor="mm")
            badges.append(box)
    for g, box in tags:
        d.rectangle(box, fill=GROUP_INK)
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), g, fill=(0, 0, 0), font=font, anchor="mm")
    rows = []
    for i, name in enumerate(kinds):
        y = 20 + i * KEY_ROW + KEY_ROW / 2
        copies = sum(labels.get(oid, oid) == name for oid, _ in objects)
        d.ellipse((w + 16, y - BADGE_R, w + 16 + 2 * BADGE_R, y + BADGE_R), fill=(0, 0, 0), outline=(255, 255, 255), width=2)
        d.text((w + 16 + BADGE_R, y), str(i + 1), fill=(255, 255, 255), font=small, anchor="mm")
        d.rectangle((w + 56, y - 11, w + 84, y + 11), fill=shades[[labels.get(o, o) for o, _ in objects].index(name)])
        d.text((w + 96, y), name + (f"  x{copies}" if copies > 1 else ""), fill=(230, 230, 230), font=font, anchor="lm")
        rows.append((i + 1, name, copies))
    bed_caption(d, font, w, h, zoom, span)
    return img, named, badges, rows


def bed_sheet(out, plate, zoom=False, key=False):
    side = Path(re.sub(r"\.3mf$", "", plate, flags=re.I) + ".bedmap.json")
    labels, groups = {}, {}
    if side.exists():
        rows = json.loads(side.read_text())["objects"]
        labels = {r["object"]: r["label"] for r in rows}
        groups = {r["object"]: r["group"] for r in rows if r.get("group")}
    else:
        print(f"no bed map at {side}: naming objects by their 3MF id")
    img, named, _, rows = bed_picture(plate, labels, zoom=zoom, groups=groups, key=key)
    if key:
        for n, name, copies in rows:
            print(f"{n:3}  {name:16} x{copies}")
    else:
        for name, (x, y) in named:
            print(f"{name:12} at {x:6.1f}, {y:6.1f} mm from the front-left corner")
    img.save(out)
    print("wrote", out)


FOOT_PX = 8          # px per mm the outlines are traced at: a kite under 10 mm across is 80 px
FOOT_TOL = 0.15      # mm an outline may stray from the traced edge when simplified
FOOT_SPECK = 0.25    # sq mm: a loop smaller than this is a speck, not a piece's edge


def mask_loops(mask):
    """The edges of a filled mask as closed loops of pixel corners (column, row), one per edge:
    each piece's outside and any hole through it. Every set pixel gives the sides it shares with
    an unset one, walked clockwise as the picture shows it, and the sides chain into loops; where
    two pixels touch only at a corner the walk turns right, so they come out as two loops."""
    w, h = mask.size
    px = mask.load()
    on = lambda c, r: 0 <= c < w and 0 <= r < h and px[c, r]
    out = {}
    for r in range(h):
        for c in range(w):
            if not px[c, r]:
                continue
            for cond, a, b in ((not on(c, r - 1), (c, r), (c + 1, r)), (not on(c + 1, r), (c + 1, r), (c + 1, r + 1)),
                               (not on(c, r + 1), (c + 1, r + 1), (c, r + 1)), (not on(c - 1, r), (c, r + 1), (c, r))):
                if cond:
                    out.setdefault(a, []).append(b)
    loops = []
    while out:
        start = next(iter(out))
        loop, at, came = [start], start, None
        while True:
            ends = out[at]
            if len(ends) > 1 and came is not None:  # a corner touch: take the right turn
                dx, dy = at[0] - came[0], at[1] - came[1]
                right = (at[0] - dy, at[1] + dx)
                nxt = right if right in ends else ends[0]
            else:
                nxt = ends[0]
            ends.remove(nxt)
            if not ends:
                del out[at]
            came, at = at, nxt
            if at == start:
                break
            loop.append(at)
        loops.append(loop)
    return loops


def simplify(ring, tol):
    """A closed ring with every point dropped that lies within `tol` of the line its neighbours
    keep (Douglas-Peucker, split at the two points farthest apart so the ring stays closed)."""
    def dp(pts):
        if len(pts) < 3:
            return pts
        (ax, ay), (bx, by) = pts[0], pts[-1]
        L = math.hypot(bx - ax, by - ay) or 1e-12
        far, k = max((abs((bx - ax) * (ay - y) - (ax - x) * (by - ay)) / L, i) for i, (x, y) in enumerate(pts[1:-1], 1))
        return dp(pts[:k + 1])[:-1] + dp(pts[k:]) if far > tol else [pts[0], pts[-1]]
    if len(ring) < 4:
        return ring
    j = max(range(len(ring)), key=lambda i: (ring[i][0] - ring[0][0]) ** 2 + (ring[i][1] - ring[0][1]) ** 2)
    return dp(ring[:j + 1])[:-1] + dp(ring[j:] + [ring[0]])[:-1]


def ring_area(ring):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1])) / 2


def outlines(tris, px=FOOT_PX, tol=FOOT_TOL):
    """One object's outlines seen from above, in bed mm: every triangle of the mesh projected onto
    the bed and filled (as `bed_picture` fills it), the filled area's edges traced and simplified.
    Not the faces at the lowest height: a star's underside is stepped and a kite's is sloped, and
    tracing the bed face alone drew stars as pentagons and kites as slivers. A piece cut in two
    gives a loop per half."""
    xs = [p[0] for t in tris for p in t]
    ys = [p[1] for t in tris for p in t]
    if not xs:
        return []
    x0, y1 = min(xs) - 1, max(ys) + 1
    w, h = math.ceil((max(xs) + 1 - x0) * px), math.ceil((y1 - min(ys) + 1) * px)
    mask = Image.new("1", (w, h), 0)
    d = ImageDraw.Draw(mask)
    for t in tris:
        d.polygon([((x - x0) * px, (y1 - y) * px) for x, y, *_ in t], fill=1)
    rings = []
    for loop in mask_loops(mask):
        ring = [(round(x0 + c / px, 2), round(y1 - r / px, 2)) for c, r in simplify(loop, tol * px)]
        if abs(ring_area(ring)) >= FOOT_SPECK:
            rings.append([list(p) for p in ring])
    return rings


def footprints(plate, bedmap=None):
    """The bed.json dict for a sliced plate (format in `footprints_sheet`)."""
    side = Path(bedmap) if bedmap else Path(re.sub(r"\.3mf$", "", str(plate), flags=re.I) + ".bedmap.json")
    rows = json.loads(side.read_text())["objects"] if side.exists() else []
    head = json.loads(side.read_text()) if side.exists() else {}
    by_oid = {r["object"]: r for r in rows}
    with zipfile.ZipFile(plate) as zf:
        objects = plate_objects(zf)
    labels = {r["object"]: r["label"] for r in rows}
    kinds = kind_order(labels, [oid for oid, _ in objects])
    order = {r["object"]: i for i, r in enumerate(rows)}
    copies, pieces = {}, []
    for oid, tris in sorted(objects, key=lambda o: order.get(o[0], len(order))):
        r = by_oid.get(oid, {})
        entry = r.get("entry", oid)
        copies[entry] = copies.get(entry, 0) + 1
        piece = r.get("piece")
        pieces.append({
            "id": f"{entry}/{copies[entry]}", "entry": entry, "copy": copies[entry], "object": oid,
            "label": labels.get(oid, oid), "name": piece, "kind": kinds.index(labels.get(oid, oid)) + 1,
            "dots": (r.get("params") or {}).get(f"dots_{piece.lower()}", 0) if piece else None,
            "outlines": outlines(tris)})
    name = re.sub(r"\.plate\.3mf$|\.3mf$", "", head.get("plate") or Path(plate).name, flags=re.I)
    return {"plate": name, "bed": {"w": BED_MM, "h": BED_MM}, "pieces": pieces}


def footprints_sheet(out, plate):
    """Write `<plate>-media/bed.json`: what the hub draws the bed from as an SVG, one shape per piece.

        {"plate": "split-10",
         "bed": {"w": 256, "h": 256},
         "pieces": [{"id": "c9/2", "entry": "c9", "copy": 2, "object": "48",
                     "label": "KITE-STOCK", "name": "Kite", "kind": 9, "dots": 0,
                     "outlines": [[[x, y], ...], ...]}, ...]}

    - Coordinates are bed mm, the frame `bed` draws in and the bed map's x and y use: x from the
      bed's left edge, y from its front edge, growing toward the back. To draw it as bed.png does,
      front edge at the bottom, an SVG takes y as `bed.h - y`.
    - `outlines` are closed rings (the first point is not repeated), the piece seen from above:
      the whole mesh projected, not the face on the bed. A piece cut in two has a ring per half;
      a hole through a piece would be a ring of its own, so draw them with fill-rule evenodd.
      Traced at FOOT_PX px a mm and simplified to FOOT_TOL mm, so a ring sits within about 0.2 mm
      of the true edge.
    - `entry` is the recipe item's code in the bed map (`c1` is the first item), `copy` counts that
      entry's objects from 1 in the bed map's order, and `id` is the two joined, `<entry>/<copy>`.
      `object` is the 3MF object id.
    - `label` is the recipe's label, `name` the piece kind the bed map names (Star, Kite, ...),
      `kind` the number the `--key` bed picture puts on the piece, and `dots` the dots on each
      half's cut face (the recipe's `dots_<piece>`, 0 when it sets none). A plate without a bed map
      gets the 3MF ids and nulls.
    Pieces are listed in the bed map's order, which is the recipe's."""
    data = footprints(plate)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(data, separators=(",", ":")) + "\n")
    rings = sum(len(p["outlines"]) for p in data["pieces"])
    print(f"wrote {out}: {len(data['pieces'])} pieces, {rings} outlines, {Path(out).stat().st_size} bytes")


SIDE_PX = 60     # px per mm on a side cut: a 0.05 mm gap is 3 px


def parse_line(text):
    """`x0,y0,x1,y1` in mm, two different points."""
    try:
        x0, y0, x1, y1 = (float(v) for v in text.split(","))
    except ValueError:
        raise SystemExit(f"side: the cut must be <x0>,<y0>,<x1>,<y1> in mm, got {text!r}")
    if (x0, y0) == (x1, y1):
        raise SystemExit(f"side: the cut's two ends are the same point, {text!r}")
    return x0, y0, x1, y1


def cut(tris, line):
    """Where a closed mesh meets the upright plane through `line`: segments ((s, z), (s, z)), s
    the distance along the line from its start in mm."""
    x0, y0, x1, y1 = line
    length = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    segs = []
    for t in tris:
        ps = [(t[j], t[j + 1], t[j + 2]) for j in (0, 3, 6)]
        d = [(x - x0) * -uy + (y - y0) * ux for x, y, _ in ps]  # signed distance off the plane
        hits = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            if (d[a] < 0) != (d[b] < 0):
                k = d[a] / (d[a] - d[b])
                x, y, z = (ps[a][i] + k * (ps[b][i] - ps[a][i]) for i in range(3))
                hits.append(((x - x0) * ux + (y - y0) * uy, z))
        if len(hits) == 2:
            segs.append(tuple(hits))
    return segs, length


def fill_cut(d, segs, length, zmax, color, top):
    """Fill the inside of a cut, column by column, even-odd: each pixel column crosses the
    outline an even number of times, and the material is between the 1st and 2nd, 3rd and 4th."""
    for px in range(int(length * SIDE_PX)):
        s = (px + 0.5) / SIDE_PX
        zs = sorted(za + (s - sa) / (sb - sa) * (zb - za)
                    for (sa, za), (sb, zb) in segs if min(sa, sb) <= s < max(sa, sb))
        for lo, hi in zip(zs[::2], zs[1::2]):
            d.line([(px, top + (zmax - hi) * SIDE_PX), (px, top + (zmax - lo) * SIDE_PX)], fill=color)


def side_picture(frame, rows):
    """One row per (label, line, piece triangles): the frame's cut grey, the piece's gold, at one
    scale. Returns the image and, per row, the frame's and the piece's tallest point in mm."""
    font = ImageFont.load_default(size=28)
    cuts = [(label, cut(frame, line), cut(piece, line)) for label, line, piece in rows]
    zmax = max([z for _, c, p in cuts for segs in (c[0], p[0]) for seg in segs for _, z in seg] + [1])
    width = int(max(c[1] for _, c, _ in cuts) * SIDE_PX)
    band, gap = int(zmax * SIDE_PX), 44
    img = Image.new("RGB", (width, len(cuts) * (band + 2 * gap)), (248, 248, 248))
    d = ImageDraw.Draw(img)
    tall = []
    for k, (label, (fsegs, flen), (psegs, plen)) in enumerate(cuts):
        top = k * (band + 2 * gap) + gap
        fill_cut(d, fsegs, flen, zmax, (128, 128, 128), top)
        fill_cut(d, psegs, plen, zmax, (168, 136, 48), top)
        h = lambda segs: max([z for seg in segs for _, z in seg] or [0])
        tall.append((h(fsegs), h(psegs)))
        d.text((6, top - gap / 2), label, fill=(40, 40, 40), font=font, anchor="lm")
        d.text((6, top + band + gap / 2), f"coaster {tall[-1][0]:.1f} mm · piece {tall[-1][1]:.1f} mm",
               fill=(90, 90, 90), font=font, anchor="lm")
    return img, tall


def side_sheet(out, frame, args):
    if not args or len(args) % 3:
        raise SystemExit("side: give each row as <label> <x0>,<y0>,<x1>,<y1> <piece.stl>")
    rows = [(args[i], parse_line(args[i + 1]), load_triangles(args[i + 2])) for i in range(0, len(args), 3)]
    img, tall = side_picture(load_triangles(frame), rows)
    for (label, _, _), (f, p) in zip(rows, tall):
        print(f"{label:30} frame {f:.2f} mm  piece {p:.2f} mm")
    img.save(out)
    print("wrote", out)


PATHS_PX = 1200   # the side of a `paths` picture, px
ARC_STEP = 0.05   # mm: an arc is drawn as chords this long
SLIT_WIDE = 0.5   # mm: bare bed closed in by lines, thinner than this on average, is a slit
# `paths --check`, the bed-face design's validator: fitted to ten slices (five pieces, stock and
# house preset), drawn at CHECK_PX_PER_MM; docs/design/printing/bed-face-slicing-design.md §6
CHECK_PX_PER_MM = 30
CHECK_MAX_SHARE = 0.6    # % of the first layer left bare
CHECK_MAX_POCKET = 0.2   # sq mm, the largest single bare pocket
FEATURE_COLORS = {"Outer wall": (235, 90, 130), "Inner wall": (180, 60, 110),
                  "Bottom surface": (250, 185, 90), "Internal solid infill": (240, 220, 120),
                  "Gap infill": (90, 190, 250)}


def gcode_layer(text, z):
    """Every extruding move on the layer nearest height z, as (feature, line width, points),
    arcs (G2/G3) walked in short chords. Returns the layer's height and the moves."""
    heights = [float(ln.split(":")[1]) for ln in text.splitlines() if ln.startswith("; Z_HEIGHT:")]
    if not heights:
        raise SystemExit("paths: the G-code has no '; Z_HEIGHT:' lines")
    want = min(heights, key=lambda h: abs(h - z))
    moves, cur, feature, width, x, y, run = [], None, None, 0.0, 0.0, 0.0, []

    def close():
        nonlocal run
        if len(run) >= 2 and cur == want:
            moves.append((feature, width, run))
        run = []

    for line in text.splitlines():
        if line.startswith("; Z_HEIGHT:"):
            close()
            cur = float(line.split(":")[1])
        elif line.startswith("; FEATURE:"):
            close()
            feature = line.split(":", 1)[1].strip()
        elif line.startswith("; LINE_WIDTH:"):
            close()
            width = float(line.split(":")[1])
        elif line[:3] in ("G0 ", "G1 ", "G2 ", "G3 "):
            words = {w[0]: float(w[1:]) for w in line.split(";")[0].split()[1:]
                     if len(w) > 1 and w[0] in "XYEIJ"}
            nx, ny = words.get("X", x), words.get("Y", y)
            if words.get("E", 0) <= 0 or cur != want:
                close()
                x, y = nx, ny
                continue
            if not run:
                run = [(x, y)]
            if line[:2] in ("G2", "G3"):
                cx, cy = x + words.get("I", 0), y + words.get("J", 0)
                a0, a1 = math.atan2(y - cy, x - cx), math.atan2(ny - cy, nx - cx)
                sweep = a1 - a0
                if line[:2] == "G3" and sweep <= 0:
                    sweep += 2 * math.pi
                if line[:2] == "G2" and sweep >= 0:
                    sweep -= 2 * math.pi
                r = math.hypot(x - cx, y - cy)
                n = max(2, int(abs(sweep) * r / ARC_STEP))
                run += [(cx + r * math.cos(a0 + sweep * i / n), cy + r * math.sin(a0 + sweep * i / n))
                        for i in range(1, n + 1)]
            else:
                run.append((nx, ny))
            x, y = nx, ny
    close()
    return want, moves


def pockets(mask, w, h):
    """4-connected components of the True cells: (size, cells on its rim, touches the picture's
    edge, its first cell's index). A rim cell has a False cell beside it."""
    seen = bytearray(w * h)
    out = []
    for start in range(w * h):
        if not mask[start] or seen[start]:
            continue
        seen[start] = 1
        q, n, rim, edge = deque([start]), 0, 0, False
        while q:
            p = q.popleft()
            n += 1
            px, py = p % w, p // w
            edge = edge or px in (0, w - 1) or py in (0, h - 1)
            nbs = [nb for nb in ((p - 1) if px else -1, (p + 1) if px < w - 1 else -1,
                                 (p - w) if py else -1, (p + w) if py < h - 1 else -1) if nb >= 0]
            rim += any(not mask[nb] for nb in nbs)
            for nb in nbs:
                if mask[nb] and not seen[nb]:
                    seen[nb] = 1
                    q.append(nb)
        out.append((n, rim, edge, start))
    return out


def slit_pockets(img, k):
    """The bare mask of a paths picture drawn at k px/mm, its slits (the bare pockets lines close
    in on every side that are thinner than SLIT_WIDE on average) and its wide pockets (closed in
    too, but wider: a hole the design cuts, or a core no line reached), each as (pixels, first
    pixel's index)."""
    w, h = img.size
    bare = [v == 0 for v in img.convert("L").tobytes()]
    slits, wide = [], []
    for n, rim, edge, start in pockets(bare, w, h):
        if not edge:
            (slits if 2 * n / rim / k < SLIT_WIDE else wide).append((n, start))
    return bare, slits, wide


def paths_picture(moves, region, below=False, px=PATHS_PX):
    """The moves inside a square region, each drawn as a bead of its own line width with round
    ends, colored by feature, on black: black left inside the print is bed nothing covered.
    `below` swaps left and right, the way the bed face looks to a person turning the piece over.
    Returns the picture and the slits, as (count, mm², the largest one's mm², the printed mm²):
    the bare pockets that lines close in on every side and that are thin, under SLIT_WIDE across
    on average (twice the area over the rim). A hole the design cuts is closed in by its wall too,
    but it is wide. The printed area is every pixel a line covers, so slits over printed plus slits
    is the share of the face left bare, which compares a kite with a whole coaster."""
    cx, cy, side = region
    k = px / side
    f = lambda x, y: (((cx + side / 2 - x) if below else (x - cx + side / 2)) * k,
                        (cy + side / 2 - y) * k)
    img = Image.new("RGB", (px, px), (0, 0, 0))
    d = ImageDraw.Draw(img)
    for feature, width, run in moves:
        color, r = FEATURE_COLORS.get(feature, (160, 160, 160)), width * k / 2
        pts = [f(*p) for p in run]
        # Each bead is drawn as its own rectangle, not with a wide line: Pillow's wide lines come
        # out a pixel or so thin at some angles, which opened hairlines between fill lines laid
        # 0.458 mm apart at 0.5 mm wide and counted thousands of slits at a 22.5 degree fill.
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            length = math.hypot(x1 - x0, y1 - y0)
            if length:
                nx, ny = -(y1 - y0) / length * r, (x1 - x0) / length * r
                d.polygon([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny),
                           (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], fill=color)
        for x, y in pts:
            d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    bare, found, _ = slit_pockets(img, k)
    slits = [n for n, _ in found]
    printed = (len(bare) - sum(bare)) / k / k
    return img, (len(slits), sum(slits) / k / k, max(slits, default=0) / k / k, printed)


def bed_face_ok(area, largest, printed):
    """The bed-face check: the bare share and the largest pocket both under their bars."""
    share = 100 * area / (area + printed) if area + printed else 0
    return share < CHECK_MAX_SHARE and largest < CHECK_MAX_POCKET


def paths_sheet(out, plate, z, region, below=False, px=PATHS_PX):
    import zipfile
    with zipfile.ZipFile(plate) as zf:
        name = next(n for n in zf.namelist() if n.endswith(".gcode"))
        text = zf.read(name).decode("utf-8", "replace")
    height, moves = gcode_layer(text, z)
    img, (n, area, largest, printed) = paths_picture(moves, region, below, px)
    font = ImageFont.load_default(size=28)
    d = ImageDraw.Draw(img)
    legend = [(f, c) for f, c in FEATURE_COLORS.items() if any(m[0] == f for m in moves)]
    for i, (feat, color) in enumerate(legend):
        d.rectangle([10, 10 + 36 * i, 34, 34 + 36 * i], fill=color)
        d.text((44, 22 + 36 * i), feat, fill=(255, 255, 255), font=font, anchor="lm")
    d.text((10, px - 20), f"z {height:.2f} mm · {region[2]:g} mm across · "
           f"{'from below' if below else 'from above'} · slits {n}, {area:.2f} sq mm",
           fill=(255, 255, 255), font=font, anchor="lm")
    img.save(out)
    share = 100 * area / (area + printed) if area + printed else 0
    print(f"layer {height:.2f} mm  slits {n}  bare {area:.3f} mm²  largest {largest:.3f} mm²  "
          f"printed {printed:.1f} mm²  bare share {share:.2f}%")
    print("wrote", out)
    return bed_face_ok(area, largest, printed)


def paths_self_test():
    """Made-up G-code on two layers: a 10 mm square wall loop 0.4 wide, filled with lines 0.4
    apart that reach the wall, has no slits; the same fill stopped 0.4 short of the wall leaves
    slits; the layer asked for is the one drawn; and an arc is walked as one."""
    def layer(z, fill_end):
        g = [f"; Z_HEIGHT: {z}", "; FEATURE: Outer wall", "; LINE_WIDTH: 0.4", "G1 X0 Y0",
             "G1 X10 Y0 E1", "G1 X10 Y10 E1", "G1 X0 Y10 E1", "G1 X0 Y0 E1",
             "; FEATURE: Bottom surface", "; LINE_WIDTH: 0.42"]
        for i in range(1, 25):
            yy = i * 0.4
            g += [f"G1 X{0.2 + fill_end} Y{yy}", f"G1 X{9.8 - fill_end} Y{yy} E1"]
        return g
    text = "\n".join(layer(0.2, 0.0) + layer(0.4, 0.4))
    region = (5, 5, 12)
    _, full = paths_picture(gcode_layer(text, 0.2)[1], region)
    _, short = paths_picture(gcode_layer(text, 0.4)[1], region)
    arc = "\n".join(["; Z_HEIGHT: 0.2", "; FEATURE: Outer wall", "; LINE_WIDTH: 0.4",
                     "G1 X1 Y0", "G3 X-1 Y0 I-1 J0 E1"])
    _, moves = gcode_layer(arc, 0.2)
    _, hole = paths_picture([m for m in gcode_layer(text, 0.2)[1] if m[0] == "Outer wall"], region)
    big, short_big = paths_picture(gcode_layer(text, 0.4)[1], region, px=2400)
    # The slicer's real first layer: fill 0.5 mm wide laid 0.458 mm apart, so the beads overlap.
    # Run at a 22.5 degree fill across the square and out past it, they leave no bed bare at any
    # angle; Pillow's wide lines once left hairlines here and counted them as slits.
    tilted = []
    for deg in (22.5, 27, 45):
        a = math.radians(deg)
        ux, uy, nx, ny = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        fill = [("Bottom surface", 0.5,
                 [(5 + o * nx - 20 * ux, 5 + o * ny - 20 * uy), (5 + o * nx + 20 * ux, 5 + o * ny + 20 * uy)])
                for o in (i * 0.458 for i in range(-40, 41))]
        wall = [m for m in gcode_layer(text, 0.2)[1] if m[0] == "Outer wall"]
        tilted.append(paths_picture(wall + fill, region, px=360)[1][0])
    return [
        ("paths: overlapping fill lines leave no slit at a 22.5, 27 or 45 degree fill, "
         "at the check's 30 px a mm", tilted == [0, 0, 0]),
        ("paths: --px sets the picture's side and keeps the bare area in sq mm",
         big.size == (2400, 2400) and abs(short_big[1] - short[1]) < 0.15 * short[1]),
        ("paths: fill that reaches the wall leaves no slit", full[0] == 0),
        ("paths: a wide hole closed in by its wall is not a slit", hole[0] == 0),
        ("paths: fill stopped short of the wall leaves slits", short[0] >= 2 and short[1] > 0.5),
        ("paths: the printed area is the square out to the wall's outer edge (10.4 mm a side)",
         abs(full[3] - 10.4 ** 2) < 3),
        ("paths: the largest slit is one of the slits, not their sum",
         0 < short[2] < short[1]),
        ("paths --check: the stock radial coaster fails on its largest pocket alone, "
         "the house radial passes, the stock middle piece passes",
         not bed_face_ok(24.240, 0.390, 4504.8) and bed_face_ok(5.007, 0.164, 4535.7)
         and bed_face_ok(0.413, 0.050, 200.7)),
        ("paths --check: the stock small kites fail, the house kites pass on share 0.51%",
         not bed_face_ok(3.429, 0.587, 65.5) and bed_face_ok(0.358, 0.049, 69.4)),
        ("paths: the layer nearest z is the one drawn", gcode_layer(text, 0.35)[0] == 0.4),
        ("paths: a half-circle arc ends where it should, through the top",
         len(moves) == 1 and math.dist(moves[0][2][-1], (-1, 0)) < 1e-6
         and max(p[1] for p in moves[0][2]) > 0.99),
    ]


def side_self_test():
    """A 4 x 4 x 4 mm frame with a 2 mm square hole through it, and a 1 mm tall piece in the hole,
    cut through the middle: the frame stands either side of the hole and not in it, the piece sits
    in the hole up to 1 mm and no higher, and the heights read 4 and 1."""
    def box(x0, y0, x1, y1, z1):
        v = [(x, y, z) for z in (0, z1) for y in (y0, y1) for x in (x0, x1)]
        faces = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
                 (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
        return [v[a] + v[b] + v[c] for a, b, c in faces]
    frame = box(0, 0, 1, 4, 4) + box(3, 0, 4, 4, 4) + box(1, 0, 3, 1, 4) + box(1, 3, 3, 4, 4)
    img, tall = side_picture(frame, [("T", (-1, 2, 5, 2), box(1.2, 1.2, 2.8, 2.8, 1))])
    at = lambda s, z: img.getpixel((int((s + 0) * SIDE_PX), int(44 + (4 - z) * SIDE_PX)))
    grey, gold = (128, 128, 128), (168, 136, 48)
    return [
        ("side fills the frame either side of the hole", at(1.5, 2) == grey and at(4.5, 2) == grey),
        ("side leaves the hole empty above the piece", at(3, 2) == (248, 248, 248)),
        ("side draws the piece in the hole, to its height only", at(3, 0.5) == gold and at(3, 1.5) != gold),
        ("side leaves the gap between piece and wall open", at(2.1, 0.5) == (248, 248, 248)),
        ("side reads the heights", [round(v, 2) for v in tall[0]] == [4.0, 1.0]),
    ]


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
    # A 10 mm slab whose bed face is only its left half (x < 5): from below, that half is on the right.
    under = bottom(sq(0, 0, 5, 10, 0) + sq(5, 0, 10, 10, 1) + sq(0, 0, 10, 10, 2))
    under_right, under_left = under.getpixel((3 * S // 4, S // 2)), under.getpixel((S // 4, S // 2))

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
        ("bottom draws the bed face mirrored, as seen from below", under_right == 255 and under_left == 0),
    ]
    checks += bed_self_test()
    checks += side_self_test()
    checks += paths_self_test()
    tall, wide = Image.new("RGB", (100, 200), (255, 0, 0)), Image.new("RGB", (300, 100), (0, 0, 255))
    joined = join_pictures([tall, wide], height=200)
    checks += [
        ("join scales each picture to one height, keeping its shape, with a gap between",
         joined.size == (100 + JOIN_GAP + 600, 200)),
        ("join keeps the order: the first picture on the left, black in the gap",
         joined.getpixel((50, 100)) == (255, 0, 0) and joined.getpixel((100 + JOIN_GAP // 2, 100)) == (0, 0, 0)
         and joined.getpixel((100 + JOIN_GAP + 300, 100)) == (0, 0, 255)),
    ]
    checks += compare_self_test()
    checks += footprints_self_test()
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return all(ok for _, ok in checks)


def compare_self_test():
    """A 400 x 300 picture, red on the left half and blue on the right, with a green dot near the
    top right. A box comes out its own size and keeps what was in it; a wedge across the right
    half is turned to point up and is blue inside, white outside; a circle is not turned; the
    sheet keeps the order, one height, and a label under each."""
    red, blue, green = (255, 0, 0), (0, 0, 255), (0, 200, 0)
    pic = Image.new("RGB", (400, 300), red)
    pic.paste(blue, (200, 0, 400, 300))
    pic.paste(green, (300, 40, 310, 50))
    near = lambda a, b: all(abs(x - y) < 40 for x, y in zip(a, b))
    box = cut_picture(pic, [295, 35, 20, 20])
    edge = cut_picture(pic, [390, 290, 20, 20])  # half off the picture: the rest is white
    wedge = cut_picture(pic, [200, 150, 100, 45, 135])  # the right side, pointing three o'clock
    circle = cut_picture(pic, [200, 150, 100, 0, 360])
    w, h = wedge.size
    sheet = compare_pictures([("A", box), ("B", circle)], height=100)
    ink = lambda x0, x1: sheet.crop((x0, 100, x1, 100 + COMPARE_CAPTION)).getextrema()[0][0] < 128
    return [
        ("compare: a box comes out its own size, with what was inside it",
         box.size == (20, 20) and box.getpixel((10, 10)) == green and box.getpixel((1, 1)) == blue),
        ("compare: a box past the picture's edge is white there", edge.getpixel((15, 15)) == WHITE
         and edge.getpixel((5, 5)) == blue),
        ("compare: a wedge is turned so its middle points up",
         near(wedge.getpixel((w // 2, 5)), blue) and h > w * 0.6),
        ("compare: a wedge across the blue half holds no red, and is white outside its sides",
         not any(near(wedge.getpixel((x, y)), red) for x in range(0, w, 7) for y in range(0, h, 7))
         and wedge.getpixel((2, h - 2)) == WHITE and wedge.getpixel((w - 3, h - 2)) == WHITE),
        ("compare: a circle is not turned: red on the left, blue on the right, white in the corners",
         circle.getpixel((40, 100)) == red and circle.getpixel((160, 100)) == blue
         and circle.getpixel((2, 2)) == WHITE),
        ("compare: the sheet keeps the order, scales each to one height, and labels each",
         sheet.size == (100 + JOIN_GAP + 100, 100 + COMPARE_CAPTION)
         and near(sheet.getpixel((50, 50)), green) and near(sheet.getpixel((100 + JOIN_GAP + 20, 50)), red)
         and ink(0, 100) and ink(100 + JOIN_GAP, 200 + JOIN_GAP)),
        ("compare: the label ends at the first = and the cut starts after the last @",
         parse_cut("G=a@b/c=d.jpg@1,2,3,4,5") == ("G", "a@b/c=d.jpg", [1, 2, 3, 4, 5])),
    ]


def footprints_self_test():
    """A 3MF in memory, as split-10's pieces sit: a star whose face on the bed is only its inner
    pentagon (the five points stand on a step above it), a piece cut into two halves lying apart,
    and a bar turned a quarter. The outline must be the star seen from above, ten corners with the
    points, not the pentagon the bed face alone draws; the halves must come out as two rings; the
    turned bar must stand along y; and each object gets its entry, copy, kind and dots from the
    bed map, copies counted in the map's order."""
    import io
    import tempfile
    ring = lambda r, a0, n: [(r * math.cos(math.radians(a0 + 360 * k / n)), r * math.sin(math.radians(a0 + 360 * k / n))) for k in range(n)]
    star = [p for o, i in zip(ring(10, 90, 5), ring(4, 126, 5)) for p in (o, i)]
    pent = ring(4, 126, 5)
    vs = [(0, 0, 1)] + [(x, y, 1) for x, y in star] + [(0, 0, 0)] + [(x, y, 0) for x, y in pent]
    ts = [(0, 1 + k, 1 + (k + 1) % 10) for k in range(10)] + [(11, 12 + k, 12 + (k + 1) % 5) for k in range(5)]
    sq = lambda x0, y0, x1, y1: [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]
    halves = sq(-11, -4, -3, 4) + sq(3, -4, 11, 4)
    bar = sq(-10, -2, 10, 2)
    mesh = lambda oid, vs, ts: (f'<object id="{oid}"><mesh><vertices>' + "".join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in vs)
                                + '</vertices><triangles>' + "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in ts)
                                + '</triangles></mesh></object>')
    quad = lambda n: [(4 * k, 4 * k + 1, 4 * k + 2) for k in range(n)] + [(4 * k, 4 * k + 2, 4 * k + 3) for k in range(n)]
    parts_ = ('<model><resources>' + mesh(1, vs, ts) + mesh(2, halves, quad(2)) + mesh(3, bar, quad(1)) + '</resources></model>')
    comp = lambda oid, sub: (f'<object id="{oid}"><components><component p:path="/3D/Objects/o.model" objectid="{sub}" '
                             'transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>')
    model = ('<model><resources>' + comp(2, 1) + comp(4, 2) + comp(6, 3) + '</resources><build>'
             '<item objectid="2" transform="1 0 0 0 1 0 0 0 1 60 60 0"/>'
             '<item objectid="4" transform="1 0 0 0 1 0 0 0 1 150 150 0"/>'
             '<item objectid="6" transform="0 1 0 -1 0 0 0 0 1 100 180 0"/></build></model>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("3D/3dmodel.model", model)
        zf.writestr("3D/Objects/o.model", parts_)
    rows = [{"object": "2", "entry": "c1", "label": "STAR", "piece": "Star", "params": {"dots_star": 2}},
            {"object": "6", "entry": "c2", "label": "KITE", "piece": "Kite", "params": {}},
            {"object": "4", "entry": "c2", "label": "KITE", "piece": "Kite", "params": {"dots_kite": 0}}]
    with tempfile.TemporaryDirectory() as tmp:
        side = Path(tmp) / "t.plate.bedmap.json"
        side.write_text(json.dumps({"plate": "t.plate.3mf", "bed": "x2d", "objects": rows}))
        data = footprints(buf, side)
    p = {q["object"]: q for q in data["pieces"]}

    def inside(pt, ring_):
        x, y, hit = pt[0], pt[1], False
        for (ax, ay), (bx, by) in zip(ring_, ring_[1:] + ring_[:1]):
            if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
                hit = not hit
        return hit
    st = p["2"]["outlines"]
    bx = [q[0] for r in p["6"]["outlines"] for q in r]
    by = [q[1] for r in p["6"]["outlines"] for q in r]
    return [
        ("footprints draws a star seen from above, its points in, not the pentagon it stands on",
         len(st) == 1 and 10 <= len(st[0]) <= 14 and inside((60, 68.5), st[0]) and inside((52, 62.6), st[0])
         and not inside((60, 54), st[0])),
        ("footprints gives a piece cut in two a ring per half", len(p["4"]["outlines"]) == 2),
        ("footprints turns a bar a quarter turn", abs(max(bx) - min(bx) - 4) < 0.3 and abs(max(by) - min(by) - 20) < 0.3),
        ("footprints names copies by entry, counted in the bed map's order",
         [q["id"] for q in data["pieces"]] == ["c1/1", "c2/1", "c2/2"] and p["6"]["copy"] == 1),
        ("footprints numbers kinds as the --key picture does, and reads the dots",
         (p["2"]["kind"], p["4"]["kind"], p["2"]["dots"], p["6"]["dots"]) == (1, 2, 2, 0)),
        ("footprints names the plate and the bed", data["plate"] == "t" and data["bed"] == {"w": BED_MM, "h": BED_MM}),
    ]


def bed_self_test():
    """A 3MF in memory: one 20 x 4 mm bar, placed twice — once as drawn at (50, 50), once turned a
    quarter at (150, 150). The picture must fill the bar where each was placed, turned, and leave
    the bed around it empty; the label must come from the map."""
    import io
    bar = ('<model><resources><object id="1"><mesh><vertices>'
           '<vertex x="-10" y="-2" z="0"/><vertex x="10" y="-2" z="0"/>'
           '<vertex x="10" y="2" z="0"/><vertex x="-10" y="2" z="0"/></vertices><triangles>'
           '<triangle v1="0" v2="1" v3="2"/><triangle v1="0" v2="2" v3="3"/></triangles></mesh></object>'
           '</resources></model>')
    model = ('<model><resources>'
             '<object id="2"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
             '<object id="4"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
             '<object id="6"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
             '<object id="8"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
             '<object id="10"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
             '</resources><build>'
             '<item objectid="2" transform="1 0 0 0 1 0 0 0 1 50 50 0"/>'
             '<item objectid="4" transform="0 1 0 -1 0 0 0 0 1 150 150 0"/>'
             '<item objectid="6" transform="1 0 0 0 1 0 0 0 1 50 60 0"/>'
             '<item objectid="8" transform="1 0 0 0 1 0 0 0 1 50 68 0"/>'
             '<item objectid="10" transform="1 0 0 0 1 0 0 0 1 50 76 0"/>'
             '</build></model>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("3D/3dmodel.model", model)
        zf.writestr("3D/Objects/o.model", bar)
    _, named, boxes, lines = bed_picture(buf, {"2": "FLAT", "4": "TURNED", "6": "NEAR", "8": "ROW 3", "10": "ROW 4"})
    img = bed_picture(buf, {}, names=False)[0]  # the label boxes are white: test under them
    lit = lambda x, y: sum(img.getpixel((int(x * BED_PX), int((BED_MM - y) * BED_PX)))) > 300
    covers = lambda b: any(sum(img.getpixel((x, y))) > 300 for x in range(int(b[0]), int(b[2])) for y in range(int(b[1]), int(b[3])))
    apart = lambda a, b: a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]
    # Two 15 mm squares 17 mm apart, as SPL-1's fit tiles sit: zoomed, each label fits on its own
    # square and needs no line; at the whole-bed scale it does not fit and moves off with one.
    square = ('<model><resources><object id="1"><mesh><vertices>'
              '<vertex x="-7.5" y="-7.5" z="0"/><vertex x="7.5" y="-7.5" z="0"/>'
              '<vertex x="7.5" y="7.5" z="0"/><vertex x="-7.5" y="7.5" z="0"/></vertices><triangles>'
              '<triangle v1="0" v2="1" v3="2"/><triangle v1="0" v2="2" v3="3"/></triangles></mesh></object>'
              '</resources></model>')
    pair = ('<model><resources>'
            '<object id="2"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
            '<object id="4"><components><component p:path="/3D/Objects/o.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>'
            '</resources><build>'
            '<item objectid="2" transform="1 0 0 0 1 0 0 0 1 120 100 0"/>'
            '<item objectid="4" transform="1 0 0 0 1 0 0 0 1 137 100 0"/>'
            '</build></model>')
    sq = io.BytesIO()
    with zipfile.ZipFile(sq, "w") as zf:
        zf.writestr("3D/3dmodel.model", pair)
        zf.writestr("3D/Objects/o.model", square)
    zimg, znamed, zboxes, zlines = bed_picture(sq, {"2": "G-10L", "4": "G-10U"}, zoom=True)
    _, _, _, flines = bed_picture(sq, {"2": "G-10L", "4": "G-10U"})
    bare = bed_picture(sq, {}, names=False, zoom=True)[0]
    on_own = lambda b, cx: all(sum(bare.getpixel((x, y))) > 300 for x in (int(b[0]), int(b[2]) - 1)
                               for y in (int(b[1]), int(b[3]) - 1)) and b[0] < cx < b[2]
    zf_ = lambda mm: (mm - (120 - 7.5 - ZOOM_MARGIN)) * ZOOM_PX / (17 + 15 + 2 * ZOOM_MARGIN)
    # Two sets of two squares, as split-04's sets sit: each set gets a yellow box GROUP_PAD mm out
    # from its pieces and a tag above it, and each piece's label stays inside its own set's box.
    sets = io.BytesIO()
    with zipfile.ZipFile(sets, "w") as zf:
        zf.writestr("3D/3dmodel.model", pair.replace("120 100 0", "60 100 0").replace("137 100 0", "60 140 0")
                    .replace("</build>", '<item objectid="6" transform="1 0 0 0 1 0 0 0 1 180 100 0"/>'
                             '<item objectid="8" transform="1 0 0 0 1 0 0 0 1 180 140 0"/></build>')
                    .replace("</resources>", "".join(
                        f'<object id="{i}"><components><component p:path="/3D/Objects/o.model" objectid="1" '
                        'transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>' for i in (6, 8)) + "</resources>"))
        zf.writestr("3D/Objects/o.model", square)
    groups = {"2": "set A", "4": "set A", "6": "set B", "8": "set B"}
    gimg, _, gboxes, _ = bed_picture(sets, {k: f"P{k}" for k in groups}, groups=groups)
    gp = lambda x, y: (round(x * BED_PX), round((BED_MM - y) * BED_PX))
    rect = lambda cx: (gp(cx - 7.5 - GROUP_PAD, 0)[0], gp(0, 147.5 + GROUP_PAD)[1],
                       gp(cx + 7.5 + GROUP_PAD, 0)[0], gp(0, 92.5 - GROUP_PAD)[1])
    within = lambda b, r: r[0] <= b[0] and b[2] <= r[2] and r[1] <= b[1] and b[3] <= r[3]
    # A pin half, as split-07's are: a 15 mm square face 1 mm up with a 2 mm pin standing 1 mm on
    # it. From above both have one outline, so only the height tells the pin from the face.
    pinned = io.BytesIO()
    with zipfile.ZipFile(pinned, "w") as zf:
        zf.writestr("3D/3dmodel.model", pair)
        zf.writestr("3D/Objects/o.model", square.replace('z="0"', 'z="1"').replace(
            "</vertices>", '<vertex x="-1" y="-1" z="2"/><vertex x="1" y="-1" z="2"/>'
                           '<vertex x="1" y="1" z="2"/><vertex x="-1" y="1" z="2"/></vertices>').replace(
            "</triangles>", '<triangle v1="4" v2="5" v3="6"/><triangle v1="4" v2="6" v3="7"/></triangles>'))
    pimg = bed_picture(pinned, {}, names=False)[0]
    pin_at, face_at = sum(pimg.getpixel(gp(120, 100))), sum(pimg.getpixel(gp(125, 100)))
    # --key on the two sets: two copies of A, two of B. Then a piece made of two 8 mm halves with a
    # 6 mm gap between them, as a kite's two halves come off the bed as one object: its box centre
    # is the gap, so a badge there would point at bare bed.
    kimg, _, kbadges, krows = bed_picture(sets, {"6": "B", "8": "B", "2": "A", "4": "A"}, key=True)
    kbare = bed_picture(sets, {}, names=False)[0]
    halves = io.BytesIO()
    with zipfile.ZipFile(halves, "w") as zf:
        zf.writestr("3D/3dmodel.model", pair.replace('<item objectid="4" transform="1 0 0 0 1 0 0 0 1 137 100 0"/>', ''))
        zf.writestr("3D/Objects/o.model", '<model><resources><object id="1"><mesh><vertices>' + "".join(
            f'<vertex x="{x}" y="{y}" z="0"/>' for x0 in (-11, 3) for x, y in ((x0, -4), (x0 + 8, -4), (x0 + 8, 4), (x0, 4)))
            + '</vertices><triangles><triangle v1="0" v2="1" v3="2"/><triangle v1="0" v2="2" v3="3"/>'
            '<triangle v1="4" v2="5" v3="6"/><triangle v1="4" v2="6" v3="7"/></triangles></mesh></object></resources></model>')
    _, _, hbadges, _ = bed_picture(halves, {"2": "KITE"}, key=True)
    hbare = bed_picture(halves, {}, names=False)[0]
    mid = lambda b: (round((b[0] + b[2]) / 2), round((b[1] + b[3]) / 2))
    return [
        ("bed --key lists each label once, numbered in the map's order not the bed's, with its copies",
         krows == [(1, "B", 2), (2, "A", 2)]),
        ("bed --key gives copies of one label one color, and another label another",
         kimg.getpixel(gp(55, 95)) == kimg.getpixel(gp(55, 135)) != kimg.getpixel(gp(175, 95))),
        ("bed --key puts one badge on each piece", len(kbadges) == 4 and all(sum(kbare.getpixel(mid(b))) > 300 for b in kbadges)),
        ("bed --key puts a badge on each half of a two-halves piece, none in the gap between",
         len(hbadges) == 2 and all(sum(hbare.getpixel(mid(b))) > 300 for b in hbadges)),
        ("bed --key widens the picture by the list", kimg.size[0] == gimg.size[0] + KEY_W),
        ("bed draws a pin brighter than the face it stands on", pin_at > face_at + 60),
        ("bed draws a box round each set, GROUP_PAD mm out from its pieces",
         gimg.getpixel(gp(60 - 7.5 - GROUP_PAD, 120)) == GROUP_INK and gimg.getpixel(gp(180 + 7.5 + GROUP_PAD, 120)) == GROUP_INK
         and gimg.getpixel(gp(120, 120)) != GROUP_INK),
        ("bed tags each set above its box", len(gboxes) == 6 and all(b[3] <= rect(c)[1] for b, c in zip(gboxes[:2], (60, 180)))),
        ("bed keeps each piece's label inside its own set's box",
         all(within(b, rect(c)) for b, c in zip(gboxes[2:], (60, 60, 180, 180)))),
        ("bed --zoom draws only the pieces' part of the bed, long side at ZOOM_PX",
         zimg.size[0] == ZOOM_PX and zimg.size[1] < ZOOM_PX + CAPTION),
        ("bed --zoom puts each label on its own piece, with no lines",
         not zlines and on_own(zboxes[0], zf_(120)) and on_own(zboxes[1], zf_(137))),
        ("bed at the whole-bed scale moves a label that does not fit its piece", len(flines) >= 1),
        ("bed fills a placed bar along its length", lit(58, 50) and lit(42, 50)),
        ("bed leaves the bed beside the bar empty", not lit(50, 56)),
        ("bed turns a bar a quarter turn", lit(150, 158) and not lit(158, 150)),
        ("bed names each object from the map", [n for n, _ in named] == ["FLAT", "TURNED", "NEAR", "ROW 3", "ROW 4"]),
        ("bed puts no label over a piece", not any(covers(b) for b in boxes)),
        ("bed puts no label over another (bars 6 to 8 mm apart)",
         all(apart(a, b) for i, a in enumerate(boxes) for b in boxes[i + 1:])),
        ("bed runs no leader line through another label (four bars in a stack)",
         len(lines) >= 3 and not any(crosses(ln, b) for ln in lines for b in boxes
                                     if not (b[0] <= ln[1][0] <= b[2] and b[1] <= ln[1][1] <= b[3]))),
    ]


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        sys.exit(0 if self_test() else 1)
    if len(a) >= 3 and a[0] in ("sheet", "art"):
        (sheet if a[0] == "sheet" else art_sheet)(a[1], a[2:])
        sys.exit(0)
    if len(a) >= 3 and a[0] == "pins":
        pins_sheet(a[1], a[2:])
        sys.exit(0)
    if len(a) >= 3 and a[0] == "bed" and set(a[3:]) <= {"--zoom", "--key"} and len(set(a[3:])) == len(a[3:]):
        bed_sheet(a[1], a[2], zoom="--zoom" in a[3:], key="--key" in a[3:])
        sys.exit(0)
    if len(a) == 3 and a[0] == "footprints":
        footprints_sheet(a[1], a[2])
        sys.exit(0)
    if len(a) >= 4 and a[0] == "join":
        join_sheet(a[1], a[2:])
        sys.exit(0)
    if len(a) >= 3 and a[0] == "compare":
        compare_sheet(a[1], a[2:])
        sys.exit(0)
    if len(a) >= 6 and a[0] == "side":
        side_sheet(a[1], a[2], a[3:])
        sys.exit(0)
    if len(a) >= 3 and a[0] == "bottom":
        bottom_sheet(a[1], a[2:])
        sys.exit(0)
    if len(a) >= 5 and a[0] == "paths":
        rest, below, px, check = a[5:], False, None, False
        while rest[:1] in (["--below"], ["--check"]) or (rest[:1] == ["--px"] and rest[1:2] and rest[1].isdigit()):
            if rest[0] == "--px":
                px, rest = int(rest[1]), rest[2:]
            else:
                below, check, rest = below or rest[0] == "--below", check or rest[0] == "--check", rest[1:]
        if not rest:
            region = parse_region(a[4])
            if px is None:
                px = round(CHECK_PX_PER_MM * region[2]) if check else PATHS_PX
            ok = paths_sheet(a[1], a[2], float(a[3]), region, below=below, px=px)
            if check:
                print(("PASS" if ok else "FAIL") + f": bed face (bare share under {CHECK_MAX_SHARE}%, "
                      f"largest pocket under {CHECK_MAX_POCKET} sq mm, at {px / region[2]:.0f} px a mm)")
            sys.exit(0 if ok or not check else 1)
    if len(a) >= 4 and a[0] == "edge":
        edge_sheet(a[1], parse_region(a[2]), a[3:])
        sys.exit(0)
    sys.exit(__doc__)
