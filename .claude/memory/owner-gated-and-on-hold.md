---
name: owner-gated-and-on-hold
description: "What only Omar can do and what is deliberately on hold — printing (no CAL bet settled), schema-v tag and npm publish, contract acceptance, Cloudflare/GHCR settings, studio secrets"
metadata:
  node_type: memory
  type: project
  originSessionId: b317004f-c205-413f-8ef8-7b5f99a1b742
  modified: 2026-10-03T20:01:37.689Z
---

**On hold — printing.** Decided 2026-07-27: printing is paused; when it resumes the machine is the Bambu A1/P1S/X1C class (256³ bed); catalog print targets stay "actuals only". Consequences: every `CAL-*` bet is provisional and no constant is earned; coupons (MC-1…MC-8, LG-*, W-F1/W-C1, LG-P1/P2) are `planned`; the prints tab ships an honest empty register and its gate is deferred to ship with the first real print (D-046).

**Sending a plate is no longer owner-only (D-093, 2026-10-03).** A session may run `bambu print send --yes` for a plate whose page in `docs/plates/` carries a live approval: Omar's tick, or his yes in chat naming that plate, written onto the page first. One approval per send; the send spends it. The `send-plate` skill runs it; see [[approvals-one-per-send]]. Loading filament and clearing the bed stay his.

**Owner-gated (never do these):**
- push the `schema-v*` tag / npm-publish `@naqshcoffee/qiyas-schema` (now 0.3.0 unpublished);
- accept contract rows in sacred-patterns (mirrors elsewhere stay PROPOSED);
- Cloudflare: the studio deploy token permission (deploy on main fails on it as of 2026-09-01), Access `self_hosted_domains`, redeploying the studio with its secrets (`setup-secrets.sh`); GHCR package access is UI-only;
- branch protection changes (applied 2026-09-02).
- the physical send: on 2026-10-03 the auto-mode classifier denied `bambu print send … --record --yes` ("Real-World Transactions") with only the recorded yes; after Omar wrote "explicit auth to send" in chat it ran. So: do send-plate up to the dry run and bed photo, and send only on an explicit chat go for this send (else hand him the `! <command>`); never retry a denial another way. Held again for send 2 the same day: his plain "yes" was denied, "explicit permission to send" ran it — so ask for that wording up front once the dry run is green.
- that first real CLI send (sheets-04b) failed at the FTPS upload with `553`: the X2D had no external drive (FTPS on 990 serves only external storage; Studio uses built-in eMMC over port 6000). The X2D takes a USB drive, not microSD. With a drive in, the second try ran on Omar's "expliclty authorizing run" (#501), started, then PAUSED at layer 0 with `0500-8051` (plate on the bed ≠ the gcode's plate). It ended FAILED `0300-400C` (a cancel, most likely Omar at the printer) at 20:12 UTC. Cause, settled 2026-10-03 from three sources (bed photo = gold Textured PEI; Studio conf `app.curr_bed_type` "4" = Textured PEI; slice `plate_1.json` `bed_type` cool_plate): our slices never named a plate, Studio's CLI defaults to Cool Plate (bed 35 °C, z 0.022 vs 55 °C, z 0.002), and the send said "auto". Fixed on branch `send-parity` (slice takes Studio's saved plate or `--plate-type`; send carries the slice's token and checks `cur_id`, P0101 = Textured PEI). sheets-04b needs a re-slice and a new yes. Resume, stop or a plate swap is Omar's call at the printer — never ours.
- printer option switches (`bambu options set`) are his, one go per change — EXCEPT the two plate switches (Foreign Object Detection, Type Detection), which are standing since 2026-10-07 (D-108, #609, Omar: "can you do this automatically per our skill? when you look at plates pre print"): at send-plate's bed look, write the verdict (`--non-bambu` for the glacier) and run `bambu options for-bed <plate> --yes` with no ask.

**Why:** these need credentials or ownership decisions the session does not hold; attempting them produces a confident failure.

**How to apply:** when a task lands on one of these, finish everything else, then hand the exact command back. Related: [[deploy-verification]], [[contract-and-schema-mirror]], [[bikar-studio-access]], [[calibration-baseline-trailer]].
