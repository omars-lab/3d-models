---
name: d3-integration-decisions
description: The settled d3 integration calls (Q-HOME, Q-SHELL, Q-VOCAB, Q-DATA) and the orb-view instrument's join findings — the ring is the key, two id namespaces, join lives in the overlay
metadata:
  type: project
---

Settled with the user 2026-08-31, recorded in `docs/d3-integration-design.md` §5 (3d-models #113 `75cf71d`): **Q-HOME** = opt-in converter on a d3-agnostic bikar core (`viz-d3.ts`, extractable to `@naqshcoffee/bikar-d3` when a second consumer appears); **Q-SHELL** = plain/Lit shell, not React (the `wip/react-d3-2024` shell is cited prior art only); **Q-VOCAB** = converge on one naming convention, refactoring either side is authorized; **Q-DATA** = qiyas emits per-shape `{id,x,y,status}` as a documented JOIN of `/encoding`+`/diff`, not new fields (D-API-4, qiyas #25 `65b0edb`). Studio pages: `/rosette-explorer` (bikar #125 `ac26658`) and `/orb-instrument` (bikar #132 `7824e12`; qiyas #26 `95dd893` added inline `POST /diff`, D-API-5).

- **Two id namespaces**: ref-side buckets join on `/encoding(ref)`, recon-side (surplus, `matched.recon_id`) on `/encoding(recon)`.
- **The ring is the key, not the centroid**: on orb faces centre-in-face is not bijective (concave hexagram fragments); qiyas keeps bikar-tagged contours vertex-exact, so `evidence.outline` matches one `<path data-face-index>` ring 55/55 at 0.0 deviation. By-design: unknown id → `unknown`, unclaimed face → `unclaimed`, id in two buckets throws.
- Fixtures are pinned to the live render byte-for-byte AND to the encoding's `image.sha256`, so drift reads red, not stale.

**Why:** the obvious key failed on the first concave case — a join key is measured on real data before it is coded.

**How to apply:** the join lives in the d3 overlay by default; add a qiyas endpoint only when a second consumer wants it. Explorer-side findings: [[rosette-explorer-findings]]; API rules: [[qiyas-runtime-and-gates]].
