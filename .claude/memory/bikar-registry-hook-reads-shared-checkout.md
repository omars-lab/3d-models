---
name: bikar-registry-hook-reads-shared-checkout
description: "bikar's pre-commit `gen-calibration-registry` check reads ../3d-models/.claude/skills/calibrate/bets.md (whatever branch the shared checkout is on); set THREED_MODELS_DIR to a worktree at master content, and fresh bikar worktrees need npm install + build before pre-commit runs"
metadata: 
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-21T00:43:07.261Z
---

bikar's pre-commit `gen-calibration-registry` check compares against
`../3d-models/.claude/skills/calibrate/bets.md` — the SHARED 3d-models checkout, on whatever
branch another session left it. If that copy is stale, EVERY bikar commit and cherry-pick
`--continue` is blocked with "bets.md is STALE", even though the bikar change is fine.

**Why:** 2026-09-17: the shared 3d-models was on another session's `feat/x2d-slice-preflight`
with a stale bets.md; bikar #195 (which registered CAL-EQV-01) could not be followed by any
commit until bets.md was regenerated on master (3d-models #207).

**How to apply:** Prefix bikar commits with
`THREED_MODELS_DIR=/Users/omareid/Workspace/git/3d-models-constructions` (or any 3d-models
worktree at master content). NOTE (2026-09-20): "master content" means **origin/master**, not a
stale *local* master — this session the shared checkout AND the `3d-models-pm` worktree (local
master, behind origin) were both stale; only origin/master's bets.md was in sync. Fix was
`git -C 3d-models-master-ro checkout --detach origin/master` then point THREED_MODELS_DIR there.
Confirm sync first: `THREED_MODELS_DIR=<dir> npx tsx scripts/gen-calibration-registry.ts --check
--out <dir>/.claude/skills/calibrate/bets.md` must print OK. Two separate bikar hooks read the
sibling: this `gen-calibration-registry` sync check AND the calibration-records registry hook —
both fire on any staged `packages/core/src/` file, even an importer change that touches no
calibration record. Regenerate bets.md with
`THREED_MODELS_DIR=… npx --prefix <bikar-worktree> tsx <bikar-worktree>/scripts/gen-calibration-registry.ts`
and ship it as its own 3d-models PR (counts gate: every `<!--count:cal-bets-->` site and the
design-coupon id lists beside them must be updated too). A fresh bikar worktree also needs
`npm install` + `npm run build` before its pre-commit (eslint config, typecheck) can run.
Related: [[force-push-denied-cherry-pick-fresh-branch]], [[bikar-build-and-test-traps]].
