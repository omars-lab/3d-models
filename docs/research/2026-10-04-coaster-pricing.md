---
date: 2026-10-04
produced-by: checker agent (Claude Opus 5.5), method — checker over pricing-a (PR #544) and pricing-b (PR #545); the load-bearing sources re-opened on 2026-10-04 with curl (Bambu US store product pages read from their embedded JSON-LD and page text, the Bambu wiki power page, EIA tables 5.3 and 5.6.A, both Prusa pages, Shopify pricing and blog, Omni), the Bambu forum's Discourse JSON (topics 259832, 256018, 251064, 246829), and one Chrome tab of my own for Etsy (fees, payments and creativity policies, two searches re-run, six listings opened), closed at the end
feeds:
  - order-driven-lab-design (being written)
---

# Coaster pricing inputs (consolidated)

This is the one to act on. It checks two independent research passes,
[pricing A](2026-10-04-coaster-pricing-a.md) (PR #544) and
[pricing B](2026-10-04-coaster-pricing-b.md) (PR #545), against the pages behind them. The two
files stay as the record this was built from.

The product: one coaster about 112.5 mm across, a frame plus press-in loose pieces, printed on a
Bambu X2D with an AMS, one color per plate. The measured print facts both passes were given: a
full plate (frame and every loose piece, which is one coaster) sliced at 86 min and about 27 g of
PLA Basic and printed in about 98 min; a small plate sliced at 12 min and 3.5 g and printed in 13
to 14 min; an AMS color swap costs about 1.6 min plus prime-tower waste, which no longer applies
because plates are one color.

How to read this:

- **Re-opened** means I loaded the page myself on 2026-10-04 and read the value. **Carried** means
  I did not re-open it and am relying on a research file's own mark (fetched or snippet).
- Store and marketplace prices are that day's listed prices, not lasting facts.
- Etsy numbers are first-page search results, which Etsy ranks by relevance and personalizes. The
  counts are listings seen, never Etsy's totals.

## The short answer

1. **Machine and material cost about $1 a coaster; the market asks $20 to $45 a set.** Filament
   is $0.43, power about $0.08, printer wear $0.34 to $0.73 depending on how many hours the
   printer is assumed to last. Both passes reach the same picture: the price is set by labor,
   fees and markup, not by the machine.
2. **The things that decide the price are not on any web page.** Labor minutes per order,
   packaging, the failure rate, and the printer's real hours of use must be measured on Omar's own
   orders. Both passes say so.
3. **Two conflicts settled, one left open.** The X2D's maximum draw is 1100 W at 110 V (B was
   right; A read an H2D table embedded on the X2D page). Shopify Basic's in-person rate is 2.6% +
   10¢ (B was right; 3.5% + 10¢ is the keyed-in rate). The forum's "$10.91 a roll at 10" does not
   match any line on the store today; use the store's $11.19.
4. **Two palette entries are priced wrong by their line label.** Plain PLA Silk is gone from the
   US store, so Silk Gold (13401) cannot be bought there; Gilded Rose (13901) is on sale, but as
   PLA Silk Multi-Color at $24.99 with no refill and no bulk discount.

## What the two passes agreed on

Every row here was found by both passes and re-opened by me unless the last column says carried.

| Claim | A | B | What the source says on 2026-10-04 | Status |
|---|---|---|---|---|
| PLA Basic, 1 kg | refill $15.99 (30 colors), spool $18.99 (13) | same | JSON-LD: 30 offers at $15.99, 13 at $18.99, all in stock | agree, re-opened |
| PLA Matte, 1 kg | refill $15.99 (25), spool $18.99 (6) | same, 1 refill out of stock | 24 + 1 out of stock at $15.99, 6 at $18.99 | agree, re-opened |
| PLA Silk+, 1 kg | refill $15.99 (4: Gold, Silver, Titan Gray, White), spool $18.99 (13) | same | same; the four refill codes are 13405, 13109, 13108, 13110 | agree, re-opened |
| PLA Sparkle | $24.99 spool only (6), no refill, not on the bulk list | same | 6 offers at $24.99, no refill | agree, re-opened |
| PETG Basic | refill $13.99, spool $16.99 (13 each) | same | same | agree, re-opened |
| Plain PLA Silk | not a current product | not found | `/products/pla-silk` returns HTTP 404 with no product data (A said "no product data", B said 404; both true). The PLA collection page links only Silk+ and Silk Multi-Color | agree, re-opened |
| Bulk tiers | 2 items 5%, 4 items 10%, 6 items 15%, 10 items 30% | same | same, on the bulk-sale page | agree, re-opened |
| Bulk headline | "PLA from $11.19, PETG from $9.79" | same | same; the PLA Basic and Matte pages each read "$11.19 USD /roll (Lowest price for 10+ rolls) MSRP: $15.99" | agree, re-opened |
| Lines in the bulk sale | 11 named | the same 11 | PLA Basic, PLA Matte, PLA Pure, PLA Silk+, PLA Translucent, PLA Tough+, PETG Basic, PETG Matte, PETG HF, PETG Translucent, ABS. Sparkle and Silk Multi-Color are not on it | agree, re-opened |
| X2D price | $649; AMS Combo $899; Print with Care $949; Print More $1,149 | same | four offers at those prices, all in stock | agree, re-opened |
| X2D steady-state draw | 250 W printing PLA, 550 W PC, at 25 °C ambient | same | wiki and the X2D's own store spec table both say 250 W / 550 W | agree, re-opened |
| US residential electricity | 18.31 ¢/kWh, July 2026 | same | EIA Electric Power Monthly, data for July 2026, released Sep 24, 2026: U.S. total residential 18.31 | agree, re-opened |
| Textured PEI plate, X2D | $34.99 | same | the X2D variant is $34.99 | agree, re-opened |
| Prusa machine rate | printer price ÷ payback hours × print hours; 6 months = 4,392 h gives $0.21/h for an MK3S | same, plus $0.10/h for the MINI | same. Note 4,392 h is 6 months of round-the-clock printing (183 days × 24 h), not 6 months of normal use | agree, re-opened |
| Prusa failure margin | 30% of material cost as a starting guess | same | "for starters, he set the margin to be 30% of the material (filament or resin) price", after saying he "has to observe what percentage of prints tend to fail" | agree, re-opened |
| Prusa on electricity | negligible | negligible, under $0.023 a print at 100 to 150 W and $0.07 to $0.09/kWh | same | agree, re-opened |
| Prusa labor | about 5 min of preparation a print, $9.50/h | 5 min | same; the $9.50/h is the 2020 Czech average wage | agree, re-opened |
| Shopify's formulas and margins | cost + markup; cost ÷ (1 − margin); NYU margins general retail 33.18%, home furnishings 30.28%, apparel 56.88% | same | same | agree, re-opened |
| Omni formula | (material + labor) × (100% + markup) | same, no default markup | same | agree, re-opened |
| Etsy listing fee | $0.20, 4 months; a multi-quantity listing renews at $0.20 after each sale | same | "the listing will be automatically renewed at $0.20 after each of the items sells" | agree, re-opened |
| Etsy transaction fee | 6.5% of item price plus shipping and gift wrap | same | same | agree, re-opened |
| Etsy Offsite Ads | 15% under $10k sales in the prior 365 days (can opt out); 12% at or over, for the life of the shop; capped at $100 an order | same, plus orders within 30 days of the ad click | same | agree, re-opened |
| Etsy Payments, US | 3% + $0.25 on the whole order including shipping and tax | same | US row "3% + 0.25 USD"; "assessed on the gross order amount, including shipping and tax"; page updated Jul 31, 2026 | agree, re-opened |
| Etsy rule for 3D-printed goods | made with computerized tools, "must be produced based on a seller's original design"; example a 3D-printed bust | same | same; page updated Jun 10, 2025 | agree, re-opened |
| Shopify Basic | $39/mo monthly, $29/mo yearly; online 2.9% + 30¢; third-party gateway +2% | same | same | agree, re-opened |
| Etsy fees on a $25 order, no shipping or tax | $2.83, about 11%; with an Offsite Ad +$3.75, about 26% | $2.83 (11.3%); $6.58 (26.3%) | arithmetic checked: 1.625 + 1.00 + 0.20 = 2.825; + 3.75 = 6.575 | agree |
| Material for one coaster | 27 g × $15.99/kg = $0.43; $0.30 at the 10-roll tier | same | arithmetic checked | agree |
| Power for one coaster | about $0.08 | $0.075 | (250 W + 12 W AMS) × 1.63 h × $0.1831 = $0.078 | agree |
| Market band, printed coasters | listing medians $20.80 to $25.00 across 4 printed or geometric searches | listing medians $24.93 to $27.99 across 7 printed searches; title-says-printed group median $22.99 (74 listings) | my re-run of `3d printed coasters`: 62 listings, median $25.00; the 19 whose titles say 3D printed, median $22.00. My re-run of `islamic geometric coaster`: 61 listings, min $1.75, Q1 $16.14, median $25.00, Q3 $34.00, max $190.00 (A saw 57 and B 56, both median $25.00) | agree, re-opened |
| Islamic printed sets | 1887433579 set of 5 $35 PLA; 4411122673 set of 4 + holder $25 PLA | the same two | re-opened: both say "Materials: PLA" at those prices; 1887433579 is 4.5 in across | agree, re-opened |
| Wear-part lifetimes | not found | not found from Bambu; one owner's ~300 h of PLA on an older plate (snippet) | nothing in hours from Bambu on either pass | agree, not found |
| Packaging cost | not found | only inside one forum example | no source | agree, not found |

## Where they disagreed, and which side the source backs

### X2D maximum power at 110 V: 1100 W or 1320 W

- **A:** the store spec sheet says 2200 W at 220 V / 1320 W at 110 V; the wiki says 1600 W /
  1100 W; A reported the two as a conflict.
- **B:** 1100 W at 110 V from the store page, picking the X2D table out by its 256 × 256 × 260 mm
  volume and 16.25 kg weight, and noting that the page also embeds an H2D table at 1320 W.
- **Source:** the X2D store page holds two spec tables. The 1320 W table sits beside "Physical
  Dimensions 492*514*626 mm³" and "Net Weight 31 kg", which are the H2D's. The table with "Main
  Nozzle Printing: 256*256*260 mm³" and "Net Weight 16.25 kg (Gross Weight: X2D 20.2 kg, X2D AMS
  Combo 22.2kg)" reads "Max Power 1100 W@110 V" and "PLA (25 °C): 250 W@110 V". The wiki's X2D
  row also reads 1600 W at 220 V and 1100 W at 110 V.
- **Verdict: B.** There is no conflict for the X2D: 1100 W at 110 V, from both Bambu sources. It
  only matters for sizing a circuit, not for running cost.

### Shopify Basic in-person rate: 3.5% + 10¢ or 2.6% + 10¢

- **A:** in person 3.5% + 10¢. **B:** in person 2.6% + 10¢.
- **Source:** the pricing page's Basic column lists "In-person card rates 2.6% + 10¢" and
  "In-person manual rates 3.5% + 10¢" (a card number typed in by hand). It also lists "Online
  premium card rates 3.5% + 30¢", which neither pass reported.
- **Verdict: B** for a card that is tapped or swiped. A's figure is the keyed-in rate. Neither
  matters until Omar sells in person.

### The 10-roll floor: $10.91 or $11.19

- **A:** $11.19 (the store's bulk page and the PLA refill's 30% tier). **B:** found both: the
  store's $11.19, and Bambu's own forum announcement of 2026-09-16, "Bulk discount prices as low
  as $10.91/roll when you buy 10 rolls".
- **Source:** both are real. The announcement (forum topic 259832, post 1, the BambuLab account)
  says $10.91 and "details vary by region and filament". On the store today the lowest 10+ price
  on each bulk line is: PLA Basic, PLA Matte, ABS, PETG HF and PETG Translucent $11.19; PLA
  Silk+ and PLA Translucent $13.29; PLA Pure $13.99; PLA Tough+ from $14.69; PETG Basic and PETG
  Matte $9.79. None of the 11 lines shows $10.91. $10.91 would be 30% off $15.59, and no line I
  checked lists $15.59.
- **Verdict: use $11.19 for PLA Basic and Matte.** It is what the store charges today and it is
  exactly 30% off $15.99. The $10.91 is unexplained: possibly a launch price, another region, or
  a typo. Flagged, not used. Neither page says how long the 30% tier lasts.

### A single X2D 0.4 mm hotend: none found, or $17.99

- **A:** not found; every single-hotend address tried came back empty. A found only kits: 0.2 +
  0.6 mm $34.18, 0.2 + 0.6 + 0.8 mm $48.57, 0.2 + 0.4 + 0.6 + 0.8 mm $61.17.
- **B:** "Bambu Hotend - H2/P2S/X2D", Standard Flow 0.4 mm hardened steel $17.99, High Flow
  $49.99.
- **Source:** `us.store.bambulab.com/products/bambu-hotend-h2-p2s` lists "Standard Flow / X2D /
  0.4mm Hardened Steel" at $17.99, in stock, and High Flow X2D 0.4 mm at $49.99.
- **Verdict: B.** A's kit prices are carried (not re-opened). For wear, use $17.99 a hotend.

### Two of the Islamic listings: printed or not

- **4537645821** ($20.76, set of 4, "Marble Effect"). A: probably printed, because "PLA" appeared
  on the page. B: marble, a comparable. **Source:** there is no Materials line; the description
  says "Finished in an elegant marble-effect texture" and "Lightweight yet sturdy", and names no
  material. On my load "PLA" appeared nowhere on the page. **Verdict: neither.** It is not real
  marble ("marble-effect") and not shown to be printed. Leave it out of both sets.
- **4369156051** ($25.00, Palestine). A: probably printed ("PLA" in the page text), set size not
  read. B: ceramic. **Source:** "What's included: 4 ceramic coasters" and a gold-leaf stir spoon.
  **Verdict: B.** Ceramic, set of 4. A's own hedge (the "PLA" could come from a recommended
  listing) was the right one.

So the printed Islamic listings both passes found and I confirmed are three by A's count, not
five: 1887433579, 4411122673, and A's 1894065811 (below).

### Smaller points

- **Silk+ at 10 rolls.** B's design notes put the Silk+ 10+ floor at $13.29 ($0.0133/g). The
  page's $13.29 is 30% off the $18.99 *spool* (it reads "MSRP: $18.99"). A Silk+ *refill* at the
  10-item tier would be $15.99 × 0.70 = $11.19 by the same rule, but the page does not show that
  number. Treat $13.29 as the spool floor; $11.19 for the refill is arithmetic, not read.
- **Owner-measured draw.** B's notes say owners measured "70 to 170 W on similar machines". The
  forum post (topic 251064, post 1) is an X2D owner: "~170w vs ~70w" doing the same PETG prints,
  where 70 W was his old X1C. So ~170 W is the one owner reading for the X2D itself, on PETG, below
  Bambu's 250 W PLA figure. One person, one material.
- **Prusa's hedge.** B attaches "many people … see it differently" to the 30% failure margin. On
  the page that sentence follows the whole order's price, not the margin. The margin's own hedge is
  the "has to observe what percentage of prints tend to fail" line both passes quote.

## What only one pass found

### Only A

| Claim | Status |
|---|---|
| Electricity history: 17.30 ¢ for 2025, 16.48 ¢ for 2024 | re-opened (EIA table 5.3 annual rows) |
| X2D standby 7.3 to 7.8 W offline, 7.8 to 8.2 W on WiFi; Low Power Mode about 750 W; AMS 2 Pro 1 W standby, 12 W working, 80 W drying | re-opened (wiki) |
| PLA Basic $13.29 and PETG Basic $11.89 as add-ons bought with an X2D | re-opened (X2D page, `discountPrice` 13.29 against 18.99); only with a printer purchase, so not a running cost |
| Prusa calculator defaults: 6 h daily commercial use, 5% of printer price for repairs over its life, 20% filament markup | re-opened |
| Prusa commenter: divide cost by a success rate (example 0.8) | re-opened ("1.0 = always succeeds and 0.8 = fails 20% of the time … I divide by this factor") |
| Islamic listing 1894065811: 6-piece Arabic calligraphy set, $45, "Materials: PLA", "3D-printed" | re-opened |
| "Enjoy 10% off storewide!" banner | re-opened, and **weaker than stated**: in the page source the line is the description of a "Maker's Supply Anniversary Sale" page, not a filament offer. Do not assume it applies to filament or stacks with the bulk tiers |
| Engineering plate $39.18 (against $48.97); hotend kits $34.18 / $48.57 / $61.17 | carried (fetched by A) |
| Shopify Grow $79 (2.7%), Advanced $299 (2.5%), Plus from $2,300 (2.25%) | re-opened; third-party fees on those plans are 1%, 0.6% and 0.2% |
| Etsy seller-handbook example of a seller charging $20 to $135 for prints, because buyers treat them as gifts | carried (A, Chrome); one seller's account |
| Resin and laser comparable searches (12 and 63 listings, medians $26.50 and $25.00) | carried; A's own hedge: only 5 of the 12 "resin" cards mention resin |

### Only B

| Claim | Status |
|---|---|
| State electricity rates: NY 29.90, CA 33.61, TX 15.88 ¢/kWh (July 2026) | re-opened (EIA table 5.6.A) |
| Bambu's 2026-09-16 price cut: PLA Basic refill to $15.99, PETG Basic $13.99, PLA Pure $16.99, bulk from 2 rolls, free US shipping from $59 (was $89) | the "$10.91/roll" line re-opened (forum topic 259832 post 1); the rest carried. The PLA Basic and PETG Basic refill prices match today's store pages; PLA Pure's page shows $19.99 against its 10+ floor, so its $16.99 was not confirmed |
| Lifetime-based rate: "assume a life time of 2000h, an H2C at ±2000$ and 300$ in replacement parts", "more like 1.2$ / h"; an A1 "closer to 0.3$ / h" | re-opened (topic 256018 post 4). One forum member's assumption, not a measured life |
| "The printer costs basically nothing"; labor first, filament second | re-opened (topic 256018 post 3) |
| Failure allowance by rate: "If 5% of comparable prints fail, the successful jobs need to recover a little over 5% extra"; "fails 1 in 10 times needs the other 9 to cover it" | re-opened (posts 9 and 12) |
| Full cost-plus: price = (production cost + development ÷ expected units) × (1 + markup); "Unattended machine time is not the same as paid labour" | re-opened (post 15) |
| Worked forum examples: 45.57 € plus 20 to 30% for failures, "roughly 55–60€"; a second at ≈ 18 to 22 € with packaging and platform at 2 € | re-opened (topic 246829 posts 25 and 28; post 25 calls itself "a theoretical model") |
| Rules of thumb: "Minutes x $0.28"; material × 2; material × 2 × 2; "$2" an hour plus filament | "Minutes x $0.28" re-opened (topic 256018 post 2); the others carried (topics 221025, 197260) |
| P1S energy: 8.4 kWh for ~100 h in a month | carried (topic 252520); a different printer |
| P1S warm-up ~850 W for 30 to 60 s; four-P1S monthly average; hardened nozzle never worn out; ~300 h on a plate | **snippets only** in B. Flagged, not used |
| PEI plates "keep trucking until they have literal holes in them" | carried (topic 184785); one owner |
| Silk Multi-Color, PETG HF, Gradient, Marble, Galaxy prices | Silk Multi-Color re-opened ($24.99, 10 colors, spool only); PETG HF re-opened ($15.99 refill, 10+ floor $11.19); the rest carried |
| Shopify Payments in-person 2.6% + 10¢ | re-opened (see the disagreement above) |
| Etsy: transaction fee not charged on US sales tax; Pattern $15/mo; set-up fee amount not stated | carried |
| Per-coaster price distributions and set-of-4 / set-of-6 groups (286 unique physical listings across 9 searches; title-printed per coaster median $5.00 over 39 listings; set of 4 median $20.00 over 23; set of 6 median $25.50 over 12) | carried; B's regex sort was checked by hand on 13 listings only |
| Islamic or Arabic printed listings: 4413086895 ($7, set of 4, PLA + cork, 9.2 cm), 4527598674 ($16.14, set of 6, 3.74 in, not geometric), 4440970337 ($22.85, options single / 4 / 6), 4334311750 ($25, set of 4, PETG, Kufic), 1873629785 ($35, set of 5, calligraphy), 1879888010 ($45, set of 6, geometric + calligraphy) | 1879888010 re-opened ("Materials: PLA", "6-piece", $45); the other five carried |
| None of the printed comparables looked like a frame with press-in loose pieces | carried; a difference in the product, not evidence of a premium (B's own hedge) |

**One thing neither pass noted.** Three of the four printed Islamic listings I opened are from
one Texas shop (1887433579 "Made by Tawakkul", 1879888010 and 1894065811 both from
TawakkulDesignsStore, with the same description text). The "Islamic printed" price band leans
heavily on one seller's prices.

## Plain PLA Silk and the palette

The color palette `.claude/skills/color-themes/palette.yaml` lists Gold as line "PLA Silk", code
13401, and Gilded Rose as line "PLA Silk", code 13901.

- **Gold 13401.** The US store has no plain PLA Silk: its product address returns 404, the PLA
  collection links only Silk+ and Silk Multi-Color, and the code 13401 appears on none of the 19
  store pages fetched for this check (listed under sources). No page says plain Silk is discontinued; it is simply not
  sold on the US store today (K1: absent, not "discontinued"). What it means: a theme using 13401
  can only be printed from a spool Omar already owns, and an order cannot be priced from a store
  price. The nearest live color is **Silk+ Gold, 13405** ($15.99 refill, $18.99 spool, in the bulk
  sale), which the palette already carries as its own entry with a different hex (#F4A925 against
  #E5B03D). Swapping 13401 for 13405 is a color change that has to be looked at, not a rename.
- **Gilded Rose 13901.** On sale and in stock, but under **PLA Silk Multi-Color** at $24.99 for a
  1 kg spool, no refill, not in the bulk sale. Price it at $24.99/kg (27 g = $0.67 a coaster),
  and the line label in the palette is out of date.

For pricing: a theme's filament cost should come from the line the code is sold under today, and
a code the store does not sell should be marked "stock on hand only" rather than priced.

## Recommended inputs

Worked figures use the full one-coaster plate: 27 g and 98 min (1.63 h) as printed. "Measure"
means the value must come from Omar's own orders and print log; nothing on the web can supply it.

| Input | Value (or range) | Source | Confidence | Measure on own orders? |
|---|---|---|---|---|
| PLA Basic / Matte, per kg | $15.99 refill bought singly; $18.99 with spool; $13.59 at 6 items; $11.19 at 10 items | Bambu US store product and bulk pages, both passes, re-opened | high for 2026-10-04; the 30% tier is called a sale with no end date | no; refresh the price |
| PLA Silk+, per kg | $15.99 refill (Gold, Silver, Titan Gray, White only); $18.99 spool; spool at 10 items $13.29 | store, both passes, re-opened | high for that day | no |
| Sparkle, Silk Multi-Color (incl. Gilded Rose) | $24.99, spool only, no bulk tier | store, re-opened | high | no |
| PETG Basic, per kg | $13.99 refill; $9.79 at 10 items | store, re-opened | high | no |
| Filament per coaster | grams from the slice × $/kg. Full plate: 27 g → $0.43 refill, $0.51 spool, $0.30 at 10 items, $0.67 for Sparkle or Silk Multi-Color | Omar's 27 g × the rows above | high | grams yes (slicer, per design) |
| Waste beyond the slice | none on a one-color plate; on a multi-color plate about 1.6 min per swap plus prime-tower filament | given facts | high for one color | only if multi-color returns |
| Printer power while printing | 262 W (250 W X2D PLA steady state + 12 W AMS 2 Pro working); one owner saw ~170 W on PETG | Bambu wiki and X2D store spec (re-opened); forum 251064 (re-opened, one owner) | medium: Bambu's figure is steady state at 25 °C, no measured X2D average on PLA | optional: a plug meter for one plate settles it |
| Electricity rate | $0.1831/kWh US average (July 2026); states range from 15.88 ¢ (TX) to 33.61 ¢ (CA) in the rows read | EIA tables 5.3 and 5.6.A, re-opened | high for the average | yes: Omar's own utility rate |
| Power per coaster | $0.05 to $0.08 at the US average; about $0.14 at California's rate | derived | medium; small either way | follows the two rows above |
| Printer price | $899 (X2D AMS Combo) | store, both passes, re-opened | high that it is today's price | no; use what was actually paid |
| Payback hours (a setting) | 2,000 h → $0.45/h; 4,380 h (6 h a day for 2 years) → $0.21/h. Plus repairs at 5% of price over that life, about $0.01 to $0.02/h | B: forum assumption for an H2C (re-opened); A: Prusa calculator's 6 h/day and 5% defaults with a 2-year life A chose (re-opened). Prusa's own 4,392 h is 6 months nonstop | low: no source measured an X2D's life; both numbers are assumptions | yes: real hours of use a day and how long the printer is kept |
| Printer wear per coaster | $0.34 (4,380 h) to $0.73 (2,000 h) | derived | low, follows payback hours | follows the row above |
| Wear parts | hotend $17.99 (X2D standard 0.4 mm); Textured PEI plate $34.99; no life in hours from any source | store, re-opened | prices high; lives not found | yes: log each replacement against print hours, or fold into the failure allowance as Prusa does |
| Failure allowance | divide cost by the share of plates that come out good (start at 0.8 until the log has a rate), or add 30% of material ($0.13 a coaster) | Prusa post and its comment (re-opened); forum topic 256018 (re-opened) | low: every figure is a starting guess | **yes**: the print log's kept / failed count |
| Labor | Omar's hands-on minutes per order (slice and send, clear the plate, press pieces in, pack) × an hourly rate he picks. Reference points only: Prusa 5 min of prep at $9.50/h (2020 Czech average wage); a forum example 30 min at 25 €/h. Unattended print time is not labor | Prusa (re-opened); forum 246829, 256018 post 15 (re-opened) | method high, minutes unknown | **yes**: time several real orders. Likely the largest cost per coaster |
| Packaging | not found in any source either pass read; one forum example lumps platform and packaging at 2 € | none | none | **yes**: cost of box, insert, label per order |
| Coasters per plate | 1 for the full plate measured | given | high for that plate | **yes** for each new plate layout: divide every per-plate cost by it |
| Etsy fees | $0.20 listing (again on each sale of a multi-quantity listing) + 6.5% of (item + shipping + gift wrap) + 3% of (item + shipping + tax) + $0.25. On $25 with no shipping or tax: $2.83 (11.3%). If the order came through an Offsite Ad, add 15% (12% once the shop passes $10k a year), capped at $100 | Etsy fees and payments policies, both passes, re-opened | high for the rates; whether an order came from an ad is per order | per order: shipping charged, ad or not |
| Shopify fees | Basic: 2.9% + 30¢ online ($1.03 on $25), 3.5% + 30¢ on premium cards, +2% with a third-party gateway; plan $39/mo or $29/mo yearly, spread over the month's orders | Shopify pricing, re-opened | high | the monthly fee per order depends on order volume |
| Markup or target margin | a setting, not a number. Only sourced benchmark: general retail gross margins 30 to 57% (NYU via Shopify), which are whole retail sectors and transfer to a one-person shop only as a rough guide (A's transfer note). Forum habits run from material × 2 to × 4, or 30 to 50% on full cost | Shopify blog (re-opened); forum (re-opened) | low as a number | Omar's call; check the result against the market band |
| Market band: printed coasters | listing medians $22 to $25 on the first page of each search, 19 to 74 listings per set (see the agreement table); per coaster about $5.00 median (39 listings, B, carried) | Etsy, both passes plus my re-runs | medium: first page only, asking prices not sales, a card may show the cheapest variant | no; repeat the search when setting prices |
| Market band: Islamic printed sets | 4 confirmed printed listings: $25 (set of 4, 4.2 in), $35 (set of 5, 4.5 in), $45 (set of 6), $45 (set of 6), so $6.25 to $7.50 a coaster. B's wider set of 7 gives a per-coaster median of $6.25, including a $1.75 set of smaller 9.2 cm coasters | Etsy listings re-opened by me (1887433579, 4411122673, 1894065811, 1879888010); B's others carried | medium-low: small set, three of the four from one shop, all smaller than 112.5 mm, none a frame with loose pieces | no; but whether the loose-piece build earns more is only learned by selling |

**Cost floor for one full coaster, before labor, packaging and fees** (not a price): filament
$0.43 + power $0.08 + printer wear $0.34 to $0.73 + 30% failure on material $0.13 = **about $0.98
to $1.37**. A's $0.86 left out the failure allowance; B's $1.37 used 2,000 h. Both agree that this
is small next to a $25 set, and that labor, fees and markup set the price.

## Open questions

- **What the $10.91 a roll in Bambu's announcement refers to.** No line on the US store shows it
  on 2026-10-04.
- **Whether bulk tiers stack with any other store discount**, and whether refills and spools of
  different lines count together toward a tier. The product pages say "Mix & Match for max
  savings"; neither pass tested a checkout.
- **How long the X2D, a hotend and a PEI plate last on PLA.** No Bambu source gives hours. A
  replacement log on Omar's own printer is the only way to get it.
- **What the X2D actually draws over a whole print**, warm-up included. Bambu gives one steady-state
  figure; a plug meter on one plate would settle it.
- **What buyers pay, not what sellers ask.** Neither pass found sales volumes; Etsy listing prices
  are asking prices.

## Sources the checker re-opened

All on 2026-10-04.

- Bambu US store (curl, JSON-LD offers and page text): products pla-basic-filament, pla-matte,
  pla-silk (404), pla-silk-upgrade, pla-sparkle, pla-silk-multi-color, petg-basic, petg-hf,
  petg-matte, petg-translucent, pla-translucent, pla-tough-upgrade, pla-pure, abs-filament, x2d,
  bambu-hotend-h2-p2s, bambu-textured-pei-plate; collections/pla; pages/promotions/filament-bulk-sale.
- Bambu wiki, general/power-consumption.
- EIA Electric Power Monthly, tables 5.3 and 5.6.A (data for July 2026, released Sep 24, 2026).
- Prusa blog: how-to-calculate-printing-costs_38650 (published 2020-10-13) and
  3d-printing-price-calculator_38905.
- Shopify: /pricing and /blog/how-to-price-your-product. Omni: /other/3d-printing.
- Bambu forum (Discourse JSON): topic 259832 post 1; topic 256018 posts 2, 3, 4, 9, 12, 15; topic
  251064 posts 1 and 9; topic 246829 posts 25 and 28.
- Etsy (Chrome): /legal/fees/, /legal/etsy-payments/, /legal/creativity/; searches
  `islamic geometric coaster` and `3d printed coasters`; listings 1887433579, 4411122673,
  1894065811, 1879888010, 4537645821, 4369156051.

Carried without re-opening, with each research file's own mark: Etsy seller handbook (A, B
fetched), B's other forum threads (221025, 197260, 252520, 184785 fetched; 172881, 173002, 26077,
8257 snippets), the remaining Etsy searches and listings in both files, Shopify blog date, and
A's hotend-kit and engineering-plate prices.
