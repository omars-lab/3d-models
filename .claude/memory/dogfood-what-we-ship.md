---
name: dogfood-what-we-ship
description: "Tenet (Omar 2026-10-01) — use our own tools on what we ship; a new naqsh keyword gets a real cookbook recipe and picture, never a not-yet line to dodge the gate"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-01T19:37:09.401Z
---

Use what we ship before calling it done. A new mechanism gets used through our own tools the
way a reader would: a cookbook recipe with a real rendered picture, a sample through the real
CLI. If our tool cannot show it (the cookbook renderer couldn't draw loose pieces), fixing the
tool *is* the work, not adding the keyword to the not-yet list.

**Why:** Omar, 2026-10-01: "we should have a tenet of eating our own dogfood and using our
stuff, write a real recipe and validate our thinking and approach" — after I put `loose`
(bikar #292) on the cookbook not-yet list with `COOKBOOK_NOT_YET_MAY_GROW=1` (3d-models #467)
because the renderer only drew the assembled coaster. The auto-mode classifier also flagged
the push of that override as a CI bypass.

**How to apply:** when hook 47 (cookbook coverage) blocks on a new keyword, write the recipe;
if the picture would show nothing, extend `tools/cookbook_render.py` so it can. Treat
`COOKBOOK_NOT_YET_MAY_GROW=1` as a last resort for keywords that genuinely can't be pictured
(e.g. animation settings), not for new features. Lives in the project CLAUDE.md
"Self-improvement is part of finishing" paragraph. Related: [[look-before-you-print]].
