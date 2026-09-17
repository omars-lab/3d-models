// `bambu print list` — enumerate every print record, newest first.
//
// "Can we list all the things it's printed?" A record is a plate that came off a machine, and it
// lives in one of two places: the SHIPPED tree `docs/prints/<run>/` (checked in, gate-verified) and
// the DRAFT staging `.bambu/records/<run>/` (gitignored, written by `print send --record`, not yet
// promoted). This verb reads both so a plate you sent five minutes ago and a plate that shipped last
// month both show up, each tagged with where it lives.
//
// It parses NOTHING itself. Frontmatter is read by exactly one authority — `prints_gate.py`, the same
// parser that gates the record — via its read-only `--list` projection (robustness-over-ease: one code
// path, never two that can disagree). Today the honest answer is empty: nothing has ever been printed.

import { existsSync } from "node:fs";
import { join } from "node:path";
import { runWithTimeout, ev } from "../log.js";
import { repoRoot, recordsDir } from "../paths.js";

const PYTHON = process.env.PYTHON ?? "python3";

interface ListOpts {
  json?: boolean;
  shipped?: boolean; // only docs/prints/
  drafts?: boolean; // only .bambu/records/
  how?: boolean; // show the process-identity columns instead of the outcome columns
  // filters — narrow the *parseable* set; a broken record is always surfaced regardless (below)
  settles?: string; // a CAL id substring, e.g. CAL-FIT or CAL-FIT-01
  material?: string; // filament substring, e.g. PLA
  machine?: string; // machine substring, e.g. X2D
  status?: string; // exact lifecycle status, e.g. measured
}

// The "how" — the process-identity subset the gate projects from the record's profile, so the list can
// answer not just what came off the plate but the numbers to reprint it (prints-tab-design.md §4.1).
interface How {
  machine?: string | null;
  material?: string | null;
  nozzle_mm?: number | null;
  layer_mm?: number | null;
  slicer_profile?: string | null;
}

// One record as the gate projects it; `error` is set instead when the record does not parse (a broken
// record is surfaced, never dropped — for the operator "it's broken" is different news from "no record").
interface Rec {
  run: string;
  date?: string | null;
  plate?: string | null;
  status?: string | null;
  outcome?: string | null;
  objects?: number;
  readings?: number;
  settles?: string[];
  how?: How;
  error?: string;
  source?: "shipped" | "draft"; // added here, not by the gate
}

/**
 * Narrow to the records matching every active filter. A broken record (no parsed fields) can never be
 * *asserted* to match a positive filter, but hiding it is the one failure mode this verb exists to avoid
 * — so broken records always pass through. Pure function: no I/O, so it is the testable core of the query.
 */
export function applyFilters(recs: Rec[], f: Pick<ListOpts, "settles" | "material" | "machine" | "status">): Rec[] {
  const has = (hay: string | null | undefined, needle: string) =>
    (hay ?? "").toLowerCase().includes(needle.toLowerCase());
  return recs.filter((r) => {
    if (r.error) return true; // surfaced regardless — a broken record must never hide behind a filter
    if (f.settles && !(r.settles ?? []).some((s) => has(s, f.settles!))) return false;
    if (f.material && !has(r.how?.material, f.material)) return false;
    if (f.machine && !has(r.how?.machine, f.machine)) return false;
    if (f.status && (r.status ?? "").toLowerCase() !== f.status.toLowerCase()) return false;
    return true;
  });
}

/** Shell the gate's `--list` projection over one dir. A missing dir is an empty list, not an error. */
async function listDir(gate: string, dir: string, source: "shipped" | "draft"): Promise<Rec[]> {
  if (!existsSync(dir)) return [];
  const res = await runWithTimeout(PYTHON, [gate, "--list", dir], { timeoutMs: 60_000, label: "prints_list" });
  if (res.code !== 0) {
    if (res.stderr.trim()) console.error(res.stderr.trim());
    throw new Error(`prints_gate --list exited ${res.code ?? "null"} for ${dir}`);
  }
  const parsed = JSON.parse(res.stdout) as { records: Rec[] };
  return parsed.records.map((r) => ({ ...r, source }));
}

function pad(s: string, w: number): string {
  return s.length >= w ? s : s + " ".repeat(w - s.length);
}

/** A fixed-width table, newest first. Broken records get their own line so they cannot hide. */
function renderTable(recs: Rec[]): string {
  const rows = recs.map((r) => ({
    date: r.date ?? r.run.slice(0, 10),
    plate: r.error ? `⚠ ${r.run} — unparseable: ${r.error}` : String(r.plate ?? r.run),
    status: r.error ? "broken" : String(r.status ?? "?"),
    obj: r.error ? "" : String(r.objects ?? 0),
    read: r.error ? "" : String(r.readings ?? 0),
    settles: r.error ? "" : (r.settles ?? []).join(",") || "—",
    source: r.source ?? "",
  }));
  const w = {
    date: Math.max(4, ...rows.map((r) => r.date.length)),
    plate: Math.max(5, ...rows.map((r) => r.plate.length)),
    status: Math.max(6, ...rows.map((r) => r.status.length)),
    settles: Math.max(7, ...rows.map((r) => r.settles.length)),
    source: Math.max(6, ...rows.map((r) => r.source.length)),
  };
  const header = `${pad("DATE", w.date)}  ${pad("PLATE", w.plate)}  ${pad("STATUS", w.status)}  OBJ  RD  ${pad("SETTLES", w.settles)}  ${pad("SOURCE", w.source)}`;
  const lines = rows.map(
    (r) =>
      `${pad(r.date, w.date)}  ${pad(r.plate, w.plate)}  ${pad(r.status, w.status)}  ${pad(r.obj, 3)}  ${pad(r.read, 2)}  ${pad(r.settles, w.settles)}  ${pad(r.source, w.source)}`,
  );
  return [header, ...lines].join("\n");
}

