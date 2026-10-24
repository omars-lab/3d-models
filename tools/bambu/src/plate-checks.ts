// The checks every plate must pass before it is sent (.claude/skills/send-plate/plate-checks.yaml).
// Each entry is a past mistake a script can catch from the plate alone: split-06's bitten ledges,
// minis-05's second bed. `bambu print send` runs every entry that applies, dry run too, and prints
// one ✓/✗ line each; any ✗ refuses a real send. A check that cannot run (its script gone, the
// interpreter missing, a timeout) is a ✗, never a skip, and no flag skips one (Omar 2026-10-24:
// "a hook that blocks prints until they pass validation").
//
// The list is data, read at run time, so a new mistake becomes a new entry and not a code change.
// One parser serves the send and `bambu plate-checks verify` (make validate-plate-checks), so the
// file the gate passed is the file the send reads.

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { parse as parseYaml } from "yaml";

/** Where the list lives, from the repo root. */
export const PLATE_CHECKS_FILE = join(".claude", "skills", "send-plate", "plate-checks.yaml");

/** Which plates an entry runs on, read from the plate's recipe. A closed set: anything else throws. */
export type AppliesRule = { kind: "always" } | { kind: "any_item_bkr_contains"; text: string };

export interface PlateCheck {
  id: string;
  mistake: string;
  source: string;
  applies: AppliesRule;
  command: string;
  pass: string;
  fail: string;
}

/** The parts of a recipe the rules and placeholders read. */
export interface RecipeFacts {
  bkrs: string[]; // every item's bkr
  beds: number; // the recipe's `beds:`, 1 when it sets none
}

export interface CheckResult {
  id: string;
  ok: boolean;
  mark: "✓" | "✗";
  line: string;
  detail: string[]; // the tail of the check's own output, shown under a ✗
}

/** What running one command gave back; `error` is set when it could not start at all. */
export interface RunOutcome {
  status: number | null;
  signal: string | null;
  stdout: string;
  stderr: string;
  error?: Error;
}

export type Runner = (argv: string[], cwd: string) => RunOutcome;

const PLACEHOLDERS = new Set(["plate3mf", "yaml", "beds"]);
const FIELDS = ["id", "mistake", "source", "command", "pass", "fail"] as const;

/** Read one entry's `applies:`. Throws on anything outside the closed set. PURE. */
export function parseApplies(raw: unknown): AppliesRule {
  if (raw === "always") return { kind: "always" };
  if (raw !== null && typeof raw === "object" && !Array.isArray(raw)) {
    const keys = Object.keys(raw);
    const text = (raw as Record<string, unknown>).any_item_bkr_contains;
    if (keys.length === 1 && typeof text === "string" && text.trim() !== "") {
      return { kind: "any_item_bkr_contains", text };
    }
  }
  throw new Error(
    `applies must be \`always\` or { any_item_bkr_contains: "<text>" }, got ${JSON.stringify(raw)}`,
  );
}

/** The command split into words, each placeholder checked. Throws on an unknown one. PURE. */
export function commandWords(command: string): string[] {
  const words = command.trim().split(/\s+/).filter(Boolean);
  if (words.length === 0) throw new Error("command is empty");
  for (const w of words) {
    for (const m of w.matchAll(/\{([^}]*)\}/g)) {
      if (!PLACEHOLDERS.has(m[1] ?? "")) {
        throw new Error(`command names {${m[1]}}; only {plate3mf}, {yaml} and {beds} are filled`);
      }
    }
  }
  return words;
}

/** Parse the list's text. Throws, naming the entry, on the first thing wrong. PURE. */
export function parsePlateChecks(text: string): PlateCheck[] {
  const doc = parseYaml(text) as { checks?: unknown } | null;
  if (!doc || !Array.isArray(doc.checks) || doc.checks.length === 0) {
    throw new Error("the list has no `checks:` entries");
  }
  const seen = new Set<string>();
  return doc.checks.map((raw, i) => {
    const e = (raw ?? {}) as Record<string, unknown>;
    const where = `entry ${i + 1}${typeof e.id === "string" ? ` (${e.id})` : ""}`;
    for (const f of FIELDS) {
      if (typeof e[f] !== "string" || (e[f] as string).trim() === "") throw new Error(`${where}: no \`${f}:\``);
    }
    const id = e.id as string;
    if (seen.has(id)) throw new Error(`${where}: id ${id} is used twice`);
    seen.add(id);
    try {
      commandWords(e.command as string);
      return {
        id,
        mistake: e.mistake as string,
        source: e.source as string,
        applies: parseApplies(e.applies),
        command: e.command as string,
        pass: e.pass as string,
        fail: e.fail as string,
      };
    } catch (err) {
      throw new Error(`${where}: ${(err as Error).message}`);
    }
  });
}

