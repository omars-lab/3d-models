import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { type ApproveTool, plateApproval, plateApproveTool, plateNameOf, printerBusy, recipeHashOf, spendApproval } from "./send-gate.js";
import { checkSliceFresh } from "./slice-fresh.js";

// The send checks (send-gate.ts, D-093, D-096, D-097), run against the real `plate_approve.py` (the
// manage-approvals skill's) on pages under a temporary git repo whose origin/master holds them, since
// a yes names the master commit of the recipe iteration it covers. The load-bearing case is the spent approval: a page whose yes was
// spent by a send is not approved for the next one, even with its box still ticked (sheets-04 on
// 2026-10-02 was sent from Bambu Studio, which does not untick the box).

let root: string;
const TABLE = "| Date | Decision | By | Covers | Spent by |\n|---|---|---|---|---|";

function page(name: string, opts: { box?: "x" | " "; approvals?: string[]; rows?: string[]; maturity?: string; stage?: string }): string {
  const dir = join(root, "docs", "design", "plates");
  const fm = ["---", `plate: ${name}`, `recipe: ${name}.yaml`, `stage: ${opts.stage ?? "waiting"}`, `maturity: ${opts.maturity ?? "experiment"}`, "---"].join("\n");
  const box = `\n## Your call\n\n- [${opts.box ?? " "}] **Approve as it stands**\n- [ ] **Hold**\n`;
  const approvals = `\n## Approvals\n\n${[TABLE, ...(opts.approvals ?? [])].join("\n")}\n`;
  const rows = (opts.rows ?? ["2026-10-01 | proposed — drawn"]).map((r) => `| ${r} | this page |`);
  const body = `${box}${approvals}\n## Timeline\n\n| Date | What happened | Where it is written |\n|---|---|---|\n${rows.join("\n")}\n\n## After\n\ntext\n`;
  const path = join(dir, `${name}.md`);
  writeFileSync(join(dir, `${name}.yaml`), `bed: x2d\n# ${name}\n`);
  writeFileSync(path, `${fm}\n${body}`);
  plateApproveTool([path, "--iterate", "--date", "2026-10-01"]);
  merged();
  return path;
}

/** What a merge to master does for the temporary repo: commit everything, move origin/master. */
function merged(): void {
  const git = (...args: string[]) => execFileSync("git", ["-C", root, ...args], { stdio: "ignore" });
  git("add", "-A");
  git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "merged");
  git("update-ref", "refs/remotes/origin/master", "HEAD");
}

/** A yes, written the way a session writes one: through the tool. */
function approve(path: string, date: string): void {
  plateApproveTool([path, "--approved", "--by", "Omar, tick", "--date", date]);
}

beforeAll(() => {
  root = mkdtempSync(join(tmpdir(), "send-gate-"));
  mkdirSync(join(root, "docs", "design", "plates"), { recursive: true });
  execFileSync("git", ["init", "-q", root]);
});
afterAll(() => rmSync(root, { recursive: true, force: true }));

describe("plateNameOf", () => {
  it("strips the sliced suffixes", () => {
    expect(plateNameOf("/x/build/plates/sheets-04b.plate.3mf")).toBe("sheets-04b");
    expect(plateNameOf("minis-01.3mf")).toBe("minis-01");
  });
});

describe("plateApproval", () => {
  it("refuses a plate with no page", () => {
    const a = plateApproval("nowhere", root);
    expect(a.exists).toBe(false);
    expect(a.approved).toBe(false);
  });

  it("refuses a page with nothing in its Approvals table", () => {
    page("p-empty", {});
    const a = plateApproval("p-empty", root);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("no approval in the Approvals table");
  });

  it("refuses a tick nobody has recorded, and says how to record it", () => {
    page("p-tick", { box: "x" });
    const a = plateApproval("p-tick", root);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("not recorded");
  });

  it("takes an open approval on the recipe as it is", () => {
    const path = page("p-yes", { box: "x" });
    approve(path, "2026-10-03");
    expect(readFileSync(path, "utf8")).not.toMatch(/\[x\] \*\*Approve/);
    const a = plateApproval("p-yes", root);
    expect(a.approved).toBe(true);
    expect(a.how).toContain("2026-10-03");
    expect(a.how).toContain("first send");
  });

  it("reads back the color a yes covers, and none from a yes that names none", () => {
    const path = page("p-color", { box: "x" });
    plateApproveTool([path, "--approved", "--by", "Omar, in chat", "--date", "2026-10-03", "--color", "#0047bb"]);
    expect(plateApproval("p-color", root).color).toBe("#0047BB");
    expect(plateApproval("p-yes", root).color).toBeNull();
  });

  it("refuses an approval spent by a send (the sheets-04 shape, box still ticked)", () => {
    page("p-spent", {
      box: "x",
      stage: "printed",
      approvals: [
        "| 2026-10-02 | approved | Omar, tick (before the peaked set) | — | replaced 2026-10-02 |",
        "| 2026-10-02 | approved | Omar, tick, with the fixed peak | — | sent 2026-10-02 |",
      ],
      rows: ["2026-10-01 | proposed", "2026-10-02 | sent — by Omar, from Bambu Studio", "2026-10-02 | printed — on the X2D"],
    });
    const a = plateApproval("p-spent", root);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("was sent 2026-10-02");
    expect(a.how).toContain("not recorded");
    expect(a.sends).toBe(1);
  });

  it("refuses a recipe changed after the yes, and says to record the change, which resets the yes (D-097)", () => {
    const path = page("p-changed", {});
    approve(path, "2026-10-03");
    writeFileSync(path.replace(/\.md$/, ".yaml"), "bed: x2d\nspacing: 4\n");
    const a = plateApproval("p-changed", root);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("--iterate");
  });

  it("keeps the yes when the recipe only gained a comment: a reprint as-is", () => {
    const path = page("p-comment", {});
    approve(path, "2026-10-03");
    writeFileSync(path.replace(/\.md$/, ".yaml"), "# packed the same\nbed: x2d\n");
    expect(plateApproval("p-comment", root).approved).toBe(true);
  });

  it("reports the recipe hash a slice records, the same for a comment edit and new for a real one (slice-fresh.ts)", () => {
    const path = page("p-fresh", {});
    const recipe = path.replace(/\.md$/, ".yaml");
    const sliced = recipeHashOf(join(root, "build", "plates", "p-fresh.plate.3mf"), root);
    expect(sliced).toMatch(/^[0-9a-f]{12}$/);
    expect(plateApproval("p-fresh", root).recipe).toBe(sliced);
    writeFileSync(recipe, `# a note\n${readFileSync(recipe, "utf8")}`);
    expect(checkSliceFresh(sliced, plateApproval("p-fresh", root).recipe).ok).toBe(true);
    writeFileSync(recipe, "bed: x2d\nspacing: 4\n");
    const fresh = checkSliceFresh(sliced, plateApproval("p-fresh", root).recipe);
    expect(fresh.ok).toBe(false);
    expect(fresh.line).toContain("the recipe changed since this slice");
  });

  it("has no recipe hash for a plate with no page", () => {
    expect(recipeHashOf("nowhere.plate.3mf", root)).toBeNull();
  });

  it("refuses when the tool does not run: a status it cannot read is not a yes", () => {
    page("p-broken", {});
    const broken: ApproveTool = () => {
      throw Object.assign(new Error("spawn python3 ENOENT"), { stderr: "" });
    };
    const a = plateApproval("p-broken", root, broken);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("did not read the page");
  });

  it("reads a real page in this repo: sheets-04's yes was spent by its send", () => {
    const repo = fileURLToPath(new URL("../../../", import.meta.url));
    const a = plateApproval("sheets-04", repo);
    expect(a.exists).toBe(true);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("was sent 2026-10-02");
  });
});

