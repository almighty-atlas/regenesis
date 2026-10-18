#!/usr/bin/env python3
"""Rebuild B1 data from hash-pinned Minecraft 1.20.1 data and biome reports."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'pack/worldgen/sources.lock.json'
OUTPUT = ROOT / 'pack/kubejs'


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def dead_id(biome):
    return biome.replace('minecraft:', 'regenesis:dead_')


def build(extra, report):
    pins = json.loads(SOURCES.read_text())
    for path, key in [(extra, 'extra_sha256'), (report, 'biome_report_sha256')]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != pins[key]:
            raise ValueError(f'Unexpected vanilla source: {path}')
    parameters = json.loads(report.read_text())['biomes']
    originals = sorted({entry['biome'] for entry in parameters})
    mapping = {dead_id(b): b for b in originals}
    files = {}

    def put(name, data):
        files[name] = encode(data)

    with zipfile.ZipFile(extra) as archive:
        def read(name):
            return json.loads(archive.read('data/minecraft/' + name + '.json'))

        for original in originals:
            biome = read('worldgen/biome/' + original.split(':')[1])
            # VEGETAL_DECORATION only: no tick cancellation, growth or recipe changes.
            biome['features'][9] = []
            # Mangrove grass disks live in UNDERGROUND_ORES, outside that stage.
            biome['features'][6] = [feature for feature in biome['features'][6]
                                     if feature != 'minecraft:disk_grass']
            # Preserve hostile encounters, remove all ecological population categories.
            biome['spawners'] = {category: entries if category == 'monster' else []
                                 for category, entries in biome['spawners'].items()}
            biome['spawn_costs'] = {}
            biome['effects'].update(grass_color=0x77756B, foliage_color=0x77756B)
            put('data/regenesis/worldgen/biome/' + dead_id(original).split(':')[1] + '.json', biome)

        noise = read('worldgen/noise_settings/overworld')

        def transform(node):
            if isinstance(node, list):
                return [transform(value) for value in node]
            if not isinstance(node, dict):
                return node
            node = {key: transform(value) for key, value in node.items()}
            if node.get('type') == 'minecraft:biome':
                node['biome_is'] = [dead_id(b) for b in node['biome_is']]
            if node.get('type') == 'minecraft:block':
                state = node['result_state']
                if state['Name'] in {'minecraft:grass_block', 'minecraft:mycelium',
                                     'minecraft:podzol', 'minecraft:dirt', 'minecraft:mud'}:
                    node['result_state'] = {'Name': 'minecraft:gravel'}
            return node

        noise['surface_rule'] = transform(noise['surface_rule'])
        put('data/regenesis/worldgen/noise_settings/dead_overworld.json', noise)
        preset = read('worldgen/world_preset/normal')
        generator = preset['dimensions']['minecraft:overworld']['generator']
        generator['settings'] = 'regenesis:dead_overworld'
        generator['biome_source'] = {'type': 'minecraft:multi_noise', 'biomes': [
            dict(entry, biome=dead_id(entry['biome'])) for entry in parameters]}
        # One climate entry per line keeps this generated 7,593-entry table diffable.
        compact = copy.deepcopy(preset)
        compact['dimensions']['minecraft:overworld']['generator']['biome_source']['biomes'] = '__CLIMATE_TABLE__'
        rendered = encode(compact).decode().replace('"__CLIMATE_TABLE__"', '[\n' + ',\n'.join(
            '            ' + json.dumps(e, separators=(',', ':'))
            for e in generator['biome_source']['biomes']) + '\n          ]')
        files['data/regenesis/worldgen/world_preset/dead_world.json'] = rendered.encode()
        # Opt-in selectable preset; append without replacing the normal preset list.
        put('data/minecraft/tags/worldgen/world_preset/normal.json',
            {'replace': False, 'values': ['regenesis:dead_world']})
        # Only uninhabited underground structures. Do not inherit villages/outposts.
        def resolve_biomes(tag):
            result = set()
            for value in read('tags/worldgen/biome/' + tag)['values']:
                if value.startswith('#minecraft:'):
                    result.update(resolve_biomes(value.removeprefix('#minecraft:')))
                elif value in originals:
                    result.add(value)
            return result

        for tag in ['has_structure/mineshaft', 'has_structure/mineshaft_mesa', 'has_structure/stronghold']:
            put('data/minecraft/tags/worldgen/biome/' + tag + '.json',
                {'replace': False, 'values': sorted(dead_id(b) for b in resolve_biomes(tag))})

    for language, name in [('en_us', 'ReGenesis: The Dead World'), ('de_de', 'ReGenesis: Die tote Welt')]:
        put('assets/regenesis/lang/' + language + '.json', {'generator.regenesis.dead_world': name})
    put('data/regenesis/tags/worldgen/biome/dead_world.json', {'replace': False, 'values': sorted(mapping)})
    # IDs verified inside the pinned Create 6.0.8 JAR. Keep minerals without
    # is_overworld membership, which would also re-add Farmer's/Vegan Delight crops.
    put('data/regenesis/forge/biome_modifier/dead_world_minerals.json', {
        'type': 'forge:add_features', 'biomes': '#regenesis:dead_world',
        'features': ['create:zinc_ore', 'create:striated_ores_overworld'],
        'step': 'underground_ores'})
    return files, mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extra', type=Path, required=True, help='Vanilla server extra JAR from Forge installation')
    parser.add_argument('--report', type=Path, required=True, help='Vanilla --reports biome_parameters/minecraft/overworld.json')
    parser.add_argument('--check', action='store_true', help='Compare generated bytes; write nothing')
    args = parser.parse_args()
    files, mapping = build(args.extra, args.report)
    files['../worldgen/biome-map.json'] = encode({'schema_version': 1, 'biomes': mapping})
    for name, data in sorted(files.items()):
        path = OUTPUT / name
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f'Generated file differs: {path}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print(f'PASS: {len(mapping)} mapped biomes; {len(files)} reproducible files')


if __name__ == '__main__':
    main()
