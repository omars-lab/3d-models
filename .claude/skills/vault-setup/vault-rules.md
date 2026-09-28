# Vault rules — what a good docs/ vault looks like here

The rubric the [`vault-setup`](SKILL.md) skill reads at run time. Each rule says what
`tools/vault_audit.py` shows for it, so a check is a number, not an impression. Change a rule
here and the skill follows; the skill never needs to change with it.

The vault is all of `docs/`: design docs at the top level, and `research/`, `issues/`, `wiki/`,
`catalog/`, `constructions/`, `tasks/` and `prints/` below it. Decided in
[D-082](../../../docs/decisions-log.md#d-082--the-docs-vault-uses-obsidians-core-bases-for-live-views-dataview-and-other-community-query-plugins-stay-out).

## 1. Properties: a few, the same everywhere

| Where | Properties | Filled by |
|---|---|---|
| Top-level design docs | `status`, and `decisions` when the decisions log names the doc | by hand when the doc's state changes |
| Hubs (plan, backlog, decisions-log, faq, prints, site-graph, the runbooks and maps) | none | — |
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
  doc's research without anyone writing a list.
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
constructions purple, tasks light blue, prints orange, design docs blue). The groups live in
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
