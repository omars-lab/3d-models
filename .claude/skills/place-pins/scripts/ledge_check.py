#!/usr/bin/env python3
"""Does a pin disc bite a loose piece's hidden ledge?

Each loose piece of a split coaster has a wider rim (its ledge, or flange) at mid-height that sits
in the groove between the two halves. Pin bosses (`stud_boss 1`) fill that groove in a disc round
each pin and notch every ledge the disc reaches. On split-06 the discs flattened the pink hex
pieces' points and clipped their shoulders, so they wiggled while the green outer pieces, with the
same face, held (docs/design/plates/split-06.md, "What you saw off the bed").

This reads a sliced plate (.3mf) and, for every loose piece, checks that its ledge reaches past its
face by the ledge's own width all the way round: along each side and round each corner. A corner
whose ledge falls short by more than `--tol` is a bite. Exit 0 when no piece is bitten, 1 when one
is, 2 when the file cannot be read.

    python3 .claude/skills/place-pins/scripts/ledge_check.py build/plates/split-06.plate.3mf
    python3 .claude/skills/place-pins/scripts/ledge_check.py --self-test
"""
import argparse
import math
import re
import statistics
import sys
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

VERTEX = re.compile(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"')
TRIANGLE = re.compile(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"')
OBJECT_FILE = re.compile(r"3D/Objects/object_(\d+)\.model$")


def read_objects(path):
    """Every mesh in the .3mf, as (label, vertices, triangles), vertices merged by position."""
    out = []
    with zipfile.ZipFile(path) as z:
        names = sorted((n for n in z.namelist() if OBJECT_FILE.search(n)),
                       key=lambda n: int(OBJECT_FILE.search(n).group(1)))
        for name in names:
            xml = z.read(name).decode()
            raw = [tuple(map(float, m)) for m in VERTEX.findall(xml)]
            index, verts, remap = {}, [], []
            for v in raw:
                key = tuple(round(c, 5) for c in v)
                if key not in index:
                    index[key] = len(verts)
                    verts.append(v)
                remap.append(index[key])
            tris = [tuple(remap[int(i)] for i in t) for t in TRIANGLE.findall(xml)]
            out.append((f"object_{OBJECT_FILE.search(name).group(1)}", verts, tris))
    return out


def components(verts, tris):
    parent = list(range(len(verts)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b, c in tris:
        parent[find(a)] = find(b)
        parent[find(b)] = find(c)
    groups = defaultdict(list)
    for t in tris:
        groups[find(t[0])].append(t)
    return list(groups.values())


def section(verts, tris, z):
    """The outline loops where the plane at height z cuts the mesh."""
    segs = []
    for tri in tris:
        pts = [verts[i] for i in tri]
        cut = []
        for i in range(3):
            p, q = pts[i], pts[(i + 1) % 3]
            if (p[2] - z) * (q[2] - z) < 0:
                t = (z - p[2]) / (q[2] - p[2])
                cut.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        if len(cut) == 2:
            segs.append(cut)
    nbr = defaultdict(list)
    key = lambda p: (round(p[0], 4), round(p[1], 4))
    for a, b in segs:
        nbr[key(a)].append(key(b))
        nbr[key(b)].append(key(a))
    seen, loops = set(), []
    for start in list(nbr):
        if start in seen:
            continue
        loop, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [n for n in nbr[cur] if n != prev and n not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            loop.append(cur)
        if len(loop) >= 3:
            loops.append(loop)
    return loops


def area(loop):
    return sum(loop[i - 1][0] * loop[i][1] - loop[i][0] * loop[i - 1][1] for i in range(len(loop))) / 2


def inside(pt, loops):
    hit = False
    for loop in loops:
        for i in range(len(loop)):
            (x1, y1), (x2, y2) = loop[i - 1], loop[i]
            if (y1 > pt[1]) != (y2 > pt[1]):
                if pt[0] < x1 + (pt[1] - y1) * (x2 - x1) / (y2 - y1):
                    hit = not hit
    return hit


def corners(loop, deg=12):
    """Drop points that turn less than deg degrees, so straight runs and soft arcs collapse."""
    out = loop[:]
    changed = True
    while changed and len(out) > 3:
        changed = False
        for i in range(len(out)):
            p, q, r = out[i - 1], out[i], out[(i + 1) % len(out)]
            a1 = math.atan2(q[1] - p[1], q[0] - p[0])
            a2 = math.atan2(r[1] - q[1], r[0] - q[0])
            if abs((math.degrees(a2 - a1) + 180) % 360 - 180) < deg:
                out.pop(i)
                changed = True
                break
    return out


def ray_hit(origin, direction, loops):
    """Distance along the ray to the nearest outline crossing, or None."""
    best = None
    ox, oy = origin
    dx, dy = direction
    for loop in loops:
        for i in range(len(loop)):
            (x1, y1), (x2, y2) = loop[i - 1], loop[i]
            ex, ey = x2 - x1, y2 - y1
            den = dx * ey - dy * ex
            if abs(den) < 1e-12:
                continue
            t = ((x1 - ox) * ey - (y1 - oy) * ex) / den
            u = ((x1 - ox) * dy - (y1 - oy) * dx) / den
            if t > 1e-6 and 0 <= u <= 1 and (best is None or t < best):
                best = t
    return best


def check_piece(verts, tris, tol):
    """None for a component that is not a loose piece, else a dict of what was measured."""
    zs = [verts[i][2] for t in tris for i in t]
    zlo, zhi = min(zs), max(zs)
    if zhi - zlo < 1.0:
        return None
    face_loops = section(verts, tris, zlo + 0.3)
    if len(face_loops) != 1:
        return None  # a half with holes in it, not a piece
    face = corners(face_loops[0])
    if area(face) < 0:
        face = face[::-1]
    face_area = area(face)
    best_z, best_loops, best_area = None, None, face_area
    for k in range(40):
        z = zlo + (zhi - zlo) * (k + 0.5) / 40
        loops = section(verts, tris, z)
        a = sum(abs(area(lp)) for lp in loops)
        if a > best_area * 1.02:
            best_z, best_loops, best_area = z, loops, a
    cx = sum(p[0] for p in face) / len(face)
    cy = sum(p[1] for p in face) / len(face)
    result = {"centre": (cx, cy), "corners": len(face), "ledge_z": best_z}
    if best_loops is None:
        result["width"] = 0.0
        result["bites"] = []
        return result
    n = len(face)
    normals = []
    for i in range(n):
        (x1, y1), (x2, y2) = face[i], face[(i + 1) % n]
        L = math.hypot(x2 - x1, y2 - y1)
        normals.append(((y2 - y1) / L, -(x2 - x1) / L))  # outward for a counter-clockwise loop
    widths = []
    for i in range(n):
        (x1, y1), (x2, y2) = face[i], face[(i + 1) % n]
        d = ray_hit(((x1 + x2) / 2, (y1 + y2) / 2), normals[i], best_loops)
        if d is not None:
            widths.append(d)
    width = statistics.median(widths) if widths else 0.0
    result["width"] = width
    need = width - tol
    bites = []
    for i in range(n):
        q = face[i]
        n_in, n_out = normals[i - 1], normals[i]
        a0 = math.atan2(n_in[1], n_in[0])
        sweep = (math.atan2(n_out[1], n_out[0]) - a0) % (2 * math.pi)
        if sweep > math.pi:
            continue  # a reflex corner: the two sides' offsets cover it
        worst = None
        for s in range(9):
            a = a0 + sweep * s / 8
            d = ray_hit(q, (math.cos(a), math.sin(a)), best_loops) or 0.0
            if worst is None or d < worst[0]:
                worst = (d, a)
        p, r = face[i - 1], face[(i + 1) % n]
        v1, v2 = (p[0] - q[0], p[1] - q[1]), (r[0] - q[0], r[1] - q[1])
        angle = math.degrees(math.acos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1])
                                                    / (math.hypot(*v1) * math.hypot(*v2))))))
        if worst[0] < need:
            bites.append({"at": (q[0] - cx, q[1] - cy), "angle": angle, "reach": worst[0]})
    result["bites"] = bites
    return result


