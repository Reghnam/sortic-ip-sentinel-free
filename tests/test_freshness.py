"""Stored-date freshness. A null date fails this mode and passes the normal run."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import claim_rules  # noqa: E402

TODAY = date(2026, 10, 4)
WINDOW = ROOT / "references" / "sme-fund-window.json"
OK_LINE = (
    "hygiene check OK: 0.5.49-free; description 1018 chars; "
    "body 501 lines; 18 references; 189 evals"
)


def baseline() -> dict:
    data, error = claim_rules.parse_window_text(WINDOW.read_text(encoding="utf-8"))
    if error or not isinstance(data, dict):
        raise AssertionError(error)
    return data


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "check-hygiene.py"), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


class FreshnessTests(unittest.TestCase):
    def test_null_fails_freshness(self) -> None:
        problems = claim_rules.freshness_problems(baseline(), TODAY)
        self.assertTrue(any("not set" in problem for problem in problems))

    def test_age_limits(self) -> None:
        for days, ok in ((13, True), (14, True), (15, False)):
            data = baseline()
            data["last_verified"] = (TODAY - timedelta(days=days)).isoformat()
            data["stale_after_days"] = 14
            problems = claim_rules.freshness_problems(data, TODAY)
            with self.subTest(days=days):
                if ok:
                    self.assertEqual(problems, [])
                else:
                    self.assertTrue(any("days old" in problem for problem in problems))

    def test_future_and_grace(self) -> None:
        source = (SCRIPTS / "claim_rules.py").read_text(encoding="utf-8")
        self.assertIn("timezone grace", source)
        data = baseline()
        data["last_verified"] = "2026-12-01"
        problems = claim_rules.freshness_problems(data, TODAY)
        self.assertTrue(any("future" in problem for problem in problems))
        data["last_verified"] = "2026-10-05"
        self.assertEqual(claim_rules.freshness_problems(data, TODAY), [])
        data["last_verified"] = "2026-10-06"
        self.assertTrue(claim_rules.freshness_problems(data, TODAY))

    def test_compact_date_fails_the_schema(self) -> None:
        data = baseline()
        data["last_verified"] = "20261004"
        self.assertTrue(claim_rules.validate_window(data, TODAY))
        self.assertTrue(claim_rules.freshness_problems(data, TODAY))

    def test_by_must_be_human(self) -> None:
        data = baseline()
        data["last_verified"] = "2026-10-04"
        data["last_verified_by"] = "script"
        self.assertTrue(claim_rules.freshness_problems(data, TODAY))

    def test_cli_fixture_exit_codes(self) -> None:
        outside = Path(tempfile.mkdtemp())
        path = outside / "window-fresh.json"
        fresh = baseline()
        fresh["last_verified"] = "2026-10-04"
        path.write_text(json.dumps(fresh), encoding="utf-8")
        ok = _run(["--freshness", "--window", str(path), "--today", "2026-10-04"])
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertIn("freshness OK:", ok.stdout)
        self.assertNotIn("Traceback", ok.stdout + ok.stderr)

        stale = baseline()
        stale["last_verified"] = "2026-09-19"
        path.write_text(json.dumps(stale), encoding="utf-8")
        aged = _run(["--freshness", "--window", str(path), "--today", "2026-10-04"])
        self.assertEqual(aged.returncode, 1, aged.stdout + aged.stderr)
        self.assertIn("days old", aged.stdout)

        missing = baseline()
        missing["last_verified"] = None
        path.write_text(json.dumps(missing), encoding="utf-8")
        null = _run(["--freshness", "--window", str(path), "--today", "2026-10-04"])
        self.assertEqual(null.returncode, 1)
        self.assertIn("not set", null.stdout)
        self.assertNotIn("Traceback", null.stdout + null.stderr)

        compact = baseline()
        compact["last_verified"] = "20261004"
        path.write_text(json.dumps(compact), encoding="utf-8")
        bad = _run(["--freshness", "--window", str(path), "--today", "2026-10-04"])
        self.assertEqual(bad.returncode, 1)
        self.assertNotIn("Traceback", bad.stdout + bad.stderr)

    def test_real_tree_freshness_exits_1(self) -> None:
        completed = _run(["--freshness"])
        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertIn("freshness FAIL: references/sme-fund-window.json", completed.stdout)
        self.assertIn("not set: a human must read both live pages and set it", completed.stdout)
        self.assertIn("name patterns: skipped (no external file)", completed.stdout)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)
        self.assertNotIn("hygiene check OK:", completed.stdout)

    def test_normal_run_allows_a_null_date(self) -> None:
        completed = _run([])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        ok_lines = [line for line in completed.stdout.splitlines() if line.startswith("hygiene check OK:")]
        self.assertEqual(ok_lines, [OK_LINE])
        self.assertNotIn("not set:", completed.stdout)
        self.assertIn("name patterns: skipped (no external file)", completed.stdout)
        self.assertIn("claim allow-list warnings:", completed.stdout)
        self.assertIn("corpus legacy warnings:", completed.stdout)

    def test_cli_extra_pattern_does_not_print_the_match(self) -> None:
        token = "zzdummyfirm"
        outside = Path(tempfile.mkdtemp())
        patterns = outside / "patterns.txt"
        patterns.write_text(token + "\n", encoding="utf-8")
        window = outside / "window.json"
        data = baseline()
        data["last_verified"] = "2026-10-04"
        data["instrument_label"] = "see " + token
        window.write_text(json.dumps(data), encoding="utf-8")
        completed = _run(
            [
                "--freshness",
                "--window",
                str(window),
                "--today",
                "2026-10-04",
                "--extra-patterns",
                str(patterns),
            ]
        )
        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertIn("extra pattern #1", completed.stdout)
        self.assertNotIn(token, completed.stdout)
        self.assertNotIn(token, completed.stderr)


if __name__ == "__main__":
    unittest.main()
