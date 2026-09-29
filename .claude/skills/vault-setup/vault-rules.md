# Vault rules — what a good docs/ vault looks like here

The rubric the [`vault-setup`](SKILL.md) skill reads at run time. Each rule says what
`tools/vault_audit.py` shows for it, so a check is a number, not an impression. Change a rule
here and the skill follows; the skill never needs to change with it.

The vault is all of `docs/`: design docs at the top level, and `research/`, `issues/`, `wiki/`,
`catalog/`, `constructions/`, `tasks/` and `prints/` below it. Decided in
[D-082](../../../docs/working-model/decisions-log.md#d-082--the-docs-vault-uses-obsidians-core-bases-for-live-views-dataview-and-other-community-query-plugins-stay-out).

## 1. Properties: a few, the same everywhere

| Where | Properties | Filled by |
|---|---|---|
| Top-level design docs | `status`, and `decisions` when the decisions log names the doc | by hand when the doc's state changes |
| Hubs (plan, backlog, decisions-log, faq, prints, site-graph, the runbooks and maps) | none | — |
| `working-model/feedback-requests/` | `date` | the `request-feedback` skill; answers are tick boxes in the body |
| `research/` | `date`, `produced-by`, `feeds` | the `ground-design-doc` skill when research is checked in |
| `issues/` | `date` | whoever writes the pivot up |
| `wiki/troubleshooting/` | `title`, `symptom`, `kind`, `proof`, `first_seen` | the `print-wiki` skill's template |
| `prints/<run>/index.md` | `run`, `plate`, `status`, `outcome` and the rest | the prints gate requires them |
| `catalog/patterns/` | the catalog's own set | its generator |

- **`status` is one of** `idea`, `draft`, `decided`, `built`, `superseded`. A doc is `built`
  when what it designs has shipped, `decided` when the choice is made and the build is not
  finished, `superseded` when another doc replaced it (say which in the doc).
- **`decisions`** is a list of `D-0xx` ids, the ones whose decisions-log section links the doc.
- **`feeds`** is a list of wikilinks, single-quoted: `- '[[coaster-design]]'`. A qualifier goes in
  the alias: `- '[[decisions-log|decisions-log D-066]]'`. Obsidian's backlinks pane then shows a
  doc's research without anyone writing a list. Research that feeds no doc yet says so with
  `feeds: []`; the research view's "Feeds nothing" table lists it.
- **Quote a value** that starts with a quote or holds `: `. Otherwise the frontmatter is not
  valid YAML and Obsidian drops every property of the note, silently. The docs gate refuses it
  (D8).

The audit shows: `properties` per folder, and `invalid frontmatter`, which must be 0.

## 2. Views: core Bases, one file per area

- Views live in `docs/bases/<area>.base` and are embedded on the home page,
  [`docs/README.md`](../../../docs/README.md).
- **Bases before Dataview.** Filter, group, sort and a backlink count are all Bases needs to do
  here. Reach for a community query plugin only for a view Bases cannot express, and name that
  view in a new decision.
- A new area earns a base when it has properties worth sorting on, not before.
- **Write `.base` files the way Obsidian saves them; comments are dropped on save.** Obsidian
  rewrites a view file whenever someone changes the view in the app. Seen 2026-09-28 on
  `design-docs.base`: it dropped every `#` comment line and wrote `note.status` as plain `status`
  in `groupBy` and `order`, while keeping `note.` in filters, in `sort` and in the `properties`
  keys. So a `.base` file has no comments (what each view is for lives in the table below), and
  names a note property bare in `groupBy` and `order`. The docs gate holds this (D10).

| Base | Shows | Notes |
|---|---|---|
| `design-docs.base` | Design docs by where they stand | A doc joins by carrying a `status` (idea, draft, decided, built, superseded). Hubs such as plan.md carry none. |
| `research.base` | Research notes, newest first, with the docs each feeds | `feeds` holds wikilinks, so a doc's backlinks pane lists the research behind it. "Feeds nothing" lists notes with no `feeds` or `feeds: []`. |
| `issues.base` | Pivots and dead ends in `issues/`, newest first | |
| `prints.base` | Print records, `prints/<run>/index.md`, newest first | Its properties are the ones the prints gate requires, so a record listed here passed it. |
| `troubleshooting.base` | Print troubleshooting notes, grouped by kind | Its properties are the `print-wiki` skill's template. |

The audit shows: `bases`, each with the notes that embed it. A base embedded nowhere is dead.

## 3. Links: markdown in the body, wikilinks in properties

- **Note bodies use markdown links** (`[text](path.md)`). GitHub renders them, the docs gate
  checks each one resolves (D1), and Obsidian follows them and counts them as backlinks just the
  same.
- **Wikilinks go in properties** (`feeds:`), because a property is where Obsidian needs one to
  draw the link and a markdown link there is only text. A wikilink in a body is not wrong, but
  GitHub shows it as raw `[[...]]`.
- Every wikilink must name a file in the vault (D1). Research bodies are exempt, like every other
  D1 rule, because they are kept verbatim.
- **One exception to verbatim: a link target in a research body moves with the note it points
  at.** A target is an address, not researched content, so `tools/move_doc.py` rewrites it (and a
  label that is the target itself, written out as a path). A path named in research
  prose — in a sentence or a provenance header — stays as written, and the mover lists it.
- A bare `[[name]]` finds a note wherever it sits, so a move leaves it alone; the mover flags a
  move that makes a name stop being unique.

The audit shows: `links` — markdown count, wikilink count, broken wikilinks (must be 0).

## 4. No orphans

Every note is linked from somewhere: a hub, a doc that uses it, or the home page. An orphan is
invisible in Obsidian unless you already know its name.

The audit shows: `orphans`. Fix by linking from the note's natural hub; the home page's
"Also here" list is the fallback, not the first choice.

## 5. Names people can read

Obsidian shows the file name in the graph, tabs, search and link suggestions, not the title
property. A file named by an id (a YouTube id, a hash, a bare number) reads as noise there.
Keep the id as a property and name the file after its title.

The audit shows: `opaque file names`, which should be 0.

## 6. Graph colors by kind of page

The graph view colors pages by folder (research gray, issues red, wiki green, catalog amber,
constructions purple, tasks light blue, prints orange, design docs blue — `design/` or a
`-design` name, so a doc is blue before and after it moves). The groups live in
`tools/vault_audit.py` and are merged into the vault's local graph settings (graph.json, not committed) by `--setup-graph`.

The audit shows: `graph color groups`, at least as many as the tool defines.

## 7. What `.obsidian/` commits

Only what makes the vault the same from any checkout: `.gitignore`, `app.json`,
`community-plugins.json`, and the BRAT and review-md settings. Window layout, `graph.json`,
`core-plugins.json` and plugin code stay local. Any tool that writes a file in `.obsidian/`
reads it first and merges, because Obsidian may be running and rewrites these files itself.

## 8. No community plugin code from us

The community plugins on are BRAT and review-md, for review threads. Adding one is a decision
(log it), and this skill never installs plugin code. Core plugins are fine to turn on.

The audit shows: `plugins` — community list, and the core plugins this rubric uses.

## 9. Folders of same-shaped notes have a checked outline

Where a folder's notes share a shape, the docs gate checks the shape (D9), so a note that drifts
is caught when it is committed rather than when someone reads it. The rules are one table,
`FOLDER_RULES` in `.claude/gates/docs_gate.py`; this is the same table in words.

| Notes | Must carry | Headings, in this order | Reads only |
|---|---|---|---|
| `wiki/troubleshooting/*.md` | the fields in the `print-wiki` template | the template's `##` headings | all |
| `research/*-grounding-audit.md` | — | the `ground-design-doc` skill's audit layout, less "Citation spot-check results" (one verbatim audit has none) | all but `hemisphere-split-grounding-audit.md`, written before that layout |
| `research/*.md` | `date`, `feeds` | — | all |
| `issues/*.md` | `date` | — | all |
| any note outside `prints/` and `catalog/` | a `status`, if it has one, of idea, draft, decided, built, superseded | — | notes with a `status` |
| `design/coaster/coaster-*-design.md` | — | The ask, Options and the rubric, Grammar, Decisions, Not yet | status decided or built |

- The troubleshooting and audit outlines are **read from their templates when the gate runs**, not
  copied into the gate. Change the template and the check follows.
- Headings match by their words: numbering, `§`, case, punctuation and anything after `—` or `:`
  are ignored, so `## 4. Grammar — the keyword` is `Grammar`. Other headings may sit between the
  required ones.
- A new family earns a row when its notes already share the shape. Measure first:
  `python3 .claude/gates/docs_gate.py --outline-summary` prints, per row, how many notes it reads
  and how many pass. If some fail, fix those notes in the same change rather than exempting them;
  an exemption names one note and says why.

**Validator:** `python3 .claude/gates/docs_gate.py` (in `make validate-docs` and the pre-commit
hook) reports each note that breaks its folder's row, and `--self-test` runs every row against a
passing note and its hard failures.

- PASS: `docs/wiki/troubleshooting/floating-regions-warning.md` as it stands: all five template fields,
  and the five headings in the template's order.
- FAIL: the same note with "Is it a concern?" moved below "What to do": every heading is still
  there, only the order is wrong, and the gate names the heading that is out of place.
- FAIL: the same note with "Proof — our own prints" renamed "Evidence", or with `first_seen`
  removed from its properties.
