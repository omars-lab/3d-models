import"./modulepreload-polyfill-BxR_cmXS.js";import{n as e,r as t,t as n}from"./note-BLUpIaoN.js";import{_ as r,b as i,d as a,f as o,g as s,h as c,t as l,u,w as d}from"./dist-B5rd_OWE.js";import{i as f,r as p}from"./lego-scripts-N56Wnyi7.js";var m=6;function h(e,t){let n=Math.cos(t),r=Math.sin(t);return{x:e.x*n-e.y*r,y:e.x*r+e.y*n}}function g(e){return Math.round(e/8)*8}function _(e,t,n){let r=h(t,n),i={x:g(r.x),y:g(r.y)},a=Math.abs(r.x-i.x),o=Math.abs(r.y-i.y);return{label:e,at:r,snap:i,resX:a,resY:o,worstMm:Math.max(a,o)}}function v(e){let t=i(e.basis),n=e.atTheta===`zero`?0:t.thetaDeg,r=n*Math.PI/180,a=e.studsHalf??3,[o,s]=e.basis;return{name:e.name,report:t,thetaDeg:n,vectors:[_(`a₁`,o,r),_(`a₂`,s,r)],points:y(e.basis,r,e.generations??2,a*8),studsHalf:a,unbuildable:e.unbuildable??!1}}function y([e,t],n,r,i){let a=[];for(let o=-r;o<=r;o++)for(let s=-r;s<=r;s++){if(b.has(`${o},${s}`))continue;let r=h({x:o*e.x+s*t.x,y:o*e.y+s*t.y},n);x(r,i)&&a.push(r)}return a}var b=new Set([`0,0`,`1,0`,`0,1`]),x=(e,t)=>Math.abs(e.x)<=t&&Math.abs(e.y)<=t;function S(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function C(e,t=6){let n=e.studsHalf*8,r=2*(n+m)*t,i=e=>(e+n+m)*t,o=e=>(n+m-e)*t,s=e=>Number(e.toFixed(2)).toString(),c=[];for(let t=-e.studsHalf;t<=e.studsHalf;t++){let e=t*8;c.push(`<line class="lat-grid" x1="${s(i(-n))}" y1="${s(o(e))}" x2="${s(i(n))}" y2="${s(o(e))}" />`,`<line class="lat-grid" x1="${s(i(e))}" y1="${s(o(-n))}" x2="${s(i(e))}" y2="${s(o(n))}" />`)}for(let n=-e.studsHalf;n<=e.studsHalf;n++)for(let r=-e.studsHalf;r<=e.studsHalf;r++)c.push(`<circle class="lat-stud" cx="${s(i(n*8))}" cy="${s(o(r*8))}" r="${s(a/2*t)}" />`);for(let n of e.points)c.push(`<circle class="lat-pt" cx="${s(i(n.x))}" cy="${s(o(n.y))}" r="${s(.7*t)}" />`);for(let n of e.vectors)c.push(...w(n,{X:i,Y:o,n:s,scale:t}));c.push(`<circle class="lat-origin" cx="${s(i(0))}" cy="${s(o(0))}" r="${s(.9*t)}" />`);let l=`${e.name} — grid fit ${e.report.fit===void 0?`n/a`:e.report.fit.toFixed(2)} at ${e.thetaDeg.toFixed(1)} degrees`;return`<svg class="lattice-plan${e.unbuildable?` unbuildable`:``}" viewBox="0 0 ${s(r)} ${s(r)}" role="img" aria-label="${S(l)}" xmlns="http://www.w3.org/2000/svg">${c.join(``)}</svg>`}function w(e,{X:t,Y:n,n:r,scale:i}){let a=[`<line class="lat-vec" x1="${r(t(0))}" y1="${r(n(0))}" x2="${r(t(e.at.x))}" y2="${r(n(e.at.y))}" />`,`<circle class="lat-tip" cx="${r(t(e.at.x))}" cy="${r(n(e.at.y))}" r="${r(.8*i)}" />`,`<text class="lat-lbl" x="${r(t(e.at.x/2)+6)}" y="${r(n(e.at.y/2)-4)}">${S(e.label)}</text>`],o=e.worstMm<u,s=o?`lat-res ok`:`lat-res`;if(a.push(`<path class="${s}" d="M ${r(t(e.at.x))} ${r(n(e.at.y))} L ${r(t(e.snap.x))} ${r(n(e.at.y))} L ${r(t(e.snap.x))} ${r(n(e.snap.y))}" fill="none" />`),!o){let i=e.resX>=e.resY,o=i?(e.at.x+e.snap.x)/2:e.snap.x,s=i?e.at.y:(e.at.y+e.snap.y)/2;a.push(`<text class="lat-lbl lat-lbl-res" x="${r(t(o))}" y="${r(n(s)-5)}" text-anchor="middle">${e.worstMm.toFixed(2)} mm</text>`)}return a}function T(e,t){return C(v(e),t)}var E={square:e=>[{x:e,y:0},{x:0,y:e}],hexagonal:e=>[{x:e,y:0},{x:e/2,y:e*Math.sqrt(3)/2}],rhombic72:e=>[{x:e,y:0},{x:e*Math.cos(72*Math.PI/180),y:e*Math.sin(72*Math.PI/180)}],rectangular32:e=>[{x:e,y:0},{x:0,y:1.5*e}]},D={square:{probe:8,best:8},hexagonal:{probe:8,best:17.57},rhombic72:{probe:8,best:6.995},rectangular32:{probe:8,best:16}};function O(e,t,n={}){let r={name:`${e} at ${t} mm`,basis:E[e](t),studsHalf:n.studsHalf,unbuildable:n.unbuildable};return{model:v(r),svg:T(r)}}function k(e){let t=p(e);if(!t)throw Error(`design note references a preset the Lab does not ship: ${e}`);let n=c(t.source);if(!n.brick3d)throw Error(`${e} compiled to no brick`);return n.brick3d.grid}function A(e){return e.fit===void 0?`n/a`:e.fit.toFixed(2)}function j(e){return e.repeatUnitStuds?.join(` × `)??`n/a`}var M={id:`lattice-basis`,title:`The lattice matrix has a row the grammar cannot build`,eyebrow:`3d-models · docs/lego-lab-design.md · §5.3, §11 Q8`,date:`2026-07-31`,status:`decided`,decision:`<strong>Label the row.</strong> §5.3's table gains an <strong>Authorable</strong>
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
    and three ways to close it.`,render(){let t=O(`square`,D.square.probe),n=O(`hexagonal`,D.hexagonal.probe),r=O(`hexagonal`,D.hexagonal.best),i=O(`rectangular32`,D.rectangular32.probe,{studsHalf:4}),a=O(`rectangular32`,D.rectangular32.best,{studsHalf:4}),o=O(`rhombic72`,D.rhombic72.best,{unbuildable:!0}),s=k(`hex-field-tile`),c=k(`rational-repeat-tile`),l=o.model.vectors[0].worstMm.toFixed(2),u=o.model.vectors[1].worstMm.toFixed(2);return`
<section class="panel stack">
  <h2>What the score actually reads</h2>

  <div class="split">
    ${e({svg:t.svg,caption:`A square basis at one stud pitch. Both repeat vectors end on a stud centre, both
        residual legs are zero, and the score is <b>${A(t.model.report)}</b> with a repeat
        unit of <b>${j(t.model.report)}</b> studs.`,from:"gridFit(), on the family scripts/sweep-lattice-matrix.ts calls `square`"})}

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
    ${e({svg:i.svg,caption:`A 3 : 2 rectangular lattice at ${D.rectangular32.probe} mm scores
        <b>${A(i.model.report)}</b>. Nothing is wrong with the lattice; it is the wrong
        size.`,from:"gridFit(), on the family the sweep calls `rectangular32`"})}

    ${e({svg:a.svg,caption:`The same lattice at ${D.rectangular32.best} mm: every vector lands,
        <b>${A(a.model.report)}</b>, repeat unit <b>${j(a.model.report)}</b>
        studs. This is <code>Rational-Repeat-Tile</code>, which compiles to
        <b>${A(c)}</b> on a <b>${j(c)}</b> stud repeat — not square, and
        perfect anyway.`,from:`gridFit(), and patterns/Lego/Rational-Repeat-Tile.bkr compiled alongside it`})}
  </div>

  <div class="pair">
    ${e({svg:n.svg,caption:`The hexagonal lattice at ${D.hexagonal.probe} mm, at the best angle there
        is (<b>${n.model.thetaDeg.toFixed(1)}°</b>): <b>${A(n.model.report)}</b>.
        This is <code>Hex-Field-Tile</code>, which compiles to <b>${A(s)}</b> and reports
        its repeat unit as <b>${j(s)}</b> — a sheared basis has no answer in whole studs,
        and withholding one is not the same as scoring zero.`,from:`gridFit(), and patterns/Lego/Hex-Field-Tile.bkr compiled alongside it`})}

    ${e({svg:r.svg,caption:`The best the hexagonal lattice does anywhere in the swept interval —
        ${D.hexagonal.best} mm at <b>${r.model.thetaDeg.toFixed(1)}°</b>, scoring
        <b>${A(r.model.report)}</b>. Better, and still short: √3 is irrational, so no scale
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
        (${D.rhombic72.best} mm, <b>${o.model.thetaDeg.toFixed(1)}°</b>): one vector
        ${l} mm off a stud, the other ${u} mm, scoring
        <b>${A(o.model.report)}</b>.`,from:"gridFit(), on the family the sweep calls `rhombic72`",overlaid:`nothing here is compiled from a .bkr — no script in the language produces this basis`})}

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
</p>`}};function N(e,t){let n=e*e-t*t;return n>0?Math.sqrt(n):0}function P(e,t){let n=t-e.y,r=N(e.outerDiaMm/2,n);if(r===0)return[];if(e.kind===`pin`)return[{x0:e.x-r,x1:e.x+r,what:`pin`}];let i=N(l/2,n);return i===0?[{x0:e.x-r,x1:e.x+r,what:`tube`}]:[{x0:e.x-r,x1:e.x-i,what:`tube`},{x0:e.x+i,x1:e.x+r,what:`tube`}]}function F(e,t={}){let{w:n,ox:i,oy:a}=f(e.cols,e.rows,e.origin),s=e.solution.anchors,c=t.cutY??s[0]?.y??a,l=r(e.fit),u=i-n/2,p=i+n/2,m=[{x0:u,x1:u+l,what:`wall`},...s.flatMap(e=>P(e,c)),{x0:p-l,x1:p,what:`wall`}].sort((e,t)=>e.x0-t.x0),h=d(e,e.solution),{studSpans:g,ghosts:_}=I(e,h,c),v=[{z0:0,z1:e.engageMm,role:`cavity`,spans:m},{z0:e.engageMm,z1:e.heightMm,role:`ceiling`,spans:[{x0:u,x1:p,what:`ceiling`}]}];return(g.length>0||_.length>0)&&v.push({z0:e.heightMm,z1:e.heightMm+o,role:`stud`,spans:g.sort((e,t)=>e.x0-t.x0)}),{name:e.name,cutY:c,extent:{x0:u,x1:p,z0:0,z1:e.heightMm+(h.length>0?o:0)},bands:v,ghosts:_,dims:t.dims===!1?[]:L(e,u,p,n),overlays:t.overlays??[],notes:R(e,c)}}function I(e,t,n){let r=s(e.fit)/2,i=[],a=[];for(let s of t){let t=N(r,n-s.y);t>0?i.push({x0:s.x-t,x1:s.x+t,what:`stud`}):a.push({x0:s.x-r,x1:s.x+r,z0:e.heightMm,z1:e.heightMm+o,what:`stud behind the cut`})}return{studSpans:i,ghosts:a}}function L(e,t,n,r){let i=e.solution.anchors.find(e=>e.kind===`tube`);return[{axis:`x`,from:t,to:n,at:-2.4,label:`${r.toFixed(1)} mm`},{axis:`z`,from:0,to:e.heightMm,at:n+2.4,label:`${e.heightMm.toFixed(1)} mm`},{axis:`z`,from:0,to:e.engageMm,at:t-2.4,label:`engage ${e.engageMm.toFixed(1)}`},{axis:`z`,from:e.engageMm,to:e.heightMm,at:t-6.4,label:`ceiling ${e.ceilingMm.toFixed(1)}`},...i?[{axis:`x`,from:i.x-i.outerDiaMm/2,to:i.x+i.outerDiaMm/2,at:e.engageMm+2,label:`⌀${i.outerDiaMm.toFixed(3)}`}]:[]]}function R(e,t){let n=[`Section at y = ${t.toFixed(2)} mm through ${e.name}, drawn from the compiled brick.`];return e.clutch!==`none`&&e.fit.ribMm>0&&n.push(`Clutch ribs (${e.fit.ribMm} mm × ${e.fit.ribArcMm} mm arc) sit off this plane and are not drawn.`),n.push(...e.notes),n}var z=10;function B(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`)}function V(e,t=8){let{extent:n}=e,r=(n.x1-n.x0+2*z)*t,i=(n.z1-n.z0+2*z)*t,a=e=>(e-n.x0+z)*t,o=e=>(n.z1-e+z)*t,s=e=>Number(e.toFixed(2)).toString(),c=[];for(let n of e.ghosts)c.push(`<rect class="sec-ghost" x="${s(a(n.x0))}" y="${s(o(n.z1))}" width="${s((n.x1-n.x0)*t)}" height="${s((n.z1-n.z0)*t)}"><title>${B(n.what)}</title></rect>`);for(let n of e.bands)for(let e of n.spans)c.push(`<rect class="sec-solid sec-${e.what}" x="${s(a(e.x0))}" y="${s(o(n.z1))}" width="${s((e.x1-e.x0)*t)}" height="${s((n.z1-n.z0)*t)}" data-what="${e.what}" data-x-mm="${s((e.x0+e.x1)/2)}"><title>${B(e.what)}</title></rect>`);c.push(`<line class="sec-bed" x1="${s(a(n.x0-z/2))}" y1="${s(o(0))}" x2="${s(a(n.x1+z/2))}" y2="${s(o(0))}" />`);let l={X:a,Z:o,n:s,scale:t};for(let t of e.dims)c.push(...H(t,l));for(let t of e.overlays)c.push(...U(t,l));return`<svg class="section" viewBox="0 0 ${s(r)} ${s(i)}" role="img" aria-label="${B(e.name)} section at y = ${e.cutY.toFixed(2)} mm" xmlns="http://www.w3.org/2000/svg">${c.join(``)}</svg>`}function H(e,{X:t,Z:n,n:r}){let[i,a,o,s]=e.axis===`x`?[t(e.from),n(e.at),t(e.to),n(e.at)]:[t(e.at),n(e.from),t(e.at),n(e.to)],c=(i+o)/2,l=(a+s)/2;return[`<line class="sec-dim" x1="${r(i)}" y1="${r(a)}" x2="${r(o)}" y2="${r(s)}" />`,e.axis===`x`?`<text class="sec-lbl" x="${r(c)}" y="${r(l-3)}" text-anchor="middle">${B(e.label)}</text>`:`<text class="sec-lbl" x="${r(c)}" y="${r(l)}" text-anchor="middle" transform="rotate(-90 ${r(c)} ${r(l)})">${B(e.label)}</text>`]}function U(e,{X:t,Z:n,n:r,scale:i}){let a=[],o=e.diaMm??3;if(e.kind===`rod`){let s=e.heightMm??12;a.push(`<rect class="sec-rod" x="${r(t(e.xMm-o/2))}" y="${r(n(e.zMm+s))}" width="${r(o*i)}" height="${r(s*i)}" />`)}else e.kind===`phantom`&&a.push(`<circle class="sec-phantom" cx="${r(t(e.xMm))}" cy="${r(n(e.zMm))}" r="${r(o/2*i)}" />`);return e.label&&a.push(`<text class="sec-lbl sec-lbl-note" x="${r(t(e.xMm))}" y="${r(n(e.zMm)-6)}" text-anchor="middle">${B(e.label)}</text>`),a}function W(e,t,n){return V(F(e,t),n)}function G(e){let t=p(e);if(!t)throw Error(`design note references a preset the Lab does not ship: ${e}`);let n=c(t.source);if(!n.brick3d)throw Error(`${e} compiled to no brick`);return n.brick3d}var K=[M,{id:`multi-piece-export`,title:`Multi-piece export needs something to decompose`,eyebrow:`3d-models · docs/lego-lab-design.md · §10 P1`,date:`2026-07-31`,status:`decided`,decision:`<strong>Studs as ports.</strong> Decided 2026-07-31 — 3d-models
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
    forward, every section drawn from a compiled brick at the same scale.`,render(){let t=G(`classic-brick`),n=t.solution.anchors[0],r=t.solution.engaged[0],i=W(t,{overlays:[{kind:`rod`,xMm:0,zMm:t.heightMm+6,diaMm:3,heightMm:10},{kind:`phantom`,xMm:0,zMm:t.engageMm+t.ceilingMm/2,diaMm:3.15,label:`declared ⌀3.15 — not cut`}]}),a=W(t,{cutY:n.y,dims:!1},6),o=W(t,{cutY:r.y,dims:!1},6),s=W(t,{dims:!1,overlays:[{kind:`phantom`,xMm:0,zMm:t.engageMm+t.ceilingMm/2,diaMm:3.15,label:`material that would be removed`}]}),c=t.solution.anchors[0]?.outerDiaMm.toFixed(3)??`n/a`;return`
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
</p>`}}];function q(e){return K.find(t=>t.id===e)}function J(){return`<header class="masthead">
      <div class="eyebrow">bikar · design notes</div>
      <h1>Decisions, with the geometry attached</h1>
      <p class="standfirst">
        Each note argues one decision that could not be settled from the code alone. Every section
        drawing on these pages is compiled from a script in <code>patterns/</code> when you open it,
        so a figure and the part it describes cannot quietly disagree.
      </p>
      <p><a href="./studio.html">&larr; Studio</a> · <a href="./lego.html">Lego Lab</a> · <a href="./lab.html">Orb Lab</a></p>
    </header>
    <section class="notes-list">${K.map(e=>`<a class="panel note-card" href="?n=${encodeURIComponent(e.id)}">
      <div class="eyebrow">${n(e.date)} · ${n(e.status)}</div>
      <h2>${n(e.title)}</h2>
      <p>${e.standfirst}</p>
    </a>`).join(``)}</section>`}function Y(e){return`<header class="masthead">
      <div class="eyebrow">${n(e.eyebrow)}</div>
      <h1>${n(e.title)}</h1>
      <p class="standfirst">${e.standfirst}</p>
      <div class="provenance">${n(e.date)} · ${t(e)}</div>
      <p><a href="./design.html">&larr; All design notes</a></p>
    </header>
    ${e.render()}`}function X(e){return`<header class="masthead">
      <div class="eyebrow">bikar · design notes</div>
      <h1>No note called “${n(e)}”</h1>
      <p class="standfirst">
        Notes are never deleted, so a link that does not resolve is a link that was never right.
      </p>
      <p><a href="./design.html">&larr; All design notes</a></p>
    </header>`}function Z(e,t){let r=t instanceof Error?t.message:String(t);return`<header class="masthead">
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
    </section>`}function Q(){let e=document.querySelector(`#app`);if(!e)return;let t=new URLSearchParams(window.location.search).get(`n`);if(!t){e.innerHTML=J(),document.title=`Design notes — bikar`;return}let n=q(t);if(!n){e.innerHTML=X(t);return}document.title=`${n.title} — bikar design notes`;try{e.innerHTML=Y(n)}catch(t){e.innerHTML=Z(n,t)}}Q();