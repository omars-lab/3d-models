---
date: 2026-11-13
repo: 3d-models
session: monitor-print-watcher
branch: retro-branch-pass
folded: no
---

## Snags
- `.claude/skills/consolidate-branches/scripts/branch_inventory.py snapshot`: pushing bikar's snapshot refs failed with `make: *** [local.check-node] Error 2`, because bikar's pre-push hook needs Node 22 on the path, and the snapshot push runs that hook. With Node 22 the push took over two minutes. The script could put Node 22 on the path, or the skill could say to.
- `branch_inventory.py verify` calls a branch "diverged, NOT proven dead" when master has merged it and then rewritten some of its lines (`one-app-design`: five lines changed by later PRs). Proving it meant a hand loop over each added line. A mode that lists the branch lines master lacks, and the commit that changed each one, would make that a single command.

## Worth copying
- Saving every tip under `refs/snapshots/<date>/` first, then re-running `verify` on each branch just before deleting it, one at a time, made 22 deletes safe to do without asking.
