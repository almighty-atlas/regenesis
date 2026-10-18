import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pack_tool', ROOT / 'tools/pack.py')
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


class PackTests(unittest.TestCase):
    def setUp(self):
        self.lock = json.loads(pack.LOCK.read_text())

    def test_lock(self):
        pack.validate(self.lock)
        self.assertEqual(len(self.lock['mods']), 13)
        self.assertEqual(self.lock['verification']['minecraft_boot'], 'not_run')

    def test_reject_bad_records(self):
        for field, value in [('filename', '../bad.jar'), ('sha256', '0' * 63),
                             ('url', 'http://example.org/a.jar'), ('side', 'unknown')]:
            with self.subTest(field=field):
                lock = copy.deepcopy(self.lock)
                lock['mods'][0][field] = value
                with self.assertRaises(ValueError):
                    pack.validate(lock)
        self.lock['mods'].append(self.lock['mods'][0])
        with self.assertRaises(ValueError):
            pack.validate(self.lock)

    def test_corrupt_cache_fails_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            mod = self.lock['mods'][0]
            (cache / mod['filename']).write_bytes(b'corrupt')
            with patch('urllib.request.urlopen', side_effect=AssertionError('network')):
                with self.assertRaisesRegex(ValueError, 'Cache hash mismatch'):
                    pack.fetch(mod, cache)

    def test_failed_download_not_published(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            with patch('urllib.request.urlopen', side_effect=OSError('network failure')):
                with self.assertRaises(OSError):
                    pack.fetch(self.lock['mods'][0], cache)
            self.assertEqual(list(cache.iterdir()), [])

    def test_archive_reproducible_and_exact(self):
        # Integration test uses only already fetched local artifacts.
        cache = ROOT / '.work/artifacts'
        if not all((cache / mod['filename']).exists() for mod in self.lock['mods']):
            self.skipTest('Download artifacts with python3 tools/pack.py first')
        with tempfile.TemporaryDirectory() as directory:
            outputs = [Path(directory) / f'{n}.zip' for n in range(2)]
            for output in outputs:
                subprocess.run([sys.executable, str(ROOT / 'tools/pack.py'),
                                '--output', str(output)], check=True, capture_output=True)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            with zipfile.ZipFile(outputs[0]) as archive:
                for mod in self.lock['mods']:
                    if mod['side'] != 'server':
                        data = archive.read('.minecraft/mods/' + mod['filename'])
                        self.assertEqual(hashlib.sha256(data).hexdigest(), mod['sha256'])
                jars = [name for name in archive.namelist() if name.endswith('.jar')]
                self.assertEqual(len(jars), 13)
                platform = json.loads(archive.read('mmc-pack.json'))
                self.assertEqual(platform['components'][1]['version'], '47.4.10')
            result = subprocess.run([sys.executable, str(ROOT / 'tools/pack.py'),
                                     '--output', str(outputs[0])], capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
