#!/usr/bin/env python3
"""Checks for the optional sme_fund_pointer example in the headless contract.

The package example fence is hashed so that key stays out of the object
consumers already accept. The pointer example is a separate fence.
"""

from __future__ import annotations

import hashlib
import json
import re

import claim_rules

SCHEMA_ID = "sorticai.hygiene_package.v1"
POINTER_KEY = "sme_fund_pointer"

# Bytes of the package example fence. A later edition change updates this.
SCHEMA_FENCE_SHA256 = "630f4b1db0643cb13e5f56f041fc45d66fb488b8d3d7f585272f2b2559049342"

CANONICAL_KEYS = (
    "schema",
    "edition",
    "activation_level",
    "output_register",
    "not_for_third_party",
    "owner_gated",
    "noticed",
    "snapshot",
    "show_hold",
    "deliverables",
    "holdbacks",
    "contribution_log_started",
    "agent_exposure",
    "approval_required",
    "evidence_or_blocked",
    "stop_or_decline",
    "next_hygiene_step",
    "disclaimer",
    "sources_note",
)

EXPECTED = {
    "sme_fund_pointer": (
        "fired",
        "level",
        "instrument_label",
        "window_status",
        "window_note",
        "last_verified",
        "stale",
        "sources",
        "provider_must_be_listed",
        "reimbursement_claim",
        "intake_sheet",
        "not_the_official_report",
    ),
    "sources": ("label", "url"),
    "intake_sheet": ("offered", "included", "fields"),
    "fields": (
        "sme_status_evidence",
        "vat_certificate_ready",
        "bank_confirmation_ready",
        "asset_names",
        "show_hold_map_exists",
        "contribution_log_started",
        "public_next_90_days",
        "prior_disclosure_or_filing",
        "preferred_listed_expert",
    ),
}

RULE_SNIPPETS = (
    ("heading", "## Schema (emit exactly these keys, plus `sme_fund_pointer` only when the pointer fired)"),
    ("schema-id", "Schema stays `sorticai.hygiene_package.v1`."),
    ("omit-key", "When the pointer did not fire, omit that key."),
    ("no-null", "Do not emit the key as null."),
    ("reimbursement", "`reimbursement_claim` is always the string `none`."),
    ("expert", "`preferred_listed_expert` is always the empty string."),
    ("no-figures", "No percent, no amount, and no provider name in any value."),
    (
        "stale",
        "`stale` is true when `last_verified` is null or older than `stale_after_days` in `references/sme-fund-window.json`.",
    ),
    ("parameters", "Technical parameters pasted by the user never go into `intake_sheet`."),
    ("show-hold", "Point to the show/hold map."),
    ("defaults", "Headless defaults stay options 1 and 8."),
    ("catalog", "The numbered catalog stays 8 options."),
)

_FENCE = re.compile(r"^```json\n(.*?)\n```", re.M | re.S)
_SECTION = re.compile(r"^### Field list\n(.*?)(?=^### |\Z)", re.M | re.S)
_GROUP = re.compile(
    r"^`(?P<name>sme_fund_pointer|sources|intake_sheet|fields)`:\n+(?P<body>(?:- `[^`]+`\n)+)",
    re.M,
)
_PERCENT = re.compile(r"%|(?i:(?<!\d)\d{1,6}(?:[.,]\d{1,4})?(?!\d)\s*percent\b)")
_LEVELS = frozenset({"L2", "L3"})


def _dedupe(items: list[str]) -> list[str]:
    seen: list[str] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def fence_bodies(text: str) -> list[str]:
    return [match.group(1) for match in _FENCE.finditer(text)]


def parse_fences(text: str) -> tuple[list[object], list[str]]:
    values: list[object] = []
    errors: list[str] = []
    for index, body in enumerate(fence_bodies(text), 1):
        try:
            values.append(json.loads(body))
        except json.JSONDecodeError:
            errors.append(f"headless JSON fence {index} is not valid JSON")
    return values, errors


def schema_example_sha256(text: str) -> str | None:
    for body in fence_bodies(text):
        try:
            obj = json.loads(body)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("schema") == SCHEMA_ID:
            return hashlib.sha256(body.encode("utf-8")).hexdigest()
    return None


def documented_fields(text: str) -> tuple[dict[str, list[str]] | None, list[str]]:
    match = _SECTION.search(text)
    if not match:
        return None, ["headless field list is missing"]
    found: dict[str, list[str]] = {}
    for group in _GROUP.finditer(match.group(1)):
        name = group.group("name")
        keys = re.findall(r"- `([^`]+)`", group.group("body"))
        if name in found:
            return None, ["headless field list repeats a group"]
        found[name] = keys
    if set(found) != set(EXPECTED):
        return None, ["headless field list is missing a group"]
    return found, []


