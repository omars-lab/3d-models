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
      box (or a yes in chat) is the input; the manage-approvals skill's `plate_approve.py`
      writes the row and unticks the box. Covers is `iteration N @ <commit>`: the iteration of
      the recipe the decision was made on, and the master commit that holds it (P9). An
      approval's Spent by is empty while it is open, `sent <date>` once a send used it,
      `replaced <date>` when a later decision took its place, or `reset <date>` when the recipe
      changed under it (P9); held and standing rows say `—`. Checked: the table
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

  P9  **A yes covers one iteration** (D-097, Omar's answer to print-review call 6). A plate's
      recipe changes in place, and each change is the next iteration, numbered per plate in
      the manage-approvals skill's `approvals.yaml`; the page says `iteration: N`. Checked: the
      page and the file agree on N; the recipe now is iteration N (its content, so a comment
      or key order is not a change and a reprint as-is passes); each approved or standing row
      covers an iteration the file has, through a commit on master that holds it; an open yes
      covers the latest iteration, and a `reset` date has a later iteration that day. The
      load-bearing case: a recipe edited after a yes with nothing recorded. That edit resets
      the yes, so the commit cannot go in until `plate_approve.py --iterate` writes the next
      iteration and marks the yes `reset`. A production recipe is P8's: it does not iterate,
      it is derived.

  P10 **Print log.** What the printer said while a plate printed, appended by the
      monitor-print skill's `print_monitor.py` to its own file, `print-logs/<plate>.md` beside
      the pages: `| Time (UTC) | Event | Layer | Done | What the printer said |`, one row per
      change. The page links it from its frontmatter, `print_log: '[[print-logs/<plate>|print
      log]]'`, and keeps no log in its body. A plate with no print yet has no log. Checked: the
      link names a log that exists, every log is linked from its plate's page and names that
      plate, the header, each row's time (`YYYY-MM-DD HH:MM`) in order, its event in
      PRINT_EVENTS, and that rows are only ever added at the end: every row master has is
      still there, unchanged, in its place, and a log master has is not deleted. A `finished`
      row is the printer's word, not a print record: it does not count toward
      `times_printed`, and the timeline's `printed` row still waits for a record (P3, P6). The
      load-bearing cases: a row with an event the monitor never writes, which means the table
      was typed by hand or by a different tool, and a row master has that was edited.

Not a finding: a ticked Approve or Hold box that the table does not record yet. It prints a
notice, because the fix is a read-back by whoever runs the skill, and a whole-tree gate that
failed on it would block every other session's commit until then; the send refuses it. Nor is
a page that claims less maturity than its prints show: experiment asks nothing, and promoting
is a choice.

  rank:        python3 .claude/gates/plates_gate.py --rank
  as data:     python3 .claude/gates/plates_gate.py --rank --json   (3d-model-hub's plate queue)
  rewrite:     python3 .claude/gates/plates_gate.py --write
  wholesale:   make validate-prints (hook 39 runs it after the prints gate)
  override:    PRINTS_GATE_OK=1 git commit
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "manage-approvals" / "scripts"))
import iterations as it  # noqa: E402
from iterations import recipe_hash  # noqa: E402,F401 — plate_grade and plate_approve read it here
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
# The print log (P10): the printer's own report while a plate prints, one row per change,
# written by the monitor-print skill's print_monitor.py. `watching` is the monitor's first look;
# `stalled` is RUNNING with no new layer or percent for a while; `lost` is the monitor giving up
# when the printer stops answering.
PRINT_LOG_HEAD = "| Time (UTC) | Event | Layer | Done | What the printer said |"
# Each plate's log is its own file in this folder beside the pages, outside the page glob.
LOGS = "print-logs"
PRINT_EVENTS = ("watching", "preparing", "printing", "paused", "resumed", "progress", "stalled",
                "error", "finished", "failed", "stopped", "lost")
LOG_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*\|\s*([a-z]+)\s*\|(.*)$")
DECISIONS = ("approved", "held", "standing")
TABLE_FROM = "2026-10-03"
# A yes covers one iteration of the recipe (D-097, Omar's answer to print-review call 6): a
# change makes the next iteration, which resets the open yes (`reset <date>`).
SPENT = re.compile(r"^(sent|replaced|reset) (\d{4}-\d{2}-\d{2})$")
APPROVE_TOOL = ".claude/skills/manage-approvals/scripts/plate_approve.py"

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


def log_link(plate: str) -> str:
    """The page's `print_log:` property: a wikilink, so Obsidian opens the log from the page."""
    return f"[[{LOGS}/{plate}|print log]]"


def table_lines(text: str) -> list[str]:
    """Every table line of a print log, header first."""
    return [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]


def print_log(text: str) -> tuple[list[tuple[str, str]], str | None]:
    """A print log's table as ([(time, event)], problem). A line that starts with `|` and is
    neither the header, the rule, nor a timed row is a problem, so a hand-typed row cannot
    hide by failing to match."""
    lines = table_lines(text)
    if not lines or lines[0] != PRINT_LOG_HEAD:
        return [], f"the table header is not {PRINT_LOG_HEAD}"
    rows = []
    for ln in lines[2:]:
        r = LOG_ROW.match(ln)
        if not r:
            return rows, f"row '{ln[:60]}' has no `YYYY-MM-DD HH:MM` time"
        rows.append((r.group(1), r.group(2)))
    return rows, None


