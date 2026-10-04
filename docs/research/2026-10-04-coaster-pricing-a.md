---
date: 2026-10-04
produced-by: Claude Opus 5.5 (researcher A of two, independent), direct page fetches with curl (Bambu store, Bambu wiki, EIA, Prusa, Shopify, Omni) and a real Chrome session (Etsy pages, which refuse plain fetches); the web-search budget ran out early, so every source below was opened directly by URL and none rests on a search snippet
feeds:
  - order-driven-lab-design (being written)
---

# Coaster pricing inputs, researcher A

What this is: the numbers a pricing formula for Omar's printed coasters needs, each with
where it came from. The formula itself is designed elsewhere. One coaster is about 112.5 mm
across, a frame plus loose pieces that press in, printed on a Bambu X2D with an AMS, one
color per plate.

The measured print facts I was given:

- a full coaster plate sliced at 86 min and about 27 g of PLA Basic, and printed in about 98 min;
- a small plate sliced at 12 min and 3.5 g, and printed in about 13 to 14 min;
- an AMS color swap costs about 1.6 min plus prime-tower waste. This only matters on a plate
  with more than one color, and Omar now prints one color per plate.

How to read the tables:

- **Fetched** means I opened the page and read the value on it. No value here comes from a
  search snippet.
- **Date** is the day I fetched it, 2026-10-04, unless the row says otherwise.
- Store prices change often. Each one is that day's listed price, not a lasting fact.
- Every set of listings is counted ("N listings seen"). No claim here covers all of Etsy.

## Q1. Bambu US store filament prices

Every product page carries its variants and prices in embedded structured data, and I read
them from there. All URLs are under `https://us.store.bambulab.com`. "Spool" is the 1 kg roll
on a reusable spool; "refill" is the same 1 kg with no spool. None of the variants showed a
crossed-out "was" price on 2026-10-04, so these are the regular listed prices.

| Item | Value | Source URL | Fetched or snippet | Date |
|---|---|---|---|---|
| PLA Basic, 1 kg spool | $18.99 (13 colors listed) | /products/pla-basic-filament | fetched | 2026-10-04 |
| PLA Basic, 1 kg refill | $15.99 (30 colors listed) | /products/pla-basic-filament | fetched | 2026-10-04 |
| PLA Matte, 1 kg spool | $18.99 (6 colors) | /products/pla-matte | fetched | 2026-10-04 |
| PLA Matte, 1 kg refill | $15.99 (25 colors) | /products/pla-matte | fetched | 2026-10-04 |
| PLA Silk (plain, not Silk+) | not found. The page at /products/pla-silk holds no product data, so the store does not list plain Silk as a current product | /products/pla-silk | fetched | 2026-10-04 |
| PLA Silk+, 1 kg spool | $18.99 (13 colors) | /products/pla-silk-upgrade (page title "PLA Silk+") | fetched | 2026-10-04 |
| PLA Silk+, 1 kg refill | $15.99 (only 4 colors: Gold, Silver, Titan Gray, White) | /products/pla-silk-upgrade | fetched | 2026-10-04 |
| PLA Sparkle, 1 kg spool | $24.99 (6 colors) | /products/pla-sparkle | fetched | 2026-10-04 |
| PLA Sparkle, refill | not found. No refill variant is listed | /products/pla-sparkle | fetched | 2026-10-04 |
| PETG Basic, 1 kg spool | $16.99 (13 colors) | /products/petg-basic | fetched | 2026-10-04 |
| PETG Basic, 1 kg refill | $13.99 (13 colors) | /products/petg-basic | fetched | 2026-10-04 |
| Bulk sale headline | "Buy more, save more", up to 30% off; "PLA from $11.19, PETG from $9.79" | /pages/promotions/filament-bulk-sale | fetched | 2026-10-04 |
| Bulk sale tiers | 2 items 5% off, 4 items 10%, 6 items 15%, 10 items 30% | /pages/promotions/filament-bulk-sale | fetched | 2026-10-04 |
| Bulk tier prices embedded for the PLA refill | $15.19 / $14.39 / $13.59 / $11.19 (= $15.99 × 0.95 / 0.90 / 0.85 / 0.70) | /pages/promotions/filament-bulk-sale | fetched | 2026-10-04 |
| Filaments the bulk sale covers | 11 listed: PLA Basic, PLA Matte, PLA Pure, PLA Silk+, PLA Translucent, PLA Tough+, PETG Basic, PETG Matte, PETG HF, PETG Translucent, ABS. PLA Sparkle is not on the list | /pages/promotions/filament-bulk-sale | fetched | 2026-10-04 |
| Add-on price when bought with an X2D | PLA Basic spool $13.29 (shown against $18.99); PETG Basic spool $11.89 (shown against $16.99). Only as an add-on to a printer purchase | /products/x2d | fetched | 2026-10-04 |
| Site-wide banner | "Enjoy 10% off storewide!" The terms were not read, so whether it stacks with the bulk tiers is not known | site header, every page | fetched | 2026-10-04 |

