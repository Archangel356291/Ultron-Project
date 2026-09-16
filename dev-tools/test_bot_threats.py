"""Self-check for the Discord bot's /threats command (Sentinel parity).

Uses the fake discord package: registers the real command function and
calls it directly with a fake interaction against a scripted backend
response, proving the embed carries the watchdog's numbers, goes red only
when a finding is error-level, and that the unauthorized path is refused.

Run standalone from anywhere:
    python dev-tools/test_bot_threats.py
"""
import asyncio
import os
import sys

BOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-discord-bot")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BOT_DIR)

os.environ["DISCORD_BOT_TOKEN"] = "fake-discord-token"
os.environ["ULTRON_API_TOKEN"] = "fake-api-token"
os.environ["ULTRON_BACKEND_URL"] = "http://backend.test:5000"
os.environ["ULTRON_DISCORD_ALLOWED_USERS"] = "1001"

import discord  # noqa: E402
import bot  # noqa: E402


def demo():
    clean = {"enabled": True, "interval_seconds": 300, "last_run": "2026-09-16T16:28:00",
             "active_findings": [], "active_count": 0}
    embed = bot.format_threats_embed(clean)
    assert embed.title.startswith("Sentinel")
    assert embed.color == bot.BRAND_COLOR
    fields = {f["name"]: f["value"] for f in embed.fields}
    assert fields["Watching"] == "every 5 min" and fields["Active findings"] == "none", fields
    assert fields["Last check"] == "2026-09-16 16:28:00"

    hot = {"enabled": True, "interval_seconds": 300, "last_run": "2026-09-16T16:33:00", "active_count": 2,
           "active_findings": [
               {"key": "container_down:jellyfin", "status": "warning", "summary": "container jellyfin is not running"},
               {"key": "lockout:203.0.113.9", "status": "error", "summary": "sign-in lockout active for 203.0.113.9"},
           ]}
    embed = bot.format_threats_embed(hot)
    assert embed.color == bot.ERROR_COLOR, "an error-level finding must turn the embed red"
    names = [f["name"] for f in embed.fields]
    assert names.count("WARN") == 1 and names.count("CRIT") == 1, names

    disabled = {"enabled": False, "interval_seconds": 0, "last_run": None, "active_findings": []}
    fields = {f["name"]: f["value"] for f in bot.format_threats_embed(disabled).fields}
    assert fields["Watching"].startswith("disabled") and fields["Last check"] == "not yet", fields

    # The command end to end through the fake interaction: authorized user
    # gets the embed from the scripted backend; a stranger is refused
    # before any backend call.
    bot.bot.http_session = None  # backend_get is replaced below; no session needed

    async def fake_backend_get(session, path):
        assert path == "/api/security/threats", path
        return hot
    bot.backend_get = fake_backend_get

    ok = discord.Interaction(user_id=1001)
    asyncio.run(bot.threats_command(ok))
    assert ok.response.deferred
    sent = ok.followup.sent[-1]
    assert sent.embed.title.startswith("Sentinel") and sent.embed.color == bot.ERROR_COLOR

    stranger = discord.Interaction(user_id=4242)
    asyncio.run(bot.threats_command(stranger))
    assert stranger.response.sent and "Not authorized" in stranger.response.sent["content"]
    assert not stranger.followup.sent, "an unauthorized user must never reach the backend"

    print("OK: /threats renders Sentinel's watching/last-check/findings, turns red only on an "
          "error-level finding, handles the disabled state, and refuses unauthorized users.")


if __name__ == "__main__":
    demo()
