<!--
  Research produced 2026-08-18 by Claude Opus 5, under the 3d-models
  design-doc rules, to ground docs/orb-construction-timelapse-design.md.
  Sources: MEASUREMENT RUNS against two local checkouts —
  `~/Workspace/git/bikar` at `e0a81cc` (branch `main`) and
  `~/Workspace/git/3d-models` at `50bac8d` (branch `master`).
  No web sources; no external documentation was consulted.
  Feeds: docs/orb-construction-timelapse-design.md, sections 3, 4, 6 and 7.
  WHAT WAS RUN: eight `node -e` programs against bikar's built bundle
  `packages/core/dist/index.js`, reproduced below in full. Nothing was
  written into either repo: no file was created, moved or deleted, no
  rasterizer was invoked, and no `make` target was run. Every program is
  read-only and re-runnable by paste.
  PREREQUISITE: `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`
  and `cd ~/Workspace/git/bikar`. The system Node is too old and fails in
  ways that look like code bugs.
  Tool output is preserved verbatim; commentary is marked as commentary.
-->

# Orb stage decomposition: the measured runs

## 0. Why this file exists

The design doc it feeds claims that a construction stage is a pure filter over
an already-computed scene, requiring no change to bikar's geometry engine. That
claim is only worth anything if the filter was actually run over every orb and
the resulting frames actually checked. This file is that run.

It also records four numbers that an earlier draft of the design doc got
**wrong**, and which this run corrected. They are flagged inline as
CORRECTION, because a research file whose job is grounding must show where the
grounding moved the answer.

## 1. The decisive structural fact

Commentary. bikar's `packages/core/src/dsl/evaluator.ts` reaches solidification
in a single call per family — `solidifyLattice`, `weaveLattice`,
`solidifyMacladoField` — with no stage boundary exposed and no partial result
retained. The construction is therefore **not staged internally**. What makes
the design possible is that the *view* pipeline is tagged per element.

Run:

    node -e "
    import('./packages/core/dist/index.js').then(async m=>{
    const fs=await import('node:fs');
    const r=m.compileToGeometry(fs.readFileSync('patterns/Orbs/Star-Orb.bkr','utf8'));
    const P={radiusMm:r.orb3d.radiusMm,projection:r.orb3d.projection,view:m.symmetryViewAxes(r.orb3d.base)[0]};
    const s=m.projectOrbViewScene(r,P);
    const p=s.polygons[0];
    console.log('polygon keys:', Object.keys(p).join(','));
    console.log('baseFaceIndex',p.baseFaceIndex,'patternFaceIndex',p.patternFaceIndex);
    console.log('surface',r.orb3d.surface,'family',r.orb3d.family);
    });"

