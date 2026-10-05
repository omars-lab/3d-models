# Buyers and rules for simulate-buyers

Read this file on every run, before writing a thought. It is kept apart from SKILL.md so the
buyers can get sharper without the skill changing. `buyers.py check` reads the buyer ids from the
table below, so a buyer added here is one every sweep must then cover.

**These are made-up people.** Every thought is Claude imagining what such a person might think on
seeing the coaster at a price. Nobody was asked. A sweep is good for finding which kinds of buyer
a price loses, and for the words they might use. It is not evidence of what anyone pays, and
nothing here may be quoted as customer feedback. Say so wherever a sweep is shown.

## The six buyers

They differ first on how they think about price, which is what a sweep tests.

| Id | Name | Weighs the price against | Cares about | Put off by |
|---|---|---|---|---|
| `bargain-hunter` | Price-conscious shopper | A plain printed coaster at about $5 on Etsy, or a four-pack of cork from a big store | A fair deal; pays a little more for something clearly nicer | Paying for a story; anything past about twice the cheap option |
| `gift-buyer` | Gift buyer | The whole present: a set of four, boxed, for someone they like, about $25 to $50 | Looks finished and special when unwrapped | A price so low the gift feels like a token; one so high it outgrows a casual gift |
| `design-lover` | Design and pattern lover | A ceramic tile, an art print, a museum-shop object | The geometry, the loose pieces set in like tilework, colors that feel chosen | A price that says mass-made; plastic passed off as more than it is |
| `cafe-owner` | Café owner buying two dozen | The coaster times 24, against what a coffee earns; losses to theft and wear | Survives wiping, looks good as a set, cheap to replace | A unit price above a few dollars; pieces that could pop out; a frame that shows stains |
| `coffee-enthusiast` | Home-coffee enthusiast | Beans at $20 a bag and a grinder at $300: a coaster is a small accessory | Fits the coffee bar; a cup sits steady on it | Wobble or loose pieces under a wet cup; a gimmick |
| `impulse-browser` | Impulse browser, at a market stall or scrolling | A line of about $10: under it, an easy yes; over it, they think and leave | Catches the eye now | Having to think about it |

## What a buyer is shown

The coaster's picture (the theme's SVG, rendered and opened), its size and build in one plain
line (the sweep's `shown`), and one price per coaster. Each sweep writes `shown` down, so the
thoughts can be read against what the buyer saw.

## The verdicts

| Verdict | Means | Counts in the curve as |
|---|---|---|
| `buy` | They would buy at this price | 1 |
| `maybe` | They hesitate: a sale, a closer photo, or a review could tip it | ½ |
| `walk` | Too much for what they think it is; they leave | 0 |
| `too-cheap` | So cheap they doubt it, and leave | 0 |

The ½ for a maybe is a made-up weight, not a measured one. The page says so beside the curve.

## How to write a thought

1. **Look at the picture first.** A thought names what in the picture or the price drove it: the
   white frame, the blues, the star, the loose pieces. It is not a general opinion.
2. **One line in the buyer's own voice**, first person, as it would go through their head: at most
   240 characters. Raw is the point. "Ten dollars for one coaster? It's plastic." is a thought;
   "the price point exceeds this segment's willingness to pay" is not.
3. **Let it change as the price moves.** A buyer's thoughts at $8 and at $12 should not be the same
   sentence with the number swapped. Say what tips them: the set total, a comparison they reach
   for, a doubt the price raises.
4. **Keep the buyers apart.** A sweep where all six walk at the same price is a sign the buyers
   were blurred, not a finding.
5. **Each buyer has one window.** Going up the prices, a `maybe` may become a `buy` (the lower
   price felt a bit cheap), but once a buyer cools they never warm again, and a `walk` is never
   followed by anything warmer. A price so low it puts them off is `too-cheap`, not `walk`, and it
   can only come below their first `buy` or `maybe`. `buyers.py check` refuses a sweep that breaks
   this: a buyer who walks at $10 and buys at $15 is a slip, not a taste.
6. **The overall line** is one sentence: where the buyers split, and who holds on longest. It is
   not an average; the page draws the curve.
