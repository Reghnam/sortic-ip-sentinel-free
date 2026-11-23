"""Current-edition changelog read check. Warn-only unless strict mode is on."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
ROLLING = "docs/host-reads/ROLLING.md"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


HYGIENE = _load("check_hygiene_reads", SCRIPTS / "check-hygiene.py")
SYNC = _load("sync_packs_reads", SCRIPTS / "sync-packs.py")
BUILD = _load("build_packs_reads", SCRIPTS / "build-packs.py")


def _bad_tip() -> str:
    return "\n".join(
        (
            "## [9.9.9-free] — 2026-01-01",
            "",
            "### Later read — first",
            "",
            "- A functional line stays.",
            "",
            "### Later read — second",
            "",
            "- NOTIFY_BLOCKED",
            "",
            "### Prior read in this edition",
            "",
            "- returned no messages",
            "",
            "## [9.9.8-free] — 2025-12-01",
            "",
            "Gmail stays in an older edition.",
            "",
        )
    )


class ChangelogReadRuleTest(unittest.TestCase):
    def test_strict_mode_fails_on_second_heading_and_ops_phrase(self) -> None:
        findings = HYGIENE.changelog_read_findings(_bad_tip())
        self.assertTrue(any("2 Later read headings" in item for item in findings))
        self.assertTrue(any("Prior read headings" in item for item in findings))
        self.assertTrue(any("NOTIFY_BLOCKED" in item for item in findings))
        self.assertTrue(any("returned no messages" in item for item in findings))
        self.assertFalse(any(item.endswith(": Gmail") for item in findings))
        errors, warnings = HYGIENE.partition_changelog_findings(findings, strict=True)
        self.assertEqual(errors, findings)
        self.assertEqual(warnings, [])
        self.assertTrue(errors)

    def test_default_mode_keeps_the_exit_clear(self) -> None:
        findings = HYGIENE.changelog_read_findings(_bad_tip())
        errors, warnings = HYGIENE.partition_changelog_findings(findings, strict=False)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, findings)

    def test_bare_words_are_not_operator_phrases(self) -> None:
        text = "\n".join(
            (
                "## [9.9.9-free] — 2026-01-01",
                "",
                "### Later read — day",
                "",
                "- A backup is not a publish. An export is a paste.",
                "- A mail note is not a transcript. Drive is not a vault.",
                "",
            )
        )
        self.assertEqual(HYGIENE.changelog_read_findings(text), [])

    def test_line_cap_is_about_forty(self) -> None:
        cap = HYGIENE.CHANGELOG_READ_LINE_CAP
        self.assertEqual(cap, 40)

        def tip(extra: int) -> str:
            lines = ["## [9.9.9-free] — 2026-01-01", "", "### Later read — day"]
            lines.extend("- kept" for _ in range(extra))
            lines.append("## [9.9.8-free] — 2025-12-01")
            return "\n".join(lines) + "\n"

        # Heading plus (cap - 1) body lines is the cap. One more fails.
        self.assertEqual(HYGIENE.changelog_read_findings(tip(cap - 1)), [])
        over = HYGIENE.changelog_read_findings(tip(cap))
        self.assertEqual(len(over), 1)
        self.assertIn(f"is {cap + 1} lines", over[0])

    def test_cleaned_tip_passes_strict(self) -> None:
        text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        findings = HYGIENE.changelog_read_findings(text)
        errors, warnings = HYGIENE.partition_changelog_findings(findings, strict=True)
        self.assertEqual(findings, [])
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertTrue(HYGIENE.strict_changelog_enabled(True, None))
        self.assertTrue(HYGIENE.strict_changelog_enabled(False, "1"))
        self.assertFalse(HYGIENE.strict_changelog_enabled(False, None))
        self.assertFalse(HYGIENE.strict_changelog_enabled(False, "true"))

    def test_strict_cli_passes_on_cleaned_tip(self) -> None:
        env = os.environ.copy()
        env.pop("HYGIENE_STRICT_CHANGELOG", None)
        completed = subprocess.run(
            [sys.executable, "scripts/check-hygiene.py", "--strict-changelog"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("hygiene check OK:", completed.stdout)
        self.assertNotIn("changelog warning:", completed.stdout)

    def test_env_strict_cli_passes_on_cleaned_tip(self) -> None:
        env = os.environ.copy()
        env["HYGIENE_STRICT_CHANGELOG"] = "1"
        completed = subprocess.run(
            [sys.executable, "scripts/check-hygiene.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertNotIn("changelog warning:", completed.stdout)

    def test_rolling_file_is_outside_shipped_packs(self) -> None:
        path = ROOT / ROLLING
        self.assertTrue(path.is_file())
        self.assertNotIn(path.parts[-3], HYGIENE.PACKS)
        for pack in HYGIENE.PACKS:
            names = BUILD.pack_members(ROOT / pack)
            self.assertNotIn("ROLLING.md", names)
            self.assertFalse(any(name.endswith("ROLLING.md") for name in names))
        plan = SYNC.build_plan(ROOT)
        self.assertNotIn(ROLLING, plan.writes)
        self.assertNotIn(ROLLING, plan.deletes)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn(f"`{ROLLING}`", changelog)
        self.assertIn(f"`{ROLLING}`", contributing)
        self.assertIn("Do not record a host read in CHANGELOG.md.", changelog)
        self.assertIn("Do not record a host read in CHANGELOG.md.", contributing)
        self.assertEqual(HYGIENE.host_read_ops_findings(ROOT), [])

    def test_host_read_operator_phrase_is_named(self) -> None:
        findings = HYGIENE.operator_phrase_findings(
            ROLLING,
            "status line",
        )
        self.assertEqual(findings, [])
        findings = HYGIENE.operator_phrase_findings(ROLLING, "see NOTIFY_BLOCKED")
        self.assertEqual(findings, [f"{ROLLING} contains operator phrase: NOTIFY_BLOCKED"])


if __name__ == "__main__":
    unittest.main()