Hedges carried:

- The bulk discount needs several items in one order. The page does not say whether different
  colors or filaments can be mixed toward a tier; I did not test this at checkout.
- "From $11.19" is the 10-item tier on a refill, not the single-roll price.

## Q2. X2D running cost

| Item | Value | Source URL | Fetched or snippet | Date |
|---|---|---|---|---|
| X2D, printer only | $649 | https://us.store.bambulab.com/products/x2d | fetched | 2026-10-04 |
| X2D AMS Combo | $899 | same | fetched | 2026-10-04 |
| Combo "Print with Care" bundle | $949 ("Add only $50 to X2D Combo for 4 extra rolls of PLA Pure") | same | fetched | 2026-10-04 |
| "Print More" bundle (2 AMS 2 Pro) | $1149 | same | fetched | 2026-10-04 |
| Max power, store spec sheet | 2200 W at 220 V / 1320 W at 110 V | same | fetched | 2026-10-04 |
| Max power, Bambu wiki | 1600 W at 220 V / 1100 W at 110 V. **This disagrees with the store's 1320 W at 110 V.** Max power only matters for sizing a circuit, not for running cost | https://wiki.bambulab.com/en/general/power-consumption | fetched | 2026-10-04 |
| X2D, steady-state printing PLA | 250 W at both 110 V and 220 V, measured at 25 °C ambient | same wiki page | fetched | 2026-10-04 |
| X2D, steady-state printing PC | 550 W | same | fetched | 2026-10-04 |
| X2D standby | 7.3 to 7.8 W offline; 7.8 to 8.2 W on WiFi | same | fetched | 2026-10-04 |
| X2D Low Power Mode | about 750 W (the wiki lists it with the peak figures) | same | fetched | 2026-10-04 |
| AMS 2 Pro | standby 1 W, working 12 W, drying 80 W | same | fetched | 2026-10-04 |
| Other models on the same page, PLA, for comparison | P2S steady 200 W; X1C average 105 W; H2D average 197 W; H2S and H2C 200 W | same | fetched | 2026-10-04 |
| Electricity, US residential average | 18.31 ¢/kWh in July 2026; 17.30 ¢ for 2025; 16.48 ¢ for 2024 (EIA Electric Power Monthly Table 5.3, released Sep 24, 2026, data through July 2026) | https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=table_5_03 | fetched | 2026-10-04 |
| Textured PEI plate for the X2D | $34.99 | https://us.store.bambulab.com/products/bambu-textured-pei-plate | fetched | 2026-10-04 |
| Engineering plate for the X2D | $39.18 (shown against $48.97) | Bambu US store, plate product page | fetched | 2026-10-04 |
| Multi-size hotend kit, X2D / P2S | 0.2 + 0.6 mm $34.18; 0.2 + 0.6 + 0.8 mm $48.57; 0.2 + 0.4 + 0.6 + 0.8 mm $61.17 | Bambu US store, hotend kit page | fetched | 2026-10-04 |
| A single 0.4 mm X2D hotend | not found. Every single-hotend product address I tried came back with no product | Bambu US store | fetched (empty) | 2026-10-04 |
| Life of a hotend or a PEI plate in print hours | not found on any page I opened | none | none | none |
| Prusa calculator defaults for a machine rate | "Daily commercial usage" 6 h; repair cost 5% of the printer's price over its life; payback period set in years; filament markup default 20% | https://blog.prusa3d.com/3d-printing-price-calculator_38905/ | fetched | 2026-10-04 |
| Prusa worked example of a machine rate | printer price ÷ payback hours × print hours; pays back in 6 months = 4392 h, giving $0.21/h for an MK3S | https://blog.prusa3d.com/how-to-calculate-printing-costs_38650/ (published 2020-10-13) | fetched | 2026-10-04 |

