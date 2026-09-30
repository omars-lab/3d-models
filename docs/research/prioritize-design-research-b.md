---
date: 2026-09-29
produced-by: researcher B subagent (Claude Opus 5.5), one of two independent prioritize-design researchers; web search and fetch, the Europe PMC and Printables public APIs, and a read of this repo's ledger, prints, skills and open-calls page
feeds:
  - '[[prioritize-design-b]]'
---

# Prioritize-design research B: what makes a coaster design worth making next

The raw findings behind [`../design/process/prioritize-design-b.md`](../design/process/prioritize-design-b.md).

**The question.** Omar asked on 2026-09-29 for a skill that reviews candidate coaster designs
and guesses three things: which one customers would like most, which is most unusual, and
which is most different from the coasters already made. His words, on call 4b of the
[open-calls page](../working-model/feedback-requests/2026-09-29-open-calls.md): "How do we add
a good skill that reviews coasters ... and tries to guess which one customes would like the
most? which one is more unqiue? which one is diffferent thatn the ones we've done before, etc?
... we should have a prioritize-design skill that we can iterate on."

**How to read the source marks.** Every outside source says whether I **fetched** it (read the
text itself) or saw only a **snippet** (a line or two a search engine showed, which can be out
of context). Nothing load-bearing in the design rests on a snippet alone. Quotes are short;
everything else is paraphrase.

## 1. Who the customer is: nothing stated

A search of `docs/` and `.claude/` for shop, Etsy, customer, retail, sell and price found no
stated customer and no sales channel. The nearest things:

- The [README](../../README.md) describes a public gallery of the models and the repo's start
  as Islamic cookie cutters.
- The candidate screen's licence section is conditional: "**If coasters are sold.** A rebuild
  from a video is the route every Brewer coaster took." ([candidate-screen-2026-09-27](candidate-screen-2026-09-27.md#licence-position))
- The owner runs Naqsh Coffee (from the brief, not from the repo).

So "what customers like" has no customer data behind it today. Until there is a channel, the
only buyer-side signal the repo has is Omar's own verdicts on printed pieces.

## 2. Outside sources

### 2.1 Novelty and typicality together (MAYA)

**Hekkert, Snelders & van Wieringen 2003**, "'Most advanced, yet acceptable': typicality and
novelty as joint predictors of aesthetic preference in industrial design", *British Journal of
Psychology* 94:111–124. PubMed 12648393. **Fetched** (the abstract, through the Europe PMC API;
the PubMed page itself wanted cookies, and the full text was not read).

- "typicality (operationalized as 'goodness of example') and novelty are jointly and equally
  effective in explaining the aesthetic preference of consumer products, but that they
  suppress each other's effect."
- "Direct correlations between both variables and aesthetic preference were not significant,
  but each relationship became highly significant when the influence of the other variable was
  partialed out."
- "the expertise level of observers did not affect the relative contribution of novelty and
  typicality."
- Study 3: "a more 'objective' measure of typicality, central tendency - operationalized as an
  exemplar's average similarity to all other members of the category - yielded the same
  effect".
- "people prefer novel designs as long as the novelty does not affect typicality ... Preferred
  are products with an optimal combination of both aspects."

**What this gives the skill.** Two things. First, "unusual" and "liked" are not the same
score, and a design that is unusual in a way that makes it stop looking like a coaster (or
like an Islamic star) loses. Second, "average similarity to all other members" is a
measurable definition of how typical something is, and it is the same arithmetic as "how
different is this from what we made", with the made set as the category.

**Silvennoinen, Kotkajuuri & Kujala 2025**, "The Effect of Novelty and Typicality on Aesthetic
Appeal of Websites", *International Journal of Human–Computer Interaction*, doi
10.1080/10447318.2025.2576633, CC BY 4.0. **Fetched** (the full PDF from jyx.jyu.fi).

