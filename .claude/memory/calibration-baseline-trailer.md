---
name: calibration-baseline-trailer
description: bikar's calibration gate blocks baseline growth unless the tip commit carries a single-line Calibration-Baseline-May-Grow trailer in its final paragraph
metadata:
  type: feedback
---

bikar's `.calibration-baseline.json` gate is shrink-only: adding a `CAL-*` bet needs the trailer `Calibration-Baseline-May-Grow: <value>` on the **tip commit**, as **one line**, in the message's **final paragraph**. A multi-line value wrapped at column 0 made `git log --format='%(trailers:key=…)'` return empty and CI never set `may_grow=1`; a blank line above the trailer demotes it to prose, byte-indistinguishable from absent.

**Why:** git only parses trailers in the last paragraph and continuation lines must be indented; the gate's own guidance reads `git log -1`.

**How to apply:** put the trailer last, single line, on the commit CI will see (after a squash, that is the squash commit's message). The bets themselves are all provisional until something prints — [[owner-gated-and-on-hold]]; the bet format is the `calibrate` skill's business.
