# Loop prompts

Each file is a self-paced `/loop` prompt for a clean session. There is one job per loop, and
each file names the other loops so no two do the same work. When the state changes, update
the matching file; don't add a new one.

| Loop | Job | Runs in |
|---|---|---|
| [`coaster-pipeline.md`](coaster-pipeline.md) | Get the first coaster plate printed, and measure the calibration numbers from it | 3d-models |
| [`print-infrastructure.md`](print-infrastructure.md) | Turn a short config file into a reviewed, send-ready plate with one command | 3d-models |
| [`catalog-expansion.md`](catalog-expansion.md) | Find new patterns and turn reconstructions into catalog coasters | 3d-models, bikar, youtube |
| [`video-reconstruction.md`](video-reconstruction.md) | Rebuild one tutorial video as a proved GeoGebra construction | youtube |
| [`consolidation.md`](consolidation.md) | Merge PRs, clean up branches, worktrees and stashes, and lose nothing | all six repos |

Work flows from reconstruction to catalog, then to the print infrastructure, then to the
printed plate. Consolidation runs beside all of them.