About the power figure: the 250 W comes from Bambu's own wiki, for the X2D itself. No
stand-in model was needed. It is a single steady-state figure at 25 °C ambient. The wiki does
not give a whole-print average with heat-up included, so the first few minutes of a print
probably draw more.

## Q3. How small print businesses build a price

| Item | Value | Source URL | Fetched or snippet | Date |
|---|---|---|---|---|
| Material cost | filament price ÷ spool weight × model weight | https://blog.prusa3d.com/how-to-calculate-printing-costs_38650/ | fetched | 2026-10-04 |
| Labor | $9.50/h in the example; about 5 min of print preparation per job | same | fetched | 2026-10-04 |
| Electricity | treated as small enough to ignore (150 W at $0.09/kWh in the example) | same | fetched | 2026-10-04 |
| Machine time | printer price ÷ payback hours × print hours (see Q2) | same | fetched | 2026-10-04 |
| Failure allowance | "Margin (30% of material cost)", presented as insurance against failed prints, not as profit. Hedge carried: the author "has to observe what percentage of prints tend to fail", so 30% is a starting guess, not a measured rate | same | fetched | 2026-10-04 |
| Failure allowance, other form | a commenter on the same post divides total cost by a success rate (example 0.8) | same, comments | fetched | 2026-10-04 |
| Calculator formula | final price = (material + labor) × (100% + markup) | https://www.omnicalculator.com/other/3d-printing | fetched | 2026-10-04 |
| General formula | cost + markup = price; price for a target margin = cost ÷ (1 − margin) | https://www.shopify.com/blog/how-to-price-your-product (Lizzie Davey, Sep 3, 2026) | fetched | 2026-10-04 |
| Typical gross margins (Shopify citing NYU data) | general retail 33.18%; furniture and home furnishings 30.28%; electronics 38.77%; apparel 56.88%; food 26.31% | same | fetched | 2026-10-04 |
| Etsy's guidance | count materials, time, labor and overhead; gross margin = (revenue − cost of goods) ÷ revenue × 100; "profit margins vary widely by industry" | https://www.etsy.com/seller-handbook/article/1106022743419 | fetched (Chrome) | 2026-10-04 |
| Etsy seller example | a seller quoted on that page charges $20 to $135 for prints that cost far less in materials, because buyers treat them as gifts. One seller's account, not a survey | same | fetched (Chrome) | 2026-10-04 |
| Packaging cost per order | not found with a source | none | none | none |
| A survey of markups for 3D-printed goods specifically | not found. The margins above are general retail categories, not printed goods | none | none | none |
| Seller forums (Reddit) | not read. Reddit refused the automated request (403) | none | none | none |

On transfer: the NYU margins are for whole retail sectors at scale. They carry over to a
one-person print shop only as a rough guide. A shop this small has almost no inventory cost
and a much higher share of labor, so its margin on cost of goods can sit far above these
figures and still barely pay for the time.

## Q4. Selling fees

| Item | Value | Source URL | Fetched or snippet | Date |
|---|---|---|---|---|
| Etsy listing fee | $0.20 per listing. It runs 4 months, and on a listing with more than one in stock it is charged again on each sale | https://www.etsy.com/legal/fees/ (page reads "Last updated on Oct 5, 2026", a day ahead of my fetch date, presumably a timezone offset) | fetched (Chrome) | 2026-10-04 |
| Etsy transaction fee | 6.5% of the item price plus shipping and gift wrap | same | fetched (Chrome) | 2026-10-04 |
| Etsy Offsite Ads | 15% of the order for shops under $10k in sales over the past 365 days (they can opt out); 12% for shops at or above $10k (required, for the life of the shop); capped at $100 per order; charged only on orders that come through an ad | same | fetched (Chrome) | 2026-10-04 |
| Other Etsy fees | a possible one-time shop set-up fee; Etsy Plus $10/mo (optional); currency conversion 2.5%; a regulatory operating fee in some countries | same | fetched (Chrome) | 2026-10-04 |
| Etsy payment processing, US | "3% + 0.25 USD", charged on the whole order including shipping and tax | https://www.etsy.com/legal/etsy-payments/ (updated Jul 31, 2026) | fetched (Chrome) | 2026-10-04 |
| Etsy rule for 3D-printed goods | listed under "Items produced using computerized tools" (laser printer, 3D printer, CNC, and so on): "These items must be produced based on a seller's original design". Etsy's own example of something that counts as made by the seller is a bust printed on a 3D printer | https://www.etsy.com/legal/creativity/ (updated Jun 10, 2025) | fetched (Chrome) | 2026-10-04 |
| Shopify Basic | $39/mo billed monthly, or $29/mo billed yearly; trial "3 days free, then $1/month for 3 months" | https://www.shopify.com/pricing | fetched | 2026-10-04 |
| Shopify Basic card rates | online 2.9% + 30¢; in person 3.5% + 10¢; using a third-party payment provider adds 2% | same | fetched | 2026-10-04 |
| Shopify higher plans | Grow $79/mo (online 2.7% + 30¢, third-party fee 1%); Advanced $299/mo (online 2.5%); Plus from $2,300/mo (2.25%). I did not read the third-party fee for Advanced and Plus closely enough to report it | same | fetched | 2026-10-04 |
| Shopify "Agentic" plan | $0/mo at 2.9% + 30¢. What it includes was not studied | same | fetched | 2026-10-04 |

