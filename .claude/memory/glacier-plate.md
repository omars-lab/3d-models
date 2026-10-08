---
name: glacier-plate
description: "The X2D's second build plate is a smooth light-blue \"glacier\" plate (Omar 2026-10-07); the printer reads it as P0101 base 4, like the Textured PEI"
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-07T22:23:09.032Z
---

On 2026-10-07 the bed photo showed a new plate: smooth, light blue, with a honeycomb marker strip
on the right edge, and a second one leaning beside it. Omar: "remeber this new glaciar plate".
It is not the gold, grainy Textured PEI plate of every earlier print, and not the SuperTack I first
guessed.

- The printer reports it as `device.plate.cur_id: P0101`, `base: 4`. That is the same id
  `tools/bambu/src/plate-type.ts` mapped to Textured PEI from one sighting on 2026-10-03, so
  P0101 alone does not tell the two plates apart. Only the bed photo does.
- The CLI's `PLATE_TYPES` has no glacier entry, and Bambu Studio's resources name no "glacier"
  plate either (grep, 2026-10-07).
- Omar on which plate to slice for: "will print on teither" (either). sld-1 went out on the
  glacier plate, sliced `textured_plate`, with the bed verdict's note naming the glacier plate.

- **The X2D would not print on it.** sld-1 stopped before layer 0 with 0500-806E ("Foreign objects
  detected on heatbed") on an empty glacier plate, then 0500-8062 ("print plate marker was not
  detected"). Omar swapped in the gold Textured PEI plate and it ran at once (18:50Z). Bambu
  Studio's X2D profile rules out only the Cool Plate (`not_support_bed_type`), so Studio does have
  smooth plate types for it (Smooth PEI / High Temp, SuperTack). "glacier" names none of them,
  and I have not confirmed who makes this plate.

- **How to print on it (research #604–#606, CLI + skills #607, 2026-10-07):** slice
  `--plate-type hot_plate` (Smooth PEI; Textured lowers the nozzle 0.02 mm), PLA 55 °C, bed
  verdict `--plate-type hot_plate` with a note naming the glacier. `checkPlate` then lets the
  slice through on P0101 with a ⚠ (P0101 is marked `alsoSeenWith`). Foreign Object Detection and
  Type Detection must be off for it and back on for the gold plate; printer-wide (see D-108 below).
- **CLI for the switches (#608, 2026-10-07, Omar "yes command that changes settings"):**
  `bambu options show` (read-only, Studio closed) and `bambu options set foreign-object|plate-type|plate-alignment|displacement on|off`.
  `show` read the X2D live on 2026-10-07 (every option on, AI checks medium), so the bit decode holds.
  Each other `set --yes` still needs his go in chat for that change.
- **The two plate switches are now automatic (D-108, #609, 2026-10-07; Omar: "can you do this
  automatically per our skill? when you look at plates pre print"):** the bed verdict takes
  `--non-bambu` for the glacier, `bambu options for-bed <plate> --yes` switches Foreign Object +
  Type Detection to fit (off for glacier, on for gold), and the send's `options:` line refuses a
  mismatch. First real run 2026-10-07 on sld-1: both switched off, read back ✓ (printer screen not
  yet checked by Omar). That run first read a pre-flag glacier verdict as Bambu's own and sent
  nothing, so since #610 a verdict must say `--bambu-plate` or `--non-bambu`, and `for-bed` and
  the send refuse one that says neither.

**Why:** P0101 alone cannot tell the plates apart; the bed photo is what decides.
**How to apply:** say which plate the photo shows (gold grainy = Textured PEI, smooth blue =
glacier) in every bed verdict note, `--non-bambu` for the glacier and `--bambu-plate` for gold;
follow send-plate step 4. The switches are printer-wide: they stay off until a gold-plate for-bed.
Related: [[bambu-x2d-bringup]], [[bambu-studio-conf-holds-access-code]].
