---
date: 2026-09-29
produced-by: researcher A subagent (Claude Opus 5.5), one of two independent researchers; did not read researcher B's files
feeds:
  - '[[prioritize-design-a|the prioritize-design design doc]]'
---

# What makes a coaster design worth making next: raw findings (researcher A)

Omar asked on 2026-09-29 for a `prioritize-design` skill that looks at candidate coaster
designs and guesses three things: which one customers would like most, which is most unusual,
and which is most different from the coasters already made, "that we can iterate on"
([backlog item 5](../tasks/catalog-expansion/backlog.md)). This file is the raw research
behind the proposed design, [prioritize-design-a](../design/process/prioritize-design-a.md).

Every outside claim below names its source and says how I read it:

- **fetched**: I opened the page and read it (for papers, usually the abstract page, not the
  full text; that is said where it matters);
- **snippet**: I saw only a search-result snippet, because the page refused me (403, a
  cookie wall, or a page drawn by script). A snippet claim is weaker and is flagged as such.

## 1. Sources and how each was read

| # | Source | Read as | What it gives us |
|---|---|---|---|
| S1 | Hekkert, Snelders & van Wieringen 2003, "'Most advanced, yet acceptable': typicality and novelty as joint predictors of aesthetic preference in industrial design", *British Journal of Psychology* 94:111–124 ([TU/e page](https://research.tue.nl/en/publications/most-advanced-yet-acceptable-typicality-and-novelty-as-joint-pred/)) | fetched (abstract page); the PubMed and Wiley pages refused me | novel and typical both raise liking, and each holds the other back |
| S2 | Bertamini, Rampone, Makin & Jessop 2019, symmetry preference across categories ([PMC6585942](https://pmc.ncbi.nlm.nih.gov/articles/PMC6585942/)) | fetched (full text) | people prefer symmetry in abstract shapes; the effect is small and people differ a lot |
| S3 | Bies, Blanc-Goldhammer, Boydston, Taylor & Sereno 2016, "Aesthetic responses to exact fractals driven by physical complexity" ([Frontiers](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2016.00210/full)) | fetched (full text, read through a summarising fetch) | for ordered patterns, most people like more complexity; a quarter like less |
| S4 | Reber, Schwarz & Winkielman 2004, "Processing fluency and aesthetic pleasure", *Personality and Social Psychology Review* 8:364–382 ([abstract](https://pages.ucsd.edu/~pwinkiel/abs_beauty-PSPR-2004.htm)) | fetched (abstract) | symmetry, contrast and typicality please because they are easy to take in |
| S5 | Nguyen, "Contextual Visual Distinctiveness in Online Product Search", arXiv 2608.21691 ([abstract](https://arxiv.org/abs/2608.21691)) | fetched (abstract page) | a measured "unusual": image distance to the nearest look-alike. It raises clicks, not sales |
| S6 | van Enschot & van Hooijdonk, fluency theory and Berlyne's inverted U ([VU page](https://research.vu.nl/en/publications/reconciling-fluency-theory-and-berlynes-inverted-u-curve-an-exper/)) | fetched (abstract page) | ease and novelty work together, "no rivals but rather team players" |
| S7 | Althuizen 2021, "Revisiting Berlyne's inverted U-shape relationship between complexity and liking", *Psychology & Marketing* ([Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/mar.21449)) | **snippet** (403) | across product-design studies, "scant evidence" for the inverted U |
| S8 | Peng, Eisend & Chen 2025, "A meta-analysis of product visual aesthetics", *Journal of Marketing* ([doi](https://doi.org/10.1177/00222429251356484)) | **snippet** (403 at Sage, ResearchGate, DeepDyve) | harmony is the strongest single look property |
| S9 | Jacobsen & Höfel 2002, beauty judgments of novel graphic patterns, *Perceptual and Motor Skills* 95:755 ([doi](https://doi.org/10.2466/pms.2002.95.3.755)) | **snippet** (the doi redirects to Sage, not fetched) | symmetry was the strongest cue for "beautiful", complexity second |
| S10 | Rehorst, "Coasters, anyone?" ([blog, 2020](https://drmrehorst.blogspot.com/2020/10/coasters-anyone.html)) | fetched | a printed coaster's gaps trap spills and are hard to clean |
| S11 | Printables model 614926, "Hexagon coaster" ([page](https://www.printables.com/model/614926-hexagon-coaster)) | **snippet** (403) | offers a closed-base option so drinks don't drip through |
| S12 | Siraya Tech, 3D-printed coasters ([blog](https://siraya.tech/blogs/news/3d-printed-coasters)) | **snippet** | more top and bottom layers, 3–4 walls and a clear coat for a waterproof coaster |
| S13 | Etsy market pages, Islamic coasters ([islamic_coasters](https://www.etsy.com/market/islamic_coasters) and related) | **snippet** (every Etsy page returned 403) | what sells: sets, colour, calligraphy, gift framing |
| S14 | "500 days of Thingiverse", *Rapid Prototyping Journal* 26(10):1723 ([Emerald](https://www.emerald.com/rpj/article-abstract/26/10/1723/367784/500-days-of-Thingiverse-a-longitudinal-study-of-30?redirectedFrom=PDF)) | **snippet** | how downloads and makes relate on a maker site |
| S15 | Printables public search API, 20 search terms, pulled 2026-09-29T22:55Z (§4) | fetched (raw data, 970 models) | what makers like among coasters, and how rare Islamic patterns are there |
| R1 | This repo: catalog, ledger, coaster styles, print records, the review-print rubric, Omar's memory notes, the open-calls page (§5) | read | the made set, the only reactions on record, and the candidates |

Pages I could not read at all, so nothing below rests on them: MakerWorld search (403),
Thingiverse search (drawn by script, empty to a fetch), PubMed (cookie wall).

## 2. Findings from outside: what people like to look at

**Novel, but still recognisable (S1, fetched abstract).** Typicality and novelty "jointly and
equally" predict how much people like a consumer product's look, and each suppresses the
other's effect: "people prefer novel designs as long as the novelty does not affect
typicality." Design expertise did not change this. The abstract page does not name the
product types studied, so I cannot say whether small home goods were among them.

- *Transfers because* a coaster is a consumer product judged mostly by its look at a glance,
  which is the judgment S1 studied. What does not transfer is any number: S1 gives a
  direction, not a weight.
- *Consequence for the skill:* "most unusual" should only count for a piece that still reads
  as a coaster. An unusual fragment is not a win.

**Symmetry helps, a little, and people differ (S2 fetched, S9 snippet, S4 fetched abstract).**
S2 found a general preference for symmetry that is stronger for abstract shapes (β = 0.1399,
p < 0.001), not significant for flowers, and reversed for landscapes. Agreement across
categories was weak and individual differences were strong. S9 (snippet only) reports
symmetry as the strongest cue for "beautiful" in novel graphic patterns, complexity second,
also with substantial individual differences. S4 explains why: symmetry, figure–ground contrast,
repetition and typicality make an image easier to take in, and ease feels like beauty.

- *Transfers because* our patterns are abstract line shapes, the category where S2's effect
  was strongest. The effect is small, so symmetry is a tie-breaker, not a winner-maker.
- Every candidate we have is symmetric, so this check mostly separates **centred** pieces
  (symmetric about the coaster's middle) from **off-centre fragments** (a tile corner, a
  half-star), which is also what Omar's "felt incomplete" rejection names (§5).

**Complexity: more is usually fine for ordered patterns, with a floor and no agreed peak
(S3 fetched, S6 fetched abstract, S7 snippet).** S3 found that for exact (ordered)
fractals, 76% of participants liked higher complexity more, while 24% liked it less; a
"surprisingly large subgroup" did not respond to mirror symmetry at all. This runs against
the older finding that moderate complexity is best, which came from statistical fractals such
as natural scenes. S7 (snippet only) reports, across studies with over 1,800 participants in
product design, "scant evidence for an inverted U-shape"; complexity mattered through
interest and through how much effort or skill the maker seemed to put in. S6 found that ease
of reading and novelty work together rather than against each other.

- *Transfers because* Islamic geometric patterns are ordered, repeating line geometry,
  closer to S3's exact fractals than to natural scenes. They are not fractals, so this is a
  direction hint only.
- *Consequence:* there is no outside number for "just complex enough". The working floor is
  Omar's own: near-solid and half-empty pieces are rejected (§5). "Looks like it took skill"
  (S7, snippet) is a plausible reason intricate stars appeal, and it is untested here.

**Harmony (S8, snippet only).** A meta-analysis of 727 effect sizes from 263 samples
(1993–2024) reports that product looks raise consumer attitudes and behaviour, and that
harmony is the strongest single property. I could not open it, so I do not know how
"harmony" was defined. Flagged, not relied on.

## 3. Findings from outside: what "unusual" means, and whether it sells

**A measurable version (S5, fetched abstract).** Nguyen measures a product's visual
distinctiveness as the image distance from its nearest similar alternative in the set a
shopper sees, using image embeddings, over about 800,000 e-commerce search events. Products
with no close look-alike got more clicks, and the premium grew when the text descriptions of
competitors were similar. But those extra clicks converted about 5–7% less often: being
distinct pulled attention, it did not make the product more wanted.

- *Transfers because* the method (distance to the nearest neighbour) needs only pictures of
  the candidates and of the comparison set, which we have. The finding transfers as a
  warning, from online shopping in general: "unusual" and "sells" are separate questions,
  so the skill should answer them separately rather than folding them into one score.
- The same nearest-neighbour idea answers Omar's third question: compare a candidate to the
  **closest** coaster we already made, not to the average of them.

## 4. Findings from marketplaces

### 4.1 Printables (S15, fetched through the public API)

I queried the Printables public GraphQL search (`searchPrints2`) for 20 terms, each by
"popular" and by "makes_count", up to 100 results each, 970 distinct models in all. The
one-off script is reproduced at the end of this section, and the models are saved as
[prioritize-design-research-a-printables.csv](prioritize-design-research-a-printables.csv)
(id, name, likes, downloads, makes, date, and the terms that found it).

Total matches per term, as the API reported them:

| term | models | term | models |
|---|---|---|---|
| coaster | 10,000 (probably the API's cap) | geometric coaster | 51 |
| coaster set | 428 | tile coaster | 50 |
| star coaster | 197 | moroccan | 49 |
| celtic coaster | 172 | geometric pattern | 47 |
| hexagon coaster | 117 | girih | 14 |
| pattern coaster | 74 | islamic pattern | 6 |
| mandala coaster | 63 | arabic coaster | 4 |
| multicolor coaster | 61 | zellige | 4 |
| voronoi coaster | 55 | moroccan coaster | 2 |
| | | islamic geometric | 2 |
| | | islamic coaster | 1 |

What the sample shows:

- **Islamic geometric coasters are rare there.** "islamic coaster" finds one model,
  "12-Pointed Islamic Star Coaster" (id 231256, 2022: 50 likes, 302 downloads, 1 make).
  "moroccan coaster" finds "Zellij Moroccan Tile Coaster - MMU & Multipart" (id 231263: 89
  likes, 210 downloads) and a football logo. "girih" finds Arabesque (Girih) coasters and a
  trivet with 1–9 likes each.
- **Fold is almost never named.** Across all 970 names, none mention a ten-point, ten-fold,
  seven-point, eight-point or octagon star; one mentions 12-pointed; one mentions 5-fold (a
  Penrose braid). None mention a rectangle; the four that mention "square" are Voronoi
  coasters; none of the three "diamond" names is a coaster. This is a search over names in
  this sample only, not over pictures, so it says what makers call things, not what exists.
- **The most-liked coasters are not geometric art.** The top of the "coaster" list by
  popularity is a joke print (The Torture Toaster, 11,136 likes), a sunflower fabric coaster
  (10,404), leaf coasters with a plant holder (8,607), a "printing in progress" coaster, woven
  and fabric coasters, a Celtic coaster with a holder (3,010), record and pallet coasters,
  Pokémon, F1, Halloween and Star Wars sets. Several are sold as a set or come with a holder.
  The best-liked patterned ones are Voronoi (881 likes for the top one), a hexagonal design
  (877), "Wave Coasters" (878), snowflakes (677) and a Moiré coaster (441).
- **Flower and mandala forms are common**: 79 of the 970 names mention flower, petal, lotus or
  mandala; "mandala coaster" alone has 63 matches.

*How far this transfers (K10).* Printables likes and downloads measure **makers choosing a
free file to print**, not buyers paying for an object. S14 (snippet only) found on
Thingiverse that makes per download fell from 1 in 474 to 1 in 784 over 500 days, so even
downloads overstate how often something is actually made. So the Printables sample says two
things with some confidence: an Islamic star coaster is **unusual** among shared coaster
files, and there is **little evidence of demand** there either way. It says little about
what a paying customer would pick.

The one-off pull script (run once, 2026-09-29; the API has no published schema and rejects
introspection; `popular`, `makes_count` and `latest` are the orderings it accepted):

```python
TERMS = ["coaster", "geometric coaster", "islamic coaster", "moroccan coaster", "arabic coaster",
         "mandala coaster", "star coaster", "hexagon coaster", "celtic coaster", "voronoi coaster",
         "pattern coaster", "tile coaster", "coaster set", "multicolor coaster", "girih",
         "islamic pattern", "islamic geometric", "geometric pattern", "moroccan", "zellige"]
Q = ('{ searchPrints2(query: %s, limit: 100, ordering: %s) { totalCount items { id name slug '
     'likesCount downloadCount makesCount datePublished } } }')
# for each term and ordering in ("popular", "makes_count"):
#   POST https://api.printables.com/graphql/ with {"query": Q % (json.dumps(term), ordering)}
```

### 4.2 Etsy (S13, snippet only)

Every Etsy page returned 403, so this rests on search snippets. Listings seen in snippets
included "Islamic Coaster Set of 5 | Arabic Calligraphy … 3D Printed" (104 reviews, $35,
marked bestseller) and "Esfahan Tile Coaster Set • Persian Mandala-Inspired" (343 reviews,
colourful). Snippet reviews praised the colours and a clear design. Ceramic, metal and cork
coasters appear beside printed ones, and listings lean on gifts and occasions (Ramadan, Eid,
housewarming) and on calligraphy.

*Transfers because* these are objects people paid for, the closest thing to "customers" in
this research. But it is snippet-level, from one marketplace, and the leading listings use
calligraphy and colour, which are not pattern choices. What it suggests for the skill is
narrow: **sets** and **colour** show up among the listings that sell. A pattern that makes a
good set (a tile that repeats edge to edge) or takes colour well (the fill style) may matter
more to a buyer than which star it is. That is a guess to test, not a finding.

### 4.3 Using a coaster (S10 fetched, S11 and S12 snippet)

Rehorst (fetched): patterns and a rim lip trap condensation, "spills will inevitably find
tiny gaps between lines in the print that can't be properly cleaned out", keep a pattern
shallow in height, and be careful with hot drinks on PLA. S11 (snippet) offers a closed base
so drinks don't drip through; S12 (snippet) recommends more top and bottom layers, 3–4 walls
and a clear coat.

*Transfers because* this is about printed coasters, the same product. But it bears on the
**style** (an openwork style such as minimal lets water through; plain has a solid base),
not on which pattern to pick. So it belongs in the style choice after a pattern is chosen,
not in the pattern ranking.

## 5. Findings inside the repo

**No customer or sales channel is stated.** A search of `docs/`, `.claude/memory/`,
`CLAUDE.md`, `README.md` and `index.html` for etsy, customer, sell, sales, gift, price, buyer
and shop found no stated customer, shop or price. Naqsh Coffee appears as the domain and
Cloudflare organisation of the studio site. The word "customers" appears only in Omar's
request itself. The candidate screen's licence note is conditional, "If coasters are sold"
([candidate-screen-2026-09-27](candidate-screen-2026-09-27.md#licence-position)). So the
customer is unstated, and I do not assume one.

**The only reactions on record are Omar's.**

- Pieces left off a plate on sight (the [review-print rubric](../../.claude/skills/review-print/rubric.md),
  minis-03, 2026-09-25): sDO9 and nmEj as near-solid ("mostly solid disks are not good
  coasters"), n3Ii as half-filled ("felt incomplete"), lEfW and tA8e for bare wedges ("lots
  of weird empty space"). The rubric's measured hints: `biggest` ≥ 0.05 flagged both gross
  gaps and `open` ≤ 0.15 flagged both near-solid pieces, over nine pieces, "too few to set a
  pass line".
- Printed pieces ([minis-03](../prints/2026-09-26-minis-03/index.md),
  [minis-04](../prints/2026-09-26-minis-04/index.md)): every verdict is "adjust". The notes
  include "good start: the pattern reads", "much too small at 40 mm", a pegs border too wide,
  and tiny holes from a slicer fallback.
- Omar's memory note [look-before-you-print](../../.claude/memory/look-before-you-print.md):
  "fewer good pieces beat full coverage".

**Pictures can mislead about openness.** The candidate screen judged coaster fit from
thumbnails; bknV and n3Ii looked open in the video yet read near-solid at 90 mm
([candidate-screen-2026-09-27](candidate-screen-2026-09-27.md)). So a picture-only score for
"reads as a coaster" is provisional until the piece is rendered at size.

**The made set.** Nine patterns have a coaster file in `src/Coasters/` (plain style shown;
most have more styles). All nine are Sarah Brewer GeoGebra rebuilds
([ledger](../constructions/ledger.md)):

| coaster | construction | fold | outline | lines | kind |
|---|---|---|---|---|---|
| CS-1 | GimTvN9hw4U | 6 | hexagon | straight | star rosette |
| CS-2 | 7apC5Q9QS-8 | 8 | square | straight | rosette |
| CS-6 | tA8eSdVx_EQ | 7 | heptagon | straight | star rosette |
| CS-7 | lEfWSogWscs | 8 | octagon | straight | rosette (Itimad-ud-Daula tomb) |
| CS-8 | rDuxHF3xMOc | 8 | square | straight | star rosette |
| CS-9 | nmEjCTzMbDg | 18 | round | arcs | flower; renders near-solid |
| CS-10 | n3IidKfXE1I | 12 | round | straight | 12-6-4 rosette |
| CS-11 | sDO9fpu76v8 | 6 | hexagon | straight | tessellation (repeat tile) |
| CS-12 | bknVRSMcLj0 | 12 | round | straight | kite tile, one repeat cell |

Made folds: 6, 7, 8, 12, 18. Made outlines: hexagon, square, heptagon, octagon, round. No
5-fold or 10-fold coaster exists, and no rectangle or rhombus outline.

**The candidates** are the eight video rebuilds of [D-084](../working-model/decisions-log.md),
shown as video, rebuild and difference on the
[open-calls page](../working-model/feedback-requests/2026-09-29-open-calls.md) call 4. What I
saw in each picture, and what the backlog says:

| video | creator | what it is | score (steps) | what I saw |
|---|---|---|---|---|
| NtnlGMTElBk | Samira Mian | Mustansiriya 10-fold interlaced star, one closed band of 40 segments | 0.930 (13/13) | a clean, compact interlaced star; open centre |
| A9fefFurD_s | Lex Wilson, from Broug's book | ten-point star medallion | 0.855 (17/17) | star within star, a jagged outer edge of big points |
| n_ICgwOr6qs | Samira Mian | ten petals from one compass setting, five-fold as drawn, all arcs | 0.886 (9/9) | an overlapping-petal flower; holes of very different sizes |
| gBV_JTt3Kxk | Samira Mian | Itimad-ud-Daula ten-fold rosette in a 72° rhombus tile | 0.906 (11/11) | a ten-point star that fills its rhombus |
| _U6G8QSfWnk | Samira Mian | Sutton's fivefold rectangle, ten-point stars at opposite corners | 0.895 (6/6) | two half-stars; looks unfinished alone |
| fhGHzop7ULw | Mohamad Aljanabi | six-fold 1 × √3 rectangle from Baghdad | 0.921 (9/9) | stars cut by the rectangle edge; big uneven holes |
| jlTmt_279M4 | Bourgoin pl. 170 | four seven-point stars and octagons in a tilted square tile | 0.941 (17/17) | a dense, even square that fills its outline |
| Y6kS1MvnKoc | Eric Broug | Mamluk Qur'an page, seven ten-point stars, 1.376 rectangle | 0.861 (17/18) | the picture shows the circle scaffold; the pattern itself is hard to see |

The licence notes come from the candidate screen's licence section, which is the researchers'
reading and not legal advice: videos are presumed standard YouTube licence (rebuild, don't
copy frames); A9fefFurD_s follows Broug's book, which adds his copyright; Bourgoin (1879,
jlTmt_279M4) is public domain.

**Precedent.** Two process evaluations in this repo
([dsl-extension-skill-evaluation](../design/process/dsl-extension-skill-evaluation.md),
[issue-register-evaluation](../design/process/issue-register-evaluation.md)) concluded "no
skill, a gate instead": each found a *missing check*. A third,
[request-feedback-evaluation](../design/process/request-feedback-evaluation.md), concluded
"yes, a skill", because the missing thing was a way of *writing* and "a gate cannot write a
page". The review-print skill already keeps a rubric next to it that grows as prints come
back. Among the skills in `.claude/skills/` on 2026-09-29, none ranks rebuilt constructions
for which becomes a coaster: review-print judges a piece already chosen for a plate,
review-design judges a design *document's* readability, and find-model finds other people's
models to print.

## 6. What this research does not settle

- **What a paying customer likes.** Nothing here measures it for this product. The lab
  studies (S1–S4) are about looks in general; Printables is makers; Etsy is snippets.
- **The weights.** No source gives a number for how much symmetry, complexity or novelty
  should count for a coaster.
- **Whether "unusual" helps sales.** S5 suggests it draws attention without raising
  conversion, in online shopping in general.
- **Openness at size.** None of the eight candidates has a coaster file yet, so none has been
  measured with the print-review numbers.
