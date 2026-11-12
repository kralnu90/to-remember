# 30 × to Remember: handover notes

Upload this file at the start of a new session so Claude can pick up where we left off.

## The project
- Time-loop dungeon crawler. Repo `kralnu90/to-remember`, live at https://kralnugames.com/to-remember/, listed on the hub's WIP page (`/wip/`).
- One file game: `index.html` holds everything (CSS, game, menus). Also `manifest.webmanifest`, `sw.js`, `version.json`, `icons/`.
- Design notes live in Kris's Google Doc "30 Times to Remember – Design Notes".

## Kris's house rules
- Credit Claude in the game ("Ideas, design and testing by Kris. Built with Claude, an AI by Anthropic.").
- Free forever. Never ask players outright for money; Ko-fi is optional.
- Warn before anything costs money or could expose a password or personal detail in the public repo.
- In anything public, never name Kris's son or wife.

## Releasing an update
1. Change `GAME_VERSION` in `index.html`, `BUILD` in the update kit at the bottom of `index.html`, and `version.json`, all to the same new number.
2. Add a changelog entry to `README.md`.
3. Players see a "new version ready" notice. The menu's "Get the latest version" button forces a fresh copy.
4. Only bump `VERSION` in `sw.js` if icons or the manifest change.
5. **Every release, also update the hub** (repo `kralnu90/kralnu90.github.io`, Kris asked for this): add a post to the top of `news.json` (type `update`, game `30 × to Remember`), bump the version fact on the WIP card in `wip/index.html`, and refresh its feature list or `to-remember.jpg` screenshot when they go out of date.

