---
date: 2026-11-03
repo: 3d-models
session: else
branch: authorized-2026-11-03, PR #872
folded: no
---

## Snags

- The auto-mode classifier refused `gh pr merge` on bikar #368 twice, as "merge without
  review", even after the diff was read and the local CI had passed in the pre-push. Merging a
  sibling repo's PR is Omar's step from this harness; the edits that wait on that merge (the
  ledger row, the CS-18 block, the catalog sync) were written out in the agent's hand-off file
  instead of guessed into the tree.
- The plates gate blocked the first commit after master gained star-3's print log (#871):
  a branch cut before an append-only log exists reads as having deleted it. Merge
  `origin/master` into the branch before committing; the overlap check (`comm` of the two
  file lists) showed nothing shared, so the merge was clean.
- After that merge, hook 20 refused the staged map: its `as_of` pin was the old merge-base.
  `validate.py --refresh` and restage; the map moves with every merge from master.
- Changing a ledger oracle cell (gBV's O1, FAIL 134/20 to PASS 144/0) changes the catalog page
  that quotes it, and hook 51 blocks the commit until `catalog.py sync` is run and the page is
  staged too. A ledger cell edit and its catalog sync are one commit.
- Agent C's strict pre-push suite raced on the Studio keyboard-dial specs at load average 75:
  four agents' test workers in sibling bikar worktrees. The agent waited for the load to drop
  and pushed again rather than skipping the gate. Several bikar pushes at once from one
  machine is too many; stagger them.

- Hook 20 blocked a ledger note written under an anchored line, because the unchanged
  map could not be staged to clear it. Fixed in the hook rather than overridden: when the
  map is not staged, the pointers into a staged file are now read against the staged content
  and the commit passes when every one still resolves (a moved or unanchored pointer still
  blocks); four self-test cases cover both ways.

## Worth copying

- One branch, four agents, each committing its own files by name, the main session
  serializing the decisions log: no two agents wrote the same file, and the log got one commit
  with six ids.
- Getting the decisions log past hook 20 by bundling a legitimate map change (UC34 for the
  intake tool, plus the repaired pins) instead of an override.
- A hand-off file for edits that must wait on another repo's merge, with the exact
  replacement lines and the gates to run, so the next session applies them without
  rediscovering the ledger's column rule.
- Reading the sibling's PR diff and its description before the merge attempt, so the review
  stands on the record whoever merges it.

## Checks on the tip

Every later tip of the branch (the hook 20 fix, the held-edits file, this note) was run the
same way before its push, and the PR body names the verdict on the final tip.

## Blossom follow-up

- bikar #368 merged on Omar's "merge all prs", and the held edits (ledger row and count,
  the Oracle-notes paragraph, CS-18, the catalog page and picture, the baseline entry) were
  applied from the checked-in hand-off file and the file deleted in one commit (#873). The
  catalog sync had said "89 already in step" before the ledger row changed: it reads
  migration from the ledger row, not from bikar, so the row goes first and the sync after.

- `make validate` on 63c9ac00, in the worktree with `build/orb-breakdown` removed first: hook-parity all 32 verified, exit 0. The `FAILED` lines in its output are the coaster-pictures self-test's cases that are meant to fail.
