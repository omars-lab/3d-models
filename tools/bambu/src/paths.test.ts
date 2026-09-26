import { describe, expect, it } from "vitest";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { join } from "node:path";
import { platesDir } from "./paths.js";
import { bikarDir } from "./backends/bikar.js";

// `slice compose` used to write its .3mf to the working directory, so a run from the repo root left
// an untracked plate beside the Makefile (found by the minis-02 run). Plates belong in the
// gitignored build/plates at the repo root, wherever the CLI is started from.
describe("platesDir", () => {
  const root = mkdtempSync(join(tmpdir(), "bambu-paths-"));
  mkdirSync(join(root, ".claude", "gates"), { recursive: true });
  writeFileSync(join(root, ".claude", "gates", "prints_gate.py"), "");
  mkdirSync(join(root, "tools", "bambu"), { recursive: true });

  it("is build/plates at the repo root, from the root or below it", () => {
    expect(platesDir(root)).toBe(join(root, "build", "plates"));
    expect(platesDir(join(root, "tools", "bambu"))).toBe(join(root, "build", "plates"));
  });

  it("is the starting dir outside the repo", () => {
    const outside = mkdtempSync(join(tmpdir(), "bambu-outside-"));
    expect(platesDir(outside)).toBe(outside);
  });
});

// The default once pointed at ~/Workspace/git/bikar, the bare repo, whose leftover files are a
// 12 September build that fails on current .bkr files. It must match the Makefile's BIKAR_DIR.
describe("bikarDir", () => {
  it("defaults to the bikar-main work tree, and BIKAR_DIR overrides it", () => {
    const saved = process.env.BIKAR_DIR;
    try {
      delete process.env.BIKAR_DIR;
      expect(bikarDir()).toBe(join(homedir(), "Workspace", "git", "bikar-main"));
      process.env.BIKAR_DIR = "/elsewhere/bikar";
      expect(bikarDir()).toBe("/elsewhere/bikar");
    } finally {
      if (saved === undefined) delete process.env.BIKAR_DIR;
      else process.env.BIKAR_DIR = saved;
    }
  });
});