/** The "how" view — the process identity, so the operator reprints from a number, not a memory. */
function renderHowTable(recs: Rec[]): string {
  const rows = recs.map((r) => ({
    date: r.date ?? r.run.slice(0, 10),
    plate: r.error ? `⚠ ${r.run} — unparseable: ${r.error}` : String(r.plate ?? r.run),
    machine: r.error ? "" : String(r.how?.machine ?? "—"),
    material: r.error ? "" : String(r.how?.material ?? "—"),
    nozzle: r.error ? "" : r.how?.nozzle_mm != null ? `${r.how.nozzle_mm}` : "—",
    layer: r.error ? "" : r.how?.layer_mm != null ? `${r.how.layer_mm}` : "—",
    profile: r.error ? "" : String(r.how?.slicer_profile ?? "—"),
    source: r.source ?? "",
  }));
  const w = {
    date: Math.max(4, ...rows.map((r) => r.date.length)),
    plate: Math.max(5, ...rows.map((r) => r.plate.length)),
    machine: Math.max(7, ...rows.map((r) => r.machine.length)),
    material: Math.max(8, ...rows.map((r) => r.material.length)),
    profile: Math.max(7, ...rows.map((r) => r.profile.length)),
    source: Math.max(6, ...rows.map((r) => r.source.length)),
  };
  const header = `${pad("DATE", w.date)}  ${pad("PLATE", w.plate)}  ${pad("MACHINE", w.machine)}  ${pad("MATERIAL", w.material)}  NOZ   LYR   ${pad("PROFILE", w.profile)}  ${pad("SOURCE", w.source)}`;
  const lines = rows.map(
    (r) =>
      `${pad(r.date, w.date)}  ${pad(r.plate, w.plate)}  ${pad(r.machine, w.machine)}  ${pad(r.material, w.material)}  ${pad(r.nozzle, 4)}  ${pad(r.layer, 4)}  ${pad(r.profile, w.profile)}  ${pad(r.source, w.source)}`,
  );
  return [header, ...lines].join("\n");
}

export async function runPrintList(opts: ListOpts): Promise<void> {
  const root = repoRoot();
  if (!root) {
    console.error("could not find the repo root (.claude/gates). Run from inside the 3d-models repo.");
    process.exitCode = 1;
    return;
  }
  const gate = join(root, ".claude", "gates", "prints_gate.py");
  const wantShipped = Boolean(!opts.drafts || opts.shipped);
  const wantDrafts = Boolean(!opts.shipped || opts.drafts);
  ev("print_list_start", { shipped: wantShipped, drafts: wantDrafts });
  let recs: Rec[] = [];
  try {
    if (wantShipped) recs = recs.concat(await listDir(gate, join(root, "docs", "prints"), "shipped"));
    if (wantDrafts) recs = recs.concat(await listDir(gate, recordsDir(), "draft"));
  } catch (err) {
    console.error(`list failed: ${(err as Error).message}`);
    process.exitCode = 1;
    return;
  }
  // Newest first: run names begin with YYYY-MM-DD, so a reverse string sort is chronological.
  recs.sort((a, b) => (a.run < b.run ? 1 : a.run > b.run ? -1 : 0));
  const total = recs.length;
  recs = applyFilters(recs, opts);
  const filtered = Boolean(opts.settles || opts.material || opts.machine || opts.status);
  ev("print_list_done", { count: recs.length, total, filtered });

  if (opts.json) {
    console.log(JSON.stringify({ records: recs }, null, 2));
    return;
  }
  if (recs.length === 0) {
    if (filtered && total > 0) {
      // The list is non-empty but nothing matched — say so, and how many were skipped, so the operator
      // knows this is "no match" (a real answer), not "nothing printed" (the zero-record baseline).
      console.log(`0 of ${total} record(s) match this filter.`);
      return;
    }
    // The honest baseline — the same truth the prints gate prints at zero records.
    console.log("0 print records — nothing printed yet.");
    console.log("A record is written by `bambu print send --record` (draft) and promoted to docs/prints/ once it ships.");
    return;
  }
  console.log(opts.how ? renderHowTable(recs) : renderTable(recs));
  const broken = recs.filter((r) => r.error).length;
  const of = filtered ? ` of ${total}` : "";
  console.log(`\n${recs.length}${of} record(s)${broken ? `, ${broken} unparseable` : ""}.`);
}
