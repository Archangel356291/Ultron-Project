"""Generates original pixel-art PNG sprites/backdrop for the Ultron tab's
pixel-companion scene (dashboard, Ultron's Corner). Style/palette inspired
by two reference images the owner supplied (a red/gunmetal armored robot
portrait, and a teal-lit isometric sci-fi control room) -- NOT traced or
copied from either, since the character reference is itself modeled on
Marvel's copyrighted Ultron design. This draws an original silhouette
(angular gunmetal armor, glowing red core/joints, a crested head) built
from primitive shapes, matching the reference's palette and general
proportions rather than reproducing its actual artwork. Same principle
this project's own Module 13 already applied to the 3D hero head.

Quality pass (2026-09-15): same shapes/proportions/canvas sizes as before
(so ultron-dashboard.html's positioning math -- WALK_MIN_X/MAX_X, desk/tube
X offsets, FLOOR_Y anchoring -- needs zero changes), but every sprite now
gets a crisp dark outline, multi-tone shading instead of flat single-color
fills, and small grounding/material details (contact shadows, rim-lit glass,
a keyboard, panel seams) that a flat-Pillow-rectangle pass skips. Closest
available in-repo style reference is body_design.png/relic_gauge.png
(gen_design_assets.py) -- both already use rim-glow + multi-tone shading;
this brings the room sprites up to that same bar. The owner's own two
source photos referenced above were only ever shared in chat, never saved
to this repo, so they aren't available to re-check against here.

Run to (re)generate everything directly into ../pixel-assets/, which
ultron-backend/app.py serves at /pixel-assets/<file> (same pattern as
/three-pipeline/<file>):
    python dev-tools/gen_pixel_assets.py
"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os
import random

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pixel-assets")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- palette (matches ultron-dashboard.html's own CSS custom properties) ----
# Metallic pass (2026-09-16, owner: "make all metal items and characters
# metallic"): the shared armour/structure tones are cooled and brightened into
# brushed gunmetal/steel so every agent, desk, tube and the room backgrounds
# read as metal. Ultron gets his own gunmetal/platinum/titanium override in
# main(). Keep these in step with the dashboard's canvas metals.
BODY_DARK = (34, 38, 44, 255)     # cool dark steel
BODY_MID = (64, 70, 80, 255)      # gunmetal
BODY_LIGHT = (112, 120, 133, 255) # brushed steel highlight
STEEL = (170, 178, 190, 255)      # bright steel
# Ultron's own metallic body (his specific request): gunmetal gray, dark
# platinum, weathered titanium -- with red eyes/core (RED_BRIGHT below).
U_GUNMETAL = (48, 53, 61, 255)
U_PLATINUM = (98, 105, 116, 255)
U_TITANIUM = (156, 154, 146, 255)   # weathered, faintly warm
U_PLATE = (182, 184, 180, 255)      # polished titanium plating (faceplate/crest/seams)
RED_BRIGHT = (255, 59, 59, 255)
RED_CORE = (255, 130, 110, 255)
RED_DIM = (150, 30, 30, 255)
VOID = (8, 9, 10, 255)
PANEL = (17, 19, 22, 255)
PANEL_RAISED = (28, 32, 37, 255)
LINE = (56, 62, 71, 255)          # metallic seams/structure
CYAN = (61, 214, 255, 255)
GREEN = (51, 209, 122, 255)
# The two subagents the owner named on 2026-09-16: Sentinel (security
# watchdog) in the dashboard's --amber, Scout (web research) in the violet
# the activity feed already uses for its backup icon -- both colours the
# UI already speaks, not new ones.
AMBER = (255, 194, 75, 255)
VIOLET = (176, 132, 240, 255)
# The ten specialists added 2026-09-16 (see AGENT_REGISTRY in app.py and the
# SUBAGENTS table in ultron-dashboard.html) -- each its own colour so the
# room reads at a glance. Deliberately away from Ultron's red and Sentinel's
# amber.
AGENT_COLORS = {
    "cyan": CYAN, "green": GREEN, "amber": AMBER, "violet": VIOLET,
    "blue": (79, 166, 224, 255),      # Dockhand
    "indigo": (110, 110, 255, 255),   # Relay
    "mint": (120, 255, 200, 255),     # Gatekeeper
    "lime": (170, 230, 60, 255),      # Proof
    "rose": (255, 120, 150, 255),     # Auditor
    "steel": (170, 180, 200, 255),    # Scribe
    "lavender": (200, 160, 255, 255), # Archivist
    "peach": (255, 170, 120, 255),    # Librarian
    "magenta": (230, 80, 200, 255),   # Herald
    "olive": (160, 170, 60, 255),     # Envoy
    "copper": (205, 125, 60, 255),    # Forge
    "sky": (120, 200, 255, 255),      # Seeker
    "teal": (0, 190, 180, 255),       # Muse
    # blueprint agents added 2026-09-16 (subagent_blueprint.md gaps)
    "gold": (229, 184, 11, 255),      # Tally (stats)
    "bitcoin": (247, 147, 26, 255),   # Oracle (crypto market)
    "crimson": (215, 38, 74, 255),    # Redcell (ethical-hacking lab)
    # least-privilege cyber/coding/records specialists (owner-requested 2026-09-17)
    "cobalt": (47, 107, 255, 255),    # Bastion (sentinel-defense)
    "slate": (125, 139, 160, 255),    # Overwatch (overwatch-logger)
    "ember": (255, 140, 66, 255),     # Anvil (forge-coder)
    "vermilion": (255, 59, 46, 255),  # Breach (red-team-sandbox)
    # full-ecosystem specialists (owner-requested 2026-09-17)
    "ivory": (230, 221, 196, 255),    # Architect (architecture-lead)
    "mulberry": (166, 77, 121, 255),  # Critic (code-reviewer)
    "graphite": (90, 98, 112, 255),   # Steward (homelab-monitor)
    "candy": (255, 106, 213, 255),    # Pixel (pixel-artist)
    "spearmint": (63, 224, 160, 255), # Arbiter (game-balancer)
    "royalgold": (255, 207, 58, 255), # Game Master (gold crown)
}
OUTLINE_COLOR = (5, 6, 8, 255)


def glow(img, color, blur=3):
    """Soft glow layer: a blurred copy of the opaque shapes, tinted,
    composited behind the original -- cheap way to fake emissive light
    without a real lighting engine."""
    alpha = img.split()[3].filter(ImageFilter.GaussianBlur(blur))
    tint = Image.new("RGBA", img.size, color)
    tint.putalpha(alpha.point(lambda a: int(a * 0.55)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(tint)
    out.alpha_composite(img)
    return out


def outline(img, color=OUTLINE_COLOR, size=3):
    """Crisp dark rim around the opaque silhouette -- the single biggest
    lever for making flat Pillow-primitive shapes read as pixel art instead
    of plain rectangles. Dilates the alpha channel and fills the resulting
    ring, so it hugs whatever shape (rect/poly/ellipse) is already there."""
    alpha = img.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(size))
    ring = ImageChops.subtract(dilated, alpha)
    ring_layer = Image.new("RGBA", img.size, color)
    ring_layer.putalpha(ring)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(ring_layer)
    out.alpha_composite(img)
    return out


def shade(color, factor):
    """Lighten (factor>1) or darken (factor<1) an RGBA tuple, clamped."""
    r, g, b = (max(0, min(255, int(c * factor))) for c in color[:3])
    return (r, g, b, color[3] if len(color) > 3 else 255)


# ---- drawing surface -------------------------------------------------------
# Room pass (2026-09-16, owner: "double the size, and let us tell what we are
# looking at, even if the pixel edges get rounded slightly"). Everything below
# is drawn in *room units* -- the same coordinate space the dashboard's
# pixel-room script lays the scene out in -- onto a supersampled sheet that is
# then downsampled, which is what rounds the stair-stepped edges off. Assets
# are saved at RES pixels per room unit so they stay sharp on high-DPI phones.
RES = 2   # saved pixels per room unit
SS = 3    # supersample factor while drawing
PAD = 6   # transparent margin (room units) on every sprite, so the outline and
          # glow never clip. The dashboard subtracts it when placing sprites
          # (SPRITE_PAD in ultron-dashboard.html) -- keep the two in step.


class Sheet:
    def __init__(self, w, h, pad=PAD):
        self.w, self.h, self.pad, self.k = w, h, pad, RES * SS
        size = (int(round((w + 2 * pad) * self.k)), int(round((h + 2 * pad) * self.k)))
        self.img = Image.new("RGBA", size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def pt(self, x, y):
        return ((x + self.pad) * self.k, (y + self.pad) * self.k)

    def rect(self, x0, y0, x1, y1, fill=None, r=0.0, outline=None, width=0.0):
        box = [self.pt(x0, y0), self.pt(x1, y1)]
        w = max(1, int(round(width * self.k))) if outline else 0
        if r:
            self.d.rounded_rectangle(box, radius=r * self.k, fill=fill, outline=outline, width=w)
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=w)

    def poly(self, points, fill):
        self.d.polygon([self.pt(x, y) for x, y in points], fill=fill)

    def ellipse(self, x0, y0, x1, y1, fill=None, outline=None, width=0.0):
        w = max(1, int(round(width * self.k))) if outline else 0
        self.d.ellipse([self.pt(x0, y0), self.pt(x1, y1)], fill=fill, outline=outline, width=w)

    def line(self, points, fill, width=1.0):
        w = max(1, int(round(width * self.k)))
        pts = [self.pt(x, y) for x, y in points]
        self.d.line(pts, fill=fill, width=w, joint="curve")
        for px, py in pts:  # round caps and joints
            self.d.ellipse([px - w / 2, py - w / 2, px + w / 2, py + w / 2], fill=fill)

    def overlay(self):
        """A transparent sheet in the same coordinates. ImageDraw overwrites
        alpha rather than blending, so anything translucent is drawn on an
        overlay and merged."""
        s = Sheet.__new__(Sheet)
        s.w, s.h, s.pad, s.k = self.w, self.h, self.pad, self.k
        s.img = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        s.d = ImageDraw.Draw(s.img)
        return s

    def merge(self, other, blur=0.0):
        self.img.alpha_composite(other.img.filter(ImageFilter.GaussianBlur(blur * self.k)) if blur else other.img)

    def finish(self, rim=1.0, glow_color=None, glow_blur=3.0):
        size = (int(round((self.w + 2 * self.pad) * RES)), int(round((self.h + 2 * self.pad) * RES)))
        img = self.img.resize(size, Image.LANCZOS)
        if rim:
            img = outline(img, size=2 * int(round(rim * RES)) + 1)
        if glow_color:
            img = glow(img, glow_color, blur=glow_blur * RES)
        return img


# ---- characters ------------------------------------------------------------
# One robot, drawn on a 20-wide grid of `u` room units per cell. Ultron and
# every agent share the armoured vocabulary (so they read as one family); what
# tells them apart is colour, the crest on the helmet, the build, and the
# emblem on the monitor beside them. Original silhouette -- see the module
# docstring on why this is not a copy of any existing character design.
HEAD_TOP = 3.5  # grid rows of headroom above the helmet for crests/antennae
CRESTS = ("crown", "plates", "antenna", "visor", "dome", "fin", "horns")


def draw_robot(u, accent, pose, crest="crown", heavy=False, eye=None, bd=BODY_DARK, bm=BODY_MID, bl=BODY_LIGHT):
    """pose: 'walk_a' | 'walk_b' (full body) or 'work' (seated at a desk, cut
    off below the chest -- the desk sprite covers the rest).

    `eye`/`bd`/`bm`/`bl` override the eye-glow and the three body tones for a
    character with its own palette (Ultron: a metallic gunmetal/platinum/
    titanium body with red eyes); default to the shared armour so every agent
    is unchanged."""
    eye = eye or accent
    rows = (26 if pose != "work" else 20) + HEAD_TOP
    s = Sheet(20 * u, rows * u)
    dark = (8, 6, 6, 255)

    def R(x0, y0, x1, y1, c, r=0.0):
        s.rect(x0 * u, (y0 + HEAD_TOP) * u, x1 * u, (y1 + HEAD_TOP) * u, fill=c, r=r * u)

    def P(points, c):
        s.poly([(x * u, (y + HEAD_TOP) * u) for x, y in points], c)

    def E(x0, y0, x1, y1, c):
        s.ellipse(x0 * u, (y0 + HEAD_TOP) * u, x1 * u, (y1 + HEAD_TOP) * u, fill=c)

    # contact shadow first, under everything
    if pose != "work":
        sh = s.overlay()
        sh.ellipse(3.5 * u, (25.2 + HEAD_TOP) * u, 16.5 * u, (26.4 + HEAD_TOP) * u, fill=(0, 0, 0, 150))
        s.merge(sh, blur=0.06 * u)

    # helmet
    if heavy:
        P([(6.0, 5.6), (6.2, 2.4), (7.4, 0.6), (10, 0.0), (12.6, 0.6), (13.8, 2.4), (14.0, 5.6)], bm)
        P([(6.0, 5.6), (6.2, 2.4), (7.4, 0.6), (10, 0.0), (10, 5.6)], shade(bm, 1.25))
    else:
        P([(5.5, 5.5), (5.8, 2.2), (7, -0.4), (10, -1.3), (13, -0.4), (14.2, 2.2), (14.5, 5.5)], bm)
        P([(5.5, 5.5), (5.8, 2.2), (7, -0.4), (10, -1.3), (10, 5.5)], shade(bm, 1.25))
    R(5.6, 3.9, 14.4, 8.6, bl, r=0.5)
    # lit faceplate with dark eye slits and a mouth grille -- the face is the
    # thing that has to read at a glance, so it is the biggest bright shape
    P([(6.1, 4.3), (13.9, 4.3), (13.4, 8.3), (6.6, 8.3)], accent)
    P([(6.1, 4.3), (13.9, 4.3), (13.8, 5.0), (6.2, 5.0)], shade(accent, 1.3))
    for ex in (8.1, 11.9):
        if heavy:
            R(ex - 1.25, 5.5, ex + 1.25, 6.35, dark, r=0.15)
        else:
            E(ex - 1.3, 5.1, ex + 1.3, 6.6, dark)
            E(ex - 0.5, 5.5, ex + 0.5, 6.2, shade(eye, 1.4))
    for gx in (7.4, 8.6, 9.8, 11.0, 12.2):
        R(gx, 7.2, gx + 0.5, 8.1, dark)

    # crest -- the silhouette cue
    if crest == "crown":
        tips = ((6.3, -1.6), (7.9, -2.4), (10.0, -3.1), (12.1, -2.4), (13.7, -1.6))
        bases = (6.0, 7.1, 8.5, 11.5, 12.9, 14.0)
        for i in range(5):
            P([(bases[i], 0.6), tips[i], (bases[i + 1], 0.6)], accent)
            P([(bases[i], 0.6), tips[i], ((bases[i] + tips[i][0]) / 2, -0.4)], shade(accent, 1.3))
    elif crest == "plates":
        for x0 in (6.8, 9.0, 11.2):
            P([(x0, 0.9), (x0 + 1.0, -1.0), (x0 + 2.0, 0.9)], accent)
    elif crest == "antenna":
        R(9.7, -2.6, 10.3, -0.9, STEEL)
        E(9.2, -3.4, 10.8, -1.8, accent)
        E(9.6, -3.1, 10.2, -2.5, (255, 255, 255, 220))
    elif crest == "visor":   # hard-hat brim: the builders
        P([(5.0, 1.6), (15.0, 1.6), (14.2, 0.4), (5.8, 0.4)], accent)
        R(4.6, 1.5, 15.4, 2.3, shade(accent, 0.75), r=0.3)
    elif crest == "dome":    # a band across a smooth dome: the knowledge crew
        R(6.1, 1.1, 13.9, 2.0, accent, r=0.3)
        E(9.3, -1.6, 10.7, -0.3, accent)
    elif crest == "fin":     # one tall fin: the communicators
        P([(9.2, -0.6), (10.0, -3.2), (12.4, 0.2)], accent)
        P([(9.2, -0.6), (10.0, -3.2), (10.4, -0.4)], shade(accent, 1.3))
    elif crest == "horns":   # two swept horns: the guards
        P([(6.2, 1.4), (5.0, -2.2), (7.8, 0.2)], accent)
        P([(13.8, 1.4), (15.0, -2.2), (12.2, 0.2)], accent)

    # neck, shoulders, chest
    x0, x1 = (1.0, 19.0) if heavy else (3.0, 17.0)
    R(7.6 if heavy else 8.0, 8.2, 12.4 if heavy else 12.0, 9.7, bm)
    P([(x0, 11.6), (x1, 11.6), (x1 - 1.4, 9.4), (x0 + 1.4, 9.4)], bl)
    P([(x0, 11.6), (10, 11.6), (10, 9.4), (x0 + 1.4, 9.4)], shade(bl, 1.2))
    R(x0 + 0.6, 11.6, x1 - 0.6, 13.0, bm)
    for sx in (x0 + 0.9, x1 - 2.1):
        E(sx, 10.0, sx + 1.2, 11.2, shade(accent, 0.9))
    R(x0 + 1.0, 13.0, x1 - 1.0, 19.0, bm, r=0.4)
    R(x0 + 1.0, 13.0, x0 + 2.6, 19.0, bd)
    R(x1 - 2.6, 13.0, x1 - 1.0, 19.0, bd)
    for gy in (15.6, 17.4):
        R(6, gy, 14, gy + 0.55, accent)
    if heavy:   # shield on the chest
        P([(7.4, 11.0), (12.6, 11.0), (12.6, 13.8), (10, 15.4), (7.4, 13.8)], PANEL)
        P([(8.0, 11.6), (12.0, 11.6), (12.0, 13.5), (10, 14.7), (8.0, 13.5)], shade(accent, 0.6))
        E(9.0, 12.0, 11.0, 13.8, eye)
    else:       # glowing core
        R(7.5, 10.4, 12.5, 15.2, PANEL, r=0.5)
        E(8.2, 11.0, 11.8, 14.6, eye)
        E(9.1, 11.9, 10.9, 13.7, (255, 255, 255, 235))

    # arms
    aw = 3.2 if heavy else 2.2
    for ax in (x0 - 0.6, x1 + 0.6 - aw):
        R(ax, 12.2, ax + aw, 19.4, bl if heavy else bm, r=0.6)
        R(ax, 12.2, ax + 0.7, 19.4, shade(bl, 1.15))
        R(ax - 0.1, 15.0, ax + aw + 0.1, 15.6, shade(accent, 0.8))
        if pose != "work":
            E(ax + aw / 2 - 1.1, 18.9, ax + aw / 2 + 1.1, 21.1, shade(accent, 0.6))

    if pose != "work":
        lead = pose == "walk_b"
        lx, rx = (5.5, 11.6) if lead else (6.6, 10.6)
        ly, ry = (24.6, 24.0) if lead else (24.0, 24.6)   # one foot lifts
        R(lx, 19, lx + 2.6, ly, bm)
        R(rx, 19, rx + 2.6, ry, bl)
        R(lx, 19, lx + 0.7, ly, shade(bm, 1.25))
        R(lx, 21.2, lx + 2.6, 21.8, shade(accent, 0.7))
        R(rx, 21.2, rx + 2.6, 21.8, shade(accent, 0.7))
        R(lx - 0.6, ly, lx + 3.2, ly + 1.4, bd, r=0.4)
        R(rx - 0.6, ry, rx + 3.2, ry + 1.4, bd, r=0.4)

    return s.finish(rim=1.0, glow_color=accent, glow_blur=max(2.0, u * 0.45))


# ---- role emblems ----------------------------------------------------------
# What each monitor shows: one plain symbol per job, drawn in a -1..1 box.
EMBLEMS = ("core", "code", "bulb", "shield", "globe", "containers", "block", "hammer", "magnifier",
           "brush", "network", "check", "eye", "lines", "folder", "book", "megaphone", "chat",
           "chart", "coin", "target")


def draw_emblem(s, kind, cx, cy, r, color, bg):
    def X(v):
        return cx + v * r

    def Y(v):
        return cy + v * r

    lw = r * 0.2

    def L(pts, w=lw, c=color):
        s.line([(X(a), Y(b)) for a, b in pts], c, w)

    def C(a, b, rad, fill=None, w=lw, c=color):
        s.ellipse(X(a - rad), Y(b - rad), X(a + rad), Y(b + rad), fill=fill, outline=None if fill else c, width=w)

    if kind == "core":
        C(0, 0, 0.85)
        C(0, 0, 0.5, w=lw * 0.6)
        C(0, 0, 0.22, fill=color)
    elif kind == "code":
        L([(-0.3, -0.55), (-0.85, 0), (-0.3, 0.55)])
        L([(0.3, -0.55), (0.85, 0), (0.3, 0.55)])
        L([(0.14, -0.75), (-0.14, 0.75)])
    elif kind == "bulb":
        C(0, -0.25, 0.6)
        L([(-0.22, 0.5), (0.22, 0.5)])
        L([(-0.16, 0.8), (0.16, 0.8)])
        L([(0, -0.25), (0, 0.3)], w=lw * 0.7)
    elif kind == "shield":
        s.poly([(X(-0.72), Y(-0.75)), (X(0.72), Y(-0.75)), (X(0.72), Y(0.05)), (X(0), Y(0.88)), (X(-0.72), Y(0.05))], color)
        s.poly([(X(-0.4), Y(-0.45)), (X(0.4), Y(-0.45)), (X(0.4), Y(0.0)), (X(0), Y(0.48)), (X(-0.4), Y(0.0))], bg)
    elif kind == "globe":
        C(0, 0, 0.82)
        L([(-0.82, 0), (0.82, 0)], w=lw * 0.7)
        s.ellipse(X(-0.36), Y(-0.82), X(0.36), Y(0.82), outline=color, width=lw * 0.7)
    elif kind == "containers":
        for bx0, by0, bx1, by1 in ((-0.88, 0.08, -0.06, 0.8), (0.06, 0.08, 0.88, 0.8), (-0.41, -0.8, 0.41, -0.08)):
            s.rect(X(bx0), Y(by0), X(bx1), Y(by1), outline=color, width=lw * 0.8, r=r * 0.08)
            for i in (0.33, 0.66):
                L([(bx0 + (bx1 - bx0) * i, by0 + 0.2), (bx0 + (bx1 - bx0) * i, by1 - 0.2)], w=lw * 0.5)
    elif kind == "block":
        C(0, 0, 0.8)
        L([(-0.55, -0.55), (0.55, 0.55)])
    elif kind == "hammer":
        s.rect(X(-0.78), Y(-0.85), X(0.6), Y(-0.3), fill=color, r=r * 0.1)
        L([(0, -0.3), (0, 0.85)], w=lw * 1.3)
    elif kind == "magnifier":
        C(-0.18, -0.18, 0.55)
        L([(0.24, 0.24), (0.8, 0.8)], w=lw * 1.4)
    elif kind == "brush":
        L([(0.8, -0.8), (-0.05, 0.05)], w=lw * 1.1)
        C(-0.42, 0.42, 0.36, fill=color)
    elif kind == "network":
        nodes = ((0, -0.62), (-0.68, 0.52), (0.68, 0.52))
        L([nodes[0], nodes[1], nodes[2], nodes[0]], w=lw * 0.7)
        for a, b in nodes:
            C(a, b, 0.24, fill=color)
    elif kind == "check":
        L([(-0.75, 0.05), (-0.22, 0.58), (0.78, -0.58)], w=lw * 1.4)
    elif kind == "eye":
        s.poly([(X(-0.9), Y(0)), (X(-0.4), Y(-0.48)), (X(0.4), Y(-0.48)), (X(0.9), Y(0)), (X(0.4), Y(0.48)), (X(-0.4), Y(0.48))], color)
        C(0, 0, 0.34, fill=bg)
        C(0, 0, 0.14, fill=color)
    elif kind == "lines":
        for i, ln in enumerate((0.8, 0.45, 0.7, 0.3)):
            y = -0.66 + i * 0.44
            C(-0.78, y, 0.09, fill=color)
            L([(-0.5, y), (-0.5 + ln * 1.3, y)], w=lw * 0.8)
    elif kind == "folder":
        s.poly([(X(-0.85), Y(-0.6)), (X(-0.2), Y(-0.6)), (X(0.0), Y(-0.35)), (X(0.85), Y(-0.35)), (X(0.85), Y(0.7)), (X(-0.85), Y(0.7))], color)
        s.rect(X(-0.62), Y(-0.08), X(0.62), Y(0.06), fill=bg)
    elif kind == "book":
        s.poly([(X(-0.9), Y(-0.55)), (X(0), Y(-0.35)), (X(0), Y(0.75)), (X(-0.9), Y(0.55))], color)
        s.poly([(X(0.9), Y(-0.55)), (X(0), Y(-0.35)), (X(0), Y(0.75)), (X(0.9), Y(0.55))], shade(color, 0.72))
        L([(0, -0.35), (0, 0.75)], w=lw * 0.6, c=bg)
    elif kind == "megaphone":
        s.poly([(X(-0.35), Y(-0.28)), (X(0.72), Y(-0.8)), (X(0.72), Y(0.8)), (X(-0.35), Y(0.28))], color)
        s.rect(X(-0.85), Y(-0.28), X(-0.42), Y(0.28), fill=color, r=r * 0.06)
    elif kind == "chat":
        s.rect(X(-0.85), Y(-0.7), X(0.85), Y(0.35), fill=color, r=r * 0.22)
        s.poly([(X(-0.45), Y(0.3)), (X(-0.05), Y(0.3)), (X(-0.55), Y(0.85))], color)
        for a in (-0.4, 0.0, 0.4):
            C(a, -0.18, 0.11, fill=bg)
    elif kind == "chart":   # rising bars + a baseline: Tally / stats
        L([(-0.85, 0.8), (0.85, 0.8)], w=lw * 0.7)
        for i, (bx, h) in enumerate(((-0.62, 0.5), (-0.2, 0.95), (0.22, 0.7), (0.64, 1.35))):
            s.rect(X(bx - 0.16), Y(0.75 - h), X(bx + 0.16), Y(0.72), fill=color, r=r * 0.05)
    elif kind == "coin":    # a coin with a currency slash: Oracle / market
        C(0, 0, 0.8)
        C(0, 0, 0.55, w=lw * 0.5)
        L([(0.12, -0.5), (-0.12, 0.5)], w=lw * 0.8)
        for yy in (-0.18, 0.18):
            L([(-0.28, yy), (0.28, yy)], w=lw * 0.7)
    elif kind == "target":  # crosshair: Redcell / authorized recon
        C(0, 0, 0.78)
        C(0, 0, 0.3, fill=color)
        for a, b, c, d in ((-1.0, 0, -0.5, 0), (1.0, 0, 0.5, 0), (0, -1.0, 0, -0.5), (0, 1.0, 0, 0.5)):
            L([(a, b), (c, d)], w=lw * 0.8)


# ---- furniture -------------------------------------------------------------
def draw_desk(w, desk_h, mon_w, mon_h, accent, emblem, active):
    """A desk seen from the front with its monitor standing on the right-hand
    side, showing the role emblem. The robot is drawn behind it, so the front
    panel is left plain: the dashboard writes the name plate there as real
    text, which stays readable at any size."""
    gap = 6
    h = desk_h + mon_h + gap
    s = Sheet(w, h)
    top = mon_h + gap
    trim = accent if active else shade(accent, 0.45)

    # monitor: stand, bezel, screen, emblem
    mx0 = w - mon_w - 4
    s.rect(mx0 + mon_w / 2 - 4, mon_h - 1, mx0 + mon_w / 2 + 4, top + 1, fill=BODY_DARK)
    s.rect(mx0 + mon_w / 2 - 14, top - 2.5, mx0 + mon_w / 2 + 14, top + 0.5, fill=BODY_LIGHT, r=1)
    s.rect(mx0, 0, mx0 + mon_w, mon_h, fill=BODY_DARK, r=3)
    s.rect(mx0, 0, mx0 + mon_w, mon_h, outline=BODY_LIGHT, width=0.8, r=3)
    screen_bg = shade(accent, 0.2 if active else 0.13)
    s.rect(mx0 + 3, 3, mx0 + mon_w - 3, mon_h - 3, fill=screen_bg, r=1.5)
    if active:
        halo = s.overlay()
        draw_emblem(halo, emblem, mx0 + mon_w / 2, mon_h / 2, mon_h * 0.3, accent[:3] + (190,), screen_bg)
        s.merge(halo, blur=1.4)
    draw_emblem(s, emblem, mx0 + mon_w / 2, mon_h / 2, mon_h * 0.3, shade(accent, 1.15) if active else shade(accent, 0.85), screen_bg)
    sheen = s.overlay()
    sheen.poly([(mx0 + 3, 3), (mx0 + mon_w * 0.55, 3), (mx0 + mon_w * 0.3, mon_h - 3), (mx0 + 3, mon_h - 3)], (255, 255, 255, 16))
    s.merge(sheen)

    # keyboard edge on the desk top, in front of where the robot sits
    s.rect(w * 0.12, top - 3, w * 0.5, top, fill=shade(BODY_LIGHT, 0.85), r=1)

    # desk: slab, lit trim, recessed front panel (the name plate), feet
    s.rect(0, top, w, top + 8, fill=BODY_LIGHT, r=2)
    s.rect(0, top, w, top + 2.5, fill=shade(BODY_LIGHT, 1.3), r=1.2)
    s.rect(3, top + 8, w - 3, h - 3, fill=PANEL_RAISED)
    s.rect(3, top + 8, w - 3, top + 10.5, fill=trim)
    s.rect(9, top + 15, w - 9, h - 9, fill=shade(PANEL, 0.8), r=2)
    s.rect(9, top + 15, w - 9, h - 9, outline=shade(LINE, 1.2), width=0.6, r=2)
    s.ellipse(w - 9, top + 2.5, w - 5, top + 6.5, fill=trim)
    for fx in (5, w - 17):
        s.rect(fx, h - 3, fx + 12, h, fill=BODY_DARK)
    return s.finish(rim=1.0, glow_color=accent if active else None, glow_blur=2.0)


def draw_tube(w, h, accent):
    """Recharge pod: a glass cylinder of coolant on a plinth, with a bolt on
    the plinth so it reads as a charger rather than a lamp."""
    s = Sheet(w, h)
    cap, plinth = h * 0.06, h * 0.12
    gx0, gx1, gy0, gy1 = w * 0.12, w * 0.88, cap, h - plinth
    glass = s.overlay()
    glass.rect(gx0, gy0, gx1, gy1, fill=accent[:3] + (120,), r=w * 0.1)
    glass.rect(gx0 + (gx1 - gx0) * 0.32, gy0, gx0 + (gx1 - gx0) * 0.68, gy1, fill=shade(accent, 1.2)[:3] + (110,))
    s.merge(glass)
    fx = s.overlay()
    fx.rect(gx0 + 2, gy0 + 3, gx0 + (gx1 - gx0) * 0.22, gy1 - 3, fill=(255, 255, 255, 70), r=1)   # glass highlight
    random.seed(sum(accent[:3]) + int(h))
    for _ in range(max(4, int(h / 28))):
        bx, by, br = random.uniform(gx0 + 4, gx1 - 6), random.uniform(gy0 + 8, gy1 - 8), random.uniform(1.0, 2.4)
        fx.ellipse(bx, by, bx + br, by + br, fill=(255, 255, 255, 120))
    s.merge(fx)
    s.rect(gx0, gy0, gx1, gy1, outline=BODY_LIGHT, width=0.8, r=w * 0.1)
    s.rect(w * 0.04, 0, w * 0.96, cap, fill=shade(LINE, 1.5), r=2)
    s.rect(0, gy1, w, h, fill=shade(LINE, 1.35), r=2)
    s.rect(0, gy1, w, gy1 + 2, fill=shade(STEEL, 0.8), r=1)
    bx, by, bs = w / 2, gy1 + plinth * 0.55, plinth * 0.36
    s.poly([(bx + bs * 0.35, by - bs), (bx - bs * 0.6, by + bs * 0.15), (bx - bs * 0.05, by + bs * 0.15),
            (bx - bs * 0.35, by + bs), (bx + bs * 0.6, by - bs * 0.15), (bx + bs * 0.05, by - bs * 0.15)], accent)
    return s.finish(rim=1.0, glow_color=accent, glow_blur=2.5)


# ---- the building ----------------------------------------------------------
# The room is a cutaway tower: a ground floor (Ultron's office) and as many
# agent storeys as the screen width needs. Each is one 1280-unit-wide strip
# the dashboard crops to its layout width, so nothing here may depend on the
# right-hand end being visible. Walls stay quiet on purpose -- the colour in
# the scene belongs to the agents.
STOREY_W, STOREY_H, STOREY_WALL = 1280, 264, 224     # strip size, and the floor line within it
GROUND_H, GROUND_WALL = 424, 384


# ---- texture helpers (metallic pass) --------------------------------------
def _frange(a, b, step):
    x = a
    while x < b:
        yield x
        x += step


def brushed(s, x0, y0, x1, y1, seed=0, density=3, light=14, dark=20):
    """Faint horizontal brushed-metal streaks over a region, so a flat metal
    fill reads as brushed steel."""
    ov = s.overlay()
    random.seed(seed)
    yy = y0
    while yy < y1:
        if random.random() < 0.5:
            ov.rect(x0, yy, x1 - random.uniform(0, (x1 - x0) * 0.3), yy + 0.5, fill=(210, 220, 235, random.randint(4, light)))
        else:
            ov.rect(x0 + random.uniform(0, (x1 - x0) * 0.3), yy, x1, yy + 0.5, fill=(0, 0, 0, random.randint(6, dark)))
        yy += random.uniform(2, density + 2)
    s.merge(ov)


def rivets(s, x0, x1, y, step, color=None, r=0.8):
    color = color or shade(STEEL, 0.75)
    for rx in _frange(x0, x1, step):
        s.ellipse(rx - r, y - r, rx + r, y + r, fill=color)
        s.ellipse(rx - r * 0.4, y - r * 0.5, rx + r * 0.2, y, fill=shade(color, 1.4))   # tiny highlight


def specks(s, x0, y0, x1, y1, seed=0, n=40, color=(0, 0, 0, 40)):
    ov = s.overlay()
    random.seed(seed)
    for _ in range(n):
        sx, sy = random.uniform(x0, x1), random.uniform(y0, y1)
        ov.ellipse(sx, sy, sx + random.uniform(0.6, 1.6), sy + random.uniform(0.6, 1.6), fill=color)
    s.merge(ov)


def warn_plate(s, x, y, w, h, seed=0):
    """A small stencilled warning/ID plate -- the kind of label a real machine
    room is covered in."""
    s.rect(x, y, x + w, y + h, fill=shade(PANEL_RAISED, 1.2), outline=shade(LINE, 1.4), width=0.7)
    random.seed(seed)
    hazard = random.random() < 0.4
    for i, ly in enumerate(_frange(y + 2.5, y + h - 1.5, 3)):
        c = (200, 170, 40, 200) if (hazard and i == 0) else (150, 160, 175, 150)
        s.rect(x + 2, ly, x + 2 + random.uniform(0.4, 0.85) * (w - 4), ly + 1, fill=c)


def _wall(w, h, wall_h):
    s = Sheet(w, h, pad=0)
    s.rect(0, 0, w, wall_h, fill=PANEL)
    brushed(s, 0, 0, w, wall_h, seed=int(w + wall_h), density=4)   # brushed-metal wall
    for px_ in range(0, w, 96):                       # panel seams + rivets down each seam
        s.rect(px_, 0, px_ + 1, wall_h, fill=shade(PANEL, 1.6))
        s.rect(px_ + 1, 0, px_ + 2, wall_h, fill=shade(PANEL, 0.5))
        for ry in _frange(20, wall_h - 6, 30):
            s.ellipse(px_ - 0.7, ry, px_ + 0.7, ry + 1.4, fill=shade(LINE, 1.3))
    for py_ in range(48, wall_h, 60):                 # horizontal panel joints
        s.rect(0, py_, w, py_ + 0.8, fill=shade(PANEL, 1.35))
        s.rect(0, py_ + 0.8, w, py_ + 1.4, fill=shade(PANEL, 0.6))
    grid = s.overlay()
    for gx in range(0, w, 32):
        grid.rect(gx, 0, gx + 0.5, wall_h, fill=(61, 214, 255, 8))
    for gy in range(0, wall_h, 32):
        grid.rect(0, gy, w, gy + 0.5, fill=(61, 214, 255, 8))
    s.merge(grid)
    wash = s.overlay()                                # ceiling light falling down the wall
    wash.rect(0, 9, w, 14, fill=(200, 235, 255, 105))
    s.merge(wash, blur=9)
    s.rect(0, 0, w, 8, fill=shade(LINE, 0.7))         # underside of the slab above
    s.rect(0, 8, w, 10, fill=(150, 178, 195, 255))    # light strip
    rivets(s, 6, w, 4, 40, color=shade(STEEL, 0.6))   # bolts along the slab underside
    # twin conduit run with brackets + bolts
    s.rect(0, 30, w, 36, fill=shade(LINE, 1.15))
    s.rect(0, 30, w, 31, fill=shade(LINE, 1.8))
    s.rect(0, 35.2, w, 36, fill=shade(LINE, 0.5))
    s.rect(0, 40, w, 43, fill=shade(LINE, 0.9))       # a thinner pipe below it
    for hx in range(40, w, 128):
        s.rect(hx, 26, hx + 4, 44, fill=LINE)
        s.ellipse(hx + 0.6, 32, hx + 3.4, 34.8, fill=shade(STEEL, 0.7))
    for wx in range(70, w, 150):                      # scattered warning/ID plates
        warn_plate(s, wx, 52, 20, 12, seed=wx)
    return s


def _slab(s, w, h, wall_h, base):
    """The floor the desks stand on. The conveyor is drawn over its front
    edge by the dashboard, so it stays plain."""
    s.rect(0, wall_h, w, h, fill=VOID if base else shade(LINE, 0.62))
    s.rect(0, wall_h, w, wall_h + 2.5, fill=shade(STEEL, 0.55))
    s.rect(0, wall_h + 2.5, w, wall_h + 3.2, fill=shade(LINE, 0.4))   # lit front lip + shadow
    rivets(s, 10, w, wall_h + 1.2, 48, color=shade(STEEL, 0.7), r=0.7)
    if base:
        for gx in range(0, w, 24):
            s.rect(gx, wall_h + 3, gx + 1, h, fill=(24, 26, 30, 255))
    else:
        s.rect(0, h - 5, w, h, fill=shade(LINE, 0.35))
        for gx in range(0, w, 20):                    # tread plate: diamond grating ticks
            s.rect(gx + 3, wall_h + 6, gx + 12, wall_h + 6.6, fill=shade(LINE, 0.85))
        for gx in range(16, w, 64):
            s.ellipse(gx, h - 16, gx + 3, h - 13, fill=shade(LINE, 1.4))
        specks(s, 0, wall_h + 4, w, h, seed=int(w), n=30, color=(0, 0, 0, 34))  # scuffs


def draw_storey():
    s = _wall(STOREY_W, STOREY_H, STOREY_WALL)
    _slab(s, STOREY_W, STOREY_H, STOREY_WALL, False)
    return s.finish(rim=0)


def draw_skyline(s, x0, y0, w, h):
    """The window: night sky, a moon, lit towers, then a frame with mullions
    so it reads as glass in a wall rather than a poster."""
    s.rect(x0, y0, x0 + w, y0 + h, fill=(10, 14, 24, 255))
    sky = s.overlay()
    sky.rect(x0, y0 + h * 0.45, x0 + w, y0 + h, fill=(40, 70, 110, 70))
    s.merge(sky, blur=10)
    s.ellipse(x0 + w * 0.74, y0 + h * 0.12, x0 + w * 0.74 + 22, y0 + h * 0.12 + 22, fill=(235, 240, 250, 255))
    random.seed(7)
    x = x0 + 2
    while x < x0 + w - 8:
        bw = min(random.randint(18, 40), int(x0 + w - x - 2))
        bh = random.randint(int(h * 0.3), int(h * 0.85))
        tower = shade((26, 31, 40, 255), random.uniform(0.85, 1.3))
        s.rect(x, y0 + h - bh, x + bw, y0 + h, fill=tower)
        win = CYAN if random.random() < 0.3 else (255, 196, 110, 255)
        for wy in range(int(y0 + h - bh + 6), int(y0 + h - 5), 9):
            for wx in range(int(x + 4), int(x + bw - 5), 8):
                if random.random() < 0.45:
                    s.rect(wx, wy, wx + 3.5, wy + 4, fill=win)
        x += bw + random.randint(2, 5)
    frame = shade(LINE, 1.7)
    s.rect(x0 - 5, y0 - 5, x0 + w + 5, y0 + h + 5, outline=frame, width=5)
    s.rect(x0 + w / 3 - 1.5, y0, x0 + w / 3 + 1.5, y0 + h, fill=frame)
    s.rect(x0 + 2 * w / 3 - 1.5, y0, x0 + 2 * w / 3 + 1.5, y0 + h, fill=frame)
    s.rect(x0 - 9, y0 + h + 5, x0 + w + 9, y0 + h + 11, fill=shade(LINE, 2.0), r=1)   # sill


def draw_server_rack(s, x0, y0, w, h):
    """Rack units with drive bays, status LEDs and a vent, so it reads as a
    server cabinet and not a locker."""
    s.rect(x0, y0, x0 + w, y0 + h, fill=PANEL_RAISED, r=3)
    s.rect(x0, y0, x0 + w, y0 + h, outline=shade(LINE, 1.6), width=1.5, r=3)
    random.seed(3)
    units = 9
    uh = (h - 34) / units
    for i in range(units):
        uy = y0 + 8 + i * uh
        s.rect(x0 + 6, uy, x0 + w - 6, uy + uh - 3, fill=shade(PANEL, 0.75), r=1)
        for b in range(4):                                          # drive bays
            s.rect(x0 + 24 + b * 9, uy + 2.5, x0 + 30 + b * 9, uy + uh - 5.5, fill=shade(LINE, 1.25))
        for l, c in enumerate((GREEN, CYAN if random.random() < 0.7 else RED_BRIGHT)):
            s.ellipse(x0 + 9 + l * 6, uy + uh / 2 - 3.2, x0 + 13 + l * 6, uy + uh / 2 + 0.8, fill=c)
    for vy in range(int(y0 + h - 22), int(y0 + h - 6), 4):           # vent
        s.rect(x0 + 10, vy, x0 + w - 10, vy + 1.5, fill=shade(LINE, 0.6))


def draw_ground():
    s = _wall(STOREY_W, GROUND_H, GROUND_WALL)
    draw_skyline(s, 214, 70, 300, 190)
    # two wall consoles between the window and Ultron's desk
    for cx, cw, ch, seed in ((566, 96, 118, 11), (684, 78, 100, 23)):
        random.seed(seed)
        s.rect(cx, 66, cx + cw, 66 + ch, fill=PANEL_RAISED, r=3)
        s.rect(cx, 66, cx + cw, 66 + ch, outline=shade(LINE, 1.4), width=1, r=3)
        s.rect(cx + 7, 74, cx + cw - 7, 66 + ch * 0.5, fill=(20, 44, 52, 255), r=2)
        for ly in range(80, int(66 + ch * 0.5) - 4, 7):
            s.rect(cx + 11, ly, cx + 11 + random.uniform(0.3, 0.8) * (cw - 24), ly + 2, fill=shade(CYAN, 0.75))
        for i, c in enumerate((CYAN, GREEN, RED_BRIGHT, CYAN, GREEN)):
            bx = cx + 8 + i * ((cw - 16) / 5)
            s.rect(bx, 66 + ch * 0.62, bx + (cw - 16) / 5 - 4, 66 + ch * 0.62 + 9, fill=c if random.random() < 0.7 else shade(c, 0.3), r=1)
        s.rect(cx + 8, 66 + ch * 0.86, cx + cw - 8, 66 + ch * 0.86 + 1.5, fill=shade(LINE, 1.6))
    _slab(s, STOREY_W, GROUND_H, GROUND_WALL, True)
    draw_server_rack(s, 84, GROUND_WALL - 236, 92, 236)
    reflect = s.overlay()                              # the room's light on the floor
    reflect.rect(0, GROUND_WALL + 3, STOREY_W, GROUND_WALL + 16, fill=(61, 214, 255, 26))
    s.merge(reflect, blur=5)
    return s.finish(rim=0)


def draw_app_icon(size, maskable=False):
    """Installable-app icon: the dashboard header's own mark (a hexagon
    outline in the site's oxide orange with a gold core pulse), drawn large
    on the void background. Original geometry, no source image. `maskable`
    keeps everything inside Android's safe zone (the centre 80%) so nothing
    is clipped when the launcher masks it to a circle or squircle."""
    s = size
    img = Image.new("RGBA", (s, s), (10, 11, 13, 255))
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = s / 2
    r = s * (0.30 if maskable else 0.40)
    oxide = (255, 138, 30, 255)
    gold = (255, 178, 56, 255)
    import math
    hexagon = [(cx + r * math.cos(math.radians(90 + 60 * i)), cy - r * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
    d.polygon(hexagon, outline=oxide, width=max(2, s // 24))
    inner = r * 0.62
    d.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], outline=(255, 178, 56, 110), width=max(1, s // 64))
    core = r * 0.30
    core_layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(core_layer).ellipse([cx - core, cy - core, cx + core, cy + core], fill=gold)
    img.alpha_composite(glow(core_layer, gold, blur=max(4, s // 16)))
    img.alpha_composite(layer)
    ImageDraw.Draw(img).ellipse([cx - core * 0.45, cy - core * 0.45, cx + core * 0.45, cy + core * 0.45], fill=(255, 233, 194, 255))
    return img


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print("wrote", path, img.size)


# Who is who: colour -> (helmet crest, monitor emblem). Mirrors the SUBAGENTS
# table in ultron-dashboard.html.
AGENT_LOOKS = {
    "cyan": ("visor", "code"),            # Engineer
    "green": ("dome", "bulb"),            # Learner
    "amber": ("plates", "shield"),        # Sentinel (heavy build)
    "violet": ("antenna", "globe"),       # Scout
    "blue": ("visor", "containers"),      # Dockhand
    "mint": ("horns", "block"),           # Gatekeeper
    "copper": ("visor", "hammer"),        # Forge
    "sky": ("antenna", "magnifier"),      # Seeker
    "teal": ("fin", "brush"),             # Muse
    "indigo": ("antenna", "network"),     # Relay
    "lime": ("dome", "check"),            # Proof
    "rose": ("horns", "eye"),             # Auditor
    "steel": ("dome", "lines"),           # Scribe
    "lavender": ("dome", "folder"),       # Archivist
    "peach": ("dome", "book"),            # Librarian
    "magenta": ("fin", "megaphone"),      # Herald
    "olive": ("fin", "chat"),             # Envoy
    "gold": ("dome", "chart"),            # Tally (stats)
    "bitcoin": ("antenna", "coin"),       # Oracle (crypto market)
    "crimson": ("horns", "target"),       # Redcell (ethical-hacking lab)
    "cobalt": ("plates", "eye"),          # Bastion (sentinel-defense)
    "slate": ("antenna", "lines"),        # Overwatch (overwatch-logger)
    "ember": ("dome", "code"),            # Anvil (forge-coder)
    "vermilion": ("antenna", "target"),   # Breach (red-team-sandbox)
    "ivory": ("dome", "network"),         # Architect (architecture-lead)
    "mulberry": ("visor", "check"),       # Critic (code-reviewer)
    "graphite": ("plates", "chart"),      # Steward (homelab-monitor)
    "candy": ("antenna", "brush"),        # Pixel (pixel-artist)
    "spearmint": ("dome", "block"),       # Arbiter (game-balancer)
    "royalgold": ("crown", "core"),       # Game Master -- gold crown
}


def main():
    # Ultron: 10 room units per grid cell (200 wide), the agents 6 (120 wide)
    # -- both about double the previous pass. His body is gunmetal / dark
    # platinum / weathered titanium with polished titanium plating and RED
    # eyes + core (owner request 2026-09-16).
    for pose in ("walk_a", "walk_b", "work"):
        save(draw_robot(10, U_PLATE, pose, "crown", eye=RED_BRIGHT, bd=U_GUNMETAL, bm=U_PLATINUM, bl=U_TITANIUM),
             f"ultron_{pose}.png")
    for active in (False, True):
        save(draw_desk(280, 96, 124, 88, RED_BRIGHT, "core", active), f"desk_ultron_{'active' if active else 'idle'}.png")
    save(draw_tube(64, 280, RED_BRIGHT), "tube_red.png")

    for name, color in AGENT_COLORS.items():
        crest, emblem = AGENT_LOOKS[name]
        save(draw_robot(6, color, "work", crest, heavy=(name == "amber")), f"agent_{name}.png")
        for active in (False, True):
            save(draw_desk(150, 68, 62, 48, color, emblem, active), f"desk_{name}_{'active' if active else 'idle'}.png")
        save(draw_tube(40, 176, color), f"tube_{name}.png")

    save(draw_storey(), "room_storey.png")
    save(draw_ground(), "room_ground.png")

    # Installable-app icons, referenced by /manifest.webmanifest in app.py.
    save(draw_app_icon(192), "app-icon-192.png")
    save(draw_app_icon(512), "app-icon-512.png")
    save(draw_app_icon(512, maskable=True), "app-icon-maskable-512.png")


if __name__ == "__main__":
    main()
