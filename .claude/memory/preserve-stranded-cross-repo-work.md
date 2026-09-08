---
name: preserve-stranded-cross-repo-work
description: "How to persist stranded/uncommitted work across a shared multi-session checkout without disrupting a live session — isolated worktree for the cherry-pick, check the sibling's own conventions first, verify what actually landed"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 332d42c3-dfe9-490a-9db7-883074290c91
  modified: 2026-09-08T02:03:58.659Z
---

Across bikar/qiyas/3d-models/sacred-patterns a single checkout is often shared by
several sessions, so valuable work goes stranded: a correct commit with no remote
branch and no PR, or memory/doc edits left dirty for days. Preserving it is a
"don't lose anything" obligation, but the naive fixes (switch the shared checkout's
branch, `git push` the stale branch, `git add` everything) either disrupt a live
session or push the wrong thing.

**Tell abandoned from live before touching anything.** Stale mtimes (days old) plus
a memory file's `originSessionId:`/`modified:` frontmatter naming a session that is
gone ⇒ abandoned, safe to persist. Files appearing *mid-operation*, or a recent
mtime ⇒ live: leave it (this is why bikar's `fix/verifier-verdict-line` cf-token
worktree was left untouched — new files kept appearing as I looked).

**Cherry-pick a stranded commit onto origin/main in a NEW worktree, never by
switching the shared checkout.** `git worktree add -b <branch> ../<repo>-<tag>
origin/main` → `git cherry-pick <sha>` → push → PR → merge → `git worktree remove`.
The shared checkout's branch never moves, so a live session there is undisturbed.
(2026-09-02: qiyas `3bed8d8`, a real DEFERRED→RESOLVED status fix with no remote
branch and no PR, was one branch-prune from loss; preserved this way as qiyas #28.)

**Check the sibling repo's own convention before committing into it.** Memory
tracking is *per-repo*: `git ls-tree origin/main -- .claude/memory` — **qiyas keeps
`.claude/memory` untracked** (tracks hooks/plans/settings/skills/state, but zero
memory files, and it is not gitignored — a deliberate convention), whereas
**3d-models tracks its memory** (committed via PR, e.g. #119). So a qiyas memory
checkpoint stays *local only*; don't push it to origin.

**Verify what actually landed, not the tool's noise.** `gh pr merge --squash`
prints a cumulative-looking file list; confirm with `git show --stat <squash-sha>`
on origin/main (qiyas #28 really touched 1 file, though gh's line showed 4).

**Why:** "don't lose anything" and "don't disrupt another session" both bind at
once; the isolated worktree is the one move that satisfies both, and the per-repo
memory convention is the trap that almost pushed local notes to a repo that keeps
them out.

**How to apply:** classify (stale vs live) → isolated worktree → check sibling
convention → PR → verify on origin. Pairs with [[git-and-gh-mechanics]],
[[stacked-pr-stranding]], [[pr-flow-for-all-repos]].
