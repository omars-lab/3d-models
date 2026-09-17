---
name: work-conflicts-by-hand
description: Omar's tenet (2026-09-17) — every merge/rebase/cherry-pick conflict is resolved by hand keeping both sides; -X ours/theirs and checkout --ours/--theirs are denied by the guardrail-manager hook block-git-ours-theirs
metadata:
  type: feedback
---

Every conflict is worked by hand: open the file, read both sides, keep both intents,
re-run the gates, `git add <file>` by name, continue. Never `-X ours`/`-X theirs`,
`-s ours`, `checkout/restore --ours/--theirs`, `merge-file --ours/--theirs`, or a
`merge=ours` driver. Never regenerate a conflicted file over the markers, never
close-and-recreate a PR to dodge the conflict (a fresh branch is only the answer to a
denied force-push, see [[force-push-denied-cherry-pick-fresh-branch]]; the conflict is
still worked by hand on that branch).

**Why:** bikar #205 conflicted with #204 in `docs/language-reference.md` (both added a
subsection at the same spot). Resolving by hand kept both; a side-taking strategy would
have silently dropped one PR's docs. Omar: "work all conflicts by hand this should be a
tenant" and "block any git commands that take ours/theirs … in hook".

**How to apply:** the tenet lives in `~/.claude/CLAUDE.md` ("Git in shared working
trees"). The `guardrail-manager` plugin (oeid-claude-plugin-marketplace, v1.2.0) ships
`hooks/block-git-ours-theirs.py`, a PreToolUse Bash hook that returns `permissionDecision:
deny` for those flags, on by default, opt-out only via `.claude/hooks/git-conflicts.conf`
`ENABLED=0`. Selftest: `make test-guardrail-hooks` in the marketplace repo. Related:
[[git-and-gh-mechanics]], [[pr-flow-for-all-repos]].
