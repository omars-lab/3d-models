#!/usr/bin/env python3
"""How much plastic each piece on a sliced plate lays on one layer, and per mm of line.

A per-piece slicer setting is only proven when the G-code changes, not when the project file says so:
Studio drops a key it does not take without a word, and a project synced to another printer once reset
a per-piece first-layer flow to 1.00 (forum 256312, post #32). This reads the plate's own G-code and
gives, for each piece on the chosen layer, the filament pushed (E, mm), the length of line it laid,
and E per mm of line, by feature (outer wall, inner wall, bottom surface, gap infill …). Two copies of
one shape with flow 1.00 and 1.05 then differ by about 5% in E per mm, whatever way each is turned.

Pieces are named by the compose bed map beside the plate (`<plate>.bedmap.json`) when there is one,
else by the file name inside the slice. Each piece's own slicer settings, from the slice, are listed
next to it.

    python3 .claude/skills/print-model/scripts/layer_extrusion.py build/plates/<name>.plate.3mf [--layer 1] [--json]
    python3 .claude/skills/print-model/scripts/layer_extrusion.py --self-test
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

WORD = re.compile(r"([A-Z])(-?\d*\.?\d+)")
START = "; start printing object, unique label id:"
STOP = "; stop printing object, unique label id:"
OWN_KEYS = {"name", "extruder"}  # object metadata that is not a slicer setting


def arc_length(x0, y0, x1, y1, i, j, clockwise):
    """Length of a G2 (clockwise) or G3 arc from (x0, y0) to (x1, y1) around (x0 + i, y0 + j)."""
    cx, cy = x0 + i, y0 + j
    r = math.hypot(i, j)
    a0 = math.atan2(y0 - cy, x0 - cx)
    a1 = math.atan2(y1 - cy, x1 - cx)
    sweep = a0 - a1 if clockwise else a1 - a0
    if sweep <= 0:
        sweep += 2 * math.pi
    return r * sweep


def measure(gcode: str, layer: int) -> dict[str, dict[str, dict[str, float]]]:
    """{label id: {feature: {"e": mm of filament, "len": mm of line}}} on layer `layer` (1 = first).

    Counts only moves that push filament (E > 0), so travel and retraction drop out. Assumes relative E
    (M83), which Bambu's X2D G-code uses; absolute E (M82) on a printing layer is refused."""
    out: dict[str, dict[str, dict[str, float]]] = {}
    n = 0
    obj = None
    feature = "?"
    x = y = 0.0
    absolute_e = False
    for raw in gcode.splitlines():
        line = raw.strip()
        if line.startswith("; CHANGE_LAYER"):
            n += 1
            if n > layer:
                break
            continue
        if line.startswith(START):
            obj = line[len(START):].strip()
            continue
        if line.startswith(STOP):
            obj = None
            continue
        if line.startswith("; FEATURE:"):
            feature = line.split(":", 1)[1].strip()
            continue
        code = line.split(";", 1)[0].strip()
        if not code:
            continue
        if code.startswith("M82"):
            absolute_e = True
        elif code.startswith("M83"):
            absolute_e = False
        cmd = code.split()[0]
        if cmd not in ("G0", "G1", "G2", "G3"):
            continue
        w = {k: float(v) for k, v in WORD.findall(code[len(cmd):])}
        nx, ny = w.get("X", x), w.get("Y", y)
        e = w.get("E", 0.0)
        moved = (nx, ny) != (x, y)  # a push with no move refills after a retraction; it lays no line
        if n == layer and obj is not None and e > 0 and moved:
            if absolute_e:
                raise SystemExit("layer_extrusion: absolute E (M82) on the measured layer; only relative E is read")
            if cmd in ("G2", "G3"):
                length = arc_length(x, y, nx, ny, w.get("I", 0.0), w.get("J", 0.0), cmd == "G2")
            else:
                length = math.hypot(nx - x, ny - y)
            f = out.setdefault(obj, {}).setdefault(feature, {"e": 0.0, "len": 0.0})
            f["e"] += e
            f["len"] += length
        x, y = nx, ny
    return out


def plate_parts(plate: Path) -> tuple[str, dict[str, str], dict[str, dict[str, str]]]:
    """The plate's G-code, {label id: object file name}, and {object file name: its own settings}."""
    with zipfile.ZipFile(plate) as z:
        gcode_name = next(n for n in z.namelist() if re.fullmatch(r"Metadata/plate_\d+\.gcode", n))
        gcode = z.read(gcode_name).decode("utf-8", "replace")
        names = {
            o.get("identify_id"): o.get("name")
            for o in ET.fromstring(z.read("Metadata/slice_info.config")).iter("object")
        }
        settings: dict[str, dict[str, str]] = {}
        for o in ET.fromstring(z.read("Metadata/model_settings.config")).iter("object"):
            own = {m.get("key"): m.get("value") for m in o.findall("metadata")}
            settings[own.get("name", "")] = {k: v for k, v in own.items() if k and k not in OWN_KEYS}
    return gcode, names, settings


