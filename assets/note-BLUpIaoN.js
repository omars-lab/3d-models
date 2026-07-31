function e(e){return e.status===`open`?`Open — no decision taken`:e.status===`superseded`?`Superseded — ${e.decision??`see the archive`}`:`Decided — ${e.decision??`see the decisions log`}`}function t(e){return e.replace(/&/g,`&amp;`).replace(/</g,`&lt;`).replace(/>/g,`&gt;`).replace(/"/g,`&quot;`)}function n(e){let n=e.overlaid?`<div class="provenance">Overlaid by hand, not compiled: ${t(e.overlaid)}</div>`:``;return`<figure class="figure">
    ${e.svg}
    <figcaption>${e.caption}</figcaption>
    <div class="provenance">Compiled from <b>${t(e.from)}</b> in your browser, just now.</div>
    ${n}
  </figure>`}export{n,e as r,t};