---
name: vault-setup
description: Audit and improve how the docs/ Obsidian vault is set up — properties (frontmatter), Bases views (Obsidian's built-in database/"SQL" tables), plugins (Dataview or not), links (markdown vs wikilinks), graph view colors, orphan pages and file names. Use for "set up / audit / revisit our Obsidian", "are we using bases / dataview / plugins / links properly", "the graph view is a mess", "which notes are orphans", "why are this note's properties missing", or after adding a new docs/ folder. Measures with tools/vault_audit.py, checks against vault-rules.md, fixes what is cheap, and reports the rest as options with pros and cons. Never installs community plugin code.
---

# vault-setup — measure the vault, compare with the rules, fix what is cheap

The vault is all of `docs/`. This skill is for its *setup* — the properties, views, links and
settings that make the notes findable — not for writing the notes. Author mode: the aim is a
notebook someone can browse, so keep the machinery small.

The rubric is [`vault-rules.md`](vault-rules.md), next to this file. Read it every run; it
changes without this file changing.

## The loop

1. **Measure.** `tools/vault_audit.py` (add `--json` to diff two runs). It prints plugins,
   properties per folder, invalid frontmatter, the Bases views and where each is embedded,
   link counts, broken wikilinks, orphans and id-like file names. It reads the worktree's
   `docs/` by default; `--vault <path>` reads another checkout.
2. **Compare** each number with its rule in `vault-rules.md`. Write down which rules hold and
   which do not, with the number.
3. **Fix what is cheap** — reversible, local, no judgment call:
   - an orphan: link it from its natural hub, or from the home page's "Also here" list;
   - frontmatter that does not parse: quote the value (the docs gate names the line);
   - a missing property on a new note in an area that has them;
   - graph colors: `tools/vault_audit.py --setup-graph` (merges into the local `graph.json`,
     keeps everything else);
   - a base embedded nowhere: embed it on [`docs/README.md`](../../../docs/README.md) or delete it.
4. **Report the rest** as options, each with its pros, cons and what it commits us to: a new
   property across a whole folder, a new base, a community plugin, a rename that moves links.
   A community plugin is always a decision for Omar, logged in the decisions log.
5. **Look at it in Obsidian.** Numbers do not show a view that renders empty. Open the base
   (`open "obsidian://open?vault=docs&file=bases/research.base"`), `screencapture -o -x <png>`,
   read the PNG. The live vault is the main checkout's `docs/`, so check after the change is on
   master, or copy a `.base` in under a scratch name, look, and delete it.

## Moving a note

`python3 tools/move_doc.py <old> <new> --dry-run` first, then without `--dry-run`; a whole
folder goes in one run with `--plan <file>` (one `old new` pair per line). It `git mv`s the note
with its review comments and picture folder, rewrites every link, pointer and path to it, and
lists what it could not rewrite — research prose, review threads, and the sibling repos (bikar
checks `3d-models/docs/...` pointers, so a move it names needs a bikar PR right behind). Never
move a note by hand or in Obsidian: Obsidian rewrites only the links it knows, not the pointer
baseline, the use-case map or code comments. `make validate-move-doc` runs its self-test.

## Why markdown links stay

Bodies keep `[text](path.md)` links: GitHub renders them, the docs gate checks them (D1), and
Obsidian counts them as backlinks anyway. Wikilinks go where only a wikilink works — properties
such as `feeds:`. Converting 1,000+ body links to wikilinks would break every page on GitHub for
nothing Obsidian does not already do.

## Checks that run without this skill

- The docs gate: D1 checks every wikilink names a vault file; D8 checks frontmatter parses.
- The prints gate checks print-record properties.

## What this skill does not do

- Install or update community plugin code (BRAT and review-md are the ones on).
- Edit `.comments.md` sidecars — use the `reviews` CLI.
- Rewrite note prose to fit a property. Properties describe a note; they do not replace it.
