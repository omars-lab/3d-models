---
date: 2026-10-04
produced-by: researcher B (fresh agent), Claude Opus 5.5, one of two independent researchers on the same question. Researcher A's files were not read.
feeds:
  - docs/design/storefront/shopify-storefront-design.md (not yet written)
method: The session's web-search budget was already spent, so no search snippets were used at all. Every page below was fetched directly with WebFetch. WebFetch hands back a small model's reading of the page, not the raw HTML, so for each load-bearing number I asked it to copy the sentence word for word, and where two readings disagreed I re-fetched and asked for the exact sentences. One such re-check caught a wrong reading (see Q4). Pages that returned 403 or 404, or that did not contain the fact, are listed as such.
---

# Shopify storefront for made-to-order coasters (research B)

**The question.** What Shopify supports in 2026 for selling a configured, made-to-order
coaster whose configuration (pattern, size, a filament color per ring plus the frame, or a
named theme) lives in an external Coaster Lab and travels as a share URL; at what cost and
with what limits. Ten sub-questions, answered in order, then a short recommendation.

**How to read the source tags.**

- **fetched-verbatim**: page fetched, the quoted sentence was asked for word for word.
- **fetched-summary**: page fetched, the fact comes from the fetch tool's summary of the page
  (no word-for-word check). Treat as one notch weaker.
- **not found**: page fetched and the fact was not on it.
- **unverified recall**: my own background knowledge, not checked against a page this session.
  Never load-bearing below unless flagged.

No claim in this file rests on a search snippet, because no search was run.

---

## Q1. Product, variant and option limits

**Findings.**

- "You can create up to 2,048 variants for a product." and "Each product can have up to
  three options." (help.shopify.com, add-variants; fetched-verbatim)
- The Admin GraphQL `productSet` reference: "By default, stores have a limit of 2048 product
  variants for each product." The qualifier "by default" is Shopify's. (fetched-verbatim)
- No per-option value limit was stated on either page (not found in 2 pages checked).
- Store-wide throttle: "Once a store has 500,000 product variants, no more than 10,000 new
  variants can be created per day, on any API", Plus exempt. (shopify.dev usage/limits;
  fetched-verbatim). Irrelevant at our size.
- The help page itself points to "a third-party app from the Shopify App Store" or theme code
  to go past the standard limits. (fetched-summary)

**What that means for per-ring colors (my arithmetic, not a Shopify statement).** A coaster
with, say, 3 rings plus a frame, from about 100 colors, is 100^4 = 100,000,000 combinations
per pattern and size. That is far past 2,048 variants and past 3 options (4 color slots alone
already need 4 options). So per-ring colors **cannot be variants**; they must travel as line
item properties (or cart line attributes, the Storefront API name for the same thing). What
*can* be variants are the few axes that drive price: size, finish tier, set size (1 / 4 / 6
with holder). Three axes fit the three-option limit exactly.

Sources:
- https://help.shopify.com/en/manual/products/variants/add-variants (fetched-verbatim)
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/productSet (fetched-verbatim)
- https://shopify.dev/docs/api/usage/limits (fetched-verbatim)
- https://help.shopify.com/en/manual/products/variants (fetched; limits not found on it)

## Q2. Line item properties and cart attributes

**How they are set.**

- **Theme product form.** Inputs named `properties[property-name]` on the product form
  ("These properties are captured through input elements with an attribute of
  `name="properties[property-name]"`"). (shopify.dev product template; fetched-verbatim)
- **AJAX Cart API.** `/cart/add.js` takes an `items` array, each with `id` (variant),
  `quantity`, optional `properties` object and `selling_plan`. Cart-level attributes go
  through `/cart/update.js` as `attributes`. (shopify.dev ajax cart reference; fetched-summary)
- **Storefront API cart.** `CartLineInput` has `merchandiseId`, `quantity`, `attributes`
  (key/value), `sellingPlanId`; `cartCreate` also takes cart-level `attributes`. "You can add
  up to 250 lines in a single request." (shopify.dev cartLinesAdd; fetched-summary, the 250
  sentence verbatim)
- **Cart permalink.** `properties` parameter: "Properties must be Base64 URL-encoded JSON",
  up to 25 properties, applied **to the first product** in the link only. (Q3)

**Private properties.**

- Single underscore (`_foo`): "Private line item properties are available in the Liquid
  `line_item.properties` object and Ajax API." They are "visually hidden at checkout, but are
  visible on the Order details page in the Shopify admin", and "To hide private properties on
  the storefront, you must modify the theme's codebase." (ajax cart reference;
  fetched-verbatim)
