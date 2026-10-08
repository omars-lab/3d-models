# Fixture 1, priced by hand

FIXTURE: every setting in [`settings.fixture.yaml`](settings.fixture.yaml) is made up so the sums check
by hand. None is a price or a real cost. This is the hand working that
`expected-price.json` and `expected-scenarios.json` must equal, to the cent
([order-driven-lab-design §9.6](../../../../../../docs/design/coaster/order-driven-lab-design.md#96-simulated-orders-the-regression-suite)).
The formula is §9.3's; amounts are carried at full precision and rounded only when shown.

## What the plan gives

From [`expected-plan.json`](expected-plan.json): 4 coasters on 5 plates, one bed each, so 5 warm-ups.
No PLA Matte print has been timed, so every plate uses its sliced minutes and every amount built on them
is marked floor.

| Plate | Grams | Sliced minutes |
|---|---|---|
| Ivory White 11100 | 68.88 | 210.4 |
| Ice Blue 11601 | 3.14 | 11.6 |
| Sky Blue 11603 | 2.61 | 17.7 |
| Marine Blue 11600 | 18.16 | 42.6 |
| Dark Blue 11602 | 24.47 | 68.8 |
| **Order** | **117.26** | **351.1** |

## The price

| Line | Working | Amount |
|---|---|---|
| printer hours | 351.1 ÷ 60 + 5 × 6 ÷ 60 = 381.1 ÷ 60 | 6.3517 h (floor) |
| material | 117.26 g × $1 a gram | $117.26 |
| power | 6.3517 × 1000 ÷ 1000 × $1 | $6.35 (floor) |
| wear | 6.3517 × $100 ÷ 100 | $6.35 (floor) |
| made | (117.26 + 6.3517 + 6.3517) ÷ 0.5 = 129.9633 ÷ 0.5 | $259.93 (floor) |
| labor | 15 minutes × 4 coasters ÷ 60 × $10 | $10.00 |
| packaging | | $4.00 |
| cost | 259.9267 + 10 + 4 | $273.93 (floor) |
| break-even | (273.9267 + 1) ÷ (1 − 0.2) | $343.66 (floor) |
| suggested | 343.6583 × (1 + 1) | $687.32 (floor) |
| each | ÷ 4: cost, break-even, suggested | $68.48, $85.91, $171.83 |

## The scenarios

`margin each = price each × 0.8 − $1 ÷ coasters − cost each`, and to cover = $1,000 ÷ margin each, rounded up.

| Row | Price each | Cost each | Margin each | To cover |
|---|---|---|---|---|
| cost-plus | 687.3167 ÷ 4 = 171.83 | 68.48 | 137.46 − 0.25 − 68.48 = 68.73 | 15 |
| market range | 50 | 68.48 | 40 − 0.25 − 68.48 = −28.73 | never, below break-even |
| story, premium | 200 | 68.48 | 91.27 | 11 |
| by finish | 100 (PLA Matte) | 68.48 | 11.27 | 89 |
| set of 4 | 440 ÷ 4 = 110 | 68.48 | 19.27 | 52 |
| set of 6 | 540 ÷ 6 = 90 | 68.32 | 72 − 0.17 − 68.32 = 3.52 | 285 |
| custom theme | 178.08 | 70.98 | 71.23 | 15 |
| launch price | 171.83 × 0.5 = 85.91 | 68.48 | 0.00 | never, below break-even |

**The set of 6 works out its own order.** Six coasters scale the plan by 1.5: grams 175.89, minutes
526.65, and each color takes a second bed, so 10 warm-ups. Printer hours (526.65 + 60) ÷ 60 = 9.7775;
made (175.89 + 9.7775 + 9.7775) ÷ 0.5 = 390.89; labor 6 × 15 ÷ 60 × $10 = $15; cost 390.89 + 15 + 4 =
409.89, so $68.32 each. A row that reused the 4-coaster cost each ($68.48) would fail the golden.
Packaging is $4 rather than $2 for this reason: at $2 the two happen to come out equal to the cent
($67.98), and the check could not tell them apart.

**The custom theme** adds 60 design minutes × $10 an hour = $10 to the cost: 283.93, break-even
(283.93 + 1) ÷ 0.8 = 356.16, suggested 712.33, so $178.08 and $70.98 each.

**The launch price** is the cost-plus price at half off, which lands on break-even: its margin rounds
to zero, and a margin of zero or less is tagged below break-even, with "never" to cover.

## Make and sell X a month

[§9.7](../../../../../../docs/design/coaster/order-driven-lab-design.md#97-pricing-ideas-the-ways-to-set-a-price-side-by-side)'s
what-if at X = 40 coasters a month (FIXTURE, like every other setting). Each row takes the margin each
above at full precision and multiplies it by 40; it never multiplies the rounded margin.

- revenue a month = price each × 40
- margin a month = margin each × 40
- profit a month = margin a month − $1,000 of monthly fixed costs

| Row | Revenue a month | Margin a month | Profit a month |
|---|---|---|---|
| cost-plus | 171.8292 × 40 = $6,873.17 | 68.7317 × 40 = $2,749.27 | $1,749.27 |
| market range | $2,000.00 | −$1,149.27 | −$2,149.27 |
| story, premium | $8,000.00 | $3,650.73 | $2,650.73 |
| by finish | $4,000.00 | $450.73 | −$549.27 |
| set of 4 | $4,400.00 | $770.73 | −$229.27 |
| set of 6 | $3,600.00 | 3.5183 × 40 = $140.73 | −$859.27 |
| custom theme | $7,123.17 | $2,849.27 | $1,849.27 |
| launch price | $3,436.58 | $0.00 | −$1,000.00 |

Rounding the cost-plus margin to $68.73 before multiplying would give $2,749.20, seven cents off.
Cost-plus covers the fixed costs at 15 coasters a month and not at 14: 68.7317 × 15 − 1,000 = $30.98, and
68.7317 × 14 − 1,000 = −$37.76.

## The price breaks

One single price of $150 each, and each break applied once. The set of 4 is the single price with
its break off. Every other break comes off the set-of-4 price, never off the typed `set_of_4` of $440.
Each row is costed as an order of its own size: the plan is scaled as the set of 6 is above, so grams
and minutes go in proportion and each color takes ⌈coasters ÷ 4⌉ beds.

| Row | Price each | Order | Cost each | Margin each | To cover | Revenue / margin / profit a month |
|---|---|---|---|---|---|---|
| single | 150 | 1 | 72.98 | 120 − 1 − 72.98 = 46.02 | 22 | $6,000.00 / $1,840.73 / $840.73 |
| set of 4 | 150 × 0.8 = 120 | 4 | 68.48 | 96 − 0.25 − 68.48 = 27.27 | 37 | $4,800.00 / $1,090.73 / $90.73 |
| set of 6 | 120 × 0.85 = 102 | 6 | 68.32 | 13.12 | 77 | $4,080.00 / $524.73 / −$475.27 |
| gift order | 120 × 0.9 = 108 | 8 | 67.98 | 18.29 | 55 | $4,320.00 / $731.73 / −$268.27 |
| café order | 120 × 0.8 = 96 | 24 | 67.65 | 9.11 | 110 | $3,840.00 / $364.40 / −$635.60 |
| wholesale | 120 × 0.5 = 60 | 24 | 67.65 | 48 − 0.04 − 67.65 = −19.69 | never, below break-even | $2,400.00 / −$787.60 / −$1,787.60 |

**Each order is costed at its own size.** For a single coaster the plan scales by ¼: 29.315 g, 87.775
minutes, still 5 beds, so 5 warm-ups. Printer hours (87.775 + 30) ÷ 60 = 1.9629; made
(29.315 + 1.9629 + 1.9629) ÷ 0.5 = 66.48; labor 15 ÷ 60 × $10 = $2.50; cost 66.48 + 2.50 + 4 = $72.98.
For 8, the plan scales by 2 with 10 beds: made (234.52 + 2 × 12.7033) ÷ 0.5 = 519.85, plus $20 labor
and $4, so 543.85 ÷ 8 = $67.98. For 24, it scales by 6 with 30 beds: made (703.56 + 2 × 38.11) ÷ 0.5 =
1,559.56, plus $60 and $4, so 1,623.56 ÷ 24 = $67.65.

**Wholesale** keeps the same $1 fixed fee but takes the wholesale fee percent, which is 0.2 here, the
same as the shop fee, so a later fixture can move it apart.

Every amount here is floor, because no PLA Matte print has been timed.
