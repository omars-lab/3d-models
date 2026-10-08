---
date: 2026-10-08
produced-by: researcher A (Claude subagent), one of two independent researchers; web search plus WebFetch. Etsy, eBay, Amazon, Faire, Redbubble, Crate & Barrel and MoMA refused WebFetch (403/500/timeout) and the Chrome extension was not connected, so every number from those sites is a search-engine snippet, marked as such
feeds:
  - docs/design/coaster/order-driven-lab-design.md §9.7 pricing
---

# Coaster market prices, raw findings (researcher A)

What this is: listed prices for decorative coasters, collected on 2026-10-08, to sit beside a
cost-plus price for a ~110 mm, 4–5 mm, one- or two-color PLA Islamic geometric coaster. Every
row says where it came from and whether the page itself was opened.

How to read the "Seen" column:

- **fetched** — I opened the page with WebFetch on 2026-10-08 and the number is from the page
  (for Shopify and Squarespace shops, often from the store's own product JSON, which lists every
  variant's price).
- **snippet** — I only saw the number in a search-result summary. The page was not opened
  (usually because the site refused automated fetches). A snippet can be stale, can pair a price
  with the wrong item, and cannot show whether a price is a sale. Treat these as weaker.

All prices are **listed (asking) prices, not sold prices.** No source I reached shows what a buyer
actually paid; Etsy and eBay sold counts were not reachable. "Sale" means the listing showed a
markdown from a higher "original" price; I give both where seen.

Per-coaster figures in brackets are my own division of the set price by the set size.

---

## Q1. Comparable coasters: prices per coaster and per set

### 1a. Islamic / Arabic / Moroccan pattern coasters, any material

| # | Seller / listing | Material, size | Set | Listed price | Per coaster | Seen | URL |
|---|---|---|---|---|---|---|---|
| 1 | Leighton House museum shop (Royal Borough of Kensington & Chelsea), "Geometric Wooden Coaster Set Dark", Islamic-art inspired | laser-cut 3 mm MDF, cork back, **110 × 110 mm** | 4 | **£24.00** (fetched). A search snippet for the same shop's set said £19.00 — older price or the lighter variant; not resolved | [£6.00] | fetched | https://museumshop.rbkc.gov.uk/products/geometric-wooden-coaster-set-dark |
| 2 | Aga Khan Museum shop, "Islamic Coasters Set (Circle) – 10 Pointed Star (Alhambra Palace)", Rahim Bhimani | maple, polyurethane; 3.95 in (~100 mm) dia; page also mentions black acrylic | 4, in embossed gift box | **$145.00** | [$36.25] | fetched | https://shop.agakhanmuseum.org/products/rahim-bhimani-coaster-set-indian-rose-tree-wood-2 |
| 3 | With a Spin, "Zahra Marble Coaster Set with Islamic Geometric Metal Inlay" | marble, brass inlay | 4, gift box, velvet lined | **$44.99, compare-at $49.99**; default option shown "Sold Out" | [$11.25] | fetched | https://shop.withaspin.com/products/zahra-marble-coaster-set |
| 4 | The Met Store, "CoasterRug Assorted Designs" (Islamic-world carpets, not geometric tiles) | nylon top, rubber back, 5 × 3.5 in | 4 | **$29.00** ($24.65 members) | [$7.25] | fetched | https://store.metmuseum.org/coasterrug-assorted-designs-80009831 |
| 5 | itsherway, "Harf Heritage Coaster" (Arabic letter, wood-burned) | natural wood, 10 cm | 6 | **AED 95.00, compare-at AED 115.00** | [AED 15.83] | fetched (product JSON) | https://www.itsherway.com/products/harf-heritage-coaster |
| 6 | Moroccan Corridor, "6 Pack Moroccan Carved Coasters with Holder" | listed as "Inox" (stainless); 8 cm | 6 + holder | **$25.99** (4 designs, same price) | [$4.33] | fetched (product JSON) | https://moroccancorridor.com/products/6-pack-moroccan-carved-coasters-and-holder |
| 7 | Nestasia (India), "Lavender / Zellij Art Framed Round Ceramic Coaster Set of 4" | ceramic, cork base, 10 cm | 4 | **₹560 sale, from ₹890**; sold out | [₹140] | fetched | https://nestasia.in/products/lavender-ceramic-coaster-set-of-4 |
| 8 | Nestasia, "Frame Patterned Ceramic Coaster Set of 4" (Moroccan tile inspired) | ceramic, cork, 10 cm | 4 | ₹660 sale, from ₹890 | [₹165] | snippet | https://nestasia.in/products/frame-patterned-ceramic-coaster-set-of-4 |
| 9 | MadeMe (UK), "Coasters – Set of four Moroccan style ceramic" | hand-decorated ceramic, cork, ~10 × 10 cm | 4 | **£14.50**, "3 in stock" | [£3.63] | fetched | https://mademe.co.uk/product/handmade-moroccan-style-ceramic-coasters/ |
| 10 | Redbubble, "Islamic Geometric Pattern … Math Formulas" (print-on-demand) | MDF, glossy, 9.5 cm sq | 4 | $15.41 | [$3.85] | snippet (fetch timed out) | https://www.redbubble.com/i/coasters/Islamic-Geometric-Pattern-Beauty-In-Every-Equation-Math-Formulas-Art-by-SplashTastic/182375689/43wr |
| 11 | Redbubble, "Modern Arabic Geometric Pattern Art" | MDF, 9.5 cm sq | 4 | $18.13 | [$4.53] | snippet (fetch 403) | https://www.redbubble.com/i/coasters/Modern-Arabic-Geometric-Pattern-Art-by-RashadSA/167998375/43wr |
| 12 | El Ryan (Iraq), "Seen Ceramic Coaster Set" (Arabic calligraphy) | ceramic, 10 cm | 4 | IQD 15,000 | [IQD 3,750] | snippet | https://www.elryan.com/en/seen-ceramic-coaster-set-4-piece-turquoise-1859841.html |
| 13 | Diwan Egypt, "Geometric Inlay Coasters" | wood inlaid with copper, bone, ebony | not stated | EGP 380, out of stock | — | snippet (fetch 403) | https://diwanegypt.com/product/geometric-inlay-coasters/ |
| 14 | Etsy, "Laser Engraved Arabesque Wood Coaster Set, Islamic Art Decor" | wood | not stated | $41.00, free shipping | — | snippet | https://www.etsy.com/market/arabic_coasters |
| 15 | Etsy, "Colorful Ornament Tile Stone Coaster Sets" (Moroccan / Persian tile) | stone | 4 | $24.69 sale, from $32.92 | [$6.17] | snippet | https://www.etsy.com/market/arabic_coasters |
| 16 | Etsy, "Dubai Coaster Set, Islamic Art Tile … Arabesque" | not stated | not stated | $3.39 sale (likely a digital file or a single; not resolved) | — | snippet | https://www.etsy.com/market/arabic_coasters |

### 1b. Geometric coasters, other materials (not Islamic-specific), for the band around ours

| # | Seller / listing | Material, size | Set | Listed price | Per coaster | Seen | URL |
|---|---|---|---|---|---|---|---|
| 17 | Zsuzsanna Horvath (Copenhagen), MOIRÉ, painted black | birch plywood 3 mm, 10 cm | 4 | **DKK 240.00** | [DKK 60] | fetched | https://www.zsuzsannahorvath.com/shop/moir-wood-coasters-set-of-4-pcs-minimalist-kitchen-decor-nordic-design-home-decor-geometric-drink-coaster-set-scandinavian-laser-cut |
| 18 | Zsuzsanna Horvath, MOIRÉ, natural | birch plywood 3 mm, 10 cm | 6 | **DKK 295.00** | [DKK 49.17] | fetched | https://www.zsuzsannahorvath.com/shop/moir-wooden-coasters-set-of-6-pcs-nordic-home-decor-laser-cut-coasters-natural-wood-coasters-coasters-for-drinks-1 |
| 19 | Lifetime Leather, Leather Hexagon Coaster Set | leather, ~3.75 × 4.25 in, snap holder | 4 + holder | **$25.00** (fetched JSON, no compare-at); a snippet showed "$18.99 on sale" | [$6.25] | fetched | https://lifetimeleather.com/products/leather-hexagon-coaster-set-1 |
| 20 | Heart of Anatolia, 4 "4x Ceramic Coaster Set" listings (Turkish tile) | handmade ceramic | 4 | **$14.70 – $19.60** (range, all four) | [$3.68–$4.90] | fetched | https://heartofanatolia.com/product-category/ceramic-collection/kitchen-utensils/trivet-coaster/ |
| 21 | Heart of Anatolia, 3 "Set of 6" listings | handmade ceramic | 6 | **$19.50 (was $29.00), $33.50 (was $49.50), $34.80 (was $49.50)** | [$3.25–$5.80 sale] | fetched | same page |
| 22 | Lasaris, "Geometric Delights" laser-cut oak | oak, 10 cm, gift box | 4 | $28 | [$7.00] | snippet (fetch SSL error) | https://lasaris.com/products/geometric-delights-laser-cut-coasters-set-85642 |
| 23 | Lasaris, "Geometric Lines" | oak or walnut, 10 cm, recycled box | 4 | $23 | [$5.75] | snippet | https://lasaris.com/products/geometric-lines-laser-cut-coasters-22776 |
| 24 | Gazer Laser, "Coaster – Geometric Laser Cut – Set of 4 with Stand" | MDF | 4 + stand | $25, "shown at $19 limited-time" | [$4.75–$6.25] | snippet | https://gazerlaser.com/products/wood-coasters/coaster-geometric-laser-cut-set-of-4-with-stand-50251072 |
| 25 | Cottonseed Marketplace, "Geometric Coasters – Set of 4" | solid wood, cork, linen bag | 4 | $25 | [$6.25] | snippet | https://cottonseedmarketplace.com/products/geometric-coasters-set-of-4 |
| 26 | Puttyprint (UK), laser-cut square geometric | oak-veneered MDF, free gift box | 4 | £15.96 | [£3.99] | snippet | https://www.puttyprint.co.uk/set-of-4-laser-cut-square-geometric-wooden-coasters |
| 27 | Crate & Barrel, Marble Coasters Set of 4 | marble | 4 | $29.95 | [$7.49] | snippet (fetch 403) | https://www.crateandbarrel.com/marble-coasters-set-of-4/s450401 |
| 28 | West Elm, Mixed Marble & Brass Coaster Sets | marble, brass | sets | "from $49.50" up to $99 | — | snippet | https://www.westelm.com/products/mixed-marble-coasters-set-of-4-e2338/ |
| 29 | Home Depot, Creative Home natural white marble | marble, 4 in | 4 | $15.83 | [$3.96] | snippet | https://www.homedepot.com/p/Creative-Home-4-in-Natural-White-Marble-Coasters-Set-of-4-74721/313625280 |
| 30 | MoMA Design Store, Geo Stacking Coasters | silicone | 6 | $19.95 non-member (from $30), $17.96 member; clearance, final sale | [$3.33] | snippet (fetch 403) | https://store.moma.org/products/geo-stacking-coasters-primary |
| 31 | Kohl's, set of 8 round ceramic, geometric, holder, cork | ceramic, 4 in | 8 + holder | $20.99 | [$2.62] | snippet | https://mobile.kohls.com/product/prd-6148585/set-of-8-round-ceramic-coasters-for-drinks-with-holder-and-cork-base-geometric-design-4-inches.jsp?prdPV=48 |
| 32 | Herrschners, hexagon acrylic coasters & holder | acrylic | 4 + holder | $19.98 | [$5.00] | snippet | https://herrschners.com/herrschners-hexagon-acrylic-coasters-holder-set-accessory/ |
| 33 | Faire, CounterArt/Thirstystone "Geometric Tiles" 4-pack | absorbent stone, 4 in sq, cork | 4 | MSRP $17.00 (wholesale price hidden) | [$4.25] | snippet | https://www.faire.com/product/p_cnrbqa2hat |
| 34 | V&A shop, William De Morgan coaster (single) | not stated | 1 | £3 | £3 | snippet | https://www.vam.ac.uk/shop/162236.html |
| 35 | Anthropologie, Alessandra marble coaster (single) | marble | 1 | $8 | $8 | snippet | https://www.anthropologie.com/anthrohome/shop/alessandra-marble-coaster2 |
| 36 | Stirabout Studio, handmade ceramic coasters | hand-painted ceramic, cork | 2 | $38.00 | [$19.00] | snippet | https://www.stiraboutstudio.com/products/handmade-ceramic-coasters-set-of-2 |
| 37 | eBay, handmade Greek ceramic set | ceramic | 6 | $27.00, marked down from $45.00 | [$4.50] | snippet | https://www.ebay.com/b/Handmade-Ceramic-Coasters/36026/bn_81105005 |
| 38 | eBay, handmade Turkish Iznik-style set, open box | ceramic | 8 | $38.95 or best offer, plus shipping | [$4.87] | snippet | same eBay category page |

---

## Q2. Set sizes, and how price per coaster falls with set size

### 2a. Same seller, several set sizes (the only clean evidence of the curve)

| Seller | Material | 1 | 2 | 4 | 6 | Seen | URL |
|---|---|---|---|---|---|---|---|
| MAD Made Creations, "Custom 3D Printed Coasters" | **PLA, ~12 cm, layered 3D texture, black/white** | **$4.99** | **$7.99 [$4.00 ea, −20%]** | **$14.99 [$3.75 ea, −25% vs single]** | — | fetched (Squarespace product JSON, variant prices) | https://www.madmadecreations.com/shop/p/custom-3d-printed-coasters |
| Zsuzsanna Horvath, MOIRÉ | birch plywood | — | — | DKK 240 [60 ea] (painted black) | DKK 295 [49.17 ea, −18%] (natural) | fetched | rows 17–18 above |
| Heart of Anatolia | Turkish ceramic | — | — | $14.70–$19.60 [$3.68–$4.90 ea] | $19.50–$34.80 sale [$3.25–$5.80 ea] | fetched | row 20–21 above |

Caveats: the Zsuzsanna pair differs in finish (painted vs natural), so part of the drop may be the
paint. Heart of Anatolia's 4s and 6s are different designs, and its 6s are on sale, so it shows
only that the bands overlap. That leaves **one** seller (MAD Made, fetched) with a clean
same-product curve, and it is a 3D-printed PLA coaster.

### 2b. Set sizes seen across all physical-coaster listings in this file

Counting each listing once (Fantastic Plastics' 13 designs count as one), over the physical
listings in Q1 and Q4 whose set size is stated:

| Set size | Listings | Notes |
|---|---|---|
| Single | 7 (MAD Made; V&A; Anthropologie; Etsy ×3 singles in Q4; 3DPrint.com 2015 Meteor) | singles exist mostly as an add-on option or as premium pieces |
| 2 | 2 (MAD Made; Stirabout Studio, row 36) | rare |
| 4 | about 40 rows (by far the most common; museum shops, Fantastic Plastics, Etsy 3D-printed, marble retailers) | the default unit everywhere I looked |
| 5 | 2 sold (rows 40, 55), plus "5 patterns" free model files on MakerWorld/Printables | appears with "one of each pattern" sets |
| 6 | about 10 (rows 5, 6, 18, 21 [3 listings], 30, 37, 47, 54, 59) | second most common |
| 8 | 3 (rows 31, 38, 63) | rare; at the low end per coaster ($2.62–$4.87) |

These counts are over the set I collected, not the market. Listybox (a tool vendor, no stated
method, fetched) advises "sets of 4 or 6 for a higher average order value"
(https://listybox.com/niche/coasters/).

---

## Q3. Bulk and wholesale price breaks (where published)

| Source | What | Break | Seen | URL |
|---|---|---|---|---|
| Faire blog / help (wholesale marketplace) | wholesale price convention for brands | "wholesale price … is 50% of the retail price" (keystone); retailer margin target 50% / 2× wholesale; first-order minimum recommended $100–$150 (UK: under £300); price parity: Faire wholesale and MSRP must be same or lower than other channels | snippet (blog fetch 403) | https://www.faire.com/blog/selling/wholesale-basics-for-brands-makers-and-artists/ ; https://www.faire.com/support/articles/360019040531 |
| Faire coaster listings | brand-set minimums on coaster sets | GP Originals sea-turtle 4-set: MSRP $18, $100 minimum; Wolfum Studio set of 4: MSRP $34, $200 minimum; wholesale prices hidden behind retailer login | snippet | https://www.faire.com/product/p_cnrbqa2hat (and other Faire product pages in the search) |
| Contrado, personalized ceramic coasters | wholesale and pack sizes | "From $29.95 (was $36.95)"; pack sizes 1, 2, 4, 6, 8, 10, 12 (per-pack prices not shown); Wholesale "Up to 20%"; bulk = custom quote | fetched | https://www.contrado.com/personalized-ceramic-coasters |
| officesigncompany, full-color glass coasters | quantity discount | "Buy 3 – 5 and get 10% off" (sets of 3 or 6) | snippet | https://www.officesigncompany.com/full-color-personalized-glass-coasters/ |
| eBay, cork personalized coasters | quantity discount | "Buy 4 or more for 10.0 each" against US$12.50 base (−20%) | snippet | https://www.ebay.com/itm/156788273763 |
| ArtistryBazaar | handmade coasters "at wholesale prices" | no volume percentage published; only a sign-up code | snippet | https://www.artistrybazaar.com/product-category/coasters |
| Sticker Mule, custom coasters (60 pt pulp board, 3.7 in) | promo printing | snippet: "$1.30 / coaster", "save 32% when you add 50 coasters"; fetched page showed tiers 50 … 10,000 but the prices are drawn by script and did not load | snippet (prices); fetched (tiers only) | https://www.stickermule.com/products/custom-coasters |
| 4over4, wedding / drink coasters | promo printing | "$10.98 for a set of 10"; "$1.10 per print down to 97.8¢ at volume" | snippet (fetched page held only menus) | https://www.4over4.com/product/wedding-drink-coasters |
| sense2 (promo cork, round) | promo printing | min 250, $160 setup; $1.98 @ 250, $1.13 @ 5,000, $0.99 @ 50,000 | snippet | https://www.sense2.com/product/16306 |
| sense2 (glass, set of 4, full colour) | promo | min 100; $17.12 @ 100 down to $10.01 @ 50,000+ (per set) | snippet | https://static.sense2.com/product/16462 |
| fluidbranding (UK foam) | promo | MOQ 250; £0.59 @ 250 to £0.48 @ 5,000; £40 setup | snippet | https://www.fluidbranding.com/foam-tuff-coasters-1287841947.html |

**3D-printed sellers with published bulk tiers: none of the 11 3D-printed shops/listings in Q4
whose pages or snippets I read.** MAD Made invites "company logos" by checkout note with no price.
The promotional-printing tiers (paper, cork, foam, glass) are a different product made on presses
with a setup fee; their curve does not transfer to a printer-hours product, because their unit
cost falls with run length and ours is roughly flat per coaster (see design notes).

---

## Q4. Direct competitors: 3D-printed coasters for sale (physical, not files)

### 4a. Islamic / Arabic / Moroccan, 3D printed

| # | Listing | Set | Listed price | Per coaster | Seen | URL |
|---|---|---|---|---|---|---|
| 40 | Etsy, "Islamic Coaster Set of 5 \| Arabic Calligraphy Decor \| … \| 3D Printed" (98 reviews in snippet) | 5 | $35.00, free shipping | [$7.00] | snippet | https://www.etsy.com/market/islamic_coasters |
| 41 | Etsy, "Geometric Coasters \| Ramadan Decor \| Islamic Moroccan Pattern \| 3D Printed Luxury Table Decor" (72 reviews) | not stated; snippet's summary mentions six round coasters | $23.26 (US); €23.95 on Etsy France, free shipping | [~$3.88 if 6] | snippet | https://www.etsy.com/fr/market/moroccan_coasters |
| 42 | Etsy, "Palestine Kufic Calligraphy Coaster Set", "Customizable Upon Request" | not stated | $25.00, free shipping | — | snippet | https://www.etsy.com/market/3d_printed_islamic_decor |
| 43 | Etsy, "Arabic Coffee Coasters Set … 3D Printed" | not stated | $18.99 | — | snippet | https://www.etsy.com/market/arabic_coasters |
| 44 | Etsy, "Moroccan Geometric Coasters, Sage Green & Cream Islamic Tile Design, 3D Printed Alhambra Art" | 4 per snippet | $7.00 (low enough that it may be a file or a single; not resolved) | [$1.75?] | snippet | https://www.etsy.com/market/islamic_3d_prints |

No Islamic-pattern 3D-printed coaster seller with a fetchable shop turned up in the searches I ran
(none of the 5 listings above could be opened).

### 4b. Geometric / decorative 3D-printed coasters

| # | Seller / listing | Material, size | Set | Listed price | Per coaster | Seen | URL |
|---|---|---|---|---|---|---|---|
| 45 | Fantastic Plastics Jax, 13 designs incl. "Geometric Flower of Life", "Genesis Star", "Honeycomb", "Mandala OM" | PLA, two colors (bottom + top) from 15+ | 4 + free holder | **$20.97** (12 designs); **$22.97** (Mandala OM); no compare-at; custom color free | [$5.24 / $5.74] | fetched (collection + products JSON) | https://fantasticplasticsjax.com/collections/3d-printed-drink-coasters |
| 46 | MAD Made Creations, custom 3D printed coasters | PLA, ~12 cm, black/white only | 1 / 2 / 4 | **$4.99 / $7.99 / $14.99** | [$4.99 / $4.00 / $3.75] | fetched | https://www.madmadecreations.com/shop/p/custom-3d-printed-coasters |
| 47 | Man Crafted Shop, "6 Drink Coaster With Holder Set" | 3D print, 4 in | 6 + holder | **$20.00** | [$3.33] | fetched (product JSON) | https://www.mancraftedshop.com/products/blank-drink-coaster-set-3d-printed-model |
| 48 | The Chemist Tree, "Geometric Shapes Coaster Set" (Platonic solids) | PETG + cork, 3.75 in sq | 4 | **$35.00** (fetched); a search snippet said $26 | [$8.75] | fetched | https://chemisttree.com/products/geometric-shapes-coaster-set |
| 49 | Micro3DTechlab via Etsy, "Geometrix Meteor" (3DPrint.com article, **May 2015**) | ABS / PLA | 1 | $28 per coaster | $28 | fetched (article) | https://3dprint.com/62529/3d-printed-coasters/ |
| 50 | Sinister Style, "Organic Cell Coaster Set" | PLA | 4 | $14.00 ("98 in stock" and "Sold out" both shown) | [$3.50] | snippet (fetch SSL error) | https://sinisterstyle.shop/products/modern-geometric-coaster-set-3d-printed-pla-drink-coasters-copy |
| 51 | Terrain Objects, "Unique Drink Coasters … Set of 4 \| PLA" | PLA, 3.5 in, holder | 4 + holder | Regular price $33.20, sold out | [$8.30] | snippet (fetched page did not load the price) | https://terrainobjects.com/products/unique-drink-coasters-3d-print-unique-design-set-of-4-pla-eco-friendly-minimal-design-spill-resistant |
| 52 | Coqui Engineering, custom set of 4, cork + holder | 3D print | 4 + holder | 73,00 PLN, sold out | [18.25 PLN] | snippet (JSON 401) | https://coquiengineering.net/products/custom-3d-printed-drink-coaster-set-of-4 |
| 53 | Etsy, "Geometric Coasters, Set of 4, Modern Design 3D Printed Custom Color options 4in Coaster with holder tray" (94–96 reviews) | 4 in | 4 + tray | **$26.39 sale, from $32.99 (20% off)**, free shipping | [$6.60 sale / $8.25] | snippet | https://www.etsy.com/market/3d_print_coaster |
| 54 | Etsy, "Geometric Coasters 6 pc with Holder \| Unique 3D Printed Housewarming Gift" | — | 6 + holder | $23.25 sale, from $31.00 (25% off), free shipping | [$3.88 / $5.17] | snippet | https://www.etsy.com/market/3d_print_coaster_holder |
| 55 | Etsy, "Forma Geo Coaster Set – … 5 Unique 3D Printed Drink Coasters" | black & white | 5 + holder | $22.40 sale, from $28.00 (20% off) | [$4.48 / $5.60] | snippet | https://www.etsy.com/market/3d_printed_coasters_set_with_holder?explicit=1&guided_search=1 |
| 56 | Etsy, "Geometric Coaster Set with Holder – 3D Printed PLA" (100 reviews) | PLA | not stated | $14.12 sale from $17.64; later snapshot $14.61 from $18.26 | — | snippet | https://www.etsy.com/market/3d_printed_coasters |
| 57 | Etsy, "3D Printed Geometric Drink Coasters, Set of 4 With Holder Base" (two-color PLA) | PLA two-color | 4 + base | $12.00, "only 8 left" | [$3.00] | snippet | https://www.etsy.com/listing/1616221109/3d-printed-geometric-drink-coasters-set |
| 58 | Etsy, set of 4 unique PLA drink coasters with holder | PLA | 4 + holder | $20.00 | [$5.00] | snippet | https://www.etsy.com/market/3d_printed_coasters |
| 59 | Etsy, "modern wavy" set of 6 with holder | — | 6 + holder | $35.00, free shipping | [$5.83] | snippet | https://www.etsy.com/market/3d_printed_coasters |
| 60 | Etsy, single geometric mountain coaster | — | 1 | $3.75 sale from $5.00 | $3.75 | snippet | https://www.etsy.com/listing/1719836046/3d-printed-geometric-mountain-coaster |
| 61 | Etsy, single "modern 3D-printed circular-pattern coaster" | — | 1 | $20.00 | $20.00 | snippet | https://www.etsy.com/market/3d_print_coaster |
| 62 | Etsy, single geometric coaster | — | 1 | $12.00 | $12.00 | snippet | https://www.etsy.com/market/3d_print_coaster |
| 63 | Etsy, personalized logo coaster set 8-pack with holder | — | 8 + holder | $26.99 | [$3.37] | snippet | https://www.etsy.com/market/custom_3d_printed_coasters |
| 64 | Etsy (tinytinker3d), personalized set of 4 with custom holder | — | 4 + holder | $11.99, free US shipping | [$3.00] | snippet | https://tinytinker3d.patternbyetsy.com/listing/1902790381/coasters-set-of-4-custom-holder-unique |
| 65 | Amazon, "3D Printed ST Logo Drink Coasters with Holder, 3.5 inch, Set of 4" | 3.5 in | 4 + holder | $29.98 | [$7.50] | snippet | https://www.amazon.com/Printed-Drink-Coasters-Holder-Black/dp/B0DSV8RZ4Q |
| 66 | Amazon, "Horse and Rider Coaster set of 4 with holder" (3D printed + vinyl) | 3.5 in | 4 + holder | $9.99 (snapshot may be old) | [$2.50] | snippet | https://www.amazon.com/Horse-Rider-Coaster-set-holder/dp/B0DH671FT3 |
| 67 | eBay shop page: Milwaukee 4 + holder $11.99 (+$6.07 delivery); Honeycomb 4 + holder $12.99; Pumpkin 4-pack $14.99 | — | 4 | $11.99 / $12.99 / $14.99 | [$3.00 / $3.25 / $3.75] | snippet | https://www.ebay.com/shop/3d-printed-coasters?_nkw=3d+printed+coasters |
| 68 | eBay, NFL team coaster sets (Detroit Lions, Tennessee Titans), 3D printed | — | 4 | $19.99 each listing, 1 sold on one | [$5.00] | snippet | https://www.ebay.com/itm/155914403011 |
| 69 | eBay, "Recycled 3D Print Coasters – Set of 4" | recycled filament | 4 | $55.00 or best offer | [$13.75] | snippet | https://www.ebay.com/itm/167243841822 |

### 4c. Summary over the 3D-printed physical listings with a stated set size

Using each listing's shown price (sale price where one was shown), divided per coaster, over
rows 40, 45–48, 50–51, 53–55, 57–59, 63–68 (21 listings; licensed and personalized included;
the 2015 single, the three singles, row 69's best-offer outlier and the unresolved rows 41–44, 52,
56 left out):

- per coaster, low to high: 2.50, 3.00, 3.00, 3.00, 3.25, 3.33, 3.37, 3.50, 3.75, 3.75, 3.88,
  4.48, 5.00, 5.00, 5.24, 5.83, 6.60, 7.00, 7.50, 8.30, 8.75
- **median $3.88 per coaster; middle half about $3.30 – $6.20; range $2.50 – $8.75**
- only 4 of the 21 rest on a fetched page (rows 45, 46, 47, 48); the other 17 are snippets.
- the 4 fetched alone: $3.33, $3.75, $5.24, $8.75 per coaster — the same spread.
- as a set of 4 (×4): **median about $15.50; middle half about $13 – $25.**

---

## Q5. What buyers pay extra for

| Extra | What the listings show | Count | Seen | Source |
|---|---|---|---|---|
| Holder / stand | Bundled at no stated extra in 13/13 Fantastic Plastics designs ("free holder") and in most Etsy 3D-printed sets above (rows 53–59, 63–66). Sold alone: RDM Designs holder $5.00 (holds 5–6); an Etsy coaster rack $6.74 sale from $8.99 | 2 standalone prices | fetched (FPJ); snippet (RDM, Etsy rack) | https://store.rdm-designs.com/product/drink-coaster-holder/ ; https://www.etsy.com/market/3d_printed_coasters |
| Gift box | Included in the price, never a separate line, in every listing that mentions one: Aga Khan (embossed box, $145), Zahra marble ("box ready for gift giving"), Lasaris (gift box / recycled presentation box), Puttyprint ("free gift box"). The one paid-looking case (4imprint executive set, "set-up charge: add $65") does not say what the fee covers | 0 of 5 listings that mention a box charge separately for it | fetched (Aga Khan, Zahra); snippet (Lasaris, Puttyprint, 4imprint) | rows 2, 3, 22, 26; https://www.4imprint.ca/product/C119945/Executive-Coaster-Set |
| Custom color | Free at Fantastic Plastics ("15+ colors", top and bottom color chosen); free in the Etsy "Custom Color options" set (row 53); MAD Made black/white only | 2 free, 0 charged | fetched (FPJ, MAD Made); snippet (Etsy) | rows 45, 46, 53 |
| Personalization | Lifetime Leather: plain included, "Large center letter" **+$2.00**, fire brand stamp free, custom stamp "contact for pricing". 3D-printed personalized sets in Q4 (rows 63, 64) sit at the low end of the band, not above it. Atomm and Listybox (blogs, no data) say personalized coasters sell best | 1 priced upcharge | fetched (Lifetime); snippet (rows 63–64; Atomm) | https://lifetimeleather.com/products/leather-hexagon-coaster-set-1 ; https://www.atomm.com/blog/2402-coaster-ideas-to-sell-on-etsy |
| Museum / provenance | Museum shops price far above makers for similar material: Aga Khan maple set $145 vs laser-cut oak sets $23–$28; Leighton House MDF £24 vs Etsy/Redbubble MDF $15–$18 | 2 museum shops | fetched | rows 1, 2 |
| Theme (Islamic / Ramadan) | Islamic-themed 3D-printed sets in Q4a list at $19–$35 per set, against a generic 3D-printed median of ~$15.50 per 4. Weak: 4 snippet-only listings, set sizes mostly unknown | 4 | snippet | rows 40–43 |
| Free shipping | Most Etsy rows above say "FREE shipping" in the price; eBay rows add $6.07 delivery on a $11.99–$12.99 set | — | snippet | rows 53–59, 67 |

---

## Sources that returned nothing usable

- Etsy search, market and listing pages: HTTP 403 to WebFetch (every attempt).
- eBay item pages, Amazon product page (500), Faire blog, Redbubble (403 / timeout), Crate &
  Barrel, MoMA store (403), Diwan Egypt (403), Sinister Style and Lasaris (TLS handshake failure),
  Coqui Engineering JSON (401), Crystal Bridges and SFMOMA products (404), Aga Khan second set (404).
- Chrome extension (to read Etsy in a real browser): not connected in this session.
- Digital STL listings (Thangs $3.00 file, Cults $5.89, Etsy files $1.22–$8.01) were seen and left
  out of every table: they are files, not coasters.

## Prior research in this repo

`docs/research/2026-10-04-coaster-pricing.md` (and its -a / -b inputs) is an earlier pricing
round that read Etsy in a real Chrome session. I read only its header to match the provenance
format, not its findings, to keep this pass independent; the checker can compare.
