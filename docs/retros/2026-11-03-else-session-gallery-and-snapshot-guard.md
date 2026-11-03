---
date: 2026-11-03
repo: 3d-models
session: the "else" session (everything but prints), e778ebdd
branch: consolidation-other-repos, PR #866 (the session's earlier PRs: #864 stale-gallery, #865 snapshot guard)
folded: no
---

## Snags
- `.claude/gates/hook_parity.py` with a Make target: a warning cannot ride on an exit code, make
  reports any failing recipe as 2. It rides on a `<check>: WARN …` output line now; the runner
  repeats those in the summary. Any future "warn, don't fail" check uses that line, not a code.
- `.claude/skills/consolidate-branches/scripts/branch_inventory.py inventory bikar` from a
  worktree looked for `./bikar` and skipped it as "not a git repo". Fixed in #866: a bare name
  resolves under `~/Workspace/git`. The store glob also listed the storefront twice through its
  `-tasks` worktree, with the keep rule applied only once; fixed in the same PR.
- `branch_inventory.py --self-test`: a `git cherry-pick -q` silently did nothing (cherry-pick has
  no `-q`), and the helper `g()` swallows errors, so a negative case passed while checking nothing.
  A commit-count assertion on the fixture caught it. Assert the fixture's shape, not only the verdict.
- `make validate-reflect` finds no transcripts when run from a worktree (it reads the main
  checkout's session dir). Tooling gap, not fixed.

## Worth copying
- Before writing a guard, run its rule read-only against the real case (hifth's old-history
  snapshot) with a scratch script; it named the two pictures before the tool existed.
- Prove a negative test discriminates by disabling the check it defends and watching it fail
  (the advisor asked for this; the first version was hollow).

## Didn't work
- Snapshotting a bikar tip pushes through bikar's pre-push hook, which runs the full suite
  (minutes) even for one snapshot ref; that is PR #365's fix, Omar's to merge.
