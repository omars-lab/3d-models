// The two checks `print send` makes before anything reaches the printer, kept apart so they can be
// tested without a printer:
//
//   - Approval (D-093, D-096). Omar's yes to a send is a row in the `## Approvals` table on the
//     plate's page in docs/design/plates/. He ticks the Approve box in Obsidian, or says yes in chat,
//     and the manage-approvals skill's `plate_approve.py` turns that into a dated row naming who said
//     yes and what it covers: an iteration of the recipe and the master commit holding it (D-097). A
//     plate with no page has nowhere to say yes, so it does not go out.
//
//     One approval is good for one send: the send fills the open row's `Spent by`, so a reprint
//     needs a new row, and the table holds every yes the design was ever given. A recipe changed
//     after the yes is not approved: recording the change (`--iterate`) resets the yes, and Omar is
//     asked again; a comment-only edit is not a change, so a reprint as-is keeps its yes. A ticked
//     box nobody has recorded yet does not count: a box ticked before a send made outside this CLI
//     looks just like a fresh one, so the tick is read back into a row first.
//
//     A production plate has a standing approval (D-095): its promotion wrote a `standing` row, its
//     prints still show production and its recipe is the one it was promoted on. It goes out with no
//     new yes, and the send spends nothing. A plate that slipped falls back to the one-per-send rule.
//
//     Both halves are `plate_approve.py` (`--status --json` before, `--sent` after), which reads the
//     table with the plates gate's own parser, so the send and the gate cannot disagree. A tool that
//     does not run is a refusal.
//   - Idle. A send while another print runs would queue over it or fail on the printer; the state
//     comes off the same status read the filament match already makes. A state we cannot read is a
//     refusal, not a pass.

import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { PrinterStatus } from "./backends/mqtt.js";

/** `build/plates/sheets-04b.plate.3mf` → `sheets-04b`: the name its page in docs/design/plates/ carries. */
export function plateNameOf(plateFile: string): string {
  return basename(plateFile).replace(/\.3mf$/i, "").replace(/\.plate$/i, "");
}

export function platePagePath(name: string, root: string): string {
  return join(root, "docs", "design", "plates", `${name}.md`);
}

export interface Approval {
  page: string; // where the page is, or would be
  exists: boolean;
  approved: boolean;
  how: string; // what said yes, or why not
  sends: number; // how many times the timeline says it went out
  standing: boolean; // a production plate's standing approval (D-095), not spent by a send
  recipe: string | null; // the plate's recipe hash now (iterations.py), or null with no recipe
  color: string | null; // the one color the open yes covers ("#RRGGBB"), or null when it names none
  iteration: number | null; // the recipe's iteration when it is the latest recorded one, else null (D-109)
}

/** Runs the manage-approvals skill's `plate_approve.py` with these arguments and returns its stdout;
 * throws on a refusal. */
export type ApproveTool = (args: string[]) => string;

const TOOL = fileURLToPath(
  new URL("../../../.claude/skills/manage-approvals/scripts/plate_approve.py", import.meta.url),
);

export const plateApproveTool: ApproveTool = (args) =>
  execFileSync("python3", [TOOL, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });

function lastLine(err: unknown): string {
  const e = err as { stderr?: string; message?: string };
  return String(e.stderr || e.message || err).trim().split("\n").pop() ?? "";
}

/** Is this plate approved for its next send? What its page's Approvals table says, read by the tool. */
export function plateApproval(name: string, root: string, tool: ApproveTool = plateApproveTool): Approval {
  const page = platePagePath(name, root);
  const no = (how: string): Approval => ({
    page,
    exists: existsSync(page),
    approved: false,
    how,
    sends: 0,
    standing: false,
    recipe: null,
    color: null,
    iteration: null,
  });
  if (!existsSync(page)) return no("no plate page, so nothing to approve");
  try {
    const st = JSON.parse(tool([page, "--status", "--json"])) as Record<string, unknown>;
    return {
      page,
      exists: true,
      approved: st.approved === true,
      how: String(st.how ?? ""),
      sends: Number(st.sends ?? 0),
      standing: st.standing === true,
      recipe: typeof st.recipe === "string" ? st.recipe : null,
      color: typeof st.color === "string" ? st.color : null,
      iteration: typeof st.iteration === "number" ? st.iteration : null,
    };
  } catch (err) {
    return no(`plate_approve.py did not read the page: ${lastLine(err)}`);
  }
}

/** The recipe hash a slice verb records beside the plate it wrote (slice-fresh.ts): the same
 * `plate_approve.py --status` read the send makes, so the two sides cannot hash differently. Null for
 * a plate with no page or no recipe. */
export function recipeHashOf(plate: string, root: string, tool: ApproveTool = plateApproveTool): string | null {
  return plateApproval(plateNameOf(plate), root, tool).recipe;
}

/** The iteration number a plate's recipe is now, for the id cut into each piece (D-109), from the
 * same `plate_approve.py --status` read. Throws, naming the fix, when the recipe as it is has no
 * recorded iteration: an id that names the wrong iteration is worse than no print. */
export function recipeIterationOf(name: string, root: string, tool: ApproveTool = plateApproveTool): number {
  const a = plateApproval(name, root, tool);
  if (!a.exists) throw new Error(`${name} has no plate page (${a.page}), so no iteration to cut into its ids`);
  if (a.iteration === null) {
    throw new Error(
      `${name}'s recipe as it is now is not a recorded iteration, so its pieces cannot carry one: ` +
        `\`python3 .claude/skills/manage-approvals/scripts/plate_approve.py ${name} --iterate\`` +
        (a.recipe === null ? ` (${a.how})` : ""),
    );
  }
  return a.iteration;
}

/**
 * Spend the approval on a successful send: the open row's `Spent by` becomes `sent <date>`, the box is
 * unticked, the stage is `sent` and a dated `sent` row joins the timeline. A standing approval (D-095)
 * spends nothing; the row says the plate went out on it. Returns the timeline row; the page is
 * rewritten in place and the caller ships it like any doc change.
 */
export function spendApproval(page: string, date: string, approval: Approval, tool: ApproveTool = plateApproveTool): string {
  const args = [page, "--sent", "--date", date, "--via", "`bambu print send`"];
  try {
    return tool(approval.standing ? [...args, "--standing"] : args).trim();
  } catch (err) {
    throw new Error(lastLine(err));
  }
}

// What the X2D reports as gcode_state when nothing is printing. Anything else (RUNNING, PAUSE,
// PREPARE, SLICING, …) means the machine is busy.
const IDLE_STATES = new Set(["IDLE", "FINISH", "FAILED"]);

/** Why the printer cannot take a plate now, or null when it is idle. */
export function printerBusy(frame: PrinterStatus): string | null {
  const raw = frame.gcode_state;
  if (raw === undefined || raw === null || String(raw).trim() === "") {
    return "the printer did not report its state";
  }
  const state = String(raw).trim().toUpperCase();
  if (IDLE_STATES.has(state)) return null;
  const job = frame.subtask_name ? ` (${String(frame.subtask_name)})` : "";
  return `the printer is ${state}${job}`;
}
