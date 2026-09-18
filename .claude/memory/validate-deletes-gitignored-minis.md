---
name: validate-deletes-gitignored-minis
description: Before `make validate` in a 3d-models checkout where `make coasters` has run, delete the gitignored `src/Coasters/*-mini.stl` — the pointer gate's two grandfathered mini entries "resolve" when the files exist and the gate then fails the baseline ratchet
metadata:
  type: project
---

`.claude/gates/doc-pointer-baseline.json` grandfathers `src/Coasters/<id>-coaster-mini.stl`
(gitignored build output, `.gitignore` excludes `*-mini.stl`). When a local `make coasters`
has rendered the minis, hook 35 reports those entries as *resolving* and fails, because a
baseline entry that resolves is stale by the ratchet rule. The fix is not to shrink the
baseline (the entries are correct by design) but to remove the build output first:

```
rm -f src/Coasters/*-mini.stl && make validate
```

A fresh worktree off origin/master has no minis and needs nothing (2026-09-17, #255 and
the border-design PR). Related: [[3d-models-deploy]], [[use-cases-refresh-surfaces-anchor-drift]].