def appended_only(before: str, now: str) -> str | None:
    """Why `now` is not `before` with rows added at the end, or None when it is. Only the
    table counts: the intro can be reworded, a row the printer reported cannot."""
    old, new = table_lines(before), table_lines(now)
    for i, ln in enumerate(old):
        if i >= len(new):
            return f"row {i - 1} ('{ln[:60]}') is gone"
        if new[i] != ln:
            return f"row {i - 1} was '{ln[:60]}' and is now '{new[i][:60]}'"
    return None


def check_print_logs(plates: Path, pages: list) -> list[str]:
    """P10: the logs in `print-logs/`, the pages' links to them, and no log left in a page."""
    out: list[str] = []
    linked: set[str] = set()
    for path, data, body, err in pages:
        if err:
            continue
        name = path.stem
        if re.search(r"^## Print log\b", body, flags=re.MULTILINE):
            out.append(f"{name}: P10 the page has a '## Print log'; the log lives in "
                       f"{LOGS}/{name}.md, linked from the page's print_log property")
        link = data.get("print_log")
        if link is None:
            continue
        if link != log_link(name):
            out.append(f"{name}: P10 print_log is {link!r}, not {log_link(name)!r}")
        elif not (plates / LOGS / f"{name}.md").is_file():
            out.append(f"{name}: P10 print_log names {LOGS}/{name}.md, which does not exist")
        else:
            linked.add(name)
    logs = plates / LOGS
    for log in sorted(logs.glob("*.md")):
        name, shown = log.stem, f"{LOGS}/{log.name}"
        text = log.read_text(encoding="utf-8")
        data, err = parse_frontmatter(text)
        if err or (data or {}).get("plate") != name:
            out.append(f"{shown}: P10 its frontmatter's plate is not '{name}'")
        if name not in linked:
            out.append(f"{shown}: P10 no plate page links it — {name}.md needs "
                       f"print_log: '{log_link(name)}'")
        rows, problem = print_log(text)
        if problem:
            out.append(f"{shown}: P10 {problem}")
        for t, ev in rows:
            if ev not in PRINT_EVENTS:
                out.append(f"{shown}: P10 event '{ev}' at {t} is not one of {list(PRINT_EVENTS)}")
        times_seen = [t for t, _ in rows]
        if times_seen != sorted(times_seen):
            out.append(f"{shown}: P10 rows are not in time order")
        before = it._git(log, "show", f"{it.MASTER}:./{log.name}")
        why = appended_only(before, text) if before is not None else None
        if why:
            out.append(f"{shown}: P10 the log is append-only and {why} against {it.MASTER}")
    on_master = it._git(plates / "README.md", "ls-tree", "--name-only", it.MASTER, f"{LOGS}/")
    for rel in (on_master or "").split():
        if rel.endswith(".md") and not (plates / rel).is_file():
            out.append(f"{rel}: P10 the log is append-only and {it.MASTER} has it, but it is gone")
    return out


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


def iterations_of(path: Path) -> list[dict]:
    """The plate's recipe iterations, oldest first, from the manage-approvals store."""
    return it.read_store(it.store_for(path.parent))[0].get(path.stem, [])


def covers_now(path: Path) -> tuple[str | None, str]:
    """(what a yes given now covers, `iteration N @ <commit>`; or None and why it cannot be
    given). The recipe here must be its latest iteration, and that iteration must be on master:
    the commit is how anyone later reads exactly what was approved."""
    h, its = recipe_hash(path), iterations_of(path)
    if h is None:
        return None, f"no readable recipe beside the page ({path.stem}.yaml)"
    if not its or its[-1]["recipe"] != h:
        return None, (f"the recipe is not a recorded iteration yet — record it first: "
                      f"`python3 {APPROVE_TOOL} {path.stem} --iterate`")
    commit = it.master_commit(path)
    if commit is None or it.hash_at(path, commit) != h:
        return None, (f"iteration {its[-1]['iteration']} of the recipe is not on {it.MASTER} yet: "
                      "merge it first, since a yes names the master commit it approved")
    return f"iteration {its[-1]['iteration']} @ {commit}", ""


