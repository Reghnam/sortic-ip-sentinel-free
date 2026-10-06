"""Text checks for the hygiene workflow.

The stdlib has no YAML parser, so these tests read the workflow by indentation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import secrets
import shlex
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "hygiene-check.yml"
ARCHIVE_SHA256 = "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
ZERO_SHA = "0000000000000000000000000000000000000000"
GUARD_STEP = "Committed config guard"
SCAN_STEP = "Secret scan"
TRAILER_STEP = "Commit trailer check"
TRAILER_SKIP = "trailer check range skipped"
TRAILER_FAIL = "commit message has a co-author trailer"
TRAILER_EVENT_FAIL = "trailer check event is not a pull request or push"
TRAILER_PR_RANGE_FAIL = "pull request range is not two commits"
UNIT_STEP = "Pack tooling unit tests"
UNIT_CMD = "python3 -m unittest discover -s tests"
GUARD_NAMES = (
    ".gitleaks.toml",
    ".gitleaks.json",
    ".gitleaks.yaml",
    ".gitleaks.yml",
    ".gitleaks",
    ".gitleaksignore",
    ".gitleaks.anything",
)
GUARD_KINDS = ("file", "dir", "symlink-file", "symlink-dir", "broken-symlink")
GUARD_START = "# secret-scan-guard-start"
GUARD_END = "# secret-scan-guard-end"
GUARD_FAIL = "secret scan refused a committed config or ignore file"
UNSET_LINE = "unset GITLEAKS_CONFIG GITLEAKS_CONFIG_TOML"
DIR_CALL = '"${tool}" dir . --no-banner --redact --ignore-gitleaks-allow --config "${scan_config}"'
GIT_CALL = (
    '"${tool}" git . --no-banner --redact --ignore-gitleaks-allow '
    '--config "${scan_config}" --log-opts="--text ${range}"'
)
SUM_LINE = 'echo "${ARCHIVE_SHA256}  ${archive}" | sha256sum -c -'
TAR_LINE = 'tar -xzf "${archive}" -C "${RUNNER_TEMP}" gitleaks'
BINARY_SHA256 = "88f91962aa2f93ac6ab281d553b9e125f5197bbbce38f9f2437f7299c32e5509"
SOURCE_SHA256 = "e163e53b9e7e8a8511e77271e2b323ed057759542a6d988258afe3a1fa329caf"
SCAN_CONFIG_SHA256 = "9e66540bf992931a74bf926200494b6b9ac333b6b7d4e1abe71f2e529422d97a"
BINARY_SUM = 'echo "${BINARY_SHA256}  ${tool}" | sha256sum -c -'
CONFIG_SUM = 'echo "${SCAN_CONFIG_SHA256}  ${scan_config}" | sha256sum -c -'
EXTRACT_CALL = "python3 - \"${tool}\" \"${embedded}\" << 'PY'"
SCAN_CONFIG_ASSIGN = 'scan_config="${RUNNER_TEMP}/scan-config.toml"'
GEN_CALL = 'python3 scripts/scan-config.py --input "${embedded}" --output "${scan_config}"'
ALLOWED_CONFIG_VALUES = ("${scan_config}", "${RUNNER_TEMP}/scan-config.toml")
RANGE_ASSIGNMENTS = (
    'range=""',
    'range="${BASE_SHA}..${HEAD_SHA}"',
    'range="${BEFORE_SHA}..${AFTER_SHA}"',
)
PR_FILTERS = ("paths:", "paths-ignore:", "branches:", "branches-ignore:")
LOG_OPTS = "--log-opts=--text ${range}"
SCANNER_MODES = {"dir", "git", "detect", "protect", "stdin"}
LONG_FORBIDDEN = {
    "--gitleaks-ignore-path",
    "--exit-code",
    "--baseline-path",
    "--enable-rule",
    "--max-target-megabytes",
}
SHORT_FORBIDDEN = {"-c", "-i", "-b"}
_INLINE_EVENT = re.compile(r"\$\{\{\s*(github|inputs)\b")
_OR_TRUE = re.compile(r"\|\|\s*true\b")
_OR_COLON = re.compile(r"\|\|\s*:")


def _dedent_block(lines: list[str]) -> str:
    indents = [len(line) - len(line.lstrip(" ")) for line in lines if line.strip()]
    trim = min(indents) if indents else 0
    trimmed: list[str] = []
    for line in lines:
        if line.strip():
            trimmed.append(line[trim:])
        else:
            trimmed.append("")
    return "\n".join(trimmed).strip("\n")


def _run_scripts(text: str) -> list[str]:
    lines = text.splitlines()
    scripts: list[str] = []
    index = 0
    while index < len(lines):
        match = re.match(r"^(\s*)run:(.*)$", lines[index])
        if not match:
            index += 1
            continue
        indent = len(match.group(1))
        rest = match.group(2).strip()
        if rest in {"|", "|-", "|+", ">", ">-", ">+"}:
            body: list[str] = []
            index += 1
            while index < len(lines):
                line = lines[index]
                if line.strip() == "":
                    body.append("")
                    index += 1
                    continue
                current = len(line) - len(line.lstrip(" "))
                if current <= indent:
                    break
                body.append(line)
                index += 1
            scripts.append(_dedent_block(body))
            continue
        scripts.append(rest)
        index += 1
    return scripts


def _named_step_block(text: str, step_name: str) -> str:
    lines = text.splitlines()
    header = f"- name: {step_name}"
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue
        indent = len(line) - len(line.lstrip(" "))
        block = [line]
        for next_line in lines[index + 1 :]:
            if next_line.strip():
                current = len(next_line) - len(next_line.lstrip(" "))
                if current <= indent:
                    break
            block.append(next_line)
        return "\n".join(block)
    raise AssertionError(f"workflow is missing the {step_name} step")


def _named_step_script(text: str, step_name: str) -> str:
    scripts = _run_scripts(_named_step_block(text, step_name))
    if len(scripts) != 1:
        raise AssertionError(f"{step_name} must have one run script, found {len(scripts)}")
    return scripts[0]


def _step_index(text: str, step_name: str) -> int:
    header = f"- name: {step_name}"
    for index, line in enumerate(text.splitlines()):
        if line.strip() == header:
            return index
    raise AssertionError(f"workflow is missing the {step_name} step")


def _guard_snippet(text: str) -> str:
    script = _named_step_script(text, GUARD_STEP)
    start = script.find(GUARD_START)
    end = script.find(GUARD_END)
    if start < 0 or end < 0 or end <= start:
        raise AssertionError("committed config guard snippet markers are missing")
    return script[start:end]


def _logical_lines(script: str) -> list[str]:
    continued: list[str] = []
    buf: list[str] = []
    for line in script.splitlines():
        buf.append(line)
        if line.rstrip().endswith("\\"):
            continue
        continued.append("\n".join(buf))
        buf = []
    if buf:
        continued.append("\n".join(buf))
    logical: list[str] = []
    for command in continued:
        if logical and command.lstrip().startswith("||"):
            logical[-1] = logical[-1] + "\n" + command
        else:
            logical.append(command)
    return logical


def _flat_command(command: str) -> str:
    return re.sub(r"\\[ \t]*\n", " ", command)


def _tokens(command: str) -> list[str]:
    flat = _flat_command(command)
    try:
        return shlex.split(flat, posix=True)
    except ValueError as exc:
        raise AssertionError(f"could not parse a secret scan command: {flat}") from exc


def _is_scanner_binary(token: str) -> bool:
    return token in {"${tool}", "gitleaks"} or token.endswith("/gitleaks")


def _scanner_calls(script: str) -> list[list[str]]:
    calls: list[list[str]] = []
    for logical in _logical_lines(script):
        tokens = _tokens(logical)
        for index, token in enumerate(tokens):
            if not _is_scanner_binary(token):
                continue
            rest = tokens[index + 1 :]
            if rest and rest[0] in SCANNER_MODES:
                calls.append(tokens[index:])
            break
    return calls


def _require_scanner_calls(script: str) -> list[list[str]]:
    calls = _scanner_calls(script)
    modes = [call[1] for call in calls if len(call) > 1]
    if modes.count("dir") < 1 or modes.count("git") < 1:
        raise AssertionError("secret scan must keep both the directory call and the git range call")
    return calls


def _forbidden_on_call(call: list[str]) -> str | None:
    for token in call:
        if token.startswith("--"):
            name = token.split("=", 1)[0]
            if name in LONG_FORBIDDEN:
                return token
            continue
        for short in SHORT_FORBIDDEN:
            if token == short or token.startswith(short):
                return short
    return None


def _is_checksum(command: str) -> bool:
    tokens = _tokens(command)
    return "sha256sum" in tokens and "-c" in tokens


def _permission_entries(text: str) -> list[str]:
    lines = text.splitlines()
    entries: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" ")) if line.strip() else 0
        if stripped in {"permissions: write-all", "permissions: read-all"}:
            entries.append(stripped)
            index += 1
            continue
        if stripped != "permissions:":
            index += 1
            continue
        index += 1
        while index < len(lines):
            nxt = lines[index]
            if nxt.strip() == "":
                index += 1
                continue
            nxt_indent = len(nxt) - len(nxt.lstrip(" "))
            if nxt_indent <= indent:
                break
            entries.append(nxt.strip())
            index += 1
    return entries


def _run_guard(snippet: str, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-c", snippet],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def _step_mapping_keys(block: str) -> list[str]:
    lines = block.splitlines()
    key_indent = None
    keys: list[str] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if key_indent is None:
            key_indent = indent
        if indent != key_indent:
            continue
        stripped = line.strip()
        if re.match(r"^[A-Za-z0-9_-]+\s*:", stripped):
            keys.append(stripped)
    return keys


def _unit_step(text: str) -> tuple[str, str, int]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != f"- name: {UNIT_STEP}":
            continue
        block = _named_step_block(text, UNIT_STEP)
        script = _named_step_script(text, UNIT_STEP)
        if UNIT_CMD not in script:
            break
        return block, script, index
    raise AssertionError(
        "the unit-test step that runs python3 -m unittest discover -s tests must stay"
    )


def _watched_scripts(text: str) -> list[tuple[str, str]]:
    return [
        ("committed config guard", _named_step_script(text, GUARD_STEP)),
        ("commit trailer check", _named_step_script(text, TRAILER_STEP)),
        ("secret scan", _named_step_script(text, SCAN_STEP)),
        ("unit test", _unit_step(text)[1]),
    ]


def _assert_guard_present(text: str) -> None:
    if _step_index(text, GUARD_STEP) >= _step_index(text, SCAN_STEP):
        raise AssertionError("committed config guard must run before the secret scan")
    snippet = _guard_snippet(text)
    if "find ." not in snippet:
        raise AssertionError("guard must search the whole working tree")
    if "-name .git" not in snippet or "-prune" not in snippet:
        raise AssertionError("guard must prune .git directories")
    if "-name '.gitleaks*'" not in snippet:
        raise AssertionError("guard must refuse every name that starts with .gitleaks")
    if "-type" in snippet:
        raise AssertionError("guard must refuse every entry type, not only files and symlinks")
    if "set -euo pipefail" not in snippet:
        raise AssertionError("set -euo pipefail was removed from the committed config guard")
    if '>"${found_file}"' not in snippet:
        raise AssertionError("a find error must fail the guard step")
    if _OR_TRUE.search(snippet) or _OR_COLON.search(snippet):
        raise AssertionError("the guard must not swallow a find error")
    if GUARD_FAIL not in snippet:
        raise AssertionError("guard must fail with a clear message")
    for key in _step_mapping_keys(_named_step_block(text, GUARD_STEP)):
        if key.startswith("if:"):
            raise AssertionError("if: was added to the committed config guard")


def _assert_bare_redact(text: str) -> None:
    calls = _require_scanner_calls(_named_step_script(text, SCAN_STEP))
    for call in calls:
        if "--redact" not in call:
            raise AssertionError(
                "--redact was removed from scanner call: " + " ".join(call)
            )
        for index, token in enumerate(call):
            if token.startswith("--redact") and token != "--redact":
                raise AssertionError(
                    "only a bare --redact is allowed on scanner call: " + " ".join(call)
                )
            if token == "--redact" and index + 1 < len(call) and not call[index + 1].startswith("-"):
                raise AssertionError(
                    "only a bare --redact is allowed on scanner call: " + " ".join(call)
                )


def _assert_ignore_allow(text: str) -> None:
    calls = _require_scanner_calls(_named_step_script(text, SCAN_STEP))
    for call in calls:
        if "--ignore-gitleaks-allow" not in call:
            raise AssertionError(
                "--ignore-gitleaks-allow was removed from scanner call: " + " ".join(call)
            )


def _assert_scan_pipefail(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    if "set -euo pipefail" not in script:
        raise AssertionError("set -euo pipefail was removed from the secret scan step")


def _assert_no_swallow(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    for logical in _logical_lines(script):
        flat = _flat_command(logical)
        if _OR_TRUE.search(flat) is None and _OR_COLON.search(flat) is None:
            continue
        if _is_checksum(logical):
            raise AssertionError("|| true or || : was added after the sha256sum -c check")
        if _scanner_calls(logical):
            raise AssertionError("|| true or || : was added after a scanner call")


def _assert_no_continue_on_error(text: str) -> None:
    if re.search(r"continue-on-error", text):
        raise AssertionError("continue-on-error was added to the workflow")


def _assert_triggers(text: str) -> None:
    if re.search(r"\bworkflow_run\b", text):
        raise AssertionError("workflow_run was added as a trigger")
    if re.search(r"\bpull_request_target\b", text):
        raise AssertionError("pull_request_target was added as a trigger")


def _assert_checksum_before_extract(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    check_at = script.find("sha256sum -c")
    extract_at = script.find("tar -xzf")
    if check_at < 0:
        raise AssertionError("sha256sum -c check was removed from the secret scan step")
    if extract_at < 0:
        raise AssertionError("archive extract is missing from the secret scan step")
    if check_at > extract_at:
        raise AssertionError("sha256sum -c was moved after extract")


def _assert_permissions(text: str) -> None:
    entries = _permission_entries(text)
    if not entries:
        raise AssertionError("contents: read permission was removed")
    for entry in entries:
        if entry != "contents: read":
            raise AssertionError(f"contents: read was widened by {entry}")


def _assert_env_unset(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    if UNSET_LINE not in script:
        raise AssertionError(
            "secret scan must keep unset GITLEAKS_CONFIG GITLEAKS_CONFIG_TOML"
        )
    if text.count(UNSET_LINE) != 1:
        raise AssertionError("unset GITLEAKS_CONFIG GITLEAKS_CONFIG_TOML must appear once")
    remainder = text.replace(UNSET_LINE, "", 1)
    if "GITLEAKS_CONFIG" in remainder:
        raise AssertionError(
            "GITLEAKS_CONFIG or GITLEAKS_CONFIG_TOML is set outside the required unset"
        )


def _config_values(call: list[str]) -> list[str]:
    values: list[str] = []
    index = 0
    while index < len(call):
        token = call[index]
        if token in {"--config", "-c"}:
            if index + 1 >= len(call):
                raise AssertionError("config flag without a path: " + " ".join(call))
            value = call[index + 1]
            if token == "-c" or value not in ALLOWED_CONFIG_VALUES:
                raise AssertionError(f"scanner call gained {token} {value}")
            values.append(value)
            index += 2
            continue
        if token.startswith("--config=") or token.startswith("-c="):
            raise AssertionError(f"scanner call gained {token}")
        index += 1
    return values


def _embedded_extractor(script: str) -> str:
    marker = EXTRACT_CALL + "\n"
    start = script.find(marker)
    if start < 0:
        raise AssertionError("the shell must write the embedded config before the script runs")
    body_at = start + len(marker)
    end = script.find("\nPY\n", body_at)
    if end < 0:
        raise AssertionError("embedded config extractor is missing its end marker")
    body = script[body_at:end]
    if "scan-config" in body or "scripts" in body:
        raise AssertionError("the embedded config extractor calls the checkout script")
    return body


def _assert_shell_integrity(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    if f'BINARY_SHA256: "{BINARY_SHA256}"' not in text:
        raise AssertionError("binary sha256 pin was removed")
    if f'SCAN_CONFIG_SHA256: "{SCAN_CONFIG_SHA256}"' not in text:
        raise AssertionError("scan config sha256 pin was removed")
    if "SOURCE_SHA256" in text or "--binary" in text or "--source-sha256" in text or "--output-sha256" in text:
        raise AssertionError("the workflow passes a binary path or a hash into the checkout script")
    if script.count(SUM_LINE) != 1:
        raise AssertionError("archive sha256sum -c must appear once")
    if script.count(BINARY_SUM) != 2:
        raise AssertionError("binary sha256sum -c must run before the script and again before the scanner")
    if script.count(CONFIG_SUM) != 1:
        raise AssertionError("scan config sha256sum -c must appear once")
    for line in script.splitlines():
        if "scripts/scan-config.py" not in line:
            continue
        if line.strip() != GEN_CALL or "${tool}" in line or "--binary" in line:
            raise AssertionError("the scan config script was given the binary path")
    archive_at = script.find(SUM_LINE)
    tar_at = script.find(TAR_LINE)
    first_bin = script.find(BINARY_SUM)
    second_bin = script.find(BINARY_SUM, first_bin + len(BINARY_SUM))
    extract_at = script.find(EXTRACT_CALL)
    gen_at = script.find(GEN_CALL)
    config_at = script.find(CONFIG_SUM)
    dir_at = script.find(DIR_CALL)
    git_at = script.find(GIT_CALL)
    if not (
        0
        <= archive_at
        < tar_at
        < first_bin
        < extract_at
        < gen_at
        < config_at
        < second_bin
        < dir_at
        < git_at
    ):
        raise AssertionError("a sha256sum -c check was removed or moved after the file it protects")
    if "python3" in script[config_at + len(CONFIG_SUM) :] or "scripts/" in script[config_at + len(CONFIG_SUM) :]:
        raise AssertionError("a checkout script runs after the config checksum")
    _embedded_extractor(script)
    for logical in _logical_lines(script):
        if not _is_checksum(logical):
            continue
        flat = _flat_command(logical)
        if _OR_TRUE.search(flat) or _OR_COLON.search(flat) or "set +e" in flat:
            raise AssertionError("sha256sum -c was softened")


def _assert_ci_config(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    _assert_shell_integrity(text)
    if "useDefault" in text or "[extend]" in text:
        raise AssertionError("the workflow extends the default config")
    if script.count(SCAN_CONFIG_ASSIGN) != 1:
        raise AssertionError("scan config must be assigned once, at the CI temp path")
    if script.count("scan-config.toml") != 1:
        raise AssertionError("scan config file location changed")
    if script.count(GEN_CALL) != 1 or script.count("scripts/scan-config.py") != 1:
        raise AssertionError("scan config must be generated once, without the binary path")
    if script.count('"${scan_config}"') != 3:
        raise AssertionError("scan config path is used outside the generator and the two scanner calls")
    assign_at = script.find(SCAN_CONFIG_ASSIGN)
    gen_at = script.find(GEN_CALL)
    dir_at = script.find(DIR_CALL)
    git_at = script.find(GIT_CALL)
    if not (0 <= assign_at < gen_at < dir_at < git_at):
        raise AssertionError("scan config must be written before either scanner call")
    calls = _require_scanner_calls(script)
    if [call[1] for call in calls] != ["dir", "git"]:
        raise AssertionError("secret scan must be one directory call and one git range call")
    for call in calls:
        values = _config_values(call)
        if values != ["${scan_config}"]:
            raise AssertionError("scanner call must use only the CI config: " + " ".join(call))


def _assert_no_forbidden_flags(text: str) -> None:
    _assert_ci_config(text)
    calls = _require_scanner_calls(_named_step_script(text, SCAN_STEP))
    for call in calls:
        found = _forbidden_on_call(call)
        if found:
            raise AssertionError(f"scanner call gained {found}: {' '.join(call)}")


def _assert_text_before_range(text: str) -> None:
    calls = _require_scanner_calls(_named_step_script(text, SCAN_STEP))
    git_calls = [call for call in calls if len(call) > 1 and call[1] == "git"]
    if len(git_calls) != 1:
        raise AssertionError("secret scan must keep one git range call")
    opts = [token for token in git_calls[0] if token.startswith("--log-opts")]
    if opts != [LOG_OPTS]:
        raise AssertionError("git log opts must put --text in front of the range")
    dir_calls = [call for call in calls if len(call) > 1 and call[1] == "dir"]
    for call in dir_calls:
        if any(token == "--text" or token.startswith("--text") for token in call):
            raise AssertionError("directory scan must not take --text")


def _assert_no_early_success(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    git_at = script.find(GIT_CALL)
    if git_at < 0:
        raise AssertionError("git scan is missing")
    if re.search(r"\bexit\s+0\b", script[:git_at]):
        raise AssertionError("the scan step exits 0 before the scanner runs")


def _assert_range_assignments(text: str) -> None:
    script = _named_step_script(text, SCAN_STEP)
    found = re.findall(r"(?m)^\s*(range\s*(?:\+?=).*)$", script)
    normalized = [re.sub(r"\s+", "", item) for item in found]
    expected = [item.replace(" ", "") for item in RANGE_ASSIGNMENTS]
    if normalized != expected:
        raise AssertionError("range was cleared or overwritten before the git call")
    if re.search(r"(?m)^\s*unset\s+range\b", script):
        raise AssertionError("range was unset before the git call")
    calls = _require_scanner_calls(script)
    git_calls = [call for call in calls if len(call) > 1 and call[1] == "git"]
    if len(git_calls) != 1 or LOG_OPTS not in git_calls[0]:
        raise AssertionError("git call lost the range")


def _pull_request_body(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped != "pull_request:" and not stripped.startswith("pull_request:"):
            continue
        if stripped.startswith("pull_request_target"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        inline = stripped[len("pull_request:") :].strip()
        body = [inline] if inline else []
        for nxt in lines[index + 1 :]:
            if nxt.strip() == "":
                continue
            current = len(nxt) - len(nxt.lstrip(" "))
            if current <= indent:
                break
            body.append(nxt.strip())
        return "\n".join(body)
    raise AssertionError("pull_request trigger is missing")


def _assert_pull_request_unfiltered(text: str) -> None:
    body = _pull_request_body(text)
    for line in body.splitlines():
        for key in PR_FILTERS:
            if re.search(r"(?:^|[\s{,])" + re.escape(key), line):
                raise AssertionError(f"pull_request gained {key}")


def _scan_config_module():
    path = ROOT / "scripts" / "scan-config.py"
    spec = importlib.util.spec_from_file_location("scan_config", path)
    if spec is None or spec.loader is None:
        raise AssertionError("scan config script could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _rule_path_count(data: dict) -> int:
    count = 0
    for rule in data.get("rules", []):
        groups = list(rule.get("allowlists") or [])
        single = rule.get("allowlist")
        if isinstance(single, dict):
            groups.append(single)
        count += sum(1 for group in groups if "paths" in group)
    return count


_TOOL: Path | None = None


def _pinned_tool() -> Path:
    global _TOOL
    if _TOOL is not None and _TOOL.is_file():
        return _TOOL
    text = WORKFLOW.read_text(encoding="utf-8")
    script = _named_step_script(text, SCAN_STEP)
    match = re.search(r'url="([^"]+)"', script)
    if match is None:
        raise AssertionError("archive url missing")
    url = match.group(1).replace("${version}", "8.30.1")
    cache = Path(tempfile.gettempdir()) / "hygiene-scan-8.30.1"
    cache.mkdir(exist_ok=True)
    archive = cache / "archive.tar.gz"
    tool = cache / "gitleaks"
    if not tool.is_file():
        subprocess.run(["curl", "-fsSL", "-o", str(archive), url], check=True)
        checksum = subprocess.run(
            ["sha256sum", "-c", "-"],
            input=f"{ARCHIVE_SHA256}  {archive}\n",
            text=True,
            capture_output=True,
            check=False,
        )
        if checksum.returncode != 0:
            raise AssertionError("pinned archive checksum failed")
        subprocess.run(["tar", "-xzf", str(archive), "-C", str(cache), "gitleaks"], check=True)
        tool.chmod(0o755)
    _TOOL = tool
    return tool


def _integrity_sequence(workflow_text: str, mode: str) -> dict[str, object]:
    tool = _pinned_tool()
    archive = tool.parent / "archive.tar.gz"
    if not archive.is_file():
        raise AssertionError("pinned archive is missing from the tool cache")
    extractor = _embedded_extractor(_named_step_script(workflow_text, SCAN_STEP))
    generator = ROOT / "scripts" / "scan-config.py"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        binary = root / "gitleaks"
        binary.write_bytes(tool.read_bytes())
        embedded = root / "embedded-config.toml"
        scan_config = root / "scan-config.toml"
        if mode == "bad-script":
            generator = root / "bad-scan-config.py"
            generator.write_text(
                "import pathlib\n"
                "import sys\n"
                "out = pathlib.Path(sys.argv[sys.argv.index('--output') + 1])\n"
                "out.write_text('title = \"changed\"\\n', encoding='utf-8')\n",
                encoding="utf-8",
            )
        shell = (
            "set -euo pipefail\n"
            'echo "$ARCHIVE_SHA256  $archive" | sha256sum -c -\n'
            'if [ "$MODE" = "swap-before" ]; then printf \'x\' >> "$tool"; fi\n'
            'echo "$BINARY_SHA256  $tool" | sha256sum -c -\n'
            'python3 - "$tool" "$embedded" << \'PY\'\n'
            + extractor
            + "\nPY\n"
            'python3 "$script" --input "$embedded" --output "$scan_config"\n'
            'if [ "$MODE" = "edit-config" ]; then printf \'\\n# tamper\\n\' >> "$scan_config"; fi\n'
            'if [ "$MODE" = "swap-after" ]; then printf \'x\' >> "$tool"; fi\n'
            'echo "$SCAN_CONFIG_SHA256  $scan_config" | sha256sum -c -\n'
            'echo "$BINARY_SHA256  $tool" | sha256sum -c -\n'
        )
        env = os.environ.copy()
        env.update(
            {
                "ARCHIVE_SHA256": ARCHIVE_SHA256,
                "BINARY_SHA256": BINARY_SHA256,
                "SCAN_CONFIG_SHA256": SCAN_CONFIG_SHA256,
                "MODE": mode,
                "archive": str(archive),
                "tool": str(binary),
                "embedded": str(embedded),
                "scan_config": str(scan_config),
                "script": str(generator),
            }
        )
        completed = subprocess.run(
            ["bash", "-c", shell],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "code": completed.returncode,
            "report": completed.stdout + completed.stderr,
            "config_exists": scan_config.exists(),
        }


def _runtime_token() -> str:
    alphabet = "QPZRY9X8GF2TVDW0S3JN54KHCE6MUA7L"
    return "AGE-SECRET-KEY-1" + "".join(secrets.choice(alphabet) for _ in range(58))


def _scan_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GITLEAKS_CONFIG", None)
    env.pop("GITLEAKS_CONFIG_TOML", None)
    return env


def _git(root: Path, *args: str, secret: str = "") -> None:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        err = completed.stderr.replace(secret, "<redacted>") if secret else completed.stderr
        raise AssertionError("git command failed: " + err[:400])


def _assert_no_inline(text: str) -> None:
    for script in _run_scripts(text):
        match = _INLINE_EVENT.search(script)
        if match:
            raise AssertionError(
                "a run script inlines "
                + match.group(0)
                + "; event values must reach scripts through env only"
            )


def _assert_no_errexit_bypass(text: str) -> None:
    for label, script in _watched_scripts(text):
        if _OR_COLON.search(script):
            raise AssertionError(f"|| : was added in the {label} step")
        if "set +e" in script:
            raise AssertionError(f"set +e was added in the {label} step")


def _assert_no_if_on_scan_steps(text: str) -> None:
    for name in (GUARD_STEP, SCAN_STEP):
        for key in _step_mapping_keys(_named_step_block(text, name)):
            if key.startswith("if:"):
                raise AssertionError(f"if: was added to the {name} step")


def _assert_unit_test_step(text: str) -> None:
    _block, script, index = _unit_step(text)
    if _OR_TRUE.search(script) or _OR_COLON.search(script):
        raise AssertionError("|| true or || : was added to the unit-test step")
    if "set +e" in script:
        raise AssertionError("set +e was added to the unit-test step")
    if "continue-on-error" in _block:
        raise AssertionError("continue-on-error was added to the unit-test step")
    if not (index < _step_index(text, GUARD_STEP) < _step_index(text, SCAN_STEP)):
        raise AssertionError("unit-test step must stay before the guard and the secret scan")


def _reject(case: unittest.TestCase, check, mutated: str, label: str) -> None:
    with case.subTest(bad_edit=label):
        try:
            check(mutated)
        except AssertionError:
            return
        raise AssertionError(f"bad edit was accepted: {label}")


def _assert_trailer_step(text: str) -> None:
    header = f"- name: {TRAILER_STEP}"
    if text.count(header) != 1:
        raise AssertionError("commit trailer check must exist once")
    guard_at = _step_index(text, GUARD_STEP)
    trailer_at = _step_index(text, TRAILER_STEP)
    scan_at = _step_index(text, SCAN_STEP)
    if not (guard_at < trailer_at < scan_at):
        raise AssertionError("commit trailer check must sit between the guard and the secret scan")
    block = _named_step_block(text, TRAILER_STEP)
    script = _named_step_script(text, TRAILER_STEP)
    if "set -euo pipefail" not in script:
        raise AssertionError("set -euo pipefail was removed from the commit trailer check")
    for key in (
        "EVENT_NAME: ${{ github.event_name }}",
        "BASE_SHA: ${{ github.event.pull_request.base.sha }}",
        "HEAD_SHA: ${{ github.event.pull_request.head.sha }}",
        "BEFORE_SHA: ${{ github.event.before }}",
        "AFTER_SHA: ${{ github.event.after }}",
    ):
        if key not in block:
            raise AssertionError("commit trailer check must read shas through env: " + key.split(":", 1)[0])
    if "env:" not in _step_mapping_keys(block):
        raise AssertionError("commit trailer check is missing env:")
    if _INLINE_EVENT.search(script):
        raise AssertionError("commit trailer check inlines an event expression")
    for name in ("${EVENT_NAME}", "${BASE_SHA}", "${HEAD_SHA}", "${BEFORE_SHA}", "${AFTER_SHA}"):
        if name not in script:
            raise AssertionError("commit trailer check script does not read " + name)
    if "git rev-list" not in script:
        raise AssertionError("commit trailer check must list the range with git rev-list")
    if "--no-merges" in script:
        raise AssertionError("commit trailer check dropped merge commits")
    if "git show -s --format=%B" not in script:
        raise AssertionError("commit trailer check must read the full message")
    if TRAILER_SKIP not in script:
        raise AssertionError("a push with an empty before must print the skip line")
    if TRAILER_FAIL not in script:
        raise AssertionError("commit trailer check must print a fixed failure message")
    if "scripts/" in script or "python" in script:
        raise AssertionError("commit trailer check must stay inline")
    if _OR_TRUE.search(script) or _OR_COLON.search(script) or "set +e" in script:
        raise AssertionError("the commit trailer check exit was softened")
    if "continue-on-error" in block:
        raise AssertionError("continue-on-error was added to the commit trailer check")
    for key in _step_mapping_keys(block):
        if key.startswith("if:"):
            raise AssertionError("if: was added to the commit trailer check")


def _trailer_stem() -> str:
    return "co-" + "authored-by"


def _trailer_key(kind: str) -> str:
    stem = _trailer_stem()
    mixed = stem[0].upper() + stem[1:]
    if kind == "lower":
        return stem
    if kind == "upper":
        return stem.upper()
    if kind == "mixed":
        return mixed
    if kind == "spaced":
        return "  " + mixed
    raise AssertionError(kind)


def _placeholder_address() -> str:
    return "placeholder" + "@" + "example.invalid"


def _trailer_line(kind: str) -> str:
    return _trailer_key(kind) + ": " + "Person <" + _placeholder_address() + ">"


def _sentence_line() -> str:
    return "The draft was " + "co-" + "authored during review for " + _placeholder_address() + "."


def _midline_note() -> str:
    return "See the note " + _trailer_line("lower")


def _commit_message(title: str, *lines: str) -> str:
    return "\n".join([title, "", *lines]) + "\n"


def _init_repo(root: Path) -> None:
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "scan@localhost")
    _git(root, "config", "user.name", "scan")


def _commit(root: Path, name: str, text: str, message: str) -> str:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    _git(root, "add", name)
    msg = root / ".git" / "COMMIT_EDITMSG_TEST"
    msg.write_text(message if message.endswith("\n") else message + "\n", encoding="utf-8")
    _git(root, "commit", "-q", "-F", str(msg))
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def _short_sha(root: Path, sha: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "--short", sha],
        text=True,
    ).strip()


def _fail_line(root: Path, sha: str) -> str:
    return _short_sha(root, sha) + " " + TRAILER_FAIL


def _trailer_env(**overrides: str) -> dict[str, str]:
    env = os.environ.copy()
    for key in ("EVENT_NAME", "BASE_SHA", "HEAD_SHA", "BEFORE_SHA", "AFTER_SHA"):
        env.pop(key, None)
    env.update(overrides)
    return env


def _pr_env(base: str, head: str) -> dict[str, str]:
    return _trailer_env(
        EVENT_NAME="pull_request",
        BASE_SHA=base,
        HEAD_SHA=head,
        BEFORE_SHA="",
        AFTER_SHA="",
    )


def _push_env(before: str, after: str) -> dict[str, str]:
    return _trailer_env(
        EVENT_NAME="push",
        BASE_SHA="",
        HEAD_SHA="",
        BEFORE_SHA=before,
        AFTER_SHA=after,
    )


def _run_trailer(script: str, root: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-c", script],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _assert_hides_trailer(case: unittest.TestCase, result: subprocess.CompletedProcess[str]) -> None:
    blob = result.stdout + result.stderr
    case.assertFalse(
        _placeholder_address() in blob,
        "step output contained the placeholder address",
    )
    case.assertFalse(
        _trailer_stem() in blob.lower(),
        "step output contained the trailer key",
    )


def _place(root: Path, relative: str, kind: str) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if kind == "file":
        target.write_text("skip\n", encoding="utf-8")
    elif kind == "dir":
        target.mkdir()
    elif kind == "symlink-file":
        real = target.parent / "real-file"
        real.write_text("skip\n", encoding="utf-8")
        target.symlink_to(real.name)
    elif kind == "symlink-dir":
        real = target.parent / "real-dir"
        real.mkdir()
        target.symlink_to(real.name)
    elif kind == "broken-symlink":
        target.symlink_to("missing-target")
    else:
        raise AssertionError(f"unknown guard entry kind: {kind}")


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
        scan = _named_step_script(self.text, SCAN_STEP)
        self.assertNotIn(
            ".gitleaksignore",
            scan,
            "secret scan must not reference an ignore file",
        )
        self.assertNotIn("allowlist", self.text)
        self.assertIn(ZERO_SHA, self.text)
        self.assertIn("push range skipped", self.text)
        self.assertIn("${BASE_SHA}..${HEAD_SHA}", self.text)
        self.assertIn("${BEFORE_SHA}..${AFTER_SHA}", self.text)

    def test_committed_config_guard_is_present(self) -> None:
        _assert_guard_present(self.text)
        _reject(
            self,
            _assert_guard_present,
            self.text.replace("-name '.gitleaks*'", "-name '.gitleaks.toml'", 1),
            "narrow the guard to .gitleaks.toml",
        )
        _reject(
            self,
            _assert_guard_present,
            self.text.replace(
                " -print -quit >\"${found_file}\"",
                " -print -quit >\"${found_file}\" || true",
                1,
            ),
            "|| true after find",
        )

    def test_guard_snippet_rejects_each_name_and_type(self) -> None:
        snippet = _guard_snippet(self.text)
        for name in GUARD_NAMES:
            for kind in GUARD_KINDS:
                for place in (name, f"nested/{name}"):
                    with self.subTest(path=place, kind=kind):
                        with tempfile.TemporaryDirectory() as tmp:
                            root = Path(tmp)
                            _place(root, place, kind)
                            result = _run_guard(snippet, root)
                        self.assertNotEqual(
                            result.returncode,
                            0,
                            f"guard should fail for {kind} {place}\n"
                            f"stdout={result.stdout}\nstderr={result.stderr}",
                        )
                        self.assertIn(GUARD_FAIL, result.stdout, f"guard message missing for {place}")

    def test_guard_snippet_fails_when_find_fails(self) -> None:
        snippet = _guard_snippet(self.text)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blocked = root / "nested" / "blocked"
            blocked.mkdir(parents=True)
            blocked.chmod(0)
            try:
                result = _run_guard(snippet, root)
            finally:
                blocked.chmod(0o755)
        self.assertNotEqual(
            result.returncode,
            0,
            f"a find error must fail the guard\nstdout={result.stdout}\nstderr={result.stderr}",
        )
        self.assertNotIn("no committed config or ignore file", result.stdout)

    def test_guard_snippet_passes_a_clean_tree(self) -> None:
        snippet = _guard_snippet(self.text)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.txt").write_text("plain\n", encoding="utf-8")
            for base in (root / ".git", root / "vendor" / ".git"):
                base.mkdir(parents=True)
                for name in GUARD_NAMES:
                    _place(base, name, "file")
                _place(base, "typed-dir/.gitleaks.toml", "dir")
                _place(base, "typed-link/.gitleaks.json", "symlink-file")
                _place(base, "typed-dirlink/.gitleaks.yaml", "symlink-dir")
                _place(base, "typed-broken/.gitleaks", "broken-symlink")
            result = _run_guard(snippet, root)
        self.assertEqual(
            result.returncode,
            0,
            f"guard should pass when .gitleaks* entries are only inside .git\n"
            f"stdout={result.stdout}\nstderr={result.stderr}",
        )
        self.assertIn("no committed config or ignore file", result.stdout)

    def test_secret_scan_keeps_redact_on_both_calls(self) -> None:
        _assert_bare_redact(self.text)
        _reject(
            self,
            _assert_bare_redact,
            self.text.replace(DIR_CALL, DIR_CALL.replace(" --redact", ""), 1),
            "remove --redact from dir",
        )
        _reject(
            self,
            _assert_bare_redact,
            self.text.replace(GIT_CALL, GIT_CALL.replace(" --redact", ""), 1),
            "remove --redact from git",
        )
        _reject(
            self,
            _assert_bare_redact,
            self.text.replace(DIR_CALL, DIR_CALL.replace(" --redact", " --redact=0"), 1),
            "--redact=0 on dir",
        )
        _reject(
            self,
            _assert_bare_redact,
            self.text.replace(GIT_CALL, GIT_CALL.replace(" --redact", " --redact=100"), 1),
            "--redact=100 on git",
        )
        _reject(
            self,
            _assert_bare_redact,
            self.text.replace(DIR_CALL, DIR_CALL.replace(" --redact ", " --redact 0 "), 1),
            "--redact 0 on dir",
        )

    def test_secret_scan_keeps_ignore_allow_on_both_calls(self) -> None:
        _assert_ignore_allow(self.text)
        _reject(
            self,
            _assert_ignore_allow,
            self.text.replace(DIR_CALL, DIR_CALL.replace(" --ignore-gitleaks-allow", ""), 1),
            "remove --ignore-gitleaks-allow from dir",
        )
        _reject(
            self,
            _assert_ignore_allow,
            self.text.replace(GIT_CALL, GIT_CALL.replace(" --ignore-gitleaks-allow", ""), 1),
            "remove --ignore-gitleaks-allow from git",
        )

    def test_secret_scan_keeps_pipefail(self) -> None:
        _assert_scan_pipefail(self.text)
        _reject(
            self,
            _assert_scan_pipefail,
            self.text.replace(
                "        run: |\n          set -euo pipefail\n          unset GITLEAKS_CONFIG",
                "        run: |\n          unset GITLEAKS_CONFIG",
                1,
            ),
            "remove set -euo pipefail from secret scan",
        )

    def test_secret_scan_does_not_swallow_scanner_or_checksum(self) -> None:
        _assert_no_swallow(self.text)
        _reject(self, _assert_no_swallow, self.text.replace(DIR_CALL, DIR_CALL + " || true", 1), "|| true after dir")
        _reject(self, _assert_no_swallow, self.text.replace(GIT_CALL, GIT_CALL + " || true", 1), "|| true after git")
        _reject(self, _assert_no_swallow, self.text.replace(SUM_LINE, SUM_LINE + " || true", 1), "|| true after sha256sum")
        _reject(self, _assert_no_swallow, self.text.replace(DIR_CALL, DIR_CALL + " || :", 1), "|| : after dir")
        _reject(self, _assert_no_swallow, self.text.replace(SUM_LINE, SUM_LINE + " || :", 1), "|| : after sha256sum")
        _reject(
            self,
            _assert_no_swallow,
            self.text.replace(DIR_CALL + "\n", DIR_CALL + "\n          || :\n", 1),
            "|| : on the next line after dir",
        )

    def test_workflow_has_no_continue_on_error(self) -> None:
        _assert_no_continue_on_error(self.text)
        _reject(
            self,
            _assert_no_continue_on_error,
            self.text.replace(
                "      - name: Secret scan\n",
                "      - name: Secret scan\n        continue-on-error: true\n",
                1,
            ),
            "continue-on-error on secret scan",
        )

    def test_workflow_does_not_add_untrusted_triggers(self) -> None:
        _assert_triggers(self.text)
        _reject(
            self,
            _assert_triggers,
            self.text.replace("on:\n  push:\n", "on:\n  workflow_run:\n    workflows: [\"hygiene-check\"]\n  push:\n", 1),
            "workflow_run trigger",
        )
        _reject(
            self,
            _assert_triggers,
            self.text.replace("  pull_request:\n", "  pull_request:\n  pull_request_target:\n", 1),
            "pull_request_target trigger",
        )

    def test_checksum_runs_before_extract(self) -> None:
        _assert_checksum_before_extract(self.text)
        swapped = self.text.replace(SUM_LINE + "\n          " + TAR_LINE, TAR_LINE + "\n          " + SUM_LINE, 1)
        self.assertNotEqual(swapped, self.text)
        _reject(self, _assert_checksum_before_extract, swapped, "sha256sum after extract")
        _reject(
            self,
            _assert_checksum_before_extract,
            self.text.replace("          " + SUM_LINE + "\n", "", 1),
            "remove sha256sum -c",
        )

    def test_contents_read_is_not_widened(self) -> None:
        _assert_permissions(self.text)
        _reject(
            self,
            _assert_permissions,
            self.text.replace("contents: read", "contents: write", 1),
            "contents: write",
        )
        _reject(
            self,
            _assert_permissions,
            self.text.replace("permissions:\n  contents: read\n", "permissions: write-all\n", 1),
            "permissions: write-all",
        )

    def test_scanner_env_is_unset_and_not_set(self) -> None:
        _assert_env_unset(self.text)
        _reject(
            self,
            _assert_env_unset,
            self.text.replace(
                "name: hygiene-check\n",
                "name: hygiene-check\n\nenv:\n  GITLEAKS_CONFIG: hidden.toml\n",
                1,
            ),
            "workflow env GITLEAKS_CONFIG",
        )
        _reject(
            self,
            _assert_env_unset,
            self.text.replace(
                "  check:\n    runs-on:",
                "  check:\n    env:\n      GITLEAKS_CONFIG_TOML: hidden\n    runs-on:",
                1,
            ),
            "job env GITLEAKS_CONFIG_TOML",
        )
        _reject(
            self,
            _assert_env_unset,
            self.text.replace(UNSET_LINE, UNSET_LINE + "\n          export GITLEAKS_CONFIG=hidden.toml", 1),
            "export GITLEAKS_CONFIG",
        )
        _reject(
            self,
            _assert_env_unset,
            self.text.replace("          " + UNSET_LINE + " || true\n", "", 1),
            "remove unset",
        )

    def test_scanner_calls_do_not_take_config_or_ignore_flags(self) -> None:
        _assert_no_forbidden_flags(self.text)
        edits = {
            "--config": DIR_CALL + " --config hidden.toml",
            "--config=": DIR_CALL + " --config=hidden.toml",
            "-c": DIR_CALL + " -c hidden.toml",
            "-c=": DIR_CALL + " -c=hidden.toml",
            "--gitleaks-ignore-path": GIT_CALL + " --gitleaks-ignore-path .",
            "--gitleaks-ignore-path=": GIT_CALL + " --gitleaks-ignore-path=.",
            "-i": GIT_CALL + " -i .",
            "-i=": GIT_CALL + " -i=.",
            "--exit-code": DIR_CALL + " --exit-code 0",
            "--exit-code=": GIT_CALL + " --exit-code=0",
            "--baseline-path": DIR_CALL + " --baseline-path report.json",
            "--baseline-path=": GIT_CALL + " --baseline-path=report.json",
            "-b": DIR_CALL + " -b report.json",
            "-b=": GIT_CALL + " -b=report.json",
            "--enable-rule": DIR_CALL + " --enable-rule one",
            "--enable-rule=": GIT_CALL + " --enable-rule=one",
            "--max-target-megabytes": DIR_CALL + " --max-target-megabytes 1",
            "--max-target-megabytes=": GIT_CALL + " --max-target-megabytes=1",
        }
        for label, replacement in edits.items():
            source = DIR_CALL if replacement.startswith(DIR_CALL) else GIT_CALL
            _reject(self, _assert_no_forbidden_flags, self.text.replace(source, replacement, 1), label)

    def test_run_scripts_do_not_inline_github_or_inputs(self) -> None:
        _assert_no_inline(self.text)
        _reject(
            self,
            _assert_no_inline,
            self.text.replace(
                "run: python3 scripts/check-hygiene.py",
                "run: python3 scripts/check-hygiene.py ${{ github.head_ref }}",
                1,
            ),
            "inline github expression",
        )
        _reject(
            self,
            _assert_no_inline,
            self.text.replace(
                "run: python3 scripts/build-packs.py",
                "run: python3 scripts/build-packs.py ${{ inputs.name }}",
                1,
            ),
            "inline inputs expression",
        )
        kept = self.text.replace(
            "          EVENT_NAME: ${{ github.event_name }}\n",
            "          EVENT_NAME: ${{ github.event_name }}\n          EXTRA: ${{ github.head_ref }}\n",
            1,
        )
        _assert_no_inline(kept)

    def test_guard_secret_scan_and_unit_test_reject_errexit_bypass(self) -> None:
        _assert_no_errexit_bypass(self.text)
        _reject(
            self,
            _assert_no_errexit_bypass,
            self.text.replace(
                "          printf '%s\\n' \"secret scan config guard: no committed config or ignore file\"\n",
                "          printf '%s\\n' \"secret scan config guard: no committed config or ignore file\" || :\n",
                1,
            ),
            "|| : in the guard",
        )
        _reject(
            self,
            _assert_no_errexit_bypass,
            self.text.replace(
                "          # secret-scan-guard-start\n          set -euo pipefail\n",
                "          # secret-scan-guard-start\n          set -euo pipefail\n          set +e\n",
                1,
            ),
            "set +e in the guard",
        )
        _reject(
            self,
            _assert_no_errexit_bypass,
            self.text.replace(
                "          " + UNSET_LINE + " || true\n",
                "          set +e\n          " + UNSET_LINE + " || true\n",
                1,
            ),
            "set +e in secret scan",
        )
        _reject(
            self,
            _assert_no_errexit_bypass,
            self.text.replace(DIR_CALL, DIR_CALL + " || :", 1),
            "|| : in secret scan",
        )
        _reject(
            self,
            _assert_no_errexit_bypass,
            self.text.replace(UNIT_CMD + " -v", UNIT_CMD + " -v || :", 1),
            "|| : in the unit-test step",
        )
        _reject(
            self,
            _assert_no_errexit_bypass,
            self.text.replace(UNIT_CMD + " -v", "set +e; " + UNIT_CMD + " -v", 1),
            "set +e in the unit-test step",
        )

    def test_guard_and_secret_scan_have_no_if(self) -> None:
        _assert_no_if_on_scan_steps(self.text)
        _assert_guard_present(self.text)
        _reject(
            self,
            _assert_no_if_on_scan_steps,
            self.text.replace(
                "      - name: Committed config guard\n",
                "      - name: Committed config guard\n        if: false\n",
                1,
            ),
            "if: on the guard",
        )
        _reject(
            self,
            _assert_no_if_on_scan_steps,
            self.text.replace(
                "      - name: Secret scan\n",
                "      - name: Secret scan\n        if: false\n",
                1,
            ),
            "if: on secret scan",
        )
        _reject(
            self,
            _assert_guard_present,
            self.text.replace(
                "          # secret-scan-guard-start\n          set -euo pipefail\n",
                "          # secret-scan-guard-start\n",
                1,
            ),
            "remove set -euo pipefail from the guard",
        )

    def test_unit_test_step_stays_before_the_scans(self) -> None:
        _assert_unit_test_step(self.text)
        block = _named_step_block(self.text, UNIT_STEP)
        removed = self.text.replace(block + "\n", "", 1)
        self.assertNotEqual(removed, self.text)
        _reject(self, _assert_unit_test_step, removed, "remove the unit-test step")
        moved = removed.rstrip() + "\n" + block + "\n"
        _reject(self, _assert_unit_test_step, moved, "move the unit-test step after the scans")
        _reject(
            self,
            _assert_unit_test_step,
            self.text.replace(UNIT_CMD + " -v", UNIT_CMD + " -v || true", 1),
            "|| true on the unit-test step",
        )
        _reject(
            self,
            _assert_unit_test_step,
            self.text.replace(UNIT_CMD + " -v", UNIT_CMD + " -v || :", 1),
            "|| : on the unit-test step",
        )
        _reject(
            self,
            _assert_unit_test_step,
            self.text.replace(UNIT_CMD + " -v", "set +e; " + UNIT_CMD + " -v", 1),
            "set +e on the unit-test step",
        )
        _reject(
            self,
            _assert_unit_test_step,
            self.text.replace(
                "      - name: Pack tooling unit tests\n",
                "      - name: Pack tooling unit tests\n        continue-on-error: true\n",
                1,
            ),
            "continue-on-error on the unit-test step",
        )

    def test_only_the_ci_config_path_is_allowed(self) -> None:
        _assert_ci_config(self.text)
        _assert_no_forbidden_flags(self.text)
        _reject(
            self,
            _assert_ci_config,
            self.text.replace('--config "${scan_config}"', "--config hidden.toml", 1),
            "replace the CI config path",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace('--config "${scan_config}"', "--config=${scan_config}", 1),
            "equals-form config flag",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace('--config "${scan_config}"', '-c "${scan_config}"', 1),
            "short config flag with the CI path",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace('--config "${scan_config}"', "-c hidden.toml", 1),
            "short config flag with another path",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(DIR_CALL, DIR_CALL + " --config other.toml", 1),
            "second config on the directory call",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(GIT_CALL, GIT_CALL + ' --config "${scan_config}"', 1),
            "second config on the git call",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(SCAN_CONFIG_ASSIGN, 'scan_config="${RUNNER_TEMP}/other.toml"', 1),
            "move the generated file inside the temp dir",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(SCAN_CONFIG_ASSIGN, 'scan_config="./scan-config.toml"', 1),
            "move the generated file into the checkout",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace('--output "${scan_config}"', '--output "./scan-config.toml"', 1),
            "generator writes into the checkout",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(
                GEN_CALL,
                GEN_CALL + '\n          cp "${scan_config}" ./scan-config.toml',
                1,
            ),
            "copy the generated config into the checkout",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(GEN_CALL + "\n", "", 1),
            "drop the config generator",
        )
        _reject(
            self,
            _assert_ci_config,
            self.text.replace(
                'name: hygiene-check\n',
                'name: hygiene-check\n\nenv:\n  useDefault: "true"\n',
                1,
            ),
            "useDefault in the workflow",
        )

    def test_ci_config_pin_drops_global_paths(self) -> None:
        self.assertIn(f'BINARY_SHA256: "{BINARY_SHA256}"', self.text)
        self.assertIn(f'SCAN_CONFIG_SHA256: "{SCAN_CONFIG_SHA256}"', self.text)
        self.assertNotIn("SOURCE_SHA256", self.text)
        self.assertNotIn("--binary", self.text)
        self.assertNotIn("allowlist", self.text)
        module = _scan_config_module()
        self.assertNotIn("useDefault = true", (ROOT / "scripts" / "scan-config.py").read_text(encoding="utf-8"))
        fixture = (
            "title = \"fixture\"\n"
            "[allowlist]\n"
            "description = \"global\"\n"
            "paths = [\n"
            "    '''skip-me''',\n"
            "]\n"
            "regexes = [\n"
            "    '''^true$''',\n"
            "]\n"
            "[[rules]]\n"
            "id = \"one\"\n"
            "regex = '''abc'''\n"
            "[[rules.allowlists]]\n"
            "paths = [\n"
            "    '''keep-me''',\n"
            "]\n"
        )
        stripped = module.strip_global_paths(fixture)
        parsed = tomllib.loads(stripped)
        self.assertNotIn("paths", parsed["allowlist"])
        self.assertEqual(parsed["rules"][0]["allowlists"][0]["paths"], ["keep-me"])
        self.assertNotIn("skip-me", stripped)
        tool = _pinned_tool()
        self.assertEqual(hashlib.sha256(tool.read_bytes()).hexdigest(), BINARY_SHA256)
        blob = module.extract_embedded_config(tool.read_bytes())
        self.assertEqual(hashlib.sha256(blob).hexdigest(), SOURCE_SHA256)
        built = module.render_config(blob)
        self.assertEqual(hashlib.sha256(built).hexdigest(), SCAN_CONFIG_SHA256)
        source = tomllib.loads(blob.decode("utf-8"))
        result = tomllib.loads(built.decode("utf-8"))
        self.assertEqual(len(source["allowlist"]["paths"]), 25)
        self.assertNotIn("paths", result["allowlist"])
        self.assertNotIn("extend", result)
        self.assertEqual(len(result["rules"]), 222)
        self.assertEqual(len(source["rules"]), len(result["rules"]))
        self.assertEqual(_rule_path_count(source), _rule_path_count(result))
        self.assertEqual(_rule_path_count(result), 3)
        self.assertNotIn(b"useDefault", built)

    def test_log_opts_pin_text_before_the_range(self) -> None:
        _assert_text_before_range(self.text)
        self.assertIn('--log-opts="--text ${range}"', self.text)
        _reject(
            self,
            _assert_text_before_range,
            self.text.replace('--log-opts="--text ${range}"', '--log-opts="${range}"', 1),
            "drop --text",
        )
        _reject(
            self,
            _assert_text_before_range,
            self.text.replace('--log-opts="--text ${range}"', '--log-opts="${range} --text"', 1),
            "--text after the range",
        )

    def test_text_log_opt_sees_a_removed_token(self) -> None:
        tool = _pinned_tool()
        module = _scan_config_module()
        token = _runtime_token()
        with tempfile.TemporaryDirectory() as tmp:
            outer = Path(tmp)
            root = outer / "repo"
            root.mkdir()
            config = outer / "scan-config.toml"
            config.write_bytes(module.render_config(module.extract_embedded_config(tool.read_bytes())))
            _git(root, "init", "-q")
            _git(root, "config", "user.email", "scan@localhost")
            _git(root, "config", "user.name", "scan")
            (root / "base.txt").write_text("base\n", encoding="utf-8")
            _git(root, "add", "base.txt")
            _git(root, "commit", "-q", "-m", "base")
            base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            (root / ".gitattributes").write_text("*.dat -diff\n", encoding="utf-8")
            (root / "notes.dat").write_text(token + "\n", encoding="utf-8")
            _git(root, "add", ".gitattributes", "notes.dat")
            _git(root, "commit", "-q", "-m", "add", secret=token)
            (root / "notes.dat").write_text("cleared\n", encoding="utf-8")
            _git(root, "add", "notes.dat")
            _git(root, "commit", "-q", "-m", "remove", secret=token)
            head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            self.assertFalse(token in (root / "notes.dat").read_text(encoding="utf-8"))
            span = f"{base}..{head}"
            without = self._range_scan(tool, root, config, span, token)
            with_text = self._range_scan(tool, root, config, f"--text {span}", token)
        self.assertEqual(without, 0)
        self.assertEqual(with_text, 1)

    def _range_scan(self, tool: Path, root: Path, config: Path, log_opts: str, token: str) -> int:
        completed = subprocess.run(
            [
                str(tool),
                "git",
                ".",
                "--no-banner",
                "--redact",
                "--ignore-gitleaks-allow",
                "--config",
                str(config),
                f"--log-opts={log_opts}",
            ],
            cwd=root,
            env=_scan_env(),
            capture_output=True,
            check=False,
        )
        if completed.returncode not in {0, 1}:
            safe = (completed.stdout + completed.stderr).replace(token.encode(), b"<redacted>")
            raise AssertionError(f"range scan failed: {safe[:300]!r}")
        return completed.returncode

    def test_scan_step_has_no_early_success_exit(self) -> None:
        _assert_no_early_success(self.text)
        _reject(
            self,
            _assert_no_early_success,
            self.text.replace(
                "          set -euo pipefail\n          unset GITLEAKS_CONFIG",
                "          set -euo pipefail\n          exit 0\n          unset GITLEAKS_CONFIG",
                1,
            ),
            "exit 0 before the scanner",
        )
        _reject(
            self,
            _assert_no_early_success,
            self.text.replace(DIR_CALL + "\n", DIR_CALL + "\n          exit 0\n", 1),
            "exit 0 between the scanner calls",
        )

    def test_range_is_not_cleared_before_the_git_call(self) -> None:
        _assert_range_assignments(self.text)
        _reject(
            self,
            _assert_range_assignments,
            self.text.replace(GIT_CALL, 'range=""\n            ' + GIT_CALL, 1),
            "clear range before the git call",
        )
        _reject(
            self,
            _assert_range_assignments,
            self.text.replace(GIT_CALL, 'range="HEAD"\n            ' + GIT_CALL, 1),
            "overwrite range before the git call",
        )
        _reject(
            self,
            _assert_range_assignments,
            self.text.replace(GIT_CALL, "unset range\n            " + GIT_CALL, 1),
            "unset range before the git call",
        )
        _reject(
            self,
            _assert_range_assignments,
            self.text.replace(
                '{ echo "pull request range is not two commits"; exit 1; }\n'
                '            range="${BASE_SHA}..${HEAD_SHA}"',
                '{ echo "pull request range is not two commits"; exit 1; }\n'
                '            range=""',
                1,
            ),
            "clear the pull request range",
        )

    def test_pull_request_trigger_has_no_path_or_branch_filter(self) -> None:
        _assert_pull_request_unfiltered(self.text)
        self.assertIn("    branches: [main, \"cursor/**\"]", self.text)
        for key in PR_FILTERS:
            _reject(
                self,
                _assert_pull_request_unfiltered,
                self.text.replace(
                    "  pull_request:\n",
                    f"  pull_request:\n    {key}\n      - '*'\n",
                    1,
                ),
                f"{key} on pull_request",
            )
        _reject(
            self,
            _assert_pull_request_unfiltered,
            self.text.replace("  pull_request:\n", "  pull_request: {paths: ['*']}\n", 1),
            "inline paths filter",
        )

    def test_shell_checksums_stay_before_each_use(self) -> None:
        _assert_shell_integrity(self.text)
        first = "          " + BINARY_SUM + "\n          " + EXTRACT_CALL
        second = "          " + BINARY_SUM + "\n          " + DIR_CALL
        config_line = "          " + CONFIG_SUM + "\n"
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(first, "          " + EXTRACT_CALL, 1),
            "remove the binary check that runs before the script",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(second, "          " + DIR_CALL, 1),
            "remove the binary check that runs before the scanner",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(config_line, "", 1),
            "remove the scan config check",
        )
        moved_first = self.text.replace(first, "          " + EXTRACT_CALL, 1).replace(
            GEN_CALL,
            GEN_CALL + "\n          " + BINARY_SUM,
            1,
        )
        self.assertNotEqual(moved_first, self.text)
        _reject(self, _assert_shell_integrity, moved_first, "move the first binary check to after the script")
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(second, "          " + DIR_CALL + "\n          " + BINARY_SUM, 1),
            "move the second binary check to after the directory scan",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(config_line, "").replace(
                DIR_CALL,
                DIR_CALL + "\n          " + CONFIG_SUM,
                1,
            ),
            "move the scan config check to after the directory scan",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(SUM_LINE + "\n          " + TAR_LINE, TAR_LINE + "\n          " + SUM_LINE, 1),
            "move the archive check to after extract",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(first, "          " + BINARY_SUM + " || true\n          " + EXTRACT_CALL, 1),
            "soften the first binary check",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(second, "          " + BINARY_SUM + " || :\n          " + DIR_CALL, 1),
            "soften the second binary check",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(CONFIG_SUM, CONFIG_SUM + " || true", 1),
            "soften the scan config check",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(SUM_LINE, SUM_LINE + " || true", 1),
            "soften the archive check",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(
                GEN_CALL,
                'python3 scripts/scan-config.py --binary "${tool}" --input "${embedded}" --output "${scan_config}"',
                1,
            ),
            "pass --binary to the checkout script",
        )
        _reject(
            self,
            _assert_shell_integrity,
            self.text.replace(
                GEN_CALL,
                'python3 scripts/scan-config.py "${tool}" --input "${embedded}" --output "${scan_config}"',
                1,
            ),
            "pass the binary path to the checkout script",
        )

    def test_tamper_fails_the_shell_checksums(self) -> None:
        clean = _integrity_sequence(self.text, "clean")
        self.assertEqual(clean["code"], 0, clean["report"])
        self.assertTrue(clean["config_exists"])
        bad_script = _integrity_sequence(self.text, "bad-script")
        self.assertNotEqual(bad_script["code"], 0)
        self.assertIn("FAILED", str(bad_script["report"]))
        self.assertIn("scan-config.toml", str(bad_script["report"]))
        self.assertTrue(bad_script["config_exists"])
        edited = _integrity_sequence(self.text, "edit-config")
        self.assertNotEqual(edited["code"], 0)
        self.assertIn("FAILED", str(edited["report"]))
        self.assertIn("scan-config.toml", str(edited["report"]))
        self.assertTrue(edited["config_exists"])
        before = _integrity_sequence(self.text, "swap-before")
        self.assertNotEqual(before["code"], 0)
        self.assertIn("FAILED", str(before["report"]))
        self.assertIn("gitleaks", str(before["report"]))
        self.assertFalse(before["config_exists"])
        after = _integrity_sequence(self.text, "swap-after")
        self.assertNotEqual(after["code"], 0)
        self.assertIn("FAILED", str(after["report"]))
        self.assertIn("gitleaks", str(after["report"]))
        self.assertTrue(after["config_exists"])
        refused = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "scan-config.py"),
                "--binary",
                str(_pinned_tool()),
                "--output",
                "scan-config.toml",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(refused.returncode, 0)

    def test_commit_trailer_check_sits_between_the_guard_and_the_secret_scan(self) -> None:
        _assert_trailer_step(self.text)
        block = _named_step_block(self.text, TRAILER_STEP)
        script = _named_step_script(self.text, TRAILER_STEP)
        removed = self.text.replace(block + "\n", "", 1)
        self.assertNotEqual(removed, self.text)
        self.assertNotIn(f"- name: {TRAILER_STEP}", removed)
        _reject(self, _assert_trailer_step, removed, "remove the commit trailer check")
        scan_block = _named_step_block(self.text, SCAN_STEP)
        moved_after = removed.replace(scan_block, scan_block + "\n" + block, 1)
        self.assertNotEqual(moved_after, self.text)
        _reject(self, _assert_trailer_step, moved_after, "move the commit trailer check after the secret scan")
        guard_block = _named_step_block(removed, GUARD_STEP)
        moved_before = removed.replace(guard_block, block + "\n" + guard_block, 1)
        _reject(self, _assert_trailer_step, moved_before, "move the commit trailer check before the guard")
        _reject(
            self,
            _assert_trailer_step,
            self.text.replace(
                'printf \'%s\\n\' "' + TRAILER_SKIP + '"',
                'printf \'%s\\n\' "' + TRAILER_SKIP + '" || true',
                1,
            ),
            "|| true in the commit trailer check",
        )
        _reject(
            self,
            _assert_trailer_step,
            self.text.replace(
                'printf \'%s\\n\' "' + TRAILER_SKIP + '"',
                'printf \'%s\\n\' "' + TRAILER_SKIP + '" || :',
                1,
            ),
            "|| : in the commit trailer check",
        )
        softened = self.text.replace(
            "          set -euo pipefail\n          is_sha() {",
            "          set +e\n          set -euo pipefail\n          is_sha() {",
            1,
        )
        self.assertNotEqual(softened, self.text)
        _reject(self, _assert_trailer_step, softened, "set +e in the commit trailer check")
        _reject(
            self,
            _assert_trailer_step,
            self.text.replace(
                f"      - name: {TRAILER_STEP}\n",
                f"      - name: {TRAILER_STEP}\n        continue-on-error: true\n",
                1,
            ),
            "continue-on-error on the commit trailer check",
        )
        _reject(
            self,
            _assert_trailer_step,
            self.text.replace(
                f"      - name: {TRAILER_STEP}\n",
                f"      - name: {TRAILER_STEP}\n        if: false\n",
                1,
            ),
            "if: on the commit trailer check",
        )
        self.assertNotIn("|| true", script)
        self.assertNotIn("continue-on-error", block)

    def _trailer_script(self) -> str:
        return _named_step_script(self.text, TRAILER_STEP)

    def test_trailer_check_clean_range_passes(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            base = _commit(root, "base.txt", "base\n", _commit_message("base"))
            head = _commit(root, "notes.txt", "notes\n", _commit_message("Update the notes"))
            cases = {
                "pull_request": _pr_env(base, head),
                "push": _push_env(base, head),
            }
            for label, env in cases.items():
                with self.subTest(event=label):
                    result = _run_trailer(script, root, env)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(result.stderr, "")
                    _assert_hides_trailer(self, result)

    def test_trailer_check_one_trailer_fails(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            base = _commit(root, "base.txt", "base\n", _commit_message("base"))
            bad = _commit(
                root,
                "notes.txt",
                "notes\n",
                _commit_message("Add a note", _trailer_line("mixed")),
            )
            subject = subprocess.check_output(
                ["git", "-C", str(root), "show", "-s", "--format=%s", bad],
                text=True,
            )
            self.assertFalse(_trailer_stem() in subject.lower())
            cases = {
                "pull_request": _pr_env(base, bad),
                "push": _push_env(base, bad),
            }
            for label, env in cases.items():
                with self.subTest(event=label):
                    result = _run_trailer(script, root, env)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertEqual(result.stdout.splitlines(), [_fail_line(root, bad)])
                    self.assertEqual(result.stderr, "")
                    _assert_hides_trailer(self, result)

    def test_trailer_check_case_and_spacing_fail(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            base = _commit(root, "base.txt", "base\n", _commit_message("base"))
            shas = []
            for index, kind in enumerate(("lower", "upper", "spaced")):
                shas.append(
                    _commit(
                        root,
                        f"note-{index}.txt",
                        f"{kind}\n",
                        _commit_message(f"Add note {index}", _trailer_line(kind)),
                    )
                )
            head = shas[-1]
            result = _run_trailer(script, root, _pr_env(base, head))
            listed = subprocess.check_output(
                ["git", "-C", str(root), "rev-list", f"{base}..{head}"],
                text=True,
            ).split()
            self.assertEqual(set(listed), set(shas))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(result.stdout.splitlines(), [_fail_line(root, sha) for sha in listed])
            self.assertEqual(result.stderr, "")
            _assert_hides_trailer(self, result)

    def test_trailer_check_second_of_three_fails(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            base = _commit(root, "base.txt", "base\n", _commit_message("base"))
            first = _commit(root, "one.txt", "one\n", _commit_message("First note"))
            second = _commit(
                root,
                "two.txt",
                "two\n",
                _commit_message("Second note", _trailer_line("mixed")),
            )
            third = _commit(root, "three.txt", "three\n", _commit_message("Third note"))
            result = _run_trailer(script, root, _pr_env(base, third))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(result.stdout.splitlines(), [_fail_line(root, second)])
            self.assertNotIn(_short_sha(root, first), result.stdout)
            self.assertNotIn(_short_sha(root, third), result.stdout)
            self.assertEqual(result.stderr, "")
            _assert_hides_trailer(self, result)

    def test_trailer_check_merge_commit_fails(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            base = _commit(root, "base.txt", "base\n", _commit_message("base"))
            _git(root, "checkout", "-q", "-b", "side")
            side = _commit(root, "side.txt", "side\n", _commit_message("Side note"))
            _git(root, "checkout", "-q", "main")
            _git(root, "merge", "--no-ff", "--no-commit", "side")
            merge = _commit(
                root,
                "merge.txt",
                "merge\n",
                _commit_message("Merge the side branch", _trailer_line("mixed")),
            )
            parents = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", f"{merge}^1", f"{merge}^2"],
                text=True,
            ).split()
            self.assertEqual(len(parents), 2)
            self.assertIn(side, parents)
            result = _run_trailer(script, root, _pr_env(base, merge))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(result.stdout.splitlines(), [_fail_line(root, merge)])
            self.assertNotIn(_short_sha(root, side), result.stdout)
            self.assertEqual(result.stderr, "")
            _assert_hides_trailer(self, result)

    def test_trailer_check_words_inside_a_sentence_pass(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            base = _commit(root, "base.txt", "base\n", _commit_message("base"))
            head = _commit(
                root,
                "notes.txt",
                "notes\n",
                _commit_message("Update the notes", _sentence_line(), _midline_note()),
            )
            result = _run_trailer(script, root, _pr_env(base, head))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")
            _assert_hides_trailer(self, result)

    def test_trailer_check_push_with_zero_before_skips(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            _commit(root, "base.txt", "base\n", _commit_message("base"))
            head = _commit(
                root,
                "notes.txt",
                "notes\n",
                _commit_message("Add a note", _trailer_line("mixed")),
            )
            cases = {
                "zero": _push_env(ZERO_SHA, head),
                "empty": _trailer_env(EVENT_NAME="push", AFTER_SHA=head, BEFORE_SHA=""),
                "missing": _trailer_env(EVENT_NAME="push", AFTER_SHA=head),
            }
            for label, env in cases.items():
                with self.subTest(before=label):
                    self.assertNotIn("BEFORE_SHA", env) if label == "missing" else self.assertIn("BEFORE_SHA", env)
                    result = _run_trailer(script, root, env)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(result.stdout.splitlines(), [TRAILER_SKIP])
                    self.assertNotIn(TRAILER_FAIL, result.stdout)
                    self.assertEqual(result.stderr, "")
                    _assert_hides_trailer(self, result)

    def test_trailer_check_unknown_event_fails(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            _commit(root, "base.txt", "base\n", _commit_message("base"))
            _commit(
                root,
                "notes.txt",
                "notes\n",
                _commit_message("Add a note", _trailer_line("upper")),
            )
            result = _run_trailer(script, root, _trailer_env(EVENT_NAME="schedule"))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout.splitlines(), [TRAILER_EVENT_FAIL])
            self.assertEqual(result.stderr, "")
            _assert_hides_trailer(self, result)

    def test_trailer_check_non_sha_base_fails(self) -> None:
        script = self._trailer_script()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _init_repo(root)
            _commit(root, "base.txt", "base\n", _commit_message("base"))
            head = _commit(
                root,
                "notes.txt",
                "notes\n",
                _commit_message("Add a note", _trailer_line("lower")),
            )
            result = _run_trailer(
                script,
                root,
                _pr_env("not-a-sha", head),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout.splitlines(), [TRAILER_PR_RANGE_FAIL])
            self.assertNotIn(TRAILER_FAIL, result.stdout)
            self.assertEqual(result.stderr, "")
            _assert_hides_trailer(self, result)


if __name__ == "__main__":
    unittest.main()
