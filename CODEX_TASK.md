# Codex-Auftrag – ReGenesis: MVP 0.1, Integrationsschritt A

Arbeite anhand von README.md und docs/*.md. Projekt ist ein Forge-1.20.1-Modpack und kein Plugin für den bestehenden Vanilla-26.3-Server.

## Auftrag

1. Stelle eine reproduzierbare Forge-1.20.1/Java-17-Entwicklungsinstanz und einen Lockfile-/Manifest-Workflow für Mods bereit (keine JARs ins Git, wenn Lizenzen/Distribution unklar sind).
2. Prüfe mindestens Create 6.0.8, Ex Deorum 1.20.1, Farmer's Delight + Vegan Delight 1.4.0, KubeJS 2001.6.5-build.26, FTB Quests 2001.4.22, JEI, Jade und erforderliche FTB-/Mod-Abhängigkeiten. Notiere tatsächliche installierte Versionsnummern und Ladefehler. Bei Inkompatibilitäten nicht blind aktualisieren; Ursache präzise ermitteln.
3. Baue einen **minimalen integrierten** Startablauf. Zunächst darf die Forschungsstation als explizit platzierte Teststruktur/Starter-Kit umgesetzt werden. Keine ungetestete großflächige Weltgen-Änderung mit einer bestehenden Welt vermischen.
4. Implementiere zwei bis vier frühe Rezepte aus docs/02-gameplay.md mit KubeJS/Datapack nur unter Verwendung bestätigter Item-IDs. Stelle sicher, dass jede Zutat reproduzierbar ist.
5. Schreibe Tests/Audits für modabhängige Rezepte und Start-Loop sowie eine Liste noch offener Risiken.

## Grundsätze

- Nicht gegen die vegane / fossilfreie Philosophie arbeiten. Bei Konflikten alternative Rezepte vorschlagen.
- Weltgen-Test mit Wasteland Reimagined ist optional, zunächst isoliert und nur für neue Wegwerfwelten; es ist wegen der vollständigen Biomüberschreibung nicht als finale Lösung gesetzt.
- Keine angeblich vollständige Terraforming- oder Tierpopulations-Mechanik vortäuschen. Das erfordert eine eigene Mod und folgt nach erfolgreichem MVP-0.1-Ressourcenloop.
- Kein automatischer Merge und keine Veränderung bestehender Minecraft-Server oder Spielstände.

## Abnahme

- Reproduzierbare Installations- und Startanleitung.
- Tatsächlich mit Forge 1.20.1 bootbarer Client; bei vorhandener Umgebung zusätzlich Server-Ladetest.
- Rezeptliste + JEI-/KubeJS-Validierung + dokumentierte erfolgreiche und fehlgeschlagene Tests.
- Kurze Next-Steps-Liste nur für noch nicht implementierte Anforderungen.

## Ergebnisformat

Kurzer Bericht mit: getesteter Modversionen-Tabelle, Startkommandos, umgesetzten Rezepten, Testlogs, verbleibenden Blockern; bei ausstehenden Ingame-Tests diese ausdrücklich als **nicht durchgeführt** markieren.
