// The post-print ACTUALS builder — what the machine actually did, read from its MQTT device report.
//
// This is the completion of the record loop the design named (docs/print-metadata-and-reprint-design.md
// §3.3.1, PMR-4): the `profile` block says what a plate was printed *under*; `actuals` says what the
// print *did* — state, progress, layers, temperatures. It exists so a print started from the Studio
// GUI (which `print send --record` never sees) can still become a counted record: `bambu print capture`
// reads the device report and scaffolds a draft carrying this block (the #71 metadata gap).
//
// Like buildHeader (header.ts), this is PURE: it takes an already-read report frame and returns a
// structured result — no MQTT, no clock beyond an injectable `now` — so it is unit-testable against a
// fixture. And it obeys the SAME honesty rule (the design's Validator): a field is filled ONLY from a
// frame key that actually carried it; a key not present prints `absent`, never a fabricated value.
//
// Confidence: the state/progress/layer/temperature keys below are the ones `status show`
// (commands/status.ts) already reads live off the X2D — proven on 20P6AJ641401412 at bring-up (memory:
// bambu-x2d-bringup), so they are `filled` when present. Filament-consumed (grams/length) is NOT among
// them and is NOT confirmed on the X2D report; it is marked `unconfirmed` and left to the RAW frame the
// capture verb persists beside the record, so the first real print (#63) settles the field name with no
// code change — the same [X2D-UNCONFIRMED]-then-confirm discipline the dispatch payload uses (mqtt.ts).

import type { PrinterStatus } from "./backends/mqtt.js";
import { pick } from "./frame.js";

/** How an actuals field got its value. A subset of header.ts FieldState — no slice-side `todo-plate`. */
export type ActualState =
  | "filled" // read from a frame key that actually carried it
  | "unconfirmed" // an RE-corpus key not observed on the X2D report — never fabricate
  | "absent"; // the frame carried no such key on this read

export interface ActualField {
  value: string | null; // the machine-read value, or null when not present
  state: ActualState;
  source: string; // the frame key it came from, or why it is null
}

export interface Actuals {
  state: ActualField; // gcode_state — RUNNING / PAUSE / FINISH / FAILED / IDLE
  progress_pct: ActualField; // mc_percent — 0..100
  layer: ActualField; // layer_num / total_layer_num — "N / M"
  remaining_min: ActualField; // mc_remaining_time — minutes the printer still predicts
  job: ActualField; // subtask_name — the job the printer is running
  error: ActualField; // print_error — 0 (none) or a fault code
  nozzle_c: ActualField; // nozzle_temper
  bed_c: ActualField; // bed_temper
  chamber_c: ActualField; // chamber_temper
  filament_g: ActualField; // [X2D-UNCONFIRMED] consumed grams — not observed on the X2D report
  captured_at: ActualField; // when the frame we read was cached (_cached_at), else the clock
}

const filled = (value: string, source: string): ActualField => ({ value, state: "filled", source });
const absent = (source: string): ActualField => ({ value: null, state: "absent", source });
const unconfirmed = (source: string): ActualField => ({ value: null, state: "unconfirmed", source });

/** A frame scalar as a trimmed string, or null when the key is missing/blank. */
function scalar(frame: PrinterStatus, ...keys: string[]): string | null {
  const raw = pick(frame, ...keys);
  if (raw == null) return null;
  const s = String(raw).trim();
  return s ? s : null;
}

