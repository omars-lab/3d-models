---
name: simulate-first-layer
description: Show how a coaster's first layer (the bottom face, where the slits are) will come out before printing, from a local slice — one setting against stock side by side, every piece on a plate one row each, or how far those numbers have tracked Omar's verdicts on printed plates. Use for "what would 75% overlap do to the bottom", "simulate this setting", "will this plate's bottom have slits", "redo the planned-slit table", "check the bottom before we send", "how much do we trust the slicer's drawing", and when iterate-first-layer calls it. It measures the slicer's plan, not the print, and every number goes out with calibrate's agreement line. Slices locally only; never sends to the printer. For rounds of new ideas, use iterate-first-layer.
---

# simulate-first-layer — the bottom face, as the slicer plans it

Built 2026-10-14 for Omar's ask: "is there a way we can simulate the slits and iterate on designs via
simulation" and, as its own skill, "we should have a dedicated simlation skill as well". The loop that
uses it is [iterate-first-layer](../iterate-first-layer/SKILL.md).

## What it simulates, and what it cannot

**It simulates the slicer's plan, not the print.** It slices locally with Bambu Studio (through
`bambu slice compose`), reads the first layer's moves out of the G-code, draws every line as a bead of
its planned width (`tools/print_review.py`) and counts the bed the beads leave bare
(`tools/bed_face_sweep.py`). Nothing is re-implemented here, and nothing goes to the printer.

**The plan cannot see:**

- **Squash and spread.** How far a bead spreads sideways when it is pressed onto the plate depends on
  the real nozzle height, the flow, the temperature and the speed. A hairline the plan draws may close
  in print, and a line it draws may fall short.
- **Pressure lag at line ends.** A line can start thin and end in a blob. The slits sit exactly at
  line ends.
- **Bed height.** The plate's real height from spot to spot, and the start code's trim per plate.

**The spread model stands in for the first and last, and it is Theory.** `--spread plan` draws each
bead exactly as planned: that is **Plan**. Any number draws each bead
`spread × flow × h / (h − lower)` times its planned width (h the first layer's height, flow the
first-layer flow ratio, lower how much closer the nozzle starts): that is **Theory**, every time. So
spread 1.0 already counts a piece's extra flow and the gold plate's lower start, which `plan` cannot.
Nothing has measured how a real bead spreads.

**Calibrate's agreement line goes with every result.** `run` and `plate` print it first, and anyone
quoting a number from this skill quotes the line with it. A number without it reads as more than it
is.

## How far it tracks the prints (calibrate, 2026-10-14)

`calibrate` re-scores the pieces Omar has compared on bedface-1 to bedface-4
([`judged-pairs.yaml`](judged-pairs.yaml): 15 pairs, his words quoted) and asks, at each reading,
whether the plan ranks each pair the way he did. Two settings within 0.13 points of bare share count
as the same in the plan, the noise the [fill-angle sweep](../../../docs/research/2026-10-14-fill-angle-sweep.md)
measured. **Measured** against his verdicts; the spreads are **Theory**:

| Reading | Pairs ranked as Omar did |
|---|---|
| plan | 4 of 15 |
| spread 1.0 (flow and height counted) | 7 of 15 |
| spread 1.1 | 5 of 15 |
| spread 1.2 | 4 of 15 |

What it gets wrong, read from the pair rows:

- **It over-credits changes to the lines' layout.** Rings, monotonicline and 30% overlap each draw
  far cleaner than stock, and Omar found them the same as stock or worse (`4` and `7` "About the
  same"; `L` worse than `H`; `F` "has more slits" than `Z`; rings `R` "About the same" as `S`).
- **It cannot see squash unless the model adds it.** The plain plan calls every flow and gold-plate
  pair the same; Omar found five of those six better (`W` was "almost identical to J"). Spread 1.0
  gets four of the six right, which is why it scores best. Neither tells `X` from `Y`.
- **No judged pair is drawn alike.** Every pair's plain drawings differ a little, so the
  "drawn alike" group in the line is empty for now.

**Do not trust a ranking from it yet.** At its best it ranks fewer than half of the judged pairs as
Omar did. It is useful to see where on a piece the bare bed sits, and to rule out a variant that leaves
the plan worse than stock; it is not a stand-in for a print. The iterate loop stops at its first step
on these numbers (its rule: more than half, or no round).

**The 0.6% bar.** The plate check passes a piece under 0.6% bare with no pocket of 0.2 sq mm or more.
In the plain plan 6 of the 18 judged pieces pass it (`P`, `2`, `T`, `4`, `F`, `R`), and every one of
them still slit in print. Since the fill-angle sweep fixed the drawing, stock itself reads 0.69% to
0.74%, close to the bar. So passing it says the plan leaves little bare bed, not that the print will
be clean. The bar is not changed here.

## The variant file (`run`)

Every key is optional; the default is the bedface-4 and bedface-5 piece (one 50 mm window of the gBV
coaster), sliced stock.

```yaml
name: overlap-75-flow-110                    # names the output folder
bkr: bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr
params: { strap: 3.75 }                      # merged over the piece's default params
window: 50@13,30
object_settings: { infill_wall_overlap: "75%", initial_layer_flow_ratio: "1.1" }   # per piece
plate_settings: { wall_generator: arachne, wall_loops: "5" }   # whole plate, a process file via -s
lower_mm: 0.0                                # Theory only: a nozzle this much closer to the bed
```

- `object_settings` takes only what compose takes per piece: `bottom_surface_pattern`,
  `infill_wall_overlap`, `initial_layer_flow_ratio`. compose refuses anything else.
- `plate_settings` takes any slicer key; the script reads every value back from the slice and stops
  if one did not hold.
- Stock is sliced with the same `bkr`, `params` and `window` and nothing else, so the two differ only
  by the settings.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/simulate.py run` | Slices one variant and stock alike, scores both at each reading, writes a side-by-side picture per reading and `result.json` under `build/simulate/runs/<name>/` | One setting or one idea against stock, before it goes on a plate | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py run <variant.yaml> [--spread plan,1.0]` |
| `scripts/simulate.py plate` | Every piece on a plate, one row each: settings, turn on the bed, slits, bare share, largest pocket. Takes a recipe (sliced first) or a sliced `.plate.3mf` | A plate page's planned-slit table; a check before a send | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py plate docs/design/plates/<plate>.yaml` |
| `scripts/simulate.py calibrate` | Re-scores every judged pair at each reading and prints the agreement line, a table per reading and the 0.6% bar's record; caches scores in `build/simulate/` | First in every iterate round; after a plate is judged and its pairs are added to `judged-pairs.yaml` | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py calibrate` |
| `scripts/simulate.py --self-test` | Checks piece isolation, the bead drawing at a spread, the model's math, settings read-back, placement and the agreement rules on made-up G-code | After editing the script; `make validate-print-review` runs it | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py --self-test` |

Logs go to `build/simulate/simulate.log`, one line per event with a UTC time, the pid and `ev=`
(`slice_start`, `slice_end`, `slice_timeout`, `score_start`, `score_end`). A slice that hangs is cut
off and logged.

## Keeping it honest

- **Add a pair to `judged-pairs.yaml` when Omar judges a new plate**, with his words exactly, then
  re-run `calibrate`. The agreement line is only as current as the pairs.
- calibrate reads the judged plates' slices from `build/plates/` (in this checkout, else the main
  checkout). It assumes those are the slices that were printed; nothing checks that against the
  sent file.
