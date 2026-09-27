# Backlog — grow the print catalog

Loop: [`catalog-expansion.md`](../../../.claude/loop-prompts/catalog-expansion.md). Done
list: [`done.md`](done.md). How to feed it: [the loop README](../../../.claude/loop-prompts/README.md).

Goal, per pass: the [ledger](../../constructions/ledger.md)'s migrated count up by one, or
the queue of screened candidates grown, each with a written GO or NO-GO.

## Open, in ROI order

1. **Oracle FAILs in the ledger, and one cell with no verdict** (runs of 2026-09-27,
   [what each tool printed](../../research/ledger-oracle-runs-2026-09-27.md)).
   - `n3IidKfXE1I` O2 has no verdict: youtube's `naqsh_score.py` treats `ggb_score.py`'s
     FAIL exit (2) as a crash. Once youtube accepts exit 2, re-run `make naqsh-score` and
     record what it prints.
   - Find out why each FAIL fails, then fix the `.bkr` or explain the gap: `n3IidKfXE1I`
     O1 (lines `r_3`, `s_3` missing) and O3 0.133 (the GeoGebra file tiles a field, the
     `.bkr` draws one cell); `nmEjCTzMbDg` O1 (points `R`, `D`, `T` off, and O1 cannot
     compare parabolas, hyperbolas or arcs yet) and O2 (the naqsh drawing shows
     construction circles the export hides); `rDuxHF3xMOc` O2 recall 0.8381 (the export
     draws two full-width construction lines the `.bkr` does not).
2. **The queue is empty.** Fewer than three screened GO candidates, and every construction so
   far comes from one creator (Sarah Brewer). Crawl out from youtube's discovery wiki for new
   creators, fold counts and tilings; screen each and write GO or NO-GO with the date.
3. **frame block (P5.3)** — only if a public GeoGebra file needs one; nothing does yet. Moved
   from the coaster-pipeline backlog on 2026-09-25, where it sat by mistake (board #7).

## Handed to the video loop

GO candidates not yet reconstructed go to the youtube repo's ladder, not here. Name the id
in this list when you hand it on, and move it to item 2's shape when it comes back done.
