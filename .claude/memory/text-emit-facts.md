---
name: text-emit-facts
description: Text-emit (labelled coupons) facts — the face is Source Code Pro Bold baked from 2.042 for the slashed zero, confusable-charset check BLOCKS, extrude-only labels, make coupons needs BIKAR_DIR at merged main
metadata:
  type: project
---

- The glyph face is Source Code Pro Bold baked from version **2.042**, not the 1.017 installed here (its `zero` feature is empty so `zero.a` is unreachable); shipping `0` is the slashed `zero.a`, one ink island, so the counter check (≥0.4 mm) is the load-bearing one. `bake-glyphs.py --alt CHAR=GLYPHNAME` (D-023, bikar #75 `3a759b5`).
- Confusability policy is **BLOCK** under `--check` (D-025, bikar #78 `29813b8`): `CONFUSABLE_PAIRS` is only `['0','O']` (1/l/I measured apart), so false alarms ≈ 0 and the fix is a rename the author picks — auto-substitution would make the check unfalsifiable.
- The emitter is extrude-only, so on the 26-piece machine card only the 4 flat plates take a label; rods/tubes self-identify by size. Labels sit off-measurand (K10): MC-5's is 0.4 mm deep, bottom-edge-centred; MC-3's clears the blind-bore line.
- `make coupons` uses `BIKAR_DIR` (default the primary checkout, often parked stale); override to a worktree at merged main after `npm run -w @naqshcoffee/bikar-cli build` — verified all 23 rungs match the calibration doc's §7 table.

**Why:** the 2.042 vs 1.017 split and the block policy were both AskUserQuestion decisions; the version numbers are what docs cite.

**How to apply:** literals in text-emit docs are 2.042 numbers; older 1.017 numbers stay under a dated addendum ([[docs-gate-quirks]]). Printing the card is on hold ([[owner-gated-and-on-hold]]).
