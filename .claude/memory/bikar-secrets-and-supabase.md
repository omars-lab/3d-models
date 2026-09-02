---
name: bikar-secrets-and-supabase
description: How bikar secrets and the Supabase pattern store are handled — dotenvx sidecar keyed by origin remote, LastPass entry dotenvx/bikar, GitHub secrets set by pipe, the 42P10 upsert-index guard lives in coffee-house-sites
metadata:
  type: project
---

- bikar uses a dotenvx sidecar (`.env.encrypted` committed, `env-*` Makefile targets, pre-commit plaintext/keyfile gate, `manage-secrets` skill). The key is backed up as LastPass entry `dotenvx/bikar`; `env-keys.sh` derives the entry name from the **origin remote**, so pushing from a worktree cannot mint a second entry, and `make env-status` syncs before comparing because a push followed by a cache read once falsely said "NOT backed up" (inviting a redundant push, the one op that overwrites the vault).
- Repo secrets go to GitHub by piping `dotenvx get <NAME> -f .env` into `gh secret set` — values never displayed. supabase-js realtime needs Node ≥22 in workflows.
- Supabase project `gmwmrcmfywsdescglijg`: `bikar_patterns.folder text NULL` (NULL is the tree root) + UNIQUE `(user_email, name)`. Every studio save had failed `42P10` until that index existed — PostgREST rejects `ON CONFLICT` without a matching unique index, and the 201s were lies.
- `Prefer: resolution=merge-duplicates` overwrites only columns the body carries: the handler sends `folder: body.folder ?? null`, never an omitted key.
- The 42P10 class guard is `make supabase-check-upsert-keys` in coffee-house-sites (scans both repos' `on_conflict=` targets against live unique indexes; rejects partial/expression indexes; errors rather than narrows without a bikar checkout — which is why it is not a hook).

**Why:** each was a silent-success failure; "an acknowledgement is not an outcome" (bikar Tenet 31).

**How to apply:** never handle secret values in chat; verify a save against the DB, not the status code. Studio-side folder semantics: [[studio-folder-store]].
