---
date: 2026-11-06
repo: 3d-models
session: plates-and-feedback (closeout-1 send)
branch: approve-queue-followup; also #903, #904, #906, #907
folded: no
---

## Snags
- `.claude/skills/manage-approvals/scripts/plate_approve.py`: every page change left the plates
  gate failing on the plate queue until `plates_gate.py --write` ran by hand. This happened on four
  commits running. Fixed in #907: the tool now rewrites the queue itself. The first version printed
  the queue line on stdout, which `bambu print send` reads as the timeline row. The follow-up
  moves it to stderr and adds a self-test case.
- `docs/design/plates/closeout-1.yaml`: a `ledge_bitten_by_design` line copied from split-08 when
  the plate was made claimed a bite this plate does not have. The send's ledge check caught it.
  The fix was a new iteration and a new yes (#903, #904). When copying a recipe, drop the by-design
  lines unless the new plate really keeps them.
- `bambu slice compose` has no `--quiet`, though other verbs take one. Run it without the flag.
- `git show <ref>:<path> --output=<file>` printed to the terminal and wrote an empty file, so a
  `cmp` against it looked like a mismatch. To check that a vault file matches master, compare
  `git rev-parse <ref>:<path>` with `git hash-object <path>`.

## Worth copying
- The send's own checks (the ledge check, and an approval refused until its iteration is on
  master) caught a false recipe line before any filament moved. Fixing the recipe rather than
  getting round the check cost two small PRs and one more yes from Omar.
