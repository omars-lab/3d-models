import"./modulepreload-polyfill-BxR_cmXS.js";import{n as e,r as t,t as n}from"./note-yGCj52Qt.js";import{C as r,O as i,b as a,h as o,j as s,m as c,n as l,p as u,t as d,w as f,x as p,y as m}from"./dist-CBzPEJa6.js";import{i as h,r as g}from"./lego-scripts-BXFMYmSH.js";var _=6;function v(e,t){let n=Math.cos(t),r=Math.sin(t);return{x:e.x*n-e.y*r,y:e.x*r+e.y*n}}function y(e){return Math.round(e/8)*8}function b(e,t,n){let r=v(t,n),i={x:y(r.x),y:y(r.y)},a=Math.abs(r.x-i.x),o=Math.abs(r.y-i.y);return{label:e,at:r,snap:i,resX:a,resY:o,worstMm:Math.max(a,o)}}function x(e){let t=f(e.basis),n=e.atTheta===`zero`?0:t.thetaDeg,r=n*Math.PI/180,i=e.studsHalf??3,[a,o]=e.basis;return{name:e.name,report:t,thetaDeg:n,vectors:[b(`a₁`,a,r),b(`a₂`,o,r)],points:S(e.basis,r,e.generations??2,i*8),studsHalf:i,unbuildable:e.unbuildable??!1}}function S([e,t],n,r,i){let a=[];for(let o=-r;o<=r;o++)for(let s=-r;s<=r;s++){if(ee.has(`${o},${s}`))continue;let r=v({x:o*e.x+s*t.x,y:o*e.y+s*t.y},n);te(r,i)&&a.push(r)}return a}var ee=new Set([`0,0`,`1,0`,`0,1`]),te=(e,t)=>Math.abs(e.x)<=t&&Math.abs(e.y)<=t;function C(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function w(e,t=6){let n=e.studsHalf*8,r=2*(n+_)*t,i=e=>(e+n+_)*t,a=e=>(n+_-e)*t,o=e=>Number(e.toFixed(2)).toString(),s=[];for(let t=-e.studsHalf;t<=e.studsHalf;t++){let e=t*8;s.push(`<line class="lat-grid" x1="${o(i(-n))}" y1="${o(a(e))}" x2="${o(i(n))}" y2="${o(a(e))}" />`,`<line class="lat-grid" x1="${o(i(e))}" y1="${o(a(-n))}" x2="${o(i(e))}" y2="${o(a(n))}" />`)}for(let n=-e.studsHalf;n<=e.studsHalf;n++)for(let r=-e.studsHalf;r<=e.studsHalf;r++)s.push(`<circle class="lat-stud" cx="${o(i(n*8))}" cy="${o(a(r*8))}" r="${o(c/2*t)}" />`);for(let n of e.points)s.push(`<circle class="lat-pt" cx="${o(i(n.x))}" cy="${o(a(n.y))}" r="${o(.7*t)}" />`);for(let n of e.vectors)s.push(...ne(n,{X:i,Y:a,n:o,scale:t}));s.push(`<circle class="lat-origin" cx="${o(i(0))}" cy="${o(a(0))}" r="${o(.9*t)}" />`);let l=`${e.name} — grid fit ${e.report.fit===void 0?`n/a`:e.report.fit.toFixed(2)} at ${e.thetaDeg.toFixed(1)} degrees`;return`<svg class="lattice-plan${e.unbuildable?` unbuildable`:``}" viewBox="0 0 ${o(r)} ${o(r)}" role="img" aria-label="${C(l)}" xmlns="http://www.w3.org/2000/svg">${s.join(``)}</svg>`}function ne(e,{X:t,Y:n,n:r,scale:i}){let a=[`<line class="lat-vec" x1="${r(t(0))}" y1="${r(n(0))}" x2="${r(t(e.at.x))}" y2="${r(n(e.at.y))}" />`,`<circle class="lat-tip" cx="${r(t(e.at.x))}" cy="${r(n(e.at.y))}" r="${r(.8*i)}" />`,`<text class="lat-lbl" x="${r(t(e.at.x/2)+6)}" y="${r(n(e.at.y/2)-4)}">${C(e.label)}</text>`],o=e.worstMm<u,s=o?`lat-res ok`:`lat-res`;if(a.push(`<path class="${s}" d="M ${r(t(e.at.x))} ${r(n(e.at.y))} L ${r(t(e.snap.x))} ${r(n(e.at.y))} L ${r(t(e.snap.x))} ${r(n(e.snap.y))}" fill="none" />`),!o){let i=e.resX>=e.resY,o=i?(e.at.x+e.snap.x)/2:e.snap.x,s=i?e.at.y:(e.at.y+e.snap.y)/2;a.push(`<text class="lat-lbl lat-lbl-res" x="${r(t(o))}" y="${r(n(s)-5)}" text-anchor="middle">${e.worstMm.toFixed(2)} mm</text>`)}return a}function re(e,t){return w(x(e),t)}var ie={square:e=>[{x:e,y:0},{x:0,y:e}],hexagonal:e=>[{x:e,y:0},{x:e/2,y:e*Math.sqrt(3)/2}],rhombic72:e=>[{x:e,y:0},{x:e*Math.cos(72*Math.PI/180),y:e*Math.sin(72*Math.PI/180)}],rectangular32:e=>[{x:e,y:0},{x:0,y:1.5*e}]},T={square:{probe:8,best:8},hexagonal:{probe:8,best:17.57},rhombic72:{probe:8,best:6.995},rectangular32:{probe:8,best:16}};function E(e,t,n={}){let r={name:`${e} at ${t} mm`,basis:ie[e](t),studsHalf:n.studsHalf,unbuildable:n.unbuildable};return{model:x(r),svg:re(r)}}function D(e){let t=g(e);if(!t)throw Error(`design note references a preset the Lab does not ship: ${e}`);let n=m(t.source);if(!n.brick3d)throw Error(`${e} compiled to no brick`);return n.brick3d.grid}function O(e){return e.fit===void 0?`n/a`:e.fit.toFixed(2)}function k(e){return e.repeatUnitStuds?.join(` × `)??`n/a`}var A={id:`lattice-basis`,title:`The lattice matrix has a row the grammar cannot build`,eyebrow:`3d-models · docs/lego-lab-design.md · §5.3, §11 Q8`,date:`2026-07-31`,status:`decided`,decision:`<strong>Label the row.</strong> §5.3's table gains an <strong>Authorable</strong>
    column stating, per row, whether a script can reach that lattice, plus the paragraph naming the
    single assignment site that decides it. The grammar is unchanged and no row is removed.
    The figures moved the argument away from the framing that produced the question: <em>widening
    the grammar would not raise a single number in the table</em>. Hexagonal is a basis the grammar
    already expresses and still tops out at 0.80, so a low score is not a symptom of a missing
    feature — it would only let an author write down a lattice that still cannot register.
    3d-models <code>docs/decisions-log.md</code> D-007, 2026-07-31.`,standfirst:`§5.3's lattice matrix is now <strong>measured</strong>, and measuring it surfaced a gap
    between the table and the language. <code>gridFit</code> scores any translation basis you hand
    it; the <code>tile</code> grammar can only <em>express</em> two of them. So one row of the table
    describes a lattice no <code>.bkr</code> can produce, and a reader has no way to tell which rows
    those are. Below: what the score reads, what scale can and cannot fix, the row with no script —
    and three ways to close it.`,render(){let t=E(`square`,T.square.probe),n=E(`hexagonal`,T.hexagonal.probe),r=E(`hexagonal`,T.hexagonal.best),i=E(`rectangular32`,T.rectangular32.probe,{studsHalf:4}),a=E(`rectangular32`,T.rectangular32.best,{studsHalf:4}),o=E(`rhombic72`,T.rhombic72.best,{unbuildable:!0}),s=D(`hex-field-tile`),c=D(`rational-repeat-tile`),l=o.model.vectors[0].worstMm.toFixed(2),u=o.model.vectors[1].worstMm.toFixed(2);return`
<section class="panel stack">
  <h2>What the score actually reads</h2>

  <div class="split">
    ${e({svg:t.svg,caption:`A square basis at one stud pitch. Both repeat vectors end on a stud centre, both
        residual legs are zero, and the score is <b>${O(t.model.report)}</b> with a repeat
        unit of <b>${k(t.model.report)}</b> studs.`,from:"gridFit(), on the family scripts/sweep-lattice-matrix.ts calls `square`"})}

    <div class="stack">
      <p>
        A pattern's <em>translation lattice</em> is two vectors. <code>gridFit</code> rotates that
        pair, and at each angle asks how far each vector's <b>x</b> and <b>y</b> components sit from
        a multiple of the 8 mm pitch. The worst of those four numbers is the
        residual; the score is <code>1 − residual / 4</code>, because a half pitch is as wrong as a
        point can be. It reports the angle that did best, since rotation is a knob the author has.
      </p>
      <p>
        That is exactly what the dashed <b>L</b> on each figure draws: the two legs <em>are</em> the
        two component residuals, and the labelled one is the leg the score used. Points beyond the
        first generation are context. The basis decides registration, so drawing every lattice point
        as though each cast a vote would be a prettier picture of a different measurement.
      </p>
      <p class="cost">
        <strong>Every figure here names its scale, and that is not a detail.</strong> §5.3's headline
        column is a <em>maximum over 2–20 mm</em> — "is there any size that lands this?" — while the
        Lab shows one size at a time. The same family can read 0.41 at one scale and 1.00 at another.
        A figure captioned with the wrong one of those would be the exact defect this page is about.
      </p>
    </div>
  </div>
</section>

<section class="panel stack">
  <h2>Scale is a real knob — and it is not enough</h2>

  <p>
    Both families below are reachable from <code>tile … mode rectangular</code> and
    <code>tile … mode hex</code>: the evaluator writes the basis at one place and it is one of two
    shapes, <code>[(dx, 0), (0, dy)]</code> or <code>[(dx, 0), (dx/2, dy)]</code>. Each is drawn
    twice — at the size an author reaches for first, and at the size the sweep found best.
  </p>

  <div class="pair">
    ${e({svg:i.svg,caption:`A 3 : 2 rectangular lattice at ${T.rectangular32.probe} mm scores
        <b>${O(i.model.report)}</b>. Nothing is wrong with the lattice; it is the wrong
        size.`,from:"gridFit(), on the family the sweep calls `rectangular32`"})}

    ${e({svg:a.svg,caption:`The same lattice at ${T.rectangular32.best} mm: every vector lands,
        <b>${O(a.model.report)}</b>, repeat unit <b>${k(a.model.report)}</b>
        studs. This is <code>Rational-Repeat-Tile</code>, which compiles to
        <b>${O(c)}</b> on a <b>${k(c)}</b> stud repeat — not square, and
        perfect anyway.`,from:`gridFit(), and patterns/Lego/Rational-Repeat-Tile.bkr compiled alongside it`})}
  </div>

  <div class="pair">
    ${e({svg:n.svg,caption:`The hexagonal lattice at ${T.hexagonal.probe} mm, at the best angle there
        is (<b>${n.model.thetaDeg.toFixed(1)}°</b>): <b>${O(n.model.report)}</b>.
        This is <code>Hex-Field-Tile</code>, which compiles to <b>${O(s)}</b> and reports
        its repeat unit as <b>${k(s)}</b> — a sheared basis has no answer in whole studs,
        and withholding one is not the same as scoring zero.`,from:`gridFit(), and patterns/Lego/Hex-Field-Tile.bkr compiled alongside it`})}

    ${e({svg:r.svg,caption:`The best the hexagonal lattice does anywhere in the swept interval —
        ${T.hexagonal.best} mm at <b>${r.model.thetaDeg.toFixed(1)}°</b>, scoring
        <b>${O(r.model.report)}</b>. Better, and still short: √3 is irrational, so no scale
        closes it.`,from:`gridFit(), at the argmax scale of scripts/sweep-lattice-matrix.ts`})}
  </div>

  <p class="cost">
    <strong>The ratio decides it, not the fold number.</strong> A rational ratio lands at some scale;
    an irrational one never does, at any scale — and the sweep itself can only report that it did not
    land within 2–20 mm. The unbounded claim rests on the arithmetic, not on the table. That is the
    whole content of §5.3, and it is why the rhombic row below is worth having.
  </p>

  <p class="cost">
    <strong>A low score is not a defect.</strong> <code>Hex-Field-Tile</code> passes the hard anchor
    gate with 15 tube anchors and prints as a correct clutching brick. What a low score costs is
    seamless extension: butt two of them edge to edge and the art breaks at the join. That is why
    the grid gate is a score and the anchor gate is a verdict, and why V8 warns rather than refuses.
  </p>
</section>

<section class="panel defect stack">
  <h2>The row that has no script</h2>

  <div class="split">
    ${e({svg:o.svg,caption:`Two equal edges at 72°, at the best scale and angle the sweep found
        (${T.rhombic72.best} mm, <b>${o.model.thetaDeg.toFixed(1)}°</b>): one vector
        ${l} mm off a stud, the other ${u} mm, scoring
        <b>${O(o.model.report)}</b>.`,from:"gridFit(), on the family the sweep calls `rhombic72`",overlaid:`nothing here is compiled from a .bkr — no script in the language produces this basis`})}

    <div class="stack">
      <p>
        The measured matrix reports this row honestly, and the sweep that produced it reached the
        basis by constructing it and handing it to the kernel. A reader of §5.3 has every reason to
        assume they could author it. They cannot: the second vector's x-component is fixed at
        <code>0</code> or at <code>dx/2</code>, and a 72° rhombus is neither.
      </p>
      <p>
        The table is not wrong. What is missing is the sentence saying which of its rows are
        reachable from the language and which are facts about the gate alone — <strong>and that is a
        K7</strong>: a document disagreeing with the machinery it ships, findable by reading one
        against the other rather than by any new research.
      </p>
      <div class="flag">
        Whatever is decided, the doc gains that sentence. The options differ in whether the grammar
        moves to meet the table, or the table admits it is describing the gate.
      </div>
    </div>
  </div>
</section>

<section class="options">

  <article class="panel opt stack">
    <div>
      <div class="opt-name">Widen the grammar</div>
      <h2>Let a tile declare its own basis</h2>
    </div>

    <p>
      Add a general two-vector basis to <code>tile</code>, so the second vector may carry an
      x-component. Every lattice <code>gridFit</code> can score becomes one an author can write, and
      the matrix stops describing anything the language cannot reach.
    </p>

    <div>
      <h3>What you'd author</h3>
<pre><span class="kw">tile</span> rose_motif
  <span class="kw">repeat_x</span> 3
  <span class="kw">repeat_y</span> 3
  <span class="kw">basis</span> (8.0, 0) (2.47, 7.61)   <span class="cm">&larr; new: any two vectors</span></pre>
    </div>

    <p class="cost">
      <strong>Largest scope.</strong> Grammar, AST, evaluator, and a tiler that steps a sheared
      basis — the rectangular and hexagonal walks are two hard-coded loops, and this replaces them
      with one general one. Crop, void-detection and anchor placement then all meet cell shapes they
      have not met.
    </p>

    <div class="flag">
      It buys a family nothing in the catalogue currently asks for. The 5-/10-fold designs §5.3 cites
      as motivation are the ones with a <em>rectangular</em> repeat — which
      <code>Rational-Repeat-Tile</code> already ships, at 1.00.
    </div>
  </article>

  <article class="panel opt taken stack">
    <div>
      <div class="opt-name">Label the row</div>
      <h2>Say which rows the language can reach</h2>
      <div class="opt-taken">Taken — D-007</div>
    </div>

    <p>
      Keep the matrix whole — it is a true statement about the gate, and the rhombic row is what
      makes the ratio argument legible — and mark each row with whether a <code>.bkr</code> can
      produce it. The reader is never misled, and the gap is documented rather than hidden.
    </p>

    <div>
      <h3>What changes</h3>
<pre><span class="cm"># docs/lego-lab-design.md §5.3</span>
| Lattice   | Ratio  | Measured | <span class="kw">Authorable</span>             |
| square    | 1.0000 | 1.0000   | <span class="kw">yes — mode rectangular</span> |
| hexagonal | 1.7321 | 0.8037   | <span class="kw">yes — mode hex</span>         |
| 72° rhomb | 1.3764 | 0.7264   | <span class="kw">no  — kernel only</span>      |</pre>
    </div>

    <p class="cost">
      <strong>Smallest scope.</strong> One table column and a paragraph. No kernel change. The sweep
      already measures exactly these families, so nothing has to be re-run.
    </p>

    <div class="flag ok">
      Costs nothing and removes the misreading. It leaves the gap open rather than closing it — a
      reader who <em>wants</em> a rhombic tile is told no, with a reason.
    </div>
  </article>

  <article class="panel opt stack">
    <div>
      <div class="opt-name">Cut the row</div>
      <h2>Measure only what can be built</h2>
    </div>

    <p>
      Drop <code>rhombic72</code> from the matrix and from the sweep, on the rule that this document
      describes the parts the repo builds. Four rows survive, every one of them reachable from a
      script.
    </p>

    <div>
      <h3>What changes</h3>
<pre><span class="cm"># scripts/sweep-lattice-matrix.ts</span>
<span class="kw">export const</span> FAMILIES = [
  square, hexagonal,
  rectangular32, quasiperiodic,
]  <span class="cm">&larr; rhombic72 removed</span></pre>
    </div>

    <p class="cost">
      <strong>Small scope, and destructive.</strong> One family, its pinned test case, and the §5.3
      row.
    </p>

    <div class="flag">
      It deletes the row that carries the argument. The hexagonal row already shows an irrational
      ratio failing — but the rhombic row is the one that corrected §5.3's original blame from φ to
      <code>cot 36°</code>, and cutting it discards the measurement behind the correction.
    </div>
  </article>

</section>

<section class="panel stack">
  <h2>Side by side</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th scope="col"></th>
          <th scope="col">Widen the grammar</th>
          <th scope="col">Label the row</th>
          <th scope="col">Cut the row</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Closes the K7</th>
          <td class="yes">yes — grammar meets table</td>
          <td class="yes">yes — table states the limit</td>
          <td class="yes">yes — removes the claim</td>
        </tr>
        <tr>
          <th scope="row">Keeps the cot 36° correction</th>
          <td class="yes">yes</td>
          <td class="yes">yes</td>
          <td class="no">no</td>
        </tr>
        <tr>
          <th scope="row">A rhombic tile becomes authorable</th>
          <td class="yes">yes</td>
          <td class="no">no</td>
          <td class="no">no</td>
        </tr>
        <tr>
          <th scope="row">Kernel work</th>
          <td class="no">general tiler, grammar, AST</td>
          <td class="yes">none</td>
          <td class="yes">none</td>
        </tr>
        <tr>
          <th scope="row">A shipped script wants it today</th>
          <td class="no">none does</td>
          <td>n/a</td>
          <td>n/a</td>
        </tr>
        <tr>
          <th scope="row">Reversible</th>
          <td class="no">a shipped grammar is forever</td>
          <td class="yes">a column</td>
          <td class="no">deletes a measurement</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<p class="foot">
  Every score on this page came from <code>gridFit</code> when you loaded it, and the two preset
  captions compiled their <code>.bkr</code> first — which is why they can claim the drawn score and
  the compiled score are the same number. The families match
  <code>scripts/sweep-lattice-matrix.ts</code>; <code>packages/lab/tests/design-lattice.test.ts</code>
  asserts that against the script itself, so a figure here cannot drift from §5.3's measured matrix
  without a red test.
</p>`}};function j(e,t){let n=e*e-t*t;return n>0?Math.sqrt(n):0}function M(e,t){let n=t-e.y,r=j(e.outerDiaMm/2,n);if(r===0)return[];if(e.kind===`pin`)return[{x0:e.x-r,x1:e.x+r,what:`pin`}];let i=j(d/2,n);return i===0?[{x0:e.x-r,x1:e.x+r,what:`tube`}]:[{x0:e.x-r,x1:e.x-i,what:`tube`},{x0:e.x+i,x1:e.x+r,what:`tube`}]}function N(e,t={}){let{w:n,ox:r,oy:a}=h(e.cols,e.rows,e.origin),s=e.solution.anchors,c=t.cutY??s[0]?.y??a,l=p(e.fit),u=r-n/2,d=r+n/2,f=[{x0:u,x1:u+l,what:`wall`},...s.flatMap(e=>M(e,c)),{x0:d-l,x1:d,what:`wall`}].sort((e,t)=>e.x0-t.x0),m=i(e,e.solution),{studSpans:g,ghosts:_}=ae(e,m,c),v=[{z0:0,z1:e.engageMm,role:`cavity`,spans:f},{z0:e.engageMm,z1:e.heightMm,role:`ceiling`,spans:[{x0:u,x1:d,what:`ceiling`}]}];return(g.length>0||_.length>0)&&v.push({z0:e.heightMm,z1:e.heightMm+o,role:`stud`,spans:g.sort((e,t)=>e.x0-t.x0)}),{name:e.name,cutY:c,extent:{x0:u,x1:d,z0:0,z1:e.heightMm+(m.length>0?o:0)},bands:v,ghosts:_,dims:t.dims===!1?[]:oe(e,u,d,n),overlays:t.overlays??[],notes:se(e,c)}}function ae(e,t,n){let r=a(e.fit)/2,i=[],s=[];for(let a of t){let t=j(r,n-a.y);t>0?i.push({x0:a.x-t,x1:a.x+t,what:`stud`}):s.push({x0:a.x-r,x1:a.x+r,z0:e.heightMm,z1:e.heightMm+o,what:`stud behind the cut`})}return{studSpans:i,ghosts:s}}function oe(e,t,n,r){let i=e.solution.anchors.find(e=>e.kind===`tube`);return[{axis:`x`,from:t,to:n,at:-2.4,label:`${r.toFixed(1)} mm`},{axis:`z`,from:0,to:e.heightMm,at:n+2.4,label:`${e.heightMm.toFixed(1)} mm`},{axis:`z`,from:0,to:e.engageMm,at:t-2.4,label:`engage ${e.engageMm.toFixed(1)}`},{axis:`z`,from:e.engageMm,to:e.heightMm,at:t-6.4,label:`ceiling ${e.ceilingMm.toFixed(1)}`},...i?[{axis:`x`,from:i.x-i.outerDiaMm/2,to:i.x+i.outerDiaMm/2,at:e.engageMm+2,label:`⌀${i.outerDiaMm.toFixed(3)}`}]:[]]}function se(e,t){let n=[`Section at y = ${t.toFixed(2)} mm through ${e.name}, drawn from the compiled brick.`];return e.clutch!==`none`&&e.fit.ribMm>0&&n.push(`Clutch ribs (${e.fit.ribMm} mm × ${e.fit.ribArcMm} mm arc) sit off this plane and are not drawn.`),n.push(...e.notes),n}var P=10;function F(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function ce(e,t=8){let{extent:n}=e,r=(n.x1-n.x0+2*P)*t,i=(n.z1-n.z0+2*P)*t,a=e=>(e-n.x0+P)*t,o=e=>(n.z1-e+P)*t,s=e=>Number(e.toFixed(2)).toString(),c=[];for(let n of e.ghosts)c.push(`<rect class="sec-ghost" x="${s(a(n.x0))}" y="${s(o(n.z1))}" width="${s((n.x1-n.x0)*t)}" height="${s((n.z1-n.z0)*t)}"><title>${F(n.what)}</title></rect>`);for(let n of e.bands)for(let e of n.spans)c.push(`<rect class="sec-solid sec-${e.what}" x="${s(a(e.x0))}" y="${s(o(n.z1))}" width="${s((e.x1-e.x0)*t)}" height="${s((n.z1-n.z0)*t)}" data-what="${e.what}" data-x-mm="${s((e.x0+e.x1)/2)}"><title>${F(e.what)}</title></rect>`);c.push(`<line class="sec-bed" x1="${s(a(n.x0-P/2))}" y1="${s(o(0))}" x2="${s(a(n.x1+P/2))}" y2="${s(o(0))}" />`);let l={X:a,Z:o,n:s,scale:t};for(let t of e.dims)c.push(...le(t,l));for(let t of e.overlays)c.push(...I(t,l));return`<svg class="section" viewBox="0 0 ${s(r)} ${s(i)}" role="img" aria-label="${F(e.name)} section at y = ${e.cutY.toFixed(2)} mm" xmlns="http://www.w3.org/2000/svg">${c.join(``)}</svg>`}function le(e,{X:t,Z:n,n:r}){let[i,a,o,s]=e.axis===`x`?[t(e.from),n(e.at),t(e.to),n(e.at)]:[t(e.at),n(e.from),t(e.at),n(e.to)],c=(i+o)/2,l=(a+s)/2;return[`<line class="sec-dim" x1="${r(i)}" y1="${r(a)}" x2="${r(o)}" y2="${r(s)}" />`,e.axis===`x`?`<text class="sec-lbl" x="${r(c)}" y="${r(l-3)}" text-anchor="middle">${F(e.label)}</text>`:`<text class="sec-lbl" x="${r(c)}" y="${r(l)}" text-anchor="middle" transform="rotate(-90 ${r(c)} ${r(l)})">${F(e.label)}</text>`]}function I(e,{X:t,Z:n,n:r,scale:i}){let a=[],o=e.diaMm??3;if(e.kind===`rod`){let s=e.heightMm??12;a.push(`<rect class="sec-rod" x="${r(t(e.xMm-o/2))}" y="${r(n(e.zMm+s))}" width="${r(o*i)}" height="${r(s*i)}" />`)}else e.kind===`phantom`&&a.push(`<circle class="sec-phantom" cx="${r(t(e.xMm))}" cy="${r(n(e.zMm))}" r="${r(o/2*i)}" />`);return e.label&&a.push(`<text class="sec-lbl sec-lbl-note" x="${r(t(e.xMm))}" y="${r(n(e.zMm)-6)}" text-anchor="middle">${F(e.label)}</text>`),a}function L(e,t,n){return ce(N(e,t),n)}function R(e){let t=g(e);if(!t)throw Error(`design note references a preset the Lab does not ship: ${e}`);let n=m(t.source);if(!n.brick3d)throw Error(`${e} compiled to no brick`);return n.brick3d}var z={id:`multi-piece-export`,title:`Multi-piece export needs something to decompose`,eyebrow:`3d-models · docs/lego-lab-design.md · §10 P1`,date:`2026-07-31`,status:`decided`,decision:`<strong>Studs as ports.</strong> Decided 2026-07-31 — 3d-models
    <code>docs/decisions-log.md</code> D-006. The deciding fact is on the drawings below: the two
    sections in that option contain no line the kernel does not already emit, so it names geometry
    the mesh already has rather than adding any. <em>Refuse the phantom</em> stays correct but
    leaves the only reachable assembly a C2 tile one, so the Lego Lab would ship a feature its own
    catalogue never triggers; <em>real hole</em> contradicts §1's Technic non-goal, and the section
    shows the bore crossing load-bearing material between two solver-placed tubes. The cost of the
    option taken — two port kinds, a stud index that survives a footprint change, a pose solver and
    a printed-onto-printed clutch rung — is accepted, not discovered. It reverses on a measurement:
    if no rung of the printed-onto-printed fit ladder holds, a stud is a shape and not a joint.
    <br><br><strong>Built 2026-07-31, and the clutch rung reported back.</strong> On the shipped fit
    defaults a printed brick stacked on a printed brick has <em>no interference at all</em>: the
    −0.2 mm diametral offsets are calibrated for a printed part meeting a moulded one, where only
    one side shrank, and brick-onto-brick applies them twice. So the default stack compiles and
    <em>warns</em> rather than erroring — the part prints and stacks, it just does not clutch.
    Applying the offsets once (<code>studDiaMm 0</code>) puts the joint back inside the window. That
    is not the reversal named above, since a rung does hold; it is why the default is a warning
    rather than a silence, and <code>CAL-STK-01</code> (coupon <code>LG-S1</code>) is the bet that
    settles where the ceiling actually sits.`,standfirst:`P1 lists <strong>multi-piece export</strong> for the Lego Lab. Nothing in the Lego
    catalogue currently decomposes into separately-printed parts, and §1's non-goals rule out the
    joint that normally would. Below: the defect found while scoping it, then the three ways
    forward, every section drawn from a compiled brick at the same scale.`,render(){let t=R(`classic-brick`),n=t.solution.anchors[0],r=t.solution.engaged[0],i=L(t,{overlays:[{kind:`rod`,xMm:0,zMm:t.heightMm+6,diaMm:3,heightMm:10},{kind:`phantom`,xMm:0,zMm:t.engageMm+t.ceilingMm/2,diaMm:3.15,label:`declared ⌀3.15 — not cut`}]}),a=L(t,{cutY:n.y,dims:!1},6),o=L(t,{cutY:r.y,dims:!1},6),s=L(t,{dims:!1,overlays:[{kind:`phantom`,xMm:0,zMm:t.engageMm+t.ceilingMm/2,diaMm:3.15,label:`material that would be removed`}]}),c=t.solution.anchors[0]?.outerDiaMm.toFixed(3)??`n/a`;return`
<section class="panel defect stack">
  <h2>What is true today: a socket the checker validates and the mesh does not have</h2>

  <div class="split">
    ${e({svg:i,caption:`Section through <code>ClassicBrick</code> at the anchor row. Everything drawn solid is
        in the exported mesh; the dashed circle and the rod above it are not.`,from:`patterns/Lego/Classic-Brick.bkr`,overlaid:`the ⌀3.15 socket and the arriving rod — neither is geometry the kernel emits`})}

    <div class="stack">
      <p>
        A <code>brick</code> accepts a declared <code>port</code>, and an <code>assembly</code> will
        happily <code>connect</code> a rod into it. The C2 fit ladder checks the pin against the
        socket diameter and passes. Then <code>--format parts</code> writes the brick out — and the
        socket is not there. <code>buildBrick</code> never sees <code>decl.ports</code>; only
        <code>hole</code> cuts material, and <code>brick</code> has no <code>hole</code> statement.
      </p>

      <div class="measure">
        <div>Panel-Left.stl <b>3764 △</b></div>
        <div>same brick, no port <b>3764 △</b></div>
        <div>difference <b>0</b></div>
      </div>

      <p class="cost">
        A <code>piece</code> is safe from this because its sockets come from <code>hole</code>, which
        cuts, and a rod's port is the rod's own end — geometry that exists either way. Only
        <code>brick</code> can mint a socket out of nothing.
        <strong>This gets a validator and a test regardless of which option below is picked.</strong>
      </p>
    </div>
  </div>
</section>

<section class="options">

  <article class="panel opt stack">
    <div>
      <div class="opt-name">Refuse the phantom</div>
      <h2>Bricks stay single prints</h2>
    </div>

    <p>
      Make a socket-role <code>port</code> on a <code>brick</code> a parse error, and leave
      multi-piece export to the pieces that already decompose: <code>Pinned-Tiles.bkr</code> is in
      the repo today, declares <code>export parts</code>, and its bores come from <code>hole</code>,
      so they are real.
    </p>

    <div>
      <h3>What you'd print</h3>
      <div class="prints">
        <span>2 slab tiles + 2 rods, from one script</span>
        <span>every Lego brick, alone, as now</span>
      </div>
    </div>

    <div>
      <h3>The DSL, unchanged</h3>
<pre><span class="cm"># patterns/Assemblies/Pinned-Tiles.bkr</span>
<span class="kw">tile</span> TileA
  <span class="kw">hole</span> h1 <span class="kw">at</span> -15, 0
    <span class="kw">band</span> d $pin_d - 0.10 …
<span class="kw">assembly</span> PinnedTiles
  <span class="kw">connect</span> PinA.seat <span class="kw">to</span> TileA.h1
  <span class="kw">export parts</span></pre>
    </div>

    <p class="cost">
      <strong>Smallest scope.</strong> One validator, plus the Lab's parts panel and per-part
      download. Nothing new in the kernel.
    </p>

    <div class="flag">
      The P1 line is satisfied literally, but the case a user can actually reach is a C2 tile
      assembly — not a Lego one. The Lego Lab ships a feature its own catalogue never triggers.
    </div>
  </article>

  <article class="panel opt taken stack">
    <div>
      <div class="opt-name">Studs as ports</div>
      <h2>Bricks join the way LEGO joins</h2>
      <div class="opt-taken">Taken — D-006</div>
    </div>

    ${e({svg:`${a}${o}`,caption:`The same brick cut twice: above, through the anchor row — the ⌀${c} mm tubes that
        receive. Below, through a stud row — the studs they receive. Both are already in the mesh.`,from:`patterns/Lego/Classic-Brick.bkr, at two cut planes`})}

    <div>
      <h3>What you'd print</h3>
      <div class="prints">
        <span>one STL per brick in the stack</span>
        <span>each plated on its own bottom face</span>
      </div>
    </div>

    <div>
      <h3>The DSL, extended</h3>
<pre><span class="kw">assembly</span> Panel
  <span class="kw">place</span> Base
  <span class="kw">place</span> Top
  <span class="kw">connect</span> Base.stud_c1r2 <span class="kw">to</span> Top.anti_c1r2
  <span class="kw">export parts</span>
<span class="cm"># stud/anti-stud ports auto-minted by brick,</span>
<span class="cm"># named by lattice cell, never by ordinal</span></pre>
    </div>

    <p class="cost">
      <strong>Largest scope.</strong> Two new port kinds, a stud-index naming scheme that survives a
      footprint change, a pose solver for the assembled preview, and a clutch-fit rung for
      printed-onto-printed. Built on 2026-07-31; the pose solver and
      <code>export parts</code> turned out to be already generic over the piece registry, so the
      only real gap was minting the ports.
    </p>

    <div class="flag ok">
      Stays inside §1's non-goals: no Technic, no SNOT, no hinge. It is the one joint the brick
      already models in full, and §3.3's contact census already describes its grip.
    </div>
  </article>

  <article class="panel opt stack">
    <div>
      <div class="opt-name">Real hole</div>
      <h2>Cut the socket, amend the non-goal</h2>
    </div>

    ${e({svg:s,caption:`The bore would be cut through the ceiling and the shell wall — through material this
        section shows is load-bearing, between two tubes the anchor solver placed.`,from:`patterns/Lego/Classic-Brick.bkr`,overlaid:`the bore — this is the geometry the option would add, not geometry that exists`})}

    <div>
      <h3>What you'd print</h3>
      <div class="prints">
        <span>bricks with true pin bores</span>
        <span>rods, sized off the C2 fit ladder</span>
      </div>
    </div>

    <div>
      <h3>The DSL, extended</h3>
<pre><span class="kw">brick</span> Left
  <span class="kw">footprint</span> 2 x 4
  <span class="kw">hole</span> h1 <span class="kw">at</span> 0, 0        <span class="cm">← new on brick</span>
    <span class="kw">band</span> d 3.15 <span class="kw">from</span> 0 <span class="kw">to</span> 6
<span class="cm"># socket now cuts; the fit check</span>
<span class="cm"># describes something that exists</span></pre>
    </div>

    <p class="cost">
      <strong>Middle scope.</strong> Reuse <code>tile</code>'s hole machinery, plus interaction rules
      against the cavity, tubes and ribs that <code>tile</code> never had to think about.
    </p>

    <div class="flag">
      Contradicts a stated non-goal: §1 rules out “Technic geometry (axle holes, pin holes, ⌀4.8
      bars)”. Taking it means amending §1 with the reasoning recorded — a widening that is argued
      for, not one that arrives as a side effect of a P1 checkbox.
    </div>
  </article>

</section>

<section class="panel stack">
  <h2>Side by side</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th scope="col"></th>
          <th scope="col">Refuse the phantom</th>
          <th scope="col">Studs as ports</th>
          <th scope="col">Real hole</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Fixes the phantom socket</th>
          <td class="yes">yes — refuses it</td>
          <td class="yes">yes — makes it real</td>
          <td class="yes">yes — makes it real</td>
        </tr>
        <tr>
          <th scope="row">A Lego script decomposes</th>
          <td class="no">no</td>
          <td class="yes">yes</td>
          <td class="yes">yes</td>
        </tr>
        <tr>
          <th scope="row">New kernel geometry</th>
          <td class="yes">none</td>
          <td class="yes">none — names existing shapes</td>
          <td class="no">a boolean cut through the shell</td>
        </tr>
        <tr>
          <th scope="row">Respects §1 non-goals</th>
          <td class="yes">yes</td>
          <td class="yes">yes</td>
          <td class="no">no — needs §1 amended</td>
        </tr>
        <tr>
          <th scope="row">New DSL surface</th>
          <td>none</td>
          <td>2 port kinds + stud indexing</td>
          <td><code>hole</code> on <code>brick</code></td>
        </tr>
        <tr>
          <th scope="row">Rough size</th>
          <td>validator + Lab panel</td>
          <td>kernel + DSL + solver + Lab panel</td>
          <td>kernel cut + DSL + Lab panel</td>
        </tr>
        <tr>
          <th scope="row">Unmeasured bet it adds</th>
          <td>none</td>
          <td>printed-tube-onto-printed-stud clutch</td>
          <td>bore-vs-cavity wall after the cut</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<p class="foot">
  All three keep the sweep strip and the compatibility matrix untouched — those are already landed
  or independent. The triangle counts in the first panel came from
  <code>bikar render … --format parts</code> against a scratch two-part assembly and
  <code>patterns/Lego/Classic-Brick.bkr</code> as the control; both binary STL headers report 3764
  triangles. Everything else on this page was compiled when you loaded it.
</p>`}},B=8/2;function V(e,t,n){let i=r(n);return{axis:e,artMm:t,studs:n,plateMm:i,smallerMm:n>1?r(n-1):i,borderMm:(i-t)/2,nearerSmaller:n>1&&i-t>B+1e-9}}function H(e){if(!e.art?.footprintAuto)return;let t=V(`x`,e.art.bboxMm.width,e.cols),n=V(`y`,e.art.bboxMm.height,e.rows);return{name:e.name,x:t,y:n,rescale:Math.min(t.smallerMm/t.artMm,n.smallerMm/n.artMm)}}var U=4;function ue(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function de(e,t=5){let n=e.x.plateMm/2,r=e.y.plateMm/2,i=(e.x.plateMm+2*U)*t,a=(e.y.plateMm+2*U)*t,o=e=>(e+n+U)*t,s=e=>(r+U-e)*t,c=e=>Number(e.toFixed(2)).toString(),l=(e,t)=>`M ${c(o(-e/2))} ${c(s(t/2))} H ${c(o(e/2))} V ${c(s(-t/2))} H ${c(o(-e/2))} Z`,u=(e,n,r)=>`<rect class="${e}" x="${c(o(-n/2))}" y="${c(s(r/2))}" width="${c(n*t)}" height="${c(r*t)}" />`,d=[`<path class="brd-dead" fill-rule="evenodd" d="${l(e.x.plateMm,e.y.plateMm)} ${l(e.x.artMm,e.y.artMm)}" />`,u(`brd-plate`,e.x.plateMm,e.y.plateMm),u(`brd-art`,e.x.artMm,e.y.artMm),u(`brd-smaller`,e.x.smallerMm,e.y.smallerMm)];for(let t of[e.x,e.y]){let r=t.axis===`x`,i=r?s(-e.y.plateMm/2+t.borderMm/2):o(-n+t.borderMm/2);d.push(r?`<text class="brd-lbl" x="${c(o(0))}" y="${c(i+3)}" text-anchor="middle">${t.borderMm.toFixed(2)} mm dead</text>`:`<text class="brd-lbl" x="${c(i)}" y="${c(s(0))}" text-anchor="middle" transform="rotate(-90 ${c(i)} ${c(s(0))})">${t.borderMm.toFixed(2)} mm dead</text>`)}let f=`${e.name}: art ${e.x.artMm.toFixed(2)} by ${e.y.artMm.toFixed(2)} mm on a ${e.x.studs} by ${e.y.studs} stud plate`;return`<svg class="border-plan" viewBox="0 0 ${c(i)} ${c(a)}" role="img" aria-label="${ue(f)}" xmlns="http://www.w3.org/2000/svg">${d.join(``)}</svg>`}function fe(e,t){let n=H(e);return n?de(n,t):``}function W(e){let t=p(e.fit),n=r(e.cols)/2,i=r(e.rows)/2,a={x:e.origin.col*8,y:e.origin.row*8};return{name:e.name,plate:{halfW:n,halfH:i},cavity:{halfW:n-t,halfH:i-t},origin:a,shellWallMm:t,anchors:e.solution.anchors.map(e=>({kind:e.kind,x:e.x,y:e.y,rMm:e.outerDiaMm/2,boreRMm:e.kind===`tube`?d/2:void 0})),span:s(e.solution,e.cols,e.rows,e.fit,e.origin),droppedAnchors:e.solution.droppedAnchors,droppedForRelief:e.solution.droppedForRelief}}var G=5;function pe(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function me(e,t=5){let{plate:n,origin:r}=e,i=(2*n.halfW+2*G)*t,a=(2*n.halfH+2*G)*t,o=e=>(e-r.x+n.halfW+G)*t,s=e=>(n.halfH+G-(e-r.y))*t,c=e=>Number(e.toFixed(2)).toString(),l=(e,n,i)=>`<rect class="${e}" x="${c(o(r.x-n))}" y="${c(s(r.y+i))}" width="${c(2*n*t)}" height="${c(2*i*t)}" />`,u=[l(`cav-plate`,n.halfW,n.halfH),l(`cav-room`,e.cavity.halfW,e.cavity.halfH)];for(let n of e.anchors)u.push(`<circle class="cav-anchor cav-${n.kind}" cx="${c(o(n.x))}" cy="${c(s(n.y))}" r="${c(n.rMm*t)}"><title>${n.kind} at ${n.x.toFixed(2)}, ${n.y.toFixed(2)}</title></circle>`),n.boreRMm!==void 0&&u.push(`<circle class="cav-bore" cx="${c(o(n.x))}" cy="${c(s(n.y))}" r="${c(n.boreRMm*t)}" />`);let{diameterMm:d,centre:f}=e.span;d>0&&u.push(`<circle class="cav-span" cx="${c(o(f.x))}" cy="${c(s(f.y))}" r="${c(d/2*t)}" />`,`<line class="cav-span-dim" x1="${c(o(f.x-d/2))}" y1="${c(s(f.y))}" x2="${c(o(f.x+d/2))}" y2="${c(s(f.y))}" />`,`<text class="cav-lbl" x="${c(o(f.x))}" y="${c(s(f.y)-4)}" text-anchor="middle">${d.toFixed(2)} mm</text>`);let p=`${e.name} underside, largest unsupported run ${d.toFixed(2)} mm across`;return`<svg class="cavity-plan" viewBox="0 0 ${c(i)} ${c(a)}" role="img" aria-label="${pe(p)}" xmlns="http://www.w3.org/2000/svg">${u.join(``)}</svg>`}function he(e){let{droppedAnchors:t,droppedForRelief:n}=e;return t+n===0?`Every anchor candidate survived, so this is the diagonal pocket between four anti-studs — the widest gap an 8 mm pitch can leave.`:`${[t>0?`${t} candidate${t===1?``:`s`} the body test rejected`:``,n>0?`${n} rejected by a relief pocket`:``].filter(Boolean).join(` and `)} — the run is open where those anchors are not.`}function K(e,t){return me(W(e),t)}var q=new Map;function J(e){let t=q.get(e);if(t)return t;let n=g(e);if(!n)throw Error(`design note references a preset the Lab does not ship: ${e}`);let r=m(n.source);if(!r.brick3d)throw Error(`${e} compiled to no brick`);return q.set(e,r.brick3d),r.brick3d}var Y=[`classic-brick`,`pin-rail`,`grid-field-tile`,`rational-repeat-tile`,`edge-stud-tile`,`star-brick`,`hex-field-tile`];function X(){return Y.filter(e=>W(J(e)).span.diameterMm>l).length}function ge(e){let t=J(e),r=W(t),i=r.droppedAnchors+r.droppedForRelief,a=r.span.diameterMm>l;return`<tr>
    <th scope="row">${n(t.name)}</th>
    <td>${t.cols} × ${t.rows}</td>
    <td class="${a?`no`:`yes`}">${r.span.diameterMm.toFixed(2)}</td>
    <td>${r.anchors.length}</td>
    <td>${i===0?`0`:`${i} (${r.droppedForRelief>0?`relief`:`body`})`}</td>
  </tr>`}function Z(e,t){return`<code>${n(e.name)}</code> from underneath — the plate, the cavity inside the shell
    wall, and every anchor the solver kept. The unfilled circle is the largest empty disc in that
    room: <b>${e.span.diameterMm.toFixed(2)} mm</b>, centred at
    ${e.span.centre.x.toFixed(2)}, ${e.span.centre.y.toFixed(2)} mm.
    ${n(he(e))} ${t}`}function Q(e,t){let r=e.warnings.filter(e=>e.startsWith(t));return r.length===0?`<div class="flag ok">No ${t} on this brick.</div>`:r.map(e=>`<div class="flag">${n(e)}</div>`).join(``)}var $=[{id:`span-and-border`,title:`The span is not the plate, and the border is not always waste`,eyebrow:`3d-models · docs/lego-lab-design.md · §11 Q4, Q5`,date:`2026-08-01`,status:`decided`,decision:`<strong>V12 warns on the measured run; V13 warns only under
    <code>footprint auto</code>.</strong> Resolved 2026-07-31 in
    <code>docs/lego-lab-design.md</code> §11 Q4 and Q5 — there is no <code>D-NNN</code> entry
    because neither was an option between designs; each was a question whose answer a measurement
    settled. Q4 asked for a <em>footprint-dependent</em> bridging warning and its premise did not
    survive the seven presets: a 1×8 and a 5×5 span the same gap to within a tenth of a millimetre,
    and the largest plate in the set is not the widest span. Q5's first draft fired on five of seven
    presets, four of which had done nothing wrong, and its "smaller plate already fits" branch was
    unreachable by <code>studsFor</code>'s own definition. Both are warnings and neither refuses:
    V12's ceiling is <code>CAL-BRG-01</code>, transcribed from a slicer preset this project has
    never printed against, and coupon <code>MC-3</code> is the print that settles it.`,standfirst:`Two open questions in §11, both about a number the compiler could compute and neither
    about a shape anyone had looked at. Q4 wanted to warn about the <strong>bridged cavity
    ceiling</strong>; Q5 wanted to know whether <code>footprint auto</code> should round a pattern up
    to the next stud or refuse it. Below: what the presets actually measured, why the first question
    was asking about the wrong dimension, and the one preset V13 is entitled to speak about — every
    plan compiled from <code>patterns/Lego/</code> when you opened this page.`,render(){let t=J(`pin-rail`),r=J(`grid-field-tile`),i=J(`hex-field-tile`),a=J(`star-brick`),o=J(`edge-stud-tile`),s=W(t),c=W(r),u=W(i),d=W(a),f=K(t,5),p=K(r,5),m=K(i,5),h=fe(a,6),g=H(o),_=l.toFixed(0);return`
<section class="panel defect stack">
  <h2>What Q4 asked for, and the sentence that turned out to be wrong</h2>

  <p>
    Q4 as written said: <em>“span still scales with footprint — a 2×2 cavity bridges 12 mm, a 6×6
    bridges 44 mm”</em>, and asked for a warning keyed on the plate. That is a reasonable thing to
    believe about a hollow box, and it is what the outline of the brick suggests. It is not what the
    ceiling spans between. §5.2 of the same document says why: <code>solveAnchors</code> places an
    anti-stud at <strong>every interior cell corner</strong>, so the stud pitch caps the widest
    unsupported run and a bigger plate simply buys more anchors.
  </p>

  <div class="pair">
    ${e({svg:f,caption:Z(s,`A 1×8 rail, and the only preset that takes <b>pins</b> rather than tubes.`),from:`patterns/Lego/Pin-Rail.bkr`})}

    ${e({svg:p,caption:Z(c,`A 5×5 plate with ${c.anchors.length} anchors — twenty-five times the area of the rail
        above, drawn at the same scale, and the same gap.`),from:`patterns/Lego/Grid-Field-Tile.bkr`})}
  </div>

  <div class="measure">
    <div>Pin-Rail, 1 × 8 <b>${s.span.diameterMm.toFixed(2)} mm</b></div>
    <div>Grid-Field-Tile, 5 × 5 <b>${c.span.diameterMm.toFixed(2)} mm</b></div>
    <div>difference <b>${Math.abs(s.span.diameterMm-c.span.diameterMm).toFixed(2)} mm</b></div>
  </div>

  <p class="cost">
    Both discs are the diagonal pocket between four anti-studs, which is the widest gap an 8 mm
    pitch can leave. <strong>The plate does not appear in the answer.</strong> So V12 is keyed on
    the measured run — <code>supportSpanMm</code>, a shrinking-grid largest-empty-circle search over
    the anchor set the build actually kept — and not on <code>cols × rows</code>.
  </p>
</section>

<section class="panel stack">
  <h2>What does move it: an anchor that was never placed</h2>

  <p>
    Every preset that spans more than ${_} mm has the same thing wrong with it, and it is not
    its size. Relief art sitting on a lattice crossing rejects the anchor candidate underneath it,
    and the ceiling has to cross the hole where that anchor would have stood.
  </p>

  ${e({svg:m,caption:Z(u,`The worst case in the catalogue, and a 6×6 — the same footprint as
      <code>Edge-Stud-Tile</code>, which spans ${W(o).span.diameterMm.toFixed(2)} mm.
      What separates them is ${u.droppedForRelief} rejected candidates against
      ${W(o).droppedForRelief}.`),from:`patterns/Lego/Hex-Field-Tile.bkr`})}

  ${Q(i,`V12`)}

  <p>
    The figure cannot show the ten candidates that were dropped, and deliberately does not try:
    <code>AnchorSolution</code> keeps their count and not their positions, and re-running the
    candidate search to recover them would be a second solve of exactly the step whose
    <em>rejections</em> are the subject. What it shows is the consequence — the room, and the widest
    thing that fits in it.
  </p>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th scope="col">preset</th>
          <th scope="col">footprint</th>
          <th scope="col">span (mm)</th>
          <th scope="col">anchors kept</th>
          <th scope="col">dropped</th>
        </tr>
      </thead>
      <tbody>
        ${Y.map(ge).join(`
`)}
      </tbody>
    </table>
  </div>

  <p class="cost">
    Read down the footprint column and it is unsorted; read down the dropped column and it splits
    the table in two. <strong>Every drop in the shipped set is a relief drop.</strong> V12 still
    reports the body-test drop separately, because the recourse differs — a body-test drop is fixed
    by a wider body and a relief drop by moving the art — but no preset here exercises that branch,
    and the note says so rather than implying both causes are represented.
  </p>
</section>

<section class="panel stack">
  <h2>Why it warns and never refuses</h2>

  <p>
    The ${_} mm ceiling is <code>BRIDGE_SPAN_MAX_MM</code>, bet <code>CAL-BRG-01</code>. It is
    Bambu Studio's shipped <code>max_bridge_length</code> — the number a stock slicer stops trusting
    at, rather than the number filament stops spanning at. The appendix that credits it also records
    community bridging at 20–80 mm on tuned machines, so a refusal would be this project asserting a
    limit it has never printed against. Coupon <code>MC-3</code> is the print that settles it, and
    until it comes back the four presets over the line are shipping, printing, and flagged.
  </p>

  <div class="measure">
    <div>ceiling, transcribed <b>${_} mm</b></div>
    <div>presets over it <b>${X()} of ${Y.length}</b></div>
    <div>presets refused <b>0</b></div>
  </div>
</section>

<section class="panel stack">
  <h2>Q5: rounding up is a decision the compiler made, and only that</h2>

  <p>
    <code>footprint auto</code> asks the compiler to pick a plate big enough for the art.
    <code>studsFor</code> picks the least <em>n</em> with <code>footprintMm(n) ≥ mm</code>, so the
    plate is always at least as big as the art and usually bigger. Q5 asked whether the leftover
    should be a warning or a refusal. It is a warning — but the draft that nearly shipped got the
    harder half wrong, which was <strong>which sources V13 may speak about</strong>.
  </p>

  ${e({svg:h,caption:`<code>${n(a.name)}</code>'s rounding, in plan. The filled ring is the dead border:
      plate minus art. The dashed rectangle is <code>footprintMm(n−1)</code>, the plate one stud
      smaller — drawn <em>inside</em> the art because that is the whole finding. It does not contain
      the art, and V13 fires because of how nearly it does.`,from:`patterns/Lego/Star-Brick.bkr`})}

  ${Q(a,`V13`)}

  <p>
    Run ungated, the first draft of V13 fired on five of the seven presets. Every one of those five
    <em>declares</em> its footprint, and in each the border is a design choice a bounding box cannot
    see — <code>Edge-Stud-Tile</code>'s ${g===void 0?`wide margin`:`margin`} is its
    perimeter stud ring, and its own header says so. A typed <code>footprint 6 x 6</code> is a
    decision; <code>auto</code> is an arithmetic result. V13 judges the arithmetic, which is the only
    thing it is entitled to judge, so it is gated on <code>auto</code> and
    <code>${n(a.name)}</code> is the single preset in the catalogue it can speak about.
  </p>

  <div class="flag ok">
    This page draws no border figure for <code>Edge-Stud-Tile</code>, and the omission is the gate
    rather than an oversight: <code>borderPlanModel</code> returns
    <code>${g===void 0?`undefined`:`a model`}</code> for it. A figure drawn for a
    typed footprint would be arguing that the author's plate is wasteful — the claim the first draft
    made about five presets and had to withdraw.
  </div>

  <p class="cost">
    The draft also offered <em>“and the smaller plate already fits it as drawn”</em>, which
    contradicts its own first clause. Under <code>auto</code> the art is <em>always</em> strictly
    wider than <code>footprintMm(n−1)</code>, by the definition of <code>studsFor</code> — the branch
    could never fire. <strong>Deleted, with the proof kept beside the code.</strong> No source could
    have settled that one; it was found by reading the message against itself.
  </p>
</section>

<section class="panel stack">
  <h2>What the two warnings cost the reader</h2>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th scope="col"></th>
          <th scope="col">V12 — bridged span</th>
          <th scope="col">V13 — dead border</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">Fires on</th>
          <td>measured run &gt; ${_} mm</td>
          <td>border &gt; half a stud pitch, per axis</td>
        </tr>
        <tr>
          <th scope="row">Gated on</th>
          <td>nothing — every brick has a cavity</td>
          <td><code>footprint auto</code> only</td>
        </tr>
        <tr>
          <th scope="row">Shipped presets it flags</th>
          <td>${X()}</td>
          <td>${a.warnings.filter(e=>e.startsWith(`V13`)).length} (both axes of one preset)</td>
        </tr>
        <tr>
          <th scope="row">Number behind it</th>
          <td class="no">borrowed — <code>CAL-BRG-01</code>, unprinted</td>
          <td class="yes">derived — <code>STUD_PITCH_MM / 2</code></td>
        </tr>
        <tr>
          <th scope="row">Recourse it names</th>
          <td>widen the body, or move the art, by which drop counter fired</td>
          <td>rescale the art, or declare the footprint</td>
        </tr>
        <tr>
          <th scope="row">What would reverse it</th>
          <td>MC-3 printing a wider span cleanly</td>
          <td>nothing measurable — it is arithmetic about a choice</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<p class="foot">
  Both figures on this page are drawn from records the kernel returns rather than from a second
  calculation: <code>supportSpan</code> hands back the circle's centre with its diameter precisely so
  a drawing of the span can be checked against the warning, and
  <code>BrickResultProvenance.art</code> carries the bounding box and the <code>auto</code> flag that
  V13 was handed. <code>design-cavity.test.ts</code> holds the drawn diameter to
  <code>BrickProvenance.supportSpanMm</code>, so a picture that disagreed with the message beside it
  would fail the suite rather than ship. ${d.anchors.length===1?`<code>${n(a.name)}</code> is worth one last look: a 4×4 plate with a single surviving anchor, which is what ${d.droppedForRelief} relief drops out of nine candidates leaves.`:``}
</p>`}},A,z];function _e(e){return $.find(t=>t.id===e)}function ve(){return`<header class="masthead">
      <div class="eyebrow">bikar · design notes</div>
      <h1>Decisions, with the geometry attached</h1>
      <p class="standfirst">
        Each note argues one decision that could not be settled from the code alone. Every section
        drawing on these pages is compiled from a script in <code>patterns/</code> when you open it,
        so a figure and the part it describes cannot quietly disagree.
      </p>
      <p><a href="./studio.html">&larr; Studio</a> · <a href="./lego.html">Lego Lab</a> · <a href="./lab.html">Orb Lab</a></p>
    </header>
    <section class="notes-list">${$.map(e=>`<a class="panel note-card" href="?n=${encodeURIComponent(e.id)}">
      <div class="eyebrow">${n(e.date)} · ${n(e.status)}</div>
      <h2>${n(e.title)}</h2>
      <p>${e.standfirst}</p>
    </a>`).join(``)}</section>`}function ye(e){return`<header class="masthead">
      <div class="eyebrow">${n(e.eyebrow)}</div>
      <h1>${n(e.title)}</h1>
      <p class="standfirst">${e.standfirst}</p>
      <div class="provenance">${n(e.date)} · ${t(e)}</div>
      <p><a href="./design.html">&larr; All design notes</a></p>
    </header>
    ${e.render()}`}function be(e){return`<header class="masthead">
      <div class="eyebrow">bikar · design notes</div>
      <h1>No note called “${n(e)}”</h1>
      <p class="standfirst">
        Notes are never deleted, so a link that does not resolve is a link that was never right.
      </p>
      <p><a href="./design.html">&larr; All design notes</a></p>
    </header>`}function xe(e,t){let r=t instanceof Error?t.message:String(t);return`<header class="masthead">
      <div class="eyebrow">${n(e.eyebrow)}</div>
      <h1>${n(e.title)}</h1>
    </header>
    <section class="panel defect stack">
      <h2>This note no longer compiles</h2>
      <p>
        Its figures are sections of parts this repo builds, and one of them will not build. The note
        is stale, not the page — read the error, then fix the note or the kernel.
      </p>
      <pre>${n(r)}</pre>
      <p><a href="./design.html">&larr; All design notes</a></p>
    </section>`}function Se(){let e=document.querySelector(`#app`);if(!e)return;let t=new URLSearchParams(window.location.search).get(`n`);if(!t){e.innerHTML=ve(),document.title=`Design notes — bikar`;return}let n=_e(t);if(!n){e.innerHTML=be(t);return}document.title=`${n.title} — bikar design notes`;try{e.innerHTML=ye(n)}catch(t){e.innerHTML=xe(n,t)}}Se();