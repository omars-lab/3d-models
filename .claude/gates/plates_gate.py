#!/usr/bin/env python3
"""Plates gate for 3d-models: a plate page tells the truth about its plate.

`docs/plates/<plate>.yaml` is what gets sliced; `docs/plates/<plate>.md` is the page Omar
reviews it on: what it is, why print it, pictures, cost and risk, their approval tick box, and
a timeline of what happened to it. Its frontmatter holds the few facts the queue ranks on and
the facts that must never drift — whether Omar approved it, and how many times it printed.
The design is `docs/design/printing/print-review-design.md`; these are its §6 rules.

  P1  **Shape.** The frontmatter parses and carries every key in REQUIRED; `plate` is the
      file name; `recipe` is the `.yaml` beside it; `stage`, `kind` and `risk` are in their
      vocabularies; every `bets` id is a real bet in `bets.md`; a plate the queue ranks
      carries its cost (`minutes`, `grams`, `bed_plates`) as positive numbers. A `planned`
      plate is designed but cannot be built yet: it may have no recipe and no cost, and it
      names what it waits on in `needs:`. Only a planned plate has `needs:` — a plate that
      still waits on a build is not ready to rank, so it cannot sit at a later stage.

  P2  **Approval.** `approved` is true, false, or empty (the plate went out before pages
      existed, and nobody asked). True if and only if `approved_on` is a date. A plate at
      `approved` is approved. A plate at `sent` or `printed` is not `approved: false` — the
      load-bearing case: nothing goes out that the page says Omar did not approve.

  P3  **Count.** `runs` is exactly the print records under `docs/prints/` whose `plate:`
      starts with this plate's name, and `times_printed` is how many there are. Hard case:
      a page that types `times_printed: 0` and `runs: []` correctly for each other still
      fails when a record exists — the count is checked against the records, not against
      itself.

  P4  **Pictures.** Every listed picture exists. A page waiting on Omar, or approved, shows
      at least one: nobody approves a plate they have not seen.

  P5  **Coverage.** Every plate `.yaml` has a page and every page has a `.yaml`.

  P6  **Timeline.** The `## Timeline` table's rows are dated, in order, and name an event in
      EVENTS. An approved page has an `approved` row on `approved_on`; every run has a
      `printed` row naming it, and there are as many `printed` rows as `times_printed`.

  P7  **The queue is current.** The block between the queue markers in
      `docs/plates/README.md` is exactly what `--write` would write from the pages and the
      weights in the `prioritize-prints` skill's scoring.md. Priority is presented, never
      stored (prints-tab-design §6): no page holds a rank, the queue is recomputed.

Not a finding: a ticked approval box that the frontmatter does not know yet. It prints a
notice, because the fix is a read-back by whoever runs the skill, and a whole-tree gate that
failed on it would block every other session's commit until then.

  rank:        python3 .claude/gates/plates_gate.py --rank
  as data:     python3 .claude/gates/plates_gate.py --rank --json   (3d-model-hub's plate queue)
  rewrite:     python3 .claude/gates/plates_gate.py --write
  wholesale:   make validate-prints (hook 39 runs it after the prints gate)
  override:    PRINTS_GATE_OK=1 git commit
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prints_gate import CAL_ID, parse_frontmatter, record_dirs  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PLATES = ROOT / "docs" / "plates"
PRINTS = ROOT / "docs" / "prints"
SCORING = ROOT / ".claude" / "skills" / "prioritize-prints" / "scoring.md"
BETS = ROOT / ".claude" / "skills" / "calibrate" / "bets.md"

REQUIRED = (
    "plate", "recipe", "stage", "approved", "approved_on", "times_printed", "runs",
    "answers", "kind", "bets", "unblocks", "minutes", "grams", "bed_plates", "risk", "pictures",
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
EVENTS = ("proposed", "reviewed", "approved", "held", "sliced", "sent", "printed", "judged", "retired")

Q_START, Q_END = "<!-- queue:start -->", "<!-- queue:end -->"
ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([a-z]+)\b(.*)$")
TICKED_APPROVE = re.compile(r"^\s*-\s*\[[xX]\]\s*\*{0,2}Approve", re.MULTILINE)


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

    # P2 — approval
    approved, on = data["approved"], data["approved_on"]
    if approved not in (True, False, None):
        out.append(f"{name}: P2 approved {approved!r} is not true, false or empty")
    if (approved is True) != isinstance(on, dt.date):
        out.append(f"{name}: P2 approved is {approved!r} but approved_on is {on!r} — a date "
                   "goes with true, and only with true")
    if stage == "approved" and approved is not True:
        out.append(f"{name}: P2 stage 'approved' but approved is {approved!r}")
    if stage in ("sent", "printed") and approved is False:
        out.append(f"{name}: P2 stage '{stage}' but approved is false — it went out unapproved")
    if stage in ("planned", "proposed", "waiting") and approved is True:
        out.append(f"{name}: P2 approved is true but stage is still '{stage}'")

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
    if approved is True and isinstance(on, dt.date) and not any(
            ev == "approved" and d == on.isoformat() for d, ev, _ in rows):
        out.append(f"{name}: P6 approved on {on} but no 'approved' row on that date")
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
        "weights in [scoring.md](../../.claude/skills/prioritize-prints/scoring.md). Do not edit "
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


def queue_json(pages: list[dict], w: dict, titles: dict[str, str | None]) -> dict:
    """The queue as data, for 3d-model-hub's plate queue: the same ranking `render_queue` writes,
    with the page facts beside it so the hub never parses a plate page itself."""
    def facts(p: dict) -> dict:
        on = p["approved_on"]
        return {
            "plate": p["plate"], "title": titles.get(p["plate"]), "stage": p["stage"],
            "approved": p["approved"], "approved_on": on.isoformat() if isinstance(on, dt.date) else None,
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

def check_tree(plates: Path, prints: Path, scoring: Path, bets: Path
               ) -> tuple[list[str], list[str], int, str | None]:
    """(findings, notices, pages checked, rendered queue or None)."""
    findings: list[str] = []
    notices: list[str] = []
    records = records_by_plate(prints)
    bet_ids = set(re.findall(r"CAL-[A-Z]+-\d+", bets.read_text(encoding="utf-8")))
    pages = read_pages(plates)
    good: list[dict] = []
    for path, data, body, err in pages:
        if err:
            findings.append(f"{path.stem}: P1 {err}")
            continue
        f = check_page(path, data, body, records, bet_ids)
        findings += f
        if not f:
            good.append(data)
        if TICKED_APPROVE.search(body) and data.get("approved") is not True:
            notices.append(f"{path.stem}: an Approve box is ticked but approved is not true yet "
                           "— read it back (prioritize-prints skill, step 1)")
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


def run(plates=PLATES, prints=PRINTS, scoring=SCORING, bets=BETS) -> int:
    findings, notices, n, _ = check_tree(plates, prints, scoring, bets)
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


def sort_pages(plates: Path, prints: Path, bets: Path
               ) -> tuple[list[dict], list[str], dict[str, str | None]]:
    """(pages with no finding, the findings of the rest, each page's title)."""
    records = records_by_plate(prints)
    bet_ids = set(re.findall(r"CAL-[A-Z]+-\d+", bets.read_text(encoding="utf-8")))
    good, bad, titles = [], [], {}
    for path, data, body, err in read_pages(plates):
        f = [f"{path.stem}: {err}"] if err else check_page(path, data, body, records, bet_ids)
        bad += f
        if not f:
            good.append(data)
            titles[data["plate"]] = title_of(body)
    return good, bad, titles


def rank_json(plates=PLATES, prints=PRINTS, scoring=SCORING, bets=BETS) -> int:
    """--rank --json: the queue as JSON on stdout. Refuses, like --write, while a page is wrong."""
    import json
    good, bad, titles = sort_pages(plates, prints, bets)
    if bad:
        print("\n".join(bad), file=sys.stderr)
        print("plates-gate: fix the pages before ranking them", file=sys.stderr)
        return 1
    print(json.dumps(queue_json(good, read_weights(scoring), titles), indent=2))
    return 0


def rewrite(plates=PLATES, prints=PRINTS, scoring=SCORING, bets=BETS, quiet=False) -> int:
    """--write: rewrite the queue block. Refuses while any page has a finding other than P7."""
    good, bad, _ = sort_pages(plates, prints, bets)
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


def _page(plate: str, fm: dict, timeline_rows: list[str], tick: str = " ") -> str:
    return ("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n"
            f"# {plate}\n\n## Your call\n\n- [{tick}] **Approve** — print it as it is\n\n"
            "## Timeline\n\n| Date | What happened | Where |\n|---|---|---|\n"
            + "\n".join(timeline_rows) + "\n")


def _build(tmp: Path) -> tuple[Path, Path, Path, Path]:
    plates, prints = tmp / "docs" / "plates", tmp / "docs" / "prints"
    (plates / "minis-08-media").mkdir(parents=True)
    (plates / "minis-08-media" / "sheet.png").write_bytes(b"png")
    rec = prints / "2026-09-26-minis-09"
    rec.mkdir(parents=True)
    (rec / "index.md").write_text('---\nrun: 2026-09-26-minis-09\nplate: "minis-09 — a test"\n---\n',
                                  encoding="utf-8")
    base = {"approved": False, "approved_on": None, "times_printed": 0, "runs": [],
            "answers": "does it hold", "kind": "new", "bets": ["CAL-CST-06"],
            "unblocks": ["a decision"], "minutes": 120, "grams": 30, "bed_plates": 1,
            "risk": "watch", "pictures": ["minis-08-media/sheet.png"]}
    for n, extra, rows in (
        ("minis-08", {"stage": "waiting"},
         ["| 2026-09-30 | proposed | page written |", "| 2026-09-30 | reviewed | sheet |"]),
        ("minis-09", {"stage": "printed", "approved": None, "times_printed": 1,
                      "runs": ["2026-09-26-minis-09"], "minutes": None, "grams": None,
                      "bed_plates": None, "pictures": []},
         ["| 2026-09-25 | proposed | yaml |",
          "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |"]),
    ):
        (plates / f"{n}.yaml").write_text("bed: x2d\n", encoding="utf-8")
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
    rewrite(plates, prints, scoring, bets, quiet=True)
    return plates, prints, scoring, bets


def _edit(page: str, old: str, new: str):
    def f(plates: Path) -> None:
        p = plates / f"{page}.md"
        text = p.read_text(encoding="utf-8")
        assert old in text, (page, old)
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
    return f


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
    ("P2 approved with no date", _edit("minis-08", "approved: false", "approved: true"),
     "P2 approved is True but approved_on is None"),
    ("P2 stage approved while approved is false",
     _edit("minis-08", "stage: waiting", "stage: approved"), "P2 stage 'approved' but approved"),
    ("P2 sent while the page says not approved (the load-bearing case)",
     _edit("minis-08", "stage: waiting", "stage: sent"), "it went out unapproved"),
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
     _edit("sheets-09", "approved: false\napproved_on: null",
           "approved: true\napproved_on: 2026-10-01"),
     "P2 approved is true but stage is still 'planned'"),
    ("P1 a recipe named that is not there",
     _edit("sheets-09", "recipe: null", "recipe: sheets-09.yaml"),
     "P1 recipe 'sheets-09.yaml' is not the sheets-09.yaml"),
    ("P6 approved with no approved row",
     _edit("minis-08", "stage: waiting\napproved: false\napproved_on: null",
           "stage: approved\napproved: true\napproved_on: 2026-09-30"),
     "P6 approved on 2026-09-30 but no 'approved' row"),
    ("P6 a run with no printed row",
     _edit("minis-09", "| 2026-09-26 | printed | [2026-09-26-minis-09](x) |",
           "| 2026-09-26 | judged | verdicts |"), "P6 run 2026-09-26-minis-09 has no 'printed' row"),
    ("P6 rows out of date order",
     _edit("minis-08", "| 2026-09-30 | reviewed", "| 2026-09-01 | reviewed"),
     "P6 timeline rows are not in date order"),
    ("P7 a page edited, queue not rewritten", _stale_queue, "P7 the queue block is not"),
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
            found, _, _, _ = check_tree(plates, prints, scoring, bets)
            if want is None:
                report(not found, label, f"clean fixture reported {found}")
            else:
                report(any(want in f for f in found), label, f"wanted {want!r}, got {found or 'nothing'}")

        # A ticked box not read back is a notice, never a finding.
        case = tmp / "tick-is-a-notice"
        plates, prints, scoring, bets = _build(case)
        _edit("minis-08", "- [ ] **Approve**", "- [x] **Approve**")(plates)
        found, notices, _, _ = check_tree(plates, prints, scoring, bets)
        report(not found and len(notices) == 1, "a ticked box not read back is a notice only",
               f"findings={found} notices={notices}")

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
            p.update({"approved": False, "approved_on": None, "times_printed": 0, "runs": [],
                      "bed_plates": 1, "pictures": []})
        data = queue_json([a, b, c], w, {"a": "a — first"})
        report([q["plate"] for q in data["queue"]] == ["a", "b"]
               and data["queue"][0]["title"] == "a — first"
               and [h["plate"] for h in data["held"]] == ["c"] and data["planned"] == [],
               "the JSON queue is the table's order, titled, with the held plate apart", str(data))

        # --rank --json refuses while a page is wrong, rather than ranking around it.
        import contextlib
        import io
        case = tmp / "json-refuses"
        plates, prints, scoring, bets = _build(case)
        _edit("minis-08", "grams: 30", "grams: null")(plates)
        with contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()):
            code = rank_json(plates, prints, scoring, bets)
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
