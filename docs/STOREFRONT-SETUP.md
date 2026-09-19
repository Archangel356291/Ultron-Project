# Odin's Eye — Storefront Setup Guide (Shopify + AI Dropshipping)

This is the step-by-step to get the two village storefronts —
**Trade Post (Shopify)** and **Dropship Docks (AI dropshipping)** — from "off"
to actually taking orders and feeding sales into your Odin's Eye ledger.

**What Odin's Eye does vs. what stays with you**

| Odin's Eye (the AI) | You (the human) |
|---|---|
| Stores *your* API keys, encrypted, private to your account | Create the Shopify + supplier accounts |
| Pulls orders/sales into the ledger; tracks revenue, tax, net | Own the money — payouts land in **your** bank via Shopify |
| Drafts listing copy / SEO / product ideas | Approve pricing and hit publish |
| Flags restocks, tallies tax owed, keeps the sales log folder | File taxes; accept Shopify's terms |

The AI never holds funds, never creates accounts, and never moves money on its
own. It runs the busywork; you own the store and the bank account.

---

## Part 1 — Set up your Shopify store (the seller side)

1. **Create the account.** Go to shopify.com and start the free trial (it
   usually rolls into a discounted intro rate, e.g. ~$1/mo for the first few
   months). Enter your real business details — this is your legal dashboard.
2. **Pick the Basic plan.** Cheapest tier that still has payments, checkout, and
   full app-store access — everything a beginner store needs.
3. **Turn on payments.** Settings → Payments → enable **Shopify Payments** (or a
   gateway like Stripe/PayPal) so customers can check out. Payouts go to your
   bank; Odin's Eye never touches this.
4. **Generate your policies.** Settings → Policies → use Shopify's built-in
   generators for Refund, Privacy, and Terms of Service. Do not skip this —
   suppliers and customers expect them.
5. **Apply a theme.** Online Store → Themes. The free **Dawn** theme is clean
   and conversion-optimized; start there.

## Part 2 — Set up AI dropshipping (the automation side)

The heavy automation lives *inside* Shopify via apps — Odin's Eye reads the
results, it doesn't replace these tools.

1. **Install an AI store/dropship app.** e.g. **AutoDS** or **DSers** (both
   integrate into the Shopify admin). AutoDS also has an AI store builder that
   generates layouts, banners, and placeholders for a chosen niche.
2. **Find winning products with AI research.** Use the app's product-research
   features (they scrape TikTok Creative Center, Amazon, AliExpress, etc.) to
   surface high-demand, low-competition items instead of guessing.
3. **Import products in one click.** The importer pulls images, variants, and
   dimensions straight into your Shopify inventory.
4. **Optimize listings with generative AI.** Use **Shopify Magic** (built in)
   for SEO titles, descriptions, and benefit bullets — or let Odin's Eye draft
   them for you and paste them in.
5. **Automate fulfillment.** With AutoDS/DSers connected, a customer order auto-
   purchases from the supplier, forwards the shipping address, and marks the
   order shipped — no manual packing.
6. **Add AI customer service.** Install a chat widget (e.g. Tidio) so an
   autonomous bot handles order status, returns, and FAQs 24/7.

## Part 3 — Connect it to Odin's Eye (5 minutes)

1. **Get a Shopify Admin API token.** In your Shopify admin: **Settings → Apps
   and sales channels → Develop apps → Create an app → Configure Admin API
   scopes** (grant read for orders/products; add write only if you want the AI
   to draft/update listings) → **Install app** → copy the **Admin API access
   token** (starts with `shpat_`).
2. **Open the storefront in the village.** Reload Odin's Eye → **Valhalla** tab →
   click the **SHOPIFY** building (or *Open Ledger*).
3. **Paste your keys** under **"Your API keys"** (they're encrypted and private
   to *your* login — never shared with other users or the owner):
   - `SHOPIFY_STORE` → `your-store.myshopify.com`
   - `SHOPIFY_ADMIN_TOKEN` → the `shpat_...` token
   - (Dropship Docks also takes `DROPSHIP_API_KEY` → your AutoDS/DSers key)
4. **Flip the storefront ON** with the toggle at the top of the village (or in
   the panel). It ships **OFF** so it's opt-in.
5. **Verify.** Record a test sale in the panel, or wait for the first real order
   to sync. Every sale lands in the ledger folder with its tax:
   `…/storefront-ledger/` (per-store CSV + a master `ledger.jsonl`).

## The two decisions to make before you launch

- **Niche** — pick one (tech accessories, apparel, pet, home decor, fitness…).
  A focused store converts far better than a general one.
- **Budget** — set an initial number for the store + first ad tests, and hold to
  it. Track spend against sales in the ledger.

---

### Odin's Eye endpoints (for reference / your own scripts)

- `GET /api/storefronts` — list + revenue/tax totals
- `POST /api/storefronts/<id>/active` `{active:true|false}` — toggle
- `POST /api/storefronts/<id>/sales` `{item,subtotal,tax_rate|tax,...}` — record
- `GET /api/me/keys` / `POST /api/me/keys` `{name,value}` — your private key vault

All require your Bearer token; keys are per-user and encrypted at rest.
