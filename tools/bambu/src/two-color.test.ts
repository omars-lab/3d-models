// Tests for a plate with two filaments: each item names its slot, each slot its color, and Studio is
// told which slot each mesh prints in. Built for sheets-04g (2026-10-04), where the pink and black
// piece sets are the same meshes in two colors, so slot is the only thing that tells them apart.

import { describe, it, expect } from "vitest";
import {
  bedMap,
  checkItemFilaments,
  itemSliceProfile,
  parseManifest,
  stagedName,
  type ManifestItem,
  type ResolvedItem,
} from "./commands/compose.js";
import { buildStudioArgs } from "./commands/slice.js";

const PLA = "Bambu PLA Basic @BBL X2D 0.4 nozzle";
const profile = { settings: "m;p", filament: `${PLA};${PLA}` };

describe("parseManifest — `filament:` slots and a color list", () => {
  const twoColor = (items: string[]) =>
    ["profile:", `  filament: "${PLA};${PLA}"`, '  color: ["#F5547C", "#000000"]', "items:", ...items].join("\n");

  it("takes a color list and a slot per item", () => {
    const m = parseManifest(
      twoColor(["  - bkr: bikar:a.bkr", "    filament: 1", "  - bkr: bikar:a.bkr", "    filament: 2", "    label: BLACK"]),
    );
    expect(m.profile?.color).toEqual(["#F5547C", "#000000"]);
    expect(m.items.map((i) => i.filament)).toEqual([1, 2]);
  });

  it("refuses an item with no slot on a two-filament plate — it would print in slot 1 unasked", () => {
    expect(() => parseManifest(twoColor(["  - bkr: bikar:a.bkr", "    filament: 1", "  - bkr: bikar:b.bkr"]))).toThrow(
      /items\[1\]: the plate has 2 filaments/,
    );
  });

  it("refuses a slot past the filaments", () => {
    expect(() => parseManifest(twoColor(["  - bkr: bikar:a.bkr", "    filament: 3"]))).toThrow(/slot from 1 to 2, got 3/);
  });

  it("refuses a color list with a bad entry", () => {
    const text = ["profile:", '  color: ["#F5547C", "black"]', "items:", "  - bkr: bikar:a.bkr"].join("\n");
    expect(() => parseManifest(text)).toThrow(/profile\.color/);
  });

  it("leaves a one-filament plate's items free to omit the slot", () => {
    expect(() => checkItemFilaments([{ bkr: "bikar:a.bkr" }], 1)).not.toThrow();
  });
});

describe("itemSliceProfile — an item's id names the preset it prints in", () => {
  it("keeps the plate's whole filament string for an item with no slot, so old ids stay", () => {
    expect(itemSliceProfile({}, profile)).toBe(profile);
  });

  it("names the slot's own preset for an item with a slot", () => {
    const two = { settings: "m;p", filament: `${PLA};Bambu PETG HF` };
    expect(itemSliceProfile({ filament: 2 }, two)).toEqual({ settings: "m;p", filament: "Bambu PETG HF" });
  });
});

function item(entry: string, iteration: string, label: string, filament: number): ResolvedItem {
  const sourcePath = "patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr";
  return {
    entry,
    sourcePath,
    sourceAtRef: `bikar:${sourcePath}@x`,
    piece: "Kite",
    params: {},
    window: "",
    count: 1,
    sourceSha256: "s",
    iteration,
    label,
    filament,
  };
}

describe("the bed map tells two colors of one piece apart", () => {
  const pink = item("c1", "it-aaaaaaaaaaaa", "PINK KITE", 1);
  const black = item("c2", "it-aaaaaaaaaaaa", "BLACK KITE", 2);

  it("stages slot 1 under the old name and another slot with -f<slot>", () => {
    expect(stagedName(pink)).toBe("it-aaaaaaaaaaaa.stl");
    expect(stagedName(black)).toBe("it-aaaaaaaaaaaa-f2.stl");
  });

  it("joins each object to its color's item, whatever order the arrange gave them", () => {
    const rows = bedMap(
      [
        { objectId: "4", name: "it-aaaaaaaaaaaa-f2.stl", x: 20, y: 20, turnDeg: 0 },
        { objectId: "2", name: "it-aaaaaaaaaaaa.stl", x: 60, y: 20, turnDeg: 0 },
      ],
      [pink, black],
    );
    expect(rows.map((r) => [r.label, r.filament, r.x])).toEqual([
      ["PINK KITE", 1, 60],
      ["BLACK KITE", 2, 20],
    ]);
  });
});

describe("buildStudioArgs — one filament id per input", () => {
  it("passes the ids in input order", () => {
    const args = buildStudioArgs(["a.stl", "b.stl", "b.stl"], "/o", "p.3mf", { arrange: true, plate: "0", filamentIds: [2, 1, 1] }, []);
    expect(args.slice(args.indexOf("--load-filament-ids"), args.indexOf("--load-filament-ids") + 2)).toEqual([
      "--load-filament-ids",
      "2,1,1",
    ]);
  });

  it("leaves the flag out with no ids", () => {
    expect(buildStudioArgs(["a.stl"], "/o", "p.3mf", { arrange: true, plate: "0" }, [])).not.toContain("--load-filament-ids");
  });

  it("refuses a count that differs from the inputs, as Studio would (exit 254)", () => {
    expect(() => buildStudioArgs(["a.stl", "b.stl"], "/o", "p.3mf", { arrange: true, plate: "0", filamentIds: [1] }, [])).toThrow(
      /1 filament id\(s\) for 2 input\(s\)/,
    );
  });
});

// The type a manifest item carries its slot on, checked at compile time.
const _typed: ManifestItem = { stl: "x.stl", sha256: "0".repeat(64), filament: 2 };
void _typed;
