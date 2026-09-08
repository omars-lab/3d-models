---
name: gate-verdict-checkout-independent
description: "A gate's verdict must not depend on which checkout runs it — linked worktrees sit one level below the siblings, and a self pin taken at branch HEAD does not survive a squash merge"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 416aa36c-c7af-4cf1-91db-d2cdc9668841
  modified: 2026-09-02T19:56:32.780Z
---

A gate's verdict must not depend on which checkout runs it. Two ways it did in 3d-models
(found 2026-09-01, fixed in #132 `44fba5c` and #133 `b7a8908`):

- **Linked worktrees** (`X.worktrees/<branch>`) sit one directory deeper than the primary
  clone, so `../bikar` and `../../bikar/...` resolve into the empty `X.worktrees/`. Three
  gates (doc_pointers, docs_gate D1, the use-case validator) silently skipped or
  downgraded every sibling pointer from a worktree, and one turned "skipped" into
  "resolves now" and blocked the commit. Now each retries beside the primary clone via
  `git rev-parse --git-common-dir` (GIT_* scrubbed, or a hook makes every checkout answer
  as the primary).
- **A self pin taken at branch HEAD** (the use-case map's own `as_of`) is orphaned by a
  squash merge — master carried a hash that no longer existed. Now pinned at
  merge-base(HEAD, origin default), i.e. the published base.

**Why:** the hook and a hand-run from the primary disagreed, so the gap survived; the
`BIKAR_DIR` knob and `USE_CASES_OK=1` were being used as workarounds for a gate defect.

**How to apply:** any gate that touches a path outside the repo, or pins the repo's own
history, ships a self-test that builds a primary + worktree + sibling layout in a tempdir
and asserts the same verdict from both. Do not reach for `BIKAR_DIR`/`USE_CASES_OK=1`
from a worktree without first checking whether the gate, not the tree, is wrong. Related:
[[3d-models-use-case-hook]], [[stacked-pr-stranding]].

**Third gate brought under the rule, 2026-09-02 (#158 `2e93495`).** `site_graph.py`'s
`cross_check_bikar` (the G6 mirror check) read bikar's `public-surface.json` from the
**working tree** — so a peer session's stale bikar checkout (`public` where origin/main
says `access`) made it false-fire G6 on every 3d-models commit. It caught me landing the
truthful `access` mirror: the self-test itself went red against the stale sibling. Fixed
the same way doc_pointers does it — read at the **published ref** (`git show
origin/HEAD:packages/web/public-surface.json`, then `origin/main`/`origin/master`), env
scrubbed of GIT_*; skip to MIRRORED-ONLY when no clone or ref is reachable. Its self-test
gained a **G6 case**: a scratch bikar whose committed ref says `access` and whose working
tree says `public`, requiring the read to return `access` (red before, green after). The
value read for a cross-check must come from the authority (a ref), never a checkout —
working-tree-OR-ref (doc_pointers' existence check) is fine for *does this path exist* but
reintroduces drift for *what value does it hold*.
