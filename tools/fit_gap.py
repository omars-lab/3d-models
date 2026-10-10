#!/usr/bin/env python3
"""How a loose piece sits in its pocket: the gap all round, outline against outline.

    python3 tools/fit_gap.py <frame.stl> <piece.stl> [<piece.stl> ...] [--z <mm>] [--json]
    python3 tools/fit_gap.py walls <plate.3mf> <frame.stl> <piece.stl> [...] [--z <mm>]
    python3 tools/fit_gap.py studs <plate.3mf> <plate.bedmap.json>
    python3 tools/fit_gap.py --self-test

`studs` reads a split plate's slice: for each stud pair on the bed map, the stud's and the
socket's diameter as the slicer's wall paths make them (median over the layers, and the
socket's lowest layer on its own), and the gap between them. spl-1 found every drawn gap kept
to within 0.005 mm, so a fit that comes out tighter than drawn is the nozzle, not the slice.

Both meshes must be in the same frame: each piece where its pocket is, as bikar renders a
`loose` coaster's pieces without `pack zipper`. The tool cuts the frame and every piece flat at
height `z` (default 2.0 mm, inside the straight wall, under any top round) and, for each piece
file (one group, named by the file), prints:

  pieces    how many pieces it found, each matched to the pocket its middle sits in
  gap       the gap from the piece's outline to the pocket's, per face, min / mean / max over
            every piece of the group, sampled every 0.05 mm along the piece. Below 0 the piece
            is bigger than its pocket there.
  area, perim, P/A   one piece's area (mm²), outline length (mm), and outline per area (1/mm):
            how much the printer's fixed error along the outline weighs against the piece's size
  tip       the piece's sharpest corner, degrees, and the pocket's sharpest corner
  span      the piece's widest span across (mm) and the pocket's, and their ratio
  corners   each kind of corner the piece has (inside angle, so a notch is over 180) and the
            gap at it: where along the outline the play is

The numbers are the drawn geometry, before the slicer and the nozzle. What the printer does to
an outline is not here; the issue doc that uses this tool says how it adds up.
Only the standard library is needed.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from print_review import load_triangles  # noqa: E402

STEP = 0.05     # mm between samples along a piece's outline
FLAT = 179.0    # degrees: a corner this open is a straight run, not a corner
KEY = 1e-4      # mm: endpoints this close are the same point when chaining a cut


def slice_loops(tris, z):
    """Closed outlines where the mesh meets the plane at height z, as lists of (x, y)."""
    segs = []
    for t in tris:
        ps = [(t[j], t[j + 1], t[j + 2]) for j in (0, 3, 6)]
        hits = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            p, q = sorted((ps[a], ps[b]))  # one order per edge, so both faces get the same point
            if (p[2] < z) != (q[2] < z):
                k = (z - p[2]) / (q[2] - p[2])
                hits.append((p[0] + k * (q[0] - p[0]), p[1] + k * (q[1] - p[1])))
        if len(hits) == 2:
            segs.append(hits)
    key = lambda p: (round(p[0] / KEY), round(p[1] / KEY))
    nxt = {}
    for a, b in segs:
        nxt.setdefault(key(a), []).append(b)
        nxt.setdefault(key(b), []).append(a)
    seen, loops = set(), []
    for a, b in segs:
        if (key(a), key(b)) in seen:
            continue
        loop, prev, cur = [a], a, b
        seen.add((key(a), key(b)))
        while key(cur) != key(a) and len(loop) < len(segs) + 1:
            loop.append(cur)
            options = [p for p in nxt[key(cur)] if key(p) != key(prev)] or nxt[key(cur)]
            prev, cur = cur, options[0]
            seen.add((key(prev), key(cur)))
            seen.add((key(cur), key(prev)))
        seen.add((key(b), key(a)))
        if len(loop) >= 3:
            loops.append(loop)
    return loops


def area(poly):
    return 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))


def perimeter(poly):
    return sum(math.dist(p, q) for p, q in zip(poly, poly[1:] + poly[:1]))


def centroid(poly):
    a = area(poly)
    cx = sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))
    cy = sum((y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))
    return cx / (6 * a), cy / (6 * a)


def inside(pt, poly):
    x, y = pt
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def seg_dist(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    L = ax * ax + ay * ay
    k = 0.0 if L == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L))
    return math.hypot(p[0] - a[0] - k * ax, p[1] - a[1] - k * ay)


def ccw(poly):
    return poly if area(poly) > 0 else poly[::-1]


def corners(poly, where=False):
    """Inside angles (degrees) at the real corners of a loop, straight runs merged; with
    `where`, (angle, point) pairs."""
    poly = ccw(poly)
    n, out = len(poly), []
    for i in range(n):
        a, b, c = poly[i - 1], poly[i], poly[(i + 1) % n]
        u = (a[0] - b[0], a[1] - b[1])
        v = (c[0] - b[0], c[1] - b[1])
        if math.hypot(*u) < 1e-6 or math.hypot(*v) < 1e-6:
            continue
        turn = u[0] * v[1] - u[1] * v[0]  # > 0: a reflex corner on a CCW loop
        ang = math.degrees(math.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1])
                                                     / (math.hypot(*u) * math.hypot(*v))))))
        ang = 360 - ang if turn > 0 else ang
        if abs(ang - 180) > 180 - FLAT:
            out.append((ang, b) if where else ang)
    return out


def span(poly):
    return max(math.dist(p, q) for p in poly for q in poly)


def samples(poly):
    out = []
    for p, q in zip(poly, poly[1:] + poly[:1]):
        n = max(1, int(math.dist(p, q) / STEP))
        out += [(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n) for i in range(n)]
    return out


def gap(piece, pocket):
    """Signed gap from each point of the piece's outline to the pocket's outline: above 0 the
    point is inside the pocket, below 0 it pokes into the wall."""
    edges = list(zip(pocket, pocket[1:] + pocket[:1]))
    out = []
    for p in samples(piece):
        d = min(seg_dist(p, a, b) for a, b in edges)
        out.append(d if inside(p, pocket) else -d)
    return out


def measure(frame_loops, piece_tris, z):
    pieces = [ccw(l) for l in slice_loops(piece_tris, z) if abs(area(l)) > 1e-6]
    holes = [l for l in frame_loops if abs(area(l)) > 1e-6]
    gaps, rows = [], []
    for pc in pieces:
        c = centroid(pc)
        around = [h for h in holes if inside(c, h)]
        if not around:
            continue
        pocket = ccw(min(around, key=lambda h: abs(area(h))))
        if abs(area(pocket)) > 10 * abs(area(pc)):
            continue  # the coaster's own outline, not a pocket: the piece is not in place
        g = gap(pc, pocket)
        gaps += g
        rows.append((pc, pocket, g))
    if not rows:
        return None
    pc, pocket, _ = rows[0]
    A, P = area(pc), perimeter(pc)
    edges = list(zip(pocket, pocket[1:] + pocket[:1]))
    at_corners = sorted({(round(ang, 1), round(min(seg_dist(p, a, b) for a, b in edges)
                                                  * (1 if inside(p, pocket) else -1), 3))
                         for ang, p in corners(pc, where=True)})
    return {
        "corners": [{"angle": a, "gap": g} for a, g in at_corners],
        "pieces": len(rows),
        "gap_min": min(gaps), "gap_mean": sum(gaps) / len(gaps), "gap_max": max(gaps),
        "area": A, "perimeter": P, "p_over_a": P / A,
        "piece_tip": min(corners(pc)), "pocket_tip": min(corners(pocket)),
        "piece_span": span(pc), "pocket_span": span(pocket),
        "span_ratio": span(pc) / span(pocket),
        "_piece": pc, "_pocket": pocket,
    }


def gcode_walls(text, z):
    """The outer-wall loops the slicer printed on the layer nearest height z:
    {object label: [(loop, line width), ...]}, arcs (G2/G3) walked in short steps."""
    layers = gcode_all_walls(text)
    nearest = min(layers, key=lambda h: abs(h - z))
    return nearest, layers[nearest]


def gcode_all_walls(text):
    """Every layer's outer-wall loops: {height: {object label: [(loop, line width), ...]}}."""
    layers, cur, obj, feature, width = {}, None, None, None, None
    x = y = 0.0
    run = []

    def close():
        nonlocal run
        if len(run) >= 4 and math.dist(run[0], run[-1]) < 1.0 and cur is not None:
            layers.setdefault(cur, {}).setdefault(obj, []).append((run[:-1], width))
        run = []

    for line in text.splitlines():
        if line.startswith("; Z_HEIGHT:"):
            close()
            cur = float(line.split(":")[1])
        elif line.startswith("; start printing object, unique label id:"):
            obj = line.rsplit(":", 1)[1].strip()
        elif line.startswith("; stop printing object"):
            close()
            obj = None
        elif line.startswith("; FEATURE:"):
            close()
            feature = line.split(":", 1)[1].strip()
        elif line.startswith("; LINE_WIDTH:"):
            width = float(line.split(":")[1])
        elif line[:3] in ("G0 ", "G1 ", "G2 ", "G3 "):
            words = {w[0]: float(w[1:]) for w in line.split(";")[0].split()[1:] if len(w) > 1
                     and w[0] in "XYZEIJ"}
            nx, ny = words.get("X", x), words.get("Y", y)
            printing = words.get("E", 0) > 0 and feature == "Outer wall"
            if not printing:
                close()
                x, y = nx, ny
                continue
            if not run:
                run = [(x, y)]
            if line[:2] in ("G2", "G3"):
                cx, cy = x + words.get("I", 0), y + words.get("J", 0)
                a0 = math.atan2(y - cy, x - cx)
                a1 = math.atan2(ny - cy, nx - cx)
                sweep = a1 - a0
                if line[:2] == "G3" and sweep <= 0:
                    sweep += 2 * math.pi
                if line[:2] == "G2" and sweep >= 0:
                    sweep -= 2 * math.pi
                r = math.hypot(x - cx, y - cy)
                n = max(2, int(abs(sweep) * r / STEP))
                run += [(cx + r * math.cos(a0 + sweep * i / n), cy + r * math.sin(a0 + sweep * i / n))
                        for i in range(1, n + 1)]
            else:
                run.append((nx, ny))
            x, y = nx, ny
    close()
    return layers


