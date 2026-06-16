from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "smoke_aoa_evals_mcp.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke_aoa_evals_mcp_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SmokeAoaEvalsMcpTests(unittest.TestCase):
    def run_smoke_with_selection(
        self,
        selection_payload: dict[str, object],
    ) -> tuple[dict[str, object], list[str]]:
        module = load_smoke_module()
        calls: list[str] = []

        def result(payload: dict[str, object]) -> object:
            return types.SimpleNamespace(content=[types.SimpleNamespace(text=json.dumps(payload))])

        class FakeClientSession:
            def __init__(self, read: object, write: object) -> None:
                pass

            async def __aenter__(self) -> "FakeClientSession":
                return self

            async def __aexit__(self, *args: object) -> None:
                return None

            async def initialize(self) -> None:
                return None

            async def list_tools(self) -> object:
                return types.SimpleNamespace(
                    tools=[types.SimpleNamespace(name=name) for name in module.REQUIRED_TOOLS]
                )

            async def call_tool(self, name: str, args: dict[str, object]) -> object:
                calls.append(name)
                if name in {
                    "aoa_evals_inspect",
                    "aoa_evals_report_skeleton",
                    "aoa_evals_validate_evidence_candidate",
                }:
                    raise AssertionError(f"{name} should not run without a selected eval")
                payloads: dict[str, dict[str, object]] = {
                    "aoa_evals_select": selection_payload,
                    "aoa_evals_find_or_propose": {
                        "outcome": "proposed",
                        "read_only": True,
                        "source_mutation_allowed": False,
                        "proposal_validation": {"valid": True},
                        "proposal_context": {"packet": {"schema_version": "eval_need_v1"}},
                    },
                    "aoa_evals_runtime_status": {
                        "freshness": {"mirror_is_authority": False, "status": "current"}
                    },
                    "aoa_evals_runtime_candidate_exports": {
                        "count": 0,
                        "candidates": [],
                        "private_payloads_included": False,
                    },
                }
                return result(payloads[name])

        class FakeStdioClient:
            async def __aenter__(self) -> tuple[object, object]:
                return object(), object()

            async def __aexit__(self, *args: object) -> None:
                return None

        class FakeStdioServerParameters:
            def __init__(self, *args: object, **kwargs: object) -> None:
                pass

        mcp_module = types.ModuleType("mcp")
        mcp_module.ClientSession = FakeClientSession
        mcp_module.StdioServerParameters = FakeStdioServerParameters
        client_module = types.ModuleType("mcp.client")
        stdio_module = types.ModuleType("mcp.client.stdio")
        stdio_module.stdio_client = lambda params: FakeStdioClient()

        with mock.patch.dict(
            sys.modules,
            {
                "mcp": mcp_module,
                "mcp.client": client_module,
                "mcp.client.stdio": stdio_module,
            },
        ):
            smoke = asyncio.run(module.run_smoke(ROOT))

        return smoke, calls

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

    def test_empty_selection_skips_inspect_report_and_validation_followups(self) -> None:
        smoke, calls = self.run_smoke_with_selection({"matches": []})

        self.assertFalse(smoke["ok"])
        self.assertEqual(smoke["selected_eval"], "")
        self.assertIsNone(smoke["candidate_only"])
        self.assertIsNone(smoke["candidate_validation"])
        self.assertEqual(smoke["errors"], ["aoa_evals_select returned no bounded candidates"])
        self.assertNotIn("aoa_evals_inspect", calls)
        self.assertNotIn("aoa_evals_report_skeleton", calls)
        self.assertNotIn("aoa_evals_validate_evidence_candidate", calls)

    def test_malformed_selection_reports_error_before_selected_eval_followups(self) -> None:
        for selection_payload in ({"matches": [{}]}, {"matches": [{"name": 123}]}):
            with self.subTest(selection_payload=selection_payload):
                smoke, calls = self.run_smoke_with_selection(selection_payload)

                self.assertFalse(smoke["ok"])
                self.assertEqual(smoke["selected_eval"], "")
                self.assertIsNone(smoke["candidate_only"])
                self.assertIsNone(smoke["candidate_validation"])
                self.assertEqual(
                    smoke["errors"],
                    ["aoa_evals_select returned matches without a usable eval name"],
                )
                self.assertNotIn("aoa_evals_inspect", calls)
                self.assertNotIn("aoa_evals_report_skeleton", calls)
                self.assertNotIn("aoa_evals_validate_evidence_candidate", calls)


if __name__ == "__main__":
    unittest.main()
