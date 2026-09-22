---
title: Grid plate spacing / stretched instances
symptom: Copies on a plate look unevenly spaced, or a re-grid stretches the layout
kind: tolerance
proof: slice-only
first_seen: 2026-09-21
---

# Grid plate spacing / stretched instances

> **Symptom (what you see):** you place N copies of a model on the bed and the spacing looks too tight,
> too sparse, or — after changing the grid shape — the pieces sit in a **stretched** rectangle instead
> of a tidy square arrangement.

## What it means

The even-grid placer spreads instances across the **full bed** on each axis independently. For an
R×C grid on a bed of side `B`:

- pitch (centre-to-centre) = `B / N` per axis (`B/C` across, `B/R` up),
- each centre sits at `pitch · (i + 0.5)`,
- gap between footprints = `pitch − footprint`, and the edge margin = `gap / 2`.

Two consequences follow directly. **Fewer pieces → bigger gaps** (the same bed divided fewer ways), so a
3×3 has much wider spacing than a 5×5 — that is correct, not a bug. And when the grid is **not square**
(rows ≠ cols), the per-axis pitch differs, so the layout is **stretched**: a 2×3 on a 256 mm bed gives a
different pitch across than up. Print *time* is driven by piece **count**, not spacing — wide gaps add
only negligible travel, so "spread them out" does not meaningfully cost time.

## Is it a concern?

**Usually not — but check two things.**

- **Not a concern when** you want display pieces spread across the bed and the gaps are comfortable. Wide
  gaps are free (time-wise) and ease part removal.
- **A concern when** the stretch is unintended (you wanted even spacing and got a rectangle because rows
  ≠ cols) — pick a square-ish grid, or accept the stretch deliberately. Also a concern if pitch drops
  **below the footprint**: the placer refuses that (pieces would overlap), which is the guard firing, not
  a failure.

## What to do

- Want even spacing → choose R and C close to square for the count you want.
- Want them packed tight (less bed, similar time) → a smaller bed value or a denser grid; the placer
  refuses a grid too dense to fit.
- Accept a stretched 2×3 if that is the count you need — it is a valid layout, just non-square.

## Proof — our own prints

- `slice-only`: the egg-grid series — 3×3 (pitch 85.3 mm, gap 55.5, margin 27.8) re-gridded to 2×3
  (pitch 85.3 across × 128.0 up — the intended stretch), plus 4×4 and 5×5, all placed by
  `.claude/skills/print-model/scripts/grid_plate.py` and covered by `grid_plate_test.py`.
- Upgrade to a print-record proof link once a grid plate prints (task #72 / #63).

## See also

- `.claude/skills/print-model/scripts/grid_plate.py` — the placer (and its regression test)
- The `print-model` skill — arrangement reasoning (pack repeats, rotate-to-fit, fill the bed)
