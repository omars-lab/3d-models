---
name: maintain-use-cases
description: Maintain the actor/use-case map for the whole 3d-models experience. Use when shipping or changing any user-facing capability (gallery, Lab, studio, CLI, prototypes, pieces), when the pre-commit use-case hook blocks or reminds, or when auditing what the project supports and where each capability lives in code.
---

# Maintain use cases

The map lives next to this file in `use-cases.md`: a mermaid diagram of every
actor and shipped use case, plus a table pinning each use case to the code
that delivers it. It is the answer to "who is this for and where does that
capability live?" — kept honest by `validate.py` and the pre-commit hook.

## The contract

- **Pointer syntax** (must be backticked): `` `repo:path:L10` `` or
  `` `repo:path:L10-L20` ``. `repo` is `3d-models`, `bikar`, or `qiyas`; paths
  are repo-relative.
- **The syntax is checked everywhere, not only here.** `validate.py` scans every
  markdown file in the repo for it, so a pointer written in `docs/` is held to
  the same three checks as one in the table. It has to be: an anchored pointer
  carries a space and a quote, which puts it outside `doc_pointers.py`'s
  backticked-path class — so before the scan existed, moving a pointer out of
  this file moved it out of *every* gate. Measured 2026-08-17, a pointer naming
  line **99999** of a real file, anchored on a literal present nowhere in it,
  passed `doc_pointers.py`, `docs_gate.py` and this validator at exit 0. The one
  exemption is the reserved repo name `repo:`, which is how the rule is taught.
  A pointer naming a repo the frontmatter does not pin is an error, not a skip.
- **Anchor a pointer that names a specific line**: append a quoted literal that
  must appear inside the range — `` `3d-models:Makefile:L223 "orbs:"` ``. Write
  one whenever the line number *is* the claim; a bare `:L1` means "this file"
  and needs none. Without an anchor, `--refresh` moves the pin forward and
  re-checks only that the file is long enough, which is how **23 of the map's
  44 line claims** ended up on unrelated lines by 2026-08-02 while every run
  printed "all valid". `validate.py` reports the anchored/unanchored split on
  every run, so the gap stays visible instead of being assumed away.
- **Siblings pinned, this repo live.** A `bikar` or `qiyas` pointer is valid at
  that repo's frontmatter `as_of` commit — they move without a commit here to
  blame, so drift after the pin is expected and fine. **A `3d-models` pointer is
  not pinned**: the map and the code it points at ship in the same commit, so
  the self pin is always the *parent*, and validating there checked every anchor
  against exactly the copy the commit was replacing. Since 2026-08-03 a
  self-repo pointer reads what the commit will contain — the index for a staged
  file, HEAD for the rest at commit time, the working tree on a whole-tree run.
  Measured when it changed: 35 of 50 self-repo pointers anchored, **0 drifting**
  against the working tree, and `20-use-cases` already blocks any commit that
  stages a pointed-at file, so drift cannot accumulate unseen.
- **Diagram ↔ table parity**: every `UC<n>` node in the mermaid diagram must
  have a table row and vice versa (validated).
- **Shipped only**: a use case must exist in deployed/committed code.
  Planned experiences stay in design docs and the task list until they ship.
- Cross-repo checkouts (`repos:` in frontmatter, relative to this repo) that
  are missing locally are warn-and-skip, never a failure.

## Workflows

**Add or change a use case** — when a commit ships a new user-facing
capability (or retires one): add/edit the diagram node and the table row with
real pointers, run `validate.py --refresh` (rewrites every reachable repo's
`as_of` and re-validates — fix any pointer it reports broken by re-finding the
line), and stage `use-cases.md` in the same commit as the change. A `3d-models`
pointer you repair for the new content is correct immediately, in the same
commit; there is no follow-up re-pin to make it true.

**Validate** — `make validate-use-cases` (or run
`.claude/skills/maintain-use-cases/validate.py` directly). Checks frontmatter,
pointer existence and line ranges, every anchor against the lines its pointer
names, and diagram/table parity. A drifted anchor is reported with the line the
target moved to, so the repair is the message; every finding names the source it
was read from, so it is never ambiguous what was measured.
`validate.py --self-test` covers the pure readers plus three git fixtures
(unpublished-branch refresh, squash-orphaned pin, and self-repo live reads —
the last pins the counterfactual first, asserting that the old read *passed*
the edit, then that each of the three sources behaves).

**Open one in an editor** — `make use-case-links` prints a `vscode://file/...`
link per pointer, in this map and in every other doc, marked `anchored` or
`line only` and tagged when a sibling link lands off-target because that
checkout has moved past the pin. Generated on demand and never committed: the
URL needs an absolute path, and `doc_pointers.py` rejects `/Users/...` precisely
because such a path is a claim about one laptop. A validation failure prints no
links at all — a clickable link to a line the tool knows is wrong is worse than
none, because it looks authoritative.

**Audit** — read `use-cases.md` top to bottom; anything the project does that
has no UC row is either missing from the map or not actually a user-facing
capability. Actors with no arrows and UC rows whose pointers you cannot
justify are pruning candidates.

## The pre-commit hook

`.githooks/pre-commit` dispatches every script in `.githooks/pre-commit.d/`
in order; `20-use-cases` runs `validate.py --staged`:

| Situation | Result |
|---|---|
| `use-cases.md` staged | Staged content must fully validate AND its `3d-models` `as_of` must equal HEAD (the commit being built on) — otherwise **blocked** |
| Staged file is referenced by a `3d-models` pointer, map not staged | **Blocked** — update the map, or override once with `USE_CASES_OK=1 git commit ...` |
| Staged files touch experience surfaces (`index.html`, `Makefile`, `docs/*.md`, `src/`) | Non-blocking reminder |
| Map's `as_of` > 20 commits behind HEAD | Non-blocking reminder to `--refresh` |

The `as_of == HEAD` rule means the recorded commit is always the parent of
the commit that last touched the map — as recent as it can possibly be
without knowing the new hash.

**After a squash merge, re-pin.** Squashing replaces the branch's commits with
one new commit, so the commit the map pinned survives only as a dangling object
in the clone that made it — a fresh clone of `master` cannot resolve it and
every pointer check fails at once. Full mode now errors when this repo's pin is
not an ancestor of HEAD; it shipped on 2026-08-03 because nothing caught it the
first time. Fix with `validate.py --refresh` on a follow-up commit.

## Rules

- Never edit `as_of` hashes by hand — always `validate.py --refresh`.
- One use case per real capability; do not split one experience into many
  rows to inflate the map.
- Retiring a capability removes its node and row in the same commit.
- The override (`USE_CASES_OK=1`) is for genuinely map-irrelevant edits to a
  referenced file (typo fixes, refactors) — never for shipping an unmapped
  capability.
