# Phase-A-Prüfprotokoll – 2026-10-18

Branch: `feat/issue-1-forge-bootstrap`; Issue #1.

## Tatsächlich ausgeführt

| Prüfung | Ergebnis | Aussagegrenze |
|---|---|---|
| Alle 13 Modartefakte recherchiert, heruntergeladen und SHA256 fixiert | **bestanden** | keine Runtime-Kompatibilitätsgarantie |
| Hersteller-Prüfsummen, TOML-Bereiche/Abhängigkeiten, Java-Basisbytecode untersucht | **bestanden** | [Recherche](artifact-research.md); kein API-/Mixin-Test |
| `python3 tools/pack.py --check` | **bestanden** | Plattform/Lockformat |
| `python3 tools/pack.py` | **bestanden** | 13 verifizierte JARs in lokalem Prism-Archiv |
| Download aus leerem Cache mit `--cache .work/clean-downloads --output .work/regenesis-clean.zip` | **bestanden** | echte Neuinstallation der Modartefakte ohne Recherchecache |
| `python3 tools/audit_artifacts.py` | **bestanden** | 13 Haupt-/20 inklusive eingebetteter JARs; Hash, CRC, Metadaten, erforderliche Provider |
| `python3 -m unittest discover -s tests -v` | **bestanden**, 5 Tests, 0 übersprungen | Lockfehler, Cache-Manipulation, Downloadfehler, exakte/deterministische ZIPs, Überschreibschutz |
| `python3 -m py_compile tools/pack.py tools/server_smoke.py tools/audit_artifacts.py` | **bestanden** | Python-Syntax |
| Prism 11.1.1: isolierte Instanz entdeckt, Start versucht | **blockiert** | kein Konto in isoliertem Profil; kein Minecraft-Prozess nachgewiesen |
| Forge 47.4.10 Dedicated Installer, Java 17 | **bestanden**, Exit 0 | nur Installation |
| Echter Dedicated-Pre-EULA-Start mit zwölf serverseitigen Artefakten | **blockiert**, Läufer-Exit 2 | endet bei `eula=false`, kein `Done`, keine Welt |
| GUI-Import, Client-Hauptmenü, neue Welt, JEI/Jade/Create/Quests ingame | **nicht durchgeführt** | authentifizierter Clientstart erforderlich |
| Vollständiger Serverboot, Clientverbindung, Save/Reload | **nicht durchgeführt** | Betreiber-EULA-Zustimmung und weiterer Lauf nötig |
| Nachhaltigkeits-/Progressionschecks P01–P12 | **nicht durchgeführt** | Phase A implementiert keine Gameplayregeln |

## Clientversuch und genauer Blocker

Java 17 ist installiert (`/usr/lib/jvm/java-17-openjdk/bin/java`,
OpenJDK `17.0.20.1+1`). Systemstandard ist dagegen Java **27**;
Java 17 muss deshalb in Prism explizit für diese Instanz gewählt werden.
Grafik ist vorhanden (AMD RX 7800 XT, Mesa 26.2.4, OpenGL 4.6).
Kein Hinweis auf einen fehlenden Java-17-/GPU-Treiber als Startblocker.

Für die lokale Diagnose wurde das erzeugte Prism-Archiv in das neue Verzeichnis
`.work/prism/instances/regenesis` entpackt und nur dort der Java-Pfad gesetzt.
Keine bestehende Prism-Konfiguration und keine fremden Kontodaten wurden übernommen.

Zweiter, zeitlich begrenzter Aufruf:

```sh
QT_QPA_PLATFORM=xcb timeout 20s xvfb-run -a prismlauncher --dir .work/prism --launch regenesis --offline ReGenesisTest
```

Der Prozess blieb im Launcher bis zur Zeitgrenze (Exit 124). Beleg:
[`evidence/prism-launch-attempt.log`](evidence/prism-launch-attempt.log).

```text
Found instance ID "regenesis"
Failed to read the account list file accounts.json (No such file or directory).
```

Ein erster Aufruf ohne `QT_QPA_PLATFORM=xcb` nutzte trotz Xvfb den vorhandenen
Wayland-Backend und blieb in der Ersteinrichtung. Der zweite wurde daher auf
X11/Xvfb begrenzt. Das fehlende Konto ist belegt; ein Minecraft-Authfehler oder
Mod-Ladefehler wurde **nicht** erreicht. Es wird weder eine erfolgreiche
Prism-GUI-Importabnahme noch ein Clientboot behauptet. Ein legitimes
Minecraft-Java-Konto muss der Betreiber selbst in der separaten Prism-Instanz
hinzufügen und die Ersteinrichtung abschließen. Keine Authentifizierung umgehen.

## Server, bekannte Risiken und nächste Abnahme

[Server-Belege und opt-in Testkommando](server-smoke-evidence.md).
Auch ein Pre-EULA-Exit 0 ist kein Nachweis vollständiger Modinitialisierung.

1. Separates Prism-Profil einrichten, anmelden, Java 17 auswählen; Hauptmenü
   mit dieser unveränderten Artefaktliste erreichen, `latest.log`/Crashreport sichern.
2. Create/Flywheel/Ponder-Rendering und tatsächliche JarJar-Auswahl, Farmer's
   Delight/Vegan-Delight-APIs sowie KubeJS-/FTB-/JEI-Integration ingame prüfen.
   Bei Fehlern zuerst Stacktrace/Modmetadaten analysieren, nicht blind aktualisieren.
3. Nach persönlicher EULA-Zustimmung Server bis `Done` starten, sauber stoppen,
   anschließend Clientverbindung in einer neuen Wegwerfwelt testen.
4. Erst danach Phase B/Rezepte und nachhaltige Progression auditieren. Unveränderte
   Vanilla-/Mod-Rezepte bieten derzeit noch Tierprodukte/Verbrennung; dies ist
   **kein nachhaltig spielbarer Release** und keine Umsetzung dieser Designziele.

Es wurden keine Rezepte, Pflichtzutaten, Questkapitel, Terraforming-Mods oder
Weltgen-Regeln hinzugefügt. Keine bestehenden Server oder Spielstände verändert.
