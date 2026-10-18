# Forge 1.20.1 artifact research (2026-10-18)

Branch: `feat/issue-1-forge-bootstrap`. This research report covers artifact downloads and static metadata inspection only. Separate process-start evidence is in [bootstrap-tests.md](bootstrap-tests.md) and [server-smoke-evidence.md](server-smoke-evidence.md). No existing server/world was modified.

## Selected downloadable artifacts

| Mod | Pinned release | Notes |
|---|---|---|
| Create | 6.0.8 | Required fixed candidate; Modrinth `mc1.20.1-6.0.8` |
| Ex Deorum | 1.53 | Latest Forge 1.20.1 release returned by Modrinth; no external mandatory mod dependency |
| Farmer's Delight | 1.2.11a | Latest published 1.2.x release, not 1.3.x; TOML runtime version `1.20.1-1.2.11a` |
| Vegan Delight | 1.4.0 | Required fixed publication `1.4.0-forge`; actual filename `vegandelight-1.4.jar`, runtime version `1.4`; not the 2.0 beta |
| KubeJS | 2001.6.5-build.26 | Required fixed candidate |
| Rhino | 2001.2.3-build.10 | Latest listed Forge 1.20.1 release; satisfies KubeJS `[2001.2.2-build.1,)` |
| Architectury API | 9.2.14 | Latest listed Forge 1.20.1 release; satisfies KubeJS and FTB minima |
| JEI | 15.56.0.205 | Latest Modrinth **release**, exceeds Create's `[15.19.0,)`; client installation policy |
| Jade | 11.13.3 | Latest listed Forge 1.20.1 release; installed on both sides for server-backed inspection |
| FTB Quests | 2001.4.22 | Required fixed candidate, official FTB Maven |
| FTB Library | 2001.2.9 | Matches Quests 2001.4.22 upstream build dependency |
| FTB Teams | 2001.3.0 | Matches Quests 2001.4.22 upstream build dependency |
| FTB XMod Compat | 2.1.3 | Optional integration explicitly listed in project modstack; KubeJS/JEI/Quests ranges satisfied |

FTB pairing evidence: https://raw.githubusercontent.com/FTBTeam/FTB-Quests/1.20.1/main/gradle.properties (saved locally as `research-FTB-Quests-gradle.properties`; declares mod_version=2001.4.22, ftb_library_version=2001.2.9, ftb_teams_version=2001.3.0). Newer FTB releases were not substituted merely because they exist. Selected Modrinth entries are all tagged `release`, Forge, and Minecraft 1.20.1.

## Embedded transitives — do not install separately

`bundled_jars` in each lock entry records exact paths, versions, SHA-256, Maven coordinates/ranges and nested `mods.toml` metadata. These are already delivered inside the downloaded parent, not extra top-level installer downloads.

- Create: Registrate `MC1.20-1.3.3` (GAMELIBRARY, no mod ID), Flywheel `1.0.5` (client dependency), Ponder `1.0.91`, MixinExtras Forge `0.4.1` (itself containing MixinExtras core `0.4.1`).
- KubeJS: MixinExtras Forge `0.2.0-rc.2` (itself containing MixinExtras core `0.2.0-rc.2`).
- Both MixinExtras Forge JarJar ranges admit `0.4.1`: Create `[0.4.1,)`, KubeJS `[0.2.0-rc.2,)`. Expected resolver candidate: 0.4.1; actual Forge JarJar behavior still needs a full runtime boot test.
- Item Filters, FTB Chunks/Ranks, LuckPerms, CraftTweaker, REI, Embeddium/Sodium are optional in the selected JARs and are not added.
- The exploratory JEI `15.71.0.224` download is a **beta and NOT locked**. It adds MezzConfig (embedded 0.6.6). Selected release 15.56.0.205 has no such dependency. Its exploratory JAR may remain in `.work/artifacts`; installers must use only lock filenames, never copy all research artifacts.

## Schema details for installer/tests