- N = 108 people rated six commercial and six service websites.
- "both novelty and typicality predict website aesthetic appeal, supporting the MAYA
  principle. However, the connection between novelty and aesthetic appeal is stronger".
- Typicality mattered more for the commercial websites.
- It lists where MAYA has been studied: "paintings, colors, furniture, music, industrial
  machinery, and product and service branding."
- It keeps a hedge the design must keep: "research has produced conflicting findings regarding
  preferences for typicality and novelty."

Transfer: the websites result (novelty's link is stronger) was measured on websites, not
objects, so it does **not** tell us to weight novelty above typicality for coasters. What
transfers is the general finding that both count and pull against each other. It transfers
because Hekkert's own studies used consumer products, which is closer to a coaster than a
website is.

### 2.2 Complexity: the inverted U, and why it splits

**Güçlütürk, Jacobs & van Lier 2016**, "Liking versus Complexity: Decomposing the Inverted
U-curve", *Frontiers in Human Neuroscience* 10:112, doi 10.3389/fnhum.2016.00112, CC BY.
**Fetched** (full text through the Europe PMC API).

- 30 participants rated "digitally generated grayscale images" for liking and complexity.
- "one group of participants in our sample had increasingly lower liking ratings for
  increasingly more complex stimuli, while a second group of participants had increasingly
  higher liking ratings for increasingly more complex stimuli."
- The inverted U "comes about as the combination of different individual liking functions."
- It cites Nadal et al. 2010: studies that varied complexity found "not always" an inverted U
  but "sometimes increasing, decreasing or U-shaped" curves.

**Mather, Aleem, Rhee & Grzywacz 2023**, "Social groups and polarization of aesthetic values
from symmetry and complexity", *Scientific Reports* 13:21507, doi 10.1038/s41598-023-47835-w,
CC BY 4.0. **Fetched** (full text through the Europe PMC API; nature.com redirected to a
login and PMC showed a captcha).

- The images were generated to vary symmetry and complexity on purpose.
- "The majority of people liked high degrees of symmetry the most and the preferred
  complexities exhibited a statistically significant rise-then-fall histogram".
- But: "most, but not all subjects, formed two distinct natural clusters, termed 'islands'".
  "Most subjects (66%) divided themselves between the two islands" (n = 106).
- The Symmetry-Island "preferred all ranges of complexity if the degree of symmetry was high";
  the Simplicity-Island "preferred all ranges of degree of symmetry if the complexity was low".
- "people with more art exposure were less likely to belong to an island." Gender shifted
  which island people fell in.

**Symmetry 12(11):1820** (MDPI; title not recorded). **Snippet only**: preference rose
steadily with the number of mirror lines.

**"Revisiting Berlyne's inverted U"** (Wiley, *Psychology & Marketing*, article mar.21449).
**Snippet only**: across more than 1,800 participants in product design, "scant evidence for
an inverted U-shape". Neither WebFetch nor the Europe PMC API returned it.

**What this gives the skill.** Symmetry is the best-supported single cue: most people like
more of it. Complexity is not a dial with one best setting; people split into groups that want
opposite things. Transfer: these studies used generated abstract images, which is closer to a
flat geometric pattern than paintings or photos are, and that is why they transfer better than
most aesthetics work. They say nothing about function, material, price or gifting. And a
coaster seller picks one design for many buyers, so the split means any one design will lose
part of the audience; a small set with one busy and one calm design covers both groups.

### 2.3 Judging "unusual"

**Amabile's Consensual Assessment Technique** (1982 onward). **Snippet only** (search summary;
the ResearchGate PDF was not fetched): judges who know a domain rate creativity by their own
sense of it, not a checklist, and agree with each other well. The summary adds that ratings of
creativity and novelty agree closely, but are not cleanly separated from technical goodness
and liking.

Use: the "unusual" score in the skill is a judged score, and the way to make a judged score
trustworthy is more than one judge (the skill plus Omar), not a finer formula. The snippet's
last point also warns that a judge who likes a piece tends to call it novel, so the skill
should judge "unusual" before it judges appeal.

