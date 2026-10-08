---
name: third-party-stls-stay-out-of-git
description: "a downloaded STL on a plate (phone model, Printables bear) stays gitignored in .bambu/imports/ pinned by sha256; 3d-models is public; a re-cut by OpenSCAD 2021 changes the hash"
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-04T03:25:58.825Z
---

Third-party meshes on a plate recipe (`stl:` items, since #519) are never committed: 3d-models is a
public repo, a downloaded model's license may forbid sharing (the iPhone 16 Pro STL on sheets-04d),
and some are huge (the CC0 gummy bear is 34 MB). They live in the gitignored `.bambu/imports/` and
the recipe pins each by `sha256:`. A derived cut (the phone cut out of the phone+case model by
`docs/design/plates/sheets-04d-phone.scad`) is not committed either; the `.scad` that makes it is.

**Why:** licensing and repo size; decided while building sheets-04d (2026-10-03).

**How to apply:** never `git add` anything under `.bambu/imports/`; do not backtick those paths in
markdown (the pointer gate holds a backticked path to the repo). OpenSCAD 2021.01 writes the same
triangles in a different order each run, so a re-cut needs its new sha256 put in the recipe. A
two-body download may slice clean only as one body in its modeled pose — slice each body alone
before putting it on a plate. Related: [[owner-gated-and-on-hold]].
