"""
Ultron Discord bot — a thin remote-control surface for the existing backend.

This bot does not talk to the host directly and does not duplicate any
monitoring or action logic. Every command is an HTTP call to the same
backend (app.py) the dashboard uses, so there is exactly one implementation
of "what the system status is" and "what happens when you deploy a
container" — here and in the dashboard.

Commands:
    /status       -> GET /api/status
    /containers    -> GET /api/containers
    /storage        -> GET /api/storage
    /systems         -> GET /api/systems
    /repos            -> GET /api/dev/repos
    /diff              -> GET /api/dev/repos/<repo>/diff
    /trades             -> GET /api/trades
    /portfolio           -> GET /api/trades/summary (FIFO realized gain/loss — not tax advice)
    /usage                 -> GET /api/chat/usage (real token usage, cache activity, budget status)
    /mcp                     -> GET /api/mcp/servers (external tool servers, reachability, approval status)
    /export                  -> GET /api/trades/export (CSV file attachment — transactions or tax-lots)
    /backup                 -> POST /api/actions/backup — MUTATES THE HOST, see below
    /deploy                -> POST /api/actions/deploy-container — MUTATES THE HOST, see below
    /ask <message>           -> POST /api/chat (routes through Ultron's LLM brain)
    /forget                    -> clears your chat history with Ultron

/backup and /deploy use the exact same preview-then-confirm flow as the
backend and dashboard: running the command shows what would happen as a
Discord embed with Confirm/Cancel buttons, and nothing happens on the host
until you — specifically you, not just anyone who can see the message —
click Confirm. The confirmation token comes from the backend itself, the
same as it does for the dashboard; this bot doesn't grant itself any
capability the backend doesn't already gate.

/trades and /portfolio are read-only, matching the backend's own chat-tool
boundary: there is no command here to *add* a trade. Recording a financial
transaction is a deliberate action you take directly on the dashboard or
API, not something this bot exposes — same reasoning that keeps /backup and
/deploy behind an explicit confirm instead of being one-shot commands.

Security:
    Every command checks the calling user's Discord ID against
    ULTRON_DISCORD_ALLOWED_USERS before doing anything. Without that
    allowlist, anyone who can see the bot in a server could query or
    control a home lab — this is a remote-control surface, and it's
    scoped tightly on purpose. The Confirm/Cancel buttons on /backup and
    /deploy additionally only respond to the same user who ran the command.

Run:
    pip install -r requirements.txt
    $env:DISCORD_BOT_TOKEN = "..."
    $env:ULTRON_BACKEND_URL = "http://127.0.0.1:5000"
    $env:ULTRON_API_TOKEN = "same token the backend was started with"
    $env:ULTRON_DISCORD_ALLOWED_USERS = "123456789012345678,987654321098765432"
    python bot.py
"""

import io
import os
import re
import sys
import urllib.parse

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
BACKEND_URL = os.environ.get("ULTRON_BACKEND_URL", "http://127.0.0.1:5000")
API_TOKEN = os.environ.get("ULTRON_API_TOKEN")
def _parse_allowed_users(raw):
    ids = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            sys.exit(
                f"ULTRON_DISCORD_ALLOWED_USERS contains a non-numeric entry: '{part}'.\n"
                "Discord user IDs are numeric (right-click a user with Developer Mode "
                "on -> Copy User ID)."
            )
        ids.add(int(part))
    return ids


ALLOWED_USER_IDS = _parse_allowed_users(os.environ.get("ULTRON_DISCORD_ALLOWED_USERS", ""))
# Optional: sync slash commands to one guild only, for instant availability
# while testing. Leave unset to sync globally (takes up to an hour to
# propagate the first time, per Discord's own behavior).
DEV_GUILD_ID = os.environ.get("ULTRON_DISCORD_DEV_GUILD_ID")

if not DISCORD_BOT_TOKEN:
    sys.exit(
        "DISCORD_BOT_TOKEN is not set. Refusing to start.\n"
        "Set it with (PowerShell): $env:DISCORD_BOT_TOKEN = '<your bot token>'"
    )
if not API_TOKEN:
    sys.exit(
        "ULTRON_API_TOKEN is not set. Refusing to start with no backend auth.\n"
        "Use the same token the backend (app.py) was started with."
    )
