---
name: contract-and-schema-mirror
description: The bikar↔qiyas contract flow — canonical in sacred-patterns, qiyas exports JSON Schema, bikar vendors it byte-identical under a runbook, a 3d-models gate now compares copy to source at the map's pins
metadata:
  type: project
---

qiyas exports `src/qiyas/contract/schemas/{annotations,diff,encoding,review_verdict}.json`; bikar vendors them byte-identical into `packages/qiyas-schema/schemas/` and codegens `src/*.ts` (runbook: bikar `.claude/skills/release-the-schema-mirror/SKILL.md`). Contract v1.5 was accepted and cascaded (sacred-patterns#36 `8a9e43b`, bikar#101 `2fc4d6e`, qiyas#17 `a77ed52`; qiyas v0.3.0 on GHCR `dfd0f76`). The mirror lagged by two stems with every check green because nothing compared copy to source; re-vendored in bikar #145 `cdc0331` and gated by 3d-models `.claude/gates/schema_mirror.py` (hook 41, `make validate-schema-mirror`), which reads both dirs at the use-case map's pins, names `$defs.X.properties lacks in bikar: …`, treats JSON-equal-but-reformatted as a finding, skips an absent sibling and FAILS on an unfetched pin.

**Why:** generated sibling schema types are a claim too; a vendored copy drifts silently unless a gate reads the source.

**How to apply:** change qiyas schema → run the runbook → the gate goes red in 3d-models until bikar is re-vendored and the map re-pinned. `packages/qiyas-schema` is at 0.3.0 unpublished; the `schema-v*` tag and npm publish are the owner's ([[owner-gated-and-on-hold]]). Runtime side: [[qiyas-runtime-and-gates]]; pin mechanics: [[use-case-map-mechanics]].
