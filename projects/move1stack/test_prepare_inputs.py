import importlib.util
import io
import stat
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare_inputs', Path(__file__).with_name('prepare-inputs.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArchiveSafety(unittest.TestCase):
    def archive(self, info):
        memory = io.BytesIO()
        with zipfile.ZipFile(memory, 'w') as archive:
            archive.writestr(info, b'input')
        memory.seek(0)
        return zipfile.ZipFile(memory)

    def test_safe_nested_file(self):
        with self.archive('assets/minecraft/model.json') as archive:
            self.assertEqual(len(module.safe_entries(archive)), 1)

    def test_traversal_and_platform_paths_are_rejected(self):
        for name in ['../escape', '/absolute', 'C:/drive', r'..\escape', 'control\nname']:
            with self.subTest(name=name), self.archive(name) as archive:
                with self.assertRaises(ValueError):
                    module.safe_entries(archive)

    def test_symlink_is_rejected(self):
        info = zipfile.ZipInfo('link')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.archive(info) as archive:
            with self.assertRaises(ValueError):
                module.safe_entries(archive)

    def test_expansion_limit_is_checked_before_extraction(self):
        with self.archive('entry') as archive:
            archive.infolist()[0].file_size = module.MAX_UNPACKED + 1
            with self.assertRaises(ValueError):
                module.safe_entries(archive)


if __name__ == '__main__':
    unittest.main()