- Double underscore on a **cart attribute** (`__foo`): "Private cart attributes are not
  available in the Liquid `cart.attributes` object or the Ajax API." (same page;
  fetched-verbatim)

**Do they reach the order?**

- Admin GraphQL `LineItem.customAttributes`: "A list of attributes that represent custom
  features or special requests." `Order.customAttributes`: "A list of additional information
  that has been attached to the order." (fetched-verbatim)
- REST Order resource (legacy, but its shape is what the order webhooks send):
  `line_items[].properties` is "An array of custom information for the item that has been
  added to the cart. Often used to provide product customization options." (fetched-verbatim).
  REST is "a legacy API as of October 1, 2024. Starting April 1, 2025, all new public apps must
  be built exclusively with the GraphQL Admin API." (same page; fetched-verbatim)
- Private (underscore) line properties show on the admin order page (above). I did not find
  a page that states, for non-private properties, exactly where they show on the customer's
  order confirmation; my recall is that standard themes and the order notification print
  them, but that is **unverified recall**.

**Size limits.** Not found in the 6 pages checked (ajax cart reference, product template,
Liquid `line_item`, Storefront `cartLinesAdd`, `AttributeInput`, Storefront cart guide).
`AttributeInput` key and value are plain `String!` with no stated length. The only nearby
hard numbers found: `Order.note` "Maximum length is 5000 characters" (fetched-verbatim), 25
properties in a permalink, 250 lines per Storefront request. **Consequence:** do not plan to
carry the whole configuration as one giant property; carry the short share URL (or a config
id) plus a handful of human-readable properties, and keep the full configuration in our
backend.

