---
status: draft
---

# Prioritize-design: which coaster to make next (researcher B)

**Status:** research draft, 2026-09-29. One of two independent write-ups on the same question;
a checker merges them before the skill is written. The sources are in
[`../../research/prioritize-design-research-b.md`](../../research/prioritize-design-research-b.md),
each marked as fetched or a search snippet. No skill is written here and no decision id is
taken.

## The ask

Omar, on call 4b of the [open-calls page](../../working-model/feedback-requests/2026-09-29-open-calls.md),
2026-09-29: a skill "that reviews coasters ... and tries to guess which one customes would
like the most? which one is more unqiue? which one is diffferent thatn the ones we've done
before ... a prioritize-design skill that we can iterate on." Its rules live in a file next to
the skill so they can sharpen after each round. Its first run ranks the eight video rebuilds
and answers 4b. ([catalog-expansion backlog](../../tasks/catalog-expansion/backlog.md), item 5.)

## The short version

- **Three questions, three scores, kept apart.** How much people would like it, how unusual it
  is, how different it is from what we made. The research says liked and unusual pull against
  each other, so adding them up hides the trade. The skill shows all three and then one
  suggested order.
- **One check before any score: does it read as a coaster.** Omar's only recorded taste so far
  is about fill: not a solid disc, not half-empty, no bare wedges. A design that fails this is
  not ranked until it is fixed.
- **"Different from what we made" is arithmetic, so it is a tool, not prose.** Four facts per
  design (fold family, layout, outline, straight or curved lines) compared with the nine made
  coasters. It must be recomputed after every pick.
- **"Liked" and "unusual" are judgment.** The skill judges from the picture, writes its
  reasons, and asks Omar through a feedback page. There is no customer and no sales channel
  stated in the repo, so today Omar's picks and print verdicts are the only thing that can
  correct it.
- **First run on the eight rebuilds:** jlTmt_279M4 and gBV_JTt3Kxk (as a rhombus) tie at
  13.55, NtnlGMTElBk is at 13.15. The gap is smaller than one judged point, so the scores do
  not overturn the 4b pick. They make the real choice visible: an evenly filled square tile
  with a rare fold (jlTmt) against a new fold on a familiar round star (Ntnl).

## Who the customer is

Nothing in `docs/` or `.claude/` names a shop, a customer or a price. The candidate screen's
licence note is conditional ("If coasters are sold"). So:

- "What customers like" is a guess built from outside studies and marketplace hints, checked
  only against one person's taste (Omar's), until there is a channel.
- One person's taste is a narrow sample. The best-read study here found that people split into
  groups that like opposite things (see criterion 1). Omar's picks will train the skill toward
  Omar, which is fine for a maker choosing what to make, and not the same as buyers.

## The criteria

### 0. It reads as a coaster (a check, not a score)

**How it is judged.** The three things Omar has turned down, from the
[review-print rubric](../../../.claude/skills/review-print/rubric.md) and the
look-before-you-print memory: a near-solid disc ("mostly solid disks are not good coasters"),
half-empty art ("felt incomplete"), bare wedges between the art and the frame ("lots of weird
empty space"). Once a design has a mesh, `tools/print_review.py` gives the numbers the rubric
uses as hints: `open` at or below 0.15 flagged both near-solid pieces, `biggest` at or above
0.05 flagged both big gaps, and nothing flagged tA8e's wedges. The rubric calls these "hints
for the eye, not a gate: nine pieces is too few to set a pass line." Before a mesh exists (the
eight rebuilds today), it is judged from the rebuild picture.

**Evidence.** Omar's own verdicts on the minis-03 candidates. This is the strongest evidence
in the whole design, because it is the only part that comes from the person choosing.

**One rule, one place.** This check belongs to review-print. prioritize-design reads that
rubric at run time and does not copy it, so a new print verdict sharpens both skills at once.

### 1. Would people like it (appeal, 0 to 10)

Five checks, each 0, 1 or 2, judged from the picture:

