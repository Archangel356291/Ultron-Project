# Testing Odin — a quick guide

Thanks for helping test Odin! This walks you through getting connected
and what you can actually do once you're in. Should take about 5
minutes.

## What you'll need

- **A link and a token** — the person who invited you will send you both.
  Keep the token private, like a password; it's yours alone.
- **The Tailscale app** on whatever device you're using (phone, laptop,
  tablet) — this is what lets your device securely reach Odin without
  it being exposed to the whole internet. Install it from your device's
  app store, or [tailscale.com/download](https://tailscale.com/download)
  on a computer.
- An invite to join the tailnet — you'll get this from whoever's hosting
  Odin, separately from the link/token above. Accept it in the
  Tailscale app.

## Step 1 — Connect Tailscale

Open the Tailscale app, sign in (or accept the invite you were sent), and
confirm it shows **Connected**. That's it for this step — no further
setup needed here.

## Step 2 — Open Odin

In a normal browser tab (Chrome, Safari, whatever you'd normally use), go
to the link you were given. It'll look something like:

```
http://<some-name>.<random-letters>.ts.net:5000/
```

You should see the Odin dashboard load, showing sample/placeholder data
at first — that's expected, you're not connected yet.

## Step 3 — Connect with your token

1. Click **Settings** in the left-hand menu (or bottom menu on a phone).
2. Under **Connection**, enter:
   - **Backend URL**: the same link from Step 2
   - **API token**: the token you were given
3. Click **Connect**.

If it works, you'll see "connected" near the Connect button, and the menu
will shrink down to just a couple of options — that's correct, see below.

**If it says "could not reach backend"** and you're sure you typed
everything right: double check Tailscale still shows Connected, and try
reloading the page. If it still doesn't work, let whoever invited you
know.

## What you can actually do

As a beta tester, you get a deliberately limited view — this is by
design, not a bug:

- **AI Assistant** — chat with Odin. Ask it questions, have a
  conversation. This is the main thing to test.
- **Crypto & Markets** — you can *see* trade history and price info, but
  can't add, edit, or delete anything, and there's no export button.
  View-only.
- **Settings** — just the connection info and some display preferences.

Everything else (home lab controls, security tools, system diagnostics,
dev tools, admin settings) is intentionally hidden. That's not something
broken on your end — beta testers don't get access to those, full stop.

**Chat has a $1.00 total spend cap.** This is a lifetime cap for your
whole time testing, not a daily one — it doesn't reset. Once you hit it,
the AI Assistant will tell you plainly that the beta spend limit was
reached instead of silently failing or guessing; everything else you have
access to keeps working. If you need more, ask whoever invited you.

## Trying out the chat

Go to **AI Assistant** and just type a message — ask it something, like
you would any chat assistant. A few things worth trying:

- Ask it a general question.
- Ask about the recorded trades ("what's my portfolio look like?") — it
  can pull real numbers for that.
- Ask it something outside what it's allowed to see (like system status
  or security info) — it should tell you it doesn't have access to that,
  rather than guessing or making something up. If it *does* guess or
  give you a made-up-sounding answer instead of saying it can't check,
  that's worth reporting.

**Voice replies:** off by default. To turn it on, go to **Settings →
Preferences → "Speak replies aloud."** It resets to off every time you
reconnect — that's expected, not a bug.

## What to report

If anything feels broken, confusing, or just off, say so — including:

- Error messages, especially the exact wording
- Anything that seems slow or hangs
- Odin answering with information it shouldn't have access to (this
  one's important — flag it right away)
- Anything in the interface that looks wrong, cut off, or doesn't work
  the way you'd expect

There's no such thing as a report that's "too small" — a confusing
button label is as useful to know about as an actual crash.
