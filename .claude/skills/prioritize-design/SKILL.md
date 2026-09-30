---
name: prioritize-design
description: Rank the coaster candidates and say which pattern becomes a coaster next — the rebuilt constructions that have no coaster yet, or a set the user names — by three scores kept apart (would people like it, is it unusual, how different is it from the coasters already made) plus a "reads as a coaster" check, and put the ranking on a feedback page Omar answers. Use for "which pattern next", "what should we make next", "rank the candidates", "prioritize the coasters", "which of these is most unusual / most different from what we have", and after every pick, since the difference score changes each time a coaster is made. Not for judging a design document (review-design) or a piece already chosen for a plate (review-print).
---

# prioritize-design — which pattern becomes a coaster next

Omar asked for this instead of picking a pattern by hand (2026-09-29, review thread 952r93):
a skill that reviews the candidate coasters and guesses which customers would like most,
which is most unusual, and which differs most from the ones already made, "that we can
iterate on". The scoring lives in [`scoring.md`](scoring.md): the checks, the three scores,
the four facts per design and the round log. Read it every run; it sharpens as Omar answers.

Three rules the design settled (D-085 to D-088 in the
[decisions log](../../../docs/working-model/decisions-log.md)):

- **Three scores, not one judgment.** Appeal and unusual are judged from the picture with
  the reasons written down; difference is arithmetic, so a tool does it and it is recomputed
  after every pick. The total is appeal + 5 × difference + unusual ÷ 2, and the three raw
  scores stay beside it.
- **A check before any score.** Omar's only recorded taste is about fill (no solid disc, no
  half-empty art, no bare wedges), so a candidate that fails the review-print rubric is held
  and fixed, not ranked.
- **Omar decides on a page, not in chat.** Each round writes one request-feedback page. His
  ticks and notes are the only thing that corrects the guesses today, because no shop or
  customer is named anywhere in the repo.

## How one run goes

1. **Read the rules.** [`scoring.md`](scoring.md) and the
   [review-print rubric](../review-print/rubric.md) (the fill verdicts and the `open`,
   `biggest` and `sym` hints come from there; never copy them here).
2. **Collect the candidates.** The [constructions ledger](../../../docs/constructions/ledger.md)
   rows done in youtube with no coaster, or the set the user names. Their coaster notes and
   rebuild scores are in the catalog-expansion backlog's screened queue
   ([backlog](../../../docs/tasks/catalog-expansion/backlog.md)); their pictures are the
   feedback pages' media folders and the youtube reconstructions' step renders.
   Every candidate needs a row in the four-facts table; `python3 tools/design_difference.py
   check` names the ones that do not, and a made coaster missing a row fails the same way.
3. **Run the two checks** on each: reads as a coaster (from the picture, written "not
   measured"; from `python3 tools/print_review.py sheet` once a mesh exists) and the sell
   flag. A candidate that fails is held with the fix it needs written down. Held ones appear
   on the page under their own heading, not in the ranking.
4. **Judge unusual first, then appeal**, 0 to 2 and 0 to 8, one line of reason per part.
   Write them into a small table in the scratchpad: `id | appeal | unusual | ready | rebuild`
   (readiness from scoring.md section 4, the rebuild score from the backlog).
5. **Rank**: `python3 tools/design_difference.py rank --scores <that table>`. It prints
   the difference, the nearest made coaster, the "same source as" note, the total and the
   tie-breaks. The top total is the suggestion; a tie goes to the readier one.
6. **Write the page** through the [request-feedback](../request-feedback/SKILL.md) skill: each
   ranked candidate as a picture beside its nearest made coaster, the three scores with their
   reasons, the total, readiness and sell flag; the held ones with their fixes; and tick boxes
   for **make this first**, **most unusual to me** and **I disagree with this part**, with a
   Notes line. Ship it, bring it into the vault, open it, tell Omar in two lines.

## When Omar answers

1. Read the page and its review threads back the request-feedback way: a decisions-log entry
   per ticked call, a `**Decided <date>:**` line under it, the task moved with manage-tasks.
2. Add one line to the **round log** in [`scoring.md`](scoring.md): the date, what was
   ranked, the suggestion, his pick, and whether a check or a weight moved and why, in his
   words. A weight moves only with a reason; the two weights live at the top of
   `tools/design_difference.py`.
3. A tick on "I disagree with this part" changes that part's wording in scoring.md, with his
   reason beside it. A print verdict on a made coaster goes to review-print's rubric, which
   this skill reads, not here.
4. The chosen pattern starts through `import-construction`. Once its coaster is vendored, the
   ledger's coaster column puts it in the made set, and the next run's differences change on
   their own.

## What this skill never writes

The ledger, the backlogs and review-print's rubric. It reads them; it writes only its page,
its round log, and a fact row when a candidate or a made coaster has none.
