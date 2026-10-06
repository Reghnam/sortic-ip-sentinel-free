"""Text checks for the hygiene workflow.

The stdlib has no YAML parser, so these tests read the workflow by indentation.
"""

from __future__ import annotations

import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "hygiene-check.yml"
ARCHIVE_SHA256 = "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
ZERO_SHA = "0000000000000000000000000000000000000000"
GUARD_STEP = "Committed config guard"
SCAN_STEP = "Secret scan"
# Pinned scanner reads these from the target on its own. The only config
# filename is `.gitleaks.toml`. `.gitleaksignore` is the ignore filename.
GUARD_FILENAMES = (".gitleaksignore", ".gitleaks.toml")
GUARD_START = "# secret-scan-guard-start"
GUARD_END = "# secret-scan-guard-end"
GUARD_FAIL = "secret scan refused a committed config or ignore file"
UNSET_LINE = "unset GITLEAKS_CONFIG GITLEAKS_CONFIG_TOML"
SCANNER_MODES = {"dir", "git", "detect", "protect", "stdin"}
FORBIDDEN_SCAN_FLAGS = {"--config", "--gitleaks-ignore-path", "-c", "-i"}
_INLINE_EVENT = re.compile(r"\$\{\{\s*(github|inputs)\b")
_OR_TRUE = re.compile(r"\|\|\s*true\b")


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


def _flag_name(token: str) -> str | None:
    if token.startswith("--"):
        return token.split("=", 1)[0]
    if token.startswith("-") and len(token) > 1:
        return token.split("=", 1)[0]
    return None


