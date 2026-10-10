"""Claim rules, negation, allow-list, and external name patterns."""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import claim_rules  # noqa: E402


# One passing line and one failing line for every rule id.
# Failing lines are the banned shape. Passing lines are outside it, or negated.
CASES = (
    ("percent-near-refund", "listing budget is 1% of context", False),
    ("percent-near-refund", "reimbursed at 90%", True),
    ("currency-amount", "no amounts are stated", False),
    ("currency-amount", "10 EUR", True),
    ("residency-claim", "US-hosted today", False),
    ("residency-claim", "EU-hosted storage", True),
    ("guaranteed", "no guarantee", False),
    ("guaranteed", "guaranteed protection", True),
    ("legal-advice-positive", "not legal advice", False),
    ("legal-advice-positive", "this is legal advice", True),
    ("provider-claim", "IP Scan by a provider listed by the national office", False),
    ("provider-claim", "IP Scan by zzdummyfirm", True),
    ("our-ip-scan", "an IP Scan from the national office", False),
    ("our-ip-scan", "our IP Scan", True),
    ("free-ip-scan", "free IP Sentinel", False),
    ("free-ip-scan", "free IP Scan", True),
    ("apply-now", "do not say apply now", False),
    ("apply-now", "apply now", True),
    ("vouchers-open", "never say vouchers are open", False),
    ("vouchers-open", "vouchers are open", True),
    ("reopen-date-fact", "described a reopening as expected in November 2026", False),
    ("reopen-date-fact", "vouchers reopen on 1 May 2027", True),
    ("eligibility-verdict", "do not say you are eligible", False),
    ("eligibility-verdict", "you are eligible", True),
    ("we-will-file", "do not say we will file this for you", False),
    ("we-will-file", "we will file this for you", True),
    ("noticed-claim", "what we noticed", False),
    ("noticed-claim", "I noticed", True),
    ("verified-claim", "not sources verified", False),
    ("verified-claim", "sources verified", True),
    ("kills-novelty", "never kills novelty", False),
    ("kills-novelty", "kills novelty", True),
)


