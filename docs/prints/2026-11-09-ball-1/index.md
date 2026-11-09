---
run: 2026-11-09-ball-1
plate: "ball-1 — the ping-pong ball alone, supports from the bed only"
plate_3mf: "ball-1.plate.3mf"
status: printed
outcome: no-reading
profile:
  machine: "Bambu Lab X2D"
  material: "PLA Basic, green #00AE42"
  spool: ~
  nozzle_mm: 0.4
  nozzle_type: ~
  nozzle_side: left
  layer_mm: 0.2
  slicer_profile: "Naqsh supports bed only 0.20mm @BBL X2D + Bambu PLA Basic @BBL X2D 0.4 nozzle"
  ambient_c: ~
  instrument: "none; looked at by hand, answered on the hub"
pins:
  bikar_ref: fe6b109e1bdb22fbfe6dbe2863b5dfa4e5b49a0a
  self_ref: ~
objects:
  - entry: "c1"
    source: "3d-models:.bambu/imports/airless-ping-pong-ball-20.stl"
    source_sha256: "0b9ba2089962c7e678d6f1c8b568afa3c96c9e9d74a160de06cc43083eff0102"
    params: {}
    count: 1
    iteration: "it-3efd211b452a"
    verdict: keep
    notes:
      - "A downloaded ball mesh (not ours), supports only from the bed and a support blocker in the hollow"
      - "Row 1, Omar: \"Ball good.\""
      - "Read, not said: whether the hollow came out clear and the nubs in the lower windows picked out was not answered one by one; \"good\" is taken as print it like this again"
photos: []
readings: []
feedback:
  lesson: "A support blocker inside the ball's hollow, with supports only from the bed, gave a ball Omar called good; toys-1's ball had support grown inside it. 0.4 mm nozzle, 0.20 mm layers, Bambu PLA Basic"
  decisions: []
  symptom: "Omar: \"Ball good.\""
  cause: "The blocker keeps the slicer from growing support in the hollow; the bed-only setting keeps support off the shell's upper windows"
  next: "Print the ball like this again: the same recipe, the blocker and the bed-only supports. No change to try"
---

Omar looked at the ball after the print and answered its one question on the hub's judging page
on 2026-11-08.

The bed had one piece: the airless ping-pong ball, a downloaded mesh kept out of git and pinned
by its sha256. It has no carved id. The slice put supports only on the bed and a blocker in the
hollow, so no support could grow inside the ball.

| Question | Answer | In Omar's words |
|---|---|---|
| 1. Did the ball come out hollow, with only the outside held up? | in my words | "Ball good." |

**Read, not said.** The question asked for three things: a clear hollow, whether the nubs in the
lower windows picked out, and whether it bounces. His answer covers the ball as a whole, so it is
read as the first of the row's outcomes, "print it like this again". No piece-by-piece readings
are recorded.

**The print.** Sent at 00:23 UTC on 2026-11-09 in green from AMS 0 slot 3, 10.08 g by the slice.
Finished at 01:36 UTC, all 201 layers (the [print log](../../design/plates/print-logs/ball-1.md)).
Nothing was measured with a tool, so there are no readings and no bet moves.
