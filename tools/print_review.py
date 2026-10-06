#!/usr/bin/env python3
"""Look at a print before printing it: a top-down contact sheet and four numbers per piece.

    python3 tools/print_review.py sheet <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py art <out.png> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py edge <out.png> <x>,<y>,<side> <a.stl> [<b.stl> ...]
    python3 tools/print_review.py bed <out.png> <plate.3mf> [--zoom]
    python3 tools/print_review.py side <out.png> <frame.stl> <label> <x0>,<y0>,<x1>,<y1> <piece.stl> [...]
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

`bed` draws a composed plate from above as it will print: every object where `--arrange` put
it, turned as it was turned, on the bed square with the front edge at the bottom, and each one
named by the label in the bed map `bambu slice compose` wrote beside the plate
(`<plate>.bedmap.json`; without it, by the object's file name). It is for plates whose sets look
alike, so the person at the printer bags each one under the right name. A label sits on its own
piece when it fits there whole, and otherwise beside it, clear of every piece, with a line to it.
`--zoom` draws only the part of the bed the pieces take, larger, so a plate of many small pieces
(SPL-1: 30 squares 15 mm across) gets each label on its own piece instead of a web of lines.

`side` cuts the frame and a piece straight down along a line, x0,y0 to x1,y1 mm in their shared
frame, and draws the cut from the side: the frame grey, the piece gold, one row per label, every
row at the same scale and with the tallest point of each written under it. It is for seeing how
tall a piece stands against the walls it sits in. Both meshes must be in the same frame: a
piece at the place of its hole, as bikar's coupons put them. The label, line and piece repeat,
one row each.

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


BED_MM = 256     # the X2D bed, mm (D-053)
BED_PX = 4       # px per mm on the bed picture
ZOOM_PX = 1400   # the long side of a --zoom bed picture, px (the size the plate pages shrink to)
ZOOM_MARGIN = 8  # mm of bed kept round the pieces on a --zoom picture
NUM = r"(-?[0-9.]+(?:[eE][-+]?[0-9]+)?)"


def transform(text):
    """A 3MF transform (12 numbers, row-vector form) as a function of (x, y) -> (x, y)."""
    m = [float(v) for v in text.split()] if text else [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    return lambda x, y: (x * m[0] + y * m[3] + m[9], x * m[1] + y * m[4] + m[10])


def plate_objects(zf):
    """[(object id, [triangle as three (x, y) bed points])] for every build item of a 3MF."""
    model = zf.read("3D/3dmodel.model").decode()
    comps = {}
    for oid, body in re.findall(r'<object id="([^"]+)"[^>]*>(.*?)</object>', model, re.S):
        comps[oid] = re.findall(r'<component[^>]*?path="([^"]+)"[^>]*?objectid="([^"]+)"[^>]*?(?:transform="([^"]*)")?[^>]*/>', body)
    meshes = {}

    def mesh(path, oid):
        if (path, oid) not in meshes:
            text = zf.read(path.lstrip("/")).decode()
            body = re.search(rf'<object id="{oid}"[^>]*>(.*?)</object>', text, re.S).group(1)
            vs = [(float(x), float(y)) for x, y in re.findall(rf'<vertex x="{NUM}" y="{NUM}"', body)]
            ts = [(int(a), int(b), int(c)) for a, b, c in re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', body)]
            meshes[(path, oid)] = (vs, ts)
        return meshes[(path, oid)]

    build = re.search(r"<build\b.*?</build>", model, re.S).group(0)
    out = []
    for tag in re.findall(r"<item\b[^>]*>", build):
        oid = re.search(r'objectid="([^"]+)"', tag).group(1)
        place = transform((re.search(r'transform="([^"]*)"', tag) or [None, ""])[1])
        tris = []
        for path, sub, t in comps.get(oid, []):
            local = transform(t)
            vs, ts = mesh(path, sub)
            pts = [place(*local(x, y)) for x, y in vs]
            tris += [(pts[a], pts[b], pts[c]) for a, b, c in ts]
        out.append((oid, tris))
    return out


def crosses(line, box):
    """Does a leader line pass through a label box? Sampled every 2 px: the boxes are 30 px tall."""
    (x0, y0), (x1, y1) = line
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 2))
    return any(box[0] <= x0 + (x1 - x0) * i / n <= box[2] and box[1] <= y0 + (y1 - y0) * i / n <= box[3]
               for i in range(n + 1))


def label_spot(d, font, name, at, taken, mask, size, lines=(), own=None):
    """Where a label's box goes: at the object's centre if the box lies wholly on that object
    (`own`, its footprint alone) or covers no object, and no other label; else the nearest place
    on rings round it that covers no object, whose leader line crosses no other label and whose
    box sits on no other leader. A box on top of small look-alike pieces hides the very thing the
    picture is for, and a leader running through a neighbour's box points at the wrong row
    (sheets-04g-fit: kite rungs under their labels, then KITE 0.10's line through KITE 0.05). A box
    on its own piece points at nothing else. `size` is the picture's (width, height)."""
    w, h = size
    for r in range(0, max(w, h), 12):
        for k in range(1 if r == 0 else 16):
            a = 2 * math.pi * k / 16
            x, y = at[0] + r * math.cos(a), at[1] - r * math.sin(a)
            b = d.textbbox((x, y), name, font=font, anchor="mm")
            box = (b[0] - 6, b[1] - 4, b[2] + 6, b[3] + 4)
            if box[0] < 0 or box[1] < 0 or box[2] >= w or box[3] >= h:
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


def bed_picture(plate, labels, names=True, zoom=False):
    """The bed from above, front edge at the bottom: each object in its own shade, its label on a
    white box on its own object when it fits there whole, else clear of every object and every
    other label with a line from the box to its object. `labels` maps object id -> label;
    names=False leaves the boxes off. zoom=True draws only the pieces' part of the bed, ZOOM_MARGIN
    mm round them, at the scale that puts its long side at ZOOM_PX."""
    with zipfile.ZipFile(plate) as zf:
        objects = plate_objects(zf)
    x0, y0, x1, y1, px = 0, 0, BED_MM, BED_MM, BED_PX
    pts = [p for _, tris in objects for t in tris for p in t]
    if zoom and pts:
        x0 = max(0, min(p[0] for p in pts) - ZOOM_MARGIN)
        y0 = max(0, min(p[1] for p in pts) - ZOOM_MARGIN)
        x1 = min(BED_MM, max(p[0] for p in pts) + ZOOM_MARGIN)
        y1 = min(BED_MM, max(p[1] for p in pts) + ZOOM_MARGIN)
        px = ZOOM_PX / max(x1 - x0, y1 - y0)
    w, h = round((x1 - x0) * px), round((y1 - y0) * px)
    img = Image.new("RGB", (w, h + CAPTION), (24, 24, 24))
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
    named, owns = [], []
    for k, (oid, tris) in enumerate(objects):
        own = Image.new("L", (w, h), 0)
        o = ImageDraw.Draw(own)
        for t in tris:
            d.polygon([f(p) for p in t], fill=shades[k % len(shades)])
            m.polygon([f(p) for p in t], fill=255)
            o.polygon([f(p) for p in t], fill=255)
        owns.append(own)
        xs = [p[0] for t in tris for p in t] or [0]
        ys = [p[1] for t in tris for p in t] or [0]
        named.append((labels.get(oid, oid), ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)))
    taken, lines = [], []
    for (name, centre), own in zip(named, owns) if names else []:
        at = f(centre)
        (x, y), box = label_spot(d, font, name, at, taken, mask, (w, h), lines, own)
        taken.append(box)
        if (x, y) != at:
            lines.append((at, (x, y)))
            d.line([at, (x, y)], fill=(255, 255, 255), width=2)
            d.ellipse([at[0] - 4, at[1] - 4, at[0] + 4, at[1] + 4], fill=(255, 255, 255))
    for (name, centre), box in zip(named if names else [], taken):
        d.rectangle(box, fill=(255, 255, 255))
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), name, fill=(0, 0, 0), font=font, anchor="mm")
    caption = "front of the bed" if not zoom else \
        f"front of the bed (this is {x0:.0f} to {x1:.0f} mm across, {y0:.0f} to {y1:.0f} mm back)"
    d.text((w / 2, h + CAPTION / 2), caption, fill=(200, 200, 200), font=font, anchor="mm")
    return img, named, taken, lines


def bed_sheet(out, plate, zoom=False):
    side = Path(re.sub(r"\.3mf$", "", plate, flags=re.I) + ".bedmap.json")
    labels = {}
    if side.exists():
        labels = {r["object"]: r["label"] for r in json.loads(side.read_text())["objects"]}
    else:
        print(f"no bed map at {side}: naming objects by their 3MF id")
    img, named, _, _ = bed_picture(plate, labels, zoom=zoom)
    for name, (x, y) in named:
        print(f"{name:12} at {x:6.1f}, {y:6.1f} mm from the front-left corner")
    img.save(out)
    print("wrote", out)


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
    checks += bed_self_test()
    checks += side_self_test()
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return all(ok for _, ok in checks)


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
    return [
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
    if len(a) in (3, 4) and a[0] == "bed" and a[3:] in ([], ["--zoom"]):
        bed_sheet(a[1], a[2], zoom=a[3:] == ["--zoom"])
        sys.exit(0)
    if len(a) >= 6 and a[0] == "side":
        side_sheet(a[1], a[2], a[3:])
        sys.exit(0)
    if len(a) >= 4 and a[0] == "edge":
        edge_sheet(a[1], parse_region(a[2]), a[3:])
        sys.exit(0)
    sys.exit(__doc__)
