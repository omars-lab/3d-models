# Done — the print line

Newest first: date, what shipped, PR. Backlog: [`backlog.md`](backlog.md).

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

### Plates and the bambu CLI (P4.x)
- #1 — P4.1 `bambu slice compose`, the plate composer with a shared `it-<sha12>` helper — design D-072 (3d-models #264, 83703d4); implementation (3d-models #265, bd83fe6)
- #3 — P4.2 minis-01, the first coaster compose plate (3d-models #280, c450fd4)
- #11 — bambu CLI help gate: a generated flag reference held in sync by hook 45 (3d-models #273, fc8ecd8)
- #19 — `bambu ams` read verb + filament-sync: reconcile a plate's logical AMS slots to the live trays by colour (3d-models #285, 7c022fa)

### Coaster colour regions → per-body export → AMS filament map (old #37)
- #2 — the umbrella: a coaster's colour regions become separate bodies that land on separate AMS slots, plus a Coaster Lab knob — design D-073 (3d-models #264, 83703d4); closed by #12–#18 below
- #12 — part 2: `color <region> <PaletteName>` grammar + evaluator (bikar #213, a325d73)
- #13 — §6 research: the headless BambuStudio 3MF → AMS filament-assignment contract (3d-models #267, 871762a)
- #14 — part 3: `--format parts` region body split, pinch detection and `--pinch` strategies, D-074 (bikar #214, 726d567); the `.parts.json` sidecar (bikar #215, 1649389)
- #15 — part 4: palette name → AMS logical slot map for coaster plates, D-075 (3d-models #271, 58612a3)
- #16 — part 5: Coaster Lab per-region colour knob + full per-region 3D tint (bikar #216, 6746237); D-076 recorded (3d-models #272, 1a79fef)
- #17 — K7 reconcile of the design doc's §4 error phases against bikar's parse-time checks (3d-models #267, 871762a)
- #18 — part 4b-ii: multi-part coaster → AMS 3MF assembler + the headless-crash pivot (3d-models #274, d96ea8c); `slice coaster` verb end to end, bikar `--format parts` → `--load-filaments` (3d-models #275, ce86591)

**▸ Snapshot 8 — 2026-09-17 (first-party dispatch + the dogfooding gates).** A
**continuation of Snapshot 7's board, not a renumber** — `#50`–`#57` sit on the same
fresh sequence Snapshot 7 opened (`#8` = X2D bring-up), so Snapshot 8's `#50` is the
first-party dispatch port, not Snapshot 1's Lego M7 anchor solver or Snapshot 2's
woven re-cut `#50`. These closed the transport gap and the pre-dispatch honesty gates
that stood between the sliced Plate 1 and a send. Still open on the board at this
prune: **`#9`** — dogfood guide-print to a physical Plate 1 print, now blocked only by
`#9b` (the warnings sidecar, owned by the concurrent slice-preflight session) and the
owner-gated physical send; its dispatch dependency (`#50`) is delivered and proven by
`--dry-run`. `#9a` (the checked-in ground-truth diff surface) shipped with the
guide-print pre-send-gate work in this same prune.

### First-party dispatch + the pre-dispatch gates
- #50 — port `bambu print send` to first-party dispatch: FTPS :990 implicit-TLS upload + MQTT `print.project_file`, retiring the uninstallable griches MCP from the dispatch path; 18 builder unit tests, `--dry-run` review surface, pivot doc first-party-dispatch.md, the three X2D-UNCONFIRMED CAL fields (bed_type/ams_mapping/md5) exposed as flags (3d-models #243)
- #51 — `bambu slice open <plate.3mf>`: a first-class read-only verb that opens a sliced plate in Bambu Studio for visual approval and dispatches nothing, replacing the raw `open -a` (3d-models, guide-print step 2)
- #52 — the pre-dispatch warnings gate: capture Studio's own slicing warnings, classify against expected-by-design, and fail-closed on an unexpected one (or a missing `<plate>.warnings.json` sidecar) so `print send` never dispatches what Studio would warn about
- #53 — reason the X2D dual-nozzle filament-grouping mode in print-model + `bambu slice --filament-map-mode` — a no-op on a single-material plate (Studio's Filament-Saving default is already correct), a real choice only on a multi-filament plate
- #54 — fold the dogfooding findings into guide-print: warnings triage, grouping mode, open-in-Studio, the GUI one-click alternative
- #55 — slice at `--debug 2` so Studio's slicing warnings surface headlessly into the sidecar the gate reads
- #56 — correct the sub-floor-rung assumption: only `MC2Wall04` (0.4 mm) floats by design; the 0.6 / 0.8 / 1.0 mm rungs slice clean and must not expect the warning (measured 2026-09-17)
- #57 — guard against re-slicing an already-sliced `.3mf` (its embedded custom presets aren't in the bundle, so a re-slice silently loses them)
- #9a — the checked-in ground-truth diff surface: the exact Plate-1 `project_file` payload to diff against a BambuStudio GUI capture, appended to first-party-dispatch.md; the guide-print step-4 pre-send gate + the "are we ready to print?" checklist shipped alongside