class ClaimRuleTests(unittest.TestCase):
    def test_every_rule_has_a_pass_and_a_fail(self) -> None:
        ids = {rule.id for rule in claim_rules.CLAIM_RULES}
        self.assertEqual(len(ids), len(claim_rules.CLAIM_RULES))
        passed = {rule_id for rule_id, _line, hit in CASES if not hit}
        failed = {rule_id for rule_id, _line, hit in CASES if hit}
        self.assertEqual(passed, ids)
        self.assertEqual(failed, ids)
        for rule_id, line, should_hit in CASES:
            with self.subTest(rule=rule_id, hit=should_hit):
                found = claim_rules.uncleared_rule_ids(line)
                if should_hit:
                    self.assertIn(rule_id, found)
                else:
                    self.assertNotIn(rule_id, found)

    def test_only_two_rules_ignore_negation(self) -> None:
        non = {rule.id for rule in claim_rules.CLAIM_RULES if not rule.negatable}
        self.assertEqual(non, {"percent-near-refund", "currency-amount"})
        self.assertIn("percent-near-refund", claim_rules.uncleared_rule_ids("do not say reimbursed at 90%"))
        self.assertIn("currency-amount", claim_rules.uncleared_rule_ids("do not write 10 EUR"))
        self.assertIn("percent-near-refund", claim_rules.uncleared_rule_ids("90% paid"))
        self.assertIn("percent-near-refund", claim_rules.uncleared_rule_ids("a refund of 15 percent"))
        self.assertNotIn("currency-amount", claim_rules.uncleared_rule_ids("EUR is a code with no number"))
        self.assertIn("currency-amount", claim_rules.uncleared_rule_ids("€10"))
        self.assertIn("currency-amount", claim_rules.uncleared_rule_ids("$10"))
        self.assertIn("currency-amount", claim_rules.uncleared_rule_ids("10 euros"))
        self.assertIn("currency-amount", claim_rules.uncleared_rule_ids("10 Kč"))

    def test_negation_cases(self) -> None:
        self.assertEqual(claim_rules.uncleared_rule_ids("not legal advice"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("Not legal advice."), [])
        self.assertIn("legal-advice-positive", claim_rules.uncleared_rule_ids("this is legal advice"))
        mixed = "it is not legal advice, but we give legal advice"
        hits = claim_rules.classify_line(mixed)
        legal = [hit for hit in hits if hit.rule_id == "legal-advice-positive"]
        self.assertEqual(len(legal), 2)
        self.assertTrue(legal[0].cleared)
        self.assertFalse(legal[1].cleared)
        self.assertIn("legal-advice-positive", claim_rules.uncleared_rule_ids("your lawyer"))
        self.assertIn("legal-advice-positive", claim_rules.uncleared_rule_ids("attorney-client"))
        self.assertEqual(claim_rules.uncleared_rule_ids("never your lawyer"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("no guarantee"), [])
        self.assertIn("guaranteed", claim_rules.uncleared_rule_ids("guaranteed protection"))
        self.assertEqual(claim_rules.uncleared_rule_ids("do not say guaranteed"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("guaranteed protection", "banned phrases:"), [])
        both = "It is not legal advice and carries no guarantees."
        self.assertEqual(claim_rules.uncleared_rule_ids(both), [])

    def test_provider_and_free_exceptions(self) -> None:
        for line in (
            "IP Scan by a provider listed by the national office",
            "IP Scan by an provider listed by the national office",
            "IP Scan by any provider listed by the national office",
            "IP Scan by the provider listed by the national office",
            "Only a provider listed by the national office can deliver the official IP Scan.",
            "free IP Sentinel",
        ):
            with self.subTest(line=line):
                self.assertNotIn("provider-claim", claim_rules.uncleared_rule_ids(line))
                self.assertNotIn("free-ip-scan", claim_rules.uncleared_rule_ids(line))
        self.assertIn("provider-claim", claim_rules.uncleared_rule_ids("we deliver your IP Scan"))
        self.assertIn("provider-claim", claim_rules.uncleared_rule_ids("we run your IP Scan"))
        self.assertIn("provider-claim", claim_rules.uncleared_rule_ids("we do your IP Scan"))

    def test_reopen_hedges(self) -> None:
        self.assertEqual(
            claim_rules.uncleared_rule_ids("it described a reopening as expected in November 2026 while UNVERIFIED"),
            [],
        )
        self.assertEqual(claim_rules.uncleared_rule_ids("UNVERIFIED reopening on 1 May 2027"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("vouchers may reopen on 1 June 2027"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("the window will reopen"), [])
        self.assertIn("reopen-date-fact", claim_rules.uncleared_rule_ids("reopen in May 2027"))
        window = (ROOT / "references" / "sme-fund-window.json").read_text(encoding="utf-8")
        for line in window.splitlines():
            self.assertNotIn("reopen-date-fact", claim_rules.uncleared_rule_ids(line))

    def test_residency_hosting_shapes(self) -> None:
        flagged = (
            "hosted in the EU",
            "stored in the EU",
            "European servers keep your data",
            "EU-based servers",
            "data remains in Europe",
            "European data centres",
        )
        for line in flagged:
            with self.subTest(line=line):
                self.assertIn("residency-claim", claim_rules.uncleared_rule_ids(line))
        self.assertEqual(claim_rules.uncleared_rule_ids("not hosted in the EU"), [])
        self.assertEqual(
            claim_rules.uncleared_rule_ids("we make no claim that data is stored in the EU"),
            [],
        )

    def test_percent_near_pay_and_back(self) -> None:
        self.assertIn("percent-near-refund", claim_rules.uncleared_rule_ids("EU pays 90%"))
        self.assertIn("percent-near-refund", claim_rules.uncleared_rule_ids("You get 90 % back"))

    def test_false_negation_phrases_do_not_clear(self) -> None:
        self.assertIn(
            "residency-claim",
            claim_rules.uncleared_rule_ids("Not just GDPR compliant but fast"),
        )
        self.assertIn(
            "legal-advice-positive",
            claim_rules.uncleared_rule_ids("No doubt this is legal advice"),
        )
        self.assertEqual(claim_rules.uncleared_rule_ids("not legal advice"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("Not legal advice."), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("do not say apply now"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("never say vouchers are open"), [])

    def test_apply_and_voucher_availability(self) -> None:
        for line in (
            "apply today",
            "apply immediately",
            "vouchers open now",
            "vouchers are available",
        ):
            with self.subTest(line=line):
                self.assertTrue(claim_rules.uncleared_rule_ids(line))

    def test_other_bans(self) -> None:
        self.assertIn("residency-claim", claim_rules.uncleared_rule_ids("GDPR"))
        self.assertIn("residency-claim", claim_rules.uncleared_rule_ids("EU data residency"))
        self.assertIn("residency-claim", claim_rules.uncleared_rule_ids("data stays in the EU"))
        self.assertEqual(claim_rules.uncleared_rule_ids("not EU-hosted"), [])
        self.assertIn("noticed-claim", claim_rules.uncleared_rule_ids("I detected"))
        self.assertIn("noticed-claim", claim_rules.uncleared_rule_ids("I monitored your work"))
        self.assertIn("verified-claim", claim_rules.uncleared_rule_ids("links valid"))
        self.assertIn("verified-claim", claim_rules.uncleared_rule_ids("reviewed by counsel"))
        self.assertEqual(claim_rules.uncleared_rule_ids('Never write "sources verified" / "links valid".'), [])
        self.assertIn("eligibility-verdict", claim_rules.uncleared_rule_ids("you qualify"))
        self.assertIn("kills-novelty", claim_rules.uncleared_rule_ids("this kills novelty"))
        self.assertEqual(claim_rules.uncleared_rule_ids("do not say kills novelty"), [])

    def test_emphasis_is_stripped_before_matching(self) -> None:
        self.assertEqual(claim_rules.uncleared_rule_ids("**not legal advice**"), [])
        self.assertIn("legal-advice-positive", claim_rules.uncleared_rule_ids("this is **legal advice**"))

    def test_allow_list_invariants(self) -> None:
        files: dict[str, list[Path]] = {}
        for path in claim_rules.iter_claim_files(ROOT):
            rel = path.relative_to(ROOT).as_posix()
            files.setdefault(claim_rules.pack_relative(rel), []).append(path)
        seen: set[tuple[str, str, str]] = set()
        self.assertGreaterEqual(len(claim_rules.ALLOW_LIST), 1)
        for entry in claim_rules.ALLOW_LIST:
            self.assertTrue(entry.reason.strip())
            self.assertIn(entry.kind, {"false-positive", "legacy-claim-review"})
            self.assertNotIn(Path(entry.path).name, claim_rules.NEW_FILE_NAMES)
            key = (entry.rule_id, entry.path, entry.line)
            self.assertNotIn(key, seen)
            seen.add(key)
            matched = False
            for path in files.get(entry.path, []):
                lines = path.read_text(encoding="utf-8").splitlines()
                for index, raw in enumerate(lines):
                    if raw.strip() != entry.line:
                        continue
                    prev = lines[index - 1] if index else ""
                    if entry.rule_id in claim_rules.uncleared_rule_ids(raw, prev):
                        matched = True
            self.assertTrue(matched, entry.path)

    def test_real_tree_claims_pass(self) -> None:
        scan = claim_rules.scan_claims(ROOT)
        self.assertEqual(scan.errors, [])
        self.assertGreater(scan.allow_count, 0)
        for name in claim_rules.NEW_FILE_NAMES:
            self.assertFalse(any(entry.path.endswith(name) for entry in claim_rules.ALLOW_LIST))

    def test_missing_disclaimer_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "SKILL.md").write_text("hello\n", encoding="utf-8")
            for pack in claim_rules.PACK_DIRS:
                (root / pack).mkdir()
                (root / pack / "SKILL.md").write_text("hello\n", encoding="utf-8")
            errors = claim_rules.disclaimer_errors(root)
            self.assertEqual(len(errors), 5)
            (root / "SKILL.md").write_text("Not legal advice.\n", encoding="utf-8")
            for pack in claim_rules.PACK_DIRS:
                (root / pack / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
            self.assertEqual(claim_rules.disclaimer_errors(root), [])

    def test_version_lines_stay_readable_by_sync(self) -> None:
        text = (SCRIPTS / "check-hygiene.py").read_text(encoding="utf-8")
        self.assertIn('VERSION = "0.5.56-free"\n', text)
        self.assertIsNotNone(
            re.search(
                r'^PACKS = \("chatgpt-skill", "claude-skill", "grok-skill", "cursor-skill"\)$',
                text,
                re.M,
            )
        )

    def test_extra_pattern_file(self) -> None:
        token = "zzdummyfirm"
        outside = Path(tempfile.mkdtemp())
        pattern_file = outside / "patterns.txt"
        pattern_file.write_text("# comment\n\n" + token + "\n", encoding="utf-8")
        loaded = claim_rules.load_extra_patterns(str(pattern_file), None, ROOT)
        self.assertEqual(loaded.errors, [])
        self.assertFalse(loaded.skipped)
        messages = claim_rules.pattern_line_errors("notes.md", "see " + token + " here\n", loaded.patterns)
        self.assertEqual(messages, ["extra pattern #1 in notes.md:1"])
        self.assertNotIn(token, "\n".join(messages))

        inside = claim_rules.load_extra_patterns(str(ROOT / "README.md"), None, ROOT)
        self.assertFalse(inside.skipped)
        self.assertTrue(any("inside the repo" in error for error in inside.errors))

        missing = claim_rules.load_extra_patterns(str(outside / "absent.txt"), None, ROOT)
        self.assertTrue(any("missing" in error for error in missing.errors))

        bad = outside / "bad.txt"
        bad.write_text("# note\n(\n", encoding="utf-8")
        invalid = claim_rules.load_extra_patterns(str(bad), None, ROOT)
        self.assertTrue(any("line 2" in error for error in invalid.errors))
        self.assertNotIn("(", "\n".join(invalid.errors))

        skipped = claim_rules.load_extra_patterns(None, None, ROOT)
        self.assertTrue(skipped.skipped)
        self.assertEqual(skipped.errors, [])

        unreadable = Path(tempfile.mkdtemp())
        blocked = claim_rules.load_extra_patterns(str(unreadable), None, ROOT)
        self.assertTrue(any("unreadable" in error for error in blocked.errors))

        empty = outside / "empty.txt"
        empty.write_text("# only a comment\n\n", encoding="utf-8")
        chosen = claim_rules.load_extra_patterns(str(empty), str(outside / "absent.txt"), ROOT)
        self.assertEqual(chosen.errors, [])
        self.assertEqual(chosen.patterns, [])

    def test_scan_reports_extra_pattern_without_the_text(self) -> None:
        token = "zzdummyfirm"
        pattern = re.compile(token, re.IGNORECASE)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "README.md").write_text("see " + token + "\n", encoding="utf-8")
            (root / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
            for pack in claim_rules.PACK_DIRS:
                (root / pack).mkdir()
                (root / pack / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
            scan = claim_rules.scan_claims(root, [pattern])
        blob = "\n".join(scan.errors)
        self.assertIn("extra pattern #1 in README.md:1", blob)
        self.assertNotIn(token, blob)

    def test_clause_boundaries_block_a_cue(self) -> None:
        flagged = (
            ("Not legal advice - this is guaranteed", "guaranteed"),
            ("Not legal advice: it is guaranteed", "guaranteed"),
            ("Not legal advice (it is guaranteed)", "guaranteed"),
            ("No guarantees because we say it is guaranteed", "guaranteed"),
            ("Not legal advice then apply now", "apply-now"),
            ("not a lawyer so this is legal advice", "legal-advice-positive"),
            ("no | guaranteed", "guaranteed"),
            ("Not legal advice\u2014it is guaranteed", "guaranteed"),
            ("Not legal advice \u2013 guaranteed", "guaranteed"),
            ("No guarantees since it is guaranteed", "guaranteed"),
            ("Not legal advice while it is guaranteed", "guaranteed"),
            ("Not legal advice although it is guaranteed", "guaranteed"),
            ("Not legal advice or it is guaranteed", "guaranteed"),
        )
        for line, rule_id in flagged:
            with self.subTest(line=line):
                self.assertIn(rule_id, claim_rules.uncleared_rule_ids(line))
        allowed = (
            "No guarantees. Not legal advice",
            "This is not legal advice",
            "do not say guaranteed",
            "not an IP Scan provider",
        )
        for line in allowed:
            with self.subTest(line=line):
                self.assertEqual(claim_rules.uncleared_rule_ids(line), [])

    def test_line_marker_stops_at_the_sentence_end(self) -> None:
        flagged = "Banned phrases: none. We guarantee protection"
        self.assertIn("guaranteed", claim_rules.uncleared_rule_ids(flagged))
        self.assertEqual(claim_rules.uncleared_rule_ids("Banned phrases: guaranteed"), [])
        self.assertEqual(claim_rules.uncleared_rule_ids("guaranteed protection", "banned phrases:"), [])
        carried = claim_rules.uncleared_rule_ids("none. We guarantee protection", "Banned phrases:")
        self.assertEqual(carried, ["guaranteed"])

    def test_normalize_folds_spaces_hyphens_and_width(self) -> None:
        self.assertIn("legal-advice-positive", claim_rules.uncleared_rule_ids("this is legal  advice"))
        self.assertIn("legal-advice-positive", claim_rules.uncleared_rule_ids("this is legal-advice"))
        self.assertIn("guaranteed", claim_rules.uncleared_rule_ids("a guaran\u00adtee"))
        full_width = "reimbursed at \uff19\uff10\uff05"
        self.assertIn("percent-near-refund", claim_rules.uncleared_rule_ids(full_width))
        self.assertIn("guaranteed", claim_rules.uncleared_rule_ids("a guar\u200bantee"))

    def test_currency_word_percent_and_reopen_spellings(self) -> None:
        for line in ("10 CHF", "GBP 5", "10 USD", "\u00a310"):
            with self.subTest(line=line):
                self.assertIn("currency-amount", claim_rules.uncleared_rule_ids(line))
        self.assertIn(
            "percent-near-refund",
            claim_rules.uncleared_rule_ids("reimbursed at ninety percent"),
        )
        self.assertNotIn(
            "percent-near-refund",
            claim_rules.uncleared_rule_ids("ninety percent complete"),
        )
        self.assertIn(
            "reopen-date-fact",
            claim_rules.uncleared_rule_ids("vouchers re-open on 1 May 2027"),
        )
        self.assertIn(
            "reopen-date-fact",
            claim_rules.uncleared_rule_ids("vouchers reopen on 1 May 2027"),
        )

    def test_mixed_script_warns_without_mapping_a_lookalike(self) -> None:
        inserted = "guarant" + "\u0430" + "eed"
        swapped = "guar" + "\u0430" + "nteed"
        self.assertTrue(claim_rules.mixed_script_line("see " + inserted))
        self.assertFalse(claim_rules.mixed_script_line(swapped))
        self.assertFalse(claim_rules.mixed_script_line("guaranteed"))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "README.md").write_text("see " + inserted + "\n", encoding="utf-8")
            (root / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
            for pack in claim_rules.PACK_DIRS:
                (root / pack).mkdir()
                (root / pack / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
            scan = claim_rules.scan_claims(root)
        self.assertTrue(any(item.startswith("WARNING mixed-script in README.md:") for item in scan.warnings))
        self.assertFalse(any("mixed-script" in item for item in scan.errors))

    def test_long_digit_line_stays_fast(self) -> None:
        import time

        line = "9" * 20000
        started = time.perf_counter()
        found = claim_rules.uncleared_rule_ids(line)
        elapsed = time.perf_counter() - started
        self.assertEqual(found, [])
        self.assertLess(elapsed, 2.0)
        started = time.perf_counter()
        claim_rules.uncleared_rule_ids("9" * 10000)
        self.assertLess(time.perf_counter() - started, 0.1)

    def test_extra_pattern_file_rejects_undecodable_bytes(self) -> None:
        outside = Path(tempfile.mkdtemp())
        raw = outside / "patterns.txt"
        raw.write_bytes(b"\xff\xfe\x80")
        loaded = claim_rules.load_extra_patterns(str(raw), None, ROOT)
        blob = "\n".join(loaded.errors)
        self.assertIn(raw.name, blob)
        self.assertNotIn("Traceback", blob)
        self.assertNotIn("UnicodeDecodeError", blob)
        self.assertNotIn(str(outside), blob)

    def test_tip_scan_reports_seeded_address(self) -> None:
        address = "person@example.com"
        cases = (
            ("CHANGELOG.md", "# log\nplain line\n", 3),
            ("PUSH_TO_GITHUB.txt", "push the branch\n", 2),
        )
        for name, starter, lineno in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as raw:
                    src = Path(raw) / "src"
                    src.mkdir()
                    (src / "SKILL.md").write_text("Not legal advice.\n", encoding="utf-8")
                    for pack in claim_rules.PACK_DIRS:
                        (src / pack).mkdir()
                        (src / pack / "SKILL.md").write_text("not legal advice\n", encoding="utf-8")
                    (src / "CHANGELOG.md").write_text("# log\nplain line\n", encoding="utf-8")
                    (src / "PUSH_TO_GITHUB.txt").write_text("push the branch\n", encoding="utf-8")
                    dst = Path(raw) / "tree"
                    shutil.copytree(src, dst)
                    target = dst / name
                    target.write_text(starter + "contact " + address + "\n", encoding="utf-8")
                    scan = claim_rules.scan_claims(dst)
                    blob = "\n".join(scan.errors + scan.warnings)
                    self.assertEqual(scan.errors, [f"email in {name}:{lineno}"])
                    self.assertNotIn(address, blob)


if __name__ == "__main__":
    unittest.main()
