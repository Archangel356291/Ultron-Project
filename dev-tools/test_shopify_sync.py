"""Shopify order sync: records real orders into the ledger, deduped by order id,
and fails cleanly when no keys are set. (No network -- exercises the record path
with mocked orders, which is what the live fetch feeds into.)"""
import os
import sys
import tempfile

_TMP = tempfile.mkdtemp(prefix="odin-shopify-test-")
os.environ["ODIN_DB_PATH"] = os.path.join(_TMP, "odin.db")
os.environ["ODIN_API_TOKEN"] = "t"
os.environ["ODIN_GRAPH_ENCRYPTION_KEY"] = "seed"
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend"))
import app  # noqa: E402


def demo():
    orders = [
        {"id": 1001, "current_subtotal_price": "35.00", "current_total_tax": "2.80",
         "line_items": [{"title": "Raven Tee", "quantity": 2}]},
        {"id": 1002, "subtotal_price": "20.00", "total_tax": "1.60",
         "line_items": [{"title": "Rune Mug", "quantity": 1}]},
    ]
    r = app._shopify_record_orders("trade-post", orders)
    assert r["synced"] == 2 and r["skipped"] == 0, r

    # re-syncing the same orders is idempotent (dedupe by order id)
    r2 = app._shopify_record_orders("trade-post", orders)
    assert r2["synced"] == 0 and r2["skipped"] == 2, r2

    # a new order gets picked up
    r3 = app._shopify_record_orders("trade-post", orders + [
        {"id": 1003, "current_subtotal_price": "12.00", "current_total_tax": "0.96",
         "line_items": [{"title": "Wax Candle", "quantity": 1}]}])
    assert r3["synced"] == 1 and r3["skipped"] == 2, r3

    # ledger reflects it: gross 35+20+12 = 67, tax 2.80+1.60+0.96 = 5.36
    tp = next(s for s in app.storefront_summary()["storefronts"] if s["id"] == "trade-post")
    assert tp["gross"] == 67.0 and tp["tax"] == 5.36 and tp["sales"] == 3, tp

    # no keys -> a clean error, not a crash
    o, e = app._shopify_fetch_orders("", "")
    assert o is None and "no Shopify" in e, (o, e)

    print("OK: Shopify sync records orders, dedupes by id, and errors cleanly without keys.")


if __name__ == "__main__":
    demo()
