# Dedicated-Server-Diagnose – 2026-10-18

**Forge-Installation bestanden; echter Pre-EULA-Prozessstart ausgeführt;
vollständiger Server-Boot blockiert. Kein Nachweis der Laufzeitkompatibilität.**

## Ausführung

Umgebung: Linux amd64, OpenJDK `17.0.20.1+1`, Python 3.14.8.
Vom Repository-Wurzelverzeichnis:

```sh
python3 tools/pack.py
python3 tools/server_smoke.py --java /usr/lib/jvm/java-17-openjdk/bin/java
```

Interne Kommandos, ausschließlich in neuem `.work/server-smoke`:

```sh
/usr/lib/jvm/java-17-openjdk/bin/java -jar forge-1.20.1-47.4.10-installer.jar --installServer
/usr/lib/jvm/java-17-openjdk/bin/java -Xmx3G @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.20.1-47.4.10/unix_args.txt nogui
```

- Installer: Exit **0**, `The server installed successfully`.
- Serverprozess: Exit **0** nach **2,50 s**, endet mit EULA-Hinweis.
- Diagnoseläufer: Exit **2**, `blocked_eula`; dies ist **kein bestandener Boot**.
- `eula=false`; kein `Done`, keine Welt erzeugt. Kein Crash im ausgeführten Pfad.
- Die EULA wurde nicht stellvertretend angenommen. `--accept-eula` wurde nicht verwendet.
- Abweichend von der geplanten Reihenfolge „Client zuerst“ wurde nur dieser isolierte
  Pre-EULA-Diagnoselauf vorgezogen; er ersetzt keinen Client- oder Server-Abnahmetest.

Vollständige Serverkonsole: [`evidence/server-pre-eula.log`](evidence/server-pre-eula.log).
Warnungen zu Forge-Core-Libraries ohne `mods.toml` sowie Erstanlage von `fml.toml`
sind im Log erhalten. Sie waren im ausgeführten Pfad nicht fatal; spätere Fehler
bei Modinitialisierung sind damit nicht ausgeschlossen.

## Pins und Isolation

`pack/platform.lock.json` enthält URL, SHA256 und separat vom Hersteller
verglichene SHA1 des Forge-Installers. SHA1 ist kein Signaturnachweis.
Alle zwölf `both`-Modartefakte wurden gegen `pack/mods.lock.json` geprüft und
kopiert; JEI bleibt clientseitig. Create-interne JARs werden nicht separat installiert.
Lock-Snapshot-SHA256: `46e59cbb89f5068403afd59b90491b310b30bac19338798280b0c0d1b6ea3ae5`.

Der Läufer lehnt vorhandene Testziele ab und beendet nur seine eigenen
Prozessgruppen. Grenzen: Downloadbudget 120 s plus Sockettimeout bis 30 s,
Installer 600 s, Serverstart 240 s, Shutdown 60 s.

```properties
level-name=smoke-world
server-ip=127.0.0.1
server-port=25585
view-distance=2
simulation-distance=2
online-mode=true
spawn-protection=0
```

Lokale Zusatzbelege (nicht im Git): `.work/server-smoke/result.json`,
`installer-console.log`, `logs/latest.log`, `mods.lock.snapshot.json`, `eula.txt`.
Bestehende Minecraft-Server oder Welten wurden nicht verändert.

## Fehlversuch und Wiederholung

Erster SHA1-Abruf: HTTP 403 ohne expliziten User-Agent. Mit
`ReGenesis-Server-Smoke/1.0` erfolgreich; keine Modversion gewechselt.
Fehlversuch erhalten unter `.work/server-smoke-network-attempt`.

**Nicht durchgeführt:** vollständiger Boot bis `Done`, Stoppen nach `Done`,
Weltgenerierung, Clientverbindung, Persistenz, Timeout-/Kill-Pfade und der
EULA-Opt-in-Pfad. Für einen späteren echten Test muss der Betreiber zuerst die
EULA lesen und selbst zustimmen. Danach vorhandenen Belegordner selbst archivieren
(der Läufer überschreibt ihn nicht) und optional ausführen:

```sh
python3 tools/server_smoke.py --java /ABSOLUTER/PFAD/ZU/java17 --accept-eula
```
