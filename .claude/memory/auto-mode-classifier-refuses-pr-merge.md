---
name: auto-mode-classifier-refuses-pr-merge
description: In auto mode the classifier refuses `gh pr merge` as "Merge Without Review" even after the diff was read; one attempt, then the merge is Omar's
metadata:
  type: feedback
---

The auto-mode permission classifier denies `gh pr merge` with the reason "[Merge Without Review]".
It did so on bikar #368 (twice, 2026-11-03) and 3d-models #872 (once, after `make validate` was
green on the tip). Reading the diff first, or merging a PR this session opened, does not change
the verdict.

**Why:** the denial is about the action class, not the evidence; retrying or rewording the command
is working around a permission, which is not allowed.

**How to apply:** make at most one `gh pr merge` attempt per PR, after validate passes. If refused,
skip the detach, branch delete and fast-forward that would have followed, say so plainly, and put
the merge in the "yours to do" list for Omar with the PR link. See [[owner-gated-and-on-hold]].
