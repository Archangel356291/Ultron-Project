# -*- coding: utf-8 -*-
# Offline check for the live-crypto parser: no network, pure arithmetic.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fake_pkgs"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "odin-backend"))
os.environ.setdefault("ODIN_API_TOKEN", "dev-preview-token")
import app

# blockstream returns satoshis in chain_stats (confirmed) + mempool_stats (pending)
d = app._btc_parse({
    "chain_stats":   {"funded_txo_sum": 150000000, "spent_txo_sum": 50000000, "tx_count": 3},
    "mempool_stats": {"funded_txo_sum": 10000000,  "spent_txo_sum": 0,        "tx_count": 1},
})
assert d["confirmed"] == 1.0, d          # (1.5 - 0.5) BTC confirmed
assert d["pending"] == 0.1, d            # 0.1 BTC pending
assert d["balance"] == 1.1, d            # total
assert d["tx_count"] == 4, d

# empty address parses to zero, never throws
z = app._btc_parse({})
assert z["balance"] == 0 and z["confirmed"] == 0, z
print("OK: BTC live parser sums confirmed+pending, handles empty, read-only.")