def describe(r):
    """One piece's verdict, without its position, so copies of one piece read the same."""
    shape = f"{r['corners']} corners"
    if r["ledge_z"] is None:
        return shape, "no ledge", False
    if not r["bites"]:
        return shape, f"ledge {r['width']:.2f} mm all round, ok", False
    # a copy turned 180 degrees on the bed reads its corners mirrored: name them by angle and distance
    found = sorted({(round(b["angle"]), round(math.hypot(*b["at"]), 2), round(b["reach"], 2)) for b in r["bites"]})
    parts = [f"the {a}° corner {d:.2f} mm from the centre reaches {reach:.2f} mm" for a, d, reach in found]
    return shape, f"BITTEN: {'; '.join(parts)} (its sides reach {r['width']:.2f} mm)", True


def check(path, tol):
    groups = defaultdict(int)
    pieces = bitten = 0
    for label, verts, tris in read_objects(path):
        for tris_c in components(verts, tris):
            r = check_piece(verts, tris_c, tol)
            if r is None:
                continue
            shape, verdict, bad = describe(r)
            pieces += 1
            bitten += bad
            groups[(label, shape, verdict)] += 1
    for (label, shape, verdict), count in groups.items():
        print(f"{label}: {count} × {shape}: {verdict}")
    print(f"{pieces} loose pieces, {bitten} with a bitten ledge (tolerance {tol} mm)")
    return 1 if bitten else 0


