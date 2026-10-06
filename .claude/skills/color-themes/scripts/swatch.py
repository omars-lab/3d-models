#!/usr/bin/env python3
"""A swatch plate for one filament color: its recipe, and its review page.

Omar decided on 2026-10-05 (D-105) that we print our own swatch card instead of buying sample
packs: "our swatch/samples will be erived form bambu ... but we might buy other faimelnt too
eventually". A swatch is one small plate per color we own or buy, printed in that color, so it
shows the real top surface, the sheen and the bed face. On it:

  CHIP    bikar's Swatch-Chip.bkr: a 50 x 30 mm card with the color's code engraved (1)
  WINDOW  a 30 mm window of the gBV coaster sheets-04g printed, at its star, so the color is seen
          on our own straps and edges (1)

The color is picked at the send, as on sheets-04g: `bambu print send … --color "#RRGGBB"`.

A color is named by its code, the five digits on a Bambu spool, which is also what the chip
engraves. The name, line, finish and hexes come from the color catalog by that code; whether we
own the color comes from the palette. Another brand's color goes in the catalog with a number of
our own, since the chip engraves digits only.

Usage:
    swatch.py recipe <code>                       write docs/design/plates/swatch-<code>.yaml
    swatch.py page <code> --minutes M --grams G [--slices DIR]
                                                  write its page, from the local slice
    swatch.py chip-picture --bikar DIR            draw swatch-media/chip.png, the picture every
                                                  page shows (once, or when the chip changes)
    swatch.py list                                every color, owned first, and which have plates
    swatch.py --self-test

A new swatch, start to finish:
    swatch.py recipe 10204
    bambu slice compose docs/design/plates/swatch-10204.yaml     (prints minutes and grams)
    swatch.py page 10204 --minutes 22 --grams 6                  (copies the slice's picture)
    plate_approve.py docs/design/plates/swatch-10204.md --iterate
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parent.parent
ROOT = SKILL.parent.parent.parent
PALETTE = SKILL / "palette.yaml"
CATALOG = ROOT / "docs" / "design" / "coaster" / "themes" / "catalog" / "catalog.yaml"
PLATES = ROOT / "docs" / "design" / "plates"
SLICES = ROOT / "build" / "plates"

# The coaster the window is cut from: sheets-04g's, at the size it printed.
COASTER = "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr"
COASTER_PARAMS = "{ size: 112.5, strap: 3.75, height: 4.4, round: 1.25 }"
WINDOW = "30@0,0"
BACKDROP = "#d4d4d4"  # behind a shrunk slice picture, light enough for black, dark enough for white


def load_catalog(path: Path = CATALOG) -> dict[str, dict]:
    """Code -> catalog row, over every line."""
    data = yaml.safe_load(path.read_text())
    rows = data["colors"] if isinstance(data, dict) and "colors" in data else data
    return {str(r["code"]): r for r in rows}


def load_owned(path: Path = PALETTE) -> dict[str, dict]:
    """Code -> palette entry, for the colors the printer holds now."""
    data = yaml.safe_load(path.read_text())
    return {str(c["code"]): c for c in data.get("owned", []) if c.get("code")}


def load_buy(path: Path = PALETTE) -> dict[str, dict]:
    data = yaml.safe_load(path.read_text())
    return {str(c["code"]): c for c in data.get("buy", []) if c.get("code")}


def color(code: str, catalog: dict, owned: dict) -> dict:
    if not (code.isdigit() and len(code) <= 5):
        raise SystemExit(f"{code}: a code is up to five digits (the chip engraves digits only)")
    row = catalog.get(code)
    if row is None:
        raise SystemExit(f"{code}: not in the color catalog ({CATALOG.relative_to(ROOT)})")
    hexes = [h[:7].upper() for h in row["hexes"]]
    return {"code": code, "name": row["name"], "line": row["line"], "finish": row.get("finish"),
            "kind": row.get("kind", "single"), "hexes": hexes, "owned": code in owned}


def filament_preset(line: str) -> str:
    """The spool's own line picks the preset, as `bambu plates by-color` does: a Silk spool sliced
    as PLA Basic prints at the wrong heat and speed. The slice refuses a preset Studio lacks."""
    return f"Bambu {line} @BBL X2D 0.4 nozzle"


def recipe_text(c: dict) -> str:
    many = len(c["hexes"]) > 1
    shades = " and ".join(c["hexes"])
    send = c["hexes"][0]
    both = f" (the\n# spool is {shades})" if many else ""
    return f"""# swatch-{c['code']} — a swatch of {c['line']} {c['name']} ({c['code']}), printed in that color
