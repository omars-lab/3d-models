import"./modulepreload-polyfill-CXK8biUa.js";/* empty css               */import{t as e}from"./note-DTXxOHsy.js";var t=[{id:`designer`,name:`Designer`,blurb:`Authors the patterns, pieces and walls, and decides what the catalogue contains.`},{id:`gallery-visitor`,name:`Gallery visitor`,blurb:`Arrived to look, and might leave with an STL.`},{id:`lab-visitor`,name:`Lab visitor`,blurb:`Wants their own version of a part, not the one on the shelf.`},{id:`studio-author`,name:`Studio author`,blurb:`Writes the DSL directly, with the dials and the code in sync.`,elsewhere:`the bikar studio — packages/web, deployed separately`},{id:`print-operator`,name:`Print operator`,blurb:`Owns the machine, the filament and the failures, and needs numbers that survive both.`},{id:`baker`,name:`Baker`,blurb:`Downstream of everything here: a printed cutter and dough.`,elsewhere:`a kitchen. Nothing in this package is for them, and nothing should be`},{id:`qiyas-validator`,name:`qiyas validator`,blurb:`Automated. Diffs renders against ground truth and never opens a page.`,elsewhere:`qiyas, on CI — a page would be the wrong shape of answer entirely`}],n=[{id:`studio`,file:`studio.html`,name:`Studio index`,tagline:`Every page in the studio, who it is for, and what they leave with.`,entry:`src/studio-main.ts`,status:`live`,useCases:[]},{id:`lab`,file:`lab.html`,name:`Orb Lab`,tagline:`Turn an Islamic geometric orb until it is yours, then take the mesh.`,entry:`src/main.ts`,status:`live`,useCases:[{uc:`UC5`,actor:`lab-visitor`,does:`Move the knobs and watch the orb re-solve, with a gate readout that says whether what you just made can actually be printed — then keep the URL, which is the whole configuration.`},{uc:`UC4`,actor:`print-operator`,does:`Download the STL of the orb you configured. It is the same watertight, gate-checked mesh the catalogue ships — configured rather than chosen.`}]},{id:`lego`,file:`lego.html`,name:`Lego Lab`,tagline:`A LEGO-compatible brick, sized for the printer in the room.`,entry:`src/lego-main.ts`,status:`live`,useCases:[{uc:`UC15`,actor:`lab-visitor`,does:`Set the footprint and the clutch fit and see the anchor lattice the solver actually placed — every fit number tagged with whether a measured coupon set it or nobody has measured it yet.`},{uc:`UC15`,actor:`print-operator`,does:`Sweep a fit knob across its range, read where both grid gates stay green, and take the STL at the setting your machine holds — the sweep is the thing you print a strip of and measure.`}]},{id:`breakdown`,file:`breakdown.html`,name:`Orb breakdown`,tagline:`Watch one orb turn, then watch it get built — stage by stage, from the generator’s own frames.`,entry:`src/breakdown-main.ts`,status:`preview`,useCases:[{uc:`UC23`,actor:`gallery-visitor`,does:`See that the flat rosette on the catalogue card really is a sphere — it turns — and then step through the sequence that built it, one face and then one repeat unit at a time, with the count of what is actually visible from that angle.`},{uc:`UC23`,actor:`designer`,does:`Check the construction against what you wrote: every stage is tagged with the DSL constructs that produced it and the moment each one first appears, so a stage that shows up in the wrong act is visible rather than inferred.`}]},{id:`design`,file:`design.html`,name:`Design notes`,tagline:`The argument behind a decision, with the geometry compiled beside it.`,entry:`src/design-main.ts`,status:`preview`,useCases:[{uc:`UC16`,actor:`designer`,does:`Read why a decision went the way it did, against sections cut from the parts the repo builds right now — so the figure and the part cannot quietly disagree, and a note whose argument has expired breaks loudly instead of ageing well.`}]}];function r(e){return t.map(t=>({actor:t,uses:e.useCases.filter(e=>e.actor===t.id)})).filter(e=>e.uses.length>0)}function i(e){return n.map(t=>({page:t,uses:t.useCases.filter(t=>t.actor===e)})).filter(e=>e.uses.length>0)}function a(t){return t.map(t=>`<div class="uc">
        <span class="uc-id" title="use case ${e(t.uc)} in the actor/use-case map">${e(t.uc)}</span>
        <span>${e(t.does)}</span>
      </div>`).join(``)}function o(t){let n=r(t);return n.length===0?`<p>You are on it. This page is the index — it does its work by sending you somewhere
      else, so it carries no use case of its own.</p>`:`<dl class="actor-rows">
    ${n.map(({actor:t,uses:n})=>`<div class="actor-row">
          <dt>${e(t.name)}<small>${e(t.blurb)}</small></dt>
          <dd>${a(n)}</dd>
        </div>`).join(``)}
  </dl>`}function s(t){let n=t.useCases.length===0?``:`<a class="page-open" href="./${e(t.file)}">Open ${e(t.name)} &rarr;</a>`;return`<section class="panel page-card" id="${e(t.id)}">
    <div class="page-head">
      <h2>${e(t.name)}</h2>
      <span class="file">${e(t.file)}</span>
      <span class="status ${t.status}">${e(t.status)}</span>
      <p class="tagline">${e(t.tagline)}</p>
    </div>
    ${o(t)}
    ${n}
  </section>`}function c(t){let n=i(t.id);if(n.length===0)return`<div class="unserved">
      <span class="name">${e(t.name)}</span>
      <span class="where">no page here — ${e(t.elsewhere??`nowhere recorded`)}</span>
    </div>`;let r=n.map(({page:t})=>`<a href="./${e(t.file)}">${e(t.name)}</a>`).join(` · `);return`<div>
    <span class="name">${e(t.name)}</span>
    <span class="where">${r}</span>
  </div>`}function l(e){return[`no`,`One`,`Two`,`Three`,`Four`,`Five`,`Six`,`Seven`][e]??String(e)}function u(){let e=t.filter(e=>i(e.id).length>0).length,r=new Set(n.flatMap(e=>e.useCases.map(e=>e.uc))).size,a=t.length-e;return`<header class="masthead">
      <div class="eyebrow">bikar · studio</div>
      <h1>${l(n.length)} pages, and who each one is for</h1>
      <p class="standfirst">
        Everything below is rendered from <code>src/catalog.ts</code> — the same list the build
        checks its entry points against. A page that exists and is not here fails the test suite,
        and a use case cited here that the actor map does not carry fails the commit. So this is not
        a description of the studio kept beside it; it is the studio, read out.
      </p>
      <div class="provenance">
        ${n.length} pages · ${e} of ${t.length} actors served here · ${r} use cases
      </div>
    </header>

    <section class="page-list">
      ${n.map(s).join(``)}
    </section>

    <section class="panel stack">
      <h2>If you know who you are</h2>
      <p>
        The same map read the other way round. ${l(a)} of these people are real and have
        no page in this package — that is a fact about where the work happens, not a gap waiting to
        be filled.
      </p>
      <div class="actor-index">
        ${t.map(c).join(``)}
      </div>
    </section>

    <p class="foot">
      Use-case ids (<span class="uc-id">UC5</span> and its siblings) are the ones in the
      actor/use-case map at <code>3d-models/.claude/skills/maintain-use-cases/use-cases.md</code>,
      where each is pinned to the code that delivers it at a recorded commit. The pre-commit hook
      there reads the ids off this catalogue and fails if one of them has no entry, so a page cannot
      claim a use case the system has not admitted to having.
    </p>`}function d(){let e=document.querySelector(`#app`);e&&(e.innerHTML=u())}d();