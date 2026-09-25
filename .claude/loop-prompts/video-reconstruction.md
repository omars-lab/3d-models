# Loop prompt — take a tutorial video apart and rebuild it

Paste the block below into a fresh session **in the youtube repo** (`~/Workspace/git/youtube`),
or run it there as `/loop` with no interval. Written 2026-09-25. It lives here, next to the
other loops, because its output is what the catalog loop turns into coasters
([`catalog-expansion.md`](catalog-expansion.md)).

---

## The goal

**One tutorial video at a time becomes a GeoGebra construction that is proved to match the
video.** Every scored step must pass, and a person must have looked at the render. Each video
also leaves the tooling better for the next one.

The youtube repo calls one video taken all the way a **rung**, and the sequence of videos the
**ladder**. A rung is done when:
- `scripts/yt-study.sh status <id>` is green,
- the notes say how the construction converged and what caught each mistake,
- every gap the rung exposed in the tooling is either fixed or filed.

## Start here (in the youtube repo)

- The `youtube-ladder` skill owns the loop: screen, study, close gaps, record. Follow it.
  `youtube-study` does one rung. `youtube-reconstruct` does the construction.
  `youtube-retro` is for when a rung goes sideways.
- The ladder and its numbered gaps are in that repo's `.claude/plans/learning-from-youtube.md`.
  Finished rungs are in its `docs/tasks/done.md`.
- The worked example of a good iteration log is `reconstructions/bknVRSMcLj0/notes.md`: one
  entry per commit, what was wrong, and what caught it.
- `make ladder` lists the candidates; `yt-study.sh status <id>` shows a half-done rung.

## Each pass of the loop

1. **Finish before starting.** If any rung is half-done, finish it first.
2. **Screen, don't inherit.** Run `make ladder`. Prefer a GO with a short gap list over the
   next line of an old list. Write the verdict with its date.
3. **Rebuild it.** Take evidence from the frames (keyframes, zoomed crops), never from a
   guess that happens to fit a crowded frame. Build, score, look at the render, fix, and
   commit each step that improves the score, with the reason in the commit message.
4. **Close the gaps.** Name every place the tooling made the rung harder. Fix the small ones
   with a test. File the big ones as numbered gaps in the plan.
5. **Hand it on.** When the rung is done, add a line to `done.md` saying what the tooling can
   now do. Tell the catalog loop the id is ready to migrate.
6. **Stop** when: no candidate can be screened today; the next rung needs a gap bigger than
   one rung; the same step fails the same way twice (run `youtube-retro`); or Omar's own
   limit is reached. Say which one, then schedule the next wakeup 30 to 60 minutes out.

## Never

- Never mark a rung done on a best-effort score that no one has looked at.
- One rung per pass. Never fan out across videos.
- youtube has no remote. Commit on its main branch through its own checks, and keep
  generated renders out of git.
- Never download a video without the youtube skills' own licence and provenance steps.
