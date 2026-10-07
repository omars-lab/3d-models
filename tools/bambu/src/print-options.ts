// The printer's own print options: the checks the X2D runs before and during a print, switched on the
// printer, not in the slice (Settings > Print Options on the screen, Device > Print Options in Studio).
//
// Added 2026-10-07 for the glacier plate. Bambu's X2D page says third-party plates give false
// foreign-object alarms, and the X2D cannot read the glacier's marker, so a print on it needs Foreign
// Object Detection and Type Detection off, and on again for the gold plate
// (docs/research/2026-10-07-third-party-plates.md). Omar asked for a command that changes them
// ("yes command that changes settings").
//
// Everything here is Bambu Studio's own, read from its source at da8b44e: the command is
// `DevPrintOptions::command_xcam_control`, the state bits are the `xcam.cfg` parse in
// `DevPrintOptions.cpp`, and which checks a printer has is the `fun2` parse (`get_flag_bits_no_border`,
// bit 0 the lowest bit of the last hex digit). It is untested on Omar's printer until the first
// `options show` reads it. PURE: the frame comes in, the lines and the payload go out.

import { startSequenceId } from "./backends/mqtt.js";

type Frame = Record<string, unknown> | null | undefined;

export interface PrintOption {
  key: string; // the CLI's name for it
  label: string; // Studio's label, so the screen and the CLI say the same thing
  module: string; // the `module_name` Studio sends for it
  /** On, off, or null when the printer does not report it. */
  read(frame: Frame): boolean | null;
  /** Whether the printer has the check: true, false, or null when it does not say. */
  supported(frame: Frame): boolean | null;
  /** The AI checks carry a level (low, medium, high), sent back unchanged when switched. */
  level?: (frame: Frame) => string | null;
  /** What the research says to do with it on a non-Bambu plate, for `show`. */
  nonBambu: "off" | "on";
}

function xcam(frame: Frame): Record<string, unknown> | undefined {
  const x = frame?.xcam;
  return x && typeof x === "object" ? (x as Record<string, unknown>) : undefined;
}

/** `xcam.cfg`, an integer in base 10 (the X2D sample: 8089015), or null. */
export function xcamCfg(frame: Frame): bigint | null {
  const raw = xcam(frame)?.cfg;
  if (typeof raw === "number" && Number.isInteger(raw) && raw >= 0) return BigInt(raw);
  if (typeof raw === "string" && /^\d+$/.test(raw.trim())) return BigInt(raw.trim());
  return null;
}

function bits(value: bigint, start: number, count = 1): number {
  return Number((value >> BigInt(start)) & ((1n << BigInt(count)) - 1n));
}

/** Studio's `get_flag_bits_no_border` on `fun2`: a hex string, bit 0 the lowest of its last digit. */
export function fun2Bit(frame: Frame, bit: number): boolean | null {
  const raw = frame?.fun2;
  if (typeof raw !== "string") return null;
  const hex = raw.trim().replace(/^0x/i, "").replace(/[^0-9a-f]/gi, "");
  if (!hex) return null;
  return bits(BigInt(`0x${hex}`), bit) === 1;
}

const cfgBit = (bit: number) => (frame: Frame) => {
  const cfg = xcamCfg(frame);
  return cfg === null ? null : bits(cfg, bit) === 1;
};

const LEVELS = ["low", "medium", "high"];
const cfgLevel = (bit: number) => (frame: Frame) => {
  const cfg = xcamCfg(frame);
  return cfg === null ? null : (LEVELS[bits(cfg, bit, 2)] ?? null);
};

/** Studio sets the AI checks as supported whenever `xcam.cfg` is there. */
const hasCfg = (frame: Frame) => (xcamCfg(frame) === null ? null : true);

