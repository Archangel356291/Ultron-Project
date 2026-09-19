"""Storefront ledger: records sales with tax, writes a browsable log folder,
and persists the on/off toggle. Runs against a throwaway temp DB/ledger dir."""
import os
import sys
import tempfile

_TMP = tempfile.mkdtemp(prefix="odin-storefront-test-")
os.environ["ODIN_DB_PATH"] = os.path.join(_TMP, "odin.db")
os.environ["ODIN_API_TOKEN"] = "test-token"
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

import app  # noqa: E402


def demo():
    # two storefronts seeded, OFF by default
    summ = app.storefront_summary()
    ids = {s["id"] for s in summ["storefronts"]}
    assert ids == {"trade-post", "dropship-docks"}, ids
    assert all(not s["active"] for s in summ["storefronts"]), "storefronts must start OFF (opt-in)"
    assert summ["totals"] == {"revenue": 0, "tax": 0, "sales": 0}, summ["totals"]

    # toggle persists
    assert app.set_storefront_active("trade-post", True)["active"] is True
    assert next(s for s in app.storefront_summary()["storefronts"] if s["id"] == "trade-post")["active"] is True

    # record a sale -> tax computed from rate, totals update
    r = app.record_storefront_sale("trade-post", {"item": "Raven Tee", "qty": 2, "subtotal": 40.00, "tax_rate": 8.5})
    assert r.get("ok"), r
    assert r["sale"]["tax"] == 3.40, r["sale"]      # 40.00 * 8.5% = 3.40
    assert r["sale"]["total"] == 43.40, r["sale"]

    # explicit tax overrides the rate
    r2 = app.record_storefront_sale("dropship-docks", {"item": "Rune Mug", "subtotal": 20, "tax": 1.75})
    assert r2["sale"]["total"] == 21.75, r2["sale"]

    # summary reflects both sales
    tot = app.storefront_summary()["totals"]
    assert tot["sales"] == 2 and tot["revenue"] == 65.15 and tot["tax"] == 5.15, tot

    # unknown storefront rejected
    assert "error" in app.record_storefront_sale("nope", {"subtotal": 1}), "unknown storefront must error"

    # the browsable log folder holds detailed records
    ledger = app.STOREFRONT_LEDGER_DIR
    master = os.path.join(ledger, "ledger.jsonl")
    per = os.path.join(ledger, "sales-trade-post.csv")
    assert os.path.isfile(master) and os.path.isfile(per), os.listdir(ledger)
    assert "Raven Tee" in open(per, encoding="utf-8").read()
    assert sum(1 for _ in open(master, encoding="utf-8")) == 2, "master ledger has a line per sale"

    print("OK: storefront ledger records sales+tax, writes the log folder, and the on/off toggle persists.")


if __name__ == "__main__":
    demo()
