#!/usr/bin/env python3
"""Write the CI scan config from the pinned binary.

The binary embeds the tagged default rules. This keeps those rules and drops
the global paths list. It does not extend the defaults.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tomllib
from pathlib import Path

PREFIX = b"# This file has been auto-generated. Do not edit manually.\n"


def extract_embedded_config(binary: bytes) -> bytes:
    start = binary.find(PREFIX)
    if start < 0:
        raise SystemExit("embedded config prefix missing")
    if binary.find(PREFIX, start + len(PREFIX)) != -1:
        raise SystemExit("embedded config prefix is not unique")
    region = binary[start:]
    nul = region.find(b"\x00")
    if nul < 0:
        raise SystemExit("embedded config is not bounded")
    blob = region[:nul]
    if blob.decode("utf-8").encode("utf-8") != blob:
        raise SystemExit("embedded config is not utf-8")
    return blob


def strip_global_paths(text: str) -> str:
    lines = text.splitlines(keepends=True)
    start = _global_table(lines)
    end = _next_table(lines, start + 1)
    begin = None
    for index in range(start, end):
        if lines[index].strip() == "paths = [":
            if begin is not None:
                raise SystemExit("global table has more than one paths list")
            begin = index
    if begin is None:
        raise SystemExit("global paths list missing")
    close = None
    for index in range(begin + 1, end):
        if lines[index].strip() == "]":
            close = index
            break
    if close is None:
        raise SystemExit("global paths list has no closer")
    return "".join(lines[:begin] + lines[close + 1 :])


def _global_table(lines: list[str]) -> int:
    found = None
    for index, line in enumerate(lines):
        if line.strip() != "[allowlist]":
            continue
        if line[:1].isspace():
            continue
        if found is not None:
            raise SystemExit("more than one global allowlist table")
        found = index
    if found is None:
        raise SystemExit("global allowlist table missing")
    return found


def _next_table(lines: list[str], start: int) -> int:
    for index in range(start, len(lines)):
        stripped = lines[index].lstrip()
        if lines[index][:1].isspace() or not stripped.startswith("["):
            continue
        return index
    return len(lines)


def _rule_path_lists(data: dict) -> list[list[str]]:
    found: list[list[str]] = []
    for rule in data.get("rules", []):
        groups = rule.get("allowlists") or []
        if isinstance(rule.get("allowlist"), dict):
            groups = [rule["allowlist"], *groups]
        for group in groups:
            if "paths" in group:
                found.append(list(group["paths"]))
    return found


def _require_stripped(original: str, stripped: str) -> None:
    source = tomllib.loads(original)
    result = tomllib.loads(stripped)
    if "paths" not in source.get("allowlist", {}):
        raise SystemExit("pinned config has no global paths list")
    if "paths" in result.get("allowlist", {}):
        raise SystemExit("global paths list is still present")
    if "extend" in result or "useDefault" in stripped:
        raise SystemExit("config extends another config")
    if len(result.get("rules", [])) != len(source.get("rules", [])):
        raise SystemExit("rule count changed")
    if _rule_path_lists(source) != _rule_path_lists(result):
        raise SystemExit("rule path lists changed")


def build_config(binary: bytes, source_sha256: str, output_sha256: str) -> bytes:
    blob = extract_embedded_config(binary)
    actual_source = hashlib.sha256(blob).hexdigest()
    if actual_source != source_sha256:
        raise SystemExit("embedded config checksum mismatch")
    text = blob.decode("utf-8")
    stripped = strip_global_paths(text)
    _require_stripped(text, stripped)
    out = stripped.encode("utf-8")
    actual_output = hashlib.sha256(out).hexdigest()
    if actual_output != output_sha256:
        raise SystemExit("scan config checksum mismatch")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the CI scan config from the pinned binary.")
    parser.add_argument("--binary", required=True)
    parser.add_argument("--source-sha256", required=True)
    parser.add_argument("--output-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    output = Path(args.output)
    if output.name.startswith(".gitleaks"):
        raise SystemExit("refusing to write a guarded config name")
    if not output.parent.is_dir():
        raise SystemExit("scan config directory is missing")
    payload = build_config(Path(args.binary).read_bytes(), args.source_sha256, args.output_sha256)
    output.write_bytes(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
