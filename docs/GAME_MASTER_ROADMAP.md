# Game Master Roadmap — Odin Pixel-Game

Single source of truth for the pixel robot game growing inside Odin's
dashboard. Last updated 2026-09-17.

---

## 0. What this project actually is (read first)

The game lives **inside `odin-dashboard.html`** as "Ultron's Corner" — a
canvas pixel-art room plus an idle/incremental economy ("Odin's Foundry") and
a customization + loot sub-game ("Odin's Expedition"). It is a **browser
idle/management game with a modular robot builder and a seeded loot system**,
persisted per-viewer in `localStorage` (`odin_foundry_v1`). Data-driven parts
now live in `pixel-game/*.js` and are unit-tested with Node.

It is **not** (yet) a real-time action-adventure engine: there is no player
movement, no live combat frame loop, no enemies, no scenes/biomes rendered as
playable levels. Much of the seven-part brief (combat, enemies/bosses, world
regions, story missions, audio) describes that action game. Building it is a
**large new system and a scope/technology decision** (see §7). Everything below
separates "done", "data/foundation done", and "needs the action-game decision".

---

## 1. Implemented & working (verified, 0 console errors)

- **Idle economy (Odin's Foundry)**: robots assembled → march out → mint
  currency; upgrades with exponential cost scaling; offline accrual; auto-collect.
- **Evolving currency**: Bits → Bytes → Chits → Scrip → Nanits (×1000 each),
  used for every balance and cost.
- **Multi-bay factory**: up to 10 unlockable bays, per-bay colour/weapon, robot
  build progress bars, march-into-formation, salute.
- **Modular Chassis Builder (Expedition)**: 38 part categories in 7 collapsible
  sections (native `<select>`s), 6 quick presets (Scout/Tank/Hacker/Builder/
  Medic/Odin), user-saved named loadouts, live preview silhouette.
- **Robot cosmetic skins**: 13 palette-driven skins wired into the builder.
- **Data-driven loot engine** (`pixel-game/loot-engine.js`): 82 base items
  across weapon/armor/shield/throwable/artifact/consumable/ammo; 6 rarity tiers;
  21 stats; 16 affixes; seeded reproducible generation; validation; global
  rarity-weighted drops. Wired as the Expedition's drop source + starter gear.
  Tested: `node dev-tools/test_loot_engine.js` (12k+ assertions pass).
- **Colour-palette tokens** (`pixel-game/palettes.js`): 12 environments, 6 rarity
  (shape + colorblind-safe), combat/HUD set, 13 robot skins, accessibility set.
- **Equip loadout**: 5 slots (core/legs/arm/util/head); looted parts equip;
  summed stat totals; carry-only loot (consumables/artifacts/ammo/throwables).
- **Persistence**: one localStorage key, try/catch guarded, offline-time stamp.

Docs: `LOOT_SYSTEM.md`, `COLOR_PALETTES.md`, this file.

## 2. Partial / placeholder

- **Item effects & elements** are generated and shown (burn, freeze, EMP, etc.)
  but are **descriptive only** — no combat resolves them.
- **Adventures** resolve on a timer (Scout/Delve/Odyssey) and grant loot; there
  is no playable mission, just idle time → reward.
- **Environment palettes** are defined + documented but not applied to scenes
  (there are no scenes yet).
- **Economy**: `value`/`sellPrice` exist on items; no vendor/sell/dismantle UI.
- **Save system**: works, but no versioning/migration or corruption recovery.

## 3. Missing (needs the action-game decision in §7)

Combat (movement, aiming, hit detection, damage formulas, status effects) ·
enemies & bosses · world/biomes as playable regions · main/side missions &
objectives · story/dialogue/codex · skill trees & XP/levels · crafting/upgrading/
dismantling economy · vendors · audio/music · main/pause/settings menus ·
tutorial/onboarding · controller support · full accessibility toggles ·
save migration.

---

## 4. Dependencies between systems

```
palettes.js ──▶ rarity colours ──▶ loot UI, HUD, skins
loot-engine.js ──▶ Expedition loot ──▶ equip/loadout ──▶ (needs) combat
robot builder ──▶ loadout identity ──▶ (needs) combat + world
combat ──▶ enemies/bosses ──▶ world/missions ──▶ story/codex ──▶ progression
economy(value/sell) ──▶ vendors ──▶ progression
save versioning underlies everything that persists
```

Foundational layers (palettes, loot engine, builder, save) are in place; combat
is the keystone the rest of the action game hangs on.

## 5. Recommended order of implementation

**Critical (foundation — mostly done or safe next):**
1. ✅ Data-driven loot engine + tests + docs.
2. ✅ Palette tokens + rarity/combat colours + docs.
3. ✅ Modular builder + saved loadouts + skins.
4. ⬜ Save versioning + migration + corruption recovery (safe, no design risk).
5. ⬜ Vendor/sell/dismantle + material economy (uses existing `value`/`sellPrice`).

**High (needs the §7 decision):**
6. ⬜ Combat core: damage formula from equipped stats, status effects, a
   deterministic resolver — even before real-time, an *auto-battler* Expedition
   turns loadouts into outcomes and makes stats matter immediately.
7. ⬜ Enemies/bosses as data (archetypes, drops, telegraphs) feeding #6.
8. ⬜ Progression: XP/levels, unlockable recipes, skill/upgrade paths.

**Polish:**
9. ⬜ Codex/database (enemies/items/lore) — data-driven, easy win.
10. ⬜ Accessibility toggles (high-contrast/colorblind/reduced-glow) using tokens.
11. ⬜ Audio plan + minimal SFX/music states.

**Future / endgame:**
12. ⬜ Real-time movement + combat engine (if chosen in §7).
13. ⬜ World regions, missions, story campaign, New Game+.

## 6. Risks & design decisions

- **Save compatibility**: adding fields is safe (guards default them); changing
  item shape is not. The loot engine keeps a `version`; add a migration step
  before any breaking change. **Do not** wipe `odin_foundry_v1`.
- **Scope creep vs. the host**: this is a page inside a personal dashboard, not a
  standalone game project. Heavy real-time canvas combat may fight the dashboard
  for the main thread on phones. Keep the game in its own module/loop.
- **Balance**: rarity weights and stat ranges are first-pass; tune with the Node
  test's distribution output, not by feel.
- **No deploy without approval**: all work above is local + preview-tested only.

## 7. Questions requiring your approval

1. **Combat model** — pick one:
   - **(a) Auto-battler / idle-RPG** (recommended, low risk, fits the host):
     equipped stats + enemy data resolve Expedition outcomes deterministically;
     no real-time input. Highest value for least risk; reuses everything built.
   - **(b) Real-time action** (movement/aiming/dodging on a canvas): the full
     brief, but a large new engine and a performance risk inside the dashboard.
   - **(c) Turn-based tactics**: middle ground.
2. **Where should the game live** — keep it embedded in the dashboard, or split
   it into its own page/route (`/pixel-game`) so it can grow without bloating
   `odin-dashboard.html`?
3. **Story tone/canon** — how close to Marvel's Odin vs. an original
   "Odin-inspired" character? (Affects names, lore, and anything shareable.)
4. **Audio** — OK to add small self-hosted SFX/music files (size/perf budget),
   or keep silent for now?
5. **Deploy** — say the word and I'll rebuild the container, verify served bytes,
   and commit/push; until then everything stays local.

---

*Next safe step if you don't want to decide §7 yet:* item #4 (save
versioning/migration) and #5 (vendor/sell using existing item values) — both are
pure foundation, need no design call, and make the loot you already generate
meaningful.
