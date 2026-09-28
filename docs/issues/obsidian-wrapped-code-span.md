---
date: 2026-09-28
---

# The table was fine; a wrapped code span broke it

Review thread 7rlhya (2026-09-28) on
[`construction-equivalence.md`](../constructions/construction-equivalence.md): the tables in
§5 and §6 showed as raw pipes in Obsidian, and the ask was a check that catches
broken tables.

## What was tried

The first guess was the tables themselves: a bad separator row or a stray pipe.
Both tables were well-formed — every row had the header's cell count, and the
same file rendered correctly on GitHub and in Obsidian's reading view.

## What the evidence showed

Screenshots of Obsidian's editor (Live Preview) before and after one edit
settled it. §4 had a code span that wrapped across a line break:

```
the naqsh side is `bikar render --piece Coaster --format stl
--check` of the same file
```

CommonMark allows that, which is why GitHub and the reading view were fine.
Obsidian's editor pairs backticks one line at a time, so the opening backtick
paired with the next backtick further down, and every span after it paired
wrongly. With an odd count left over, everything from §4 on — headings, bold,
tables — showed as raw text. Rejoining that span onto one line fixed §5 and §6
without touching either table.

## What replaced the table-only check

The gate got two render rules in `.claude/gates/docs_gate.py`:

- **D6** — a code span opens and closes on one line. Measured before gating: 133
  wrapped spans across 55 files under `docs/`. All were rewrapped by
  `docs_gate.py --fix-code-spans`, which moves the word holding the opening
  backtick down to the next line (or joins the next line up), so the rendered
  HTML is unchanged. The 55 files were rendered with `marked` before and after:
  0 differ. Three spans inside block quotes or next to a `+`-led line were fixed
  by hand; the `+`-led one had also been read as a list item on GitHub. `.claude/` is skipped, since it is not in the Obsidian vault.
- **D7** — every table row has the header's cell count. Measured: 13 hits in 6 tables,
  all real — 3 a pipe inside backticks, which splits a cell on GitHub too, and
  10 rows short of the header (a spare empty header cell, merged cells, a
  missing cell). All fixed.

The table check was still worth having, but it would not have caught the bug
that was reported. Check the actual render before you blame the element that
looks broken.
