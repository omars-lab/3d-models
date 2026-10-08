#!/usr/bin/env python3
"""Write Omar's decisions on a plate into its page's `## Approvals` table, and read them back.

    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --approved --by "Omar, tick" [--color "#0047BB"]
                                    a yes (tick or chat), on the recipe's latest iteration;
                                    --color names the one color the yes covers
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --held --by "Omar, in chat"    a hold
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --iterate
                                    the recipe changed: record the next iteration, reset the yes
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --standing
                                    a production plate's standing approval, written on promotion
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --sent [--via "Bambu Studio"] [--standing]
                                    a send: spends the open approval
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --status [--json]   may it go out now, and why
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --table             add an empty table to a page
    python3 .claude/skills/manage-approvals/scripts/plate_approve.py --self-test

`<plate>` is a plate name (`sheets-04b`) or the path of its page. `--date` defaults to today.

Why a table and not frontmatter (D-096): one `approved:` field holds one yes, and a design gets
many — approved, held, approved again after a change, sent, approved for a reprint. The tick box
on the page (or a yes in chat) stays the way Omar answers; this tool turns it into a dated row
naming who decided and what the decision covers, then unticks the box so the next tick is a new
answer. A send fills the open approval's `Spent by`, so one yes is good for one send (D-093).

What a yes covers (D-097): an iteration of the recipe and the master commit that holds it,
`iteration 2 @ 1a2b3c4d5e`. The recipe changes in place, with no new plate per version; each
change is the next iteration in `approvals.yaml` beside this skill, and `--iterate` is what
records it. Recording it resets the open yes (`reset <date>`), so a changed plate goes back to
Omar. A comment-only edit is not a change: a reprint as-is keeps its iteration and its yes. The
plates gate (P2, P9; hook 39) reads the same table and file with the same code, so what this
writes and what the gate checks cannot disagree; `bambu print send` asks `--status` before it
sends and calls `--sent` after.

What color a yes covers (print-time-color-map §5): a one-color recipe fixes no color (call 18),
so the color is named at the send. A yes may name it too, `iteration 2 @ 1a2b3c4d5e in #0047BB`,
and then the send must name the same one; a new color is a new yes (D-103). A yes that names
none covers whatever color the send names. A recipe that fixes its own colors (a multi-color
plate, or a frozen production one) refuses `--color`: the recipe already says.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))

import iterations as it  # noqa: E402 — beside this file, already on sys.path
import plates_gate as pg  # noqa: E402

INTRO = ("Every yes or hold Omar gives this plate, one row each, oldest first (D-096). A tick "
         "under Your call, or a yes in chat, becomes a row here through the manage-approvals skill's "
         "`plate_approve.py`; a send spends the open approval, and a recipe change resets it.")
TABLE = f"{pg.APPROVALS_HEAD}\n|---|---|---|---|---|"
UNTICK = {"Approve": re.compile(r"^(\s*-\s*)\[[xX]\](\s*\*{0,2}Approve)", re.MULTILINE),
          "Hold": re.compile(r"^(\s*-\s*)\[[xX]\](\s*\*{0,2}Hold)", re.MULTILINE)}
STANDING_BY = "plate_grade.py, promoted to production (D-095)"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def recipe_colors(page: Path):
    """What the recipe beside the page fixes in `profile.color` (a color, a list, or None)."""
    try:
        doc = pg.yaml.safe_load(page.with_suffix(".yaml").read_text(encoding="utf-8"))
    except (OSError, pg.yaml.YAMLError):
        return None
    prof = doc.get("profile") if isinstance(doc, dict) else None
    return prof.get("color") if isinstance(prof, dict) else None


def yes_color(page: Path, color: str | None) -> str | None:
    """The color a yes will name, uppercased; refuses one that is not `#RRGGBB`, and any on a
    recipe that fixes its own colors."""
    if color is None:
        return None
    if not HEX.match(color):
        raise Refused(f"--color {color!r} is not #RRGGBB")
    fixed = recipe_colors(page)
    if fixed:
        raise Refused(f"the recipe fixes its colors ({fixed}), so a yes names none: --color is for "
                      "a one-color plate whose color is named at the send (call 18)")
    return color.upper()


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


def decide(page: Path, decision: str, by: str, date: str, color: str | None = None) -> str:
    """Write an approved, held or standing row; returns the row as written. `color` (approved
    only) is the one color the yes covers, written into its Covers cell."""
    text, data, body = read(page)
    head = split(text)[0]
    body = with_table(body)
    rows = _rows(body)
    if rows and rows[-1]["date"] > date:
        raise Refused(f"the table's last row is dated {rows[-1]['date']}, after {date}")
    now, why = pg.covers_now(page)
    if not by.strip():
        raise Refused("--by is empty: say who decided, and how (\"Omar, tick\", \"Omar, in chat\")")
    if color is not None and decision != "approved":
        raise Refused("--color goes with --approved: only a yes names the color it covers")
    if decision == "approved":
        if data.get("stage") in ("planned", "retired"):
            raise Refused(f"stage is {data.get('stage')!r}: a plate with no recipe to print, or one "
                          "retired, cannot be approved")
        if now is None:
            raise Refused(why)
        hexc = yes_color(page, color)
        _replace_open(rows, date)
        row = {"date": date, "decision": "approved", "by": by,
               "covers": f"{now} in {hexc}" if hexc else now, "spent": ""}
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
        if now is None:
            raise Refused(why)
        if not pinned or pinned != pg.recipe_hash(page):
            raise Refused(f"the pinned recipe_hash {pinned!r} is not the recipe now "
                          f"({pg.recipe_hash(page)}); promotion pins it first")
        row = {"date": date, "decision": "standing", "by": by, "covers": now, "spent": "—"}
    rows.append(row)
    page.write_text(head + write_rows(body, rows), encoding="utf-8")
    return render([row]).split("\n")[-1]


def set_iteration(head: str, n: int) -> str:
    """The frontmatter with `iteration: n`, after the `recipe:` line when it had none."""
    if re.search(r"^iteration:", head, flags=re.MULTILINE):
        return re.sub(r"^iteration:.*$", f"iteration: {n}", head, count=1, flags=re.MULTILINE)
    return re.sub(r"^(recipe:.*)$", rf"\1\niteration: {n}", head, count=1, flags=re.MULTILINE)


def iterate(page: Path, date: str) -> str:
    """The recipe changed: record its next iteration, and reset the open yes (D-097). Refuses
    when nothing changed, since a reprint as-is keeps its iteration and its yes; and a production
    recipe, which does not change in place (D-095). Returns what it did, in one line."""
    text, data, body = read(page)
    h = pg.recipe_hash(page)
    if h is None:
        raise Refused(f"no readable recipe beside the page ({page.stem}.yaml)")
    store = it.store_for(page.parent)
    every, bad = it.read_store(store) if store.is_file() else ({}, [])
    if bad:
        raise Refused(f"{it.STORE_REL} has problems, fix them first: " + "; ".join(bad))
    its = every.get(page.stem, [])
    if its and its[-1]["recipe"] == h:
        raise Refused(f"the recipe is iteration {its[-1]['iteration']} as it is (a comment-only "
                      "edit is not a change); a reprint as-is keeps its iteration and its yes")
    if its and data.get("maturity") == "production":
        raise Refused("a production recipe does not change in place (D-095): put the change on a "
                      f"new experiment plate (`python3 tools/plate_grade.py --derive {page.stem} "
                      f"<new>`) and put {page.stem}.yaml back")
    if its and its[-1]["date"] > date:
        raise Refused(f"iteration {its[-1]['iteration']} is dated {its[-1]['date']}, after {date}")
    n = len(its) + 1
    every[page.stem] = its + [{"iteration": n, "recipe": h, "date": date}]
    head = set_iteration(split(text)[0], n)
    did = f"{page.stem}: iteration {n} of the recipe ({h})"
    if pg.APPROVALS.search(body):
        rows = _rows(body)
        yes = pg.open_approval(rows)
        if yes:
            yes["spent"] = f"reset {date}"
            body = write_rows(body, rows)
            did += f"; the yes of {yes['date']} is reset, so it goes back to Omar"
            if data.get("stage") == "approved":
                head = set_stage(head, "waiting")
    it.write_store(store, every)
    page.write_text(head + body, encoding="utf-8")
    return did


def status(page: Path, paths: tuple[Path, Path, Path] | None = None) -> dict:
    """{approved, how, sends, standing, color, recipe, iteration}: what `bambu print send` asks
    before it sends. `recipe` is the plate's recipe hash now (iterations.py), which the send
    compares with the one its slice recorded; `color` is the one color the open yes covers, or None
    when it names none (then the send's --color is the send's to name). `iteration` is the
    recipe's iteration number when the recipe as it is now is the latest one recorded, else None:
    `bambu slice compose` cuts it into each piece's id (D-109). `paths` is (prints, bets, rubric),
    by default the ones in the page's own repo."""
    h = pg.recipe_hash(page)
    return {**_approval(page, paths), "recipe": h, "iteration": recipe_iteration(page, h)}


