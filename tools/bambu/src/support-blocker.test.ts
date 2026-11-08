import { describe, expect, it } from "vitest";
import {
  blockersByName,
  blockersMissing,
  checkSupportBlocker,
  injectSupportBlockers,
  sphereFit,
} from "./support-blocker.js";
import { parseManifest } from "./commands/compose.js";

/** A hollow ball's two faces as vertices: an outer and an inner ring of points at radius 20 and 17.6. */
function shellPoints(c: [number, number, number]): string {
  const out: string[] = [];
  for (const r of [20, 17.6]) {
    for (let i = 1; i < 12; i++) {
      for (let j = 0; j < 24; j++) {
        const th = (Math.PI * i) / 12;
        const ph = (2 * Math.PI * j) / 24;
        const [x, y, z] = [c[0] + r * Math.sin(th) * Math.cos(ph), c[1] + r * Math.sin(th) * Math.sin(ph), c[2] + r * Math.cos(th)];
        out.push(`     <vertex x="${x}" y="${y}" z="${z}"/>`);
      }
    }
  }
  return out.join("\n");
}

/** An arranged plate as Studio writes one: the ball's mesh centred in its own file, the root object's
 *  component carrying the offset, and the object's name in model_settings.config. */
function arranged() {
  const meshes = new Map([
    [
      "/3D/Objects/object_1.model",
      `<model xmlns:p="x">\n <resources>\n  <object id="1" p:UUID="u1" type="model">\n   <mesh>\n    <vertices>\n${shellPoints([0, 0, 0])}\n    </vertices>\n   </mesh>\n  </object>\n </resources>\n</model>\n`,
    ],
  ]);
  const rootModel =
    `<model>\n <resources>\n  <object id="2" p:UUID="u2" type="model">\n   <components>\n` +
    `    <component p:path="/3D/Objects/object_1.model" objectid="1" p:UUID="u3" transform="1 0 0 0 1 0 0 0 1 92 89 19.7"/>\n` +
    `   </components>\n  </object>\n </resources>\n <build>\n  <item objectid="2" transform="1 0 0 0 1 0 0 0 1 10 140 0"/>\n </build>\n</model>\n`;
  const settingsXml =
    `<config>\n  <object id="2">\n    <metadata key="name" value="it-abc.stl"/>\n    <metadata key="extruder" value="1"/>\n` +
    `    <part id="1" subtype="normal_part">\n      <metadata key="name" value="ball"/>\n    </part>\n  </object>\n</config>\n`;
  return { rootModel, settingsXml, meshes };
}

