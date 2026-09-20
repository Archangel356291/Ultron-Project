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

    print("OK: launch board seeds current items, tracks stage->progress, and logs changes.")


if __name__ == "__main__":
    demo()
