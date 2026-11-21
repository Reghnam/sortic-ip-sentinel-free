"""Structural check of sorticai.hygiene_package.v1 against the documented keys.

Stdlib only. The schema is compared to the JSON examples and the field list
in references/headless-hygiene-package.md. A pipe list in an example is the
enum. Duplicate pipe values are one allowed value, first occurrence kept.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "references" / "headless-hygiene-package.md"
SCHEMA = ROOT / "references" / "hygiene-package.v1.schema.json"
DRAFT = "https://json-schema.org/draft/2020-12/schema"


def _fences(text: str) -> list[object]:
    bodies = re.findall(r"```json\n(.*?)\n```", text, re.S)
    return [json.loads(body) for body in bodies]


def _unique_pipe(value: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for part in value.split(" | "):
        if part not in seen:
            seen.add(part)
            found.append(part)
    return found


def _field_groups(text: str) -> dict[str, list[str]]:
    section = re.search(r"^### Field list\n(.*?)(?=^### |\Z)", text, re.M | re.S)
    if section is None:
        return {}
    groups: dict[str, list[str]] = {}
    for match in re.finditer(
        r"^`(?P<name>[^`]+)`:\n+(?P<body>(?:- `[^`]+`\n)+)",
        section.group(1),
        re.M,
    ):
        groups[match.group("name")] = re.findall(r"- `([^`]+)`", match.group("body"))
    return groups


class HygienePackageSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        fences = _fences(cls.doc)
        cls.package = fences[0]
        cls.pointer = fences[1]["sme_fund_pointer"]

    def test_draft_and_top_level_keys(self) -> None:
        self.assertEqual(self.schema["$schema"], DRAFT)
        self.assertEqual(self.schema["title"], "sorticai.hygiene_package.v1")
        self.assertEqual(self.schema["type"], "object")
        self.assertIs(self.schema["additionalProperties"], False)
        self.assertEqual(self.schema["required"], list(self.package))
        self.assertEqual(
            list(self.schema["properties"]),
            list(self.package) + ["sme_fund_pointer"],
        )
        self.assertNotIn("sme_fund_pointer", self.schema["required"])
        self.assertEqual(self.schema["properties"]["schema"]["const"], self.package["schema"])

    def test_package_example_matches_schema(self) -> None:
        self._walk(self.schema, self.package, "package")

    def test_pointer_example_matches_schema(self) -> None:
        self._walk(
            self.schema["properties"]["sme_fund_pointer"],
            self.pointer,
            "sme_fund_pointer",
        )
        groups = _field_groups(self.doc)
        pointer = self.schema["properties"]["sme_fund_pointer"]
        self.assertEqual(pointer["required"], groups["sme_fund_pointer"])
        self.assertEqual(pointer["properties"]["sources"]["items"]["required"], groups["sources"])
        intake = pointer["properties"]["intake_sheet"]
        self.assertEqual(intake["required"], groups["intake_sheet"])
        self.assertEqual(intake["properties"]["fields"]["required"], groups["fields"])

    def test_documented_always_values(self) -> None:
        self.assertIn("JSON null, or one date string", self.doc)
        last = self.schema["properties"]["sme_fund_pointer"]["properties"]["last_verified"]
        self.assertEqual(last["type"], ["string", "null"])
        self.assertIn("`owner_gated`: always `true`", self.doc)
        self.assertIs(self.schema["properties"]["owner_gated"]["const"], True)
        pointer = self.schema["properties"]["sme_fund_pointer"]["properties"]
        self.assertIn("`reimbursement_claim` is always the string `none`", self.doc)
        self.assertEqual(pointer["reimbursement_claim"]["const"], "none")
        self.assertIn("`preferred_listed_expert` is always the empty string", self.doc)
        fields = pointer["intake_sheet"]["properties"]["fields"]["properties"]
        self.assertEqual(fields["preferred_listed_expert"]["const"], "")
        self.assertIn("sets `fired` to true", self.doc)
        self.assertIs(pointer["fired"]["const"], True)
        self.assertIn("`provider_must_be_listed` is true", self.doc)
        self.assertIs(pointer["provider_must_be_listed"]["const"], True)
        self.assertIn("`not_the_official_report` is true", self.doc)
        self.assertIs(pointer["not_the_official_report"]["const"], True)

    def _walk(self, schema: dict, example: object, path: str) -> None:
        if isinstance(example, dict):
            self.assertEqual(schema["type"], "object", path)
            self.assertIs(schema["additionalProperties"], False, path)
            self.assertEqual(schema["required"], list(example), path)
            present = [key for key in schema["properties"] if key in example]
            self.assertEqual(present, list(example), path)
            for key in schema["properties"]:
                if key not in example:
                    self.assertNotIn(key, schema["required"], path)
            for key, value in example.items():
                self._walk(schema["properties"][key], value, f"{path}.{key}")
            return
        if isinstance(example, list):
            self.assertEqual(schema["type"], "array", path)
            if example:
                self._walk(schema["items"], example[0], path + "[]")
            return
        if isinstance(example, bool):
            self.assertEqual(schema["type"], "boolean", path)
            return
        if isinstance(example, int):
            self.assertEqual(schema["type"], "integer", path)
            return
        if isinstance(example, str):
            if path.endswith("last_verified"):
                self.assertEqual(schema["type"], ["string", "null"], path)
                return
            if " | " in example:
                self.assertEqual(schema["type"], "string", path)
                self.assertEqual(schema["enum"], _unique_pipe(example), path)
                return
            self.assertEqual(schema["type"], "string", path)
            return
        self.fail(f"unexpected example at {path}: {example!r}")


if __name__ == "__main__":
    unittest.main()
