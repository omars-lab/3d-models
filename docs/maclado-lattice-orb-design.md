# The lattice-walk maclado orb — design doc (the fourth Family-3 orb)

Status: **shipped 2026-09-02** — increment 1 (`bikar#153`, the open-shell kernel)
and increment 2 (`bikar#154`, the `place rule latticewalk` DSL seam + integration)
are merged to bikar main; increment 3 is the 3d-models integration (this PR: the
decision record, the `make orbs` publish-pipeline skip, and the use-case map). The
fourth orb in the 9-fold maclado family
([`maclado-orb-design.md`](maclado-orb-design.md) is the family doc; this doc is
one orb). Authorised by the owner in [D-049 §5](decisions-log.md) ("build a fourth
orb, and use the build to find gaps and inconsistencies and make the approach more
robust in the process") and, this session, resolved to the **18-wheel open shell**
among the offered shapes. Ground truth pinned to bikar `1083046` (origin/main);
grounded 2026-09-02 (Appendix A). Its [stop list](#6-the-stop-list-d-049-5) is
complete — **eight detectors, no instruction** — so per D-049 §5 **no orb-creation
skill is written**. Recorded as [D-051](decisions-log.md). Printing stays HELD (no
printer in the loop); the mouth-span bet in Appendix B is still deferred.

---

## 1. What this orb is, and is not

The three shipped maclado presets — `Maclado-9`, `Maclado-9-Weave`,
`Maclado-9-Overlap` (`bikar:patterns/Orbs/Maclado-9.bkr` and siblings) — are the
**full symmetric field**: nine-point wheels on all twenty dodecahedral vertices,
their gaps closed by twelve congruent 30-gon fillers, one filler class. This orb
is the **quantized lattice walk** measured as M4c
([`maclado-orb-design.md`](maclado-orb-design.md) §8; bikar #92 `ec4518b`,
[D-031](decisions-log.md)) made into a shipped object: an 18-site walk along the
field's dodecahedral adjacency, whose gaps close into **four** filler congruence
classes on two distinct separations.

**Goals.**

1. **Realise the walk as a printable solid.** Place the eighteen walk wheels,
   close their mutual gaps with fillers, and hem the open boundary so the object
   is a single watertight manifold — the same export contract the family holds
   ([`maclado-orb-design.md`](maclado-orb-design.md) §5.5, §7).
2. **Keep the filler classes whole and visible.** The walk's value over the
   symmetric field is *not* mold economy — the symmetric field wins that, one
   class to four ([`maclado-orb-design.md`](maclado-orb-design.md) §8, M4c). Its
   value is that the multiple classes are quantization's doing on an asymmetric
   partial field, and this object is the physical evidence. **A qualifier the open
   mouth forces:** the "four congruence classes" is M4c's measurement over the
   *closed* hull decomposition of the eighteen sites (13 tiles → 4 classes, member
   sizes 8/2/2/1). The open shell fills only the **interior** tiles — those whose
   bounding wheels are all in the walk — so the emitted fillers are the subset of
   the 13 that do not border the mouth. The object therefore exhibits **at most**
   four classes, and the build records how many survive once the mouth tiles are
   excluded. Whole-filler congruence is still verified per tile against the four
   canonical templates (§4), the family's standing invariant
   ([`maclado-orb-design.md`](maclado-orb-design.md) §5.3), so a class the mouth
   removes is a smaller vocabulary, never a wrong tile.
3. **Log the build as a process measurement.** Every stop an earlier orb also
   needed is written into §6 labelled *detector* or *instruction*, under the
   D-049 §5 rule. This is the reason the orb is built at all; the object is the
   vehicle.

**Non-goals, and the one that is load-bearing.**

- **A closed ball is out of scope, because it is not this object.** The twenty
  wheel positions are fixed by the dodecahedron; a walk chooses an *ordering and
  a subset*, never a new position. A walk that visits all twenty sites places the
  same twenty wheels as `Maclado-9` and closes to the same one-class field — it
  *is* `Maclado-9`, and building it would ship a duplicate. The walk yields a
  distinct object **only while the field stays partial**, so the open mouth where
  two sites are unvisited is not a blemish to close over but the condition under
  which the four-class result exists at all. This is the shape the owner chose.
- **The weave and overlap treatments** (Family 1) are out of scope here. The
  four-class result is a property of *filler tiles*, which only the solid
  (Family 2) field has; a woven walk would trace ribbons and carry none of the
  measurement this orb exists to make. Solid is not a preference, it is where the
  claim lives.
- **Reproducing a specific Martín López object** — the family's standing
  non-goal ([`maclado-orb-design.md`](maclado-orb-design.md) §1); his placement
  rule is unretrievable and no walk is claimed to be his.

---

## 2. Engine ground truth — bikar `1083046`

What exists today, and exactly where the walk stops short of geometry.

- **The walk instrument.** `bikar:packages/core/src/kernel3d/maclado-lattice.ts`
  exports `latticeWalk(field, length, start)` — a lowest-index-first DFS simple
  path along `field.adjacency` — and `siteSeparations(field, sites, tol)` — the
  sorted distinct pairwise arc separations of a site subset. Both are **analysis
  only**: their sole consumer is
  `bikar:packages/core/tests/kernel3d/maclado-lattice.test.ts`. Nothing in `src/`
  outside that file turns a walk into a mesh.
- **The field builder is closed to subsets.** `buildMacladoField` in
  `bikar:packages/core/src/kernel3d/maclado-field.ts` derives placement from the
  full icosahedral group and constructs all twenty wheels plus twelve fillers;
  it takes no site subset. Its solid path `solidifyMacladoField` gates on
  `mesh.stats.watertight`.
- **Placement grammar names one rule.** `bikar:packages/core/src/kernel3d/placement-rule.ts`
  registers only `dodecahedral` (all twenty sites); the DSL type is
  `place?: 'dodecahedral'`. A `sites` count *does* exist
  (`bikar:packages/core/src/dsl/parser.ts`) but only for `base sphere` (v1: 1 or
  2); `base wheelfield` does not take it
  (`bikar:packages/core/src/dsl/evaluator.ts`), so the DSL cannot express
  "eighteen of twenty" today.
- **The gap machinery already generalises to a partial field.** M4c generalised
  the §6 cut in `bikar:packages/core/src/kernel3d/maclado-gap.ts` from one tile
  per hull *triangle* to one tile per hull *face*, precisely so an asymmetric
  subset's gaps decompose. The filler emitter is
  `bikar:packages/core/src/kernel3d/maclado-filler.ts`.
- **The gates a new orb must pass** (all `bikar:packages/core/src/kernel3d/`):
  `mesh-gate.ts` (`meshGate` — watertight, degenerate-area floor, min feature
  `CAL-FEA-01`); `print-gate.ts` (`printGate` — bed contact `CAL-BED-01`, and a
  single-body count, which a shell with a coastline must not violate);
  `linkage-gate.ts` (`linkageGate` — body clearance `CAL-CLR-01` 0.4 mm, the floor
  the woven presets cite). The `stl --check` path runs `meshGate` and
  `linkageGate`; `--check print` adds `printGate`.

The one sentence M4c left open — "whether a lattice-walk orb is worth *shipping*
… is a separate scope decision" ([`maclado-orb-design.md`](maclado-orb-design.md)
§8) — is the decision D-049 §5 made. This doc does not re-argue it.

---

## 3. Construction

Five steps. Steps 1 and 3–4 reuse the family's machinery; **step 5 is new** — the
symmetric field has no boundary, so nothing in bikar hems one today.

1. **Select the walk.** `latticeWalk(field, 18, start)` returns eighteen site
   indices; the two unvisited sites define the open region. `start` is a
   parameter (§4 pins its determinism).
2. **Place the eighteen wheels** with the existing `placeWheelInFrame`
   (`bikar:packages/core/src/kernel3d/maclado-field.ts`), unchanged — placement
   is per-site and never assumed the full twenty.
3. **Close the interior gaps.** The M4c hull-face cut
   (`bikar:packages/core/src/kernel3d/maclado-gap.ts`) is analysis-only today and
   `buildMacladoField` takes no subset (§2); the new subset-driven filler path
   (§5) drives the decomposition over the eighteen wheel centres and reuses
   `maclado-filler.ts`'s emitter. Each *interior* gap — one whose bounding wheels
   are all in the walk — is emitted and must be congruent to one of the four
   canonical templates (§4). Gaps that bound an unvisited site are **not** filled;
   they open onto the mouth.
4. **Find the coastline.** The mouth is bounded by a single closed loop of wheel-
   rim arcs and unfilled-gap edges — the coastline. It is computed as the
   boundary of the placed-and-filled region, and the build asserts it is one loop
   (a walk that split the field into two mouths would fail here, loudly).
5. **Hem the coastline into a watertight solid.** A bowl is a watertight manifold:
   an inner and an outer surface joined along a rim. The rim closes the thick
   shell's cross-section along the coastline, so the object is *visually* open —
   one mouth — and *topologically* closed, with no boundary edge. "Watertight"
   here is the **mesh-manifold** sense `meshGate` enforces — every edge shared by
   exactly two faces, no boundary edge — not the hobbyist "holds water" sense a
   vase-mode single-wall surface satisfies while staying non-manifold; the rim is
   what makes the two coincide. Then the family's tail runs unchanged: vertex
   weld, then `meshGate`
   ([`maclado-orb-design.md`](maclado-orb-design.md) §5.5).

**The closure invariant** (the family's §5.3, carried, not re-derived): a
placement's fillers are accepted only when **each** interior filler is congruent
to a canonical template within tolerance. An aggregate area or count cannot see
one stretched tile — the repo's standing lesson
([`maclado-orb-design.md`](maclado-orb-design.md) §5.3;
`lego-lab-design.md` §14). The walk has four templates where the symmetric field
had one, so the check runs against a four-entry template set.

---

## 4. Validators

Each carries the D2 marker and a hand-built counterexample.

**Validator (walk determinism):** `latticeWalk(field, 18, start)` returns the
same eighteen indices in the same order for a given `start`, independent of run.
PASS: two evaluations at `start = 0` agree index-for-index. FAIL: a build that
seeds the DFS from a set iteration order — two runs return the same *set* but a
different *order*, so a per-order downstream (the coastline's arc sequence)
silently differs while a membership check passes.

**Validator (per-filler congruence, four classes):** every interior filler is
congruent to one of the four canonical M4c templates, edge and angle residuals
below tolerance, checked tile by tile. PASS: a walk whose every interior filler
individually matches a template. FAIL: one filler stretched — its edges deviate —
while total filler area and filler count are unchanged, so an area sum or a count
passes and only the per-tile check fires.

**Validator (coastline is one loop):** the unfilled boundary forms exactly one
closed loop. PASS: an 18-walk whose two unvisited sites are adjacent or share a
filler, leaving one connected mouth. FAIL: a walk (or `start`) whose two unvisited
sites are antipodal and non-adjacent, opening **two** disjoint mouths — the build
must refuse it, not hem two rims and pass a watertight check that never noticed the
object has two holes. The 18-of-20 case makes this reachable, so it is gated, not
assumed.

**Validator (watertight after hemming):** the hemmed solid passes `meshGate` —
`mesh.stats.watertight` true, no boundary edge. PASS: the hemmed 18-walk shell.
FAIL: the *un*-hemmed shell (steps 1–4 without step 5) — a thick shell with an
open coastline has a boundary edge and is not a manifold; if this passes, the rim
is doing nothing. This is the by-design failure the gate exists to catch.

**Validator (own topology pins):** the orb's genus and Euler characteristic are
pinned to its **own** measured values, not the full field's. PASS: the 18-walk
shell matches its recorded genus/Euler. FAIL: the test reuses the symmetric
field's genus 379 / Euler −756
(`bikar:packages/core/tests/kernel3d/wheelfield-orb.test.ts`) — a partial field
with a mouth has fewer tunnels and a different Euler, so those numbers are a wrong
witness that happens to be near.

---

## 5. What is new in the kernel — the detector surface

Everything the symmetric field never needed, and therefore everything the build
will stop on. Named here so §6's stops are recognised when they arrive.

- **A partial placement rule.** A `lattice-walk` rule in `placement-rule.ts`
  driven by `latticeWalk`, taking `length` and `start`; the first placement rule
  that is not the whole field.
- **A subset field builder.** `buildMacladoField` parameterised by a site subset,
  or a sibling that takes one — the first field that is not twenty wheels.
- **A boundary.** The coastline and its rim (step 4–5) — geometry with no
  precedent in the family, because a closed sphere has no coastline. This is where
  the build is most likely to discover an *instruction* (a thing only a prior
  orb-builder would know) versus a *detector* (a check that could have caught it).
- **DSL surface.** `place rule lattice-walk length N start K` in the grammar
  (`parser.ts`, `evaluator.ts`, `ast.ts`), validated on `base wheelfield`.
- **The preset.** `bikar:patterns/Orbs/Maclado-9-Lattice.bkr` — the only new file
  3d-models' `make orbs` will glob (`3d-models:Makefile:L290 "patterns/Orbs"`).

---

## 6. The stop list (D-049 §5)

The rule, verbatim in intent: every time the build stops for something an earlier
orb build also needed, the stop is written here with one label —

- **detector** — a test, gate or generated file could have caught or produced it.
  Detector items become gates or tests **in the same PR** that hits them.
- **instruction** — only a person who had built an orb before could have known it.

An orb-creation skill is written **only if** the instruction column is non-empty
when the orb ships, and it is then a checklist pointing at those entries and
nothing else. The precedent decides the empty case: two earlier skill proposals
were each evaluated against measured recurrence and both ended *no skill, a gate
instead* ([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md),
[`issue-register-evaluation.md`](issue-register-evaluation.md)).

**Validator (the stop list is honest):** at ship, every entry is labelled and
every *detector* entry names the gate or test it became. PASS: the orb ships with
each stop labelled and each detector pointing at its gate/test; the skill exists
iff the instruction column has entries. FAIL: a skill proposed before the list
exists, or with an empty instruction column, or a detector entry that named no
gate — the D-049 §5 failure, restated.

Increment 1 (the kernel geometry, `bikar#153`) touched only
`bikar:packages/core/src/kernel3d/maclado-field.ts` and its unit test — the
boundary §5 flagged as most likely to hide an *instruction* was discharged with
coastline/rim tests, so it arrived as a detector. Stops 1–7 are from increment 2
(`bikar#154`), where the orb reaches its public surfaces; stop 8 is from
increment 3 (this 3d-models PR), where it reaches the publish pipeline.

| # | The stop | Label | Became / who knew |
|---|----------|-------|-------------------|
| 1 | A new orb on disk must be registered as a Lab chip. | detector | `bikar:packages/lab/tests/orb-presets.test.ts` "offers every orb on disk" goes red on the unregistered `.bkr`. The test exists because `Maclado-9-Overlap` sat unregistered for a week; fixed by an entry in `bikar:packages/lab/src/scripts.ts`. |
| 2 | The orb must be listed in the pattern manifest. | detector | `bikar:packages/web/tests/pattern-manifest.test.ts` holds `bikar:patterns/index.json` to the files on disk; fixed by one manifest line. |
| 3 | The public `patternSources` count is stale (122 → 123). | detector | `bikar:packages/web/tests/public-surface.test.ts` recomputes the count from `bikar:patterns/index.json` and fails on the old number in `bikar:packages/web/public-surface.json`. |
| 4 | The orb must join the timelapse corpus table, as `[null, null]`. | detector | `bikar:packages/core/tests/kernel3d/orb-timelapse.test.ts` "covers every orb in the corpus" fails until the row is added; the cells-`null` is then forced by the same `projectOrbViewScene` throw the sweep sees, not a free choice. |
| 5 | `render --format views` exits 1 on the open-shell orb, killing the sweep mid-corpus. | detector | The `orb-validate` CI job went red — the same shape a 2D disc caused (`declaresOrbViews`). Graduated to the finer `drawsOrbViews` in `bikar:scripts/sweep-orb-validate.ts`, witnessed by `bikar:packages/lab/tests/sweep-declares-orb-views.test.ts` and reconciled in `bikar:packages/lab/tests/orb-composites.test.ts` (SWEPT / MESH_ONLY partition). |
| 6 | `place rule lattice-walk` will not lex — a hyphen is subtraction. | detector | The preset fails to parse and `bikar:packages/lab/tests/orb-presets.test.ts` "parses every registered script" catches it; the keyword is the compound word `latticewalk`, the precedent being `wheelfield` / `dodecahedral`. Recorded in `bikar:docs/decisions/2026-09-02-latticewalk-grammar.md` §3, so no one re-derives it. |
| 7 | Adding a decision doc regenerates the ledger, which sorted differently on macOS than in CI. | detector | The `coherence` gate went red on a `LEDGER.md` whose deadend rows macOS ordered before CI's C-locale ASCII. Fixed at the root — `export LC_ALL=C` in `bikar:scripts/gen-decision-ledger.sh` — so local `make ledger` == CI. Decisions-infra, not orb-specific, but it stopped this build and any build that logs a decision. |
| 8 | 3d-models' `make orbs` loop renders `--format views` on every orb; the open-shell orb exits 1 with a message the round-pattern skip does not match, so the loop's `else` branch stops the whole publish build. | detector | Same exit-1 as stop 5, but in the *publish* pipeline (`3d-models:Makefile` `orbs:`) rather than bikar's sweep. Fixed by a sibling skip branch grepping `has no cell decomposition` → STL only, no views/timelapse, no `src/Orbs` copy and no gallery entry (viewless orbs are absent from the gallery, like the round-pattern discs). The `else` stays as the fail-closed net: an unrecognized `--format views` error still stops the build. From increment 3 (this 3d-models PR). |

**The skill decision.** The instruction column is **empty**: every stop an
earlier orb build also hit was caught by a gate or test, and each became one.
Stop 6 is the only novel *knowledge* (the lexer's identifier class), and it is
not orb-specific — it recurs for any compound keyword, is readable from
`lexer.ts` or the two existing compounds, and is already written down as a
decision. By the D-049 §5 rule an orb-creation skill is written **iff** the
instruction column is non-empty, so **no skill is written** — the outcome the
precedent predicts ([`dsl-extension-skill-evaluation.md`](dsl-extension-skill-evaluation.md),
[`issue-register-evaluation.md`](issue-register-evaluation.md): *no skill, a gate
instead*). The eight detectors are the durable record; the next orb build inherits
them as red tests, not as a checklist to remember.

---

## 7. Print

The family's §7 governs unchanged ([`maclado-orb-design.md`](maclado-orb-design.md)
§7): the ribbon/strut cross-section, its nozzle-relative K10 condition, and the
single-watertight-manifold requirement that §4's watertight validator enforces.

The rim (step 5) introduces no new free number: it is the **same thick-shell
cross-section as the struts, hemmed along the coastline**. This transfers by
construction — same material, same wall, same shell, only a different edge — so it
carries the family's wall default without a fresh bet. Should the coastline demand
a wall the strut section cannot give (a fair mouth radius may want a thicker hem to
stay rigid), that is an empirical question and graduates to a `CAL-*` bet after a
coupon, never a bare number here.

---

## Appendix A — sources

The family's survey and grounding carry the 9-fold theorem, the divisor trick, and
the print constraints ([`maclado-orb-design.md`](maclado-orb-design.md) Appendix A;
[`research/maclado-orb-survey.md`](research/maclado-orb-survey.md)). This orb adds
no new external claim — the walk's numbers (four classes, two separations, the
hull-face cut) are measured in bikar and cited to M4c above. The grounding audit
is [`research/maclado-lattice-orb-grounding-audit.md`](research/maclado-lattice-orb-grounding-audit.md)
(2026-09-02): it verified every bikar citation first-hand at commit `1083046`,
found no fabricated or misattributed citation and no K2 over-claim, and confirmed
the Martín López attribution is faithfully de-scoped. Its one substantive finding —
the "four classes" count against the open mouth — is applied in §1 goal 2 and §4.
The mesh-manifold requirement §3–§4 leans on is a **checked invariant** (`meshGate`),
not a literature claim, so a citation is optional here; the standard FDM statements
of it are [Hubs](https://www.hubs.com/knowledge-base/fixing-most-common-stl-file-errors/),
[Meshy](https://www.meshy.ai/blog/fix-non-manifold-edges-stl-repair) and
[Tripo3D](https://www.tripo3d.ai/blog/watertight-3d-models).

## Appendix B — contested bets and open questions

- **The rim wall** — reused from the strut section by the §7 transfer sentence, so
  it is the **same quantity** as the family's ~2.0 mm wall default
  ([`maclado-orb-design.md`](maclado-orb-design.md) §7), not a new bet (one
  quantity, one bet). That family wall is itself a citation-grounded `**Default:**`
  the family defers to a coupon; this orb inherits it unchanged.
- **The unsupported mouth span** — the one thing a closed sphere never has, so the
  one genuinely new empirical unknown: whether an open shell bows or warps across
  the mouth regardless of wall thickness. It is deferred exactly as the family wall
  is — no printer is in the loop (printing is HELD), so it graduates to a `CAL-*`
  bet when 2.10.b's geometry exists and a mouth coupon can be cut, not before.
  Apparatus: a printed partial-shell coupon at the chosen mouth radius, measured
  for flatness of the rim after release and handling.
- **Mold economy** — the walk's four classes lose to the symmetric field's one
  ([`maclado-orb-design.md`](maclado-orb-design.md) §8). This orb does not dispute
  that; it ships for the measurement (§1 goal 3), and the losing comparison is
  stated, not buried.
- **`start` selection** — which of the walk seeds gives the fairest single mouth
  is a taste question left to the build; §4 only requires the chosen one produce
  one loop.
