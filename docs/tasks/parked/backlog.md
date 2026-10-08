# Parked — open work no loop owns

Moved here on 2026-09-25 from [`docs/working-model/backlog.md`](../../working-model/backlog.md) §6, which held the work that
"is not printer-gated". None of the five [loops](../../../.claude/loop-prompts/README.md) is pointed at these. A loop that
takes one on moves it into its own backlog; a loop that finds work nobody owns adds it here.

## Pattern catalog vault — step 5, the rest of the bikar library, is next

[`docs/catalog/plan.md`](../../catalog/plan.md) plans the Obsidian vault in `docs/`: one note per
pattern (planned ones too), a generated catalog page, deep links for every picture, review-md
through BRAT, and a check plus a skill that keep it current. Asked for by Omar, 2026-09-27.

Steps 1 to 4 are done (see [done.md](done.md)). The catalog page is
[`docs/catalog/index.md`](../../catalog/index.md); the `pattern-catalog` skill writes it, a
queued pattern gets its note from [`docs/catalog/planned.yaml`](../../catalog/planned.yaml), and
`make validate` fails when bikar has a construction file no note claims.
Step 5 is next: notes for the rest of the bikar library (stars, rosettes, tiled, weave, orbs,
lego, coupons), mostly generated, per [the plan](../../catalog/plan.md#steps-in-order-of-value).

Step 5's size question now has a number: the 36 pictures step 2 committed average 39 kB, 1.4 MB
in all.

## The FAQ — waiting on Omar

The `session-reflect` skill proposed six FAQ candidates in the untracked proposal file in
`docs/`. Omar marks each keep or discard and writes the answers (regenerate the candidates with
`python3 tools/session_reflect.py update-faq`). Then one PR, per that skill, with ids from
`python3 tools/next_id.py next Q`. Never write an FAQ answer yourself. Moved from the
coaster-pipeline backlog on 2026-09-25 (board #10).

## LDraw export, never opened in a viewer

`--format ldraw` shipped with Lego Lab P3 (bikar `a10f4f6`, PR #53), and
[`lego-lab-design.md`](../../design/pieces/lego-lab-design.md) §10 records the one thing §14.3 asked for that
is **not** done: *"no LDraw viewer has opened the output."*
[`research/ldraw-cli-viewers.md`](../../research/ldraw-cli-viewers.md) costs the run. It needs
downloads, not a printer. Five items, the first being the reason to do it soon:

1. LeoCAD's `lcModel::LoadLDraw` appears to drop line types 2–5 into `mFileLines`, read back
   only by `SaveLDraw`. Our MPD is two type-1 lines and 3,764 type-3 triangles, so the
   **predicted** outcome is an empty model and no error. §14.3.1 flags this as a source
   reading, not an observation; some other path reconstituting those lines is not ruled out.
2. LeoCAD's behaviour on an unresolvable reference, and whether it resolves names against
   same-file `0 FILE` blocks.
3. BrickLink Studio on an inline-defined part, on import and round-trip — untouched; nothing
   in the viewer survey predicts it.
4. Whether `0 BFC CERTIFY CCW` is safe to emit — it stays out "until someone looks."
5. LDView's parts-tracker behaviour after a failed lookup — largely dissolved for a
   well-formed file, surviving only for a malformed one.

How to run it, with the hedge intact: nothing LDraw is installed here and the research found
no Homebrew formula for LDView, LeoCAD or Studio, so it starts with a manual download. LDView
with `-VerifyLDrawDir=0` is the candidate, but its macOS off-screen path is claimed on the
strength of `MacOSX/LDView/main.m` alone, rests on deprecated CGL pbuffers, and is untested.
The survey covers twelve named tools, not all LDraw software.

## Open decisions and engine gaps

| Item | What it needs | Source |
|---|---|---|
| Lego Lab §11 Q6 — whether a rib-deflection or bending estimate is worth adding to the grid gate | a decision, then code; calibrating it needs LG-F1 and LG-D1 prints | [`lego-lab-design.md`](../../design/pieces/lego-lab-design.md) §11 Q6 |
| Lego Lab §11 Q8 — widen the grammar to a general two-vector basis so a `.bkr` can make the rhombic lattice | resolved as a label by D-007; the widening is an unbuilt option | [`lego-lab-design.md`](../../design/pieces/lego-lab-design.md) §11 Q8 |
| The `polygon`/`C.mpt` evaluator asymmetry MC-4 had to work around | a bikar issue | [`calibration-design.md`](../../design/printing/calibration-design.md) §4 |
| No polygon-offset primitive — MC-4's wall thickness co-varies with the angle under test | a bikar feature; MC-4 is the coupon to re-cut first if it lands | [`calibration-design.md`](../../design/printing/calibration-design.md) §5.4, §8 |

The last two shaped the machine-card coupons and block no print; read them if the first card
comes back hard to read. The third engine gap §6.2 listed, text emit, has since shipped.

## Merges waiting on Omar

Finished work that a session may not merge itself. Take a line off when it lands.

- **youtube `coaster-0ke` (c8d2b48) and `coaster-n_I` (6e7fc45) into youtube main.** The first
  is the 0ke_GpoBa-s source the ten-fold rosette coaster was imported from (3d-models #583); the
  second is the n_ICgwOr6qs source rewrite and the O1 check for arcs (2026-10-06). A session's
  push to youtube main was refused as a merge without review, so both are Omar's.

Before these: the four youtube branches and 3d-models #427, #432, #433 and #434 merged on
2026-09-30 (#424 and #425 closed, superseded by #427). #430, another session's ledger rows for
ten youtube reconstructions, was approved by Omar the same day. It had fallen behind master, so
it landed through a fresh branch that merged it and worked the conflicts by hand.

## Cross-repo governance

How this repo's decisions log joins a decision hub (Omar's call;
[D-004](../../working-model/decisions-log.md) chose the local format), then whether the cross-repo ledger check
should block and bring this repo in, then a studio status page rendered from the repos. The
hub decision gates the other two. Source: bikar's cross-repo-dependencies doc and decision
ledger.
