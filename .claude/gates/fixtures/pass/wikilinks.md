---
feeds:
  - "[[all-rules]]"
  - "[[pass/render-code-spans-and-tables]]"
  - '[[all-rules|the all-rules fixture, D1 to D7]]'
---
# Fixture: wikilinks that resolve

Asserted PASS fixture for the wikilink half of D1. Each form Obsidian resolves:
a bare name [[all-rules]], a name with `.md` [[all-rules.md]], a partial path
[[pass/wikilinks]], a heading and alias [[all-rules#Anything|shown text]], an
embed ![[render-code-spans-and-tables]], a case change [[ALL-RULES]], and a
same-file heading [[#Fixture: wikilinks that resolve]]. The frontmatter parses
as YAML (D8), and its last `feeds:` entry, an alias with a pipe right above the
closing `---`, is not read as a table (D7).

In code, `[[not-a-note]]` is a mention, and so is a fenced one:

```
Printer[[X2D over LAN]]
```
