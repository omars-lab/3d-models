---
name: secret-check-no-stdout-leak
description: "Omar authorized running commands that internally materialize a secret (e.g. dotenvx decrypt) as long as NOTHING sensitive reaches stdout/context — emit only booleans, lengths, or masked results, then unset"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9aae5724-5284-48f1-85cb-3c0496a1c2e1
  modified: 2026-09-17T03:42:30.162Z
---

Omar (2026-09-16, during X2D bring-up) explicitly authorized me to run commands that
**decrypt/materialize a secret internally** — validating its shape, length, or a prefix/suffix —
**provided the secret value never reaches stdout or my context.** Emit only derived booleans
(`len==8: YES`, `starts_with_c: YES`), capture the value in a shell variable, and `unset` it right
after. This does **not** authorize printing the value, writing it to a file, or sending it anywhere.

**Why:** the auto-mode classifier blocks `dotenvx run` as "Credential Materialization" by default,
which is correct for the general case — but a validation that provably keeps the plaintext out of
context is safe, and Omar wants it treated as such rather than bounced to a `!`-prefix hand-run.
The proven-safe pattern (worked 2026-09-16): `v="$(dotenvx get KEY 2>/dev/null)"; printf '%s' "$([ "${#v}" -eq 8 ] && echo YES || echo NO)"; unset v` — value stays in `$v`, only the boolean prints.

**How to apply:** for a secret check, decrypt into a variable and print only the derived result; never
the value. If a command would put the plaintext on stdout (`dotenvx get KEY` alone, `cat .env` after
decrypt, echoing `$v`), do **not** run it — that is the line this authorization does not cross. The
[[bambu-x2d-bringup]] token (`BAMBU_TOKEN` in the dotenvx `.env`) was validated this way; secret
storage/masking discipline is [[bikar-secrets-and-supabase]] and [[owner-gated-and-on-hold]].
