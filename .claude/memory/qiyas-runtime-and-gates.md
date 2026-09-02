---
name: qiyas-runtime-and-gates
description: qiyas runtime facts that bite — orb-validate needs the :dev Docker image, host sweeps are broken so CI is the authority, ci.yml paths-ignore inverts a doc test, FastAPI only, which score fields mean what
metadata:
  type: feedback
---

- `qiyas orb-validate` needs the `:dev` Docker image (`cd qiyas && make build`); the GHCR `latest`/old tags predate it and the host venv lacks libcairo (cairocffi DYLD), so local composite sweeps are broken and CI is the authority for scores.
- `ci.yml`'s `paths-ignore` inverts a doc-parsing test: a docs-only push skips the run that reads the doc.
- The frozen `face_class` audit can be red at HEAD independently of your change; `ci-local-fast` skips it. Pre-existing gate debt (semgrep sha1 in cli.py, vulture, codespell) is not yours to fix in a feature PR.
- Never add Flask: qiyas already has a versioned pydantic contract (`schema.py` SCHEMA_VERSION, JSON Schema in `contract/schemas/`, drift-gated) and a FastAPI server (`qiyas serve` :8731, `/encoding`, `/diff`, `POST /deconstruct`); handlers return raw `JSONResponse`, so `response_model=` is what gets a shape into `/openapi.json` (qiyas #24 `62124f4`, `separate_input_output_schemas=False` keeps a pinned `$ref` when a schema is also a request body — #26 `95dd893`).
- Score semantics: `views[].scores` is the encoder floor while `recon_scores` is 0.0000 by construction; `geometric` is non-monotonic — never gate on it without `drop`. Orb view scoring is type-agnostic (Hungarian on centres, 0.02-diag acceptance); the typed self-diff caps at 0.67 by vocabulary split.
- Canonical fixtures under `fixtures-canonicals/` are gitignored by design (local-only).

**Why:** each was mistaken for a code regression at least once.

**How to apply:** build `:dev` before scoring; read CI, not the host; extend the FastAPI app. Contract flow: [[contract-and-schema-mirror]].
