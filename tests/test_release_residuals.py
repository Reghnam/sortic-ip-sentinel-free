"""Tracked-file leak guard and host-zip edition pins.

Seed strings are built at runtime from parts so this file stays scannable.
"""

from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


HYGIENE = _load("check_hygiene", SCRIPTS / "check-hygiene.py")
BUILD = _load("build_packs_residuals", SCRIPTS / "build-packs.py")


def _leaks(name: str, text: str) -> list[str]:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "--", name], cwd=root, check=True)
        return HYGIENE.tree_leak_errors(root)


def _users_path() -> str:
    return "/" + "Users" + "/" + "ada" + "/notes"


def _home_path() -> str:
    return "/" + "home" + "/" + "ada" + "/notes"


def _windows_backslash() -> str:
    return "C:" + "\\" + "Users" + "\\" + "ada"


def _windows_slash() -> str:
    return "C:" + "/" + "Users" + "/" + "ada"


def _handoff_path() -> str:
    return "handoffs" + "/" + "note.md"


def _workspace_path() -> str:
    return "/" + "workspace" + "/" + "note.md"


def _chat_link() -> str:
    return "https://" + "grok.com" + "/c/" + "ab12cd34"


def _share_link() -> str:
    return "https://" + "grok.com" + "/share/" + "ab12cd34"


def _bad_email() -> str:
    return "ops" + "@" + "example.test"


