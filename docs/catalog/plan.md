# Pattern catalog vault — the plan

Proposed 2026-09-27. Nothing below is built yet. Once step 1 is in, review this note in Obsidian
with review-md: it is the first note in the vault.

## What this is for

Omar asked for four things (2026-09-27):

1. **An Obsidian vault in `docs/`** that catalogues every design, pattern and picture we have.
2. **Skills that keep it up to date** as patterns are added, built and printed.
3. **review-md installed through BRAT**, so each pattern can be reviewed and commented on in
   place.
4. **A deep link for every pattern and picture**, including the patterns we only plan to make,
   plus a catalog page of those links that stays current.

The goal is a notebook to review designs in and choose what to print next. It is not a
database. Each pattern gets one note, with its pictures and a short page of what we know about
it.

## What exists today

| What | Where | Why it isn't the catalog |
|---|---|---|
| Print-troubleshooting wiki | [`docs/wiki/`](../wiki/index.md), kept by the `print-wiki` skill | Covers slicer warnings and print faults only. No patterns, no pictures. |
| The constructions ledger | [`docs/constructions/ledger.md`](../constructions/ledger.md) | One table row per rebuilt video: oracle results, coaster file, catalog id. No pictures and no notes. |
| Pattern sources | bikar `patterns/` (constructions, stars, rosettes, orbs, lego, coupons, …) | Code, not notes. Lives in another repo. |
| Coaster pictures | bikar `packages/lab/src/coaster-thumbs/`, about 1 MB | Drawn for Coaster Lab. Nothing links a picture back to a note. |
| Print records | [`docs/prints/`](../prints) with photos | Organised by plate, not by pattern. |
| Patterns we want to make | [`research/candidate-screen-2026-09-27.md`](../research/candidate-screen-2026-09-27.md) | A queue in a research doc. No note for each pattern to point at. |
| Video rebuilds | youtube repo `reconstructions/<id>/` | youtube has no remote, so a note can't link into it. The note links the video instead. |

No `.obsidian/` folder exists in any of the six repos, so nobody has opened `docs/` as a vault
yet.

## The shape

**The vault is the whole of `docs/`.** Design docs, the wiki, prints and plates all live there
already, so one vault shows them all, and review-md can comment on any of them, not only on the
catalog.

A new folder, `docs/catalog/`, holds:

- **index.md**: the catalog page. It has a table per family (constructions and their coasters,
  stars, rosettes, orbs, lego, coupons, planned). Each row shows a small picture, the name, the
  status and a link to the note.
- **patterns/`<name>`.md**: one note per pattern, named so a person can read it, because
  Obsidian shows the file name as the note's title (Omar, 2026-09-28: "Titles shouldnt be
  youtube ids ... it should be a human legible name").
  - The file name is the `title` property in lowercase words joined by `-`, then the catalog
    id when there is one: `simple-20-step-six-fold-star-rosette-cs-1.md`.
  - The pattern's id stays in the frontmatter. A rebuilt video's id is its YouTube id
    (`GimTvN9hw4U`); a library pattern's id is its bikar file name (`Rosette-12`). The id is
    also listed under `aliases`, so searching Obsidian for the id, or linking `[[GimTvN9hw4U]]`,
    still finds the note.
  - Tools find a note by its `id` property, never by its file name.
  - bikar's `.bkr` files keep their ids as names. They are code, not notes.
  - The top of the note is **generated**: pictures, source video and creator, bikar files,
    coaster styles, oracle results, prints and their verdicts, status.
  - The bottom is **written by hand**: what makes the pattern work, what went wrong, what to
    try next.
- **styles/`<style>`.md**: one note per coaster style (minimal, frame, pegs, key, tab, twist,
  lobed, border, interlock, fill). Each shows every pattern made in that style. Style names come
  from [`coaster-styles.md`](../../.claude/skills/import-construction/coaster-styles.md).
