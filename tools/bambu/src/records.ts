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
import type { RecordActuals } from "./actuals.js";

const TODO = "TODO";
/** A 64-hex placeholder the gate will flag as "not the blob" until a real print is recorded. */
const TODO_SHA = "0".repeat(64);

export interface ScaffoldObject {
  entry: string; // e.g. "MC-2" — the machine-card rung / plate-object id
  source: string; // "bikar:<path>" — bikar source path (any @ref is stripped; the ref lives in pins)
  piece?: string; // the bikar piece rendered (optional; the plate composer always sets it)
  params?: Record<string, unknown>; // the --param overrides this object was rendered at
  count?: number; // R8 multiplicity — copies of this object on the plate (omitted ⇒ 1)
  iteration?: string; // it-<sha12> — the iteration identity (src/iteration.ts); the plate↔iteration map
}

/** Post-print ground truth captured off the printer's MQTT device report (actuals.ts). Present only
 *  for a `bambu print capture` scaffold — a `--record` dispatch draft is written before the print runs,
 *  so it has no actuals yet. The verbatim `rawFrame` is persisted beside index.md so a field the
 *  builder left unconfirmed (filament grams) stays recoverable and settles with no code change. */
export interface CaptureData {
  actuals: RecordActuals; // the filled fields, projected by actualsToRecord
  capturedAt: string; // when the frame was cached (or the clock, if it carried no timestamp)
  rawFrame: unknown; // the whole report frame, written to device-report.json
}

export interface ScaffoldOpts {
  slug: string; // <slug> in the run name; date is prepended
  plateName: string; // human-readable plate label
  plateFile: string; // the sliced .3mf that was (or would be) dispatched
  objects: ScaffoldObject[]; // one per printed object; source must be bikar:<path>
  date?: string; // YYYY-MM-DD, defaults to today (local)
  baseDir?: string; // defaults to <cwd>/.bambu/records
  profile?: RecordProfile; // machine-known header fields (from `bambu header`), pre-filling the block
  capture?: CaptureData; // present for `print capture`: the actuals block + raw frame
  via?: string; // the verb that scaffolded it, for the closing note (default: send --record)
}

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

/** Emit the objects[] list, typing each value: strings quoted, `count` a bare int, `params` inline
 *  JSON (a valid YAML flow mapping). A generic all-quoted emitter would write `count: "2"`, which the
 *  prints gate rejects (R8 needs a real int) — so objects get their own emitter. Keys are emitted in a
 *  fixed, stable order; optional keys are skipped when absent. */
function yamlObjects(objs: Array<Record<string, unknown>>): string {
  const ORDER = ["entry", "source", "source_sha256", "piece", "params", "count", "iteration"];
  const emit = (v: unknown): string => {
    if (typeof v === "number") return String(v);
    if (v && typeof v === "object") return JSON.stringify(v); // params → inline flow mapping (valid YAML)
    return JSON.stringify(v); // strings quoted
  };
  return objs
    .map((o) =>
      ORDER.filter((k) => o[k] !== undefined)
        .map((k, i) => `${i === 0 ? "  - " : "    "}${k}: ${emit(o[k])}`)
        .join("\n"),
    )
    .join("\n");
}

/** Emit the `actuals:` block from a capture. Only genuinely-filled fields are present in `actuals`
 *  (actualsToRecord drops unconfirmed/absent ones), so this writes exactly what the machine answered
 *  plus the provenance pointers — `source` (this came off MQTT, not a slice) and `raw` (the verbatim
 *  frame beside index.md, so an unconfirmed field like filament grams is still recoverable). The
 *  prints gate does not read this block (it is additive; measure a rule before gating it), so its only
 *  job is to be honest, well-formed YAML. */
function yamlActuals(cap: CaptureData): string {
  const ORDER: (keyof RecordActuals)[] = [
    "state", "progress_pct", "layer", "remaining_min", "job", "error", "nozzle_c", "bed_c", "chamber_c", "filament_g",
  ];
  const lines = [
    "actuals:",
    "  source: mqtt-device-report", // where these came from — never a slice-time estimate
    "  raw: device-report.json", // the verbatim frame, for fields the builder left unconfirmed
    `  captured_at: ${JSON.stringify(cap.capturedAt)}`,
  ];
  for (const k of ORDER) {
    const v = cap.actuals[k];
    if (v !== undefined) lines.push(`  ${k}: ${JSON.stringify(v)}`);
  }
  return lines.join("\n");
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
  const objectBlocks: Array<Record<string, unknown>> = [];
  for (const o of opts.objects) {
    // A source may arrive as `bikar:<path>` or `bikar:<path>@<ref>` — the ref lives in pins.bikar_ref,
    // so strip it before both the blob lookup and the recorded source (R1 resolves path @ that pin).
    const raw = o.source.startsWith("bikar:") ? o.source.slice("bikar:".length) : o.source;
    const path = raw.split("@")[0] ?? raw;
    const sha = bikarRef !== TODO ? await bikarBlobSha(bikarRef, path) : null;
    objectBlocks.push({
      entry: o.entry,
      source: `bikar:${path}`,
      source_sha256: sha ?? TODO_SHA,
      piece: o.piece,
      params: o.params,
      count: o.count,
      iteration: o.iteration,
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
    yamlObjects(objectBlocks),
    "photos: []",
    "readings: []",
    ...(opts.capture ? [yamlActuals(opts.capture)] : []),
    "---",
    "",
    `Draft record scaffolded by \`${opts.via ?? "bambu print send --record"}\` for **${opts.plateName}**.`,
    ...(opts.capture
      ? [
          "",
          "The `actuals:` block is the printer's own MQTT device report — what the print actually did;",
          "the verbatim frame is in `device-report.json` beside this file (a field the builder could not",
          "confirm on the X2D, e.g. filament grams, is recoverable there).",
        ]
      : []),
    "",
    "Before moving this dir into `docs/prints/`, fill every `TODO`, add the plate photos under",
    "`photos/` (and list them with their sha256), record the measurements under `readings`, and",
    "check it with `bambu validate record .bambu/records`. The prints gate is the authority.",
    "",
  ].join("\n");

  writeFileSync(join(rec, "index.md"), fm);
  if (opts.capture) {
    writeFileSync(join(rec, "device-report.json"), JSON.stringify(opts.capture.rawFrame, null, 2) + "\n");
  }
  ev("record_scaffold", { run, dir: rec, objects: opts.objects.length, capture: Boolean(opts.capture) });
  return rec;
}
