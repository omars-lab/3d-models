#!/usr/bin/env python3
"""The Bambu filament color catalog: every color Bambu Studio knows, as data and as swatch sheets.

Bambu Studio ships one file listing every Bambu filament color it can show in the slicer:
`filaments_color_codes.json`. This script copies it into the repo as
`docs/design/coaster/themes/catalog/catalog.yaml`, one entry per color with its product code, line,
English name, every hex with its alpha byte, whether the spool is one color, a gradient or a
multi-color spool, and a finish label read off the line's name. palette.yaml's buy list is checked
against it (`themes.py --self-test`), so no buy color can carry a hex we made up.

Usage:
    catalog.py build             the Bambu Studio app on this Mac -> catalog.yaml (and the sheets)
    catalog.py refresh           fetch the same file from Bambu's GitHub repo and say what changed;
                                 writes nothing
    catalog.py sheets            catalog.yaml -> one swatch sheet per coaster line, and the page
    catalog.py check             fails when the sheets or the page are out of date with catalog.yaml
    catalog.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import re
import sys
import urllib.request
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parent.parent
ROOT = SKILL.parent.parent.parent
THEMES_DIR = ROOT / "docs" / "design" / "coaster" / "themes"
CATALOG_DIR = THEMES_DIR / "catalog"
CATALOG = CATALOG_DIR / "catalog.yaml"
PAGE = THEMES_DIR / "bambu-color-catalog.md"
PALETTE = SKILL / "palette.yaml"
RESEARCH = "docs/research/2026-10-04-bambu-filament-color-catalog.md"

APP = Path("/Applications/BambuStudio.app")
APP_FILE = APP / "Contents" / "Resources" / "profiles" / "BBL" / "filament" / "filaments_color_codes.json"
GITHUB_REPO = "bambulab/BambuStudio"
GITHUB_PATH = "resources/profiles/BBL/filament/filaments_color_codes.json"
# Checked on 2026-10-04 with `gh api repos/bambulab/BambuStudio/contents/<path>`: the file is there
# on the default branch, master.
GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/{GITHUB_PATH}"

# The lines a coaster can print in on this X2D with the PLA and PETG profiles. Every PLA line, and
# the plain PETG lines. Carbon-fiber PETG, the engineering plastics, TPU and the support materials
# are left out: they need other nozzles, other temperatures, or are not meant to be seen.
COASTER_LINES = [
    "PLA Basic", "PLA Matte", "PLA Silk", "PLA Silk+", "PLA Sparkle", "PLA Galaxy", "PLA Marble",
    "PLA Metal", "PLA Translucent", "PLA Glow", "PLA Wood", "PLA Lite", "PLA Pure", "PLA Tough",
    "PLA Tough+", "PLA Aero", "PLA-CF", "PLA Dynamic",
    "PETG Basic", "PETG Matte", "PETG HF", "PETG Translucent",
]

# The finish label is the word in the line's name. A line whose name names no finish is "plain":
# that is all the file says, not a claim about how it looks.
FINISH_WORDS = [
    ("Silk+", "silk+"), ("Silk", "silk"), ("Matte", "matte"), ("Sparkle", "sparkle"),
    ("Galaxy", "galaxy"), ("Marble", "marble"), ("Metal", "metal"), ("Translucent", "translucent"),
    ("Glow", "glow"), ("Wood", "wood"), ("Dynamic", "uv color change"), ("Basic", "basic"),
    ("-CF", "carbon fiber"), ("-GF", "glass fiber"),
]

# The page's sections, in this order; any other finish goes last in the order met.
FINISH_ORDER = ["basic", "matte", "silk", "silk+", "sparkle", "galaxy", "marble", "metal",
                "translucent", "glow", "wood", "uv color change", "carbon fiber", "plain"]

KIND = {"单色": "single", "渐变色": "gradient", "多拼色": "multi"}

# How the pictures draw a finish. Everything else is drawn flat.
SHEEN = {"silk", "silk+", "metal"}
FLECKS = {"sparkle", "galaxy"}


def load_yaml(path: Path):
    with open(path) as f:
        return yaml.safe_load(f)


def finish_of(line: str) -> str:
    for word, label in FINISH_WORDS:
        if word in line:
            return label
    return "plain"


def entries(raw: dict) -> list[dict]:
    """Bambu's JSON -> catalog entries, sorted by line and code."""
    out = []
    for e in raw["data"]:
        kind = KIND.get(e["fila_color_type"])
        if kind is None:
            raise SystemExit(f"{e['fila_color_code']}: unknown color type {e['fila_color_type']!r}")
        out.append({
            "code": str(e["fila_color_code"]),
            "slot": e["color_code"],
            "line": e["fila_type"],
            "name": e["fila_color_name"]["en"].strip(),
            "kind": kind,
            "finish": finish_of(e["fila_type"]),
            "hexes": [h.upper() for h in e["fila_color"]],
        })
    codes = [e["code"] for e in out]
    if len(codes) != len(set(codes)):
        raise SystemExit("two entries share a product code; the catalog keys on it")
    return sorted(out, key=lambda e: (e["line"], e["code"]))


