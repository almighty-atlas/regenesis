#!/usr/bin/env python3
"""Opt-in B1 Forge tests in three EXCLUSIVELY NEW local worlds (no GUI test).

Requires the pinned Forge server libraries installed by tools/server_smoke.py.
Never starts, edits or reuses that server's world/configuration. No downloads.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

import pack
from server_smoke import terminate

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.20.1-47.4.10'
SEEDS = (3, 8675309, -20261018)


def run(java, directory):
    command = [str(java), '-Xmx3G',
               '@libraries/net/minecraftforge/forge/' + VERSION + '/unix_args.txt', 'nogui']
    report = {'command': command, 'done': False, 'biome_samples': {}}
    with (directory / 'console.log').open('xb') as log, (directory / 'console.log').open('rb') as reader:
        process = subprocess.Popen(command, cwd=directory, stdin=subprocess.PIPE,
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        pending = b''
        deadline = time.monotonic() + 300
        sample_deadline = None
        stopped = False

        def send(command):
            process.stdin.write((command + '\n').encode())
            process.stdin.flush()

        try:
            while True:
                pending += reader.read()
                lines = pending.split(b'\n')
                pending = lines.pop()
                for line in lines:
                    if b']: Done (' in line and not report['done']:
                        report['done'] = True
                        send('seed')
                        send('datapack list enabled')
                        for x, z in [(0, 0), (128, 128), (-128, -128)]:
                            send(f'forceload add {x} {z}')
                        sample_deadline = time.monotonic() + 15
                if sample_deadline is not None and time.monotonic() >= sample_deadline and not stopped:
                    # Allow the forceload tickets to generate before querying heights.
                    for x, z in [(0, 0), (128, 128), (-128, -128)]:
                        send(f'execute positioned {x} 0 {z} positioned over world_surface summon minecraft:marker run data get entity @s Pos')
                        for biome in json.loads((ROOT / 'pack/worldgen/biome-map.json').read_text())['biomes']:
                            send(f'execute positioned {x} 0 {z} positioned over world_surface if biome ~ ~-1 ~ {biome} run say B1_SAMPLE {x} {z} {biome}')
                    send('save-all flush')
                    send('stop')
                    stopped = True
                    deadline = time.monotonic() + 60
                if process.poll() is not None:
                    break
                if time.monotonic() > deadline:
                    raise TimeoutError('Worldgen startup/test/shutdown deadline exceeded')
                time.sleep(0.1)
        finally:
            terminate(process)
            process.stdin.close()
            report['exit_code'] = process.returncode
            evidence = (directory / 'console.log').read_bytes()
            report['biome_samples'] = {x.decode() + ',' + z.decode(): biome.decode()
                for x, z, biome in re.findall(
                    rb'B1_SAMPLE (-?\d+) (-?\d+) (regenesis:dead_\w+)', evidence)}
            report['passed'] = (report['done'] and len(report['biome_samples']) == 3
                                and stopped and process.returncode == 0)
            (directory / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, default=ROOT / '.work/server-smoke')
    parser.add_argument('--output', type=Path, default=ROOT / '.work/worldgen-b1')
    parser.add_argument('--accept-eula', action='store_true', help='Operator accepts https://aka.ms/MinecraftEULA')
    args = parser.parse_args()
    if not args.accept_eula:
        parser.error('Explicit personal --accept-eula required; no server started')
    if not args.java.is_absolute():
        parser.error('--java must be an absolute Java 17 path')
    java_version = subprocess.run([str(args.java), '-version'], capture_output=True, text=True, check=True)
    if not re.search(r'version "17[.\"]', java_version.stderr + java_version.stdout):
        parser.error('Java 17 required')
    runtime = args.runtime.resolve(strict=True)
    args.output.mkdir(parents=True, exist_ok=False)
    lock = json.loads(pack.LOCK.read_text())
    pack.validate(lock)
    for index, seed in enumerate(SEEDS):
        directory = args.output / str(seed)
        directory.mkdir()
        # Libraries are read-only inputs; no reuse of source worlds, mods or configs.
        shutil.copytree(runtime / 'libraries', directory / 'libraries')
        shutil.copytree(ROOT / 'pack/kubejs', directory / 'kubejs')
        shutil.copytree(ROOT / 'pack/config', directory / 'config')
        (directory / 'mods').mkdir()
        for mod in lock['mods']:
            if mod['side'] == 'client':
                continue
            artifact = ROOT / '.work/artifacts' / mod['filename']
            if pack.digest(artifact) != mod['sha256']:
                raise ValueError('Artifact SHA256 mismatch: ' + mod['filename'])
            shutil.copyfile(artifact, directory / 'mods' / mod['filename'])
        (directory / 'eula.txt').write_text('# Explicit operator --accept-eula\neula=true\n')
        (directory / 'server.properties').write_text(
            f'level-name=b1-test-world\nlevel-seed={seed}\nlevel-type=regenesis:dead_world\n'
            f'server-ip=127.0.0.1\nserver-port={25586 + index}\nonline-mode=true\n'
            'view-distance=2\nsimulation-distance=2\nspawn-protection=0\n')
        report = run(args.java, directory)
        print(json.dumps({'seed': seed, **report}), flush=True)
        if not report['passed']:
            raise RuntimeError(f'World test failed: {directory}/console.log')


if __name__ == '__main__':
    main()