| check | 2 | 1 | 0 | why this check |
|---|---|---|---|---|
| reads at size | clear bands and holes at 90 mm | some parts thin or crowded | a mesh of thin lines | review-print check 1 |
| fills its outline | even to the edge | small gaps at the rim | half-empty or big wedges | Omar's verdicts on lEfW, tA8e, n3Ii |
| one clear centre | one star or flower in the middle | a centre, but weak | no centre, or cut off | Printables: the round, centred mandala coasters sit above the tile ones (weak, a handful of models) |
| symmetry | turns and mirrors | turns only, or mirror only | little | Mather 2023: "The majority of people liked high degrees of symmetry the most" |
| busyness | in the middle | a bit sparse or a bit busy | bare, or a dense mesh | Berlyne's inverted U, with the hedges below |

**Hedges the rubric must keep.**

- Complexity has no single best setting for everyone. Güçlütürk 2016 (fetched) found the
  inverted U "comes about as the combination of different individual liking functions": one
  group liked busier images more, the other less. Mather 2023 (fetched) found "most, but not
  all subjects" fell into two groups, one liking high symmetry at any complexity and one
  liking low complexity at any symmetry. A product-design paper (snippet only) found "scant
  evidence for an inverted U-shape." So the busyness check is weak and scores the middle only
  because a coaster seller picks one design for many buyers.
- Those studies used computer-made abstract images, which is why they transfer to flat
  geometric patterns better than studies of paintings would. They say nothing about function,
  material, price or gifting.

**Who can settle it.** Only real buyers can settle it. Until there is a channel, Omar's picks
and print verdicts stand in for them.

### 2. How unusual is it (0 to 10)

Judged against the typical Islamic star coaster: one straight-band star in the middle of a
round or square coaster. Five checks, each 0, 1 or 2:

| check | 2 | 1 | 0 |
|---|---|---|---|
| curves | arcs or petals carry the design | some arcs | straight bands only |
| over-under weave | one closed band that can weave | a woven look without a true weave | none |
| fold family | 7 or 9 | 5 or 10 | 4, 8, 3, 6 or 12 |
| outline | rhombus, √3 rectangle, other | tilted or unusual square | circle, hexagon, square |
| layout | a cut from a field, or a repeat tile | a centre with a strong border | one centre star |

**Evidence.** Hekkert 2003 (abstract fetched) measured how typical a design is as "goodness of
example" and found "people prefer novel designs as long as the novelty does not affect
typicality." That is the reason this score is kept apart from appeal: more unusual is not
automatically better. The fold row leans on one count (snippet only): "48% of 644 Islamic
patterns examined" were in the square four-fold family with mirrors. That does not say how
rare 5, 7 or 10-fold patterns are. The heptagon cannot be drawn exactly with compass and
straightedge (a maths fact); that sevenfold patterns are rarer for that reason is my inference,
not a source.

**How to judge it well.** The Consensual Assessment Technique (snippet only) says judges who
know a field agree well on how novel something is, and also that judges who like a piece tend
to call it novel. So the skill scores "unusual" first, before appeal, and Omar gives his own
"most unusual" tick on the feedback page. Two judges, not a finer formula.

**Who can settle it.** Omar. "Unusual" is a question about the brand as much as the picture:
whether an odd shape or an odd fold is Naqsh Coffee.

### 3. How different is it from what we made (0 to 1)

**How it is scored.** Four facts per design:

- **fold family**: which base angles the star comes from: 4 and 8; 3, 6 and 12; 5 and 10; 7;
  9 and 18;
- **layout**: one centre star, a repeat tile, or a cut from a field;
- **outline**: round, hexagon, square, octagon, heptagon, rhombus, rectangle;
- **lines**: straight or arcs.

Two designs are as similar as the share of the four facts they share (0, 0.25, 0.5, 0.75 or
1). A candidate's **difference** is 1 minus its average similarity to every made coaster. That
is Hekkert's own measure of how typical a thing is, "an exemplar's average similarity to all
other members of the category", with our nine made coasters as the category. The skill also
shows the **nearest** made coaster, since "we have made almost this" is easier to act on than
an average.

**Recompute after every pick.** No made coaster is 5 or 10-fold today, and six of the eight
rebuilds are. The first 10-fold coaster uses up most of that difference for the other five.

