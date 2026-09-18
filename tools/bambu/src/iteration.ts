// The iteration identity — `it-<sha12>`.
//
// An "iteration" is the existing (geometry, process) unit prints-tab-design.md §3 defines: a piece at
// a specific parameter set AND slice profile. This module gives that unit a stable, content-addressed
// id so a manifest item, a reprint, and a metrics view all name the SAME recipe by the SAME id — one
// source of truth, not a fork (docs/print-metadata-and-reprint-design.md §2.2, CLAUDE.md D-052).
//
// The id is `it-<sha12>` = the first 12 hex of sha256 over the CANONICAL JSON of the iteration key
//   { source, source_sha256, piece, params, slice_profile }
// "Canonical" = deterministic: object keys sorted recursively so the same recipe hashes identically
// regardless of the order fields happen to be authored in. This is the whole reason a content hash was
// chosen over a monotonic @vNN counter (PMR-1): no central allocator to collide on across sessions
// (memory decision-id-collision-recurred), and it is the repo's standing identity pattern (gate R1).
//
// This helper is deliberately the ONLY place the id is computed. The plate composer writes it into a
// record's objects[].iteration today; the reprint verb (print-metadata design) will import this same
// function, so the two can never disagree about what a given recipe's id is.

import { createHash } from "node:crypto";

/** The five fields that determine what a plate can teach and what a re-slice would reproduce.
 *  `slice_profile` is the preset DISPLAY names `slice` consumes (machine;process and filament) — not
 *  re-derivable from the nine-field process profile alone (print-metadata-and-reprint-design.md §2.1). */
export interface IterationKey {
  source: string; // "bikar:<path>@<ref>" or "bikar:<path>"
  source_sha256: string; // the bkr blob sha at the pinned ref
  piece: string; // the bikar piece rendered
  params: Record<string, unknown>; // canonicalized --param overrides
  slice_profile: {
    settings: string; // "<machine>;<process>" display names
    filament: string; // filament display name(s)
  };
}

/** Recursively sort object keys so JSON.stringify is order-independent. Arrays keep their order (an
 *  array's order is data); scalars pass through. This is the "canonical" in "canonical JSON". */
export function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    const out: Record<string, unknown> = {};
    for (const k of Object.keys(value as Record<string, unknown>).sort()) {
      out[k] = canonicalize((value as Record<string, unknown>)[k]);
    }
    return out;
  }
  return value;
}

/** The canonical JSON string of a value — deterministic key order, no incidental whitespace. */
export function canonicalJson(value: unknown): string {
  return JSON.stringify(canonicalize(value));
}

/** `it-<sha12>` for an iteration key: the first 12 hex of sha256 over its canonical JSON. */
export function iterationId(key: IterationKey): string {
  const digest = createHash("sha256").update(canonicalJson(key), "utf8").digest("hex");
  return `it-${digest.slice(0, 12)}`;
}