export const PRINT_OPTIONS: readonly PrintOption[] = [
  {
    key: "foreign-object",
    label: "Foreign Object Detection",
    module: "fod_check",
    read: cfgBit(21),
    supported: (f) => fun2Bit(f, 13),
    nonBambu: "off",
  },
  {
    key: "plate-type",
    label: "Build Plate Detection > Type Detection",
    module: "buildplate_marker_detector",
    read: (f) => {
      const v = xcam(f)?.buildplate_marker_detector;
      return typeof v === "boolean" ? v : null;
    },
    supported: (f) => (xcam(f) ? "buildplate_marker_detector" in xcam(f)! : null),
    nonBambu: "off",
  },
  {
    key: "plate-alignment",
    label: "Build Plate Detection > Alignment Detection",
    module: "plate_offset_switch",
    read: cfgBit(20),
    supported: (f) => fun2Bit(f, 2),
    nonBambu: "on",
  },
  {
    key: "displacement",
    label: "Printed Part Displacement Detection",
    module: "model_movement_check",
    read: cfgBit(22),
    supported: (f) => fun2Bit(f, 14),
    nonBambu: "on",
  },
  { key: "spaghetti", label: "AI: Spaghetti Detection", module: "spaghetti_detector", read: cfgBit(7), level: cfgLevel(8), supported: hasCfg, nonBambu: "on" },
  { key: "pileup", label: "AI: Purge Chute Pile-Up Detection", module: "pileup_detector", read: cfgBit(10), level: cfgLevel(11), supported: hasCfg, nonBambu: "on" },
  { key: "clumping", label: "AI: Nozzle Clumping Detection", module: "clump_detector", read: cfgBit(13), level: cfgLevel(14), supported: hasCfg, nonBambu: "on" },
  { key: "air-printing", label: "AI: Air Printing Detection", module: "airprint_detector", read: cfgBit(16), level: cfgLevel(17), supported: hasCfg, nonBambu: "on" },
];

export function optionByKey(key: string): PrintOption {
  const hit = PRINT_OPTIONS.find((o) => o.key === key.trim().toLowerCase());
  if (!hit) throw new Error(`unknown option "${key}". Use one of: ${PRINT_OPTIONS.map((o) => o.key).join(", ")}.`);
  return hit;
}

export function parseOnOff(word: string): boolean {
  const w = word.trim().toLowerCase();
  if (w === "on") return true;
  if (w === "off") return false;
  throw new Error(`"${word}" is not on or off.`);
}

const onOff = (v: boolean | null) => (v === null ? "not reported" : v ? "on" : "off");

/** The `show` table: each option, on or off, its level, and what a non-Bambu plate wants. */
export function renderOptions(frame: Frame): string {
  const rows = PRINT_OPTIONS.map((o) => {
    const supported = o.supported(frame);
    const state = supported === false ? "not on this printer" : onOff(o.read(frame));
    const level = o.level && o.read(frame) ? o.level(frame) : null;
    return `${o.key.padEnd(16)}${(state + (level ? ` (${level})` : "")).padEnd(22)}${o.nonBambu.padEnd(18)}${o.label}`;
  });
  return [
    `${"option".padEnd(16)}${"now".padEnd(22)}${"non-Bambu plate".padEnd(18)}Studio's name`,
    ...rows,
    "",
    "First Layer Inspection is not offered on the X2D. Idle Heating Protection and Filament Tangle are",
    "not read here. Both switches a non-Bambu plate needs are printer-wide: switch them back on for a Bambu plate.",
  ].join("\n");
}

/**
 * The switch command, as Studio sends it: `control` carries the value, `enable` and `print_halt` are
 * its "old protocol" fields, and an AI check carries its level so switching it keeps the level.
 */
export function buildOptionCommand(option: PrintOption, on: boolean, level: string | null = null, sequenceId = startSequenceId()): { xcam: Record<string, unknown> } {
  const cmd: Record<string, unknown> = {
    command: "xcam_control_set",
    sequence_id: sequenceId,
    module_name: option.module,
    control: on,
    enable: on,
    print_halt: true,
  };
  if (option.level && level) cmd.halt_print_sensitivity = level;
  return { xcam: cmd };
}

/**
 * The two switches that follow the plate on the bed (D-108): on for Bambu's own plates, off for a
 * non-Bambu one, whose surface sets off Foreign Object Detection (806E) and whose marker the X2D cannot
 * read (8062). The bed verdict says which plate the photo shows; nothing else decides it.
 */
