# Backlog — grow the print catalog

Loop: [`catalog-expansion.md`](../../../.claude/loop-prompts/catalog-expansion.md). Done
list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal, per pass: the [ledger](../../constructions/ledger.md)'s migrated count up by one, or
the queue of screened candidates grown, each with a written GO or NO-GO.

## Open, in ROI order

1. **A framed openwork coaster: a solid frame, the pattern's straps standing, holes in the
   empty spaces.** Omar asked for it on 2026-09-25 ("just the pattern with holes in the empty
   spaces, no background behind empty spaces"). The unframed version already ships as the
   `-minimal-coaster` style. `trivet` can't make the framed one: it cuts the relief region, and
   with `relief faces` on CS-1 or CS-2 the face region covers the straps too, so the whole inside
   drops out (tried at size 40: CS-1 kept only the outer frame, CS-2 an empty square ring).
   `trivet` was designed to cut one hole, for example a centre square (bikar
   coaster height-field design doc, CV6b). This needs a kernel option that cuts
   "inside the art, off the straps", plus `-openwork-coaster.bkr` files for CS-1 and CS-2.
   CV6b must still pass: each strap island has to reach the frame. Found by the minis-02 run.
2. **`bknVRSMcLj0` has no ledger row.** youtube reconstructed it (Imamzadeh Isma'il 12-fold
   kite tile, 82/82 steps, mean score 0.877). Migrate it with the `import-construction` skill,
   and find out why nothing flagged the missing row — a check that should have failed.
3. **Blank oracle cells in the ledger** (as of 2026-09-25). Run the check and record the
   verdict it prints; never type one it didn't.
   - O1, O2, O3 all blank: `lEfWSogWscs`, `n3IidKfXE1I`, `nmEjCTzMbDg`, `sDO9fpu76v8`,
     `tA8eSdVx_EQ`.
   - O2, O3 blank: `rDuxHF3xMOc`.
   - O3 blank: `7apC5Q9QS-8`.
4. **The queue is empty.** Fewer than three screened GO candidates, and every construction so
   far comes from one creator (Sarah Brewer). Crawl out from youtube's discovery wiki for new
   creators, fold counts and tilings; screen each and write GO or NO-GO with the date.
5. **frame block (P5.3)** — only if a public GeoGebra file needs one; nothing does yet. Moved
   from the coaster-pipeline backlog on 2026-09-25, where it sat by mistake (board #7).

## Handed to the video loop

GO candidates not yet reconstructed go to the youtube repo's ladder, not here. Name the id
in this list when you hand it on, and move it to item 1's shape when it comes back done.
