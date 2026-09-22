import { describe, expect, it } from "vitest";
import {
  colourDistance,
  logicalSlotsFromPlate,
  physicalTraysFromSlots,
  reconcile,
  renderReport,
  rgb,
  MATCH_TOLERANCE,
  type PhysicalTray,
} from "./filament-sync.js";
import type { Slot } from "./frame.js";

const tray = (where: string, hex: string | null, type: string | null, remain: number | null = null): PhysicalTray => ({
  where,
  hex,
  type,
  remain,
});

describe("rgb / colourDistance", () => {
  it("parses #RRGGBB, #RGB, #RRGGBBAA and bare RRGGBBAA to the same triple", () => {
    expect(rgb("#FF0000")).toEqual([255, 0, 0]);
    expect(rgb("#f00")).toEqual([255, 0, 0]);
    expect(rgb("#FF0000FF")).toEqual([255, 0, 0]); // alpha dropped
    expect(rgb("00FF00CC")).toEqual([0, 255, 0]); // no leading # + alpha
    expect(rgb("garbage")).toBeNull();
    expect(rgb(null)).toBeNull();
  });

  it("is 0 for identical colours and symmetric", () => {
    expect(colourDistance("#123456", "#123456")).toBe(0);
    expect(colourDistance("#000000", "#ffffff")).toBeCloseTo(441.67, 1);
    expect(colourDistance("#ff0000", "#00ff00")).toBe(colourDistance("#00ff00", "#ff0000"));
  });

  it("returns Infinity when either colour is unparseable, so it never wins a match", () => {
    expect(colourDistance("#ff0000", null)).toBe(Infinity);
    expect(colourDistance("nope", "#ff0000")).toBe(Infinity);
  });
});

describe("physicalTraysFromSlots", () => {
  it("drops empty trays and normalises colour to #RRGGBB", () => {
    const slots: Slot[] = [
      { where: "AMS 0 · slot 1", tray: { tray_type: "PLA", tray_color: "FF0000FF", remain: 80 } },
      { where: "AMS 0 · slot 2", tray: { tray_type: "", tray_color: "" } }, // empty → dropped
      { where: "External spool", tray: { tray_type: "PETG", tray_color: "0000FFFF", remain: -1 } },
    ];
    const trays = physicalTraysFromSlots(slots);
    expect(trays).toEqual([
      { where: "AMS 0 · slot 1", hex: "#FF0000", type: "PLA", remain: 80 },
      { where: "External spool", hex: "#0000FF", type: "PETG", remain: -1 },
    ]);
  });
});

describe("logicalSlotsFromPlate", () => {
  it("numbers slots 1-based, skips colourless slots, pads missing types with ''", () => {
    const logical = logicalSlotsFromPlate(["#FF0000", "not-a-colour", "#00FF00"], ["PLA"]);
    expect(logical).toEqual([
      { slot: 1, hex: "#FF0000", type: "PLA" },
      { slot: 3, hex: "#00FF00", type: "" }, // slot 2 skipped; type padded blank
    ]);
  });
});

describe("reconcile — the clean case", () => {
  it("binds each colour to its closest tray, each tray once, and reports ok", () => {
    const logical = logicalSlotsFromPlate(["#FF0000", "#0000FF"], ["PLA", "PLA"]);
    const trays = [tray("AMS 0 · slot 1", "#0000EE", "PLA", 90), tray("AMS 0 · slot 2", "#EE0000", "PLA", 90)];
    const r = reconcile(logical, trays);
    expect(r.ok).toBe(true);
    expect(r.needsOperator).toBe(false);
    expect(r.bindings[0]!.tray?.where).toBe("AMS 0 · slot 2"); // red → the red tray, not slot 1
    expect(r.bindings[1]!.tray?.where).toBe("AMS 0 · slot 1");
    expect(r.bindings.every((b) => b.status === "matched")).toBe(true);
  });
});

