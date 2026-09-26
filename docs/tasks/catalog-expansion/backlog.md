# Backlog — grow the print catalog

Loop: [`catalog-expansion.md`](../../../.claude/loop-prompts/catalog-expansion.md). Done
list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal, per pass: the [ledger](../../constructions/ledger.md)'s migrated count up by one, or
the queue of screened candidates grown, each with a written GO or NO-GO.

## Open, in ROI order

1. **Openwork coaster joins with a thinner border.** Omar, 2026-09-26, after minis-04: the
   pegged coasters' border is still too wide; build each option in the
   [joins design](../../coaster-borderless-joins-design.md) except magnets, each selectable
   in the Coaster Lab. One sibling style file per join (`-minimal-frame` none,
   `-minimal-pegs` dovetail and slim dovetail, `-minimal-key`, `-minimal-tab`).
   - **Join row in the Coaster Lab** — switches between a construction's join files and
     keeps size, height, strap and clearance; in review (bikar, branch
     `feat/coaster-lab-join-row`).
   - **Butterfly key** — a notch mid-edge and a separate bow-tie key: an `interlock key`
     clause, the key as its own piece, a fit check (CV-K1). In progress (bikar, branch
     `feat/coaster-key-join`).
   - **Tab into the neighbour's opening** — `interlock tab` and a `-minimal-tab` file. Starts
     after the key lands; both touch the same kernel files.
   - **Join gallery in the Coaster Lab** — one example construction, every join shown side
     by side, mated.
   - **Not now**: bevel overlap, a tray, art carried across the seam, strap-end joints,
     magnets (Omar: "except magnets for now"). Reasons are in the design doc.
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
in this list when you hand it on, and move it to item 2's shape when it comes back done.