describe("plateApproval on a production plate (D-095)", () => {
  it("passes on the tool's standing answer", () => {
    page("p-prod", { maturity: "production" });
    const stands: ApproveTool = () => JSON.stringify({ approved: true, how: "standing approval: its prints still show production (D-095)", sends: 2, standing: true });
    const a = plateApproval("p-prod", root, stands);
    expect(a.approved).toBe(true);
    expect(a.standing).toBe(true);
    expect(a.how).toContain("D-095");
  });

  it("refuses a page that says production when its grade cannot be read, and says why", () => {
    // The temporary repo has no print records or bets file, so the grade does not run.
    page("p-nograde", { maturity: "production" });
    const a = plateApproval("p-nograde", root);
    expect(a.approved).toBe(false);
    expect(a.standing).toBe(false);
    expect(a.how).toContain("no standing approval");
  });
});

describe("spendApproval", () => {
  it("spends the yes: Spent by filled, box unticked, stage sent, the send logged, the next send refused", () => {
    const path = page("p-spend", {});
    approve(path, "2026-10-03");
    writeFileSync(path, readFileSync(path, "utf8").replace("- [ ] **Approve", "- [x] **Approve"));
    const before = plateApproval("p-spend", root);
    expect(before.approved).toBe(true);
    const row = spendApproval(path, "2026-10-03", before);
    const text = readFileSync(path, "utf8");
    expect(row).toContain("spends the approval of 2026-10-03");
    expect(text).toContain("stage: sent");
    expect(text).toContain("| sent 2026-10-03 |");
    expect(text).not.toMatch(/\[x\] \*\*Approve/);
    expect(text.indexOf(row)).toBeLessThan(text.indexOf("## After"));
    const after = plateApproval("p-spend", root);
    expect(after.approved).toBe(false);
    expect(after.sends).toBe(1);
  });

  it("passes --standing for a standing send, so it spends nothing", () => {
    const seen: string[][] = [];
    const tool: ApproveTool = (args) => {
      seen.push(args);
      return "| 2026-10-03 | sent — by `bambu print send`, on the standing approval of a production plate (D-095) | this page |\n";
    };
    const row = spendApproval("/p.md", "2026-10-03", { page: "/p.md", exists: true, approved: true, how: "", sends: 0, standing: true, recipe: null, color: null }, tool);
    expect(seen[0]).toContain("--standing");
    expect(row).toContain("standing approval");
  });

  it("refuses to spend on a page that is not approved, with the tool's reason", () => {
    const path = page("p-nospend", {});
    expect(() => spendApproval(path, "2026-10-03", plateApproval("p-nospend", root))).toThrow(/not approved for a send/);
  });
});

describe("printerBusy", () => {
  it("lets an idle printer take a plate", () => {
    for (const s of ["IDLE", "FINISH", "FAILED", "idle"]) expect(printerBusy({ gcode_state: s })).toBeNull();
  });
  it("refuses a busy printer, naming the job", () => {
    expect(printerBusy({ gcode_state: "RUNNING", subtask_name: "sheets-04" })).toBe("the printer is RUNNING (sheets-04)");
    for (const s of ["PAUSE", "PREPARE", "SLICING"]) expect(printerBusy({ gcode_state: s })).not.toBeNull();
  });
  it("refuses a state it cannot read", () => {
    expect(printerBusy({})).toBe("the printer did not report its state");
    expect(printerBusy({ gcode_state: "" })).not.toBeNull();
  });
});