def bed_labels(plate: Path) -> dict[str, str]:
    """{iteration file name: the recipe's label} from compose's bed map, when it sits beside the plate."""
    bedmap = plate.with_name(plate.name.removesuffix(".3mf") + ".bedmap.json")
    if not bedmap.exists():
        return {}
    return {f"{o['iteration']}.stl": o.get("label") or o["entry"] for o in json.loads(bedmap.read_text())["objects"]}


def report(plate: Path, layer: int) -> list[dict]:
    gcode, names, settings = plate_parts(plate)
    labels = bed_labels(plate)
    rows = []
    for oid, feats in measure(gcode, layer).items():
        name = names.get(oid, oid)
        e = sum(f["e"] for f in feats.values())
        length = sum(f["len"] for f in feats.values())
        rows.append(
            {
                "piece": labels.get(name, name),
                "label_id": oid,
                "settings": settings.get(name, {}),
                "e_mm": round(e, 3),
                "line_mm": round(length, 1),
                "e_per_mm": round(e / length, 5) if length else 0.0,
                "features": {k: {"e_per_mm": round(v["e"] / v["len"], 5) if v["len"] else 0.0, "line_mm": round(v["len"], 1)} for k, v in feats.items()},
            }
        )
    return rows


def print_rows(rows: list[dict], layer: int) -> None:
    base = next((r for r in rows if not r["settings"]), None)
    print(f"layer {layer}: plastic per piece (E per mm of line; vs = against the first piece with no settings of its own)")
    for r in rows:
        vs = f"  vs {r['e_per_mm'] / base['e_per_mm']:.3f}" if base and base["e_per_mm"] else ""
        own = ", ".join(f"{k}={v}" for k, v in r["settings"].items()) or "plate's own"
        print(f"  {r['piece']:<14} E {r['e_mm']:>9.3f} mm  line {r['line_mm']:>8.1f} mm  {r['e_per_mm']:.5f}/mm{vs}  [{own}]")
        for k, v in sorted(r["features"].items()):
            fvs = ""
            if base and k in base["features"] and base["features"][k]["e_per_mm"]:
                fvs = f"  vs {v['e_per_mm'] / base['features'][k]['e_per_mm']:.3f}"
            print(f"      {k:<16} {v['e_per_mm']:.5f}/mm over {v['line_mm']:>7.1f} mm{fvs}")


SAMPLE = """\
M83
; CHANGE_LAYER
; start printing object, unique label id: 1
; FEATURE: Outer wall
G1 X0 Y0
G1 X10 Y0 E0.4
G1 X10 Y10 E0.4
G1 E-0.8
G1 X20 Y20
G1 E0.8
; stop printing object, unique label id: 1
; start printing object, unique label id: 2
; FEATURE: Outer wall
G1 X30 Y0
G1 X40 Y0 E0.42
G3 X30 Y0 I-5 J0 E0.6597
; stop printing object, unique label id: 2
; CHANGE_LAYER
; start printing object, unique label id: 1
G1 X0 Y0 E9
"""


def self_test() -> None:
    m = measure(SAMPLE, 1)
    a, b = m["1"]["Outer wall"], m["2"]["Outer wall"]
    assert abs(a["len"] - 20) < 1e-9 and abs(a["e"] - 0.8) < 1e-9, a  # travel and retraction left out
    assert abs(b["len"] - (10 + 5 * math.pi)) < 1e-9, b  # a half circle, counter-clockwise, radius 5
    ratio = (b["e"] / b["len"]) / (a["e"] / a["len"])
    assert abs(ratio - 1.05) < 1e-3, ratio  # PASS: 5% more per mm reads as 1.05
    assert measure(SAMPLE, 2) == {"1": {"Outer wall": {"e": 9.0, "len": 30.0}}}  # layer 2 kept apart from layer 1
    try:  # FAIL: absolute E on the measured layer is refused, not misread
        measure(SAMPLE.replace("M83", "M82"), 1)
    except SystemExit:
        pass
    else:
        raise AssertionError("absolute E was read")
    print("layer_extrusion self-test: ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("plate", nargs="?", type=Path, help="a sliced .3mf")
    ap.add_argument("--layer", type=int, default=1, help="which layer, 1 = the first (default)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
        return 0
    if not a.plate:
        ap.error("give a sliced .3mf, or --self-test")
    rows = report(a.plate, a.layer)
    if a.json:
        print(json.dumps(rows, indent=2))
    else:
        print_rows(rows, a.layer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
