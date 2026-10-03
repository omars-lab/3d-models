#!/usr/bin/env python3
"""Write Omar's decisions on a plate into its page's `## Approvals` table, and read them back.

    python3 tools/plate_approve.py <plate> --approved --by "Omar, tick"   a yes (tick or chat)
    python3 tools/plate_approve.py <plate> --held --by "Omar, in chat"    a hold
    python3 tools/plate_approve.py <plate> --standing                     a production plate's
                                                    standing approval, written on promotion
    python3 tools/plate_approve.py <plate> --sent [--via "Bambu Studio"] [--standing]
                                                    a send: spends the open approval
    python3 tools/plate_approve.py <plate> --status [--json]   may it go out now, and why
    python3 tools/plate_approve.py <plate> --table             add an empty table to a page
    python3 tools/plate_approve.py --self-test

`<plate>` is a plate name (`sheets-04b`) or the path of its page. `--date` defaults to today.

Why a table and not frontmatter (D-096): one `approved:` field holds one yes, and a design gets
many — approved, held, approved again after a change, sent, approved for a reprint. The tick box
on the page (or a yes in chat) stays the way Omar answers; this tool turns it into a dated row
naming who decided and the recipe the decision covers (`recipe <hash>`, the plates gate's
`recipe_hash`), then unticks the box so the next tick is a new answer. A send fills the open
approval's `Spent by`, so one yes is good for one send (D-093). A recipe changed after the yes is
named on the send; whether it voids the yes is Omar's open call 6 (print-review-design §9), one
switch in the plates gate. The plates gate (P2) reads the same table with the
same parser, so what this writes and what the gate checks cannot disagree; `bambu print send`
asks `--status` before it sends and calls `--sent` after.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "gates"))

import plates_gate as pg  # noqa: E402

INTRO = ("Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick "
         "under Your call, or a yes in chat, becomes a row here through `tools/plate_approve.py`; "
         "a send spends the open approval.")
TABLE = f"{pg.APPROVALS_HEAD}\n|---|---|---|---|---|"
UNTICK = {"Approve": re.compile(r"^(\s*-\s*)\[[xX]\](\s*\*{0,2}Approve)", re.MULTILINE),
          "Hold": re.compile(r"^(\s*-\s*)\[[xX]\](\s*\*{0,2}Hold)", re.MULTILINE)}
STANDING_BY = "plate_grade.py, promoted to production (D-095)"


class Refused(Exception):
    """The decision cannot be written as asked; the message says why."""


def page_of(plate: str, plates: Path = pg.PLATES) -> Path:
    p = Path(plate)
    return p.resolve() if p.suffix == ".md" else plates / f"{plate}.md"


def root_of(page: Path) -> Path:
    """The repo a page sits in: <root>/docs/design/plates/<page>.md."""
    return page.parents[3]


def split(text: str) -> tuple[str, str]:
    """(frontmatter block with its fences, body)."""
    end = text.find("\n---", 4)
    if not text.startswith("---\n") or end == -1:
        raise Refused("the page has no frontmatter")
    return text[:end + 4], text[end + 4:]


def read(page: Path) -> tuple[str, dict, str]:
    if not page.is_file():
        raise Refused(f"no plate page {page}")
    text = page.read_text(encoding="utf-8")
    data, err = pg.parse_frontmatter(text)
    if err or not data:
        raise Refused(f"the page's frontmatter does not parse: {err}")
    return text, data, split(text)[1]


def set_stage(head: str, stage: str) -> str:
    return re.sub(r"^stage:.*$", f"stage: {stage}", head, count=1, flags=re.MULTILINE)


def with_table(body: str) -> str:
    """The body with an empty Approvals table, placed before the Timeline, if it had none."""
    if pg.APPROVALS.search(body):
        return body
    section = f"## Approvals\n\n{INTRO}\n\n{TABLE}\n\n"
    at = body.find("\n## Timeline")
    if at == -1:
        return body.rstrip("\n") + "\n\n" + section
    return body[:at + 1] + section + body[at + 1:]


def render(rows: list[dict]) -> str:
    return "\n".join([TABLE] + [f"| {r['date']} | {r['decision']} | {r['by']} | {r['covers']} | "
                                f"{r['spent']} |".replace("|  |", "| |") for r in rows])


def write_rows(body: str, rows: list[dict]) -> str:
    """Replace the table's lines in the Approvals section; prose around it stays."""
    m = pg.APPROVALS.search(body)
    sec = m.group(1)
    lines = sec.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.strip().startswith("|")]
    new = render(rows).split("\n")
    if idx:
        lines[idx[0]:idx[-1] + 1] = new
    else:
        lines[1:1] = new
    start = m.start(1)
    return body[:start] + "\n".join(lines) + body[m.end(1):]