Hedge carried on the Etsy rule: "original design" is the condition. A coaster printed from
someone else's model file would not meet it. Coasters from Omar's own naqsh constructions
would, but whether the Islamic patterns themselves need credit to a source is a question for
another doc.

## Q5. Market prices for printed coasters

Method: Etsy search in Chrome, first page of results only, read on 2026-10-04. The price on a
card is the sale price when one is shown, and it may be the cheapest variant (a single, say)
of a listing that also sells sets. Card prices are therefore a low bound on what the listing
sells for. Each search below is its own set; the counts are listings seen, not Etsy's totals.

| Search (URL `https://www.etsy.com/search?q=...`) | Listings seen | Min | Q1 | Median | Q3 | Max | Notes | Fetched | Date |
|---|---|---|---|---|---|---|---|---|---|
| `3d+printed+coasters` | 59 | $4.00 | $13.99 | $21.97 | $33.73 | $55.00 | 24 were ads, 16 on sale. Mixed set: includes a $6.90 STL file library plus cotton, wood, laser-engraved and stone coasters | fetched (Chrome) | 2026-10-04 |
| same, only titles containing "3d print" | 22 | $4.49 | $18.34 | $20.80 | $31.00 | $55.00 | narrower and closer to our product | fetched (Chrome) | 2026-10-04 |
| `geometric+3d+printed+coasters` | 58 | $3.99 | $18.74 | $25.00 | $30.53 | $44.95 | | fetched (Chrome) | 2026-10-04 |
| same, only titles containing "3d print" | 31 | $3.99 | $17.99 | $22.85 | $29.62 | $40.64 | | fetched (Chrome) | 2026-10-04 |
| `islamic+geometric+coaster` | 57 | $2.95 | $16.00 | $25.00 | $31.00 | $190.00 | 22 ads, 16 on sale. Mostly ceramic, wood, marble and glass; the printed ones are listed below | fetched (Chrome) | 2026-10-04 |
| `resin+geometric+coasters` (resin comparable) | 12 | $11.99 | $19.57 | $26.50 | $30.25 | $39.99 | only 5 of the 12 cards mention resin or epoxy, so this is a weak resin set | fetched (Chrome) | 2026-10-04 |
| `laser+cut+geometric+coasters` (laser comparable) | 63 | $1.66 | $11.94 | $25.00 | $31.50 | $99.95 | 28 of the 63 cards mention laser | fetched (Chrome) | 2026-10-04 |

Examples from the `3d printed coasters` search: a 6-piece snail set $31; a Desert Sunset set
$34.99 (shown against $69.98); a set of 4 "LINED" $26.46 (shown against $52.92); a set of 4
geometric $26.39 (shown against $32.99); a wavy set of 6 with holder $35; Monstera sets
$18.97 to $47.50; a set of 4 Mecca crate $40; and a wood and epoxy resin set of 6 at $39.99,
the one resin comparable in that search.

Islamic or Arabic printed coasters, each listing page opened in Chrome:

| Listing id | What it is | Price | Material, from the listing page | Price per coaster |
|---|---|---|---|---|
| 1887433579 | Islamic geometric, set of 5 (quantity choice 1 to 8) | $35.00 | "Materials: PLA" | $7.00 |
| 4411122673 | Islamic geometric, set of 4 with holder | $25.00 | "Materials: Pla" | $6.25 |
| 1894065811 | Arabic calligraphy, 6-piece set | $45.00 | "Materials: PLA", and "3D print" in the text | $7.50 |
| 4537645821 | Islamic geometric, set of 4, marble effect, Moroccan star | $20.76 | no Materials line; "PLA" appears in the page text | $5.19 |
| 4369156051 | Islamic geometric, Palestine | $25.00 | no Materials line; "PLA" appears in the page text. How many coasters it includes was not read | unknown |

