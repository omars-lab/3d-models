---
date: 2026-10-04
produced-by: checker (fresh agent), consolidating -a and -b. Claude Opus 5.5. The load-bearing sources were re-opened on 2026-10-04 with WebFetch, each asked to copy the sentence word for word; no web search was run (the session's search budget was spent), and help.shopify.com refused curl with a bot check, so every quote below is WebFetch's copy of the page.
feeds:
  - docs/design/storefront/shopify-storefront-design.md (not yet written)
---

# Selling configured coasters on Shopify (consolidated)

This is the one to act on. It checks two independent research passes,
[storefront A](2026-10-04-shopify-storefront-a.md) (PR #551) and
[storefront B](2026-10-04-shopify-storefront-b.md) (PR #552), against the pages behind them.
Both files stay as they are, the record this was built from.

The question: what Shopify supports on 2026-10-04 for selling a made-to-order coaster that a
customer configures in our own Coaster Lab, hosted outside Shopify, where each ring takes one
of about 100 filament colors.

How to read this:

- **Re-opened** means I fetched the page on 2026-10-04 and asked for the exact sentence. WebFetch
  returns a small model's reading of the page; where it came back as a summary rather than a
  quote, the row says so.
- **Carried** means I did not re-open it and rely on the research file's own mark.
- **Not found in N pages** means the fact was not on the N pages named. It does not mean Shopify
  lacks it.
- Prices and limits are that day's readings.

## The short answer

| Question | Verdict |
|---|---|
| (a) Can our own app read names and addresses on Basic? | **Open.** Two Shopify pages disagree. The developer page says a custom app always has Level 2; the help page says custom Level 2 apps need Grow. Settle it with one test on the real store (see the recommendation). |
| (b) Starter plan for a new store? | **No.** "The Starter plan isn't available to new stores." B was right. |
| (c) Shop Pay Installments merchant fee? | **Not found in 9 pages re-opened here** (about 15 distinct pages across all three passes). A fee exists and is kept on refunds. 5.9% + 30¢ stays unverified recall. |
| (d) Which cart transform operations are Plus-only? | **Confirmed.** Only `lineUpdate` (and `update`) is limited to Plus or development stores. `lineExpand` has no plan sentence, but our own custom app with any Function needs Plus, so on Basic or Grow it takes a public App Store app. |
| (e) Is `orders/cancelled` a webhook topic? | **Yes.** `ORDERS_CANCELLED` is listed. |
| (f) Do the three privacy webhooks bind a custom-distribution app? | **The pages tie the mandate to App Store apps only**; no sentence about custom distribution was found in 2 pages. Subscribe anyway. |
| (g) Plan prices and card rates | **Both tables confirmed**, A's premium-card column too. |
| (h) Shopify Tax lifetime threshold | **Confirmed.** Stores created on or after 2026-05-13 get a lifetime $100,000 free threshold. Both files gave the Plus US rate correctly; the yearly $5,000 cap applies only to older stores. |
| (i) Etsy sync and personalization | **No first-party Etsy channel found; whether Etsy personalization text reaches the Shopify order was not found in 4 pages.** Etsy's own pages refused the fetch (403). |

## (a) Customer names and addresses on Basic

| Claim | A | B | Checked source (re-opened, quote) | Verdict |
|---|---|---|---|---|
| Level 2 means name, address, phone or email | yes | yes | [dev: protected customer data](https://shopify.dev/docs/apps/launch/protected-customer-data): Level 2 is "Customer data ... **including** name, address, phone, or email fields" | both agree, confirmed |
| A custom app has Level 2 "Always available" | yes | not reported | same page, table: Level 2, Custom app "Always available", Admin created custom app "Varies by plan" (that cell links to the help page's `#custom-level2-pii-app` anchor). Text above the table: "access to the different levels can vary based on app types" | A only, confirmed |
| Custom Level 2 apps need Grow or above | yes, flagged as a conflict | yes, treated as settled | [help: custom apps](https://help.shopify.com/en/manual/apps/app-types/custom-apps), under "Custom Level 2 PII apps": "To access Custom Level 2 PII apps, your store must be on the Grow plan or higher." and "If you sign up for or downgrade your plan to the Basic plan, then you won't have access to Custom Level 2 Personally Identifiable Information (PII) apps." | both found the sentence; they disagree on its reach |
| Which custom apps that sentence covers | not stated | not stated | The help section names no app type. Its lead-in reads "Apps from the Shopify App Store can access different types of PII ...". It sits under the "Custom apps" heading, which now says "You create and manage custom apps using the Dev Dashboard." and "If you have legacy custom apps created before January 1, 2026, you can manage them from your Shopify admin." | **not settled by any page checked** |
| Admin-created custom apps are closed to new apps | yes | yes | [dev: distribution](https://shopify.dev/docs/apps/launch/distribution): Shopify admin row, "no longer available for new apps" | both agree, confirmed |

Pages checked for a plan rule on Dev Dashboard apps and not found in: the Dev Dashboard
"create apps" guide, the distribution page, the help plan-features index (3 pages, plus the two
above).

**Where the evidence leans.** The developer page is the more specific one: it gives custom apps
and admin-created custom apps separate columns and points to the plan rule only from the
admin-created cell. Read that way, a new store's Dev Dashboard app keeps Level 2 on Basic, and
the help sentence is about the legacy admin-created kind. The help page, though, places the rule
under a heading that now describes Dev Dashboard apps and never limits it to legacy ones. B's
"on Basic, our own app would not get the shipping name and address" hardened one reading into a
ruling (K1); A's "a checker should re-open both" was the right call. Neither page settles it.

**How to settle it.** Not by more reading: install the custom app on the real store while it is
on Basic and query one order's `shippingAddress`. Fields an app is not approved for "will be
redacted" and come back null (B's protected-customer-data reading, carried, summary). Null means
Grow; a real address means Basic is enough. A trial or development store may not reproduce the
plan rule, so test on the paid plan.

## (b) The Starter plan

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| Starter is open to new stores | "still exists" | "isn't available to new stores" | [help: Starter plan](https://help.shopify.com/en/manual/intro-to-shopify/pricing-plans/plans-features/shopify-starter-plan): "The Starter plan isn't available to new stores." and "If you're a merchant currently on the Starter plan and you decide to change your plan, then you can't revert back to the Starter plan." | **B is right.** A's evidence (the help navigation and the Oxygen list name Starter) is true for existing Starter stores and does not contradict it |
| Starter price and card rate | not found | not found | same page: "Review the Starter plan to find the specific transaction fees for your region." No number on the page | moot for a new store |
| Oxygen runs on Starter | yes | not found | [dev: Hydrogen fundamentals](https://shopify.dev/docs/storefronts/headless/hydrogen/fundamentals): "Oxygen is available at no extra charge on paid Shopify plans: Starter, Basic, Grow, Advanced, Plus, Pause and build" | A only, confirmed; covers existing Starter stores |

## (c) The Shop Pay Installments merchant fee

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| The merchant fee | not found in 6 pages | not found in 6 pages; recalls 5.9% + 30¢ | not found in the 9 pages re-opened here: help [FAQ](https://help.shopify.com/en/manual/payments/shop-pay-installments/faq), [payouts and fees](https://help.shopify.com/en/manual/payments/shop-pay-installments/payouts-and-fees), [activate](https://help.shopify.com/en/manual/payments/shop-pay-installments/activate-shop-pay-installments), [Shopify Payments FAQ](https://help.shopify.com/en/manual/payments/shopify-payments/faq), [billing: transaction fees](https://help.shopify.com/en/manual/your-account/manage-billing/your-invoice/transaction-fees); [shopify.com/shop-pay-installments](https://www.shopify.com/shop-pay-installments), [shopify.com/pricing](https://www.shopify.com/pricing), [shopify.com/payments](https://www.shopify.com/payments), [US payments terms](https://www.shopify.com/legal/terms-payments-us). A guessed Installments terms URL returned 404 | **not found** by any pass; 5.9% + 30¢ is recall only |
| A fee exists and is kept on a refund | not found | not found | help FAQ: "The Shop Pay Installments transaction fee isn't returned to you when you issue a refund." | new here, confirmed |
| Where the terms live | not found | not found | US payments terms, summary only: merchants agree to separate terms with Affirm; no fee in that document | summary, flagged |
| Eligible US order range $35 to $30,000 | yes | yes | carried (both fetched) | both agree |

The rate has to be read in the store's admin (Settings, Payments) before the price model uses it.

## (d) Cart transforms and Functions

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| `lineUpdate` is Plus-only | yes | yes | [dev: Cart Transform API](https://shopify.dev/docs/api/functions/latest/cart-transform): "Only development stores or stores on a Shopify Plus plan can use apps with `lineUpdate` operations." and the same sentence for `update` | both agree, confirmed |
| `lineExpand` and `linesMerge` are open on any plan | yes | yes, after a re-check | same page: no sentence limits them by plan (WebFetch, asked to say so explicitly); the only rule naming all three: "Shopify rejects `lineExpand`, `linesMerge`, and `lineUpdate` operations if a selling plan is present." | both agree, confirmed as an absence on 1 page |
| `lineExpand` sets a price | `fixedPricePerUnit` | `ExpandedItemPriceAdjustment` with `fixedPricePerUnit` | same page: `lineExpand` is "An operation that expands a single cart line item to form a bundle of components." The price-adjustment field came back as a summary, not a quote | both agree; the field description is summary-level, flagged |
| Functions in our own custom app need Plus | yes | yes | [dev: Functions](https://shopify.dev/docs/api/functions/latest): "All plans: Except as noted in individual API pages, stores on any plan can use public apps that are distributed through the Shopify App Store and contain functions." and "Shopify Plus: Only stores on a Shopify Plus plan can use custom apps that contain Shopify Function APIs." [dev: build Functions](https://shopify.dev/docs/apps/build/functions) repeats both and adds "Some Shopify Functions capabilities are available only to stores on a Shopify Plus plan." | both agree, confirmed |
| Where transforms do not run | selling plans | Create Order API, Order Edit, pre-order, subscriptions | Cart Transform page, list (summary): Create Order API; Order Edit (Admin); Order Edit (Checkout); Pre-order and Try Before You Buy; Subscription | B's fuller list confirmed |
| One transform per app per store | yes | yes | "You can install a maximum of one cart transform function per app on each store." | both agree, confirmed |
| A discount function cannot raise a price | not found | "lowers prices only" | [dev: Discount Function API](https://shopify.dev/docs/api/functions/latest/discount): nothing on the page addresses raising prices (asked explicitly). "You can activate a maximum of 25 discount functions on each store." "The fetch target is limited to custom apps installed on Shopify Plus and Enterprise stores." | B's "lowers only" is a reading of an absence; A's "not found" is the accurate form |
| Function limits | 256 kB binary, 128 kB in, 20 kB out, 11M instructions | same | Functions page: "Compiled binary size: 256 kB"; for carts up to 200 lines, "11 million instructions", "Function input: 128 kB", "Function output: 20 kB" | both agree, confirmed |

So on Basic or Grow, a cart transform that prices a configured line takes a **public** app
(App Store review), even though `lineExpand` itself has no plan rule. The "Except as noted in
individual API pages" qualifier means each Function API's own page can narrow this further.

## (e) Order webhooks

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| `orders/cancelled` is a topic | yes | not confirmed, "check it" | [dev: WebhookSubscriptionTopic](https://shopify.dev/docs/api/admin-graphql/latest/enums/WebhookSubscriptionTopic): "The webhook topic for `orders/cancelled` events. Occurs whenever an order is cancelled. Requires at least one of the following scopes: read_orders, read_marketplace_orders, read_buyer_membership_orders." | **A is right**, confirmed |
| `orders/paid`, `orders/create` | yes | yes | same page: "Occurs whenever an order is paid." / "Occurs whenever an order is created." both "Requires at least one of the following scopes: read_orders, read_marketplace_orders." | both agree, confirmed |
| Timeouts | 1 s connect, 5 s total | same | [dev: HTTPS webhooks](https://shopify.dev/docs/apps/build/webhooks/subscribe/https): "Shopify has a one-second connection timeout and a five-second timeout for the entire request." "Any response outside the 200 range, including 3XX codes, is treated as an error." | both agree, confirmed |
| Retries and removal | 8 over 4 h, then deleted | same | same page: "Shopify retries 8 times over the next 4 hours." "After 8 consecutive failures, the subscription is automatically deleted if it was configured using the Admin API." | both agree, confirmed; keep the "configured using the Admin API" qualifier |
| HMAC on the raw body; dedupe | yes | yes | same page: "HMAC verification requires the raw request body." "Use the `X-Shopify-Webhook-Id` to detect and skip duplicates" | both agree, confirmed |
| No ordering, no delivery guarantee | not found in 3 pages | yes | [dev: webhook best practices](https://shopify.dev/docs/apps/build/webhooks/best-practices): "Shopify doesn't guarantee ordering within a topic, or across different topics for the same resource." "Webhook delivery isn't always guaranteed ..." "use reconciliation jobs to periodically fetch data from Shopify" | B only, confirmed |
| 60-day order window | yes | yes | [dev: Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order): "Only the last 60 days' worth of orders from a store are accessible from the `Order` object by default. If you want to access older records, then you need to request access to all orders." | both agree, confirmed |

## (f) The three privacy webhooks

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| Who must subscribe | App Store apps; custom not stated | same | [dev: privacy law compliance](https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance): "Mandatory compliance webhooks are callback methods that Shopify requires for apps listed on the Shopify App Store." "Every app that's distributed through the Shopify App Store must subscribe to the following compliance webhook topics:" | both agree, confirmed |
| Custom distribution apps | not found in 2 pages | not found in 2 pages | no sentence on custom or custom-distribution apps on that page or the protected-customer-data page | not found in 2 pages; not "exempt" |

Both researchers recommend subscribing anyway: three handlers are cheap and give deletion
requests a path.

## (g) Plans and card rates (US, shopify.com/pricing)

| Plan | Billed monthly | Billed yearly | Online standard | Online premium | In person | Third-party gateway | Checked |
|---|---|---|---|---|---|---|---|
| Basic | "$39 USD/mo" | "$29 USD/mo" | "2.9% + 30¢" | "3.5% + 30¢" | "2.6% + 10¢" | "2%" | A and B agree |
| Grow | "$105 USD/mo" | "$79 USD/mo" | "2.7% + 30¢" | "3.3% + 30¢" | "2.5% + 10¢" | "1%" | A and B agree |
| Advanced | "$399 USD/mo" | "$299 USD/mo" | "2.5% + 30¢" | "3.1% + 30¢" | "2.4% + 10¢" | "0.6%" | A and B agree |
| Plus | "Starts at $2,300 USD/mo" | not listed | "2.25% + 30¢" | "2.95% + 30¢" | "2.3% + 10¢" | "0.2%" | A and B agree |

Re-opened [shopify.com/pricing](https://www.shopify.com/pricing). The premium column was in A
only and is confirmed. B's "Online international rates + 1%" was not re-checked (B's summary).
The page does not define "premium" cards and says nothing about Installments fees.

Grow costs $50 a month more than Basic on yearly billing and saves 0.2 points on standard online
cards, so it pays for itself on card fees alone only above about $25,000 of card sales a month
($50 / 0.002, my arithmetic). Below that, the reason to pick Grow is (a), not the rate.

## (h) Shopify Tax

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| Lifetime threshold for new stores | yes | yes | [help: Shopify Tax pricing](https://help.shopify.com/en/manual/taxes/shopify-tax/pricing): "For stores that were created before May 13, 2026, Shopify Tax is free until you reach an annual threshold of sales. For stores that were created on or after May 13, 2026, Shopify Tax is free until you reach a lifetime threshold of sales." The new-store table: United States, "Lifetime sales threshold" $100,000 USD, "Maximum fee per order" $0.99 USD | both agree, confirmed |
| Fee above the threshold | 0.35% Basic to Advanced, 0.25% Plus | same | same page: United States, Shopify Plus 0.25%, Basic, Grow, or Advanced 0.35% (EU, UK, Canada: 0.15% and 0.25%) | both agree, confirmed |
| $5,000 yearly cap per region | older stores only | not reported | same page: the cap column is in the table for stores created before 2026-05-13 only; the new-store table has no yearly cap | A only, confirmed |

## (i) Etsy alongside Shopify

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| Shopify's Marketplace Connect covers Etsy | no | no | [App Store: Marketplace Connect](https://apps.shopify.com/marketplace-connect): "Sell products on Amazon, Target+, eBay, and Walmart with seamless integration." Etsy appears only under "More apps like this" (CedCommerce, InfoShore). Pricing: "First 50 marketplace-synced orders/mo free, 1% fee per additional synced-order, capped at $99/month". The [help page](https://help.shopify.com/en/manual/online-sales-channels/shopify-marketplace-connect) does not mention Etsy | both agree, confirmed; "no first-party Etsy channel found in 2 pages" |
| CedCommerce Etsy app | $9 / $29 / $59 | same | [App Store listing](https://apps.shopify.com/etsy-marketplace-integration): $9 (10 products), $29 (200 products, 100 orders a month), $59 (1,000 products, 500 orders a month); 4.5 stars, 1,249 reviews | both agree, confirmed |
| Personalization reaches the Shopify order | not found | not found | CedCommerce listing: none of "personalization", "personalisation", "custom text", "buyer note". [LitCommerce](https://apps.shopify.com/litcommerce) lists Etsy, $29 a month or $278 a year, no personalization sentence (summary). Etsy's [personalization help](https://help.etsy.com/hc/en-us/articles/360000336247-How-to-Add-Personalization-to-a-Listing) returned 403 | **not found in 4 pages**; Etsy pages refuse the fetch |

## Other load-bearing claims, cross-checked

| Claim | A | B | Checked source | Verdict |
|---|---|---|---|---|
| 2,048 variants, 3 options | yes | yes | [help: add variants](https://help.shopify.com/en/manual/products/variants/add-variants): "You can create up to 2,048 variants for a product." "Each product can have up to three options." No per-option value limit on the page | both agree, confirmed |
| Per-ring colors cannot be variants | yes | yes | arithmetic on the above (100^4 combinations) | both agree |
| Line property size limits | not found in 6 pages | not found in 6 pages | not re-opened | both agree; still open |
| Cart permalink: 25 properties, first product only | yes | yes | [dev: cart permalinks](https://shopify.dev/docs/apps/build/checkout/cart-permalinks): "You can add line item properties (up to 25) to the first product. Properties must be Base64 URL-encoded JSON." "Selling plans don't work with cart permalinks" | both agree, confirmed |
| AJAX `/cart/add.js` works only on a Shopify-hosted theme | yes | cross-origin not found | [dev: Ajax API](https://shopify.dev/docs/api/ajax): "The Ajax API can only be used by themes that are hosted by Shopify. You can't use the Ajax API on a Shopify custom storefront." | A's reading confirmed; the Lab cannot call it from its own domain |
| Storefront API cart, `checkoutUrl` | yes | yes | [dev: manage a cart](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/cart/manage): "The response includes a URL that redirects customers through Shopify's web checkout." | both agree, confirmed |
| Cart id secret | not reported | "don't include it in shareable links" | same page, the full sentence: "Never expose the `secret` part of the ID. Treat it like a password—don't include it in shareable links, public pages, or any client-side code." | B only, and B's quote dropped "or any client-side code"; that clause favours A's choice of calling the cart from the Lab's **server** |
| Tokenless Storefront access | complexity 1,000 | same | [dev: Storefront API](https://shopify.dev/docs/api/storefront): "Tokenless access has a query complexity limit of 1,000." Covers "Cart (read/write)". "Requests from real buyers aren't subject to a fixed request-per-minute limit." | both agree, confirmed |
| A plan requirement for the Storefront API or Headless channel | not found | not found | Storefront API page: none stated. [Headless app](https://apps.shopify.com/headless): "Free", developer Shopify, a compatibility list that did not render | not found in 3 pages |
| Shopify Bundles | free, all plans, 30 components, 3 options and 100 variants | not reported | [help: Shopify Bundles](https://help.shopify.com/en/manual/products/bundles/shopify-bundles): "available on all Shopify plans", "Fixed bundles: Up to 30 components", "Dynamic bundles: Up to 150 components", "Maximum of 3 options and 100 variants total per bundle", "Bundles must use the Online Store or Headless storefronts." | A only, confirmed |
| Draft orders set a server price | yes | yes | carried (both fetched the draft-order pages) | both agree |
| GraphQL Admin rate limits by plan | yes | yes | carried | both agree |

## Flagged

Claims that rest on one side, on recall, or on a summary rather than a quote:

1. **(a) Level 2 on Basic.** Two Shopify pages disagree and no page checked settles it. B's
   recommendation (Grow) rests on one reading of the help sentence.
2. **Shop Pay Installments 5.9% + 30¢.** B's recall only. No pass found a number.
3. **`fixedPricePerUnit` on `lineExpand`.** Both name it; my re-check got a summary, not a quote.
4. **"A discount function lowers prices only"** (B). An absence on the page, not a statement.
5. **Fields not approved "will be redacted" and come back null** (B). Summary, not re-opened.
6. **Etsy personalization.** Not found; Etsy pages 403. LitCommerce's listing came back as a summary.
7. **US payments terms point to separate Affirm terms.** Summary of a long legal page.
8. **International cards +1%** (B). Summary, not re-opened.
9. **Untracked inventory never sells out** (both). Recall in both files; not on the 1 to 3 pages each checked.
10. **iframe plus `postMessage` to theme script** (both). Reasoning, no Shopify page.
11. **Line property and attribute size limits.** Not found in 6 pages by either pass.

## Consolidated recommendation

**Plan: Basic or Grow, settled by a test, billed monthly until then.** A leans Basic, B says
Grow; the whole difference is (a). The specific developer table leans Basic, the help sentence
leans Grow. Build the custom app first, install it on the real store on Basic, and read one
order's shipping address. If it comes back, stay on Basic; if it is redacted, move to Grow
($79 a month yearly). Both plans are a two-way door. Starter is not an option for a new store.
Plus ($2,300 a month) is the only plan where our own app can run a Function, and nothing here
needs it.

**Integration path: the Lab builds a Storefront API cart from its server, then sends the buyer
to `checkoutUrl`.** Both agree. One cart line per configured coaster or set, each with its own
attributes, which a cart permalink cannot do past the first product. The cart secret stays on
the Lab's server, since Shopify says not to put it in "any client-side code". The theme's
product page links into the Lab. A cart permalink stays the fallback for a one-click "buy this
theme" link. `/cart/add.js` is out from the Lab's own domain.

**Pricing mechanism: price-tier variants plus a check after the order arrives.** Both agree on
the shape: variants only on what moves the price (size, finish tier, set size or theme kind,
three options at most), per-ring colors as line attributes, a private config id. B adds a
server-signed `_sig` attribute over variant and config, which makes the post-order check exact;
take it. On a mismatch, hold the line with `fulfillmentOrderHold` (B, carried) and contact the
buyer. Draft orders cover quotes and large orders. A pricing cart transform needs a public app
or Plus, so it is out at launch.

**Order sync: one Dev Dashboard custom app, webhooks plus a reconciliation sweep.** Subscribe to
`orders/create` (run the signature check early), `orders/paid` (start printing),
`orders/cancelled` (confirmed a topic) and `orders/updated`. Verify the HMAC on the raw body,
answer within 5 seconds and queue, dedupe on `X-Shopify-Webhook-Id`, and run a periodic sweep,
because Shopify neither orders nor guarantees deliveries and deletes an Admin-API subscription
after 8 straight failures. Mark lines In progress while plates print and ship with
`fulfillmentCreate` and tracking, partially when a set spans plates. Handle the three privacy
webhooks even though the pages only require them of App Store apps.

**Before the design commits:** the (a) test, the Installments rate read from the admin, and the
line-attribute size limit (or keep the payload to an id and a short color list, as both advise).
