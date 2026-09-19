"""Per-user API-key vault: keys are namespaced per identity, encrypted at
rest, values are never returned, and ONLY the owner falls back to env vars."""
import os
import sys
import sqlite3
import tempfile

_TMP = tempfile.mkdtemp(prefix="odin-vault-test-")
os.environ["ODIN_DB_PATH"] = os.path.join(_TMP, "odin.db")
os.environ["ODIN_API_TOKEN"] = "owner-token"
os.environ["ODIN_GRAPH_ENCRYPTION_KEY"] = "test-vault-seed"
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
os.environ["SHOPIFY_TOKEN_ENVONLY"] = "env-value-should-not-leak"

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend"))
import app  # noqa: E402


def as_owner():
    app.g.role, app.g.beta_name = "admin", None


def as_beta(name):
    app.g.role, app.g.beta_name = "beta", name


def demo():
    assert app._VAULT is not None, "cryptography must be installed for the vault"
    with app.app.test_request_context():
        # owner stores a Shopify token
        as_owner()
        assert app.set_user_key("SHOPIFY_TOKEN", "owner-secret").get("ok")
        assert app.get_user_key("SHOPIFY_TOKEN") == "owner-secret"

        # a beta user stores their OWN Shopify token
        as_beta("alice")
        assert app.set_user_key("SHOPIFY_TOKEN", "alice-secret").get("ok")
        assert app.get_user_key("SHOPIFY_TOKEN") == "alice-secret", "beta must get her own key"

        # isolation: switching back to owner still yields the owner's key
        as_owner()
        assert app.get_user_key("SHOPIFY_TOKEN") == "owner-secret", "keys must not cross identities"

        # a beta user NEVER receives the owner's env vars
        as_beta("bob")
        assert app.get_user_key("SHOPIFY_TOKEN") is None, "bob set nothing -> None"
        assert app.get_user_key("SHOPIFY_TOKEN_ENVONLY") is None, "non-owner must NOT get env fallback"

        # the owner DOES fall back to env for an unset key
        as_owner()
        assert app.get_user_key("SHOPIFY_TOKEN_ENVONLY") == "env-value-should-not-leak"

        # list returns which keys are set, but NEVER the values
        as_beta("alice")
        listing = app.list_user_keys()
        assert listing["identity"] == "beta:alice"
        names = {k["name"] for k in listing["keys"]}
        assert names == {"SHOPIFY_TOKEN"}, names
        assert "alice-secret" not in repr(listing), "values must never be returned"

    # encrypted at rest: the raw DB never holds the plaintext
    raw = sqlite3.connect(os.environ["ODIN_DB_PATH"]).execute(
        "SELECT value_enc FROM user_settings").fetchall()
    blob = " ".join(r[0] for r in raw)
    assert "owner-secret" not in blob and "alice-secret" not in blob, "values must be encrypted at rest"

    print("OK: per-user vault isolates keys, encrypts at rest, hides values, owner-only env fallback.")


if __name__ == "__main__":
    demo()
