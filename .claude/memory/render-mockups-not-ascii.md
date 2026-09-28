---
name: render-mockups-not-ascii
description: Omar wants UI/layout mockups in design docs rendered (HTML in the product's styles, or the real tool) and embedded as a PNG — ASCII-art code blocks only as a stated fallback; and docs about color should show color pictures
metadata:
  type: feedback
---

A mockup in a design doc is a rendered picture, not a text sketch. Build it as HTML using the
product's own CSS tokens (for the Coaster Lab: bikar `packages/lab/src/style.css` and
`coaster.css`), screenshot it with headless Chrome
(`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=W,H --screenshot=out.png file://…`),
commit the HTML next to the PNG, and embed the PNG. When the real tool can draw it
(`bikar render --format preview`, the Lab), use that instead of a mockup. Label which parts are
real data (e.g. orbit rows from `bikar bands`) and which are stand-ins.

**Why:** Omar, review thread leu4yg on `colour-preview-design-a.md` §5 (2026-09-28): "Why is the
code block here text? why couldnt we have implemented HTML and got a screenshot of it and embedded
into doc? we should update our wokring model to take this paproach into consideration." Same day,
thread e7b42d: "why don't i see any images of color in this?" A doc about how something looks
that shows no picture of it cannot be judged.

**How to apply:** when a design doc describes a UI, a layout or a look, render it before shipping
the doc. The rule lives in the `ground-design-doc` skill's Rules (CLAUDE.md is at its 200-line
cap). A gate was not added: ASCII mockups were found in only a few docs, too few to justify one
under "measure a rule before gating on it". Related: [[look-before-you-print]],
[[omar-working-preferences]].
