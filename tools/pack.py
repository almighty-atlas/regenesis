#!/usr/bin/env python3
"""Hash-verified local Prism instance export; Python 3.11+, no third-party packages."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'pack/mods.lock.json'


def validate(lock):
    if (lock['schema_version'], lock['minecraft'], lock['forge'], lock['java']) != (1, '1.20.1', '47.4.10', 17):
        raise ValueError('Unexpected platform')
    names = set()
    for mod in lock['mods']:
        name = mod['filename']
        if Path(name).name != name or not name.endswith('.jar') or name in names:
            raise ValueError(f'Unsafe/duplicate filename: {name}')
        names.add(name)
        if mod['side'] not in ('both', 'client', 'server'):
            raise ValueError('Invalid side')
        if not mod['url'].startswith('https://'):
            raise ValueError('HTTPS required')
        if len(mod['sha256']) != 64 or any(c not in '0123456789abcdef' for c in mod['sha256']):
            raise ValueError('Invalid SHA-256')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(mod, cache):
    target = cache / mod['filename']
    if target.exists():
        if digest(target) != mod['sha256']:
            raise ValueError(f'Cache hash mismatch: {target}')
        return target
    request = urllib.request.Request(mod['url'], headers={'User-Agent': 'ReGenesis-bootstrap/0.1 (+https://github.com/almighty-atlas/regenesis)'})
    with tempfile.NamedTemporaryFile(dir=cache, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                while block := response.read(1024 * 1024):
                    handle.write(block)
            handle.close()
            if digest(temporary) != mod['sha256']:
                raise ValueError(f'Download hash mismatch: {mod["name"]}')
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate lock only; no network')
    parser.add_argument('--output', type=Path, default=ROOT / '.work/regenesis-phase-a.zip')
    parser.add_argument('--cache', type=Path, default=ROOT / '.work/artifacts')
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text())
    validate(lock)
    if args.check:
        print(f'PASS: platform and {len(lock["mods"])} artifact records; no runtime claim')
        return
    if args.output.exists():
        parser.error('Output already exists; choose a new --output (no overwrite)')
    args.cache.mkdir(parents=True, exist_ok=True)
    artifacts = [(m, fetch(m, args.cache)) for m in lock['mods'] if m['side'] != 'server']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Fixed ZIP timestamps and ordering make the same lock produce the same archive.
    with zipfile.ZipFile(args.output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        def put(name, data):
            archive.writestr(zipfile.ZipInfo(name, date_time=(2025, 1, 1, 0, 0, 0)), data)
        put('mmc-pack.json', json.dumps({'formatVersion': 1, 'components': [
            {'uid': 'net.minecraft', 'version': lock['minecraft'], 'important': True},
            {'uid': 'net.minecraftforge', 'version': lock['forge'], 'important': True}
        ]}, indent=2))
        put('instance.cfg', '[General]\nInstanceType=OneSix\nname=ReGenesis Phase A\nOverrideMemory=true\nMinMemAlloc=512\nMaxMemAlloc=4096\n')
        put('.minecraft/regenesis-mods.lock.json', LOCK.read_bytes())
        for mod, path in artifacts:
            put('.minecraft/mods/' + mod['filename'], path.read_bytes())
    print(f'Created {args.output}; {len(artifacts)} verified mods. LOCAL USE ONLY; do not redistribute archive.')


if __name__ == '__main__':
    main()
