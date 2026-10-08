#!/usr/bin/env python3
"""A theme's plates: one plate per color, each with its review page, and a priced buy list.

Omar picked the first themes to print on 2026-10-05 (D-106): "all the bottom row", that is Midnight
blue, Night sky, Terracotta souk and Iznik tile. Each theme prints as one plate per color (D-103),
so the plates come from `bambu plates by-color`, given the theme's colors by their spool codes. A
code slices with its own line's preset (a Silk spool as PLA Silk, not PLA Basic) and is priced by
its own store price.

For each theme this script:
  1. runs `bambu plates by-color … --costs --slice` into build/themes/<theme>/ (gitignored),
  2. copies each color's recipe to docs/design/plates/theme-<theme>-<code>.yaml,
  3. copies its slice picture to theme-<theme>-<code>-media/bed.png,
  4. writes its page, with the slice's minutes and grams and the store price of its grams,
  5. records the recipe's iteration (manage-approvals' plate_approve.py --iterate, D-097).
A page that already carries a yes, a hold or a print is kept as it is, recipe and all: rewriting it
would lose that record. The run says so; change such a plate by hand, with --iterate.
Then it writes one page for the themes together: their plates, and the colors to buy with prices
from docs/design/coaster/themes/catalog/prices.yaml.

Usage:
    theme_plates.py <construction> <theme>... [--reuse]
        e.g. theme_plates.py gbv midnight-blue night-sky terracotta-souk iznik-tile
        --reuse   skip the slicing and use what build/themes/<theme>/ already holds
        The theme plates page lists only the themes named in the run, so name them all.
    theme_plates.py --self-test

Run it with BIKAR_DIR set to a built bikar checkout, as for every slice. The pages start at
`stage: waiting`: each send still needs Omar's yes (D-093).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import themes  # noqa: E402  the palette and the construction files
from swatch import shrink  # noqa: E402  the same picture size as every plate page

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "manage-approvals" / "scripts"))
import plate_approve as pa  # noqa: E402  the iteration and the approvals, as the plates gate reads them

ROOT = themes.ROOT
PLATES = ROOT / "docs" / "design" / "plates"
PRICES = ROOT / "docs" / "design" / "coaster" / "themes" / "catalog" / "prices.yaml"
CATALOG = PRICES.parent / "catalog.yaml"
# What a spool of more than one color does to a print, by the catalog's kind (catalog.py's header).
SPREAD = {
    "gradient": "the color shifts along the spool, so where it shifts on a given piece cannot be predicted",
    "multi": "its colors run side by side in the strand, so a piece can show either color, or both",
}
BUILD = ROOT / "build" / "themes"
BAMBU = ROOT / "tools" / "bambu" / "bin" / "bambu"
# The tier a buy is priced at: a refill where the store sells one, else a spool.
TIERS = ("refill", "spool")


def kv(params: dict) -> list[str]:
    return [f"{k}={v}" for k, v in params.items()]


def by_color_args(con: dict, theme: dict, pal: dict, out: Path) -> list[str]:
    """The `bambu plates by-color` call for one theme, every color named by its spool code."""
    def code(cid: str) -> str:
        c = pal.get(cid)
        if not c or not c.get("code"):
            raise SystemExit(f"{theme['id']}: color {cid} has no spool code in the palette")
        return str(c["code"])

    args = ["plates", "by-color", con["source"]["pieces"]]
    for p in kv(con["piece_params"]):
        args += ["--param", p]
    args += ["--frame", con["source"]["frame"]]
    for p in kv(con["params"]):
        args += ["--frame-param", p]
    args += ["--frame-color", code(theme["colors"][themes.FRAME])]
    for g in con["groups"]:
        args += ["--color", f"{g['piece']}={code(theme['colors'][g['id']])}"]
    return args + ["--name", f"theme-{theme['id']}", "-o", str(out), "--costs", "--slice"]


def slice_theme(con: dict, theme: dict, pal: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([str(BAMBU), *by_color_args(con, theme, pal, out)], cwd=ROOT,
                          capture_output=True, text=True, timeout=1800)
    if proc.returncode != 0:
        raise SystemExit(f"{theme['id']}: plates by-color failed:\n{proc.stdout}{proc.stderr}")


def plates_of(costs: dict) -> list[dict]:
    """The one-plate-per-color route's plates, the ones that become pages."""
    route = next(r for r in costs["routes"] if r["key"] == "per-color")
    return route["plates"]


