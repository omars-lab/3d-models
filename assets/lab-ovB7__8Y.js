var e=(e,t)=>()=>(t||(e((t={exports:{}}).exports,t),e=null),t.exports);(function(){let e=document.createElement(`link`).relList;if(e&&e.supports&&e.supports(`modulepreload`))return;for(let e of document.querySelectorAll(`link[rel="modulepreload"]`))n(e);new MutationObserver(e=>{for(let t of e)if(t.type===`childList`)for(let e of t.addedNodes)e.tagName===`LINK`&&e.rel===`modulepreload`&&n(e)}).observe(document,{childList:!0,subtree:!0});function t(e){let t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin===`use-credentials`?t.credentials=`include`:e.crossOrigin===`anonymous`?t.credentials=`omit`:t.credentials=`same-origin`,t}function n(e){if(e.ep)return;e.ep=!0;let n=t(e);fetch(e.href,n)}})();var t=e(((e,t)=>{var n=(function(){var e=String.fromCharCode,t=`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=`,n=`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$`,r={};function i(e,t){if(!r[e]){r[e]={};for(var n=0;n<e.length;n++)r[e][e.charAt(n)]=n}return r[e][t]}var a={compressToBase64:function(e){if(e==null)return``;var n=a._compress(e,6,function(e){return t.charAt(e)});switch(n.length%4){default:case 0:return n;case 1:return n+`===`;case 2:return n+`==`;case 3:return n+`=`}},decompressFromBase64:function(e){return e==null?``:e==``?null:a._decompress(e.length,32,function(n){return i(t,e.charAt(n))})},compressToUTF16:function(t){return t==null?``:a._compress(t,15,function(t){return e(t+32)})+` `},decompressFromUTF16:function(e){return e==null?``:e==``?null:a._decompress(e.length,16384,function(t){return e.charCodeAt(t)-32})},compressToUint8Array:function(e){for(var t=a.compress(e),n=new Uint8Array(t.length*2),r=0,i=t.length;r<i;r++){var o=t.charCodeAt(r);n[r*2]=o>>>8,n[r*2+1]=o%256}return n},decompressFromUint8Array:function(t){if(t==null)return a.decompress(t);for(var n=Array(t.length/2),r=0,i=n.length;r<i;r++)n[r]=t[r*2]*256+t[r*2+1];var o=[];return n.forEach(function(t){o.push(e(t))}),a.decompress(o.join(``))},compressToEncodedURIComponent:function(e){return e==null?``:a._compress(e,6,function(e){return n.charAt(e)})},decompressFromEncodedURIComponent:function(e){return e==null?``:e==``?null:(e=e.replace(/ /g,`+`),a._decompress(e.length,32,function(t){return i(n,e.charAt(t))}))},compress:function(t){return a._compress(t,16,function(t){return e(t)})},_compress:function(e,t,n){if(e==null)return``;var r,i,a={},o={},s=``,c=``,l=``,u=2,d=3,f=2,p=[],m=0,h=0,g;for(g=0;g<e.length;g+=1)if(s=e.charAt(g),Object.prototype.hasOwnProperty.call(a,s)||(a[s]=d++,o[s]=!0),c=l+s,Object.prototype.hasOwnProperty.call(a,c))l=c;else{if(Object.prototype.hasOwnProperty.call(o,l)){if(l.charCodeAt(0)<256){for(r=0;r<f;r++)m<<=1,h==t-1?(h=0,p.push(n(m)),m=0):h++;for(i=l.charCodeAt(0),r=0;r<8;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1}else{for(i=1,r=0;r<f;r++)m=m<<1|i,h==t-1?(h=0,p.push(n(m)),m=0):h++,i=0;for(i=l.charCodeAt(0),r=0;r<16;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1}u--,u==0&&(u=2**f,f++),delete o[l]}else for(i=a[l],r=0;r<f;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1;u--,u==0&&(u=2**f,f++),a[c]=d++,l=String(s)}if(l!==``){if(Object.prototype.hasOwnProperty.call(o,l)){if(l.charCodeAt(0)<256){for(r=0;r<f;r++)m<<=1,h==t-1?(h=0,p.push(n(m)),m=0):h++;for(i=l.charCodeAt(0),r=0;r<8;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1}else{for(i=1,r=0;r<f;r++)m=m<<1|i,h==t-1?(h=0,p.push(n(m)),m=0):h++,i=0;for(i=l.charCodeAt(0),r=0;r<16;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1}u--,u==0&&(u=2**f,f++),delete o[l]}else for(i=a[l],r=0;r<f;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1;u--,u==0&&(u=2**f,f++)}for(i=2,r=0;r<f;r++)m=m<<1|i&1,h==t-1?(h=0,p.push(n(m)),m=0):h++,i>>=1;for(;;)if(m<<=1,h==t-1){p.push(n(m));break}else h++;return p.join(``)},decompress:function(e){return e==null?``:e==``?null:a._decompress(e.length,32768,function(t){return e.charCodeAt(t)})},_decompress:function(t,n,r){var i=[],a=4,o=4,s=3,c=``,l=[],u,d,f,p,m,h,g,_={val:r(0),position:n,index:1};for(u=0;u<3;u+=1)i[u]=u;for(f=0,m=2**2,h=1;h!=m;)p=_.val&_.position,_.position>>=1,_.position==0&&(_.position=n,_.val=r(_.index++)),f|=+(p>0)*h,h<<=1;switch(f){case 0:for(f=0,m=2**8,h=1;h!=m;)p=_.val&_.position,_.position>>=1,_.position==0&&(_.position=n,_.val=r(_.index++)),f|=+(p>0)*h,h<<=1;g=e(f);break;case 1:for(f=0,m=2**16,h=1;h!=m;)p=_.val&_.position,_.position>>=1,_.position==0&&(_.position=n,_.val=r(_.index++)),f|=+(p>0)*h,h<<=1;g=e(f);break;case 2:return``}for(i[3]=g,d=g,l.push(g);;){if(_.index>t)return``;for(f=0,m=2**s,h=1;h!=m;)p=_.val&_.position,_.position>>=1,_.position==0&&(_.position=n,_.val=r(_.index++)),f|=+(p>0)*h,h<<=1;switch(g=f){case 0:for(f=0,m=2**8,h=1;h!=m;)p=_.val&_.position,_.position>>=1,_.position==0&&(_.position=n,_.val=r(_.index++)),f|=+(p>0)*h,h<<=1;i[o++]=e(f),g=o-1,a--;break;case 1:for(f=0,m=2**16,h=1;h!=m;)p=_.val&_.position,_.position>>=1,_.position==0&&(_.position=n,_.val=r(_.index++)),f|=+(p>0)*h,h<<=1;i[o++]=e(f),g=o-1,a--;break;case 2:return l.join(``)}if(a==0&&(a=2**s,s++),i[g])c=i[g];else if(g===o)c=d+d.charAt(0);else return null;l.push(c),i[o++]=d+c.charAt(0),a--,d=c,a==0&&(a=2**s,s++)}}};return a})();typeof define==`function`&&define.amd?define(function(){return n}):t!==void 0&&t!=null?t.exports=n:typeof angular<`u`&&angular!=null&&angular.module(`LZString`,[]).factory(`LZString`,function(){return n})}))();function n(e,t){return e.find(e=>e.name===t)}function r(e,t,r){if(!n(t,`inner`)||!n(t,`shoulder`)||e.inner===void 0||e.shoulder===void 0)return;let i=e.shoulder-8;e.inner<=i||(r.push({name:`inner`,from:e.inner,to:i,reason:`inner radius must stay 8 mm under the shoulder`}),e.inner=i)}function i(e,t,r){let i=n(t,`amplitude`);if(!i||!n(t,`strut_depth`)||e.amplitude===void 0||e.strut_depth===void 0)return;let a=(e.strut_depth+.4)/2,o=i.max===void 0?a:Math.min(a,i.max);e.amplitude>=o||(r.push({name:`amplitude`,from:e.amplitude,to:o,reason:`weave amplitude must clear the strut depth`}),e.amplitude=o)}function a(e,t){let n=[];return r(e,t,n),i(e,t,n),n}function o(e){return String(Math.round(e*1e6)/1e6)}function s(e,t){let n=e.trimStart();if(n===``||n.startsWith(`#`))return null;let r=/^(\s*param\s+)([A-Za-z_][A-Za-z0-9_]*)(\s*=\s*)(.*)$/.exec(e);if(!r)return`stop`;if(r[2]!==t)return null;let i=r[4],a=i.indexOf(`#`),o=a>=0?i.slice(0,a):i,s=a>=0?i.slice(a):``,c=/\s(?:range|advanced)\b/.exec(o),l=(c?o.slice(0,c.index):o).replace(/\s+$/,``),u=l.length;return{prefix:r[1]+r[2]+r[3],tail:o.slice(u)+s,isExpression:!/^-?\d+(\.\d+)?$/.test(l)}}function c(e,t,n){let r=e.split(`
`);for(let e=0;e<r.length;e+=1){let i=s(r[e],t);if(i===`stop`)break;if(i!==null)return r[e]=i.prefix+o(n)+i.tail,{source:r.join(`
`),replacedExpression:i.isExpression}}return{source:e,replacedExpression:!1}}var l=`bkr1
`;function u(e){return(0,t.compressToEncodedURIComponent)(l+e)}function d(e){let n;try{n=(0,t.decompressFromEncodedURIComponent)(e)}catch{return null}if(!n||!n.startsWith(l))return null;let r=n.slice(l.length);return r.length>65536?null:r}function f(e){return e.name.replace(/_/g,` `)}function p(e){let t=e.min??Math.min(e.defaultValue/2,e.defaultValue-1),n=e.max??Math.max(e.defaultValue*2,e.defaultValue+1);return{min:t,max:n,step:e.step??Math.max(.1,Math.round((n-t)/100*10)/10)}}function m(e,t,n){let{min:r,max:i,step:a}=p(e),o=document.createElement(`div`);o.className=`knob-row`,o.dataset.knob=e.name;let s=document.createElement(`label`);s.textContent=f(e),s.htmlFor=`knob-${e.name}`;let c=document.createElement(`input`);c.type=`range`,c.id=`knob-${e.name}`,c.min=String(r),c.max=String(i),c.step=String(a),c.value=String(t);let l=document.createElement(`input`);l.type=`number`,l.setAttribute(`aria-label`,`${f(e)} value`),l.min=String(r),l.max=String(i),l.step=String(a),l.value=String(t);let u=document.createElement(`span`);if(u.className=`knob-chip`,u.hidden=!0,e.name===`radius`){let e=e=>{u.textContent=`exceeds your print target`,u.hidden=e<=n.radiusCeilingMm};e(t),o.dataset.radiusChip=`1`,c.addEventListener(`input`,()=>e(Number(c.value))),l.addEventListener(`input`,()=>e(Number(l.value)))}return c.addEventListener(`input`,()=>{l.value=c.value,n.onChange(e.name,Number(c.value))}),l.addEventListener(`change`,()=>{let t=Math.max(r,Math.min(i,Number(l.value)||e.defaultValue));l.value=String(t),c.value=String(t),n.onChange(e.name,t)}),o.append(s,c,l,u),o}function h(e,t,n,r){if(e.textContent=``,t.length===0){let t=document.createElement(`p`);t.className=`knob-empty`,t.textContent=`This script declares no knobs.`,e.append(t);return}let i=t.filter(e=>!e.advanced),a=t.filter(e=>e.advanced);for(let t of i)e.append(m(t,n[t.name]??t.value,r));if(a.length>0){let t=document.createElement(`details`);t.className=`knob-advanced`;let i=document.createElement(`summary`);i.textContent=`Advanced (${a.length})`,t.append(i);for(let e of a)t.append(m(e,n[e.name]??e.value,r));e.append(t)}}function g(e,t){for(let n of e.querySelectorAll(`.knob-row`)){let e=n.dataset.knob;if(!e||t[e]===void 0)continue;let r=n.querySelector(`input[type="range"]`),i=n.querySelector(`input[type="number"]`);r&&(r.value=String(t[e])),i&&(i.value=String(t[e]))}}var _=[{id:`bambu-x1c`,label:`Bambu Lab X1 Carbon (256³)`,xMm:256,yMm:256,zMm:256,process:`fdm`},{id:`bambu-p1s`,label:`Bambu Lab P1S (256³)`,xMm:256,yMm:256,zMm:256,process:`fdm`},{id:`bambu-a1`,label:`Bambu Lab A1 (256³)`,xMm:256,yMm:256,zMm:256,process:`fdm`},{id:`bambu-a1-mini`,label:`Bambu Lab A1 mini (180³)`,xMm:180,yMm:180,zMm:180,process:`fdm`},{id:`prusa-mk4s`,label:`Prusa MK4S (250×210×220)`,xMm:250,yMm:210,zMm:220,process:`fdm`},{id:`prusa-core-one`,label:`Prusa CORE One (250×220×270)`,xMm:250,yMm:220,zMm:270,process:`fdm`},{id:`ender-3`,label:`Creality Ender 3 (220×220×250)`,xMm:220,yMm:220,zMm:250,process:`fdm`},{id:`sls-service`,label:`SLS print service — nylon (300³)`,xMm:300,yMm:300,zMm:300,process:`powder`},{id:`mjf-service`,label:`MJF print service (380×284×380)`,xMm:380,yMm:284,zMm:380,process:`powder`},{id:`custom`,label:`Custom…`,xMm:256,yMm:256,zMm:256,process:`fdm`}];function v(e){return Math.floor((Math.min(e.xMm,e.yMm,e.zMm)-10)/2)}var y=`orbLab.printTarget`;function b(){try{let e=localStorage.getItem(y);if(e){let t=JSON.parse(e),n=_.find(e=>e.id===t.id);if(n&&n.id===`custom`)return{...n,xMm:typeof t.xMm==`number`?t.xMm:n.xMm,yMm:typeof t.yMm==`number`?t.yMm:n.yMm,zMm:typeof t.zMm==`number`?t.zMm:n.zMm};if(n)return n}}catch{}return _[0]}function x(e){try{localStorage.setItem(y,JSON.stringify(e))}catch{}}function S(e,t){return t.find(t=>t.source===e)?.id??null}function C(e,t){let n=[],r=e;for(let e of Object.keys(t).sort()){let i=c(r,e,t[e]);i.replacedExpression&&n.push(e),r=i.source}return{source:r,replacedExpressions:n}}var w=`orbLab.customDraft`;function ee(e,t){try{e.setItem(w,JSON.stringify(t))}catch{}}function T(e){let t={};if(typeof e!=`object`||!e)return t;for(let[n,r]of Object.entries(e))typeof r==`number`&&Number.isFinite(r)&&(t[n]=r);return t}function te(e){try{let t=e.getItem(w);if(!t)return null;let n=JSON.parse(t);if(typeof n!=`object`||!n)return null;let r=n;return typeof r.source==`string`?{source:r.source,overrides:T(r.overrides)}:null}catch{return null}}function ne(e){try{e.removeItem(w)}catch{}}var re=120,ie=class{opts;constructor(e){this.opts=e,e.textarea.addEventListener(`input`,()=>{this.renderGutter(),e.onInput()}),e.textarea.addEventListener(`scroll`,()=>{e.gutter.scrollTop=e.textarea.scrollTop}),e.textarea.addEventListener(`keydown`,e=>this.handleKeydown(e)),e.toggle.addEventListener(`click`,()=>this.isOpen?this.close():this.open()),this.initResize()}get isOpen(){return!this.opts.drawer.hidden}getSource(){return this.opts.textarea.value}setSource(e){this.opts.textarea.value=e,this.renderGutter()}open(){this.opts.drawer.hidden=!1,this.opts.toggle.classList.add(`active`),this.opts.toggle.setAttribute(`aria-expanded`,`true`),this.renderGutter()}close(){this.opts.drawer.hidden=!0,this.opts.toggle.classList.remove(`active`),this.opts.toggle.setAttribute(`aria-expanded`,`false`)}handleKeydown(e){e.key===`Tab`&&(e.preventDefault(),this.opts.textarea.setRangeText(`  `,this.opts.textarea.selectionStart,this.opts.textarea.selectionEnd,`end`),this.renderGutter(),this.opts.onInput())}renderGutter(){let e=this.opts.textarea.value.split(`
`).length,t=[];for(let n=1;n<=e;n+=1)t.push(String(n));this.opts.gutter.textContent=t.join(`
`),this.opts.gutter.scrollTop=this.opts.textarea.scrollTop}initResize(){let{resizeHandle:e,drawer:t}=this.opts,n=0,r=0,i=e=>{let i=Math.round(window.innerHeight*.7),a=Math.min(i,Math.max(re,r+(n-e.clientY)));t.style.height=`${a}px`};e.addEventListener(`pointerdown`,a=>{n=a.clientY,r=t.getBoundingClientRect().height,e.setPointerCapture(a.pointerId),e.addEventListener(`pointermove`,i),e.addEventListener(`pointerup`,()=>e.removeEventListener(`pointermove`,i),{once:!0})})}},E=[{id:`rosette-dodeca`,title:`Rosette · Dodecahedron`,blurb:`10-petal rosettes on 12 pentagonal faces`,source:`# Rosette-Orb — dodecahedral 10-petal rosette sphere.
# Each of the 12 pentagonal faces carries a classical rosette: 10 kite
# petals reaching all 5 corners and all 5 edge midpoints (both shared
# with the neighboring faces, so the lattice closes watertight), joined
# shoulder-to-shoulder on a ring so their inner edges zigzag into a
# 10-pointed star core. 21 voids per face: 10 petals + 10 boundary
# cells + the pierced star core.
# Render with: bikar render Rosette-Orb.bkr --format stl -o out.stl
# Sweep a knob: bikar render Rosette-Orb.bkr --format stl --param inner=50 -o out.stl

# Ranges are the measured gate-PASS envelopes (2026-07 sweep at radius 60);
# keep inner below shoulder - 8 or the petals invert into bowties.
param radius = 60 range 40..110 step 5
param inner = 38 range 16..58 step 2
param shoulder = 60 range 48..76 step 2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_rosette
  # Face pentagon: circumradius 100, corners at 90 + k*72 deg CCW — the
  # canonical orb pattern frame.
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]
  # Midpoint-direction circle: rays at 54 + k*72 aim at edge midpoints.
  circle Cm center(0,0) radius 100
  divide Cm into 5 offset 54
  # Exact edge midpoint = edge chord x center ray (point R0_E4.cpt0).
  line E4 from C0.cpt4 to C0.cpt0
  line R0 from C0.mpt to Cm.cpt0
  # Inner ring (star core) and shoulder ring, 10 points each.
  circle C1 center(0,0) radius $inner
  divide C1 into 10 offset 18
  circle C2 center(0,0) radius $shoulder
  divide C2 into 10 offset 36

pattern pent_rosette on pent_rosette
  edges from pent
  rotate 5 around C0.mpt
    # Corner petal + midpoint petal; adjacent petals share shoulders.
    connect cycle [C0.cpt0 C2.cpt1 C1.cpt2 C2.cpt2]
    connect cycle [R0_E4.cpt0 C2.cpt0 C1.cpt1 C2.cpt1]
  voids detect

orb RosetteOrb
  base dodecahedron
  radius $radius
  inscribe pent_rosette
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:.954},{id:`rosette-cube`,title:`Rosette · Cube`,blurb:`8-petal rosettes on 6 square faces`,source:`# Rosette-Cube-Orb — cubic 8-petal rosette sphere.
# The same rosette construction as Rosette-Orb on the cube's 6 square
# faces: 8 kite petals per face reaching all 4 corners and all 4 edge
# midpoints (both shared with the neighboring faces), joined
# shoulder-to-shoulder so their inner edges zigzag into an 8-pointed
# star core. 17 voids per face: 8 petals + 8 boundary cells + the
# pierced star core.
# Render with: bikar render Rosette-Cube-Orb.bkr --format stl -o out.stl

# Ring ranges carry over from the dodecahedral rosette sweep (same
# pattern-unit frame); keep inner below shoulder - 8 or the petals
# invert into bowties. The mesh gate backstops the square-face extremes.
param radius = 60 range 40..110 step 5
param inner = 38 range 16..58 step 2
param shoulder = 60 range 48..76 step 2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint sq_rosette
  # Face square: circumradius 100, corners at 90 + k*90 deg CCW — the
  # canonical orb pattern frame.
  circle C0 center(0,0) radius 100
  divide C0 into 4 offset 90
  polygon sq [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3]
  # Midpoint-direction circle: rays at 45 + k*90 aim at edge midpoints.
  circle Cm center(0,0) radius 100
  divide Cm into 4 offset 45
  # Exact edge midpoint = edge chord x center ray (point R0_E3.cpt0).
  line E3 from C0.cpt3 to C0.cpt0
  line R0 from C0.mpt to Cm.cpt0
  # Inner ring (star core) and shoulder ring, 8 points each.
  circle C1 center(0,0) radius $inner
  divide C1 into 8 offset 0
  circle C2 center(0,0) radius $shoulder
  divide C2 into 8 offset 22.5

pattern sq_rosette on sq_rosette
  edges from sq
  rotate 4 around C0.mpt
    # Corner petal + midpoint petal; adjacent petals share shoulders.
    connect cycle [C0.cpt0 C2.cpt1 C1.cpt2 C2.cpt2]
    connect cycle [R0_E3.cpt0 C2.cpt0 C1.cpt1 C2.cpt1]
  voids detect

orb RosetteCubeOrb
  base cube
  radius $radius
  inscribe sq_rosette
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:.975},{id:`rosette-weave`,title:`Rosette Weave · Dodecahedron`,blurb:`petals threaded into 10 interlaced chainmail ribbons`,source:`# Rosette-Weave-Orb — dodecahedral woven flower sphere (Family 1).
# Each pentagonal face carries only 5 midpoint kite petals chained
# through shoulders placed under the corners (no face-boundary edges and
# no corner petals — those would make odd-degree nodes, which cannot
# weave). Petals fuse across edge midpoints and around shoulder points,
# and strand tracing threads them into 10 closed ribbons that interlace
# alternately: amplitude 1.6 over a 2.4 ribbon depth leaves a 0.8mm
# clearance, so the print is a linked chainmail flower-ball.
# Render with: bikar render Rosette-Weave-Orb.bkr --format stl -o out.stl

# Ring ranges stay inside the rosette sweet range — the weave adds parity
# and clearance constraints on top of the lattice's, so the envelope is
# narrower than the pierced rosettes'. Keep amplitude at or above
# (strut_depth + 0.4) / 2: the mesh gate is per-tube and cannot see
# ribbon-ribbon interpenetration.
param radius = 60 range 40..110 step 5
param inner = 38 range 24..50 step 2
param shoulder = 60 range 48..70 step 2
param amplitude = 1.6 range 1.4..2.6 step 0.2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_flower
  # Canonical circumradius-100 pentagon frame (corners at 90 + k*72 CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]
  # Midpoint-direction circle: rays at 54 + k*72 aim at edge midpoints.
  circle Cm center(0,0) radius 100
  divide Cm into 5 offset 54
  # Exact edge midpoint = edge chord x center ray (point R0_E4.cpt0).
  line E4 from C0.cpt4 to C0.cpt0
  line R0 from C0.mpt to Cm.cpt0
  # Inner ring under the midpoints; shoulder ring under the corners.
  circle C1 center(0,0) radius $inner
  divide C1 into 5 offset 54
  circle C2 center(0,0) radius $shoulder
  divide C2 into 5 offset 90

pattern pent_flower on pent_flower
  rotate 5 around C0.mpt
    connect cycle [R0_E4.cpt0 C2.cpt4 C1.cpt0 C2.cpt0]
  voids detect

orb RosetteWeaveOrb
  base dodecahedron
  radius $radius
  inscribe pent_flower
  project spherical
  struts width $strut_width depth $strut_depth
  weave crossing alternating amplitude $amplitude
`,qiyasComposite:1},{id:`hankin-dodeca`,title:`Hankin · Dodecahedron`,blurb:`polygons-in-contact stars — dial the contact angle`,source:`# Hankin-Orb — dodecahedral polygons-in-contact star sphere (Kaplan 2005,
# Bonner's Hankin method). Each pentagonal face launches two rays from
# every edge midpoint at the contact angle theta to the edge; adjacent
# rays intersect to form a five-pointed central star with kite cells at
# the corners. The contact points are the edge midpoints — shared with
# the neighboring face — so the lattice closes watertight across every
# edge for any theta in the calibrated range.
# Render with: bikar render Hankin-Orb.bkr --format stl -o out.stl
# Sweep the star: bikar render Hankin-Orb.bkr --format stl --param theta=36 -o out.stl

# theta detents worth trying: 36 (the pentagon's natural k*180/5 angle),
# 54 (ideal angle 90 - 180/5 — the classical balanced star, default),
# 72 (fat/obtuse family). Range 18..80 is the measured gate-PASS envelope
# across the full radius and strut-width ranges; outside it the corner
# kites collapse below the strut inset limit and the engine reports the
# degeneracy.
param radius = 60 range 40..110 step 5
param theta = 54 range 18..80 step 1
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_hankin
  # Canonical circumradius-100 pentagon frame (corners at 90 + k*72 CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]

pattern pent_pic on pent_hankin
  edges from pent
  hankin angle $theta on C0
  voids detect

orb HankinOrb
  base dodecahedron
  radius $radius
  inscribe pent_pic
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:1},{id:`star-icosa`,title:`Star · Icosahedron`,blurb:`hexagrams on 20 triangular faces`,source:`# Star-Orb — icosahedral pierced-lattice sphere (the M0 spike, in DSL).
# Each of the 20 triangular faces carries a {6/2} hexagram whose
# alternating tips land exactly on the triangle's edge midpoints, so the
# lattice connects across every face boundary and the shell closes
# watertight. Render with: bikar render Star-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 — its tips must land
# exactly on the edge midpoints or the cross-face weld fails — so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_face
  # Face triangle: circumradius 100, corners at 90/210/330 deg — the
  # canonical orb pattern frame (corners at 90 + k*120, CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 3 offset 90
  polygon tri [C0.cpt0 C0.cpt1 C0.cpt2]
  # Inradius circle: its 6 points are the 3 edge midpoints (at 30/150/270)
  # plus 3 points under the corners — the hexagram's tips.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_star on tri_face
  edges from tri
  connect every 2 on C1
  voids detect

orb StarOrb
  base icosahedron
  radius $radius
  inscribe tri_star
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:1},{id:`star-dodeca`,title:`Star · Dodecahedron`,blurb:`corner-to-corner pentagrams on 12 pentagonal faces`,source:`# Dodeca-Orb — dodecahedral pierced-lattice sphere with a 5-fold star.
# Each of the 12 pentagonal faces (pattern circumradius 100, corners at
# 90 + k*72 deg CCW) carries a corner-to-corner pentagram {5/2}: every
# strut ends on a face corner or runs along a face edge, both shared with
# the neighboring faces, so the lattice closes watertight (11 voids per
# face: 5 star tips + 5 edge regions + the central pentagon).
# Render with: bikar render Dodeca-Orb.bkr --format stl -o out.stl

# The pentagram runs corner-to-corner on the fixed face frame, so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_face
  circle C0 center(0,0) radius 100
  divide C0 into 5 offset 90
  polygon pent [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3 C0.cpt4]

pattern pent_star on pent_face
  edges from pent
  connect every 2 on C0
  voids detect

orb DodecaOrb
  base dodecahedron
  radius $radius
  inscribe pent_star
  project spherical
  struts width $strut_width depth $strut_depth
`,qiyasComposite:1},{id:`star-cube`,title:`Star · Cube`,blurb:`{8/3} octagrams on 6 square faces`,source:`# Star-Cube-Orb — cubic pierced-lattice sphere with an {8/3} octagram.
# Each of the 6 square faces carries an eight-pointed star whose tips sit
# on the face's inradius circle: 4 land exactly on the edge midpoints
# (shared with the neighboring faces) and 4 under the corners, so the
# lattice closes watertight across every edge.
# Render with: bikar render Star-Cube-Orb.bkr --format stl -o out.stl

# The octagram circle stays at the fixed inradius 100*cos(45) — its
# midpoint tips must land exactly on the edge midpoints or the cross-face
# weld fails — so the pattern itself has no knobs; only the print
# dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint sq_star_face
  # Canonical circumradius-100 square frame (corners at 90 + k*90 CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 4 offset 90
  polygon sq [C0.cpt0 C0.cpt1 C0.cpt2 C0.cpt3]
  # Inradius circle: its 8 points are the 4 edge midpoints (at 45 + k*90)
  # plus 4 points under the corners — the octagram's tips.
  circle C1 center(0,0) radius 70.7106781187
  divide C1 into 8 offset 45

pattern sq_octagram on sq_star_face
  edges from sq
  connect every 3 on C1
  voids detect

orb StarCubeOrb
  base cube
  radius $radius
  inscribe sq_octagram
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:1},{id:`star-octa`,title:`Star · Octahedron`,blurb:`bold hexagrams on 8 large triangular faces`,source:`# Star-Octa-Orb — octahedral pierced-lattice sphere with a {6/2} hexagram.
# The same canonical triangle-face hexagram as Star-Orb, on the
# octahedron's 8 faces: alternating tips land exactly on the triangle's
# edge midpoints, so the lattice connects across every face boundary and
# the shell closes watertight. Fewer, larger faces than the icosahedral
# Star-Orb give a bolder, more open star field.
# Render with: bikar render Star-Octa-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 — its tips must land
# exactly on the edge midpoints or the cross-face weld fails — so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_face
  # Face triangle: circumradius 100, corners at 90/210/330 deg — the
  # canonical orb pattern frame (corners at 90 + k*120, CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 3 offset 90
  polygon tri [C0.cpt0 C0.cpt1 C0.cpt2]
  # Inradius circle: its 6 points are the 3 edge midpoints (at 30/150/270)
  # plus 3 points under the corners — the hexagram's tips.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_star on tri_face
  edges from tri
  connect every 2 on C1
  voids detect

orb StarOctaOrb
  base octahedron
  radius $radius
  inscribe tri_star
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:.992},{id:`star-tetra`,title:`Star · Tetrahedron`,blurb:`four quarter-sphere hexagrams — the minimal base`,source:`# Star-Tetra-Orb — tetrahedral pierced-lattice sphere with a {6/2} hexagram.
# The same canonical triangle-face hexagram as Star-Orb, on the
# tetrahedron's 4 faces: alternating tips land exactly on the triangle's
# edge midpoints, so the lattice connects across every face boundary and
# the shell closes watertight. The minimal base — 4 giant faces whose
# spherical projection stretches each star across a full quarter-sphere.
# Render with: bikar render Star-Tetra-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 — its tips must land
# exactly on the edge midpoints or the cross-face weld fails — so the
# pattern itself has no knobs; only the print dimensions do.
param radius = 60 range 40..110 step 5
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_face
  # Face triangle: circumradius 100, corners at 90/210/330 deg — the
  # canonical orb pattern frame (corners at 90 + k*120, CCW).
  circle C0 center(0,0) radius 100
  divide C0 into 3 offset 90
  polygon tri [C0.cpt0 C0.cpt1 C0.cpt2]
  # Inradius circle: its 6 points are the 3 edge midpoints (at 30/150/270)
  # plus 3 points under the corners — the hexagram's tips.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_star on tri_face
  edges from tri
  connect every 2 on C1
  voids detect

orb StarTetraOrb
  base tetrahedron
  radius $radius
  inscribe tri_star
  project spherical
  struts width $strut_width depth $strut_depth
  pierce voids
`,qiyasComposite:1},{id:`weave-icosa`,title:`Weave · Icosahedron`,blurb:`26 interlaced great-circle and triangle ribbons`,source:`# Weave-Orb — icosahedral woven-strapwork sphere (Family 1).
# Each face carries only the {6/2} hexagram (no face-boundary edges — those
# would make degree-6 nodes, which cannot weave). The hexagram's medial
# triangle connects the face's edge midpoints, so its edges run straight
# through into adjacent faces and close into 6 great-circle ribbons (the
# icosidodecahedron's equators); the other triangle stays interior, giving
# 20 small triangular ribbons. All 26 ribbons interlace alternately:
# amplitude 1.6 over a 2.4 ribbon depth leaves a 0.8mm clearance, so the
# print is a genuinely linked chainmail ball, not a fused lattice.
# Render with: bikar render Weave-Orb.bkr --format stl -o out.stl

# The hexagram circle stays at the fixed inradius 50 (tips must land on
# edge midpoints for cross-face closure). Keep amplitude at or above
# (strut_depth + 0.4) / 2 — the mesh gate is per-tube and cannot see
# ribbon-ribbon interpenetration, so a too-small amplitude fuses the
# chainmail silently.
param radius = 60 range 40..110 step 5
param amplitude = 1.6 range 1.4..2.6 step 0.2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint tri_weave_face
  # Inradius circle of the canonical circumradius-100 triangle frame: its
  # 6 points are the 3 edge midpoints (at 30/150/270) plus 3 inner points
  # under the corners — the hexagram's vertices.
  circle C1 center(0,0) radius 50
  divide C1 into 6 offset 30

pattern tri_hexagram on tri_weave_face
  connect every 2 on C1

orb WeaveOrb
  base icosahedron
  radius $radius
  inscribe tri_hexagram
  project spherical
  struts width $strut_width depth $strut_depth
  weave crossing alternating amplitude $amplitude
`,qiyasComposite:.997},{id:`weave-dodeca`,title:`Weave · Dodecahedron`,blurb:`pentagram chords woven into chainmail ribbons`,source:`# Weave-Dodeca-Orb — dodecahedral woven pentagram sphere (Family 1).
# Each pentagonal face carries only a {5/2} pentagram connecting the 5
# edge midpoints (no face-boundary edges — those would make odd-degree
# nodes, which cannot weave). Midpoints are degree 2 in-face and weld to
# degree 4 across the edge, so strand tracing runs each chord straight
# through into the neighboring face, closing the lattice into ribbons
# that interlace alternately — a linked chainmail star-ball.
# Render with: bikar render Weave-Dodeca-Orb.bkr --format stl -o out.stl

# Keep amplitude at or above (strut_depth + 0.4) / 2 — the mesh gate is
# per-tube and cannot see ribbon-ribbon interpenetration, so a too-small
# amplitude fuses the chainmail silently.
param radius = 60 range 40..110 step 5
param amplitude = 1.6 range 1.4..2.6 step 0.2
param strut_width = 3 range 1.5..6 step 0.5 advanced
param strut_depth = 2.4 range 1.2..4 step 0.2 advanced

blueprint pent_weave_face
  # Midpoint circle of the canonical circumradius-100 pentagon frame
  # (corners at 90 + k*72): inradius 100*cos(36), midpoints at 126 + k*72.
  circle C1 center(0,0) radius 80.9016994375
  divide C1 into 5 offset 126

pattern pent_pentagram on pent_weave_face
  connect every 2 on C1
  voids detect

orb WeaveDodecaOrb
  base dodecahedron
  radius $radius
  inscribe pent_pentagram
  project spherical
  struts width $strut_width depth $strut_depth
  weave crossing alternating amplitude $amplitude
  pierce voids
`,qiyasComposite:1}],ae=`rosette-dodeca`;function D(e){return E.find(t=>t.id===e)}function oe(){let e=new URLSearchParams(window.location.search),t={},n=null,r=null;for(let[i,a]of e)if(i!==`v`){if(i===`f`){n=a;continue}if(i===`code`){r=a;continue}t[i]=a}return{scriptId:n,code:r,rawParams:t}}function se(e){return String(Math.round(e*1e6)/1e6)}function ce(e,t,n){let r=new URLSearchParams;r.set(`v`,`1`),r.set(`f`,e);for(let e of t){let t=n[e.name];t===void 0||t===e.defaultValue||r.set(e.name,se(t))}return r}function le(e){return window.location.origin.length+window.location.pathname.length+1+e.toString().length}function ue(e,t,n,r,i){let a=ce(e,t,n),o=!1,s=le(a);i&&(a.set(`code`,i),s=le(a),s<=1800?o=!0:a.delete(`code`));let c=`${window.location.pathname}?${a.toString()}`;return r===`push`?history.pushState(null,``,c):history.replaceState(null,``,c),{codeIncluded:o,hrefLength:s}}var de=class{canvas;mesh=null;yaw=-.6;pitch=.35;zoom=1;frame=0;constructor(e){this.canvas=e,this.attachPointerHandlers(),this.attachWheelHandler(),window.addEventListener(`resize`,()=>{this.fitCanvas(),this.redraw()}),this.fitCanvas()}setMesh(e){this.mesh=e,this.redraw()}fitCanvas(){let e=window.devicePixelRatio||1,t=this.canvas.parentElement,n=Math.max(280,Math.min(720,(t?.clientWidth??640)-16,(t?.clientHeight??640)-16));this.canvas.width=Math.round(n*e),this.canvas.height=Math.round(n*e),this.canvas.style.width=`${n}px`,this.canvas.style.height=`${n}px`}redraw(){this.frame||=requestAnimationFrame(()=>{this.frame=0,this.draw()})}project(e){let t=Math.cos(this.yaw),n=Math.sin(this.yaw),r=Math.cos(this.pitch),i=Math.sin(this.pitch),a=e.vertices,o=a.length,s=new Float64Array(o),c=new Float64Array(o),l=new Float64Array(o),u=0;for(let e=0;e<o;e++){let o=a[e];u=Math.max(u,Math.hypot(o.x,o.y,o.z));let d=t*o.x+n*o.z,f=t*o.z-n*o.x;s[e]=d,c[e]=r*o.y-i*f,l[e]=i*o.y+r*f}return{xs:s,ys:c,zs:l,maxLen:u}}draw(){let e=this.mesh,t=this.canvas.getContext(`2d`);if(!e||!t)return;let n=this.canvas.width;t.clearRect(0,0,n,n);let{xs:r,ys:i,zs:a,maxLen:o}=this.project(e),s=n/2,c=(s-12)/(o||1)*this.zoom,l=e.triangles,u=new Float64Array(l.length);for(let e=0;e<l.length;e++){let[t,n,r]=l[e];u[e]=a[t]+a[n]+a[r]}let d=l.map((e,t)=>t);d.sort((e,t)=>u[e]-u[t]);let f=Math.hypot(.35,.55,.76),p=-.35/f,m=.55/f,h=.76/f;for(let e of d){let[n,o,u]=l[e],d=r[o]-r[n],f=i[o]-i[n],g=a[o]-a[n],_=r[u]-r[n],v=i[u]-i[n],y=a[u]-a[n],b=f*y-g*v,x=g*_-d*y,S=d*v-f*_,C=Math.hypot(b,x,S);if(C===0)continue;b/=C,x/=C,S/=C;let w=S>0,ee=w?b*p+x*m+S*h:-(b*p+x*m+S*h),T=.4+.6*Math.max(0,ee),te=w?`rgb(${Math.round(214*T)},${Math.round(178*T)},${Math.round(84*T)})`:`rgb(${Math.round(105*T)},${Math.round(82*T)},${Math.round(40*T)})`;t.beginPath(),t.moveTo(s+r[n]*c,s-i[n]*c),t.lineTo(s+r[o]*c,s-i[o]*c),t.lineTo(s+r[u]*c,s-i[u]*c),t.closePath(),t.fillStyle=te,t.strokeStyle=te,t.lineWidth=1,t.fill(),t.stroke()}}attachPointerHandlers(){let e=!1,t=0,n=0;this.canvas.addEventListener(`pointerdown`,r=>{e=!0,t=r.clientX,n=r.clientY,this.canvas.setPointerCapture(r.pointerId),this.canvas.classList.add(`dragging`)}),this.canvas.addEventListener(`pointermove`,r=>{e&&(this.yaw+=(r.clientX-t)*.01,this.pitch=Math.max(-1.5,Math.min(1.5,this.pitch+(r.clientY-n)*.01)),t=r.clientX,n=r.clientY,this.redraw())}),this.canvas.addEventListener(`pointerup`,t=>{e=!1,this.canvas.releasePointerCapture(t.pointerId),this.canvas.classList.remove(`dragging`)})}attachWheelHandler(){this.canvas.addEventListener(`wheel`,e=>{e.preventDefault(),this.zoom=Math.max(.4,Math.min(3,this.zoom*Math.exp(-e.deltaY*.0015))),this.redraw()},{passive:!1})}},fe=15e3,pe=6e4,me=[/\bsubdivide\s+[34]\b/,/\bgirih\s+field\b/,/\bshells\s+\d/,/\brepeat\b.*\bdepth\s+[3-9]\b/,/\bdivide\b.*\binto\s+\d{3,}\b/,/\btile\s+grid\b/];function he(e){return me.some(t=>t.test(e))?pe:fe}function ge(e,t){return e.source===t.source&&JSON.stringify(e.params)===JSON.stringify(t.params)}function _e(e,t){return e===`stop`?`Evaluation stopped.`:e===`crash`?"The evaluation crashed its worker (likely out of memory) — reduce `subdivide`, `shells`, or repeat depth.":`Evaluation exceeded ${Math.round(t/1e3)} s and was stopped — reduce \`subdivide\`, \`shells\`, or repeat depth, or download the .bkr and render it with the bikar CLI.`}var ve=class{opts;worker;generation=0;lastGood=null;primedFlag=!1;primingSeq=null;inflight=new Map;latestEvalSeq=0;latestBudgetMs=fe;deadlineTimer;deadlineSeq=null;held=[];constructor(e){this.opts=e,this.worker=this.attach(e.spawn())}get primed(){return this.primedFlag}evaluate(e){let t={...e,generation:this.generation};this.inflight.set(t.seq,t),this.latestEvalSeq=t.seq,this.latestBudgetMs=(this.opts.budgetMs??he)(t.source),this.worker.postMessage(t),this.armDeadline(t.seq,this.latestBudgetMs)}request(e){let t={...e,generation:this.generation};if(!this.primedFlag){this.held.push(t);return}this.worker.postMessage(t)}stop(){this.deadlineSeq!==null&&this.kill(`stop`)}attach(e){return e.onmessage=e=>this.handleReply(e.data),e.onerror=()=>this.kill(`crash`),e.onmessageerror=()=>this.kill(`crash`),e}armDeadline(e,t){this.clearDeadline(),this.deadlineSeq=e,this.deadlineTimer=setTimeout(()=>this.kill(`timeout`),t)}clearDeadline(){this.deadlineTimer!==void 0&&clearTimeout(this.deadlineTimer),this.deadlineTimer=void 0,this.deadlineSeq=null}setPrimed(e){if(this.primedFlag=e,!e)return;let t=this.held;this.held=[];for(let e of t)this.worker.postMessage({...e,generation:this.generation})}handleReply(e){e.generation===this.generation&&((e.type===`result`||e.type===`error`)&&this.settleEvaluate(e)||this.opts.onMessage(e))}settleEvaluate(e){if(e.seq===this.deadlineSeq&&this.clearDeadline(),this.primingSeq!==null&&e.seq===this.primingSeq)return this.finishPriming(e.type===`result`),!0;e.type===`result`&&(this.lastGood=this.inflight.get(e.seq)??this.lastGood,this.setPrimed(!0));for(let t of this.inflight.keys())t<=e.seq&&this.inflight.delete(t);return!1}finishPriming(e){if(this.primingSeq=null,e){this.setPrimed(!0);return}this.lastGood=null}kill(e){let t=this.latestBudgetMs,n=this.primingSeq!==null,r=this.inflight.get(this.latestEvalSeq)??null;this.clearDeadline(),this.worker.terminate(),this.generation+=1,this.inflight.clear(),this.primingSeq=null,this.primedFlag=!1,this.worker=this.attach(this.opts.spawn()),this.opts.onMessage({type:`error`,seq:this.latestEvalSeq,generation:this.generation,message:_e(e,t)}),this.reprime(n,r)}reprime(e,t){if(e){this.lastGood=null;return}if(!this.lastGood)return;if(t&&ge(this.lastGood,t)){this.lastGood=null;return}let n={...this.lastGood,generation:this.generation};this.primingSeq=n.seq,this.worker.postMessage(n),this.armDeadline(n.seq,(this.opts.budgetMs??he)(n.source))}};function O(e){let t=document.querySelector(e);if(!t)throw Error(`Orb Lab markup is missing ${e}`);return t}var ye=O(`#knob-panel`),k=O(`#archetype-chips`),A=O(`#machine-select`),be=O(`#custom-dims`),xe=O(`#dim-x`),j=O(`#dim-y`),M=O(`#dim-z`),Se=O(`#target-note`),Ce=O(`#process-note`),we=O(`#stl-button`),N=O(`#copy-link`),P=O(`#gate-panel`),Te=O(`#error-panel`),Ee=O(`#spinner`),De=O(`#spinner-label`),F=O(`#stop-button`),Oe=O(`#toast`),ke=O(`#view-tabs`),Ae=O(`#axis-view`),je=O(`#orb-canvas`),Me=O(`#bake-button`),Ne=O(`#bkr-download`),Pe=O(`#open-studio`),Fe=O(`#drawer-hide`),Ie=`https://bikar-studio.pages.dev/editor`,Le=new de(je),Re=Number(new URLSearchParams(window.location.search).get(`budgetMs`))||0,I=new ve({spawn:()=>new Worker(new URL(``+new URL(`worker-BpkFWDq2.js`,import.meta.url).href,``+import.meta.url),{type:`module`}),onMessage:e=>St(e),...Re>0?{budgetMs:()=>Re}:{}}),L=`preset`,R=ae,z=[],ze=``,B={},V=new Set,H=b(),Be=null,U=`3d`,Ve=``,W=null,G=0,He=0,Ue=0,We=0,K=!1,Ge=0,Ke=0,qe=0,Je=0,Ye=0;function q(e){Oe.textContent=e,Oe.hidden=!1,window.clearTimeout(Ye),Ye=window.setTimeout(()=>{Oe.hidden=!0},3600)}function Xe(){return L===`custom`?Q.getSource():(D(R)??E[0]).source}function J(){let e={};for(let t of V)B[t]!==void 0&&(e[t]=B[t]);return e}function Y(){let e=Xe();G+=1,Ue=G,De.textContent=he(e)===6e4?`computing — this design is large, may take up to a minute…`:`computing…`,I.evaluate({type:`evaluate`,seq:G,source:e,params:J()}),window.clearTimeout(qe),qe=window.setTimeout(()=>{Ee.hidden=!1},300),window.clearTimeout(Je),F.hidden=!0,Je=window.setTimeout(()=>{F.hidden=!1},2300)}function Ze(){window.clearTimeout(qe),window.clearTimeout(Je),Ee.hidden=!0,F.hidden=!0}var X=null;function Z(e){if(L===`custom`){let t=Q.getSource();X=ue(`custom`,z,B,e,u(t)),ee(window.localStorage,{source:t,overrides:J()})}else X=ue(R,z,B,e);it()}function Qe(){h(ye,z,B,{radiusCeilingMm:v(H),onChange:$e})}function $e(e,t){B[e]=t,V.add(e),K=!1;let n=a(B,z);for(let e of n)V.add(e.name);n.length>0&&g(ye,B),window.clearTimeout(Ge),Ge=window.setTimeout(()=>{Y(),Z(`replace`)},200)}function et(){window.clearTimeout(Ke),Ke=window.setTimeout(()=>{K=!1,tt()},500)}var Q=new ie({drawer:O(`#code-drawer`),textarea:O(`#code-editor`),gutter:O(`#editor-gutter`),toggle:O(`#code-toggle`),resizeHandle:O(`#drawer-resize`),onInput:et});function tt(){let e=S(Q.getSource(),E);if(e){let t=L===`custom`||R!==e;L=`preset`,R=e,ne(window.localStorage),t&&$(),Z(`replace`)}else{let e=L===`preset`;L=`custom`,e&&$(),Z(e?`push`:`replace`)}Y()}function nt(){let e=J();if(Object.keys(e).length===0){q(`All knob values already match the code defaults`);return}let t=C(Q.getSource(),e);if(t.replacedExpressions.length>0){let e=t.replacedExpressions.join(`, `);if(!window.confirm(`Writing values will replace derived defaults (${e}) with plain numbers. Continue?`))return}V.clear(),Q.setSource(t.source),K=!1,tt(),q(`Knob values written into the code`)}function rt(){let e=C(Q.getSource(),J()),t=new Blob([e.source],{type:`text/plain`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=`${L===`custom`?`custom-orb`:R}.bkr`,r.click(),URL.revokeObjectURL(n)}function it(){if(Pe.href=`${Ie}#code/${u(Xe())}`,L===`custom`&&X&&!X.codeIncluded){N.disabled=!0,N.title=`Too large to share as a link (${X.hrefLength} chars) — Download .bkr instead. Tip: trimming comments usually gets a script back under the line.`;return}N.disabled=!1,N.title=L===`custom`?`Anyone with this link gets your exact orb — the code rides in the URL`:``}function at(e){if(e.family!==`weave`)return[];let t=[];e.strandCount!==null&&t.push([`ribbons`,`${e.strandCount} interlocked`]);let n=B.amplitude,r=B.strut_depth;if(n!==void 0&&r!==void 0){let e=2*n-r;t.push([`ribbon gap`,`${e.toFixed(1)} mm ${e>=.4?`✓`:`✗ fused`}`])}return t}function ot(){let e=document.createElement(`div`);if(e.className=`trust-badge`,L===`custom`)return e.classList.add(`custom`),e.textContent=`custom design — not qiyas-validated`,e.title=`The mesh gate above is the entire claim. To score a custom design offline: bikar render <file.bkr> --format views, then qiyas orb-validate on the output.`,e;let t=(D(R)??E[0]).qiyasComposite.toFixed(3);return[...V].every(e=>{let t=z.find(t=>t.name===e);return t===void 0||B[e]===t.defaultValue})?(e.classList.add(`validated`),e.textContent=`qiyas-validated ✓ ${t}`,e.title=`CI score of this committed script at declared defaults (composite gate ≥ 0.95)`):(e.classList.add(`range`),e.textContent=`calibrated range`,e.title=`Knobs moved within the gate-swept envelope — the qiyas score (${t}) was measured at declared defaults.`),e}function st(e){let{gate:t,mesh:n}=e;P.textContent=``,P.dataset.tris=String(n.triangles.length);let r=document.createElement(`div`);r.className=t.passed?`gate-badge pass`:`gate-badge fail`,r.textContent=t.passed?`PASS — printable`:`FAIL`,P.append(r,ot());let i=[[`watertight`,t.watertight?`yes`:`NO`],[`triangles`,String(n.triangles.length)],[`volume`,`${(n.stats.volumeMm3/1e3).toFixed(1)} cm³`],[`min feature`,`${t.minFeatureMm.toFixed(2)} mm (declared ${t.declaredMinFeatureMm.toFixed(2)} mm)`],...at(e)],a=document.createElement(`dl`);for(let[e,t]of i){let n=document.createElement(`dt`);n.textContent=e;let r=document.createElement(`dd`);r.textContent=t,a.append(n,r)}P.append(a);for(let e of t.failures){let t=document.createElement(`p`);t.className=`gate-failure`,t.textContent=e,P.append(t)}}function ct(e){Te.textContent=e,Te.hidden=!1,we.disabled=!0}function lt(){G+=1,We=G,I.request({type:`views`,seq:G})}function ut(){let e=W?.find(e=>e.id===U);e&&(Ae.innerHTML=e.svg)}function dt(){if(W){ut();return}lt()}function ft(e){U=e;for(let t of ke.querySelectorAll(`button`)){let n=t.dataset.view===e;t.classList.toggle(`active`,n),t.setAttribute(`aria-selected`,n?`true`:`false`)}let t=e===`3d`;je.hidden=!t,Ae.hidden=t,t||dt()}function pt(e){ke.textContent=``;let t=[{id:`3d`,label:`3D`,title:`Interactive preview — drag to rotate`},...e.map(e=>({id:e.id,label:e.id,title:`${e.fold}-fold symmetry axis — the view qiyas validates`}))];for(let e of t){let t=document.createElement(`button`);t.className=`view-tab`,t.dataset.view=e.id,t.setAttribute(`role`,`tab`),t.textContent=e.label,t.title=e.title,t.addEventListener(`click`,()=>ft(e.id)),ke.append(t)}}function mt(){let e=Be===`weave`&&H.process===`fdm`;Ce.hidden=!e,e&&(Ce.textContent=`Interlocked ribbons print pre-assembled only on powder systems — pick an SLS/MJF service for this design, or print it as a keepsake that needs support surgery.`)}function ht(e){Be=e.family,W=null;let t=e.viewAxes.map(e=>e.id).join(`,`);t!==Ve&&(Ve=t,pt(e.viewAxes)),ft(U===`3d`||e.viewAxes.some(e=>e.id===U)?U:`3d`),mt()}function gt(e){for(let t of e)t.dropped?(V.delete(t.name),delete B[t.name]):B[t.name]=t.to}function _t(){let e=a(B,z);if(e.length===0)return K=!1,0;for(let t of e)V.add(t.name);return K||(K=!0,Y(),Z(`replace`)),e.length}function vt(){let e=z.map(e=>[e.name,e.min,e.max,e.step,e.advanced].join(`|`)).join(`;`);if(e!==ze){ze=e,Qe();return}g(ye,B)}function yt(e){z=e.specs,gt(e.adjustments);for(let e of z)V.has(e.name)||(B[e.name]=e.value);let t=_t(),n=e.adjustments.length+t;n>0&&q(`Adjusted ${n} parameter${n===1?``:`s`} to printable values`),Te.hidden=!0,Le.setMesh(e.mesh),st(e),ht(e),we.disabled=!e.gate.passed,vt(),Z(`replace`)}function bt(){let e=L===`custom`?`custom-orb`:R;for(let t of z){let n=B[t.name];n===void 0||n===t.defaultValue||(e+=`-${t.name}${String(Math.round(n*1e6)/1e6)}`)}return`${e}.stl`}function xt(e){let t=new Blob([e],{type:`model/stl`}),n=URL.createObjectURL(t),r=document.createElement(`a`);r.href=n,r.download=bt(),r.click(),URL.revokeObjectURL(n)}function St(e){if(e.type===`stl`){xt(e.data);return}if(e.type===`views`){e.seq===We&&(W=e.views,U!==`3d`&&ut());return}if(e.seq===Ue&&Ze(),!(e.seq<=He)){if(He=e.seq,e.type===`error`){ct(e.message);return}yt(e)}}function Ct(e){if(L===`preset`&&e===R)return;let t=D(e)??E[0];L===`custom`&&!window.confirm(`Discard your custom orb and load ${t.title}? Your code is still at the previous link (Back button) until you edit again.`)||(L=`preset`,R=t.id,V.clear(),B={},z=[],ze=``,K=!1,Q.setSource(t.source),$(),ue(R,[],{},`push`),Y())}function $(){k.textContent=``;for(let e of E){let t=document.createElement(`button`);t.className=L===`preset`&&e.id===R?`chip active`:`chip`,t.textContent=e.title,t.title=e.blurb,t.addEventListener(`click`,()=>Ct(e.id)),k.append(t)}if(L===`custom`){let e=document.createElement(`button`);e.className=`chip active`,e.textContent=`Custom orb`,e.title=`Your edited script — not one of the committed presets`,k.append(e)}it()}function wt(){Se.textContent=`Largest printable radius: ${v(H)} mm (${H.xMm}×${H.yMm}×${H.zMm} mm build volume, 10 mm margin)`}function Tt(){let e=(e,t)=>{let n=Number(e.value);return Number.isFinite(n)&&n>=50?n:t};return{xMm:e(xe,256),yMm:e(j,256),zMm:e(M,256)}}function Et(e){let t=_.find(t=>t.id===e)??_[0];be.hidden=t.id!==`custom`,H=t.id===`custom`?{...t,...Tt()}:t,x(H),wt(),mt(),Qe()}function Dt(){for(let e of _){let t=document.createElement(`option`);t.value=e.id,t.textContent=e.label,A.append(t)}A.value=H.id,be.hidden=H.id!==`custom`,xe.value=String(H.xMm),j.value=String(H.yMm),M.value=String(H.zMm),wt(),A.addEventListener(`change`,()=>Et(A.value));for(let e of[xe,j,M])e.addEventListener(`change`,()=>Et(`custom`))}function Ot(e){let t=0;for(let[n,r]of Object.entries(e)){let e=Number(r);if(!Number.isFinite(e)){t+=1;continue}B[n]=e,V.add(n)}t>0&&q(`Ignored ${t} non-numeric link value${t===1?``:`s`}`)}function kt(e){if(e!==null){let t=d(e);if(t===null){q(`This share link is damaged — it may have been truncated by a chat app. Ask the sender for the .bkr file instead.`);return}L=`custom`,Q.setSource(t),Q.open();return}let t=te(window.localStorage);if(t){L=`custom`,Q.setSource(t.source),Q.open();for(let[e,n]of Object.entries(t.overrides))B[e]=n,V.add(e)}}function At(e){if(e.scriptId===`custom`){kt(e.code);return}e.scriptId&&(D(e.scriptId)?R=e.scriptId:q(`Unknown design "${e.scriptId}" — showing the default`),e.code&&q(`This link names a preset — ignoring its embedded code`))}function jt(){let e=oe();At(e),Ot(e.rawParams),L===`preset`&&Q.setSource((D(R)??E[0]).source),$(),Dt(),we.addEventListener(`click`,()=>{G+=1,I.request({type:`stl`,seq:G})}),F.addEventListener(`click`,()=>I.stop()),N.addEventListener(`click`,()=>{navigator.clipboard.writeText(window.location.href).then(()=>q(`Link copied`),()=>q(`Could not copy — use the address bar`))}),Me.addEventListener(`click`,nt),Ne.addEventListener(`click`,rt),Fe.addEventListener(`click`,()=>Q.close()),window.addEventListener(`popstate`,()=>window.location.reload()),Y()}jt();