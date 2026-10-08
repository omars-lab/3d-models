---
date: 2026-10-08
produced-by: checker agent (Claude Opus 5.5), the third step of "two researchers, then a checker" over researcher A (PR #631) and researcher B (PR #630). Method — read all four research files, then re-opened the pages behind the load-bearing numbers with WebFetch on 2026-10-08 (Shopify and Squarespace shops through their product JSON, which lists every variant's price and currency), plus two web searches. Etsy, Redbubble and Faire were tried once each and refused (HTTP 403); eBay and Amazon were not tried again, since both researchers recorded them as refusing. No bot check was worked around and no browser was used.
feeds:
  - docs/design/coaster/order-driven-lab-design.md §9.7 pricing
  - docs/working-model/decisions-log.md D-113 (the market band the cost-plus price is checked against)
built-from:
  - docs/research/coaster-market-pricing-a-raw.md
  - docs/research/coaster-market-pricing-a.md
  - docs/research/coaster-market-pricing-b-raw.md
  - docs/research/coaster-market-pricing-b.md
---

# Coaster market prices (consolidated)

This is the one to act on. It checks two independent research passes against the pages behind
them: researcher A ([raw](coaster-market-pricing-a-raw.md), [notes](coaster-market-pricing-a.md),
PR #631) and researcher B ([raw](coaster-market-pricing-b-raw.md),
[notes](coaster-market-pricing-b.md), PR #630). Those four files stay exactly as written; they
are the record this was built from. Row numbers below point into them: **A r45** is row 45 of
A's raw file, **B #24** or **B B1** is row 24 or B1 of B's raw file.

It feeds [order-driven-lab-design §9.7](../design/coaster/order-driven-lab-design.md#97-pricing-ideas-the-ways-to-set-a-price-side-by-side)
and [D-113](../working-model/decisions-log.md) (price = cost plus a markup, checked against a
market band). The product being compared: a 3D-printed Islamic geometric coaster, about 110 mm
across, 4–5 mm thick, PLA, one or two colors. This file holds public listing prices only, none
of our own costs or prices.

**How to read the marks.**

- **re-opened** — I loaded the page on 2026-10-08 and read the number off it.
- **snippet** — the number exists only in a search-result summary, in A's or B's file or in mine.
  The page was not opened, usually because the site refuses automated reads.
- **blocked** — the site refused the fetch (Etsy, eBay, Amazon, Redbubble, Faire).
- **carried (Oct 4)** — from the earlier pricing round,
  [2026-10-04-coaster-pricing.md](2026-10-04-coaster-pricing.md), whose checker read Etsy in a
  real Chrome tab. I did not re-open those listings; that file's own mark is carried.

Every price is a **listed (asking) price, not a sold price**. Neither pass, nor this check,
reached anything that shows what a buyer paid.

---

## The short answer

1. **Generic 3D-printed set of 4: middle half about $13–$28, median about $17** over the 21
   US-dollar sets of 4 the two passes found between them (2 re-opened, 19 snippets). The earlier
   Chrome round put the same median at $20 over 23 Etsy listings. So a plain printed set of 4
   lists at about **$17–$20**, or **$4.25–$5.00 a coaster**.
2. **Islamic-themed 3D-printed sets list higher: $25 for 4, $35 for 5, $45 for 6, so about
   $6.25–$7.50 a coaster** where the set size is known. Few listings (3 with a known size, read in
   a real browser on Oct 4; the $35 set of 5 also turns up as a snippet in both passes today).
3. **The market check for our coaster: about $20–$30 for a set of 4, $5–$7.50 a coaster.** That
   is the top half of the generic band up to the Islamic-themed sets. It is a reading of the bands,
   not a number any source states.
4. **Sets of 4 first, 6 second, single as an option.** Both passes agree, by wide counts.
5. **Per coaster, a set of 4 runs about 15–25% below a single, and a set of 6 about another 15–20%
   below a set of 4.** Four same-seller cases, all re-opened; only one of them is 3D printed.
6. **Extras are bundled, not sold:** holder in the set, gift box in the price, color choice free,
   personalization free or a couple of dollars. Both passes agree.
7. **No 3D-printing seller among those seen here publishes a bulk table.** Every published tier
   table found here is for printed-surface coasters with a setup cost, so its curve transfers only as far as
   our own cost per coaster falls with order size.

---

## 1. The market band, per coaster and per set of 4

### 1.1 The bands

| Band | Per coaster | Set of 4 | Rests on | How sure |
|---|---|---|---|---|
| **Generic 3D-printed, set of 4** | median $4.24; middle half $3.19–$7.05 | median $16.95; middle half $12.75–$28.19; range $9.99–$39.00 | 21 US-dollar listings across A and B (list below), 2 re-opened | **medium** — two passes plus the Oct 4 Chrome round land within $3 of each other on the median; 19 of 21 are snippets |
| Same, Oct 4 Chrome round | $5.00 median (39 listings, all set sizes) | $20.00 median (23 listings) | carried (Oct 4), Etsy only | medium — that round re-ran two searches by hand; its size grouping was checked on 13 listings |
| **Generic 3D-printed, set of 6** | median $3.33 | — (set of 6: median $20, range $18–$35) | 5 listings, 1 re-opened (Man Crafted, $20 with holder) | low — 5 listings; the Oct 4 round had $25.50 over 12 |
| **Islamic-themed 3D-printed** | $6.25–$7.50 where the size is known | about $25–$30 | Oct 4 Chrome round: $25 for 4 + holder, $35 for 5, $45 for 6 (all PLA, re-opened in a browser that day); today, A r40 = B #29 ($35 for 5) as a snippet in both; A r41 = B #30 ($23.26) and A r42 = B #31 ($25) with no set size | **low to medium** — few listings, three of the Oct 4 ones from one shop, all smaller than 110 mm |
| Islamic or Moroccan pattern printed on MDF (print on demand, not 3D printed) | $3.50–$4.50 | $14–$18 | Redbubble, 3 listings (A r10–r11, B #37–#39) | medium — both passes saw the same two prices; snippet only, Redbubble blocked today |
| **Same-size Islamic geometric, other material (the ceiling)** | £6 | £24 | Leighton House museum shop, 110 × 110 mm laser-cut MDF (A r1 = B #32), **re-opened: £24.00 GBP** | high that the price is real; low that it transfers (a museum sells its name and its visitors too) |
| Premium Islamic geometric | $11.25 to CAD 36.25 | $44.99 marble; CAD 145 maple | Zahra marble with brass inlay, gift box (re-opened: $44.99 USD, compare-at $49.99, out of stock); Aga Khan Museum maple set, gift box (re-opened: **145.00 CAD**) | high that the prices are real; a ceiling, not a band |

The 21 generic sets of 4, per set, low to high (each listing once; where A and B saw the same
listing it is counted once): $9.99 (A r66), $11.99 (A r64 = B #1), $11.99 (A r67), $12.00
(A r57 = B #2), $12.50 (B #21, plus shipping), $12.99 (A r67), $14.00 (A r50), $14.99 (A r46,
**re-opened**), $14.99 (A r67), $15.00 (B #3), $16.95 (B #17), $17.25 (B #4), $19.99 (A r68),
$20.00 (A r58 = B #6), $20.97 (A r45, **re-opened**), $26.39 sale (A r53 = B #7), $29.98 (A r65),
$30.00 (B #8), $30.00 sale (B #9), $33.20 (A r51 = B #25), $39.00 (B #10). Left out: Chemist Tree
(CAD, see 1.2), the £20 eBay set (B #22), the PLN and INR sets (A r52, B #27), and A r69's
$55-or-best-offer outlier. Taking out the five licensed or logo sets (A r65, r66, r67 Milwaukee,
r68, B #21) moves the median only to about $17.10.

### 1.2 Why A's and B's medians came apart

A gave **$3.88 a coaster, about $15.50 a set of 4**. B gave **about $5.60 a coaster, about $22.50
a set of 4**. Both did their arithmetic right on their own lists; the gap is in what went in.

- **A mixed set sizes.** A's $3.88 is the median per coaster over sets of 4, 5, 6 and 8 together,
  then multiplied by 4. Sets of 6 and 8 run cheaper per coaster (section 3), so this pulls a "set
  of 4" figure down.
- **B's sample ran high.** B's 14 sets of 4 lacked the cheap eBay and Amazon rows A found
  ($9.99–$14.99) and included more $30–$39 listings A did not have. B also counted Chemist Tree's
  $35 as about US dollars ("currency likely CAD").
- **Chemist Tree is CAD.** Re-opened: the store's product data gives `price_currency` CAD for the
  35.00 price. B was right to flag it; A listed it as $35 and put it at the top of the band. It is
  the only 3D-printed PETG set seen, so it is left out of the US-dollar median rather than
  converted at a rate I did not fetch.
- **Aga Khan is CAD too.** Re-opened: 145.00 CAD. A wrote $145; B wrote "currency not named". It
  sits far above every band either way.

Pooling both lists, one listing counted once, gives the $16.95 median above. The Oct 4 round's
$20.00 sits between A and B. **Verdict: a plain 3D-printed set of 4 lists at about $17–$20; A's
$15.50 is low because of the mixed sizes, B's $22.50 is high because of a thinner, pricier
sample.**

### 1.3 Size does not show in the price

Both passes found this and it holds: most printed competitors are 3.5–4 in (about 89–100 mm); the
one ~120 mm printed coaster (MAD Made, re-opened: "approximately 12 cm") sits in the lower half
of the band at $3.75 a coaster in a set of 4. None of the listings seen here charges more for a
bigger coaster. So the band transfers to a 110 mm coaster only as "what a buyer sees beside it",
not as evidence that a larger coaster earns more.

### 1.4 The market check for D-113

| Check | Set of 4 | Per coaster | Read |
|---|---|---|---|
| Below this, cheaper than most printed sets | under about $13 | under about $3.25 | bottom quarter of the generic band |
| **Where an Islamic geometric printed set sits** | **about $20–$30** | **about $5–$7.50** | top half of the generic band up to the Islamic-themed sets |
| Above this, dearer than any printed set seen | over about $35–$39 | over about $9–$10 | only non-printed or museum sets list here |

How sure: **medium** on the generic band, **low to medium** on where the Islamic geometric set
sits within it. The middle row is my judgment from the bands; both A ("upper half of the generic
band or above it") and B ("the mid band, $5–$7.50 a coaster / $20–$30 a set") reached the same
reading on their own.

---

## 2. Set sizes to offer

| Size | A's count | B's count | Read |
|---|---|---|---|
| 4 | about 40 listings | 30 rows | the default everywhere: both passes, every kind of seller |
| 6 | about 10 | 9 | second; often with a holder, and for Ramadan and Eid table sets |
| 1 | 7 | 5–6 | an option beside sets, or a premium single; uncommon among printed sellers |
| 2 | 2 | 2–3 | rare; logo and custom sets |
| 5 | 2 | 2 | "one of each pattern" sets; the Islamic calligraphy set of 5 |
| 8 | 3 | 1 | rare, at the low end per coaster |
| 12 | 0 | 1 | one Ramadan table set (Islamic Wall Art Store, re-opened) |

**Offer: single, set of 4, set of 6.** A also suggests a "one of each design" set when a
collection has 5 designs; B suggests a set of 12 if Ramadan and Eid hosting is a target. Both are
reasonable add-ons resting on 1–2 listings each.

How sure: **medium** for 4 and 6. Two independent counts agree on the order. These count listings,
not sales. The one outside source on set sizes, Listybox (re-opened), says "Consider offering sets
of 4 or 6 for a higher average order value" and gives no data behind it.

---

## 3. Price breaks

### 3.1 By set size (the same seller, the same item)

Every case here was re-opened today.

| Seller | Kind | Step | Per coaster | Change per coaster | Found by |
|---|---|---|---|---|---|
| MAD Made Creations | **3D-printed PLA**, ~12 cm | 1 → 2 → 4: $4.99, $7.99, $14.99 | $4.99 → $4.00 → $3.75 | −20% at 2, **−25% at 4** | A (B saw only "about $4.99 base") |
| Santa Barbara Company | ceramic tile, 4.25 in | 1 → 2 → 4: $12, $24, $40 | $12 → $12 → $10 | 0% at 2, **−17% at 4** | B |
| Zsuzsanna Horvath | birch plywood, 10 cm | 4 → 6: DKK 240, DKK 295 | DKK 60 → DKK 49.17 | **−18% at 6**, but the 4 is painted black and the 6 natural, and neither page offers the other finish | A |
| Islamic Wall Art Store | mirror acrylic | 6 → 12: $44, $54 (compare-at $59, $72) | $7.33 → $4.50 | **−39% at 12** | B |

Across sellers the same direction shows: printed sets of 6 run about $3.33 a coaster (5 listings)
against about $4.24 for sets of 4 (21 listings), and the Oct 4 round had $25.50 for 6 against
$20.00 for 4, which is $4.25 against $5.00 a coaster (−15%).

**Steps to model:** a set of 4 at about **15–25% less per coaster than a single**; a set of 6 at
about **15–20% less per coaster than a set of 4**; a 12-piece table set, if offered, could go
deeper (one seller: −39%). How sure: **low to medium** — four sellers, all re-opened, but only one
of them 3D printed and the 4 → 6 pair has the paint confound.

### 3.2 By order size (bulk, a café or an event)

No 3D-printing seller among those seen here publishes a quantity table: none of the 11 A read,
none of the 32 printed listings B read (only 4 of B's from the page itself), and none in my two
searches. The one printed wedding-coaster listing (B B7, snippet) says "starting at $6.00 each"
and "discounts available for bulk orders", with no tiers.

What is published, all by sellers of printed-surface coasters (paper, cork, ceramic, glass,
acrylic):

| Source | Tiers | Change | Mark |
|---|---|---|---|
| Qstomize custom coasters (B B1) | 50–99 $3.95; 100–249 $2.95; 250+ $2.25 per piece; minimum 50; "all-inclusive" of setup | −25% at 100, −43% at 250 | re-opened |
| Qstomize ceramic set (B B2) | 50–99 $6.50; 100–249 $5.50; 250–499 $4.75; 500+ $4.10 per "piece" (the page does not say whether a piece is one coaster or the set of four) | −15%, −27%, −37% | re-opened |
| Contrado ceramic (A Q3) | "Wholesale: Up to 20%"; "Bulk Orders: Custom Quotation"; packs of 1–12 with no per-pack price shown | up to −20% | re-opened |
| Glass coasters, "Buy 3 – 5 and get 10% off" (A Q3) | — | −10% | snippet |
| eBay cork coasters, "Buy 4 or more for 10.0 each" against $12.50 (A Q3) | — | −20% | snippet, eBay blocked |
| Sense2 glass set, Fluid Branding acrylic and foam, Sticker Mule, 4over4, LamPro (A Q3, B B3–B6) | minimums of 50–250, setup fees of £25–$160, falling 40–57% over thousands | — | snippet in both passes; not re-opened |

The snippets for Qstomize (B), Islamic Wall Art Store (B), and Leighton House and Chemist Tree
(both passes) had shown different prices from the pages: higher for Qstomize, lower for the other
three. B's
coasterholders.com row (B B8) also differs today: snippet "holder $1.75 from $2.75, bundle $3.99
from $4.99", page (re-opened) "Wholesale Coaster Holder $2.50", "Coasters With Holder $6.99, was
$9.99". Snippet prices drift.

### 3.3 Wholesale (a shop reselling)

Both passes: **wholesale is about half of retail ("keystone")**. Re-check:

- The glossary B cited (femfounded.org, re-opened): "Keystone pricing is setting the retail price
  at double the cost, which produces a 100% markup and a 50% gross margin." It does not mention
  Faire.
- Faire's own article and blog: **blocked** (403) for A, B and me. A search summary today quotes
  the Faire help article: "Typically that margin is 50%—or 2x the wholesale price." That is a
  snippet.
- **Only in A, snippet only:** Faire's first-order minimum of $100–$150 and a rule that Faire
  prices must be no higher than on other channels. Today's search summary said it could not
  confirm the second one against Faire's policy. Unverified.
- **Only in this check, snippet only:** Faire also takes a commission from the brand on each
  order. Third-party reviews disagree on the rate (one says 25% on a first order, 15% on repeats,
  0% on retailers the brand brings; another says 10% for those). So what a brand keeps on Faire is
  less than half of retail; how much less is not settled.

### 3.4 What transfers to a 3D-printed coaster

- **Set-size steps transfer as buyer expectations; one of them is from a printed coaster.** MAD
  Made's 1 → 4 step (−25%) is the same process as ours. The step is affordable for us only if
  part of our cost is fixed per order (packing, per-order platform fees, hands-on time per order),
  because a bigger set spreads that; the print cost per coaster itself does not fall with set size.
  If almost all our cost is per coaster, a 25% set discount comes straight out of the markup.
- **The bulk curves (−25% at 100, −40% or more at 250) transfer only if our cost per coaster falls
  the same way.** Those sellers spread a setup cost (art, a plate, a die, a press run) over the
  order. A 3D print's cost is mostly print time and filament per piece, which the Oct 4 round
  priced per coaster, with hands-on time per order as its largest unmeasured input. Ours falls only through per-order work spread over more
  coasters and fuller plates, and neither is measured yet. A and B agree on this condition. A goes
  further and calls the small published consumer breaks (10%, 20%) "the ones made by sellers whose
  cost behaves like ours"; that does not hold as stated, since those sellers make glass, cork and
  print-on-demand ceramic coasters, not printed ones. They transfer as "what a buyer sees
  elsewhere", not as cost evidence.
- **Keystone transfers as a rule about the reseller, not about us.** A shop buying wholesale
  expects to double the price. So a wholesale line exists only if retail is at least twice our
  full cost, and more than twice if a platform commission comes out of the wholesale price.

**Breaks to model for now, all low confidence:** about 10% for a small gift order of a few sets;
up to about 20% for a café or event order; tiers beyond that only once our own cost per coaster at
50 or 100 pieces is measured; wholesale at half of retail, before any platform commission.

---

## 4. Extras

| Extra | What the listings show | Mark | Model it as |
|---|---|---|---|
| **Holder or stand** | Bundled in most printed sets: all 13 Fantastic Plastics designs (re-opened: every title says "with Free Holder"), Man Crafted's set of 6 (re-opened), and 13 of B's 24 printed sets. None of the listings seen here prices the set with and without a holder, so its premium can't be read off. Sold alone: $5.00 (A, RDM Designs, snippet; the site did not resolve today) and $6.74 from $8.99 (A, Etsy rack, snippet); blank supply holders $2.50 (coasterholders.com, re-opened) | holder in a set: re-opened; standalone retail price: snippet | part of the set; a standalone holder at about $5–$9 if sold |
| **Gift box** | Included, never a separate line, in every listing that mentions one: Aga Khan (embossed box, re-opened), Zahra marble ("Comes in a box ready for gift giving", re-opened), Lasaris, Puttyprint and an Etsy Moorish-star wood set (snippets). A counts 0 of 5 charging for it; B 0 of 3 | re-opened (2), snippet (rest) | a cost, not a revenue line |
| **Custom color** | Free wherever offered: Fantastic Plastics (re-opened: same $20.97 for every design, "Custom Color Options", 15+ colors), Adeptus Craftus (re-opened: color choice from a dropdown, $12.99 for 2, no adder), Boyd's 3D Studio (re-opened: $8.00 a coaster, "mix and match colors"), plus 3 Etsy snippets. A found 2, B 5; none of the listings seen here charges for color | re-opened (3), snippet (3) | no upcharge |
| **Personalization** | One priced add-on: Lifetime Leather, large center letter +$2.00, fire-brand stamp free, custom stamp on request (re-opened; leather, not printed). Printed: Adeptus custom logo with no adder (re-opened); personalized and logo sets (Tiny Tinker $11.99 for 4, logo 8-pack $26.99) sit at the low end of the band (snippets) | re-opened (2), snippet (rest) | free, or a small fixed add-on of about $2; no evidence of a large premium |
| **Theme (Islamic, Ramadan)** | Islamic-themed printed sets list at $6.25–$7.50 a coaster against about $4.25–$5.00 generic | see 1.1 | a reason to sit in the upper half of the band, not a separate add-on |
| **Material and venue** | Museum and premium sets list at about 1.5–2× (Leighton £24) to several times (marble $44.99, maple CAD 145) the printed median | re-opened | a ceiling, not a band |
| **Shipping** | Most Etsy listings say free shipping, so their price includes postage; eBay rows mostly add it (e.g. +$6.07, +$8.75) | snippet in both passes | compare against a price that includes shipping |

---

## 5. Agree, disagree, only one

| Claim | A | B | Re-check (2026-10-08) | Verdict |
|---|---|---|---|---|
| Leighton House 110 mm MDF set of 4 | £24.00 fetched; snippet £19 | £24.00 fetched; snippet £19 | re-opened: £24.00 GBP; today's search summary again says £19 | **agree**; the £19 is a stale snippet |
| Zahra marble Islamic inlay set | $44.99 from $49.99, gift box | same, sold out | re-opened: same, inventory 0 | **agree** |
| Aga Khan maple set | "$145.00" | $145, currency not named | re-opened: **145.00 CAD** | **B closer**; it is CAD |
| Chemist Tree PETG set of 4 | $35 (treated as US) | $35, "currency likely CAD" | re-opened: **35.00 CAD** | **B right** |
| Generic printed set of 4, median | about $15.50 (from $3.88 × 4 over mixed sizes) | about $22.50 (14 sets of 4) | pooled 21 sets of 4: **$16.95**; Oct 4 Chrome round: $20.00 | **neither alone**; about $17–$20 |
| Islamic-themed printed sets | $19–$35, 4 snippets | $23.26, $25, $35, 3 snippets | Etsy blocked; Oct 4 Chrome round had $25 (4), $35 (5), $45 (6) | **agree** on the shape; $45 for 6 was in neither pass |
| Islamic set of 5, review count | 98 reviews | 104 reviews | blocked | prices agree ($35); counts drift between snippets |
| Islamic Moroccan geometric printed listing, set size | "possibly 6" | not stated | blocked | **unknown** |
| An Islamic geometric printed seller with its own shop | none found | none found | none in my search either (only model files and non-printed sets came back) | **agree**: none of the three searches found one; says little about whether one exists |
| Set of 4 is the default, 6 second | about 40 / 10 | 30 / 9 | Listybox re-opened: "sets of 4 or 6", no data | **agree** |
| Set-size step 1 → 4 | −25% (MAD Made, fetched) | MAD Made variants not seen; −17% (Santa Barbara) | both re-opened and confirmed | **both right**, different sellers; −15% to −25% |
| Set-size step 4 → 6 | −18% (Zsuzsanna, confounded) | not found | re-opened: painted 4 vs natural 6 confirmed | **A only**, confound stands |
| Set-size step 6 → 12 | not found | −39% (Islamic Wall Art Store) | re-opened: $44 / $54 for 6 / 12, compare-at $59 / $72 | **B only**, confirmed |
| Fantastic Plastics, 13 printed designs, set of 4 + free holder | $20.97; Mandala OM $22.97 | not found | re-opened: same | **A only**, confirmed |
| Man Crafted printed set of 6 + holder | $20.00 | not found | re-opened: $20.00, 4 in | **A only**, confirmed |
| Boyd's printed stackable coaster | not found | $8.00 "Sale", unit not stated | re-opened: $8.00 each, "each coaster is priced individually" | **B only**, confirmed, per coaster |
| Adeptus Craftus printed set of 2 | not found | $12.99, logo, no adder | re-opened: same | **B only**, confirmed |
| Bulk tiers, printed-surface coasters | promo curves shown, "do not port" | Qstomize −25% / −43%, "only if our cost falls that way" | Qstomize both re-opened and confirmed; "piece" in the ceramic set undefined | **agree** on the transfer condition; B's tiers confirmed |
| Small consumer breaks | 10% (glass), −20% (eBay cork), Contrado "up to 20%" | not found | Contrado re-opened: "Wholesale: Up to 20%", bulk by quote; the other two snippets | **A only**; Contrado confirmed, the rest snippet |
| Keystone: wholesale about half of retail | Faire guidance, snippet | glossary + Faire, snippet | glossary re-opened ("double the cost ... 50% gross margin"); Faire blocked; search summary quotes Faire "Typically that margin is 50%—or 2x the wholesale price." | **agree**; medium (Faire's own page unread) |
| Faire minimums and same-price rule | $100–$150 first order; parity rule | not found | blocked; search summary could not confirm parity | **A only**, snippet; unverified |
| Faire commission on brands | not found | not found | third-party snippets disagree (25% / 15% / 0%, or 10%) | **only this check**, snippet; flagged |
| Holder bundled | 13/13 Fantastic Plastics; most Etsy sets | 13 of 24 printed sets | Fantastic Plastics re-opened: all 13 "with Free Holder" | **agree** |
| Standalone holder price | $5.00 RDM, $6.74 Etsy (snippets) | wholesale metal $1.75–$2.75 (snippet) | RDM site did not resolve; coasterholders.com re-opened: holder $2.50, and the bundle price differs from B's snippet | **not settled**; retail $5–$9 rests on 2 snippets |
| Gift box included, not charged | 0 of 5 charge | 0 of 3 charge | Aga Khan and Zahra re-opened: box included | **agree** |
| Custom color free | 2 listings | 5 listings | Fantastic Plastics, Adeptus, Boyd's re-opened: no adder | **agree** |
| Personalization | +$2 large letter (leather); printed personalized sets at the low end | no visible adder in 4 listings | Lifetime Leather re-opened: +$2.00; Adeptus re-opened: no adder | **agree**: free or about $2 |
| Size is not priced | yes | yes | MAD Made re-opened: 12 cm, lower half of band | **agree** |

---

## 6. What is still unknown, and how to settle it

- **Etsy prices from today.** Every Etsy number in both passes is a snippet, and snippets were
  wrong on at least five pages that did load (Leighton House, Chemist Tree, Islamic Wall Art
  Store, Qstomize, coasterholders.com). Settle it by reading Etsy in a real browser, as the Oct 4
  round did: re-run the searches "3d printed coasters set of 4" and "islamic geometric coaster", open the
  Islamic-themed listings (A r40–r44, B #29–#31) for set size, size and material, and record
  20–50 listings with their review counts.
- **What sells, not what is asked.** Nothing here shows a sold price. The nearest public signals
  are Etsy review counts and eBay's sold-listings filter, both of which need a browser. Our own
  first orders will say more than either.
- **A second printed same-seller curve,** especially 4 → 6, to replace the painted-versus-natural
  plywood pair.
- **Whether a 110 mm Islamic geometric printed set earns the top half of the band.** Three
  Islamic-themed printed listings with a known size is thin. Only selling it will show; simulated
  buyers (D-104) can rank prices but are not customer research.
- **Our own cost at 50 and 100 coasters.** Until it is measured, the bulk curves stay borrowed
  shapes. Time a real multi-set order: per-order hands-on time and packing, and whether fuller
  plates lower the per-coaster print time.
- **Faire's terms.** Wholesale prices and the exact commission sit behind a retailer or brand
  login; Faire's help pages refused automated reads.
- **Exchange rates.** GBP, CAD and DKK prices are left as listed. No rate was fetched; any
  conversion in A's or B's notes uses an assumed rate.

---

## Sources re-opened on 2026-10-08

All with WebFetch; Shopify product JSON unless noted.

- MAD Made Creations, Squarespace product data (1 / 2 / 4: $4.99 / $7.99 / $14.99; ~12 cm PLA)
- Fantastic Plastics Jax, collection product data (13 designs, $20.97 / $22.97, free holder)
- Man Crafted Shop ($20.00, 6 + holder, 4 in)
- Chemist Tree (35.00 CAD, PETG + cork, 3.75 in)
- Leighton House museum shop (£24.00 GBP, 110 × 110 mm MDF)
- Aga Khan Museum shop (145.00 CAD, maple, embossed box)
- With a Spin, Zahra ($44.99, compare-at $49.99, out of stock, gift box)
- Islamic Wall Art Store (6: $44 / $59; 12: $54 / $72; 48 variants, price set only by size)
- Santa Barbara Company (1 / 2 / 4: $12 / $24 / $40)
- Zsuzsanna Horvath, set of 4 and set of 6 pages (DKK 240 painted; DKK 295 natural)
- Lifetime Leather ($25.00; large center letter $2.00)
- Adeptus Craftus, Wix page ($12.99 for 2, PLA, color and logo, no adder)
- Boyd's 3D Studio, collection data ($8.00 each, five colors)
- Heart of Anatolia, category page (sets of 4 $14.70–$19.60; sets of 6 $19.50–$34.80 on sale)
- Qstomize custom coasters and ceramic set, pages (tiers as in 3.2)
- Contrado personalized ceramic coasters, page ("From $29.95", "Wholesale: Up to 20%")
- coasterholders.com tag page (holder $2.50; bundle $6.99 from $9.99)
- Over the Moon, Alhambra linen set of 6 ($60.00); Kemper Art Museum ceramic set of 4 ($60.00)
- Zazzle Moroccan zellige coaster, page ($10.29 from $12.10, single, no quantity tiers)
- Nestasia lavender ceramic set of 4 (₹560, compare-at ₹890); MadeMe Moroccan ceramic set of 4,
  page (£14.50); V&A De Morgan coaster, page (£3, single)
- Listybox coaster niche page ("sets of 4 or 6", "$8 to $35", no method stated)
- femfounded.org keystone pricing glossary

Tried and refused (403): Etsy's islamic_coasters market page, Redbubble Islamic geometric coaster,
Faire blog and Faire help article. Did not resolve: store.rdm-designs.com. Searches: one for an
Islamic geometric 3D-printed coaster shop outside Etsy (none found), one for Faire's wholesale
guidance (summary only).

Carried from the earlier round without re-opening:
[2026-10-04-coaster-pricing.md](2026-10-04-coaster-pricing.md#what-the-two-passes-agreed-on)
(Etsy search medians and the Islamic printed sets, read in Chrome on Oct 4).
