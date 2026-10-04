"""Tree-level corpus rule. New pointer files are not on the legacy list."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import claim_rules  # noqa: E402
import zipscan  # noqa: E402


def _needle(prefix: str) -> str:
    return prefix + "-ip-law-" + "ground-truth"


class CorpusRuleTests(unittest.TestCase):
    def test_clean_tree_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "notes.md").write_text("hello\n", encoding="utf-8")
            errors, warnings = claim_rules.scan_corpus(root, zipscan.CORPUS_RE)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_legacy_file_warns(self) -> None:
        self.assertIn("SKILL.md", claim_rules.LEGACY_CORPUS_FILES)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "SKILL.md").write_text("see " + _needle("us") + "\n", encoding="utf-8")
            errors, warnings = claim_rules.scan_corpus(root, zipscan.CORPUS_RE)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("SKILL.md", warnings[0])
        self.assertIn("(1)", warnings[0])

    def test_new_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            folder = root / "references"
            folder.mkdir()
            (folder / "sme-fund-window.json").write_text(_needle("eu") + "\n", encoding="utf-8")
            errors, warnings = claim_rules.scan_corpus(root, zipscan.CORPUS_RE)
        self.assertEqual(warnings, [])
        self.assertTrue(
            any(error.startswith("corpus-ref in references/sme-fund-window.json:1") for error in errors)
        )

    def test_new_pointer_files_are_not_listed(self) -> None:
        for name in (
            "references/sme-fund-window.json",
            "references/sme-fund-pointer-and-intake.md",
            "scripts/claim_rules.py",
            "scripts/check-hygiene.py",
            ".github/workflows/sme-fund-freshness.yml",
        ):
            self.assertNotIn(name, claim_rules.LEGACY_CORPUS_FILES)
        for pack in ("chatgpt-skill", "claude-skill", "grok-skill", "cursor-skill"):
            self.assertNotIn(f"{pack}/references/sme-fund-window.json", claim_rules.LEGACY_CORPUS_FILES)
            self.assertNotIn(
                f"{pack}/references/sme-fund-pointer-and-intake.md",
                claim_rules.LEGACY_CORPUS_FILES,
            )

    def test_real_tree_warns_and_does_not_fail(self) -> None:
        errors, warnings = claim_rules.scan_corpus(ROOT, zipscan.CORPUS_RE)
        self.assertEqual(errors, [])
        self.assertGreater(len(warnings), 0)
        blob = "\n".join(errors + warnings)
        self.assertNotIn("scripts/check-hygiene.py", blob)


if __name__ == "__main__":
    unittest.main()
