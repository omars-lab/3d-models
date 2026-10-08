import { describe, expect, it, vi } from "vitest";
import { bottomIdText, itemRenderFlags, parseManifest, resolveManifestItems } from "./compose.js";

// The carved id (D-109): a recipe with an `id_code:` gives every item an `id:` or a `no_id:`, and each
// `id:` item renders with `--bottom-id <code>/<iteration> <id>`. The bikar blob read is stubbed so the
// resolve tests need no bikar checkout; everything else is the real code.
vi.mock("../backends/bikar.js", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../backends/bikar.js")>()),
  bikarBlobSha: async () => "b".repeat(40),
}));

const recipe = (...lines: string[]) => lines.join("\n");
const BKR = "  - bkr: bikar:patterns/Coasters/Split-Fit.bkr";

describe("parseManifest — the carved id fields", () => {
  it("reads an id_code and keeps each item's id and no_id", () => {
    const m = parseManifest(
      recipe("id_code: SP1", "items:", BKR, "    piece: Lower", "    id: D", BKR, "    piece: Upper", '    no_id: "prints face down"'),
    );
    expect(m.id_code).toBe("SP1");
    expect(m.items[0]).toMatchObject({ id: "D" });
    expect(m.items[1]).toMatchObject({ no_id: "prints face down" });
  });

  it("reads a YAML number id as its one character", () => {
    const m = parseManifest(recipe("id_code: P1", "items:", BKR, "    id: 7"));
    expect(m.items[0]).toMatchObject({ id: "7" });
  });

  it("leaves a recipe without an id_code as it was", () => {
    expect(parseManifest(recipe("items:", BKR)).id_code).toBeUndefined();
  });

  it("refuses an id_code that is too long, lower case, or holds the letter O", () => {
    for (const bad of ["SPL1", "sp1", "PO1", '""']) {
      expect(() => parseManifest(recipe(`id_code: ${bad}`, "items:", BKR, "    id: A"))).toThrow(/id_code/);
    }
  });

  it("refuses an item with neither id nor no_id once the recipe has an id_code", () => {
    expect(() => parseManifest(recipe("id_code: SP1", "items:", BKR, "    id: A", BKR))).toThrow(/items\[1\].*every item needs/);
  });

  it("refuses an id without an id_code, two items with one id, and an id that is not one character", () => {
    expect(() => parseManifest(recipe("items:", BKR, "    id: A"))).toThrow(/needs the recipe's `id_code:`/);
    expect(() => parseManifest(recipe("id_code: SP1", "items:", BKR, "    id: A", BKR, "    id: A"))).toThrow(/already another item's/);
    for (const bad of ["AB", "O", "a", '""']) {
      expect(() => parseManifest(recipe("id_code: SP1", "items:", BKR, `    id: ${bad}`))).toThrow(/`id:` must be one of/);
    }
  });

  it("refuses an item with both, and an empty no_id", () => {
    expect(() => parseManifest(recipe("id_code: SP1", "items:", BKR, "    id: A", "    no_id: why"))).toThrow(/not both/);
    expect(() => parseManifest(recipe("id_code: SP1", "items:", BKR, '    no_id: " "'))).toThrow(/must say why/);
  });

  it("refuses an id on an iteration item and on an stl item: neither renders from source", () => {
    expect(() => parseManifest(recipe("id_code: SP1", "items:", "  - iteration: it-aaaaaaaaaaaa", "    id: A"))).toThrow(
      /only a `bkr:` item can be cut/,
    );
    const stl = ["  - stl: .bambu/imports/bear.stl", `    sha256: ${"a".repeat(64)}`];
    expect(() => parseManifest(recipe("id_code: SP1", "items:", ...stl, "    id: A"))).toThrow(/only a `bkr:` item can be cut/);
    expect(parseManifest(recipe("id_code: SP1", "items:", ...stl, "    no_id: bought in")).items[0]).toMatchObject({ no_id: "bought in" });
  });
});

describe("bottomIdText — what bikar cuts", () => {
  it("is the code, then the iteration and the piece id", () => {
    expect(bottomIdText("SP1", 2, "D")).toBe("SP1/2 D");
  });

  it("refuses an iteration past one digit, and one that is not a count", () => {
    for (const bad of [0, 10, 1.5]) expect(() => bottomIdText("SP1", bad, "D")).toThrow(/one digit/);
  });
});

describe("itemRenderFlags — the id reaches bikar", () => {
  it("adds --bottom-id only when the piece carries one", () => {
    expect(itemRenderFlags({ piece: "Lower", params: {}, window: "", bottomId: "SP1/2 D" })).toEqual([
      "--piece",
      "Lower",
      "--bottom-id",
      "SP1/2 D",
    ]);
    expect(itemRenderFlags({ piece: "Lower", params: {}, window: "", bottomId: "" })).toEqual(["--piece", "Lower"]);
    expect(itemRenderFlags({ piece: "Lower", params: {}, window: "" })).toEqual(["--piece", "Lower"]);
  });
});

describe("resolveManifestItems — the id is part of the recipe", () => {
  const profile = { settings: "X2D;0.20 Std", filament: "PLA Basic" };
  const item = (extra: Record<string, unknown> = {}) => ({ bkr: "bikar:patterns/Coasters/Split-Fit.bkr", piece: "Lower", ...extra });

  it("cuts the plate's code and iteration with each piece's id, and none into a no_id piece", async () => {
    const [d, bare] = await resolveManifestItems([item({ id: "D" }), item({ no_id: "face down" })], "ref", profile, undefined, {
      code: "SP1",
      iteration: 2,
    });
    expect(d!.bottomId).toBe("SP1/2 D");
    expect(bare!.bottomId).toBe("");
  });

  it("keeps a piece without an id on the iteration it had before ids existed", async () => {
    const [before] = await resolveManifestItems([item()], "ref", profile);
    const [after] = await resolveManifestItems([item({ no_id: "face down" })], "ref", profile, undefined, { code: "SP1", iteration: 2 });
    expect(after!.iteration).toBe(before!.iteration);
  });

  it("gives a cut piece its own iteration, and another one for another plate iteration", async () => {
    const [plain] = await resolveManifestItems([item()], "ref", profile);
    const [two] = await resolveManifestItems([item({ id: "D" })], "ref", profile, undefined, { code: "SP1", iteration: 2 });
    const [three] = await resolveManifestItems([item({ id: "D" })], "ref", profile, undefined, { code: "SP1", iteration: 3 });
    expect(two!.iteration).not.toBe(plain!.iteration);
    expect(three!.iteration).not.toBe(two!.iteration);
  });

  it("refuses an id when the caller has no plate code and iteration to cut with it", async () => {
    await expect(resolveManifestItems([item({ id: "D" })], "ref", profile)).rejects.toThrow(/needs the plate's id_code and iteration/);
  });
});
