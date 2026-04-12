from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_codex_plane_rollout_contracts import validate_codex_plane_rollout_contracts


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class CodexPlaneRolloutTests(unittest.TestCase):
    def test_rollout_docs_stay_discoverable_from_primary_routes(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        install = (REPO_ROOT / "docs" / "WORKSPACE_INSTALL.md").read_text(encoding="utf-8")
        regeneration = (REPO_ROOT / "docs" / "CODEX_PLANE_REGENERATION.md").read_text(
            encoding="utf-8"
        )
        rollout = (REPO_ROOT / "docs" / "CODEX_PLANE_ROLLOUT.md").read_text(encoding="utf-8")

        self.assertIn("docs/CODEX_PLANE_ROLLOUT.md", readme)
        self.assertIn("docs/CODEX_PLANE_ROLLOUT.md", install)
        self.assertIn("CODEX_PLANE_ROLLOUT.md", regeneration)
        self.assertIn("When deployment signals disagree, prefer:", rollout)
        self.assertIn("/.codex/generated/rollout/codex_plane_trust_state.current.json", rollout)

    def test_component_refresh_route_stays_discoverable_and_owner_bounded(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        install = (REPO_ROOT / "docs" / "WORKSPACE_INSTALL.md").read_text(encoding="utf-8")
        regeneration = (REPO_ROOT / "docs" / "CODEX_PLANE_REGENERATION.md").read_text(
            encoding="utf-8"
        )
        rollout = (REPO_ROOT / "docs" / "CODEX_PLANE_ROLLOUT.md").read_text(encoding="utf-8")
        component_refresh = (REPO_ROOT / "docs" / "COMPONENT_REFRESH_ROUTE.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/COMPONENT_REFRESH_ROUTE.md", readme)
        self.assertIn("generated or install drift", agents)
        self.assertIn("owner repo", agents)
        self.assertIn("docs/COMPONENT_REFRESH_ROUTE.md", install)
        self.assertIn("docs/COMPONENT_REFRESH_ROUTE.md", regeneration)
        self.assertIn("COMPONENT_REFRESH_ROUTE.md", rollout)
        self.assertIn("component:codex-plane:shared-root", component_refresh)
        self.assertIn("config/codex_plane/runtime_manifest.v1.json", component_refresh)
        self.assertIn(".codex/config.toml", component_refresh)
        self.assertIn("route the evidence to the owner repo", component_refresh)

    def test_rollout_examples_validate_and_stay_coherent(self) -> None:
        validate_codex_plane_rollout_contracts()

        trust = load_json("examples/codex_plane_trust_state.example.json")
        regeneration = load_json("examples/codex_plane_regeneration_report.example.json")
        receipt = load_json("examples/codex_plane_rollout_receipt.example.json")

        self.assertEqual(trust["schema_version"], "8dionysus_codex_plane_trust_state_v1")
        self.assertEqual(
            regeneration["schema_version"],
            "8dionysus_codex_plane_regeneration_report_v1",
        )
        self.assertEqual(
            receipt["schema_version"],
            "8dionysus_codex_plane_rollout_receipt_v1",
        )
        self.assertEqual(receipt["trust_state_id"], trust["trust_state_id"])
        self.assertEqual(
            receipt["regeneration_report_id"],
            regeneration["regeneration_report_id"],
        )


if __name__ == "__main__":
    unittest.main()