So 5 printed Islamic listings were seen, at $20.76 to $45.00 a listing, median $25.00. For
the 4 whose set size was read, the price per coaster is $5.19 to $7.50. The two without a
Materials line are only probably printed: "PLA" on the page could come from a recommended
listing rather than the listing itself.

Islamic-titled coasters in other materials, from the same search: a laser-cut wood set of 4
$16; wood arabesque sets $30 (5 pieces) and $34; ceramic Moroccan and Arabic tiles from $3.39
to $27.70; a marble Bismillah coaster $34.99; Mughal marble-inlay set of 4 $34.99; glass
$17.99; wood and cork set of 6 $36.

Not found: sales volume. A listing's price says what sellers ask, not what buyers pay or how
often they buy.

## Design notes: recommended inputs

These are my suggestions for the formula's inputs, each with how sure I am. The arithmetic is
shown so the formula's author can redo it with other choices.

| Input | Recommended value | How I got it | Confidence |
|---|---|---|---|
| Filament cost | $15.99/kg (PLA Basic or Matte refill, one at a time); $13.59/kg when buying 6 at once; $11.19/kg at 10. Use $24.99/kg for Sparkle, which has no refill and no bulk tier | Q1 store prices | high for that day's prices; they change |
| Filament per full coaster plate | 27 g × $15.99/kg = **$0.43**; at the 10-roll tier, $0.30; at spool price, $0.51; in Sparkle, $0.67 | measured 27 g × Q1 | high |
| Electricity per hour | (250 W printer + 12 W AMS) × $0.1831/kWh = **about $0.05/h**; about $0.08 for a 98 min plate | Q2 wiki + EIA July 2026 US average. Omar's own utility rate would replace the national average | medium: the 250 W is steady state only, and the rate is a national average |
| Machine wear and payback per hour | $899 combo ÷ (6 h/day × 365 × 2 years = 4380 h) = **$0.21/h**, plus repairs at 5% of price over that life = $0.01/h. About $0.35 for a 98 min plate | Prusa's method and defaults, with the X2D price. The 6 h/day and 2-year life are Prusa's defaults and my choice, not measured on this printer | low: the hours per day and the life are guesses to replace with Omar's actual use |
| Plates and hotends | not costed per hour. A PEI plate is $34.99 and a 4-hotend kit $61.17, but no source gave a life in hours | Q2 | not found; make it a calibration bet or log replacements |
| Failure allowance | divide the cost by the share of plates that come out good (start at 0.8 until Omar's print log gives a real rate), or add 30% of material | Prusa post and its comments | low: both are guesses until the print log measures a real failure rate |
| Labor | Omar's own minutes per order (unpacking, pressing pieces in, packing) times an hourly rate. Prusa's example uses $9.50/h and 5 min of prep | Q3 | not measured here; it is likely the biggest cost per coaster, so it should be timed |
| Packaging | not found | none | not found |
| Etsy fees on a $25 order, free shipping | 6.5% ($1.63) + 3% + $0.25 ($1.00) + listing $0.20 = **$2.83, about 11%**. If the order came from an Offsite Ad, add 15% ($3.75), for about 26% in total | Q4 | high for the rates; whether a sale came from an ad is per order |
| Shopify fees | 2.9% + $0.30 per order, plus $29 to $39 a month for the plan | Q4 | high for the rates |
| Market price anchor | printed coasters on Etsy sit around **$20 to $25 a listing** (medians of $20.80 to $25.00 across the four printed and geometric sets above). Printed Islamic sets seen: $20.76 to $45, or $5.19 to $7.50 a coaster | Q5 | medium: first page of results only, asking prices not sales, and some card prices are the cheapest variant |
| Color swap cost | 1.6 min per swap, but only on multi-color plates; zero for Omar's current one-color plates | given | high for one-color plates |

Hard cost of one full coaster plate in one color, before labor, packaging and failures:
$0.43 filament + $0.08 power + $0.35 machine = **about $0.86**. The cost is small next to
market prices. The open costs are labor, packaging and the failure rate, and none of the
pages I read can supply them; they have to be measured on Omar's own orders.

One assumption to check: I took "a full coaster plate" to mean the plate that makes one
coaster (frame and pieces). If a plate makes more than one, divide the per-plate costs by
that number.
