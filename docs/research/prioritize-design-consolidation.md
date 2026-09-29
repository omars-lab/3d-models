---
date: 2026-09-29
produced-by: checker subagent (Claude Opus 5.5), reading both prioritize-design researchers' files after they finished; re-opened the sources behind their load-bearing claims (web fetch, curl, the Crossref, Europe PMC and Printables public APIs), the eight rebuild pictures, the ledger and the bikar coaster outline code
feeds:
  - '[[prioritize-design|the consolidated prioritize-design doc]]'
---

# Prioritize-design: checking the two research passes

Two researchers worked the same question on their own, without reading each other:

- **A**: [research](prioritize-design-research-a.md), [design](../design/process/prioritize-design-a.md),
  with its [Printables sample](prioritize-design-research-a-printables.csv) (PR #425);
- **B**: [research](prioritize-design-research-b.md), [design](../design/process/prioritize-design-b.md) (PR #424).

The question is Omar's, from review thread 952r93 on the
[open-calls page](../working-model/feedback-requests/2026-09-29-open-calls.md) and
[backlog item 5](../tasks/catalog-expansion/backlog.md): how to rank candidate patterns so we
know which becomes a coaster next. The ranking weighs three things: would buyers like it, is it
unusual, and is it different from what we already make and ready to iterate on.

This file records what I re-opened and what I found. The design built from it is
[prioritize-design](../design/process/prioritize-design.md).

**How to read the verdicts.**

- **confirmed**: I opened the source myself and it says what the researcher said.
- **confirmed, with a change**: it says that, plus something the researcher left out that
  changes how the claim should be used.
- **contradicted**: I opened it and it does not say that, or says something else.
- **could not open**: still a search snippet only. It stays flagged, and nothing in the
  design rests on it alone.

## 1. Outside sources

| # | claim | who | source | how I read it | verdict |
|---|---|---|---|---|---|
| 1 | Novel and typical both predict liking, "jointly and equally", and each holds the other back; expertise made no difference; "people prefer novel designs as long as the novelty does not affect typicality" | A, B | Hekkert, Snelders & van Wieringen 2003, *Br J Psychol* 94:111 ([TU/e abstract](https://research.tue.nl/en/publications/most-advanced-yet-acceptable-typicality-and-novelty-as-joint-pred/)) | fetched, abstract | **confirmed**. The abstract does not name the product types studied (A says so; keep that hedge) |
| 2 | Typicality can be measured as "an exemplar's average similarity to all other members of the category" | B | same abstract (Study 3) | fetched, abstract | **confirmed**. This is the ground for B's difference arithmetic |
| 3 | Symmetry preference is stronger for abstract shapes (β = 0.1399), not significant for flowers, reversed for landscapes; weak agreement across categories | A | Bertamini et al. 2019 ([PMC6585942](https://pmc.ncbi.nlm.nih.gov/articles/PMC6585942/)) | fetched, full text | **confirmed** (flowers β −0.0155 n.s., landscapes β −0.0845) |
| 4 | For exact (ordered) fractals, 76% liked more complexity and 24% less; a "surprisingly large" subgroup did not respond to mirror symmetry | A | Bies et al. 2016, *Front Hum Neurosci* ([10.3389/fnhum.2016.00210](https://doi.org/10.3389/fnhum.2016.00210)) | fetched, full text | **confirmed**. The subgroup was about a third in Experiment 2. Transfer hedge: fractals, not Islamic patterns (A says so) |
| 5 | Symmetry, figure–ground contrast and typicality please because they are easy to take in | A | Reber, Schwarz & Winkielman 2004 ([abstract](https://pages.ucsd.edu/~pwinkiel/abs_beauty-PSPR-2004.htm)) | fetched, abstract | **confirmed** |
| 6 | Products with no close look-alike got more clicks, but "the extra clicks distinctiveness recruits convert 5-7% less often downstream"; over 800,000 search events | A | Nguyen, arXiv [2608.21691](https://arxiv.org/abs/2608.21691) | fetched, abstract | **confirmed**, abstract only. The premium roughly doubled when competitors' descriptions were alike. One author (Felicia Nguyen). A preprint, not peer reviewed as far as the page shows |
| 7 | Ease and novelty are "no rivals but rather team players" | A | van Enschot & van Hooijdonk ([VU abstract](https://research.vu.nl/en/publications/reconciling-fluency-theory-and-berlynes-inverted-u-curve-an-exper/)) | fetched, abstract | **confirmed, with a change**: the pictures studied were visual metaphors in advertising, which A did not say. That is further from a coaster than A's text implies |
| 8 | Across more than 1,800 participants in product design, "scant evidence for an inverted U-shape" | A, B (both as snippet) | Althuizen 2021, *Psychology & Marketing* ([10.1002/mar.21449](https://doi.org/10.1002/mar.21449)) | fetched, the publisher's abstract through the Crossref API (Wiley itself gave 403) | **confirmed, with a change** that neither researcher had: "When accounting for the influence of mediators and covariates, aesthetic complexity appeared negatively related to product liking and positively related to perceived originality." Brand status also changed the effect. So busyness pushes "unusual" up and may push "liked" down, which is a reason to keep those two scores apart and not to reward "busy in the middle" inside appeal |
| 9 | 727 effect sizes from 263 samples (1993–2024); "harmony is the strongest property" | A (snippet) | Peng, Eisend & Chen 2025, *J Marketing* ([10.1177/00222429251356484](https://doi.org/10.1177/00222429251356484)) | fetched, abstract through Crossref (Sage gave 403) | **confirmed**, abstract only. Some combinations of conditions turn the effect negative. How "harmony" was defined is still unknown |
| 10 | Symmetry was the strongest cue for "beautiful" in novel graphic patterns, complexity second, with large individual differences | A (snippet) | Jacobsen & Höfel 2002, *Percept Mot Skills* 95:755 ([10.2466/pms.2002.95.3.755](https://doi.org/10.2466/pms.2002.95.3.755)) | fetched, abstract through Europe PMC | **confirmed**, including "a few participants considered nonsymmetric patterns more beautiful" |
| 11 | Both novelty and typicality predict how much people like a website, with novelty's link stronger; typicality mattered more for commercial sites; findings across studies conflict | B | Silvennoinen, Kotkajuuri & Kujala 2025, *IJHCI* ([10.1080/10447318.2025.2576633](https://doi.org/10.1080/10447318.2025.2576633)) | fetched, full PDF | **confirmed** (N = 108, six commercial and six service sites). B's transfer note (websites, so no weight for coasters) is right |
| 12 | Liking of complexity splits into two groups, one liking busier images more and one less; the inverted U "comes about as the combination of different individual liking functions" | B | Güçlütürk, Jacobs & van Lier 2016, *Front Hum Neurosci* ([10.3389/fnhum.2016.00112](https://doi.org/10.3389/fnhum.2016.00112)) | fetched, full text | **confirmed, with a change**: B called the pictures "digitally generated grayscale images". They were 144 grayscale geometric patterns built from circles, hexagons, squares and triangles, which is closer to our patterns than B's wording suggests. 30 participants |
| 13 | "The majority of people liked high degrees of symmetry the most"; 66% of 106 people fell into two groups, one liking high symmetry at any complexity, one liking low complexity at any symmetry; art exposure made group membership less likely | B | Mather et al. 2023, *Sci Rep* 13:21507 ([PMC10700581](https://pmc.ncbi.nlm.nih.gov/articles/PMC10700581/)) | fetched, full text through Europe PMC | **confirmed** |
| 14 | "48% of 644 Islamic patterns examined" were in the square four-fold family with mirrors (p4m) | B (snippet) | *Heritage Science*, "Application-based principles of islamic geometric patterns; state-of-the-art, and future trends in computer science/technologies: a review" ([10.1186/s40494-022-00852-w](https://doi.org/10.1186/s40494-022-00852-w)) | fetched, full article text (curl with a cookie jar; WebFetch got a login page) | **contradicted**: the text I fetched has no "48%" and no "p4m", and "644" appears only inside reference entries. The figure may sit in a table image or come from a cited source (Abas & Salman is cited), but it is not in the text. Also, the paper is dated 2023-02-01, not 2022. B's fold row in "unusual" leans on this number, so that row loses its only outside support |
| 15 | Printed coasters trap spills in their gaps and are hard to clean | A | Rehorst blog ([2020](https://drmrehorst.blogspot.com/2020/10/coasters-anyone.html)) | fetched | **confirmed** |
| 16 | Makes per download on Thingiverse fell from 1 in 474 to 1 in 784 over 500 days | A (snippet) | "500 days of Thingiverse", *Rapid Prototyping Journal* 26(10):1723 | fetched, abstract through Crossref | **confirmed, with a change**: the study followed 30 popular things and says it "does not represent most things on the platform". Add that hedge wherever it is used |
| 17 | Judges who know a field agree well on how novel something is, but novelty ratings are not cleanly apart from liking | B (snippet) | Amabile's Consensual Assessment Technique | a search snippet again, worded a little differently ("strong convergent validity between creativity and novelty but weak discriminant validity with technical goodness and liking") | **could not open**. B's rule "judge unusual before appeal" rests on it alone, so the rule is kept as a cheap habit, not as a finding |
| 18 | A hexagon coaster offers a closed base so drinks do not drip | A (snippet) | Printables model 614926 | the page gave 403; the API summary says only "The hexagon coaster has a diameter of 10cm." | **could not open** |
| 19 | Waterproofing: more top and bottom layers, 3–4 walls, a clear coat | A (snippet) | Siraya Tech blog | not re-checked | **could not open** (not re-tried) |
| 20 | Etsy: Islamic coaster sets, calligraphy and colour among what sells; prices | A, B (snippet) | Etsy market pages | 403 again | **could not open** |
| 21 | Preference rose with the number of mirror lines | B (snippet) | *Symmetry* 12(11):1820 | not re-checked | **could not open** (not re-tried) |
| 22 | MakerWorld download counts | B (snippet) | MakerWorld pages | not re-checked | **could not open** (not re-tried) |

## 2. Printables (A and B both queried it)

Re-queried the public API (`searchPrints2`; the ordering must be a bare word such as
`popular`, not a quoted string) on 2026-09-29:

| search | total the API reports | items checked |
|---|---|---|
| islamic coaster | 1 | 12-Pointed Islamic Star Coaster (231256): 50 likes, 302 downloads, 1 make |
| moroccan coaster | 2 | Zellij Moroccan Tile Coaster (231263): 89, 210, 1 |
| star coaster | 197 | |
| mandala coaster | 63 | Mandala Coaster 154, 800, 8; Lotus Mandala 57, 269, 2 |
| girih | 14 | |
| coaster set | 428 | Disc Brake set 1326, 4879, 63; F1 614, 2953, 18; Monstera 333, 2070, 13; Hexagon set 376, 1396, 30 |
| coaster, by popular | 10,000 (a cap) | Torture Toaster 11,136 likes; sunflower 10,404; leaf 8,607 |

Every figure both researchers quoted matched. A's CSV has 970 rows; 79 names mention flower,
petal, lotus or mandala; one says "12-pointed" and one "5-fold"; none says ten-, seven- or
eight-point, octagon or rectangle. **One small error in A:** A says the four names with
"square" are all Voronoi coasters. Three are; the fourth is a "dual-pattern 2x2 checkered
square coaster". It does not change any conclusion.

Both researchers say the same thing about what this data can carry, and it holds: Printables
likes measure makers choosing a free file, not buyers paying for an object.

## 3. Inside the repo

| claim | who | what I checked | verdict |
|---|---|---|---|
| Rebuild scores: Ntnl 0.930, gBV 0.906, jlTmt 0.941, fhG 0.921, _U6G 0.895, n_IC 0.886, Y6kS 0.861, A9fe 0.855 | A, B | the call 4 table on the open-calls page | **confirmed** |
| Omar's recorded rejections: near-solid (sDO9, nmEj), "felt incomplete" (n3Ii), bare wedges (lEfW, tA8e); `open` ≤ 0.15 and `biggest` ≥ 0.05 are "hints for the eye, not a gate" | A, B | [review-print rubric](../../.claude/skills/review-print/rubric.md), [look-before-you-print](../../.claude/memory/look-before-you-print.md) | **confirmed** |
| The nine made coasters and their outlines: CS-1 hexagon, CS-2 square, CS-6 heptagon, CS-7 octagon, CS-8 square, CS-9 round, CS-10 round, CS-11 hexagon, CS-12 round | A, B | the [ledger](../constructions/ledger.md) and the coaster block of each `.bkr` in `src/Coasters/` | **confirmed**. No made coaster is 5- or 10-fold |
| No coaster style makes a rhombus (B); whether our outlines can draw one "has not been checked" (A) | A, B | bikar's `packages/core/src/kernel3d/coaster-outline.ts`, read in the local bikar-main checkout (not pinned to a ref) | **B confirmed, with a change**: the outline kinds are round, square, polygon (a regular N-gon), lobed and pattern. There is no rhombus or rectangle slab. But the `pattern` kind, where the straps themselves are the footprint (the minimal style), may print a rhombus or rectangle tile with no new outline. I did not try it |
| Ntnl can be woven over-under | A ("assumes it is built over-under"), B (weave row 2) | [coaster styles](../../.claude/skills/import-construction/coaster-styles.md) and bikar's kernel | **open**: no coaster style mentions a weave; bikar's weave code sits in the orb kernel. A woven Ntnl coaster is a build question nobody has answered |
| B's difference numbers (Ntnl 0.53, gBV 0.61, jlTmt 0.61, n_IC 0.72, and the after-pick changes) | B | recomputed from B's four facts | **confirmed**, every figure, including A9fe 0.47 and gBV 0.57 after Ntnl, and Ntnl 0.55 and n_IC 0.75 after jlTmt |
| A's rank sums (Ntnl 6, gBV 6, jlTmt 9.5, A9fe 14, n_IC 15, fhG 16, _U6G 19, Y6kS 22.5) | A | recomputed from A's scores and A's stated rule (tied scores share the average rank; the three "not yet a coaster" or not judged go last on Q2) | **confirmed**. One loose end: A scored Y6kS 1 on Q2 but ranked it with the last three, as "not judged". That is what A's note says; the table's "1" and the rank disagree |
| B says "nothing load-bearing in the design rests on a snippet alone" | B | B's own fold row | **contradicted**: the fold row in B's "unusual" rests on the one snippet in row 14, which I could not find in the source |

## 4. Pictures

I looked at all eight rebuild pictures myself
([media folder](../working-model/feedback-requests/2026-09-29-open-calls-media/)).

- Both researchers describe them the same way, and so would I.
- **One scoring difference matters.** Ntnl (a compact ten-point interlaced star) and A9fe (a
  ten-point medallion) both have deep notches between their points. On a round slab, both
  leave ten wedge gaps at the rim, the same kind of fault Omar rejected in lEfW and tA8e.
  - B scored both "fills its outline" 1. That is consistent.
  - A scored A9fe down for it ("big points leave wedges") but not Ntnl. That is not
    consistent.
  - The consolidated scores apply the fault to both.

## 5. What neither researcher connected

gBV_JTt3Kxk and the made coaster CS-7 (lEfWSogWscs) come from the **same monument**, the
tomb of Itimad-ud-Daula in Agra.

- Both of A's tables name the monument, but A never draws the link.
- B's four facts cannot see it, because the two differ on fold (10 against 8) and outline.

Whether a buyer would see the pair as a set or as a repeat is a taste question. But "different
from ours" should show it, so the design adds a free-text "same source as" note beside the
nearest made coaster.

## 6. Agreement, disagreement, and what only one found

**Both found (independent agreement, the strongest evidence here)**

- The repo names no customer, shop or price. The licence note says "If coasters are sold".
- Keep the three questions as three scores, not one blended number, because liked and unusual
  pull against each other (Hekkert).
- Check "reads as a coaster" before any score, from Omar's own rejections.
- Complexity has no single best level for everyone. Symmetry is a small plus.
- Printables measures makers, not buyers. Islamic star coasters are rare there.
- No made coaster is 5- or 10-fold.
- "Different" means comparing against the made set and showing the nearest made coaster.
- The data about each pattern (fold, outline, lines) is stored nowhere today, so a tool or new
  ledger columns are needed.
- The countable parts become tools. Appeal and unusual are judgment.
- A thin skill that writes a request-feedback page, not a gate. The precedent is
  request-feedback, not the two "no skill, a gate instead" evaluations.
- It learns from Omar's picks, then prints, then sales.
- _U6G fails as it stands. Y6kS cannot be judged from its picture. fhG is weak. A9fe is lower
  and needs a licence check.
- Both researchers put Ntnl, gBV and jlTmt in the top three.

**They disagree**

| on | A | B | which the evidence supports |
|---|---|---|---|
| how to combine | add the three ranks, equal weight | appeal + 5 × difference + unusual ÷ 2 | neither weight has a source; both say so. A's rank sum needs no weight nobody can source. The consolidated doc uses it and shows B's total beside it |
| first pick | Ntnl (a tie with gBV, broken on 0.930 against 0.906) | jlTmt, with Ntnl second, "my reading", within 0.4 | with the wedge fault scored the same way for Ntnl and A9fe, jlTmt leads or ties in three of four readings (see the design doc) |
| how different jlTmt is | 0 new features (7-fold and square are both made) | 0.61, because its layout (a repeat tile) and fold family differ from the nearest made coasters | B. A's own doc says its count "cannot see what the eye does" for jlTmt. B's average similarity is Hekkert's measure (row 2) |
| what "unusual" is scored against | coaster names on Printables (a fetched sample) | a checklist: curves, weave, fold family, outline, layout | A. B's fold row rests on the contradicted row 14, and most of B's other rows repeat the "different" facts |
| readiness to build | part of Q3's score | a tie-break only | B. A's version counts "round" twice (fits its outline, and again as readiness) and ranks ease above the question asked. Omar's "that we can iterate on" is kept as the tie-break and as listed work |
| rhombus outline for gBV | unchecked | no style makes one | B, with the change in §3: the minimal style might |
| busyness | no "not too complex" part | a busyness part scoring the middle best | A. Althuizen (row 8, now fetched) found complexity lowers liking and raises originality once other factors are held; Güçlütürk and Mather show no shared middle |

**Only A found**

- Nguyen's click-versus-sale result.
- Bies's 76/24 split. Bertamini's category result.
- The licence as a sell flag beside the name.
- Drips and cleaning as a style question, not a ranking one.
- Interlace as a new line type.
- The retire rules: three rounds with every pick different; rebuilds rarer than monthly.

**Only B found**

- Silvennoinen, Güçlütürk and Mather.
- Typicality as average similarity, and the arithmetic built on it.
- Recompute "different" after every pick.
- A Validator for the tool, with pass and fail cases.
- Storing the four facts as ledger columns so a gate can require them.
- Tracking how often Omar's pick lands in the top three.
- Judging "unusual" before appeal.

**Only the checker found**

- Althuizen's result that complexity lowers liking and raises originality (row 8).
- The Heritage Science figure is missing from its source (row 14).
- The shared monument of gBV and CS-7 (§5).
- The inconsistent wedge scoring for Ntnl (§4).
- The `pattern` outline kind as a possible route for tile shapes (§3).

## 7. Search scope

I re-opened only the sources behind load-bearing claims in the two design docs. I ran no new
literature search. Anything neither researcher looked at is still unlooked-at.