Sources:
- https://shopify.dev/docs/api/ajax/reference/cart (fetched, twice)
- https://shopify.dev/docs/storefronts/themes/architecture/templates/product#line-item-properties (fetched)
- https://shopify.dev/docs/api/liquid/objects/line_item (fetched)
- https://shopify.dev/docs/api/storefront/latest/mutations/cartLinesAdd (fetched)
- https://shopify.dev/docs/api/storefront/latest/input-objects/AttributeInput (fetched)
- https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/cart/manage (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Order (fetched)
- https://shopify.dev/docs/api/admin-rest/latest/resources/order (fetched)
- https://help.shopify.com/en/manual/online-store/themes/customizing-themes/edit-theme-code/line-item-properties (fetched; topic not on the page)

## Q3. Embedding or linking the external Coaster Lab

| Path | What the docs say | Pros | Cons |
|---|---|---|---|
| **Cart permalink** (`/cart/VARIANT:QTY,...`) | Parameters: `properties` (Base64 URL-encoded JSON, up to 25, first product only), `discount`, `access_token`, `source_name`, `note`, `attributes`, `ref`, `payment=shop_pay`, `storefront=true` (land in cart, not checkout), and `checkout[email]` / address prefill. Limits stated: "Selling plans don't work with cart permalinks", "Cart permalinks cannot bypass storefront passwords", discount codes with commas cannot be passed. (fetched-verbatim on properties and limits) | No app, no token, any plan with a store; the Lab only builds a URL. | Properties only on the **first** product, so an order of several *different* coasters cannot carry each coaster's colors in one link. Customer can edit the URL. |
| **AJAX cart `/cart/add.js`** | Theme-side API; variant `id`, `quantity`, `properties`. (fetched-summary) | Simple, keeps the native cart, many lines each with properties. | Meant for scripts running on the shop's own domain. Whether a request from an external domain (the Lab) is allowed cross-origin was **not found** in the pages checked; assume it needs a page on the shop domain (theme or app proxy) to make the call. |
| **Storefront API cart** (`cartCreate` / `cartLinesAdd` then `checkoutUrl`) | Lines carry `attributes`; up to 250 lines per request; the cart id has a `secret` part: "Never expose the `secret` part of the ID ... don't include it in shareable links". Tokenless access covers "products, collections, cart operations, and search" with "a query complexity limit of 1,000"; tokens come from the Headless channel. "Requests from real buyers aren't subject to a fixed request-per-minute limit"; a checkout-creation throttle returns "200 Throttled". (fetched-verbatim on the quoted parts) | Built for exactly this: an external site makes a Shopify cart and sends the buyer to Shopify checkout. Many lines, each with its own colors. Works from any domain. | The Lab must hold a Storefront token (public token is visible to buyers by design) and manage the cart id. Price still comes from the variant. |
| **App proxy** (`shop.com/apps/<sub>` proxied to our server) | "A Shopify app can have only one proxy route configured." Shopify signs each request: `signature` is "a hexadecimal encoded SHA-256 HMAC of the other parameters"; `logged_in_customer_id` is added. Liquid is rendered if the response is `Content-Type: application/liquid`. Shopify strips `Cookie`, `Set-Cookie` and some auth headers. (fetched-verbatim) | Lab (or a thin page of it) appears on the shop's own domain, so `/cart/add.js` works same-origin; requests are signed. | Needs an app (custom distribution is fine); no cookies from our server; one route per app. |
| **Theme app extension / app block** | Online Store 2.0 themes only. Limits: 10 MB total, 30 blocks, 100 KB of Liquid; suggested 100 KB CSS and **10 KB JavaScript** (compressed). Blocks cannot render on checkout pages. (fetched-verbatim) | Merchant can drop a "Customize" block on the product page with no theme code edits. | A full 3D/2D configurator will not fit a 10 KB suggested JS budget; realistic use is a launcher block that opens the Lab, not the Lab itself. |
| **iframe of the Lab on a theme page** | No Shopify page on this was checked. | Lab stays our code, appears inline. | Cross-origin: the iframe cannot call the parent's `/cart/add.js` directly; it would `postMessage` to a theme script that does. My reasoning, not a Shopify statement. |
| **Headless (Hydrogen + Oxygen, or Headless channel + our own stack)** | Three build options: Hydrogen (React Router app), Hydrogen React, and the Headless channel ("Build headless using the framework of your choice ... using only the Storefront API"). The Headless channel is "a single place to create and manage access tokens for the Storefront API". (fetched-summary) Oxygen plan eligibility and cost: **not found** in the 3 pages checked (one only said shareable deployment links need "the Basic plan or above"). | Whole storefront is ours; the Lab is native. | Rebuilds everything a theme gives for free (catalog pages, SEO, apps that assume a theme). Large surface for a one-person shop. |

**Starter plan cannot be the base.** "The Starter plan isn't available to new stores."
(help.shopify.com, Starter plan page; fetched-verbatim). It also only had the Spotlight theme.

Sources:
- https://shopify.dev/docs/apps/build/checkout/create-cart-permalinks (fetched, twice)
- https://help.shopify.com/en/manual/products/details/cart-permalink (fetched)
- https://shopify.dev/docs/apps/build/online-store/display-dynamic-data (fetched)
- https://shopify.dev/docs/apps/build/online-store/app-proxies/authenticate-app-proxies (fetched)
- https://shopify.dev/docs/apps/build/online-store/app-proxies (fetched)
- https://shopify.dev/docs/apps/build/online-store/theme-app-extensions (fetched)
- https://shopify.dev/docs/apps/build/online-store/theme-app-extensions/configuration (fetched)
- https://shopify.dev/docs/api/storefront/latest#rate-limits (fetched)
- https://shopify.dev/docs/storefronts/headless/getting-started/build-options (fetched)
- https://shopify.dev/docs/storefronts/headless/hydrogen (fetched; plan facts not on it)
- https://shopify.dev/docs/storefronts/headless/hydrogen/deployments (fetched)
- https://help.shopify.com/en/manual/online-sales-channels/hydrogen (fetched; topic not on it)
- https://shopify.dev/docs/apps/build/checkout/cart-permalinks/cart-permalinks and https://shopify.dev/docs/apps/build/app-extensions/cart-permalinks (both 404)

## Q4. Custom prices for a configured item

**Variants.** Price is set on the variant in the admin; the buyer picks a variant. Up to
2,048 variants and 3 options (Q1). A storefront request cannot set a price: neither
`CartLineInput` nor the `/cart/add.js` item has a price field (fetched-summary, both pages).

**Shopify Functions, plan gate.**
- "Stores on any plan can use public apps that are distributed through the Shopify App Store
  and contain functions." (fetched-verbatim)
- "Only stores on a Shopify Plus plan can use custom apps that contain Shopify Function APIs."
  (fetched-verbatim, on two pages)
- "Some Shopify Functions capabilities are available only to stores on a Shopify Plus plan."
  (fetched-verbatim)
- Resource limits: 11 million instructions, 128 kB input, 20 kB output (scaled above 200 line
  items), 256 kB binary. (fetched-summary)

**Cart Transform Function.**
- Operations `lineExpand`, `linesMerge`, `lineUpdate`. `lineUpdate` "allows you to override the
  price, title, and image of a cart line item." (fetched-verbatim)
- Plan: "Only development stores or stores on a Shopify Plus plan can use apps with
  `lineUpdate` operations." (fetched-verbatim). **Correction caught on re-check:** a first
  summary of the same page said `lineExpand` and `linesMerge` were also Plus-only; asked for the
  exact sentences, the page names only `lineUpdate`/`update`. Expand's price adjustment
  (`ExpandedItemPriceAdjustment` with `fixedPricePerUnit`) is not restricted by any sentence on
  that page. It would still need a **public** app on a non-Plus store, because of the custom-app
  rule above.
- "You can install a maximum of one cart transform function per app on each store." The
  function can read line attributes. Transforms are rejected when a selling plan is present and
  are not supported in Create Order API, Order Edit, pre-order/try-before-you-buy and
  subscriptions. (fetched-summary)

**Discount Function.** Product, order and shipping discounts; it lowers prices only, no
surcharge. "You can activate a maximum of 25 discount functions on each store." Its network
`fetch` target "is limited to custom apps installed on Shopify Plus and Enterprise stores."
(fetched-verbatim on the quoted parts)

**Draft orders (server-side price).** `draftOrderCreate` takes custom line items (title plus
`originalUnitPriceWithCurrency`, no variant) or a variant with `priceOverride`: "This price will
be used in place of the product variant's catalog price in this draft order." Lines take
`customAttributes`. The customer pays through the invoice URL or `draftOrderInvoiceSend`.
Scope `write_draft_orders`. (fetched-verbatim on the field descriptions). A draft-order creation
rate limit was **not found** on the page.

**Third-party product-options apps.** Example: Easify Custom Product Options, free plan, then
$9.99 / $19.99 / $99.99 per month; "Price (formula, per character, one time)" and "variant
upcharges". The listing does not say how the upcharge is charged (hidden add-on product,
cart transform, or draft order). (fetched-summary). One app checked only; a second listing URL
404ed.

