import { describe, expect, it } from "vitest";
import { Command } from "commander";
import { dumpFlags } from "./flags.js";

// dumpFlags renders the commander tree to the checked-in FLAGS.md; the gate diffs it. These pin the
// contract the gate depends on: the whole visible surface is listed, hidden commands are not, and a
// description with a pipe cannot break the markdown table. A fixture program (not the real CLI) keeps
// the test stable when a real flag is added — that drift is the gate's job, not this test's.
function fixture(): Command {
  const p = new Command();
  p.name("demo").description("a demo CLI").version("9.9.9");
  const grp = p.command("build").description("build things");
  grp
    .command("run")
    .description("run a build | fast")
    .argument("<target>", "what to build")
    .option("--watch", "rebuild on change")
    .option("--jobs <n>", "parallelism | default 1");
  grp.command("secret", { hidden: true }).description("internal use").option("--force", "no prompt");
  return p;
}

describe("dumpFlags — the generated flag reference", () => {
  const out = dumpFlags(fixture());

  it("lists every visible command by full path, in registration order", () => {
    expect(out).toContain("### `demo build`");
    expect(out).toContain("### `demo build run`");
    // `build` heading appears before `build run` (depth-first, registration order).
    expect(out.indexOf("### `demo build`")).toBeLessThan(out.indexOf("### `demo build run`"));
  });

  it("renders the root global options (e.g. --version)", () => {
    expect(out).toContain("### `demo` (global)");
    expect(out).toMatch(/-V, --version/);
  });

  it("renders a command's positional arguments with their required flag", () => {
    expect(out).toMatch(/\| `target` \| yes \| what to build \|/);
  });

  it("renders each option with its flags and description", () => {
    expect(out).toMatch(/\| `--watch` \| rebuild on change \|/);
  });

  it("escapes a pipe in a description so it cannot break the table", () => {
    expect(out).toContain("run a build \\| fast");
    expect(out).toContain("parallelism \\| default 1");
    // Every pipe inside the rendered descriptions is the escaped form (\|), never a bare | that would
    // spill a table column.
    for (const desc of ["run a build \\| fast", "parallelism \\| default 1"]) {
      expect(out).toContain(desc);
    }
    expect(out).not.toContain("run a build | fast");
  });

  it("omits a hidden command and its options entirely", () => {
    expect(out).not.toContain("demo build secret");
    expect(out).not.toContain("--force");
  });

  it("is deterministic — same tree renders byte-identical output", () => {
    expect(dumpFlags(fixture())).toBe(out);
  });

  it("ends with exactly one trailing newline (byte-exact for `git diff`)", () => {
    expect(out.endsWith("\n")).toBe(true);
    expect(out.endsWith("\n\n")).toBe(false);
  });
});
