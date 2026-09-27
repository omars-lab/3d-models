---
date: 2026-09-27
produced-by: researcher B (Claude Opus 5.5), one of two independent candidate screeners; web research (web search, page fetch, YouTube oEmbed and yt-dlp metadata-only reads, thumbnails viewed locally and not kept)
feeds: docs/tasks/catalog-expansion/backlog.md item 2 ("The queue is empty")
---

# Construction candidates from other creators: screen B

Every construction in the [ledger](../constructions/ledger.md) comes from one creator,
Sarah Brewer, and is mostly a 6-, 8- or 12-fold rosette (plus one 7-fold rosette, one
n-fold flower, and a few tilings and walls). This file screens new candidates from **other creators**,
aiming for new fold counts (5, 7, 9, 10, 16) and new tilings, and gives each one a
GO or NO-GO dated 2026-09-27.

Where I started: the youtube repo's discovery wiki (index, relevance.toml, the one creator
page, the concept pages). It knows only Sarah Brewer, and its girih-tiles and
Topkapi-scroll concept pages have no videos yet. Its design doc names Eric Broug as a
"candidate" creator; nothing from him is in the corpus. None of the video ids below
appears anywhere in the youtube repo (grep, 2026-09-27).

## How I checked, and what I did not check

- **Channel, date, length, description:** read from YouTube's oEmbed endpoint and from
  `yt-dlp --skip-download` metadata. No video was downloaded.
- **Licence:** yt-dlp fills its `license` field only when the watch page shows a Creative
  Commons marker. It was empty for **every** video below, and a grep of one saved watch page
  (`0ke_GpoBa-s`) found no "Creative Commons" string. So I read every video as the
  **standard YouTube licence (all rights reserved)**. I did not confirm this on each
  rendered page by eye.
- **Coaster fit:** judged from the thumbnail (and, for GeoGebra files, the page text). I
  did **not** watch any video end to end. A thumbnail shows the finished art at best, so
  every coaster-fit call below is a first read, to be confirmed at reconstruction.
- **Search space (K2):** YouTube search on six queries (9-fold, 16-fold, 7-fold, 10-fold,
  GeoGebra + Islamic pattern, Broug), the full video lists of three channels (Eric Broug,
  Samira Mian, Eman Zainab), and one GeoGebra book. When I say "not found", I mean not found
  in that space. My 9-fold YouTube search returned one result, which does not show that
  no good 9-fold video exists.

## Licence rule for everything below

Reconstructing geometry from a video is not copying the video. We rebuild the construction
from scratch in GeoGebra and naqsh, and we never download or republish the video or its
frames. The historical patterns themselves (Mamluk, Mughal, Timurid, Bourgoin 1879) are
centuries old. What we must record for each row: the video's licence (standard, below),
the creator's credit, and the historical source when one is named. **Two routes carry a
reusable licence:**

- **Bourgoin, *Les éléments de l'art arabe* (1879):** on archive.org under the Public Domain
  Mark 1.0 (fetched). Any candidate traced to a Bourgoin plate can be checked against the
  plate itself.
- **GeoGebra materials:** GeoGebra's Terms of Service (fetched) say "We grant you permission
  to use the Website Content under the terms of the Creative Commons
  Attribution-Non-Commercial-ShareAlike license (version 4.0 or later)". **Hedge:** the text
  I read does not say in so many words that "Website Content" covers files other users
  uploaded. The same terms give GeoGebra itself a broad licence to uploaded material. Read
  it as CC BY-NC-SA 4.0 *probably*, and record the author and the material id either way.
  NC matters if coasters are ever sold.

## Candidates

Fold counts marked "(thumb)" come from counting the thumbnail, not from the video.