**Can the price be set server-side so the client cannot tamper with it?**
- **Yes, fully**, with a draft order (our server writes the price) or a Plus-store cart
  transform (Shopify runs the function server-side; the buyer can still tamper with the
  attributes it reads, so the function must derive the price from the attributes, not trust a
  price attribute).
- **Not at add-to-cart time** on a non-Plus store with our own custom app: there is no price
  field to set, and Functions in custom apps need Plus. The buyer can always pick a cheaper
  variant than their colors deserve. The defence is to check after the order arrives (Q5,
  recommendation).

Sources:
- https://shopify.dev/docs/apps/build/functions (fetched, twice)
- https://shopify.dev/docs/api/functions/latest#availability (fetched)
- https://shopify.dev/docs/api/functions/latest/cart-transform (fetched three times; the third asked for exact sentences)
- https://shopify.dev/docs/apps/build/product-merchandising/bundles/add-customized-bundle (fetched; no plan or price facts)
- https://shopify.dev/docs/api/functions/latest/discount (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/draftOrderCreate (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/input-objects/DraftOrderLineItemInput (fetched)
- https://apps.shopify.com/easify-product-options (fetched); https://apps.shopify.com/globo-product-options (404)

## Q5. Getting orders to our backend

**Webhooks.**
- Topics `orders/create`, `orders/paid`, `orders/updated`, `orders/fulfilled`,
  `fulfillments/create` and the `fulfillment_orders/*` family are listed. (fetched-summary)
- HMAC: "compute HMAC-SHA256 of the raw request body using your app's client secret as the
  key, then compare it to the decoded header value" (`X-Shopify-Hmac-SHA256`, base64). "Reject
  any delivery where the signatures don't match." HMAC applies to HTTPS delivery, not Pub/Sub or
  EventBridge. (fetched-verbatim)
- Timing: "a one-second connection timeout and a five-second timeout for the entire request";
  anything outside 2xx, "including 3XX codes, is treated as an error". (fetched-verbatim)
- Retries: "it retries 8 times over the next 4 hours"; after 8 consecutive failures "the
  subscription is automatically deleted if it was configured using the Admin API". (fetched-verbatim)
