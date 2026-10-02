// Tests for the bed map: which plate item each arranged object is, and where it sits.
//
// The fixture is real: test/fixtures/sheets-04/ holds `3D/3dmodel.model` and
// `Metadata/model_settings.config` of docs/plates/sheets-04.yaml as `bambu slice compose` sliced it
// on 2026-10-01 (Bambu Studio 02.08.02.61). Four of its six objects are the same ring of hexagons
// at four gaps, which is why the map exists: on the bed they cannot be told apart by eye.

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parsePlacements } from "./threemf.js";
import { bedMap, bedMapPathFor, parseManifest, type ResolvedItem } from "./commands/compose.js";

const fixture = (name: string) =>
  readFileSync(join(dirname(fileURLToPath(import.meta.url)), "..", "test", "fixtures", "sheets-04", name), "utf8");
const model = fixture("3dmodel.model");
const settings = fixture("model_settings.config");

function item(entry: string, iteration: string, label: string, piece: string, params: Record<string, number>, count = 1): ResolvedItem {
  const sourcePath = "patterns/Coupons/Loose-Fit-Coupon.bkr";
  return { entry, sourcePath, sourceAtRef: `bikar:${sourcePath}@x`, piece, params, window: "", count, sourceSha256: "s", iteration, label };
}

const sheets04: ResolvedItem[] = [
  item("c1", "it-b034a32d6453", "FRAME", "Frame", {}),
  item("c2", "it-cd96e639aad9", "GAP 05", "Hex", { gap: 0.05 }),
  item("c3", "it-a9d89945f18a", "GAP 10", "Hex", { gap: 0.1 }),
  item("c4", "it-adecc6965fc7", "GAP 15", "Hex", { gap: 0.15 }),
  item("c5", "it-5d426d2c0825", "GAP 20", "Hex", { gap: 0.2 }),
  item("c6", "it-467183d1c5cb", "STAR 15", "Star", { star_gap: 0.15 }),
];

describe("parsePlacements", () => {
  it("reads all six objects of the real sheets-04 slice with their names and centres", () => {
    const p = parsePlacements(model, settings);
    expect(p).toHaveLength(6);
    const gap05 = p.find((o) => o.name === "it-cd96e639aad9.stl");
    expect(gap05?.objectId).toBe("6");
    expect(gap05?.x).toBeCloseTo(117.22, 2);
    expect(gap05?.y).toBeCloseTo(203.77, 2);
  });

  it("reads the turn arrange gave an object, and 0 for one it left alone", () => {
    const p = parsePlacements(model, settings);
    expect(p.find((o) => o.objectId === "2")?.turnDeg).toBe(0);
    // object 12: m00 0.9877, m01 -0.1564 — turned 9° clockwise
    expect(p.find((o) => o.objectId === "12")?.turnDeg).toBeCloseTo(-9, 0);
  });

  it("keeps an object with no name in the settings as an empty name", () => {
    const p = parsePlacements(model, "<config/>");
    expect(p).toHaveLength(6);
    expect(p.every((o) => o.name === "")).toBe(true);
  });

  it("returns nothing for a model with no build", () => {
    expect(parsePlacements("<model/>", settings)).toEqual([]);
  });
});

describe("bedMap — tell look-alike sets apart on the bed", () => {
  it("names each of the four hexagon rings by its label and position", () => {
    const rows = bedMap(parsePlacements(model, settings), sheets04);
    expect(rows.map((r) => r.label)).toEqual(["FRAME", "GAP 05", "GAP 10", "GAP 15", "GAP 20", "STAR 15"]);
    const gap10 = rows.find((r) => r.label === "GAP 10");
    expect(gap10).toMatchObject({ entry: "c3", piece: "Hex", params: { gap: 0.1 }, x: 67.2, y: 203.8 });
  });

  it("falls back to the entry when an item has no label", () => {
    const unlabeled = sheets04.map((r) => ({ ...r, label: "" }));
    expect(bedMap(parsePlacements(model, settings), unlabeled)[1]?.label).toBe("c2");
  });

  it("hands copies of one recipe to the items in manifest order", () => {
    const placements = [
      { objectId: "1", name: "it-aaaaaaaaaaaa.stl", x: 10, y: 10, turnDeg: 0 },
      { objectId: "2", name: "it-aaaaaaaaaaaa.stl", x: 50, y: 10, turnDeg: 0 },
      { objectId: "3", name: "it-aaaaaaaaaaaa.stl", x: 90, y: 10, turnDeg: 0 },
    ];
    const rows = bedMap(placements, [item("c1", "it-aaaaaaaaaaaa", "A", "P", {}, 2), item("c2", "it-aaaaaaaaaaaa", "B", "P", {})]);
    expect(rows.map((r) => r.label)).toEqual(["A", "A", "B"]);
  });

  it("leaves an object no item claims with an empty entry and its file name", () => {
    const rows = bedMap([{ objectId: "9", name: "stray.stl", x: 1, y: 2, turnDeg: 0 }], sheets04);
    expect(rows[0]).toMatchObject({ entry: "", label: "stray.stl" });
  });

  it("writes the map next to the plate", () => {
    expect(bedMapPathFor("/b/plates/sheets-04.plate.3mf")).toBe("/b/plates/sheets-04.plate.bedmap.json");
  });
});

describe("parseManifest — `label:`", () => {
  const base = ["items:", "  - bkr: bikar:patterns/a.bkr", "    label: GAP 05"];

  it("accepts a label", () => {
    expect((parseManifest(base.join("\n")).items[0] as { label?: string }).label).toBe("GAP 05");
  });

  it("rejects an empty label", () => {
    expect(() => parseManifest(["items:", "  - bkr: bikar:patterns/a.bkr", '    label: " "'].join("\n"))).toThrow(/label/);
  });

  it("rejects two items with one label — they could not be told apart", () => {
    expect(() => parseManifest([...base, "  - bkr: bikar:patterns/b.bkr", "    label: GAP 05"].join("\n"))).toThrow(/already used/);
  });
});
