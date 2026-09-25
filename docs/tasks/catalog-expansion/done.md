# Done — catalog growth

Newest first: date, what shipped, PR. Backlog: [`backlog.md`](backlog.md).

- 2026-09-25 — The gallery has a named card for every coaster style, "<Pattern> · <style>" as the Lab titles them, and `make coasters` fails on a coaster with no card; pegs previews drawn as mated pairs (3d-models, this PR)
- 2026-09-25 — Openwork coasters: `openwork frame <mm>` and the minimal-frame and minimal-pegs styles for CS-1 and CS-2 (bikar #248)

## From the session task board, before the split

Finished work up to 2026-09-25 was kept on one list, `docs/tasks/done.md`, as ten snapshots
of the session task board; its sections were moved here by loop on 2026-09-25 (the file is in
git history). Numbers are the board's task ids, and **the board was renumbered more than
once**, so an id means something only under its snapshot: Snapshot 1's #14 and Snapshot 2's
#14 are different tasks. Each snapshot's own note below says which sequence it uses. Newest
first.

**▸ Snapshot 10 — 2026-09-25 (plates, colour regions, the construction migrations,
the consolidation).** **A fresh id sequence, not a continuation of Snapshot 9.** The
live board was rebuilt from the continuation plan's later phases, so this snapshot's
`#1` is the plate composer and its `#37` is the B′ coords producer, not Snapshot 9's
colour-regions id. Where a title below cites a second number (e.g. "#37 part 2",
"#17 — youtube verdict scripts"), that inner number is the *old* board's id the task
was carried over from. Decisions D-072…D-080 are in the [decisions log](../../decisions-log.md).
Still open on the board at this prune: `#4` (P4.3 print record for minis-01, waits on
a physical print), `#6` (P5.2 standard-size plate, after the CAL-CST-* bets are
measured), `#7` (P5.3 frame block, only if a public GeoGebra fixture needs it), `#9`
(push bikar CI secrets, owner-gated) and `#10` (session-reflect skill, after Omar
reviews the 3d-models #218 design).

### Coaster kernel features
- #20–#24 — twist / helix extrude, T1–T5: lofted-ring solid, the `twist <deg>` statement and its conflict refusal, evaluator + render wiring, CV12 + CAL-CST-08, Lab preset + tests (bikar #217, 42ce6dd); CAL-CST-08 mirrored into the calibrate bets file (3d-models #279, 2c1dbb0; count fix #281, 5ed8031)
- #25 — radial-band colouring: the ring a polygon sits in is a print region, D-078 — design (3d-models #277, 6d67693); `bands` verb (bikar #219, 103caa8); ring colour onto the height field (bikar #220, f68a536); `--format parts` split by ring colour (bikar #221, 2e45cd5)
- #26 — emit-golden fix: `emitBkr` round-trips palette + color blocks (bikar #218, 60b5ff4)
- #28, #30 — rods relief: investigated as a Coaster Lab option, then built as path A, half-round height-field straps (bikar #226, 5a588e5)

### Construction migrations (P5.1)
- #5 — P5.1 umbrella, the five remaining constructions; ledger at 8 migrated / 1 by design / 0 remaining; closed by #29 and #32–#39
- #29 — lEfWSogWscs (Tomb of Itimad ad-Daula): bikar golden (bikar #225, 28f3989); CS-7 standard STL + catalog entry (3d-models #284, 4d7f072)
- #32 — rDuxHF3xMOc, 8-fold star rosette with Sequences: list-literal transforms lowered (bikar #227, 2da2e68); CS-8 (3d-models #287, eadf605)
- #33 — sDO9fpu76v8, Royal Alcazar pattern (bikar #228, cc35d6d); CS-11 (3d-models #294, 350d134)
- #34, #38 — nmEjCTzMbDg, n-fold flower, the first open line-art migration, via the B′ self-bootstrapped coords (bikar #243, 87ea3b4); CS-9 (3d-models #291, 34ad03b)
- #35 — n3IidKfXE1I, variable-angled 12-6-4 star rosette (bikar #229, 0191780); CS-10 (3d-models #294, 350d134)
- #36 — the self-improvement loop: each migration fills the gap the last one hit — point reflection (bikar #230), circle inversion (bikar #231), conic loci (bikar #232), arc straps (bikar #233), CircularArc/Circle/Segment lowering (bikar #234); written up as a tenet (3d-models #286, fe0b764)
- #37 — B′: `--emit-coords` / evaluatedCoords, bikar self-bootstraps `cached_coords` (bikar #236, 07f1bf3); decision D-080 (3d-models #290, 265a4e3)
- #39 — the printer emits `connect points`, nmEj's last engine gap (bikar #238, f201377)

**▸ Snapshot 9 — 2026-09-17 (the coaster forms — shape v2, interlock, Coaster Lab,
minimal).** A **continuation of Snapshot 6's constructions board, not of Snapshot
7/8's first-print board**: `#27` and `#30` are the two "agent running" ids Snapshot 6
left open, and `#31`–`#38` were minted on that same sequence afterwards — so this
snapshot's `#33` is coaster shape v2, not an id on the first-print board (Snapshot 7's
`#13` is the blog `.env`). The board is still the plan "GeoGebra constructions →
naqsh (bikar) → STL coasters" (session plan iterative-dazzling-finch), now carried
by its self-contained continuation
[coaster-border-continuation](../../../.claude/plans/coaster-border-continuation.md);
decisions D-065…D-071 in the [decisions log](../../decisions-log.md). Still open on
the board at this prune: `#12` (the later-phases umbrella: P4.x plate composer,
P5.x corpus), `#17` (youtube's O1/O2 verdict scripts on its local `feat/ggb-coords`
until Omar says main), `#21` (CI secrets sync, owner-gated), `#24` (session-reflect
implementation, waits on the `#23` design review), **`#36`** (the coaster border,
D-071: design shipped in 3d-models #257, bikar implementation checkpointed at
f5d1781 on `feat/coaster-border`, validators/importer/docs remaining per the
continuation plan §2) and `#37` (colour regions → per-body export → filament map).

### Phase 2/3 remainder — the first coasters into the catalog
- #27 — P2.7 disc coaster from the GimTvN9hw4U golden: mini `size=40` / standard `size=90`, `--check` both; the importer emits the coaster block itself, `--coaster` beside `--piece` (bikar #207, 05d12ff); the product-side coaster design doc + D-065 (3d-models #227, 6bb053b)
- #30 — P2.5 GeoGebra → naqsh cookbook, held to the importer by a conformance test + the G3 fence glob (bikar #204, 035b0df); P2.4 readability rules + `validate --style constructions` (bikar #206, 1d42690)
- #31 — P3.3 catalog + gallery + `make coasters` for the two migrated coasters, CS-1/CS-2 (3d-models #244, 41a4939)
- #32 — P3.1 `import-construction` skill: GeoGebra construction → naqsh → coaster, rubric read at run time (3d-models #230, 6c06590)

### Coaster forms (D-066…D-070)
- #33 — shape v2: outline fitted to the art (hex / square / octagon), `rotate` and `margin` knobs, CV7 enclosure, the "clipped" claim retracted — design + D-066…D-068 (3d-models #239, 50de1ba); bikar implementation (bikar #208, 48b28b9); CS-1/CS-2 re-vendored from bikar main at shape v2 (3d-models #247, e47ce9a)
- #34 — interlock: self-mating half-edge dovetail on every straight edge, D-069 — design (3d-models #245, 97e6952); bikar grammar `interlock`, slotted ring + exact wall, CV8/CV9, `--interlock` importer flag, CAL-CST-06 (bikar #209, 89b63fd); CS-3 + mated-pair gallery previews, D-069 → built (3d-models #250, 1ab40f2)
- #35 — Coaster Lab in bikar's lab on the Orb Lab pattern, D-067: live structural-check panel, the knobs ARE the param block, roster pinned to `patterns/Constructions/*-coaster.bkr` by a presets test that sweeps mini and standard (bikar #210, 3b7b6f8); vendored into the gallery (3d-models #253, 2f600c3); pointer baseline shrunk once its paths resolved on bikar main (3d-models #254, b33606e)
- #38 — minimal coasters: `outline pattern`, the strap network itself extruded with a rounded top edge and no slab; CAL-CST-07 free-standing floor, CV10 round-over check — design D-070 (3d-models #251, 8688876); bikar (bikar #211, 5152cfd); CS-4 + gallery pair, D-070 → built (3d-models #255, fa86bab)

**▸ Snapshot 6 — 2026-09-17 (the GeoGebra-constructions → naqsh → coaster prune).**
The live board was renumbered again after Snapshot 5, so these ids are a **fresh
sequence**: Snapshot 6's `#8` is the naqsh construction statements, not Snapshot
4/5's cross-repo ledger block, and its `#1` is the worktree setup, not Snapshot 2's
Q5 unstale. The board is the plan "GeoGebra constructions → naqsh (bikar) → STL
coasters, repeatably" (session plan file iterative-dazzling-finch; decisions
D-056…D-064 in the [decisions log](../../decisions-log.md); the record of what is
migrated is the [constructions ledger](../../constructions/ledger.md)). Task ids
`P<phase>.<n>` are the plan's own. Still open on the board at this prune: `#12`
(the later-phases umbrella: P3.1 skill, P3.3 catalog + `make coasters`, P4.x plate
composer, P5.x corpus), `#17` (youtube's O1/O2 verdict scripts sit on its local
`feat/ggb-coords` branch until Omar says main), `#21` (CI secrets sync,
owner-gated), `#24` (session-reflect implementation, waits on the `#23` design
review), `#27` (P2.7 disc coaster + the product-side coaster design doc, agent
running) and `#30` (P2.5 cookbook + P2.4 readability rules, agent running).

