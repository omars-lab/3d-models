#!/usr/bin/env python3
"""grid_plate_test.py — regression guard for grid_plate.py (no slicer needed, runs in ~1s).

WHY THIS EXISTS (graduation rule, CLAUDE.md): two defects were found by eye on a real plate and fixed —
  (1) the plate's object was named after a mktemp token (grid-plate.XXXXXX.…) that leaked into the
      BambuStudio GUI, and (2) `validate sliced --expect-objects N` checks the COUNT but never the
      placement, so a wrong pitch or an overlapping / off-bed grid would pass it. This test locks in the
      fix and covers the load-bearing property a count check cannot: the grid is EVEN, non-overlapping,
      and inside the bed. Run: python3 grid_plate_test.py  (exit 0 = pass).
"""
import os
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLACER = os.path.join(HERE, "grid_plate.py")


def write_cube_stl(path, size, origin=(0.0, 0.0, 0.0)):
    """Write a minimal binary-STL axis-aligned cube of edge `size` at `origin` (12 triangles)."""
    ox, oy, oz = origin
    s = size
    v = [
        (ox, oy, oz), (ox + s, oy, oz), (ox + s, oy + s, oz), (ox, oy + s, oz),
        (ox, oy, oz + s), (ox + s, oy, oz + s), (ox + s, oy + s, oz + s), (ox, oy + s, oz + s),
    ]
    faces = [
        (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6), (0, 4, 5), (0, 5, 1),
        (1, 5, 6), (1, 6, 2), (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0),
    ]
    with open(path, "wb") as fh:
        fh.write(b"\0" * 80)
        fh.write(struct.pack("<I", len(faces)))
        for a, b, c in faces:
            fh.write(struct.pack("<3f", 0.0, 0.0, 0.0))
            for idx in (a, b, c):
                fh.write(struct.pack("<3f", *v[idx]))
            fh.write(struct.pack("<H", 0))


def parse_3mf(path):
    """Return (object_name, [(tx,ty,tz), …]) from a grid .3mf."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("3D/3dmodel.model").decode("utf-8")
    root = ET.fromstring(xml)
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    obj = root.find(".//m:resources/m:object", ns)
    name = obj.get("name")
    items = root.findall(".//m:build/m:item", ns)
    translations = []
    for it in items:
        t = [float(x) for x in it.get("transform").split()]
        translations.append((t[9], t[10], t[11]))
    return name, translations


def approx(a, b, tol=1e-3):
    return abs(a - b) <= tol


def main():
    fails = []
    with tempfile.TemporaryDirectory() as d:
        model = os.path.join(d, "TestCube.stl")
        # A cube NOT at the origin, to prove the placer centres by the mesh's own bbox, not by (0,0).
        size, origin = 20.0, (5.0, 7.0, 3.0)
        write_cube_stl(model, size, origin)
        out = os.path.join(d, "grid.3mf")
        rows, cols, bed = 2, 3, 100.0
        r = subprocess.run(
            [sys.executable, PLACER, model, "--out", out, "--rows", str(rows), "--cols", str(cols),
             "--bed", str(bed)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(r.stdout + r.stderr)
            sys.exit("placer exited non-zero")

        name, trans = parse_3mf(out)

        # (1) object name is the model basename, NOT a temp token — the leak that was found by eye.
        if name != "TestCube":
            fails.append(f"object name is {name!r}, expected 'TestCube'")

        # (2) instance count == rows*cols.
        if len(trans) != rows * cols:
            fails.append(f"{len(trans)} instances, expected {rows * cols}")

        # (3) even grid: each instance's CENTRE sits at pitch*(i+0.5); pitch = bed/N. The placer
        #     translates by (cell_centre - mesh_centre); mesh centre = origin + size/2.
        pitch_x, pitch_y = bed / cols, bed / rows
        mcx, mcy = origin[0] + size / 2, origin[1] + size / 2
        got_centres = sorted((round(tx + mcx, 3), round(ty + mcy, 3)) for tx, ty, _ in trans)
        want_centres = sorted(
            (round(pitch_x * (c + 0.5), 3), round(pitch_y * (rw + 0.5), 3))
            for rw in range(rows) for c in range(cols)
        )
        if got_centres != want_centres:
            fails.append(f"grid centres {got_centres} != expected {want_centres}")

        # (4) no overlap and inside the bed: every instance's footprint bbox is within [0,bed] and
        #     adjacent centres are at least `size` apart (pitch - size = gap >= 0).
        for tx, ty, tz in trans:
            lo_x, lo_y = origin[0] + tx, origin[1] + ty
            if lo_x < -1e-6 or lo_y < -1e-6 or lo_x + size > bed + 1e-6 or lo_y + size > bed + 1e-6:
                fails.append(f"instance at ({lo_x:.2f},{lo_y:.2f}) escapes the {bed:.0f} bed")
                break
        if pitch_x < size or pitch_y < size:
            fails.append(f"pitch {pitch_x:.1f}x{pitch_y:.1f} < footprint {size} — pieces would overlap")

        # (5) base dropped to z=0 (tz = -min_z of the mesh = -origin_z).
        if not all(approx(tz, -origin[2]) for _, _, tz in trans):
            fails.append("z translation does not drop the base to the plate (z=0)")

        # (6) the overlap guard fires: a grid too dense for the bed must be REFUSED, not emitted.
        dense = subprocess.run(
            [sys.executable, PLACER, model, "--out", os.path.join(d, "x.3mf"),
             "--rows", "10", "--cols", "10", "--bed", str(bed)],
            capture_output=True, text=True,
        )
        if dense.returncode == 0:
            fails.append("a 10x10 grid of 20mm cubes on a 100mm bed should be refused, but succeeded")

    if fails:
        print("FAIL:")
        for f in fails:
            print(f"  ✗ {f}")
        sys.exit(1)
    print("grid_plate_test: OK — name, count, even spacing, in-bed, no-overlap, z-drop, overlap-refusal")


if __name__ == "__main__":
    main()
