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

    def test_actions_are_pinned_to_full_shas(self) -> None:
        uses = re.findall(r"uses:\s*(\S+)", self.text)
        at = chr(64)
        checkout = "11d5960a326750d5838078e36cf38b85af677262"
        setup = "a26af69be951a213d495a4c3e4e4022e16d87065"
        self.assertEqual(
            uses,
            ["actions/checkout" + at + checkout, "actions/setup-python" + at + setup],
        )
        for item in uses:
            self.assertRegex(item, re.escape(at) + r"[0-9a-f]{40}$")
            self.assertNotIn(at + "main", item)
            self.assertNotIn(at + "master", item)
            self.assertNotRegex(item, re.escape(at) + r"v\d")
        self.assertIn("# v4.4.0", self.text)
        self.assertIn("# v5.6.0", self.text)
        self.assertIn("persist-credentials: false", self.text)

    def test_step_runs_stored_date_only(self) -> None:
        self.assertIn("timeout-minutes:", self.text)
        self.assertIn("ubuntu-latest", self.text)
        self.assertIn('python-version: "3.12"', self.text)
        self.assertIn("name: Freshness (stored date only)", self.text)
        self.assertIn("python3 scripts/check-hygiene.py --freshness", self.text)


if __name__ == "__main__":
    unittest.main()
