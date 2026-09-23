---
name: docs-gate-quirks
description: "Small docs-gate behaviours that CLAUDE.md does not spell out — PASS:/FAIL: must be bare at line start, C4 checks the list beside a count, research files are exempt from D4 and the pointer gate, absence rules vs coverage rules"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-09-19T04:31:22.162Z
---

- D2 wants a bare `PASS:` / `FAIL:` at line start in the validator's section; a backticked `` `PASS:` `` does not count.
- The counts gate's C4 checks the LIST beside a marked count, not only the digit — a new catalog entry means naming it in every list that counts it (P8 was caught this way).
- `docs/research/*` is exempt from D4 withdrawn literals and from the pointer gate: the convention there is a verbatim body plus an Errata section, so audit reports and survey files go there untouched.
- A superseded measurement (a composite score re-swept to a new value) is a version supersession, not a D4 withdrawal — keep the old number verbatim under a dated addendum; no WITHDRAWN row.
- An absence rule is not a coverage rule: a gate asserting "no style markers in stage frames" passed for weeks while the base solid was missing from every frame (D-037). Write the rule in both directions.
- A by-design FAIL test whose input is read from the file the fix changes stops testing the thing it exists for; pin the literal (D-039's linkage-gate test).
- Adding one bikar `Calibrated` record (e.g. CAL-CST-08 for twist) cascades: bikar's pre-commit regenerates `.claude/skills/calibrate/bets.md` in the 3d-models checkout (honors `THREED_MODELS_DIR`/`--out`), which bumps `bets`/`records`/`bets-design`/`design-records` totals, which the counts gate then flags at every `<!--count:cal-*-->` site across `backlog.md`/`decisions-log.md`/research. Bump the live project-state digits (keep the re-derived arithmetic block internally consistent) AND append the new id to the two design-bet lists (C4). A verbatim census quote in a research/audit file gets `<!--count:quote-->` (opts out of C1+C3, freezing the number as it read at audit time) — do NOT falsify the quoted digit. Editing a map-pinned doc (decisions-log) with no anchor move: run `validate.py` to confirm all pointers valid, then commit with `USE_CASES_OK=1` (nothing to stage in use-cases.md).

**Why:** each is a gate that stayed green through a real defect, or a false red that cost a rewrite.

**How to apply:** when a gate passes suspiciously, ask what it would take to make it fail; when adding a count or a validator, write the FAIL line first. Related: [[use-case-map-mechanics]].
