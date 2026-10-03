#!/usr/bin/env python3
"""Plates gate for 3d-models: a plate page tells the truth about its plate.

`docs/design/plates/<plate>.yaml` is what gets sliced; `docs/design/plates/<plate>.md` is the page Omar
reviews it on: what it is, why print it, pictures, cost and risk, their approval tick box, a
table of every approval they gave it, and a timeline of what happened to it. Its frontmatter
holds the few facts the queue ranks on and how many times it printed; whether Omar approved it
is the Approvals table, which can hold the second yes on the same design (D-096).
The design is `docs/design/printing/print-review-design.md`; these are its §6 rules.

  P1  **Shape.** The frontmatter parses and carries every key in REQUIRED; `plate` is the
      file name; `recipe` is the `.yaml` beside it; `stage`, `kind` and `risk` are in their
      vocabularies; every `bets` id is a real bet in `bets.md`; a plate the queue ranks
      carries its cost (`minutes`, `grams`, `bed_plates`) as positive numbers. A `planned`
      plate is designed but cannot be built yet: it may have no recipe and no cost, and it
      names what it waits on in `needs:`. Only a planned plate has `needs:` — a plate that
      still waits on a build is not ready to rank, so it cannot sit at a later stage.

  P2  **Approvals** (D-096). Omar's decisions are rows in the page's `## Approvals` table,
      `| Date | Decision | By | Covers | Spent by |`, one row per decision, as many as the plate
      gets: `approved`, `held`, or `standing` (a production plate's standing approval). Not
      frontmatter: one `approved:` field cannot hold the second yes on the same design. The tick
      box (or a yes in chat) is the input; `tools/plate_approve.py` writes the row and unticks
      the box. Covers is `recipe <hash>`, the recipe the decision was made on. An approval's
      Spent by is empty while it is open, `sent <date>` once a send used it, or `replaced <date>`
      when a later decision took its place; held and standing rows say `—`. Checked: the table
      and its header are there; rows are dated, in order, with words from the vocabularies; a
      `sent` date has a timeline `sent` row, and every timeline `sent` row from TABLE_FROM on
      was spent by exactly one approval or went out on a standing one; a `replaced` date has a
      later decision that day; at most one approval is open and nothing is decided after it;
      stage `approved` holds exactly while an approval is open. The load-bearing case: a send
      with no approval spent on it — nothing goes out that the page says Omar did not approve.

  P3  **Count.** `runs` is exactly the print records under `docs/prints/` whose `plate:`
      starts with this plate's name, and `times_printed` is how many there are. Hard case:
      a page that types `times_printed: 0` and `runs: []` correctly for each other still
      fails when a record exists — the count is checked against the records, not against
      itself.

  P4  **Pictures.** Every listed picture exists. A page waiting on Omar, or approved, shows
      at least one: nobody approves a plate they have not seen.

  P5  **Coverage.** Every plate `.yaml` has a page and every page has a `.yaml`.

  P6  **Timeline.** The `## Timeline` table's rows are dated, in order, and name an event in
      EVENTS. Every run has a `printed` row naming it, and there are as many `printed` rows as
      `times_printed`. Approvals are not timeline events; they are P2's table.

  P7  **The queue is current.** The block between the queue markers in
      `docs/design/plates/README.md` is exactly what `--write` would write from the pages and the
      weights in the `prioritize-prints` skill's scoring.md. Priority is presented, never
      stored (prints-tab-design §6): no page holds a rank, the queue is recomputed.

  P8  **Maturity is earned.** `maturity` is `experiment`, `repeatable` or `production`
      (`docs/design/printing/plate-maturity-design.md`), and no higher than the print records
      show. Repeatable: every piece in the recipe — same model file, piece, params, on any
      plate — has its latest K verdicts all `keep`. Production: repeatable, `bed_fill` at least
      the rubric's, `kind: repeat`, and this plate's own latest run kept every piece and printed
      what the recipe holds now. K and the fill are read from the grade-plate skill's
      rubric.md. A level above experiment has a `promoted` row, and the last promoted or
      demoted row names the level the page says. Hard case: three pieces kept twice each and
      one never kept is not repeatable — every piece, not a total.
      A production plate's recipe does not change in place (D-095): its page pins
      `recipe_hash` when it is promoted, and a recipe that no longer matches it is a finding.
      A change goes on a new experiment plate whose `derived_from` names it
      (`tools/plate_grade.py --derive`). A `derived_from` must name a plate page that exists.
      A production page's last `standing` row covers its pinned `recipe_hash`.
      `standing_approval` says whether a production plate may go out with no new yes; the
      send check (`tools/bambu/src/send-gate.ts`) reads it through `plate_approve.py --status`.

Not a finding: a ticked Approve or Hold box that the table does not record yet, or an open
approval whose recipe has changed since. Each prints a notice, because the fix is a read-back
by whoever runs the skill, and a whole-tree gate that failed on it would block every other
session's commit until then. The send refuses an unrecorded tick; a changed recipe it names and
lets through while LAPSE_ON_RECIPE_CHANGE is off (Omar's call 6, print-review-design §9). Nor is a page that
claims less maturity than its prints show: experiment asks nothing, and promoting is a choice.

  rank:        python3 .claude/gates/plates_gate.py --rank
  as data:     python3 .claude/gates/plates_gate.py --rank --json   (3d-model-hub's plate queue)
  rewrite:     python3 .claude/gates/plates_gate.py --write
  wholesale:   make validate-prints (hook 39 runs it after the prints gate)
  override:    PRINTS_GATE_OK=1 git commit
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prints_gate import CAL_ID, parse_frontmatter, record_dirs  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PLATES = ROOT / "docs" / "design" / "plates"
PRINTS = ROOT / "docs" / "prints"
SCORING = ROOT / ".claude" / "skills" / "prioritize-prints" / "scoring.md"
RUBRIC = ROOT / ".claude" / "skills" / "grade-plate" / "rubric.md"
BETS = ROOT / ".claude" / "skills" / "calibrate" / "bets.md"
# The queue links the weights from the page it is written on, so the link follows the folder.
SCORING_LINK = Path(os.path.relpath(SCORING, PLATES)).as_posix()

REQUIRED = (
    "plate", "recipe", "stage", "times_printed", "runs",
    "answers", "kind", "maturity", "bets", "unblocks", "minutes", "grams", "bed_plates", "risk",
    "pictures",
)
# planned: designed, waiting on a build before it can have a recipe or a slice.
# proposed: page written, not yet looked over. waiting: looked over, waiting on Omar's tick.
# approved: Omar ticked it. sent: it went to the printer. printed: a record exists.
# retired: not printing it again.
STAGES = ("planned", "proposed", "waiting", "approved", "sent", "printed", "retired")
RANKED = frozenset({"proposed", "waiting", "approved"})
SHOWN = frozenset({"waiting", "approved"})
KINDS = ("new", "taste", "repeat")
RISKS = ("ok", "watch", "hold")
# What past prints showed, lowest first (plate-maturity-design §2). Not `kind`: kind is why the
# next print happens, maturity is what the last ones proved.
MATURITY = ("experiment", "repeatable", "production")
EVENTS = ("proposed", "reviewed", "sliced", "sent", "printed", "judged", "promoted", "demoted",
          "retired")
# The approvals table (P2, D-096). Rows before TABLE_FROM were moved in from the timeline when
# the table began: they may cover `—` (the recipe they approved was not hashed), and a send
# before it needs no row (minis-01 to -03 went out before plate pages existed).
APPROVALS_HEAD = "| Date | Decision | By | Covers | Spent by |"
DECISIONS = ("approved", "held", "standing")
TABLE_FROM = "2026-10-03"
# Does a yes lapse when the recipe changes after it? Omar's open call 6 in print-review-design
# §9; until he answers, a change is named on the send and in a notice, and the yes stands, as
# before the table. "Gate it" is this one switch: the table already records what each yes covers.
LAPSE_ON_RECIPE_CHANGE = False
COVERS = re.compile(r"^recipe [0-9a-f]{12}$")
SPENT = re.compile(r"^(sent|replaced) (\d{4}-\d{2}-\d{2})$")

Q_START, Q_END = "<!-- queue:start -->", "<!-- queue:end -->"
ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([a-z]+)\b(.*)$")
TICKED_APPROVE = re.compile(r"^\s*-\s*\[[xX]\]\s*\*{0,2}Approve", re.MULTILINE)
TICKED_HOLD = re.compile(r"^\s*-\s*\[[xX]\]\s*\*{0,2}Hold", re.MULTILINE)


def plate_of(record_plate) -> str | None:
    """A record's free-text `plate:` ("minis-03 — openwork minis at 40 mm") -> "minis-03"."""
    if not isinstance(record_plate, str) or not record_plate.strip():
        return None
    return record_plate.split()[0]


