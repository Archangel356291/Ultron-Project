/*
 * Ultron pixel-game — data-driven loot engine.
 * Pure, dependency-free, UMD (browser global `LootEngine` + node require).
 *
 * Design goals (from the owner's spec):
 *  - Base item DEFINITIONS are separate from generated INSTANCES.
 *  - Seeded, reproducible generation (same seed -> same item) for saves/debug.
 *  - Rarity-weighted drops; high tiers genuinely rare.
 *  - Every instance carries: id, name, type, slot, rarity, tier, description,
 *    baseStats, rolledStats, effects, value, sellPrice, dropWeight, upgradeCompat.
 *  - validate() rejects impossible combinations.
 *
 * To ADD content: append to BASES / AFFIXES; no gameplay code changes needed.
 * See LOOT_SYSTEM.md for the full guide.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LootEngine = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- seeded RNG (mulberry32) ----------
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hashStr(s) {
    s = String(s); var h = 2166136261 >>> 0;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function rngFrom(seed) {
    if (seed == null) seed = (Math.random() * 4294967296) >>> 0;
    if (typeof seed !== 'number') seed = hashStr(seed);
    return mulberry32(seed >>> 0);
  }
  function ri(rnd, lo, hi) { return lo + Math.floor(rnd() * (hi - lo + 1)); }
  function pick(rnd, arr) { return arr[Math.floor(rnd() * arr.length)]; }

  // ---------- rarity tiers ----------
  // shape + colorblind (cb) colour satisfy "never rely on colour alone".
  var TIERS = [
    { key: 'common', tier: 1, label: 'Common', color: '#9aa2ae', cb: '#c9ccd2', shape: '●', rolls: [0, 1], weight: 6900, value: 1.0, unique: false },
    { key: 'uncommon', tier: 2, label: 'Uncommon', color: '#33d17a', cb: '#7fd4ff', shape: '▲', rolls: [1, 1], weight: 2000, value: 2.2, unique: false },
    { key: 'rare', tier: 3, label: 'Rare', color: '#3d9bff', cb: '#5b8dff', shape: '◆', rolls: [1, 2], weight: 700, value: 5.0, unique: false },
    { key: 'epic', tier: 4, label: 'Epic', color: '#b084f0', cb: '#c98bff', shape: '⬟', rolls: [2, 3], weight: 250, value: 12.0, unique: false },
    { key: 'legendary', tier: 5, label: 'Legendary', color: '#ff9d3c', cb: '#ffc400', shape: '★', rolls: [3, 4], weight: 45, value: 30.0, unique: true },
    { key: 'mythic', tier: 6, label: 'Mythic', color: '#ff5a7a', cb: '#00e5ff', shape: '✦', rolls: [4, 5], weight: 5, value: 80.0, unique: true },
  ];
  var TIER_BY_KEY = {}; TIERS.forEach(function (t) { TIER_BY_KEY[t.key] = t; });
  function tierIndex(key) { for (var i = 0; i < TIERS.length; i++) if (TIERS[i].key === key) return i; return -1; }

  // ---------- stat pool (21 stats) ----------
  var STATS = {
    dmg: { l: 'Damage', u: '' }, fireRate: { l: 'Fire Rate', u: '%' }, critChance: { l: 'Crit Chance', u: '%' },
    critDmg: { l: 'Crit Dmg', u: '%' }, reload: { l: 'Reload Speed', u: '%' }, capacity: { l: 'Capacity', u: '' },
    accuracy: { l: 'Accuracy', u: '%' }, heatCap: { l: 'Heat Cap', u: '' }, cooldown: { l: 'Cooldown Red.', u: '%' },
    armor: { l: 'Armor', u: '' }, maxHp: { l: 'Max Health', u: '' }, maxShield: { l: 'Max Shield', u: '' },
    shieldRegen: { l: 'Shield Regen', u: '%' }, energyRegen: { l: 'Energy Regen', u: '%' }, moveSpeed: { l: 'Move Speed', u: '%' },
    dashRegen: { l: 'Dash Regen', u: '%' }, lootFind: { l: 'Loot Find', u: '%' }, repairPower: { l: 'Repair Power', u: '%' },
    elemResist: { l: 'Elem. Resist', u: '%' }, armorPen: { l: 'Armor Pen', u: '%' }, statusChance: { l: 'Status Chance', u: '%' },
  };
  var STAT_ROLL = {
    dmg: [4, 14], capacity: [1, 6], armor: [3, 12], maxHp: [10, 45], maxShield: [8, 40], heatCap: [4, 16],
    fireRate: [3, 12], critChance: [2, 9], critDmg: [6, 22], reload: [4, 15], accuracy: [3, 12], cooldown: [3, 12],
    shieldRegen: [4, 15], energyRegen: [4, 15], moveSpeed: [3, 10], dashRegen: [4, 14], lootFind: [2, 8],
    repairPower: [5, 20], elemResist: [4, 16], armorPen: [3, 12], statusChance: [3, 12],
  };
  var ROLL_POOL = {
    weapon: ['dmg', 'fireRate', 'critChance', 'critDmg', 'reload', 'capacity', 'accuracy', 'heatCap', 'cooldown', 'armorPen', 'statusChance'],
    armor: ['armor', 'maxHp', 'maxShield', 'elemResist', 'moveSpeed', 'dashRegen', 'shieldRegen', 'accuracy', 'repairPower'],
    shield: ['maxShield', 'shieldRegen', 'elemResist', 'cooldown', 'armor', 'statusChance'],
    throwable: ['dmg', 'statusChance', 'cooldown', 'armorPen'],
    artifact: ['critDmg', 'energyRegen', 'lootFind', 'cooldown', 'elemResist'],
    consumable: ['repairPower', 'cooldown'],
    ammo: ['capacity', 'armorPen', 'statusChance'],
  };

  // ---------- affixes (reusable, name-building) ----------
  var AFFIXES = {
    prefix: [
      { id: 'reinforced', n: 'Reinforced', stat: 'armor', mult: 0.15 },
      { id: 'overclocked', n: 'Overclocked', stat: 'fireRate', mult: 0.15 },
      { id: 'precise', n: 'Precise', stat: 'critChance', mult: 0.15 },
      { id: 'charged', n: 'Charged', stat: 'energyRegen', mult: 0.15 },
      { id: 'swift', n: 'Swift', stat: 'moveSpeed', mult: 0.15 },
      { id: 'fortified', n: 'Fortified', stat: 'maxHp', mult: 0.15 },
      { id: 'regenerative', n: 'Regenerative', stat: 'shieldRegen', mult: 0.15 },
      { id: 'efficient', n: 'Efficient', stat: 'cooldown', mult: 0.15 },
      { id: 'scavenger', n: 'Scavenger', stat: 'lootFind', mult: 0.20 },
      { id: 'piercing', n: 'Piercing', stat: 'armorPen', mult: 0.18 },
    ],
    suffix: [
      { id: 'incendiary', n: 'of Cinders', effect: 'Applies stacking burn damage', elem: 'fire' },
      { id: 'cryogenic', n: 'of Frost', effect: 'Chance to freeze on hit', elem: 'cryo' },
      { id: 'unstable', n: 'of Instability', effect: 'Shock arcs: +damage, −10% accuracy', elem: 'shock', tradeoff: { accuracy: -0.10 } },
      { id: 'prototype', n: 'of the Prototype', effect: '+1 mod slot, volatile rolls' },
      { id: 'ancient', n: 'of the Ancients', effect: 'Elemental-resist aura', elem: 'corruption' },
      { id: 'corrupted', n: 'of Corruption', effect: 'Lifesteal, drains own shield', tradeoff: { shieldRegen: -0.15 } },
    ],
  };

  // ---------- base item catalog (DEFINITIONS) ----------
  // t: type, s: equip zone, rar: [minTierKey,maxTierKey], base: flat base stats,
  // el: element (weapons), dsc: description, dm: drop-weight modifier.
  var W = function (id, name, rar, base, el, dsc) { return { id: id, name: name, t: 'weapon', s: 'arm', rar: rar, base: base, el: el || 'kinetic', dsc: dsc || '' }; };
  var A = function (id, name, zone, rar, base, dsc) { return { id: id, name: name, t: 'armor', s: zone, rar: rar, base: base, dsc: dsc || '' }; };
  var S = function (id, name, rar, base, dsc) { return { id: id, name: name, t: 'shield', s: 'util', rar: rar, base: base, dsc: dsc || '' }; };
  var T = function (id, name, rar, base, dsc) { return { id: id, name: name, t: 'throwable', s: null, rar: rar, base: base, dsc: dsc || '' }; };
  var R = function (id, name, rar, base, dsc) { return { id: id, name: name, t: 'artifact', s: 'artifact', rar: rar, base: base, dsc: dsc || '' }; };
  var C = function (id, name, rar, dsc, effect) { return { id: id, name: name, t: 'consumable', s: null, rar: rar, base: {}, dsc: dsc || '', special: effect }; };
  var M = function (id, name, rar, weapons, dsc) { return { id: id, name: name, t: 'ammo', s: null, rar: rar, base: {}, weapons: weapons, dsc: dsc || '' }; };

  var BASES = [
    // weapons
    W('rusty_pulse_pistol', 'Rusty Pulse Pistol', ['common', 'uncommon'], { dmg: 8, fireRate: 6 }, 'kinetic', 'A dented sidearm that still fires.'),
    W('arc_blaster', 'Arc Blaster', ['uncommon', 'rare'], { dmg: 14, fireRate: 8 }, 'shock', 'Spits crackling arcs of charge.'),
    W('ion_revolver', 'Ion Revolver', ['rare', 'epic'], { dmg: 22, critChance: 6 }, 'shock', 'Six chambers of ionized death.'),
    W('scrap_shotgun', 'Scrap Shotgun', ['common', 'rare'], { dmg: 26, accuracy: -4 }, 'kinetic', 'Fires whatever it can scavenge.'),
    W('plasma_scattergun', 'Plasma Scattergun', ['rare', 'legendary'], { dmg: 34, heatCap: 8 }, 'fire', 'A spread of molten plasma.'),
    W('bolt_rifle', 'Bolt Rifle', ['uncommon', 'rare'], { dmg: 20, accuracy: 6 }, 'kinetic', 'Reliable mid-range workhorse.'),
    W('laser_carbine', 'Laser Carbine', ['rare', 'epic'], { dmg: 24, fireRate: 10 }, 'fire', 'Continuous coherent beam.'),
    W('rail_rifle', 'Rail Rifle', ['epic', 'legendary'], { dmg: 60, armorPen: 10 }, 'kinetic', 'Magnetically slings a slug through walls.'),
    W('micro_missile_pod', 'Micro Missile Pod', ['rare', 'epic'], { dmg: 30, statusChance: 6 }, 'fire', 'Volley of homing micro-rockets.'),
    W('plasma_mortar', 'Plasma Mortar', ['epic', 'mythic'], { dmg: 72, heatCap: 12 }, 'fire', 'Lobbed plasma that erupts on impact.'),
    W('emp_projector', 'EMP Projector', ['uncommon', 'legendary'], { dmg: 10, statusChance: 14 }, 'emp', 'Shreds shields and stuns machines.'),
    W('cryo_beam', 'Cryo Beam', ['rare', 'legendary'], { dmg: 18, statusChance: 12 }, 'cryo', 'A freezing lance of coolant.'),
    W('nano_swarm_emitter', 'Nano Swarm Emitter', ['epic', 'mythic'], { dmg: 40, statusChance: 16 }, 'corruption', 'Releases a devouring nanite cloud.'),
    W('shock_baton', 'Shock Baton', ['common', 'rare'], { dmg: 16, critChance: 5 }, 'shock', 'Close-range electric jolt.'),
    W('mono_blade', 'Mono Blade', ['rare', 'legendary'], { dmg: 44, critDmg: 12 }, 'kinetic', 'A monomolecular edge that ignores plating.'),
    W('gravity_hammer', 'Gravity Hammer', ['epic', 'mythic'], { dmg: 80, armorPen: 8 }, 'kinetic', 'Slams a localized gravity well.'),
    W('hacker_spike', 'Hacker Spike', ['rare', 'mythic'], { dmg: 12, statusChance: 18 }, 'emp', 'Jacks in and turns foes against each other.'),
    // armor (zones map to equip slots: head/core/util/legs)
    A('salvaged_headplate', 'Salvaged Headplate', 'head', ['common', 'uncommon'], { armor: 6, maxHp: 12 }, 'Bolted-on scrap protection.'),
    A('scout_visor', 'Scout Visor', 'head', ['uncommon', 'rare'], { accuracy: 8, moveSpeed: 4 }, 'Widens sensor field, trims weight.'),
    A('tactical_sensor_crown', 'Tactical Sensor Crown', 'head', ['rare', 'epic'], { accuracy: 12, critChance: 6 }, 'Target-locking sensor ring.'),
    A('quantum_helm', 'Quantum Helm', 'head', ['legendary', 'mythic'], { accuracy: 16, energyRegen: 10, maxShield: 20 }, 'Reads a half-second into the future.'),
    A('scrap_chestplate', 'Scrap Chestplate', 'core', ['common', 'rare'], { armor: 10, maxHp: 20 }, 'Heavy, ugly, effective.'),
    A('reactive_torso_shell', 'Reactive Torso Shell', 'core', ['rare', 'legendary'], { armor: 16, maxHp: 30, elemResist: 8 }, 'Plating that hardens on impact.'),
    A('reactor_core_housing', 'Reactor Core Housing', 'core', ['epic', 'mythic'], { maxHp: 40, energyRegen: 14, maxShield: 30 }, 'Houses an overclocked reactor.'),
    A('servo_arm_plating', 'Servo Arm Plating', 'util', ['common', 'rare'], { armor: 8, reload: 6 }, 'Guards the weapon servos.'),
    A('precision_arm_rig', 'Precision Arm Rig', 'util', ['rare', 'epic'], { accuracy: 10, critChance: 6, reload: 8 }, 'Stabilized precision actuators.'),
    A('titan_arm_assembly', 'Titan Arm Assembly', 'util', ['legendary', 'mythic'], { armor: 20, dmg: 12, maxHp: 25 }, 'Heavy-weapon arms of a titan.'),
    A('reinforced_leg_frame', 'Reinforced Leg Frame', 'legs', ['common', 'rare'], { armor: 8, maxHp: 16 }, 'Sturdy load-bearing struts.'),
    A('sprint_servo_legs', 'Sprint Servo Legs', 'legs', ['rare', 'epic'], { moveSpeed: 10, dashRegen: 10 }, 'Built for speed and dashes.'),
    A('hover_stabilizer_legs', 'Hover Stabilizer Legs', 'legs', ['legendary', 'mythic'], { moveSpeed: 14, dashRegen: 16, elemResist: 8 }, 'Floats above the hazards below.'),
    A('magnetic_boots', 'Magnetic Boots', 'legs', ['uncommon', 'epic'], { moveSpeed: 6, armor: 6 }, 'Locks to any surface.'),
    A('adaptive_cloak_shell', 'Adaptive Cloak Shell', 'core', ['epic', 'mythic'], { moveSpeed: 8, elemResist: 12, maxShield: 20 }, 'Bends light and radar around you.'),
    // shields
    S('basic_capacitor_shield', 'Basic Capacitor Shield', ['common', 'uncommon'], { maxShield: 30, shieldRegen: 6 }, 'A starter energy buffer.'),
    S('kinetic_barrier', 'Kinetic Barrier', ['uncommon', 'rare'], { maxShield: 45, armor: 6 }, 'Blunts physical impacts.'),
    S('arc_shield', 'Arc Shield', ['rare', 'epic'], { maxShield: 55, statusChance: 8 }, 'Retaliates with shock on break.'),
    S('thermal_deflector', 'Thermal Deflector', ['rare', 'legendary'], { maxShield: 60, elemResist: 12 }, 'Scatters heat and fire.'),
    S('reflective_prism_shield', 'Reflective Prism Shield', ['epic', 'legendary'], { maxShield: 70, shieldRegen: 10 }, 'Chance to reflect projectiles.'),
    S('void_phase_shield', 'Void Phase Shield', ['legendary', 'mythic'], { maxShield: 90, shieldRegen: 16, elemResist: 10 }, 'Phases briefly on break.'),
    S('drone_shield_generator', 'Drone Shield Generator', ['epic', 'mythic'], { maxShield: 75, shieldRegen: 14 }, 'A companion drone projects the field.'),
    // throwables
    T('scrap_grenade', 'Scrap Grenade', ['common', 'uncommon'], { dmg: 20 }, 'Cheap shrapnel burst.'),
    T('shock_grenade', 'Shock Grenade', ['uncommon', 'rare'], { dmg: 16, statusChance: 12 }, 'Stuns and chains between foes.'),
    T('emp_grenade', 'EMP Grenade', ['rare', 'epic'], { dmg: 8, statusChance: 20 }, 'Drops shields in a radius.'),
    T('cryo_canister', 'Cryo Canister', ['rare', 'epic'], { dmg: 12, statusChance: 16 }, 'Freezes a wide area.'),
    T('plasma_mine', 'Plasma Mine', ['rare', 'legendary'], { dmg: 40 }, 'Proximity-triggered plasma blast.'),
    T('nano_repair_beacon', 'Nano Repair Beacon', ['uncommon', 'epic'], { repairPower: 20 }, 'Heals allies in its field.'),
    T('decoy_hologram', 'Decoy Hologram', ['rare', 'legendary'], {}, 'A hologram that draws enemy fire.'),
    T('gravity_orb', 'Gravity Orb', ['epic', 'mythic'], { dmg: 24 }, 'Pulls enemies into a singularity.'),
    T('blackout_pulse', 'Blackout Pulse', ['legendary', 'mythic'], { statusChance: 26 }, 'Blinds and disables all nearby machines.'),
    // artifacts (fixed passives, may roll a stat or two)
    R('corrupted_data_chip', 'Corrupted Data Chip', ['rare', 'rare'], { lootFind: 8 }, 'Loot find up; occasional glitchy readouts.'),
    R('overclocked_cpu', 'Overclocked CPU', ['epic', 'epic'], { cooldown: 12, energyRegen: 10 }, 'Faster abilities, runs hot.'),
    R('ancient_reactor_fragment', 'Ancient Reactor Fragment', ['epic', 'epic'], { energyRegen: 16 }, 'Endless trickle of ancient power.'),
    R('ghost_protocol', 'Ghost Protocol', ['legendary', 'legendary'], { moveSpeed: 10 }, 'Brief cloak after a dodge.'),
    R('titan_servo_core', 'Titan Servo Core', ['legendary', 'legendary'], { maxHp: 40, dmg: 10 }, 'Melee hits stagger and knock back.'),
    R('quantum_memory_shard', 'Quantum Memory Shard', ['legendary', 'legendary'], { critDmg: 20 }, 'Stores one loadout swap mid-run.'),
    R('singularity_battery', 'Singularity Battery', ['mythic', 'mythic'], { energyRegen: 24 }, 'Abilities cost half energy.'),
    R('ultron_prime_core', 'Ultron Prime Core', ['mythic', 'mythic'], { dmg: 20, maxShield: 30 }, 'Summons a squad of loyal drones.'),
    R('living_circuit', 'Living Circuit', ['mythic', 'mythic'], { repairPower: 25 }, 'Slowly regrows destroyed parts.'),
    R('chrono_relay', 'Chrono Relay', ['mythic', 'mythic'], { cooldown: 20 }, 'Rewinds 2s once per encounter.'),
    // consumables (fixed effects)
    C('small_repair_kit', 'Small Repair Kit', ['common', 'common'], 'Restore 25% health.', { hp: 0.25 }),
    C('standard_repair_kit', 'Standard Repair Kit', ['uncommon', 'uncommon'], 'Restore 50% health.', { hp: 0.50 }),
    C('advanced_nano_repair', 'Advanced Nano Repair', ['rare', 'rare'], 'Restore 50% health over 5s, cleanse burn.', { hp: 0.50, cleanse: 'fire' }),
    C('emergency_core_repair', 'Emergency Core Repair', ['epic', 'epic'], 'Full heal, brief invulnerability.', { hp: 1.0, iframes: 2 }),
    C('shield_cell', 'Shield Cell', ['common', 'common'], 'Restore 40% shield.', { shield: 0.40 }),
    C('shield_battery', 'Shield Battery', ['uncommon', 'uncommon'], 'Restore 80% shield.', { shield: 0.80 }),
    C('overcharge_battery', 'Overcharge Battery', ['rare', 'rare'], 'Overcharge shield +25% for 15s.', { shield: 1.0, over: 0.25 }),
    C('phase_battery', 'Phase Battery', ['epic', 'epic'], 'Full shield + phase through the next hit.', { shield: 1.0, phase: 1 }),
    C('coolant_canister', 'Coolant Canister', ['uncommon', 'uncommon'], 'Instantly vent heat.', { heat: 1.0 }),
    C('power_surge_capsule', 'Power Surge Capsule', ['rare', 'rare'], '+30% fire rate for 12s.', { buff: 'fireRate', amt: 0.30, dur: 12 }),
    C('speed_servo_injector', 'Speed Servo Injector', ['rare', 'rare'], '+25% move speed for 12s.', { buff: 'moveSpeed', amt: 0.25, dur: 12 }),
    C('damage_amplifier', 'Damage Amplifier', ['epic', 'epic'], '+40% damage for 10s.', { buff: 'dmg', amt: 0.40, dur: 10 }),
    C('cloaking_module_charge', 'Cloaking Module Charge', ['epic', 'epic'], 'Cloak for 8s or until you attack.', { buff: 'cloak', dur: 8 }),
    C('revival_spark', 'Revival Spark', ['legendary', 'legendary'], 'Auto-revive once at 40% health.', { revive: 0.40 }),
    C('core_stabilizer', 'Core Stabilizer', ['legendary', 'legendary'], 'Immune to status effects for 15s.', { immune: 'status', dur: 15 }),
    // ammo / resources
    M('scrap_cells', 'Scrap Cells', ['common', 'uncommon'], ['kinetic'], 'Feeds ballistic weapons.'),
    M('energy_cells', 'Energy Cells', ['common', 'uncommon'], ['shock', 'fire'], 'Charges energy weapons.'),
    M('rail_slugs', 'Rail Slugs', ['uncommon', 'rare'], ['kinetic'], 'Dense slugs for rail weapons.'),
    M('plasma_cartridges', 'Plasma Cartridges', ['uncommon', 'rare'], ['fire'], 'Superheated plasma charges.'),
    M('rocket_capsules', 'Rocket Capsules', ['rare', 'epic'], ['fire'], 'Warheads for missile pods.'),
    M('emp_charges', 'EMP Charges', ['rare', 'epic'], ['emp'], 'Disruptor charges.'),
    M('cryo_fuel', 'Cryo Fuel', ['uncommon', 'rare'], ['cryo'], 'Coolant for cryo weapons.'),
    M('nano_gel', 'Nano Gel', ['rare', 'epic'], ['corruption'], 'Feeds nanite swarms.'),
    M('universal_energy', 'Universal Energy', ['epic', 'legendary'], ['kinetic', 'shock', 'fire', 'cryo', 'emp', 'corruption'], 'Powers any weapon.'),
  ];
  var BASE_BY_ID = {}; BASES.forEach(function (b) { BASE_BY_ID[b.id] = b; });

  // ---- how base zones map to the game's 5 equip slots (null = carry-only) ----
  var ZONE_TO_SLOT = { arm: 'arm', head: 'head', core: 'core', util: 'util', legs: 'legs', feet: 'legs' };

  // ---------- generation ----------
  function tierWeightInRange(minKey, maxKey) {
    var lo = tierIndex(minKey), hi = tierIndex(maxKey), out = [];
    for (var i = lo; i <= hi; i++) out.push(TIERS[i]);
    return out;
  }
  function rollRarity(rnd, base) {
    var pool = tierWeightInRange(base.rar[0], base.rar[1]);
    var total = 0, i; for (i = 0; i < pool.length; i++) total += pool[i].weight;
    var r = rnd() * total;
    for (i = 0; i < pool.length; i++) { r -= pool[i].weight; if (r <= 0) return pool[i]; }
    return pool[pool.length - 1];
  }
  function scaleFlat(v, ilvl, tierN) { return Math.max(1, Math.round(v * (1 + 0.25 * (ilvl - 1)) * (1 + 0.10 * (tierN - 1)))); }

  // generate(baseId, opts): opts = { seed, ilvl, rarity(key) }
  function generate(baseId, opts) {
    opts = opts || {};
    var base = BASE_BY_ID[baseId];
    if (!base) throw new Error('unknown base: ' + baseId);
    var ilvl = opts.ilvl || 1;
    var seed = opts.seed != null ? opts.seed : (baseId + ':' + Date.now() + ':' + Math.random());
    var rnd = rngFrom(seed);
    var tier = opts.rarity ? TIER_BY_KEY[opts.rarity] : rollRarity(rnd, base);
    if (!tier) tier = TIER_BY_KEY[base.rar[0]];

    // base stats scaled
    var baseStats = {}, k;
    for (k in base.base) if (base.base[k]) baseStats[k] = scaleFlat(base.base[k], ilvl, tier.tier);

    // rolled stats: N distinct stats from the type's pool (N from tier.rolls)
    var pool = (ROLL_POOL[base.t] || []).slice();
    var nRolls = ri(rnd, tier.rolls[0], tier.rolls[1]);
    var rolled = [], used = {};
    for (var j = 0; j < nRolls && pool.length; j++) {
      var idx = Math.floor(rnd() * pool.length), sk = pool.splice(idx, 1)[0];
      if (used[sk]) continue; used[sk] = 1;
      var rr = STAT_ROLL[sk] || [3, 10];
      var val = scaleFlat(ri(rnd, rr[0], rr[1]), ilvl, tier.tier);
      rolled.push({ k: sk, label: STATS[sk] ? STATS[sk].l : sk, value: val, unit: STATS[sk] ? STATS[sk].u : '' });
    }

    // affixes -> name; rare+ get a prefix, legendary+ get a suffix effect
    var ti = tier.tier, name = base.name, effects = [], prefix = null, suffix = null;
    if (base.dsc) effects.push(base.dsc);
    if (base.special) effects.push(base.dsc || 'Consumable');
    if (ti >= 3) { prefix = pick(rnd, AFFIXES.prefix); name = prefix.n + ' ' + name; }
    if (ti >= 5 || (base.t === 'weapon' && ti >= 4)) { suffix = pick(rnd, AFFIXES.suffix); name = name + ' ' + suffix.n; effects.push(suffix.effect); }
    if (tier.unique) effects.push(tier.tier >= 6 ? 'Build-defining effect' : 'Unique effect');

    // apply prefix boost to its stat if present in the item
    if (prefix) {
      var found = rolled.filter(function (s) { return s.k === prefix.stat; })[0];
      if (found) found.value = Math.round(found.value * (1 + prefix.mult));
      else if (baseStats[prefix.stat] != null) baseStats[prefix.stat] = Math.round(baseStats[prefix.stat] * (1 + prefix.mult));
      else { var rr2 = STAT_ROLL[prefix.stat] || [3, 8]; rolled.push({ k: prefix.stat, label: STATS[prefix.stat] ? STATS[prefix.stat].l : prefix.stat, value: scaleFlat(ri(rnd, rr2[0], rr2[1]), ilvl, ti), unit: STATS[prefix.stat] ? STATS[prefix.stat].u : '' }); }
    }

    var value = Math.round(10 * tier.value * (1 + 0.15 * (ilvl - 1)) * (1 + rolled.length * 0.12));
    var idNum = hashStr(String(seed) + baseId + tier.key + nRolls).toString(36);

    var item = {
      id: 'it_' + idNum,
      base: baseId,
      name: name,
      fullName: tier.label + ' ' + name,
      type: base.t,
      zone: base.s,
      slot: base.s ? (ZONE_TO_SLOT[base.s] || null) : null,
      rarity: tier.key,
      tier: tier.tier,
      tierLabel: tier.label,
      color: tier.color,
      colorblind: tier.cb,
      shape: tier.shape,
      description: base.dsc,
      element: base.el || null,
      baseStats: baseStats,
      rolledStats: rolled,
      effects: effects,
      affixes: { prefix: prefix ? prefix.id : null, suffix: suffix ? suffix.id : null },
      value: value,
      sellPrice: Math.max(1, Math.floor(value * 0.25)),
      dropWeight: tier.weight,
      upgradeCompat: base.s ? [base.s, base.t] : [base.t],
      seed: String(seed),
      ilvl: ilvl,
      // convenience for the existing UI:
      stats: (function () { var m = {}, kk; for (kk in baseStats) m[kk] = baseStats[kk]; rolled.forEach(function (s) { m[s.k] = (m[s.k] || 0) + s.value; }); return m; })(),
      mods: effects.slice(),
    };
    return item;
  }

  // Roll a GLOBAL rarity by tier weight first (so the common->mythic curve
  // holds no matter how the catalog is composed), then pick a base that can
  // actually produce that rarity. This is what keeps high tiers genuinely rare.
  function rollDrop(opts) {
    opts = opts || {};
    var seed = opts.seed != null ? opts.seed : ('drop:' + Date.now() + ':' + Math.random());
    var rnd = rngFrom(seed);
    var candidates = opts.types ? BASES.filter(function (b) { return opts.types.indexOf(b.t) >= 0; }) : BASES;
    if (opts.slots) candidates = candidates.filter(function (b) { return b.s && opts.slots.indexOf(ZONE_TO_SLOT[b.s]) >= 0; });
    if (!candidates.length) candidates = BASES;
    // which tiers can any candidate produce?
    var canProduce = TIERS.filter(function (t) {
      var ti = t.tier - 1;
      return candidates.some(function (b) { return ti >= tierIndex(b.rar[0]) && ti <= tierIndex(b.rar[1]); });
    });
    var total = 0, i; for (i = 0; i < canProduce.length; i++) total += canProduce[i].weight;
    var r = rnd() * total, tier = canProduce[0];
    for (i = 0; i < canProduce.length; i++) { r -= canProduce[i].weight; if (r <= 0) { tier = canProduce[i]; break; } }
    var ti = tier.tier - 1;
    var pool = candidates.filter(function (b) { return ti >= tierIndex(b.rar[0]) && ti <= tierIndex(b.rar[1]); });
    var base = pick(rnd, pool.length ? pool : candidates);
    return generate(base.id, { seed: String(seed) + ':' + base.id, ilvl: opts.ilvl || 1, rarity: tier.key });
  }

  // ---------- validation ----------
  function validate(item) {
    var errors = [];
    if (!item || typeof item !== 'object') return { ok: false, errors: ['not an object'] };
    if (!item.id) errors.push('missing id');
    if (!BASE_BY_ID[item.base]) errors.push('unknown base ' + item.base);
    var ti = tierIndex(item.rarity);
    if (ti < 0) errors.push('unknown rarity ' + item.rarity);
    var base = BASE_BY_ID[item.base];
    if (base && ti >= 0) {
      var lo = tierIndex(base.rar[0]), hi = tierIndex(base.rar[1]);
      if (ti < lo || ti > hi) errors.push('rarity ' + item.rarity + ' outside base range');
      var t = TIERS[ti];
      if (item.rolledStats.length > t.rolls[1] + 2) errors.push('too many rolled stats');
      var seen = {};
      item.rolledStats.forEach(function (s) {
        if (!STATS[s.k]) errors.push('invalid stat ' + s.k);
        if (seen[s.k]) errors.push('duplicate stat ' + s.k);
        seen[s.k] = 1;
      });
    }
    if (!(item.value > 0)) errors.push('value must be > 0');
    return { ok: errors.length === 0, errors: errors };
  }

  return {
    TIERS: TIERS, STATS: STATS, AFFIXES: AFFIXES, BASES: BASES,
    generate: generate, rollDrop: rollDrop, validate: validate,
    rngFrom: rngFrom, hashStr: hashStr,
    listBases: function () { return BASES.map(function (b) { return { id: b.id, name: b.name, type: b.t }; }); },
    version: 1,
  };
});
