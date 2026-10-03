import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { type Grader, gradeWithPython, plateApproval, plateNameOf, printerBusy, spendApproval } from "./send-gate.js";

// The send checks (send-gate.ts, D-093). The load-bearing case is the spent approval: a page that was
// approved, then sent and printed, is not approved for the next send, even with its box still ticked
// (sheets-04 on 2026-10-02 was sent from Bambu Studio, which does not untick the box).

let root: string;

function page(name: string, opts: { approved?: string; box?: "x" | " "; rows?: string[]; maturity?: string }): string {
  const fm = [
    "---",
    `plate: ${name}`,
    "stage: waiting",
    `approved: ${opts.approved ? "true" : "false"}`,
    `approved_on: ${opts.approved ?? ""}`,
    `maturity: ${opts.maturity ?? "experiment"}`,
    "---",
  ].join("\n");
  const box = opts.box ? `\n## Your call\n\n- [${opts.box}] **Approve as it stands**\n- [ ] **Hold**\n` : "";
  const rows = (opts.rows ?? ["2026-10-01 | proposed — drawn"]).map((r) => `| ${r} | this page |`);
  const body = `${box}\n## Timeline\n\n| Date | What happened | Where it is written |\n|---|---|---|\n${rows.join("\n")}\n\n## After\n\ntext\n`;
  const path = join(root, "docs", "plates", `${name}.md`);
  writeFileSync(path, `${fm}\n${body}`);
  return path;
}

beforeAll(() => {
  root = mkdtempSync(join(tmpdir(), "send-gate-"));
  mkdirSync(join(root, "docs", "plates"), { recursive: true });
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

  it("refuses an unticked box", () => {
    page("p-unticked", { box: " " });
    expect(plateApproval("p-unticked", root).approved).toBe(false);
  });

  it("takes a first-time tick before it is read back", () => {
    page("p-tick", { box: "x" });
    const a = plateApproval("p-tick", root);
    expect(a.approved).toBe(true);
    expect(a.how).toContain("ticked");
  });

  it("takes a dated approval", () => {
    page("p-fm", { approved: "2026-10-02", box: "x", rows: ["2026-10-01 | proposed", "2026-10-02 | approved — by Omar"] });
    const a = plateApproval("p-fm", root);
    expect(a.approved).toBe(true);
    expect(a.how).toContain("2026-10-02");
  });

  it("refuses an approval spent by a send and a print (the sheets-04 shape, box still ticked)", () => {
    page("p-spent", {
      approved: "2026-10-02",
      box: "x",
      rows: [
        "2026-10-01 | proposed",
        "2026-10-02 | approved — as it stands",
        "2026-10-02 | approved — again",
        "2026-10-02 | sent — by Omar, from Bambu Studio",
        "2026-10-02 | printed — on the X2D",
        "2026-10-02 | judged — pieces fell through",
      ],
    });
    const a = plateApproval("p-spent", root);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("spent");
    expect(a.how).toContain("tick after a send");
    expect(a.sends).toBe(1);
  });

  it("takes a fresh approval after a print, for the reprint", () => {
    page("p-reprint", {
      approved: "2026-10-03",
      rows: ["2026-10-01 | approved", "2026-10-01 | sent", "2026-10-02 | printed", "2026-10-03 | approved — reprint"],
    });
    const a = plateApproval("p-reprint", root);
    expect(a.approved).toBe(true);
    expect(a.how).toContain("send 2");
  });

  it("refuses a plate that went out with no approval at all", () => {
    page("p-legacy", { rows: ["2026-09-25 | sent — before pages existed"] });
    expect(plateApproval("p-legacy", root).approved).toBe(false);
  });
});

// D-095: a production plate goes out on a standing approval, but only when the grader agrees.
// The grader is injected; the real one is plate_grade.py, tested in its own self-test.
const stands: Grader = () => ({ standing: true, why: "its prints still show production" });
const slipped: Grader = () => ({ standing: false, why: "the prints now show repeatable" });
const broken: Grader = () => {
  throw new Error("python3: not found");
};
const sentTwice = ["2026-09-01 | approved", "2026-09-02 | sent", "2026-09-03 | printed", "2026-09-10 | promoted — to production", "2026-09-20 | sent"];

describe("plateApproval on a production plate (D-095)", () => {
  it("sends a production plate the grader still stands behind, with no new yes", () => {
    page("p-prod", { approved: "2026-09-01", maturity: "production", rows: sentTwice });
    const a = plateApproval("p-prod", root, stands);
    expect(a.approved).toBe(true);
    expect(a.standing).toBe(true);
    expect(a.how).toContain("D-095");
  });

  it("refuses a page that says production when the prints no longer do, and says why", () => {
    page("p-slipped", { approved: "2026-09-01", maturity: "production", rows: sentTwice });
    const a = plateApproval("p-slipped", root, slipped);
    expect(a.approved).toBe(false);
    expect(a.standing).toBe(false);
    expect(a.how).toContain("no standing approval: the prints now show repeatable");
  });

  it("refuses when the grader cannot run: a grade it cannot read is not a yes", () => {
    page("p-nograde", { approved: "2026-09-01", maturity: "production", rows: sentTwice });
    const a = plateApproval("p-nograde", root, broken);
    expect(a.approved).toBe(false);
    expect(a.how).toContain("the grade did not run");
  });

  it("still takes a fresh yes on a production plate that lost its standing", () => {
    page("p-slipped-yes", { approved: "2026-09-21", maturity: "production", rows: [...sentTwice, "2026-09-21 | approved — by Omar"] });
    const a = plateApproval("p-slipped-yes", root, slipped);
    expect(a.approved).toBe(true);
    expect(a.standing).toBe(false);
  });

  it("reads the real grader's JSON: a plate in this repo, every one an experiment today", () => {
    const repo = fileURLToPath(new URL("../../../", import.meta.url));
    const s = gradeWithPython("sheets-04b", repo);
    expect(s.standing).toBe(false);
    expect(s.why).toContain("not production");
  });

  it("never asks the grader about an experiment", () => {
    page("p-exp", { box: " " });
    expect(plateApproval("p-exp", root, stands).approved).toBe(false);
  });
});

describe("spendApproval", () => {
  it("leaves a standing approval in place and logs the send as standing", () => {
    const path = page("p-prod-send", { approved: "2026-09-01", box: "x", maturity: "production", rows: sentTwice });
    const before = plateApproval("p-prod-send", root, stands);
    const row = spendApproval(path, "2026-10-03", before);
    const text = readFileSync(path, "utf8");
    expect(row).toContain("standing approval of a production plate");
    expect(text).toMatch(/\[x\] \*\*Approve/);
    expect(plateApproval("p-prod-send", root, stands).approved).toBe(true);
  });

  it("unticks, marks the plate sent, logs the send, and the next send is refused", () => {
    const path = page("p-spend", { approved: "2026-10-03", box: "x", rows: ["2026-10-01 | proposed", "2026-10-03 | approved — by Omar"] });
    const before = plateApproval("p-spend", root);
    expect(before.approved).toBe(true);
    const row = spendApproval(path, "2026-10-03", before);
    const text = readFileSync(path, "utf8");
    expect(text).toContain("stage: sent");
    expect(text).not.toMatch(/\[x\] \*\*Approve/);
    expect(text).toContain(row);
    // the row lands inside the table, before the next section
    expect(text.indexOf(row)).toBeLessThan(text.indexOf("## After"));
    const after = plateApproval("p-spend", root);
    expect(after.approved).toBe(false);
    expect(after.sends).toBe(1);
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
