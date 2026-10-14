---
name: iterate-first-layer
description: Run rounds of ideas against the coaster's bottom slits in the slicer, before printing — an ideation agent proposes up to three first-layer variants, a simulation agent slices and scores them beside stock with the simulate-first-layer skill, and the main session keeps the ledger of what has been tried and sends the results back for the next round. Use for "try ideas for the slits", "iterate on the first layer", "go back and forth on bottom-slit designs", "run a round", "what else could close the slits", and after a bottom-slit plate is judged. Ends with a dated round record in docs/research/ and a plate proposal through prioritize-prints; never sends to the printer. For one setting or one plate's numbers, use simulate-first-layer instead.
---

# iterate-first-layer — ideas against the bottom slits, tried in the slicer first

Omar asked for this on 2026-10-14: "is there a way we can simulate the slits and iterate on designs
via simulation where we have an ideation agent and simualtion agnet go back and forth? this should be
dirven by a skill of ours", and "our main session should cooridate agents".

This skill is the loop only. It owns no simulator code: every number comes from
`.claude/skills/simulate-first-layer/scripts/simulate.py`, called by its path. How a variant is
sliced and scored, what the numbers mean and what they cannot see is in
[simulate-first-layer](../simulate-first-layer/SKILL.md); read it before the first round.

