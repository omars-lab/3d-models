import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { plateRecipePath } from "./color-at-send.js";
import { repoRoot } from "./paths.js";
import {
  applies,
  loadPlateChecks,
  parseApplies,
  parsePlateChecks,
  readRecipeFacts,
  runCheck,
  runPlateChecks,
  spawnRunner,
  verifyPlateChecks,
  type PlateCheck,
  type Runner,
} from "./plate-checks.js";

// The plate checks a send runs (plate-checks.ts, list in .claude/skills/send-plate/plate-checks.yaml).
// The load-bearing case is split-06: its recipe and a bitten kite from ledge_check.py's own
// self-test, through the real script, must be refused.

const root = repoRoot()!;
const PY = process.env.PYTHON ?? "python3";

const entry = (over: Partial<PlateCheck> = {}): PlateCheck => ({
  id: "demo",
  mistake: "demo-01, 2026-10-24: something went wrong",
  source: "docs/design/plates/split-06.md",
  applies: { kind: "always" },
  command: "python3 .claude/skills/place-pins/scripts/ledge_check.py {plate3mf}",
  pass: "all good",
  fail: "something is wrong",
  ...over,
});
const ran = (status: number | null, extra: Partial<ReturnType<Runner>> = {}): Runner => () => ({
  status,
  signal: null,
  stdout: "",
  stderr: "",
  ...extra,
});
const vals = { plate3mf: "/x.3mf", yaml: "/x.yaml", beds: 1 };

describe("the list in the repo", () => {
  it("reads, and every file it names is there (make validate-plate-checks)", () => {
    expect(verifyPlateChecks(root)).toEqual([]);
  });

  it("starts with the ledge check from split-06", () => {
    const first = loadPlateChecks(root)[0]!;
    expect(first.id).toBe("ledge");
    expect(first.command).toContain("ledge_check.py {plate3mf}");
  });
});

describe("parseApplies", () => {
  it("reads the two rule kinds", () => {
    expect(parseApplies("always")).toEqual({ kind: "always" });
    expect(parseApplies({ any_item_bkr_contains: "split-flange" })).toEqual({
      kind: "any_item_bkr_contains",
      text: "split-flange",
    });
  });

  it("refuses anything else, so a typo cannot quietly turn a check off", () => {
    expect(() => parseApplies("sometimes")).toThrow(/applies must be/);
    expect(() => parseApplies({ any_item_bkr_contain: "split" })).toThrow(/applies must be/);
    expect(() => parseApplies({ any_item_bkr_contains: "" })).toThrow(/applies must be/);
    expect(() => parseApplies(undefined)).toThrow(/applies must be/);
  });
});

describe("parsePlateChecks", () => {
  const one = (fields: string) => `checks:\n  - ${fields.trim().split("\n").join("\n    ")}\n`;
  const good = `id: a
mistake: "x"
source: s
applies: always
command: "python3 a.py {plate3mf}"
pass: p
fail: f`;

  it("reads a good entry", () => {
    expect(parsePlateChecks(one(good))[0]).toMatchObject({ id: "a", applies: { kind: "always" } });
  });

  it("refuses a placeholder the send does not fill", () => {
    expect(() => parsePlateChecks(one(good.replace("{plate3mf}", "{plate}")))).toThrow(/\{plate\}/);
  });

  it("refuses an entry with a field missing, and names it", () => {
    expect(() => parsePlateChecks(one(good.replace("fail: f", "")))).toThrow(/entry 1 \(a\): no `fail:`/);
  });

  it("refuses an id used twice", () => {
    expect(() => parsePlateChecks(`checks:\n  - ${good.split("\n").join("\n    ")}\n  - ${good.split("\n").join("\n    ")}\n`)).toThrow(
      /used twice/,
    );
  });

  it("refuses an empty list", () => {
    expect(() => parsePlateChecks("checks: []\n")).toThrow(/no `checks:`/);
  });
});

describe("which checks a plate gets", () => {
  it("split-06 gets the ledge check and the sliced check", () => {
    const facts = readRecipeFacts(plateRecipePath("split-06", root));
    const ids = loadPlateChecks(root)
      .filter((c) => applies(c.applies, facts))
      .map((c) => c.id);
    expect(ids).toEqual(["ledge", "sliced"]);
  });

  it("a plate with no recipe gets only the checks that apply always, with one bed", () => {
    const facts = readRecipeFacts(plateRecipePath("no-such-plate", root));
    expect(facts).toEqual({ bkrs: [], beds: 1 });
    expect(loadPlateChecks(root).filter((c) => applies(c.applies, facts)).map((c) => c.id)).toEqual(["sliced"]);
  });
});

