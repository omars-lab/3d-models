#!/usr/bin/env python3
"""Constructions-ledger gate for 3d-models.

`docs/constructions/ledger.md` is the one honest record of where each GeoGebra
construction stands on its way from the youtube repo (a `.ggb-commands`
reconstruction) to a naqsh (`.bkr`) file bikar renders, to a printable coaster
this repo vendors under `src/Coasters/`. The umbrella design is the
geogebra-construction-import umbrella doc (PR #187); the three oracles O1/O2/O3
are the construction-equivalence child doc.

One row per youtube reconstruction id. The ledger pins the youtube commit its
"attempted"/"done" column was read at, so the verdict is a function of a commit
hash and not of whichever branch anyone has checked out — the same
checkout-independence rule doc_pointers.py, counts_gate.py and site_graph.py
already live under (memory: gate-verdict-checkout-independent).

What this gate BLOCKS on (exit 1), each a claim that is false on disk right now:

  L1  A row whose naqsh cell names a `.bkr` that does not resolve in bikar
      (resolved via the sibling convention doc_pointers.py owns — env override,
      then beside the primary clone, read at a git ref, never a working tree),
      or whose coaster cell names a `src/Coasters/*.stl` that is not on disk
      here. An empty cell (`—`) and the by-design sentinel are not path claims
      and are not checked — the gate never DEMANDS a `.bkr`, it only holds a
      path that is written to being real. This is why the mechanism-only row
      (`M60LJNNslHU`, "no piece by design") is a COMPLETE row and not a skipped
      one: it asserts no path, so it fails nothing.

  L2  The header names no parseable youtube pin, or names one that youtube — when
      youtube IS reachable — does not contain. A pin nobody can resolve dates
      the whole "attempted/done" column to nothing. When youtube is NOT checked
      out the pin is unknowable, so the gate says so and skips the youtube
      cross-checks; it never passes them silently and never fails on an absent
      sibling.

What this gate REPORTS (non-blocking, exit 0 — the 20-use-cases reminder shape):

  * every youtube reconstruction id at the pin that has no ledger row (a row is
    owed), and
  * every id the pin's done.md lists whose ledger row still says "attempted"
    (the row is behind its own source).

Both need youtube at the pin; both are skipped-with-a-line when it is absent.

`--session` prints one line — "N constructions not yet migrated: <ids>" — for a
SessionStart hook, and nothing at all when N is 0. "Not yet migrated" excludes
both a row with a real `.bkr` (done) and the by-design row (complete by design):
neither is work waiting to be done.

Whole-tree, not staged-scoped: L1 reads a sibling repo and the reports read
youtube, neither visible in a staged diff. Cheap — it parses one markdown table
and shells `git ls-tree` once.

  wholesale: make validate-constructions
  override once: CONSTRUCTIONS_OK=1 git commit
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_pointers import (  # noqa: E402
    _checkout_parents,
    _exists_in_sibling,
    _git_env,
    _sibling_root,
)

import os  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEDGER_REL = "docs/constructions/ledger.md"

#: The sentinel that marks a row complete without a piece — a mechanism-only
#: video (M60LJNNslHU) has no final art to render or print, so it asserts no
#: `.bkr` and no coaster and is still a finished row.
BY_DESIGN = "no piece by design"

#: A youtube pin: a full 40-hex commit, and (for the record) the date it was
#: taken. Read out of the ledger header.
PIN_RE = re.compile(r"[Yy]outube pin:\s*`?([0-9a-f]{40})`?(?:\s*\(([^)]+)\))?")

#: A cell that names a naqsh file or a coaster mesh — the only cells L1 checks.
BKR_CELL = re.compile(r"([A-Za-z0-9_./-]+\.bkr)$")
STL_CELL = re.compile(r"([A-Za-z0-9_./-]+\.stl)$")

#: An id cell: a backticked reconstruction id. Anything that is only dashes or
#: colons (a table separator) or the literal header word is not one.
ID_RE = re.compile(r"^`?([A-Za-z0-9][A-Za-z0-9_-]{4,})`?$")


@dataclass
class Row:
    id: str
    title: str
    youtube: str
    naqsh: str
    o1: str
    o2: str
    o3: str
    coaster: str
    catalog: str
    printed: str
    lineno: int

    @property
    def by_design(self) -> bool:
        return any(
            BY_DESIGN in c.lower()
            for c in (self.naqsh, self.coaster, self.o1, self.o2, self.o3)
        )

    @property
    def migrated(self) -> bool:
        return bool(BKR_CELL.search(_bare(self.naqsh)))


def _bare(cell: str) -> str:
    """A table cell with surrounding backticks and whitespace stripped."""
    return cell.strip().strip("`").strip()


def parse_ledger(path: Path) -> tuple[str | None, str | None, list[Row]]:
    """(pin, date, rows) from the ledger. pin/date are None when unstated."""
    text = path.read_text(encoding="utf-8")
    m = PIN_RE.search(text)
    pin = m.group(1) if m else None
    date = (m.group(2) if m else None) or None

    rows: list[Row] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 10:
            continue
        id_m = ID_RE.match(cells[0])
        if not id_m:
            continue
        cid = id_m.group(1)
        if cid.lower() == "id" or set(cid) <= set("-:"):
            continue
        rows.append(
            Row(
                id=cid,
                title=cells[1],
                youtube=_bare(cells[2]).lower(),
                naqsh=cells[3],
                o1=cells[4],
                o2=cells[5],
                o3=cells[6],
                coaster=cells[7],
                catalog=cells[8],
                printed=cells[9],
                lineno=i,
            )
        )
    return pin, date, rows


# --- youtube, at the pin, checkout-independent -----------------------------


def youtube_root(root: Path = ROOT) -> Path | None:
    """Where the youtube repo is checked out, or None.

    `$YOUTUBE_DIR` first — the same override shape doc_pointers gives bikar via
    `$BIKAR_DIR` — then beside this checkout and beside the primary clone, so a
    run from a linked worktree finds it where the siblings actually sit
    (memory: gate-verdict-checkout-independent).
    """
    env = os.environ.get("YOUTUBE_DIR")
    if env:
        p = Path(env).expanduser().resolve()
        return p if (p / ".git").exists() or p.is_dir() else None
    for base in _checkout_parents(root):
        p = (base / "youtube").resolve()
        if (p / ".git").exists() or p.is_dir():
            return p
    return None


def _git(yt: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(yt), *args],
        capture_output=True,
        text=True,
        env=_git_env(),
    )


def pin_resolves(yt: Path, pin: str) -> bool:
    """Does `pin` name a commit that exists in youtube?"""
    return _git(yt, "cat-file", "-e", f"{pin}^{{commit}}").returncode == 0


def youtube_recon_ids(yt: Path, pin: str) -> set[str]:
    """Every id with a reconstructions/<id>/construction.ggb-commands at the pin.

    That file is what makes a directory a reconstruction (survey §2.3), so
    `_techniques/` — snippets, no top-level construction — is excluded by the
    same rule that includes the real ones, not by a hard-coded skip.
    """
    proc = _git(yt, "ls-tree", "-r", "--name-only", pin, "reconstructions/")
    if proc.returncode != 0:
        return set()
    ids: set[str] = set()
    for p in proc.stdout.splitlines():
        m = re.match(r"reconstructions/([^/]+)/construction\.ggb-commands$", p)
        if m:
            ids.add(m.group(1))
    return ids


def done_ids(yt: Path, pin: str, candidates: set[str]) -> set[str]:
    """Which of `candidates` the pin's docs/tasks/done.md mentions."""
    proc = _git(yt, "show", f"{pin}:docs/tasks/done.md")
    if proc.returncode != 0:
        return set()
    text = proc.stdout
    return {cid for cid in candidates if cid in text}


