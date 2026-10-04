"""Text checks for the weekly freshness workflow. No YAML library."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "sme-fund-freshness.yml"


class FreshnessWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_schedule_and_dispatch_only(self) -> None:
        self.assertIn("name: freshness", self.text)
        self.assertIn("schedule:", self.text)
        self.assertIn("cron:", self.text)
        self.assertIn("workflow_dispatch:", self.text)
        self.assertNotIn("push:", self.text)
        self.assertNotIn("pull_request:", self.text)
        cron = re.search(r'cron:\s*"([^"]+)"', self.text)
        self.assertIsNotNone(cron)
        minute = (cron.group(1) if cron else "").split()[0]
        self.assertNotEqual(minute, "0")

    def test_contents_read_is_the_only_permission(self) -> None:
        self.assertIn("permissions:", self.text)
        self.assertIn("contents: read", self.text)
        self.assertEqual(self.text.count("contents:"), 1)
        self.assertNotIn("issues: write", self.text)
        self.assertNotIn("secrets.", self.text)
        self.assertNotIn("pull-requests:", self.text)

    def test_no_write_or_network_steps(self) -> None:
        for banned in (
            "git push",
            "git commit",
            "gh ",
            "curl",
            "wget",
            "upload-artifact",
            "issues: write",
        ):
            self.assertNotIn(banned, self.text)

    def test_actions_are_pinned_by_version_tag(self) -> None:
        uses = re.findall(r"uses:\s*(\S+)", self.text)
        at = chr(64)
        self.assertEqual(
            uses,
            ["actions/checkout" + at + "v4", "actions/setup-python" + at + "v5"],
        )
        pin = at + "v"
        for item in uses:
            self.assertRegex(item, re.escape(pin) + r"\d+$")
            self.assertNotIn(chr(64) + "main", item)
            self.assertNotIn(chr(64) + "master", item)

    def test_step_runs_stored_date_only(self) -> None:
        self.assertIn("timeout-minutes:", self.text)
        self.assertIn("ubuntu-latest", self.text)
        self.assertIn('python-version: "3.12"', self.text)
        self.assertIn("name: Freshness (stored date only)", self.text)
        self.assertIn("python3 scripts/check-hygiene.py --freshness", self.text)


if __name__ == "__main__":
    unittest.main()
