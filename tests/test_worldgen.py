import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
import zipfile

from test_pack import pack

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'pack/kubejs/data'


def read(path):
    return json.loads((DATA / path).read_text())


class WorldgenTests(unittest.TestCase):
    def setUp(self):
        self.mapping = json.loads((ROOT / 'pack/worldgen/biome-map.json').read_text())['biomes']
        self.preset = read('regenesis/worldgen/world_preset/dead_world.json')

    def test_climate_regions_are_bijective_and_preserved(self):
        self.assertEqual(len(self.mapping), 53)
        self.assertEqual(len(set(self.mapping.values())), 53)
        source = self.preset['dimensions']['minecraft:overworld']['generator']['biome_source']
        self.assertEqual(source['type'], 'minecraft:multi_noise')
        self.assertEqual(len(source['biomes']), 7593)
        self.assertEqual({b['biome'] for b in source['biomes']}, set(self.mapping))
        for entry in source['biomes']:
            self.assertEqual(set(entry['parameters']), {
                'temperature', 'humidity', 'continentalness', 'erosion', 'depth', 'weirdness', 'offset'})

    def test_only_opt_in_preset_and_structure_tags_touch_vanilla(self):
        paths = {p.relative_to(DATA / 'minecraft').as_posix() for p in (DATA / 'minecraft').rglob('*.json')}
        self.assertEqual(paths, {'tags/worldgen/world_preset/normal.json',
            'tags/worldgen/biome/has_structure/mineshaft.json',
            'tags/worldgen/biome/has_structure/mineshaft_mesa.json',
            'tags/worldgen/biome/has_structure/stronghold.json'})
        for name in paths:
            self.assertIs(read('minecraft/' + name)['replace'], False)
            self.assertTrue(read('minecraft/' + name)['values'])
        self.assertEqual(read('minecraft/tags/worldgen/world_preset/normal.json')['values'],
                         ['regenesis:dead_world'])
        # Growth safety: data definitions only, no scheduled functions or event hooks.
        files = list((ROOT / 'pack/kubejs').rglob('*'))
        self.assertFalse(any(p.suffix in {'.js', '.mcfunction'} for p in files))

    def test_dead_biomes_keep_minerals_carvers_without_ecological_spawns(self):
        for dead in self.mapping:
            with self.subTest(biome=dead):
                biome = read('regenesis/worldgen/biome/' + dead.split(':')[1] + '.json')
                self.assertEqual(biome['features'][9], [])
                self.assertNotIn('minecraft:disk_grass', biome['features'][6])
                self.assertIn('minecraft:ore_iron_upper', biome['features'][6])
                self.assertIn('minecraft:ore_diamond', biome['features'][6])
                self.assertIn('minecraft:cave', biome['carvers']['air'])
                for category, entries in biome['spawners'].items():
                    if category != 'monster':
                        self.assertEqual(entries, [])

    def test_create_minerals_are_scoped_to_dead_biomes(self):
        modifier = read('regenesis/forge/biome_modifier/dead_world_minerals.json')
        self.assertEqual(modifier, {'type': 'forge:add_features',
            'biomes': '#regenesis:dead_world', 'step': 'underground_ores',
            'features': ['create:zinc_ore', 'create:striated_ores_overworld']})
        tagged = read('regenesis/tags/worldgen/biome/dead_world.json')['values']
        self.assertEqual(set(tagged), set(self.mapping))

    def test_vanilla_terrain_density_and_resources_from_pinned_sources(self):
        extra = ROOT / '.work/server-smoke/libraries/net/minecraft/server/1.20.1-20230612.114412/server-1.20.1-20230612.114412-extra.jar'
        report = ROOT / '.work/b1-vanilla-reports/reports/biome_parameters/minecraft/overworld.json'
        if not extra.exists() or not report.exists():
            self.skipTest('Regenerate vanilla reports as documented in docs/worldgen-b1.md')
        spec = importlib.util.spec_from_file_location('worldgen', ROOT / 'tools/worldgen.py')
        worldgen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(worldgen)
        files, mapping = worldgen.build(extra, report)
        self.assertEqual(mapping, self.mapping)
        for name, data in files.items():
            self.assertEqual((ROOT / 'pack/kubejs' / name).read_bytes(), data, name)
        with zipfile.ZipFile(extra) as archive:
            vanilla = json.loads(archive.read('data/minecraft/worldgen/noise_settings/overworld.json'))
        dead = read('regenesis/worldgen/noise_settings/dead_overworld.json')
        for key in vanilla.keys() - {'surface_rule'}:
            self.assertEqual(dead[key], vanilla[key], key)

    def test_export_contains_exact_worldgen_bytes_and_no_saves(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / 'fixture.jar'
            artifact.write_bytes(b'fixture')
            outputs = [root / 'one.zip', root / 'two.zip']
            for output in outputs:
                with patch.object(pack, 'fetch', return_value=artifact), patch.object(sys, 'argv',
                        ['pack.py', '--output', str(output), '--cache', str(root / 'cache')]):
                    pack.main()
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            with zipfile.ZipFile(outputs[0]) as archive:
                for path in (ROOT / 'pack/kubejs').rglob('*.json'):
                    name = '.minecraft/kubejs/' + path.relative_to(ROOT / 'pack/kubejs').as_posix()
                    self.assertEqual(archive.read(name), path.read_bytes())
                self.assertFalse(any('/saves/' in n for n in archive.namelist()))


if __name__ == '__main__':
    unittest.main()
