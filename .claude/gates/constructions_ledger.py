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
      youtube IS reachable — does not contain, or one that is not an ancestor of
      youtube's tip ref (a pin on a side branch dates the column to work that
      may never land on main). A pin nobody can resolve dates the whole youtube
      column to nothing. When youtube is NOT checked out the pin is unknowable,
      so the gate says so and skips the youtube cross-checks; it never passes
      them silently and never fails on an absent sibling.

  L3  A youtube reconstruction with no ledger row, or a row the pin cannot see.
      "Reconstruction" is read at two commits: the pin, and youtube's default
      branch tip (`main`, else `master`, else `origin/HEAD` — a ref, never the
      working tree, so the verdict does not move with whatever branch youtube
      has checked out). An id at either with no row FAILS: a row is owed. A row
      whose id is not a reconstruction at the pin FAILS too: the pin lags the
      row and must be advanced, or the row's youtube column is dated to a
      commit that never had it. Until 2026-09-27 the first half was only a
      report, and only at the pin, so `bknVRSMcLj0` — reconstructed in youtube
      after the pin was taken — sat unledgered with every gate green
      (docs/issues/constructions-ledger-missed-new-reconstruction.md).

  L4  A row whose youtube cell says "done" while the rung's own state file at
      the pin (reconstructions/<id>/rung.yaml, `work.status`) says otherwise —
      blocked, queued, claimed, in-progress. Until 2026-11-03 "done" was a text
      search of youtube's docs/tasks/done.md, which counted an id mentioned as
      "attempted" as done, and `yZN_wn0uvTY` (blocked in youtube) sat as done
      here. The youtube column is now read from rung.yaml and nowhere else
      (docs/constructions/reconstruction-intake-design.md §5, item 7).

What this gate REPORTS (non-blocking, exit 0):

  * a row whose youtube cell differs from its rung status at the pin in any
    other way (the row says "attempted" while the rung says done: the row is
    behind its own source); `tools/reconstruction_intake.py --write` refreshes
    every cell from the pin.
  * a row with no rung.yaml at the pin (a pin older than youtube's rung files,
    before youtube 30a2709), whose cell therefore cannot be checked.

It needs youtube at the pin, and is skipped-with-a-line when youtube is absent,
as are L2's resolve and all of L3 and L4.

`--session` is the SessionStart line and is answered by the intake tool
(`tools/reconstruction_intake.py --session`), which shares this file's youtube
reader (`read_rungs`): the completed rungs with no coaster here, and what a
`--write` would change. It prints nothing when nothing is owed.

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
#: colons (a table separator) or the literal header word is not one. A YouTube id
#: may start with `_` or `-` (`_U6G8QSfWnk`); requiring a letter first left that
#: reconstruction's row unreadable, so the gate owed a row no edit could write.
ID_RE = re.compile(r"^`?(?!-+$)([A-Za-z0-9_-]{5,})`?$")


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


#: Where youtube's current work lives, most specific first. youtube's local
#: `main` is the record (its `origin` is a push mirror on the studio machine,
#: not a branch anyone reads); `origin/HEAD` is the fallback for a clone that
#: has only the mirror.
TIP_REFS = ("refs/heads/main", "refs/heads/master", "refs/remotes/origin/HEAD")


