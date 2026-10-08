---
date: 2026-10-08
produced-by: researcher B (Claude subagent, Opus 5.5), one of two independent researchers on the same question; the other researcher's files and branch were not read. Method — WebSearch (standard and extended) for listings, WebFetch for every page that would load. Etsy, eBay, Redbubble, Amazon, Faire and one Shopify maker shop refused WebFetch (HTTP 403, 400 or 500); the Chrome extension was not connected, so those marketplaces are known only from search-result snippets. No bot check was worked around.
feeds:
  - docs/design/coaster/order-driven-lab-design.md §9.7 pricing
---

# Coaster market prices: raw findings (research B)

Design notes built from this file: [coaster-market-pricing-b.md](coaster-market-pricing-b.md).
It feeds [order-driven-lab-design §9.7](../design/coaster/order-driven-lab-design.md#97-pricing-ideas-the-ways-to-set-a-price-side-by-side).

**How to read the tables.**

- **Seen** says how the number was read. **fetched** means WebFetch loaded the page and the
  number came off it. **snippet** means the number came only from a search-result summary;
  the page itself was not opened (usually because the site refused the fetch). A snippet is a
  third-hand reading — the search tool's summary of a crawled page — so treat it as weaker.
- Prices are copied with their wording: "sale from", "was", "from", "sold out". A price with no
  currency code is written as the page showed it.
- **Per coaster** is my own division of the set price by the set size; it is not on the page.
- Where a fetched page and an earlier snippet disagreed, both are written down. This happened
  four times (Leighton House, Chemist Tree, Islamic Wall Art Store, Qstomize), which is a
  warning about the snippet-only rows.
- Prices are listed, not sold. None of these pages shows what a buyer actually paid; Etsy
  review counts in a few snippets are the only hint of sales volume.

---

## Q1. Listed prices for comparable coasters

### 1a. 3D-printed coasters (physical, not files)

| # | Seller / listing | Where | Set | Price as shown | Per coaster | Size, material, extras | Seen | URL |
|---|---|---|---|---|---|---|---|---|
| 1 | Tiny Tinker 3D, "Coasters (Set of 4) Custom Holder … Personalized 3D Printed" | Etsy (Pattern site) | 4 + holder | $11.99, free US shipping | $3.00 | ~4 in; color choice for coasters and holder; name on holder; "dishwasher safe" | snippet (fetch: HTTP 400) | https://tinytinker3d.patternbyetsy.com/listing/1902790381/coasters-set-of-4-custom-holder-unique |
| 2 | BHCustomGoods, "3D Printed Geometric Drink Coasters, Set of 4 With Holder Base" | Etsy | 4 + holder | $12.00 ("8 left") | $3.00 | PLA, two-color geometric, inside color choice | snippet (fetch: 403) | https://www.etsy.com/listing/1616221109/3d-printed-geometric-drink-coasters-set |
| 3 | "Custom 3D Printed Coasters … (4-pack With Holder)" | Etsy | 4 + holder | $15.00 | $3.75 | PLA | snippet | https://www.etsy.com/listing/1660129703/custom-3d-printed-coasters-unleash-your |
| 4 | "Hexagonal 3D Printed Coasters, Minimalist PLA Set of 4" | Etsy | 4 | $17.25 | $4.31 | PLA; holder not mentioned | snippet | https://www.etsy.com/market/3d_printed_coasters_set_of_4 |
| 5 | "Geometric Coaster Set with Holder – 3D Printed PLA" | Etsy | not stated | $18.37 | — | PLA, holder | snippet | https://www.etsy.com/market/3d_printed_coasters_set_of_4 |
| 6 | BespokeAandD, "3D Printed Coasters Set of 4: Unique PLA Drink Coasters With Holder" | Etsy | 4 + holder | $20.00 (US market page); AU$30.03 (AU page) | $5.00 | PLA; ships from Pennsylvania | snippet | https://www.etsy.com/au/listing/1768147884/3d-printed-coasters-set-of-4-unique-pla |
| 7 | "Geometric Coasters, Set of 4, Modern Design 3D Printed" | Etsy | 4 + holder tray | $26.39 sale, from $32.99; free shipping | $6.60 sale / $8.25 list | 4 in; custom colors | snippet | https://www.etsy.com/market/3d_printed_coasters_set_of_4 |
| 8 | RaesCreationsxo, honeycomb hexagon set with stand | Etsy | 4 + stand | $30.00 | $7.50 | "cold drinks only" | snippet | https://www.etsy.com/listing/1061270018/3d-printed-honey-comb-hexagon-coater-set |
| 9 | Multicolor PLA Christmas set | Etsy | 4 | $30.00 sale, from $40.00 | $7.50 sale / $10.00 list | PLA, multicolor | snippet | https://www.etsy.com/market/3d_printed_coasters_set_of_4 |
| 10 | "Minimalist 3D Printed Coaster Set: Eco-friendly PLA With Caddy" | Etsy | 4 + caddy | $39.00 | $9.75 | PLA | snippet | https://www.etsy.com/listing/1341392654/minimalist-3d-printed-coaster-set-eco |
| 11 | Multiverse3DForge, geometric set with holder | Etsy | 6 + holder | $23.25 sale, from $31.00 (25% off); free shipping, ships from NJ | $3.88 sale / $5.17 list | geometric; a Kumiko-pattern hexagon listing showed the same $23.25 | snippet | https://www.etsy.com/market/3d_print_coaster |
| 12 | multiverse3dforge, "3D Printed Kumiko Coaster Set with Holder \| Japanese Geometric Pattern" | eBay | set + holder (size not in snippet) | $31.00 | — | geometric (Kumiko) | snippet (fetch: 410) | https://www.ebay.com/str/multiverse3dforge |
| 13 | "Modern Wavy Coaster Set of 6 with Holder" | Etsy | 6 + holder | $35.00 | $5.83 | — | snippet | https://www.etsy.com/market/3d_printed_coasters |
| 14 | "Mario Coin Coaster Set – 6 Coasters with Warp Pipe Holder" | Etsy | 6 + holder | $18.00 | $3.00 | licensed-character design | snippet | https://www.etsy.com/market/3d_printed_custom_coasters_with_holder |
| 15 | "Personalized Logo Coaster Set: 3D Printed Business Gift, 8-pack With Holder" | Etsy | 8 + holder | $26.99 | $3.37 | ~4 in; logo | snippet | https://www.etsy.com/listing/1876538697/personalized-logo-coaster-set-3d-printed |
| 16 | Business logo coasters | Etsy | 2 | $8.80 sale, from $11.00 | $4.40 sale / $5.50 list | logo | snippet | https://www.etsy.com/market/custom_coasters_3d_printed |
| 17 | Custom car coasters | Etsy | 4 | $16.95 | $4.24 | — | snippet | https://www.etsy.com/market/custom_coasters_3d_printed |
| 18 | Adeptus Craftus, "Custom 3d Printed Coasters (set of 2)" | own shop (Wix) | 2 | $12.99 | $6.50 | ~4 in, 1/4 in thick, PLA; color choice; custom logo upload, no adder shown | **fetched** | https://www.adeptuscraftus.com/product-page/custom-3d-printed-coasters-set-of-2 |
| 19 | Boyd's 3D Studio, "Stackable Coaster" (5 colors) | own shop (Shopify) | unit not stated | $8.00, labelled "Sale", no original price | $8.00 if per coaster | "mix and match colors" to build a set | **fetched** (redirected from boydscustomfab.com) | https://boyds3dstudio.com/collections/3d-printed-coasters |
| 20 | MAD Made Creations, custom 3D printed coasters | eBay | 1, 2 or 4 | about $4.99 base | — | 4.72 in (120 mm), PLA, hand wash only | snippet (fetch: 403) | https://www.ebay.com/itm/205585957330 |
| 21 | "Custom 3D Printed Deadpool Coasters - Set of 4" | eBay | 4 | US $12.50 + $8.75 shipping | $3.13 + shipping | licensed-character design | snippet | https://www.ebay.de/itm/326335657321 |
| 22 | "Luxury-Inspired Red Round Designer Coasters – Set of 4 – Premium 3D Printed Gift" | eBay (business seller) | 4 | £20.00 | £5.00 | — | snippet | https://www.ebay.de/itm/396877049054 |
| 23 | "Modern 3D-Printed Coaster Set" | eBay | 6 | US $19.48 (listing ~279 days old) | $3.25 | square and round, gray and pink | snippet | https://www.ebay.com/itm/326468784307 |
| 24 | Chemist Tree, "Geometric Shapes Coaster Set" | own shop (Shopify) | 4 | $35.00 on the fetched page, no currency stated (a related product says "Prices in CAD"); the snippet said $26 | $8.75 | 3.75 × 3.75 × 0.125 in, **PETG** with cork base | **fetched** | https://chemisttree.com/products/geometric-shapes-coaster-set |
| 25 | Terrain Objects, "Unique Drink Coasters … Set of 4 PLA" | own shop | 4 + holder | $33.20, "sold out" (snippet); fetched page did not load the price | $8.30 | 3.5 in, PLA | snippet (fetch loaded no price) | https://terrainobjects.com/products/unique-drink-coasters-3d-print-unique-design-set-of-4-pla-eco-friendly-minimal-design-spill-resistant |
| 26 | Sendnodes Plant Shop, "3D Printed Hanging Coaster Set" | own shop (Shopify) | one set (pot + leaves) | $45.00, sold out, no discount | — | PLA; novelty plant design, not geometric | **fetched** | https://sendnodesplantshop.com/products/coasters |
| 27 | "3D Printed Coaster Set with Holder, Blue and Yellow, PLA, Modern Ribbed" | Amazon.in | 4 + holder | ₹250.00, M.R.P. ₹350 | ₹62.50 | PLA | snippet | https://www.amazon.in/Printed-Coaster-Material-Coasters-Included/dp/B0GHGQH8FV |
| 28 | "3D Printed Coaster" | Etsy | unit unclear | $5.59 sale, from $6.99 | — | — | snippet | https://www.etsy.com/listing/1254752996/3d-printed-coaster |

**Islamic or Arabic-themed 3D-printed listings** (the closest competitors to us):

| # | Listing | Where | Set | Price as shown | Per coaster | Notes | Seen | URL |
|---|---|---|---|---|---|---|---|---|
| 29 | "Islamic Coaster Set of 5 \| Arabic Calligraphy Decor \| … \| 3D Printed" | Etsy | 5 | $35.00, free shipping; (104) reviews in the snippet | $7.00 | calligraphy, not geometric | snippet | https://www.etsy.com/market/islamic_coasters |
| 30 | "Geometric Coasters \| Ramadan Decor \| Islamic Moroccan Pattern \| 3D Printed Luxury Table Decor" | Etsy | not stated | $23.26, free shipping; (99) reviews | — | the only Islamic **geometric** 3D-printed listing found | snippet | https://www.etsy.com/market/islamic_3d_prints |
| 31 | "Palestine Kufic Calligraphy Coaster Set - 3D Printed - Customizable Upon Request" | Etsy | not stated | $25.00, free shipping; (7) reviews | — | calligraphy | snippet | https://www.etsy.com/market/arabic_coasters |

Not found: none of the searches here turned up an Islamic-geometric 3D-printed coaster on Amazon,
eBay or an independent shop. MakerWorld, Printables, Thangs and Cults host free or paid **files**
for Islamic-pattern coasters (a Zellij Moroccan tile coaster by Dany Sánchez, a 12-pointed
Islamic star coaster, Sipek Design's "sacred geometry" coasters at $3.00 per file on Thangs), and
several carry commercial-use restrictions — those are design-file prices, not coaster prices.

### 1b. Islamic or geometric coasters in other materials

| # | Seller / listing | Where | Set | Price as shown | Per coaster | Size, material, extras | Seen | URL |
|---|---|---|---|---|---|---|---|---|
| 32 | Leighton House Museum, "Geometric Wooden Coaster Set Dark" (inspired by the Arab Hall) | museum shop (RBKC) | 4 | **£24.00** on the fetched page; a snippet showed £19.00 (perhaps another colorway or an older price) | £6.00 | **110 × 110 mm**, laser-cut 3 mm MDF, wood oil, cork back; no box mentioned | **fetched** | https://museumshop.rbkc.gov.uk/products/geometric-wooden-coaster-set-dark |
| 33 | Aga Khan Museum, "Islamic Coasters Set (Circle) - 10 Pointed Star (Alhambra Palace)" | museum shop | 4 | $145.00, currency not named (the shop's selector offers CAD first) | $36.25 | 3.95 in, maple, glossy black acrylic, rubber feet; embossed gift box 5 × 7 in | **fetched** | https://shop.agakhanmuseum.org/products/rahim-bhimani-coaster-set-indian-rose-tree-wood-2 |
| 34 | With Aspin, "Zahra Marble Coaster Set with Islamic Geometric Metal Inlay" | own shop | 4 | $44.99, compare-at $49.99; "Sold Out" | $11.25 | marble with brass inlay, velvet lining, "Comes in a box ready for gift giving" | **fetched** | https://shop.withaspin.com/products/zahra-marble-coaster-set |
| 35 | Islamic Wall Art Store, "Modern Islamic Acrylic Coasters – Ramadan Table Decor" | own shop | 6 or 12 | set of 6: $44 (compare-at $59); set of 12: $54 (compare-at $72). A snippet had shown $29 / $36 | 6: $7.33 sale / $9.83 list; 12: $4.50 sale / $6.00 list | mirror acrylic, calligraphy cut-outs; no holder or box mentioned | **fetched** | https://islamicwallartstore.com/products/modern-islamic-acrylic-coasters-ramadan-table-decor |
| 36 | Lamisa, "Wooden Geometric Coasters" | own shop (UK) | 4 | £4.00, sold out | £1.00 | 10 × 10 cm wood; an outlier — maybe a clearance price | **fetched** | https://lamisa-uk.com/products/geometric-coasters |
| 37 | Redbubble, "Islamic Geometric Pattern … Coasters (Set of 4)" | print on demand | 4 | $15.41 | $3.85 | 9.5 cm MDF, gloss, cork back | snippet (fetch: 403) | https://www.redbubble.com/i/coasters/Islamic-Geometric-Pattern-Beauty-In-Every-Equation-Math-Formulas-Art-by-SplashTastic/182375689/43wr |
| 38 | Redbubble, "Modern Arabic Geometric Pattern" | print on demand | 4 | $18.13 | $4.53 | same MDF blank | snippet | https://www.redbubble.com/i/coasters/Modern-Arabic-Geometric-Pattern-Art-by-RashadSA/167998375/43wr |
| 39 | Redbubble, "Moroccan Pattern Rug Design" | print on demand | 4 | $14.12, from $16.62 (15% off) | $3.53 | same MDF blank | snippet | https://www.redbubble.com/i/coasters/Moroccan-Pattern-Rug-Design-by-SpaceBazaar/180613077/43wr |
| 40 | Zazzle, "Moroccan Zellige Pattern Geometric Coaster" | print on demand | 1 | $10.29 sale "per coaster", from $12.10 (15% savings) | $10.29 | 4.25 in sandstone, cork pad; no quantity tiers shown | **fetched** | https://www.zazzle.com/moroccan_zellige_pattern_geometric_coaster-256394148523227139 |
| 41 | Zazzle, "Alhambra Wall Tile #3" coaster | print on demand | 1 | $11.52 sale, from $12.80 | $11.52 | sandstone | snippet | https://www.zazzle.com/alhambra_wall_tile_3_coaster-174039838724880181 |
| 42 | Nestasia, "Zellij Art Framed Round Ceramic Coaster … Set of 4" | own shop (India) | 4 | ₹560 shown beside ₹890 ("37%"), sold out | ₹140 | 10 cm ceramic, cork underside | **fetched** | https://nestasia.in/products/lavender-ceramic-coaster-set-of-4 |
| 43 | World Market, "Terracotta Moroccan Tile Coasters 4 Pack" | chain store | 4 | page text: "Price reduced from $19.99 to" … "Price reduced from $13.98 to" (cut off); a snippet said $6.99 from $13.98 | ~$1.75–$3.50 | 4 in square terracotta, assorted designs | **fetched** (price wording incomplete) | https://www.worldmarket.com/p/terracotta-moroccan-tile-coasters-4-pack-545098.html |
| 44 | V&A shop, William De Morgan tile coaster | museum shop | 1 | £3 | £3 | 10 × 10 cm, melamine on eucalyptus board, cork back; floral design (De Morgan drew on Islamic tile traditions) | **fetched** | https://www.vam.ac.uk/shop/162237.html |
| 45 | Etsy, laser-engraved Arabesque wood set | Etsy | not stated | $41.00, free shipping | — | wood | snippet | https://www.etsy.com/market/islamic_coasters |
| 46 | Etsy, "Islamic Geometric Coaster Set of 5" | Etsy | 5 | $35.00; ~100 reviews | $7.00 | material not stated in snippet | snippet | https://www.etsy.com/market/islamic_coasters |
| 47 | Etsy, "SET of 6 Wood Coasters … Moorish Star" | Etsy | 6 (gift box) | $17.21 sale, from $21.51 | $2.87 sale / $3.59 list | wood, gift box | snippet | https://www.etsy.com/il-en/listing/924593166/set-of-6-wood-coasters-ramadan |
| 48 | Etsy UK, "Islamic Geometric Coasters Set of 4 \| Marble Effect … Moroccan Star" | Etsy | 4 | £14.99, from £17.98 | £3.75 | marble effect | snippet | https://www.etsy.com/uk/market/islamic_art_coasters |
| 49 | Etsy, set of 4 Islamic geometric with holder | Etsy | 4 + holder | €27.48 | €6.87 | — | snippet | https://www.etsy.com/market/ramadan_coasters |
| 50 | Etsy, six-piece Islamic Ramadan/Eid set | Etsy | 6 | $45.00, free shipping | $7.50 | wording + pattern | snippet | https://www.etsy.com/market/ramadan_coasters |
| 51 | Etsy, Rub el Hizb set | Etsy | not stated | CA$39.15 | — | — | snippet | https://www.etsy.com/market/islamic_coasters |
| 52 | Etsy, Andalusian (Alhambra) tile coasters | Etsy | unit unclear | $7.49 sale, from $9.99; ~113 reviews | — | ceramic | snippet | https://www.etsy.com/market/islamic_coasters |
| 53 | Diwan Egypt, "Geometric Inlay Coasters" | own shop (Egypt) | not stated | EGP 380, out of stock | — | wood inlaid with bone, copper, ebony | snippet (fetch: 403) | https://diwanegypt.com/product/geometric-inlay-coasters/ |
| 54 | Over the Moon, "Alhambra Linen Coasters in Green, Set of 6" (Los Encajeros) | own shop | 6 | $60 | $10.00 | linen, embroidered | **fetched** | https://overthemoon.com/products/alhambra-linen-coasters-set-of-6 |

### 1c. General decorative coasters used for set-size and premium reference

| # | Listing | Set | Price as shown | Per coaster | Seen | URL |
|---|---|---|---|---|---|---|
| 55 | Santa Barbara Company, "Laila Ceramic Tile Coaster Set" (Mexican tile, geometric-floral) | 1 / 2 / 4 | single $12; set of 2 $24; set of 4 $40 | $12 / $12 / $10 | **fetched** | https://www.santabarbaracompany.com/products/laila-coasters |
| 56 | Kemper Art Museum shop, "Multicolor Ceramic Coaster Set" (Brooklyn stoneware) | 4 | $60.00 | $15.00 | **fetched** | https://shop.kemperart.org/products/multicolor-ceramic-coaster-set |
| 57 | Thirstystone (CounterArt) "Geometric Tiles" 4-pack on Faire | 4 | MSRP $17.00 (wholesale not visible) | $4.25 | snippet (fetch: 403) | https://www.faire.com/product/p_cnrbqa2hat |
| 58 | Thirstystone single coasters on Walmart (e.g. "Mocha Lily") | 1 | about $8.50 | $8.50 | snippet | https://www.walmart.com/ip/46273301 |
| 59 | Wayfair sets with holder: stoneware 4 + holder $21.99; wood 4 + holder $16.99; leather 6 + holder $32.99 | 4, 4, 6 | as shown | $5.50 / $4.25 / $5.50 | snippet | https://www.wayfair.com/kitchen-tabletop/sb1/coaster-set-with-holder-coasters-c1806735-a8417~491506.html |

---

## Q2. Set sizes, and how the price per coaster falls with set size

### 2a. How often each set size appears

Counted over the physical-coaster rows above whose set size is stated.

| Set size | 3D-printed rows (1a, #1–#31) | Other-material rows (1b + 1c) | All |
|---|---|---|---|
| 1 (single) | 1 (#20 offers 1/2/4) | 4 (#40, #41, #44, #58; + #55, which also sells 2 and 4) | 5–6 |
| 2 | 2 (#16, #18) | 0 (+ #55 variant) | 2–3 |
| 4 | 15 (#1–#4, #6–#10, #17, #21, #22, #24, #25, #27) | 15 (#32–#34, #36–#39, #42, #43, #48, #49, #56, #57, two in #59; + #55 variant) | 30 |
| 5 | 1 (#29) | 1 (#46) | 2 |
| 6 | 4 (#11, #13, #14, #23) | 5 (#35, #47, #50, #54, #59 leather) | 9 |
| 8 | 1 (#15) | 0 | 1 |
| 12 | 0 | 1 (#35) | 1 |

Set of 4 is the default in both groups: 30 rows, against about 21 for every other size
combined. Set of 6 is second (9 rows). Singles appear mainly at print-on-demand (Zazzle) and tile-coaster shops; among the
3D-printed rows here only one offers a single.

### 2b. Price per coaster at different set sizes — the same seller

| Seller | Sizes | Per coaster | Drop | Rows it rests on | Seen |
|---|---|---|---|---|---|
| Santa Barbara Co. (ceramic tile) | 1 → 2 → 4 | $12 → $12 → $10 | 0% at 2, −17% at 4 | 1 | fetched |
| Islamic Wall Art Store (mirror acrylic) | 6 → 12 | $7.33 → $4.50 (sale); $9.83 → $6.00 (compare-at) | −39% at 12 | 1 | fetched |
| Thirstystone (stone, different designs) | 1 vs 4 | ~$8.50 vs $4.25 (MSRP) | about −50%, across different designs and stores | 2 | snippet |
| MAD Made Creations (3D printed) | 1 / 2 / 4 | "about $4.99 base"; variant prices not shown | unknown | 1 | snippet |

### 2c. Across sellers: 3D-printed sets by size (per coaster)

| Set size | Per-coaster values (3D-printed rows, list or sale as shown) | Count | Median |
|---|---|---|---|
| 2 | $4.40 (sale), $6.50 | 2 | ~$5.45 |
| 4 | $3.00, $3.00, $3.13 (+ship), $3.75, $4.24, $4.31, $5.00, ~$6.25 (£5), $6.60 (sale), $7.50, $7.50 (sale), $8.30, $8.75, $9.75 | 14 | ~$5.60 (set price median ~$22.50; range $11.99–$39.00) |
| 5 | $7.00 (Islamic calligraphy) | 1 | — |
| 6 | $3.00, $3.25, $3.88 (sale), $5.83 | 4 | ~$3.6 |
| 8 | $3.37 | 1 | — |

(£5 converted at roughly 1.25 USD/GBP only for ordering; the Amazon.in row is left out of the median.)

---

## Q3. Bulk and wholesale price breaks

| # | Source | What | Tiers as shown | Drop, smallest → largest tier | Seen | URL |
|---|---|---|---|---|---|---|
| B1 | Qstomize, custom coasters | pulpboard / cork / leather / sandstone, 4 in, min 50 | 50–99: $3.95; 100–249: $2.95; 250+: $2.25 per piece; "Setup, art, decoration and tracked shipping bundled" (but also "Shipping quoted at checkout"). A snippet had shown $12.99 → $8.83 | −25% at 100, −43% at 250 | **fetched** | https://qstomize.com/products/custom-coasters |
| B2 | Qstomize, ceramic coaster set | "Four ceramic coasters with cork backing", min 50 | 50–99: $6.50; 100–249: $5.50; 250–499: $4.75; 500+: $4.10 per "pc" (whether a pc is one coaster or four is unclear). A snippet had shown $12.00 / $10.50 / $9.25 | −15% at 100, −27% at 250, −37% at 500 | **fetched** | https://qstomize.com/products/coaster-set-ceramic |
| B3 | Promotional Product Inc., 4 in pulpboard | min 100 | $1.76 each at 100, + $90 setup; reorders no setup | — | snippet | https://www.promotionalproductinc.com/4-square-heavy-weight-125-pt-pulpboard-coaster-w-4-color-process-printing-cmyk |
| B4 | Sense2, glass coaster set of four | min 100 | $17.12 at 100 → $10.01 at 50,000; $70 setup (a second Sense2 page: $12.91 at 100, $52.77 setup) | −42% | snippet | https://static.sense2.com/product/16462 |
| B5 | Fluid Branding, acrylic | — | £2.70 at 50 → £1.17 at 10,000; £25 setup | −57% | snippet | https://fluidbranding.com/bespoke-shaped-acrylic-coaster-12658252.html |
| B6 | LamPro, blotter paper | — | $0.42–$0.38 at 250–500, falling at higher counts | — | snippet | https://www.lampro.com/category/Coasters |
| B7 | Etsy, "Personalized Wedding Coasters: 3D Printed Plastic, Custom Names & Date" | 4 in, 3D printed | "starting at $6.00 each"; "discounts available for bulk orders" — tiers not published | — | snippet (fetch: 403) | https://www.etsy.com/listing/4357221914/personalized-wedding-coasters-3d-printed |
| B8 | Wholesale Coaster Holders | metal holder alone | $1.75 sale, from $2.75; coaster + holder bundle $3.99, from $4.99 | — | snippet | https://coasterholders.com/product-tag/coasters-with-holder/ |
| B9 | Faire (wholesale marketplace): Dock 6 Pottery single coaster | 1 | MSRP $11.00; description gives "$5.50 ea" | 50% of MSRP | snippet (fetch: 403) | https://faire.com/product/p_59w9mf6mo2?signUp=1 |
| B10 | Keystone convention (retail ≈ 2 × wholesale), as described by third-party glossaries; the search summary attributed "about 50% margin" to Faire's own guidance, but the Faire article refused the fetch | — | — | — | snippet only | https://femfounded.org/reference/keystone-pricing/ ; https://faire.com/support/articles/360019040531 |

None of the 32 3D-printed listings looked at here (#1–#31 and B7) shows a quantity-tier table —
though only four of them (#18, #19, #24, #26) were read from the page itself; the one that
mentions bulk (B7) says to ask. Every published tier table found is for printed-surface blanks
(paper, pulpboard, glass, acrylic, ceramic), not for 3D-printed coasters — so the *shape* of
those curves transfers only as far as our cost per coaster actually falls with quantity.

---

## Q4. Direct competitors: 3D-printed geometric coasters

| Competitor | What | Price | Per coaster | Seen |
|---|---|---|---|---|
| Etsy listing #30 ("Islamic Moroccan Pattern, 3D Printed Luxury Table Decor") | Islamic geometric, 3D printed | $23.26, free shipping, 99 reviews | set size not in snippet | snippet |
| Etsy listing #29 (Islamic set of 5, calligraphy, 3D printed) | Islamic calligraphy | $35.00, free shipping, 104 reviews | $7.00 | snippet |
| Etsy listing #31 (Palestine Kufic, 3D printed) | calligraphy | $25.00, free shipping | not stated | snippet |
| BHCustomGoods (Etsy #2) | geometric, two-color PLA, 4 + holder | $12.00 | $3.00 | snippet |
| Multiverse3DForge (Etsy #11, eBay #12) | geometric / Kumiko, 6 + holder | $23.25 sale from $31.00 (Etsy); $31.00 (eBay) | $3.88–$5.17 | snippet |
| Etsy #7 "Geometric Coasters, Set of 4" | geometric, 4 + tray | $26.39 sale from $32.99 | $6.60–$8.25 | snippet |
| Etsy #4 hexagonal minimalist | geometric (hexagon), 4 | $17.25 | $4.31 | snippet |
| Etsy #5 "Geometric Coaster Set with Holder" | geometric | $18.37 | not stated | snippet |
| Chemist Tree (#24) | geometric (Platonic solids), PETG, 4 | $35.00 (currency likely CAD) | $8.75 | fetched |

Nine competitors; only one (Chemist Tree) was read from its own page. The three
Islamic-themed 3D-printed listings sit at **$23–$35 a set**; the plain-geometric ones spread
from **$12 to $33 a set**.

---

## Q5. What buyers pay extra for

| Extra | What the listings show | Rows | Seen |
|---|---|---|---|
| Holder / stand / caddy | Bundled, not priced separately: 13 of the 24 3D-printed listings with a stated set size include one (#1–#3, #6–#8, #10, #11, #13–#15, #25, #27). None of these 13 shows a "without holder" price, so the holder's premium cannot be read off one listing. Wholesale, a metal holder alone is $1.75–$2.75 (B8). | 13 + B8 | snippet |
| Gift box | Included, not an add-on: the marble inlay set (#34, $44.99, "Comes in a box ready for gift giving"), the Aga Khan museum set (#33, embossed box, $145) and the Etsy Moorish-star wood set of 6 (#47, $17.21 sale). None of the listings here shows a paid gift-box option. The boxed sets are the dearest Islamic-geometric rows found, but they are also marble or maple, so the box's own share is not separable. | 3 | fetched (2), snippet (1) |
| Custom color | Offered free by every 3D-printed seller that mentions it (#1, #2, #7, #18, #19 "mix and match"). None of the five shows a color surcharge. | 5 | fetched (2), snippet (3) |
| Personalization (name, logo) | No visible adder: #1 personalized holder at $11.99 (the cheapest set here), #18 custom logo with no adder. Logo/business sets (#15, #16) are priced in the same band as plain ones. Wedding/event coasters (B7) are priced "from $6.00 each". | 4 | fetched (1), snippet (3) |
| Multicolor | The multicolor Christmas set (#9) lists at $40 ($30 sale), the two-color geometric set (#2) at $12 — two rows, no pattern. | 2 | snippet |
| Free shipping | Most Etsy snippets show "FREE shipping" (#1, #7, #11, #29–#31, #45, #50); the eBay rows mostly charge it (#21: $8.75). Free shipping is the Etsy norm here, so a listed Etsy price includes postage. | ~9 | snippet |
| Material / maker story | The clear premium in the data is material and venue, not add-ons: museum and marble/maple sets at £24–$145 for four (#32–#34) against print-on-demand MDF at $14–$18 (#37–#39). | 6 | mixed |

---

## Sources not usable

- Etsy listing and search pages, Redbubble, eBay item pages, Faire, Amazon.com, Justin3D LLC's
  Shopify shop (https://shop.justin3dllc.com/products/6-woven-coasters-and-coaster-holder-3d-printed)
  and Diwan Egypt refused WebFetch (403/400/410/500). The Chrome extension was not connected.
- Louvre boutique coaster page (https://boutique.louvre.fr/en/product/62887-coaster-coating-tile.html),
  SFMOMA Ruth Asawa coasters, Milk Street "Marrakesh silver coasters" and KrisShop "Fez" set:
  404 on fetch; no price recorded.
- Search-tool summaries sometimes added their own arithmetic or advice (e.g. "set a modest
  5–10% set discount"); none of that is recorded here as a finding.
