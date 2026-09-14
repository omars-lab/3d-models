# Per-print rubric (read at run time)

The CLI and the skill read this file when preparing a plate, so it can sharpen without either
changing. It answers three questions before any slice or dispatch.

## 1. Is this a prototype or decoration?

Restate the questions the plate must answer (same discipline as the `prototype` skill). If none is
answerable by looking at or measuring the physical object, it's decoration — say so and stop.

- [ ] What concrete, measurable question does this plate settle?
- [ ] Is it the cheapest print that settles the most downstream questions?
- [ ] Is it blocked by an earlier prototype's unanswered questions?

## 2. Which nozzle / profile?

The X2D is dual-nozzle: a main nozzle for parts and an auxiliary nozzle for supports.

- Single-material part, no support → main nozzle, standard profile.
- Needs easy support removal → dual-nozzle, auxiliary for supports.
- Advanced material (needs the heated chamber) → confirm the material profile before slicing.
- Any strut/feature near the FDM minimum → run `bambu validate mesh` first; the min-strut floor is
  bikar's, not the slicer's.

## 3. Is a dispatch justified?

- [ ] Does a settled or open `CAL-*` bet motivate this print? (A coupon that only measures the
      machine/material/nozzle belongs on the machine card, not the prototype catalog.)
- [ ] Is printing currently owner-gated / on hold? If so, a dispatch is a deliberate owner call.
- [ ] Will `--record` capture the geometry pin, the nine-field profile header, and the questions?

If any box is unchecked, prepare the plate but do not dispatch — hand it back for a decision.
