# ReGenesis — Agent Instructions

## Project context
- Minecraft Java **1.20.1**, **Forge 47.4.10**, **Java 17**.
- This repository is currently **planning-only**. Do not claim that a modpack or any feature runs until it has been tested.
- Read `README.md`, `CODEX_TASK.md` and the relevant `docs/*.md` before changing implementation.
- Work in small, reviewable increments. Keep the scope of each PR tightly focused; do not auto-merge.
- Never modify the user's existing Minecraft Vanilla 26.3 server or its worlds.

## Non-negotiable gameplay principles
- Every required food and crafting progression path must be **vegan**. No required meat, milk, eggs, leather, wool, honey, bones or animal-product farms.
- **No fossil or combustible-fuel energy path** (coal, charcoal, oil, gas or burning biomass). Mechanically renewable wind/water, then solar/electric energy and storage.
- Prefer **recycling, repair, nutrient and water loops** over disposable resources. Recycling must not generate materials/energy without input.
- Animals serve ecological roles (habitat, pollination, seed dispersal and balance), not industrial resource extraction.
- Early progression must have no softlocks: all essential resources, plants and recipes must have repeatable recovery paths.
- Leave complex world regeneration, biome transformation and population simulation out of the bootstrap; they are separate planned features.

## Working method
1. Inspect existing files, dependencies and versions before editing. Verify actual 1.20.1 Forge artifact availability and mod compatibility; do not guess item IDs or APIs.
2. Prefer data packs, KubeJS and mod configurations for recipes/quests. Introduce custom Java/Forge code only for functionality that needs it, with a documented reason.
3. Make changes on a feature branch with a clear PR. Avoid force pushes and destructive file/world operations.
4. Include reproducible commands, pinned dependency versions, and tests/checks for the changed behavior.
5. Run available checks and report what was actually executed. Distinguish **passed**, **failed**, and **not run**. Never infer a successful Minecraft boot from static file generation.
6. Keep `README.md` and `docs/` in sync with actual progress. Mark proposed mechanics as proposals until implemented and verified.

## Immediate priority
Implement the smallest reproducible modpack bootstrap described in `CODEX_TASK.md`: Forge 1.20.1 client + minimal compatible modset, installation guidance, boot evidence and documented blockers. Proceed to early recipes only after verifying that bootstrap.
