// Slicer-warnings capture + classification — the honest source for the pre-dispatch gate (#52).
//
// THE FINDING (2026-09-17, measured): the BambuStudio headless CLI is silent on slicing warnings at
// its default log level, but at `--debug 2` (warning) it emits the SAME per-object advisory the GUI
// shows, as a structured line:
//
//   [warning] plate 1: found NON_CRITICAL slicing warnings: It seems object MC2Wall04.stl has
//             floating regions. Please re-orient the object or enable support generation.
//
// So we do NOT guess with a regex over arbitrary output (the old best-effort `scanSlicerWarnings`);
// we parse BambuStudio's OWN warning lines. Severity is binary, grounded in the binary's format
// strings: `plate %1%: found slicing warnings: %2%, no_check=%3%` (critical) and
// `: found NON_CRITICAL slicing warnings: ` (advisory).
//
// Plain `[warning]` boilerplate that is NOT a `found … slicing warnings:` line (the version banner,
// `no filament colors found in projects`, `can not find system preset file` on a re-slice) is NOT a
// slicing warning and must never be classified as one — only the `found … slicing warnings:` form is.

import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { repoRoot } from "../paths.js";

export type Severity = "critical" | "non_critical";

/** One slicing warning at per-object granularity: a `found …` line naming N objects yields N of these
 *  (or one with object=null when it names none), so each can be classified independently. */
export interface SlicerWarning {
  severity: Severity;
  plate: number | null;
  object: string | null;
  message: string;
  raw: string;
}

/** A manifest rule: an EXPECTED (by-design) warning we already understand and choose not to block. */
export interface WarningRule {
  /** Regex (string) matched against the warning's object name (e.g. "^MC2Wall04\\b"). Omit for object-less. */
  object?: string;
  /** Regex (string) matched against the warning message (e.g. "floating regions"). Required. */
  message: string;
  /** If set, the rule only matches this severity. */
  severity?: Severity;
  /** Why this warning is expected — shown to the operator so a by-design advisory reads as such. */
  reason: string;
  /** Optional CAL bet id this by-design failure belongs to (e.g. "CAL-FEA-01"). */
  settles?: string;
}

export interface Manifest {
  rules: WarningRule[];
}

// The `found … slicing warnings:` line. Captures an optional `plate N:` prefix, the NON_CRITICAL
// marker (absent ⇒ critical), and the message blob after the colon. A trailing `, no_check=<bool>`
// (present on the critical form) is trimmed from the message.
const FOUND_RE = /(?:plate\s+(\d+):\s+)?found\s+(NON_CRITICAL\s+)?slicing\s+warnings:\s*(.+?)(?:,\s*no_check=\S+)?\s*$/i;

/** Every object the message names, e.g. "object MC2Wall04.stl has …" → ["MC2Wall04.stl"]. Matched by
 *  the mesh-file extension so "the object or enable support" doesn't read as an object named "or" —
 *  BambuStudio names the object by its source filename in these advisories (measured). An object with
 *  no extension (renamed in Studio) is not captured, so its warning stays object-less ⇒ unexpected ⇒
 *  blocks: fail-closed, the safe direction for a dispatch gate. */
function objectsInMessage(message: string): string[] {
  const found: string[] = [];
  const re = /\bobject\s+(\S+\.(?:stl|3mf|obj|step|stp|amf))\b/gi;
  let m: RegExpExecArray | null;
  while ((m = re.exec(message)) !== null) {
    if (m[1]) found.push(m[1].replace(/[.,;:]+$/, ""));
  }
  return found;
}

/** Parse BambuStudio's own slicing-warning lines out of a slice's stdout+stderr, at per-object
 *  granularity. Only `found … slicing warnings:` lines count; all other output is ignored. */
export function parseSlicerWarnings(text: string): SlicerWarning[] {
  const out: SlicerWarning[] = [];
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    const m = line.match(FOUND_RE);
    if (!m) continue;
    const plate = m[1] ? Number(m[1]) : null;
    const severity: Severity = m[2] ? "non_critical" : "critical";
    const message = (m[3] ?? "").trim();
    const objects = objectsInMessage(message);
    if (objects.length === 0) {
      out.push({ severity, plate, object: null, message, raw: line });
    } else {
      for (const object of objects) out.push({ severity, plate, object, message, raw: line });
    }
  }
  return out;
}

/** Does a manifest rule cover this warning? Message must match; object and severity match if the
 *  rule constrains them. A rule WITHOUT an `object` only covers an object-less warning (conservative:
 *  a by-object advisory must be whitelisted per object, never blanket-cleared by a message rule). */
