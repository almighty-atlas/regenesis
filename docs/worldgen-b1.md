# Phase B1 — Die tote Welt

## Status und Entscheidung

Issue [#3](https://github.com/almighty-atlas/regenesis/issues/3): implementierter
**Datenprototyp, noch keine bestätigte spielbare Welt**. Statische Prüfungen und
Export sind bestanden. Drei-Seed-Ingame-Abnahme und Screenshots fehlen;
[Prüfprotokoll](worldgen-b1-tests.md). Keine bestehenden Welten verwenden.

| Strategie unter Forge 1.20.1 | Bewertung |
|---|---|
| Wasteland Reimagined, ein Ersatzbiom | Nicht gewählt: ursprüngliche regionale Ökotypen gehen verloren; zusätzliche Modabhängigkeit. |
| Globale Vanilla-Biom-/Spawn-/Tick-Overrides | Nicht gewählt: beeinflusst normale Welten und erschwert spätere Wiederherstellung. |
| Eigenes Preset mit zuordenbaren toten Biomvarianten | **B1:** bestehender Noise-Generator, getrennte Daten und lokale Spawn-/Featuredefinitionen; keine neue Mod. |
| Eigener Forge-Chunkgenerator / dauernde Chunk-Nachbearbeitung | Für B1 unnötig. Eigene Mod erst für persistente Umweltwerte und budgetierte dynamische Änderungen. |

Die technische Grundlage wurde **an den tatsächlich vorhandenen 1.20.1-Dateien**
geprüft: `worldgen/world_preset/normal.json`, `worldgen/biome/*.json`,
`worldgen/noise_settings/overworld.json` und der echte Vanilla-`--reports`-Export
der Klimaparameter. Quellenhashes: `pack/worldgen/sources.lock.json`.
Das gepinnte KubeJS-2001.6.5-build.26-JAR enthält
`WorldLoaderPackConfigMixin.injectKubeJSPacks`: Es bindet seinen Datenordner
beim WorldLoader ein, bevor die dynamischen Worldgen-Registries gelesen werden.
Auch der [Upstream-KubeJS-Code](https://github.com/KubeJS-Mods/KubeJS/blob/2001/common/src/main/java/dev/latvian/mods/kubejs/KubeJS.java)
beschreibt `kubejs/data` als Datenpaket. Diese technische Prüfung ersetzt keinen
Boot mit dem neuen Preset.

## Umsetzung und Grenzen

- `regenesis:dead_world` ist ein **zusätzliches**, ausdrücklich auszuwählendes
  Weltpreset. Vanilla-Normal bleibt Standard; Ex Deorums Void-Default bleibt aus.
  Nether und End sind unverändert und **nicht** Teil der toten Overworld.
- 53 Varianten `regenesis:dead_<original>` erhalten alle 7.593 Klimazuordnungen.
  Temperatur, Niederschlag, dreidimensionale Höhlenregionen und Biominformationen
  bleiben zuordenbar. Kein einzelnes universelles Wasteland-Biom.
- Overworld-Dichtefunktionen, Höhenbereich −64 bis 319, Aquifere, Meeresspiegel,
  Erzadern und Carver bleiben in den Daten unverändert. Die Oberflächenregeln
  kennen die neuen Biom-IDs; Gras, Erde, Podzol, Myzel und Schlamm werden dort
  durch Kies ersetzt. Sand, Schnee, Eis, Fels und Badlands bleiben regional.
  Unterirdische Erd-/Kies-/Tonvorkommen und Vanilla-Erze bleiben erhalten.
- `VEGETAL_DECORATION` ist nur in den neuen Biomen leer: keine generierten
  Wälder, Blumen, Gräser, Korallen/Kelp oder Lush-Cave-Vegetation aus dieser
  Stufe. Mangroven-`disk_grass` wird zusätzlich aus der Erzstufe entfernt.
  Sculk, Fossilien und Strukturholz können verbleiben; dies ist kein steriles
  Universum und keine tierproduktfreie Rezeptfreigabe.
- Friedliche Land-/Wasserpopulationen, Axolotl und Fledermäuse haben in den neuen
  Biomen leere Spawnlisten. Hostile Spawns bleiben. Kein globales
  `doMobSpawning=false`, keine Event-Abbrüche. Struktur-/Spezialspawns,
  insbesondere wandernde Händler/Patrouillen, sind damit **nicht allgemein
  gesperrt**. Sie sind eine bekannte B1-Grenze.
- Nur die Struktur-Biomtags für Minenschächte, Mesa-Minenschächte und Strongholds
  werden um passende neue Biome ergänzt; verschachtelte Vanilla-Tags werden
  aufgelöst. Dörfer und andere bewohnte Vanilla-Strukturen werden nicht
  übernommen. Strukturen sind in den Daten zugelassen, noch nicht ingame belegt.
- Die toten Biome erben bewusst keine breiten `is_overworld`-/Klima-Tags:
  Farmer's Delight und Vegan Delight würden sonst wieder Wildpflanzen hinzufügen.
  Create 6.0.8 `create:zinc_ore` und `create:striated_ores_overworld` werden
  ausdrücklich per lokalem Forge-Biommodifier ergänzt. Diese IDs und
  `underground_ores` wurden aus dem gepinnten Create-JAR gelesen.
- Es gibt keine Wachstums-, Random-Tick-, Pflanz- oder Rezept-Hooks. Auf geeigneter
  Erde bei passendem Licht können Setzlinge/Saatgut weiterhin die ursprünglichen
  Wachstumsregeln verwenden. **Technisch abgesichert, noch kein beobachteter
  Wachstumstest.** B2 muss Startvorräte und wiederholbare Rückgewinnung garantieren;
  B1-Survival ohne Testinventar ist noch keine geprüfte Progression.
- Minecraft verwendet an einzelnen Stellen direkte Vanilla-Biomprüfungen
  (z. B. besondere Eisberg-/Badlands-Oberflächenbehandlung). Die neuen IDs
  garantieren deshalb keine blockidentische Geografie zum Vanilla-Vergleich.
  Modkonfigurationen können Features/Spawns ergänzen; nach Modänderungen neu testen.

## Neue Client-Testinstanz

Die bestehenden Installationsschritte aus der README gelten weiterhin. Zusätzlich:

```sh
python3 tools/pack.py --output .work/regenesis-phase-b1.zip
python3 -m unittest discover -s tests -v
```

Neues ZIP in eine **neue** Prism-Instanz importieren, Java 17 setzen. Keine Dateien
in eine bereits benutzte Instanz kopieren. Unter **Neue Welt → Welt → Welttyp**
**ReGenesis: Die tote Welt** auswählen (englisch: **ReGenesis: The Dead World**).
Die experimentelle-Worldgen-Abfrage bestätigen, sofern angezeigt. Fehlt das
Preset oder scheitert die Registry, abbrechen und `logs/latest.log` sichern;
eine normale Welt wäre kein bestandener B1-Test. Kein Datenpaket manuell hinzufügen:
`tools/pack.py` exportiert alle versionierten `pack/kubejs/data`-/`assets`-Dateien
und die Zuordnungs-/Quellenmetadaten automatisch. Keine neue JAR-Abhängigkeit.

Mindestens drei **neue Creative-Welten mit Cheats**: Seeds `3`, `8675309`,
`-20261018`, jeweils eindeutiger Name `B1-<seed>-<lauf>`. Diese Creative-Testwahl
ersetzt noch keine Survival-Abnahme. Pro Welt:

1. Presetwahl und erste Oberfläche mit F3, Seed, XYZ und Biom dokumentieren.
2. Spawngebiet und mindestens zwei entfernte Landregionen untersuchen; Berge/
   Täler, Gewässer und Vegetationsarmut fotografieren. Meeresspawns sind möglich.
3. Im Zuschauermodus Höhlen und tatsächliche Eisen-/Kupfer-/Diamant-/Zinkvorkommen
   untersuchen. Erzpalette/Dateidefinition alleine ist kein Fundnachweis.
4. Bei normaler Tages-/Tickregel Erde, Wasser, Setzling und Weizen aus dem
   Creative-Inventar setzen. Wachstum und Save/Reload prüfen; F3-Biom mit
   `pack/worldgen/biome-map.json` abgleichen. Knochenmehl ist keine nötige Zutat.
5. Tagsüber friedliche Populationen beobachten, einschließlich Wasser und
   Spezialspawns. Logs, Koordinaten, Screenshots und Beobachtungsdauer sichern.

Die Steuermetadaten eines bestehenden Saves niemals nachträglich austauschen.

## Reproduzierbare Generierung und Tests

Normaler Export benötigt nur die versionierten JSONs und den Modcache. Zum
Nachgenerieren braucht man den gepinnten Forge-Server-Installationscache aus
`tools/server_smoke.py`; die **Installation und Datengenerierung** erfordern
keine EULA-Annahme und starten keine Spielwelt. Java 17 explizit wählen.
Den Bundler in einem neuen Arbeitsverzeichnis ausführen, damit auch seine
entpackten Libraries nicht mit vorhandenen Installationen vermischt werden:

```sh
mkdir .work/b1-datagen
cd .work/b1-datagen
/usr/lib/jvm/java-17-openjdk/bin/java \
  -DbundlerMainClass=net.minecraft.data.Main \
  -jar ../server-smoke/libraries/net/minecraft/server/1.20.1/server-1.20.1.jar \
  --reports --output ../b1-vanilla-reports
cd ../..
python3 tools/worldgen.py \
  --extra .work/server-smoke/libraries/net/minecraft/server/1.20.1-20230612.114412/server-1.20.1-20230612.114412-extra.jar \
  --report .work/b1-vanilla-reports/reports/biome_parameters/minecraft/overworld.json \
  --check
```

Ohne `--check` schreibt der Generator seine versionierten Ausgabedateien neu.
JAR und Bericht müssen vor der Generierung die gespeicherten SHA256 erfüllen.
Der optionale Integrationstest vergleicht **alle** generierten Bytes sowie alle
Noise-Settings-Felder außer den beabsichtigt geänderten Oberflächenregeln.
Ohne lokalen Vanilla-Cache wird nur dieser Test explizit übersprungen; die
übrigen Daten-/Exporttests brauchen weder Netzwerk noch Minecraft.

Nach persönlicher EULA-Annahme kann der Betreiber den neuen automatisierten
**Dedicated-Testpfad** ausführen:

```sh
python3 tools/worldgen_smoke.py \
  --java /usr/lib/jvm/java-17-openjdk/bin/java --accept-eula
```

Dieser Pfad ist **noch nicht runtime-verifiziert**. Er kopiert ausschließlich
Libraries aus dem alten Installationscache und hashgeprüfte Mods in ein exklusiv
neu erzeugtes `.work/worldgen-b1/<seed>`, startet nacheinander drei neue Welten
auf `127.0.0.1:25586–25588` und wartet pro Boot maximal 300 s.
Er protokolliert `Done`, Seed, Pakete, Oberflächenhöhe und Biom an drei
Koordinatenpaaren `(0,0)`, `(128,128)`, `(-128,-128)`.
Danach speichert und stoppt er sauber. Nur `Done`, drei nachgewiesene tote
Biom-Samples und Exit 0 ergeben einen bestandenen Smoke-Test. Wachstum bleibt
ein Clienttest mit Spieler: zwangsgeladene Chunks allein sind kein belastbarer
Nachweis natürlicher Random Ticks. Das ist kein Screenshot-, Wachstums-,
Survival-, Tierpopulations- oder umfangreicher Ressourcen-/Geografietest.
`console.log`, `result.json`, `logs/latest.log` und neue Saves bleiben lokal.
Ein existierendes Ausgabeziel wird abgelehnt; Wiederholungen brauchen
`--output .work/worldgen-b1-lauf2`. Keine Wiederverwendung vorhandener Server.

## Anschluss für dynamische Renaturierung

`pack/worldgen/biome-map.json`, Schema 1, enthält die vollständige bijektive
Zuordnung, z. B. `regenesis:dead_forest → minecraft:forest`. Die gespeicherte
Chunk-Biompalette hält damit den ursprünglichen Ökotyp auch nach Neustart fest.
Generator/Mapping und Seed gehören ins zukünftige Save-Backup; IDs nicht löschen.

Eine spätere kleine Forge-Mod kann zuerst persistente Umweltwerte pro Region
(Dimension + Chunk/Quartkoordinate + Schemaversion + ursprünglicher Biom-ID)
speichern und Blockregeneration mit einem Änderungsbudget durchführen. **Vor**
einem späteren Biomwechsel muss sie den ursprünglichen Ökotyp separat speichern;
ein Wechsel zu Vanilla-Biomen darf die Mappinginformation nicht verlieren.
Biome-Änderungen müssen Chunk-Paletten, Persistenz und Client-Synchronisation
berücksichtigen. Das ist ein Anschlussplan, keine implementierte API/Simulation.
Anpflanzungen funktionieren bereits ohne automatische Biomänderung; neue
Chunkgenerierung darf bereits restaurierte Bereiche nicht erneut abräumen.