def recipe_iteration(page: Path, h: str | None) -> int | None:
    """The iteration the recipe is now: the latest recorded one, when its hash is the recipe's.
    An edit not yet recorded with --iterate has none, and neither does an older recipe put back."""
    its = pg.iterations_of(page)
    return its[-1]["iteration"] if h is not None and its and its[-1]["recipe"] == h else None


def _approval(page: Path, paths: tuple[Path, Path, Path] | None) -> dict:
    try:
        text, data, body = read(page)
    except Refused as e:
        return {"approved": False, "how": str(e), "sends": 0, "standing": False, "color": None}
    lost = ""
    if data.get("maturity") == "production":
        root = root_of(page)
        prints, bets, rubric = paths or (root / p.relative_to(pg.ROOT)
                                         for p in (pg.PRINTS, pg.BETS, pg.RUBRIC))
        try:
            ctx = pg.context(prints, bets, rubric, page.parent)
            ev = pg.maturity_evidence(page, data, ctx["history"], ctx["runs"], ctx["rubric"])
            ok, why = pg.standing_approval(page, data, ev, body)
        except (OSError, ValueError) as e:
            ok, why = False, f"the grade did not run: {e}"
        sends = sum(1 for _, ev_, _ in pg.timeline(body) if ev_ == "sent")
        if ok:
            return {"approved": True, "how": f"standing approval: {why} (D-095)", "sends": sends,
                    "standing": True, "color": None}
        lost = f"; no standing approval: {why}"
    st = pg.approval_status(page, data, body)
    row = st["row"] if st["approved"] else None
    return {"approved": st["approved"], "how": st["how"] + ("" if st["approved"] else lost),
            "sends": st["sends"], "standing": False,
            "color": it.covers_color(row["covers"]) if row else None}


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
        row = (f"| {date} | sent — by {via}; spends the approval of {yes['date']}, "
               f"{yes['covers']} | this page |")
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

        def merge(root: Path) -> None:
            """What a merge to master does for the fixture: commit, and move origin/master."""
            import subprocess
            for args in (["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit",
                                         "-q", "-m", "merged"],
                         ["update-ref", "refs/remotes/origin/master", "HEAD"]):
                subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)

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
        try:
            iterate(m8, "2026-10-06")
            check(False, "--iterate on a recipe that did not change is refused")
        except Refused as e:
            check("reprint as-is" in str(e), "--iterate on a recipe that did not change is refused",
                  str(e))
        check(status(m8)["iteration"] == 1, "the status names the recipe's iteration",
              str(status(m8)))
        (plates / "minis-08.yaml").write_text("bed: x2d\nspacing: 4\n", encoding="utf-8")
        st = status(m8)
        check(not st["approved"] and "--iterate" in st["how"] and any("P9" in f for f in gate()),
              "a recipe changed after the yes is refused on the send and found by the gate",
              f"{st} {gate()}")
        check(st["iteration"] is None, "an edit not yet recorded has no iteration", str(st))
        did = iterate(m8, "2026-10-07")
        check(status(m8)["iteration"] == 2, "--iterate gives the edit iteration 2",
              str(status(m8)))
        rows = pg.approvals(m8.read_text(encoding="utf-8"))[0]
        fm = pg.parse_frontmatter(m8.read_text(encoding="utf-8"))[0]
        check("reset" in did and rows[-1]["spent"] == "reset 2026-10-07" and fm["iteration"] == 2
              and stage(m8) == "waiting" and not status(m8)["approved"] and gate() == [],
              "--iterate records iteration 2, resets the yes, and the gate is clean",
              f"{did} {rows[-1]} {fm.get('iteration')} {gate()}")
        try:
            decide(m8, "approved", "Omar, tick", "2026-10-07")
            check(False, "a yes on an iteration not yet on master is refused")
        except Refused as e:
            check("not on origin/master yet" in str(e),
                  "a yes on an iteration not yet on master is refused", str(e))
        merge(tmp)
        decide(m8, "approved", "Omar, tick", "2026-10-07")
        rows = pg.approvals(m8.read_text(encoding="utf-8"))[0]
        check(rows[-1]["covers"].startswith("iteration 2 @ ") and status(m8)["approved"]
              and gate() == [], "once merged, a new yes covers iteration 2 at its master commit",
              f"{rows[-1]} {gate()}")

        decide(m8, "approved", "Omar, in chat", "2026-10-07", color="#0047bb")
        rows = pg.approvals(m8.read_text(encoding="utf-8"))[0]
        st = status(m8)
        check(rows[-1]["covers"].endswith(" in #0047BB") and st["approved"]
              and st["color"] == "#0047BB" and gate() == [],
              "--color goes into the yes's Covers, uppercased; status reports it; the gate passes",
              f"{rows[-1]} {st} {gate()}")
        decide(m8, "approved", "Omar, in chat", "2026-10-07")
        check(status(m8)["color"] is None, "a yes that names no color reports none",
              str(status(m8)))
        for color, decision, want in (("blue", "approved", "not #RRGGBB"),
                                      ("#0047BB", "held", "goes with --approved")):
            try:
                decide(m8, decision, "Omar", "2026-10-07", color=color)
                check(False, f"--color {color} with {decision} is refused ({want})")
            except Refused as e:
                check(want in str(e), f"--color {color} with {decision} is refused ({want})", str(e))
        recipe = plates / "minis-08.yaml"
        before = recipe.read_text(encoding="utf-8")
        recipe.write_text(before + "profile:\n  color: \"#FFFFFF\"\n", encoding="utf-8")
        try:
            yes_color(m8, "#0047BB")
            check(False, "--color on a recipe that fixes its color is refused")
        except Refused as e:
            check("fixes its colors" in str(e), "--color on a recipe that fixes its color is refused",
                  str(e))
        recipe.write_text(before, encoding="utf-8")

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
    for flag in ("approved", "held", "iterate", "sent", "status", "table", "self-test"):
        act.add_argument(f"--{flag}", action="store_true")
    ap.add_argument("--standing", action="store_true",
                    help="alone: write the standing row; with --sent: a standing send")
    ap.add_argument("--by", help="who decided, and how (\"Omar, tick\", \"Omar, in chat\")")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--via", default="`bambu print send`", help="with --sent: what sent it")
    ap.add_argument("--json", action="store_true", help="with --status: as JSON")
    ap.add_argument("--color", help="with --approved: the one color (#RRGGBB) the yes covers")
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
        if a.iterate:
            print(iterate(page, a.date))
            return 0
        if a.sent:
            print(sent(page, a.date, a.via, a.standing))
            return 0
        if a.approved or a.held or a.standing:
            decision = "approved" if a.approved else "held" if a.held else "standing"
            by = a.by if a.by is not None else (STANDING_BY if decision == "standing" else "")
            print(decide(page, decision, by, a.date, a.color))
            return 0
    except Refused as e:
        print(f"plate_approve: {page.stem}: {e}", file=sys.stderr)
        return 1
    ap.error("say what to record: --approved, --held, --iterate, --standing, --sent, --status "
             "or --table")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