def code_of(name: str) -> str:
    return name.rsplit("-", 1)[1]


def store_price(prices: dict, code: str) -> tuple[str, float] | None:
    row = (prices.get("colors") or {}).get(code)
    if not row:
        return None
    for t in TIERS:
        if t in row and t not in (row.get("out_of_stock") or []):
            return t, row[t]
    for t in TIERS:
        if t in row:
            return f"{t}, out of stock when read", row[t]
    return None


def flags(spool: dict, con: dict) -> list[str]:
    """What Omar should know before saying yes to this plate."""
    out = []
    gap = con["piece_params"].get("gap")
    if gap == 0:
        out.append(
            "**The pieces are cut at `gap: 0`, as sheets-04g printed them, and that fit was off:** the "
            "kites were too tight and the middle too loose. [sheets-04g-fit](sheets-04g-fit.md) tries "
            "kites from 0.05 to 0.25 mm and the middle from 0 to 0.15 mm, and has not printed "
            "(CAL-LSE-01). Printing this plate first repeats the old fit; printing the fit plate first "
            "lets these plates take its gaps, as a new iteration of each recipe.")
    if len(spool["hexes"]) > 1:
        shades = ", ".join(h[:7] for h in spool["hexes"])
        how = SPREAD.get(spool.get("kind"), "how its colors fall on a given piece cannot be predicted")
        out.append(
            f"**A {len(spool['hexes'])}-color spool ({shades}).** The color catalog files {spool['name']} as "
            f"{spool.get('kind', 'more than one color')}: {how}. The theme picture draws it as its first "
            "color only, and that is the color the send names, the one the AMS reports for the tray.")
    return out


def page_text(theme: dict, con: dict, plate: dict, spool: dict, line: str, owned: bool,
              n_plates: int, picture: str, today: str, iteration: int = 1) -> str:
    name = plate["name"]
    code = code_of(name)
    minutes = round(plate["minutes"])
    grams = plate["grams"]
    what = ", ".join(plate["what"])
    full = f"{line} {spool['name']} ({code})"
    usd = f"${plate['usd']:.2f} of filament" if plate.get("usd") is not None else "no price in the price file"
    have = ("On the printer now, so it can print as soon as you say yes." if owned
            else "Not on the printer: it prints once the spool is bought and loaded (see the buy list).")
    flag_lines = "\n".join(f"- {f}" for f in flags(spool, con)) or "- Nothing beyond the usual."
    note = "; ".join(plate.get("notes") or [])
    spill = f" {note}." if note else ""
    risk = "ok" if plate.get("sendable", True) else "watch"
    framed = [w for w in plate["what"] if w.lower().startswith("frame")]
    if framed and len(framed) == len(plate["what"]):
        laid = "One frame, flat on one bed, the frame sheets-04g printed at this size."
    elif framed:
        laid = "The frame and loose small pieces on one bed, as sheets-04g printed them."
    else:
        laid = "Loose small pieces on one bed, as sheets-04g printed them."
    one = len(plate["what"]) == 1 and plate["what"][0].endswith("×1")
    ask = f"does its {what} come out as the theme draws it" if one else f"do its {what} come out as the theme draws them"
    every = "in" if one else "every one in"
    return f"""---
plate: {name}
recipe: {name}.yaml
iteration: {iteration}
stage: waiting
times_printed: 0
runs: []
answers: "{theme['name']}, one of its {n_plates} plates: {ask}, in {full}?"
kind: taste
maturity: experiment
bets: []
unblocks: []
minutes: {minutes}
grams: {grams:g}
bed_plates: {plate.get('beds') or 1}
risk: {risk}
pictures:
  - {picture}
  - {name}-media/bed.png
---

# {name} — {theme['name']} in {spool['name']}

**In short.** You picked {theme['name']} as one of the first four themes to print (D-106: "all the
bottom row"). It prints as one plate per color, {n_plates} plates in all; this one is {full}:
{what}. {have} The plate is [`{name}.yaml`]({name}.yaml). One bed, {minutes} minutes, about
{grams:g} g, {usd}. The other plates and the colors to buy are on
[the theme plates page](../coaster/themes/{con['_folder'].name}-theme-plates.md).

## What it is

- **{what}**, {every} {full}, the {con['short']} coaster at sheets-04g's size
  ({con['params']['size']} mm).
- {theme['mood']}

**The color is picked at the send:** `bambu print send … --color "{spool['hexes'][0][:7].upper()}"`.
The recipe names no color (call 18), so say the color with the yes.

**Before you say yes:**

{flag_lines}

## Why print it

A theme on a screen is a guess at how the colors sit together. Printing its plates and putting the
pieces in the frame settles it for this theme. The persona scores beside each theme are simulated,
not customer research; these prints are the first thing to hold them against.

## Pictures

The theme as the gallery draws it.

![{theme['name']}: the {con['short']} coaster drawn flat in the theme's colors]({picture})

The slice: this plate's pieces on the bed.

![{name} on the bed: {what} in {spool['name']}]({name}-media/bed.png)

## Cost and risk

One bed, {minutes} minutes, about {grams:g} g, {usd} (local slice, {today}, the X2D preset and
{line}'s own filament preset, nothing sent).{spill} One color, so no swaps.

**Risk: {risk}.** {laid}

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
| {today} | proposed — {theme['name']} in {spool['name']}, by the color-themes skill's theme_plates.py (D-106) | this page |
| {today} | sliced — local slice, {minutes} minutes, {grams:g} g | this page |
"""


