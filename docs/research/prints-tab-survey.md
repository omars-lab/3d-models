<!-- Produced 2026-08-28 by Claude (Opus 4.8), local tree measurements only — no web sources. Sources: MEASUREMENT RUNS against the 3d-models tree at 91ad069 and the bikar tree at ref 8dda702 (the ref build/bikar-ref.txt pins). Feeds: docs/prints-tab-design.md (its zero-state and identity claims derive from this file). WHAT WAS RUN: the shell commands quoted verbatim beside each number below; every count is reproducible on the same two refs. -->

# Prints tab — zero-state survey (local measurement)

Measurement date: 2026-08-28. Method: every number here is the output of the
command quoted beside it, run against the working trees at the refs named in the
provenance header. Nothing here is a web claim; nothing here is estimated. The
design doc consumes these as its starting facts — the tab is being designed for a
repository that has recorded **zero prints**, and that emptiness is the load-bearing
condition, not a footnote.

## 1. The register the catalog already offers is empty

The prototype catalog ships an **Iteration log** table per entry — a place to record
what a print taught. Every one of them is empty.

| quantity | value | command (run in `3d-models/`) |
|---|---|---|
| Iteration-log tables in the catalog | 32 | `grep -c 'Iteration log' .claude/skills/prototype/catalog.md` |
| Data rows across all of them | 0 | `grep -cE '^\s*\| *[0-9]+ *\|' .claude/skills/prototype/catalog.md` |

An empty register that no gate measures is exactly the failure
`docs/issue-register-evaluation.md` names: a structure that *looks* like tracking
is occurring while nothing is tracked. The design deletes this divergence rather
than routing a second register around it — the D-041 rule, paid now while the cost
is zero rows.

## 2. Every calibration bet is unsettled — no print has moved a number

The bet registry's generated census line reports that not one bet has been settled
by a measured print. Read verbatim from the tool, it carries 21
<!--count:cal-bets--> registered bets and 21 <!--count:cal-records-->
`Calibrated` records — all provisional, **0 measured**, and 6 bets with no record in
bikar (`grep -nE 'registered bets' .claude/skills/calibrate/bets.md`).

`0 measured` is the number the prints tab exists to change: a settled bet is the
proof that a print happened and taught something. Today there are none.

## 3. The repository has never tracked a photograph

A print record without a photo of the plate is an assertion; the repo has neither.

| quantity | value | command (run in `3d-models/`) |
|---|---|---|
| Tracked `.jpg/.jpeg/.heic/.heif` files | 0 | `git ls-files \| grep -icE '\.(jpg\|jpeg\|heic\|heif)$'` |
| Tracked `.png` files (renders, for contrast) | 1 | `git ls-files \| grep -icE '\.png$'` |

Photos would be the repository's first tracked non-generated binaries. They are
**source, not build output** — `make orbs` wipes `build/`, so a photo committed
there would not survive a rebuild. The design tracks them on master beside their
record.

## 4. Geometry identity is resolvable and stable at the pinned ref

The design's R1 identity rule requires that a run record can pin the exact geometry
it printed — a `.bkr` path plus the blob's `sha256` at a recorded bikar commit — and
that the pin still resolves later. Measured against the ref this repo pins today:

```
$ cat build/bikar-ref.txt
8dda702fc943d1876c56fe14b5b608ed53ea51e8 main

$ (cd ../bikar && git cat-file -p 8dda702:patterns/Coupons/Machine-Card.bkr | shasum -a 256)
fdc100884e34c0aeffc517a5335d3df2ce79d718c9ee8a31a7f4330643d0a0e4

$ (cd ../bikar && shasum -a 256 patterns/Coupons/Machine-Card.bkr)   # worktree, for equality
fdc100884e34c0aeffc517a5335d3df2ce79d718c9ee8a31a7f4330643d0a0e4
```

The blob read back from the pinned commit equals the worktree blob: the identity a
record would pin is exact and re-resolvable, which is what makes R1 checkable at all.
This is the pair the design's worked example (`MC-2` / `CAL-FEA-01`) uses verbatim.

## What was NOT measured here

No prior-art survey of how other tools (PrusaSlicer project notes, Printables
"makes", OctoPrint history) track prints was run for this file — the design does not
lean on one, and a survey drafted from search snippets would violate this repo's
grounding rules. If such a survey is later wanted, it belongs in its own
`docs/research/` file under its own provenance header, recording what was actually
fetched.
