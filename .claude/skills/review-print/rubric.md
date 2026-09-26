# Print review — what a piece must be before it is printed

Read by the [review-print](SKILL.md) skill every run. Each check says where it came from; add
one when a print teaches something new.

## The checks, looking at the top-down sheet

1. **It reads as the pattern at the size it prints.** The holes are the point of an openwork
   piece. A near-solid disc with pinholes is not a sample of the pattern; it is a disc. (sDO9,
   nmEj on minis-03, 2026-09-25: "mostly solid disks are not good coasters".)
2. **The art fills its shape.** The pattern reaches the frame all the way round. Look for:
   - big bare wedges between the art and the corners;
   - a patch of the pattern floating in an empty field;
   - a half-filled outline.

   These read as unfinished. (n3Ii: "felt incomplete"; lEfW and tA8e: "lots of weird empty
   space"; same plate.)
3. **The holes are evenly spread.** A few holes much bigger than the rest usually means
   missing art, not design. Compare them with the pattern's own full-size render before you
   decide.
4. **It is a good object in the hand.** Ask whether Omar would pick it up and keep it. For a
   coaster that means a flat, steady top with the pattern clearly visible. For a sample it
   means it answers the question it was printed for.
5. **Completeness never outranks a good piece.** "Every pattern represented" is not a reason to
   print one that fails 1–4. (The minis-03 mistake: the failing renders were already on disk.)

## What the numbers catch

`tools/print_review.py` numbers, measured on 2026-09-25 over the minis-03 candidates at size
40 and strap 1.6 (sDO9 at 60, nmEj at 70). Verdicts are Omar's.

| piece | open | biggest | bare | verdict |
|---|---|---|---|---|
| CS-1 minimal-frame | 0.25 | 0.01 | 0.00 | print |
| CS-1 minimal-pegs | 0.13 | 0.00 | 0.00 | print (the wide dovetail frame lowers `open`) |
| CS-2 minimal-frame | 0.23 | 0.01 | 0.00 | print |
| rDux minimal-frame | 0.21 | 0.01 | 0.00 | print |
| lEfW minimal-frame | 0.37 | 0.07 | 0.08 | left off: empty space |
| tA8e minimal-frame | 0.36 | 0.02 | 0.00 | left off: empty space |
| n3Ii minimal-frame | 0.36 | 0.08 | 0.03 | left off: incomplete |
| sDO9 minimal-frame @60 | 0.14 | 0.01 | 0.00 | left off: near-solid |
| nmEj minimal-frame @70 | 0.09 | 0.00 | 0.00 | left off: near-solid |

What the table shows:

- **`biggest` ≥ 0.05 flagged both gross gaps** (lEfW, n3Ii). The good pieces all sit at 0.01.
- **`open` ≤ 0.15 flagged both near-solid pieces.** It also flags the pegs piece, whose wide
  frame adds material that has nothing to do with the art. On a pegs or wide-frame style, read
  `open` against the same pattern's minimal-frame instead.
- **Nothing flagged tA8e.** Its wedges are about the size of its real holes. A high `open`
  (0.36) on a piece with few holes (36) is a hint, not a rule: lEfW and n3Ii share it.

These flags are hints for the eye, not a gate: nine pieces is too few to set a pass line. Re-measure
when new verdicts come in and move the flags here.
