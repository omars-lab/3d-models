---
date: 2026-11-03
repo: 3d-models
session: plates-and-feedback
branch: star-2-record, PR #854; star-2-done-pr, PR #855
folded: no
---

## Snags

- `.claude/skills/review-print/SKILL.md`: step 2 asks for the `pattern-catalog` sync in the middle
  of a paragraph, so it got skipped, and hook `51-pattern-catalog` then blocked the record's
  commit. The record steps should end with `catalog.py sync`, next to `prints_page.py --write`.
- `.claude/gates/plates_gate.py --write`, run by a relative path from a worktree session, ran
  against the main checkout, because that was the shell's folder. It changed nothing that time.
  A worktree session should call gates and page writers by the worktree's full path.

## Worth copying

- Writing a record from the hub's answers: pieces Omar named got his words as their verdict, and
  pieces nobody named stayed `not-judged` instead of being guessed (star-2: one kept, two
  dropped, three not judged).
- `.claude/skills/judge-page/scripts/open_questions.py` opened the hub at the first question
  still owed, in one call.