if not ALLOWED_USER_IDS:
    sys.exit(
        "ULTRON_DISCORD_ALLOWED_USERS is not set. Refusing to start with no\n"
        "allowlist — without it, anyone who can message this bot could query\n"
        "or control your home lab. Set it to a comma-separated list of\n"
        "Discord user IDs (right-click a user in Discord with Developer Mode\n"
        "enabled -> Copy User ID)."
    )

BRAND_COLOR = 0xFF8A1E  # matches the dashboard's --oxide accent
ERROR_COLOR = 0xE0483C

MAX_MESSAGE_CHARS = 4000  # mirrors the backend's own limit


# --------------------------------------------------------------------------
# pure logic — testable without a real Discord or network connection
# --------------------------------------------------------------------------
def is_authorized(user_id, allowed_ids=None):
    allowed_ids = ALLOWED_USER_IDS if allowed_ids is None else allowed_ids
    return user_id in allowed_ids


def format_status_embed(data):
    embed = discord.Embed(title="System Status", color=BRAND_COLOR)
    embed.add_field(name="CPU", value=f"{data.get('cpu_percent', 0):.0f}%", inline=True)
    embed.add_field(name="Memory", value=f"{data.get('mem_percent', 0):.0f}%", inline=True)
    temp = data.get("cpu_temp_c")
    embed.add_field(name="Temp", value=(f"{temp}°C" if temp is not None else "unavailable"), inline=True)
    embed.add_field(name="Uptime", value=data.get("uptime", "—"), inline=True)
    if data.get("containers_error"):
        embed.add_field(name="Containers", value="unavailable: " + data["containers_error"], inline=False)
    else:
        embed.add_field(
            name="Containers",
            value=f"{data.get('containers_running', 0)} / {data.get('containers_total', 0)} running",
            inline=True,
        )
    return embed


def format_containers_embed(data):
    containers = data.get("containers", [])
    embed = discord.Embed(title="Docker Containers", color=BRAND_COLOR)
    if not containers:
        embed.description = "No containers found."
        return embed
    lines = []
    for c in containers:
        marker = "●" if c.get("state") == "running" else "○"
        extra = ""
        if c.get("cpu") or c.get("mem"):
            extra = f"  ({c.get('cpu', '—')}, {c.get('mem', '—')})"
        lines.append(f"{marker} {c.get('name', '?')} — {c.get('state', '?')}{extra}")
    # Discord field values cap at 1024 chars; truncate gracefully rather than error
    body = "\n".join(lines)
    if len(body) > 1000:
        body = body[:1000] + "\n… (truncated, see the dashboard for the full list)"
    embed.description = "```\n" + body + "\n```"
    return embed


def format_storage_embed(data):
    embed = discord.Embed(title="Storage", color=BRAND_COLOR)
    if not data:
        embed.description = "No storage mounts configured."
        return embed
    for label, info in data.items():
        if info.get("error"):
            embed.add_field(name=label, value=f"{info.get('path', '?')}: {info['error']}", inline=False)
        else:
            pct = info.get("percent_used", 0)
            embed.add_field(
                name=label,
                value=f"{info.get('used_gb', 0):.1f} GB / {info.get('total_gb', 0):.1f} GB ({pct:.0f}%)",
                inline=False,
            )
    return embed


def format_systems_embed(data):
    embed = discord.Embed(title="Systems", color=BRAND_COLOR)
    pending = data.get("pending_updates")
    embed.add_field(
        name="Pending updates",
        value=(f"{pending}" if pending is not None else "unavailable on this host"),
        inline=True,
    )
    temp = data.get("cpu_temp_c")
    embed.add_field(name="Temp", value=(f"{temp}°C" if temp is not None else "unavailable"), inline=True)
    embed.add_field(name="Uptime", value=data.get("uptime", "—"), inline=True)
    return embed


# Discord hard-caps an embed description at 4096 chars; leave headroom for
# the ```code fence``` wrapper and a truncation note.
EMBED_CODE_BLOCK_MAX = 3800