export function loadPlateChecks(root: string): PlateCheck[] {
  return parsePlateChecks(readFileSync(join(root, PLATE_CHECKS_FILE), "utf8"));
}

/** The recipe's items and beds; a plate with no recipe has no items and one bed. */
export function readRecipeFacts(recipe: string): RecipeFacts {
  if (!existsSync(recipe)) return { bkrs: [], beds: 1 };
  const doc = parseYaml(readFileSync(recipe, "utf8")) as { items?: unknown; beds?: unknown } | null;
  const items = Array.isArray(doc?.items) ? doc!.items : [];
  const bkrs = items
    .map((it) => (it && typeof it === "object" ? (it as { bkr?: unknown }).bkr : undefined))
    .filter((b): b is string => typeof b === "string");
  const beds = typeof doc?.beds === "number" && Number.isInteger(doc.beds) && doc.beds >= 1 ? doc.beds : 1;
  return { bkrs, beds };
}

/** Does this entry run on this plate? PURE. */
export function applies(rule: AppliesRule, facts: RecipeFacts): boolean {
  if (rule.kind === "always") return true;
  return facts.bkrs.some((b) => b.includes(rule.text));
}

/** The words in an entry's command that name a file in the repo: each must exist. PURE. */
export function scriptsNamed(check: PlateCheck): string[] {
  return commandWords(check.command).filter((w) => w.includes("/") && !w.includes("{"));
}

/** The make target's check: the list parses, and every file it names is there. */
export function verifyPlateChecks(root: string): string[] {
  let checks: PlateCheck[];
  try {
    checks = loadPlateChecks(root);
  } catch (err) {
    return [`${PLATE_CHECKS_FILE}: ${(err as Error).message}`];
  }
  const problems: string[] = [];
  for (const c of checks) {
    for (const s of scriptsNamed(c)) {
      if (!existsSync(join(root, s))) problems.push(`${c.id}: names ${s}, which is not in the repo`);
    }
    if (!existsSync(join(root, c.source))) problems.push(`${c.id}: its source ${c.source} is not in the repo`);
  }
  return problems;
}

export const spawnRunner: Runner = (argv, cwd) => {
  const r = spawnSync(argv[0] ?? "", argv.slice(1), { cwd, encoding: "utf8", timeout: 180_000 });
  return { status: r.status, signal: r.signal, stdout: r.stdout ?? "", stderr: r.stderr ?? "", error: r.error };
};

function tail(out: RunOutcome, n = 4): string[] {
  return `${out.stdout}\n${out.stderr}`
    .split("\n")
    .map((l) => l.trimEnd())
    .filter((l) => l.trim() !== "")
    .slice(-n);
}

/** Run one entry against one plate. */
export function runCheck(
  check: PlateCheck,
  vals: { plate3mf: string; yaml: string; beds: number },
  root: string,
  run: Runner = spawnRunner,
): CheckResult {
  const bad = (reason: string, detail: string[] = []): CheckResult => ({
    id: check.id,
    ok: false,
    mark: "✗",
    line: `${check.id}: ${reason} [the mistake: ${check.mistake}]`,
    detail,
  });
  let argv: string[];
  try {
    argv = commandWords(check.command).map((w) =>
      w.replace(/\{(plate3mf|yaml|beds)\}/g, (_, k: "plate3mf" | "yaml" | "beds") => String(vals[k])),
    );
  } catch (err) {
    return bad(`could not run (${(err as Error).message})`);
  }
  const missing = scriptsNamed(check).filter((s) => !existsSync(join(root, s)));
  if (missing.length > 0) return bad(`could not run: ${missing.join(", ")} is not in the repo`);
  const out = run(argv, root);
  if (out.error) return bad(`could not run (${out.error.message})`);
  if (out.signal) return bad(`stopped by ${out.signal} before it finished`, tail(out));
  if (out.status !== 0) return bad(`failed (exit ${out.status}): ${check.fail}`, tail(out));
  return { id: check.id, ok: true, mark: "✓", line: `${check.id}: ${check.pass}`, detail: [] };
}

/** Every entry that applies to this plate, run in list order. An entry that does not apply is not
 * a result: the send prints only what ran. */
export function runPlateChecks(
  checks: PlateCheck[],
  plate3mf: string,
  recipe: string,
  root: string,
  run: Runner = spawnRunner,
): CheckResult[] {
  const facts = readRecipeFacts(recipe);
  return checks
    .filter((c) => applies(c.applies, facts))
    .map((c) => runCheck(c, { plate3mf, yaml: recipe, beds: facts.beds }, root, run));
}
