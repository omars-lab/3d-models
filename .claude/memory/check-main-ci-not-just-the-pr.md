---
name: check-main-ci-not-just-the-pr
description: "bikar's `ci` workflow was red on main for four runs (2026-08-31 → 09-02) and three PRs merged on top of it; a PR's red check may be main's, so read main's last run before diagnosing yours"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 332d42c3-dfe9-490a-9db7-883074290c91
  modified: 2026-09-02T01:34:45.746Z
---

When a PR check is red, look at main's last run of the same workflow before reading the PR's log as if the PR caused it. On 2026-09-02 bikar #130's `ci` was red with `no SVG rasterizer found` from `timelapse-story.test.ts` beat 4 — a dependency #121 added on 2026-08-31 that ubuntu-latest does not ship. Main had been red for four runs and #125, #128 and #129 merged on top of it. Fixed by bikar #131 (eef7587): the `Install a rasterizer` step from `orb-validate.yml`, plus its `ci-parity.yaml` entry. The same day #132 turned it red again (codespell on `parseRing`), fixed by adding the identifier to `.codespellrc` in its own PR (#133). Then a direct push (`5ddbd95`, no PR) left `package-lock.json` out of sync and `npm ci` refused it on main's next run. Three instances in one day is a pattern, not an accident — bikar main is not branch-protected; D-048 in 3d-models' decisions log holds the measurement and the command.

**Why:** main is not branch-protected in bikar, so nothing stops a merge on red, and a red gate that everyone merges past is ignored within a week (bikar's own `ci.yml` header says so). The PR author reads the failure as theirs, spends the diagnosis on the wrong tree, or worse, merges on red because "it was red before" — which is how the streak grew to four.

**Recurrence, 2026-09-17 (admin merges):** while bikar's checks were billing-blocked (every run `steps: 0`, nothing measured), #209 (interlock coaster files) and #210 (Coaster Lab, whose roster test globs every `*-coaster.bkr` on disk) were admin-merged within hours of each other. Each was green locally on its own base; together they made main red on `coaster-presets.test.ts` (`expected 2 to be 4`) and nobody saw it until the next branch ran the full suite. Fixed in #211 by rostering the twins. When CI cannot run, **the local full suite on a rebased branch is the merge gate**, and after every admin merge run it once on `origin/main` itself before the next one.

**How to apply:** `gh run list -R NaqshCoffee/bikar -b main -w ci -L 3` first. If main is red for the same reason, fix that in its own PR off main (never stacked on the feature branch), merge it, rebase the feature branch so its `pull_request` run uses the fixed workflow file, then poll to green. Pair with [[gh-auto-merge-footgun]] and [[pr-flow-for-all-repos]].
