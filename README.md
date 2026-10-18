# ReGenesis — Entwicklungsgrundlage v0.4

**Status:** Phase-A-Bootstrap mit gepinnten Artefakten und lokal erzeugbarem Prism-Archiv. Clientstart mit Java 17, 18 angezeigten Mods und normale Weltgenerierung sind durch den Nutzer bestätigt (2026-10-18). Der Export enthält jetzt den Ex-Deorum-Default für normale Welten. Serverstart nur bis EULA-Sperre getestet; **noch keine nachhaltige Gameplay-Freigabe**. Siehe [Prüfprotokoll](docs/bootstrap-tests.md).

Ein Minecraft-Java-Modpack über die Wiederherstellung einer toten Welt: SkyFactory-artige Ressourcengewinnung, vegane Landwirtschaft, regenerative Energie, Kreislaufwirtschaft, Terraforming, Wiederansiedlung und Rekonstruktion von Arten.

## Technische Leitplanken

- Minecraft **1.20.1**, Forge **47.4.10 (Recommended)**, Java **17**.
- Modartefakte und Forge-Installer sind fixiert; weiterführende Ingame-/Server-Prüfungen bleiben vor einem spielbaren Build erforderlich.
- Keine Pflichtrezepte mit Fleisch, Milch, Eiern, Leder, Wolle, Honig, Knochenmehl oder tierischen Mobdrops.
- Keine Kohle-, Holzkohle-, Öl- oder Gasverbrennung als Produktions-/Energieweg.
- Jede Grundressource und Pflanzenart muss verlustsicher neu gewonnen werden können.
- Tierpopulationen werden als ökologische Akteure behandelt, nicht als Produktionsinventar.
- Ökologische Stabilität muss über Neustarts persistent sein.

## Phase A installieren (Prism Launcher)

Voraussetzungen: Git, **Python 3.11+**, **Java 17**, Prism Launcher (Diagnose mit
11.1.1) und ein legitimes Minecraft-Java-Konto. Die Skripte benötigen keine
Python-Pakete. Befehle im frisch geklonten Repository ausführen:

```sh
git clone https://github.com/almighty-atlas/regenesis.git
cd regenesis
python3 tools/pack.py --check
python3 tools/pack.py
python3 tools/audit_artifacts.py
python3 -m unittest discover -s tests -v
```

1. `tools/pack.py` lädt ausschließlich die 13 Einträge aus
   [`pack/mods.lock.json`](pack/mods.lock.json) direkt von Modrinth/FTB,
   prüft SHA256 und erstellt `.work/regenesis-phase-a.zip`.
   Keine automatischen Versionsupdates. Keine JARs im Git.
2. Prism mit **separatem Datenverzeichnis** starten:
   `prismlauncher --dir /ABSOLUTER/NEUER/PFAD/regenesis-prism`.
   Ersteinrichtung abschließen, Minecraft-Konto selbst hinzufügen.
3. **Instanz hinzufügen → Importieren**: das lokal erzeugte ZIP auswählen.
   Es enthält `mmc-pack.json` für Minecraft 1.20.1 / Forge 47.4.10 und die
   verifizierten Mods sowie `.minecraft/config/exdeorum-common.toml` mit
   `[common]` → `set_void_world_as_default = false`. Dadurch wird Ex Deorums
   Void-/Skyblock-Preset nicht als Standard für neue Welten gesetzt.
   Die Vorlage liegt in [`pack/config/exdeorum-common.toml`](pack/config/exdeorum-common.toml).
   Keine bestehenden Instanzen, Server oder Saves verwenden.
4. **Instanz bearbeiten → Einstellungen → Java**: explizit **Java 17** auswählen
   und testen (auf diesem Host `/usr/lib/jvm/java-17-openjdk/bin/java`).
   Nicht auf die System-JVM verlassen: hier ist der Standard Java 27.
   Der Export setzt 512 MiB Minimum / 4096 MiB Maximum, aber keinen hostabhängigen Java-Pfad.
5. Instanz starten; Prism lädt Minecraft, Forge und Launcher-Libraries nach.
   Nach dem Hauptmenü nur eine **neue Wegwerfwelt** anlegen. `logs/latest.log`,
   gegebenenfalls `crash-reports/`, sowie die genaue Modliste für die Abnahme sichern.
   Clientstart und normale Weltgenerierung wurden vom Nutzer bestätigt;
   separate JEI-/Quest-/Renderingtests und von Codex erfasste Clientlogs fehlen noch.

**CachyOS / Audio:** Bei verzerrtem oder blechernem Sound gegebenenfalls unter
**Instanz bearbeiten → Einstellungen → Workarounds** die Option
**Use system installation of OpenAL** aktivieren und den Client neu starten.
Dies hat den Sound beim Nutzertest korrigiert. Die Einstellung ist hostabhängig
und wird im Export nicht global erzwungen.

Das ZIP ist ein **lokales Installationsprodukt, kein freigegebenes Distributionspaket**.
Insbesondere FTB-/Jade-/Create-Lizenzen vor jeder Weitergabe prüfen; keine JARs
oder generierten ZIPs in GitHub-Releases hochladen. Download-/Lizenzquellen und
Versionen: [Artefaktbericht](docs/artifact-research.md).
Downloads kontaktieren Modrinth CDN, FTB Maven und (durch Prism/Forge) die
Minecraft-/Forge-/Launcher-Dienste. Die Python-Skripte benötigen keine Kontodaten.

