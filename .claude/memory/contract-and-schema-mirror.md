---
name: contract-and-schema-mirror
description: "The bikar↔qiyas contract flow — canonical in sacred-patterns, qiyas exports JSON Schema, bikar vendors it byte-identical under a runbook, a 3d-models gate now compares copy to source at the map's pins"
metadata: 
  node_type: memory
  type: project
  originSessionId: 792c03e6-3f91-4133-a2ea-35c8bfde5227
  modified: 2026-09-03T04:33:41.088Z
---

qiyas exports `src/qiyas/contract/schemas/{annotations,diff,encoding,review_verdict}.json`; bikar vendors them byte-identical into `packages/qiyas-schema/schemas/` and codegens `src/*.ts` (runbook: bikar `.claude/skills/release-the-schema-mirror/SKILL.md`). Contract v1.5 was accepted and cascaded (sacred-patterns#36 `8a9e43b`, bikar#101 `2fc4d6e`, qiyas#17 `a77ed52`; qiyas v0.3.0 on GHCR `dfd0f76`). The mirror lagged by two stems with every check green because nothing compared copy to source; re-vendored in bikar #145 `cdc0331` and gated by 3d-models `.claude/gates/schema_mirror.py` (hook 41, `make validate-schema-mirror`), which reads both dirs at the use-case map's pins, names `$defs.X.properties lacks in bikar: …`, treats JSON-equal-but-reformatted as a finding, skips an absent sibling and FAILS on an unfetched pin.

**Why:** generated sibling schema types are a claim too; a vendored copy drifts silently unless a gate reads the source.

**How to apply:** change qiyas schema → run the runbook → the gate goes red in 3d-models until bikar is re-vendored and the map re-pinned. `packages/qiyas-schema` is at 0.3.0 unpublished; the `schema-v*` tag and npm publish are the owner's ([[owner-gated-and-on-hold]]). Runtime side: [[qiyas-runtime-and-gates]]; pin mechanics: [[use-case-map-mechanics]].

**Bump guardrails (bikar PR #164, merged 2026-09-03).** Two node-builtins-only scripts now enforce the release discipline the runbook only described: `scripts/schema-breakage.mjs` diffs `packages/qiyas-schema/schemas/*.json` against the latest `schema-v*` tag and prints the severity + the exact `npm version` command to run (`--assert <level>` fails CI if a change is more breaking than a ceiling); `scripts/check-schema-version.mjs` is a pre-commit BLOCK (override `SCHEMA_VERSION_OK=1`) if a watched schemas/src file is staged without a package.json version bump, and a `--ci` gate (`check:schema-version`, wired into `npm run ci` after `check:pointers`). **Pre-1.0 mapping (0ver, locked 2026-09-02 via user decision):** while `major==0`, a *breaking* contract change → `npm version minor`, additive → `patch` — so the detector reports MAJOR honestly but recommends `minor`. That is why 0.2→0.3 (breaking) was a minor bump and the pending 0.3.0 is correctly versioned. Runbook: bikar `.claude/skills/release-the-schema-mirror/SKILL.md` step 5.
