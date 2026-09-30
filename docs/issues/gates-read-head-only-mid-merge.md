---
date: 2026-09-30
---

# Checks that compared with the last commit broke on merges

Found 2026-09-30 while merging master into the prioritize-design branch (3d-models #427). Three
checks here, and one in youtube, compare what is being committed with "the commit before". In
a normal commit that is HEAD. In a merge commit there are two commits before: HEAD (the branch)
and MERGE_HEAD (what is being merged in). Each check read HEAD alone, so work that arrived from
the other side looked new, and was either refused or would have been undone.

## What went wrong in each

- **The use-case map's pin** (hook `20-use-cases`, `.claude/skills/maintain-use-cases/validate.py`).
  The map records one commit of this repo, and the check wants it to be the newest commit
  already on master. Mid-merge it looked only at the branch, so it asked for the branch's old
  starting point. Master's newer pin, which the merge was bringing in, was refused, and the
  merge had to move the pin backwards.
- **The broken-link allowance list** (hook `35-doc-pointers`, `.claude/gates/doc_pointers.py`).
  The list may only shrink. Three entries master had added looked like growth, and the merge
  needed `DOC_POINTERS_BASELINE_MAY_GROW=1` to go through.
- **The cookbook's not-yet list** (hook `47-cookbook`, `.claude/gates/cookbook_coverage.py`)
  has the same only-shrinks rule and the same blind spot. It had not fired yet; it would have
  the first time master listed a new keyword while a branch was open.
- **youtube's run catalog** (fixed earlier the same day in youtube's `run_catalog.py`) thought
  main's 32 newest runs were missing, and its sync would have deleted them.

## The fix

Each check now also reads MERGE_HEAD when a merge is in progress. Something either side already
has is inherited, not new. The pin check takes the newest commit master shares with the merge
being made (`git merge-base origin/master HEAD MERGE_HEAD`). Each has a self-test that builds a
real merge in a scratch repo, and a control that aborts the merge and shows the old answer.

`plan_sync.py` also reads HEAD, but was left alone. It checks that a plan row marked shipped
comes with a new line in the shipped list. A merge brings both from the same side, so reading
HEAD alone already gives the right answer.

## For the next check

A check that compares with "the commit before" must read every commit before: HEAD, and
MERGE_HEAD when `git rev-parse -q --verify MERGE_HEAD` succeeds. Test it on a real merge, not
only on a normal commit. A normal commit never shows the problem.
