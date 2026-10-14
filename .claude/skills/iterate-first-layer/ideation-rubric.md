# How the ideation agent proposes first-layer variants

The ideation agent reads this file, [the no-slits design](../../../docs/design/printing/no-slits-design.md)
and [the ledger of what has been tried](tried.yaml) before each round. It answers with at most three
variants, each in the shape below. The main session checks every variant against these rules before
the simulation agent sees it, and sends back any that break one.

## The rules

1. **At most three variants a round.** Fewer is fine. A round of three good ideas beats a round of
   three where one is padding.
2. **Each variant says four things:**
   - **Hypothesis:** why it should leave fewer slits, in one or two sentences.
   - **Predicted effect:** what the simulator should show against stock, in the plan's own terms:
     bare share up or down and by roughly how much, the largest pocket, and where on the piece the
     bare bed should move to (strap edges, strap middles, crossings).
   - **What it attacks**, one or more of:
     - *line ends*: where a fill line stops or turns at a wall and leaves a notch;
     - *leftover width*: the strap is not a whole number of lines wide, and the fraction left over
       has to go somewhere (a seam, a gap-fill line);
     - *crossings*: where two straps meet and no line spacing fits the patch whole;
     - *squash*: how far each bead spreads (flow, height, the plate). The plain plan cannot see
       squash at all, so a variant that only attacks squash is read at the spreads, which are Theory.
   - **Runnable:** one of
     - *now, per piece*: only `bottom_surface_pattern`, `infill_wall_overlap`,
       `initial_layer_flow_ratio`, or a bkr param such as `strap`. It can sit beside stock on one
       plate.
     - *now, whole plate*: any other slicer key, through a process file. It cannot share a plate
       with stock, so a print of it needs its own plate and its stock pair on the plate before or
       after.
     - *needs a tool*: a new compose key, a G-code post-processor, a bikar change to the shape. Say
       which tool. **A needs-a-tool variant is never simulated by hand-waving**: no guessed numbers,
       no "it would probably score". It goes in the round record as a tool request, and the round
       moves on without it.
3. **No re-proposing a ledger entry without saying what is different.** If a variant matches an
   entry in `tried.yaml` (same keys, or the same idea), say which entry and what changed: a new
   value, a new combination, a different piece, a print where there was only a plan. "Try 55% again"
   is not a variant; "55% with no elephant-foot shrink, because 55% moved the notch and the shrink
   sets where the wall sits" is.
4. **Rank by the print, not by the plan.** The plan has misranked the print before (no-slits design
   §2). A variant whose case rests only on a lower bare share in the plan, with nothing about why the
   print would follow, is weak. Say what in the print it would change.
5. **Name the cost.** Every variant says what it may make worse: a ridge, a flared bottom edge,
   looser fits, a different look on the top face, more print time. The product is the coaster in
   the hand; a cleaner bottom that looks or fits worse is not a win.

## The shape of an answer

```yaml
- name: arachne-5-overlap-55          # becomes the output folder; short, no spaces
  hypothesis: ...
  predicted_effect: ...
  attacks: [line ends, leftover width]
  runnable: now, whole plate           # or: now, per piece / needs a tool: <which>
  differs_from_ledger: "Walls-only straps, 5 Arachne walls: adds 55% overlap at the crossings"
  costs: ...
  variant:                             # the simulate.py variant file; left out for needs a tool
    object_settings: { infill_wall_overlap: "55%" }
    plate_settings: { wall_generator: arachne, wall_loops: "5" }
```

The `variant:` block is exactly what `simulate.py run` reads (its keys are in
[simulate-first-layer](../simulate-first-layer/SKILL.md)). The main session writes each one to a
file and hands the files to the simulation agent.
