#!/usr/bin/env python3
"""Offline verification of cached locked JARs, nested hashes and TOML metadata (Python 3.11+)."""
import hashlib
import io
import json
from pathlib import Path
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def inspect(data, entry):
    if hashlib.sha256(data).hexdigest() != entry['sha256']:
        raise ValueError(f'Hash mismatch: {entry["filename"]}')
    with zipfile.ZipFile(io.BytesIO(data)) as jar:
        if jar.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        metadata = tomllib.loads(jar.read('META-INF/mods.toml').decode()) if 'META-INF/mods.toml' in jar.namelist() else {}
        ids = sorted(m['modId'] for m in metadata.get('mods', []))
        if ids != sorted(entry['mod_ids']):
            raise ValueError(f'Mod IDs differ: {entry["filename"]}')
        dependencies = {}
        for owner, records in metadata.get('dependencies', {}).items():
            for dep in records:
                dependencies[dep['modId']] = dep.get('versionRange', '')
        if dependencies != entry['dependencies']:
            raise ValueError(f'Dependency ranges differ: {entry["filename"]}')
        for child in entry.get('bundled_jars', []):
            inspect(jar.read(child['jar_path']), child)


def main():
    lock = json.loads((ROOT / 'pack/mods.lock.json').read_text())
    providers = {'minecraft', 'forge'}
    entries = []
    def collect(entry):
        entries.append(entry)
        providers.update(entry['mod_ids'])
        for child in entry.get('bundled_jars', []):
            collect(child)
    for entry in lock['mods']:
        collect(entry)
        inspect((ROOT / '.work/artifacts' / entry['filename']).read_bytes(), entry)
    for entry in entries:
        for dep in entry.get('dependency_details', []):
            if dep['mandatory'] and dep['mod_id'] not in providers:
                raise ValueError(f'Missing required provider: {dep["mod_id"]}')
    print(f'PASS: {len(lock["mods"])} parent JARs; {len(entries)} including nested JARs; hashes, CRC, declared IDs/ranges, required providers')
    print('Does not prove Maven version ordering, API compatibility, side safety or Minecraft boot.')


if __name__ == '__main__':
    main()