def money(x: float | None) -> str:
    return "—" if x is None else f"${x:.2f}"


def summary_text(con: dict, done: list[dict], pal: dict, cat: dict, prices: dict, today: str) -> str:
    """The themes' plates together, and the colors to buy for them."""
    rows, need = [], {}
    for t in done:
        theme, plates = t["theme"], t["plates"]
        mins = sum(p["minutes"] for p in plates)
        grams = sum(p["grams"] for p in plates)
        usd = None if any(p.get("usd") is None for p in plates) else sum(p["usd"] for p in plates)
        buy = [c for c in t["colors"] if not pal[c]["owned"]]
        links = ", ".join(f"[{code_of(p['name'])}](../../plates/{p['name']}.md)" for p in plates)
        rows.append(f"| {theme['name']} | {len(plates)} | {links} | {mins:.0f} | {grams:.1f} | {money(usd)} | "
                    f"{'none' if not buy else str(len(buy))} |")
        for p in plates:
            cid = t["by_code"][code_of(p["name"])]
            need.setdefault(cid, {})[theme["name"]] = p["grams"]

    buy_rows, owned_rows, total, mixed = [], [], 0.0, []
    for cid, n in sorted(need.items(), key=lambda kv: (pal[kv[0]]["owned"], str(pal[kv[0]]["code"]))):
        c, code = pal[cid], str(pal[cid]["code"])
        sp = store_price(prices, code)
        row = (prices.get("colors") or {}).get(code, {})
        spool = cat.get(code, {})
        label = spool.get("name", c["name"])
        if len(spool.get("hexes", [])) > 1:
            mixed.append(f"{label} ({code})")
        store = row.get("line") or c.get("line") or spool.get("line", "")
        price = "not in the price file" if sp is None else f"${sp[1]:.2f} ({sp[0]})"
        each = sorted({round(g, 1) for g in n.values()})
        most = max(n.values())
        per_kg = "—" if most == 0 else f"{1000 / most:.0f}"
        line = (f"| {code} | {label} | {store} | {', '.join(n)} | {' / '.join(f'{g:.1f}' for g in each)} | "
                f"{per_kg} | {price} |")
        if c["owned"]:
            owned_rows.append(line)
        else:
            buy_rows.append(line)
            total += sp[1] if sp else 0.0

    names = ", ".join(t["theme"]["name"] for t in done)
    spread = "".join(
        f"- **{m} is a spool of more than one color.** Its plate page says how the color catalog files it; "
        "its pieces will not all match the theme picture, which draws it as its first color only.\n"
        for m in mixed)
    return f"""# {con['short']} theme plates — the first themes to print, and what to buy

You picked the first themes to print on 2026-10-05 (D-106): "all the bottom row", that is {names}.
Each prints as one plate per color (D-103), so a theme is as many sends as it has colors. Every
plate below has its own page with its picture, its slice and an Approve box; each send still needs
your yes (D-093). Written by the color-themes skill's `theme_plates.py` on {today}, from local
slices; nothing was sent.

## The plates

Minutes and grams are each plate's own slice, warm-up included, added up for the theme; the
filament cost is those grams at the store prices read {prices['read']} ({prices['store']}).

| Theme | Plates | Each plate's page (by spool code) | Minutes | Grams | Filament | Colors to buy |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

Where two themes share a color (the black frame), each theme has its own plate for it, so a
theme's plates can be approved and sent on their own. The two frame plates are the same print.

## What to buy

One spool or refill of each, at the store's price when the prices were read. A refill is the
cheaper buy where the store sells one, and needs a reusable spool to sit on. "Coasters a kg" is
how many coasters one kilogram makes, from the grams one coaster's slice uses (the most, where
the themes using it differ).

| Code | Color | Store line | For | Grams a coaster | Coasters a kg | Price |
|---|---|---|---|---|---|---|
{chr(10).join(buy_rows)}

**One of each: ${total:.2f}**, before shipping and tax.

Already on the printer, so nothing to buy:

| Code | Color | Store line | For | Grams a coaster | Coasters a kg | Store price |
|---|---|---|---|---|---|---|
{chr(10).join(owned_rows)}

## Before printing any of them

- **The fit.** Every plate cuts its pieces at `gap: 0`, as sheets-04g did, and that fit was off:
  the kites too tight, the middle too loose. [sheets-04g-fit](../../plates/sheets-04g-fit.md) tries
  wider and narrower gaps and has not printed. Printing it first lets these plates take its gaps.
{spread}- **One color at a time.** The X2D holds four spools; a theme with more colors than are loaded
  needs a spool swapped between sends.
"""


