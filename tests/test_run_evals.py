"""Schema, coverage, gate exclusion, and the model-in-loop stub."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run-evals.py"
FIXTURE = ROOT / "tests" / "evals" / "activation_v0.1.jsonl"
FIXTURE_SHA256 = "d60f5d862c764ec90ba2670fe18c1423933d42ee8f8f85d0bda5d212380ca4da"


def _load():
    spec = importlib.util.spec_from_file_location("run_evals", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["run_evals"] = module
    spec.loader.exec_module(module)
    return module


RUN = _load()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


SKILL = """---
name: demo
description: >
  Use when the user says protect the IP, patent, trade secret, or when headless, a Grok Bot
  will show, email, push, post, or pass the work (protected-lane, infra paste).
  Do not use for generic privacy, telemetry, debug, CI.
when-to-use: >
  Triggers: "protect the IP", "before we demo", and headless, Grok Bot that will show, email, push, post, or pass the work.
  Do not activate for generic privacy.
---
# Demo
"""


def _row(fixture_id: str, level: str, prompt: str, **extra: object) -> dict:
    row = {
        "id": fixture_id,
        "prompt": prompt,
        "expected_level": level,
    }
    row.update(extra)
    return row


def _jsonl(rows: list[dict]) -> str:
    return "".join(json.dumps(row) + "\n" for row in rows)


class RunEvalTests(unittest.TestCase):
    def _tree(self, rows: list[dict], skill: str = SKILL) -> Path:
        raw = tempfile.mkdtemp()
        root = Path(raw)
        _write(root / "SKILL.md", skill)
        _write(root / "tests" / "evals" / "cases.jsonl", _jsonl(rows))
        return root

    def test_schema_errors_fail(self) -> None:
        root = Path(tempfile.mkdtemp())
        _write(root / "SKILL.md", SKILL)
        _write(
            root / "tests" / "evals" / "bad.jsonl",
            "\n".join(
                (
                    "{not json",
                    json.dumps(["nope"]),
                    json.dumps({"id": "a", "expected_level": "L0"}),
                    json.dumps({"id": "", "prompt": "x", "expected_level": "L0"}),
                    json.dumps({"id": "b", "prompt": "x", "expected_level": "L9"}),
                    json.dumps({"id": "c", "prompt": "x", "expected_level": "L0", "must": "hold"}),
                    json.dumps(
                        {"id": "d", "prompt": "x", "expected_level": "L0", "ambiguous": "yes"}
                    ),
                    json.dumps({"id": "e", "prompt": "x", "expected_level": "L0", "headless": 1}),
                    "",
                )
            )
            + "\n",
        )
        text, code = RUN.render(root)
        self.assertEqual(code, 1)
        self.assertIn("invalid JSON", text)
        self.assertIn("fixture is not an object", text)
        self.assertIn("missing key prompt", text)
        self.assertIn("id is not a non-empty string", text)
        self.assertIn("expected_level is not L0, L1, L2, or L3", text)
        self.assertIn("must is not a list of strings", text)
        self.assertIn("ambiguous is not a bool", text)
        self.assertIn("headless is not a bool", text)
        self.assertIn("failed", text)
        self.assertNotIn("\nok", text)

    def test_duplicate_ids_fail(self) -> None:
        root = Path(tempfile.mkdtemp())
        _write(root / "SKILL.md", SKILL)
        row = _row("act-001", "L0", "debug the loop")
        _write(root / "tests" / "evals" / "a.jsonl", _jsonl([row]))
        _write(root / "tests" / "evals" / "b.jsonl", _jsonl([row]))
        text, code = RUN.render(root)
        self.assertEqual(code, 1)
        self.assertIn("duplicate id act-001", text)

    def test_unknown_fields_and_optional_lists_are_kept(self) -> None:
        must_not = ["re-offer after decline (respect 'skip sentinel')", "second"]
        row = _row(
            "act-043",
            "L3",
            "Protect the IP.",
            must_not=must_not,
            zebra={"kept": True},
            headless=True,
        )
        root = self._tree(
            [
                _row("act-001", "L0", "debug the loop"),
                _row("act-002", "L1", "Keep this private."),
                _row("act-003", "L2", "Demo tomorrow."),
                row,
            ]
        )
        loaded, errors = RUN.load_fixtures(root)
        self.assertEqual(errors, [])
        found = next(item for item in loaded if item["id"] == "act-043")
        self.assertEqual(found["must_not"], must_not)
        self.assertEqual(found["zebra"], {"kept": True})
        self.assertIs(found["headless"], True)
        self.assertNotIn("must", found)
        text, code = RUN.render(root)
        self.assertEqual(code, 0)
        self.assertIn(
            "unscored must_not: act-043: re-offer after decline (respect 'skip sentinel'); second",
            text,
        )

    def test_missing_gate_level_fails(self) -> None:
        root = self._tree(
            [
                _row("act-001", "L0", "debug"),
                _row("act-002", "L1", "Keep this private."),
                _row("act-003", "L2", "Demo tomorrow."),
                _row("act-004", "L3", "Protect the IP.", gate_excluded=True),
            ]
        )
        text, code = RUN.render(root)
        self.assertEqual(code, 1)
        self.assertIn("missing level L3 in gate set", text)
        self.assertIn("levels all: L0=1 L1=1 L2=1 L3=1", text)
        self.assertIn("levels gate: L0=1 L1=1 L2=1 L3=0", text)

    def test_gate_excluded_skips_coverage_and_warnings(self) -> None:
        root = self._tree(
            [
                _row("fp-open", "L0", "How does a patent last?"),
                _row("fp-shut", "L0", "How does a patent last?", gate_excluded=True),
                _row("quiet", "L1", "Keep this private."),
                _row("miss-open", "L2", "Demo tomorrow with no protect word."),
                _row("miss-shut", "L2", "Demo tomorrow with no protect word.", gate_excluded=True),
                _row("explicit", "L3", "Protect the IP before the pilot."),
                _row("noun-shut", "L3", "patent filing", gate_excluded=True, ambiguous=True),
            ]
        )
        text, code = RUN.render(root)
        self.assertEqual(code, 0)
        self.assertIn("fixtures: 7", text)
        self.assertIn("excluded: 3", text)
        self.assertIn("gate: 4", text)
        self.assertIn("levels all: L0=2 L1=1 L2=2 L3=2", text)
        self.assertIn("levels gate: L0=1 L1=1 L2=1 L3=1", text)
        self.assertIn("warning false-positive: fp-open L0 matched:", text)
        self.assertIn("patent", text)
        self.assertNotIn("fp-shut", text)
        self.assertIn("warning missed-moment: miss-open L2 matched none", text)
        self.assertNotIn("miss-shut", text)
        self.assertNotIn("noun-shut", text)
        self.assertIn("summary: false-positive=1 missed-moment=1 excluded=3", text)
        self.assertTrue(text.endswith("ok"))

    def test_model_in_loop_is_a_stub(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = RUN.main(["--model-in-loop"])
        self.assertEqual(code, 0)
        self.assertEqual(buf.getvalue().strip(), "model-in-loop: not configured")

    def test_model_in_loop_subprocess_reads_no_fixture(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--model-in-loop", "--root", "/no/such/root"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), "model-in-loop: not configured")
        self.assertNotIn("failed", completed.stdout)
        self.assertEqual(completed.stderr, "")

    def test_trigger_phrases_from_frontmatter(self) -> None:
        phrases = {item.casefold() for item in RUN.parse_trigger_phrases(SKILL)}
        self.assertIn("protect the ip", phrases)
        self.assertIn("before we demo", phrases)
        self.assertIn("headless", phrases)
        self.assertIn("grok bot", phrases)
        self.assertIn("patent", phrases)
        self.assertIn("infra paste", phrases)
        self.assertNotIn("push", phrases)
        self.assertNotIn("email", phrases)
        self.assertNotIn("show", phrases)
        self.assertNotIn("post", phrases)
        self.assertNotIn("ci", phrases)
        self.assertNotIn("privacy", phrases)

    def test_real_skill_trigger_list(self) -> None:
        phrases = {
            item.casefold()
            for item in RUN.parse_trigger_phrases((ROOT / "SKILL.md").read_text(encoding="utf-8"))
        }
        for needle in (
            "protect the ip",
            "before we demo",
            "ip sensitive moment",
            "headless",
            "grok bot",
            "computer-use",
            "bot-to-bot",
            "partner pre-read",
            "investor demo",
            "fundraising deck",
            "claude.ai sync",
        ):
            self.assertIn(needle, phrases)
        for banned in (
            "push",
            "email",
            "show",
            "post",
            "ci",
            "privacy",
            "debug",
            "pass the work",
            "claude",
        ):
            self.assertNotIn(banned, phrases)

    def test_activation_fixture_is_byte_identical(self) -> None:
        digest = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
        self.assertEqual(digest, FIXTURE_SHA256)

    def test_real_tree_counts_and_gate(self) -> None:
        text, code = RUN.render(ROOT)
        self.assertEqual(code, 0, text)
        self.assertIn("fixtures: 51", text)
        self.assertIn("excluded: 3", text)
        self.assertIn("gate: 48", text)
        self.assertIn("levels all: L0=13 L1=11 L2=19 L3=8", text)
        self.assertIn("levels gate: L0=13 L1=10 L2=19 L3=6", text)
        self.assertIn(
            "unscored must_not: act-043: re-offer after decline (respect 'skip sentinel')",
            text,
        )
        for fixture_id in ("act-011", "act-034", "act-035"):
            self.assertNotIn(fixture_id, text)
        self.assertIn("warning false-positive: act-007 L0 matched:", text)
        self.assertIn("warning missed-moment: act-036 L2 matched none", text)
        self.assertTrue(text.endswith("ok"))
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), text)


if __name__ == "__main__":
    unittest.main()
