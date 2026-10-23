import { describe, expect, it } from "vitest";
import { checkGroups } from "./commands/compose.js";
import { BLOCK_GAP_MM, footprintCentres, layoutGroups, overlaps, writePlacements, type LayoutPiece } from "./group-layout.js";

const bed = { x: 256, y: 256 };

function set(tag: string): LayoutPiece[] {
  return [
    { name: `lower-${tag}.stl`, group: `set ${tag}`, w: 60, h: 55 },
    { name: `upper-${tag}.stl`, group: `set ${tag}`, w: 60, h: 55 },
    { name: `kite-${tag}.stl`, group: `set ${tag}`, w: 12, h: 20 },
    { name: `kite-${tag}.stl`, group: `set ${tag}`, w: 12, h: 20 },
    { name: `star-${tag}.stl`, group: `set ${tag}`, w: 14, h: 14 },
  ];
}

describe("layoutGroups", () => {
  it("puts each group in its own block, side by side, nothing touching", () => {
    const { pieces, blocks } = layoutGroups([...set("25"), ...set("15"), ...set("10")], bed);
    expect(blocks.map((b) => b.group)).toEqual(["set 25", "set 15", "set 10"]);
    for (let i = 1; i < blocks.length; i++) expect(blocks[i]!.x0 - blocks[i - 1]!.x1).toBeCloseTo(BLOCK_GAP_MM);
    for (const p of pieces) {
      const b = blocks.find((k) => k.group === p.group)!;
      expect(p.x - p.w / 2).toBeGreaterThanOrEqual(b.x0 - 1e-9);
      expect(p.x + p.w / 2).toBeLessThanOrEqual(b.x1 + 1e-9);
      expect(p.y - p.h / 2).toBeGreaterThanOrEqual(b.y0 - 1e-9);
      expect(p.y + p.h / 2).toBeLessThanOrEqual(b.y1 + 1e-9);
      expect(p.x - p.w / 2).toBeGreaterThanOrEqual(0);
      expect(p.x + p.w / 2).toBeLessThanOrEqual(bed.x);
    }
    expect(pieces).toHaveLength(15);
    expect(overlaps(pieces, 1)).toBeNull();
  });

  it("refuses a piece wider than its column", () => {
    const wide = [...set("25"), ...set("15"), ...set("10"), { name: "big.stl", group: "set 10", w: 90, h: 10 }];
    expect(() => layoutGroups(wide, bed)).toThrow(/big\.stl is 90\.0 mm wide/);
  });

  it("refuses a group deeper than the bed", () => {
    const deep = Array.from({ length: 6 }, (_, i) => ({ name: `p${i}.stl`, group: "one", w: 200, h: 50 }));
    expect(() => layoutGroups(deep, bed)).toThrow(/group "one" needs/);
  });
});

describe("overlaps", () => {
  it("names two pieces that come closer than the clearance", () => {
    const a = { name: "a", group: "g", w: 10, h: 10, x: 0, y: 0 };
    const b = { name: "b", group: "g", w: 10, h: 10, x: 11, y: 0 };
    expect(overlaps([a, b], 0.5)).toBeNull();
    expect(overlaps([a, b], 2)).toEqual(["a", "b"]);
  });
});

describe("writePlacements", () => {
  const model = `<model><resources/><build><item objectid="2" transform="0 1 0 -1 0 0 0 0 1 10 20 3.5" printable="1"/><item objectid="4" printable="1"/></build></model>`;
  const settings = `<config><object id="2"><metadata key="name" value="a.stl"/></object><object id="4"><metadata key="name" value="b.stl"/></object></config>`;
  const place = (name: string, x: number, y: number) => ({ name, group: "g", w: 1, h: 1, x, y });

  it("moves each item to its place, unturned, keeping its height", () => {
    const out = writePlacements(model, settings, [place("a.stl", 50, 60), place("b.stl", 70, 80)]);
    expect(out).toContain('transform="1 0 0 0 1 0 0 0 1 50.0000 60.0000 3.5"');
    expect(out).toContain('<item transform="1 0 0 0 1 0 0 0 1 70.0000 80.0000 0" objectid="4"');
  });

  it("refuses an object with no place", () => {
    expect(() => writePlacements(model, settings, [place("a.stl", 1, 1)])).toThrow(/no place in the group layout for b\.stl/);
  });

  it("refuses a place with no object", () => {
    expect(() => writePlacements(model, settings, [place("a.stl", 1, 1), place("b.stl", 1, 1), place("c.stl", 1, 1)])).toThrow(/no object in the arranged plate for c\.stl/);
  });
});

describe("checkGroups", () => {
  it("takes a plate where every item or no item names a group", () => {
    expect(() => checkGroups([{ group: "a" }, { group: "b" }])).not.toThrow();
    expect(() => checkGroups([{}, {}])).not.toThrow();
  });

  it("refuses a plate where only some items name a group, or a group is blank", () => {
    expect(() => checkGroups([{ group: "a" }, {}])).toThrow(/items\[1\]: other items name a `group:`/);
    expect(() => checkGroups([{ group: " " }])).toThrow(/must be a non-empty string/);
  });
});

describe("footprintCentres", () => {
  // Two objects whose meshes are the same square, offset by opposite components, as Studio wrote
  // split-04's lower and upper halves: their centres differ though both items sat at one place.
  const model = `<model><resources>
<object id="2" type="model"><components><component p:path="/3D/Objects/a.model" objectid="1" transform="1 0 0 0 1 0 0 0 1 20 15 1.8"/></components></object>
<object id="4" type="model"><components><component p:path="/3D/Objects/b.model" objectid="3" transform="1 0 0 0 1 0 0 0 1 20 -15 1.1"/></components></object>
</resources><build><item objectid="2" transform="1 0 0 0 1 0 0 0 1 100 100 0"/><item objectid="4" transform="1 0 0 0 1 0 0 0 1 100 100 0"/></build></model>`;
  const square = `<mesh><vertices><vertex x="-5" y="0" z="0"/><vertex x="5" y="10" z="0"/></vertices></mesh>`;
  const meshes = new Map([["/3D/Objects/a.model", square], ["/3D/Objects/b.model", square]]);
  const settings = `<config><object id="2"><metadata key="name" value="a.stl"/></object><object id="4"><metadata key="name" value="b.stl"/></object></config>`;

  it("measures each object's centre through its component's offset", () => {
    const c = footprintCentres(model, meshes);
    expect(c.get("2")).toEqual({ cx: 20, cy: 20 });
    expect(c.get("4")).toEqual({ cx: 20, cy: -10 });
  });

  it("shifts each item so its footprint, not its origin, lands on the place", () => {
    const out = writePlacements(model, settings, [
      { name: "a.stl", group: "g", w: 10, h: 10, x: 50, y: 50 },
      { name: "b.stl", group: "g", w: 10, h: 10, x: 50, y: 70 },
    ], footprintCentres(model, meshes));
    expect(out).toContain('transform="1 0 0 0 1 0 0 0 1 30.0000 30.0000 0"');
    expect(out).toContain('transform="1 0 0 0 1 0 0 0 1 30.0000 80.0000 0"');
  });

  it("refuses an object whose mesh file is missing", () => {
    expect(() => footprintCentres(model, new Map([["/3D/Objects/a.model", square]]))).toThrow(/object 4: no mesh file/);
  });
});
