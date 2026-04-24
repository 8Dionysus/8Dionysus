from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import audit_agents_map


class AgentsMapAuditTests(unittest.TestCase):
    def test_live_scan_counts_nested_agents_and_validator_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo = workspace / "8Dionysus"
            (repo / "docs").mkdir(parents=True)
            (repo / "generated").mkdir()
            (repo / "scripts").mkdir()
            (repo / "AGENTS.md").write_text("# AGENTS.md\nroot\n", encoding="utf-8")
            (repo / "docs" / "AGENTS.md").write_text("# AGENTS.md\ndocs\n", encoding="utf-8")
            (repo / "generated" / "AGENTS.md").write_text("# AGENTS.md\ngenerated\n", encoding="utf-8")
            (repo / "scripts" / "validate_nested_agents.py").write_text(
                'REQUIRED_AGENTS = {"docs/AGENTS.md": (), "generated/AGENTS.md": (), "schemas/AGENTS.md": ()}\n',
                encoding="utf-8",
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("8Dionysus",),
                include_extra_repos=False,
            )
            scanned = payload["repositories"][0]

            self.assertEqual(payload["schema_version"], audit_agents_map.SCHEMA_VERSION)
            self.assertEqual(scanned["checkout_state"], "scanned")
            self.assertEqual(scanned["agents_md_count"], 3)
            self.assertEqual(scanned["nested_agents_count"], 2)
            self.assertTrue(scanned["validator_present"])
            self.assertEqual(scanned["validator_required_count"], 3)
            self.assertEqual(scanned["missing_required_agents"], ["schemas/AGENTS.md"])
            self.assertIn("scripts", scanned["high_risk_dirs_without_agents"])
            self.assertEqual(scanned["unvalidated_nested_agents"], [])

    def test_validator_extraction_accepts_pack1_variable_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo = workspace / "aoa-sdk"
            (repo / "docs").mkdir(parents=True)
            (repo / "scripts").mkdir()
            (repo / "AGENTS.md").write_text("# AGENTS.md\nroot\n", encoding="utf-8")
            (repo / "docs" / "AGENTS.md").write_text("# AGENTS.md\ndocs\n", encoding="utf-8")
            (repo / "scripts" / "validate_nested_agents.py").write_text(
                'REQUIRED_AGENTS_DOCS = {"docs/AGENTS.md": (), "schemas/AGENTS.md": ()}\n',
                encoding="utf-8",
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("aoa-sdk",),
                include_extra_repos=False,
            )
            scanned = payload["repositories"][0]

            self.assertEqual(scanned["validator_required_count"], 2)
            self.assertEqual(scanned["missing_required_agents"], ["schemas/AGENTS.md"])

    def test_workspace_manifest_preferred_path_beats_runtime_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            source = root / "src" / "abyss-stack"
            runtime = workspace / "abyss-stack"
            sdk_manifest = workspace / "aoa-sdk" / ".aoa"
            source.mkdir(parents=True)
            runtime.mkdir(parents=True)
            sdk_manifest.mkdir(parents=True)
            (source / "AGENTS.md").write_text("# AGENTS.md\nsource\n", encoding="utf-8")
            (runtime / "generated").mkdir()
            (runtime / "generated" / "AGENTS.md").write_text("# AGENTS.md\nruntime\n", encoding="utf-8")
            (sdk_manifest / "workspace.toml").write_text(
                '\n[repos.abyss-stack]\npreferred = ["{workspace_parent}/../src/abyss-stack"]\n',
                encoding="utf-8",
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("abyss-stack",),
                include_extra_repos=False,
            )
            scanned = payload["repositories"][0]

            self.assertTrue(scanned["root_agents_present"])
            self.assertEqual(scanned["agents_md_count"], 1)
            self.assertNotEqual(scanned["path_hint"], "abyss-stack")
            self.assertNotIn(str(root), scanned["path_hint"])

    def test_unvalidated_nested_agents_are_reported_without_executing_validator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo = workspace / "aoa-skills"
            (repo / "skills").mkdir(parents=True)
            (repo / "scripts").mkdir()
            (repo / "AGENTS.md").write_text("# AGENTS.md\nroot\n", encoding="utf-8")
            (repo / "skills" / "AGENTS.md").write_text("# AGENTS.md\nskills\n", encoding="utf-8")
            (repo / "scripts" / "validate_nested_agents.py").write_text(
                "raise RuntimeError('validator must not be executed during map extraction')\n"
                'REQUIRED_AGENTS = {"docs/AGENTS.md": ()}\n',
                encoding="utf-8",
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("aoa-skills",),
                include_extra_repos=False,
            )
            scanned = payload["repositories"][0]

            self.assertEqual(scanned["missing_required_agents"], ["docs/AGENTS.md"])
            self.assertEqual(scanned["unvalidated_nested_agents"], ["skills/AGENTS.md"])

    def test_public_baseline_is_stable_and_json_serializable(self) -> None:
        payload = audit_agents_map.build_public_baseline_map()
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

        self.assertEqual(payload["audit_mode"], "public-baseline")
        self.assertEqual(payload["totals"]["known_public_repositories"], 16)
        self.assertIn("Agents-of-Abyss", payload["known_repositories"])
        self.assertIn("agents_map_public_baseline", rendered)
        self.assertNotIn("/mnt/", rendered)

    def test_markdown_report_contains_regeneration_commands_and_issue_legend(self) -> None:
        payload = audit_agents_map.build_public_baseline_map()
        markdown = audit_agents_map.render_markdown(payload)

        self.assertIn("python scripts/audit_agents_map.py", markdown)
        self.assertIn("--workspace-root <workspace-root>", markdown)
        self.assertIn("unvalidated_nested_agents", markdown)
        self.assertIn("high_risk_dirs_without_agents", markdown)
        self.assertIn("8Dionysus", markdown)


if __name__ == "__main__":
    unittest.main()