### Phase 0 — ground and decide (docs only)
- #1 — P0.5 worktrees: `3d-models-constructions` (also the `THREED_MODELS_DIR` every bikar commit's registry hook reads), `bikar-constructions`, youtube per its CLAUDE.md (commits on `main` only when asked)
- #2 — P0.1 research survey, preserved verbatim under a provenance header (3d-models #187, 18ba47c)
- #3 — P0.2 umbrella design doc — architecture, rubric + option tables, AST contract, ledger, skill; Default/Validator markers green (3d-models #187)
- #4 — P0.3 decisions D-A…D-I appended as D-056…D-064 (3d-models #187) — D-055 was taken by master mid-flight, so the whole block renumbered before merge (memory: decision-id-collision-recurred)
- #5 — P0.4 naqsh names the language, bikar keeps the engine: decision note, doc titles, bikar-dsl skill line, memory naqsh-is-bikar-dsl-synonym (bikar #191, 4c81a52)

### Phase 1 — languages made robust (grammar as source of truth)
- #6 — P1.1 youtube EBNF for `.ggb-commands` + G3-twin conformance test + G2-twin vocabulary fixture; no parser rewrite (youtube main ff58490)
- #7 — P1.3 youtube `--ast-json` + Pydantic schema with a regenerate-and-byte-compare test (youtube main ff58490); schema vendored byte-identical into bikar's qiyas-schema package (bikar #192, c244794)
- #8 — P1.4 naqsh construction statements: (a) named points — `point <id> = …`, bare-name PointRefs, `pick`, a *defined* intersect order (bikar #193, 489758c); (b)–(d) transforms, derived lines/circles, `regular` polygons, rotate inside mirror (bikar #197, 93b0216)
- #9 — P1.5 printer, re-scoped: the first agent looped 9.5 h / 1,348 tool calls / zero files written trying to invert the whole parser for a full-corpus round-trip (memory: subagent-loop-signal); shipped instead as a printer for the statement subset the importer emits, inside bikar #200; the full-corpus round-trip is a follow-on, not a claim
- #10 — P1.2b youtube coordinate oracle: Playwright + GeoGebra Apps API → `coords.json`, `--scad` → OpenSCAD `reference.stl` (youtube `feat/ggb-coords` 86147cb, 16a7202 — local, see `#17`)
- #13 — P1.6 kernel half: height-field coaster kernel, structural validators with hard FAIL fixtures, CAL-CST-01…05 registered, design doc coaster-height-field in bikar (bikar #194, 6c6a54d)
- #26 — P1.6 DSL half: the `coaster` declaration — grammar §10.3, parser, evaluator, `--piece` render, three Tier-0 witnesses, 37 tests (bikar #203, 6b89f6f). Carried finding: CV4 (bottom bevel > 45°) is unexpressible in the surface syntax because `edge` mints an equal rise, so it is exercised only at the validator level; the parser's fall-through keyword list had omitted `mural`
- #19 — P1.7 highlighting generated from one source: bikar tmLanguage + keywords JSON + lab editor overlay, checked in a real browser (bikar #196, 4456607); youtube Prism grammar + keyword mirror byte-identical (youtube `feat/ggb-highlight` aa6cbe8, ed04bbe — local)