Wiederholung: Ein vorhandenes Ausgabe-ZIP wird **nicht** überschrieben.
Mit `--output .work/regenesis-phase-a-2.zip` einen neuen Namen verwenden;
Cache-Dateien werden erneut gehasht. Ein falscher Cachehash führt zum Abbruch,
nicht zum stillen Überschreiben. Bei unterbrochenen Downloads wird keine
unverifizierte JAR als fertiges Cache-Artefakt veröffentlicht.
Bereits erzeugte ZIPs enthalten die neue Konfiguration nicht nachträglich:
ein neues Archiv bauen und als neue Instanz importieren. Der Exporter verändert
keine installierten Instanzen oder Spielstände.

### Optionaler isolierter Serverdiagnoselauf (Linux)

Nach `python3 tools/pack.py`:

```sh
python3 tools/server_smoke.py --java /ABSOLUTER/PFAD/ZU/java17
```

Ohne EULA-Zustimmung: erwarteter Abbruch an `eula=false` (Läufer-Exit **2**).
Nur wenn der Betreiber die [Minecraft-EULA](https://aka.ms/MinecraftEULA)
selbst gelesen hat und akzeptiert, kann er explizit `--accept-eula` ergänzen.
Der Läufer verwendet nur ein **neues** `.work/server-smoke`, bindet
`127.0.0.1:25585`, wartet begrenzt auf `Done` und sendet danach `stop`.
Vorhandene Testordner werden abgelehnt, nicht gelöscht/überschrieben.
Keinen vorhandenen Server verwenden. [Ergebnis und Logs](docs/server-smoke-evidence.md).
Dieser automatisierte Opt-in-Bootpfad bleibt ungetestet.

### Ergebnisübersicht

- **Bestanden:** echte Moddownloads (auch mit leerem Cache), Hash-/Metadatenchecks,
  deterministischer Export, sechs Workflowtests einschließlich des Konfigurationschecks
  im ZIP, Forge-Serverinstallation.
- **Durch Nutzer bestätigt:** Clientstart mit Java 17 und 18 angezeigten Mods;
  normale Weltgenerierung nach Abschalten des Ex-Deorum-Void-Defaults.
- **Blockiert:** vollständiger Serverstart ohne persönliche EULA-Zustimmung.
- **Nicht durchgeführt:** separate JEI-/Quest-/Rendering-/Verbindungstests;
  vegane und fossilfreie Progressionsabnahme.

## Dokumente

- [`docs/01-modstack.md`](docs/01-modstack.md) – Kernmods, Versionen, Risiken
- [`docs/02-gameplay.md`](docs/02-gameplay.md) – Spawn, Kapitel I und II, Materialflüsse
- [`docs/03-tests.md`](docs/03-tests.md) – Abnahmekriterien, Progressions- und Ethik-Checks
- [`CODEX_TASK.md`](CODEX_TASK.md) – nächste konkrete Entwicklungsaufgabe

## Technische Grenzen des jetzigen Stands

1. Wasteland Reimagined überschreibt für seinen Wasteland-Welttyp andere Biome; eine dauerhafte dynamische Renaturierung ist dadurch **nicht gelöst**.
2. Das jüngere Addon „KubeJS Ex Deorum“ ist **nicht** für Forge 1.20.1 erhältlich. Ex-Deorum-Rezepte werden daher zunächst mittels des integrierten Datapack-Systems beziehungsweise dokumentierter 1.20.1-APIs angepasst.
3. „Startkiste“, einzigartige Boden-/Wasserproben und regionale Umweltwerte sind vorerst **Spezifikation**, noch keine implementierten Spielmechaniken.
4. Der erfolgreiche Clientboot und die normale Weltgenerierung beruhen auf dem Nutzerbericht, ohne von Codex erfasste Clientlogs. Ein vollständiger Serverboot ist weiterhin nicht nachgewiesen. Der Server-Pre-EULA-Lauf bestätigt nur den frühen Startpfad; weitere Ingame-/Rezepttests bleiben offen.
5. Phase A verändert keine Vanilla-/Mod-Rezepte: Tierprodukte und Verbrennung sind noch nicht gesperrt. Der Bootstrap ist keine nachhaltige Gameplay-Freigabe.

## Öffentliche Quellen

- Forge 1.20.1: https://files.minecraftforge.net/net/minecraftforge/forge/index_1.20.1.html
- Create: https://www.curseforge.com/minecraft/mc-mods/create
- Ex Deorum: https://www.curseforge.com/minecraft/mc-mods/ex-deorum
- Farmer's Delight: https://www.curseforge.com/minecraft/mc-mods/farmers-delight
- Vegan Delight: https://www.curseforge.com/minecraft/mc-mods/vegan-delight
- KubeJS: https://www.curseforge.com/minecraft/mc-mods/kubejs
- FTB Quests: https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge
- Wasteland Reimagined: https://www.curseforge.com/minecraft/mc-mods/wasteland-reimagined