def approval_status(path: Path, data: dict, body: str) -> dict:
    """{approved, how, row, sends}: may this plate go out on a yes, one per send (D-093)?
    Only an open approval on the recipe as it is now. A ticked box is not one until it is a row:
    a box ticked before a send made outside the CLI looks exactly like a fresh one."""
    sends = sum(1 for _, ev, _ in timeline(body) if ev == "sent")
    rows, bad = approvals(body)
    if bad:
        return {"approved": False, "how": bad, "row": None, "sends": sends}
    row = open_approval(rows)
    record = (f"record it with `python3 {APPROVE_TOOL} {path.stem} --approved "
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
    lapsed = yes_lapsed(path, row)
    if lapsed:
        return {"approved": False, "row": row, "sends": sends,
                "how": f"the approval of {row['date']} no longer holds: {lapsed}"}
    nth = "its first send" if sends == 0 else f"send {sends + 1}"
    how = f"approved on {row['date']} ({row['by']}), {row['covers']}, for {nth}"
    return {"approved": True, "row": row, "sends": sends, "how": how}


def yes_lapsed(path: Path, row: dict) -> str | None:
    """Why an open yes does not cover the recipe as it is now, or None when it does (D-097): it
    names the latest iteration, its commit on master holds that iteration, and the recipe here
    is still it. A comment-only edit is the same recipe, so a reprint as-is keeps its yes."""
    got = it.parse_covers(row["covers"])
    if got is None:
        return f"it covers {row['covers']!r}, not `iteration N @ <commit>`"
    n, commit = got
    its, h = iterations_of(path), recipe_hash(path)
    if not its or n != its[-1]["iteration"]:
        return (f"it covers iteration {n}, but the recipe is at iteration "
                f"{its[-1]['iteration'] if its else 0} — record it as `reset` "
                f"(`python3 {APPROVE_TOOL} {path.stem} --iterate` does) and ask Omar again")
    if its[-1]["recipe"] != h:
        return (f"the recipe changed after the yes (iteration {n} is {its[-1]['recipe']}, the "
                f"recipe is now {h}) — record the change with `python3 {APPROVE_TOOL} "
                f"{path.stem} --iterate`, which resets the yes, and ask Omar again")
    if it.hash_at(path, commit) != its[-1]["recipe"]:
        return (f"its commit {commit} does not hold iteration {n} of the recipe — a yes names the "
                "master commit it approved")
    if not it.on_master(path, commit):
        return f"its commit {commit} is not on {it.MASTER}"
    return None


def check_approvals(name: str, data: dict, body: str) -> list[str]:
    """P2: the table reads, its rows agree with each other and with the timeline's sends."""
    out = [f"{name}: P2 `{k}` is in the frontmatter — approvals moved to the page's "
           "## Approvals table (D-096)" for k in ("approved", "approved_on") if k in data]
    rows, bad = approvals(body)
    if bad:
        return out + [f"{name}: P2 {bad} — `python3 {APPROVE_TOOL} {name} --table` "
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
        if dec in ("approved", "standing") and not it.COVERS.match(r["covers"]) and not (
                d < TABLE_FROM and r["covers"] == "—"):
            out.append(f"{where}: an {dec} row covers {r['covers']!r}, not "
                       "`iteration N @ <commit>`")
        if dec == "approved":
            m = SPENT.match(spent)
            if spent and not m:
                out.append(f"{where}: Spent by {spent!r} is not empty, `sent <date>`, "
                           "`replaced <date>` or `reset <date>`")
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
                    and isinstance(m.get("production_fill"), (int, float))
                    and not isinstance(m["production_fill"], bool)
                    and 0 <= m["production_fill"] <= 1):
                raise ValueError(f"{rubric}: maturity needs keeps_for_repeatable (a positive "
                                 "whole number) and production_fill (in [0, 1], 0 for no bar)")
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
            params = stl_scale_params(it.get("scale")) if it.get("stl") else it.get("params")
            key = piece_key(src, it.get("piece"), params, it.get("window"))
            out[key] = out.get(key, 0) + (it.get("count") or 1)
    return out


def stl_scale_params(scale) -> dict:
    """An `stl:` item's scale as the params its record carries, as `bambu slice compose` writes
    them (`stlScaleParams` in compose.ts): none at 1, `scale` when every axis is the same, else
    `scale_x/_y/_z`. Without this a phone at full size and one at a third are one piece."""
    x, y, z = (scale, scale, scale) if isinstance(scale, (int, float)) else (scale or [1, 1, 1])
    if x == y == z:
        return {} if x == 1 else {"scale": x}
    return {"scale_x": x, "scale_y": y, "scale_z": z}


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
    if not last:
        return ("no standing row in the Approvals table — promotion writes it "
                f"(`python3 {APPROVE_TOOL} {path.stem} --standing`)")
    got = it.parse_covers(last[-1]["covers"])
    its = iterations_of(path)
    held = its[got[0] - 1]["recipe"] if got and 0 < got[0] <= len(its) else None
    if held != data.get("recipe_hash"):
        return (f"the last standing row ({last[-1]['date']}) covers {last[-1]['covers']}, not the "
                f"iteration promoted (recipe_hash {data.get('recipe_hash')})")
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
    """A tick the table does not hold yet. A notice, not a finding: the read-back is the next
    session's, and the send refuses it. (A recipe changed after a yes is P9's finding.)"""
    name, out = path.stem, []
    if TICKED_APPROVE.search(body):
        out.append(f"{name}: an Approve box is ticked but not in the Approvals table — record it: "
                   f"`python3 {APPROVE_TOOL} {name} --approved --by \"Omar, tick\"`")
    if TICKED_HOLD.search(body):
        out.append(f"{name}: the Hold box is ticked but not in the Approvals table — record it: "
                   f"`python3 {APPROVE_TOOL} {name} --held --by \"Omar, tick\"`")
    return out


def check_iterations(path: Path, data: dict, body: str, store: dict[str, list[dict]]
                     ) -> list[str]:
    """P9 (D-097): the page, the store and the recipe agree on which iteration this is, and
    every yes covers an iteration whose master commit holds it. The load-bearing case: a recipe
    edited after the yes with nothing recorded — that edit is what resets the yes, so the commit
    that makes it cannot go in until the iteration is written."""
    name, out = path.stem, []
    its, h = store.get(name, []), recipe_hash(path)
    k = its[-1]["iteration"] if its else 0
    at = data.get("iteration", 0 if h is None else None)
    if not isinstance(at, int) or isinstance(at, bool) or at != k:
        out.append(f"{name}: P9 the page says iteration {at!r}, the iterations file "
                   f"({it.STORE_REL}) has {k}")
    iterate = f"`python3 {APPROVE_TOOL} {name} --iterate`"
    if h is not None and data.get("maturity") != "production":
        if not its:
            out.append(f"{name}: P9 no iteration of the recipe is recorded — {iterate} records "
                       "iteration 1")
        elif its[-1]["recipe"] != h:
            out.append(f"{name}: P9 the recipe changed since iteration {k} (it was "
                       f"{its[-1]['recipe']}, it is now {h}) — {iterate} records iteration "
                       f"{k + 1}, which resets an open yes (D-097). A comment-only edit is not a "
                       "change, so a reprint as-is needs nothing")
    rows, _ = approvals(body)
    for i, r in enumerate(rows):
        got = it.parse_covers(r["covers"])
        if r["decision"] not in ("approved", "standing") or got is None:
            continue
        n, commit = got
        where = f"{name}: P9 Approvals row {i + 1} ({r['date']})"
        if not 0 < n <= k:
            out.append(f"{where}: covers iteration {n}, which the iterations file does not have")
        elif it.hash_at(path, commit) != its[n - 1]["recipe"]:
            out.append(f"{where}: commit {commit} does not hold iteration {n} of the recipe "
                       f"({its[n - 1]['recipe']})")
        elif not it.on_master(path, commit):
            out.append(f"{where}: commit {commit} is not on {it.MASTER}; a yes covers a merged "
                       "recipe")
        m = SPENT.match(r["spent"])
        if r["decision"] == "approved" and not r["spent"] and n != k:
            out.append(f"{where}: the yes is open on iteration {n}, but the recipe is at {k} — "
                       f"it is `reset` ({iterate} writes it)")
        if m and m.group(1) == "reset" and not any(
                e["iteration"] > n and e["date"] == m.group(2) for e in its):
            out.append(f"{where}: reset on {m.group(2)}, but no later iteration is dated that day")
    return out


def page_findings(path: Path, data: dict, body: str, ctx: dict) -> tuple[list[str], list[str]]:
    """(findings, notices) for one page: P1-P4 and P6, then P8 once the shape holds."""
    f = check_page(path, data, body, ctx["records"], ctx["bet_ids"])
    if f:
        return f, []
    f = check_iterations(path, data, body, ctx["store"])
    m, n = check_maturity(path, data, body, ctx["history"], ctx["runs"], ctx["rubric"])
    return f + m, n


def context(prints: Path, bets: Path, rubric: Path, plates: Path = PLATES) -> dict:
    store, bad = it.read_store(it.store_for(plates))
    return {"records": records_by_plate(prints),
            "bet_ids": set(re.findall(r"CAL-[A-Z]+-\d+", bets.read_text(encoding="utf-8"))),
            "history": piece_history(prints), "runs": plate_runs(prints),
            "rubric": read_rubric(rubric), "store": store, "store_bad": bad}


def check_tree(plates: Path, prints: Path, scoring: Path, bets: Path, rubric: Path = RUBRIC
               ) -> tuple[list[str], list[str], int, str | None]:
    """(findings, notices, pages checked, rendered queue or None)."""
    findings: list[str] = []
    notices: list[str] = []
    try:
        ctx = context(prints, bets, rubric, plates)
    except (OSError, ValueError) as e:
        return [f"rubric: P8 {e}"], [], 0, None
    pages = read_pages(plates)
    # P9 — the iterations file reads, and names only plates that have a page
    findings += [f"iterations: P9 {b}" for b in ctx["store_bad"]]
    findings += [f"{n}: P9 the iterations file has this plate, but it has no page"
                 for n in sorted(set(ctx["store"]) - {p.stem for p, *_ in pages})]
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
    findings += check_print_logs(plates, pages)
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
    ctx = context(prints, bets, rubric, plates)
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


def _head(plates: Path) -> str:
    return it._git(plates / "x.md", "rev-parse", "HEAD").strip()[:10]


def _approve(page: str, *rows: str):
    """Add Approvals rows to a fixture page; `{covers}` is iteration 1 at the fixture's master
    commit, which is what a yes given on the fixture as built covers."""
    def f(plates: Path) -> None:
        cov = f"iteration 1 @ {_head(plates)}"
        p = plates / f"{page}.md"
        lines = p.read_text(encoding="utf-8").split("\n")
        end = lines.index(_SEP) + 1
        while end < len(lines) and lines[end].startswith("|"):
            end += 1  # after the rows already there, so the table stays in date order
        lines[end:end] = [r.replace("{covers}", cov) for r in rows]
        p.write_text("\n".join(lines), encoding="utf-8")
    return f


def _store_edit(fn):
    """Change the fixture's iterations file: `fn` takes and returns {plate: [entries]}."""
    def f(plates: Path) -> None:
        store = it.store_for(plates)
        it.write_store(store, fn(it.read_store(store)[0]))
    return f


def _git_init(tmp: Path) -> None:
    """Make the fixture a repo whose master holds it as built, as the real tree's does."""
    import subprocess
    for args in (["add", "-A"],
                 ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "fixture"],
                 ["update-ref", "refs/remotes/origin/master", "HEAD"]):
        subprocess.run(["git", "-C", str(tmp), *args], check=True, capture_output=True)


