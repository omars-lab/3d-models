# Backlog — PRs, branches and worktrees

Loop: [`consolidation.md`](../../../.claude/loop-prompts/consolidation.md). Done list:
[`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

This loop's work comes from a fresh stock-take each pass, so most of it never needs writing
down. Write an item here only when a pass has to leave it: a PR waiting on Omar, a branch
another session is still using, a trap that needs a fix in its own PR.

## Open

Last full pass 2026-09-25: 0 open PRs and 0 stashes in all six repos; state in the
[`branch-state-across-repos`](../../../.claude/memory/branch-state-across-repos.md) memory.

1. **Push bikar's CI secrets — waiting on Omar.** `make setup-secrets` in bikar needs his
   LastPass login; nothing to do until he runs it. Moved from the coaster-pipeline backlog on
   2026-09-25 (board #9).
2. **A renamed or deleted doc leaves broken links that the commit hook passes.** Hook 30 runs
   `docs_gate.py --staged`, which checks the links *inside* the staged files only. Renaming
   `docs/tasks/parked/done.md` committed cleanly while five links to it in other docs broke;
   only the whole-tree run (`make validate`) found them. Fix: when the staged set renames or
   deletes a file, check the whole tree. Found 2026-09-25 by a test rename.
3. **Links in `.claude/` are never checked.** The whole-tree run covers `docs/**` and
   `CLAUDE.md` only, so a broken link in a loop prompt, skill, plan or memory file ships
   silently (the loop README's link to the renamed file above was not flagged). Fix: add
   `.claude/**/*.md` to D1's link check, and repair whatever it finds first. Found 2026-09-25.
4. **A fresh worktree fails `make validate` until `tools/bambu` has its packages.** Every new
   worktree hits hook 45's "deps not installed" and needs
   `npm ci --prefix tools/bambu`. Fix: have the target install them when they're missing.
   Found 2026-09-25, again.