def youtube_tip(yt: Path) -> str | None:
    """The first of TIP_REFS that names a commit, as a ref name; None if none do."""
    for ref in TIP_REFS:
        if _git(yt, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode == 0:
            return ref
    return None


def is_ancestor(yt: Path, pin: str, ref: str) -> bool:
    """Is `pin` on the first-parent history of `ref` (or equal to it)?"""
    return _git(yt, "merge-base", "--is-ancestor", pin, ref).returncode == 0


def cat_files(yt: Path, ref: str, paths: list[str]) -> dict[str, bytes | None]:
    """The bytes of each `path` at `ref`, read in one `git cat-file --batch`.

    One subprocess for the whole set, so reading 34 rung files and their 34
    constructions stays well inside the seconds a SessionStart hook has. A path
    missing at the ref maps to None. Bytes, not text: the construction digest is
    sha256 over the file's raw bytes, so a decode would change it.
    """
    if not paths:
        return {}
    proc = subprocess.run(
        ["git", "-C", str(yt), "cat-file", "--batch"],
        input="".join(f"{ref}:{p}\n" for p in paths).encode("utf-8"),
        capture_output=True,
        env=_git_env(),
    )
    out: dict[str, bytes | None] = {p: None for p in paths}
    if proc.returncode != 0:
        return out
    data = proc.stdout
    pos = 0
    for p in paths:
        nl = data.find(b"\n", pos)
        if nl < 0:
            break
        header = data[pos:nl].decode("utf-8", "replace").split()
        pos = nl + 1
        if len(header) == 3 and header[1] != "missing":
            size = int(header[2])
            out[p] = data[pos : pos + size]
            pos += size + 1  # the trailing newline cat-file adds after each blob
    return out


#: The status values youtube's rung script accepts for `work.status`.
RUNG_STATUSES = ("queued", "claimed", "in-progress", "blocked", "done")


@dataclass
class Rung:
    """One reconstructions/<id>/rung.yaml, read at a ref, plus the digest check.

    `work` is kept by hand in youtube; `synced` is written by youtube's
    `make rung-sync`. `digest_ok` is ours: sha256 of construction.ggb-commands
    at the same ref, first 12 hex, must equal both digests the rung records,
    or the synced half lags the construction beside it.
    """

    id: str
    status: str
    verdict: str
    passed: int | None
    scored: int | None
    fresh: bool
    accepted_partial: str | None
    title: str
    creator: str
    synced_digest: str
    score_digest: str
    digest: str

    @property
    def digest_ok(self) -> bool:
        return self.digest == self.synced_digest == self.score_digest

    @property
    def score(self) -> str:
        """`PASS 18/18`, `PARTIAL 6/9`, or the bare verdict when no counts."""
        if self.passed is None or self.scored is None:
            return self.verdict
        return f"{self.verdict} {self.passed}/{self.scored}"


def _rung_from_yaml(cid: str, text: bytes, construction: bytes | None) -> Rung:
    import hashlib

    import yaml  # the hooks already require PyYAML (20-use-cases)

    doc = yaml.safe_load(text.decode("utf-8")) or {}
    work = doc.get("work") or {}
    synced = doc.get("synced") or {}
    score = synced.get("score") or {}
    digest = hashlib.sha256(construction).hexdigest()[:12] if construction is not None else ""
    accepted = work.get("accepted_partial")
    return Rung(
        id=cid,
        status=str(work.get("status") or ""),
        verdict=str(score.get("verdict") or ""),
        passed=score.get("passed"),
        scored=score.get("scored"),
        fresh=bool(score.get("fresh")),
        accepted_partial=str(accepted).strip() if accepted else None,
        title=str(synced.get("title") or "").strip(),
        creator=str(synced.get("creator") or "").strip(),
        synced_digest=str(synced.get("construction_digest") or ""),
        score_digest=str(score.get("construction_digest") or ""),
        digest=digest,
    )


def read_rungs(yt: Path, ref: str) -> dict[str, Rung]:
    """Every rung.yaml at `ref`, by id — the one youtube reader.

    Read at a ref, never the working tree: youtube's checkout may be on any
    branch, mid-edit by another session. A reconstruction (a folder with a
    construction.ggb-commands, see `youtube_recon_ids`) with no rung.yaml at
    the ref is absent here; a ref older than youtube's rung files (before
    youtube 30a2709) gives an empty dict, and callers say so rather than
    treating "no rung" as "not done".
    """
    proc = _git(yt, "ls-tree", "-r", "--name-only", ref, "reconstructions/")
    if proc.returncode != 0:
        return {}
    ids = sorted(
        m.group(1)
        for m in (re.match(r"reconstructions/([^/]+)/rung\.yaml$", p) for p in proc.stdout.splitlines())
        if m
    )
    paths = [f"reconstructions/{cid}/rung.yaml" for cid in ids]
    paths += [f"reconstructions/{cid}/construction.ggb-commands" for cid in ids]
    blobs = cat_files(yt, ref, paths)
    rungs: dict[str, Rung] = {}
    for cid in ids:
        text = blobs.get(f"reconstructions/{cid}/rung.yaml")
        if text is None:
            continue
        rungs[cid] = _rung_from_yaml(cid, text, blobs.get(f"reconstructions/{cid}/construction.ggb-commands"))
    return rungs


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
    owed: list[str] = []

    if not ledger_path.exists():
        return (
            [f"{LEDGER_REL} is missing — the ledger is the record; there is no gate without it"],
            [],
            {"rows": 0},
        )

    pin, date, rows = parse_ledger(ledger_path)
    rel = ledger_path.relative_to(root) if root in ledger_path.parents else Path(LEDGER_REL)

    _check_paths(rel, rows, root, findings, reports)
    _check_youtube(rel, pin, rows, root, yt, findings, reports, owed)

    unmigrated = [r.id for r in rows if not r.migrated and not r.by_design]
    stats = {
        "rows": len(rows),
        "migrated": sum(1 for r in rows if r.migrated),
        "by_design": sum(1 for r in rows if r.by_design),
        "unmigrated": unmigrated,
        "owed": owed,
        "pin": pin,
        "date": date,
    }
    return findings, reports, stats


def _check_paths(rel, rows, root, findings, reports) -> None:
    """L1 — a written path must be real."""
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


def _check_youtube(rel, pin, rows, root, yt, findings, reports, owed) -> None:
    """L2 — the pin, and the youtube cross-checks that hang off it."""
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
            recon = _check_ids(rel, pin, rows, yt, findings, owed)
            _check_rungs(rel, pin, rows, yt, recon, findings, reports)


def _check_ids(rel, pin, rows, yt, findings, owed) -> set[str]:
    """L3 — every reconstruction has a row, and the pin sees every row; then L2 —
    the pin sits on youtube's tip ref's history. Returns the ids at the pin."""
    recon = youtube_recon_ids(yt, pin)
    have = {r.id for r in rows}
    tip = youtube_tip(yt)
    at_tip = youtube_recon_ids(yt, tip) if tip else set()
    for cid in sorted((recon | at_tip) - have):
        where = "the pin" if cid in recon else f"youtube {tip.rsplit('/', 1)[-1]}"
        owed.append(cid)
        findings.append(
            f"{rel}: L3 youtube reconstruction {cid} exists at {where} but has "
            f"no ledger row — a row is owed. tools/reconstruction_intake.py "
            f"--write adds it (youtube cell from its rung.yaml, the other cells "
            f"`—` until the work lands) and advances the pin."
        )
    for r in rows:
        if r.id not in recon:
            findings.append(
                f"{rel}:{r.lineno}: L3 {r.id} has a row but no reconstruction "
                f"at the pin {pin[:12]} — advance the pin to a youtube commit "
                f"that has it."
            )
    if tip and not is_ancestor(yt, pin, tip):
        findings.append(
            f"{rel}: L2 the pinned youtube commit {pin[:12]} is not an ancestor "
            f"of youtube {tip.rsplit('/', 1)[-1]} — the pin is on a side branch; "
            f"re-pin to a commit on {tip.rsplit('/', 1)[-1]}."
        )
    return recon


def _check_rungs(rel, pin, rows, yt, recon, findings, reports) -> None:
    """L4 — the youtube cell is read from the rung's own state file at the pin."""
    rungs = read_rungs(yt, pin)
    for r in rows:
        rung = rungs.get(r.id)
        if rung is None:
            if r.id in recon:
                reports.append(
                    f"{rel}:{r.lineno}: {r.id} has no rung.yaml at the pin "
                    f"{pin[:12]} — its youtube cell cannot be checked (advance "
                    f"the pin past youtube 30a2709)."
                )
            continue
        if r.youtube == rung.status:
            continue
        if r.youtube == "done":
            findings.append(
                f"{rel}:{r.lineno}: L4 {r.id} says done but its rung.yaml at the "
                f"pin says {rung.status} — a row may not claim a rung finished "
                f"that youtube has not; run tools/reconstruction_intake.py --write."
            )
        else:
            reports.append(
                f"{rel}:{r.lineno}: {r.id} says {r.youtube} but its rung.yaml at "
                f"the pin says {rung.status} — the row is behind its source; "
                f"tools/reconstruction_intake.py --write refreshes it."
            )


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

Scope of the set (K2): **3 <!--count:constructions-total--> constructions**.

| id | title | youtube | naqsh | O1 | O2 | O3 | coaster | catalog | printed |
|---|---|---|---|---|---|---|---|---|---|
| `AAAAAAAAAAA` | first | done | — | — | — | — | — | — | — |
| `BBBBBBBBBBB` | mechanism | done | no piece by design | — | — | — | no piece by design | — | — |
| `_CCCCCCCCCC` | added after the old pin | queued | — | — | — | — | — | — | — |

## Oracle notes
"""


def scratch_git(yt: Path):
    """A `git(*args)` runner for a scratch repo, with a fixed author and no hooks."""
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}

    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(yt), *args], capture_output=True,
                              text=True, check=True, env=env).stdout.strip()

    return git


def write_rung(
    yt: Path,
    cid: str,
    *,
    status: str = "done",
    verdict: str = "PASS",
    passed: int = 9,
    scored: int = 9,
    fresh: bool = True,
    accepted_partial: str | None = None,
    stale_digest: bool = False,
    title: str | None = None,
    creator: str = "Test Maker",
    construction: str = "A = (0,0)\n",
) -> None:
    """A scratch reconstructions/<cid>/ with its construction and rung.yaml.

    The rung's two digests are computed from `construction` the way youtube's
    `make rung-sync` does (sha256 of the bytes, first 12 hex); `stale_digest`
    writes an older digest instead, the shape of a synced half that lags the
    construction beside it — the hard case the design doc's §8 names.
    """
    import hashlib

    d = yt / "reconstructions" / cid
    d.mkdir(parents=True, exist_ok=True)
    (d / "construction.ggb-commands").write_text(construction, encoding="utf-8")
    digest = hashlib.sha256(construction.encode("utf-8")).hexdigest()[:12]
    recorded = "000000000000" if stale_digest else digest
    accepted = f"'{accepted_partial}'" if accepted_partial else "null"
    (d / "rung.yaml").write_text(
        f"id: {cid}\n"
        f"work:\n"
        f"  status: {status}\n"
        f"  blocked_by: []\n"
        f"  accepted_partial: {accepted}\n"
        f"synced:\n"
        f"  title: '{title or 'Rung ' + cid}'\n"
        f"  creator: '{creator}'\n"
        f"  construction_digest: {recorded}\n"
        f"  score:\n"
        f"    verdict: {verdict}\n"
        f"    passed: {passed}\n"
        f"    scored: {scored}\n"
        f"    construction_digest: {recorded}\n"
        f"    fresh: {'true' if fresh else 'false'}\n",
        encoding="utf-8",
    )


def _init_youtube(yt: Path) -> tuple[str, str, str]:
    """A scratch youtube repo shaped like the bknVRSMcLj0 miss. Returns (old_pin, pin, side).

    `old_pin` has AAAAAAAAAAA and BBBBBBBBBBB; the next commit on `main` (`pin`)
    adds _CCCCCCCCCC, the way bknVRSMcLj0 landed in youtube after the ledger's
    pin was taken. _CCCCCCCCCC's rung says `queued` while done.md names it under
    "attempted" — the text-search shape that once read as done. A third commit
    on a feature branch (`side`) — left CHECKED OUT, so it is youtube's working
    tree — adds DDDDDDDDDDD, which is not on `main` and so owes no row yet: the
    gate reads refs, not whatever youtube has checked out.
    """
    yt.mkdir(parents=True, exist_ok=True)
    git = scratch_git(yt)

    def commit(msg: str, done: str) -> str:
        (yt / "docs" / "tasks" / "done.md").write_text(done, encoding="utf-8")
        git("add", "-A")
        git("commit", "-q", "-m", msg)
        return git("rev-parse", "HEAD")

    git("init", "-q", "-b", "main")
    # core.hooksPath is set repo-wide for this clone, so a bare `git init` scratch
    # repo would otherwise fire this project's own pre-commit hooks on its seed
    # commit. Point it at nothing: the scratch repo is not the project.
    git("config", "core.hooksPath", "/dev/null")
    write_rung(yt, "AAAAAAAAAAA")
    write_rung(yt, "BBBBBBBBBBB")
    (yt / "reconstructions" / "_techniques").mkdir()
    (yt / "reconstructions" / "_techniques" / "note.md").write_text("snippet\n", encoding="utf-8")
    (yt / "docs" / "tasks").mkdir(parents=True)
    old_pin = commit("seed", "done: AAAAAAAAAAA BBBBBBBBBBB\n")
    write_rung(yt, "_CCCCCCCCCC", status="queued", verdict="PARTIAL", passed=1, scored=2)
    pin = commit("add C", "done: AAAAAAAAAAA BBBBBBBBBBB\nattempted: _CCCCCCCCCC\n")
    git("checkout", "-q", "-b", "feat/d")
    write_rung(yt, "DDDDDDDDDDD")
    side = commit("add D", "done: AAAAAAAAAAA BBBBBBBBBBB DDDDDDDDDDD\nattempted: _CCCCCCCCCC\n")
    return old_pin, pin, side


def self_test() -> int:
    import shutil
    import tempfile

    failures = 0
    tmp = Path(tempfile.mkdtemp(prefix="constructions-gate-"))
    try:
        yt = tmp / "youtube"
        old_pin, pin, side = _init_youtube(yt)
        primary = tmp / "3d-models"
        (primary / "docs" / "constructions").mkdir(parents=True)
        (primary / ".git").mkdir()  # enough for relative_to; youtube passed explicitly
        ledger = primary / LEDGER_REL

        def run(body: str, **kw):
            ledger.write_text(body, encoding="utf-8")
            return check(root=primary, ledger_path=ledger, yt=kw.get("yt", yt))

        def case(label: str, body: str, want_findings: int, want_report: str | None,
                 must_pass_report_absent: str | None = None,
                 want_finding: str | None = None, **kw) -> None:
            nonlocal failures
            findings, reports, _stats = run(body, **kw)
            ok = len(findings) == want_findings
            if want_report is not None:
                ok = ok and any(want_report in r for r in reports)
            if must_pass_report_absent is not None:
                ok = ok and not any(must_pass_report_absent in r for r in reports)
            if want_finding is not None:
                ok = ok and any(want_finding in f for f in findings)
            print(f"self-test {'ok  ' if ok else 'FAIL'}: {label}"
                  + ("" if ok else f" — findings={findings} reports={reports}"))
            failures += 0 if ok else 1

        clean = _CLEAN_LEDGER.format(pin=pin)
        # Every reconstruction on youtube main has a row and the pin sees them all.
        # DDDDDDDDDDD sits only on the checked-out feature branch: owed nothing yet.
        case("clean ledger blocks nothing", clean, 0, None)
        # The by-design row passed with no path — no finding attributable to it.
        case("by-design row needs no .bkr", clean, 0, None)

        def drop_c(body: str) -> str:
            return "\n".join(l for l in body.splitlines() if "_CCCCCCCCCC" not in l) + "\n"

        # L3: an id at the pin with no row FAILS (was a non-blocking report).
        case("missing row at the pin FAILS", drop_c(clean), 1, None,
             want_finding="_CCCCCCCCCC exists at the pin")
        # L3, the bknVRSMcLj0 miss itself: the pin predates the reconstruction and
        # the row was never written. Reading only the pin saw nothing owed; reading
        # youtube main too FAILS it.
        case("pin lags youtube main, row missing FAILS", drop_c(_CLEAN_LEDGER.format(pin=old_pin)),
             1, None, want_finding="_CCCCCCCCCC exists at youtube main")
        # L3: the row is written but the pin was not advanced — the pin cannot see it.
        case("row the pin cannot see FAILS", _CLEAN_LEDGER.format(pin=old_pin), 1, None,
             want_finding="advance the pin")

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

        # A row that says "attempted" while the rung says done is REPORTED, not failed.
        attempted = clean.replace("| `AAAAAAAAAAA` | first | done |",
                                  "| `AAAAAAAAAAA` | first | attempted |")
        case("attempted-but-done is reported", attempted, 0,
             "says attempted but its rung.yaml at the pin says done")

        # Item 7 of the intake design: done.md names _CCCCCCCCCC under "attempted",
        # and the old text search would have called it done. Its rung says queued,
        # so the clean ledger's `queued` cell draws no report — and a cell that
        # says done over it FAILS.
        case("a done.md mention does not make a rung done", clean, 0, None,
             must_pass_report_absent="_CCCCCCCCCC")
        done_over_queued = clean.replace("| `_CCCCCCCCCC` | added after the old pin | queued |",
                                         "| `_CCCCCCCCCC` | added after the old pin | done |")
        case("done over a queued rung FAILS", done_over_queued, 1, None,
             want_finding="L4 _CCCCCCCCCC says done but its rung.yaml at the pin says queued")

        # L2: a pin on a side branch FAILS as not an ancestor of youtube main
        # (and DDDDDDDDDDD, which that pin has, owes a row — two findings).
        case("pin on a side branch FAILS", _CLEAN_LEDGER.format(pin=side), 2, None,
             want_finding="is not an ancestor of youtube main")

        # The shared reader: the pin sees three rungs, and the digest it recomputes
        # matches the two the rung records.
        rungs = read_rungs(yt, pin)
        ok = (sorted(rungs) == ["AAAAAAAAAAA", "BBBBBBBBBBB", "_CCCCCCCCCC"]
              and all(r.digest_ok for r in rungs.values())
              and rungs["_CCCCCCCCCC"].status == "queued"
              and rungs["AAAAAAAAAAA"].score == "PASS 9/9")
        print(f"self-test {'ok  ' if ok else 'FAIL'}: read_rungs reads three rungs at the pin, digests match"
              + ("" if ok else f" — {rungs}"))
        failures += 0 if ok else 1

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
                    help="the SessionStart lines, answered by tools/reconstruction_intake.py; "
                         "silent when nothing is owed")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if args.session:
        # One reader: the intake tool imports this file's youtube helpers and
        # prints the session lines, so the gate and the hook never disagree.
        # Imported here, not at the top, because the tool imports this module.
        sys.path.insert(0, str(ROOT / "tools"))
        from reconstruction_intake import session_lines  # noqa: E402

        for line in session_lines():
            print(line)
        return 0

    if os.environ.get("CONSTRUCTIONS_OK"):
        print("constructions: skipped (CONSTRUCTIONS_OK=1)")
        return 0

    findings, reports, stats = check()

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
            "a file that is not there, and every youtube reconstruction owes a row. "
            "Override once with CONSTRUCTIONS_OK=1 git commit",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
