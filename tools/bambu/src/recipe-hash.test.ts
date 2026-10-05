import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { type ColorPlate, writeRecipes } from "./by-color.js";
import { recipeHash } from "./recipe-hash.js";

// The planner keys its frozen slices by recipeHash, and the send and the approvals key a recipe by
// iterations.py's hash_text. If the two ever disagree, a plan's slice and the plate it becomes no
// longer match, so this runs both on the same texts. PYTHON names an interpreter with PyYAML (the
// Makefile passes its own); the macOS system python3 has none, and the test says so rather than skip.

const repo = fileURLToPath(new URL("../../../", import.meta.url));
const scripts = join(repo, ".claude/skills/manage-approvals/scripts");

function pythonHashes(texts: string[]): Array<string | null> {
  const code = [
    "import json, sys",
    `sys.path.insert(0, ${JSON.stringify(scripts)})`,
    "from iterations import hash_text",
    "print(json.dumps([hash_text(t) for t in json.load(sys.stdin)]))",
  ].join("\n");
  const res = spawnSync(process.env.PYTHON ?? "python3", ["-c", code], { input: JSON.stringify(texts), encoding: "utf8" });
  if (res.status !== 0) throw new Error(`python could not hash (needs PyYAML; set PYTHON): ${res.stderr || res.error}`);
  return JSON.parse(res.stdout) as Array<string | null>;
}

const plate: ColorPlate = {
  color: { key: "PLA Silk|13401", hex: "#e5b03d", line: "PLA Silk", code: "13401", name: "Gold", note: "not on the US store, 2026-10-04" },
  items: [
    { construction: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr", params: { size: 112.5, strap: 3.75 }, piece: null, count: 2, rank: -1 },
    { construction: "bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr", params: { size: 112.5, gap: 0 }, piece: "Star", count: 2, rank: 3 },
  ],
};
const written = writeRecipes([plate], "fixture-t", ["about — with a dash"], () => 10)[0]!.text;

describe("recipeHash — the same hash as iterations.py", () => {
  const texts = [
    written,
    written.replace(/^# .*$/m, "# a comment edited, so not a change"),
    written.replace("count:  2", "count:  3"),
    readFileSync(join(repo, "docs/design/plates/sheets-04g.yaml"), "utf8"),
    "label: Café ✓\nitems: [1, 2.5, true, null]\n",
    "",
    "items: [\n",
  ];

  it("agrees with python on written recipes, a real plate, non-ASCII, empty and broken YAML", () => {
    expect(texts.map(recipeHash)).toEqual(pythonHashes(texts));
  });

  it("ignores a comment edit and sees a count change", () => {
    const [a, comment, count] = texts.map(recipeHash);
    expect(comment).toBe(a);
    expect(count).not.toBe(a);
    expect(recipeHash("")).toBeNull();
  });
});