def format_repos_embed(data):
    repos = data.get("repos", [])
    embed = discord.Embed(title="Repositories", color=BRAND_COLOR)
    if not repos:
        embed.description = "No repositories configured."
        return embed
    lines = []
    for r in repos:
        if r.get("error"):
            lines.append(f"{r.get('name', '?')}: {r['error']}")
            continue
        status = "uncommitted changes" if r.get("dirty") else "clean"
        commit = r.get("last_commit") or {}
        commit_text = f"{commit.get('message', '?')} ({commit.get('when', '?')})" if commit else "no commits"
        lines.append(f"{r.get('name', '?')} [{r.get('branch', '?')}] — {status} — {commit_text}")
    body = "\n".join(lines)
    if len(body) > EMBED_CODE_BLOCK_MAX:
        body = body[:EMBED_CODE_BLOCK_MAX] + "\n… (truncated, see the dashboard)"
    embed.description = "```\n" + body + "\n```"
    return embed


def format_diff_embed(data):
    repo = data.get("repo", "?")
    embed = discord.Embed(title=f"Diff — {repo}", color=BRAND_COLOR)
    if not data.get("has_changes"):
        embed.description = "No uncommitted changes."
        return embed
    diff_text = data.get("diff", "")
    if len(diff_text) > EMBED_CODE_BLOCK_MAX:
        diff_text = diff_text[:EMBED_CODE_BLOCK_MAX] + "\n… (truncated, see the dashboard for the full diff)"
    embed.description = "```diff\n" + diff_text + "\n```"
    return embed


def format_trades_embed(data):
    trades = data.get("trades", [])
    embed = discord.Embed(title="Trade History", color=BRAND_COLOR)
    if not trades:
        embed.description = "No trades recorded yet."
    else:
        lines = [
            f"{t.get('trade_date', '?')}  {t.get('asset', '?'):<6} {t.get('side', '?'):<4} "
            f"qty={t.get('quantity', '?')} @ ${t.get('price_usd', '?')} (fee ${t.get('fee_usd', 0)})"
            for t in trades
        ]
        body = "\n".join(lines)
        if len(body) > EMBED_CODE_BLOCK_MAX:
            body = body[:EMBED_CODE_BLOCK_MAX] + "\n… (truncated, see the dashboard for the full list)"
        embed.description = "```\n" + body + "\n```"
    if data.get("disclaimer"):
        embed.set_footer(text=data["disclaimer"][:2048])
    return embed


def format_portfolio_embed(data):
    embed = discord.Embed(title="Portfolio — Realized Gain/Loss (FIFO)", color=BRAND_COLOR)
    by_asset = data.get("by_asset", {})
    if not by_asset:
        embed.description = "No realized gains/losses yet — record a buy and a matching sell to see results here."
    else:
        for asset, entry in by_asset.items():
            gain = entry.get("realized_gain_usd", 0)
            holding = entry.get("current_holding_qty", 0)
            value = f"${gain:,.2f} realized · holding {holding}"
            warnings = entry.get("warnings") or []
            if warnings:
                value += "\n⚠️ " + "; ".join(warnings)[:500]
            embed.add_field(name=asset, value=value[:1024], inline=False)
        total = data.get("total_realized_gain_usd", 0)
        embed.description = f"**Total realized: ${total:,.2f}**"
    if data.get("disclaimer"):
        embed.set_footer(text=data["disclaimer"][:2048])
    return embed


def format_usage_embed(data):
    embed = discord.Embed(title="Today's Claude API usage", color=BRAND_COLOR)
    embed.add_field(name="Requests today", value=str(data.get("requests_today", 0)), inline=True)
    embed.add_field(name="Total tokens", value=f"{data.get('total_tokens', 0):,}", inline=True)
    embed.add_field(
        name="Input / Output",
        value=f"{data.get('input_tokens', 0):,} in, {data.get('output_tokens', 0):,} out",
        inline=True,
    )
    cache_read = data.get("cache_read_tokens", 0)
    cache_write = data.get("cache_creation_tokens", 0)
    cache_note = f"{cache_read:,} read from cache, {cache_write:,} written to cache" if (cache_read or cache_write) else "no cache activity yet today"
    embed.add_field(name="Prompt caching", value=cache_note, inline=False)

    budget = data.get("daily_budget")
    if budget is None:
        embed.set_footer(text="No daily budget configured (ULTRON_LLM_DAILY_TOKEN_BUDGET unset — no limit).")
    else:
        total = data.get("total_tokens", 0)
        pct = (total / budget * 100) if budget else 0
        remaining = data.get("budget_remaining", 0)
        embed.add_field(
            name="Daily budget",
            value=f"{total:,} / {budget:,} tokens used ({pct:.0f}%) — {remaining:,} remaining",
            inline=False,
        )
        if pct >= 90:
            embed.color = ERROR_COLOR
    return embed


