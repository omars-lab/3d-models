---
status: draft
---

# A prioritize-design skill: which pattern becomes a coaster next (proposal A)

**Date:** 2026-09-29 · **By:** researcher A, one of two independent proposals; a checker
merges them · **Research:** [prioritize-design-research-a](../../research/prioritize-design-research-a.md)

## 1. The ask

> A skill that reviews the candidate coasters and guesses which customers would like most,
> which is most unusual, and which differs most from the ones already made, "that we can
> iterate on". Its rubric lives in a file next to the skill so it can sharpen.
> (Omar, 2026-09-29, review thread 952r93; [backlog item 5](../../tasks/catalog-expansion/backlog.md))

Its first run ranks the eight video rebuilds of
[D-084](../../working-model/decisions-log.md) and answers call 4b on the
[open-calls page](../../working-model/feedback-requests/2026-09-29-open-calls.md): which one
becomes a coaster first.

**Who "customers" are is not written down anywhere in this repo.** No shop, channel or price is
stated (research §5). Until one is, the only buyer whose taste is on record is Omar, so this
skill guesses on behalf of a buyer and Omar corrects the guess.

## 2. Skill, or gate?

The repo's two precedents ([dsl-extension](dsl-extension-skill-evaluation.md),
[issue-register](issue-register-evaluation.md)) both ended "no skill, a gate instead". Each
found a missing *check*: something was wrong and nothing detected it.

**That precedent does not fit the core of this job, and here is why.** Ranking candidates by
likely appeal and by how unusual they are is a judgment from pictures and from taste nobody has
measured. A gate answers pass or fail against a fixed rule; it cannot rank, and there is no rule
yet to fix. The closer precedents are:

- [request-feedback](request-feedback-evaluation.md), which became a skill because what was
  missing was a way of *writing* ("a gate cannot write a page");
- the review-print skill, which keeps a rubric file beside it and adds to it as prints come
  back.

**But the precedent does apply to the parts that can be checked**, and those should be tool
numbers, not prose the skill re-argues each run:

- whether a piece reads as a coaster at size: `tools/print_review.py` already measures it;
- which of a candidate's features our made coasters already have (fold, outline, line type):
  a count from data, which a small tool could print (not written yet; §6).

Among the skills in `.claude/skills/` on 2026-09-29, none does this job, so this is not a third
skill on top of two (the dsl-extension failure). review-print judges a piece already chosen,
review-design judges a design *document*, and find-model finds other people's models.

**Naming.** "design" in this repo's skill list already means a design document (review-design,
write-design). The skill's description must say "coaster candidates" and "which pattern next",
or it will be dispatched for documents.

## 3. Three questions, three lists, not one score

Omar asked three different questions. The research gives a reason to keep them apart: in online
shopping, products with no close look-alike got more clicks but converted 5–7% less (research
§3, fetched abstract). Unusual and liked are different things, so the skill answers each
question on its own list. It then names one suggested first build by a simple stated rule (§3.5),
and shows its working so Omar can disagree with any part.

Before any list, two checks run on every candidate.

### 3.0 Two checks before scoring

**Check 1: does it read as a coaster at size?** This is review-print's rubric, applied early:
not near-solid, no bare wedges, not half-empty (Omar's rejections on minis-03). When the
candidate has a coaster file, render it at 90 mm in minimal-frame and run
`tools/print_review.py sheet`; use the rubric's hints (`open` ≤ 0.15 near-solid, `biggest`
≥ 0.05 a gap). These are hints from nine pieces, not a pass line (the rubric says so). A
candidate with no coaster file yet is marked "not measured", never "passed", because
pictures misled the candidate screen about openness twice (bknV, n3Ii). A clear failure on
the sheet is left off the lists with the reason written, as review-print does.

**Check 2: can it be sold?** A flag, not a score: *clear* (public domain), *credit* (rebuilt
from a video, credit the creator), or *check first* (follows a copyrighted book, or copies a
GeoGebra file under non-commercial terms). This comes from the candidate screen's licence
section, which is the researchers' reading and not legal advice. The flag does not change a
rank. It is printed next to the name so nobody picks a *check first* piece to sell without
seeing it.

### 3.1 Question 1: would buyers like it? (a guess; only Omar or sales can settle it)

Three parts, each 0, 1 or 2, scored from the picture:

