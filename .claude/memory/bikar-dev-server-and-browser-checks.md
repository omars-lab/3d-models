---
name: bikar-dev-server-and-browser-checks
description: Port collisions and browser-check rules for bikar Lab/studio dev servers — fixed ports, lsof first, bind 127.0.0.1, a real-browser check is part of shipping a page
metadata:
  type: feedback
---

- Lab preview runs on **:4613** (`make lab-dev`); the vite default :4173 collided with an unrelated user preview and Playwright's `reuseExistingServer` silently tested the wrong site. 3d-models `make site` serves on :8613 because the Lab worker cannot load over `file://`.
- `localhost` can resolve to another session's app: one session held a port on IPv4 while vite bound `[::1]`. Bind `--host 127.0.0.1` on a fresh port and run `lsof -iTCP:<port>` first.
- Playwright-in-Docker 403s on Vite's allowed-hosts; use Chrome on the host. The Chrome extension sometimes refuses to connect — measuring the served bytes (e.g. SVG with shapely) is an equivalent check when the page inserts files as `<img src>`.
- Studio: `editor.html` → `assets/editor-*.js`; `assets/main-*.js` is a 0.07 kB landing shim, so grepping it looks like a stale deploy. Grep for a string literal or CSS class, never an identifier (minification mangles names).

**Why:** a dev-server check in a real browser is part of shipping a page, not optional (two page defects were found only by looking — [[breakdown-page-instrument]]); a green run against the wrong port proves nothing.

**How to apply:** `lsof`, fixed port, real browser, then screenshot or byte-measure. Deploy-side equivalent: [[deploy-verification]].