def line_counts(es: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for e in es:
        counts[e["line"]] = counts.get(e["line"], 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def app_version() -> str:
    with open(APP / "Contents" / "Info.plist", "rb") as f:
        return plistlib.load(f).get("CFBundleShortVersionString", "unknown")


def catalog_text(es: list[dict], source: dict) -> str:
    lines = [
        "# generated by .claude/skills/color-themes/scripts/catalog.py build; do not edit.",
        "# Every Bambu filament color Bambu Studio ships, from its filaments_color_codes.json.",
        f"# How it was read, and what a hex here is and is not: {RESEARCH}",
        "# A hex is #RRGGBBAA: the alpha byte is FF for an opaque color, 80 for a translucent one.",
        "# kind: single (one color), gradient (the color shifts along the spool), multi (two or more",
        "# colors side by side in the strand). finish: the word in the line's name; plain names none.",
        "",
    ]
    doc = {
        "source": source,
        "coaster_lines": COASTER_LINES,
        "lines": line_counts(es),
        "colors": es,
    }
    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=200)
    # One color per line reads better than yaml's block form for 314 entries.
    flow = []
    for e in es:
        flow.append("  - " + yaml.safe_dump(e, default_flow_style=True, sort_keys=False, width=400).strip())
    head = body.split("\ncolors:\n")[0]
    return "\n".join(lines) + head + "\ncolors:\n" + "\n".join(flow) + "\n"


def load_catalog(path: Path = CATALOG) -> dict:
    data = load_yaml(path)
    data["by_code"] = {e["code"]: e for e in data["colors"]}
    return data


def cmd_build() -> None:
    raw_bytes = APP_FILE.read_bytes()
    raw = json.loads(raw_bytes)
    es = entries(raw)
    if raw.get("total") is not None and raw["total"] != len(es):
        raise SystemExit(f"the file says total {raw['total']} but lists {len(es)}")
    source = {
        "file": str(APP_FILE),
        "app": f"Bambu Studio {app_version()}",
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "entries": len(es),
        "github": GITHUB_RAW,
    }
    missing = [ln for ln in COASTER_LINES if ln not in {e["line"] for e in es}]
    if missing:
        raise SystemExit(f"coaster lines not in the file: {missing}")
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(catalog_text(es, source))
    print(f"{CATALOG.relative_to(ROOT)}: {len(es)} colors in {len(line_counts(es))} lines, "
          f"from {source['app']}")
    cmd_sheets()


# ---------------------------------------------------------------- refresh


def diff(old: list[dict], new: list[dict]) -> dict:
    """Added, removed and changed colors between two entry lists, keyed on product code."""
    a = {e["code"]: e for e in old}
    b = {e["code"]: e for e in new}
    changed = []
    for code in sorted(a.keys() & b.keys()):
        fields = [k for k in ("line", "name", "kind", "hexes", "slot") if a[code][k] != b[code][k]]
        if fields:
            changed.append((code, {k: (a[code][k], b[code][k]) for k in fields}))
    return {
        "added": [b[c] for c in sorted(b.keys() - a.keys())],
        "removed": [a[c] for c in sorted(a.keys() - b.keys())],
        "changed": changed,
    }


def fetch_github() -> bytes:
    req = urllib.request.Request(GITHUB_RAW, headers={"User-Agent": "3d-models catalog.py refresh"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def report(d: dict) -> list[str]:
    out = []
    for e in d["added"]:
        out.append(f"added    {e['code']} {e['line']} {e['name']} {' '.join(e['hexes'])}")
    for e in d["removed"]:
        out.append(f"removed  {e['code']} {e['line']} {e['name']}")
    for code, fields in d["changed"]:
        what = "; ".join(f"{k} {v[0]} -> {v[1]}" for k, v in fields.items())
        out.append(f"changed  {code}: {what}")
    return out


def cmd_refresh() -> int:
    cat = load_catalog()
    try:
        raw_bytes = fetch_github()
    except Exception as exc:  # the network, a moved file, a rate limit: say which and stop
        print(f"refresh: could not fetch {GITHUB_RAW}: {exc}")
        print(f"refresh: if Bambu moved the file, look for it with "
              f"`gh api repos/{GITHUB_REPO}/contents/resources/profiles/BBL/filament`.")
        return 1
    sha = hashlib.sha256(raw_bytes).hexdigest()
    new = entries(json.loads(raw_bytes))
    d = diff(cat["colors"], new)
    print(f"refresh: GitHub master has {len(new)} colors (sha256 {sha[:12]}); "
          f"catalog.yaml has {len(cat['colors'])} from {cat['source']['app']} (sha256 {cat['source']['sha256'][:12]})")
    lines = report(d)
    for ln in lines:
        print(ln)
    if not lines:
        print("refresh: no color added, removed or changed. Nothing to do.")
    else:
        print(f"refresh: {len(d['added'])} added, {len(d['removed'])} removed, {len(d['changed'])} changed. "
              "Nothing was written. To take them, update Bambu Studio and run `catalog.py build`, "
              "then `themes.py --self-test` to see whether a buy color moved.")
    return 0


# ---------------------------------------------------------------- drawing a color


def rgb(hexstr: str) -> tuple[int, int, int]:
    h = hexstr.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def alpha(hexstr: str) -> float:
    h = hexstr.lstrip("#")
    return int(h[6:8], 16) / 255 if len(h) == 8 else 1.0


def opaque(hexstr: str) -> str:
    return "#" + hexstr.lstrip("#")[:6].upper()


def lightness(hexstr: str) -> float:
    r, g, b = (v / 255 for v in rgb(hexstr))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def draw_opacity(a: float) -> float:
    """A clear filament (alpha 0) is still drawn a little, so its shape shows."""
    return round(max(a, 0.15), 2)


def finish_defs(key: str, finish: str, hexes: list[str], user_space: tuple | None = None) -> list[str]:
    """SVG defs a color's fill needs: the spool's own gradient, a sheen, flecks.

    Returns def elements whose ids start with `key`. `fill_attrs` and `overlays` refer to them.
    """
    out = []
    if len(hexes) > 1:
        stops = "".join(f'<stop offset="{i / (len(hexes) - 1):.2f}" stop-color="{opaque(h)}" />'
                        for i, h in enumerate(hexes))
        out.append(f'<linearGradient id="{key}-spool" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>')
    if finish in SHEEN:
        out.append(f'<linearGradient id="{key}-sheen" x1="0" y1="1" x2="1" y2="0">'
                   '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0" />'
                   '<stop offset="0.45" stop-color="#FFFFFF" stop-opacity="0.55" />'
                   '<stop offset="0.6" stop-color="#FFFFFF" stop-opacity="0.1" />'
                   '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0" /></linearGradient>')
    if finish in FLECKS:
        fleck = "#FFFFFF" if lightness(hexes[0]) < 0.6 else "#5A5A5A"
        s = user_space or (6.0, 0.35)
        size, r = s
        dots = "".join(f'<circle cx="{x * size:.2f}" cy="{y * size:.2f}" r="{r * k:.2f}" fill="{fleck}" '
                       f'fill-opacity="{o}" />'
                       for x, y, k, o in ((0.15, 0.2, 1.0, 0.9), (0.6, 0.35, 0.7, 0.7), (0.35, 0.75, 0.8, 0.8),
                                          (0.85, 0.8, 0.6, 0.6), (0.8, 0.1, 0.5, 0.7)))
        out.append(f'<pattern id="{key}-flecks" patternUnits="userSpaceOnUse" width="{size}" height="{size}">'
                   f"{dots}</pattern>")
    return out


def fill_attrs(key: str, hexes: list[str]) -> str:
    fill = f"url(#{key}-spool)" if len(hexes) > 1 else opaque(hexes[0])
    a = alpha(hexes[0])
    return f'fill="{fill}"' + (f' fill-opacity="{draw_opacity(a)}"' if a < 1 else "")


def overlay_fills(key: str, finish: str) -> list[str]:
    out = []
    if finish in SHEEN:
        out.append(f"url(#{key}-sheen)")
    if finish in FLECKS:
        out.append(f"url(#{key}-flecks)")
    return out


# ---------------------------------------------------------------- swatch sheets and the page


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("+", "-plus")).strip("-")


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def palette_marks(path: Path = PALETTE) -> tuple[dict, dict]:
    """Tray hexes (owned) -> tray name, and buy-list code -> palette id."""
    data = load_yaml(path)
    trays = {c["hex"].upper(): c["name"] for c in data["owned"]}
    buy = {str(c["code"]): c["id"] for c in data["buy"]}
    return trays, buy


def mark_of(e: dict, trays: dict, buy: dict) -> str:
    if len(e["hexes"]) == 1 and alpha(e["hexes"][0]) == 1 and opaque(e["hexes"][0]) in trays:
        return "tray"
    if e["code"] in buy:
        return "buy"
    return ""


COLS, SW, SH, GAP, TXT = 6, 128, 72, 14, 54


def sheet_svg(line: str, es: list[dict], trays: dict, buy: dict) -> str:
    rows = (len(es) + COLS - 1) // COLS
    w = COLS * (SW + GAP) + GAP
    h = 44 + rows * (SH + TXT + GAP) + GAP
    defs, body = [], []
    for i, e in enumerate(es):
        x = GAP + (i % COLS) * (SW + GAP)
        y = 44 + (i // COLS) * (SH + TXT + GAP)
        key = f"c{e['code']}"
        defs += finish_defs(key, e["finish"], e["hexes"], user_space=(14.0, 1.1))
        if alpha(e["hexes"][0]) < 1:
            body.append(f'  <rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="url(#checks)" />')
        body.append(f'  <rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" {fill_attrs(key, e["hexes"])} '
                    'stroke="#00000033" stroke-width="1" />')
        for ov in overlay_fills(key, e["finish"]):
            body.append(f'  <rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ov}" />')
        mark = mark_of(e, trays, buy)
        if mark == "tray":
            body.append(f'  <circle cx="{x + SW - 13}" cy="{y + 13}" r="8" fill="#1A1A1A" stroke="#FFFFFF" stroke-width="2" />')
        elif mark == "buy":
            body.append(f'  <circle cx="{x + SW - 13}" cy="{y + 13}" r="7" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="2.5" />')
        ty = y + SH + 16
        name = e["name"] if len(e["name"]) <= 24 else e["name"][:23] + "…"
        body.append(f'  <text x="{x}" y="{ty}" font-size="{12.5 if len(name) <= 18 else 10.5}" '
                    f'font-weight="bold">{esc(name)}</text>')
        body.append(f'  <text x="{x}" y="{ty + 15}" font-size="11">{e["code"]} · {e["slot"]}'
                    f'{" · " + e["kind"] if e["kind"] != "single" else ""}</text>')
        hexes = [h[:7] + ("" if h.endswith("FF") else " a" + h[7:]) for h in e["hexes"]]
        for k in range(0, len(hexes), 2):  # two hexes to a row, so four still fit the swatch's width
            body.append(f'  <text x="{x}" y="{ty + 29 + k * 6}" font-size="10.5" fill="#555555">'
                        f'{" ".join(hexes[k:k + 2])}</text>')
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        'font-family="Helvetica, Arial, sans-serif">',
        f"  <title>Bambu {esc(line)}: {len(es)} colors</title>",
        "  <defs>",
        '    <pattern id="checks" patternUnits="userSpaceOnUse" width="16" height="16">'
        '<rect width="16" height="16" fill="#FFFFFF" /><rect width="8" height="8" fill="#D8D8D8" />'
        '<rect x="8" y="8" width="8" height="8" fill="#D8D8D8" /></pattern>',
        *("    " + d for d in defs),
        "  </defs>",
        f'  <rect width="{w}" height="{h}" fill="#F7F5F2" />',
        f'  <text x="{GAP}" y="28" font-size="18" font-weight="bold">{esc(line)}</text>',
        f'  <text x="{w - GAP}" y="28" font-size="12" text-anchor="end" fill="#555555">{len(es)} colors · '
        f'finish: {esc(es[0]["finish"])}</text>',
        *body,
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def sections(cat: dict) -> list[tuple[str, list[str]]]:
    """Finish -> the coaster lines with that finish, in FINISH_ORDER."""
    by: dict[str, list[str]] = {}
    for ln in cat["coaster_lines"]:
        f = next(e["finish"] for e in cat["colors"] if e["line"] == ln)
        by.setdefault(f, []).append(ln)
    order = FINISH_ORDER + [f for f in by if f not in FINISH_ORDER]
    return [(f, by[f]) for f in order if f in by]


def page_text(cat: dict, trays: dict, buy: dict) -> str:
    src = cat["source"]
    coaster = [e for e in cat["colors"] if e["line"] in cat["coaster_lines"]]
    others = {ln: n for ln, n in cat["lines"].items() if ln not in cat["coaster_lines"]}
    n_tray = sum(1 for e in coaster if mark_of(e, trays, buy) == "tray")
    n_buy = sum(1 for e in coaster if mark_of(e, trays, buy) == "buy")
    out = [
        "---",
        "status: built",
        "generated: true",
        "produced-by: .claude/skills/color-themes/scripts/catalog.py sheets",
        "---",
        "",
        "# Bambu filament colors: the catalog to mix and match from",
        "",
        "> Generated from [catalog/catalog.yaml](catalog/catalog.yaml) by `catalog.py sheets`. "
        "Edit nothing here; rebuild the catalog instead.",
        "",
        f"Every color Bambu Studio knows, {src['entries']} in {len(cat['lines'])} lines, read from "
        f"{src['app']}'s own color list ([how it was read](../../../research/2026-10-04-bambu-filament-color-catalog.md)). "
        f"The {len(cat['coaster_lines'])} lines a coaster can print in on this printer hold {len(coaster)} of them, "
        "drawn below one sheet per line, grouped by finish. The [color themes](gbv-themes.md) draw from these.",
        "",
        "**How to read a sheet.**",
        "",
        f"- **A filled black dot** means a tray on the printer has exactly this hex ({n_tray} swatches). "
        "A hex does not say which product is loaded: black matches several lines.",
        f"- **A white ring** means it is on the [buy list](../../../../.claude/skills/color-themes/palette.yaml) "
        f"a theme may use ({n_buy} swatches). No mark: in the catalog, not yet on the list.",
        "- **Finishes are drawn, roughly.** Silk, silk+ and metal get a white sheen, sparkle and galaxy "
        "get flecks, and translucent colors are half see-through over a checkerboard. Matte, basic and "
        "the rest are flat. A sheen on a screen is a reminder, not a picture of the plastic.",
        "- **A gradient or multi-color spool** shows its hexes side by side. Where along the spool the "
        "color shifts cannot be predicted for a given piece, so a coaster's pieces will not come out "
        "matching the picture.",
        "- **A hex is Bambu's label for the color,** not a measurement of a printed part, and a screen "
        "is not a spool.",
        "",
        "| Finish | Lines | Colors |",
        "|---|---|---|",
    ]
    # A heading spells "+" as "plus", so its link works in Obsidian and on GitHub alike.
    for f, lines in sections(cat):
        n = sum(cat["lines"][ln] for ln in lines)
        out.append(f"| [{f}](#{slug(f)}) | {', '.join(lines)} | {n} |")
    out.append("")
    for f, lines in sections(cat):
        out += [f"## {f.replace('+', ' plus')}", ""]
        for ln in lines:
            es = [e for e in coaster if e["line"] == ln]
            kinds = {k: sum(1 for e in es if e["kind"] == k) for k in ("single", "gradient", "multi")}
            extra = ", ".join(f"{n} {k}" for k, n in kinds.items() if n and k != "single")
            out += [f"### {ln}", "",
                    f"{len(es)} colors{' (' + extra + ')' if extra else ''}.", "",
                    f"![Bambu {ln} swatches](catalog/{slug(ln)}.svg)", ""]
    out += [
        "## Lines left out",
        "",
        "These are in the catalog file but not drawn: other plastics that need another nozzle, "
        "temperature or profile than the coasters print with, and support materials.",
        "",
        "| Line | Colors |",
        "|---|---|",
    ]
    for ln, n in others.items():
        out.append(f"| {ln} | {n} |")
    out += [
        "",
        "## Keeping it current",
        "",
        "`catalog.py refresh` fetches the same file from Bambu's public repository on GitHub and lists "
        "the colors added, removed or changed since this catalog was built. It writes nothing. "
        "`catalog.py build` rebuilds the catalog from the Bambu Studio on this Mac, so update the app "
        "first.",
    ]
    return "\n".join(out) + "\n"


def sheet_files(cat: dict, trays: dict, buy: dict) -> dict:
    out = {}
    for ln in cat["coaster_lines"]:
        es = [e for e in cat["colors"] if e["line"] == ln]
        out[CATALOG_DIR / f"{slug(ln)}.svg"] = sheet_svg(ln, es, trays, buy)
    out[PAGE] = page_text(cat, trays, buy)
    return out


def cmd_sheets(png_dir: str | None = None) -> None:
    import subprocess

    cat = load_catalog()
    trays, buy = palette_marks()
    for path, text in sheet_files(cat, trays, buy).items():
        path.write_text(text)
        print(path.relative_to(ROOT))
        if png_dir and path.suffix == ".svg":
            Path(png_dir).mkdir(parents=True, exist_ok=True)
            subprocess.run(["rsvg-convert", "-w", "960", str(path), "-o",
                            str(Path(png_dir) / f"catalog-{path.stem}.png")], check=True)


def cmd_check(quiet: bool = False) -> int:
    cat = load_catalog()
    errors = []
    if len(cat["colors"]) != cat["source"]["entries"]:
        errors.append(f"catalog.yaml lists {len(cat['colors'])} colors, its source line says {cat['source']['entries']}")
    if sum(cat["lines"].values()) != len(cat["colors"]):
        errors.append("the line counts do not add up to the colors")
    trays, buy = palette_marks()
    for path, text in sheet_files(cat, trays, buy).items():
        if not path.exists() or path.read_text() != text:
            errors.append(f"{path.relative_to(ROOT)} is stale or missing; run `catalog.py sheets`")
    for e in errors:
        print(f"catalog: {e}")
    if not errors and not quiet:
        print(f"catalog: {len(cat['colors'])} colors, sheets and page up to date")
    return 1 if errors else 0


# ---------------------------------------------------------------- self-test


FIXTURE = {
    "data": [
        {"fila_color_code": "10100", "fila_id": "GFA00", "fila_color_type": "单色", "fila_type": "PLA Basic",
         "fila_color_name": {"en": "Jade White"}, "color_code": "W1", "fila_color": ["#FFFFFFFF"]},
        {"fila_color_code": "13104", "fila_id": "GFA05", "fila_color_type": "单色", "fila_type": "PLA Silk",
         "fila_color_name": {"en": "Silver"}, "color_code": "D1", "fila_color": ["#eaecebFF"]},
        {"fila_color_code": "13902", "fila_id": "GFA05", "fila_color_type": "多拼色", "fila_type": "PLA Silk",
         "fila_color_name": {"en": "Midnight Blaze"}, "color_code": "T2", "fila_color": ["#0047BBFF", "#7D1B49FF"]},
        {"fila_color_code": "13610", "fila_id": "GFA13", "fila_color_type": "单色", "fila_type": "PLA Translucent",
         "fila_color_name": {"en": "Ice Blue"}, "color_code": "B0", "fila_color": ["#B8CDE980"]},
        {"fila_color_code": "13603", "fila_id": "GFA06", "fila_color_type": "单色", "fila_type": "PLA Silk+",
         "fila_color_name": {"en": "Baby Blue"}, "color_code": "B0", "fila_color": ["#A8C6EEFF"]},
    ],
    "total": 5,
}


def self_test() -> int:
    fails = []

    def expect(cond, what):
        if not cond:
            fails.append(what)

    # 1. Reading Bambu's file: names, kinds, finishes, every hex with its alpha, upper case.
    es = entries(FIXTURE)
    by = {e["code"]: e for e in es}
    expect(len(es) == 5, f"fixture: {len(es)} entries")
    expect(by["13104"]["hexes"] == ["#EAECEBFF"], "a lower-case hex was not upper-cased")
    expect(by["13902"]["kind"] == "multi" and len(by["13902"]["hexes"]) == 2, "a dual-color spool lost a hex")
    expect(by["13610"]["hexes"][0].endswith("80"), "a translucent color lost its alpha")
    expect(by["13603"]["finish"] == "silk+" and by["13104"]["finish"] == "silk",
           "Silk+ must not read as silk, nor silk as silk+")
    expect(finish_of("PLA Tough+") == "plain" and finish_of("PLA Matte") == "matte"
           and finish_of("PETG Translucent") == "translucent" and finish_of("PLA-CF") == "carbon fiber",
           "a finish label is wrong")
    try:
        entries({"data": FIXTURE["data"] + [FIXTURE["data"][0]]})
        fails.append("two entries with one code were accepted")
    except SystemExit:
        pass

    # 2. The diff: nothing changed is empty; an added, a removed and a one-digit hex change all show.
    expect(report(diff(es, entries(FIXTURE))) == [], "the same file twice should report nothing")
    moved = json.loads(json.dumps(FIXTURE))
    moved["data"][0]["fila_color"] = ["#FFFFFEFF"]
    moved["data"].pop(1)
    moved["data"].append({**FIXTURE["data"][0], "fila_color_code": "10999", "fila_color_name": {"en": "New"}})
    d = diff(es, entries(moved))
    expect([e["code"] for e in d["added"]] == ["10999"], f"added: {d['added']}")
    expect([e["code"] for e in d["removed"]] == ["13104"], f"removed: {d['removed']}")
    expect([c for c, _ in d["changed"]] == ["10100"], f"a one-digit hex change was not reported: {d['changed']}")

    # 3. The checked-in catalog: whole, every coaster line present, sheets in step with it.
    cat = load_catalog()
    expect(len(cat["colors"]) == cat["source"]["entries"] == 314, f"catalog: {len(cat['colors'])} colors")
    expect(sum(cat["lines"].values()) == len(cat["colors"]), "line counts do not add up")
    lines = {e["line"] for e in cat["colors"]}
    expect(all(ln in lines for ln in cat["coaster_lines"]), "a coaster line is not in the catalog")
    expect(cat["coaster_lines"] == COASTER_LINES, "catalog.yaml's coaster lines differ from the script's")
    multi = [e for e in cat["colors"] if len(e["hexes"]) > 1]
    expect(all(e["kind"] != "single" for e in multi), "a spool with two hexes is marked single")

    # 4. The app on this Mac, if it is the one the catalog was built from, rebuilds it exactly.
    if APP_FILE.exists():
        raw = APP_FILE.read_bytes()
        if hashlib.sha256(raw).hexdigest() == cat["source"]["sha256"]:
            expect(entries(json.loads(raw)) == cat["colors"], "the app's file no longer builds catalog.yaml")
        else:
            print("self-test note: Bambu Studio's color file changed since the catalog was built; "
                  "run `catalog.py refresh` to see what moved, then `catalog.py build`")

    # 5. Drawing: a translucent fill is see-through, a dual spool fills with its own gradient.
    expect('fill-opacity="0.5"' in fill_attrs("k", ["#B8CDE980"]), "translucent was drawn opaque")
    expect(fill_attrs("k", ["#0047BBFF", "#7D1B49FF"]).startswith('fill="url(#k-spool)"'),
           "a dual spool was drawn as one color")
    expect(draw_opacity(0.0) > 0, "a clear filament would be drawn invisible")
    svg = sheet_svg("PLA Silk", [by["13104"], by["13902"]], {}, {})
    expect("c13104-sheen" in svg and "c13902-spool" in svg, "a silk swatch has no sheen, or a dual spool no gradient")

    for f in fails:
        print(f"self-test FAIL: {f}")
    print("catalog self-test: " + ("ok" if not fails else f"{len(fails)} failed"))
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build")
    sub.add_parser("refresh")
    s = sub.add_parser("sheets")
    s.add_argument("--png", help="also write a PNG of each sheet here, to look at")
    c = sub.add_parser("check")
    c.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "build":
        cmd_build()
    elif a.cmd == "refresh":
        return cmd_refresh()
    elif a.cmd == "sheets":
        cmd_sheets(a.png)
    elif a.cmd == "check":
        return cmd_check(a.quiet)
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