- **media/`<id>`/**: the pictures for each note, named `<id>-<style>.png`, so any picture's file
  name says which pattern it belongs to. Pictures keep the id: nobody reads them as titles.

**Status** is one of: planned, rebuilding, built, printed, rejected. **A planned pattern gets
its note on the day it is queued.** Its link then never changes as the pattern moves from queued
to built to printed. That is what makes "deep-link a pattern we want to make" work.

The frontmatter uses plain Obsidian properties: id, aliases (the id again), title, family, status, source, creator,
catalog id (`CS-n`), bikar files, tags. Obsidian reads these without a plugin, so the vault needs
only BRAT and review-md.

## Deep links

- **A note's path is set once**, from its title, on the day the note is made. Editing the title
  later does not rename the file. A rename is a deliberate edit that moves the note's comment
  file with it and fixes every link in the same change; the docs gate fails on any link left
  dead.
- **Inside the repo**, notes link to each other with ordinary relative Markdown links. The
  docs gate already checks that those resolve.
- **From outside the repo** (a chat, a picture sent to your phone, a review sheet, Coaster Lab
  running locally), the link is an `obsidian://open` link to the note. A second link,
  `obsidian://review-md-open`, opens the note with its comments panel. A small tool prints both
  for any id or picture file, so no link is typed by hand.
- **Which vault the link opens.** Obsidian names a vault after its folder, so every `docs/`
  vault is called "docs", and review-md ships its own `docs/` dev vault. The links therefore
  name the vault by its folder path (`path=`), not by name. That path is Omar's main checkout,
  `~/Workspace/git/3d-models/docs`.
  - The catch: that checkout is shared, and the vault only shows what has been pulled into it.
    A session that merges a note change fast-forwards that checkout afterwards.
- **Write the note so its parts can be linked.** A link can land on a heading (the note's link
  plus #minimal opened the CS-1 note at that heading, checked in Obsidian 2026-09-27), but not
  on a table cell or a bare picture. So:
  - anything someone may want to link to on its own (a style, a print, a picture) gets its own
    heading, with the picture under it — not a cell in a picture grid;
  - heading text is part of the link, like a file name: name it after something that doesn't
    change (the style name from [the coaster styles](../../.claude/skills/import-construction/coaster-styles.md)),
    and treat renaming a heading like renaming a file, since every link to it breaks;
  - review-md writes a `^id` onto a passage someone comments on. Keep it when editing that
    passage; deleting it cuts the thread loose from its text.
- **The docs gate checks `obsidian://` links too.** [`obsidian-vaults.json`](../../.claude/gates/obsidian-vaults.json)
  maps each vault (by name, id or folder) to its folder in the repo, so a link written into a
  doc must open a note that exists, land on a heading or `^id` it has, and, for a review-md
  link, name a thread the note has. Both `vault=docs` and `path=` links open the note in
  Obsidian (checked 2026-09-27). A new vault goes in that file before links to it will pass.
- **Every picture a session sends of a pattern carries its note link** in the caption. The skill
  makes that a rule, and it applies to review sheets and plate pictures too.
- **The public gallery gets no `obsidian://` links**, because they only work on Omar's machine.
  Coaster Lab may get them in its local dev mode (step 6).

## Keeping it current

The repo's own precedent ([`dsl-extension-skill-evaluation.md`](../dsl-extension-skill-evaluation.md),
[`issue-register-evaluation.md`](../issue-register-evaluation.md)) is: a check does the
bookkeeping, and a skill does only the part that needs judgement. So:

- **A generator** (`tools/catalog.py sync`). It reads:
  - bikar at `origin/main`: pattern files and pictures;
  - the ledger, the print records, the plate files and the candidate queue.

  It rewrites the generated top of each note and the index, and copies pictures into `media/`.
  It never touches the hand-written part: that sits below a marker line the tool stops at.
  It can also render pictures for patterns that have none (bikar `--format views`, then
  `rsvg-convert`).
- **A check** (`sync --check`, as a pre-commit hook and in `make validate`). It fails when a
  pattern has no note, or a note's generated part is out of date. It reads bikar at a git ref,
  like the pointer gate, so the verdict doesn't depend on what is checked out.
- **A skill** (`pattern-catalog`). It covers:
  - writing the hand-written part of a note, and laying out every note so its parts can be
    linked (the rule in "Deep links" above; the generated top follows it too);
  - adding a planned pattern;
  - answering "where is the note for …" and "give me the link to …";
  - adding the note link to every pattern picture a session sends.

  Its description line has to name those phrases so the skill actually fires.
- **The loops call it.**
  - The catalog-expansion loop: when a pattern is queued (planned note) and when it is migrated
    (built).
  - The coaster-pipeline loop: when a print record lands (printed, with the verdict).
  - The video loop, in youtube: at hand-on it asks for the note in 3d-models, because it can't
    write one from there.
  - `review-print` and `print-coaster-samples` put note links next to each piece on their sheets.

## review-md

**Omar does, once, in Obsidian** (it needs the GUI and a trust click):

1. Open `~/Workspace/git/3d-models/docs` as a vault and trust it.
2. Install and enable **BRAT**.
3. Run *BRAT: Add a beta plugin* → `omars-lab/review-md`.
4. Enable **Review MD**.
5. Set the reviewer name.

**Checked in, so the vault is the same from any checkout:**
- A small `docs/.obsidian/`: `app.json`, `community-plugins.json` (BRAT and review-md) and
  BRAT's `data.json`, which lists review-md.
- The rest is gitignored: `workspace.json`, the plugin code, the cache.

**The agent side.** review-md's Claude Code plugin gives sessions the `reviews` command, so a
session can list the open threads, fix the note and reply on each. It goes in **this repo's**
`.claude/settings.json` (a project-scoped marketplace and plugin), not in the global config,
because we only touch our repos.

**Comment files.** review-md keeps each note's threads in a hidden `.<note>.comments.md` next
to the note. It is committed with the note. Two things to settle before the first comment is
committed:
- **The doc gates.** The pointer gate walks every `*.md` under `docs/`, hidden files included.
  A comment that quotes a path would then be checked as a claim. Comments are conversation,
  not claims, so the gates should skip `*.comments.md`. Prove it with a test comment first.
- **The re-anchoring hook.** review-md's post-commit hook moves threads onto the commit after
  one lands. This repo runs its hooks from `.githooks/`, so that hook needs an entry there
  rather than its own install.

## Steps, in order of value

1. **Vault and review-md working on one note.**
   - The `docs/.obsidian/` files and the gitignore.
   - The doc gates skip `*.comments.md`.
   - The post-commit entry in `.githooks/`.
   - One hand-written note, for `GimTvN9hw4U` (CS-1, on the minis-01 plate).
   - Omar installs BRAT and review-md.

   *Done when* Omar leaves a comment on the CS-1 note in Obsidian and a session answers it with
   `reviews reply`.
2. **Generator, index and every construction.** The generator, a note for each of the ten
   ledger videos (built, or "no piece by design"), the style notes and the index.

   *Done when* `sync --check` passes and every construction row in the ledger has a note with
   its pictures.
3. **Planned patterns.** A note for each of the ten queued candidates in the
   [consolidated screen](../research/candidate-screen-2026-09-27.md), with status planned: the
   video link, the creator and what to watch for. The held ids get notes marked held.

   *Done when* every id in the queue has a note, and the catalog-expansion backlog links each
   queue entry to its note.
4. **The check, the skill and the loops.**
   - The pre-commit hook.
   - The `pattern-catalog` skill.
   - The loop prompts and `manage-tasks` routing updated to call it.
   - `review-print` sheets carrying note links.

   *Done when* adding a pattern file to bikar without a note fails `make validate` here.
5. **The rest of the bikar library**: stars, rosettes, tiled, weave, orbs, lego, coupons.
   These notes are mostly generated: a picture, the file, the family. Hand-written text goes in
   only where there is something to say. Rough size: one or two pictures of about 40 kB each
   per pattern file. Whether that is worth committing is decided here, at the numbers step 2
   actually measured, not before.
6. **Optional: an "open note" link on each Coaster Lab card**, in local dev mode only.

## Assumptions to check first

These were decided without asking, so the plan could be written. Each is cheap to change now and
costly after step 2. Comment on the one you disagree with.

| Assumption | Why | The other way |
|---|---|---|
| The vault is all of `docs/` | One vault for the catalog, design docs, wiki and prints. review-md then works on design docs too. | A vault of only `docs/catalog/`: a tidier file list, but design docs can't be reviewed and cross-links leave the vault. |
| Notes are named by id, not title | Ids never change, so links never break. | Titles read better in the file list, but a title edit breaks every link and thread. Obsidian shows the frontmatter title either way. |
| Pictures are committed into the vault | Obsidian and review-md can only show what is on disk, and a picture thread needs a stable file. | Link to bikar's pictures in place: no copies, but they fall outside the vault and a sibling checkout's state decides what shows. |
| Links name the vault by path | Every docs vault is called "docs". | Name-based links are shorter, but open the wrong vault. |
| The review-md agent plugin is set per repo | Only our repos are touched. | A global install covers every repo, but that is Omar's config to change, not ours. |
| No Dataview or other query plugins | The index is generated, so it needs no plugin and reads the same on GitHub. | Dataview makes live tables, but they show as raw code everywhere outside Obsidian. |

## Not in this plan

- **No video frames copied into the vault.** The licence position is in the
  [candidate screen](../research/candidate-screen-2026-09-27.md). Notes link the video at a
  timestamp instead.
- **The vault is not published.** The public gallery stays as it is.
- **The print wiki stays as it is.** It becomes part of the vault by being in `docs/`, and
  catalog notes link its entries where a print ran into one.