export function ruleCovers(rule: WarningRule, w: SlicerWarning): boolean {
  if (rule.severity && rule.severity !== w.severity) return false;
  let msgRe: RegExp;
  let objRe: RegExp | null = null;
  try {
    msgRe = new RegExp(rule.message, "i");
    if (rule.object !== undefined) objRe = new RegExp(rule.object, "i");
  } catch {
    return false; // a malformed rule covers nothing (fail closed)
  }
  if (!msgRe.test(w.message)) return false;
  if (objRe) return w.object !== null && objRe.test(w.object);
  return w.object === null;
}

export interface Classification {
  expected: Array<{ warning: SlicerWarning; rule: WarningRule }>;
  unexpected: SlicerWarning[];
}

/** Split warnings into expected (a manifest rule covers them) and unexpected (nothing does → block).
 *  Fail-closed: an empty/absent manifest classifies every warning as unexpected. */
export function classifyWarnings(warnings: SlicerWarning[], manifest: Manifest): Classification {
  const expected: Classification["expected"] = [];
  const unexpected: SlicerWarning[] = [];
  for (const w of warnings) {
    const rule = manifest.rules.find((r) => ruleCovers(r, w));
    if (rule) expected.push({ warning: w, rule });
    else unexpected.push(w);
  }
  return { expected, unexpected };
}

/** Default manifest location: <repo root>/.claude/gates/expected-slicer-warnings.json. */
export function defaultManifestPath(): string | null {
  const root = repoRoot();
  return root ? join(root, ".claude", "gates", "expected-slicer-warnings.json") : null;
}

/** Load the manifest, or an empty one (fail-closed) if the path is missing/unreadable/malformed. */
export function loadManifest(path: string | null = defaultManifestPath()): Manifest {
  if (!path || !existsSync(path)) return { rules: [] };
  try {
    const j = JSON.parse(readFileSync(path, "utf8")) as Partial<Manifest>;
    return { rules: Array.isArray(j.rules) ? j.rules : [] };
  } catch {
    return { rules: [] };
  }
}

/** The sidecar path a sliced .3mf carries its captured warnings in, alongside the artifact. */
export function sidecarPath(threemfPath: string): string {
  return `${threemfPath}.warnings.json`;
}

export interface WarningsSidecar {
  tool: string;
  sliced_at: string;
  studio_version: string | null;
  /** SHA-256 of the exact .3mf bytes these warnings were captured for. Lets the dispatch gate refuse
   *  a STALE sidecar (one sitting beside a .3mf it was not sliced from) — not only a missing one.
   *  Optional for backward-compat: a legacy sidecar without it cannot be proven fresh ⇒ unverifiable. */
  source_sha256?: string;
  warnings: SlicerWarning[];
}

/** SHA-256 of a file's bytes, or null if it is missing/unreadable. Content-based, so the freshness
 *  verdict survives worktrees, checkouts and mtime noise that an mtime dependency would trip on. */
export function hashFile(path: string): string | null {
  try {
    return createHash("sha256").update(readFileSync(path)).digest("hex");
  } catch {
    return null;
  }
}

/** Read a sidecar; null if absent/unreadable (the caller decides whether absence blocks). */
export function readSidecar(threemfPath: string): WarningsSidecar | null {
  const p = sidecarPath(threemfPath);
  if (!existsSync(p)) return null;
  try {
    const j = JSON.parse(readFileSync(p, "utf8")) as WarningsSidecar;
    if (!Array.isArray(j.warnings)) return null;
    return j;
  } catch {
    return null;
  }
}

/** Whether a sidecar corresponds to the .3mf on disk right now:
 *   - "missing"      → no sidecar beside the plate;
 *   - "unverifiable" → sidecar present but pre-dates source_sha256 (legacy) or the .3mf is unreadable;
 *   - "stale"        → sidecar's source_sha256 does not match the current .3mf bytes;
 *   - "fresh"        → hashes match — the warnings describe THIS plate.
 *  A dispatch gate treats everything but "fresh" as fail-closed. */
export type Freshness = "missing" | "unverifiable" | "stale" | "fresh";

export function sidecarFreshness(threemfPath: string): { sidecar: WarningsSidecar | null; status: Freshness } {
  const sidecar = readSidecar(threemfPath);
  if (!sidecar) return { sidecar: null, status: "missing" };
  if (!sidecar.source_sha256) return { sidecar, status: "unverifiable" };
  const actual = hashFile(threemfPath);
  if (!actual) return { sidecar, status: "unverifiable" };
  return { sidecar, status: actual === sidecar.source_sha256 ? "fresh" : "stale" };
}

/** The BambuStudio version banner it prints on every slice — kept for the sidecar's provenance. */
export function studioVersionFrom(text: string): string | null {
  const m = text.match(/Current BambuStudio Version\s+([\d.]+)/i);
  return m?.[1] ?? null;
}
