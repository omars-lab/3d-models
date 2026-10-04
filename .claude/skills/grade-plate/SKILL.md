---
name: grade-plate
description: Grade a plate's maturity — experiment, repeatable or production — from its print history, how full its bed is, and what its prints taught, then write the level onto its page in docs/design/plates/ with a dated promoted or demoted row. Use for "grade this plate", "plate maturity", "is this plate production ready", "is this plate repeatable", "promote a plate", "demote a plate", "can we pack this plate", "is this bed optimized", after a print record's verdicts are judged, after a plate's recipe or layout changes, "change a production plate", "derive a plate", "tweak a production recipe", and when the plates gate reports a P8 finding. Writes `maturity`, `bed_fill`, `recipe_hash` and the timeline row, and derives a new experiment plate for a change to a production one; never ticks an approval and never sends to the printer.
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
   experiment does not need one, and is not asked to be packed. A production page always
   carries one, even while the rubric's bar is 0 (D-098), so an empty bed stays in view.
4. **Write the level.**
   - **Up:** only when the grade shows the higher level. Set `maturity:` and add a timeline row
     `| <today> | promoted to <level>: <the evidence in a line> | this page |`. To production,
     also pin the recipe: `recipe_hash: '<python3 tools/plate_grade.py --recipe-hash <plate>>'`.
     Then write the standing row in its Approvals table:
     `python3 .claude/skills/manage-approvals/scripts/plate_approve.py docs/design/plates/<plate>.md --standing` (D-096). From then on
     the plate goes out on its standing approval (D-095), and its recipe is frozen.
   - **Down:** when the grade shows less than the page says (the gate will already be failing).
     Lower `maturity:` and add `| <today> | demoted to <level>: <what changed> | this page |` —
     a new verdict, a recipe change, a repack, or a stricter rubric.
   - **Under-claim:** when the prints would carry more than the page says, the gate prints a
     notice. Leave it unless Omar wants it promoted: keeping an experiment an experiment is
     their call, and never wrong.
5. **Production means proven as laid out.** A plate going to production is `kind: repeat`, and
   its latest run printed the counts its recipe holds now. The rubric's fill bar decides whether
   it must also be packed; it is 0 since D-098 (phones-02, 2026-10-04), so today it need not be.
   When the bar is above 0, repacking to reach it changes the counts, so the plate stays
   repeatable until the packed layout prints clean once — say so on the page and queue that
   print through prioritize-prints.
6. **Check.** `python3 .claude/gates/plates_gate.py` must be clean; `--write` rewrites the queue
   if a page edit moved it.

## Changing a production plate

A production plate's recipe does not change in place (D-095, Omar: "recipe change should be in a
new experimental plate derived from a prod plate"). Editing it would send an untried layout on a
standing approval, so the gate fails on a recipe that no longer matches the page's `recipe_hash`
and the send check refuses it. Instead:

1. **Derive.** `python3 tools/plate_grade.py --derive <parent> <new> --answers "<what the change
   tests>"`. It copies the recipe to `<new>.yaml` and writes `<new>.md`: an unapproved experiment
   with `derived_from: <parent>` and the parent's bets, cost and risk. It refuses a parent that
   is not production.
2. **Change and say it.** Make the change in `<new>.yaml`, and fill the page's "What changes"
   section: what changed and why. Slice it and replace the copied cost; add a picture before it
   goes to Omar, as for any plate (prioritize-prints).
3. **Print it as an experiment.** It needs Omar's yes per send like any experiment, and its
   pieces earn their keeps on their own records.
4. **Promote, then retire.** When the grade shows the derived plate at production, promote it
   (with its `recipe_hash`) and set the parent's `stage: retired` with a `retired` row naming the
   plate that replaced it. Until then the parent keeps printing as it was.

A mistaken edit to a production recipe is undone by putting the file back, not by re-pinning the
hash; re-pinning would put an untried recipe on the standing approval.

## Never

- Never tick an Approve box, write an `approved` row, or send. Below production every send needs an
  open `approved` row in the Approvals table, one per send (D-093, D-096); the only row this skill
  writes is the `standing` one on promotion, and the standing approval (D-095) is still read at
  send time from this grade.
- Never re-pin `recipe_hash` on a production page to make the gate pass. Derive instead.
- Never promote on a total. Three keeps on one piece and none on another is an experiment.
- Never type a `bed_fill` that did not come from `--fill` on a slice of the current recipe.

## Changing the bar

A grade that looks wrong is a rubric change, not an exception on one page: change the number in
`rubric.md`, add a round-log line saying why, and run the gate — it names every page the change
moved.
