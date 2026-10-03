"""Each plate's recipe iterations, and the git facts a yes is checked against (D-097).

A plate's recipe changes in place: no new plate per version. Each version that differs from the
last is an iteration, numbered from 1 per plate and kept in `approvals.yaml` beside this skill.
The page's frontmatter says which iteration it is at (`iteration: N`). A yes in the page's
Approvals table names the iteration and the commit on master it approved
(`iteration 2 @ 1a2b3c4d5e`), so `git show <commit>:docs/design/plates/<plate>.yaml` is exactly
what Omar said yes to and `git diff <commit> -- <recipe>` is what changed since.

What counts as a change is the recipe's content, not its text: a comment or key order does not
make an iteration, so a reprint as-is keeps its iteration and its yes. The plates gate imports
this module (hook 39); `plate_approve.py --iterate` is the only writer.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml

STORE_REL = Path(".claude") / "skills" / "manage-approvals" / "approvals.yaml"
# A yes covers a recipe as it is on master. A branch commit would not do: a squash merge drops it.
MASTER = "origin/master"
COVERS = re.compile(r"^iteration (\d+) @ ([0-9a-f]{10})$")
HASH = re.compile(r"^[0-9a-f]{12}$")
HEADER = """\
# Each plate's recipe iterations (D-097), written by
# `python3 .claude/skills/manage-approvals/scripts/plate_approve.py <plate> --iterate`.
# An iteration is a version of docs/design/plates/<plate>.yaml whose content (not its comments)
# differs from the one before; `recipe` is its hash. A yes on the plate's page names the
# iteration it covers and the master commit it approved. The plates gate (P9) checks this file
# against the pages and the recipes; do not edit it by hand.
"""


def repo_of(path: Path) -> Path | None:
    """The working tree a path sits in: the nearest parent holding `.git` (a worktree's is a file)."""
    for p in (path, *path.parents):
        if (p / ".git").exists():
            return p
    return None


def store_for(plates: Path) -> Path:
    root = repo_of(plates.resolve())
    return (root or plates.parent) / STORE_REL


def hash_text(text: str) -> str | None:
    try:
        recipe = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    if recipe is None:
        return None
    canon = json.dumps(recipe, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:12]


def recipe_hash(page: Path) -> str | None:
    """The recipe's content, not its text: comments and key order do not change it."""
    try:
        return hash_text((page.parent / f"{page.stem}.yaml").read_text(encoding="utf-8"))
    except OSError:
        return None


def read_store(store: Path) -> tuple[dict[str, list[dict]], list[str]]:
    """({plate: [entry, …]}, problems). Each entry is {iteration, recipe, date}, oldest first."""
    if not store.is_file():
        return {}, [f"no iterations file {STORE_REL}"]
    try:
        data = yaml.safe_load(store.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return {}, [f"{STORE_REL} does not parse: {e}"]
    if not isinstance(data, dict):
        return {}, [f"{STORE_REL} is not a mapping of plate to iterations"]
    out, bad = {}, []
    for plate, entries in data.items():
        if not isinstance(entries, list):
            bad.append(f"{plate}: its iterations are not a list")
            continue
        rows = []
        for i, e in enumerate(entries, 1):
            e = e if isinstance(e, dict) else {}
            date = e.get("date")
            date = date.isoformat() if isinstance(date, dt.date) else str(date or "")
            row = {"iteration": e.get("iteration"), "recipe": str(e.get("recipe") or ""),
                   "date": date}
            if row["iteration"] != i:
                bad.append(f"{plate}: entry {i} is numbered {row['iteration']!r}, not {i}")
            if not HASH.match(row["recipe"]):
                bad.append(f"{plate}: iteration {i}'s recipe {row['recipe']!r} is not a 12-hex hash")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                bad.append(f"{plate}: iteration {i}'s date {date!r} is not YYYY-MM-DD")
            rows.append(row)
        if [r["date"] for r in rows] != sorted(r["date"] for r in rows):
            bad.append(f"{plate}: its iterations are not in date order")
        out[str(plate)] = rows
    return out, bad


def write_store(store: Path, data: dict[str, list[dict]]) -> None:
    lines = [HEADER.rstrip("\n")]
    for plate in sorted(data):
        lines.append(f"{plate}:")
        lines += [f"  - {{iteration: {e['iteration']}, recipe: '{e['recipe']}', date: '{e['date']}'}}"
                  for e in data[plate]]
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_covers(covers: str) -> tuple[int, str] | None:
    m = COVERS.match(covers)
    return (int(m.group(1)), m.group(2)) if m else None


def _git(page: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", "-C", str(page.parent), *args], capture_output=True,
                           text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout if r.returncode == 0 else None


def master_commit(page: Path, ref: str = MASTER) -> str | None:
    """The last commit on master that changed this plate's recipe, abbreviated to ten."""
    out = _git(page, "log", "-1", "--format=%H", ref, "--", f"{page.stem}.yaml")
    return out.strip()[:10] if out and out.strip() else None


def hash_at(page: Path, commit: str) -> str | None:
    """The recipe's hash at a commit, or None when the commit or the file is not there."""
    out = _git(page, "show", f"{commit}:./{page.stem}.yaml")
    return hash_text(out) if out is not None else None


def on_master(page: Path, commit: str, ref: str = MASTER) -> bool:
    return _git(page, "merge-base", "--is-ancestor", commit, ref) is not None
