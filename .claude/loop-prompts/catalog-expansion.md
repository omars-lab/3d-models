# Loop prompt — grow the print catalog

Paste the block below into a fresh session, or run it as `/loop` with no interval so the
session paces itself. Written 2026-09-25.

This loop decides what to make next and turns finished reconstructions into catalog
coasters. Rebuilding a single video is [`video-reconstruction.md`](video-reconstruction.md).
Tooling for plates is [`print-infrastructure.md`](print-infrastructure.md).

---

## The goal

**A growing catalog of printable Islamic-geometry coasters.** Each one is traced to its
source, passes the fidelity checks, and ships with a standard STL and a catalog entry. The
queue of next candidates is chosen on purpose and never runs dry.

Met, for each pass, when the ledger's migrated count has gone up by one, or the candidate
queue has grown by screened sources, each with a written GO or NO-GO.

## Where it stands (2026-09-25)

- **[Ledger](../../docs/constructions/ledger.md):** 8 migrated (CS-1, 2, 6 to 11), 1 with no
  piece by design (`M60LJNNslHU`), 0 remaining of the rows it lists.
- **The open items** — the `bknVRSMcLj0` reconstruction with no ledger row, the blank O1, O2
  and O3 cells, the empty candidate queue — are in the backlog,
  [`docs/tasks/catalog-expansion/backlog.md`](../../docs/tasks/catalog-expansion/backlog.md).
  What shipped goes in its [done list](../../docs/tasks/catalog-expansion/done.md).
- **Sources:** youtube's discovery wiki (creators, concepts, a relevance file) and its
  `youtube-discover` / `youtube-discovery` skills. So far every construction comes from one
  creator, Sarah Brewer.

## Each pass of the loop

1. **Take stock.** Read the backlog. Compare youtube's `reconstructions/` folder with the ledger rows, and
   look at the blank oracle cells. Check youtube's ladder (`make ladder` in that repo) for
   candidates.
2. **Pick by ROI:**
   1. A finished reconstruction with no ledger row. Migrate it with the
      `import-construction` skill: one bikar PR, then one 3d-models PR (ledger row,
      `CS-<n>` entry, vendored STL, gallery).
   2. A migrated row with a blank oracle cell. Run the check and record the verdict it
      prints.
   3. The queue is short (fewer than three screened GO candidates): discover more. Crawl
      outward from the discovery wiki to new creators and patterns. Screen each one for how
      buildable it is and what it teaches, then write GO or NO-GO with the date. Aim for new
      creators, fold counts and tilings, not ten more 8-fold rosettes.
   4. A GO candidate that is not yet reconstructed: hand it to the video-reconstruction
      loop. Name the id; don't reconstruct it here.
3. **Ship it.** One PR per repo, each from its own worktree. When a construction needs
   something bikar can't express, add that to bikar in its own PR first; that is how the
   earlier migrations went.
4. **Record it,** in the same PR (the `manage-tasks` skill moves the task lines). The ledger row, the count, and the screening verdict. Move
   the item to the done list with the date and PR number; add new finds, including screened
   candidates and hand-offs, to the backlog. Take any new D- id from
   `python3 tools/next_id.py next D`.
5. **Wait when there's nothing to migrate and the queue is full.** Say so in one line, then
   schedule the next wakeup 30 to 60 minutes out.

## Never

- Never record an oracle verdict the tool didn't print. Never fake a coaster for a
  construction that has no piece; mark it "no piece by design", as `M60LJNNslHU` is.
- Never download or republish a video or model without its license in the provenance.
- Never dispatch a print.

Plans: [`iterative-dazzling-finch.md`](../plans/iterative-dazzling-finch.md) (P3.x, P5.1),
and the construction-migration memory
[`remaining-migrations-gated-on-list-literal-fix`](../memory/remaining-migrations-gated-on-list-literal-fix.md)
for the tricks the migrations have used.
