# Startzustand und Kapitel I–II (v0.4)

**Sämtliche Mengen sind Balancing-Zielwerte und keine existierenden Mod-Rezepte.** Eigene Items unten sind geplant, noch nicht registriert.

## Welt- und Startregeln

- Echte Overworld mit Höhenunterschieden und unterirdischen Strukturen; Oberfläche grau, kaum belebter Boden, keine natürlichen friedlichen Tier-Spawns.
- Start immer in einer versiegelten kleinen Forschungsstation; dort ist das letzte Lebensmaterial erhalten.
- Verlässliche Startkiste (kein Loot-RNG): 12 wiedergewonnene Planken, 8 staubige Steinbrocken, 2 sterile Erdböden, 1 Eichen-Setzling, 2 Kartoffeln, 1 Weizensamen, 1 Sojasamen, 12 konservierte rein pflanzliche Rationen, 2 kontaminierte Wasserproben und ein Forschungstagebuch. Die Items „Steinbrocken“, „steriler Boden“, „Wasserprobe“ und „Ration“ sind zunächst Konzept-/KubeJS-Items; wo es sich anbietet, Vanilla-Items verwenden.
- Erster Biozyklus ohne Tierprodukte und ohne Brennstoff. Holz kann als Bau- und Werkzeugmaterial dienen, **nicht** als frühe Verbrennungsabkürzung.
- Wasser aus der Welt kann fürs Bauen verfügbar sein; **nur aufbereitetes Wasser** zählt später für ökologische Quests. Für MVP keine Behauptung, dass Wasserflüssigkeiten physikalisch endlich sind.
- Nach Verlust jedes Starter-Items gibt es eine dokumentierte alternative Herstellung/Fundroute. Wiederholbare Rezepte müssen nachgewiesen werden, bevor Permadeath-/Hardcore-Modi angeboten werden.

## Kapitel I — Die Asche

| # | Quest und messbarer Abschluss | Geschätzter Input / Belohnung | Freischaltung |
|---|---|---|---|
| 1 | **Letzte Zuflucht:** Forschungstagebuch aufnehmen | Startvorräte finden | Questkarte und Wegweiser |
| 2 | **Wiederverwerten:** 16 Einheiten Schutt/Steinbrocken verarbeiten | Oberflächen- und Höhlenstein | Schuttrecycling |
| 3 | **Erste Werkzeuge:** Werkbank, Hammer, Sieb herstellen | Planken, Stein, wiederverwendbare Fasern | Ex-Deorum-Grundprozesse |
| 4 | **Metallspuren:** 4 Eisenfragmente durchs Sieben gewinnen | Sand/Kies/Staub, Sieb | Metallrecycling |
| 5 | **Licht ohne Kohle:** 4 regenerative Leuchtmittel platzieren | Aufbereitete biologische/mineralische Stoffe | sicherer Arbeitsraum |
| 6 | **Ein Tropfen Hoffnung:** 2 Wasserproben aufbereiten | Filtermaterial, kontaminierte Proben | erstes sauberes Wasser |
| 7 | **Boden statt Asche:** 4 Einheiten Kompost herstellen | Wiedergewonnene Biomasse | Substrat-Rezept |
| 8 | **Die Keimprobe:** Ersten Baum erfolgreich wachsen lassen | erhaltener Setzling, Boden, Wasser | Kapitel II |

**Hinweis:** Kapitel I soll keinen Stein-/Eisengenerator voraussetzen, der erst per Create erhältlich ist. Frühe Materialien müssen mit Handtools und Ex Deorum entstehen.

## Kapitel II — Ein Funke Leben

