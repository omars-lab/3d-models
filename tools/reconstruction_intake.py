#!/usr/bin/env python3
"""Reconstruction intake: from a finished youtube rung to a ledger row here.

Design: docs/constructions/reconstruction-intake-design.md (call 1 took option (b),
decision D-122). youtube keeps one reconstructions/<id>/rung.yaml per rung; this
repo keeps one row per reconstruction in docs/constructions/ledger.md. This tool
is the step between them, and the one place that decides what "completed in
youtube" means here.

A rung is COMPLETED when, read from rung.yaml at youtube's tip ref (main):

  * work.status is `done`;
  * synced.score.verdict is PASS, or PARTIAL with work.accepted_partial written
    (youtube's own rule for `done`, repeated on purpose; call 3);
  * synced.score.fresh is true;
  * sha256 of construction.ggb-commands at the same ref, first 12 hex, equals
    both digests the rung records (ours: a synced half must not lag the
    construction beside it).

A completed rung is NOT YET IMPORTED when no ledger row names a `.bkr`, the row
is not "no piece by design", and no `src/Coasters/<id>*-standard.stl` is on
disk. A missing row counts as not imported.

Modes — read-only unless `--write` is given:

  --list      (default) every completed, not-yet-imported rung: id, score,
              "accepted partial" when that is why it counts, title, creator.
              This is the list import-construction's step 0 and
              prioritize-design's "collect the candidates" read.
  --session   the SessionStart lines (.claude/settings.json): the list in one
              line, and one line saying what `--write` would change. Prints
              nothing when nothing is owed; prints a "could not read" line when
              youtube is not checked out, so silence always means clean.
  --write     moves the ledger's youtube pin to youtube's tip, adds a stub row
              for every rung at the tip with no row (youtube cell from its
              rung.yaml status, every other cell `—`), refreshes the youtube
              cell of every row from its rung status, and updates the
              `constructions-total` count. Refuses on master/main: a write lands
              as a small PR from a worktree (call 2: the pin moves at every
              intake write and at every import PR). A second `--write` changes
              nothing.
  --self-test a scratch youtube repo and ledger; see `self_test`.

youtube is read at a ref, never its working tree, through the gate's own
helpers (`.claude/gates/constructions_ledger.py`: `read_rungs`, `youtube_tip`),
so there is one youtube reader for the hook, the gate and this tool.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "gates"))

from constructions_ledger import (  # noqa: E402
    LEDGER_REL,
    PIN_RE,
    Row,
    Rung,
    _git,
    check,
    parse_ledger,
    read_rungs,
    youtube_root,
    youtube_tip,
)

COUNT_RE = re.compile(r"(\d+)(\s*<!--count:constructions-total-->)")


# --- the completed test ---------------------------------------------------


def completed(rung: Rung) -> bool:
    """The four-part test from the design doc §2 (call 3: accepted PARTIAL counts)."""
    if rung.status != "done":
        return False
    if rung.verdict == "PASS":
        verdict_ok = True
    elif rung.verdict == "PARTIAL" and rung.accepted_partial:
        verdict_ok = True
    else:
        verdict_ok = False
    return verdict_ok and rung.fresh and rung.digest_ok


def has_coaster(cid: str, root: Path) -> bool:
    """A vendored `src/Coasters/<id>*-standard.stl` of any style (design doc §8)."""
    return any((root / "src" / "Coasters").glob(f"{cid}*-standard.stl"))


def imported(cid: str, rows: dict[str, Row], root: Path) -> bool:
    row = rows.get(cid)
    if row is not None and (row.migrated or row.by_design):
        return True
    return has_coaster(cid, root)


# --- reading both sides ----------------------------------------------------


@dataclass
class State:
    """Everything the modes need, read once."""

    yt: Path
    tip_ref: str
    tip: str
    pin: str | None
    behind: int | None
    rows: dict[str, Row]
    rungs: dict[str, Rung]
    ledger_text: str


def read_state(root: Path, ledger_path: Path, yt: Path) -> State | None:
    tip_ref = youtube_tip(yt)
    if tip_ref is None:
        return None
    tip = _git(yt, "rev-parse", f"{tip_ref}^{{commit}}").stdout.strip()
    pin, _date, row_list = parse_ledger(ledger_path)
    behind = None
    if pin:
        proc = _git(yt, "rev-list", "--count", f"{pin}..{tip}")
        behind = int(proc.stdout.strip()) if proc.returncode == 0 else None
    return State(
        yt=yt,
        tip_ref=tip_ref,
        tip=tip,
        pin=pin,
        behind=behind,
        rows={r.id: r for r in row_list},
        rungs=read_rungs(yt, tip_ref),
        ledger_text=ledger_path.read_text(encoding="utf-8"),
    )


def queue(state: State, root: Path) -> list[Rung]:
    """Completed at the tip and not yet imported here, by id."""
    return [
        r for cid, r in sorted(state.rungs.items())
        if completed(r) and not imported(cid, state.rows, root)
    ]


def mark(rung: Rung) -> str:
    return f"{rung.id} (accepted partial)" if rung.accepted_partial else rung.id


# --- the write plan --------------------------------------------------------


@dataclass
class Plan:
    pin_from: str | None
    pin_to: str
    behind: int | None
    new_rows: list[Rung] = field(default_factory=list)
    cell_fixes: list[tuple[Row, str]] = field(default_factory=list)  # (row, new status)

    @property
    def empty(self) -> bool:
        return not self.new_rows and not self.cell_fixes and self.pin_from == self.pin_to

    def summary(self) -> list[str]:
        out: list[str] = []
        if self.new_rows:
            out.append(f"add {len(self.new_rows)} ledger row(s): "
                       + ", ".join(r.id for r in self.new_rows))
        if self.cell_fixes:
            out.append(f"fix {len(self.cell_fixes)} youtube cell(s): "
                       + ", ".join(f"{row.id} {row.youtube}→{new}" for row, new in self.cell_fixes))
        if self.pin_from != self.pin_to:
            lag = f" ({self.behind} commits behind youtube main)" if self.behind else ""
            out.append(f"move the pin {(self.pin_from or 'none')[:7]}→{self.pin_to[:7]}{lag}")
        return out


def plan_write(state: State) -> Plan:
    plan = Plan(pin_from=state.pin, pin_to=state.tip, behind=state.behind)
    for cid, rung in sorted(state.rungs.items()):
        row = state.rows.get(cid)
        if row is None:
            plan.new_rows.append(rung)
        elif row.youtube != rung.status:
            plan.cell_fixes.append((row, rung.status))
    return plan


def _stub_row(rung: Rung) -> str:
    title = rung.title.replace("|", "/").strip() or rung.id
    if rung.creator:
        title = f"{title} ({rung.creator})"
    return f"| `{rung.id}` | {title} | {rung.status} | — | — | — | — | — | — | — |"


def _set_cell(line: str, index: int, value: str) -> str:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    cells[index] = value
    return "| " + " | ".join(cells) + " |"


def apply_write(plan: Plan, state: State, ledger_path: Path, today: str | None = None) -> None:
    """Rewrite the ledger in place: pin, cells, stub rows, count — nothing else."""
    today = today or _dt.date.today().isoformat()
    lines = state.ledger_text.split("\n")
    for row, new in plan.cell_fixes:
        lines[row.lineno - 1] = _set_cell(lines[row.lineno - 1], 2, new)
    if plan.new_rows:
        last = max(r.lineno for r in state.rows.values()) if state.rows else None
        if last is None:
            raise SystemExit("intake: the ledger has no table rows to append after")
        stubs = [_stub_row(r) for r in plan.new_rows]
        lines[last:last] = stubs
    text = "\n".join(lines)
    text = PIN_RE.sub(f"Youtube pin: `{plan.pin_to}` ({today})", text, count=1)
    total = len(state.rows) + len(plan.new_rows)
    text = COUNT_RE.sub(lambda m: f"{total}{m.group(2)}", text, count=1)
    ledger_path.write_text(text, encoding="utf-8")


def current_branch(root: Path) -> str | None:
    proc = subprocess.run(["git", "-C", str(root), "branch", "--show-current"],
                          capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else None


def write_refusal(root: Path) -> str | None:
    """Why `--write` will not run here, or None when it may (call 2: a write is a PR)."""
    branch = current_branch(root)
    if branch in ("master", "main"):
        return (f"intake: refusing to write on {branch} — the write lands as a PR from a worktree "
                f"(git worktree add ../3d-models-<name> -b <branch>)")
    return None


# --- the modes -------------------------------------------------------------


def list_lines(state: State, root: Path) -> list[str]:
    q = queue(state, root)
    out = []
    for r in q:
        why = " accepted partial" if r.accepted_partial else ""
        who = f" ({r.creator})" if r.creator else ""
        out.append(f"{r.id}  {r.score}{why}  {r.title}{who}")
    out.append(f"{len(q)} done in youtube, not yet imported here "
               f"(youtube {state.tip_ref.rsplit('/', 1)[-1]} {state.tip[:7]})")
    return out


def session_lines(root: Path = ROOT, ledger_path: Path | None = None,
                  yt: Path | None = None) -> list[str]:
    """The SessionStart lines. Empty when nothing is owed; never silent on a failure to read."""
    ledger_path = ledger_path or (root / LEDGER_REL)
    if not ledger_path.exists():
        return [f"intake: {LEDGER_REL} is missing — could not read the ledger"]
    yt = yt if yt is not None else youtube_root(root)
    if yt is None:
        return ["intake: youtube is not checked out — could not read its rungs"]
    state = read_state(root, ledger_path, yt)
    if state is None:
        return [f"intake: youtube at {yt} has no main/master tip ref — could not read its rungs"]
    out: list[str] = []
    q = queue(state, root)
    if q:
        out.append(f"{len(q)} done in youtube, not yet imported here: "
                   + ", ".join(mark(r) for r in q))
    plan = plan_write(state)
    if not plan.empty:
        out.append("intake --write would " + "; ".join(plan.summary())
                   + " — python3 tools/reconstruction_intake.py --write")
    return out


# --- self-test -------------------------------------------------------------


def self_test() -> int:
    import shutil
    import tempfile

    from constructions_ledger import scratch_git, write_rung

    failures = 0

    def ok(label: str, cond: bool, detail: str = "") -> None:
        nonlocal failures
        print(f"self-test {'ok  ' if cond else 'FAIL'}: {label}" + ("" if cond else f" — {detail}"))
        failures += 0 if cond else 1

    tmp = Path(tempfile.mkdtemp(prefix="reconstruction-intake-"))
    try:
        # youtube: the five rungs the design doc's item 2 names, plus a migrated
        # one, a by-design one and a coaster-only one; then a later commit that
        # adds one more completed rung with no row here (the bknVRSMcLj0 shape).
        yt = tmp / "youtube"
        yt.mkdir()
        git = scratch_git(yt)
        git("init", "-q", "-b", "main")
        git("config", "core.hooksPath", "/dev/null")
        write_rung(yt, "PASSPASSPAS", title="A fresh pass")
        write_rung(yt, "PARTIALACCE", verdict="PARTIAL", passed=6, scored=9,
                   accepted_partial="her compass hand", title="An accepted partial")
        write_rung(yt, "DONEBUTFAIL", verdict="FAIL", passed=2, scored=9)
        write_rung(yt, "STALEDIGEST", stale_digest=True, title="Changed after the score")
        write_rung(yt, "BLOCKEDRUNG", status="blocked", verdict="PARTIAL", passed=9, scored=13)
        write_rung(yt, "MIGRATEDROW", title="Already a naqsh file")
        write_rung(yt, "BYDESIGNROW", title="A mechanism video")
        write_rung(yt, "COASTERONLY", title="A coaster on disk, no row cell")
        git("add", "-A")
        git("commit", "-q", "-m", "seed")
        pin = git("rev-parse", "HEAD")
        write_rung(yt, "NEWATTHETIP", title="Landed after the pin | with a pipe", creator="Maker Two")
        git("add", "-A")
        git("commit", "-q", "-m", "add one more")
        tip = git("rev-parse", "HEAD")

        # this repo: a scratch root on `main` (the write guard), a ledger whose
        # pin is one commit behind, and the migrated row's .bkr in a scratch bikar.
        root = tmp / "3d-models"
        (root / "docs" / "constructions").mkdir(parents=True)
        (root / "src" / "Coasters").mkdir(parents=True)
        (root / "src" / "Coasters" / "COASTERONLY-minimal-coaster-standard.stl").write_bytes(b"")
        rgit = scratch_git(root)
        rgit("init", "-q", "-b", "main")
        rgit("config", "core.hooksPath", "/dev/null")
        bikar = tmp / "bikar"
        (bikar / "patterns" / "Constructions").mkdir(parents=True)
        (bikar / "patterns" / "Constructions" / "MIGRATEDROW.bkr").write_text("piece Coaster\n")
        os.environ["BIKAR_DIR"] = str(bikar)
        ledger = root / LEDGER_REL
        ledger.write_text(
            "# Constructions ledger\n\n"
            f"Youtube pin: `{pin}` (2026-09-17)\n\n"
            "Scope of the set (K2): **8 <!--count:constructions-total--> constructions**.\n\n"
            "| id | title | youtube | naqsh | O1 | O2 | O3 | coaster | catalog | printed |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| `PASSPASSPAS` | A fresh pass | done | — | — | — | — | — | — | — |\n"
            "| `PARTIALACCE` | An accepted partial | done | — | — | — | — | — | — | — |\n"
            "| `DONEBUTFAIL` | Done but FAIL | done | — | — | — | — | — | — | — |\n"
            "| `STALEDIGEST` | Changed after the score | done | — | — | — | — | — | — | — |\n"
            "| `BLOCKEDRUNG` | Blocked, row says done | done | — | — | — | — | — | — | — |\n"
            "| `MIGRATEDROW` | Already a naqsh file | done | `bikar/patterns/Constructions/MIGRATEDROW.bkr` | — | — | — | — | — | — |\n"
            "| `BYDESIGNROW` | A mechanism video | done | no piece by design | — | — | — | no piece by design | — | — |\n"
            "| `COASTERONLY` | A coaster on disk | done | — | — | — | — | — | — | — |\n"
            "\n## Oracle notes\n",
            encoding="utf-8",
        )

        state = read_state(root, ledger, yt)
        assert state is not None
        ids = [r.id for r in queue(state, root)]
        # Item 2: of the five, only the fresh PASS and the accepted PARTIAL come back.
        # Item 3: the migrated row and the by-design row are absent; §8: so is the
        # coaster-only id. The rung added after the pin, with no row, is owed.
        ok("list = the fresh PASS, the accepted PARTIAL, and the new rung with no row",
           ids == ["NEWATTHETIP", "PARTIALACCE", "PASSPASSPAS"], str(ids))
        ok("done with a FAIL verdict is left out", "DONEBUTFAIL" not in ids)
        ok("done + PASS + changed construction (stale digest, the hard case) is left out",
           "STALEDIGEST" not in ids)
        ok("blocked is left out", "BLOCKEDRUNG" not in ids)
        ok("migrated, by-design and coaster-on-disk are left out",
           not {"MIGRATEDROW", "BYDESIGNROW", "COASTERONLY"} & set(ids))
        shown = "\n".join(list_lines(state, root))
        ok("the accepted PARTIAL is marked accepted partial, with its score",
           "PARTIALACCE  PARTIAL 6/9 accepted partial" in shown, shown)

        # Session lines name the queue and what --write would change.
        lines = session_lines(root, ledger, yt)
        ok("session names the queue with the accepted partial marked",
           any("3 done in youtube, not yet imported here: NEWATTHETIP, PARTIALACCE (accepted partial), PASSPASSPAS" == l
               for l in lines), str(lines))
        ok("session says what --write would do",
           any("add 1 ledger row(s): NEWATTHETIP" in l and "fix 1 youtube cell(s): BLOCKEDRUNG done→blocked" in l
               and "move the pin" in l for l in lines), str(lines))

        # Item 6: before --write the gate fails L3 (a row owed) and L4 (done over
        # blocked); after it, the gate passes; a second --write changes nothing.
        before, _, _ = check(root=root, ledger_path=ledger, yt=yt)
        ok("gate fails before --write (row owed, done over blocked)",
           len(before) == 2 and any("L3" in f for f in before) and any("L4" in f for f in before),
           str(before))
        plan = plan_write(state)
        apply_write(plan, state, ledger, today="2026-11-03")
        after, _, _ = check(root=root, ledger_path=ledger, yt=yt)
        ok("gate passes after --write", after == [], str(after))
        text = ledger.read_text(encoding="utf-8")
        ok("the pin moved to the tip", f"Youtube pin: `{tip}` (2026-11-03)" in text)
        ok("the stub row carries its title, creator and rung status, pipe replaced",
           "| `NEWATTHETIP` | Landed after the pin / with a pipe (Maker Two) | done | — | — | — | — | — | — | — |" in text,
           text)
        ok("the count moved to 9", "**9 <!--count:constructions-total--> constructions**" in text)
        ok("the stub row sits inside the table, before the notes",
           text.index("NEWATTHETIP") < text.index("## Oracle notes"))
        state2 = read_state(root, ledger, yt)
        assert state2 is not None
        plan2 = plan_write(state2)
        apply_write(plan2, state2, ledger, today="2026-11-03")
        ok("a second --write changes nothing", plan2.empty and ledger.read_text(encoding="utf-8") == text)

        # Item 4: session mode prints nothing when nothing is owed, and writes no
        # file. Nothing owed = pin at tip, every rung with a row, every completed
        # rung imported: give the three queued ones a .bkr each.
        for cid in ("PASSPASSPAS", "PARTIALACCE", "NEWATTHETIP"):
            (bikar / "patterns" / "Constructions" / f"{cid}.bkr").write_text("piece Coaster\n")
        quiet = re.sub(
            r"^(\| `(PASSPASSPAS|PARTIALACCE|NEWATTHETIP)` \| [^|]+ \| done \| )—",
            lambda m: m.group(1) + f"`bikar/patterns/Constructions/{m.group(2)}.bkr`",
            text, flags=re.M,
        )
        ledger.write_text(quiet, encoding="utf-8")
        stat = ledger.stat()
        lines = session_lines(root, ledger, yt)
        ok("session prints nothing when nothing is owed", lines == [], str(lines))
        ok("session wrote no file", ledger.stat() == stat and ledger.read_text(encoding="utf-8") == quiet)
        gate_quiet, _, _ = check(root=root, ledger_path=ledger, yt=yt)
        ok("the quiet ledger passes the gate", gate_quiet == [], str(gate_quiet))

        # The write guard: on main the write is refused; on a branch it goes.
        ok("write refuses on main", (write_refusal(root) or "").startswith("intake: refusing to write on main"))
        rgit("switch", "-q", "-c", "intake-test")
        ok("write allowed on a branch", write_refusal(root) is None, str(write_refusal(root)))

        # youtube absent: session says it could not read, never silence.
        os.environ["YOUTUBE_DIR"] = str(tmp / "no-such-youtube")
        try:
            lines = session_lines(root, ledger, None)
            ok("youtube absent -> a could-not-read line", lines == ["intake: youtube is not checked out — could not read its rungs"], str(lines))
        finally:
            del os.environ["YOUTUBE_DIR"]
    finally:
        os.environ.pop("BIKAR_DIR", None)
        shutil.rmtree(tmp, ignore_errors=True)

    print("self-test:", "PASS" if failures == 0 else f"FAIL ({failures})")
    return 1 if failures else 0


# --- main ------------------------------------------------------------------


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true", help="the completed, not-yet-imported rungs (default)")
    mode.add_argument("--session", action="store_true", help="the SessionStart lines; silent when nothing is owed")
    mode.add_argument("--write", action="store_true", help="stub rows, youtube cells, the pin and the count, in the ledger")
    mode.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.session:
        for line in session_lines():
            print(line)
        return 0

    ledger_path = ROOT / LEDGER_REL
    yt = youtube_root(ROOT)
    if yt is None:
        print("intake: youtube is not checked out (set YOUTUBE_DIR or clone it beside this repo)", file=sys.stderr)
        return 2
    state = read_state(ROOT, ledger_path, yt)
    if state is None:
        print(f"intake: youtube at {yt} has no main/master tip ref", file=sys.stderr)
        return 2

    if args.write:
        refusal = write_refusal(ROOT)
        if refusal:
            print(refusal, file=sys.stderr)
            return 2
        plan = plan_write(state)
        if plan.empty:
            print("intake: nothing to write — the pin is at youtube's tip, every rung has a row, "
                  "every youtube cell matches its rung")
            return 0
        apply_write(plan, state, ledger_path)
        for line in plan.summary():
            print(f"intake wrote: {line}")
        print(f"intake: {LEDGER_REL} updated — commit it with the use-case map re-pinned "
              f"(python3 .claude/skills/maintain-use-cases/validate.py --refresh)")
        return 0

    for line in list_lines(state, ROOT):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