- Duplicates and order: dedupe on `X-Shopify-Webhook-Id`; `X-Shopify-Event-Id` correlates
  deliveries from one merchant action (fetched-verbatim). Shopify "doesn't guarantee ordering
  within a topic"; "webhook delivery isn't always guaranteed", so run a periodic reconciliation
  that fetches by `updated_at`. (fetched-summary)

**Admin GraphQL API.**
- Rate limit by plan, points per second: Standard 100, Advanced 200, Plus 1000, Enterprise
  2000. "A single query may not exceed a cost of 1,000 points, regardless of plan limits."
  Leaky bucket. (fetched-verbatim)
- Orders: "Only the last 60 days' worth of orders from a store are accessible from the `Order`
  object by default"; older orders need `read_all_orders`. (fetched-verbatim)
- Fulfillment with tracking: `fulfillmentCreate` takes `lineItemsByFulfillmentOrder` (pick
  specific lines, so partial fulfillment), `trackingInfo` (company, number, url),
  `notifyCustomer`, `originAddress`. Scopes `write_assigned_fulfillment_orders` or
  `write_merchant_managed_fulfillment_orders` or `write_third_party_fulfillment_orders`. With no
  lines given, "the mutation fulfills all items in the fulfillment order." (fetched-summary)
- Holds: `fulfillmentOrderHold` "Applies a fulfillment hold on a fulfillment order", can hold
  specific lines, max 10 active holds per fulfillment order per app (since 2025-01).
  (fetched-summary)

**Custom app versus public app.**
- Custom distribution: one store (or several in one Plus organization), no approval, cannot
  bill through Shopify. Public: many stores, review required. Admin-created apps are
  deprecated: "No longer available for new apps"; custom apps are now made in the Dev
  Dashboard, and the help centre refers to "legacy custom apps created before January 1, 2026".
  (fetched-summary). A first summary also said custom apps "cannot leverage ... app extensions";
  re-asked for exact text, the only such sentence is "Can't use app extensions" on the
  **admin-created** (deprecated) row, not on custom distribution.
- **Plan gate on customer data (load-bearing):** "To access Custom Level 2 PII apps, your store
  must be on the Grow plan or higher." and "If you sign up for or downgrade your plan to the
  Basic plan, then you won't have access to Custom Level 2 Personally Identifiable Information
  (PII) apps." (help.shopify.com custom apps; fetched-verbatim). Level 2 is "name, address,
  phone, or email". So **on Basic, our own app would not get the shipping name and address.**

**Mandatory privacy webhooks.** `customers/data_request`, `customers/redact`, `shop/redact`;
"If your app is distributed through the Shopify App Store, it must be subscribed" to them.
Return 401 on a bad HMAC; act within 30 days; `shop/redact` arrives 48 hours after uninstall.
(fetched-summary). The pages checked tie the mandate to App Store apps; whether a
custom-distribution app must subscribe was **not found** in the 2 pages checked.

