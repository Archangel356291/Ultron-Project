# Remote access — Tailscale setup

This is the piece that's been referenced throughout this project ("use a
Tailscale address instead of opening a port") without ever being written
down as an actual walkthrough. Here it is.

**A note on what this document is:** everything else in this project is
code you can run and I can test. Tailscale is a third-party service —
there's no way to install it, authenticate against it, or verify a real
tailnet from the environment this was built in. So this is a setup guide,
verified against Tailscale's current documentation and known Windows
Firewall behavior, not something with a test suite behind it the way the
backend and dashboard are. Treat it accordingly — sanity-check the one or
two commands below on your own machine before relying on them.

## What Tailscale actually is, briefly

A mesh VPN built on WireGuard. Install it on two devices, sign into the
same account on both, and they can reach each other directly — no port
forwarding, no static IP, no router configuration. Free for personal use:
the Personal plan allows 6 user accounts and (as of a 2026 pricing change)
unlimited devices per account, which is more than enough for a home lab
and a phone or two.

The alternative most people compare it to is raw WireGuard, which Tailscale
is built on. Setting up WireGuard yourself means generating and managing
keypairs, writing config files, and handling NAT traversal manually.
Tailscale does all of that for you in exchange for running its coordination
service — reasonable tradeoff for a personal project, which is why this
guide covers Tailscale and not raw WireGuard.

## 1. Install on the Cyberpower PC (the backend host)

1. Go to `tailscale.com/download/windows` (or install from the Microsoft
   Store) and run the installer.
2. Sign in when prompted — Google, Microsoft, GitHub, or your own SSO all
   work. This creates your "tailnet" (your private network) on first sign-in.
3. That's it. Tailscale runs in the background from here on; there's no
   ongoing "connect" step like a traditional VPN client.

### Find this machine's Tailscale address

Either:
- Click the Tailscale icon in the system tray → it shows this device's
  Tailscale IP (looks like `100.x.x.x`).
- Or open PowerShell and run:
  ```powershell
  tailscale ip -4
  ```
- Or, more durably, use the MagicDNS hostname instead of the IP — visible
  in the tray icon or the admin console at `login.tailscale.com/admin/machines`.
  It looks like `your-pc-name.tailXXXX.ts.net` and, unlike the IP, doesn't
  change if the device re-registers.

Prefer the MagicDNS hostname over the raw IP for the dashboard/bot config
below — one less thing to update later.

## 2. Windows Firewall — probably already handled

The backend's main setup already has you run this:

```powershell
New-NetFirewallRule -DisplayName "Ultron Backend" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

Notice there's no `-Profile` parameter — when it's omitted, the rule
applies to **all** Windows Firewall profiles (Domain, Private, and Public),
not just one. Tailscale's virtual network adapter registers itself under
the "Private" profile by default, which this rule already covers. In the
normal case, you don't need to do anything extra here.

If you want to double-check rather than take that on faith:

```powershell
Get-NetFirewallRule -DisplayName "Ultron Backend" | Get-NetFirewallProfile
```

If that shows the rule scoped to all profiles (or at least includes
Private), Tailscale traffic to port 5000 will reach the backend.

### Optional: a stricter rule instead of a LAN-wide one

The rule above allows port 5000 from *any* address that can reach the
machine, Tailscale or not. If you'd rather only allow the Tailscale side
and close it off from the rest of your LAN, Tailscale's virtual IPs all
fall in the `100.64.0.0/10` range — you can replace the rule above with
one scoped to just that:

```powershell
Remove-NetFirewallRule -DisplayName "Ultron Backend"
New-NetFirewallRule -DisplayName "Ultron Backend (Tailscale only)" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow -RemoteAddress 100.64.0.0/10
```

This is a genuine tightening — worth it if you don't need other LAN
devices (that aren't on your tailnet) hitting the backend directly.

## 3. Install on your phone

Tailscale is on the iOS App Store and Google Play. Install it, sign in
with the same account you used on the Cyberpower PC. Once signed in, your
phone and the PC are both on the same tailnet and can reach each other —
whether the phone is on the same Wi-Fi or on cellular data across the
country.

## 4. Point the dashboard and bot at the Tailscale address

**Dashboard:** open `ultron-dashboard.html`, go to Settings → Connection,
and enter the Tailscale address instead of the LAN IP:

```
http://your-pc-name.tailXXXX.ts.net:5000
```

Same API token as always. This works identically whether you're on the
home Wi-Fi or not — that's the entire point of Tailscale over a LAN-only
setup.

**Discord bot** (only relevant if the bot runs on a *different* machine
than the backend): set `ULTRON_BACKEND_URL` to the same Tailscale address:

```powershell
$env:ULTRON_BACKEND_URL = "http://your-pc-name.tailXXXX.ts.net:5000"
```

If the bot runs on the same machine as the backend, it can keep using
`http://127.0.0.1:5000` regardless — no change needed.

## 5. Verify it actually works

With the phone on cellular data (Wi-Fi off, to genuinely test off-LAN
access):

1. Open the Tailscale app, confirm it shows "Connected."
2. In a mobile browser, visit `http://your-pc-name.tailXXXX.ts.net:5000/api/health`.
   You should get back `{"ok": true}`.
3. If that works, the dashboard and bot will too — they're hitting the
   same address.

If step 2 doesn't work: check that Tailscale shows "Connected" on *both*
devices (tray icon on the PC, app on the phone), and re-run the
`Get-NetFirewallRule` check from step 2 above.

