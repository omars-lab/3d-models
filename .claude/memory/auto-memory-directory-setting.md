---
name: auto-memory-directory-setting
description: autoMemoryDirectory silently ignores relative paths and checked-in project settings — it needs an absolute or ~/ path in settings.local.json
metadata:
  type: reference
---

`autoMemoryDirectory` (Claude Code 2.1.233) decides where auto-memory is read
and written. Two rules make a plausible-looking value a **silent no-op** — no
warning, memory just keeps landing in the default
`~/.claude/projects/<sanitized-cwd>/memory/`:

1. **Relative paths are rejected.** The normalizer bails on anything that is not
   `path.isAbsolute()`. Only an absolute path, or a `~/`-prefixed one (expanded
   to absolute), survives. A bare `.claude/memory` never resolves.
2. **Checked-in project settings are ignored for security.** The setting's own
   description says so: *"Ignored if set in projectSettings (checked-in
   .claude/settings.json)."* The supported per-project home is
   `.claude/settings.local.json`, which is gitignored here.

Resolution order: policy → flag → (local → project, only when the project is
trusted) → user. `CLAUDE_COWORK_MEMORY_PATH_OVERRIDE` short-circuits all of it.

**Why this was worth writing down:** `~/.claude/settings.json` carried
`"autoMemoryDirectory": ".claude/memory"` since 2026-01-24 and it had never once
taken effect — all 36 project memory dirs sat in the default location, and
nothing said so. A setting that fails closed and silently reads as a
configured system.

**How to apply:** set it in `<repo>/.claude/settings.local.json` with a `~/`
absolute path. This repo (2026-08-16) uses
`"~/Workspace/git/3d-models/.claude/memory"`. The resolved path is memoized per
session on `cwd|trust`, so a change only takes effect in the **next** session.

The global value is still the broken relative one; leaving it there is harmless
but misleading, and pointing it at one absolute path would make all projects
share a single memory dir. See [[3d-models-use-case-hook]] for the other
`.claude/`-tracked-as-project-knowledge convention this repo follows.
