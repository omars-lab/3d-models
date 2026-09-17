// Print-record scaffolding.
//
// A finished record lives at docs/prints/<date>-<slug>/index.md and must satisfy the prints gate
// (.claude/gates/prints_gate.py — the authority; see docs/prints-tab-design.md §7). That gate is
// WHOLE-TREE: an incomplete draft under docs/prints/ would block every commit in the repo. So a
// `--record` scaffold is written to the gitignored .bambu/records/ staging area instead, where it
// can be filled in (readings, photos, the real self_ref) and gate-checked with
// `bambu validate record .bambu/records` before a human moves the finished dir into docs/prints/.
//
// The scaffold pins provenance we CAN know at dispatch time — the bikar HEAD and each object's blob
// sha at that ref — and marks everything a machine cannot know yet with TODO, so the gate's findings
// read as a precise to-do list rather than a wall of missing keys.

import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { basename, join } from "node:path";
import { bikarHead, bikarBlobSha } from "./backends/bikar.js";
import { recordsDir } from "./paths.js";
import { ev } from "./log.js";
import type { RecordProfile } from "./header.js";

const TODO = "TODO";
/** A 64-hex placeholder the gate will flag as "not the blob" until a real print is recorded. */
const TODO_SHA = "0".repeat(64);

export interface ScaffoldObject {
  entry: string; // e.g. "MC-2" — the machine-card rung / plate-object id
  source: string; // "bikar:<path>" — bikar source path
}

export interface ScaffoldOpts {
  slug: string; // <slug> in the run name; date is prepended
  plateName: string; // human-readable plate label
  plateFile: string; // the sliced .3mf that was (or would be) dispatched
  objects: ScaffoldObject[]; // one per printed object; source must be bikar:<path>
  date?: string; // YYYY-MM-DD, defaults to today (local)
  baseDir?: string; // defaults to <cwd>/.bambu/records
  profile?: RecordProfile; // machine-known header fields (from `bambu header`), pre-filling the block
}

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

function yamlList(objs: Array<Record<string, string>>): string {
  // Minimal, stable YAML for the object/photo lists — deterministic key order, always quoted.
  return objs
    .map((o) =>
      Object.entries(o)
        .map(([k, v], i) => `${i === 0 ? "  - " : "    "}${k}: ${JSON.stringify(v)}`)
        .join("\n"),
    )
    .join("\n");
}

/**
 * Write a draft record dir under .bambu/records/ and return its path. Resolves the bikar HEAD and
 * each object's blob sha so R1's provenance is pinned to a real commit; leaves human-supplied fields
 * (readings, photos, self_ref, ambient, instrument) as TODO for the operator to complete.
 */
export async function scaffoldRecord(opts: ScaffoldOpts): Promise<string> {
  const date = opts.date ?? today();
  const run = `${date}-${opts.slug}`;
  const baseDir = opts.baseDir ?? recordsDir();
  const rec = join(baseDir, run);
  if (existsSync(rec)) throw new Error(`record already exists: ${rec}`);
  mkdirSync(join(rec, "photos"), { recursive: true });

  const bikarRef = (await bikarHead()) ?? TODO;
  const objectBlocks: Array<Record<string, string>> = [];
  for (const o of opts.objects) {
    const path = o.source.startsWith("bikar:") ? o.source.slice("bikar:".length) : o.source;
    const sha = bikarRef !== TODO ? await bikarBlobSha(bikarRef, path) : null;
    objectBlocks.push({
      entry: o.entry,
      source: `bikar:${path}`,
      source_sha256: sha ?? TODO_SHA,
    });
  }

  // The SAME header builder that `bambu header` prints pre-fills these where the machine + .3mf
  // actually answered; a field the builder could not fill honestly stays TODO for the operator
  // (D-052: one code path, not a fork — the header logic lives in header.ts, consumed here and there).
  const p = opts.profile ?? {};
  const pf = (v: string | undefined): string => (v && v.trim() ? v : TODO);
  const fm = [
    "---",
    `run: ${run}`,
    `plate: ${JSON.stringify(opts.plateName)}`,
    "status: draft", // draft | measured | … (operator sets the real state)
    `outcome: ${TODO}`, // what the plate answered — readings | scrapped | …
    "profile:",
    `  machine: ${pf(p.machine)}`,
    `  material: ${pf(p.material)}`,
    `  spool: ${pf(p.spool)}`,
    `  nozzle_mm: ${pf(p.nozzle_mm)}`,
    `  nozzle_type: ${pf(p.nozzle_type)}`,
    `  layer_mm: ${pf(p.layer_mm)}`,
    `  slicer_profile: ${JSON.stringify(p.slicer_profile ?? basename(opts.plateFile))}`,
    `  ambient_c: ${TODO}`, // manual — the printer cannot know room temp (chamber ≠ room)
    `  instrument: ${TODO}`, // manual — the operator's caliper
    "pins:",
    `  bikar_ref: ${bikarRef}`,
    `  self_ref: ${TODO}`,
    "objects:",
    yamlList(objectBlocks),
    "photos: []",
    "readings: []",
    "---",
    "",
    `Draft record scaffolded by \`bambu print send --record\` for **${opts.plateName}**.`,
    "",
    "Before moving this dir into `docs/prints/`, fill every `TODO`, add the plate photos under",
    "`photos/` (and list them with their sha256), record the measurements under `readings`, and",
    "check it with `bambu validate record .bambu/records`. The prints gate is the authority.",
    "",
  ].join("\n");

  writeFileSync(join(rec, "index.md"), fm);
  ev("record_scaffold", { run, dir: rec, objects: opts.objects.length });
  return rec;
}