def offset_by_area(A, P, k, area_after, grow):
    """The even offset d that takes an outline of area A, length P and corner sum k from A to
    `area_after`: A - P·d + k·d² inward (a piece), A + P·d + k·d² outward (a hole)."""
    s = 1 if grow else -1
    # k·d² + s·P·d + (A - area_after) = 0, the root nearest zero
    c = A - area_after
    disc = P * P - 4 * k * c
    return (-s * P + s * math.sqrt(disc)) / (2 * k) if k else -c / (s * P)


def plate_gcode(plate):
    import zipfile
    with zipfile.ZipFile(plate) as zf:
        name = next(n for n in zf.namelist() if n.endswith(".gcode"))
        return zf.read(name).decode("utf-8", "replace")


ROUND = 0.97    # 4πA/P² at or over this is a circle; a hexagon is 0.907, a letter far less
NEAR = 12.0     # mm: a round wall this far from every object's spot on the bed is not one of ours


def round_walls(layers, objects, max_d):
    """Every round outer wall under max_d across, put with the bed-map object it sits nearest:
    {entry: [(height, printed diameter, line width), ...]}. A wall round a stud is printed
    outside its path, so the stud is the path plus one line width; a wall round a socket is
    printed inside it, so the socket is the path less one. Which one it is comes from the
    object's piece: round walls on a Lower are studs, on an Upper sockets."""
    out = {o["entry"]: [] for o in objects}
    for h in sorted(layers):
        for loops in layers[h].values():
            for poly, w in loops:
                A, P = abs(area(poly)), perimeter(poly)
                if P == 0 or 4 * math.pi * A / (P * P) < ROUND:
                    continue
                d = 2 * math.sqrt(A / math.pi)
                if d > max_d:
                    continue
                c = centroid(poly)
                o = min(objects, key=lambda o: math.dist(c, (o["x"], o["y"])))
                if math.dist(c, (o["x"], o["y"])) > NEAR:
                    continue
                stud = o["piece"] == "Lower"
                out[o["entry"]].append((h, d + w if stud else d - w, w))
    return out


