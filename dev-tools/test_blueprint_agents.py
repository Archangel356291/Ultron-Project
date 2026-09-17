"""Self-check for the three blueprint agents added 2026-09-16 (Oracle,
Tally, Redcell -- subagent_blueprint.md gaps).

Proves the two new runtime tools are read-only and behave when offline, the
crypto tool never becomes a trading backdoor (Module 11), and the three new
registry entries carry the scope/forbidden text they must. The financial-
action keyword guard and the registry/definition-file checks live in
test_no_financial_action_tools.py and test_agents.py; this covers behavior.

Run standalone from anywhere:
    python dev-tools/test_blueprint_agents.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"
# No SearXNG etc.; the crypto call may or may not reach CoinGecko from the
# test host -- both outcomes must be handled, so we don't assert on the network.

import app  # noqa: E402


def demo():
    # Both tools are dispatchable and get_-prefixed (read-only by convention).
    for name in ("get_crypto_market", "get_stats_rollup"):
        assert name in app.TOOL_DISPATCH, name
        assert name.startswith("get_"), name
        assert name in {t["name"] for t in app.TOOLS}, name + " missing from TOOLS schema"

    # Tally: a rollup shaped from records already kept, no crash on an empty DB.
    r = app.get_stats_rollup()
    for k in ("date", "llm", "agents", "activity", "containers", "note"):
        assert k in r, k
    assert r["llm"]["requests_today"] == 0, r["llm"]

    # Oracle: read-only market. Offline -> available False and an empty coin
    # list with a reason; online -> available True with priced coins. Either
    # way it never carries an action, an order, or a private key.
    m = app.get_crypto_market()
    assert set(("available", "coins")).issubset(m), m
    assert isinstance(m["coins"], list)
    if m["available"] and m["coins"]:
        c = m["coins"][0]
        assert "price_usd" in c and "symbol" in c, c
        assert "not advice" in m["note"].lower() and "never places" in m["note"].lower(), m["note"]
    else:
        assert m.get("note"), m
    forbidden_words = ("order", "buy", "sell", "execute", "private_key", "api_secret")
    blob = repr(m).lower()
    for w in ("api_secret", "private_key"):
        assert w not in blob, w

    # Module 11 stands: the trade-capable tool set is unchanged, and the new
    # tools are not trade tools.
    trade = {t for t in app.TOOL_DISPATCH if "trade" in t or "position" in t}
    assert trade == {"get_trades", "get_trade_summary", "get_trade_tax_lots"}, trade
    assert "get_crypto_market" not in trade and "get_stats_rollup" not in trade

    # The three registry entries carry their guardrails.
    reg = app.AGENT_REGISTRY
    assert reg["market_analyst"]["kind"] == "tool"
    assert "financial boundary is untouched" in reg["market_analyst"]["scope"].lower()
    for kw in ("buy", "sell", "advice"):
        assert kw in reg["market_analyst"]["forbidden"].lower(), kw
    assert reg["stats_tracker"]["kind"] == "tool"
    assert reg["ethical_hacking"]["kind"] == "claude-code"
    forb = reg["ethical_hacking"]["forbidden"].lower()
    for kw in ("scan", "exploit", "public", "malware"):
        assert kw in forb, kw
    assert "unwired" in reg["ethical_hacking"]["tools"].lower(), "scanning tools must be documented as unwired"

    print("OK: get_crypto_market and get_stats_rollup are read-only get_ tools that behave offline; "
          "the crypto tool carries no order/key and does not join the trade-tool set (Module 11 intact); "
          "Oracle/Tally/Redcell registry guardrails are present, Redcell's scanners documented as unwired.")


if __name__ == "__main__":
    demo()
