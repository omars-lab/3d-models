---
name: teach-simulator
description: Teach simulate-first-layer how one printer setup (machine, nozzle, build plate, filament) lays its first layer, from the bed-face photos and Omar's verdicts on printed pieces — mark where the slits sit in each photo, fit the Fitted reading's few numbers, hold out one plate at a time to score it, write the setup's profile, and write a dated prediction for the next plate before it prints. Use for a new printer, nozzle, build plate or filament; "teach the simulator"; "the simulator disagrees with the print"; "how well does the simulator know this machine"; and after a plate is judged and its pairs are added. Never sends anything to the printer.
---

# teach-simulator — learn one setup's first layer from its prints

Built 2026-10-14 for Omar: "Teach the simulator", "have a teach the simulator skill we cna use later
if we ever change machines", "i iamgin the simulator is learning our sepcific machine /setup".

[simulate-first-layer](../simulate-first-layer/SKILL.md) draws the slicer's plan. The plan cannot see
how the real bead spreads or how it thins where a line starts, and those depend on the machine, the
nozzle, the plate and the filament together: the **setup**. This skill fits a few numbers for one
setup to what Omar saw on its prints, and writes them as that setup's profile in
`simulate-first-layer/setups/<setup>.yaml`. simulate.py then draws a **Fitted** reading for every
slice made for that setup, and says when no profile matches.

**Fitted is not Measured.** Its numbers are chosen because they rank the judged pairs as Omar did;
no bead was measured. Every Fitted number goes out with the profile's agreement line.

## The model it fits

The fewest numbers that can put the bare bed where the photos have it (see
[the marking rubric](marking-rubric.md) and the
[fit research](../../../docs/research/2026-10-14-first-layer-fit.md)):

| Number | What it stands for | Tried |
|---|---|---|
| `spread` | every bead `spread × flow × h / (h − lower)` times its planned width | 1.0, 1.05, 1.1 |
| `pull_mm` | the first this-many mm of every stroke laid thin: the line start, where pressure lags | 0, 0.25, 0.5, 1.0 |
| `thin` | how thin that start is: 1 not laid at all, 0.5 half its width | 0.5, 1.0 |
| `at_turns` | a turn sharper than 60° starts the thin stretch again, as the head slows there | no, yes |

A **stroke** is what the nozzle lays from one travel to the next. `pull_mm` 0 is the spread model
alone: one free number. The pick is the model that ranks the most training pairs as Omar did; a tie
goes to the one with fewer free numbers.

## Steps

1. **Gather the judged pieces.** Every pair Omar compared is in
   [`judged-pairs.yaml`](../simulate-first-layer/judged-pairs.yaml) with his words. Tag each piece
   with its `setup`. Check the tag against the slice: `fit.py show-setup <plate>` prints the slice's
   machine, nozzle, plate type and filament, and `fit` stops if a tagged piece's slice says otherwise.
   The slice cannot tell two plates of one type apart (the glacier plate slices as the High Temp
   plate), so the tag comes from the print record. A pair whose two pieces printed on different
   setups is never fit; `fit` names it in its own row.
2. **Mark the slits in each photo.** Read [marking-rubric.md](marking-rubric.md) first, every time.
   Write each piece's marks into
   [`marked-slits.yaml`](../simulate-first-layer/marked-slits.yaml), then run `marks.py`. It checks
   the file and says whether the marks separate the verdicts: whether slits sit in different places
   by layout, and whether fewer marks line up with Omar's "better".
   **Stop rule:** if every kind of place shows on every layout in like numbers, the marks cannot
   teach a model where the bare bed goes. Ship the marks with that finding, and no fit.
3. **Fit.** `fit.py fit --setup <setup> --pictures <dir>` scores every piece at the plain plan and at
   every model in the grid (cached in `build/simulate/teach/`), picks the model, and prints the pair
   table. Look at the pictures for three or four pieces: the Fitted bare bed should sit where the
   marks put it (wall, middle of a strap, ring seam). Write what you saw in one line.