**What a round can and cannot say.** The simulator measures the slicer's plan, not the print. The
plan has misranked the print three times ([no-slits design §2](../../../docs/design/printing/no-slits-design.md#2-why-the-plan-is-not-the-print)).
So a round narrows which ideas are worth a plate; it never decides that one is clean. Only a print,
judged by Omar, does that.

## The files

- [`tried.yaml`](tried.yaml): the ledger, every idea tried so far, plan or print, with its result
  and where it is recorded. The main session appends to it; nobody edits an old entry.
- [`ideation-rubric.md`](ideation-rubric.md): what the ideation agent may propose and how. At most
  three variants a round, each with a hypothesis, a predicted effect, what it attacks, and whether it
  runs now or needs a tool.

## The loop

The main session coordinates, with the Agent and SendMessage tools (not a Workflow). It holds the
ledger and is the only one that writes to the repo.

**(a) Calibrate first.** Run
`python3 .claude/skills/simulate-first-layer/scripts/simulate.py calibrate`. It prints one agreement
line: how many of the pairs Omar has judged the plan ranks as he did, split into pairs the plain plan
draws differently and pairs it draws the same (those only the spread model can tell apart), and the
spread that agrees best. That line goes at the top of every round report and the round record.

Then read the setup's profile: the slice's setup (`teach-simulator/scripts/fit.py show-setup`) and
its line under `agreement` in `simulate-first-layer/setups/<setup>.yaml`, written by
[teach-simulator](../teach-simulator/SKILL.md). That line goes on top too.

- **Stop** unless the Fitted reading, **held out one plate at a time**, ranks more than half of the
  judged pairs that are not ties as Omar did, **and** at least half of the ties (the profile's
  `agreement.meets_iterate_bar`). Report both lines and the disagreeing pairs instead of running a
  round: the simulator is not tracking the prints, and ideas ranked by it would be ranked by noise.
  A setup with no profile, or one that carries no fit, stops here too. (Until 2026-10-14 the bar was
  "the plain plan or the best spread agrees on more than half of all pairs", scored on the same pairs
  it was read from; a held-out score is the honest one, and the ties are kept apart because a
  reading that calls everything different can never get one.)
- Otherwise the round reads every variant at `plan` and at `fitted`. Name which is which in every
  report: `plan` is **Plan**, any spread is **Theory**, `fitted` is **Fitted**.

**(b) The ideation agent proposes.** Start a fresh `general-purpose` agent (not a fork: it should
not inherit this session's framing). Its prompt:

> Read docs/design/printing/no-slits-design.md, .claude/skills/iterate-first-layer/tried.yaml and
> .claude/skills/iterate-first-layer/ideation-rubric.md. Propose at most three first-layer variants
> for the bedface piece, in the rubric's YAML shape. The goal is a bottom with no slits that Omar
> would sell. Do not run the slicer or the simulator; the simulation agent does. Do not edit files.

Check each variant against the rubric (four parts, a ledger match named, needs-a-tool has no
`variant:` block). Send back any that break a rule; do not fix them yourself. Write each runnable
variant's `variant:` block to `build/simulate/round-<n>/<name>.yaml` (gitignored).

**(c) The simulation agent runs them.** A fork is fine. Its prompt names the variant files and the
spread, and asks it to:

- run `python3 .claude/skills/simulate-first-layer/scripts/simulate.py run <file> --spread plan,fitted`
  for each file;
- open every picture the runs print (Read the PNG) and say what it sees: where the bare bed is
  (strap edges, middles, crossings), and whether it moved from where stock has it;
- report each variant's numbers against stock at each reading, whether the prediction held, and what
  the plan cannot see for this variant: squash and spread, the pressure lag at line ends, the bed
  height, and anything the variant changes off the first layer (the top face, the fits, a flare).

**(d) The main session records and sends back.** Append one `tried.yaml` entry per variant
(`tried: plan`), and one for each needs-a-tool idea (`tried: needs a tool`, the tool named in
`result`). Then send the ideation agent the results with SendMessage, so
round two builds on round one in the same agent.

**(e) Stop** after the round cap (default 3, or what Omar set) or after two rounds in a row with no
gain. A gain is a variant whose bare share, at the reading the round trusts (`fitted`, the one
that met the bar), beats the best so far by more than the tie band calibrate uses (0.13 points). Within the
band is noise.

**(f) Write it up.** Nothing is sent to the printer.

- **The round record**: `docs/research/<date>-first-layer-round-<n>.md`, one per round, under the
  research provenance header (date, produced-by, feeds). The agreement line first; then each variant
  with its hypothesis, prediction, numbers at each reading, what the pictures showed and what the
  plan cannot see; then the needs-a-tool ideas, each as a tool request. Pictures the record shows
  are copied, shrunk, into `docs/research/<date>-first-layer-round-<n>-media/` (build/ is
  gitignored). Label every number **Plan** or **Theory**.
- **The plate proposal**, after the last round: a recipe in `docs/design/plates/` for the variants
  worth a print, the bedface piece (the same window as bedface-4 and bedface-5), two of each, a
  stock pair on the same bed, every piece turned the same way. Per-piece variants share one plate;
  a whole-plate variant needs its own plate, with its stock pair printed on the plate before or after
  it. Slice it, then hand it to [prioritize-prints](../prioritize-prints/SKILL.md) for its page and its
  place in the queue. It waits for Omar's yes like any plate.
- **Report** with the agreement line on top, the variants ranked, and the plate proposal. The ideas
  are the agents'; the call to print is Omar's.

## Scripts — when to use each

This skill has no scripts of its own. It calls the simulator's, by path.

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `simulate-first-layer/scripts/simulate.py calibrate` | Re-scores every judged pair against Omar's verdicts and prints the agreement line | Step (a), at the start of every loop | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py calibrate` |
| `teach-simulator/scripts/fit.py show-setup` | Prints a slice's setup and the profile that matches it, whose held-out line and bar are step (a)'s | Step (a), after calibrate | `python3 .claude/skills/teach-simulator/scripts/fit.py show-setup <plate>` |
| `simulate-first-layer/scripts/simulate.py run` | Slices one variant beside stock and scores both, with a side-by-side picture per reading | Step (c), once per variant file | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py run build/simulate/round-<n>/<name>.yaml --spread plan,fitted` |
| `simulate-first-layer/scripts/simulate.py plate` | Scores every piece on a sliced plate, one row each | Step (f), on the proposed plate before handing it on | `python3 .claude/skills/simulate-first-layer/scripts/simulate.py plate docs/design/plates/<plate>.yaml` |
