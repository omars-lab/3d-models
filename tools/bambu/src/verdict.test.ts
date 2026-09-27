import { describe, expect, it } from "vitest";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { applyVerdict, setVerdict, VerdictError } from "./verdict.js";

// A record as the scaffolder writes it: the verdict a quoted TODO, notes an empty flow list.
const DRAFT = [
  "---",
  "run: 2026-09-27-t",
  "status: printed",
  "objects:",
  '  - entry: "c1"',
  '    source: "bikar:patterns/a.bkr"',
  '    params: {"size": 80}',
  "    count: 1",
  '    verdict: "TODO"',
  "    notes: []",
  '  - entry: "c2"',
  '    source: "bikar:patterns/b.bkr"',
  "    count: 2",
  "    verdict: adjust",
  "    notes:",
  '      - "pegs too tight"',
  "photos: []",
  "---",
  "",
  "Body text, with a --- rule below.",
  "---",
  "",
].join("\n");

function changedLines(a: string, b: string): { removed: string[]; added: string[] } {
  const as = a.split("\n");
  const bs = b.split("\n");
  return { removed: as.filter((l) => !bs.includes(l)), added: bs.filter((l) => !as.includes(l)) };
}

describe("applyVerdict", () => {
  it("replaces a TODO verdict and turns notes: [] into a list", () => {
    const r = applyVerdict(DRAFT, "c1", "keep", ["clean edges"]);
    expect(r.from).toBe("TODO");
    expect(r.text.split("\n").slice(8, 12)).toEqual([
      "    verdict: keep",
      "    notes:",
      '      - "clean edges"',
      '  - entry: "c2"',
    ]);
    expect(r.text.split("\n").length).toBe(DRAFT.split("\n").length + 1);
  });

  it("appends notes after the existing ones and touches no other piece", () => {
    const r = applyVerdict(DRAFT, "c2", "drop", ["border too wide"]);
    expect(r.from).toBe("adjust");
    const lines = r.text.split("\n");
    const i = lines.indexOf('      - "pegs too tight"');
    expect(lines[i + 1]).toBe('      - "border too wide"');
    expect(lines[i + 2]).toBe("photos: []");
    expect(r.text.split("\n").slice(0, 11)).toEqual(DRAFT.split("\n").slice(0, 11));
  });

  it("does not add a note that is already there, so a repeat changes nothing", () => {
    const r = applyVerdict(DRAFT, "c2", "adjust", ["pegs too tight"]);
    expect(r.notesAdded).toEqual([]);
    expect(r.text).toBe(DRAFT);
  });

  it("adds a verdict line to a piece that has none, before its notes", () => {
    const noVerdict = DRAFT.replace('    verdict: "TODO"\n', "");
    const r = applyVerdict(noVerdict, "c1", "adjust");
    expect(r.from).toBeNull();
    const lines = r.text.split("\n");
    expect(lines[lines.indexOf("    verdict: adjust") + 1]).toBe("    notes: []");
  });

  it("leaves the body alone even when it has --- lines", () => {
    const r = applyVerdict(DRAFT, "c1", "keep");
    expect(r.text.split("\n---\n").slice(1)).toEqual(DRAFT.split("\n---\n").slice(1));
  });

  // The by-design refusals: each must throw, never write something the prints gate would reject.
  it.each([
    ["an unknown piece, naming the ones there are", "c9", "keep", [], /no piece "c9".*c1, c2/],
    ["a verdict outside keep|adjust|drop", "c1", "looks-good", [], /must be one of keep, adjust, drop/],
    ["a note with a line break", "c1", "keep", ["a\nb"], /one non-empty line/],
    ["an empty note", "c1", "keep", ["  "], /one non-empty line/],
  ] as const)("refuses %s", (_what, entry, verdict, notes, msg) => {
    expect(() => applyVerdict(DRAFT, entry, verdict, notes)).toThrow(msg);
  });

  it("refuses a file with no front matter", () => {
    expect(() => applyVerdict("no front matter\n", "c1", "keep")).toThrow(VerdictError);
  });

  it("keeps a note with quotes and a colon readable as YAML", () => {
    const note = 'border "about 11 mm": worked out, not measured';
    const r = applyVerdict(DRAFT, "c1", "keep", [note]);
    expect(r.notesAdded).toEqual([note]);
  });
});

describe("applyVerdict on a shipped record", () => {
  // The real minis-04 record: hand-written notes, flow-mapping params, a feedback block after.
  const real = readFileSync(resolve(dirname(fileURLToPath(import.meta.url)), "../../../docs/prints/2026-09-26-minis-04/index.md"), "utf8");

  it("changes only the one verdict line", () => {
    const r = applyVerdict(real, "c2", "keep");
    expect(changedLines(real, r.text)).toEqual({ removed: [], added: ["    verdict: keep"] });
    expect(r.text.split("\n").length).toBe(real.split("\n").length);
  });
});

describe("setVerdict", () => {
  it("writes the record, and writes nothing when nothing changes", () => {
    const root = mkdtempSync(join(tmpdir(), "bambu-verdict-"));
    try {
      const dir = join(root, "docs", "prints", "2026-09-27-t");
      mkdirSync(dir, { recursive: true });
      writeFileSync(join(dir, "index.md"), DRAFT);
      const first = setVerdict(root, "2026-09-27-t", "c1", "keep", ["ok"]);
      expect(first).toMatchObject({ from: "TODO", to: "keep", notesAdded: ["ok"], changed: true });
      const again = setVerdict(root, "2026-09-27-t", "c1", "keep", ["ok"]);
      expect(again.changed).toBe(false);
      expect(() => setVerdict(root, "../etc", "c1", "keep")).toThrow(/not a run name/);
      expect(() => setVerdict(root, "2026-01-01-none", "c1", "keep")).toThrow(/no print record/);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
