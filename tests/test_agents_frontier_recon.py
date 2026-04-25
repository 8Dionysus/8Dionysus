from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "recon_agents_frontier.py"
SPEC = importlib.util.spec_from_file_location("recon_agents_frontier", SCRIPT_PATH)
frontier = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = frontier
SPEC.loader.exec_module(frontier)


class AgentsFrontierReconTests(unittest.TestCase):
    def sample_map(self) -> dict[str, object]:
        return {
            "schema_version": "test_agents_map",
            "audit_mode": "test",
            "repositories": [
                {
                    "name": "8Dionysus",
                    "kind": "public-route-map",
                    "checkout_state": "scanned",
                    "validator_present": True,
                    "high_risk_dirs_without_agents": ["docs", "schemas", ".codex"],
                },
                {
                    "name": "abyss-stack",
                    "kind": "runtime-infrastructure",
                    "checkout_state": "scanned",
                    "validator_present": True,
                    "high_risk_dirs_without_agents": ["examples"],
                },
            ],
        }

    def test_prioritizes_contract_and_projection_dirs(self) -> None:
        result = frontier.build_frontier(self.sample_map())
        top_paths = [item["path"] for item in result["top_candidates"][:2]]
        self.assertIn(".codex/AGENTS.md", top_paths)
        self.assertIn("schemas/AGENTS.md", top_paths)
        self.assertEqual("P0", result["top_candidates"][0]["priority"])

    def test_preserves_legacy_unvalidated_signal(self) -> None:
        payload = {
            "repositories": [
                {
                    "name": "legacy",
                    "kind": "extra",
                    "checkout_state": "scanned",
                    "validator_present": True,
                    "high_risk_dirs_without_agents": [],
                    "unvalidated_nested_agents": ["docs/AGENTS.md"],
                }
            ]
        }
        result = frontier.build_frontier(payload)
        repo = result["repositories"][0]
        self.assertEqual(["docs/AGENTS.md"], repo["unvalidated_by_any_agents_validator"])
        self.assertEqual(["docs/AGENTS.md"], repo["not_in_nested_validator_map"])

    def test_markdown_contains_candidate_table(self) -> None:
        result = frontier.build_frontier(self.sample_map())
        text = frontier.render_markdown(result)
        self.assertIn("# AGENTS frontier reconnaissance", text)
        self.assertIn("| Priority | Score | Repository | Path | Decision | Rationale |", text)
        self.assertIn("schemas/AGENTS.md", text)

    def test_cli_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            map_path = root / "agents_map.min.json"
            json_path = root / "frontier.min.json"
            md_path = root / "frontier.md"
            map_path.write_text(json.dumps(self.sample_map()), encoding="utf-8")
            code = frontier.main(["--map", str(map_path), "--write", str(json_path), "--markdown", str(md_path)])
            self.assertEqual(0, code)
            self.assertTrue(json_path.is_file())
            self.assertTrue(md_path.is_file())
            data = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual("8dionysus_agents_frontier_recon_v1", data["schema_version"])


if __name__ == "__main__":
    unittest.main()