#
# Omar, 2026-10-05 (D-105): our own swatch card, one per color we own or buy, so it shows the real
# surface, the sheen and the bed face. Written by the color-themes skill's swatch.py; every swatch
# plate is the same two pieces with a different code on the chip.
#
#   CHIP    a 50 x 30 mm card, 2 mm thick, the code {c['code']} engraved 0.6 mm deep (1)
#   WINDOW  a 30 mm window of the gBV coaster sheets-04g printed, at its star (1)
#
# No color here, on purpose. The send picks it: `bambu print send … --color "{send}"`{both}.
#
# Validate (no hardware; slicing is local):
#   bambu slice compose docs/design/plates/swatch-{c['code']}.yaml --dry-run

bed: x2d
profile:
  settings: "Bambu Lab X2D 0.4 nozzle;0.20mm Standard @BBL X2D"
  filament: "{filament_preset(c['line'])}"

items:
  - bkr:    bikar:patterns/Coupons/Swatch-Chip.bkr
    piece:  Chip
    params: {{ code: {int(c['code'])} }}
    label:  CHIP
  - bkr:    {COASTER}
    piece:  Coaster
    params: {COASTER_PARAMS}
    window: {WINDOW}
    label:  WINDOW
"""


def page_text(c: dict, minutes: int, grams: float, today: str) -> str:
    name = f"swatch-{c['code']}"
    send = c["hexes"][0]
    if c["owned"]:
        have = "On the printer now, so it can print as soon as you say yes."
    else:
        have = "Not on the printer: it prints once the spool is bought and loaded."
    spool = (f"a {c['kind']} spool ({', '.join(c['hexes'])}), so one chip shows only part of it"
             if len(c["hexes"]) > 1 else f"one color, {send}")
    return f"""---
plate: {name}
recipe: {name}.yaml
iteration: 1
stage: waiting
times_printed: 0
runs: []
answers: "What does {c['line']} {c['name']} ({c['code']}) really look like printed: its top, its sheen and its bed face, on a chip and on our own straps?"
kind: taste
maturity: experiment
bets: []
unblocks: []
minutes: {minutes}
grams: {grams:g}
bed_plates: 1
risk: ok
pictures:
  - swatch-media/chip.png
  - {name}-media/bed.png
---

# {name} — a swatch of {c['line']} {c['name']}

**In short.** You picked our own swatch card over bought sample packs (D-105): "our swatch/samples
will be erived form bambu ... but we might buy other faimelnt too eventually". This is the swatch
for {c['line']} {c['name']}, code {c['code']}, {spool}. {have} The plate is
[`{name}.yaml`]({name}.yaml). One bed, {minutes} minutes, about {grams:g} g.

## What it is

- **CHIP:** a 50 x 30 mm card, 2 mm thick, with {c['code']} engraved in the top. The top shows the
  surface and the sheen; the bottom shows the bed face, the side a coaster sits on.
- **WINDOW:** a 30 mm window of the gBV coaster [sheets-04g](sheets-04g.md) printed, cut at its
  star, so the color is seen on our own straps and edges.

**The color is picked at the send:** `bambu print send … --color "{send}"`.

**What I assumed, for you to change:**

- **The code is the label.** It is the number on the spool, so a chip names the spool to buy again.
- **A window of the coaster, not a whole one,** to keep a swatch to a few grams.

## Why print it

A picture on a screen is not the color a coaster comes out in. The chip settles it for this spool,
and sits beside the others when picking a theme.

## Pictures

