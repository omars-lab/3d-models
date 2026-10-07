import { describe, expect, it } from "vitest";
import { buildOptionCommand, fun2Bit, optionByKey, parseOnOff, PRINT_OPTIONS, readBack, renderOptions, setRefusal, xcamCfg } from "./print-options.js";

// An X2D's report as the community sample in the research shows it (cfg 8089015, fun2 "B7B77"): every
// AI check on at medium, alignment, foreign objects and displacement on, and the printer saying it has
// all three of those. Decoded by hand in docs/research/2026-10-07-third-party-plates.md.
const X2D = { gcode_state: "IDLE", fun2: "B7B77", xcam: { cfg: 8089015, buildplate_marker_detector: true } };

const read = (frame: unknown) => Object.fromEntries(PRINT_OPTIONS.map((o) => [o.key, o.read(frame as never)]));

describe("reading the switches", () => {
  it("decodes the X2D sample: all on, the AI checks at medium", () => {
    expect(read(X2D)).toEqual({
      "foreign-object": true,
      "plate-type": true,
      "plate-alignment": true,
      displacement: true,
      spaghetti: true,
      pileup: true,
      clumping: true,
      "air-printing": true,
    });
    expect(optionByKey("spaghetti").level!(X2D)).toBe("medium");
    for (const o of PRINT_OPTIONS) expect(o.supported(X2D)).toBe(true);
  });

  it("reads each cfg bit on its own, so one switch off shows only that one off", () => {
    const fodOff = { ...X2D, xcam: { ...X2D.xcam, cfg: 8089015 - 2 ** 21 } };
    const r = read(fodOff);
    expect(r["foreign-object"]).toBe(false);
    expect(r["plate-alignment"]).toBe(true);
    expect(r.displacement).toBe(true);
    const typeOff = { ...X2D, xcam: { ...X2D.xcam, buildplate_marker_detector: false } };
    expect(read(typeOff)["plate-type"]).toBe(false);
    expect(read(typeOff)["foreign-object"]).toBe(true);
  });

  it("says not reported, not off, when the printer leaves the field out", () => {
    expect(read({ gcode_state: "IDLE" })).toEqual(Object.fromEntries(PRINT_OPTIONS.map((o) => [o.key, null])));
    expect(xcamCfg({ xcam: { cfg: "not a number" } })).toBeNull();
    expect(fun2Bit({}, 13)).toBeNull();
  });

  it("takes cfg as a string too, and reads fun2 from its last hex digit", () => {
    expect(xcamCfg({ xcam: { cfg: "8089015" } })).toBe(8089015n);
    expect(fun2Bit({ fun2: "4" }, 2)).toBe(true);
    expect(fun2Bit({ fun2: "4" }, 1)).toBe(false);
    // a printer without foreign-object detection: bit 13 clear
    expect(fun2Bit({ fun2: "B5B77" }, 13)).toBe(false);
  });

  it("shows a check the printer lacks as not on this printer", () => {
    const table = renderOptions({ ...X2D, fun2: "B5B77" });
    expect(table).toMatch(/foreign-object\s+not on this printer/);
    expect(renderOptions(X2D)).toMatch(/spaghetti\s+on \(medium\)/);
  });
});

describe("the switch command", () => {
  it("is Studio's xcam_control_set, with the value in control and enable", () => {
    expect(buildOptionCommand(optionByKey("foreign-object"), false, null, "20001")).toEqual({
      xcam: { command: "xcam_control_set", sequence_id: "20001", module_name: "fod_check", control: false, enable: false, print_halt: true },
    });
    expect(buildOptionCommand(optionByKey("plate-type"), true, null, "20002").xcam.module_name).toBe("buildplate_marker_detector");
  });

  it("carries an AI check's level, and only an AI check's", () => {
    expect(buildOptionCommand(optionByKey("spaghetti"), true, "medium", "1").xcam.halt_print_sensitivity).toBe("medium");
    expect(buildOptionCommand(optionByKey("displacement"), true, "medium", "1").xcam).not.toHaveProperty("halt_print_sensitivity");
  });

  it("refuses mid-print and on a printer without the check", () => {
    expect(setRefusal(optionByKey("foreign-object"), false, { ...X2D, gcode_state: "RUNNING" })).toMatch(/RUNNING/);
    expect(setRefusal(optionByKey("foreign-object"), false, { ...X2D, gcode_state: "PREPARE" })).toMatch(/PREPARE/);
    expect(setRefusal(optionByKey("foreign-object"), false, { ...X2D, fun2: "B5B77" })).toMatch(/no Foreign Object/);
    expect(setRefusal(optionByKey("foreign-object"), false, X2D)).toBeNull();
    expect(setRefusal(optionByKey("foreign-object"), false, { ...X2D, gcode_state: "PAUSE" })).toBeNull();
  });

  it("reads the switch back: ✓ as asked, ✗ unchanged, ? not reported", () => {
    const fod = optionByKey("foreign-object");
    expect(readBack(fod, false, { xcam: { cfg: 8089015 - 2 ** 21 } }).mark).toBe("✓");
    expect(readBack(fod, false, X2D).mark).toBe("✗");
    expect(readBack(fod, false, {}).mark).toBe("?");
  });

  it("takes only known names and on or off", () => {
    expect(() => optionByKey("fod")).toThrow(/unknown option/);
    expect(parseOnOff("OFF")).toBe(false);
    expect(() => parseOnOff("disable")).toThrow(/not on or off/);
  });
});