### Phase 2 — transpiler, first constructions, oracles
- #11 — P2.1 `bikar import geogebra` (lowering, fail-loud coverage) + P2.2 first slice GimTvN9hw4U golden and fixture (bikar #200, 3c79b46); oracles on the golden: O1 PASS 23/0, O2 PASS (SSIM 0.983), O3 PASS coverage 1.000
- #25 — P2.3 fast coaster: `--piece`/`--depth` emit the slice-1 `piece Coaster` trailer, unit range corrected to 8..25 (bikar #201, 50169f1); mini at unit 9 = 40.5 × 46.8 × 4.0 mm, standard at unit 20 = 90.0 × 103.9 × 4.0 mm, mesh + linkage `--check` PASS on both
- #16 — P2.3b `qiyas mesh compare`, the O3 oracle (qiyas #32, bcd84fa) with the dropped-edge variant as the by-design FAIL; finding carried into the equivalence doc: bikar's extrude solidifies the silhouette, so O3 at the flat stage cannot see interior edges
- #18 — construction-equivalence design doc + measurements research file (3d-models #187) and CAL-EQV-01, the O2 coverage floor (bikar #195, dcbfb40)
- #28 — P2.6 second slice 7apC5Q9QS-8, 144/144 lowered (bikar #202, c1c9063). The O2 recall-0.01 FAIL was two defects: a stale square hero export (guard + issue note on youtube `feat/ggb-coords` 49e7e1a; memory o2-stale-hero-export) and the lowerer drawing exported-and-hidden labels (drawn = exported ∧ ¬hidden, unit test + golden); after both O1 PASS 144/0, O2 PASS 1.000/1.000

### Phase 3 — the ledger
- #20 — P3.2 constructions ledger + gate + hook `44-constructions` + SessionStart nudge, self-tested in a fresh worktree, `M60LJNNslHU` as the "no piece by design" row the gate must not skip (3d-models #206, a0dc2f7)
- #29 — first two migrated rows, verdicts copied from the validators not re-typed, design docs linked (3d-models #219, 73ec316)
