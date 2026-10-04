"""Built zips match the pack trees and pass the scan."""

from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _edition() -> str:
    text = (ROOT / "scripts" / "check-hygiene.py").read_text(encoding="utf-8")
    match = re.search(r'^VERSION = "([^"]+)"', text, re.M)
    if not match:
        raise AssertionError("scripts/check-hygiene.py is missing VERSION")
    return match.group(1)


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
            edition = _edition()
            for path in zips:
                self.assertTrue(path.name.startswith("free-ip-sentinel-"))
                self.assertIn(edition, path.name)

    def test_two_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            first = base / "one"
            second = base / "two"
            self.assertEqual(BUILD.build(ROOT, first), 0)
            self.assertEqual(BUILD.build(ROOT, second), 0)
            names = sorted(path.name for path in first.glob("*.zip"))
            self.assertEqual(names, sorted(path.name for path in second.glob("*.zip")))
            self.assertEqual(len(names), len(BUILD._load_sync().read_packs(ROOT)))
            for name in names:
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())

    def test_zip_member_lists_match_pack_trees(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            dist = Path(raw)
            self.assertEqual(BUILD.build(ROOT, dist), 0)
            edition = _edition()
            for pack in BUILD._load_sync().read_packs(ROOT):
                expected = sorted(BUILD.pack_members(ROOT / pack))
                archive = dist / BUILD.zip_name(pack, edition)
                with zipfile.ZipFile(archive) as zf:
                    self.assertEqual(zf.namelist(), expected)


if __name__ == "__main__":
    unittest.main()
