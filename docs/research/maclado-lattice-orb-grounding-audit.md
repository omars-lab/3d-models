<!--
Provenance: adversarial grounding audit of docs/maclado-lattice-orb-design.md.
Date: 2026-09-02. Produced-by: general-purpose research agent (WebSearch/WebFetch +
bikar read at commit 1083046), under the ground-design-doc skill.
Feeds: docs/maclado-lattice-orb-design.md (Appendix A + Appendix B).
Preserved verbatim below; doc edits applied from the "Recommended doc changes" section.
-->

# Grounding audit: maclado-lattice-orb-design.md

**Auditor's bottom line.** This is, as the doc itself states (Appendix A), an almost-entirely-internal-geometry doc that adds **no new external claim**. Every external fact it leans on (the Martín López attribution, the 9-fold/twinning family story, the FDM wall/manifold constraints) is inherited from `docs/research/maclado-orb-survey.md`, which was already grounded, and the doc handles those claims faithfully — notably keeping the Martín López reproduction as a *non-goal*, so it commits **no K2 over-claim and no un-sourced attribution**. The load-bearing risks are therefore internal-consistency (K7), not grounding. I verified all bikar citations first-hand at commit `1083046`; they hold. The two open bets are correctly empirical (rim wall) or already recorded (mold economy). One genuine internal qualification is recommended (the "four classes" headline vs. the open mouth).

## Claim-by-claim verdicts

