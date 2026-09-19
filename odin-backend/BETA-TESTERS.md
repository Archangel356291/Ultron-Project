# Beta testers

Everyone who helps test Odin gets credited here as they join — not
because it's required, but because finding what's broken before it
matters is real work.

## How someone gets added

Each tester gets their **own** token — never your `ODIN_API_TOKEN`,
and never one token shared between people. `ODIN_BETA_TOKENS` in `.env`
holds all of them at once, as `name:token` pairs:

```
ODIN_BETA_TOKENS=alice:3f9a1c7e2b8d4056a1f2e3c4b5a69788,bob:9c2e5f81a4b7301dc6e9f0a2b3c4d5e6
```

0. **Ask first.** `BETA-INVITE-MESSAGE.md` has a ready-to-send invite —
   copy/paste it in, fill in their name, send. The steps below are for
   once they've said yes.
1. **Generate a token** for the new person (PowerShell):
   ```powershell
   -join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})
   ```
2. **Add it to `ODIN_BETA_TOKENS`** in `.env` as `name:token`, comma-separated
   from any existing entries. Restart the backend to pick it up.
3. **Send them `BETA-TESTER-GUIDE.md`, their URL, and their token.** The
   guide is written for the tester directly (no dev background assumed)
   — walks them through installing Tailscale, connecting, and what
   they're allowed to do. Paste its contents into a message/doc rather
   than pointing them at this repo. `/api/whoami` reports their name
   back once connected, so it's easy to confirm which token actually
   ended up in their hands — and, for a beta tester, their current spend
   against the cap (see below).
4. **Add a row to the roster below** with their name and the date they
   started — and the matching table in the main `README.md`'s "Beta
   testers" section, which mirrors this one for visibility. Keep both
   in sync.
5. **When they stop testing:** remove their `name:token` entry from
   `ODIN_BETA_TOKENS` and restart the backend. This revokes only that
   person — everyone else's token keeps working.

## Roster

| Name | Started | Notes |
|---|---|---|
| _none yet_ | | |

Beta test #1 (2026-09-13) verified the `beta_tester` role itself, end to
end, using the owner's own second device (phone) over Tailscale — not a
third-party tester, so it isn't listed as one here. This roster is for
actual other people.

## Spend cap

Every beta tester is capped at **$1.00 of real API spend, total, for the
whole time they're testing** — not a daily allowance, a lifetime one. It's
enforced in `/api/chat` itself (a genuine refusal once reached, not just a
displayed number — see `odin-backend/app.py`'s `_beta_tester_spend_usd`
and the check in the `chat()` route), computed from each call's actual
token usage at real Claude pricing, not estimated. Default is
`$1.00`; override with `ODIN_BETA_MAX_SPEND_USD` in `.env` if a
particular tester (or the beta as a whole) needs a different limit —
it applies to every beta token, there's no per-tester override yet.
Admin chat is never subject to this. A tester can see their own running
total via `/api/whoami`; the roster's spend across everyone is visible to
the admin via `/api/chat/usage`'s `beta_testers` field, the dashboard's
Settings → Usage & cost controls card, or watch who's actually connected
right now via `/api/connections` (dashboard: Settings → Connections;
Discord: `/connections`).

## What's still not covered

Per-tester tokens give independent revocation and `/api/whoami`
attribution, but there's still no persistent record tying a tester's
name to their *past* activity in the trade/usage logs — the backend logs
requests, not who made them. Fine for a handful of trusted people; a real
accounts table would be the next step if this grows past that.