Sources:
- https://shopify.dev/docs/api/webhooks/latest (fetched)
- https://shopify.dev/docs/apps/build/webhooks/subscribe/https (fetched)
- https://shopify.dev/docs/apps/build/webhooks/best-practices (fetched)
- https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Order (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentCreate (fetched)
- https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentOrderHold (fetched)
- https://shopify.dev/docs/apps/launch/distribution (fetched, twice)
- https://help.shopify.com/en/manual/apps/app-types/custom-apps (fetched, twice)
- https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance (fetched)

## Q6. Made-to-order

- **Inventory.** "Continue selling when out of stock" is a per product/variant setting in the
  Inventory section. Untracked inventory ("Inventory not tracked") is a setting; the pages
  checked did not spell out the buying behaviour when tracking is off (not found in 3 pages).
  My recall is that untracked items are always purchasable (unverified recall); either setting
  would serve a made-to-order item.
- **Pre-orders.** "Shopify does not offer native pre-order functionality"; a pre-order app is
  needed, and pre-orders are "only available to merchants using Shopify Payments or Paypal
  Express", with full, partial or no payment at order time. (fetched-summary). Cart transforms
  are not supported with pre-orders (Q4). **We do not need pre-orders:** made-to-order with full
  payment up front and a stated lead time is an ordinary order.
- **Lead-time messaging.** No Shopify feature for this was found in the pages checked; the
  usual route is product-page text (theme or app block) and the order confirmation template.
  Our reasoning, not a Shopify page.
- **Fulfillment statuses.** Unfulfilled, In progress, On hold, Scheduled, Partially fulfilled,
  Fulfilled, Fulfillment not required. Partially fulfilled: "When you fulfill part of the items
  in an order." (help.shopify.com order status; fetched-verbatim on the quoted parts). Partial
  fulfillment through the API is `fulfillmentCreate` with selected lines (Q5). "In progress"
  maps to "printing".

Sources:
- https://help.shopify.com/en/manual/products/inventory/setup/selling-when-out-of-stock (fetched)
- https://help.shopify.com/en/manual/products/inventory/setup/set-up-inventory-tracking (fetched)
- https://help.shopify.com/en/manual/products/inventory/getting-started-with-inventory/inventory-tracking (fetched; table of contents only)
- https://help.shopify.com/en/manual/products/purchase-options/pre-orders (fetched)
- https://help.shopify.com/en/manual/orders/order-status (fetched)
- https://help.shopify.com/en/manual/fulfillment/managing-orders/order-status (fetched)
- https://help.shopify.com/en/manual/fulfillment/fulfilling-orders/fulfill-orders (fetched; statuses not on it)

## Q7. Plans and payment fees (US)

**The plans are now Basic, Grow, Advanced and Plus.** The plan formerly called "Shopify" is
listed as **Grow**; the help centre also names Starter, Lite, Retail, Shopify for enterprise
and an "Agentic plan" (fetched-summary, plan-features index). I did not find a page saying
Grow is the renamed "Shopify" plan (not found on the Grow page); the price point matches.

| Plan | Monthly billing | Yearly billing (per month) | Shopify Payments online | In person | Third-party gateway fee |
|---|---|---|---|---|---|
| Basic | $39 | $29 | 2.9% + 30¢ | 2.6% + 10¢ | 2% |
| Grow | $105 | $79 | 2.7% + 30¢ | 2.5% + 10¢ | 1% |
| Advanced | $399 | $299 | 2.5% + 30¢ | 2.4% + 10¢ | 0.6% |
| Plus | from $2,300 | n/a | 2.25% + 30¢ | 2.3% + 10¢ | 0.2% |

(shopify.com/pricing; fetched-summary, one fetch.) International cards: "Online international
rates + 1%" (same page, fetched-summary).

- **Starter:** "The Starter plan isn't available to new stores." and a merchant who leaves it
  "can't revert back to the Starter plan." (fetched-verbatim). The shopify.com/starter page now
  shows only a free trial and a "$1/month" offer (fetched-summary).
- **Shop Pay Installments merchant fee: not found** in the 6 pages checked (help centre
  overview, eligibility, payouts-and-fees, US payment methods, US Shopify Payments,
  shop-pay-installments marketing page; shopify.com/pricing also lacks it). What was found:
  eligible US order range "$35 to $30,000 USD ... including discounts, shipping, and taxes";
  needs Shopify Payments and Shop Pay; US entity with USD payouts (fetched-summary). The
  marketing page's "Rates from 0-36% APR" is the **buyer's** APR, not our fee. My recall of a
  5.9% + 30¢ merchant rate is **unverified recall** and must not go into the price model until
  checked in the admin.

Sources:
- https://www.shopify.com/pricing (fetched, twice)
- https://help.shopify.com/en/manual/intro-to-shopify/pricing-plans/plans-features/plan-features (fetched)
- https://help.shopify.com/en/manual/intro-to-shopify/pricing-plans/plans-features/shopify-starter-plan (fetched, twice)
- https://help.shopify.com/en/manual/intro-to-shopify/pricing-plans/plans-features/grow-plan (fetched)
- https://www.shopify.com/starter (fetched)
- https://help.shopify.com/en/manual/payments/shop-pay-installments (fetched)
- https://help.shopify.com/en/manual/payments/shop-pay-installments/eligibility (fetched)
- https://help.shopify.com/en/manual/payments/shop-pay-installments/payouts-and-fees (fetched)
- https://www.shopify.com/shop-pay-installments (fetched)
- https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries/united-states (fetched)
- https://help.shopify.com/en/manual/payments/shopify-payments/supported-countries/united-states/payment-methods (fetched)
- https://help.shopify.com/en/manual/payments/shop-pay-installments/fees (fetched; nothing on fees)

## Q8. Taxes, shipping, international (brief)

- **Shopify Tax pricing.** Stores created before May 13, 2026 are free up to an **annual**
  $100,000 of global sales; stores created **on or after May 13, 2026** are free up to a
  **lifetime** $100,000. Above it, US stores pay 0.35% (Basic/Grow/Advanced) or 0.25% (Plus) on
  orders from regions where tax collection is on. (help.shopify.com Shopify Tax pricing;
  fetched-summary). A new store opened now falls under the lifetime rule.
- **Shipping profiles.** A general profile plus "up to 99 custom shipping profiles".
  (fetched-summary). Rate types named on the pages checked: flat, free, carrier-calculated
  (fetched-summary). Which plans get carrier-calculated rates at checkout was **not found** in
  the 3 pages checked; Starter could not use third-party carrier-calculated shipping
  (fetched-summary).
- **Small light parcels.** Shopify Shipping offers USPS Ground Advantage (2-5 business days),
  Priority Mail, First-Class Mail and others; label rates are "based on Shopify's account with
  USPS". A sub-1-lb Ground Advantage tier was **not found** on that page. (fetched-summary). A
  coaster or a set of 4 is well under a pound, so a flat or weight-based rate in one profile is
  enough to start.
- **Markets.** Markets sells in local currencies, handles duties and import taxes, and can
  redirect by region (fetched-summary). Markets-per-plan limits and Managed Markets fees were
  **not found** on the page checked. Suggest US-only at launch.

Sources:
- https://help.shopify.com/en/manual/taxes/shopify-tax/pricing (fetched)
- https://help.shopify.com/en/manual/taxes/shopify-tax (fetched)
- https://help.shopify.com/en/manual/shipping/setting-up-and-managing-your-shipping/shipping-profiles (fetched)
- https://help.shopify.com/en/manual/shipping/setting-up-and-managing-your-shipping/setting-up-shipping-rates (fetched)
- https://help.shopify.com/en/manual/shipping/setting-up-and-managing-your-shipping/carrier-calculated-shipping (fetched; plan facts not on it)
- https://help.shopify.com/en/manual/shipping/shopify-shipping/shipping-carriers/usps (fetched)
- https://help.shopify.com/en/manual/shipping/understanding-shipping/shopify-shipping (fetched; facts not on it)
- https://help.shopify.com/en/manual/international (fetched)

## Q9. Selling the same catalog on Etsy

- **Shopify's own channel does not list Etsy.** Shopify Marketplace Connect (developer:
  Shopify) covers "Amazon, Target Plus, Walmart, and eBay". Pricing: "First 50
  marketplace-synced orders/mo free, 1% fee per additional synced-order, capped at $99/month."
  (apps.shopify.com/marketplace-connect; fetched-summary). Etsy was not on that listing or on
  the help-centre Marketplace Connect page (not found in 3 pages; I did not find a statement
  that Etsy was dropped, only its absence).
