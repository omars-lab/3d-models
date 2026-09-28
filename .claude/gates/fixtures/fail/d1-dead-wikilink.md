---
feeds:
  - "[[all-rules]]"
---
# Fixture: D1 must fire on a wikilink that names no file

Asserted FAIL fixture for rule D1 (K9), wikilink form. The frontmatter link
resolves (a note in `pass/`, found by name as Obsidian finds it); the one below
does not: [[no-such-note|a note that was renamed]].

Written as code, `[[also-missing]]` is a mention and is not checked.

Expected: exactly one finding, `D1 (K9) wikilink`.