| # | Claim | Internal/External | Verdict | Supporting | Refuting |
|---|-------|-------------------|---------|-----------|----------|
| 1 | Full symmetric field = 20 nine-point wheels + 12 congruent 30-gon fillers, **one** filler class | Internal | **GROUNDED** — family §2 + `maclado-field.test.ts` | family doc §2; bikar `maclado-field.test.ts` | — |
| 2 | The 18-site walk's gaps close into **four** congruence classes on **two** separations (= M4c) | Internal | **GROUNDED** — matches M4c verbatim and the test | family §8 M4c; `maclado-lattice.test.ts:115` (`13 tiles → 4 classes`, members `[8,2,2,1]`) | — |
| 3 | A walk visiting all 20 sites *is* `Maclado-9` (only the OPEN partial field is distinct) | Internal | **GROUNDED** — sound: a walk chooses subset+order, never a new position; 20 sites → same 20 wheels → same 1-class field | doc §1; positions fixed by dodecahedron (family §2) | — |
| 4 | An open bowl (inner + outer + rim) is a watertight closed 2-manifold with no boundary edge | Internal (topology) + External (FDM) | **GROUNDED** — standard mesh topology; a boundary edge = an edge on one face = a hole = non-manifold, and a rim removes it | [hubs.com](https://www.hubs.com/knowledge-base/fixing-most-common-stl-file-errors/); [meshy.ai](https://www.meshy.ai/blog/fix-non-manifold-edges-stl-repair); [tripo3d](https://www.tripo3d.ai/blog/watertight-3d-models) | none found |
| 5 | genus 379 / Euler −756 is the **full** field's, not the partial shell's | Internal | **GROUNDED** — and the cited file is correct | `wheelfield-orb.test.ts:171-172` (`genus 379`, `euler −756`); also in `maclado-field.test.ts:139` | — |
| 6 | DSL cannot express "18 of 20" today; `place?: 'dodecahedral'` only | Internal | **GROUNDED (with a wording nit)** — see spot-check | bikar `parser.ts:168`, `placement-rule.ts` (only `dodecahedral` registered) | — |
| 7 | `latticeWalk(field, length, start)` / `siteSeparations(field, sites, tol)` are analysis-only; no `src/` mesh consumer | Internal | **GROUNDED** — signatures exact; M4c states "no solidify/seam/weave machinery consumes it" | `maclado-lattice.ts:37,71`; family §8 M4c | — |
| 8 | "Keep the **four filler classes** whole and visible" as an object goal | Internal | **CONTESTED (by the doc itself, K7)** — the 4-class count is M4c's measurement over the *closed* 18-site hull decomposition; the OPEN shell leaves mouth tiles unfilled, so the emitted interior fillers may realise **fewer than four** classes | doc §1 goal 2 vs. §3 step 3 ("gaps that bound an unvisited site are not filled") | — |
| 9 | Reproducing a specific Martín López object is a non-goal; "no walk is claimed to be his" | External | **GROUNDED** — faithful to survey §3 (placement rule unretrievable); no attribution over-claim added | survey §3; family §1 | — |
| 10 | Rim reuses the strut thick-shell cross-section, "no new free number" | Internal + Empirical | **GROUNDED as stated, with correct empirical escape hatch** | doc §7 K10-transfer sentence | — |
| 11 | Rim wall may need to be thicker for mouth rigidity | Empirical | **UNGROUNDED–EMPIRICAL (correctly flagged)** — only a coupon/printer settles it; doc routes it to a `CAL-*` bet | doc §7, App. B | — |

## Counter-evidence deep dives

Only two claims are literature-groundable; neither yields real counter-evidence.

**Bet A — "a rim closes a thick shell into a watertight solid; an open shell is still a manifold."**
This is standard and the doc states it correctly. What the sources say:
- [hubs.com — Common STL errors](https://www.hubs.com/knowledge-base/fixing-most-common-stl-file-errors/): a **boundary edge is an edge connected to only one face**, indicating a hole; such a model "does not represent a closed, watertight volume." Exactly the doc's §4 by-design FAIL (un-hemmed shell has a boundary edge).
- [meshy.ai — Fix non-manifold edges](https://www.meshy.ai/blog/fix-non-manifold-edges-stl-repair) and [tripo3d — Watertight models](https://www.tripo3d.ai/blog/watertight-3d-models): a printable mesh is a closed surface where **every edge is shared by exactly two faces**; slicers (Cura, PrusaSlicer, Bambu, Chitubox) fail/skip/blob on violations. The doc's "inner + outer + rim = closed, no boundary edge" is precisely the condition these require. **No source complicates it** — the topology is uncontroversial.
- One honesty nuance worth carrying: [Prusa — "Watertight 3D printing: vases, cups and open models"](https://blog.prusa3d.com/watertight-3d-printing-pt1-vases-cups-and-other-open-models_48949/) uses "watertight" in the *holds-liquid* sense (vase/spiralize mode prints a single-wall **open, non-manifold** surface that is nonetheless waterproof). The doc uses "watertight" in the *mesh-manifold* sense. These are different meanings; the doc's usage is the correct one for a mesh gate, and it never conflates them — but a reader coming from the hobby literature could. No change required.

**Bet B — prior-art novelty of a "lattice-walk-selected asymmetric wheel-field made printable."**
The doc makes **no hard novelty claim** ("no system does X"), so there is nothing to refute — this is the correct posture (K2-clean). The survey already scopes the nearest prior art (Kaplan's 3D-printed spherical star balls use 10-/12-point stars on truncated-icosahedron/dodecahedron symmetry — never 9; Bonner classes 9-fold as strictly non-systematic) under an explicit "of the sources surveyed here" hedge. The doc inherits that framing and adds no un-scoped assertion. I did an independent sanity sweep for equivalent generative-sculpture prior art (asymmetric polyhedral subset openwork spheres) and found nothing that would force a novelty *retraction* — but since the doc claims no novelty, this is confirmation, not a finding.

## Citation spot-check results

All verified in `~/Workspace/git/bikar` at the doc's pinned commit `1083046` (exists; HEAD is `5b9fb27`). Every cited file resolves.

- **Family §8 / M4c says what the doc attributes to it — YES, verbatim.** Family doc: *"an 18-wheel walk cuts into 13 tiles → 4 congruence classes on 2 distinct separations; a 13-wheel walk gives 12 tiles → 6 classes; the full 20-site field closes … at 12 tiles → 1 class."* The bikar test confirms: `maclado-lattice.test.ts:115` — `13 tiles`, `4 classes`, member sizes `[8,2,2,1]`. The doc's "four classes / two separations" and "one class to four" are faithful.
- **genus 379 / Euler −756 is the FULL field's — YES, and the doc's citation is correct.** The doc cites `wheelfield-orb.test.ts`; that file (`:171-172`) pins `genus 379`/`euler −756` for the closed shell, with a comment deriving `χ = 4 − 2·380 = −756`. (The same numbers also appear in `maclado-field.test.ts:139`, which is what the *family* doc cites — so both docs point at valid, mutually consistent locations; not a discrepancy.) Internal check: `χ = 2 − 2g = 2 − 758 = −756` ✓.
- **The hull-face generalisation (M4c generalised the cut "one tile per hull triangle → one tile per hull face") — confirmed** in family §8 and `maclado-lattice.test.ts` (`path.length − hullEdgeCount + hullFaceCount === 2`).
- **`latticeWalk`/`siteSeparations` analysis-only — confirmed.** Signatures exact (`maclado-lattice.ts:37,71`); M4c explicitly: *"no solidify/seam/weave machinery consumes it."*
- **`place?: 'dodecahedral'`, only rule registered — confirmed** (`parser.ts:168`; `placement-rule.ts:61,90-93` "v1 ships the one dodecahedral rule").
- **`3d-models:Makefile:L290 "patterns/Orbs"` — confirmed** (line 290 is the `for bkr in $(BIKAR_DIR)/patterns/Orbs/*.bkr` glob).

## Misgrounded or missing citations

Nothing misgrounded. Two small precision issues, neither blocking:

1. **§2 wording nit — "`base wheelfield` explicitly refuses a `sites` count."** The DSL *does* carry a `sites?: number` field (`parser.ts:172-173`), but its docstring scopes it to **`base sphere` only (v1: 1 or 2)** — it is not available to the wheelfield path, and even on `base sphere` it caps at 1–2. The doc's *conclusion* ("the DSL cannot express 'eighteen of twenty' today") is correct; the phrasing "refuses a `sites` count" reads as "no such field exists," which is slightly too strong. Suggest: *"…the `sites` count exists only for `base sphere` (v1: 1 or 2); `wheelfield` does not take it, so the DSL cannot express 'eighteen of twenty' today."*
2. **§3 step 3 implies existing emission over a subset.** "each interior gap … **is filled by `maclado-filler.ts`**" reads as if today's filler emitter already runs over an 18-site subset. It does not: M4c's hull-face cut is *analysis-only* and `buildMacladoField` "takes no site subset" (the doc's own §2). §5 correctly lists "a subset field builder" as new kernel work, so this is a wording tension, not a false claim — but step 3 should say the filler emitter is *driven by* the new subset decomposition, not that it already does this.

## Empirical residue (candidate CAL bets)

- **Rim wall thickness (mouth hem).** Only a coupon decides whether the strut cross-section keeps the open mouth rigid, or the hem needs to be thicker. The doc already routes this to a `CAL-*` bet (§7, Appendix B) and refuses a bare number — correct. **Candidate id: e.g. `CAL-RIM-01`.** This is the one true empirical unknown.
- **Mouth-radius / rigidity of an open shell under print + handling.** Related to the above; a large fair mouth may bow or warp regardless of wall. If the coupon separates "wall thickness" from "unsupported span across the mouth," these may be two bets, not one.
- (Non-bets, correctly not owned here: min feature `CAL-FEA-01`, bed contact `CAL-BED-01`, body clearance `CAL-CLR-01` 0.4 mm — all inherited gates, not new numbers.)

## Recommended doc changes

**1. Qualify the "four classes" goal against the open mouth (the one substantive K7).** Goal 2 (§1) and the §4 congruence validator advertise "four filler congruence classes," but that count is M4c's measurement over the **closed** 18-site hull decomposition (13 tiles), while §3 step 3 leaves the mouth-bounding tiles *unfilled*. The object's *emitted interior fillers* are therefore a subset of those 13, and may realise fewer than four classes if the mouth consumes an entire class. Paste-ready:

> *The "four congruence classes" is M4c's measurement over the closed hull decomposition of the eighteen sites (13 tiles → 4 classes, member sizes 8/2/2/1). The open shell fills only the **interior** tiles — those whose bounding wheels are all in the walk — so the emitted fillers are the subset of the 13 that do not border the mouth. The object therefore exhibits **at most** four classes, and the build records how many survive once the mouth tiles are excluded; the per-filler validator (§4) checks each emitted filler against the four canonical templates, so a class the mouth removes is a smaller vocabulary, never a wrong tile.*

**2. Tighten §2's `sites` sentence** as in Misgrounded item 1 above (the field exists but is `base sphere`-only, v1: 1 or 2).

**3. Tighten §3 step 3** so it reads "each interior gap … is filled by the new subset-driven filler path (§5), reusing `maclado-filler.ts`'s emitter" — separating the *analysis* decomposition (M4c, exists) from the *emission over a subset* (new), which §5 already flags.

**4. (Optional, honesty) Add one line distinguishing the two senses of "watertight"** where the bowl argument is made (§3 step 5): the mesh-manifold sense (no boundary edge, every edge on two faces) is what `meshGate` enforces, distinct from the hobbyist "holds water" sense — so a reader is not tempted to treat a vase-mode single-wall surface as an acceptable substitute. Supported by [hubs.com](https://www.hubs.com/knowledge-base/fixing-most-common-stl-file-errors/) / [meshy.ai](https://www.meshy.ai/blog/fix-non-manifold-edges-stl-repair).

**New external sources to cite (if §3/§4's manifold framing is ever challenged):** the three FDM-manifold references above ([hubs.com](https://www.hubs.com/knowledge-base/fixing-most-common-stl-file-errors/), [meshy.ai](https://www.meshy.ai/blog/fix-non-manifold-edges-stl-repair), [tripo3d](https://www.tripo3d.ai/blog/watertight-3d-models)). But per this repo's grounding philosophy, the manifold requirement is already a *checked invariant* (`meshGate`, §4's by-design-failure validator), so a citation is optional — the gate is the grounding.

**Net:** No fabricated or misattributed citation; no K2 over-claim; the Martín López attribution is faithfully de-scoped; the FDM/topology claim is standard and correctly gated. The only substantive edit is the "four classes vs. open mouth" qualification (recommendation 1); the rest are one-line precision tightenings. Grounding is legitimately inherited from the family survey, and the sole real open bet is empirical (the rim wall), already routed to `CAL-*`.