| # | Quest und messbarer Abschluss | Voraussetzung | Freischaltung |
|---|---|---|---|
| 1 | **Mehr als ein Setzling:** mindestens 4 neue Setzlinge gewinnen | erster Baum | erneuerbares Holz |
| 2 | **Pflanzenfaser:** 16 Fasern aus Blättern/Pflanzen gewinnen | erneuerbarer Pflanzenbestand | Seile, Netze, Textilien |
| 3 | **Fruchtbarer Boden:** 16 Erde/Substrat erzeugen | Kompostierung | erster Garten |
| 4 | **Nahrungskreislauf:** 16 Kartoffeln oder gleichwertige Pflanzennahrung ernten | Garten | selbsterhaltende Nahrung |
| 5 | **Pflanzenvielfalt:** drei nutzbare Pflanzenarten erfolgreich vermehren | Saatgutarchiv | Saatgutvermehrung |
| 6 | **Kompostkreislauf:** 8 Pflanzenreste verwerten und daraus erneut Erde herstellen | Biomasse | verbesserte Bodenkosten |
| 7 | **Handkraft zu Windkraft:** erste Create-Windmühle bauen | Ex-Deorum-Metalle, Holz, Create | Rotationsenergie |
| 8 | **Wasser zurückgewinnen:** 8 Wasserproben aufbereiten und 4 Filter regenerieren | Wasserfilter | Wasserkreislauf I |
| 9 | **Die erste Oase:** ein 16×16-Testgebiet mit Erde und drei Pflanzenarten begrünen | Pflanzen- und Wasserzyklus | Regional-Ökologie-Demo |
| 10 | **Ein selbsttragender Anfang:** Oase nach Laden/Neustart stabil | Region gespeichert | Kapitel III vorbereitet |

Der Oasentest darf im ersten Build zunächst auf sichtbaren Blockänderungen beruhen. **Echte autonome Regionsausbreitung** ist erst mit der zusätzlichen ReGenesis-Mod als erfüllt zu markieren.

## Vorgesehene Rezeptketten (nicht als gültige JEI-Rezepte ausgegeben)

| Rezept-ID / Endprodukt | Designrezept | Quelle und Sinn |
|---|---|---|
| Pflanzenfaser (`regenesis:plant_fiber`) | 1 Blattblock → 2 Fasern | vermeidet Spinnenfarmen/Tierprodukte |
| Filterschicht (`regenesis:filter_media`) | 2 Kies + 1 Sand + 2 Pflanzenfasern → 1 | regenerierbares Frühspiel-Filtermaterial |
| Aufbereitetes Wasser (`regenesis:clean_water_sample`) | 1 kontaminierte Probe + Filterkapazität → 1 sauber | eigenes Testitem, **kein Vanilla-Flüssigkeitsersatz** |
| Kompost (`regenesis:compost`) | 4 Pflanzenreste → 1 Kompost | Ex-Deorum-Fass oder KubeJS-Datenrezept |
| Gartensubstrat (`regenesis:fertile_substrate`) | 2 Kompost + 1 mineralischer Staub → 1 Substrat | veganer Pflanzenkreislauf |
| Pflanzengewebe (`regenesis:plant_fabric`) | 4 Pflanzenfasern → 1 Gewebe | alternative Netze/Bett-/Maschinenmaterialien |
| Mineralische Leuchtpaste (`regenesis:phosphor_paste`) | mineralisches Pulver + kultivierte Pilze → 1 | technische Alternative zu Kohletorches |
| Filterschicht regenerieren | verbrauchter Filter + Sand + Wasserbehandlung → 1 Filter | Materialkreislauf statt Einmalfilter |

**Bei Rezeptumsetzung:** Exakte Item IDs, Mengen, Container-Rückgaben, Tags, Kompatibilität mit JEI und Herstellungsstationen erst aus installierten Mod-Daten abgleichen. Insbesondere müssen alle Startmaterialien ohne einmalige Questbelohnungen langfristig beschaffbar sein.

## Vermeidung von Progressions-Sackgassen

- Setzling verloren: garantierter zweiter Seed-Vault oder regenerierbare Pflanzenprobe über Forschungsstation.
- Wasserprobe verloren: wiederholbare Probenahme aus natürlichem kontaminiertem Wasser/Schmelzwasser/Untergrundquelle.
- Erde verloren: Sand/Kies/Staub + Biomasse erlauben neue Erde; alternative Biomasse-/Sporenquelle für Totalausfall.
- Kein Eisenerz: Sieb-Rezepte liefern reproduzierbare Metallfragmente (Rate per Messung balancieren).
- Kein Brennstoff: weder Kiste noch Modrezept fordert Kohle oder Holzkohle für den ersten Windantrieb.
- Keine Tier-Rohstoffe: Faser statt String, Pilz-/Pflanzenleder statt Leder, Kompost statt Knochenmehl, pflanzliche Nahrung.

## Übergang zu Kapitel III

Nach Kapitel II folgt erst **gereinigtes Wasser als Infrastruktur**, anschließend elektromechanische Pumpen, Gewässerrenaturierung und die Wiederansiedlung erster überlebender Bestäuber. DNA-Rekonstruktion kommt bewusst später.