### 2.4 How common each fold is among Islamic patterns

**Heritage Science 2022**, "Application-based principles of Islamic geometric patterns ..." (title cut off in the snippet),
doi 10.1186/s40494-022-00852-w (via nature.com). **Snippet only** (nature.com redirected to a
login): "48% of 644 Islamic patterns examined" had the p4m symmetry group, the square
four-fold family with mirrors.

Use, hedged: square-family (4 and 8-fold) patterns look like the most common kind in that one
count. It does not say how common 5, 7 or 10-fold patterns are, so the skill cannot claim they
are rare from this source; it can say they are not the family this count found most often.

### 2.5 Marketplaces

**Printables public API** (api.printables.com/graphql, query `searchPrints2`, top results
by the site's own relevance order, not by popularity). **Fetched** on 2026-09-29. Likes,
downloads and makes (people who posted a print of it):

| search | model | likes | downloads | makes |
|---|---|---|---|---|
| coaster set | Disc Brake Coaster Set | 1326 | 4879 | 63 |
| coaster set | Formula 1 Coaster Set - F1 Logo | 614 | 2953 | 18 |
| coaster set | Monstera Coaster Set | 333 | 2070 | 13 |
| coaster set | Hexagon Coaster Set | 376 | 1396 | 30 |
| coaster set | Optical Illusion Coaster Set | 231 | 707 | 7 |
| mandala coaster | Mandala Coaster | 154 | 800 | 8 |
| mandala coaster | Lotus Mandala Coaster | 57 | 269 | 2 |
| moroccan coaster | Zellij Moroccan Tile Coaster - MMU & Multipart | 89 | 210 | 1 |
| star coaster, islamic coaster | 12-Pointed Islamic Star Coaster | 50 | 302 | 1 |
| geometric coaster | Simple Geometric Coaster | 39 | 133 | 0 |
| geometric coaster | Geometric Coaster (id 229313) | 36 | 181 | 3 |
| girih | Arabesque (Girih) Coasters | 1 | 22 | 0 |
| islamic pattern | Andalusian wall decor - Islamic pattern design | 25 | 133 | 1 |

Eight searches were run: geometric coaster, islamic pattern, moroccan coaster, mandala
coaster, coaster set, girih, arabesque coaster, star coaster (15 results each at most). What
they show, within those eight:

- The most-liked coaster sets are themes and brands (car parts, Formula 1, a plant, Pac-Man),
  not pattern art.
- Among pattern coasters, the round, centred ones (mandala, lotus mandala) sit above the
  square or tile ones, and the one Islamic star coaster found has 50 likes. That is a weak
  lean toward "one clear centre in a round coaster", from a handful of models.
- Islamic-pattern coasters are a small niche on Printables: tens of likes, not hundreds.

Transfer: Printables is a free-download site for people who print things. A like or download
there says what makers want to print, not what a buyer pays for, and relevance order is not a
popularity ranking. It transfers only as a weak hint about which looks catch the eye.

**MakerWorld, Printables model pages, Etsy search pages.** WebFetch got HTTP 403 on each one I
tried (Printables model 1038262, MakerWorld model 402076, etsy.com/market/geometric_coasters).
**Snippet only** from search summaries:

- MakerWorld: a "Round Honeycomb Coaster" at 17.4k downloads and a "Monstera Leaf Coaster Set
  with Holder" at 10.2k downloads; a "Geometric Coaster Set" of six with 11 boosts.
- Etsy: bestsellers named in the summary were personalized name coasters, drink-brand
  coasters, monstera sets, Pokéball and game-rune coasters. What reviewers praise, per the
  summary: detail and smooth surfaces, that it works (glasses do not stick), colors that match
  the photos, packaging.
- From my earlier search in this session (also snippet): a monstera set with 989 reviews and a
  fidget coaster set with 877 reviews on Etsy; STL downloads at $1–5 and finished coasters at
  $10–40 and up.

Nothing here was fetched, so none of it sets a number in the design. The one pattern that
repeats across the Printables table and both snippet summaries: sets sell and get liked,
round-and-centred reads well, and a theme or a story (a car part, a plant, a named place)
carries a lot.

## 3. Inside the repo

### 3.1 What Omar has already said about good and bad coasters

From [look-before-you-print](../../.claude/memory/look-before-you-print.md) and the
[review-print rubric](../../.claude/skills/review-print/rubric.md), Omar's verdicts on the
minis-03 candidates:

- Near-solid discs: sDO9 and nmEj, "mostly solid disks are not good coasters".
- Half-empty art: n3Ii, "felt incomplete".
- Bare wedges between the art and the frame: lEfW and tA8e, "lots of weird empty space".
- Upsizing did not fix density: sDO9 at 60 mm and nmEj at 70 mm were still near-solid.

The rubric's numbers from `tools/print_review.py` (share of the outline cut through, share
taken by the biggest hole, share of cells nearly all hole) flagged the gross cases:
`biggest` at or above 0.05 caught both big gaps, `open` at or below 0.15 caught both
near-solid pieces, and nothing caught tA8e's wedges. The rubric calls these "hints for the
eye, not a gate: nine pieces is too few to set a pass line."