def pointer_examples(values: list[object]) -> list[dict]:
    found: list[dict] = []
    for value in values:
        if isinstance(value, dict) and set(value) == {POINTER_KEY}:
            found.append(value)
    return found


def string_values(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, list):
        for item in value:
            found.extend(string_values(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(string_values(item))
    return found


def _pipe_set(value: object) -> set[str] | None:
    if not isinstance(value, str):
        return None
    return {part.strip() for part in value.split("|")}


def alignment_errors(pointer: dict, window: dict) -> list[str]:
    errors: list[str] = []
    if pointer.get("instrument_label") != window.get("instrument_label"):
        errors.append("headless pointer example instrument_label drifted from the window file")
    parts = _pipe_set(pointer.get("window_status"))
    if parts != set(claim_rules.WINDOW_STATUSES):
        errors.append("headless pointer example window_status drifted from the window enum")
    return errors


def rule_text_problems(text: str) -> list[str]:
    errors: list[str] = []
    for rule_id, snippet in RULE_SNIPPETS:
        if snippet not in text:
            errors.append(f"headless contract is missing pointer rule {rule_id}")
    return errors


def _example_from(text: str, values: list[object]) -> list[str]:
    errors: list[str] = []
    documented, doc_errors = documented_fields(text)
    errors.extend(doc_errors)
    examples = pointer_examples(values)
    if len(examples) != 1:
        errors.append("headless pointer example must be one JSON object")
        return errors
    pointer = examples[0].get(POINTER_KEY)
    if not isinstance(pointer, dict):
        errors.append("headless pointer example must be an object")
        return errors
    if documented is not None:
        for name, expected in EXPECTED.items():
            if documented.get(name) != list(expected):
                errors.append(f"headless field list for {name} drifted")
        if list(pointer) != documented.get("sme_fund_pointer"):
            errors.append("headless pointer example does not match the field list")
    if _pipe_set(pointer.get("level")) != _LEVELS:
        errors.append("headless pointer example level is not L2 or L3")
    if pointer.get("reimbursement_claim") != "none":
        errors.append('headless pointer example reimbursement_claim must be "none"')
    sheet = pointer.get("intake_sheet")
    field_map: dict = {}
    if not isinstance(sheet, dict) or list(sheet) != list(EXPECTED["intake_sheet"]):
        errors.append("headless pointer example intake_sheet does not match the field list")
    elif documented is not None and list(sheet) != documented.get("intake_sheet"):
        errors.append("headless pointer example intake_sheet does not match the field list")
    if isinstance(sheet, dict) and isinstance(sheet.get("fields"), dict):
        field_map = sheet["fields"]
        if list(field_map) != list(EXPECTED["fields"]):
            errors.append("headless pointer example fields do not match the field list")
        elif documented is not None and list(field_map) != documented.get("fields"):
            errors.append("headless pointer example fields do not match the field list")
    if field_map.get("preferred_listed_expert") != "":
        errors.append("headless pointer example preferred_listed_expert must be empty")
    sources = pointer.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("headless pointer example sources must list one item")
    else:
        for item in sources:
            if not isinstance(item, dict) or list(item) != list(EXPECTED["sources"]):
                errors.append("headless pointer example sources do not match the field list")
                break
            if documented is not None and list(item) != documented.get("sources"):
                errors.append("headless pointer example sources do not match the field list")
                break
    for value in string_values(examples[0]):
        if _PERCENT.search(value):
            errors.append("headless pointer example value contains a percent")
            break
    for value in string_values(examples[0]):
        if claim_rules.CURRENCY_RE.search(value):
            errors.append("headless pointer example value contains a currency amount")
            break
    return errors


def _schema_from(text: str, values: list[object]) -> list[str]:
    errors: list[str] = []
    schemas = [value for value in values if isinstance(value, dict) and value.get("schema") == SCHEMA_ID]
    if len(schemas) != 1:
        errors.append("headless package example must be one JSON object")
        return errors
    obj = schemas[0]
    if POINTER_KEY in obj:
        errors.append("headless package example includes sme_fund_pointer")
    if list(obj) != list(CANONICAL_KEYS):
        errors.append("headless package example keys changed")
    if schema_example_sha256(text) != SCHEMA_FENCE_SHA256:
        errors.append("headless package example bytes changed")
    return errors


def example_problems(text: str) -> list[str]:
    values, errors = parse_fences(text)
    errors.extend(_example_from(text, values))
    return _dedupe(errors)


def contract_errors(text: str, window: dict | None = None) -> list[str]:
    values, errors = parse_fences(text)
    errors.extend(_example_from(text, values))
    errors.extend(_schema_from(text, values))
    errors.extend(rule_text_problems(text))
    if isinstance(window, dict):
        examples = pointer_examples(values)
        if len(examples) == 1 and isinstance(examples[0].get(POINTER_KEY), dict):
            errors.extend(alignment_errors(examples[0][POINTER_KEY], window))
    return _dedupe(errors)
