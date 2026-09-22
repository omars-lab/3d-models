---
name: print-wiki
description: The 3D-printing troubleshooting wiki — resolve a print/slice symptom (a slicer warning like "floating regions" or "can't select PLA…PLA", a mesh flag like non-manifold edges, warping/stringing/detachment, an AMS filament-mapping puzzle) into what it means, whether it is a concern for THIS part, and what to do — grounded in our own prints as proof. Also the maintainer: when a new gotcha, error, or nuance is met at the machine or in a slice, ingest it into docs/wiki/ as a durable entry. Use for "what does this warning mean?", "is <thing> a cause for concern?", "why did my print <symptom>?", "add this to the wiki", "capture this gotcha". It reads and writes docs/wiki/; it never changes a slicer setting and never dispatches a print (that stays the owner's gate).
---

# print-wiki — the LLM-maintained 3D-printing troubleshooting wiki

A knowledge base that **compounds**. Every print, every slice, every machine session throws off a
nuance — a warning that looks scary but is by-design, an error message that names the wrong cause, a
tolerance that only bites in one material. Left in a transcript, that knowledge is lost by the next
session. This skill turns each one into a durable **wiki entry** under `docs/wiki/`, grounded in our
own prints as proof, so the next operator meets the symptom already answered.

Two jobs, one skill:

- **Query (the front door):** an operator hits a symptom and needs to know *what it means, whether it
  is a concern for this part, and what to do.* This is the flagship — troubleshooting.
- **Ingest (the back door):** a new phenomenon is observed and needs to become an entry, or an existing
  entry needs the new evidence. Humans curate; this skill maintains.

It **advises**. It never silently changes a slicer setting, and it **never dispatches** — the physical
send stays Omar's owner gate (`bambu print send`, or the Studio GUI Print click).

## Basis — the Karpathy LLM-wiki pattern, adapted to this repo

This skill applies Andrej Karpathy's **"LLM Wiki"** pattern:
**https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f** (fetched 2026-09-21). The pattern:
three layers — *Raw Sources* (immutable evidence), *Wiki* (LLM-maintained markdown synthesis), *Schema*
(the config that governs it) — and four operations — *Ingest, Query, Lint, Index & Log*. Synthesis
compounds: nothing is rebuilt per query, and humans curate while the LLM maintains.

Prior art in this org: the **`wiki-manager`** plugin (oeid-claude-plugins) already implements this same
pattern, but bound to a NotePlan vault split into confidentiality spaces. That substrate is wrong for a
git-repo, print-grounded reference, so this skill **reuses the pattern, not that machinery** — an
in-repo `docs/wiki/` whose proof links point at real `docs/prints/` records.

### The three layers, mapped to this repo

| Karpathy layer | Here |
|---|---|
| **Raw Sources** (immutable) | Our print records (`docs/prints/<run>/`), slicer-warning sidecars (`*.sliced.3mf.warnings.json`), screenshots, the bikar/qiyas design docs, and external references (Bambu wiki, slicer docs). Cited, never rewritten. |
| **Wiki** (LLM-maintained) | `docs/wiki/**` markdown — one entry per phenomenon. Each says what it is, what it means, **when it is a concern and when it is not**, what to do, and links its proof. |
| **Schema** (config) | This `SKILL.md`, the entry [`template.md`](template.md), and the repo's grounding gates — the wiki lives in `docs/`, so `docs_gate.py` already lints it (see Lint). |

### The four operations

1. **Ingest** — a new gotcha/error/nuance is met. Add or update one entry, grounded in a cited source
   (a print record, a sidecar, a screenshot, a design doc). **Never a bare claim** — every "this is / is
   not a concern" ties to evidence or is explicitly labelled an unverified expectation.
2. **Query** — the troubleshooting front door. Match the operator's symptom to an entry; answer *what it
   means → is it a concern for THIS part → what to do*. If no entry exists, say so and offer to Ingest.
3. **Lint** — before shipping an entry, run it against the grounding rules (below). The wiki is under
   `docs/`, so the repo's doc gates enforce most of this automatically at commit.
4. **Index & Log** — keep [`docs/wiki/index.md`](../../../docs/wiki/index.md) (one line per entry) and
   append to [`docs/wiki/log.md`](../../../docs/wiki/log.md) (what changed, when, why, source) on every
   Ingest.

## Query — the troubleshooting front door (the flagship)

When an operator asks "what does this mean / is this a concern / why did my print do this":

1. **Find the entry.** Read `docs/wiki/index.md`, then the matching entry under `docs/wiki/troubleshooting/`.
2. **Answer the three questions the entry is built around**, in order:
   - **What it means** — the mechanism, in plain terms, carrying the source's hedge (K1).
   - **Is it a concern *for this part*?** — the load-bearing judgement. A "floating regions" warning is
     by-design cosmetic on a decor egg and a hard stop on a functional bracket; the answer depends on
     what the part is *for*. Never give a context-free verdict.
   - **What to do** — the action, or the explicit "nothing — proceed."
3. **Show the proof.** Point at the print record or sidecar the entry cites, so the operator can see it
   is grounded, not asserted.
4. **No entry yet?** Say so plainly. Do not invent a verdict. Offer to **Ingest** it once we have
   evidence (a real slice, record, or screenshot) — a wiki entry with no proof is exactly what this
   skill exists to prevent.

## Ingest — turning a phenomenon into an entry

Only Ingest what we have **actually observed**. This is the graduation rule (CLAUDE.md) applied to the
wiki: an entry is the durable record of a real gotcha, not a speculative FAQ.

1. **Gather the evidence first.** The slice's warnings sidecar, the print record, the screenshot, the
   design-doc section. No evidence → no entry (offer to slice/observe first).
2. **Copy [`template.md`](template.md)** to `docs/wiki/troubleshooting/<kebab-slug>.md` and fill every
   section. If an entry already covers the phenomenon, **update it** — do not fork a second entry (a
   migration never buys a fork).
3. **Ground every claim.** Each "when it is a concern" and "when it is not" ties to a cited source or is
   labelled an unverified expectation. Carry the source's hedge; do not harden a "may" into a "will".
4. **Link the proof.** Cite the print record (`docs/prints/<run>/…`) or sidecar. Until a real print
   exists (owner-gated, task #63), a slice sidecar or screenshot is the honest proof; mark the entry
   `proof: slice-only` and upgrade it to a print-record link when one lands (task #72).
5. **Index & Log.** Add the one-line pointer to `index.md`; append a dated line to `log.md`.

## Lint — the grounding rules (mostly enforced for free)

The wiki lives under `docs/`, so **`.claude/gates/docs_gate.py` already runs on every staged wiki file**
(`make validate-docs` over the whole tree). Write the markers; the gate checks the rest:

- **Relative links resolve (D1)** — every proof link and cross-link points at a file that exists.
- **`**Default:**` markers (K4→D3)** — any default value carries a citation link or a `CAL-*` bet id.
- **Anchored pointers** — a backticked `path:Lnnn` is a claim; anchor it `repo:path:Lnn "literal"`
  or cite the record/PR instead (prefer records over line numbers — they don't drift).
- **Withdrawn literals (D4)** — a number an audit has killed stays killed corpus-wide.

Beyond the gate, apply the grounding taxonomy this repo already teaches (CLAUDE.md K1/K2/K7/K10):
carry the hedge (K1), do not claim exhaustiveness over machines/materials you did not test (K2), read
the entry against itself (K7), and state the transfer conditions when a rule ported from one
material/nozzle is applied to another (K10).

**If a lint rule starts to recur across entries, graduate it to a gate — not a reminder.** That is the
repo's standing idiom (`docs/issue-register-evaluation.md`): measure the rule first, then gate it.

## This is a troubleshooting reference, not an issue register

The repo deliberately has **no issue catalog** (`docs/issue-register-evaluation.md`,
`docs/dsl-extension-skill-evaluation.md`): registers of past defects decay because nobody re-reads them.
The wiki is a *different animal* and must stay one:

- An **issue register** catalogs defects in *our own code/docs*, read once at fix time then never again.
- The **print wiki** catalogs *3D-printing phenomena the operator meets at the machine* — it has a live
  **query path** (every time a symptom appears), so it is re-read by design, and every entry is grounded
  in a print as proof. It answers the checkable question the register never could: *is this symptom a
  concern for the part in front of me?*

Keep it that way: an entry earns its place by being **queried**, not by cataloguing everything that
could go wrong. If an entry is never the answer to a real symptom, it is register cruft — remove it.

## Guardrails

- **Never change a slicer setting or dispatch a print.** This skill reads evidence and writes docs. The
  physical send is the owner's gate.
- **Never invent a verdict.** "Is this a concern?" with no grounding is answered "we have not observed
  this — here is what the source says, hedge intact" or "let's Ingest it once we've seen it."
- **Secrets stay secret.** A screenshot or record cited as proof must not embed the printer access code
  or any token; scrub before committing (memory *secret-check-no-stdout-leak*).
- **PR-flow.** The wiki ships branch→PR→merge like every doc here; `docs_gate` runs at commit.