def _branch_yes(plates: Path) -> None:
    """A yes naming a commit made on a branch: it holds iteration 1, but master never had it."""
    import subprocess
    subprocess.run(["git", "-C", str(plates), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-q", "--allow-empty", "-m", "branch"], check=True)
    head = _head(plates)
    _approve("minis-08", f"| 2026-10-03 | approved | Omar | iteration 1 @ {head} | |")(plates)


def _timeline_add(page: str, after: str, row: str):
    return _edit(page, after, f"{after}\n{row}")


def _log_text(plate: str, rows: tuple[str, ...], head: str = PRINT_LOG_HEAD) -> str:
    table = "\n".join([head, "|---|---|---|---|---|", *rows])
    return f"---\nplate: {plate}\n---\n\n# {plate} — print log\n\nWhat the printer said.\n\n{table}\n"


def _print_log(page: str, *rows: str, head: str = PRINT_LOG_HEAD, link: str | None = None,
               log_plate: str | None = None):
    """Give a fixture plate a print log and link it from the page, as the monitor writes them.
    `link` replaces the page's print_log value; `log_plate` the log's own plate."""
    def f(plates: Path) -> None:
        (plates / LOGS).mkdir(exist_ok=True)
        (plates / LOGS / f"{page}.md").write_text(
            _log_text(log_plate or page, rows, head), encoding="utf-8")
        _edit(page, f"plate: {page}\n",
              f"plate: {page}\nprint_log: '{link or log_link(page)}'\n")(plates)
    return f


def _on_master(plates: Path) -> None:
    """Commit the fixture as it stands and make it master, as a merged PR would."""
    import subprocess
    root = plates.parents[1]
    for args in (["add", "-A"],
                 ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "merged"],
                 ["update-ref", "refs/remotes/origin/master", "HEAD"]):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


_LOGGED = ("| 2026-09-26 14:02 | watching | 0/20 | 0% | PREPARE |",
           "| 2026-09-26 14:30 | printing | 1/20 | 2% | RUNNING |")


def _log_rewrite(*rows: str):
    """The log on master, then rewritten to `rows` on the branch."""
    def f(plates: Path) -> None:
        _print_log("minis-09", *_LOGGED)(plates)
        _on_master(plates)
        (plates / LOGS / "minis-09.md").write_text(_log_text("minis-09", rows), encoding="utf-8")
    return f


def _log_deleted(plates: Path) -> None:
    _print_log("minis-09", *_LOGGED)(plates)
    _on_master(plates)
    (plates / LOGS / "minis-09.md").unlink()
    _edit("minis-09", f"print_log: '{log_link('minis-09')}'\n", "")(plates)


def _log_in_page(plates: Path) -> None:
    p = plates / "minis-09.md"
    table = "\n".join([PRINT_LOG_HEAD, "|---|---|---|---|---|", *_LOGGED])
    p.write_text(p.read_text(encoding="utf-8") + f"\n## Print log\n\n{table}\n", encoding="utf-8")


def _build(tmp: Path) -> tuple[Path, Path, Path, Path]:
    plates, prints = tmp / "docs" / "plates", tmp / "docs" / "prints"
    (plates / "minis-08-media").mkdir(parents=True)
    import subprocess
    subprocess.run(["git", "init", "-q", str(tmp)], check=True)  # the store is found by its repo
    (plates / "minis-08-media" / "sheet.png").write_bytes(b"png")
    rec = prints / "2026-09-26-minis-09"
    rec.mkdir(parents=True)
    (rec / "index.md").write_text('---\nrun: 2026-09-26-minis-09\nplate: "minis-09 — a test"\n---\n',
                                  encoding="utf-8")
    base = {"iteration": 1, "times_printed": 0, "runs": [],
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
    del fm["iteration"]  # no recipe yet, so no iteration of it
    (plates / "sheets-09.md").write_text(
        _page("sheets-09", fm, ["| 2026-10-01 | proposed | the design |"]), encoding="utf-8")
    scoring = tmp / "scoring.md"
    scoring.write_text(_WEIGHTS_MD, encoding="utf-8")
    bets = tmp / "bets.md"
    bets.write_text("CAL-CST-06 dovetail neck\n", encoding="utf-8")
    (plates / "README.md").write_text(f"# Plates\n\n{Q_START}\n{Q_END}\n", encoding="utf-8")
    (tmp / "rubric.md").write_text(_RUBRIC_MD, encoding="utf-8")
    it.write_store(tmp / it.STORE_REL, {
        n: [{"iteration": 1, "recipe": recipe_hash(plates / f"{n}.md"), "date": "2026-09-25"}]
        for n in ("minis-08", "minis-09")})
    rewrite(plates, prints, scoring, bets, quiet=True, rubric=_rubric(plates))
    _git_init(tmp)
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
                     "{covers} | — |")(plates)
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
     _approve("minis-08", "| 2026-10-04 | approved | Omar, tick | {covers} | |"),
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
                    "| 2026-10-03 | approved | Omar, tick | {covers} | replaced 2026-10-04 |",
                    "| 2026-10-04 | held | Omar, in chat | {covers} | — |",
                    "| 2026-10-05 | approved | Omar, in chat | {covers} | sent 2026-10-05 |"),
           _timeline_add("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
                         "| 2026-10-05 | sent | by bambu print send |")), None),
    ("P2 two approvals open at once",
     _then(_edit("minis-08", "stage: waiting", "stage: approved"),
           _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | {covers} | |",
                    "| 2026-10-04 | approved | Omar, tick | {covers} | |")),
     "P2 2 approvals are open"),
    ("P2 an open approval with a hold after it",
     _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | {covers} | |",
              "| 2026-10-04 | held | Omar | {covers} | — |"),
     "is open but a later decision came after it"),
    ("P2 an approval spent by a send the timeline does not have",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | {covers} | sent 2026-10-05 |"),
     "P2 1 approval(s) spent by a send on 2026-10-05, but the timeline has 0"),
    ("P2 replaced with nothing decided that day",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | {covers} | replaced 2026-10-04 |"),
     "replaced on 2026-10-04, but no later decision that day"),
    ("P2 a decision outside the vocabulary",
     _approve("minis-09", "| 2026-10-03 | maybe | Omar | {covers} | — |"),
     "decision 'maybe' is not one of"),
    ("P2 an approval since the table began that covers no recipe",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | — | replaced 2026-10-03 |",
              "| 2026-10-03 | held | Omar | — | — |"),
     "an approved row covers '—', not `iteration N @ <commit>`"),
    ("P2 an approval moved in from before the table may cover no recipe",
     _then(_approve("minis-09", "| 2026-10-02 | approved | Omar | — | sent 2026-10-02 |"),
           _timeline_add("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
                         "| 2026-10-02 | sent | from Bambu Studio |")), None),
    ("P2 a row with a cell missing",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | {covers} |"),
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
           _approve("minis-09", "| 2026-09-28 | standing | promoted | iteration 9 @ 0000000000 | — |")),
     "covers iteration 9 @ 0000000000, not the iteration promoted"),
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
    ("P9 a recipe edited with nothing recorded (the load-bearing case: it would reset a yes)",
     _edit_recipe("bed: x2d", "bed: x2d\nspacing: 4"),
     "P9 the recipe changed since iteration 1"),
    ("P9 a recipe that only gained a comment is the same iteration",
     _edit_recipe("bed: x2d", "# packed\nbed: x2d"), None),
    ("P9 the page names another iteration than the file",
     _edit("minis-08", "iteration: 1", "iteration: 2"),
     "P9 the page says iteration 2, the iterations file"),
    ("P9 a recipe with no iteration recorded",
     _store_edit(lambda d: {k: v for k, v in d.items() if k != "minis-08"}),
     "P9 no iteration of the recipe is recorded"),
    ("P9 a yes still open on an older iteration",
     _then(_store_edit(lambda d: {**d, "minis-08": d["minis-08"] + [
         {"iteration": 2, "recipe": d["minis-08"][0]["recipe"], "date": "2026-10-04"}]}),
           _edit("minis-08", "iteration: 1", "iteration: 2"),
           _edit("minis-08", "stage: waiting", "stage: approved"),
           _approve("minis-08", "| 2026-10-03 | approved | Omar | {covers} | |")),
     "the yes is open on iteration 1, but the recipe is at 2"),
    ("P9 a reset with no later iteration that day",
     _approve("minis-09", "| 2026-10-03 | approved | Omar | {covers} | reset 2026-10-04 |"),
     "reset on 2026-10-04, but no later iteration is dated that day"),
    ("P9 a yes naming a commit that does not exist",
     _then(_edit("minis-08", "stage: waiting", "stage: approved"),
           _approve("minis-08", "| 2026-10-03 | approved | Omar | iteration 1 @ ffffffffff | |")),
     "commit ffffffffff does not hold iteration 1"),
    ("P9 a yes naming a branch commit, not one on master (a squash merge drops it)",
     _then(_edit("minis-08", "stage: waiting", "stage: approved"), _branch_yes),
     "is not on origin/master"),
    ("P9 the iterations file names a plate with no page",
     _store_edit(lambda d: {**d, "minis-07": [
         {"iteration": 1, "recipe": "0" * 12, "date": "2026-10-01"}]}),
     "minis-07"),
    ("P9 the iterations file numbered out of order",
     _store_edit(lambda d: {**d, "minis-09": [{**d["minis-09"][0], "iteration": 2}]}),
     "entry 1 is numbered 2"),
    ("P10 a print log as the monitor writes it, through a pause",
     _print_log("minis-09", "| 2026-09-26 14:02 | watching | 0/20 | 0% | PREPARE |",
                "| 2026-09-26 14:09 | paused | 0/20 | 0% | 0500-8051: the plate on the bed is not "
                "the one the file was sliced for |",
                "| 2026-09-26 14:30 | resumed | 1/20 | 2% | RUNNING |"), None),
    ("P10 an event the monitor never writes (the load-bearing case: a typed row)",
     _print_log("minis-09", "| 2026-09-26 14:02 | jammed | 3/20 | 9% | |"),
     "P10 event 'jammed'"),
    ("P10 rows out of time order",
     _print_log("minis-09", "| 2026-09-26 14:30 | printing | 1/20 | 2% | RUNNING |",
                "| 2026-09-26 14:02 | watching | 0/20 | 0% | PREPARE |"),
     "P10 rows are not in time order"),
    ("P10 a row with no time",
     _print_log("minis-09", "| today | printing | 1/20 | 2% | RUNNING |"), "has no `YYYY-MM-DD HH:MM`"),
    ("P10 a table with another header",
     _print_log("minis-09", "| 2026-09-26 14:02 | watching | | | |",
                head="| Time | Event | Note |"), "P10 the table header"),
    ("P10 rows added at the end of a log master has",
     _log_rewrite(*_LOGGED, "| 2026-09-26 15:10 | finished | 20/20 | 100% | FINISH |"), None),
    ("P10 a row master has, edited (the load-bearing case: the log is append-only)",
     _log_rewrite(_LOGGED[0], "| 2026-09-26 14:30 | printing | 2/20 | 5% | RUNNING |"),
     "P10 the log is append-only and row 2 was"),
    ("P10 a row master has, dropped",
     _log_rewrite(_LOGGED[1]), "P10 the log is append-only and row 1 was"),
    ("P10 a log master has, deleted with its link",
     _log_deleted, "print-logs/minis-09.md: P10 the log is append-only and origin/master has it"),
    ("P10 a log left in the page's body",
     _log_in_page, "minis-09: P10 the page has a '## Print log'"),
    ("P10 a log no page links",
     _then(_print_log("minis-09", *_LOGGED),
           _edit("minis-09", f"print_log: '{log_link('minis-09')}'\n", "")),
     "print-logs/minis-09.md: P10 no plate page links it"),
    ("P10 a link to another plate's log",
     _print_log("minis-09", *_LOGGED, link=log_link("minis-08")),
     "minis-09: P10 print_log is"),
    ("P10 a link to a log that is not there",
     _edit("minis-09", "plate: minis-09\n", f"plate: minis-09\nprint_log: '{log_link('minis-09')}'\n"),
     "which does not exist"),
    ("P10 a log that names another plate",
     _print_log("minis-09", *_LOGGED, log_plate="minis-08"),
     "P10 its frontmatter's plate is not 'minis-09'"),
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

        # An open approval: the plate stands approved on the iteration it covers (D-097). A
        # comment-only edit is the same recipe, so the yes holds; a real change, once recorded
        # with --iterate, resets it and the plate needs a new yes.
        def opened(*steps):
            case = tmp / f"open-{next(opens)}"
            plates, prints, scoring, bets = _build(case)
            _then(_edit("minis-08", "stage: waiting", "stage: approved"),
                  _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | {covers} | |"),
                  *steps)(plates)
            rewrite(plates, prints, scoring, bets, quiet=True, rubric=_rubric(plates))
            found, notices, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
            page = plates / "minis-08.md"
            text = page.read_text(encoding="utf-8")
            data, _ = parse_frontmatter(text)
            return found, notices, approval_status(page, data, text) | {"page": page}

        def changed(pl: Path) -> None:
            (pl / "minis-08.yaml").write_text("bed: x2d\nspacing: 4\n", encoding="utf-8")

        def iterated(pl: Path) -> None:
            """What `plate_approve.py --iterate` writes for that change on 2026-10-04."""
            _store_edit(lambda d: {**d, "minis-08": d["minis-08"] + [
                {"iteration": 2, "recipe": recipe_hash(pl / "minis-08.md"),
                 "date": "2026-10-04"}]})(pl)
            _edit("minis-08", "iteration: 1", "iteration: 2")(pl)
            _edit("minis-08", "stage: approved", "stage: waiting")(pl)
            page = pl / "minis-08.md"
            text = page.read_text(encoding="utf-8")
            row = re.search(r"^\| 2026-10-03 \| approved \|.*\| \|$", text, re.M).group(0)
            page.write_text(text.replace(row, row[:-2] + " reset 2026-10-04 |"), encoding="utf-8")

        opens = iter(range(100))
        found, notices, st = opened()
        report(not found and not notices and st["approved"] and "for its first send" in st["how"],
               "an open approval on the recipe as it is lets the plate go out",
               f"{found} {notices} {st}")
        # Inside a git hook GIT_DIR is set, and the commit lookups must still find the recipe:
        # sheets-04b's yes was refused at commit time while the gate passed by hand (2026-10-03).
        case = tmp / "inside-a-hook"
        plates, prints, scoring, bets = _build(case)
        _then(_edit("minis-08", "stage: waiting", "stage: approved"),
              _approve("minis-08", "| 2026-10-03 | approved | Omar, tick | {covers} | |"))(plates)
        rewrite(plates, prints, scoring, bets, quiet=True, rubric=_rubric(plates))
        saved = {k: os.environ.get(k) for k in ("GIT_DIR", "GIT_INDEX_FILE")}
        os.environ.update(GIT_DIR=str(case / ".git"), GIT_INDEX_FILE=str(case / ".git" / "index"))
        try:
            found, _, _, _ = check_tree(plates, prints, scoring, bets, _rubric(plates))
        finally:
            for k, v in saved.items():
                os.environ.pop(k, None) if v is None else os.environ.update({k: v})
        report(not found, "an open approval checks clean inside a git hook (GIT_DIR set)", str(found))
        found, notices, st = opened(lambda pl: (pl / "minis-08.yaml").write_text(
            "# packed tighter next time\nbed: x2d\n", encoding="utf-8"))
        report(not found and st["approved"],
               "a comment-only edit keeps the iteration and the yes (a reprint as-is)",
               f"{found} {st}")
        found, notices, st = opened(changed)
        report(any("P9 the recipe changed since iteration 1" in f and "--iterate" in f
                   for f in found) and not st["approved"] and "--iterate" in st["how"],
               "a recipe changed after the yes with nothing recorded is a finding, and the send "
               "refuses it (the load-bearing case)", f"{found} {st}")
        found, notices, st = opened(changed, iterated)
        report(not found and not st["approved"] and "reset 2026-10-04" in st["how"],
               "once --iterate records iteration 2, the yes reads reset and the page is clean",
               f"{found} {st}")
        found, notices, st = opened(changed, iterated,
                                    _approve("minis-08", "| 2026-10-04 | approved | Omar | "
                                             "iteration 2 @ 0123456789 | |"),
                                    _edit("minis-08", "stage: waiting", "stage: approved"))
        report(any("commit 0123456789 does not hold iteration 2" in f for f in found)
               and not st["approved"],
               "a yes on iteration 2 naming a commit that does not hold it is refused",
               f"{found} {st}")

        case = tmp / "spent-then-ticked"
        plates, prints, scoring, bets = _build(case)
        _then(_approve("minis-09", "| 2026-10-03 | approved | Omar | {covers} | sent 2026-10-03 |"),
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

        # A fill of 0 is no bar (round log 2026-10-04); below 0 or above 1 is a typo.
        _rubric(plates).write_text(_RUBRIC_MD.replace("production_fill: 0.5",
                                                      "production_fill: 0"), encoding="utf-8")
        report(read_rubric(_rubric(plates))["production_fill"] == 0,
               "a production_fill of 0 reads as no fill bar", "")
        for bad_fill in ("-0.1", "1.5", "true"):
            _rubric(plates).write_text(_RUBRIC_MD.replace("production_fill: 0.5",
                                                          f"production_fill: {bad_fill}"),
                                       encoding="utf-8")
            try:
                read_rubric(_rubric(plates))
                refused = False
            except ValueError:
                refused = True
            report(refused, f"a production_fill of {bad_fill} is refused", "")

        # A standing approval (D-095): only production, still earned, on its promoted recipe.
        cases = iter(range(100))

        def standing(*steps) -> tuple[bool, str]:
            case = tmp / f"standing-{next(cases)}"
            plates, prints, _, bets = _build(case)
            for s in steps:
                s(plates)
            ctx = context(prints, bets, _rubric(plates), plates)
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

        # A local STL at two scales is two pieces, keyed as `bambu slice compose` records them
        # (phones-02: the full phone and the small one were one piece of count 4).
        case = tmp / "stl-scales"
        case.mkdir()
        (case / "p.yaml").write_text(
            "items:\n  - { stl: i/p.stl, count: 2 }\n  - { stl: i/p.stl, scale: 0.5 }\n"
            "  - { stl: i/p.stl, scale: [0.3125, 0.3125, 0.5], count: 2 }\n", encoding="utf-8")
        got = recipe_pieces(case / "p.md", {"recipe": "p.yaml"})
        src = "3d-models:i/p.stl"
        report(got == {piece_key(src, None, {}): 2, piece_key(src, None, {"scale": 0.5}): 1,
                       piece_key(src, None, {"scale_x": 0.3125, "scale_y": 0.3125,
                                             "scale_z": 0.5}): 2},
               "a local STL at each scale is its own piece, keyed like its record", str(got))

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
