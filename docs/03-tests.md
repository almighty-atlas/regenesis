# Prüfplan — ReGenesis v0.1 / v0.2

## Phase A – aktueller Stand

[Ausgeführte Prüfungen und Blocker](bootstrap-tests.md),
[Serverstart-Belege](server-smoke-evidence.md).

Moddownloads/Hashes, Metadaten, Exporttests und Forge-Installation sind bestanden.
Clientstart mit Java 17, 18 angezeigten Mods und normale Weltgenerierung sind
**durch den Nutzer bestätigt** (2026-10-18), ohne von Codex erfasste Clientlogs.
Der Exporttest prüft `common.set_void_world_as_default = false` im Prism-ZIP;
er ersetzt keinen erneuten Ingame-Test des neu erzeugten Archivs.
Ein vollständiger Serverboot ist **nicht nachgewiesen**.
Der Pre-EULA-Serverlauf ist kein Ersatz dafür.
Die folgenden Gameplaytests bleiben Spezifikation für spätere Phasen.
Forschungsstation, eigene Rezepte und Weltgenerierung gehören nicht zu Issue #1.

## Integration (Client / Server)

1. Prism-Launcher-Instanz 1.20.1/Forge 47.4.10 mit Java 17 bootet; Versions- und Abhängigkeitsliste wird eingefroren.
2. Phase A: Eine neue Wegwerfwelt verwendet normale Terrain-Generierung als Standard
   (vom Nutzer bestätigt). Forschungsstation/Wasteland sind spätere, noch nicht
   implementierte Abnahmeziele; eigene Weltgenerierung gehört nicht zum Bootstrap.
3. Alle Rezepte sind in JEI sichtbar; keine ungültigen oder mehrdeutigen IDs.
4. Derselbe Pack bootet mit denselben Mods auf einem Dedicated-Forge-Server; Testclient kann verbinden.
5. Persistente Quest- und Regionsdaten überleben Neustart und Backup/Restore.

## Testfälle mit klarem Bestehen/Nichtbestehen

| ID | Test | Erfolg |
|---|---|---|
| P01 | Alle Startvorräte absichtlich zerstören | alternative Gewinnungsroute für Setzlinge, Biomasse, Wasser und Werkzeuge vorhanden |
| P02 | 10 zufällige Seeds erzeugen | alle können Kapitel I ohne Cheats abschließen |
| P03 | 2 h nur pflanzliche Nahrung | Hunger ist ohne Tierprodukte stabil deckbar |
| P04 | Tierische Loot- und Standardrezepte prüfen | keine notwendige Rezeptkette verlangt Tierausbeutung |
| P05 | Energieherstellung durchsuchen | keine Pflichtmaschine benötigt Kohle, Holzkohle, Öl, Gas oder fossile Verbrennung |
| P06 | Frühe Eisenbeschaffung | Sieb-/Hammerroute erneuerbar und JEI-dokumentiert |
| P07 | Zerstörtes Filtermaterial | Nachproduktion aus reproduzierbaren Rohstoffen möglich |
| P08 | Früheste Create-Windmühle | ohne fossil befeuerte Schmelze erreichbar |
| P09 | Oase erfolgreich regenerieren | Fläche sichtbar grün; keine direkte Freischaltung allein durch Placement-Abkürzung |
| P10 | Save & Reload | gleiche Renaturierungsstufe, Pflanzen und Questzustände |
| P11 | Tiere töten/melken/scheren | keine Progressionsvorteile; benötigte Alternativen existieren |
| P12 | Vanilla-Furnace-/Campfire-/Smoker-Bypass | nicht als alternative fossile Produktionsroute ausnutzbar |

## Performance und Server

- Regionen nur in geladenen Chunks mit Budget pro Tick verarbeiten; Zustände für entladene Gebiete aggregiert speichern.
- Max. Änderungen/Entities pro Tick hart begrenzen; keine endlosen Spread-Loops.
- Jedes Rezept-/Spawn-Override und jede Weltgen-Regel ist konfigurierbar und testbar.
- Spawn-/Biome-/Chunk-Änderungen zuerst in Wegwerf-Testwelten prüfen; nicht in bestehenden Vanilla-Welten testen.

## Definition der frühen Releases

- **MVP 0.1:** Ein neuer Spieler kann einen Baum, wiederholbare pflanzliche Nahrung, ein Sieb, einen Wasserfilter, fruchtbaren Boden und eine mechanisch angetriebene Produktionsstation ohne Fossilenergie herstellen.
- **MVP 0.2:** Ein 16×16-Teilgebiet erhält persistente Umweltwerte, wandelt sichtbar Blöcke um und unterstützt eine erste geeignete, natürlich vermehrbare Bestäuberpopulation.

Die Gameplay- und Releaseziele bleiben **Spezifikation, nicht bestandene Tests**;
die manuelle Client-/Terrain-Abnahme bestätigt nur den Bootstrap.
