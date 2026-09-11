---
name: breakdown-page-instrument
description: "The per-orb breakdown page and the orb-view instrument it shares files with — why the 2D ribbon projector draws gaps, the re-record order, and the killed display/ shield"
metadata: 
  node_type: memory
  type: project
  originSessionId: 332d42c3-dfe9-490a-9db7-883074290c91
  modified: 2026-09-09T22:13:49.191Z
---

`breakdown.html?orb=<Name>` teaches construction in five beats (flat drawing → base solid → tiling copies → depth-cued turntable → live viewer), parameterised by the manifest, zero per-orb code; guarded by `.claude/gates/timelapse_gate.py`. Facts that survive:

- The "style human surfaces, keep the gray instrument byte-stable in a `display/` subdirectory" split was **killed by D-041** and executed by D-043 — do not rebuild it. `build/` is gitignored, so orb views are artifacts, not state; the feared three-repo re-record cascade was one repo.
- The 2D ribbon projector draws every pass on a constant shell (`radiusMm ± amplitudeMm`) while the 3D mesh interpolates the offset to zero at corners, so every gap in the drawing is an approximation artifact growing as ~2·amplitude·ρ; paint order was measured correct. The silhouette is wrong in both directions (turntable ribbons overshoot, stage frames stop under the front cap); the renderer comment calling it "a few tenths" is a K10 in a code comment.
- `DEFAULT_FRONT_CAP_MIN_DOT = 0.3` is a detector constraint; applied to display it caps content at 0.954r (D-037). Display frames use back-face cull + painter order by `meanDot`; the terminal `complete` frame is byte-pinned to the shipped view (D-045).
- Instrument re-record order: regenerate → sweep → re-pin composites → **hashes last**. A cell view draws the pattern, not the weave, so amplitude changes move ribbon hashes only.
- Wrap-morph design (`docs/orb-wrap-morph-design.md`): the bend is a radial lerp, not a slerp; J1/J2 byte junctions and polygon-count invariance are the gate rules; wheelfield/preview orbs get `morph: null`. Build is two PRs, bikar first.
- **D-052 (landed 2026-09-09):** `data-orb-base-face` names a TRUE base-polyhedron face only. Wheelfield orbs (`base.faces==0`, no base solid) stamp `data-orb-unit`. The renderer has **two** scaffold stamp layers — the main polygon loop (`buildViewFaceAttrs`, already read `baseIndexKind`) AND the breakdown base-solid *underlay* (`scaffoldElements`, was hardcoded 'face'); fixing one left the drawn cells saying `unit` under a scaffold saying `base-face`. bikar #170 (`c2fa085`) made both family-driven via `OrbViewPlan.baseIndexKind`. T9 (`timelapse_gate.py`) branches on `base.faces==0`: lifted → base-face checks, wheelfield → unit checks + any base-face is a finding. Pivot recorded in `docs/issues/base-face-honesty-scaffold-pivot.md`. The earlier "universal check, no branching" plan was dropped — fixing the producer beat forking the reader.

**Why:** the page has no gate for continuity or coverage, so these are the defects a reader finds first.

**How to apply:** look at the actual render before reasoning ([[bikar-dev-server-and-browser-checks]]); gate rules in [[docs-gate-quirks]].
