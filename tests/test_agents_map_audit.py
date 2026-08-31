from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import audit_agents_map


class AgentsMapAuditTests(unittest.TestCase):
    def test_checked_in_v2_map_matches_schema_and_is_path_redacted(self) -> None:
        root = Path(__file__).resolve().parents[1]
        rendered = (root / "generated" / "agents_map.min.json").read_text(
            encoding="utf-8"
        )
        payload = json.loads(rendered)
        schema = json.loads(
            (root / "schemas" / "agents-map.schema.json").read_text(encoding="utf-8")
        )

        self.assertEqual(list(Draft202012Validator(schema).iter_errors(payload)), [])
        self.assertNotIn("/home/", rendered)
        self.assertNotIn("/srv/", rendered)
        self.assertEqual(payload["schema_version"], "8dionysus_agents_map_v2")
        self.assertEqual(
            payload["totals"]["review_items_total"],
            payload["totals"]["tracked_document_files"]
            + payload["totals"]["shared_root_files"],
        )

    def test_v2_schema_accepts_payload_without_additive_checkout_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = audit_agents_map.build_agents_map(
                Path(tmp),
                known_repositories=("aoa-routing",),
                include_extra_repos=False,
            )
            payload["repositories"][0].pop("checkout_requirement")
            schema = json.loads(
                (
                    Path(__file__).resolve().parents[1]
                    / "schemas"
                    / "agents-map.schema.json"
                ).read_text(encoding="utf-8")
            )

            self.assertEqual(
                list(Draft202012Validator(schema).iter_errors(payload)),
                [],
            )

    def test_missing_deprecated_routing_checkout_is_optional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = audit_agents_map.build_agents_map(
                Path(tmp),
                known_repositories=("aoa-routing",),
                include_extra_repos=False,
            )
            routing = payload["repositories"][0]

            self.assertEqual(routing["checkout_state"], "missing")
            self.assertEqual(routing["checkout_requirement"], "optional")
            self.assertEqual(routing["issues"], [])
            self.assertEqual(payload["totals"]["known_repositories_missing"], 0)
            self.assertEqual(payload["totals"]["optional_repositories_missing"], 1)
            self.assertEqual(payload["totals"]["repos_with_issues"], 0)

    def test_missing_active_repository_remains_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = audit_agents_map.build_agents_map(
                Path(tmp),
                known_repositories=("aoa-sdk",),
                include_extra_repos=False,
            )
            sdk = payload["repositories"][0]

            self.assertEqual(sdk["checkout_requirement"], "required")
            self.assertEqual(payload["totals"]["known_repositories_missing"], 1)
            self.assertEqual(payload["totals"]["optional_repositories_missing"], 0)
            self.assertTrue(sdk["issues"])

    def test_owner_repo_override_scans_clean_checkout_not_workspace_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace_owner = workspace / "8Dionysus"
            clean_owner = root / "clean-owner"
            workspace_owner.mkdir(parents=True)
            (workspace_owner / "AGENTS.md").write_text(
                "# AGENTS.md\nworkspace copy\n", encoding="utf-8"
            )
            (clean_owner / "docs").mkdir(parents=True)
            (clean_owner / "AGENTS.md").write_text(
                "# AGENTS.md\nclean owner\n", encoding="utf-8"
            )
            (clean_owner / "docs" / "AGENTS.md").write_text(
                "# AGENTS.md\ndocs\n", encoding="utf-8"
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("8Dionysus",),
                include_extra_repos=False,
                owner_repo_root=clean_owner,
            )
            scanned = payload["repositories"][0]

            self.assertEqual(scanned["path_hint"], "8Dionysus")
            self.assertEqual(scanned["agents_md_count"], 2)

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

    def test_dionysus_legacy_archive_is_not_scanned_as_active_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo = workspace / "Dionysus"
            (repo / "legacy" / "nested").mkdir(parents=True)
            (repo / "AGENTS.md").write_text("# AGENTS.md\nactive\n", encoding="utf-8")
            (repo / "legacy" / "AGENTS.md").write_text(
                "# AGENTS.md\narchived\n", encoding="utf-8"
            )
            (repo / "legacy" / "nested" / "AGENTS.md").write_text(
                "# AGENTS.md\narchived nested\n", encoding="utf-8"
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("Dionysus",),
                include_extra_repos=False,
            )
            scanned = payload["repositories"][0]

            self.assertEqual(scanned["agents_md_count"], 1)
            self.assertEqual(scanned["nested_agents_count"], 0)
            self.assertEqual(
                scanned["kind"],
                "personal-portrait-protocol",
            )

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

    def test_isolated_matrix_can_ignore_workspace_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            source = root / "source" / "abyss-stack"
            matrix = workspace / "abyss-stack"
            sdk_manifest = workspace / "aoa-sdk" / ".aoa"
            source.mkdir(parents=True)
            matrix.mkdir(parents=True)
            sdk_manifest.mkdir(parents=True)
            (source / "AGENTS.md").write_text("# AGENTS.md\nsource\n", encoding="utf-8")
            (matrix / "AGENTS.md").write_text("# AGENTS.md\nmatrix\n", encoding="utf-8")
            (sdk_manifest / "workspace.toml").write_text(
                f'\n[repos.abyss-stack]\npreferred = ["{source}"]\n',
                encoding="utf-8",
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("abyss-stack",),
                include_extra_repos=False,
                use_workspace_manifest=False,
            )
            scanned = payload["repositories"][0]

            self.assertEqual(scanned["path_hint"], "abyss-stack")
            self.assertTrue(scanned["root_agents_present"])

    def test_workspace_manifest_limited_toml_fallback_supports_preferred_paths(self) -> None:
        original_tomllib = audit_agents_map._tomllib
        audit_agents_map._tomllib = None
        try:
            manifest = audit_agents_map.load_workspace_toml(
                '''
                schema_version = 1

                [repos.abyss-stack]
                role = "source_checkout"
                preferred = ["~/src/abyss-stack", "{workspace_parent}/abyss-stack"] # keep source first
                runtime_mirror = "{workspace_parent}/abyss-stack"
                '''
            )
        finally:
            audit_agents_map._tomllib = original_tomllib

        self.assertEqual(
            manifest["repos"]["abyss-stack"]["preferred"],
            ["~/src/abyss-stack", "{workspace_parent}/abyss-stack"],
        )
        self.assertEqual(manifest["repos"]["abyss-stack"]["role"], "source_checkout")

    def test_workspace_manifest_limited_toml_parser_supports_preferred_paths(self) -> None:
        manifest = audit_agents_map._parse_limited_workspace_toml(
            '''
            schema_version = 1

            [repos.abyss-stack]
            role = "source_checkout"
            preferred = ["~/src/abyss-stack", "{workspace_parent}/abyss-stack"] # keep source first
            runtime_mirror = "{workspace_parent}/abyss-stack"
            '''
        )

        self.assertEqual(
            manifest["repos"]["abyss-stack"]["preferred"],
            ["~/src/abyss-stack", "{workspace_parent}/abyss-stack"],
        )
        self.assertEqual(manifest["repos"]["abyss-stack"]["role"], "source_checkout")

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

    def test_deleted_placeholder_disposition_accepts_absence_only_for_delete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            repo = workspace / "8Dionysus"
            repo.mkdir(parents=True)
            (repo / "AGENTS.md").write_text("# AGENTS.md\nroot\n", encoding="utf-8")
            dispositions = Path(tmp) / "dispositions.json"
            dispositions.write_text(
                json.dumps(
                    {
                        "schema_version": "8dionysus_readme_agents_dispositions_v1",
                        "records": [
                            {
                                "repository": "8Dionysus",
                                "path": "obsolete/README.md",
                                "review_state": "reviewed",
                                "disposition": "delete-obsolete-placeholder",
                                "owner_evidence": ["owner:obsolete/README.md"],
                            },
                            {
                                "repository": "8Dionysus",
                                "path": "expected/README.md",
                                "review_state": "reviewed",
                                "disposition": "keep",
                                "owner_evidence": ["owner:expected/README.md"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            payload = audit_agents_map.build_agents_map(
                workspace,
                known_repositories=("8Dionysus",),
                include_extra_repos=False,
                disposition_manifest_path=dispositions,
            )

            self.assertEqual(
                payload["disposition_issues"],
                [
                    "disposition target is absent from current corpus: "
                    "8Dionysus:expected/README.md"
                ],
            )

    def test_public_baseline_is_stable_and_json_serializable(self) -> None:
        payload = audit_agents_map.build_public_baseline_map()
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

        self.assertEqual(payload["audit_mode"], "public-baseline")
        self.assertEqual(payload["totals"]["known_public_repositories"], 20)
        self.assertIn("Agents-of-Abyss", payload["known_repositories"])
        self.assertIn("abyss-machine", payload["known_repositories"])
        self.assertIn("aoa-dashboard", payload["known_repositories"])
        self.assertIn("aoa-models", payload["known_repositories"])
        self.assertIn("aoa-session-memory", payload["known_repositories"])
        self.assertIn("aoa-agon", audit_agents_map.KNOWN_REPO_NAMES)
        self.assertNotIn("aoa-agon", payload["known_repositories"])
        self.assertIn("agents_map_public_baseline", rendered)
        self.assertNotIn("/mnt/", rendered)

    def test_markdown_report_contains_regeneration_commands_and_issue_legend(self) -> None:
        payload = audit_agents_map.build_public_baseline_map()
        markdown = audit_agents_map.render_markdown(payload)

        self.assertIn("python scripts/audit_agents_map.py", markdown)
        self.assertIn("--workspace-root <workspace-root>", markdown)
        self.assertIn("recon_agents_frontier.py", markdown)
        self.assertIn("AGENTS_FRONTIER_RECON", markdown)
        self.assertIn("unvalidated_nested_agents", markdown)
        self.assertIn("high_risk_dirs_without_agents", markdown)
        self.assertIn("8Dionysus", markdown)


if __name__ == "__main__":
    unittest.main()
