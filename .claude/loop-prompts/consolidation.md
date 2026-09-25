# Loop prompt — PRs, branches and worktrees, consolidated with nothing lost

Paste the block below into a fresh session, or run it as `/loop` with no interval so the
session paces itself. Written 2026-09-25. This loop only tidies. The product work is in
[`coaster-pipeline.md`](coaster-pipeline.md), and neither loop does the other's job.

---

## The goal

**Every repo sits on its default branch, plus only the refs that are deliberately kept. Every
finished PR is merged. Every piece of unmerged work has reached the default branch or is
still in progress on purpose. No change is lost in either direction.**

Repos: 3d-models, bikar, qiyas, youtube, sacred-patterns, 3d-model-hub, all under
`~/Workspace/git/`. The last verified state, with the refs that are kept on purpose
(3d-models `gh-pages`, sacred-patterns `gh-pages` and `wip/react-d3-2024`, the
detached `pm` and `master-ro` worktrees), is in
[`branch-state-across-repos`](../memory/branch-state-across-repos.md). The goal is met
when a full pass finds nothing to do, and that memory says so with the date.

## Each pass of the loop

1. **Take stock, from the remote.** In each repo run `git fetch --prune`, then
   `gh pr list`, `git branch -a`, `git worktree list` and `git stash list`. Judge against
   `origin/<default>`, never the local ref, which lags. Before merging anything, check the
   default branch's last CI run or `make validate`
   ([why](../memory/check-main-ci-not-just-the-pr.md)).
2. **Sort each item** and handle the ones that are ready, one at a time:
   - **An open PR.** Review it, merge it (squash), then clean up after it. A draft, or a
     branch another session committed to recently, stays open: leave it and say so.
   - **A branch with no PR.** Diff its content against `origin/<default>` (not
     `git cherry`, which misses squash merges). If nothing is unique, delete it. If
     something is, bring it onto a fresh branch off the default and open a PR.
   - **A worktree.** Remove it only when its branch is merged or empty and it has no
     uncommitted changes. If files are left over, move them to a PR first.
   - **A stash.** Read it. Move what is still wanted to a PR, then drop it.
3. **Cleanup after a merge.** Check that `git diff --stat <branch> origin/<default>` is
   empty. Then `git branch -D` and `git push origin --delete` as two separate commands.
   Fast-forward the local default, and move the detached worktrees to it with
   `checkout --detach`.
4. **Record it.** Add a line to the
   [done list](../../docs/tasks/consolidation/done.md) with the date, counts and PRs. Anything
   left for a later pass (a PR waiting on Omar, a branch still in use) goes in the
   [backlog](../../docs/tasks/consolidation/backlog.md). Update
   [`branch-state-across-repos`](../memory/branch-state-across-repos.md) with the date and
   counts. When a new trap shows up, add it to
   [`git-and-gh-mechanics`](../memory/git-and-gh-mechanics.md).
5. **Wait when nothing is left.** Report the counts in one line, then schedule the next
   wakeup 30 to 60 minutes out.

## Order

Take the item most at risk of losing work first: work on a stale branch that no PR covers,
or a stash. Next come PRs that are ready to merge, oldest first, because every merge makes
the next conflict bigger. Deleting dead refs comes last.

## Never

- Never resolve a conflict with `-X ours`/`-X theirs` or `checkout --ours`/`--theirs`.
  Open the file, keep both sides, re-run the checks
  ([rule](../memory/work-conflicts-by-hand.md)).
- Never switch the shared checkout. Do merges and cherry-picks in their own worktree
  ([how](../memory/preserve-stranded-cross-repo-work.md)).
- Never base a PR on another open PR's branch ([why](../memory/stacked-pr-stranding.md)).
  Never use a range cherry-pick, `git add -A`, `git restore .`, or `--no-verify`.
- Never delete a branch or worktree without proving it holds no unique content.
- Never merge `gh-pages` into master.

Omar's calls: a PR the auto-mode check won't merge unattended, a force push, and any change
to branch protection or repo settings. Name the PR and what it needs, then move on.
