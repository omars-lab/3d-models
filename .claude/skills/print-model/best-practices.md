# print-model best practices (read at run time)

Grounded rules the print-model design doc establishes, **plus our own real examples** as we practice
them. This file is **self-healing**: a defect found on a real plate graduates into an example that
fails-before / passes-after the next plan — the repo's graduation rule
([`CLAUDE.md`](../../../CLAUDE.md), "The graduation rule") applied to printing. Grounded rules and their
hedges are attributed in the print-model design doc (docs/print-model-design.md, PR #191) and its
research file; this file adds *our* data on top.

> **Seeded scaffold (task #31).** The examples below are the ones this project has already produced.
> Task #45 grounds the general rules in full; task #46 wires the self-healing graduation so physical
> findings land here automatically.

## Our examples (real, from this project)

- **Known-good X2D Plate-1 slice trio.** machine `Bambu Lab X2D 0.4 nozzle` · process
  `0.20mm Standard @BBL X2D` · filament `Bambu PLA Basic @BBL X2D 0.4 nozzle`. Slices clean end-to-end
  to an X2D-headed `.3mf` (`printer_model = Bambu Lab X2D`, `nozzle_diameter = 0.4,0.4`). Source: memory
  *bambu-x2d-bringup* and the Plate-1 bench sheet.
- **MC-4 overhang fan → supports OFF.** The calibration fan coupon is sliced deliberately with supports
  off (its whole point is to read unsupported overhang) — a calibration case where the setting is a
  *measurement*, not a choice. Pre-flight eyeballed OK (full 360° funnel, base on bed, flare up).
- **LEGO sources slice clean at 0.4 mm.** `ClassicBrick.stl`, `RosetteBrick.stl`, and `StarBrick.stl`
  all slice by preset name to a valid X2D plate at 0.4 mm — no profile-specific surprise before Plate 2.
- **Loaded filament, read live (2026-09-17).** `bambu filament` read AMS 0 slot 0 =
  PLA Basic · #F5547C · GFA00 · 100%, plus a loaded external `vir_slot`. Confirms the discovery seam the
  filament decision depends on.

## Grounded rules (seed — deepened by #45)

- **Nozzle single-wall floor.** A wall thinner than the chosen nozzle's single-wall floor cannot print;
  catch it before slicing rather than letting the slicer silently drop the wall.
- **Orientation minimizes support, not strength.** Report the layer-line direction as a weakness
  advisory; do not claim strength was optimized (no surveyed tool does it).
- **Defer to the profile.** Infill density/pattern default to the slicer profile; advise a change only
  on a stated cause (load-bearing → denser; display → lighter).
- **Brim/raft is thin-sourced.** Attribute any brim/raft advice to the named community source; never
  assert it bare. When a real plate settles it, replace the community rule with our own datum here.

## The calibration exception

Calibration coupons (`settles: CAL-…`) never take advice from this file: their settings are measurements
fixed by the bench sheet. See [`prototype`](../prototype/SKILL.md) / [`calibrate`](../calibrate/SKILL.md).

## How a finding graduates here (task #46)

1. A plate prints and a defect or a confirmed good setting is observed.
2. The finding is recorded against the print record's `feedback` (design §6).
3. If it is *physical and new*, it becomes an example above with the plate it came from — a rule the
   next plan honors. That is the fails-before / passes-after obligation, applied to printing.
