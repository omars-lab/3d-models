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

- **hifth remote branches: Omar's call.** Every one of these was merged by a real merge
  commit and is an ancestor of its PR's merge (#103–#127, checked 2026-09-27):
  `archive-tasks-0926`, `decision-pages-hybrids`, `hop-keeps-drawer-down`,
  `look-alike-print-words`, `merge-nudge-hook`, `pitch-next-3` through `-7`, `pitch-next-9`
  through `-15`, `pitch-note-beside`, `verse-drawer` and `word-drawer`. The auto-mode check
  refused to touch hifth while another session was working there. Keep four branches that
  never had a PR (`experience-atlas`, `qul-integration`, `qul-page-diff`, `tafsir-seam`),
  plus `perf-budget` and `pitch-next-16`, which are both checked out.
- **youtube `feat/any-source-video-fetch`**: one unmerged commit from 2026-09-27 (fetch any
  source yt-dlp reads) in the `youtube-video-fetch` worktree. It is either live work or waiting
  for Omar to merge it by hand (youtube has no remote).
- **The shared 3d-models checkout** is 19 behind origin/master and cannot fast-forward. Its
  uncommitted memory edits now match origin/master (the two unique lines landed in this pass's
  PR), so they can be discarded and the checkout fast-forwarded. That checkout belongs to
  whichever session is using it.
