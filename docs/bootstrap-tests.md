# Phase-A-Prüfprotokoll – 2026-10-18

Branch: `feat/issue-1-forge-bootstrap`; Issue #1.

Historischer Phase-A-Bericht. Später wurden nach ausdrücklicher Zustimmung
drei neue B1-Serverwelten erfolgreich gestartet, geprüft und gestoppt;
[aktuelles B1-Protokoll](worldgen-b1-tests.md). Clientabnahme für B1 bleibt offen.

## Tatsächlich ausgeführt

| Prüfung | Ergebnis | Aussagegrenze |
|---|---|---|
| Alle 13 Modartefakte recherchiert, heruntergeladen und SHA256 fixiert | **bestanden** | keine Runtime-Kompatibilitätsgarantie |
| Hersteller-Prüfsummen, TOML-Bereiche/Abhängigkeiten, Java-Basisbytecode untersucht | **bestanden** | [Recherche](artifact-research.md); kein API-/Mixin-Test |
| `python3 tools/pack.py --check` | **bestanden** | Plattform/Lockformat |
| `python3 tools/pack.py` | **bestanden** | 13 verifizierte JARs in lokalem Prism-Archiv |
| Download aus leerem Cache mit `--cache .work/clean-downloads --output .work/regenesis-clean.zip` | **bestanden** | echte Neuinstallation der Modartefakte ohne Recherchecache |
| `python3 tools/audit_artifacts.py` | **bestanden** | 13 Haupt-/20 inklusive eingebetteter JARs; Hash, CRC, Metadaten, erforderliche Provider |
| `python3 -m unittest discover -s tests -v` (erneut nach Konfigurationsänderung) | **bestanden**, 6 Tests, 0 übersprungen | Lockfehler, Cache-Manipulation, Downloadfehler, exakte/deterministische ZIPs, Überschreibschutz, Ex-Deorum-TOML im ZIP |
| `python3 -m py_compile tools/pack.py tools/server_smoke.py tools/audit_artifacts.py tests/test_pack.py` | **bestanden** | Python-Syntax |
| Prism 11.1.1: früherer isolierter Codex-Startversuch | **damals blockiert** | kein Konto in diesem separaten Profil; historischer Beleg unten |
| Manueller Clientstart mit Java 17, 18 angezeigte Mods | **durch Nutzer bestätigt**, 2026-10-18 | reguläres Prism-Profil; keine von Codex erfassten Clientlogs |
| Neue normale Minecraft-Welt nach `set_void_world_as_default = false` | **durch Nutzer bestätigt**, 2026-10-18 | Bootstrap-Terrain, keine eigene ReGenesis-Weltgenerierung |
| Forge 47.4.10 Dedicated Installer, Java 17 | **bestanden**, Exit 0 | nur Installation |
| Echter Dedicated-Pre-EULA-Start mit zwölf serverseitigen Artefakten | **blockiert**, Läufer-Exit 2 | endet bei `eula=false`, kein `Done`, keine Welt |
| Neuer Export mit festem Ex-Deorum-Default: Ingame-Wiederholung | **nicht durchgeführt** | Export automatisiert geprüft; Nutzer testete zuvor die lokale Konfigurationsänderung |
| Separate JEI/Jade/Create-/Quest-Funktionstests ingame | **nicht durchgeführt** | Clientstart alleine bestätigt nicht diese Funktionen |
| Vollständiger Serverboot, Clientverbindung, Save/Reload | **nicht durchgeführt** | Betreiber-EULA-Zustimmung und weiterer Lauf nötig |
| Nachhaltigkeits-/Progressionschecks P01–P12 | **nicht durchgeführt** | Phase A implementiert keine Gameplayregeln |

## Nachtrag zu PR #2: Clientabnahme und Exportkonfiguration

