---
status: draft
date: 2026-10-04
produced-by: Claude (Opus 5.5), from a read of this repo at origin/master 214c818, of bikar at origin/main 6629f24, and of the private 3d-model-hub checkout on 2026-10-04
---

# Orders: type in what someone wants, and get the plates, the time, the filament and the price

This design turns one typed order — which coaster, what size, which colors, how many, by when —
into everything needed to make and sell it: the plates[^plate] to print, the time on the printer,
the filament[^filament] by color, what to buy, and a price. Today all of that is worked out by hand, and
the price and the stock of filament are not worked out anywhere. It proposes one command that
does the working out, and three pages over one private store that show it: a plan, a price and
the shelf of filament. It also writes down a set of made-up orders that every part must get right
before it ships (§9.6), and a view that lays the ways of setting a price side by side (§9.7).

> Status: draft, 2026-10-04. Nothing here is built. Omar, who designs, prints and sells the
> coasters, has five calls to make, in
> [§10](#10-open-calls-for-omar). No price is worked out here on purpose: every price setting is
> still empty. Four have looked-up references to confirm (§9.3), five come only from Omar's own
> records, and three are his to choose.

## 1. The problem: an order is five questions, answered by hand

Omar asked, on 2026-10-04: "if I order different prints, will I know how much material i will
need? how much time it will take to make? how many plates we will need to print? how much I
should price/sell things for?"

Someone wants four of the gBV coaster[^gbv] in the Ice to navy theme[^theme], by a date. Before
saying yes, Omar needs five answers: how much
plastic, how long on the printer, how many plates, what to charge, and whether the colors
are on the shelf. Today each one is worked out by hand, from different places, and two of them
have nowhere to be worked out at all.

| Question | What exists today | What is missing |
|---|---|---|
| **Material** | The slicer's[^slicer] filament length for one plate, turned into grams by `bambu validate sliced` (the bambu CLI[^bambu]). A designed, unbuilt "live estimates" panel that adds grams piece by piece ([plate-builder §6](../printing/plate-builder-design.md#6-the-live-estimates-panel--grams-exact-time-a-floor)). The printer has not been seen to report the grams a print used (unconfirmed) | Grams per color for a number of coasters |
| **Time** | Sliced minutes for one plate. Print logs[^printlog] that show how long a plate really took: of the five in this repo, three are one-color PLA[^pla] Basic plates watched from start to finish, sheets-04g[^sheets04g], [sheets-04c](../plates/print-logs/sheets-04c.md) and [phones-02](../plates/print-logs/phones-02.md)[^phones] | A total for an order, corrected by what prints really take |
| **Plates** | One plate recipe[^recipe] per plate, written by hand. A proposed command that writes one recipe per color from a design ([piece colors[^piececolors] §4.5](infill-color-ux-design.md#45-export-to-plate-recipes)), not built | "Four coasters in five colors" turned into a list of plates |
| **Price** | Nothing | Everything: no cost, no price, no record of what was charged |
| **Inventory** | `bambu filament` reads the four loaded trays[^tray] and, for a tagged spool[^spool], the percent left. The [color catalog](themes/bambu-color-catalog.md) says which colors are owned | Grams on the shelf, what open orders already need, what to buy |

**Plainly: there is no order, no price and no inventory model anywhere in these repos today.**
The Coaster Lab[^lab], where a coaster is designed, knows nothing about grams or money. Its share
link[^sharelink] records the design and nothing about how many or for whom.

## 2. Why it matters now

Three things changed on 2026-10-04, and each one makes the hand method worse:

- **One color per plate.** Omar dropped plates that switch colors mid-print, because phones-01[^phones]
  took about 62 minutes against 22 sliced and lost about a third of its plastic to the switches
  ([phones-02](../plates/phones-02.md#cost-and-risk)). The color is now picked when the plate is
  sent. So a coaster in five colors is five plates, five sends and five warm-ups[^warmup]. Nobody can see
  that from a picture of a coaster.
- **Themes need colors we do not own.** The gBV themes page lists themes built from the whole
  range of Bambu Lab, the maker of our printer and its filament. Ice to navy uses five PLA Matte colors and none of them is on the shelf. An order
  in that theme starts with a purchase.
- **A spool is bought whole, but an order uses grams.** Four coasters use about 108 g (from a PLA
  Basic slice), and buying
  their colors means five whole spools. Without a record of what is left, the second order in the
  same theme looks like it needs five more.

And one thing makes a better method possible: there are now three one-color prints where both the
sliced time and the real time are known, so the slicer's estimate can be corrected instead of
trusted.

Without this, a quote is a guess. A low guess loses money on warm-ups and spools; a high one loses
the order.

## 3. The idea: an order is a recipe card scaled for guests

A recipe says what one serving needs. Tell it eight guests, and it gives the shopping list, the
oven time and the cost per plate, and you check the pantry before you shop. An order[^order] works
the same way. It is **the only thing anyone types**: which coaster, which size, which colors, how
many, by when. Everything else is worked out from it and worked out again whenever it changes:

```mermaid
flowchart LR
  order["order (what, how many, colors, due)"] --> pieces["pieces, counted by color"]
  pieces --> plates["plates, one color each"]
  plates --> slice["slice: minutes and grams per plate"]
  ratio["ratio from past prints"] --> time["time, corrected"]
  slice --> time
  slice --> grams["grams by color"]
  grams --> check["filament check against inventory"]
  shelf["inventory: spools on hand"] --> check
  check --> buy["buy list"]
  grams --> cost["cost"]
  time --> cost
  cost --> price["price"]
  market["what similar coasters sell for"] -.->|"shown beside, never sets it"| price
```

**In the diagram:** order[^order]; plate[^plate]; slice[^slicer]; ratio[^ratio];
inventory[^inventory]; buy list[^buylist]; price[^price].

Two rules follow. **Nothing downstream is typed**: a page that shows a plate count or a price
has worked it out, and says from what. **A number nobody has measured or looked up is shown as
missing**, never filled with a guess. An estimate is labeled "estimate", a looked-up range is
shown as a range with its source, and neither is ever shown as measured. The pricing page in §7
has no prices in it today for exactly that reason.

## 4. A worked example: four gBV coasters in Ice to navy

| Step | What comes out | From |
|---|---|---|
| The order | 4 × gBV at 112.5 mm, strap[^strap] 3.75, height 4.4, round 1.25, Ice to navy | typed |
| Pieces | 4 frames and 164 pieces: 4 middles, 40 kites, 40 hexes, 40 stars, 40 outers (the five groups[^palette]) | 4 × the 1 + 41 that sheets-04g prints |
| Colors | Frame ivory white; middle ice blue; kites sky blue; hexes marine blue; stars and outers dark blue | the theme |
| Plates | 5, one per color, each one bed[^bed] if the pieces fit (the packer[^packer] checks) | one color per plate |
| Grams | about 108 g | 4 × 27 g |
| Sliced minutes | 344, from a PLA Basic slice, standing in until the Matte re-slice | 4 × 86 |
| Corrected minutes | none yet: no Matte plate has been timed. Once the Matte slices exist, the page shows them alone, marked "floor" (the least the print can take), with 5 plates' warm-ups not timed. PLA Basic's ratio would give about 388, and the page names it as not used | the ratio rule, §9.1 step 4 |
| Filament check | none of the five colors on hand | the loaded trays are pink, blue, black, green |
| Buy list | 5 spools of PLA Matte, by color code[^code]: 11100, 11601, 11603, 11600, 11602 | what the shelf is short of, rounded up to whole spools |
| Price | not yet: every setting is empty; four have looked-up references to confirm, five come only from Omar's own records and three are his to choose | §9.3 |

Two things this example shows that a single plate does not. The split of the 108 g by color is
an estimate, from each group's share of the plastic, until each color's plate is sliced: the
frames are most of the plastic (about 62 of the 108 g, by the [gBV themes](themes/gbv-themes.md#ice-to-navy)
split), so the ivory spool does most of the work. And five spools bought for 108 g leave most of five spools on the shelf, so
the order should be charged for its grams, not for the spools, and the shelf should remember the
rest.

**Batching.** If a second open order also wants dark blue, its stars and outers ride on the same
dark blue plate while it fits the bed. Fewer plates, fewer warm-ups, fewer sends.

## 5. Context: who uses it and what it touches

```mermaid
flowchart LR
  subgraph people["people"]
    customer(["customer"])
    owner(["owner (designs, sells)"])
    operator(["print operator"])
  end
  subgraph newsys["the order system (all new)"]
    pages["Orders tab in the hub: Plan, Price, Inventory"]
    store["order, shelf and price store"]
    planner["order planner"]
  end
  lab["Coaster Lab (+ one new button: Add to order)"]
  printer["X2D printer"]
  seller["filament seller"]
  customer -->|"designs a coaster, sends the owner its share link"| lab
  owner -->|"Add to order: the share link"| pages
  owner -->|"quantity, due date, price inputs"| pages
  pages --- store
  store -->|"order file"| planner
  planner -->|"plates, minutes, grams by color"| store
  planner -->|"plate recipes"| operator
  operator -->|"sends a plate, color picked at the send"| printer
  printer -->|"finished row, through the print monitor"| store
  pages -->|"buy list"| seller
```

**In the diagram:** Coaster Lab[^lab]; share link[^sharelink]; hub[^hub]; order planner[^planner];
plate recipe[^recipe]; X2D[^x2d]; print monitor[^monitor]; buy list[^buylist].

Everything inside the box is new; the Lab gains one button; the printer and the people are as
they are today. Today the owner and the print operator are the same person, Omar. They are drawn
apart because they do different things at different times. The customer never touches the hub
or the planner: the hub is private, so a customer designs in the Lab and sends the owner the
share link, and the owner adds it to an order.

## 6. Use cases

Each is an actor doing something. "New" means nothing does it today; "impacted" means an existing
step changes.

1. **A customer configures a coaster and sends the owner its link; the owner adds it to an
   order** (new). The design is made in the Coaster Lab as today. On the owner's own devices a
   new Add to order button hands the share link to the hub. A customer who presses it sees "Send
   this link to the shop to order" with the link to copy, because their device cannot reach the
   private hub.
2. **The owner plans an order** (new): pieces, plates, minutes and grams by color.
3. **The owner checks an order against the shelf and gets a buy list** (new).
4. **The owner prices an order** (new): the cost built up line by line, the lowest price that
   breaks even, a suggested price, and what similar coasters sell for.
5. **The owner batches open orders by color** (new): plates of the same color merge.
6. **The print operator sends an order's plates** (impacted): the recipes now come from the plan,
   and each send still needs its own yes.
7. **The print operator closes a print against the shelf** (new): the plate's grams come off the
   spool that fed it.
8. **The owner records a spool bought or opened** (new).
9. **The owner compares ways of setting a price** (new): cost-plus, the market, a premium, by
   finish, sets, a custom theme, a launch price, each with its margin per coaster (§9.7).
10. **A developer runs the simulated orders** (new): every made-up order's plan, shelf, price and
    pages checked against what they must show, before a change merges (§9.6).

```mermaid
flowchart LR
  c(["customer"]) --> uc1["configure a coaster, hand over its link (new)"]
  o(["owner"]) --> uc1b["add a design to an order (new)"]
  uc1 -.->|"the share link"| uc1b
  o --> uc2["plan an order (new)"]
  o --> uc3["check the shelf, get a buy list (new)"]
  o --> uc4["price an order (new)"]
  o --> uc5["batch orders by color (new)"]
  o --> uc8["record a spool (new)"]
  o --> uc9["compare ways to set a price (new)"]
  d(["developer"]) --> uc10["run the simulated orders (new)"]
  op(["print operator"]) --> uc6["send an order's plates (impacted)"]
  op --> uc7["close a print against the shelf (new)"]
```

**In the diagram:** order[^order]; spool[^spool]; buy list[^buylist]; plate[^plate].

## 7. What a user sees

A command, three pages and a button, with one store behind them. Where the store and the three pages live is call 1 in §10;
the pictures assume the recommended answer, the hub.

| Surface | Where | What is new |
|---|---|---|
| `bambu order plan <order.yaml>` | the command line, this repo | A new command. Prints the plan; with `--write`, writes the plate recipes |
| **Plan** page | the hub, a new Orders tab | A new page: the order, its pieces, its plates, time, material, filament check. Buttons: Write the plate recipes, Reserve filament, Price this order |
| **Price** page | the hub, Orders tab | A new page: every price input with where it comes from, the cost built up, the price, the market band. A second view, Scenarios, lays out seven ways of setting the price (§9.7) |
| **Inventory** page | the hub, Orders tab | A new page: spools on hand, what prints used, what open orders hold, the buy list. Buttons: Read the trays, Mark the buy list ordered, Add a spool by hand |
| `make validate-orders` | the command line, this repo; a target of the same name in the hub | A new check over the simulated orders (§9.6), called by `make validate` |
| **Add to order** | the Coaster Lab, beside the share button | One new button. On a device that can reach the private hub, it opens the hub with the share link filled in. Anywhere else it shows "Send this link to the shop to order" and the link to copy |

The three pages are drawn below as mockups, not built pages, in the Coaster Lab's own colors and
classes ([mockup.css](order-driven-lab-media/mockup.css), copied from the
[Piece colors mockup](infill-color-ux-media/piece-colors-mockup.html)) and screenshotted with
headless Chrome. Numbers with a dotted underline are stand-ins or estimates. First the Plan page:

![Mockup of the order plan page: an order for four gBV coasters in Ice to navy, its pieces by color, five one-color plates with estimated minutes and grams and an empty corrected column (no Matte plate timed yet), the total tagged "Basic stand-in", a filament check showing none of the five colors on hand, and the time and material totals](order-driven-lab-media/order-plan-mockup.png)

[order-plan-mockup.html](order-driven-lab-media/order-plan-mockup.html). What is real and what
stands in:

| Part of the picture | Real or stand-in |
|---|---|
| The theme Ice to navy and its five colors, hex color values and codes | **Real**, [the gBV themes](themes/gbv-themes.md) and the [color catalog](themes/bambu-color-catalog.md) |
| The groups and counts per coaster (frame, Middle 1, Kite 10, Hex 10, Star 10, Outer 10) | **Real**, the pieces [sheets-04g](../plates/sheets-04g.md) prints |
| 344 sliced minutes for four coasters | **Real for PLA Basic**, four times sheets-04g's local slice (86 minutes); a stand-in for Matte until the Matte re-slice (§9.1), so not yet a floor for this order |
| 108 g for four coasters | **Real for PLA Basic**, four times sheets-04g's 27 g; a stand-in for Matte until the Matte re-slice (§9.1) |
| The ratio 1.13, shown as not used | **Real** for PLA Basic: three one-color prints, 1.08, 1.13 and 1.14, pooled as total watched over total sliced minutes (§12). Not used for this Matte order, so the corrected column is empty and the total is tagged "Basic stand-in" |
| None of the five colors on hand | **Real**: the four loaded trays are pink, blue, black and green |
| The split of minutes and grams by color | Estimates, labeled so: the 344 minutes and 108 g shared out by the [gBV themes](themes/gbv-themes.md#ice-to-navy) split, until each color's plate is sliced |
| The bed count per color | Stand-in. It comes from packing each color's plate, which nothing does yet |
| The order number, the due date, the `theme=` end of the link | Stand-ins. The share link carries the colors, one `color.<Name>=<code or hex>` key per group, but has no `theme=` key, so that end stands in for those keys ([storefront design §12.1](../storefront/shopify-storefront-design.md#121-the-share-link)) |

Then the Price page and the Inventory page:

![Mockup of the pricing page: twelve settings, each marked looked up, your bill, your records, or your choice, with the research's reference beside it; the cost built up line by line with empty amounts; the break-even and suggested price formulas with a markup; an empty price; the market band from the research; and 108 g charged against five whole spools bought](order-driven-lab-media/pricing-mockup.png)

[pricing-mockup.html](order-driven-lab-media/pricing-mockup.html). Real: 5 plates, 5 spools
and the shape of the formula. Stand-ins until the Matte re-slice: 108 g and about 5¾ hours, both
from the PLA Basic slice. The references on the left are the consolidated research's (§9.3), not
values, and not yet confirmed on our orders. The page shows no price because every setting is
still empty: four have looked-up references to confirm, five come only from Omar's own records,
and three are his to choose.

![Mockup of the inventory page: four spools on hand with tray and percent left, two finished prints as examples (sheets-04g, phones-02) with their grams, a reorder level marked your choice, the five colors order 0007 needs and is short of, and a buy list of five PLA Matte spools](order-driven-lab-media/inventory-mockup.png)

[inventory-mockup.html](order-driven-lab-media/inventory-mockup.html). Real: the four owned
colors, the two "used by prints" rows (sheets-04g, 27 g of green; phones-02, 3.5 g of pink, each
from its slice), and the five colors on the buy list with their codes. Estimates: the grams by
color the order needs are the gBV themes split (§4), until each plate is sliced. Stand-ins: tray
slots, percent left and the grams that follow from it.

## 8. The pieces and where they live

Three repos are involved. **bikar**[^bikar] owns the Coaster Lab. **This repo** owns the planning:
the catalog of designs, the plate recipes, the measured ratios, and the new `order plan` command,
all public. **The hub** owns everything private: orders and customers, the shelf, price inputs
and quotes.

```mermaid
flowchart TB
  subgraph bikar["bikar (public): packages/lab"]
    labpage["Coaster Lab page"]
    link["share link"]
    addbtn["Add to order button (new)"]
  end
  subgraph models["3d-models (public): tools/bambu and docs"]
    plan["order plan command (new)"]
    bycolor["plates by-color writer (proposed, piece colors phase 1)"]
    compose["slice compose (reused)"]
    vsliced["validate sliced: minutes, grams (reused)"]
    ratios["ratios from print logs (new, read from reused logs)"]
    fil["bambu filament: trays (reused)"]
    monitor["print monitor: finished row (reused)"]
    send["print send: send record (new)"]
  end
  subgraph hubrepo["3d-model-hub (private): server and web"]
    store["order, shelf and price store (new)"]
    adapter["CLI adapter (reused)"]
    pricer["price breakdown (new)"]
    closer["close a print: finished row + send record (new)"]
    pages["Orders tab: Plan, Price, Inventory (new)"]
  end
  labpage --> link --> addbtn
  addbtn -->|"share link"| pages
  pages --> store
  store -->|"order file, outside git"| adapter
  adapter -->|"runs"| plan
  plan --> bycolor --> compose --> vsliced
  ratios --> plan
  plan -->|"plan as JSON"| adapter
  adapter -->|"runs"| fil
  adapter -->|"plan as JSON"| pricer
  store -->|"price inputs"| pricer
  pricer --> pages
  monitor -->|"finished row"| closer
  send -->|"plate, color, tray"| closer
  closer -->|"grams off the spool"| store
```

**In the diagram:** Coaster Lab[^lab]; share link[^sharelink]; order planner[^planner];
plate recipe[^recipe]; ratio[^ratio]; tray[^tray]; print monitor[^monitor]; hub[^hub];
CLI adapter[^adapter]; price[^price].

**One recipe writer.** The planner does not write recipes itself. It counts pieces by color across
the order, then hands each color to the `plates by-color` writer, so a recipe has one writer
whether it came from one coaster or an order of twenty. As piece colors §4.5 designs it,
`plates by-color` takes one design and writes for the fixed PLA Basic profile. Phase 1 here
extends it: many lines with counts, colors from the order file, and each line's filament profile.
That is why phase 1 here and piece colors phase 1 are built together (§11).

**The data it touches**, drawn at type level because the set is small. Eight types are new; three
already exist and keep their format: the planner writes recipes in the existing format, and the
print log keeps its rows. The new send record is what lets a finished row find its spool.

```mermaid
classDiagram
  class Order {
    <<new>>
    id
    customer_ref
    due
    status
    lines
  }
  class OrderLine {
    <<new>>
    frame_construction
    frame_color
    pieces_construction
    params
    colors_by_group
    count
    share_link
  }
  class PlatePlan {
    <<new>>
    color
    items
    beds
    sliced_min
    ratio
    corrected_min
    grams
    source
  }
  class Spool {
    <<new>>
    line
    color_code
    start_g
    used_g
    opened
    where
  }
  class Reservation {
    <<new>>
    order_id
    color_code
    grams
  }
  class PriceInputs {
    <<new>>
    settings
    markup
    sources
  }
  class SendRecord {
    <<new>>
    plate
    color
    tray
    sent_at
  }
  class PriceBreakdown {
    <<new>>
    lines
    cost
    break_even
    suggested
    market_band
  }
  class PlateRecipe {
    <<reused>>
  }
  class SliceResult {
    <<reused>>
  }
  class PrintLogRow {
    <<reused>>
  }
  Order "1" *-- "many" OrderLine
  Order "1" --> "many" PlatePlan : plans
  PlatePlan --> PlateRecipe : writes, via plates by-color
  PlatePlan --> SliceResult : reads minutes and grams
  PlatePlan --> PrintLogRow : reads the ratio
  Order "1" --> "many" Reservation : holds
  Reservation --> Spool : against
  PrintLogRow --> SendRecord : finished row closes the send
  SendRecord --> SliceResult : grams to subtract
  SendRecord --> Spool : subtracts grams from
  PriceBreakdown --> PlatePlan : reads
  PriceBreakdown --> PriceInputs : reads
```

| Type | Where | Status | Why it is touched |
|---|---|---|---|
| Order | hub store | new | The one input; it holds the customer only as a reference to a private record |
| OrderLine | hub store, copied into the order file | new | One design at one size in one coloring, times a count; carries the share link it came from |
| PlatePlan | worked out by the planner, never stored by hand | new | One plate of one color: what is on it, beds, sliced and corrected minutes, grams, and where each number came from |
| Spool | hub store | new | The shelf: what was bought, what is left |
| Reservation | hub store | new | Grams an open order will use, so two orders cannot count the same spool |
| PriceInputs | hub store (private ones); this repo (public ones) | new | Every setting the price formula needs, each with its source |
| SendRecord | this repo, written by `bambu print send` beside the print log | new | Which plate went out in which color from which tray, so the finished row knows which spool to subtract from |
| PriceBreakdown | worked out by the hub's pricer from the plan JSON and PriceInputs, stored with a quote | new | The cost line by line and the price, so a quote can be explained later |
| PlateRecipe | this repo, plate YAML | reused | What the planner's writer produces, in the format the slicing step already reads |
| SliceResult | this repo, `bambu validate sliced` | reused | The source of minutes and grams |
| PrintLogRow | this repo, print logs | reused | The source of real minutes (the ratio) and of the "finished" event that closes a print against the shelf |

The buy list is not a type: it is worked out each time from Reservation and Spool.

## 9. How it works

### 9.1 Planning an order

In plain words: count the pieces, sort them by color, put each color on as few beds as fit, slice
each, then correct the time.

The order file the planner reads is plain YAML. It names no person:

```yaml
# an order file, written by the hub into its private store, never into this repo
id: "0007"
due: 2026-10-18
lines:
  - count: 4
    frame:                      # the coaster itself, one per count
      construction: bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-coaster.bkr
      params: { size: 112.5, strap: 3.75, height: 4.4, round: 1.25 }
      color: { line: PLA Matte, code: "11100" }
    pieces:                     # the loose pieces that drop into it
      construction: bikar:patterns/Constructions/gBV_JTt3Kxk-minimal-pieces.bkr
      params: { size: 112.5, strap: 3.75, height: 4.4, gap: 0 }
      colors:                   # palette name → a color from the catalog
        Middle: { line: PLA Matte, code: "11601" }
        Kite: { line: PLA Matte, code: "11603" }
        Hex: { line: PLA Matte, code: "11600" }
        Star: { line: PLA Matte, code: "11602" }
        Outer: { line: PLA Matte, code: "11602" }
```

1. **Pieces.** Each line has a count and two constructions[^construction], the same two
   [sheets-04g](../plates/sheets-04g.yaml) prints: the frame, one per count, and the loose
   pieces, each group times the count. The pieces' groups are the palette names[^palette] the
   design already uses for `--piece` (the flag that picks one group of pieces,
   [loose pieces](loose-pieces-design.md)), so nothing is renamed. "Frame" is the order file's
   name for the coaster construction, not a palette name: the pieces file's own frame is only
   the host its pieces are cut from, and is never printed.
2. **Plates.** Pieces are grouped by color across every line, and, when batching, across every
   open order. Each color goes to the `plates by-color` writer, which writes one recipe per color
   and lets the packer spread a color over two beds when it does not fit one (the X2D bed is
   256 × 256 mm). A frame rides with pieces of its own color when they share one.
3. **Slice.** Each recipe is sliced. Minutes and grams come from the slice. Until a recipe is
   sliced, the page shows an estimate scaled from the pieces' volume, labeled "estimate", the way
   plate-builder §6 adds grams.
4. **Correct the time.** Sliced minutes are a floor. The planner multiplies by the ratio of real
   to sliced minutes from past prints with the same printer, process and filament profile, and
   shows how many prints the ratio rests on. With no matching print, it shows the sliced minutes
   alone, marked "floor", and names the nearest ratio it did not use and why. Warm-ups are
   counted, not timed: whether a slice's minutes include its warm-up is not known. The gBV
   themes page assumes they do (it calls them start-ups), so 4 × 86 would hold four and five
   plates add one more. Until a warm-up is timed, the page says "5 plates, warm-ups not timed".
   The price's warm-up setting (§9.3) is only the part a slice leaves out, so it is zero if a
   timed print shows the slice already includes it, and nothing is counted twice.

**Grams depend on the filament.** The slice writes its own grams, from its filament profile's
density (PLA Basic 1.26 g/cm³, Matte 1.32), and `validate sliced` and the planner both read them
from one place (`3d-models:tools/bambu/src/slice-numbers.ts:L5 "Grams: the slice writes its own"`).
An older headless slice wrote 0 g because the X2D profile then carried no density; for those, and
when `--density` is given, grams are worked out from the filament length and labeled derived, never
passed off as the slice's. Each plate is sliced with its own color's profile, so a Matte order's
minutes and grams are Matte numbers: phase 1's real slices of §4's order give 5 plates, 351 sliced
minutes and 117 g, where §4's Basic stand-ins said 344 and 108.

### 9.2 The shelf: reserving, buying, closing a print

In plain words: the shelf is a list of spools and how much is left. An open order holds the grams
it will use. What is short goes on the buy list. When a print finishes, its grams come off the
spool that fed it.

```mermaid
flowchart LR
  bought["spool bought or opened"] -->|"start grams"| onhand["on hand"]
  finished["print finished, failed or stopped (its sent row names the tray)"] -->|"minus the slice's grams"| onhand
  trays["tray tags: percent left"] -.->|"shown beside, owner corrects"| onhand
  orders["open orders' plans"] -->|"planned grams by color"| held["held"]
  onhand --> avail["available = on hand − held"]
  held --> avail
  avail -->|"below zero"| buy["buy list, whole spools"]
```

**In the diagram:** spool[^spool]; inventory[^inventory]; tray[^tray]; buy list[^buylist].

- **On hand** for a spool is its starting grams minus what prints used. A tagged spool also
  reports a percent left through `bambu filament`; the page shows both and, when they disagree,
  the owner corrects the book by hand. No tolerance is set: there is no measurement to set it
  from.
- **Held** is the sum of open orders' planned grams for that color. **Available** is on hand
  minus held.
- **Buy list**: every color where available is below zero, rounded up to whole spools, with the
  line and code from the catalog. Whether to buy before a level is reached (a reorder level) is
  the owner's choice, so phase 2 lists only what is short and sets no level. A color only a
  closed order needs is not listed. The note beside a buy comes from the palette's store notes
  (Silk Gold's "not on the US store").
- **Closing a print** happens on the print monitor's[^monitor] `finished` row. The grams are the slice's,
  because the X2D has not been seen to report what it used (the field is marked unconfirmed in the code). A
  failed print still used its plastic and counts, as its full slice grams: an overcount for a print stopped early, until the owner corrects the book. A
  `stopped` row counts the same way, for the same reason. A `lost` row closes nothing: the
  printer stopped answering, and the print may still be going. The tray comes from the send record: the color
  `bambu print send --color` used to pick the tray, written beside the print log at the send.
- **The send record is a row in the print log.** Phase 2 adds a `sent` row, the first row of a
  send, written by `print_monitor.py <plate> --sent <hex> <tray> <grams>` (one triple per
  filament). Its last column reads `fed #00ae42 from AMS 1 slot 4, 27.28 g by the slice`, with
  `; ` between trays. The log stays append-only (the plates gate's P10), so the record cannot be
  edited after the print. The next `finished`, `failed` or `stopped` row closes it. A second
  `sent` row before a close leaves the first send listed as not closed. A finished, failed or
  stopped row with no `sent` row before it is listed as not counted, since it names no tray and
  no grams. Every print before phase 2 is one of these, so the book starts from the spools'
  start grams, not from a guess. Making `print send` write the row itself is the next piece of
  work.
- **The tray's color names the spool.** A spool's color is its line and code; the tray reports a
  hex. A send's hex is matched to the spools whose catalog color has that hex. When two colors
  share a hex (Jade White and Ivory White are both `#ffffff`), the spool's `tray:` must say which
  one was loaded there. Without it the grams are listed as unmatched and nothing is taken off, so
  a guess never moves the book. Among spools of one color, the one in that tray is used, else the
  first listed.
- **A finished print stops holding.** When a plate an open order holds prints to the end, its
  grams come off the spool and stop being held, so they are not counted twice. A failed print
  keeps its hold, because the reprint still needs the plastic.

**The shelf file** lists the spools and the orders. It points at each order's plan rather than
copying it:

```yaml
spool_grams: 1000              # a whole spool, for the buy list
spool_grams_by_line: {}        # e.g. { "PLA Silk": 500 } where a line sells another size
spools:
  - { id: navy-end, line: PLA Matte, code: "11602", start_grams: 40, tag_percent: 4,
      tray: "AMS 1 slot 2", corrections: [{ date: 2026-10-05, grams: -4, why: weighed }] }
orders:
  - { plan: orders/FIXTURE-1.plan.json, status: open }   # bambu order plan --json, saved
logs: ../../docs/design/plates/print-logs                 # optional; the repo's print logs by default
```

`bambu shelf show [shelf.yaml]` prints each spool's grams left, each color's on hand, held and
available with the plates holding it, the buy list, and how each print in the logs was counted
(`--json` gives the same as data). Where the shelf lives is call 1, still open. **Assumed until
then:** a gitignored local file, `.bambu/shelf/shelf.yaml`, the command's default. It keeps
orders out of this public repo (§9.4). Moving the shelf into the hub later changes where the file
is read from, not what it holds.

### 9.3 The price

In plain words: add up what the order costs to make, divide out the selling fee to find the lowest
price that breaks even, add a markup for the suggested price, and show what similar coasters sell
for beside it.

Every name in the formula is a setting with a source, never a number typed in as settled. The
order's grams, print minutes and plates come from the plan (§9.1), so how many coasters fit on a
plate is counted by the planner, not typed; the price per coaster is the order's price over its
coasters.

```text
printer hours = print minutes ÷ 60 + plates × warm-up minutes ÷ 60
material      = Σ over colors ( grams × price per gram of that line )
power         = printer hours × printer watts ÷ 1000 × electricity rate
wear          = printer hours × printer price ÷ payback hours
made          = (material + power + wear) ÷ good-plate share
cost          = made + hands-on minutes ÷ 60 × labor rate + packaging
break-even    = (cost + fixed fee) ÷ (1 − fee percent)
suggested     = break-even × (1 + markup)
```

**Print minutes** are the corrected minutes when a ratio matches. With no matching ratio, they are
the sliced minutes marked "floor", and every amount built on them is marked "floor" too, as the
least the order can cost.

A **markup** is added on top of the break-even price (break-even × (1 + markup)); a margin is a share of the selling
price. The research keeps the two apart, and this formula uses a markup.

The public inputs were looked up on 2026-10-04 in the
[consolidated pricing research](../../research/2026-10-04-coaster-pricing.md), which checks two
independent passes ([A](../../research/2026-10-04-coaster-pricing-a.md),
[B](../../research/2026-10-04-coaster-pricing-b.md)) against their sources and is the one to act
on. Each value it gives is a starting point or a reference, not a settled value, so every one of
the twelve settings starts empty. Four have looked-up references Omar confirms or replaces: price
per gram, printer watts, printer price and the selling fee. Five come only from Omar's own
records: his electricity rate, warm-up minutes, the good-plate share, hands-on minutes and
packaging. Three are his to choose: payback hours, labor rate and markup. The market band is not
a setting; it is shown beside the price.

| Setting | What it is | What the research found | Where its value comes from |
|---|---|---|---|
| Price per gram, by line | What a spool costs, over its grams | PLA Basic and Matte $15.99 a refill (the same filament without the plastic reel) or $18.99 a spool; Silk+ the same, with refills in four colors only; Sparkle and Silk Multi-Color $24.99, spool only, no bulk discount. Bulk: 5% off at 2 items up to 30% at 10 ($11.19 a roll), called a sale with no end date; whether different lines count together was not tested | looked up; Omar's real receipts replace it |
| Printer watts | Power drawn while printing | 262 W: Bambu's 250 W steady state for PLA at 25 °C plus 12 W for the filament feeder. One owner saw about 170 W on PETG (a tougher plastic than PLA, which these coasters do not use). The 1100 W maximum only matters for sizing the circuit | looked up; a plug meter on one plate settles it |
| Electricity rate | What a kWh costs Omar | 18.31¢ is the US average for July 2026; of the three states read, Texas 15.88¢, New York 29.90¢, California 33.61¢ | Omar's own bill |
| Printer price | What the printer cost | $899 for the X2D combo (the printer with its automatic filament feeder), listed that day | looked up; what Omar actually paid replaces it |
| Payback hours | The printer hours the printer price is spread over | assumptions only: 2,000 h ($0.45 an hour; one forum member's assumption, for a different Bambu printer) or 4,380 h ($0.21 an hour; Prusa's calculator's 6 h a day over a 2-year life one researcher chose); no source measured an X2D's life | Omar's to choose |
| Warm-up minutes | The heat-up and checks before each plate's first layer that its sliced minutes leave out; zero if a timed print shows the slice already includes them | not found in the sources read | measured: a timed print |
| Good-plate share | The share of plates that come out good | starting guesses only: divide by 0.8, or add 30% of the material cost; both passes say measure it | measured: kept against failed plates in the print logs |
| Hands-on minutes | Clearing the plate, pressing pieces in, packing; unattended print time is not labor | reference points only, from other shops | measured: timed real orders. Likely the largest cost per coaster |
| Labor rate | What an hour of Omar's time is worth | not a lookup | Omar's to choose |
| Packaging | Box, insert, label, per order | not found in the sources read; one forum example lumps it with other costs | measured: the boxes Omar picks |
| Fee percent and fixed fee | What the selling channel takes | Etsy (an online marketplace for handmade goods): $0.20 a listing, 6.5% of item and shipping, 3% + $0.25 for payment on the whole order; about 11% of a $25 set with no shipping or tax. When an Offsite Ad (Etsy advertising the listing on other sites) brought the sale, 15% more under $10,000 a year of sales (12% at or above it), about 26% in all | looked up, Etsy only; per order |
| Markup | What is added on top of the break-even price | not a number: retail margins of 30 to 57% (as a markup, about 43% to 133%) are whole sectors and only a rough guide for a one-person shop | Omar's to choose, checked against the market band |
| Market band | What similar coasters are listed at | printed coasters about $5 each (median of 39 listings, one pass, not re-checked); printed Islamic sets $25 to $45 for 4 to 6 coasters, about $6.25 to $7.50 each, from 4 listings, three from one shop and all smaller than ours. Asking prices on one day's first page, not sales | looked up; repeat the search when setting a price |

The research puts one full coaster's plastic, power, wear and a failure allowance at about $0.98
to $1.37, before labor, packaging and fees; most of the spread is the payback hours. That is not
an input here, and it is small next to a $25 set: labor, fees and markup set the price.

The formula is cost-plus with a market check. Whether that is the method at all is call 2.

**Charged against spent.** The order is charged for its grams. The spools bought for it are cash
out, and what is left on them is shelf stock for the next order. The Price page shows both lines
so a big first purchase does not read as a loss on one order.

### 9.4 What may go in the public repo

This repo is public, so the line is drawn by what would hurt if read by anyone:

| Public, in this repo | Private, in the hub |
|---|---|
| The catalog, the designs, plate recipes, the planner | Customer names and contact details |
| Measured ratios and print logs | The list of orders, due dates, what each paid |
| Public prices: what a spool or a channel charges | Labor rate, markup, quotes |

An order file is written by the hub into its own private store and passed to the planner by path.
It never enters this repo, and it names the customer only by a reference the hub resolves.

### 9.5 Checks

**Validator:** the planner's numbers add up per plate, and no number is invented.

PASS: for the 4 × gBV order, the plates hold exactly 4 frames, 4 middles, 40 kites, 40 hexes, 40
stars and 40 outers, each on the plate of its color; every plate's minutes and grams equal its own
`bambu validate sliced` output; the order total equals the sum of its plates; a plate with no
matching print shows "floor" and no corrected minutes.

FAIL: one color's pieces spill onto a second bed and the plan still says one bed for that color,
with the right order total. The total cannot vouch for each plate, so the check compares beds and
items plate by plate, not the sum. Also FAIL: any price shown while one of its inputs is pending.

### 9.6 Simulated orders: the regression suite

In plain words: a set of made-up orders, each with the plan, the shelf and the price it must
produce, written down before the planner exists. Each phase is done when its part of the set comes
out right, and the pages are checked against the same numbers in a real browser.

**Where the files live.** Each fixture[^fixture] is one folder in this repo, under
`tools/bambu/test/fixtures/orders/<name>/`. Nothing in it is private: the order id reads
"FIXTURE", no customer is named, and no setting is a real price.

| File | What it holds | Checked from phase |
|---|---|---|
| `fixture.yaml` | The fixture's phase, its one-line about, and `wrong_must_say`: the words the check must give when it refuses the wrong plan | 1 |
| `order.yaml` | The order, in the format of §9.1 | 1 |
| `expected-plan.json` | The golden file[^golden] for the plan: each plate by color, the pieces on it by construction and group, its beds, minutes and grams, and the ratio used or "floor" | 1 |
| `wrong-plan.json` | The fixture's hard case, written out as a plan that is wrong in exactly that way. The check must reject it | 1 |
| `shelf.fixture.yaml`, `expected-shelf.json` | A starting shelf (§9.2's format), pointing at other fixtures' plans and, for fixture 5, at its own `print-logs/` whose rows close prints; then on hand, held, available and the buy list | 2 |
| `wrong-shelf.json` | The shelf as the hard case gets it wrong; `fixture.yaml`'s `wrong_shelf_must_say` holds the words the check must give when it refuses it | 2 |
| `settings.fixture.yaml`, `expected-price.json` | The twelve settings of §9.3 with made-up values, and the cost lines, break-even and suggested price they give, or "no price" with the empty setting named | 3 |
| `expected-scenarios.json` | The scenarios of §9.7, worked on the same made-up settings | 3 |

Two files sit beside the folders, shared by all of them, because two fixtures can print the same
plate: `slices.json`, one frozen slice[^frozen] per recipe some fixture plans (its hash, minutes,
grams and beds), and `prints.json`, the timed prints the time correction rests on, frozen as
`bambu order timed --json` printed them on 2026-10-04, so a new print does not move a golden.

**Made-up settings stay made up.** Each `settings.fixture.yaml` says FIXTURE in its first line and
beside every value. The values are picked so the sums can be checked by hand (whole numbers,
rates of 1), never a looked-up or real value. So a fixture can never be read as a price, and a
real price can never slip into a public test.

**Frozen slices keep the suite fast.** The checks read each plate's minutes and grams from
`slices.json` instead of running the slicer. So they need no Bambu Studio, no printer and no
network. Each frozen slice carries the hash[^hash] of the recipe it came from. If the planner writes a
different recipe, the hash no longer matches and the fixture fails with "re-freeze", so a stale
slice cannot pass. Phase 1 shipped the planner and the real slices together, so no stand-in was
ever frozen. `bambu order fixtures --slice` slices each recipe `slices.json` lacks and rewrites it
with only the slices some fixture still plans, so an edited fixture is re-frozen by the tool, not by
hand. The live check, that a recipe's
numbers equal `bambu validate sliced` on it (§9.5), stays separate. It runs on the flagship
order only, on a machine with the slicer, because it is slow and needs Bambu Studio.

```mermaid
flowchart LR
  fx["fixture folder: order, frozen slices, made-up settings"] --> plan["bambu order plan"]
  plan -->|"plan JSON"| cmp1{"equal, plate by plate?"}
  gold["golden files"] --> cmp1
  wrong["wrong plan"] -->|"must be rejected"| cmp1
  plan -->|"plan JSON"| hub["hub: shelf and price"]
  hub -->|"shelf and price JSON"| cmp2{"equal?"}
  gold --> cmp2
  hub --> pages["Plan, Price, Inventory pages"]
  pages -->|"numbers read by a headless browser, and screenshots"| cmp3{"equal?"}
  gold --> cmp3
```

**In the diagram:** fixture[^fixture]; frozen slice[^frozen]; golden file[^golden]; headless
browser[^headless]; hub[^hub].

**The eight fixtures.**

| # | Fixture | The order | The claim it checks | The hard case it covers |
|---|---|---|---|---|
| 1 | Ice to navy, 4 | §4's order: 4 × gBV in Ice to navy | §4 plate by plate: 5 plates, the piece counts of §9.5, 351 sliced minutes and 117 g from the Matte slices, every plate "floor" (no Matte print is timed), 5 spools to buy | Star and Outer share one color, so two groups share one plate. A plan can get every total right while one kite sits on the wrong plate |
| 2 | One color | 1 × gBV, the frame and every group in one color | One plate, the frame riding with its pieces, as [sheets-04g](../plates/sheets-04g.yaml) printed it: 86 sliced minutes, 27 g | One plate per group would make six plates with the same total grams. Only the plate count, and so the warm-ups, shows it |
| 3 | A color over two beds | 5 × gBV in Ice to navy | The frame color takes two beds, and the plan says two beds, two warm-ups and not sendable for it | The totals stay right while the plan says one bed. Five 112.5 mm frames fit a 256 × 256 mm bed by area (about 60,270 of 65,536 mm²) but not by packing, so the packer spills them. Six are refused before slicing, because their area alone (72,321 mm²) is bigger than the bed: splitting such a color across plates is later work, and phase 1 says so rather than guess |
| 4 | Two orders, one color | Two open orders that both need the same color; a shelf with one part spool that covers either order alone, not both | Held is the sum of both orders, available goes below zero, and the buy list asks for one spool | Checking each order against what is on hand says both fit. Only held, summed across orders, shows the shortfall |
| 5 | A failed print | Fixture 2's plate, closed by monitor rows that end in a failure partway | The spool loses the plate's full slice grams (§9.2); the order is still open, so its grams stay held for the reprint | Counting only finished prints leaves the spool 27 g too full |
| 6 | One setting empty | Fixture 1's order; every made-up setting filled except packaging | No cost total, no break-even, no price; the page names packaging as the empty one; the lines that do not need it still show | Treating empty as zero gives a price a little lower than fixture 1's. It looks right, so only "no price" in the golden catches it |
| 7 | Silk Gold | 1 × gBV with one group in Silk Gold (13401) | The plan works; the buy list carries the store note "not on the US store, 2026-10-04" from in `.claude/skills/color-themes/palette.yaml`; the material line and the price say no store price for 13401 | Using Silk+ Gold's (13405) price because it is the nearest color. A price appears, and it is wrong: the research calls that swap a color change to look at, not a rename |
| 8 | Two constructions | 2 × gBV and 2 × the GimTvN9hw4U minimal coaster (another pattern in the catalog, a frame with no loose pieces), all frames in one color | That color's plates hold 4 frames, counted 2 and 2 by construction; an order line with no pieces is valid | A planner keyed on the group name or on "frame" alone counts 4 gBV frames. The totals can still match |

**Validator:** the plan comes out right plate by plate (fixtures 1, 2, 3, 7, 8).

PASS: for each fixture, every plate in the planner's JSON matches one plate in
`expected-plan.json` by color. It has the same pieces by construction and group, the same bed
count, minutes and grams equal to its frozen slice, and "floor" where no ratio matches. No plate
is extra or missing, and the order total equals the sum of its plates. Each fixture's
`wrong-plan.json` is rejected.

FAIL: fixture 1's wrong plan moves one kite from its own plate onto another color's plate and keeps every
total. A check that compares totals passes it. This one fails it, because it compares the pieces
on each plate. If any `wrong-plan.json` passes, the suite fails: a check that cannot reject its
own hard case is not checking it.

**Validator:** the shelf adds up (fixtures 4, 5 and 7's buy list).

PASS: on hand, held, available and the buy list, color by color, equal `expected-shelf.json`. A
failed print takes its full slice grams off its spool, and its order's grams stay held.

FAIL: fixture 4 checked one order at a time. Each order fits on its own, so no buy list appears;
the golden asks for one spool. Also FAIL: fixture 5 with the failed row skipped, so the spool
reads 27 g too full.

**Validator:** a price shows only when every input is filled (fixtures 1, 6, 7).

PASS: with every made-up setting filled (fixture 1), each cost line, the break-even and the
suggested price equal `expected-price.json` to the cent. They also equal a hand working of §9.3,
written out in the fixture's README. With packaging empty (fixture 6), or a color with no store
price (fixture 7), no total, break-even or price appears, and the missing input is named.

FAIL: fixture 6 with the empty setting read as zero. It shows a break-even a little below
fixture 1's, which looks reasonable. The golden for fixture 6 is "no price", so any number fails.

**Validator:** the pages show the same numbers as the JSON (all eight, from phase 4).

PASS: a headless browser[^headless] opens Plan, Price and Inventory for each fixture, on a fresh
store holding only that fixture. Every number a page shows is read from an element tagged with the
JSON field it shows. Each equals the golden, formatted by the one rounding rule the pages share.
Every golden field the page is meant to show is found on it. A screenshot of each page is kept
with the run's report.

FAIL: the Plan page shows the previous fixture's plan (a stale store), or rounds 62.4 g to 62
when the golden says 62.4, or drops a plate row and still shows the right total. A golden field
missing from the page also fails. A check that reads only what the page shows cannot see what the
page leaves out.

**The make target.** `make validate-orders` runs in this repo, and `make validate` calls it. It
runs the planner's unit tests, then the plan checks on the frozen slices, with no slicer, printer
or network; it does ask the local bikar checkout for each pieces file's groups, so it needs
`BIKAR_DIR`. Since phase 2 it also runs the shelf's unit tests and, on fixtures 4, 5 and 7, the
shelf checks: the fixture's `shelf.fixture.yaml` against `expected-shelf.json`, and its
`wrong-shelf.json` refused with the words in `wrong_shelf_must_say`. The shelf code lives in this
repo until call 1 says otherwise (§9.2). The price and page checks run where that code lives. If call 1 picks the hub,
that is a hub target of the same name, reading the fixture folders from this repo at a pinned
commit. Before a phase lands, the runner lists its fixtures as "waiting on phase N". The runner
holds one number, the last phase shipped (`3d-models:tools/bambu/src/commands/order.ts:L141 "const SHIPPED_PHASE = 2;"`),
and raising it when a phase lands runs that phase's fixtures. So a fixture cannot stay waiting by
being forgotten.

**Which phase builds which part.** The suite comes first, as the test each phase must pass:

| Phase | What it adds to the suite |
|---|---|
| 0, before phase 1 | The eight fixture folders; goldens worked by hand from §4, §9.2 and §9.3; the wrong plans; the runner; `make validate-orders`, with every fixture listed as waiting |
| 1, the planner | The plan checks pass on fixtures 1, 2, 3, 7 and 8, on real slices. Phases 0 and 1 shipped together: the runner and its fixtures came with the planner, not before it |
| 2, the shelf | The shelf checks pass on fixtures 4, 5 and 7, and each fixture's wrong shelf is refused. Shipped with `bambu shelf show` and the `sent` row; `print send` writing that row is still to come |
| 3, the price | The price checks pass on fixtures 1, 6 and 7, and the scenario check in §9.7 |
| 4, the pages | The browser run, with its screenshots, over all eight |

### 9.7 Pricing ideas: the ways to set a price, side by side

In plain words: before settling on one price, lay out the ways of setting it next to each other.
For each, see what it earns per coaster and how many coasters a month it takes to cover the
shop's fixed costs. Call 2 picks the method a quote uses. This view is where that choice is tried
out, and later where a quote is checked against the other ways.

Every market number below is from the
[consolidated pricing research](../../research/2026-10-04-coaster-pricing.md), with its hedges.
That research found no sales volumes, only asking prices on one day, so nothing below says what
buyers pay. The first three rows are call 2's three methods. The other four are ways to shape a
price, and work on top of whichever method call 2 picks.

| Strategy | How the price is set | Pros | Cons | Implications | What the research gives it |
|---|---|---|---|---|---|
| Cost-plus | Break-even × (1 + markup), §9.3 | Never below cost; every number explained | Needs all twelve settings; the markup is a judgment | Call 2's pick; the other rows are compared to it | One coaster's plastic, power, wear and failures cost about $0.98–1.37, before labor, packaging and fees. Labor is likely the largest cost |
| Market range | A pick inside what similar coasters are listed at | Easy to sell at; no settings needed to pick it | Can sell below cost: a five-color order has five plates and five warm-ups that a one-color listing does not | The band moves without us, so repeat the search before using it | Printed coasters about $5 each (median of 39 listings, one pass, not re-checked); sets of 4 median $20 (23 listings), sets of 6 $25.50 (12). First page only, asking prices, not sales |
| Story, premium | A pick above the band, for the Islamic geometry and the handmade, loose-piece build | Earns the most per coaster, if it sells | Nothing to check it against: no sales, and the research found no evidence of a premium for the loose-piece build. It calls the build a difference in the product, not proof of a premium | An untested bet until a few real sales; the page labels it as one | Printed Islamic sets $6.25–7.50 a coaster, from 4 listings, three of them from one shop, all smaller than ours (112.5 mm), none a frame with loose pieces. Medium-low evidence |
| By finish | One price per line: Matte or Basic, Silk+, and Sparkle or Silk Multi-Color | A menu buyers can see; a visible reason for a higher price | The filament cost barely differs, so a finish step is a price choice, not a cost passed on | A "Silk" tier means Silk+: plain PLA Silk is not on the US store. Silk+ refills come in four colors only | Silk+ costs the same as Basic and Matte ($15.99 refill, $18.99 spool). Sparkle and Silk Multi-Color cost $24.99, spool only, no bulk discount: $0.67 a full plate against $0.43–0.51 |
| Sets and bundles | 4 or 6 coasters, with a holder, priced as one | Warm-ups, packaging and the fixed fee spread over more coasters; listings already sell this way | The holder is not designed: no construction, no slice, no cost | Each set size is planned as its own order, so its cost per coaster is its own. A holder design joins the backlog | Sets of 4 median $20 (23 listings), sets of 6 $25.50 (12); one Islamic set of 4 with a holder listed at $25 |
| Custom theme | The custom order's own plan, priced as usual, plus a surcharge for the design time | Pays for the back-and-forth a custom order takes | Nothing to set the surcharge from. More colors already cost more through the formula (one plate and one warm-up per color), so the surcharge must not charge for them again | The surcharge covers design minutes only. A color the store does not sell (Silk Gold) cannot be priced at all | Nothing: the research did not look at custom work |
| Launch price | A lower price for the first orders, for a set count or a set time | First sales and first reviews come sooner | Can sell below cost, and a first price sets what buyers expect | Selling below break-even is a choice to lose money on purpose. Call 5 decides whether the view allows it | Nothing: the research found no sales volumes and nothing on launch prices |

**The view.** A Scenarios view in the Price tab, beside the Breakdown, with one row per strategy.
Each row shows the price per coaster, the margin per coaster, and how many coasters a month it
takes to cover the shop's fixed costs (its break-even volume[^scenario]):

```text
cost each   = order cost ÷ coasters in the order                     (§9.3's cost)
margin each = price each × (1 − fee percent) − fixed fee ÷ coasters − cost each
to cover    = monthly fixed costs ÷ margin each, rounded up; "never" when margin each ≤ 0
```

Labor is already inside the cost, so the margin is what is left after paying for Omar's time.
"To cover" is how many coasters a month pay the fixed costs at that margin. It is not a forecast
of what will sell.

The view needs one input that §9.3 does not: **monthly fixed costs**, what the shop pays each month
whatever it sells. The research's reference is the plan of Shopify (a service for running an
online shop) at $39 a month, or $29 a month paid
yearly, if the shop sells there. It starts empty, like every setting, and it is not one of §9.3's
twelve, because a quote does not use it. The rows that are not formulas (a market pick, a story
price, finish steps, set prices, a surcharge, a launch discount) each take a candidate price from
Omar, and start empty too.

![The Scenarios view in the Price tab for the 4 × gBV order. Seven strategies, one row each:
cost-plus, market range, story or premium, by finish, sets of 4 and 6 with a holder, custom theme
and launch price. Every price, margin and coasters-to-cover cell is a dash, because every input
at left is empty, each with the research's reference beside it. Below: the three formulas, and
what a scenario is not.](order-driven-lab-media/price-scenarios-mockup.png)

*The [mockup](order-driven-lab-media/price-scenarios-mockup.html), drawn in the Lab's look.
Every number is a dash on purpose.*

**The rules the view keeps.**

- A row shows no number while any of its inputs is empty, the same rule as §9.3.
- Every row uses the cost from §9.3, never a cost of its own.
- A set row plans its own order, of 4 or 6 coasters, through the planner.
- A row below break-even carries a tag saying so.

**Validator:** every scenario runs through the one formula and shows only what it can work out.

PASS: on fixture 1, with every made-up setting and candidate price filled, each row's price,
margin and coasters to cover equal `expected-scenarios.json`. The cost-plus row's price equals
the Breakdown's suggested price. The set-of-6 row's cost each comes from a plan of 6 coasters, not
from fixture 1's plan of 4. A row whose margin is at or below zero shows "never" and a "below
break-even" tag.

FAIL: the set-of-6 row reuses the cost each of fixture 1's 4 coasters. The warm-ups and packaging
are then spread over 4 coasters, not 6, and the margin reads lower than it is. That is a
believable number, and only the golden worked from a 6-coaster plan catches it. Also FAIL: any
row that shows a number while one of its inputs is empty.

**A skill, a page or a gate.** Two earlier evaluations each weighed a proposed skill against how
often its job actually came back:
[the DSL-extension skill evaluation](../process/dsl-extension-skill-evaluation.md) and
[the issue-register evaluation](../process/issue-register-evaluation.md). Both concluded: no
skill, a gate instead. The count here is zero, because no coaster has been priced yet, by hand or
otherwise. So this is **a page and a gate, not a skill**: the Scenarios view, with phase 3
working out its numbers and phase 4 showing them, and the validator above inside the fixture
suite.

**A possible later skill.** A thin persona skill could follow the pattern of review-theme[^reviewtheme]:
simulated buyers each react to a coaster's picture and a candidate price, saying whether it feels
fair, cheap or too much. It would be **simulated, not customer research**. It cannot say what
anyone pays. A price is a money decision, so a made-up reaction can mislead more there than a
theme score does. Whether to build it is call 4. The suggested trigger for building it is measured
recurrence: three priced orders where Omar wanted a second opinion beyond the scenarios.

## 10. Open calls for Omar

Tick one box per call. My pick is first, with its reason. A call with no tick stays open.

### Call 1: where the orders, the shelf and the three pages live

| | A. Order files in this repo | **B. The hub (recommended)** | C. The Coaster Lab, in the browser | D. A spreadsheet |
|---|---|---|---|---|
| What it is | A folder of order files here, pages on this repo's public website | The private hub owns orders, the shelf and price inputs; it runs the planner; the Lab only hands over a link | Orders saved in the Lab's browser storage, beside the design draft | A sheet the owner fills in, with the plan pasted in |
| Pros | One repo; history in git; no new server | Private by default; already runs the CLI and reads the printer; already on Omar's list ("estimates" is its next step); one store for three pages | No server; next to the design | Fastest to start; familiar |
| Cons | **Customer names would be public**; a quote is a commit | Only reachable on Omar's private network; hub work before pages appear | One browser, one device; lost when cleared; the Lab is public, so no private inputs | Nothing is worked out from the order; numbers drift from the slices |
| Implications | Rules out storing a customer; forces call 3 to "never" or a second repo | The planner stays here and public; the hub is the only writer of orders; the Lab gains one button | Rules out batching and inventory across devices | Every later page re-types what the sheet holds |
| Better version searched for | "Files here with a code instead of the customer's name": still public order history and prices. Not found to dominate B | "Hub stores, Lab shows read-only plan": possible later, same store | "Lab plus export to the hub": that is B | "Sheet fed by the planner's JSON": B without the pages |
| Short-term challenge | None technical; the privacy fix is policy | The hub's Orders tab and store are new; its plate queue is only half built | Storage limits; no shared shelf | None |
| Long term, build or reuse | Builds here, on a public surface | Builds on the hub we already own | Builds in the Lab, the wrong place for money | Depends on a sheet tool and hand entry |
| What it verifies | The plan, by its commit | The plan against real slices and the real trays; the shelf against finished prints | The plan only | Nothing: the numbers are typed |

**Pick B**, because it is the only option that keeps customers private and still works the shelf
out from real prints. The planner stays public in this repo either way.

- [ ] A. Order files in this repo
- [ ] B. The hub (recommended)
- [ ] C. The Coaster Lab in the browser
- [ ] D. A spreadsheet

### Call 2: how the price is set

| | **Cost-plus with a market band (recommended)** | Market price | Value price |
|---|---|---|---|
| What it is | The break-even price from cost, a markup on top, what similar coasters sell for drawn beside it | Price at what similar coasters sell for | Price at what this design is worth to a buyer |
| Pros | Never sells below cost; every number explained; the band catches a price far off the market | Easy to sell at; no cost model needed | Can earn most on a striking design |
| Cons | Needs every cost setting; the markup is a judgment | Can sell below cost for a five-color order nobody else makes | No way to check it; hard to explain a quote |
| Implications | Phase 3 needs all twelve settings filled before it quotes: the four looked-up ones confirmed, the five from Omar's records, and the three his to choose | The cost lines become a warning, not the price | Needs sales history we do not have |
| Better version searched for | It is the better version: cost-plus alone ignores the market, market alone ignores cost | "Market, never below break-even": the same as the recommended one | "Value, never below break-even": a markup choice inside the recommended one |
| Short-term challenge | The looked-up settings have references to confirm; warm-up, hands-on minutes, the good-plate share and packaging need timed prints and a real order, and the electricity rate needs Omar's bill | Usable now: the research gives a band (Etsy, one day's asking prices) | Nothing to set it from until there are sales |
| Long term, build or reuse | Builds on phase 1's numbers, which we own and re-measure with every print | Reuses other sellers' prices, which move without us | Reuses Omar's judgment, unrecorded |
| What it verifies | Cost against slices and measured time | Nothing about our cost | Nothing |

**Pick cost-plus with a market band**, because it is the only one that cannot quote below cost,
and it keeps the market in view. Either way, the settings from Omar's own records come from real
orders, his print logs and his bill.

- [ ] Cost-plus with a market band (recommended)
- [ ] Market price
- [ ] Value price

### Call 3: orders as files in git

This repo is public. A committed customer name is public for good, even after it is deleted.

| | **Never in this repo (recommended)** | In this repo, a code instead of the customer's name | In a private repo |
|---|---|---|---|
| Pros | Nothing private can leak by a commit | Orders get history and review | History, and private |
| Cons | Order history lives in the hub's store, which needs its own backup | Order volume, dates and prices are still public | A fourth repo to keep in step |
| Implications | The planner reads order files by path from outside the repo | Prices and quotes must stay out too | Could hold the hub's store later |
| Better version searched for | "Never here, and the hub's store backed up to a private repo": the same pick plus a backup, so a possible later step, not a different option | "Codes instead of names, and no prices": still shows how many orders, and when | "Private repo with only the store's backup": that is the version left |
| Short-term challenge | The hub needs a store and a backup it does not have yet | A gate to keep names and prices out, which the next mistake defeats | A fourth repo, with its own hooks and pins, before there is one order |
| Long term, build or reuse | Builds the store once, in the hub we already own | Reuses git, but every commit is public for good | Reuses git, and doubles the repos kept in step |
| What it verifies | The planner, which is public and tested here; orders are checked by the hub, not by git | The commit log, and it leaks what it logs | The commit log, privately |

**Pick "never in this repo"**, because the other two make some part of the business public or
add a repo for a store that has none yet. What git would check about an order (who changed it,
when) the hub's store records itself.

- [ ] Never in this repo (recommended)
- [ ] In this repo, a code instead of the customer's name
- [ ] In a private repo

**Decided 2026-10-05:** never in this repo; the order files live in an iCloud folder →
[D-101](../../working-model/decisions-log.md#d-101--orders-never-go-in-this-repo-they-live-in-an-icloud-folder).

### Call 4: how to try out pricing ideas

| | **A. The Scenarios view and its check, no skill (recommended)** | B. The view, plus a price-persona skill | C. A pricing skill instead of a view | D. No view: call 2's one price only |
|---|---|---|---|---|
| What it is | §9.7's seven rows in the Price tab, worked by the §9.3 formula and checked by the fixture suite | A, plus simulated buyers who react to a picture and a candidate price, on review-theme's pattern | A conversation in Claude that walks through the strategies for one coaster and writes up a pick | The Breakdown's suggested price, nothing beside it |
| Pros | Every number comes from the formula and is tested; nothing new to keep up besides one view | A second opinion before a first sale; cheap to run | No page work; flexible | Nothing to build |
| Cons | Shows what each way earns, not whether it sells | **Simulated, not customer research**: it cannot say what anyone pays, and a made-up reaction can steer a money decision | Numbers typed in chat drift from the plan and the settings; nothing checks them | No way to compare a set or a launch price before choosing one |
| Implications | Phase 3 works out the rows and phase 4 shows them; a persona skill stays possible later | A persona file to write and keep; its scores must be labeled simulated wherever they appear | A third place prices are worked out, beside the hub and the formula | Strategies are weighed in Omar's head, unrecorded |
| Better version searched for | "A, with the persona skill built once there is recurrence": the same pick plus a stated trigger | "Personas checked against real buyers": needs sales we do not have | "A skill that reads the hub's JSON": that is A with a chat front end | "One price plus the market band": already in the Breakdown |
| Short-term challenge | Empty until the settings are filled, like the rest of the Price tab | Persona prompts written with no sales to check them against | A skill with no measured recurrence, against both precedent evaluations | None |
| Long term, build or reuse | Builds on the formula and fixtures we already plan | Reuses review-theme's pattern; adds a scored opinion nobody can verify | Builds a second pricing path | Nothing built; nothing learned |
| What it verifies | Every row against the golden file, and the set rows against their own plans | The rows, as A; the personas verify nothing | Nothing | The one price, as in §9.5 |

**Pick A**, because the precedents say measure recurrence before a skill, and no coaster has
been priced yet. The trigger to look at B again: three priced orders where Omar wanted a second
opinion beyond the scenarios.

- [ ] A. The Scenarios view and its check, no skill (recommended)
- [ ] B. The view, plus a price-persona skill
- [ ] C. A pricing skill instead of a view
- [ ] D. No view: call 2's one price only

**Decided 2026-10-05:** more than B, from Omar's comment: the view with charts, simulated buyers
who say in their own words why they buy or walk away and how that changes with the price, costs at
1, 5, 10 and 100, all built so real orders replace the simulation later →
[D-104](../../working-model/decisions-log.md#d-104--pricing-is-tried-on-simulated-buyers-and-on-a-charted-view-built-for-real-orders-later).

### Call 5: a scenario priced below break-even

A launch price, or a market pick for a five-color order, can come out below break-even.

| | **Shown and tagged; quoting it takes a reason (recommended)** | Never shown | Shown, no tag |
|---|---|---|---|
| Pros | The trade is visible; a deliberate loss is allowed and recorded with its reason | No loss can be quoted by accident | Simplest view |
| Cons | One more field on a quote | Hides the very thing a launch price is about; a market pick below cost just disappears | A loss looks like any other price |
| Implications | The quote stores its reason; the fixture suite checks the tag (§9.7) | Launch prices floor at break-even; the launch row becomes a smaller markup | The Breakdown's break-even is the only warning |
| Better version searched for | It is the better version of the other two: it shows the loss and asks for the reason | "Hidden, with a count of hidden rows": still hides the price | "Colored red, no reason asked": the tag without the record |
| Short-term challenge | None beyond the view | None | None |
| Long term, build or reuse | Builds on the view and the quote record | Builds a filter | Builds nothing |
| What it verifies | The tag, against the golden file; the reason, by being required | That no row below break-even shows | Nothing |

**Pick "shown and tagged"**, because a launch price below cost is a choice Omar may want to make
on purpose, and the tag plus the reason keep it from happening by accident.

- [ ] Shown and tagged; quoting it takes a reason (recommended)
- [ ] Never shown
- [ ] Shown, no tag

## 11. The build, in order of value for the work

Write the simulated orders first, as the test every later phase must pass. Then build the
command, because it answers material, time and plates with no pages. Then the shelf, then pricing
once its inputs exist. The pages come last, since they only show what the first three work out.

| Phase | What | Where | Value | Test |
|---|---|---|---|---|
| 0 | **The simulated orders** (§9.6): eight fixture folders, goldens worked by hand, a wrong plan per fixture, the runner and `make validate-orders` | 3d-models `tools/bambu` test fixtures; the hub's checks read them at a pinned commit | Each later phase has its finish line written down before it starts | The runner lists all eight fixtures as waiting, and rejects every wrong plan it can already read |
| 1 | **`bambu order plan`**, built with piece colors phase 1 (`plates by-color`): read an order file, count pieces by color, write or print one recipe per color, slice each, print minutes, grams, beds and the ratio used, as text and JSON | 3d-models `tools/bambu` | Answers material, time and plates for any order, today, with no pages | The 4 × gBV order gives 5 recipes holding exactly the §9.5 counts; each recipe's numbers equal `bambu validate sliced` on it; a color forced onto two beds shows two; no matching print shows "floor" |
| 2 | **The shelf**: a spool file, reservations from open orders, the buy list, closing a print on the monitor's finished row | shipped as `bambu shelf show` in 3d-models `tools/bambu`, on a gitignored shelf file until call 1 places it | Answers "is it on the shelf" and "what to buy"; stops double counting spools | A send with a send record (sheets-04g, green, the tray it picked) followed by its finished row subtracts 27 g from the green spool; a failed print subtracts too; two orders in dark blue reserve the sum; a color short by 1 g lists one spool |
| 3 | **Price**: the inputs, the formula, the breakdown, the market band, and the scenarios' numbers (§9.7) | the hub's pricer runs the formula on phase 1's JSON; public settings' references in this repo from the consolidated research, private ones in the hub | Answers "what to charge", explained line by line | With every setting filled, break-even and suggested match the formula by hand; with any setting empty, no price shows |
| 4 | **The pages**: Plan, Price (with its Scenarios view), Inventory in a hub Orders tab, and the Lab's Add to order button | the hub web; bikar `packages/lab` | The same answers without a terminal, and from a design straight to an order | A real-browser run: Add to order in the Lab opens the hub's Plan page with the design filled in; its numbers equal phase 1's JSON |

Pricing is third, not first, because its inputs are not settled and phases 1 and 2 are useful
without it. The pages are last because each one only shows what phases 1–3 already work out.

## 12. Checking the numbers, and where they stop holding

This section checks that the example's sums add up, and says when the time ratio and the grams
can be reused for another print.

- **The example satisfies its own formulas.** 4 × 27 = 108 g; 4 × 86 = 344 minutes;
  344 × 158 ÷ 140 ≈ 388, the figure the page names but does not use for a Matte order. The
  mockups' per-color rows (Plan and Inventory) are estimates, the gBV themes split times four
  (Ivory 200 min and 62.4 g, Dark Blue 72 and 22.4, Marine 60 and 18.4, Ice 8 and 3.2, Sky 4 and
  1.6), which sum to 344 minutes and 108 g; the Plan's corrected column is empty and its total is
  tagged "Basic stand-in", as the ratio rule below requires.
- **The ratio** rests on the three one-color PLA Basic prints watched from start to finish, of
  the five print logs in this repo (phones-01 switched colors, and [sheets-04b](../plates/print-logs/sheets-04b.md)'s watch began at 38%
  after a cancelled first send, so its real minutes are not known): sheets-04g 97 watched minutes
  over 86 sliced, about 1.13; sheets-04c 48 over 42, about 1.14; phones-02 13 over 12, about
  1.08. Pooled as total watched over total sliced, 158 over 140, about 1.13. All
  three start at the monitor's first row, which may be after the printer began warming up, so all
  may run a little low. Three prints are not enough to say whether long plates or short ones run
  over more. **This transfers** to another plate only on the same printer, process profile and
  filament profile; it never transfers to PLA Matte, a different profile: a Matte ratio replaces it once a Matte plate is
  timed. The page always names the prints a ratio rests on.
- **Grams transfer** from one profile to another only through the density, which is attributed,
  not measured (§9.1).
- **No price appears anywhere in this doc**, and none should until all twelve settings are filled:
  the four looked-up ones confirmed, the five from Omar's own records, and the three his to choose
  (payback hours, labor rate, markup). Until a Matte plate is timed, a price rests on the sliced
  floor and says so. The
  research values in §9.3 are references, not a price. Its cost of about $0.98 to $1.37 for one
  full coaster leaves out labor, packaging and fees, and is not an input here.
- **The fixtures hold no price either.** Their settings are made up, say FIXTURE beside every
  value, and are picked so the sums can be checked by hand. Fixture 2's 86 minutes and 27 g are
  sheets-04g's slice, the same figures as the time ratio above, and fixture 1's are §4's
  stand-ins until phase 1 slices its recipes. The market numbers in §9.7 are the research's, with
  its hedges, and none of them is a setting.
- **The flagship can be built by what this doc ships**: phase 1 alone produces every row of §4
  down to the corrected minutes, with Matte slices in place of the Basic stand-ins; the filament
  check and buy list come from phase 2's shelf, run on the saved plan.

## Glossary

[^gbv]: **gBV** — short for gBV_JTt3Kxk, one geometric pattern, first drawn in GeoGebra (a geometry drawing app), made
    into a coaster: a frame with 41 loose pieces that drop into its holes, in five groups (1
    middle, 10 kites, 10 hexes, 10 stars, 10 outers). The frame and the pieces are two
    constructions.
[^theme]: **theme** — a named set of colors, one for each group of pieces. Ice to navy runs from
    pale ice blue in the middle to dark navy at the edge.
[^plate]: **plate** — one print job: everything that goes on the printer's bed at once. Since
    2026-10-04, one color per plate.
[^slicer]: **slicer, slice** — the program (Bambu Studio) that turns a 3D model into printer
    instructions, layer by layer, and estimates the minutes and the filament length. A
    **profile** is its saved settings for one printer, one print style (the process profile) or one
    filament.
[^strap]: **strap** — the width, in mm, of the band lines that form the pattern's frame.
[^code]: **color code** — Bambu Lab's five-digit product number for one color in one line of
    filament.
[^bambu]: **bambu CLI** — this repo's command-line tool for the printer: it builds plates,
    slices, checks, sends and watches prints.
[^printlog]: **print log** — a page per plate with one row each time the printer's state changed
    while it printed, written by the print monitor; the source of real print times.
[^recipe]: **plate recipe** — a YAML file that lists what goes on one plate (which design, which
    pieces, how many, at what size) and with which printer settings.
[^tray]: **tray** — one of the four filament slots on the printer that feed it a spool.
[^spool]: **spool** — a reel of filament, bought whole, of one line (PLA Basic, PLA Matte) and one
    color. Most Bambu spools carry a tag the printer reads for the color and the percent left: a
    **tagged spool**.
[^filament]: **filament** — the plastic a 3D printer melts to build a part, sold as a thin thread
    wound on a spool; bought by the spool, used by the gram.
[^construction]: **construction** — the design file (a `.bkr`) a coaster is made from: the
    pattern, its pieces and its knobs.
[^lab]: **Coaster Lab** — the web page in bikar where a coaster is designed: pick a pattern, turn
    knobs, see it in 3D.
[^sharelink]: **share link** — the Coaster Lab's address for a design: the pattern and every knob
    changed from its default, short enough to paste anywhere.
[^order]: **order** — what someone wants: which coaster, which size, which colors, how many, by
    when. The only input in this design.
[^ratio]: **ratio** — real print minutes over sliced minutes, from past prints with the same
    settings; used to correct the slicer's estimate.
[^inventory]: **inventory, the shelf** — the spools on hand and how many grams each has left.
[^buylist]: **buy list** — the colors the shelf is short of for open orders, in whole spools.
[^price]: **price** — what an order is sold for; here worked out from cost, a markup, and a look
    at what similar coasters sell for.
[^packer]: **packer** — the step that lays pieces out on a bed and decides how many beds a plate
    needs.
[^warmup]: **warm-up** — what the printer does before the first layer of every plate: heating
    and checking the bed. Each extra plate repeats it; nobody has timed it yet.
[^hub]: **hub** — 3d-model-hub, a private web app on Omar's own private network (Tailscale, a service that links one person's devices) that shows
    the printer and the print queue and runs the bambu CLI. Not reachable from the internet.
[^planner]: **order planner** — the proposed `bambu order plan` command: an order file in, plates,
    minutes and grams by color out.
[^x2d]: **X2D** — the Bambu Lab printer these coasters are printed on.
[^sheets04g]: **sheets-04g** — the plate that printed one gBV coaster's frame and all 41 of its
    pieces in green on 2026-10-04. Its slice and its watched print are the measured numbers this
    doc scales up.
[^phones]: **phones-01, phones-02** — two test plates of phone-shaped blocks. phones-01 switched
    between two colors mid-print; phones-02 printed the same shapes in one color. Together they
    show what a color switch costs.
[^pla]: **PLA, PLA Basic, PLA Matte** — PLA is the plastic these coasters print in. Bambu sells it
    in lines: Basic (glossy), Matte (flat finish), Silk+ (shiny), Silk Multi-Color (shiny, more
    than one color on a spool) and Sparkle (with glitter), each with its own colors and its own
    slicer settings.
[^piececolors]: **piece colors** — the sibling design for choosing a color for each group of loose
    pieces in the Coaster Lab; its phase 1 is a command that writes one plate recipe per color.
[^palette]: **palette name** — the name a design gives one group of pieces (for gBV: Middle, Kite,
    Hex, Star, Outer), used to pick that group's color. The frame is a separate construction, not a
    palette name.
[^adapter]: **CLI adapter** — the part of the hub that runs this repo's bambu CLI and reads its
    JSON output.
[^bed]: **bed** — the flat plate inside the printer that a print is built on, 256 × 256 mm on the
    X2D. A plate whose pieces do not fit one bed needs a second print.
[^monitor]: **print monitor** — this repo's script that watches a running print and writes a row
    to the print log whenever the printer's state changes, ending with a `finished` row.
[^fixture]: **fixture** — a made-up order kept as test files, with the plan, shelf and price it
    must produce. It names no customer and uses no real price.
[^golden]: **golden file** — the expected output, written down and checked in, that a run's output
    is compared with. A run that differs from it fails.
[^frozen]: **frozen slice** — a slice's minutes, grams and beds saved to a file with the hash of
    the recipe they came from, so a check can use them without running the slicer.
[^headless]: **headless browser** — a real browser (Chrome) run by a script with no window, which
    opens a page, reads it and takes its screenshot.
[^scenario]: **scenario, margin, break-even volume** — a scenario is one way of setting the price,
    worked out for the order on the page. The margin is what one coaster leaves after the selling
    fee and its cost, labor included. The break-even volume is how many coasters a month that
    margin needs to cover the shop's fixed costs.
[^hash]: **hash** — a short fingerprint computed from a file's contents; any change to the file
    changes it.
[^reviewtheme]: **review-theme** — this repo's skill in which six simulated coffee drinkers score
    each color theme from its picture. It says so itself: simulated, not customer research.
[^bikar]: **bikar** — the sibling repo with the pattern language and geometry engine, and the web
    Labs built on it.

## Appendix: anchors

The facts above, pinned to the lines that hold them.

- The share link's budget, 1800 characters: `bikar:packages/lab/src/url-state.ts:L12 "URL_BUDGET_CHARS = 1800"`.
- The Coaster Lab keeps one design draft in browser storage: `bikar:packages/lab/src/custom-state.ts:L106 "COASTER_DRAFT_SLOT"`.
- The X2D has not been seen to report grams used (unconfirmed): `3d-models:tools/bambu/src/actuals.ts:L46 "[X2D-UNCONFIRMED] consumed grams"`.
- A spool with no tag reports no percent: `3d-models:tools/bambu/src/commands/filament.ts:L48 "remain unknown (no RFID)"`.
- A slice that wrote no grams has them worked out with an attributed PLA density: `3d-models:tools/bambu/src/slice-numbers.ts:L14 "DEFAULT_PLA_DENSITY = 1.24"`.
- The X2D bed is 256 × 256 mm: `3d-models:tools/bambu/src/commands/compose.ts:L279 "X2D single-nozzle build area 256×256 mm"`.
- The hub's next step is estimates (private repo, read 2026-10-04): its README, "Next: estimates (P1's third surface)".
