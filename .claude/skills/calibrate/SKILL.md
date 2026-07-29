---
name: calibrate
description: Turn "no source can decide this — measure it" into an earned number. Use when a grounding audit returns UNGROUNDED on a physical quantity, when a constant in millimetres is about to ship on a literature value, or when two design docs are separately unsure about the same physical property. Harvests unsettled empirical bets, clusters them by the measurement that settles them, designs the coupon, and propagates the reading back into code with its provenance.
---

# Calibrate — earning the numbers only a printer can settle

`ground-design-doc` settles what *sources* can settle. Its audits keep ending on
the same verdict — *no literature can decide this; measure it* — and until this
skill existed, that trail simply stopped. The residue is visible in shipped code:
constants whose comments honestly admit they are placeholders, and nothing that
makes them enumerable, stops them ageing into numbers that merely *look* earned,
or notices that the same quantity is separately unresolved in two documents at
once.

The three skills hand off in a cycle:

```
ground-design-doc  --(UNGROUNDED + empirical)-->  calibrate
        ^                                             |
        |                                     (coupon + print pack)
        |                                             v
        +-------(Appendix B closes)-------  prototype (physical print)
```

The bet registry is `bets.md` next to this file. It is **generated** from
`bikar/packages/core/src/kernel3d/calibration.ts` by
`bikar/scripts/gen-calibration-registry.ts` — regenerate it, never hand-edit it.
The source of truth is the `Calibrated<T>` record on the constant itself, so a
bet cannot drift away from the value it governs.

## Workflows

**Harvest** — sweep three surfaces: design-doc Appendix B + Open Questions,
`prototype/catalog.md` entries, and the generated registry. Classify every
unsettled claim as **EMPIRICAL** (a measurement decides it) or **ARGUED**
(sources or reasoning decide it — that belongs to `ground-design-doc`).
Misfiling an ARGUED claim as a bet is this skill's main failure mode: it buys a
print to answer a question a citation would have answered for free. When a claim
is genuinely ambiguous, leave it untagged and say so; fewer correct bets beat a
full-looking table.

**Cluster** — group bets by *the single measurement that settles them*, not by
the document they came from. Duplicates across docs collapse to one ID. This is
the step that earns the skill its keep: one plate can close entries in five
documents, and without it four coupons get designed to measure one property.
Watch specifically for a quantity that is a property of *(machine, material,
nozzle, profile)* being carried as a property of a clip, a brick, or an orb —
warp and wall floor are not features of your design, and measuring them per
design is measuring the printer four times.

**Design the coupon** — one variable per coupon. A ladder that brackets the
unknown generously, because a ladder that turns out to be centred wrong wastes
the whole print. Identity must be readable from the geometry or the filename.
State the print orientation the measurement assumes: a bridge or an overhang
number means nothing without it, and a coupon printed on its side answers a
different question than the one asked.

**Emit the print pack** — the `.bkr`, the exact CLI line per rung, the
measurement protocol from `protocol.md` (instrument, where on the part, how many
samples), and a blank data sheet to fill at the bench. A coupon shipped without
the protocol produces readings that cannot be compared to the next machine's.

**Measure** — readings come only from the physical object. Never from a slicer
preview, never from a render, never from reasoning about what the number should
be. This is inherited verbatim from `prototype`, and it is the rule most likely
to be quietly broken under time pressure, because a plausible number is always
available. A failed print is a result. A ladder that brackets wrong is a result.

**Propagate** — a reading is not earned until it lands:

- the constant's value is replaced **and** its `provenance.status` flips from
  `provisional` to a full `measured` record naming machine, material, nozzle,
  profile, date, and coupon;
- the design doc's Appendix B entry closes with the measured value;
- the `catalog.md` entry flips and its questions are answered by number;
- `bets.md` is regenerated, not edited;
- commit hashes are cited in both repos.

Until every one of those has happened, the bet is open, whatever the bench
notebook says.

## Rules

- A bet with no coupon is a backlog item, not a finding. Register it OPEN and
  say what apparatus it needs — an honest gap beats an invented coupon.
- A number without a recorded machine, material, and nozzle is anecdote, not
  calibration (bikar Tenet 30). It does not get to replace a placeholder.
- Never delete a lost bet. A measurement that refutes the design is a **success**
  outcome of this skill, as in `ground-design-doc` — bury it and the next person
  re-runs the print.
- Never mark a bet settled from a render. Rendering a coupon proves the
  geometry; only the caliper proves the number.
- A new provisional constant must enter `.calibration-baseline.json` in the same
  commit that introduces it — the baseline is append-blocked and may only
  shrink, so an unbaselined provisional value fails the gate by design.
- Rung ranges authored before a machine exists are **brackets around an unknown**,
  not predictions. Label them so, and log a re-centring as a result rather than
  a mistake.
