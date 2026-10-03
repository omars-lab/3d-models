// The nozzles a slice was made for, against the ones on the printer.
//
// A slice is made for a nozzle size: line widths, flow and the first layer all follow from it, and
// the printer does not refuse a file made for another size. Bambu Studio compares them before it
// sends; our send did not. The X2D reports its two nozzles in the status frame as
// `device.nozzle.info[].diameter` (0.4 and 0.4, type HS01, read 2026-10-03), and the slice carries
// `nozzle_diameter` in its project settings (threemf.ts).
//
// Which slice entry belongs to which nozzle id is not settled by any source we hold, so the two are
// compared as sets of sizes, sorted. That catches a 0.6 slice on 0.4 nozzles; it would miss a slice
// whose two sizes are swapped between the nozzles, a case that cannot arise while both are 0.4.
// PURE: both sides are passed in.

import type { PrinterStatus } from "./backends/mqtt.js";

export interface NozzleCheck {
  ok: boolean; // false: refuse the send
  mark: "✓" | "⚠" | "✗";
  line: string; // without the mark
}

/** The printer's nozzle sizes in mm, from `device.nozzle.info[]`, then the top-level `nozzle_diameter`. */
export function printerNozzles(frame: PrinterStatus | null): number[] {
  const device = frame?.device as Record<string, unknown> | undefined;
  const nozzle = device?.nozzle as Record<string, unknown> | undefined;
  const info = nozzle?.info;
  if (Array.isArray(info)) {
    const sizes = info
      .map((n) => Number((n as Record<string, unknown>)?.diameter))
      .filter((d) => Number.isFinite(d) && d > 0);
    if (sizes.length) return sizes;
  }
  const top = (frame as Record<string, unknown> | null)?.nozzle_diameter;
  const flat = (Array.isArray(top) ? top : top != null ? [top] : []).map(Number).filter((d) => Number.isFinite(d) && d > 0);
  return flat;
}

const fmt = (xs: number[]): string => xs.map((x) => x.toFixed(1)).join(", ");
const sorted = (xs: number[]): number[] => [...xs].sort((a, b) => a - b);

/** May a slice made for `slice` nozzle sizes go to a printer reporting `printer`? */
export function checkNozzles(slice: string[], printer: number[]): NozzleCheck {
  const want = slice.map(Number).filter((d) => Number.isFinite(d) && d > 0);
  if (!want.length) {
    return { ok: false, mark: "✗", line: "nozzle: the slice names no nozzle size. Slice it again" };
  }
  if (!printer.length) {
    return { ok: true, mark: "⚠", line: `nozzle: slice for ${fmt(want)} mm; the printer did not report its nozzles. Check them at the printer` };
  }
  const a = sorted(want);
  const b = sorted(printer);
  const same = a.length === b.length && a.every((x, i) => Math.abs(x - b[i]!) < 1e-6);
  if (!same) {
    return {
      ok: false,
      mark: "✗",
      line: `nozzle: the slice is for ${fmt(want)} mm and the printer has ${fmt(printer)} mm. Slice it again for the nozzles fitted`,
    };
  }
  return { ok: true, mark: "✓", line: `nozzle: ${fmt(printer)} mm, as the slice was made for` };
}
