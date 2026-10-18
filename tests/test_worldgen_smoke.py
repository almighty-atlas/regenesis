import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location('worldgen_smoke', TOOLS / 'worldgen_smoke.py')
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class WorldgenSmokeSafetyTests(unittest.TestCase):
    def test_no_eula_consent_never_creates_output_or_launches_java(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'new-server'
            with patch.object(sys, 'argv', ['worldgen_smoke.py', '--java', '/absent/java',
                                          '--output', str(output)]), \
                 patch.object(smoke.subprocess, 'run', side_effect=AssertionError('Java started')):
                with self.assertRaises(SystemExit) as error:
                    smoke.main()
            self.assertEqual(error.exception.code, 2)
            self.assertFalse(output.exists())

    def test_existing_output_is_preserved_without_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'existing-server'
            output.mkdir()
            marker = output / 'do-not-touch.txt'
            marker.write_text('existing world sentinel')
            version = subprocess.CompletedProcess([], 0, '', 'openjdk version "17.0.1"')
            with patch.object(sys, 'argv', ['worldgen_smoke.py', '--java', '/fake/java',
                     '--runtime', directory, '--output', str(output), '--accept-eula']), \
                 patch.object(smoke.subprocess, 'run', return_value=version), \
                 patch.object(smoke, 'run', side_effect=AssertionError('Server started')):
                with self.assertRaises(FileExistsError):
                    smoke.main()
            self.assertEqual(marker.read_text(), 'existing world sentinel')
            self.assertEqual(list(output.iterdir()), [marker])


if __name__ == '__main__':
    unittest.main()
