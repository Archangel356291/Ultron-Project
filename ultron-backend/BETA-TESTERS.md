# Beta testers

Everyone who helps test Ultron gets credited here as they join — not
because it's required, but because finding what's broken before it
matters is real work.

## How someone gets added

Each tester gets their **own** token — never your `ULTRON_API_TOKEN`,
and never one token shared between people. `ULTRON_BETA_TOKENS` in `.env`
holds all of them at once, as `name:token` pairs:

```
ULTRON_BETA_TOKENS=alice:3f9a1c7e2b8d4056a1f2e3c4b5a69788,bob:9c2e5f81a4b7301dc6e9f0a2b3c4d5e6
```

0. **Ask first.** `BETA-INVITE-MESSAGE.md` has a ready-to-send invite —
   copy/paste it in, fill in their name, send. The steps below are for
   once they've said yes.
1. **Generate a token** for the new person (PowerShell):
   ```powershell
   -join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})
   ```
2. **Add it to `ULTRON_BETA_TOKENS`** in `.env` as `name:token`, comma-separated
   from any existing entries. Restart the backend to pick it up.
3. **Send them `BETA-TESTER-GUIDE.md`, their URL, and their token.** The
   guide is written for the tester directly (no dev background assumed)
   — walks them through installing Tailscale, connecting, and what
   they're allowed to do. Paste its contents into a message/doc rather
   than pointing them at this repo. `/api/whoami` reports their name
   back once connected, so it's easy to confirm which token actually
   ended up in their hands.
4. **Add a row to the roster below** with their name and the date they
   started.
5. **When they stop testing:** remove their `name:token` entry from
   `ULTRON_BETA_TOKENS` and restart the backend. This revokes only that
   person — everyone else's token keeps working.

## Roster

| Name | Started | Notes |
|---|---|---|
| _none yet_ | | |

Beta test #1 (2026-09-13) verified the `beta_tester` role itself, end to
end, using the owner's own second device (phone) over Tailscale — not a
third-party tester, so it isn't listed as one here. This roster is for
actual other people.

## What's still not covered

Per-tester tokens give independent revocation and `/api/whoami`
attribution, but there's still no persistent record tying a tester's
name to their *past* activity in the trade/usage logs — the backend logs
requests, not who made them. Fine for a handful of trusted people; a real
accounts table would be the next step if this grows past that.
