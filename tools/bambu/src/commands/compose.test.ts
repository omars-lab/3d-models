import { describe, expect, it } from "vitest";
import { createHash } from "node:crypto";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  parseManifest,
  bedFitPrecheck,
  resolveBed,
  findIterationGeometry,
  resolveManifestItems,
  type PartFootprint,
} from "./compose.js";
import { scaledCenteredStl, stlBoundsFromBuffer } from "../mesh.js";

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

  it("reads `profile.color:` as #RRGGBB and refuses anything else", () => {
    const plate = (color: string) =>
      ["profile:", "  filament: PLA Basic", `  color: "${color}"`, "items:", "  - iteration: it-aaaaaaaaaaaa"].join("\n");
    expect(parseManifest(plate("#F5547C")).profile?.color).toBe("#F5547C");
    for (const bad of ["pink", "#F5547", "F5547C", "#F5547CFF"]) {
      expect(() => parseManifest(plate(bad))).toThrow(/profile\.color/);
    }
  });

  it("reads `beds:` and leaves it unset when absent", () => {
    const items = ["items:", "  - iteration: it-aaaaaaaaaaaa"];
    expect(parseManifest(["beds: 2", ...items].join("\n")).beds).toBe(2);
    expect(parseManifest(items.join("\n")).beds).toBeUndefined();
  });

  it("rejects a `beds:` that is not a whole number >= 1", () => {
    for (const bad of ["0", "1.5", "two"]) {
      expect(() => parseManifest([`beds: ${bad}`, "items:", "  - iteration: it-aaaaaaaaaaaa"].join("\n"))).toThrow(/beds/);
    }
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

describe("an `stl:` item — a local mesh, pinned by its hash", () => {
  const SHA = "a".repeat(64);
  const stlItem = (...extra: string[]) =>
    ["items:", "  - stl: .bambu/imports/bear.stl", `    sha256: ${SHA}`, ...extra].join("\n");

  it("accepts a path inside the repo with a hash, a scale and a count", () => {
    const m = parseManifest(stlItem("    scale: 5", "    count: 2", "    label: BEAR"));
    expect(m.items[0]).toMatchObject({ stl: ".bambu/imports/bear.stl", sha256: SHA, scale: 5, count: 2 });
  });

  it("accepts a scale per axis, [x, y, z]", () => {
    // phones-02: the small phones 1.25× wider and longer and 2× thicker than a quarter.
    const m = parseManifest(stlItem("    scale: [0.3125, 0.3125, 0.5]"));
    expect(m.items[0]).toMatchObject({ scale: [0.3125, 0.3125, 0.5] });
  });

  it("refuses a path outside the repo, a missing hash, a bad scale, and bikar fields", () => {
    const bad = (text: string, why: RegExp) => expect(() => parseManifest(text)).toThrow(why);
    bad(["items:", "  - stl: /Users/x/bear.stl", `    sha256: ${SHA}`].join("\n"), /inside this repo/);
    bad(["items:", "  - stl: ../bear.stl", `    sha256: ${SHA}`].join("\n"), /inside this repo/);
    bad(["items:", "  - stl: bear.stl"].join("\n"), /sha256/);
    for (const s of ["0", "-1", "big", "[1, 2]", "[1, 0, 2]", "[1, big, 2]"]) bad(stlItem(`    scale: ${s}`), /scale/);
    bad(stlItem("    piece: Orb"), /cannot also carry `piece:`/);
    bad(stlItem("    bkr: bikar:foo.bkr"), /cannot also carry `bkr:`/);
  });
});

describe("resolveManifestItems — an `stl:` item checks its file", () => {
  const profile = { settings: "X2D;0.20 Std", filament: "PLA Basic" };
  const root = mkdtempSync(join(tmpdir(), "compose-stl-"));
  mkdirSync(join(root, ".bambu", "imports"), { recursive: true });
  const body = asciiTriangle();
  writeFileSync(join(root, ".bambu", "imports", "bear.stl"), body);
  const sha = createHash("sha256").update(body).digest("hex");
  const item = (extra: Record<string, unknown> = {}) => ({ stl: ".bambu/imports/bear.stl", sha256: sha, ...extra });

  it("pins the file as 3d-models:<path> with its hash, and a scale makes another recipe", async () => {
    const [plain, big, one] = await resolveManifestItems([item(), item({ scale: 5 }), item({ scale: 1 })], "ref", profile, root);
    expect(plain).toMatchObject({ sourceAtRef: "3d-models:.bambu/imports/bear.stl", sourceSha256: sha, params: {} });
    expect(plain!.file).toBe(join(root, ".bambu", "imports", "bear.stl"));
    expect(big!.params).toEqual({ scale: 5 });
    expect(big!.iteration).not.toBe(plain!.iteration);
    expect(one!.iteration).toBe(plain!.iteration); // scale 1 is no scale
  });

  it("keys a scale per axis by each axis, and the same number on all three is the plain scale", async () => {
    const [axes, same, five, ones] = await resolveManifestItems(
      [item({ scale: [0.3125, 0.3125, 0.5] }), item({ scale: [5, 5, 5] }), item({ scale: 5 }), item({ scale: [1, 1, 1] })],
      "ref",
      profile,
      root,
    );
    expect(axes!.params).toEqual({ scale_x: 0.3125, scale_y: 0.3125, scale_z: 0.5 });
    expect(same!.params).toEqual({ scale: 5 });
    expect(same!.iteration).toBe(five!.iteration);
    expect(ones!.params).toEqual({});
  });

  it("refuses a file whose hash is not the recipe's, and a file that is not there", async () => {
    await expect(resolveManifestItems([item({ sha256: "b".repeat(64) })], "ref", profile, root)).rejects.toThrow(/not the b{64}/);
    await expect(
      resolveManifestItems([{ stl: ".bambu/imports/none.stl", sha256: sha }], "ref", profile, root),
    ).rejects.toThrow(/no such file/);
  });
});

describe("scaledCenteredStl — the copy a local item puts on the plate", () => {
  it("scales an ASCII or binary mesh, centers its footprint on the origin and writes binary", () => {
    const ascii = Buffer.from(asciiTriangle());
    const big = scaledCenteredStl(ascii, 5);
    expect(big.readUInt32LE(80)).toBe(1);
    expect(stlBoundsFromBuffer(big)).toEqual({ min: [-5, -7.5, 0], max: [5, 7.5, 20] });
    const again = scaledCenteredStl(big, 0.5); // binary in, binary out
    expect(stlBoundsFromBuffer(again)).toEqual({ min: [-2.5, -3.75, 0], max: [2.5, 3.75, 10] });
    expect(() => scaledCenteredStl(ascii, 0)).toThrow(/scale/);
  });

  it("scales each axis by its own number and turns the face normal to match", () => {
    const ascii = Buffer.from(asciiTriangle());
    for (const input of [ascii, scaledCenteredStl(ascii, 1)]) {
      const out = scaledCenteredStl(input, [2, 1, 0.5]);
      expect(stlBoundsFromBuffer(out)).toEqual({ min: [-2, -1.5, 0], max: [2, 1.5, 2] });
      // Edges (4,0,2) and (0,3,0) after the scale: the face points along (-1, 0, 2)/√5.
      const n = [0, 4, 8].map((o) => out.readFloatLE(84 + o));
      expect(n[0]).toBeCloseTo(-1 / Math.sqrt(5), 5);
      expect(n[1]).toBeCloseTo(0, 5);
      expect(n[2]).toBeCloseTo(2 / Math.sqrt(5), 5);
    }
    expect(() => scaledCenteredStl(ascii, [1, 0, 1])).toThrow(/scale/);
  });

  it("moves a mesh modeled off-center so the bed map's place is where it prints", () => {
    // The sheets-04d iPhone sat at x 64-102, y 70-110: the bed map put it 83 mm from where it printed.
    const off = scaledCenteredStl(Buffer.from(asciiTriangle([64, 70, 3])), 1);
    expect(stlBoundsFromBuffer(off)).toEqual({ min: [-1, -1.5, 0], max: [1, 1.5, 4] });
  });
});

/** One triangle spanning 2 x 3 x 4 mm from the corner given (the origin by default). */
function asciiTriangle([x, y, z]: [number, number, number] = [0, 0, 0]): string {
  return [
    "solid t",
    "facet normal 0 0 1",
    "outer loop",
    `vertex ${x} ${y} ${z}`,
    `vertex ${x + 2} ${y} ${z + 4}`,
    `vertex ${x} ${y + 3} ${z}`,
    "endloop",
    "endfacet",
    "endsolid t",
  ].join("\n");
}

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