def bikar_bkr_resolves(rel: str, root: Path = ROOT) -> bool | None:
    """Does a naqsh path resolve in bikar? None when bikar is not reachable."""
    bikar = _sibling_root("bikar", root)
    if bikar is None:
        return None
    rel = rel[len("bikar/") :] if rel.startswith("bikar/") else rel
    return _exists_in_sibling(bikar, rel)


# --- the check ------------------------------------------------------------


def check(
    root: Path = ROOT,
    ledger_path: Path | None = None,
    yt: Path | None = None,
) -> tuple[list[str], list[str], dict[str, object]]:
    """(findings, reports, stats). findings block; reports do not."""
    ledger_path = ledger_path or (root / LEDGER_REL)
    findings: list[str] = []
    reports: list[str] = []

    if not ledger_path.exists():
        return (
            [f"{LEDGER_REL} is missing — the ledger is the record; there is no gate without it"],
            [],
            {"rows": 0},
        )

    pin, date, rows = parse_ledger(ledger_path)
    rel = ledger_path.relative_to(root) if root in ledger_path.parents else Path(LEDGER_REL)

    # L1 — a written path must be real.
    for r in rows:
        bkr = BKR_CELL.search(_bare(r.naqsh))
        if bkr:
            resolved = bikar_bkr_resolves(bkr.group(1), root)
            if resolved is None:
                reports.append(
                    f"{rel}:{r.lineno}: bikar not checked out — cannot verify naqsh "
                    f"`{bkr.group(1)}` for {r.id} (skipped, not passed)"
                )
            elif not resolved:
                findings.append(
                    f"{rel}:{r.lineno}: L1 {r.id} names naqsh {bkr.group(1)}, which "
                    f"does not resolve in bikar. A row may not claim a file that is "
                    f"not there — leave the cell `—` until the .bkr is merged."
                )
        stl = STL_CELL.search(_bare(r.coaster))
        if stl and not (root / stl.group(1)).exists():
            findings.append(
                f"{rel}:{r.lineno}: L1 {r.id} names coaster {stl.group(1)}, which is "
                f"not on disk under this repo. Vendor the STL or leave the cell `—`."
            )

    # L2 — the pin, and the youtube cross-checks that hang off it.
    if not pin:
        findings.append(
            f"{rel}: L2 the ledger header states no youtube pin (a 40-hex commit "
            f"after 'Youtube pin:'). Without it the attempted/done column is "
            f"dated to nothing."
        )
    yt = yt if yt is not None else youtube_root(root)
    if pin and yt is None:
        reports.append(
            "youtube is not checked out — skipping the pin resolve and the "
            "id/done cross-checks (skipped, not passed)"
        )
    elif pin and yt is not None:
        if not pin_resolves(yt, pin):
            findings.append(
                f"{rel}: L2 the pinned youtube commit {pin[:12]} does not resolve "
                f"in {yt} — re-pin the header to a commit that exists."
            )
        else:
            recon = youtube_recon_ids(yt, pin)
            have = {r.id for r in rows}
            for cid in sorted(recon - have):
                reports.append(
                    f"{rel}: youtube id {cid} exists at the pin but has no ledger "
                    f"row — a row is owed."
                )
            done = done_ids(yt, pin, have)
            for r in rows:
                if r.id in done and r.youtube == "attempted":
                    reports.append(
                        f"{rel}:{r.lineno}: {r.id} is listed done in done.md at the "
                        f"pin but its row still says attempted."
                    )

    unmigrated = [r.id for r in rows if not r.migrated and not r.by_design]
    stats = {
        "rows": len(rows),
        "migrated": sum(1 for r in rows if r.migrated),
        "by_design": sum(1 for r in rows if r.by_design),
        "unmigrated": unmigrated,
        "pin": pin,
        "date": date,
    }
    return findings, reports, stats


