"""Closed schema for the pointer window file."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import claim_rules  # noqa: E402

TODAY = date(2026, 10, 4)
WINDOW = ROOT / "references" / "sme-fund-window.json"


def baseline() -> dict:
    data, error = claim_rules.parse_window_text(WINDOW.read_text(encoding="utf-8"))
    if error or not isinstance(data, dict):
        raise AssertionError(error)
    return data


class WindowSchemaTests(unittest.TestCase):
    def test_real_file_passes(self) -> None:
        errors = claim_rules.validate_window(baseline(), TODAY)
        self.assertEqual(errors, [])

    def test_every_required_key_missing(self) -> None:
        for key in sorted(claim_rules.WINDOW_KEYS):
            data = baseline()
            del data[key]
            errors = claim_rules.validate_window(data, TODAY)
            with self.subTest(key=key):
                self.assertTrue(any(f"missing key {key}" in error for error in errors))

    def test_unknown_key_and_enum(self) -> None:
        data = baseline()
        data["extra"] = "no"
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("unknown key extra" in error for error in errors))
        data = baseline()
        data["window_status"] = "closed"
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("window_status" in error for error in errors))
        data = baseline()
        data["schema"] = "other"
        self.assertTrue(claim_rules.validate_window(data, TODAY))
        data = baseline()
        data["scope"] = "advice"
        self.assertTrue(claim_rules.validate_window(data, TODAY))

    def test_bad_dates(self) -> None:
        for value in ("2026-02-31", "20261004", "2026-10-04T00:00:00Z", "2099-01-01"):
            data = baseline()
            data["last_verified"] = value
            errors = claim_rules.validate_window(data, TODAY)
            with self.subTest(value=value):
                self.assertTrue(errors)

    def test_tomorrow_passes_and_the_day_after_fails(self) -> None:
        data = baseline()
        data["last_verified"] = "2026-10-05"
        self.assertEqual(claim_rules.validate_window(data, TODAY), [])
        data["last_verified"] = "2026-10-06"
        self.assertTrue(any("tomorrow" in error for error in claim_rules.validate_window(data, TODAY)))

    def test_old_date_is_valid_for_the_schema(self) -> None:
        data = baseline()
        data["last_verified"] = "2020-01-01"
        self.assertEqual(claim_rules.validate_window(data, TODAY), [])

    def test_open_while_null_is_rejected(self) -> None:
        data = baseline()
        data["window_status"] = "open"
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("open" in error for error in errors))

    def test_null_note_must_be_unverified(self) -> None:
        data = baseline()
        data["last_verified_note"] = "a human will set this"
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("UNVERIFIED" in error for error in errors))

    def test_stale_after_days_bounds(self) -> None:
        for value in (True, False, 0, 31, 14.5, "14"):
            data = baseline()
            data["stale_after_days"] = value
            with self.subTest(value=value):
                self.assertTrue(claim_rules.validate_window(data, TODAY))
        for value in (1, 14, 30):
            data = baseline()
            data["stale_after_days"] = value
            with self.subTest(value=value):
                self.assertEqual(claim_rules.validate_window(data, TODAY), [])

    def test_window_note_and_footer(self) -> None:
        data = baseline()
        data["window_note"] = "a\nb"
        self.assertTrue(claim_rules.validate_window(data, TODAY))
        data = baseline()
        data["window_note"] = "x" * 401
        self.assertTrue(claim_rules.validate_window(data, TODAY))
        data = baseline()
        data["footer_template"] = "Status as of a date. Not legal advice."
        self.assertTrue(claim_rules.validate_window(data, TODAY))
        data = baseline()
        data["footer_template"] = "Status as of {last_verified}."
        self.assertTrue(claim_rules.validate_window(data, TODAY))

    def test_lookalike_hosts_fail(self) -> None:
        for url in (
            "https://euipo.europa.eu.example.test/page",
            "https://xeuipo.europa.eu/page",
            "http://www.euipo.europa.eu/page",
            "https://www.euipo.europa.eu:443/page",
        ):
            data = baseline()
            data["sources"] = [
                {"label": "EUIPO", "url": url},
                {"label": "national office page", "url": "https://www.upv.gov.cz/sluzby/cosme-fund"},
            ]
            errors = claim_rules.validate_window(data, TODAY)
            with self.subTest(url=url):
                self.assertTrue(errors)
        at = chr(64)
        data = baseline()
        data["sources"] = [
            {
                "label": "EUIPO",
                "url": "https://user:pass" + at + "www.euipo.europa.eu/page",
            },
            {"label": "national office page", "url": "https://www.upv.gov.cz/sluzby/cosme-fund"},
        ]
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("user info" in error for error in errors))

    def test_both_hosts_and_label(self) -> None:
        data = baseline()
        data["sources"] = [
            {"label": "EUIPO", "url": "https://www.euipo.europa.eu/en/sme-corner/sme-fund/2026"}
        ]
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("every allowed host" in error for error in errors))
        data = baseline()
        data["sources"] = [
            {"label": "  ", "url": "https://www.euipo.europa.eu/en/sme-corner/sme-fund/2026"},
            {"label": "national office page", "url": "https://www.upv.gov.cz/sluzby/cosme-fund"},
        ]
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("label is empty" in error for error in errors))

    def test_unverified_markers(self) -> None:
        data = baseline()
        data["unverified"] = ["a plain line"]
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("must start with UNVERIFIED" in error for error in errors))
        data = baseline()
        data["unverified"] = ["UNVERIFIED: nothing named here"]
        errors = claim_rules.validate_window(data, TODAY)
        self.assertTrue(any("EUIPO" in error for error in errors))
        self.assertTrue(any("call text" in error for error in errors))
        data = baseline()
        data["unverified"] = []
        self.assertTrue(claim_rules.validate_window(data, TODAY))

    def test_percent_and_amount_in_strings(self) -> None:
        data = baseline()
        data["instrument_label"] = "label 90%"
        self.assertTrue(any("percent" in error for error in claim_rules.validate_window(data, TODAY)))
        data = baseline()
        data["instrument_label"] = "label 90 percent"
        self.assertTrue(any("percent" in error for error in claim_rules.validate_window(data, TODAY)))
        data = baseline()
        data["instrument_label"] = "label 10 EUR"
        self.assertTrue(any("currency amount" in error for error in claim_rules.validate_window(data, TODAY)))
        data = baseline()
        data["facts_allowed"] = list(data["facts_allowed"]) + ["see https://example.test/page"]
        self.assertTrue(any("allow-list" in error for error in claim_rules.validate_window(data, TODAY)))

    def test_duplicate_key_is_rejected(self) -> None:
        data, error = claim_rules.parse_window_text('{"schema": "a", "schema": "b"}')
        self.assertIsNone(data)
        self.assertIsNotNone(error)
        self.assertIn("duplicate key schema", error or "")

    def test_by_must_be_human(self) -> None:
        data = baseline()
        data["last_verified_by"] = "script"
        self.assertTrue(claim_rules.validate_window(data, TODAY))


if __name__ == "__main__":
    unittest.main()
