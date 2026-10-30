"""Tracked-file leak guard and host-zip edition pins.

Seed strings are built at runtime from parts so this file stays scannable.
"""

from __future__ import annotations

import ast
import importlib.util
import re
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


def _license_repo(files: dict[str, str]) -> list[str]:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        for name, text in files.items():
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "--", *files], cwd=root, check=True)
        return HYGIENE.license_version_errors(root)


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

    def test_license_editions_match_version(self) -> None:
        self.assertEqual(HYGIENE.license_version_errors(ROOT), [])
        edition = "v" + HYGIENE.VERSION
        paid = "(with paid paths), see the main skill."
        completed = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        names = [
            rel
            for rel in completed.stdout.decode("utf-8").split("\0")
            if rel and Path(rel).name.lower() == "license.md"
        ]
        self.assertEqual(
            names,
            [
                "LICENSE.md",
                "chatgpt-skill/LICENSE.md",
                "claude-skill/LICENSE.md",
                "cursor-skill/LICENSE.md",
                "grok-skill/LICENSE.md",
            ],
        )
        for rel in names:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(edition, text)
            self.assertIn(paid, text)
            self.assertNotIn("Checkpoint (with )", text)

    def test_stale_license_edition_fails(self) -> None:
        stale = "v" + "1.2.3-free"
        errors = _license_repo({"LICENSE.md": "notice " + stale + "\n"})
        self.assertEqual(errors, ["LICENSE.md license edition is not " + HYGIENE.VERSION])

    def test_mixed_license_edition_fails(self) -> None:
        text = "v" + HYGIENE.VERSION + " and v" + "1.2.3-free" + "\n"
        errors = _license_repo({"cursor-skill/LICENSE.md": text})
        self.assertEqual(
            errors,
            ["cursor-skill/LICENSE.md license edition is not " + HYGIENE.VERSION],
        )

    def test_suffixed_license_edition_fails(self) -> None:
        for suffix in ("-alpha", "2", "+build"):
            with self.subTest(suffix=suffix):
                text = "notice v" + HYGIENE.VERSION + suffix + "\n"
                errors = _license_repo({"LICENSE.md": text})
                self.assertEqual(
                    errors,
                    ["LICENSE.md license edition is not " + HYGIENE.VERSION],
                )
        both = "v" + HYGIENE.VERSION + " and v" + HYGIENE.VERSION + "-alpha\n"
        errors = _license_repo({"LICENSE.md": both})
        self.assertEqual(errors, ["LICENSE.md license edition is not " + HYGIENE.VERSION])

    def test_current_license_ignores_other_files(self) -> None:
        files = {
            "LICENSE.md": "notice v" + HYGIENE.VERSION + "\n",
            "notes.md": "old v" + "1.2.3-free" + "\n",
        }
        self.assertEqual(_license_repo(files), [])

    def test_empty_checkpoint_parenthesis_fails(self) -> None:
        text = "notice v" + HYGIENE.VERSION + "\nCheckpoint (with )\n"
        errors = _license_repo({"LICENSE.md": text})
        self.assertEqual(errors, ["LICENSE.md has an empty checkpoint parenthesis"])

    def test_missing_license_fails(self) -> None:
        errors = _license_repo({"README.md": "v" + HYGIENE.VERSION + "\n"})
        self.assertEqual(errors, ["no tracked LICENSE.md"])

    def test_removing_the_guard_call_fails(self) -> None:
        self.assertTrue(_extends_errors("_hygiene", "tree_leak_errors"))
        self.assertTrue(_extends_errors("_hygiene", "zip_edition_errors"))
        self.assertTrue(_extends_errors("_hygiene", "license_version_errors"))
        self.assertTrue(_extends_errors("_hygiene", "edition_pin_errors"))

    def test_edition_pins_match_current_tree(self) -> None:
        self.assertEqual(HYGIENE.edition_pin_errors(ROOT), [])

    def test_skill_metadata_mismatch_fails(self) -> None:
        stale = "0.5." + "52" + "-free"
        text = 'metadata:\n  version: "' + stale + '"\n'
        self.assertEqual(
            HYGIENE.metadata_pin_error("SKILL.md", text),
            "SKILL.md metadata edition is not " + HYGIENE.VERSION,
        )
        current = 'metadata:\n  version: "' + HYGIENE.VERSION + '"\n'
        self.assertIsNone(HYGIENE.metadata_pin_error("SKILL.md", current))

    def test_readme_history_is_not_the_pin(self) -> None:
        stale = "0.5." + "52" + "-free"
        text = "edition " + HYGIENE.VERSION + "\nolder v" + stale + "\n"
        self.assertIsNone(HYGIENE.readme_pin_error("README.md", text))

    def test_readme_stale_first_pin_fails(self) -> None:
        stale = "0.5." + "52" + "-free"
        text = "edition " + stale + "\nlater " + HYGIENE.VERSION + "\n"
        self.assertEqual(
            HYGIENE.readme_pin_error("README.md", text),
            "README.md edition is not " + HYGIENE.VERSION,
        )

    def test_readme_suffix_fails(self) -> None:
        text = "edition v" + HYGIENE.VERSION + "-alpha\n"
        self.assertEqual(
            HYGIENE.readme_pin_error("README.md", text),
            "README.md edition is not " + HYGIENE.VERSION,
        )

    def test_changelog_tip_ignores_later_headings(self) -> None:
        stale = "0.5." + "52" + "-free"
        current = "## [" + HYGIENE.VERSION + "] — 2026-10-29\n## [" + stale + "] — 2026-10-07\n"
        self.assertIsNone(HYGIENE.changelog_pin_error("CHANGELOG.md", current))
        swapped = "## [" + stale + "] — 2026-10-07\n## [" + HYGIENE.VERSION + "] — 2026-10-29\n"
        self.assertEqual(
            HYGIENE.changelog_pin_error("CHANGELOG.md", swapped),
            "CHANGELOG.md tip edition is not " + HYGIENE.VERSION,
        )

    def test_license_suffix_pin_fails(self) -> None:
        text = "notice v" + HYGIENE.VERSION + "-alpha\n"
        self.assertEqual(
            HYGIENE.license_pin_error("LICENSE.md", text),
            "LICENSE.md license edition is not " + HYGIENE.VERSION,
        )
        mixed = "v" + HYGIENE.VERSION + " and v" + "1.2.3-free" + "\n"
        self.assertEqual(
            HYGIENE.license_pin_error("LICENSE.md", mixed),
            "LICENSE.md license edition is not " + HYGIENE.VERSION,
        )
        clean = "notice v" + HYGIENE.VERSION + "\n"
        self.assertIsNone(HYGIENE.license_pin_error("LICENSE.md", clean))

    def test_missing_edition_pin_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            errors = HYGIENE.edition_pin_errors(root)
        self.assertIn("SKILL.md edition pin missing", errors)
        self.assertIn("LICENSE.md edition pin missing", errors)
        self.assertIn("README.md edition pin missing", errors)
        self.assertIn("CHANGELOG.md edition pin missing", errors)

    def test_activation_separates_exposure_from_debug(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        desc = HYGIENE.description_text(ROOT / "SKILL.md")
        when_match = re.search(
            r"^when-to-use:\s*>\n((?:  .*\n)+)",
            skill,
            re.M,
        )
        self.assertIsNotNone(when_match)
        when = "\n".join(line[2:] for line in when_match.group(1).splitlines()).strip()
        self.assertLessEqual(len(desc), 1024)
        self.assertLessEqual(len(desc) + len(when), 1536)
        flat = " ".join(desc.split())
        self.assertIn("Bot-to-Bot will show", flat)
        self.assertIn("does not expose the work", flat)
        self.assertIn("debug", flat.lower())
        self.assertIn("no exposure", when)
        body = HYGIENE.body_after_frontmatter(ROOT / "SKILL.md")
        self.assertIn("does not show, email, push, post, or pass the work", body)
        self.assertIn("headless one-shot, computer-use, or Bot-to-Bot pass of the work", body)
        evals = (ROOT / "references" / "evals.md").read_text(encoding="utf-8")
        self.assertIn("## Eval 277 —", evals)
        self.assertIn("## Eval 281 —", evals)
        self.assertIn("L0 silent — generic privacy, telemetry, and debug", evals)
        self.assertIn("L2 soft tip only — exposure without an explicit protect ask", evals)


if __name__ == "__main__":
    unittest.main()
