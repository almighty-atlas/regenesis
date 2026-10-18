# B1-Prüfprotokoll — 2026-10-18

Branch: `feat/issue-3-dead-world`, Ausgangspunkt gemergtes `main` (`87d1322`).
Issue #3 bleibt bis zur Laufzeitabnahme offen. **Kein bestätigter spielbarer
B1-Build und keine vollständige Definition of Done.**

## Tatsächlich ausgeführt

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

Es gibt **keine Ingame-Screenshots oder Weltkoordinaten-Beobachtungen** dieses
Laufs. Die in der Anleitung genannten Koordinaten sind Testziele, keine Funde.
Keine künstlichen Vorschaugrafiken als Spielbeleg erstellt.

Dedicated-Worldgen-Test: **nicht durchgeführt**. Die explizite EULA-Zustimmung
wurde separat angefragt und liegt für diesen Lauf bislang nicht vor.
`tools/worldgen_smoke.py` ist vorbereitet, aber sein Boot-/Drei-Seed-Pfad
einschließlich Konsolenproben ist **ungetestet**. Nur seine Verweigerung ohne
Zustimmung und sein Schutz vorhandener Ausgabeziele wurden getestet.
Keine Testwelt erzeugt und keine bestehenden Welten/Server verändert.

Die statische Absicherung belegt fehlende globale Wachstumsverbote und erhaltene
Noise-/Erz-/Carverdefinitionen; sie belegt **nicht** die erfolgreiche Anwendung
durch Forge, den erwarteten visuellen Eindruck oder tatsächliches Pflanzenwachstum.
B2-Startervorräte, Verlustschutz, vegane/fossilfreie Progression, dynamische
Renaturierung und Multiplayer-Abnahme bleiben separat offen.