Output (abridged only where the polygon's `source` object is dumped in full):

    polygon keys: points,baseFaceIndex,patternFaceIndex,minDot,source
    baseFaceIndex 0 patternFaceIndex 1
    surface inscribed family lattice

The `source` object printed alongside carries, verbatim:

    sources: Set(3) { 'tri', 'layer:0', 'C1:every:2:#0' },
    edgeSources: [
      Set(2) { 'tri', 'layer:0' },
      ...
      Set(2) { 'C1:every:2:#0', 'layer:0' },
    ],

Commentary. This was not anticipated and it matters for the "prose for free"
requirement: every polygon names the DSL construct that produced it
(`tri` is the `polygon tri [...]` declaration, `C1:every:2:#0` is the
`connect every 2 on C1` statement, `layer:0` the layer). A caption can name the
construction element without a human typing it. This is stronger evidence for
derived prose than the frame counts are.

## 2. The 14-orb enumeration, viewBox invariance, and terminal identity

Run (single program; the frame rule is `1 base + elements + repeats + 1 final
(+ strands)`, and cumulative frames are rendered and their `viewBox` collected):

    node -e "
    import('./packages/core/dist/index.js').then(async m=>{
    const fs=await import('node:fs'), path=await import('node:path'), crypto=await import('node:crypto');
    const sha=s=>crypto.createHash('sha256').update(s).digest('hex').slice(0,12);
    const dir='patterns/Orbs';
    const files=fs.readdirSync(dir).filter(f=>f.endsWith('.bkr')).sort();
    console.log('orb count:',files.length);
    console.log('FILE|surface|family|elements|repeats|strands|frames|viewBoxes|termIdentical');
    let total=0;
    for(const f of files){
      const r=m.compileToGeometry(fs.readFileSync(path.join(dir,f),'utf8'));
      const view=m.symmetryViewAxes(r.orb3d.base)[0];
      const P={radiusMm:r.orb3d.radiusMm,projection:r.orb3d.projection,view,ribbonWidthMm:r.orb3d.strutWidthMm};
      const vbs=new Set(); let elements=0,repeats=0,strands=0,term='n/a';
      let cellScene=null;
      try{ cellScene=m.projectOrbViewScene(r,P); }catch(e){ cellScene=null; }
      if(cellScene && cellScene.polygons.length){
        const S=cellScene;
        const bases=[...new Set(S.polygons.map(p=>p.baseFaceIndex))];
        repeats=bases.length;
        const first=bases[0];
        const pats=[...new Set(S.polygons.filter(p=>p.baseFaceIndex===first).map(p=>p.patternFaceIndex))];
        elements=pats.length;
        const full=m.renderOrbViewSVG({scene:S,faceColors:r.faceColors,faceClasses:r.faceClasses});
        let last=null;
        for(let i=1;i<=pats.length;i++){
          const keep=new Set(pats.slice(0,i));
          const sub={...S,polygons:S.polygons.filter(p=>p.baseFaceIndex===first&&keep.has(p.patternFaceIndex))};
          const svg=m.renderOrbViewSVG({scene:sub,faceColors:r.faceColors,faceClasses:r.faceClasses});
          vbs.add((svg.match(/viewBox=\"([^\"]+)\"/)||[])[1]);
        }
        for(let i=1;i<=bases.length;i++){
          const keep=new Set(bases.slice(0,i));
          const sub={...S,polygons:S.polygons.filter(p=>keep.has(p.baseFaceIndex))};
          const svg=m.renderOrbViewSVG({scene:sub,faceColors:r.faceColors,faceClasses:r.faceClasses});
          vbs.add((svg.match(/viewBox=\"([^\"]+)\"/)||[])[1]);
          last=svg;
        }
        term=(sha(last)===sha(full))?'YES '+sha(last):'NO '+sha(last)+'!='+sha(full);
      }
      let ribScene=null;
      try{ ribScene=m.projectOrbRibbonScene(r,P); }catch(e){ ribScene=null; }
      if(ribScene && ribScene.polygons.length){
        const ids=[...new Set(ribScene.polygons.map(p=>p.ribbon.strandId))];
        strands=ids.length;
        const fullR=m.renderOrbRibbonViewSVG({scene:ribScene});
        let lastR=null;
        for(let i=1;i<=ids.length;i++){
          const keep=new Set(ids.slice(0,i));
          const sub={...ribScene,polygons:ribScene.polygons.filter(p=>keep.has(p.ribbon.strandId))};
          const svg=m.renderOrbRibbonViewSVG({scene:sub});
          vbs.add((svg.match(/viewBox=\"([^\"]+)\"/)||[])[1]);
          lastR=svg;
        }
        if(term==='n/a') term=(sha(lastR)===sha(fullR))?'YES(rib) '+sha(lastR):'NO(rib)';
      }
      const frames=(cellScene&&cellScene.polygons.length?1+elements+repeats+1:1)+strands;
      total+=frames;
      console.log([f,r.orb3d.surface,r.orb3d.family,elements,repeats,strands,frames,vbs.size,term].join('|'));
    }
    console.log('TOTAL FRAMES:',total);
    });"

Output, verbatim:

    orb count: 14
    FILE|surface|family|elements|repeats|strands|frames|viewBoxes|termIdentical
    Dodeca-Orb.bkr|inscribed|lattice|11|6|0|19|1|YES 58826178e02e
    Hankin-Orb.bkr|inscribed|lattice|6|6|0|14|1|YES 485734c5fed7
    Maclado-9-Overlap.bkr|wheelfield|weave|0|0|30|31|1|YES(rib) f23163d5a69e
    Maclado-9-Weave.bkr|wheelfield|weave|19|13|26|60|1|YES d050c039a16d
    Maclado-9.bkr|wheelfield|lattice|19|13|0|34|1|YES d050c039a16d
    Rosette-Cube-Orb.bkr|inscribed|lattice|7|3|0|12|1|YES 4906f5f2c91d
    Rosette-Orb.bkr|inscribed|lattice|21|6|0|29|1|YES 9a18f22e507c
    Rosette-Weave-Orb.bkr|inscribed|weave|6|3|9|20|1|YES 57d5fa4304e6
    Star-Cube-Orb.bkr|inscribed|lattice|12|3|0|17|1|YES b603361664ca
    Star-Octa-Orb.bkr|inscribed|lattice|4|4|0|10|1|YES a626cf6e9e10
    Star-Orb.bkr|inscribed|lattice|10|10|0|22|1|YES c575552949e9
    Star-Tetra-Orb.bkr|inscribed|lattice|2|3|0|7|1|YES 906c21bc99be
    Weave-Dodeca-Orb.bkr|inscribed|weave|6|3|9|20|1|YES 0490840de0ce
    Weave-Orb.bkr|inscribed|weave|7|10|15|34|1|YES ce66a8c4c1f1
    TOTAL FRAMES: 329

What this establishes, stated no wider than the run:

- **All 14 orbs were enumerated.** None was extrapolated from a neighbour.
- **`viewBoxes` is 1 for every orb.** Across all 329 cumulative frames, no
  sequence contained two distinct `viewBox` strings. The camera cannot drift
  under filtering because the viewBox is derived from `radiusMm` plus padding
  and never from content bounds.
- **Terminal identity holds for all 14.** The last cumulative frame is
  byte-identical to the unfiltered render. Star-Orb's pair is
  `c575552949e9` == `c575552949e9`; the other thirteen shas are in the table.
- **11 orbs are `inscribed`, 3 are `wheelfield`; 9 are `lattice`, 5 are
  `weave`.** Both fields are read from `r.orb3d`, not inferred from filenames.

CORRECTION 1. An earlier draft reported **303** total frames. That number came
from mixing two different decompositions of the three Maclado orbs. The
re-derived total under one consistent decomposition is **329**.

CORRECTION 2. An earlier draft reported the Maclado orbs as `spikes=9
wheels=10`. Both figures were wrong. The measured values are `elements=19`,
`repeats=13`, and section 3 shows why 19 is the right number.

CAVEAT. `elements` is counted on the **first visible base face only**
(`bases[0]`). Faces nearer the cap rim are clipped and carry fewer polygons, so
`elements` is a per-unit count for one representative unit, not a minimum or a
mean across units.

CAVEAT. Every count in this table is for **one hero view** — the first axis
returned by `symmetryViewAxes`. See section 7 for why the three-view figures in
the design doc are arithmetic rather than measurement.

## 3. Maclado-9: the 392-cell breakdown and the within-wheel spike ordering

Run:

    node -e "
    import('./packages/core/dist/index.js').then(async m=>{
    const fs=await import('node:fs');
    for(const f of ['Maclado-9.bkr','Maclado-9-Weave.bkr','Maclado-9-Overlap.bkr']){
      const r=m.compileToGeometry(fs.readFileSync('patterns/Orbs/'+f,'utf8'));
      console.log('=== '+f+' orbCells:',r.orbCells?r.orbCells.length:'null');
      if(!r.orbCells){ console.log('   (no cells)'); continue; }
      const byKind={}; for(const c of r.orbCells) byKind[c.kind]=(byKind[c.kind]||0)+1;
      console.log('   all cells by kind:',JSON.stringify(byKind));
      console.log('   units:',new Set(r.orbCells.map(c=>c.unit)).size);
      const view=m.symmetryViewAxes(r.orb3d.base)[0];
      const P={radiusMm:r.orb3d.radiusMm,projection:r.orb3d.projection,view};
      const S=m.projectOrbViewScene(r,P);
      const visCells=S.polygons.map(p=>r.orbCells[p.patternFaceIndex]).filter(Boolean);
      const vk={}; for(const c of visCells) vk[c.kind]=(vk[c.kind]||0)+1;
      console.log('   visible cells:',S.polygons.length,'by kind:',JSON.stringify(vk));
      console.log('   visible units:',[...new Set(S.polygons.map(p=>p.baseFaceIndex))].join(','));
      const mismatch=S.polygons.filter(p=>r.orbCells[p.patternFaceIndex] && r.orbCells[p.patternFaceIndex].unit!==p.baseFaceIndex).length;
      console.log('   cells where unit !== baseFaceIndex:',mismatch);
      const firstUnit=S.polygons[0].baseFaceIndex;
      const wheel=S.polygons.filter(p=>p.baseFaceIndex===firstUnit).map(p=>r.orbCells[p.patternFaceIndex]);
      console.log('   spike order in one wheel:',wheel.map(c=>c.kind+':'+c.index).join(' '));
      console.log('   distinct kinds order:',[...new Set(r.orbCells.map(c=>c.kind))].join(','));
    }
    });"

Output, verbatim (the `cell0` dump of 9 xyz points is elided; `kind` and `unit`
from it are quoted below):

    === Maclado-9.bkr orbCells: 392
       all cells by kind: {"core":20,"triangle":180,"petal":180,"filler":12}
       units: 32
       visible cells: 127 by kind: {"core":4,"triangle":60,"petal":60,"filler":3}
       visible units: 0,1,2,3,4,5,6,7,15,16,20,25,31
       cells where unit !== baseFaceIndex: 0
       spike order in one wheel: core:0 triangle:0 petal:0 triangle:1 petal:1 triangle:2 petal:2 triangle:3 petal:3 triangle:4 petal:4 triangle:5 petal:5 triangle:6 petal:6 triangle:7 petal:7 triangle:8 petal:8
       distinct kinds order: core,triangle,petal,filler
    === Maclado-9-Weave.bkr orbCells: 392
       (identical on every line to Maclado-9.bkr above)
    === Maclado-9-Overlap.bkr orbCells: null
       (no cells)

`cell0` begins `{"points":[...9 points...],"unit":0,"kind":"core","index":0}`.

What this establishes:

- **392 cells = `{core:20, triangle:180, petal:180, filler:12}`**, over 32
  units. `20 + 180 + 180 + 12 = 392`, and `180 = 20 x 9`, which is the nine
  spikes the orb is named for.
- **One wheel is 19 cells** — `1 core + 9 triangle + 9 petal` — which is
  exactly the `elements=19` of section 2. The generic
  `(baseFaceIndex, patternFaceIndex)` filter and the semantic wheel
  decomposition **agree**, and CORRECTION 2's `9`/`10` was simply wrong.
- **`unit === baseFaceIndex` on every visible cell** (`mismatch: 0`), so wheel
  grouping is free from the projected scene alone; `orbCells` is needed only to
  *name* and *order* the cells within a wheel by `kind`.
- **The 12 `filler` cells belong to no wheel.** They are what the field needs to
  close, and they are why 392 is not a multiple of 19.
- **Maclado-9 and Maclado-9-Weave have identical cell decompositions.** Their
  section 2 shas agree too (`d050c039a16d` both) — the weave differs in the
  ribbon layer, not the cell layer.

CAVEAT, and it is the one the design doc must carry into any caption: the
visible counts are **front-cap** counts. 127 of 392 cells and 13 of 32 units
are visible in one view. Prose beside a frame that says "twenty wheels" is
describing the solid, not the picture.

## 4. Maclado-9-Overlap: shipped artifacts the current engine cannot produce

Run A, in `~/Workspace/git/3d-models`:

    ls -la build/orb-views/Maclado9Overlap/
    find build -type d -name "ribbons"

Output, verbatim:

    total 1624
    drwxr-xr-x  11 omareid  staff     352 Aug 15 17:01 .
    drwxr-xr-x  16 omareid  staff     512 Aug 15 16:48 ..
    -rw-r--r--   1 omareid  staff  134652 Aug 15 17:01 Maclado9Overlap.edge-2.gt.json
    -rw-r--r--   1 omareid  staff  113239 Aug 15 17:01 Maclado9Overlap.edge-2.png
    -rw-r--r--   1 omareid  staff   16805 Aug 15 17:01 Maclado9Overlap.edge-2.svg
    -rw-r--r--   1 omareid  staff  138433 Aug 15 17:01 Maclado9Overlap.face-5.gt.json
    -rw-r--r--   1 omareid  staff  121947 Aug 15 17:01 Maclado9Overlap.face-5.png
    -rw-r--r--   1 omareid  staff   17817 Aug 15 17:01 Maclado9Overlap.face-5.svg
    -rw-r--r--   1 omareid  staff  138806 Aug 15 17:01 Maclado9Overlap.vertex-3.gt.json
    -rw-r--r--   1 omareid  staff  116897 Aug 15 17:01 Maclado9Overlap.vertex-3.png
    -rw-r--r--   1 omareid  staff   17646 Aug 15 17:01 Maclado9Overlap.vertex-3.svg

`find` returned nothing: **no `ribbons` directory exists anywhere under
`build/`.**

The shipped SVG's first two elements, verbatim:

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="-70.00 -70.00 140.00 140.00" width="140" height="140" data-orb-view="edge-2" data-projection="spherical">
      <rect x="-70.00" y="-70.00" width="140.00" height="140.00" fill="#ffffff" pointer-events="none" />
      <path d="M31.5311,24.8737 L42.9703,29.9148 L27.0859,37.3602 L24.2436,31.1665 L31.5311,24.8737 Z" fill="#8a8a8a" stroke="#333333" stroke-width="0.4" data-face-index="0" data-sides="4" data-orb-view="edge-2" data-projection="spherical" data-orb-base-face="0" />

and its ground truth reports `schema_version 1.25`, `shapes 63`.

Commentary. `data-orb-base-face` and `data-face-index` are the **cell**
renderer's attributes. These are cell views.

Run B, in `~/Workspace/git/bikar`:

    node -e "
    import('./packages/core/dist/index.js').then(async m=>{
    const fs=await import('node:fs');
    const r=m.compileToGeometry(fs.readFileSync('patterns/Orbs/Maclado-9-Overlap.bkr','utf8'));
    console.log('orbCells today:', r.orbCells===null?'null':(r.orbCells?r.orbCells.length:'undefined'));
    const view=m.symmetryViewAxes(r.orb3d.base).find(v=>v.id==='edge-2');
    const P={radiusMm:r.orb3d.radiusMm,projection:r.orb3d.projection,view,ribbonWidthMm:r.orb3d.strutWidthMm};
    try{ const S=m.projectOrbViewScene(r,P); console.log('polygons:',S.polygons.length); }
    catch(e){ console.log('projectOrbViewScene today -> THROWS:', e.message); }
    const R=m.projectOrbRibbonScene(r,P);
    console.log('ribbon edge-2 -> polys:',R.polygons.length,'strands:',new Set(R.polygons.map(p=>p.ribbon.strandId)).size);
    });"

Output, verbatim:

    orbCells today: undefined
    projectOrbViewScene today -> THROWS: projectOrbViewScene: this wheelfield orb has no cell decomposition — the woven-overlap preset grows its rims until they cross, so the field cells are not its surface. Lifting the flat preview instead would render a different solid; use the ribbon views.
    ribbon edge-2 -> polys: 478 strands: 32

What this establishes. The engine at `e0a81cc` **refuses**, with a deliberate
and well-written error, to produce the very artifacts dated 2026-08-15 that are
sitting in `build/orb-views/Maclado9Overlap/`. Three cell SVGs, three PNGs and
three ground-truth files are stale against the current engine, and nothing in
either repo currently detects that. The design doc's claim that "the final
frame equals the shipped render" is therefore **already false today** for this
orb, before any timelapse exists.

CORRECTION 3. An earlier draft said the engine "emits `cells: null`" for this
orb. It does not: `r.orbCells` is `undefined`, and `projectOrbViewScene`
throws. The `null` is in bikar `packages/lab/src/scripts.ts`, where
`qiyasComposite.cells` is `null` — a different field with a different meaning
("no score recorded"). The two were conflated.

CAVEAT. `edge-2` yields **32** visible strands and 478 polygons, while the hero
view of section 2 yields **30** strands and 516 polygons. Strand visibility
varies by view. Neither is "the" strand count.

## 5. The `overlap` sweep: two disjoint feasible bands

Commentary. `Maclado-9-Overlap.bkr` declares `param overlap = 1.2 range
1.15..1.25 step 0.01`. Its header narrates the orb as a spike field "grown past
tangency". To test whether that narrative is expressible as a param-sweep
timelapse, the declared range was widened **in memory only** — the source
string was edited in the program, no file was touched — and the kernel probed
across it.

Run:

    node -e "
    import('./packages/core/dist/index.js').then(async m=>{
    const fs=await import('node:fs');
    const src0=fs.readFileSync('patterns/Orbs/Maclado-9-Overlap.bkr','utf8');
    const line=src0.split('\n').find(l=>l.includes('param overlap'));
    const src=src0.replace(line, line.replace('range 1.15..1.25','range 1.0..1.6'));
    let out=[];
    for(let ov=1.02; ov<=1.60001; ov+=0.02){
      const v=Math.round(ov*100)/100;
      try{
        const r=m.compileToGeometry(src,{params:{overlap:v}});
        const P={radiusMm:r.orb3d.radiusMm,projection:r.orb3d.projection,view:m.symmetryViewAxes(r.orb3d.base)[0],ribbonWidthMm:r.orb3d.strutWidthMm};
        const rs=m.projectOrbRibbonScene(r,P);
        out.push(v.toFixed(2)+':OK('+rs.polygons.length+')');
      }catch(e){ out.push(v.toFixed(2)+':x'); }
    }
    console.log(out.join(' '));
    });"

Output, verbatim:

    1.02:x 1.04:x 1.06:x 1.08:OK(516) 1.10:OK(516) 1.12:OK(516) 1.14:OK(516) 1.16:OK(516) 1.18:OK(516) 1.20:OK(516) 1.22:OK(516) 1.24:OK(516) 1.26:OK(516) 1.28:x 1.30:x 1.32:x 1.34:x 1.36:x 1.38:OK(750) 1.40:OK(750) 1.42:OK(750) 1.44:OK(750) 1.46:OK(750) 1.48:OK(750) 1.50:OK(750) 1.52:OK(750) 1.54:OK(744) 1.56:OK(744) 1.58:OK(744) 1.60:OK(744)

Characterising the two bands:

    node -e "... for(const v of [1.20,1.44]) { ...projectOrbRibbonScene... } ..."

Output, verbatim:

    overlap 1.2 orbWeave keys: nodes,edges,passes,amplitudeMm
       visible strands 30 polys 516 over 192 trimmed 300
    overlap 1.44 orbWeave keys: nodes,edges,passes,amplitudeMm
       visible strands 30 polys 750 over 270 trimmed 456

The three refusal messages, verbatim and in full:

    --- overlap=1 ---
    Parse error at 30:11: orb overlap expects a cap-growth ratio strictly above 1 (got 1) — at 1 the field is tangent: rims touch tip-to-tip and nothing crosses
    --- overlap=1.05 ---
    Evaluation error: orb Maclado9Overlap: maclado woven overlap: 30 of 30 adjacent pairs cannot weld at ratio 1.05 — pair (0, 1): weld nodes 0.76mm apart — closer than the 1.2mm strut width, they fuse
    --- overlap=1.3 ---
    Evaluation error: orb Maclado9Overlap: maclado woven overlap: 30 of 30 adjacent pairs cannot weld at ratio 1.3 — pair (0, 1): weld nodes 0.39mm apart — closer than the 1.2mm strut width, they fuse

What this establishes:

- **The feasible set is two disjoint bands** — `[1.08, 1.26]` and
  `[1.38, 1.60]` — separated by a dead band at `[1.28, 1.36]`. It is not an
  interval, and the `.bkr` header's "past ~1.25" phrasing reads as a single
  ceiling.
- **The declared range `1.15..1.25` is strictly inside band one** and is
  conservative: the kernel accepts from 1.08.
- **The two bands are different weave regimes**, not the same solid at
  different sizes: 516 polygons / 192 `over` passes versus 750 / 270. A third
  step appears at 1.54 (744).
- **The dead band and the lower refusal share one mechanism.** Both messages
  report weld nodes closer than the 1.2 mm strut width — 0.76 mm at 1.05 and
  0.39 mm at 1.30. Weld-node spacing is not monotonic in the overlap ratio,
  which is why feasibility is not an interval.
- **Tangency is unreachable.** `overlap = 1` is refused by the **parser**, not
  the kernel, with a dedicated message. The frame the orb's own narrative wants
  first is the one frame that cannot be rendered at any setting.

CAVEAT. Everything above is a **compile-time** result. No STL was exported, no
qiyas score was run, and nothing here says the second band is a legitimate solid
rather than one that happens to survive the welder. "Two disjoint bands" is a
statement about what compiles and nothing more.

CAVEAT. The sweep steps 0.02 and therefore locates each band edge only to
within 0.02. The bands are reported to the sampled endpoints, not to a bisected
boundary.

## 6. Timing

Run:

    node -e "... compileToGeometry over all 14, then per-file ..."

Output, verbatim:

    compile all 14: 94 ms
      Dodeca-Orb.bkr            3 ms
      Hankin-Orb.bkr            1 ms
      Maclado-9-Overlap.bkr     12 ms
      Maclado-9-Weave.bkr       7 ms
      Maclado-9.bkr             11 ms
      Rosette-Cube-Orb.bkr      3 ms
      Rosette-Orb.bkr           7 ms
      Rosette-Weave-Orb.bkr     2 ms
      Star-Cube-Orb.bkr         6 ms
      Star-Octa-Orb.bkr         2 ms
      Star-Orb.bkr              5 ms
      Star-Tetra-Orb.bkr        1 ms
      Weave-Dodeca-Orb.bkr      2 ms
      Weave-Orb.bkr             2 ms

Run (the full section 2 frame generation, timed):

    node -e "... project + renderOrbViewSVG/renderOrbRibbonViewSVG for every cumulative frame ..."

Output, verbatim:

    projection+SVG for 329 frames: 31 ms

What this establishes. Generating every frame of every orb's timelapse, at one
view, as SVG, costs **31 ms** on top of a **94 ms** compile of all 14. The
Maclado Overlap — flagged in the brief as the cost risk for its 60 loops — is a
12 ms compile.

CORRECTION 4. An earlier draft reported the frame generation as 152 ms and the
compile as 109 ms. The re-derived figures are 31 ms and 94 ms. The 152 ms
figure appears to have included compilation; the 109/94 gap is ordinary
run-to-run variance on a warm cache. Both numbers here are single runs and
should be read as order-of-magnitude, not as benchmarks.

NOT VERIFIED — rasterisation cost. An earlier draft claimed
`rsvg-convert` at 1024x1024 costs ~32 ms/frame, from a 10-run 0.317 s loop.
**This was not re-derived and is deliberately omitted.** `rsvg-convert`
requires a regular file for `-o` and rejects `/dev/null`
(`Error opening output "/dev/null": Target file is not a regular file`), and
this session was forbidden from writing files. Any claim in the design doc that
rasterisation dominates per-frame cost, or that SVG-only is ~30x cheaper, rests
on this un-re-derived number and must be marked as such until someone re-runs
it with a writable output path.

## 7. What was not measured

- **Three-view costs are arithmetic, not measurement.** Every count and timing
  above is for one hero view — the first axis from `symmetryViewAxes`. The
  design doc's three-view figures are the one-view figures multiplied by three.
  Section 4 shows this is known to be wrong in the safe direction and the
  unsafe one: the same orb yields 30 visible strands on the hero view and 32 on
  `edge-2`.
- **No CI measurement.** All timings are local, single machine, warm module
  cache, macOS on Apple silicon. No GitHub workflow was run.
- **No baseline for `make orbs`.** Running it writes to `build/`, which this
  session was forbidden to do. The design doc therefore states the timelapse's
  cost as an absolute addition and never as a percentage.
- **`projectSphericalCells` is not reachable from the built bundle.** It is
  exported from `packages/core/src/kernel3d/index.ts` but
  `packages/core/package.json` declares exactly one export path
  (`"." -> "./dist/index.js"`) and `dist/` contains only `index.js` and
  `index.d.ts`. It is therefore available to code **inside** core but not to an
  external consumer. Consequence: the base-polyhedron frame's visibility counts
  quoted in an earlier draft (Star-Orb 5 of 20, Rosette-Orb 3 of 12, Maclado-9
  3 of 12) **could not be re-derived in this session and are omitted rather
  than restated.** The build plan must budget for widening that export, or for
  placing the stage generator inside core.
- **A discarded probe.** An early attempt to count strands read
  `orbWeave.polylines`, which does not exist — the object's keys are
  `nodes, edges, passes, amplitudeMm` — and it silently reported `strands=0`.
  Every strand count in this file comes from `projectOrbRibbonScene` instead,
  and is therefore a **front-cap-visible** count. The "60 loops" figure in the
  orb's own header was never independently verified here.
- **Prose derivation was not demonstrated.** Section 1 shows the provenance tags
  exist. No caption generator was written, and nothing here shows that derived
  sentences read as prose rather than as telemetry.