- `mods` lists the 13 downloadable artifacts. `side` is pack installation policy (`both` or `client`), not an inference that Forge metadata proves server safety.
- `dependencies` maps **all** dependency mod IDs to exact unmodified TOML version ranges, including optional dependencies. `dependency_details` preserves owner, mandatory flag, side and ordering so optional entries are not mistaken for required downloads.
- `mod_ids` describes mods directly provided by the artifact; embedded providers are described recursively in `bundled_jars`.
- `version` uses the selected human-facing release number. `source_version` retains Modrinth's publication identifier, `mod_versions` retains actual runtime versions (including resolution of Jade's `${file.jarVersion}` via MANIFEST.MF).
- `verification.minecraft_boot` is `not_run` in the original static research snapshot; the lock is an artifact pin set, **not** runtime evidence. The subsequent user-confirmed Java 17 client boot (18 displayed mods) and normal terrain generation are recorded separately in [bootstrap-tests.md](bootstrap-tests.md); no artifact pins changed.

## Validation actually executed

**Passed:**

1. Downloaded all 13 selected JARs using Python urllib; pinned SHA-256 computed over each complete downloaded file.
2. Compared all nine Modrinth artifacts against the API-provided SHA-1/SHA-512 hashes.
3. Compared all four FTB artifacts against their official Maven `.jar.sha256` files (`research-ftb-checksums.json`).
4. ZIP CRC checks and TOML parsing for all 13 parents plus seven recursively embedded JARs (`python3 .work/research-lock.py`).
5. Checked all JavaFML loader ranges against Forge 47.4.10. Checked 45 dependency edges whose targets are present, including optional installed pairings; all required dependency providers accounted for (`research-validation.json`). The bounded version comparator refuses unresolved qualifier comparisons rather than claiming to implement full Maven ComparableVersion; all selected checks resolve numerically.
6. Checked 8,404 base class headers across 20 parent/nested JARs: class major <=61 (Java 17). Multi-release `META-INF/versions/` overrides excluded by design (`research-bytecode.json`). This is bytecode-level evidence, not verification of every invoked Java API.

**Failed/recovered research requests:**

- Modrinth slugs `ftb-quests`, `ftb-library`, `ftb-teams`, `ftb-xmod-compat`: HTTP 404.
- Official Maven `.../maven-metadata.xml`: HTTP 403. The public Reposilite listing API `https://maven.ftb.dev/api/maven/details/releases/dev/ftb/mods/<artifact>` works; version listings saved in `research-*-listing.json`. Exact JAR and checksum URLs work.
- Initial static validator did not handle the embedded library wildcard loader range `*`; corrected validator, final run passed. No artifact version was changed to hide a range failure.

**Not run during this artifact research:** Minecraft/Forge client/server boot, Java runtime loading, JarJar runtime selection, recipe/API integration, rendering/quest functionality. No static declared dependency conflict remained. See [bootstrap-tests.md](bootstrap-tests.md) for subsequent process tests and the user-confirmed client boot; detailed integration checks remain open.

## License/download considerations

- All selected download URLs were accessible without API credentials; no unresolved artifact download blocker.
- All four FTB JARs declare `All Rights Reserved`. Official source URLs are recorded; JAR redistribution/rehosting permissions have **not** been established. Installer should fetch directly from manufacturer; do not commit/bundle JARs.
- Jade declares `CC BY-NC-SA 4.0`: attribution, non-commercial and share-alike constraints matter for redistribution.
- Create JAR declares MIT; Modrinth project labels a custom `LicenseRef-Create-Mod-License` and points to https://github.com/Creators-of-Create/Create/blob/HEAD/LICENSE.md. Do not treat the project-level license label as MIT or infer unrestricted redistribution without reviewing the actual shipped/source licenses and assets. Lock retains JAR-declared license verbatim.
- Other JAR-declared licenses are recorded in lock (MIT/LGPL/MPL/GPL etc.); embedded libraries also carry their inspected declarations. This inspection is not legal clearance for a redistribution bundle.
- `.work/`, JARs and generated ZIPs are ignored. No mod binaries are committed.

## Reproduction

Reproduce downloads from the committed lock and audit their bytes/metadata:

```sh
python3 tools/pack.py
python3 tools/audit_artifacts.py
```

`tools/audit_artifacts.py` checks hashes, ZIP CRCs, mod IDs, recorded dependency ranges and required providers. It does not implement Maven version ordering. The original range and bytecode research results are archived under `docs/evidence/`; the exploratory `.work/research-*` scripts are local research notes, not prerequisites for installation. Only install entries from `pack/mods.lock.json`, never the entire research cache.
