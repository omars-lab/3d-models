// Structured, greppable logging + subprocess timeout wrapper.
//
// Global CLAUDE.md observability tenet: long/blocking calls emit one line BEFORE and one AFTER,
// each `ev=<event> key=value` with a UTC timestamp and pid, free text in a quoted msg="...".
// Any subprocess that can hang gets a timeout that logs `ev=*_timeout` and recovers.

import { appendFileSync, mkdirSync } from "node:fs";
import { spawn } from "node:child_process";
import { dirname } from "node:path";

const LOG_PATH = process.env.BAMBU_LOG ?? `${process.cwd()}/.bambu/bambu.log`;

function ts(): string {
  return new Date().toISOString();
}

/** Emit one structured event line to the log file (best-effort) and, when verbose, to stderr. */
export function ev(event: string, fields: Record<string, string | number | boolean> = {}): void {
  const parts = [`ts=${ts()}`, `pid=${process.pid}`, `ev=${event}`];
  for (const [k, v] of Object.entries(fields)) {
    // Keys/values are space-free; free text goes in a quoted msg="..." by the caller.
    parts.push(`${k}=${v}`);
  }
  const line = parts.join(" ") + "\n";
  try {
    mkdirSync(dirname(LOG_PATH), { recursive: true });
    appendFileSync(LOG_PATH, line);
  } catch {
    /* logging is best-effort; never let it break a command */
  }
  if (process.env.BAMBU_VERBOSE) process.stderr.write(line);
}

export interface RunResult {
  code: number | null;
  stdout: string;
  stderr: string;
  timedOut: boolean;
}

/**
 * Run a subprocess with a hard timeout. Brackets the call with ev=proc_start / ev=proc_done,
 * and on timeout kills the child and logs ev=proc_timeout so a stall is visible in the log
 * and cannot freeze the run.
 */
export function runWithTimeout(
  cmd: string,
  args: string[],
  opts: { timeoutMs?: number; cwd?: string; env?: NodeJS.ProcessEnv; label?: string } = {},
): Promise<RunResult> {
  const timeoutMs = opts.timeoutMs ?? 30_000;
  const label = opts.label ?? cmd;
  return new Promise((resolve) => {
    ev("proc_start", { label, timeout_ms: timeoutMs });
    const child = spawn(cmd, args, { cwd: opts.cwd, env: opts.env ?? process.env });
    let stdout = "";
    let stderr = "";
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      ev("proc_timeout", { label, timeout_ms: timeoutMs });
      child.kill("SIGKILL");
    }, timeoutMs);
    child.stdout?.on("data", (d) => (stdout += d.toString()));
    child.stderr?.on("data", (d) => (stderr += d.toString()));
    child.on("error", (err) => {
      clearTimeout(timer);
      ev("proc_error", { label, msg: `"${String(err.message).replace(/"/g, "'")}"` });
      resolve({ code: null, stdout, stderr: stderr || String(err.message), timedOut });
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      ev("proc_done", { label, code: code ?? "null", timed_out: timedOut });
      resolve({ code, stdout, stderr, timedOut });
    });
  });
}
