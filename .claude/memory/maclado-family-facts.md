---
name: maclado-family-facts
description: "Family 3 (9-fold maclado) results by decision id — divisor trick, symmetric field, chain continuum, quantization, overlap regimes, welded woven-overlap orb, and the D-031-walk orb shipped as an open shell (D-051)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 792c03e6-3f91-4133-a2ea-35c8bfde5227
  modified: 2026-09-02T15:42:22.753Z
---

Family 3 is the 9-spike "maclado" orb after Ángel María Martín López (design doc `docs/maclado-orb-design.md`, survey in `docs/research/`). Load-bearing theorem: polyhedral site symmetry is only 2/3/4/5, so no polyhedral 9-fold axis exists — but the **divisor trick** (3 | 9) sits a 9-wheel on an icosahedral 3-fold axis with 30 exact tip joins and 12 congruent 30-gon fillers (M4, bikar #88 `d20e3f5`; corrected the doc's own over-hardened §2). Cap half-angle acos(√5/3)/2 ≈ 20.905°; solid genus 379; weave 46 strands/390 crossings. Presets `Maclado-9`, `Maclado-9-Weave`, `Maclado-9-Overlap`.

- **D-030** (bikar #91 `0fe0cea`): a greedy chain's separations are a continuum → 34 gap tiles, 33 classes; a successor rule must quantize separations by construction.
- **D-031** (bikar #92 `ec4518b`): lattice walks on the dodecahedral site set quantize (5 separations; 18-wheel walk → 4 classes). No orb shipped.
- **D-032** (bikar #93 `f7bddb7`): tangency touches, overlap weaves, both need phase; ρ 1.15–1.25 gives all 30 pairs two transversal crossings and degree-4 nodes.
- **D-033** (bikar #94 `f3cb04c`): welded woven-overlap orb built — 60 loops over 420 crossings, parity solves.
- **D-040/D-044**: overlap band two unprintable; overlap without weave is a kernel impossibility ([[woven-orb-clearance]], [[orb-kernel-facts]]).
- **D-051** (bikar #153 kernel + #154 DSL seam; 3d-models integration): the D-031-walk orb shipped as an **18-wheel open shell** — a pierced bowl, 2 of 20 dodecahedral sites left open-mouth, fillers in the walk's congruence classes, rim hemming the mouth, grammar `place rule latticewalk length <n> start <k>`. It is the **only** orb that declares `orb3d` yet decomposes into neither cells nor a weave: `render --format views` refuses it (`projectOrbViewScene` throws "has no cell decomposition"), so it is validated by mesh topology, not 2D views — Lab entry `maclado-9-lattice` carries `qiyasComposite: {cells:null, ribbons:null}` (mesh-only, distinct from a `null` whole-field). That viewless refusal is caught **twice**: bikar's sweep via the `drawsOrbViews` predicate (finer than `declaresOrbViews`), and 3d-models `make orbs` via an open-shell `elif` beside the round-pattern skip, keeping the fail-closed `else`. Build produced **eight detectors, zero instructions** → per D-049 §5, **no orb-creation skill** ([[islamic-orb-project]] process rule). Design doc `docs/maclado-lattice-orb-design.md`, decision `docs/decisions-log.md` D-051.

**Why:** these ids are what any future Family 3 work must cite; the numbers above are the ones docs re-derive.
