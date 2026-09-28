---
name: review-md-comment-loop
description: When Omar says he left comments "in the wiki"/Obsidian, they are review-md threads — pull them with the `reviews` CLI, answer each with a reply, resolve only what is done; never hand-edit the .comments.md files
metadata:
  type: reference
---

Omar reviews docs in Obsidian (vault = this repo's `docs/`) with the review-md plugin. Each
commented doc gets a sidecar `docs/.<name>.comments.md` (untracked, in the main checkout
`~/Workspace/git/3d-models`), and the commented line carries a block id (`^7rlhya`).

CLI: `~/Workspace/git/review-md/plugins/review-md/bin/reviews`
- `reviews list docs --open` — every open thread (a path argument is required; bare `list` exits 2).
- `reviews reply <doc> <id> "…" --author claude [--resolve]` — replies go through Obsidian
  (an `obsidian://review-md-reply` URL), so Obsidian must be running; "reply landed" confirms it.

How to work a round: list open threads, do the work in a PR, reply on each thread with what
changed (PR, commit), `--resolve` only when the ask is fully done — leave a thread open when part
of it is deferred (e.g. e7b42d's rename, 2026-09-28). The block ids the plugin adds to the docs are
real edits: commit them with the PR. If a reply turns out wrong, post a correction reply; never
edit the sidecar by hand.

As of 2026-09-28 the plugin is not installed (absent from `~/.claude/plugins/installed_plugins.json`);
only a stale 0.1.0 cache sits in `~/.claude/plugins/cache/review-md/`, whose skill says "there's no
resolve command yet". The source at `~/Workspace/git/review-md` is 0.1.1 and documents `--resolve`
and `reviews resolve`, so read that `skills/reviews/SKILL.md`, not the cache. Omar installs it with
`/plugin marketplace add omars-lab/review-md` then `/plugin install review-md@review-md`
(user-level installs are his to run). Related: [[render-mockups-not-ascii]].