def format_mcp_servers_embed(data):
    servers = data.get("servers", [])
    embed = discord.Embed(title="External Tools (MCP)", color=BRAND_COLOR)
    if not servers:
        embed.description = "No external tool servers configured (ULTRON_MCP_CONFIG unset)."
        return embed
    for s in servers:
        status = "🟢 reachable" if s.get("reachable") else "🔴 unreachable"
        lines = [s.get("url", "?"), status]
        if not s.get("reachable"):
            lines.append(f"Error: {s.get('error') or 'unknown'}")
        else:
            tools = s.get("tools", [])
            if not tools:
                lines.append("No tools offered.")
            else:
                for t in tools:
                    mark = "✓ approved" if t.get("approved") else "not approved"
                    lines.append(f"{t.get('name', '?')} — {mark}")
        value = "\n".join(lines)
        if len(value) > 1024:
            suffix = "\n… (truncated, see the dashboard)"
            value = value[:1024 - len(suffix)] + suffix
        embed.add_field(name=s.get("name", "?"), value=value, inline=False)
    return embed


def format_connections_embed(data):
    embed = discord.Embed(title="Who's connected", color=BRAND_COLOR)
    people = data.get("people", [])
    if not people:
        embed.description = "No one's connected since the backend last started."
        return embed
    for p in people:
        status = "online" if p.get("online") else f"last seen {p.get('last_seen_seconds_ago', 0)}s ago"
        embed.add_field(
            name=f"{p.get('name')} ({p.get('role')})",
            value=f"{p.get('device_count', 0)} device(s) — {status}",
            inline=False,
        )
    embed.set_footer(text=f"{data.get('online_count', 0)} online now · {data.get('device_count', 0)} device(s) total")
    return embed


def format_error_embed(message):
    embed = discord.Embed(title="Ultron", description=message, color=ERROR_COLOR)
    return embed


def format_chat_embed(reply, tools_used):
    embed = discord.Embed(title="Ultron", description=reply[:4000], color=BRAND_COLOR)
    if tools_used:
        embed.set_footer(text="checked: " + ", ".join(sorted(set(tools_used))))
    return embed


# --------------------------------------------------------------------------
# backend client — the only place that knows the backend's URL shape
# --------------------------------------------------------------------------
class BackendError(Exception):
    """Raised for any backend call that didn't succeed, with a message
    that's already safe to show the user directly."""


async def backend_get(session, path):
    url = BACKEND_URL.rstrip("/") + path
    headers = {"Authorization": "Bearer " + API_TOKEN}
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 401:
                raise BackendError("The backend rejected this token. Check ULTRON_API_TOKEN.")
            if resp.status >= 400:
                # the backend always returns a JSON {"error": "..."} body on
                # failure — parse it out instead of showing the raw response
                data = await resp.json()
                raise BackendError(data.get("error", f"backend returned {resp.status}"))
            return await resp.json()
    except aiohttp.ClientError as e:
        raise BackendError(f"Could not reach the backend at {BACKEND_URL}: {e}")


async def backend_chat(session, message, history):
    url = BACKEND_URL.rstrip("/") + "/api/chat"
    headers = {"Authorization": "Bearer " + API_TOKEN, "Content-Type": "application/json"}
    body = {"message": message, "history": history}
    try:
        # Chat can take a while (LLM + tool calls) — give it real room, matching
        # the backend's own ULTRON_LLM_TIMEOUT_SECONDS default of 60s.
        async with session.post(url, headers=headers, json=body, timeout=aiohttp.ClientTimeout(total=75)) as resp:
            data = await resp.json()
            if resp.status != 200:
                raise BackendError(data.get("error", f"backend returned {resp.status}"))
            return data
    except aiohttp.ClientError as e:
        raise BackendError(f"Could not reach the backend at {BACKEND_URL}: {e}")


