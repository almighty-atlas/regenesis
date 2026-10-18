# Modstack und Entscheidungsmatrix

## Verbindliche Plattform

| Komponente | Ziel |
|---|---|
| Minecraft | Java 1.20.1 |
| Loader | Forge 47.4.10 (Recommended; Abhängigkeiten prüfen) |
| JVM | Java 17 |
| Entwicklungsclient | Prism Launcher (lokale, getrennte Instanz) |
| Testserver | Forge Dedicated Server erst nach Client-Boot |

## Phase A – Artefaktpins (2026-10-18)

Die folgende Tabelle dokumentiert die heruntergeladenen und statisch geprüften
Artefakte. Clientboot mit Java 17 und 18 angezeigten Mods sowie normale
Weltgenerierung sind inzwischen durch den Nutzer bestätigt; weiterführende
Integrationstests bleiben offen. Server nur bis EULA-Sperre gestartet.
Vollständige SHA256, Bezugsquellen,
Mod-IDs, Seiten und deklarierte Abhängigkeiten stehen in
[`pack/mods.lock.json`](../pack/mods.lock.json), der Forge-Installer in
[`pack/platform.lock.json`](../pack/platform.lock.json).
`side` bezeichnet die Installationspolitik, nicht nachgewiesene Serversicherheit.

| Artefakt | Gepinnte Version | Seite |
|---|---|---|
| Create | 6.0.8 | beide |
| Ex Deorum | 1.53 | beide |
| Farmer's Delight | 1.2.11a | beide |
| Vegan Delight | 1.4.0 (interne JAR-Version 1.4) | beide |
| KubeJS | 2001.6.5-build.26 | beide |
| Rhino | 2001.2.3-build.10 | beide |
| Architectury API | 9.2.14 | beide |
| FTB Quests | 2001.4.22 | beide |
| FTB Library | 2001.2.9 | beide |
| FTB Teams | 2001.3.0 | beide |
| FTB XMod Compat | 2.1.3 | beide |
| JEI | 15.56.0.205 | Client |
| Jade | 11.13.3 | beide |

Create enthält Flywheel 1.0.5, Ponder 1.0.91, Registrate und MixinExtras bereits
als Jar-in-Jar. Nicht nochmals installieren. KubeJS liefert ebenfalls MixinExtras;
die deklarierten Bereiche lassen Creates 0.4.1 zu, die tatsächliche Auswahl ist
noch runtime-seitig zu prüfen. FTB Library/Teams sind anhand der Quests-Upstream-
Buildversionen gewählt. XMod Compat ist die ausdrücklich geplante optionale
Integration. Item Filters und weitere optionale Mods werden nicht hinzugefügt.

[Auswahlbegründung/Lizenzen](artifact-research.md) ·
[Testresultate](bootstrap-tests.md)

## Ursprüngliche Phase-A-Kandidaten (Planungshistorie)

| Mod | Vorgeschlagene Version | Funktion | Status |
|---|---|---|---|
| Create | 6.0.8 | Rotationsenergie, Maschinen | einzeln veröffentlicht, Integration offen |
| Ex Deorum | kompatibles 1.20.1-Release festzulegen | Siebe, Hämmer, Fass, Tiegel | 1.20.1-Version vorhanden |
| Farmer's Delight | 1.20.1/1.2.x bevorzugt bis Compat-Test | Pflanzenverarbeitung | Versionsprüfung offen |
| Vegan Delight | 1.4.0 (Forge 1.20.1) | Soja, Tofu, pflanzliche Alternativen | veröffentlicht |
| KubeJS | 2001.6.5-build.26 | Start-Items, Vanilla-Rezepte, Policies | veröffentlicht |
| FTB Quests | 2001.4.22 | Questbook | veröffentlicht |
| JEI | passendes 1.20.1-Release | Rezeptinspektion | Version offen |
| Jade | passendes 1.20.1-Release | Weltinspektion | Version offen |
| FTB Library/Teams/XMod Compat | jeweils passend | Abhängigkeiten und KubeJS-/JEI-Integration | im Installer verifizieren |

**Keine JARs allein aufgrund eines passenden Minecraft-Versionslabels als konfliktfrei behandeln.** Alle neuen Mods einzeln in die Testinstanz aufnehmen und Boot, Rezepte, Client und Server prüfen.

## Phase B – später, nicht Core-Boot

| Mod | Version/Kandidat | Grund |
|---|---|---|
| Create Crafts & Additions | 1.3.3 (Forge 1.20.1) | mechanisch ⇄ elektrisch, Motoren, Speicher |
| Create: Solar Powered | 1.2.6 (1.20.1) | Solarstrom mit Tag-/Wettereinfluss |
| Naturalist | 5.0pre5 Beta (Forge 1.20.1) | Tiere und Verhaltensweisen; Spawns zunächst sperren |
| In Control! | passendes Forge-1.20.1-Release | Spawn-Policies |
| Wasteland Reimagined | 1.2.5 (Forge 1.20.1) | **nur experimentelle Weltgen-Baseline** |

### Blocker und offene Architekturentscheidungen

- **Weltgen B1:** Eigenes opt-in World-Preset mit 53 zuordenbaren toten Biomvarianten über den vorhandenen KubeJS-Datenordner implementiert, ohne neue JARs. Originale Klimazuordnung und Terrain-Dichte bleiben erhalten; Runtime-Abnahme fehlt. Wasteland Reimagined wird nicht hinzugefügt. [Entscheidung, Details und Grenzen](worldgen-b1.md).
- **Renaturierung:** Eigene Forge-Mod für persistente Regionswerte, Flächenänderungen, Artansiedlung und spätere Biome. Für MVP zuerst demonstrierbare **Blockregeneration** in einem kleinen Testgebiet; Biomwechsel danach.
- **Ex-Deorum-Rezepte:** Basismod enthält datengetriebene Rezepte; 1.20.1-API tatsächlich am gewählten JAR prüfen. Das Zusatzmod „KubeJS Ex Deorum“ ist nur für jüngere NeoForge-Versionen gelistet.
- **Vegan Delight:** Version 1.4.0 Stable gegenüber 2.0.0 Beta bevorzugen; Farmer's-Delight-API-/Versionstest erforderlich.
- **Energietransition:** Keine Vanilla-Furnace-Abkürzung durch Holz/Kohle. Verbrennungs-Fuel-Events und Vanilla-Smelting-Bypässe auditieren und vor spielbarer Alpha sperren.

## Grundsatz beim Pack-Design

Artefaktpins und Laufzeitfreigabe getrennt behandeln: Der Lock fixiert Bytes und deklarierte Abhängigkeiten, **nicht** erfolgreiche Client-/Server-Kompatibilität. Pairings erst nach vollständigen Loader-/Ingame-Tests als runtime-verifiziert markieren. Keine Mods blind auf den aktuellsten Release aktualisieren.
