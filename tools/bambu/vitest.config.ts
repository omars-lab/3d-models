import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { defineConfig } from "vitest/config";

// The source uses NodeNext ".js" import specifiers that resolve to ".ts" files on disk (so `tsc`
// stays happy). Vite's default resolver does not rewrite them, so this tiny pre-plugin maps a
// relative "*.js" import to its "*.ts" sibling when that exists — keeping ONE spelling of the
// imports across the typechecker and the test runner.
export default defineConfig({
  plugins: [
    {
      name: "nodenext-js-to-ts",
      enforce: "pre",
      resolveId(source: string, importer?: string) {
        if (importer && source.startsWith(".") && source.endsWith(".js")) {
          const candidate = resolve(dirname(importer), source.slice(0, -3) + ".ts");
          if (existsSync(candidate)) return candidate;
        }
        return null;
      },
    },
  ],
  test: { include: ["src/**/*.test.ts"], environment: "node" },
});
