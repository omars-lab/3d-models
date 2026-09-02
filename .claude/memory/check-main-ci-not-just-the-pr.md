---
name: check-main-ci-not-just-the-pr
description: "bikar's `ci` workflow was red on main for four runs (2026-08-31 → 09-02) and three PRs merged on top of it; a PR's red check may be main's, so read main's last run before diagnosing yours"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 332d42c3-dfe9-490a-9db7-883074290c91
  modified: 2026-09-02T01:34:45.746Z
---

When a PR check is red, look at main's last run of the same workflow before reading the PR's log as if the PR caused it. On 2026-09-02 bikar #130's `ci` was red with `no SVG rasterizer found` from `timelapse-story.test.ts` beat 4 — a dependency #121 added on 2026-08-31 that ubuntu-latest does not ship. Main had been red for four runs and #125, #128 and #129 merged on top of it. Fixed by bikar #131 (eef7587): the `Install a rasterizer` step from `orb-validate.yml`, plus its `ci-parity.yaml` entry.

**Why:** main is not branch-protected in bikar, so nothing stops a merge on red, and a red gate that everyone merges past is ignored within a week (bikar's own `ci.yml` header says so). The PR author reads the failure as theirs, spends the diagnosis on the wrong tree, or worse, merges on red because "it was red before" — which is how the streak grew to four.

**How to apply:** `gh run list -R NaqshCoffee/bikar -b main -w ci -L 3` first. If main is red for the same reason, fix that in its own PR off main (never stacked on the feature branch), merge it, rebase the feature branch so its `pull_request` run uses the fixed workflow file, then poll to green. Pair with [[gh-auto-merge-footgun]] and [[pr-flow-for-all-repos]].
