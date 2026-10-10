import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'install.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.base = Path(self.tmp.name) / 'skills'
        (self.root / 'lin-frontend/references').mkdir(parents=True)
        (self.root / 'lin-frontend/SKILL.md').write_text('version 1')

    def test_install_update_and_no_backup(self):
        m.install(self.root, self.base)
        (self.root / 'lin-frontend/SKILL.md').write_text('version 2')
        m.install(self.root, self.base)
        self.assertEqual((self.base / 'lin-frontend/SKILL.md').read_text(), 'version 2')
        self.assertEqual(sorted(x.name for x in self.base.iterdir()), [m.MANIFEST, 'lin-frontend'])

    def test_local_edits_preserved(self):
        m.install(self.root, self.base)
        p = self.base / 'lin-frontend/SKILL.md'
        p.write_text('user changes')
        with self.assertRaises(RuntimeError):
            m.install(self.root, self.base)
        self.assertEqual(p.read_text(), 'user changes')

    def test_unknown_copy_and_adopt(self):
        import shutil
        shutil.copytree(self.root / 'lin-frontend', self.base / 'lin-frontend')
        with self.assertRaises(RuntimeError):
            m.install(self.root, self.base)
        m.install(self.root, self.base, adopt=True)

    def test_adopt_rejects_difference(self):
        (self.base / 'lin-frontend').mkdir(parents=True)
        (self.base / 'lin-frontend/SKILL.md').write_text('different')
        with self.assertRaises(RuntimeError):
            m.install(self.root, self.base, adopt=True)

    def test_dry_run_does_not_write(self):
        m.install(self.root, self.base, dry_run=True)
        self.assertFalse(self.base.exists())

    def fake_git(self, dirty='', ahead='0', remote=None, fail_fetch=False):
        def run(root, *args):
            if args == ('rev-parse', '--show-toplevel'): return str(self.root)
            if args[:2] == ('remote', 'get-url'): return remote or next(iter(m.REMOTES))
            if args == ('branch', '--show-current'): return 'main'
            if args == ('status', '--porcelain'): return dirty
            if args[0] == 'fetch' and fail_fetch: raise subprocess.TimeoutExpired('git', 60)
            if args[0] == 'rev-list': return ahead
            return ''
        return run

    def test_dirty_repo_no_fetch(self):
        with patch.object(m, 'git', side_effect=self.fake_git(dirty=' M file')) as g:
            with self.assertRaises(RuntimeError): m.update_source(self.root)
            self.assertFalse(any(c.args[1] == 'fetch' for c in g.call_args_list))

    def test_divergence_no_merge(self):
        with patch.object(m, 'git', side_effect=self.fake_git(ahead='1')) as g:
            with self.assertRaises(RuntimeError): m.update_source(self.root)
            self.assertFalse(any(c.args[1] == 'merge' for c in g.call_args_list))

    def test_wrong_remote(self):
        with patch.object(m, 'git', side_effect=self.fake_git(remote='wrong')):
            with self.assertRaises(RuntimeError): m.update_source(self.root)

    def test_offline_no_merge(self):
        with patch.object(m, 'git', side_effect=self.fake_git(fail_fetch=True)) as g:
            with self.assertRaises(subprocess.TimeoutExpired): m.update_source(self.root)
            self.assertFalse(any(c.args[1] == 'merge' for c in g.call_args_list))

    def test_ff_only(self):
        with patch.object(m, 'git', side_effect=self.fake_git()) as g:
            m.update_source(self.root)
            g.assert_any_call(self.root, 'merge', '--ff-only', 'origin/main')


if __name__ == '__main__': unittest.main()
