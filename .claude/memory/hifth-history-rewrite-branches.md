---
name: hifth-history-rewrite-branches
description: "hifth's main was rewritten 2026-10-08 to scrub two held-text pictures; old-history branches look diverged, must be proven dead by hand, and their snapshots must never be pushed"
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-28T00:05:44.895Z
---

hifth's main was rewritten on 2026-10-08 (`git filter-repo --strip-blobs-with-ids`) to remove two
pictures showing held Quran text: `native/shots/baseline/ipad-hafs-kfqc_2_255.png` (old blob
8b7c1d13…) and `iphone-hafs-kfqc_2_255.png` (old blob 5f251330…). Main has new pictures under the
same names.

- Every branch still on the old history shows as `diverged` (about +500–900 / −1432) in the
  consolidate-branches inventory, and its history holds the scrubbed blobs.
- Prove one dead by hand: compare its tree with the rewritten twin of the same merge (find it by
  commit subject on origin/main); the only differences should be the two pictures.
- **Never push a snapshot of such a tip** (`branch_inventory.py snapshot … --no-push` only): it
  re-publishes the scrubbed pictures.
- Still on hifth's GitHub as of 2026-10-27, Omar's to purge: ~130 old-history branches, ~60
  `refs/snapshots/2026-10-04/*` and `2026-10-08/*` refs, and `refs/pull/*` (needs GitHub Support).
- 2026-10-27 pass: the three agent branches at 17a22559 matched new main's #193 merge (94233180)
  bar the two pictures; local-only snapshots written, branches deleted.

**Why:** the inventory's printed snapshot line pushes by default and would undo the scrub.
**How to apply:** in any consolidate pass over hifth, skip the printed snapshot line; a
rules.md Known-traps line and a script guard (refuse to push a tip holding a blob origin's default
lacks) are still to ship. See [[branch-state-across-repos]].
