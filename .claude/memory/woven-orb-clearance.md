---
name: woven-orb-clearance
description: Every woven orb the gallery shipped would have printed as one lump — the amplitude rule was about centrelines, ribbons have width, clearance is now gated, and declared range endpoints are the least-tested values
metadata:
  type: project
---

D-039 (bikar #116 `546b734`, 3d-models #90 `5f3301b`): `linkageGate` measured 4 of 5 woven orbs fused. The prose rule amplitude ≥ `(strut_depth+0.4)/2` describes ribbon *centrelines*; the other ribbon's surface sits half a width off the node where the sinusoidal offset has already decayed, faster the denser the crossings. All five amplitudes were re-cut from measurement; two ranges widened because a default pinned at its ceiling "is a measured default quietly becoming an unmeasurable one". `MIN_BODY_CLEARANCE_MM = 0.4` is provisional against **CAL-CLR-01**, settled by coupon MC-8 (in-place wall pairs, explicitly not MC-1's assembled press fit — no transfer sentence, K10).

D-040 (bikar #117 `b414d5c`): `Maclado-9-Overlap`'s second ratio band merely compiles (`pieces=2`, two unlinked 30-ribbon chains) and amplitude cannot fix it; a band reported to its sampled endpoint is not a measured edge; inside band one clearance falls off a cliff (0.498 mm at 1.22 → interpenetration at 1.25).

**The tenet:** a declared `range lo..hi` is a promise and its endpoints are the least-tested values in it — they become Lab slider stops. Test the endpoints, reading them out of the `.bkr` so the test survives the range moving. Open decision: all five woven floors fuse (5/5), and raising a floor collides with a by-design test that the floor is legal — narrow the ranges vs run the gate in the Lab is a user call (plan §2).

**Why:** the picture-side (D-039 grew every projected split 75%) and print-side were fixed separately; see [[breakdown-page-instrument]].

**How to apply:** any new woven source ships with a linkage-gate reading at both endpoints; promote numbers from comments to gates, then measure them. Kernel context: [[orb-kernel-facts]].
