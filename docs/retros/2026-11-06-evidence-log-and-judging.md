---
date: 2026-11-06
repo: 3d-models
session: plates-and-feedback (evidence log, closeout-1 judging)
branch: after-print-copies; also #916, #917, #918, 3d-model-hub #26 and #27
folded: no
---

## Snags
- `.githooks/pre-commit.d/56-decision-evidence`: since the evidence log lists the plates waiting
  to be judged, any tool that changes that list must rewrite the page in the same commit, or the
  hook refuses it. #917 made `after_print.py answer` and `print_monitor.py` do it. The hub stages
  files by name, so it needed its own change as well (3d-model-hub #27). A new generated page that
  a hook keeps current needs every writer of its inputs listed before it ships.
- `.claude/skills/review-print/scripts/after_print.py`: `matched()` compared recipe items one to
  one with the bed map, so any `count: 2` item made every piece unmatched and `pieces` refused.
  closeout-1 found it. Fixed on this branch.
- The complexity hook refused a three-line addition to `after_print.py`'s `main`. Putting the new
  lines in a small function of their own is the fix, and it is quicker than arguing the score.
- The live hub could not be updated after #26 and #27 merged. Another session had uncommitted
  changes in the hub's main checkout, which only takes a fast-forward. Work merged on the hub is
  not live until that checkout is clear.

## Worth copying
- Asking the advisor before the hub change caught that the hub stages only the plate page. A
  hook-56 refusal would otherwise have shown up on Omar's first saved answer.
