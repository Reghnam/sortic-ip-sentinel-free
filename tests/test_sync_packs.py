"""Pack sync copies body, references, and knowledge, and stamps edition slots."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_sync():
    spec = importlib.util.spec_from_file_location("sync_packs", ROOT / "scripts" / "sync-packs.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["sync_packs"] = module
    spec.loader.exec_module(module)
    return module


SYNC = _load_sync()


def _eval_headings(root: Path) -> int:
    return (root / "references" / "evals.md").read_text(encoding="utf-8").count("## Eval ")


def _knowledge_copies(root: Path) -> int:
    names = {path.name for path in (root / "references").iterdir() if path.is_file()}
    knowledge = root / "openai-gpt-package" / "knowledge"
    if not knowledge.is_dir():
        return 0
    return sum(1 for path in knowledge.iterdir() if path.is_file() and path.name in names)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fixture(tmp: Path) -> None:
    _write(
        tmp / "scripts" / "check-hygiene.py",
        'VERSION = "0.5.48-free"\nPACKS = ("chatgpt-skill",)\n',
    )
    _write(
        tmp / "SKILL.md",
        "---\n"
        "name: demo\n"
        "description: >\n"
        "  alpha line\n"
        "  beta line\n"
        'version: "0.5.47-free"\n'
        "---\n"
        "# Demo Free Edition (v0.5.47-free)\n"
        "\n"
        "Body from root.\n"
        "Mailed pack v0.5.25-free is stale.\n",
    )
    _write(tmp / "references" / "note.md", "hello root\n")
    _write(
        tmp / "references" / "headless-hygiene-package.md",
        '"edition": "0.5.47-free"\n',
    )
    _write(
        tmp / "chatgpt-skill" / "SKILL.md",
        "---\n"
        "name: demo\n"
        "description: >\n"
        "  old line\n"
        'version: "0.5.47-free"\n'
        "extra: keep\n"
        "---\n"
        "old body\n",
    )
    _write(tmp / "chatgpt-skill" / "references" / "note.md", "old note\n")
    _write(tmp / "chatgpt-skill" / "references" / "extra.md", "drop me\n")
    _write(
        tmp / "chatgpt-skill" / "README.md",
        "# Host pack v0.5.47-free\n",
    )
    _write(tmp / "openai-gpt-package" / "knowledge" / "note.md", "old knowledge\n")
    _write(tmp / "openai-gpt-package" / "knowledge" / "other.md", "keep me\n")
    _write(tmp / "CHANGELOG.md", "## [0.5.47-free]\nkept\n")
    _write(tmp / "LICENSE.md", "# License Notice (v0.5.1-free)\n")
    _write(
        tmp / "README.md",
        "# Demo\n\nhygiene sentinel (**v0.5.47-free**).\n- slogan (v0.5.47-free)\n",
    )


class SyncPackTests(unittest.TestCase):
    def test_sync_updates_slots_and_is_idempotent(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _fixture(root)
            before = SYNC.main(["--check", "--root", str(root)])
            self.assertEqual(before, 1)
            wrote = SYNC.main(["--root", str(root)])
            self.assertEqual(wrote, 0)
            skill = (root / "chatgpt-skill" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Body from root.", skill)
            self.assertIn("alpha line", skill)
            self.assertIn("extra: keep", skill)
            self.assertIn('version: "0.5.48-free"', skill)
            self.assertIn("Free Edition (v0.5.48-free)", skill)
            self.assertIn("v0.5.25-free is stale", skill)
            self.assertEqual(
                (root / "chatgpt-skill" / "references" / "note.md").read_text(encoding="utf-8"),
                "hello root\n",
            )
            self.assertFalse((root / "chatgpt-skill" / "references" / "extra.md").exists())
            self.assertEqual(
                (root / "references" / "headless-hygiene-package.md").read_text(encoding="utf-8"),
                '"edition": "0.5.48-free"\n',
            )
            self.assertEqual(
                (root / "openai-gpt-package" / "knowledge" / "note.md").read_text(encoding="utf-8"),
                "hello root\n",
            )
            self.assertEqual(
                (root / "openai-gpt-package" / "knowledge" / "other.md").read_text(encoding="utf-8"),
                "keep me\n",
            )
            self.assertEqual((root / "CHANGELOG.md").read_text(encoding="utf-8"), "## [0.5.47-free]\nkept\n")
            self.assertIn("0.5.1-free", (root / "LICENSE.md").read_text(encoding="utf-8"))
            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("v0.5.48-free", readme)
            self.assertIn("v0.5.48-free", (root / "chatgpt-skill" / "README.md").read_text(encoding="utf-8"))
            again = SYNC.main(["--check", "--root", str(root)])
            self.assertEqual(again, 0)
            second = SYNC.main(["--root", str(root)])
            self.assertEqual(second, 0)
            self.assertEqual(SYNC.build_plan(root).diffs(), [])

    def test_disagreeing_slots_stop(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            _fixture(root)
            skill = (root / "SKILL.md").read_text(encoding="utf-8")
            skill = skill.replace('version: "0.5.47-free"', 'version: "0.5.40-free"', 1)
            (root / "SKILL.md").write_text(skill, encoding="utf-8")
            head = (root / "references" / "headless-hygiene-package.md").read_text(encoding="utf-8")
            head = head.replace("0.5.47-free", "0.5.41-free")
            (root / "references" / "headless-hygiene-package.md").write_text(head, encoding="utf-8")
            with self.assertRaises(SystemExit):
                SYNC.build_plan(root)

    def test_split_skill_keeps_dashes_inside_frontmatter(self) -> None:
        text = (
            "---\n"
            "name: demo\n"
            "description: >\n"
            "  a --- token stays in frontmatter\n"
            "note: keep\n"
            "---\n"
            "body keeps a --- token too\n"
        )
        front, body = SYNC.split_skill(text)
        self.assertIn("a --- token stays in frontmatter", front)
        self.assertIn("note: keep", front)
        self.assertEqual(body, "\nbody keeps a --- token too\n")
        self.assertEqual(front + body, text)
        real = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        real_front, real_body = SYNC.split_skill(real)
        self.assertEqual(real_front + real_body, real)

    def test_real_tree_check_is_clean(self) -> None:
        plan = SYNC.build_plan(ROOT)
        self.assertEqual(plan.diffs(), [])
        self.assertEqual(plan.version, SYNC.read_version(ROOT))
        self.assertEqual(len(plan.packs), len(SYNC.read_packs(ROOT)))
        self.assertEqual(plan.knowledge_count, _knowledge_copies(ROOT))
        code = SYNC.main(["--check", "--root", str(ROOT)])
        self.assertEqual(code, 0)

    def test_hygiene_still_reports_current_edition(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/check-hygiene.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        version = SYNC.read_version(ROOT)
        evals = _eval_headings(ROOT)
        self.assertIn(f"hygiene check OK: {version}", completed.stdout)
        self.assertIn(f"{evals} evals", completed.stdout)


if __name__ == "__main__":
    unittest.main()
