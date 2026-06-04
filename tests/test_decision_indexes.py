from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "generate_decision_indexes.py"
SPEC = importlib.util.spec_from_file_location("generate_decision_indexes", SCRIPT_PATH)
decision_indexes = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = decision_indexes
SPEC.loader.exec_module(decision_indexes)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _decision_text(*, decision_id: str = "8DION-D-0001", original_date: str = "2026-06-04") -> str:
    return "\n".join(
        [
            "# Example",
            "",
            "## Index Metadata",
            "",
            f"- Decision ID: {decision_id}",
            f"- Original date: {original_date}",
            "- Surface classes: public entry",
            "- Route anchors: README.md",
            "- Owner lanes: 8Dionysus",
            "- Guard families: owner boundary",
            "- Posture: accepted",
            "",
        ]
    )


class DecisionIndexTests(unittest.TestCase):
    def test_live_decision_indexes_are_current(self) -> None:
        self.assertEqual([], decision_indexes.validate_decision_indexes(REPO_ROOT))

    def test_by_number_index_exposes_canonical_id_and_path(self) -> None:
        records, issues = decision_indexes.collect_decision_records(REPO_ROOT)

        self.assertEqual([], issues)
        rendered = decision_indexes.render_index_files(records)
        by_number = rendered[decision_indexes.INDEX_DIR / "by-number.md"]

        self.assertIn("| Decision ID | Date | Decision | Path |", by_number)
        self.assertIn("8DION-D-0001", by_number)
        self.assertIn("`docs/decisions/8DION-D-0001-shared-root-projection.md`", by_number)

    def test_grouped_indexes_are_lookup_bullets_not_repeated_ledgers(self) -> None:
        records, issues = decision_indexes.collect_decision_records(REPO_ROOT)

        self.assertEqual([], issues)
        rendered = decision_indexes.render_index_files(records)
        by_anchor = rendered[decision_indexes.INDEX_DIR / "by-route-anchor.md"]

        self.assertNotIn("| Decision | Date |", by_anchor)
        self.assertIn("- [8DION-D-", by_anchor)
        self.assertIn("(`docs/decisions/8DION-D-", by_anchor)

    def test_decision_id_must_match_filename_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            _write(
                repo_root / "docs" / "decisions" / "8DION-D-0001-example.md",
                _decision_text(decision_id="8DION-D-0002"),
            )

            _, issues = decision_indexes.collect_decision_records(repo_root)

        self.assertTrue(any("Decision ID must match filename prefix" in message for _, message in issues))

    def test_original_date_must_use_canonical_yyyy_mm_dd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            _write(
                repo_root / "docs" / "decisions" / "8DION-D-0001-example.md",
                _decision_text(original_date="20260604"),
            )

            _, issues = decision_indexes.collect_decision_records(repo_root)

        self.assertIn(
            ("docs/decisions/8DION-D-0001-example.md", "Original date must use YYYY-MM-DD"),
            issues,
        )

    def test_legacy_numeric_decision_filename_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            _write(repo_root / "docs" / "decisions" / "0001-example.md", _decision_text())

            _, issues = decision_indexes.collect_decision_records(repo_root)

        self.assertTrue(any("top-level decision markdown must use 8DION-D-####-slug.md" in message for _, message in issues))


if __name__ == "__main__":
    unittest.main()
