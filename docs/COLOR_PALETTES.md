# Color Palettes — `pixel-game/palettes.js`

Reusable colour tokens for the Ultron pixel-game: biome/environment palettes,
loot-rarity colours, combat/HUD colours, player robot cosmetic skins, and
accessibility alternates. Data only — no hard-coded one-off colours in gameplay
code. Loads as `window.GamePalettes` (browser) and `require()` (Node).

> The dashboard's own visual identity (its CSS custom properties) is preserved
> and unchanged; these tokens are for the game layer and are applied where the
> game already has customization (the robot skin picker) or documented for the
> world/scenes that are still on the roadmap.

## Environment palettes (12)

Each: `{ name, colors: [bg, a, b, c, d, highlight], use }`.

| Palette | Intended use |
|---|---|
| Ultron Core | Ultron HQ, reactor rooms, title |
| Neon Hacker | terminals, hack minigames, net |
| Cyberpunk City | city streets, markets, rain |
| Industrial Scrapyard | scrapyards, foundry, salvage |
| Plasma Wasteland | blasted plasma flats, storms |
| Frozen Circuit | cryo labs, frozen ruins |
| Toxic Reactor | reactor cores, toxic caves |
| Desert Machine World | solar deserts, dune machines |
| Alien Void | alien ruins, void rifts |
| Underwater Tech Ruins | sunken labs, coral tech |
| Stealth / Ghost Protocol | stealth missions, night ops |
| Boss / Danger Mode | boss arenas, alarms |

Full hex values are in `palettes.js` (`GamePalettes.environments`).

## Loot rarity colours (6)

`GamePalettes.rarity[key]` → `{ label, color, border, glow, shape, cbSafe }`.
Hexes match the loot engine tiers. **Never colour alone**: every rarity also has
a distinct shape (● ▲ ◆ ⬟ ★ ✦) and a colorblind-safe alternate (`cbSafe`).

| Rarity | Color | Shape | Colorblind-safe |
|---|---|---|---|
| Common | `#9aa2ae` | ● | `#c9ccd2` |
| Uncommon | `#33d17a` | ▲ | `#7fd4ff` |
| Rare | `#3d9bff` | ◆ | `#5b8dff` |
| Epic | `#b084f0` | ⬟ | `#c98bff` |
| Legendary | `#ff9d3c` | ★ | `#ffc400` |
| Mythic | `#ff5a7a` | ✦ | `#00e5ff` |

## Combat / HUD colours

`GamePalettes.combat` defines: health, shield, energy, heat, xp, currency,
objective, friendly/neutral/enemy/elite/boss, crit, healing, shieldGain,
damageTaken, and the damage types fire/shock/cryo/corruption/emp, plus lootDrop,
interactable, warning, error. Use these tokens for every HUD element and
particle so colour meaning is consistent everywhere.

## Robot cosmetic skins (13)

`GamePalettes.robotSkins[key]` → `{ name, primary, secondary, shadow, highlight,
glow, eye, damage, effect }`. **Wired in**: the Expedition Chassis Builder's
skin picker uses these; selecting one sets the robot's eye/LED colour and is
saved per loadout. Skins: Ultron Cyan/Violet, Hacker Green, Crimson Assault,
Solar Gold, Arctic Blue, Toxic Reactor, Industrial Rust, Neon Pink, Royal
Purple, White/Chrome, Black Stealth, Rainbow/Prototype, Corrupted/Glitch.

## Accessibility

`GamePalettes.accessibility` provides a high-contrast UI palette plus toggle
names: `highContrast, colorblindSafe, reducedMotion, reducedGlow, largeText`.
Principles: important text/UI high-contrast; never success/fail as red-vs-green
alone (pair with icon + text); colorblind-safe alternates per rarity;
reduced-glow drops glow alpha to 0 with no strobing.

## Adding / changing palettes

Edit `palettes.js` — add a key to the relevant group. Keep pixel-art
readability: avoid blur-heavy glows that muddy sprites; glow tokens are for LED
accents, not full-screen bloom. No test harness is required for pure data, but
keep hex values valid and documented here.
