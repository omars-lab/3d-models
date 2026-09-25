# Routing — which file an item belongs in

Read by [`SKILL.md`](SKILL.md) on every run. Ask these in order and stop at the first yes.
When a routing call turns out wrong, fix the rule here, not only the item.

| # | Question | Goes to |
|---|---|---|
| 1 | Is it merging PRs, deleting branches, worktrees or stashes, repo hygiene, memory tidying, hooks or gates across repos, CI or deploy plumbing? | `consolidation` |
| 2 | Does it need the physical printer, or a measurement from a printed plate — a `CAL-*` bet, a coupon, plate 1 to 5, a print record? | `coaster-pipeline` |
| 3 | Is it about getting a plate from config to send-ready — `bambu` CLI, compose, slice, preflight, AMS or filament mapping, plate YAML, the prints tab? | `print-infrastructure` |
| 4 | Is it a new pattern, a construction migration, the constructions ledger, oracle cells, coaster forms or kernel features for a catalog coaster? | `catalog-expansion` |
| 5 | Is it rebuilding a tutorial video as a GeoGebra construction? | youtube repo (video-reconstruction loop) |
| 6 | None of the above — orbs, Lego Lab, LDraw, d3, the rosette explorer, Maclado, the DSL itself? | `parked` |

Tie-breaks:

- **Printer beats software.** Work that the plate-1 print is waiting on goes to
  `coaster-pipeline` even if the fix is in the `bambu` CLI; the rest of the CLI goes to
  `print-infrastructure`.
- **Cross-repo cleanup is consolidation** even when the repo is bikar or qiyas.
- **Owner-gated items still get a home.** Route them by the rules above and mark them as
  waiting on Omar.
