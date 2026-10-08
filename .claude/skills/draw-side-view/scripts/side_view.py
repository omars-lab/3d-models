#!/usr/bin/env python3
"""Draw a labeled cut-through side view of a coaster from a short YAML description.

Omar, 2026-10-08 (thread dunuoe): "do we have a good skill to draw these kinds of svgs? I enjoy
them". Until this tool, every side view was drawn by hand, one at a time, each in its own style.
This is the kit: a handful of parts (half, lip, piece, flange, pocket, air, stud, socket,
dovetail, seam, bed, arrow, dim), each placed in millimetres, painted in order, so a picture is a
dozen lines of data and every page gets the same look as the first one,
`docs/working-model/feedback-requests/2026-10-05-open-calls-media/way-a-cut-pieces.png`.

The description sits beside the picture as `<name>.side.yaml`; the picture is `<name>.svg` and
`<name>.png`. `check` re-draws every description and fails when its SVG is missing or stale, so a
picture cannot drift from the words that made it.

    side_view.py draw <spec.side.yaml> [--no-png] [--zoom 2]
    side_view.py check [--root docs]
    side_view.py kinds
    side_view.py --self-test

Painting is in order: a later part covers an earlier one. Holes (pocket, air, socket, a slot)
paint white, as the gaps do in the first picture. A part's `first` and `last` marks are drawn
right after its fill, so whatever is painted later covers them too: a rail standing on a face
hides that face's last-layer mark under its root, which is what the printer does.
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
SPEC_SUFFIX = ".side.yaml"
DRAW_CMD = "python3 .claude/skills/draw-side-view/scripts/side_view.py draw"

# --- the look, matched to way-a-cut-pieces.png ------------------------------------------------

PAGE_BG = "#f8f7f4"
HOLE = "#ffffff"
INK = "#222222"
NOTE_INK = "#444444"
LEGEND_INK = "#555555"
WARN_INK = "#c0392b"
LEADER = "#666666"
FIRST_LAYER = "#2f6fd8"
LAST_LAYER = "#e27a2a"
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"

HALF_FILL = {"lower": "#8e8a83", "upper": "#aba69f"}
HALF_WORDS = {"lower": "Dark gray: lower half of the coaster.", "upper": "Light gray: upper half."}
PIECE_COLORS = {
    "gold": "#dcaa33",
    "teal": "#3f9189",
    "pink": "#e58fb0",
    "green": "#5c9e57",
    "blue": "#4a78c2",
    "red": "#c2473b",
    "black": "#333333",
    "white": "#f1efe9",
}

DEFAULT_SCALE = (18.0, 36.0)
MIN_CELL_W = 420.0  # px; notes wrap at the column width, so a narrow drawing still gets readable lines  # px per mm across, px per mm up; the first picture's proportions
MARK_W = 4.0
TITLE_PX = 17
LEGEND_PX = 12.5
PANEL_TITLE_PX = 14
NOTE_PX = 12
LABEL_PX = 12
CHAR_EM = 0.53  # average glyph width as a share of the font size, for wrapping and fitting

# --- the kit -------------------------------------------------------------------------------------

COMMON = {"kind", "both", "first", "last", "label", "label_at", "label_side"}

KINDS: dict[str, dict] = {
    "half": {
        "keys": {"box", "side"},
        "needs": {"box", "side"},
        "about": "a coaster half (or a wall of one): `side: lower|upper`, `box: [x, z, w, h]`",
    },
    "lip": {
        "keys": {"box", "side"},
        "needs": {"box", "side"},
        "about": "a half's lip reaching over the piece: painted as its half, `side`, `box`",
    },
    "piece": {
        "keys": {"box", "color"},
        "needs": {"box"},
        "about": "a piece or a piece half: `box`, `color` (gold if left out)",
    },
    "flange": {
        "keys": {"box", "color"},
        "needs": {"box"},
        "about": "a piece's band, wider than its face block: `box`, `color`",
    },
    "pocket": {
        "keys": {"box"},
        "needs": {"box"},
        "about": "a recess cut into a half: painted white, `box`",
    },
    "air": {
        "keys": {"box"},
        "needs": {"box"},
        "about": "an air gap: painted white, `box`",
    },
    "stud": {
        "keys": {"box", "side", "color", "toward", "chamfer"},
        "needs": {"box"},
        "about": "a peg standing off a half: `box`, `side` or `color`, its free end `toward: up|down`,"
        " `chamfer` mm at that end (0.2)",
    },
    "socket": {
        "keys": {"box"},
        "needs": {"box"},
        "about": "the hole a stud goes into: painted white, `box`",
    },
    "dovetail": {
        "keys": {"at", "width", "height", "flare", "gap", "depth", "steps", "toward", "show", "side", "color"},
        "needs": {"at", "width", "height", "flare"},
        "about": "a rail in its slot: root center `at: [x, z]`, root `width`, rail `height`, `flare` mm a"
        " side wider at its top, `gap` mm a side (0), slot `depth` (height), `steps` layer mm (smooth"
        " if left out), grows `toward: up|down`, `show: both|rail|slot`, rail painted by `side` or"
        " `color`",
    },
    "seam": {
        "keys": {"line"},
        "needs": {"line"},
        "about": "where a piece is cut in two: a white dashed line, `line: [x, z, w]`",
    },
    "bed": {
        "keys": {"line", "text"},
        "needs": {"line"},
        "about": "the print bed under parts drawn as they print: `line: [x, z, w]`, `text`",
    },
    "arrow": {
        "keys": {"from", "to", "text"},
        "needs": {"from", "to"},
        "about": "a move, such as closing the halves: `from: [x, z]`, `to: [x, z]`, `text`",
    },
    "dim": {
        "keys": {"from", "to", "text", "place"},
        "needs": {"from", "to", "text"},
        "about": "a measurement: `from`, `to`, `text`, its text `place: left|right|above|below` (right)",
    },
}

SPEC_KEYS = {"title", "legend", "scale", "columns", "panels"}
PANEL_KEYS = {"title", "width", "scale", "parts", "notes", "warn"}
HOLE_KINDS = {"pocket", "air", "socket"}
BOX_KINDS = {k for k, v in KINDS.items() if "box" in v["keys"]}
LINE_KINDS = {"seam", "bed"}


class Refusal(Exception):
    """A description the kit will not draw, with the reason in plain words."""


# --- reading a description -----------------------------------------------------------------------


def _nums(value, n: int, where: str) -> list[float]:
    if not isinstance(value, list) or len(value) != n or not all(isinstance(v, (int, float)) for v in value):
        raise Refusal(f"{where}: needs {n} numbers in a list, got {value!r}")
    return [float(v) for v in value]


def _color(part: dict, where: str) -> str:
    if "color" in part:
        c = str(part["color"])
        if c in PIECE_COLORS:
            return PIECE_COLORS[c]
        if c.startswith("#") and len(c) in (4, 7):
            return c
        raise Refusal(f"{where}: color {c!r} is not one of {', '.join(PIECE_COLORS)} or a #hex")
    if "side" in part:
        return HALF_FILL[part["side"]]
    return PIECE_COLORS["gold"]


def check_part(part, where: str) -> dict:
    if not isinstance(part, dict) or "kind" not in part:
        raise Refusal(f"{where}: a part is a mapping with a `kind`, got {part!r}")
    kind = part["kind"]
    if kind not in KINDS:
        raise Refusal(f"{where}: no part kind {kind!r}; the kit has {', '.join(KINDS)}")
    spec = KINDS[kind]
    unknown = set(part) - COMMON - spec["keys"]
    if unknown:
        raise Refusal(f"{where}: {kind} has no {', '.join(sorted(unknown))}; it takes {', '.join(sorted(spec['keys'] | COMMON - {'kind'}))}")
    missing = spec["needs"] - set(part)
    if missing:
        raise Refusal(f"{where}: {kind} needs {', '.join(sorted(missing))}")
    if "side" in part and part["side"] not in HALF_FILL:
        raise Refusal(f"{where}: side is lower or upper, got {part['side']!r}")
    if kind == "dim" and part.get("place", "right") not in ("left", "right", "above", "below"):
        raise Refusal(f"{where}: a dim's text is placed left, right, above or below")
    for mark in ("first", "last"):
        faces = part.get(mark, [])
        faces = [faces] if isinstance(faces, str) else faces
        if not isinstance(faces, list) or any(f not in ("top", "bottom") for f in faces):
            raise Refusal(f"{where}: {mark} names faces, top and/or bottom, got {part.get(mark)!r}")
    if "label" in part and ("\n" in str(part["label"]) or not str(part["label"]).strip()):
        raise Refusal(f"{where}: a label is one short line")
    if part.get("label_side", "right") not in ("left", "right"):
        raise Refusal(f"{where}: a label sits left or right of the drawing, got {part.get('label_side')!r}")
    if "box" in part:
        x, z, w, h = _nums(part["box"], 4, f"{where} box")
        if w <= 0 or h <= 0:
            raise Refusal(f"{where}: a box has a width and a height above zero, got {part['box']!r}")
    if "line" in part:
        _nums(part["line"], 3, f"{where} line")
    for key in ("from", "to", "at", "label_at"):
        if key in part:
            _nums(part[key], 2, f"{where} {key}")
    if kind in ("piece", "flange", "stud", "dovetail"):
        _color(part, where)
    if kind == "stud" and part.get("toward", "up") not in ("up", "down"):
        raise Refusal(f"{where}: a stud's free end is toward up or down")
    if kind == "dovetail":
        check_dovetail(part, where)
    return part


def check_dovetail(part: dict, where: str) -> None:
    width, height, flare = (float(part[k]) for k in ("width", "height", "flare"))
    gap = float(part.get("gap", 0))
    depth = float(part.get("depth", height))
    if width <= 0 or height <= 0:
        raise Refusal(f"{where}: a dovetail has a root width and a height above zero")
    if flare <= gap:
        raise Refusal(
            f"{where}: the rail's top is {flare:g} mm a side wider than its root, no more than the"
            f" {gap:g} mm gap, so it would lift straight out of its slot; a dovetail locks only when"
            " its flare beats the gap (bikar refuses this one too)"
        )
    if depth < height:
        raise Refusal(f"{where}: the slot ({depth:g} mm) is shallower than the rail ({height:g} mm), so the cut faces could not close")
    if part.get("toward", "up") not in ("up", "down"):
        raise Refusal(f"{where}: a dovetail grows toward up or down")
    if part.get("show", "both") not in ("both", "rail", "slot"):
        raise Refusal(f"{where}: show is both, rail or slot")
    if "steps" in part:
        steps = float(part["steps"])
        layers = height / steps if steps > 0 else 0
        if steps <= 0 or abs(layers - round(layers)) > 1e-6 or round(layers) < 2:
            raise Refusal(f"{where}: steps ({part['steps']!r}) must split the {height:g} mm rail into two or more whole layers")
        slot_layers = depth / steps
        if abs(slot_layers - round(slot_layers)) > 1e-6:
            raise Refusal(f"{where}: steps ({steps:g}) must split the {depth:g} mm slot into whole layers")


@dataclass
class Panel:
    title: str
    width: float
    scale: tuple[float, float]
    parts: list[dict]
    notes: list[str] = field(default_factory=list)
    warn: list[str] = field(default_factory=list)


@dataclass
class Spec:
    title: str
    legend: str | None
    columns: int
    panels: list[Panel]


def read_spec(data, where: str = "description") -> Spec:
    if not isinstance(data, dict):
        raise Refusal(f"{where}: the description is a mapping with a title and panels")
    unknown = set(data) - SPEC_KEYS
    if unknown:
        raise Refusal(f"{where}: no {', '.join(sorted(unknown))} at the top; it takes {', '.join(sorted(SPEC_KEYS))}")
    if not data.get("title") or not isinstance(data.get("panels"), list) or not data["panels"]:
        raise Refusal(f"{where}: needs a title and at least one panel")
    scale = tuple(_nums(data["scale"], 2, f"{where} scale")) if "scale" in data else DEFAULT_SCALE
    panels = []
    for i, p in enumerate(data["panels"], 1):
        pw = f"{where} panel {i}"
        if not isinstance(p, dict):
            raise Refusal(f"{pw}: a panel is a mapping")
        unknown = set(p) - PANEL_KEYS
        if unknown:
            raise Refusal(f"{pw}: no {', '.join(sorted(unknown))}; a panel takes {', '.join(sorted(PANEL_KEYS))}")
        if not p.get("title") or not isinstance(p.get("parts"), list) or not p["parts"]:
            raise Refusal(f"{pw}: needs a title and at least one part")
        parts = [check_part(part, f"{pw} part {j}") for j, part in enumerate(p["parts"], 1)]
        pscale = tuple(_nums(p["scale"], 2, f"{pw} scale")) if "scale" in p else scale
        width = float(p["width"]) if "width" in p else max(_extent(part)[2] for part in parts)
        if any(part.get("both") for part in parts) and "width" not in p:
            raise Refusal(f"{pw}: a part drawn on `both` sides needs the panel's `width` to mirror about")
        for j, part in enumerate(parts, 1):
            x0, _, x1, _ = _extent(part)
            if part["kind"] not in ("dim", "arrow") and (x0 < -1e-9 or x1 > width + 1e-9):
                raise Refusal(f"{pw} part {j}: the {part['kind']} runs from {x0:g} to {x1:g} mm, outside the panel's 0 to {width:g}")
        notes = p.get("notes", [])
        warn = p.get("warn", [])
        notes = [notes] if isinstance(notes, str) else list(notes)
        warn = [warn] if isinstance(warn, str) else list(warn)
        panels.append(Panel(str(p["title"]), width, pscale, parts, [str(n) for n in notes], [str(w) for w in warn]))
    columns = int(data.get("columns", min(2, len(panels))))
    if columns < 1:
        raise Refusal(f"{where}: columns is one or more")
    return Spec(str(data["title"]), data.get("legend"), columns, panels)


# --- geometry in millimetres ---------------------------------------------------------------------


def dovetail_polys(part: dict) -> tuple[list | None, list | None]:
    """The slot and rail outlines, in mm, for one dovetail part."""
    cx, z0 = (float(v) for v in part["at"])
    w, h, flare = (float(part[k]) for k in ("width", "height", "flare"))
    gap = float(part.get("gap", 0))
    depth = float(part.get("depth", h))
    sign = 1.0 if part.get("toward", "up") == "up" else -1.0
    show = part.get("show", "both")

    def outline(right: list[tuple[float, float]]) -> list[tuple[float, float]]:
        left = [(2 * cx - x, z) for x, z in reversed(right)]
        return [(x, z0 + sign * dz) for x, dz in right + left]

    def side(extra: float, total: float) -> list[tuple[float, float]]:
        if "steps" not in part:
            pts = [(cx + w / 2 + extra, 0.0), (cx + w / 2 + flare + extra, h)]
            if total > h:
                pts.append((cx + w / 2 + flare + extra, total))
            return pts
        s = float(part["steps"])
        n = round(h / s)
        pts = []
        for i in range(round(total / s)):
            hw = w / 2 + flare * min(i, n - 1) / (n - 1) + extra
            pts += [(cx + hw, i * s), (cx + hw, (i + 1) * s)]
        return pts

    slot = outline(side(gap, depth)) if show in ("both", "slot") else None
    rail = outline(side(0.0, h)) if show in ("both", "rail") else None
    return slot, rail


def _extent(part: dict) -> tuple[float, float, float, float]:
    """x0, z0, x1, z1 in mm."""
    kind = part["kind"]
    if "box" in part:
        x, z, w, h = (float(v) for v in part["box"])
        return x, z, x + w, z + h
    if "line" in part:
        x, z, w = (float(v) for v in part["line"])
        return x, z, x + w, z
    if kind == "dovetail":
        pts = [p for poly in dovetail_polys(part) if poly for p in poly]
    else:
        pts = [tuple(part["from"]), tuple(part["to"])]
    xs, zs = [float(p[0]) for p in pts], [float(p[1]) for p in pts]
    return min(xs), min(zs), max(xs), max(zs)


def mirrored(part: dict, width: float) -> dict:
    m = dict(part)
    if "box" in part:
        x, z, w, h = part["box"]
        m["box"] = [width - x - w, z, w, h]
    if "line" in part:
        x, z, w = part["line"]
        m["line"] = [width - x - w, z, w]
    for key in ("at", "from", "to", "label_at"):
        if key in part:
            m[key] = [width - part[key][0], part[key][1]]
    return m


# --- drawing -------------------------------------------------------------------------------------


def _f(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text_w(text: str, px: float) -> float:
    return len(text) * px * CHAR_EM


def wrap(text: str, px: float, width: float) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and text_w(trial, px) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + ([line] if line else [])


class Box:
    """A running pixel bounding box, so a panel can be shifted to fit everything it drew."""

    def __init__(self) -> None:
        self.x0 = self.y0 = math.inf
        self.x1 = self.y1 = -math.inf

    def add(self, x: float, y: float) -> None:
        self.x0, self.y0 = min(self.x0, x), min(self.y0, y)
        self.x1, self.y1 = max(self.x1, x), max(self.y1, y)

    def add_text(self, x: float, y: float, text: str, px: float, anchor: str) -> None:
        w = text_w(text, px)
        left = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
        self.add(left, y - px)
        self.add(left + w, y + px * 0.3)


@dataclass
class Drawn:
    svg: list[str]
    box: Box
    labels: list[tuple[float, float, str, str]]  # anchor x, anchor y, text, side
    used: set[str]


def draw_panel(panel: Panel) -> Drawn:
    sx, sz = panel.scale
    zs = [v for part in panel.parts for v in (_extent(part)[1], _extent(part)[3])]
    ztop = max(zs)

    def P(x: float, z: float) -> tuple[float, float]:
        return x * sx, (ztop - z) * sz

    out: list[str] = []
    box = Box()
    labels: list[tuple[float, float, str, str]] = []
    used: set[str] = set()

    def poly(pts, fill: str, kind: str) -> None:
        px = [P(x, z) for x, z in pts]
        for x, y in px:
            box.add(x, y)
        d = " ".join(f"{_f(x)},{_f(y)}" for x, y in px)
        out.append(f'<polygon data-kind="{kind}" points="{d}" fill="{fill}"/>')

    def rect(x0: float, z0: float, x1: float, z1: float, fill: str, kind: str) -> None:
        poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], fill, kind)

    def marks(part: dict, x0: float, z0: float, x1: float, z1: float) -> None:
        for mark, color, dash in (("first", FIRST_LAYER, ""), ("last", LAST_LAYER, ' stroke-dasharray="6 4"')):
            faces = part.get(mark, [])
            for face in [faces] if isinstance(faces, str) else faces:
                z = z1 if face == "top" else z0
                (ax, ay), (bx, _) = P(x0, z), P(x1, z)
                out.append(
                    f'<line data-mark="{mark}" x1="{_f(ax)}" y1="{_f(ay)}" x2="{_f(bx)}" y2="{_f(ay)}"'
                    f' stroke="{color}" stroke-width="{_f(MARK_W)}"{dash}/>'
                )
                box.add(ax, ay - MARK_W / 2)
                box.add(bx, ay + MARK_W / 2)
                used.add(mark)

    for part in panel.parts:
        copies = [part]
        if part.get("both"):
            copies = sorted([part, mirrored(part, panel.width)], key=lambda c: _extent(c)[0] + _extent(c)[2])
        for n, cp in enumerate(copies):
            kind = cp["kind"]
            x0, z0, x1, z1 = _extent(cp)
            if kind in BOX_KINDS:
                if kind in HOLE_KINDS:
                    fill = HOLE
                    used.add("hole")
                elif kind in ("half", "lip"):
                    fill = HALF_FILL[cp["side"]]
                    used.add(cp["side"])
                else:
                    fill = _color(cp, kind)
                    used.add("piece" if "side" not in cp or "color" in cp else cp["side"])
                if kind == "stud":
                    c = min(float(cp.get("chamfer", 0.2)), (x1 - x0) / 3, (z1 - z0) / 2)
                    if cp.get("toward", "up") == "up":
                        pts = [(x0, z0), (x1, z0), (x1, z1 - c), (x1 - c, z1), (x0 + c, z1), (x0, z1 - c)]
                    else:
                        pts = [(x0, z0 + c), (x0 + c, z0), (x1 - c, z0), (x1, z0 + c), (x1, z1), (x0, z1)]
                    poly(pts, fill, kind)
                else:
                    rect(x0, z0, x1, z1, fill, kind)
                marks(cp, x0, z0, x1, z1)
            elif kind == "dovetail":
                slot, rail = dovetail_polys(cp)
                if slot:
                    poly(slot, HOLE, "slot")
                    used.add("hole")
                if rail:
                    poly(rail, _color(cp, kind), "rail")
                    used.add("piece" if "side" not in cp or "color" in cp else cp["side"])
                    rx0, rz0, rx1, rz1 = _extent(dict(cp, show="rail"))
                    marks(cp, rx0, rz0, rx1, rz1)
            elif kind == "seam":
                (ax, ay), (bx, _) = P(x0, z0), P(x1, z0)
                out.append(f'<line data-kind="seam" x1="{_f(ax)}" y1="{_f(ay)}" x2="{_f(bx)}" y2="{_f(ay)}" stroke="{HOLE}" stroke-width="1.5" stroke-dasharray="3 2"/>')
                box.add(ax, ay)
                box.add(bx, ay)
            elif kind == "bed":
                (ax, ay), (bx, _) = P(x0, z0), P(x1, z0)
                y = ay + MARK_W / 2 + 2
                out.append(f'<rect data-kind="bed" x="{_f(ax - 6)}" y="{_f(y)}" width="{_f(bx - ax + 12)}" height="5" fill="#cfcbc3"/>')
                text = str(cp.get("text", "print bed"))
                out.append(f'<text x="{_f(bx + 10)}" y="{_f(y + 6)}" font-size="{NOTE_PX}" fill="{NOTE_INK}">{_esc(text)}</text>')
                box.add(ax - 6, y + 5)
                box.add_text(bx + 10, y + 6, text, NOTE_PX, "start")
            elif kind == "arrow":
                (ax, ay), (bx, by) = P(*cp["from"]), P(*cp["to"])
                ang = math.atan2(by - ay, bx - ax)
                hx, hy = bx - 9 * math.cos(ang), by - 9 * math.sin(ang)
                nx, ny = -math.sin(ang) * 5, math.cos(ang) * 5
                out.append(f'<line data-kind="arrow" x1="{_f(ax)}" y1="{_f(ay)}" x2="{_f(bx)}" y2="{_f(by)}" stroke="{NOTE_INK}" stroke-width="1.6"/>')
                out.append(f'<polyline points="{_f(hx + nx)},{_f(hy + ny)} {_f(bx)},{_f(by)} {_f(hx - nx)},{_f(hy - ny)}" fill="none" stroke="{NOTE_INK}" stroke-width="1.6"/>')
                box.add(ax, ay)
                box.add(bx, by)
                if cp.get("text"):
                    tx, ty = (ax + bx) / 2 + 12, (ay + by) / 2 + 4
                    out.append(f'<text x="{_f(tx)}" y="{_f(ty)}" font-size="{NOTE_PX}" fill="{NOTE_INK}">{_esc(str(cp["text"]))}</text>')
                    box.add_text(tx, ty, str(cp["text"]), NOTE_PX, "start")
            elif kind == "dim":
                (ax, ay), (bx, by) = P(*cp["from"]), P(*cp["to"])
                ang = math.atan2(by - ay, bx - ax)
                tx, ty = -math.sin(ang) * 4, math.cos(ang) * 4
                out.append(f'<g data-kind="dim" stroke="{LEADER}" stroke-width="1">')
                out.append(f'<line x1="{_f(ax)}" y1="{_f(ay)}" x2="{_f(bx)}" y2="{_f(by)}"/>')
                for qx, qy in ((ax, ay), (bx, by)):
                    out.append(f'<line x1="{_f(qx - tx)}" y1="{_f(qy - ty)}" x2="{_f(qx + tx)}" y2="{_f(qy + ty)}"/>')
                out.append("</g>")
                text, mx, my = str(cp["text"]), (ax + bx) / 2, (ay + by) / 2
                tx, ty, anchor = {
                    "right": (mx + 7, my + 4, "start"),
                    "left": (mx - 7, my + 4, "end"),
                    "above": (mx, my - 6, "middle"),
                    "below": (mx, my + 15, "middle"),
                }[cp.get("place", "right")]
                out.append(f'<text x="{_f(tx)}" y="{_f(ty)}" font-size="{NOTE_PX - 1}" fill="{NOTE_INK}" text-anchor="{anchor}">{_esc(text)}</text>')
                box.add(ax, ay)
                box.add(bx, by)
                box.add_text(tx, ty, text, NOTE_PX - 1, anchor)
            # the label goes on the copy drawn last, the right-hand one when mirrored
            if "label" in cp and n == len(copies) - 1:
                if "label_at" in cp:
                    lx, ly = P(*cp["label_at"])
                else:
                    lx, ly = P((x0 + x1) / 2, (z0 + z1) / 2)
                labels.append((lx, ly, str(cp["label"]), str(cp.get("label_side", "right"))))
    return Drawn(out, box, labels, used)


def legend_for(spec: Spec, used: set[str]) -> str:
    words = ["Cut through, side view."]
    words += [HALF_WORDS[s] for s in ("lower", "upper") if s in used]
    if "piece" in used:
        names = []
        for panel in spec.panels:
            for part in panel.parts:
                if part["kind"] in ("piece", "flange", "dovetail") and ("color" in part or "side" not in part):
                    name = str(part.get("color", "gold"))
                    if name in PIECE_COLORS and name not in names:
                        names.append(name)
        names.sort(key=list(PIECE_COLORS).index)
        if names:
            said = " and ".join([", ".join(names[:-1]), names[-1]] if len(names) > 1 else names)
            words.append(f"{said[0].upper()}{said[1:]}: the piece.")
    if "hole" in used:
        words.append("White: air.")
    if "first" in used:
        words.append("Solid blue: printed on the bed (first layer).")
    if "last" in used:
        words.append("Orange dashed: printed last (top surface).")
    scales = {p.scale for p in spec.panels}
    words.append("To scale." if all(sx == sz for sx, sz in scales) else "Not to scale.")
    return " ".join(words)


def render(spec: Spec) -> str:
    drawn = [draw_panel(p) for p in spec.panels]
    used = set().union(*(d.used for d in drawn))

    # each panel's cell: title, then left labels | drawing | right labels, then notes
    cells = []
    for panel, d in zip(spec.panels, drawn):
        cols = {}
        for side in ("left", "right"):
            texts = [t for _, _, t, sd in d.labels if sd == side]
            cols[side] = max(text_w(t, LABEL_PX) for t in texts) + 34 if texts else 0.0
        draw_w = d.box.x1 - d.box.x0
        need = max(cols["left"] + draw_w + cols["right"], text_w(panel.title, PANEL_TITLE_PX))
        cells.append((panel, d, draw_w, cols, need))
    # a column is as wide as its widest cell, so one big drawing does not widen the others
    col_w = [max([MIN_CELL_W] + [c[4] for c in cells[i :: spec.columns]]) for i in range(spec.columns)]
    col_x = [0.0] * spec.columns

    margin, col_gap, row_gap = 20.0, 56.0, 34.0
    for i in range(1, spec.columns):
        col_x[i] = col_x[i - 1] + col_w[i - 1] + col_gap
    page_w = margin * 2 + sum(col_w) + col_gap * (spec.columns - 1)
    body: list[str] = []
    y = margin + TITLE_PX
    body.append(f'<text x="{_f(margin)}" y="{_f(y)}" font-size="{TITLE_PX}" font-weight="bold" fill="{INK}">{_esc(spec.title)}</text>')
    legend = spec.legend if spec.legend else legend_for(spec, used)
    for line in wrap(legend, LEGEND_PX, page_w - 2 * margin):
        y += LEGEND_PX + 4
        body.append(f'<text x="{_f(margin)}" y="{_f(y)}" font-size="{LEGEND_PX}" fill="{LEGEND_INK}">{_esc(line)}</text>')
    y += 22

    for row in range(0, len(cells), spec.columns):
        row_h = 0.0
        for col, (panel, d, draw_w, cols, _) in enumerate(cells[row : row + spec.columns]):
            cx = margin + col_x[col]
            cy = y + PANEL_TITLE_PX
            g = [f'<g data-panel="{_esc(panel.title)}">']
            g.append(f'<text x="{_f(cx)}" y="{_f(cy)}" font-size="{PANEL_TITLE_PX}" font-weight="bold" fill="{INK}">{_esc(panel.title)}</text>')
            left = cx + cols["left"]
            dx, dy = left - d.box.x0, cy + 18 - d.box.y0
            g.append(f'<g transform="translate({_f(dx)},{_f(dy)})">')
            g += d.svg
            g.append("</g>")
            bottom = cy + 18 + (d.box.y1 - d.box.y0)
            # labels: a column each side of the drawing, in anchor order, never closer than a line apart
            for side in ("left", "right"):
                mine = sorted(((ax, ay, t) for ax, ay, t, sd in d.labels if sd == side), key=lambda t: t[1])
                if not mine:
                    continue
                tx = left + draw_w + 28 if side == "right" else left - 28
                elbow = 14 if side == "right" else -14
                stub = 4 if side == "right" else -4
                anchor = "start" if side == "right" else "end"
                placed: list[float] = []
                for ax, ay, text in mine:
                    want = ay + dy + 4
                    ly = max(want, placed[-1] + LABEL_PX + 4) if placed else want
                    placed.append(ly)
                    g.append(f'<circle data-label-dot="1" cx="{_f(ax + dx)}" cy="{_f(ay + dy)}" r="2.6" fill="{INK}"/>')
                    g.append(f'<polyline points="{_f(ax + dx)},{_f(ay + dy)} {_f(tx - elbow)},{_f(ly - 4)} {_f(tx - stub)},{_f(ly - 4)}" fill="none" stroke="{LEADER}" stroke-width="0.9"/>')
                    g.append(f'<text data-label="1" x="{_f(tx)}" y="{_f(ly)}" font-size="{LABEL_PX}" fill="{INK}" text-anchor="{anchor}">{_esc(text)}</text>')
                bottom = max(bottom, placed[-1] + 4)
            ny = bottom + 26
            for text, ink in [(n, NOTE_INK) for n in panel.notes] + [(w, WARN_INK) for w in panel.warn]:
                for line in wrap(text, NOTE_PX, col_w[col]):
                    g.append(f'<text x="{_f(cx)}" y="{_f(ny)}" font-size="{NOTE_PX}" fill="{ink}">{_esc(line)}</text>')
                    ny += NOTE_PX + 5
            g.append("</g>")
            body += g
            row_h = max(row_h, ny - y)
        y += row_h + row_gap

    page_h = y - row_gap + margin
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_f(page_w)}" height="{_f(page_h)}"'
        f' viewBox="0 0 {_f(page_w)} {_f(page_h)}" font-family="{FONT}">'
    )
    return "\n".join(
        [head, f"<title>{_esc(spec.title)}</title>", f'<rect width="100%" height="100%" fill="{PAGE_BG}"/>', *body, "</svg>", ""]
    )


# --- commands ------------------------------------------------------------------------------------


def outputs(spec_path: Path) -> tuple[Path, Path]:
    if not spec_path.name.endswith(SPEC_SUFFIX):
        raise Refusal(f"{spec_path}: a description is named <name>{SPEC_SUFFIX}")
    stem = spec_path.name[: -len(SPEC_SUFFIX)]
    return spec_path.with_name(stem + ".svg"), spec_path.with_name(stem + ".png")


def load(spec_path: Path) -> Spec:
    try:
        data = yaml.safe_load(spec_path.read_text())
    except yaml.YAMLError as e:
        raise Refusal(f"{spec_path}: not YAML: {e}") from e
    return read_spec(data, str(spec_path))


def to_png(svg: Path, png: Path, zoom: float) -> None:
    if not shutil.which("rsvg-convert"):
        raise Refusal("rsvg-convert is not installed (brew install librsvg); draw with --no-png for the SVG alone")
    subprocess.run(["rsvg-convert", "-z", _f(zoom), "-o", str(png), str(svg)], check=True, timeout=60)


def cmd_draw(spec_path: Path, png: bool, zoom: float) -> int:
    svg_path, png_path = outputs(spec_path)
    svg_path.write_text(render(load(spec_path)))
    print(f"wrote {svg_path}")
    if png:
        to_png(svg_path, png_path, zoom)
        print(f"wrote {png_path}")
    return 0


def stale(root: Path) -> list[str]:
    problems = []
    for spec_path in sorted(root.rglob(f"*{SPEC_SUFFIX}")):
        svg_path, png_path = outputs(spec_path)
        try:
            want = render(load(spec_path))
        except Refusal as e:
            problems.append(f"{spec_path}: {e}")
            continue
        rel = spec_path.relative_to(ROOT) if spec_path.is_relative_to(ROOT) else spec_path
        if not svg_path.exists():
            problems.append(f"{rel}: no {svg_path.name} beside it; draw it with `{DRAW_CMD} {rel}`")
        elif svg_path.read_text() != want:
            problems.append(f"{rel}: {svg_path.name} is not what the description draws; re-draw with `{DRAW_CMD} {rel}`")
        elif not png_path.exists():
            problems.append(f"{rel}: no {png_path.name} beside it; draw it with `{DRAW_CMD} {rel}`")
    return problems


def cmd_check(root: Path) -> int:
    problems = stale(root)
    for p in problems:
        print(f"side view: {p}", file=sys.stderr)
    count = len(list(root.rglob(f"*{SPEC_SUFFIX}")))
    if problems:
        return 1
    print(f"side views: {count} description(s), every picture current")
    return 0


def cmd_kinds() -> int:
    for name, spec in KINDS.items():
        print(f"{name:9} {spec['about']}")
    print("\nany part: both (mirror about the panel's middle), first/last (top, bottom: layer marks),")
    print("          label (a callout), label_at [x, z] (where its leader points), label_side left|right (default right)")
    return 0


# --- self-test -----------------------------------------------------------------------------------

FIXTURE = """
title: Every part of the kit
panels:
  - title: Halves, lips, piece, seam, labels
    width: 24
    parts:
      - {kind: half, side: lower, box: [0, 0, 4, 2.2], both: true, first: bottom, label: lower half}
      - {kind: half, side: upper, box: [0, 2.2, 4, 2.2], both: true, first: top, label: upper half}
      - {kind: lip, side: lower, box: [4, 0, 1, 0.6], both: true, first: bottom}
      - {kind: air, box: [4, 0.6, 0.2, 3.2], both: true, label: air gap}
      - {kind: piece, box: [4.2, 0.6, 15.6, 1.6], color: teal, first: bottom}
      - {kind: piece, box: [4.2, 2.2, 15.6, 1.6], first: top, last: bottom}
      - {kind: seam, line: [4.2, 2.2, 15.6]}
    notes: [A note that is long enough to wrap onto a second line when the panel is narrow, so wrapping is drawn.]
    warn: [A warning line.]
  - title: Stud, socket, pocket, flange, dovetail, bed, arrow, dim
    width: 20
    parts:
      - {kind: half, side: lower, box: [0, 0, 20, 2]}
      - {kind: stud, side: lower, box: [2, 2, 1.5, 1], label: stud, label_side: left}
      - {kind: socket, box: [16, 0.5, 1.7, 1.5], label: socket}
      - {kind: pocket, box: [6, 1.4, 8, 0.6]}
      - {kind: flange, box: [7, 1.5, 6, 0.4], color: pink}
      - {kind: dovetail, at: [10, 2], width: 4, height: 0.8, flare: 0.3, gap: 0.15, depth: 1.0, steps: 0.2, color: teal, last: top, label: rail}
      - {kind: bed, line: [0, 0, 20]}
      - {kind: arrow, from: [10, 4.5], to: [10, 3.2], text: close}
      - {kind: dim, from: [19, 0], to: [19, 2], text: 2 mm, place: left}
