#!/usr/bin/env python3
"""A plate's after-print questions as data, and Omar's answers written back onto its page.

    python3 .claude/skills/review-print/scripts/after_print.py questions <plate> [--json]
                                    the page's `## After the print` rows, each split into the pieces
                                    to pick up, the pieces to hold them against, the lead paragraph
                                    and pictures before Do, Do, Look for, what we expect, and one answer per outcome the last cell names; with
                                    every piece's label and turn from the recipe and bed map, its
                                    tile, a photo when a print record has one, and the answers so far
    python3 .claude/skills/review-print/scripts/after_print.py answer <plate> <row> <answer> [-n "<his words>"] [--date YYYY-MM-DD]
                                    one answer into the page's `## Judged` table, word for word;
                                    <answer> is one of the row's outcomes, or "not judged yet"
    python3 .claude/skills/review-print/scripts/after_print.py waiting [--json]
                                    the plates whose print finished and whose questions are not all
                                    answered: what the hub page lists
    python3 .claude/skills/review-print/scripts/after_print.py pieces <plate> [--build-dir build/plates]
                                    one picture per piece, cut from the bed drawing, into
                                    `<plate>-media/pieces/<id>.png` beside the page
    python3 .claude/skills/review-print/scripts/after_print.py measure
                                    every page's rows through the parser; prints each cell it cannot
                                    read fully, exits 1 if there is one
    python3 .claude/skills/review-print/scripts/after_print.py plate <plate> note|reprint -n "<his words>"
                                    one line about the whole plate into the page's `## On the whole
                                    plate` table: a general note, or a reprint he asks for (pieces
                                    lost or broken), word for word
    python3 .claude/skills/review-print/scripts/after_print.py --self-test

Why this exists (Omar, 2026-10-22): judging from a chat question gives no picture and no piece
ids. The hub page shows one row at a time, each piece as a tile by the id cut into it, and saves
each answer here. Answers go on the plate page, not into the print record: a session turns them
into the record with review-print, so the step from a row's answer to each piece's verdict lives
in one place.

The section is `## Judged`, not "answers": the frontmatter's `answers:` already means what the
plate answers. Rows are only ever added; a changed answer is a new row, and the newest row for a
question is the one that counts. The writer never touches `stage` or the Timeline: `printed`
comes with the record.

The table is read with plates_gate's own `after_print`, so the gate (P12) and this script cannot
read a page differently.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))
sys.path.insert(0, str(ROOT / "tools"))

import plates_gate as pg  # noqa: E402

NOT_JUDGED = "not judged yet"
JUDGED_HEAD = "| Row | Answer | His words | Date |"
JUDGED = re.compile(r"^## Judged\b.*?$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
JUDGED_INTRO = ("Omar's answers to the rows of After the print, word for word, one row each, "
                "oldest first. They are written by the review-print skill's `after_print.py "
                "answer` (the hub's Judge a print page calls it); the newest answer to a row is "
                "the one that counts. A session turns them into the print record with review-print.")
WHOLE_KINDS = {"note": "note", "reprint": "reprint asked"}
WHOLE_HEAD = "| Kind | His words | Date |"
WHOLE = re.compile(r"^## On the whole plate\b.*?$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
WHOLE_INTRO = ("What Omar said about the plate as a whole on the hub's Judge a print page, word for "
               "word, oldest first: a general note, or a reprint he asked for. They are written by the "
               "review-print skill's `after_print.py plate`. A reprint asked is a request, not an "
               "approval: the reprint still needs its own yes before it is sent (D-093).")
TICK = re.compile(r"`([^`]+)`")
OWNER = re.compile(r"\b([a-z][a-z0-9]*(?:-[a-z0-9]+)+)'s\s*$")
DO_LOOK = re.compile(r"\*\*Do:\*\*\s*(.*?)\s*\*\*Look for:\*\*\s*(.*)$", re.DOTALL)
FIGURE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
SENTENCE = re.compile(r"(?<=\.)\s+(?=[A-Z0-9`*])")
LABEL_MAX = 80
DECIMAL = re.compile(r"\d\.\d")
IN_WORDS = "in my words"
PIPE = re.compile(r"(?<!\\)\|")
TILE_PX = 360
TILE_MARGIN_MM = 3


class Refused(Exception):
    """The answer cannot be written as asked; the message says why."""


# ---------------------------------------------------------------------------
# reading a row
# ---------------------------------------------------------------------------

def outcomes(cell: str) -> tuple[list[dict], list[str]]:
    """The last cell's "Answer: what it changes." sentences, as [{answer, changes}], and the
    sentences before the first of them, which say what the row decides ("The tightest gap that
    holds becomes the stud gap ..."): a row that names no answers is answered in words."""
    out, intro = [], []
    for s in SENTENCE.split(cell.strip()):
        head, sep, tail = s.partition(": ")
        if sep and len(head) <= LABEL_MAX and "." not in DECIMAL.sub("", head.replace("`", "")):
            out.append({"answer": head.strip("* "), "changes": tail.strip()})
        elif out:
            out[-1]["changes"] += " " + s.strip()
        else:
            intro.append(s.strip())
    return out, intro


def ids_in(text: str, plate: str) -> list[dict]:
    """The backticked ids in a run of the Pieces cell, each with the plate it belongs to: an id
    after `<plate>'s` is that plate's, and so is each id after it joined by a bare comma; any
    other words between two ids bring it back to this plate."""
    found, owner, pos = [], plate, 0
    for m in TICK.finditer(text):
        before = text[pos:m.start()]
        o = OWNER.search(before)
        if o:
            owner = o.group(1)
        elif before.strip(" ,"):
            owner = plate
        found.append({"plate": owner, "id": m.group(1)})
        pos = m.end()
    return found


def split_outside_brackets(cell: str) -> list[str]:
    """The cell cut at each `;` that is not inside round brackets."""
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(cell):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(depth - 1, 0)
        elif ch == ";" and depth == 0:
            parts.append(cell[start:i])
            start = i + 1
    parts.append(cell[start:])
    return parts


def groups(cell: str, plate: str) -> tuple[list[dict], bool]:
    """The Pieces cell as [{these, against}] (`;` parts one beside the other), and whether it
    names every piece on the plate ("All twelve"). A `;` inside brackets is a note on one piece,
    not a second group: dragon-egg-1's "DRAGON EGG (no carved id; the only piece on the bed)"
    showed as two "Pick up these"."""
    out = []
    for part in [p.strip() for p in split_outside_brackets(cell) if p.strip()]:
        these, _, against = part.partition(" beside ")
        out.append({"these": ids_in(these, plate), "these_text": these.strip(),
                     "against": ids_in(against, plate), "against_text": against.strip()})
    every = not any(g["these"] or g["against"] for g in out) and bool(re.match(r"(?i)all\b", cell))
    return out, every


def row_of(i: int, cells: list[str], plate: str) -> tuple[dict, list[str]]:
    """One row as data, and how far it reads: (row, notes). A note is not an error; it says what
    the page falls back to (pieces named in words, the question shown whole, answers in words)."""
    pieces, question, expect, last = (cells + ["", "", "", ""])[:4]
    gs, every = groups(pieces, plate)
    m = DO_LOOK.search(question)
    outs, intro = outcomes(last)
    # Before **Do:** a row may say in plain words what it checks and why, with a picture of what
    # good and bad look like (asking.md; Omar, 2026-11-03: "narrative style writing on what to look
    # for and relevant supplementary figures"). The pictures come out of the text, so a page that
    # shows `question` whole does not print their markup.
    figures = [{"alt": a.strip(), "path": f} for a, f in FIGURE.findall(question)]
    lead = FIGURE.sub("", question[:m.start()] if m else "")
    lead = re.sub(r"\s+", " ", lead).strip()
    question = re.sub(r"[ \t]+", " ", FIGURE.sub("", question)).strip()
    notes = []
    if not every and not any(g["these"] for g in gs):
        notes.append(f"row {i}: pieces named in words, no carved ids ({pieces!r})")
    if not m:
        notes.append(f"row {i}: no **Do:** / **Look for:**, the question is shown whole")
    if not outs:
        notes.append(f"row {i}: names no answers, so it is answered in words")
    return {"row": i, "pieces": pieces, "groups": gs, "every_piece": every,
            "question": question, "lead": lead, "figures": figures,
            "do": m.group(1).strip() if m else None,
            "look_for": m.group(2).strip() if m else None, "expect": expect,
            "decides": " ".join(intro), "outcomes": outs}, notes


def read_page(plate: str, plates: Path) -> tuple[Path, str, dict, str]:
    page = plates / f"{plate}.md"
    if not page.is_file():
        raise Refused(f"no plate page {page}")
    text = page.read_text(encoding="utf-8")
    data, err = pg.parse_frontmatter(text)
    if err or not data:
        raise Refused(f"{page.name}: the frontmatter does not parse: {err}")
    return page, text, data, text[text.find("\n---", 4) + 4:]


def rows_of(plate: str, plates: Path) -> tuple[list[dict], list[str]]:
    _, _, _, body = read_page(plate, plates)
    cells, why = pg.after_print(body)
    if why:
        raise Refused(f"{plate}: {why}")
    rows, problems = [], []
    for i, c in enumerate(cells, 1):
        r, p = row_of(i, c, plate)
        rows.append(r)
        problems += p
    return rows, problems


# ---------------------------------------------------------------------------
# the pieces: label and turn from the recipe and bed map, a tile, a photo
# ---------------------------------------------------------------------------

def recipe_items(plate: str, plates: Path) -> list[dict]:
    try:
        doc = pg.yaml.safe_load((plates / f"{plate}.yaml").read_text(encoding="utf-8"))
    except (OSError, pg.yaml.YAMLError):
        return []
    items = doc.get("items") if isinstance(doc, dict) else None
    return [i for i in items if isinstance(i, dict)] if isinstance(items, list) else []


def bedmap(plate: str, build: Path) -> list[dict]:
    try:
        return json.loads((build / f"{plate}.plate.bedmap.json").read_text())["objects"]
    except (OSError, ValueError, KeyError):
        return []


def matched(items: list[dict], objects: list[dict]) -> list[tuple[dict, dict | None]]:
    """Each recipe item with its bed-map object. The bed map names objects c1…cN in item order,
    one per copy, so an item with `count: 2` stands for two objects (closeout-1's kites); that is
    trusted only when every label agrees, else no item gets an object."""
    copies = [i for i in items for _ in range(max(1, int(i.get("count") or 1)))]
    if len(objects) == len(copies) and all(o.get("label") == i.get("label")
                                           for i, o in zip(copies, objects)):
        return list(zip(copies, objects))
    return [(i, None) for i in copies]


def photos(plate: str, prints: Path) -> dict[str, str]:
    """id -> the newest photo of that piece's bottom in a print record of this plate."""
    out = {}
    for d in sorted(prints.glob(f"*-{plate}")):
        for p in sorted((d / "photos").glob("piece-*-bed-face.*")):
            out[p.name.split("-")[1].upper()] = str(p.relative_to(ROOT))
    return out


def piece_info(plate: str, plates: Path, build: Path, prints: Path) -> dict[str, dict]:
    """id -> {label, turn_deg, tile, photo, grams} for every carved id on the plate; grams is the
    filament that piece took in the slice (`piece_grams`), None when the slice is not on disk."""
    import zipfile

    from piece_grams import piece_grams
    pics = photos(plate, prints)
    three = build / f"{plate}.plate.3mf"
    grams = {}
    if three.is_file():
        with zipfile.ZipFile(three) as zf:
            grams = piece_grams(zf)
    out = {}
    for item, obj in matched(recipe_items(plate, plates), bedmap(plate, build)):
        pid = item.get("id")
        if not pid:
            continue
        tile = plates / f"{plate}-media" / "pieces" / f"{pid}.png"
        out[str(pid)] = {"label": item.get("label"),
                         "turn_deg": obj.get("turn_deg") if obj else None,
                         "tile": str(tile.relative_to(ROOT)) if tile.is_file() else None,
                         "photo": pics.get(str(pid).upper()),
                         "grams": grams.get(str(obj.get("object"))) if obj and grams else None}
    return out


def label_grams(plate: str, plates: Path, build: Path) -> dict[str, float]:
    """recipe label -> grams of every copy of it on the plate, for rows that name pieces by label
    (every plate before carved ids did). Empty when the slice or a matching bed map is missing."""
    import zipfile

    from piece_grams import piece_grams
    three = build / f"{plate}.plate.3mf"
    if not three.is_file():
        return {}
    with zipfile.ZipFile(three) as zf:
        grams = piece_grams(zf)
    out: dict[str, float] = {}
    for obj in bedmap(plate, build):
        if str(obj.get("object")) not in grams:
            return {}
        out[obj.get("label")] = out.get(obj.get("label"), 0.0) + grams[str(obj.get("object"))]
    return out


def row_grams(row: dict, plate: str, by_label: dict[str, float]) -> float | None:
    """What a question's own pieces cost to print: the grams of every piece of this plate it asks
    to pick up (not the earlier prints it compares against, which are already made). A row with
    no carved ids is read by label: each recipe label named as a whole word in its pieces cell,
    every copy counted. None when any piece has no grams, so a part-known sum never reads as the
    whole."""
    these = [p for g in row["groups"] for p in g["these"] if p.get("plate") == plate]
    if these:
        if any(p.get("grams") is None for p in these):
            return None
        return round(sum(p["grams"] for p in these), 2)
    def named(lb: str) -> bool:
        # star-1's halves sit on the bed as SLOPE-NONE-1 and -2 while its row names SLOPE-NONE
        for name in (lb, re.sub(r"-\d+$", "", lb)):
            if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", row["pieces"]):
                return True
        return False
    hits = [lb for lb in by_label if lb and named(lb)]
    return round(sum(by_label[lb] for lb in hits), 2) if hits else None


def tiles(plate: str, plates: Path, build: Path) -> list[Path]:
    """One picture per piece, cut from the bed drawing (`print_review.bed_picture`, the same one the
    plate page's bed.png comes from) round that object's footprint, into `<plate>-media/pieces/`."""
    import print_review as pr
    from PIL import Image

    three = build / f"{plate}.plate.3mf"
    objects = bedmap(plate, build)
    pairs = matched(recipe_items(plate, plates), objects)
    if not three.is_file():
        raise Refused(f"no slice at {three}: slice the plate first (send-plate step 3)")
    if not all(o for _, o in pairs):
        raise Refused(f"the bed map beside {three.name} does not match the recipe's items label for "
                      "label, so no tile could be named by its id")
    import zipfile
    with zipfile.ZipFile(three) as zf:
        shapes = dict(pr.plate_objects(zf))
    img, _, _, _ = pr.bed_picture(str(three), {}, names=False)
    px, h = pr.BED_PX, img.height - pr.CAPTION
    out_dir = plates / f"{plate}-media" / "pieces"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for item, obj in pairs:
        tris = shapes.get(str(obj["object"]))
        if not item.get("id") or not tris:
            continue
        xs = [p[0] for t in tris for p in t]
        ys = [p[1] for t in tris for p in t]
        box = (round((min(xs) - TILE_MARGIN_MM) * px), round(h - (max(ys) + TILE_MARGIN_MM) * px),
               round((max(xs) + TILE_MARGIN_MM) * px), round(h - (min(ys) - TILE_MARGIN_MM) * px))
        tile = img.crop(box)
        tile.thumbnail((TILE_PX, TILE_PX))
        path = out_dir / f"{item['id']}.png"
        tile.convert("P", palette=Image.Palette.ADAPTIVE, colors=64).save(path, optimize=True)
        written.append(path)
    return written


# ---------------------------------------------------------------------------
# answers: the `## Judged` table
# ---------------------------------------------------------------------------

def judged(body: str) -> list[dict]:
    m = JUDGED.search(body)
    if not m:
        return []
    lines = pg.table_lines(m.group(1))
    if not lines or lines[0].strip() != JUDGED_HEAD:
        return []
    out = []
    for ln in lines[2:]:
        c = [uncell(x.strip()) for x in PIPE.split(ln.strip()[1:-1])]
        if len(c) == 4 and c[0].isdigit():
            out.append({"row": int(c[0]), "answer": c[1], "words": "" if c[2] == "—" else c[2],
                        "date": c[3]})
    return out


def latest(answers: list[dict]) -> dict[int, dict]:
    last = {}
    for a in answers:
        last[a["row"]] = a
    return last


def cell(text: str) -> str:
    """A table cell from free words, word for word: one line, each pipe escaped so it cannot
    split the row (Obsidian shows `\\|` as a plain pipe)."""
    return " ".join(text.split()).replace("|", "\\|")


def uncell(text: str) -> str:
    return text.replace("\\|", "|")


def answer(plate: str, row: int, said: str, words: str, date: str, plates: Path) -> str:
    page, text, data, body = read_page(plate, plates)
    rows, _ = rows_of(plate, plates)
    if not 1 <= row <= len(rows):
        raise Refused(f"{plate} has {len(rows)} after-print rows, not a row {row}")
    allowed = [o["answer"] for o in rows[row - 1]["outcomes"]] + [IN_WORDS, NOT_JUDGED]
    pick = next((a for a in allowed if a.casefold() == said.strip().casefold()), None)
    if pick is None:
        raise Refused(f"row {row}'s answers are {allowed}, not {said!r}")
    if pick == IN_WORDS and not words.strip():
        raise Refused(f"'{IN_WORDS}' needs the words: pass them with -n")
    line = f"| {row} | {cell(pick)} | {cell(words) or '—'} | {date} |"
    m = JUDGED.search(body)
    if m and pg.table_lines(m.group(1)):
        lines = m.group(1).split("\n")
        last = max(i for i, ln in enumerate(lines) if ln.strip().startswith("|"))
        lines.insert(last + 1, line)
        new_body = body[:m.start(1)] + "\n".join(lines) + body[m.end(1):]
    else:
        section = f"## Judged\n\n{JUDGED_INTRO}\n\n{JUDGED_HEAD}\n|---|---|---|---|\n{line}\n\n"
        after = pg.AFTER.search(body)
        new_body = body[:after.end()] + section + body[after.end():] if after else \
            body.rstrip("\n") + "\n\n" + section
        if m:  # an empty Judged heading left by hand: replace it
            new_body = new_body.replace(m.group(0), "", 1)
    page.write_text(text[:len(text) - len(body)] + new_body, encoding="utf-8")
    return line


def whole_plate(body: str) -> list[dict]:
    m = WHOLE.search(body)
    if not m:
        return []
    lines = pg.table_lines(m.group(1))
    if not lines or lines[0].strip() != WHOLE_HEAD:
        return []
    kinds = {v: k for k, v in WHOLE_KINDS.items()}
    out = []
    for ln in lines[2:]:
        c = [uncell(x.strip()) for x in PIPE.split(ln.strip()[1:-1])]
        if len(c) == 3 and c[0] in kinds:
            out.append({"kind": kinds[c[0]], "words": c[1], "date": c[2]})
    return out


def plate_line(plate: str, kind: str, words: str, date: str, plates: Path) -> str:
    """One line about the whole plate, not tied to a row (Omar, 2026-11-08: "there should be
    ability to give general feedback in hub"; "a re-printing option on the judge page - if for
    some reason we lost pieces / need to reprint")."""
    page, text, data, body = read_page(plate, plates)
    if kind not in WHOLE_KINDS:
        raise Refused(f"the kinds are {sorted(WHOLE_KINDS)}, not {kind!r}")
    if not words.strip():
        raise Refused(f"a {kind} needs his words: pass them with -n")
    line = f"| {WHOLE_KINDS[kind]} | {cell(words)} | {date} |"
    m = WHOLE.search(body)
    if m and pg.table_lines(m.group(1)):
        lines = m.group(1).split("\n")
        last = max(i for i, ln in enumerate(lines) if ln.strip().startswith("|"))
        lines.insert(last + 1, line)
        new_body = body[:m.start(1)] + "\n".join(lines) + body[m.end(1):]
    else:
        section = f"## On the whole plate\n\n{WHOLE_INTRO}\n\n{WHOLE_HEAD}\n|---|---|---|\n{line}\n\n"
        # after Judged when the page has it, else after After the print, else at the end
        after = JUDGED.search(body) or pg.AFTER.search(body)
        new_body = body[:after.end()] + section + body[after.end():] if after else \
            body.rstrip("\n") + "\n\n" + section
        if m:  # an empty heading left by hand: replace it
            new_body = new_body.replace(m.group(0), "", 1)
    page.write_text(text[:len(text) - len(body)] + new_body, encoding="utf-8")
    return line


# ---------------------------------------------------------------------------
# the queue the page lists
# ---------------------------------------------------------------------------

def finished(plate: str, plates: Path) -> bool:
    log = plates / "print-logs" / f"{plate}.md"
    if not log.is_file():
        return False
    rows, _ = pg.print_log(log.read_text(encoding="utf-8"))
    return any(kind == "finished" for _, kind in rows)


def waiting(plates: Path, prints: Path) -> list[dict]:
    """Plates sent, finished on the printer, with no print record yet: Omar has pieces in hand."""
    recorded = pg.records_by_plate(prints)
    out = []
    for page in sorted(plates.glob("*.md")):
        plate = page.stem
        try:
            _, _, data, body = read_page(plate, plates)
        except Refused:
            continue
        if data.get("stage") != "sent" or plate in recorded or not finished(plate, plates):
            continue
        cells, why = pg.after_print(body)
        if why or not cells:
            continue
        done = latest(judged(body))
        out.append({"plate": plate, "title": pg.title_of(body), "rows": len(cells),
                    "answered": sum(1 for a in done.values() if a["answer"] != NOT_JUDGED)})
    return out


def bed_shown(pictures: list[str]) -> str | None:
    """The bed picture the judging page shows when no piece has one of its own: the slice's first
    layer when the page lists it, since it draws the supports, brim and skirt the pieces came off
    (Omar on star-1, 2026-11-01: "Why don't I see the supports that were actually printed here?"),
    else the bed drawing, which shows the pieces alone."""
    for name in ("first-layer.png", "bed.png"):
        hit = next((p for p in pictures if p.endswith(name)), None)
        if hit:
            return hit
    return None


def questions(plate: str, plates: Path, build: Path, prints: Path) -> dict:
    page, _, data, body = read_page(plate, plates)
    rows, problems = rows_of(plate, plates)
    info = {plate: piece_info(plate, plates, build, prints)}
    by_label = label_grams(plate, plates, build)
    for r in rows:
        for g in r["groups"]:
            for p in g["these"] + g["against"]:
                if p["plate"] not in info:
                    info[p["plate"]] = piece_info(p["plate"], plates, build, prints)
    for r in rows:
        for g in r["groups"]:
            for p in g["these"] + g["against"]:
                p.update(info.get(p["plate"], {}).get(p["id"], {}))
        if r["every_piece"]:
            r["groups"] = [{"these": [{"plate": plate, "id": k, **v} for k, v in info[plate].items()],
                            "these_text": r["pieces"], "against": [], "against_text": ""}]
        r["grams"] = row_grams(r, plate, by_label)
        # A row's pictures are linked from the page; the hub names them from the repo root.
        for f in r["figures"]:
            f["path"] = os.path.relpath(os.path.normpath(plates / f["path"]), ROOT)
    bed =bed_shown(data.get("pictures") or [])
    return {"plate": plate, "title": pg.title_of(body), "stage": data.get("stage"),
            "bed_picture": str((plates / bed).relative_to(ROOT)) if bed else None,
            "rows": rows, "answers": judged(body), "whole_plate": whole_plate(body),
            "notes": problems}


def measure(plates: Path, quiet: bool = False) -> int:
    """Every page's rows through the parser: how many give answer buttons, carved-id tiles and a
    Do / Look for, and each row that falls back. Exits 1 only on a page whose table cannot be read
    at all; a fallback is shown, not refused, since the older pages predate the SOP (2026-10-09)."""
    pages = sorted(p for p in plates.glob("*.md") if pg.AFTER.search(p.read_text(encoding="utf-8")))
    rows = buttons = tiles_ = steps = broken = 0
    for page in pages:
        try:
            got, notes = rows_of(page.stem, plates)
        except Refused as e:
            print(f"{page.stem}: NOT READ: {e}")
            broken += 1
            continue
        rows += len(got)
        buttons += sum(1 for r in got if r["outcomes"])
        tiles_ += sum(1 for r in got if r["every_piece"] or any(g["these"] for g in r["groups"]))
        steps += sum(1 for r in got if r["do"])
        for n in [] if quiet else notes:
            print(f"{page.stem}: {n}")
    print(f"{len(pages)} pages, {rows} rows: {buttons} with answer buttons, {tiles_} with pieces "
          f"by carved id, {steps} with Do / Look for; {broken} page(s) not read")
    return 1 if broken else 0


# ---------------------------------------------------------------------------

def self_test() -> int:
    fails = []

    def check(name, got, want):
        if got != want:
            fails.append(f"{name}: got {got!r}, want {want!r}")

    # outcomes: commas and backticks inside a label, a two-sentence consequence
    o, s = outcomes("Like `2`, `T`: 55% repeats, and it is the base. Not like them: 55% is less "
                    "sure; weigh the rows against `3`, `5` only. It says so.")
    check("outcome labels", [x["answer"] for x in o], ["Like `2`, `T`", "Not like them"])
    check("outcome tail joins", o[1]["changes"].endswith("only. It says so."), True)
    check("no intro", s, [])
    o, _ = outcomes("100% cleaner still and no ridge: 100% is. A ridge: the step before it is the pick.")
    check("label starting with a digit", o[0]["answer"], "100% cleaner still and no ridge")
    o, s = outcomes("We expect fewer. Fewer: keep it. More: drop it.")
    check("a sentence before the first answer is what the row decides", (s, len(o)),
          (["We expect fewer."], 2))
    o, _ = outcomes("None show: the floor stays 0.6 mm. 0.6 shows: the floor goes up.")
    check("a decimal in a label", [x["answer"] for x in o], ["None show", "0.6 shows"])
    o, s = outcomes("The tightest gap that holds becomes the stud gap. If none holds, go looser.")
    check("FAIL: a row with no answers gives no buttons", (o, len(s)), ([], 2))

    # a lead paragraph and a picture before Do: both read, the picture's markup out of the text
    r, n = row_of(1, ["`A` beside `B`", "![a flat face beside a curved one](x-media/face.png) The "
                      "face should be flat. **Do:** 1. Turn it. **Look for:** a curve.", "Flat.",
                      "Flat: keep it. Curved: drop it."], "demo-1")
    check("lead", r["lead"], "The face should be flat.")
    check("figure", r["figures"], [{"alt": "a flat face beside a curved one", "path": "x-media/face.png"}])
    check("question without the picture's markup", "![" in r["question"], False)
    check("do and look for still split", (r["do"], r["look_for"]), ("1. Turn it.", "a curve."))
    check("no fallback note", n, [])
    r, _ = row_of(1, ["`A`", "**Do:** 1. Turn it. **Look for:** a curve.", "Flat.", "Flat: keep it."], "demo-1")
    check("FAIL: a row with no lead gives an empty lead and no pictures", (r["lead"], r["figures"]), ("", []))

    # pieces: another plate's ids, and `;` groups
    g, every = groups("`3`, `5` (stock) beside bedface-4's `H`, `J`", "bedface-5")
    check("these", [(p["plate"], p["id"]) for p in g[0]["these"]], [("bedface-5", "3"), ("bedface-5", "5")])
    check("against, other plate", [(p["plate"], p["id"]) for p in g[0]["against"]],
          [("bedface-4", "H"), ("bedface-4", "J")])
    g, _ = groups("`8`, `9` (55%) beside `3`, `5`, and bedface-4's `2`, `T`", "bedface-5")
    check("mixed against", [(p["plate"], p["id"]) for p in g[0]["against"]],
          [("bedface-5", "3"), ("bedface-5", "5"), ("bedface-4", "2"), ("bedface-4", "T")])
    g, _ = groups("`G`, `K` (55% and flow) beside `8`, `9`; `R`, `S` (75% and flow) beside `A`, `C`",
                  "bedface-5")
    check("two groups", [[p["id"] for p in x["these"]] for x in g], [["G", "K"], ["R", "S"]])
    g, _ = groups("DRAGON EGG (no carved id; the only piece on the bed)", "dragon-egg-1")
    check("a ; in brackets is one group", [x["these_text"] for x in g],
          ["DRAGON EGG (no carved id; the only piece on the bed)"])
    _, every = groups("All twelve", "bedface-5")
    check("every piece", every, True)

    # the writer, on a made-up page: refuses an answer the row does not name, adds rows, leaves
    # the rest of the page byte for byte
    with tempfile.TemporaryDirectory() as t:
        plates = Path(t)
        page = plates / "demo-1.md"
        head = "---\nplate: demo-1\nstage: sent\n---\n\n# demo-1 — a test\n\n"
        after = ("## After the print\n\nAsked.\n\n" + pg.AFTER_HEAD + "\n|---|---|---|---|\n"
                 "| `A` beside `B` | **Do:** Turn them over. **Look for:** Slits? | Fewer. | "
                 "Fewer: keep it. The same: drop it. |\n\n")
        tail = "## Timeline\n\n| Date | What happened | Where it is written |\n|---|---|---|\n"
        page.write_text(head + after + tail, encoding="utf-8")
        try:
            answer("demo-1", 1, "Better", "", "2026-10-22", plates)
            fails.append("FAIL: an answer the row does not name was written")
        except Refused:
            pass
        try:
            answer("demo-1", 2, "Fewer", "", "2026-10-22", plates)
            fails.append("FAIL: a row the page does not have was written")
        except Refused:
            pass
        try:
            answer("demo-1", 1, "in my words", " ", "2026-10-22", plates)
            fails.append("FAIL: 'in my words' with no words was written")
        except Refused:
            pass
        answer("demo-1", 1, "fewer", "A has | a few", "2026-10-22", plates)
        answer("demo-1", 1, "In my words", "B is\nbetter", "2026-10-22", plates)
        answer("demo-1", 1, "not judged yet", "", "2026-10-23", plates)
        text = page.read_text(encoding="utf-8")
        body = text[text.find("\n---", 4) + 4:]
        check("rows kept in order", [(a["answer"], a["words"]) for a in judged(body)],
              [("Fewer", "A has | a few"), (IN_WORDS, "B is better"), (NOT_JUDGED, "")])
        check("newest counts", latest(judged(body))[1]["answer"], NOT_JUDGED)
        check("page around it untouched", text.startswith(head + after) and text.endswith(tail), True)
        check("the gate still reads the questions", len(pg.after_print(body)[0]), 1)
        check("stage untouched", "stage: sent" in text, True)

        # the whole plate: a note and a reprint asked, after Judged, rows untouched
        for kind, words in (("redo", "two lost"), ("note", " ")):
            try:
                plate_line("demo-1", kind, words, "2026-11-08", plates)
                fails.append(f"FAIL: a {kind!r} with {words!r} was written")
            except Refused:
                pass
        plate_line("demo-1", "note", "nice | overall", "2026-11-08", plates)
        plate_line("demo-1", "reprint", "lost `A`\noff the desk", "2026-11-09", plates)
        text = page.read_text(encoding="utf-8")
        body = text[text.find("\n---", 4) + 4:]
        check("whole plate kept in order", whole_plate(body),
              [{"kind": "note", "words": "nice | overall", "date": "2026-11-08"},
               {"kind": "reprint", "words": "lost `A` off the desk", "date": "2026-11-09"}])
        check("whole plate comes after Judged",
              body.find("## Judged") < body.find("## On the whole plate") < body.find("## Timeline"), True)
        check("Judged rows unchanged by it", len(judged(body)), 3)
        check("the gate still reads the questions", len(pg.after_print(body)[0]), 1)
        check("FAIL: a page with no such section has none", whole_plate(head + after + tail), [])

    # the picture shown when no piece has its own: the first layer (supports drawn) wins over the bed
    check("first layer over bed", bed_shown(["x-media/bed.png", "x-media/first-layer.png"]),
          "x-media/first-layer.png")
    check("bed when no first layer", bed_shown(["x-media/on-paper.png", "x-media/bed.png"]), "x-media/bed.png")
    check("FAIL: neither listed gives none", bed_shown(["x-media/on-paper.png"]), None)

    # the bed map is trusted only when its labels match the recipe's items
    items = [{"label": "STOCK A", "id": "3"}, {"label": "55 A", "id": "8"}]
    check("matched", [o for _, o in matched(items, [{"label": "STOCK A"}, {"label": "55 A"}])] != [None, None], True)
    check("FAIL: a reordered bed map names no object",
          [o for _, o in matched(items, [{"label": "55 A"}, {"label": "STOCK A"}])], [None, None])
    two = [{"label": "KITE", "count": 2}, {"label": "STAR"}]
    check("a count: 2 item matches two bed-map objects",
          [o["object"] for _, o in matched(two, [{"label": "KITE", "object": 1}, {"label": "KITE", "object": 2},
                                                  {"label": "STAR", "object": 3}])], [1, 2, 3])
    check("FAIL: a count: 2 item with one object on the bed names none",
          [o for _, o in matched(two, [{"label": "KITE"}, {"label": "STAR"}])], [None, None, None])

    # grams per question: carved ids summed, labels matched whole (halves' -1/-2 included)
    by_label = {"KITE": 0.1, "KITE-G08": 0.2, "STAR-1": 0.3, "STAR-2": 0.3}
    row = lambda text, these=(): {"pieces": text, "groups": [{"these": list(these), "against": [{"plate": "x", "grams": 9}]}]}
    check("carved ids summed, against left out",
          row_grams(row("`A`, `B`", [{"plate": "p", "grams": 0.5}, {"plate": "p", "grams": 0.25}]), "p", {}), 0.75)
    check("FAIL: one carved piece without grams gives none",
          row_grams(row("`A`, `B`", [{"plate": "p", "grams": 0.5}, {"plate": "p", "grams": None}]), "p", {}), None)
    check("a label names its halves", row_grams(row("1 dot (STAR)"), "p", by_label), 0.6)
    check("FAIL: KITE does not pick up KITE-G08", row_grams(row("KITE (no dots)"), "p", by_label), 0.1)
    check("FAIL: a row in words gives none", row_grams(row("The whole coaster"), "p", by_label), None)

    for f in fails:
        print("FAIL", f)
    print(f"after_print self-test: {'PASS' if not fails else 'FAIL'}")
    return 1 if fails else 0


def refresh_evidence_log() -> None:
    """A saved answer moves the evidence log's waiting list; rewrite it so hook 56 passes."""
    import evidence_log  # it imports this module, so not at the top
    said = evidence_log.refresh()
    if said:
        print(said)


def run_questions(args) -> int:
    out = questions(args.plate, pg.PLATES, Path(args.build_dir), pg.PRINTS)
    if args.json:
        print(json.dumps(out, ensure_ascii=False))
        return 0
    for r in out["rows"]:
        print(f"{r['row']}. {r['pieces']}\n   {r['look_for']}")
        for o in r["outcomes"]:
            print(f"   - {o['answer']}: {o['changes']}")
    for n in out["notes"]:
        print("note:", n)
    return 0


def run_answer(args) -> int:
    print(answer(args.plate, args.row, args.answer, args.note, args.date, pg.PLATES))
    refresh_evidence_log()
    return 0


def run_plate(args) -> int:
    print(plate_line(args.plate, args.kind, args.note, args.date, pg.PLATES))
    return 0


def run_waiting(args) -> int:
    out = waiting(pg.PLATES, pg.PRINTS)
    print(json.dumps(out, ensure_ascii=False) if args.json else
          "\n".join(f"{w['plate']}: {w['answered']} of {w['rows']} answered" for w in out))
    return 0


def run_pieces(args) -> int:
    for path in tiles(args.plate, pg.PLATES, Path(args.build_dir)):
        print("wrote", path.relative_to(ROOT))
    return 0


def run_measure(args) -> int:
    return measure(pg.PLATES, args.quiet)


RUNS = {"questions": run_questions, "answer": run_answer, "plate": run_plate,
        "waiting": run_waiting, "pieces": run_pieces, "measure": run_measure}


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    today = datetime.date.today().isoformat()
    q = sub.add_parser("questions")
    q.add_argument("plate")
    q.add_argument("--json", action="store_true")
    q.add_argument("--build-dir", default=str(ROOT / "build" / "plates"))
    a = sub.add_parser("answer")
    a.add_argument("plate")
    a.add_argument("row", type=int)
    a.add_argument("answer")
    a.add_argument("-n", "--note", default="")
    a.add_argument("--date", default=today)
    wp = sub.add_parser("plate")
    wp.add_argument("plate")
    wp.add_argument("kind", choices=sorted(WHOLE_KINDS))
    wp.add_argument("-n", "--note", default="")
    wp.add_argument("--date", default=today)
    w = sub.add_parser("waiting")
    w.add_argument("--json", action="store_true")
    p = sub.add_parser("pieces")
    p.add_argument("plate")
    p.add_argument("--build-dir", default=str(ROOT / "build" / "plates"))
    m = sub.add_parser("measure")
    m.add_argument("--quiet", action="store_true", help="the tally only, not each fallback")
    return ap


def main(argv: list[str]) -> int:
    ap = parser()
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    run = RUNS.get(args.cmd)
    if not run:
        ap.print_help()
        return 2
    try:
        return run(args)
    except Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
