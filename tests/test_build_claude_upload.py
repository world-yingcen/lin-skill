import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'scripts/build_claude_upload.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def baseline(self):
        source = self.root / 'source'
        shutil.copytree(ROOT / 'Lin-EVO/assets/evo-starter', source / 'assets/evo-starter')
        return source

    def test_missing_empty_file_is_rejected(self):
        source = self.baseline()
        (source / 'assets/evo-starter/06-切版/image/.gitkeep').unlink()
        with self.assertRaises(ValueError):
            builder.validate_baseline(source)

    def test_modified_baseline_is_rejected(self):
        source = self.baseline()
        (source / 'assets/evo-starter/06-切版/scss/_header.scss').write_text('changed')
        with self.assertRaises(ValueError):
            builder.validate_baseline(source)

    def test_extra_entry_is_rejected(self):
        (self.root / 'SKILL.md').write_text('entry')
        (self.root / 'nested').mkdir()
        (self.root / 'nested/SKILL.md').write_text('entry')
        with self.assertRaises(ValueError):
            builder.validate_links(self.root)

    def test_broken_and_external_local_links_are_rejected(self):
        for target in ('missing.md', '../outside.md'):
            (self.root / 'SKILL.md').write_text('[ref](' + target + ')')
            with self.assertRaises(ValueError):
                builder.validate_links(self.root)

    def test_existing_output_is_preserved(self):
        output = self.root / 'existing.zip'
        output.write_bytes(b'keep')
        with self.assertRaises(ValueError):
            builder.build(ROOT / 'Lin-EVO', output)
        self.assertEqual(output.read_bytes(), b'keep')

if __name__ == '__main__':
    unittest.main()