def kept_because(page: Path) -> str | None:
    """Why a page must not be rewritten: a yes, a hold or a print on it would be lost."""
    if not page.is_file():
        return None
    text = page.read_text(encoding="utf-8")
    head = yaml.safe_load(text.split("---")[1]) or {}
    if head.get("times_printed") or head.get("runs"):
        return "it has prints"
    if pa.pg.approvals(text)[0]:
        return "it has rows in its Approvals table"
    if head.get("stage", "waiting") != "waiting":
        return f"its stage is {head['stage']}"
    return None


def iteration_of(name: str) -> int:
    """The iteration the page carries now; the --iterate after it moves it on if the recipe changed."""
    store = pa.it.store_for(PLATES)
    every, _ = pa.it.read_store(store) if store.is_file() else ({}, [])
    return len(every.get(name, [])) or 1


def record_iteration(page: Path, today: str) -> str:
    try:
        return pa.iterate(page, today)
    except pa.Refused as e:
        return f"{page.stem}: {e}"


def run(cid: str, theme_ids: list[str], reuse: bool) -> list[Path]:
    con = themes.construction(cid)
    pal = themes.palette()
    prices = yaml.safe_load(PRICES.read_text())
    cat = {str(e["code"]): e for e in yaml.safe_load(CATALOG.read_text())["colors"]}
    by_id = {t["id"]: t for t in con["themes"]}
    today = dt.date.today().isoformat()
    written, done = [], []
    for tid in theme_ids:
        theme = by_id.get(tid)
        if theme is None:
            raise SystemExit(f"{cid}: no theme {tid} in themes.yaml")
        out = BUILD / tid
        if not reuse:
            print(f"slicing {tid} …", flush=True)
            slice_theme(con, theme, pal, out)
        costs = json.loads((out / "costs.json").read_text())
        plates = plates_of(costs)
        colors = sorted(set(theme["colors"].values()))
        by_code = {str(pal[c]["code"]): c for c in colors}
        picture = os.path.relpath(con["_folder"] / f"{tid}.svg", PLATES)
        for p in plates:
            name = p["name"]
            cidc = by_code[code_of(name)]
            page = PLATES / f"{name}.md"
            why = kept_because(page)
            if why:
                print(f"kept {name} as it is: {why}", flush=True)
                continue
            shutil.copyfile(out / f"{name}.yaml", PLATES / f"{name}.yaml")
            media = PLATES / f"{name}-media"
            media.mkdir(exist_ok=True)
            shrink(out / f"{name}.plate.preview.png", media / "bed.png")
            page.write_text(page_text(theme, con, p, cat[code_of(name)], p["colors"][0]["line"], pal[cidc]["owned"],
                                      len(plates), picture, today, iteration_of(name)))
            print(record_iteration(page, today), flush=True)
            written.append(page)
        done.append({"theme": theme, "plates": plates, "colors": colors, "by_code": by_code})
    summary = themes.THEMES_DIR / f"{con['_folder'].name}-theme-plates.md"
    summary.write_text(summary_text(con, done, pal, cat, prices, today))
    written.append(summary)
    return written


