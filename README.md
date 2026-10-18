# ReGenesis — Entwicklungsgrundlage v0.4

**Status:** Konzept und technische Spezifikation, **kein installierbares Modpack**. Stand: 2026-10-18.

Ein Minecraft-Java-Modpack über die Wiederherstellung einer toten Welt: SkyFactory-artige Ressourcengewinnung, vegane Landwirtschaft, regenerative Energie, Kreislaufwirtschaft, Terraforming, Wiederansiedlung und Rekonstruktion von Arten.

## Technische Leitplanken

- Minecraft **1.20.1**, Forge **47.4.10 (Recommended)**, Java **17**.
- Vor dem ersten spielbaren Build eine gemeinsame Versionen-/Startprüfung vornehmen.
- Keine Pflichtrezepte mit Fleisch, Milch, Eiern, Leder, Wolle, Honig, Knochenmehl oder tierischen Mobdrops.
- Keine Kohle-, Holzkohle-, Öl- oder Gasverbrennung als Produktions-/Energieweg.
- Jede Grundressource und Pflanzenart muss verlustsicher neu gewonnen werden können.
- Tierpopulationen werden als ökologische Akteure behandelt, nicht als Produktionsinventar.
- Ökologische Stabilität muss über Neustarts persistent sein.

## Dokumente

- [`docs/01-modstack.md`](docs/01-modstack.md) – Kernmods, Versionen, Risiken
- [`docs/02-gameplay.md`](docs/02-gameplay.md) – Spawn, Kapitel I und II, Materialflüsse
- [`docs/03-tests.md`](docs/03-tests.md) – Abnahmekriterien, Progressions- und Ethik-Checks
- [`CODEX_TASK.md`](CODEX_TASK.md) – nächste konkrete Entwicklungsaufgabe

## Technische Grenzen des jetzigen Stands

1. Wasteland Reimagined überschreibt für seinen Wasteland-Welttyp andere Biome; eine dauerhafte dynamische Renaturierung ist dadurch **nicht gelöst**.
2. Das jüngere Addon „KubeJS Ex Deorum“ ist **nicht** für Forge 1.20.1 erhältlich. Ex-Deorum-Rezepte werden daher zunächst mittels des integrierten Datapack-Systems beziehungsweise dokumentierter 1.20.1-APIs angepasst.
3. „Startkiste“, einzigartige Boden-/Wasserproben und regionale Umweltwerte sind vorerst **Spezifikation**, noch keine implementierten Spielmechaniken.
4. Es wurde noch kein gemeinsamer Ingame-Boot-/Crash-/Rezept-Test durchgeführt.

## Öffentliche Quellen

- Forge 1.20.1: https://files.minecraftforge.net/net/minecraftforge/forge/index_1.20.1.html
- Create: https://www.curseforge.com/minecraft/mc-mods/create
- Ex Deorum: https://www.curseforge.com/minecraft/mc-mods/ex-deorum
- Farmer's Delight: https://www.curseforge.com/minecraft/mc-mods/farmers-delight
- Vegan Delight: https://www.curseforge.com/minecraft/mc-mods/vegan-delight
- KubeJS: https://www.curseforge.com/minecraft/mc-mods/kubejs
- FTB Quests: https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge
- Wasteland Reimagined: https://www.curseforge.com/minecraft/mc-mods/wasteland-reimagined
