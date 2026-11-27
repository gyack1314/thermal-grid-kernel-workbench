"""检查资料能否被读取并保持原始字节身份。"""
import hashlib
from pathlib import Path
import tempfile
import unittest

from inspect_inputs import inventory


class InventoryTest(unittest.TestCase):
    def test_materials(self):
        root = Path(__file__).resolve().parents[1] / 'inputs'
        result = list(inventory(root))
        self.assertTrue(result)
        self.assertEqual(len(result), len({item['path'] for item in result}))
        self.assertTrue(any(item['path'].endswith('.json') for item in result))
        for item in result:
            raw = (root / item['path']).read_bytes()
            self.assertEqual(item['size'], len(raw))
            self.assertEqual(item['sha256'], hashlib.sha256(raw).hexdigest())

    def test_change_of_bytes_changes_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'station.json'
            path.write_bytes(b'{"id": 1}\n')
            before = next(inventory(root))['sha256']
            path.write_bytes(b'{"id": 1}\r\n')
            self.assertNotEqual(before, next(inventory(root))['sha256'])


if __name__ == '__main__':
    unittest.main()