- **Third-party Etsy integrations exist.** Etsy Integration by CedCommerce: from $9/month
  (Beginner $9, Standard $29, Growth $59), 7-day trial, syncs listings, inventory, orders and
  pricing, "Built for Shopify", 4.5 stars over 1,249 reviews. LitCommerce (eBay, Etsy, Amazon
  and more): $29/month or $278/year. (both fetched-summary)
- **Does personalization carry over?** Neither app listing mentions personalization: the
  CedCommerce page contains none of "personalization", "personalisation" or "custom text"
  (fetched, asked for exact matches), and LitCommerce has no Etsy-specific personalization
  sentence. Etsy's own help and fee pages returned 403 to both WebFetch and curl, and the Etsy
  API reference page came back as navigation only. So **whether an Etsy buyer's
  personalization text lands on the synced Shopify order is unknown** from the pages checked.
  Since a per-ring color set cannot be an Etsy variation anyway (Etsy variations are few; my
  recall, unverified), an Etsy listing would most likely sell fixed themes or "send us your
  share link" in the personalization box, handled by hand.

Sources:
- https://apps.shopify.com/marketplace-connect (fetched)
- https://help.shopify.com/en/manual/online-sales-channels/shopify-marketplace-connect (fetched)
- https://help.shopify.com/en/manual/online-sales-channels/shopify-marketplace-connect/etsy (fetched; no Etsy content)
- https://apps.shopify.com/etsy-marketplace-integration (fetched, twice)
- https://apps.shopify.com/litcommerce (fetched)
- https://apps.shopify.com/search?q=etsy (fetched; results failed to load)
- https://www.etsy.com/legal/fees/ and https://help.etsy.com/hc/en-us/articles/360000336247-How-to-Add-Personalization-to-a-Listing (403)
- https://developers.etsy.com/documentation/reference (fetched; navigation only)

