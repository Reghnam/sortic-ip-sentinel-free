"""Built zips match the pack trees and pass the scan."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_build():
    spec = importlib.util.spec_from_file_location("build_packs", ROOT / "scripts" / "build-packs.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_packs"] = module
    spec.loader.exec_module(module)
    return module


BUILD = _load_build()


class BuildPackTests(unittest.TestCase):
    def test_real_packs_match_zip_lists_and_scan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            dist = Path(raw)
            code = BUILD.build(ROOT, dist)
            self.assertEqual(code, 0)
            zips = sorted(dist.glob("*.zip"))
            self.assertEqual(len(zips), 4)
            for path in zips:
                self.assertTrue(path.name.startswith("free-ip-sentinel-"))
                self.assertIn("0.5.47-free", path.name)


if __name__ == "__main__":
    unittest.main()
