---
date: 2026-10-04
produced-by: researcher A (fresh agent), Claude Opus 5.5, one of two independent researchers; pages opened directly by URL with a web-fetch tool (the session's web-search budget was already spent, so no source below comes from a search snippet)
feeds:
  - docs/design/storefront/shopify-storefront-design.md (being written, in a separate step)
---

# Selling configured coasters on Shopify, researcher A

What this is: what Shopify supports on 2026-10-04 for selling a coaster that a customer
configures in our own Coaster Lab (hosted outside Shopify), at what cost and with what limits.
The storefront itself will be built in a separate repo; this file decides which designs are
feasible. My own recommendation is at the end, kept apart from the findings.

How to read it:

- **Fetched** means I opened the page on 2026-10-04 and read the value from it. The fetch tool
  hands back a model's reading of the page, so a "quote" below is the tool's quote of the page;
  the load-bearing ones were asked for verbatim, and a checker should re-open them.
- **Not fetched (prior knowledge)** marks the few places where I say something I did not read
  on a page today. None of them is load-bearing for the recommendation, and each is labelled.
- **Not found in N pages** means I looked on the N pages named and the fact was not there. It
  does not mean Shopify lacks the feature.
- Everything is dated 2026-10-04. Prices and limits change; each is that day's reading.

## Q1. Products, variants and options

| Fact | Value | Source | Status |
|---|---|---|---|
| Variants per product | "You can create up to 2,048 variants for a product." | [help: add variants](https://help.shopify.com/en/manual/products/variants/add-variants) | fetched |
| Options per product | "Each product can have up to three options." | same | fetched |
| Values per option | not stated on that page | same | not found in 1 page |
| Going past 2,048 | "use a third-party app from the Shopify App Store, or customize your theme code" | same | fetched |
| Bulk variant creation throttle | once a store has 500,000 variants, at most 10,000 new variants a day on any API; does not apply to Plus | [dev: API limits](https://shopify.dev/docs/api/usage/limits) | fetched |
| Array inputs | "Input arguments that accept an array have a maximum size of 250, on every Shopify API." | same | fetched |
| Theme AJAX product reads | product responses are capped at 250 variants | [dev: AJAX API](https://shopify.dev/docs/api/ajax) | fetched |

**What this means for per-ring colors.** A coaster has several rings plus a frame, each picked
from about 100 colors. Four color slots alone give 100^4 = 100,000,000 combinations, which is
far over 2,048 variants and over the three-option limit before size or finish is counted. So
per-ring colors cannot be variants. They have to travel as line item properties (Q2) or as
data held by our backend and referenced from the line. Variants can still carry the few
choices that change price: size, finish tier, set size, standard or custom theme. Even a
small grid like 3 sizes × 4 finish tiers × 2 theme kinds = 24 variants fits easily. Note the
three-option limit: size, finish and theme kind use all three, so set size (single, 4, 6)
must be a separate product, a bundle (Q4), or folded into one of the three options.

## Q2. Line item properties and cart attributes

| Fact | Value | Source | Status |
|---|---|---|---|
| Theme form, line properties | inputs named `properties[name]` inside the product form | [dev: Liquid line_item](https://shopify.dev/docs/api/liquid/objects/line_item#line_item-properties) | fetched |
| Theme form, cart attributes | inputs named `attributes[name]` | [dev: cart template](https://shopify.dev/docs/storefronts/themes/architecture/templates/cart#cart-attributes) | fetched |
| Private (hidden) properties | prefix the key with `_` to hide it from customers at checkout, e.g. `properties[_hiddenPropertyName]` | [dev: Liquid line_item](https://shopify.dev/docs/api/liquid/objects/line_item#line_item-properties) and [dev: AJAX cart](https://shopify.dev/docs/api/ajax/reference/cart) | fetched |
| AJAX cart, `/cart/add.js` | `items` array of `{id, quantity, properties, selling_plan}`; `properties` "must be an object of key-value pairs" | [dev: AJAX cart](https://shopify.dev/docs/api/ajax/reference/cart) | fetched |
| AJAX cart attributes | set with `/cart/update.js` and `attributes: {...}` | same | fetched |
| Storefront API | `cartCreate` / `cartLinesAdd` take `attributes` on each line (`CartLineInput`) and on the cart; up to 250 lines per `cartLinesAdd` request | [dev: manage a cart](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/cart/manage), [dev: cartLinesAdd](https://shopify.dev/docs/api/storefront/latest/mutations/cartLinesAdd) | fetched |
| Shows on the order | Admin API `LineItem.customAttributes`: "A list of attributes that represent custom features or special requests." `Order.customAttributes`: "additional information that has been attached to the order" | [dev: LineItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem), [dev: Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order) | fetched |
| Order note length | "The maximum length is 5000 characters." | [dev: Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order) | fetched |
| Cart errors about size | `CART_TOO_LARGE` "The cart is too large to save.", `NOTE_TOO_LONG` | [dev: CartErrorCode](https://shopify.dev/docs/api/storefront/latest/enums/CartErrorCode) | fetched |
| Size limit on one property key or value, or on the count of properties | **not found in 6 pages**: AJAX cart reference, Liquid `line_item`, cart template, `AttributeInput`, Storefront cart guide, `cartLinesAdd` | those pages | not found |

The practical reading: a share URL (a few hundred characters) or a short config id fits in one
property comfortably by any reasonable limit, but no page I opened states the limit, so the
design should keep the payload small (an id plus a human-readable color list) rather than an
encoded full configuration. `CART_TOO_LARGE` shows there is a ceiling somewhere.

## Q3. Embedding or linking an external configurator

| Path | What the docs say | Source | Status |
|---|---|---|---|
| App proxy | proxies `https://<shop>/[prefix]/[subpath]` to our app URL; "Each app can have only one proxy route configured"; a response with `Content-Type: application/liquid` is rendered in the shop's theme; `Set-Cookie`, `Cookie` and other headers are stripped; needs `write_app_proxy` | [dev: app proxies](https://shopify.dev/docs/apps/build/online-store/app-proxies) | fetched |
| App proxy auth | Shopify adds `signature`, "A hexadecimal encoded SHA-256 HMAC of the other parameters", plus `logged_in_customer_id`; "The signature check only guarantees that the request hasn't been tampered with" | [dev: authenticate app proxies](https://shopify.dev/docs/apps/build/online-store/app-proxies/authenticate-app-proxies) | fetched |
| Theme app extension | app blocks and app embed blocks; work only on "Online Store 2.0 themes" | [dev: theme app extensions](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions) | fetched |
| Theme app extension limits | all files 10 MB; Liquid 100 KB across files; at most 30 blocks; CSS 100 KB and JS 10 KB compressed (suggested, not enforced); assets served from Shopify's CDN | [dev: extension configuration](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions/configuration) | fetched |
| Admin-created custom apps | "No longer available for new apps"; existing ones keep working; they "Cannot use App Bridge, app extensions, or the billing system" | [dev: distribution](https://shopify.dev/docs/apps/launch/distribution) | fetched |
| Custom distribution apps | one store (or several in one Plus organization); no review; cannot bill through Shopify | same | fetched |
| New custom apps live in the Dev Dashboard | "If you have legacy custom apps created before January 1, 2026, you can manage them from your Shopify admin" | [help: custom apps](https://help.shopify.com/en/manual/apps/app-types/custom-apps) | fetched |
| AJAX cart `/cart/add.js` | works only "in themes that are hosted by Shopify", not on other domains; unauthenticated; "no hard rate limits" but abuse prevention applies | [dev: AJAX API](https://shopify.dev/docs/api/ajax) | fetched |
| Cart permalink | `https://{shop}/cart/{variant_id}:{qty},...`; goes to checkout by default, `storefront=true` goes to the cart; "line item properties (up to 25) to the first product", Base64 URL-encoded JSON; `attributes[...]` and `note` show in the order's Notes; "Selling plans don't work with cart permalinks" | [dev: cart permalinks](https://shopify.dev/docs/apps/build/checkout/cart-permalinks) | fetched |
| Storefront API cart | Headless channel issues public and private tokens, at most 100 storefronts and tokens per shop; tokenless access exists with query complexity capped at 1,000; buyer traffic has no fixed per-minute cap, checkout creation is throttled | [dev: Storefront API getting started](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/getting-started), [dev: Storefront API](https://shopify.dev/docs/api/storefront) | fetched |
| Storefront API checkout | the cart's `checkoutUrl` "redirects customers through Shopify's web checkout" | [dev: manage a cart](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/cart/manage) | fetched |
| Hydrogen on Oxygen | "Oxygen is available at no extra charge on paid Shopify plans: Starter, Basic, Grow, Advanced, Plus, Pause and build"; dev stores and trials get no public environment | [dev: Hydrogen fundamentals](https://shopify.dev/docs/storefronts/headless/hydrogen/fundamentals) | fetched |
| iframe in a theme section | no Shopify page on embedding a third-party iframe was opened; a custom Liquid section can hold any HTML | none | not fetched (prior knowledge) |

Pros and cons, my reading of the above:

- **Link out, then cart permalink back.** The Lab stays where it is; it builds a permalink with
  the chosen variant and up to 25 properties on the first product, and sends the customer to
  checkout or the cart. Pros: no app, no Shopify code, works on any plan. Cons: properties only
  on the first product, so a mixed cart of differently configured coasters needs a cart that
  already holds the others (`storefront=true`) or one permalink per configured item; the URL is
  fully client-built, so any value in it can be edited by the customer (Q4 covers price).
- **Storefront API cart from the Lab.** The Lab (its server, with a private token, or the
  browser with a public one) calls `cartCreate`/`cartLinesAdd` with per-line attributes, then
  redirects to `checkoutUrl`. Pros: any number of configured lines, each with its own
  attributes; CORS-free for a server; one cart across several coasters. Cons: the Lab must keep
  the cart id (cookie) to add more items; the theme's own cart page does not see this cart
  unless the shop is fully headless (not checked on any page).
- **iframe of the Lab inside a theme page, posting to `/cart/add.js`.** The Lab sends the
  config to the parent page (postMessage), and theme JavaScript on the shop's own domain calls
  `/cart/add.js`. Pros: the customer never leaves the shop; the theme cart stays the single
  cart. Cons: two pieces of JavaScript in two repos must agree; iframe sizing and mobile
  layout; the iframe mechanics rest on prior knowledge, not a fetched page.
- **App proxy.** Serves the Lab (or its API) under the shop's own domain, with a Shopify HMAC
  on each request. Pros: same-origin, so the Lab page could call `/cart/add.js` directly; the
  signature proves a request came through Shopify. Cons: needs an app (Dev Dashboard, custom
  distribution); cookies are stripped; one proxy route per app; the Lab's own host still runs.
- **Theme app extension (app block).** Puts a "Configure" block on the product page. Pros: the
  merchant can place it without code. Cons: JS budget of 10 KB is suggested, so a full Lab
  bundle belongs on our host and is loaded or framed by the block; needs an app; Online
  Store 2.0 themes only.
- **Headless Hydrogen.** The whole shop is ours on Oxygen at no extra charge. Pros: the Lab and
  the shop are one app. Cons: we build and run the whole storefront (catalog, cart, SEO,
  accounts), which is the largest piece of work here; checkout is still Shopify's.

## Q4. Setting a price for a configured item

| Mechanism | What the docs say | Source | Status |
|---|---|---|---|
| Client cannot set a price | `CartLine.cost` is "The cost of the merchandise that the buyer will pay for at checkout"; no Storefront cart field sets a price. The AJAX cart reference describes no price field | [dev: CartLine](https://shopify.dev/docs/api/storefront/latest/objects/CartLine), [dev: AJAX cart](https://shopify.dev/docs/api/ajax/reference/cart) | fetched (absence on 2 pages) |
| Variants | price is the variant's price, set by us in admin; see Q1 limits | Q1 sources | fetched |
| Function availability | "stores on any plan can use public apps that are distributed through the Shopify App Store and contain functions"; "Only stores on a Shopify Plus plan can use custom apps that contain Shopify Function APIs" | [dev: Functions](https://shopify.dev/docs/api/functions), [dev: build Functions](https://shopify.dev/docs/apps/build/functions) | fetched |
| Function limits | binary 256 kB; input 128 kB; output 20 kB; 11 million instructions (up to 200 items) | [dev: Functions](https://shopify.dev/docs/api/functions) | fetched |
| Cart transform operations | `lineExpand`, `linesMerge`, `lineUpdate` ("override the price, title, and image of a cart line item") | [dev: Cart Transform API](https://shopify.dev/docs/api/functions/latest/cart-transform) | fetched |
| `lineUpdate` plan | "Only development stores or stores on a Shopify Plus plan can use apps with lineUpdate operations." | same | fetched |
| `lineExpand` price | expanded items accept a `fixedPricePerUnit` price adjustment; the input query can read line attributes (`attribute(key: ...)`) | same | fetched |
| Cart transforms per store | one per app; if several apps have one, all run; operations rejected "if a selling plan is present" | same | fetched |
| Discount functions | read cart line attributes; outputs `productDiscountsAdd`, `orderDiscountsAdd`, `deliveryDiscountsAdd`; "You can activate a maximum of 25 discount functions on each store." | [dev: Discount Function API](https://shopify.dev/docs/api/functions/latest/discount) | fetched |
| Discounts raising a price | not stated; the API speaks only of reductions | same | not found in 2 pages |
| Draft orders | a custom line item takes `title` and `originalUnitPriceWithCurrency` with no variant ("`variantId` ... Must be null for custom line items"); `priceOverride` on a variant line; `customAttributes`; `invoiceUrl` is "The link to the checkout, which is sent to the customer in the invoice email"; needs `write_draft_orders` | [dev: draftOrderCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/draftOrderCreate), [dev: DraftOrderLineItemInput](https://shopify.dev/docs/api/admin-graphql/latest/input-objects/DraftOrderLineItemInput), [dev: DraftOrder](https://shopify.dev/docs/api/admin-graphql/latest/objects/DraftOrder) | fetched |
| Draft order rate limits | not stated | same 3 pages | not found in 3 pages |
| Shopify Bundles (first party) | free, "available on all Shopify plans"; fixed bundles up to 30 components; "Maximum of 3 options and 100 variants total per bundle"; Online Store or Headless only; a component's price change does not update the bundle price | [help: Shopify Bundles](https://help.shopify.com/en/manual/products/bundles/shopify-bundles) | fetched |
| Third-party options app (one example) | Easify Custom Product Options: free plan, then $9.99, $19.99, $99.99 a month; pricing by "formula, per character, one time"; "Built for Shopify", 4.9 stars over 3,106 reviews | [App Store: Easify](https://apps.shopify.com/easify-product-options) | fetched |
| How options apps charge the add-on price | the Easify listing says add-on prices appear in the cart as line items; how (hidden add-on product, cart transform, or other) is not stated | same | not found in 1 page |

**Can a price be set server-side without the customer tampering with it?** From the pages above:

- **Variant price:** yes, the price lives in Shopify, but the customer chooses the variant. A
  customer could pick a cheaper variant (say a Matte tier) while the properties name Silk+
  colors. The price is safe; the match between price and configuration is not, so our backend
  must check it (Q5).
- **Draft order:** yes. Our server computes the price and creates the draft order through the
  Admin API, and the customer only gets the `invoiceUrl`. Nothing on the client sets the price.
  The cost is that the customer leaves the normal cart: one invoice per configured order.
- **Cart transform `lineExpand` with `fixedPricePerUnit`:** the price is computed inside
  Shopify, from line attributes the customer can edit. It is safe only if the function
  recomputes the price from the configuration itself, so an edited configuration is priced as
  what it now describes and the order carries that same configuration. Our own function needs
  either Plus (custom app) or an App Store-listed public app. `lineUpdate` is Plus only.
- **Discount function:** can lower a price computed from attributes; a page saying it can raise
  one was not found, so a "base variant at the top price, discounted down" scheme would be the
  only shape, with the same Plus-or-public-app rule.

## Q5. Getting orders to our backend

| Fact | Value | Source | Status |
|---|---|---|---|
| Delivery targets | "a URL, Google Pub/Sub URI, or Amazon EventBridge ARN" | [dev: webhooks](https://shopify.dev/docs/apps/build/webhooks) | fetched |
| Headers | `X-Shopify-Topic`, `X-Shopify-Webhook-Id`, `X-Shopify-Hmac-Sha256` | same | fetched |
| HMAC | base64 HMAC-SHA256 of the **raw** body with the app's client secret; compare in constant time; "HMAC verification requires the raw request body" | [dev: HTTPS webhooks](https://shopify.dev/docs/apps/build/webhooks/subscribe/https) | fetched |
| Timeouts | "a one-second connection timeout and a five-second timeout for the entire request"; any non-2xx, 3xx included, is retried | same | fetched |
| Retries | "retries 8 times over the next 4 hours"; after 8 consecutive failures, subscriptions configured via the Admin API are deleted | same; [dev: troubleshooting](https://shopify.dev/docs/apps/build/webhooks/troubleshooting-webhooks) says "if failures persist, the subscription is removed" without the API qualifier | fetched |
| Duplicates | dedupe on `X-Shopify-Webhook-Id`; related deliveries share `X-Shopify-Event-Id` | [dev: HTTPS webhooks](https://shopify.dev/docs/apps/build/webhooks/subscribe/https) | fetched |
| Ordering | not stated | 3 webhook pages | not found in 3 pages |
| Topics | `orders/create` "Occurs whenever an order is created"; `orders/paid` "whenever an order is paid"; `orders/partially_fulfilled`, `orders/fulfilled`, `orders/updated`, `orders/cancelled`; `fulfillments/create`. Order topics need `read_orders` (or marketplace/buyer-membership order scopes) | [dev: WebhookSubscriptionTopic](https://shopify.dev/docs/api/admin-graphql/latest/enums/WebhookSubscriptionTopic) | fetched |
| Reading orders | `read_orders`; "Only the last 60 days' worth of orders from a store are accessible ... by default", older needs a request for all orders | [dev: Order](https://shopify.dev/docs/api/admin-graphql/latest/objects/Order) | fetched |
| Fulfillment and tracking | `fulfillmentCreate` with `lineItemsByFulfillmentOrder` (quantities per fulfillment-order line), `trackingInfo` (company, number, URL), `notifyCustomer`; needs a `write_*_fulfillment_orders` scope | [dev: fulfillmentCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentCreate) | fetched |
| GraphQL Admin rate limits | Standard 100 points/s, Advanced 200, Plus 1,000, Enterprise 2,000; one query at most 1,000 points; bulk operations are exempt | [dev: GraphQL Admin rate limits](https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits) | fetched |
| Custom vs public app | public: App Store review, can bill; custom distribution: one store or one Plus organization, no review, no Shopify billing; admin-created: closed to new apps | [dev: distribution](https://shopify.dev/docs/apps/launch/distribution) | fetched |
| Mandatory privacy webhooks | `customers/data_request`, `customers/redact`, `shop/redact` (48 hours after uninstall); act within 30 days; return 401 on a bad HMAC. Stated as required for public App Store apps | [dev: privacy law compliance](https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance) | fetched |
| Whether custom apps must subscribe to them | not stated | 2 pages (privacy compliance, protected customer data) | not found in 2 pages |

## Q6. Made to order

| Fact | Value | Source | Status |
|---|---|---|---|
| Selling past stock | "To continue selling products that are out of stock, select the Continue selling when out of stock option." | [help: inventory tracking](https://help.shopify.com/en/manual/products/inventory/getting-started-with-inventory/set-up-inventory-tracking) | fetched |
| Untracked inventory behavior | the page does not say what "not tracked" does | same | not found in 1 page; that an untracked product never sells out is prior knowledge |
| Pre-orders | need "a pre-order app from the Shopify App Store"; "you can collect full, partial, or no payment at the time the customer places their order"; "only available to merchants using Shopify Payments or Paypal Express" | [help: pre-orders](https://help.shopify.com/en/manual/products/purchase-options/pre-orders) | fetched |
| Lead-time messaging | no native field found | 2 pages (pre-orders, inventory) | not found in 2 pages; theme text or a product metafield is the usual route (prior knowledge) |
| Fulfillment statuses | Unfulfilled, In progress, On hold ("you can't fulfill the order until the fulfillment hold is released"), Scheduled (prepaid subscriptions), Partially fulfilled, Fulfilled, Fulfillment not required | [help: order status](https://help.shopify.com/en/manual/fulfillment/managing-orders/order-status) | fetched |
| Payment statuses | include Authorized, Expiring (two days before the capture deadline), Expired, Paid, Partially paid | same | fetched |
| Partial fulfillment | by quantity per line through `fulfillmentCreate` | [dev: fulfillmentCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentCreate) | fetched (see Q5) |

A made-to-order coaster is not a pre-order in Shopify's sense: it is paid in full and shipped
when printed. Untracked inventory (or "continue selling") plus "In progress" while it prints,
and partial fulfillment when a set ships in parts, covers it. The pre-order apps matter only if
we want to take a deposit.

## Q7. Plans and payment fees (US)

| Plan | Monthly, billed monthly | Monthly, billed yearly | Online card rate (Shopify Payments) | "Premium" online rate | In person | Third-party gateway fee | Staff |
|---|---|---|---|---|---|---|---|
| Basic | $39 | $29 | 2.9% + 30¢ | 3.5% + 30¢ | 2.6% + 10¢ | 2% | none included |
| Grow | $105 | $79 | 2.7% + 30¢ | 3.3% + 30¢ | 2.5% + 10¢ | 1% | up to 5 |
| Advanced | $399 | $299 | 2.5% + 30¢ | 3.1% + 30¢ | 2.4% + 10¢ | 0.6% | up to 15 |
| Plus | from $2,300 | not stated | 2.25% + 30¢ | 2.95% + 30¢ | 2.3% + 10¢ | 0.2% | unlimited |

Source: [shopify.com/pricing](https://www.shopify.com/pricing), fetched. The plan the question
calls "Shopify" is named **Grow** on that page. The page does not define "premium" cards. Its
FAQ: "Third-party transaction fees may apply when you use a third-party payment provider
(instead of Shopify Payments)." The page also offers a 3-day trial, then $1 a month for 3
months. This agrees with the pricing research already checked in, [coaster pricing
§ Shopify](2026-10-04-coaster-pricing.md).

- **Starter:** still exists. The help navigation lists it, the [Starter plan
  page](https://help.shopify.com/en/manual/intro-to-shopify/pricing-plans/plans-features/shopify-starter-plan)
  (fetched) says it sells "through social media platforms or messaging apps" with "product
  links", and only the Spotlight theme; Oxygen lists Starter among paid plans. Its price and
  card rate were not on either page, and the main pricing page does not list it. Price: not
  found in 3 pages.
- **Shop Pay Installments:** US orders "$35 to $30,000 USD" are eligible; needs Shopify Payments
  and Shop Pay; not for password-protected stores, non-English primary language, or B2B
  ([help: Shop Pay Installments](https://help.shopify.com/en/manual/payments/shop-pay-installments),
  [eligibility](https://help.shopify.com/en/manual/payments/shop-pay-installments/eligibility),
  both fetched). **The merchant fee was not found in 6 pages** (those two, the activate page,
  the Shopify Payments FAQ, the rates page and the shopify.com Installments page, which states
  only the customer's "0-36% APR"). A checker should find the fee before the design prices it.

## Q8. Taxes, shipping and international (brief)

- **Shopify Tax** ([help: pricing](https://help.shopify.com/en/manual/taxes/shopify-tax/pricing),
  fetched): 0.35% of US sales on Basic, Grow and Advanced (0.25% on Plus), after a free
  threshold of $100,000. For stores created on or after May 13, 2026 that threshold is
  **lifetime**, not yearly; older stores keep a yearly one and a $5,000 yearly cap per region.
  Per-order cap $0.99. A new store opened now would be in the lifetime group.
- **Shipping profiles** ([help](https://help.shopify.com/en/manual/fulfillment/setup/shipping-profiles),
  fetched): one general profile plus "up to 99 custom shipping profiles".
- **Rates** ([help](https://help.shopify.com/en/manual/fulfillment/setup/shipping-rates/setting-up-shipping-rates),
  fetched): flat, by order amount, or by weight; built-in carrier-calculated rates such as USPS
  "are available on all plans"; your own carrier accounts need "specific Shopify plans or an
  additional monthly fee" (which plans and what fee: not found in 2 pages). A coaster set is a
  small light parcel, so a weight-based rate tier or calculated USPS rates both fit.
- **Markets** ([help](https://help.shopify.com/en/manual/international/markets), fetched):
  currencies, duties and taxes, and international domains from one store. Limits on the number
  of markets and any Managed Markets fee: not found in 1 page.

## Q9. Etsy alongside Shopify

| Fact | Value | Source | Status |
|---|---|---|---|
| Shopify Marketplace Connect | sells on "Amazon, Target Plus, eBay, and Walmart"; Etsy not listed; first 50 synced orders a month free, then 1% per order, capped at $99 a month | [App Store: Marketplace Connect](https://apps.shopify.com/marketplace-connect) | fetched |
| Help page for it | names Google, Amazon and Temu as examples; Etsy not mentioned | [help: Marketplace Connect](https://help.shopify.com/en/manual/online-sales-channels/shopify-marketplace-connect) | fetched |
| Third-party Etsy apps | Etsy Integration by CedCommerce: $9 (10 products), $29 (200 products, 100 orders a month), $59 (1,000 products, 500 orders a month, Etsy-to-Shopify inventory and fulfillment sync); 4.5 stars over 1,249 reviews. The same listing page names InfoShore as another | [App Store: CedCommerce Etsy](https://apps.shopify.com/etsy-marketplace-integration) | fetched |
| Whether Etsy personalization text reaches the Shopify order | not stated | CedCommerce listing | not found in 1 page |
| Etsy's own fees | $0.20 listing, 6.5% transaction, 3% + $0.25 payments in the US, Offsite Ads 15% or 12% | [coaster pricing](2026-10-04-coaster-pricing.md), re-opened there | carried from our checked research |
| Etsy personalization and variation limits | etsy.com and help.etsy.com refused the fetch (403) | — | not fetched |

So no first-party Shopify-to-Etsy channel was found (2 pages), and the third-party apps sync
listings, stock and orders. An Etsy buyer would not use our Lab; a per-ring color choice on
Etsy would have to be Etsy's free-text personalization or a fixed theme listing, and whether
that text arrives on the synced Shopify order is unconfirmed.

## Q10. Customer data and privacy duties for an app receiving orders

| Fact | Value | Source | Status |
|---|---|---|---|
| Two levels | Level 1: customer data without name, address, phone, email. Level 2: with those fields | [dev: protected customer data](https://shopify.dev/docs/apps/launch/protected-customer-data) | fetched |
| Access by app type | public app: review for both levels; custom app: "Always available" for both; admin-created custom app: Level 2 "Varies by plan" | same | fetched |
| Plan rule (help center) | "To access Custom Level 2 PII apps, your store must be on the Grow plan or higher"; downgrading to Basic loses them | [help: custom apps](https://help.shopify.com/en/manual/apps/app-types/custom-apps) | fetched |
| Level 1 duties | minimum data; tell merchants the purpose; limit to it; respect consent and opt-outs; "Encrypt data at rest and in transit"; retention periods | [dev: protected customer data](https://shopify.dev/docs/apps/launch/protected-customer-data) | fetched |
| Level 2 duties | also encrypt backups, separate test and production data, data-loss prevention, limit staff access, strong staff passwords, access logs, incident response | same | fetched |
| Compliance webhooks | see Q5 | — | — |

**A conflict to settle.** The dev page says a (Dev Dashboard) custom app has Level 2 "Always
available" and only an admin-created one "Varies by plan", linking to the help page. The help
page's sentence says "Custom Level 2 PII apps" need Grow or higher, without saying it is limited
to admin-created apps. If it applies to Dev Dashboard custom apps too, then **on Basic, our own
app could not read the customer's name, email or shipping address** from an order. A printing
backend can do without those (Shopify prints the label), but the plan choice depends on which
reading is right. A checker should re-open both.

## Recommendation (researcher A's own)

**Integration path: the Lab builds a Storefront API cart, then hands off to Shopify checkout;
link to the Lab from a product page.** The Lab already owns the configuration and the share URL.
Calling `cartCreate`/`cartLinesAdd` from the Lab's server, with one line per configured coaster
or set and its attributes on the line, supports a cart of several different configurations,
which a cart permalink cannot (properties only on the first product). No Shopify app is needed
for this path: the Headless channel issues the token. If staying inside the theme matters more
than a mixed cart, the fallback is an iframe plus `/cart/add.js` in theme code. Hydrogen is the
most work for the least gain while the Lab lives elsewhere.

**Pricing: price-carrying variants, and a backend check on every order.** Make one product per
sellable unit (single, set of 4 with holder, set of 6 with holder) with variants only on what
changes the price: size, finish tier (Matte, Silk+, Sparkle, or a "mixed" tier priced at the
highest finish used), standard or custom theme. That is well inside 2,048 variants and three
options. The Lab picks the variant from the configuration. Per-ring colors, the construction and
the share URL ride as line properties: a visible, human-readable color list and a private
`_config` id. Draft orders give a fully server-set price but take the customer out of the cart,
so keep them for quotes and large custom orders. Our own cart transform needs Plus or an App
Store app, so it is out at Basic or Grow unless one of those changes. A third-party options app
works on any plan, but how it charges the price was not found, so I would not build on it
without reading its docs.

**Order sync: one Dev Dashboard custom app, webhooks plus GraphQL Admin.** Subscribe to
`orders/paid` (to start printing) and `orders/cancelled`. Verify the HMAC on the raw body, return
200 inside 5 seconds and queue the work, dedupe on `X-Shopify-Webhook-Id`. Then recompute the
price from the `_config` and compare it with the variant paid. On a mismatch, put the order on
hold and ask the customer, rather than printing it. This is the tamper check the variant scheme
needs. Mark work "In progress" while plates print, and write each shipment with
`fulfillmentCreate` and `trackingInfo`, partially when a set ships in parts. Reconcile through
the Admin API on a timer, because a subscription can be deleted after 8 failed deliveries.
Handle the three privacy webhooks anyway, keep only the order id and configuration, and let
Shopify keep the address.

**What decides the plan:** Basic is enough for this path unless the Level 2 data reading (Q10)
says our custom app needs Grow to see names and addresses. Settle that, and the Shop Pay
Installments fee, before the design commits.
