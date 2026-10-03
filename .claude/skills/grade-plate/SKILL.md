---
name: grade-plate
description: Grade a plate's maturity — experiment, repeatable or production — from its print history, how full its bed is, and what its prints taught, then write the level onto its page in docs/plates/ with a dated promoted or demoted row. Use for "grade this plate", "plate maturity", "is this plate production ready", "is this plate repeatable", "promote a plate", "demote a plate", "can we pack this plate", "is this bed optimized", after a print record's verdicts are judged, after a plate's recipe or layout changes, and when the plates gate reports a P8 finding. Writes `maturity`, `bed_fill` and the timeline row; never ticks an approval and never sends to the printer.
---

# grade-plate — how proven is this plate

Omar asked for this on 2026-10-03: grade a plate "from historic prints, space efficiency of
plate, proven value of prints", with the rule that "prod plates should be optimized, experimental
plates arent". The levels, what each must show, and the calls still open:
[plate-maturity-design](../../../docs/design/printing/plate-maturity-design.md).

The numbers the levels use (how many kept prints make a piece repeatable, how full a production
bed must be) are in [`rubric.md`](rubric.md) — read it every run, since they may have changed.
The plates gate's P8 rule holds what this skill writes, from the same function, so a grade the
tool prints and a check the hook runs cannot disagree.

## Every run

1. **Grade.** `python3 tools/plate_grade.py` grades every page (`--plate <name>` for one, `--json`
   for data). For each plate it prints the level the page says, the level the prints show, the
   per-piece verdicts behind it, its own runs, the bet readings that landed, and the bed fill of
   the local slice when there is one.
2. **Read before you move anything.** Open the records the grade names in `docs/prints/`. A level
   is a claim about every piece: check the pieces the grade lists against the recipe, not the
   totals.
3. **Measure the bed** when the page is, or is about to be, production: slice the plate
   (`bambu slice compose`), then `python3 tools/plate_grade.py --fill build/plates/<plate>.plate.3mf`,
   and copy `fill` onto the page as `bed_fill`, the way minutes and grams are copied. An
   experiment does not need one, and is not asked to be packed.
4. **Write the level.**
   - **Up:** only when the grade shows the higher level. Set `maturity:` and add a timeline row
     `| <today> | promoted | to <level>: <the evidence in a line> | this page |`.
   - **Down:** when the grade shows less than the page says (the gate will already be failing).
     Lower `maturity:` and add `| <today> | demoted | to <level>: <what changed> | this page |` —
     a new verdict, a recipe change, a repack, or a stricter rubric.
   - **Under-claim:** when the prints would carry more than the page says, the gate prints a
     notice. Leave it unless Omar wants it promoted: keeping an experiment an experiment is
     their call, and never wrong.
5. **Production means packed.** A plate going to production is `kind: repeat`, and its latest
   run printed the counts its recipe holds now. Repacking to reach the fill changes the counts,
   so the plate stays repeatable until the packed layout prints clean once — say so on the page
   and queue that print through prioritize-prints.
6. **Check.** `python3 .claude/gates/plates_gate.py` must be clean; `--write` rewrites the queue
   if a page edit moved it.

## Never

- Never tick an Approve box, set `approved: true`, or send. Maturity does not change who says
  yes: every send still needs an `approved` row after the last send (D-093). A standing approval
  for production plates is Omar's open call 1 in the design.
- Never promote on a total. Three keeps on one piece and none on another is an experiment.
- Never type a `bed_fill` that did not come from `--fill` on a slice of the current recipe.

## Changing the bar

A grade that looks wrong is a rubric change, not an exception on one page: change the number in
`rubric.md`, add a round-log line saying why, and run the gate — it names every page the change
moved.
