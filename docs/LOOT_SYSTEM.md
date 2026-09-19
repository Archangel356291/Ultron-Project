# Loot System — `pixel-game/loot-engine.js`

A pure, data-driven, seeded loot engine for the Odin pixel-game (the
Expedition sub-game inside `odin-dashboard.html`). No dependencies. Loads as a
browser global (`window.LootEngine`) and as a Node module
(`require('./pixel-game/loot-engine.js')`), so the same code the page runs is the
code the tests run.

Tests: `node dev-tools/test_loot_engine.js` (seeded reproducibility, rarity
distribution, stat-roll limits, unique ids, validation, invalid-combo rejection).

## Concepts

- **Base definition** vs **generated instance** are separate. Bases live in the
  `BASES` array; instances come only from `generate()` / `rollDrop()`.
- **Seeded**: `generate(baseId, {seed})` is deterministic — same seed, same item.
  Saves store the seed so an item can be reproduced for debugging.
- **Rarity-weighted**: `rollDrop()` rolls a *global* rarity by tier weight first,
  then picks a base that can produce it, so high tiers stay genuinely rare
  regardless of how many bases exist.

## Rarity tiers

| Tier | Key | Color | Shape | Rolled stats | Weight |
|---|---|---|---|---|---|
| T1 | common | `#9aa2ae` | ● | 0–1 | 6900 |
| T2 | uncommon | `#33d17a` | ▲ | 1 | 2000 |
| T3 | rare | `#3d9bff` | ◆ | 1–2 | 700 |
| T4 | epic | `#b084f0` | ⬟ | 2–3 | 250 |
| T5 | legendary | `#ff9d3c` | ★ | 3–4 + unique | 45 |
| T6 | mythic | `#ff5a7a` | ✦ | 4–5 + build-defining | 5 |

Shape + colorblind alternate (`cb`) mean rarity never relies on colour alone.

## Item instance shape

```js
{
  id, base, name, fullName, type, zone, slot, rarity, tier, tierLabel,
  color, colorblind, shape, description, element,
  baseStats: { statKey: value },
  rolledStats: [ { k, label, value, unit } ],
  effects: [ "…" ],           // innate + affix + rarity effects
  affixes: { prefix, suffix },
  value, sellPrice, dropWeight, upgradeCompat: [ zone, type ],
  seed, ilvl,
  stats: { statKey: value },  // baseStats+rolled merged, for the UI
  mods:  [ "…" ]              // = effects, for the existing UI
}
```

`type` ∈ weapon · armor · shield · throwable · artifact · consumable · ammo.
`slot` maps armour/weapons to the Expedition's five equip slots
(core · legs · arm · util · head) or is `null` for carry-only loot.

## 21 stats

damage, fire rate, crit chance, crit damage, reload speed, capacity, accuracy,
heat cap, cooldown reduction, armor, max health, max shield, shield regen,
energy regen, move speed, dash regen, loot find, repair power, elemental
resistance, armor penetration, status chance. Roll ranges live in `STAT_ROLL`.

## Affixes

Prefixes boost a stat (`Reinforced`, `Overclocked`, `Precise`, `Charged`,
`Swift`, `Fortified`, `Regenerative`, `Efficient`, `Scavenger`, `Piercing`).
Suffixes add an effect (`of Cinders`, `of Frost`, `of Instability`,
`of the Prototype`, `of the Ancients`, `of Corruption`). Rare+ get a prefix;
Legendary+ (and Epic weapons) get a suffix. Names build as
`[Tier] [Prefix] [Base] [Suffix]`, e.g. *Epic Overclocked Plasma Scattergun*.

## API

```js
LootEngine.generate(baseId, { seed, ilvl, rarity })  // one specific base
LootEngine.rollDrop({ seed, ilvl, types, slots })    // a random weighted drop
LootEngine.validate(item)  // -> { ok, errors: [...] }
LootEngine.TIERS / STATS / AFFIXES / BASES / listBases()
```

## Adding content (no gameplay code changes)

- **New item**: append to `BASES` using a helper (`W` weapon, `A` armor,
  `S` shield, `T` throwable, `R` artifact, `C` consumable, `M` ammo). Give it an
  id, name, rarity range `[minTier, maxTier]`, and a base-stat profile.
- **New affix**: add to `AFFIXES.prefix` or `AFFIXES.suffix`.
- **New rarity / rebalance**: edit `TIERS` (weight = rarity; `rolls` = stat count).
- **New stat**: add to `STATS`, `STAT_ROLL`, and the relevant `ROLL_POOL[type]`.

After any change, run `node dev-tools/test_loot_engine.js`.

## Not yet wired (see GAME_MASTER_ROADMAP.md)

Item effects/elements are generated and displayed but there is **no combat
simulation yet**, so effects like burn/freeze are descriptive. Vendor/sell,
crafting/dismantle, and stacking of consumables/ammo are modelled in the data
(`value`, `sellPrice`, `stack`-style fields) but not yet surfaced in the UI.