def self_test() -> int:
    fails = []
    con = {"source": {"frame": "bikar:f.bkr", "pieces": "bikar:p.bkr"}, "short": "gBV",
           "params": {"size": 112.5}, "piece_params": {"size": 112.5, "gap": 0},
           "groups": [{"id": "kite", "piece": "Kite"}, {"id": "star", "piece": "Star"}],
           "_folder": Path("gbv")}
    pal = {"black": {"code": "10101", "name": "Black", "hexes": ["#000000"], "owned": True},
           "blue": {"code": "13903", "name": "Blue", "hexes": ["#0047BB", "#BB22A3"], "owned": True},
           "gold": {"code": "13402", "name": "Classic Gold Sparkle", "line": "PLA Sparkle",
                    "hexes": ["#E4BD68"], "owned": False}}
    theme = {"id": "t", "name": "T", "mood": "A test.", "colors": {"frame": "black", "kite": "blue", "star": "gold"}}
    args = by_color_args(con, theme, pal, Path("/o"))
    if args[args.index("--frame-color") + 1] != "10101":
        fails.append(f"the frame is not named by its code: {args}")
    if "Kite=13903" not in args or "Star=13402" not in args:
        fails.append(f"a group is not named by its code: {args}")
    if args[-2:] != ["--costs", "--slice"] or "theme-t" not in args:
        fails.append(f"the call does not slice and cost under the theme's name: {args}")
    try:
        by_color_args(con, {**theme, "colors": {**theme["colors"], "star": "nope"}}, pal, Path("/o"))
        fails.append("took a color with no code")
    except SystemExit:
        pass
    prices = {"read": "2026-10-05", "store": "bambu-us", "colors": {
        "13402": {"line": "PLA Sparkle", "spool": 24.99},
        "11600": {"line": "PLA Matte", "refill": 15.99, "spool": 18.99},
        "13902": {"line": "PLA Silk Multi-Color", "spool": 24.99, "out_of_stock": ["spool"]}}}
    if store_price(prices, "11600") != ("refill", 15.99) or store_price(prices, "13402") != ("spool", 24.99):
        fails.append("a buy is not priced as a refill where there is one, else a spool")
    if store_price(prices, "13902") != ("spool, out of stock when read", 24.99) or store_price(prices, "1") is not None:
        fails.append("out of stock or an unknown code read wrong")
    # The palette gives an owned spool one hex; the catalog has both of Neon City's, and its kind.
    cat = {"13903": {"code": "13903", "name": "Neon City", "hexes": ["#0047BBFF", "#BB22A3FF"], "kind": "multi"},
           "13402": {"code": "13402", "name": "Classic Gold Sparkle", "hexes": ["#E4BD68FF"], "kind": "single"},
           "10101": {"code": "10101", "line": "PLA Basic", "name": "Black", "hexes": ["#000000FF"], "kind": "single"}}
    plate = {"name": "theme-t-13903", "minutes": 36.3, "grams": 11.78, "usd": 0.29, "what": ["Kite ×10"],
             "beds": 1, "sendable": True, "notes": [], "colors": [{"line": "PLA Silk"}]}
    page = page_text(theme, con, plate, cat["13903"], "PLA Silk", True, 3, "../t.svg", "2026-10-05")
    head = yaml.safe_load(page.split("---")[1])
    if head["plate"] != "theme-t-13903" or head["minutes"] != 36 or head["stage"] != "waiting":
        fails.append(f"page frontmatter wrong: {head}")
    if "A 2-color spool (#0047BB, #BB22A3)" not in page or "side by side in the strand" not in page or "gap: 0" not in page:
        fails.append("the page does not flag the two-color spool by its kind, and the gap")
    if "PLA Silk Neon City (13903)" not in page or "$0.29 of filament" not in page:
        fails.append("the page does not name the spool by the catalog, or carry its filament cost")
    # Call 18: the recipe names no color, so the page says which one to name at the send.
    if '--color "#0047BB"`' not in page or "sliced as that color" in page:
        fails.append("the page does not say the color is picked at the send, by the spool's first hex")
    gold = {**plate, "name": "theme-t-13402", "usd": None, "grams": 2.2}
    gpage = page_text(theme, con, gold, cat["13402"], "PLA Sparkle", False, 3, "../t.svg", "2026-10-05")
    if "-color spool" in gpage or "Not on the printer" not in gpage or "no price in the price file" not in gpage:
        fails.append("a one-color bought spool is flagged or priced wrong")
    # Two themes share the black frame: its grams are one coaster's, not the two added up.
    frame = {**plate, "name": "theme-t-10101", "grams": 16.0}
    fpage = page_text(theme, con, {**frame, "what": ["frame ×1"]}, cat["10101"], "PLA Basic", True, 3,
                      "../t.svg", "2026-10-05")
    if "One frame, flat on one bed" not in fpage or "does its frame ×1 come out as the theme draws it," not in fpage:
        fails.append("a frame plate is described as loose pieces")
    if "Loose small pieces on one bed" not in page or "simulated,\nnot customer research" not in page:
        fails.append("a piece plate lost its risk line, or the persona scores are not called simulated")
    # A page with a yes on it is kept: rewriting it would drop the row.
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        fresh, yes = Path(d) / "fresh.md", Path(d) / "yes.md"
        fresh.write_text(page)
        yes.write_text(page.replace("|---|---|---|---|---|\n",
                                    "|---|---|---|---|---|\n| 2026-10-06 | approved | Omar, in chat | iteration 1 | |\n"))
        if kept_because(fresh) is not None or kept_because(yes) != "it has rows in its Approvals table":
            fails.append(f"the keep check is wrong: {kept_because(fresh)!r}, {kept_because(yes)!r}")
    other = {**theme, "name": "U"}
    done = [{"theme": theme, "plates": [plate, gold, frame], "colors": ["black", "blue", "gold"],
             "by_code": {"13903": "blue", "13402": "gold", "10101": "black"}},
            {"theme": other, "plates": [{**frame, "name": "theme-u-10101"}], "colors": ["black"],
             "by_code": {"10101": "black"}}]
    s = summary_text(con, done, pal, cat, prices, "2026-10-05")
    if "**One of each: $24.99**" not in s:
        fails.append("the buy list total is not the bought colors' prices")
    owned = s.split("Already on the printer")[1]
    if "| 13903 | Neon City |" not in owned:
        fails.append("an owned color is not listed as owned, by its catalog name")
    if "| 10101 | Black | PLA Basic | T, U | 16.0 | 62 |" not in owned:
        fails.append("a color two themes share is not one coaster's grams")
    if "Neon City (13903) is a spool of more than one color" not in s:
        fails.append("the summary does not flag the two-color spool")
    for f in fails:
        print(f"FAIL: {f}")
    print(f"theme_plates self-test: {'ok' if not fails else f'{len(fails)} failed'}")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("construction", nargs="?")
    ap.add_argument("themes", nargs="*")
    ap.add_argument("--reuse", action="store_true", help="use the slices build/themes/<theme>/ holds")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.construction or not a.themes:
        ap.print_help()
        return 2
    for p in run(a.construction, a.themes, a.reuse):
        print(p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
