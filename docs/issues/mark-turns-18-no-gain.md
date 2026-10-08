---
date: 2026-10-07
---

# Mark turns at 18° steps gained no id, so they were not added

Was the "Turns" part of catalog-expansion backlog item 9, now closed in its
[done list](../tasks/catalog-expansion/done.md). Nothing shipped in bikar.

## What was suspected

A split coaster's id mark that has no room upright tries turned boxes, in 15° steps
(`MARK_TURNS_DEG` in bikar's `coaster-mark.ts`). Those steps match the straps of four-, six-
and twelve-fold patterns. The item guessed that on a five- or ten-fold pattern, whose straps run
at 18° steps, a mark took the nearest 15° turn and so needed more room than it should, and that
adding the 18° turns would let more ids fit.

## What was tried

The turns ±18°, ±36°, ±54° and ±72° were added after the existing ones, so a mark that fit
before kept its spot and only a mark that fit nowhere tried them. A mark that ends up on one of
those turns is then one the change made room for. The split coasters are both gBV, which is
ten-fold, so they are where a gain would show.

## What the evidence showed

None of the ids landed on an 18° turn.

| Coaster | Size | Ids tried | What fit |
|---|---|---|---|
| Lip (split-01) | 112.5 | 10 to 99 | 11, 12, 15, 17 upright; 14, 71, 77 at 75°, all of which fit before |
| Lip | 80, 90, 100 | 1 and 7 | none at 80; upright at 90 and 100 |
| Flange (split-02) | 80, 90, 100 | 1 and 7 | none |
| Flange | 112.5 | 10 to 19 | none: no room, and at 10 and 14 a counter closes at the 2 mm cap |

Every id refused was refused for room, whatever the turn. The existing mark tests passed
unchanged with the 18° turns in, which says the same from the other side: nothing they cover
moved.

## What replaced it

Nothing was added. A turn that never wins is a code path no test can show working. An id still
needs a bigger spot or a smaller mark, which is the item's other open part (two-digit ids). If a
five- or ten-fold coaster with a narrower bottom face comes along, try this again on that
coaster first; taking the turn from the strap under the mark is the other way the item named.