# --- self-test: a kite with a clean ledge, and the same kite with its point bitten flat ------------

FACE = [(-5.57, -3.90), (0.00, -5.71), (5.57, -3.90), (5.57, 1.95), (0.00, 9.62), (-5.57, 1.95)]
CLEAN = [(-6.37, -4.49), (0.00, -6.55), (6.37, -4.49), (6.37, 2.21), (0.00, 10.98), (-6.37, 2.21)]
BITTEN = [(-6.37, -4.49), (0.00, -6.55), (6.37, -4.49), (6.37, 0.92), (6.14, 2.53),
          (0.74, 9.96), (-0.74, 9.96), (-6.14, 2.53), (-6.37, 0.92)]


def prism_model(layers):
    """A 3mf object model: polygons stacked as (polygon, z0, z1), joined through one shared centre."""
    verts, tris = [], []

    def vid(x, y, z):
        verts.append((x, y, z))
        return len(verts) - 1

    first = layers[0][0]
    cx = sum(p[0] for p in first) / len(first)
    cy = sum(p[1] for p in first) / len(first)
    for poly, z0, z1 in layers:
        lo = [vid(x, y, z0) for x, y in poly]
        hi = [vid(x, y, z1) for x, y in poly]
        c0, c1 = vid(cx, cy, z0), vid(cx, cy, z1)
        n = len(poly)
        for i in range(n):
            j = (i + 1) % n
            tris += [(lo[i], lo[j], hi[j]), (lo[i], hi[j], hi[i]), (c0, lo[j], lo[i]), (c1, hi[i], hi[j])]
    v = "".join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in verts)
    t = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tris)
    return f"<model><mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh></model>"


def write_plate(path, ledge):
    layers = [(FACE, 0.0, 1.5), (ledge, 1.5, 2.5), (FACE, 2.5, 4.0)]
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("3D/Objects/object_1.model", prism_model(layers))


def self_test():
    ok = True
    with tempfile.TemporaryDirectory() as d:
        for name, ledge, want in [("clean", CLEAN, 0), ("bitten", BITTEN, 1)]:
            p = Path(d) / f"{name}.3mf"
            write_plate(p, ledge)
            print(f"--- {name} kite")
            got = check(p, 0.25)
            verdict = "PASS" if got == want else "FAIL"
            ok &= got == want
            print(f"{verdict}: {name} kite exits {got}, expected {want}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("plate", nargs="?", help="a sliced plate, build/plates/<name>.plate.3mf")
    ap.add_argument("--tol", type=float, default=0.25,
                    help="how far short of its own width the ledge may fall at a corner, mm")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--write-fixture", metavar="DIR",
                    help="write the self-test's clean.3mf and bitten.3mf into DIR (for the send's tests)")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.write_fixture:
        for name, ledge in [("clean", CLEAN), ("bitten", BITTEN)]:
            write_plate(Path(a.write_fixture) / f"{name}.3mf", ledge)
        return 0
    if not a.plate:
        ap.error("give a plate, or --self-test")
    try:
        return check(a.plate, a.tol)
    except (OSError, zipfile.BadZipFile) as e:
        print(f"cannot read {a.plate}: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
