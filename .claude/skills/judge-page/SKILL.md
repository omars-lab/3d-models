---
name: judge-page
description: Get a printed plate ready for Omar to judge on the hub's judging page (http://127.0.0.1:4717/judge.html) — check its After-the-print questions read cleanly, cut one picture per piece from the slice, ship them with the page, look at the page in a browser at desktop and phone width, then send him the link. Use when a print finishes (monitor-print says finished), when Omar asks to "make a judge page", "get <plate> ready to judge", "put <plate> on the hub", or asks why a plate is missing from the judging page or shows no pictures. Not for writing the print record after he answers — that is review-print.
---

# judge-page — a printed plate, ready to judge on the hub

Omar judges prints on the hub's judging page, one question at a time, with each piece shown as
its own picture under the id cut into it. He asked for it on 2026-10-22: "a feedback page ...
where I can see each peiece individually, and what peices im supposed to compare, what I am to
compare". Then: "we should have dedicated skill for making a judge page". The page reads the
plate page's `## After the print` table, so a plate is only as easy to judge as that table and
its pictures. This skill gets both right before he hears the plate is ready.

The hub is a separate repo (`omars-lab/3d-model-hub`), always running on 127.0.0.1:4717. It
reads its own copy of 3d-models at `origin/master` (refreshed every 10 minutes), so **a fix
reaches the page only once it is merged**. Answers he saves land in the plate page's
`## Judged` table, through a PR the hub opens.

## Steps

1. **Find the plate.** `python3 .claude/skills/review-print/scripts/after_print.py waiting`
   lists the plates Omar has in hand: page at `stage: sent`, its print log says finished, an
   `## After the print` table it can read, and no print record yet. If the plate is not there,
   say which of those four it fails. A plate that already has a record is judged, not waiting.
2. **Make every row readable.** `python3 .claude/skills/review-print/scripts/after_print.py measure`
   flags any cell the page cannot read. Then read the plate's rows yourself against
   [`asking.md`](../review-print/asking.md): the pieces by the id cut into them, one action per
   step, what each result looks like, at most four answers, each saying what it changes. Ids
   avoid look-alike letters (B/D, M/N, O). A rewritten row keeps the question it asked; never
   change what a row asks after the print, only how clearly it says it.
3. **Make the pictures.** `python3 .claude/skills/review-print/scripts/after_print.py pieces <plate>`
   cuts one picture per piece from the slice's bed drawing into `<plate>-media/pieces/`. It
   refuses when the slice's pieces do not match the recipe's: slice again
   (`bambu slice compose`), never hand-place a picture. Open every tile and check its id and
   shape match the piece the row names. A row that compares against an earlier print needs
   that print's photo on the page, checked as review-print step 4 says (no location data,
   sha256 listed).
4. **Ship it.** Branch off `origin/master`, stage the page and its `-media/pieces/` by name,
   `make validate`, PR, merge.
5. **Look at it as he will.** Wait for the hub to pick up master (up to 10 minutes; its main page
   shows the commit it read), then:
   - `curl -s http://127.0.0.1:4717/api/judge/<plate>` returns every row, each with its pieces
     and answers;
   - open `http://127.0.0.1:4717/judge.html#<plate>/1` in a browser at desktop and phone width
     (390 px), step through every row, and check each tile loads and each answer button names
     what it changes. The address `#<plate>/<row>` opens that row directly.

   Something wrong: fix it in 3d-models (the page) or in the hub (the page's code), and look
   again. Never tell him a plate is ready from the curl alone.
6. **Tell him** in two lines: the link `http://127.0.0.1:4717/judge.html#<plate>/1` and how many
   questions there are. When page comments are on in the hub, the same page at
   `http://127.0.0.1:8766/judge.html` takes comments (press C), and those are answered with
   `development-manager:answer-page-comments`.

## After he answers

Each saved answer opens or adds to an `After-print answers: <plate>` PR in 3d-models. Merge it
like any PR. Then review-print writes the print record from the `## Judged` table ("When a print
comes back"). Never edit the `## Judged` table by hand: it is his record.

## Scripts — when to use each

This skill has no scripts of its own. Every step uses review-print's `after_print.py`, so the
judging page and the record read the same table through the same parser.

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `review-print/scripts/after_print.py waiting` | Lists the plates sent, finished on the printer and not yet recorded, with how many rows are answered | Step 1 | `python3 .claude/skills/review-print/scripts/after_print.py waiting` |
| `review-print/scripts/after_print.py measure` | Flags any After-the-print cell the parser cannot read; exit 1 when one is found | Step 2 | `python3 .claude/skills/review-print/scripts/after_print.py measure` |
| `review-print/scripts/after_print.py questions` | The rows exactly as the hub sees them | Step 2, to read a row as the page will | `python3 .claude/skills/review-print/scripts/after_print.py questions <plate> --json` |
| `review-print/scripts/after_print.py pieces` | Cuts one picture per piece from the slice's bed drawing | Step 3 | `python3 .claude/skills/review-print/scripts/after_print.py pieces <plate>` |