def records_by_plate(prints: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for rec in record_dirs(prints):
        data, _ = parse_frontmatter((rec / "index.md").read_text(encoding="utf-8"))
        name = plate_of((data or {}).get("plate"))
        if name:
            out.setdefault(name, []).append(rec.name)
    return {k: sorted(v) for k, v in out.items()}


def read_pages(plates: Path) -> list[tuple[Path, dict | None, str, str | None]]:
    """(path, frontmatter, body, error) for every page in `plates`, README excluded."""
    out = []
    for p in sorted(plates.glob("*.md")):
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8")
        data, err = parse_frontmatter(text)
        end = text.find("\n---", 4)
        body = text[end + 4:] if end != -1 else ""
        out.append((p, data, body, err))
    return out


def read_weights(scoring: Path) -> dict:
    """The `weights:` yaml block in scoring.md — the rubric sharpens without code changing."""
    text = scoring.read_text(encoding="utf-8")
    for block in re.findall(r"```yaml\n(.*?)```", text, flags=re.DOTALL):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and isinstance(data.get("weights"), dict):
            return data["weights"]
    raise ValueError(f"{scoring}: no ```yaml block with a `weights:` mapping")


def _pos(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x > 0


def timeline(body: str) -> list[tuple[str, str, str]]:
    """(date, event, rest of row) for each dated row under `## Timeline`."""
    m = re.search(r"^## Timeline\b.*?$(.*?)(?=^## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        r = ROW.match(line.strip())
        if r:
            rows.append((r.group(1), r.group(2), r.group(3)))
    return rows


# ---------------------------------------------------------------------------
# P2 — the approvals table (D-096)
# ---------------------------------------------------------------------------

APPROVALS = re.compile(r"^## Approvals\b.*?$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)


def approvals(body: str) -> tuple[list[dict], str | None]:
    """(rows, why the table does not read) for `## Approvals`. Each row is
    {date, decision, by, covers, spent}, in the order the table holds them."""
    m = APPROVALS.search(body)
    if not m:
        return [], "no '## Approvals' table"
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip().startswith("|")]
    if not lines or lines[0] != APPROVALS_HEAD:
        return [], f"the Approvals table's header is not `{APPROVALS_HEAD}`"
    rows = []
    for ln in lines[2:]:  # the header, then its |---| line
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) != 5:
            return [], f"an Approvals row does not have five cells: {ln}"
        rows.append(dict(zip(("date", "decision", "by", "covers", "spent"), cells)))
    return rows, None


def open_approval(rows: list[dict]) -> dict | None:
    """The approval not yet spent or replaced, if there is one (P2 allows at most one)."""
    live = [r for r in rows if r["decision"] == "approved" and not r["spent"]]
    return live[-1] if live else None


def covers(path: Path) -> str | None:
    """What an approval made now covers: `recipe <hash>`, or None with no readable recipe."""
    h = recipe_hash(path)
    return f"recipe {h}" if h else None


def approval_status(path: Path, data: dict, body: str) -> dict:
    """{approved, how, row, sends}: may this plate go out on a yes, one per send (D-093)?
    Only an open approval on the recipe as it is now. A ticked box is not one until it is a row:
    a box ticked before a send made outside the CLI looks exactly like a fresh one."""
    sends = sum(1 for _, ev, _ in timeline(body) if ev == "sent")
    rows, bad = approvals(body)
    if bad:
        return {"approved": False, "how": bad, "row": None, "sends": sends}
    row = open_approval(rows)
    record = (f"record it with `python3 tools/plate_approve.py {path.stem} --approved "
              "--by \"Omar, tick\"`")
    if row is None:
        last = [r for r in rows if r["decision"] in ("approved", "held")]
        if not last:
            how = "no approval in the Approvals table"
        elif last[-1]["decision"] == "held":
            how = f"held on {last[-1]['date']} ({last[-1]['by']})"
        else:
            how = f"the approval of {last[-1]['date']} was {last[-1]['spent']}"
        if TICKED_APPROVE.search(body):
            how += f"; the Approve box is ticked but not recorded — {record}"
        return {"approved": False, "how": how, "row": None, "sends": sends}
    now = covers(path)
    changed = row["covers"] != now
    if changed and LAPSE_ON_RECIPE_CHANGE:
        return {"approved": False, "row": row, "sends": sends,
                "how": (f"the approval of {row['date']} covers {row['covers']}, but the recipe is "
                        f"now {now}: the recipe changed after the yes, so it needs a new one")}
    nth = "its first send" if sends == 0 else f"send {sends + 1}"
    how = f"approved on {row['date']} ({row['by']}), for {nth}"
    if changed:
        how += (f"; but the recipe changed since (the yes covers {row['covers']}, the recipe is "
                f"now {now}) — whether that voids the yes is Omar's open call 6 in "
                "print-review-design §9, so tell him and ask before sending")
    return {"approved": True, "row": row, "sends": sends, "how": how}


def check_approvals(name: str, data: dict, body: str) -> list[str]:
    """P2: the table reads, its rows agree with each other and with the timeline's sends."""
    out = [f"{name}: P2 `{k}` is in the frontmatter — approvals moved to the page's "
           "## Approvals table (D-096)" for k in ("approved", "approved_on") if k in data]
    rows, bad = approvals(body)
    if bad:
        return out + [f"{name}: P2 {bad} — `python3 tools/plate_approve.py {name} --table` "
                      "writes an empty one"]
    for i, r in enumerate(rows):
        d, dec, spent = r["date"], r["decision"], r["spent"]
        where = f"{name}: P2 Approvals row {i + 1} ({d})"
        try:
            dt.date.fromisoformat(d)
        except ValueError:
            out.append(f"{where}: the date is not YYYY-MM-DD")
            continue
        if dec not in DECISIONS:
            out.append(f"{where}: decision {dec!r} is not one of {list(DECISIONS)}")
            continue
        if not r["by"]:
            out.append(f"{where}: By is empty — say who decided, and how")
        if dec in ("approved", "standing") and not COVERS.match(r["covers"]) and not (
                d < TABLE_FROM and r["covers"] == "—"):
            out.append(f"{where}: an {dec} row covers {r['covers']!r}, not `recipe <hash>`")
        if dec == "approved":
            m = SPENT.match(spent)
            if spent and not m:
                out.append(f"{where}: Spent by {spent!r} is not empty, `sent <date>` or "
                           "`replaced <date>`")
            elif m and m.group(2) < d:
                out.append(f"{where}: spent on {m.group(2)}, before it was given")
            elif m and m.group(1) == "replaced" and not any(
                    x["date"] == m.group(2) and x["decision"] in DECISIONS for x in rows[i + 1:]):
                out.append(f"{where}: replaced on {m.group(2)}, but no later decision that day")
        elif spent != "—":
            out.append(f"{where}: a {dec} row is not spent, so Spent by is `—`, not {spent!r}")
    if [r["date"] for r in rows] != sorted(r["date"] for r in rows):
        out.append(f"{name}: P2 Approvals rows are not in date order")
    live = [i for i, r in enumerate(rows) if r["decision"] == "approved" and not r["spent"]]
    if len(live) > 1:
        out.append(f"{name}: P2 {len(live)} approvals are open; a new decision replaces the "
                   "last one")
    elif live and any(r["decision"] in ("approved", "held") for r in rows[live[0] + 1:]):
        out.append(f"{name}: P2 the approval of {rows[live[0]]['date']} is open but a later "
                   "decision came after it — mark it `replaced <date>`")
    stage = data.get("stage")
    if (stage == "approved") != bool(live):
        out.append(f"{name}: P2 stage '{stage}' but "
                   + ("an approval is open — record the stage as approved"
                      if live else "no approval is open in the Approvals table"))
    # Sends: each spent approval names a send, and each send since the table began spent one.
    sent = [(d, rest) for d, ev, rest in timeline(body) if ev == "sent"]
    standing_from = min((r["date"] for r in rows if r["decision"] == "standing"), default=None)
    spent_on: dict[str, int] = {}
    for r in rows:
        m = SPENT.match(r["spent"]) if r["decision"] == "approved" else None
        if m and m.group(1) == "sent":
            spent_on[m.group(2)] = spent_on.get(m.group(2), 0) + 1
    for d, n in sorted(spent_on.items()):
        on_day = [rest for sd, rest in sent if sd == d and "standing approval" not in rest]
        if len(on_day) < n:
            out.append(f"{name}: P2 {n} approval(s) spent by a send on {d}, but the timeline has "
                       f"{len(on_day)} 'sent' row(s) that day")
    for d in sorted({sd for sd, _ in sent if sd >= TABLE_FROM}):
        rests = [rest for sd, rest in sent if sd == d]
        standing = [x for x in rests if "standing approval" in x]
        if standing and not (standing_from and standing_from <= d):
            out.append(f"{name}: P2 a send on {d} says it went out on a standing approval, but "
                       "no standing row comes before it")
        if len(rests) - len(standing) > spent_on.get(d, 0):
            out.append(f"{name}: P2 it went out on {d} with no approval spent on it — nothing "
                       "goes out unapproved (record the yes, then `plate_approve.py --sent`)")
    return out


# ---------------------------------------------------------------------------
# P8 — maturity: what the page claims against what the prints showed
# ---------------------------------------------------------------------------

def read_rubric(rubric: Path) -> dict:
    """The `maturity:` yaml block in the grade-plate skill's rubric.md, read like the weights."""
    text = rubric.read_text(encoding="utf-8")
    for block in re.findall(r"```yaml\n(.*?)```", text, flags=re.DOTALL):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and isinstance(data.get("maturity"), dict):
            m = data["maturity"]
            if not (isinstance(m.get("keeps_for_repeatable"), int) and m["keeps_for_repeatable"] > 0
                    and _pos(m.get("production_fill")) and m["production_fill"] <= 1):
                raise ValueError(f"{rubric}: maturity needs keeps_for_repeatable (a positive "
                                 "whole number) and production_fill (in (0, 1])")
            return m
    raise ValueError(f"{rubric}: no ```yaml block with a `maturity:` mapping")


def _norm(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return v
    return round(float(v), 6)


def piece_key(source, piece, params, window=None) -> str:
    """One piece, the same on any plate: model file, piece, params, and the window a sampler
    cell is cut to. A recipe's `{ gap: 0.1 }` and a record's `{"gap": 0.1}` give the same key;
    a number is a number, 2 and 2.0 alike."""
    params = params or {}
    p = {str(k): _norm(v) for k, v in params.items()} if isinstance(params, dict) else params
    return json.dumps([source, piece or "", p] + ([str(window)] if window else []), sort_keys=True)


def _obj_key(o: dict) -> str:
    """A record object's key; `bambu slice sheet` writes a vendored cell as `3d-models:<stl>`."""
    return piece_key(o.get("source"), o.get("piece"), o.get("params"), o.get("window"))


def _label(key: str) -> str:
    source, piece, params, *window = json.loads(key)
    name = str(source).rsplit("/", 1)[-1].removesuffix(".bkr")
    knobs = ", ".join(f"{k} {v:g}" if isinstance(v, float) else f"{k} {v}"
                      for k, v in (params or {}).items())
    return (name + (f" {piece}" if piece else "") + (f" ({knobs})" if knobs else "")
            + (f" window {window[0]}" if window else ""))


def _records(prints: Path) -> list[tuple[str, dict]]:
    out = []
    for rec in record_dirs(prints):
        data, _ = parse_frontmatter((rec / "index.md").read_text(encoding="utf-8"))
        out.append((rec.name, data or {}))
    return out  # record_dirs sorts by name, and a run's name starts with its date


def piece_history(prints: Path) -> dict[str, list[tuple[str, str]]]:
    """piece key -> [(run, verdict)], oldest first, across every record on every plate."""
    out: dict[str, list[tuple[str, str]]] = {}
    for run_id, data in _records(prints):
        for o in data.get("objects") or []:
            if isinstance(o, dict) and o.get("verdict"):
                out.setdefault(_obj_key(o), []).append((run_id, o["verdict"]))
    return out


def plate_runs(prints: Path) -> dict[str, list[dict]]:
    """plate -> its runs, oldest first: what each printed, whether every piece was kept, and
    how many of its bet readings landed (any verdict but no-reading)."""
    out: dict[str, list[dict]] = {}
    for run_id, data in _records(prints):
        name = plate_of(data.get("plate"))
        if not name:
            continue
        objs = [o for o in data.get("objects") or [] if isinstance(o, dict)]
        counts: dict[str, int] = {}
        verdicts: dict[str, int] = {}
        for o in objs:
            key = _obj_key(o)
            counts[key] = counts.get(key, 0) + (o.get("count") or 1)
            verdicts[o.get("verdict")] = verdicts.get(o.get("verdict"), 0) + 1
        readings = [r for r in data.get("readings") or [] if isinstance(r, dict)]
        out.setdefault(name, []).append({
            "run": run_id, "counts": counts, "verdicts": verdicts,
            "clean": bool(objs) and all(o.get("verdict") == "keep" for o in objs),
            "readings": len(readings),
            "landed": sum(1 for r in readings if r.get("verdict") not in (None, "no-reading")),
        })
    return out


def recipe_pieces(path: Path, data: dict) -> dict[str, int] | str:
    """piece key -> how many the recipe prints, or why there is nothing to read."""
    if data.get("recipe") is None:
        return "no recipe yet"
    try:
        recipe = yaml.safe_load((path.parent / f"{path.stem}.yaml").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as e:
        return f"the recipe does not read ({e})"
    recipe = recipe if isinstance(recipe, dict) else {}
    # A plate lists `items`; a sampler sheet a `card` with `cells` on it, printed as one object
    # but recorded, and judged, part by part (`bambu slice sheet`).
    items = recipe.get("items") or ([recipe["card"]] + list(recipe.get("cells") or [])
                                    if isinstance(recipe.get("card"), dict) else [])
    if not items:
        return "the recipe has no items"
    out: dict[str, int] = {}
    for it in items:
        if isinstance(it, dict):
            src = it.get("bkr") or (f"3d-models:{it['stl']}" if it.get("stl") else None)
            key = piece_key(src, it.get("piece"), it.get("params"), it.get("window"))
            out[key] = out.get(key, 0) + (it.get("count") or 1)
    return out


def maturity_evidence(path: Path, data: dict, history: dict, runs: dict, rubric: dict) -> dict:
    """The highest level the prints support: {level, why: [lines], pieces: [per-piece facts]}.

    repeatable  every piece in the recipe has its latest K verdicts all `keep`, on any plate.
                The latest K, not any K: a keep, keep, adjust piece was judged wrong last.
    production  repeatable, the page's `bed_fill` is at least the rubric's, and this plate's
                own latest run kept every piece and printed what the recipe prints now. Pieces
                kept on other plates do not show that this layout prints clean.
    """
    k, need = rubric["keeps_for_repeatable"], rubric["production_fill"]
    pieces = recipe_pieces(path, data)
    if isinstance(pieces, str):
        return {"level": "experiment", "why": [pieces], "pieces": []}
    facts, short = [], []
    for key in pieces:
        seen = [v for _, v in history.get(key, [])]
        ok = len(seen) >= k and all(v == "keep" for v in seen[-k:])
        facts.append({"piece": _label(key), "verdicts": seen, "repeatable": ok})
        if not ok:
            short.append(f"{_label(key)}: {', '.join(seen) or 'never printed'}")
    if short:
        return {"level": "experiment", "pieces": facts,
                "why": [f"not every piece has its last {k} verdicts keep:"] + short}
    why = [f"every piece's last {k} verdicts are keep"]
    own = runs.get(path.stem, [])
    fill = data.get("bed_fill")
    gaps = []
    if not (_pos(fill) and fill >= need):
        gaps.append(f"bed_fill {fill!r} is under {need}")
    if not own:
        gaps.append("this plate has never printed")
    elif not own[-1]["clean"]:
        gaps.append(f"its latest run {own[-1]['run']} did not keep every piece")
    elif own[-1]["counts"] != pieces:
        gaps.append(f"its latest run {own[-1]['run']} printed a different set than the recipe "
                    "holds now")
    if gaps:
        return {"level": "repeatable", "pieces": facts, "why": why + ["not production: " + "; ".join(gaps)]}
    return {"level": "production", "pieces": facts,
            "why": why + [f"bed_fill {fill} and its latest run {own[-1]['run']} kept every piece"]}


def recipe_hash(path: Path) -> str | None:
    """The recipe's content, not its text: comments and key order do not change it."""
    try:
        recipe = yaml.safe_load((path.parent / f"{path.stem}.yaml").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    canon = json.dumps(recipe, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:12]


def recipe_unchanged(path: Path, data: dict) -> str | None:
    """Why a production page's recipe is not the one it was promoted on, or None when it is."""
    pinned, now = data.get("recipe_hash"), recipe_hash(path)
    if not pinned:
        return ("no recipe_hash pinned — promotion writes it "
                f"(`python3 tools/plate_grade.py --recipe-hash {path.stem}`)")
    if pinned != now:
        return (f"its recipe changed since it was promoted (recipe_hash {pinned}, now {now}). A "
                "production recipe does not change in place: put the change on a new experiment "
                f"plate (`python3 tools/plate_grade.py --derive {path.stem} <new>`) and put "
                f"{path.stem}.yaml back")
    return None


def standing_row(path: Path, data: dict, body: str) -> str | None:
    """Why a production page's Approvals table does not hold its standing approval, or None.
    The last `standing` row covers the recipe the page was promoted on (D-095, D-096)."""
    rows, bad = approvals(body)
    if bad:
        return bad
    last = [r for r in rows if r["decision"] == "standing"]
    want = f"recipe {data.get('recipe_hash')}"
    if not last:
        return ("no standing row in the Approvals table — promotion writes it "
                f"(`python3 tools/plate_approve.py {path.stem} --standing`)")
    if last[-1]["covers"] != want:
        return (f"the last standing row ({last[-1]['date']}) covers {last[-1]['covers']}, not the "
                f"promoted {want}")
    return None


def standing_approval(path: Path, data: dict, ev: dict, body: str) -> tuple[bool, str]:
    """(may it go out with no new yes, why). Only a production page whose prints still show
    production, whose recipe is the one it was promoted on (D-095), and whose Approvals table
    holds the standing row for that recipe (D-096)."""
    if data.get("maturity") != "production":
        return False, f"maturity is {data.get('maturity')!r}, not production"
    if ev["level"] != "production":
        return False, (f"the page says production but the prints now show {ev['level']} — "
                       + " ".join(ev["why"]) + "; demote it (grade-plate skill)")
    changed = recipe_unchanged(path, data) or standing_row(path, data, body)
    if changed:
        return False, changed
    return True, "a production plate whose prints still show production, on its promoted recipe"


def check_maturity(path: Path, data: dict, body: str, history: dict, runs: dict,
                   rubric: dict) -> tuple[list[str], list[str]]:
    """(findings, notices). Claiming more than the prints show is a finding; claiming less is a
    notice, since an experiment needs nothing and a promotion is Omar's to want."""
    name, out, notes = path.stem, [], []
    level = data.get("maturity")
    if level not in MATURITY:
        return [f"{name}: P8 maturity {level!r} is not one of {list(MATURITY)}"], []
    fill = data.get("bed_fill")
    if fill is not None and not (_pos(fill) and fill <= 1):
        out.append(f"{name}: P8 bed_fill {fill!r} is not a share of the bed in (0, 1]")
    ev = maturity_evidence(path, data, history, runs, rubric)
    if MATURITY.index(level) > MATURITY.index(ev["level"]):
        out.append(f"{name}: P8 maturity '{level}' but the prints show {ev['level']} — "
                   + " ".join(ev["why"]))
    elif MATURITY.index(level) < MATURITY.index(ev["level"]):
        notes.append(f"{name}: the prints would carry {ev['level']}, the page says {level} — "
                     "grade it (grade-plate skill)")
    if level == "production" and data.get("kind") != "repeat":
        out.append(f"{name}: P8 a production plate prints again what is known, so its kind is "
                   f"'repeat', not {data.get('kind')!r}")
    if level == "production":
        changed = recipe_unchanged(path, data)
        if changed:
            out.append(f"{name}: P8 production plate: {changed}")
        missing = standing_row(path, data, body)
        if missing:
            out.append(f"{name}: P8 production plate: {missing}")
    moves = [(d, ev_, rest) for d, ev_, rest in timeline(body) if ev_ in ("promoted", "demoted")]
    if moves and level not in moves[-1][2]:
        out.append(f"{name}: P8 maturity '{level}' but the last promoted/demoted row "
                   f"({moves[-1][0]}) does not name it")
    if not moves and level != "experiment":
        out.append(f"{name}: P8 maturity '{level}' with no 'promoted' row saying when and why")
    return out, notes


def check_page(path: Path, data: dict, body: str, records: dict[str, list[str]],
               bet_ids: set[str]) -> list[str]:
    name = path.stem
    out: list[str] = []
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        return [f"{name}: P1 frontmatter is missing {missing}"]

    # P1 — shape
    if data["plate"] != name:
        out.append(f"{name}: P1 plate '{data['plate']}' is not the file name")
    stage = data["stage"]
    no_recipe_yet = stage == "planned" and data["recipe"] is None
    if not no_recipe_yet and (data["recipe"] != f"{name}.yaml"
                              or not (path.parent / f"{name}.yaml").is_file()):
        out.append(f"{name}: P1 recipe '{data['recipe']}' is not the {name}.yaml beside the page")
    for key, vocab in (("stage", STAGES), ("kind", KINDS), ("risk", RISKS)):
        if data[key] not in vocab:
            out.append(f"{name}: P1 {key} '{data[key]}' is not one of {list(vocab)}")
    bets = data["bets"] if isinstance(data["bets"], list) else None
    if bets is None:
        out.append(f"{name}: P1 bets is not a list")
    else:
        for b in bets:
            if not (isinstance(b, str) and CAL_ID.match(b) and b in bet_ids):
                out.append(f"{name}: P1 bet '{b}' is not a bet in bets.md")
    if not isinstance(data["unblocks"], list) or not all(
            isinstance(u, str) and u.strip() for u in data["unblocks"]):
        out.append(f"{name}: P1 unblocks is not a list of non-empty strings")
    if not isinstance(data["answers"], str) or not data["answers"].strip():
        out.append(f"{name}: P1 answers is empty — say the question the plate answers")
    parent = data.get("derived_from")
    if parent is not None and (not isinstance(parent, str) or parent == name
                               or not (path.parent / f"{parent}.md").is_file()):
        out.append(f"{name}: P1 derived_from {parent!r} is not another plate page in docs/design/plates/")
    needs = data.get("needs")
    if stage == "planned":
        if not isinstance(needs, list) or not needs or not all(
                isinstance(n, str) and n.strip() for n in needs):
            out.append(f"{name}: P1 stage 'planned' but needs is not a list of what it waits on")
    elif needs:
        out.append(f"{name}: P1 needs lists unbuilt work but stage is '{stage}' — a plate that "
                   "waits on a build is 'planned'")
    if stage in RANKED:
        for key in ("minutes", "grams", "bed_plates"):
            if not _pos(data[key]):
                out.append(f"{name}: P1 stage '{stage}' is ranked, so {key} must be a positive "
                           f"number, not {data[key]!r}")

    # P2 — approvals: the table, not the frontmatter
    out += check_approvals(name, data, body)

    # P3 — the count is the records, not what the page says about itself
    runs = data["runs"] if isinstance(data["runs"], list) else None
    actual = records.get(name, [])
    times = data["times_printed"]
    if runs is None:
        out.append(f"{name}: P3 runs is not a list")
    elif sorted(runs) != actual:
        out.append(f"{name}: P3 runs {sorted(runs)} are not the records for this plate {actual}")
    if not isinstance(times, int) or isinstance(times, bool) or times != len(actual):
        out.append(f"{name}: P3 times_printed {times!r} but docs/prints/ holds {len(actual)} "
                   "record(s) for this plate")
    if stage == "printed" and not actual:
        out.append(f"{name}: P3 stage 'printed' but no record for this plate")

    # P4 — pictures
    pics = data["pictures"] if isinstance(data["pictures"], list) else None
    if pics is None:
        out.append(f"{name}: P4 pictures is not a list")
    else:
        for pic in pics:
            if not isinstance(pic, str) or not (path.parent / pic).is_file():
                out.append(f"{name}: P4 picture '{pic}' does not exist beside the page")
        if stage in SHOWN and not pics:
            out.append(f"{name}: P4 stage '{stage}' asks Omar to look, but there is no picture")

    # P6 — timeline
    rows = timeline(body)
    if not rows:
        out.append(f"{name}: P6 no dated rows under '## Timeline'")
    for d, ev, _ in rows:
        if ev not in EVENTS:
            out.append(f"{name}: P6 timeline event '{ev}' on {d} is not one of {list(EVENTS)}")
    dates = [d for d, _, _ in rows]
    if dates != sorted(dates):
        out.append(f"{name}: P6 timeline rows are not in date order")
    printed_rows = [rest for _, ev, rest in rows if ev == "printed"]
    for run_id in actual:
        if not any(run_id in rest for rest in printed_rows):
            out.append(f"{name}: P6 run {run_id} has no 'printed' row naming it")
    if isinstance(times, int) and len(printed_rows) != times:
        out.append(f"{name}: P6 {len(printed_rows)} 'printed' row(s) but times_printed {times}")
    return out


# ---------------------------------------------------------------------------
# the queue: computed, never stored on a page
# ---------------------------------------------------------------------------

def value_of(data: dict, w: dict) -> float:
    """The value half of the score; a planned plate has it before it has a cost."""
    return (w["per_bet"] * len(data["bets"]) + w["per_unblock"] * len(data["unblocks"])
            + w["kind"][data["kind"]])


def score(data: dict, w: dict) -> tuple[float, float, float]:
    """(value, cost in hours, roi). scoring.md says what each weight means and why."""
    value = value_of(data, w)
    cost = data["minutes"] / 60 + data["grams"] / w["grams_per_hour"]
    return value, cost, value / cost


def planned(pages: list[dict], w: dict) -> list[dict]:
    """Plates waiting on a build, highest value first. Not ranked against the queue: with no
    slice there is no cost, and value alone would put an untimed plate above a timed one."""
    return sorted((p for p in pages if p["stage"] == "planned"),
                  key=lambda p: (-value_of(p, w), p["plate"]))


def rank(pages: list[dict], w: dict) -> list[tuple[dict, float, float, float]]:
    """Ranked plates, best ROI first; a plate waits below any unprinted plate it is `after`."""
    live = [p for p in pages if p["stage"] in RANKED and p["risk"] != "hold"]
    scored = sorted(((p, *score(p, w)) for p in live), key=lambda t: (-t[3], t[0]["plate"]))
    names = {p["plate"] for p in live}
    placed: list = []
    pending = list(scored)
    while pending:
        for i, t in enumerate(pending):
            needs = [a for a in (t[0].get("after") or []) if a in names]
            if all(any(q[0]["plate"] == a for q in placed) for a in needs):
                break
        else:
            i = 0  # a cycle: fall back to ROI order rather than hang
        placed.append(pending.pop(i))
    return placed


def _links(ps: list[dict], tail) -> str:
    return ", ".join(f"[{p['plate']}]({p['plate']}.md){tail(p)}" for p in ps) or "none"


def render_queue(pages: list[dict], w: dict) -> str:
    lines = [
        Q_START,
        "Written by `python3 .claude/gates/plates_gate.py --write` from the plate pages and the "
        f"weights in [scoring.md]({SCORING_LINK}). Do not edit "
        "by hand; the prints hook fails when this block and the pages disagree.",
        "",
        "| # | Plate | Stage | Value | Hours | ROI | Risk | What it answers |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, (p, value, cost, roi) in enumerate(rank(pages, w), 1):
        lines.append(f"| {i} | [{p['plate']}]({p['plate']}.md) | {p['stage']} | {value:g} | "
                     f"{cost:.1f} | {roi:.2f} | {p['risk']} | {p['answers']} |")
    held = [p for p in pages if p["stage"] in RANKED and p["risk"] == "hold"]
    sent = [p for p in pages if p["stage"] == "sent"]
    done = [p for p in pages if p["stage"] in ("printed", "retired")]
    times = lambda p: f" ×{p['times_printed']}"  # noqa: E731
    worth = lambda p: f" (value {value_of(p, w):g})"  # noqa: E731
    lines += [
        "",
        "**Waiting on a build** (no recipe or slice yet, so no hours; highest value first): "
        f"{_links(planned(pages, w), worth)}.",
        "",
        f"**Held for hardware risk:** {_links(held, lambda p: '')}.",
        "",
        f"**Went to the printer, no record yet:** {_links(sent, lambda p: '')}.",
        "",
        f"**Printed:** {_links(done, times)}.",
        Q_END,
    ]
    return "\n".join(lines)


def title_of(body: str) -> str | None:
    """The page's own `# minis-06 — the two dovetails` heading, or None."""
    m = re.search(r"^# (.+)$", body, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


def queue_json(pages: list[dict], w: dict, titles: dict[str, str | None], plates: Path = PLATES,
               approved_on: dict[str, str | None] | None = None) -> dict:
    """The queue as data, for 3d-model-hub's plate queue: the same ranking `render_queue` writes,
    with the page facts beside it so the hub never parses a plate page itself. `page` is the page's
    path in this repo; the hub resolves `pictures` beside it, so moving the folder moves nothing there.
    `approved` and `approved_on` are the open approval in the page's table (D-096), if any."""
    approved_on = approved_on or {}

    def facts(p: dict) -> dict:
        on = approved_on.get(p["plate"])
        return {
            "plate": p["plate"], "page": Path(os.path.relpath(plates / f"{p['plate']}.md", ROOT)).as_posix(),
            "title": titles.get(p["plate"]), "stage": p["stage"],
            "approved": on is not None, "approved_on": on,
            "times_printed": p["times_printed"], "runs": p["runs"], "answers": p["answers"],
            "kind": p["kind"], "bets": p["bets"], "unblocks": p["unblocks"],
            "minutes": p["minutes"], "grams": p["grams"], "bed_plates": p["bed_plates"],
            "risk": p["risk"], "pictures": p["pictures"], "needs": p.get("needs") or [],
        }
    queue = [{"rank": i, "value": value, "hours": round(cost, 2), "roi": round(roi, 2), **facts(p)}
             for i, (p, value, cost, roi) in enumerate(rank(pages, w), 1)]
    return {
        "queue": queue,
        "planned": [{"value": value_of(p, w), **facts(p)} for p in planned(pages, w)],
        "held": [facts(p) for p in pages if p["stage"] in RANKED and p["risk"] == "hold"],
        "sent": [facts(p) for p in pages if p["stage"] == "sent"],
        "printed": [facts(p) for p in pages if p["stage"] in ("printed", "retired")],
    }


def queue_block(readme: Path) -> str | None:
    text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    a, b = text.find(Q_START), text.find(Q_END)
    return text[a:b + len(Q_END)] if a != -1 and b != -1 else None


def write_queue(readme: Path, block: str) -> None:
    text = readme.read_text(encoding="utf-8")
    a, b = text.find(Q_START), text.find(Q_END)
    readme.write_text(text[:a] + block + text[b + len(Q_END):], encoding="utf-8")


# ---------------------------------------------------------------------------

def approval_notices(path: Path, data: dict, body: str) -> list[str]:
    """A tick the table does not hold yet, or an open approval on a recipe since changed. A
    notice, not a finding: the read-back is the next session's, and the send refuses either."""
    name, out = path.stem, []
    rows, _ = approvals(body)
    row = open_approval(rows)
    if TICKED_APPROVE.search(body):
        out.append(f"{name}: an Approve box is ticked but not in the Approvals table — record it: "
                   f"`python3 tools/plate_approve.py {name} --approved --by \"Omar, tick\"`")
    if TICKED_HOLD.search(body):
        out.append(f"{name}: the Hold box is ticked but not in the Approvals table — record it: "
                   f"`python3 tools/plate_approve.py {name} --held --by \"Omar, tick\"`")
    if row and row["covers"] != covers(path):
        out.append(f"{name}: the open approval of {row['date']} covers {row['covers']}, but the "
                   f"recipe is now {covers(path)} — "
                   + ("the send will refuse it until Omar approves again" if LAPSE_ON_RECIPE_CHANGE
                      else "ask Omar before it goes out (print-review call 6 is open)"))
    return out


def page_findings(path: Path, data: dict, body: str, ctx: dict) -> tuple[list[str], list[str]]:
    """(findings, notices) for one page: P1-P4 and P6, then P8 once the shape holds."""
    f = check_page(path, data, body, ctx["records"], ctx["bet_ids"])
    if f:
        return f, []
    return check_maturity(path, data, body, ctx["history"], ctx["runs"], ctx["rubric"])


def context(prints: Path, bets: Path, rubric: Path) -> dict:
    return {"records": records_by_plate(prints),
            "bet_ids": set(re.findall(r"CAL-[A-Z]+-\d+", bets.read_text(encoding="utf-8"))),
            "history": piece_history(prints), "runs": plate_runs(prints),
            "rubric": read_rubric(rubric)}


def check_tree(plates: Path, prints: Path, scoring: Path, bets: Path, rubric: Path = RUBRIC
               ) -> tuple[list[str], list[str], int, str | None]:
    """(findings, notices, pages checked, rendered queue or None)."""
    findings: list[str] = []
    notices: list[str] = []
    try:
        ctx = context(prints, bets, rubric)
    except (OSError, ValueError) as e:
        return [f"rubric: P8 {e}"], [], 0, None
    pages = read_pages(plates)
    good: list[dict] = []
    for path, data, body, err in pages:
        if err:
            findings.append(f"{path.stem}: P1 {err}")
            continue
        f, n = page_findings(path, data, body, ctx)
        findings += f
        notices += n
        if not f:
            good.append(data)
            notices += approval_notices(path, data, body)
    # P5 — coverage, both ways
    stems = {p.stem for p, *_ in pages}
    for y in sorted(plates.glob("*.yaml")):
        if y.stem not in stems:
            findings.append(f"{y.stem}: P5 plate recipe has no page ({y.stem}.md)")
    rendered = None
    if not findings:
        try:
            rendered = render_queue(good, read_weights(scoring))
        except (ValueError, KeyError, TypeError) as e:
            findings.append(f"README: P7 cannot rank — {e}")
    if rendered is not None and queue_block(plates / "README.md") != rendered:
        findings.append("README: P7 the queue block is not what the pages and weights give — "
                        "run `python3 .claude/gates/plates_gate.py --write`")
    return findings, notices, len(pages), rendered


def run(plates=PLATES, prints=PRINTS, scoring=SCORING, bets=BETS, rubric=RUBRIC) -> int:
    findings, notices, n, _ = check_tree(plates, prints, scoring, bets, rubric)
    for x in notices:
        print(f"notice: {x}")
    if findings:
        for f in findings:
            print(f, file=sys.stderr)
        print(f"\nplates-gate: {len(findings)} finding(s) across {n} page(s). See "
              "docs/design/printing/print-review-design.md §6. Override once with "
              "PRINTS_GATE_OK=1 git commit", file=sys.stderr)
        return 1
    print(f"plates: {n} page(s) checked, queue current")
    print("OK")
    return 0


def sort_pages(plates: Path, prints: Path, bets: Path, rubric: Path = RUBRIC
               ) -> tuple[list[dict], list[str], dict[str, str | None], dict[str, str | None]]:
    """(pages with no finding, the findings of the rest, each page's title, the date of each
    page's open approval)."""
    ctx = context(prints, bets, rubric)
    good, bad, titles, opened = [], [], {}, {}
    for path, data, body, err in read_pages(plates):
        f = [f"{path.stem}: {err}"] if err else page_findings(path, data, body, ctx)[0]
        bad += f
        if not f:
            good.append(data)
            titles[data["plate"]] = title_of(body)
            row = open_approval(approvals(body)[0])
            opened[data["plate"]] = row["date"] if row else None
    return good, bad, titles, opened


def rank_json(plates=PLATES, prints=PRINTS, scoring=SCORING, bets=BETS, rubric=RUBRIC) -> int:
    """--rank --json: the queue as JSON on stdout. Refuses, like --write, while a page is wrong."""
    good, bad, titles, opened = sort_pages(plates, prints, bets, rubric)
    if bad:
        print("\n".join(bad), file=sys.stderr)
        print("plates-gate: fix the pages before ranking them", file=sys.stderr)
        return 1
    print(json.dumps(queue_json(good, read_weights(scoring), titles, plates, opened), indent=2))
    return 0


def rewrite(plates=PLATES, prints=PRINTS, scoring=SCORING, bets=BETS, quiet=False,
            rubric=RUBRIC) -> int:
    """--write: rewrite the queue block. Refuses while any page has a finding other than P7."""
    good, bad, _, _ = sort_pages(plates, prints, bets, rubric)
    if bad:
        print("\n".join(bad), file=sys.stderr)
        print("plates-gate: fix the pages before writing the queue", file=sys.stderr)
        return 1
    readme = plates / "README.md"
    if queue_block(readme) is None:
        print(f"plates-gate: {readme} has no {Q_START} … {Q_END} block", file=sys.stderr)
        return 1
    write_queue(readme, render_queue(good, read_weights(scoring)))
    if not quiet:
        print(f"queue written: {readme}")
    return 0


# ---------------------------------------------------------------------------
# self-test: a clean fixture comes back clean, then one mutation per rule fires
# ---------------------------------------------------------------------------

_WEIGHTS_MD = """# scoring

```yaml
weights:
  per_bet: 2
  per_unblock: 2
  kind: {new: 2, taste: 1, repeat: 0}
  grams_per_hour: 100
```
"""

_RUBRIC_MD = """# rubric

```yaml
maturity:
  keeps_for_repeatable: 2
  production_fill: 0.5
```
"""

# minis-09 prints two pieces: one A, two B. The maturity cases judge them on records.
_A = ("bikar:a.bkr", "Hex", {"gap": 0.1})
_B = ("bikar:b.bkr", None, {})
_RECIPE_09 = """bed: x2d
items:
  - bkr: bikar:a.bkr
    piece: Hex
    params: { gap: 0.1 }
  - bkr: bikar:b.bkr
    count: 2
"""


_SEP = "|---|---|---|---|---|"


def _page(plate: str, fm: dict, timeline_rows: list[str], tick: str = " ") -> str:
    return ("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n"
            f"# {plate}\n\n## Your call\n\n- [{tick}] **Approve** — print it as it is\n"
            "- [ ] **Hold** — say why\n\n"
            f"## Approvals\n\n{APPROVALS_HEAD}\n{_SEP}\n\n"
            "## Timeline\n\n| Date | What happened | Where |\n|---|---|---|\n"
            + "\n".join(timeline_rows) + "\n")


def _approve(page: str, *rows: str):
    """Add Approvals rows to a fixture page; `{hash}` is the page's recipe hash now."""
    def f(plates: Path) -> None:
        h = recipe_hash(plates / f"{page}.md")
        _edit(page, f"{_SEP}\n", f"{_SEP}\n" + "".join(r.replace("{hash}", str(h)) + "\n"
                                                     for r in rows))(plates)
    return f


def _timeline_add(page: str, after: str, row: str):
    return _edit(page, after, f"{after}\n{row}")


def _build(tmp: Path) -> tuple[Path, Path, Path, Path]:
    plates, prints = tmp / "docs" / "plates", tmp / "docs" / "prints"
    (plates / "minis-08-media").mkdir(parents=True)
    (plates / "minis-08-media" / "sheet.png").write_bytes(b"png")
    rec = prints / "2026-09-26-minis-09"
    rec.mkdir(parents=True)
    (rec / "index.md").write_text('---\nrun: 2026-09-26-minis-09\nplate: "minis-09 — a test"\n---\n',
                                  encoding="utf-8")
    base = {"times_printed": 0, "runs": [],
            "answers": "does it hold", "kind": "new", "maturity": "experiment",
            "bets": ["CAL-CST-06"],
            "unblocks": ["a decision"], "minutes": 120, "grams": 30, "bed_plates": 1,
            "risk": "watch", "pictures": ["minis-08-media/sheet.png"]}
    for n, extra, rows in (
        ("minis-08", {"stage": "waiting"},
         ["| 2026-09-30 | proposed | page written |", "| 2026-09-30 | reviewed | sheet |"]),
        ("minis-09", {"stage": "printed", "times_printed": 1,
                      "runs": ["2026-09-26-minis-09"], "minutes": None, "grams": None,
                      "bed_plates": None, "pictures": []},
         ["| 2026-09-25 | proposed | yaml |",
          "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |"]),
    ):
        (plates / f"{n}.yaml").write_text(_RECIPE_09 if n == "minis-09" else "bed: x2d\n",
                                          encoding="utf-8")
        fm = {"plate": n, "recipe": f"{n}.yaml", "stage": extra["stage"], **base, **extra}
        (plates / f"{n}.md").write_text(_page(n, fm, rows), encoding="utf-8")
    # A designed plate that waits on a build: no recipe, no slice, no picture yet.
    fm = {"plate": "sheets-09", "recipe": None, "stage": "planned", **base, "minutes": None,
          "grams": None, "bed_plates": None, "pictures": [], "needs": ["the window cut"]}
    (plates / "sheets-09.md").write_text(
        _page("sheets-09", fm, ["| 2026-10-01 | proposed | the design |"]), encoding="utf-8")
    scoring = tmp / "scoring.md"
    scoring.write_text(_WEIGHTS_MD, encoding="utf-8")
    bets = tmp / "bets.md"
    bets.write_text("CAL-CST-06 dovetail neck\n", encoding="utf-8")
    (plates / "README.md").write_text(f"# Plates\n\n{Q_START}\n{Q_END}\n", encoding="utf-8")
    (tmp / "rubric.md").write_text(_RUBRIC_MD, encoding="utf-8")
    rewrite(plates, prints, scoring, bets, quiet=True, rubric=_rubric(plates))
    return plates, prints, scoring, bets


def _rubric(plates: Path) -> Path:
    return plates.parents[1] / "rubric.md"


def _record(plates: Path, run: str, objects: list[tuple[tuple, int, str]]) -> None:
    """A record under the fixture's prints/: each object is (piece, count, verdict)."""
    rec = plates.parent / "prints" / run
    rec.mkdir(parents=True, exist_ok=True)
    objs = [{"entry": f"c{i}", "source": src, **({"piece": piece} if piece else {}),
             "params": params, "count": count, "verdict": verdict}
            for i, ((src, piece, params), count, verdict) in enumerate(objects, 1)]
    plate = run.split("-", 3)[3]
    (rec / "index.md").write_text("---\n" + yaml.safe_dump(
        {"run": run, "plate": plate, "objects": objs}, sort_keys=False) + "---\n", encoding="utf-8")


def _mature(level: str, history: list[tuple[str, str, str]], own: list | None = None,
            kind: str = "repeat", fill: float | None = 0.6, row: str | None = None,
            pin: bool = True, standing: bool = True):
    """minis-09 claims `level`; `history` is (run on another plate, A's verdict, B's verdict);
    `own` replaces minis-09's own record's objects. A production claim pins its recipe's hash
    unless `pin` is false, and records its standing approval unless `standing` is false."""
    def f(plates: Path) -> None:
        for run, va, vb in history:
            _record(plates, run, [(_A, 1, va), (_B, 2, vb)])
        if own is not None:
            _record(plates, "2026-09-26-minis-09", own)
        pinned = (f"\nrecipe_hash: '{recipe_hash(plates / 'minis-09.md')}'"
                  if level == "production" and pin else "")
        _edit("minis-09", "kind: new\nmaturity: experiment",
              f"kind: {kind}\nmaturity: {level}" + (f"\nbed_fill: {fill}" if fill else "")
              + pinned)(plates)
        if level != "experiment" or row:
            _edit("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
                  "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |\n"
                  + (row or f"| 2026-09-28 | promoted | to {level}: the grade |"))(plates)
        if level == "production" and pin and standing:
            _approve("minis-09", "| 2026-09-28 | standing | plate_grade.py, promoted | "
                     "recipe {hash} | — |")(plates)
    return f


_KEPT = [("2026-09-20-minis-07", "keep", "keep"), ("2026-09-21-minis-07", "keep", "keep")]
_CLEAN_OWN = [(_A, 1, "keep"), (_B, 2, "keep")]


def _then(*steps):
    def f(plates: Path) -> None:
        for s in steps:
            s(plates)
    return f


def _edit_recipe(old: str, new: str):
    def f(plates: Path) -> None:
        p = plates / "minis-09.yaml"
        text = p.read_text(encoding="utf-8")
        assert old in text, old
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
    return f


def _edit(page: str, old: str, new: str):
    def f(plates: Path) -> None:
        p = plates / f"{page}.md"
        text = p.read_text(encoding="utf-8")
        assert old in text, (page, old)
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
    return f


def _record_adjust(plates: Path) -> None:
    """minis-09 printed again, and B came back adjust."""
    _record(plates, "2026-09-30-minis-09", [(_A, 1, "keep"), (_B, 2, "adjust")])


def _second_record(plates: Path) -> None:
    rec = plates.parent / "prints" / "2026-09-29-minis-08"
    rec.mkdir(parents=True)
    (rec / "index.md").write_text('---\nrun: 2026-09-29-minis-08\nplate: "minis-08"\n---\n',
                                  encoding="utf-8")


def _orphan_yaml(plates: Path) -> None:
    (plates / "minis-07.yaml").write_text("bed: x2d\n", encoding="utf-8")


def _lose_picture(plates: Path) -> None:
    (plates / "minis-08-media" / "sheet.png").unlink()


def _stale_queue(plates: Path) -> None:
    _edit("minis-08", "minutes: 120", "minutes: 90")(plates)


CASES = [
    ("P1 plate is not the file name", _edit("minis-08", "plate: minis-08", "plate: minis-8"),
     "P1 plate 'minis-8' is not the file name"),
    ("P1 a stage outside the vocabulary", _edit("minis-08", "stage: waiting", "stage: ready"),
     "P1 stage 'ready'"),
    ("P1 a bet that is not in bets.md", _edit("minis-08", "CAL-CST-06", "CAL-CST-99"),
     "P1 bet 'CAL-CST-99'"),
    ("P1 a ranked plate with no cost", _edit("minis-08", "grams: 30", "grams: null"),
     "so grams must be a positive number"),
    ("P2 approval facts left in the frontmatter",
     _edit("minis-08", "stage: waiting", "stage: waiting\napproved: true"),
     "P2 `approved` is in the frontmatter — approvals moved"),
    ("P2 a page with no Approvals table",
     _edit("minis-08", f"## Approvals\n\n{APPROVALS_HEAD}\n{_SEP}\n\n", ""),
     "P2 no '## Approvals' table"),
    ("P2 stage approved with no open approval",
     _edit("minis-08", "stage: waiting", "stage: approved"),
     "P2 stage 'approved' but no approval is open"),
    ("P2 an open approval on a page still waiting",
     _approve("minis-08", "| 2026-10-04 | approved | Omar, tick | recipe {hash} | |"),
     "P2 stage 'waiting' but an approval is open"),
    ("P2 sent with no approval spent on it (the load-bearing case)",
     _then(_edit("minis-08", "stage: waiting", "stage: sent"),
           _timeline_add("minis-08", "| 2026-09-30 | reviewed | sheet |",
                         "| 2026-10-04 | sent | by bambu print send |")),
     "P2 it went out on 2026-10-04 with no approval spent on it"),
    ("P2 a send before the table began needs no row",
     _timeline_add("minis-09", "| 2026-09-25 | proposed | yaml |",
                   "| 2026-09-25 | sent | before plate pages |"), None),
    ("P2 many decisions on one design: approved, replaced, held, approved again, sent",
     _then(_approve("minis-09",
                    "| 2026-10-03 | approved | Omar, tick | recipe {hash} | replaced 2026-10-04 |",
                    "| 2026-10-04 | held | Omar, in chat | recipe {hash} | — |",
                    "| 2026-10-05 | approved | Omar, in chat | recipe {hash} | sent 2026-10-05 |"),
           _timeline_add("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
                         "| 2026-10-05 | sent | by bambu print send |")), None),
    ("P2 two approvals open at once",
     _then(_edit("minis-08", "stage: waiting", "stage: approved"),
           _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | recipe {hash} | |",
                    "| 2026-10-04 | approved | Omar, tick | recipe {hash} | |")),
     "P2 2 approvals are open"),
    ("P2 an open approval with a hold after it",
     _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | recipe {hash} | |",
              "| 2026-10-04 | held | Omar | recipe {hash} | — |"),
     "is open but a later decision came after it"),
    ("P2 an approval spent by a send the timeline does not have",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | recipe {hash} | sent 2026-10-05 |"),
     "P2 1 approval(s) spent by a send on 2026-10-05, but the timeline has 0"),
    ("P2 replaced with nothing decided that day",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | recipe {hash} | replaced 2026-10-04 |"),
     "replaced on 2026-10-04, but no later decision that day"),
    ("P2 a decision outside the vocabulary",
     _approve("minis-09", "| 2026-10-03 | maybe | Omar | recipe {hash} | — |"),
     "decision 'maybe' is not one of"),
    ("P2 an approval since the table began that covers no recipe",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | — | replaced 2026-10-03 |",
              "| 2026-10-03 | held | Omar | — | — |"),
     "an approved row covers '—', not `recipe <hash>`"),
    ("P2 an approval moved in from before the table may cover no recipe",
     _then(_approve("minis-09", "| 2026-10-02 | approved | Omar | — | sent 2026-10-02 |"),
           _timeline_add("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
                         "| 2026-10-02 | sent | from Bambu Studio |")), None),
    ("P2 a row with a cell missing",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | recipe {hash} |"),
     "does not have five cells"),
    ("P3 a record the page does not count, count self-consistent (the hard case)",
     _second_record, "P3 runs [] are not the records for this plate ['2026-09-29-minis-08']"),
    ("P3 printed with a count that disagrees",
     _edit("minis-09", "times_printed: 1", "times_printed: 2"), "P3 times_printed 2"),
    ("P4 a listed picture is gone", _lose_picture, "P4 picture 'minis-08-media/sheet.png'"),
    ("P4 waiting on Omar with no picture",
     _edit("minis-08", "pictures:\n- minis-08-media/sheet.png", "pictures: []"),
     "asks Omar to look, but there is no picture"),
    ("P5 a recipe with no page", _orphan_yaml, "P5 plate recipe has no page"),
    ("P1 planned with nothing named to wait on",
     _edit("sheets-09", "needs:\n- the window cut", "needs: []"),
     "P1 stage 'planned' but needs is not a list"),
    ("P1 a needs list on a plate past planned (it would rank before it can be built)",
     _edit("minis-08", "pictures:\n- minis-08-media/sheet.png",
           "pictures:\n- minis-08-media/sheet.png\nneeds:\n- a bikar change"),
     "P1 needs lists unbuilt work but stage is 'waiting'"),
    ("P2 planned and approved before it exists",
     _approve("sheets-09", "| 2026-10-01 | approved | Omar | — | |"),
     "P2 stage 'planned' but an approval is open"),
    ("P1 a recipe named that is not there",
     _edit("sheets-09", "recipe: null", "recipe: sheets-09.yaml"),
     "P1 recipe 'sheets-09.yaml' is not the sheets-09.yaml"),
    ("P6 an approval written as a timeline event (it belongs in the table)",
     _timeline_add("minis-08", "| 2026-09-30 | reviewed | sheet |",
                   "| 2026-09-30 | approved | by Omar |"),
     "P6 timeline event 'approved' on 2026-09-30 is not one of"),
    ("P6 a run with no printed row",
     _edit("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
           "| 2026-09-26 | judged | verdicts |"), "P6 run 2026-09-26-minis-09 has no 'printed' row"),
    ("P6 rows out of date order",
     _edit("minis-08", "| 2026-09-30 | reviewed", "| 2026-09-01 | reviewed"),
     "P6 timeline rows are not in date order"),
    ("P7 a page edited, queue not rewritten", _stale_queue, "P7 the queue block is not"),
    ("P8 a word outside the maturity levels",
     _edit("minis-09", "maturity: experiment", "maturity: prototype"), "P8 maturity 'prototype'"),
    ("P8 repeatable when every piece's last two verdicts are keep", _mature("repeatable", _KEPT),
     None),
    ("P8 repeatable on a high keep count while one piece was never kept (an aggregate is not "
     "every part)",
     _mature("repeatable", [("2026-09-19-minis-07", "keep", "adjust"),
                            ("2026-09-20-minis-07", "keep", "adjust"),
                            ("2026-09-21-minis-07", "keep", "drop")]),
     "b: adjust, adjust, drop"),
    ("P8 repeatable with two keeps but judged wrong last (the latest two, not any two)",
     _mature("repeatable", _KEPT + [("2026-09-22-minis-07", "adjust", "keep")]),
     "P8 maturity 'repeatable' but the prints show experiment"),
    ("P8 repeatable with no promoted row", _mature("repeatable", _KEPT,
     row="| 2026-09-28 | judged | nothing |"), "no 'promoted' row"),
    ("P8 the last maturity row names another level",
     _mature("repeatable", _KEPT, row="| 2026-09-28 | promoted | to repeatable |\n"
             "| 2026-09-29 | demoted | to experiment: a new piece |"),
     "the last promoted/demoted row (2026-09-29) does not name it"),
    ("P8 production: kept pieces, full bed, its own latest run kept everything",
     _mature("production", _KEPT[:1], own=_CLEAN_OWN), None),
    ("P8 production on pieces kept elsewhere while this plate never printed clean",
     _mature("production", _KEPT), "its latest run 2026-09-26-minis-09 did not keep every piece"),
    ("P8 production whose own run printed a different set than the recipe now holds",
     _mature("production", _KEPT[:1], own=[(_A, 1, "keep"), (_B, 1, "keep")]),
     "printed a different set than the recipe holds now"),
    ("P8 production with the bed under the rubric's fill",
     _mature("production", _KEPT[:1], own=_CLEAN_OWN, fill=0.3), "bed_fill 0.3 is under 0.5"),
    ("P8 production with no bed_fill at all",
     _mature("production", _KEPT[:1], own=_CLEAN_OWN, fill=None), "bed_fill None is under 0.5"),
    ("P8 production that is not kind repeat",
     _mature("production", _KEPT[:1], own=_CLEAN_OWN, kind="taste"),
     "its kind is 'repeat', not 'taste'"),
    ("P8 a bed_fill that is not a share of the bed",
     _mature("experiment", [], fill=1.4, row="| 2026-09-28 | judged | x |"),
     "P8 bed_fill 1.4 is not a share"),
    ("P8 a planned page with no recipe claims repeatable",
     _edit("sheets-09", "maturity: experiment", "maturity: repeatable"),
     "P8 maturity 'repeatable' but the prints show experiment — no recipe yet"),
    ("P8 production with no standing row in the Approvals table",
     _mature("production", _KEPT[:1], own=_CLEAN_OWN, standing=False),
     "P8 production plate: no standing row in the Approvals table"),
    ("P8 production whose standing row covers another recipe",
     _then(_mature("production", _KEPT[:1], own=_CLEAN_OWN, standing=False),
           _approve("minis-09", "| 2026-09-28 | standing | promoted | recipe 000000000000 | — |")),
     "covers recipe 000000000000, not the promoted"),
    ("P8 production with no recipe_hash pinned",
     _mature("production", _KEPT[:1], own=_CLEAN_OWN, pin=False), "no recipe_hash pinned"),
    ("P8 production whose recipe was edited in place, same pieces (a repack the counts miss)",
     _then(_mature("production", _KEPT[:1], own=_CLEAN_OWN), _edit_recipe("bed: x2d", "bed: x2d\nspacing: 4")),
     "its recipe changed since it was promoted"),
    ("P8 production whose recipe only gained a comment is the same recipe",
     _then(_mature("production", _KEPT[:1], own=_CLEAN_OWN), _edit_recipe("bed: x2d", "# packed\nbed: x2d")),
     None),
    ("P1 derived_from a plate that has no page",
     _edit("minis-08", "maturity: experiment", "maturity: experiment\nderived_from: minis-07"),
     "P1 derived_from 'minis-07' is not another plate page"),
    ("P1 derived_from a plate that has a page",
     _edit("minis-08", "maturity: experiment", "maturity: experiment\nderived_from: minis-09"),
     None),
]


def self_test() -> int:
    import shutil
    import tempfile

    failures = 0
    tmp = Path(tempfile.mkdtemp(prefix="plates-gate-"))

    def report(ok: bool, label: str, why: str) -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))

    try:
        for label, mutate, want in [("the fixture itself is clean", None, None)] + CASES:
            case = tmp / re.sub(r"[^a-z0-9]+", "-", label.lower())
            plates, prints, scoring, bets = _build(case)
            if mutate:
                mutate(plates)
            found, _, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
            if want is None:
                report(not found, label, f"clean fixture reported {found}")
            else:
                report(any(want in f for f in found), label, f"wanted {want!r}, got {found or 'nothing'}")

        # A ticked box not read back is a notice, never a finding.
        case = tmp / "tick-is-a-notice"
        plates, prints, scoring, bets = _build(case)
        _edit("minis-08", "- [ ] **Approve**", "- [x] **Approve**")(plates)
        found, notices, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
        report(not found and len(notices) == 1, "a ticked box not read back is a notice only",
               f"findings={found} notices={notices}")

        # An open approval: the plate stands approved on the recipe it covers. When the recipe
        # changes after the yes it is a notice and a warning on the send; only with the call-6
        # switch on does the status refuse it.
        def opened(*steps):
            case = tmp / f"open-{len(steps)}"
            plates, prints, scoring, bets = _build(case)
            _then(_edit("minis-08", "stage: waiting", "stage: approved"),
                  _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | recipe {hash} | |"),
                  *steps)(plates)
            rewrite(plates, prints, scoring, bets, quiet=True, rubric=_rubric(plates))
            found, notices, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
            page = plates / "minis-08.md"
            text = page.read_text(encoding="utf-8")
            data, _ = parse_frontmatter(text)
            return found, notices, approval_status(page, data, text) | {"page": page}

        found, notices, st = opened()
        report(not found and not notices and st["approved"] and "for its first send" in st["how"],
               "an open approval on the recipe as it is lets the plate go out",
               f"{found} {notices} {st}")
        found, notices, st = opened(lambda pl: (pl / "minis-08.yaml").write_text(
            "bed: x2d\nspacing: 4\n", encoding="utf-8"))
        report(not found and any("call 6 is open" in n for n in notices)
               and st["approved"] and "open call 6" in st["how"],
               "a recipe changed after the yes is a notice and a named warning on the send, while "
               "call 6 is Omar's", f"{found} {notices} {st}")
        globals()["LAPSE_ON_RECIPE_CHANGE"] = True
        try:
            st = approval_status(st["page"], {}, st["page"].read_text(encoding="utf-8"))
        finally:
            globals()["LAPSE_ON_RECIPE_CHANGE"] = False
        report(not st["approved"] and "recipe changed after the yes" in st["how"],
               "with the call-6 switch on, the same approval is refused", str(st))
        case = tmp / "spent-then-ticked"
        plates, prints, scoring, bets = _build(case)
        _then(_approve("minis-09", "| 2026-10-03 | approved | Omar | recipe {hash} | sent 2026-10-03 |"),
              _timeline_add("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
                            "| 2026-10-03 | sent | from Bambu Studio |"),
              _edit("minis-09", "- [ ] **Approve**", "- [x] **Approve**"))(plates)
        page = plates / "minis-09.md"
        text = page.read_text(encoding="utf-8")
        st = approval_status(page, parse_frontmatter(text)[0], text)
        report(not st["approved"] and "was sent 2026-10-03" in st["how"] and "not recorded" in st["how"]
               and st["sends"] == 1,
               "a box still ticked after its approval was spent is not a new yes (the sheets-04 shape)",
               str(st))

        # Claiming less than the prints show is a notice, never a finding.
        case = tmp / "under-claim-is-a-notice"
        plates, prints, scoring, bets = _build(case)
        _mature("experiment", _KEPT, fill=None, row="| 2026-09-28 | judged | x |")(plates)
        found, notices, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
        report(not found and any("would carry repeatable" in n for n in notices),
               "a page under what its prints show is a notice only",
               f"findings={found} notices={notices}")

        # The rubric is read at run time, so raising K turns a repeatable plate back.
        case = tmp / "rubric-raised"
        plates, prints, scoring, bets = _build(case)
        _mature("repeatable", _KEPT)(plates)
        _rubric(plates).write_text(_RUBRIC_MD.replace("keeps_for_repeatable: 2",
                                                      "keeps_for_repeatable: 3"), encoding="utf-8")
        found, _, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
        report(any("last 3 verdicts" in f for f in found), "the rubric's K is the one applied",
               str(found))

        # A standing approval (D-095): only production, still earned, on its promoted recipe.
        cases = iter(range(100))

        def standing(*steps) -> tuple[bool, str]:
            case = tmp / f"standing-{next(cases)}"
            plates, prints, _, bets = _build(case)
            for s in steps:
                s(plates)
            ctx = context(prints, bets, _rubric(plates))
            page = plates / "minis-09.md"
            text = page.read_text(encoding="utf-8")
            data, _ = parse_frontmatter(text)
            ev = maturity_evidence(page, data, ctx["history"], ctx["runs"], ctx["rubric"])
            return standing_approval(page, data, ev, text)

        prod = _mature("production", _KEPT[:1], own=_CLEAN_OWN)
        ok, why = standing(prod)
        report(ok, "a production plate, still earned, on its promoted recipe stands approved", why)
        ok, why = standing()
        report(not ok and "not production" in why, "an experiment has no standing approval", why)
        ok, why = standing(prod, _record_adjust)
        report(not ok and "prints now show" in why,
               "a production page whose latest run came back adjust loses it before it is demoted",
               why)
        ok, why = standing(_mature("production", _KEPT[:1], own=_CLEAN_OWN, standing=False))
        report(not ok and "no standing row" in why,
               "a production plate with no standing row in its table does not stand approved", why)
        ok, why = standing(prod, _edit_recipe("bed: x2d", "bed: x2d\nspacing: 4"))
        report(not ok and "--derive minis-09" in why,
               "a production recipe edited in place loses it, and says to derive a new plate", why)

        # A recipe's yaml params and a record's JSON params name the same piece.
        report(piece_key("x.bkr", "Hex", {"gap": 0.1, "h": 4}) == piece_key("x.bkr", "Hex", {"h": 4.0, "gap": 0.1})
               and piece_key("x.bkr", None, {}) == piece_key("x.bkr", "", None)
               and piece_key("x.bkr", "Hex", {"gap": 0.1}) != piece_key("x.bkr", "Hex", {"gap": 0.15}),
               "a piece is its file, piece and params, however they are written", "")

        # A sampler sheet's pieces are its card and every cell, as `bambu slice sheet` records
        # them; two cells of one model cut to different windows are two pieces.
        case = tmp / "sheet-pieces"
        case.mkdir()
        (case / "s.yaml").write_text(
            "card: { bkr: 'bikar:cards.bkr', piece: Card }\ncells:\n"
            "  - { name: A, bkr: 'bikar:c.bkr', piece: Coaster, window: '30@0,0' }\n"
            "  - { name: B, bkr: 'bikar:c.bkr', piece: Coaster, window: '30@9,1' }\n"
            "  - { name: C, stl: src/x.stl, window: '30@0,0' }\n", encoding="utf-8")
        got = recipe_pieces(case / "s.md", {"recipe": "s.yaml"})
        report(isinstance(got, dict) and len(got) == 4
               and piece_key("3d-models:src/x.stl", None, {}, "30@0,0") in got
               and piece_key("bikar:c.bkr", "Coaster", {}, "30@9,1") in got,
               "a sheet's card and cells are its pieces, a window part of each", str(got))

        # The ranking: held plates are listed apart, and `after` beats ROI.
        w = yaml.safe_load(_WEIGHTS_MD.split("```yaml\n")[1].split("```")[0])["weights"]
        a = {"plate": "a", "stage": "waiting", "risk": "ok", "kind": "new", "bets": [],
             "unblocks": ["x"], "minutes": 60, "grams": 0, "answers": "a"}
        b = {**a, "plate": "b", "unblocks": ["x", "y", "z"], "after": ["a"]}
        c = {**a, "plate": "c", "risk": "hold", "unblocks": ["x", "y", "z", "w"]}
        order = [t[0]["plate"] for t in rank([a, b, c], w)]
        report(order == ["a", "b"], "rank keeps `after` and leaves a held plate out",
               f"got {order}")
        text = render_queue([a, b, c], w)
        report("**Held for hardware risk:** [c](c.md)." in text, "the queue names the held plate",
               text)
        d = {**a, "plate": "d", "stage": "planned", "minutes": None, "grams": None,
             "unblocks": ["x", "y", "z", "w", "v"], "needs": ["a build"]}
        e = {**d, "plate": "e", "unblocks": ["x"]}
        order = [t[0]["plate"] for t in rank([a, b, d, e], w)]
        text = render_queue([a, b, d, e], w)
        report(order == ["a", "b"] and "[d](d.md) (value 12), [e](e.md) (value 4)." in text,
               "a planned plate is listed by value apart from the ranked queue", f"{order} {text}")

        # The JSON the hub reads ranks exactly as the table does, and carries the page's facts.
        for p in (a, b, c):
            p.update({"times_printed": 0, "runs": [], "bed_plates": 1, "pictures": []})
        data = queue_json([a, b, c], w, {"a": "a — first"}, approved_on={"b": "2026-10-03"})
        report([q["plate"] for q in data["queue"]] == ["a", "b"]
               and data["queue"][0]["title"] == "a — first"
               and [h["plate"] for h in data["held"]] == ["c"] and data["planned"] == [],
               "the JSON queue is the table's order, titled, with the held plate apart", str(data))
        report([(q["approved"], q["approved_on"]) for q in data["queue"]]
               == [(False, None), (True, "2026-10-03")],
               "the JSON's approved facts are each page's open approval", str(data["queue"]))
        report(data["queue"][0]["page"] == "docs/design/plates/a.md",
               "the JSON names each page by its path in the repo, for the hub's pictures", str(data["queue"][0]))

        # --rank --json refuses while a page is wrong, rather than ranking around it.
        import contextlib
        import io
        case = tmp / "json-refuses"
        plates, prints, scoring, bets = _build(case)
        _edit("minis-08", "grams: 30", "grams: null")(plates)
        with contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()):
            code = rank_json(plates, prints, scoring, bets, _rubric(plates))
        report(code == 1 and out.getvalue() == "", "--rank --json refuses a page with a finding",
               f"exit {code}, stdout {out.getvalue()!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    if "--write" in argv:
        return rewrite()
    if "--rank" in argv and "--json" in argv:
        return rank_json()
    if "--rank" in argv:
        _, _, _, rendered = check_tree(PLATES, PRINTS, SCORING, BETS)
        if rendered is None:
            return run()
        print(rendered)
        return 0
    return run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
