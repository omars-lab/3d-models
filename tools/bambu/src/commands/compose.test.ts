import { describe, expect, it } from "vitest";
import {
  parseManifest,
  bedFitPrecheck,
  resolveBed,
  findIterationGeometry,
  type PartFootprint,
} from "./compose.js";

describe("parseManifest — validate before anything renders", () => {
  it("accepts a bkr item with numeric params and a count", () => {
    const m = parseManifest(
      [
        "bed: x2d",
        "profile:",
        "  settings: X2D;0.20 Std",
        "  filament: PLA Basic",
        "items:",
        "  - bkr: bikar:patterns/Orbs/foo.bkr",
        "    piece: Orb",
        "    params:",
        "      size: 40",
        "    count: 2",
      ].join("\n"),
    );
    expect(m.bed).toBe("x2d");
    expect(m.items).toHaveLength(1);
  });

  it("accepts a bare iteration item", () => {
    const m = parseManifest(["items:", "  - iteration: it-0123456789ab"].join("\n"));
    expect(m.items[0]).toMatchObject({ iteration: "it-0123456789ab" });
  });

  it("rejects a manifest with no items", () => {
    expect(() => parseManifest("bed: x2d\n")).toThrow(/no `items:`/);
  });

  it("accepts a bkr item with no piece (renders the file's default last solid)", () => {
    const m = parseManifest("items:\n  - bkr: bikar:patterns/Orbs/Star-Orb.bkr");
    expect(m.items[0]).toMatchObject({ bkr: "bikar:patterns/Orbs/Star-Orb.bkr" });
    expect((m.items[0] as { piece?: string }).piece).toBeUndefined();
  });

  it("rejects an empty-string piece (a typo, not an intent to render the default solid)", () => {
    expect(() => parseManifest('items:\n  - bkr: bikar:foo.bkr\n    piece: ""')).toThrow(/non-empty string/);
  });

  it("rejects a non-bikar source", () => {
    expect(() => parseManifest("items:\n  - bkr: foo.bkr\n    piece: Orb")).toThrow(/bikar:<path>/);
  });

  it("rejects a non-numeric param (bikar --param takes numbers)", () => {
    const text = ["items:", "  - bkr: bikar:foo.bkr", "    piece: Orb", "    params:", '      size: "big"'].join("\n");
    expect(() => parseManifest(text)).toThrow(/must be a number/);
  });

  it("rejects count < 1", () => {
    const text = ["items:", "  - bkr: bikar:foo.bkr", "    piece: Orb", "    count: 0"].join("\n");
    expect(() => parseManifest(text)).toThrow(/integer >= 1/);
  });

  it("rejects an item that carries both iteration and bkr", () => {
    const text = ["items:", "  - iteration: it-abc", "    bkr: bikar:foo.bkr"].join("\n");
    expect(() => parseManifest(text)).toThrow(/cannot also carry bkr/);
  });
});

describe("bedFitPrecheck — the per-part check is the load-bearing one (K6/D2)", () => {
  const bed = resolveBed("x2d"); // 256×256

  it("passes when every part fits and the aggregate area is under the bed", () => {
    const parts: PartFootprint[] = [
      { entry: "A", x: 40, y: 40, count: 2 },
      { entry: "B", x: 30, y: 30, count: 1 },
    ];
    expect(bedFitPrecheck(parts, bed).ok).toBe(true);
  });

  it("FAILS on one oversized part even when the plate is otherwise near-empty (hard case)", () => {
    // Aggregate area is tiny, so an aggregate-only check would pass — the per-part check must catch it.
    const parts: PartFootprint[] = [
      { entry: "big", x: 300, y: 20, count: 1 }, // 300 mm > 256 mm bed edge
      { entry: "small", x: 5, y: 5, count: 1 },
    ];
    const res = bedFitPrecheck(parts, bed);
    expect(res.ok).toBe(false);
    expect(res.failures.join("\n")).toMatch(/big: footprint 300\.0×20\.0 mm does not fit/);
  });

  it("FAILS when aggregate area exceeds the bed even though each part fits", () => {
    const parts: PartFootprint[] = [{ entry: "tile", x: 200, y: 200, count: 2 }]; // each fits; 2× area > bed
    const res = bedFitPrecheck(parts, bed);
    expect(res.ok).toBe(false);
    expect(res.failures.join("\n")).toMatch(/total footprint area/);
  });
});

describe("resolveBed", () => {
  it("is case-insensitive and knows x2d", () => {
    expect(resolveBed("X2D").x).toBe(256);
  });
  it("throws on an unknown bed, naming the known ones", () => {
    expect(() => resolveBed("bogus")).toThrow(/unknown --bed/);
  });
});

describe("findIterationGeometry — reprint-by-id lookup", () => {
  const record = (iteration: string) =>
    [
      "---",
      "run: 2026-09-18-plate",
      "objects:",
      "  - entry: MC-1",
      "    source: bikar:patterns/Orbs/foo.bkr",
      "    piece: Orb",
      "    params: {size: 40}",
      `    iteration: ${iteration}`,
      "---",
      "body",
    ].join("\n");

  it("finds the geometry recorded under a matching iteration id", () => {
    const geom = findIterationGeometry("it-known", ["/rec/2026-09-18-plate"], () => record("it-known"));
    expect(geom).toMatchObject({ sourcePath: "patterns/Orbs/foo.bkr", piece: "Orb", params: { size: 40 } });
  });

  it("returns null when no record carries the id", () => {
    expect(findIterationGeometry("it-missing", ["/rec/x"], () => record("it-other"))).toBeNull();
  });
});
