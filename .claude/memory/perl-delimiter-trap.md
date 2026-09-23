---
name: perl-delimiter-trap
description: perl -pi with `|` delimiters silently matches empty when the pattern contains `||`, prepending the replacement to line 1; use s{}{} delimiters for shell text
metadata:
  type: feedback
---

Twice in one session (2026-09-17) a `perl -pi -e 's|…|…|'` edit on a `.sh` wrapper containing
`||` matched the empty string and prepended the replacement to line 1, leaving the header
after the `die` line. Self-observed, not a user correction.

**Why:** the `|` inside the pattern ends the pattern early; perl compiles a shorter regex that
matches at offset 0 of every line.

**How to apply:** for any shell, Makefile or code text that can contain `|`, use brace
delimiters (`s{…}{…}`) and re-read the first three lines of the file after the edit. Prefer
the Edit tool when the target is unique.
