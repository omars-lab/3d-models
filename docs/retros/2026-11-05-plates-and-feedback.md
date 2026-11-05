---
date: 2026-11-05
repo: 3d-models
session: plates-and-feedback
branch: piece-grams, PR #883; question-sort, PR (this one)
folded: no
---

## Snags

- `tools/print_review.py` imports PIL at the top, and the hub runs `after_print.py` with a
  python3 that has none. Anything after_print needs from it has to live in a stdlib-only file
  (`tools/piece_grams.py` was the first).
- `.claude/skills/review-print/scripts/after_print.py questions`: rows that name pieces in words
  ("Both stars here") get no grams. Only carved ids or whole recipe labels can be counted.
- `gh pr merge` without `--delete-branch` left the remote branch behind; it had to be deleted by
  hand after the merge.

## Worth copying

- Sorting open questions by reading the later plates' records (`lesson`, `next`) and the next
  plate page's "In short" first. split-10's page showed that Omar had already judged split-07
  in chat, which no `## Judged` table recorded.

## Didn't work

- Reading split-07's eight questions as all unanswered because its `## Judged` table was empty.
  Chat answers moved them on.