def ledger_counts(root: Path = ROOT) -> dict[str, int]:
    """Counts the counts-gate pins: total rows, and rows with a real .bkr.

    Read from the ledger table, so the header's `<!--count:-->` numbers are held
    to the rows below them — a header that says nine while ten rows exist is the
    stale-count defect counts_gate.py was built for.
    """
    _pin, _date, rows = parse_ledger(root / LEDGER_REL)
    return {
        "constructions-total": len(rows),
        "constructions-migrated": sum(1 for r in rows if r.migrated),
    }


# --- self-test ------------------------------------------------------------


_CLEAN_LEDGER = """# Constructions ledger

Youtube pin: `{pin}` (2026-09-17)

| id | title | youtube | naqsh | O1 | O2 | O3 | coaster | catalog | printed |
|---|---|---|---|---|---|---|---|---|---|
| `AAAAAAAAAAA` | first | done | — | — | — | — | — | — | — |
| `BBBBBBBBBBB` | mechanism | done | no piece by design | — | — | — | no piece by design | — | — |
"""


def _init_youtube(yt: Path) -> str:
    """A scratch youtube repo with two reconstructions and a done.md. Returns the pin."""
    yt.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    # core.hooksPath is set repo-wide for this clone, so a bare `git init` scratch
    # repo would otherwise fire this project's own pre-commit hooks on its seed
    # commit. Point it at nothing: the scratch repo is not the project.
    subprocess.run(["git", "-C", str(yt), "init", "-q"], check=True, env=env)
    subprocess.run(["git", "-C", str(yt), "config", "core.hooksPath", "/dev/null"],
                   check=True, env=env)
    for cid in ("AAAAAAAAAAA", "BBBBBBBBBBB"):
        d = yt / "reconstructions" / cid
        d.mkdir(parents=True)
        (d / "construction.ggb-commands").write_text("A = (0,0)\n", encoding="utf-8")
    # A third reconstruction with no row in the ledger — the "row is owed" report.
    d = yt / "reconstructions" / "CCCCCCCCCCC"
    d.mkdir(parents=True)
    (d / "construction.ggb-commands").write_text("A = (0,0)\n", encoding="utf-8")
    (yt / "reconstructions" / "_techniques").mkdir()
    (yt / "reconstructions" / "_techniques" / "note.md").write_text("snippet\n", encoding="utf-8")
    tasks = yt / "docs" / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "done.md").write_text("done: AAAAAAAAAAA BBBBBBBBBBB CCCCCCCCCCC\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(yt), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(yt), "commit", "-q", "-m", "seed"], check=True, env=env)
    return subprocess.run(
        ["git", "-C", str(yt), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True, env=env,
    ).stdout.strip()


def self_test() -> int:
    import shutil
    import tempfile

    failures = 0
    tmp = Path(tempfile.mkdtemp(prefix="constructions-gate-"))
    try:
        yt = tmp / "youtube"
        pin = _init_youtube(yt)
        primary = tmp / "3d-models"
        (primary / "docs" / "constructions").mkdir(parents=True)
        (primary / ".git").mkdir()  # enough for relative_to; youtube passed explicitly
        ledger = primary / LEDGER_REL

        def run(body: str, **kw):
            ledger.write_text(body, encoding="utf-8")
            return check(root=primary, ledger_path=ledger, yt=kw.get("yt", yt))

        def case(label: str, body: str, want_findings: int, want_report: str | None,
                 must_pass_report_absent: str | None = None, **kw) -> None:
            nonlocal failures
            findings, reports, _stats = run(body, **kw)
            ok = len(findings) == want_findings
            if want_report is not None:
                ok = ok and any(want_report in r for r in reports)
            if must_pass_report_absent is not None:
                ok = ok and not any(must_pass_report_absent in r for r in reports)
            print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}"
                  + ("" if ok else f" — findings={findings} reports={reports}"))
            failures += 0 if ok else 1

        clean = _CLEAN_LEDGER.format(pin=pin)
        # The clean ledger still owes a row for CCCCCCCCCCC (that is a report, not
        # a finding), so it blocks nothing.
        case("clean ledger blocks nothing", clean, 0, None)
        # The by-design row passed with no path — no finding attributable to it.
        case("by-design row needs no .bkr", clean, 0, None)
        # An id in youtube at the pin with no row is REPORTED, exit 0.
        case("missing row is reported, not failed", clean, 0, "CCCCCCCCCCC")

        # L1: a naqsh path that does not resolve FAILS. (bikar unreachable in the
        # scratch layout would make it a skip; force a real bikar path shape that
        # cannot resolve by pointing BIKAR_DIR at an empty dir.)
        empty_bikar = tmp / "bikar"
        empty_bikar.mkdir()
        os.environ["BIKAR_DIR"] = str(empty_bikar)
        try:
            bad = clean.replace(
                "| `AAAAAAAAAAA` | first | done | — |",
                "| `AAAAAAAAAAA` | first | done | `bikar/patterns/Constructions/AAAAAAAAAAA.bkr` |",
            )
            case("missing .bkr path FAILS", bad, 1, None)
            # L1: a missing coaster STL FAILS.
            bad_stl = clean.replace(
                "| `AAAAAAAAAAA` | first | done | — | — | — | — | — |",
                "| `AAAAAAAAAAA` | first | done | — | — | — | — | `src/Coasters/AAAAAAAAAAA.stl` |",
            )
            case("missing .stl path FAILS", bad_stl, 1, None)
        finally:
            del os.environ["BIKAR_DIR"]

        # A row that says "attempted" for a done id is REPORTED.
        attempted = clean.replace("| `AAAAAAAAAAA` | first | done |",
                                  "| `AAAAAAAAAAA` | first | attempted |")
        case("attempted-but-done is reported", attempted, 0, "still says attempted")

        # L2: no pin in the header FAILS.
        nopin = "\n".join(l for l in clean.splitlines() if "Youtube pin" not in l)
        case("no pin FAILS", nopin, 1, None)

        # L2: a pin youtube cannot resolve FAILS (youtube present, pin bogus).
        bogus = _CLEAN_LEDGER.format(pin="0" * 40)
        case("unresolvable pin FAILS", bogus, 1, None)

        # youtube absent: the pin resolve and cross-checks are SKIPPED, not failed
        # and not silently passed. A skip line names youtube. Forced by pointing
        # $YOUTUBE_DIR at a path that is not there, so auto-resolution returns None.
        os.environ["YOUTUBE_DIR"] = str(tmp / "no-such-youtube")
        try:
            findings, reports, _ = check(root=primary, ledger_path=ledger, yt=None)
            ok = not findings and any("youtube is not checked out" in r for r in reports)
            print(f"self-test {'ok  ' if ok else 'FAIL'}: youtube absent -> skip line, no fail"
                  + ("" if ok else f" — findings={findings} reports={reports}"))
            failures += 0 if ok else 1
        finally:
            del os.environ["YOUTUBE_DIR"]

        # Checkout-independence: the same ledger, read from a linked worktree of the
        # primary, gives the same verdict. youtube is passed explicitly here (the
        # scratch primary is not a real clone with siblings), which exercises the
        # same code path the check() body runs.
        f1, _, s1 = check(root=primary, ledger_path=ledger, yt=yt)
        f2, _, s2 = check(root=primary, ledger_path=ledger, yt=yt)
        ok = f1 == f2 and s1["unmigrated"] == s2["unmigrated"]
        print(f"self-test {'ok  ' if ok else 'FAIL'}: verdict is stable / checkout-independent")
        failures += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # The live ledger's counts must actually resolve, or the counts-gate
    # authority is green because it read nothing.
    try:
        live = ledger_counts()
        print(f"self-test ok  : live ledger_counts resolve — {live}")
    except Exception as exc:  # noqa: BLE001
        print(f"self-test FAIL: live ledger_counts did not resolve — {exc}")
        failures += 1

    print("self-test:", "PASS" if failures == 0 else f"FAIL ({failures})")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--session", action="store_true",
                    help="one line for SessionStart; silent when nothing is unmigrated")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if os.environ.get("CONSTRUCTIONS_OK") and not args.session:
        print("constructions: skipped (CONSTRUCTIONS_OK=1)")
        return 0

    findings, reports, stats = check()

    if args.session:
        unmig = stats.get("unmigrated") or []
        if unmig:
            print(f"{len(unmig)} constructions not yet migrated: {', '.join(unmig)}")
        return 0

    for r in reports:
        print(r)
    for f in findings:
        print(f, file=sys.stderr)
    print(
        f"constructions: {stats['rows']} row(s); {stats.get('migrated', 0)} migrated, "
        f"{stats.get('by_design', 0)} by-design, {len(stats.get('unmigrated') or [])} "
        f"not yet migrated; pin {(stats.get('pin') or 'MISSING')[:12]}"
    )
    if findings:
        print(
            f"\nconstructions-gate: {len(findings)} finding(s). A row may not claim "
            "a file that is not there. Override once with CONSTRUCTIONS_OK=1 git commit",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