**▸ Snapshot 7 — 2026-09-17 (the first-print campaign — bambu CLI, the print-model
skill, and X2D bring-up prep).** The live board was renumbered again after Snapshot
6, so these ids are a **fresh sequence**: Snapshot 7's `#8` is the X2D live-hardware
bring-up, not Snapshot 6's naqsh construction statements or Snapshot 4/5's ledger
block. The board is the plan "First-print campaign — turning the X2D into settled
calibration data" (session plan binary-tickling-kay; decisions D-053/D-054 in the
[decisions log](../../decisions-log.md), D-055 amending D-054). The A-numbers
(`A1…A11`) are the plan's own Phase-A ids. Still open on the board at this prune:
**`#9`** — slice a real plate + the first owner-gated dispatch, which stays
CAL-bet-gated and owner-physical (filament is loaded; the remaining steps are Omar's
caliper/instruments, the Plate 1 slice-to-`.3mf`, and `bambu print send --record`).
The Phase-A slice profile + MC-4 pre-flight (A4/A5, tasks `#21`/`#22`) landed via PR
#185; their whole-card slice + auto_brim finding landed separately in #210.

### Bring-up + the bambu CLI foundation
- #8 — X2D live-hardware bring-up (LAN + Developer Mode + transport proof). The touchscreen toggle is owner-physical; transport was proven read-only end-to-end by the first-party MQTT backend (`status show` → live temps/state off the device), memory bambu-x2d-bringup
- #10 — merge the bambu phases 1–3 PR: the `setup-bambu-x2d` skill + `tools/bambu` CLI (3d-models #177)
- #11 — merge the blog PR documenting the printer bring-up (omars-lab.github.io #225)
- #12 — refresh the use-case map's stale as_of base + repair 18 drifted bikar anchors (3d-models #178)
- #13 — encrypt the blog `.env` with dotenvx + a commit-time secret hook (blog repo)
- #14 — `bambu setup discover`: passive, print-safe LAN printer discovery, zero-touch (3d-models #179)
- #15 — carry the dotenvx v1→v2 fixes back to bikar (bikar)
- #16 — a stale `build/orb-breakdown` dist tripped the 38-timelapse gate (74 findings); rebuilt so the gate reads current
- #17 — pin/migrate dotenvx v1→v2 in bikar + the blog env-sync (an unpinned `npx` was resolving 2.28) (bikar, blog)
- #26 — `A9`: `bambu print list` — enumerate print history from the records (3d-models #181)
- #27 — the day-to-day bambu-CLI usage skill, the front door over the verbs (3d-models #181)
- #30 — first-party MQTT `status` backend that retires the spawned MCP for reads (D-055, amends D-054) (3d-models #188)

### The print-model skill (the sage-operator driver)
- #31 — scaffold the print-model skill dir + SKILL.md front door (3d-models #193)
- #32 — filament discovery: the `bambu filament` verb reads AMS trays + external spool, read-only (3d-models #192)
- #33 — best-orientation reasoning for a piece (3d-models #196)
- #34 — settings reasoning: infill / supports / brim / raft (3d-models #197)
- #35 — the AskUserQuestion filament-selection step (3d-models #195)
- #36 — the per-print plan artifact + slice/preview + the owner-gate handoff (3d-models #199)
- #37 — print-issue feedback + the recovery loop (3d-models #200)
- #42 — plate arrangement: pack repeated pieces on a grid, rotate-to-fit (3d-models #203)
- #43 — nozzle-diameter recommendation (0.2 / 0.4 / 0.6 / 0.8) (3d-models #204)
- #44 — the proactive-advisory sweep: fill unused bed, scale-up, catch footguns (3d-models #205)
- #45 — the best-practices reference, grounded in full + our real examples (3d-models #208)
- #46 — the self-healing loop: physical-iteration findings graduate into best-practices examples (3d-models #209)
- #49 — the task-tracked lifecycle + the questions-intro + the sage input-critique principle (3d-models #220)

