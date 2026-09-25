# Parked — open work no loop owns

Moved here on 2026-09-25 from [`docs/backlog.md`](../../backlog.md) §6, which held the work that
"is not printer-gated". None of the five [loops](../../../.claude/loop-prompts/README.md) is pointed at these. A loop that
takes one on moves it into its own backlog; a loop that finds work nobody owns adds it here.

## LDraw export, never opened in a viewer

`--format ldraw` shipped with Lego Lab P3 (bikar `a10f4f6`, PR #53), and
[`lego-lab-design.md`](../../lego-lab-design.md) §10 records the one thing §14.3 asked for that
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
| Lego Lab §11 Q6 — whether a rib-deflection or bending estimate is worth adding to the grid gate | a decision, then code; calibrating it needs LG-F1 and LG-D1 prints | [`lego-lab-design.md`](../../lego-lab-design.md) §11 Q6 |
| Lego Lab §11 Q8 — widen the grammar to a general two-vector basis so a `.bkr` can make the rhombic lattice | resolved as a label by D-007; the widening is an unbuilt option | [`lego-lab-design.md`](../../lego-lab-design.md) §11 Q8 |
| The `polygon`/`C.mpt` evaluator asymmetry MC-4 had to work around | a bikar issue | [`calibration-design.md`](../../calibration-design.md) §4 |
| No polygon-offset primitive — MC-4's wall thickness co-varies with the angle under test | a bikar feature; MC-4 is the coupon to re-cut first if it lands | [`calibration-design.md`](../../calibration-design.md) §5.4, §8 |

The last two shaped the machine-card coupons and block no print; read them if the first card
comes back hard to read. The third engine gap §6.2 listed, text emit, has since shipped.

## Cross-repo governance

How this repo's decisions log joins a decision hub (Omar's call;
[D-004](../../decisions-log.md) chose the local format), then whether the cross-repo ledger check
should block and bring this repo in, then a studio status page rendered from the repos. The
hub decision gates the other two. Source: bikar's cross-repo-dependencies doc and decision
ledger.