"""


def _self_test() -> int:
    failures: list[str] = []

    def expect(ok: bool, what: str) -> None:
        if not ok:
            failures.append(what)

    spec = read_spec(yaml.safe_load(FIXTURE), "fixture")
    svg = render(spec)
    for kind in ("half", "lip", "piece", "air", "seam", "stud", "socket", "pocket", "flange", "slot", "rail", "bed", "arrow", "dim"):
        expect(f'data-kind="{kind}"' in svg, f"every kind is drawn: {kind} missing")
    expect(svg.count('data-kind="half"') == 5, "a `both` half is drawn twice (4) plus the plain one (1)")
    expect(svg.count('data-mark="first"') == 8, f"first-layer marks: want 8, got {svg.count('data-mark=\"first\"')}")
    expect(svg.count('data-mark="last"') == 2, "last-layer marks: the piece's lower face and the rail's top")
    expect(svg.count('data-label="1"') == 6, f"one label per labeled part, mirrored ones once: got {svg.count('data-label=\"1\"')}")
    expect(render(spec) == svg, "drawing is deterministic")
    left = re.findall(r'<polyline points="([\d.]+),[\d.]+ [\d.]+,[\d.]+ ([\d.]+),[^"]*"[^>]*/>\s*<text data-label="1" [^>]*text-anchor="end">stud<', svg)
    expect(len(left) == 1, "a label_side: left label is end-anchored, after its leader")
    expect(bool(left) and float(left[0][1]) < float(left[0][0]), "a left label's leader runs left, away from the drawing")
    legend = legend_for(spec, {"lower", "upper", "piece", "hole", "first", "last"})
    expect("Gold, teal and pink: the piece." in legend, f"legend names the piece colors used: {legend}")
    expect("Not to scale." in legend, "default scale is not to scale and says so")

    # the stepped rail: four 0.2 mm layers, each 0.1 mm a side wider, top 0.3 wider than its root
    slot, rail = dovetail_polys({"kind": "dovetail", "at": [10, 0], "width": 4, "height": 0.8, "flare": 0.3, "gap": 0.15, "depth": 1.0, "steps": 0.2})
    xs = sorted({round(x, 3) for x, _ in rail if x > 10})
    expect(xs == [12.0, 12.1, 12.2, 12.3], f"rail layers widen 0.1 mm a side per layer: {xs}")
    expect(max(z for _, z in slot) == 1.0 and max(z for _, z in rail) == 0.8, "slot one layer deeper than the rail")
    expect(round(min(x for x, z in slot if z == 0) , 3) == round(10 - 2 - 0.15, 3), "slot mouth is the root plus the gap a side")
    _, down = dovetail_polys({"kind": "dovetail", "at": [0, 2], "width": 2, "height": 1, "flare": 0.2, "toward": "down"})
    expect(min(z for _, z in down) == 1.0, "a rail toward down grows below its root")

    # refusals, each with its reason; the dovetail that would lift out is the by-design failure
    bad = {
        "an unknown kind": ({"kind": "bolt", "box": [0, 0, 1, 1]}, "no part kind"),
        "an unknown key": ({"kind": "piece", "box": [0, 0, 1, 1], "hue": "gold"}, "has no hue"),
        "a missing field": ({"kind": "half", "box": [0, 0, 1, 1]}, "needs side"),
        "a bad color": ({"kind": "piece", "box": [0, 0, 1, 1], "color": "mauve"}, "is not one of"),
        "a bad face": ({"kind": "piece", "box": [0, 0, 1, 1], "first": "side"}, "names faces"),
        "a dovetail that lifts out": ({"kind": "dovetail", "at": [5, 0], "width": 4, "height": 0.8, "flare": 0.1, "gap": 0.15}, "lift straight out"),
        "a slot shallower than its rail": ({"kind": "dovetail", "at": [5, 0], "width": 4, "height": 0.8, "flare": 0.3, "depth": 0.6}, "shallower"),
        "steps that do not divide": ({"kind": "dovetail", "at": [5, 0], "width": 4, "height": 0.8, "flare": 0.3, "steps": 0.3}, "whole layers"),
        "a label on a bad side": ({"kind": "piece", "box": [0, 0, 1, 1], "label": "x", "label_side": "top"}, "left or right"),
        "a part outside the panel": ({"kind": "piece", "box": [8, 0, 4, 1]}, "outside the panel"),
    }
    for what, (part, reason) in bad.items():
        try:
            read_spec({"title": "t", "panels": [{"title": "p", "width": 10, "parts": [part]}]})
            failures.append(f"refuses {what}: it drew it")
        except Refusal as e:
            expect(reason in str(e), f"refuses {what} with the reason ({reason!r} not in {e})")
    try:
        read_spec({"title": "t", "panels": [{"title": "p", "parts": [{"kind": "piece", "box": [0, 0, 1, 1], "both": True}]}]})
        failures.append("refuses `both` without a panel width: it drew it")
    except Refusal:
        pass

    # check: a fresh picture passes, an edited description fails until re-drawn, a missing SVG fails
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        spec_path = root / "media" / "fixture.side.yaml"
        spec_path.parent.mkdir()
        spec_path.write_text(FIXTURE)
        expect(any("no fixture.svg" in p for p in stale(root)), "check fails a description with no picture")
        svg_path, png_path = outputs(spec_path)
        svg_path.write_text(render(load(spec_path)))
        png_path.write_bytes(b"")
        expect(stale(root) == [], f"check passes a current picture: {stale(root)}")
        spec_path.write_text(FIXTURE.replace("lower half}", "lower coaster half}"))
        expect(any("re-draw" in p for p in stale(root)), "check fails a picture its description no longer draws")
        if shutil.which("rsvg-convert"):
            cmd_draw(spec_path, True, 1.0)
            expect(png_path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "draw writes a PNG")
            expect(stale(root) == [], "check passes after a re-draw")

    for f in failures:
        print(f"self-test FAIL: {f}", file=sys.stderr)
    if failures:
        return 1
    print("side_view self-test: ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    d = sub.add_parser("draw", help="draw <name>.svg and <name>.png beside a <name>.side.yaml")
    d.add_argument("spec", type=Path)
    d.add_argument("--no-png", action="store_true")
    d.add_argument("--zoom", type=float, default=2.0)
    c = sub.add_parser("check", help="every description's picture is current")
    c.add_argument("--root", type=Path, default=ROOT / "docs")
    sub.add_parser("kinds", help="list the parts of the kit")
    args = ap.parse_args(argv)
    try:
        if args.self_test:
            return _self_test()
        if args.cmd == "draw":
            return cmd_draw(args.spec, not args.no_png, args.zoom)
        if args.cmd == "check":
            return cmd_check(args.root)
        if args.cmd == "kinds":
            return cmd_kinds()
    except Refusal as e:
        print(f"side view refused: {e}", file=sys.stderr)
        return 2
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
