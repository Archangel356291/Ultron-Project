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

# address validation: an allowlist guards every chain before a network call,
# so junk / injection payloads never reach a URL or RPC body.
assert app._valid_addr("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq")   # bech32
assert app._valid_addr("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")   # ETH hex
assert app._valid_addr("DQkwDpRYUyNNnoEZDf5Cb3QwB1Kk3n1Bdd")           # DOGE base58
assert not app._valid_addr("")                                          # empty
assert not app._valid_addr("bad addr; rm -rf")                          # spaces/punctuation
assert not app._valid_addr("http://evil/inject?x=1")                    # url injection
assert not app._valid_addr("x" * 200)                                   # over length

# SOL: lamports -> SOL (1e9), stubbed RPC so there is no network
app._http_post_json = lambda url, payload, timeout=12: ({"result": {"value": 2500000000}}, None)
d, err = app._sol_live("So11111111111111111111111111111111111111112")
assert err is None and d["balance"] == 2.5, (d, err)
d, err = app._sol_live("not valid!")
assert d is None and err, (d, err)

# DOGE: koinu -> DOGE (1e8), confirmed + unconfirmed, stubbed explorer
app._http_get_json = lambda url, headers=None, timeout=12: ({"balance": 500000000, "unconfirmed_balance": 100000000}, None)
d, err = app._doge_live("DQkwDpRYUyNNnoEZDf5Cb3QwB1Kk3n1Bdd")
assert err is None and d["confirmed"] == 5.0 and d["pending"] == 1.0 and d["balance"] == 6.0, (d, err)

print("OK: BTC/SOL/DOGE parsers correct; address allowlist blocks junk & injection; read-only.")