def add_timeline(body: str, row: str) -> str:
    m = re.search(r"^## Timeline\b.*?$(.*?)(?=^## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    if not m:
        return (body.rstrip("\n") + "\n\n## Timeline\n\n| Date | What happened | Where it is "
                f"written |\n|---|---|---|\n{row}\n")
    lines = m.group(1).split("\n")
    last = max((i for i, ln in enumerate(lines) if ln.strip().startswith("|")), default=0)
    lines.insert(last + 1, row)
    return body[:m.start(1)] + "\n".join(lines) + body[m.end(1):]


def _rows(body: str) -> list[dict]:
    rows, bad = pg.approvals(body)
    if bad:
        raise Refused(f"{bad} — add one with --table")
    return rows


def _replace_open(rows: list[dict], date: str) -> None:
    row = pg.open_approval(rows)
    if row:
        row["spent"] = f"replaced {date}"


def decide(page: Path, decision: str, by: str, date: str) -> str:
    """Write an approved, held or standing row; returns the row as written."""
    text, data, body = read(page)
    head = split(text)[0]
    body = with_table(body)
    rows = _rows(body)
    if rows and rows[-1]["date"] > date:
        raise Refused(f"the table's last row is dated {rows[-1]['date']}, after {date}")
    now = pg.covers(page)
    if not by.strip():
        raise Refused("--by is empty: say who decided, and how (\"Omar, tick\", \"Omar, in chat\")")
    if decision == "approved":
        if data.get("stage") in ("planned", "retired"):
            raise Refused(f"stage is {data.get('stage')!r}: a plate with no recipe to print, or one "
                          "retired, cannot be approved")
        if now is None:
            raise Refused(f"no readable recipe beside the page ({page.stem}.yaml)")
        _replace_open(rows, date)
        row = {"date": date, "decision": "approved", "by": by, "covers": now, "spent": ""}
        head = set_stage(head, "approved")
        body = UNTICK["Approve"].sub(r"\1[ ]\2", body)
    elif decision == "held":
        _replace_open(rows, date)
        row = {"date": date, "decision": "held", "by": by, "covers": now or "—", "spent": "—"}
        if data.get("stage") == "approved":
            head = set_stage(head, "waiting")
        body = UNTICK["Hold"].sub(r"\1[ ]\2", body)
    else:
        pinned = data.get("recipe_hash")
        if data.get("maturity") != "production":
            raise Refused(f"maturity is {data.get('maturity')!r}: only a production plate stands "
                          "approved (D-095)")
        if not pinned or f"recipe {pinned}" != now:
            raise Refused(f"the pinned recipe_hash {pinned!r} is not the recipe now ({now}); "
                          "promotion pins it first")
        row = {"date": date, "decision": "standing", "by": by, "covers": now, "spent": "—"}
    rows.append(row)
    page.write_text(head + write_rows(body, rows), encoding="utf-8")
    return render([row]).split("\n")[-1]


def status(page: Path, paths: tuple[Path, Path, Path] | None = None) -> dict:
    """{approved, how, sends, standing}: what `bambu print send` asks before it sends. `paths`
    is (prints, bets, rubric), by default the ones in the page's own repo."""
    try:
        text, data, body = read(page)
    except Refused as e:
        return {"approved": False, "how": str(e), "sends": 0, "standing": False}
    lost = ""
    if data.get("maturity") == "production":
        root = root_of(page)
        prints, bets, rubric = paths or (root / p.relative_to(pg.ROOT)
                                         for p in (pg.PRINTS, pg.BETS, pg.RUBRIC))
        try:
            ctx = pg.context(prints, bets, rubric)
            ev = pg.maturity_evidence(page, data, ctx["history"], ctx["runs"], ctx["rubric"])
            ok, why = pg.standing_approval(page, data, ev, body)
        except (OSError, ValueError) as e:
            ok, why = False, f"the grade did not run: {e}"
        sends = sum(1 for _, ev_, _ in pg.timeline(body) if ev_ == "sent")
        if ok:
            return {"approved": True, "how": f"standing approval: {why} (D-095)", "sends": sends,
                    "standing": True}
        lost = f"; no standing approval: {why}"
    st = pg.approval_status(page, data, body)
    return {"approved": st["approved"], "how": st["how"] + ("" if st["approved"] else lost),
            "sends": st["sends"], "standing": False}


def sent(page: Path, date: str, via: str, standing: bool,
         paths: tuple[Path, Path, Path] | None = None) -> str:
    """A send: spend the open approval (or note the standing one), untick, stage sent, and log
    it on the timeline. Returns the timeline row. Refuses a plate that is not approved."""
    st = status(page, paths)
    if not st["approved"]:
        raise Refused(f"not approved for a send: {st['how']}")
    if standing != st["standing"]:
        raise Refused("--standing given, but the plate goes out on a yes, not a standing approval"
                      if standing else
                      "it stands approved (D-095): pass --standing so the send does not spend a yes")
    text, _, body = read(page)
    head = set_stage(split(text)[0], "sent")
    if standing:
        row = (f"| {date} | sent — by {via}, on the standing approval of a production plate "
               "(D-095) | this page |")
    else:
        rows = _rows(body)
        yes = pg.open_approval(rows)
        yes["spent"] = f"sent {date}"
        body = write_rows(UNTICK["Approve"].sub(r"\1[ ]\2", body), rows)
        row = f"| {date} | sent — by {via}; spends the approval of {yes['date']} | this page |"
    page.write_text(head + add_timeline(body, row), encoding="utf-8")
    return row


# ---------------------------------------------------------------------------

def self_test() -> int:
    import shutil
    import tempfile

    fails = 0

    def check(ok: bool, label: str, why: str = "") -> None:
        nonlocal fails
        fails += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}" + ("" if ok else f" — {why}"))

    tmp = Path(tempfile.mkdtemp(prefix="plate-approve-"))
    try:
        plates, prints, scoring, bets = pg._build(tmp)
        rubric = pg._rubric(plates)
        m8 = plates / "minis-08.md"

        def gate() -> list[str]:
            pg.rewrite(plates, prints, scoring, bets, quiet=True, rubric=rubric)
            return pg.check_tree(plates, prints, scoring, bets, rubric)[0]

        def stage(p: Path) -> str:
            return pg.parse_frontmatter(p.read_text(encoding="utf-8"))[0]["stage"]

        pg._edit("minis-08", "- [ ] **Approve**", "- [x] **Approve**")(plates)
        decide(m8, "approved", "Omar, tick", "2026-10-03")
        text = m8.read_text(encoding="utf-8")
        check("[x] **Approve" not in text and stage(m8) == "approved" and gate() == [],
              "a tick becomes a row: the box is unticked, the stage approved, the gate clean",
              f"{gate()}")
        st = status(m8)
        check(st["approved"] and "Omar, tick" in st["how"], "the status reads the open row", str(st))

        decide(m8, "approved", "Omar, in chat", "2026-10-04")
        rows = pg.approvals(m8.read_text(encoding="utf-8"))[0]
        check([r["spent"] for r in rows] == ["replaced 2026-10-04", ""] and gate() == [],
              "a second yes replaces the first; one stays open", str(rows))

        decide(m8, "held", "Omar, in chat", "2026-10-04")
        st = status(m8)
        check(stage(m8) == "waiting" and not st["approved"] and "held on 2026-10-04" in st["how"]
              and gate() == [], "a hold closes the open yes and puts the plate back to waiting",
              f"{st} {gate()}")

        decide(m8, "approved", "Omar, tick", "2026-10-05")
        row = sent(m8, "2026-10-05", "`bambu print send`", standing=False)
        rows = pg.approvals(m8.read_text(encoding="utf-8"))[0]
        st = status(m8)
        check(stage(m8) == "sent" and rows[-1]["spent"] == "sent 2026-10-05"
              and "spends the approval of 2026-10-05" in row and not st["approved"]
              and st["sends"] == 1 and gate() == [],
              "a send spends the yes, logs the send, and the next send is refused",
              f"{rows} {st} {gate()}")
        try:
            sent(m8, "2026-10-05", "x", standing=False)
            check(False, "a second send on the same yes is refused")
        except Refused as e:
            check("was sent 2026-10-05" in str(e), "a second send on the same yes is refused", str(e))

        decide(m8, "approved", "Omar, in chat", "2026-10-06")
        rows = pg.approvals(m8.read_text(encoding="utf-8"))[0]
        check(len(rows) == 5 and status(m8)["approved"] and gate() == [],
              "a reprint is one more yes on the same design", str(rows))
        (plates / "minis-08.yaml").write_text("bed: x2d\nspacing: 4\n", encoding="utf-8")
        st = status(m8)
        check(st["approved"] and "open call 6" in st["how"],
              "a recipe changed after the yes is named on the send (call 6 is Omar's)", str(st))

        for plate, decision, want in (
                ("sheets-09", "approved", "stage is 'planned'"),
                ("minis-09", "standing", "only a production plate"),
                ("minis-08", "approved", "after 2026-10-01")):
            date = "2026-10-01" if want.startswith("after") else "2026-10-07"
            try:
                decide(plates / f"{plate}.md", decision, "Omar", date)
                check(False, f"{decision} on {plate} is refused ({want})")
            except Refused as e:
                check(want in str(e), f"{decision} on {plate} is refused ({want})", str(e))

        bare = tmp / "bare.md"
        bare.write_text("---\nplate: bare\n---\n\n# bare\n\n## Your call\n\n- [ ] **Approve**\n\n"
                        "## Timeline\n\n| a | b | c |\n|---|---|---|\n", encoding="utf-8")
        bare.write_text(split(bare.read_text())[0] + with_table(split(bare.read_text())[1]))
        text = bare.read_text(encoding="utf-8")
        check(pg.approvals(split(text)[1]) == ([], None)
              and text.index("## Approvals") < text.index("## Timeline"),
              "--table adds an empty table before the timeline", text)

        pg._mature("production", pg._KEPT[:1], own=pg._CLEAN_OWN, standing=False)(plates)
        m9 = plates / "minis-09.md"
        st = status(m9, (prints, bets, rubric))
        check(not st["approved"] and "no standing approval" in st["how"],
              "a production plate with no standing row is not standing", str(st))
        decide(m9, "standing", STANDING_BY, "2026-10-03")
        st = status(m9, (prints, bets, rubric))
        check(gate() == [] and st["approved"] and st["standing"],
              "a standing row written on promotion passes P8 and lets it go out", f"{gate()} {st}")
        row = sent(m9, "2026-10-04", "`bambu print send`", standing=True, paths=(prints, bets, rubric))
        rows = pg.approvals(m9.read_text(encoding="utf-8"))[0]
        check("standing approval" in row and rows[-1]["spent"] == "—" and gate() == [],
              "a standing send spends nothing", f"{row} {gate()}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("self-test: " + ("PASS" if not fails else f"FAIL ({fails})"))
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plate", nargs="?", help="a plate name, or the path of its page")
    act = ap.add_mutually_exclusive_group()
    for flag in ("approved", "held", "sent", "status", "table", "self-test"):
        act.add_argument(f"--{flag}", action="store_true")
    ap.add_argument("--standing", action="store_true",
                    help="alone: write the standing row; with --sent: a standing send")
    ap.add_argument("--by", help="who decided, and how (\"Omar, tick\", \"Omar, in chat\")")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--via", default="`bambu print send`", help="with --sent: what sent it")
    ap.add_argument("--json", action="store_true", help="with --status: as JSON")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.plate:
        ap.error("name a plate")
    page = page_of(a.plate)
    try:
        if a.status:
            st = status(page)
            print(json.dumps(st) if a.json else
                  f"{page.stem}: {'approved' if st['approved'] else 'not approved'} — {st['how']}")
            return 0
        if a.table:
            text, _, body = read(page)
            page.write_text(split(text)[0] + with_table(body), encoding="utf-8")
            print(f"{page.stem}: Approvals table present")
            return 0
        if a.sent:
            print(sent(page, a.date, a.via, a.standing))
            return 0
        if a.approved or a.held or a.standing:
            decision = "approved" if a.approved else "held" if a.held else "standing"
            by = a.by if a.by is not None else (STANDING_BY if decision == "standing" else "")
            print(decide(page, decision, by, a.date))
            return 0
    except Refused as e:
        print(f"plate_approve: {page.stem}: {e}", file=sys.stderr)
        return 1
    ap.error("say what to record: --approved, --held, --standing, --sent, --status or --table")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
