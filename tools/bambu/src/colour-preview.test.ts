import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { composeColourPreview, missingRegionColours, svgColours, svgRenderArgs } from "./colour-preview.js";

// A colour plate had no picture: `slice coaster` cannot slice with pictures headless, so seeing the
// regions meant opening Bambu Studio (a scratch border-coaster plate, 2026-09-26). The picture is now
// drawn from bikar's SVG, whose fills are the sidecar hexes the slot map reports.
const parts = [
  { region: "base", stl: "C-base.stl", triangles: 1, paletteName: "Slab", hex: "#333333" },
  { region: "straps", stl: "C-straps.stl", triangles: 1, paletteName: "Gold", hex: "#d4af37" },
  { region: "border", stl: "C-border.stl", triangles: 1, paletteName: "Copper", hex: "#B87333" },
];

describe("missingRegionColours", () => {
  it("passes a drawing that paints every region's slot colour (fill or stroke, any case)", () => {
    const svg = '<svg><rect fill="#FFFFFF"/><path fill="#333333"/><path stroke="#D4AF37"/><path style="stroke:#b87333"/></svg>';
    expect(missingRegionColours(svg, parts)).toEqual([]);
  });

  it("names the region a drawing leaves out", () => {
    const svg = '<svg><path fill="#333333"/><path stroke="#d4af37"/></svg>';
    expect(missingRegionColours(svg, parts)).toEqual(["border (Copper #B87333)"]);
  });

  it("does not ask the drawing for a region with no palette colour", () => {
    const untagged = [{ region: "body", stl: "b.stl", triangles: 1, paletteName: null, hex: null }];
    expect(missingRegionColours("<svg/>", untagged)).toEqual([]);
  });

  it("reads only real colours, not none or gradients", () => {
    expect([...svgColours('<path fill="none" stroke="url(#g)"/><path fill="#abc"/>')]).toEqual(["#abc"]);
  });
});

describe("svgRenderArgs", () => {
  it("draws the same recipe the parts render used", () => {
    expect(svgRenderArgs("cli.js", "/b/x.bkr", "tile", { size: 80, height: 3 }, "/s/it.svg")).toEqual([
      "cli.js", "render", "/b/x.bkr", "--format", "svg", "-o", "/s/it.svg",
      "--piece", "tile", "--param", "size=80", "--param", "height=3",
    ]);
  });

  it("leaves out --piece for the default solid", () => {
    expect(svgRenderArgs("cli.js", "/b/x.bkr", undefined, {}, "/s/it.svg")).not.toContain("--piece");
  });
});

describe("composeColourPreview", () => {
  it("lays two drawings side by side in their own colours", async () => {
    const dir = mkdtempSync(join(tmpdir(), "bambu-colour-preview-"));
    const svg = (hex: string) =>
      `<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10" fill="${hex}"/></svg>`;
    writeFileSync(join(dir, "a.svg"), svg("#d4af37"));
    writeFileSync(join(dir, "b.svg"), svg("#b87333"));
    const out = join(dir, "plate.preview.png");
    await composeColourPreview([join(dir, "a.svg"), join(dir, "b.svg")], out, 20);
    const size = execFileSync("magick", ["identify", "-format", "%wx%h", out]).toString();
    expect(size).toBe("40x20");
    const px = (x: number) => execFileSync("magick", [out, "-format", `%[hex:p{${x},10}]`, "info:"]).toString().slice(0, 6);
    expect(px(5).toLowerCase()).toBe("d4af37");
    expect(px(30).toLowerCase()).toBe("b87333");
  });
});
