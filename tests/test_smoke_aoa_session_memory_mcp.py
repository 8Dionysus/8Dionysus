from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "smoke_aoa_session_memory_mcp.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("smoke_aoa_session_memory_mcp_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_evidence_ref_count_ignores_empty_lexical_ref_containers() -> None:
    module = load_smoke_module()

    assert module.evidence_ref_count({"lexical": {"results": [{"refs": {}}, {"refs": {"raw_refs": []}}]}}) == 0


def test_evidence_ref_count_counts_actual_raw_and_segment_refs() -> None:
    module = load_smoke_module()

    payload = {
        "evidence_refs": ["raw:line:1", {"segment_ref": "segment:one"}],
        "lexical": {
            "results": [
                {"refs": {"raw_ref": "raw:line:2"}},
                {"refs": {"segment_refs": ["segment:two", "segment:three"]}},
                {"refs": {"raw": {"session": "s1", "line": 3}}},
            ]
        },
        "packet": {"evidence_refs": ["raw:line:4"]},
    }

    assert module.evidence_ref_count(payload) == 7