describe("reconcile — the hard cases", () => {
  it("flags a missing colour when no tray is within tolerance", () => {
    const logical = logicalSlotsFromPlate(["#00FF00"], ["PLA"]);
    const r = reconcile(logical, [tray("AMS 0 · slot 1", "#FF0000", "PLA")]); // only red loaded
    expect(r.bindings[0]!.status).toBe("missing");
    expect(r.bindings[0]!.tray).toBeNull();
    expect(r.needsOperator).toBe(true);
    expect(r.ok).toBe(false);
  });

  it("flags a material mismatch when the colour matches but the type differs", () => {
    const logical = logicalSlotsFromPlate(["#FF0000"], ["PLA"]);
    const r = reconcile(logical, [tray("AMS 0 · slot 1", "#FF0000", "PETG", 90)]);
    expect(r.bindings[0]!.status).toBe("material-mismatch");
    expect(r.bindings[0]!.tray?.type).toBe("PETG");
    expect(r.needsOperator).toBe(true);
  });

  it("flags an ambiguous near-tie when two loaded trays are ~equally close", () => {
    // Two greys straddling the target within AMBIGUITY_MARGIN of each other.
    const logical = logicalSlotsFromPlate(["#808080"], ["PLA"]);
    const r = reconcile(logical, [
      tray("AMS 0 · slot 1", "#7A7A7A", "PLA", 90),
      tray("AMS 0 · slot 2", "#868686", "PLA", 90),
    ]);
    expect(r.bindings[0]!.status).toBe("ambiguous");
    expect(r.bindings[0]!.runnerUp).not.toBeNull();
    expect(r.needsOperator).toBe(true);
  });

  it("warns (does not block) on a low-remain tray", () => {
    const logical = logicalSlotsFromPlate(["#FF0000"], ["PLA"]);
    const r = reconcile(logical, [tray("AMS 0 · slot 1", "#FF0000", "PLA", 5)]);
    expect(r.bindings[0]!.status).toBe("low-remain");
    expect(r.needsOperator).toBe(false); // a warning, not a stop
    expect(r.ok).toBe(true);
  });

  it("does not warn on the -1 'unknown remain' sentinel", () => {
    const logical = logicalSlotsFromPlate(["#FF0000"], ["PLA"]);
    const r = reconcile(logical, [tray("AMS 0 · slot 1", "#FF0000", "PLA", -1)]);
    expect(r.bindings[0]!.status).toBe("matched");
  });

  it("never binds one tray to two slots — the second same-colour slot goes missing", () => {
    const logical = logicalSlotsFromPlate(["#FF0000", "#FF0000"], ["PLA", "PLA"]);
    const r = reconcile(logical, [tray("AMS 0 · slot 1", "#FF0000", "PLA", 90)]); // only one red tray
    expect(r.bindings[0]!.status).toBe("matched");
    expect(r.bindings[1]!.status).toBe("missing"); // the tray was already used
  });

  it("is deterministic under a distance tie (breaks by slot then tray index)", () => {
    const logical = logicalSlotsFromPlate(["#FF0000", "#FF0000"], ["PLA", "PLA"]);
    const trays = [tray("t-a", "#FF0000", "PLA", 90), tray("t-b", "#FF0000", "PLA", 90)];
    const a = reconcile(logical, trays);
    const b = reconcile(logical, trays);
    expect(a.bindings.map((x) => x.tray?.where)).toEqual(b.bindings.map((x) => x.tray?.where));
    expect(a.bindings[0]!.tray?.where).toBe("t-a"); // first slot takes first tray
    expect(a.bindings[1]!.tray?.where).toBe("t-b");
  });

  it("reports 'nothing to reconcile' when the plate has no coloured slots", () => {
    const r = reconcile([], [tray("AMS 0 · slot 1", "#FF0000", "PLA")]);
    expect(r.ok).toBe(false);
    expect(r.needsOperator).toBe(false);
    expect(renderReport(r)).toMatch(/no coloured filament slots/);
  });
});

describe("renderReport", () => {
  it("shows the measured distance on every matched line and a clear verdict", () => {
    const logical = logicalSlotsFromPlate(["#FF0000"], ["PLA"]);
    const out = renderReport(reconcile(logical, [tray("AMS 0 · slot 1", "#EE0000", "PLA", 90)]));
    expect(out).toMatch(/slot 1 #FF0000 PLA → AMS 0 · slot 1/);
    expect(out).toMatch(/Δ\d/); // distance always printed
    expect(out).toMatch(/safe to print/);
  });

  it("names the tolerance on a missing line", () => {
    const logical = logicalSlotsFromPlate(["#00FF00"], ["PLA"]);
    const out = renderReport(reconcile(logical, [tray("AMS 0 · slot 1", "#FF0000", "PLA")]));
    expect(out).toContain(`load this colour`);
    expect(out).toContain(`Δ${MATCH_TOLERANCE}`);
  });
});
