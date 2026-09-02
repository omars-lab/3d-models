---
name: orb-lab-conventions
description: Orb Lab and studio conventions that are decisions, not code — knobs are DSL params, touched-set overrides, print target stays out of share URLs, knobs live in packages/knobs, walls reach the Lab only via custom script
metadata:
  type: project
---

- Knobs are DSL-native `param name = v [range a..b [step s]] [advanced]` declarations (Omar's own proposal); out-of-range overrides are a hard ParseError, never clamped by the engine; `compileToGeometry` throws on an unknown override. Cross-param clamps (inner ≤ shoulder−8, amplitude ≥ (depth+0.4)/2 — the latter now superseded by [[woven-orb-clearance]]) stay UI-side.
- Touched-set model: only user-touched knobs are sent as overrides/URL keys; untouched ones refresh from the result so derived defaults recompute. URL `v=1&f=<id>&<param>=` with default elision; `code=<lz>` ≤1800 chars else `.bkr` download.
- Print-target picker (Bambu/Prusa/Ender + services, custom XYZ, `2R ≤ min(XYZ)−10`) lives in localStorage and NEVER in share URLs; weave family gets an FDM warning.
- The knob layer lives in `packages/knobs`; the `@naqshcoffee/ui` fold was abandoned (private GitHub Packages needs `GITHUB_PACKAGES_TOKEN`, unset → E401).
- Lab axis views are byte-identical to CLI `--format views` path data (scale 4 differs). Lab shows measured/declared, CLI declared/floor — same data.
- A wall reaches the Lab only via the custom-script path (preset chips are scoped out); orb-only UI is suppressed by payload shape (`strandCount: null`, `viewAxes: []`), not a flag; a wall's STL is `<Tile>-module`. Known wart: mesh-gate failure text still says "widen struts".
- Watchdog e2e: `subdivide` bombs fail fast; `divide C1 into 1200` + `connect every 541` gives ~9 s honest compute.

**Why:** these were chosen over alternatives with Omar; re-deriving them wastes a decision.

**How to apply:** new Lab features honour the touched-set and URL rules; new archetypes declare their own params. Dev mechanics: [[bikar-dev-server-and-browser-checks]].
