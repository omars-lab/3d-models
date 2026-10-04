---
date: 2026-10-04
produced-by: researcher B (Claude Opus 5.5), one of two independent researchers on the same question. Method — the web-search budget ran out early, so pages were read directly; curl with a browser user agent against the Bambu US store (prices read from each product page's embedded JSON-LD offers) and the Bambu forum (its Discourse JSON search and topic API); WebFetch for EIA, Prusa, Shopify and Omni; a Chrome tab for Etsy (its policy pages and nine listing searches, extracted with in-page JavaScript, 13 listings opened to check material). Researcher A's files were not read.
feeds:
  - order-driven-lab-design
---

# Coaster pricing inputs (research B)

**The question.** Omar prints Islamic geometric coasters (about 112.5 mm: a frame plus
press-in loose pieces) on a Bambu X2D with an AMS. He wants each order to report its cost
and a suggested price. The formula is being designed separately; this file collects the
inputs, with their sources: filament price, machine-hour cost, how small print sellers
build a price, selling fees, and what similar coasters sell for.

**His measured numbers, as given to me (not re-measured here).** A full coaster plate was
sliced at 86 min / ~27 g PLA Basic and printed in ~98 min. A small plate was sliced at
12 min / 3.5 g and printed in 13–14 min. Each AMS color swap costs about 1.6 min plus
prime-tower waste, so he now prints one color per plate.

**How to read the tables.** "Fetched" means I opened the page itself and read the value
there. "Snippet" means I saw the value only in a search-result blurb and did not open the
page. All fetches are dated 2026-10-04 unless a row says otherwise. Prices are USD.

---

## Q1 — Bambu filament, US retail

All rows come from the US store product pages. The listed price is the offer price of every
variant in the page's JSON-LD; "N variants" counts the colors listed at that price.

| Line | Refill (no spool) | With spool | Bulk floor shown on page | Source | Fetched / snippet |
|---|---|---|---|---|---|
| PLA Basic | $15.99 (30 variants) | $18.99 (13 variants) | "$11.19 USD /roll (Lowest price for 10+ rolls) MSRP: $15.99" | https://us.store.bambulab.com/products/pla-basic-filament | fetched |
| PLA Matte | $15.99 (25 variants, 1 out of stock) | $18.99 (6 variants) | same $11.19 for 10+ against $15.99 | https://us.store.bambulab.com/products/pla-matte | fetched |
| PLA Silk+ | $15.99 (4 variants) | $18.99 (13 variants) | "$13.29 … for 10+ rolls", MSRP $18.99 | https://us.store.bambulab.com/products/pla-silk-upgrade | fetched |
| PLA Silk (plain) | not found | not found | — | https://us.store.bambulab.com/products/pla-silk returned 404, and the PLA collection page lists no plain Silk. It looks like Silk+ replaced it, but no page says so. | fetched (the 404) |
| PLA Sparkle | none offered | $24.99 (6 variants) | none shown; not on the bulk-sale list | https://us.store.bambulab.com/products/pla-sparkle | fetched |
| PETG Basic | $13.99 (13 variants) | $16.99 (13 variants) | "$9.79 … for 10+ rolls" | https://us.store.bambulab.com/products/petg-basic | fetched |
| PLA Silk Multi-Color (extra) | — | $24.99 | not on the bulk list | https://us.store.bambulab.com/products/pla-silk-multi-color | fetched |
| PETG HF (extra) | $15.99 | $18.99 | on the bulk list | https://us.store.bambulab.com/products/petg-hf | fetched |
| PLA Basic Gradient, Marble, Galaxy (extras) | — | $24.99 each (all 8 Gradient variants out of stock) | — | the three product pages under us.store.bambulab.com/products/ | fetched |

**Bulk and bundle discounts.**

| Finding | Value | Source | Fetched / snippet | Date |
|---|---|---|---|---|
| Bulk tiers, mix and match | 2 items 5% off, 4 items 10%, 6 items 15%, 10 items 30%; "Buy more, save more – up to 30% OFF"; "PLA from $11.19, PETG from $9.79" | https://us.store.bambulab.com/pages/promotions/filament-bulk-sale | fetched | 2026-10-04 |
| Lines the bulk sale covers (11 named on that page) | PLA Basic, PLA Matte, PLA Pure, PLA Silk+, PLA Translucent, PLA Tough+, PETG Basic, PETG Matte, PETG HF, PETG Translucent, ABS. Sparkle and Silk Multi-Color are not on it. | same page | fetched | 2026-10-04 |
| Price cut announcement | Refills: PETG Basic $13.99, PLA Basic $15.99, PLA Pure $16.99; "new bulk discount on 2 rolls"; "as low as $10.91/roll when you buy 10 rolls"; US free shipping from $59, down from $89 | https://forum.bambulab.com/t/259832 (post #1, the BambuLab account) | fetched | 2026-09-16 |

**A conflict to carry.** The announcement says $10.91 a roll at 10 rolls, but the store pages
fetched today show $11.19 as the 10+ floor for PLA Basic and Matte. ($15.99 × 0.70 = $11.19,
so the store figure matches the 30% tier.) The announcement says "details vary by region and
filament", and I did not find which line the $10.91 is for.

**Hedge.** Both the bulk page and the announcement call this a sale or a new price. Neither
says how long the 30% tier lasts.

---

## Q2 — X2D power, machine-hour rate, purchase price

| Finding | Value | Source | Fetched / snippet | Date |
|---|---|---|---|---|
| X2D price | X2D $649; X2D AMS Combo $899; "Print More Bundle (2 AMS 2 Pro included)" $1,149; "Combo Print with Care Bundle" $949; all in stock; page also says "30-day price protection, 2-year warranty" | https://us.store.bambulab.com/products/x2d (JSON-LD offers) | fetched | 2026-10-04 |
| X2D max power | 1100 W @110 V | same page, spec table (picked out by its 256×256×260 mm volume and 16.25 kg net weight; the page also embeds an H2D table at 1320 W — a different machine) | fetched | 2026-10-04 |
| X2D steady-state power | "PLA (25 °C): 250 W@110 V", "PC (25 °C): 550 W@110 V" | same spec table | fetched | 2026-10-04 |
| Measured X2D draw (owner) | PETG at "~170w vs ~70w" for an X1C; later got the X2D combo to "about 15-20w extra"; AMS 2 Pro "about 7 watts extra" | https://forum.bambulab.com/t/251064 posts #1 and #9 | fetched | 2026-04-24 |
| Measured P1S energy (owner) | ~100 h/month of printing used 8.4 kWh in April ($2.59 at $0.31/kWh), 9.6 kWh in March, dryer included | https://forum.bambulab.com/t/252520 post #5 | fetched | 2026-05-12 |
| Four-P1S average (owner) | May total 48.75 kWh, 12.2 kWh per printer (hours not given in the blurb) | https://forum.bambulab.com/t/172881 post #5 | snippet | 2025-06-16 |
| P1S warm-up | ~850 W for the first 30–60 s, then roughly 30–70 W | https://forum.bambulab.com/t/173002 | snippet | — |
| US electricity price | US residential average 18.31 ¢/kWh (July 2026); NY 29.90; CA 33.61; TX 15.88 | EIA Electric Power Monthly, table 5.6.A, https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a | fetched | 2026-10-04 |
| Depreciation method | Printer price ÷ payback hours × print hours. Prusa assumes 6 months of use = 4,392 h, giving $0.21/h for the MK3S and $0.10/h for the MINI | https://blog.prusa3d.com/how-to-calculate-printing-costs_38650/ (article date not captured) | fetched | 2026-10-04 |
| Electricity, Prusa's view | "practically negligible", under $0.023 a print, for printers drawing "100-150 W" at $0.07–0.09/kWh | same | fetched | 2026-10-04 |
| Failure and maintenance margin | "30% of the material price" as a starting estimate, with the hedge that "many people … see it differently" | same | fetched | 2026-10-04 |
| Lifetime-based rate (forum) | "assume a life time of 2000h, an H2C at ±2000$ and 300$ in replacement parts/consumables, then the cost per hour should be more like 1.2$ / h"; "an A1 … closer to 0.3$ / h" | https://forum.bambulab.com/t/256018 post #4 | fetched | 2026-07-02 |
| "Printer costs basically nothing" (forum) | "If you had to replace an A1 every year it would still be only a few cents an hour"; labor first, filament second | https://forum.bambulab.com/t/256018 post #3 | fetched | 2026-07-02 |
| Machine-time rate example (forum) | 8 h at "about 3€/hour" machine time = 24 € (illustration, "a theoretical model") | https://forum.bambulab.com/t/246829 post #25 | fetched | 2026-04-06 |
| Replacement hotend for the X2D | Standard Flow, 0.4 mm hardened steel: $17.99; High Flow, 0.4 mm hardened steel: $49.99 | https://us.store.bambulab.com/products/bambu-hotend-h2-p2s (product "Bambu Hotend - H2/P2S/X2D") | fetched | 2026-10-04 |
| Textured PEI plate for the X2D | $34.99 | https://us.store.bambulab.com/products/bambu-textured-pei-plate (variant "X2D") | fetched | 2026-10-04 |
| Hotend wear on PLA | "never had to replace a hardened nozzle due to wear" (one owner) | https://forum.bambulab.com/t/26077 | snippet | — |
| PEI plate life | No hours or print count found. One owner wrote that plates "keep trucking until they have literal holes in them"; another said it depends on material and cleaning | https://forum.bambulab.com/t/184785 posts #2 and #4 | fetched | 2025-07-23 |
| Plate life, one data point | ~300 h of PLA before specks pulled off the plate's engineering side (an older plate type) | https://forum.bambulab.com/t/8257 post #1 | snippet | 2023-03-30 |

**Not found:** a lifetime in hours for the X2D, its hotend or its plate from Bambu itself.
The hotend and plate prices above are real, but no source gave how many hours either lasts
printing PLA.

---

## Q3 — How small FDM sellers build a price

| Finding | Value | Source | Fetched / snippet | Date |
|---|---|---|---|---|
| Cost-plus and target-margin formulas | "Cost + Markup = Selling price"; "Target price = cost / (1 − margin)", e.g. $14.28 at 20% margin → $17.85 | Shopify blog, "How to Price a Product in 2026" (Lizzie Davey), https://www.shopify.com/blog/how-to-price-your-product | fetched | 2026-09-03 |
| Average gross margins (NYU data, quoted by Shopify) | general retail 33.18%; furniture/home furnishings 30.28%; apparel 56.88% | same | fetched | 2026-09-03 |
| Etsy's own method | Top-down: materials + overhead ÷ items + labor at the wage you'd want; bottom-up: research the market. Gross margin = (revenue − COGS) / revenue × 100. No markup number given | Etsy Seller Handbook, "Pricing Basics", https://www.etsy.com/seller-handbook/article/1106022743419 | fetched | 2026-10-04 |
| Calculator form | final price = (material + labor) × (1 + markup); no default markup | Omni 3D printing cost calculator, https://www.omnicalculator.com/other/3d-printing | fetched | 2026-10-04 |
| Full cost-plus, forum | Price = (production cost + licence per unit) × (1 + markup); for your own design add development ÷ expected units. Production = material and waste, electricity, depreciation and maintenance, hands-on labor, failure allowance, overheads. "Unattended machine time is not the same as paid labour." | https://forum.bambulab.com/t/256018 post #15 | fetched | 2026-09-15 |
| Failure allowance, forum | "If 5% of comparable prints fail, the successful jobs need to recover a little over 5% extra"; another: "a print that fails 1 in 10 times needs the other 9 to cover it" | same thread, posts #9 and #12 | fetched | 2026-08-11, 2026-09-12 |
| Worked example, forum | material 2.40 € + machine 24 € + labor 30 min at 25 €/h = 12.50 € + design share 6.67 € = 45.57 €; plus 20–30% for failures, waste and risk → "roughly 55–60€" | https://forum.bambulab.com/t/246829 post #25 | fetched | 2026-04-06 |
| Second worked example, same author | production 6 € + development 3 € + platform and packaging 2 € + 10% risk 1 € = 12 € net; +19% VAT ≈ 14.30 €; + "30–50%" profit → "≈ 18–22€". Returns and defects: "+5–10% risk surcharge" | same thread, post #28 | fetched | 2026-04-10 |
| Rules of thumb, forum (anecdotes) | "material cost x 2" ("extremely simplified version for friends") | https://forum.bambulab.com/t/221025 post #18 | fetched | 2026-05-04 |
|  | "Minutes x $0.28" | https://forum.bambulab.com/t/256018 post #2 | fetched | 2026-07-02 |
|  | material ×2 for waste and power, ×2 again for labor and machine time, then adjust | https://forum.bambulab.com/t/197260 post #2 | fetched | 2025-09-23 |
|  | "$2" an hour of printer time plus filament | same thread, post #7 | fetched | 2025-09-23 |
| Value over cost, forum | a cost calculation "gives you the floor; the market determines the selling price" (post #9); "a decorative Pokemon model might only be worth $15 … even if it took 10 hours" (post #5) | https://forum.bambulab.com/t/256018 | fetched | 2026-07/08 |
| Labor, Prusa | about 5 min of preparation and slicing a print | Prusa blog (as in Q2) | fetched | 2026-10-04 |

**Hedge.** Apart from Shopify's general retail margins, every markup figure here is one
person's habit on a forum. None of the sources surveyed gives a measured markup for
3D-printed home decor. That covers Shopify, Etsy, Omni, Prusa and five forum threads.

---

## Q4 — Selling fees and marketplace rules

| Finding | Value | Source | Fetched / snippet | Date |
|---|---|---|---|---|
| Etsy listing fee | $0.20 per listing, expires after 4 months, auto-renews; a multi-quantity listing renews for $0.20 after each sale | Etsy Fees & Payments Policy, https://www.etsy.com/legal/fees/ ("Last updated on Oct 5, 2026" as shown on the page) | fetched | 2026-10-04 |
| Etsy transaction fee | 6.5% of item price plus shipping and gift wrap; not charged on US sales tax | same | fetched | 2026-10-04 |
| Etsy Offsite Ads | 15% for shops under $10k sales in the prior 365 days (these can opt out); 12% at or over $10k (mandatory, permanently); capped at $100 per order; applies to an order within 30 days of the ad click | same | fetched | 2026-10-04 |
| Etsy set-up fee | a one-time fee "may" apply; the amount is not stated on the policy page | same | fetched | 2026-10-04 |
| Etsy optional extras | Etsy Plus $10/mo; Pattern $15/mo; currency conversion 2.5% | same | fetched | 2026-10-04 |
| Etsy Payments processing (US) | "3% + 0.25 USD", charged on the order total including tax and shipping | Etsy Payments Policy, https://www.etsy.com/legal/etsy-payments/ | fetched | 2026-10-04 |
| Etsy rule on 3D-printed goods | "Made by a seller" includes items made "using computerized tools such as a laser printer, 3D printer, CNC or Cricut machine" and they "must be produced based on a seller's original design"; example given: "Bust made by a seller using automated tools (3D printer)". "Designed by a seller" covers original designs a third party produces | Etsy Creativity Standards, https://www.etsy.com/legal/creativity/ (last updated Jun 10, 2025) | fetched | 2026-10-04 |
| Shopify Basic | $39/mo billed monthly, $29/mo billed yearly | https://www.shopify.com/pricing | fetched | 2026-10-04 |
| Shopify Payments, Basic | online 2.9% + 30¢; in person 2.6% + 10¢; 2% extra when using a third-party gateway | same | fetched | 2026-10-04 |
| Licensing, forum | "Most models can't be printed commercially without a license from the designer" | https://forum.bambulab.com/t/256018 post #3 | fetched | 2026-07-02 |

**What the Etsy rule means here (my reading, not Etsy's words).** Omar's patterns are drawn
from his own constructions, so his coasters fit "made by a seller". A coaster printed
from someone else's downloaded model would not.

**Not checked:** Amazon Handmade, eBay, and Etsy's set-up fee amount.

---

## Q5 — Market prices for similar coasters (Etsy, 2026-10-04)

**Method.** I ran nine Etsy searches in a Chrome tab signed in from the US, with prices in
USD. Each search read the first results page after scrolling, 56–64 listing cards per
search. For each card I took the price shown and, when the card was on sale, its crossed-out
price. A title regex sorted the cards: material (3D-printed, resin, laser/wood/acrylic),
theme (Islamic/Arabic/Moroccan, geometric) and set size ("set of N", "N-piece", "N pack").
I removed the same listing appearing in several searches, which left 298 unique listings;
12 of them were digital files (SVG, STL, templates) and were excluded, leaving 286.

**Hedges on these numbers.**
- This is one page per search, not the market. Etsy ranks by relevance and personalizes
  results, and ads were not separated out.
- I believe a card shows the price of the default variation, which may be the cheapest. I
  did not confirm that against an Etsy page.
- A per-coaster price is computed only when the title states the set size.
- "3D-printed" means the title says 3D printed. Many results for "3d printed coaster" do
  not say so in the title and are not counted in that group.
- The theme sort is a regex on titles, and I checked it by hand on only 13 listings (the
  table further down).
- Listings with no stated size are left out of the size columns, so I could not separate
  single coasters as a clean group.

**Per search (first page, before removing repeats).** Each cell reads count, then
min / 25th percentile / median / 75th percentile / max, in USD.

| Search | Listing price | Cards on sale | Per coaster (size in title) |
|---|---|---|---|
| 3d printed coaster | 63: 4.24 / 18.58 / 24.93 / 29.99 / 52.95 | 13 | 20: 2.50 / 3.12 / 5.18 / 6.71 / 11.25 |
| 3d printed coasters set of 4 | 62: 5.17 / 17.25 / 25.00 / 32.00 / 52.95 | 14 | 36: 1.87 / 4.19 / 6.25 / 8.00 / 12.50 |
| 3d printed coasters set of 6 | 62: 5.17 / 17.05 / 25.00 / 31.80 / 55.00 | 16 | 31: 1.87 / 3.25 / 5.83 / 7.50 / 11.25 |
| geometric 3d printed coaster | 60: 3.99 / 18.00 / 25.00 / 30.00 / 45.00 | 16 | 27: 2.50 / 3.73 / 6.00 / 7.40 / 10.00 |
| islamic geometric coaster | 56: 1.75 / 16.43 / 25.00 / 32.50 / 190.00 | 15 | 20: 1.90 / 4.89 / 6.25 / 7.81 / 11.25 |
| islamic coaster 3d printed | 57: 2.55 / 20.00 / 27.99 / 35.00 / 51.00 | 13 | 26: 0.99 / 5.04 / 6.31 / 7.50 / 12.75 |
| mosaic coaster 3d printed | 62: 5.50 / 18.00 / 25.00 / 31.75 / 54.40 | 20 | 24: 1.44 / 4.50 / 6.63 / 7.63 / 13.60 |
| resin geometric coaster (comparable, not 3D-printed) | 62: 1.44 / 18.49 / 25.00 / 31.42 / 73.00 | 18 | 25: 2.17 / 6.00 / 6.25 / 7.50 / 13.60 |
| laser cut geometric coaster (comparable, not 3D-printed) | 64: 1.44 / 7.43 / 25.00 / 30.78 / 99.95 | 18 | 23: 0.11 / 5.08 / 6.50 / 7.50 / 13.50 |

**By group (286 physical listings, repeats removed, sorted by title).**

| Group | All listings | Set of 4 | Set of 6 | Per coaster |
|---|---|---|---|---|
| Title says 3D-printed | 74: 7.00 / 18.00 / 22.99 / 31.00 / 52.95 | 23: 7.00 / 15.49 / 20.00 / 29.63 / 45.00 | 12: 16.99 / 18.00 / 25.50 / 35.00 / 50.00 | 39: 1.75 / 3.31 / 5.00 / 6.81 / 11.25 |
| 3D-printed and geometric | 23: 7.00 / 18.49 / 24.93 / 31.00 / 40.64 | 9: 7.00 / 11.69 / 22.99 / 30.00 / 39.00 | 3: 16.99 / 17.49 / 17.99 / 24.49 / 31.00 | 13: 1.75 / 2.92 / 5.17 / 7.50 / 9.75 |
| Islamic / Arabic / Moroccan theme, any material (noisy: includes ceramic tile, glass, a charcuterie board) | 50: 2.55 / 16.93 / 24.99 / 34.74 / 58.69 | 7: 7.00 / 18.38 / 25.00 / 25.24 / 51.00 | 7: 5.95 / 20.27 / 31.00 / 40.50 / 45.00 | 19: 0.99 / 4.08 / 6.00 / 7.00 / 12.75 |
| Resin (comparable) | 26: 1.74 / 15.25 / 25.00 / 39.74 / 73.00 | 6: 25.00 / 26.75 / 35.50 / 43.50 / 54.40 | 1: 39.99 | 7: 6.25 / 6.46 / 8.00 / 10.50 / 13.60 |
| Laser-cut / wood / acrylic (comparable) | 56: 1.44 / 15.99 / 27.98 / 35.25 / 99.95 | 17: 7.50 / 19.95 / 27.96 / 35.00 / 54.00 | 6: 12.99 / 16.66 / 28.00 / 38.99 / 45.91 | 27: 0.11 / 3.66 / 6.25 / 7.50 / 13.50 |

The $0.11 per coaster in the laser group is almost certainly a parse artifact: a title
whose count is not the number of coasters sold. I did not open that listing. Read the
laser and resin minimums as noise.

**Closest comparables, opened and checked (13 listings).** This is every listing whose
title says Islamic and geometric, plus every title-3D-printed listing with an Islamic or
Arabic theme. For each one I read the description for material, size and set count.
Listing URLs follow the pattern https://www.etsy.com/listing/ID.

| Listing ID | Card price | Set | Material (from description) | Size | Theme | Per coaster |
|---|---|---|---|---|---|---|
| 4413086895 | $7.00 | 4 | PLA + cork | 9.2 cm | Moroccan geometric | $1.75 |
| 4527598674 | $16.14 (on sale from $18.99) | 6 | PLA, 3D-printed | 3.74 in | Arabic coffee (not geometric) | $2.69 |
| 4440970337 | $22.85 | options: single / 4 / 6 | PLA, 3D-printed | 100 mm | Islamic Moroccan geometric | unknown (the card is probably the single, unconfirmed) |
| 4334311750 | $25.00 | 4 + holder | PETG, 3D-printed | 4.75 in | Kufic calligraphy | $6.25 |
| 4411122673 | $25.00 | 4 + holder | plastic (PLA named) | 4.2 in | Islamic geometric | $6.25 |
| 1887433579 | $35.00 | 5 | PLA, 3D-printed | 4.5 in | Islamic geometry + calligraphy | $7.00 |
| 1873629785 | $35.00 | 5 | PLA, 3D-printed | — | Islamic calligraphy | $7.00 |
| 1879888010 | $45.00 | 6 | PLA, 3D-printed | 4.25 in | Islamic geometric + calligraphy | $7.50 |
| 4537645821 | $20.76 | 4 | marble (comparable) | — | Islamic geometric | $5.19 |
| 4449325425 | $24.99 | set (size not stated) | ceramic tile (comparable) | — | Moroccan mosaic | — |
| 4369156051 | $25.00 | — | ceramic (comparable) | — | Islamic geometric / Palestine | — |
| 4302228688 | $3.39 (on sale from $3.99) | set (size not stated) | ceramic + cork (comparable) | 10 cm | Persian tile | — (the card is likely one variation) |
| 1782642749 | $16.00 | 4 | wood, laser-engraved (comparable) | — | Islamic geometric | $4.00 |

The eight 3D-printed rows give per-coaster prices for 7 of them: 1.75, 2.69, 6.25, 6.25,
7.00, 7.00, 7.50, with a median of **$6.25**. Set prices for the sets of 4 to 6 run from
$25 to $45. The two lowest are a set of 4 at $7 and a sale set of 6 at $16.14. Both are
smaller coasters than Omar's (9.2 cm and 3.74 in). None of the eight looked, from its
description, like a frame with press-in loose pieces. That is a difference between his
product and these listings, not evidence of a premium.

---

## Design notes — recommended inputs

These are my suggestions for the separate pricing formula. Each line gives the number,
where it comes from and how sure I am. Worked figures use Omar's full-coaster plate: 27 g
and 98 min as printed.

| Input | Recommended value | Basis | Confidence |
|---|---|---|---|
| PLA Basic / Matte cost per gram | $0.016/g (refill, $15.99/kg); $0.019/g with spool. Use $0.0112/g only when buying 10+ rolls at the 30% tier | store pages, Q1 | High for today's price; medium for how long it lasts (cut on 2026-09-16, bulk is a "sale") |
| Silk+ cost per gram | $0.016/g refill, $0.019/g spool; 10+ floor $0.0133/g | Q1 | High |
| Sparkle / Silk Multi / Marble / Galaxy | $0.025/g (spool only, no bulk tier) | Q1 | High |
| PETG Basic | $0.014/g refill | Q1 | High |
| Material for one full coaster | 27 g × $0.016 = **$0.43** (bulk: $0.30) | his 27 g × Q1 | High |
| Power while printing PLA | 250 W (X2D spec, steady state, 25 °C room); owners measured 70–170 W on similar machines, so 250 W is the high end | spec + forum | Medium: the spec is fetched, but no one has measured an X2D on PLA |
| Electricity price | $0.1831/kWh US average (EIA, July 2026). Use his own utility rate if known: states run from 15.88 to 33.61 ¢ in the rows fetched | EIA | High for the average; his own rate is unknown |
| Power for one full coaster | 250 W × 1.63 h = 0.41 kWh × $0.1831 = **$0.075** (at 170 W: $0.05) | derived | Medium. Small next to the other costs either way, as Prusa says |
| Printer cost | X2D AMS Combo $899 (store, today) | Q2 | High that this is today's price; it may be a promotion |
| Payback hours | Make it a setting. 2,000 h (forum estimate of lifetime) gives **$0.45/h**; Prusa's 4,392 h (6 months nonstop) gives $0.20/h | Q2 | Low. Both are assumptions; nobody measured an X2D lifetime |
| Depreciation for one full coaster | 1.63 h × $0.45 = **$0.73** (Prusa's hours: $0.33) | derived | Low (follows the payback hours) |
| Wear parts | Hotend $17.99, Textured PEI plate $34.99. No lifetime found. Either fold wear into the failure margin (Prusa's way), or set a lifetime as a stated assumption | Q2 | Prices high, lifetimes not found |
| Failure and maintenance allowance | 30% of material cost (Prusa's starting estimate) = $0.13 a coaster. Or divide cost by (1 − failure rate) once a measured rate exists; forum suggestions run from 5% to 1 in 10 | Q2, Q3 | Low to medium. His own print log should replace this |
| Labor | Price hands-on minutes only (slicing, plate removal, pressing pieces in, packing) at a wage he picks. Prusa counts 5 min to prepare a print; the forum example uses 30 min at 25 €/h | Q3 | Medium for the method; the minutes are his to measure |
| Etsy fees | $0.20 listing + 6.5% of (item + shipping) + 3% of (item + shipping + tax) + $0.25. On a $25 set with no shipping or tax: **$2.83 (11.3%)**. An Offsite Ads order adds 15% ($3.75), making **$6.58 (26.3%)** | Q4 | High (policy pages fetched today) |
| Shopify fees | 2.9% + $0.30 a sale (on $25: $1.03), plus $39/mo or $29/mo yearly | Q4 | High |
| Markup / margin | No sourced number for this product type. A formula would add a markup ("cost × (1 + markup)") or aim for a gross margin ("cost ÷ (1 − margin)"). The only sourced benchmarks are general retail margins of 30–57% (NYU via Shopify). Forum habits are material × 2 to × 4, or 30–50% on full cost | Q3 | Low as a number; high that the formula should take it as a setting |
| Market band, 3D-printed sets | Set of 4 median **$20** (middle half $15.49–29.63, 23 listings); set of 6 median **$25.50** (middle half $18–35, 12 listings); per coaster median **$5.00** (middle half $3.31–6.81, 39 listings) | Q5 | Medium: one results page per search, titles sorted by regex |
| Market band, Islamic 3D-printed | per coaster median **$6.25** (7 checked listings); sets of 4–6 sold at $25–45 | Q5 | Medium-low: small sample, and smaller coasters than his |

**Rough cost floor for one full coaster plate, from the rows above (not a price).** Material
$0.43, power $0.08, depreciation at 2,000 h $0.73, and 30% failure on material $0.13 come
to about **$1.37** before labor, packing and fees. At Prusa's 4,392 h it is about $0.97.
Depreciation is the largest of these, and it is also the least grounded. Labor will
probably outweigh all four, but its minutes are not measured. The market band ($5–7.50 a
coaster for Islamic or geometric 3D-printed listings) sits well above this floor. So the
formula's price will be set by labor, fees and markup more than by machine cost.
