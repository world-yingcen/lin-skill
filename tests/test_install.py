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

    def test_link_reads_source_changes_without_reinstall(self):
        m.install(self.root, self.base, mode='link')
        target = self.base / 'lin-frontend'
        self.assertTrue(target.is_symlink())
        (self.root / 'lin-frontend/SKILL.md').write_text('live edit')
        self.assertEqual((target / 'SKILL.md').read_text(), 'live edit')
        self.assertEqual(m.checked_manifest(self.root, self.base)['mode'], 'link')
        self.assertEqual(self.run_cli('--skill', 'lin-frontend', '--status'), 0)

    def test_copy_to_link_and_back_preserves_source(self):
        m.install(self.root, self.base)
        m.install(self.root, self.base, mode='link')
        self.assertTrue((self.base / 'lin-frontend').is_symlink())
        m.install(self.root, self.base, mode='copy')
        self.assertFalse((self.base / 'lin-frontend').is_symlink())
        self.assertEqual((self.root / 'lin-frontend/SKILL.md').read_text(), 'version 1')

    def test_link_conversion_rejects_edited_copy(self):
        m.install(self.root, self.base)
        (self.base / 'lin-frontend/SKILL.md').write_text('user edit')
        with self.assertRaises(RuntimeError):
            m.install(self.root, self.base, mode='link')
        self.assertEqual((self.base / 'lin-frontend/SKILL.md').read_text(), 'user edit')

    def test_wrong_and_broken_links_preserved(self):
        self.base.mkdir()
        target = self.base / 'lin-frontend'
        target.symlink_to(self.root / 'missing')
        with self.assertRaises(RuntimeError):
            m.install(self.root, self.base, mode='link', adopt=True)
        self.assertEqual(target.readlink(), self.root / 'missing')

    def test_link_rollback_does_not_delete_source(self):
        m.install(self.root, self.base, mode='link')
        record = (self.base / m.MANIFEST).read_bytes()
        with patch.object(m.os, 'replace', side_effect=OSError('failure')):
            with self.assertRaises(OSError):
                m.install(self.root, self.base, mode='link')
        self.assertTrue((self.base / 'lin-frontend').is_symlink())
        self.assertEqual((self.root / 'lin-frontend/SKILL.md').read_text(), 'version 1')
        self.assertEqual((self.base / m.MANIFEST).read_bytes(), record)

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

    def test_miffy_install_isolated_from_lin(self):
        (self.root / 'miffy/references').mkdir(parents=True)
        (self.root / 'miffy/SKILL.md').write_text('miffy version 1')
        m.install(self.root, self.base)
        lin_manifest = (self.base / m.MANIFEST).read_bytes()
        m.install(self.root, self.base, skill='miffy')
        (self.root / 'miffy/SKILL.md').write_text('miffy version 2')
        m.install(self.root, self.base, skill='miffy')
        self.assertEqual((self.base / 'miffy/SKILL.md').read_text(), 'miffy version 2')
        self.assertEqual((self.base / 'lin-frontend/SKILL.md').read_text(), 'version 1')
        self.assertEqual((self.base / m.MANIFEST).read_bytes(), lin_manifest)
        self.assertIsNotNone(m.checked_manifest(self.root, self.base, skill='miffy'))

    def test_miffy_local_edits_preserved(self):
        (self.root / 'miffy/references').mkdir(parents=True)
        (self.root / 'miffy/SKILL.md').write_text('miffy version 1')
        m.install(self.root, self.base, skill='miffy')
        p = self.base / 'miffy/SKILL.md'
        p.write_text('user changes')
        with self.assertRaises(RuntimeError):
            m.install(self.root, self.base, skill='miffy')
        self.assertEqual(p.read_text(), 'user changes')

    def bundle_source(self):
        (self.root / 'miffy/references').mkdir(parents=True)
        (self.root / 'miffy/SKILL.md').write_text('miffy version 1')

    def run_cli(self, *args):
        with patch.object(m, '__file__', str(self.root / 'install.py')), patch.object(
                m.sys, 'argv', ['install.py', '--target', str(self.base), *args]):
            return m.main()

    def test_default_cli_installs_both(self):
        self.bundle_source()
        self.assertEqual(self.run_cli(), 0)
        self.assertEqual((self.base / 'lin-frontend/SKILL.md').read_text(), 'version 1')
        self.assertEqual((self.base / 'miffy/SKILL.md').read_text(), 'miffy version 1')
        self.assertEqual(self.run_cli('--status'), 0)
        self.assertTrue((self.base / 'lin-frontend').is_symlink())
        self.assertTrue((self.base / 'miffy').is_symlink())

    def test_bundle_preflight_preserves_both_on_edited_copy(self):
        self.bundle_source()
        self.assertEqual(self.run_cli('--copy'), 0)
        (self.root / 'lin-frontend/SKILL.md').write_text('version 2')
        (self.base / 'miffy/SKILL.md').write_text('user changes')
        self.assertEqual(self.run_cli(), 1)
        self.assertEqual((self.base / 'lin-frontend/SKILL.md').read_text(), 'version 1')
        self.assertEqual((self.base / 'miffy/SKILL.md').read_text(), 'user changes')

    def test_bundle_update_checks_remote_once_and_keeps_default_selection(self):
        self.bundle_source()
        m.install(self.root, self.base)
        with patch.object(m, 'update_source') as update, patch.object(m.subprocess, 'call', return_value=0) as call:
            self.assertEqual(self.run_cli('--update'), 0)
            update.assert_called_once_with(self.root.resolve())
            self.assertNotIn('--skill', call.call_args.args[0])

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