def studs_report(plate, bedmap, max_d):
    """Stud and socket diameters as sliced, per pair: the toolpath, before the nozzle."""
    objects = json.loads(Path(bedmap).read_text())["objects"]
    walls = round_walls(gcode_all_walls(plate_gcode(plate)), objects, max_d)
    by_pair = {}
    for o in objects:
        if o["piece"] in ("Lower", "Upper"):
            key = json.dumps(o["params"], sort_keys=True)
            by_pair.setdefault(key, {})[o["piece"]] = o
    print("as sliced: the wall paths, plus or less one line width; the nozzle's squish is not in it")
    print(f"{'pair':28} {'stud':>6} {'socket':>7} {'mouth':>6} {'gap':>7} {'at mouth':>8} "
          f"{'stud z':>11} {'socket z':>11}")
    for key, pair in by_pair.items():
        lo, up = pair.get("Lower"), pair.get("Upper")
        st = walls[lo["entry"]] if lo else []
        so = walls[up["entry"]] if up else []
        if not st or not so:
            print(f"{key:28} no round stud or socket found")
            continue
        stud = sorted(d for _, d, _ in st)[len(st) // 2]
        socket = sorted(d for _, d, _ in so)[len(so) // 2]
        mouth = min(so)[1]  # the socket's lowest layer
        zs = lambda ws: f"{min(h for h, _, _ in ws):.1f}-{max(h for h, _, _ in ws):.1f}"
        print(f"{key:28} {stud:6.3f} {socket:7.3f} {mouth:6.3f} {socket - stud:+7.3f} "
              f"{mouth - stud:+8.3f} {zs(st):>11} {zs(so):>11}")


def assign_loops(ls, groups, target, shared=False):
    """Wall loops to groups by expected loop area. A piece loop goes to the one group it is
    nearest (by ratio), so the first layer's wider line and elephant-foot shrink never hand a
    loop to two groups. A pocket loop is `shared`: a gap ladder of one shape (sheets-04g-fit2's
    middle pieces at 0, 0.025 and 0.05) all go into the same hole, so the hole goes to every
    group whose pocket it matches, not only the first."""
    out = {g: [] for g in groups}
    off = lambda a, g: abs(math.log(a / target(groups[g])))
    for lw in ls:
        a = abs(area(lw[0]))
        near = [g for g in groups if off(a, g) < 0.5]
        if near and not shared:
            near = [min(near, key=lambda g: off(a, g))]
        for g in near:
            out[g].append(lw)
    return out


def assign_objects(objs, groups, target):
    """Piece wall loops to groups, a whole slice object at a time. Each group is its own object
    on the plate, so when as many objects as groups come near a group's expected loop area, they
    pair in order of size: the biggest object with the biggest group. Loop by loop, a step
    smaller than the slicer's own offset sends every loop to one group (sheets-04g-fit3's kites
    at 0.05 and 0.075, 0.3 mm² apart, all twenty went to the 0.05). Otherwise, loop by loop."""
    mean = lambda ls: sum(abs(area(lw[0])) for lw in ls) / len(ls)
    near = {o: ls for o, ls in objs.items()
            if ls and any(abs(math.log(mean(ls) / target(groups[g]))) < 0.5 for g in groups)}
    if len(near) == len(groups) > 1:
        by_size = sorted(near, key=lambda o: mean(near[o]))
        return {g: near[o] for g, o in zip(sorted(groups, key=lambda g: target(groups[g])), by_size)}
    return assign_loops([lw for ls in near.values() for lw in ls], groups, target)


def walls_report(plate, frame, pieces, z):
    text = plate_gcode(plate)
    h, objs = gcode_walls(text, z)
    frame_label = max(objs, key=lambda o: len(objs[o]))
    pocket_loops = sorted(objs[frame_label], key=lambda lw: abs(area(lw[0])))[:-1]  # drop the rim
    piece_objs = {o: ls for o, ls in objs.items() if o != frame_label}
    loops = slice_loops(load_triangles(frame), z)
    print(f"slicer outer walls on the layer at z = {h} mm (frame object {frame_label})")
    print(f"{'group':8} {'width':>5} {'pieces':>6} {'piece edge in':>13} {'pockets':>7} "
          f"{'pocket edge in':>14} {'gap as sliced':>13}")
    def shape(poly):
        return (abs(area(poly)), perimeter(poly),
                sum(1 / math.tan(math.radians(a) / 2) for a in corners(poly)))

    groups = {}
    for path in pieces:
        m = measure(loops, load_triangles(path), z)
        if m is not None:
            groups[Path(path).stem] = (m, shape(m["_piece"]), shape(m["_pocket"]))

    piece_of = assign_objects(piece_objs, groups, lambda s: s[1][0] - s[1][1] * 0.21)
    pocket_of = assign_loops(pocket_loops, groups, lambda s: s[2][0] + s[2][1] * 0.21, shared=True)
    for g, (m, (A, P, k), (Ah, Ph, kh)) in groups.items():
        mine, holes = piece_of[g], pocket_of[g]
        if not mine or not holes:
            print(f"{g:8} no matching wall loops on this layer")
            continue
        w = mine[0][1]
        d_in = [offset_by_area(A, P, k, abs(area(l)), grow=False) for l, _ in mine]
        d_out = [offset_by_area(Ah, Ph, kh, abs(area(l)), grow=True) for l, _ in holes]
        e_piece = sum(d_in) / len(d_in) - w / 2   # the printed edge, this far inside the drawn one
        e_pocket = sum(d_out) / len(d_out) - holes[0][1] / 2
        print(f"{g:8} {w:5.2f} {len(mine):6d} {e_piece:+13.3f} {len(holes):7d} "
              f"{e_pocket:+14.3f} {m['gap_mean'] + e_piece + e_pocket:+13.3f}")


def report(frame, pieces, z, as_json):
    loops = slice_loops(load_triangles(frame), z)
    out = {}
    for path in pieces:
        out[Path(path).stem] = measure(loops, load_triangles(path), z)
    if as_json:
        print(json.dumps({g: m and {k: v for k, v in m.items() if not k.startswith("_")}
                          for g, m in out.items()}, indent=2))
        return
    print(f"cut at z = {z} mm")
    print(f"{'group':8} {'n':>3} {'gap min':>8} {'mean':>7} {'max':>7} {'area':>8} {'perim':>7} "
          f"{'P/A':>6} {'tip':>6} {'pocket':>7} {'span':>7} {'ratio':>8}")
    for name, m in out.items():
        if m is None:
            print(f"{name:8} no piece sits in a pocket at this height")
            continue
        print(f"{name:8} {m['pieces']:3d} {m['gap_min']:8.3f} {m['gap_mean']:7.3f} {m['gap_max']:7.3f} "
              f"{m['area']:8.1f} {m['perimeter']:7.1f} {m['p_over_a']:6.3f} {m['piece_tip']:6.1f} "
              f"{m['pocket_tip']:7.1f} {m['piece_span']:7.2f} {m['span_ratio']:8.5f}")
        print(f"{'':8}   corners (angle° gap mm): "
              + ", ".join(f"{c['angle']:.0f}° {c['gap']:+.3f}" for c in m["corners"]))


def box(x0, y0, x1, y1, z1, inward=False):
    """A closed axis-aligned box as STL-style 9-float triangles; inward flips the winding."""
    v = [(x, y, z) for z in (0, z1) for y in (y0, y1) for x in (x0, x1)]
    quads = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    tris = []
    for a, b, c, d in quads:
        for t in ((a, b, c), (a, c, d)):
            t = t[::-1] if inward else t
            tris.append(tuple(k for i in t for k in v[i]))
    return tris


def self_test():
    frame = box(-20, -20, 20, 20, 4) + box(-5, -5, 5, 5, 4, inward=True)  # a slab, a 10 mm hole
    loops = slice_loops(frame, 2.0)
    loose = measure(loops, box(-4.9, -4.9, 4.9, 4.9, 4), 2.0)
    tight = measure(loops, box(-5.1, -5.1, 5.1, 5.1, 4), 2.0)
    away = measure(loops, box(30, 30, 35, 35, 4), 2.0)
    checks = [
        ("cut finds the slab's outline and its hole", len(loops) == 2),
        ("a piece 0.1 mm in from each face has a 0.1 mm gap",
         loose and abs(loose["gap_min"] - 0.1) < 1e-6 and abs(loose["gap_max"] - 0.1) < 1e-6),
        # Its faces poke 0.1 into the wall and its corners 0.1·√2 past the pocket's corners.
        ("a piece 0.1 mm out past each face reads -0.1, its corners -0.141",
         tight and abs(tight["gap_max"] + 0.1) < 1e-6 and abs(tight["gap_min"] + 0.1 * 2 ** 0.5) < 1e-6),
        ("a square's corners are 90 degrees", loose and abs(loose["piece_tip"] - 90) < 1e-6),
        ("a piece away from every pocket is not matched", away is None),
    ]
    # Two pieces of one shape at two gaps, laddered against one hole: each piece loop goes to
    # its own group, and the one hole goes to both.
    sq = lambda s: [(-s, -s), (s, -s), (s, s), (-s, s)]
    groups = {"g0": (None, (100.0, 40.0, 0), (100.0, 40.0, 0)),
              "g1": (None, (96.0, 39.2, 0), (100.0, 40.0, 0))}
    pieces = assign_loops([(sq(5), 0.4), (sq(4.9), 0.4)], groups, lambda s: s[1][0])
    holes = assign_loops([(sq(5), 0.4)], groups, lambda s: s[2][0], shared=True)
    checks += [
        ("a ladder's piece loops go one to each group",
         [len(pieces["g0"]), len(pieces["g1"])] == [1, 1] and pieces["g1"][0][0] == sq(4.9)),
        ("a ladder's one hole goes to every group", [len(holes["g0"]), len(holes["g1"])] == [1, 1]),
    ]
    # The same ladder sliced with every loop 0.2 mm bigger, as two objects, beside a far piece:
    # loop by loop, both 10.2 (104) and 10.0 (100) are nearest g0; by object, each to its own.
    sliced = {"7": [(sq(5.1), 0.4)] * 3, "8": [(sq(5.0), 0.4)] * 3, "9": [(sq(20), 0.4)]}
    by_obj = assign_objects(sliced, groups, lambda s: s[1][0])
    checks += [
        ("a ladder sliced with a common offset pairs object to group by size",
         by_obj["g0"] == sliced["7"] and by_obj["g1"] == sliced["8"]),
    ]
    # A 2 mm stud on a lower at (10, 0) and a 2.1 mm socket on an upper at (40, 0), as wall
    # paths 0.42 wide: the stud's path is 1.58 across, the socket's 2.52. A square letter on
    # the lower is not round and is left out.
    ring = lambda cx, d: [(cx + d / 2 * math.cos(i * math.pi / 90), d / 2 * math.sin(i * math.pi / 90))
                          for i in range(180)]
    objs = [{"entry": "c1", "piece": "Lower", "x": 10, "y": 0},
            {"entry": "c2", "piece": "Upper", "x": 40, "y": 0}]
    layers = {0.4: {"1": [(ring(10, 1.58), 0.42), ([(9, 3), (10, 3), (10, 4), (9, 4)], 0.42)],
                    "2": [(ring(40, 2.52), 0.42)]}}
    got = round_walls(layers, objs, 4.0)
    checks += [
        ("a stud's printed edge is its path plus one line width",
         len(got["c1"]) == 1 and abs(got["c1"][0][1] - 2.0) < 1e-3),
        ("a socket's printed edge is its path less one line width",
         len(got["c2"]) == 1 and abs(got["c2"][0][1] - 2.1) < 1e-3),
    ]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return all(ok for _, ok in checks)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--self-test"]:
        sys.exit(0 if self_test() else 1)
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    z = 2.0
    if "--z" in a:
        i = a.index("--z")
        z = float(a[i + 1])
        del a[i:i + 2]
    if len(a) == 3 and a[0] == "studs":
        studs_report(a[1], a[2], 4.0)
        sys.exit(0)
    if len(a) >= 4 and a[0] == "walls":
        walls_report(a[1], a[2], a[3:], z)
        sys.exit(0)
    if len(a) < 2:
        sys.exit(__doc__)
    report(a[0], a[1:], z, as_json)
