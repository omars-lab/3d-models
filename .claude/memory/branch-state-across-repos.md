---
name: branch-state-across-repos
description: Remote branch state after the 2026-08-30/31 cleanup, re-verified 2026-09-22 (3d-models master + gh-pages only, 0 open PRs, two detached worktrees kept, snapshot ref) — one kept prior-art branch, one superseded branch that must never merge, branch guards and protection since 2026-09-02
metadata:
  type: project
---

Remote state after the cleanup (all merges sentinel-verified by content, not subject): **bikar** = `main` only; **qiyas** = `main` only; **3d-models** = `master` + `gh-pages` (deliberately diverged, never merged into master); **sacred-patterns** = `master` + `gh-pages` + `wip/react-d3-2024` (kept as cited prior art for the d3 work; `wip/weave-progress-page` was merged as PR #43 `0d3ad1e`). One bikar branch was SUPERSEDED, not merged: `fix/weave-amplitude-guard-by-depth-suffix` improved a rule main withdrew in D-042 and was deleted — if it reappears, it must not merge.

**Re-verified 2026-09-22 (second consolidation):** **3d-models** remote = `master` + `gh-pages` only, 0 open PRs. Eight squash-merged leftovers were deleted by content diff vs `origin/master`, and `feat/x2d-slice-preflight` (one commit, superseded by master's bench sheet) was deleted local + remote. The shared checkout sits on `master`; the linked worktrees `../3d-models-pm` and `../3d-models-master-ro` are clean and detached at master (kept as cheap two-way doors, not removed). The pre-cleanup shared tree is preserved at `refs/snapshots/tree-2026-09-22` (9efbc3d) if anything turns out to be missing. Only untracked file left: `.env` (dotenvx-encrypted, public repo — Omar's call whether it stays untracked or goes).

Since 2026-09-02 a pre-commit hook refuses direct commits on main/master in both repos (`BRANCH_OK=1` overrides; bikar #136 `4ac089b`, 3d-models #131 `04f2137`), and branch protection is applied: bikar main requires ci/e2e/gitleaks (admins not enforced), 3d-models master is PR-only (D-048/D-049).

**Why:** a stale local `main` can be ahead of origin with pre-rebase duplicates; "origin authoritative" was once asserted before being verified.

**How to apply:** sentinel-verify before any reset or delete; a parity test that diffs an ahead/behind count another session can move is flaky by construction — mask it. Flow rules: [[pr-flow-for-all-repos]], [[git-and-gh-mechanics]].