**Validator:** the difference tool scores a coaster that is already in the made set.
PASS: CS-2 (7apC5Q9QS-8) scored against the nine made coasters shows CS-2 itself as nearest at
1.00, and its difference is lower than any rebuild's.
FAIL: a tool that leaves the candidate's own row out, or compares fewer than the four facts,
shows CS-2's nearest below 1.00. The limit it cannot catch: NtnlGMTElBk and A9fefFurD_s share
all four facts and so get the same score, though they look different. The picture judgment in
criteria 1 and 2 is what tells them apart.

**Who can settle it.** Nobody needs to: it is arithmetic over facts the repo can hold. What
Omar can change is which facts count and how much each weighs.

### 4. Cost to build now (a tie-break, not a score)

Straight lines only (the arc path is not built), an outline the coaster styles already make,
no crop or mirror step still to decide, and the licence note from the
[candidate screen](../../research/candidate-screen-2026-09-27.md#licence-position) (Broug's book
for A9fefFurD_s, "(c) Eric Broug 2014" on Y6kS1MvnKoc, Bourgoin 1879 in the public domain for
jlTmt_279M4; "not legal advice"). It breaks ties and names the work a design needs first; it
does not rank.

## Who settles what

| question | settled by | until then |
|---|---|---|
| does it read as a coaster | the mesh numbers plus Omar's print verdicts | the rebuild picture |
| would people like it | real buyers (sales, reviews) | Omar's picks and print verdicts |
| is it unusual, and is unusual good for us | Omar | the skill's judgment, marked as a guess |
| how different from what we made | the tool | nothing needed |
| can we build it now | the ledger and the style list | nothing needed |

## What the skill reads and writes

**Reads**

- its rubric (the file next to it) and review-print's rubric;
- the [constructions ledger](../../constructions/ledger.md), for the made set and what each
  candidate still lacks;
- the prototype catalog CS entries and the print records under `docs/prints/`, for what was
  printed and Omar's verdicts;
- the candidate pictures (for the rebuilds, the open-calls media folder) and, once a mesh
  exists, the `print_review.py` sheet;
- the four facts per design, from wherever the checker decides they live (below).

**Writes**

- one feedback page per round through the request-feedback skill: the top candidates as
  pictures, the three scores and the reasons, and tick boxes for "make this first", "most
  unusual to me" and "I disagree with this check";
- after Omar answers: a dated line per round in the rubric's round log, and any change to a
  check or a weight, each with the reason in Omar's words;
- nothing else. It does not edit the ledger, the backlog or review-print's rubric.

**Where the four facts live.** Two choices for the checker:

| option | pros | cons | implications |
|---|---|---|---|
| four new ledger columns (recommended) | one place for facts about a construction; the ledger gate can require them, so the tool never silently skips a row | a gate change and a wider table | every new ledger row needs its four facts before it counts as migrated |
| a table in the rubric | no gate change | facts about constructions stored in a scoring file; can drift from the ledger | the tool must check the table covers every ledger row itself |

The recommendation is the ledger, because a missing fact then fails loudly.

## How a round sharpens the rubric

1. **Run.** The skill scores the candidates and writes the feedback page.
2. **Read back.** Omar ticks and comments. The round log gets: date, the skill's top three,
   Omar's pick, his "most unusual" pick, his reasons.
3. **Change the rubric only from a stated reason.** If his pick was not the skill's top and his
   reason names something no check covers, add a check with his words as its source. If it
   contradicts a check, move that check's weight or scale and say why, dated. A pick with no
   stated reason is logged but moves nothing.
4. **Prints come back.** A keep, adjust or drop from review-print on a design this skill
   ranked is evidence on the appeal checks. Fill failures go to review-print's rubric, which
   this skill already reads.
5. **Keep score of the skill.** After each round, count how often Omar's pick was in the
   skill's top three. If that stays low over several rounds, the weights are wrong; if it
   stays high, the skill can be trusted to sort a long list and Omar only looks at the top.
6. **If a sales channel appears,** units and reviews per design replace Omar's picks as the
   appeal signal, and Omar's tick stays for brand fit.

The starting weights below are a guess, stated as a guess. The first few rounds are what move
them.

