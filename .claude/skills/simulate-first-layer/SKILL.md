---
name: simulate-first-layer
description: Show how a coaster's first layer (the bottom face, where the slits are) will come out before printing, from a local slice — one setting against stock side by side, every piece on a plate one row each, or how far those numbers have tracked Omar's verdicts on printed plates. Use for "what would 75% overlap do to the bottom", "simulate this setting", "will this plate's bottom have slits", "redo the planned-slit table", "check the bottom before we send", "how much do we trust the slicer's drawing", and when iterate-first-layer calls it. It measures the slicer's plan, not the print, and every number goes out with calibrate's agreement line. A Fitted reading, taught on one printer setup's judged prints by teach-simulator, goes out with that setup's held-out line. Slices locally only; never sends to the printer. For rounds of new ideas, use iterate-first-layer.
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
the plan worse than stock; it is not a stand-in for a print. The iterate loop now stops at its first
step unless the Fitted reading, held out one plate at a time, clears its bar (see Fitted, below).

**The 0.6% bar.** The plate check passes a piece under 0.6% bare with no pocket of 0.2 sq mm or more.
In the plain plan 6 of the 18 judged pieces pass it (`P`, `2`, `T`, `4`, `F`, `R`), and every one of
them still slit in print. Since the fill-angle sweep fixed the drawing, stock itself reads 0.69% to
0.74%, close to the bar. So passing it says the plan leaves little bare bed, not that the print will
be clean. The bar is not changed here.

## Fitted: the reading taught on one setup's prints

`--spread fitted` (on by default in `plate` and `calibrate`) draws the **Fitted** reading: the spread
model at a taught spread, then the first stretch of every stroke laid thin, where a line starts and
the pressure lags (and, if taught so, again after every sharp turn). A stroke is what the nozzle lays
from one travel to the next. Its four numbers come from
[teach-simulator](../teach-simulator/SKILL.md), which picks them because they rank the judged pairs
as Omar did. **Fitted is not Measured**: no bead was measured, and its numbers stand only as far as
its held-out score says.

`run` and `plate` print the setup's line (its held-out agreement) before any Fitted number. Quote it
with every Fitted number, as the calibrate line goes with Plan and Theory.

**How far it tracks (2026-10-14, the glacier setup).** Taught on all 13 glacier pairs, Fitted ranks 7
as Omar did, against the plan's 4. Held out one plate at a time it ranks 4, and none of the 4 ties, so
it does not meet the iterate bar. Its first real test is bedface-5, predicted before it prints. The
marks, the fit and the prediction are in the
[fit research](../../../docs/research/2026-10-14-first-layer-fit.md).

### Setups and profiles

A **setup** is the machine, the nozzle, the build plate and the filament. Each has one profile in
[`setups/`](setups/), written by teach-simulator: the fitted numbers, what they were fit on, the
agreement numbers and the date. simulate.py reads the slice's printer, nozzle, plate type and
filament preset from its project settings and uses the profile whose `match` is that setup.

- **No profile matches**: it says so, prints no Fitted reading, and the plain plan stands, labeled
  Plan.
- **The profile carries no fit** (`can_fit: false`): it prints the profile's `why` and the plain
  plan. The textured plate (bedface-3) is one: two pieces, each judged only against a glacier piece,
  and its grain hides the slits in the photos.
- **Two profiles match one slice**: it stops until one is named with `--setup <name>`. The slicer has
  no type for the glacier plate, which is sliced as the High Temp plate, so a slice for Bambu's own
  High Temp plate also matches the glacier profile. Nothing says the glacier fit carries to that
  plate.

A pair whose two pieces printed on different setups (bedface-3's against bedface-2's) is never pooled
into a fit; calibrate scores no Fitted reading for it.

### What Fitted cannot see

- **Anything the judged pieces did not vary.** It was taught on stock, wall overlap, first-layer flow,
  monotonicline and rings on one setup. A change outside that (speed, temperature, a new fill
  pattern, a larger shape) is read by the same four numbers, which nothing has checked there.
- **Pressure as a nozzle has it.** The thin line start is a stand-in fitted to the photos, not a
  model of the extruder; it cannot say how a slower start or a priming move would change the start.
- **The bed's own height, spot to spot, and the plate's surface.** A slit from a low spot is not in
  the model.
- **Whether a gap closes by squash after the second layer.** Like the plan, it reads the first layer
  alone.
- **The tie band.** Fitted carries the plan's 0.13-point band over without measuring its own noise.

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
| `scripts/simulate.py plate` | Every piece on a plate, one row each: settings, turn on the bed, slits, bare share, largest pocket. Takes a recipe (sliced first) or a sliced `.plate.3mf` | A plate page's planned-slit table; a check before a send. Reads Plan and Fitted by default; `--setup <name>` names the profile when two match | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py plate docs/design/plates/<plate>.yaml` |
| `scripts/simulate.py calibrate` | Re-scores every judged pair at each reading and prints the agreement line, a table per reading (Fitted on the pairs its setup was taught on, so not held out) and the 0.6% bar's record; caches scores in `build/simulate/` | First in every iterate round; after a plate is judged and its pairs are added to `judged-pairs.yaml` | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py calibrate` |
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