async def backend_post(session, path, body):
    """POST helper for the action endpoints. Used for both the initial
    preview call (no confirm_token) and the confirm call (with one) — the
    backend itself distinguishes those, this is just a thin transport."""
    url = BACKEND_URL.rstrip("/") + path
    headers = {"Authorization": "Bearer " + API_TOKEN, "Content-Type": "application/json"}
    try:
        # 130s comfortably exceeds the backend's own 120s deploy timeout.
        async with session.post(url, headers=headers, json=body, timeout=aiohttp.ClientTimeout(total=130)) as resp:
            data = await resp.json()
            if resp.status == 401:
                raise BackendError("The backend rejected this token. Check ULTRON_API_TOKEN.")
            if resp.status >= 400:
                raise BackendError(data.get("error", f"backend returned {resp.status}"))
            return data
    except aiohttp.ClientError as e:
        raise BackendError(f"Could not reach the backend at {BACKEND_URL}: {e}")


async def backend_get_csv(session, path):
    """GET helper for the CSV export endpoint specifically — the response
    is text/csv on success, not JSON, so this can't reuse backend_get()."""
    url = BACKEND_URL.rstrip("/") + path
    headers = {"Authorization": "Bearer " + API_TOKEN}
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status == 401:
                raise BackendError("The backend rejected this token. Check ULTRON_API_TOKEN.")
            if resp.status >= 400:
                # every error path on this endpoint returns JSON, same as the rest of the API
                data = await resp.json()
                raise BackendError(data.get("error", f"backend returned {resp.status}"))
            content_text = await resp.text()
            disposition = resp.headers.get("Content-Disposition", "") if hasattr(resp, "headers") else ""
            match = re.search(r'filename="([^"]+)"', disposition)
            filename = match.group(1) if match else "ultron-export.csv"
            return content_text, filename
    except aiohttp.ClientError as e:
        raise BackendError(f"Could not reach the backend at {BACKEND_URL}: {e}")


def format_backup_preview_embed(preview, expires_in_seconds):
    embed = discord.Embed(title="Backup preview — nothing has run yet", color=BRAND_COLOR)
    embed.add_field(name="Sources", value="\n".join(preview.get("sources", [])) or "none", inline=False)
    embed.add_field(name="Destination", value=preview.get("destination", "?"), inline=False)
    embed.add_field(name="Estimated size", value=f"{preview.get('estimated_size_mb', 0)} MB", inline=False)
    embed.set_footer(text=f"Expires in {max(1, expires_in_seconds // 60)} minute(s) — click Confirm to run it")
    return embed


def format_backup_result_embed(result):
    archived = len(result.get("archives", []))
    failed = len(result.get("errors", []))
    ok = archived > 0 and failed == 0
    desc = f"Backup complete — {archived} archive(s) created"
    if failed:
        desc += f", {failed} failed"
    return discord.Embed(title="Backup result", description=desc, color=(BRAND_COLOR if ok else ERROR_COLOR))


def format_deploy_preview_embed(preview, expires_in_seconds):
    embed = discord.Embed(title="Deploy preview — nothing has run yet", color=BRAND_COLOR)
    embed.add_field(name="Image", value=preview.get("image", "?"), inline=True)
    embed.add_field(name="Name", value=preview.get("name", "?"), inline=True)
    ports_text = ", ".join(f"{host}→{cport}" for cport, host in preview.get("ports", {}).items()) or "none"
    embed.add_field(name="Ports (host→container)", value=ports_text, inline=False)
    env_text = ", ".join(preview.get("env", {}).keys()) or "none"
    embed.add_field(name="Env vars set", value=env_text, inline=False)
    embed.set_footer(text=f"Expires in {max(1, expires_in_seconds // 60)} minute(s) — click Confirm to run it")
    return embed


def format_deploy_result_embed(result):
    desc = f"Deployed **{result.get('image', '?')}** as **{result.get('name', '?')}** " \
           f"({result.get('container_id', '?')[:12]})"
    return discord.Embed(title="Deploy result", description=desc, color=BRAND_COLOR)


