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
DIR_CALL = '"${tool}" dir . --no-banner --redact --ignore-gitleaks-allow'
GIT_CALL = '"${tool}" git . --no-banner --redact --ignore-gitleaks-allow --log-opts="${range}"'
SUM_LINE = 'echo "${ARCHIVE_SHA256}  ${archive}" | sha256sum -c -'
TAR_LINE = 'tar -xzf "${archive}" -C "${RUNNER_TEMP}" gitleaks'
SCANNER_MODES = {"dir", "git", "detect", "protect", "stdin"}
LONG_FORBIDDEN = {
    "--config",
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


def _assert_no_forbidden_flags(text: str) -> None:
    calls = _require_scanner_calls(_named_step_script(text, SCAN_STEP))
    for call in calls:
        found = _forbidden_on_call(call)
        if found:
            raise AssertionError(f"scanner call gained {found}: {' '.join(call)}")


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


if __name__ == "__main__":
    unittest.main()
