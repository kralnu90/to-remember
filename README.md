# 30 × to Remember

*Some lives are lived once. Some are remembered forever.*

A time-loop dungeon crawler from Kralnu Games. A wizard's spell went wrong and left the town of Aetherfall stuck in time. You remember every loop. Nobody else does.

## [▶ Play the work in progress](https://kralnugames.com/to-remember/)

- **Every action costs time.** Attacks, spells, heals and doors all take seconds off your clock. Beating enemies earns seconds back.
- **The loop always resets.** Your levels stay. Only soulbound gear you're wearing survives.
- **Turn-based fights** with Diablo-style stats (life, damage, armour, crits, dodge), drawn as pixel art straight from code: one sprite per class, coloured for each character.
- **Fallen companions** are lost at the reset, but some come back as strangers. Follow their Distant Echoes to help them remember.
- **The Hamlet:** hire at the Tavern, pick your party at the Campfire, manage gear at your Cottage, and keep an eye on the Wizard.

Works offline once installed. Saves stay on your device.

This is an early build. Things will change, and saves may reset between versions.

☕ [Support on Ko-fi](https://ko-fi.com/kralnu90) · ✉️ hello@kralnugames.com

## Changelog

### 0.3.0 · 11 November 2026
- Clerics rework, inspired by FFXIV's White Mage: when the party is topped up, healers deal damage
- New Cleric skills from level 1: **Holy Light** (160% damage, grows a Lily) and **Mend**
- **Lily gauge:** each Holy Light grows a Lily (max 3). **Lily Mend** (level 3) heals for just 1s by using a Lily. Three Lily Mends bloom a Blood Lily, which unlocks **Misery** (level 5), a 300% hit on every enemy
- Heals now scale with the healer's own weapon damage and gear, not the target's max life, and they can crit
- Overhealing is wasted, shown in the log and the fight summary
- Rewind wounds is now a heal over 3 rounds

### 0.2.0 · 11 November 2026
- New combat stats: the D&D dice and AC are gone. Attacks always land unless the target dodges, armour cuts the damage you take, and crits hit for extra
- Skills now deal a share of your weapon damage (Time Bolt hits for 280%), so better gear makes every skill stronger
- Skills are worth using: Time Bolt now costs 7s instead of 12s, Firebolt really hits every enemy, Volley and Flurry hit harder
- Some enemies are armoured or quick on their feet, so plain attacks won't cut it
- Skill buttons show what each skill does
- New gear stats: Armour, Crit chance, Crit damage and Dodge. Gear from older saves is converted automatically
- Tuning numbers have been reset to suit the new system

### 0.1.1 · 11 November 2026
- Fixed: the battle scene and Hamlet map could go blank once a returning stranger joined your party, and fight rewards wouldn't appear until you refreshed
- The battle scene now recovers by itself if a drawing error ever happens, so rewards always pop

### 0.1.0 · 10 November 2026
- First public work-in-progress build
- Main menu with continue, new game, how to play, settings, reviews, Ko-fi, install and update
- Settings: battle speed, sound effects, text size and test tools
- Pixel-art battle scene with attack, hit, heal and buff animations
- Pixel-art Hamlet map
- Chiptune sound effects
- Installs to your home screen and tells you when a new version is out

---

Ideas, design and testing by Kris. Built with Claude, an AI by Anthropic.

© 2026 kralnu90. All rights reserved.
