"""Current-edition changelog read check. Warn-only unless strict mode is on."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
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
        self.assertTrue(any("3 day blocks" in item for item in findings))
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

    def test_day_blocks_ignore_heading_wording(self) -> None:
        stacked = "\n".join(
            (
                "## [9.9.9-free] — 2026-01-01",
                "",
                "### OpenAI (first)",
                "",
                "- one day",
                "",
                "### OpenAI (first)",
                "",
                "- another day",
                "",
                "## [9.9.8-free] — 2025-12-01",
                "",
            )
        )
        findings = HYGIENE.changelog_read_findings(stacked)
        self.assertTrue(any("2 day blocks" in item for item in findings))
        self.assertFalse(any("Later read" in item for item in findings))
        single = "\n".join(
            (
                "## [9.9.9-free] — 2026-01-01",
                "",
                "Substantive notes stay outside the day block.",
                "",
                "### Host read — 2026-01-02",
                "",
                "- one kept read",
                "",
                "## [9.9.8-free] — 2025-12-01",
                "",
            )
        )
        self.assertEqual(HYGIENE.changelog_read_findings(single), [])

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
        self.assertEqual(HYGIENE.operator_state_findings(ROOT), [])
        self.assertEqual(HYGIENE.host_read_findings(ROOT), [])
        self.assertEqual(HYGIENE.skill_byte_errors(ROOT), [])

    def test_operator_classes_match_run_state_and_not_rulings(self) -> None:
        positives = {
            "search": "Gmail search did not finish.",
            "export": "This run's grok-export did not finish.",
            "timeout": "This run's gmail search timed out.",
            "token refresh": "The token refresh did not finish.",
            "notify": "A blocked notify line was logged for this run.",
            "tool name": "conversation_search returned no messages.",
            "backup": "Our backup was marked PARTIAL.",
            "owner note": "No later owner note dated 21 or 22 Nov.",
            "unfinished mail": "Gmail and Drive did not finish.",
        }
        for label, sentence in positives.items():
            self.assertIn(label, HYGIENE.operator_class_labels(sentence), sentence)
        product = (
            "Does not email partners. Does not invent a Bot DM.",
            "Deck mail is not a transcript.",
            "A mailbox copy is not a transcript.",
            "grok-export PARTIAL (no conversation_search), public clip",
            "Dump the Grok chat export into the public skill.",
            "Drive title search timed out.",
            "A timeout deny is not a wipe.",
            "A token-refresh timeout is not a transcript.",
            "a memory snapshot is not a grok-export",
            "is NOTIFY_BLOCKED, not a publish",
            "No newer grok-export than W38.",
            "The missing later owner note wiped the hold.",
            "A tool list is not a limit.",
            "weekly backup without protect intent",
            "Changelog tip re-read 12 Oct is still 2.1.296 (9 Oct).",
        )
        for sentence in product:
            self.assertEqual(HYGIENE.operator_class_labels(sentence), [], sentence)
            self.assertFalse(HYGIENE.is_host_read_text(sentence), sentence)
        self.assertTrue(HYGIENE.is_host_read_text("is still 0.172.0 (23 Nov)"))
        self.assertFalse(HYGIENE.is_host_read_text("A later non-prerelease tag is the stable CLI."))

    def test_host_read_rule_exempts_only_rolling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rolling = root / "docs" / "host-reads"
            rolling.mkdir(parents=True)
            (rolling / "ROLLING.md").write_text(
                "is still 0.172.0 (23 Nov)\nGmail and Drive did not finish.\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "is still 0.172.0 (23 Nov)\n",
                encoding="utf-8",
            )
            (root / "EXEC-SUMMARY.md").write_text("Edition stays.\n", encoding="utf-8")
            (root / "LAUNCH.md").write_text("Public on GitHub.\n", encoding="utf-8")
            (root / "SKILL.md").write_text("No host log.\n", encoding="utf-8")
            (root / "references").mkdir()
            findings = HYGIENE.host_read_findings(root)
            self.assertTrue(any(item.startswith("README.md") for item in findings))
            self.assertFalse(
                any(item.startswith(f"{ROLLING}:") or item.startswith(f"{ROLLING} ") for item in findings)
            )
            operators = HYGIENE.operator_state_findings(root)
            self.assertTrue(any("ROLLING.md" in item and "unfinished mail" in item for item in operators))


if __name__ == "__main__":
    unittest.main()
