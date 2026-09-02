---
name: maclado-family-facts
description: Family 3 (9-fold maclado) results by decision id — divisor trick, symmetric field, chain continuum, quantization, overlap regimes, welded woven-overlap orb — and the still-open taste call
metadata:
  type: project
---

Family 3 is the 9-spike "maclado" orb after Ángel María Martín López (design doc `docs/maclado-orb-design.md`, survey in `docs/research/`). Load-bearing theorem: polyhedral site symmetry is only 2/3/4/5, so no polyhedral 9-fold axis exists — but the **divisor trick** (3 | 9) sits a 9-wheel on an icosahedral 3-fold axis with 30 exact tip joins and 12 congruent 30-gon fillers (M4, bikar #88 `d20e3f5`; corrected the doc's own over-hardened §2). Cap half-angle acos(√5/3)/2 ≈ 20.905°; solid genus 379; weave 46 strands/390 crossings. Presets `Maclado-9`, `Maclado-9-Weave`, `Maclado-9-Overlap`.

- **D-030** (bikar #91 `0fe0cea`): a greedy chain's separations are a continuum → 34 gap tiles, 33 classes; a successor rule must quantize separations by construction.
- **D-031** (bikar #92 `ec4518b`): lattice walks on the dodecahedral site set quantize (5 separations; 18-wheel walk → 4 classes). No orb shipped.
- **D-032** (bikar #93 `f7bddb7`): tangency touches, overlap weaves, both need phase; ρ 1.15–1.25 gives all 30 pairs two transversal crossings and degree-4 nodes.
- **D-033** (bikar #94 `f3cb04c`): welded woven-overlap orb built — 60 loops over 420 crossings, parity solves.
- **D-040/D-044**: overlap band two unprintable; overlap without weave is a kernel impossibility ([[woven-orb-clearance]], [[orb-kernel-facts]]).

**Open (user's taste call, recorded in D-049):** building an orb on the D-031 walk — the shipped symmetric field already beats it 1 class to 4, so it is not an engineering question.

**Why:** these ids are what any future Family 3 work must cite; the numbers above are the ones docs re-derive.
