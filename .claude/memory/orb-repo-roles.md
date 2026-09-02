---
name: orb-repo-roles
description: Which of the four repos owns what (bikar engine, qiyas validator, 3d-models publishing, sacred-patterns contract), the local checkout layout, and which preset directories the orb pipeline globs
metadata:
  type: project
---

- **bikar** (`~/Workspace/git/bikar`, NaqshCoffee, private): the `.bkr` DSL + all 3D kernel work (`packages/core/src/kernel3d/`), studio (`packages/web`), Lab (`packages/lab`), knobs (`packages/knobs`). Producer of record; 3d-models never reimplements it.
- **qiyas** (`~/Workspace/git/qiyas`, private): Python CV validator; `qiyas orb-validate` scores per-axis orb views; FastAPI `qiyas serve` on port 8731.
- **3d-models** (`omars-lab/3d-models`, public): design docs, gallery, `make orbs`/`make lab`/`make deploy`, gates. No CI — pre-commit hooks are the only run.
- **sacred-patterns**: canonical home of the bikar↔qiyas contract; contract rows are PROPOSED elsewhere and owner-accepted there.
- coffee-house-* repos live under `~/Workspace/git-naqshcoffee/`, a different parent, so bikar's pointer gate skips (never resolves) pointers into them.

**Why:** ownership decides where a fix goes and which repo's PR lands first (bikar before 3d-models so `bikar:` pointers resolve — [[use-case-map-mechanics]]).

**How to apply:** 3d-models `make orbs` globs only `bikar/patterns/Orbs/*.bkr` and renders every orb with `--check`; coupons, pieces, walls, assemblies live in `patterns/{Coupons,Pieces,Walls,Assemblies}/` precisely so they never enter the gallery pipeline. A new preset is claimed in three places: the lab pin-list test, `patterns/index.json`, and `public-surface.json`'s count. The primary bikar checkout is often parked on another session's branch; do work in a fresh worktree off `origin/main` ([[git-and-gh-mechanics]], [[bikar-build-and-test-traps]]). Studio access: [[bikar-studio-access]].
