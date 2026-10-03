import { describe, expect, it } from "vitest";
import type { PrinterStatus } from "./backends/mqtt.js";
import { checkNozzles, printerNozzles } from "./nozzle-check.js";

// The nozzle check a send runs (nozzle-check.ts). The frame shape is the X2D's own, read
// 2026-10-03: two nozzles under device.nozzle.info, 0.4 mm each, type HS01.

const X2D = {
  nozzle_diameter: "0.4",
  device: {
    nozzle: {
      exist: 3,
      info: [
        { id: 0, diameter: 0.4, type: "HS01" },
        { id: 1, diameter: 0.4, type: "HS01" },
      ],
    },
  },
} as unknown as PrinterStatus;

describe("printerNozzles", () => {
  it("reads both nozzles off the X2D frame", () => {
    expect(printerNozzles(X2D)).toEqual([0.4, 0.4]);
  });

  it("falls back to the top-level nozzle_diameter", () => {
    expect(printerNozzles({ nozzle_diameter: "0.6" } as unknown as PrinterStatus)).toEqual([0.6]);
  });

  it("reports none for no frame", () => {
    expect(printerNozzles(null)).toEqual([]);
  });
});

describe("checkNozzles", () => {
  it("passes the sheets-04b slice (0.4, 0.4) on the X2D", () => {
    const c = checkNozzles(["0.4", "0.4"], printerNozzles(X2D));
    expect(c).toMatchObject({ ok: true, mark: "✓" });
  });

  it("refuses a 0.6 slice on 0.4 nozzles", () => {
    const c = checkNozzles(["0.6", "0.6"], printerNozzles(X2D));
    expect(c).toMatchObject({ ok: false, mark: "✗" });
    expect(c.line).toContain("the slice is for 0.6, 0.6 mm and the printer has 0.4, 0.4 mm");
  });

  it("refuses a slice for one nozzle size when one of two differs", () => {
    expect(checkNozzles(["0.4", "0.6"], [0.4, 0.4]).ok).toBe(false);
  });

  it("compares as sets: the same two sizes in either order pass", () => {
    expect(checkNozzles(["0.6", "0.4"], [0.4, 0.6]).ok).toBe(true);
  });

  it("refuses a slice that names no nozzle", () => {
    expect(checkNozzles([], [0.4, 0.4])).toMatchObject({ ok: false, mark: "✗" });
  });

  it("warns, not refuses, when the printer reports no nozzles", () => {
    expect(checkNozzles(["0.4", "0.4"], [])).toMatchObject({ ok: true, mark: "⚠" });
  });
});