The printed plates: [minis-03](../prints/2026-09-26-minis-03/index.md) (CS-1, CS-2, rDux
minimal-frame; "good start: the pattern reads", "much too small at 40 mm") and
[minis-04](../prints/2026-09-26-minis-04/index.md) (CS-1 frame and pegs, CS-2, rDux, CS-1
twist, all "adjust"; tiny holes blamed on the slice, not the design).

So Omar's recorded taste so far is about **fill**: the pattern must read, must reach its
outline and must not be a disc. None of his recorded verdicts is about fold, story or
novelty.

### 3.2 The made set

From the [constructions ledger](../constructions/ledger.md) and the prototype catalog, the nine
coasters with a vendored mesh:

| catalog | id | fold | layout | outline | lines | what happened |
|---|---|---|---|---|---|---|
| CS-1 | GimTvN9hw4U | 6 | one centre star | hexagon | straight | printed, adjust |
| CS-2 | 7apC5Q9QS-8 | 8 | one centre star | square | straight | printed, adjust |
| CS-6 | tA8eSdVx_EQ | 7 | one centre star | heptagon | straight | left off: wedges |
| CS-7 | lEfWSogWscs | 8 | one centre star | octagon | straight | left off: empty space |
| CS-8 | rDuxHF3xMOc | 8 | repeat tile | square | straight | printed, adjust |
| CS-9 | nmEjCTzMbDg | 18 | one centre flower | round | arcs | left off: near-solid |
| CS-10 | n3IidKfXE1I | 12 | one centre star | round | straight | left off: incomplete |
| CS-11 | sDO9fpu76v8 | 6 | repeat tile | hexagon | straight | left off: near-solid |
| CS-12 | bknVRSMcLj0 | 12 | repeat tile | round | straight | not yet printed |

The layout, outline and lines columns are my reading of the ledger titles, the catalog and the
coaster pictures; they are not stored anywhere in the repo today. The ledger's own `printed`
column is `—` for every row, while CS-1, CS-2 and CS-8 have print records; the print status
lives in `docs/prints/`, not the ledger.

**No made coaster is 5-fold or 10-fold.** Six of the eight rebuilds are. That makes fold the
biggest single difference on offer, and it also means the difference is used up by the first
10-fold coaster: once one is made, the other five lose most of it.

### 3.3 The eight rebuilds

From the open-calls page call 4 table, the [catalog-expansion backlog](../tasks/catalog-expansion/backlog.md)
item 2, the candidate screen and the rebuild pictures in
[`2026-09-29-open-calls-media/`](../working-model/feedback-requests/2026-09-29-open-calls-media/),
which I looked at one by one:

