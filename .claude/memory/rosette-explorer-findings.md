---
name: rosette-explorer-findings
description: What the rosette→LEGO-pin explorer taught — run the real kernel not a port, measure a roster precondition per entry, param bleed throws, plates are data, the cap keeps the thickest wall
metadata:
  type: project
---

The `/rosette-explorer` page recompiles the canonical `Rosette-N.bkr` live (taken from STARTER_PATTERNS, never re-typed), reads pieces via `faceConstructs`, and runs the real `solveAnchorsOnGlobalGrid` + `ribbedRingPoints` + kernel `anchorability` — it deleted a hand-ported anchor copy because two code paths that disagree ARE the defect. Its one divergence (global baseplate vs piece-local lattice) lives in the kernel, not the page. Source of record: `docs/rosette-pin-explorer-design.md`.

- **Roster precondition measured per entry** (bikar #134 `85269ac`): "flat, origin-centred" was false for tilings (Hex-Tiled compiles at (300, 259.8)); the page recentres on the face bbox and frames from the declared span rather than editing public presets. The cheap "one line each" estimate hid the only real work.
- **Param bleed**: Star-N declares neither `crossover` nor `petal_reach` and `compileToGeometry` THROWS on an unknown override, so dials are cleared before reseeding on a pattern swap.
- **Plates as data** (bikar #141 `571cba2`): `data/plates.json` `{id, studs, mm, brand}`; `brand: nominal` = unmeasured 8 mm × studs; a measured clone plate belongs to CAL-CLB-01; the loader throws on every malformed case instead of falling back.
- **Pin-count cap** (bikar #143 `a4318c9`): keeps the thickest-walled anchors first (the kernel's own `minAnchorWallMm` criterion, not a spatial spread — §11 Q6 forbids a clutch guess). The first draft kept the outermost and turned a wall FAIL into a PASS; the honest invariant is one-directional (a cap never fails a kernel pass) and the test also requires a FAIL→PASS flip so the clause is exercised.
- Grounding audit (3d-models #136): "measured in LG-S1" was a K1 hardening — nothing has printed; every 'measured' must name the record that measured it, and `bets.md`'s `0 measured` is the check.

**Why:** each finding changed the page's design, not just its code.

**How to apply:** adding a roster figure = one line plus the centring/span test passing; decisions behind the page: [[d3-integration-decisions]]; kernel: [[lego-lab-and-ldraw-facts]].
