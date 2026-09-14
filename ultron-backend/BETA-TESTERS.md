# Beta testers

Everyone who helps test Ultron gets credited here as they join — not
because it's required, but because finding what's broken before it
matters is real work.

## How someone gets added

1. Give them their own value for `ULTRON_BETA_TOKEN` and the URL to your
   backend (see `BETA-LAUNCH-CHECKLIST.md` and `REMOTE-ACCESS.md`). They
   connect as `beta_tester`: chat plus view-only trading data, nothing
   else — see `README.md`'s auth section for exactly what that covers.
2. Add a row to the roster below with their name and the date they
   started.
3. When they stop testing, remove their row and rotate
   `ULTRON_BETA_TOKEN` — see the note on token sharing below.

## Roster

| Name | Started | Notes |
|---|---|---|
| _none yet_ | | |

Beta test #1 (2026-09-13) verified the `beta_tester` role itself, end to
end, using the owner's own second device (phone) over Tailscale — not a
third-party tester, so it isn't listed as one here. This roster is for
actual other people.

## A real limitation, not yet fixed

`ULTRON_BETA_TOKEN` is a single shared secret — every beta tester
currently uses the *same* token. That means:

- No way to tell which tester made a given request from the logs alone.
- Removing one tester's access means rotating the token for everyone,
  not just them.

Fine for one or two people you trust; worth revisiting (per-tester
tokens, or a lightweight accounts table) before handing this out more
widely. Flagging it here rather than building it preemptively — no one's
needed it yet.