| # | Video / file | Creator | Fold / kind | Verdict (2026-09-27) | One line of reasons |
|---|---|---|---|---|---|
| 1 | [`0ke_GpoBa-s`](https://www.youtube.com/watch?v=0ke_GpoBa-s) "#13 Tenfold Rosette 3 Ways" (2020, 43:00) | Samira Mian | **10-fold rosette** | **GO** | Chaptered step by step (divide the circle into 5 and 10, the fivefold rectangle, then the rosette), first 10-fold in the set, and the thumbnail's line rosette is an open star ring that fits a 90 mm disc. |
| 2 | [`_U6G8QSfWnk`](https://www.youtube.com/watch?v=_U6G8QSfWnk) "Umm Al Girih Tutorial 1 — A Five/Tenfold Pattern Two Ways" (2020, 29:30; parts 2–4: `uNi8Tq6gtA8`, `ZpsDMdPZ0c0`, `XhezGJdyW9o`) | Samira Mian | **5/10-fold girih tiling** | **GO** | Opens with the five girih shapes, then the fivefold rectangle and proportioning circles: the first girih tiling here, and it fills the wiki's empty girih-tiles concept. Coaster fit is likely but unconfirmed: it is a tiling, so crop it the way `bknVRSMcLj0` was cropped. Needs part 1 only, or 1–4. |
| 3 | [`Y6kS1MvnKoc`](https://www.youtube.com/watch?v=Y6kS1MvnKoc) "How to Draw a Mamluk Quran Page" (2014, 12:38) | Eric Broug | **10-fold star field** (Mamluk Qur'an, Cairo c. 1306–15, Chester Beatty 1479, per the thumbnail) | **GO** | Compass-and-ruler, "no maths, no calculations, just drawing". The creator the wiki already names as next. A historical source on a named manuscript. With the floral fill left off, the line pattern is a 10-point star ringed by kites and pentagons: an open lattice when cropped to a disc around the centre star. The thumbnail reads "(c) Eric Broug 2014". |
| 4 | [`88q-u2eWZqg`](https://www.youtube.com/watch?v=88q-u2eWZqg) "4 Fold Rosette with 16 Petals" (2022, 5:45) | Eman Zainab (@artwitheman) | **16-fold rosette** | **GO** | The only 16-fold video found. 16 is 8 bisected, so it is exact with compass and straightedge. The thumbnail shows a thin-line petal ring, open. **Risk:** 16 lines meet at a small central star, which may crowd at 90 mm, so check the centre before printing. 5:45 is short; the title says "step by step". |
| 5 | [`jlTmt_279M4`](https://www.youtube.com/watch?v=jlTmt_279M4) "islamic geometry: how to draw 7, 4 fold pattern" (2021, 2:47) | unravelling pattern | **7-point stars in a 4-fold square repeat** (Bourgoin plate 170) | **GO** | New pairing: a 7-point star in a square repeat (our 7-fold is a lone rosette), and the thumbnail is a clean open line lattice in a square. The plate is public domain (Bourgoin 1879 on archive.org). **Hedges:** the video is 2:47 with music and "instructions … in one tile", so it may be too fast to read every step, with the plate as the fallback reference. A regular heptagon cannot be built exactly with compass and straightedge, so the video's 7-division is either approximate or given as an angle; which one is unverified. |
| 6 | [`yZN_wn0uvTY`](https://www.youtube.com/watch?v=yZN_wn0uvTY) "Islamic Geometry Using Geogebra: Tenfold Mughal India" (2021, 11:27) | Geogebra_Road to School (Amanda La Hadi with IAIN Kendari students) | **10-fold rosette** (Itimad-ud-Daula) | **GO** | Built **in GeoGebra Classic 5** with the Algebra panel on screen, the same legibility that made Sarah Brewer's videos rebuildable. The description credits Samira Mian's hand version (`gBV_JTt3Kxk`), so the two can cross-check each other. The thumbnail's interlaced 10-fold rosette is open. **Hedge:** the narration is Indonesian, so read the commands, not the voice. |
| 7 | [`hzyhmg9p`](https://www.geogebra.org/m/hzyhmg9p) "12- and 9-pointed stars" (GeoGebra book "Islamic Geometric Patterns", ch. 7) | Chris Cambré (after Lynn Bodner on the Tashkent scrolls) | **9 + 12 combined stars** | **GO (conditional)** | The only 9-fold candidate with a traceable historical source, and a public GeoGebra file whose construction can be read directly. **Conditions:** the page says the result has "minor distortions" (acceptable in historical practice), so the rebuild must keep the construction as drawn, not an idealised one. Coaster fit is not seen: I read the page text, not the render. It is not a video. |
| 8 | [`cjAFU4ck`](https://www.geogebra.org/m/cjAFU4ck) "Broug 'Fivefold Pattern 1' Construction" | Stewart C. Russell | **5-fold pattern** | **GO (conditional)** | True 5-fold, in a public GeoGebra file. **Conditions:** the page does not say whether it is step by step, and the pattern is from Broug's copyrighted book (Thames & Hudson 2013, pp. 204–205), so record both credits. Coaster fit not seen. |
| 9 | [`LoCRh3SOhls`](https://www.youtube.com/watch?v=LoCRh3SOhls) "Tenfold Rosette in a Pentagon" (2020, 20:20) | Samira Mian | 10-fold rosette | **NO-GO** | Duplicates #1 (same creator, same rosette in a pentagon frame). Keep it as #1's alternate frame, not as a separate construction. |
| 10 | [`FuusIqjDUys`](https://www.youtube.com/watch?v=FuusIqjDUys) "Tenfold Ottoman Pattern 3 Ways" | Samira Mian | 10-fold field | **NO-GO** | Its thumbnail shows a fine field of many small cells, likely near-solid at 90 mm. It also adds nothing #1–#3 do not. |
| 11 | [`n_ICgwOr6qs`](https://www.youtube.com/watch?v=n_ICgwOr6qs) "Sheikh Zayed Grand Mosque Fivefold Motif" (2020, 29:39) | Samira Mian | 5-fold motif, curved | **NO-GO** | Its chapter list includes "Outlining freehand curves", so part of the final art is not constructed. Revisit if we want a 5-fold with arcs after #8. |
| 12 | [`vpB4VAqOduo`](https://www.youtube.com/watch?v=vpB4VAqOduo) "How to draw an Islamic geometric pattern: Ayyubid Star" (2014, 4:38) | Eric Broug | star, fold **unconfirmed** | **NO-GO (for now)** | I could not count the fold from the thumbnail: roughly 9–10 points, drawn over a pre-laid line grid with "a ruler and pencils". Confirm the fold and the grid's origin first; if it is 9, it jumps the queue. |
| 13 | [`QZqGQGu7QOg`](https://www.youtube.com/watch?v=QZqGQGu7QOg) "Mamluk Star 2" (2014, 0:50, silent) | Eric Broug | 10-fold, ten interlinked kites | **NO-GO** | 50 seconds, silent: too thin to rebuild each step. #3 covers Broug and 10-fold better. |
| 14 | [`6X4UgrXzfkQ`](https://www.youtube.com/watch?v=6X4UgrXzfkQ) "How to Construct a Heptagonal/Octagonal Islamic Geometric Pattern" (2017, 13:51) | arithilemn | 7/8 tiling | **NO-GO (backup)** | A plausible 7-with-8 tiling, but #5 teaches the 7-in-a-square lesson with a public-domain plate behind it. A hand-drawn heptagon is approximate at best. Backup if #5 proves unreadable. |
| 15 | [`Dyfw1GGJ82M`](https://www.youtube.com/watch?v=Dyfw1GGJ82M) "Ustadh Soufiane Abbadi Explores the 10 Rosette with GeoGebra" (2019, 2:42) | Deen Arts Foundation | 10-fold (GeoGebra) | **NO-GO** | 2:42, and the thumbnail shows only the 10-division scaffold: likely an excerpt, not a whole construction (unwatched, so a hedge). |
| 16 | [`SsV1q9GPGjE`](https://www.youtube.com/watch?v=SsV1q9GPGjE) "How to Draw 9-Fold Symmetry" (2020, 4:03) | Pepper and Pine | 9-fold overlapping circles | **NO-GO** | A Waldorf "sacred geometry" circle rosette, not an Islamic line pattern. The author says she "adjusted and readjusted my compass" until the divisions came out even (trial and error). The circle overlaps read near-solid. |
| 17 | [`syYjWk5pbWg`](https://www.youtube.com/watch?v=syYjWk5pbWg) "Tutorial for Creating 12 pointed star design in GeoGebra" (2021, 6:03) | beckykwarren | 12-fold star | **NO-GO** | Clear GeoGebra steps, but 12-fold is already in the set, and its filled-polygon star is a solid badge, not a lattice. |
| 18 | [`gfRLxv-Oap0`](https://www.youtube.com/watch?v=gfRLxv-Oap0) "How to Draw 10 Fold Rosette" (2021, 1:59) | Nik Zarina | 10-fold rosette | **NO-GO** | 1:59 with music, and the same rosette family as #1, which is chaptered and 43 minutes long. |

Tally: 18 screened from 12 creators, none of them Sarah Brewer. 6 GO, 2 GO (conditional),
10 NO-GO. The GOs cover 5 creators (Samira Mian, Eric Broug, Eman Zainab, unravelling
pattern, Geogebra_Road to School), plus two GeoGebra authors (Chris Cambré, Stewart
Russell) in the conditional GOs. New folds and kinds across the GOs: 10, 16, 5/10 girih,
7-in-4, 9+12, 5.

## Recommendation: reconstruct in this order

1. **`0ke_GpoBa-s`, Samira Mian's tenfold rosette.** Highest return for the least risk.
   It is the first 10-fold, it is a single rosette (the shape our pipeline handles best:
   one wedge, then rotate), it is the most carefully chaptered video in the screen, and
   its 5/10 circle division and fivefold rectangle are exactly the scaffold that #2 and
   #3 reuse. Build it first and the next two start from a proven 10-fold scaffold.
2. **`Y6kS1MvnKoc`, Eric Broug's Mamluk Qur'an page.** It brings in the second creator the
   wiki already flags as next, a named historical source, and a 10-fold star **field**
   (star plus surrounding kites and pentagons) instead of a lone rosette. It reuses #1's
   scaffold. Crop it to a disc around the centre star.
3. **`88q-u2eWZqg`, Eman Zainab's 16-fold rosette.** A new fold that is still exact with
   compass and straightedge (bisected 8), from a third creator. Check the crowding at the
   centre before printing.

Next in line: `_U6G8QSfWnk` (girih, which fills an empty wiki concept but is a tiling and
needs cropping), `jlTmt_279M4` (7-in-4, with the Bourgoin plate as a public-domain
cross-check), and `yZN_wn0uvTY` (GeoGebra on screen: the easiest to read, but a third
10-fold, so it ranks below the new folds). The two GeoGebra files (#7 9+12, #8 5-fold)
need their renders looked at before they are real GOs.

## Sources

"Fetched" means I read the page's content (for YouTube, through oEmbed or yt-dlp metadata
plus the thumbnail). "Snippet" means I saw only a search-engine result line.

| Source | What it gave | Fetched or snippet |
|---|---|---|
| youtube repo discovery wiki (index.md, relevance.toml, creators/sarah-brewer.md, concepts/girih-tiles.md, topkapi-scroll.md, rosette-7fold-line.md) | Starting corpus; only one creator; girih has no videos | Fetched (read on disk) |
| [ledger](../constructions/ledger.md), [backlog](../tasks/catalog-expansion/backlog.md) | The 10 existing constructions and item 2 | Fetched (read on disk) |
| YouTube oEmbed for `0ke_GpoBa-s`, `LoCRh3SOhls`, `88q-u2eWZqg`, `OK3TRZl_wKI`, `YcqakkAKvFI` | Title and channel | Fetched |
| yt-dlp metadata (no download) for rows 1–6 and 9–18 | Channel, upload date, length, licence field (empty), description | Fetched |
| yt-dlp channel lists: @EricBroug, @samiramian, @artwitheman | Every title on each channel | Fetched |
| yt-dlp YouTube search: 9-fold, 16-fold, 7-fold, GeoGebra Islamic | Found rows 5, 6, 12–18 | Fetched (result lists) |
| Thumbnails for rows 1–6 and 9–18 (i.ytimg.com, viewed locally, not kept) | Coaster-fit first read; fold count; "(c) Eric Broug 2014" on row 3 | Fetched |
| [samiramian.uk/youtube](https://www.samiramian.uk/youtube) | Tutorials grouped by fold family; no licence statement | Fetched |
| [samiramian.uk/fivefold](https://www.samiramian.uk/fivefold) | The #fivefoldfun series (rows 1, 2, 9, 11, Umm al Girih 1–4); no licence statement | Fetched |
| [geogebra.org/m/cjAFU4ck](https://www.geogebra.org/m/cjAFU4ck) | Row 8: author, Broug book source, pages | Fetched |
| [geogebra.org/m/kxp4qekc](https://www.geogebra.org/m/kxp4qekc) | Chris Cambré's book, chapter and material list | Fetched |
| [geogebra.org/m/hzyhmg9p](https://www.geogebra.org/m/hzyhmg9p) | Row 7: Bodner and Tashkent source, "minor distortions" | Fetched |
| [geogebra.org/m/cuhkk3up](https://www.geogebra.org/m/cuhkk3up) | A 5-fold dual pattern, finished applet, not step by step (not screened as a row) | Fetched |
| [geogebra.org/m/aZjxtshJ](https://www.geogebra.org/m/aZjxtshJ) | Arthur Lee's "polygon patterns from rotation" slider tool (a generator, not a construction; not screened) | Fetched |
| [geogebra.org/tos](https://www.geogebra.org/tos) | The CC BY-NC-SA 4.0 "Website Content" sentence | Fetched |
| [geogebra.org/license](https://www.geogebra.org/license) | Does not state a licence for user materials | Fetched |
| [archive.org Bourgoin](https://archive.org/details/LesElementsDeLArtArabeBourgoin) | Public Domain Mark 1.0, 1879, Firmin-Didot | Fetched |
| [artvee Bourgoin pl. 170](https://artvee.com/dl/les-elements-de-lart-arabe-pl-170/) | That plate 170 is hosted as public domain | **Snippet** (fetch returned 403) |
| [unravellingpattern.com](https://www.unravellingpattern.com) | Row 5's creator site; no licence text; no Bourgoin mention on the home page | Fetched |
| Web search "Eric Broug YouTube tutorial" | That his channel has a tenfold Cairo Qur'an page and a sixfold star | Snippet |
| Web search "Eric Broug Ayyubid star" | A twelvefold Ayyubid panel is mentioned; does **not** settle row 12's fold | Snippet |
| Web search "GeoGebra materials license" | GeoGebra ToS CC BY-NC-SA 4.0 (then fetched, above) | Snippet, then fetched |
| [mathemartiste 10-fold PDF](http://mathemartiste.com/geometricdesign/10foldRosetteTutorial_SarahBrewer.pdf) | Sarah Brewer has a 10-fold tutorial PDF; out of scope (same creator) but a possible cross-check for #1 | Snippet |
