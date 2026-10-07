"""Share-link ids: one positive and one bare-base negative per host family."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import claim_rules  # noqa: E402
import zipscan  # noqa: E402

MARK = "Ab12Cd34ef"
ELLIPSIS = "\u2026"


def _load_build():
    spec = importlib.util.spec_from_file_location("build_packs", SCRIPTS / "build-packs.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_packs"] = module
    spec.loader.exec_module(module)
    return module


BUILD = _load_build()


def _lines(text: str) -> list[int]:
    return zipscan.share_link_lines(text + ("" if text.endswith("\n") else "\n"))


class ShareLinkFamilyTests(unittest.TestCase):
    def test_grok_share_id_flags(self) -> None:
        self.assertEqual(_lines("see https://grok.com/share/" + MARK), [1])
        self.assertEqual(_lines("see grok.com/share/" + MARK), [1])

    def test_grok_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://grok.com"), [])
        self.assertEqual(_lines("https://grok.com/"), [])
        self.assertEqual(_lines("https://grok.com/share"), [])
        self.assertEqual(_lines("https://grok.com/share/"), [])

    def test_grok_chat_id_flags(self) -> None:
        self.assertEqual(_lines("see https://grok.com/c/" + MARK), [1])
        self.assertEqual(_lines("see grok.com/c/" + MARK), [1])

    def test_grok_chat_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://grok.com/c"), [])
        self.assertEqual(_lines("https://grok.com/c/"), [])

    def test_chatgpt_share_id_flags(self) -> None:
        self.assertEqual(_lines("https://chatgpt.com/c/" + MARK), [1])
        self.assertEqual(_lines("https://chatgpt.com/share/" + MARK), [1])

    def test_chatgpt_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://chatgpt.com"), [])
        self.assertEqual(_lines("https://chatgpt.com/c"), [])
        self.assertEqual(_lines("https://chatgpt.com/c/"), [])
        self.assertEqual(_lines("https://chatgpt.com/share"), [])
        self.assertEqual(_lines("https://chatgpt.com/share/"), [])

    def test_chat_openai_share_id_flags(self) -> None:
        self.assertEqual(_lines("https://chat.openai.com/share/" + MARK), [1])

    def test_chat_openai_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://chat.openai.com"), [])
        self.assertEqual(_lines("https://chat.openai.com/share"), [])
        self.assertEqual(_lines("https://chat.openai.com/share/"), [])

    def test_claude_share_id_flags(self) -> None:
        self.assertEqual(_lines("https://claude.ai/chat/" + MARK), [1])
        self.assertEqual(_lines("https://claude.ai/share/" + MARK), [1])

    def test_claude_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://claude.ai"), [])
        self.assertEqual(_lines("https://claude.ai/chat"), [])
        self.assertEqual(_lines("https://claude.ai/chat/"), [])
        self.assertEqual(_lines("https://claude.ai/share"), [])
        self.assertEqual(_lines("https://claude.ai/share/"), [])

    def test_x_share_id_flags(self) -> None:
        self.assertEqual(_lines("https://x.com/i/grok/share/" + MARK), [1])

    def test_x_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://x.com"), [])
        self.assertEqual(_lines("https://x.com/i/grok/share"), [])
        self.assertEqual(_lines("https://x.com/i/grok/share/"), [])
        self.assertEqual(_lines("https://x.com/i/grok/share/" + ELLIPSIS), [])

    def test_dropbox_share_id_flags(self) -> None:
        self.assertEqual(
            _lines("https://www.dropbox.com/scl/fi/" + MARK + "/notes.txt?rlkey=Zz98Yy76Xx"),
            [1],
        )
        self.assertEqual(_lines("https://www.dropbox.com/s/" + MARK + "/notes.txt"), [1])

    def test_dropbox_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://dropbox.com"), [])
        self.assertEqual(_lines("https://www.dropbox.com"), [])
        self.assertEqual(_lines("https://www.dropbox.com/"), [])
        self.assertEqual(_lines("https://www.dropbox.com/home"), [])
        self.assertEqual(_lines("https://www.dropbox.com/s/"), [])

    def test_onedrive_short_share_id_flags(self) -> None:
        self.assertEqual(_lines("https://1drv.ms/b/s!" + MARK), [1])

    def test_onedrive_short_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://1drv.ms"), [])
        self.assertEqual(_lines("https://1drv.ms/"), [])

    def test_onedrive_live_share_id_flags(self) -> None:
        self.assertEqual(
            _lines("https://onedrive.live.com/redir?resid=" + MARK + "&authkey=Zz98Yy76"),
            [1],
        )

    def test_onedrive_live_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://onedrive.live.com"), [])
        self.assertEqual(_lines("https://onedrive.live.com/"), [])
        self.assertEqual(_lines("https://onedrive.live.com/about"), [])

    def test_sharepoint_share_id_flags(self) -> None:
        self.assertEqual(
            _lines("https://contoso.sharepoint.com/:w:/s/team/E" + MARK),
            [1],
        )

    def test_sharepoint_bare_base_does_not_flag(self) -> None:
        self.assertEqual(_lines("https://sharepoint.com"), [])
        self.assertEqual(_lines("https://contoso.sharepoint.com"), [])
        self.assertEqual(_lines("https://contoso.sharepoint.com/"), [])
        self.assertEqual(_lines("https://contoso.sharepoint.com/sites/team"), [])

    def test_zip_reports_the_line_without_the_id(self) -> None:
        url = "https://chatgpt.com/share/" + MARK
        with tempfile.TemporaryDirectory() as raw:
            dest = Path(raw) / "sample.zip"
            BUILD.write_deterministic_zip(
                dest,
                {"SKILL.md": b"ok\n", "references/note.md": ("see " + url + "\n").encode()},
            )
            result = zipscan.scan_zip(dest, legacy_paths=set())
        blob = "\n".join(result.failures)
        self.assertIn("share link in references/note.md:1", result.failures)
        self.assertNotIn(MARK, blob)
        self.assertNotIn(url, blob)

    def test_tip_scan_reports_the_line_without_the_id(self) -> None:
        url = "https://claude.ai/share/" + MARK
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "SKILL.md").write_text("Not legal advice.\n", encoding="utf-8")
            for pack in claim_rules.PACK_DIRS:
                (root / pack).mkdir()
                (root / pack / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("# log\nplain\nsee " + url + "\n", encoding="utf-8")
            scan = claim_rules.scan_claims(root)
        blob = "\n".join(scan.errors + scan.warnings)
        self.assertEqual(scan.errors, ["share link in CHANGELOG.md:3"])
        self.assertNotIn(MARK, blob)
        self.assertNotIn(url, blob)

    def test_shipped_tree_has_no_share_link_findings(self) -> None:
        scan = claim_rules.scan_claims(ROOT)
        share = [line for line in scan.errors if line.startswith("share link in ")]
        self.assertEqual(share, [])

    def test_placeholder_in_shipped_skill_is_not_an_id(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("/share/" + ELLIPSIS, text)
        self.assertEqual(zipscan.share_link_lines(text), [])


# Host, share prefix, and a separator that reaches the open-ended piece.
# A space blocks an id. "?" and "&" sit inside the query and path runs.
_REPEAT_UNITS = (
    ("grok\\.com", "grok.com/share/ "),
    ("grok\\.com(?![A-Za-z0-9.-])/c/", "grok.com/c/ "),
    ("/c/", "chatgpt.com/c/ "),
    ("chatgpt\\.com(?![A-Za-z0-9.-])/share/", "chatgpt.com/share/ "),
    ("chat\\.openai\\.com", "chat.openai.com/share/ "),
    ("/chat/", "claude.ai/chat/ "),
    ("claude\\.ai(?![A-Za-z0-9.-])/share/", "claude.ai/share/ "),
    ("x\\.com", "x.com/i/grok/share/ "),
    ("(?:s|sh|scl/(?:fi|fo))", "dropbox.com/s/ "),
    ("rlkey=", "dropbox.com/s/?&"),
    ("s!", "1drv.ms/a/&"),
    ("{7,200}", "1drv.ms/abc "),
    ("onedrive\\.live\\.com(?![A-Za-z0-9.-])/:[A-Za-z]:/", "onedrive.live.com/:a:/&"),
    ("resid|authkey", "onedrive.live.com?&"),
    ("sharepoint\\.com(?![A-Za-z0-9.-])/:[A-Za-z]:/", "sharepoint.com/:a:/&"),
    ("guestaccess\\.aspx", "sharepoint.com/&"),
)

# One near-miss line per host family. The separator is the slow shape for that family.
_FAMILY_UNITS = (
    "grok.com/share/ ",
    "chatgpt.com/share/ ",
    "chat.openai.com/share/ ",
    "claude.ai/share/ ",
    "x.com/i/grok/share/ ",
    "dropbox.com/s/?&",
    "1drv.ms/a/&",
    "onedrive.live.com?&",
    "sharepoint.com/&",
)


def _repeat(unit: str, length: int = 100_000) -> str:
    copies = (length + len(unit) - 1) // len(unit)
    return unit * copies


class ShareLinkRepeatTests(unittest.TestCase):
    def test_each_pattern_finishes_on_a_repeated_host(self) -> None:
        patterns = zipscan._SHARE_LINK
        self.assertEqual(len(patterns), len(_REPEAT_UNITS))
        for pattern, (marker, unit) in zip(patterns, _REPEAT_UNITS):
            self.assertIn(marker, pattern.pattern)
            line = _repeat(unit)
            self.assertGreaterEqual(len(line), 100_000)
            best = None
            found = None
            for _ in range(3):
                started = time.perf_counter()
                found = pattern.search(line)
                elapsed = time.perf_counter() - started
                if best is None or elapsed < best:
                    best = elapsed
            self.assertIsNone(found, unit)
            self.assertLess(best, 0.250, f"{unit!r} took {best * 1000:.1f} ms")

    def test_adversarial_family_line_is_not_a_share_link(self) -> None:
        self.assertEqual(len(_FAMILY_UNITS), 9)
        for unit in _FAMILY_UNITS:
            line = _repeat(unit)
            self.assertGreaterEqual(len(line), 100_000)
            self.assertFalse(zipscan.line_has_share_link(line), unit)


if __name__ == "__main__":
    unittest.main()
