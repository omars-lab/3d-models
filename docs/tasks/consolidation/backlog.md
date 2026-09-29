# Backlog — PRs, branches and worktrees

Loop: [`consolidation.md`](../../../.claude/loop-prompts/consolidation.md). Done list:
[`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

This loop's work comes from a fresh stock-take each pass, so most of it never needs writing
down. Write an item here only when a pass has to leave it: a PR waiting on Omar, a branch
another session is still using, a trap that needs a fix in its own PR.

## Open

Last full pass 2026-09-27: 0 open PRs and 0 stashes in all six repos; state in the
[`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.
Left by that pass:

- **The video-loop stack is stranded: Omar's call.** #404 merged into #403's branch, not
  master, which closed #403 and #405 and left #406–#410 on a closed base. None of the eight
  records (`n_ICgwOr6qs` through `A9fefFurD_s`) is on master; all of them are on
  `backlog-A9fefFurD_s`. Asked as call 4a on the
  [2026-09-29 open-calls page](../../working-model/feedback-requests/2026-09-29-open-calls.md).
  If he accepts: cherry-pick the eight commits after `b6870c7` onto one branch off master
  (the 88q line is already there from #402; work that conflict by hand), then close
  #406–#410 and delete the old branches.
- **The shared 3d-models checkout** is 19 behind origin/master and cannot fast-forward. Its
  uncommitted memory edits now match origin/master (the two unique lines landed in this pass's
  PR), so they can be discarded and the checkout fast-forwarded. That checkout belongs to
  whichever session is using it.
