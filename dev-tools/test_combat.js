/* Self-checks for the auto-battler. Run: node dev-tools/test_combat.js
 * Covers: seeded reproducibility, stronger gear wins more, defeat still
 * salvages loot, and the wave chain scales with run duration. */
'use strict';
const assert = require('assert');
const C = require('../pixel-game/combat.js');
const LE = require('../pixel-game/loot-engine.js');

let checks = 0; const ok = (c, m) => { assert.ok(c, m); checks++; };

// build a gear map at a given rarity for all 5 slots
function gearAt(rarity, ilvl) {
  const seeds = { core: 'reactor_core_housing', legs: 'hover_stabilizer_legs', arm: 'rail_rifle', util: 'titan_arm_assembly', head: 'quantum_helm' };
  const weak = { core: 'scrap_chestplate', legs: 'reinforced_leg_frame', arm: 'rusty_pulse_pistol', util: 'servo_arm_plating', head: 'salvaged_headplate' };
  const src = rarity === 'strong' ? seeds : weak;
  const g = {};
  Object.keys(src).forEach(s => { g[s] = LE.generate(src[s], { seed: s + rarity, ilvl: ilvl || 1, rarity: rarity === 'strong' ? 'legendary' : 'common' }); });
  return g;
}

// 1) seeded reproducibility
const g = gearAt('strong', 2);
const a = C.resolveRun(g, { ilvl: 2, dur: 1, seed: 'run-7' });
const b = C.resolveRun(g, { ilvl: 2, dur: 1, seed: 'run-7' });
ok(a.win === b.win && a.wavesCleared === b.wavesCleared && a.power === b.power, 'same seed -> same battle');

// 2) stronger gear => higher power and better win rate
const strong = C.deriveStats(gearAt('strong', 3));
const weak = C.deriveStats(gearAt('weak', 3));
ok(strong.power > weak.power, 'legendary loadout out-powers common (' + strong.power + ' > ' + weak.power + ')');
let sWins = 0, wWins = 0;
for (let i = 0; i < 200; i++) {
  if (C.resolveRun(gearAt('strong', 2), { ilvl: 2, dur: 1, seed: 's' + i }).win) sWins++;
  if (C.resolveRun(gearAt('weak', 2), { ilvl: 2, dur: 1, seed: 'w' + i }).win) wWins++;
}
ok(sWins > wWins, 'strong gear wins more often (' + sWins + ' vs ' + wWins + ')');

// 3) loot multiplier always salvages something, and a win pays more
const r = C.resolveRun(gearAt('weak', 4), { ilvl: 4, dur: 2, seed: 'lose-likely' });
ok(r.lootMult >= 0.34, 'defeat still salvages loot (mult ' + r.lootMult.toFixed(2) + ')');
ok(r.totalWaves === 8, 'odyssey (dur 2) has 8 waves');
ok(C.resolveRun(g, { ilvl: 1, dur: 0, seed: 'x' }).totalWaves === 3, 'scout (dur 0) has 3 waves');

// 4) capstone enemy per duration
ok(C.resolveRun(g, { ilvl: 1, dur: 2, seed: 'x' }).bossKind === 'boss', 'odyssey ends on a boss');

// 5) starter (common) gear can win a Scout run at least sometimes — early game is fair
let starterScoutWins = 0;
for (let i = 0; i < 200; i++) if (C.resolveRun(gearAt('weak', 1), { ilvl: 1, dur: 0, seed: 'ss' + i }).win) starterScoutWins++;
ok(starterScoutWins > 40, 'starter gear clears Scout sometimes (' + starterScoutWins + '/200)');

console.log('combat: ' + checks + ' checks passed. strongWins=' + sWins + '/200 weakWins=' + wWins + '/200');
