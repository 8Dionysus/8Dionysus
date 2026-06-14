from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "smoke_aoa_evals_mcp.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke_aoa_evals_mcp_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmokeAoaEvalsMcpTests(unittest.TestCase):
    def test_matched_runtime_export_returns_none_without_matched_refs(self) -> None:
        module = load_smoke_module()

        self.assertIsNone(
            module.matched_runtime_export(
                {
                    "candidates": [
                        {"record_id": "one", "validation": {"matched_eval_refs": []}},
                        {"record_id": "two", "validation": {"valid": True}},
                    ]
                }
            )
        )

    def test_matched_runtime_export_selects_first_export_with_eval_refs(self) -> None:
        module = load_smoke_module()

        match = module.matched_runtime_export(
            {
                "candidates": [
                    {"record_id": "one", "validation": {"matched_eval_refs": []}},
                    {"record_id": "two", "validation": {"matched_eval_refs": ["aoa-bounded-change-quality"]}},
                ]
            }
        )

        self.assertEqual(match["record_id"], "two")

    def test_runtime_walkthrough_summary_marks_missing_export_as_skipped(self) -> None:
        module = load_smoke_module()

        summary = module.runtime_walkthrough_summary(None, None)

        self.assertEqual(
            summary,
            {
                "skipped": True,
                "reason": "no matched runtime candidate export in listing",
            },
        )


if __name__ == "__main__":
    unittest.main()