| id | pattern | steps, oracle score | what the picture shows |
|---|---|---|---|
| n_ICgwOr6qs | ten-petal blossom from one compass setting | 9/9, 0.886 | big arc petals round a small star; five in front, five behind; the tips leave gaps at the rim |
| Y6kS1MvnKoc | Mamluk Qur'an page, seven ten-point stars | 17/18, 0.861 | the construction grid only; the finished pattern is not visible in the picture |
| NtnlGMTElBk | Mustansiriya ten-fold interlaced star | 13/13, 0.930 | one closed band of squares round a ten-point star; compact; ten small gaps between the points and a circle |
| gBV_JTt3Kxk | Itimad-ud-Daula ten-fold rosette in a rhombus | 11/11, 0.906 | a ten-point rosette that fills a rhombus edge to edge |
| _U6G8QSfWnk | Sutton's fivefold rectangle, traced quarter | 6/6, 0.895 | a sparse fragment, a few crossing lines; reads as a quarter of something |
| fhGHzop7ULw | sixfold √3 rectangle from Baghdad | 9/9, 0.921 | a tall rectangle with two stars cut by its edges; big open shapes |
| jlTmt_279M4 | sevenfold stars in a tilted square | 17/17, 0.941 | a square tile filled evenly, four seven-point stars round an octagon; quarter turns, no mirror |
| A9fefFurD_s | Broug's ten-point star from one circle | 17/17, 0.855 | a ten-point medallion; the outer layer shows long straight lines that leave big triangles near the rim |

Licence notes from the candidate screen: A9fefFurD_s's method comes from Broug's book (his
copyright may apply), Y6kS1MvnKoc carries "(c) Eric Broug 2014", jlTmt_279M4's source is
Bourgoin 1879 on archive.org under the Public Domain Mark. It says "That is the researchers'
reading, not legal advice."

None of the eight has a naqsh file yet (the ledger's naqsh column is `—` for each), so
`print_review.py` cannot measure any of them today.

### 3.4 Precedent

- [dsl-extension-skill-evaluation](../design/process/dsl-extension-skill-evaluation.md): the
  proposed skill would have repeated two existing ones; the real gap was something a detector
  could check. "the fix is a detector, not more documentation."
- [issue-register-evaluation](../design/process/issue-register-evaluation.md): a register,
  skill and reminder hook were rejected because the guards did the work and nobody read the
  documents.
- [request-feedback-evaluation](../design/process/request-feedback-evaluation.md): a skill was
  built, with no hook, because the work was a recurring page Omar reads and answers.

The question those two measured was "is there a rule a machine can check?" For
prioritize-design, part of it is: fold, layout, outline and lines against the made set is
arithmetic, and fill is `print_review.py`. The rest (would a buyer like it, is it unusual) has
no right answer to check against, so a gate would have no case where it can be proven wrong.
That part is judgment, and judgment is what a skill is for.

## 4. Search scope (K2)

- Outside: WebSearch on coaster marketplaces (MakerWorld, Printables, Etsy, 3 searches), MAYA,
  Berlyne's inverted U, symmetry and complexity preference, the Consensual Assessment
  Technique, and fold statistics for Islamic patterns. Fetched: Hekkert 2003 abstract,
  Silvennoinen 2025, Güçlütürk 2016, Mather 2023, the Printables API. Blocked (403, login or
  captcha): Printables and MakerWorld model pages, Etsy search pages, PMC, nature.com,
  ResearchGate, bertamini.org, PubMed. Not searched: Thingiverse's API (it needs a token),
  gift-buying studies, and any study on Islamic patterns as consumer products; I found none in
  the searches above, which is not the same as there being none.
- Inside: the ledger, the prototype catalog CS entries, the two print records named above, the
  review-print skill and rubric, the look-before-you-print memory, coaster styles, the
  candidate screen, the catalog-expansion backlog, the open-calls page and its comments file,
  and the three process docs above. I did not read the other researcher's files, by design.
