"""Text checks for the hygiene workflow. No YAML library."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "hygiene-check.yml"
ARCHIVE_SHA256 = "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
ZERO_SHA = "0000000000000000000000000000000000000000"


class HygieneWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_push_and_pull_request_only(self) -> None:
        self.assertIn("name: hygiene-check", self.text)
        self.assertIn("push:", self.text)
        self.assertIn("pull_request:", self.text)
        self.assertNotIn("pull_request_target:", self.text)
        self.assertNotIn("workflow_dispatch:", self.text)

    def test_contents_read_is_the_only_permission(self) -> None:
        self.assertIn("permissions:", self.text)
        self.assertIn("contents: read", self.text)
        self.assertEqual(self.text.count("contents:"), 1)
        self.assertNotIn("secrets.", self.text)
        self.assertNotIn("GITLEAKS_LICENSE", self.text)
        self.assertNotIn("issues: write", self.text)
        self.assertNotIn("pull-requests:", self.text)

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
        self.assertNotIn("gitleaks-action", self.text)

    def test_zip_scan_runs_and_is_not_uploaded(self) -> None:
        self.assertIn("name: Zip scan", self.text)
        self.assertIn("python3 scripts/build-packs.py", self.text)
        self.assertNotIn("upload-artifact", self.text)
        self.assertNotIn("actions/upload-artifact", self.text)

    def test_secret_scan_checks_the_pinned_archive(self) -> None:
        self.assertIn("name: Secret scan", self.text)
        self.assertIn(f'ARCHIVE_SHA256: "{ARCHIVE_SHA256}"', self.text)
        self.assertIn("sha256sum -c -", self.text)
        self.assertIn('version="8.30.1"', self.text)
        self.assertIn("gitleaks_${version}_linux_x64.tar.gz", self.text)
        self.assertIn('"${tool}" dir .', self.text)
        self.assertIn("--log-opts=", self.text)
        self.assertNotIn("--all", self.text)
        self.assertNotIn(".gitleaksignore", self.text)
        self.assertNotIn("allowlist", self.text)
        self.assertIn(ZERO_SHA, self.text)
        self.assertIn("push range skipped", self.text)
        self.assertIn("${BASE_SHA}..${HEAD_SHA}", self.text)
        self.assertIn("${BEFORE_SHA}..${AFTER_SHA}", self.text)


if __name__ == "__main__":
    unittest.main()
