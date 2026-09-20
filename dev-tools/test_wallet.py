"""Crypto wallet ledger: records typed transactions, keeps a running balance per
asset, tracks added/removed, and writes a browsable log folder."""
import os
import sys
import tempfile

_TMP = tempfile.mkdtemp(prefix="odin-wallet-test-")
os.environ["ODIN_DB_PATH"] = os.path.join(_TMP, "odin.db")
os.environ["ODIN_API_TOKEN"] = "t"
os.environ["ODIN_GRAPH_ENCRYPTION_KEY"] = "seed"
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend"))
import app  # noqa: E402


def near(a, b):
    return abs(a - b) < 1e-9


def demo():
    for tx in [
        {"kind": "deposit", "asset": "BTC", "amount": 0.5, "note": "seed"},
        {"kind": "mining_reward", "asset": "BTC", "amount": 0.01, "wallet_label": "rig-1"},
        {"kind": "withdrawal", "asset": "BTC", "amount": 0.1},
        {"kind": "transfer_out", "asset": "BTC", "amount": 0.05},
        {"kind": "adjustment", "asset": "BTC", "amount": -0.01},
        {"kind": "deposit", "asset": "ETH", "amount": 2},
    ]:
        r = app.record_wallet_tx(tx)
        assert r.get("ok"), r

    s = app.wallet_summary()
    bya = {a["asset"]: a for a in s["assets"]}
    assert near(bya["BTC"]["balance"], 0.35), bya["BTC"]          # 0.5+0.01-0.1-0.05-0.01
    assert near(bya["BTC"]["added"], 0.51), bya["BTC"]            # deposit + mining
    assert near(bya["BTC"]["removed"], 0.16), bya["BTC"]          # withdrawal + transfer + adj
    assert bya["BTC"]["count"] == 5, bya["BTC"]
    assert near(bya["ETH"]["balance"], 2.0), bya["ETH"]

    # transaction types are named + a recent history exists
    labels = {t["kind_label"] for t in s["recent"]}
    assert {"Deposit", "Mining reward", "Withdrawal", "Transfer out", "Adjustment"} <= labels, labels

    # bad input rejected cleanly
    assert "error" in app.record_wallet_tx({"kind": "nope", "amount": 1})
    assert "error" in app.record_wallet_tx({"kind": "deposit", "amount": 0})

    # browsable log folder holds the records
    master = os.path.join(app.WALLET_LEDGER_DIR, "wallet.jsonl")
    btc = os.path.join(app.WALLET_LEDGER_DIR, "wallet-BTC.csv")
    assert os.path.isfile(master) and os.path.isfile(btc), os.listdir(app.WALLET_LEDGER_DIR)
    assert "Mining reward" in open(btc, encoding="utf-8").read()

    print("OK: wallet ledger tracks per-asset balance, added/removed, named types, and writes the log folder.")


if __name__ == "__main__":
    demo()