4. **Hold out one plate at a time and score it.** `fit` does it in the same run: for each plate, the
   model is picked on every other plate's pairs and scored on that plate's. Plates judged against
   each other go out together. It reports agreement on all pairs, on the pairs that are not ties, on
   the ties, and held out; **the held-out score is the one that counts**. One pair out at a time is
   printed too, as a second look. The stop rule's second half: if the held-out score stays at half or
   below, say so plainly, and do not let iterate-first-layer start a round on it.
5. **Write the setup's profile.** `fit.py fit --setup <setup> --write` writes the model, what it was
   fit on, the agreement numbers, the date and the line simulate.py prints beside every Fitted
   number. A setup with too little to fit gets a profile with `can_fit: false` and a `why`, so
   simulate.py says why there is no Fitted reading instead of borrowing another setup's.
6. **Write a dated prediction for the next plate before it prints.**
   `fit.py predict <plate> --setup <setup> --write` ranks the plate's pieces by Fitted bare share,
   fewest first, names them by the ids cut into them, and adds the ranking, dated, to the profile.
   It refuses to rewrite a prediction already there. When Omar judges that plate, add its pairs and
   compare: that is the first test the fit did not choose.

## A new setup

When the printer, nozzle, build plate or filament changes, start a profile by copying the comment
and `match` block of the nearest one in `setups/`, with `match` set to what `fit.py show-setup`
prints for a slice of the new setup, `can_fit: false` and `why: not taught yet`. Until it is taught,
simulate.py shows the plain plan for that setup, labeled Plan. Print a plate of pairs on it (one repeat
of the shape per piece, stock beside one change at a time, as bedface-4 did), have Omar judge
them, and run the steps. Never pool pairs from two setups to get more of them: what one plate teaches
about spread and line starts does not carry to another surface unless a held-out score on the second
says so (K10).

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/marks.py` | Checks `marked-slits.yaml` (every judged piece has an entry, levels 0–3, a reason for every unmarked piece, the photos exist, the reader is named as Claude), then prints the mean slit level by layout and place, the mark totals against each pair, and the stop rule's verdict | Step 2, after marking or re-marking | `python3 .claude/skills/teach-simulator/scripts/marks.py` |
| `scripts/fit.py fit` | Scores the judged pieces of one setup at the plan and every model, picks the model, holds out one plate at a time, prints the tables and the agreement line; `--write` writes the profile, `--pictures` draws plan beside Fitted per piece | Steps 3 to 5; again whenever a plate of that setup is judged | `python3 .claude/skills/teach-simulator/scripts/fit.py fit --setup <setup> [--write] [--pictures DIR]` |
| `scripts/fit.py predict` | The Fitted ranking of a sliced plate's pieces, fewest bare first, by carved id; `--write` adds it, dated, to the profile and never overwrites one | Step 6, before the plate is sent | `python3 .claude/skills/teach-simulator/scripts/fit.py predict <plate> --setup <setup> --write` |
| `scripts/fit.py show-setup` | Prints a slice's machine, nozzle, plate type and filament, as a profile's `match`, and which profile matches it now | Starting a profile for a new setup; checking a piece's tag | `python3 .claude/skills/teach-simulator/scripts/fit.py show-setup <plate>` |
| `--self-test` (both) | fit.py: line starts, strokes, turns, the grid, the tie rule, folds, held-out scoring, the bar, profile matching. marks.py: the file checks and the separation rules. On made-up data | After editing either script; `make validate-print-review` runs both | `python3 .claude/skills/teach-simulator/scripts/fit.py --self-test` |

Logs go to `build/simulate/teach/teach.log`, one line per event with a UTC time, the pid and `ev=`
(`fit_score_start`, `fit_score_progress`, `fit_score_end`).

## Rules

- Never name anything here `calibrate`: that word belongs to `simulate.py calibrate` and the
  `calibrate` skill.
- Label every number by what it is: Plan, Theory (the spread model by hand), Fitted. Never Measured.
- Quote Omar's words exactly; the marks are Claude's reading and say so.
- The 0.6% plate-check bar is not this skill's to move.
