---
name: 3d-models-use-case-hook
description: 3d-models pre-commit is a dispatcher (gitleaks + use-case map guard) — commits touching pointer-referenced files block unless the use-case map is restaged; USE_CASES_OK=1 overrides
metadata: 
  node_type: memory
  type: project
  originSessionId: 27e89d38-2159-4b95-9416-70151c40cbd0
  modified: 2026-07-28T05:30:55.776Z
---

3d-models `.githooks/pre-commit` dispatches `.githooks/pre-commit.d/` in order: `10-gitleaks` (secret scan, fails closed) then `20-use-cases` (runs `.claude/skills/maintain-use-cases/validate.py --staged`). Shipped 2026-07-28 (`96b5b75` + `ad4949a`), skill: `maintain-use-cases`.

**Why:** the actor/use-case map (`.claude/skills/maintain-use-cases/use-cases.md`) pins code pointers to per-repo `as_of` hashes (3d-models/bikar/qiyas); the hook keeps pins fresh instead of letting them rot.

**How to apply:** a commit touching a pointer-referenced file (e.g. `Makefile`, `index.html`) BLOCKS unless `use-cases.md` is staged too — update the map, run `validate.py --refresh` (never hand-edit `as_of`), restage; genuinely map-irrelevant edits override once with `USE_CASES_OK=1 git commit`. When the map is staged, its `3d-models` `as_of` must equal HEAD. If a refresh moves the pin past commits that shifted referenced lines, re-aim those pointers in the same commit. `make validate-use-cases` = full check. Shipping a user-facing capability ⇒ add its UC node + table row (see [[islamic-orb-project]]).
