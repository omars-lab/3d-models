---
name: 3d-models-deploy
description: "How the 3d-models gallery site is built, rendered, and deployed (gh-pages, OpenSCAD, image pipeline)"
metadata: 
  node_type: memory
  type: project
  originSessionId: b5c27e75-8686-44ff-b3d9-1b6af5f89729
  modified: 2026-08-19T18:55:00.000Z
---

The `3d-models` repo publishes a static gallery (`index.html`) of OpenSCAD cookie cutters.

- **Deploy branch:** the live site is served from the **`gh-pages`** branch, which has a **diverged history** from `master` (its own copy of `index.html` + `build/`). Changes on `master` do NOT appear live until ported to `gh-pages` — use `make deploy` (worktree-based; never run a bare `git rebase`/`git checkout gh-pages` in the main worktree, it hijacks it).
- **Live URL:** `https://blog.bytesofpurpose.com/3d-models/` (omars-lab.github.io/3d-models/ 301-redirects there). The old `3d-models.bytesofpurpose.com` CNAME was deleted on gh-pages (commit "Delete CNAME") and no longer routes; `make deploy` does NOT manage CNAME so it preserves whatever Pages settings dictate.
- **`make deploy` succeeding is not the site being live.** The push returns immediately; GitHub Pages then builds for ~40 s, and during that window newly-added paths 404 while already-published ones still serve 200 — measured 2026-08-19, when `/breakdown.html` and `/build/orb-breakdown/index.json` 404'd while `/` and `/lab.html` were fine, then both went 200 once the build finished. Do not diagnose a serving bug from that: check `gh api repos/omars-lab/3d-models/pages/builds/latest --jq '.status, .commit'` and wait for `built` at the commit you pushed. Also probe the custom domain directly — the `omars-lab.github.io` 301 makes every path read as a redirect first.
- **Only `DEPLOY_PATHS` goes live.** `build/orb-views/` is deliberately not in it — that is the gray qiyas instrument set, not a published surface; the gallery ships `build/images/`. A 404 on `build/orb-views/...` is correct, not a missing file.
- **gh-pages tracks `.DS_Store` files** — they can block `git checkout`/rebase from the main worktree; `make deploy` avoids this by using a separate worktree.
- **Working dir:** `/Users/omareid/workplace` is a symlink to `/Users/omareid/Workspace` — both paths are the same repo.
- **OpenSCAD binary:** `/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD` (the `openscad` shell alias may point to a stale/missing path). Cornfield render bg = `#FFFFE5`.
- **Render pipeline:** `.scad` in `src/CookieCutters/` → `make cookie-cutters` builds `build/images/*.png` + `build/stls/*.stl`. STL export with Minkowski (Camel, Ballarina2) is very slow and can hang headless — render PNGs only when you just need previews.
- **Web images:** `build/images/web/*.png` are post-processed (cream `#FFFFE5` keyed to transparency + autocropped via PIL) so the gold renders float on the gallery background. The gallery `index.html` references these, not the raw renders.
- **Pillow gap (2026-08-02):** no system python has Pillow — homebrew's `python3` moved to 3.14 with empty site-packages, so `make deploy` fails at `web-images`. Fix: `python3 -m venv`, `pip install pillow pyyaml`, then `make deploy PYTHON=<venv>/bin/python3`. Faster path, verified 2026-08-19 — several miniconda envs already carry Pillow and need no setup: `make deploy PYTHON=/usr/local/bin/miniconda3/envs/workspace/bin/python3` (also `genai-note-companion`, `knowledge-agents`, `markitdown`). The default `py3` env is *not* one of them, which is why the bare `make deploy` still fails at `web-images` every time. Also pass `BIKAR_DIR=` explicitly when the primary bikar checkout isn't on main — `make lab` vendors whatever tree BIKAR_DIR points at (default `~/Workspace/git/bikar`).
- **Gallery design:** titled **"Islamic Cookie Cutters"** (NOT "Sacred Patterns" — that's a separate site of Omar's; avoid reusing it here). No Arabic subtitle. "architectural/blueprint" aesthetic — warm paper grid, Fraunces serif + IBM Plex Mono, single terracotta accent. Deliberately avoids the old Inter + purple-gradient "AI slop".
- **Known model quirk:** SVG `import(..., invert=True)` is invalid (capital `True`, and `invert` isn't an SVG import param) — removed from Camel/Ballarina/Ballarina2. Kaaba was redesigned from a lopsided hexagon to a clean cube.