Der [Nutzerbericht in PR #2](https://github.com/almighty-atlas/regenesis/pull/2#issuecomment-6255154986)
bestätigt Clientstart mit Java 17 und **18 angezeigten Mods**. Diese Anzeige ist
von den **13 heruntergeladenen Modartefakten** im Lock zu unterscheiden;
die Zählung ist kein vollständiger Abgleich der Runtime-Modliste.
Nach lokaler Änderung von `config/exdeorum-common.toml` auf
`[common]` → `set_void_world_as_default = false` wurde eine normale Minecraft-Welt
erfolgreich erstellt. Der vorherige Standard führte zu einem Ex-Deorum-Skyblock.
Unter CachyOS korrigierte **Use system installation of OpenAL** den zunächst
verzerrten Sound. Die README dokumentiert diese optionale Prism-Einstellung.

Die versionierte Vorlage `pack/config/exdeorum-common.toml` wird nun unverändert
als `.minecraft/config/exdeorum-common.toml` in jedes neue Prism-Archiv geschrieben.
Die Common-Config-Registrierung und der Pfad `common.set_void_world_as_default`
(Moddefault `true`) wurden direkt im gepinnten Ex-Deorum-1.53-JAR geprüft:

```sh
javap -c -p -classpath .work/artifacts/exdeorum-1.53.jar 'thedarkcolour.exdeorum.config.EConfig$Common' thedarkcolour.exdeorum.ExDeorum
```

Der neue Test `test_archive_contains_normal_world_default` erzeugt ein Archiv,
liest die TOML daraus und prüft den exakten Pfad, die unveränderten Vorlagenbytes
und den Boolean-Wert `false`. Nur die Moddownloads werden durch lokale Testdaten
ersetzt; dieser Test läuft auch ohne Artefaktcache oder Netzwerk. Der bestehende
Integrationstest exportiert weiterhin die echten gehashten JARs zweimal und
prüft Bytegleichheit und Überschreibschutz. Alle sechs Tests wurden mit
vorhandenem Artefaktcache ausgeführt; keiner wurde übersprungen.

Erneut bestanden: Lockcheck, Artefaktaudit (13 Haupt-/20 inklusive eingebetteter
JARs), Unittests und Python-Syntaxprüfung. Der neue Export wurde außerdem mit
den echten Artefakten aus beiden vorhandenen Caches verglichen; Befehle und
Archivhash stehen in [`evidence/pr-2-followup-checks.txt`](evidence/pr-2-followup-checks.txt).
Kein erneuter Minecraft- oder Serverstart wurde dafür ausgeführt.
Bestehende ZIPs, Instanzen und Spielstände werden nicht nachträglich verändert.

## Früherer Codex-Clientversuch und damaliger Blocker

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
Mod-Ladefehler wurde **nicht** erreicht. Dieser Versuch belegt weder einen
erfolgreichen Prism-GUI-Import noch einen Clientboot. Die spätere erfolgreiche
Clientabnahme stammt ausschließlich aus dem oben verlinkten Nutzerbericht.

## Server, bekannte Risiken und nächste Abnahme

[Server-Belege und opt-in Testkommando](server-smoke-evidence.md).
Auch ein Pre-EULA-Exit 0 ist kein Nachweis vollständiger Modinitialisierung.

1. Das neu erzeugte Archiv in einer neuen Instanz ingame gegenprüfen und
   `latest.log`/Modliste sichern; die bisherige manuelle Abnahme verwendete eine
   lokal angepasste Ex-Deorum-Konfiguration.
2. Create/Flywheel/Ponder-Rendering und tatsächliche JarJar-Auswahl, Farmer's
   Delight/Vegan-Delight-APIs sowie KubeJS-/FTB-/JEI-Integration ingame prüfen.
   Bei Fehlern zuerst Stacktrace/Modmetadaten analysieren, nicht blind aktualisieren.
3. Nach persönlicher EULA-Zustimmung Server bis `Done` starten, sauber stoppen,
   anschließend Clientverbindung in einer neuen Wegwerfwelt testen.
4. Erst danach Phase B/Rezepte und nachhaltige Progression auditieren. Unveränderte
   Vanilla-/Mod-Rezepte bieten derzeit noch Tierprodukte/Verbrennung; dies ist
   **kein nachhaltig spielbarer Release** und keine Umsetzung dieser Designziele.

Es wurden keine Rezepte, Pflichtzutaten, Questkapitel, Terraforming-Mods oder
eigene Weltgenerierung hinzugefügt. Die Ex-Deorum-Konfiguration ändert nur den
Standard-Welttyp für neue Welten. Keine bestehenden Server oder Spielstände verändert.
