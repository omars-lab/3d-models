---
name: color-switching-costs-time-and-filament
description: Two-color plates on the X2D run far slower than the slicer says and waste filament on the prime tower — measured on phones-01 (2026-10-04); prefer one color per plate
metadata:
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-04T15:12:33.830Z
---

Omar, 2026-10-04, after phones-01 (pink + black, one color swap per layer) finished: "i want the
color swtichign to be saved as a memory - it results in alot more waste and slower prints".

**What phones-01 measured** (from the monitor's log against the slice):
- Slicer said 22 min; the print took about 62 min (sent 12:53, finished 13:55 UTC).
- 22 layers, 22 color swaps (one per layer). Layers ran about 53 min against the slicer's 17.
- About **1.6 min per swap** on average: about 1.0 min for a swap to black, about 2.2 min for a
  swap to pink (each layer time is ±0.6 min, the monitor polls every ~34 s).
- The slicer counts almost none of this: its progress barely moves across a swap.
- On the X2D each color has its own nozzle, so nothing is flushed between colors; the time is the
  nozzle swap, the reheat from standby, and a prime tower pass. The waste is the prime tower,
  printed on every layer that has two colors.

**Why:** a two-color plate costs about three times the slicer's minutes and filament nobody keeps.

**How to apply:**
- Prefer one color per plate. When two colors are wanted, ask whether two single-color plates do it.
- If a plate must have two colors, keep the second color to as few layers as possible (fewer swaps).
- Estimate a two-color plate as slicer minutes + 1.6 min × swaps, and put the swap count and that
  estimate on the plate page, not the slicer's number alone.
- Filament, measured by difference: phones-02 (same phones, pink only, small ones slightly bigger)
  slices at 12 min and 3.46 g against phones-01's 22 min and 4.85 g, so about 1.5 g, roughly a
  third of phones-01, went to the swaps and the prime tower.
- The one-color control: phones-02 printed in about 13 min against its 12 sliced (2026-10-04), so
  the slicer is right for a one-color plate and the gap on phones-01 is the swaps.
- Omar followed this with "i dont want to do multi color plate anymore": one plate, one color,
  picked at the send with `bambu print send --color "#RRGGBB"` (sheets-04g).

Related: [[look-before-you-print]], [[approvals-one-per-send]].
