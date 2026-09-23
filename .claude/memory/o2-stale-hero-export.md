---
name: o2-stale-hero-export
description: A reconstruction's hero export.png in the iCloud data dir can be stale relative to its step renders; O2 refuses a non-uniform frame; rebuild the hero with the loop's two commands before scoring
metadata:
  type: project
---

Found 2026-09-17 on 7apC5Q9QS-8: `reconstruction/render/export.png` was a 5123×5123 RGB square from an earlier run (no `export.size` sidecar) while the step renders and `export.ggb` were current (1505×868 view → 3368×1942 at 96 dpi). Oracle O2 (`make naqsh-score` in youtube) derives placement from the view, so it scored two unrelated frames and reported recall 0.01 for a construction O1 had passed on every label.

**Why:** `yt_reconstruct.build_export` rebuilds the hero on every loop run, but nothing else does, and iCloud mtimes are not trustworthy enough to gate on. A frame error looks exactly like a drawing error in the O2 numbers.

**How to apply:** before trusting an O2 FAIL, rebuild the hero with the loop's own two commands (`scripts/ggb-build.sh --in <commands> --out render/export.ggb --export`, then `scripts/ggb-render.sh --dpi 96 --out render/export.png render/export.ggb`) and confirm `ev=export_size … verdict=ok`. `naqsh_score.py` now refuses a hero whose two axes scale the view differently (youtube `feat/ggb-coords` 49e7e1a, `docs/issues/naqsh-score-stale-hero.md`); a stale hero with the right aspect is still invisible to it. The second cause of that FAIL was bikar's lowerer drawing exported-but-hidden labels; the drawn rule is `exported && !hidden_at_end` (bikar PR feat/construction-7apC). See [[orb-repo-roles]], [[islamic-orb-project]].
