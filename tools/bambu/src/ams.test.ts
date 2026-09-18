import { describe, expect, it } from "vitest";
import {
  buildAmsSlotMap,
  filamentArrays,
  extruderForRegion,
  DEFAULT_AMS_SLOTS,
  type CoasterPartsSidecar,
} from "./ams.js";

/** A coaster sidecar with base/straps/border tagged as given (null ⇒ untagged). */
function sidecar(
  coaster: string,
  regions: Array<[string, string | null, string | null]>,
): CoasterPartsSidecar {
  return {
    coaster,
    pinch: "fillet",
    parts: regions.map(([region, paletteName, hex], i) => ({
      region,
      stl: `${coaster}-${region}.stl`,
      triangles: 100 + i,
      paletteName,
      hex,
    })),
  };
}

describe("buildAmsSlotMap — palette name → logical slot (D-075)", () => {
  it("slot 1 is the plate default; distinct palettes take slots 2+ in first-seen order", () => {
    const sc = sidecar("Star", [
      ["base", "Slab", "#333333"],
      ["straps", "Gold", "#d4af37"],
      ["border", "Slab", "#333333"], // same name as base ⇒ shares its slot
    ]);
    const map = buildAmsSlotMap([sc], { defaultFilament: "PLA Basic" });
    expect(map.slots).toEqual([
      { slot: 1, paletteName: null, hex: null },
      { slot: 2, paletteName: "Slab", hex: "#333333" },
      { slot: 3, paletteName: "Gold", hex: "#d4af37" },
    ]);
    const star = map.assignments.get("Star")!;
    expect(star.get("base")).toBe(2);
    expect(star.get("straps")).toBe(3);
    expect(star.get("border")).toBe(2); // shared with base by name
  });

  it("an untagged region maps to slot 1 (the plate default filament)", () => {
    const sc = sidecar("Plain", [
      ["base", null, null],
      ["straps", "Gold", "#d4af37"],
    ]);
    const map = buildAmsSlotMap([sc], { defaultFilament: "PLA Basic" });
    expect(map.assignments.get("Plain")!.get("base")).toBe(1);
    expect(map.assignments.get("Plain")!.get("straps")).toBe(2);
  });

  it("a palette name shared across coasters shares one slot (first-seen order across the plate)", () => {
    const a = sidecar("A", [["straps", "Gold", "#d4af37"]]);
    const b = sidecar("B", [
      ["base", "Copper", "#b87333"],
      ["straps", "Gold", "#d4af37"], // same name as A's straps ⇒ same slot
    ]);
    const map = buildAmsSlotMap([a, b], { defaultFilament: "PLA Basic" });
    expect(map.slots.map((s) => s.paletteName)).toEqual([null, "Gold", "Copper"]);
    expect(map.assignments.get("A")!.get("straps")).toBe(2);
    expect(map.assignments.get("B")!.get("straps")).toBe(2);
    expect(map.assignments.get("B")!.get("base")).toBe(3);
  });

  it("rejects a palette name that resolves to two different colours", () => {
    const a = sidecar("A", [["straps", "Gold", "#d4af37"]]);
    const b = sidecar("B", [["straps", "Gold", "#ffd700"]]); // same name, different hex
    expect(() => buildAmsSlotMap([a, b], { defaultFilament: "PLA Basic" })).toThrow(/two colours/);
  });

  it("rejects a plate that needs more slots than the AMS has", () => {
    const sc = sidecar("Rainbow", [
      ["base", "Red", "#ff0000"],
      ["straps", "Green", "#00ff00"],
      ["border", "Blue", "#0000ff"],
    ]);
    // default + 3 palettes = 4 slots; cap at 3 ⇒ over capacity.
    expect(() => buildAmsSlotMap([sc], { defaultFilament: "PLA Basic", maxSlots: 3 })).toThrow(
      /but the AMS has 3/,
    );
    // 4 slots fit the one-unit default exactly.
    expect(() => buildAmsSlotMap([sc], { defaultFilament: "PLA Basic" })).not.toThrow();
    expect(DEFAULT_AMS_SLOTS).toBe(4);
  });
});

describe("filamentArrays — project_settings.config parallel arrays (§6)", () => {
  it("reuses the default type+id for every slot and overrides only the colour", () => {
    const sc = sidecar("Star", [
      ["base", "Slab", "#333333"],
      ["straps", "Gold", "#d4af37"],
    ]);
    const map = buildAmsSlotMap([sc], { defaultFilament: "PLA Basic" });
    const arrays = filamentArrays(map, { type: "PLA", id: "GFA00", hex: "#ffffff" });
    expect(arrays.filament_type).toEqual(["PLA", "PLA", "PLA"]);
    expect(arrays.filament_id).toEqual(["GFA00", "GFA00", "GFA00"]); // non-empty per slot (§6)
    expect(arrays.filament_colour).toEqual(["#ffffff", "#333333", "#d4af37"]); // slot 1 = default hex
  });
});

describe("extruderForRegion — the per-part `extruder` value the assembler writes", () => {
  it("returns the 1-based slot, and throws on an unmapped coaster/region", () => {
    const sc = sidecar("Star", [["straps", "Gold", "#d4af37"]]);
    const map = buildAmsSlotMap([sc], { defaultFilament: "PLA Basic" });
    expect(extruderForRegion(map, "Star", "straps")).toBe(2);
    expect(() => extruderForRegion(map, "Star", "border")).toThrow(/no slot/);
    expect(() => extruderForRegion(map, "Ghost", "base")).toThrow(/no slot/);
  });
});