The chip, drawn from bikar's `Swatch-Chip.bkr` (every swatch's chip, with its own code).

![A swatch chip: a 50 by 30 mm card with a five-digit code engraved in the middle](swatch-media/chip.png)

The slice: the chip and the coaster window on the bed, in the slicer's green, since the recipe names no color and the send picks it.

![{name} on the bed: the chip and a 30 mm window of the gBV coaster]({name}-media/bed.png)

## Cost and risk

One bed, {minutes} minutes, about {grams:g} g (local slice, {today}, X2D preset and {c['line']},
sliced for the Textured PEI plate Bambu Studio has saved, nothing sent). One color, so no swaps.

**Risk: ok.** Two flat pieces, no loose small parts.

## Your call

- [ ] **Approve as it stands**
- [ ] **Hold** — say why in the notes

Notes:

## Approvals

Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's `plate_approve.py`; a send spends the open approval, and a recipe change resets it.

| Date | Decision | By | Covers | Spent by |
|---|---|---|---|---|

## Timeline

| Date | What happened | Where it is written |
|---|---|---|
| {today} | proposed — the swatch for {c['code']}, by the color-themes skill's swatch.py (D-105) | this page |
| {today} | sliced — local slice fits one bed, {minutes} minutes, {grams:g} g | this page |
"""


def write_recipe(code: str, plates: Path = PLATES) -> Path:
    c = color(code, load_catalog(), load_owned())
    out = plates / f"swatch-{code}.yaml"
    out.write_text(recipe_text(c))
    return out


def write_page(code: str, minutes: int, grams: float, plates: Path = PLATES,
               slices: Path = SLICES) -> Path:
    c = color(code, load_catalog(), load_owned())
    name = f"swatch-{code}"
    if not (plates / f"{name}.yaml").exists():
        raise SystemExit(f"{name}: write the recipe first (swatch.py recipe {code})")
    preview = slices / f"{name}.plate.preview.png"
    if not preview.exists():
        raise SystemExit(f"{name}: no slice picture at {preview}; run bambu slice compose first")
    media = plates / f"{name}-media"
    media.mkdir(exist_ok=True)
    shrink(preview, media / "bed.png")
    if not (plates / "swatch-media" / "chip.png").exists():
        raise SystemExit("swatch-media/chip.png is missing: the chip picture every page shows")
    out = plates / f"{name}.md"
    out.write_text(page_text(c, minutes, grams, dt.date.today().isoformat()))
    return out


def write_chip_picture(bikar: Path, code: str = "10204", plates: Path = PLATES) -> Path:
    """swatch-media/chip.png: the chip drawn from bikar's file, at one code, by OpenSCAD."""
    sys.path.insert(0, str(ROOT / "build"))
    from brick_previews import openscad, render  # the gallery's OpenSCAD picture

    binary = openscad()
    if not binary:
        raise SystemExit("OpenSCAD not found: the chip picture is drawn with it")
    bkr = bikar / "patterns" / "Coupons" / "Swatch-Chip.bkr"
    cli = bikar / "packages" / "cli" / "dist" / "index.js"
    with tempfile.TemporaryDirectory() as t:
        stl, png = Path(t) / "chip.stl", Path(t) / "chip.png"
        subprocess.run(["node", str(cli), "render", str(bkr), "--format", "stl", "--check",
                        "--param", f"code={code}", "-o", str(stl)], check=True, timeout=120)
        render(binary, str(stl), str(png), color="#F5547C")
        media = plates / "swatch-media"
        media.mkdir(exist_ok=True)
        shrink(png, media / "chip.png")
    return media / "chip.png"


def shrink(src: Path, dst: Path) -> None:
    """The request-feedback skill's picture size, so a page stays small.

    The slicer's preview is transparent around the pieces, and PNG8 keys its transparency on
    black, so a black plate came out blank (the theme plates, 2026-10-05). Flattening onto a
    light grey first keeps a black piece and a white one both visible."""
    if shutil.which("magick"):
        subprocess.run(["magick", str(src), "-background", BACKDROP, "-alpha", "remove",
                        "-alpha", "off", "-resize", "1400x>", "-strip", "-colors", "64",
                        f"PNG8:{dst}"], check=True, timeout=60)
    else:
        shutil.copyfile(src, dst)