## 6. A couple of security options worth knowing about

These live in the Tailscale admin console (`login.tailscale.com/admin`),
not in anything this project's code touches:

- **Device approval** — under Settings → Device management, you can
  require new devices to be manually approved before they join your
  tailnet, rather than any sign-in on your account auto-joining.
- **Tags and grants** — restrict which devices can reach the backend's
  port 5000 at the Tailscale layer itself, on top of (not instead of) the
  Windows Firewall rule from step 2. Overkill for a two-device tailnet (PC
  + phone) where you own everything — genuinely useful once you add more
  devices, or if you ever invite someone else onto your tailnet. Covered
  in full below since it's easy to get subtly wrong.

Neither of these is required for a basic personal setup — they're here
because "what does Tailscale's own security model offer beyond the
Windows Firewall rule" is a reasonable question once you're relying on it
for remote access to something that can deploy containers and run backups.

### Tags and grants, in more depth

Tailscale's current recommended syntax for access rules is called
**grants** (it superseded the older `acls` array format, which still
works but isn't getting new features). Both live in the same place: the
tailnet policy file, edited from the admin console's Access Controls page.

The default policy — what you have right now, unless you've touched this
— is effectively "allow all": every device on your tailnet can reach
every other device. That's exactly why Tailscale is easy to set up, and
it's genuinely fine for a solo tailnet of devices you own. The moment you
add a device you *don't* fully trust with everything (a friend's device
you've shared access with, a cheap IoT gadget, a VPS), a blanket "allow
all" means that device can reach your Ultron backend too, port 5000 and
all.

**A safe, minimal starting point** — restrict your tailnet to only letting
your own devices talk to each other, which costs nothing if you're the
only person on it and protects you the moment you're not:

```json
{
  "grants": [
    {
      "src": ["autogroup:member"],
      "dst": ["autogroup:self"],
      "ip": ["*"]
    }
  ]
}
```

`autogroup:self` means "devices owned by the same user" — your PC and
your phone, since you signed into both with the same account. It's
**destination-only**: Tailscale rejects it on the `src` side ("not valid
on the src side of a rule"), so the source has to be `autogroup:member`
("any authenticated user on this tailnet") instead — with only one
person on the tailnet, that still resolves to exactly the same thing:
your own devices can talk to each other, freely; nothing else is
allowed by default.

**The nuance that's easy to miss:** `autogroup:self` explicitly does
**not** cover tagged devices — Tailscale treats a tagged device as more
of a service identity than a personal device, even if you're the one who
tagged it. So if you tag the Cyberpower PC (say, to scope port 5000
specifically), the grant above stops covering it, and you need a second,
explicit grant for the tag:

```json
{
  "tagOwners": {
    "tag:ultron-backend": ["autogroup:admin"]
  },
  "grants": [
    {
      "src": ["autogroup:member"],
      "dst": ["autogroup:self"],
      "ip": ["*"]
    },
    {
      "src": ["autogroup:member"],
      "dst": ["tag:ultron-backend"],
      "ip": ["tcp:5000"]
    }
  ]
}
```

`tagOwners` says who's allowed to apply `tag:ultron-backend` to a device
(here, tailnet admins — you, on a personal account). You'd then actually
tag the Cyberpower PC with `tag:ultron-backend` from the admin console's
Machines page. The second grant says "your own devices can reach port
5000 specifically on anything tagged `ultron-backend`" — narrower than
the first grant's "everything," which is the point: even if some other
device on your tailnet gets compromised later, it can't reach the backend
unless it matches one of these rules.

**Before you save a policy change:** the admin console's policy editor
validates syntax and shows you a diff before applying anything, and past
versions are recoverable from the Configuration logs page if a change
breaks something you needed. Grants are deny-by-default once you start
writing them — an empty or incomplete `grants` section can cut off
connectivity you didn't mean to touch (SSH between your own devices,
for instance, needs its own explicit `ssh` section if you rely on it,
separate from `grants`).

The first example (`autogroup:member` → `autogroup:self`) **has now been
saved against a real tailnet** (2026-09-13) and works — it originally read
`"src": ["autogroup:self"]` here, which Tailscale rejects outright
("`autogroup:self` not valid on the src side of a rule"); fixed above.
The tag-based second example is still unverified — adapt and check it
against the admin console's own diff/validation before trusting it, and
Tailscale's own [grant examples
page](https://tailscale.com/docs/reference/examples/grants) is the
authoritative source for anything beyond what's covered here.

## Troubleshooting

- **`tailscale ip -4` shows nothing / Tailscale icon shows "not connected"**
  — sign out and back in from the tray icon; this usually resolves it.
- **The health check works from the PC itself but not the phone** — almost
  always the firewall rule. Re-run the `Get-NetFirewallRule ... |
  Get-NetFirewallProfile` check above.
- **MagicDNS hostname doesn't resolve** — confirm MagicDNS is enabled in
  the admin console (DNS page); it's on by default for tailnets created
  after October 2022, but worth a direct check if you have an older
  account. The raw `100.x.x.x` IP always works as a fallback regardless.
- **Works on Wi-Fi but not cellular** — turn Wi-Fi off on the phone
  entirely rather than just leaving the home network's range; some phones
  stay associated with a "known" Wi-Fi network's Tailscale state even when
  signal is weak, giving a false read on whether cellular-only access
  actually works.
