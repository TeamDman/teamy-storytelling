"""Offline integration checks for reference setup and preservation of local work."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('setup_references', Path(__file__).resolve().parents[1] / 'scripts/setup-references.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class References(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.source = base / 'source'
        self.source.mkdir()
        setup.git(self.source, 'init', '--quiet')
        setup.git(self.source, 'config', 'user.name', 'Reference fixture')
        setup.git(self.source, 'config', 'user.email', 'fixture@example.invalid')
        (self.source / 'LICENSE').write_text('Synthetic license fixture\n')
        setup.git(self.source, 'add', 'LICENSE')
        setup.git(self.source, 'commit', '--quiet', '-m', 'fixture')
        self.entry = {'name': 'fixture', 'url': str(self.source),
                      'commit': setup.git(self.source, 'rev-parse', 'HEAD'),
                      'license_sha256': hashlib.sha256((self.source / 'LICENSE').read_bytes()).hexdigest()}
        self.root = base / 'references'

    def test_pin_and_offline_reuse(self):
        path = setup.ensure(self.root, self.entry)
        self.assertEqual(setup.git(path, 'rev-parse', 'HEAD'), self.entry['commit'])
        self.source.rename(self.source.with_name('unavailable'))
        self.assertEqual(setup.ensure(self.root, self.entry), path)
        self.assertEqual(setup.ensure(self.root, self.entry, True), path)

    def test_dirty_checkout_preserved(self):
        path = setup.ensure(self.root, self.entry)
        (path / 'notes.txt').write_text('keep my notes')
        with self.assertRaisesRegex(ValueError, 'local changes'):
            setup.ensure(self.root, self.entry)
        self.assertEqual((path / 'notes.txt').read_text(), 'keep my notes')

    def test_wrong_origin_and_revision_preserved(self):
        path = setup.ensure(self.root, self.entry)
        setup.git(path, 'remote', 'set-url', 'origin', 'https://example.invalid/unrelated')
        with self.assertRaisesRegex(ValueError, 'origin differs'):
            setup.ensure(self.root, self.entry)
        setup.git(path, 'remote', 'set-url', 'origin', self.entry['url'])
        with self.assertRaisesRegex(ValueError, 'revision differs'):
            setup.ensure(self.root, dict(self.entry, commit='0' * 40))
        self.assertEqual(setup.git(path, 'rev-parse', 'HEAD'), self.entry['commit'])

    def test_failed_fetch_leaves_no_partial_checkout(self):
        with self.assertRaises(subprocess.CalledProcessError):
            setup.ensure(self.root, dict(self.entry, commit='0' * 40))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_check_only_does_not_create_missing_root(self):
        with self.assertRaisesRegex(ValueError, 'missing'):
            setup.ensure(self.root, self.entry, True)
        self.assertFalse(self.root.exists())

    def test_license_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, 'license digest'):
            setup.ensure(self.root, dict(self.entry, license_sha256='0' * 64))
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