### Print metadata + the prints gate
- #38 — the print-metadata schema: lifecycle status, feedback, sheet↔print + repeated-element mapping (rules R6–R9) (3d-models #198)
- #39 — the freshness rules R10–R14: a record's status must match its evidence (3d-models #201)
- #40 — the print-history query: what we printed AND how — `print list --how` + filters (3d-models #202)

### Design docs
- #41 — `docs/print-model-design.md`: lifecycle, mermaid diagrams, decisions + the run-time rubric (3d-models #191)
- #47 — the plate-builder frontend-experience design doc (the served operator front end; now the seed of the private 3d-model-hub repo, Option D)
- #48 — reconcile the print-metadata design with Omar's PMR answers + the estimation-slice primitive (3d-models #217)

**▸ Snapshot 5 — 2026-09-10 (the D-052 base-face-honesty cascade + contract-mirror
gate prune).** A **continuation of Snapshot 4's board, not a renumber** — the four
tasks Snapshot 4 listed as still-open all closed here (`#8` cross-repo ledger block,
`#49` the T9 outline↔solid gate, and the two bench/bet-gated Prints entries `#67` and
`#71`), and the D-052 cascade added `#81`–`#85` on the same sequence. So Snapshot 4's
and Snapshot 5's shared ids (`#8`, `#49`, `#67`, `#71`) are the *same* tasks, closed
here. Still open on the board at this prune: **`#81`** — make the orb breakdown pages
teach flat→sphere construction, the full plan beyond the T9 gate (spec:
`.claude/plans/sunny-booping-crescent.md`; new-session brief:
`.claude/plans/breakdown-pages-kickoff.md`).

### Prints tab (S-series, bench/bet-gated, closed at the bench)
- #67 — Prints tab S2: print Plate 1 and fill the first run record at the bench
- #71 — Prints tab S4: add gate rule R3 (two-way propagation) after the first bet flips (was blocked by #67)

**▸ Snapshot 4 — 2026-09-02 (the prints / wrap-morph / innerHTML prune).** Same
calendar day as Snapshot 3 but a **later, separate prune of a board that was
renumbered again** after it — so the ids below are yet another **fresh
sequence**: Snapshot 4's `#4` is the M4c lattice-walk fourth orb, not Snapshot
2's OrbViewer task or Snapshot 3's `#67`; Snapshot 4's `#72`/`#73` are the mesh-
gate widening and the d3 Phase-2 status overlay, not Snapshot 3's housekeeping
PR / rosette-N plan under the same numbers. Read every id under this date. These
are the completed entries of the board that carried the Prints tab (S-series),
the flat→sphere wrap morph and round-pattern breakdowns, the studio status page
and d3 Phase 2, and the master-commit and innerHTML-taint gates. Still open on
the board at this prune: `#8` (make the cross-repo ledger check block + add
3d-models to the loop); `#49` (T9 — tie the drawn outline to the manifest's
solid, owned by another concurrent session); bench-gated `#67` (Prints S2 —
print Plate 1 and fill the first run record at the bench); and bet-gated `#71`
(Prints S4 — add gate rule R3, two-way propagation, after the first bet flips,
blocked by `#67`).

### Prints tab (S-series)
- #66 — Prints tab S3: ship prints_gate.py with R1/R2/R4 + hook 39-prints
- #68 — Prints tab S5: delete the empty Iteration log from every catalog entry
- #69 — Prints tab S6: build the rendered docs/prints.md tab
- #70 — Prints tab S7: vendor the prints.html lab page (audience: gallery visitors)

**▸ Snapshot 2 — 2026-08-30 (the renumbered board).** Fresh id namespace — see the
namespace warning in the header. Still open on the live board at this prune:
user-decision tasks #4 / #9 / #36; printer-independent tasks #8 / #10 / #26 / #49;
and prints-tab rungs #66–#71 — of which only #67 (print Plate 1 at the bench) and
#71 (R3, waits on the first settled bet) truly need a printer, the rest being
buildable now.

### Decision handbacks + prints tab S1 (S2)
- #61 — Hand back #4 (M4c orb) as a visual decision artifact
- #62 — Hand back #36 (as_of pin under squash merges) as a visual decision artifact
- #63 — Hand back #9 (this repo's D-log joins the decision hub) as a visual decision artifact
- #64 — Prints tab: record the 4 resolved decisions + preserve the design in-repo
- #65 — Prints tab S1: write the run-record format + one filled Plate-1 example
