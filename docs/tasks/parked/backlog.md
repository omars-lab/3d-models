# Parked — open work no loop owns

Moved here on 2026-09-25 from [`docs/working-model/backlog.md`](../../working-model/backlog.md) §6, which held the work that
"is not printer-gated". None of the five [loops](../../../.claude/loop-prompts/README.md) is pointed at these. A loop that
takes one on moves it into its own backlog; a loop that finds work nobody owns adds it here.

## The FAQ — waiting on Omar

Five of the six candidates in `docs/faq-proposal.md` are already answered as Q-001 to Q-005 in
the [FAQ](../../faq.md), written 2026-11-03. The proposal file is older than those answers, so
regenerate it with `python3 tools/session_reflect.py update-faq` before asking Omar anything
from it. The one still open is the use-case ids (UC23 and the like, cand-006). Omar marks it keep
or discard and writes the answer, then one PR per the `session-reflect` skill with an id from
`python3 tools/next_id.py next Q`. Never write an FAQ answer yourself. Moved from the
coaster-pipeline backlog on 2026-09-25 (board #10).

## Code graph trial and the two fixes before it (D-129)

Omar picked these on 2026-11-05 from the [code graph design](../../design/process/code-graph.md).
Take them in this order: the first two help on their own, and the third is measured against them.
The first two are done (see [done.md](done.md)): the FAQ answer now shows at the search, and a
complexity check lists the 86 Python functions over 10 and stops any new one.

- **graphify on bikar for two weeks.** Code only, version pinned, no git hooks, no strict mode, per
  §6 of the design and section 7 of the [research](../../research/2026-11-05-graphify-code-graph.md).
  **Running since 2026-11-06, ends 2026-11-20** (bikar #370, graph built from bikar main
  `21420bc3`; see [done.md](done.md)). Exported constants are graph entries and static class
  fields are not, so FILL_ATTRIBUTES stays a FAQ answer. At the end, rerun the FAQ tool over
  bikar sessions and judge against the design's PASS and FAIL lines. The claude-techniques session
  (social-presence-hub) runs a side-by-side test of the graph on real bikar tasks, on the same
  commit, once Omar OKs its plan; read its result beside the FAQ rerun rather than either alone.
  **That test came back 2026-11-10 and does not pass:** searches for code names were not cut
  (13.75 a run with the map, 14.4 without), and map questions came on top of the searches. It
  fits the second FAIL case of the design's §6; details under
  [D-129](../../working-model/decisions-log.md). The FAQ rerun on 2026-11-20 is still owed.
  Stopping early and removing graphify is Omar's call.
- **After the trial:** a script for links between repos (design question 3).
- **Shrinking the complexity list, by hand, a function a PR** (no skill: the design's §5 says
  gate, not skill, and the gate is hook 55). `complexity_gate.py --update` after each split.
  2026-11-07: `prints_gate.py::check_record` (57) split into one helper per rule, gate output on
  the 101 staging records unchanged (#929). Then `tools/move_doc.py::rewrite_text` (35), its five
  nested link fixers made methods of a small class, self-test and a dry-run move report unchanged
  (#930). Then `.claude/gates/plates_gate.py::check_page` (33), one helper per rule group, the
  same findings on all 67 plate pages with each field broken in turn (44,820 cases). Then
  `tools/session_reflect.py::census` (30), its per-line work made methods of a small tally class,
  self-test unchanged and the same result on all 458 real transcripts of this repo not touched in
  the 30 minutes before the run (#934). Then `.claude/gates/site_graph.py::check` (28), one helper
  per rule G0 to G5, self-test unchanged and the same findings on the real graph with each edge,
  node and host field broken in turn (8,358 cases) (#935). Then
  `.claude/skills/draw-side-view/scripts/side_view.py::draw_panel` (27), its per-part drawing made
  methods of a small class, self-test unchanged and every SVG and PNG byte for byte the same on the
  15 real side-view descriptions plus one written to reach the branches they miss (#936). Then
  `.claude/skills/monitor-print/scripts/print_monitor.py::step` (25), one helper per kind of
  change (no reply, someone else's job, first sight, a state change, the 25/50/75% marks, a
  stall), self-test unchanged and the same watch state and rows after every poll on all 36 runs
  in the 32 saved watch logs, each replayed four ways (its own settings, short stall and lost
  windows, pick-up flipped): 144 replays, 5,068 polls (#937). Then
  `.claude/gates/plates_gate.py::check_approvals` (23), one helper each for a row, its Spent by,
  the open approval and the sends, the same findings on all 67 plate pages with every approval
  cell, row and 'sent' timeline row broken in turn (43,230 cases, 35,540 with a finding, every
  rule firing) (#938). Then `.claude/gates/constructions_ledger.py::check` (20), one helper each
  for the file paths, the youtube pin, the ids at the pin and the rung states, self-test unchanged
  and the same findings, reports and counts on the real ledger with each row's youtube, naqsh and
  coaster cells changed, each row dropped or renamed, the pin removed, made up or moved to 12
  older youtube commits, and youtube missing (928 cases, every rule firing) (#939). Then
  `.claude/skills/send-plate/scripts/color_map.py::check` (19), one helper each for one row per
  plate, the answers, shared trays and the plate pages, only the check and nothing on the send
  path, self-test unchanged and the same failures and notices on color maps made from all 66 plate
  pages with a recipe, through the real `bambu filament map` (no saved color map exists), under four tray
  loadouts, with every answer each question offers, and each map broken in turn (775 maps, 68,243 cases, every rule firing) (#940).
  Then `.claude/skills/maintain-vocabulary/scripts/vocabulary.py::problems` (19), one helper each
  for a term's own fields, its links and its files, self-test unchanged and the same problems on
  the real vocabulary.yaml with each of its 19 terms broken field by field (1,149 cases, every
  rule firing) (#941). Then `.claude/skills/draw-side-view/scripts/side_view.py::check_part` (19),
  one helper each for a part's kind and keys, its words and its numbers, run in the old order so a
  part broken two ways is refused for the same first reason, self-test unchanged and the same
  answer on all 225 parts of the 15 real side-view descriptions and the self-test's, each broken
  key by key, kind by kind and two keys at once (747,350 cases, every refusal firing) (#942); the
  crashes that proof found (a size or kind that is not a number or a word) became refusals in
  #943. Then `.claude/skills/color-themes/scripts/themes.py::main` (19), its parser, `check` and
  `suggest` each in a helper, self-test unchanged and the same exit code, output and errors on 97
  command lines (help, check on every construction and `--all`, suggest with every helper and good
  and bad colors, a made-up id) and the same listing pictures, apart from the hero pictures, which
  differ between two runs of the same copy (#944). Then `.claude/gates/catalog_models.py::run`
  (19), one helper each for the excused knobs, one knob's verdict, the message for a knob no model
  declares and the summary, self-test unchanged and the same violations, summary and printed lines
  on the real catalog and on copies with each of its 70 knobs renamed or excused, each entry's
  model file missing, the baseline missing or broken four ways and bikar's grammar and lego
  sources unavailable, each with the full listing on and off (1,504 cases, every verdict seen)
  (#945). Then `build/verify_machine_card.py::verify` (18), one helper each for the STL's
  triangles and volume, the print gate and the mesh gate, problems in the old order, self-test
  unchanged, the same report on the real 23-rung run, and the same problems and volume on every
  rung against made-up bikar output with each line the check reads missing, right or wrong
  (60,720 cases, 60,412 with a problem) (#946). Then `tools/print_review.py::bed_picture` (18),
  one helper each for the part of the bed drawn, the grid, painting the pieces, the set boxes,
  placing the labels and inking the boxes, drawn in the old order, self-test unchanged and every
  picture pixel for pixel the same, with the same names, boxes and lines, on 1,408 cases: the
  61 built plates, each with no bed map, its own bed map where it has one, and two made-up sets,
  under every mix of names, zoom and key (#954). Then `.claude/gates/hook_parity.py::run` (17),
  one helper each for running the hooks, running the checks with no hook, and the summary, with
  the exit code left in `run`; self-test unchanged, and the same printed text and exit code on
  2,080 made-up runs (the declaration check failing or not, up to three hooks each passing,
  failing or missing its tool, up to two extra checks each passing, warning or failing, strict on
  or off; exit codes 0, 1 and 2 all seen). Then `.claude/gates/plates_gate.py::check_print_logs`
  (17), one helper each for the pages' links, one log file, and one log's rows; self-test
  unchanged, and the same findings in the same order on 1,655 cases: the real plates folder and
  copies with each log's plate, header, rows, events and order broken in turn, each log deleted,
  each page's link removed, wrong or left beside a `## Print log` heading, each under master's
  copy absent, the same, a row changed, rows added, and a log master has gone from disk.
  68 left. The `self_test` functions (`branch_inventory.py` 34, `theme_plates.py` 22,
  `site_graph.py` 21, `docs_gate.py` 20, `plates_gate.py` 19, `validate.py` 18) are skipped: each
  is a list of test cases, so splitting it buys little. On 2026-11-08 the list held 53, and
  the two once named next, `catalog.py::build` and `buyers.py::sweep_problems`, were already off
  it (`build` came under 10 in #976). The highest left outside the self-tests are at 14:
  `.claude/gates/docs_gate.py::outline_verdict`,
  `.claude/skills/print-model/scripts/layer_extrusion.py::measure`,
  `.claude/skills/review-print/scripts/prints_page.py::render` and
  `tools/print_review.py::gcode_layer`; read `.claude/gates/complexity-baseline.json` before
  picking, not this line. A
  cleanup skill comes back only if
  this proves a repeated manual task, and then as an extension of the built-in `simplify` skill.
- **A post about the design**, which Omar asked for once he signed off: written with the
  claude-techniques session, numbers and design only. A second post can follow with the trial's
  result.

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

Finished work that a session may not merge itself. Take a line off when it lands. None waiting
as of 2026-11-05.

The youtube `coaster-0ke` and `coaster-n_I` branches merged into youtube main on 2026-11-05
(28baef1 and 7deb8ab). Before these: the four youtube branches and 3d-models #427, #432, #433 and #434 merged on
2026-09-30 (#424 and #425 closed, superseded by #427). #430, another session's ledger rows for
ten youtube reconstructions, was approved by Omar the same day. It had fallen behind master, so
it landed through a fresh branch that merged it and worked the conflicts by hand.

## Cross-repo governance

How this repo's decisions log joins a decision hub (Omar's call;
[D-004](../../working-model/decisions-log.md) chose the local format), then whether the cross-repo ledger check
should block and bring this repo in, then a studio status page rendered from the repos. The
hub decision gates the other two. Source: bikar's cross-repo-dependencies doc and decision
ledger.