describe("support blocker — a sphere inside a hollow piece where no support grows", () => {
  it("fits a sphere's centre and radius from its points", () => {
    const pts: [number, number, number][] = [];
    for (let i = 0; i < 200; i++) {
      const th = Math.acos(1 - (2 * (i + 0.5)) / 200);
      const ph = i * 2.399963;
      pts.push([5 + 9 * Math.sin(th) * Math.cos(ph), -3 + 9 * Math.sin(th) * Math.sin(ph), 7 + 9 * Math.cos(th)]);
    }
    const f = sphereFit(pts);
    expect(f.centre[0]).toBeCloseTo(5, 6);
    expect(f.centre[1]).toBeCloseTo(-3, 6);
    expect(f.centre[2]).toBeCloseTo(7, 6);
    expect(f.radius).toBeCloseTo(9, 6);
  });

  it("adds the sphere at the piece's own centre, through its component's transform, with a blocker part", () => {
    const a = arranged();
    const out = injectSupportBlockers(a.rootModel, a.settingsXml, a.meshes, new Map([["it-abc.stl", { radius_mm: 18.6 }]]));
    expect(out.placed).toHaveLength(1);
    const p = out.placed[0]!;
    expect(p.centre[0]).toBeCloseTo(92, 3);
    expect(p.centre[1]).toBeCloseTo(89, 3);
    expect(p.centre[2]).toBeCloseTo(19.7, 3);
    expect(p.inner).toBeCloseTo(17.6, 3);
    // A new mesh object, past every id in either file, in the ball's own mesh file …
    const mesh = out.meshes.get("/3D/Objects/object_1.model")!;
    expect(mesh).toMatch(/<object id="3" p:UUID="[^"]+" type="model">/);
    // … a second component naming it, unmoved, and the first one untouched …
    expect(out.rootModel).toMatch(/objectid="3" p:UUID="[^"]+" transform="1 0 0 0 1 0 0 0 1 0 0 0"\/>/);
    expect(out.rootModel).toContain('objectid="1" p:UUID="u3" transform="1 0 0 0 1 0 0 0 1 92 89 19.7"');
    // … and the part line that tells Studio it blocks support.
    expect(out.settingsXml).toMatch(/<part id="3" subtype="support_blocker">/);
    expect(blockersMissing(blockersByName(out.settingsXml), [{ name: "it-abc.stl", count: 1 }])).toEqual([]);
    // The sphere's vertices sit at the radius from the fit centre, in the object's frame.
    const v = [...mesh.split('<object id="3"')[1]!.matchAll(/x="([^"]*)" y="([^"]*)" z="([^"]*)"/g)].map((m) => m.slice(1).map(Number));
    for (const [x, y, z] of v.slice(0, 50)) expect(Math.hypot(x! - 92, y! - 89, z! - 19.7)).toBeCloseTo(18.6, 3);
  });

  it("refuses a radius that would reach the piece's outer face and stop the support under it", () => {
    const a = arranged();
    expect(() => injectSupportBlockers(a.rootModel, a.settingsXml, a.meshes, new Map([["it-abc.stl", { radius_mm: 19.5 }]]))).toThrow(
      /within 1 mm of the piece's outer face/,
    );
  });

  it("refuses a name that matches no object", () => {
    const a = arranged();
    expect(() => injectSupportBlockers(a.rootModel, a.settingsXml, a.meshes, new Map([["it-zzz.stl", { radius_mm: 10 }]]))).toThrow(
      /no object named it-zzz.stl/,
    );
  });

  it("the read-back fails a slice that dropped the blocker, and one where another piece grew one", () => {
    const a = arranged();
    expect(blockersMissing(blockersByName(a.settingsXml), [{ name: "it-abc.stl", count: 1 }])).toEqual([
      "it-abc.stl: blockers per object in the slice are 0, the recipe asks for 1",
    ]);
    const out = injectSupportBlockers(a.rootModel, a.settingsXml, a.meshes, new Map([["it-abc.stl", { radius_mm: 18.6 }]]));
    expect(blockersMissing(blockersByName(out.settingsXml), [])).toEqual([
      "it-abc.stl: carries a support blocker in the slice, the recipe asks for none",
    ]);
  });

  it("the recipe takes radius_mm on an stl: item only", () => {
    expect(checkSupportBlocker({ radius_mm: 18.6 }, "items[0]")).toEqual({ radius_mm: 18.6 });
    expect(() => checkSupportBlocker({ sphere_mm: 18.6 }, "items[0]")).toThrow(/not a blocker setting/);
    expect(() => checkSupportBlocker({ radius_mm: 0 }, "items[0]")).toThrow(/above 0/);
    const sha = "a".repeat(64);
    const ok = parseManifest(`items:\n  - stl: .bambu/imports/b.stl\n    sha256: ${sha}\n    support_blocker: { radius_mm: 18.6 }\n`);
    expect((ok.items[0] as { support_blocker?: unknown }).support_blocker).toEqual({ radius_mm: 18.6 });
    expect(() => parseManifest(`items:\n  - bkr: "bikar:a.bkr"\n    support_blocker: { radius_mm: 5 }\n`)).toThrow(
      /only an `stl:` item takes `support_blocker:`/,
    );
  });
});