| part | 2 | 1 | 0 | evidence |
|---|---|---|---|---|
| **Whole and centred** | symmetric about its own middle and complete in its outline | complete, but in an outline that lowers its symmetry, or its points leave empty wedges in any frame | a fragment: cut stars, half a motif, needs a crop | symmetry is preferred in abstract shapes, a small effect (S2, fetched); ease of taking it in (S4, fetched abstract); Omar's "felt incomplete" |
| **Reads at 90 mm** | holes of similar size spread evenly | a few holes much bigger than the rest, or crossings so tight they may close up | near-solid, half-empty, or can't be judged from the picture | Omar's near-solid and bare-wedge rejections; review-print check 3 |
| **One clear motif** | one star or rosette the eye goes to | two layered motifs, or several stars competing | no motif stands out | harmony (S8, snippet only; flagged); symmetry and complexity as the top cues for "beautiful" (S9, snippet only) |

There is deliberately no "not too complex" part. For ordered patterns most people in one
study liked more complexity, not less (S3, fetched: 76% versus 24%), and a review of product
design studies found little evidence for a best middle level (S7, snippet only). The floor
that is on record is Omar's: not near-solid, not half-empty, and "reads at 90 mm" covers it.

**This whole question is a judgment call.** The evidence is lab studies of looks in general,
maker likes on Printables, and Etsy snippets; none measures a buyer of this product. The scores
are a starting guess for Omar to correct, and the rubric records each correction (§5).

### 3.2 Question 2: is it unusual? (a guess, with one measured anchor)

Scored 0, 1 or 2 against what a coaster usually looks like. The anchor is the Printables
sample (research §4.1): 970 coaster-related models, where flower and mandala forms are common
and Islamic star coasters are rare.

| score | when |
|---|---|
| 2 | no coaster in the sample is named for its form: a star in a tile shape (rhombus, rectangle, tilted square), or an interlaced star |
| 1 | a star medallion: rare as an Islamic pattern there, but "star coaster" is a common form (197 matches) |
| 0 | a common coaster form: flower, mandala, petals, hexagon, Voronoi |

**The "still a coaster" floor.** People like novelty only while the thing stays recognisable
(S1, fetched abstract: "novel designs as long as the novelty does not affect typicality"). So a
candidate that scores 0 on "whole and centred" is listed as "unusual, but not yet a coaster"
and ranked after the rest on this list, whatever its score. That is how a tile fragment avoids
winning "most unusual".

**This is a judgment call too.** The sample is names, not pictures, and it is makers, not
buyers. A later round can replace it with a picture comparison (§5).

### 3.3 Question 3: is it different from ours, and can we iterate on it? (mostly computed)

Two halves, added together.

**New to us (0 to 3).** One point for each feature that none of our nine made coasters has.
The made values (research §5) are:

- **fold:** 6, 7, 8, 12, 18;
- **outline:** hexagon, square, heptagon, octagon, round;
- **line type:** straight, arcs.

An interlaced band (one line crossing over and under itself) counts as a new line type, since
no made coaster has one. This is a rough stand-in for S5's nearest-neighbour distance: it asks,
feature by feature, whether any made coaster already has it.

**Ready to iterate on (0 to 3).** One point each:

- **fits its own outline with no crop** (a round medallion, or a tile whose edge is its outline);
- **its lines are straight.** Arcs score 0 for now, because the one arc coaster, nmEj, renders
  near-solid and is marked "do not print";
- **the rebuild matches the video closely**, scoring 0.90 or more on the open-calls table. This
  line is a starting guess, not a measured one. It is there so the thing we iterate on is the
  real pattern.

The creator is left out: a buyer cannot see it. It is still shown, since all nine made coasters
are Sarah Brewer's.

**What this count misses.** It only knows three features. jlTmt_279M4 scores 0 new features
(7-fold and square are both made) yet looks nothing like the 7-fold CS-6. So the skill always
shows each candidate beside its nearest made coaster in one picture, and Omar's eye overrides
the count. Section 5 says how a round turns that override into a sharper rule.

### 3.4 Using the coaster: kept out of the ranking

Printed coasters trap spills in their gaps and are hard to clean (S10, fetched), and a closed
base stops drips (S11, snippet). That is a question about the **style** (openwork lets water
through, plain has a solid base), not about which pattern to pick. So the skill notes it where
the style is chosen, after the ranking, and does not score it.

### 3.5 One suggested first build

For each question, the skill ranks the candidates (tied scores share the average rank) and adds
the three ranks. The lowest total is the suggestion. Ties go to the higher rebuild score. Adding
ranks rather than scores keeps any one question's 0–6 range from swamping another's 0–2. It
weights the three questions equally, and whether they should be equal is Omar's call (§4).

## 4. What only Omar, or real sales, can settle

Said plainly, so nobody reads a guess as a finding:

