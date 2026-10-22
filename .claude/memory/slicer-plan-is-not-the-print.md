---
name: slicer-plan-is-not-the-print
description: "bedface-1 (2026-10-11) — a G-code first-layer drawing scoring 0.26% bare vs stock's 1.10% printed no cleaner; never rank a bed-face setting on the plan's bare share alone"
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-11T20:13:44.258Z
---

The bed-face design drew each first layer from the G-code and scored the bare bed. On bedface-1 the house preset (concentric bottom, 30% overlap, 0.42 first line) scored 0.26% bare against stock's 1.10%. In print, Omar found it "about the same" or worse: there were dashes and triangles where two sets of rings meet, down the strap middles and at junctions. The plan had drawn those as specks.

**Why:** the drawing assumes the planned bead width. In print, where rings meet, the line opens up. A narrower line squashes less, and the glacier plate gets no 0.02 mm push. None of these causes is separated yet.

**How to apply:** treat the plan's bare share as a filter for slits the slicer *plans*, never as proof of a clean underside. A bed-face setting needs a print side by side with stock before it rolls out. The four next steps are in `docs/issues/bed-face-preset-failed-in-print.md`. Related: [[look-before-you-print]], [[quality-over-efficiency]].
