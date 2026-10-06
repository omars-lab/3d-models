import { describe, expect, it } from "vitest";
import type { PlateColor } from "../by-color.js";
import { plateColor } from "./plates.js";

// `--color Name=<value>` and `--frame-color <value>`: a hex slices as PLA Basic, a spool code as
// that spool's own line, so a Silk spool is not sliced at Basic's heat and speed.

const SILK: PlateColor = { key: "PLA Silk|13903", hex: "#0047bb", line: "PLA Silk", code: "13903", name: "Neon City", note: null };
const spool = (code: string) => {
  if (code !== "13903") throw new Error(`${code}: no spool with this code`);
  return SILK;
};

describe("plateColor — a hex or a spool code", () => {
  it("takes a five-digit code as that spool, with its own line", () => {
    expect(plateColor("13903", "--color Kite=13903", spool)).toBe(SILK);
  });

  it("takes a hex, with or without #, as PLA Basic", () => {
    expect(plateColor("0047BB", "--frame-color", spool)).toMatchObject({ hex: "#0047bb", line: "PLA Basic", code: null });
  });

  it("refuses anything else, and passes on the catalog's refusal", () => {
    expect(() => plateColor("blue", "--color Kite=blue", spool)).toThrow("--color Kite=blue: expected #rrggbb or a five-digit spool code");
    expect(() => plateColor("99999", "--color Kite=99999", spool)).toThrow("no spool with this code");
  });
});
