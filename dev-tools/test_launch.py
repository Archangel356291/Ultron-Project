"""Launch board: seeds current products/campaigns, tracks stage -> progress, and
logs every change so nothing is lost before launch."""
import os
import sys
import tempfile

_TMP = tempfile.mkdtemp(prefix="odin-launch-test-")
os.environ["ODIN_DB_PATH"] = os.path.join(_TMP, "odin.db")
os.environ["ODIN_API_TOKEN"] = "t"
os.environ["ODIN_GRAPH_ENCRYPTION_KEY"] = "seed"
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend"))
import app  # noqa: E402


def demo():
    s = app.launch_summary()
    assert len(s["products"]) == 2 and len(s["campaigns"]) == 3, (len(s["products"]), len(s["campaigns"]))
    tee = next(p for p in s["products"] if "Keeper of Small Fires" in p["name"])
    assert tee["stage"] == "Design" and tee["progress"] == 40, tee   # (1+1)/5

    # advance the tee to Listed -> 80%
    r = app.launch_upsert({"id": tee["id"], "stage": "Listed"})
    assert r.get("ok"), r
    tee2 = next(p for p in app.launch_summary()["products"] if p["id"] == tee["id"])
    assert tee2["stage"] == "Listed" and tee2["progress"] == 80, tee2

    # add a new campaign item
    r2 = app.launch_upsert({"kind": "campaign", "name": "Video 4 - behind the scenes", "stage": "Idea"})
    assert r2.get("ok"), r2
    assert len(app.launch_summary()["campaigns"]) == 4

    # bad input rejected
    assert "error" in app.launch_upsert({"kind": "nope", "name": "x"})
    assert "error" in app.launch_upsert({"kind": "product", "stage": "Wat", "name": "y"})

    # records logged
    log = os.path.join(app.LAUNCH_LOG_DIR, "launch.jsonl")
    assert os.path.isfile(log) and sum(1 for _ in open(log, encoding="utf-8")) >= 2, "stage changes logged"

    # --- Odin-drafts-the-work pipeline ---
    # every non-terminal stage of every ladder has an assigned agent + task,
    # and the terminal stage deliberately has none (that step is the human's).
    for kind, ladder in app.LAUNCH_LADDERS.items():
        for st in ladder[:-1]:
            assert (kind, st) in app.LAUNCH_TASKS, (kind, st)
        assert (kind, ladder[-1]) not in app.LAUNCH_TASKS, (kind, ladder[-1])

    # without an LLM key, drafting refuses cleanly (503) and changes nothing.
    app.anthropic_client = None
    res, code = app.launch_draft(tee["id"])
    assert code == 503 and "error" in res, (code, res)

    # with the LLM stubbed, drafting saves an artifact, assigns the agent,
    # and advances the stage -- but never past the terminal (publish) stage.
    app.anthropic_client = object()
    app.run_ultron_chat = lambda msg, hist, **kw: ("DRAFT: a cozy Norse design brief.", [], [])
    idea = app.launch_upsert({"kind": "product", "name": "Runestone mug", "stage": "Idea"})
    res, code = app.launch_draft(idea["id"])
    assert code == 200 and res["ok"], (code, res)
    assert res["agent"] == "store_scout" and res["stage"] == "Design", res
    got = next(p for p in app.launch_summary()["products"] if p["id"] == idea["id"])
    assert got["agent"] == "store_scout" and len(got["artifacts"]) == 1, got
    assert got["artifacts"][0]["text"].startswith("DRAFT:"), got

    print("OK: launch board seeds items, tracks stage->progress, logs changes, and Odin drafts each step (human keeps the publish).")


if __name__ == "__main__":
    demo()
