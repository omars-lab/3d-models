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

An object whose face has holes is a half (its openings for the loose pieces) and is skipped; a
piece with its id carved in its face also has a hole, a few mm², so a half is told by its holes
taking more than a quarter of its outline (HOLE_SHARE). Before that rule every piece with an id
was skipped as a half, and the first run on split-08 checked only its stars and kites.

A plate that tests the bite on purpose (split-08 keeps split-06's discs as its control) says so in
its recipe with a top-level `ledge_bitten_by_design: "<why>"`. Given `--recipe`, such a plate
passes only when a piece IS bitten, so the check still tests that the experiment is what it says.

`--draw DIR` writes one picture per set (the bed map's `group:`, else one per object): each piece's
face grey, its hidden ledge orange, and each bitten corner ringed blue with how far its ledge reaches.

    python3 .claude/skills/place-pins/scripts/ledge_check.py build/plates/split-06.plate.3mf
    python3 .claude/skills/place-pins/scripts/ledge_check.py build/plates/split-08.plate.3mf \
        --recipe docs/design/plates/split-08.yaml --draw docs/design/plates/split-08-media
    python3 .claude/skills/place-pins/scripts/ledge_check.py --self-test
"""
import argparse
import json
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


def bed_names(path):
    """{"object_N": (label, group)} from the bed map `bambu slice compose` writes beside the plate,
    joined through the build objects of 3D/3dmodel.model; {} when either is missing."""
    side = Path(re.sub(r"\.3mf$", "", str(path), flags=re.I) + ".bedmap.json")
    if not side.exists():
        return {}
    rows = {str(r["object"]): (r.get("label"), r.get("group")) for r in json.loads(side.read_text())["objects"]}
    with zipfile.ZipFile(path) as z:
        if "3D/3dmodel.model" not in z.namelist():
            return {}
        model = z.read("3D/3dmodel.model").decode()
    out = {}
    for oid, body in re.findall(r'<object id="([^"]+)"[^>]*>(.*?)</object>', model, re.S):
        for file in re.findall(r'path="[^"]*?(object_\d+)\.model"', body):
            if oid in rows:
                out[file] = rows[oid]
    return out


def recipe_why(path):
    """The recipe's `ledge_bitten_by_design:` reason, or None."""
    m = re.search(r'^ledge_bitten_by_design:\s*"?(.*?)"?\s*$', Path(path).read_text(), re.M)
    return m.group(1) if m and m.group(1) else None


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


def net_area(loops):
    """The largest loop's area less every other loop's: holes subtract."""
    sizes = sorted((abs(area(lp)) for lp in loops), reverse=True)
    return sizes[0] - sum(sizes[1:]) if sizes else 0.0


# A half is a lattice: its openings for the loose pieces are most of its outline. A carved id is a
# few mm² in a piece's face. Holes past this share of the outline mean a half, not a piece.
HOLE_SHARE = 0.25


def check_piece(verts, tris, tol):
    """None for a component that is not a loose piece, else a dict of what was measured."""
    zs = [verts[i][2] for t in tris for i in t]
    zlo, zhi = min(zs), max(zs)
    if zhi - zlo < 1.0:
        return None
    face_loops = sorted(section(verts, tris, zlo + 0.3), key=lambda lp: abs(area(lp)), reverse=True)
    if not face_loops:
        return None
    outer = abs(area(face_loops[0]))
    if outer - net_area(face_loops) > HOLE_SHARE * outer:
        return None  # a half with openings in it, not a piece (a carved id is a small hole, kept)
    face = corners(face_loops[0])
    if area(face) < 0:
        face = face[::-1]
    face_area = area(face)
    best_z, best_loops, best_area = None, None, face_area
    for k in range(40):
        z = zlo + (zhi - zlo) * (k + 0.5) / 40
        loops = section(verts, tris, z)
        a = net_area(loops)
        if a > best_area * 1.02:
            best_z, best_loops, best_area = z, loops, a
    cx = sum(p[0] for p in face) / len(face)
    cy = sum(p[1] for p in face) / len(face)
    result = {"centre": (cx, cy), "corners": len(face), "ledge_z": best_z, "face": face, "ledge": best_loops or []}
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


def check(path, tol, why=None, draw=None):
    """Exit 0 when no piece is bitten, 1 when one is. With `why` (the recipe tests the bite on
    purpose) the other way round: 0 only when a piece is bitten."""
    names = bed_names(path)
    groups = defaultdict(int)
    sets = defaultdict(list)
    pieces = bitten = 0
    for obj, verts, tris in read_objects(path):
        label, group = names.get(obj, (None, None))
        name = f"{obj} ({label})" if label else obj
        for tris_c in components(verts, tris):
            r = check_piece(verts, tris_c, tol)
            if r is None:
                continue
            shape, verdict, bad = describe(r)
            pieces += 1
            bitten += bad
            groups[(name, shape, verdict)] += 1
            sets[group or obj].append((label or obj, r))
    for (name, shape, verdict), count in groups.items():
        print(f"{name}: {count} × {shape}: {verdict}")
    print(f"{pieces} loose pieces, {bitten} with a bitten ledge (tolerance {tol} mm)")
    if draw:
        for title, rows in sets.items():
            print("wrote", draw_set(Path(draw), title, rows, tol))
    if why is None:
        return 1 if bitten else 0
    if bitten:
        print(f"bitten by design, as the recipe says: {why}")
        return 0
    print(f"the recipe says this plate is bitten by design ({why}), but no piece is: the test is not what it says")
    return 1


# --- the pictures: one per set, each piece's face, its ledge and its bitten corners -----------------

DRAW_PX = 40      # px per mm: a 0.17 mm ledge is 7 px
DRAW_PAD = 1.5    # mm round each piece
DRAW_TOP = 80     # px for the set's title
DRAW_FOOT = 70    # px for the key under the pieces


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def draw_set(out, title, rows, tol):
    """One PNG of a set's pieces side by side, each centred on its face, named, with its bites."""
    from PIL import Image, ImageDraw, ImageFont  # only the pictures need PIL
    boxes = []
    for _, r in rows:
        pts = [(x - r["centre"][0], y - r["centre"][1]) for lp in r["ledge"] + [r["face"]] for x, y in lp]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        boxes.append((min(xs) - DRAW_PAD, min(ys) - DRAW_PAD, max(xs) + DRAW_PAD, max(ys) + DRAW_PAD))
    w = round(sum(b[2] - b[0] for b in boxes) * DRAW_PX) + 20
    tall = max(b[3] - b[1] for b in boxes)
    h = DRAW_TOP + round(tall * DRAW_PX) + 40 + DRAW_FOOT
    w = max(w, 900)
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)
    big, small = ImageFont.load_default(size=30), ImageFont.load_default(size=20)
    d.text((14, DRAW_TOP / 2), title, fill=(30, 30, 30), font=big, anchor="lm")
    left = 10
    for (label, r), (bx0, by0, bx1, by1) in zip(rows, boxes):
        cx, cy = r["centre"]
        ox = left - bx0 * DRAW_PX
        oy = DRAW_TOP + 30 + by1 * DRAW_PX
        f = lambda p: (ox + (p[0] - cx) * DRAW_PX, oy - (p[1] - cy) * DRAW_PX)
        for lp in r["ledge"]:
            d.polygon([f(p) for p in lp], fill=(245, 170, 80))
        d.polygon([f(p) for p in r["face"]], fill=(150, 150, 150))
        for b in r["bites"]:
            x, y = f((cx + b["at"][0], cy + b["at"][1]))
            d.ellipse([x - 26, y - 26, x + 26, y + 26], outline=(40, 90, 220), width=4)
            d.text((x, y - 34), f"{b['reach']:.2f}", fill=(40, 90, 220), font=small, anchor="md")
        d.text((ox, DRAW_TOP + 14), label, fill=(30, 30, 30), font=small, anchor="mm")
        left += (bx1 - bx0) * DRAW_PX
    d.text((14, h - DRAW_FOOT / 2),
           f"grey: the face   orange: the hidden ledge   blue ring: a corner whose ledge falls more than "
           f"{tol} mm short, with how far it reaches (mm)", fill=(80, 80, 80), font=small, anchor="lm")
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"ledges-{slug(title)}.png"
    img.save(path)
    return path


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


# A carved id in the face: a small triangle round the kite's centre, 0.6 mm deep, so the outline
# 0.3 mm up has a second loop in it (split-08's hex and outer pieces, which the check once skipped).
MARK = [(-0.6, 0.0), (0.6, 0.0), (0.0, 1.0)]


def write_plate(path, ledge, mark=False):
    layers = [(FACE, 0.0, 1.5), (ledge, 1.5, 2.5), (FACE, 2.5, 4.0)] + ([(MARK, 0.0, 0.6)] if mark else [])
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
        # A carved id must not hide a piece from the check: the bitten kite with a mark still fails.
        p = Path(d) / "bitten-id.3mf"
        write_plate(p, BITTEN, mark=True)
        print("--- bitten kite with an id carved in its face")
        got = check(p, 0.25)
        ok &= got == 1
        print(f"{'PASS' if got == 1 else 'FAIL'}: bitten kite with an id exits {got}, expected 1")
        # A recipe that tests the bite on purpose: the bitten kite passes, the clean one fails.
        recipe = Path(d) / "by-design.yaml"
        recipe.write_text('bed: x2d\nledge_bitten_by_design: "the control keeps split-06\'s discs"\nitems: []\n')
        why = recipe_why(recipe)
        for name, want in [("bitten", 0), ("clean", 1)]:
            print(f"--- {name} kite, recipe says bitten by design")
            got = check(Path(d) / f"{name}.3mf", 0.25, why=why)
            verdict = "PASS" if got == want else "FAIL"
            ok &= got == want
            print(f"{verdict}: {name} kite with the by-design recipe exits {got}, expected {want}")
        # The picture: one per set, written where --draw says.
        check(Path(d) / "bitten.3mf", 0.25, draw=Path(d) / "pics")
        drawn = sorted(p.name for p in (Path(d) / "pics").glob("*.png"))
        ok &= drawn == ["ledges-object-1.png"]
        print(f"{'PASS' if drawn == ['ledges-object-1.png'] else 'FAIL'}: --draw writes one picture per set: {drawn}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("plate", nargs="?", help="a sliced plate, build/plates/<name>.plate.3mf")
    ap.add_argument("--tol", type=float, default=0.25,
                    help="how far short of its own width the ledge may fall at a corner, mm")
    ap.add_argument("--recipe", metavar="YAML",
                    help="the plate's recipe; `ledge_bitten_by_design:` in it turns the verdict round")
    ap.add_argument("--draw", metavar="DIR", help="write one picture per set into DIR")
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
        why = recipe_why(a.recipe) if a.recipe else None
        return check(a.plate, a.tol, why=why, draw=a.draw)
    except (OSError, zipfile.BadZipFile) as e:
        print(f"cannot read {a.plate}: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