export const PLATE_SWITCHES = ["foreign-object", "plate-type"] as const;

/** Said when a verdict predates `--bambu-plate`/`--non-bambu`; the plate name follows it. */
export const PLATE_KIND_UNSAID =
  "the bed verdict does not say whether the plate is Bambu's own, so the two checks cannot be set from it. Look at a new photo and write the verdict with --bambu-plate or --non-bambu: bambu bed verdict";

export interface PlateSwitchChange {
  option: PrintOption;
  on: boolean;
}

/** The switches to flip so they fit the plate, in PLATE_SWITCHES order; empty when they already fit. */
export function plateSwitchChanges(frame: Frame, nonBambu: boolean): PlateSwitchChange[] {
  return PLATE_SWITCHES.map((k) => optionByKey(k))
    .filter((o) => o.supported(frame) !== false && o.read(frame) !== !nonBambu)
    .map((option) => ({ option, on: !nonBambu }));
}

/**
 * The send's `options:` line. ✗ when a switch is wrong for the plate the verdict saw: on with a
 * non-Bambu plate the print stops before layer 0 (sld-1, 2026-10-07); off with a Bambu plate nothing
 * checks for a print left on the bed. ✗ too when the verdict does not say which kind of plate it saw
 * (`nonBambu` undefined): both plates read P0101, so the look is the only source. ⚠ when the printer
 * does not report a switch.
 */
export function plateSwitchCheck(frame: Frame, nonBambu: boolean | undefined, plate: string): { ok: boolean; mark: "✓" | "✗" | "⚠"; line: string } {
  if (nonBambu === undefined) return { ok: false, mark: "✗", line: `options: ${PLATE_KIND_UNSAID} ${plate}` };
  const which = nonBambu ? "a non-Bambu plate" : "a Bambu plate";
  const want = nonBambu ? "off" : "on";
  const options = PLATE_SWITCHES.map((k) => optionByKey(k)).filter((o) => o.supported(frame) !== false);
  const unknown = options.filter((o) => o.read(frame) === null);
  const wrong = plateSwitchChanges(frame, nonBambu).filter((c) => c.option.read(frame) !== null);
  if (wrong.length) {
    return { ok: false, mark: "✗", line: `options: ${wrong.map((c) => c.option.key).join(" and ")} ${wrong.length > 1 ? "are" : "is"} ${nonBambu ? "on" : "off"}; the bed verdict saw ${which}, which needs ${want}. Run: bambu options for-bed ${plate} --yes` };
  }
  if (unknown.length) return { ok: true, mark: "⚠", line: `options: the printer does not report ${unknown.map((o) => o.key).join(" or ")}; ${which} needs ${want}, so check the screen` };
  return { ok: true, mark: "✓", line: `options: ${options.map((o) => o.key).join(" and ")} ${want}, as ${which} needs` };
}

/** States a switch may be changed in: not mid-job. A paused print counts as stopped, so an alarm can be answered. */
const BUSY = new Set(["RUNNING", "PREPARE", "SLICING"]);

/** Why this switch should not be sent now, or null. PURE. */
export function setRefusal(option: PrintOption, on: boolean, frame: Frame): string | null {
  const state = typeof frame?.gcode_state === "string" ? frame.gcode_state : null;
  if (state && BUSY.has(state.toUpperCase())) return `the printer is ${state}; change a print option between prints`;
  if (option.supported(frame) === false) return `this printer has no ${option.label}`;
  return null;
}

/** After the send: did the printer take it? ✓ it reads back as asked, ✗ it does not, ? not reported. */
export function readBack(option: PrintOption, on: boolean, frame: Frame): { mark: "✓" | "✗" | "?"; line: string } {
  const now = option.read(frame);
  if (now === null) return { mark: "?", line: `${option.key}: sent; the printer does not report it, so check the screen` };
  if (now === on) return { mark: "✓", line: `${option.key}: ${onOff(now)}, read back from the printer` };
  return { mark: "✗", line: `${option.key}: asked for ${onOff(on)}, the printer still reports ${onOff(now)}` };
}
