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
  older youtube commits, and youtube missing (928 cases, every rule firing). 77 left.
  The `self_test` functions (`branch_inventory.py` 34, `theme_plates.py` 22, `site_graph.py` 21,
  `docs_gate.py` 20) are skipped: each is a list of test cases, so splitting it buys little. Next
  are the four at 19: `send-plate/scripts/color_map.py::check`, `maintain-vocabulary/scripts/vocabulary.py::problems`,
  `draw-side-view/scripts/side_view.py::check_part` and `color-themes/scripts/themes.py::main`. A
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