- **Question 1 in full.** The only taste on record is Omar's, from nine pieces.
- **Question 2's anchor.** Printables names describe maker files, not what buyers see or buy.
- **How much each question counts.** Equal weight in §3.5 is a placeholder.
- **Whether a customer exists and who it is.** Nothing in the repo says, and the answer changes
  what "like" means. A gift buyer on Etsy, a café, and Omar's own shelf would each want
  something different.
- **The licence flags.** They are the researchers' reading, not legal advice.

The computed parts (the openness numbers and the new-feature count) do not need Omar. What
they mean for a coaster still does.

## 5. What the skill reads and writes, and how a round sharpens it

**Reads, every run:**

- its own rubric file beside the skill (the checks and parts in §3, and the round log below);
- the candidates: ledger rows with no coaster yet ([ledger](../../constructions/ledger.md)) and
  their pictures (the open-calls media, or the youtube repo's records);
- the made set: the coaster files in `src/Coasters/`, the ledger's CS numbers, and the
  [coaster styles](../../../.claude/skills/import-construction/coaster-styles.md);
- the reactions on record: the [review-print rubric](../../../.claude/skills/review-print/rubric.md)
  and the print records in `docs/prints/`;
- the licence notes in the [candidate screen](../../research/candidate-screen-2026-09-27.md#licence-position).

**Writes:**

- a feedback page made with the request-feedback skill. It shows each candidate beside its
  nearest made coaster, the three lists with their scores, the suggestion, and tick boxes: agree
  or disagree per list, plus "build this one first";
- after Omar answers, one dated block in the rubric's round log: each candidate's scores, Omar's
  verdict, and for each disagreement which part was wrong and what changed;
- the backlog line for the chosen build, through manage-tasks.

**How a round sharpens the rubric.** The pattern is the one review-print already uses: dated,
sourced, and small.

1. **Log every disagreement against a part, not a total.** "Omar ranked jlTmt above Ntnl for
   buyers; the skill had them tied; the part that missed was one clear motif, and he said the
   even square reads better." A total that is wrong cannot teach anything; a part can.
2. **Change a part only after it misses twice in the same direction.** One round is one
   opinion. Change its wording or its scoring bands, and write the date and the two rounds that
   caused it, as review-print's rubric does ("sDO9, nmEj on minis-03").
3. **Promote a picture check to a number when a number agrees with Omar.** Openness went this way
   already (review-print's `open` and `biggest`). The next one to try: once coaster renders
   exist for the made set and the candidates, measure the picture distance from each candidate to
   its nearest made coaster (S5's method). If that agrees with Omar's "different" calls better
   than the feature count, it replaces the count.
4. **When prints come back, their verdicts join the log.** A piece ranked high that prints badly
   tells us a part (usually "reads at 90 mm") was scored too kindly from the picture.
5. **When a sales channel exists, sales join the log as a column.** They then outrank Omar's
   guess for question 1, and the Etsy and Printables anchors can be retired.

**What would reverse this skill.** Drop the scores and keep only the picture page if, after
three rounds, Omar's pick differs from the suggestion every time and the rubric changes have not
narrowed the gap. That would mean the scoring adds nothing over showing him the pictures.
Fold it into the catalog-expansion loop as a checklist instead of a skill if rebuilds arrive
less than about once a month, too rarely to earn a place in the skill list.

## 6. What the skill needs that does not exist yet

- **Features as data.** Fold, outline and line type live in prose (ledger titles, backlog notes,
  coaster files). A column per feature in the ledger, or a small tool that reads them from each
  coaster file, would make "new to us" a number the skill reads rather than re-derives. That is
  the gate-shaped part of this job, and it should be built as one.
- **Coaster renders for candidates.** Check 1 cannot run until a candidate has a coaster file.
  The cheapest route is to render the top three by §3.5 in minimal-frame at 90 mm, run the
  print-review sheet, and re-rank if one fails. Rendering all eight is not needed to pick one.

## 7. Worked example: the eight video rebuilds

Scored from the three-panel pictures on the open-calls page and the backlog notes (research §5).
**Check 1 is "not measured" for all eight**, because none has a coaster file yet, so this whole
ranking is provisional until the top three are rendered and sheeted.

| video | whole and centred | reads at 90 mm | one motif | **Q1** | **Q2** | new to us | ready | **Q3** | sell flag |
|---|---|---|---|---|---|---|---|---|---|
| NtnlGMTElBk | 2 | 1 (large open centre, tight crossings) | 2 | **5** | **2** interlaced | 2 (fold 10, interlace) | 3 | **5** | credit (Mian) |
| gBV_JTt3Kxk | 1 (rhombus lowers symmetry) | 2 | 2 | **5** | **2** rhombus tile | 2 (fold 10, rhombus) | 3 | **5** | credit (Mian) |
| jlTmt_279M4 | 2 | 2 | 1 (four stars and octagons) | **5** | **2** tilted-square tile | 0 | 3 | **3** | clear (Bourgoin 1879) |
| n_ICgwOr6qs | 2 | 1 (petal holes far bigger than centre) | 2 | **5** | **0** flower | 1 (fold 5) | 1 (arcs; 0.886) | **2** | credit (Mian) |
| A9fefFurD_s | 1 (big points leave wedges) | 2 | 1 (two layered stars) | **4** | **1** star medallion | 1 (fold 10) | 2 (0.855) | **3** | **check first** (Broug's book) |
| fhGHzop7ULw | 0 (stars cut by the edge) | 1 (big uneven holes) | 1 | **2** | 2, but not yet a coaster | 1 (rectangle) | 3 | **4** | credit (Aljanabi) |
| _U6G8QSfWnk | 0 (two half-stars) | 0 (half-empty) | 1 | **1** | 2, but not yet a coaster | 2 (fold 10, rectangle) | 1 (no outline; 0.895) | **3** | credit (Mian) |
| Y6kS1MvnKoc | not judged: the picture shows the scaffold, not the pattern | — | — | **—** | 1 star medallion, if cropped round | 1 (fold 10) | 1 (needs a crop; 0.861) | **2** | credit (Broug) |

How to read it: Q1 = the three parts added (0–6), Q2 = §3.2 (0–2), Q3 = new to us plus ready
(0–6). For gBV, "fits its own outline" is scored for the art filling its rhombus; whether our
coaster outlines can draw a rhombus has not been checked. For Ntnl, the interlace point assumes
it is built over-under. Built as flat straight lines, it scores 1 new and Q3 = 4.

**The three lists:**

1. **Would buyers like it:** Ntnl, gBV, jlTmt and n_IC tie at 5; then A9fe 4, fhG 2, _U6G 1;
   Y6kS not judged. The guess cannot separate the top four. That is Omar's call, and exactly
   what the page's tick boxes are for.
2. **Most unusual:** Ntnl, gBV and jlTmt at 2; A9fe 1; n_IC 0. fhG and _U6G score 2 but are "not
   yet a coaster", and Y6kS was not judged, so all three rank last.
3. **Most different from ours and ready to iterate on:** Ntnl and gBV at 5; fhG 4; jlTmt, A9fe and
   _U6G at 3; n_IC and Y6kS at 2.

**Suggested first build (§3.5).** Rank sums, tied scores sharing the average rank:

| video | Q1 rank | Q2 rank | Q3 rank | sum |
|---|---|---|---|---|
| NtnlGMTElBk | 2.5 | 2 | 1.5 | **6** |
| gBV_JTt3Kxk | 2.5 | 2 | 1.5 | **6** |
| jlTmt_279M4 | 2.5 | 2 | 5 | 9.5 |
| A9fefFurD_s | 5 | 4 | 5 | 14 |
| n_ICgwOr6qs | 2.5 | 5 | 7.5 | 15 |
| fhGHzop7ULw | 6 | 7 | 3 | 16 |
| _U6G8QSfWnk | 7 | 7 | 5 | 19 |
| Y6kS1MvnKoc | 8 | 7 | 7.5 | 22.5 |

(A candidate not judged on Q1 ranks last there. On Q2, the three ranked last share ranks 6 to 8, so each gets 7.)

Ntnl and gBV tie on 6. The tie goes to the higher rebuild score, **NtnlGMTElBk** (0.930 against
0.906). It is also round, so every existing style fits it without asking whether a rhombus
outline works. **gBV_JTt3Kxk is second, and jlTmt_279M4 third.** jlTmt is the one to watch: it
ties for buyer appeal, is the only public-domain source, and is scored low on "different" only
because the feature count cannot see what the eye does (§3.3).

The suggestion matches the pick call 4b already proposed. That is not independent support: the
same facts (round, straight lines, 0.930) fed both.

Next, before anything is built: render Ntnl, gBV and jlTmt in minimal-frame at 90 mm, run the
print-review sheet, drop any that fail check 1, and put the result on Omar's page.

## 8. What the rubric file starts with

The rubric file beside the skill starts with sections 3.0 to 3.5 of this doc, in short form: the
two checks, the three questions' parts and bands, the rank-sum rule, and an empty round log.
Each part names the finding it came from, as review-print's checks do. Where the research could
open only a snippet, the part says so, so a later round knows which parts rest on the weakest
ground.
