---
date: 2026-10-08
produced-by: researcher B (Claude subagent, Opus 5.5), one of two independent researchers on the same question; the other researcher's files and branch were not read. Built only from the raw findings file beside it.
feeds:
  - docs/design/coaster/order-driven-lab-design.md §9.7 pricing
---

# What coasters like ours sell for (research B, design notes)

Raw findings, every number with its URL and how it was read:
[coaster-market-pricing-b-raw.md](coaster-market-pricing-b-raw.md). Row numbers (#n, Bn) below
point into that file. This feeds the "market prices shown beside the cost" part of
[order-driven-lab-design §9.7](../design/coaster/order-driven-lab-design.md#97-pricing-ideas-the-ways-to-set-a-price-side-by-side).

**What we are comparing.** A 3D-printed Islamic geometric coaster, about 110 mm across, 4–5 mm
thick, PLA, one or two colors. This file holds public listing prices only — none of our own
costs or prices.

**How sure to be, in one line.** Most marketplace numbers (Etsy, eBay, Redbubble) are from
search-result summaries, because those sites refused to load for the fetch tool; and on four
pages that did load, the page disagreed with the earlier summary. So the bands below are the
right *shape* and roughly the right *level*, but any single snippet price may be off. Every
price is a listed price, not a sold one.

---

## 1. The market bands, per coaster and per set of 4

| Band | Per coaster | Set of 4 | What sits here | Rests on | Confidence |
|---|---|---|---|---|---|
| **Budget 3D-printed** | $3–$4.50 | $12–$17 | plain or simple geometric PLA sets, often with a holder; personalized-name sets | 6 listings (#1–#4, #17, #21) | medium — many listings agree, all snippets |
| **Mid 3D-printed** | $5–$7.50 | $20–$30 | geometric sets with holder or tray, multicolor sets, the Islamic-themed 3D-printed sets | 5 set-of-4 listings (#6–#9, #22) + 3 Islamic-themed (#29–#31) | medium-low — snippets; Islamic ones have unclear set sizes |
| **Top of 3D-printed** | $8–$10 | $33–$39 | design-led sets from small shops (caddy, PETG, maker story) | 3 listings (#10, #24, #25) | low — one fetched (#24, currency probably CAD) |
| **Print-on-demand pattern coasters** (not 3D printed) | $3.50–$4.50 | $14–$18 | Islamic and Moroccan patterns printed on MDF blanks | 3 listings (#37–#39) | medium — same blank, consistent |
| **Museum / premium Islamic geometric** (not 3D printed) | £6–$36 | £24–$145 | laser-cut MDF at 110 mm (£24, #32), marble with brass inlay in a gift box ($44.99, #34), maple in an embossed box ($145, #33) | 3 listings, all fetched | high that the prices are real; low that they transfer (see §5) |

**Across all 14 3D-printed sets of four with a price:** $11.99 to $39.00 a set; middle of the pack
about $22.50 a set, or about $5.60 a coaster (raw §2c). Free shipping is usually included on Etsy.

**The closest competitors** — Islamic-themed 3D-printed coasters on Etsy — are listed at
**$23.26, $25 and $35 a set** (#29–#31, snippets). Only one of the three is geometric (#30, set
size not shown); the other two are calligraphy. That is three listings; none of the searches here
found an Islamic-geometric 3D-printed coaster sold on Amazon, eBay or an independent shop, which
says little about whether one exists.

**Where a ~110 mm Islamic-geometric PLA coaster plausibly sits:** the mid band, $5–$7.50 a
coaster / $20–$30 a set of four, with the Islamic-themed listings near its top. That is my
reading of the bands, not a number any source states. The budget band is where plain geometric
3D-printed sets crowd; the museum band shows buyers pay much more for Islamic geometry when it
comes as marble, maple or a museum's name — not evidence they pay it for PLA.

## 2. Set sizes to offer

| Size | How common (rows in raw §2a) | Note |
|---|---|---|
| **4** | 30 rows — more than all other sizes combined (~21) | the default everywhere; the size buyers compare on |
| **6** | 9 rows | second; common with a holder (#11, #13, #14) and for Ramadan/Eid gift sets (#35, #47, #50) |
| **1** | 5–6 rows, mostly print-on-demand and tile shops | rare among 3D-printed sellers (1 of the 3D-printed rows, #20) |
| **2** | 2–3 rows | small; logo and custom sets (#16, #18) |
| 5, 8, 12 | 2, 1, 1 rows | 12 appears only as a Ramadan table set (#35) |

**Offer:** single, set of 4, set of 6; add a 12-piece event/table set if Ramadan and Eid hosting
is a target. Set of 2 is optional. Confidence: medium — the count is broad, but it counts
listings, not sales.

## 3. Price breaks to model

### 3a. Set size (same seller, same item)

Only two sellers show the same item at several set sizes on a fetched page:

- Ceramic tile, single → 2 → 4: **0% off at 2, 17% off a coaster at 4** (#55).
- Mirror-acrylic Ramadan set, 6 → 12: **39% off a coaster at 12** (#35).

Across different sellers, 3D-printed sets of 6 and 8 run lower per coaster (median ~$3.60 at 6,
4 rows; $3.37 at 8, 1 row) than sets of 4 (~$5.60), but that mixes sellers and designs.

**Model:** a per-coaster discount that is small from 1 to 4 (around a sixth) and larger at
table-set sizes (6–12). Confidence: low — two same-item sources.

### 3b. Bulk orders (cafés, events, gifts)

No 3D-printed seller among the 32 3D-printed listings here publishes a quantity-tier table; the
one wedding/event seller says "from $6.00 each" and "discounts available for bulk orders" (B7).
Every published tier table found is for printed-surface coasters:

| Source | Tiers | Drop |
|---|---|---|
| Qstomize custom (B1, fetched) | 50 / 100 / 250 | −25% at 100, −43% at 250 |
| Qstomize ceramic set (B2, fetched) | 50 / 100 / 250 / 500 | −15%, −27%, −37% |
| Sense2 glass (B4, snippet) | 100 → 50,000 | −42% |
| Fluid Branding acrylic (B5, snippet) | 50 → 10,000 | −57% |

Minimum orders in those tables start at **50** (B1, B2, B5) or **100** (B3, B4), and several add a
one-off setup fee. **Model:** tiers at about 25, 50, 100 and 250 pieces, falling up to roughly
a quarter at 100 and two-fifths at 250 — **only if our own cost per coaster falls that way**.
These curves come from processes with a large setup cost (a printing plate, a die) spread over a
run; a 3D print's cost is mostly per-piece print time and filament, so the curve transfers only
as far as plate packing and fewer setups actually lower our per-coaster cost. Confidence: low
for 3D printing.

### 3c. Wholesale (shops reselling)

Retail at about **2 × wholesale** (keystone) is the convention; one Faire maker shows
MSRP $11.00 and "$5.50 ea" (B9). Both are snippets — the Faire pages refused to load.
Confidence: medium that keystone is the norm, low on Faire's exact terms.

## 4. What buyers pay extra for

- **A holder** is in 13 of 24 3D-printed set listings, always bundled; no listing here prices it
  separately, so its premium can't be read directly. Sets with a holder span the whole range
  ($11.99–$39), so a holder is expected rather than a premium. Wholesale metal holders: $1.75–$2.75 (B8).
- **A gift box** appears only bundled, in the dearest Islamic-geometric sets (#33, #34) and one
  cheap wood set (#47). No paid gift-box option in any listing here.
- **Custom color and personalization** carry no visible surcharge in any of the 3D-printed
  listings that offer them (5 for color, 4 for names/logos). They are table stakes, not upsells,
  in this sample.
- **Material and venue** carry the real premium: marble, maple, a museum shop.

## 5. Where these numbers stop holding

- **Size.** Most comparison coasters are about 4 in (~100 mm); ours is ~110 mm. Leighton House
  (#32) is exactly 110 mm. A 10% larger coaster uses more filament and time, but nothing in this
  data shows buyers paying more for 10 mm.
- **Currency and region.** Prices are USD unless marked; the GBP, CAD, INR and EGP rows are not
  converted except for rough ordering.
- **Snippets drift.** On four pages that did load, the snippet price was wrong (#32, #24, #35,
  B1/B2). Before a market price is printed next to a cost on a page someone will rely on, open the
  listing in a browser and re-read it.
- **Listed, not sold.** Review counts (#29 104, #30 99) are the only sales signal, and they
  count reviews over the listing's life, not current demand.

## Assumed, not decided

- That the mid band is where we sit is a judgment from the bands, not a source's claim.
- The bulk-tier shape is borrowed from non-3D processes, under the condition in §3b.
- Set sizes to offer follow how often each size is listed, which is not proof of what sells.