## Skill or gate?

Both evaluations the repo asks us to read before building a skill ended "no skill, a gate
instead": the [DSL extension](dsl-extension-skill-evaluation.md) because the real gap was one a
detector could check, the [issue register](issue-register-evaluation.md) because the guards did
the work and nobody read the documents.

It applies here in part:

- **The countable parts become tools and checks, not prose.** Difference from the made set is a
  tool. Fill is `print_review.py`, which exists. The four facts per ledger row can be required
  by the ledger gate.
- **The rest cannot be a gate.** "Would people like it" and "is it unusual" have no right
  answer to test against, so a gate would have no failing case, and the repo's own rule is that
  a gate with no failing case tests nothing.
- **Unlike the register, this output is read by design.** Each run is a feedback page Omar asked
  for and answers, the same reason [request-feedback](request-feedback-evaluation.md) was built.

So: a thin skill, its rubric file, one small tool, and a ledger rule. Not a skill that repeats
review-print.

## Worked example: the eight video rebuilds

Judged from the rebuild pictures on the open-calls page. None of the eight has a naqsh file, so
no `print_review.py` numbers exist yet. gBV_JTt3Kxk is scored as a rhombus coaster (its own
repeat cell), since that is the shape it fills; as a round crop it scores lower (below).

**Appeal (each check 0 to 2)**

| id | reads | fills | centre | symmetry | busyness | appeal /10 | fill check |
|---|---|---|---|---|---|---|---|
| NtnlGMTElBk | 2 | 1 | 2 | 2 | 2 | 9 | passes; ten small gaps between the star points and a round rim |
| gBV_JTt3Kxk | 2 | 2 | 2 | 1 | 2 | 9 | passes as a rhombus |
| jlTmt_279M4 | 2 | 2 | 1 | 1 | 2 | 8 | passes; the most even fill of the eight |
| A9fefFurD_s | 2 | 1 | 2 | 1 | 2 | 8 | passes; big triangles near the rim |
| n_ICgwOr6qs | 2 | 1 | 2 | 1 | 1 | 7 | passes; gaps between petal tips |
| fhGHzop7ULw | 2 | 1 | 0 | 0 | 1 | 4 | borderline; stars cut by the edges |
| _U6G8QSfWnk | 1 | 0 | 0 | 1 | 0 | 2 | **fails**: a quarter-tile fragment; mirror it to the full tile, then rescore |
| Y6kS1MvnKoc | — | — | — | — | — | not scored | **cannot judge**: the picture shows the construction grid, not the pattern; render the pattern alone first |

**Unusual (each check 0 to 2)**

| id | curves | weave | fold family | outline | layout | unusual /10 |
|---|---|---|---|---|---|---|
| jlTmt_279M4 | 0 | 0 | 2 | 1 | 2 | 5 |
| _U6G8QSfWnk | 0 | 0 | 1 | 2 | 2 | 5 |
| n_ICgwOr6qs | 2 | 1 | 1 | 0 | 0 | 4 |
| fhGHzop7ULw | 0 | 0 | 0 | 2 | 2 | 4 |
| NtnlGMTElBk | 0 | 2 | 1 | 0 | 0 | 3 |
| gBV_JTt3Kxk | 0 | 0 | 1 | 2 | 0 | 3 |
| Y6kS1MvnKoc | 0 | 0 | 1 | 0 | 2 | 3 |
| A9fefFurD_s | 0 | 0 | 1 | 0 | 0 | 1 |

**Different from the nine made coasters**

The made set's four facts: CS-1 (6, centre, hexagon, straight), CS-2 (8, centre, square,
straight), CS-6 (7, centre, heptagon, straight), CS-7 (8, centre, octagon, straight), CS-8 (8,
tile, square, straight), CS-9 (18, centre, round, arcs), CS-10 (12, centre, round, straight),
CS-11 (6, tile, hexagon, straight), CS-12 (12, tile, round, straight).

