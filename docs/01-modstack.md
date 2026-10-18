# Modstack und Entscheidungsmatrix

## Verbindliche Plattform

| Komponente | Ziel |
|---|---|
| Minecraft | Java 1.20.1 |
| Loader | Forge 47.4.10 (Recommended; Abhängigkeiten prüfen) |
| JVM | Java 17 |
| Entwicklungsclient | Prism Launcher (lokale, getrennte Instanz) |
| Testserver | Forge Dedicated Server erst nach Client-Boot |

## Phase A – Core

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

- **Weltgen:** Wasteland Reimagined überschreibt andere Biome. Für prozedurale Landschaftsvielfalt + spätere regionale Biomrückkehr brauchen wir voraussichtlich ein eigenes Datapack-Worldgen-Setup oder eine kleine Mod. Der Test mit Wasteland ist kein Architekturentscheid für 1.0.
- **Renaturierung:** Eigene Forge-Mod für persistente Regionswerte, Flächenänderungen, Artansiedlung und spätere Biome. Für MVP zuerst demonstrierbare **Blockregeneration** in einem kleinen Testgebiet; Biomwechsel danach.
- **Ex-Deorum-Rezepte:** Basismod enthält datengetriebene Rezepte; 1.20.1-API tatsächlich am gewählten JAR prüfen. Das Zusatzmod „KubeJS Ex Deorum“ ist nur für jüngere NeoForge-Versionen gelistet.
- **Vegan Delight:** Version 1.4.0 Stable gegenüber 2.0.0 Beta bevorzugen; Farmer's-Delight-API-/Versionstest erforderlich.
- **Energietransition:** Keine Vanilla-Furnace-Abkürzung durch Holz/Kohle. Verbrennungs-Fuel-Events und Vanilla-Smelting-Bypässe auditieren und vor spielbarer Alpha sperren.

## Grundsatz beim Pack-Design

Erst nur mit tatsächlichem Loader-Test als **locked** markieren: Mod-JAR-Version, SHA-256, benötigte Abhängigkeiten, getestete Pairings und Ergebnis. Keine Mods blind auf den aktuellsten Release aktualisieren.