describe("runCheck", () => {
  it("passes on exit 0", () => {
    expect(runCheck(entry(), vals, root, ran(0))).toMatchObject({ ok: true, mark: "✓", line: "demo: all good" });
  });

  it("refuses on a non-zero exit, with the mistake and the tail of the output", () => {
    const r = runCheck(entry(), vals, root, ran(1, { stdout: "a\nb\n20 of 41 bitten\n" }));
    expect(r).toMatchObject({ ok: false, mark: "✗" });
    expect(r.line).toContain("failed (exit 1): something is wrong");
    expect(r.line).toContain("demo-01, 2026-10-24");
    expect(r.detail.at(-1)).toBe("20 of 41 bitten");
  });

  it("refuses when the interpreter cannot be started, rather than skipping", () => {
    const r = runCheck(entry(), vals, root, ran(null, { error: new Error("spawnSync python3 ENOENT") }));
    expect(r).toMatchObject({ ok: false, mark: "✗" });
    expect(r.line).toContain("could not run (spawnSync python3 ENOENT)");
  });

  it("refuses when the script it names is gone, without running anything", () => {
    let called = false;
    const r = runCheck(entry({ command: "python3 tools/gone.py {plate3mf}" }), vals, root, () => {
      called = true;
      return { status: 0, signal: null, stdout: "", stderr: "" };
    });
    expect(called).toBe(false);
    expect(r.line).toContain("tools/gone.py is not in the repo");
  });

  it("refuses a check stopped by a timeout", () => {
    expect(runCheck(entry(), vals, root, ran(null, { signal: "SIGTERM" })).line).toContain("stopped by SIGTERM");
  });

  it("fills the placeholders, the recipe's beds included", () => {
    let argv: string[] = [];
    runCheck(entry({ command: "tools/bambu/bin/bambu validate sliced {plate3mf} --beds {beds}" }), { ...vals, beds: 2 }, root, (a) => {
      argv = a;
      return { status: 0, signal: null, stdout: "", stderr: "" };
    });
    expect(argv).toEqual(["tools/bambu/bin/bambu", "validate", "sliced", "/x.3mf", "--beds", "2"]);
  });
});

// The load-bearing case: split-06's recipe with a plate whose kite has its point bitten flat,
// through the real ledge_check.py. The `sliced` entry is stubbed (it would start a second CLI).
describe("split-06's shape is refused", () => {
  let dir: string;
  beforeAll(() => {
    dir = mkdtempSync(join(tmpdir(), "plate-checks-"));
    const w = spawnSync(PY, [join(root, ".claude/skills/place-pins/scripts/ledge_check.py"), "--write-fixture", dir], {
      encoding: "utf8",
    });
    expect(w.status, w.stderr).toBe(0);
  });
  afterAll(() => rmSync(dir, { recursive: true, force: true }));

  const realLedgeOnly: Runner = (argv, cwd) =>
    argv.some((a) => a.endsWith("ledge_check.py")) ? spawnRunner(argv, cwd) : { status: 0, signal: null, stdout: "", stderr: "" };

  it("a bitten ledge on a split-flange plate refuses the send", () => {
    const results = runPlateChecks(loadPlateChecks(root), join(dir, "bitten.3mf"), plateRecipePath("split-06", root), root, realLedgeOnly);
    const ledge = results.find((r) => r.id === "ledge")!;
    expect(ledge).toMatchObject({ ok: false, mark: "✗" });
    expect(ledge.line).toContain("split-06, 2026-10-24");
    expect(ledge.detail.join("\n")).toContain("1 with a bitten ledge");
    expect(results.every((r) => r.ok)).toBe(false);
  });

  it("the same kite with its ledge whole passes", () => {
    const results = runPlateChecks(loadPlateChecks(root), join(dir, "clean.3mf"), plateRecipePath("split-06", root), root, realLedgeOnly);
    expect(results.map((r) => `${r.mark} ${r.id}`)).toEqual(["✓ ledge", "✓ sliced"]);
  });

  it("a plate the script cannot read is refused too", () => {
    const junk = join(dir, "junk.3mf");
    writeFileSync(junk, "not a zip");
    const ledge = runPlateChecks(loadPlateChecks(root), junk, plateRecipePath("split-06", root), root, realLedgeOnly)[0]!;
    expect(ledge).toMatchObject({ ok: false, mark: "✗" });
    expect(ledge.line).toContain("exit 2");
  });
});
