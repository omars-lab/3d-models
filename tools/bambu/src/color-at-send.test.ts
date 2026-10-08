import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { colorAtSend, plateRecipePath, recipeColor } from "./color-at-send.js";

describe("colorAtSend — the color is named at the send (call 18)", () => {
  // The by-design failure: a one-color plate, a recipe with no color, and no flag naming one.
  it("FAIL: refuses a one-color plate whose recipe names no color, and the reason names --color", () => {
    const r = colorAtSend({ used: [1], fixed: null });
    expect(r.ok).toBe(false);
    expect(r.line).toContain("--color");
  });

  it("PASS: the same plate with --color goes out in the color named", () => {
    expect(colorAtSend({ used: [1], fixed: null, color: "#FFFFFF" })).toEqual({
      ok: true,
      line: "color: #FFFFFF, named at the send (--color)",
    });
  });

  it("PASS: --ams-mapping picks the tray, so the color is picked at the send too", () => {
    expect(colorAtSend({ used: [1], fixed: null, amsMapping: "[0]" }).ok).toBe(true);
  });

  it("PASS: a two-color plate (phones-01) is matched tray by tray", () => {
    expect(colorAtSend({ used: [1, 2], fixed: ["#000000", "#F5B6CD"] }).ok).toBe(true);
  });

  it("PASS: a frozen production recipe that still fixes its one color (phones-02) goes out on it", () => {
    const r = colorAtSend({ used: [1], fixed: "#000000" });
    expect(r.ok).toBe(true);
    expect(r.line).toContain("D-095");
  });

  it("leaves a slice with no filament list to the filament match, which refuses it later", () => {
    expect(colorAtSend({ used: null, fixed: null }).ok).toBe(true);
  });
});

describe("recipeColor", () => {
  const root = mkdtempSync(join(tmpdir(), "color-at-send-"));
  mkdirSync(join(root, "docs", "design", "plates"), { recursive: true });
  const write = (name: string, text: string): string => {
    const p = plateRecipePath(name, root);
    writeFileSync(p, text);
    return p;
  };

  it("reads a fixed color, a list of colors, or none", () => {
    const profile = 'bed: x2d\nprofile:\n  settings: "s"\n  filament: "f"\n';
    expect(recipeColor(write("one", `${profile}  color: "#FFFFFF"\n`))).toBe("#FFFFFF");
    expect(recipeColor(write("two", `${profile}  color: ["#000000", "#F5B6CD"]\n`))).toEqual(["#000000", "#F5B6CD"]);
    expect(recipeColor(write("none", profile))).toBeNull();
    expect(recipeColor(plateRecipePath("missing", root))).toBeNull();
  });
});