| id | four facts | difference | nearest made |
|---|---|---|---|
| n_ICgwOr6qs | 5/10, centre, round, arcs | 0.72 | CS-9, 0.75 |
| Y6kS1MvnKoc | 5/10, field cut, round, straight | 0.69 | CS-10, 0.50 |
| _U6G8QSfWnk | 5/10, tile, rectangle, straight | 0.69 | CS-8, 0.50 |
| gBV_JTt3Kxk | 5/10, centre, rhombus, straight | 0.61 | CS-1, 0.50 |
| jlTmt_279M4 | 7, tile, square, straight | 0.61 | CS-8, 0.75 |
| fhGHzop7ULw | 3/6/12, tile, rectangle, straight | 0.58 | CS-11, 0.75 |
| NtnlGMTElBk | 5/10, centre, round, straight | 0.53 | CS-10, 0.75 |
| A9fefFurD_s | 5/10, centre, round, straight | 0.53 | CS-10, 0.75 |

**One suggested order.** Starting weights, a guess: appeal counts fully, and difference and
unusual count half each, so that a well-liked design leads and novelty lifts it (the MAYA
reading). Total = appeal + 5 × difference + unusual ÷ 2, out of 20.

| rank | id | appeal | 5 × diff | unusual ÷ 2 | total | to build first |
|---|---|---|---|---|---|---|
| 1= | jlTmt_279M4 | 8 | 3.05 | 2.5 | 13.55 | ready: square, straight lines, public-domain source |
| 1= | gBV_JTt3Kxk | 9 | 3.05 | 1.5 | 13.55 | a rhombus outline, which no coaster style makes yet |
| 3 | NtnlGMTElBk | 9 | 2.65 | 1.5 | 13.15 | ready: round, straight lines, one closed band |
| 4 | n_ICgwOr6qs | 7 | 3.60 | 2.0 | 12.60 | the arc path |
| 5 | A9fefFurD_s | 8 | 2.65 | 0.5 | 11.15 | ready; Broug's book named as the method's source |
| 6 | fhGHzop7ULw | 4 | 2.90 | 2.0 | 8.90 | a rectangle outline |
| — | _U6G8QSfWnk | 2 | 3.45 | 2.5 | (7.95) | held: fails the fill check until mirrored |
| — | Y6kS1MvnKoc | — | 3.45 | 1.5 | — | held: render the pattern alone; a crop to decide; "(c) Eric Broug 2014" |

**What the example says, plainly.**

- The three questions have different winners. Most liked: NtnlGMTElBk and gBV_JTt3Kxk (9).
  Most unusual: jlTmt_279M4 and _U6G8QSfWnk (5). Most different: n_ICgwOr6qs (0.72).
- The top three totals are within 0.4 of each other. Moving any single judged check by one
  point moves a total by 1 (appeal) or 0.5 (unusual), so the order among them is not
  something these scores can settle. Scored as a round crop instead of a rhombus, gBV drops to
  11.15 (fills 1, outline 0, difference 0.53).
- **On 4b.** The scores do not overturn NtnlGMTElBk. They show the choice: jlTmt_279M4 fills its
  shape most evenly, which is the only thing Omar's past verdicts reward, and has the cleanest
  licence; NtnlGMTElBk is the familiar round star with one new thing (a 10-fold weave), the
  "most advanced, yet acceptable" case, but its ten rim gaps are the same kind of fault as
  tA8e's wedges, only smaller. If one must be named: jlTmt_279M4 first, NtnlGMTElBk second. That
  is my reading; the feedback page is where it gets settled.
- **After the first pick.** If NtnlGMTElBk is made, A9fefFurD_s's difference falls from 0.53 to
  0.47 and gBV_JTt3Kxk's from 0.61 to 0.57; jlTmt_279M4 moves from 0.61 to 0.62. If jlTmt_279M4
  is made first, NtnlGMTElBk rises to 0.55 and n_ICgwOr6qs to 0.75.

## Not yet

- The appeal and unusual scores above are one judge (me) from pictures. The feedback page adds
  the second.
- No outside source here measured coasters, decor gifts or Islamic patterns as products. The
  closest are consumer products in general (Hekkert) and generated abstract images (Mather,
  Güçlütürk). The marketplace numbers are hints from free-download sites and snippets, not
  sales.
- The four facts are my reading of the pictures and titles; they are not stored anywhere yet.
