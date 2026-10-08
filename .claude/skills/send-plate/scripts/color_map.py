#!/usr/bin/env python3
"""Map a Lab design's colors to the loaded trays before any send, and ask about each one that does not fit.

docs/design/coaster/print-time-color-map-design.md, build step 3 (§3, §4, §5, §10). Omar's call 19
(2026-10-08): when the skill takes a Lab design to print, it reads the trays, maps each design
color to a loaded tray, and asks one question per color that does not fit: load it, use the
nearest, or stop. One plate per color (call 16); each send names its color (call 18).

The matching is not done here. It is `bambu filament map`, which runs the send's own `reconcile`
over every design color at once, so a tray goes to at most one color and the plan agrees with the
send (§3). This script runs that command, keeps the answers, writes the plate pages' color block,
and checks the result plate by plate. It never sends, never writes a yes, and never changes a
printer setting: the only printer call it makes is the read-only tray read inside `filament map`,
and with `--trays <file>` it makes none.

The skill asks the questions (AskUserQuestion), one at a time; this script cannot. So the work is
in steps, each a plain command:

    color_map.py plan <pieces.bkr> [plates by-color options …] [--trays <file>] [--out <dir>]
    color_map.py plan --by-color <by-color.json> [--trays <file>] [--out <dir>]
        Runs `bambu plates by-color … --json` (or reads its saved output), then
        `bambu filament map --colors … --json`, and writes color-map.json beside the recipes in
        build/ (the folder of the by-color rows' paths, or --out). Prints one question per row
        that needs one, as JSON with --json.
    color_map.py answer <color-map.json> <plate> <answer> [--trays <file>]
        Records Omar's answer to that plate's question. The answers a row offers are in its
        question: tray / runner-up (a near tie), nearest (use the nearest tray), load (he loads
        it now: the trays are read again and every color mapped again), later (he loads it
        before that plate's send), stop (nothing more is mapped and no page is written).
    color_map.py pages <color-map.json> [--plates <dir>]
        Once every question is answered: writes the color block on each plate page that exists
        (docs/design/plates/<plate>.md whose recipe is the one mapped), then checks, and prints
        each send's --color.
    color_map.py check <color-map.json> [--plates <dir>]
        The §10 validator, plate by plate.
    color_map.py --self-test

Run it from the repo root, with BIKAR_DIR set for `plan <pieces.bkr>` as for any by-color run.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BAMBU = ROOT / "tools" / "bambu" / "bin" / "bambu"
PLATES = ROOT / "docs" / "design" / "plates"
MAP_FILE = "color-map.json"
BY_COLOR_FILE = "by-color.json"
START, END = "<!-- color-map:start -->", "<!-- color-map:end -->"
SCRIPT = ".claude/skills/send-plate/scripts/color_map.py"

sys.path.insert(0, str(ROOT / ".claude" / "skills" / "manage-approvals" / "scripts"))
from iterations import hash_text  # noqa: E402  the recipe hash the pages and the send read

# The statuses `reconcile` gives that need no question (§4's table): mapped as they are.
NO_QUESTION = ("matched", "low-remain")
# The answers that give a plate a tray to print from.
SENDS = ("auto", "tray", "runner-up", "nearest")


# --- the bambu command ------------------------------------------------------------------------

def bambu(args: list[str]) -> str:
    """Run the bambu command and return what it printed. Read-only verbs only reach here."""
    if not (ROOT / "tools" / "bambu" / "node_modules").is_dir():
        raise SystemExit("tools/bambu has no node_modules: run `npm --prefix tools/bambu ci` first")
    proc = subprocess.run([str(BAMBU), *args], cwd=ROOT, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        raise SystemExit(f"bambu {' '.join(args[:2])} failed (exit {proc.returncode}):\n{proc.stdout}{proc.stderr}")
    return proc.stdout


def filament_map(by_color: Path, trays: str | None) -> dict:
    args = ["filament", "map", "--colors", str(by_color), "--json"]
    if trays:
        args += ["--trays", trays]
    return json.loads(bambu(args))


# --- the rows -----------------------------------------------------------------------------------

def tray_text(t: dict) -> str:
    tag = ", no tag: its color was set by hand" if t.get("tagged") is False else ""
    left = f", {t['remain']}% left" if isinstance(t.get("remain"), int) and t["remain"] >= 0 else ""
    return f"{t['where']} ({' '.join(x for x in (t.get('type'), t.get('hex') or 'no color') if x)}{left}{tag})"


def dist(n: float | None) -> str:
    return "?" if n is None else f"{n:.0f}"


def question(row: dict) -> dict | None:
    """The one question a row needs, with the options it offers, or None (§4, §5)."""
    status = row["status"]
    if status in NO_QUESTION:
        return None
    head = f"{row['design_hex']} ({', '.join(row['groups']) or 'no group'}, plate {row['name']})"
    opts: list[dict] = []
    if status == "missing":
        n = row.get("nearest")
        text = f"{head}: no free tray within the send's match distance."
        opts.append({"answer": "load", "label": "Load it now",
                     "says": "load the spool, then the trays are read again and every color mapped again"})
        opts.append({"answer": "later", "label": "Load it before this plate's send",
                     "says": "the plate waits with no color; map again before its send"})
        if n:
            text += f" Nearest: {tray_text(n)}, distance {dist(n['distance'])}."
            say = f"prints in {n['hex']}, not the designed {row['design_hex']}"
            if n.get("taken_by"):
                text += f" That tray already went to {n['taken_by']}."
                say += f"; {n['taken_by']} prints from the same tray, so two groups come out one color"
            opts.append({"answer": "nearest", "label": f"Use the nearest ({n['hex']})", "says": say})
        else:
            text += " No tray is loaded."
    elif status == "ambiguous":
        t, r = row["tray"], row["runner_up"]
        text = (f"{head}: two trays are too close to call: {tray_text(t)}, distance {dist(row['distance'])}, "
                f"and {tray_text(r)}, distance {dist(r['distance'])}.")
        opts.append({"answer": "tray", "label": f"{t['where']} ({t['hex']})", "says": f"prints in {t['hex']}"})
        opts.append({"answer": "runner-up", "label": f"{r['where']} ({r['hex']})", "says": f"prints in {r['hex']}"})
    else:  # material-mismatch: the map gives no material, so only a hand-made map reaches this
        t = row["tray"]
        text = f"{head}: the close tray, {tray_text(t)}, holds a different material."
        opts.append({"answer": "load", "label": "Load the right material",
                     "says": "load it, then the trays are read again and every color mapped again"})
        opts.append({"answer": "tray", "label": "Use it anyway", "says": f"prints in {t['hex']} from that material"})
    opts.append({"answer": "stop", "label": "Stop", "says": "nothing more is mapped and no page is written; nothing was sent"})
    return {"plate": row["name"], "text": text, "options": opts}


def settle(row: dict) -> dict:
    """The row as the map gave it, with its question, or mapped as it is when it needs none."""
    q = question(row)
    row["question"] = q
    if q is None:
        row["answer"], row["send_tray"] = "auto", row["tray"]
    else:
        row["answer"], row["send_tray"] = None, None
    row["color"] = row["send_tray"]["hex"] if row["send_tray"] else None
    return row


def same_choice(a: dict, b: dict) -> bool:
    """Whether a row is offered the same thing it was offered before the trays were read again."""
    key = lambda r: (r["status"], *(  # noqa: E731
        (t or {}).get(k) for t in (r.get("tray"), r.get("runner_up"), r.get("nearest")) for k in ("index", "hex")),
        (r.get("nearest") or {}).get("taken_by"))
    return key(a) == key(b)


def build(by_color: Path, fmap: dict, earlier: dict | None = None) -> dict:
    """color-map.json from the by-color rows and the `filament map` output. An answer given before
    the trays were read again is kept only when that row is offered exactly what it was before;
    otherwise it is asked again. A `load` answer is never kept: the load is what was re-read."""
    hashes = {r["name"]: r.get("recipe_hash") for r in json.loads(by_color.read_text())}
    old = {r["name"]: r for r in (earlier or {}).get("rows", [])}
    rows = []
    for r in fmap["rows"]:
        row = settle({**r, "recipe_hash": hashes.get(r["name"])})
        prev = old.get(row["name"])
        if row["question"] and prev and prev.get("answer") not in (None, "load") and same_choice(prev, row):
            row["answer"], row["send_tray"], row["color"] = prev["answer"], prev.get("send_tray"), prev.get("color")
        rows.append(row)
    return {"made_by": SCRIPT, "by_color": str(by_color), "read_at": fmap.get("read_at"),
            "trays_from": fmap.get("trays_from"), "trays": fmap.get("trays", []),
            "stopped": False, "rows": rows}


def pending(m: dict) -> list[dict]:
    return [r for r in m["rows"] if r["question"] and r["answer"] is None]


# --- plan, answer -------------------------------------------------------------------------------

def out_dir(by_color_rows: list[dict], given: str | None) -> Path:
    if given:
        return Path(given).resolve()
    paths = [r.get("path") for r in by_color_rows if r.get("path")]
    if not paths:
        raise SystemExit("the by-color rows give no recipe path: pass --out <dir>")
    return Path(paths[0]).resolve().parent


def plan(pieces: str | None, by_color_args: list[str], by_color_file: str | None, trays: str | None,
         out: str | None) -> Path:
    if by_color_file:
        src = Path(by_color_file).resolve()
        rows = json.loads(src.read_text())
        where = out_dir(rows, out)
    else:
        if not pieces:
            raise SystemExit("plan needs a pieces .bkr, or --by-color <file>")
        rows = json.loads(bambu(["plates", "by-color", pieces, *by_color_args, "--json"]))
        where = out_dir(rows, out)
        src = where / BY_COLOR_FILE
        where.mkdir(parents=True, exist_ok=True)
        src.write_text(json.dumps(rows, indent=2) + "\n")
    m = build(src, filament_map(src, trays))
    where.mkdir(parents=True, exist_ok=True)
    path = where / MAP_FILE
    save(path, m)
    return path


def save(path: Path, m: dict) -> None:
    path.write_text(json.dumps(m, indent=2) + "\n")


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def answer(path: Path, plate: str, ans: str, trays: str | None) -> dict:
    m = load(path)
    if m.get("stopped"):
        raise SystemExit(f"{path}: the map was stopped; plan again to start over")
    row = next((r for r in m["rows"] if r["name"] == plate), None)
    if row is None:
        raise SystemExit(f"no plate {plate} in {path} (its plates: {', '.join(r['name'] for r in m['rows'])})")
    if not row["question"]:
        raise SystemExit(f"{plate} needs no question: it is {row['status']} to {row['tray']['where']}")
    offered = [o["answer"] for o in row["question"]["options"]]
    if ans not in offered:
        raise SystemExit(f"{plate}: '{ans}' is not one of its answers ({', '.join(offered)})")
    if ans == "stop":
        row["answer"], m["stopped"] = "stop", True
    elif ans == "load":
        # He loaded the spool: read the trays again and map every color again, since loading one
        # spool can unload another (§4).
        row["answer"] = "load"
        m = build(Path(m["by_color"]), filament_map(Path(m["by_color"]), trays), m)
    elif ans == "later":
        row["answer"], row["send_tray"], row["color"] = "later", None, None
    else:
        pick = {"tray": row.get("tray"), "runner-up": row.get("runner_up"), "nearest": row.get("nearest")}[ans]
        tray = {k: v for k, v in pick.items() if k not in ("distance", "taken_by")}
        row["answer"], row["send_tray"], row["color"] = ans, tray, tray["hex"]
    row_now = next((r for r in m["rows"] if r["name"] == plate), row)
    row_now.setdefault("answered_at", None)
    if ans != "load":
        row_now["answered_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    save(path, m)
    return m


# --- the §10 check ------------------------------------------------------------------------------

def check(m: dict, plates: Path | None = None) -> tuple[list[str], list[str]]:
    """(failures, notices), plate by plate (§10). A count of plates against a count of colors does
    not discharge it: each design color must have its own row, its own answer, a --color equal to
    the tray it prints from, and no tray hex shared with another plate unless Omar chose it."""
    fails: list[str] = []
    notes: list[str] = []
    if m.get("stopped"):
        fails.append("the map was stopped: nothing is planned to send")
    try:
        names = [r["name"] for r in json.loads(Path(m["by_color"]).read_text())]
    except (OSError, ValueError, KeyError) as e:
        fails.append(f"cannot read the by-color rows the map was made from: {e}")
        names = []
    rows = m["rows"]
    for n in names:
        k = sum(1 for r in rows if r["name"] == n)
        if k != 1:
            fails.append(f"{n}: {k} rows in the map, not one")
    for r in rows:
        if r["name"] not in names:
            fails.append(f"{r['name']}: in the map but not in the by-color rows")
    by_hex: dict[str, list[dict]] = {}
    for r in rows:
        a = r.get("answer")
        if a is None:
            fails.append(f"{r['name']}: its question is not answered yet")
        elif a == "later":
            notes.append(f"{r['name']}: {r['design_hex']} is to be loaded before its send; map again then")
        elif a in SENDS:
            t = r.get("send_tray") or {}
            if not r.get("color") or r["color"] != t.get("hex"):
                fails.append(f"{r['name']}: --color {r.get('color')} is not the hex of the tray it prints from ({t.get('hex')})")
            else:
                by_hex.setdefault(r["color"], []).append(r)
    for hex_, group in by_hex.items():
        # Sharing a tray is allowed only when every plate that came to share it, beyond the one
        # that holds it, was Omar's "use the nearest", asked with the holder named (§4).
        chosen = [r for r in group if r["answer"] == "nearest"]
        if len(group) > 1 and len(group) - len(chosen) > 1:
            fails.append(f"{' and '.join(r['name'] for r in group)} all on the {hex_} tray, and not by Omar's 'use the nearest'")
    if plates is not None:
        for r in rows:
            page = plates / f"{r['name']}.md"
            if not page.exists():
                notes.append(f"{r['name']}: no plate page yet")
                continue
            block = page_block(page.read_text())
            if block is None:
                notes.append(f"{r['name']}: its page has no color block yet (run pages)")
            elif r.get("color") and f"`--color \"{r['color']}\"`" not in block:
                fails.append(f"{r['name']}: its page's color block does not name {r['color']}")
    return fails, notes


# --- the pages ----------------------------------------------------------------------------------

def page_block(text: str) -> str | None:
    if START not in text or END not in text:
        return None
    return text[text.index(START): text.index(END) + len(END)]


def block_for(r: dict, m: dict) -> str:
    when = m.get("read_at") or "an unknown time"
    src = "from the printer" if m.get("trays_from") == "printer" else f"from the saved list {m.get('trays_from')}"
    head = f"**Color map** (the send-plate skill's `color_map.py`; trays read {when}, {src}). Designed in {r['design_hex']}"
    t = r.get("send_tray")
    if r["answer"] == "later":
        body = (f"{head}, which no tray holds yet. Load it before this plate's send, then map again; "
                "the send names no color until then.")
    else:
        why = {"auto": "it matched" if r["status"] == "matched" else "it matched, on a spool running low", "tray": "Omar picked this tray of two close ones",
               "runner-up": "Omar picked this tray of two close ones",
               "nearest": "the nearest tray, as Omar answered"}[r["answer"]]
        same = "" if t["hex"] == r["design_hex"] else f", not the designed {r['design_hex']}"
        low = (f" Only {t['remain']}% is left on that spool."
               if r["status"] == "low-remain" and isinstance(t.get("remain"), int) else "")
        body = (f"{head}; prints from {tray_text(t)} in {t['hex']}{same} ({why}).{low} "
                f"Send it with `--color \"{t['hex']}\"`, and record the yes with the same `--color`.")
    return f"{START}\n{body}\n{END}"


def put_block(text: str, block: str) -> str:
    old = page_block(text)
    if old is not None:
        return text.replace(old, block)
    for anchor in ("\n## Your call", "\n## Approvals"):
        if anchor in text:
            i = text.index(anchor)
            return f"{text[:i]}\n{block}\n{text[i:]}"
    return f"{text.rstrip()}\n\n{block}\n"


def pages(path: Path, plates: Path) -> tuple[list[str], list[str], list[str]]:
    """(written, skipped with why, the send lines). Refuses while a question is open or stopped."""
    m = load(path)
    if m.get("stopped"):
        raise SystemExit("the map was stopped: no page is written (§5)")
    open_ = pending(m)
    if open_:
        raise SystemExit(f"answer these first: {', '.join(r['name'] for r in open_)}")
    written, skipped, sends = [], [], []
    for r in m["rows"]:
        page = plates / f"{r['name']}.md"
        recipe = page.with_suffix(".yaml")
        if not page.exists() or not recipe.exists():
            skipped.append(f"{r['name']}: no plate page yet; write its page first, then run pages again")
        elif r.get("recipe_hash") and hash_text(recipe.read_text()) != r["recipe_hash"]:
            skipped.append(f"{r['name']}: the page's recipe is not the one mapped (hash differs); left as it is")
        else:
            page.write_text(put_block(page.read_text(), block_for(r, m)))
            written.append(str(page))
        if r.get("color"):
            sends.append(f"{r['name']}: --color \"{r['color']}\"")
        else:
            sends.append(f"{r['name']}: no color yet (load {r['design_hex']} before its send, then map again)")
    return written, skipped, sends


# --- the self-test ------------------------------------------------------------------------------

PINK, BLACK, WHITE, GOLD, TAN = "#F5547C", "#000000", "#FFFFFF", "#C8A24A", "#C9A44C"
CON = "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr"


def _by_color(d: Path, rows: list[tuple[str, str | None]]) -> Path:
    """A by-color run as `bambu plates by-color --json` prints it, with its recipes on disk."""
    out = []
    for hex_, piece in rows:
        name = f"test-by-color-{hex_[1:].lower()}"
        recipe = d / f"{name}.yaml"
        item = f"  - bkr: {CON}\n    params: {{ size: 112.5 }}\n" + (f"    piece: {piece}\n" if piece else "")
        recipe.write_text(f"bed: x2d\nitems:\n{item}")
        out.append({"name": name, "path": str(recipe), "recipe_hash": hash_text(recipe.read_text()), "color": hex_,
                    "items": [{"construction": CON, "params": {"size": 112.5}, "piece": piece, "count": 1}]})
    f = d / BY_COLOR_FILE
    f.write_text(json.dumps(out, indent=2))
    return f


def _trays(d: Path, name: str, slots: list[str | None]) -> str:
    """Made-up trays in the shape `bambu filament --json` prints."""
    tray = [{"id": str(i), "tray_type": "PLA", "tray_color": f"{c[1:]}FF", "remain": 80} if c else {"id": str(i), "state": 0}
            for i, c in enumerate(slots)]
    f = d / name
    f.write_text(json.dumps({"ams": {"ams": [{"id": "0", "tray": tray}]},
                             "vir_slot": [{"id": "254", "tray_type": "", "tray_color": "00000000"}]}))
    return str(f)


def _page(plates: Path, recipe: Path) -> Path:
    shutil.copyfile(recipe, plates / recipe.name)
    page = plates / f"{recipe.stem}.md"
    page.write_text(f"# {recipe.stem}\n\n## What it is\n\nA test plate.\n\n## Your call\n\n- [ ] **Approve**\n\n## Approvals\n")
    return page


def self_test() -> int:
    fails: list[str] = []

    def expect(cond: bool, what: str) -> None:
        if not cond:
            fails.append(what)

    def refused(fn, what: str, needle: str) -> None:
        try:
            fn()
        except SystemExit as e:
            expect(needle in str(e), f"{what}: refused, but not saying '{needle}': {e}")
            return
        fails.append(f"{what}: not refused")

    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp).resolve()  # macOS: /var is a link to /private/var

        # §10 PASS: a three-color gBV design, pink and black loaded, gold missing.
        d = t / "pass"
        d.mkdir()
        plates = d / "plates"
        plates.mkdir()
        bc = _by_color(d, [(PINK, "Kite"), (BLACK, "Star"), (GOLD, None)])
        first = _trays(d, "trays-1.json", [WHITE, PINK, None, BLACK])
        path = plan(None, [], str(bc), first, None)
        expect(path == d / MAP_FILE, f"color-map.json beside the recipes, got {path}")
        m = load(path)
        row = {r["design_hex"]: r for r in m["rows"]}
        expect((row[PINK]["answer"], row[PINK]["send_tray"]["index"]) == ("auto", 1), f"pink: {row[PINK]['answer']}")
        expect((row[BLACK]["answer"], row[BLACK]["send_tray"]["index"]) == ("auto", 3), "black on tray 3")
        q = row[GOLD]["question"]
        expect(q is not None and [o["answer"] for o in q["options"]] == ["load", "later", "nearest", "stop"],
               f"gold's options: {q and [o['answer'] for o in q['options']]}")
        expect(q is not None and "already went to test-by-color-f5547c" in q["text"],
               "gold's question names that the nearest tray is pink's")
        expect(m["trays_from"] == first, "the map says its trays came from the file")
        f, _ = check(m)
        expect(any("gold" in x or "c8a24a" in x for x in f), f"an open question fails the check: {f}")
        refused(lambda: pages(path, plates), "pages before gold is answered", "answer these first")
        refused(lambda: answer(path, "test-by-color-f5547c", "nearest", None), "a question pink was never asked",
                "needs no question")
        refused(lambda: answer(path, "test-by-color-c8a24a", "runner-up", None), "an answer gold was not offered",
                "not one of its answers")
        # Omar loads gold; the trays are read again and every color mapped again.
        m = answer(path, "test-by-color-c8a24a", "load", _trays(d, "trays-2.json", [WHITE, PINK, GOLD, BLACK]))
        expect([(r["design_hex"], r["answer"], r["send_tray"]["index"]) for r in m["rows"]]
               == [(PINK, "auto", 1), (BLACK, "auto", 3), (GOLD, "auto", 2)],
               f"after the load: {[(r['design_hex'], r['answer']) for r in m['rows']]}")
        pages_of = {r["name"]: _page(plates, Path(r["path"])) for r in json.loads(bc.read_text())}
        written, skipped, sends = pages(path, plates)
        expect(len(written) == 3 and not skipped, f"three pages written: {written} {skipped}")
        colors = [s.split("--color ")[1] for s in sends]
        expect(sorted(colors) == sorted(f'"{h}"' for h in (PINK, BLACK, GOLD)), f"three different --colors: {sends}")
        for name, page in pages_of.items():
            r = next(x for x in m["rows"] if x["name"] == name)
            text = page.read_text()
            expect(f"`--color \"{r['send_tray']['hex']}\"`" in text, f"{name}'s page names its tray hex")
            expect(text.index(START) < text.index("## Your call"), f"{name}'s block sits before Your call")
        f, n = check(load(path), plates)
        expect(not f, f"§10 PASS checks clean: {f}")
        again = pages_of["test-by-color-000000"].read_text()
        pages(path, plates)
        expect(pages_of["test-by-color-000000"].read_text() == again, "a second pages run changes nothing")
        # A page whose recipe is not the one mapped is left alone.
        other = pages_of["test-by-color-f5547c"].with_suffix(".yaml")
        other.write_text(other.read_text() + "  - bkr: other.bkr\n")
        _, skipped, _ = pages(path, plates)
        expect(any("hash differs" in s for s in skipped), f"a changed recipe's page is skipped: {skipped}")

        # §10 FAIL: gold and tan, one gold tray loaded.
        d = t / "fail"
        d.mkdir()
        bc = _by_color(d, [(GOLD, "Kite"), (TAN, "Star")])
        loaded = _trays(d, "trays.json", [GOLD, BLACK, WHITE])
        path = plan(None, [], str(bc), loaded, None)
        m = load(path)
        gold, tan = m["rows"]
        expect((gold["answer"], gold["send_tray"]["index"]) == ("auto", 0), "gold keeps the gold tray")
        expect(tan["status"] == "missing" and tan["question"] is not None, "tan is asked, not given the gold tray")
        expect("already went to test-by-color-c8a24a" in tan["question"]["text"],
               "tan's question says gold and tan both want the gold tray")
        # A matcher that took each color's nearest tray on its own: both on the gold tray. Three
        # plates for three colors would pass a count; the per-plate check must not.
        alone = json.loads(json.dumps(m))
        alone["rows"][1].update(status="matched", answer="auto", tray=gold["tray"], send_tray=gold["tray"],
                                color=gold["tray"]["hex"], question=None)
        f, _ = check(alone)
        expect(any("all on the #C8A24A tray" in x for x in f), f"§10 FAIL: two plates on one tray must fail: {f}")
        # A --color that is not its tray's hex fails too.
        wrong = json.loads(json.dumps(m))
        wrong["rows"][0]["color"] = TAN
        f, _ = check(wrong)
        expect(any("is not the hex of the tray" in x for x in f), f"a --color off its tray fails: {f}")
        # Omar answering "use the nearest", told that gold holds it, is his call: it passes.
        m = answer(path, "test-by-color-c9a44c", "nearest", None)
        f, _ = check(m)
        expect(not f, f"tan on gold's tray by Omar's 'use the nearest' passes: {f}")
        expect(m["rows"][1]["color"] == GOLD, "tan prints in the gold tray's hex")
        # Stop: nothing more is mapped and no page is written.
        path2 = plan(None, [], str(bc), loaded, str(d / "again"))
        answer(path2, "test-by-color-c9a44c", "stop", None)
        refused(lambda: pages(path2, d), "pages after stop", "stopped")
        f, _ = check(load(path2))
        expect(any("stopped" in x for x in f), "a stopped map fails the check")
        # Later: the plate waits with no color, which is a notice, not a pass to send.
        path3 = plan(None, [], str(bc), loaded, str(d / "later"))
        m = answer(path3, "test-by-color-c9a44c", "later", None)
        f, n = check(m)
        expect(not f and any("before its send" in x for x in n), f"later is a notice: {f} {n}")
        expect(m["rows"][1]["color"] is None, "a later plate has no --color")

    for x in fails:
        print(f"FAIL {x}")
    print(f"color_map self-test: {'ok' if not fails else f'{len(fails)} failure(s)'}")
    return 1 if fails else 0


# --- the command line ---------------------------------------------------------------------------

def main() -> int:
    if sys.argv[1:] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="map each design color to a loaded tray and list the questions")
    p.add_argument("pieces", nargs="?", help="the Lab's pieces .bkr, as `bambu plates by-color` takes it")
    p.add_argument("--by-color", help="a saved `bambu plates by-color --json`, in place of running it")
    p.add_argument("--trays", help="a saved `bambu filament --json`, in place of reading the printer")
    p.add_argument("--out", help="where color-map.json goes (default: beside the recipes)")
    p.add_argument("--json", action="store_true", help="print the questions as JSON")
    a = sub.add_parser("answer", help="record Omar's answer to one plate's question")
    a.add_argument("map")
    a.add_argument("plate")
    a.add_argument("answer", choices=("tray", "runner-up", "nearest", "load", "later", "stop"))
    a.add_argument("--trays", help="for load: a saved `bambu filament --json`, in place of reading the printer")
    g = sub.add_parser("pages", help="write the color block on each plate page, then check")
    g.add_argument("map")
    g.add_argument("--plates", default=str(PLATES))
    c = sub.add_parser("check", help="the §10 check, plate by plate")
    c.add_argument("map")
    c.add_argument("--plates", default=str(PLATES))
    args, rest = ap.parse_known_args()
    if rest and args.cmd != "plan":
        ap.error(f"unrecognized arguments: {' '.join(rest)}")

    if args.cmd in ("plan", "answer"):
        if args.cmd == "plan":
            path = plan(args.pieces, rest, args.by_color, args.trays, args.out)
        else:
            path = Path(args.map)
            answer(path, args.plate, args.answer, args.trays)
        m = load(path)
        qs = [r["question"] for r in pending(m)]
        if getattr(args, "json", False):
            print(json.dumps({"map": str(path), "stopped": m["stopped"], "questions": qs}, indent=2))
            return 0
        for r in m["rows"]:
            state = r["answer"] or "ASK"
            where = r["send_tray"]["where"] if r.get("send_tray") else "no tray"
            print(f"[{state:9}] {r['design_hex']} {r['name']} → {where}{' ' + r['color'] if r.get('color') else ''}")
        for q in qs:
            print(f"\nASK {q['plate']}: {q['text']}")
            for o in q["options"]:
                print(f"  {o['answer']:9} {o['label']}: {o['says']}")
        print(f"\n{path}" + (" (stopped)" if m["stopped"] else ""))
        return 0
    if args.cmd == "pages":
        written, skipped, sends = pages(Path(args.map), Path(args.plates))
        for w in written:
            print(f"wrote the color block on {w}")
        for s in skipped:
            print(f"skipped {s}")
        print("\nEach send names its color:")
        for s in sends:
            print(f"  {s}")
    f, n = check(load(args.map), Path(args.plates))
    for x in n:
        print(f"note {x}")
    for x in f:
        print(f"FAIL {x}")
    print(f"check: {'ok' if not f else f'{len(f)} failure(s)'}")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
