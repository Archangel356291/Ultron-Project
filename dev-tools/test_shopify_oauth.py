# -*- coding: utf-8 -*-
# Security checks for the Shopify OAuth connect flow: HMAC verification (using
# Shopify's own documented example vector) and shop-domain validation. No network.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fake_pkgs"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "odin-backend"))
os.environ.setdefault("ODIN_API_TOKEN", "dev-preview-token")
import app

# --- HMAC verification: Shopify's canonical example (secret "hush") ---
good = {
    "code": "0907a61c0c8d55e99db179b68161bc00",
    "shop": "some-shop.myshopify.com",
    "state": "0.6784241404160823",
    "timestamp": "1337178173",
    "hmac": "700e2dadb827fcc8609e9d5ce208b2e9cdaab9df07390d2cbca10d7c328fc4bf",
}
assert app._shopify_verify_hmac(good, "hush") is True, "valid HMAC must pass"

# wrong secret -> reject
assert app._shopify_verify_hmac(good, "wrong-secret") is False, "wrong secret must fail"

# tampered param -> reject (attacker changes shop but keeps old hmac)
tampered = dict(good, shop="evil-shop.myshopify.com")
assert app._shopify_verify_hmac(tampered, "hush") is False, "tampered params must fail"

# missing hmac -> reject
nohmac = {k: v for k, v in good.items() if k != "hmac"}
assert app._shopify_verify_hmac(nohmac, "hush") is False, "missing hmac must fail"

# --- shop domain allowlist: only real *.myshopify.com ---
assert app._shopify_shop_ok("mikaaf-11.myshopify.com") == "mikaaf-11.myshopify.com"
assert app._shopify_shop_ok("https://mikaaf-11.myshopify.com/") == "mikaaf-11.myshopify.com"
assert app._shopify_shop_ok("evil.com") is None
assert app._shopify_shop_ok("mikaaf-11.myshopify.com.evil.com") is None
assert app._shopify_shop_ok("mikaaf-11.myshopify.com/../x") is None
assert app._shopify_shop_ok("") is None

print("OK: Shopify OAuth HMAC verifies the real signature, rejects wrong/tampered/missing; shop allowlist blocks spoofed domains.")
