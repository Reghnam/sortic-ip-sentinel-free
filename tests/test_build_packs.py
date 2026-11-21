"""Built zips match the pack trees and pass the scan."""

from __future__ import annotations

import importlib.util
import io
import os
import re
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
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
            skill = BUILD.read_skill_name(ROOT / "claude-skill")
            names = {path.name for path in zips}
            self.assertIn(f"{skill}.zip", names)
            for path in zips:
                if path.name == f"{skill}.zip":
                    self.assertNotIn(edition, path.name)
                    continue
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
                members, skill_folder = BUILD.zip_members(pack, ROOT / pack)
                expected = sorted(members)
                archive = dist / BUILD.zip_name(pack, edition, skill_folder)
                with zipfile.ZipFile(archive) as zf:
                    self.assertEqual(zf.namelist(), expected)

    def test_claude_zip_has_no_root_file_and_one_name_folder(self) -> None:
        skill = BUILD.read_skill_name(ROOT / "claude-skill")
        prefix = skill + "/"
        with tempfile.TemporaryDirectory() as raw:
            dist = Path(raw)
            self.assertEqual(BUILD.build(ROOT, dist), 0)
            archive = dist / f"{skill}.zip"
            with zipfile.ZipFile(archive) as zf:
                names = zf.namelist()
            self.assertTrue(names)
            self.assertEqual([name for name in names if "/" not in name], [])
            self.assertEqual({name.split("/", 1)[0] for name in names}, {skill})
            for required in (
                "SKILL.md",
                "README.md",
                "LICENSE.md",
                "references/evals.md",
            ):
                self.assertIn(prefix + required, names)
            edition = _edition()
            for pack in BUILD._load_sync().read_packs(ROOT):
                if pack == "claude-skill":
                    continue
                other = dist / BUILD.zip_name(pack, edition)
                with zipfile.ZipFile(other) as zf:
                    others = zf.namelist()
                self.assertIn("SKILL.md", others)
                self.assertFalse(any(name.startswith(prefix) for name in others))

    def test_claude_frontmatter_keys_stay_inside_the_spec(self) -> None:
        allowed = {
            "name",
            "description",
            "license",
            "compatibility",
            "metadata",
            "allowed-tools",
        }
        text = (ROOT / "claude-skill" / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        block = text.split("---\n", 2)[1]
        keys = [
            line.split(":", 1)[0]
            for line in block.splitlines()
            if line and not line.startswith(" ") and ":" in line
        ]
        self.assertTrue(keys)
        self.assertEqual([key for key in keys if key not in allowed], [])

    def test_missing_and_inside_pattern_files_fail_closed(self) -> None:
        missing = BUILD.load_name_patterns(None, "/tmp/ips-missing-patterns-9f3a.txt", ROOT)
        self.assertFalse(missing.skipped)
        self.assertEqual(missing.errors, ["extra patterns file is missing"])
        inside = BUILD.load_name_patterns(str(ROOT / "patterns.txt"), None, ROOT)
        self.assertEqual(inside.errors, ["extra patterns file is inside the repo"])
        self.assertEqual(inside.patterns, [])

    def test_flag_wins_and_invalid_pattern_is_not_echoed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            outside = Path(raw)
            flag = outside / "flag.txt"
            env = outside / "env.txt"
            flag.write_text("# note\n\nzz-flag-token\n", encoding="utf-8")
            env.write_text("zz-env-token\n", encoding="utf-8")
            loaded = BUILD.load_name_patterns(str(flag), str(env), ROOT)
            self.assertFalse(loaded.skipped)
            self.assertEqual(loaded.errors, [])
            self.assertEqual(len(loaded.patterns), 1)
            self.assertIsNotNone(loaded.patterns[0].search("ZZ-FLAG-TOKEN"))
            self.assertIsNone(loaded.patterns[0].search("zz-env-token"))
            bad = outside / "bad.txt"
            bad.write_text("ok\n(\n", encoding="utf-8")
            rejected = BUILD.load_name_patterns(str(bad), None, ROOT)
            self.assertEqual(
                rejected.errors,
                ["extra patterns file: invalid regular expression on line 2"],
            )
            self.assertNotIn("(", " ".join(rejected.errors))

    def test_external_pattern_flags_member_without_echoing_text(self) -> None:
        phrase = "Not legal advice"
        with tempfile.TemporaryDirectory() as raw:
            outside = Path(raw)
            pattern_file = outside / "patterns.txt"
            pattern_file.write_text(phrase + "\n", encoding="utf-8")
            dist = outside / "dist"
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = BUILD.main(
                    ["--root", str(ROOT), "--dist", str(dist), "--extra-patterns", str(pattern_file)]
                )
            report = buf.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("extra-pattern #1: SKILL.md", report)
            self.assertNotIn(phrase, report)
            quiet = outside / "quiet.txt"
            quiet.write_text(r"zz-no-such-token-9f3a" + "\n", encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = BUILD.main(
                    ["--root", str(ROOT), "--dist", str(dist), "--extra-patterns", str(quiet)]
                )
            self.assertEqual(code, 0, buf.getvalue())
            self.assertNotIn("FAIL", buf.getvalue())

    def test_env_pattern_file_is_used_when_flag_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            outside = Path(raw)
            pattern_file = outside / "patterns.txt"
            pattern_file.write_text("zz-no-such-token-9f3a\n", encoding="utf-8")
            dist = outside / "dist"
            previous = os.environ.get("IPS_EXTRA_PATTERNS_FILE")
            os.environ["IPS_EXTRA_PATTERNS_FILE"] = str(pattern_file)
            try:
                buf = io.StringIO()
                with redirect_stdout(buf):
                    code = BUILD.main(["--root", str(ROOT), "--dist", str(dist)])
            finally:
                if previous is None:
                    os.environ.pop("IPS_EXTRA_PATTERNS_FILE", None)
                else:
                    os.environ["IPS_EXTRA_PATTERNS_FILE"] = previous
            self.assertEqual(code, 0, buf.getvalue())
            self.assertNotIn("skipped (no external file)", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
