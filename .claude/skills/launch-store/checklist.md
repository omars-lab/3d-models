# Pre-launch checklist — everything the store needs before it opens

One list for the coaster store, gathered from every design that feeds it. A line is ticked only
when the thing is done or decided, and each line says who does it and where the work is
tracked. `scripts/launch_check.py` checks the form and the calls' ticks; it cannot check that a
"done" line is true, so tick a line only with the PR or the date that did it.

Line form: `- [ ] What. *Who:* <owner>. *Tracked:* [where](link).` The owners are Omar,
3d-models, bikar, coffee-house-storefront (the store's own repo) and hub (3d-model-hub, which
reads the orders).

## The calls the store waits on

A call line's tick must match its call on the open-calls page: ticked when the page shows a
**Decided** line under it, open when not. Only Omar decides a call.

- [ ] Call 12: where the orders, the stock and the three pages live. *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#12-where-the-orders-the-stock-and-the-three-pages-live).
- [ ] Call 13: how the price is set. *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#^a35dir).
- [x] Call 14: orders never in this repo, an iCloud folder instead (D-101). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#14-orders-as-files-in-git).
- [x] Call 15: prices tried on simulated buyers and a charted page (D-104). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#^rzw30d).
- [ ] Call 16: a price below break-even. *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#16-a-price-below-break-even).
- [x] Call 17: Basic, settled by one test order (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#17-shopify-basic-or-grow).
- [x] Call 18: a custom order prints one plate per color (D-103). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#18-how-a-custom-order-gets-its-yes-to-print).
- [x] Call 19: the price follows finish, set size and how many colors (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#19-which-options-carry-the-price).
- [x] Call 20: Etsy later, after the store sells (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#20-etsy-now-or-later).
- [x] Call 21: a lead-time range per order, custom colorings final sale except damage (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#21-lead-time-and-returns).
- [x] Call 22: the Lab in the product page adds to the cart, the hub checks every order (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#22-how-a-design-gets-into-the-cart).
- [x] Call 23: a rights record per design, nothing listed without one (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#23-which-designs-may-be-sold).
- [x] Call 24: drawings now, a photo of each design before opening, and this checklist (D-102). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#24-which-pictures-the-store-opens-with).
- [x] Call 25: our own printed swatch card, Bambu filament first (D-105). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#25-seeing-real-colors-before-buying-spools).
- [x] Call 26: the first themes are the bottom row (D-106). *Who:* Omar. *Tracked:* [open calls](../../../docs/working-model/feedback-requests/2026-10-05-open-calls.md#^ha5dwm).

## The store's setup (D-102)

- [x] The store exists on the Basic plan, closed to buyers (2026-10-05). *Who:* Omar. *Tracked:* [storefront phase S0](../../../docs/design/storefront/shopify-storefront-design.md#15-phases).
- [ ] The custom app installed from inside the store's own organisation, and one test order read, its shipping address included: a hidden address moves the plan to Grow. *Who:* coffee-house-storefront. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).
- [ ] A read-only client-credentials token minted on the live store. *Who:* coffee-house-storefront. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).
- [ ] The Shop Pay Installments fee read in the admin. *Who:* coffee-house-storefront. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).
- [ ] The gBV product with its variants (finish × set size × colors, up to 27), prices left empty, and the theme picker on its page. *Who:* coffee-house-storefront. *Tracked:* [storefront phase S1](../../../docs/design/storefront/shopify-storefront-design.md#15-phases).
- [ ] An uploaded drawing, the timelapse GIF and one 3D file tried on a closed product, to see how the page shows them. *Who:* coffee-house-storefront. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).
- [ ] The Lab's public build, coasters only, on its own host, with the studio still behind its login. *Who:* bikar. *Tracked:* [storefront phase S2](../../../docs/design/storefront/shopify-storefront-design.md#15-phases).
- [ ] The Lab inside the product page hands a design to Shopify's cart with the one agreed attribute list. *Who:* coffee-house-storefront. *Tracked:* [the line attributes](../../../docs/design/storefront/shopify-storefront-design.md#123-the-line-attributes).
- [ ] How long one line attribute may be, and whether the Lab in its frame fits a phone screen, both tried on the closed store. *Who:* coffee-house-storefront. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).
- [ ] Intake: the hub reads each paid order, checks its coloring, holds a line that fails, and writes the order file; storefront fixtures S1 to S8 pass. *Who:* hub. *Tracked:* [the store's checks](../../../docs/design/storefront/shopify-storefront-design.md#14-checks).
- [ ] Write-back: shipping with tracking, releasing a hold, cancelling; and whether Shopify's own shipping labels are on Basic. *Who:* hub. *Tracked:* [storefront phase S4](../../../docs/design/storefront/shopify-storefront-design.md#15-phases).

## Designs and pictures

- [ ] A rights record in bikar's design files: the design's source, the source's terms, who cleared it and when, with the Lab's store mode showing only cleared designs. *Who:* bikar. *Tracked:* [call 9](../../../docs/design/storefront/shopify-storefront-design.md#call-9-which-designs-may-be-sold).
- [ ] gBV's record written and cleared: the first product waits on it. *Who:* Omar. *Tracked:* [D-102](../../../docs/working-model/decisions-log.md#d-102--the-stores-first-setup-basic-plan-priced-by-finish-set-and-colors-etsy-later).
- [x] Drawn listing pictures for a theme, each labeled as a drawing: `themes.py listing` (3d-models #562). *Who:* 3d-models. *Tracked:* [product pictures](../../../docs/design/storefront/shopify-storefront-design.md#118-product-pictures-what-a-listing-shows-and-how-each-picture-is-made).
- [ ] A photo of a real print of each listed design before opening, starting with gBV in one theme, and the photo setup (light, a background, a mug). *Who:* Omar. *Tracked:* [D-102](../../../docs/working-model/decisions-log.md#d-102--the-stores-first-setup-basic-plan-priced-by-finish-set-and-colors-etsy-later).

## Prints and supplies

- [x] A custom order prints one plate per color, so each new coloring gets its own yes: the planner already plans this way, nothing to build (D-103; `bambu order plan`, 3d-models #561). *Who:* 3d-models. *Tracked:* [D-103](../../../docs/working-model/decisions-log.md#d-103--a-custom-order-prints-one-plate-per-color-so-each-new-coloring-gets-its-own-yes).
- [ ] The swatch card: a plate recipe and page, one chip per color we own or plan to buy (D-105). *Who:* 3d-models. *Tracked:* [coaster-pipeline backlog](../../../docs/tasks/coaster-pipeline/backlog.md#owner-gated).
- [ ] The swatch card printed. *Who:* Omar. *Tracked:* [D-105](../../../docs/working-model/decisions-log.md#d-105--swatches-are-our-own-printed-card-from-bambu-filament-first).
- [ ] The four first themes (Midnight blue, Night sky, Terracotta souk, Iznik tile): a plate recipe per color for each, and the list of colors to buy, priced (D-106). *Who:* 3d-models. *Tracked:* [coaster-pipeline backlog](../../../docs/tasks/coaster-pipeline/backlog.md#owner-gated).
- [ ] The colors for three of those themes bought, and the themes printed. *Who:* Omar. *Tracked:* [D-106](../../../docs/working-model/decisions-log.md#d-106--the-first-themes-to-print-are-the-bottom-row-midnight-blue-night-sky-terracotta-souk-iznik-tile).
- [ ] The iCloud folder for order files chosen and named, so the planner reads orders from it (D-101). *Who:* Omar. *Tracked:* [D-101](../../../docs/working-model/decisions-log.md#d-101--orders-never-go-in-this-repo-they-live-in-an-icloud-folder).
- [ ] What packaging and shipping cost per order: a packed set weighed and priced. *Who:* Omar. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).
- [ ] How long pressing the pieces in takes: one assembly timed, for the pricer's labor. *Who:* Omar. *Tracked:* [tests on the closed store](../../../docs/design/storefront/shopify-storefront-design.md#163-questions-a-test-settles).

## Pricing

- [x] The pricer: cost, break-even and a suggested price by order size (3d-models #570). *Who:* 3d-models. *Tracked:* [the build phases](../../../docs/design/coaster/order-driven-lab-design.md#11-the-build-in-order-of-value-for-the-work).
- [x] Simulated buyers and the price page (3d-models #572). *Who:* 3d-models. *Tracked:* [pricing ideas](../../../docs/design/coaster/order-driven-lab-design.md#97-pricing-ideas-the-ways-to-set-a-price-side-by-side).
- [ ] The pricer's settings filled and every variant's price set. *Who:* Omar. *Tracked:* [values only Omar sets](../../../docs/design/storefront/shopify-storefront-design.md#164-values-only-omar-sets).
- [ ] The price check passes: every variant's price on the store equals the one set in the hub, and the hub flags each below break-even. *Who:* hub. *Tracked:* [the store's checks](../../../docs/design/storefront/shopify-storefront-design.md#14-checks).

## Only Omar, last

- [ ] The lead-time range per order, long enough for the wait on his review of each new coloring (D-103), and the returns wording: custom colorings are final sale except damage. *Who:* Omar. *Tracked:* [values only Omar sets](../../../docs/design/storefront/shopify-storefront-design.md#164-values-only-omar-sets).
- [ ] The public Lab's domain, and the Cloudflare settings behind it. *Who:* Omar. *Tracked:* [values only Omar sets](../../../docs/design/storefront/shopify-storefront-design.md#164-values-only-omar-sets).
- [ ] The store template published, by hand. *Who:* Omar. *Tracked:* [values only Omar sets](../../../docs/design/storefront/shopify-storefront-design.md#164-values-only-omar-sets).
- [ ] The store opened to buyers. *Who:* Omar. *Tracked:* [storefront phase S5](../../../docs/design/storefront/shopify-storefront-design.md#15-phases).

## Not before opening

Decided to come after the store sells, so not on this list: Etsy (call 20), a set holder, and
quotes from the hub's pages.
