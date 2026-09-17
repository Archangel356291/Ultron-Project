/*
 * Ultron pixel-game — deterministic auto-battler (idle-RPG combat model).
 * Pure, dependency-free, UMD (browser global `Combat` + node require).
 *
 * Turns an equipped loadout (the 5 Expedition slots) into a combat outcome
 * against a scaled chain of enemy archetypes. Seeded, so a run reproduces.
 * No real-time input; this is the low-risk combat model from GAME_MASTER_ROADMAP §7(a).
 *
 * Tests: node dev-tools/test_combat.js
 */
(function (root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.Combat = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hashStr(s) { s = String(s); var h = 2166136261 >>> 0; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rngFrom(seed) { if (seed == null) seed = (Math.random() * 4294967296) >>> 0; if (typeof seed !== 'number') seed = hashStr(seed); return mulberry32(seed >>> 0); }

  // Enemy archetypes (data-driven). base stats scale with the run's ilvl.
  var ENEMIES = [
    { id: 'scrapling', name: 'Scrapling', kind: 'melee', hp: 40, dmg: 6, armor: 2, shield: 0 },
    { id: 'rust_turret', name: 'Rust Turret', kind: 'ranged', hp: 55, dmg: 9, armor: 4, shield: 0 },
    { id: 'skitter', name: 'Skitter Drone', kind: 'fast', hp: 26, dmg: 5, armor: 0, shield: 0 },
    { id: 'bulwark', name: 'Bulwark', kind: 'tank', hp: 140, dmg: 8, armor: 14, shield: 0 },
    { id: 'aegis', name: 'Aegis Unit', kind: 'shielded', hp: 60, dmg: 8, armor: 4, shield: 60 },
    { id: 'phantom', name: 'Phantom', kind: 'stealth', hp: 50, dmg: 14, armor: 2, shield: 0 },
    { id: 'jammer', name: 'Jammer', kind: 'hacker', hp: 45, dmg: 7, armor: 3, shield: 20 },
    { id: 'nano_swarm', name: 'Nano Swarm', kind: 'swarm', hp: 20, dmg: 4, armor: 0, shield: 0 },
    { id: 'warden', name: 'Elite Warden', kind: 'elite', hp: 180, dmg: 16, armor: 10, shield: 40 },
    { id: 'breaker', name: 'Mini-Boss Breaker', kind: 'miniboss', hp: 320, dmg: 22, armor: 14, shield: 60 },
    { id: 'sentinel_prime', name: 'Rogue Sentinel Prime', kind: 'boss', hp: 600, dmg: 30, armor: 20, shield: 120 },
  ];
  var TRASH = ENEMIES.filter(function (e) { return ['melee', 'ranged', 'fast', 'tank', 'shielded', 'stealth', 'hacker', 'swarm'].indexOf(e.kind) >= 0; });
  // dur -> capstone enemy (Scout beatable with starter gear; Odyssey is a boss)
  var CAP = { 0: 'bulwark', 1: 'warden', 2: 'sentinel_prime' };

  // Aggregate the equipped items' stats into combat stats.
  function deriveStats(gear) {
    var s = { hp: 100, shield: 0, dmg: 8, fireRate: 0, armor: 0, crit: 0, critDmg: 50, accuracy: 80, moveSpeed: 0, elemResist: 0 };
    Object.keys(gear || {}).forEach(function (slot) {
      var it = gear[slot]; if (!it || !it.stats) return; var st = it.stats;
      s.hp += st.maxHp || 0; s.shield += st.maxShield || 0; s.dmg += st.dmg || 0;
      s.fireRate += st.fireRate || 0; s.armor += st.armor || 0; s.crit += st.critChance || 0;
      s.critDmg += st.critDmg || 0; s.accuracy += st.accuracy || 0; s.moveSpeed += st.moveSpeed || 0;
      s.elemResist += st.elemResist || 0;
    });
    var critMult = 1 + (Math.min(s.crit, 100) / 100) * (s.critDmg / 100);
    s.dps = s.dmg * (1 + s.fireRate / 100) * critMult * (0.6 + Math.min(s.accuracy, 120) / 200);
    s.ehp = s.hp + s.shield;
    s.dr = Math.min(60, s.armor * 0.5 + s.elemResist * 0.2);  // % damage reduction, capped
    s.power = Math.round(s.dps * 2 + s.ehp * 0.5 + s.armor * 3 + s.moveSpeed);
    return s;
  }

  function scaleEnemy(e, ilvl) {
    var f = 1 + 0.35 * (ilvl - 1);
    return { name: e.name, kind: e.kind, hp: Math.round((e.hp + (e.shield || 0)) * f), dmg: Math.round(e.dmg * f), armor: e.armor };
  }

  // One encounter. Mutates player.ehpCur. Returns a short result.
  function resolveEncounter(p, e, rnd) {
    var php = p.ehpCur, ehp = e.hp;
    var pdps = Math.max(1, p.dps - e.armor * 0.5);
    var edps = Math.max(1, e.dmg * (1 - p.dr / 100));
    var round = 0, cap = 60;
    while (php > 0 && ehp > 0 && round < cap) {
      round++;
      ehp -= pdps * (0.85 + rnd() * 0.3);
      if (ehp <= 0) break;
      php -= edps * (0.85 + rnd() * 0.3);
    }
    p.ehpCur = Math.max(0, php);
    return { win: ehp <= 0 && php > 0, enemy: e.name, kind: e.kind, rounds: round, hpLeft: Math.round(Math.max(0, php)) };
  }

  // Full run: a wave chain scaled to the run's ilvl/duration.
  function resolveRun(gear, opts) {
    opts = opts || {};
    var ilvl = opts.ilvl || 1, dur = opts.dur || 0;
    var rnd = rngFrom(opts.seed);
    var p = deriveStats(gear);
    if (opts.powerMult && opts.powerMult !== 1) { p.dps *= opts.powerMult; p.ehp *= opts.powerMult; p.power = Math.round(p.power * opts.powerMult); }  // skill-tree combat bonus
    p.ehpCur = p.ehp;
    var waveCount = [3, 5, 8][dur] || 3;
    var waves = [], i;
    for (i = 0; i < waveCount - 1; i++) waves.push(scaleEnemy(TRASH[Math.floor(rnd() * TRASH.length)], ilvl));
    var capId = opts.bossMult ? 'sentinel_prime' : (CAP[dur] || 'warden');
    waves.push(scaleEnemy(ENEMIES.filter(function (e) { return e.id === capId; })[0], ilvl));
    if (opts.bossMult && opts.bossMult !== 1) waves.forEach(function (w) { w.hp = Math.round(w.hp * opts.bossMult); w.dmg = Math.round(w.dmg * opts.bossMult); });  // boss challenge: everything hits harder

    var log = [], cleared = 0, win = true;
    for (i = 0; i < waves.length; i++) {
      var r = resolveEncounter(p, waves[i], rnd);
      log.push(r);
      if (r.win) { cleared++; p.ehpCur += p.ehp * 0.12; if (p.ehpCur > p.ehp) p.ehpCur = p.ehp; }  // small regen between wins
      else { win = false; break; }
    }
    var frac = cleared / waves.length;
    var lootMult = win ? 1.5 : Math.max(0.34, frac);  // defeat still salvages something
    return {
      win: win, wavesCleared: cleared, totalWaves: waves.length,
      power: p.power, hpLeft: Math.round(p.ehpCur), ehp: Math.round(p.ehp), dps: Math.round(p.dps),
      lootMult: lootMult, bossKind: waves[waves.length - 1].kind, log: log,
    };
  }

  return {
    ENEMIES: ENEMIES, deriveStats: deriveStats, resolveEncounter: resolveEncounter,
    resolveRun: resolveRun, rngFrom: rngFrom, version: 1,
  };
});
