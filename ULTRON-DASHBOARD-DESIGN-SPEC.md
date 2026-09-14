# Ultron AI Dashboard — Design Specification (from reference image)

**Status (2026-09-13): mostly historical.** This document predates the
"consolidate project files into git-tracked repo folder" commit and had
been sitting lost in an untracked backup zip outside the repo until
recovered while cleaning up the workspace — restored here so it doesn't
get lost again. Its recommendations were independently re-derived and
acted on during the same day's dashboard visual-match pass (chamfered
corners, status/activity icon badges, orb-as-CSS-glow, header
user/status cluster, footer divider marks — all match what's now in
`ultron-dashboard.html`), with one exception: its one specific,
actionable finding — darken `--line` toward `#03294A` — hadn't been
applied yet and is now fixed. Kept as a record of the original pixel
analysis, not as an open task list.

Source: `3437.png`, 1290×1219px. Every color below was extracted by
directly sampling pixels from the actual image file (Python/PIL,
averaging small regions to filter anti-aliasing noise, and cross-checking
against 6–10x magnified crops of real border/text edges) — not estimated
by eye. Confidence level is noted per value, since a rendered/glowing
sci-fi UI has soft edges and bloom effects that genuinely limit how
precisely a single "true" color can be pinned down in some spots.

**Important context: a working implementation of this exact reference
already exists** — `ultron-dashboard.html` in this project, built and
live-wired against the real Ultron backend across the whole preceding
build. This document is written to do two things: (1) stand alone as a
from-scratch spec if you want to rebuild, and (2) call out the specific,
verified differences between the reference image and what's currently
implemented, so the faster path is likely refining the existing file
rather than starting over.

## Color palette (sampled)

| Role | Sampled hex | Confidence | Existing CSS var | Match? |
|---|---|---|---|---|
| Base/void background | `#00050C` (avg of several flat regions) | High | `--void: #050810` | Close — negligible visual difference, no change needed |
| **Panel/card border lines** | `#032C4A` (brightest pixels in a magnified border crop) | High | `--line: #1C2B45` | **Meaningful mismatch — see below** |
| Bright amber accent (logo, active nav text/icon, active-state glow) | `#F6BC63` (brightest pixels, "AI" logo text edge) | High | `--amber: #FFC24B` | Close match, no change needed |
| Orb glow — white-hot core | `#FEEF87` (brightest orb-center pixels) | Medium (small hot-spot, easy to clip) | — | No existing variable for this exact tone; see orb notes below |
| Orb glow — mid-orange | `#C4580D` to `#A2421C` (sampled at increasing radius from core) | High | `--oxide: #FF8A1E` | Reference gradient's mid-tones are *darker/more muted* than pure `--oxide` — expected, since a radial glow naturally dims with distance; `--oxide` is a reasonable value for the gradient's brighter inner band |
| Green "online/active" status | not independently verified this pass | — | `--signal: #33D17A` | Standard success-green convention; low risk, no evidence to contradict it |

### The one real, actionable color finding

**The panel border lines in the reference are a distinctly darker,
more saturated navy-blue than what's currently implemented.** This was
confirmed two ways: a magnified crop of an actual corner (System Status
panel, top-left) showed a clean blue line with no amber influence at
all, and the brightest pixels sampled directly from it cluster tightly
around `#032C4A`–`#042945`. The existing `--line: #1C2B45` is a lighter,
less saturated blue-gray by comparison. If matching the reference
closely matters, darken `--line` toward the `#03294A` range — likely as
a genuine CSS variable change rather than a one-off tweak, since this
color is almost certainly used consistently across every panel border in
the existing stylesheet.

**Worth noting explicitly since it's easy to assume otherwise at a
glance:** the *structural* borders throughout this UI (panel edges, card
outlines) are blue, not amber. Amber/gold is reserved for the logo,
active/highlighted states (the active HOME nav item, the active "General"
mode pill, the orb, icons that indicate emphasis), and glow/bloom
effects — confirmed by directly zooming into an active nav item (clear
amber background gradient + amber icon + amber bold text) versus a
plain panel corner (clean blue line, zero amber). Getting this
foreground/background color split right is probably the single highest-
leverage thing for genuine visual fidelity, more than any individual hex
value.

