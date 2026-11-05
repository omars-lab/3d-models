---
date: 2026-11-05
repo: 3d-models
session: plates-and-feedback
branch: piece-grams, PR #883; question-sort, PR #884; hexfit-2, PRs #890, #891; hexfit-2-sent, PR (this one)
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
- `tools/print_review.py pins` labels each join with its STL's file name, so a picture for the
  page needs the STLs copied to version names first (hexfit-2: `1-dot-HEX-CTRL.stl` …).
- `.claude/gates/plates_gate.py` has no `supersedes:` key; a page says what it replaces in its
  text. A slice made before recipe hashes were written shows `✗ slice` at the dry run and has
  to be sliced again from the vault.
- `tools/bambu/src/backends/tls-pin.ts`: the printer's certificate was read from each worktree's
  own `.bambu/`, so the hub's printer panel said "can't reach the printer" while the
  printer answered. Fixed in #892 (read from the main checkout); other `.bambu/` paths in the
  CLI still resolve per worktree and may hide the same trap.
- `.claude/skills/review-print/scripts/after_print.py pieces`: on a plate whose pieces carry dots
  instead of ids (hexfit-2, D-121) and print as two halves, it refuses with "does not match the
  recipe's items label for label". The real reason is that there are no ids to name pictures by
  and the bed has two objects per recipe item; the message should say so.

## Worth copying

- Sorting open questions by reading the later plates' records (`lesson`, `next`) and the next
  plate page's "In short" first. split-10's page showed that Omar had already judged split-07
  in chat, which no `## Judged` table recorded.

## Didn't work

- Reading split-07's eight questions as all unanswered because its `## Judged` table was empty.
  Chat answers moved them on.