/** Build the actuals block from a pushall report frame (pure; unit-tested against a fixture). */
export function buildActuals(frame: PrinterStatus, now: Date = new Date()): Actuals {
  const state = scalar(frame, "gcode_state", "mc_print_stage");
  const pct = scalar(frame, "mc_percent");
  const layerNum = scalar(frame, "layer_num");
  const totalLayer = scalar(frame, "total_layer_num");
  const remain = scalar(frame, "mc_remaining_time");
  const job = scalar(frame, "subtask_name");
  const err = scalar(frame, "print_error");
  const nozzle = scalar(frame, "nozzle_temper");
  const bed = scalar(frame, "bed_temper");
  const chamber = scalar(frame, "chamber_temper");
  // Filament consumed is an RE-corpus field (pybambu/bambulabs_api name it variously) NOT observed on
  // the X2D report — never invent it; the raw frame the capture verb persists settles it later.
  const filamentG = scalar(frame, "filament_used_g", "print_gram", "total_gram");

  const layer =
    layerNum != null
      ? filled(totalLayer != null ? `${layerNum} / ${totalLayer}` : layerNum, "frame layer_num / total_layer_num")
      : absent("frame layer_num (no key on this read)");

  const cachedAt =
    typeof frame._cached_at === "string" && frame._cached_at
      ? filled(frame._cached_at, "frame _cached_at (when the report was cached)")
      : filled(now.toISOString(), "clock (UTC) — frame carried no _cached_at");

  return {
    state: state != null ? filled(state, "frame gcode_state") : absent("frame gcode_state (no key on this read)"),
    progress_pct: pct != null ? filled(pct, "frame mc_percent") : absent("frame mc_percent (no key)"),
    layer,
    remaining_min: remain != null ? filled(remain, "frame mc_remaining_time") : absent("frame mc_remaining_time (no key)"),
    job: job != null ? filled(job, "frame subtask_name") : absent("frame subtask_name (no key)"),
    error: err != null ? filled(err, "frame print_error") : absent("frame print_error (no key)"),
    nozzle_c: nozzle != null ? filled(nozzle, "frame nozzle_temper") : absent("frame nozzle_temper (no key)"),
    bed_c: bed != null ? filled(bed, "frame bed_temper") : absent("frame bed_temper (no key)"),
    chamber_c: chamber != null ? filled(chamber, "frame chamber_temper") : absent("frame chamber_temper (no key)"),
    filament_g:
      filamentG != null
        ? { value: filamentG, state: "unconfirmed", source: "frame filament_used_g (H2-proxy; not confirmed on X2D)" }
        : unconfirmed("frame filament-consumed key not observed on the X2D report (see the raw frame)"),
    captured_at: cachedAt,
  };
}

/** True when the frame carried no recognizable print-state key at all — a capture worth warning about. */
export function actualsAreEmpty(a: Actuals): boolean {
  return (
    a.state.state !== "filled" &&
    a.progress_pct.state !== "filled" &&
    a.layer.state !== "filled" &&
    a.job.state !== "filled"
  );
}

/** The record's `actuals:` frontmatter block (records.ts) — filled fields carry their value; a field
 *  the frame did not answer is emitted as an honest marker, never a fabricated number. `raw` points at
 *  the verbatim device report the capture verb writes beside index.md so an unconfirmed field is still
 *  recoverable. Keys are emitted in a fixed order; the emitter lives in records.ts (one YAML writer). */
export interface RecordActuals {
  state?: string;
  progress_pct?: string;
  layer?: string;
  remaining_min?: string;
  job?: string;
  error?: string;
  nozzle_c?: string;
  bed_c?: string;
  chamber_c?: string;
  filament_g?: string;
}

/** Map a built Actuals onto the record's actuals keys — only genuinely-filled fields carry a value;
 *  unconfirmed/absent fields are omitted (the raw frame keeps them recoverable). */
export function actualsToRecord(a: Actuals): RecordActuals {
  const val = (f: ActualField): string | undefined => (f.state === "filled" && f.value ? f.value : undefined);
  return {
    state: val(a.state),
    progress_pct: val(a.progress_pct),
    layer: val(a.layer),
    remaining_min: val(a.remaining_min),
    job: val(a.job),
    error: val(a.error),
    nozzle_c: val(a.nozzle_c),
    bed_c: val(a.bed_c),
    chamber_c: val(a.chamber_c),
    filament_g: val(a.filament_g), // always undefined today (unconfirmed) — present when the X2D confirms it
  };
}
