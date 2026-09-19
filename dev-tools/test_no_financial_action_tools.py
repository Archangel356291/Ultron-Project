"""Module 11: the permanent, not training-wheels, rule -- Odin never
executes a real trade or financial action, full stop. Unlike Module 7's
human-review gate (explicitly expected to relax after 10-20 trusted
sessions), this one doesn't have a sunset condition.

The system prompt says this now (see ODIN_SYSTEM_PROMPT's "Hard
limits" section), but a prompt is not enforcement -- this test is the
actual enforcement's regression guard: it fails loudly the moment
anyone ever adds a tool capable of executing a financial action,
forcing that to be a deliberate, visible decision (updating this test,
which means explaining why) rather than a capability that quietly
slipped in alongside an unrelated feature -- e.g. while wiring Module
10's runtime graph, or any future memory/retrieval work, into chat.

Run standalone from anywhere:
    python dev-tools/test_no_financial_action_tools.py
"""
import os
import re
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"

import app  # noqa: E402

# Deliberately broad, not a precise regex -- the point is to catch
# anything that COULD be a financial-action tool by name, and force a
# human to look at it, not to be a clever perfect classifier. A false
# alarm here costs one look at a tool name; a missed real one defeats
# the entire point of this test.
_ACTION_KEYWORDS = (
    "execute_trade", "place_trade", "place_order", "submit_order",
    "buy", "sell", "transfer", "withdraw", "deposit", "send_payment",
    "swap", "convert_currency", "close_position", "open_position",
    "add_trade", "record_trade", "delete_trade", "cancel_order",
)

# The read-only trade tools that DO exist and are fine -- named here
# explicitly so a rename doesn't silently evade the keyword scan below
# without a human noticing (the assertion checks these are exactly the
# trade-related tools present, not just "some are present").
_EXPECTED_TRADE_READ_TOOLS = {"get_trades", "get_trade_summary", "get_trade_tax_lots"}


def demo():
    tool_names = set(app.TOOL_DISPATCH.keys())

    trade_related = {t for t in tool_names if "trade" in t.lower() or "position" in t.lower()}
    assert trade_related == _EXPECTED_TRADE_READ_TOOLS, (
        f"trade-related tools changed: expected exactly {_EXPECTED_TRADE_READ_TOOLS}, "
        f"found {trade_related}. If this is a deliberate, reviewed addition, update this "
        f"test's expectations explicitly -- don't just widen the assertion to pass."
    )
    for name in _EXPECTED_TRADE_READ_TOOLS:
        assert name.startswith("get_"), f"{name} isn't a get_-prefixed read tool"

    for name in tool_names:
        lowered = name.lower()
        for kw in _ACTION_KEYWORDS:
            assert kw not in lowered, (
                f"tool {name!r} matches financial-action keyword {kw!r} -- Module 11's rule is "
                f"that Odin has NO tool that executes a trade or financial action, permanently. "
                f"If this is real and deliberate, it needs a human-confirmed dashboard action-token "
                f"flow (like /api/actions/backup and /api/actions/deploy-container already use), "
                f"never a bare chat-callable tool -- and this test needs to be consciously updated "
                f"to acknowledge that, not silently pass."
            )

    # Same check against beta's (narrower) tool scope, for completeness --
    # it's already a subset of TOOL_DISPATCH, but worth asserting directly
    # rather than assuming the subset relationship always holds.
    for name in app.BETA_ALLOWED_TOOLS:
        lowered = name.lower()
        for kw in _ACTION_KEYWORDS:
            assert kw not in lowered, f"BETA_ALLOWED_TOOLS contains {name!r}, matching {kw!r}"

    # The system prompt itself states this rule -- a lightweight check
    # that the actual guidance text hasn't been quietly removed.
    prompt = app.ODIN_SYSTEM_PROMPT.lower()
    assert "no tool that executes a trade or any financial action" in prompt, (
        "the permanent financial-action rule's own sentence seems to have been edited out "
        "of the system prompt -- Module 11 requires this stated explicitly, not just enforced "
        "by tool absence"
    )

    print(f"OK: no financial-action-capable tool exists in TOOL_DISPATCH ({len(tool_names)} tools) "
          f"or BETA_ALLOWED_TOOLS, trade tools are exactly the expected read-only set, and the "
          f"system prompt still states the permanent rule.")


if __name__ == "__main__":
    demo()