## Q10. Customer data and privacy duties for an app that receives orders

- Protected customer data is "Data that directly relates to a customer or prospective
  customer", including orders and shipping information. Level 1 is that data without name,
  address, phone and email; Level 2 includes them. Custom apps get access without review;
  public apps must request it. Fields an app is not approved for "will be redacted" and come
  back `null`. (shopify.dev protected-customer-data; fetched-summary)
- Duties: process "only the minimum personal data required", be transparent with the
  merchant, "Limit your processing of personal data to the stated purposes", honour consent
  and opt-outs, set "retention periods", "Encrypt data at rest and in transit". Level 2 adds
  encrypted backups, separate test and production, data-loss prevention, staff access limits
  and strong passwords, access logging and an incident-response policy. (fetched-summary)
- The Basic-plan block on custom Level 2 apps (Q5) is the sharpest constraint found.
- Orders API: "Only use orders data if it's required for your app's functionality. Shopify
  will restrict access to scopes for apps that don't have a legitimate use for the associated
  data." (fetched-summary)
- Compliance webhooks: mandatory for App Store apps (Q5); for our custom app, cheap to add
  and they give a clear path for deletion requests.

Sources:
- https://shopify.dev/docs/apps/launch/protected-customer-data (fetched)
- https://help.shopify.com/en/manual/apps/app-types/custom-apps (fetched)
- https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance (fetched)

---

## Recommendation (researcher B)

**Plan: Grow, not Basic.** Basic blocks a custom app from customer name and address
(Q5, Q10), and our backend needs the address to ship. Grow is $79/month billed yearly with
2.7% + 30¢ online. A Basic store could still work if labels are bought by hand in the Shopify
admin and our backend only sees order lines, but that cuts the order sync in half. Plus is the
only plan where our own app can run Functions, and $2,300/month is far out of proportion.

**Integration path: the Lab stays outside; the Storefront API cart hands off to Shopify
checkout.** The Lab, on its own domain, builds a Storefront API cart (Headless channel token):
one line per distinct coaster (or set), each carrying a few short attributes (pattern, size,
finish tier, the share URL or a config id, and a `_sig` signature, below). It then sends the
buyer to `checkoutUrl`. This is the one path in Q3 that carries per-coaster colors for a
multi-coaster order from an external site without an app proxy. The theme product page has a
"Design yours" link into the Lab (a plain link, or a small app block later). Cart permalinks
are the fallback for a single-coaster "buy this theme" link (25 properties, first product
only).

**Pricing mechanism: price-tier variants, plus a check after the order arrives.** One
"Custom coaster" product per pattern family (or one overall) with three options that carry
the price drivers, for example Size × Finish tier (Matte / Silk+ / Sparkle, priced by the
dearest finish in the configuration) × Set (single / 4 with holder / 6 with holder). That is
a few dozen variants, well under 2,048. A custom theme surcharge is a separate add-on product
line. Per-ring colors go in attributes only. Because a buyer can pick a cheaper variant than
the colors justify, the Lab's server signs (variant id + config) into a private `_sig`
attribute; our backend recomputes it when the order arrives and puts a fulfillment hold on any
line whose signature or finish tier does not match, then contacts the buyer. Draft orders
(server-set `priceOverride`, invoice link) cover the rare quote: a large or unusual order.
A public app with a cart transform is the only fully server-priced cart on a non-Plus store
and needs App Store review; not worth it at launch.

**Order sync: one custom app (Dev Dashboard, custom distribution) with webhooks plus a
nightly sweep.** Subscribe to `orders/paid` (start production), `orders/create` (run the
signature check early) and `orders/updated`, plus `orders/cancelled` (that topic was not
among the ones I confirmed on the topic list; check it). Verify the HMAC on the raw
body, answer 200 inside 5 seconds and queue the work, dedupe on `X-Shopify-Webhook-Id`, and
run a nightly GraphQL sweep by `updated_at` because delivery is not guaranteed and a
subscription is deleted after 8 failures. Mark lines "In progress" while printing, then
`fulfillmentCreate` with the shipped lines and tracking (partial fulfillment when a set of 6
spans plates finishing on different days). Subscribe to the three privacy webhooks even though
the mandate names App Store apps.

**Open items for the design doc.** Line-property and attribute size limits (not found); the
Shop Pay Installments merchant fee (not found); whether Etsy personalization reaches the
Shopify order (not found); Oxygen plan eligibility (only needed if we go headless).
