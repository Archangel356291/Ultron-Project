/*
 * Odin pixel-game — shared color-palette tokens.
 * UMD (browser global `GamePalettes` + node require). Data only, no hard-coded
 * one-off colours in gameplay code. See COLOR_PALETTES.md for the full guide.
 *
 * Groups: environments (biomes), rarity (loot), combat (gameplay HUD/effects),
 * robotSkins (player cosmetics), accessibility (safe alternates + toggles).
 */
(function (root, factory) {
  var api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GamePalettes = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // 12 environment/biome palettes: [bg, a, b, c, d, highlight]
  var environments = {
    ultronCore: { name: 'Odin Core', colors: ['#05060f', '#00e5ff', '#2b6bff', '#7a4dff', '#ffffff', '#4dfff0'], use: 'Odin HQ, reactor rooms, title' },
    neonHacker: { name: 'Neon Hacker', colors: ['#03080a', '#19ff7a', '#b6ff3d', '#00e5ff', '#0c3b3a', '#ffb000'], use: 'Terminals, hack minigames, net' },
    cyberpunkCity: { name: 'Cyberpunk City', colors: ['#160a2e', '#ff2bd0', '#ff5aa0', '#2b8bff', '#00e5ff', '#2a2f3a'], use: 'City streets, markets, rain' },
    industrialScrapyard: { name: 'Industrial Scrapyard', colors: ['#1c1b18', '#e0621f', '#8a8f96', '#0a0a0a', '#ffd21e', '#3d9bff'], use: 'Scrapyards, foundry, salvage' },
    plasmaWasteland: { name: 'Plasma Wasteland', colors: ['#160b2e', '#9a4dff', '#ff2bd0', '#ff5aa0', '#8a8f96', '#ffffff'], use: 'Blasted plasma flats, storms' },
    frozenCircuit: { name: 'Frozen Circuit', colors: ['#071427', '#9be8ff', '#bcd8ff', '#c9ccd2', '#eef6ff', '#7a4dff'], use: 'Cryo labs, frozen ruins' },
    toxicReactor: { name: 'Toxic Reactor', colors: ['#0a1a0d', '#9dff1e', '#33d17a', '#ffd21e', '#40482a', '#e0621f'], use: 'Reactor cores, toxic caves' },
    desertMachineWorld: { name: 'Desert Machine World', colors: ['#e9c98a', '#b5651d', '#c9772e', '#4a3120', '#ffd21e', '#e04a2b'], use: 'Solar deserts, dune machines' },
    alienVoid: { name: 'Alien Void', colors: ['#0b0518', '#4a2bff', '#7a4dff', '#2b6bff', '#00c2b4', '#ffffff'], use: 'Alien ruins, void rifts' },
    underwaterTechRuins: { name: 'Underwater Tech Ruins', colors: ['#03121f', '#0d5b6a', '#00e5ff', '#2fa27a', '#ff7a6a', '#eef6ff'], use: 'Sunken labs, coral tech' },
    stealthGhost: { name: 'Stealth / Ghost Protocol', colors: ['#050608', '#2a2f3a', '#5c6a7a', '#3a7f8a', '#5a4a7a', '#c0392b'], use: 'Stealth missions, night ops' },
    bossDanger: { name: 'Boss / Danger Mode', colors: ['#0a0405', '#7a0f1e', '#ff2b3d', '#ff6a1e', '#ffe9d6', '#b04dff'], use: 'Boss arenas, alarms' },
  };

  // Loot rarity — colour + border + icon shape + label (never colour alone) +
  // colorblind-safe alternate. Hexes match the loot engine tiers.
  var rarity = {
    common: { label: 'Common', color: '#9aa2ae', border: '#6a7079', glow: 'rgba(154,162,174,.35)', shape: '●', cbSafe: '#c9ccd2' },
    uncommon: { label: 'Uncommon', color: '#33d17a', border: '#1e8f52', glow: 'rgba(51,209,122,.40)', shape: '▲', cbSafe: '#7fd4ff' },
    rare: { label: 'Rare', color: '#3d9bff', border: '#2664b0', glow: 'rgba(61,155,255,.45)', shape: '◆', cbSafe: '#5b8dff' },
    epic: { label: 'Epic', color: '#b084f0', border: '#7a4dff', glow: 'rgba(176,132,240,.50)', shape: '⬟', cbSafe: '#c98bff' },
    legendary: { label: 'Legendary', color: '#ff9d3c', border: '#c9741a', glow: 'rgba(255,157,60,.55)', shape: '★', cbSafe: '#ffc400' },
    mythic: { label: 'Mythic', color: '#ff5a7a', border: '#c0304f', glow: 'rgba(255,90,122,.60)', shape: '✦', cbSafe: '#00e5ff' },
  };

  // Combat / gameplay HUD + damage-type colours.
  var combat = {
    health: '#33d17a', shield: '#3d9bff', energy: '#7a4dff', heat: '#ff6a1e', xp: '#b6ff3d',
    currency: '#ffd21e', objective: '#00e5ff', friendly: '#33d17a', neutral: '#c9ccd2', enemy: '#ff4d5e',
    elite: '#ff9d3c', boss: '#ff2b3d', crit: '#ffe066', healing: '#33d17a', shieldGain: '#3d9bff',
    damageTaken: '#ff4d5e', fire: '#ff6a1e', shock: '#ffe066', cryo: '#9be8ff', corruption: '#9a4dff',
    emp: '#00e5ff', lootDrop: '#b6ff3d', interactable: '#00e5ff', warning: '#ffb000', error: '#ff4d5e',
  };

  // 13 player robot cosmetic palettes.
  // Each: primary, secondary, shadow, highlight, glow(LED), eye, damage, effect.
  var robotSkins = {
    ultron: { name: 'Odin Cyan/Violet', primary: '#3a4049', secondary: '#8a8f96', shadow: '#1a1e24', highlight: '#c9ccd2', glow: '#00e5ff', eye: '#ff3b3b', damage: '#7a0f1e', effect: '#7a4dff' },
    hacker: { name: 'Hacker Green', primary: '#12331f', secondary: '#1e8f52', shadow: '#08160d', highlight: '#b6ff3d', glow: '#19ff7a', eye: '#b6ff3d', damage: '#3a1f0a', effect: '#00e5ff' },
    crimson: { name: 'Crimson Assault', primary: '#3a1416', secondary: '#c0392b', shadow: '#1a0708', highlight: '#ff8a7a', glow: '#ff2b3d', eye: '#ffe066', damage: '#4a0a0a', effect: '#ff6a1e' },
    solarGold: { name: 'Solar Gold', primary: '#4a3a12', secondary: '#e0a81f', shadow: '#241c08', highlight: '#ffe9a6', glow: '#ffd21e', eye: '#fff2c0', damage: '#5a3a0a', effect: '#ff9d3c' },
    arctic: { name: 'Arctic Blue', primary: '#1a2b3a', secondary: '#5b8dc9', shadow: '#0a141f', highlight: '#cfe6ff', glow: '#9be8ff', eye: '#eef6ff', damage: '#3a1f2a', effect: '#00e5ff' },
    toxic: { name: 'Toxic Reactor', primary: '#1a2b12', secondary: '#6fae1e', shadow: '#0a1408', highlight: '#c8ff6a', glow: '#9dff1e', eye: '#ffd21e', damage: '#3a2a0a', effect: '#33d17a' },
    industrial: { name: 'Industrial Rust', primary: '#2b2320', secondary: '#b5651d', shadow: '#140f0d', highlight: '#e0a878', glow: '#e0621f', eye: '#ffd21e', damage: '#3a1a0a', effect: '#8a8f96' },
    neonPink: { name: 'Neon Pink', primary: '#2e0f28', secondary: '#ff2bd0', shadow: '#160514', highlight: '#ffb0ec', glow: '#ff5aa0', eye: '#00e5ff', damage: '#3a0a2a', effect: '#7a4dff' },
    royal: { name: 'Royal Purple', primary: '#241a3a', secondary: '#7a4dff', shadow: '#100a1c', highlight: '#c9b6ff', glow: '#9a4dff', eye: '#ffe066', damage: '#2a0a3a', effect: '#00e5ff' },
    chrome: { name: 'White / Chrome', primary: '#c9ccd2', secondary: '#8a8f96', shadow: '#5c6270', highlight: '#ffffff', glow: '#eef6ff', eye: '#2b6bff', damage: '#7a0f1e', effect: '#00e5ff' },
    stealth: { name: 'Black Stealth', primary: '#14171c', secondary: '#2a2f3a', shadow: '#050608', highlight: '#5c6a7a', glow: '#3a7f8a', eye: '#00e5ff', damage: '#3a0a0a', effect: '#5a4a7a' },
    prototype: { name: 'Rainbow / Prototype', primary: '#2a2f3a', secondary: '#00e5ff', shadow: '#12151c', highlight: '#ffffff', glow: '#ff2bd0', eye: '#b6ff3d', damage: '#7a0f1e', effect: '#ffd21e' },
    corrupted: { name: 'Corrupted / Glitch', primary: '#160a2e', secondary: '#9a4dff', shadow: '#080416', highlight: '#ff2bd0', glow: '#00ff9d', eye: '#ff2bd0', damage: '#00e5ff', effect: '#ff2b3d' },
  };

  var accessibility = {
    highContrastUI: { bg: '#000000', panel: '#0a0a0a', text: '#ffffff', accent: '#ffd21e', line: '#ffffff' },
    notes: [
      'Rarity carries a distinct SHAPE and LABEL, never colour alone.',
      'Damage types pair colour with an icon/label in the HUD.',
      'colorblind-safe alternates provided per rarity (cbSafe).',
      'reducedGlow/reducedFlash: drop the glow tokens to 0 alpha, no strobing.',
      'Never encode success/failure as red-vs-green alone; add icon + text.',
    ],
    toggles: ['highContrast', 'colorblindSafe', 'reducedMotion', 'reducedGlow', 'largeText'],
  };

  return {
    environments: environments,
    rarity: rarity,
    combat: combat,
    robotSkins: robotSkins,
    accessibility: accessibility,
    version: 1,
  };
});