def _forbidden_flag(token: str) -> str | None:
    if token.startswith("--"):
        name = token.split("=", 1)[0]
        if name in {"--config", "--gitleaks-ignore-path"}:
            return name
        return None
    for short in ("-c", "-i"):
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
        guard_at = _step_index(self.text, GUARD_STEP)
        scan_at = _step_index(self.text, SCAN_STEP)
        self.assertLess(
            guard_at,
            scan_at,
            "committed config guard must run before the secret scan",
        )
        snippet = _guard_snippet(self.text)
        self.assertIn("find .", snippet, "guard must search the whole working tree")
        self.assertIn("-name .git", snippet, "guard must exclude .git")
        self.assertIn("-prune", snippet, "guard must prune .git directories")
        for name in GUARD_FILENAMES:
            self.assertIn(name, snippet, f"guard must refuse a committed {name}")
        self.assertIn(GUARD_FAIL, snippet, "guard must fail with a clear message")

    def test_guard_snippet_rejects_each_committed_file(self) -> None:
        snippet = _guard_snippet(self.text)
        cases = [
            ".gitleaksignore",
            ".gitleaks.toml",
            "nested/.gitleaksignore",
            "nested/deep/.gitleaks.toml",
        ]
        for relative in cases:
            with self.subTest(path=relative):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("skip\n", encoding="utf-8")
                    result = _run_guard(snippet, root)
                self.assertNotEqual(
                    result.returncode,
                    0,
                    f"guard should fail when {relative} is committed\n"
                    f"stdout={result.stdout}\nstderr={result.stderr}",
                )
                self.assertIn(
                    GUARD_FAIL,
                    result.stdout,
                    f"guard message missing for {relative}",
                )
        with self.subTest(path="symlink"):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "real.toml").write_text("skip\n", encoding="utf-8")
                (root / ".gitleaks.toml").symlink_to("real.toml")
                result = _run_guard(snippet, root)
            self.assertNotEqual(
                result.returncode,
                0,
                "guard should fail when .gitleaks.toml is a symlink",
            )

    def test_guard_snippet_passes_a_clean_tree(self) -> None:
        snippet = _guard_snippet(self.text)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.txt").write_text("plain\n", encoding="utf-8")
            git_dir = root / ".git"
            git_dir.mkdir()
            (git_dir / ".gitleaksignore").write_text("skip\n", encoding="utf-8")
            (git_dir / ".gitleaks.toml").write_text("skip\n", encoding="utf-8")
            nested_git = root / "vendor" / ".git"
            nested_git.mkdir(parents=True)
            (nested_git / ".gitleaks.toml").write_text("skip\n", encoding="utf-8")
            result = _run_guard(snippet, root)
        self.assertEqual(
            result.returncode,
            0,
            f"guard should pass when skip files are absent outside .git\n"
            f"stdout={result.stdout}\nstderr={result.stderr}",
        )
        self.assertIn("no committed config or ignore file", result.stdout)

    def test_secret_scan_keeps_redact_on_both_calls(self) -> None:
        calls = _require_scanner_calls(_named_step_script(self.text, SCAN_STEP))
        for call in calls:
            names = [name for name in (_flag_name(token) for token in call) if name]
            self.assertIn(
                "--redact",
                names,
                f"--redact was removed from scanner call: {' '.join(call)}",
            )

    def test_secret_scan_keeps_ignore_allow_on_both_calls(self) -> None:
        calls = _require_scanner_calls(_named_step_script(self.text, SCAN_STEP))
        for call in calls:
            names = [name for name in (_flag_name(token) for token in call) if name]
            self.assertIn(
                "--ignore-gitleaks-allow",
                names,
                "--ignore-gitleaks-allow was removed from scanner call: " + " ".join(call),
            )

    def test_secret_scan_keeps_pipefail(self) -> None:
        script = _named_step_script(self.text, SCAN_STEP)
        self.assertIn(
            "set -euo pipefail",
            script,
            "set -euo pipefail was removed from the secret scan step",
        )

    def test_secret_scan_does_not_swallow_scanner_or_checksum(self) -> None:
        script = _named_step_script(self.text, SCAN_STEP)
        for logical in _logical_lines(script):
            if _OR_TRUE.search(_flat_command(logical)) is None:
                continue
            self.assertFalse(
                _is_checksum(logical),
                "|| true was added after the sha256sum -c check",
            )
            self.assertFalse(
                bool(_scanner_calls(logical)),
                "|| true was added after a scanner call",
            )

    def test_workflow_has_no_continue_on_error(self) -> None:
        self.assertIsNone(
            re.search(r"continue-on-error", self.text),
            "continue-on-error was added to the workflow",
        )

    def test_workflow_does_not_add_untrusted_triggers(self) -> None:
        self.assertIsNone(
            re.search(r"\bworkflow_run\b", self.text),
            "workflow_run was added as a trigger",
        )
        self.assertIsNone(
            re.search(r"\bpull_request_target\b", self.text),
            "pull_request_target was added as a trigger",
        )

    def test_checksum_runs_before_extract(self) -> None:
        script = _named_step_script(self.text, SCAN_STEP)
        check_at = script.find("sha256sum -c")
        extract_at = script.find("tar -xzf")
        self.assertNotEqual(
            check_at,
            -1,
            "sha256sum -c check was removed from the secret scan step",
        )
        self.assertNotEqual(
            extract_at,
            -1,
            "archive extract is missing from the secret scan step",
        )
        self.assertLess(
            check_at,
            extract_at,
            "sha256sum -c was moved after extract",
        )

    def test_contents_read_is_not_widened(self) -> None:
        entries = _permission_entries(self.text)
        self.assertTrue(entries, "contents: read permission was removed")
        for entry in entries:
            self.assertEqual(
                entry,
                "contents: read",
                f"contents: read was widened by {entry}",
            )

    def test_scanner_env_is_unset_and_not_set(self) -> None:
        script = _named_step_script(self.text, SCAN_STEP)
        self.assertIn(
            UNSET_LINE,
            script,
            "secret scan must keep unset GITLEAKS_CONFIG GITLEAKS_CONFIG_TOML",
        )
        self.assertEqual(
            self.text.count(UNSET_LINE),
            1,
            "unset GITLEAKS_CONFIG GITLEAKS_CONFIG_TOML must appear once",
        )
        remainder = self.text.replace(UNSET_LINE, "", 1)
        self.assertNotIn(
            "GITLEAKS_CONFIG",
            remainder,
            "GITLEAKS_CONFIG or GITLEAKS_CONFIG_TOML is set outside the required unset",
        )

    def test_scanner_calls_do_not_take_config_or_ignore_flags(self) -> None:
        calls = _require_scanner_calls(_named_step_script(self.text, SCAN_STEP))
        for call in calls:
            for token in call:
                forbidden = _forbidden_flag(token)
                self.assertIsNone(
                    forbidden,
                    f"scanner call gained {forbidden}: {' '.join(call)}",
                )

    def test_run_scripts_do_not_inline_github_or_inputs(self) -> None:
        for script in _run_scripts(self.text):
            match = _INLINE_EVENT.search(script)
            found = match.group(0) if match else ""
            self.assertIsNone(
                match,
                "a run script inlines "
                + found
                + "; event values must reach scripts through env only",
            )


if __name__ == "__main__":
    unittest.main()
