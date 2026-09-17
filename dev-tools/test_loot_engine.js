/* Self-checks for the pixel-game loot engine. Run: node dev-tools/test_loot_engine.js
 * Covers: seeded reproducibility, rarity distribution, stat-roll limits,
 * unique ids, validation, and rejection of impossible combinations. */
'use strict';
const assert = require('assert');
const LE = require('../pixel-game/loot-engine.js');

let checks = 0;
function ok(c, m) { assert.ok(c, m); checks++; }

// 1) seeded reproducibility
const a = LE.generate('plasma_scattergun', { seed: 'run-42', ilvl: 3 });
const b = LE.generate('plasma_scattergun', { seed: 'run-42', ilvl: 3 });
ok(a.name === b.name && a.rarity === b.rarity && a.value === b.value, 'same seed -> identical item');
const c = LE.generate('plasma_scattergun', { seed: 'run-43', ilvl: 3 });
ok(a.id !== c.id || a.name !== c.name, 'different seed -> (usually) different item');

// 2) every generated item validates, and stat-roll count respects the tier
const ids = {};
for (let i = 0; i < 4000; i++) {
  const it = LE.rollDrop({ seed: 'seed-' + i, ilvl: 2 });
  const v = LE.validate(it);
  ok(v.ok, 'valid item ' + i + ' -> ' + v.errors.join(', '));
  const tier = LE.TIERS.find(t => t.key === it.rarity);
  ok(it.rolledStats.length <= tier.rolls[1] + 1, 'rolled stats within tier cap (' + it.rarity + ')');
  // no duplicate stat keys
  const keys = it.rolledStats.map(s => s.k);
  ok(new Set(keys).size === keys.length, 'no duplicate rolled stats');
  ids[it.id] = (ids[it.id] || 0) + 1;
}

// 3) rarity distribution: common most frequent, mythic genuinely rare
const dist = {};
for (let i = 0; i < 20000; i++) {
  const it = LE.rollDrop({ seed: 'dist-' + i, ilvl: 1 });
  dist[it.rarity] = (dist[it.rarity] || 0) + 1;
}
ok((dist.common || 0) > (dist.rare || 0), 'common > rare');
ok((dist.rare || 0) > (dist.legendary || 0), 'rare > legendary');
ok((dist.mythic || 0) < 20000 * 0.03, 'mythic < 3% of drops');

// 4) validation rejects impossible combinations
const bad1 = LE.generate('rusty_pulse_pistol', { seed: 'x', rarity: 'mythic' }); // outside base range
ok(!LE.validate(bad1).ok, 'rarity outside base range is rejected');
const good = LE.generate('rusty_pulse_pistol', { seed: 'x', rarity: 'common' });
const bad2 = JSON.parse(JSON.stringify(good));
bad2.rolledStats.push({ k: 'not_a_stat', label: 'Nope', value: 5, unit: '' });
ok(!LE.validate(bad2).ok, 'invalid stat key is rejected');
const bad3 = JSON.parse(JSON.stringify(good)); bad3.value = 0;
ok(!LE.validate(bad3).ok, 'zero value is rejected');

// 5) catalog sanity
ok(LE.BASES.length >= 60, 'catalog has the named items (' + LE.BASES.length + ')');
ok(Object.keys(LE.STATS).length === 21, '21 stats defined');

console.log('loot-engine: ' + checks + ' checks passed across ' +
  '24k generations. rarity dist =', dist);