## How the game is built (key systems)
- **Saves:** `localStorage` keys `t2r-meta2` (between loops, `M`), `t2r-run2` (current run, `S`), `t2r-tune` (tuning numbers), `t2r-settings` (`SET`), `t2r-rv-name`.
- **Engine (no DOM):** `startRun`, `chooseDoor`, `startFight`, `act`, `enemyPhase`, `winFight`, `applyReset`. Tuning numbers live in `TUNE`/`CFG`. `window.__sim(n, keys, lvl, gear)` runs balance sims in the console.
- **Classes:** `CLASSES` (hero is the Fixed Point plus 8 companion classes). **Enemies (since 0.6.0):** bestiary catalogue doc "30 × to Remember – Bestiary v1 Catalogue" (Claude doc). `BESTIARY` rows (name, family, era, unlock loop, life/dmg/armour profile vs the Bonewalker, speed, ability) → `CREATURES`/`FOES` (present, future, past); profiles above 1 are halved towards 1 by `soften` because `scaleFoe` already scales with level. `poolFor(era,loop,elite)` picks what's unlocked; `fightLineup` handles chapels (past), packs and weights heavy creatures down. Ranks `RANKS`/`rollRank`/`rankUp`, modifiers `MODS`/`hasMod`. Abilities live in `enemyHit`, `enemyPhase`, `hitFoe` (rise, volatile), `strike` (shroud, reflective, mirror), `tickDots` (poison/burn), `costOf` (fear). `M.wraith` = companion ids a Loop Wraith has killed. Mini-bosses still `BOSSES`.
- **Combat stats (since 0.2.0, Diablo-style, no dice):** life, weapon damage range (`dmgMin`–`dmgMax`) plus `dmgPct` (+`lvlDmg`% per level), armour (`armCut(arm, attackerLvl)` = arm ÷ (arm + `armK` + `armLvl`×level), max 75%), dodge % (max 30), crit chance/damage (base 5% / 150%). `strike(st,a,f,pct)` deals pct% weapon damage; skill percentages live in `act()` and `SKILL_INFO`. Enemies scale life/damage/armour by minutes survived and party level (`scaleFoe`). Old saves are converted by `migrateAll` on load.
- **Skill tree (since 0.5.0):** catalogue doc "30 × to Remember – Skill Tree v1 Catalogue" (Claude doc). Data in `TREE_DEF` + `HYBRIDS` → `TREE` (ids like `chrono_05`, `hy_relic`); owned ids in `M.tree.owned`; `treeFx()`/`TF()` sums effects and every system reads it (hero stats in `calc`, door hints in `fillDoors`/`rollType`, gold/drops/XP, reset effects in `applyReset`). Points = hero level − 1 + loop milestones. UI: `treeSheet()`/`treeSVG()` spider web, `initTree()` handles drag, pinch, wheel; zoom kept in `UI.tz`.
- **Economy (since 0.4.0):** `M.gold` persists (the wizard enchanted the hero's purse). `STORE` items are bought into `M.pack`, unpacked in `startRun` (items, start time, `S.buffs`), then `M.pack` is cleared. `M.store` stock rerolls each loop (`rollStore`). Selling (`sellItem`) only in the frozen window after a cleared run. Crystal sinks: binding at the Cottage (`bindItem`, cost rises with `M.binds`) and the Sanctum (`SANCTUM`, `M.sanctum`, cost = base × (rank+1)^1.5). `ensureEconomy()` fills missing fields on old saves.
- **Healing (since 0.3.0):** `healPower(a,pct)` = pct% of the healer's weapon damage (can crit); `applyHeal` caps at max life and tracks overheal. Cleric Lily gauge lives on the run copy of the member (`lilies`, `lilyUsed`, `blood`): Holy Light grows a Lily, Lily Mend spends one, 3 Lily Mends give a Blood Lily for Misery. Rewind sets `regen`, ticked in `startTurn`.
- **Battle scene:** pixel art drawn in code. `SPR` holds one text sprite per class and enemy shape; `FOE_LOOK` maps each enemy name to a sprite, palette and flags (`big`, `warp`, `float`, `flip`). `palOf(m)` colours a companion from their name colour plus a hash of their id; strangers get faded colours.
- **Dialogue portraits (since 0.6.1):** `PORTRAITS` holds 15 packed 48×48 text portraits (mouth closed + talking rows). **Every line of dialogue should go through `speak(key, label, lines)`**, which draws the portrait box and plays the talk animation. Keys: `hero`, `wizard`, `tavern`, `shopkeeper`, the 8 class keys, `shadow` (any speaking enemy, including a Nemesis), `champion` (Hollow Champion), `rememberer` (Last Rememberer). Class portraits are gender-neutral. Source: `tools/portraits.py` makes the PNGs and `portraits.js`; `tools/pack.py` packs them into the `PORTRAITS` line.
- **Dungeon rooms (since 0.6.4):** `roomView()` shows a `#room` canvas (128×104 art pixels, `RS` canvas pixels each) with door buttons laid over it (`RD_BOX`). `makeRoomArt(room)` paints walls, era floor, doors (shut, open for the way you came, echo), door signs (`RICON`: fight, elite, treasure, shrine, quiet, unknown) and a centrepiece picked from the room name, then lights it with `artPainter().finish()`. It's cached by `roomKey()`. `drawRoom()` animates torches, echo-door shimmer and motes. `artPainter(W,H)` is the shared pixel painter with baked lighting; use it for any new scene.
- **Hi-res sprites (since 0.6.6):** `SPR_HD` holds 2× versions of every `SPR` sprite (classes 20×28, creatures double size), using the same palette letters plus UPPERCASE for a darker shade and `#` for outline. `drawSpr` looks them up through `HD_OF` and draws at half scale, so sizes, positions and hit boxes are unchanged. `BC` is now 6 (the battle canvas is 768×432) so half-cells land on whole pixels. Source: `tools/sprites_hd.py`.
- **Battle animations:** the engine pushes events with `bfx()` (`hit`, `miss`, `ehit`, `emiss`, `heal`, `buff`). `BAT` queues them and `stepBattle()` plays them one by one. The fight summary waits until the queue is empty (`batBusy()`). Settings → Battle speed runs more steps per frame.
- **Backgrounds (redrawn in 0.6.5):** `makeBg(era, name, echo)` paints the battle backdrop with `artPainter` (128×72 art pixels, `BC` each), with a prop picked from the room name; cached in `BAT.bg` by `bgKey()` (`era|name|e`) through `bgFor()`. `canvas.meta` holds the clock, lamps and flags that `drawBgLife()` animates (clock twitch, twinkling stars, lamp flicker, fireflies, echo mist). Used by `drawBattle` and `drawMenuArt`.
- **Hamlet map (redrawn in 0.6.3):** 240×308 art pixels, `TB` canvas pixels each (not `BC`). `makeTown()` paints the static scene once with baked night lighting (light pools from `light()` calls, banded and dithered); `drawTown()` animates the rift, campfire, river glints, fireflies and the `T_FROZEN` pixels (smoke, fountain spray, sparks, floating apple) that stutter a pixel every few seconds. Places are HTML buttons over the canvas (`T_PLACES`, boxes in art pixels), so they stay tappable and keyboard friendly.
- **One loop:** `battleLoop()` runs every frame and draws whichever canvas is on screen (`#battle`, `#town`, `#menuart`).
- **Menus:** `UI.menu` shows `renderMenu()`. Sheets: `settings`, `howto`, `review`, `newconfirm`, plus the game's own. Test tools (tuning and the sacrifice button) only show when Settings → Test tools is on.
- **Sound:** tiny WebAudio chirps in `SFX`, switched off by `SET.sound`.
- **Reviews:** posted to the same Google Form as Fairway Tales; the version field says "30× to Remember 0.1.0" so they can be told apart.
- **Install and update kits:** the standard Kralnu Games blocks at the bottom of `index.html` (`data-install`, `data-get-latest`).

## Agreed but not built yet (don't re-decide)
- Nemesis and memory return (fully designed in the bestiary doc): the creature that downs a lost companion holds their true name; Nemesis door after the stranger's echo fragments; stranger must be in the party; three strikes (clover) then the Unworthy curse (no talent, forever); wipes = one Nemesis holding several names; no snowballing; boss kills = never fully returned. Nemesis name shows red (`.card.nemesis`, rank `nemesis`).
- Milestone bosses at loops 5/10/15/20 (Forgotten King, Clockwork Sovereign, Maw Beneath, Paradox Regent) and the fate reflections (Hollow Champion = the hero's, Last Rememberer = the wizard's) in the echo levels.
- More crystal sinks: Reforging (reroll a stat or upgrade rarity) and rebuilding the Hamlet (blacksmith, bigger tavern, new services). Respecs already cost crystals.
- Skill tree open questions: companion trees later or not; achievements as a point source; is Glass Cannon too harsh solo.
- Possibly let the battle scene replace the enemy cards.

## Session log
- 10 Nov 2026: pixel battle scene and pixel Hamlet added to the prototype; turned into v0.1.0 with menus, settings, reviews, Ko-fi, install and update; pushed to `to-remember` and added to the hub's new WIP page.
- 11 Nov 2026: v0.2.0 swapped the D&D d20/AC system for Diablo-style stats (always hit, armour as damage cut, crits, dodge, skills as % weapon damage); rebalanced with `__sim` so using skills beats spamming Attack.
- 11 Nov 2026: v0.3.0 Cleric rework (Holy Light, Lily gauge, Lily Mend, Misery), heals scale from the healer, overheal wasted, Rewind became a heal over time. Sims: healer parties no longer dominate; Warrior (Taunt + armour) is now the standout.
- 11 Nov 2026: v0.4.0 gold, General Store, selling in the reset window, binding with crystals, Wizard's Sanctum. A full run earns roughly 300 gold at level 1 (sim).
- 11 Nov 2026: v0.5.0 hero skill tree (spider-web ring, 60 nodes + 6 hybrids), door hints, Market Square capstone shop, Slow and Rewind Turn skills.
- 12 Nov 2026: v0.6.0 bestiary v1 (16 creatures, abilities, Elite/Champion/Dread ranks, 10 modifiers). Village named Bleakthorpe, world Aetherfall.
