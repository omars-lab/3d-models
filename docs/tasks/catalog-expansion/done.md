# Done — catalog growth

Newest first: date, what shipped, PR. Backlog: [`backlog.md`](backlog.md).

- 2026-10-06 — Loose pieces in an open frame: `loose` now works on an `outline pattern` (minimal) coaster. `--piece Frame` is the plain minimal coaster with the loose spaces left open, the same vertex for vertex, and each piece is as tall as the straps unless `height` says otherwise. On gBV all 41 openings get a piece with a 0.1 mm gap; the slab's edge rule had silently dropped two outer pieces there, so on an open frame a face the frame cannot wall is refused by name instead (bikar #314). The cookbook has a recipe and picture for it
- 2026-10-06 — Loose pieces can be taller or shorter than their pocket: `loose … height <mm>` sets the piece's wall from the pocket floor, left off it sits flush as before, and a peak goes on top of it; a split coaster refuses it (bikar #313). The cookbook has a recipe with a picture at 0.4, 1.2 and 3 mm, and sampler sheet 5's row D, the 1.8 mm piece in a 1.2 mm pocket, no longer waits on bikar
- 2026-10-05 — A Loose button on each filled ring's chip in Coaster Lab (loose-pieces §6 item 4): on, the ring's pieces print loose and the preview lifts them out in their own colors; off, the ring is a solid fill again. It writes the same `loose` line a hand-written file would. The parts list and the guided step bar wait on loose-pieces call 2 (bikar #308)
- 2026-10-02 — Peaked loose pieces, the SKIMS look Omar asked for: `loose … peak <mm>` keeps each piece's outline and wall, then curves the top up to a point over its middle, never overhanging; peak 0 gives the same bytes as before, and a piece that cannot rise to one point from its middle is refused (bikar #298). Shown on a feedback page at 2, 4 and 6 mm (3d-models #476); Omar chose 2 mm and one peaked set on the gBV fit sheet (D-091), so sheets-04 now has `PEAK 2` beside the flat set at 0.15 mm, 62 minutes and 17 g. The cookbook has a recipe and picture for it (3d-models #477)
- 2026-10-02 — A coaster's strap holes are cut on their exact outline, the face moved in by half a strap, sharp at every corner, the same outline the loose pieces are cut from. The traced holes had cut straight across each sharp corner: with the gBV pieces at gap 0.05, 220 of 280 corners were short of the gap, the worst 0.45 mm inside the strap; now none are. Ten coasters with strap holes changed their mesh and all pass the mesh check, and the color split cuts the same holes (bikar #297). sheets-04 is re-sliced on it, 56 minutes and 15 g, and every set keeps exactly its gap: +0.050, +0.100, +0.150 and +0.200 mm, the stars +0.150, where before only GAP 20 cleared
- 2026-10-01 — Sheet 1's row A, today's staircase edge: three 30 mm windows of the old edge (CS-1, CS-2, gBV) rendered once at the commit before the true edges with the window cut copied onto it, kept in `src/Samplers/sheets-01-row-a/` with the patch, the steps and their hashes; a rebuild came out byte for byte the same. `bambu slice sheet` takes a kept STL as a cell and refuses one whose hash has changed, and `print_review.py edge` draws the bottom faces close up, where A's 0.4 mm steps and pinholes show beside B's straight walls. Sheet 1 is built in full and slices to one bed, 1 h 48 m and 46 g; its page waits on Omar's tick (3d-models #471)
- 2026-10-01 — The sampler sheet's card and plate (sampler sheets §5 steps 3 and 4): `Sampler-Cards.bkr` is the labeled card, 138 × 122 × 1.4 mm with every code engraved and none on a sample (bikar #294), and `bambu slice sheet` stands each 30 mm window on its cell as one object, refusing a sample off the card or touching another, judged per sample and per pair. Sheet 1's rows B and C on CS-1, CS-2 and gBV assemble and slice clean headless; row A, today's staircase edge, is still to build, so the sheet is not for printing yet (3d-models #470)
- 2026-10-01 — The window cut for the sampler sheets (sampler sheets §2): `--window <side>[@<x>,<y>]` cuts a square sample out of a finished coaster at its own scale, so a 30 mm window of a 90 mm coaster keeps its 3 mm straps; a window re-fitted to its own side fails the same test, and a window holding the whole coaster gives the same mesh vertex for vertex. A strap the cut detaches is dropped and named; joins, twist, a bottom edge, loose pieces and fins thinner than the floor are refused. Tried with the mesh check on CS-1, CS-2 and gBV, on gBV at round 1.5, and on the CS-2 fill coaster, where it also splits into color parts (bikar #293)
- 2026-10-01 — Loose pieces and the backed frame they drop into (loose-pieces design §6 items 2 and 3, D-090): `loose where <condition> [clearance <mm>]` picks faces the way a fill line does, `--piece Frame` is the coaster with each loose face a pocket down to the slab, and `--piece <color>` gives the pieces, flush with the frame top, the whole gap taken off the piece (default 0.15 mm). The pocket walls follow the exact outline: on CS-1 every one of the 24 pieces has its full 0.150 mm gap at 80 and 90 mm, where the grid staircase touched all 24. gBV gives 41 pieces, the smallest 2.4 mm across; frames and pieces pass the mesh check, and every existing coaster file renders to the same bytes (bikar #292)
- 2026-10-01 — Coaster walls follow the outline between grid points instead of a 0.4 mm staircase (smooth-lines option 3, D-090): each wall is traced where the solid value crosses zero along a grid square's sides. Typical edge error fell from about 0.09 mm to 0.0005 mm, the share of edge more than 0.05 mm off from 65–75% to 3–4%, `tools/edge_stairs.py` shows all six sides of CS-1 straight, all 30 coasters pass the mesh check and CS-1's mirror score rose from 0.971 to 0.998. Star tips narrower than a grid square are still shaved by about 0.2 mm, and interlock insides and relief color boundaries still follow the grid (bikar #291)
- 2026-09-30 — The four facts the prioritize-design skill measures difference from, written for the twelve youtube reconstructions #430 added to the ledger, so every made design now has a row in the skill's `scoring.md` (3d-models #451)
- 2026-09-30 — The loose-pieces design: fills raised above the straps as well as lowered, inner pieces printed loose for a printed frame (three frame kinds), the LP-1 sample plate, and a guided "assemble your own coaster" page ([loose-pieces-design.md](../../design/coaster/loose-pieces-design.md); 3d-models #443). Nothing is built until Omar answers its four calls; the item stays open in the backlog
- 2026-09-30 — The top three candidates built as flat minimal coasters at 90 mm: the Mustansiriya ten-fold star `NtnlGMTElBk` (bikar #285), the 7/4-fold straight-line field `jlTmt_279M4` (bikar #286) and the Itimad-ud-Daula ten-fold rosette `gBV_JTt3Kxk` (bikar #287); shown on the top-three renders page (3d-models #435, D-087), then given ledger rows, catalog notes and gallery cards (3d-models #436). Omar's pick among them stays open in the backlog
- 2026-09-30 — CS-6's "uneven petals" were two centring mistakes, not uneven art. The video and our rebuild are both exactly seven-fold. The symmetry check turned the art about its bounding-box middle, which on a seven-point star sits above the star's real middle, so it scored 0.73. The coaster itself had the same mistake and printed the star 1.94 mm low in its frame. bikar now centres art that turns onto itself on its real middle; the other coasters render to the same bytes (bikar #290). The check now turns about the art's centre of mass, and CS-6 scores 1.00 at order 7 with the coaster re-vendored ([write-up](../../issues/cs6-symmetry-centre.md); 3d-models #453)
- 2026-09-30 — Coaster Lab fill picker, the radial-fill item's missing half (Omar's redirect on thread kpdekz): click a piece in the picture and every piece on its ring lights up, the Orbits row is marked, and a chip offers Fill ring or Clear ring, writing the same `fill void where orbit == N` line the tick writes through the same evaluate path; hover previews a ring, a drag still rotates, and a script whose faces do not line up with the orbits gets no picker rather than a wrong ring. Unit tests for the pick geometry and the piece join, one Playwright test on the radial preset (bikar #288)
- 2026-09-30 — The prioritize-design skill: which pattern becomes a coaster next. Three scores kept apart (appeal and unusual judged from the picture, difference measured by `tools/design_difference.py` from four facts per design against every made coaster in the ledger), a reads-as-a-coaster check read from review-print's rubric, the D-085 total, and a request-feedback page per round; the four-facts table for the twelve made coasters and ten candidates lives in the skill's `scoring.md` (D-086), and hook 49 fails a commit that vendors a coaster without a row (3d-models #437)
- 2026-09-29 — Coaster Lab color controls, steps 6–8 of [color-preview-design.md](../../design/coaster/color-preview-design.md) §10: the Orbits panel with ticks, colors, presets and a Parts row (bikar #282); `fills <mm>` for fills lower than the straps, with a fill-height slider (bikar #283); and the openwork split, so a minimal coaster with filled faces prints as a straps body plus one body per fill color, the top fillet kept (bikar #284)
- 2026-09-29 — Radial fill: the `orbit` word groups a minimal coaster's pieces by their distance from the centre, `fill void where orbit == N` makes chosen rings solid, and filled faces close on minimal coasters, with `GimTvN9hw4U-radial-coaster.bkr` as the radial coaster (bikar #270, D-081). Four CS-1 fill choices were rendered for Omar with captions on the review sheets (3d-models #417); Omar's own pick in the Lab stays open in the backlog
- 2026-09-28 — The thin slivers along the pegs coaster's frame edges were a fold in the mesh: the collar between the dovetail ring and the 0.4 mm grid folded back over the frame top, in every interlocked coaster, and still passed the watertight, Euler and degenerate gates. The collar now pairs each staircase point with its foot on the ring and takes the shortest strip with no folded triangle (bikar #275); the four interlocked STLs here were re-rendered from it (3d-models #389)
- 2026-09-28 — Gallery cards for the five bikar coasters that had none (3d-models #382), and 20 stale vendored coaster files refreshed from bikar main 654fae2 (3d-models #383)
- 2026-09-28 — Colored coaster pictures, steps 1–5 of [color-preview-design.md](../../design/coaster/color-preview-design.md) §10. D-081 groups pieces by orbit and fills chosen orbits on openwork (3d-models #374); two researchers and a checker wrote the design (3d-models #377); three hand-made POCs showed it is only an engine change ([color-poc-2026-09-28.md](../../research/color-poc-2026-09-28.md); 3d-models #379); bikar gained one body-to-color rule in core, the coaster picture as data, and `render --format preview` (bikar #272, #273, #274); and the gallery draws each coaster in its filament colors, with a coaster-pictures check (3d-models #381). Omar's three review threads on the design (7rlhya, e7b42d, leu4yg) were answered in the same round: two new docs-gate rules for wrapped code spans and broken tables, color pictures in the doc, and a rendered Lab mockup in place of an ASCII sketch (3d-models #385)
- 2026-09-28 — The naqsh cookbook in `docs/cookbook/`: a recipe per mechanism with a one-knob picture, the maintain-cookbook skill, and a check that fails when a keyword has neither a recipe nor a not-yet line (3d-models #387); the dovetail recipe drawn at three tab sizes (3d-models #390)
- 2026-09-27 — New construction candidates from creators other than Sarah Brewer, screened by two independent researchers and a checker: 29 ids, 10 GO in rebuild order, the four disagreements settled on the sources ([the consolidated screen](../../research/candidate-screen-2026-09-27.md)); the top three handed to the video loop (3d-models #363, #364, #365)
- 2026-09-27 — Oracle FAILs worked through, in [the FAILs note](../../research/ledger-oracle-fails-2026-09-27.md):
  - `n3IidKfXE1I` had been imported from a draft of its construction. Re-imported from the finished one, it now passes all three checks: O1 PASS 64/0, O2 PASS 1.0/1.0, O3 PASS 1.000. Its coaster draws the open 12-fold rosette, because the whole field was near-solid at 90 mm.
  - `nmEjCTzMbDg`: the rim circles drew only half their outline. That bikar import bug is fixed. Its other cause, a wrong root for `R`, is in the youtube source and proposed there.
  - `rDuxHF3xMOc` O2 is by design: the export shows four bounding lines the coaster cannot draw.

  (bikar #269, 3d-models #361)
- 2026-09-27 — `bknVRSMcLj0`, the Imamzadeh Isma'il 12-fold kite tile, migrated: ninth construction, O1 PASS 79/0, O2 PASS 1.000/1.000, O3 PASS 1.000, coaster vendored as CS-12 (bikar #268). The whole-wall coaster read as a solid gold square at 90 mm, so the coaster now inscribes one repeat cell on a round slab, about 2.3 times larger, through a new importer option `--coaster-omit R6` (bikar #268). The ledger gate now fails when a youtube reconstruction on `main` has no row, or a row is not at the pin — it had only noted a missing row, and only at a pin that predated this one (3d-models #360)
- 2026-09-27 — Ran the three fidelity checks on every blank cell in the constructions ledger and recorded what each printed: 11 PASS, 5 FAIL, and two cells with a written reason (`n3IidKfXE1I` O2, the scorer crashes; `nmEjCTzMbDg` O3, nothing solid to compare); the FAILs and the crash stay in the backlog's "Oracle FAILs" item (3d-models #359)

- 2026-09-27 — Lobed wave outline: a coaster edge of scallops drawn with compass arcs (bikar #266)
- 2026-09-27 — The import-construction skill sends a pasted construction-video link to the youtube repo's video loop instead of treating it as a GeoGebra construction (3d-models #354)
- 2026-09-27 — On a relief coaster a strap cell stays part of the strap instead of being raised with the fill (bikar #263)
- 2026-09-27 — Flush color fills keep their straps and pass the mesh gate (bikar #261)
- 2026-09-26 — Joins sample plate (KEY-1): one mated pair per join on CS-1 at 80 mm, split across [minis-05](../../design/plates/minis-05.yaml) (plain, butterfly key with a 0.05/0.10/0.15 key ladder, tab) and [minis-06](../../design/plates/minis-06.yaml) (dovetail, slim dovetail), every piece through the mesh gate and the review sheet; closes the joins item — the print waits on Omar in the coaster-pipeline backlog
- 2026-09-26 — Margin ruler on every join gallery picture: the solid band between the two patterns, measured off the built mesh and held by a test to two of each file's declared frames within the 0.4 mm grid — none 6.0, dovetail 11.1, slim dovetail 8.4, key 5.7, tab 5.8 mm (bikar #259)
- 2026-09-26 — Tab join: `interlock tab`, a tab on every other hexagon edge whose head drops into the neighbour's pattern opening, fit check CV-T1 (size 55–120 mm), the six-fold minimal-tab coaster, and two pinhole fixes shared with the key (bikar #258)
- 2026-09-26 — Join gallery in the Coaster Lab: "How each join works" opens a card per join, each a picture of two 80 mm six-fold coasters mated as the engine builds them with the seam enlarged, and "Use this join" switches the open coaster; `npm run coaster-join-pairs` draws the pictures and a test holds them to the joins (bikar #257)
- 2026-09-26 — Size chips respect the coaster's range: Mini is dimmed on the butterfly-key coaster (60–120 mm) and says why, instead of producing an error (bikar #256)
- 2026-09-26 — Butterfly key: a notch mid-edge and a separate bow-tie key, `interlock key`, the key as its own piece, fit check CV-K1, and the six-fold minimal-key coaster (bikar #255)
- 2026-09-26 — Join row in the Coaster Lab: switches between a construction's join files (none, dovetail, slim dovetail, key) and keeps size, height and strap (bikar #254)
- 2026-09-26 — Slim dovetail: a `wall` knob on both minimal-pegs coasters (floor 2.1 mm, where CV8 still clears); at neck 2, depth 2, wall 2.1 the frame drops from 5.65 to 4.2 mm and the band between joined patterns from about 11 to 8.4 mm (bikar #253)
- 2026-09-26 — Joins design: ways to join openwork coasters that reuse the frame instead of widening it, with sourced research (3d-models #330)
- 2026-09-25 — The Eight-Fold Star Rosette coaster (CS-8) has all four cells of its square: the video stops at three, so the coaster alone adds the fourth, marked coaster-only; the construction stays faithful (bikar #250)
- 2026-09-25 — The Coaster Lab picks presets from pictures grouped by pattern, captioned by style; `npm run coaster-thumbnails` captures them, and a test fails when a preset has no picture (bikar #249)
- 2026-09-25 — The gallery has a named card for every coaster style, "<Pattern> · <style>" as the Lab titles them, and `make coasters` fails on a coaster with no card; pegs previews drawn as mated pairs (3d-models #318)
- 2026-09-25 — Openwork coasters: `openwork frame <mm>` and the minimal-frame and minimal-pegs styles for CS-1 and CS-2 (bikar #248)

## From the session task board, before the split

Finished work up to 2026-09-25 was kept on one list, `docs/tasks/done.md`, as ten snapshots
of the session task board; its sections were moved here by loop on 2026-09-25 (the file is in
git history). Numbers are the board's task ids, and **the board was renumbered more than
once**, so an id means something only under its snapshot: Snapshot 1's #14 and Snapshot 2's
#14 are different tasks. Each snapshot's own note below says which sequence it uses. Newest
first.

**▸ Snapshot 10 — 2026-09-25 (plates, color regions, the construction migrations,
the consolidation).** **A fresh id sequence, not a continuation of Snapshot 9.** The
live board was rebuilt from the continuation plan's later phases, so this snapshot's
`#1` is the plate composer and its `#37` is the B′ coords producer, not Snapshot 9's
color-regions id. Where a title below cites a second number (e.g. "#37 part 2",
"#17 — youtube verdict scripts"), that inner number is the *old* board's id the task
was carried over from. Decisions D-072…D-080 are in the [decisions log](../../working-model/decisions-log.md).
Still open on the board at this prune: `#4` (P4.3 print record for minis-01, waits on
a physical print), `#6` (P5.2 standard-size plate, after the CAL-CST-* bets are
measured), `#7` (P5.3 frame block, only if a public GeoGebra fixture needs it), `#9`
(push bikar CI secrets, owner-gated) and `#10` (session-reflect skill, after Omar
reviews the 3d-models #218 design).

### Coaster kernel features
- #20–#24 — twist / helix extrude, T1–T5: lofted-ring solid, the `twist <deg>` statement and its conflict refusal, evaluator + render wiring, CV12 + CAL-CST-08, Lab preset + tests (bikar #217, 42ce6dd); CAL-CST-08 mirrored into the calibrate bets file (3d-models #279, 2c1dbb0; count fix #281, 5ed8031)
- #25 — radial-band coloring: the ring a polygon sits in is a print region, D-078 — design (3d-models #277, 6d67693); `bands` verb (bikar #219, 103caa8); ring color onto the height field (bikar #220, f68a536); `--format parts` split by ring color (bikar #221, 2e45cd5)
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
decisions D-065…D-071 in the [decisions log](../../working-model/decisions-log.md). Still open on
the board at this prune: `#12` (the later-phases umbrella: P4.x plate composer,
P5.x corpus), `#17` (youtube's O1/O2 verdict scripts on its local `feat/ggb-coords`
until Omar says main), `#21` (CI secrets sync, owner-gated), `#24` (session-reflect
implementation, waits on the `#23` design review), **`#36`** (the coaster border,
D-071: design shipped in 3d-models #257, bikar implementation checkpointed at
f5d1781 on `feat/coaster-border`, validators/importer/docs remaining per the
continuation plan §2) and `#37` (color regions → per-body export → filament map).

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
D-056…D-064 in the [decisions log](../../working-model/decisions-log.md); the record of what is
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