# --------------------------------------------------------------------------
# bot wiring
# --------------------------------------------------------------------------
class UltronBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.http_session = None
        # Per-user conversation history, in memory only. Restarting the bot
        # clears it — there's no persistence layer here, same as the
        # dashboard's in-browser-memory chat history.
        self.chat_histories = {}

    async def setup_hook(self):
        self.http_session = aiohttp.ClientSession()
        if DEV_GUILD_ID:
            guild = discord.Object(id=int(DEV_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def close(self):
        if self.http_session:
            await self.http_session.close()
        await super().close()


bot = UltronBot()

# Slightly under the backend's own 300s (5 min) confirmation-token TTL, so
# the Discord button disables itself right around when the token would
# have expired anyway, rather than offering a "Confirm" that then fails.
ACTION_CONFIRM_TIMEOUT_SECONDS = 280


class ConfirmActionView(discord.ui.View):
    """Confirm/Cancel for a previewed action. Only the user who ran the
    original command can use either button — enforced via
    interaction_check, which gates every component in this view."""

    def __init__(self, author_id, action_path, confirm_token, result_embed_fn):
        super().__init__(timeout=ACTION_CONFIRM_TIMEOUT_SECONDS)
        self.author_id = author_id
        self.action_path = action_path
        self.confirm_token = confirm_token
        self.result_embed_fn = result_embed_fn
        self.message = None  # set by the caller right after sending

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Only the person who ran this command can confirm or cancel it.",
                ephemeral=True,
            )
            return False
        return True

    async def on_timeout(self):
        self.disable_all_items()
        if self.message is not None:
            try:
                await self.message.edit(content="Confirmation expired — run the command again.", view=self)
            except discord.HTTPException:
                pass

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.disable_all_items()
        try:
            data = await backend_post(bot.http_session, self.action_path, {"confirm_token": self.confirm_token})
            embed = self.result_embed_fn(data)
        except BackendError as e:
            embed = format_error_embed(str(e))
        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass
        await interaction.followup.send(embed=embed)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_all_items()
        await interaction.response.edit_message(content="Cancelled — nothing was run.", embed=None, view=self)
        self.stop()


async def require_auth(interaction):
    """Returns True if allowed; otherwise sends the "Not authorized" reply
    itself and returns False. Callers should `return` immediately when this
    returns False — every command below does exactly that, in one line
    instead of repeating the same authorization-check-plus-reply block."""
    if is_authorized(interaction.user.id):
        return True
    await interaction.response.send_message("Not authorized.", ephemeral=True)
    return False


@bot.event
async def on_ready():
    print(f"Ultron bot online as {bot.user} (id={bot.user.id})")
    print(f"Backend: {BACKEND_URL}")
    print(f"Allowlisted users: {len(ALLOWED_USER_IDS)}")


@bot.tree.command(name="status", description="Get Ultron's current system status")
async def status_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/status")
        await interaction.followup.send(embed=format_status_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="containers", description="List Docker containers on the host")
async def containers_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/containers")
        await interaction.followup.send(embed=format_containers_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="storage", description="Get disk usage for the host")
async def storage_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/storage")
        await interaction.followup.send(embed=format_storage_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="systems", description="Get pending updates and hardware health")
async def systems_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/systems")
        await interaction.followup.send(embed=format_systems_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="repos", description="Get git status for configured repositories")
async def repos_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/dev/repos")
        await interaction.followup.send(embed=format_repos_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@app_commands.describe(repo="Repo name, matching one from /repos")
@bot.tree.command(name="diff", description="Get the uncommitted diff for one repository")
async def diff_command(interaction: discord.Interaction, repo: str):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, f"/api/dev/repos/{urllib.parse.quote(repo, safe='')}/diff")
        await interaction.followup.send(embed=format_diff_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@app_commands.describe(asset="Optional asset symbol to filter by, e.g. BTC")
@bot.tree.command(name="trades", description="List your recorded trades (read-only — add trades from the dashboard)")
async def trades_command(interaction: discord.Interaction, asset: str = ""):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        path = "/api/trades" + (f"?asset={urllib.parse.quote(asset, safe='')}" if asset else "")
        data = await backend_get(bot.http_session, path)
        await interaction.followup.send(embed=format_trades_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="portfolio", description="Realized gain/loss per asset (FIFO) — not tax advice")
async def portfolio_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/trades/summary")
        await interaction.followup.send(embed=format_portfolio_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="usage", description="Today's real Claude API token usage and budget status")
async def usage_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/chat/usage")
        await interaction.followup.send(embed=format_usage_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="connections", description="Who's currently connected to Ultron (people and device count)")
async def connections_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/connections")
        await interaction.followup.send(embed=format_connections_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="mcp", description="External (MCP) tool servers, their reachability, and which tools are approved")
async def mcp_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_get(bot.http_session, "/api/mcp/servers")
        await interaction.followup.send(embed=format_mcp_servers_embed(data))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@app_commands.describe(format="Which export to download")
@app_commands.choices(format=[
    app_commands.Choice(name="Transactions (raw trade list)", value="transactions"),
    app_commands.Choice(name="Tax lots (FIFO disposal detail)", value="tax-lots"),
])
@bot.tree.command(name="export", description="Download your trade records as a CSV file")
async def export_command(interaction: discord.Interaction, format: app_commands.Choice[str]):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        content, filename = await backend_get_csv(bot.http_session, f"/api/trades/export?format={format.value}")
        buf = io.BytesIO(content.encode("utf-8"))
        await interaction.followup.send(
            content=f"Here's your {format.name.lower()} export.",
            file=discord.File(buf, filename=filename),
        )
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="backup", description="Preview and run a backup (requires confirmation)")
async def backup_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    await interaction.response.defer()
    try:
        data = await backend_post(bot.http_session, "/api/actions/backup", {})
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))
        return

    embed = format_backup_preview_embed(data.get("preview", {}), data.get("expires_in_seconds", 300))
    view = ConfirmActionView(interaction.user.id, "/api/actions/backup", data["confirm_token"], format_backup_result_embed)
    msg = await interaction.followup.send(embed=embed, view=view)
    view.message = msg