## Layout structure

- **Full-bleed top header bar**: logo lockup on the left ("ULTRON AI" in
  a bold condensed display face, with "AI" in the amber accent color,
  and a smaller tagline below: "AUTONOMOUS • SECURE • ALWAYS ON YOUR
  SIDE"), a centered nav-label row (ANALYZE / AUTOMATE / PROTECT /
  OPTIMIZE / BUILD, small-caps, wide letter-spacing, muted gray), and a
  right-aligned user/status cluster (shield+user icon, "USER: [NAME]" +
  "ADMIN ACCESS", a live clock, date, and an "● SYSTEM ONLINE" status
  line in the signal-green color).
- **Left sidebar** (fixed width, roughly 20% of viewport): vertical nav
  list, each item an icon + bold label + smaller muted subtitle
  underneath. The active item gets the amber treatment described above;
  inactive items are icon+text in the muted steel/gray tone with no
  background fill.
- **Main hero area**: centered "ULTRON ONLINE" title with small angled
  accent marks flanking it, a subtitle line beneath, the large glowing
  wireframe-sphere/orb graphic as the visual centerpiece (this is
  clearly a generated/rendered 3D-style graphic, not something to
  attempt as literal CSS/SVG geometry — a CSS-animated glow/particle
  effect achieving the same *impression* is the reasonable target, which
  is what the existing implementation already does), and two short word
  columns flanking the orb (LEARN / ADAPT / SOLVE / EVOLVE on the right).
- **Talk-to-Ultron input bar**: a bordered box below the hero, with a
  waveform icon + "TALK TO ULTRON" label, a text input with placeholder
  text, a circular mic button, and a filled amber send button. Below the
  input, a row of mode-select pills (General / Code / Home Lab /
  Analysis / Trading / Automation) — the active pill (General) gets a
  filled amber background; inactive pills are outlined/dark.
- **Right column** (two stacked panels): System Status (a checklist of
  system components each with an icon, label, and right-aligned status
  value, most in green) above Quick Actions (a list of clickable rows,
  each icon + label + trailing chevron).
- **Bottom row** (four panels in the reference, roughly equal width):
  Home Lab Overview (three circular ring-gauges in different accent
  colors — cyan, green, purple — plus a service list and a small device
  card), Latest Activity (a timestamped event list with colored icon
  badges per event type), Market & Crypto (a compact ticker row plus a
  small sparkline chart), and AI Status (a short "assistant is ready"
  message card).
- **Footer**: a thin centered line of small-caps text — "YOUR HOME LAB •
  YOUR DATA • YOUR RULES • ULTRON" — with amber divider marks.

## Structural/decorative details worth getting right

- **Chamfered corners, not rounded ones.** Every panel in the reference
  has its corners cut at a 45° angle rather than a border-radius curve —
  confirmed directly in the magnified border crop (the corner is a
  visible diagonal cut, not an arc). This is a core part of the sci-fi
  HUD aesthetic and is easy to accidentally soften into rounded corners
  without a close look at the source.
- **Thin single-pixel-weight border lines**, not thick strokes — the
  reference's borders read as delicate/precise rather than heavy.
- **Status rows and list items use small icon badges** (icon inside a
  faint colored circle/square) rather than bare icons, giving each row a
  consistent left-aligned anchor point.
- **Typography**: the display/heading face (logo, section titles,
  "ULTRON ONLINE") is a bold condensed sans — matches the existing
  implementation's use of Barlow Condensed / Orbitron-style fonts for
  headers, with a cleaner standard sans for body copy and small-caps
  with wide letter-spacing for labels/taglines throughout.

## Recommended next step

Given a tested, live-wired implementation already exists: open
`ultron-dashboard.html`, locate the `--line` CSS variable (and confirm
it's the single source of truth for border colors across the stylesheet,
which it should be given the project's established one-variable-per-role
convention), and darken it toward `#03294A`. Then do a side-by-side visual
comparison against `3437.png` at the panel-corner level specifically —
that's where this spec's one confirmed, actionable difference lives.
Everything else checked in this pass (background tone, amber accent,
orb glow, layout structure, chamfered corners) already matches closely
enough that a rebuild-from-scratch would mostly be re-deriving what's
already correct.
