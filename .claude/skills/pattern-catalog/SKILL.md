---
name: pattern-catalog
description: Keep the pattern catalog in docs/catalog/ in step — one Obsidian note per construction in the ledger, one per coaster style, and the catalog page. Use when a construction is added to the ledger or migrated to naqsh, a coaster style or plate or print record changes, when asked to "sync the catalog", for "the catalog note" or "where is the note for" a pattern, or to "link to" a pattern's picture or style; also when `sync --check` reports a file out of date.
---

# Pattern catalog — one note per pattern, kept in step

The catalog lives in `docs/catalog/`: `patterns/` holds a note for every construction in the
[ledger](../../../docs/constructions/ledger.md), `styles/` a note for every coaster style,
`media/<id>/` the pictures, and [`index.md`](../../../docs/catalog/index.md) the page that lists
them. How it is laid out and why: [the plan](../../../docs/catalog/plan.md).

Each note has two parts. The top — properties, pictures, checks, plates and prints — is written
by the sync tool from the ledger, bikar, the plate files and the print records. Everything from
the line `<!-- written by hand below this line; the sync tool stops here -->` down is written by
hand: what makes the pattern work, what went wrong, what to try next. The tool never touches it.

## Scripts — when to use each

| Script | What it does | When to reach for it | Command |
|---|---|---|---|
| `scripts/catalog.py sync` | Writes every note's top, the style notes, the catalog page and the pictures; leaves files that are already right alone | after the ledger, a bikar construction, a plate or a print record changes | `python3 .claude/skills/pattern-catalog/scripts/catalog.py sync` |
| `scripts/catalog.py sync --check` | Writes nothing; names each file that is out of date and exits 1 | before a commit that touches the ledger, plates or prints | `python3 .claude/skills/pattern-catalog/scripts/catalog.py sync --check` |

bikar is read at a git ref (`origin/main` unless `--bikar-ref` says otherwise), never from its
working tree, so another session's checkout cannot change the result. It is found through
`--bikar-dir`, then `$BIKAR_DIR`, then `~/Workspace/git/bikar-work`; fetch it first so
`origin/main` is current.

## Rules

- **Never edit a note's top by hand.** Change the source (the ledger row, the plate file, the
  print record, the styles table in the import-construction skill) and sync. A hand edit to the
  top is overwritten on the next run.
- **Write prose under the marker.** A new note gets a `## Notes` heading there with a line
  saying nothing is written yet; replace that line.
- **Find a note by its `id` property, not its file name.** A note keeps its path once made, even
  if the ledger title changes. Style notes are found by their `style` property.
- **Comment threads survive a sync.** review-md's `^id` markers on a generated line are carried
  over when the line comes out the same. When the line changed, the sync stops and names it:
  answer or resolve the thread, then move the marker by hand to the new line (or drop it once
  the thread is resolved) and sync again.
- **Link to a picture by note and style heading**, e.g.
  `patterns/simple-20-step-six-fold-star-rosette-cs-1.md#minimal`. Never write an
  `obsidian://` link into anything the public gallery shows.
- **Status comes from the facts:** no naqsh file yet is `rebuilding`, a print record naming one
  of its files is `printed`, anything else is `built`. A ledger row marked "no piece by design"
  is `built` with the `no-piece-by-design` tag.
