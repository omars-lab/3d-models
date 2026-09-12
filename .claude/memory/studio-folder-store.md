---
name: studio-folder-store
description: "bikar studio folder semantics — root is an absent folder key never '', the dev overlay patterns/.folders.json is three-state, folders are labels not objects"
metadata: 
  node_type: memory
  type: project
  originSessionId: 416aa36c-c7af-4cf1-91db-d2cdc9668841
  modified: 2026-09-11T01:47:01.304Z
---

- **Root is an ABSENT `folder` key, never `''`**: `'' ?? null` is `''`, so an empty string lands in the column as a folder named `""` that no header renders while the tree draws the file at root — row and display disagree silently. `setPatternFolder` in `packages/web/src/pattern-api.ts` folds `''` into root, and lives there rather than `main.ts` because `main.ts` needs a DOM and cannot be imported by vitest.
- Dev's folder store `patterns/.folders.json` is a **three-state overlay**: entry absent = ask the disk, `name → "Orbs"` = filed there, `name → null` = deliberately at root. Omitting a root pattern hands the question back to the disk, so the move undoes itself on reload. The reader throws on an unparseable file rather than returning `{}`. On main the file is `{}`: the filing is the directory, the overlay is dev-only.
- A folder is a label, not an object: dragging the last file out dissolves it; `knownFolders` keeps it droppable for the session.
- Folder-move UI: drag onto a folder header to file, onto the root zone under the tree to unfile (bikar #49 `c9cf3fb`).

**Why:** two representations of "root" and two of "unset" produced a reload that reverted user moves with nothing to say why.

**How to apply:** any new per-pattern attribute follows the same null-vs-absent discipline end to end ([[bikar-secrets-and-supabase]] for the server half).

**Prod does NOT round-trip folders — confirmed live 2026-09-08 (#52).** Signed into
`bikar.naqshcoffee.com/editor` behind Access, dragged a root pattern into a folder and
watched the network: the move issues `PUT /api/pattern/<name>` with a body that *does*
carry the folder (`{"bkr_source":…,"folder":"Rosettes"}`), but prod answers **405 Method
Not Allowed** — there is no Pages Function accepting the write. Both reads 404:
`GET /api/patterns` (list) and `GET /api/pattern/<name>` (single) return the SPA
`404.html`, so the studio boots from the build-baked pattern seed (the `index.json` glob),
not the server. Reload → the moved pattern is back at root. So on prod the drag control is
present but silently no-ops: **folder persistence is dev-only** (the `.folders.json`
overlay + vite PUT handler), exactly as the dev-overlay note above implies. Wiring prod
persistence is a bikar + Supabase change (server half is paused — [[bikar-secrets-and-supabase]]),
an owner call, not done.

**Reframe — it was a DEPLOY gap, not missing code (bikar PR #166, 2026-09-09).** The 405/404
above are not "persistence unwritten": the handlers and `packages/web/tests/pattern-api.test.ts`
(folder round-trip + root/NULL) have passed on bikar `main` since 2026-07-31. CI shipped **zero
Pages Functions** because `.github/workflows/deploy.yml` ran `wrangler pages deploy
packages/web/dist` from the **repo root**, and wrangler discovers `functions/` **relative to its
working directory** — from root it finds none. Proof, three ways: CI run 33707538430 logged
`Uploaded 0 files (58 already uploaded)` with **no Functions bundle line**; the live 405/404; and
`wrangler.toml`'s own comment ("CI runs from the repo ROOT, so it never reads this file"). Fix
mirrors `make web-deploy`: `workingDirectory: packages/web` + `command: pages deploy dist`. Two
couplings the summary missed — running from `packages/web` means wrangler now **reads
wrangler.toml** (applies its `ASSET_STORE` binding per-deploy; that stale comment was rewritten in
the same commit), and the fix is **safe to merge with Supabase paused** (functions 502, client
`if (!res.ok) return` keeps the seed — no regression). Guard added: `check-deploy.sh` now asserts
an `/api` route is answered by a Function (200/401/502, no page marker) not the 404 shell — but it
runs only in the token-gated content branch, so **NOT VERIFIED until #125 mints the pages.dev
Access service token**. Live round-trip still owner-gated: merge #166, un-pause Supabase, verify
the `folder` column + non-partial unique index, set Pages secrets, deploy, re-verify.

**Merged + deployed, fix CONFIRMED LIVE (2026-09-09, bikar squash `784ff94`).** The merge
auto-triggered Deploy run `34350470307`; its deploy step logged `✨ Compiled Worker
successfully` + `✨ Uploading Functions bundle` (both ABSENT in the pre-fix run 33707538430's
`Uploaded 0 files`) and the guard printed `✓ /api/patterns — HTTP 200, answered by a
function`. Functions ship now; Supabase `gmwmrcmfywsdescglijg` is unpaused (Healthy). But the
Deploy WORKFLOW is still RED — on a *separate, pre-existing* cause (prior 3 runs also red): the
CF Access service token does **not** authenticate against `bikar-studio.pages.dev`, so every
token-branch content check gets a markerless 200 (the Access login wall) and the not-found path
returns 200 not 404. That is #63/#125 Access config, owner-gated. **Guard weakness caught:** the
`/api-present` check treats `200 + no page marker` as "a function answered", but the Access
login page is *also* 200-with-no-marker, so its ✓ is a false pass while the token is broken —
tighten it to assert a JSON/function marker once the token works. Live round-trip still owner
steps: fix the pages.dev token (or verify in a signed-in browser), confirm Pages secrets
`SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` on bikar-studio, confirm the non-partial unique index
(`make supabase-check-upsert-keys`), then drag→reload→persists.

**Guard weakness FIXED (bikar PR #167, 2026-09-09).** The discriminator is now the
**content-type**, not status+marker: a real Pages Function answers non-HTML
(`application/json` 200, or `text/plain` 401 without a usable JWT); both the SPA 404 shell and
the Access login wall are `text/html`. Requiring non-HTML rejects both and still accepts 401/502
as "shipped". The subtle bug the new test caught: `fetch` set the content-type in a shell
**variable**, but every caller runs it in a command substitution (`status="$(fetch …)"`) whose
subshell assignment is lost on exit — so the parent read the empty initial value and the wall
false-passed anyway. Fixed by recording content-type in a FILE (like `$BODY`), read back by
`ctype_of`. `scripts/check-deploy.test.mjs` locks in all four shapes (json/text401/wall/shell)
under `npm run test:scripts` (CI). This makes the token-branch content check trustworthy even
before #125 mints a working pages.dev token — a broken token now correctly FAILS the deploy
instead of silently passing.

**Round-trip verification tool SHIPPED (bikar PR #172, 2026-09-10, merged `eaed8a7`).**
`make check-round-trip` (`scripts/check-round-trip.sh` + `.test.mjs`) closes the live-persistence
question (#52 step 4) and step 3 transitively. Given a signed-in browser's **`CF_Authorization`
cookie** (via `$CF_AUTHORIZATION`), it moves a pattern to a test folder, READS IT BACK through
`GET /api/patterns` — the stored row, **never the PUT status** (the studio's own pre-fix bug
spread a PostgREST error object into a 200) — asserts the stored value changed, and restores the
original via a trap. A green run also proves the `folder` column + non-partial `(user_email,name)`
unique index (a 42P10 is reported with a hint; standalone check stays `make supabase-check-upsert-keys`).
**Auth is the browser cookie, NOT the service token**: a service token passes the Access edge but
is not a `CF_Authorization` JWT, so `functions/api/_cf-auth.js` `getCFJWT` 401s it — that IS the
401 seen against a signed-in session. Test's load-bearing case `liar` (a 200 that doesn't persist)
must FAIL, enforcing "verify the save against the DB, not the status code". Only owner step left on
#52: run it against the live studio with a real cookie.

**LIVE DIAGNOSIS 2026-09-10 (#52/#72) — the deployed function 401s a VALID Access session; the
blocker is bikar-studio's `CF_ACCESS_*` Pages config, NOT the cookie.** Drove the already-signed-in
`bikar.naqshcoffee.com/editor` tab via claude-in-chrome and ran the checks in-page (no cookie
extraction — same-origin fetch attaches the HttpOnly `CF_Authorization` automatically; the tool
*blocks* reading cookie/header values, which is fine, we never need them). Result: `GET /api/patterns`
→ **401 `text/plain` "Unauthorized"**, while `GET /cdn-cgi/access/get-identity` on the same origin →
**200 with full identity** (email present). So Access itself passed and the session is real; the sole
401 path is `functions/api/patterns.js:13 if(!payload)` — `getCFJWT` found the cookie but
`verifyCFJWT` (`_cf-auth.js`) returned null, i.e. `env.CF_ACCESS_TEAM_DOMAIN` (certs fetch, `:33`) or
`env.CF_ACCESS_AUDIENCE` (aud check, `:64-66`) is missing/wrong on the deployed `bikar-studio`
project. Most likely an **AUD mismatch**: if separate Access apps guard `bikar.naqshcoffee.com` and
`bikar-studio.pages.dev`, the single `CF_ACCESS_AUDIENCE` secret matches only one, and the
custom-domain cookie carries the other's AUD. **This CORRECTS the note above** ("the browser-cookie
path via the custom domain does not depend on that"): it 401s too. `make check-round-trip` with a
copied cookie, a `/debug` page, and cloudflared would all hit the same `verifyCFJWT` gate — none
bypass it. Owner diagnostic: `bash scripts/setup-secrets.sh --check` (needs CF token + decryptable
`.env`) lists whether `CF_ACCESS_TEAM_DOMAIN`/`CF_ACCESS_AUDIENCE` exist on `bikar-studio`; the
correct AUD is Cloudflare dashboard → Zero Trust → Access → Applications → (the app for
`bikar.naqshcoffee.com`) → Application Audience tag. Set both, redeploy, then re-run — see
[[bikar-secrets-and-supabase]] for the secret-push mechanics.

**CONFIRMED via the Cloudflare dashboard 2026-09-10 — the AUD-mismatch is real: TWO Access apps
front one backend.** Zero Trust → Access → Applications shows four self-hosted apps, two of which
guard the studio with DISTINCT AUD tags: **"Bikar Studio"** → `bikar.naqshcoffee.com` (policy:
NaqshCoffee org members) and **"bikar-studio - Cloudflare Pages"** → `bikar-studio.pages.dev` (+1
other domain; policies: org members + 1 other). The one `CF_ACCESS_AUDIENCE` secret on the
bikar-studio Pages project matches at most one of these, so a session on the custom domain 401s at
the function if the secret carries the pages.dev app's AUD (or is unset). FIX: set
`CF_ACCESS_AUDIENCE` = the **Bikar Studio (bikar.naqshcoffee.com)** app's Application Audience tag
(Access → that app → Details sub-tab), and `CF_ACCESS_TEAM_DOMAIN` = `<team>.cloudflareaccess.com`.
Simplest to set them directly in the Pages project → Settings → Environment variables (encrypted,
Production) — no dotenvx/wrangler needed — then redeploy. Robust alternative: consolidate both
hostnames under ONE Access app so a single AUD covers both (removes the two-meanings split). The
other two apps — **qiyas review backend** (`qiyas.naqshcoffee.com`, service-token policy, the review
proxy) and **Coffee House Sites** (`gallery.naqshcoffee.com` +1) — are unrelated to studio auth; no
action. Note: `setup-secrets.sh --check` tripped its dotenvx eval-export guard in Omar's interactive
`(py3)` shell (a non-brew dotenvx shadowing `/opt/homebrew/bin/dotenvx` 2.22.0, which emits correct
`export` lines); the dashboard route sidesteps it entirely.

**CORRECTION + collision (2026-09-10) — the script fix is ALREADY in-flight; publish via the
already-fixed script, no new PR.** The failing dotenvx guard is UNCOMMITTED work in the shared
bikar checkout (`fix/verifier-verdict-line`): another session's large in-flight feature already (a)
fixed `scripts/setup-secrets.sh` to dotenvx-decrypt an encrypted `.env`, (b) documented it in
`.claude/skills/manage-secrets/SKILL.md` (PATH recipe, the shadow trap, fail-closed guard,
`cf-tunnel-verify.sh` got the same), and (c) confirmed the script already publishes
`CF_ACCESS_AUDIENCE` to bikar-studio. So do NOT reimplement the fix off main and do NOT edit
`manage-secrets/SKILL.md` in a rival branch — both collide. **Correct re-run command is
homebrew-FIRST** (homebrew ships node v26.8.1 ≥22 *and* dotenvx 2.22.0, both `/opt/homebrew/bin`,
verified): `export PATH="/opt/homebrew/bin:$PATH"; bash scripts/setup-secrets.sh` from
`~/Workspace/git/bikar`. The **nvm-v22 `dotenvx` is the BAD, JSON-dumping build** that trips the
guard and once leaked `.env` to a transcript — it must NOT win the PATH (an earlier draft command
that put nvm-v22 first was wrong). After Omar runs it → redeploy bikar-studio → re-verify
`/api/patterns` flips 401→200 (#52/#72).

**CLOSED — live persistence CONFIRMED end-to-end 2026-09-10 (#52 + #72 done).** Omar published
`CF_ACCESS_AUDIENCE` (homebrew-first `setup-secrets.sh`, all Pages + Actions secrets ✓), then
bikar-studio was redeployed (`gh workflow run deploy.yml`, run 34529531415 — genuinely deployed:
`✨ Compiled Worker` + `✨ Uploading Functions bundle` + `Deployment complete`; the 16 post-deploy
reds are the KNOWN pages.dev service-token false-negative #63/#125, not a real failure). Verified in
the signed-in `bikar.naqshcoffee.com/editor` tab via in-page fetch (cookie auto-attached, never
handled): (1) `GET /api/patterns` → **200 application/json** (was 401 — the AUD fix worked); (2)
full **write round-trip** — `PUT /api/pattern/__roundtrip-probe.bkr` `folder:"__roundtrip_<ts>"`
→ 200, `GET` read back that **exact folder** from the DB; then `PUT folder:null` → 200, `GET` read
back ` root`. Read-back matched the write both times (not the status code). This proves the column
exists, `on_conflict=user_email,name` resolved a non-partial unique index (no 42P10), and root =
absent/NULL. **So prod DOES round-trip folders now** — the long "prod does NOT round-trip" thread
above is fully superseded; its diagnosis chain (deploy gap → AUD mismatch) was correct and is done.
**Side effect / gap:** the probe pattern `__roundtrip-probe.bkr` remained at root because **the
Pages API had NO `onRequestDelete`** — a pattern saved via PUT was permanent through the API.

**GAP CLOSED — `DELETE /api/pattern/:name` shipped (bikar PR #174, 2026-09-10, squash `0a0f34c`).**
`onRequestDelete` in `functions/api/pattern/[name].js`: same verified-JWT gate as read/write, scoped
to `user_email=eq.<you>&name=eq.<name>` so a caller only ever deletes their own row, never
`bikar_canonical_patterns`. Idempotent **204** (removed a row or found none — a 404-on-absent would
make a repeat/concurrent delete look like a failure); fails closed to **502** via `readRows` on any
PostgREST response that is not the array of deleted rows. Dev analogue in `vite.config.ts`: DELETE
removes the file (guarded within `patternsDir`) + drops its `.folders.json` entry via
`removeFolderOverlay` (mirrors a row delete taking its `folder` column). `check-round-trip.sh` is now
**self-cleaning**: on an empty account it provisions `__roundtrip-probe.bkr`, round-trips it, and
DELETEs it on exit via a trap (a named `CHECK_PATTERN` against an empty list is an error, not a reason
to invent one). Tests: real-handler DELETE (401/scoped-URL/204/502/no-leak) + `removeFolderOverlay`
cases + the harness empty-account path. **The leftover probe is deleted** — drove the signed-in
`bikar.naqshcoffee.com/editor` tab in-page: `DELETE /api/pattern/__roundtrip-probe.bkr` → 204, read
back `GET /api/patterns` → `[]`. Confirms the route is live in prod. Verify mechanics live in
[[bikar-secrets-and-supabase]].
