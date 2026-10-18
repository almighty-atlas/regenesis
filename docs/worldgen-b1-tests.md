# B1-Prüfprotokoll — 2026-10-18

Branch: `feat/issue-3-dead-world`, getesteter Commit `8727cbb`, Ausgangspunkt
gemergtes `main` (`87d1322`). PR [#4](https://github.com/almighty-atlas/regenesis/pull/4)
bleibt Draft, Issue #3 offen. **Serverseitiger Drei-Seed-Smoke-Test bestanden;
bereit für die manuelle Clientabnahme.** Noch kein bestätigter spielbarer
B1-Clientbuild und keine vollständige Definition of Done.

## Dedicated-Lauf mit ausdrücklicher EULA-Zustimmung

Am 2026-10-18, 23:39–23:41 Uhr Europe/Berlin, tatsächlich ausgeführt:

```sh
python3 tools/worldgen_smoke.py \
  --java /usr/lib/jvm/java-17-openjdk/bin/java \
  --accept-eula \
  --output .work/worldgen-b1-consented-01
```

**Läufer-Exit 0**, alle drei Welten im ersten Versuch bestanden. Keine
Fehlversuche, Wiederholungen oder Korrekturen an Läufer, Worldgendaten oder
Modversionen erforderlich. Der Betreiber hat die EULA ausdrücklich selbst
akzeptiert und das Opt-in ausschließlich für neue isolierte B1-Testserver
autorisiert. Die Zustimmung wurde nur in diesen drei neuen Serverkopien gesetzt.

### Voraussetzungen und Isolation

- Vor dem Lauf: sauberer Arbeitsbaum auf dem angeforderten Branch; PR-Head
  identisch mit `8727cbb`. Python **3.14.8**, OpenJDK **17.0.20.1+1**,
  Minecraft **1.20.1**, Forge **47.4.10**.
- Läufer und seine Tests geprüft: explizites EULA-/Java-17-Gate, exklusive
  Erstellung des Ausgabeordners, sequenzielle Prozesse, begrenzter Start/Stop
  und Beendigung ausschließlich der eigenen Prozessgruppen. Kein GUI-Test.
  Der Läufer wertet `Done`, drei Biomproben und Exit 0 aus; zusätzliche
  Log-/Höhen-/Speicherprüfungen erfolgten separat nach dem Lauf.
- `.work/worldgen-b1-consented-01` existierte vor dem Aufruf **nicht**.
  Darunter wurden nur die neuen Unterverzeichnisse `3`, `8675309`, `-20261018`
  mit jeweils eigenem `b1-test-world` erzeugt. Kein Testverzeichnis gelöscht,
  überschrieben oder als Welt wiederverwendet.
- Alle **13** Cache-Artefakte vorab gegen `pack/mods.lock.json` gehasht;
  pro Server **12** gepinnte JARs kopiert, clientseitiges JEI ausgelassen.
  Keine neuen Moddownloads oder geänderten Pins. Kopierte Mod-Hashes nach dem
  Lauf erneut gegen den Lock geprüft.
- Nur die **104 Bibliotheksdateien** aus `.work/server-smoke/libraries`
  kopiert, keine dortigen Welten, Mods oder Konfigurationen übernommen.
  Alle kopierten Libraries und versionierten KubeJS-Dateien nach dem Lauf
  byteweise per SHA256 mit der Quelle verglichen. Konfigurationen stammen aus
  `pack/config`; Forge ergänzt Defaults ausschließlich in den neuen Kopien.
  Das alte `.work/server-smoke/eula.txt` steht weiterhin auf `false`.
- Ports **25586–25588** vorab durch Listenerliste und gleichzeitige Test-Binds
  als frei geprüft. Jeder Server bindet nur `127.0.0.1`; während des dritten
  Laufs bestätigte `ss` ausschließlich `127.0.0.1:25588`. Nach Abschluss keine
  Listener auf allen drei Ports. Socketprüfung und Serverlauf erfolgten
  außerhalb der Socket-beschränkten Sandbox. Kein bestehender Server,
  keine bestehende Instanz und keine bestehende Welt wurden verändert.

### Tatsächliche Serverergebnisse

| Seed | Loopback-Port | `Done`-Wert | Geladene tote Biomproben | Speichern / Shutdown | Ergebnis |
|---|---|---|---|---|---|
| `3` | 25586 | 8,902 s | 3 / 3 | `Saved the game`, abschließend alle Dimensionen gespeichert, Exit 0 | **bestanden** |
| `8675309` | 25587 | 8,976 s | 3 / 3 | `Saved the game`, abschließend alle Dimensionen gespeichert, Exit 0 | **bestanden** |
| `-20261018` | 25588 | 10,303 s | 3 / 3 | `Saved the game`, abschließend alle Dimensionen gespeichert, Exit 0 | **bestanden** |

Die Zeitwerte stammen aus der jeweiligen `Done`-Zeile, nicht aus einer Messung
der gesamten JVM-Laufzeit. Seed und 18 aktivierte Datenpakete wurden pro Welt
in der Konsole bestätigt; KubeJS meldet erfolgreichen Resource-Reload.
Nach `Done` wurden drei Chunks zwangsgeladen, nach 15 s Oberflächenhöhe und Biom
abgefragt und anschließend `save-all flush` sowie `stop` gesendet.

| Seed | Ziel-X/Z | Y der Oberflächenabfrage | Tatsächlich bestätigtes Biom bei Y−1 |
|---|---|---|---|
| `3` | 0 / 0 | 71 | `regenesis:dead_old_growth_birch_forest` |
| `3` | 128 / 128 | 65 | `regenesis:dead_dark_forest` |
| `3` | −128 / −128 | 67 | `regenesis:dead_old_growth_birch_forest` |
| `8675309` | 0 / 0 | 63 | `regenesis:dead_forest` |
| `8675309` | 128 / 128 | 70 | `regenesis:dead_old_growth_birch_forest` |
| `8675309` | −128 / −128 | 95 | `regenesis:dead_meadow` |
| `-20261018` | 0 / 0 | 98 | `regenesis:dead_forest` |
| `-20261018` | 128 / 128 | 118 | `regenesis:dead_snowy_slopes` |
| `-20261018` | −128 / −128 | 94 | `regenesis:dead_forest` |

`positioned over world_surface` liefert die Position oberhalb des höchsten
Nicht-Luftblocks (einschließlich Wasser), keine visuelle Geografieabnahme.
Die Marker stehen jeweils in der Blockmitte, z. B. −127,5 / −127,5 für das
Ziel −128 / −128. Belegt sind neun generierte Oberflächenproben und fünf
unterschiedliche tote Biomtypen; nicht alle 53 Biome wurden ingame aufgesucht.

### Loganalyse und Aussagegrenzen

Pro Welt: **keine ERROR-/FATAL-Einträge** in `console.log`, `logs/latest.log`,
`logs/debug.log` sowie KubeJS-Startup-/Serverlog; keine Crashreports.
Keine fehlgeschlagenen Konsolenproben, Registry-/Datapack-Ladefehler,
Terrain-/Chunkgenerator- oder Feature-Zyklus-Fehler beobachtet.
Das abschließende Speichern umfasst Overworld, Nether und End; eine eigene
Terrainabnahme von Nether/End erfolgte nicht.

Jede Konsole enthält dieselben **286 Warnungen**, geprüft und eingeordnet:

- 276 zur Erstanlage/Ergänzung von Forge-/Modkonfigurationsdefaults
  (1 FMLConfig, 275 ForgeConfigSpec); der Ex-Deorum-Void-Default bleibt `false`.
- 4 Forge-Core-Libraries ohne `mods.toml`, 4 übersprungene clientseitige bzw.
  optionale KubeJS-Plugins und 2 `union:`-Ressourcenpfadwarnungen.
- Zusätzlich stehen im **Debuglog** zwei abgefangene Netty-Capability-Probes:
  `UnsupportedOperationException` für reflektives `setAccessible` und
  `IllegalAccessException` beim Zugriff auf `jdk.internal.misc.Unsafe`.
  Beide treten vor dem erfolgreichen Boot auf; danach folgen `Done`, die
  neun erfolgreichen Proben und reguläre Shutdowns. Keine JVM-Zugriffsrechte
  oder Abhängigkeiten zur Unterdrückung dieser Debugmeldungen verändert.

Versionierte Belege: [Laufberichte mit Hashes](evidence/worldgen-b1-runtime.json)
und [unveränderte ausgewählte Konsolen-/Debugzeilen](evidence/worldgen-b1-runtime.log).
Vollständige Originale bleiben lokal pro Seed unter
`.work/worldgen-b1-consented-01/<seed>/`: `console.log`, `result.json`,
`logs/latest.log`, `logs/debug.log`, `logs/kubejs/` und die neuen Saves.
Die JSON-Belege enthalten SHA256/Größe dieser Logs, Mod-/Plattform-Lockhashes
und den Hash des tatsächlich ausgeführten Läufers.

Zusätzlich in diesem Lauf tatsächlich bestanden (**jeweils Exit 0**):

```sh
python3 tools/pack.py --check
python3 tools/audit_artifacts.py
python3 -m unittest discover -s tests -v
python3 tools/worldgen.py \
  --extra .work/server-smoke/libraries/net/minecraft/server/1.20.1-20230612.114412/server-1.20.1-20230612.114412-extra.jar \
  --report .work/b1-vanilla-reports/reports/biome_parameters/minecraft/overworld.json \
  --check
python3 -m py_compile tools/pack.py tools/worldgen.py tools/worldgen_smoke.py tests/test_worldgen.py tests/test_worldgen_smoke.py
git diff --check
```

**14 Tests bestanden, 0 übersprungen**; 53 Biome / 64 Dateien reproduziert.
Keine erneuten Clientstarts oder ZIP-Exporte für diesen Serverlauf durchgeführt.

## Vorherige Bootstrap-/Vorprüfungen

| Prüfung | Ergebnis / Aussagegrenze |
|---|---|
| Vorhandene 1.20.1-Biom-/Preset-/Noise-JSONs und gepinnte KubeJS-/Create-/FD-/Vegan-Delight-JARs untersucht | **bestanden**; konkrete IDs, Injektionszeitpunkt, Biommodifier und Tagabhängigkeiten statisch geprüft |
| Vanilla Java-17-Datengenerator `-DbundlerMainClass=net.minecraft.data.Main … --reports --output …/.work/b1-vanilla-reports` | **bestanden**, Exit 0; 7.593 Klimaparametereinträge, 53 Overworld-Biome; keine Spielwelt gestartet |
| `python3 tools/worldgen.py --extra …extra.jar --report …/overworld.json --check` | **bestanden**; gehashte Quellen, 64 Dateien einschließlich Mapping, exakte Regenerierung |
| `python3 tools/pack.py --check` | **bestanden**; bestehende 13 Modpins unverändert |
| `python3 tools/audit_artifacts.py` | **bestanden**; 13 Haupt-/20 inklusive eingebetteter JARs, Hash/CRC/Metadaten; kein Runtime-Nachweis |
| `python3 -m unittest discover -s tests -v` | **bestanden**, 14 Tests, 0 übersprungen; sechs Bootstraptests, sechs Worldgen-/Exporttests, zwei Testläufer-Schutztests |
| `python3 -m py_compile tools/pack.py tools/worldgen.py tools/worldgen_smoke.py tests/test_worldgen.py tests/test_worldgen_smoke.py` | **bestanden** |
| Zwei echte Exporte mit gehashten Mods, `regenesis-phase-b1.zip` und `regenesis-phase-b1-repeat.zip` | **bestanden**, bytegleich; keine JARs/ZIPs in Git |
| `python3 tools/worldgen_smoke.py --java /usr/lib/jvm/java-17-openjdk/bin/java` ohne EULA-Opt-in | **erwartet verweigert**, Exit 2; kein Serverstart, kein Testweltordner |
| B1-ZIP in neues `.work/prism/instances/regenesis-b1` entpackt, Java 17 lokal gesetzt | **ausgeführt**; nur Testinstanz, keine Konten/Saves übernommen; kein GUI-Importnachweis |
| Prism/Xvfb innerhalb der Sandbox | **fehlgeschlagen**, Abbruch vor Minecraft; danach unterscheidender Host-Test |
| `QT_QPA_PLATFORM=xcb timeout 25s xvfb-run -a prismlauncher --dir …/.work/prism --launch regenesis-b1 --offline ReGenesisTest` außerhalb der Sandbox | **blockiert**, Exit 124; Prism 11.1.1 erkennt B1-Instanz, `accounts.json` fehlt; kein Minecraft-/Modladefehler erreicht |

Vollständige Befehle und Prüfausgaben:
[`evidence/worldgen-b1-checks.txt`](evidence/worldgen-b1-checks.txt).
Der Datengenerator wurde tatsächlich mit Arbeitsverzeichnis `/tmp` ausgeführt
(ausschließlich neue Bundler-Ausgaben dort); die dokumentierte Wiederholung in
`.work/b1-datagen` isoliert diese Ausgaben im Repository. Datenquellen und
Ausgabehashes sind gleich. Kein Server, keine EULA-Annahme und kein Weltstart
für diese Datengenerierung.

Archiv-SHA256:
`b2dc03da00563f07b9493a910a576b6ba329eede659031fe3181cf640f582e5b`.
Lokales Installationsprodukt unter `.work/regenesis-phase-b1.zip`, keine
Distributions-/Lizenzfreigabe.

Prism-Log: [`evidence/worldgen-b1-prism.log`](evidence/worldgen-b1-prism.log).
Es enthält keine übernommenen Kontodaten; das separate Testprofil besitzt kein
Konto. Der Launcher wurde nach 25 s beendet. Diese Grenze ist kein Minecraft-
Boottime-Messwert. Der frühere Phase-A-Nutzerbericht gilt nicht als B1-Abnahme.

## Nicht durchgeführt / offen

| Seed | Neue Clientwelt | Höhen/Geografie, tatsächliche Erz-/Höhlenfunde | XYZ/Biom-Screenshots | Wachstum / Tiere / Reload |
|---|---|---|---|---|
| `3` | **nicht durchgeführt** | **nicht durchgeführt** | **keine** | **nicht durchgeführt** |
| `8675309` | **nicht durchgeführt** | **nicht durchgeführt** | **keine** | **nicht durchgeführt** |
| `-20261018` | **nicht durchgeführt** | **nicht durchgeführt** | **keine** | **nicht durchgeführt** |

Es gibt weiterhin **keine Client-Ingame-Screenshots oder visuellen
Weltbeobachtungen**. Die Server-Koordinatenproben stehen oben; sie ersetzen
keine entfernten Geografie-, Höhlen- oder Ressourcenfunde im Client.
Keine künstlichen Vorschaugrafiken als Spielbeleg erstellt.

Dedicated-Worldgen-Test: **jetzt bestanden**. Die frühere EULA-Sperre ist für
die drei neuen B1-Testserver durch die ausdrückliche Betreiberzustimmung
aufgehoben. **Manuelle Clientabnahme offen:** Presetwahl/Clientboot,
Renderdarstellung, entfernte Regionen, tatsächliche Erz-/Höhlenfunde,
Screenshots mit F3/XYZ/Biom, natürliches Wachstum, Tierbeobachtung und
Save/Reload. Es wurde gespeichert und sauber gestoppt, aber kein Save erneut
geladen und kein Client verbunden. PR #4 ist für diese manuelle Abnahme
vorbereitet und bleibt bis dahin Draft; kein Merge und keine Gameplay-Freigabe.

Die statische Absicherung belegt fehlende globale Wachstumsverbote und erhaltene
Noise-/Erz-/Carverdefinitionen. Der zusätzliche Serverlauf belegt nun die
erfolgreiche Preset-/Biomanwendung an den Messpunkten durch Forge, weiterhin
**nicht** den erwarteten visuellen Eindruck oder tatsächliches Pflanzenwachstum.
B2-Startervorräte, Verlustschutz, vegane/fossilfreie Progression, dynamische
Renaturierung und Multiplayer-Abnahme bleiben separat offen.
