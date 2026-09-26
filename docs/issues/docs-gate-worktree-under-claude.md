# Docs gate skipped its grounding rules inside a `.claude/worktrees/` checkout

Found 2026-09-26 while validating `docs/research/coaster-bubble-lettering.md` from an agent
worktree at `<repo>/.claude/worktrees/<name>/`.

## What happened

`make validate-docs` failed its own self-test: "D4 content under a normal path should fire, got
nothing". `is_claude_config()` in `.claude/gates/docs_gate.py` decided whether a file is a
`.claude/` config file (links checked, grounding rules D2–D5 skipped) by looking for `/.claude/`
anywhere in the **absolute** path. In a worktree that lives under `.claude/worktrees/`, every
file's absolute path contains `/.claude/`, so every doc in the tree was treated as config and
D2–D5 were silently skipped. Only the self-test noticed; the whole-tree run reported clean.

## Fix

Judge the path relative to the repo root when the file is inside it: a file is config only when
its first path part inside the repo is `.claude`. Files outside the repo root (the self-test's
throwaway repo) keep the old absolute check. After the fix the self-test passes and the whole-tree
run in the worktree reports no findings.

The self-test's existing case ("D4 content under a normal path should fire") is the test that
fails before the fix and passes after.
