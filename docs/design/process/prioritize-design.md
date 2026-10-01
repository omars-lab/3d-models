---
status: decided
---

# Prioritize-design: which pattern becomes a coaster next

**Date:** 2026-09-29 · **Status:** decided, not built. Omar answered the four open calls on
2026-09-29 ([section 9](#9-open-calls-for-omar), D-085 to D-088 in the
[decisions log](../../working-model/decisions-log.md)): a weighted total, the four facts in the
skill's scoring file, render the top three first, and pick after the renders.

This doc merges two independent proposals, [A](prioritize-design-a.md) and
[B](prioritize-design-b.md). A checker then re-opened their sources, and the result is in
[prioritize-design-consolidation](../../research/prioritize-design-consolidation.md). Where A
and B disagree, this doc says so and says which side the evidence supports.

## 1. The ask

> "How do we add a good skill that reviews coasters ... and tries to guess which one customes
> would like the most? which one is more unqiue? which one is diffferent thatn the ones we've
> done before ... we should have a prioritize-design skill that we can iterate on."
> (Omar, 2026-09-29, review thread 952r93 on call 4b of the
> [open-calls page](../../working-model/feedback-requests/2026-09-29-open-calls.md);
> [backlog item 5](../../tasks/catalog-expansion/backlog.md))

Its first job is to rank the eight video rebuilds of
[D-084](../../working-model/decisions-log.md) and answer call 4b: which one becomes a coaster
first.

## 2. The short version

- **Three questions, three scores, then one suggestion.**
  - The questions: would people like it, is it unusual, and is it different from what we
    made.
  - They are not blended into one number. Liked and unusual pull against each other: people
    like new designs only while they still look like the thing they are (Hekkert 2003, both
    researchers, confirmed).
  - Busier designs read as more original and can be liked less (Althuizen 2021, confirmed by
    the checker).
- **One check before any score: does it read as a coaster.** This check is Omar's own
  rejections, kept in review-print's rubric and read from there.
- **"Different from ours" is arithmetic, so it is a tool.** "Liked" and "unusual" are
  judgment, so the skill judges them, shows its reasons, and asks Omar on a feedback page.
- **A thin skill plus one small tool, not a gate.** The countable parts go into the tool and
  its scoring file. The rest has no right answer to test against.
- **First run: jlTmt_279M4 is the suggestion, with NtnlGMTElBk and gBV_JTt3Kxk close
  behind.** Omar picks after the renders (D-088).
  - jlTmt leads or ties in three of the four ways the open build questions can go.
  - It is also the only one of the three that can be built today with nothing left to decide.
  - Ntnl wins only if it is woven over-under *and* printed without a round rim.
  - Render all three at 90 mm before choosing, as both researchers say.

## 3. Who the buyer is: not written down

Neither researcher found a shop, customer or price anywhere in the repo. The licence note in the
[candidate screen](../../research/candidate-screen-2026-09-27.md#licence-position) is
conditional: "If coasters are sold".

So until a sales channel exists, "would people like it" is a guess, corrected by one person's
taste, Omar's. That is fine for a maker choosing what to make next. It is not the same as
buyers, and the studies below say people split on taste.

## 4. The rubric

| part | how it is scored | who or what scores it | range |
|---|---|---|---|
| reads as a coaster | review-print's rubric, plus `tools/print_review.py` once a mesh exists | the tool gives hints; the eye decides | pass, hold |
| sell flag | the candidate screen's licence notes | the skill, from the notes | clear, credit, check first |
| would people like it | four parts from the picture | judged | 0–8 |
| is it unusual | against what coasters on Printables usually look like | judged, with a measured sample behind it | 0–2 |
| different from ours | four facts, compared with every made coaster | measured by a tool | 0–1 |
| ready to build | three yes/no facts | measured from the ledger and the styles | tie-break only |

### 4.0 Two checks before scoring

**Reads as a coaster (both researchers).** It fails if it is any of these:

- near-solid ("mostly solid disks are not good coasters");
- half-empty or cut off ("felt incomplete");
- surrounded by bare wedges ("lots of weird empty space").

These are Omar's verdicts in the
[review-print rubric](../../../.claude/skills/review-print/rubric.md). The skill reads that
rubric each time it runs and does not copy it, so a new print verdict updates both skills.

- Once a candidate has a mesh, `tools/print_review.py` gives the rubric's hints: `open` at
  0.15 or below, and `biggest` at 0.05 or above. The rubric calls them "hints for the eye, not
  a gate: nine pieces is too few to set a pass line."
- **Symmetric, by default** (Omar, 2026-09-29, review thread uqjg9s: "we should default to
  symetric coasters"). The same tool prints `sym`: the top-face art turned by 360/n about its
  own centre, and how well it lands on itself. The review-print rubric's check 6 holds a piece
  below 0.9. On 2026-09-29, 25 of the 26 current meshes scored 1.00; CS-6 (tA8eSdVx_EQ) scored
  0.73, which on 2026-09-30 turned out to be the tool turning a seven-point star about its bbox
  centre rather than its middle; it scores 1.00 about its centre of mass. Only turns are tried, not mirrors, and 27 pieces is a thin base for
  the line, so it is the rubric's to move.
- Before a mesh exists, the check is made from the picture. It is marked "not measured",
  never "passed", because pictures misled the candidate screen about openness twice (bknV,
  n3Ii).
- A candidate that fails is **held**, not ranked, and the fix it needs is written down.

**Sell flag (A).** One of:

- *clear*: public domain;
- *credit*: rebuilt from a video, so credit the creator;
- *check first*: it follows a copyrighted book.

The flag is printed beside the name and never changes a rank. It is the researchers' reading
of the licence notes, not legal advice.

### 4.1 Would people like it (judged, 0 to 8)

Four parts, each scored 0, 1 or 2 from the picture:

| part | 2 | 1 | 0 | from |
|---|---|---|---|---|
| **whole and centred** | symmetric about its own middle, complete | complete, but the outline lowers its symmetry | a fragment: cut stars, half a motif | A; symmetry is a small, general plus (Bertamini 2019, Jacobsen 2002, Mather 2023) |
| **fills its outline** | even to the edge | gaps at the rim or the corners | half-empty, or big wedges | B; Omar's verdicts on lEfW, tA8e, n3Ii |
| **reads at 90 mm** | holes of similar size, spread evenly | a few holes far bigger than the rest, or crossings tight enough to close | near-solid, or a mesh of thin lines | A and B; review-print |
| **one clear motif** | one star or rosette the eye goes to | two layered motifs, or several competing | nothing stands out | A; B's "one clear centre" |

**Dropped: "busyness in the middle" (B) and a separate symmetry part (B).**

- Busyness is dropped because no middle level of complexity suits everyone. People split into
  groups that want opposite things (Güçlütürk 2016, Mather 2023, Bies 2016). In product
  design, busier looked more original and was liked less, once other factors were held
  (Althuizen 2021).
- A separate symmetry part is dropped because the effect is small and "whole and centred"
  already covers it from the picture. Once a mesh exists, symmetry is measured instead, as a
  check before scoring (4.0), not as a score.

### 4.2 Is it unusual (judged, 0 to 2)

This uses A's anchor: 970 coaster models pulled from Printables, where flower and mandala
forms are common and Islamic star coasters are rare.

| score | when |
|---|---|
| 2 | nothing in the sample is named for this form: a star in a tile shape, or an interlaced star |
| 1 | a star medallion: rare as an Islamic pattern, but "star coaster" is a common search (197 models) |
| 0 | a common form: flower, mandala, petals, hexagon, Voronoi |

**The "still a coaster" floor (both).** A candidate that scores 0 on "whole and centred", or
that cannot be judged, is held. It is never the "most unusual" winner. This follows Hekkert: an
unusual thing is liked only while it still reads as its kind.

**Why A's anchor and not B's checklist.** B scored unusual on curves, weave, fold family,
outline and layout.

- The fold-family row leaned on one number, "48% of 644 Islamic patterns" in the four-fold
  family. That number is not in the source it was credited to (consolidation, row 14).
- Most of the other rows repeat the "different from ours" facts, so they would count the same
  thing twice.

**Order (B).** Score unusual before appeal. A judge who likes a piece tends to call it novel.
That rests on a search snippet about the Consensual Assessment Technique (not opened), so it is
kept as a cheap habit, not as a finding.

### 4.3 Different from ours (measured, 0 to 1)

This part is B's, with one change.

**The four facts:**

- **fold family:** 4 and 8; 3, 6 and 12; 5 and 10; 7; 9 and 18;
- **layout:** one centre star, a repeat tile, or a cut from a field;
- **outline:** round, hexagon, square, octagon, heptagon, rhombus, rectangle;
- **lines:** straight, arcs, or **woven**. Woven is new; it comes from A's "interlace is a new
  line type" and B's weave row.

**How the score is worked out.**

- Two designs are as similar as the share of the four facts they have in common: 0, 0.25,
  0.5, 0.75 or 1.
- A candidate's difference is 1 minus its average similarity to every made coaster.
- That average similarity is Hekkert's own measure of how typical a thing is: "an exemplar's
  average similarity to all other members of the category". The nine made coasters are the
  category.

**What the tool also shows.**

- The **nearest** made coaster, since "we have almost made this" is easier to act on than an
  average.
- A free-text **same source as** note, for what the facts cannot see. gBV_JTt3Kxk and the made
  CS-7 both come from the tomb of Itimad-ud-Daula. That link turned up in the check, and
  neither researcher drew it.
- The difference is recomputed after every pick. No made coaster is 5- or 10-fold, and six of
  the eight rebuilds are, so the first 10-fold coaster uses up most of that difference for the
  other five.

**Validator:** the difference tool, scoring a coaster that is already in the made set.
PASS: CS-2 (7apC5Q9QS-8), scored against the nine made coasters, shows CS-2 itself as nearest
at 1.00, and its difference is lower than any candidate's.
FAIL: a tool that leaves the candidate's own row out, or compares fewer than four facts, shows
CS-2's nearest below 1.00.

The case it cannot catch: two designs with the same four facts get the same score however
different they look. Flat Ntnl and A9fe are such a pair, and the picture parts in 4.1 are what
tell them apart.

### 4.4 Ready to build (a tie-break, not a score)

Three yes/no facts, shown beside each candidate:

- **An outline we can make.**
  - bikar's coaster outlines are round, square, regular polygon, lobed, and "pattern", where
    the straps are the footprint.
  - There is no rhombus or rectangle slab. The pattern kind might print a tile shape; nobody
    has tried.
- **Lines we can make.**
  - Straight lines are fine.
  - Arcs: the one arc coaster (CS-9) came out near-solid.
  - Woven: no coaster style weaves today.
- **A close rebuild.** The rebuild scores 0.90 or more on the open-calls table. This is a
  starting guess, so that the thing we build is the real pattern.

**Why readiness is a tie-break (B) and not part of the score (A).**

- A's version counts "fits its own outline" twice: once in appeal and once in readiness.
- It also lets ease outrank the three questions Omar asked.
- "That we can iterate on" is kept two ways: as the tie-break, and as the list of work each
  candidate needs first.

### 4.5 Putting the three together

The skill does three things (Omar's pick, D-085):

1. It works out one total per candidate: **appeal + 5 × difference + unusual ÷ 2** (B's
   weighted total). The highest total is the suggestion.
2. It breaks a tie on readiness, then on the rebuild score.
3. It shows the three raw scores beside the total, so a total that hides a weak part is still
   visible.

**The weights are guesses, and the log says so.** The 5 and the ½ are B's, stated as a guess;
nothing found in either pass can set them. A total keeps the size of a lead, which adding ranks
threw away, and it can lean toward "liked" on purpose. The cost is that each round's log must
say whether the weights moved and why (section 6). Adding ranks, A's proposal, needed no
weights and counted the three questions equally; Omar chose the total over it.

## 5. Skill or gate?

Two earlier evaluations in this repo ended "no skill, a gate instead":
[dsl-extension](dsl-extension-skill-evaluation.md) and
[issue-register](issue-register-evaluation.md). In both, what was missing was a **check**:
something was wrong and nothing detected it. The rule they set is to make whatever can be
checked into a check.

**Read against that rule, this job splits in two.**

- **The countable parts become checks and tools, not prose.**
  - Fill is `tools/print_review.py`, which already exists.
  - Difference is one small tool (4.3).
  - The four facts live in a table in the skill's scoring file (Omar's pick, D-086), not in
    the [ledger](../../constructions/ledger.md). No gate changes. The cost is that the table can
    drift from the ledger, so the difference tool checks for itself that the table has a row
    for every made coaster and every ledger row it is asked to rank, and fails naming the
    missing ids. This is the check-shaped piece of the job.
- **Liked and unusual cannot be a gate.**
  - There is no right answer to test against, so a gate would have no failing case.
  - This repo already holds that a gate with no failing case tests nothing.
- **What is missing is a way of writing a page Omar answers.** This is the reason
  [request-feedback](request-feedback-evaluation.md) became a skill ("a gate cannot write a
  page").
  - Each run writes a request-feedback page: each candidate beside its nearest made coaster,
    the three scores with reasons, the suggestion, and tick boxes for "build this first",
    "most unusual to me" and "I disagree with this part".

So the proposal is:

- a thin skill;
- a scoring file next to it: sections 4.0 to 4.5 in short form, the four-facts table, and an
  empty round log;
- the difference tool, which reads that table.

Among the skills in `.claude/skills/` on 2026-09-29, none does this job, and none would be
repeated:

- review-print judges a piece already chosen;
- review-design judges a design document;
- find-model finds other people's models.

The skill's description must say "coaster candidates" and "which pattern next". Otherwise
"design" will send it requests about design documents (A's naming point).

## 6. How it learns

Both researchers use the same pattern as review-print: a dated log, a source for each
change, and small edits.

1. **Log each round against a part, not a total.** The log records:
   - date, the skill's top three, Omar's pick and his "most unusual" pick;
   - for each disagreement, which part missed and Omar's reason;
   - whether the weights in 4.5 changed, and why (D-085).

   A wrong total teaches nothing. A wrong part does. (A and B.)
2. **Change a part only on evidence.** One of these two:
   - the part missed twice in the same direction (A);
   - Omar gives a reason that names something no part covers (B). That reason becomes a new
     part, with his words as its source.

   A single miss with no reason is logged and changes nothing.
3. **Keep score of the skill (B).** Count how often Omar's pick lands in the skill's top
   three. If that is high, the skill can sort a long list and Omar only looks at the top.
4. **Swap a judged part for a measured one once a number agrees with Omar (A).** Openness went
   this way already. The next to try: once meshes exist, the picture distance from each
   candidate to its nearest made coaster (Nguyen's method). If it matches Omar's "different"
   calls better than the four facts, it replaces them.
5. **Prints (both).** A review-print verdict on a ranked piece is evidence for "fills its
   outline" and "reads at 90 mm". A piece ranked high that prints badly means one of those was
   scored too kindly from the picture. Fill failures go into review-print's rubric, which this
   skill reads.
6. **Sales, later (both).** Once a channel exists, sales and reviews per design replace Omar's
   picks as the appeal signal, and the Printables anchor can be retired. Omar's tick stays for
   brand fit and for "unusual".

## 7. What would retire it

- **Drop the scores and keep only the picture page if the scores add nothing.** The test,
  after three rounds: Omar's pick was never the suggestion, it was outside the top three at
  least twice, and the rubric changes have not narrowed the gap. That would mean the page's
  pictures do the work and the scores are noise. (A, with B's hit rate as the measure.)
- **Fold it into the catalog-expansion loop as a checklist if it runs too rarely.** The
  measure is rebuilds arriving less than about once a month. (A.)
- **Replace "liked" with a sales count once sales exist for enough designs to rank.** The
  judged part then retires, and the skill keeps only unusual, different and the checks.

## 8. Worked ranking: the eight video rebuilds

All eight are scored from the rebuild pictures on the open-calls page. None has a coaster
file yet, so "reads as a coaster" is **not measured** for any of them, and this ranking is
provisional until the leaders are rendered at 90 mm.

### 8.1 Held before ranking (both researchers agree)

| video | why held | the fix it needs |
|---|---|---|
| _U6G8QSfWnk | a quarter-tile fragment: two half-stars, half-empty | mirror it to the full tile, then score it |
| Y6kS1MvnKoc | the picture shows the construction grid, not the pattern | render the pattern alone; decide a crop; "(c) Eric Broug 2014" |
| fhGHzop7ULw | stars cut by the rectangle edge ("whole and centred" 0) | choose a repeat cell that does not cut the stars |

A ranked fhG sixth and B ranked it sixth, so holding it changes no one's order.

### 8.2 What A and B each said

| video | A: Q1 / Q2 / Q3, rank sum | B: appeal / unusual / diff, total | where they part |
|---|---|---|---|
| NtnlGMTElBk | 5 / 2 / 5, **6** (1st) | 9 / 3 / 0.53, 13.15 (3rd) | A scores it 2 new features (fold 10, interlace); B's facts do not see the weave, and B marks its rim gaps |
| gBV_JTt3Kxk | 5 / 2 / 5, **6** (2nd) | 9 / 3 / 0.61, **13.55** (1st=) | both near the top; B says the rhombus needs an outline no style makes |
| jlTmt_279M4 | 5 / 2 / 3, 9.5 (3rd) | 8 / 5 / 0.61, **13.55** (1st=) | A counts 0 new features; B sees a new layout and fold pairing |
| A9fefFurD_s | 4 / 1 / 3, 14 | 8 / 1 / 0.53, 11.15 | agree it is lower |
| n_ICgwOr6qs | 5 / 0 / 2, 15 | 7 / 4 / 0.72, 12.60 | B rewards its arcs as unusual and different; A marks arcs as not ready |

The checker recomputed both columns, and every figure matches.

**Why they differ.** Three reasons, in order of weight:

1. **How different jlTmt is.** A's count asks, feature by feature, whether any made coaster
   has it. 7-fold (CS-6) and square (CS-2, CS-8) are both made, so jlTmt scores 0. B compares
   whole designs: no made coaster is a 7-fold repeat tile, so jlTmt scores 0.61. A's own doc
   says its count "cannot see what the eye does" here. B's measure is the one Hekkert used.
2. **Readiness.** A adds readiness into the score, which lifts round, straight-lined Ntnl. B
   uses it only to break ties.
3. **Ntnl's rim.** B scores Ntnl's ten rim gaps as a fill fault. A scored the same fault
   against A9fe but not against Ntnl. The checker looked at both pictures, and both have it.

### 8.3 The consolidated ranking

These are the scores after the rubric in section 4 is applied:

- appeal takes A's parts, with the rim-wedge fault moved into B's "fills its outline" and
  scored the same way for Ntnl, A9fe and n_IC;
- unusual takes A's anchor;
- difference takes B's arithmetic.

| video | whole | fills | reads | motif | **appeal** | **unusual** | **diff** (flat / woven) | nearest made | ready | sell flag |
|---|---|---|---|---|---|---|---|---|---|---|
| jlTmt_279M4 | 2 | 2 | 2 | 1 | **7** | **2** | **0.61** | CS-8, 0.75 | square, straight, 0.941: **yes** | clear (Bourgoin 1879) |
| gBV_JTt3Kxk | 1 | 2 | 2 | 2 | **7** | **2** | **0.61** | CS-1, 0.50; same monument as CS-7 | rhombus: **no outline** (pattern kind untried); straight; 0.906 | credit (Mian) |
| NtnlGMTElBk | 2 | 1 | 1 | 2 | **6** | **2** | **0.53 / 0.75** | CS-10, 0.75 (flat) | round, straight, 0.930: **yes** flat; woven: **not built** | credit (Mian) |
| n_ICgwOr6qs | 2 | 1 | 1 | 2 | **6** | **0** | **0.72** | CS-9, 0.75 | round; **arcs** (CS-9 came out near-solid); 0.886 | credit (Mian) |
| A9fefFurD_s | 2 | 1 | 2 | 1 | **6** | **1** | **0.53** | CS-10, 0.75 | round, straight; 0.855, below 0.90 | **check first** (Broug's book) |

Two open build questions move the result: is Ntnl woven, and is it framed by a round rim or
printed in the minimal style, where the straps are the footprint and there is no rim to leave
wedges? In the minimal style the rim-wedge fault goes, so Ntnl, n_IC and A9fe score 2 on "fills
its outline" (appeal 7). Weighted totals (4.5), highest first:

| reading | jlTmt | gBV | Ntnl | n_IC | A9fe | suggestion |
|---|---|---|---|---|---|---|
| round rim, flat lines | **11.05** | **11.05** | 9.65 | 9.60 | 9.15 | jlTmt (ties gBV; ready) |
| round rim, woven Ntnl | **11.05** | **11.05** | 10.75 | 9.60 | 9.15 | jlTmt (ties gBV; ready) |
| minimal style, flat lines | **11.05** | **11.05** | 10.65 | 10.60 | 10.15 | jlTmt (ties gBV; ready) |
| minimal style, woven Ntnl | 11.05 | 11.05 | **11.75** | 10.60 | 10.15 | Ntnl |

Adding ranks, the method the feedback page also showed, names the same suggestion in all four
readings; the one change is that round-rim woven Ntnl drops from a three-way tie to third.

**The consolidated top three, and why each is there:**

1. **jlTmt_279M4.**
   - It leads or ties in three of the four readings.
   - It is the only leader that can be built today with nothing left to decide: square
     outline, straight lines, the closest rebuild (0.941).
   - It has the cleanest licence (Bourgoin 1879, public domain) and the most even fill of
     the eight.
   - Its one weak part is "one clear motif": four seven-point stars round an octagon, and no
     single centre.
2. **NtnlGMTElBk.**
   - It is the most different of all eight, but only if it is woven, and no coaster style
     weaves yet.
   - It wins outright only when woven *and* printed without a round rim.
   - Built flat, it has the same four facts as A9fe and falls behind n_IC.
   - It is still the pick call 4b proposed. That proposal rested on the same facts (round,
     straight, 0.930), so it is not independent support.
3. **gBV_JTt3Kxk.**
   - It ties jlTmt on every score.
   - It loses the tie because no coaster outline draws a rhombus. Whether the minimal style
     prints it is untried.
   - It shares its monument with the made CS-7, and a buyer may read that as a set or as a
     repeat.

**What the scores cannot settle.**

- The top three sit within 1.4 points of each other in every reading, out of totals near 11.
- One judged part moving by one point can reorder them. For example, Ntnl's "reads at 90 mm"
  is 1 because the crossings may close at size; at 2, it leads the minimal-style flat reading
  (11.65).
- This is the gap both researchers named, and it is why the next step is a render and not
  more scoring.

**Next, before anything is built** (both researchers):

1. Render jlTmt, Ntnl and gBV in the minimal style at 90 mm, with Ntnl flat. Weaving is its
   own build question.
2. Run `tools/print_review.py` on each, including `sym`.
3. Hold any that fail "reads as a coaster" or score `sym` below 0.9.
4. Put the result on Omar's page with this table; he picks from it (D-087, D-088).

## 9. Open calls for Omar

All four were answered on the
[feedback page](../../working-model/feedback-requests/2026-09-29-prioritize-design.md) on
2026-09-29. The options, with their pros, cons and implications, are on that page and in each
decisions-log entry.

| call | recommended here | Omar's pick | decision |
|---|---|---|---|
| How to combine the three | add the ranks (A) | **weighted total (B)** | D-085, section 4.5 |
| Where the four facts live | ledger columns (B) | **a table in the scoring file** | D-086, section 5 |
| First build | render the top three, then pick | **render the three first** | D-087, section 8.3 |
| Which pattern goes first | jlTmt_279M4 | **decide after the renders** | D-088 |

## 10. What would need building (not built here)

- **The renders of jlTmt, Ntnl (flat) and gBV** in the minimal style at 90 mm, checked by
  `tools/print_review.py` (8.3, "Next"). None has a coaster file yet, so each is an
  import-construction job first. This comes before everything below (D-087).
- **The difference tool**, reading the four-facts table, with the Validator in 4.3. It also
  checks that the table has a row for every made coaster and every candidate it ranks (D-086).
- **The four facts for the nine made coasters and the eight candidates**, as that table in the
  scoring file. Today they are one reader's reading of titles and pictures (B's).
- **The skill and its scoring file**, writing through request-feedback.
- **A check of the pattern outline kind** for rhombus and rectangle tiles, and of weaving in a
  coaster. Each of these changes the ranking (8.3).
