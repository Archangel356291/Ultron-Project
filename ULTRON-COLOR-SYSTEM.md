# Site-wide visual polish: black + metal + blue + gold + red

A full re-theme of `ultron-dashboard.html` — not scoped to Home this
time, per explicit instruction. Same file, same constraint as every
prior pass tonight: no backend/API/route/auth changes, no functionality
removed, no new dependencies.

## Existing UI architecture (audit, before touching anything)

Confirmed unchanged from earlier tonight: plain HTML/CSS/vanilla JS,
one file, no framework, no build step, no WebSocket (REST polling).
`--oxide` (orange, `#FF8A1E`) was the *only* accent color used across
the whole site before this pass — nav active state, every button,
every panel-label dot, every card's top-edge highlight, focus rings,
toggle switches, error text, warning text, and the AI brain, all at
once. That's the actual root of "feels flat/generic" the brief
describes: one color carrying every kind of meaning reads as no
hierarchy at all, regardless of how dark the background is.

## The color system

Five roles, matching the requested 60-70/15-25/5-10/3-8/1-5 split:

| Role | Token(s) | Where |
|---|---|---|
| Black (60-70%) | `--void #08090A`, `--panel #0F1113`, `--panel-raised #16191C` | All backgrounds — three steps, not one flat value, so surfaces read as stacked material |
| Dark metallic silver (15-25%) | `--line`/`--metal #2C2F33`, `--metal-light #474C52`, `--metal-dim #1B1D20`, `--steel #8B93A0` | Borders, separators, inactive controls, structural framing |
| Blue (5-10%) | `--blue #4FA6E0`, `--blue-bright #8FD6FF`, `--cyan #3DD6FF` | Readable text, telemetry, AND the general interactive accent (nav active, focus rings, buttons, toggles) |
| Gold/orange (3-8%) | `--oxide #FF8A1E` (narrowed), `--core-gold #FFB238` | Ultron's identity/intelligence *specifically* — narrowed hard, see below |
| Red (1-5%, new) | `--red #C0392B`, `--red-bright #FF3B3B` | Errors, critical states, financial losses — didn't exist as a dedicated token before tonight |

**The two token-value-only changes that did the most work for the
least risk**: recoloring `--void`/`--panel`/`--panel-raised` (black
family) and `--line` (metal family) required zero per-rule edits,
since those four tokens already drove nearly every background and
border in the file. That alone covers most of "black-dominant,
metallic structure" automatically.

## `--oxide`: narrowed from "the site's accent" to "AI-tied only"

This was the real work — 67 individual usages (54 `var(--oxide)` +
13 raw hex/rgba), each reclassified on its own merits, not a blind
find-replace:

- **Stays gold** (13 remaining, all genuinely AI-identity-tied): the
  header logo mark + its pulse, the "AI" in "ULTRON AI," everything
  inside the hero panel itself (eyebrow bolts, sphere-labels border —
  the AI core's own immediate surroundings), the mic button specifically
  while `.listening` (reflects the brain's own real state machine, not
  a static accent), the `who` label on Ultron's own chat messages, the
  AI Assistant tab's brain-canvas labels and its own hub node (Ultron's
  literal node in that graph).
- **Becomes red** (`.sev.crit`, `.msg.ultron.err`, `.conn-status.err`,
  activity `status === 'error'`, a negative realized trade gain, the
  90%+ tier of every spend/token/beta-spend gauge, one inline error
  span) — every genuine error/critical/loss state, verified live: the
  Crypto ticker's `-0.6%` now renders in red, previously orange.
- **Becomes blue** (everything else — ~40 declarations: nav active
  state, every button, panel-label dots sitewide, focus rings, toggle
  switches, footer/card edge highlights, the talk bar's general chrome,
  Settings' connect button, the checkbox accent, the "Trading" category
  color in both the brain-canvas and the Knowledge Graph). This is the
  bulk of what used to be "the orange site" and is now "the blue-lit
  metal command interface."
- **One deliberate exception, not red or gold**: the topbar connectivity
  pip's "not ok" state → `var(--steel)` (metal gray), not red — per the
  brief's own status vocabulary, "OFFLINE: dark metallic gray" is
  distinct from "CRITICAL: red," and "not yet connected" is this app's
  normal resting state before setup, not a fault. The hero brain's
  separate `alert` state (Module 14, driven by an *actual*
  connection-loss-after-being-connected condition) still turns red —
  that's the real fault signal; this pip's neutral gray is deliberately
  not competing with it.

## Navigation

Redesigned per the brief's own description ("feel like the control
interface of an AI system... blue text... angular highlights... small
status LEDs"): the active nav item is now a metal-toned wash with
blue-bright text/icon, plus one small red left-edge accent (2px,
literally a status LED, not a wash) satisfying "selected states" from
the color hierarchy without making the sidebar red. Verified live
across Home, Security, AI Assistant, Crypto & Markets, and Settings —
consistent everywhere, and confirmed the small red accent doesn't read
as "the site is red now," just as a precise indicator.

## Verified live in Chrome

Reloaded fresh (console armed from load, not mid-session) and clicked
through Home, Security, AI Assistant (brain-canvas), Crypto & Markets
(confirmed the real `-0.6%` loss renders red), and Settings (toggle
switches, connect button, external-tools button) — console clean
throughout, no errors on any section, the gold AI brain and the
Knowledge Graph's own established cyan/gold/purple category colors are
both untouched and remain visually dominant/legible against the new
darker background. No backend/Python file touched this pass — existing
test checkpoint re-run clean regardless, since a pure CSS/token change
has no code path to break there.

## Known limitations — not solved this round

- **Mobile/tablet layout not independently re-verified** — same
  automation-environment limitation as every prior pass tonight
  (`resize_window` doesn't reflow the actual viewport here). No
  responsive breakpoint rules were touched, so existing behavior should
  carry through unchanged, but that's an inference, not a live check.
- **`prefers-reduced-motion`/Reduced Visual Mode behavior unaffected by
  this pass** (pure recolor, no animation/timing logic touched) but
  also not re-verified live for the same reason.
- **The Crypto ticker's hardcoded fake BTC/ETH/SOL/SPY prices** (flagged
  as a known pre-existing issue in `HOME-DASHBOARD-REDESIGN.md`) are
  still there — out of scope for a color pass, unrelated to today's work.
- **No systematic contrast-ratio audit.** `--blue`/`--blue-bright`
  against the new darker `--void`/`--panel` were chosen by eye for
  "clearly readable," not measured against WCAG thresholds.
