"""Zip scan failures and legacy corpus warnings."""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import zipscan  # noqa: E402


def _load_build():
    spec = importlib.util.spec_from_file_location("build_packs", SCRIPTS / "build-packs.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_packs"] = module
    spec.loader.exec_module(module)
    return module


BUILD = _load_build()


def _corpus_needle() -> str:
    return "us" + "-ip-law-" + "ground-truth"


def _mark_encrypted(path: Path) -> None:
    data = bytearray(path.read_bytes())
    for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        index = data.find(signature)
        if index < 0:
            raise AssertionError("zip header is missing")
        flag = int.from_bytes(data[index + flag_offset : index + flag_offset + 2], "little") | 0x1
        data[index + flag_offset : index + flag_offset + 2] = flag.to_bytes(2, "little")
    path.write_bytes(data)


def _zip(tmp: Path, members: dict[str, bytes]) -> Path:
    dest = Path(tmp) / "sample.zip"
    BUILD.write_deterministic_zip(dest, members)
    return dest


class ZipScanTests(unittest.TestCase):
    def test_clean_zip_passes(self) -> None:
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": b"hello\n", "references/note.md": b"plain\n"})
            result = zipscan.scan_zip(path, legacy_paths=set())
        self.assertTrue(result.ok)
        self.assertEqual(result.names, ["SKILL.md", "references/note.md"])
        self.assertEqual(result.warnings, [])

    def test_secret_token_built_from_parts_is_caught(self) -> None:
        token = "sk" + "-" + ("a" * 20)
        self.assertNotIn(token, (SCRIPTS / "zipscan.py").read_text(encoding="utf-8"))
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": b"ok\n", "references/note.md": token.encode()})
            result = zipscan.scan_zip(path, legacy_paths=set())
        self.assertFalse(result.ok)
        self.assertTrue(any(line.startswith("secret-token:") for line in result.failures))
        self.assertNotIn(token, "\n".join(result.failures))

    def test_other_secret_shapes_are_caught(self) -> None:
        samples = {
            "bearer.md": "Bearer " + ("b" * 20),
            "key.md": "-----BEGIN " + "RSA PRIVATE KEY-----",
            "hub.md": "ghp" + "_" + ("c" * 30),
        }
        with self._tmp() as tmp:
            members = {"SKILL.md": b"ok\n"}
            members.update({name: text.encode() for name, text in samples.items()})
            result = zipscan.scan_zip(_zip(tmp, members), legacy_paths=set())
        secret_hits = [line for line in result.failures if line.startswith("secret-token:")]
        self.assertEqual(len(secret_hits), 3)

    def test_forbidden_names_are_caught(self) -> None:
        names = (
            "CHANGELOG.md",
            "LAUNCH.md",
            "PUSH_TO_GITHUB.txt",
            ".env",
            "secrets/id_rsa",
            "cert.pem",
            "store.sqlite",
            "tool.exe",
            "plugin.json",
            "nested/ground-truth/readme.md",
        )
        with self._tmp() as tmp:
            members = {"SKILL.md": b"ok\n"}
            members.update({name: b"x\n" for name in names})
            result = zipscan.scan_zip(_zip(tmp, members), legacy_paths=set())
        denied = [line for line in result.failures if ":" in line]
        self.assertGreaterEqual(len(denied), len(names))
        blob = "\n".join(result.failures)
        for name in ("CHANGELOG.md", ".env", "id_rsa", "cert.pem", "store.sqlite", "plugin.json"):
            self.assertIn(name, blob)

    def test_local_path_and_company_email_are_caught(self) -> None:
        body = "\n".join(
            (
                "see /Users/example/notes",
                "see /home/example/notes",
                "see C:\\Users\\example\\notes",
                "see handoffs/draft.md",
                "write ops@example.test",
            )
        )
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": body.encode()})
            result = zipscan.scan_zip(path, legacy_paths=set())
        blob = "\n".join(result.failures)
        self.assertIn("local-path:", blob)
        self.assertIn("email:", blob)
        self.assertNotIn("ops@example.test", blob)

    def test_public_mailbox_is_still_an_email(self) -> None:
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": b"write ops@gmail.com\n"})
            result = zipscan.scan_zip(path, legacy_paths=set())
        self.assertFalse(result.ok)
        self.assertTrue(any(line.startswith("email:") for line in result.failures))

    def test_noreply_addresses_are_allowed(self) -> None:
        bodies = (
            "write noreply@example.com\n",
            "write no-reply@example.com\n",
            "write noreply+tag@example.com\n",
            "write 12345+login@users.noreply.github.com\n",
        )
        for body in bodies:
            with self._tmp() as tmp:
                path = _zip(tmp, {"SKILL.md": body.encode()})
                result = zipscan.scan_zip(path, legacy_paths=set())
            self.assertTrue(result.ok, (body, result.failures))

    def test_chat_share_and_cloud_drive_links_are_caught(self) -> None:
        samples = {
            "references/a.md": "https://" + "grok" + ".com/c/" + "abc",
            "references/b.md": "https://" + "chatgpt" + ".com/share/" + "abc",
            "references/c.md": "https://" + "claude" + ".ai/share/" + "abc",
            "references/d.md": "https://" + "drive" + ".google" + ".com/file/abc",
            "references/e.md": "https://" + "docs" + ".google" + ".com/document/d/abc",
        }
        with self._tmp() as tmp:
            members = {"SKILL.md": b"ok\n"}
            members.update({name: (text + "\n").encode() for name, text in samples.items()})
            result = zipscan.scan_zip(_zip(tmp, members), legacy_paths=set())
        blob = "\n".join(result.failures)
        self.assertEqual(sum(line.startswith("chat-share:") for line in result.failures), 3)
        self.assertEqual(sum(line.startswith("cloud-drive:") for line in result.failures), 2)
        for text in samples.values():
            self.assertNotIn(text, blob)
        self.assertFalse(result.ok)

    def test_ordinary_host_mentions_are_not_share_links(self) -> None:
        body = "\n".join(
            (
                "claude" + ".ai sync",
                "chatgpt" + ".com/pricing",
                "grok" + ".com/careers",
                "docs" + ".google" + ".com.example",
                "not" + "drive" + ".google" + ".com",
            )
        )
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": body.encode()})
            result = zipscan.scan_zip(path, legacy_paths=set())
        self.assertTrue(result.ok, result.failures)

    def test_extra_pattern_reports_number_and_member_only(self) -> None:
        token = "zz-unique-marker-9f3a"
        patterns = [re.compile("nope-zz-absent"), re.compile(token)]
        with self._tmp() as tmp:
            path = _zip(
                tmp,
                {"SKILL.md": b"ok\n", "references/note.md": (token + "\n").encode()},
            )
            result = zipscan.scan_zip(path, legacy_paths=set(), extra_patterns=patterns)
        self.assertEqual(result.failures, ["extra-pattern #2: references/note.md"])
        report = zipscan.format_report(result)
        self.assertNotIn(token, report)
        self.assertNotIn("nope-zz-absent", report)

    def test_legacy_corpus_mention_warns_and_new_file_fails(self) -> None:
        needle = _corpus_needle()
        with self._tmp() as tmp:
            legacy_zip = _zip(
                tmp,
                {"SKILL.md": f"never bundle {needle}\n".encode()},
            )
            warned = zipscan.scan_zip(legacy_zip, legacy_paths={"SKILL.md"})
            new_zip = Path(tmp) / "new.zip"
            BUILD.write_deterministic_zip(
                new_zip,
                {
                    "SKILL.md": b"ok\n",
                    "references/new-note.md": f"see {needle}\n".encode(),
                },
            )
            failed = zipscan.scan_zip(new_zip, legacy_paths={"SKILL.md"})
        self.assertTrue(warned.ok)
        self.assertEqual(warned.warning_mentions, 1)
        self.assertTrue(any("corpus legacy" in line for line in warned.warnings))
        self.assertFalse(failed.ok)
        self.assertTrue(any(line.startswith("corpus-ref:") for line in failed.failures))

    def test_layout_and_size_limits(self) -> None:
        with self._tmp() as tmp:
            missing = _zip(tmp, {"README.md": b"no skill\n"})
            missing_result = zipscan.scan_zip(missing, legacy_paths=set())
            nested = Path(tmp) / "nested.zip"
            BUILD.write_deterministic_zip(
                nested,
                {"SKILL.md": b"ok\n", "extra/SKILL.md": b"no\n"},
            )
            nested_result = zipscan.scan_zip(nested, legacy_paths=set())
            huge = Path(tmp) / "huge.zip"
            BUILD.write_deterministic_zip(huge, {"SKILL.md": b"0123456789"})
            huge_result = zipscan.scan_zip(huge, legacy_paths=set(), max_uncompressed=4)
        self.assertFalse(missing_result.ok)
        self.assertFalse(nested_result.ok)
        self.assertTrue(any(line.startswith("size:") for line in huge_result.failures))

    def test_unsafe_member_names_are_caught(self) -> None:
        with self._tmp() as tmp:
            dest = Path(tmp) / "names.zip"
            with __import__("zipfile").ZipFile(dest, "w") as zf:
                for name in (
                    "SKILL.md",
                    "../SKILL.md",
                    "/tmp/SKILL.md",
                    "C:/SKILL.md",
                    "dir\\note.md",
                    "nested/../../outside.md",
                    "/workspace/note.md",
                ):
                    zf.writestr(name, b"x\n")
            result = zipscan.scan_zip(dest, legacy_paths=set())
        blob = "\n".join(result.failures)
        self.assertIn("parent-segment: ../SKILL.md", blob)
        self.assertIn("parent-segment: nested/../../outside.md", blob)
        self.assertIn("absolute-path: /tmp/SKILL.md", blob)
        self.assertIn("absolute-path: C:/SKILL.md", blob)
        self.assertIn("backslash: dir\\note.md", blob)
        self.assertIn("workspace-path: /workspace/note.md", blob)
        self.assertFalse(result.ok)

    def test_double_dot_inside_a_name_is_not_a_parent_segment(self) -> None:
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": b"ok\n", "references/a..b.md": b"plain\n"})
            result = zipscan.scan_zip(path, legacy_paths=set())
        self.assertTrue(result.ok, result.failures)
        self.assertFalse(any(line.startswith("parent-segment:") for line in result.failures))

    def test_case_variant_names_are_caught(self) -> None:
        with self._tmp() as tmp:
            dest = Path(tmp) / "case.zip"
            with __import__("zipfile").ZipFile(dest, "w") as zf:
                zf.writestr("SKILL.md", b"one\n")
                zf.writestr("skill.md", b"two\n")
            result = zipscan.scan_zip(dest, legacy_paths=set())
        blob = "\n".join(result.failures)
        self.assertIn("case-duplicate:", blob)
        self.assertIn("SKILL.md", blob)
        self.assertIn("skill.md", blob)
        self.assertFalse(result.ok)

    def test_symlink_member_is_caught(self) -> None:
        with self._tmp() as tmp:
            dest = Path(tmp) / "link.zip"
            with __import__("zipfile").ZipFile(dest, "w") as zf:
                zf.writestr("SKILL.md", b"ok\n")
                info = __import__("zipfile").ZipInfo("link.md")
                info.compress_type = __import__("zipfile").ZIP_STORED
                info.create_system = 3
                info.external_attr = 0o120777 << 16
                zf.writestr(info, b"SKILL.md")
            result = zipscan.scan_zip(dest, legacy_paths=set())
        self.assertTrue(any(line.startswith("symlink: link.md") for line in result.failures))
        self.assertFalse(result.ok)

    def test_corrupt_deflate_member_is_a_fail_line(self) -> None:
        import struct

        with self._tmp() as tmp:
            dest = Path(tmp) / "bad-deflate.zip"
            with __import__("zipfile").ZipFile(dest, "w") as zf:
                info = __import__("zipfile").ZipInfo("SKILL.md")
                info.compress_type = __import__("zipfile").ZIP_DEFLATED
                zf.writestr(info, b"hello skill\n" * 80, compresslevel=9)
            data = bytearray(dest.read_bytes())
            name_len, extra_len = struct.unpack_from("<HH", data, 26)
            comp_size = struct.unpack_from("<I", data, 18)[0]
            start = 30 + name_len + extra_len
            data[start + max(comp_size // 2, 1)] ^= 0xFF
            dest.write_bytes(data)
            result = zipscan.scan_zip(dest, legacy_paths=set())
        self.assertTrue(any(line.startswith("unreadable-member: SKILL.md") for line in result.failures))
        report = zipscan.format_report(result)
        self.assertIn("FAIL unreadable-member: SKILL.md", report)
        self.assertIn("zip scan FAILED", report)
        self.assertFalse(result.ok)

    def test_duplicate_names_are_caught(self) -> None:
        with self._tmp() as tmp:
            dest = Path(tmp) / "dup.zip"
            with __import__("zipfile").ZipFile(dest, "w") as zf:
                zf.writestr("SKILL.md", b"one\n")
                zf.writestr("SKILL.md", b"two\n")
            result = zipscan.scan_zip(dest, legacy_paths=set())
        self.assertTrue(any(line.startswith("duplicate-name: SKILL.md") for line in result.failures))

    def test_encrypted_member_is_a_failure_not_a_crash(self) -> None:
        with self._tmp() as tmp:
            dest = Path(tmp) / "enc.zip"
            with __import__("zipfile").ZipFile(dest, "w") as zf:
                zf.writestr("SKILL.md", b"hidden\n")
            _mark_encrypted(dest)
            result = zipscan.scan_zip(dest, legacy_paths=set())
        self.assertTrue(any(line.startswith("encrypted:") for line in result.failures))
        self.assertFalse(result.ok)

    def test_workspace_fragment_in_file_text_is_caught(self) -> None:
        with self._tmp() as tmp:
            path = _zip(tmp, {"SKILL.md": b"see /workspace/notes\n"})
            result = zipscan.scan_zip(path, legacy_paths=set())
        self.assertTrue(any(line.startswith("local-path:") for line in result.failures))

    def test_corrupt_zip_is_a_fail_line(self) -> None:
        with self._tmp() as tmp:
            dest = Path(tmp) / "bad.zip"
            dest.write_bytes(b"this is not a zip")
            result = zipscan.scan_zip(dest, legacy_paths=set())
        self.assertEqual(result.failures, ["unreadable-zip"])
        report = zipscan.format_report(result)
        self.assertIn("FAIL unreadable-zip", report)
        self.assertIn("zip scan FAILED", report)
        self.assertFalse(result.ok)

    def test_zip_bytes_are_deterministic(self) -> None:
        members = {"SKILL.md": b"b\n", "references/a.md": b"a\n"}
        with self._tmp() as tmp:
            first = Path(tmp) / "one.zip"
            second = Path(tmp) / "two.zip"
            BUILD.write_deterministic_zip(first, members)
            BUILD.write_deterministic_zip(second, members)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            info = __import__("zipfile").ZipFile(first).infolist()
        self.assertEqual([item.filename for item in info], ["SKILL.md", "references/a.md"])
        self.assertTrue(all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in info))

    def _tmp(self):
        import tempfile

        return tempfile.TemporaryDirectory()


if __name__ == "__main__":
    unittest.main()