def _extends_errors(fn: str, callee: str) -> bool:
    tree = ast.parse((SCRIPTS / "check-hygiene.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name != fn:
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            func = child.func
            if not isinstance(func, ast.Attribute) or func.attr != "extend":
                continue
            if not isinstance(func.value, ast.Name) or func.value.id != "errors":
                continue
            if not child.args:
                continue
            arg = child.args[0]
            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == callee:
                return True
    return False


class ReleaseResidualTests(unittest.TestCase):
    def _assert_local_path(self, text: str, needle: str, filename: str = "note.md") -> None:
        errors = _leaks(filename, "see " + text + "\n")
        blob = "\n".join(errors)
        self.assertTrue(any(item.startswith("local-path:") for item in errors), errors)
        self.assertIn(filename, blob)
        self.assertNotIn(needle, blob)

    def test_users_path_fails(self) -> None:
        needle = _users_path()
        self._assert_local_path(needle, needle)

    def test_home_path_fails(self) -> None:
        needle = _home_path()
        self._assert_local_path(needle, needle)

    def test_windows_backslash_path_fails(self) -> None:
        needle = _windows_backslash()
        self._assert_local_path(needle, needle)

    def test_windows_slash_path_fails(self) -> None:
        needle = _windows_slash()
        self._assert_local_path(needle, needle)

    def test_handoffs_path_fails(self) -> None:
        needle = _handoff_path()
        self._assert_local_path(needle, needle)

    def test_workspace_path_fails(self) -> None:
        needle = _workspace_path()
        self._assert_local_path(needle, needle)

    def test_chat_conversation_link_fails(self) -> None:
        link = _chat_link()
        errors = _leaks("note.md", "see " + link + "\n")
        blob = "\n".join(errors)
        self.assertTrue(any(item.startswith("share link in note.md:") for item in errors), errors)
        self.assertNotIn(link, blob)
        self.assertNotIn("ab12cd34", blob)

    def test_share_link_fails(self) -> None:
        link = _share_link()
        errors = _leaks("note.md", "see " + link + "\n")
        blob = "\n".join(errors)
        self.assertTrue(any(item.startswith("share link in note.md:") for item in errors), errors)
        self.assertNotIn(link, blob)
        self.assertNotIn("ab12cd34", blob)

    def test_disallowed_email_fails(self) -> None:
        bad = _bad_email()
        errors = _leaks("note.md", "write " + bad + "\n")
        blob = "\n".join(errors)
        self.assertTrue(any(item.startswith("email:") for item in errors), errors)
        self.assertNotIn(bad, blob)
        allowed = "noreply" + "@" + "example.com"
        self.assertEqual(_leaks("note.md", "write " + allowed + "\n"), [])

    def test_changelog_path_fails(self) -> None:
        needle = "/" + "workspace" + "/" + "handoffs" + "/note.md"
        self._assert_local_path(needle, needle, "CHANGELOG.md")

    def test_push_note_home_path_fails(self) -> None:
        needle = _users_path()
        self._assert_local_path(needle, needle, "PUSH_TO_GITHUB.txt")

    def test_stale_grok_bot_share_zip_fails(self) -> None:
        stale = "free-ip-sentinel-" + "grok" + "-v" + "0.5.36" + ".zip"
        self.assertNotEqual(HYGIENE.zip_edition(stale), HYGIENE.VERSION)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            share = root / "grok-bot-share"
            share.mkdir()
            (share / "bot-template.json").write_text(
                '{"skills":[{"source_zip":"' + stale + '"}]}\n',
                encoding="utf-8",
            )
            (share / "README.md").write_text("upload `" + stale + "`\n", encoding="utf-8")
            (share / "skills.md").write_text("from `" + stale + "`\n", encoding="utf-8")
            errors = HYGIENE.zip_edition_errors(root)
        blob = "\n".join(errors)
        for rel in (
            "grok-bot-share/bot-template.json",
            "grok-bot-share/README.md",
            "grok-bot-share/skills.md",
        ):
            self.assertIn(rel, blob)

    def test_stale_launch_zip_fails(self) -> None:
        stale = "free-ip-sentinel-" + "cursor" + "-v" + "0.5.36" + ".zip"
        self.assertNotEqual(HYGIENE.zip_edition(stale), HYGIENE.VERSION)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "LAUNCH.md").write_text("Zip: `" + stale + "`\n", encoding="utf-8")
            errors = HYGIENE.zip_edition_errors(root)
        self.assertTrue(any("LAUNCH.md" in item for item in errors), errors)

    def test_stale_warning_without_zip_name_passes(self) -> None:
        current = BUILD.zip_name("cursor-skill", HYGIENE.VERSION)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "LAUNCH.md").write_text(
                "Zip: `" + current + "`\nMailed try pack v" + "0.5.36" + " is stale.\n",
                encoding="utf-8",
            )
            self.assertEqual(HYGIENE.zip_edition_errors(root), [])

    def test_exclusion_is_exact_path(self) -> None:
        self.assertNotIn("CHANGELOG.md", HYGIENE.TREE_LEAK_EXCLUSIONS)
        self.assertNotIn("PUSH_TO_GITHUB.txt", HYGIENE.TREE_LEAK_EXCLUSIONS)
        needle = _users_path()
        self.assertEqual(_leaks("scripts/zipscan.py", "see " + needle + "\n"), [])
        errors = _leaks("scripts/zipscan.py.txt", "see " + needle + "\n")
        self.assertTrue(any(item.startswith("local-path:") for item in errors), errors)
        self.assertNotIn(needle, "\n".join(errors))

    def test_clean_head_passes(self) -> None:
        self.assertEqual(HYGIENE.tree_leak_errors(ROOT), [])
        self.assertEqual(HYGIENE.zip_edition_errors(ROOT), [])
        grok = BUILD.zip_name("grok-skill", HYGIENE.VERSION)
        cursor = BUILD.zip_name("cursor-skill", HYGIENE.VERSION)
        readme = (ROOT / "grok-bot-share" / "README.md").read_text(encoding="utf-8")
        skills = (ROOT / "grok-bot-share" / "skills.md").read_text(encoding="utf-8")
        template = (ROOT / "grok-bot-share" / "bot-template.json").read_text(encoding="utf-8")
        launch = (ROOT / "LAUNCH.md").read_text(encoding="utf-8")
        self.assertIn(grok, readme)
        self.assertIn(grok, skills)
        self.assertIn('"source_zip": "' + grok + '"', template)
        self.assertIn(cursor, launch)
        for text in (readme, skills, template, launch):
            self.assertNotIn("0.5.36.zip", text)

    def test_removing_the_guard_call_fails(self) -> None:
        self.assertTrue(_extends_errors("_hygiene", "tree_leak_errors"))
        self.assertTrue(_extends_errors("_hygiene", "zip_edition_errors"))


if __name__ == "__main__":
    unittest.main()
