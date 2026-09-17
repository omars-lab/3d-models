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
  error?: string;
  source?: "shipped" | "draft"; // added here, not by the gate
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
  ev("print_list_done", { count: recs.length });

  if (opts.json) {
    console.log(JSON.stringify({ records: recs }, null, 2));
    return;
  }
  if (recs.length === 0) {
    // The honest baseline — the same truth the prints gate prints at zero records.
    console.log("0 print records — nothing printed yet.");
    console.log("A record is written by `bambu print send --record` (draft) and promoted to docs/prints/ once it ships.");
    return;
  }
  console.log(renderTable(recs));
  const broken = recs.filter((r) => r.error).length;
  console.log(`\n${recs.length} record(s)${broken ? `, ${broken} unparseable` : ""}.`);
}
