"""Optional sme_fund_pointer example on the headless hygiene package."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import claim_rules  # noqa: E402
import headless_pointer  # noqa: E402

HEADLESS = ROOT / "references" / "headless-hygiene-package.md"
WINDOW = ROOT / "references" / "sme-fund-window.json"


def _text() -> str:
    return HEADLESS.read_text(encoding="utf-8")


def _window() -> dict:
    data, error = claim_rules.parse_window_text(WINDOW.read_text(encoding="utf-8"))
    if error or not isinstance(data, dict):
        raise AssertionError(error)
    return data


def _pointer(text: str | None = None) -> dict:
    values, errors = headless_pointer.parse_fences(text if text is not None else _text())
    if errors:
        raise AssertionError(errors)
    examples = headless_pointer.pointer_examples(values)
    if len(examples) != 1:
        raise AssertionError(examples)
    pointer = examples[0]["sme_fund_pointer"]
    if not isinstance(pointer, dict):
        raise AssertionError(pointer)
    return pointer


def _schema(text: str | None = None) -> dict:
    values, errors = headless_pointer.parse_fences(text if text is not None else _text())
    if errors:
        raise AssertionError(errors)
    found = [
        value
        for value in values
        if isinstance(value, dict) and value.get("schema") == headless_pointer.SCHEMA_ID
    ]
    if len(found) != 1:
        raise AssertionError(found)
    return found[0]


class HeadlessPointerExampleTests(unittest.TestCase):
    def test_example_block_parses(self) -> None:
        pointer = _pointer()
        self.assertIs(pointer["fired"], True)
        self.assertIs(pointer["stale"], False)
        self.assertIs(pointer["provider_must_be_listed"], True)
        self.assertIs(pointer["not_the_official_report"], True)
        self.assertIs(pointer["intake_sheet"]["offered"], True)
        self.assertIs(pointer["intake_sheet"]["included"], False)

    def test_reimbursement_and_expert_are_fixed(self) -> None:
        pointer = _pointer()
        self.assertEqual(pointer["reimbursement_claim"], "none")
        self.assertEqual(pointer["intake_sheet"]["fields"]["preferred_listed_expert"], "")

    def test_example_values_have_no_percent_or_currency(self) -> None:
        values, errors = headless_pointer.parse_fences(_text())
        self.assertEqual(errors, [])
        examples = headless_pointer.pointer_examples(values)
        self.assertEqual(len(examples), 1)
        for value in headless_pointer.string_values(examples[0]):
            self.assertNotIn("%", value)
            self.assertIsNone(claim_rules.CURRENCY_RE.search(value))
            self.assertIsNone(re.search(r"(?i)\d\s*percent\b", value))

    def test_example_keys_match_the_documented_field_list(self) -> None:
        documented, errors = headless_pointer.documented_fields(_text())
        self.assertEqual(errors, [])
        self.assertIsNotNone(documented)
        assert documented is not None
        pointer = _pointer()
        self.assertEqual(set(pointer), set(documented["sme_fund_pointer"]))
        self.assertEqual(list(pointer), documented["sme_fund_pointer"])
        self.assertEqual(set(pointer["intake_sheet"]), set(documented["intake_sheet"]))
        self.assertEqual(set(pointer["intake_sheet"]["fields"]), set(documented["fields"]))
        self.assertEqual(set(pointer["sources"][0]), set(documented["sources"]))
        for name, expected in headless_pointer.EXPECTED.items():
            self.assertEqual(documented[name], list(expected))

    def test_package_example_omits_the_pointer_key(self) -> None:
        schema = _schema()
        self.assertNotIn("sme_fund_pointer", schema)
        self.assertEqual(list(schema), list(headless_pointer.CANONICAL_KEYS))
        self.assertEqual(
            headless_pointer.schema_example_sha256(_text()),
            headless_pointer.SCHEMA_FENCE_SHA256,
        )

    def test_edition_matches_the_hygiene_check(self) -> None:
        check = (ROOT / "scripts" / "check-hygiene.py").read_text(encoding="utf-8")
        match = re.search(r'^VERSION = "([^"]+)"', check, re.M)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match.group(1), "0.5.54-free")
        self.assertEqual(_schema()["edition"], "0.5.54-free")
        self.assertEqual(_schema()["schema"], "sorticai.hygiene_package.v1")

    def test_status_enum_and_label_follow_the_window_file(self) -> None:
        pointer = _pointer()
        window = _window()
        self.assertEqual(pointer["instrument_label"], window["instrument_label"])
        parts = {part.strip() for part in pointer["window_status"].split("|")}
        self.assertEqual(parts, set(claim_rules.WINDOW_STATUSES))
        self.assertIn(window["window_status"], parts)
        levels = {part.strip() for part in pointer["level"].split("|")}
        self.assertEqual(levels, {"L2", "L3"})

    def test_contract_accepts_the_shipped_file(self) -> None:
        self.assertEqual(headless_pointer.contract_errors(_text(), _window()), [])

    def test_reimbursement_other_than_none_fails(self) -> None:
        bad = _text().replace('"reimbursement_claim": "none"', '"reimbursement_claim": "full"', 1)
        errors = headless_pointer.example_problems(bad)
        self.assertTrue(any("reimbursement_claim" in error for error in errors))

    def test_named_expert_fails(self) -> None:
        bad = _text().replace(
            '"preferred_listed_expert": ""',
            '"preferred_listed_expert": "a"',
            1,
        )
        errors = headless_pointer.example_problems(bad)
        self.assertTrue(any("preferred_listed_expert" in error for error in errors))

    def test_percent_and_currency_in_values_fail(self) -> None:
        percent = _text().replace('"short text"', '"short text 10%"', 1)
        errors = headless_pointer.example_problems(percent)
        self.assertTrue(any("percent" in error for error in errors))
        word = _text().replace('"short text"', '"10 percent"', 1)
        errors = headless_pointer.example_problems(word)
        self.assertTrue(any("percent" in error for error in errors))
        amount = _text().replace('"short text"', '"10 EUR"', 1)
        errors = headless_pointer.example_problems(amount)
        self.assertTrue(any("currency amount" in error for error in errors))

    def test_key_drift_fails(self) -> None:
        bad = _text().replace('"not_the_official_report": true', '"not_report": true', 1)
        errors = headless_pointer.example_problems(bad)
        self.assertTrue(any("field list" in error for error in errors))
        extra = _text().replace('"fired": true,', '"fired": true, "extra": 1,', 1)
        errors = headless_pointer.example_problems(extra)
        self.assertTrue(any("field list" in error for error in errors))

    def test_pointer_inside_the_package_example_fails(self) -> None:
        bad = _text().replace(
            "Public URLs located are not 'verified sources'.\"\n}",
            "Public URLs located are not 'verified sources'.\",\n"
            '  "sme_fund_pointer": {"fired": true}\n}',
            1,
        )
        errors = headless_pointer.contract_errors(bad, _window())
        self.assertTrue(any("includes sme_fund_pointer" in error for error in errors))

    def test_missing_rule_sentence_fails(self) -> None:
        bad = _text().replace(
            "Headless defaults stay options 1 and 8.",
            "Headless defaults were removed.",
            1,
        )
        errors = headless_pointer.rule_text_problems(bad)
        self.assertTrue(any("defaults" in error for error in errors))
        self.assertEqual(headless_pointer.rule_text_problems(_text()), [])


if __name__ == "__main__":
    unittest.main()