@app_commands.describe(
    image="Docker image, e.g. nginx:latest",
    name="Container name",
    port="Optional port mapping, host:container — e.g. 8080:80",
    env="Optional single environment variable, KEY=value",
)
@bot.tree.command(name="deploy", description="Preview and deploy a new container (requires confirmation)")
async def deploy_command(interaction: discord.Interaction, image: str, name: str, port: str = "", env: str = ""):
    if not await require_auth(interaction):
        return

    ports = {}
    if port:
        parts = port.split(":")
        if len(parts) != 2 or not parts[0].strip().isdigit() or not parts[1].strip().isdigit():
            await interaction.response.send_message(
                "Port must look like host:container, e.g. 8080:80", ephemeral=True
            )
            return
        ports[parts[1].strip()] = parts[0].strip()

    env_dict = {}
    if env:
        idx = env.find("=")
        if idx < 1:
            await interaction.response.send_message("Env var must look like KEY=value", ephemeral=True)
            return
        env_dict[env[:idx].strip()] = env[idx + 1:]

    await interaction.response.defer()
    try:
        data = await backend_post(
            bot.http_session,
            "/api/actions/deploy-container",
            {"image": image, "name": name, "ports": ports, "env": env_dict},
        )
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))
        return

    embed = format_deploy_preview_embed(data.get("preview", {}), data.get("expires_in_seconds", 300))
    view = ConfirmActionView(
        interaction.user.id, "/api/actions/deploy-container", data["confirm_token"], format_deploy_result_embed
    )
    msg = await interaction.followup.send(embed=embed, view=view)
    view.message = msg


@app_commands.describe(message="What do you want to ask Ultron?")
@bot.tree.command(name="ask", description="Ask Ultron a question (routes through the LLM, checks real data)")
async def ask_command(interaction: discord.Interaction, message: str):
    if not await require_auth(interaction):
        return
    if len(message) > MAX_MESSAGE_CHARS:
        await interaction.response.send_message(
            f"Message too long (max {MAX_MESSAGE_CHARS} chars).", ephemeral=True
        )
        return

    await interaction.response.defer()
    history = bot.chat_histories.get(interaction.user.id, [])
    try:
        data = await backend_chat(bot.http_session, message, history)
        bot.chat_histories[interaction.user.id] = data.get("history", history)
        await interaction.followup.send(embed=format_chat_embed(data["reply"], data.get("tools_used", [])))
    except BackendError as e:
        await interaction.followup.send(embed=format_error_embed(str(e)))


@bot.tree.command(name="forget", description="Clear your conversation history with Ultron")
async def forget_command(interaction: discord.Interaction):
    if not await require_auth(interaction):
        return
    bot.chat_histories.pop(interaction.user.id, None)
    await interaction.response.send_message("Conversation history cleared.", ephemeral=True)


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
