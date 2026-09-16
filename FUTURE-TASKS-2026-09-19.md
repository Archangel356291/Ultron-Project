# Scheduled work — begin 2026-09-19 (Saturday) 02:00

Owner-requested task list, to be started automatically at the date/time in
this file's name, and worked through **in the order listed**. Do not
reorder or skip items; if an item turns out to be infeasible, say so
explicitly in that session's report rather than silently dropping it.

Before starting: read this repo's own established context first —
`ULTRON-COLOR-SYSTEM.md`, `ULTRON-DASHBOARD-DESIGN-SPEC.md`,
`HOME-DASHBOARD-REDESIGN.md`, `CLAUDE.md`, and this session's git log
(commit `78256c7` and the two before it) — a lot of "make it cinematic/
alive" ground was already covered there; this list continues from that
point rather than starting over. Same copyright-safety rule as always:
original work inspired by reference material, never a traced copy of
Marvel's copyrighted Ultron design.

## 1. Full "alive / futuristic / cyberspace" pass on the whole dashboard

Highest visual/interaction quality achievable. The specific bar: it should
feel like talking to **someone**, not interacting with an object or a
computer. Use every reference image already in the `Ultron Project` parent
folder (relic, pixel-Ultron, pixel-room, status-tracker, body-design,
Ultron-body, brain — the same set used this session) as style source
material — original art inspired by them, not traced copies. This is a
continuation of, not a replacement for, the glass-panel/brain-graph/
Vitals-panel/pixel-art work already shipped.

## 2. Investigate an offline version of Ultron

Can the dashboard/assistant function meaningfully without an internet
connection (no Claude API, no Tailscale)? Scope what "offline mode" would
even mean here — cached last-known state? A local-only subset of features?
Report findings; only build it if it's genuinely feasible and worthwhile,
not a fake offline mode that just shows stale data with no indication.

## 3. Investigate an "API-lite" version of Ultron

A reduced-scope/lower-cost mode of the assistant (fewer tools, cheaper
model, or both) for situations where the full setup is overkill. Scope
what "lite" would actually cut before building anything.

## 4. Investigate a downloadable app for phones/other devices

Is a real native or PWA-style installable app realistic here, given the
current stack (static HTML/CSS/vanilla JS + Flask, no build tooling)? What
would it take? Report the honest scope/effort before attempting anything.

## 5. Survey available plugins/skills/tools for staying current

Check what's available in the Claude Code environment at that time for
coding, art/design, theming, performance, security, and privacy —
specifically what would materially improve this project — and report what
was found, installed, or deliberately not used and why.

## 6. Fix: only 2 of 4 subagents show in the pixel room

Owner has 4 subagents; the pixel room currently only renders 2 (cyan and
green — see `SUBAGENTS` array in `ultron-dashboard.html` and
`dev-tools/gen_pixel_assets.py`). Find out what the other 2 subagents
actually are (ask the owner if it isn't already recorded somewhere in this
repo) and add them to the scene with their own desk + tube, matching the
existing pattern.
