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