def list_colors() -> None:
    catalog, owned, buy = load_catalog(), load_owned(), load_buy()
    for code in list(owned) + [k for k in buy if k not in owned]:
        c = color(code, catalog, owned)
        has = "plate" if (PLATES / f"swatch-{code}.yaml").exists() else "-"
        print(f"{code}  {'owned' if c['owned'] else 'buy  '}  {has:5}  {c['line']} {c['name']}")


def self_test() -> int:
    fails = []
    catalog = {"10204": {"code": "10204", "line": "PLA Basic", "name": "Hot Pink", "kind": "single",
                         "finish": "basic", "hexes": ["#F5547CFF"]},
               "13903": {"code": "13903", "line": "PLA Silk", "name": "Neon City", "kind": "multi",
                         "finish": "silk", "hexes": ["#0047BBFF", "#BB22A3FF"]}}
    owned = {"10204": {"code": "10204"}}
    pink = color("10204", catalog, owned)
    if not pink["owned"] or pink["hexes"] != ["#F5547C"]:
        fails.append(f"owned single color read wrong: {pink}")
    neon = color("13903", catalog, {})
    if neon["owned"] or neon["hexes"] != ["#0047BB", "#BB22A3"]:
        fails.append(f"two-color spool read wrong: {neon}")
    r = yaml.safe_load(recipe_text(pink))
    chip = r["items"][0]
    if chip["params"] != {"code": 10204} or chip["piece"] != "Chip":
        fails.append(f"the chip does not engrave the code: {chip}")
    if r["items"][1].get("window") != WINDOW:
        fails.append("the coaster window is missing")
    if "color" in r or any("filament" in i for i in r["items"]):
        fails.append("a swatch recipe names a color; the send picks it")
    if yaml.safe_load(recipe_text(neon))["profile"]["filament"] != "Bambu PLA Silk @BBL X2D 0.4 nozzle":
        fails.append("a Silk spool is not sliced with the Silk preset")
    if "spool is #0047BB and #BB22A3" not in recipe_text(neon):
        fails.append("a two-color spool's recipe does not say both shades")
    page = page_text(pink, 20, 5.5, "2026-10-05")
    head = yaml.safe_load(page.split("---")[1])
    if head["plate"] != "swatch-10204" or head["grams"] != 5.5 or head["stage"] != "waiting":
        fails.append(f"page frontmatter wrong: {head}")
    for bad, why in (("1234567", "six or more digits"), ("10A04", "a letter"), ("99999", "not in the catalog")):
        try:
            color(bad, catalog, owned)
            fails.append(f"accepted a code with {why}: {bad}")
        except SystemExit:
            pass
    with tempfile.TemporaryDirectory() as t:
        try:
            write_page("10204", 20, 5.5, plates=Path(t), slices=Path(t))
            fails.append("wrote a page with no recipe")
        except SystemExit:
            pass
    for f in fails:
        print(f"FAIL: {f}")
    print(f"swatch self-test: {'ok' if not fails else f'{len(fails)} failed'}")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("recipe")
    r.add_argument("code")
    p = sub.add_parser("page")
    p.add_argument("code")
    p.add_argument("--minutes", type=int, required=True)
    p.add_argument("--grams", type=float, required=True)
    p.add_argument("--slices", type=Path, default=SLICES,
                   help="where the slice wrote its picture (the checkout bambu ran in)")
    c = sub.add_parser("chip-picture")
    c.add_argument("--bikar", type=Path, required=True, help="a bikar checkout with the CLI built")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "recipe":
        print(write_recipe(a.code).relative_to(ROOT))
    elif a.cmd == "page":
        print(write_page(a.code, a.minutes, a.grams, slices=a.slices).relative_to(ROOT))
    elif a.cmd == "chip-picture":
        print(write_chip_picture(a.bikar).relative_to(ROOT))
    elif a.cmd == "list":
        list_colors()
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
