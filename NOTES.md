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

## How the game is built (key systems)
- **Saves:** `localStorage` keys `t2r-meta2` (between loops, `M`), `t2r-run2` (current run, `S`), `t2r-tune` (tuning numbers), `t2r-settings` (`SET`), `t2r-rv-name`.
- **Engine (no DOM):** `startRun`, `chooseDoor`, `startFight`, `act`, `enemyPhase`, `winFight`, `applyReset`. Tuning numbers live in `TUNE`/`CFG`. `window.__sim(n, keys, lvl, gear)` runs balance sims in the console.
- **Classes:** `CLASSES` (hero is the Fixed Point plus 8 companion classes). **Enemies:** `FOES`, `ELITES`, `BOSSES`.
- **Combat stats (since 0.2.0, Diablo-style, no dice):** life, weapon damage range (`dmgMin`–`dmgMax`) plus `dmgPct` (+`lvlDmg`% per level), armour (`armCut(arm, attackerLvl)` = arm ÷ (arm + `armK` + `armLvl`×level), max 75%), dodge % (max 30), crit chance/damage (base 5% / 150%). `strike(st,a,f,pct)` deals pct% weapon damage; skill percentages live in `act()` and `SKILL_INFO`. Enemies scale life/damage/armour by minutes survived and party level (`scaleFoe`). Old saves are converted by `migrateAll` on load.
- **Skill tree (since 0.5.0):** catalogue doc "30 × to Remember – Skill Tree v1 Catalogue" (Claude doc). Data in `TREE_DEF` + `HYBRIDS` → `TREE` (ids like `chrono_05`, `hy_relic`); owned ids in `M.tree.owned`; `treeFx()`/`TF()` sums effects and every system reads it (hero stats in `calc`, door hints in `fillDoors`/`rollType`, gold/drops/XP, reset effects in `applyReset`). Points = hero level − 1 + loop milestones. UI: `treeSheet()`/`treeSVG()` spider web, `initTree()` handles drag, pinch, wheel; zoom kept in `UI.tz`.
- **Economy (since 0.4.0):** `M.gold` persists (the wizard enchanted the hero's purse). `STORE` items are bought into `M.pack`, unpacked in `startRun` (items, start time, `S.buffs`), then `M.pack` is cleared. `M.store` stock rerolls each loop (`rollStore`). Selling (`sellItem`) only in the frozen window after a cleared run. Crystal sinks: binding at the Cottage (`bindItem`, cost rises with `M.binds`) and the Sanctum (`SANCTUM`, `M.sanctum`, cost = base × (rank+1)^1.5). `ensureEconomy()` fills missing fields on old saves.
- **Healing (since 0.3.0):** `healPower(a,pct)` = pct% of the healer's weapon damage (can crit); `applyHeal` caps at max life and tracks overheal. Cleric Lily gauge lives on the run copy of the member (`lilies`, `lilyUsed`, `blood`): Holy Light grows a Lily, Lily Mend spends one, 3 Lily Mends give a Blood Lily for Misery. Rewind sets `regen`, ticked in `startTurn`.
- **Battle scene:** pixel art drawn in code. `SPR` holds one text sprite per class and enemy shape; `FOE_LOOK` maps each enemy name to a sprite, palette and flags (`big`, `warp`, `float`, `flip`). `palOf(m)` colours a companion from their name colour plus a hash of their id; strangers get faded colours.
- **Battle animations:** the engine pushes events with `bfx()` (`hit`, `miss`, `ehit`, `emiss`, `heal`, `buff`). `BAT` queues them and `stepBattle()` plays them one by one. The fight summary waits until the queue is empty (`batBusy()`). Settings → Battle speed runs more steps per frame.
- **Backgrounds:** `makeBg(era)` (present night street with clocktower, future overgrown ruin), cached in `BAT.bg`.
- **Hamlet map:** `makeTown()` paints the static map once, `drawTown()` animates the rift, river, windows, smoke, fire and fireflies. Places are HTML buttons over the canvas (`T_PLACES`, boxes in map cells), so they stay tappable and keyboard friendly.
- **One loop:** `battleLoop()` runs every frame and draws whichever canvas is on screen (`#battle`, `#town`, `#menuart`).
- **Menus:** `UI.menu` shows `renderMenu()`. Sheets: `settings`, `howto`, `review`, `newconfirm`, plus the game's own. Test tools (tuning and the sacrifice button) only show when Settings → Test tools is on.
- **Sound:** tiny WebAudio chirps in `SFX`, switched off by `SET.sound`.
- **Reviews:** posted to the same Google Form as Fairway Tales; the version field says "30× to Remember 0.1.0" so they can be told apart.
- **Install and update kits:** the standard Kralnu Games blocks at the bottom of `index.html` (`data-install`, `data-get-latest`).

## Agreed but not built yet (don't re-decide)
- More crystal sinks: Reforging (reroll a stat or upgrade rarity) and rebuilding the Hamlet (blacksmith, bigger tavern, new services). Respecs already cost crystals.
- Skill tree open questions: companion trees later or not; achievements as a point source; is Glass Cannon too harsh solo.
- Possibly let the battle scene replace the enemy cards.

## Session log
- 10 Nov 2026: pixel battle scene and pixel Hamlet added to the prototype; turned into v0.1.0 with menus, settings, reviews, Ko-fi, install and update; pushed to `to-remember` and added to the hub's new WIP page.
- 11 Nov 2026: v0.2.0 swapped the D&D d20/AC system for Diablo-style stats (always hit, armour as damage cut, crits, dodge, skills as % weapon damage); rebalanced with `__sim` so using skills beats spamming Attack.
- 11 Nov 2026: v0.3.0 Cleric rework (Holy Light, Lily gauge, Lily Mend, Misery), heals scale from the healer, overheal wasted, Rewind became a heal over time. Sims: healer parties no longer dominate; Warrior (Taunt + armour) is now the standout.
- 11 Nov 2026: v0.4.0 gold, General Store, selling in the reset window, binding with crystals, Wizard's Sanctum. A full run earns roughly 300 gold at level 1 (sim).
- 11 Nov 2026: v0.5.0 hero skill tree (spider-web ring, 60 nodes + 6 hybrids), door hints, Market Square capstone shop, Slow and Rewind Turn skills.
