#!/usr/bin/env python3
"""Pointer gate for 3d-models — a path named in prose must resolve to a file.

A path inside backticks is prose to every tool in this repo. `docs_gate.py`'s
D1 rule covers markdown *links* (`[text](target)`), which is where a reader
clicks; it says nothing about the far larger set of paths this repo writes as
code spans, which is where a reader *looks*. Those decay the same way and
announce nothing when they do — W-F1's catalog entry pointed at
`Fit-Coupon.bkr` for weeks while describing a different joint, and
`w2-connector-design.md` §8 named `Fit-Step-Gauge.bkr`, a file that has never
existed in any repo (docs/decisions-log.md D-008).

## What transferred from bikar, and under what conditions

This is a port of bikar's `scripts/check-doc-pointers.ts`. The **rule**
transfers unchanged: every backticked path-looking token must resolve, or be
grandfathered in an append-blocked baseline that may only shrink. Two things
did **not** transfer, and stating why is the point of this paragraph:

  - **The implementation language.** bikar is a TypeScript monorepo whose gates
    run under `tsx`; this repo's gates are Python 3 with no toolchain beyond
    the interpreter (`docs_gate.py`, `site_graph.py`). A `.ts` gate here would
    need a `node_modules` that nothing else in the repo needs.
  - **The search roots.** bikar's roots are its own package `src` directories,
    because its docs address modules the way its code imports them. This repo
    has no packages. Its docs instead address **bikar's** files — 97 pointers
    start `bikar/`, 87 start `packages/`, 40 start `kernel3d/` — so the roots
    here are the sibling checkout's roots. That inverts the original's premise
    and is the reason this file is a port and not a copy.

## What resolution means here, precisely

A pointer resolves if the path exists under **any** root tried, so this gate
answers *"could a reader find this file where they would look?"* and not
*"does this path name the repo the sentence implies?"*. `docs/architecture.md`
is bikar's and `docs/backlog.md` is ours, and both resolve. That ambiguity is
inherited from bikar's design and accepted for the same reason: tightening it
would mean rewriting several hundred pointers into a repo-qualified form no
reader asked for. `--list` prints the root each pointer resolved under, so the
ambiguity is visible rather than hidden.

A sibling repo that is **not checked out** makes its pointers unknowable, not
wrong; they are skipped and counted, and the count is printed. This gate has no
CI job — nothing in this repo does — so in practice it runs from
`.githooks/pre-commit.d/35-doc-pointers` and from `make validate-pointers`, on
a machine where the siblings are present. If that ever stops being true the
skip count is the thing to read.

## What is deliberately not an error

Each is a real way to write a path that names no single file:

  - **Template placeholders** — `sessions/<id>/…`, `iterations/N/pattern.bkr`,
    `patterns/**/*.bkr`. A segment that is `N`, `<…>`, `{…}`, `…` or contains
    `*` marks a family.
  - **Bare filenames** — `Makefile`, `tokens.ts`. Ambiguous by construction; a
    path claim needs a separator.
  - **URLs and machine-local absolute paths** — `https://…/spec.md`,
    `/tmp/probe.mjs`, `/Users/…`. Never repo files.
  - **Build outputs at any depth** — `build/stls/…`, `dist/index.js`. These
    exist iff someone has run `make`, so checking them would make the verdict a
    function of working-tree state rather than of the documents. bikar learned
    this the hard way when its gate passed in a built checkout and failed in a
    fresh worktree.

Usage:
  doc_pointers.py                  check the tree
  doc_pointers.py --list           print every pointer and the root it resolved under
  doc_pointers.py --write-baseline rewrite the baseline from the current tree
  doc_pointers.py --self-test      run the fixtures and verify the gate fires

Exit 0 clean / 1 violation. Growth of the baseline needs
DOC_POINTERS_BASELINE_MAY_GROW=1, so it is something someone typed rather than
a diff nobody read.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _git_env() -> dict[str, str]:
    """Env for a `git -C <sibling>` read, with git's own repo pointers removed.

    `GIT_DIR` outranks `-C` — under it a read spelled as bikar's tree is served
    from *this* repo's object store. Here that is latent rather than live, because
    `_exists_in_sibling` tries the working tree before the ref and every sibling
    file currently exists on disk; it would surface the first time a path exists
    at the pinned ref but not in the checkout. Scrubbed anyway: the same variable
    was live in `maintain-use-cases/validate.py`, where it cost 67 pointer checks
    per worktree commit. `.githooks/tests/hook-env-git-dir.sh` holds all three.
    """
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    return env


#: Repo-relative path of the tracked baseline — also the key `git show` uses.
BASELINE_REL = ".claude/gates/doc-pointer-baseline.json"

#: Extensions a backticked token must end in to count as a path claim.
POINTER_EXT = re.compile(
    r"\.(?:ts|tsx|js|mjs|cjs|py|sh|md|json|jsonl|ya?ml|toml|bkr|scad|stl|html|css|svg|png|txt)$"
)

#: A path naming a family rather than a file.
PLACEHOLDER = re.compile(r"(?:^|/)N(?:/|$)|[<>{}*]|\.\.\.|…")

#: Schemes and machine-local absolutes — never repo files.
NOT_A_REPO_PATH = re.compile(r"^(?:[a-z][a-z0-9+.-]*://|/|~)")

#: Build outputs at any depth. Excluded by rule, not baselined: they are not
#: broken, they are absent until someone runs a build.
GENERATED = re.compile(r"(?:^|/)(?:build|dist|coverage|node_modules|\.gh-pages)/")

#: Session/working artifacts that are not repo files.
NOT_REPO_PREFIX = re.compile(r"^(?:iterations|input|output|tmp)/")

#: Documents excluded from the scan, with the reason each is excluded.
#:
#: `docs/research/` is the exclusion this repo needs and bikar's gate never
#: faced. A research file's job is to survey **other projects' source trees** —
#: Cura's `resources/definitions/fdmprinter.def.json`, JSCAD's
#: `packages/modeling/src/operations/booleans/union.js`, machineblocks'
#: `lib/block.scad`. Those paths are claims about a tree this gate has no access
#: to, so a local existence check cannot say anything true about them: it would
#: report ~30 findings, every one of them a correct citation. The transfer
#: condition bikar's rule needs — *the path names a file in a tree we can
#: read* — does not hold here, so the rule does not apply here.
#:
#: The cost, stated rather than discovered later: a research file that cites
#: **our** paths gets no check at all. That is the same trade bikar makes for
#: `docs/issues/`, and the thing that would change it is a research file whose
#: local pointers went stale in a way that mattered.
#:
#: `docs/decisions-log.md` is deliberately **not** excluded, though bikar
#: excludes its `docs/decisions/` tree. bikar's reason is that a decision doc
#: cites the throwaway script that session ran; here the log is one file, the
#: convention is to append a dated correction rather than rewrite, and a
#: superseded filename shows up a handful of times — which is what the baseline
#: is for. If the log starts producing baseline entries faster than decisions,
#: this is the list to add it to.
EXCLUDED: list[re.Pattern[str]] = [re.compile(r"^docs/research/")]

#: Sibling repos that may prefix a pointer, as a **closed set**. An open
#: predicate ("any lowercase first segment might be a repo") fails open: it
#: would report `ok` for any typo whose first segment is not a local directory.
SIBLING_REPOS = ("bikar", "qiyas", "sacred-patterns", "3d-models")

#: Labels that are branches or remotes rather than directories. A pointer
#: written `gh-pages:assets/x.css` names a path on a branch that is not checked
#: out at a stable location, so it is skipped the way an absent sibling is.
NON_DIRECTORY_LABELS = ("gh-pages", "origin", "master", "main")

#: Roots inside a checked-out `bikar` that a pointer may be relative to.
#:
#: This mirrors `SEARCH_ROOTS` in bikar's own `scripts/check-doc-pointers.ts`,
#: because this repo's docs address bikar's source with exactly the shorthand
#: bikar's docs use (`kernel3d/corner-clip.ts`, `packages/core/src/...`). It is
#: a copy of another repo's list and will drift; the drift is safe in one
#: direction only. A root bikar adds and this list lacks turns into a new
#: baseline entry — visible, and blocked by the append-block. A root bikar
#: *removes* would leave this list resolving a path bikar no longer has.
#:
#: The package roots without `/src` (`packages/lab`, `packages/core`) are ours
#: and not bikar's: this repo's skill files address that layout as
#: `src/design/notes/index.ts` and `tests/design-notes.test.ts`, which is
#: package-relative rather than src-relative.
BIKAR_ROOTS = (
    "",
    "packages",
    "packages/core",
    "packages/core/src",
    "packages/web",
    "packages/web/src",
    "packages/cli",
    "packages/cli/src",
    "packages/knobs/src",
    "packages/lab",
    "packages/lab/src",
    "packages/e2e",
    "packages/qiyas-schema",
)

BACKTICKED = re.compile(r"`([A-Za-z0-9_.<>{}*/@:…-]+)`")

#: A backticked span used as a markdown link *label* — ``[`x/y.md`](../x/y.md)``.
#: The label is prose naming the target; the claim that can be false is the
#: target, and D1 in `docs_gate.py` already resolves every relative link. Two
#: gates checking one string means the shorthand label `prototype/catalog.md`
#: gets reported broken while the link beside it resolves — a finding with
#: nothing to fix. Match `](` after the closing backtick and `[` before the
#: opening one, so a backticked path merely *followed* by a link still counts.
#:
#: The target must be **relative** for the hand-off to be real. A label pointing
#: at an external URL — ``[`kernel3d/slice.ts`](https://github.com/…)`` — is a
#: claim about our tree with a link that leaves it, and D1 does not follow URLs;
#: dropping those would lose the check with nothing picking it up.
LINK_LABEL_AFTER = re.compile(r"^\]\((?![a-z][a-z0-9+.-]*:|#)")


class Pointer:
    """One path claim a document makes about a tree, located well enough to report."""

    __slots__ = ("doc", "line", "path")

    def __init__(self, doc: str, line: int, path: str) -> None:
        self.doc = doc
        self.line = line
        self.path = path

    @property
    def key(self) -> str:
        return f"{self.doc} :: {self.path}"


def scanned_docs(root: Path = ROOT) -> list[str]:
    """Every markdown document this gate reads, repo-relative and sorted."""
    out: list[str] = []
    if (root / "CLAUDE.md").exists():
        out.append("CLAUDE.md")
    for d in (".claude/skills", ".claude/gates", "docs"):
        base = root / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            rel = p.relative_to(root).as_posix()
            if any(rx.search(rel) for rx in EXCLUDED):
                continue
            out.append(rel)
    return sorted(set(out))


def pointers_in_line(line: str) -> list[str]:
    """The path claims one line of prose makes — everything else dropped.

    Split out from `collect_pointers` so `--self-test` exercises the real filter
    rather than a restatement of it. The link-label rule is positional, so it
    cannot be tested on a bare path the way the others can.
    """
    out: list[str] = []
    for m in BACKTICKED.finditer(line):
        path = m.group(1)
        if not POINTER_EXT.search(path) or "/" not in path:
            continue
        if PLACEHOLDER.search(path) or NOT_A_REPO_PATH.search(path):
            continue
        if GENERATED.search(path) or NOT_REPO_PREFIX.search(path):
            continue
        if m.start() > 0 and line[m.start() - 1] == "[" and LINK_LABEL_AFTER.search(line[m.end():]):
            continue
        out.append(path)
    return out


def collect_pointers(docs: list[str], root: Path = ROOT) -> list[Pointer]:
    """Every path-shaped backticked token, families and non-repo paths dropped."""
    found: list[Pointer] = []
    for doc in docs:
        text = (root / doc).read_text(encoding="utf-8")
        for i, line in enumerate(text.split("\n"), 1):
            for path in pointers_in_line(line):
                found.append(Pointer(doc, i, path))
    return found


def _sibling_root(name: str, root: Path) -> Path | None:
    """Where sibling `name` is checked out, or None when it is not.

    `bikar` is read from `$BIKAR_DIR` when set — the same variable the Makefile
    passes to `site_graph.py`, so the two gates agree about where bikar is.
    """
    if name == "3d-models":
        return root
    if name == "bikar":
        env = os.environ.get("BIKAR_DIR")
        if env:
            p = Path(env).expanduser().resolve()
            return p if p.is_dir() else None
    p = (root / ".." / name).resolve()
    return p if p.is_dir() else None


#: Every tracked path in a sibling, at a ref, cached per (repo, ref).
_TREE_CACHE: dict[tuple[str, str], frozenset[str] | None] = {}


def _tracked_at_ref(repo: Path, ref: str) -> frozenset[str] | None:
    """Every path tracked in `repo` at `ref`, or None when the ref is unusable.

    WHY THIS EXISTS, and it is not an optimisation. Checking a sibling pointer
    against that sibling's **working tree** makes this gate's verdict a function
    of which branch someone else has checked out. That is not hypothetical: the
    first full run of this gate reported `bikar/patterns/Coupons/
    Clipseat-Fit-Coupon.bkr` as broken minutes after it was merged to
    `origin/main`, because the sibling checkout sat on a detached HEAD that
    predated the merge. It is the same defect bikar found with `dist/` — a gate
    whose answer changes with somebody's working state teaches you to ignore it
    — one repository over.

    Reading the ref instead also satisfies this project's standing rule for a
    checkout another session owns (`docs/decisions-log.md` D-001): read via
    `git show` / `git ls-tree` against a ref, never touch the working tree.
    """
    key = (str(repo), ref)
    if key in _TREE_CACHE:
        return _TREE_CACHE[key]
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", ref],
            capture_output=True,
            text=True,
            check=True,
            env=_git_env(),
        ).stdout
        tree: frozenset[str] | None = frozenset(out.splitlines())
    except (subprocess.CalledProcessError, FileNotFoundError):
        tree = None
    _TREE_CACHE[key] = tree
    return tree


def _shipped_by_makefile(repo: Path, rel: str) -> bool:
    """Is `rel` a build product `repo`'s Makefile names in what it ships?

    A vendored lab page is gitignored (`.gitignore` `/lab.html`) and exists
    only where `make lab-vendor` has run — so "does the file exist" answers a
    question about the local checkout, not about the doc. The rule that
    actually decides whether `3d-models:lab.html` is a real page is the
    Makefile's `LAB_PAGES`, and `DEPLOY_PATHS` is what the site ships; a path
    either list names verbatim resolves whether or not it has been built here.
    Exactly the named token, nothing under it: `assets` is shipped, but that
    does not vouch for `assets/no-such.css` — a child is a fresh claim.

    Found the day a docs-only commit from a fresh worktree failed on a pointer
    that passed in every checkout that had built the site.
    """
    makefile = repo / "Makefile"
    if not makefile.is_file():
        return False
    shipped: set[str] = set()
    for line in makefile.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(LAB_PAGES|DEPLOY_PATHS)\s*[:?]?=\s*(.*)$", line)
        if not m:
            continue
        for tok in m.group(2).split():
            if not tok.startswith("$("):
                shipped.add(tok)
    return rel in shipped


def _exists_in_sibling(repo: Path, rel: str) -> bool:
    """Does `rel` exist in `repo` — in the working tree, or at its upstream ref?

    Working tree first, because it is the cheapest and the common case. The ref
    lookup is what makes the answer independent of someone else's checkout;
    `origin/HEAD` is tried before `HEAD` for the same reason.
    """
    if (repo / rel).exists():
        return True
    for ref in ("origin/HEAD", "origin/main", "origin/master", "HEAD"):
        tree = _tracked_at_ref(repo, ref)
        if tree is None:
            continue
        if rel in tree or any(t.startswith(rel.rstrip("/") + "/") for t in tree):
            return True
    return _shipped_by_makefile(repo, rel)


def _looks_sibling_relative(path: str) -> bool:
    """Is this the unprefixed shorthand for a sibling's own layout?

    `kernel3d/slice.ts` and `packages/core/src/index.ts` are bikar paths written
    the way bikar's own docs write them. They carry no repo prefix, so a broken
    one is reported with no clue that the answer depended on another checkout.
    """
    return not (ROOT / path).exists() and (
        path.startswith("packages/") or path.startswith("kernel3d/") or path.startswith("scripts/")
    )


def resolve_under(path: str, doc: str, root: Path = ROOT) -> str | None:
    """Name the root `path` resolves under, `'skipped'` if unknowable, else None.

    Order matters and is the order a reader would try: this repo, then relative
    to the document doing the pointing (how a markdown link resolves, and the
    only way `../x.md` means anything), then each checked-out sibling.
    """
    label = None
    rest = path
    if ":" in path.split("/", 1)[0]:
        label, rest = path.split(":", 1)
        if label in NON_DIRECTORY_LABELS:
            return "skipped"
        if label not in SIBLING_REPOS:
            return None
    elif path.split("/", 1)[0] in SIBLING_REPOS:
        label, rest = path.split("/", 1)

    if label is None:
        if (root / path).exists() or _shipped_by_makefile(root, path):
            return "."
        if (root / Path(doc).parent / path).resolve().exists():
            return f"{Path(doc).parent.as_posix()}/ (doc-relative)"
        # Unprefixed shorthand for a sibling's own layout — `kernel3d/x.ts`.
        bikar = _sibling_root("bikar", root)
        if bikar is None:
            return "skipped"
        for base in BIKAR_ROOTS:
            if _exists_in_sibling(bikar, f"{base}/{path}" if base else path):
                return f"bikar/{base}" if base else "bikar/"
        return None

    sibling = _sibling_root(label, root)
    if sibling is None:
        return "skipped"
    roots = BIKAR_ROOTS if label == "bikar" else ("",)
    for base in roots:
        if _exists_in_sibling(sibling, f"{base}/{rest}" if base else rest):
            return f"{label}/{base}" if base else f"{label}/"
    return None


# --- baseline -------------------------------------------------------------


def read_baseline(text: str, label: str) -> list[dict[str, str]]:
    """Parse the baseline, failing closed on every shape it does not match."""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise SystemExit(f"{label}: not valid JSON — {e}")
    if not isinstance(parsed, dict) or not isinstance(parsed.get("unresolved"), list):
        raise SystemExit(f'{label}: expected an object with an "unresolved" array')
    for entry in parsed["unresolved"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("doc"), str) or not isinstance(
            entry.get("path"), str
        ):
            raise SystemExit(f'{label}: every entry needs string "doc" and "path" — got {entry!r}')
    return parsed["unresolved"]


def previous_baseline(root: Path) -> list[dict[str, str]] | None:
    """The baseline as of HEAD, or None when it is not tracked yet.

    HEAD is the right comparison point because this gate runs from pre-commit,
    where the working tree is the change and HEAD is its parent. A committed
    baseline that will not parse is a BROKEN baseline, not an absent one, so
    only the `git show` failure is swallowed — `read_baseline` still raises.
    """
    try:
        text = subprocess.run(
            ["git", "show", f"HEAD:{BASELINE_REL}"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return read_baseline(text, f"HEAD:{BASELINE_REL}")


def added_entries(
    previous: list[dict[str, str]], current: list[dict[str, str]]
) -> list[dict[str, str]]:
    """Entries in `current` and not in `previous` — a set question, not a count.

    A count cannot see a swap: delete one entry and add another and the length
    is unchanged. That is not a contrived case — the ratchet-down rule *obliges*
    an author to delete a fixed entry, so "one out, one in" is the ordinary
    shape of a docs commit here.
    """
    before = {(e["doc"], e["path"]) for e in previous}
    return [e for e in current if (e["doc"], e["path"]) not in before]


# --- run ------------------------------------------------------------------


def run(root: Path, list_all: bool) -> tuple[list[str], str]:
    """Check the tree. Returns (violations, one-line summary)."""
    docs = scanned_docs(root)
    pointers = collect_pointers(docs, root)

    resolved: list[tuple[Pointer, str]] = []
    broken: list[Pointer] = []
    skipped: list[Pointer] = []
    for p in pointers:
        where = resolve_under(p.path, p.doc, root)
        if where == "skipped":
            skipped.append(p)
        elif where is None:
            broken.append(p)
        else:
            resolved.append((p, where))

    if list_all:
        for p in pointers:
            where = resolve_under(p.path, p.doc, root)
            mark = "MISS" if where is None else ("skip" if where == "skipped" else "ok  ")
            print(f"{mark} {p.doc}:{p.line}  {p.path}" + (f"   [{where}]" if where and where != "skipped" else ""))

    baseline_path = root / BASELINE_REL
    baseline = (
        read_baseline(baseline_path.read_text(encoding="utf-8"), BASELINE_REL)
        if baseline_path.exists()
        else []
    )
    grandfathered = {(e["doc"], e["path"]) for e in baseline}

    violations: list[str] = []
    for p in broken:
        if (p.doc, p.path) in grandfathered:
            continue
        hint = ""
        head = p.path.split(":", 1)[0].split("/", 1)[0]
        if head in SIBLING_REPOS and head != "3d-models" or _looks_sibling_relative(p.path):
            hint = (
                "\n    If this file was only just added over there, the sibling checkout may\n"
                "    predate it — `git -C <sibling> fetch origin` and re-run before editing prose."
            )
        violations.append(
            f"{p.doc}:{p.line}: `{p.path}` resolves to no file.\n"
            f"    Fix the path, or grandfather it in {BASELINE_REL} with:\n"
            f'      {{ "doc": {json.dumps(p.doc)}, "path": {json.dumps(p.path)} }}' + hint
        )

    # A baselined pointer that resolves now, or is no longer written, is stale.
    broken_keys = {(p.doc, p.path) for p in broken}
    still_written = {(p.doc, p.path) for p in pointers}
    for e in baseline:
        k = (e["doc"], e["path"])
        if k in broken_keys:
            continue
        violations.append(
            f'{BASELINE_REL}: `{e["path"]}` in {e["doc"]} resolves now — delete its entry.'
            if k in still_written
            else f'{BASELINE_REL}: `{e["path"]}` is no longer written in {e["doc"]} — delete its entry.'
        )

    previous = previous_baseline(root)
    if previous is not None and os.environ.get("DOC_POINTERS_BASELINE_MAY_GROW") != "1":
        added = added_entries(previous, baseline)
        if added:
            violations.append(
                f"{BASELINE_REL} GREW by {len(added)} entr{'y' if len(added) == 1 else 'ies'}:\n"
                + "\n".join(f'      {e["doc"]} :: {e["path"]}' for e in added)
                + "\n    The baseline is append-blocked and may only shrink. Fix the\n"
                "    pointer, or state the addition:\n"
                "      DOC_POINTERS_BASELINE_MAY_GROW=1 make validate-pointers"
            )

    summary = (
        f"doc pointers: {len(pointers)} claim(s) in {len(docs)} document(s); "
        f"{len(resolved)} resolve, {len(grandfathered)} grandfathered, "
        f"{len(skipped)} skipped (sibling repo not checked out)"
    )
    return violations, summary


def write_baseline(root: Path) -> None:
    """Rewrite the baseline from the current tree. Never run by the gate."""
    docs = scanned_docs(root)
    entries = sorted(
        (
            {"doc": p.doc, "path": p.path}
            for p in collect_pointers(docs, root)
            if resolve_under(p.path, p.doc, root) is None
        ),
        key=lambda e: (e["doc"], e["path"]),
    )
    seen: set[tuple[str, str]] = set()
    unique = []
    for e in entries:
        k = (e["doc"], e["path"])
        if k in seen:
            continue
        seen.add(k)
        unique.append(e)
    payload = {
        "_comment": (
            "Pointers that do not resolve, grandfathered. APPEND-BLOCKED: this list may "
            "only shrink. Fixing a pointer and deleting its entry is the only routine "
            "edit. See .claude/gates/doc_pointers.py."
        ),
        "unresolved": unique,
    }
    (root / BASELINE_REL).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {BASELINE_REL}: {len(unique)} grandfathered pointer(s)")


# --- self-test ------------------------------------------------------------


def self_test() -> int:
    """Assert each classification fires, on constructed inputs.

    Every case here is a shape measured in this repo's docs, not an invented
    one: the counts in the module docstring come from a scan of the tree.
    """
    cases: list[tuple[str, str | None, str]] = [
        # (path, expected — "resolve" | "miss" | "skipped" | "dropped", why)
        ("docs/backlog.md", "resolve", "a local doc, the plain case"),
        ("docs/no-such-file.md", "miss", "the defect this gate exists for"),
        ("kernel3d/corner-clip.ts", "resolve", "bikar src shorthand, no prefix"),
        ("bikar/patterns/Coupons/Clip-Coupon.bkr", "resolve", "sibling-prefixed"),
        ("bikar/patterns/no-such.bkr", "miss", "sibling-prefixed and wrong"),
        ("gh-pages:assets/style.css", "skipped", "a branch, not a directory"),
        ("https://example.com/spec.md", "dropped", "a URL is not a repo path"),
        ("/tmp/probe.mjs", "dropped", "machine-local absolute"),
        ("build/stls/coupons/W-F1.stl", "dropped", "build output, absent until made"),
        ("patterns/**/*.bkr", "dropped", "a glob names a family"),
        ("sessions/<id>/log.json", "dropped", "a placeholder names a family"),
        ("Makefile.md", "dropped", "no separator — a bare filename is ambiguous"),
    ]
    failures = 0
    for path, expected, why in cases:
        doc = "docs/backlog.md"
        if not pointers_in_line(f"see `{path}` for the shape"):
            got = "dropped"
        else:
            where = resolve_under(path, doc, ROOT)
            got = "miss" if where is None else ("skipped" if where == "skipped" else "resolve")
        ok = got == expected
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {path} → {got} (want {expected}; {why})")

    # A vendored page resolves by the Makefile's rule, not by having been built
    # here — asserted on the helper, because in a checkout that has run
    # `make lab-vendor` the presence check would answer first and hide it.
    rule_cases: list[tuple[str, bool, str]] = [
        ("lab.html", True, "in LAB_PAGES — gitignored, absent until vendored"),
        ("docs/prints.md", True, "in DEPLOY_PATHS by name"),
        ("no-such-page.html", False, "no list names it"),
        ("assets/no-such.css", False, "under a shipped directory, not named — a child is a fresh claim"),
        ("$(LAB_PAGES)", False, "a make variable is not a path"),
    ]
    for rel, want_shipped, why in rule_cases:
        got_shipped = _shipped_by_makefile(ROOT, rel)
        ok = got_shipped == want_shipped
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: shipped({rel}) → {got_shipped} (want {want_shipped}; {why})")

    # The link-label rule is positional: same path, three positions, two verdicts.
    line_cases: list[tuple[str, int, str]] = [
        ("[`docs/a.md`](../docs/a.md) is the doc", 0, "a label with a relative target: D1 has it"),
        ("[`docs/a.md`](https://x.test/a.md) is the doc", 1, "external target — D1 cannot follow it"),
        ("`docs/a.md` and [the doc](../docs/a.md)", 1, "backticks near a link, but not its label"),
    ]
    for line, want, why in line_cases:
        got_n = len(pointers_in_line(line))
        ok = got_n == want
        failures += 0 if ok else 1
        print(f"self-test {'ok  ' if ok else 'FAIL'}: {line!r} → {got_n} claim(s) (want {want}; {why})")

    # The append-block must see a swap, which is why it is a set and not a count.
    prev = [{"doc": "a.md", "path": "x.ts"}]
    cur = [{"doc": "a.md", "path": "y.ts"}]
    added = added_entries(prev, cur)
    ok = len(added) == 1 and added[0]["path"] == "y.ts"
    failures += 0 if ok else 1
    print(
        f"self-test {'ok  ' if ok else 'FAIL'}: one-out-one-in is seen as growth "
        f"(a count would report 1 == 1 and pass)"
    )

    print("self-test: " + ("PASS" if failures == 0 else f"FAIL ({failures})"))
    return 0 if failures == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print every pointer and where it resolved")
    ap.add_argument("--write-baseline", action="store_true", help="rewrite the baseline from the tree")
    ap.add_argument("--self-test", action="store_true", help="verify the gate's own classifications")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.write_baseline:
        write_baseline(ROOT)
        return 0

    violations, summary = run(ROOT, args.list)
    print(summary)
    if violations:
        print(f"\n{len(violations)} violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
